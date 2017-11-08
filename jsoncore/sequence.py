"""Sequence an element or items & restore to its original type.

    >>> sequence = Items('item1')
    >>> sequence.items = [i.upper() for i in sequence.items]
    >>> sequence.value
    'ITEM1'

    >>> sequence = Items(['item1', 'item2'])
    >>> sequence.items = [i.upper() for i in sequence.items]
    >>> sequence.value
    ['ITEM1', 'ITEM2']
"""
from collections import Sequence
from copy import deepcopy

from ._compat import string_type, text_type


def is_seq_and_not_str(obj):
    """Exclude strings when determining whether an object is a Sequence."""
    return (isinstance(obj, Sequence) and
            not isinstance(obj, (string_type, text_type)))


class Items(object):
    """Wrap a string or non-sequence in a list."""

    def __init__(self, obj):
        """Wrap a string or non-Sequence in a list."""
        self.items = deepcopy(obj)
        self.is_str_or_not_sequence = not is_seq_and_not_str(obj)
        if self.is_str_or_not_sequence:
            self.items = [self.items]

    @property
    def value(self):
        """Unwrap if applicable; return the original object type."""
        if self.is_str_or_not_sequence:
            return self.items[0]
        return self.items
