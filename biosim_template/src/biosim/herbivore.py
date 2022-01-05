import math as m


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





    def __init__(self):
        self.age = 0
        self.weight = w_birth
        self.fitness = 1/(1 + m.exp(phi_age(self.age-a_half))) * 1/(1 + m.exp(phi_weight(w_half-self.weight))) if self.weight>0 else 0



    def year(self, F):
        self.age += 1
        self.weight = F*beta - self.weight*eta
        self.fitness = 1/(1 + m.exp(phi_age(self.age-a_half))) * 1/(1 + m.exp(phi_weight(w_half-self.weight))) if self.weight>0 else 0

