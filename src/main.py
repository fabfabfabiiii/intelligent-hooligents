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

    # Show original graph
    st.subheader("Original Network")
    orig_fig, orig_ax = plt.subplots()
    draw_graph(graphFromFile, orig_ax)
    st.pyplot(orig_fig)

    # Initialize the routes agent
    routesAgent = RoutesAgent(Model(), "10", "Stadion")

    # Get lists of subgraphs from division methods
    randomSubGraphList = routesAgent._divide_by_random_partitioning(streckennetz, 2)
    spanningTreeSubGraphList = routesAgent._divide_by_spanning_tree(streckennetz, 2)
    geometricSubGraphList = routesAgent._divide_by_geometry(streckennetz, 2)

    # Create separate sections for each partition type
    st.subheader("Random Partitioning")
    if randomSubGraphList:
        random_cols = st.columns(len(randomSubGraphList))
        for i, subgraph in enumerate(randomSubGraphList):
            with random_cols[i]:
                fig, ax = plt.subplots()
                draw_graph_on_ax(subgraph.convert_to_networkx(), ax)
                ax.set_title(f"Random Partition {i + 1}")
                st.pyplot(fig)
    else:
        st.write("No random partitions generated")

    st.subheader("Spanning Tree Partitioning")
    if spanningTreeSubGraphList:
        spanning_cols = st.columns(len(spanningTreeSubGraphList))
        for i, subgraph in enumerate(spanningTreeSubGraphList):
            with spanning_cols[i]:
                fig, ax = plt.subplots()
                draw_graph_on_ax(subgraph.convert_to_networkx(), ax)
                ax.set_title(f"Spanning Tree Partition {i + 1}")
                st.pyplot(fig)
    else:
        st.write("No spanning tree partitions generated")

    st.subheader("Geometric Partitioning")
    if geometricSubGraphList:
        geo_cols = st.columns(len(geometricSubGraphList))
        for i, subgraph in enumerate(geometricSubGraphList):
            with geo_cols[i]:
                fig, ax = plt.subplots()
                draw_graph_on_ax(subgraph.convert_to_networkx(), ax)
                ax.set_title(f"Geometric Partition {i + 1}")
                st.pyplot(fig)
    else:
        st.write("No geometric partitions generated")

if __name__ == '__main__':
    main()