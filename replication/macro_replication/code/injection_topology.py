"""
injection_topology.py -- Cantillon injection-topology diffusion model.
Companion to Section [6.6] and Proposition 1: does the distributional outcome
of monetary injection depend on WHERE money enters the spending network
(topology) rather than HOW MUCH enters (scale)?

Part A (stylized): agents on a Watts-Strogatz small-world graph; each period
every agent spends fraction s of balances equally to neighbors at the current
global price P_t; P adjusts with speed lam toward the quantity-theory level.
One-shot injection of 10% of the money stock at the max-degree hub vs
uniformly. Advantage = cumulative real consumption minus the no-injection
counterfactual, grouped by shortest-path distance from the hub.

Part B (calibrated): Barabasi-Albert scale-free graph (Fedwire-consistent
core-periphery injection layer, Soramaki et al. 2007); lam in {0.07, 0.11,
0.23} from median price durations of 14.5 / 8-11 / 4.3 months (Kehoe-Midrigan
2015; Nakamura-Steinsson 2008; Bils-Klenow 2004); s in {0.11, 0.45} bracketing
M2-type vs transactional velocity; 23% of the money stock injected as a
12-month flow (US M2 grew >23% YoY in 2020, pre-2020 record <15%); and a
2020-21 replica mixing 75% hub / 25% uniform (QE plus direct checks).

The dynamics are linear in balances, so superposition holds exactly:
mixed-channel outcomes are convex combinations of the pure channels.

Caveats (also in README): one good, one global price, quantity-theory anchor,
fixed spend fraction, no behavioral response. The Fedwire evidence grounds the
injection-layer topology, not the full household spending graph, which is
unobserved. Mechanism demonstration with grounded parameters, not measurement.
"""
import json
import os
import numpy as np
import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")
os.makedirs(RESULTS, exist_ok=True)

SEED = 42
N = 500
M0 = 100.0
P0 = 1.0


def spend_matrix(G):
    A = nx.to_numpy_array(G)
    deg = A.sum(axis=1)
    return A / deg[:, None], int(np.argmax(deg))


def distances(G, hub):
    return np.array([nx.shortest_path_length(G, hub, j) for j in range(N)])


# ---------------- Part A: stylized (one-shot, WS graph) ----------------
S_A = 0.30
T_A = 120


def run_oneshot(W, hub, m_inj, mode, lam, order="spend_first"):
    m = np.full(N, M0)
    if mode == "hier":
        m[hub] += m_inj
    elif mode == "unif":
        m += m_inj / N
    P_star = m.sum() / (N * M0)
    P = P0
    real = np.zeros(N)
    for t in range(T_A):
        if order == "price_first":
            P = P + lam * (P_star - P)
        spend = S_A * m
        real += spend / P
        m = m - spend + W.T @ spend
        if order == "spend_first":
            P = P + lam * (P_star - P)
    return real


def near_far(adv, dist):
    md = dist.max()
    near = float(np.mean([adv[dist == d].mean() for d in (0, 1)]))
    far = float(np.mean([adv[dist == d].mean() for d in (md - 1, md)]))
    return near, far


G = nx.watts_strogatz_graph(N, 6, 0.1, seed=SEED)
W, hub = spend_matrix(G)
dist = distances(G, hub)
MINJ_A = 0.10 * N * M0

out = {"params_A": {"N": N, "K": 6, "p_rewire": 0.1, "s": S_A, "T": T_A,
                    "seed": SEED, "inj_frac": 0.10, "max_distance": int(dist.max())}}

print("PART A -- STYLIZED (WS graph, one-shot 10% injection, lam=0.05)")
lam0 = 0.05
tiers = {}
for mode in ["hier", "unif"]:
    adv = (run_oneshot(W, hub, MINJ_A, mode, lam0)
           - run_oneshot(W, hub, 0, "none", lam0))
    per_tier = {}
    for d in range(int(dist.max()) + 1):
        idx = dist == d
        per_tier[d] = {"n": int(idx.sum()),
                       "adv_pc": float(adv[idx].mean()),
                       "share": float(adv[idx].sum() / adv.sum())}
    tiers[mode] = per_tier
    n, f = near_far(adv, dist)
    print(f"  {mode:4s}: near_pc={n:.1f} far_pc={f:.1f} gradient={n - f:.1f}")
out["A_tiers"] = tiers
print(f"  hier tier advs: " + " ".join(
    f"d{d}={tiers['hier'][d]['adv_pc']:.1f}" for d in sorted(tiers['hier'])))

print("A2 -- topology vs scale (share stability across injection sizes)")
share_rows = []
for frac in [0.05, 0.10, 0.20, 0.40]:
    adv = (run_oneshot(W, hub, frac * N * M0, "hier", lam0)
           - run_oneshot(W, hub, 0, "none", lam0))
    share_rows.append([float(adv[dist == d].sum() / adv.sum())
                       for d in range(int(dist.max()) + 1)])
