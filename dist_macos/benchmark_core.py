from __future__ import print_function

import hashlib
import mmap
import os
import random
import shutil
import tempfile
import time
from pathlib import Path

import numpy as np


VERSIONS = 40
WRITE_KIB = 64
SEED = 20260812


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb", buffering=0) as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def create_npz(path, target_bytes):
    n = max(1, (int(target_bytes) - 512) // 4)
    a = (np.arange(n, dtype=np.uint32) * np.uint32(2654435761)).view(np.float32)
    np.savez(path, data=a)
    return Path(path).stat().st_size


def deterministic_updates(size, versions, write_bytes):
    rng = random.Random(SEED)
    updates = []
    for _ in range(versions - 1):
        off = rng.randrange(0, size - write_bytes + 1)
        data = bytes(rng.getrandbits(8) for _ in range(write_bytes))
        updates.append([(off, data)])
    return updates


def apply_fd(path, batch):
    fd = os.open(str(path), os.O_RDWR)
    try:
        for off, data in batch:
            if hasattr(os, "pwrite"):
                os.pwrite(fd, data, off)
            else:
                os.lseek(fd, off, os.SEEK_SET)
                os.write(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)


def benchmark_versioned(hkd_fs, dataset_path, versions=VERSIONS, write_kib=WRITE_KIB):
    dataset_path = Path(dataset_path)
    size = dataset_path.stat().st_size
    hkd_fs.authorize_size(size)

    write_bytes = min(int(write_kib) * 1024, max(1024, size // 16))
    updates = deterministic_updates(size, versions, write_bytes)

    with tempfile.TemporaryDirectory(prefix="hkd_fs_bench_") as td:
        td = Path(td)

        full = td / "full"
        full.mkdir()

        working = full / "working.bin"
        shutil.copyfile(dataset_path, working)

        full_bytes = 0
        t0 = time.perf_counter()

        for v in range(versions):
            if v:
                apply_fd(working, updates[v - 1])

            snap = full / ("v%03d.bin" % v)
            shutil.copyfile(working, snap)
            with open(snap, "rb") as f:
                os.fsync(f.fileno())

            full_bytes += snap.stat().st_size

        full_t = time.perf_counter() - t0
        truth = sha256(working)

        hdir = td / "hkd"
        hdir.mkdir()

        base = hdir / "base.bin"
        journal = hdir / "versions.hkd"

        total_t0 = time.perf_counter()

        vf = hkd_fs.VersionedFile(base, journal, create=True, size=size)
        vf.initialize_from(dataset_path)

        active_t0 = time.perf_counter()
        for batch in updates:
            vf.commit(batch)
        active_t = time.perf_counter() - active_t0

        hkd_total_t = time.perf_counter() - total_t0

        out = hdir / "latest.bin"
        vf.materialize(out)

        hkd_bytes = base.stat().st_size + journal.stat().st_size
        exact = sha256(out) == truth

        return {
            "size": size,
            "versions": versions,
            "write_bytes": write_bytes,
            "full_t": full_t,
            "hkd_total_t": hkd_total_t,
            "hkd_active_t": active_t,
            "full_bytes": full_bytes,
            "hkd_bytes": hkd_bytes,
            "exact": exact,
        }


def print_result(label, hkd_fs, r):
    print(label)
    print("edition=%s" % hkd_fs.EDITION)
    print("module=%s" % hkd_fs.__file__)
    print("file_bytes=%d" % r["size"])
    print("versions=%d" % r["versions"])
    print("active_bytes_per_update=%d" % r["write_bytes"])
    print("full_snapshot_elapsed_s=%.6f" % r["full_t"])
    print("hkd_total_elapsed_s=%.6f" % r["hkd_total_t"])
    print("hkd_active_journal_elapsed_s=%.6f" % r["hkd_active_t"])
    print("writer_total_speedup_x=%.6f" % (r["full_t"] / r["hkd_total_t"]))
    print("writer_byte_reduction_x=%.6f" % (r["full_bytes"] / r["hkd_bytes"]))
    print("exact_hkd=%s" % r["exact"])
    print("PASS=%s" % r["exact"])
