from jsoncore.core import get_item

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


def test_get_item_missing_key():
    data = SAMPLE_DATA
    keys = ('missing', 'key')
    result = get_item(keys, data)
    expect = ('key', None)
    assert result == expect


def test_get_item():
    data = SAMPLE_DATA
    keys = ('asteroids', 0, 'name')
    result = get_item(keys, data)
    expect = ('name', 'Ryugu')
    assert result == expect


def test_get_item_fullpath():
    data = SAMPLE_DATA
    keys = ('asteroids', 0, 'name')
    result = get_item(keys, data, fullpath=True)
    expect = ('asteroids.0.name', 'Ryugu')
    assert result == expect


def test_get_item_default_value():
    data = SAMPLE_DATA
    keys = ('missing', 'key')
    result = get_item(keys, data, default='N/A')
    expect = ('key', 'N/A')
    assert result == expect