share_mat = np.array(share_rows)
h = np.array([tiers["hier"][d]["share"] for d in sorted(tiers["hier"])])
u = np.array([tiers["unif"][d]["share"] for d in sorted(tiers["unif"])])
max_std = float(share_mat.std(axis=0).max())
max_diff = float(np.abs(h - u).max())
print(f"  max tier-share std across scales 5%-40% = {max_std:.4f}")
print(f"  max tier-share diff hier vs uniform    = {max_diff:.4f}")
out["A_scale"] = {"max_share_std_across_scales": max_std,
                  "max_share_diff_hier_vs_uniform": max_diff}

print("A3 -- price-adjustment-speed sweep (hier)")
sweep = {}
for lam in [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]:
    adv = (run_oneshot(W, hub, MINJ_A, "hier", lam)
           - run_oneshot(W, hub, 0, "none", lam))
    n, f = near_far(adv, dist)
    sweep[str(lam)] = {"near_pc": n, "far_pc": f, "gradient": n - f,
                       "total": float(adv.sum())}
    print(f"  lam={lam:>4}: gradient={n - f:9.1f} total={adv.sum():10.1f}")
g0 = sweep["0.0"]["gradient"]
g1 = sweep["1.0"]["gradient"]
print(f"  gradient retention lam 0 -> 1: {100 * g1 / g0:.1f}%  "
      f"(total collapses {sweep['0.0']['total']:.0f} -> {sweep['1.0']['total']:.0f})")
out["A_lam_sweep"] = sweep

print("A4 -- robustness")
adv = (run_oneshot(W, hub, MINJ_A, "hier", 1.0, order="price_first")
       - run_oneshot(W, hub, 0, "none", 1.0, order="price_first"))
n, f = near_far(adv, dist)
print(f"  price-first ordering, lam=1.0: gradient={n - f:.1f} total={adv.sum():.1f}"
      f"  (zero aggregate windfall, redistribution persists)")
out["A_rob_ordering"] = {"gradient": n - f, "total": float(adv.sum())}
rob_seeds = {}
for sd in [7, 123, 2024]:
    Gs = nx.watts_strogatz_graph(N, 6, 0.1, seed=sd)
    Ws, hs = spend_matrix(Gs)
    ds = distances(Gs, hs)
    adv = (run_oneshot(Ws, hs, MINJ_A, "hier", 0.05)
           - run_oneshot(Ws, hs, 0, "none", 0.05))
    n, f = near_far(adv, ds)
    rob_seeds[sd] = {"gradient": n - f}
    print(f"  seed {sd}: gradient={n - f:.1f}")
out["A_rob_seeds"] = rob_seeds
rob_ba = {}
for sd in [42, 7]:
    Gx = nx.barabasi_albert_graph(N, 3, seed=sd)
    Wx, hx = spend_matrix(Gx)
    dx = distances(Gx, hx)
    adv = (run_oneshot(Wx, hx, MINJ_A, "hier", 0.05)
           - run_oneshot(Wx, hx, 0, "none", 0.05))
    n, f = near_far(adv, dx)
    rob_ba[sd] = {"gradient": n - f, "max_dist": int(dx.max())}
    print(f"  BA graph seed {sd}: gradient={n - f:.1f} (max_dist={dx.max()})")
out["A_rob_graph_family"] = rob_ba

# A5 -- MECHANISM: why the gradient survives instant price adjustment.
# Two candidate channels: (a) price-timing (near agents buy at stale prices),
# (b) balance dilution (the price level rises for everyone from t=0; near agents
# are compensated by new money arriving first, far agents are not). Decisive test:
# hold the price at its final level for ALL t, so there are ZERO stale-price
# purchases by construction. If the gradient persists, (a) is ruled out.
Pf = (N * M0 + MINJ_A) / (N * M0)


def run_fixed_price(m_inj, P, mode):
    m = np.full(N, M0)
    if mode == "hier":
        m[hub] += m_inj
    real = np.zeros(N)
    for t in range(T_A):
        spend = S_A * m
        real += spend / P
        m = m - spend + W.T @ spend
    return real


print("A5 -- mechanism decomposition (instant price, no stale-price purchases)")
# hier priced at Pf throughout; baseline priced at its own level 1.0
adv_instant = run_fixed_price(MINJ_A, Pf, "hier") - run_fixed_price(0, 1.0, "none")
n_i, f_i = near_far(adv_instant, dist)
# channel split: dilution_i = baseline_i * (1/Pf - 1), an exact proportional haircut;
# new-money_i = adv_i - dilution_i, the real value of injected money reaching i.
base10 = run_fixed_price(0, 1.0, "none")
dilution = run_fixed_price(0, Pf, "none") - base10
newmoney = adv_instant - dilution
dilution_frac = float((1 / Pf - 1))
dilution_flat = float(dilution.std() / abs(dilution.mean()))   # ~0 => uniform haircut
newmoney_grad_corr = float(np.corrcoef(newmoney, -dist)[0, 1])
identity_err = float(np.abs(dilution - base10 * (1 / Pf - 1)).max())
print(f"  instant-price gradient survives: {n_i - f_i:.1f} "
      f"(vs gradual {sweep['0.05']['gradient']:.1f}); aggregate windfall {adv_instant.sum():.2f}")
