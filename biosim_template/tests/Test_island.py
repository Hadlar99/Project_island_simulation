from biosim.Island import Island
import textwrap
geogr = """\
               WWW
               WLW
               WWW"""
geogr = textwrap.dedent(geogr)
ini_herbs = [{'loc': (2, 2),
                'pop': [{'species': 'Herbivore',
                        'age': 5,
                        'weight': 20}
                        for _ in range(50)]}]

def test_feeding_season():
    cell = Island(geogr, ini_herbs)
    cell.feeding_season()


def test_amount_of_herbivores():
    world = Island(geogr, ini_herbs)
    assert world.amount_of_herbivores() == 50

