import math as m
import random


class Herbivore:


    params = {'w_birth' : 8.0,
        'sigma_birth' : 1.5,
        'beta' : 0.9,
        'eta' : 0.05,
        'a_half' : 40.0,
        'phi_age' : 0.6,
        'w_half' : 10.0,
        'phi_weight' : 0.1,
        'mu' : 0.25,
        'gamma' : 0.2,
        'zeta' : 3.5,
        'xi' : 1.2,
        'omega' : 0.4,
        'F' : 10.0}



    @classmethod
    def set_params(cls, given_params):
        for key in given_params:
            if key not in cls.params:
                raise KeyError(f'Invalid parameter name: {key}')

        for key in given_params():
            cls.params[key] = given_params[key]





    def __init__(self, weight):
        self.age = 0
        self.weight = weight
        #self.fitness = 1/(1 + m.exp(self.params['phi_age'](self.age-self.params['a_half']))) * 1/(1 + m.exp(self.params['phi_weight'](self.params['w_half']-self.weight))) if self.weight>0 else 0



    def year(self):
        self.age += 1



    def weight(self, Food):
        self.weight = Food * self.params['beta'] - self.weight * self.params['eta']



    def fitness(self):
        self.fitness = 1 / (1 + m.exp(self.params['phi_age'](self.age - self.params['a_half']))) * 1 / (
                    1 + m.exp(self.params['phi_weight'](self.params['w_half'] - self.weight))) if self.weight > 0 else 0



    def birth(self, N):
        if self.weight < self.params['zeta'] * (self.params['w_birth'] + self.params['sigma_birth']):
            return False
        elif random.uniform(0, 1) < min(1, self.params['gamma']*self.fitness*(N-1)):
            weight_baby = random.gauss(self.params['w_birth'], self.params['sigma_birth'])
            self.weight -= self.params['xi'] * weight_baby
            return weight_baby
        else:
            return False

    def death(self):
        if self.weight == 0:
            return True
        elif random.uniform(0,1) < self.params['omega'] *(1-self.fitness):
            return True
        else:
            return False