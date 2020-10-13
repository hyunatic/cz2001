import networkx as nx
import matplotlib.pyplot as plt
import random

start = 0
hospital = 0

def GenerateNetworkMap():
    nodes = random.randrange(10,20)
    edges = random.randrange(9,60)

    a = nx.gnm_random_graph(nodes, edges,random.randrange(5))
    global hospital
    hospital = random.randrange(len(list(a)))
    while True:
        global start
        start = random.randrange(len(list(a)))
        if hospital != start:
            break
    return a

def getStart():
    return start
def getHospital():
    return hospital

def PrintGraph(networkgraph, edges):
    color_map = []
    for node in networkgraph:
        if node == getHospital():
            color_map.append('red')
        elif node == getStart():
            color_map.append('blue')
        else: 
            color_map.append('green')
            
    nx.draw(networkgraph, node_color=color_map, with_labels=True)
 
    plt.show()

def ConvertNodeToEdge(path):
    edges = []
    for i in range(0,len(path)-1):
        single_edge = (path[i],path[i+1])
        edges.append(single_edge)
    return edges
