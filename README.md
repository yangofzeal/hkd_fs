# HKD FS

**Up to 30x faster exact versioned file writes in Python.**

HKD FS is designed for versioned files with sparse changes: checkpoints, NumPy arrays, scientific state, databases, caches, simulation output, serialized models, and other persistent binary artifacts.

## Python Example

Native Python full-version saving:

```python
import shutil

shutil.copyfile("state.bin", "state.v1.bin")
shutil.copyfile("state.bin", "state.v2.bin")
shutil.copyfile("state.bin", "state.v3.bin")
```

HKD FS:

```python
from hkd_fs import VersionedFile

vf = VersionedFile(
    "state.base",
    "state.hkd",
    create=True,
    size=file_size,
)

vf.initialize_from("state.bin")

vf.commit([
    (offset, changed_bytes),
])

vf.commit([
    (next_offset, next_changed_bytes),
])

vf.materialize("state.latest.bin")
vf.materialize("state.version1.bin", version=1)
```

## Benchmark

Test workload:

```text
file size:           32 MiB
versions:            40
changes per version: 1
changed bytes:       64 KiB
durability:          fsync
verification:        exact
```

### Linux

```text
full_snapshot_elapsed_s=4.336363
hkd_total_elapsed_s=0.265541
writer_total_speedup_x=16.330284
writer_byte_reduction_x=37.167805
exact_hkd=True
```

### macOS

```text
full_snapshot_elapsed_s=1.099268
hkd_total_elapsed_s=0.036671
writer_total_speedup_x=29.976518
writer_byte_reduction_x=37.167805
exact_hkd=True
```

**Measured result: up to 29.98x faster end-to-end versioned writes and 37.17x fewer persistent bytes in the tested workload.**

## Buy unlimited (no size restriction) hkd_fs:
https://buy.stripe.com/bJecMYf594fZ5fs4sDgUM06

## Why It Works

For a file of `N` bytes stored across `V` complete versions:

```text
W_full = V * N
```

If each later version changes `D_t` bytes, HKD stores:

```text
W_HKD = N + sum(D_t) + metadata
```

For uniform changed size `D`:

```text
W_HKD = N + (V - 1) * D + metadata
```

Ignoring small metadata, the reduction factor is:

```text
(V * N) / (N + (V - 1) * D)
```

For fixed `V` and small `D/N`, this approaches:

```text
V
```

For 40 versions, the theoretical byte-work ceiling approaches 40x as the changed fraction approaches zero.

## Exact Reconstruction Theorem

Let `S_0` be the initial file and let `Delta_t` be the exact ordered byte replacements from version `t-1` to version `t`:

```text
S_t = APPLY(S_(t-1), Delta_t)
```

HKD stores `S_0` exactly and stores every `Delta_t` exactly.

Base case: version 0 reconstructs exactly because the stored base is `S_0`.

Inductive step: if replay through `Delta_t` reconstructs `S_t`, then applying the exact stored `Delta_(t+1)` yields exactly `S_(t+1)`.

Therefore every stored version is exactly reconstructible.

## Free Edition

The Free edition is intentionally limited to:

```text
1 MiB per source file
```

Run:

```bash
python test.py
```

The test creates `dataset_free.npz` automatically if it is missing.

Any realistic larger file requires Unlimited.

Run:

```bash
python test_large.py
```

Expected result:

```text
HKD_FS_FREE_LARGE_TEST
edition=FREE
requested_bytes=33554432
FREE_LIMIT_TRIGGERED=True
HKD FS Free limit exceeded: 33,554,432 bytes > 1,048,576 bytes.
Real-world files require HKD FS Unlimited.
```

## Unlimited Edition

HKD FS Unlimited removes the file-size restriction.

Run:

```bash
python test.py
python test_large.py
```

The paid `test_large.py` creates `dataset_large.npz` automatically if missing and runs the full 32 MiB benchmark.

## Requirements

HKD FS itself uses only the Python standard library.

Benchmarks require:

```text
numpy
```

The theorem test requires:

```text
sympy
```

Run:

```bash
python theory_test.py
```

## Project

```text
https://github.com/yangofzeal/hkd_fs
```

## Buy unlimited (no size restriction) hkd_fs:
https://buy.stripe.com/bJecMYf594fZ5fs4sDgUM06

## Buy HKD FS Unlimited

```text
STRIPE_LINK_TO_BE_FILLED_IN
```
