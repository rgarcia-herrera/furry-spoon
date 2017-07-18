import networkx as nx
from math import sin, cos, radians
from pony.orm import db_session, Database, Required, Json
from pyveplot import Hiveplot, Axis, Node


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
offcenter = 50
center = (250, 250)
rotation = 60
axis_vegan0_start = rotate(offcenter,
                           angle=rotation - 20,
                           origin=center)
axis_vegan0_end = rotate(offcenter + len(vegan)*4,
                         angle=rotation - 30,
                         origin=axis_vegan0_start)
axis_vegan0 = Axis(axis_vegan0_start, axis_vegan0_end,
                   stroke="darkgreen", stroke_opacity="0.3", stroke_width=4)


axis_vegan1_start = rotate(offcenter,
                           angle=rotation + 10,
                           origin=center)
axis_vegan1_end = rotate(offcenter + len(vegan)*4,
                         angle=rotation + 10,
                         origin=axis_vegan1_start)
axis_vegan1 = Axis(axis_vegan1_start, axis_vegan1_end,
                   stroke="darkgreen", stroke_opacity="0.3", stroke_width=4)


axis_carnic0_start = rotate(offcenter,
                            angle=rotation + 120 - 10,
                            origin=center)
axis_carnic0_end = rotate(offcenter + len(carnic)*4,
                          angle=rotation + 120 - 10,
                          origin=axis_carnic0_start)
axis_carnic0 = Axis(axis_carnic0_start, axis_carnic0_end,
                    stroke="red", stroke_opacity="0.3", stroke_width=4)

axis_carnic1_start = rotate(offcenter,
                            angle=rotation + 120 + 10,
                            origin=center)
axis_carnic1_end = rotate(offcenter + len(carnic)*4,
                          angle=rotation + 120 + 10,
                          origin=axis_carnic1_start)
axis_carnic1 = Axis(axis_carnic1_start, axis_carnic1_end,
                    stroke="red", stroke_opacity="0.3", stroke_width=4)


axis_animal0_start = rotate(offcenter,
                            angle=rotation + 240 - 10,
                            origin=center)
axis_animal0_end = rotate(offcenter + len(animal)*4,
                          angle=rotation + 240 - 10,
                          origin=axis_animal0_start)
axis_animal0 = Axis(axis_animal0_start, axis_animal0_end,
                    stroke="darkkhaki", stroke_opacity="0.8", stroke_width=4)


axis_animal1_start = rotate(offcenter,
                            angle=rotation + 240 + 10,
                            origin=center)
axis_animal1_end = rotate(offcenter + len(animal)*4,
                          angle=rotation + 240 + 10,
                          origin=axis_animal1_start)
axis_animal1 = Axis(axis_animal1_start, axis_animal1_end,
                    stroke="darkkhaki", stroke_opacity="0.8", stroke_width=4)

j = 0.0
for n in carnic:
    j += 1.0
    axis_carnic0.add_node(Node(n[1]), j / len(carnic))
    axis_carnic1.add_node(Node(n[1]), j / len(carnic))
j = 0.0
for n in animal:
    j += 1.0
    axis_animal0.add_node(Node(n[1]), j / len(animal))
    axis_animal1.add_node(Node(n[1]), j / len(animal))
j = 0.0
for n in vegan:
    j += 1.0
    axis_vegan0.add_node(Node(n[1]), j / len(vegan))
    axis_vegan1.add_node(Node(n[1]), j / len(vegan))


# edges from axis0 to axis1
for e in g.edges():
    if ((e[0] in axis_vegan0.nodes) and (e[1] in axis_vegan1.nodes)) or \
       ((e[1] in axis_vegan0.nodes) and (e[0] in axis_vegan1.nodes)):
        h.connect(axis_vegan0, e[0],
                  5,  # angle of invisible axis for source control points
                  axis_vegan1, e[1],
                  -5,  # angle of invisible axis for target control points
                  stroke_width=0.2,  # pass any SVG attributes to an edge
                  stroke_opacity=0.2,
                  stroke='limegreen')

    elif ((e[0] in axis_animal0.nodes) and (e[1] in axis_animal1.nodes)) or \
         ((e[1] in axis_animal0.nodes) and (e[0] in axis_animal1.nodes)):
        h.connect(axis_animal0, e[0],
                  5,  # angle of invisible axis for source control points
                  axis_animal1, e[1],
                  -5,  # angle of invisible axis for target control points
                  stroke_width=0.2,  # pass any SVG attributes to an edge
                  stroke_opacity=0.2,
                  stroke='burlywood')

    elif ((e[0] in axis_carnic0.nodes) and (e[1] in axis_carnic1.nodes)) or \
         ((e[1] in axis_carnic0.nodes) and (e[0] in axis_carnic1.nodes)):
        h.connect(axis_carnic0, e[0],
                  5,  # angle of invisible axis for source control points
                  axis_carnic1, e[1],
                  -5,  # angle of invisible axis for target control points
                  stroke_width=0.2,  # pass any SVG attributes to an edge
                  stroke_opacity=0.2,
                  stroke='darkred')

    elif ((e[0] in axis_vegan1.nodes) and (e[1] in axis_carnic0.nodes)) or \
         ((e[1] in axis_carnic0.nodes) and (e[0] in axis_vegan1.nodes)):
        h.connect(axis_vegan1, e[0],
                  35,  # angle of invisible axis for source control points
                  axis_carnic0, e[1],
                  -35,  # angle of invisible axis for target control points
                  stroke_width=0.3,  # pass any SVG attributes to an edge
                  stroke_opacity=0.3,
                  stroke='brown')

    elif ((e[0] in axis_carnic1.nodes) and (e[1] in axis_animal0.nodes)) or \
         ((e[1] in axis_animal0.nodes) and (e[0] in axis_carnic1.nodes)):
        h.connect(axis_carnic1, e[0],
                  20,  # angle of invisible axis for source control points
                  axis_animal0, e[1],
                  -20,  # angle of invisible axis for target control points
                  stroke_width=0.3,  # pass any SVG attributes to an edge
                  stroke_opacity=0.3,
                  stroke='peru')

    elif ((e[0] in axis_animal1.nodes) and (e[1] in axis_vegan0.nodes)) or \
         ((e[1] in axis_vegan0.nodes) and (e[0] in axis_animal1.nodes)):
        h.connect(axis_animal1, e[0],
                  35,  # angle of invisible axis for source control points
                  axis_vegan0, e[1],
                  -35,  # angle of invisible axis for target control points
                  stroke_width=0.3,  # pass any SVG attributes to an edge
                  stroke_opacity=0.3,
                  stroke='darkkhaki')


h.save()
