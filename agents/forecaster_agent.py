# agents/perception_forecaster.py
def perception_forecaster(state: dict) -> dict:
    """Forecasts brand sentiment using mocked time-series analysis."""
    raw = state.get("raw_signals", {})
    forecast = "Expected +8% brand sentiment in 3 weeks due to rising analyst/media momentum."
    state["forecast"] = forecast
    state["next"] = "simulate"
    return state
