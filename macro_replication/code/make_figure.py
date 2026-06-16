"""
make_figure.py
--------------
Generates figure_P3_convergence_regimes.png: gap-closure trajectories
x_t = (1 - psi*lambda)^t x_0 across the three regimes of Proposition 3
(Neo-Solon 2026e, Appendix A.2). A visual companion to the closed-form proof.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

from verify_proposition_3 import simulate_gap


def main():
    lam = 0.5
    periods = 24
    cases = [
        (0.50, "psi*lambda = 0.25  (monotone)",            "#1a6fa8"),
        (1.00, "psi*lambda = 0.50  (monotone, baseline)",  "#2e8b57"),
        (2.10, "psi*lambda = 1.05  (damped oscillation)",  "#d98a2b"),
        (4.00, "psi*lambda = 2.00  (marginal)",            "#8a4fa0"),
        (4.20, "psi*lambda = 2.10  (divergent)",           "#b03030"),
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    for psi, label, color in cases:
        path = simulate_gap(psi, lam, x0=1.0, periods=periods, noise=0.0)
        ax.plot(range(periods + 1), path, marker="o", ms=3, lw=1.6,
                color=color, label=label)

    ax.axhline(0.0, color="#888888", lw=0.8, ls="--")
    ax.set_xlabel("Period t")
    ax.set_ylabel("Log price-path gap  $x_t$")
    ax.set_title("Proposition 3 — path-targeting convergence regimes ($\\lambda = 0.5$)")
    ax.set_ylim(-1.6, 1.6)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(alpha=0.25)
    fig.tight_layout()

    out_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "figure_P3_convergence_regimes.png")
    fig.savefig(out, dpi=150)
    print(f"wrote {os.path.normpath(out)}")


if __name__ == "__main__":
    main()
