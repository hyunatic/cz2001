from heapq import heappush, heappop
from itertools import count
import networkx as nx
from Networkx import *


#Programmed by Yong Qiang, Wayne, Iskandar
def AStarSearch(graph, source, target, heuristic=None):
    t=100
    for x in target:
        dis = resistance_distance(graph,source,x)
        #print("get")
        #print(x)
        #print(dis)
        
        if(t > dis):
            t = dis
            tar = x
    if source not in graph or tar not in graph:
        msg = f"Either source {source} or target {target} is not in graph"
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
    explorednodes = {}
    
    while queue:
    # Pop the smallest item from queue
        _, __, current, dist, parent = pop(queue)
        
        if current == tar:
            path = [current]
            node = parent
            while node is not None:
                path.append(node)
                node = explorednodes[node]
            path.reverse()
            return path

        if current in explorednodes:
            # Do not override the parent of starting node
            if explorednodes[current] is None:
                continue

            # Skip bad paths that were enqueued before finding a better one
            qcost, h = enqueued[current]
            if qcost < dist:
                continue

        explorednodes[current] = parent

        for neighbor, w in graph[current].items():
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
                h = heuristic(neighbor, tar)
                
            enqueued[neighbor] = ncost, h
            push(queue, (ncost + h, next(c), neighbor, ncost, current))

    raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")
