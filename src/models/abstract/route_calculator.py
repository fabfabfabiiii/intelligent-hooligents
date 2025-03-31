from abc import ABC, abstractmethod

import networkx as nx

from models.streckennetz import Streckennetz


class RouteCalculator(ABC):
    """
    Abstract base class for route calculators.
    """

    @abstractmethod
    def calculate_route(self, graph: Streckennetz | nx.Graph, start_node: str, mandatory_nodes: list[str] | None) -> \
    list[str]:
        """
        Calculate a route through the graph.

        :param graph: The graph to calculate the route on.
        :param start_node: The starting node for the route.
        :param mandatory_nodes: A list of nodes that must be included in the route. None if all nodes are mandatory.
        :return: A list of nodes representing the route.
        """
        pass
