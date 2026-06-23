{
  "provenance": {
    "macro_1959_2026.csv": {
      "series": [
        "M2SL",
        "CPIAUCSL",
        "PCEPI"
      ],
      "range": "1959-01-01..2026-04-01",
      "n": 808,
      "md5": "21cc80cf0f70",
      "source": "FRED via US-Macro-Forecast-Hub 2026 target snapshot"
    },
    "m1sl_1959_2019.csv": {
      "series": [
        "M1SL"
      ],
      "range": "1959-01-01..2019-09-01",
      "n": 729,
      "md5": "2b573c071733",
      "source": "FRED-MD current.csv (pre-2020 clean M1)"
    },
    "divisia_dm1.csv": {
      "series": [
        "DM1 (CFS Divisia M1, level index, base 100 @ 1967-01)"
      ],
      "range": "1967-01-01..2026-04-01",
      "n": 712,
      "source": "Center for Financial Stability, AMFM program (Barnett Divisia), Narrow worksheet, user-supplied workbook",
      "note": "user-cost weighted; continuous across the May-2020 M1 redefinition"
    },
    "CURRSL.csv": {
      "series": ["CURRSL (Currency Component of M1, SA, $bn)"],
      "range": "1959-01-01..2026-04-01",
      "n": 808,
      "md5": "6fcb58dd2a92",
      "source": "FRED (Board of Governors, H.6), monthly seasonally-adjusted level",
      "note": "composition tier component (active): currency"
    },
    "DEMDEPSL.csv": {
      "series": ["DEMDEPSL (Demand Deposits, SA, $bn)"],
      "range": "1959-01-01..2026-04-01",
      "n": 808,
      "md5": "049a6956a329",
      "source": "FRED (Board of Governors, H.6), monthly seasonally-adjusted level",
      "note": "composition tier component (active): demand deposits"
    },
    "OCDSL.csv": {
      "series": ["OCDSL (Other Checkable Deposits, SA, $bn)"],
      "range": "1959-01-01..2020-04-01",
      "n": 736,
      "md5": "262e23262dd3",
      "source": "FRED (Board of Governors, H.6), monthly seasonally-adjusted level",
      "note": "composition tier component (active): other-checkable deposits. DISCONTINUED after 2020-04 (H.6 Feb-2021 change stopped separate OCD reporting). Do NOT substitute MDLM, which folds savings into the transactional tier and defeats the test. The composition tier ends here by construction; Divisia carries 2021 onward."
    }
  },
  "constructions": {
    "Mt_composition": "CURRSL + DEMDEPSL + OCDSL (currency + demand + other-checkable), savings held OUT. Built by src/build_mt.py:composition_granular; horserace in src/run_composition_horserace.py. Window 1959-01..2020-04."
  },
  "integrity_checks": {
    "M2_loggrowth_Feb2020_Apr2022_pct": 34.0,
    "CPI_YoY_Jun2022_pct": 9.0,
    "M2SL_last": 22804.5,
    "M2SL_last_date": "2026-04-01"
  }
}