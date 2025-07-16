# agents/collector_agent.py
def brand_signal_collector(state: dict) -> dict:
    """Fetch brand signal data from mock sources."""
    company = state.get("brand_attr", "analyst visibility")
    state["raw_signals"] = {
        "news": f"Positive coverage on {company}",
        "reddit": f"Retail buzz around {company}",
        "twitter": f"Influencers are bullish on {company}",
        "reports": f"Analyst reports signal growing interest in {company}"
    }
    state["next"] = "forecast"
    return state
