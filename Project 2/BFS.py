import networkx as nx
from collections import deque

__all__ = [
    "bfs_edges",
    "bfs_tree",
    "bfs_successors",
    "descendants_at_distance",
]


def generic_bfs_edges(G, source, neighbors=None, depth_limit=None, sort_neighbors=None):
    if callable(sort_neighbors):
        _neighbors = neighbors
        neighbors = lambda node: iter(sort_neighbors(_neighbors(node)))

    visited = {source}
    if depth_limit is None:
        depth_limit = len(G)
    queue = deque([(source, depth_limit, neighbors(source))])
    while queue:
        parent, depth_now, children = queue[0]
        try:
            child = next(children)
            if child not in visited:
                yield parent, child
                visited.add(child)
                if depth_now > 1:
                    queue.append((child, depth_now - 1, neighbors(child)))
        except StopIteration:
            queue.popleft()


def bfs_edges(G, source, reverse=False, depth_limit=None, sort_neighbors=None):
    if reverse and G.is_directed():
        successors = G.predecessors
    else:
        successors = G.neighbors
    yield from generic_bfs_edges(G, source, successors, depth_limit, sort_neighbors)



def bfs_tree(G, source, reverse=False, depth_limit=None, sort_neighbors=None):
    for s, t in bfs_edges(
        G, source, depth_limit=depth_limit, sort_neighbors=sort_neighbors
    ):
        yield (t, s)



def bfs_successors(G, source, depth_limit=None, sort_neighbors=None):
    parent = source
    children = []
    for p, c in bfs_edges(
        G, source, depth_limit=depth_limit, sort_neighbors=sort_neighbors
    ):
        if p == parent:
            children.append(c)
            continue
        yield (parent, children)
        children = [c]
        parent = p
    yield (parent, children)



def descendants_at_distance(G, source, distance):
    if not G.has_node(source):
        raise nx.NetworkXError(f"The node {source} is not in the graph.")
    current_distance = 0
    queue = {source}
    visited = {source}

    # this is basically BFS, except that the queue only stores the nodes at
    # current_distance from source at each iteration
    while queue:
        if current_distance == distance:
            return queue

        current_distance += 1

        next_vertices = set()
        for vertex in queue:
            for child in G[vertex]:
                if child not in visited:
                    visited.add(child)
                    next_vertices.add(child)

        queue = next_vertices

    return set()