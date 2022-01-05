class lowland:

    def __init__(self, herbivores=None, carnivores= None):
        self.fodder = 800
        self.herbivores = herbivores if herbivores is not None else []
        self.herbivores = sorted(self.herbivores, key=lambda x: x.fitness, reverse=True)
        self.carnivores = carnivores if carnivores is not None else []

    def feeding(self):
        for herbi in self.herbivores:
            if self.fodder >= 10:
                self.fodder -= 10
                herbi.year(10)
            else:
                herbi.year(self.fooder)
                self.fooder = 0

