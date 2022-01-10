from .landscape import Lowland, Highland, Water, Dessert

"""Class for the island"""

class Island:

    def __init__(self, island_map, ini_animals=None):
        self.map = {}
        map_lines = island_map.splitlines()
        len_first_line = len(map_lines[0].strip())

        'Checks if the boundaries are all water and if the lines in the landscape are equal length'
        for landscape in map_lines[0] + map_lines[-1]:
            if landscape != 'W':
                raise ValueError('Boundary must be W')
        for row in map_lines:
            if len(row) != len_first_line:
                raise ValueError('All lines must have the same length')
            if row[0] != 'W' or row[-1] != 'W':
                raise ValueError('Boundary must be W')

        """Place the different landscape in the right places, also raises error if wrong type of landscape"""
        for i, row in enumerate(island_map.splitlines()):
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
        self.year = 0 #reset the year
        """Import the animals"""
        if ini_animals:
            self.new_animals(ini_animals)

    def season(self):
        """Everything that happens each year in correct order"""
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
        """Count how many herbivores it is"""
        return sum(cell.num_herbivores() for cell in self.map.values())

    def amount_of_carnivores(self):
        """Count how many carnivores it is"""
        return sum(cell.num_carnivores() for cell in self.map.values())

    def new_animals(self, ini_pop):
        """Takes in a dictonary with the location and what kind of species and put it on the island """
        loc_start = ini_pop[0]['loc']
        pop = ini_pop[0]['pop']
        self.map[loc_start].pop_animals(pop)
