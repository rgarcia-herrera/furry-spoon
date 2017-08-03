import csv
import pickle
import model

ings = {'WorldWide': {'omni': [],
               'veggie': [],
               'vegan': []}}

with open('data/srep00196-s3.csv') as f:
    reader = csv.reader(f)
    all = set()
    for r in reader:
        # discard comments
        if r[0].startswith('#'):
            continue

        cuisine = r[0]

        if cuisine not in ings:
            ings[cuisine] = {'omni': [],
                             'veggie': [],
                             'vegan': []}

        ings[cuisine]['omni'].append(r[1:])
        ings['WorldWide']['omni'].append(r[1:])

        veggie_r = []
        for ingredient in r[1:]:
            if ingredient not in model.carnic:
                veggie_r.append(ingredient)
        ings[cuisine]['veggie'].append(veggie_r)
        ings['WorldWide']['veggie'].append(veggie_r)

        vegan_r = []
        for ingredient in r[1:]:
            if ingredient not in model.carnic and ingredient not in model.animal:
                vegan_r.append(ingredient)
        ings[cuisine]['vegan'].append(vegan_r)
        ings['WorldWide']['vegan'].append(vegan_r)


#count
c = {cuisine: {'omni': {},
               'veggie': {},
               'vegan': {}} for cuisine in ings.keys()}

for cuisine in ings:
    for tag in ('omni', 'veggie', 'vegan'):
        for recipe in ings[cuisine][tag]:
            size = len(recipe)
            if size in c[cuisine][tag]:
                c[cuisine][tag][size] += 1
            else:
                c[cuisine][tag][size] = 1


with open('data/ingredient_count_dist.pickle', 'w') as f:
    pickle.dump(c, f)
