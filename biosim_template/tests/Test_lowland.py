"""Test for lowland class"""
import random

from biosim.Landscape import Lowland
from biosim.Animal import Herbivore, Carnivore

import pytest
seed = 456


def test_count_herbivores():
    """Tests the if the count_herbivores count correctly"""
    cell = Lowland([Herbivore() for _ in range(50)])

    assert cell.num_herbivores() == 50


def test_pop_herbivores():
    cell = Lowland()
    cell.pop_herbivores([{'species': 'Herbivore',
                        'age': 5,
                        'weight': 20}
                        for _ in range(50)])
    assert cell.num_herbivores() == 50

def test_feeding():
    """Tests if the right amount of food are eaten"""
    cell = Lowland([Herbivore() for _ in range(50)])
    cell.feeding()

    assert cell.fodder == 800-50*10


def test_feeding_no_fodder():
    """Test if there are no food left when all the food are eaten"""
    cell = Lowland([Herbivore() for _ in range(90)])
    cell.feeding()

    assert cell.fodder == 0


def test_reproduction():
    """Test if there are getting more herbivores when new herbivores are born"""
    random.seed(seed)
    cell = Lowland([Herbivore(3, 35) for _ in range(10)])
    cell.reproduction()

    assert cell.num_herbivores() > 10


def test_aging():
    """Tests if the herbivores are aging correctly"""
    cell = Lowland([Herbivore(a, 35) for a in range(10)], [Carnivore(a, 35) for a in range(10)])
    cell.aging()

    assert all(herbi.age == i + 1 for i, herbi in enumerate(cell.herbivores))


def test_loss_of_weight():
    """Test if the herbivores loses weight correctly """
    cell = Lowland([Herbivore(7, 35)])
    cell.loss_of_weight()

    assert cell.herbivores[0].weight == 35 - 35 * cell.herbivores[0].params['eta']


def test_pop_reduction():
    """Test if there are getting less herbivores when herbivores dies """
    random.seed(seed)
    cell = Lowland([Herbivore(a, 20) for a in range(50)])
    cell.pop_reduction()

    assert cell.num_herbivores() < 50


def test_food_params():
    Lowland.food_params({'f_max': 100.})
    cell = Lowland([Herbivore() for _ in range(50)])
    cell.feeding()
    assert cell.fodder == 0
