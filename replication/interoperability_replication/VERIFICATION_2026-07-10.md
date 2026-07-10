# Independent Verification of the EQUA Replication (2026-07-10)

The Paper 7 external-layer scripts were re-run independently and reproduce every headline number.

| Claim | Published | Re-run | Status |
|---|---|---|---|
| Common +2% anchor → real-rate wedge | −5.8% | −5.8% | ✓ |
| Common +3%, three wage models | −8.5 / −7.6 / +5.4% | −8.49 / −7.60 / +5.42% | ✓ |
| Common zero, all three wage models | ~0 | ~0.0% | ✓ |
| Heterogeneous levels (lag k=1..5) | −3.9 to −18.0% (constant) | reproduced | ✓ |

The result is a **mechanism property** (algebra of the settlement formula), not an empirical
forecast — the package's own framing. The red-team script is genuinely adversarial: it attacks
the paper's own claims and documents where they were corrected (the "−38%" was a
never-catch-up artifact; the "8×" was baseline-specific). Verified as reproducing.

Scope reminder: EQUA is the **CS-to-CS** settlement layer (an add-on, Serra's mechanism class,
proposed/untested-in-world). It does NOT bear on CS-to-non-CS FX, which is an ordinary float
(see the separate FX exploratory record — null result).
