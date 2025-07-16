# groq_sim_engine.py
from groq import Groq
import os

client = Groq(api_key="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")

def simulate_feedback(brand_attr, market, change_pct):
    prompt = f"""
    A company is increasing its {brand_attr} by {change_pct}% in the {market} market.
    Predict the likely changes in brand perception, investor engagement, and sales-qualified leads.
    Give detailed commentary.
    """

    response = client.chat.completions.create(
        model="mistral-saba-24b",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
    )
    return response.choices[0].message.content
