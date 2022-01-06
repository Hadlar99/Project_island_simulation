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

    assert cell.num_herbivores() < 10
