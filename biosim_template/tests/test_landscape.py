"""Test for Landscape class"""
import random

from biosim.landscape import Lowland, Highland, Dessert, Water
from biosim.animal import Herbivore, Carnivore
import pytest
seed = 456
ini_herbs = [{'species': 'Herbivore',
              'age': 5,
              'weight': 20}
             for _ in range(50)]
ini_carns = [{'species': 'Carnivore',
              'age': 5,
              'weight': 20}
             for _ in range(20)]


def test_pop_animals():
    """Test if it counts the list of herbivores and carnivores correctly"""
    cell = Lowland()
    cell.pop_animals([{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)])
    cell.pop_animals([{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)])
    assert cell.num_herbivores(), cell.num_carnivores() == 50


def test_pop_animals_ValueError():
    """Checks if the program raises a ValueError if wrong species"""
    with pytest.raises(ValueError):
        cell = Lowland()
        cell.pop_animals([{'species': 'Animal',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)])

def test_count_herbivores():
    """Tests if the num_herbivores count correctly"""
    cell = Lowland(herbivores=[Herbivore() for _ in range(50)])

    assert cell.num_herbivores() == 50

def test_count_carnivore():
    """Test if the num_carnivore count correctly"""
    cell = Highland(carnivores=[Carnivore() for _ in range(50)])

    assert cell.num_carnivores() == 50

def test_feeding():
    """Tests if the right amount of food are eaten"""
    cell = Lowland([Herbivore() for _ in range(50)])
    cell.feeding()

    assert cell.fodder == 800-50*10


def test_feeding_if_no_fodder():
    """Test when all the fodder goes empty"""
    cell = Lowland([Herbivore() for _ in range(90)])
    cell.feeding()

    assert cell.fodder == 0


def test_feeding_carnivores():
    """Test if the carnivores are going to eat any herbivores"""
    random.seed(seed)

    cell = Lowland()
    cell.pop_animals(ini_herbs)
    cell.pop_animals(ini_carns)

    cell.carnivore_feeding()

    assert cell.num_herbivores() < 50


def test_reproduction():
    """Test if there are getting more herbivores when new herbivores are born"""
    random.seed(seed)
    cell = Lowland([Herbivore(3, 35) for _ in range(10)])
    cell.reproduction()

    assert cell.num_herbivores() > 10


def test_aging():
    """Tests if the herbivores are aging correctly"""
    cell = Lowland([Herbivore(a, 35) for a in range(10)], [Carnivore(a, 35) for a in range(10)])
    cell.aging_and_loss_of_weight()

    assert all(herbi.age == i + 1 for i, herbi in enumerate(cell.herbivores))


def test_loss_of_weight():
    """Test if the herbivores loses weight correctly """
    cell = Lowland([Herbivore(7, 35)])
    cell.aging_and_loss_of_weight()

    assert cell.herbivores[0].weight == 35 - 35 * cell.herbivores[0].params['eta']


def test_pop_reduction():
    """Test if there are getting less herbivores when herbivores dies """
    random.seed(seed)
    cell = Lowland([Herbivore(a, 20) for a in range(50)])
    cell.pop_reduction()

    assert cell.num_herbivores() < 50


def test_food_params():
    """Test if we can change the food params for a given landscape"""
    Lowland.food_params({'f_max': 100.})
    cell = Lowland([Herbivore() for _ in range(50)])
    cell.feeding()
    assert cell.fodder == 0


def test_moving_params():
    """Test if is possible to move to this landscape"""
    cell = Lowland()
    assert cell.move


def test_moving_water_params():
    """Test if it is not possible to move to this landscape"""
    cell = Water()
    assert not cell.move


def test_migration():
    """Tests if the function migration returns 2 lists"""
    cell = Lowland([Herbivore() for _ in range(50)])
    cell_herbi, cell_carni = cell.migration()

    assert type(cell_herbi) == list and type(cell_carni) == list

def test_food_params():
    """Test if it is possible to change the food parameter in landscape"""
    Dessert.food_params({'f_max': 600})
    assert Dessert.f_max == 600