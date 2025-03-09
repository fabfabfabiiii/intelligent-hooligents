#%%
import networkx as nx
import xml.etree.ElementTree as ElementTree
#%%
def readGraphFromXml(xmlPath): #type: (str) -> nx.Graph
    root = ElementTree.parse(xmlPath).getroot()
    nodes = root.findall('.//node')
    edges = root.findall('.//edge')
    graph = nx.Graph()

    for node in nodes:
        attr = node.attrib
        graph.add_node(attr["id"], id=attr["id"], label=attr["mainText"], size=attr["size"], pos=[int(attr["positionX"]),int(attr["positionY"])])

    for edge in edges:
        attr = edge.attrib
        graph.add_edge(attr["source"], attr["target"], weight=attr["weight"])

    return graph