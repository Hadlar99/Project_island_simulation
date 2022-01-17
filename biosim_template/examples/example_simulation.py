import textwrap
from biosim.simulation import BioSim


geogr = '''\
           WWWWWWWWWWWWWWWWWWWWW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHLLLLWWLLLLLLLWW
           WWHHLLLLLLLWWLLLLLLLW
           WWHHLLLLLLLWWLLLLLLLW
           WWWWWWWWHWWWWLLLLLLLW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHDDDHHHWWLLLLLLWWW
           WHHHHHDDDDLLLLLLLLWWW
           WWWWWWWWWWWWWWWWWWWWW'''
geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 7),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(80)]}]
ini_carns = [{'loc': (2, 7),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]

sim = BioSim(geogr, ini_herbs + ini_carns, seed=1,
             hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                         'age': {'max': 60.0, 'delta': 2},
                         'weight': {'max': 60, 'delta': 2}},
             cmax_animals={'Herbivore': 200, 'Carnivore': 50},
             img_dir='../data',
             img_base='sample', vis_years=1)
sim.simulate(50)
sim.make_movie()
