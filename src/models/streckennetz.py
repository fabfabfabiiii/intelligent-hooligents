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
            #filters, if edge can't exist anymore
            subgraph.add_edge(u, v, self.edge_distances[(u, v)])

        return subgraph

    #return name of node, if name is created
    #return None, if node with this name already exists
    def add_node(self, node: str, coordinate: tuple[int, int]) -> None | str:
        if node in self.nodes:
            return None

        self.nodes.append(node)
        self.num_nodes = len(self.nodes)

        self.node_coordinates[node] = coordinate

        return node

    #return None, if node can't be created (exists already or one of the nodes not exists
    def add_edge(self, start: str, end:str, distance: int) -> None | tuple[str, str]:
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
            g.add_node(node, pos=(int(x), int(y)))

        for u, v in self.edges:
            g.add_edge(u,v, weight=self.edge_distances[(u, v)])

        return g

    def is_network(self) -> bool:
        #TODO implement
        print(f'not implemented')

        return False