#!/usr/bin/env python3
from __future__ import print_function

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import hkd_fs

REQUESTED_BYTES = 32 * 1024 * 1024

print("HKD_FS_FREE_LARGE_TEST")
print("edition=%s" % hkd_fs.EDITION)
print("module=%s" % hkd_fs.__file__)
print("requested_bytes=%d" % REQUESTED_BYTES)

try:
    hkd_fs.authorize_size(REQUESTED_BYTES)
except hkd_fs.HKDFreeLimitError as e:
    print("FREE_LIMIT_TRIGGERED=True")
    print(str(e))
    raise SystemExit(2)

print("FREE_LIMIT_TRIGGERED=False")
print("FAIL=True")
raise SystemExit(1)
