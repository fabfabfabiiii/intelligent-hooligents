from abc import ABC, abstractmethod

class RouteCalculator(ABC):
    """
    Abstract base class for route calculators.
    """

    @abstractmethod
    def calculate_route(self, start_node: str, mandatory_nodes: list[str] | None) -> \
    list[str]:
        """
        Calculate a route through the graph.

        :param start_node: The starting node for the route.
        :param mandatory_nodes: A list of nodes that must be included in the route. None if all nodes are mandatory.
        :return: A list of nodes representing the route.
        """
        pass
