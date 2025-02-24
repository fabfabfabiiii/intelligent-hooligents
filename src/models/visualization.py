import matplotlib.pyplot as plt
import networkx as nx
from networkx import Graph

from src.models.streckennetz import Streckennetz


def _convert_to_networkx(graph: Streckennetz) -> Graph:
    g = nx.Graph()

    for node in graph.nodes:
        g.add_node(node, pos=graph.node_coordinates[node])

    for u, v in graph.edges:
        g.add_edge(u,v, weight=graph.edge_distances[(u, v)])

    return g

def draw_graph(graph: Streckennetz | Graph):

    if isinstance(graph, Streckennetz):
        #convert into networkxgraph
        G: Graph = _convert_to_networkx(graph)
    else:
        G: nx.Graph = graph

