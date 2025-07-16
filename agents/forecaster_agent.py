# agents/perception_forecaster.py
'''
def perception_forecaster(state: dict) -> dict:
    """Forecasts brand sentiment using mocked time-series analysis."""
    raw = state.get("raw_signals", {})
    forecast = "Expected +8% brand sentiment in 3 weeks due to rising analyst/media momentum."
    state["forecast"] = forecast
    state["next"] = "simulate"
    return state
'''

'''
# agents/perception_forecaster.py
from agents.tools.infosys_integrations import TopazAI

# Initialize Topaz AI (sentiment + NER)
topaz_ai = TopazAI()

def perception_forecaster(state: dict) -> dict:
    """Use Topaz sentiment model to forecast perception based on analyst and social data."""
    social_data = state.get("social_sentiment", {})
    news_data = state.get("news_articles", [])

    # Aggregate sentiment and generate score
    social_pos = social_data.get("sentiment_distribution", {}).get("positive", 0.5)
    news_sentiment = sum(article.get("sentiment", 0.5) for article in news_data) / max(len(news_data), 1)
    combined_sentiment = (0.4 * social_pos) + (0.6 * news_sentiment)

    # Simulate analyst coverage metric
    analyst_index = 50 + int(25 * combined_sentiment)

    state["forecast"] = {
        "combined_sentiment_score": round(combined_sentiment, 2),
        "analyst_coverage_index": analyst_index
    }
    return state
'''


# agents/perception_forecaster.py
from datetime import datetime
from typing import Dict, List

# Simulated Topaz FinBERT sentiment model
POSITIVE_KEYWORDS = ["growth", "confident", "strong", "innovation", "leadership"]
NEGATIVE_KEYWORDS = ["risk", "concern", "challenge", "uncertain", "volatile"]


def analyze_sentiment(text: str) -> Dict:
    words = text.lower().split()
    pos_score = sum(1 for word in POSITIVE_KEYWORDS if word in words)
    neg_score = sum(1 for word in NEGATIVE_KEYWORDS if word in words)

    raw_sentiment = (pos_score - neg_score) / max(1, len(words))
    sentiment_score = max(-1, min(1, raw_sentiment * 10))

    if sentiment_score > 0.2:
        label = "positive"
    elif sentiment_score < -0.2:
        label = "negative"
    else:
        label = "neutral"

    emotion = "confident" if sentiment_score > 0.4 else "cautious" if sentiment_score < -0.4 else "neutral"

    key_phrases = []
    for keyword in POSITIVE_KEYWORDS + NEGATIVE_KEYWORDS:
        if keyword in text.lower():
            key_phrases.append(keyword)

    return {
        "sentiment_score": sentiment_score,
        "sentiment_label": label,
        "emotion_detected": emotion,
        "key_phrases": key_phrases,
        "timestamp": datetime.now().isoformat()
    }


def perception_forecaster(state: dict) -> dict:
    """Forecasts brand perception and extracts sentiment/emotion metrics."""
    text = state.get("brand_signals_text", "")
    analysis = analyze_sentiment(text)

    state["forecast_output"] = {
        "sentiment_score": analysis["sentiment_score"],
        "sentiment_label": analysis["sentiment_label"],
        "emotion": analysis["emotion_detected"],
        "key_phrases": analysis["key_phrases"],
        "timestamp": analysis["timestamp"]
    }

    # For downstream scenario simulator
    state["sentiment_score"] = analysis["sentiment_score"]
    state["emotion"] = analysis["emotion_detected"]
    state["key_phrases"] = analysis["key_phrases"]

    return state

