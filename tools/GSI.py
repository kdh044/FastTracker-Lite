import os
import numpy as np
from os.path import join
from collections import defaultdict
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from scipy.interpolate import PchipInterpolator
import argparse

def make_parser():
    parser = argparse.ArgumentParser("GSI")
    parser.add_argument("--loadpath", type=str, default=".\\YOLOX_outputs\\yolox_x_mix_det\\run033\\track_results")
    parser.add_argument("--savepath", type=str, default=".\\YOLOX_outputs\\yolox_x_mix_det\\run033\\track_results_gsi")
    return parser

def LinearInterpolation(input_, interval):
    input_ = input_[np.lexsort([input_[:, 0], input_[:, 1]])]  
    output_ = input_.copy()

    id_pre, f_pre, row_pre = -1, -1, np.zeros((10,))
    for row in input_:
        f_curr, id_curr = row[:2].astype(int)
        if id_curr == id_pre:  
            if f_pre + 1 < f_curr < f_pre + interval:
                for i, f in enumerate(range(f_pre + 1, f_curr), start=1):  
                    step = (row - row_pre) / (f_curr - f_pre) * i
                    row_new = row_pre + step
                    output_ = np.append(output_, row_new[np.newaxis, :], axis=0)
        else:  
            id_pre = id_curr
        row_pre = row
        f_pre = f_curr
    output_ = output_[np.lexsort([output_[:, 0], output_[:, 1]])]
    return output_


def GaussianSmooth(input_, tau):
    output_ = []
    ids = set(input_[:, 1])
    for id_ in ids:
        tracks = input_[input_[:, 1] == id_]

        if len(tracks) < 2:
            continue

        len_scale = np.clip(tau * np.log(tau ** 3 / len(tracks)), tau ** -1, tau ** 2)
        if not np.isfinite(len_scale) or len_scale <= 0:
            len_scale = 1.0

        kernel = RBF(len_scale)

        t = tracks[:, 0].reshape(-1, 1)
        x = tracks[:, 2].reshape(-1, 1)
        y = tracks[:, 3].reshape(-1, 1)
        w = tracks[:, 4].reshape(-1, 1)
        h = tracks[:, 5].reshape(-1, 1)

        try:
            # Use one GPR per feature
            xx = GPR(kernel).fit(t, x).predict(t)
            yy = GPR(kernel).fit(t, y).predict(t)
            ww = GPR(kernel).fit(t, w).predict(t)
            hh = GPR(kernel).fit(t, h).predict(t)
        except Exception as e:
            print(f"GPR error for ID {id_}: {e}")
            continue

        output_.extend([
            [t[i, 0], id_, xx[i, 0], yy[i, 0], ww[i, 0], hh[i, 0], 1, -1, -1, -1]
            for i in range(len(t))
        ])

    return output_

def smooth_track_1d(t, values):
    interp = PchipInterpolator(t.flatten(), values.flatten())
    return interp(t.flatten())

def GaussianSmooth_1D(input_):
    output_ = []
    ids = set(input_[:, 1])
    for id_ in ids:
        tracks = input_[input_[:, 1] == id_]
        if len(tracks) < 2:
            continue

        t = tracks[:, 0].reshape(-1, 1)
        x = tracks[:, 2].reshape(-1, 1)
        y = tracks[:, 3].reshape(-1, 1)
        w = tracks[:, 4].reshape(-1, 1)
        h = tracks[:, 5].reshape(-1, 1)

        try:
            xx = smooth_track_1d(t, x)
            yy = smooth_track_1d(t, y)
            ww = smooth_track_1d(t, w)
            hh = smooth_track_1d(t, h)
        except Exception as e:
            print(f"[Smooth error] ID {id_}: {e}")
            continue

        output_.extend([
            [t[i, 0], id_, xx[i], yy[i], ww[i], hh[i], 1, -1, -1, -1]
            for i in range(len(t))
        ])

    return output_
# GSI
def GSInterpolation(path_in, path_out, interval, tau):
    input_ = np.loadtxt(path_in, delimiter=',')
    li = LinearInterpolation(input_, interval)
    gsi = GaussianSmooth_1D(li)
    np.savetxt(path_out, gsi, fmt='%d,%d,%.2f,%.2f,%.2f,%.2f,%.2f,%d,%d,%d')
    
if __name__ == '__main__':
    args = make_parser().parse_args()
    numfiles = len (os.listdir(args.loadpath))
    for index, txtfile in enumerate(os.listdir(args.loadpath)):
        loadtxtpath = os.path.join(args.loadpath, txtfile)
        savetxtpath = os.path.join(args.savepath, txtfile)
        print('Progress: {}/{}. Fetching {} \n'.format(index, numfiles, txtfile))
        try:
            GSInterpolation(
                path_in=loadtxtpath,
                path_out=savetxtpath,
                interval=20,
                tau=10
            )
        except Exception as e:
            print(f"Error processing {txtfile}: {e}")