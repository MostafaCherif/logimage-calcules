from board import Board
from typing import List, Tuple
from utils import check_dim, get_following_values, currently_satisfied_constraints
from copy import deepcopy
from exceptions import *
from tqdm import tqdm
import numpy as np


class Logimage:

    def __init__(self, left_constraints: List[List[int]] = None, top_constraints: List[List[int]] = None):
        if left_constraints is None:
            left_constraints = []
        if top_constraints is None:
            top_constraints = []
        self.height = len(left_constraints)
        self.width = len(top_constraints)
        self.left_constraints = left_constraints
        self.top_constraints = top_constraints

    def is_fillable(self, board: Board, research_function=Board.find_border_empty_square) -> Tuple[bool, Board]:
        (h, w) = research_function(board)
        if h is None:
            if self.is_solution(board):
                return (True, board)
            else:
                return (False, None)
        else:
            FIRST_VALUE = 1
            SECOND_VALUE = 0
            # There was a try to fine-tune these values according to the constraints, but it wasn't successful
            # as a 1 provides much more information than a 0.

            # We first try to fill the square
            try:
                board_with_fill_1 = deepcopy(board)
                board_with_fill_1.set_square(h, w, FIRST_VALUE)
                self.surely_fill_empty_squares(board_with_fill_1)
                is_f, sol = self.is_fillable(
                    board_with_fill_1, research_function)
                if is_f:
                    return (True, sol)
                else:
                    raise NoSolutionError
            except NoSolutionError:
                # So now we try to put a blank square
                try:
                    board_with_fill_0 = deepcopy(board)
                    board_with_fill_0.set_square(h, w, SECOND_VALUE)
                    self.surely_fill_empty_squares(board_with_fill_0)
                    is_f, sol = self.is_fillable(
                        board_with_fill_0, research_function)
                    if is_f:
                        return True, sol
                    else:
                        return (False, None)
                except NoSolutionError:
                    # Now, the only possibility is that the board given in entry is false
                    return (False, None)

    def solve(self, research_function=Board.find_border_empty_square) -> Board:
        empty_board = Board(height=self.height, width=self.width)
        is_f, sol = self.is_fillable(empty_board, research_function)
        if is_f:
            return sol
        else:
            raise ValueError(
                "Tried (and failed) to solve a logimage with no solution.")

    def check_for_multiple_solutions(self, trial_count=10):
        print("Naturally solving the logimage...")
        initial_solution = self.solve()
        print("Try to find a different solution...")
        for trial in tqdm(range(trial_count)):
            sol = self.solve(
                research_function=Board.find_random_border_empty_square)
            if not(np.array_equal(sol.data, initial_solution.data)):
                print("\nTwo different solutions were found.")
                return False
        return True

    def surely_fill_empty_squares(self, board: Board) -> None:
        # When the first square of a row is filled, fill the next squares according to the constraint
        for i, left_constraint in enumerate(self.left_constraints):
            if len(left_constraint) == 0:  # Blank row
                for j in range(self.width):
                    board.set_square(i, j, 0)
            else:
                constraint = left_constraint[0]
                if board.data[i, 0] == 1 or constraint == self.width:
                    for j in range(constraint):
                        board.set_square(i, j, 1)
                    if constraint < self.width:
                        board.set_square(i, constraint, 0)

        # When the first square of a column is filled, fill the next squares according to the constraint
        for j, top_constraint in enumerate(self.top_constraints):
            if len(top_constraint) == 0:  # Blank column
                for i in range(self.height):
                    board.set_square(i, j, 0)
            else:
                constraint = top_constraint[0]
                if board.data[0, j] == 1 or constraint == self.height:
                    for i in range(constraint):
                        board.set_square(i, j, 1)
                    if constraint < self.height:
                        board.set_square(constraint, j, 0)

        # When the maximum count of filled squares is reached in a row, fill the next squares with 0
        for i, left_constraint in enumerate(self.left_constraints):
            sum_constraints = sum(left_constraint)
            for j in range(self.width):
                if sum_constraints <= 0:
                    board.set_square(i, j, 0)
                if board.data[i, j] == 1:
                    sum_constraints -= 1

        # When the maximum count of filled squares is reached in a column, fill the next squares with 0
        for j, top_constraint in enumerate(self.top_constraints):
            sum_constraints = sum(top_constraint)
            for i in range(self.height):
                if sum_constraints <= 0:
                    board.set_square(i, j, 0)
                if board.data[i, j] == 1:
                    sum_constraints -= 1

        # Fill rows and columns where a constraint is partially satisfied

        for i, left_constraint in enumerate(self.left_constraints):
            for j in range(self.width):
                if board.data[i, j] == -1:
                    should_be_continued, n = get_following_values(
                        left_constraint, board.data[i], index=j)
                    if should_be_continued:
                        for k in range(n):
                            if j + k < self.width:
                                board.set_square(i, j + k, 1)
                    else:
                        board.set_square(i, j, 0)
                    break

        for j, top_constraint in enumerate(self.top_constraints):
            for i in range(self.height):
                if board.data[i, j] == -1:
                    should_be_continued, n = get_following_values(
                        top_constraint, board.data[:, j], index=i)
                    if should_be_continued:
                        for k in range(n):
                            if i + k < self.height:
                                board.set_square(i + k, j, 1)
                    else:
                        board.set_square(i, j, 0)
                    break

        # When the maximum count of empty squares is reached in a row, fill the next square with 1
        for i, left_constraint in enumerate(self.left_constraints):
            sum_constraints = sum(left_constraint)
            min_space_taken = sum_constraints + len(left_constraint) - 1
            for j in range(self.width):
                if board.data[i, j] != 0:
                    return  # nothing can be concluded
                if self.width - j <= min_space_taken:
                    board.set_square(i, j, 1)
                    self.surely_fill_empty_squares(board)  # recursive call

        # When the maximum count of empty squares is reached in a column, fill the next square with 1
        for j, top_constraint in enumerate(self.top_constraints):
            sum_constraints = sum(top_constraint)
            min_space_taken = sum_constraints + len(top_constraint) - 1
            for i in range(self.height):
                if board.data[i, j] != 0:
                    return  # nothing can be concluded
                if self.height - i <= min_space_taken:
                    board.set_square(i, j, 1)
                    self.surely_fill_empty_squares(board)  # recursive call

    def is_solution(self, board: Board) -> bool:
        """
        Checks whether the `Board` instance is a solution of the logimage `log`.
        """

        if self.height != board.height or self.width != board.width:
            print("Dimensions do not match.")
            print("Left constraints: ", self.left_constraints)
            print("Top constraints: ", self.top_constraints)
            print("Board: ")
            print(board.data)
            return False

        for i, constraint in enumerate(self.left_constraints):
            if not(check_dim(constraint, board.data[i])):
                return False
        for i, constraint in enumerate(self.top_constraints):
            if not(check_dim(constraint, board.data[:, i])):
                return False
        return True


def board_to_logimage(board: Board) -> Logimage:
    """
    Transposes a filled `Board` to the corresponding `Logimage`.
    """
    left_constraints = []
    top_constraints = []
    height, width = board.data.shape
    for i in range(height):
        left_constraints.append(
            currently_satisfied_constraints(board.data[i])[0])
    for j in range(width):
        top_constraints.append(
            currently_satisfied_constraints(board.data[:, j])[0])
    return Logimage(left_constraints=left_constraints, top_constraints=top_constraints)
