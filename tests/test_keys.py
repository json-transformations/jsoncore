'''
from jsoncore.jsonfuncts import jsonkeys


def test_jsonkeys():
    data = {"status": "success", "message": {"affenpinscher": []}}
    expect = {('status',), ('message', 'affenpinscher'), (), ('message',)}
    result = jsonkeys(data)
    assert expect == result
'''
