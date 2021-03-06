import numpy as np

from utils import Utils, G_MAX, SigmaFilter, GRAYSCALE_IMAGE
import cv2 as cv


class FormulationOne:
    @staticmethod
    def sigma_filter_then_histogram_equalization(r):
        # get input image
        noisy_lenna = Utils.load_image('noisy_imgs/noisy_lenna.jpg', GRAYSCALE_IMAGE)
        # define image cardinality for posterior usage
        cardinality = noisy_lenna.shape[0]*noisy_lenna.shape[1]

        # instantiate and apply the sigma filter
        sigma_filter = SigmaFilter(k=1, image_shape=noisy_lenna.shape)
        sigma_filtered_img = sigma_filter.apply_filter(noisy_lenna)

        # get the relative frequencies of the image obtained with the sigma filter application (H/omega)
        h = cv.calcHist([sigma_filtered_img], [0], None, [G_MAX + 1], [0, G_MAX + 1])
        h = np.divide(h, cardinality)

        # initiate final image with zeros
        final_image = np.zeros(sigma_filtered_img.shape, dtype=np.uint8())

        # histogram equalization application
        print(f'Starting histogram equalization algorithm for r={r}')
        for x, line in enumerate(sigma_filtered_img):
            for y, column in enumerate(line):
                u = column
                val = Utils.histogram_equalization(h, r, u)
                final_image[x][y] = val
        print('Histogram equalization algorithm terminated')

        cv.imshow(f'Resulting image for r={r}', final_image)
        cv.waitKey(0)
        cv.destroyAllWindows()
