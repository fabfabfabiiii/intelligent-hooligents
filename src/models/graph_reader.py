import math
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