import networkx as nx
import csv
from itertools import combinations
from random import sample

# all networks
R = {}
with open('data/srep00196-s3.csv') as f:
    reader = csv.reader(f)
    for r in reader:
        # discard comments
        if r[0].startswith('#'):
            continue
        cuisine = r[0]

        if cuisine not in R:
            R[cuisine] = [r[1:],]
        else:
            R[cuisine].append(r[1:])

S = {}
for cuisine in R:
    if len(R[cuisine]) >= 2512:
        S[cuisine] = sample(R[cuisine], 2512)

# build networks from sampled recipes
G = {}
for cuisine in S:
    # a different network per cuisine
    if cuisine not in G:
        G[cuisine] = nx.Graph()

    # connect all combinations of two ingredients, repeats sum weight
    for r in S[cuisine]:
        for pair in combinations(r, 2):
            e = G[cuisine].get_edge_data(*pair)
            if e:
                w = e['weight'] + 1
            else:
                w = 1
            G[cuisine].add_edge(*pair, weight=w)

for cuisine in G:
    # write an edgelist by cuisine
    nx.edgelist.write_weighted_edgelist(G[cuisine],
                                        'data/sampled/%s_edgelist.csv' % cuisine,
                                        comments='#',
                                        delimiter=',',
                                        encoding='utf-8')
    # write out unique ingredients
    ingredients = set(G[cuisine].nodes())
    with open('data/sampled/ingredients_%s.csv' % cuisine, 'w') as o:
        o.writelines(['%s\n' % i for i in ingredients])
