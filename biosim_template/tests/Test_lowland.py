from biosim.Landscape import lowland
from biosim.herbivore import Herbivore

import pytest


def test_count_herbivores():
    cell = lowland([Herbivore() for _ in range(50)])

    assert cell.num_herbivores() == 50


def test_feeding():
    cell = lowland([Herbivore() for _ in range(50)])
    cell.feeding()

    assert cell.fodder == 800-50*10


def test_feeding_no_fodder():
    cell = lowland([Herbivore() for _ in range(90)])
    cell.feeding()

    assert cell.fodder == 0


def test_reproduction():
    cell = lowland([Herbivore(3, 35) for _ in range(10)])
    cell.reproduction()

    assert cell.num_herbivores() > 10


def test_aging():
    cell = lowland([Herbivore(a, 35) for a in range(10)])
    cell.aging()

    assert cell.herbivores[-1].age == 10


def test_loss_of_weight():
    cell = lowland([Herbivore(7, 35)])
    cell.loss_of_weight()

    assert cell.herbivores[0].weight == 35 - 35 * cell.herbivores[0].params['eta']

def test_pop_reduction():
    cell = lowland([Herbivore(a, 35) for a in range(50)])
    cell.pop_reduction()

    assert cell.num_herbivores() < 50