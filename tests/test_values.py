from jsoncore.core import jsonvalues

SAMPLE_DATA = [
    {"name": "Ryugu", "type": "Cg", "value $": 82760000000},
    {"name": "1989 ML", "type": "X", "value $": 13940000000}
]

EXPECTED_RESULT = ['Ryugu', 'Cg', 82760000000, '1989 ML', 'X', 13940000000]


def test_jsonvalues():
    assert set(jsonvalues(SAMPLE_DATA)) == set(EXPECTED_RESULT)
