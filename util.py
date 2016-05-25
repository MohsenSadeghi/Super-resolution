import numpy as np

# Finds the center of mass of a frame (to center it)
def frame_COM(f):
    lx, ly = f.shape
    mass = np.sum(f)

    pos_mat = np.mgrid[0:lx, 0:ly]

    x_mat = pos_mat[0]
    y_mat = pos_mat[1]

    cx = np.sum(x_mat * f) / mass
    cy = np.sum(y_mat * f) / mass

    return cx, cy


# Calculated the second area moment tensor and the elongated direction
# It is assumed that the picture is centered around the COM
def frame_orient(f):
    lx, ly = f.shape

    pos_mat = np.mgrid[-0.5 * lx:0.5 * lx, -0.5 * ly:0.5 * ly]

    x_mat = pos_mat[0]
    y_mat = pos_mat[1]

    x2_mat = np.power(x_mat, 2)
    y2_mat = np.power(y_mat, 2)
    xy_mat = x_mat * y_mat

    Ixx = np.sum(y2_mat * f)
    Ixy = np.sum(xy_mat * f)
    Iyy = np.sum(x2_mat * f)

    alpha = 0.5 * np.arctan(2.0 * Ixy / (Iyy - Ixx))

    cos_a = np.cos(alpha)
    sin_a = np.sin(alpha)

    cos2_a = cos_a * cos_a
    sin2_a = sin_a * sin_a
    sin_2a = 2.0 * sin_a * cos_a

    I1 = Ixx * cos2_a + Iyy * sin2_a - Ixy * sin_2a
    I2 = Ixx * sin2_a + Iyy * cos2_a + Ixy * sin_2a

    if I1 > I2:
        theta = alpha
    else:
        theta = alpha + 0.5 * np.pi

    return theta


def interpolate_point(f, xr, yr):
    lx, ly = f.shape

    x1 = int(np.floor(xr))
    y1 = int(np.floor(yr))

    eps = 2.0 * (xr - x1) - 1.0
    eta = 2.0 * (yr - y1) - 1.0

    N1 = 0.25 * (1.0 - eps) * (1.0 - eta)
    N2 = 0.25 * (1.0 + eps) * (1.0 - eta)
    N3 = 0.25 * (1.0 + eps) * (1.0 + eta)
    N4 = 0.25 * (1.0 - eps) * (1.0 + eta)

    p = N1 * f[x1, y1] + N2 * f[x1 + 1, y1] + N3 * f[x1 + 1, y1 + 1] + N4 * f[x1, y1 + 1]

    return p


def insert_rot_frame(f, f_pad, th):
    lx, ly = f.shape
    lpx, lpy = f_pad.shape

    fac = 1.0 / float(np.sum(f))

    sin_th = np.sin(th)
    cos_th = np.cos(th)

    for i in range(lpx):
        for j in range(lpy):

            xr = sin_th * (i - 0.5 * lpx) + cos_th * (j - 0.5 * lpy) + 0.5 * lx
            yr = -cos_th * (i - 0.5 * lpx) + sin_th * (j - 0.5 * lpy) + 0.5 * ly

            if (xr > 0) and (xr < lx - 1) and (yr > 0) and (yr < ly - 1):
                f_pad[i, j] = fac * interpolate_point(f, xr, yr)
                # else:
                #	f_pad[i, j] = 10