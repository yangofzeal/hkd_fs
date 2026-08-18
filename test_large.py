#!/usr/bin/env python3
from __future__ import print_function

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import hkd_fs

REQUESTED_BYTES = 32 * 1024 * 1024

print("HKD_FS_LARGE_TEST")
print("edition=%s" % hkd_fs.EDITION)
print("module=%s" % hkd_fs.__file__)
print("requested_bytes=%d" % REQUESTED_BYTES)

if hkd_fs.EDITION.upper() == "FREE":
    try:
        hkd_fs.authorize_size(REQUESTED_BYTES)
    except hkd_fs.HKDFreeLimitError as e:
        print("FREE_LIMIT_TRIGGERED=True")
        print(str(e))
        print("PASS=True")
        raise SystemExit(2)

    print("FREE_LIMIT_TRIGGERED=False")
    print("PASS=False")
    raise SystemExit(1)

try:
    hkd_fs.authorize_size(REQUESTED_BYTES)
except Exception as e:
    print("UNLIMITED_ACCEPTED=False")
    print(str(e))
    print("PASS=False")
    raise SystemExit(1)

print("UNLIMITED_ACCEPTED=True")
print("PASS=True")
raise SystemExit(0)
