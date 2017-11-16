import json
import os

from jsoncore._compat import text_type
from jsoncore.mapreducefilter import map_values

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))


def test_map_values():
    data = json.load(open(os.path.join(MODULE_PATH, 'data/nfl_arrests.json')))
    result = map_values([('Team_name',)], getattr(text_type, 'upper'), data)
    assert result[0]['Team_name'] == 'VIKINGS'
    assert result[0]['Team_city'] == 'Minneapolis'
    assert result[1]['Team_name'] == 'BRONCOS'


def test_map_nested_values():
    data = json.load(open(os.path.join(MODULE_PATH, 'data/patients.json')))
    fields = [
        ('entry', '*', 'resource', 'contact', '*', 'gender'),
        ('entry', '*', 'resource', 'name', '*', 'family'),
        ('entry', '*', 'resource', 'name', '*', 'given', 0)
    ]
    result = map_values(fields, getattr(text_type, 'upper'), data)
    resource = result['entry'][10]['resource']
    assert resource['contact'][0]['gender'] == 'FEMALE'
    assert resource['name'][0]['family'] == 'CHALMERSCNVMSL'
    assert resource['name'][0]['given'][0] == 'PETERCNVMSL'