print(f"  dilution is a flat proportional haircut of {dilution_frac * 100:.2f}% "
      f"(cross-tier std/mean {dilution_flat:.3f}); identity err {identity_err:.1e}")
print(f"  the gradient lives entirely in the new-money-reaching-i term "
      f"(corr with proximity {newmoney_grad_corr:.3f})")
out["A5_mechanism"] = {
    "instant_price_gradient": n_i - f_i,
    "instant_aggregate_windfall": float(adv_instant.sum()),
    "dilution_proportional_haircut_pct": dilution_frac * 100,
    "dilution_cross_tier_std_over_mean": dilution_flat,
    "dilution_identity_max_err": identity_err,
    "newmoney_proximity_corr": newmoney_grad_corr,
    "reading": ("At instant adjustment there are no stale-price purchases, yet the "
                "gradient persists. The price rise is a flat proportional real haircut "
                "on every agent's own consumption; the redistribution is entirely in "
                "which agents the new nominal money reaches first. Timing channel ruled "
                "out; dilution/first-recipient channel confirmed.")}

# ---------------- Part B: calibrated (flow, BA graph) ----------------
T_B = 60
Gb = nx.barabasi_albert_graph(N, 3, seed=SEED)
Wb, hubb = spend_matrix(Gb)
distb = distances(Gb, hubb)
MINJ_B = 0.23 * N * M0


def run_flow(m_inj_total, mode, lam, s, inj_months=12, mix_u=0.0):
    m = np.full(N, M0)
    P = P0
    real = np.zeros(N)
    per = m_inj_total / inj_months if inj_months else 0
    for t in range(T_B):
        if mode != "none" and t < inj_months:
            if mode == "hier":
                m[hubb] += per
            elif mode == "unif":
                m += per / N
            elif mode == "mix":
                m[hubb] += per * (1 - mix_u)
                m += per * mix_u / N
        P_star = m.sum() / (N * M0)
        spend = s * m
        real += spend / P
        m = m - spend + Wb.T @ spend
        P = P + lam * (P_star - P)
    return real


print("PART B -- CALIBRATED (BA graph, 23% of M over 12 months, T=60 months)")
grid = {}
for lam, lsrc in [(0.07, "Kehoe-Midrigan 14.5mo"),
                  (0.11, "Nakamura-Steinsson 8-11mo"),
                  (0.23, "Bils-Klenow 4.3mo")]:
    for s, ssrc in [(0.11, "M2-type velocity"), (0.45, "transactional velocity")]:
        base = run_flow(0, "none", lam, s)
        row = {"lam_source": lsrc, "s_source": ssrc}
        for mode in ["hier", "unif"]:
            adv = run_flow(MINJ_B, mode, lam, s) - base
            n, f = near_far(adv, distb)
            row[mode] = {"near_pc": n, "far_pc": f, "gradient": n - f,
                         "total": float(adv.sum())}
        grid[f"lam={lam},s={s}"] = row
        ratio = row["hier"]["gradient"] / row["unif"]["gradient"] \
            if row["unif"]["gradient"] != 0 else float("inf")
        print(f"  lam={lam} s={s}: hier grad={row['hier']['gradient']:8.1f}  "
              f"unif grad={row['unif']['gradient']:7.1f}  "
              f"far_pc(hier)={row['hier']['far_pc']:7.1f}")
out["B_grid"] = grid

base = run_flow(0, "none", 0.11, 0.11)
advm = run_flow(MINJ_B, "mix", 0.11, 0.11, mix_u=0.25) - base
advh = run_flow(MINJ_B, "hier", 0.11, 0.11) - base
nm, fm = near_far(advm, distb)
nh, fh = near_far(advh, distb)
red = 100 * (1 - (nm - fm) / (nh - fh))
print(f"B2 -- 2020-21 replica mix (75% hub / 25% uniform), lam=0.11 s=0.11:")
print(f"  mix gradient={nm - fm:.1f} vs pure-hier {nh - fh:.1f}: "
      f"reduction={red:.1f}% (linear by superposition)")
out["B_mix"] = {"mix_gradient": nm - fm, "hier_gradient": nh - fh,
                "reduction_pct": red}

with open(os.path.join(RESULTS, "injection_topology_results.json"), "w") as f:
    json.dump(out, f, indent=2)
print("wrote results/injection_topology_results.json")
