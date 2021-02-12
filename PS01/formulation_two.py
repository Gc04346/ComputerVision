import cv2 as cv
from utils import Utils
import numpy as np


class FormulationTwo:
    @staticmethod
    def a():
        video = Utils.load_video('star.mp4')
        print(f'No. of frames: {int(video.get(cv.CAP_PROP_FRAME_COUNT))}')
        Utils.play_video(video)

    @staticmethod
    def b():
        video = Utils.load_video('star.mp4')

        # The chosen data measures will be: mean, standard deviation and contrast
        mean = np.array([])
        std = np.array([])
        contrast = np.array([])

        succes: bool = True
        while succes:
            success, frame = video.read()
            if not success:
                break
            mean = np.append(mean, frame.mean())
            std = np.append(std, frame.std())
            contrast = np.append(contrast, cv.cvtColor(frame, cv.COLOR_BGR2GRAY).std())
        print(f'Mean: {mean[:5]}...\n\nStd.: {std[:5]}...\n\nContrast: {contrast[:5]}...')
        return mean, std, contrast

    @staticmethod
    def c():
        mean_function, std_function, contrast_function = FormulationTwo.b()

        alpha_std_function = (std_function.std() / mean_function.std()) * (mean_function.mean() - std_function.mean())
        beta_std_function = mean_function.std() / std_function.std()

        alpha_contrast_function = (contrast_function.std() / mean_function.std()) * (mean_function.mean() - contrast_function.mean())
        beta_contrast_function = contrast_function.std() / std_function.std()

        new_mean = []
        new_std = []
        new_contrast = []

        for i, _ in enumerate(mean_function):
            new_mean.append(mean_function[i])
            new_std.append(beta_std_function * (std_function[i] + alpha_std_function))
            new_contrast.append(beta_contrast_function * (contrast_function[i] + alpha_contrast_function))
        print(f'Mean: {new_mean[:5]}...\n\nStd.: {new_std[:5]}...\n\nContrast: {new_contrast[:5]}...')
        return new_mean, new_std, new_contrast

    @staticmethod
    def d() -> None:
        new_mean, new_std, new_contrast = FormulationTwo.c()

        std_distance = 0.0
        contrast_distance = 0.0

        for i, _ in enumerate(new_mean):
            std_distance += abs(new_mean[i] - new_std[i])
            contrast_distance += abs(new_mean[i] - new_contrast[i])
        std_distance /= len(new_mean)
        contrast_distance /= len(new_mean)

        print(f'new_std\'s distance from the mean: {std_distance}')
        print(f'new_contrast\'s distance from the mean: {contrast_distance}')
