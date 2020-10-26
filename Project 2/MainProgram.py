from __future__ import print_function
from Nodemap import *
from heapq import heappush, heappop
from itertools import count
import networkx as nx
from Networkx import *
from AStar import AStarSearch
## This is for reference
from BFS import *
from DFS import *
from timeit import default_timer as timer    


#Programmed by Wayne and Yong Qiang

if __name__=="__main__":
    #A Star Search
    nwmap = GenerateNetworkMap()
    path = AStarSearch(nwmap, getStart(), getHospital())

    #BFS
    #nwmap = GenerateNetworkMap()
    #bfsgenedges = generic_bfs_edges(nwmap, getStart())
    #bfsedges = bfs_edges(nwmap, getStart())
    #bfstree = bfs_tree(nwmap, getStart())
    #bfssuccessors = bfs_successor(nwmap, getStart())

    #DFS
    #nwmap = GenerateNetworkMap()
    #dfsedges = dfs_edges(nwmap)
    #dfstree = dfs_tree(nwmap)
    #dfssuccessors = dfs_successors(nwmap)
    #dfslabeledge = dfs_labeled_edges(nwmap)

    #Write path taken into a file
    #Task A and B
    with open("RandomGraphPath.txt", 'w') as f:
        f.write(str(path) + "\n")
        ##Print total Distance
        ##Since the graph is unweighted, default edge value is 1
        #So we just take the length of the array
        f.write(str(len(path)) + "\n")
    f.close() 

    #Get Edge List
    edges = ConvertNodeToEdge(path)
    #Use Python library to display the GUI graph
    PrintGraph(nwmap, edges)
