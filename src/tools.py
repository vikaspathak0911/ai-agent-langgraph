# tools.py
import json
import os
import re
from datetime import datetime, timezone, timedelta
from difflib import get_close_matches


# ---------------- Data Load ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

PRODUCTS = json.load(open(os.path.join(DATA_DIR, "products.json")))
ORDERS = json.load(open(os.path.join(DATA_DIR, "orders.json")))

# ---------------- Helpers ----------------
import re

def parse_price(query: str):
    """
    Extract maximum price from user input.
    Returns a high default if no price mentioned.
    """
    query_lower = query.lower()

    # Patterns: "under $100", "less than 100", "below 120"
    match = re.search(r"(?:under|less than|below)\s*\$?(\d+)", query_lower)
    return int(match.group(1)) if match else float('inf')


def parse_tags(query: str):
    """Extract tags based on keywords in user input"""
    tags = []
    q = query.lower()
    if "wedding" in q: tags.append("wedding")
    if "midi" in q: tags.append("midi")
    if "party" in q: tags.append("party")
    if "day" in q or "daywear" in q: tags.append("daywear")
    return tags


# List of 100 common color names
COLOR_PALETTE = [
    "black", "white", "red", "blue", "green", "yellow", "pink", "orange",
    "purple", "brown", "grey", "violet", "indigo", "turquoise", "beige",
    "maroon", "navy", "olive", "teal", "lime", "magenta", "cyan", "gold",
    "silver", "bronze", "peach", "lavender", "cream", "mint", "coral",
    "apricot", "tan", "chocolate", "burgundy", "charcoal", "mustard",
    "khaki", "plum", "salmon", "sky blue", "rose", "emerald", "jade",
    "amber", "sapphire", "ruby", "copper", "ivory", "mauve", "lemon",
    "cerulean", "fuchsia", "cerise", "orchid", "wheat", "cinnamon", "sienna",
    "periwinkle", "lavender blush", "pale green", "forest green", "sea green",
    "slate gray", "midnight blue", "electric blue", "pearl", "blush", "cream white",
    "powder blue", "rust", "burgundy red", "cherry", "almond", "coffee",
    "mahogany", "taupe", "sand", "jet black", "mint green", "baby blue",
    "bubblegum pink", "canary yellow", "raspberry", "plum purple", "fawn",
    "ash gray", "smoke", "emerald green", "lemon yellow", "cobalt", "aqua",
    "denim", "charcoal gray", "olive drab", "seafoam", "moss green", "indian red",
    "celeste", "cream yellow", "peacock", "carmine", "topaz"
]

def parse_color(query: str, products=None, return_all=False):
    """
    Detect color from user query based on a 100-color palette.
    Optionally map to product colors if a product list is provided.
    """
    query_clean = re.sub(r"[^\w\s]", "", query.lower())
    words = query_clean.split()

    # Exact matches from the palette
    matches = [color for color in COLOR_PALETTE if color in query_clean]

    # Fuzzy match fallback
    if not matches:
        for word in words:
            close = get_close_matches(word, COLOR_PALETTE, n=1, cutoff=0.7)
            if close:
                matches.append(close[0])

    if not matches:
        return None

    detected_colors = matches if return_all else [matches[0]]

    # Map detected colors to product colors if products provided
    if products:
        product_colors = {p["color"].lower(): p["color"] for p in products}
        mapped_colors = []
        for color in detected_colors:
            # Fuzzy match to product colors
            close = get_close_matches(color, product_colors.keys(), n=1, cutoff=0.7)
            if close:
                mapped_colors.append(product_colors[close[0]])
        return mapped_colors if return_all else mapped_colors[0] if mapped_colors else None

    return detected_colors if return_all else detected_colors[0]


# ---------------- Product Tools ----------------
def product_search(query, price_max=None, tags=None):
    """
    Return up to 2 products matching query, price, tags, and optional color.
    Respects 'under $X' as price ≤ X.
    """
    price_max = price_max or parse_price(query)
    tags = tags or parse_tags(query)
    color = parse_color(query)

    results = []
    for p in PRODUCTS:
        # Price filter
        if p["price"] > price_max:
            continue

        # Tag filter
        if tags and not all(tag in p["tags"] for tag in tags):
            continue

        # Color filter
        if color and p["color"].lower() != color.lower():
            continue

        results.append(p)

    # Sort by price ascending before returning top 2
    results = sorted(results, key=lambda x: x["price"])
    return results[:2]


def size_recommender(user_input):
    text = user_input.lower()

    # Defaults
    height = "average"
    weight = "average"
    fit = "regular"

    # Detect height
    if any(word in text for word in ["tall", "high", "long"]):
        height = "tall"
    elif any(word in text for word in ["short", "small"]):
        height = "short"

    # Detect build/weight
    if any(word in text for word in ["slim", "thin", "light"]):
        weight = "slim"
    elif any(word in text for word in ["medium", "average", "normal"]):
        weight = "medium"
    elif any(word in text for word in ["heavy", "large", "big"]):
        weight = "large"

    # Detect fit preference
    if "loose" in text:
        fit = "loose"
    elif "tight" in text or "slim fit" in text:
        fit = "tight"

    # Size decision rules
    if weight == "slim":
        size = "S" if fit != "loose" else "M"
    elif weight == "medium":
        size = "M" if fit != "loose" else "L"
    else:  # large/heavy
        size = "L" if fit != "loose" else "XL"

    # Adjust for height
    if height == "tall" and size != "XL":
        size += "-Tall"

    return f"Based on your input, we recommend size {size} ({fit} fit)."

# ZIP code region mapping
shipping_regions = {
    "East": {"zip_range": range(10000, 20000), "standard": (3, 5)},    # (min_days, max_days)
    "Midwest": {"zip_range": range(50000, 60000), "standard": (4, 6)},
    "West": {"zip_range": range(90000, 100000), "standard": (5, 7)},
}

DEFAULT_PROCESSING_DAYS = 2  # Default processing time added to range

def eta(zip_code):
    """
    Return ETA as a range of days (e.g., '2-5 days') based on ZIP code.
    
    Args:
        zip_code (int): Customer ZIP code
    Returns:
        str: ETA range as a string
    """
    # Default range if ZIP not found
    min_days, max_days = 4, 7
    
    for region, info in shipping_regions.items():
        if zip_code in info["zip_range"]:
            region_min, region_max = info["standard"]
            min_days = region_min + DEFAULT_PROCESSING_DAYS
            max_days = region_max + DEFAULT_PROCESSING_DAYS
            break
    
    return f"{min_days}-{max_days} days"

# ---------------- Order Tools ----------------
def order_lookup(order_id, email):
    """Lookup order dynamically by ID + email from orders.json"""
    for o in ORDERS:
        if o["order_id"].lower() == order_id.lower() and o["email"].lower() == email.lower():
            return o
    return None

def order_cancel(order, now=None):
    """Return policy decision for cancellation"""
    if now is None:
        now = datetime.now(timezone.utc)
    created_at = datetime.fromisoformat(order["created_at"].replace("Z","+00:00"))
    elapsed = now - created_at
    if elapsed <= timedelta(minutes=60):
        return {"cancel_allowed": True}
    else:
        return {"cancel_allowed": False, "reason": ">60 min"}
