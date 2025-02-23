class Streckennetz:
    def __init__(self):
        self.num_nodes: int = 0
        self.nodes: list[str] = []
        self.node_coordinates: dict[str, tuple[int, int]] = {}
        self.edges: list[tuple[str, str]] = []
        self.edge_distances: dict[tuple[str, str], int] = {}

    def __str__(self):
        string: str = f"Streckennetz has {self.num_nodes} nodes and {len[self.edges]} edges."
        return string

    #this methods removes nodes from the STRECKENNETZ
    #bitte nur auf deep copy anwenden
    def keep_nodes(self, nodes: list[str]) -> None:
        if len(nodes) == 0:
            return

        nodes_to_keep: list[str] = []
        for node in self.nodes:
            if node in  nodes:
                nodes_to_keep.append(node)

        self.nodes = nodes_to_keep
        self.num_nodes = len(self.nodes)

        self.node_coordinates = {k: v for k, v in self.node_coordinates.items() if k in nodes_to_keep}

        self.edges = [(u, v) for u, v in self.edges if u in nodes_to_keep and v in nodes_to_keep]
        self.edge_distances = {k: v for k, v in self.edge_distances.items() if k in self.edges}

    #return name of node, if name is created
    #return None, if node with this name already exists
    def add_node(self, node: str, coordinate: tuple[int, int]) -> None | str:
        if node not in self.nodes:
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