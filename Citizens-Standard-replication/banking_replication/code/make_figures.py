"""
Publication-quality figures for Paper 6 (Full-Reserve Banking).
Three figures, each matched to its in-text caption. Clean academic styling:
consistent serif-free typography, muted palette, panel labels (a)/(b),
no decorative titles (the caption lives in the paper text).
Numbers are imported from the verified model in paper6_model.py.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 10.5,
    "axes.titleweight": "bold",
    "axes.labelsize": 9.5,
    "axes.edgecolor": "#333333",
    "axes.linewidth": 0.8,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
})
BLUE, LBLUE, GREY, RED, GREEN, INK = "#2E74B5", "#9DC3E6", "#9AA0A6", "#C0392B", "#2E8B57", "#222222"

# ---- verified anchors (from paper6_model.py) ----
M2 = 22.366
DEP = 18.0
inside_today = DEP / M2                 # ~0.80
term = 0.60 * M2                        # 13.42
equity = term / 3                       # 4.47
cap = term + equity                     # 17.89
TERM_SHARE = 0.60

def panel_label(ax, s):
    ax.text(-0.08, 1.06, s, transform=ax.transAxes, fontsize=11, fontweight="bold", va="top")

# ============================ FIGURE 1 ============================
# (a) inside-money share today vs CS; (b) M_T decomposition fractional vs full-reserve
fig, ax = plt.subplots(1, 2, figsize=(9.0, 3.5))

ax[0].bar([0, 1], [inside_today, 0.0], color=[GREY, BLUE], width=0.58, edgecolor=INK, linewidth=0.6)
ax[0].set_xticks([0, 1]); ax[0].set_xticklabels(["Incumbent\n(fractional reserve)", "Citizens Standard\n(full reserve)"])
ax[0].set_ylabel("inside money as share of the money stock"); ax[0].set_ylim(0, 1.0)
ax[0].text(0, inside_today + 0.03, "~0.8", ha="center", fontsize=9.5)
ax[0].text(1, 0.03, "0", ha="center", fontsize=9.5)
ax[0].spines[["top", "right"]].set_visible(False)
panel_label(ax[0], "(a)")

# (b) M_T decomposition: fractional = M_o + d_T*D ; full = M_o
Mo = 1.0; dTD = 0.55                    # illustrative units (M_o normalized to 1)
ax[1].bar([0], [Mo], color=BLUE, width=0.58, edgecolor=INK, linewidth=0.6, label="outside money $M_o$")
ax[1].bar([0], [dTD], bottom=[Mo], color=LBLUE, width=0.58, edgecolor=INK, linewidth=0.6, label="bank-created $d_T\\cdot D$")
ax[1].bar([1], [Mo], color=BLUE, width=0.58, edgecolor=INK, linewidth=0.6)
ax[1].set_xticks([0, 1]); ax[1].set_xticklabels(["Fractional\n$M_T=M_o+d_T D$", "Full reserve\n$M_T=M_o$"])
ax[1].set_ylabel("price-relevant transactional money $M_T$ (index)")
ax[1].set_ylim(0, 1.85); ax[1].legend(fontsize=7.5, loc="upper right", frameon=False)
ax[1].spines[["top", "right"]].set_visible(False)
panel_label(ax[1], "(b)")

fig.tight_layout()
fig.savefig("figure1.png")
plt.close(fig)

# ============================ FIGURE 2 ============================
# (a) bank credit capacity = term + equity (4:1); (b) credit-clearing frontier
fig, ax = plt.subplots(1, 2, figsize=(9.0, 3.5))

ax[0].bar([0], [term], color=LBLUE, width=0.5, edgecolor=INK, linewidth=0.6, label="term deposits")
ax[0].bar([0], [equity], bottom=[term], color=BLUE, width=0.5, edgecolor=INK, linewidth=0.6, label="bank equity")
ax[0].set_xticks([0]); ax[0].set_xticklabels(["bank credit capacity"])
ax[0].set_ylabel("$ trillion"); ax[0].set_ylim(0, 21)
ax[0].text(0, term/2, f"${term:.1f}T", ha="center", va="center", color=INK, fontsize=9)
ax[0].text(0, term+equity/2, f"${equity:.1f}T", ha="center", va="center", color="white", fontsize=9)
ax[0].text(0, cap+0.5, f"${cap:.1f}T total (4:1)", ha="center", fontsize=9)
ax[0].legend(fontsize=8, loc="upper left", frameon=False)
ax[0].spines[["top", "right"]].set_visible(False)
panel_label(ax[0], "(a)")

# (b) frontier under a 30% term-deposit shortfall
r0, es, ed = 3.0, 0.01, 0.04
C0 = cap; S0 = 0.70 * cap
def C_of_r(r): return C0 * (1 - ed * (r - r0))
def S_of_r(r): return S0 * (1 + es * (r - r0))
rstar = r0 + (C0 - S0) / (S0 * es + C0 * ed)
rg = np.linspace(r0, rstar, 120)
offset = [max(0.0, (C_of_r(r) - S_of_r(r)) / C_of_r(r)) * 100 for r in rg]
ax[1].plot(np.array(rg) - r0, offset, color=RED, lw=2.4)
ax[1].scatter([0], [offset[0]], color=BLUE, s=55, zorder=6, edgecolor=INK, linewidth=0.6)
ax[1].annotate("hold the loan rate:\nsovereign citizen-channel\noffset (TLF / KT / KI$_T$)",
               (0, offset[0]), fontsize=7.6, xytext=(0.35, offset[0] - 11), color="#1A4A73")
ax[1].annotate("let the rate clear:\ncredit crunch\n($\\approx$6pp, $-$25%)",
               (rstar - r0, 0), fontsize=7.6, xytext=(rstar - r0 - 3.0, 4.5), color="#7A1F15",
               ha="left")
ax[1].set_xlabel("loan-rate premium (percentage points)")
ax[1].set_ylabel("credit funded by sovereign offset (%)")
ax[1].set_xlim(-0.3, rstar - r0 + 0.3); ax[1].set_ylim(0, 34)
ax[1].spines[["top", "right"]].set_visible(False)
panel_label(ax[1], "(b)")

fig.tight_layout()
fig.savefig("figure2.png")
plt.close(fig)

# ============================ FIGURE 3 ============================
# max systemic money contraction: 1930-33 vs CS (term share)
fig, ax = plt.subplots(figsize=(5.4, 3.5))
ax.bar([0, 1], [1.0, TERM_SHARE], color=[RED, GREEN], width=0.55, edgecolor=INK, linewidth=0.6)
ax.set_xticks([0, 1]); ax.set_xticklabels(["1930–33 run\n(all deposits runnable)", "Citizens Standard\n(term layer only)"])
ax.set_ylabel("maximum systemic money contraction\n(share of the money stock)")
ax.set_ylim(0, 1.12)
ax.text(0, 1.03, "~100%", ha="center", fontsize=9.5)
ax.text(1, TERM_SHARE + 0.03, f"~{TERM_SHARE:.0%}", ha="center", fontsize=9.5)
ax.axhspan(0, TERM_SHARE, color=GREEN, alpha=0.06)
ax.annotate("reserved transaction layer\ncannot be run", (1, 0.30), fontsize=7.6, ha="center", color="#1d5c39")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("figure3.png")
plt.close(fig)

# report dimensions for embedding
from PIL import Image
for f in ("figure1.png", "figure2.png", "figure3.png"):
    w, h = Image.open(f).size
    print(f"{f}: {w}x{h}  aspect {w/h:.3f}")
print("done")
