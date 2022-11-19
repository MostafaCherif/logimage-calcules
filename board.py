from typing import List, Tuple
import numpy as np
from numpy.typing import NDArray
from exceptions import *
import random as rd


class Board:
    def __init__(self, height: int = None, width: int = None, data: NDArray = None):
        if height is None or width is None:
            if data is None:
                raise ValueError(
                    "Building a board requires providing either its width and its height, or its initial data.")
            else:
                height, width = data.shape
        elif data is None:
            data = np.ones(shape=(height, width))
            data *= -1
            data = data.astype(int)

        self.height = height
        self.width = width
        self.data = data

    def draw(self):
        total_to_print = " " + "-" * (2*self.width + 1)
        for row in range(self.height):
            line_to_print = "| "
            for column in range(self.width):
                if self.data[row][column] == 1:
                    line_to_print += "X "
                else:
                    line_to_print += "  "
            line_to_print += "|"

            total_to_print += "\n" + line_to_print
        total_to_print += "\n" + " " + "-" * (2*self.width + 1)

        print(total_to_print)

    def set_square(self, h_coord: int, w_coord: int, value: int) -> None:
        """
        Sets the value of the square of coordinates (`h_coord`, `w_coord`) to `value`.
        If a 0 is replaced by a 1 or a 1 is replaced by a 0, raises `NoSolutionError` to stop the current search.
        """
        if (self.data[h_coord, w_coord] == 1 and value == 0) or (self.data[h_coord, w_coord] == 0 and value == 1):
            raise NoSolutionError
        self.data[h_coord, w_coord] = value

    def find_first_empty_square(self) -> Tuple[int, int]:
        data = self.data
        if len(data) == 0:
            raise ValueError(
                "Trying to find an empty square in an empty board, which is nonsense.")
        for i, j in np.ndindex(data.shape):
            if data[i, j] == -1 or abs(data[i, j] + 1) < 1e-3:
                return (i, j)
        return (None, None)

    def find_random_empty_square(self) -> Tuple[int, int]:
        """Extremely slow!"""
        data = self.data
        if len(data) == 0:
            raise ValueError(
                "Trying to find an empty square in an empty board, which is nonsense.")
        if not(-1 in data):
            return (None, None)
        while True:
            i = rd.randint(0, self.height - 1)
            j = rd.randint(0, self.width - 1)
            if data[i, j] == -1 or abs(data[i, j] + 1) < 1e-3:
                return (i, j)

    def find_border_empty_square(self) -> Tuple[int, int]:
        data = self.data
        if len(data) == 0:
            raise ValueError(
                "Trying to find an empty square in an empty board, which is nonsense.")
        for i in range(self.height):
            if data[i, 0] == -1:
                return (i, 0)
        for j in range(1, self.width):
            if data[0, j] == -1:
                return (0, j)
        for i in range(1, self.height):
            for j in range(1,self.width):
                if data[i, j] == -1:
                    return (i, j)
        return (None, None)

    def find_random_border_empty_square(self) -> Tuple[int, int]:
        data = self.data
        if len(data) == 0:
            raise ValueError(
                "Trying to find an empty square in an empty board, which is nonsense.")
        if not(-1 in data):
            return (None, None)
        available_squares_in_border = []
        for i in range(self.height):
            if data[i, 0] == -1:
                available_squares_in_border.append((i, 0))
        for j in range(1, self.width):
            if data[0, j] == -1:
                available_squares_in_border.append((0, j))
        
        if available_squares_in_border != []:
            return rd.choice(available_squares_in_border)

        while True:
            i = rd.randint(1, self.height - 1)
            j = rd.randint(1, self.width - 1)
            if data[i, j] == -1 or abs(data[i, j] + 1) < 1e-3:
                return (i, j)
        