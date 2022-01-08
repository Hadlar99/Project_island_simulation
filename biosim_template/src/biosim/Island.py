from .Animal import Herbivore
from .Landscape import Lowland, Highland, Water, Dessert

class Island:

    def __init__(self, island_map, ini_animals=None):
        self.map = {}
        map_lines = island_map.splitlines()
        first_line = len(map_lines[0])
        for i, row in enumerate(island_map.splitlines()):
            if len(row) != first_line:
                raise ValueError('All lines must have the same length')
            for j, landscape in enumerate(row):
                if landscape == 'W':
                    self.map[(i+1, j+1)] = Water()
                elif landscape == 'L':
                    self.map[(i+1, j+1)] = Lowland()
                elif landscape == 'H':
                    self.map[(i+1, j+1)] = Highland()
                elif landscape == 'D':
                    self.map[(i+1, j+1)] = Dessert()
                else:
                    raise ValueError(f'Landscape has to be W, L, H, D, can not be {landscape}')
        self.year = 0
        if ini_animals:
            self.new_animals(ini_animals)

    def season(self):
        for cell in self.map.values():
            if type(cell) is not Water:
                cell.feeding()
                cell.carnivore_feeding()
                cell.reproduction()
                cell.aging()
                cell.loss_of_weight()
                cell.pop_reduction()
        self.year += 1

    def amount_of_herbivores(self):
        return sum(cell.num_herbivores() for cell in self.map.values())

    def amount_of_carnivores(self):
        return sum(cell.num_carnivores() for cell in self.map.values())

    def new_animals(self, ini_pop):
        loc_start = ini_pop[0]['loc']
        pop = ini_pop[0]['pop']
        self.map[loc_start].pop_animals(pop)




