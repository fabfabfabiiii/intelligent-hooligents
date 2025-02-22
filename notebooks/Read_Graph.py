#!/usr/bin/env python
# coding: utf-8
import networkx as nx
import xml.etree.ElementTree as ElementTree

def readGraphML(path):
    root = ElementTree.parse(path).getroot()
    nodes = root.findall('.//node')
    edges = root.findall('.//edge')
    print(nodes[0].attrib)
    graph = nx.Graph()

    for node in nodes:
        attr = node.attrib
        graph.add_node(attr["id"], label=attr["mainText"], size=attr["size"],
                       pos=(attr["positionX"], attr["positionY"]))

    for edge in edges:
        attr = edge.attrib
        graph.add_edge(attr["source"], attr["target"], weight=attr["weight"])
    #
    # labelDict = {}
    # for key in graph.nodes.keys():
    #     labelDict[key] = graph.nodes[key]["label"]

    return graph