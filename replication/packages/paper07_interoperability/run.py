"""
paper07_interoperability — verifies that `interoperability_replication/` still reproduces the numbers the paper publishes.

The package itself is NOT copied here. It stays where the repo keeps it, at
`replication/interoperability_replication/`, and remains independently runnable. This adapter only drives it:
copy to a scratch dir, run its own entry point offline, compare every produced number against
the golden artifact the paper cites. See ../../paper_pkg.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPL = HERE.parents[2]                 # replication/
sys.path.insert(0, str(REPL))
from paper_pkg import verify

PKG       = REPL / "interoperability_replication"
ENTRY     = 'code/_harness_report.py'
ARTIFACTS = [('stdout', 'outputs/behavioral_calibrated.out.txt'), ('stdout', 'outputs/behavioral_idle_capital.out.txt'), ('stdout', 'outputs/cs_channel_test.out.txt'), ('stdout', 'outputs/cs_contraction_compare.out.txt'), ('stdout', 'outputs/cs_engine.out.txt'), ('stdout', 'outputs/cs_independence_redteam.out.txt'), ('stdout', 'outputs/cs_sterilization_test.out.txt'), ('stdout', 'outputs/equa_model_v3.out.txt'), ('stdout', 'outputs/equa_redteam.out.txt'), ('stdout', 'outputs/equa_stress.out.txt'), ('stdout', 'outputs/fig_paper7.out.txt')]


def run(data_dir=None, refresh=False):
    # data_dir/refresh are part of the harness contract; this package ships its own
    # bundled snapshot, so both are accepted and ignored.
    return verify(PKG, ENTRY, ARTIFACTS)


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2)[:2500])
