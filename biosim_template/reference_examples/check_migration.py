import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim

"""
Checks if the Animals are migrating correctly
"""

if __name__ == '__main__':

    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WLLLLLLLLLLLLLLLLLLLW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(400)]}]
    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 1000}
                          for _ in range(150)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs+ini_carns,
                 seed=123456,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 vis_years=1, cmax_animals={'Herbivore': 60})

    sim.set_animal_parameters('Herbivore', {'mu': 100})
    sim.set_animal_parameters('Carnivore', {'mu': 100, 'F': 0})
    sim.set_landscape_parameters('L', {'f_max': 700})

    sim.simulate(num_years=10)
