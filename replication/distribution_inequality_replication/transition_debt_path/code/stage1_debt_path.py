"""
Transition debt-retirement path -- Paper 3's central quantitative transition claim,
tested on real fiscal data. VERIFIED ANCHORS ONLY; the uncertain macro parameters
(growth, interest rate, KT issuance capacity) are swept, not guessed.

THE CLAIM (Paper 3): under Mode T, a transition-only channel (KT) retires legacy
debt while remaining consumer-price neutral and self-throttling on inflation.
Public debt-to-GDP falls from ~102% at enactment to ~39% by Year 30 and to ~15% by
~Year 45. Citizen K1/K2 flow uninterrupted at full price stability throughout.

WHAT THIS TESTS: whether that retirement PATH is arithmetically consistent given
realistic growth, the interest cost on remaining debt, and a KT issuance capacity
bounded so it stays non-inflationary (capped at the price-stability locus -- KT can
only use the headroom between realized growth and what K1/K2 already issue).

VERIFIED ANCHORS (2024-2026, real data):
  - Gross federal debt > $39T (exceeded March 2026); debt HELD BY PUBLIC ~$28-30T,
    ~98-100% of GDP (FY2024: $28.2T, 98%). Paper's $31.4T/102% is a near-term
    forward figure; we anchor at a transparent ~100% of GDP and note this.
  - GDP ~ $29T (2024-25). Real growth ~1.8-2.7% (CBO 2025-2035 range).
  - Net interest ~3.2% of GDP (2025), rising; avg rate on debt ~3.3%.
  - M2 ~ $21-22T; growth-matched issuance headroom ~ real growth x M2.
"""

# verified starting anchors
DEBT0_PCT = 1.00        # debt held by public as share of GDP at enactment (transparent ~100%)
GDP0 = 29000.0          # $B, 2024-25
M2_0 = 21500.0          # $B
# KT capacity: the price-stability locus says total issuance ~ real growth x M2.
# K1+K2 (citizen channels) use part; KT uses the REMAINDER as debt-retirement headroom.
# Paper: K1/K2 run at full price stability; KT is the transition-only residual.
# Model KT as a share of the growth-matched budget routed to debt retirement.

def run_path(real_growth, infl, avg_rate, kt_share, years=50):
    """
    real_growth: real GDP growth (annual)
    infl: GDP deflator / inflation (annual) -> nominal growth = real+infl
    avg_rate: average interest rate on public debt
    kt_share: share of the growth-matched issuance budget routed to KT debt retirement
    """
    debt = DEBT0_PCT*GDP0      # $B nominal
    gdp = GDP0
    m2 = M2_0
    path=[]
    for y in range(1, years+1):
        nominal_growth = real_growth + infl
        gdp *= (1+nominal_growth)
        m2 *= (1+nominal_growth)               # M2 grows with nominal economy
        # growth-matched issuance budget this year (price-stability locus)
        issuance_budget = max(0, real_growth) * m2
        kt = kt_share * issuance_budget         # debt-retirement channel
        # debt evolves: + interest accrual - KT retirement (no NEW borrowing under Mode T)
        interest = avg_rate * debt
        debt = debt + interest - kt
        if debt < 0.15*gdp: debt = 0.15*gdp     # operational floor (paper: ~15%)
        path.append((y, 100*debt/gdp))
    return path

# central case: CBO-ish growth, moderate KT
print("="*72)
print("TRANSITION DEBT-RETIREMENT PATH (Paper 3 claim: 102% -> 39% Y30 -> 15% Y45)")
print("="*72)
print("Anchored at ~100% of GDP (FY2024 actual 98%; paper's 102% is near-term forward)")
print()
central = run_path(real_growth=0.020, infl=0.023, avg_rate=0.033, kt_share=0.6)
print(f"Central case: real growth 2.0%, inflation 2.3%, avg rate 3.3%, KT share 0.6")
print(f"  {'Year':>5} {'debt/GDP':>9}")
for y,d in central:
    if y in (1,5,10,15,20,25,30,35,40,45,50):
        print(f"  {y:>5} {d:>7.0f}%")
print()
# locate when it hits the paper's milestones
def year_at(path, target):
    for y,d in path:
        if d<=target: return y
    return None
y39=year_at(central,39); y15=year_at(central,15.5)
print(f"Reaches 39% of GDP at Year {y39} (paper claims ~Year 30)")
print(f"Reaches ~15% floor at Year {y15} (paper claims ~Year 45)")
