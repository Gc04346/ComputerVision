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

    @staticmethod
    def get_image_in_frequency_domain(image, dp_shifted: bool = True):
        frequency_img = np.fft.fft2(image)
        if dp_shifted:
            # deslocando o 00 para o centro
            frequency_img = np.fft.fftshift(frequency_img)
        return frequency_img

    @staticmethod
    def get_amplitude_and_phase_values_separately(window_freq) -> Tuple[np.uint8, np.uint8]:
        """
        Based on an input window Wp, gets the amplitude and phase values from the center pixel p.
        :param window_freq: current window_freq Wp
        :return: amplitude and phase values as integers
        """

        # default values for amplitude and phase
        amplitude, phase = (0, 0)

        # gets the center position of the current window
        window_shape = window_freq.shape
        center_pos_x = window_shape[0] // 2
        center_pos_y = window_shape[1] // 2

        # window_freq[center_pos_x][center_pos_y] returns a tuple. The approach I chose for separating this tuple con-
        #  taining a complex number into amplitude and phase values was to turn the tuple into a string and spliting it
        #  into two, based on the operator + or - of the complex number. Then i had to remove the parenthesis that re-
        #  mained from the tuple to make the conversion. For the imaginary part, i got the module of it with the abs()
        #  function. Both values were converted to np.uint8 before returning.
        str_val = str(window_freq[center_pos_x][center_pos_y])
        if '+' in str_val:
            amplitude, phase = str_val.split("+")
        elif '-' in str_val:
            amplitude, phase = str_val.split('-')
        return np.uint8(amplitude.replace('(','')), np.uint8(abs((complex(phase.replace(')','')))))


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
