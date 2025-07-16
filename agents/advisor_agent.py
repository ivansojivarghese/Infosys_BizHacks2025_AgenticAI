# agents/advisor_chat_agent.py
'''
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
    state["advisor_summary"] = summary
    state["next"] = None  # End of flow
    return state
'''

from datetime import datetime
from typing import Dict, List

# agents/advisor_chat.py
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from langchain.output_parsers import StrOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

# Load Groq LLM (adjust as needed)
llm = ChatGroq(
    model="mistral-saba-24b",
    temperature=1.0,
    api_key="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"
)

# Prompt template for generating banker-style advice
advisor_prompt = PromptTemplate(
    input_variables=["company", "ipo_impact", "brand_attr", "sector", "market"],
    template="""
    You are a senior investment banking associate advising on IPO readiness for {company}.

    Based on the following simulation results:
    - Company: {company}
    - Market: {market}
    - Sector: {sector}
    - Brand Attribute: {brand_attr}
    - Simulated IPO Impact: {ipo_impact}

    Provide a clear and concise strategic advisory memo:
    - What should the company do next?
    - What are the risks and trade-offs?
    - How should this be communicated to institutional investors?

    Write in the tone of a McKinsey or BCG memo. Use bullet points and crisp reasoning.
    """
)

advisor_chain = LLMChain(llm=llm, prompt=advisor_prompt, output_parser=StrOutputParser())


def advisor_chat(state: dict) -> dict:
    """Generates strategic advisory output from simulation results."""
    response = advisor_chain.invoke({
        "company": state.get("company", "The Company"),
        "ipo_impact": state.get("ipo_impact", {}),
        "brand_attr": state.get("brand_attr", "Analyst visibility"),
        "market": state.get("market", "Global"),
        "sector": state.get("sector", "Fintech")
    })
    # Ensure raw string is extracted, regardless of LLMChain formatting
    if isinstance(response, dict) and "text" in response:
        state["advisor_summary"] = response["text"].strip()
    elif isinstance(response, str):
        state["advisor_summary"] = response.strip()
    else:
        state["advisor_summary"] = str(response).strip()

    return state

'''
def generate_immediate_actions(sentiment_score: float, skepticism: float, emotion: str) -> List[str]:
    actions = []
    if sentiment_score < -0.3:
        actions.append("Acknowledge investor concerns and present specific metrics.")
    if skepticism > 0.7:
        actions.append("Incorporate concrete customer examples in responses.")
    if emotion == "cautious":
        actions.append("Increase delivery confidence and energy.")
    return actions if actions else ["Maintain current communication approach."]

def adjust_talking_points(categories: List[str], sentiment_trend: str) -> Dict:
    adjust = {"emphasize": [], "de_emphasize": [], "add": []}
    if "financial" in categories:
        adjust["emphasize"].append("Path to profitability")
        adjust["add"].append("More granular unit economics")
    if "competitive" in categories:
        adjust["emphasize"].append("Tech differentiation")
        adjust["de_emphasize"].append("Broad market size claims")
    if sentiment_trend == "improving":
        adjust["emphasize"].append("Long-term vision")
    return adjust

def suggest_body_language(emotion: str, sentiment_score: float) -> List[str]:
    cues = []
    if sentiment_score < 0:
        cues.extend([
            "Maintain eye contact and open posture.",
            "Use deliberate hand gestures to emphasize key points."
        ])
    if emotion == "cautious":
        cues.append("Slow down speech and lean forward slightly to show sincerity.")
    return cues

def synthesize_memo(score: float, trend: str, probability: float) -> str:
    if probability > 0.7 and trend == "improving":
        return "Session is progressing well — sustain momentum and close with long-term vision."
    elif probability < 0.4:
        return "Investor confidence is low — prioritize data-backed reassurance and targeted follow-up."
    elif trend == "declining":
        return "Engagement is weakening — increase narrative strength and address emerging doubts."
    return "Neutral outlook — enhance clarity and distinctiveness in responses."

def advisor_chat(state: dict) -> dict:
    """Generates strategic advisory output from simulation results."""
    sentiment_score = state.get("sentiment_score", 0.0)
    emotion = state.get("emotion", "neutral")
    skepticism = max((q.get("skepticism_level", 0.0) for q in state.get("institutional_questions", [])), default=0.0)
    categories = list({q.get("primary_category") for q in state.get("institutional_questions", []) if q.get("primary_category")})
    sentiment_trend = state.get("sentiment_trend", "stable")
    success_prob = state.get("ipo_impact", {}).get("valuation_estimates", {}).get("mid", 0) / 2.5e9  # rough baseline

    state["advisor_summary"] = {
        "timestamp": datetime.now().isoformat(),
        "immediate_actions": generate_immediate_actions(sentiment_score, skepticism, emotion),
        "talking_points": adjust_talking_points(categories, sentiment_trend),
        "body_language_tips": suggest_body_language(emotion, sentiment_score),
        "memo": synthesize_memo(sentiment_score, sentiment_trend, success_prob)
    }

    return state
'''