"""Graph diameter, radius, eccentricity and other properties."""

import networkx as nx
from networkx.utils import not_implemented_for

__all__ = [
    "extrema_bounding",
    "eccentricity",
    "diameter",
    "radius",
    "periphery",
    "center",
    "barycenter",
    "resistance_distance",
]


def extrema_bounding(G, compute="diameter"):

    # init variables
    degrees = dict(G.degree())  # start with the highest degree node
    minlowernode = max(degrees, key=degrees.get)
    N = len(degrees)  # number of nodes
    # alternate between smallest lower and largest upper bound
    high = False
    # status variables
    ecc_lower = dict.fromkeys(G, 0)
    ecc_upper = dict.fromkeys(G, N)
    candidates = set(G)

    # (re)set bound extremes
    minlower = N
    maxlower = 0
    minupper = N
    maxupper = 0

    # repeat the following until there are no more candidates
    while candidates:
        if high:
            current = maxupper  # select node with largest upper bound
        else:
            current = minlower  # select node with smallest lower bound
        high = not high

        # get distances from/to current node and derive eccentricity
        dist = dict(nx.single_source_shortest_path_length(G, current))
        if len(dist) != N:
            msg = "Cannot compute metric because graph is not connected."
            raise nx.NetworkXError(msg)
        current_ecc = max(dist.values())

        # print status update
        #        print ("ecc of " + str(current) + " (" + str(ecc_lower[current]) + "/"
        #        + str(ecc_upper[current]) + ", deg: " + str(dist[current]) + ") is "
        #        + str(current_ecc))
        #        print(ecc_upper)

        # (re)set bound extremes
        maxuppernode = None
        minlowernode = None

        # update node bounds
        for i in candidates:
            # update eccentricity bounds
            d = dist[i]
            ecc_lower[i] = low = max(ecc_lower[i], max(d, (current_ecc - d)))
            ecc_upper[i] = upp = min(ecc_upper[i], current_ecc + d)

            # update min/max values of lower and upper bounds
            minlower = min(ecc_lower[i], minlower)
            maxlower = max(ecc_lower[i], maxlower)
            minupper = min(ecc_upper[i], minupper)
            maxupper = max(ecc_upper[i], maxupper)

        # update candidate set
        if compute == "diameter":
            ruled_out = {
                i
                for i in candidates
                if ecc_upper[i] <= maxlower and 2 * ecc_lower[i] >= maxupper
            }

        elif compute == "radius":
            ruled_out = {
                i
                for i in candidates
                if ecc_lower[i] >= minupper and ecc_upper[i] + 1 <= 2 * minlower
            }

        elif compute == "periphery":
            ruled_out = {
                i
                for i in candidates
                if ecc_upper[i] < maxlower
                and (maxlower == maxupper or ecc_lower[i] > maxupper)
            }

        elif compute == "center":
            ruled_out = {
                i
                for i in candidates
                if ecc_lower[i] > minupper
                and (minlower == minupper or ecc_upper[i] + 1 < 2 * minlower)
            }

        elif compute == "eccentricities":
            ruled_out = {}

        ruled_out.update(i for i in candidates if ecc_lower[i] == ecc_upper[i])
        candidates -= ruled_out

        #        for i in ruled_out:
        #            print("removing %g: ecc_u: %g maxl: %g ecc_l: %g maxu: %g"%
        #                    (i,ecc_upper[i],maxlower,ecc_lower[i],maxupper))
        #        print("node %g: ecc_u: %g maxl: %g ecc_l: %g maxu: %g"%
        #                    (4,ecc_upper[4],maxlower,ecc_lower[4],maxupper))
        #        print("NODE 4: %g"%(ecc_upper[4] <= maxlower))
        #        print("NODE 4: %g"%(2 * ecc_lower[4] >= maxupper))
        #        print("NODE 4: %g"%(ecc_upper[4] <= maxlower
        #                            and 2 * ecc_lower[4] >= maxupper))

        # updating maxuppernode and minlowernode for selection in next round
        for i in candidates:
            if (
                minlowernode is None
                or (
                    ecc_lower[i] == ecc_lower[minlowernode]
                    and degrees[i] > degrees[minlowernode]
                )
                or (ecc_lower[i] < ecc_lower[minlowernode])
            ):
                minlowernode = i

            if (
                maxuppernode is None
                or (
                    ecc_upper[i] == ecc_upper[maxuppernode]
                    and degrees[i] > degrees[maxuppernode]
                )
                or (ecc_upper[i] > ecc_upper[maxuppernode])
            ):
                maxuppernode = i

        # print status update
    #        print (" min=" + str(minlower) + "/" + str(minupper) +
    #        " max=" + str(maxlower) + "/" + str(maxupper) +
    #        " candidates: " + str(len(candidates)))
    #        print("cand:",candidates)
    #        print("ecc_l",ecc_lower)
    #        print("ecc_u",ecc_upper)
    #        wait = input("press Enter to continue")

    # return the correct value of the requested metric
    if compute == "diameter":
        return maxlower
    elif compute == "radius":
        return minupper
    elif compute == "periphery":
        p = [v for v in G if ecc_lower[v] == maxlower]
        return p
    elif compute == "center":
        c = [v for v in G if ecc_upper[v] == minupper]
        return c
    elif compute == "eccentricities":
        return ecc_lower
    return None



