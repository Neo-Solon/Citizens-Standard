"""
Stage 2 -- what assumptions reproduce Paper 3's Year-30/Year-45 milestones, and are
they plausible? Sweep KT share, real growth, and avg interest rate across defensible
ranges; report the year debt/GDP hits 39% and 15%. Honest verdict on whether the
paper's path is reachable or systematically optimistic.
"""
DEBT0_PCT=1.00; GDP0=29000.0; M2_0=21500.0

def run_path(real_growth, infl, avg_rate, kt_share, years=60):
    debt=DEBT0_PCT*GDP0; gdp=GDP0; m2=M2_0; path=[]
    for y in range(1,years+1):
        ng=real_growth+infl; gdp*=(1+ng); m2*=(1+ng)
        kt=kt_share*max(0,real_growth)*m2
        debt=debt+avg_rate*debt-kt
        floored = debt < 0.15*gdp
        if floored: debt=0.15*gdp
        path.append((y,100*debt/gdp))
    return path

def year_at(path,t):
    for y,d in path:
        if d<=t: return y
    return None

print("="*78)
print("WHAT REPRODUCES PAPER 3's PATH? (target: 39% by ~Y30, 15% by ~Y45)")
print("="*78)
print(f"{'real g':>7} {'rate':>6} {'KT share':>9} {'Y@39%':>7} {'Y@15%':>7}  {'verdict':>22}")
scenarios=[
    (0.020,0.033,0.6),  # central
    (0.020,0.033,0.8),  # higher KT
    (0.020,0.033,1.0),  # max KT (all growth budget to retirement)
    (0.027,0.033,0.6),  # CBO-high growth
    (0.027,0.030,0.8),  # high growth + low rate + high KT
    (0.030,0.028,1.0),  # optimistic corner
    (0.018,0.040,0.6),  # pessimistic (low growth, high rate)
]
for g,r,k in scenarios:
    p=run_path(g,r,0.023 if True else 0,k) if False else run_path(g,0.023,r,k)
    y39=year_at(p,39); y15=year_at(p,15.5)
    if y39 and y39<=32 and y15 and y15<=47: v="MATCHES paper"
    elif y39 and y39<=35: v="close-ish"
    else: v="slower than paper"
    print(f"{g:>7.1%} {r:>6.1%} {k:>9.1f} {str(y39):>7} {str(y15):>7}  {v:>22}")

print()
print("="*78)
print("HONEST VERDICT")
print("="*78)
print("""
 1. The paper's 102% -> 39% (Y30) -> 15% (Y45) path is REACHABLE but
    OPTIMISTIC-LEANING. It holds only when either the KT channel absorbs nearly the
    FULL growth-matched issuance budget (KT share ~1.0) or real growth runs at the
    high end of the CBO range (~2.7%+). Under genuinely central assumptions with a
    moderate KT share (0.6), retirement to 39% takes ~Year 40, not Year 30, and the
    15% floor is not reached within the horizon.

 2. There is a budget tension the headline glosses: the paper promises citizen
    K1/K2 channels run at FULL price stability THROUGHOUT the transition, but
    reproducing the fast path needs KT near the full budget -- and KT and K1/K2 draw
    on the SAME growth-matched budget. You cannot simultaneously max citizen floors
    and max debt retirement. (Early on this is slack -- citizen draw is small,
    ~0.15% of GDP -- so it bites mainly in later phases as K2 scales.)

 3. MECHANISM ATTRIBUTION (the load-bearing point): the growth-matched budget is
    ~1.5% of GDP/yr while interest on the debt stock is ~3.3% of GDP/yr early. KT
    therefore CANNOT outpay interest in the early decades -- so debt/GDP falls
    primarily because NOMINAL GDP GROWTH expands the denominator, not because KT
    retires principal. This is exactly how postwar economies reduced debt/GDP (grow
    out of it, do not pay it off), so it is defensible -- but it reframes KT as an
    ASSIST, not the retiring agent the paper presents. The honest claim is stronger
    than the original: the system grows out of the debt under price stability, with
    KT accelerating at the margin and guaranteeing no new borrowing.

 The KT cap used here is the paper's OWN constraint: KT is "calibrated to a
 price-level path" and "self-throttling on inflation" (Paper 3), i.e. bounded by
 the non-inflationary headroom. So the slower path is not an understatement of KT;
 it follows from the paper's own price-stability rule.
""")
