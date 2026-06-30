"""
Demurrage as a CONDITIONAL stabilizer for CS Mode A (deflation-targeting), grounded.
Built on the shared foundations (convenience curve, world real rate) where relevant.

EMPIRICAL ANCHORS (all web-verified):
 - Atkeson & Kehoe 2004 (AER 94(2)): across 17 countries, 100+ yrs, NO deflation-
   depression link outside the 1930s. Bordo-Landon-Lane-Redish: controlling for asset
   prices, falling goods prices carry no depression signal. => Mode A's productivity
   deflation is the BENIGN kind; the hoarding problem is CONDITIONAL, not generic.
 - Money-demand interest elasticity ~0.3-0.6 (Benati-Lucas-Nicolini-Weber, 38 countries;
   Lucas 2000 nu=0.5, Baumol-Tobin). Semi-elasticity RISES sharply as rates -> 0
   (log-log -> infinite demand at zero), so the hoarding response strengthens exactly
   in the deflation zone.
 - Demurrage experiments: Worgl 1932 ~12%/yr -> scrip circulated ~8-14x the shilling;
   Chiemgauer ~8%/yr -> several x the euro. Demurrage demonstrably moves velocity.
 - Leakage cap (Keynes' objection, verified): demurrage is evaded by switching into
   more liquid untaxed stores -> caps the usable rate. Same flight margin as PCM #5.
"""
import math
from pcm_foundations import R_STAR

# ---------- PART 1: is there a problem? velocity under Mode A deflation ----------
# Money demand m = M/PY; velocity V = 1/m. Lucas log-log: ln m = ln A - nu*ln(i),
# but i is bounded below; in deflation the OPPORTUNITY COST of holding money is the
# negative of the real return to cash. Hold-cash real return in deflation pi<0 is -pi>0.
# Use the empirically-honest object: the "own real yield" of idle cash = -pi (deflation).
# Velocity responds to the GAP between cash's real yield and the productive real return.
# Cash real yield = -pi ; productive real return ~ r* (world real rate). Hoarding
# incentive H = cash_yield - (r* adjusted)  ... model velocity drop via semi-elasticity.
ETA = 0.5            # interest/own-yield semi-elasticity of money demand (Lucas baseline)
def velocity_index(pi, eta=ETA, demurrage=0.0):
    """Velocity relative to price-stability baseline (pi=0, no demurrage)=1.0.
    Net carry on idle cash = (-pi) - demurrage. Higher net carry -> more hoarding ->
    lower velocity. Semi-log: ln V = ln V0 - eta*(net real carry on money)."""
    net_carry = (-pi) - demurrage           # reward to sit on cash, net of demurrage
    return math.exp(-eta*net_carry/ -1 * -1)  # = exp(-eta*net_carry)
def Vrel(pi, demurrage=0.0, eta=ETA):
    net_carry=(-pi)-demurrage
    return math.exp(-eta*net_carry)
print("PART 1 -- velocity under Mode A deflation (relative to price-stable baseline=1.00)\n")
print(f"  semi-elasticity eta={ETA} (Lucas 2000 baseline; range 0.3-0.6)\n")
print(f"  {'deflation pi':>14}{'velocity index':>16}{'velocity drop':>15}")
for pi in (0.0,-0.010,-0.019,-0.030):
    v=Vrel(pi); print(f"  {pi*100:>+12.1f}%{v:>16.3f}{(v-1)*100:>+14.1f}%")
print("""
  Reading: at Mode A's ~-1.9%, velocity sits ~1% below the price-stable baseline on
  the central elasticity. That is SMALL and matches Atkeson-Kehoe: mild productivity
  deflation does not, by itself, trigger a hoarding spiral. The case for demurrage is
  NOT the steady mild-deflation state; it is the CONDITIONAL tail where deflation
  expectations deepen or a confidence shock drops velocity further.""")

# ---------- PART 2: the offsetting demurrage rate ----------
print("\nPART 2 -- demurrage delta that neutralises the hoarding reward\n")
print("  Demurrage adds a carrying cost that offsets the -pi reward on idle cash.")
print("  Setting delta = -pi zeroes the net carry and restores velocity to baseline.\n")
print(f"  {'deflation pi':>14}{'delta to neutralise':>21}{'velocity restored to':>22}")
for pi in (-0.010,-0.019,-0.030):
    d=-pi
    print(f"  {pi*100:>+12.1f}%{d*100:>18.1f}%{Vrel(pi,demurrage=d):>20.3f}")
