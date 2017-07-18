import networkx as nx
from pony.orm import db_session, Database, Required, Json


db = Database()


class Ingredient(db.Entity):
    name = Required(str)
    tags = Required(Json)


db.bind('sqlite', 'data/ingredients.sqlite', create_db=False)
db.generate_mapping(create_tables=False)

g = nx.gpickle.read_gpickle('data/omnivorous.pickle')

with db_session:
    carnic = [i.name for i in Ingredient.select(lambda i:
                                                'carnic' in i.tags)]
    animal = [i.name for i in Ingredient.select(lambda i:
                                                'animal origin' in i.tags)]

vegetarian = g.copy()
vegetarian.remove_nodes_from(carnic)
nx.gpickle.write_gpickle(vegetarian, 'data/vegetarian_nw.pickle')


vegan = g.copy()
vegan.remove_nodes_from(carnic)
vegan.remove_nodes_from(animal)
nx.gpickle.write_gpickle(vegan, 'data/vegan_nw.pickle')
