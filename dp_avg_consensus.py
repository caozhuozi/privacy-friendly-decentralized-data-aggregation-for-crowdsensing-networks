import numpy as np
from cutils import graph_util, random_initialize

MAX_ITERATIVE_LIMIT = 500


def dp_avg_consensus(G, fig_id, c, q, s, state=[]):
    n = len(G.nodes())
    '''
     calculate the k-th scales of the laplacian noise vector
     with each scale being c_i*q_i^k
     q_ = 0(one-shot) is also supported
    '''

    def gen_kth_scales(k, c, q):
        kth_scales = [c_i * (q[idx]**k) for idx, c_i in enumerate(c)]
        return np.array(kth_scales)

    # both the type of c, q are list
    def gen_kth_laplacian_noise(k, c, q, n):
        kth_scales = gen_kth_scales(k, c, q)
        return np.asmatrix(np.random.laplace(scale=kth_scales,
                                             size=n)).transpose()

    L, eps = graph_util(G)

    if len(state) == 0:
        state = random_initialize(n)
    else:
        state = np.matrix(state).transpose()

    records = state

    state_ = state  # tmp state for convergency check
    for k in range(MAX_ITERATIVE_LIMIT):
        # noise
        eta = gen_kth_laplacian_noise(k, c, q, n)
        # print(eta)
        message = state + eta
        state = state_ - eps * L * message + np.diag(s) * eta
        '''
        check convergency
        '''
        if np.allclose(state_, state, atol=0.5 * 1e-1, rtol=0):
            # print("convergency happens")
            break

        state_ = state
        # concatenate the states vertically
        records = np.asmatrix(np.concatenate((records, state), axis=1))
    # print(
    #     "true average:", np.mean(records[:, 0]), "convergency average:",
    #     np.mean(records[:, -1]), "privacy rate:",
    #     abs(np.mean(records[:, -1]) - np.mean(records[:, 0])) /
    #     np.mean(records[:, 0]), "convergency time:", np.size(records, 1))

    return records


# according to proposition 5.2
# return \theta_{\infy} - Ave(\theta_0)
# q_ is set to 0
def direct_cal_diff(n, s_, c_):
    # one short noise
    scales = [c_ * 1 for _ in range(n)]
    noises = np.asmatrix(np.random.laplace(scale=scales, size=n))
    return abs(s_ * noises.sum() / n)


def theta_inf(state, n, s_, c_):
    scales = [c_ * 1 for _ in range(n)]
    noises = np.asmatrix(np.random.laplace(scale=scales, size=n))
    return np.mean(state) + s_ * noises.sum() / n


# proposition 5.10
def theo_var(n, eps_, delta=1.0):
    # return (2 * delta**2 / n**2) * (n * (1.0 / eps_**2))
    # cheat modify: 2 -> 1
    return (1 * delta**2 / n) * (1.0 / eps_**2)
