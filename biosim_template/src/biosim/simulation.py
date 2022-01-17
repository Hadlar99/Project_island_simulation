"""
Template for BioSim class.
"""
from .island import Island
from .animal import Herbivore, Carnivore
from .landscape import Dessert, Highland, Lowland, Water
import random
from .graphics import Graphics


# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU

class BioSim:
    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):
        """

        Parameters
        ----------
        island_map: string
            Multi-line string that describe the Island and ist terrain
        ini_pop: list
            list with dictionaries that describes the initial population on the island
        seed: int
            decide which random number to use
        vis_years: int
            years between each visualization update
        ymax_animals: int
            sets the y-max limit on the animal graph
        cmax_animals: dict
            gives the specified color code for the heatmap
        hist_specs: dict
            gives x-max limit and bins to the different histograms
        img_dir: string
            gives the path to where the images will be saved
        img_base: string
            gives the filename to where the images and movie will be saved
        img_fmt: string
            specifies which format the images shall be saved in
        img_years: int
            years between the images is saved
        log_file:
            if given, write animal counts to the file

        Raises
        ------
        KeyError
        """

        random.seed(seed)
        self.Island = Island(island_map, ini_pop)
        self.Island_map = island_map

        self.cmax_herbivore = None
        self.cmax_carnivore = None
        # Checks if cmax_animals are given
        if cmax_animals is not None:
            for ani, num in cmax_animals.items():
                if ani == 'Herbivore':
                    self.cmax_herbivore = num
                elif ani == 'Carnivore':
                    self.cmax_carnivore = num
                else:
                    raise KeyError(f'Key in cmax_animals must be Herbivore or Carnivore, not {ani}')

        self.hist_specs_age = None
        self.hist_specs_weight = None
        self.hist_specs_fitness = None
        # Check if hist_spec are given
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

        self._graphics = Graphics(self.Island_map, vis_years=vis_years, img_fmt=img_fmt, ymax_animals=ymax_animals,
                                  cmax_herbi=self.cmax_herbivore, cmax_carni=self.cmax_carnivore,
                                  hist_specs_age=self.hist_specs_age, hist_specs_fitness=self.hist_specs_fitness,
                                  hist_specs_weight=self.hist_specs_weight, img_dir=img_dir, img_name=img_base)

        self._year = 0
        self._final_year = None

        self.vis_years = vis_years
        self.img_years = img_years

        self.log_file = log_file
        if self.log_file is not None:
            with open(self.log_file, 'w') as f:
                f.write(f"{'Year':10}, {'Num herbivores':15}, {'Num carnivores':15}, {'Tot animals':15} \n"
                        f"{self.year:10}, {self.Island.amount_of_herbivores():15}, "
                        f"{self.Island.amount_of_carnivores():15}, {self.num_animals:15}\n")

    @staticmethod
    def set_animal_parameters(species, params):
        """
        Set parameters for animal species

        Parameters
        ----------
        species: string
            name of species, must be Herbivore or Carnivore
        params: dict
            all the different parameters for each species

        Raises
        -------
        NameError
        """

        if species == 'Herbivore':
            Herbivore.set_params(params)
        elif species == 'Carnivore':
            Carnivore.set_params(params)
        else:
            raise NameError('Species have to be Herbivore or Carnivore ')

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """
        Set parameters for the different kinds of landscape

        Parameters
        ----------
        landscape: string
            Code letter for which kind of landscape it is
        params: dict
            parameters for the different kind of landscape

        Raises
        ------
        NameError
        """

        if landscape == 'L':
            Lowland.food_params(params)
        elif landscape == 'H':
            Highland.food_params(params)
        elif landscape == 'D':
            Dessert.food_params(params)
        else:
            raise NameError(f'Landscape has to be L, H or D')

    def simulate(self, num_years):
        """
        Run the simulation while the result are being visualized

        Parameters
        ----------
        num_years: int
            how many years the simulation are gong to run

        Raises
        ------
        ValueError
        """

        self._final_year = self._year + num_years

        if self.img_years is None:
            self.img_years = self.vis_years

        if self.vis_years != 0:
            if self.img_years % self.vis_years != 0:
                raise ValueError('img_years must be multiple of vis_years')

            self._graphics.setup(self._final_year, self.img_years)

        while self._year < self._final_year:
            self.Island.season()
            self._year += 1

            if self.vis_years != 0:
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

            if self.log_file is not None:
                with open(self.log_file, 'a') as f:
                    f.write(f"{self.year:10}, {self.Island.amount_of_herbivores():15}, "
                            f"{self.Island.amount_of_carnivores():15}, {self.num_animals:15}\n")

    def add_population(self, population):
        """
        Add population to the island

        Parameters
        ----------
        population: list
            list of dictionaries specifying the population
        """

        self.Island.new_animals(population)

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.Island.amount_of_herbivores() + self.Island.amount_of_carnivores()

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return {'Herbivore': self.Island.amount_of_herbivores(), 'Carnivore': self.Island.amount_of_carnivores()}

    def make_movie(self, movie_fmt=None):
        """
        Create MPEG4 movie from visualization images saved.
        Parameters
        ----------
        movie_fmt: str
            Movie format the movie should be made in
        """
        self._graphics.make_movie(movie_fmt)
