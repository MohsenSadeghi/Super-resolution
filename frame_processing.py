import matplotlib.pyplot as plt
import numpy as np
import scipy.io


# def frame_distance (i, j):

def dist(f1, f2):
    return np.sum(np.power((f1 - f2).reshape((-1, 1)), 2))


def evaluate():
    global dat

    raw_dat = scipy.io.loadmat('../149septinpixels.mat')

    dat = raw_dat["allseptins"]

    n_frames = dat.size

    np.set_printoptions(threshold=np.nan)

    # print dat1[0][1]

    # return

    # plt.ion ()

    fig1 = plt.figure()

    ax = fig1.gca()

    # current_plot = ax.imshow (dat1[0][0])
    lxmax = None
    lymax = None

    for i in range(n_frames):
        frame_dat = dat[0][i]

        lx, ly = frame_dat.shape
        lxmax = max(lx, lxmax) if lxmax is not None else lx
        lymax = max(ly, lymax) if lymax is not None else ly

    #	old_plot = current_plot

    # current_plot = plt.imshow (frame_dat)

    #	ax.collections.remove (old_plot)

    # plt.pause (0.1)

    # plt.draw ()

    # plt.waitforbuttonpress ()

    lmax = max(lxmax, lymax)

    frames_padded = []

    d = np.array([0 for _ in range(n_frames)])

    for i in range(n_frames):
        frame_dat = dat[0][i]
        frame_dat_padded = np.zeros((lmax, lmax), dtype=np.float32)
        s = frame_dat.shape
        frame_dat_padded[:s[0], :s[1]] = frame_dat[:]
        frames_padded.append(frame_dat_padded)

        d[i] = dist(frames_padded[i], frames_padded[0])

    # current_plot = ax.imshow (frame_dat_padded)

    # plt.pause (0.1)

    # plt.draw ()

    d_ind = np.argsort(d)

    for i in range(n_frames):
        current_plot = ax.imshow(frames_padded[d_ind[i]])

        plt.pause(0.1)

        plt.draw()


evaluate()
