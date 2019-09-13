#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Move STATIONS and sources locations to make the Pacific the model's center.
"""
from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

from glob import glob
import numpy as np
import shutil


def read_stations(filename):
    stations = {}
    with open(filename) as f:
        for sta in f:
            name, net, lat, lon, _, _ = sta.split()
            stations[".".join([net, name])] = np.array([float(lon),
                                                        float(lat)])
    return stations


def write_stations(filename, stations):
    with open(filename, "w") as f:
        for sta in sorted(stations.keys()):
            net, name = sta.split(".")
            xz = stations[sta]
            f.write("{} {} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(
                name, net, xz[0], xz[1], 0, 0))

for stations_file in glob("STATIONS_*"):
    print("Moving", stations_file)
    stations = read_stations(stations_file)
    write_stations(stations_file, stations)
