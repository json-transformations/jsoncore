from jsoncore.functional import (
    apply_funct, group_array_keys, key_funct, splitlist
)
from jsoncore.core import get_value, set_value


def test_splitlist():
    data = ['Solar System', 'planets', '*', 'moons', '*', 'craters', '*',
            'name']
    expect = [['Solar System', 'planets'], ['moons'], ['craters'], ['name']]
    result = splitlist(data)
    assert result == expect


def test_group_array_keys():
    data = [
        ['Solar System', 'planets', 'number'],
        ['Solar System', 'planets', '*', 'moons', '*', 'craters', '*', 'name'],
        ['Solar System', 'planets', '*', 'moons', '*', 'craters', '*', 'size']]
    expect = [(
        (['Solar System', 'planets'], ['moons'], ['craters']),
        (['name'], ['size'])), ((), (['Solar System', 'planets', 'number'],))]
    result = group_array_keys(data)
    assert result == expect


def test_key_funct():
    def map_values(keys, funct, seq):
        def apply_funct2keys(item):
            for key in keys:
                set_value(key, funct(get_value(key, item)), item)
            return item
        result = list(map(apply_funct2keys, seq))
        return result

    def capitalize(keys, data):
        return map_values(keys, str.upper, data)

    data = {
      "Solar System": {
        "planets": [
          {
            "name": "Mars",
            "moons": [
              {
                "name": "Phobos",
                "craters": [
                  {
                    "name": "Clustril",
                    "diameter (km)": 3.4
                  },
                  {
                    "name": "D'Arrest",
                    "diameter (km)": 2.1
                  }
                ]
              },
              {
                "name": "Deimos",
                "craters": [
                  {
                    "name": "Swift",
                    "diameter (km)": 1
                  },
                  {
                    "name": "Voltaire",
                    "diameter (km)": 1.9
                  }
                ]
              }
            ]
          },
          {
            "name": "Jupiter",
            "moons": [
              {
                "name": "Amalthea",
                "craters": [
                  {
                    "name": "Gaea",
                    "diameter (km)": 80
                  },
                  {
                    "name": "Pan",
                    "diameter (km)": 100
                  }
                ]
              },
              {
                "name": "Callisto",
                "craters": [
                  {
                    "name": "Adal",
                    "diameter (km)": 41.7
                  },
                  {
                    "name": "Aegir",
                    "diameter (km)": 53.9
                  }
                ]
              }
            ]
          }
        ]
      }
    }
    expect = {
      "Solar System": {
        "planets": [
          {
            "name": "Mars",
            "moons": [
              {
                "name": "Phobos",
                "craters": [
                  {
                    "name": "CLUSTRIL",
                    "diameter (km)": 3.4
                  },
                  {
                    "name": "D'ARREST",
                    "diameter (km)": 2.1
                  }
                ]
              },
              {
                "name": "Deimos",
                "craters": [
                  {
                    "name": "SWIFT",
                    "diameter (km)": 1
                  },
                  {
                    "name": "VOLTAIRE",
                    "diameter (km)": 1.9
                  }
                ]
              }
            ]
          },
          {
            "name": "Jupiter",
            "moons": [
              {
                "name": "Amalthea",
                "craters": [
                  {
                    "name": "GAEA",
                    "diameter (km)": 80
                  },
                  {
                    "name": "PAN",
                    "diameter (km)": 100
                  }
                ]
              },
              {
                "name": "Callisto",
                "craters": [
                  {
                    "name": "ADAL",
                    "diameter (km)": 41.7
                  },
                  {
                    "name": "AEGIR",
                    "diameter (km)": 53.9
                  }
                ]
              }
            ]
          }
        ]
      }
    }
    groups = [('Solar System', 'planets'), ('moons',)]
    array = ('craters',)
    keys = [('name',)]
    result = key_funct(capitalize, groups, array, keys, data)
    assert result == expect


def test_apply_funct():

    data = {
      "Solar System": {
        "planets": [
          {
            "name": "Mars",
            "moons": [
              {
                "name": "Phobos",
                "craters": [
                  {
                    "name": "Clustril",
                    "diameter (km)": 3.4
                  },
                  {
                    "name": "D'Arrest",
                    "diameter (km)": 2.1
                  }
                ]
              },
              {
                "name": "Deimos",
                "craters": [
                  {
                    "name": "Swift",
                    "diameter (km)": 1
                  },
                  {
                    "name": "Voltaire",
                    "diameter (km)": 1.9
                  }
                ]
              }
            ]
          },
          {
            "name": "Jupiter",
            "moons": [
              {
                "name": "Amalthea",
                "craters": [
                  {
                    "name": "Gaea",
                    "diameter (km)": 80
                  },
                  {
                    "name": "Pan",
                    "diameter (km)": 100
                  }
                ]
              },
              {
                "name": "Callisto",
                "craters": [
                  {
                    "name": "Adal",
                    "diameter (km)": 41.7
                  },
                  {
                    "name": "Aegir",
                    "diameter (km)": 53.9
                  }
                ]
              }
            ]
          }
        ]
      }
    }
    expect = {
      "Solar System": {
        "planets": [
          {
            "name": "MARS",
            "moons": [
              {
                "name": "PHOBOS",
                "craters": [
                  {
                    "name": "CLUSTRIL",
                    "diameter (km)": 3.4
                  },
                  {
                    "name": "D'ARREST",
                    "diameter (km)": 2.1
                  }
                ]
              },
              {
                "name": "DEIMOS",
                "craters": [
                  {
                    "name": "SWIFT",
                    "diameter (km)": 1
                  },
                  {
                    "name": "VOLTAIRE",
                    "diameter (km)": 1.9
                  }
                ]
              }
            ]
          },
          {
            "name": "JUPITER",
            "moons": [
              {
                "name": "AMALTHEA",
                "craters": [
                  {
                    "name": "GAEA",
                    "diameter (km)": 80
                  },
                  {
                    "name": "PAN",
                    "diameter (km)": 100
                  }
                ]
              },
              {
                "name": "CALLISTO",
                "craters": [
                  {
                    "name": "ADAL",
                    "diameter (km)": 41.7
                  },
                  {
                    "name": "AEGIR",
                    "diameter (km)": 53.9
                  }
                ]
              }
            ]
          }
        ]
      }
    }
    keys = [
        [
            "Solar System",
            "planets",
            "*",
            "moons",
            "*",
            "craters",
            "*",
            "name"
        ],
        [
            "Solar System",
            "planets",
            "*",
            "moons",
            "*",
            "name"
        ],
        [
            "Solar System",
            "planets",
            "*",
            "name"
        ]
    ]

    def map_values(keys, funct, seq):
        def apply_funct2keys(item):
            for key in keys:
                set_value(key, funct(get_value(key, item)), item)
            return item
        result = list(map(apply_funct2keys, seq))
        return result

    def capitalize(keys, data):
        return map_values(keys, str.upper, data)

    result = apply_funct(keys, capitalize, data)
    assert result == expect
