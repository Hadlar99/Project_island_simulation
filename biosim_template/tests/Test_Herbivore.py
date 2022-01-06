import random

from biosim.herbivore import Herbivore
import pytest
random.seed(15)


def test_age():
    num_year = 21
    herbivore = Herbivore(5)
    for i in range (num_year):
        herbivore.year()
    assert herbivore.age == num_year + 5


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


def test_give_birth(mocker):
    mocker.patch('random.random', return_value=0.1)
    mocker.patch('random.gauss', return_value=8)
    herbivore = Herbivore(5, 50)

    assert 8 == herbivore.birth(10)


def test_not_birth_weight(mocker):
    herbivore = Herbivore(0, 10)

    assert 6.5 >= herbivore.birth(100) <= 9.5


def test_death():
    herbivore = Herbivore(0, 0)
    assert herbivore.death()

