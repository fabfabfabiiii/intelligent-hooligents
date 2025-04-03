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

    optimization: TransportOptimization = TransportOptimization(graph)

    stations: list[str] = ['1','2','3']
    persons: list[Person] = [Person('3', Verein.Club_A),
                             Person('1', Verein.Club_B),]

    optimization.prepare_optimization(2, stations, persons)



if __name__ == '__main__':
    main()
