"""
credit_cascade_test_v2.py
==========================
Fisher debt-deflation cascade model — updated with Tool 15 (M2 Contraction Floor).

Tool 15 added to emergency toolkit:
  Trigger:  M2 contracts > 5% over any rolling 12-month window
  Ceiling:  3.0% of current M2 per year ($671B/yr at launch)
  Mechanism: Equal per-citizen direct deposit, immediately spendable
  Sunset:   18 months automatic; continuation requires FDCA certification

Compares three toolkit configurations:
  (A) No toolkit
  (B) Original 14-tool toolkit (Tools 1, 2, 8, 9 + K2)
  (C) Updated 15-tool toolkit (adds Tool 15)

Reference: Fisher (1933), Benes & Kumhof (2012), Neo-Solon (2026a) Section 10.
Run: python3 credit_cascade_test_v2.py
"""

# =============================================================================
# Launch parameters
# =============================================================================

M2_B                 = 22_366.0
TRANSACTION_SHARE    = 0.40
TERM_DEPOSIT_SHARE   = 0.60
MAX_LEVERAGE         = 4.0
BANK_EQUITY_RATIO    = 0.25

# Emergency tool parameters
TOOL1_CEILING_PCT    = 0.020
TOOL2_CEILING_PCT    = 0.040
TOOL8_CEILING_PCT    = 0.0005
TOOL9_CEILING_PCT    = 0.005
TOOL15_CEILING_PCT   = 0.030   # NEW: Tool 15 M2 Contraction Floor
K2_ANNUAL_PCT        = 0.010

# Fisher cascade parameters
FISHER_AMPLIFIER     = 0.80
ASSET_PRICE_FLOOR    = 0.50
PROPERTY_SHARE_LOANS = 0.45
TOOL1_TRIGGER_DEFL   = 0.01
TOOL15_TRIGGER_M2_PCT = 5.0   # Tool 15 triggers when M2 contracts > 5% over 12 months

