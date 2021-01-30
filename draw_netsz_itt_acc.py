'''
  the results of this script is determined as an experiment part for the publication
  this script aims at figuring out the relationship between iterative times and network size
'''
import numpy as np
from cutils import random_initialize, set_c, set_dis
from dp_avg_consensus import dp_avg_consensus, direct_cal_diff
from cgeograph import gen_draw_geograph
import matplotlib.pyplot as plt
import datetime
from matplotlib.lines import Line2D

q_ = 0  # one-shot adding
s_ = 1.0
dp_eps_ = 0.3
c_ = set_c(dp_eps_, q_, s_)

size_list = [50, 100, 150, 200, 225, 250, 275, 300]


def cmp_netsz_iternumbers(unique_id, dp_eps_):
    fig = plt.figure()

    plt.rc('text', usetex=True)
    plt.rc('font', family='Times New Roman', weight='normal', size=14)
    plt.rcParams['mathtext.fontset'] = 'stix'

    # set_xscale only supported in add_subplot
    ax = fig.add_subplot(111)
    mean_cord = []
    for n in size_list:
        # for n in [5]:
        q = [q_ for _ in range(n)]
        s = [s_ for _ in range(n)]
        c = [c_ for _ in range(n)]
        state = random_initialize(n, 50, 100)
        G, fig_id = gen_draw_geograph(n, set_dis(n), unique_id)
        y_cord = []
        for _ in range(20):
            records = dp_avg_consensus(G,
                                       fig_id,
                                       c,
                                       q,
                                       s,
                                       state=np.matrix(state).transpose())
            y_cord.append(records.shape[1])
        ax.scatter([n for _ in range(20)],
                   y_cord,
                   marker='D',
                   s=160,
                   facecolors='none',
                   edgecolors='black')
        mean_cord.append(np.mean(y_cord))
    ax.scatter(size_list,
               mean_cord,
               marker='o',
               s=80,
               color='none',
               edgecolors='g',
               linewidth=3)

    ax.plot(size_list, mean_cord, c='b', lw=1)

    # custom legend
    legend_elements = [
        Line2D([0], [0],
               c='none',
               marker='D',
               markerfacecolor='none',
               markeredgecolor='black',
               label='Iterative Times of Each Run (PE-IDA)',
               markersize=9),
        Line2D([0], [0],
               c='none',
               marker='o',
               markerfacecolor='none',
               markeredgewidth=3,
               markeredgecolor='g',
               label='Iterative Times of IDA algorithm',
               markersize=9)
    ]
    ax.legend(handles=legend_elements, prop={'size': 15})

    plt.xticks([50, 100, 150, 200, 225, 250, 275, 300],
               fontsize=20,
               weight='bold')
    plt.yticks(fontsize=20, weight='bold')
    plt.xlabel(r"$|\mathcal{V}|$", fontsize=20)
    plt.ylabel(r"Iterative Times", fontsize=25, weight='bold')
    ax.grid(ls=':')

    ax.set_aspect(1.0 / ax.get_data_ratio() * 0.6)

    # plt.show()

    # plt.show()
    fig_id = unique_id + "_eps_" + str(dp_eps_).replace('.', '') + "_szitt"
    plt.savefig("../final_exp_publication/netsz_acc_itertnum/" + fig_id +
                '.pdf',
                bbox_inches="tight",
                pad_inches=0.01)


def cmp_netsz_accuracy(unique_id, dp_eps_):
    fig = plt.figure()
    plt.rc('text', usetex=True)
    plt.rc('font', family='Times New Roman', weight='normal', size=14)
    plt.rcParams['mathtext.fontset'] = 'stix'
    # set_xscale only supported in add_subplot
    ax = fig.add_subplot(111)
    mean_cord = []
    for n in size_list:
        # for n in [5]:

        state = random_initialize(n, 50, 100)
        G, _ = gen_draw_geograph(n, set_dis(n), unique_id)
        y_cord = []
        for _ in range(20):
            y_cord.append(direct_cal_diff(n, s_, c_))
        ax.scatter(
            [n for _ in range(20)],
            y_cord,
            marker='P',
            s=160,
            # color="#007dff",
            # linewidth=2,
            color='none',
            edgecolors='black')
        mean_cord.append(np.mean(y_cord))
    ax.scatter(size_list,
               mean_cord,
               marker='o',
               s=80,
               color='none',
               edgecolors='b',
               linewidth=3)
    ax.plot(size_list, mean_cord, c='b', lw=1)

    # custom legend
    legend_elements = [
        Line2D([0], [0],
               c='none',
               marker='P',
               markerfacecolor='none',
               markeredgecolor='black',
               label='Error of Each Run',
               markersize=9),
        Line2D([0], [0],
               c='none',
               marker='o',
               markerfacecolor='none',
               markeredgewidth=3,
               markeredgecolor='b',
               label='Empirical Mean',
               markersize=9)
    ]
    ax.legend(handles=legend_elements, prop={'size': 15})
    ax.grid(ls=':')

    plt.xticks([50, 100, 150, 200, 225, 250, 275, 300],
               fontsize=20,
               weight='bold')
    plt.yticks(fontsize=20, weight='bold')
    # plt.yticks([1, 2])
    plt.xlabel(r"$|\mathcal{V}|$", fontsize=20)
    plt.ylabel(r"$|x^{*} - \bar{\mathbf{x}}|$", fontsize=25)

    ax.set_aspect(1.0 / ax.get_data_ratio() * 0.6)

    # plt.show()
    fig_id = unique_id + "_eps_" + str(dp_eps_).replace('.', '') + "_szacc"
    plt.savefig("../final_exp_publication/netsz_acc_itertnum/" + fig_id +
                '.pdf',
                bbox_inches="tight",
                pad_inches=0.01)


for e in [0.01, 0.1, 1, 10]:
    unique_id = str(datetime.datetime.now().strftime('%m%d-%H%M%S'))

    cmp_netsz_accuracy(unique_id, e)
    cmp_netsz_iternumbers(unique_id, e)
