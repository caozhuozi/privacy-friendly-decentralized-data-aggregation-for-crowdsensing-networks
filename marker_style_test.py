
def test_marker(n, x_cords, y_cords, mk):

    fig = plt.figure()
    # set_xscale only supported in add_subplot
    ax = fig.add_subplot(111)
    rows = len(x_cords)

    for i in range(rows):
        ax.scatter(
            x_cords[i],
            y_cords[i],
            marker=mk,
            s=100,
            # color="#007dff",
            color='none',
            # color='b',
            edgecolors='black')

        ax.axvline(x=eps_swp[i], c='grey', ls=':', lw=1)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim([10**-2 - 10**-3, 10**2 + 10])
    ax.set_ylim([10**-4, 10**2])

    ax.yaxis.grid(ls=':')
    ax.set_aspect(1.0 / ax.get_data_ratio() * 0.3)
    plt.savefig("../tmp/" + str(ord(mk)) + '.pdf',
                bbox_inches="tight",
                pad_inches=0.1)
    # plt.show()
    plt.close()




mks = ['o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'd', 'D']

for mk in mks:
    n = 50
    state = random_initialize(n, 50, 100)

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

    test_marker(n, x_cords, y_cords, mk)
