from cgeograph import gen_draw_geograph
from cutils import set_dis, time_stamp, set_c
from cdraw import draw_consensus
from average_consensus import average_consensus
from dp_avg_consensus import dp_avg_consensus
import numpy as np

n = 6

unique_id = time_stamp()
G, _ = gen_draw_geograph(n, set_dis(n), unique_id)
state_ = [70, 74, 77, 80, 84, 87]
avg = np.mean(state_)
q_ = 0
s_ = 1.0
dp_eps_ = 0.1
c_ = set_c(dp_eps_, q_, s_)

for _ in range(20):

    records = average_consensus(G, unique_id, state=state_)
    if np.size(records, 1) < 10:
        continue
    draw_consensus(records, unique_id + "_none" + "_cons")
    for dp_eps_ in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:

        c_ = set_c(dp_eps_, q_, s_)
        records = dp_avg_consensus(G,
                                   unique_id, [c_ for _ in range(n)],
                                   [q_ for _ in range(n)],
                                   [s_ for _ in range(n)],
                                   state=state_)

        conv = np.mean(records[:, -1])
        dt = abs(avg - conv)
        dt_flg = 'tinyminus'
        if dt > 0.5 and dt < 1:
            dt_flg = 'tiny'
        elif dt >= 1 and dt < 2:
            df_flg = 'tinyplus'
        elif dt >= 2 and dt < 3:
            dt_flg = 'medium'
        elif dt >= 3:
            dt_flg = 'large'

        draw_consensus(
            records,
            unique_id + "_eps_" + str(dp_eps_) + "_" + dt_flg + "_cons", 1)
