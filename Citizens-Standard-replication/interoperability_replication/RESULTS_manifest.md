# Paper 7 — Results Manifest (claim → script → output)

Every quantitative claim in the paper maps to a script here and a line of its captured
output in `outputs/`. Reproduce all with `python run_all.py` (deterministic; seeds fixed
in the stochastic scripts). Environment in `requirements.txt`.

## Domestic engine (computed on the published CS specification, launch calibration)
| Paper claim | Value | Script | Output |
|---|---|---|---|
| K1 per new citizen | $2,250 | cs_engine.py | cs_engine.out.txt (A) |
| K1 aggregate | $9.0B | cs_engine.py | (A) |
| Growth-matched line (g_r·M2) | $447B | cs_engine.py | (A) |
| K2 (Mode B) | $438B | cs_engine.py | (A) |
| KI (Mode C launch) | $816B | cs_engine.py | (A) |
| Citizen dividend K3, flat across regimes | $219B | cs_engine.py | (B); fig_A1_dividend.png |
| Bundled dividend (0% / +2% / +3%) | $0 / $447B / $671B | cs_engine.py | (B); fig_A1 |

## External layer (EQUA exact formula; calibrated mechanism result)
| Paper claim (§7 result) | Value | Script | Output |
|---|---|---|---|
| 1 Real-neutral layer | real rate = 1.000000 | equa_redteam.py | equa_redteam.out.txt |
| 2 Full indexation: level irrelevant | identical paths | equa_model_v3.py | equa_model_v3.out.txt |
| 3 Heterogeneous-level distortion | −3.9 / −11.2 / −18.0% (−37.6% bound) | equa_model_v3.py | (1) |
| 4 Common level + heterogeneous stickiness | 0% / −2.9% / −8.5% | equa_model_v3.py | (2) |
| 5 Cost of positive anchor | +226 / +388 / +632% vs 0/−1/−2%; zero +0/+49/+124% | equa_model_v3.py | (3); fig_A3_cost.png |
| 6 Variance of the differential | 0.28 / 2.79 / 0.56 %/yr | equa_model_v3.py | (4) |
| 7 Zero-robustness across wage processes | lag −8.5%, partial −7.6%, Calvo +5.4% (−5.2% flipped); common 0 ~0 | equa_stress.py | equa_stress.out.txt (S3); fig_A2 |
| Interoperation reproduced inside engine | corridor −5.7%, zero clean | cs_channel_test.py | cs_channel_test.out.txt (Test 3) |

## Domestic feasibility, independence, contraction, onboarding
| Paper claim | Value | Script | Output |
|---|---|---|---|
| Asymmetric independence (Break A real; B,C reinforce zero) | — | cs_independence_redteam.py | cs_independence_redteam.out.txt |
| Bond sterilization stock at 40y (r<g/r=g/r>g) | 56% / 80% / 119% of GDP | cs_contraction_compare.py | cs_contraction_compare.out.txt; fig_A4 |
| Surcharge: no stock, ~2% GDP bounded drag | 0% stock | cs_contraction_compare.py | same |
| Transient shock absorbed; persistent buys finite runway | — | cs_sterilization_test.py | cs_sterilization_test.out.txt |
| Onboarding convergence (yr0 19% → yr12 ~0) | 19/11.6/1.7/0.04% | cs_channel_test.py | (Test 4) |
| Idle-capital incidence: inflation regressive, targeted progressive | saver 2.1% vs rentier 0.3% (infl); 0.6% vs 1.5% (targeted) | behavioral_idle_capital.py | behavioral_idle_capital.out.txt |

## Verification note
- The uploaded equa_stress.py originally omitted the Calvo block; it is restored here and
  reproduces the +5.4% (and −5.2% under the flipped stickiness assignment). The paper states
  the sign tracks which member is stickier, not the wage process — see equa_stress.out.txt (S3).
