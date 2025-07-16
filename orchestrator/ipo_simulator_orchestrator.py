# langgraph_orchestrator.py
from langgraph.graph import StateGraph, END
from agents.collector_agent import brand_signal_collector
from agents.forecaster_agent import perception_forecaster
from agents.simulator_agent import scenario_simulator
from agents.outcome_agent import outcome_mapper
from agents.advisor_agent import advisor_chat

# Define LangGraph
workflow = StateGraph(dict)

# Add nodes for each agent
workflow.add_node("collect", brand_signal_collector)
workflow.add_node("forecast", perception_forecaster)
workflow.add_node("simulate", scenario_simulator)
workflow.add_node("map", outcome_mapper)
workflow.add_node("advise", advisor_chat)

# Define graph flow
workflow.set_entry_point("collect")
workflow.add_edge("collect", "forecast")
workflow.add_edge("forecast", "simulate")
workflow.add_edge("simulate", "map")
workflow.add_edge("map", "advise")
workflow.add_edge("advise", END)

# Compile
# Compile and expose
ipo_orchestrator = workflow.compile()

