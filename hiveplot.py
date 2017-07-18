import networkx as nx
from math import sin, cos, radians
from pony.orm import db_session, Database, Required, Json
from pyveplot import Hiveplot, Axis, Node
import argparse
from os import path

description = """Create hiveplot from pickled ingredient graph."""

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
    carnic = sorted([(g.degree(i.name), i.name)
                     for i in Ingredient.select(lambda i:
                                                'carnic' in i.tags)],
                    reverse=True)
    vegan = sorted([(g.degree(i.name), i.name)
                    for i in Ingredient.select(lambda i:
                                               'vegan' in i.tags)],
                   reverse=True)
    animal = sorted([(g.degree(i.name), i.name)
                     for i in Ingredient.select(lambda i:
                                                'animal origin' in i.tags)],
                    reverse=True)


def rotate(radius, angle, origin=(0, 0)):
    """ Returns a tuple of destination coordinates
        given a radius, angle and origin tuple """
    return (origin[0] + round((radius * cos(radians(angle))), 2),
            origin[1] + round((radius * sin(radians(angle))), 2))


prefix = path.basename(args.gpickle.name).split('.')[0]
hive_path = path.join("plots",
                      "%s.svg" % prefix)

h = Hiveplot(hive_path)
offcenter = 50
center = (250, 250)
rotation = 60
axis_vegan0_start = rotate(offcenter,
                           angle=rotation - 30,
                           origin=center)
axis_vegan0_end = rotate(offcenter + len(vegan)*4,
                         angle=rotation - 30,
                         origin=axis_vegan0_start)
axis_vegan0 = Axis(axis_vegan0_start, axis_vegan0_end,
                   stroke="darkgreen", stroke_opacity="1", stroke_width=3)


axis_vegan1_start = rotate(offcenter,
                           angle=rotation + 10,
                           origin=center)
axis_vegan1_end = rotate(offcenter + len(vegan)*4,
                         angle=rotation + 10,
                         origin=axis_vegan1_start)
axis_vegan1 = Axis(axis_vegan1_start, axis_vegan1_end,
                   stroke="darkgreen", stroke_opacity="1", stroke_width=3)


axis_carnic0_start = rotate(offcenter,
                            angle=rotation + 120 - 15,
                            origin=center)
axis_carnic0_end = rotate(offcenter + len(carnic)*4,
                          angle=rotation + 120 - 10,
                          origin=axis_carnic0_start)
axis_carnic0 = Axis(axis_carnic0_start, axis_carnic0_end,
                    stroke="darkred", stroke_opacity="1", stroke_width=3)

axis_carnic1_start = rotate(offcenter,
                            angle=rotation + 120 + 15,
                            origin=center)
axis_carnic1_end = rotate(offcenter + len(carnic)*4,
                          angle=rotation + 120 + 10,
                          origin=axis_carnic1_start)
axis_carnic1 = Axis(axis_carnic1_start, axis_carnic1_end,
                    stroke="darkred", stroke_opacity="1", stroke_width=2)


axis_animal0_start = rotate(offcenter,
                            angle=rotation + 240 - 12,
                            origin=center)
axis_animal0_end = rotate(offcenter + len(animal)*4,
                          angle=rotation + 240 - 10,
                          origin=axis_animal0_start)
axis_animal0 = Axis(axis_animal0_start, axis_animal0_end,
                    stroke="darkkhaki", stroke_opacity="1", stroke_width=2)


axis_animal1_start = rotate(offcenter,
                            angle=rotation + 240 + 12,
                            origin=center)
axis_animal1_end = rotate(offcenter + len(animal)*4,
                          angle=rotation + 240 + 10,
                          origin=axis_animal1_start)
axis_animal1 = Axis(axis_animal1_start, axis_animal1_end,
                    stroke="darkkhaki", stroke_opacity="1", stroke_width=2)

j = 0.0
for n in carnic:
    j += 1.0
    n0 = Node(n[1])
    n1 = Node(n[1])
    axis_carnic0.add_node(n0, j / len(carnic))
    axis_carnic1.add_node(n1, j / len(carnic))
    n0.dwg = n0.dwg.circle(center=(n0.x, n0.y),
                           r=2,
                           stroke_width=0,
                           fill='darkred',
                           fill_opacity=0.3)
    n1.dwg = n1.dwg.circle(center=(n1.x, n1.y),
                           r=2,
                           stroke_width=0,
                           fill='darkred',
                           fill_opacity=0.3)

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


