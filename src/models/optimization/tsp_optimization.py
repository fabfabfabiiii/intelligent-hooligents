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

    def prepare_optimization_shortest_route(self) -> None:
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
            self.prepare_optimization_shortest_route()

        if goal == TSPOptimizationGoal.EXIST_ROUTE:
            print("not yet implemented")
            #TODO implement

        self.goal = goal
        return True

    def compute_cycles(self) -> list[list]:
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
        cycles = self.compute_cycles()
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
            cycles = self.compute_cycles()

        self.is_optimized = True
        return True

    def get_result(self) -> None | tuple[int, list[str], Streckennetz] | bool:
        if not self.is_optimized or self.goal is None:
            self.log.append("No result available. Please solve the optimization first")
            return None

        print("not yet implemented")
        #TODO implement

    def print_logging(self) -> None:
        for line in self.log:
            print(line)