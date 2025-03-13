import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
from Read_Graph import readGraphFromXml

def draw_graph(graph, ax, highlight_nodes=None, highlight_edges=None, node_identifier="label"):
    if highlight_nodes is None:
        highlight_nodes = []
    if highlight_edges is None:
        highlight_edges = []
    pos = {node_id: data["pos"] for node_id, data in graph.nodes(data=True)}
    labels = {node_id: data["label"] for node_id, data in graph.nodes(data=True)}
    node_colors = ['red' if data[node_identifier] in highlight_nodes else 'blue' for _, data in graph.nodes(data=True)]
    edge_colors = ['red' if edge_id in highlight_edges else 'blue' for edge_id in graph.edges()]

    ax.clear()  # Clear the previous plot
    nx.draw(graph, ax=ax, pos=pos, with_labels=True, labels=labels, node_color=node_colors, edge_color=edge_colors, font_size=10, font_weight='bold')

if __name__ == "__main__":
    # Load the graph
    graphFromFile = readGraphFromXml('../resources/Verkehrsnetz.graphml')

    # Streamlit UI
    st.title("Graph Visualization")

    # Create a Streamlit placeholder to update the figure dynamically
    plot_area = st.empty()

    # Create the Matplotlib figure
    plotFig, plotAx = plt.subplots()

    # Define the steps for node and edge highlights
    steps = [
        (["0"], []),
        (["0", "1"], [("0", "1")]),
        (["0", "1", "7"], [("0", "1"), ("1", "7")]),
        (["0", "1", "7", "6"], [("0", "1"), ("1", "7"), ("6", "7")]),
        (["0", "1", "7", "6", "4"], [("0", "1"), ("1", "7"), ("6", "7"), ("4", "6")]),
    ]

    # Iterate through each step and update the figure dynamically
    for highlightedNodes, highlightedEdges in steps:
        draw_graph(graphFromFile, plotAx, highlightedNodes, highlightedEdges, node_identifier="id")
        plot_area.pyplot(plotFig)  # Update the Streamlit plot
        plt.pause(0.5)

    st.write("Graph updates completed.")

# use "streamlit run <path.to.file>" run this file