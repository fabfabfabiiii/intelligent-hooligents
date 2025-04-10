import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import time
import numpy as np
import random
from collections import defaultdict

import config
from models.agents.bus_agent import BusAgent
from models.impl.ImplRouteCalculator import ImplRouteCalculator
from models.person import Person
from models.person_handler import PersonHandler
from models.passenger_exchange_optimizer import PassengerExchangeOptimizer
from models.streckennetz import Streckennetz
from models.intelligent_hooligents_model import IntelligentHooligentsModel
from models.abstract.route_calculator import RouteCalculator
from models.abstract.passenger_exchange_handler import PassengerExchangeHandler
from models.graph_reader import read_graphml
from models.verein import Verein


# TODO: Replace with actual implementations
class DummyRouteCalculator(RouteCalculator):
    def calculate_route(self, graph, start_node, mandatory_nodes):
        try:
            path = [edge[1] for edge in nx.find_cycle(graph, start_node)]
            return path
        except nx.NetworkXNoPath:
            return []


class DummyRandomRouteCalculator(RouteCalculator):
    def calculate_route(self, graph, start_node, mandatory_nodes):
        try:
            # Find all simple cycles in the graph
            all_cycles = list(nx.simple_cycles(graph))

            # Filter cycles that contain the start_node
            valid_cycles = [cycle for cycle in all_cycles if start_node in cycle]

            if not valid_cycles:
                return []

            # Randomly select one of the valid cycles
            selected_cycle = random.choice(valid_cycles)

            # Rotate the cycle so that it starts with the node after start_node and ends with the start_node
            start_index = selected_cycle.index(start_node) + 1
            rotated_cycle = selected_cycle[start_index:] + selected_cycle[:start_index]

            return rotated_cycle
        except nx.NetworkXNoCycle:
            return []


class DummyPassengerExchangeHandler(PassengerExchangeHandler):
    def handle_passenger_exchange(self, remaining_stops, bus_capacity, current_passengers, people_at_station):
        # Dummy implementation
        # TODO: Implement proper passenger exchange logic
        return [], []


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
    route_calculator = ImplRouteCalculator()
    passenger_exchange_handler = PassengerExchangeOptimizer(streckennetz)
    person_handler: PersonHandler = PersonHandler(dict[tuple[str, Verein], int]())

    for i in range(100):
        person_handler.add_person(Person(f'{random.randint(2, streckennetz.num_nodes)}',
                                         random.choice(list(Verein)), current_position='1'))

    stadium_node_id = "1"  # todo make this configurable

    # streckennetz: Streckennetz = Streckennetz.from_nx_graph(read_graphml(config.GRAPHML_PATH))

    # Create model
    model = IntelligentHooligentsModel(
        graph=streckennetz,
        stadium_node_id=stadium_node_id,
        route_calculator=route_calculator,
        passenger_exchange_handler=passenger_exchange_handler,
        person_handler=person_handler,  # TODO: people initialization
        num_busses=model_params["num_busses"],
        num_people=model_params["num_people"],
        bus_speed=model_params["bus_speed"],
    )

    return model, streckennetz


def generate_color_map(agent_ids):
    """Generate a consistent color map for agents based on their unique IDs"""
    if 'agent_colors' not in st.session_state:
        # Define a colorful palette
        colors = [
            '#e6194B', '#3cb44b', '#4363d8', '#f58231', '#911eb4',
            '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990',
            '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3'
        ]
        # Ensure we have enough colors by cycling if necessary
        color_map = {}
        for i, agent_id in enumerate(agent_ids):
            color_map[agent_id] = colors[i % len(colors)]
        st.session_state.agent_colors = color_map
    return st.session_state.agent_colors


