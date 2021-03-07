import numpy as np

from utils import Utils, G_MAX, SigmaFilter, GRAYSCALE_IMAGE
import cv2 as cv


class FormulationThree:
    @staticmethod
    def local_operators():
        # load input image
        lenna = Utils.load_image('../imgs/lenna.png', GRAYSCALE_IMAGE)

        # define the two output images
        lenna_amplitude = np.zeros(lenna.shape, dtype=np.uint8())
        lenna_phase = np.zeros(lenna.shape, dtype=np.uint8())

        # define the 3x3 sliding windows running through the image I pixel by pixel
        windows = Utils.sliding_window(image=lenna, step=1, window_size=(3, 3))

        # total windows value is simply for percentage printing on the for loop
        total_windows = lenna.shape[0]*lenna.shape[1]

        for i, window in enumerate(windows):
            print(f'{round((i/total_windows)*100, 2)}%')
            px = window[0]
            py = window[1]
            wp = window[2]

            # perform the 2D DFT on the current window
            window_freq = Utils.get_image_in_frequency_domain(wp)

            # gets amplitude and phase values from the center pixel of the window
            amplitude, phase = Utils.get_amplitude_and_phase_values_separately(window_freq)

            # sets image M and P pixel values
            lenna_amplitude[py][px] = amplitude
            lenna_phase[py][px] = phase

        # thresholds for the Canny Operator
        low_threshold = 50
        high_threshold = low_threshold * 3
        lenna_canny = cv.Canny(lenna, low_threshold, high_threshold)

        # showing the original image, the Canny operator edge detector results and my algorithm results
        cv.imshow('Original Lenna', lenna)
        cv.imshow('Edges detected by Canny Operator', lenna_canny)
        cv.imshow('Amplitude Window', lenna_amplitude)
        cv.imshow('Phase Window', lenna_phase)
        cv.waitKey(0)
        cv.destroyAllWindows()
