import cmath
import math
import sys
from random import randint
from typing import Tuple

from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np

G_MAX = 255
GRAYSCALE_IMAGE = 0


class Utils:

    @staticmethod
    def load_image(filename: str, grayscale=GRAYSCALE_IMAGE):
        return cv.imread(f'{filename}', grayscale)

    @staticmethod
    def load_random_image(filepath: str, grayscale=GRAYSCALE_IMAGE):
        """
        Gets a random image from the directory passed as a parameter
        :param filepath: directory with the images
        :param grayscale: indicates if the image should be returned as a grayscale
        :return: random image
        """
        from os import listdir
        from os.path import isfile, join
        images = [f for f in listdir(filepath) if isfile(join(filepath, f))]
        random_index = randint(0, len(
            images) - 1)  # randint is inclusive on the latter index, which could cause index errors
        return cv.imread(f'{filepath}/{images[random_index]}', grayscale)

    @staticmethod
    def thresholding_operation(image, threshold=None) -> Tuple[int, int]:
        """
        Returns the input image binarized, using a simple threshold algorithm.
        :param image: Input image.
        :param threshold: Optional. If no value is provided, a random one between 1 and G_MAX will be used.
        :return: Threshold value and the resulting binary image
        """
        img_j = np.zeros(image.shape, dtype=np.uint8())
        if not threshold:
            threshold = randint(1, G_MAX)

        for x, values in enumerate(image):
            for y, value in enumerate(values):
                img_j[x][y] = G_MAX if image[x][y] < threshold else 0
        return threshold, img_j

    @staticmethod
    def sliding_window(image, step, window_size):
        """
        Sliding windows algorithm based on the algorithm by Chanran Kim at: https://stackoverflow.com/questions/61051120/sliding-window-on-a-python-image
        :param image: Image I
        :param step: defines pixel step. 1 indicates a pixel by pixel sliding window
        :param window_size: size of the window. send 2k+1
        :return: windows one by one with yield
        """
        for y in range(0, image.shape[0], step):
            for x in range(0, image.shape[1], step):
                yield x, y, image[y:y + window_size[1], x:x + window_size[0]]
