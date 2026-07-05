"""
growth_scenario.py
==================
Illustrative scaling of the Citizens Standard dividend channels with the real
growth rate. This is a COMPARATIVE STATIC, not a forecast: it reports the
per-citizen dividend implied at launch parameters by a given real growth rate g,
for each dividend-paying channel. It exists to show that the constitutional
issuance rule SCALES CONTINUOUSLY and stays price-stable by construction -- not
to predict any growth rate.

Two honest distinctions the calculation makes explicit:
  * Only the K2 / growth channel scales with g. Mode B's split dividend and the
    full growth-matched ceiling both rise with real growth.
  * The Mode C KI dividend is FLAT (1.98% of M2, ~$108/mo) and does NOT scale
    with growth -- it is a fixed inflationary channel, not a growth-linked one.
  * The full growth-matched dividend carries zero inflation BY CONSTRUCTION
    (issuance defined equal to real growth), an identity of the k2=1.0 rule,
    not an empirical result.

All dollar figures use the launch anchors (M2, GDP, population) documented below.
Run:  python3 growth_scenario.py
"""

# launch anchors (same as the architecture engine)
M2 = 22366.2e9        # $22.37T money stock (the issuance base -- NOT GDP)
GDP = 30762.099e9     # $30.76T nominal GDP
POP = 341.8e6         # population
NC = 0.011703         # new-citizen (K1 recipient) share
K1 = 0.025            # K1 endowment fraction of GDP/capita
KAPPA_D = 0.40        # Mode B dividend share of the growth-matched budget
KI_RATE = 0.0198      # Mode C KI: flat 1.98% of M2 (does NOT scale with growth)

GROWTH_RATES = [0.02, 0.03, 0.05, 0.08, 0.10, 0.15, 0.20]


def k1_total():
    return K1 * (GDP / POP) * POP * NC


def growth_matched_pool(g):
    """The full real-growth-matched issuance available for dividend, net of K1."""
    return max(0.0, 1.0 * M2 * g - k1_total())


def per_citizen_month(pool):
    return (pool / POP) / 12.0


def scenario_row(g):
    full_pool = growth_matched_pool(g)
    full_mo = per_citizen_month(full_pool)          # price-stable ceiling (k2=1.0)
    modeB_mo = per_citizen_month(KAPPA_D * full_pool)  # Mode B split dividend
    ki_mo = per_citizen_month(KI_RATE * M2)         # Mode C KI: FLAT, growth-independent
    infl_full = 1.0 * g - g                          # = 0 by construction
    return dict(g=g, full_mo=full_mo, modeB_mo=modeB_mo, ki_mo=ki_mo, infl_full=infl_full)


def main():
    print("=" * 74)
    print("DIVIDEND SCALING WITH REAL GROWTH  (comparative static, launch parameters)")
    print("  Illustrative, NOT a forecast. Issuance is a share of M2 scaled by REAL")
    print("  growth -- not a share of GDP.")
    print("=" * 74)
    print(f"  {'real g':>7}{'Mode B split':>15}{'full ceiling':>15}{'Mode C KI':>13}"
          f"{'inflation':>13}")
    print(f"  {'':>7}{'(growth-linked)':>15}{'(k2=1, price-':>15}{'(flat, not':>13}"
          f"{'(full)':>13}")
    print(f"  {'':>7}{'':>15}{'stable max)':>15}{'growth-linked)':>13}{'':>13}")
    print("  " + "-" * 70)
    for g in GROWTH_RATES:
        r = scenario_row(g)
        print(f"  {g:>6.0%}"
              f"{'$'+format(round(r['modeB_mo']),',')+'/mo':>15}"
              f"{'$'+format(round(r['full_mo']),',')+'/mo':>15}"
              f"{'$'+format(round(r['ki_mo']),',')+'/mo':>13}"
              f"{'0.0%':>13}")
    print("  " + "-" * 70)
    print("  Notes:")
    print("  - Mode C KI is constant across g: it is a fixed 1.98%-of-M2 inflationary")
    print("    dividend, NOT tied to growth. Only the K2/growth channel scales with g.")
    print("  - The full ceiling's 0.0% inflation is an IDENTITY of the k2=1.0 rule")
    print("    (issuance defined equal to real growth), not an empirical finding.")
    print("  - Sustained high real growth (e.g. 10-20%) for a large mature economy is")
    print("    historically unprecedented; these rows show the RULE does not break,")
    print("    not that such growth is expected.")


def make_figure(outpath="../figures/paper9_growth_scaling.png"):
    """Regenerate the Paper 9 §7 figure from the same anchors as the table."""
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "figure.dpi": 120, "font.size": 12, "axes.titlesize": 13,
        "axes.titleweight": "bold", "axes.spines.top": False,
        "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25,
        "legend.frameon": True, "legend.framealpha": 0.9,
    })
    # house palette: Mode B green, Mode C orange; a neutral for the ceiling
    C_B, C_C, C_CEIL = "#16a34a", "#ea580c", "#334155"

    gs = [g * 100 for g in GROWTH_RATES]
    rows = [scenario_row(g) for g in GROWTH_RATES]
    modeB = [r["modeB_mo"] for r in rows]
    full = [r["full_mo"] for r in rows]
    ki = [r["ki_mo"] for r in rows]

    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    ax.plot(gs, full, "o-", color=C_CEIL, lw=2.4,
            label="Full growth-matched ceiling (price-stable, k\u2082=1)")
    ax.plot(gs, modeB, "s-", color=C_B, lw=2.4,
            label="Mode B split dividend (\u03ba_d = 0.4)")
    ax.plot(gs, ki, "^--", color=C_C, lw=2.0,
            label="Mode C KI (flat 1.98% of M2 \u2014 not growth-linked)")

    ax.set_xlabel("real annual growth rate  g  (%)")
    ax.set_ylabel("dividend per citizen ($/month)")
    ax.set_title("Dividend scaling with real growth (comparative static, not a forecast)")
    ax.set_xticks(gs)
    ax.legend(loc="upper left", fontsize=10)
    # honest annotation: the ceiling is price-stable BY CONSTRUCTION
    ax.annotate("full dividend carries 0% inflation\nby construction (issuance \u2261 real growth)",
                xy=(15, full[-2]), xytext=(2.4, 720),
                fontsize=9, color=C_CEIL,
                arrowprops=dict(arrowstyle="->", color=C_CEIL, lw=1))
    fig.tight_layout()

    os.makedirs(os.path.dirname(os.path.abspath(
        os.path.join(os.path.dirname(__file__), outpath))), exist_ok=True)
    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), outpath)
    fig.savefig(dest, bbox_inches="tight")
    plt.close(fig)
    return dest


if __name__ == "__main__":
    import sys
    if "--figure" in sys.argv:
        print("figure written:", make_figure())
    else:
        main()
