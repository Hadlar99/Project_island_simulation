import random

from .landscape import Lowland, Highland, Water, Dessert

"""Class for the island"""


class Island:

    def __init__(self, island_map, ini_animals=None):
        self.map = {}
        map_lines = island_map.splitlines()
        self.height = len(map_lines)
        self.length = len(map_lines[0].strip())

        'Checks if the boundaries are all water and if the lines in the landscape are equal length'
        for landscape in map_lines[0] + map_lines[-1]:
            if landscape != 'W':
                raise ValueError('Boundary must be W')
        for row in map_lines:
            if len(row) != self.length:
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
        self.year = 0   # set the start year to 0
        """Import the animals"""
        if ini_animals:
            self.new_animals(ini_animals)

    def migrate_season(self):
        """Moves animals from one cell to another"""
        for loc, cell in self.map.items():
            move_to = [(loc[0]-1, loc[1]), (loc[0], loc[1]-1), (loc[0]+1, loc[1]), (loc[0], loc[1]+1)]
            # The cells Animals can move to
            herbivores, carnivores = cell.migration()   # gets the animals that are emigrating

            for herbi in herbivores:
                if (new_cell := self.map[random.choice(move_to)]).move:     # Checks if the animal can move to that cell
                    new_cell.immigrating_herbivores.append(herbi)
                else:
                    cell.immigrating_herbivores.append(herbi)

            for carni in carnivores:
                if (new_cell := self.map[random.choice(move_to)]).move:
                    new_cell.immigrating_carnivores.append(carni)
                else:
                    cell.immigrating_carnivores.append(carni)
        for cell in self.map.values():
            cell.immigration()      # Immigrate the immigrating animals in each cell

    def season(self):
        """Everything that happens each year in correct order"""
        for cell in self.map.values():
            cell.feeding()
            cell.carnivore_feeding()
            cell.reproduction()
        self.migrate_season()
        for cell in self.map.values():
            cell.aging_and_loss_of_weight()
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
        for animals in ini_pop:
            loc_start = animals['loc']
            pop = animals['pop']
            self.map[loc_start].pop_animals(pop)

    def herbivore_map(self):
        return [[self.map[(j, i)].num_herbivores() for i in range(1, self.length+1)] for j in range(1, self.height+1)]

    def carnivore_map(self):
        return [[self.map[(j, i)].num_carnivores() for i in range(1, self.length+1)] for j in range(1, self.height+1)]

    def herbivore_ages(self):
        herbi_ages = []
        for cell in self.map.values():
            herbi_ages.extend(cell.list_herbivores_ages())
        return herbi_ages

    def carnivore_ages(self):
        carni_ages = []
        for cell in self.map.values():
            carni_ages.extend(cell.list_carnivores_ages())
        return carni_ages

    def herbivore_weights(self):
        herbi_weights = []
        for cell in self.map.values():
            herbi_weights.extend(cell.list_herbivores_weight())
        return herbi_weights

    def carnivore_weights(self):
        carni_weights = []
        for cell in self.map.values():
            carni_weights.extend(cell.list_carnivores_weight())
        return carni_weights

    def herbivore_fitness(self):
        herbi_fitness = []
        for cell in self.map.values():
            herbi_fitness.extend(cell.list_herbivores_fitness())
        return herbi_fitness

    def carnivore_fitness(self):
        carni_fitness = []
        for cell in self.map.values():
            carni_fitness.extend(cell.list_carnivores_fitness())
        return carni_fitness
