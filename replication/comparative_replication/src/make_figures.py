"""
make_figures.py - two figures that back the distinctive-cell claim with real numbers.

Fig 1: annual per-person cash benefit (USD/yr), dividend/flow systems only.
Fig 2: owned, compounding wealth stock per person (USD); flow systems own nothing.

Both figures annotate the systems that differ in kind rather than hiding them,
so the chart cannot be misread as a single-winner ranking.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from data import (ALASKA, SOCIAL_SECURITY, UBI, CITIZENS_STANDARD)


def f(x):
    return x.value


INK = "#10161C"; AMBER = "#E6A93E"; TEAL = "#3FAE92"; DIM = "#9AA3AE"; RED = "#C0563B"


def fig_annual_benefit(path):
    labels = ["UBI\n($1k/mo proposal)", "Social Security\n(avg, contributory)",
              "Alaska PFD\n(avg dividend)", "Citizens Std\n(Mode C)", "Citizens Std\n(Mode B)"]
    vals = [f(UBI["canonical_monthly_usd"]) * 12,
            f(SOCIAL_SECURITY["avg_benefit_usd_mo"]) * 12,
            f(ALASKA["dividend_avg_usd"]),
            f(CITIZENS_STANDARD["dividend_modeC_usd_yr"]),
            f(CITIZENS_STANDARD["dividend_modeB_usd_yr"])]
    cols = [DIM, DIM, TEAL, AMBER, AMBER]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, vals, color=cols, edgecolor=INK, linewidth=0.6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 250, f"${v:,.0f}", ha="center",
                va="bottom", fontsize=9, color=INK)
    ax.set_ylabel("Annual per-person benefit (real USD/yr)")
    ax.set_title("Annual per-person cash benefit, where systems are comparable",
                 fontsize=11, color=INK)
    ax.annotate("Social Security is contributory & retirement-only,\n"
                "not a universal working-age flow; Georgism pays no\n"
                "per-person benefit (funding source) and is omitted.",
                xy=(0.97, 0.74), xycoords="axes fraction", ha="right", va="top",
                fontsize=7.5, color=DIM,
                bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=DIM, lw=0.5))
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, max(vals) * 1.18)
    plt.tight_layout()
    fig.savefig(path, dpi=140); plt.close(fig)


def fig_wealth_stock(path):
    labels = ["UBI", "Social Security", "Alaska\n(fund/resident)",
              "Citizens Std\n(Mode A)", "Citizens Std\n(Mode B)"]
    vals = [0, 0,
            round(f(ALASKA["fund_value_usd"]) / f(ALASKA["recipients"])),
            f(CITIZENS_STANDARD["floor_modeA_usd"]),
            f(CITIZENS_STANDARD["floor_modeB_usd"])]
    cols = [RED, RED, TEAL, AMBER, AMBER]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, vals, color=cols, edgecolor=INK, linewidth=0.6)
    for b, v in zip(bars, vals):
        txt = "$0\n(no owned stock)" if v == 0 else f"${v:,.0f}"
        ax.text(b.get_x() + b.get_width()/2, v + 4000, txt, ha="center",
                va="bottom", fontsize=8.5, color=(RED if v == 0 else INK))
    ax.set_ylabel("Owned, compounding wealth stock per person (real USD)")
    ax.set_title("Owned wealth stock per person: only the wealth-building systems compare",
                 fontsize=11, color=INK)
    ax.annotate("UBI and Social Security build no owned stock\n"
                "(Social Security: no property right, Flemming v. Nestor).\n"
                "Alaska is proven; the Citizens Standard floor is theoretical.",
                xy=(0.03, 0.96), xycoords="axes fraction", ha="left", va="top",
                fontsize=7.5, color=DIM,
                bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=DIM, lw=0.5))
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, max(vals) * 1.2)
    plt.tight_layout()
    fig.savefig(path, dpi=140); plt.close(fig)


if __name__ == "__main__":
    fig_annual_benefit("../results/fig_annual_benefit.png")
    fig_wealth_stock("../results/fig_wealth_stock.png")
    print("wrote results/fig_annual_benefit.png and results/fig_wealth_stock.png")
