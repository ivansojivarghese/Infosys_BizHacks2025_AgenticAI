# agents/scenario_simulator.py
'''
from langchain.agents import tool
import random

def scenario_simulator(state: dict) -> dict:
    """Simulate hypothetical intervention and downstream brand effect."""
    options = [
        "+15% sentiment, better investor trust",
        "Neutral effect, marginal brand recall",
        "-5% due to overexposure"
    ]
    state["simulated_scenario"] = random.choice(options)
    state["next"] = "map"
    return state
'''

'''
# agents/scenario_simulator.py
from datetime import datetime
from typing import Dict


def scenario_simulator(state: dict) -> dict:
    """Accepts hypothetical brand actions and predicts downstream perception shifts."""
    brand_attr = state.get("brand_attr", "analyst visibility")
    change_pct = state.get("change_pct", 25)
    forecast = state.get("forecast", {})

    base_sentiment = forecast.get("combined_sentiment_score", 0.5)
    analyst_index = forecast.get("analyst_coverage_index", 50)

    # Heuristic simulation logic
    adjusted_sentiment = min(1.0, base_sentiment + (change_pct / 100) * 0.3)
    lead_conversion_delta = round(change_pct * 0.4, 1)
    valuation_shift = round(adjusted_sentiment * 0.15 * 100, 2)  # percent

    state["ipo_impact"] = {
        "adjusted_sentiment": adjusted_sentiment,
        "lead_conversion_delta": f"+{lead_conversion_delta}%",
        "valuation_shift": f"+{valuation_shift}%",
        "analyst_coverage_index": analyst_index + int(change_pct * 0.2)
    }
    return state
'''


# agents/scenario_simulator.py

from typing import Dict, List
from datetime import datetime

def analyze_institutional_questions(questions: List[str]) -> List[Dict]:
    """Analyze institutional investor questions for category, skepticism, and follow-up need."""
    categories = {
        "financial": ["revenue", "margin", "profit", "cash", "burn"],
        "competitive": ["competition", "moat", "differentiation", "market share"],
        "operational": ["scale", "execution", "team", "hiring"],
        "risk": ["risk", "concern", "challenge", "threat"],
        "growth": ["growth", "expansion", "TAM", "market size"]
    }

    skeptical_words = ["really", "actually", "but", "however", "concern", "worried"]

    analyzed = []
    for q in questions:
        lowered = q.lower()
        is_question = "?" in q

        matched_cats = [k for k, kw in categories.items() if any(w in lowered for w in kw)]
        skepticism_score = min(sum(1 for w in skeptical_words if w in lowered) / 3, 1.0)
        requires_followup = skepticism_score > 0.7

        analyzed.append({
            "question": q,
            "timestamp": datetime.now().isoformat(),
            "is_question": is_question,
            "primary_category": matched_cats[0] if matched_cats else "general",
            "categories": matched_cats,
            "skepticism_level": skepticism_score,
            "requires_followup": requires_followup
        })

    return analyzed


def scenario_simulator(state: dict) -> dict:
    """Simulates how brand perception evolves with actions and questions."""
    # Add scenario simulation placeholder
    state["scenario_simulation"] = {
        "message_amplification": "positive",
        "analyst_coverage_gain": 0.4,
        "expected_shift": +0.12  # Simulated uplift in sentiment
    }

    # Institutional question simulation analysis
    sample_questions = state.get("institutional_questions_raw", [])
    if isinstance(sample_questions, list) and sample_questions:
        state["institutional_questions"] = analyze_institutional_questions(sample_questions)

    return state
