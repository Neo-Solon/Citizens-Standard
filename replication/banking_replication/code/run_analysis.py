"""
run_analysis.py
===============
Unified entry point for the Paper 6 banking replication. This does NOT add new
analysis -- it dispatches to the existing modules and assembles their output into
one consolidated evidence report, and it exposes a query mode for one-off
questions. It exists so the package answers "what do we know, and how robust is
it?" from a single command, rather than requiring a reader to run six scripts.

FULL REPORT (default) -- runs the whole battery in order:
    python3 run_analysis.py
      1. propositions      (test_propositions.py)   -- do N1-N5 hold at baseline?
      2. balance sheet     (balance_sheet.py)        -- the derived quantities
      3. sensitivity       (sensitivity.py)          -- sweeps + thresholds + 10k invariants
      4. exploration       (explore.py)              -- discovered boundaries
      5. parameter import. (parameter_importance.py) -- what drives each proposition

QUERY MODE -- ask one thing:
    python3 run_analysis.py propositions        # just the PASS/FAIL battery
    python3 run_analysis.py thresholds          # just discovered boundaries
    python3 run_analysis.py robustness          # just the 10k Monte Carlo pass rates
    python3 run_analysis.py importance          # just parameter importance
    python3 run_analysis.py what-if collateral=2.0     # a single what-if
    python3 run_analysis.py boundary chi_c             # where a proposition flips
    python3 run_analysis.py dashboard           # one-page verification dashboard
    python3 run_analysis.py summary             # one-screen headline numbers only
"""

import sys
import io
import contextlib


def _rule(title):
    print("\n" + "=" * 72)
    print("# " + title)
    print("=" * 72)


# ---------------------------------------------------------------------------
# section runners (each imports the real module and calls its entry function)
# ---------------------------------------------------------------------------
def run_propositions():
    _rule("PROPOSITION TESTS  (N1-N5 at baseline; derived, structural vs calibration)")
    import test_propositions as tp
    tp._print_group("structural", "STRUCTURAL (unchanged if parameters change):")
    tp._print_group("calibration", "\nCALIBRATION-DEPENDENT (contingent on calibrated values):")
    ok = all(r[1] for r in tp._results)
    print(f"\n  -> {'ALL PROPOSITIONS PASS' if ok else 'SOME FAILED'} "
          f"({sum(1 for r in tp._results if r[1])}/{len(tp._results)})")
    return ok


def run_balance_sheet():
    _rule("BALANCE SHEET  (derived quantities; intentionally minimal scope)")
    import balance_sheet as bs
    # balance_sheet prints its summary under __main__; call the pieces directly
    inc, cs = bs.incumbent(), bs.citizens_standard()
    print(f"  incumbent inside-money share of money stock: {inc['inside_share']:.2f}")
    print(f"  CS transaction money  = ${cs['transaction_money']:.1f}T")
    print(f"  CS term deposits      = ${cs['term_deposits']:.1f}T")
    print(f"  CS inside money (derived) = ${cs['inside_money']:.3f}T")
    print(f"  CS credit capacity    = ${cs['credit_capacity']:.1f}T")
    print(f"  determinacy root theta = {bs.determinacy_root():.2f}")


def run_sensitivity():
    _rule("SENSITIVITY, THRESHOLDS, AND 10,000-DRAW MONTE CARLO")
    import sensitivity as s
    s.sensitivity_table()
    print()
    s.threshold_discovery()
    print()
    s.randomized_invariants()


def run_exploration():
    _rule("EXPLORATION  (discovered boundaries)")
    import explore as e
    e.discover()


def run_importance():
    _rule("PARAMETER IMPORTANCE  (what drives each proposition)")
    import parameter_importance as pi
    pi.analyze()


# ---------------------------------------------------------------------------
# query helpers
# ---------------------------------------------------------------------------
def query_thresholds():
    import explore as e
    e.discover()


def query_robustness():
    import sensitivity as s
    s.randomized_invariants()


def query_what_if(kvs):
    import explore as e
    params = {}
    for kv in kvs:
        k, v = kv.split("=")
        params[k] = float(v)
    e.what_if(**params)


def query_boundary(param):
    import explore as e
    b = e.stability_boundary(param, 0.0, 1.0)
    print(f"separation flips at {param} = {b:.4f}" if b
          else f"no separation flip over {param} in [0,1]")


