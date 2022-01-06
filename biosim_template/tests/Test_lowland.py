from biosim.Landscape import lowland
from biosim.herbivore import Herbivore
import pytest

def test_count_herbivores():
    cell = lowland([Herbivore() for _ in range(50)])

    assert cell.num_herbivores() == 50



