from tkinter.tix import ROW
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from IPython.display import clear_output
from itertools import combinations
import solveur
from threading import Thread, Event
from nonogram import Nonogram
from typing import Tuple


def preprocess_image(
    original_image_path: str = "test.jpg",
    threshold: int = 190,
    output_size: Tuple[int, int] = (24, 24)
):
    """
    Transforms the image whose path is given as argument to its black and white version relative to the threshold and the sizes.
    Args:
    `original_image_path`: the path of the original image (provided by the user)
    `threshold`: the black and white threshold (from 0 to 255)
    `output_size`: the size (in pixels) of the output image. Default is (24px, 24px)
    """

    # Open file

    img_PIL = Image.open(original_image_path)

    im_grayscale = img_PIL.convert("L")

    im_edge = im_grayscale.filter(ImageFilter.FIND_EDGES)

    # Convert to small image
    res = im_edge.resize(output_size, Image.BILINEAR)

    # Save output image
    name = original_image_path[-4]
    filename = name + f'_{output_size[0]}x{output_size[1]}.jpg'
    res.save(filename)

    enhancer = ImageEnhance.Contrast(res)
    factor = 1.5  # increase contrast
    im_output = enhancer.enhance(factor)
    im_output.save(filename)

    imgmtplt = mpimg.imread(filename)

    # Inequality reversed because 255 is considered as white
    imgThreshold = imgmtplt < threshold
    return imgThreshold


def ImgToLogimage(im):  # To rebuild, `im` is not used and `i_size` is undefined
    ROW_VALUES = []
    for row in range(i_size[1]):
        ROW_VALUES.append([])
        count = 0
        for el in imgThreshold[row]:
            if el:
                if count != 0:
                    ROW_VALUES[-1].append(count)
                    count = 0
            else:
                count += 1
        if count != 0:
            ROW_VALUES[-1].append(count)

    COL_VALUES = []
    for col in range(i_size[0]):
        count = 0
        COL_VALUES.append([])
        for row in range(i_size[1]):
            if imgThreshold[row][col]:
                if count != 0:
                    COL_VALUES[-1].append(count)
                    count = 0
            else:
                count += 1
        if count != 0:
            COL_VALUES[-1].append(count)

    '''ROW_VALUES.pop(0)
    COL_VALUES.pop(0)
    ROW_VALUES.pop()
    COL_VALUES.pop()'''

# Enlever les colonnes et les lignes vides

    while ROW_VALUES[0] == []:
        ROW_VALUES.pop(0)
    while COL_VALUES[0] == []:
        COL_VALUES.pop(0)
    while ROW_VALUES[-1] == []:
        ROW_VALUES.pop()
    while COL_VALUES[-1] == []:
        COL_VALUES.pop()

    # return Nonogram(ROW_VALUES, COL_VALUES)
    return (ROW_VALUES, COL_VALUES)

# solveur


def thresholdUp():
    global threshold
    threshold += 1
    imgT = imgGray > threshold
    (R, C) = ImgToLogimage(imgT)
    return (threshold, R, C)

# le logimage ainsi créé n'a pas forcément une seule solution, nous allons donc ajouter des cases jusqu'à ce que ça soit le cas


def solvable(r, c):
    s = solveur.NonogramSolver(r, c, "./test")
    return s.solved


def _solvable(r, c):
    action_thread = Thread(target=solvable(r, c))
    action_thread.start()
    action_thread.join(timeout=10)
    s = solveur.NonogramSolver(r, c, "./test")
    return s.solved


"""
def solvable(nonogram):
    s = solveur.NonogramSolver(nonogram,"./test")
    return s.solved
def _solvable(nonogram):
    action_thread = Thread(target=solvable(nonogram))
    action_thread.start()
    action_thread.join(timeout=10)
    s = solveur.NonogramSolver(nonogram,"./test")
    return s.solved
"""


def logimage_une_solution():
    global threshold
    global ROW_VALUES
    global COL_VALUES
    # global NONOGRAM
    if threshold < 256:
        print(threshold)
        # if not solvable(NONOGRAM):
        if not solvable(ROW_VALUES, COL_VALUES):
            threshold = thresholdUp()[0]
            ROW_VALUES = thresholdUp()[1]
            COL_VALUES = thresholdUp()[2]
            # NONOGRAM = Nonogram(ROW_VALUES, COL_VALUES)
            logimage_une_solution()
        else:
            print("Lesgo")
    print("Done")
