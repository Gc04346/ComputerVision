import numpy as np

import cv2 as cv


class FormulationThree:

    @staticmethod
    def run(image_path):
        image = cv.imread(image_path)
        image_name = image_path.split('/')[-1].split('.')[0].capitalize()
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(gray, 50, 150, apertureSize=3)
        min_line_length = 100
        max_line_gap = 10
        lines = cv.HoughLinesP(edges, 1, np.pi / 180, 50, None, minLineLength=min_line_length, maxLineGap=max_line_gap)
        if lines is not None:
            for i in range(len(lines)):
                l = lines[i][0]
                cv.line(image, (l[0], l[1]), (l[2], l[3]), (0, 255, 0), 3, cv.LINE_AA)
        cv.imshow(f'Lines at {image_name}', image)
        cv.waitKey(0)
        cv.destroyAllWindows()
