"""
paper12_crisis — verifies that `crisis_behaviour_replication/` still reproduces the numbers the paper publishes.

The package itself is NOT copied here. It stays where the repo keeps it, at
`replication/crisis_behaviour_replication/`, and remains independently runnable. This adapter only drives it:
copy to a scratch dir, run its own entry point offline, compare every produced number against
the golden artifact the paper cites. See ../../paper_pkg.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPL = HERE.parents[2]                 # replication/
sys.path.insert(0, str(REPL))
from paper_pkg import verify

PKG       = REPL / "crisis_behaviour_replication"
ENTRY     = 'run_all.py'
ARTIFACTS = [('json', 'results/stress_results.json')]


def run(data_dir=None, refresh=False):
    # data_dir/refresh are part of the harness contract; this package ships its own
    # bundled snapshot, so both are accepted and ignored.
    return verify(PKG, ENTRY, ARTIFACTS)


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2)[:2500])