def query_summary():
    """One-screen headline numbers, assembled from the modules (silently)."""
    import balance_sheet as bs
    import explore as e
    import sensitivity as s
    with contextlib.redirect_stdout(io.StringIO()):
        import test_propositions as tp
        n_pass = sum(1 for r in tp._results if r[1])
        n_tot = len(tp._results)
        max_ts = e.max_term_share(0.25)
        max_k = e.max_credit_intensity()
        max_nm = e.max_near_money(0.25)
    cs = bs.citizens_standard()
    print("PAPER 6 BANKING -- HEADLINE EVIDENCE")
    print("-" * 48)
    print(f"  propositions passing at baseline:      {n_pass}/{n_tot}")
    print(f"  CS credit capacity:                    ${cs['credit_capacity']:.1f}T")
    print(f"  CS inside money (derived):             ${cs['inside_money']:.3f}T")
    print(f"  max term-deposit share (M_o>=25% M2):  {max_ts:.3f}")
    print(f"  max credit intensity (separation):     {max_k:.3f}")
    print(f"  max observable near-money (<=25% M_T):  {max_nm:.1%}")
    print("  (run 'python3 run_analysis.py' for the full report)")


# ---------------------------------------------------------------------------
# dispatch
# ---------------------------------------------------------------------------
def dashboard():
    """One-page verification dashboard: PASS/FAIL grid + headline diagnostics.
    All quantities are the model's real diagnostics (not the stale B-vocabulary).
    """
    import io, contextlib
    import balance_sheet as bs
    import explore as e
    with contextlib.redirect_stdout(io.StringIO()):
        import test_propositions as tp
        results = list(tp._results)
        max_ts = e.max_term_share(0.25)
        max_k = e.max_credit_intensity()
    cs = bs.citizens_standard()
    inc = bs.incumbent()
    coupling = bs.LAMBDA_LEAK + bs.CHI_C * bs.PHI_LIQ
    ctrl_margin_pp = (bs.ZETA_STAR - coupling) * 100.0
    reserved_share = 1.0 - bs.TERM_SHARE          # run-proof (unrunnable) share
    atrisk_share = bs.TERM_SHARE                  # term-deposit (runnable) share
    equity_ratio = cs["equity"] / cs["credit_capacity"]
    all_pass = all(r[1] for r in results)
    # binding constraint for credit capacity
    D = cs["term_deposits"]; E = cs["equity"]
    binding = "term deposits (funding)" if D <= (bs.LEVERAGE - 1.0) * E + 1e-9 else "equity (leverage)"

    line = "=" * 42
    print(line)
    print("      Paper 6 Verification Summary")
    print(line)
    print()
    titles = {"N1": "complete monetary control",
              "N2": "circuit separation",
              "N3": "credit capacity",
              "N4": "run-proof payments",
              "N5": "near-money boundary"}
    for tag, ok, kind, title, detail in results:
        print(f"  {tag}  {'PASS' if ok else 'FAIL'}   {titles.get(tag, '')}  [{kind}]")
    print()
    print(f"  Inside money (derived):        ${cs['inside_money']:.3f}T  (0 = full control)")
    print(f"  Determinacy root theta:        {bs.determinacy_root():.2f}  (>1 = determinate)")
    print(f"  Credit capacity:               ${cs['credit_capacity']:.1f}T")
    print(f"  Binding constraint:            {binding}")
    print(f"  Equity / credit capacity:      {equity_ratio:.1%}")
    print()
    print(f"  Run-proof (reserved) share:    {reserved_share:.0%}")
    print(f"  At-risk (term-deposit) share:  {atrisk_share:.0%}")
    print(f"  Controllability margin:        {ctrl_margin_pp:.1f} pp  (zeta* - coupling)")
    print()
    print(f"  Max term-deposit share:        {max_ts:.3f}  (keeps M_o >= 25% of M2)")
    print(f"  Max credit intensity:          {max_k:.3f}  (preserves separation)")
    print()
    print(line)
    if all_pass:
        print("  Overall: all structural propositions verified;")
        print("           calibration-dependent ones hold at baseline.")
    else:
        print("  Overall: ONE OR MORE PROPOSITIONS FAILED -- see detail.")
    print(line)
    return all_pass


def full_report():
    print("#" * 72)
    print("# PAPER 6 -- FULL-RESERVE BANKING: CONSOLIDATED EVIDENCE REPORT")
    print("# (unified driver over the replication modules; no new analysis)")
    print("#" * 72)
    print()
    dashboard()
    ok = run_propositions()
    run_balance_sheet()
    run_sensitivity()
    run_exploration()
    run_importance()
    _rule("END OF REPORT")
    return ok


def main(argv):
    if not argv:
        ok = full_report()
        sys.exit(0 if ok else 1)

    cmd = argv[0]
    if cmd == "propositions":
        sys.exit(0 if run_propositions() else 1)
    elif cmd == "thresholds":
        query_thresholds()
    elif cmd == "robustness":
        query_robustness()
    elif cmd == "importance":
        run_importance()
    elif cmd == "sensitivity":
        run_sensitivity()
    elif cmd == "what-if":
        query_what_if(argv[1:])
    elif cmd == "boundary" and len(argv) > 1:
        query_boundary(argv[1])
    elif cmd == "summary":
        query_summary()
    elif cmd == "dashboard":
        sys.exit(0 if dashboard() else 1)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
