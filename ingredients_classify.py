import curses
from pony.orm import *

db = Database()


class Ingredient(db.Entity):
    name = Required(str)
    tags = Required(Json)


db.bind('sqlite', 'data/ingredients.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


class Tagger:

    def __init__(self, stdscr):
        self.screen = stdscr
        self.current_ingredient = 0
        self.next_ingredient()

    @db_session
    def next_ingredient(self):
        if self.current_ingredient + 1 <= select(i for i in Ingredient).count():
            self.current_ingredient += 1
            self.ingredient = Ingredient[self.current_ingredient].name
            self.tags = Ingredient[self.current_ingredient].tags

    @db_session
    def prev_ingredient(self):
        if self.current_ingredient > 1:
            self.current_ingredient -= 1
            self.ingredient = Ingredient[self.current_ingredient].name
            self.tags = Ingredient[self.current_ingredient].tags

    @db_session
    def update_ingredient(self):
        self.ingredient = Ingredient[self.current_ingredient].name
        self.tags = Ingredient[self.current_ingredient].tags

    @db_session
    def toggle_tag(self, tag):
        if tag in Ingredient[self.current_ingredient].tags:
            i = Ingredient[self.current_ingredient].tags.index(tag)
            Ingredient[self.current_ingredient].tags.pop(i)
        else:
            Ingredient[self.current_ingredient].tags.append(tag)

    def render(self):
        self.screen.clear()

        self.screen.addstr(1, 1,
                           '[n]ext [p]revious ' +
                           '[v]egan [c]arnic ' +
                           '[a]nimal origin',
                           curses.color_pair(1))

        self.screen.addstr(2, 1,
                           "%s: %s" % (str(self.current_ingredient), self.ingredient),
                           curses.color_pair(2))

        self.screen.addstr(3, 1,
                           str(self.tags),
                           curses.color_pair(2))

        self.screen.refresh()


def main(stdscr):
    # initialize curses environment
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)

    t = Tagger(stdscr)

    while True:

        t.render()

        c = stdscr.getch()

        if c == ord('n'):
            t.next_ingredient()

        elif c == ord('p'):
            t.prev_ingredient()
            t.screen.clear()

        elif c == ord('c'):
            t.toggle_tag('carnic')
            t.next_ingredient()

        elif c == ord('v'):
            t.toggle_tag('vegan')
            t.next_ingredient()

        elif c == ord('a'):
            t.toggle_tag('animal origin')
            t.next_ingredient()

        elif c == ord('q'):
            break  # Exit the while()


curses.wrapper(main)
