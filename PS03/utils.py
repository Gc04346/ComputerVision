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
BLACK = 0
WHITE = 255
FOUR_ADJACENCY = 4
EIGHT_ADJACENCY = 8

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
    def thresholding_operation(image, threshold=None):
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
                img_j[x][y] = WHITE if image[x][y] < threshold else BLACK
        return threshold, img_j

    @staticmethod
    def recursive_adjacency(img, pixel: tuple, visited_pixels: set, adjacency):
        """

        :param img: input image
        :param pixel: tuple of coords (x, y)
        :param visited_pixels: list of visited pixels
        :param adjacency: indicates whether it is a 4 or 8 adjacency
        :return:
        """
        x, y = pixel
        eight_adjacency = [(x + 1, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                           (x, y + 1), (x + 1, y + 1)]
        four_adjacency = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if adjacency == FOUR_ADJACENCY:
            for x, y in four_adjacency:
                if (x, y) in visited_pixels:
                    continue
                try:
                    if img[x][y] == BLACK:
                        visited_pixels.add(pixel)
                        print(f'We have visited {len(visited_pixels)} so far.')
                        Utils.recursive_adjacency(img, (x, y), visited_pixels, adjacency)
                except IndexError:
                    pass
        else:
            for x, y in eight_adjacency:
                try:
                    if img[x][y] == BLACK:
                        visited_pixels.add(pixel)
                        print(f'We have visited {len(visited_pixels)} so far.')
                        Utils.recursive_adjacency(img, (x, y), visited_pixels, adjacency)
                except IndexError:
                    pass

    @staticmethod
    def regular_adjacency(img, pixel, visited_pixels: set, adjacency):
        x, y = pixel
        eight_adjacency = [(x + 1, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                           (x, y + 1), (x + 1, y + 1)]
        four_adjacency = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if (x, y) in visited_pixels:
            print(f'Pixel {(x,y)} already visited.')
            return
        if adjacency == FOUR_ADJACENCY:
            for posx, posy in four_adjacency:
                try:
                    if (posx, posy) not in visited_pixels:
                        visited_pixels.add((posx, posy))
                    if (
                        img[posx][posy] == BLACK
                        and (posx, posy) not in visited_pixels
                    ):
                        visited_pixels.add((posx, posy))
                        print(f'We have visited {len(visited_pixels)} so far.')
                except IndexError:
                    pass

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
