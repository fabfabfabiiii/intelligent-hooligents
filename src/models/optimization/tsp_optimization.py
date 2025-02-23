from enum import Enum

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
        for n in range(num_nodes):
            self.model.add_linear_constraint(
                poi.quicksum(self.decision_variable[n, v] for v in range(num_nodes) if (n, v) in self.graph.edges) +
                poi.quicksum(self.decision_variable[v, n] for v in range(num_nodes) if (v, n) in self.graph.edges) , poi.Eq, 2)

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

    def solve(self) ->  bool:
        if self.goal is None:
            self.log.append("No goal is set yed. Prepare optimization first")
            return False

        if self.is_optimized:
            self.log.append("Can't optimize again")
            return False

        self.model.optimize()

    def get_result(self) -> None | tuple[int, list[str], Streckennetz] | bool:
        if not self.is_optimized:
            return None

        print("not yet implemented")
        #TODO implement

    def print_logging(self) -> None:
        for line in self.log:
            print(line)