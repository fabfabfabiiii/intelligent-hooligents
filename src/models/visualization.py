import matplotlib.pyplot as plt
import networkx as nx
from networkx import Graph

from src import config
from src.models.streckennetz import Streckennetz


def _convert_to_networkx(graph: Streckennetz) -> Graph:
    g = nx.Graph()

    for node in graph.nodes:
        x, y = graph.node_coordinates[node]
        g.add_node(node, pos=(int(x), int(y)))

    for u, v in graph.edges:
        g.add_edge(u,v, weight=graph.edge_distances[(u, v)])

    return g

def draw_graph(graph: Streckennetz | Graph, highlight_nodes: list[str] | None = None,
               highlight_edges: list[tuple[str, str]] | None = None,
               figsize: tuple[int, int] = config.PLT_FIGSIZE) -> None:
    if isinstance(graph, Streckennetz):
        #convert into networkxgraph
        g: Graph = _convert_to_networkx(graph)
    else:
        g: nx.Graph = graph

    if highlight_nodes is None:
        highlight_nodes = []
    if highlight_edges is None:
        highlight_edges = []

    positions = nx.get_node_attributes(g, 'pos')
    print(positions)
    print(highlight_edges)
    print(g.edges)

    node_color: list[str] = [config.NODE_COLOR_HIGHLIGHTED if name in highlight_nodes else config.NODE_COLOR
                             for name, _ in positions.items()]
    edge_color: list[str] = [config.EDGE_COLOR_HIGHLIGHTED if (start, end) in highlight_edges
                             or (end, start) in highlight_edges
                             else config.EDGE_COLOR for start, end in g.edges]

    plt.figure(figsize=figsize)
    nx.draw(g, positions, with_labels=True, node_color=node_color, edge_color=edge_color,
            node_size=config.NODE_SIZE, font_size=config.FONT_SIZE, font_weight=config.FONT_WEIGHT)
    plt.show()