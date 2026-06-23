"""
build_csv.py
=============
Generate the corrected CSV files used for replication:
  citizens_standard_historical_data_1960_2025_v2.csv  — main paper dataset
  citizens_standard_historical_data_1928_2025_full.csv — extended for MC

Both files are built from the same authoritative_data.py source.
"""

from authoritative_data import (
    CPI_DECDEC, CPI_ANNUAL, SP500_NOMINAL, GDP_NOMINAL_B,
    REAL_GDP_GROWTH, M2_BILLIONS, POPULATION_M, real_sp500_return,
)


def write_csv(path, start_year, end_year):
    with open(path, "w") as f:
        f.write("year,m2_billions_usd,gdp_nominal_billions_usd,"
                "real_gdp_growth_pct,population_millions,"
                "cpi_u_index_1982_84_eq_100,cpi_decdec_pct,"
                "sp500_nominal_total_return_pct,sp500_real_total_return_pct\n")
        for y in range(start_year, end_year + 1):
            # 1928 has no real GDP growth (need 1927 GDP); skip it.
            if y not in REAL_GDP_GROWTH and y == 1928:
                continue
            sp_real = real_sp500_return(y) * 100  # to percent
            f.write(
                f"{y},"
                f"{M2_BILLIONS[y]:.1f},"
                f"{GDP_NOMINAL_B[y]:.1f},"
                f"{REAL_GDP_GROWTH.get(y, 0.0):.1f},"
                f"{POPULATION_M[y]:.1f},"
                f"{CPI_ANNUAL[y]:.3f},"
                f"{CPI_DECDEC[y]:.2f},"
                f"{SP500_NOMINAL[y]:.2f},"
                f"{sp_real:.4f}\n"
            )
    print(f"  wrote {path}  ({end_year - start_year + 1} rows)")


if __name__ == "__main__":
    write_csv("citizens_standard_historical_data_1960_2025_v2.csv", 1960, 2025)
    write_csv("citizens_standard_historical_data_1928_2025_full.csv", 1929, 2025)
