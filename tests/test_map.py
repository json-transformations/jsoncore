import json
import os

from jsoncore.mapreducefilter import map_values

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))


def test_map_values():
    data = json.load(open(os.path.join(MODULE_PATH, 'data/nfl_arrests.json')))
    result = map_values([('Team_name',)], str.upper, data)
    print(result)
    assert result == True
