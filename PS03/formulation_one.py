import numpy as np

from utils import Utils, G_MAX, GRAYSCALE_IMAGE
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
            if filepath is None:
                print('No filepath was provided. We\'ll get a random image for you...')
            else:
                print('The filepath provided was invalid. We\'ll get a random image for you instead.')
            image = Utils.load_random_image('../imgs/good_for_binarization')
        self.image = image

    def binarize_image(self, threshold=None):
        t, binary_img = Utils.thresholding_operation(self.image, threshold)
        cv.imshow(f'Resulting image for threshold T={t}', binary_img)
        cv.waitKey(0)
        cv.destroyAllWindows()
