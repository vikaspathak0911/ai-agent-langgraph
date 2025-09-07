# graph_enhanced.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
from datetime import datetime, timezone
from tools import product_search, size_recommender, eta, order_lookup, order_cancel, parse_price, parse_tags

# ---------- State ----------
class AgentState(TypedDict):
    user_input: str
    intent: Optional[str]
    tools_called: List[str]
    evidence: List[dict]
    policy_decision: Optional[dict]
    final_message: str

# ---------- Router ----------
def router(state: AgentState):
    text = state["user_input"].lower()
    if "dress" in text or "wedding" in text or "size" in text:
        state["intent"] = "product_assist"
    elif "order" in text or "cancel" in text:
        state["intent"] = "order_help"
    else:
        state["intent"] = "other"
    return {"intent": state["intent"]}

# ---------- Tool Selector ----------
def tool_selector(state: AgentState):
    text = state["user_input"].lower()
    intent = state["intent"]
    tools_called, evidence = [], []

    # Product Assist
    if intent == "product_assist":
        price_max = parse_price(text)
        tags = parse_tags(text)
        results = product_search(query=text, price_max=price_max, tags=tags)

        tools_called.append("product_search")
        evidence.extend(results)

        size_msg = size_recommender(text)
        tools_called.append("size_recommender")
        evidence.append({"size_recommendation": size_msg})

        eta_msg = eta("560001")  # optional: parse from text
        tools_called.append("eta")
        evidence.append({"eta": eta_msg})

    # Order Help
    elif intent == "order_help":
        order_id, email = None, None
        words = text.split()
        for w in words:
            if w.startswith("a") and w[1:].isdigit():
                order_id = w.upper()
        for w in words:
            if "@" in w:
                email = w

        order = order_lookup(order_id, email)
        tools_called.append("order_lookup")
        if order:
            evidence.append(order)

    # Guardrail / Other
    else:
        tools_called, evidence = [], []

    return {"tools_called": tools_called, "evidence": evidence}

# Wrappers for convenience
def product_tool_selector(state: AgentState):
    return tool_selector({**state, "intent": "product_assist"})

def order_tool_selector(state: AgentState):
    return tool_selector({**state, "intent": "order_help"})

# ---------- Policy Guard ----------
def policy_guard(state: AgentState):
    if state["intent"] != "order_help":
        return {"policy_decision": None}
    if not state["evidence"]:
        return {"policy_decision": {"cancel_allowed": False, "reason": "order not found"}}

    order = state["evidence"][0]
    now = datetime.now(timezone.utc)
    decision = order_cancel(order, now=now)
    return {"policy_decision": decision}

# ---------- Responder ----------
def responder(state: AgentState):
    intent = state["intent"]
    evidence = state.get("evidence", [])
    policy = state.get("policy_decision")
    tools_called = state.get("tools_called", [])

    trace = {
        "intent": intent,
        "tools_called": tools_called,
        "evidence": evidence,
        "policy_decision": policy,
        "final_message": ""
    }

 # Product Assist
    if intent == "product_assist":
        product_lines = []
        for p in evidence:
            if "title" not in p:
                continue
            title = p.get("title", "")
            price = p.get("price", "")
            sizes = ",".join(p.get("sizes", []))
            color = p.get("color", "")
            size_rec = p.get("size_recommendation", "")
            tags = ",".join(p.get("tags", []))
            eta_msg = p.get("eta", "")
            
            line_parts = [f"{title}"]
            if price: line_parts.append(f"${price}")
            if sizes: line_parts.append(f"Sizes: {sizes}")
            if color: line_parts.append(f"Color: {color}")
            if size_rec: line_parts.append(f"Recommended Size: {size_rec}")
            if tags: line_parts.append(f"Tags: {tags}")
            if eta_msg: line_parts.append(f"ETA: {eta_msg}")
            
            product_lines.append(" | ".join(line_parts))
        
        if product_lines:
            message = "Here are some options:\n" + "\n".join(product_lines)
        else:
            message = "No matching products found."

    # Order Help
    elif intent == "order_help":
        if policy and policy.get("cancel_allowed"):
            message = "Your order was successfully cancelled."
        else:
            reason = policy.get("reason","")
            message = f"Cancellation not allowed ({reason}). You can: update shipping address, request store credit, or contact support."

    # Guardrail / Other
    else:
        message = "Sorry, I can’t provide discount codes. You can join our newsletter or check first-order perks."

    trace["final_message"] = message
    return trace

# ---------- Build Graph ----------
workflow = StateGraph(AgentState)
workflow.add_node("Router", router)
workflow.add_node("ToolSelector", tool_selector)
workflow.add_node("PolicyGuard", policy_guard)
workflow.add_node("Responder", responder)

workflow.set_entry_point("Router")
workflow.add_edge("Router", "ToolSelector")
workflow.add_edge("ToolSelector", "PolicyGuard")
workflow.add_edge("PolicyGuard", "Responder")
workflow.add_edge("Responder", END)

agent = workflow.compile()
