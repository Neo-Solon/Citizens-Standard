# RESOLVED (empirically grounded): Mode C KI rate AND deflation

## Two issues, both now resolved on grounded principles (not by fiat)

### Issue 1 — KI RATE (was 3.65% in stale checks)
Paper 1 states 1.98% of M2 = 3.85% of M^T, $108/mo. Verified across Papers 1/5/9.
The engine was already correct (1.98%); stale run_all.py checks + two figure
scripts still had the old 3.65%/$199. All fixed to 1.98%/$108.

### Issue 2 — KI DEFLATION (engine gave $144K, paper says $80K)
The engine's simulate() deflated the spent KI stream at derive_cpi (0.33%, an
M2-wide base). Grounding shows this is WRONG on the framework's own terms:

  - KI is an immediately-spendable consumption dividend, so it chases GOODS
    through the TRANSACTION circuit M^T, not the whole of M2.
  - CS's core thesis (Papers 5-8) is circuit separation: asset-circuit money does
    NOT chase consumer goods. So consumer inflation is governed by M^T, giving
    1.98%/0.514 = 3.85% of M^T ~ 2% consumer inflation (the engine's cpi_target).
  - The engine's derive_cpi (diluting KI across all M2 -> 0.33%) CONTRADICTS the
    framework's own separation thesis.
  - Empirical cross-check: the validation horserace found the transaction measure
    (M1) carries the high-inflation price signal (t=2.28) while broad M2 goes
    insignificant (t=-0.37) -- supporting the M^T base.

FIX: simulate() now deflates the KI stream at cpi_target (M^T, ~2%), while the
floor keeps its regime-independent real-equity deflation. Result:
  Mode C floor $234K + KI $81K = $315K  (paper: $230K + $80K = $310K). 

The floor ($234K) was grounded separately: 5.4% is a conservative REAL equity
return (empirical real S&P ~7% over 1926-2024), and the floor is correctly
regime-independent (Mode A $235K vs Mode C $234K), which the engine's method
achieves and modec_ki_real_check's real-GDP deflation does not.

## Net: the paper's $310K was CORRECT, and now we know WHY from first principles.
All 22 architecture self-checks pass on grounded values. Modes A/B unaffected
(ki=0). Interoperability's engine copy has no KI path (unaffected).
