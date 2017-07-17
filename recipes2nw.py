import networkx as nx
import csv
from itertools import combinations


g = nx.Graph()
with open('data/srep00196-s3.csv') as f:
    reader = csv.reader(f)
    for r in reader:
        # discard comments
        if r[0].startswith('#'):
            continue

        # connect all combinations of two ingredients, repeats sum weight
        for pair in combinations(r[1:], 2):
            e = g.get_edge_data(*pair)
            if e:
                w = e['weight'] + 1
            else:
                w = 1
            g.add_edge(*pair, weight=w)

nx.gpickle.write_gpickle(g, 'data/full_nw.pickle')
