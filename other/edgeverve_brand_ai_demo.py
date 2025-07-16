# --- AgentState class ---
class AgentState(dict):
    def get_input(self):
        return self.get("input", "")

# edgeverve_brand_ai_demo_advanced.py

import streamlit as st
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain.agents import tool
from langchain_core.runnables import RunnableLambda
import random
import os

# --- Define the LLM ---
llm = ChatGroq(
    model="mistral-saba-24b",
    temperature=0.4,
    api_key="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"
)

# --- Define Tools ---
@tool
def fetch_bloomberg_like_sentiment(company_name: str) -> str:
    """Returns simulated Bloomberg-like sentiment for a company."""
    sentiments = ["Positive institutional momentum", "Neutral", "Declining trust"]
    return f"Sentiment for {company_name}: {random.choice(sentiments)}"

@tool
def mocked_finacle_brand_metrics(company_id: str) -> str:
    """Returns mocked Finacle brand KPIs."""
    metrics = {
        "lead_score": random.randint(60, 90),
        "sentiment": random.choice(["Rising", "Flat", "Falling"]),
        "engagement_index": round(random.uniform(0.4, 0.9), 2)
    }
    return str(metrics)

@tool
def risk_check(input: str) -> str:
    """Checks for reputation or compliance risks."""
    risks = ["No major risk", "Potential overexposure", "Brand dilution in new markets"]
    return random.choice(risks)

@tool
def scenario_commentary(input: str) -> str:
    """Generates strategic commentary based on agent feedback."""
    prompt = f"""
    You are a financial brand strategist. A company increases {input}.
    Based on internal analytics and brand feedback, comment on likely perception shifts,
    investor trust, and downstream conversion gains.
    """
    response = llm.invoke(prompt)
    return response.content

# --- Agent Functions ---

def planner_agent(state: AgentState) -> dict:
    input_text = state.get_input()
    
    # naive company extraction logic
    company_name = input_text.split("for")[-1].strip() if "for" in input_text else "Company A"
    
    state["company"] = company_name
    return {"next": "research"}


def research_agent(state):
    state["sentiment"] = fetch_bloomberg_like_sentiment.invoke(state["company"])
    return {"next": "finacle"}

def finacle_agent(state):
    state["finacle"] = mocked_finacle_brand_metrics.invoke("CompanyA_ID")
    return {"next": "risk"}

def risk_agent(state):
    state["risk"] = risk_check.invoke(state["company"])
    return {"next": "commentary"}

def commentary_agent(state):
    input_summary = f"{state['sentiment']} + {state['finacle']} + {state['risk']}"
    state["summary"] = scenario_commentary.invoke(input_summary)
    return {"next": END}

# --- LangGraph Assembly ---
graph = StateGraph(AgentState)
graph.add_node("planner", planner_agent)
graph.add_node("research", research_agent)
graph.add_node("finacle", finacle_agent)
graph.add_node("risk", risk_agent)
graph.add_node("commentary", commentary_agent)

graph.set_entry_point("planner")
graph.add_edge("planner", "research")
graph.add_edge("research", "finacle")
graph.add_edge("finacle", "risk")
graph.add_edge("risk", "commentary")
graph.add_edge("commentary", END)

workflow = graph.compile()

# --- Streamlit UI ---
st.set_page_config(page_title="Agentic IPO Simulator Pro", layout="wide")
st.title("🏦 Agentic AI IPO Brand Scenario Planner")

scenario = st.text_input("Scenario to test (e.g., Boost analyst visibility in Q4)",
                         "Increase executive media mentions by 25%")

if st.button("Simulate Impact"):
    with st.spinner("Running multi-agent simulation..."):
        state = AgentState({"input": scenario})
        final = workflow.invoke(state)

        st.subheader("📊 Raw Metrics")
        st.write("Sentiment:", final["sentiment"])
        st.write("Finacle Metrics:", final["finacle"])
        st.write("Risk Assessment:", final["risk"])

        st.subheader("🧠 Strategic Commentary")
        st.info(final["summary"])
