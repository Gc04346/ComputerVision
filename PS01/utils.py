import cmath
import sys
from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np

MAX_RANGE = 255
GRAYSCALE_IMAGE = 0


class Utils:

    @staticmethod
    def load_image(filename: str, grayscale=None):
        img = cv.imread(f'../imgs/{filename}', grayscale)
        if img is None:
            sys.exit('A imagem não carregou corretamente')
        return img

    @staticmethod
    def show_histogram(img):
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histr = cv.calcHist([img], [i], None, [MAX_RANGE + 1], [0, MAX_RANGE + 1])
            plt.plot(histr, color=col)
            plt.xlim([0, MAX_RANGE + 1])
        plt.show()

    @staticmethod
    def get_intensity_value(blue, green, red):
        return round(sum([blue, green, red]) / 3, 3)

    @staticmethod
    def mean_filter(im):
        img = im
        w = 2

        for i in range(2, im.shape[0] - 2):
            for j in range(2, im.shape[1] - 2):
                block = im[i - w:i + w + 1, j - w:j + w + 1]
                m = np.mean(block, dtype=np.float32)
                img[i][j] = int(m)
        return img

    @staticmethod
    def get_image_in_frequency_domain(image, dp_shifted:bool = True):
        frequency_img = np.fft.fft2(image)
        if dp_shifted:
            # deslocando o 00 para o centro
            frequency_img = np.fft.fftshift(frequency_img)
        return frequency_img

    @staticmethod
    def get_image_in_spatial_domain(image, dp_shifted:bool = True):
        if dp_shifted:
            image = np.fft.ifftshift(image)
        return np.real(np.fft.ifft2(image))

    @staticmethod
    def get_image_in_polar_coords(image):
        return [
            [cmath.polar(complex_number) for _, complex_number in enumerate(complex_group)]
            for _, complex_group in enumerate(image)
        ]

    @staticmethod
    def get_complex_from_polar(image):
        return [
            [cmath.rect(polar_coord[0], polar_coord[1]) for polar_coord in complex_group]
            for complex_group in image
        ]

    @staticmethod
    def load_video(filename: str):
        vid = cv.VideoCapture(f'../vids/{filename}')
        if vid is None:
            sys.exit('O vídeo não carregou corretamente.')
        return vid

    @staticmethod
    def play_video(video):
        success: bool = True
        while success:
            success, frame = video.read()
            if success:
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

                cv.imshow('frame', gray)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        video.release()
        cv.destroyAllWindows()
