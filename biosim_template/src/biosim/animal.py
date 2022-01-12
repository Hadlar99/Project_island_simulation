import math as m
import random

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
        for key, value in given_params.items():

            # Returns KeyError if the key is not a parameter
            if key not in cls.params:
                raise KeyError(f'Invalid parameter name: {key}')

            # Returns ValueError if the value of a parameter is below 0
            if value < 0:       #
                raise ValueError(f'Value for {key} must be positive')

            # Returns ValueError if DeltaPhiMax is not strictly positive
            if key == 'DeltaPhiMax' and value <= 0:
                raise ValueError('Value for DeltaPhiMax must be strictly positive')

            # Returns ValueError if eta is higher than 1
            if key == 'eta' and value > 1:
                raise ValueError('Value for eta must be lower than 1')

        for key in given_params:
            cls.params[key] = given_params[key]     # Changes the parameters

    def __init__(self, age=0, weight=None):
        """

        Parameters
        ----------
        age: int
            set to 0 if not anything else is given
        weight: float
            will be given a weight when born
        """

        if weight is not None:

            # Raises ValueError if the weight of the animal is not strictly positive
            if weight <= 0:
                raise ValueError('Weight of the animal must be strictly positive')
        else:
            while weight is None or weight <= 0:    # weights of a new animal must be strictly positive
                weight = random.gauss(self.params['w_birth'], self.params['sigma_birth'])

        self._age = age
        self._weight = weight
        self._fitness = 0
        self.update_fitness()   # Makes fitness the right fitness from start

    @property
    def age(self):
        """
        Returns
        -------
        The age of the animal
        """
        return self._age

    @property
    def weight(self):
        """
        Returns
        -------
        The weight of the animal
        """
        return self._weight

    @property
    def fitness(self):
        """
        Returns
        -------
        The fitness of the animal
        """
        return self._fitness

    def add_weight(self, food):
        """
        Give weight to the herbivore when it eats
        Parameters
        ----------
        food: int
            how much the animal eats

        updates the weight of the animal when the animal eats

        """
        self._weight += food * self.params['beta']
        self.update_fitness()

    def aging_and_lose_weight(self):
        """Add one year to the age and reduce the weight of the herbivore"""
        self._age += 1
        self._weight -= self._weight * self.params['eta']
        self.update_fitness()

    def update_fitness(self):

        """
        Decide how fit the herbivore are

        It is called every time the weight or age

        """
        if self._weight <= 0:    # if the herbivore weight is less than 0 it cannot get any fitness
            self._fitness = 0
        else:
            self._fitness = 1 / (1 + m.exp(self.params['phi_age'] * (self._age - self.params['a_half']))) * \
                            1 / (1 + m.exp(self.params['phi_weight'] * (self.params['w_half'] - self._weight)))

    def migrate(self):
        """
        Tests if an animal will move or not
        Returns
        -------
        True if the animal will move, otherwise it returns False
        """
        return random.random() < self.params['mu'] * self._fitness

    def birth(self, num):
        """

        Parameters
        ----------
        :num int
            How many herbivors that is present

        Returns the weight of the new baby
        -------

        """
        if self._weight < self.params['zeta'] * (self.params['w_birth'] + self.params['sigma_birth']):
            return False    # if the mother weighs too little, no birth
        elif random.random() < min(1, self.params['gamma'] * self._fitness * (num - 1)):
            weight_baby = random.gauss(self.params['w_birth'], self.params['sigma_birth'])
            # gives a weight to baby if birth
            if weight_baby > self._weight:
                return False  # if the baby is going to weigh more than the parent, no birth
            if weight_baby <= 0:
                return False  # baby not born if it weight is less or equal to 0
            self._weight -= self.params['xi'] * weight_baby  # reduce weight of parent when given birth
            self.update_fitness()
            return weight_baby
        else:
            return False

    def death(self):
        """Sets conditions for an animal to die"""
        if self._weight == 0:
            return True     # if the weight is 0 it's going to die
        elif random.random() < self.params['omega'] * (1-self._fitness):
            return True     # if less fit, more likely to die
        else:
            return False       # if not dead, it's going to live


class Herbivore(Animal):
    """Given parameters for herbivores that works with the code"""

    default_params = {'w_birth': 8.0,
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

    params = default_params

    """Method to change parameter when given a dictionary with same keys"""


class Carnivore(Animal):
    """Given parameters for carnivores that works with the code"""

    default_params = {'w_birth': 6.0,
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

    params = default_params

    """Method to change parameter when given a dictionary with same keys"""
