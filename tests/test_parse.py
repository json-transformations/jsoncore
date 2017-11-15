import pytest

from jsoncore.parse import (
    parse_csv, parse_name, parse_keys, parse_number, parse_keylist
)


def test_parse_csv():
    data = 'key1.key2,key3'
    result = parse_csv(data)
    expect = ['key1.key2', 'key3']
    assert result == expect


def test_parse_csv_with_non_alphas():
    data = 'key1.key2, "key w/ non-alphanums", key3'
    result = parse_csv(data)
    expect = ['key1.key2', 'key w/ non-alphanums', 'key3']
    assert result == expect


def test_parse_csv_with_quotechar():
    data = "key1.key2, 'w/ non-alphanums', key3"
    result = parse_csv(data, quotechar="'")
    expect = ['key1.key2', 'w/ non-alphanums', 'key3']
    assert result == expect


def test_parse_key_name_with_dot():
    data = 'k\\.2'
    result = parse_name(data)
    expect = 'k.2'
    assert result == expect


def test_key_number_out_of_range():
    with pytest.raises(ValueError):
        keys = '2'
        data = ['i1']
        result = parse_number(keys, data)
        expect = [('i1',)]
        assert result == expect


def test_parse_key_number():
    keys = '1'
    data = ['i1', 'i1.i2', 'i1.i2.i3', 'i4']
    result = parse_number(keys, data)
    expect = [('i1',)]
    assert result == expect


def test_parse_key_range_no_upper_bound():
    keys = '2-'
    data = ['i1', 'i1.i2', 'i1.i2.i3', 'i4']
    result = parse_number(keys, data)
    expect = [('i1', 'i2'), ('i1', 'i2', 'i3'), ('i4',)]
    assert result == expect


def test_parse_key_range_no_lower_bound():
    keys = '-3'
    data = ['i1', 'i1.i2', 'i1.i2.i3', 'i4']
    result = parse_number(keys, data)
    expect = [('i1',), ('i1', 'i2'), ('i1', 'i2', 'i3')]
    assert result == expect


def test_parse_keys():
    keys = ['asteroids.0.name', 'asteroids.2:']
    result = [tuple(i) for i in parse_keys(keys)]
    expect = [('asteroids', 0, 'name'), ('asteroids', slice(2, None))]
    print(result)
    assert result == expect


def test_parse_keylist():
    keys = 'asteroids.0.name,asteroids.2:'
    result = parse_keylist(keys)
    expect = [('asteroids', 0, 'name'), ('asteroids', slice(2, None))]
    assert result == expect


def test_parse_keylist_with_range():
    keynums = '1-3,5'
    keys = ['red', 'blu', 'grn', 'blk', 'yel']
    result = parse_keylist(keynums, keys=keys)
    expect = [('red',), ('blu',), ('grn',), ('yel',)]
    assert result == expect


def test_parse_keystr():
    pass
