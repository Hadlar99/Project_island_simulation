"""Test for Animal class"""
import pytest

from biosim.animal import Herbivore, Carnivore


class TestSetParameters:

    @pytest.fixture
    def reset_params(self):
        """Resetting the parameters to default"""
        yield
        Herbivore.params = Herbivore.default_params

    def test_set_params(self, reset_params):
        """Test if it is possible to change multiple params in Herbivore class"""
        Herbivore.set_params({'gamma': 0.8, 'mu': 1.5})
        assert Herbivore.params['gamma'] == 0.8 and Herbivore.params['mu'] == 1.5

    def test_invalid_param(self, reset_params):
        """Tests if it return KeyError if we try to set in a invalid parameter"""
        with pytest.raises(KeyError):
            Carnivore.set_params({'no_param': 0.6})

    def test_invalid_value(self, reset_params):
        """Tests if it return ValueError if we try to set in a invalid value for a parameter"""
        with pytest.raises(ValueError):
            Herbivore.set_params({'gamma': -0.6})

    def test_invalid_delta_phi_max(self, reset_params):
        """Tests if it return ValueError if we try to set in a invalid value for DeltaPhiMax"""
        with pytest.raises(ValueError):
            Carnivore.set_params({'DeltaPhiMax': 0})

    def test_invalid_eta(self, reset_params):
        """Tests if it return ValueError if we try to set in a invalid value for eta"""
        with pytest.raises(ValueError):
            Herbivore.set_params({'eta': 2})


def test_age():
    """Test for aging of herbivore, each time it is called the age will grow with 1"""
    num_year = 21
    herbivore = Herbivore(5)
    for i in range(num_year):
        herbivore.aging_and_lose_weight()
    assert herbivore.age == num_year + 5


def test_add_weight():
    """Checks if the weight goes up when the herbivore eats"""
    herbivore = Herbivore()
    herbivore.add_weight(10)

    assert herbivore.weight >= 9    # the weight must be more than 9 because of beta and how much it eats


def test_lose_weight():
    """Checks if the herbivore loses weight"""
    herbivore = Herbivore()
    previous_weight = herbivore.weight
    herbivore.aging_and_lose_weight()

    assert herbivore.weight < previous_weight


def test_fitness():
    """find the fitness of the animal, fitness is a number between 0 and 1"""
    herbivore = Herbivore(8)
    herbivore.update_fitness()
    assert 0 <= herbivore.fitness <= 1


def test_give_birth(mocker):
    """test if herbivore gives birth, specified the random numbers needed to give wished weight of baby"""
    mocker.patch('random.random', return_value=0.1)
    mocker.patch('random.gauss', return_value=8)
    herbivore = Herbivore(5, 50)

    assert 8 == herbivore.birth(10)


def test_not_birth_weight():
    """test if herbivore cannot give birth because of weight"""
    herbivore = Herbivore(0, 10)

    assert not herbivore.birth(100)


def test_baby_weights_too_much(mocker):
    """test if the baby is not born if it weights too much"""
    mocker.patch('random.random', return_value=0.1)
    mocker.patch('random.gauss', return_value=51)
    herbivore = Herbivore(5, 50)

    assert not herbivore.birth(10)


def test_not_birth(mocker):
    """Tests if birth returns False when it should not give birth"""
    mocker.patch('random.random', return_value=1)
    herbivore = Herbivore(5, 50)

    assert not herbivore.birth(10)


def test_death_weight_0():
    """if herbivore weight is 0 it will die"""
    herbivore = Herbivore(0, 8)
    herbivore.weight = 0
    assert herbivore.death()


def test_death(mocker):
    """Test if the animal dies when it should"""
    mocker.patch('random.random', return_value=0)
    herbivore = Herbivore(5, 50)

    assert herbivore.death()


def test_not_death(mocker):
    """Test if the animal survives when it should"""
    mocker.patch('random.random', return_value=1)
    herbivore = Herbivore(5, 50)

    assert not herbivore.death()


def test_migrate_false(mocker):
    """Tests if migrate returns False when the animal will not move"""
    mocker.patch('random.random', return_value=1)
    herbivore = Herbivore(5, 10)

    assert not herbivore.migrate()


def test_migrate_true(mocker):
    """Tests if migrate returns True when the animal will move"""
    mocker.patch('random.random', return_value=0)
    herbivore = Herbivore(5, 50)

    assert herbivore.migrate()


def test_weight_negative():
    """Tests if animal raises ValueError if weight of animal is not strictly posetive"""
    with pytest.raises(ValueError):
        Herbivore(0, 0)


def test_update_fitness_negative_weight():
    """Tests if it sets fitness to 0 if weight is 0 or lower"""
    herbivore = Herbivore(0, 8)
    herbivore.weight = -2
    herbivore.update_fitness()

    assert herbivore.fitness == 0


def test_baby_weight_negative(mocker):
    """Test if birth returns False when baby weight is negative"""
    mocker.patch('random.gauss', return_value=-1)
    mocker.patch('random.random', return_value=0)
    herbivore = Herbivore(10, 40)

    assert not herbivore.birth(10)
