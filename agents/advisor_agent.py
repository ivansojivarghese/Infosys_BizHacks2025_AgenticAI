# agents/advisor_chat_agent.py
from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    model="mistral-saba-24b",
    temperature=1.0,
    api_key="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"
)
def advisor_chat(state: dict) -> dict:
    """Returns final explanation from LangChain-powered LLM to the banker."""
    ipo_data = state.get("ipo_impact", {})
    summary = f"""
    Based on the signals and forecast:
    - Projected Valuation Shift: {ipo_data.get('valuation_shift')}
    - Expected Lead Conversion Change: {ipo_data.get('lead_conversion_delta')}
    - Analyst Coverage Outlook: {ipo_data.get('analyst_coverage_index')}

    Recommend amplifying analyst visibility in Q4 through earned media and thought leadership events.
    """
    state["final_advice"] = summary
    state["next"] = None  # End of flow
    return state
