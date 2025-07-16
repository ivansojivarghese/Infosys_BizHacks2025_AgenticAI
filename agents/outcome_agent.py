# agents/outcome_mapper.py
'''
def outcome_mapper(state: dict) -> dict:
    """Map forecast + simulation into business KPI estimates."""
    forecast = state.get("forecast", "")
    sim = state.get("simulated_scenario", "")
    state["ipo_impact"] = {
        "valuation_shift": "+$45M",
        "lead_conversion_delta": "+11%",
        "analyst_coverage_index": "↑ moderate"
    }
    state["next"] = "advise"
    return state

'''

'''
# agents/outcome_mapper.py
from typing import Dict

def outcome_mapper(state: dict) -> dict:
    """Maps forecasted brand and sentiment shifts to IPO deal outcomes."""
    impact = state.get("ipo_impact", {})
    company = state.get("company", "UnknownCo")
    base_success_prob = 0.6  # base IPO success probability

    sentiment = impact.get("adjusted_sentiment", 0.5)
    lead_growth = float(impact.get("lead_conversion_delta", "+0%" ).strip("+%"))
    valuation_lift = float(impact.get("valuation_shift", "+0%" ).strip("+%"))

    # Weighted formula to project IPO success likelihood
    success_prob = base_success_prob + 0.2 * sentiment + 0.1 * (lead_growth / 100)
    success_prob = min(0.99, round(success_prob, 2))

    # Estimated final valuation multiplier
    multiplier = 1 + (valuation_lift / 100)
    est_valuation = round(2.5e9 * multiplier, 2)

    state["ipo_outcome"] = {
        "ipo_success_probability": success_prob,
        "expected_valuation": est_valuation,
        "confidence_factors": [
            "Sentiment boost from recent PR",
            "Analyst index trending up",
            "Lead conversions tracking well"
        ]
    }
    return state
'''

# agents/outcome_agent.py
from typing import Dict, List
from datetime import datetime


RISK_FACTORS = [
    "Social sentiment volatility detected",
    "Competitor IPO announced",
    "Execution risk",
    "Regulatory uncertainty"
]


def map_to_outcome_model(sentiment_score: float, emotion: str, scenario_data: Dict) -> Dict:
    """Maps simulated perception to predicted IPO outcome metrics."""
    risk_multiplier = 1.0
    if emotion == "cautious":
        risk_multiplier += 0.2

    base_range = {
        "low": 2.2e9,
        "mid": 2.5e9,
        "high": 2.8e9
    }
    shift = sentiment_score * 0.1 * risk_multiplier

    return {
        "valuation_estimates": {
            "low": base_range["low"] * (1 + shift),
            "mid": base_range["mid"] * (1 + shift),
            "high": base_range["high"] * (1 + shift),
        },
        "risk_factors": RISK_FACTORS if sentiment_score < 0 else RISK_FACTORS[:2],
        "timestamp": datetime.now().isoformat()
    }


def outcome_mapper(state: dict) -> dict:
    """Maps brand sentiment to IPO financial projections."""
    sentiment_score = state.get("sentiment_score", 0.0)
    emotion = state.get("emotion", "neutral")
    scenario = state.get("scenario_simulation", {})

    results = map_to_outcome_model(sentiment_score, emotion, scenario)
    state["ipo_impact"] = results
    return state
