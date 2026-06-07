import warnings
warnings.filterwarnings("ignore")
from typing import TypedDict
from langgraph.graph import StateGraph, END


# ------------------
# State Definition
# ------------------

class SupportState(TypedDict):
    query: str
    category: str
    faq_answer: str
    escalate: bool
    response: str


# ------------------
# Agent 1: Triage
# ------------------

def triage_agent(state):

    query = state["query"].lower()

    if "order" in query:
        category = "Delivery Issue"

    elif "payment" in query:
        category = "Payment Issue"

    else:
        category = "General Query"

    state["category"] = category

    print("Triage Agent:", category)

    return state


# ------------------
# Agent 2: FAQ
# ------------------

def faq_agent(state):

    faq_database = {
        "Delivery Issue":
            "Orders usually arrive within 5-7 business days.",

        "Payment Issue":
            "Payments are verified within 24 hours.",

        "General Query":
            "Please contact support."
    }

    state["faq_answer"] = faq_database[state["category"]]

    print("FAQ Agent:", state["faq_answer"])

    return state


# ------------------
# Agent 3: Escalation
# ------------------

def escalation_agent(state):

    query = state["query"].lower()

    urgent_words = [
        "20 days",
        "refund",
        "fraud",
        "legal",
        "complaint",
        "manager"
    ]

    state["escalate"] = any(
        word in query
        for word in urgent_words
    )

    print("Escalation Agent:", state["escalate"])

    return state


# ------------------
# Agent 4: Response
# ------------------

def response_agent(state):

    if state["escalate"]:

        state["response"] = """
Issue requires human support.
Your request has been escalated.
"""

    else:

        state["response"] = f"""
Category: {state['category']}

Suggested Answer:
{state['faq_answer']}
"""

    print("Response Agent Complete")

    return state


# ------------------
# Build Graph
# ------------------

graph = StateGraph(SupportState)

graph.add_node("triage", triage_agent)
graph.add_node("faq", faq_agent)
graph.add_node("escalation", escalation_agent)
graph.add_node("response", response_agent)

graph.set_entry_point("triage")

graph.add_edge("triage", "faq")
graph.add_edge("faq", "escalation")
graph.add_edge("escalation", "response")
graph.add_edge("response", END)

app = graph.compile()

# ------------------
# Run Workflow
# ------------------

query = input("Enter customer query: ")

print("Workflow started")
result = app.invoke(
    {
        "query": query,
        "category": "",
        "faq_answer": "",
        "escalate": False,
        "response": ""
    }
)

print("\nFINAL RESPONSE")
print(result["response"])