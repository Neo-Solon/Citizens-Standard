"""
credit_stress_test_v2.py
========================
Banking architecture STATIC stress test for the Citizens Standard framework.

WHAT THIS IS (and is not):
This is the STATIC, no-feedback bound on credit losses. It applies a fixed
annual loss rate to the lending book and asks whether the layered buffer
structure (bank equity -> TLF -> term depositors; payment pool always
protected) absorbs the cumulative loss. It deliberately does NOT model
deleveraging, Fisher debt-deflation amplification, or money-supply feedback.

Because it omits those dynamics, this test is a LOWER BOUND on stress: it
shows the best case in which losses do not compound. The BINDING analysis
under deflationary feedback is the dynamic cascade model
(credit_cascade_test_v3.py), where the same headline shocks produce larger
losses and meaningful M2 contraction. The two are companions:
  - This file: does the static buffer stack absorb a given cumulative loss?
  - Cascade v3: what happens once losses amplify through debt-deflation?

Read the two together. Where they appear to disagree (e.g. a Depression-
magnitude shock looks fully absorbed here but produces depositor losses in
the cascade), the cascade is the operative result; this file shows only that
the buffer stack holds ABSENT amplification.

This script is a companion to the main replication package.
Run: python3 credit_stress_test_v2.py

Parameters calibrated to launch values from the architectural paper
(Neo-Solon, 2026a, Section 9 and Technical Appendix A.6):
  - M2 at launch:          $22,366B (FRED M2SL)
  - Transaction account %: 40% of M2 (full reserve, protected)
  - Term deposit %:        60% of M2 (fractional reserve, credit risk)
  - Max leverage ratio:    4:1 (normal conditions)
  - Bank equity buffer:    25% of lending book (implied by 4:1 leverage)
  - TLF ceiling:           ~$492B (Tool 5: 2.2% of M2)
"""

# =============================================================================
# Launch parameters (from Technical Appendix A.1 and Section 9)
# =============================================================================

M2_LAUNCH_B          = 22_366.0   # $B, FRED M2SL end-2025
TRANSACTION_SHARE    = 0.40       # full-reserve, constitutionally protected
TERM_DEPOSIT_SHARE   = 0.60       # fractional-reserve, credit risk
MAX_LEVERAGE         = 4.0        # normal conditions (Section 9.2)
BANK_EQUITY_RATIO    = 0.25       # equity / lending book (implied by 4:1)

# Emergency tool ceilings (% of M2, Section 10 / Appendix A.6)
TLF_CEILING_PCT      = 0.022      # Tool 5: Private Credit Guarantee (2.2%)

# Stress scenarios: annual credit loss rate as % of lending book
LOSS_RATE_SCENARIOS  = [0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 10.0]
DURATION_YEARS       = [1, 2, 3, 5, 10]

# =============================================================================
# Derived launch values
# =============================================================================

M2                   = M2_LAUNCH_B * 1e9
TRANSACTION_POOL     = M2 * TRANSACTION_SHARE
TERM_DEPOSIT_POOL    = M2 * TERM_DEPOSIT_SHARE
LENDING_BOOK         = TERM_DEPOSIT_POOL * (MAX_LEVERAGE / (MAX_LEVERAGE - 1))
BANK_EQUITY          = LENDING_BOOK * BANK_EQUITY_RATIO
TLF_BUFFER           = M2 * TLF_CEILING_PCT

# =============================================================================
# Static stress model (no feedback)
# =============================================================================

