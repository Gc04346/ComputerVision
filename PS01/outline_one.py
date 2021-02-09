import sys
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv
from utils import Utils, MAX_RANGE
import copy

initial_x, initial_y, final_x, final_y = (0,0,0,0)

class OutlineOne():
    @staticmethod
    def one():
        img = Utils.load_lenna_image()
        cv.imshow('Lenna', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    @staticmethod
    def two():
        img = Utils.load_lenna_image()
        Utils.show_histogram(img)

    @staticmethod
    def three(frame_size=13):
        img = Utils.load_lenna_image()
        def draw_rectangle(event, x, y, flags, param):
            blue = img[y, x, 0]
            green = img[y, x, 1]
            red = img[y, x, 2]
            global initial_x, initial_y, final_x, final_y
            initial_x, initial_y = (x - frame_size, y - frame_size)
            final_x, final_y = (x + frame_size, y + frame_size)
            # Because slicing is [inclusive:exclusive], we need the +1.
            my_frame = img[initial_x:final_x+1, initial_y:final_y+1]
            print(
                f'Cusor at: ({x},{y}). BGR values: ({blue}, {green}, {red}). Intensity value: {Utils.get_intensity_value(blue, green, red)}')
            print(f'Average grey level: {round(my_frame.mean(),3)}. Standard deviation: {round(my_frame.std(), 3)}')

        cv.namedWindow('Lenna')
        cv.setMouseCallback('Lenna', draw_rectangle)

        while True:
            frame = img
            cv.rectangle(img, (initial_x, initial_y), (final_x, final_y), (MAX_RANGE, MAX_RANGE, MAX_RANGE), 1)
            cv.imshow('Lenna', frame)
            img = Utils.load_lenna_image()
            k = cv.waitKey(1) & 0xFF
            if k == 27:
                break
        cv.destroyAllWindows()

    @staticmethod
    def four():
        """
        To discuss homogeneousity and inhomogeneousity in our case, it would be best to look at the histogram and standard
        deviation values only. Looking at the histogram, we would classify a homogeneous image as an image with a rather
        flat histogram, without high or low peeks. We should observe the three color level graph lines being equally
        distant from each other throughout the entire graph range. Now, looking at the standard deviation values, a
        window frame with low variance could be considered homogeneous. We could say that, the lower the variance, the
        more homogeneous the frame is. That is because, when we have a low standard deviation, the specific value does
        not differ too much from the average, thus leading to a homogeneous frame.
        """
        print('The discussion for the item 1.4 is at the docstring of the method OutlineOne.four()')