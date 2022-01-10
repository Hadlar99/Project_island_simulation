from biosim.island import Island
import textwrap
import random

seed = 1234

geogr = """\
               WWW
               WLW
               WWW"""
geogr = textwrap.dedent(geogr)
ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]


def test_amount_of_herbivores():
    """Test if the function amount_of_herbivores counts the amount of carnivores correctly"""
    world = Island(geogr, ini_herbs)
    assert world.amount_of_herbivores() == 50


def test_amount_carnivores():
    """Test if the function amount_of_carnivores counts the amount of carnivores correctly"""
    world = Island(geogr, ini_carns)
    assert world.amount_of_carnivores() == 20


def test_new_animals():
    """Tests if the new_animal function works correctly"""
    cell = Island(geogr, ini_herbs)
    cell.new_animals(ini_herbs)
    assert cell.amount_of_herbivores() == 100


def test_season():
    """Tests if there are born more herbivore"""
    random.seed(seed)
    cell = Island(geogr, ini_herbs)
    cell.season()
    cell.season()
    assert cell.amount_of_herbivores() > 50
