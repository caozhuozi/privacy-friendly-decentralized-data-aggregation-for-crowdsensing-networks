from dp_avg_consensus import direct_cal_diff, theo_var
from cutils import random_initialize, set_c
# from cgeograph import gen_draw_geograph
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import datetime
'''
 these simulation figures can be done even without generating graph structures
'''
'''
  for draw_acc, the maker of func scatter is set to 'H' with size=100

'''


def draw_acc(n, x_cords, y_cords, fig_id):

    fig = plt.figure()

    # plt.rcParams["font.family"] = "Times New Roman"
    # plt.rcParams["font.size"] = "15"

    plt.rc('text', usetex=True)
    plt.rc('font', family='Times New Roman', weight='normal', size=14)
    plt.rcParams['mathtext.fontset'] = 'stix'
    # set_xscale only supported in add_subplot
    ax = fig.add_subplot(111)
    rows = len(x_cords)

    for i in range(rows):
        ax.scatter(
            x_cords[i],
            y_cords[i],
            marker='H',
            s=100,
            # color="#007dff",
            color='none',
            # color='b',
            edgecolors='black',
            label='convergency point for each run')

        ax.axvline(x=eps_swp[i], c='grey', ls=':', lw=1)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim([10**-2 - 10**-3, 10**2 + 10])
    ax.set_ylim([10**-4, 10**2])

    ax.yaxis.grid(ls=':')
    ax.set_aspect(1.0 / ax.get_data_ratio() * 0.4)
    # custom legend
    legend_elements = [
        Line2D([0], [0],
               c='none',
               marker='H',
               markerfacecolor='none',
               markeredgecolor='black',
               label='error of each run',
               markersize=9)
    ]
    ax.legend(handles=legend_elements, prop={'size': 20})

    plt.xticks(fontsize=20, weight='bold')
    plt.yticks(fontsize=20, weight='bold')
    plt.xlabel(r"$\bar{\epsilon}$", fontsize=28)
    plt.ylabel(r"$|x^{*} - \bar{\mathbf{x}}|$", fontsize=28)

    plt.savefig("../final_exp_publication/privacy_acc_var/" + fig_id + '.pdf',
                bbox_inches="tight",
                pad_inches=0.01)
    # plt.show()
    plt.close()


def draw_var(n, eps_swp, var_cords, fig_id):

    fig = plt.figure()
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = "15"
    # set_xscale only supported in add_subplot
    ax = fig.add_subplot(111)
    # ax.set_aspect(1 / 2)

    ax.scatter(
        eps_swp,
        var_cords,
        marker='o',
        facecolors='none',
        edgecolors='black',
        linewidth=2,
        s=80,  # markersize
        label='Sample Variance')

    #     ax.plot(eps_swp[i],
    #             var_cords[i],
    #             marker='o',
    #             # color="#007dff",
    #             color='black',
    #             # markeredgecolor='black',
    #             markersize=7)

    for eps in eps_swp:
        ax.axvline(x=eps, c='grey', ls=':', lw=1)

    ax.plot(eps_swp, [theo_var(n, eps) for eps in eps_swp], c='green', ls=':')
    ax.scatter(eps_swp, [theo_var(n, eps) for eps in eps_swp],
               edgecolors='green',
               marker='*',
               s=100,
               label='Theoretical Variance')

    ax.yaxis.grid(ls=':')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim([10**-2 - 10**-3, 10**2 + 10])
    # ax.set_ylim([10**-5 - 10**-6, 10**1 + 1])

    ax.set_aspect(1.0 / 3.5)
    ax.legend(prop={'size': 18})

    plt.xticks(fontsize=20, weight='bold')
    plt.yticks(fontsize=20, weight='bold')

    plt.xlabel(r'$\bar{\epsilon}$', fontsize=28)
    plt.ylabel('Variance', fontsize=25, weight='bold')
    plt.savefig("../final_exp_publication/privacy_acc_var/" + fig_id + '.pdf',
                bbox_inches="tight",
                pad_inches=0.01)
    # plt.show()
    plt.close()


# delta = 1.0
'''
  for all the experiments in this part,  q_i(for all i), and s_i(for all i) are equal
'''
q_ = 0  # one-shot adding
s_ = 1.0
eps_swp = [10**step for step in np.arange(-2, 2.1, 0.2)]

unique_id = str(datetime.datetime.now().strftime('%m%d-%H%M%S'))

for n in [50, 100, 150, 200]:
    # for n in [50]:

    state = random_initialize(n, 50, 100)

    fig = plt.figure()
    # set_xscale only supported in add_subplot
    ax = fig.add_subplot(111)

    x_cords = []
    y_cords = []
    var_cords = []

    for eps in eps_swp:
        # x_cord is filed with the same eps
        x_cord = []
        y_cord = []
        # optimal setting
        c_ = set_c(eps, q_, s_)

        # run 20 times for each eps
        for _ in range(20):
            x_cord.append(eps)
            y_cord.append(direct_cal_diff(n, s_, c_))
        x_cords.append(x_cord)
        y_cords.append(y_cord)
        var_cords.append(np.var(y_cord, ddof=1))

    acc_fig_id = unique_id + "_" + str(n) + "_acc"
    var_fig_id = unique_id + "_" + str(n) + "_var"
    draw_acc(n, x_cords, y_cords, acc_fig_id)
    draw_var(n, eps_swp, var_cords, var_fig_id)
