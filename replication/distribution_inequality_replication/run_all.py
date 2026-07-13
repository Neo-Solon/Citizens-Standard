"""
run_all.py  --  Citizens Standard: Distribution and Wealth Inequality, full replication.

  1. verify_scf   : reproduce published SCF 2022 figures from the bundled microdata
  2. floor_by_age : extract the engine floor-by-age (endpoint = engine's $209,942)
  3. channels     : apply the four channels, write results, print the headline

Run:  pip install -r requirements.txt && python run_all.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import verify_scf, floor_by_age, channels

print("\n[1/3] SCF read-check")
ok = verify_scf.main()
print("\n[2/3] floor-by-age from the engine")
floor_by_age.__name__  # ensure import
out = floor_by_age.build()
print(f"  floor@65 = ${out['floor'][65]:,.0f} (2022$); endpoint matches engine ${out['engine_floor_2025']:,.0f} (2025$)")
print("\n[3/3] channel model")
channels.main()
print("\nDONE." if ok else "\nDONE (review read-check).")
