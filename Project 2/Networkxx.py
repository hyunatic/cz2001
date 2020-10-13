import networkx as nx
import matplotlib.pyplot as plt
import random

nodes = random.randrange(2,10)
edges = random.randrange(1,10)

a = nx.gnm_random_graph(nodes, edges,random.randrange(5))
hospital = random.randrange(len(list(a)))
while True:
    start = random.randrange(len(list(a)))
    if hospital != start:
        break

color_map = []
for node in a:
    if node == hospital:
        color_map.append('red')
    elif node == start:
        color_map.append('blue')
    else: 
        color_map.append('green')      
nx.draw(a, node_color=color_map, with_labels=True)
plt.show()
