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
    def a():
        lenna = Utils.load_image('lenna.png', GRAYSCALE_IMAGE)
        frequency_lenna = Utils.get_image_in_frequency_domain(lenna)

        # pega as coordenadas polares da lenna (amplitude, fase)
        lenna_polar = Utils.get_image_in_polar_coords(frequency_lenna)

        # faz o mesmo que fez pro baboon
        baboon = Utils.load_image('baboon.png', GRAYSCALE_IMAGE)
        frequency_baboon = Utils.get_image_in_frequency_domain(baboon)
        baboon_polar = Utils.get_image_in_polar_coords(frequency_baboon)

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

    @staticmethod
    def b():
        grass = Utils.load_image('grass.jpg', GRAYSCALE_IMAGE)
        cv.imshow('Grass - Amplitude divided by 2', grass)
        cv.waitKey(0)
        cv.destroyAllWindows()
        # night_sky = Utils.load_image('night_sky.jpg', GRAYSCALE_IMAGE)
        # tulips = Utils.load_image('tulips.jpg', GRAYSCALE_IMAGE)
        # water = Utils.load_image('water.jpg', GRAYSCALE_IMAGE)

        grass_frequency = Utils.get_image_in_frequency_domain(grass)
        # night_sky_frequency = Utils.get_image_in_frequency_domain(night_sky)
        # tulips_frequency = Utils.get_image_in_frequency_domain(tulips)
        # water_frequency = Utils.get_image_in_frequency_domain(water)

        grass_frequency_polar = Utils.get_image_in_polar_coords(grass_frequency)
        # night_sky_frequency_polar = Utils.get_image_in_polar_coords(night_sky_frequency)
        # tulips_frequency_polar = Utils.get_image_in_polar_coords(tulips_frequency)
        # water_frequency_polar = Utils.get_image_in_polar_coords(water_frequency)

        # dividindo a amplitude por 2
        for complex_group in grass_frequency_polar:
            transformed_coords = (complex_group[0][0] * 0.5, complex_group[0][1])
            complex_group[0] = transformed_coords
        # multiplicando a amplitude por -1
        # for complex_group in night_sky_frequency_polar:
        #     transformed_coords = (complex_group[0][0] * -1, complex_group[0][1])
        #     complex_group[0] = transformed_coords
        # # dividindo a fase por 2
        # for complex_group in tulips_frequency_polar:
        #     transformed_coords = (complex_group[0][0], complex_group[0][1] * 0.5)
        #     complex_group[0] = transformed_coords
        # # multiplicando a fase por -1
        # for complex_group in water_frequency_polar:
        #     transformed_coords = (complex_group[0][0], complex_group[0][1] * -1)
        #     complex_group[0] = transformed_coords

        grass_back = Utils.get_image_in_spatial_domain(grass_frequency_polar)
        # night_sky_back = Utils.get_image_in_spatial_domain(night_sky_frequency_polar)
        # tulips_back = Utils.get_image_in_spatial_domain(tulips_frequency_polar)
        # water_back = Utils.get_image_in_spatial_domain(water_frequency_polar)

        cv.imshow('Grass - Amplitude divided by 2', grass_back)
        # cv.imshow('Night Sky - Amplitude negative', night_sky_back)
        # cv.imshow('Tulips - Phase divided by 2', tulips_back)
        # cv.imshow('Water - Phase negative', water_back)
        cv.waitKey(0)
        cv.destroyAllWindows()
