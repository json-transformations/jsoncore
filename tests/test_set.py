from copy import deepcopy

from jsoncore.core import set_value

import pytest

SAMPLE_DATA = {
  "source": {
    "name": "Asterank",
    "url": "http://www.asterank.com/api"
  }, "asteroids": [
    {"name": "Ryugu", "type": "Cg", "value $": 82760000000},
    {"name": "1989 ML", "type": "X", "value $": 13940000000},
    {"name": "Nerus", "type": "Xe", "value $": 4710000000}
  ]
}


def test_set_value_missing_key():
    d = deepcopy(SAMPLE_DATA)
    set_value(('missing', 'key'), True, d)
    assert d == SAMPLE_DATA


def test_set_value_index_out_of_range():
    d = deepcopy(SAMPLE_DATA)
    set_value(('asteroids', 8), {}, d)
    assert d == SAMPLE_DATA


def test_set_value_type_error():
    d = deepcopy(SAMPLE_DATA)
    set_value(('source', 8), 'test', d)
    assert d['source'][8] == 'test'


def test_set_value_names():
    d1 = deepcopy(SAMPLE_DATA)
    set_value(('source', 'name'), 'test', d1)
    assert d1['source']['name'] == 'test'

    d2 = deepcopy(SAMPLE_DATA)
    d2['source']['name'] = 'test'
    assert d1 == d2


def test_set_value_index_number():
    d1 = deepcopy(SAMPLE_DATA)
    set_value(('asteroids', 0, 'name'), 'test', d1)
    assert d1['asteroids'][0]['name'] == 'test'

    d2 = deepcopy(SAMPLE_DATA)
    d2['asteroids'][0]['name'] = 'test'
    assert d1 == d2


def test_get_value_slice():
    d1 = deepcopy(SAMPLE_DATA)
    set_value(('asteroids', slice(1, None)), ['test'], d1)
    assert len(d1['asteroids']) == 2
    assert d1['asteroids'][1] == 'test'

    d2 = deepcopy(SAMPLE_DATA)
    d2['asteroids'][1:] = ['test']
    assert d1 == d2

    d1 = deepcopy(SAMPLE_DATA)
    set_value(('asteroids', slice(None, 2)), ['test'], d1)
    assert len(d1['asteroids']) == 2
    assert d1['asteroids'][0] == 'test'

    d2 = deepcopy(SAMPLE_DATA)
    d2['asteroids'][:2] = ['test']
    assert d1 == d2

    d1 = deepcopy(SAMPLE_DATA)
    set_value(('asteroids', slice(1, 2)), ['test'], d1)
    assert len(d1['asteroids']) == 3
    assert d1['asteroids'][1] == 'test'

    d2 = deepcopy(SAMPLE_DATA)
    d2['asteroids'][1:2] = ['test']
    assert d1 == d2

    d1 = deepcopy(SAMPLE_DATA)
    set_value(('asteroids', slice(None, None, 2)), ['test1', 'test2'], d1)
    assert len(d1['asteroids']) == 3
    assert d1['asteroids'][0] == 'test1'

    d2 = deepcopy(SAMPLE_DATA)
    d2['asteroids'][::2] = ['test1', 'test2']
    assert d1 == d2


def test_get_value_slice_in_middle():
    d1 = deepcopy(SAMPLE_DATA)
    set_value(('asteroids', slice(1, 2), 0, 'name'), 'test', d1)

    d2 = deepcopy(SAMPLE_DATA)
    d2['asteroids'][1:2][0]['name'] = 'test'
    assert d1 == d2
