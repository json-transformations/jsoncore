from jsoncore.core import jsonkeys

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

EXPECTED_RESULT = {
    (),
    ('source',),
    ('source', 'name'),
    ('source', 'url'),
    ('asteroids',),
    ('asteroids', '*'),
    ('asteroids', '*', 'name'),
    ('asteroids', '*', 'type'),
    ('asteroids', '*', 'value $')
}


def test_jsonkeys():
    result = jsonkeys(SAMPLE_DATA)
    print(result)
    assert result == EXPECTED_RESULT