def run_stress(loss_rate_pct, duration_years, verbose=False):
    """
    STATIC model: a fixed annual credit loss of `loss_rate_pct`% of the
    ORIGINAL lending book, sustained for `duration_years`. No deleveraging,
    no Fisher amplification, no money-supply feedback (those are in the
    dynamic cascade model).

    Layering, applied to CUMULATIVE loss (single coherent waterfall):
      1. Bank equity absorbs losses first (up to BANK_EQUITY).
      2. TLF absorbs the next tranche (up to TLF_BUFFER).
      3. Any remainder falls on term depositors (explicit risk-bearers).
      4. The transaction pool is never touched (full-reserve separation).

    All depositor / TLF figures derive from the SAME cumulative-loss waterfall,
    so the loop and the summary cannot disagree.
    """
    loss_rate = loss_rate_pct / 100.0
    annual_loss = LENDING_BOOK * loss_rate
    cumulative_loss = annual_loss * duration_years

    # Year in which cumulative loss first exceeds the equity buffer
    equity_exhausted_year = None
    if annual_loss > 0:
        crossover = BANK_EQUITY / annual_loss
        if crossover < duration_years:
            # first full year in which cumulative loss exceeds equity
            equity_exhausted_year = int(crossover) + 1
            if equity_exhausted_year > duration_years:
                equity_exhausted_year = None

    # Single coherent waterfall on cumulative loss
    loss_after_equity = max(0.0, cumulative_loss - BANK_EQUITY)   # beyond equity
    tlf_required      = min(loss_after_equity, TLF_BUFFER)         # TLF tranche used
    tlf_gap           = max(0.0, loss_after_equity - TLF_BUFFER)   # uncovered
    tlf_sufficient    = (loss_after_equity <= TLF_BUFFER)

    # Depositor loss = remainder after equity AND TLF are exhausted
    depositor_loss    = tlf_gap
    depositor_loss_pct = (depositor_loss / TERM_DEPOSIT_POOL * 100
                          if TERM_DEPOSIT_POOL > 0 else 0.0)

    # Depositor loss if NO TLF support at all (equity only)
    depositor_loss_no_tlf = loss_after_equity
    depositor_loss_no_tlf_pct = (depositor_loss_no_tlf / TERM_DEPOSIT_POOL * 100
                                 if TERM_DEPOSIT_POOL > 0 else 0.0)

    if verbose:
        print(f"  annual=${annual_loss/1e9:.1f}B  cumulative=${cumulative_loss/1e9:.1f}B  "
              f"equity=${BANK_EQUITY/1e9:.1f}B  beyond_equity=${loss_after_equity/1e9:.1f}B")

    return {
        "loss_rate_pct":            loss_rate_pct,
        "duration_years":           duration_years,
        "cumulative_loss_B":        cumulative_loss / 1e9,
        "bank_equity_B":            BANK_EQUITY / 1e9,
        "equity_exhausted_year":    equity_exhausted_year,
        "tlf_required_B":           tlf_required / 1e9,
        "tlf_ceiling_B":            TLF_BUFFER / 1e9,
        "tlf_sufficient":           tlf_sufficient,
        "tlf_gap_B":                tlf_gap / 1e9,
        "depositor_loss_B":         depositor_loss / 1e9,            # after equity+TLF
        "depositor_loss_pct":       depositor_loss_pct,
        "depositor_loss_no_tlf_B":  depositor_loss_no_tlf / 1e9,     # after equity only
        "depositor_loss_no_tlf_pct": depositor_loss_no_tlf_pct,
        "payment_system_at_risk":   False,    # full-reserve separation, by design
        "transaction_pool_B":       TRANSACTION_POOL / 1e9,
    }

# =============================================================================
# Output
# =============================================================================

def print_header():
    print("=" * 112)
    print("CITIZENS STANDARD — BANKING ARCHITECTURE STATIC CREDIT STRESS TEST (v2)")
    print("STATIC no-feedback bound. Dynamic binding analysis: credit_cascade_test_v3.py")
    print(f"Launch: M2=${M2/1e9:,.0f}B  Transaction pool (protected)=${TRANSACTION_POOL/1e9:,.0f}B  "
          f"Term deposits=${TERM_DEPOSIT_POOL/1e9:,.0f}B")
    print(f"Lending book=${LENDING_BOOK/1e9:,.0f}B  Bank equity buffer=${BANK_EQUITY/1e9:,.0f}B  "
          f"TLF ceiling=${TLF_BUFFER/1e9:,.0f}B")
    print("=" * 112)
    print(f"\n{'Loss rate':>10} {'Duration':>10} {'Cum. loss':>12} "
          f"{'Equity gone':>13} {'TLF used':>12} {'TLF covers?':>16} "
          f"{'Dep. loss (after TLF)':>22} {'Payment sys':>14}")
    print(f"{'(%/yr)':>10} {'(years)':>10} {'($B)':>12} "
          f"{'(year)':>13} {'($B)':>12} {'':>16} "
          f"{'($B / % of TD)':>22} {'at risk?':>14}")
    print("-" * 112)

def print_row(r):
    eq_yr  = str(r['equity_exhausted_year']) if r['equity_exhausted_year'] else "Never"
    tlf_ok = "YES" if r['tlf_sufficient'] else f"NO (gap=${r['tlf_gap_B']:.0f}B)"
    dep    = (f"${r['depositor_loss_B']:.1f}B / {r['depositor_loss_pct']:.1f}%"
              if r['depositor_loss_B'] > 0 else "$0 / 0.0%")
    pay    = "NO (protected)" if not r['payment_system_at_risk'] else "YES"
    print(f"{r['loss_rate_pct']:>10.1f} {r['duration_years']:>10} "
          f"{r['cumulative_loss_B']:>12.1f} {eq_yr:>13} "
          f"{r['tlf_required_B']:>12.1f} {tlf_ok:>16} "
          f"{dep:>22} {pay:>14}")

