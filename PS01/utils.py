import sys
from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np

MAX_RANGE = 255
GRAYSCALE_IMAGE = 0


class Utils:

    @staticmethod
    def load_lenna_image(grayscale=None):
        img = cv.imread('../imgs/lenna.png', grayscale)
        if img is None:
            sys.exit('Lenna não carregou corretamente')
        return img

    @staticmethod
    def load_baboon_image(grayscale=None):
        img = cv.imread('../imgs/baboon.png', grayscale)
        if img is None:
            sys.exit('Baboon não carregou corretamente')
        return img

    @staticmethod
    def show_histogram(img):
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histr = cv.calcHist([img], [i], None, [MAX_RANGE + 1], [0, MAX_RANGE + 1])
            plt.plot(histr, color=col)
            plt.xlim([0, MAX_RANGE + 1])
        plt.show()

    @staticmethod
    def get_intensity_value(blue, green, red):
        return round(sum([blue, green, red]) / 3, 3)

    @staticmethod
    def mean_filter(im):
        img = im
        w = 2

        for i in range(2, im.shape[0] - 2):
            for j in range(2, im.shape[1] - 2):
                block = im[i - w:i + w + 1, j - w:j + w + 1]
                m = np.mean(block, dtype=np.float32)
                img[i][j] = int(m)
        return img
