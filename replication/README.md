Citizens Standard Counterfactual

Running the replication

Requirements: Python 3.8+ with numpy and matplotlib.

```bash
# Reproduce all paper tables
python3 run\_all\_tables.py > all\_results.txt

# Regenerate figures
python3 mc\_plots.py

# Export the dataset as CSV
python3 build\_csv.py
```



