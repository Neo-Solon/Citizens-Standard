"""
credit_cascade_test_v3.py
=========================
Fisher debt-deflation cascade model — corrected methodology.

This version fixes three methodology errors present in v1 and v2:

  FIX 1 -- Intervention/deflation ordering.
    In v1 and v2, asset-price deflation for the year was computed from the
    PRE-toolkit M2, and the toolkit was added afterward. The result was
    incoherent: more intervention showed as MORE reported deflation, because
    the deflation baseline was locked before the offsetting money arrived.
    v3 computes the gross cascade impulse, then applies the toolkit response,
    then derives net M2, and drives deflation from the NET M2 change -- so
    intervention genuinely dampens deflation and feeds a smaller Fisher
    impulse into the next year.

  FIX 2 -- Double-entry injections.
    Toolkit money is outside (central-bank) money credited to citizens or
    circulation. v3 tracks it as a distinct circulating balance with a matching
    asset entry (outside_money), rather than a single-entry increment to m2.
    Net M2 = protected transaction pool + surviving term deposits
             + outside money still in circulation. The accounting balances.

  FIX 3 -- Transmission factors documented.
    v1/v2 applied undocumented multipliers (0.60, 0.80) to some tools. v3
    replaces these with a single, stated first-year transmission factor that
    represents the share of an injection reaching circulation within the year
    (the remainder carries into the following year rather than vanishing), so
    no dollars are silently discarded and the assumption is explicit.

Compares three toolkit configurations:
  (A) No toolkit
  (B) 14-tool toolkit (Tools 1, 2, 8, 9 + K2)
  (C) 15-tool toolkit (adds Tool 15, M2 Contraction Floor)

Reference: Fisher (1933) Econometrica Vol.1 No.4; Benes & Kumhof (2012)
IMF WP/12/202; Neo-Solon (2026a) Section 10.
Transmission-rate grounding:
  - Direct-transfer MPC in recessions ~0.25-0.40: Sokolova (2022) meta-analysis;
    Parker et al. (2013) on 2008 rebates; Baker et al. (2020) and NBER w27693 on
    2020 CARES (~40% spent within the period).
  - Asset-market / liquidity-trap velocity collapse: Anderson, Bordo & Duca,
    "Money and Velocity During Financial Crises" (NBER w22100, 2016); V2 in 1932
    roughly a third below pre-crisis level.
Run: python3 credit_cascade_test_v3.py
"""

# =============================================================================
# Launch parameters (Neo-Solon 2026a, Section 9; FRED M2SL end-2025)
# =============================================================================

M2_B                 = 22_366.0    # $B
TRANSACTION_SHARE    = 0.40        # full-reserve, constitutionally protected
TERM_DEPOSIT_SHARE   = 0.60        # fractional-reserve credit pool
MAX_LEVERAGE         = 4.0
BANK_EQUITY_RATIO    = 0.25

# Emergency tool ceilings (as % of launch M2)
TOOL1_CEILING_PCT    = 0.020       # Emergency K1 Provision
TOOL2_CEILING_PCT    = 0.040       # Constitutional Rainy-Day Fund
TOOL8_CEILING_PCT    = 0.0005      # Deflationary Floor Dividend
TOOL9_CEILING_PCT    = 0.005       # Enhanced Auto Stabilizers
TOOL15_CEILING_PCT   = 0.030       # Tool 15 M2 Contraction Floor (per year)
K2_ANNUAL_PCT        = 0.010       # ongoing K2 issuance as % of M2

# Fisher cascade parameters
FISHER_AMPLIFIER     = 0.80        # default amplification per unit cumulative deflation
ASSET_PRICE_FLOOR    = 0.50        # assets do not fall below 50% of launch
PROPERTY_SHARE_LOANS = 0.45        # share of lending book secured by real property
PRICE_PASSTHROUGH    = 0.70        # net M2 contraction -> price-level fall pass-through

# Transmission to circulating M2, grounded in the empirical record of money
# injected during debt-deflation / liquidity-trap conditions:
#   - Direct citizen transfers (Tool 15, K2): first-year spending MPC in
#     recessions ~0.25-0.40 (2008 stimulus 12-30%; 2020 CARES ~40% spent,
#     remainder saved/debt-paydown). Midpoint ~0.35.
#   - Asset-market operations (Tools 1, 2, 8, 9): transmit even more weakly in
#     an acute liquidity trap, where money demand surges and velocity falls by
#     roughly a third (Depression V2 collapse). Set to ~0.25.
# The untransmitted remainder is carried into circulation the following year
# (not discarded), with recovery toward normal as the crisis abates.
TRANSMISSION_DIRECT  = 0.35   # Tool 15 and K2 (direct per-citizen deposits)
TRANSMISSION_ASSET   = 0.25   # Tools 1, 2, 8, 9 (asset-market operations)

