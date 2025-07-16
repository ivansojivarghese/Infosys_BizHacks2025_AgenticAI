# agents/scenario_simulator.py
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