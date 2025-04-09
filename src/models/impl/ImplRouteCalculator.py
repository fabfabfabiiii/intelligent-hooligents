from typing import cast

from models.abstract.route_calculator import RouteCalculator
from models.optimization.tsp_optimization import TspOptimizer, TSPOptimizationGoal
from models.streckennetz import Streckennetz
from networkx import Graph


class ImplRouteCalculator(RouteCalculator):

    def calculate_route(self, graph: Streckennetz | Graph,start_node: str,
                        mandatory_nodes: list[str] | None) -> list[str]:

        if isinstance(graph, Streckennetz):
            g: Streckennetz = graph
        else:
            g: Streckennetz = Streckennetz.from_nx_graph(graph, False)

        optimizer: TspOptimizer = TspOptimizer(g)

        if mandatory_nodes is None:
            optimizer.prepare_optimization(TSPOptimizationGoal.SHORTEST_ROUTE)
        else:
            #copy
            nodes: list[str] = mandatory_nodes[:]

            if start_node not in nodes:
                nodes.append(start_node)

            optimizer.prepare_optimization(TSPOptimizationGoal.SHORTEST_SUB_ROUTE, nodes)

        optimizer.solve()

        _, nodes, _ = optimizer.get_result()
        nodes: list[str] = cast(list[str], nodes)

        return ImplRouteCalculator._reorder_list(nodes, start_node)[::-1]

    @staticmethod
    def _reorder_list(nodes: list[str], start: str) -> list[str]:
        if start not in nodes:
            return nodes

        target_index = nodes.index(start)
        return nodes[target_index:] + nodes[:target_index]