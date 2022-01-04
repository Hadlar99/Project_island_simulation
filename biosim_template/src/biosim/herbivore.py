import math as m


class Herbivore:


    def __init__(self, w_birth, a_half, w_half, phi_weight, phi_age, beta, eta):
        self.age = 0
        self.weight = w_birth
        self.a_half = a_half
        self. w_half = w_half
        self.phi_weight = phi_weight
        self.phi_age = phi_age
        self.beta = beta
        self.eta = eta


    def year(self, F):
        self.age += 1
        self.weight = F*self.beta - self.weight*self.eta
        self.fitness = 1/(1 + m.exp(self.phi_age(self.age-self.a_half))) * 1/(1 + m.exp(self.phi_weight(self.w_half-self.weight))) if self.weight>0 else 0