h.axes = [axis_animal0, axis_animal1,
          axis_carnic0, axis_carnic1,
          axis_vegan0, axis_vegan1]

edges = 0
for e in g.edges():
    #
    # same axis connections
    #
    if ((e[0] in axis_vegan0.nodes) and (e[1] in axis_vegan1.nodes)) or \
       ((e[1] in axis_vegan0.nodes) and (e[0] in axis_vegan1.nodes)):
        h.connect(axis_vegan0, e[0],
                  15,  # angle of invisible axis for source control points
                  axis_vegan1, e[1],
                  -15,  # angle of invisible axis for target control points
                  stroke_width=0.2,
                  stroke_opacity=0.2,
                  stroke='limegreen')
        edges += 1

    elif ((e[0] in axis_animal0.nodes) and (e[1] in axis_animal1.nodes)) or \
         ((e[1] in axis_animal0.nodes) and (e[0] in axis_animal1.nodes)):
        h.connect(axis_animal0, e[0],
                  5,  # angle of invisible axis for source control points
                  axis_animal1, e[1],
                  -5,  # angle of invisible axis for target control points
                  stroke_width=0.2,
                  stroke_opacity=0.6,
                  stroke='sienna')
        edges += 1

    elif ((e[0] in axis_carnic0.nodes) and (e[1] in axis_carnic1.nodes)) or \
         ((e[1] in axis_carnic0.nodes) and (e[0] in axis_carnic1.nodes)):
        h.connect(axis_carnic0, e[0],
                  5,  # angle of invisible axis for source control points
                  axis_carnic1, e[1],
                  -5,  # angle of invisible axis for target control points
                  stroke_width=0.2,
                  stroke_opacity=0.4,
                  stroke='red')
        edges += 1

    #
    # connect different axes
    #
    elif ((e[0] in axis_vegan1.nodes) and (e[1] in axis_carnic0.nodes)):
        h.connect(axis_vegan1, e[0],
                  35,  # angle of invisible axis for source control points
                  axis_carnic0, e[1],
                  -35,  # angle of invisible axis for target control points
                  stroke_width=0.3,
                  stroke_opacity=0.3,
                  stroke='goldenrod')
        edges += 1
    elif ((e[1] in axis_vegan1.nodes) and (e[0] in axis_carnic0.nodes)):
        h.connect(axis_vegan1, e[1],
                  35,  # angle of invisible axis for source control points
                  axis_carnic0, e[0],
                  -35,  # angle of invisible axis for target control points
                  stroke_width=0.3,
                  stroke_opacity=0.3,
                  stroke='goldenrod')
        edges += 1

    elif ((e[0] in axis_carnic1.nodes) and (e[1] in axis_animal0.nodes)):
        h.connect(axis_carnic1, e[0],
                  20,  # angle of invisible axis for source control points
                  axis_animal0, e[1],
                  -20,  # angle of invisible axis for target control points
                  stroke_width=0.3,
                  stroke_opacity=0.3,
                  stroke='purple')
        edges += 1
    elif ((e[1] in axis_carnic1.nodes) and (e[0] in axis_animal0.nodes)):
        h.connect(axis_carnic1, e[1],
                  20,  # angle of invisible axis for source control points
                  axis_animal0, e[0],
                  -20,  # angle of invisible axis for target control points
                  stroke_width=0.3,
                  stroke_opacity=0.3,
                  stroke='purple')
        edges += 1

    elif ((e[0] in axis_animal1.nodes) and (e[1] in axis_vegan0.nodes)):
        h.connect(axis_animal1, e[0],
                  35,  # angle of invisible axis for source control points
                  axis_vegan0, e[1],
                  -35,  # angle of invisible axis for target control points
                  stroke_width=0.3,  # pass any SVG attributes to an edge
                  stroke_opacity=0.3,
                  stroke='darkkhaki')
        edges += 1
    elif ((e[1] in axis_animal1.nodes) and (e[0] in axis_vegan0.nodes)):
        h.connect(axis_animal1, e[1],
                  35,  # angle of invisible axis for source control points
                  axis_vegan0, e[0],
                  -35,  # angle of invisible axis for target control points
                  stroke_width=0.3,  # pass any SVG attributes to an edge
                  stroke_opacity=0.3,
                  stroke='darkkhaki')
        edges += 1


h.save()