# Derived
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
    """
    equity          = BANK_EQUITY
    lending         = LENDING_BOOK
    term_deposits   = TERM_DEPOSIT_POOL
    transaction     = TRANSACTION_POOL
    m2              = M2
    asset_price_idx = 1.0
    cumulative_defl = 0.0
    cumulative_loss = 0.0
    toolkit_deployed = 0.0

    tool1_remaining  = TOOL1_CAP
    tool2_remaining  = TOOL2_CAP
    tool8_remaining  = TOOL8_CAP * duration_years
    tool9_remaining  = TOOL9_CAP * duration_years
    tool15_remaining = TOOL15_CAP * duration_years  # per-year ceiling * duration

    m2_12mo_ago      = M2  # track rolling 12-month M2 for Tool 15 trigger

    annual_states = []

    for yr in range(1, duration_years + 1):

        # Fisher amplification
        fisher_boost = FISHER_AMPLIFIER * max(0, cumulative_defl)
        effective_loss_rate = shock_pct/100 * (1 + fisher_boost)
        property_loss_boost = PROPERTY_SHARE_LOANS * max(0, 1 - asset_price_idx)
        effective_loss_rate += property_loss_boost

        annual_loss = lending * effective_loss_rate
        cumulative_loss += annual_loss

        # Equity buffer
        equity_absorbed  = min(equity, annual_loss)
        equity          -= equity_absorbed
        depositor_loss   = max(0, annual_loss - equity_absorbed)

        # Deleveraging
        if equity > 0:
            max_lending = equity / BANK_EQUITY_RATIO
            lending_contraction = max(0, lending - max_lending)
            lending = min(lending, max_lending)
        else:
            lending = max(0, lending * 0.50)
            lending_contraction = LENDING_BOOK - lending

        # Term deposit contraction
        td_contraction_rate = lending_contraction / max(LENDING_BOOK, 1)
        term_deposits = max(0, term_deposits * (1 - td_contraction_rate * 0.70))

        # M2 pre-toolkit
        m2_prev = m2
        m2 = transaction + term_deposits
        m2_contraction_pct = (m2_prev - m2) / m2_prev * 100

        # Asset price deflation
        price_fall = m2_contraction_pct * 0.70
        asset_price_idx = max(ASSET_PRICE_FLOOR, asset_price_idx * (1 - price_fall/100))
        cumulative_defl = 1 - asset_price_idx

        # Tool 15 trigger: M2 contracted > 5% vs 12 months ago
        m2_rolling_contraction = (m2_12mo_ago - m2) / m2_12mo_ago * 100
        tool15_triggered = (m2_rolling_contraction > TOOL15_TRIGGER_M2_PCT)
        m2_12mo_ago = m2  # update for next year

        # Emergency toolkit
        toolkit_this_year = 0.0

        if toolkit in ("14tool", "15tool"):
            if cumulative_defl > TOOL1_TRIGGER_DEFL and tool1_remaining > 0:
                t1 = min(tool1_remaining, TOOL1_CAP * 0.40)
                toolkit_this_year += t1; tool1_remaining -= t1; m2 += t1

            if m2_contraction_pct > 2.0 and tool2_remaining > 0:
                t2 = min(tool2_remaining, TOOL2_CAP * 0.25)
                toolkit_this_year += t2; tool2_remaining -= t2; m2 += t2 * 0.60

            if cumulative_defl > 0.05 and tool8_remaining > 0:
                t8 = min(tool8_remaining, TOOL8_CAP)
                toolkit_this_year += t8; tool8_remaining -= t8; m2 += t8

            if m2_contraction_pct > 1.0 and tool9_remaining > 0:
                t9 = min(tool9_remaining, TOOL9_CAP)
                toolkit_this_year += t9; tool9_remaining -= t9; m2 += t9 * 0.80

            k2 = K2_ANNUAL * max(0.3, asset_price_idx)
            m2 += k2; toolkit_this_year += k2

        if toolkit == "15tool" and tool15_triggered and tool15_remaining > 0:
            t15 = min(tool15_remaining, TOOL15_CAP)
            toolkit_this_year += t15; tool15_remaining -= t15; m2 += t15
            # Note: Tool 15 enters via direct citizen deposit — full circulating effect

        toolkit_deployed += toolkit_this_year

        annual_states.append({
            "year":               yr,
            "m2_B":               m2 / 1e9,
            "m2_contraction_pct": (M2 - m2) / M2 * 100,
            "lending_B":          lending / 1e9,
            "asset_price_idx":    asset_price_idx,
            "cumulative_defl":    cumulative_defl * 100,
            "annual_loss_B":      annual_loss / 1e9,
            "toolkit_yr_B":       toolkit_this_year / 1e9,
            "tool15_active":      toolkit == "15tool" and tool15_triggered,
        })

    return {
        "states":                   annual_states,
        "final_m2_B":               m2 / 1e9,
        "total_m2_contraction_pct": (M2 - m2) / M2 * 100,
        "total_credit_loss_B":      cumulative_loss / 1e9,
        "total_toolkit_B":          toolkit_deployed / 1e9,
        "final_asset_price_idx":    asset_price_idx,
        "total_deflation_pct":      (1 - asset_price_idx) * 100,
        "transaction_protected":    True,
    }


# =============================================================================
# OUTPUT
# =============================================================================

def print_scenario(label, shock, years):
    r_none  = run_cascade(shock, years, "none")
    r_14    = run_cascade(shock, years, "14tool")
    r_15    = run_cascade(shock, years, "15tool")

    print(f"\n{'='*100}")
    print(f"SCENARIO: {label}  ({shock}%/yr initial loss, {years} years)")
    print(f"{'':30} {'No toolkit':>15} {'14-tool':>15} {'15-tool':>15} {'Improvement':>15}")
    print("-"*100)

    def row(metric, v_none, v_14, v_15, fmt=".1f", suffix=""):
        improvement = v_14 - v_15 if "contraction" in metric.lower() or "deflat" in metric.lower() else v_15 - v_14
        print(f"  {metric:<28} {f'{v_none:{fmt}}{suffix}':>15} "
              f"{f'{v_14:{fmt}}{suffix}':>15} "
              f"{f'{v_15:{fmt}}{suffix}':>15} "
              f"{f'{improvement:+.1f}{suffix}':>15}")

    row("M2 contraction (%)",
        r_none["total_m2_contraction_pct"],
        r_14["total_m2_contraction_pct"],
        r_15["total_m2_contraction_pct"],
        suffix="%")

    row("Final M2 ($B)",
        r_none["final_m2_B"],
        r_14["final_m2_B"],
        r_15["final_m2_B"],
        fmt=",.0f", suffix="B")

    row("Asset price index",
        r_none["final_asset_price_idx"],
        r_14["final_asset_price_idx"],
        r_15["final_asset_price_idx"],
        fmt=".3f")

    row("Total deflation (%)",
        r_none["total_deflation_pct"],
        r_14["total_deflation_pct"],
        r_15["total_deflation_pct"],
        suffix="%")

    row("Total toolkit ($B)",
        r_none["total_toolkit_B"],
        r_14["total_toolkit_B"],
        r_15["total_toolkit_B"],
        fmt=",.0f", suffix="B")

    row("Total credit losses ($B)",
        r_none["total_credit_loss_B"],
        r_14["total_credit_loss_B"],
        r_15["total_credit_loss_B"],
        fmt=",.0f", suffix="B")

    # Year-by-year comparison
    print(f"\n  Year-by-year M2 ($B) — Transaction pool always protected at ${TRANSACTION_POOL/1e9:,.0f}B")
    print(f"  {'Year':>5} {'No toolkit':>12} {'14-tool':>12} {'15-tool':>12} {'T15 active':>12}")
    print(f"  {'-'*55}")
    for i in range(years):
        s0 = r_none["states"][i]
        s14 = r_14["states"][i]
        s15 = r_15["states"][i]
        t15_flag = "YES *" if s15["tool15_active"] else ""
        print(f"  {s0['year']:>5} "
              f"${s0['m2_B']:>10,.0f} "
              f"${s14['m2_B']:>10,.0f} "
              f"${s15['m2_B']:>10,.0f} "
              f"{t15_flag:>12}")

    # Summary assessment
    gap_closed = r_14["total_m2_contraction_pct"] - r_15["total_m2_contraction_pct"]
    pct_improvement = gap_closed / r_14["total_m2_contraction_pct"] * 100 if r_14["total_m2_contraction_pct"] > 0 else 0
    historical_gap = 30.0 - r_15["total_m2_contraction_pct"]

    print(f"\n  Tool 15 reduces M2 contraction by {gap_closed:.1f}pp vs 14-tool ({pct_improvement:.0f}% improvement)")
    print(f"  Final M2 contraction vs historical 30%: {r_15['total_m2_contraction_pct']:.1f}% "
          f"({'better' if historical_gap > 0 else 'worse'} by {abs(historical_gap):.1f}pp)")
    print(f"  Transaction pool: ${TRANSACTION_POOL/1e9:,.0f}B — PROTECTED throughout all scenarios")


if __name__ == "__main__":
    print("="*100)
    print("CITIZENS STANDARD — CASCADE MODEL v2: 14-TOOL vs 15-TOOL TOOLKIT COMPARISON")
    print(f"Tool 15: M2 Contraction Floor | Trigger: M2 contracts >{TOOL15_TRIGGER_M2_PCT}% rolling 12mo | "
          f"Ceiling: {TOOL15_CEILING_PCT*100:.0f}% M2 = ${TOOL15_CAP/1e9:,.0f}B/yr")
    print("="*100)

    print_scenario("Moderate (2008-equivalent)", 3.0, 3)
    print_scenario("Depression-magnitude",        6.0, 3)
    print_scenario("Extreme tail",               10.0, 3)
    print_scenario("Prolonged moderate",          3.0, 5)
    print_scenario("Prolonged Depression",        6.0, 5)

    print(f"\n{'='*100}")
    print("KEY FINDINGS — TOOL 15 EFFECTIVENESS")
    print("-"*100)
    # Run key scenarios for summary
    r2008_14 = run_cascade(3.0, 3, "14tool")
    r2008_15 = run_cascade(3.0, 3, "15tool")
    rdep_14  = run_cascade(6.0, 3, "14tool")
    rdep_15  = run_cascade(6.0, 3, "15tool")

    print(f"""
