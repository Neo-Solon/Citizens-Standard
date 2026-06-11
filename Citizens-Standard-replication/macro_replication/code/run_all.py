"""
run_all.py — runs the full Paper 5 computational supplement and captures output.
"""
import subprocess
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ["verify_proposition_3.py", "recompute_illustrations.py", "make_figure.py"]


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
