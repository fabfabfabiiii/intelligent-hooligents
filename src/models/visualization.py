import sys
import random
import os

import matplotlib.pyplot as plt
import networkx as nx
from networkx import Graph

# Add the project root to Python's path - das muss man machen weil python eine spielzeug sprache ist
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from src/
sys.path.append(project_root)
from src import config
from src.models.streckennetz import Streckennetz

def draw_graph(graph: Streckennetz | Graph, highlight_nodes: list[str] | None = None,
               highlight_edges: list[tuple[str, str]] | None = None,
               show_distances: bool = False,
               figsize: tuple[int, int] = config.PLT_FIGSIZE) -> None:
    if isinstance(graph, Streckennetz):
        #convert into networkxgraph
        g: Graph = graph.convert_to_networkx()
    else:
        g: nx.Graph = graph

    if highlight_nodes is None:
        highlight_nodes = []
    if highlight_edges is None:
        highlight_edges = []

    positions = nx.get_node_attributes(g, 'pos')

    node_color: list[str] = [config.NODE_COLOR_HIGHLIGHTED if name in highlight_nodes else config.NODE_COLOR
                             for name, _ in positions.items()]
    edge_color: list[str] = [config.EDGE_COLOR_HIGHLIGHTED if (start, end) in highlight_edges
                             or (end, start) in highlight_edges
                             else config.EDGE_COLOR for start, end in g.edges]

    plt.figure(figsize=figsize)
    nx.draw(g, positions, with_labels=True, node_color=node_color, edge_color=edge_color,
            node_size=config.NODE_SIZE, font_size=config.FONT_SIZE, font_weight=config.FONT_WEIGHT)

    if show_distances:
        #add distance to edge
        distances = {e: g.edges[e]['weight']  for e in g.edges()}
        nx.draw_networkx_edge_labels(g, positions, edge_labels=distances, font_size=config.FONT_SIZE)

    plt.show()

def draw_graph_on_ax(graph: Streckennetz | Graph,
               ax: plt.axes,
               highlight_nodes: list[str] | None = None,
               highlight_edges: list[tuple[str, str]] | None = None,
               show_distances: bool = False) -> None:
    if isinstance(graph, Streckennetz):
        #convert into networkxgraph
        g: Graph = graph.convert_to_networkx()
    else:
        g: nx.Graph = graph

    if highlight_nodes is None:
        highlight_nodes = []
    if highlight_edges is None:
        highlight_edges = []

    positions = nx.get_node_attributes(g, 'pos')

    node_color: list[str] = [config.NODE_COLOR_HIGHLIGHTED if name in highlight_nodes else config.NODE_COLOR
                             for name, _ in positions.items()]
    edge_color: list[str] = [config.EDGE_COLOR_HIGHLIGHTED if (start, end) in highlight_edges
                             or (end, start) in highlight_edges
                             else config.EDGE_COLOR for start, end in g.edges]

    nx.draw(g, positions, with_labels=True, node_color=node_color, edge_color=edge_color,
            node_size=config.NODE_SIZE, font_size=config.FONT_SIZE, font_weight=config.FONT_WEIGHT, ax=ax)

    if show_distances:
        #add distance to edge
        distances = {e: g.edges[e]['weight']  for e in g.edges()}
        nx.draw_networkx_edge_labels(g, positions, edge_labels=distances, font_size=config.FONT_SIZE, ax=ax)