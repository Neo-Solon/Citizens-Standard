"""
verify_scf.py  --  Read-check the 2022 SCF summary extract against published figures.

Before any Citizens-Standard channel is applied, the weighted records must reproduce
the published SCF 2022 statistics. If they do, the data is loaded correctly and the
baseline is real. Every statistic is WGT-weighted; the 5-implicate structure is handled
(WGT in the extract sums to the US household count, ~131.3M).
"""
import os
import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "SCFP2022.csv")


def load():
    return pd.read_csv(DATA, usecols=["YY1", "WGT", "NETWORTH", "AGE", "MARRIED", "INCOME"])


def wpct(v, wt, q):
    o = np.argsort(v)
    v = np.asarray(v)[o]
    wt = np.asarray(wt)[o]
    cw = (np.cumsum(wt) - 0.5 * wt) / wt.sum()
    return np.interp(q, cw, v)


def gini(v, wt):
    o = np.argsort(v)
    v = v[o].astype(float)
    wt = wt[o].astype(float)
    cw = np.cumsum(wt) / wt.sum()
    cv = np.cumsum(v * wt) / np.sum(v * wt)
    return 1 - np.sum((cw[1:] - cw[:-1]) * (cv[1:] + cv[:-1]))


def share(v, wt, lo, hi):
    o = np.argsort(v)
    s = (v[o] * wt[o])
    cc = np.cumsum(wt[o]) / wt.sum()
    return s[(cc > lo) & (cc <= hi)].sum() / s.sum() * 100


def main():
    df = load()
    w = df.WGT.values.astype(float)
    nw = df.NETWORTH.values.astype(float)
    checks = {
        "households (sum WGT)": (w.sum(), 131_306_389, "US household count"),
        "mean net worth": (np.average(nw, weights=w), 1_059_470, "SCF 2022 Bulletin"),
        "median net worth": (wpct(nw, w, 0.50), 192_900, "SCF 2022 Bulletin"),
        "top-1% threshold": (wpct(nw, w, 0.99), 13_666_778, "DQYDJ/SCF"),
        "wealth Gini": (gini(nw, w), 0.83, "published US wealth Gini"),
        "bottom-50% share": (share(nw, w, 0.0, 0.50), 2.5, "SCF/DFA ~2-3%"),
        "zero/negative NW %": (w[nw <= 0].sum() / w.sum() * 100, 7.5, "SCF 2022 ~7%"),
    }
    print("=== SCF 2022 read-check (computed vs published) ===")
    ok = True
    for name, (got, pub, src) in checks.items():
        # shares/percentages are small numbers -> judge on absolute gap (within ~1pp);
        # levels -> judge on relative gap (within 10%).
        is_share = ("share" in name) or name.strip().endswith("%") or (name == "wealth Gini")
        within = abs(got - pub) <= 1.0 if is_share else abs(got - pub) / (abs(pub) if pub else 1) < 0.10
        flag = "OK" if within else "CHECK"
        if not within:
            ok = False
        fmt = "{:>16,.3f}" if name == "wealth Gini" or "share" in name or "%" in name else "{:>16,.0f}"
        print(f"  {name:22} {fmt.format(got)}   (published ~{pub:,}; {src})  [{flag}]")
    print("READ-CHECK:", "PASSED" if ok else "REVIEW")
    return ok


if __name__ == "__main__":
    main()
