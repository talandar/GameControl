import table_reader
import re as regex
import os


class Generator(object):

    def __init__(self, values_location):
        values_files = []
        if os.path.isdir(values_location):
            for (_, _, filenames) in os.walk(values_location):
                values_files.extend(os.path.join(values_location,filename) for filename in filenames)
                break
            values_files = filter(lambda name: name.endswith("tbl"), values_files)
        elif os.path.isfile(values_location):
            values_files = [values_location]

        self._generators = table_reader.read(values_files)

        self._start_table = self._generators.start_table()

    def generate(self, overrides={}):
        if overrides is None:
            overrides = {}

        generator_queue = [self._start_table]
        generated = {}

        while generator_queue: 
            table = self._generators.get_table(generator_queue.pop())
            attr_name = attr_name = regex.sub("-.*$", '', table.get_name())
            value, next_gens = table.randomize(overrides.get(attr_name, None))
            if not value.startswith("_"):
                generated[attr_name] = value
            if next_gens:
                generator_queue.extend(next_gens)
            if self._generators.table_exists(value+'#'+attr_name):
                generator_queue.append(value+'#'+attr_name)

        print(generated)


def main():
    gen = Generator("/home/jim/share/npcgentables/")
    #  https://www.bryndonovan.com/2015/06/16/master-list-of-physical-descriptions/
    override = None
    override = {
        "Species": "Elf",
        # "Nationality": "Thellonde",
        # "Gender": "Androgenous or Agender"
    }
    for _ in range(20):
        gen.generate(override)

if __name__ == '__main__':
    main()
