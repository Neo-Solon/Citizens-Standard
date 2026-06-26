"""
Stage 2 -- cross-check the plateau against the closed-form identity, test the
active-float threshold (price discovery), and state the honest verdict.
"""
import numpy as np

def sim(c,dur,g,years=250):
    market=1.0; buys=[]
    for t in range(years):
        market*=(1+g); buys.append(c*market)
        if len(buys)>dur: buys.pop(0)
        last=sum(buys)/market
    return last
def closed(c,dur,g):
    return c*sum((1/(1+g))**k for k in range(int(dur)))

print("="*76)
print("PLATEAU CROSS-CHECK + FLOAT THRESHOLD + VERDICT")
print("="*76)
print("Simulation vs closed-form psi* = c * annuity(g, dur):")
for c,dur in [(0.0039,40),(0.0039,30),(0.0050,40),(0.0030,25)]:
    s=sim(c,dur,0.02); cf=closed(c,dur,0.02)
    print(f"  c={c:.2%} dur={dur}y: sim {s:.1%} vs closed {cf:.1%}  ({'match' if abs(s-cf)<0.002 else 'DIFF'})")
print()
print("Active float left at the plateau (price-discovery margin):")
for label,psi in [("central 10.9%",0.109),("high corner ~21%",0.21)]:
    print(f"  {label}: active float = {1-psi:.0%}  (discovery concerns bite ~40-50%+ passive)")
print()
print("="*76)
print("HONEST VERDICT")
print("="*76)
print("""
 This one largely VINDICATES Paper 8, with one nuance.

 1. The plateau is REAL (Proposition 4 holds). Ownership converges and never runs
    toward 1 in any swept case -- cohort decumulation structurally bounds the share.
    The 'permanent buyer eventually owns everything' objection is genuinely defeated.

 2. The simulation reproduces the paper's psi* = c*annuity(g,dur) identity exactly,
    and the central plateau (verified 0.39% flow, ~40y duration, 2% growth) is 10.9%
    -- squarely in the paper's stated 0.09-0.11 bracket. The number is sound.

 3. NUANCE (the honest addition): the plateau LEVEL is duration- and flow-sensitive,
    ranging ~6% (short duration / low flow) to ~21% (long duration / high floor-
    weighting). The paper's ~10% is the central case of that range, not a fixed
    point; at long holding durations it could reach the high-teens to ~20%. Still a
    clear minority -- active float stays ~79-94% across the whole range, well above
    the ~40-50% passive-ownership level where price-discovery concerns bite -- so the
    float-threshold claim (price discovery survives) holds throughout.

 BOTTOM LINE: the structural-buyer endgame is bounded as the paper argues. The
 decumulation mechanism works, the ~10% plateau is a fair central estimate, and
 price discovery is preserved. The one amendment is to present the plateau as a
 ~6-21% range centered near 10%, duration-driven, rather than a single number --
 which if anything makes the bound more credible by showing its sensitivity.
""")