def eccentricity(G, v=None, sp=None):
    #    if v is None:                # none, use entire graph
    #        nodes=G.nodes()
    #    elif v in G:               # is v a single node
    #        nodes=[v]
    #    else:                      # assume v is a container of nodes
    #        nodes=v
    order = G.order()

    e = {}
    for n in G.nbunch_iter(v):
        if sp is None:
            length = nx.single_source_shortest_path_length(G, n)
            L = len(length)
        else:
            try:
                length = sp[n]
                L = len(length)
            except TypeError as e:
                raise nx.NetworkXError('Format of "sp" is invalid.') from e
        if L != order:
            if G.is_directed():
                msg = (
                    "Found infinite path length because the digraph is not"
                    " strongly connected"
                )
            else:
                msg = "Found infinite path length because the graph is not" " connected"
            raise nx.NetworkXError(msg)

        e[n] = max(length.values())

    if v in G:
        return e[v]  # return single value
    else:
        return e


def diameter(G, e=None, usebounds=False):
    if usebounds is True and e is None and not G.is_directed():
        return extrema_bounding(G, compute="diameter")
    if e is None:
        e = eccentricity(G)
    return max(e.values())



def periphery(G, e=None, usebounds=False):
    if usebounds is True and e is None and not G.is_directed():
        return extrema_bounding(G, compute="periphery")
    if e is None:
        e = eccentricity(G)
    diameter = max(e.values())
    p = [v for v in e if e[v] == diameter]
    return p



def radius(G, e=None, usebounds=False):
    if usebounds is True and e is None and not G.is_directed():
        return extrema_bounding(G, compute="radius")
    if e is None:
        e = eccentricity(G)
    return min(e.values())



def center(G, e=None, usebounds=False):
    if usebounds is True and e is None and not G.is_directed():
        return extrema_bounding(G, compute="center")
    if e is None:
        e = eccentricity(G)
    radius = min(e.values())
    p = [v for v in e if e[v] == radius]
    return p



def barycenter(G, weight=None, attr=None, sp=None):
    if sp is None:
        sp = nx.shortest_path_length(G, weight=weight)
    else:
        sp = sp.items()
        if weight is not None:
            raise ValueError("Cannot use both sp, weight arguments together")
    smallest, barycenter_vertices, n = float("inf"), [], len(G)
    for v, dists in sp:
        if len(dists) < n:
            raise nx.NetworkXNoPath(
                f"Input graph {G} is disconnected, so every induced subgraph "
                "has infinite barycentricity."
            )
        barycentricity = sum(dists.values())
        if attr is not None:
            G.nodes[v][attr] = barycentricity
        if barycentricity < smallest:
            smallest = barycentricity
            barycenter_vertices = [v]
        elif barycentricity == smallest:
            barycenter_vertices.append(v)
    return barycenter_vertices



