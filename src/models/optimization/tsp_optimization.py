from enum import Enum

from src.models.streckennetz import Streckennetz


class TspOptimizer:
    def __init__(self, graph: Streckennetz):
        self.graph: Streckennetz = graph
        self.log: list[str] = []
        self.is_optimized: bool = False

    def solve(self, problem) -> None:
        print("not yet implemented")
        #TODO implement

    def get_Result(self) -> None:
        if not self.is_optimized:
            return None

        print("not yet implemented")
        #TODO implement

    def print_logging(self) -> None:
        for line in self.log:
            print(line)

class TSPOptimizationGoal(Enum):
    SHORTEST_ROUTE = 0
    EXIST_ROUTE = 1

    def __str__(self):
        if self.value == 0:
            return "Optimization: Shortest Route"
        if self.value == 1:
            return "Optimization: Exist Route"

        return "not implemented"