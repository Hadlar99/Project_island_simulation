import math as m


class herbavore:

    def __init__(self, w_birth, a_half, w_half, phi_weight, phi_age, beta, eta):
        self.age = 0
        self.weight = w_birth
        self.fitness = fitness

    def year(self, F):
        self.age += 1
        self.weight = F*beta - self.weight*eta
        self.fitness = 1/(1 + m.exp(phi_age(self.age-a_half))) * 1/(1 + m.exp(phi_weight(w_half-self.weight))) if self.weight>0 else 0

