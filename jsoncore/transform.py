'''
class JSONDict(object):
    """Access to environment variables using attribute-style notation."""

    def __init__(self, data):
        self.data = data
        self.keys = self.keys()
        self.ignore = (IndexError, KeyError)

    def get(self, key):
        """Get a value from a JSON document given a list of keys."""
        keys = parse_key(keys)
        return get_value(self.data, keys, ignore=self.ignore)

    def set(self, value):
        """Set a value in a JSON document given a list a keys."""
        return set_value(self.data, self.keys, value, ignore=self.ignore)

    def drop(d, keys, ignore=(IndexError, KeyError)):
        """Delete an item from a JSON document given a list of keys."""
        del_key(self.data, self.keys, ignore=self.ignore)

    def parent(self):
        return get_parent(self.data, self.keys)

    def values(self):
        return get_values(d)

    def keys(self):
        return sorted(get_keys(self.data))

    def items(self):
        return get_items(self.data)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(data)

    def __repr__(self):
        return repr(data)

    def __contains__(self, key):
        return key in self.data

    def __eq__(self, d):
        return self.data == d

    def __ne__(self, d):
        return self.data != d

    def items(self):
        return self.data.items()

    def keys(self):
        return self.data.keys()

    def pop(self, key):
        return self.data.pop(key)

    def popitem(self):
        return self.data.popitem()

    def update(self, d):
        self.data.update(d)

    def values(self):
        return self.data.values()

    def setdefault(self, key, d=None):
        self.data.setdefault(key, d)

    __getitem__ = __getattr__
    __setitem__ = __setattr__
    __delitem__ = __delattr__
'''
