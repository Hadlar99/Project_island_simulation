from .herbivore import Herbivore


class lowland:

    def __init__(self, herbivores=None, carnivores= None):
        self.fodder = 800
        self.herbivores = herbivores if herbivores is not None else []
        self.herbivores = sorted(self.herbivores, key=lambda x: x.fitness, reverse=True)
        self.carnivores = carnivores if carnivores is not None else []

    def num_herbivores(self):

        return len(self.herbivores)

    def num_carnivores(self):

        return len(self.carnivores)

    def feeding(self):
        for herbi in self.herbivores:
            if self.fodder >= herbi.params['F']:
                self.fodder -= herbi.params['F']
                herbi.add_weigth(herbi.params['F'])
            elif self.fooder == 0:
                pass
            else:
                herbi.add_weigth(self.fooder)
                self.fooder = 0

    def reproduction(self):
        N = len(self.herbivores)
        babies = [Herbivore(bw) for herbi in self.herbivores if (bw := herbi.birth(N))]
        self.herbivores.extend(babies)

    def aging(self):
        for herbi in self.herbivores:
            herbi.year()

    def loss_of_weight(self):
        for herbi in self.herbivores:
            herbi.lose_weight()

    def pop_reduction(self):
        alive = [herbi for herbi in self.herbivores if not herbi.death()]

        self.herbivores = alive


