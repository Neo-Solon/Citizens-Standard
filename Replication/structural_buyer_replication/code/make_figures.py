# Paper 8 (The Structural Buyer) — figure generation.
# Every curve here reproduces the SAME math checked in the verify_*.py scripts:
#   - Prop 1 (verify_prop1_premium.py): Q_{t+1}=(1-theta*phi)Q_t + theta(A*+phi*Qb);
#       premium = A*/phi; converges iff 0 < theta*phi < 2.
#   - psi-plateau (verify_psi_plateau.py): psi* = c * annuity(g,dur), annuity=dur if g==0
#       else (1-(1+g)**-dur)/g; -> saturates at c/g as dur->inf. Mode B (dur=40): zero-growth
#       c*dur~0.20, realized psi*~0.12 at g=2%, ceiling c/g~0.25.
#   - A* scale (paper sec 2.2 / 10.1): A* ~ $272B/yr ~ 0.39% of ~$69T equity market cap (Mode B 60/40).
# Figures carry NO "Figure N" in the image; the number lives in the docx caption.
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)

BLUE, RED, GREEN, GREY = "#1f4e79", "#c0392b", "#2e8b57", "#888888"
plt.rcParams.update({"font.size": 11, "axes.titlesize": 12,
                     "axes.grid": True, "grid.alpha": 0.3})


def fig_premium_stability():
    """Prop 1: finite premium A*/phi (left) and convergence band 0<theta*phi<2 (right)."""
    A = 0.39   # calibrated Mode B rate: A* = $272B / $69.1T = 0.39% of market cap
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.4))

    # Left: premium = A*/phi, decreasing & finite for all phi>0
    phi = np.linspace(0.15, 2.0, 400)
    axL.plot(phi, A / phi, color=BLUE, lw=2.2)
    axL.scatter([0.5], [A / 0.5], color=RED, zorder=5)
    axL.annotate("illustrative calibration\n$\\phi=0.5 \\Rightarrow$ premium $=A^*/\\phi=0.78$",
                 xy=(0.5, A / 0.5), xytext=(0.78, 2.05),
                 arrowprops=dict(arrowstyle="->", color=GREY), fontsize=9)
    axL.set_xlabel("Mean-reversion strength $\\phi$")
    axL.set_ylabel("Valuation premium  $Q^*-Q_{base}=A^*/\\phi$")
    axL.set_title("Premium is finite and decreasing in $\\phi$")
    axL.set_ylim(0, 3.2)

    # Right: Q_t paths for theta*phi in {0.5,1.0,1.5} (converge) and 2.5 (diverge)
    phi0, Qb, T = 0.5, 1.0, 28
    Qstar = Qb + A / phi0
    for tp, c, ls, npts in [(0.5, GREEN, "-", T), (1.0, BLUE, "-", T), (1.5, "#e08a1e", "-", T), (2.5, RED, "--", 6)]:
        theta = tp / phi0
        Q, path = Qb, []
        for _ in range(npts):
            path.append(Q)
            Q = (1 - theta * phi0) * Q + theta * (A + phi0 * Qb)
        axR.plot(range(npts), path, color=c, ls=ls, lw=2,
                 label=f"$\\theta\\phi={tp}$" + ("  (diverges)" if tp == 2.5 else ""))
    axR.axhline(Qstar, color=GREY, ls=":", lw=1)
    axR.annotate("fixed point $Q^*$", xy=(T * 0.62, Qstar), xytext=(T * 0.42, Qstar + 0.55), fontsize=9,
                 arrowprops=dict(arrowstyle="->", color=GREY))
    axR.set_xlabel("Repricing periods (quarters)")
    axR.set_ylabel("Valuation $Q_t$")
    axR.set_title("Converges iff $0<\\theta\\phi<2$")
    axR.set_ylim(0.5, 3.2)
    axR.legend(fontsize=8, loc="upper right")

    fig.suptitle("The bounded valuation fixed point of the structural buyer (Proposition 1)",
                 fontsize=12.5, y=1.02)
    fig.tight_layout()
    p = os.path.join(OUT, "figure_prop1_premium_stability.png")
    fig.savefig(p, dpi=150, bbox_inches="tight"); plt.close(fig)
    print("wrote", os.path.basename(p))


