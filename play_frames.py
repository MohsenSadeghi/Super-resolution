import matplotlib.pyplot as plt
import numpy as np


def main():
    frames_padded = np.load('../149septin_rotated.npy')
    path = np.load('../149septin_path.npy')

    frames_sorted = []

    n_paths = path.shape[0]

    for i in range(n_paths):
        print path[i]
        frames_sorted.append(frames_padded[path[i][:]])

    for i in range(n_paths):

        n_frames_in_path = path[i].shape[0]

        for j in range(n_frames_in_path):
            plt.clf()

            plt.imshow(frames_sorted[i][j], cmap=plt.get_cmap('hot'))

            plt.pause(0.01)

            plt.draw()

        plt.pause(1.0)

    return ()


main()
