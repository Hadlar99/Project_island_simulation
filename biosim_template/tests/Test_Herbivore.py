from biosim.herbivore import Herbivore
import pytest

def test_age():
    num_year = 21
    herbivore = Herbivore(8)
    for i in range (num_year):
        herbivore.year(10)
    assert herbivore.age == num_year
