import math
import random
import xml.etree.ElementTree as ElementTree
from networkx.classes import Graph

from src.models.streckennetz import Streckennetz
from typing import Tuple

def read_graphml(path: str) -> Graph | None:
    try:
        root = ElementTree.parse(path).getroot()
    except Exception as e:
        print(e)
        return None

    nodes = root.findall('.//node')
    edges = root.findall('.//edge')

    graph: Graph = Graph()

    for node in nodes:
        attr = node.attrib
        graph.add_node(attr["id"], label=attr["mainText"], size=attr["size"],
                       pos=(attr["positionX"], attr["positionY"]))

    for edge in edges:
        attr = edge.attrib
        graph.add_edge(attr["source"], attr["target"], weight=attr["weight"])

    return graph

def get_graph_values_for_tsp_solver(graph: Graph) -> Tuple[list[str], dict[str, tuple[int, int]], list[tuple[str, str]], dict[tuple[str, str], int]]:
    node_names: list[str] = [data["label"] for _, data in graph.nodes(data=True)]
    coordinates: dict[str, tuple[int, int]] = {data["label"]: data["pos"] for _, data in graph.nodes(data=True)}
    edges: list[tuple[str, str]] = [(graph.nodes[u]["label"], graph.nodes[v]["label"]) for u, v in graph.edges]
    distances: dict[tuple[str, str], int] = {(graph.nodes[node1]["label"], graph.nodes[node2]["label"]): int(data["weight"])
                 for node1, node2, data in graph.edges(data=True)}

    #print(node_names)
    #print(coordinates)
    #print(edges)
    #print(distances)

    return node_names, coordinates, edges, distances

def load_streckennetz(path: str, coordinates_from_positions: bool = False) -> None | Streckennetz:
    graph: Graph = read_graphml(path)

    if graph is None:
        return None

    nodes, node_coordinates, edges, edge_distances = get_graph_values_for_tsp_solver(graph)

    if coordinates_from_positions:
        for (u, v) in edges:
            x1, y1 = node_coordinates[u]
            x2, y2 = node_coordinates[v]

            print(x1, y1, x2, y2)

            distance: int = int(math.sqrt((int(x2) - int(x1)) ** 2 + (int(y2) - int(y1)) ** 2))
            edge_distances[(u, v)] = distance

    netz: Streckennetz = Streckennetz()

    for node in nodes:
        coordinate = node_coordinates[node]
        netz.add_node(node, coordinate)

    for edge in edges:
        distance = edge_distances[edge]
        start, end = edge
        netz.add_edge(start, end, distance)

    return netz