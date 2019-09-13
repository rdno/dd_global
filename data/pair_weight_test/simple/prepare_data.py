#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import argparse
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy import interpolate

from sair.specfem_io import get_nproc
from sair.specfem_io import read_all_from_folder
from sair.specfem_io import read_data_from_folder
from sair.specfem_io import write_data_to_folder


def get_values(image_file):
    im = Image.open(image_file)
    pix = im.load()
    values = np.zeros(im.size)
    height = im.size[1]
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            try:
                values[i, j] = (pix[i, height-j-1][0])/255
            except TypeError:  # grayscale image
                values[i, j] = (pix[i, height-j-1])/255
    return values


def interp(values, width, height):
    mw, mh = values.shape
    mx = np.arange(0, width, width/mw)
    my = np.arange(0, height, height/mh)
    b = interpolate.RectBivariateSpline(mx, my, values)
    return b


def update_model(b, data_folder, param, mean, spread):
    for i in range(get_nproc(data_folder)):
        x = read_data_from_folder(data_folder, "x", i)
        z = read_data_from_folder(data_folder, "z", i)
        data = b.ev(x, z)
        data = (data - 128/255)*2*spread + mean
        write_data_to_folder(data, args.data_folder, param, i)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare the specfem2d data")
    parser.add_argument("image_file", help="image file")
    parser.add_argument("data_folder", help="data folder")
    args = parser.parse_args()

    values = get_values(args.image_file)
    # plt.imshow(values)
    # plt.show()

    x = read_all_from_folder(args.data_folder, "x")
    y = read_all_from_folder(args.data_folder, "z")
    width = max(x)
    height = max(y)
    b = interp(values, width, height)
    update_model(b, args.data_folder, "vs", 3500, 500)
