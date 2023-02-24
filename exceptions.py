class NoSolutionError(Exception):
    """Raised when a `Board`, even incomplete, cannot be the solution of a `Nonogram`."""
    pass


class NullNonogramError(Exception):
    """Raised while trying to solve a `Nonogram` being `None`."""
    pass


class MultipleSolutionsError(Exception):
    """Raised when trying to solve a `Nonogram` that has multiple solutions."""
    pass


class TimeoutError(Exception):
    """Raised when encountering a timeout while solving a `Nonogram`."""
    pass
