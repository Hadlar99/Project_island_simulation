import math as m
import random


class Herbivore:

    w_birth = 8.0
    sigma_birth = 1.5
    beta = 0.9
    eta = 0.05
    a_half = 40.0
    phi_age = 0.6
    w_half = 10.0
    phi_weight = 0.1
    mu = 0.25
    gamma = 0.2
    zeta = 3.5
    xi = 1.2
    omega = 0.4
    F = 10.0

    default_params = {'w_birth': w_birth,
                    'sigma_birth': sigma_birth,
                    'beta': beta,
                    'eta': eta,
                    'a_half': a_half,
                    'phi_age': phi_age,
                    'w_half': w_half,
                    'phi_weight': phi_weight,
                    'mu': mu,
                    'gamma': gamma,
                    'zeta': zeta,
                    'xi': xi,
                    'omega': omega,
                    'F': F}



    @classmethod
    def set_params(cls, params):

        pass




    def __init__(self, weight):
        self.age = 0
        self.weight = weight
        self.fitness = 1/(1 + m.exp(self.phi_age(self.age-self.a_half))) * 1/(1 + m.exp(self.phi_weight(self.w_half-self.weight))) if self.weight>0 else 0



    def year(self, F):
        self.age += 1
        self.weight = F*self.beta - self.weight*self.eta
        self.fitness = 1/(1 + m.exp(self.phi_age(self.age-self.a_half))) * 1/(1 + m.exp(self.phi_weight(self.w_half-self.weight))) if self.weight>0 else 0

    def birth(self, N):
        if self.weight < self.zeta * (self.w_birth + self.sigma_birth):
            return False
        elif random.uniform(0, 1) < min(1, self.gamma*self.fitness*(N-1)):
            weight_baby = random.gauss(self.w_birth, self.sigma_birth)
            self.weight -= self.xi * weight_baby
            return weight_baby
        else:
            return False

    def death(self):
        if self.weight == 0:
            return True
        elif random.uniform(0,1) < self.omega *(1-self.fitness):
            return True
        else:
            return False