from nonogram import Nonogram
from exceptions import NullNonogramError, MultipleSolutionsError, TimeoutError


def check_for_unique_solution_of_nonogram(nonogram: Nonogram, raise_errors: bool = True):
    if nonogram is None:
        if raise_errors:
            raise NullNonogramError
        return None

    try:
        one_solution = nonogram.solve()
        if not one_solution and raise_errors:
            raise MultipleSolutionsError
        return one_solution

    except Exception as e:
        if "timeout" in str(e):
            if raise_errors:
                raise TimeoutError
            return False
        else:
            print("Exception:")
            print(str(e))
            return None
