"""
floor_by_age.py  --  Extract the locked-floor (and reinvested K3 dividend) accumulation
by age from the issuance engine, in 2022 dollars (the SCF price base).

The engine's base-cohort (born 1960, retire 2025) Stable Floor is the canonical
$209,942 (2025$). We capture the running balance at each age and deflate to 2022$
via the engine's own CPI series. The endpoint reproduces the engine's compute_cohort
output exactly -- the correctness check.
"""
import json
import os
import deterministic_engine as E


def build(birth=1960, retire=2025):
    data = E.build_dataset(end_year=2060)
    cpi22 = data[2022]["cpi_ann"]
    cpi25 = data[2025]["cpi_ann"]

    def deflate25(n, y):  # nominal -> 2025$
        return n * (cpi25 / data[y]["cpi_ann"])

    bal = 0.0
    k3b = 0.0
    floor = {}
    k3 = {}
    for y in range(birth, retire + 1):
        age = y - birth
        d = data[y]
        gdp_pc = (d["GDP"] * 1e9) / (d["pop"] * 1e6)
        k1 = gdp_pc * E.K1_FRACTION if y == birth else 0.0
        prev_m2 = (data[y - 1]["M2"] * 1e9) if (y - 1) in data else d["M2"] * 1e9
        rg = max(0.0, d["rgdp"] / 100.0)
        pop = d["pop"] * 1e6
        k2 = (rg * prev_m2 * E.K2_FRACTION) / pop
        if getattr(E, "K2_RESIDUAL", False):
            k2 = max(0.0, k2 - E.k1_residual_deduction_per_capita(y, gdp_pc, pop, E.K1_FRACTION))
        k3n = (1.0 - E.FLOOR_SHARE) * k2
        k2 = E.FLOOR_SHARE * k2
        bal = (bal + deflate25(k1, y) + deflate25(k2, y)) * (1 + E.GE_REALIZABLE_RETURN)
        k3b = (k3b + deflate25(k3n, y)) * (1 + E.K3_REINVEST_RATE)
        floor[age] = bal * (cpi22 / cpi25)   # store in 2022$
        k3[age] = k3b * (cpi22 / cpi25)

    # correctness check against the engine's own output
    engine_floor = E.compute_cohort(data, birth, retire, post_real_equity_return=E.GE_REALIZABLE_RETURN)
    my_floor_2025 = floor[retire - birth] * (cpi25 / cpi22)
    assert abs(my_floor_2025 - engine_floor) < 1.0, (my_floor_2025, engine_floor)
    return {"floor": floor, "k3": k3, "cpi22": cpi22, "cpi25": cpi25,
            "engine_floor_2025": engine_floor}


if __name__ == "__main__":
    out = build()
    print(f"floor@65 (2022$) = ${out['floor'][65]:,.0f}   "
          f"k3_reinvested@65 (2022$) = ${out['k3'][65]:,.0f}")
    print(f"endpoint matches engine: ${out['engine_floor_2025']:,.0f} (2025$)")
    path = os.path.join(os.path.dirname(__file__), "..", "results", "floor_by_age.json")
    json.dump(out, open(path, "w"))
    print("wrote", path)
