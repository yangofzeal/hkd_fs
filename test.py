#!/usr/bin/env python3
from __future__ import print_function

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import hkd_fs
from benchmark_core import create_npz, benchmark_versioned, print_result

DATA = os.path.join(ROOT, "dataset_free.npz")
TARGET_BYTES = 512 * 1024

if not os.path.exists(DATA):
    create_npz(DATA, TARGET_BYTES)

hkd_fs.authorize_size(os.path.getsize(DATA))

r = benchmark_versioned(
    hkd_fs,
    DATA,
    versions=40,
    write_kib=1,
)

print_result("HKD_FS_%s_BENCHMARK" % hkd_fs.EDITION, hkd_fs, r)