def visualize_model_plotly(model, streckennetz, show_agents=True, show_routes=True):
    G = model.grid.G
    pos = nx.spring_layout(G, seed=42)  # For consistent layout

    # Prepare node data
    node_x = []
    node_y = []
    node_text = []
    node_ids = []  # Store node IDs for labels

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_ids.append(str(node))  # Convert node ID to string for display

        # Create node hover text
        agents_at_node = model.grid.get_cell_list_contents([node])
        agent_info = ""
        if agents_at_node:
            agent_info = "<br>Agents at this node:<br>"
            for agent in agents_at_node:
                agent_type = type(agent).__name__
                agent_info += f"- {agent_type} (ID: {agent.unique_id})<br>"
        node_text.append(f"Node: {node}{agent_info}")

    # Create node trace
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=False,
            color='lightblue',
            size=50,
            line=dict(width=1, color='black')
        ),
        name="Nodes"
    )

    # Create node label trace
    node_label_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='text',
        text=node_ids,
        textposition="middle center",
        textfont=dict(
            size=10,
            color='black'
        ),
        hoverinfo='none',
        showlegend=False
    )

    # Prepare edge data
    edge_x = []
    edge_y = []

    # Create a separate trace for each edge with its weight
    edge_traces = []

    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        # Line for the edge
        edge_trace = go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            showlegend=False
        )
        edge_traces.append(edge_trace)

        # Weight label in the middle of the edge
        weight = edge[2].get('weight', 1)
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2

        weight_trace = go.Scatter(
            x=[mid_x],
            y=[mid_y],
            mode='text',
            text=[str(weight)],
            textposition="middle center",
            textfont=dict(
                size=9,
                color='white',
            ),
            hoverinfo='none',
            showlegend=False
        )
        edge_traces.append(weight_trace)

    # Create agent traces if enabled
    agent_traces = []
    if show_agents:
        # Group agents by node
        agents_by_node = defaultdict(list)
        for agent in model.agents:
            if hasattr(agent, 'pos'):
                agents_by_node[agent.pos].append(agent)

        # Generate color map for agents
        agent_ids = [agent.unique_id for agent in model.agents if hasattr(agent, 'pos')]
        color_map = generate_color_map(agent_ids)

        # Create agent traces
        for node, agents in agents_by_node.items():
            if node in pos:
                # Calculate positions for multiple agents at the same node
                center_x, center_y = pos[node]
                radius = 0.05

                for i, agent in enumerate(agents):
                    # Position agents in a circle around the node
                    angle = (2 * np.pi * i) / max(1, len(agents))
                    offset_x = radius * np.cos(angle)
                    offset_y = radius * np.sin(angle)

                    agent_color = color_map.get(agent.unique_id, 'red')
                    agent_type = type(agent).__name__

                    agent_trace = go.Scatter(
                        x=[center_x + offset_x],
                        y=[center_y + offset_y],
                        mode='markers',
                        marker=dict(
                            color=agent_color,
                            size=15,
                            symbol='circle',
                            line=dict(width=1, color='black')
                        ),
                        name=f"{agent_type} {agent.unique_id}",
                        text=f"{agent_type}<br>ID: {agent.unique_id}<br>Position: {agent.pos}" + (
                            f" Person count: {len(agent.passengers)}" if isinstance(
                                agent,
                                BusAgent) else "") + f"<br> Passengers:<br>{'<br>'.join([str(p.id) + f" with destination {p.zielstation} and Verein {p.verein}" for p in agent.passengers])}" if isinstance(
                            agent, BusAgent) else "",
                        hoverinfo='text'
                    )
                    agent_traces.append(agent_trace)

    # Create route traces if enabled
    route_traces = []
    if show_routes:
        # Get all bus agents from the model
        bus_agents = [agent for agent in model.agents if type(agent).__name__ == BusAgent.__name__]

        # Get the color map for agents
        agent_ids = [agent.unique_id for agent in model.agents if hasattr(agent, 'pos')]
        color_map = generate_color_map(agent_ids)

        # Create a trace for each bus's route
        for bus in bus_agents:
            if hasattr(bus, 'remaining_route') and bus.remaining_route:
                # Create a complete route that includes current position and remaining route
                complete_route = [bus.pos] + bus.remaining_route

                # Create a line for each segment of the route
                for i in range(len(complete_route) - 1):
                    start_node = complete_route[i]
                    end_node = complete_route[i + 1]

                    # Get positions of the nodes
                    if start_node in pos and end_node in pos:
                        x0, y0 = pos[start_node]
                        x1, y1 = pos[end_node]

                        # Get the bus color from the color map
                        bus_color = color_map.get(bus.unique_id, 'red')

                        # Create a trace for this route segment
                        route_segment = go.Scatter(
                            x=[x0, x1],
                            y=[y0, y1],
                            mode='lines',
                            line=dict(width=3, color=bus_color),
                            opacity=0.7,
                            hoverinfo='text',
                            text=f"Bus {bus.unique_id} route segment: {start_node} to {end_node}",
                            name=f"Bus {bus.unique_id} Route",
                            showlegend=(i == 0)  # Only show in legend once per bus
                        )
                        route_traces.append(route_segment)

    # Create figure
    fig = go.Figure(
        # data=[node_trace, node_label_trace] + edge_traces + agent_traces + route_traces,
        data=edge_traces + route_traces + [node_trace, node_label_trace] + agent_traces,
        layout=go.Layout(
            title="Intelligent Hooligents Model Visualization",
            titlefont=dict(size=16),
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            )
        )
    )

    # Apply saved camera/viewport state if available
    if 'viewport_state' in st.session_state:
        fig.update_layout(
            xaxis=dict(
                range=st.session_state.viewport_state['xaxis.range'],
                showgrid=False, zeroline=False, showticklabels=False
            ),
            yaxis=dict(
                range=st.session_state.viewport_state['yaxis.range'],
                showgrid=False, zeroline=False, showticklabels=False
            )
        )

    return fig


