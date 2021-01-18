import pick_rand
import csv


class CascadingTables(object):

    def __init__(self, start_table_name, tables):
        self._start_table_name = start_table_name
        self._tables = {}
        for tab in tables:
            self._tables[tab.get_name()] = tab

    def start_table(self):
        return self._start_table_name

    def get_table(self, name):
        if not self.table_exists(name):
            raise Exception("Table with name {0} not defined, but was requested.  Please Create a table with that name.".format(name))
        return self._tables[name]

    def table_exists(self, name):
        return name in self._tables


def read(filename):
    start_name = None
    tables = []
    with open(filename, newline='') as csvfile:
        genreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        name = None
        values = []
        weights = []
        next_gens = []
        for row in genreader:
            if not row:
                gen_table = {}
                gen_table['options'] = values.copy()
                gen_table['weights'] = weights.copy()
                gen_table['next_gens'] = next_gens.copy()
                generator = pick_rand.FollowOnGeneration(name, gen_table)
                tables.append(generator)
                if not start_name:
                    start_name = name
                name = None
                values = []
                weights = []
                next_gens = []
            else:
                if(len(row) == 1 and not name):
                    name = row[0]
                else:
                    values.append(row.pop(0))
                    # if empty now, weight is 1, no follow-on
                    if not row:
                        weights.append(1)
                        next_gens.append([])
                    # otherwise, not empty, next value is weight (which might still be empty)
                    else:
                        weight = row.pop(0)
                        if not weight:
                            weight = 1
                        weights.append(int(weight))
                    # what's left, which might be empty, is the follow-on generators
                    gens = []
                    for gen in row:
                        if gen:
                            gens.append(gen)
                    next_gens.append(gens)
    if name:
        # we didn't have any newlines at the end, so, make a table
        gen_table = {}
        gen_table['options'] = values.copy()
        gen_table['weights'] = weights.copy()
        gen_table['next_gens'] = next_gens.copy()
        generator = pick_rand.FollowOnGeneration(name, gen_table)
        tables.append(generator)
    return CascadingTables(start_name, tables)
