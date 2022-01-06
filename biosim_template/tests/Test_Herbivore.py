from biosim.herbivore import Herbivore
import pytest

def test_age():
    num_year = 21
    herbivore = Herbivore()
    for i in range (num_year):
        herbivore.year()
    assert herbivore.age == num_year


def test_add_weight():
    herbivore = Herbivore()
    herbivore.add_weight(10)

    assert herbivore.weight >= 0

def test_lose_weight():
    herbivore = Herbivore()
    previous_weight = herbivore.weight
    herbivore.lose_weight()

    assert herbivore.weight < previous_weight


def test_fitness():
    herbivore = Herbivore(8)
    assert 0 <= herbivore.fitness() <= 1