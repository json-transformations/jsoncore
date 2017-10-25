class TransformationError(Exception):
    """JSON Cut Base Exception."""


class KeyNumError(TransformationError, ValueError):
    """Invalid Key-Number."""

    pass


class RegExError(TransformationError, TypeError):
    """Invalid Regular Expression."""

    pass
