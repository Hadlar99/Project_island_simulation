from .herbivore import Herbivore

class Island:

    def __init__(self, list_loc_pop):
        self.loc = list_loc_pop[0]['loc']
        self.pop = list_loc_pop[0]['pop']
        self.pop_herbivore = [Herbivore(animal['age'], animal['weight']) for animal in self.pop
                              if animal['species'] == 'Herbivore']

    def location(self):

