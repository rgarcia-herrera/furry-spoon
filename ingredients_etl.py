import csv
from pony.orm import *

db = Database()


class Ingredient(db.Entity):
    name = Required(str)
    tags = Required(Json)


with open('data/srep00196-s3.csv') as f:
    reader = csv.reader(f)
    all = set()
    for r in reader:
        # discard comments
        if r[0].startswith('#'):
            continue

        for ingredient in r[1:]:
            all.add(ingredient)

db.bind('sqlite', 'ingredients.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

with db_session:
    for ingredient in all:
        Ingredient(name=ingredient, tags=[])
