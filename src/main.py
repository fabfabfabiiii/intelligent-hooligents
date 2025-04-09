import random

import config
from models.graph_reader import read_graphml
from models.optimization.transport_optimization import TransportOptimization
from models.person import Person, Verein
from models.visualization import draw_graph
from models.streckennetz import Streckennetz

def load_config():
    if config.USE_SEED:
        random.seed(config.SEED)


def main():
    load_config()

    print('Intelligent Agents')

    graph: Streckennetz = Streckennetz.from_nx_graph(read_graphml(config.GRAPHML_PATH))
    #draw_graph(graph)
    
if __name__ == '__main__':
    main()
