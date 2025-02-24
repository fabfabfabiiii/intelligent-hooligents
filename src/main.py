import random

from src import config
from src.models.graph_reader import load_streckennetz
from src.models.optimization.tsp_optimization import TspOptimizer, TSPOptimizationGoal
from src.models.streckennetz import Streckennetz
from src.models.visualization import draw_graph

def load_config():
    if config.USE_SEED:
        random.seed(config.SEED)

def main():
    load_config()

    print('Intelligent Agents')

    graph: Streckennetz = load_streckennetz(config.GRAPHML_PATH)

    tsp_optimizer: TspOptimizer = TspOptimizer(graph)
    tsp_optimizer.prepare_optimization(TSPOptimizationGoal.SHORTEST_ROUTE)
    tsp_optimizer.solve()

    length, names, new_graph = tsp_optimizer.get_result()

    draw_graph(new_graph, show_distances=True)

if __name__ == '__main__':
    main()