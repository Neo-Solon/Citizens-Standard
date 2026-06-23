"""
make_figures.py
===============
One figure per episode: actual CPI (BLS) vs the framework PREVENTION response
(central + demand-share band), plus the RESPONSE path (Tool 14 capacity only,
the honest slower line), with anchor and Tool 14 trigger marked.

Run:  python make_figures.py  ->  ../figures/figure_T14_{2022,1980}.png
"""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from data import EPISODES, DEMAND_SHARE_1980, demand_share_2022, ANCHOR_CPI, TRIGGER_OVER
from tool14_engine import prevention_path, response_path, summarize

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
RED, GOLD, GREEN, GREY = "#C0392B", "#C8941E", "#3F8E6B", "#9AA3AE"


def share_for(key, r):
    return (lambda t: demand_share_2022(t, r)) if key == "2022" else r


def regimes(key):
    return [0.0, 0.5, 1.0] if key == "2022" else \
           [DEMAND_SHARE_1980["low"], DEMAND_SHARE_1980["central"], DEMAND_SHARE_1980["high"]]


def make_one(key):
    ep = EPISODES[key]; actual = ep["cpi"]; months = list(range(len(actual)))
    central = 0.0 if key == "2022" else DEMAND_SHARE_1980["central"]
    prev_c, *_ = prevention_path(actual, share_for(key, central))
    band = [prevention_path(actual, share_for(key, r))[0] for r in regimes(key)]
    lo = [min(p[t] for p in band) for t in months]
    hi = [max(p[t] for p in band) for t in months]
    resp = response_path(actual)

    fig, ax = plt.subplots(figsize=(8.6, 4.7))
    ax.fill_between(months, lo, hi, color=GOLD, alpha=0.16, label="Prevention band (demand-share)")
    ax.plot(months, actual, color=RED, lw=2.4, label="Actual (BLS CPI-U)")
    ax.plot(months, prev_c, color=GOLD, lw=2.8, label="Framework, prevention (central)")
    ax.plot(months, resp, color=GREY, lw=1.8, ls=(0, (5, 2)),
            label="Tool 14 response only (capacity-bounded)")
    ax.axhline(ANCHOR_CPI, color=GREEN, lw=1.0, ls=":", label="Near-zero anchor")
    ax.axhline(ANCHOR_CPI + TRIGGER_OVER, color=GREY, lw=0.9, ls="--", label="Tool 14 trigger")

    s = summarize(actual, share_for(key, central))
    sub = "SF Fed monthly demand share" if key == "2022" else "Fed monetary attribution"
    ax.set_title(f"Tool 14 vs. the {key} inflation   (actual {s['actual_peak']:.1f}%  ->  "
                 f"prevention {s['prevention_peak']:.1f}%)   [{sub}]", fontsize=10.5)
    ax.set_xlabel(f"Months from onset ({ep['start']})")
    ax.set_ylabel("CPI inflation, % YoY")
    ax.set_ylim(0, max(actual) + 1.5)
    ax.legend(fontsize=7.5, loc="upper right", framealpha=0.9)
    ax.grid(alpha=0.15)
    fig.tight_layout()
    p = os.path.join(OUT, f"figure_T14_{key}.png"); fig.savefig(p, dpi=130); plt.close(fig)
    return p


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k in ("2022", "1980"):
        print("wrote", make_one(k))
