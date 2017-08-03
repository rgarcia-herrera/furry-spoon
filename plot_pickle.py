import pickle
import matplotlib.pyplot as plt

with open('data/ingredient_count_dist.pickle', 'r') as f:
    c = pickle.load(f)

for cuisine in c:
    plt.plot(sorted(c[cuisine]['omni'].keys()),
             [c[cuisine]['omni'][n] for n in sorted(c[cuisine]['omni'].keys())],
             'r^-',
             sorted(c[cuisine]['veggie'].keys()),
             [c[cuisine]['veggie'][n] for n in sorted(c[cuisine]['veggie'].keys())],
             'ys-',
             sorted(c[cuisine]['vegan'].keys()),
             [c[cuisine]['vegan'][n] for n in sorted(c[cuisine]['vegan'].keys())],
             'go-',
             linewidth=2.0
    )
    plt.title(cuisine)
    plt.xlabel('ingredients')
    plt.ylabel('recipes')
    plt.savefig("plots/ingredient_count_dist_%s.png" % cuisine)
    plt.clf()


# plot 'em normalized
for cuisine in c:
    plt.plot(sorted(c[cuisine]['omni'].keys()),
             [c[cuisine]['omni'][n]/float(sum(c[cuisine]['omni'].values()))
              for n in sorted(c[cuisine]['omni'].keys())],
             'r^-',
             sorted(c[cuisine]['veggie'].keys()),
             [c[cuisine]['veggie'][n]/float(sum(c[cuisine]['veggie'].values()))
              for n in sorted(c[cuisine]['veggie'].keys())],
             'ys-',
             sorted(c[cuisine]['vegan'].keys()),
             [c[cuisine]['vegan'][n]/float(sum(c[cuisine]['vegan'].values()))
              for n in sorted(c[cuisine]['vegan'].keys())],
             'go-',
             linewidth=2.0
    )
    
    plt.title("%s, normalized" % cuisine)
    plt.xlabel('ingredients')
    plt.ylabel('recipes')
    plt.savefig("plots/ingredient_count_dist_norm_%s.png" % cuisine)
    plt.clf()
