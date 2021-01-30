import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from cutils import set_dis, time_stamp
from cgeograph import gen_draw_geograph

# fig, ax = plt.subplots(nrows=2, ncols=2)

# G = nx.random_geometric_graph(50. 0.3)

unique_id = time_stamp()
for n in [50, 100, 150, 200]:
    gen_draw_geograph(n, set_dis(n), unique_id)