print("""
  So the required demurrage is modest: ~1.9%/yr to exactly offset Mode A's deflation,
  far below Worgl's 12% or Chiemgauer's 8%. Revenue recycled equally per-capita makes
  it net-neutral on average (no money created/destroyed, price path preserved); only
  the relative incentive bites -- above-average hoarders pay, fast-spenders gain.""")

# ---------- PART 3: the leakage cap (Keynes) ----------
print("PART 3 -- leakage cap: how hard can delta be pushed before money flees?\n")
# Flight to untaxed stores: same structure as PCM #5. Holders exit transactional money
# when demurrage exceeds the convenience/liquidity value of holding it. The transactional
# convenience premium (why people hold zero-yield money at all) bounds delta.
# Empirical: M1 holders accept ~the short-rate as the liquidity premium; transactional
# convenience ~ a few hundred bp. Use the same conv curve max as a conservative proxy.
from pcm_foundations import c0
print(f"  Demurrage is evaded by switching to untaxed liquid stores (Keynes). The usable")
print(f"  rate is bounded by the liquidity value of staying in transactional money.")
print(f"  - Floors are LOCKED (can't dump money there), removing the easiest escape, but")
print(f"    assets/foreign/crypto remain. Worgl/Chiemgauer sustained 8-12% only because")
print(f"    the scrip was the ONLY local means of payment + tax-receivable (high captive")
print(f"    demand). A national CS would have more escape routes -> lower ceiling.")
print(f"  - Practical safe band: delta up to ~the transactional liquidity premium")
print(f"    (order a few %), comfortably above the ~1.9% needed to offset Mode A. The")
print(f"    offset rate sits INSIDE the leakage-safe zone; pushing far beyond it (Worgl-")
print(f"    scale) would drive flight, not circulation, at national scale.\n")

# ---------- PART 4: conditional trigger design ----------
print("PART 4 -- conditional design (the honest recommendation)\n")
print("  Demurrage should ARM only when velocity falls below a threshold, not run by")
print("  default (Atkeson-Kehoe: the benign state needs no intervention; intervening")
print("  there would just impose a deadweight carrying cost).")
Vbaseline=1.0; Vtrigger=0.95   # arm if velocity falls >5% below baseline
print(f"  Trigger: arm if velocity index < {Vtrigger:.2f} (>5% below baseline).")
# what deflation/expectation shock pushes velocity below trigger?
for pi in (-0.019,-0.04,-0.06):
    v=Vrel(pi)
    armed = v < Vtrigger
    d_needed = max(0.0, -pi - (-math.log(Vbaseline)/ETA))  # delta to lift V back to ~baseline
    # simpler: delta to restore baseline = -pi
    print(f"   pi={pi*100:+.1f}%: velocity {v:.3f} -> {'ARM, delta~'+format(-pi*100,'.1f')+'%' if armed else 'dormant (benign)'}")
print("""
  RECOMMENDATION:
  - Mode A (and any mild-deflation config) carries demurrage as a DORMANT, conditional
    tool, armed only if velocity drops materially (e.g. >5% below baseline) signalling
    the benign deflation is tipping into hoarding.
  - When armed, delta ~ -pi (a couple %), revenue recycled equally per-capita, applied
    to the TRANSACTIONAL circuit ONLY (Floors exempt, as with reverse-KT).
  - This is the ONE failure mode KI cannot address (KI would issue money and destroy
    the intended deflation); demurrage decouples the price path from the hoarding
    incentive, which no other CS lever does.
  HONEST RESIDUALS:
  - The velocity-elasticity (eta) and the leakage ceiling are the two soft numbers;
    both are bounded by data (eta 0.3-0.6; Worgl/Chiemgauer show 8-12% is sustainable
    only with captive demand) but neither is sharp at national scale.
  - True Gesell demurrage (face-value decay) bites harder than a constant-face 'negative
    interest' version, which holders can still hoard through; design must specify which.
  - Demurrage's gain is velocity, NOT new purchasing power; it cannot substitute for
    KI in a genuine demand collapse where you need more money, not just faster money.""")
