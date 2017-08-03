from pony.orm import db_session, Database, Required, Json

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
