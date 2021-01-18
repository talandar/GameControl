import random


class Picker(object):

    def __init__(self, options, weights):
        if weights is None:
            weights = [1]*len(options)
        if(len(weights) != len(options)):
            print("different num arguments, weights has {0} values, options has {1} options".format(len(weights), len(options)))
            raise RuntimeError("invalid arguments to Picker")
        self._options = options
        self._weights = weights
        self._total_weights = sum(weights)
        self._cumulative_weights = [weights[0]]
        for x in range(1, len(weights)):
            self._cumulative_weights.append(self._cumulative_weights[x-1] + weights[x])

    def choose(self):
        pick = random.randrange(0, self._total_weights)
        index = 0
        while pick >= self._cumulative_weights[index]:
            index += 1
        return self._options[index]


class FollowOnGeneration(object):
    def __init__(self, name, generation_table):
        self._randomizer = Picker(generation_table['options'], generation_table['weights'])
        # is it this simple?  nested dictionary of result->list of follow-ons
        self._next_gen_map = dict(zip(generation_table['options'], generation_table['next_gens']))
        self._name = name
        if False:  # Debug Print Tables
            print()
            print("Generated Table with name: ", name, "Total weight: ", self._randomizer._total_weights)
            print("option, relative weight, percent chance, follow-ons")
            for i in range(len(generation_table['options'])):
                print("{0}, {1}, {2}, {3}".format(
                    generation_table['options'][i],
                    generation_table['weights'][i],
                    generation_table['weights'][i]/self._randomizer._total_weights * 100,
                    generation_table['next_gens'][i]))

    def get_name(self):
        return self._name

    def randomize(self, override=None):
        if override is None:
            generated = self._randomizer.choose()
        else:
            generated = override
        return generated, self._next_gen_map.get(generated, None)


def main():
    picker = Picker(["a", 'b', 'c', 'd'], [1, 2, 3, 1])
    for _ in range(20):
        picker.choose()


if __name__ == '__main__':
    main()
