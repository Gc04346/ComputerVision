import numpy as np

from utils import Utils, G_MAX, GRAYSCALE_IMAGE
import cv2 as cv


class FormulationOne:
    def __init__(self, filepath, threshold=None):
        """
        Defines the image the formulation will be working with. If no image (or an invalid image) was passed as a
         parameter, the code gets a random one from the imgs/good_for_binarization directory.
        :param filepath: Path to the desired image
        :param threshold: (Optional) Threshold value.
        """
        image = Utils.load_image(filepath)
        if image is None:
            if filepath is None:
                print('No filepath was provided. We\'ll get a random image for you...')
            else:
                print('The filepath provided was invalid. We\'ll get a random image for you instead.')
            image = Utils.load_random_image('../imgs/good_for_binarization')
        self.image = image
        print('\nPreparing image...\n')
        self.t, self.binary_image = Utils.thresholding_operation(self.image, threshold)
        print('Done!\n')

    def execute(self):
        while True:
            input_option = input('Select one of the following:\n(1) Counting Components;\n(2) Geometric Features of a Selected Component;\n(3) Exit.\nSelected option: ')
            if input_option == str(1):
                (ret, cnts) = cv.findContours(self.binary_image.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                idx = 0
                for c in cnts:
                    x, y, w, h = cv.boundingRect(c)
                    if w > 50 and h > 50:
                        idx += 1
                        new_img = self.binary_image[y:y + h, x:x + w]
                        cv.imwrite(str(idx) + '.png', new_img)
                cv.imshow("im", new_img)
                cv.waitKey(0)
                cv.destroyAllWindows()
            elif input_option == str(2):
                print('you are so beautiful')
            elif input_option == str(3):
                print('\nSuspending program execution. See you!\n')
                break
            else:
                print('\nInvalid option!\n')

    def show_binary_image(self):
        cv.imshow(f'Resulting image for threshold T={self.t}', self.binary_image)
        cv.waitKey(0)
        cv.destroyAllWindows()
