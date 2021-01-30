import numpy as np
import networkx as nx
from cutils import random_initialize, graph_util
# from matplotlib.ticker import MaxNLocator
# from draw_geo_graph import draw_geometric_graph

MAX_ITERATIVE_LIMIT = 500


def average_consensus(G, fig_id, loc=100, scale=50, state=[]):
    n = len(G.nodes())

    # laplacian matrix
    L, eps = graph_util(G)
    # initial state
    if len(state) == 0:
        state = random_initialize(n, loc, scale)
    else:
        state = np.matrix(state).transpose()
    """
    generating a n*1 matrix with all elements being the average point
    for the later convergency check
    """
    avg = np.asmatrix(state.mean() * np.ones((n, 1)))
    """
    records: record all the state during the
    iterative process until convergency
    """
    records = state

    # update the state iteratively
    for k in range(MAX_ITERATIVE_LIMIT):
        state = (np.identity(n) - eps * L) * state
        # check convergency
        # if np.array_equal(state, state_tmp):
        if np.allclose(state, avg, rtol=0, atol=1e-2):
            break
        # concatenate the states vertically
        records = np.asmatrix(np.concatenate((records, state), axis=1))

    np.savetxt("../records/" + fig_id + ".csv", records, delimiter=",")
    return records
