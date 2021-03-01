import cmath
import math
import sys
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
        for i in range(G_MAX):
            total += math.pow(h[i], r)
        return total

    @staticmethod
    def histogram_equalization(image, r):
        h = None
        fraction = G_MAX / Utils.Q(r, h)

    @staticmethod
    def sliding_window(image, step, window_size):
        for y in range(0, image.shape[0], step):
            for x in range(0, image.shape[1], step):
                yield x, y, image[y:y + window_size[1], x:x + window_size[0]]

    @staticmethod
    def get_standard_deviation_of_window(window):
        mean = np.mean(window, dtype=np.float32)
        summation = 0.0
        for pixel in window:
            summation += pixel - mean
        sigma_squared = summation / 1
        return math.sqrt(sigma_squared)


class SigmaFilter:
    def __init__(self, k):
        self.k = k
        self.window_size = (2 * k) + 1
        self.J = np.zeros((300, 300, 1))

    def smooth_image(self, image):
        windows = Utils.sliding_window(image, 1, (self.window_size, self.window_size))
        for window in windows:
            p = (window[0], window[1])
            wp = window[2]
            sigma = int(wp.std())

            # Calculate the histogram of window Wp(I)
            histogram = cv.calcHist([wp], [0], None, [G_MAX + 1], [0, G_MAX + 1])

            # Calculate the mean mi of all values in the interval [I(p)-sigma, I(p)+sigma]
            S = 0.0
            summation = 0.0
            for val in range(-sigma, sigma):
                u = np.array(image[p] + val, dtype=np.uint8)
                h_u = histogram[u]
                # summation += u * (1/h_u)
                summation += 0 if h_u == 0 else u * (1/h_u)
                S += h_u
            # mi = np.divide(summation, S, out=np.zeros_like(summation), where=S != 0)
            mi = 0 if S == 0.0 else summation / S
            # Let J(p) = mi
            self.J[p] = mi
        return self.J
