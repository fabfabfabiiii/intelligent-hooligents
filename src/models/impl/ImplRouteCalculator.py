from typing import cast

from models.abstract.route_calculator import RouteCalculator
from models.streckennetz import Streckennetz
from models.optimization.tsp_optimization import TspOptimizer, TSPOptimizationGoal

from networkx import Graph

class ImplRouteCalculator(RouteCalculator):
    def __init__(self, graph: Streckennetz | Graph):
        if isinstance(graph, Streckennetz):
            self.graph: Streckennetz = graph
        else:
            self.graph: Streckennetz = Streckennetz.from_graph(graph, False)

    def calculate_route(self, start_node: str,
                        mandatory_nodes: list[str] | None) -> list[str]:
        optimizer: TspOptimizer = TspOptimizer(self.graph)

        if mandatory_nodes is None:
            optimizer.prepare_optimization(TSPOptimizationGoal.SHORTEST_ROUTE)
        else:
            nodes: list[str] = mandatory_nodes[:]

            if start_node not in nodes:
                nodes.append(start_node)

            optimizer.prepare_optimization(TSPOptimizationGoal.SHORTEST_SUB_ROUTE, nodes)

        optimizer.solve()

        _, nodes, _ = optimizer.get_result()
        nodes: list[str] = cast(list[str], nodes)

        return ImplRouteCalculator._reorder_list(nodes, start_node)

    @staticmethod
    def _reorder_list(nodes: list[str], start: str) -> list[str]:
        if start not in nodes:
            return nodes

        target_index = nodes.index(start)
        return nodes[target_index:] + nodes[:target_index]