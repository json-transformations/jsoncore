from jsoncore.sequence import Items


def test_itemer():
    sequence = Items('item1')
    sequence.items = [i.upper() for i in sequence.items]
    assert sequence.value == 'ITEM1'

    sequence = Items(['item1', 'item2'])
    sequence.items = [i.upper() for i in sequence.items]
    assert sequence.value == ['ITEM1', 'ITEM2']
