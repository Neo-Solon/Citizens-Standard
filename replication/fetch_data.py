#!/usr/bin/env python3
"""
Shared data fetcher for --refresh.

Bundled snapshot is the default and always present. This module only runs when the
user passes --refresh AND has a FRED_API_KEY. It re-pulls the REFRESHABLE series and
leaves DISCONTINUED series on their bundled snapshot (they cannot be re-pulled).

The authoritative list of every series, its status, and vintage is data/SOURCES.md.
The machine-readable version is data/sources.json (kept in sync).
"""
import json, os, urllib.request
from pathlib import Path

FRED_CSV = "https://api.stlouisfed.org/fred/series/observations"


def _load_manifest(data_dir):
    j = Path(data_dir) / "sources.json"
    if not j.exists():
        raise FileNotFoundError("data/sources.json missing; cannot know which series are refreshable.")
    return json.loads(j.read_text())


def refresh_all(data_dir, api_key):
    manifest = _load_manifest(data_dir)
    refreshed, skipped = [], []
    for entry in manifest["series"]:
        sid = entry["id"]
        fname = entry["file"]
        if entry.get("status") == "discontinued":
            skipped.append(sid)
            continue
        try:
            url = (f"{FRED_CSV}?series_id={sid}&api_key={api_key}"
                   f"&file_type=json")
            with urllib.request.urlopen(url, timeout=30) as r:
                obs = json.loads(r.read())["observations"]
            lines = ["observation_date," + sid]
            for o in obs:
                if o["value"] not in (".", ""):
                    lines.append(f'{o["date"]},{o["value"]}')
            (Path(data_dir) / fname).write_text("\n".join(lines) + "\n")
            refreshed.append(sid)
        except Exception as e:
            print(f"    [refresh] {sid} failed ({e}); keeping bundled snapshot.")
            skipped.append(sid)
    print(f"    [refresh] updated {len(refreshed)} series; kept snapshot for {len(skipped)} "
          f"(discontinued or failed).")
    if skipped:
        print("    [refresh] snapshot-only:", ", ".join(skipped))
