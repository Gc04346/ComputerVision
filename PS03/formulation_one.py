import numpy as np

from utils import Utils, G_MAX, SigmaFilter, GRAYSCALE_IMAGE
import cv2 as cv


class FormulationOne:
    def __init__(self, filepath):
        """
        Defines the image the formulation will be working with. If no image (or an invalid image) was passed as a
         parameter, the code gets a random one from the imgs/good_for_binarization directory.
        :param filepath: Path to the desired image
        """
        image = Utils.load_image(filepath)
        if image is None:
            image = Utils.load_random_image('../imgs/good_for_binarization')
        self.image = image

    def get_image(self):
        return self.image

    def get_image_shape(self):
        return self.image.shape
