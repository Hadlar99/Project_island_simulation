"""Test for Landscape class"""
import random

from biosim.landscape import Lowland, Highland, Dessert, Water
from biosim.animal import Herbivore, Carnivore
import pytest
seed = 456
pop_1 = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(50)]

pop_2 = [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(50)]

pop_3 = [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(20)]


def test_pop_animals():
    """Test if it counts the list of herbivores and carnivores correctly"""
    cell = Lowland()
    cell.pop_animals(pop_1)
    cell.pop_animals(pop_2)
    assert cell.num_herbivores(), cell.num_carnivores() == 50


def test_pop_animals_error():
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
    """Test if the carnivores are going to eat any herbivores by reducing
    herbivore population"""
    random.seed(seed)

    cell = Lowland()
    cell.pop_animals(pop_1)
    cell.pop_animals(pop_3)

    cell.carnivore_feeding()

    assert cell.num_herbivores() < 50


def test_reproduction_herbivores():
    """Test if there are getting more herbivores when new herbivores are born"""
    random.seed(seed)
    cell = Lowland([Herbivore(3, 35) for _ in range(10)])
    cell.reproduction()

    assert cell.num_herbivores() > 10


def test_reproduction_carnivores():
    """Test if there are getting more carnivores when new carnivores are born"""
    random.seed(seed)
    cell = Lowland(carnivores=[Carnivore(3, 40) for _ in range(10)])
    cell.reproduction()

    assert cell.num_carnivores() > 10


def test_aging_animals():
    """Tests if the herbivores are aging correctly"""
    cell = Lowland([Herbivore(a, 35) for a in range(10)], [Carnivore(a, 35) for a in range(10)])
    cell.aging_animals()

    assert all(herbi._age == i + 1 for i, herbi in enumerate(cell.herbivores)) and \
           all(carni._age == i + 1 for i, carni in enumerate(cell.carnivores))


def test_loss_of_weight():
    """Test if the herbivores loses weight correctly """
    cell = Lowland([Herbivore(7, 35)], [Carnivore(7, 35)])
    cell.weight_loss()

    assert cell.herbivores[0]._weight == 35 - 35 * cell.herbivores[0].params['eta'] and \
           cell.carnivores[0]._weight == 35 - 35 * cell.carnivores[0].params['eta']


def test_pop_reduction():
    """Test if there are getting less herbivores when herbivores dies """
    random.seed(seed)
    cell = Lowland([Herbivore(a, 20) for a in range(50)])
    cell.pop_reduction()

    assert cell.num_herbivores() < 50


@pytest.fixture
def reset_food_params():
    """"""
    yield
    Lowland.f_max = Lowland.default_f_max


def test_food_params(reset_food_params):
    """Test if we can change the food params for a given landscape"""
    Lowland.food_params({'f_max': 100.})
    cell = Lowland([Herbivore() for _ in range(50)])
    cell.feeding()
    assert cell.fodder == 0


def test_invalid_food_param(reset_food_params):
    """Tests if it raises KeyError if we try to set a parameter that does not exists"""
    with pytest.raises(KeyError):
        Lowland.food_params({'food': 600})


def test_herbivore_eats_rest(reset_food_params):
    """Tests if the herbivore eats the rest of the food"""
    Lowland.food_params({'f_max': 95})
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


def test_immigration():
    """Tests if immigration works correctly"""
    cell = Highland(pop_1, pop_2)
    cell.immigrating_carnivores = pop_3
    cell.immigration()
    assert len(cell.immigrating_carnivores) == 0 and len(cell.carnivores) == len(pop_1) + len(pop_3)


def test_list_herbivore_ages():
    """Test to see if it returns a list with the ages of herbivores"""
    cell = Lowland([Herbivore(3, 50)])
    assert type(cell.list_herbivores_ages()) == list and cell.list_herbivores_ages() == [3]


def test_list_carnivores_ages():
    """Test to see if it returns a list with the ages of carnivores"""
    cell = Lowland(carnivores=[Carnivore(3, 50)])
    assert type(cell.list_carnivores_ages()) == list and cell.list_carnivores_ages() == [3]


def test_list_herbivore_weight():
    """Test to see if it returns a list with the weight of herbivores"""
    cell = Lowland([Herbivore(3, 50)])
    assert type(cell.list_herbivores_weight()) == list and cell.list_herbivores_weight() == [50]


def test_list_carnivores_weight():
    """Test to see if it returns a list with the weight of carnivores"""
    cell = Lowland(carnivores=[Carnivore(3, 50)])
    assert type(cell.list_carnivores_weight()) == list and cell.list_carnivores_weight() == [50]


def test_list_herbivore_fitness():
    """Test if it returns a list with the fitness of herbivores"""
    cell = Lowland([Herbivore(3, 50)])
    assert type(cell.list_herbivores_fitness()) == list and\
           cell.list_herbivores_fitness() == [Herbivore(3, 50)._fitness]


def test_list_carnivore_fitness():
    """Test if it retruns a list with the fitness of carnivores"""
    cell = Lowland(carnivores=[Carnivore(3, 50)])
    assert type(cell.list_carnivores_fitness()) == list and \
           cell.list_carnivores_fitness() == [Carnivore(3, 50)._fitness]
