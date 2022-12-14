from PIL import Image
import numpy as np
from numpy.typing import NDArray
from typing import Tuple
from board import Board
import nonogram


def grayscale_img(path_to_image: str) -> Image:
    return Image.open(path_to_image).convert('L')


def resize_img(img: Image, new_min_side: int = 200):
    """
    Resizes the image `img` so that its shortest side gets a new length of `new_min_size`.

    Args:
    `img`: an instance of `PIL.Image`
    `new_min_side`: The new length of the shortest side, in pixels.

    Returns a copy of the resized image.
    """
    current_height, current_width = img.size
    scale_factor = new_min_side / min(current_height, current_width)
    return img.resize((int(current_height * scale_factor), int(current_width * scale_factor)))


def to_board(array: NDArray, threshold: int = 128) -> Board:
    """
    Converts a 2-dimensional np.array featuring an image to a newarray with only 0s and 1s.
    The limit between 0 and 1 is given by `threshold`.

    Examples:
    np.array([[252, 153], [148, 112]]), threshold = 128 -> np.array([[1, 1], [1, 0]])
    np.array([[252, 153], [148, 112]]), threshold = 192 -> np.array([[1, 0], [0, 0]])
    """

    # Because white is classified as 255 in black & white scale
    arr = np.less(array, threshold*np.ones(array.shape)).astype(int)
    return Board(data=arr)


if __name__ == "__main__":
    img = grayscale_img("./images/chien1.jpg")
    img = resize_img(img, (30, 30))
    arr = np.array(img)
    board = to_board(arr, 210)
    board.draw()
    log = nonogram.board_to_nonogram(board)
    board = log.solve()
    board.draw()
