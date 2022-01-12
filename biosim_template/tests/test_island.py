from biosim.island import Island
from biosim.animal import Herbivore, Carnivore
import textwrap
import random

seed = 1234

geogr = """\
               WWW
               WLW
               WWW"""
geogr = textwrap.dedent(geogr)
age = 5
weight = 20
ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': age,
                       'weight': weight}
                      for _ in range(50)]}]

ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': age,
                       'weight': weight}
                      for _ in range(20)]}]


def test_season():
    """Tests if there are born more herbivore"""
    random.seed(seed)
    cell = Island(geogr, ini_herbs)
    cell.season()
    cell.season()
    assert cell.amount_of_herbivores() > 50


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


def test_herbivore_map():
    """Test if herbivore_map returns a list"""
    cell = Island(geogr, ini_herbs)
    assert type(cell.herbivore_map()) == list


def test_carnivore_map():
    """Test if carnivore_map returns a list"""
    cell = Island(geogr, ini_carns)
    assert type(cell.carnivore_map()) == list


def test_herbivore_ages():
    """Test if it returns a list with the age of herbivores in one location"""
    cell = Island(geogr, ini_herbs)
    assert cell.herbivore_ages() == [5 for _ in range(50)]


def test_carnivore_ages():
    """Test if it returns a list with the age of carnivores in one location"""
    cell = Island(geogr, ini_carns)
    assert cell.carnivore_ages() == [5 for _ in range(20)]


def test_herbivore_weights():
    """Test if it returns a list with the weight of herbivores in one location"""
    cell = Island(geogr, ini_herbs)
    assert cell.herbivore_weights() == [20 for _ in range(50)]


def test_carnivore_weights():
    """Test if it returns a list with the weight of carnivores in one location"""
    cell = Island(geogr, ini_carns)
    assert cell.carnivore_weights() == [20 for _ in range(20)]


def test_herbivore_fitness():
    """Test if it returns a list with the fitness of herbivores in one location"""
    cell = Island(geogr, ini_herbs)
    assert cell.herbivore_fitness() == [Herbivore(age, weight).fitness for _ in range(50)]


def test_carnivore_fitness():
    """Test if it returns a list with the fitness of carnivores in one location"""
    cell = Island(geogr, ini_carns)
    assert cell.carnivore_fitness() == [Carnivore(age, weight).fitness for _ in range(20)]