def _laplacian_submatrix(node, mat, node_list):
    j = node_list.index(node)
    n = list(range(len(node_list)))
    n.pop(j)

    if mat.shape[0] != mat.shape[1]:
        raise nx.NetworkXError("Matrix must be square")
    elif len(node_list) != mat.shape[0]:
        msg = "Node list length does not match matrix dimentions"
        raise nx.NetworkXError(msg)

    mat = mat.tocsr()
    mat = mat[n, :]

    mat = mat.tocsc()
    mat = mat[:, n]

    node_list.pop(j)

    return mat, node_list


def _count_lu_permutations(perm_array):
    """Counts the number of permutations in SuperLU perm_c or perm_r
    """
    perm_cnt = 0
    arr = perm_array.tolist()
    for i in range(len(arr)):
        if i != arr[i]:
            perm_cnt += 1
            n = arr.index(i)
            arr[n] = arr[i]
            arr[i] = i

    return perm_cnt



def resistance_distance(G, nodeA, nodeB, weight=None, invert_weight=True):
    import numpy as np
    import scipy.sparse

    if not nx.is_connected(G):
        msg = "Graph G must be strongly connected."
        raise nx.NetworkXError(msg)
    elif nodeA not in G:
        msg = "Node A is not in graph G."
        raise nx.NetworkXError(msg)
    elif nodeB not in G:
        msg = "Node B is not in graph G."
        raise nx.NetworkXError(msg)
    elif nodeA == nodeB:
        msg = "Node A and Node B cannot be the same."
        raise nx.NetworkXError(msg)

    G = G.copy()
    node_list = list(G)

    if invert_weight and weight is not None:
        if G.is_multigraph():
            for (u, v, k, d) in G.edges(keys=True, data=True):
                d[weight] = 1 / d[weight]
        else:
            for (u, v, d) in G.edges(data=True):
                d[weight] = 1 / d[weight]
    # Replace with collapsing topology or approximated zero?

    # Using determinants to compute the effective resistance is more memory
    # efficent than directly calculating the psuedo-inverse
    L = nx.laplacian_matrix(G, node_list, weight=weight)

    Lsub_a, node_list_a = _laplacian_submatrix(nodeA, L.copy(), node_list[:])
    Lsub_ab, node_list_ab = _laplacian_submatrix(nodeB, Lsub_a.copy(), node_list_a[:])

    # Factorize Laplacian submatrixes and extract diagonals
    # Order the diagonals to minimize the likelihood over overflows
    # during computing the determinant
    lu_a = scipy.sparse.linalg.splu(Lsub_a, options=dict(SymmetricMode=True))
    LdiagA = lu_a.U.diagonal()
    LdiagA_s = np.product(np.sign(LdiagA)) * np.product(lu_a.L.diagonal())
    LdiagA_s *= (-1) ** _count_lu_permutations(lu_a.perm_r)
    LdiagA_s *= (-1) ** _count_lu_permutations(lu_a.perm_c)
    LdiagA = np.absolute(LdiagA)
    LdiagA = np.sort(LdiagA)

    lu_ab = scipy.sparse.linalg.splu(Lsub_ab, options=dict(SymmetricMode=True))
    LdiagAB = lu_ab.U.diagonal()
    LdiagAB_s = np.product(np.sign(LdiagAB)) * np.product(lu_ab.L.diagonal())
    LdiagAB_s *= (-1) ** _count_lu_permutations(lu_ab.perm_r)
    LdiagAB_s *= (-1) ** _count_lu_permutations(lu_ab.perm_c)
    LdiagAB = np.absolute(LdiagAB)
    LdiagAB = np.sort(LdiagAB)

    # Calculate the ratio of determinant, rd = det(Lsub_ab)/det(Lsub_a)
    Ldet = np.product(np.divide(np.append(LdiagAB, [1]), LdiagA))
    rd = Ldet * LdiagAB_s / LdiagA_s

    return rd