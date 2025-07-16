# agents/collector_agent.py
'''
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
'''

# agents/brand_signal_collector.py

import asyncio
from datetime import datetime
from typing import Dict
from agents.tools.infosys_integrations import FinacleAPI, AssistEdgeRPA
from pydantic import BaseModel, Field

class BrandSignalCollectorInput(BaseModel):
    company: str = Field(..., description="Name of the company to analyze")

async def collect_signals(company: str) -> Dict:
    finacle = FinacleAPI()
    assistedge = AssistEdgeRPA()

    # Run in parallel
    tasks = [
        finacle.get_client_metrics(company),
        assistedge.collect_social_sentiment(company),
        assistedge.collect_news_coverage(company)
    ]
    metrics, social, news = await asyncio.gather(*tasks)

    timestamp = datetime.utcnow().isoformat()

    return {
        "company": company,
        "metrics": metrics,
        "social_sentiment": social,
        "news_articles": news,
        "collected_at": timestamp
    }

def brand_signal_collector(state: dict) -> dict:
    """Collects brand-related signals from simulated APIs."""
    company = state.get("company")
    if not company:
        raise ValueError("Missing 'company' in state for brand_signal_collector")

    signals = asyncio.run(collect_signals(company))
    state["brand_signals"] = signals
    return state
