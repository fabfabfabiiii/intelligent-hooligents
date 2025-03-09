from mesa import Agent, Model
import networkx as nx
from typing import List, Tuple, Set
from itertools import combinations


class RoutesAgent(Agent):
    def __init__(self, unique_id: int, model, graph: nx.Graph, main_station_id: str, n_routes: int):
        super().__init__(unique_id, model)
        self.graph = graph.copy()
        self.main_station = main_station_id
        self.n_routes = n_routes
        self.routes: List[nx.Graph] = []

    def find_cycles(self, subgraph: nx.Graph, start_node: str) -> List[List[str]]:
        """Findet alle möglichen Zyklen im Subgraphen, die durch start_node gehen."""
        cycles = []
        for target in subgraph.nodes():
            if target != start_node:
                try:
                    # Finde alle einfachen Pfade zwischen start_node und target
                    paths = list(nx.all_simple_paths(subgraph, start_node, target))
                    for path in paths:
                        # Prüfe, ob der Pfad einen Zyklus bilden kann
                        if subgraph.has_edge(path[-1], start_node):
                            cycle = path + [start_node]
                            cycles.append(cycle)
                except nx.NetworkXNoPath:
                    continue
        return cycles

    def divide_graph(self) -> List[nx.Graph]:
        """Teilt den Graphen in n Teilgraphen auf."""
        all_nodes = set(self.graph.nodes())
        must_include = {self.main_station}
        remaining_nodes = all_nodes - must_include
        min_nodes_per_route = max(3, len(all_nodes) // self.n_routes)

        valid_routes = []
        for r in range(min_nodes_per_route, len(remaining_nodes) + 1):
            for nodes in combinations(remaining_nodes, r):
                route_nodes = set(nodes) | must_include
                subgraph = self.graph.subgraph(route_nodes).copy()

                # Prüfe zusätzlich den Mindestgrad aller Knoten
                min_degree = min(dict(subgraph.degree()).values()) if subgraph.nodes() else 0

                if (nx.is_connected(subgraph) and
                        min_degree >= 2 and
                        len(self.find_cycles(subgraph, self.main_station)) > 0):
                    valid_routes.append(subgraph)

        return valid_routes[:self.n_routes]

    def step(self):
        """Mesa Agent step Funktion."""
        if not self.routes:
            self.routes = self.divide_graph()


class BusNetwork(Model):
    def __init__(self, graph: nx.Graph, main_station_id: str, n_routes: int):
        super().__init__()
        self.routes_agent = RoutesAgent(1, self, graph, main_station_id, n_routes)

    def step(self):
        self.routes_agent.step()