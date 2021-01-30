import networkx as nx

import datetime
from cdraw import draw_geograph

# import sys


# n: the number of nodes
# dis: distance threshold for linking edge between two nodes
def gen_draw_geograph(n, dis, unique_id):
    while True:
        G = nx.random_geometric_graph(n, dis)
        # position is stored as node attribute data for random_geometric_graph
        # find node near center (0.5,0.5)
        # pos records the node locations in a canvas
        # center node, originally with the purpose for drawing the colors gradiently, here degenerates to only testing whether the graph is fully connected; for this purpose, the center node here can be replaced by any node
        # dmin = 1
        # ncenter = 0
        # for n in pos:
        #     x, y = pos[n]
        #     d = (x - 0.5)**2 + (y - 0.5)**2
        #     if d < dmin:
        #         ncenter = n
        #         dmin = d
        ncenter = 0
        # color by path length from node near center
        # nx.single_source_shortest_path_length():
        #     compute the shortest path lengths from source to all reachable nodes.
        # Thus, it returns the set of nodes that are reachable from the center node
        p = dict(nx.single_source_shortest_path_length(G, ncenter))
        # it is expected that all points are connected by at least one path
        if len(G.nodes()) != n:
            continue
        if n == 6 and len(G.edges()) not in [9, 10]:
            continue
        if len(p.keys()) != len(G.nodes()):
            # isolated points are generated undesirably
            # print("undesired generation")
            continue
        else:
            break
    fig_id = unique_id + "_" + str(n) + "_topo"
    # save the graph figure once it is generated for the purpose of retrieval
    draw_geograph(G, fig_id)
    return G, unique_id
