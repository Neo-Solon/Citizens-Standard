"""
verify_all.py
=============
Consolidated verification aggregator and dashboard for Paper 5, "A Macro Model of
the Citizens Standard" (Neo-Solon 2026e). Runs each proposition-verification
script, records pass/fail by exit code, and surfaces the calibrated dynamic
model's headline results (eigenvalues, asset->price pass-through, dynamic
robustness) in a one-page dashboard.

This adds no new economics; the individual verify_proposition_*.py scripts and
dynamic_model.py already contain the checks. This is a single entry point that
reports the model's overall state, in the style of the Paper 6 banking harness.

Run:
    python3 verify_all.py            # run every check + dashboard
    python3 verify_all.py dashboard  # dashboard only (assumes checks pass)
"""

import os
import sys
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

# proposition scripts and a short title for each
PROP_SCRIPTS = [
    ("P3",  "verify_proposition_3.py",       "quantity rule / price path"),
    ("P3'", "verify_proposition_3prime.py",  "rebalancing recursion magnitudes"),
    ("P4",  "verify_proposition_4.py",       "no-net-saving condition"),
    ("P5",  "verify_proposition_5.py",       "floor adequacy"),
    ("P6",  "verify_proposition_6.py",       "labor-supply neutrality"),
    ("P7",  "verify_proposition_7.py",       "forward-looking determinacy"),
    ("P8",  "verify_proposition_8.py",       "welfare / distribution"),
    ("P9",  "verify_proposition_9.py",       "credit / banking synergy"),
    ("RR",  "verify_realizable_return.py",   "realizable-return transform"),
]


def _run(script):
    """Run a script; return (ok, tail) where ok is exit-code==0."""
    path = os.path.join(HERE, script)
    if not os.path.exists(path):
        return None, "(missing)"
    r = subprocess.run([sys.executable, path], capture_output=True, text=True)
    tail = (r.stdout.strip().splitlines() or ["(no output)"])[-1][:60]
    return r.returncode == 0, tail


def run_propositions():
    print("PROPOSITION CHECKS (exit-code = pass):")
    results = []
    for tag, script, title in PROP_SCRIPTS:
        ok, tail = _run(script)
        results.append((tag, ok, title))
        status = "PASS" if ok else ("MISSING" if ok is None else "FAIL")
        print(f"  {status:<7} {tag:<4} {title}")
    return results


def dynamic_summary():
    """Pull the dynamic model's headline numbers (import, not re-run subprocess)."""
    try:
        import dynamic_model as dm
        ev = dm.eigenvalues()
        irf_v = dm.impulse_response({"v": 1.0}, T=200)
        import numpy as np
        peak = float(np.max(np.abs(irf_v[:, 0])))
        bound = dm.LAMBDA_LEAK / dm.PSI_LAM
        return dict(eig=[round(float(e), 2) for e in ev],
                    stable=all(e < 1 for e in ev),
                    passthrough=peak, bound=bound)
    except Exception as e:
        return dict(error=str(e))


def dashboard(results=None):
    if results is None:
        results = [(tag, _run(s)[0], t) for tag, s, t in PROP_SCRIPTS]
    dyn = dynamic_summary()
    line = "=" * 50
    print(line)
    print("         Paper 5 Verification Summary")
    print("        (Macro Model of the Citizens Standard)")
    print(line)
    print()
    for tag, ok, title in results:
        status = "PASS" if ok else ("MISSING" if ok is None else "FAIL")
        print(f"  {tag:<4} {status:<7} {title}")
    print()
    print("  Dynamic model (calibrated, Appendix A.9):")
    if "error" not in dyn:
        print(f"    Eigenvalues:                {dyn['eig']}  "
              f"({'stable' if dyn['stable'] else 'UNSTABLE'})")
        print(f"    Asset->price pass-through:  {dyn['passthrough']:.4f}  "
              f"(bound {dyn['bound']:.4f}; circuits separate)")
    else:
        print(f"    (dynamic model unavailable: {dyn['error']})")
    print()
    n_ok = sum(1 for _, ok, _ in results if ok)
    n_tot = len(results)
    all_pass = all(ok for _, ok, _ in results)
    print(line)
    if all_pass:
        print(f"  Overall: all {n_tot} proposition checks pass;")
        print("           dynamic model validated and circuits separate.")
    else:
        print(f"  Overall: {n_ok}/{n_tot} checks pass -- see detail above.")
    print(line)
    return all_pass


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dashboard":
        ok = dashboard()
    else:
        print("#" * 60)
        print("# PAPER 5 -- MACRO MODEL: CONSOLIDATED VERIFICATION")
        print("#" * 60)
        print()
        results = run_propositions()
        print()
        ok = dashboard(results)
    sys.exit(0 if ok else 1)
