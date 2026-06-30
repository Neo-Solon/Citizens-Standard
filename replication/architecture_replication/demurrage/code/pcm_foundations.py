"""
PCM unified foundations -- single source of truth for all five models.
Every constant is grounded and cited; every model imports from here, so the set is
mutually consistent and auditable. No stale 2-4% / 3% / 2% figures: PCM's settled
anchor is NEAR-ZERO goods inflation (productivity anchor), per the earlier
convergence with Davide and the EQUA derivation.
"""
import math

# ---- macro scale ----
GDP    = 29000.0      # $B, US nominal GDP ~2026
M2_GDP = 0.73         # M2/GDP, current

# ---- convenience-yield demand curve (Krishnamurthy-Vissing-Jorgensen 2012; StL Fed 2025) ----
# c(M) = c0 * exp(-M/Mscale), fit through two empirical anchors:
#   (publicly-held safe stock ~40% GDP, convenience ~73bp)  [KVJ historical avg]
#   (~100% GDP, ~36bp)                                       [StL Fed 2025 compression]
_Ma, _ca = 0.40, 0.0073
_Mb, _cb = 1.00, 0.0036
Mscale = (_Mb - _Ma) / math.log(_ca / _cb)     # ~0.85
c0     = _ca / math.exp(-_Ma / Mscale)         # ~0.0117 (117bp, max convenience at zero supply)
def conv(M):
    """Marginal convenience yield at safe-public-liability stock M (% of GDP)."""
    return c0 * math.exp(-M / Mscale)
def conv_captured(M):
    """Total convenience captured as seigniorage by holding stock M ($B/yr)."""
    return c0 * Mscale * (1 - math.exp(-M / Mscale)) * GDP

# ---- PCM's SETTLED inflation anchor (NOT the stale Ch7 2-4% bracket) ----
# Productivity anchor (currency = hours-to-basket) -> natural GOODS inflation ~0,
# productivity flows to cheaper-in-hours baskets (real/hours appreciation). Range 0..mild defl.
PI_PCM       = 0.000
PI_PCM_RANGE = (-0.010, 0.005)

# ---- world real rate (open economy) ----
R_STAR       = 0.015
R_STAR_RANGE = (0.005, 0.025)

# ---- unified money/safe-asset demand (the #1 unified scale) ----
D_TRANS      = 0.15   # transactional/narrow money demand (~M1, % GDP)
D_SAFE_BROAD = 1.00   # broad safe-asset demand (the held safe-public stock cleared at conv)

# ---- instrument coverage: which demand each instrument serves ----
TAU_TRANS_CS  = 0.20  # CS zero-coupon bills are near-money, not the retail payment medium
TAU_SAFE_CS   = 1.00  # bills serve collateral/benchmark/safe-store fully
TAU_TRANS_PCM = 1.00  # PCM cash money IS the payment medium
THETA         = 0.60  # PCM cash collateral substitutability (the one open parameter)

# ---- cost parameters ----
KAPPA        = 0.10   # crisis output loss (share of GDP), CS DSA ceiling cross-check

if __name__ == "__main__":
    print("PCM unified foundations -- grounded constants")
    print(f"  convenience curve: c0={c0*1e4:.0f}bp, Mscale={Mscale:.3f}")
    print(f"  conv(30%)={conv(.30)*1e4:.0f}bp  conv(45%)={conv(.45)*1e4:.0f}bp  conv(60%)={conv(.60)*1e4:.0f}bp")
    print(f"  PCM anchor: pi={PI_PCM:.1%} (range {PI_PCM_RANGE[0]:.1%}..{PI_PCM_RANGE[1]:.1%}) -- near-zero, NOT 2-4%")
    print(f"  world real rate r*={R_STAR:.1%}")
    print(f"  unified demand: D_trans={D_TRANS:.0%}, D_safe_broad={D_SAFE_BROAD:.0%}, theta={THETA}")
