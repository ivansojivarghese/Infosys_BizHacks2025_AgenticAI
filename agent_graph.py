# agent_graph.py
from langgraph.graph import StateGraph, END
from agents.collector_agent import brand_signal_collector
from agents.forecaster_agent import perception_forecaster
from agents.simulator_agent import scenario_simulator
from agents.outcome_agent import outcome_mapper
from agents.advisor_agent import advisor_chat

def build_brand_simulation_graph():
    graph = StateGraph(dict)

    graph.add_node("collect_signals", brand_signal_collector)
    graph.add_node("forecast_perception", perception_forecaster)
    graph.add_node("simulate_action", scenario_simulator)
    graph.add_node("map_to_metrics", outcome_mapper)
    graph.add_node("advisor_chat", advisor_chat)

    graph.set_entry_point("collect_signals")
    graph.add_edge("collect_signals", "forecast_perception")
    graph.add_edge("forecast_perception", "simulate_action")
    graph.add_edge("simulate_action", "map_to_metrics")
    graph.add_edge("map_to_metrics", "advisor_chat")
    graph.add_edge("advisor_chat", END)

    return graph.compile()
