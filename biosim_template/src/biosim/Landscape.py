from .herbivore import Herbivore


class lowland:

    def __init__(self, F_herbivores, herbivores=None, carnivores= None):
        self.fodder = 800
        self.herbivores = herbivores if herbivores is not None else []
        self.herbivores = sorted(self.herbivores, key=lambda x: x.fitness, reverse=True)
        self.carnivores = carnivores if carnivores is not None else []
        self.F_herbivores = F_herbivores

    def num_herbivores(self):

        return len(self.herbivores)

    def num_carnivores(self):

        return len(self.carnivores)


    def feeding(self):
        for herbi in self.herbivores:
            if self.fodder >= self.F_herbivores:
                self.fodder -= self.F_herbivores
                herbi.year(self.F_herbivores)
            else:
                herbi.year(self.fooder)
                self.fooder = 0

    def reproduction(self):
        N = len(self.herbivores)
        babies = [Herbivore(bw) for herbi in self.herbivores if (bw := herbi.birth(N))]
        self.herbivores.extend(babies)


    def pop_reduction(self):
        alive = [herbi for herbi in self.herbivores if not herbi.death()]

        self.herbivores = alive