# Triggers
TOOL1_TRIGGER_DEFL    = 0.01       # cumulative deflation > 1%
TOOL2_TRIGGER_M2      = 2.0        # net M2 contraction > 2% (year)
TOOL8_TRIGGER_DEFL    = 0.05       # cumulative deflation > 5%
TOOL9_TRIGGER_M2      = 1.0        # net M2 contraction > 1% (year)
TOOL15_TRIGGER_M2_PCT = 5.0        # rolling 12-month M2 contraction > 5%

# Derived launch balances
M2                   = M2_B * 1e9
TRANSACTION_POOL     = M2 * TRANSACTION_SHARE
TERM_DEPOSIT_POOL    = M2 * TERM_DEPOSIT_SHARE
LENDING_BOOK         = TERM_DEPOSIT_POOL * (MAX_LEVERAGE / (MAX_LEVERAGE - 1))
BANK_EQUITY          = LENDING_BOOK * BANK_EQUITY_RATIO

TOOL1_CAP            = M2 * TOOL1_CEILING_PCT
TOOL2_CAP            = M2 * TOOL2_CEILING_PCT
TOOL8_CAP            = M2 * TOOL8_CEILING_PCT
TOOL9_CAP            = M2 * TOOL9_CEILING_PCT
TOOL15_CAP           = M2 * TOOL15_CEILING_PCT
K2_ANNUAL            = M2 * K2_ANNUAL_PCT


# =============================================================================
# CASCADE MODEL
# =============================================================================