def _step_callback():
    # Save the current viewport from client-side
    st.session_state.viewport_state = st.session_state.get('viewport_state', {
        'xaxis.range': None,
        'yaxis.range': None
    })
    # Step the model
    st.session_state.model.step()
    st.session_state.step_count += 1
    st.rerun()


def main():
    st.set_page_config(
        page_title="Intelligent Hooligents Model Simulation",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.sidebar.header("Streckennetz Parameters")
    graph_params = {
        "num_nodes": st.sidebar.slider("Number of Nodes", 5, 50, 10),
        "edge_probability": st.sidebar.slider("Edge probability", 0, 100, 50),
        "width": st.sidebar.slider("Graph width", 10, 1000, 100),
        "height": st.sidebar.slider("Graph height", 10, 1000, 100)
    }

    st.sidebar.header("Model Parameters")
    model_params = {
        "num_busses": st.sidebar.slider("Number of Buses", 1, 20, 3),
        "num_people": st.sidebar.slider("Number of People", 10, 500, 100),
        "bus_capacity": st.sidebar.slider("Bus Capacity", 5, 100, 10),
        "bus_speed": st.sidebar.slider("Bus Speed", 1, 100, 20)
    }

    # Initialize or regenerate the model
    if 'model' not in st.session_state or st.sidebar.button("Regenerate Model"):
        with st.spinner("Generating model..."):
            st.session_state.model, st.session_state.streckennetz = create_model(graph_params, model_params)
            st.session_state.step_count = 0
            if 'agent_colors' in st.session_state:
                del st.session_state.agent_colors  # Reset colors when regenerating model

    # Display visualization options
    st.sidebar.header("Visualization Options")
    show_agents = st.sidebar.checkbox("Show Agents", True)
    show_routes = st.sidebar.checkbox("Show Routes", True)

    # Create plot with Plotly
    fig = visualize_model_plotly(st.session_state.model, st.session_state.streckennetz,
                                 show_agents, show_routes)

    st.plotly_chart(fig, use_container_width=True)

    # Step controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Step"):
            _step_callback()

    with col2:
        st.write(f"Current Step: {st.session_state.step_count}")

    # Auto-play controls
    auto_play = st.checkbox("Auto-play")
    interval = st.slider("Step Interval (seconds)", 0.01, 5.0, 1.0)

    if auto_play:
        time.sleep(interval)
        _step_callback()


if __name__ == "__main__":
    main()
