from copy import deepcopy

from jsoncore.core import jsondel

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


def test_del_missing_key():
    d = deepcopy(SAMPLE_DATA)
    jsondel(d, ('missing', 'key'))
    assert d == SAMPLE_DATA


def test_del_index_out_of_range():
    d = deepcopy(SAMPLE_DATA)
    jsondel(d, ('asteroids', 8))
    assert d == SAMPLE_DATA


def test_del_type_error():
    d = deepcopy(SAMPLE_DATA)
    jsondel(d, ('source', 8))
    jsondel(d, ('asteriod', 'name'))
    assert d == SAMPLE_DATA


def test_jsondel_names():
    d1 = deepcopy(SAMPLE_DATA)
    jsondel(d1, ('source', 'name'))
    d2 = deepcopy(SAMPLE_DATA)
    del d2['source']['name']
    assert d1 == d2


def test_del_index_number():
    d1 = deepcopy(SAMPLE_DATA)
    jsondel(d1, ('asteroids', 0, 'name'))
    d2 = deepcopy(SAMPLE_DATA)
    del d2['asteroids'][0]['name']
    assert d1 == d2


def test_get_value_slice():
    d1 = deepcopy(SAMPLE_DATA)
    jsondel(d1, ('asteroids', slice(1, None)))
    d2 = deepcopy(SAMPLE_DATA)
    del d2['asteroids'][1:]
    assert d1 == d2

    d1 = deepcopy(SAMPLE_DATA)
    jsondel(d1, ('asteroids', slice(None, 2)))
    d2 = deepcopy(SAMPLE_DATA)
    del d2['asteroids'][:2]
    assert d1 == d2

    d1 = deepcopy(SAMPLE_DATA)
    jsondel(d1, ('asteroids', slice(1, 2)))
    d2 = deepcopy(SAMPLE_DATA)
    del d2['asteroids'][1:2]
    assert d1 == d2

    d1 = deepcopy(SAMPLE_DATA)
    jsondel(d1, ('asteroids', slice(None, None, 2)))
    d2 = deepcopy(SAMPLE_DATA)
    del d2['asteroids'][::2]
    assert d1 == d2


def test_get_value_slice_in_middle():
    d1 = deepcopy(SAMPLE_DATA)
    jsondel(d1, ('asteroids', slice(1, 2), 0, 'name'))
    d2 = deepcopy(SAMPLE_DATA)
    del d2['asteroids'][1:2][0]['name']
    assert d1 == d2
