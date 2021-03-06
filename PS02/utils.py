import cmath
import math
import sys
from typing import Tuple

from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np

G_MAX = 255
GRAYSCALE_IMAGE = 0


class Utils:

    @staticmethod
    def load_image(filename: str, grayscale=None):
        img = cv.imread(f'../imgs/{filename}', grayscale)
        if img is None:
            sys.exit('A imagem não carregou corretamente')
        return img

    @staticmethod
    def Q(r, h):
        total = 0.0
        for w in range(G_MAX + 1):
            total += math.pow(h[w], r)
        return total

    @staticmethod
    def histogram_equalization(h, r, u):
        normalization_factor = G_MAX / Utils.Q(r, h)
        summation = 0.0
        for w in range(u + 1):
            summation += math.pow(h[w], r)
        return normalization_factor * summation  # g_r(u) = (Gmax/Q)*summation(h_i(u))

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


class SigmaFilter:
    def __init__(self, k: int, image_shape: Tuple[int, int, int]):
        self.k = k
        self.window_size = (2 * k) + 1
        self.J = np.zeros(image_shape, dtype=np.uint8())

    def apply_filter(self, image):
        print('Starting sigma filter algorithm.\n')
        # define the sliding windows
        windows = Utils.sliding_window(image, 1, (self.window_size, self.window_size))
        for window in windows:
            px = window[0]
            py = window[1]
            wp = window[2]
            sigma = int(wp.std())

            # Calculate the histogram of window Wp(I)
            histogram = cv.calcHist([wp], [0], None, [G_MAX + 1], [0, G_MAX + 1])

            # Initializing range control variables according to the image value range limits
            superior_limit = image[px][py] + sigma if image[px][py] + sigma <= G_MAX else G_MAX
            inferior_limit = image[px][py] - sigma if image[px][py] - sigma >= 0 else 0

            # Initializing cumulative variables for the inner for loop
            S = 0.0
            summation = 0.0
            # Calculate the mean mi of all values in the interval [I(p)-sigma, I(p)+sigma]
            for u in range(inferior_limit, superior_limit + 1):
                h_u = histogram[u]
                summation += u * h_u
                S += h_u
            mi = np.uint8(0) if S == 0.0 else np.uint8(summation / S)[0]
            self.J[px][py] = mi
        print('Sigma filter algorithm terminated.\n')
        return self.J
