import random

import numpy as np

import cv2 as cv


class FormulationTwo:

    def run(self, image_path, sp_val=12, sr_val=19, l_val=2):
        image = cv.imread(image_path)
        image_name = image_path.split('/')[-1].split('.')[0].capitalize()
        criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
        shifted_image = self.mean_shift(image, sp_val, sr_val, l_val, criteria)
        cv.imshow(f'{image_name}, shifted at sp={sp_val}, sr={sr_val} and l={l_val}', shifted_image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    @staticmethod
    def mean_shift(image, sp_val, sr_val, l_val, criteria):
        shifted_image = image.copy()
        cv.pyrMeanShiftFiltering(image, dst=shifted_image, sp=sp_val, sr=sr_val, maxLevel=l_val, termcrit=criteria)
        # FormulationTwo.colour_segments(shifted_image)
        return shifted_image

    @staticmethod
    def colour_segments(shifted_image):
        height, width = shifted_image.shape[:2]
        # mask has to be 2 pixels larger than the image itself
        mask = np.zeros((height + 2, width + 2), np.uint8)
        for x, line in enumerate(shifted_image):
            for y, pos in enumerate(line):
                # if mask[x+1][y+1] == 0:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                cv.floodFill(shifted_image, mask, (x, y), color)
        return shifted_image
