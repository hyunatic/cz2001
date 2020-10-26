import networkx as nx
import matplotlib.pyplot as plt
import random
from CudaProcessing import ReadFile, TransferToGpu, ConvertToAdjList

start = 0
hospital = []

def GenerateNetworkMap():
    #Don't try to run this 
    #Real Graph Data
    # nparray = ReadFile()
    # cparray = TransferToGpu(nparray)
    # nodes = cp.unique(cparray)
    # a = nx.Graph()
    # a.add_nodes_from(nodes)
    # cpSortedArr = cparray[cparray[:,0].argsort()]
    # a.read_edgelist(cpSortedArr)

    ##Comment till here if you don't want to test the real graph

    #Random Graph
    #Note: If program fails, keep retrying the graph
    nodes = random.randrange(10,20)
    edges = random.randrange(9,60)
    a = nx.gnm_random_graph(nodes, edges,random.randrange(5))

    ##Comment till here if you don't want to test the random graph

    #Randomly pick hospital
    global hospital
    randlist = random.sample(range(len(list(a))), 3)

    for x in randlist:
        hospital.append(x)
        #hospital.append(random.randrange(len(list(a))))

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
    color_edge = []
    for node in networkgraph:
       
       
        if (node in hospital):
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
    #print("edges")
    #for x in edges:
        #print(edges)
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