import numpy as np

from utils import Utils, G_MAX, SigmaFilter, GRAYSCALE_IMAGE
import cv2 as cv


class FormulationOne:
    @staticmethod
    def sigma_filter_then_histogram_equalization():
        noisy_lenna = Utils.load_image('noisy_imgs/noisy_lenna.jpg', GRAYSCALE_IMAGE)
        # A imagem tem o shape (width, height, 3). 3 eh os valores de rgb, que sao iguais no caso de uma imagem em
        #  escala de cinza.
        # noisy_araras = Utils.load_image('noisy_imgs/araras.ppm', GRAYSCALE_IMAGE)
        # noisy_sculpture = Utils.load_image('noisy_imgs/sculpture.jpg', GRAYSCALE_IMAGE)

        sigma_filter = SigmaFilter(k=1)
        new_img = sigma_filter.smooth_image(noisy_lenna)

        histogram_equalized_image = Utils.histogram_equalization(new_img)

        cv.imshow('Resulting image', new_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

