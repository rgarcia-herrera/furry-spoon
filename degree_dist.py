import networkx as nx
import argparse
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook


description = """Plot degree distribution"""

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
for n in g.nodes():
    if float(g.degree(n))/len(g.nodes()) in P:
        P[float(g.degree(n))/len(g.nodes())] += 1
    else:
        P[float(g.degree(n))/len(g.nodes())] = 1


fig, ax = plt.subplots()
ax.scatter([P[k] for k in P],
           P.keys(),
           alpha=0.5)

from pprint import pprint

pprint(P)
ax.set_xlabel(r'$k$', fontsize=15)
ax.set_ylabel(r'$p(k)$', fontsize=15)

ax.set_title('Degree vs count')

ax.grid(True)
fig.tight_layout()

plt.show()