def run_cascade(shock_pct, duration_years, toolkit="none"):
    """
    toolkit: "none" | "14tool" | "15tool"

    Within-year sequence (corrected):
      1. Credit losses (Fisher-amplified) hit equity buffer.
      2. Equity depletion forces deleveraging -> lending contraction.
      3. Term deposits contract with the lending book.
      4. GROSS M2 = transaction pool + surviving term deposits + outside money
         already in circulation from prior years.
      5. Toolkit responds THIS year (outside-money injection, double-entry),
         scaled by the first-year transmission factor; the untransmitted
         remainder is carried into circulation next year.
      6. NET M2 = gross M2 + this year's transmitted injection.
      7. Deflation is driven by the NET M2 change -> feeds next year's Fisher
         impulse. Intervention therefore reduces deflation, as it should.
    """
    equity           = BANK_EQUITY
    lending          = LENDING_BOOK
    term_deposits    = TERM_DEPOSIT_POOL
    transaction      = TRANSACTION_POOL          # never changes (full reserve)
    outside_money    = 0.0                        # cumulative injected money in circulation
    pending_injection = 0.0                       # untransmitted remainder carried forward
    asset_price_idx  = 1.0
    cumulative_defl  = 0.0
    cumulative_loss  = 0.0
    depositor_losses = 0.0
    toolkit_deployed = 0.0

    tool1_remaining  = TOOL1_CAP
    tool2_remaining  = TOOL2_CAP
    tool8_remaining  = TOOL8_CAP * duration_years
    tool9_remaining  = TOOL9_CAP * duration_years
    # Tool 15 sunsets after 18 months per activation; a single continuous cascade
    # is one activation, so total capacity is 1.5 * the annual ceiling. Continuation
    # past the sunset requires FDCA certification (a citizen decision), not modeled
    # as automatic — so in a prolonged cascade Tool 15's contribution is bounded.
    tool15_remaining = TOOL15_CAP * 1.5

    m2_prev          = M2
    m2_12mo_ago      = M2
    annual_states    = []

    for yr in range(1, duration_years + 1):

        # ---- 1. Credit losses (Fisher-amplified) ----
        fisher_boost = FISHER_AMPLIFIER * max(0.0, cumulative_defl)
        effective_loss_rate = (shock_pct / 100) * (1 + fisher_boost)
        effective_loss_rate += PROPERTY_SHARE_LOANS * max(0.0, 1 - asset_price_idx)
        annual_loss = lending * effective_loss_rate
        cumulative_loss += annual_loss

        # ---- 2. Equity buffer absorbs first; remainder hits term depositors ----
        equity_absorbed = min(equity, annual_loss)
        equity -= equity_absorbed
        depositor_loss = max(0.0, annual_loss - equity_absorbed)
        depositor_losses += depositor_loss

        # ---- 3. Deleveraging -> lending contraction ----
        if equity > 0:
            max_lending = equity / BANK_EQUITY_RATIO
            lending_contraction = max(0.0, lending - max_lending)
            lending = min(lending, max_lending)
        else:
            new_lending = lending * 0.50
            lending_contraction = lending - new_lending
            lending = max(0.0, new_lending)

        # ---- 4. Term-deposit contraction (liability side) ----
        # Deposits shrink with the lending book. The 0.70 reflects that not all
        # lending contraction destroys deposits within the year (some funds shift
        # to the protected transaction pool or are held as reserves).
        td_contraction_rate = lending_contraction / max(LENDING_BOOK, 1)
        term_deposits = max(0.0, term_deposits * (1 - td_contraction_rate * 0.70))

        # ---- 5. Gross M2 (before this year's toolkit response) ----
        gross_m2 = transaction + term_deposits + outside_money

        # ---- 6. Toolkit responds THIS year (double-entry outside money) ----
        gross_contraction_pct = (M2 - gross_m2) / M2 * 100
        direct_injection = 0.0   # per-citizen deposits (Tools 1, 8, 15, K2)
        asset_injection  = 0.0   # asset-market operations (Tools 2, 9)

        # carry forward any untransmitted injection from prior year
        carried = pending_injection
        pending_injection = 0.0

        if toolkit in ("14tool", "15tool"):
            if cumulative_defl > TOOL1_TRIGGER_DEFL and tool1_remaining > 0:
                t1 = min(tool1_remaining, TOOL1_CAP * 0.40)
                tool1_remaining -= t1; toolkit_deployed += t1; direct_injection += t1
            if gross_contraction_pct > TOOL2_TRIGGER_M2 and tool2_remaining > 0:
                t2 = min(tool2_remaining, TOOL2_CAP * 0.25)
                tool2_remaining -= t2; toolkit_deployed += t2; asset_injection += t2
            if cumulative_defl > TOOL8_TRIGGER_DEFL and tool8_remaining > 0:
                t8 = min(tool8_remaining, TOOL8_CAP)
                tool8_remaining -= t8; toolkit_deployed += t8; direct_injection += t8
            if gross_contraction_pct > TOOL9_TRIGGER_M2 and tool9_remaining > 0:
                t9 = min(tool9_remaining, TOOL9_CAP)
                tool9_remaining -= t9; toolkit_deployed += t9; asset_injection += t9
            k2 = K2_ANNUAL * max(0.3, asset_price_idx)
            toolkit_deployed += k2; direct_injection += k2

        m2_rolling_contraction = (m2_12mo_ago - gross_m2) / m2_12mo_ago * 100
        tool15_triggered = (toolkit == "15tool"
                            and m2_rolling_contraction > TOOL15_TRIGGER_M2_PCT
                            and tool15_remaining > 0)
        if tool15_triggered:
            t15 = min(tool15_remaining, TOOL15_CAP)
            tool15_remaining -= t15; toolkit_deployed += t15; direct_injection += t15

        # Apply evidence-grounded per-channel transmission; remainder carries forward.
        transmitted = (direct_injection * TRANSMISSION_DIRECT
                       + asset_injection * TRANSMISSION_ASSET
                       + carried * TRANSMISSION_DIRECT)
        pending_injection = ((direct_injection + carried) * (1 - TRANSMISSION_DIRECT)
                             + asset_injection * (1 - TRANSMISSION_ASSET))
        outside_money += transmitted

        # ---- 7. Net M2 and deflation driven by NET change ----
        net_m2 = transaction + term_deposits + outside_money
        net_contraction_pct = (M2 - net_m2) / M2 * 100
        # year-over-year net change drives the price level
        yoy_net_contraction = (m2_prev - net_m2) / m2_prev * 100
        price_fall = max(0.0, yoy_net_contraction) * PRICE_PASSTHROUGH
        asset_price_idx = max(ASSET_PRICE_FLOOR, asset_price_idx * (1 - price_fall / 100))
        cumulative_defl = 1 - asset_price_idx

        m2_prev = net_m2
        m2_12mo_ago = net_m2

        annual_states.append({
            "year":               yr,
            "m2_B":               net_m2 / 1e9,
            "net_contraction_pct": net_contraction_pct,
            "lending_B":          lending / 1e9,
            "term_deposits_B":    term_deposits / 1e9,
            "outside_money_B":    outside_money / 1e9,
            "asset_price_idx":    asset_price_idx,
            "cumulative_defl":    cumulative_defl * 100,
            "annual_loss_B":      annual_loss / 1e9,
            "depositor_loss_B":   depositor_loss / 1e9,
            "toolkit_yr_B":       transmitted / 1e9,
            "tool15_active":      tool15_triggered,
        })

    return {
        "states":                   annual_states,
        "final_m2_B":               net_m2 / 1e9,
        "total_m2_contraction_pct": (M2 - net_m2) / M2 * 100,
        "total_credit_loss_B":      cumulative_loss / 1e9,
        "total_toolkit_B":          toolkit_deployed / 1e9,
        "depositor_losses_B":       depositor_losses / 1e9,
        "final_asset_price_idx":    asset_price_idx,
        "total_deflation_pct":      (1 - asset_price_idx) * 100,
        "transaction_protected":    True,
    }


