from biosim.Island import Island
import textwrap


def test_feeding_season():
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
    cell = Island(geogr, ini_herbs)
    cell.feeding_season()

