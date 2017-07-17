from pyveplot import Hiveplot, Axis
import networkx as nx
from math import sin, cos, radians
from pony.orm import db_session, Database, Required, Json
from pprint import pprint

db = Database()


class Ingredient(db.Entity):
    name = Required(str)
    tags = Required(Json)


db.bind('sqlite', 'data/ingredients.sqlite', create_db=False)
db.generate_mapping(create_tables=False)

g = nx.gpickle.read_gpickle('data/full_nw.pickle')

with db_session:
    carnic = sorted([(g.degree(i.name), i.name)
                     for i in Ingredient.select(lambda i:
                                                'carnic' in i.tags)])
    vegan = sorted([(g.degree(i.name), i.name)
                    for i in Ingredient.select(lambda i:
                                               'vegan' in i.tags)])
    animal = sorted([(g.degree(i.name), i.name)
                     for i in Ingredient.select(lambda i:
                                                'animal origin' in i.tags)])


def rotate(radius, angle, origin=(0, 0)):
    """ Returns a tuple of destination coordinates
        given a radius, angle and origin tuple """
    return (origin[0] + round((radius * cos(radians(angle))), 2),
            origin[1] + round((radius * sin(radians(angle))), 2))


h = Hiveplot('ingredients_3cat.svg')
offcenter = 10
center = (250, 250)
rotation = 9
axis_vegan0_start = rotate(offcenter,
                           angle=rotation - 10,
                           origin=center)
axis_vegan0_end = rotate(offcenter + len(vegan)*4,
                         angle=rotation - 10,
                         origin=axis_vegan0_start)
axis_vegan0 = Axis(axis_vegan0_start, axis_vegan0_end,
                   stroke="green", stroke_opacity="0.3", stroke_width=2)


axis_vegan1_start = rotate(offcenter,
                           angle=rotation + 10,
                           origin=center)
axis_vegan1_end = rotate(offcenter + len(vegan)*4,
                         angle=rotation + 10,
                         origin=axis_vegan1_start)
axis_vegan1 = Axis(axis_vegan1_start, axis_vegan1_end,
                   stroke="green", stroke_opacity="0.3", stroke_width=2)


axis_carnic0_start = rotate(offcenter,
                            angle=rotation + 120 - 10,
                            origin=center)
axis_carnic0_end = rotate(offcenter + len(carnic)*4,
                          angle=rotation + 120 - 10,
                          origin=axis_carnic0_start)
axis_carnic0 = Axis(axis_carnic0_start, axis_carnic0_end,
                    stroke="red", stroke_opacity="0.3", stroke_width=2)

axis_carnic1_start = rotate(offcenter,
                            angle=rotation + 120 + 10,
                            origin=center)
axis_carnic1_end = rotate(offcenter + len(carnic)*4,
                          angle=rotation + 120 + 10,
                          origin=axis_carnic1_start)
axis_carnic1 = Axis(axis_carnic1_start, axis_carnic1_end,
                    stroke="red", stroke_opacity="0.3", stroke_width=2)


axis_animal0_start = rotate(offcenter,
                            angle=rotation + 240 - 10, 
                            origin=center)
axis_animal0_end = rotate(offcenter + len(animal)*4,
                          angle=rotation + 240 - 10,
                          origin=axis_animal0_start)
axis_animal0 = Axis(axis_animal0_start, axis_animal0_end,
                    stroke="blue", stroke_opacity="0.3", stroke_width=2)


axis_animal1_start = rotate(offcenter,
                            angle=rotation + 240 + 10,
                            origin=center)
axis_animal1_end = rotate(offcenter + len(animal)*4,
                          angle=rotation + 240 + 10,
                          origin=axis_animal1_start)
axis_animal1 = Axis(axis_animal1_start, axis_animal1_end,
                    stroke="blue", stroke_opacity="0.3", stroke_width=2)


h.axes = [axis_animal0, axis_animal1,
          axis_carnic0, axis_carnic1,
          axis_vegan0, axis_vegan1]

h.save()
