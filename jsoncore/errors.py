class JsonCutError(Exception):
    """JSON Cut Base Exception."""


class KeyNumberOutOfRange(JsonCutError, ValueError):
    """Invalid Key-Number."""

    pass
