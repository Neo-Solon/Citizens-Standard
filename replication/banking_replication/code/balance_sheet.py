"""
balance_sheet.py
================
An explicit two-account balance sheet for the Citizens Standard banking system,
used to *derive* the banking propositions rather than assert them. The point of
this module is grounding: each proposition's claim is read off an accounting
mechanism built from primitives, so the tests can fail if the mechanism is wrong.

The balance sheet is intentionally minimal: the propositions concern transaction
money, reserves, equity, and lending capacity, not the full range of bank
activities (derivatives, trading books, off-balance-sheet vehicles, and so on).
Those are omitted because they do not bear on the claims tested here -- inside-money
creation, run exposure, credit capacity, and asset-to-consumer coupling -- and
adding them would obscure the accounting identities the propositions rest on.

Two systems are represented on the same aggregates:

  Incumbent (fractional reserve):
    - Deposits D_frac are demandable money AND fund lending (money multiplier).
    - Inside money (private bank liabilities) is the bulk of the money stock.
    - The entire demandable-deposit base is runnable (Diamond-Dybvig).

  Citizens Standard (full reserve):
    - Transaction accounts T are 100% reserved sovereign money: they are money
      but do NOT fund lending and CANNOT be run.
    - Term deposits D are at-risk, non-demandable investment claims: they fund
      lending but are NOT money and are NOT demandable.
    - The locked floor F is equity outside the deposit base entirely.

All dollar figures are in $T on the launch/current anchors documented below.
Figures are calibrations on verified anchors, not forecasts.
"""

# ---------------------------------------------------------------------------
# ANCHORS (sourced)
# ---------------------------------------------------------------------------
M2          = 22.366   # $T, launch M2 (Paper 5 anchor; FRED M2SL)
DEP_NOW     = 18.548   # $T, deposits all commercial banks, Dec 2025
                       #      (FRED DPSACBM027SBOG, seasonally adjusted)
CURR_NOW    = 2.35     # $T, currency in circulation (~; FRED CURRCIR order)
LEVERAGE    = 4.0      # regulatory leverage cap 4:1 (D <= 3E), Papers 1/3/5
TERM_SHARE  = 0.60     # term-deposit share of launch M2 (framework split, Paper 3)
PHI_LIQ     = 0.15     # pledgeable/liquid fraction of asset wealth (floors locked)

# determinacy / separation primitives inherited from Paper 5 (2026e)
ALPHA       = 1.0      # money-demand semi-elasticity (>0 suffices; illustrative)
PHI_GAIN    = 1.0      # KI price-gap response (>=0 suffices)
LAMBDA_LEAK = 0.03     # structural asset->consumer leak (Paper 5/8 baseline)
CHI_C       = 0.30     # share of bank credit spent on goods (conservative)
ZETA_STAR   = 0.13     # circuit-separation / determinacy coupling threshold (2026e A.12)


# ---------------------------------------------------------------------------
# INCUMBENT (fractional reserve) balance sheet
# ---------------------------------------------------------------------------
def incumbent():
    """Money stock split into inside (bank-liability) and outside (currency)."""
    inside = DEP_NOW                      # demandable bank deposits = inside money
    outside = CURR_NOW                    # sovereign currency
    money_stock = inside + outside
    return {
        "inside_money": inside,
        "outside_money": outside,
        "money_stock": money_stock,
        "inside_share": inside / money_stock,
        # every demandable deposit is runnable
        "runnable": inside,
        "runnable_share_of_money": inside / money_stock,
    }


# ---------------------------------------------------------------------------
# CITIZENS STANDARD (full reserve) balance sheet
# ---------------------------------------------------------------------------
def citizens_standard():
    """
    Build the CS money stock and lending base from primitives.

    Transaction money T is the reserved sovereign layer; term deposits D are the
    at-risk lending base; equity E supports leverage; the locked floor F is
    outside the deposit base. Inside money is derived, not assumed: because banks
    hold 100% reserves against T and lend only termed savings, the amount of
    money that is a private bank liability is computed to be zero.
    """
    T = (1.0 - TERM_SHARE) * M2           # reserved transaction layer (money)
    D = TERM_SHARE * M2                   # term deposits (lending base, NOT money)
    E = D / 3.0                           # equity under 4:1 cap (D <= 3E)

    # Inside money = money that is a private bank liability.
    # Transaction accounts are 100% reserved: the bank holds sovereign reserves
    # equal to T, so the deposit is a claim on reserves it fully holds -- it
    # creates no net new money. Term deposits are not demandable money at all.
    reserves_held = T                     # 100% reserve requirement on T
    inside_money = T - reserves_held      # = 0 by the full-reserve identity
    money_stock = T                       # only the reserved layer circulates as money

    # Lending capacity: L <= D + E, with D <= 3E => capacity = D * 4/3
    credit_capacity = D + E

    # Runnable base: reserved transaction accounts cannot be run (fully backed);
    # term deposits are non-demandable; the floor is equity. So the maximum
    # systemic money contraction is bounded by the term-deposit share only.
    runnable_money = 0.0                  # reserved T cannot be run
    max_money_contraction_share = D / M2  # term share of the aggregate at risk

    return {
        "transaction_money": T,
        "term_deposits": D,
        "equity": E,
        "reserves_held": reserves_held,
        "inside_money": inside_money,
        "money_stock": money_stock,
        "credit_capacity": credit_capacity,
        "runnable_money": runnable_money,
        "max_money_contraction_share": max_money_contraction_share,
    }


# ---------------------------------------------------------------------------
# determinacy / separation (derived scalars used by N1, N2)
# ---------------------------------------------------------------------------
def determinacy_root():
    """theta = 1 + (1+phi)/alpha  (Paper 5 Prop 7; applies to M_o under full reserve)."""
    return 1.0 + (1.0 + PHI_GAIN) / ALPHA


def asset_consumer_coupling(kappa_bank):
    """Total asset->consumer coupling under bank credit (Prop N2)."""
    return LAMBDA_LEAK + CHI_C * kappa_bank


def separation_kappa_ceiling():
    """Max credit intensity consistent with separation: (zeta* - lambda)/chi."""
    return (ZETA_STAR - LAMBDA_LEAK) / CHI_C


if __name__ == "__main__":
    inc = incumbent()
    cs = citizens_standard()
    print("INCUMBENT (fractional reserve):")
    print(f"  inside-money share of money stock = {inc['inside_share']:.2f}")
    print(f"  runnable share of money           = {inc['runnable_share_of_money']:.2f}")
    print("CITIZENS STANDARD (full reserve):")
    print(f"  transaction money T   = ${cs['transaction_money']:.1f}T")
    print(f"  term deposits D       = ${cs['term_deposits']:.1f}T")
    print(f"  equity E              = ${cs['equity']:.1f}T")
    print(f"  inside money (derived) = ${cs['inside_money']:.3f}T")
    print(f"  credit capacity D*4/3 = ${cs['credit_capacity']:.1f}T")
    print(f"  runnable money        = ${cs['runnable_money']:.3f}T")
    print(f"  max contraction share = {cs['max_money_contraction_share']:.2f}")
    print(f"  determinacy root theta = {determinacy_root():.2f}")
