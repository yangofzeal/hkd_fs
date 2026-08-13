#!/usr/bin/env python3
from __future__ import print_function

import sympy as sp

N, V, D = sp.symbols("N V D", positive=True)

full_work = sp.expand(V * N)
hkd_work = sp.expand(N + (V - 1) * D)
ratio = sp.factor(full_work / hkd_work)
limit_ratio = sp.limit(ratio, N, sp.oo)

print("HKD_FS_SYMPY_THEORY_TEST")
print("full_work=%s" % full_work)
print("hkd_work=%s" % hkd_work)
print("ratio=%s" % ratio)
print("limit_N_to_inf_fixed_V_D=%s" % limit_ratio)
print("PASS=%s" % (str(limit_ratio) == "V"))
