"""
make_labor_figure.py
--------------------
Reproduces figure_P4_labor_growth.png — the three-panel labor-supply figure
for Section 5.5 / Proposition 4 of Neo-Solon (2026e):
  (a) labor ratio l(b) for a range of Frisch elasticities nu,
  (b) labor reduction vs floor size, liquid vs locked (the lock is load-bearing),
  (c) the self-correcting labor-growth loop (a contraction) under a growth-indexed flow.
Pure-Python solver (no SciPy); matplotlib for rendering.
"""
import os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK="#1a1a2e"; WARM="#b0413e"; GOLD="#c08a2e"; GREEN="#3a6b4f"; GREY="#8a8a8a"

def lr(b, nu):
    if b <= 0: return 1.0
    f = lambda l: l**(1+1/nu) + b*l**(1/nu) - 1.0
    lo, hi = 1e-12, 1.0
    for _ in range(200):
        m = 0.5*(lo+hi)
        if f(m) > 0: hi = m
        else:        lo = m
    return 0.5*(lo+hi)

plt.rcParams.update({"font.family":"serif","font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8})
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))

# (a)
a = ax[0]; bs = np.linspace(0, 0.8, 200)
for nu, c in [(0.25, GREEN), (0.5, INK), (1.0, WARM)]:
    a.plot(bs, [lr(b, nu) for b in bs], lw=1.8, color=c, label=r"$\nu=%.2f$" % nu)
a.axvspan(0.0, 0.16, color=GOLD, alpha=.15)
a.text(0.08, 0.96, "locked\noperating\nrange", ha="center", va="top", fontsize=7.4, color="#8a6a1e")
a.set_xlim(0, 0.8); a.set_ylim(0.7, 1.005)
a.set_xlabel(r"spendable floor income / labor income  $b$"); a.set_ylabel(r"labor ratio  $\ell=h/h^\star$")
a.set_title("(a)  Labor response to the floor", fontsize=11, color=INK, loc="left")
a.legend(fontsize=8, loc="upper right", frameon=False, title="Frisch elasticity")

# (b)
b = ax[1]; nu = 0.5; r = 0.045; m = np.linspace(0, 20, 200)
b.plot(m, [(1-lr(r*x, nu))*100 for x in m], lw=2.0, color=WARM, label="liquid (full return, $b=rm$)")
b.plot(m, [(1-lr(0.010*x, nu))*100 for x in m], lw=2.0, color=GREEN, label=r"locked, $\kappa_d$ distributes $\approx$1%")
b.plot(m, [(1-lr(0.002*x, nu))*100 for x in m], lw=1.6, color=INK, ls="--", label=r"locked, $\kappa_d\!\to\!0$ + bequest")
b.axvline(16, color=GREY, ls=":", lw=1)
b.text(15.4, 22.5, "floor ≈ 16× income", fontsize=7.4, color=GREY, rotation=90, va="top", ha="right")
b.plot(16, (1-lr(r*16, nu))*100, "o", color=WARM, ms=6); b.annotate("−19%", (16, 19.1), xytext=(12.3, 20.4), fontsize=8.5, color=WARM)
b.plot(16, (1-lr(0.010*16, nu))*100, "o", color=GREEN, ms=6); b.annotate("−5%", (16, 5.1), xytext=(17.0, 7.0), fontsize=8.5, color=GREEN)
b.set_xlim(0, 20); b.set_ylim(0, 24)
b.set_xlabel(r"floor as multiple of annual labor income  $m=F/(\omega h^\star)$"); b.set_ylabel("labor reduction  (%)")
b.set_title("(b)  The lock is load-bearing", fontsize=11, color=INK, loc="left")
b.legend(fontsize=7.6, loc="upper left", frameon=False)

# (c)
c = ax[2]; nu = 0.5; eps_g = 0.5; gstar = 1.0; b0 = 0.10
def step(g): return gstar*(1 + eps_g*(lr(b0*(g/gstar), nu) - 1))
for g0, c0, lab in [(0.60, GREEN, "start below"), (0.999, GOLD, r"start near $g^\star$")]:
    tr = [g0]
    for _ in range(8): tr.append(step(tr[-1]))
    c.plot(range(9), tr, "o-", color=c0, ms=4, lw=1.6, label=lab)
gfp = 0.6
for _ in range(40): gfp = step(gfp)
h = 1e-5; gain = abs((step(gfp+h) - step(gfp-h))/(2*h))
c.axhline(gfp, color=INK, ls=":", lw=1)
c.text(8.0, gfp-0.028, "fixed point\n$g/g^\\star\\approx%.3f$" % gfp, fontsize=7.6, color=INK, ha="right")
c.axhline(1.0, color=GREY, lw=.8); c.text(0.1, 1.006, r"$g^\star$", fontsize=9, color=GREY)
c.text(4.4, 0.74, "loop gain $\\approx%.3f$\n(contraction)" % gain, fontsize=8, color=INK, ha="center",
       bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GREY, lw=0.6))
c.set_ylim(0.55, 1.06); c.set_xlabel("iteration"); c.set_ylabel(r"growth  $g_t/g^\star$")
c.set_title("(c)  Level effect, self-corrected", fontsize=11, color=INK, loc="left")
c.legend(fontsize=7.8, loc="center right", frameon=False)

for a_ in ax:
    a_.spines["top"].set_visible(False); a_.spines["right"].set_visible(False); a_.tick_params(labelsize=8.5)
fig.suptitle("Labor supply under a locked citizen floor: a bounded level effect, not a growth collapse "
             r"(Frisch $\nu$, lock factor $\rho_{\rm eff}/r$)", fontsize=11.5, color=INK, y=1.02)
fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "figures", "figure_P4_labor_growth.png")
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print("wrote %s ; loop gain=%.4f fixed point=%.4f" % (os.path.normpath(out), gain, gfp))
