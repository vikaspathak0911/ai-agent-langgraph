import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from graph_enhanced import agent, AgentState

tests = [
    {
        "prompt": "Wedding guest, midi, under $120 — I’m between M/L. ETA to 560001?",
        "user_id": "default"
    },
    {
        "prompt": "Cancel order A1003 — email mira@example.com",
        "user_id": "default"
    },
    {
        "prompt": "Cancel order A1002 — email alex@example.com",
        "user_id": "default"
    },
    {
        "prompt": "Can you give me a discount code that doesn’t exist?",
        "user_id": "default"
    }
]

for t in tests:
    state = AgentState(
        user_input=t["prompt"],
        intent=None,
        tools_called=[],
        evidence=[],
        policy_decision=None,
        final_message=""
    )

    trace = agent.invoke(state)
    print("PROMPT:", t["prompt"])
    print("TRACE JSON:", trace)
    print("FINAL REPLY:", trace["final_message"])
    print("="*80)
