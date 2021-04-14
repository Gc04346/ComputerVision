from typing import List, Tuple, Set

import numpy as np
import matplotlib.pyplot as plt
from utils import Utils, G_MAX, GRAYSCALE_IMAGE, BLACK, WHITE
import cv2 as cv


class FormulationOne:
    rx = np.array([-1, 1, -1, 1]).reshape((2, 2))
    ry = np.array([-1, -1, 1, 1]).reshape((2, 2))
    laplacian = np.array([1 / 12, 1 / 6, 1 / 12, 1 / 6, -1, 1 / 6, 1 / 12, 1 / 6, 1 / 12]).reshape(3, 3)

    def __init__(self, lambda_val: float, iterations: int, video_path: str, frame1: int = 1, frame2: int = 2):
        self.lambda_val = lambda_val
        self.iterations = iterations
        self.frames = []

        cap = cv.VideoCapture(video_path)
        ret, frame = cap.read()
        self.base_image = frame
        while ret:
            self.frames.append(cv.cvtColor(frame, cv.COLOR_BGR2GRAY))
            ret, frame = cap.read()

        self.frame1 = self.frames[frame1 - 1]
        self.frame2 = self.frames[frame2 - 1]

    def run(self):
        print(f'Running algorithm for lambda {self.lambda_val} and {self.iterations} iterations.')
        u, v = self.horn_shunck()
        self.plot_movement_images(u, v)
        x = np.arange(0, self.frame1.shape[1], 1)
        y = np.arange(0, self.frame1.shape[0], 1)
        fig, ax = plt.subplots()
        q = ax.quiver(x, y, u, v)
        ax.quiverkey(q, X=0.5, Y=1.1, U=1, label='Velocity', labelpos='E')
        plt.show()

    def plot_movement_images(self, u, v):
        hsv = np.zeros_like(self.base_image)
        hsv[..., 1] = 255
        magnitude, theta = cv.cartToPolar(u, v)
        hsv[..., 0] = theta * 108 / np.pi / 2
        hsv[..., 2] = cv.normalize(magnitude, None, 0, 255, cv.NORM_MINMAX)
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        cv.imshow('Movement Image', bgr)
        cv.waitKey(0)
        cv.imshow('U vector', u)
        cv.waitKey(0)
        cv.imshow('V vector', v)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def horn_shunck(self):
        frame1, frame2 = (self.frame1, self.frame2)
        fx = np.zeros(frame1.shape)
        fy = np.zeros(frame1.shape)
        ft = np.zeros(frame1.shape)

        for x, line in enumerate(frame1, start=1):
            for y, pos in enumerate(line, start=1):
                try:
                    frame_1_window = np.array(
                        [frame1[x][y], frame1[x + 1][y], frame1[x][y + 1], frame1[x + 1][y + 1]]).reshape((2, 2))
                    frame_2_window = np.array(
                        [frame2[x][y], frame2[x + 1][y], frame2[x][y + 1], frame2[x + 1][y + 1]]).reshape((2, 2))
                    fx[x][y] = 0.5 * (sum(sum(np.multiply(frame_1_window, self.rx))) + sum(
                        sum(np.multiply(frame_2_window, self.rx))))
                    fy[x][y] = 0.5 * (sum(sum(np.multiply(frame_1_window, self.ry))) + sum(
                        sum(np.multiply(frame_2_window, self.ry))))
                    ft[x][y] = sum(sum(frame_2_window - frame_1_window))
                except IndexError:
                    continue

        u = np.zeros(frame1.shape)
        v = np.zeros(frame1.shape)
        u1 = np.zeros(frame1.shape)
        v1 = np.zeros(frame1.shape)

        for i in range(self.iterations):
            print(f'Iteration no. {i+1}/{self.iterations}')
            for x, line in enumerate(frame1, start=1):
                for y, pos in enumerate(line, start=1):
                    try:
                        # u_window = np.array(u)
                        u_window = np.array(
                            [u[x - 1][y - 1], u[x][y - 1], u[x + 1][y - 1], u[x - 1][y], u[x][y], u[x + 1][y],
                             u[x - 1][y + 1], u[x][y + 1], u[x + 1][y + 1]]).reshape((3, 3))
                        v_window = np.array([v[x - 1][y - 1], v[x][y - 1], v[x + 1][y - 1], v[x - 1][y], v[x][y],
                                             v[x + 1][y], v[x - 1][y + 1], v[x][y + 1], v[x + 1][y + 1]]).reshape(
                            (3, 3))
                        uav = sum(sum(np.multiply(u_window, self.laplacian)))
                        vav = sum(sum(np.multiply(v_window, self.laplacian)))
                        p = fx[x][y] * uav + fy[x][y] * vav + ft[x][y]
                        d = self.lambda_val + fx[x][y] ** 2 + fy[x][y] ** 2
                        p_d = p / d
                        u1[x][y] = uav - fx[x][y] * p_d
                        v1[x][y] = vav - fy[x][y] * p_d
                    except IndexError:
                        continue
            print(u1 == u)
            u = u1
            v = v1
        return u, v
