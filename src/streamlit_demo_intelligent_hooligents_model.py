import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time

from models.person import PersonHandler
from models.streckennetz import Streckennetz
from models.intelligent_hooligents_model import IntelligentHooligentsModel
from models.abstract.route_calculator import RouteCalculator
from models.abstract.passenger_exchange_handler import PassengerExchangeHandler
from models.verein import Verein


# Dummy implementations for route calculator and passenger exchange handler
# TODO: Replace with actual implementations
class DummyRouteCalculator(RouteCalculator):
    def calculate_route(self, graph, start_node, end_node):
        # Simple implementation to return a path between two nodes
        try:
            path = nx.shortest_path(graph, start_node, end_node)
            return path
        except nx.NetworkXNoPath:
            return []


class DummyPassengerExchangeHandler(PassengerExchangeHandler):
    def handle_passenger_exchange(self, remaining_stops, bus_capacity, current_passengers, people_at_station):
        # Dummy implementation
        # TODO: Implement proper passenger exchange logic
        return [], []


# TODO: Implement PersonHandler class which is required by BusAgent

def create_model(graph_params, model_params):
    # Create Streckennetz
    streckennetz = Streckennetz.create_graph(
        graph_params["num_nodes"],
        float(graph_params["edge_probability"]) / 100,
        graph_params["width"],
        graph_params["height"],
    )

    # TODO: Fix model initialization with proper route calculator and passenger exchange handler
    # For now, using dummy implementations
    route_calculator = DummyRouteCalculator()
    passenger_exchange_handler = DummyPassengerExchangeHandler()

    # Stadium node is the first node for simplicity
    stadium_node_id = "node_1"  # todo make this configurable

    # Create model
    model = IntelligentHooligentsModel(
        graph=streckennetz,
        stadium_node_id=stadium_node_id,
        route_calculator=route_calculator,
        passenger_exchange_handler=passenger_exchange_handler,
        person_handler=PersonHandler(dict[tuple[str, Verein], int]()),  # TODO: people initialization
        num_busses=model_params["num_busses"],
        num_people=model_params["num_people"]
    )

    return model, streckennetz


def visualize_model(model, streckennetz, show_agents=True, show_routes=True):
    G = model.grid.G
    pos = nx.spring_layout(G, seed=42)  # For consistent layout

    plt.figure(figsize=(10, 8))

    # Draw the network
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.5)
    nx.draw_networkx_labels(G, pos)

    # Draw edge weights
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Draw agents if enabled
    if show_agents:
        bus_positions = []
        # TODO: Update to show current position including edge progress
        for agent in model.agents:
            if hasattr(agent, 'pos'):
                bus_positions.append(agent.pos)

        if bus_positions:
            nx.draw_networkx_nodes(G, pos, nodelist=bus_positions,
                                   node_color='red', node_size=200)

    # Draw routes if enabled
    if show_routes:
        # TODO: Visualize planned routes for each bus
        pass

    plt.title("Intelligent Hooligents Model Visualization")
    plt.axis('off')
    return plt


def main():
    st.title("Intelligent Hooligents Model Simulation")

    st.sidebar.header("Streckennetz Parameters")
    graph_params = {
        "num_nodes": st.sidebar.slider("Number of Nodes", 5, 50, 10),
        "edge_probability": st.sidebar.slider("Edge probability", 0, 100, 10),
        "width": st.sidebar.slider("Graph width", 10, 1000, 100),
        "height": st.sidebar.slider("Graph height", 10, 1000, 100)
    }

    st.sidebar.header("Model Parameters")
    model_params = {
        "num_busses": st.sidebar.slider("Number of Buses", 1, 20, 3),
        "num_people": st.sidebar.slider("Number of People", 10, 500, 100),
        "bus_capacity": st.sidebar.slider("Bus Capacity", 5, 100, 10)
    }

    # Initialize or regenerate the model
    if 'model' not in st.session_state or st.sidebar.button("Regenerate Model"):
        with st.spinner("Generating model..."):
            st.session_state.model, st.session_state.streckennetz = create_model(graph_params, model_params)
            st.session_state.step_count = 0

    # Display visualization options
    st.sidebar.header("Visualization Options")
    show_agents = st.sidebar.checkbox("Show Agents", True)
    show_routes = st.sidebar.checkbox("Show Routes", True)

    # Create plot
    plot = visualize_model(st.session_state.model, st.session_state.streckennetz,
                           show_agents, show_routes)
    st.pyplot(plot)

    # Step controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Step"):
            st.session_state.model.step()
            st.session_state.step_count += 1
            st.experimental_rerun()

    with col2:
        st.write(f"Current Step: {st.session_state.step_count}")

    # Auto-play controls
    auto_play = st.checkbox("Auto-play")
    interval = st.slider("Step Interval (seconds)", 0.1, 5.0, 1.0)

    if auto_play:
        st.session_state.model.step()
        st.session_state.step_count += 1
        plot = visualize_model(st.session_state.model, st.session_state.streckennetz,
                               show_agents, show_routes)
        st.pyplot(plot)
        time.sleep(interval)
        st.experimental_rerun()


if __name__ == "__main__":
    main()
