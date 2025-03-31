import sys
import random
import os

from mesa import Model

import config
from models.graph_reader import read_graphml
from models.optimization.tsp_optimization import TspOptimizer, TSPOptimizationGoal
from models.streckennetz import Streckennetz
from models.visualization import draw_graph

# only for testing purposes
import streamlit as st
import matplotlib.pyplot as plt


def load_config():
    if config.USE_SEED:
        random.seed(config.SEED)


def main():
    load_config()

    print('Intelligent Agents')

    graph = read_graphml(config.GRAPHML_PATH)

    # tsp_optimizer: TspOptimizer = TspOptimizer(Streckennetz.from_nx_graph(graph))
    # tsp_optimizer.prepare_optimization(TSPOptimizationGoal.SHORTEST_ROUTE)
    # tsp_optimizer.solve()
    #
    # length, names, new_graph = tsp_optimizer.get_result()

    # draw_graph(graph, show_distances=True)


if __name__ == '__main__':
    main()
