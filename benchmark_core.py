from __future__ import print_function

import hashlib
import os
import random
import shutil
import tempfile
import time

import numpy as np


VERSIONS = 40
WRITE_KIB = 64
SEED = 20260812


def clock():
    f = getattr(time, "perf_counter", None)
    return f() if f else time.time()


def sha256(path):
    h = hashlib.sha256()
    with open(str(path), "rb", buffering=0) as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def create_npz(path, target_bytes):
    path = str(path)
    n = max(1, (int(target_bytes) - 512) // 4)
    a = (
        np.arange(n, dtype=np.uint32) *
        np.uint32(2654435761)
    ).view(np.float32)
    np.savez(path, data=a)
    return os.path.getsize(path)


def deterministic_updates(size, versions, write_bytes):
    rng = random.Random(SEED)
    updates = []

    for _ in range(versions - 1):
        off = rng.randrange(0, size - write_bytes + 1)

        # bytes(iterable_of_ints) is supported by Python 3.4.
        data = bytes(
            bytearray(
                rng.getrandbits(8)
                for _ in range(write_bytes)
            )
        )

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


def _mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def benchmark_versioned(
    hkd_fs,
    dataset_path,
    versions=VERSIONS,
    write_kib=WRITE_KIB
):
    dataset_path = os.path.abspath(str(dataset_path))
    size = os.path.getsize(dataset_path)

    hkd_fs.authorize_size(size)

    write_bytes = min(
        int(write_kib) * 1024,
        max(1024, size // 16)
    )

    updates = deterministic_updates(
        size,
        versions,
        write_bytes
    )

    # tempfile.TemporaryDirectory does not exist on Python 3.4.
    td = tempfile.mkdtemp(prefix="hkd_fs_bench_")

    try:
        full = os.path.join(td, "full")
        _mkdir(full)

        working = os.path.join(full, "working.bin")
        shutil.copyfile(dataset_path, working)

        full_bytes = 0
        t0 = clock()

        for v in range(versions):
            if v:
                apply_fd(
                    working,
                    updates[v - 1]
                )

            snap = os.path.join(
                full,
                "v%03d.bin" % v
            )

            shutil.copyfile(
                working,
                snap
            )

            # Open writable for fsync portability/intent clarity.
            with open(snap, "rb") as f:
                os.fsync(f.fileno())

            full_bytes += os.path.getsize(snap)

        full_t = clock() - t0
        truth = sha256(working)

        hdir = os.path.join(td, "hkd")
        _mkdir(hdir)

        base = os.path.join(hdir, "base.bin")
        journal = os.path.join(
            hdir,
            "versions.hkd"
        )

        total_t0 = clock()

        vf = hkd_fs.VersionedFile(
            base,
            journal,
            create=True,
            size=size
        )

        vf.initialize_from(dataset_path)

        active_t0 = clock()

        for batch in updates:
            vf.commit(batch)

        active_t = clock() - active_t0
        hkd_total_t = clock() - total_t0

        out = os.path.join(
            hdir,
            "latest.bin"
        )

        vf.materialize(out)

        hkd_bytes = (
            os.path.getsize(base) +
            os.path.getsize(journal)
        )

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

    finally:
        shutil.rmtree(td, ignore_errors=True)


def print_result(label, hkd_fs, r):
    print(label)
    print("edition=%s" % hkd_fs.EDITION)
    print("module=%s" % hkd_fs.__file__)
    print("file_bytes=%d" % r["size"])
    print("versions=%d" % r["versions"])
    print(
        "active_bytes_per_update=%d" %
        r["write_bytes"]
    )
    print(
        "full_snapshot_elapsed_s=%.6f" %
        r["full_t"]
    )
    print(
        "hkd_total_elapsed_s=%.6f" %
        r["hkd_total_t"]
    )
    print(
        "hkd_active_journal_elapsed_s=%.6f" %
        r["hkd_active_t"]
    )
    print(
        "writer_total_speedup_x=%.6f" %
        (r["full_t"] / r["hkd_total_t"])
    )
    print(
        "writer_byte_reduction_x=%.6f" %
        (r["full_bytes"] / r["hkd_bytes"])
    )
    print("exact_hkd=%s" % r["exact"])
    print("PASS=%s" % r["exact"])
