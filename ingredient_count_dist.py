import csv
from pony.orm import *

db = Database()


class Ingredient(db.Entity):
    name = Required(str)
    tags = Required(Json)


db.bind('sqlite', 'data/ingredients.sqlite', create_db=False)
db.generate_mapping(create_tables=False)


with db_session:
    carnic = sorted([i.name
                     for i in Ingredient.select(lambda i:
                                                'carnic' in i.tags)],
                    reverse=True)
    vegan = sorted([i.name
                    for i in Ingredient.select(lambda i:
                                               'vegan' in i.tags)],
                   reverse=True)
    animal = sorted([i.name
                     for i in Ingredient.select(lambda i:
                                                'animal origin' in i.tags)],
                    reverse=True)


ings = {}

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

        veggie_r = []
        for ingredient in r[1:]:
            if ingredient not in carnic:
                veggie_r.append(ingredient)
        ings[cuisine]['veggie'].append(veggie_r)

        vegan_r = []
        for ingredient in r[1:]:
            if ingredient not in carnic and ingredient not in animal:
                vegan_r.append(ingredient)
        ings[cuisine]['vegan'].append(vegan_r)


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


from pprint import pprint                
pprint(c)

import matplotlib.pyplot as plt

for cuisine in c:
    for tag in ('omni', 'veggie', 'vegan'):
        plt.plot(c[cuisine][tag].keys(), c[cuisine][tag].values())
        plt.ylabel('%s %s' % (cuisine, tag))
        plt.show()
