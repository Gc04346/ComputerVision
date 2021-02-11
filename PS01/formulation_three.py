import cv2 as cv
import numpy as np
import cmath
from matplotlib import pyplot as plt
from utils import Utils, MAX_RANGE, GRAYSCALE_IMAGE

"""
        lenna = Utils.load_lenna_image(GRAYSCALE_IMAGE)
        frequency_lenna = np.fft.fft2(lenna)
        fshift_lenna = np.fft.fftshift(frequency_lenna)
        magnitude_spectrum = 20 * np.log(np.abs(fshift_lenna))

        plt.subplot(121), plt.imshow(lenna, cmap='gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        plt.show()
"""


class FormulationThree:
    @staticmethod
    def one():
        lenna = Utils.load_lenna_image(GRAYSCALE_IMAGE)
        frequency_lenna = Utils.get_image_in_frequency_domain(lenna)

        # pega as coordenadas polares da lenna (amplitude, fase)
        lenna_polar = [
            [cmath.polar(complex_number) for _, complex_number in enumerate(complex_group)]
            for _, complex_group in enumerate(frequency_lenna)
        ]

        # faz o mesmo que fez pro baboon
        baboon = Utils.load_baboon_image(GRAYSCALE_IMAGE)
        frequency_baboon = Utils.get_image_in_frequency_domain(baboon)
        baboon_polar = [
            [cmath.polar(complex_number) for _, complex_number in enumerate(complex_group)]
            for _, complex_group in enumerate(frequency_baboon)
        ]

        # a imagem resultante pega a amplitude da primeira imagem com a fase da segunda. por isso os indices 0 e 1 res-
        # pectivamente no complex_number que representa a imagem da lenna e no baboon_polar
        resulting_image = [
            [cmath.rect(complex_number[0], baboon_polar[i][j][1]) for j, complex_number in enumerate(complex_group)]
            for i, complex_group in enumerate(lenna_polar)
        ]
        resulting_image = Utils.get_image_in_spatial_domain(resulting_image)
        cv.imshow('Resulting image', resulting_image)
        cv.waitKey(0)
        cv.destroyAllWindows()

