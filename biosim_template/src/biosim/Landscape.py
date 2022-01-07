from .herbivore import Herbivore

'''lowland Class for'''


class Landscape:

    def num_herbivores(self):
        """Finds the number of herbivores"""
        return len(self.herbivores)

    def num_carnivores(self):
        """Finds the number of carnivores"""
        return len(self.carnivores)

    def feeding(self):
        """Feeds the herbivores in the landscape"""
        self.herbivores = sorted(self.herbivores, key=lambda x: x.fitness(), reverse=True)  # Sort herbivores by fitness
        for herbi in self.herbivores:
            if self.fodder >= herbi.params['F']:
                self.fodder -= herbi.params['F']
                herbi.add_weight(herbi.params['F'])
            elif self.fodder == 0:  # The herbivores dont get food, because there are no food left
                break
            else:  # If there are less food then a herbivore can eat
                herbi.add_weight(self.fodder)  # the herbivore get the rest of the food
                self.fodder = 0


    def reproduction(self):
        """Checks hoe many new babies there are and add them to the landscape"""
        N = len(self.herbivores)
        babies = [Herbivore(0, bw) for herbi in self.herbivores if (bw := herbi.birth(N)) > 0]
        self.herbivores.extend(babies)  # Adds the new babies to the list of herbivores


    def aging(self):
        """Makes all the animals one year older"""
        for herbi in self.herbivores:
            herbi.year()


    def loss_of_weight(self):
        """Removes the weight the animals loses in a year"""
        for herbi in self.herbivores:
            herbi.lose_weight()


    def pop_reduction(self):
        """Removes all animals that dies"""
        alive = [herbi for herbi in self.herbivores if not herbi.death()]

        self.herbivores = alive


class Water(Landscape):
    """Water without food and animals"""

    def __init__(self):
        self.fodder = 0  # How much food there are in the Water


class Lowland(Landscape):
    """Lowland with food and animals"""

    def __init__(self, herbivores=None, carnivores=None):
        self.herbivores = herbivores if herbivores is not None else []  # Empty list if no list are given
        self.carnivores = carnivores if carnivores is not None else []  # Empty list if no list are given
        self.fodder = 800       # How much food there are in the lowland


class Highland(Landscape):
    """Highland with food and animals"""

    def __init__(self, herbivores=None, carnivores=None):
        self.herbivores = herbivores if herbivores is not None else []  # Empty list if no list are given
        self.carnivores = carnivores if carnivores is not None else []  # Empty list if no list are given
        self.fodder = 0  # How much food there are in the Highland


class Dessert(Landscape):
    """Dessert animals and no food"""

    def __init__(self, herbivores=None, carnivores=None):
        self.herbivores = herbivores if herbivores is not None else []  # Empty list if no list are given
        self.carnivores = carnivores if carnivores is not None else []  # Empty list if no list are given
        self.fodder = 0  # How much food there are in the Dessert




