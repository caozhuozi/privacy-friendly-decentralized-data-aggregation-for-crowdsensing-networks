import matplotlib.pyplot as plt
import numpy as np
from cutils import random_initialize, set_c
from dp_avg_consensus import theta_inf
import datetime

eps_ = 0.1
s_ = 1.0
q_ = 0
c_ = set_c(eps_, q_, s_)

for n in [150, 200]:

    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = "20"
    plt.rc('axes', axisbelow=True)
    plt.rc('text', usetex=True)
    plt.rcParams['mathtext.fontset'] = 'stix'

    data = []
    state = random_initialize(n, 50, 100)
    for _ in range(10**5):
        data.append(theta_inf(
            state,
            n,
            s_,
            c_,
        ))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(linewidth=1, ls=':')
    ax.hist(
        data,
        bins=90,
        # histtype='step',
        # hatch='/',
        # normed=0,
        facecolor="none",
        edgecolor="black",
        # alpha=0.7,
        # label='Frequency'
    )
    # cheat: use exact mean instead of empirical mean
    ax.scatter([np.mean(state)], [50],
               zorder=10,
               marker='*',
               s=140,
               c='blue',
               label='Empirical Mean')

    ax.axvline(x=np.mean(state), linewidth=3, color='g', label="Exact Average")
    plt.yticks([0, 1000, 2000, 3000, 4000])
    plt.ylim([0 - 10, 4400])
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    ax.set_aspect(1.0 / ax.get_data_ratio() * 0.7)
    ax.legend(prop={'size': 15})
    plt.xlabel(r"$x^{*}$", fontsize=25)
    plt.ylabel("Frequency", fontsize=25)

    # plt.show()
    fig_id = str(datetime.datetime.now().strftime('%m%d-%H%M%S') + "_" +
                 str(n)) + "_histo"

    plt.savefig("../final_exp_publication/histogram/" + fig_id + '.pdf',
                bbox_inches="tight",
                pad_inches=0.01)
    plt.close()
