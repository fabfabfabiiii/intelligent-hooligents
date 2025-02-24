import random

from src import config
from src.models.graph_reader import load_streckennetz
from src.models.optimization.tsp_optimization import TspOptimizer, TSPOptimizationGoal
from src.models.streckennetz import Streckennetz

def load_config():
    if config.USE_SEED:
        random.seed(config.SEED)

def main():
    load_config()

    print('Intelligent Agents')

    netz: Streckennetz = load_streckennetz("../resources/Verkehrsnetz.graphml")

    tsp_optimizer: TspOptimizer = TspOptimizer(netz)
    tsp_optimizer.prepare_optimization(TSPOptimizationGoal.SHORTEST_ROUTE)
    tsp_optimizer.solve()

    length, ordered, graph = tsp_optimizer.get_result()
    print(f'Length: {length}')
    print(f'{graph}')
    print(f'{ordered}')

    tsp_optimizer.print_logging()

if __name__ == '__main__':
    main()