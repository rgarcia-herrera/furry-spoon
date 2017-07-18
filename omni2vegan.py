import networkx as nx
from pony.orm import db_session, Database, Required, Json
import argparse
from os import path

description = """Create vegetarian and vegan networks by removing
ingredients from omnivorous networks."""

################################
# parse command line arguments #
################################
parser = argparse.ArgumentParser(
    description=description)

parser.add_argument('gpickle',
                    type=argparse.FileType('r'),
                    help='a pickled networkx graph')

args = parser.parse_args()



db = Database()


class Ingredient(db.Entity):
    name = Required(str)
    tags = Required(Json)


db.bind('sqlite', 'data/ingredients.sqlite', create_db=False)
db.generate_mapping(create_tables=False)

g = nx.gpickle.read_gpickle(args.gpickle)

with db_session:
    carnic = [i.name for i in Ingredient.select(lambda i:
                                                'carnic' in i.tags)]
    animal = [i.name for i in Ingredient.select(lambda i:
                                                'animal origin' in i.tags)]

vegetarian = g.copy()
vegetarian.remove_nodes_from(carnic)

prefix = path.basename(args.gpickle.name).split('.')[0]
veggie_path = path.join(path.dirname(args.gpickle.name),
                        "vegetarian_%s.pickle" % prefix)
print "writing %s" % veggie_path
nx.gpickle.write_gpickle(vegetarian, veggie_path)


vegan = g.copy()
vegan.remove_nodes_from(carnic)
vegan.remove_nodes_from(animal)
vegan_path = path.join(path.dirname(args.gpickle.name),
                       "vegan_%s.pickle" % prefix)
print "writing %s" % vegan_path
nx.gpickle.write_gpickle(vegan, vegan_path)
