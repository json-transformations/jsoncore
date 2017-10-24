from jsoncore.core import get_value

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


def test_get_value_missing_key():
    assert get_value(SAMPLE_DATA, ['missing', 'key']) is None


def test_get_value_index_out_of_range():
    assert get_value(SAMPLE_DATA, ['asteroids', 8]) is None


def test_get_value_type_error():
    assert get_value(SAMPLE_DATA, ['source', 8]) is None
    assert get_value(SAMPLE_DATA, ['asteriod', 'name']) is None


def test_get_value_key_names():
    assert get_value(SAMPLE_DATA, ('source', 'name')) == 'Asterank'


def test_get_value_index_number():
    assert get_value(SAMPLE_DATA, ('asteroids', '0', 'name')) == 'Ryugu'


def test_get_value_slice():
    expect = SAMPLE_DATA['asteroids'][1:]
    assert get_value(SAMPLE_DATA, ('asteroids', '1:')) == expect

    expect = SAMPLE_DATA['asteroids'][:2]
    assert get_value(SAMPLE_DATA, ('asteroids', ':2')) == expect

    expect = SAMPLE_DATA['asteroids'][1:2]
    assert get_value(SAMPLE_DATA, ('asteroids', '1:2')) == expect

    expect = SAMPLE_DATA['asteroids'][::2]
    assert get_value(SAMPLE_DATA, ('asteroids', '::2')) == expect


def test_get_value_slice_in_middle():
    assert get_value(SAMPLE_DATA, ('asteroids', ':2', 'name')) is None

