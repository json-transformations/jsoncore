from jsoncore.jsonfuncts import jsonkeys


def test_jsonkeys():
    data = {"status": "success", "message": {"affenpinscher": []}}
    expect = {('status',), ('message', 'affenpinscher'), (), ('message',)}
    result = set(jsonkeys(data))
    assert result == expect
