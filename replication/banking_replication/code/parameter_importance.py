"""
parameter_importance.py
=======================
Parameter importance analysis: for each proposition, which assumptions most
strongly drive the result? This is the complement to the sensitivity sweeps and
the randomized invariance test -- rather than asking "does it hold?", it asks
"what does it depend on, and how much?"

Method. For each proposition we define a continuous MARGIN (signed distance from
its threshold; positive = holds, larger = more robustly). We draw many admissible
calibrations, then measure each parameter's influence on that margin two ways:

  * First-order variance contribution (a Sobol-style main effect, estimated by
    binning each parameter and measuring how much of the margin's variance is
    explained by the conditional mean across bins). This is model-free and
    captures nonlinear monotone and non-monotone effects.
  * Spearman rank correlation (sign + monotone strength), which is robust and
    interpretable as "raising this parameter raises/lowers the margin."

Reported together they identify the dominant assumptions. No external deps beyond
numpy. Run:  python3 parameter_importance.py
"""

import random
import numpy as np
import balance_sheet as bs


# ---------------------------------------------------------------------------
# admissible parameter draws (same ranges as the invariance test)
# ---------------------------------------------------------------------------
PARAMS = {
    "term_share":  (0.30, 0.80),
    "leverage":    (3.0, 6.0),
    "phi_liq":     (0.05, 0.35),
    "lambda_leak": (0.01, 0.06),
    "chi_c":       (0.15, 0.45),
    "zeta_star":   (0.10, 0.16),
    "m2":          (10.0, 40.0),
}


def draw(rng):
    return {k: rng.uniform(lo, hi) for k, (lo, hi) in PARAMS.items()}


# ---------------------------------------------------------------------------
# proposition margins (signed distance from threshold; >0 means the prop holds)
# ---------------------------------------------------------------------------
def margin_N2(p):
    """Separation margin = zeta* - coupling. Positive => circuits separate."""
    coupling = p["lambda_leak"] + p["chi_c"] * p["phi_liq"]
    return p["zeta_star"] - coupling


def margin_N3(p):
    """Credit-capacity level (always positive; importance = what scales capacity)."""
    D = p["term_share"] * p["m2"]
    E = D / (p["leverage"] - 1.0)
    return D + E


def margin_N4(p):
    """Run-proof headroom = 1 - contraction_share = reserved (unrunnable) share."""
    return 1.0 - p["term_share"]      # = transaction-money share of M2


MARGINS = {
    "N2 (separation)":       (margin_N2, ["lambda_leak", "chi_c", "phi_liq", "zeta_star"]),
    "N3 (credit capacity)":  (margin_N3, ["term_share", "leverage", "m2"]),
    "N4 (run-proof share)":  (margin_N4, ["term_share"]),
}


# ---------------------------------------------------------------------------
# importance measures
# ---------------------------------------------------------------------------
def first_order_variance_share(x, y, bins=20):
    """Fraction of Var(y) explained by E[y | x-bin] -- a main-effect index in [0,1]."""
    order = np.argsort(x)
    xs, ys = x[order], y[order]
    n = len(xs)
    edges = np.linspace(0, n, bins + 1).astype(int)
    cond_means = []
    weights = []
    for i in range(bins):
        seg = ys[edges[i]:edges[i + 1]]
        if len(seg):
            cond_means.append(seg.mean())
            weights.append(len(seg))
    cond_means = np.array(cond_means)
    weights = np.array(weights, dtype=float)
    var_cond = np.average((cond_means - ys.mean()) ** 2, weights=weights)
    var_total = ys.var()
    return float(var_cond / var_total) if var_total > 0 else 0.0


def spearman(x, y):
    """Spearman rank correlation (sign + monotone strength) without scipy."""
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    denom = np.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / denom) if denom > 0 else 0.0


# ---------------------------------------------------------------------------
# run the analysis
# ---------------------------------------------------------------------------
def analyze(n=20000, seed=770):
    rng = random.Random(seed)
    draws = [draw(rng) for _ in range(n)]
    cols = {k: np.array([d[k] for d in draws]) for k in PARAMS}

    print("=" * 70)
    print("PARAMETER IMPORTANCE ANALYSIS")
    print(f"  {n:,} admissible calibrations, seed {seed}")
    print("  first-order variance share (main effect, 0..1) + Spearman rho (sign)")
    print("=" * 70)

    for name, (fn, relevant) in MARGINS.items():
        y = np.array([fn(d) for d in draws])
        print(f"\n{name}   (margin mean {y.mean():+.3f}, sd {y.std():.3f})")
        rows = []
        for k in relevant:
            v = first_order_variance_share(cols[k], y)
            rho = spearman(cols[k], y)
            rows.append((k, v, rho))
        rows.sort(key=lambda r: -r[1])   # most important first
        tot = sum(r[1] for r in rows) or 1.0
        for k, v, rho in rows:
            bar = "#" * int(round(40 * v / max(r[1] for r in rows))) if rows else ""
            print(f"   {k:<12} var-share {v:>5.2f}  ({v/tot:>4.0%} of top-effects)  "
                  f"rho {rho:+.2f}  {bar}")
        top = rows[0][0]
        print(f"   -> dominant assumption: {top}")

    print("\n" + "=" * 70)
    print("Reading: for N2 (separation), the assumptions that most move the margin")
    print("are the ones a referee should scrutinize; for N3 the capacity scale is")
    print("driven by term share and money-stock size, not the leverage cap.")
    print("=" * 70)


if __name__ == "__main__":
    analyze()
