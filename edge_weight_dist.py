import networkx as nx
import argparse
import matplotlib.pyplot as plt
from math import log


description = """Plot edge weight distribution"""

################################
# parse command line arguments #
################################
parser = argparse.ArgumentParser(
    description=description)

parser.add_argument('gpickle',
                    type=argparse.FileType('r'),
                    help='a pickled networkx graph')

args = parser.parse_args()

g = nx.gpickle.read_gpickle(args.gpickle)

P = {}
for e in g.edges():
    w = float(g.get_edge_data(*e)['weight'])
    if w not in P:
        P[w] = 1
    else:
        P[w] += 1


fig, ax = plt.subplots()
ax.scatter([log(P[k]) for k in P],
           [log(k) for k in P.keys()],
           alpha=0.5)

ax.set_xlabel('edge weight', fontsize=15)
ax.set_ylabel('number of edges', fontsize=15)

ax.set_title('Edge Weight Distribution')

ax.grid(True)
fig.tight_layout()

plt.show()
