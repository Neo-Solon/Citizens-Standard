"""
The Citizens Standard - the liquidation flow L_t, computed.

Paper 5 (Macro Model), Prop 1:   P_t = M^T_t * V / Y_t
  -> price stability requires M^T to grow with Y.
  -> "The transactional circuit is fed by the liquidation flow L_t - the conversion of matured
      floor balances into spendable income... The issuance rule and the liquidation flow are
      JOINTLY CALIBRATED so that M^T tracks Y."

Paper 1 (Architecture), the circulating-pool ceiling:
  -> "K3 + KI + liquidation must remain within the Y-matched expansion of the circulating pool."

L_t is NEVER given a number in any of the 14 papers. Paper 5 s3.5 concedes the exposure:
  -> "Pure Mode B (KI=0) is price-stable in steady state ... but has weak short-run
      stabilization, RELYING ON L_t BEING ON-TARGET by balanced-growth construction."

This computes L_t and evaluates the constraint. No framework parameter is changed.

The framework already computes this quantity, in
replication/empirical_replication/code/demographic_flow_model.py:
      wd[retire:] = w * floor[retire:]
      ret_consumption = wd[retire:].sum()
but uses it only for Paper 8's asset-price question. It is never pointed at the price level.

Two inputs upgraded to real data:
  * mortality: SSA period life table (real l_x, single year of age) replaces "everyone dies at 85"
  * mu = M^T/M2 measured from the framework's own M^A construction (FRED)

ACCOUNTING (the crux):
  K1,K2,K3 are NEW money -> raise M2.  K1,K2 land in M^A; K3 lands in M^T.
  L_t is NOT new money: the retiree sells equity to a buyer paying with EXISTING money.
  L_t is a TRANSFER M^A -> M^T. It leaves M2 unchanged and raises M^T.
  That is why it never shows up in a quantity-of-money check -- and why it lands squarely
  on P = M^T * V / Y.
"""
import json
import numpy as np

M2_0, GDP_0, POP_0 = 22366.0, 30800.0, 342.0   # $B, $B, M   (engine)
MU_0    = 0.5135      # M^T/M2, Paper 10 (engine hardcode)
G_R     = 0.020       # real growth (engine)
N_POP   = 0.005       # population growth (engine)
K1_RATE = 0.025       # K1 = 2.5% of GDP/cap, once per new citizen
R_REAL  = 0.0426      # Mode B realizable return (Macro 6.7)
KAPPA_D = 0.40        # Mode B 60/40
W_DRAW  = 0.04        # framework's own default in demographic_flow_model.py
RETIRE  = 65
KAPPA_W = 0.03        # MPC out of asset wealth (Macro: 0.02-0.05)
MAXAGE  = 100

def load_survival(path="data/ssa_life_table_2022.csv"):
    lx = {}
    with open(path) as fh:
        next(fh)
        for line in fh:
            p = line.strip().split(",")
            lx[int(p[0])] = float(p[5])
    l = np.array([lx[a] for a in range(MAXAGE + 1)])
    return l / l[0]

def stable_population(l, n, total):
    a = np.arange(len(l), dtype=float)
    w = l * (1.0 + n) ** (-a)
    return w / w.sum() * total

def run(w_draw=W_DRAW, kappa_d=KAPPA_D, r=R_REAL, years=125, kd_sched=None, survival=None):
    l = survival if survival is not None else load_survival()
    surv = np.ones(MAXAGE + 1); surv[1:] = l[1:] / l[:-1]
    pop = stable_population(l, N_POP, POP_0)
    floor = np.zeros(MAXAGE + 1)
    M2, GDP = M2_0, GDP_0
    MT = MU_0 * M2_0; MA = M2 - MT
    keys = ("year","L","K3","spill","inflow","required","excess","pi","MT","MA","M2","mu",
            "floor_stock","kappa_d","retiree_share","floor_at_65")
    out = {k: [] for k in keys}
    for t in range(years):
        POP = pop.sum(); GDPpc = GDP*1e9/(POP*1e6)
        kd = kappa_d if kd_sched is None else kd_sched(t)
        budget = G_R * M2
        K1agg  = K1_RATE * GDPpc * (pop[0]*1e6) / 1e9
        after  = max(budget - K1agg, 0.0)
        K2agg  = (1-kd) * after
        K3agg  = kd * after
        workers = pop[:RETIRE]
        if workers.sum() > 0:
            floor[:RETIRE] += K2agg*1e9/(workers.sum()*1e6)
        floor[0] += K1_RATE * GDPpc
        floor *= (1.0 + r)
        wd = np.zeros(MAXAGE+1); wd[RETIRE:] = w_draw * floor[RETIRE:]
        L = float((wd[RETIRE:]*pop[RETIRE:]*1e6).sum()/1e9)
        floor[RETIRE:] -= wd[RETIRE:]
        floor_stock = float((floor*pop*1e6).sum()/1e9)
        s_t = min(1.0, floor_stock/max(GDP*2.0,1e-9))
        spill = min(KAPPA_W*(K2agg/MU_0)*(1.0-s_t), 200.0)
        inflow   = L + K3agg + spill
        required = G_R * MT
        pi       = inflow/MT - G_R
        for k,v in (("year",2026+t),("L",L),("K3",K3agg),("spill",spill),("inflow",inflow),
                    ("required",required),("excess",inflow-required),("pi",pi*100),
                    ("MT",MT),("MA",MA),("M2",M2),("mu",MT/M2),("floor_stock",floor_stock),
                    ("kappa_d",kd),("retiree_share",float(pop[RETIRE:].sum()/POP)),
                    ("floor_at_65",float(floor[RETIRE]))):
            out[k].append(v)
        MA = MA + (K1agg + K2agg) - L - spill
        MT = MT + inflow
        M2 = MA + MT
        # --- age the population with REAL mortality; bequests are INHERITED, not destroyed ---
        # (floor[] is per-capita; if we merely shift it, the dead's balances vanish and the
        #  floor stock -- and therefore L_t -- is understated. Recycle them into the heirs.)
        deaths = pop[:-1]*(1.0-surv[1:])
        bequest = float((deaths*floor[:-1]*1e6).sum()/1e9)       # $B released by the dead
        newborns = POP*N_POP + (pop*(1-surv)).sum()
        pop[1:] = pop[:-1]*surv[1:]; floor[1:] = floor[:-1]
        pop[0] = max(newborns,0.0); floor[0] = 0.0
        w2 = pop[:RETIRE]
        if w2.sum() > 0 and bequest > 0:
            floor[:RETIRE] += bequest*1e9/(w2.sum()*1e6)          # heirs are working-age
        GDP *= (1.0 + G_R)
    return {k: np.array(v) for k,v in out.items()}