def fig_psi_plateau():
    """psi* = c*annuity(g,dur); linear at g=0, saturates at c/g for g>0."""
    # base case = kappa_d=0 max-absorption gross rate (0.65% of ~$69T, Wilshire/CRSP);
    # high-deposit c=0.015 sensitivity. Realized Mode-B share is lower (psi*~0.10, App. A.6).
    c_base, c_high = 0.0065, 0.015
    dur = np.arange(1, 61)

    def annuity(g, d):
        return d if g == 0 else (1 - (1 + g) ** (-d)) / g

    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    for g, col, lab in [(0.0, BLUE, "g = 0%  ($\\psi^*=c\\cdot dur$, conservative bound)"),
                        (0.02, GREEN, "g = 2%  (plateaus at $c/g$)"),
                        (0.05, RED, "g = 5%  (plateaus at $c/g$)")]:
        y = [c_base * annuity(g, d) for d in dur]
        ax.plot(dur, y, color=col, lw=2.2, label=lab)
        if g > 0:
            ax.axhline(c_base / g, color=col, ls=":", lw=1, alpha=0.7)

    # base case (kappa_d=0, dur=30) and high-deposit sensitivity markers
    ax.scatter([30], [c_base * 30], color=BLUE, zorder=6)
    ax.annotate("base: $c=0.0065,\\ dur=30 \\Rightarrow \\psi^*\\approx0.20$",
                xy=(30, c_base * 30), xytext=(3.5, 0.30), fontsize=9,
                arrowprops=dict(arrowstyle="->", color=GREY))
    ax.scatter([30], [c_high * 30], color=GREY, zorder=6)
    ax.annotate("high-deposit: $c=0.015 \\Rightarrow \\psi^*=0.45$",
                xy=(30, c_high * 30), xytext=(20, 0.50), fontsize=9,
                arrowprops=dict(arrowstyle="->", color=GREY))

    ax.set_xlabel("Decumulation duration  $dur$  (years)")
    ax.set_ylabel("Steady-state decumulation bound  $\\psi^*$")
    ax.set_title("The decumulation bound $\\psi^*=c\\cdot$annuity$(g,dur)$ saturates under growth")
    ax.set_ylim(0, 0.6)
    ax.legend(fontsize=9, loc="lower right")
    fig.tight_layout()
    p = os.path.join(OUT, "figure_psi_plateau.png")
    fig.savefig(p, dpi=150, bbox_inches="tight"); plt.close(fig)
    print("wrote", os.path.basename(p))


def fig_astar_scale():
    """A* ~ $272B/yr ~ 0.39% of ~$69T equity market cap (Mode B); cumulative ownership build under Prop 2."""
    A_star = 272.0          # $B/yr (paper sec 10.1, Mode B 60/40)
    mkt_cap = A_star / 0.00394 / 1000.0  # ~ $69T implied by the 0.39% figure

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.3),
                                   gridspec_kw={"width_ratios": [1, 1.25]})

    # Left: the annual bid as a share of market cap
    axL.bar([0], [mkt_cap * 1000], width=0.5, color="#d9e2ec", edgecolor=GREY, label="US equity market cap (~$69T)")
    axL.bar([0], [A_star], width=0.5, color=BLUE, label="annual structural bid $A^*$ (~$272B)")
    axL.set_xticks([]); axL.set_ylabel("$ billion")
    axL.set_title("$A^*$ is a persistent ~0.39%/yr bid")
    axL.legend(fontsize=8, loc="upper right")
    axL.annotate("0.39% of market cap", xy=(0, A_star), xytext=(0.28, 12000),
                 fontsize=9, arrowprops=dict(arrowstyle="->", color=GREY))

    # Right: cumulative ownership share if A* reinvested at constant market cap (illustrative, Prop 2 float-constant)
    yrs = np.arange(0, 41)
    share = 1 - (1 - 0.00394) ** yrs  # compounding the annual absorption share
    axR.plot(yrs, share * 100, color=GREEN, lw=2.2)
    axR.set_xlabel("Years"); axR.set_ylabel("Cumulative public ownership share (%)")
    axR.set_title("Steady absorption accrues ownership (illustrative)")
    axR.set_ylim(0, 30)

    fig.suptitle("Scale of the structural buyer in perspective", fontsize=12.5, y=1.02)
    fig.tight_layout()
    p = os.path.join(OUT, "figure_astar_scale.png")
    fig.savefig(p, dpi=150, bbox_inches="tight"); plt.close(fig)
    print("wrote", os.path.basename(p))


if __name__ == "__main__":
    fig_premium_stability()
    fig_psi_plateau()
    fig_astar_scale()
    print("done")
