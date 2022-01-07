from .Animal import Herbivore
from .Landscape import Lowland, Highland, Water, Dessert

class Island:

    def __init__(self, island_map, ini_herbs):
        self.map = {}
        for i, row in enumerate(island_map.splitlines()):
            for j, landscape in enumerate(row):
                if landscape == 'W':
                    self.map[(i+1, j+1)] = Water()
                if landscape == 'L':
                    self.map[(i+1, j+1)] = Lowland()
                if landscape == 'H':
                    self.map[(i+1, j+1)] = Highland()
                if landscape == 'D':
                    self.map[(i+1, j+1)] = Dessert()
        self.loc_start = ini_herbs[0]['loc']
        self.pop = ini_herbs[0]['pop']
        self.map[self.loc_start].pop_herbivores(self.pop)

    def season(self):
        for cell in self.map.values():
            if type(cell) is not Water:
                cell.feeding()
                cell.reproduction()
                cell.aging()
                cell.loss_of_weight()
                cell.pop_reduction()

    def amount_of_herbivores(self):
        return sum(cell.num_herbivores() for cell in self.map.values())






