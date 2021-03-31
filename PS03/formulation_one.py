from typing import List, Tuple, Set

import numpy as np

from utils import Utils, G_MAX, GRAYSCALE_IMAGE, BLACK, WHITE
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
            # input_option = input('Select one of the following:\n(1) Counting Components;\n(2) Geometric Features of a Selected Component;\n(3) Exit.\nSelected option: ')
            input_option = str(1)
            if input_option == str(1):
                # recursive_adjacency = input('Now, please select (4), for black<white or (8), for white<black.\nSelected option: ')
                adjacency = 4
                self.count_components(adjacency)
            elif input_option == str(2):
                print('you are so beautiful')
            elif input_option == str(3):
                print('\nSuspending program execution. See you!\n')
                break
            else:
                print('\nInvalid option!\n')
            break

    def count_components(self, adjacency):
        visited_pixels: Set[Tuple[int, int]] = set()
        number_of_regions: int = 0
        img = self.binary_image
        shape = img.shape
        print(f'Starting counting algorithm. We will visit {shape[0]*shape[1]} pixels.')
        for x, values in enumerate(img):
            for y, value in enumerate(values):
                if (x, y) in visited_pixels:
                    continue
                # Utils.recursive_adjacency(img, (x, y), visited_pixels, int(adjacency))
                Utils.regular_adjacency(img, (x, y), visited_pixels, int(adjacency))
                number_of_regions += 1

        print(f'We have {number_of_regions} black regions.')
        print(f'The algorithm has visited {len(visited_pixels)} pixels in total.')

    def show_binary_image(self):
        cv.imshow(f'Resulting image for threshold T={self.t}', self.binary_image)
        cv.waitKey(0)
        cv.destroyAllWindows()
