from __future__ import print_function
from Nodemap import *
from heapq import heappush, heappop
from itertools import count
import numpy as np
import cupy as cp
import networkx as nx
from timeit import default_timer as timer    
 
def AStarSearch(G, source, target, heuristic=None):
    if source not in G or target not in G:
        msg = f"Either source {source} or target {target} is not in G"
        raise nx.NodeNotFound(msg)

    if heuristic is None:
        # The default heuristic is h=0 - same as Dijkstra's algorithm
        def heuristic(u, v):
            return 0

    push = heappush
    pop = heappop

    # The queue stores priority, node, cost to reach, and parent.
    # Uses Python heapq to keep in priority order.
    # Add a counter to the queue to prevent the underlying heap from
    # attempting to compare the nodes themselves. The hash breaks ties in the
    # priority and is guaranteed unique for all nodes in the graph.
    c = count()
    queue = [(0, next(c), source, 0, None)]

    # Maps enqueued nodes to distance of discovered paths and the
    # computed heuristics to target. We avoid computing the heuristics
    # more than once and inserting the node into the queue too many times.
    enqueued = {}
    # Maps explored nodes to parent closest to the source.
    explored = {}

    while queue:
        # Pop the smallest item from queue.
        _, __, curnode, dist, parent = pop(queue)

        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if curnode in explored:
            # Do not override the parent of starting node
            if explored[curnode] is None:
                continue

            # Skip bad paths that were enqueued before finding a better one
            qcost, h = enqueued[curnode]
            if qcost < dist:
                continue

        explored[curnode] = parent

        for neighbor, w in G[curnode].items():
            ncost = dist
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                # if qcost <= ncost, a less costly path from the
                # neighbor to the source was already determined.
                # Therefore, we won't attempt to push this neighbor
                # to the queue
                if qcost <= ncost:
                    continue
            else:
                h = heuristic(neighbor, target)
            enqueued[neighbor] = ncost, h
            push(queue, (ncost + h, next(c), neighbor, ncost, curnode))

    raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")

def ReadFile():
    edge = np.loadtxt("roadNet-PA.txt", dtype="int32", skiprows=4)
    array = np.array(edge)
    return array

def Convert(arr1):
    size = cp.unique(arr1).size
    
    arr = cp.zeros(size, dtype="int32")

    #Create [[0,0,0,0,0], [0,0,0,0,0]]
    #size = total Unique elements
    print(size // 20)
    #arr1 = cp.tile(arr, (size,1))

    # for row,col in arr1:
    #     arr[row][col] = 1
    # return arr

if __name__=="__main__":
    start = timer() 
    nparray = ReadFile()
    print("Read File Done", timer()-start) 

    start = timer() 
    cparray = cp.array(nparray)
    print("Cuda Array Done", timer()-start)

    size = cp.unique(cparray).size

    # start = timer() 
    matrix = Convert(cparray)
    # print("Process Done", timer()-start)


    # networkmap = NetworkMapFromFile(matrix)
    # path = AStarSearch(networkmap, getStart(), getHospital())
    # edges = ConvertNodeToEdge(path)
    # PrintGraph(networkmap, edges)