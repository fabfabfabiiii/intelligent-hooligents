import itertools
import random
import math
import networkx as nx
from networkx import Graph


class Streckennetz:
    def __init__(self):
        self.num_nodes: int = 0
        self.nodes: list[str] = []
        self.node_coordinates: dict[str, tuple[int, int]] = {}
        self.edges: list[tuple[str, str]] = []
        self.edge_distances: dict[tuple[str, str], int] = {}

    def __str__(self):
        string: str = f"Streckennetz has {self.num_nodes} nodes and {len(self.edges)} edges."
        return string

    def create_subgraph(self, nodes: list[str]) -> "Streckennetz":
        if len(nodes) == 0:
            return Streckennetz()

        subgraph: Streckennetz = Streckennetz()

        for node in self.nodes:
            if node in nodes:
                subgraph.add_node(node, self.node_coordinates[node])

        for (u, v) in self.edges:
            # filters, if edge can't exist anymore
            subgraph.add_edge(u, v, self.edge_distances[(u, v)])

        return subgraph

    # return name of node, if name is created
    # return None, if node with this name already exists
    def add_node(self, node: str, coordinate: tuple[int, int]) -> None | str:
        if node in self.nodes:
            return None

        self.nodes.append(node)
        self.num_nodes = len(self.nodes)

        self.node_coordinates[node] = coordinate

        return node

    # return None, if node can't be created (exists already or one of the nodes not exists
    def add_edge(self, start: str, end: str, distance: int) -> None | tuple[str, str]:
        if start not in self.nodes or end not in self.nodes:
            return None

        if (start, end) in self.edges or (end, start) in self.edges:
            return None

        self.edges.append((start, end))
        self.edge_distances[(start, end)] = distance

    def convert_to_networkx(self) -> Graph:
        g = nx.Graph()

        for node in self.nodes:
            x, y = self.node_coordinates[node]
            g.add_node(node, pos=(int(float(x)), int(float(y))), label=node)

        for u, v in self.edges:
            g.add_edge(u, v, weight=self.edge_distances[(u, v)])

        return g

    def is_network(self) -> bool:
        return self._is_hamiltonian_cycle()

    # danke, ChatGPT
    # eventuell nur eine Übergangslösung, aber scheint zu funktionieren
    def _is_hamiltonian_cycle(self) -> bool:
        graph: Graph = self.convert_to_networkx()

        # Finde alle möglichen Hamiltonianischen Pfade
        def backtrack(path):
            # Wenn alle Knoten im Pfad sind und wir zurück zum Startknoten können
            if len(path) == len(graph) and path[0] in graph[path[-1]]:
                return True
            # Versuche, weitere Knoten hinzuzufügen
            for neighbor in graph[path[-1]]:
                if neighbor not in path:
                    if backtrack(path + [neighbor]):
                        return True
            return False

        # Überprüfe für alle Knoten im Graphen
        for node in graph.nodes():
            if backtrack([node]):
                return True
        return False

    @staticmethod
    def from_nx_graph(graph: nx.Graph, coordinates_from_positions: bool = False) -> "Streckennetz":
        nodes: list[str] = [data["label"] for _, data in graph.nodes(data=True)]
        node_coordinates: dict[str, tuple[int, int]] = {data["label"]: data["pos"] for _, data in
                                                        graph.nodes(data=True)}
        edges: list[tuple[str, str]] = [(graph.nodes[u]["label"], graph.nodes[v]["label"]) for u, v in graph.edges]
        edge_distances: dict[tuple[str, str], int] = {
            (graph.nodes[node1]["label"], graph.nodes[node2]["label"]): int(data["weight"])
            for node1, node2, data in graph.edges(data=True)}

        if coordinates_from_positions:
            for (u, v) in edges:
                x1, y1 = node_coordinates[u]
                x2, y2 = node_coordinates[v]

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

    @staticmethod
    def create_graph(num_nodes: int, edge_probability: float = 1.0, width: int = 100,
                     height: int = 100) -> "Streckennetz":
        graph: Streckennetz = Streckennetz()
        node_names: list[str] = []

        for n in range(num_nodes):
            x = random.randint(0, width)
            y = random.randint(0, height)

            node_names.append(graph.add_node(f'node_{n + 1}', (x, y)))

        for start, end in itertools.combinations(node_names, 2):
            if random.random() >= edge_probability:
                continue

            start_x, start_y = graph.node_coordinates[start]
            end_x, end_y = graph.node_coordinates[end]

            distance: int = int(math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2))

            graph.add_edge(start, end, distance)

        return graph

    def get_distance(self, start: str, end: str) -> int | None:
        if start not in self.nodes or end not in self.nodes:
            return None

        if start == end:
            return 0

        g: Graph = self.convert_to_networkx()

        length: int = nx.shortest_path_length(g, start, end, weight='weight', method='dijkstra')

        return length
