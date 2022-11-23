from typing import List, Tuple
from numpy.typing import NDArray


def check_dim(constraints: List[int], board_extract: NDArray) -> bool:
    """
    Checks whether a line or column extracted from a `Board` respects the constraints.

    Args:
    - `constraints`: the constraints, for example [1, 3, 2].
    - `board_extract`: the extract from the board, where 1 corresponds to a full square, 0 to an empty square, and -1 to a square
    that is undetermined.

    Returns `True` if `board_extract_` contains only 0s and 1s and the constraints are satisfied.
    """
    if constraints == []:
        # with no constraints, all the squares should be blank
        return board_extract.tolist() == [0]*board_extract.size
    if board_extract.size == 0:
        return False
    elif board_extract[0] == 0:
        # recursive call
        return check_dim(constraints, board_extract[1:])
    elif board_extract[0] == 1:
        condition = True
        consecutive_1s = 1
        while condition:
            if consecutive_1s == len(board_extract):
                condition = False  # the whole extract is filled with 1s
            elif board_extract[consecutive_1s] == 1:
                consecutive_1s += 1
            else:
                condition = False  # we reached a 0 (or a -1)
        if constraints[0] == consecutive_1s:
            # recursive call
            return check_dim(constraints[1:], board_extract[consecutive_1s:])
        else:  # wrong count of full squares
            return False
    elif board_extract[0] == -1:
        print("Checking on a non-filled board extract.")
        return False  # corresponds to an undetermined case
    else:
        raise ValueError("A board should only contain the values -1, 0 or 1. But we found the value "
                         + str(board_extract[0]))


def currently_satisfied_constraints(board_extract: NDArray) -> Tuple[List[int], bool]:
    """
    Analyses the constraints currently satisfied by board_extract, and if a constraint is being partially satisfied.
    Examples: 
    - `board` = [X X X O X] -> `([3, 1], True)`
    - `board` = [X X X O X O] -> `([3, 1], False)`
    """
    res = []
    current_constraint = None
    for square in board_extract:
        if square == 1:
            current_constraint = 1 if current_constraint is None else current_constraint + 1
        else:
            if current_constraint is not None:
                res.append(current_constraint)
                current_constraint = None

    if current_constraint is not None:
        res.append(current_constraint)
        return (res, True)
    else:
        return (res, False)


def get_following_values(constraint_list: List[int], board_extract: NDArray, index: int = None) -> Tuple[bool, int]:
    """
    Returns whether the current sequence should be continued (and if yes, the number of 1s to add) or not.
    Examples :
    - `constraint_list` = [2, 4], `board` = [X X O X] -> `(True, 3)`
    - `constraint_list` = [2, 1], `board` = [X X O X] -> `(False, 0)`
    - `constraint_list` = [2, 1], `board` = [X X O] -> `(True, 0)` (no obligation to put a 0)
    """

    if index is None:
        for i, val in enumerate(board_extract):
            if val == -1:
                index = i
                break
    if index is None:
        return None

    satisfied_constraints, ongoing = currently_satisfied_constraints(
        board_extract[:index])
    if not ongoing:
        return (True, 0)

    for i in range(len(satisfied_constraints) - 1):
        # bad news: we already know that we wont't find a solution
        if satisfied_constraints[i] != constraint_list[i]:
            return (True, 100)
    try:
        current_constraint = satisfied_constraints[-1]
        expected_constraint = constraint_list[len(satisfied_constraints) - 1]
        if current_constraint == expected_constraint:
            return (False, 0)
        else:
            return (True, expected_constraint - current_constraint)
    except IndexError:
        print("Current_constraint: ", current_constraint)
        print("Constraint_list: ", constraint_list)
        print("Satisfied_constraints", satisfied_constraints)


def list_to_horizontal_str(list: List) -> str:
    """
    Converts a constraint list to a horizontal `str`.
    Returns "0" if the list of constraints is blank.

    Example : `[2, 5, 4, 8]` -> `"2 5 4 8"`
    """
    if list == []:
        return "0"
    return "  ".join(str(e) for e in list)


def list_to_vertical_str(list: List) -> str:
    """
    Converts a constraint list to a vertical `str`.

    Example : `[2, 5, 4, 8]` -> `"2\\n5\\n4\\n8"`
    """
    if list == []:
        return "0"
    return "\n".join(str(e) for e in list)