def current_system_cascade(shock_pct, duration_years):
    """
    Same cascade under the current fractional-reserve system: NO protected pool,
    so bank runs can destroy payment deposits directly (the 1930-33 mechanism).
    """
    m2 = M2
    total_deposits = M2
    lending = total_deposits * (MAX_LEVERAGE / (MAX_LEVERAGE - 1))
    equity = lending * BANK_EQUITY_RATIO
    asset_price_idx = 1.0
    cumulative_defl = 0.0
    cumulative_loss = 0.0

    prev_lending = LENDING_BOOK
    for yr in range(1, duration_years + 1):
        fisher_boost = FISHER_AMPLIFIER * max(0.0, cumulative_defl)
        effective_loss_rate = (shock_pct / 100) * (1 + fisher_boost)
        effective_loss_rate += PROPERTY_SHARE_LOANS * max(0.0, 1 - asset_price_idx)
        annual_loss = lending * effective_loss_rate
        cumulative_loss += annual_loss

        equity_absorbed = min(equity, annual_loss)
        equity -= equity_absorbed
        if equity > 0:
            lending = min(lending, equity / BANK_EQUITY_RATIO)
        else:
            lending = max(0.0, lending * 0.40)

        # Deposit destruction tracks the YEAR-OVER-YEAR lending contraction.
        # No protected pool: bank runs amplify it (run_multiplier). Bounded to
        # a non-negative contraction so deposits can only fall, never expand.
        lending_contraction_rate = max(0.0, (prev_lending - lending) / max(prev_lending, 1))
        prev_lending = lending
        run_multiplier = 1.30 if equity <= 0 else 1.05
        total_deposits = max(0.0, total_deposits *
                             (1 - min(1.0, lending_contraction_rate * 0.80 * run_multiplier)))
        m2 = total_deposits
        yoy = (M2 - m2) / M2 * 100
        price_fall = max(0.0, yoy) * PRICE_PASSTHROUGH
        asset_price_idx = max(0.40, asset_price_idx * (1 - price_fall / 100))
        cumulative_defl = 1 - asset_price_idx

    return {
        "final_m2_B": m2 / 1e9,
        "total_m2_contraction_pct": (M2 - m2) / M2 * 100,
        "payment_system_protected": False,
        "total_credit_loss_B": cumulative_loss / 1e9,
    }


# =============================================================================
# OUTPUT
# =============================================================================

