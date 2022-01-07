from .herbivore import Herbivore
from .Landscape import Lowland

class Island:

    def __init__(self, island_map, list_loc_pop):
        self.map ={}
        for i, row in enumerate(island_map.splitlines()):
            for j, landscape in enumerate(row):
                if landscape == 'W':
                    self.map[(i, j)] = Water()
                if landscape == 'L':
                    self.map[(i, j)] = Lowland()
                if landscape == 'H':
                    self.map[(i, j)] = Highland()
                if landscape == 'D':
                    self.map[(i, j)] = Dessert()
        self.loc = list_loc_pop[0]['loc']
        self.pop = list_loc_pop[0]['pop']
        self.pop_herbivore = [Herbivore(animal['age'], animal['weight']) for animal in self.pop
                              if animal['species'] == 'Herbivore']

    def location(self):

