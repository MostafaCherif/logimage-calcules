from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import solveur
from threading import Thread, Event
from typing import Tuple
import os


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

    # Convert to small image
    res = img_PIL.resize(output_size, Image.BILINEAR)

    # Save output image

    # TODO: delete the test folder at the closure of the app

    name = original_image_path[-4]

    path = name + "/test"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    filename = name + "/test/" + f'_{output_size[0]}x{output_size[1]}.jpg'
    if res.mode in ("RGBA", "P"): res = res.convert("RGB")
    res.save(filename)

    enhancer = ImageEnhance.Contrast(res)
    factor = 1.5  # increase contrast
    im_output = enhancer.enhance(factor)
    im_output.save(filename)

    # Convert to black, gray and white

    imgmtplt = mpimg.imread(filename)

    R, G, B = imgmtplt[:, :, 0], imgmtplt[:, :, 1], imgmtplt[:, :, 2]
    imgGray = 0.2989 * R + 0.5870 * G + 0.1140 * B

    # Inequality reversed because 255 is considered as white
    imgThreshold = imgGray < threshold
    return imgThreshold


if __name__ == "__main__":
    # Aled
    # Pixelisation

    image = 'test.jpg'

    img_PIL = Image.open(image)

    threshold = 190
    i_size = (48, 48)
    o_size = img_PIL.size

    # open file
    img = Image.open(image)

    # convert to small image
    res = img.resize(i_size, Image.BILINEAR)

    # resize to output size
    #res=small_img.resize(img.size, Image.NEAREST)

    # Save output image
    name = image[-4]
    filename = name+'_{i_size[0]}x{i_size[1]}.jpg'
    res.save(filename)

    enhancer = ImageEnhance.Contrast(res)
    factor = 1.5  # increase contrast
    im_output = enhancer.enhance(factor)
    im_output.save(filename)

    # Display images side by side
    plt.figure(figsize=(16, 10))
    plt.subplot(2, 2, 1)
    plt.title('Original image', size=10)
    plt.imshow(img)  # display image
    plt.axis('off')  # hide axis
    plt.subplot(2, 2, 2)
    plt.title(f'Pixel Art {i_size[0]}x{i_size[1]}', size=10)
    plt.imshow(im_output)
    plt.axis('off')
    # plt.show()

    '''im_grayscale = im_output.convert("L")
    
    # Detecting Edges on the Image using the argument ImageFilter.FIND_EDGES
    im_edge = im_grayscale.filter(ImageFilter.FIND_EDGES)

    im_cropped = im_edge.crop((1, 1, i_size[0] - 1, i_size[1] - 1))
    
    im_invert = ImageOps.invert(im_cropped)

    im_invert.save('./test/test.jpg')'''

    # Transformer l'image en nuances de gris

    imgmtplt = mpimg.imread(filename)

    R, G, B = imgmtplt[:, :, 0], imgmtplt[:, :, 1], imgmtplt[:, :, 2]
    imgGray = 0.2989 * R + 0.5870 * G + 0.1140 * B

    '''imgGray = mpimg.imread('./test/test.jpg')'''

    plt.subplot(2, 2, 3)
    plt.title(f'Pixel Art grayscale', size=10)
    plt.imshow(imgGray, cmap='gray')
    plt.axis('off')
    # plt.show()

    # Transformer l'image en noir et blanc avec un seuil (threshold)

    imgThreshold = imgGray > threshold

    plt.subplot(2, 2, 4)
    plt.title(f'Pixel Art black and white 180', size=10)
    plt.imshow(imgThreshold, cmap='gray')
    plt.axis('off')
    plt.show()

    # Image to nonogram list

    # solveur

    (ROW_VALUES, COL_VALUES) = ImgToLogimage(imgThreshold)
    logimage_une_solution()

    # en plus beau

    n_col = len(ROW_VALUES)
    n_row = len(COL_VALUES)

    ROWS = [" ".join(map(str, l)) for l in ROW_VALUES]
    COLS = ["\n".join(map(str, l)) for l in COL_VALUES]
    cell_text = [[" " for i in range(n_row)] for j in range(n_col)]

    print(ROWS)
    print(COLS)

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    fig, axs = plt.subplots(1, 1)
    axs.axis("tight")
    axs.axis("off")
    the_table = axs.table(cellText=cell_text, rowLabels=ROWS,
                          rowLoc="right", colLabels=COLS, loc='center')
    cellDict = the_table.get_celld()
    longueurs_col = [len(e) for e in COLS]
    max_col = max(longueurs_col)
    print(max_col)
    for k in range(n_row):
        cellDict[(0, k)].set_height(0.03*max_col)
    plt.show()
