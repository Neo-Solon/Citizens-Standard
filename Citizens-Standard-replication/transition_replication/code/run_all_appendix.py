"""
run_all_appendix.py
===================
Runs all Technical Appendix replication modules for the transition paper
(Neo-Solon, 2026c) and prints their outputs in sequence.

Usage:  python run_all_appendix.py
"""

import runpy
import sys

MODULES = [
    ("A.2  Debt trajectory",      "appendix_A2_debt_trajectory"),
    ("A.2  KT inflation",         "appendix_A2_kt_inflation"),
    ("A.3  Banking + KT synergy",  "appendix_A3_banking_synergy"),
    ("A.4  Equity rotation",      "appendix_A4_equity_rotation"),
    ("A.4.4 Rotation sensitivity","appendix_A4_4_rotation_sensitivity"),
    ("A.5  Mode T-stable",        "appendix_A5_mode_t_stable"),
]

if __name__ == "__main__":
    for label, mod in MODULES:
        print("\n" + "#" * 78)
        print(f"# {label}")
        print("#" * 78)
        runpy.run_module(mod, run_name="__main__")
    print("\n" + "=" * 78)
    print("All appendix modules reproduced. See AUDIT.md for the validation table.")
    print("=" * 78)
