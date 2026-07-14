"""
paper05_liquidation — verifies that `liquidation_flow_replication/` still reproduces the
numbers the site's methodology page cites (the liquidation flow L_t, Macro §3.3; the
circulating-pool ceiling and kappa_d schedule).

Same adapter pattern as paper05_macro: the package is NOT copied here. It stays at
`replication/liquidation_flow_replication/` and remains independently runnable. This
adapter copies it to a scratch dir, runs its own entry point offline, and compares every
produced number against the golden artifact. See ../../paper_pkg.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPL = HERE.parents[2]                 # replication/
sys.path.insert(0, str(REPL))
from paper_pkg import verify

PKG       = REPL / "liquidation_flow_replication"
ENTRY     = 'code/run_all.py'
ARTIFACTS = [('stdout', 'all_results.txt')]


def run(data_dir=None, refresh=False):
    # data_dir/refresh are part of the harness contract; this package ships its own
    # bundled data (SSA life table), so both are accepted and ignored.
    return verify(PKG, ENTRY, ARTIFACTS)


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2)[:2500])
