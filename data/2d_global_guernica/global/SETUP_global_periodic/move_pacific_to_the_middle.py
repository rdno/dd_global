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
            name, net, x, z, _, _ = sta.split()
            stations[".".join([net, name])] = np.array([float(x),
                                                        float(z)])
    return stations


def write_stations(filename, stations):
    with open(filename, "w") as f:
        for sta in sorted(stations.keys()):
            net, name = sta.split(".")
            xz = stations[sta]
            f.write("{} {} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(
                name, net, xz[0], xz[1], 0, 0))


def read_sources(filename):
    return np.loadtxt(filename)


def move(xz):
    if xz[0] < 0:
        xz[0] += 180
    else:
        xz[0] -= 180
    return xz

move_sources = False
move_stations = True

if move_sources:
    source_file = "sources.dat"
    sources = read_sources(source_file)
    for source in sources:
        move(source)
    np.savetxt(source_file, sources)

if move_stations:
    for stations_file in glob("STATIONS_*"):
        print("Moving", stations_file)
        stations = read_stations(stations_file)
        for station in stations:
            stations[station] = move(stations[station])
        write_stations(stations_file, stations)
