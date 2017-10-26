from jsoncore.types import MinMax, jsontypes


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

EXPECTED_TYPES = {
    (): {'object': MinMax(min=2, max=2)},
    ('source',): {'object': MinMax(min=2, max=2)},
    ('source', 'name'): {'string': MinMax(min=8, max=8)},
    ('source', 'url'): {'string': MinMax(min=27, max=27)},
    ('asteroids',): {'array': MinMax(min=3, max=3)},
    ('asteroids', '*'): {'object': MinMax(min=3, max=3)},
    ('asteroids', '*', 'name'): {'string': MinMax(min=5, max=7)},
    ('asteroids', '*', 'type'): {'string': MinMax(min=2, max=2)},
    ('asteroids', '*', 'value $'): {
        'number (int)': MinMax(min=4710000000, max=82760000000)
    }
}


def test_get_types():
    assert jsontypes(SAMPLE_DATA) == EXPECTED_TYPES
