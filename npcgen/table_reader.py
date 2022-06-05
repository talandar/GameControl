import pick_rand
import csv
import traceback


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




def read(filepaths):
    start_name = "BaseValues"
    found_basevalues = False
    tables = []
    for filename in filepaths:
        print(f"Parsing file {filename}...")
        try:
            with open(filename, newline='') as csvfile:
                file_tables = []
                genreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                name = None
                values = []
                weights = []
                next_gens = []
                for row in genreader:
                    if not row:
                        if name:
                            try:
                                gen_table = {}
                                gen_table['options'] = values.copy()
                                gen_table['weights'] = weights.copy()
                                gen_table['next_gens'] = next_gens.copy()
                                generator = pick_rand.FollowOnGeneration(name, gen_table)
                                file_tables.append(generator)
                            except Exception as e:
                                print(f"error building table with name {name}.  Skipping")
                            if name == start_name:
                                if found_basevalues:
                                    print(f"While building tables, found multiple tables called '{start_name}'.")
                                    print(f"Only one table should be called '{start_name}'.  Inconsistent behavior will result.")
                                found_basevalues = True
                            name = None
                            values = []
                            weights = []
                            next_gens = []
                    else:
                        if(len(row) == 1 and not name):
                            name = row[0]
                        else:
                            this_value = row.pop(0)
                            if this_value in values:
                                raise Exception(f"value {this_value} already present in generator values {values}.  Make sure all keys are unique.")
                            values.append(this_value)
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
                file_tables.append(generator)
            tables.extend(file_tables)
        except Exception as e:
            print(f"Error reading file {filename}.")
            print(e)
            traceback.print_exc()
            raise
    if not tables:
        raise Exception(f"No tables found in paths {filepaths}.")
    return CascadingTables(start_name, tables)
