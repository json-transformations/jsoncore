from jsoncore.apply import apply_funct, group_arrays, splitlist


def test_splitlist():
    data = [
        'Solar System', 'planets', '*', 'moons', '*', 'craters', '*', 'name'
    ]
    expect = [['Solar System', 'planets'], ['moons'], ['craters'], ['name']]
    result = splitlist(data)
    assert result == expect


def test_group_arrays():
    data = [
        ['Solar System', 'planets', 'number'],
        ['Solar System', 'planets', '*', 'moons', '*', 'craters', '*', 'name'],
        ['Solar System', 'planets', '*', 'moons', '*', 'craters', '*', 'size'],
    ]
    expect = [
        (
            (['Solar System', 'planets'], ['moons'], ['craters']),
            (['name'], ['size'])
        ), (
            (),
            (['Solar System', 'planets', 'number'],))
    ]

    result = group_arrays(data)
    assert result == expect


def test_apply_funct():
    def map_values(keys, funct, data):
        return [{k: funct(v) if k in keys else v for k, v in i.items()}
                for i in data]

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
                  {"name": "Clustril", "diameter (km)": 3.4},
                  {"name": "D'Arrest", "diameter (km)": 2.1}
                ]
              }, {
                "name": "Deimos",
                "craters": [
                  {"name": "Swift", "diameter (km)": 1},
                  {"name": "Voltaire", "diameter (km)": 1.9}
                ]
              }
            ]
          }, {
            "name": "Jupiter",
            "moons": [
              {
                 "name": "Amalthea",
                 "craters": [
                    {"name": "Gaea", "diameter (km)": 80},
                    {"name": "Pan", "diameter (km)": 100}
                 ]
              }, {
                "name": "Callisto",
                "craters": [
                  {"name": "Adal", "diameter (km)": 41.7},
                  {"name": "Aegir", "diameter (km)": 53.9}
                ]
              }
            ]
          }
        ]
      }
    }
    arrays = [('Solar System', 'planets'), ('moons',), ('craters',), ['name']]
    result = apply_funct(capitalize, arrays, data)
    print(result)
    expect = {
      "Solar System.planets": [
          {
            "name": "Mars",
            "moons": [
              {
                "name": "Phobos",
                "craters": [
                  {"name": "Clustril", "diameter (km)": 3.4},
                  {"name": "D'Arrest", "diameter (km)": 2.1}
                ]
              }, {
                "name": "Deimos",
                "craters": [
                  {"name": "Swift", "diameter (km)": 1},
                  {"name": "Voltaire", "diameter (km)": 1.9}
                ]
              }
            ]
          }, {
            "name": "Jupiter",
            "moons": [
              {
                 "name": "Amalthea",
                 "craters": [
                    {"name": "Gaea", "diameter (km)": 80},
                    {"name": "Pan", "diameter (km)": 100}
                 ]
              }, {
                "name": "Callisto",
                "craters": [
                  {"name": "Adal", "diameter (km)": 41.7},
                  {"name": "Aegir", "diameter (km)": 53.9}
                ]
              }
            ]
          }
        ]
    }


'''
data = [
    [('Solar System', 'planets'), ('moons'), ('craters'), ['name']],
    [('Solar System', 'planets'), ('moons'), ('craters'), ['size']],
    [('Solar System', 'planets', 'number')]
]


expect = [
    [[['Solar System', 'planets'], ['moons'], ['craters']],
     [['name'],['size']]],
    [['Solar System', 'planets', 'number']]
]
'''
