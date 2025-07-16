# Streamlit app: Agentic AI IPO Brand Impact Simulator with Multi-Agent Reasoning

from agent_graph import build_brand_simulation_graph

from orchestrator.ipo_simulator_orchestrator import ipo_orchestrator


# Build graph
workflow = build_brand_simulation_graph()

def main():
    import streamlit as st
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    from langchain_core.output_parsers import StrOutputParser
    from langchain_groq import ChatGroq
    from langchain.agents import tool
    from langgraph.graph import StateGraph, END
    # from langgraph.graph import State  # or whatever public API it uses
    import os
    import random

    # Page setup
    st.set_page_config(page_title="IPO Brand Impact Simulator", layout="wide")
    st.title("🚀 Agentic AI IPO Brand Impact Simulator")
    st.subheader("Simulate perception and lead impact of brand decisions in real-time")

    # Inputs
    company = st.text_input("Company Name", "YourCompany")
    brand_attr = st.text_input("Key Brand Attribute (e.g. Analyst Visibility)", "Executive media mentions")
    change_pct = st.slider("% Increase in Attribute", 0, 100, 25)
    market = st.selectbox("Target Market", ["India", "USA", "Singapore", "Global"])
    sector = st.selectbox("Industry Sector", ["Fintech", "Healthcare", "Energy", "AI/ML", "Logistics"])
    user_style = st.text_area("Optional: Add any notes or write your own scenario for stylistic adaptation (e.g., 'keep it casual', 'write like a McKinsey memo')", "")
    provider = st.selectbox("Inference Provider", ["Groq (default)", "Cloudflare Workers AI", "Together.ai"])

    # LangChain LLM Setup (Groq default)
    groq_llm = ChatGroq(
        model="mistral-saba-24b",
        temperature=1.0,
        api_key="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"  # Replace with your Groq API key
    )

    feedback_prompt = PromptTemplate(
        input_variables=["company", "brand_attr", "change_pct", "market", "sector", "user_style"],
        template="""
        {company}, a financial company in the {sector} sector, is increasing its {brand_attr} by {change_pct}% in the {market} market.
        Predict:
        - How will brand perception shift?
        - What will be the investor sentiment impact?
        - How will sales-qualified lead volume change?

        Respond with bullet points and clear reasoning. Use language suitable for investment bankers and IPO brand analysts. Avoid JSON or structured object formatting.
        Adapt tone and style based on: {user_style}
        """
    )

    chain = LLMChain(
        llm=groq_llm,
        prompt=feedback_prompt,
        output_parser=StrOutputParser()
    )

    import requests

    def cloudflare_infer(prompt):
        # Replace with your actual values
        account_id = "d8fc6219bc29c84b4dc5010ee8afd21a"
        model = "@cf/meta/llama-3-8b-instruct"  # e.g., "@cf/meta/llama-2-7b-chat-int8"
        api_token = "eMoOJw84F55W4FKMa9pzSZ7KrU0VB7FFc-rlF_Ze"
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"

        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        data = {
            "input": prompt
        }
        response = requests.post(url, headers=headers, json=data)
        if response.ok:
            # Adjust this depending on the actual response structure
            return response.json().get("result", "No result")
        else:
            return f"Cloudflare API error: {response.text}"

    # Together.ai integration (placeholder)
    def together_infer(prompt):
        # Replace with your actual values
        api_key = "e4e865e00e428d4136bf9b2996d25334496c29bd0a7caf0415ee2f13845fecbd"
        model = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # e.g., "togethercomputer/llama-2-7b-chat"
        url = "https://api.together.xyz/inference"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "prompt": prompt,
            "max_tokens": 512,
            "temperature": 0.7
        }
        response = requests.post(url, headers=headers, json=data)
        if response.ok:
            # Adjust this depending on the actual response structure
            return response.json().get("output", "No result")
        else:
            return f"Together.ai API error: {response.text}"
    
    # Live Finacle CRM integration (placeholder)
    @tool
    def finacle_crm_tool(company_id: str) -> str:
        """Fetch live CRM data from Finacle (EdgeVerve)"""
        # TODO: Replace with real Finacle API call
        # Example: requests.get(f'https://finacle.example.com/api/crm/{company_id}', headers={...})
        # Simulate live data
        return f"[LIVE] CRM metrics for {company_id}: Lead score {random.randint(70,99)}, Analyst mentions up {random.randint(10,40)}%, Mood index: {'Bullish' if random.random()>0.5 else 'Bearish'}"

    @tool
    def simulated_market_feed_tool(company: str) -> str:
        """Simulate real-time Bloomberg-like sentiment for demo"""
        sentiments = ["Strong buy signals from analysts", "Volatile institutional buzz", "Investor caution due to ESG concerns"]
        return f"Market Feed: {random.choice(sentiments)} for {company}"

    # Simulate agentic feedback
    if st.button("Simulate Brand Impact"):
        with st.spinner("Running multi-agent reasoning and real-time inference..."):
            try:
                # Prepare prompt for external providers
                prompt_text = feedback_prompt.format(
                    company=company,
                    brand_attr=brand_attr,
                    change_pct=change_pct,
                    market=market,
                    sector=sector,
                    user_style=user_style
                )

                if provider == "Groq (default)":
                    response = chain.invoke({
                        "company": company,
                        "brand_attr": brand_attr,
                        "change_pct": change_pct,
                        "market": market,
                        "sector": sector,
                        "user_style": user_style
                    })
                elif provider == "Cloudflare Workers AI":
                    response = cloudflare_infer(prompt_text)
                elif provider == "Together.ai":
                    response = together_infer(prompt_text)
                else:
                    response = "[Error] Unknown provider."

                st.success("Simulation complete")
                st.markdown("---")
                st.markdown(f"#### 🤖 Agent Commentary ({provider})")
                # Only show the text output, not JSON
                if isinstance(response, dict) and "text" in response:
                    st.markdown(response["text"])
                else:
                    st.markdown(response)

                input_state = {
                    "brand_attr": brand_attr,
                    "change_pct": change_pct,
                    "market": market,
                    "sector": sector,
                    "user_style": user_style,
                }

                # final_state = workflow.invoke(input_state)

                # Optionally: combine both
                full_state = {
                    "company": company,
                    "quarter": "Q4 2025",  # or make dynamic
                    "brand_attr": brand_attr,
                    "change_pct": change_pct,
                    "market": market,
                    "sector": sector,
                    "user_style": user_style,
                }

                advisor_result = ipo_orchestrator.invoke(full_state)

                st.success("Multi-Agent Simulation Complete ✅")
                st.markdown("### 🧠 Final Advisor Summary")
                st.markdown(advisor_result.get("advisor_summary", "No summary available"))

                st.markdown("#### 🛰️ Market Sentiment (Bloomberg-like)")
                st.info(simulated_market_feed_tool.invoke(company))

                st.markdown("#### 🔌 Finacle CRM Snapshot (Live)")
                st.info(finacle_crm_tool.invoke(company))

            except Exception as e:
                st.error(f"Simulation failed: {e}")


if __name__ == "__main__":
    main()
