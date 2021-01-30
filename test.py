from dp_average_consensus import differentially_private_average_consensus, direct_cal_diff, theo_var
from cdraw import draw_consensus
from cutils import random_initialize, set_c
from gen_geograph import gen_geometric_graph
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

G, fig_id = gen_geometric_graph(100, 0.125)

n = len(G.nodes())

delta = 1.0

# in all the experiments,  q_i(for all i), and s_i(for all i) are equal respectively
q_ = 0  # one-shot adding
s_ = 1.0
dp_eps_ = 10.0

q = [q_ for _ in range(n)]
s = [s_ for _ in range(n)]
c = [set_c(dp_eps_, q_, s_) for _ in range(n)]
state = random_initialize(n, 50, 100)
# records = differentially_private_average_consensus(G, state, fig_id, c, q, s)
fig = plt.figure()
ax = fig.add_subplot(111)
epss = [10**step for step in np.arange(-2, 2.1, 0.2)]
varc = []
for eps in epss:
    xc = []
    yc = []
    c_ = set_c(eps, q_, s_)
    for _ in range(20):
        xc.append(eps)
        yc.append(direct_cal_diff(n, s_, c_))
    # varc.append(np.var(yc))
    # ax.scatter(xc, yc, facecolors='none', edgecolors='b')
    varc.append(np.var(yc, ddof=1))
    ax.plot(eps, np.var(yc), 'ro')
ax.plot(epss, [theo_var(n, eps) for eps in epss])
# linear_regressor = LinearRegression()  # create object for the class
# linear_regressor.fit(
#     np.array(epss).reshape(-1, 1),
#     np.array(varc).reshape(-1, 1))  # perform linear regression
# Y_pred = linear_regressor.predict(np.array(epss).reshape(-1, 1))
# print(Y_pred)
# ax.plot(np.array(epss).reshape(-1, 1), Y_pred, color='r')

# m, b = np.polyfit(epss, varc, deg=1)

# ax.plot(epss, [m * eps + b for eps in epss], color='blue')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim([10**-2 - 10**-3, 10**2 + 10])
# ax.set_ylim([10**-4, 10**2])
# plt.show()
