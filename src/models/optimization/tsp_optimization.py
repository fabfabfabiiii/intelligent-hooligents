from enum import Enum
from itertools import combinations

import networkx as nx
from networkx import Graph
from pyoptinterface import highs
import pyoptinterface as poi

from src.models.streckennetz import Streckennetz

class TSPOptimizationGoal(Enum):
    SHORTEST_ROUTE = 0
    EXIST_ROUTE = 1

    def __str__(self):
        if self.value == 0:
            return "Shortest Route"
        if self.value == 1:
            return "Exists Route"

        return "not implemented"

class TspOptimizer:
    def __init__(self, graph: Streckennetz):
        self.graph: Streckennetz = graph
        self.log: list[str] = []

        self.is_optimized: bool = False
        self.goal: TSPOptimizationGoal | None = None
        self.model = highs.Model()
        self.decision_variable = None

        self.log.append("Initialize Streckennetz")
        self.log.append(str(self.graph))

    def _prepare_optimization_shortest_route(self) -> None:
        # Decision variable
        self.decision_variable = self.model.add_variables(self.graph.edges, domain=poi.VariableDomain.Binary)
        self.log.append("Add Decision Variables")

        # constraint : leave and enter each node only once
        num_nodes: int = len(self.graph.nodes)
        for n in self.graph.nodes:
            self.model.add_linear_constraint(
                poi.quicksum(self.decision_variable[n, v] for v in self.graph.nodes if (n, v) in self.graph.edges) +
                poi.quicksum(self.decision_variable[v, n] for v in self.graph.nodes if (v, n) in self.graph.edges) , poi.Eq, 2)

            self.log.append('Add Linear Constraint')

        obj = poi.quicksum(self.graph.edge_distances[e] * self.decision_variable[e] for e in self.graph.edges)
        self.model.set_objective(obj, poi.ObjectiveSense.Minimize)
        self.log.append("Minimize Route length")

    def prepare_optimization(self, goal: TSPOptimizationGoal) -> bool:
        if self.is_optimized:
            self.log.append('Already optimized. Can\'t prepare optimization again')
            return False

        if self.goal is not None:
            self.log.append('Goal is already optimized. Can\'t prepare optimization again')
            return False

        self.log.append(f'Optimize for {goal}')

        if goal == TSPOptimizationGoal.SHORTEST_ROUTE:
            self._prepare_optimization_shortest_route()

        if goal == TSPOptimizationGoal.EXIST_ROUTE:
            print("not yet implemented")
            #TODO implement

        self.goal = goal
        return True

    def _compute_cycles(self) -> list[list]:
        graph: Graph = Graph()
        graph.add_nodes_from(self.graph.nodes)

        edges_used = [e for e in self.decision_variable if self.model.get_variable_attribute(
            self.decision_variable[e], poi.VariableAttribute.Value) > 0.99]

        graph.add_edges_from(edges_used)
        cycles = nx.minimum_cycle_basis(graph)
        return cycles

    def solve(self) ->  bool:
        if self.goal is None:
            self.log.append("No goal is set yed. Prepare optimization first")
            return False

        if self.is_optimized:
            self.log.append("Can't optimize again")
            return False

        self.log.append(f'Start optimization for {self.goal}')
        self.model.optimize()

        #check for subtour
        cycles = self._compute_cycles()
        n_se_constraints: int = 0

        while len(cycles[0]) < self.graph.num_nodes:
            for cycle in cycles:
                cycle = sorted(cycle)
                self.model.add_linear_constraint(
                    poi.quicksum(self.decision_variable[u, v] for (u, v) in combinations(cycle, 2)) , poi.Leq, len(cycle) - 1)

                self.log.append('Add subtour constraint')

            self.log.append(f'Start optimization after adding subtour constraint')
            self.model.optimize()
            n_se_constraints += 1
            cycles = self._compute_cycles()

        self.log.append(f'Finish optimization for {self.goal}')
        self.is_optimized = True
        return True

    def _get_result_shortest_route(self) -> tuple[int, list[str], Streckennetz]:
        length: int = 0
        graph: Streckennetz = Streckennetz()

        for node in self.graph.nodes:
            graph.add_node(node, self.graph.node_coordinates[node])

        edges_used = [e for e in self.decision_variable if self.model.get_variable_attribute(
            self.decision_variable[e], poi.VariableAttribute.Value) > 0.99]

        for e in edges_used:
            length += self.graph.edge_distances[e]
            start, end = e
            graph.add_edge(start, end, self.graph.edge_distances[e])

        #Line from here until end of the function is AI GENERATED
        # Einen Startknoten finden
        # 1. Adjazenzliste erstellen
        adjacency = {}
        for start, end in edges_used:
            adjacency.setdefault(start, []).append(end)
            adjacency.setdefault(end, []).append(start)

        # 2. Einen Startpunkt finden (z. B. einen Knoten mit nur einer Verbindung)
        start_node = next((node for node in adjacency if len(adjacency[node]) == 1), None)
        if start_node is None:
            # Falls kein Startknoten gefunden wird, handelt es sich um einen Zyklus, dann nehmen wir einen beliebigen Knoten
            start_node = next(iter(adjacency))

        # 3. Pfad rekonstruierten
        ordered_nodes = [start_node]
        visited_edges = set()

        while len(ordered_nodes) < len(adjacency):
            current = ordered_nodes[-1]
            for neighbor in adjacency[current]:
                edge = tuple(sorted((current, neighbor)))  # Sorgt dafür, dass (a, b) und (b, a) gleich behandelt werden
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    ordered_nodes.append(neighbor)
                    break

        return length, ordered_nodes, graph

    def get_result(self) -> None | tuple[int, list[str], Streckennetz] | bool:
        if not self.is_optimized or self.goal is None:
            self.log.append("No result available. Please solve the optimization first")
            return None

        if self.goal == TSPOptimizationGoal.SHORTEST_ROUTE:
            return self._get_result_shortest_route()

        print("not yet implemented")
        #TODO implement
        return None

    def print_logging(self) -> None:
        for line in self.log:
            print(line)