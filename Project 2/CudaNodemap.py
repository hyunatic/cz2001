import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

start = 0
hospital = 6309

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

def NetworkMapFromFile(arr):
    a = nx.from_numpy_array(arr)
    return a

def getStart():
    global start
    return start
def getHospital():
    global hospital
    return hospital

def PrintGraph(networkgraph, edges):
    color_map = []
    color_edge = []
    for node in networkgraph:
        if node == getHospital():
            color_map.append('red')
        elif node == getStart():
            color_map.append('blue')
        else: 
            color_map.append('green')
    
    for path in edges:
        for edge in networkgraph.edges:
            #print(edge , path)
            if edge == path:
                #print('match')        
                color_edge.append('blue')
            else:
                color_edge.append('black')
    #print(color_edge)
    nx.draw(networkgraph, node_color=color_map, edge_color=color_edge ,with_labels=True)
 
    plt.show()

def ConvertNodeToEdge(path):
    path = SortnConvert(path)
    edges = []
    for i in range(0,len(path)-1):
        single_edge = (path[i],path[i+1])
        edges.append(single_edge)
    return edges

def SortnConvert(path):
    # selection sort 
    for i in range(len(path)-1):  
        min_id = i 
        for j in range(i+1, len(path)): 
            if path[min_id] > path[j]: 
                min_id = j         
        path[i], path[min_id] = path[min_id], path[i]
    return path
