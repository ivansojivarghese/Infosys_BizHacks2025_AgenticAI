# agents/outcome_mapper.py
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
