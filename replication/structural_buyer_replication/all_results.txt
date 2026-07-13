--- verify_prop1_premium.py ---
A.2 PASSED: premium = A*/phi = 0.9000 (sim 0.9000); stable for theta*phi in (0,2), divergent at 2.5; premium decreasing in phi.
--- verify_prop2_investment.py ---
A.3 PASSED: I*=A*=0.45; float constant; repricing decays at |1-theta*phi|=0.75; sum(repricing)=0.9000=A*/phi; issuance share 0 -> 1.
--- verify_prop3_leak.py ---
A.4 PASSED: leak <= kappa_W*Delta; central kappa_W=0.03 -> 3% leak, 97% re-enters M^A; working range [0.025, 0.05].
--- verify_prop7_mirror_voting.py ---
A.5 PASSED: YES_total = p for all psi (machine precision); outcome = residual outcome at every threshold; FDCA never pivotal.
--- verify_psi_plateau.py ---
Appendix A.6 verification PASSED: psi* = c*dur (both models); base=0.24, high=0.45; conservative under growth.

All Paper 8 verifications passed.
