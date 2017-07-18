import networkx as nx
import csv
from itertools import combinations


# all networks
n = {}
with open('data/srep00196-s3.csv') as f:
    reader = csv.reader(f)
    for r in reader:
        # discard comments
        if r[0].startswith('#'):
            continue
        cuisine = r[0]

        # a different network per cuisine
        if cuisine not in n:
            n[cuisine] = nx.Graph()

        # connect all combinations of two ingredients, repeats sum weight
        for pair in combinations(r[1:], 2):
            e = n[cuisine].get_edge_data(*pair)
            if e:
                w = e['weight'] + 1
            else:
                w = 1
            n[cuisine].add_edge(*pair, weight=w)

# write out a pickle per cuisine
for cuisine in n:
    nx.gpickle.write_gpickle(n[cuisine], 'data/%s_omni.pickle' % cuisine)
