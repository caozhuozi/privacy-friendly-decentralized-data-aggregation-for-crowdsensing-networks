import networkx as nx
import numpy as np
import datetime


def graph_util(G):
    A = nx.to_numpy_matrix(G)
    # laplacian matrix
    L = nx.laplacian_matrix(G).todense()
    # degree matrix
    D = L + A
    d_max = D.max()
    # eps rule
    eps = 1.0 / (d_max + 1)
    return L, eps


def random_initialize(n, loc=100, scale=50):
    norm_d = np.asmatrix(np.random.normal(loc, scale, n)).transpose()
    # rounding each element may facilitate accelerating convergency
    for e in np.nditer(norm_d, op_flags=['readwrite']):
        e[...] = int(e)
    return norm_d


# according to equation 32
# all the parameters are scalar
def set_c(dp_eps_i, q_i, s_i, delta=1.0):
    if q_i == 0:
        c = delta / dp_eps_i
    else:
        c = delta * (q_i / dp_eps_i * (q_i - abs(s_i - 1)))
    return c


def set_dis(n):
    if n <= 10:
        return 0.7
    elif n <= 50:
        return 0.3
    else:
        return 0.125


def time_stamp():
    return str(datetime.datetime.now().strftime('%m%d-%H%M%S'))
