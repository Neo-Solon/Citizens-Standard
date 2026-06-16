"""
make_determinacy_figure.py
--------------------------
Reproduces figure_P3prime_determinacy.png — the three-panel determinacy figure
for Section 3.6 / Proposition 3' of Neo-Solon (2026e):
  (a) determinacy region in the gain / money-share plane,
  (b) gap dynamics by regime after a unit price-path shock,
  (c) the maturing-circuit drift of effective psi*lambda, M2-indexed vs M^T-indexed.
A visual companion to the closed-form Proposition 3'.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

INK = "#1a1a2e"; WARM = "#b0413e"; GOLD = "#c08a2e"; GREEN = "#3a6b4f"; GREY = "#8a8a8a"


def main():
    plt.rcParams.update({"font.family": "serif", "font.size": 10,
                         "axes.edgecolor": INK, "axes.linewidth": 0.8})
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    lam0 = 0.5

    # (a) determinacy region with the psi=1.8 baseline marker
    ax = axes[0]; share = np.linspace(0.06, 1.0, 400)
    ax.fill_between(share, 0, share, color=GREEN, alpha=.20)
    ax.fill_between(share, share, np.minimum(2 * share, 1.0), color=GOLD, alpha=.22)
    ax.fill_between(share, np.minimum(2 * share, 1.0), 1.0, color=WARM, alpha=.20)
    ax.plot(share, share, color=GREEN, lw=1.6); ax.plot(share, 2 * share, color=WARM, lw=1.6)
    ax.axhline(lam0, color=INK, ls="--", lw=1.1)
    ax.text(0.95, lam0 + 0.02, r"baseline $\lambda=0.5$", ha="right", fontsize=8.5, color=INK)
    ax.plot(1 / 1.8, lam0, "o", color=INK, ms=6, zorder=5)
    ax.annotate("baseline\n(psi=1.8, psi*lam=0.90)".replace("psi", "ψ").replace("*lam", "λ"),
                (1 / 1.8, lam0), xytext=(0.74, 0.33), fontsize=7.6, ha="center", color=INK,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.plot(0.25, lam0, "o", color=INK, ms=6, zorder=5)
    ax.annotate("matured\n(ψ↑)", (0.25, lam0), xytext=(0.25, 0.66), fontsize=7.6,
                ha="center", color=INK, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.set_xlim(0.06, 1); ax.set_ylim(0, 1)
    ax.set_xlabel(r"transactional share  $M^{T}/M_{2}$"); ax.set_ylabel(r"closure gain  $\lambda$")
    ax.set_title("(a)  Determinacy region", fontsize=11, color=INK, loc="left")
    ax.legend(handles=[Patch(facecolor=GREEN, alpha=.3, label=r"monotone  ($\psi\lambda<1$)"),
                       Patch(facecolor=GOLD, alpha=.35, label=r"damped osc.  ($1<\psi\lambda<2$)"),
                       Patch(facecolor=WARM, alpha=.3, label=r"divergent  ($\psi\lambda\geq2$)")],
              fontsize=7.6, loc="upper left", frameon=False)

    # (b) gap dynamics by regime
    ax = axes[1]

    def sim(g, T=22, x0=1.0):
        x = [x0]
        for _ in range(T):
            x.append((1 - g) * x[-1])
        return np.array(x)
    for g, c, nm in [(0.90, GREEN, r"$\psi\lambda=0.90$  baseline (monotone)"),
                     (1.5, GOLD, r"$\psi\lambda=1.5$  damped osc."),
                     (2.3, WARM, r"$\psi\lambda=2.3$  divergent")]:
        ax.plot(sim(g), "o-", color=c, ms=3, lw=1.4, label=nm)
    ax.axhline(0, color=GREY, lw=.7); ax.set_ylim(-2.2, 1.4)
    ax.set_xlabel("years after a unit price-path shock"); ax.set_ylabel(r"price-path gap  $x_t$")
    ax.set_title("(b)  Gap dynamics by regime", fontsize=11, color=INK, loc="left")
    ax.legend(fontsize=7.8, loc="lower right", frameon=False)

    # (c) maturing-circuit drift
    ax = axes[2]; t = np.arange(61)
    ratio = 0.8 + 3.2 / (1 + np.exp(-0.16 * (t - 34)))
    psiL = (1 + ratio) * lam0
    ax.plot(t, psiL, color=WARM, lw=2.0, label=r"$M_2$-indexed rule")
    ax.axhline(lam0, color=GREEN, lw=2.0, label=r"$M^{T}$-indexed remedy ($\psi_{\rm eff}=1$)")
    ax.axhline(1, color=INK, ls=":", lw=1); ax.axhline(2, color=INK, ls="--", lw=1)
    ax.text(1, 1.05, "oscillation onset (ψλ=1)", fontsize=7.3, color=INK)
    ax.text(1, 2.05, "divergence (ψλ=2)", fontsize=7.3, color=INK)
    ax.plot(0, psiL[0], "o", color=WARM, ms=6); ax.text(2, psiL[0] - 0.12, "launch 0.90", fontsize=7.3, color=WARM)
    ax.fill_between(t, 2, psiL, where=(psiL >= 2), color=WARM, alpha=.12)
    ax.set_ylim(0, 3.2); ax.set_xlim(0, 60)
    ax.set_xlabel("years since launch"); ax.set_ylabel(r"effective $\psi\lambda$")
    ax.set_title("(c)  Maturing-circuit drift", fontsize=11, color=INK, loc="left")
    ax.legend(fontsize=8, loc="center right", frameon=False)

    for ax in axes:
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.tick_params(labelsize=8.5)
    fig.suptitle("Determinacy of the KI price-path rule: structural pass-through "
                 "$\\psi=M_2/M^{T}$ and the maturing-circuit stability condition",
                 fontsize=11.5, color=INK, y=1.02)
    fig.tight_layout()
    out_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "figure_P3prime_determinacy.png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"wrote {os.path.normpath(out)}")


if __name__ == "__main__":
    main()
