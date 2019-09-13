#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Move STATIONS and sources locations to make the Pacific the model's center.
"""
from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import sys
import json


event_file = sys.argv[1]
with open(event_file) as f:
    events = [x.replace("\n", "") for x in f]


# BHZ -> BXY
source = "Z"
target = "Y"
filename_mask = "pairs/dd_pairs.{}.T045-110s.filter.json"


def adapt_name_to_2d(name, event):
    net, sta, loc, comp = name.split(".")
    return ".".join([net, sta, "BX"+target, event+":0"])


def adapt_pair(pair, event):
    pair["window_id_i"] = adapt_name_to_2d(pair["window_id_i"], event)
    pair["window_id_j"] = adapt_name_to_2d(pair["window_id_j"], event)
    return pair


def is_first_win(pair):
    return pair["window_id_i"].endswith(":0") and \
        pair["window_id_j"].endswith(":0")

merged_pairs = {"X": [], "Y": [], "Z": []}
for event in events:
    with open(filename_mask.format(event)) as f:
        pairs = json.load(f)[source]
    event_pairs = [adapt_pair(pair, event) for pair in pairs
                   if is_first_win(pair)]
    merged_pairs[target].extend(event_pairs)

with open("pairs.json", "w") as f:
    json.dump(merged_pairs, f, indent=2, sort_keys=True)
