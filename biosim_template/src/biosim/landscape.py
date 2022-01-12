import random

from .animal import Herbivore, Carnivore

'''Super Class for the Landscape'''


class Landscape:

    @classmethod
    def food_params(cls, param):
        for key, value in param.items():
            if key == 'f_max':
                cls.f_max = value
            else:
                raise KeyError(f'Invalid parameter name: {key}')

    def __init__(self, herbivores=None, carnivores=None):
        self.herbivores = herbivores if herbivores is not None else []  # Empty list if no list are given
        self.carnivores = carnivores if carnivores is not None else []  # Empty list if no list are given
        self.immigrating_herbivores = []    # Lists of animals immigrating
        self.immigrating_carnivores = []
        self.fodder = self.f_max    # How much food that is available

    def pop_animals(self, pop):
        """

        Parameters
        ----------
        pop : list With Herbivore or Carnivore

        """
        for animal in pop:
            if animal['species'] == 'Herbivore':
                self.herbivores.append(Herbivore(animal['age'], animal['weight']))
            elif animal['species'] == 'Carnivore':
                self.carnivores.append(Carnivore(animal['age'], animal['weight']))
            else:
                raise ValueError(f"species must be Herbivore or Carnivore, not {animal['species']}")

    def num_herbivores(self):
        """Finds the number of herbivores"""
        return len(self.herbivores)

    def num_carnivores(self):
        """Finds the number of carnivores"""
        return len(self.carnivores)

    def feeding(self):
        """Feeds the herbivores in the landscape"""
        self.fodder = self.f_max
        self.herbivores = sorted(self.herbivores, key=lambda x: x._fitness, reverse=True)  # Sort herbivores by fitness
        for herbi in self.herbivores:
            if self.fodder >= herbi.params['F']:
                self.fodder -= herbi.params['F']
                herbi.add_weight(herbi.params['F'])
            elif self.fodder == 0:  # The herbivores dont get food, because there are no food left
                break
            else:  # If there are less food then a herbivore can eat
                herbi.add_weight(self.fodder)  # the herbivore get the rest of the food
                self.fodder = 0

    def carnivore_feeding(self):
        """Feeds the carnivores if there are any herbivores"""
        self.herbivores = sorted(self.herbivores, key=lambda x: x._fitness)
        random.shuffle(self.carnivores)
        for carni in self.carnivores:
            alive_herbivores = self.herbivores
            hunger = carni.params['F']
            for herbi in alive_herbivores:
                if (carni._fitness - herbi._fitness)/carni.params['DeltaPhiMax'] > random.random():
                    if herbi._weight >= hunger:
                        carni.add_weight(hunger)
                        self.herbivores.remove(herbi)
                        break
                    else:
                        carni.add_weight(herbi._weight)
                        self.herbivores.remove(herbi)

    def reproduction(self):
        """Checks hoe many new babies there are and add them to the landscape"""

        self.herbivores.extend([Herbivore(0, bw) for herbi in self.herbivores
                                if (bw := herbi.birth(self.num_herbivores())) > 0])
        # Adds the new babies to the list of herbivores
        self.carnivores.extend([Carnivore(0, bw) for carni in self.carnivores
                                if (bw := carni.birth(self.num_carnivores())) > 0])
        # Adds the new babies to the list of carnivores

    def aging_and_loss_of_weight(self):
        """Makes all the animals one year older and removes the weight the animals loses in a year"""
        for herbi in self.herbivores:
            herbi.aging_and_lose_weight()
        for carni in self.carnivores:
            carni.aging_and_lose_weight()

    def pop_reduction(self):
        """Removes all animals that dies"""
        alive_herbi = [herbi for herbi in self.herbivores if not herbi.death()]
        self.herbivores = alive_herbi

        alive_carni = [carni for carni in self.carnivores if not carni.death()]
        self.carnivores = alive_carni

    def migration(self):
        """
        Sortes the animal that are going to migrate and those who will stand still
        Returns
        -------
        Two list all the animals that are going to migrate
        """
        moving_herbivores = []
        stationary_herbivores = []
        for herbi in self.herbivores:  # The herbivores are getting sorted
            if herbi.migrate():
                moving_herbivores.append(herbi)
            else:
                stationary_herbivores.append(herbi)
        moving_carnivores = []
        stationary_carnivores = []
        for carni in self.carnivores:   # The carnivores are getting sorted
            if carni.migrate():
                moving_carnivores.append(carni)
            else:
                stationary_carnivores.append(carni)
        self.herbivores = stationary_herbivores
        self.carnivores = stationary_carnivores
        return moving_herbivores, moving_carnivores

    def immigration(self):
        """The specific animals that er going immigrate """
        self.herbivores.extend(self.immigrating_herbivores)  # Adds all the new animals that are immigrating to the cell
        self.carnivores.extend(self.immigrating_carnivores)
        self.immigrating_herbivores = []  # Empties the list for next time the function is called upon
        self.immigrating_carnivores = []

    def list_herbivores_ages(self):
        return [animal._age for animal in self.herbivores]

    def list_carnivores_ages(self):
        return [animal._age for animal in self.carnivores]

    def list_herbivores_weight(self):
        return [animal._weight for animal in self.herbivores]

    def list_carnivores_weight(self):
        return [animal._weight for animal in self.carnivores]

    def list_herbivores_fitness(self):
        return [animal._fitness for animal in self.herbivores]

    def list_carnivores_fitness(self):
        return [animal._fitness for animal in self.carnivores]


class Water(Landscape):
    """Water without food and animals and is not possible to move to"""
    f_max = 0
    move = False


class Lowland(Landscape):
    """Lowland with food, animals and the possibility to move to"""
    f_max = 800
    move = True

class Highland(Landscape):
    """Highland with food, animals and the possibility to move to"""
    f_max = 300
    move = True


class Dessert(Landscape):
    """Dessert with food, animals and the possibility to move to"""
    f_max = 0
    move = True
