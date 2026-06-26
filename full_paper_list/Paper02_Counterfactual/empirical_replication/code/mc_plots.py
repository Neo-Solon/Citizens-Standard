"""
mc_plots.py
============
Generate Figures M1-M4 for Section 6 of the paper, plus the additional
deterministic figures referenced by Sections 4-5.

Output files:
  figure_M1_distributions_v3.png  -- per-cohort density histograms (IID vs block)
  figure_M2_percentile_bands_v3.png  -- P5/P25/P50/P75/P95 by cohort
  figure_M3_p_below_median_v3.png  -- bars of P(<median) across configs
  figure_M4_p50_p5_sensitivity_v3.png  -- left P50, right P5 by configuration
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from mc_engine import run_all, summarize
from deterministic_engine import (
    BENCHMARKS, COHORTS, build_dataset, compute_cohort,
)


# ---- Deterministic central-scenario values (from Section 4) ----
def get_deterministic_central():
    data = build_dataset(end_year=2060)
    out = {}
    for name, b, r in COHORTS:
        out[name] = compute_cohort(data, b, r, 0.045)
    return out


# =============================================================================
# Figure M1 - Distribution histograms per cohort (1929-2025 universe)
# =============================================================================
def fig_M1(results, det_central, fname="figure_M1_distributions_v3.png"):
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Figure M1. Monte Carlo distribution of the locked Stable Floor (Mode B 60/40, realizable basis) at retirement\n"
                 "10,000 paths per cohort, full joint resampling from 1929-2025 historical universe",
                 fontsize=11)
    cohort_titles = {
        "A": "Cohort A (born 1960, retire 2025)",
        "B": "Cohort B (born 1970, retire 2035)",
        "C": "Cohort C (born 1980, retire 2045)",
        "D": "Cohort D (born 1990, retire 2055)",
    }
    for ax, name in zip(axes.flat, ["A", "B", "C", "D"]):
        b_iid   = results[(name, "1929-2025", "iid")]   / 1000   # convert to thousands
        b_block = results[(name, "1929-2025", "block")] / 1000
        bench   = BENCHMARKS[name]
        det     = det_central[name]
        med     = bench["med"]
        p50_b   = np.percentile(b_block, 50) * 1000

        # Plot histograms with shared x-axis
        upper = np.percentile(b_iid, 99)
        bins = np.linspace(0, upper, 60)
        ax.hist(b_iid,   bins=bins, density=True, alpha=0.6, color="steelblue",
                label="IID bootstrap")
        ax.hist(b_block, bins=bins, density=True, alpha=0.6, color="darkseagreen",
                label="Block bootstrap (5-yr)")
        ax.axvline(med / 1000, color="crimson", linestyle="--", lw=2,
                   label=f"Median actual + DB (${med//1000}K)")
        ax.axvline(det / 1000, color="forestgreen", linestyle=":", lw=2.4,
                   label=f"Deterministic central (${det/1000:.0f}K)")
        ax.axvline(p50_b / 1000, color="orange", linestyle="-", lw=1.2,
                   label=f"Block P50 (${p50_b/1000:.0f}K)")
        ax.set_xlim(0, upper)
        ax.set_title(cohort_titles[name], fontsize=10)
        ax.set_xlabel("Stable Floor at age 65 (2025$ thousands)")
        ax.set_ylabel("Density")
        ax.legend(fontsize=8, loc="upper right")
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(fname, dpi=120)
    plt.close()
    print(f"  wrote {fname}")


# =============================================================================
# Figure M2 - Percentile bands box-style with deterministic overlaid
# =============================================================================
def fig_M2(results, det_central, fname="figure_M2_percentile_bands_v3.png"):
    fig, ax = plt.subplots(figsize=(10, 6.5))
    fig.suptitle("Figure M2. Monte Carlo percentile bands by cohort vs. deterministic figures\n"
                 "Block bootstrap (5-yr blocks), 1929-2025 universe, 10,000 paths",
                 fontsize=11)
    xs = []
    p5s, p25s, p50s, p75s, p95s = [], [], [], [], []
    dets, meds = [], []
    labels = []
    for i, name in enumerate(["A", "B", "C", "D"]):
        b = results[(name, "1929-2025", "block")] / 1000
        xs.append(i)
        p5s.append(np.percentile(b, 5))
        p25s.append(np.percentile(b, 25))
        p50s.append(np.percentile(b, 50))
        p75s.append(np.percentile(b, 75))
        p95s.append(np.percentile(b, 95))
        dets.append(det_central[name] / 1000)
        meds.append(BENCHMARKS[name]["med"] / 1000)
        born = {"A": 1960, "B": 1970, "C": 1980, "D": 1990}[name]
        labels.append(f"Cohort {name}\n(born {born})")
    xs = np.array(xs)
    # IQR boxes
    for i in xs:
        ax.add_patch(plt.Rectangle((i - 0.35, p25s[i]), 0.7, p75s[i] - p25s[i],
                                   color="navajowhite", alpha=0.9))
    # Whiskers
    for i in xs:
        ax.plot([i, i], [p5s[i], p25s[i]], color="grey", lw=1)
        ax.plot([i, i], [p75s[i], p95s[i]], color="grey", lw=1)
        ax.plot([i - 0.1, i + 0.1], [p5s[i], p5s[i]], color="grey", lw=1)
        ax.plot([i - 0.1, i + 0.1], [p95s[i], p95s[i]], color="grey", lw=1)
    # P50 markers
    ax.scatter(xs, p50s, color="black", s=70, zorder=5, label="MC P50 (block bootstrap)")
    # Deterministic centrals
    ax.scatter(xs, dets, marker="D", color="forestgreen", s=110, zorder=5,
               label="Deterministic central scenario")
    # Median actual benchmarks
    ax.scatter(xs, meds, marker="s", color="crimson", s=80, zorder=5,
               label="Median actual + DB pension")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Stable Floor at age 65 (2025$ thousands)")
    ax.legend(loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(fname, dpi=120)
    plt.close()
    print(f"  wrote {fname}")


# =============================================================================
# Figure M3 - P(<median) bars across configurations
# =============================================================================
def fig_M3(results, fname="figure_M3_p_below_median_v3.png"):
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.suptitle("Figure M3. Probability that the framework falls below median actual retirement outcome\n"
                 "Across cohorts and bootstrap configurations",
                 fontsize=11)
    configs = [
        ("1929-2025", "iid",   "1929-2025, IID",   "steelblue"),
        ("1929-2025", "block", "1929-2025, Block", "sandybrown"),
        ("1960-2025", "iid",   "1960-2025, IID",   "lightsteelblue"),
        ("1960-2025", "block", "1960-2025, Block", "wheat"),
    ]
    cohorts = ["A", "B", "C", "D"]
    bar_width = 0.18
    xs = np.arange(len(cohorts))
    for j, (uni, meth, label, color) in enumerate(configs):
        probs = []
        for name in cohorts:
            b = results[(name, uni, meth)]
            probs.append((b < BENCHMARKS[name]["med"]).mean() * 100)
        offset = (j - 1.5) * bar_width
        ax.bar(xs + offset, probs, width=bar_width, label=label, color=color,
               edgecolor="black", lw=0.5)
        for x, v in zip(xs + offset, probs):
            ax.text(x, v + 0.4, f"{v:.1f}%", ha="center", fontsize=8)
    ax.set_xticks(xs)
    ax.set_xticklabels([f"Cohort {c}" for c in cohorts])
    ax.set_ylabel("P(locked Stable Floor, Mode B 60/40 realizable basis < median actual retirement wealth)")
    ax.set_ylim(0, max(35, ax.get_ylim()[1]))
    ax.legend(loc="upper right")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(fname, dpi=120)
    plt.close()
    print(f"  wrote {fname}")


# =============================================================================
# Figure M4 - P50 and P5 by configuration
# =============================================================================
def fig_M4(results, det_central, fname="figure_M4_p50_p5_sensitivity_v3.png"):
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle("Figure M4. Sensitivity of the locked Stable Floor (Mode B 60/40, realizable basis) to bootstrap configuration\n"
                 "P50 (central tendency, left) and P5 (adverse tail, right) across 4 configurations",
                 fontsize=11)
    configs = [
        ("1929-2025", "iid"),
        ("1929-2025", "block"),
        ("1960-2025", "iid"),
        ("1960-2025", "block"),
    ]
    labels = ["29-25 IID", "29-25 Block", "60-25 IID", "60-25 Block"]
    colors = ["steelblue", "sandybrown", "lightseagreen", "thistle"]
    cohorts = ["A", "B", "C", "D"]
    xs = np.arange(len(cohorts))
    bar_width = 0.18

    # Left: P50
    for j, ((uni, meth), label, color) in enumerate(zip(configs, labels, colors)):
        p50s = [np.percentile(results[(name, uni, meth)], 50) / 1000 for name in cohorts]
        offset = (j - 1.5) * bar_width
        ax_l.bar(xs + offset, p50s, width=bar_width, label=label, color=color,
                 edgecolor="black", lw=0.5)
    det_p50 = [det_central[name] / 1000 for name in cohorts]
    ax_l.scatter(xs, det_p50, marker="D", color="forestgreen", s=110, zorder=5,
                 label="Deterministic central")
    ax_l.set_xticks(xs)
    ax_l.set_xticklabels([f"Cohort {c}" for c in cohorts])
    ax_l.set_ylabel("P50 Stable Floor at age 65 (2025$ thousands)")
    ax_l.set_title("Median (P50) outcome by configuration")
    ax_l.legend(loc="upper left", fontsize=8)
    ax_l.grid(axis="y", alpha=0.3)

    # Right: P5
    for j, ((uni, meth), label, color) in enumerate(zip(configs, labels, colors)):
        p5s = [np.percentile(results[(name, uni, meth)], 5) / 1000 for name in cohorts]
        offset = (j - 1.5) * bar_width
        ax_r.bar(xs + offset, p5s, width=bar_width, label=label, color=color,
                 edgecolor="black", lw=0.5)
    # Median benchmarks as dashed horizontal segments per cohort
    for i, name in enumerate(cohorts):
        m = BENCHMARKS[name]["med"] / 1000
        ax_r.hlines(m, i - 0.4, i + 0.4, colors="crimson", linestyles="--",
                    lw=1.5, label="Median actual + DB" if i == 0 else None)
    ax_r.set_xticks(xs)
    ax_r.set_xticklabels([f"Cohort {c}" for c in cohorts])
    ax_r.set_ylabel("P5 Stable Floor at age 65 (2025$ thousands)")
    ax_r.set_title("Adverse-tail (P5) outcome by configuration")
    ax_r.legend(loc="upper left", fontsize=8)
    ax_r.grid(axis="y", alpha=0.3)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(fname, dpi=120)
    plt.close()
    print(f"  wrote {fname}")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    import time, os
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")
    os.makedirs(out_dir, exist_ok=True)
    os.chdir(out_dir)

    print("Running Monte Carlo (10,000 paths per configuration)...")
    t0 = time.time()
    results = run_all(n_paths=10000)
    print(f"  Done in {time.time() - t0:.1f}s.\n")

    det = get_deterministic_central()
    print(f"Deterministic central-scenario figures:")
    for name in ["A", "B", "C", "D"]:
        bench = BENCHMARKS[name]
        v = det[name]
        print(f"  Cohort {name}: ${v:>12,.0f}  "
              f"({v/bench['med']:.2f}x med, {v/bench['mean']:.2f}x mean)")
    print()

    print("Generating figures...")
    fig_M1(results, det)
    fig_M2(results, det)
    fig_M3(results)
    fig_M4(results, det)
    print("\nDone.")