def print_summary_matrix():
    print("\n" + "=" * 92)
    print("OUTCOME MATRIX — does equity+TLF absorb cumulative loss? "
          "(Y=yes, N=depositors hit) | payment pool always protected")
    print(f"{'':16}", end="")
    for d in DURATION_YEARS:
        print(f"  {d:>3}yr", end="")
    print()
    print("-" * 92)
    for lr in LOSS_RATE_SCENARIOS:
        print(f"  {lr:>5.1f}%/yr     ", end="")
        for d in DURATION_YEARS:
            r = run_stress(lr, d)
            print(f"  {'Y  ' if r['tlf_sufficient'] else 'N  ':>4}", end="")
        print()

def print_calibration(label, rate, years, note):
    print("\n" + "=" * 92)
    print(f"HISTORICAL CALIBRATION — {label}")
    print("-" * 92)
    print(note)
    print()
    r = run_stress(rate, years)
    print(f"Citizens Standard, STATIC bound ({rate}%/yr for {years} years):")
    print(f"  Cumulative credit loss:     ${r['cumulative_loss_B']:,.1f}B")
    print(f"  Bank equity buffer:         ${r['bank_equity_B']:,.1f}B")
    print(f"  Equity exhausted in year:   {r['equity_exhausted_year'] or 'Never'}")
    print(f"  TLF used:                   ${r['tlf_required_B']:,.1f}B "
          f"(ceiling ${r['tlf_ceiling_B']:,.1f}B)")
    print(f"  Equity+TLF sufficient:      {'YES' if r['tlf_sufficient'] else 'NO'}")
    print(f"  Depositor loss after TLF:   ${r['depositor_loss_B']:,.1f}B "
          f"({r['depositor_loss_pct']:.1f}% of term deposits)")
    print(f"  Depositor loss, equity only:${r['depositor_loss_no_tlf_B']:,.1f}B "
          f"({r['depositor_loss_no_tlf_pct']:.1f}% of term deposits)")
    print(f"  Transaction accounts:       ${r['transaction_pool_B']:,.1f}B — PROTECTED")
    print(f"  Payment system at risk:     NO (full-reserve separation)")
    print(f"  NOTE: static bound only. Under deflationary feedback, the cascade")
    print(f"        model (v3) shows this shock produces larger losses and M2")
    print(f"        contraction; that is the operative result.")

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    print_header()
    for lr in LOSS_RATE_SCENARIOS:
        for d in DURATION_YEARS:
            print_row(run_stress(lr, d))
        print()

    print_summary_matrix()

    print_calibration(
        "2008 FINANCIAL CRISIS",
        3.0, 2,
        "2008 peak bank charge-off rate (FDIC): ~3.0% of loans; "
        "genuine liquidity support ~$2.9T.")

    print_calibration(
        "GREAT DEPRESSION",
        6.0, 4,
        "1930-1933 estimated bank loan losses: ~25% cumulative (~6%/yr).")

    print("\n" + "=" * 92)
    print("KEY FINDINGS (STATIC BOUND)")
    print("-" * 92)
    print("""
1. The payment system (transaction accounts, $8,946B) is NEVER at risk —
   full-reserve separation is the architectural guarantee regardless of the
   credit loss rate. This holds in the static AND dynamic analyses.

2. The bank equity buffer ($4,473B, 25% of the lending book) absorbs losses
   first; the TLF ($492B) absorbs the next tranche; term depositors — explicit
   credit-risk bearers — absorb any remainder. The transaction pool never enters
   the waterfall.

3. STATIC bound: at a 6%/yr loss applied to a FIXED lending book for 4 years,
   cumulative loss (~$4,294B) is just within the equity buffer (~$4,473B), so
   the static test shows near-zero depositor loss. This is the NO-FEEDBACK case.

4. The static bound is NOT the operative stress result. The dynamic cascade
   model (credit_cascade_test_v3.py) adds deleveraging and Fisher debt-deflation
   amplification, under which the same 6%/yr shock produces meaningful depositor
   losses and ~16-22% M2 contraction. Where the two differ, the cascade governs.

5. The correct failure mode, in both analyses: credit losses fall on explicit
   risk-bearers (term depositors) and the credit system, NOT on payment
   infrastructure — unlike 1930-1933, when no separation existed and bank
   failures destroyed savings AND payments simultaneously.
""")