Tool 15 effectiveness under 2008-equivalent stress (3%/yr, 3yr):
  14-tool M2 contraction: {r2008_14['total_m2_contraction_pct']:.1f}%
  15-tool M2 contraction: {r2008_15['total_m2_contraction_pct']:.1f}%
  Improvement:            {r2008_14['total_m2_contraction_pct'] - r2008_15['total_m2_contraction_pct']:.1f}pp

Tool 15 effectiveness under Depression-magnitude stress (6%/yr, 3yr):
  14-tool M2 contraction: {rdep_14['total_m2_contraction_pct']:.1f}%
  15-tool M2 contraction: {rdep_15['total_m2_contraction_pct']:.1f}%
  Improvement:            {rdep_14['total_m2_contraction_pct'] - rdep_15['total_m2_contraction_pct']:.1f}pp
  vs historical 30%:      {rdep_15['total_m2_contraction_pct']:.1f}% (improvement of {30 - rdep_15['total_m2_contraction_pct']:.1f}pp vs historical)

Structural guarantee (all scenarios):
  Transaction pool = ${TRANSACTION_POOL/1e9:,.0f}B — constitutionally protected, never at risk
  Maximum possible M2 contraction = {TERM_DEPOSIT_SHARE*100:.0f}% (term deposit share only)
  Tool 15 does not eliminate cascade damage — it substantially reduces magnitude and duration
  The framework's honest claim: better failure mode, not no failure mode
""")
