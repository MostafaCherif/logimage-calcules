from board import Board
from typing import List, Tuple
from utils import check_dim, get_following_values, currently_satisfied_constraints
from copy import deepcopy
from tqdm import tqdm
import numpy as np
import solveur


class Nonogram:

    def __init__(self, left_constraints: List[List[int]] = None, top_constraints: List[List[int]] = None):
        if left_constraints is None:
            left_constraints = []
        if top_constraints is None:
            top_constraints = []
        self.height = len(left_constraints)
        self.width = len(top_constraints)
        self.left_constraints = left_constraints
        self.top_constraints = top_constraints

    def is_solution(self, board: Board) -> bool:
        """
        Checks whether the `Board` instance is a solution of the nonogram `log`.
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


    def solve(self):
        """
        Should return either the completed data (matrix of 0s and 1s / Board object) or None if there is no solution
        """

        # TODO
        s = solveur.NonogramSolver(self.left_constraints, self.top_constraints, "./test")
        if s.solved:
            print("Logimage successfully solved!")
            print("Saved at ./test")
        else:
            print("Zero or multiple solutions available :(")


def board_to_nonogram(board: Board) -> Nonogram:
    """
    Transposes a filled `Board` to the corresponding `Nonogram`.
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
    return Nonogram(left_constraints=left_constraints, top_constraints=top_constraints)
