# tools.py
import json
import os
import re
from datetime import datetime, timezone, timedelta

# ---------------- Data Load ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

PRODUCTS = json.load(open(os.path.join(DATA_DIR, "products.json")))
ORDERS = json.load(open(os.path.join(DATA_DIR, "orders.json")))

# ---------------- Helpers ----------------
def parse_price(query: str):
    """Extract max price from user input (e.g. 'under $120')"""
    match = re.search(r"under\s*\$?(\d+)", query.lower())
    return int(match.group(1)) if match else 999

def parse_tags(query: str):
    """Extract tags based on keywords in user input"""
    tags = []
    q = query.lower()
    if "wedding" in q: tags.append("wedding")
    if "midi" in q: tags.append("midi")
    if "party" in q: tags.append("party")
    if "day" in q or "daywear" in q: tags.append("daywear")
    return tags

def parse_color(query: str):
    """Extract color keyword from query if it matches a product"""
    q = query.lower()
    for p in PRODUCTS:
        if p["color"].lower() in q:
            return p["color"]
    return None

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
    if "m/l" in user_input.lower():
        return "We recommend size M for medium build, L if you prefer loose fit."
    return "Size M is most common."

def eta(zip_code):
    return "2-5 days"

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
