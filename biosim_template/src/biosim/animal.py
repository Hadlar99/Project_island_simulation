import math as m
import random
from numba import jit

"""This is a class for a single Herbivore"""


class Animal:

    params = {}

    @classmethod
    def set_params(cls, given_params):
        """

        Parameters
        ----------
        given_params: dict
            parameter name as key and parameter value as value

        changes the parameters for Animal
        """
        for key in given_params:
            if key not in cls.params:
                raise KeyError(f'Invalid parameter name: {key}')

        for key in given_params:
            cls.params[key] = given_params[key]

    def __init__(self, age=0, weight=None):
        """

        Parameters
        ----------
        age: int
            set to 0 if not anything else is given
        weight: float
            will be given a weight when born
        """
        self.age = age
        self.weight = weight if weight is not None else random.gauss(self.params['w_birth'], self.params['sigma_birth'])
        self.fitness = 0
        self.update_fitness()

    def add_weight(self, food):
        """
        Give weight to the herbivore when it eats
        Parameters
        ----------
        food: int
            how much the animal eats

        Returns the new weight of the animal
        -------

        """
        self.weight += food * self.params['beta']
        self.update_fitness()

    def aging_and_lose_weight(self):
        """Add one year to the age and reduce the weight of the herbivore"""
        self.age += 1
        self.weight -= self.weight * self.params['eta']
        self.update_fitness()

    def update_fitness(self):

        """
        Decide how fit the herbivore are

        Returns float between 1 and 0
        -------

        """
        if self.weight <= 0:    # if the herbivore weight is less than 0 it cannot get any fitness
            self.fitness = 0
        else:
            self.fitness = 1 / (1 + m.exp(self.params['phi_age'] * (self.age - self.params['a_half']))) * \
               1 / (1 + m.exp(self.params['phi_weight'] * (self.params['w_half'] - self.weight)))

    def migrate(self):
        """
        Tests if an animal will move or not
        Returns
        -------
        True if the animal will move, otherwise it returns False
        """
        return random.random() < self.params['mu'] * self.fitness

    def birth(self, num):
        """

        Parameters
        ----------
        :num int
            How many herbivors that is present

        Returns the weight of the new baby
        -------

        """
        if self.weight < self.params['zeta'] * (self.params['w_birth'] + self.params['sigma_birth']):
            return False    # if the mother weighs too little, no birth
        elif random.random() < min(1, self.params['gamma']*self.fitness*(num-1)):
            weight_baby = random.gauss(self.params['w_birth'], self.params['sigma_birth'])
            # gives a weight to baby if birth
            if weight_baby > self.weight:
                return False  # if the baby is going to weigh more than the parent, no birth
            if weight_baby <= 0:
                return False  # baby not born if it weight is less or equal to 0
            self.weight -= self.params['xi'] * weight_baby  # reduce weight of parent when given birth
            self.update_fitness()
            return weight_baby
        else:
            return False

    def death(self):
        """Sets conditions for an animal to die"""
        if self.weight == 0:
            return True     # if the weight is 0 it's going to die
        elif random.random() < self.params['omega'] * (1-self.fitness):
            return True     # if less fit, more likely to die
        else:
            return False       # if not dead, it's going to live


class Herbivore(Animal):
    """Given parameters for herbivores that works with the code"""

    params = {'w_birth': 8.0,
              'sigma_birth': 1.5,
              'beta': 0.9,
              'eta': 0.05,
              'a_half': 40.0,
              'phi_age': 0.6,
              'w_half': 10.0,
              'phi_weight': 0.1,
              'mu': 0.25,
              'gamma': 0.2,
              'zeta': 3.5,
              'xi': 1.2,
              'omega': 0.4,
              'F': 10.0}

    """Method to change parameter when given a dictionary with same keys"""


class Carnivore(Animal):
    """Given parameters for carnivores that works with the code"""

    params = {'w_birth': 6.0,
              'sigma_birth': 1.0,
              'beta': 0.75,
              'eta': 0.125,
              'a_half': 40.0,
              'phi_age': 0.3,
              'w_half': 4.0,
              'phi_weight': 0.4,
              'mu': 0.4,
              'gamma': 0.8,
              'zeta': 3.5,
              'xi': 1.1,
              'omega': 0.8,
              'F': 50.0,
              'DeltaPhiMax': 10.0}

    """Method to change parameter when given a dictionary with same keys"""
