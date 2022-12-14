import random

from .animal import Herbivore, Carnivore


class Landscape:
    """Super Class for the Landscape"""
    @classmethod
    def food_params(cls, param):
        """

        Parameters
        ----------
        param: dict
            Dictionary with parameter to change

        Raises
        ------
        KeyError

        """
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
        Sets animals on the Island
        Parameters
        ----------
        pop : list With Herbivore or Carnivore

        Raises
        ------
        ValueError
        """
        for animal in pop:
            if animal['species'] == 'Herbivore':
                self.herbivores.append(Herbivore(animal['age'], animal['weight']))
            elif animal['species'] == 'Carnivore':
                self.carnivores.append(Carnivore(animal['age'], animal['weight']))

            else:       # Raises ValueError if the species are not Herbivore or Carnivore
                raise ValueError(f"Species must be Herbivore or Carnivore, not {animal['species']}")

    def num_herbivores(self):
        """Finds the number of herbivores"""
        return len(self.herbivores)

    def num_carnivores(self):
        """Finds the number of carnivores"""
        return len(self.carnivores)

    def feeding(self):
        """Feeds the herbivores in the landscape"""
        self.fodder = self.f_max
        self.herbivores = sorted(self.herbivores, key=lambda x: x.fitness, reverse=True)  # Sort herbivores by fitness
        for herbi in self.herbivores:

            if self.fodder >= herbi.params['F']:
                self.fodder -= herbi.params['F']
                herbi.add_weight(herbi.params['F'])

            elif self.fodder == 0:  # The herbivores dont get food, because there are no food left
                break

            else:  # If there are less food then a herbivore can eat
                herbi.add_weight(self.fodder)  # the herbivore get the rest of the food
                self.fodder = 0
                break

    def carnivore_feeding(self):
        """Feeds the carnivores if there are any herbivores"""
        self.herbivores = sorted(self.herbivores, key=lambda x: x.fitness)
        random.shuffle(self.carnivores)

        for carni in self.carnivores:
            alive_herbivores = self.herbivores
            hunger = carni.params['F']      # How much the carnivore can eat

            for herbi in alive_herbivores:
                # Checks if the carnivore catch the herbivore
                if (carni.fitness - herbi.fitness)/carni.params['DeltaPhiMax'] > random.random():

                    # If herbivore weights more than what a carnivore can eat, the carnivore eats what it can
                    if herbi.weight >= hunger:
                        carni.add_weight(hunger)
                        self.herbivores.remove(herbi)
                        break

                    # The carnivore eats the herbivore
                    else:
                        hunger -= herbi.weight
                        carni.add_weight(herbi.weight)
                        self.herbivores.remove(herbi)

    def reproduction(self):
        """Checks hoe many new babies there are and add them to the landscape"""

        self.herbivores.extend([Herbivore(0, bw) for herbi in self.herbivores
                                if (bw := herbi.birth(self.num_herbivores())) > 0])
        # Adds the new babies to the list of herbivores
        self.carnivores.extend([Carnivore(0, bw) for carni in self.carnivores
                                if (bw := carni.birth(self.num_carnivores())) > 0])
        # Adds the new babies to the list of carnivores

    def aging_animals(self):
        """Makes all the animals one year older"""
        for herbi in self.herbivores:
            herbi.aging()
        for carni in self.carnivores:
            carni.aging()

    def weight_loss(self):
        """Makes all the animals loss the yearly weight"""
        for herbi in self.herbivores:
            herbi.lose_weight()
        for carni in self.carnivores:
            carni.lose_weight()

    def pop_reduction(self):
        """Removes all animals that dies"""
        alive_herbi = [herbi for herbi in self.herbivores if not herbi.death()]
        self.herbivores = alive_herbi

        alive_carni = [carni for carni in self.carnivores if not carni.death()]
        self.carnivores = alive_carni

    def migration(self):
        """
        Sorts the animal that are going to migrate and those who will stand still
        Returns
        -------
        Two list all the animals that are going to migrate
        """
        moving_herbivores = []      # list of herbivores emigrating
        stationary_herbivores = []      # list of herbivores not emigrating
        for herbi in self.herbivores:  # The herbivores are getting sorted
            if herbi.migrate():
                moving_herbivores.append(herbi)
            else:
                stationary_herbivores.append(herbi)

        moving_carnivores = []      # list of carnivores emigrating
        stationary_carnivores = []      # list of carnivores not emigrating
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
        """Retrieving the age of herbivores and put it in a list"""
        return [animal.age for animal in self.herbivores]

    def list_carnivores_ages(self):
        """Retrieving the age of carnivores and put it in a list"""
        return [animal.age for animal in self.carnivores]

    def list_herbivores_weight(self):
        """Retrieving the weight of herbivores and put it in a list"""
        return [animal.weight for animal in self.herbivores]

    def list_carnivores_weight(self):
        """Retrieving the weight of carnivores and put it in a list"""
        return [animal.weight for animal in self.carnivores]

    def list_herbivores_fitness(self):
        """Retrieving the fitness of herbivores and put it in a list"""
        return [animal.fitness for animal in self.herbivores]

    def list_carnivores_fitness(self):
        """Retrieving the fitness of carnivores and put it in a list"""
        return [animal.fitness for animal in self.carnivores]


class Water(Landscape):
    """Water without food and animals and is not possible to move to"""
    default_f_max = 0
    f_max = default_f_max
    move = False


class Lowland(Landscape):
    """Lowland with food, animals and the possibility to move to"""
    default_f_max = 800
    f_max = default_f_max
    move = True


class Highland(Landscape):
    """Highland with food, animals and the possibility to move to"""
    default_f_max = 300
    f_max = default_f_max
    move = True


class Dessert(Landscape):
    """Dessert with food, animals and the possibility to move to"""
    default_f_max = 0
    f_max = default_f_max
    move = True
