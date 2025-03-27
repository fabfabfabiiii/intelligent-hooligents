import sys
import random
import os

from mesa import Model

# Add the project root to Python's path - das muss man machen weil python eine spielzeug sprache ist
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from src/
sys.path.append(project_root)

from src import config
# from src.models.graph_reader import load_streckennetz
from src.models.optimization.tsp_optimization import TspOptimizer, TSPOptimizationGoal
from src.models.streckennetz import Streckennetz
from src.models.visualization import draw_graph_on_ax

# Add notebooks directory to path - relative pfade angeben können wär auch wirklich zu viel verlangt
notebooks_dir = os.path.join(project_root, 'notebooks')
sys.path.append(notebooks_dir)
from notebooks.Read_Graph import readGraphFromXml

# only for testing purposes
import streamlit as st
import matplotlib.pyplot as plt


def load_config():
    if config.USE_SEED:
        random.seed(config.SEED)

def main():
    load_config()

    print('Intelligent Agents')

    # graph: Streckennetz = load_streckennetz(config.GRAPHML_PATH)
    #
    # tsp_optimizer: TspOptimizer = TspOptimizer(graph)
    # tsp_optimizer.prepare_optimization(TSPOptimizationGoal.SHORTEST_ROUTE)
    # tsp_optimizer.solve()
    #
    # length, names, new_graph = tsp_optimizer.get_result()
    #
    # draw_graph(new_graph, show_distances=True)

if __name__ == '__main__':
    main()