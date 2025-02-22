#%%
import networkx as nx
import matplotlib.pyplot as plt
from Read_Graph import readGraphFromXml
#%%

def drawGraph(graph, highlight_nodes=[], highlight_edges=[], node_identifier="label"):
    if highlight_nodes is None:
        highlight_nodes = []
    if highlight_edges is None:
        highlight_edges = []
    pos = {node_id: data["pos"] for node_id, data in graph.nodes(data=True)}
    labels = {node_id: data["label"] for node_id, data in graph.nodes(data=True)}
    node_colors = ['red' if data[node_identifier] in highlight_nodes else 'blue' for _, data in graph.nodes(data=True)]
    edge_colors = ['red' if edge_id in highlight_edges else 'blue' for edge_id in graph.edges()]

    nx.draw(graph, pos=pos, with_labels=True, labels=labels, node_color=node_colors, edge_color=edge_colors, font_size=10, font_weight='bold')

graph = readGraphFromXml('../resources/Verkehrsnetz.graphml')

drawGraph(graph, highlight_nodes=["0"], highlight_edges=[], node_identifier="id")
plt.pause(1)
drawGraph(graph, highlight_nodes=["0", "1"], highlight_edges=[("0", "1")], node_identifier="id")
plt.pause(1)
drawGraph(graph, highlight_nodes=["0", "1", "7"], highlight_edges=[("0", "1"), ("1", "7")], node_identifier="id")
plt.pause(1)
drawGraph(graph, highlight_nodes=["0", "1", "7", "6"], highlight_edges=[("0", "1"), ("1", "7"), ("6", "7")], node_identifier="id")
plt.pause(1)
drawGraph(graph, highlight_nodes=["0", "1", "7", "6", "4"], highlight_edges=[("0", "1"), ("1", "7"), ("6", "7"), ("4", "6")], node_identifier="id")
plt.show()