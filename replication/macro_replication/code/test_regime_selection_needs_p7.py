"""
test_regime_selection_needs_p7.py
---------------------------------
COMPUTATIONAL test of the linchpin claim: does the framework's 'constitution
selects the inflation regime' claim actually REQUIRE P7's determinacy?

We simulate the forward price-gap system E_t x_{t+1} = theta * x_t + sunspot,
under determinacy (theta>1, P7 on) vs indeterminacy (theta<=1, P7 off), hit it
with the SAME sunspot noise, and measure whether the SELECTED regime (target
inflation) is actually delivered — i.e. whether the realized price path stays
anchored to the target or wanders to a different, self-fulfilling rate.

If the target is delivered ONLY under determinacy, regime selection depends on P7.
"""
import numpy as np

def simulate_path(theta, T=200, seed=0, sunspot_sd=0.5):
    """
    Forward-looking gap under RE. The MINIMAL-STATE (fundamental) solution is
    x_t = 0 (target delivered). But if |theta|<=1, NON-fundamental (sunspot)
    solutions x_t = theta*x_{t-1} + e_t are ALSO bounded equilibria -> the economy
    can follow them. If |theta|>1, only x_t=0 is bounded; sunspots explode and are
    ruled out -> target delivered.
    We test by running the BACKWARD recursion the sunspot equilibrium would follow
    and checking boundedness / drift away from target.
    """
    rng = np.random.default_rng(seed)
    x = 0.0
    path = []
    for t in range(T):
        e = rng.normal(0, sunspot_sd)
        # a candidate sunspot equilibrium evolves as x_t = (1/theta)*x_{t-1} + e
        # (the backward-stable root of the forward system); it is a VALID bounded
        # equilibrium iff |1/theta| < 1, i.e. |theta|>1 makes the sunspot DECAY...
        # WAIT: for a jump var, determinacy |theta|>1 means the ONLY bounded soln is 0.
        # The sunspot path uses the root that is bounded: if |theta|>1, sunspot must
        # satisfy x_t = theta x_{t-1}+e which EXPLODES -> not an equilibrium -> ruled out.
        # if |theta|<=1, x_t = theta x_{t-1}+e stays BOUNDED -> valid sunspot equilibrium.
        x = theta * x + e
        path.append(x)
    return np.array(path)

def analyze(theta, label):
    # run many sunspot draws; measure whether the path stays near target (0)
    drifts = []
    exploded = 0
    for seed in range(200):
        p = simulate_path(theta, seed=seed)
        if not np.all(np.isfinite(p)) or np.max(np.abs(p)) > 1e6:
            exploded += 1
        else:
            drifts.append(np.std(p[-50:]))  # late-sample dispersion around target
    if drifts:
        mean_drift = np.mean(drifts)
    else:
        mean_drift = float('inf')
    print(f"  {label} (theta={theta:.2f}):")
    print(f"    sunspot paths that EXPLODE (ruled out as equilibria): {exploded}/200")
    print(f"    bounded sunspot dispersion around target: {mean_drift:.2f}"
          + ("  (target NOT uniquely delivered)" if mean_drift>0.05 and exploded<100
             else "  (sunspots ruled out -> target delivered)"))
    return exploded, mean_drift

print("="*68)
print("Does regime selection REQUIRE P7's determinacy? (computational)")
print("="*68)
print()
print("P7 ON (determinate, theta>1): sunspot equilibria should EXPLODE and be ruled")
print("out, leaving the SELECTED target (x=0) as the unique outcome.")
e_on, d_on = analyze(1.375, "P7 ON  determinate")
print()
print("P7 OFF (indeterminate, theta<=1): sunspot equilibria stay BOUNDED -> the")
print("economy can self-fulfill a DIFFERENT inflation rate than the one selected.")
e_off, d_off = analyze(0.95, "P7 OFF indeterminate")
print()
print("="*68)
print("RESULT")
print("="*68)
target_delivered_on = e_on > 150      # sunspots explode -> ruled out -> target unique
target_lost_off = e_off < 50 and d_off > 0.05  # sunspots bounded -> target not unique
print(f"  P7 ON:  selected target uniquely delivered: {target_delivered_on}")
print(f"  P7 OFF: economy can sit at an UNSELECTED rate: {target_lost_off}")
print()
if target_delivered_on and target_lost_off:
    print("  CONFIRMED (computationally): 'the constitution selects the inflation")
    print("  regime' is a MEANINGFUL claim ONLY when P7 holds. Without determinacy,")
    print("  the selected regime is just one of many self-fulfilling outcomes -> the")
    print("  selection is empty. P7 is what gives regime selection its content.")
    print("  => P7 is LOAD-BEARING for the framework's central price-regime claim.")
else:
    print("  NOT confirmed — the dependence is weaker than argued; revisit.")
