from models.abstract.route_calculator import RouteCalculator
from models.streckennetz import Streckennetz
from networkx import Graph



class ImplRouteCalculator(RouteCalculator):
    def __init__(self, graph: Streckennetz | Graph):
        pass

    def calculate_route(self, start_node: str,
                        mandatory_nodes: list[str] | None) -> list[str]:
        pass