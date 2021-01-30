import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from cycler import cycler


def draw_consensus(records, fig_id, flg=0):

    n = np.size(records, 0)
    cols = np.size(records, 1)
    # average value
    avg = np.mean(records[:, 0])
    conv = np.mean(records[:, -1])
    r = records.tolist()
    x = [i for i in range(cols)]

    cc = (cycler(
        color=['blue', 'orange', 'red', 'cyan', 'magenta', 'grey', 'black']))
    fig = plt.figure()
    ax = fig.gca()
    plt.tight_layout()
    plt.rc('axes', prop_cycle=cc)
    plt.rc('text', usetex=True)
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = "20"

    for i in range(n):
        plt.plot(x,
                 r[i],
                 marker='x',
                 linestyle='--',
                 lw=1,
                 label='terminal ' + str(i + 1))

    # horizon line of average value
    plt.hlines(avg,
               xmin=0,
               xmax=cols + 1,
               color='green',
               linestyle=':',
               linewidth=2,
               label="Exact Average")
    plt.plot([0], [avg], marker='o', markersize=6, color='green')
    if flg != 0:
        plt.vlines(x=cols - 1,
                   ymin=min(avg, conv),
                   ymax=max(avg, conv),
                   linestyle=':',
                   lw=2,
                   color='black',
                   label=r'$|x^{*} -\bar{\mathbf{x}}|$')
        plt.hlines(y=avg,
                   xmin=cols - 1 - 0.2,
                   xmax=cols - 1 + 0.2,
                   lw=2,
                   color='black')
        plt.hlines(y=conv,
                   xmin=cols - 1 - 0.2,
                   xmax=cols - 1 + 0.2,
                   lw=2,
                   color='black')
    # dt = "{0:.2f}".format(abs(avg - conv))
    # text_str = r'$\Delta={}$'.format(str(dt))
    # plt.text(x=cols - 1 - 1.5, y=(avg + conv) / 2, s=text_str, fontsize=14)

    # custom the x tickets
    # if cols <= 30:
    #     xt = [0, 1, 2, 3, 4]
    #     for i in range(5, cols + 1, 5):
    #         xt.append(i)
    #     plt.xticks(xt)

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.xlim(xmin=-0.07, xmax=cols + 1)
    plt.yticks(records[:, 0].tolist())

    plt.xlabel("Number of Iterations", fontsize=23)
    plt.ylabel("Local Aggregation Records", fontsize=23)
    plt.legend(prop={'size': 12}, ncol=2)
    plt.grid(ls=':')

    plt.savefig("../final_exp_publication/consensus/" + fig_id + ".pdf",
                bbox_inches="tight",
                pad_inches=0.01)
    plt.close()


def draw_geograph(G, fig_id):

    pos = nx.get_node_attributes(G, 'pos')
    plt.figure(figsize=(8, 8))
    plt.tight_layout()
    # # nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    # if node_list is specified, the function will only draw nodes in node_list
    # node_color is used for testing
    nx.draw_networkx_nodes(
        G,
        pos,
        # nodelist=list(p.keys()),
        node_size=60,
        node_color='none',
        edgecolors='black'
        # node_color=list(p.values()),
        # cmap=plt.cm.Reds_r
    )

    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    # plt.axis('off')
    # plt.show()
    plt.savefig("../final_exp_publication/networks_topo/" + fig_id + ".pdf",
                bbox_inches="tight",
                pad_inches=0.01)
    plt.close()

    A = nx.to_numpy_matrix(G)
    # save the graph data
    np.savetxt("../graphdata/" + fig_id + ".csv", A, delimiter=",")

    return G, fig_id
