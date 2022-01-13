"""
Template for BioSim class.
"""
from .island import Island
from .animal import Herbivore
from .landscape import Dessert, Highland, Lowland, Water
from .map import mapping
import random
import matplotlib.pyplot as plt
from .graphics import Graphics
from mpl_toolkits.axes_grid1 import make_axes_locatable



# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU

class BioSim:
    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):

        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param vis_years: years between visualization updates (if 0, disable graphics)
        :param img_dir: String with path to directory for figures
        :param img_base: String with beginning of file name for figures
        :param img_fmt: String with file type for figures, e.g. 'png'
        :param img_years: years between visualizations saved to files (default: vis_years)
        :param log_file: If given, write animal counts to this file

        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.

        If img_dir is None, no figures are written to file. Filenames are formed as

            f'{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}'

        where img_number are consecutive image numbers starting from 0.

        img_dir and img_base must either be both None or both strings.
        """
        random.seed(seed)
        self.Island = Island(island_map, ini_pop)
        self.Island_map = island_map
        if cmax_animals is not None:

            for ani, num in cmax_animals.items():
                if ani == 'Herbivore':
                    self.cmax_herbivore = num
                elif ani == 'Carnivore':
                    self.cmax_carnivore = num
                else:
                    raise KeyError(f'Key in cmax_animals must be Herbivore or Carnivore, not {ani}')
        else:
            self.cmax_herbivore = None
            self.cmax_carnivore = None

        if hist_specs is not None:
            for ani, num in hist_specs.items():
                if ani == 'age':
                    self.hist_specs_age = num
                elif ani == 'fitness':
                    self.hist_specs_fitness = num
                elif ani == 'weight':
                    self.hist_specs_weight = num
                else:
                    raise KeyError(f'Key in hist_specs must be age, fitness or weight, not {ani}')
        else:
            self.hist_specs_age = None
            self.hist_specs_weight = None
            self.hist_specs_fitness = None

        self._graphics = Graphics(self.Island_map, img_fmt=img_fmt, ymax_animals=ymax_animals,
                                  cmax_herbi=self.cmax_herbivore, cmax_carni=self.cmax_carnivore,
                                  hist_specs_age=self.hist_specs_age, hist_specs_fitness=self.hist_specs_fitness,
                                  hist_specs_weight=self.hist_specs_weight)

        self._year = 0
        self._final_year = None

        self.vis_years = vis_years




    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == 'Herbivore':
            Herbivore.set_params(params)
        elif species == 'Carnivore':
            pass
        else:
            raise NameError('Species have to be Herbivore or Carnivore ')

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

        if landscape == 'L':
            Lowland.food_params(params)
        elif landscape == 'H':
            Highland.food_params(params)
        elif landscape == 'D':
            Dessert.food_params(params)
        else:
            raise NameError(f'Landscape has to be L, H or D')

    def simulate(self, num_years, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """

        if img_years is None:
            img_years = self.vis_years

        if img_years % self.vis_years != 0:
            raise ValueError('img_years must be multiple of vis_years')

        self._final_year = self._year + num_years
        self._graphics.setup(self._final_year, img_years)

        while self._year < self._final_year:
            self.Island.season()
            self._year += 1

            if self._year % self.vis_years == 0:
                self._graphics.update(self._year,
                                      self.Island.amount_of_herbivores(),
                                      self.Island.amount_of_carnivores(),
                                      self.Island.herbivore_map(),
                                      self.Island.carnivore_map(),
                                      self.Island.herbivore_ages(),
                                      self.Island.carnivore_ages(),
                                      self.Island.herbivore_weights(),
                                      self.Island.carnivore_weights(),
                                      self.Island.herbivore_fitness(),
                                      self.Island.carnivore_fitness())

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.Island.new_animals(population)

    @property
    def year(self):
        """Last year simulated."""
        return self._final_year
    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.Island.amount_of_herbivores() + self.Island.amount_of_carnivores()
    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return {'Herbivore': self.Island.amount_of_herbivores(), 'Carnivore': self.Island.amount_of_carnivores()}

    def make_movie(self, movie_fmt=None):
        """Create MPEG4 movie from visualization images saved."""
        self._graphics.make_movie(movie_fmt)
