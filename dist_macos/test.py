#!/usr/bin/env python3
from __future__ import print_function

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import hkd_fs
from benchmark_core import create_npz, benchmark_versioned, print_result

DATA = ROOT / "dataset_free.npz"
TARGET_BYTES = 512 * 1024

if not DATA.exists():
    create_npz(DATA, TARGET_BYTES)

hkd_fs.authorize_size(DATA.stat().st_size)

r = benchmark_versioned(
    hkd_fs,
    DATA,
    versions=40,
    write_kib=1,
)

print_result("HKD_FS_%s_BENCHMARK" % hkd_fs.EDITION, hkd_fs, r)
