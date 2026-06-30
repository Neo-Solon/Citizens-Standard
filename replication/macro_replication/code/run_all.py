"""
run_all.py — runs the full Paper 5 computational supplement and captures output.
"""
import subprocess
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ["verify_proposition_3.py", "verify_proposition_3prime.py",
           "verify_proposition_4.py", "verify_proposition_5.py", "verify_proposition_6.py", "verify_proposition_7.py", "verify_proposition_8.py", "verify_proposition_9.py",
           "verify_realizable_return.py",
           "recompute_illustrations.py", "make_figure.py",
           "make_determinacy_figure.py", "make_labor_figure.py", "make_delay_figure.py", "make_irf_figure.py", "make_forward_figure.py", "make_welfare_figure.py", "make_banking_figure.py"]


def main():
    for s in SCRIPTS:
        print("\n" + "#" * 72)
        print("# RUNNING:", s)
        print("#" * 72)
        r = subprocess.run([sys.executable, os.path.join(HERE, s)],
                           capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        if r.returncode != 0:
            sys.stderr.write(r.stderr)
            print(f"[{s} exited with code {r.returncode}]")


if __name__ == "__main__":
    main()
