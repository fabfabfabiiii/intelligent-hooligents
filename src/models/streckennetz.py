class Streckennetz:
    def __init__(self):
        self.num_nodes: int = 0
        self.node_names: dict[int, str] = {}
        self.node_coordinates: dict[int, tuple[int, int]] = {}
        self.edges: list[tuple[int, int]] = []
        self.edge_distances: dict[tuple[int, int], int] = {}

    def __str__(self):
        string: str = "Streckennetz"
        return string

    #this methods removes nodes from the STRECKENNETZ
    #bitte nur auf deep copy anwenden
    def keep_nodes(self, nodes: list[str] | list[int]) -> None:
        if len(nodes) == 0:
            return

        list_ids: list[int] = []
        if isinstance(nodes[0], int):
            list_ids = list[int](nodes.copy())
        else:
            for key, value in self.node_names.items():
                if value in nodes:
                    list_ids.append(key)

        #diese Schleife kann vermutlich verschoben werden in if block, wenn liste int enthält
        for i in range(len(list_ids) - 1, -1, -1):
            if list_ids[i] not in self.node_names:
                list_ids.remove(list_ids[i])

        #list_ids hat nun die id aller nodes, die es wirklich gibt und die behalten werden sollen
        self.num_nodes = len(list_ids)

        #entferne Werte aus Liste, die nicht enthalten werden sollen
        self.node_names = {key: self.node_names[key] for key in self.node_names if key in list_ids}
        self.node_coordinates = {key: self.node_coordinates[key] for key in self.node_coordinates if key in list_ids}

        #entferne alle edges, die nodes enthalten, welche es nicht mehr gibt
        self.edges = [edge for edge in self.edges if edge[0] in list_ids and edge[1] in list_ids]

        #entferne alle disctances, die es nicht mehr geben kann
        self.edge_distances = {key: value for key, value in self.edge_distances.items() if key in self.edges}

    def get_node_names(self) -> list[str]:
        names: list[str] = []

        for _, value in self.node_names.items():
            names.append(value)

        return names