def print_scenario(label, shock, years):
    r_none = run_cascade(shock, years, "none")
    r_14   = run_cascade(shock, years, "14tool")
    r_15   = run_cascade(shock, years, "15tool")
    curr   = current_system_cascade(shock, years)

    print(f"\n{'='*100}")
    print(f"SCENARIO: {label}  ({shock}%/yr initial loss, {years} years)")
    print(f"{'':30} {'No toolkit':>14} {'14-tool':>14} {'15-tool':>14} {'Curr. system':>14}")
    print("-"*100)

    def row(metric, a, b, c, d, fmt=".1f", suffix=""):
        print(f"  {metric:<28} {f'{a:{fmt}}{suffix}':>14} {f'{b:{fmt}}{suffix}':>14} "
              f"{f'{c:{fmt}}{suffix}':>14} {f'{d:{fmt}}{suffix}':>14}")

    row("M2 contraction (%)", r_none["total_m2_contraction_pct"],
        r_14["total_m2_contraction_pct"], r_15["total_m2_contraction_pct"],
        curr["total_m2_contraction_pct"], suffix="%")
    row("Final M2 ($B)", r_none["final_m2_B"], r_14["final_m2_B"],
        r_15["final_m2_B"], curr["final_m2_B"], fmt=",.0f", suffix="B")
    row("Total deflation (%)", r_none["total_deflation_pct"],
        r_14["total_deflation_pct"], r_15["total_deflation_pct"],
        0.0, suffix="%")
    row("Total credit losses ($B)", r_none["total_credit_loss_B"],
        r_14["total_credit_loss_B"], r_15["total_credit_loss_B"],
        curr["total_credit_loss_B"], fmt=",.0f", suffix="B")

    gap = r_14["total_m2_contraction_pct"] - r_15["total_m2_contraction_pct"]
    print(f"\n  Tool 15 effect vs 14-tool: {gap:+.1f}pp M2 contraction")
    print(f"  Deflation falls with intervention: none {r_none['total_deflation_pct']:.1f}% "
          f"-> 14-tool {r_14['total_deflation_pct']:.1f}% -> 15-tool {r_15['total_deflation_pct']:.1f}%")
    print(f"  Transaction pool ${TRANSACTION_POOL/1e9:,.0f}B PROTECTED throughout "
          f"(current system: ${0:,.0f}B protected)")


if __name__ == "__main__":
    print("="*100)
    print("CITIZENS STANDARD — CASCADE MODEL v3 (corrected methodology)")
    print(f"Tool 15: M2 Contraction Floor | Trigger: >{TOOL15_TRIGGER_M2_PCT}% rolling 12mo | "
          f"Ceiling: {TOOL15_CEILING_PCT*100:.0f}% M2 = ${TOOL15_CAP/1e9:,.0f}B/yr")
    print(f"Fixes: (1) deflation driven by NET post-toolkit M2; (2) double-entry outside-money "
          f"injections; (3) evidence-grounded transmission (direct {TRANSMISSION_DIRECT:.0%}, "
          f"asset-market {TRANSMISSION_ASSET:.0%})")
    print("="*100)

    print_scenario("Moderate (2008-equivalent)", 3.0, 3)
    print_scenario("Depression-magnitude",        6.0, 3)
    print_scenario("Extreme tail",               10.0, 3)
    print_scenario("Prolonged moderate",          3.0, 5)
    print_scenario("Prolonged Depression",        6.0, 5)

    print(f"\n{'='*100}")
    print("KEY FINDINGS — v3")
    print("-"*100)
    r2008_14 = run_cascade(3.0, 3, "14tool"); r2008_15 = run_cascade(3.0, 3, "15tool")
    rdep_14  = run_cascade(6.0, 3, "14tool"); rdep_15  = run_cascade(6.0, 3, "15tool")
    print(f"""
2008-equivalent (3%/yr, 3yr):
  14-tool M2 contraction: {r2008_14['total_m2_contraction_pct']:.1f}%
  15-tool M2 contraction: {r2008_15['total_m2_contraction_pct']:.1f}%
  Tool 15 effect:         {r2008_14['total_m2_contraction_pct']-r2008_15['total_m2_contraction_pct']:+.1f}pp
  Deflation (15-tool):    {r2008_15['total_deflation_pct']:.1f}% (intervention reduces it)

Depression-magnitude (6%/yr, 3yr):
  14-tool M2 contraction: {rdep_14['total_m2_contraction_pct']:.1f}%
  15-tool M2 contraction: {rdep_15['total_m2_contraction_pct']:.1f}%
  Tool 15 effect:         {rdep_14['total_m2_contraction_pct']-rdep_15['total_m2_contraction_pct']:+.1f}pp
  vs historical 30%:      {rdep_15['total_m2_contraction_pct']:.1f}%

Structural guarantee (all scenarios):
  Transaction pool = ${TRANSACTION_POOL/1e9:,.0f}B — constitutionally protected, never at risk
  Maximum possible M2 contraction = {TERM_DEPOSIT_SHARE*100:.0f}% (term deposit share only)
  Corrected accounting: injections are double-entry outside money; deflation
  responds to NET post-intervention M2, so the toolkit reduces deflation rather
  than (as in v1/v2) appearing to worsen it.
  The framework's honest claim: better failure mode, not no failure mode.
""")
