"""Test for Animal class"""


from biosim.Animal import Herbivore


def test_age():
    """test for aging of herbivore, each time it is called the age will grow with 1"""
    num_year = 21
    herbivore = Herbivore(5)
    for i in range(num_year):
        herbivore.year()
    assert herbivore.age == num_year + 5


def test_add_weight():
    """Checks if the weight goes up when the herbivore eats"""
    herbivore = Herbivore()
    herbivore.add_weight(10)

    assert herbivore.weight >= 9    # the weight must be more than 9 because of beta and how much it eats


def test_lose_weight():
    """checks if the herbivore loses weight"""
    herbivore = Herbivore()
    previous_weight = herbivore.weight
    herbivore.lose_weight()

    assert herbivore.weight < previous_weight


def test_fitness():
    """find the fitness of the animal, fitness is a number between 0 and 1"""
    herbivore = Herbivore(8)
    assert 0 <= herbivore.fitness() <= 1


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


def test_death():
    """if herbivore weight is 0 it will die"""
    herbivore = Herbivore(0, 0)
    assert herbivore.death()
