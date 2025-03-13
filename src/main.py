import sys
import random
import os

from mesa import Model

from src.models.visualization import draw_graph_on_ax

# Add the project root to Python's path - das muss man machen weil python eine spielzeug sprache ist
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from src/
sys.path.append(project_root)

from src import config
# from src.models.graph_reader import load_streckennetz
from src.models.optimization.tsp_optimization import TspOptimizer, TSPOptimizationGoal
from src.models.streckennetz import Streckennetz
from src.models.routes_agent import RoutesAgent

# Add notebooks directory to path - relative pfade angeben können wär auch wirklich zu viel verlangt
notebooks_dir = os.path.join(project_root, 'notebooks')
sys.path.append(notebooks_dir)
from notebooks.Read_Graph import readGraphFromXml
from notebooks.Visualize_Graph import draw_graph

from notebooks.Read_Graph import readGraphFromXml
from notebooks.Visualize_Graph import draw_graph

# only for testing purposes
import streamlit as st
import matplotlib.pyplot as plt


def load_config():
    if config.USE_SEED:
        random.seed(config.SEED)

# def main():
#     load_config()
#
#     print('Intelligent Agents')
#
#     graph: Streckennetz = load_streckennetz(config.GRAPHML_PATH)
#
#     tsp_optimizer: TspOptimizer = TspOptimizer(graph)
#     tsp_optimizer.prepare_optimization(TSPOptimizationGoal.SHORTEST_ROUTE)
#     tsp_optimizer.solve()
#
#     length, names, new_graph = tsp_optimizer.get_result()
#
#     draw_graph(new_graph, show_distances=True)

# for testing route divisions
def main():
    # Load the graph
    graphFromFile = readGraphFromXml('./resources/20250309_Verkehrsnetz.graphml')
    streckennetz = Streckennetz.from_nx_graph(graphFromFile)

    # Streamlit UI
    st.title("Graph Visualization")

    # Create a Streamlit placeholder to update the figure dynamically
    plot_area = st.empty()

    # Create the Matplotlib figure
    plotFig, plotAx = plt.subplots()

    draw_graph(graphFromFile, plotAx)
    plot_area.pyplot(plotFig)  # Update the Streamlit plot

    routesAgent = RoutesAgent(Model(), "10", "Stadion")

    # Get lists of subgraphs from division methods
    randomSubGraphList = routesAgent._divide_by_random_partitioning(streckennetz, 2)
    spanningTreeSubGraphList = routesAgent._divide_by_spanning_tree(streckennetz, 2)
    geometricSubGraphList = routesAgent._divide_by_geometry(streckennetz, 2)

    # Plot each subgraph in the random partition list
    for i, subgraph in enumerate(randomSubGraphList):
        fig, ax = plt.subplots()
        draw_graph_on_ax(subgraph.convert_to_networkx(), ax)
        ax.set_title(f"Random Partition Subgraph {i + 1}")
        plot_area.pyplot(fig)

    # Plot each subgraph in the spanning tree partition list
    for i, subgraph in enumerate(spanningTreeSubGraphList):
        fig, ax = plt.subplots()
        draw_graph_on_ax(subgraph.convert_to_networkx(), ax)
        ax.set_title(f"Spanning Tree Partition Subgraph {i + 1}")
        plot_area.pyplot(fig)

    # Plot each subgraph in the geometric partition list
    for i, subgraph in enumerate(geometricSubGraphList):
        fig, ax = plt.subplots()
        draw_graph_on_ax(subgraph.convert_to_networkx(), ax)
        ax.set_title(f"Geometric Partition Subgraph {i + 1}")
        plot_area.pyplot(fig)

if __name__ == '__main__':
    main()