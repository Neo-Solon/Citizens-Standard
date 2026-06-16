# Paper 8 (Neo-Solon, 2026h) Appendix A.3 — Proposition 2
# In steady state the permanent flow funds real investment, not perpetual repricing.
#   I* = A*  =>  float constant (delta f* = 0)
#   transition repricing R_t = a R_{t-1}, a = 1 - theta*phi (geometric decay)
#   issuance share I_t/A* rises monotonically 0 -> 1
#   total repricing  sum R_t = A*/phi  (the entire premium, once-for-all)
A, phi, theta, Qb = 0.45, 0.5, 0.5, 1.0
a = 1 - theta*phi
Qstar = Qb + A/phi

Q = Qb; R = []; share = []
for _ in range(400):
    I = phi*(Q - Qb)
    r = theta*(A - I)            # = Q_{t+1} - Q_t
    R.append(r)
    share.append((Q - Qb)/(Qstar - Qb))
    Q += r

# I* = A* at the fixed point  ->  constant float
I_ss = phi*(Q - Qb)
assert abs(I_ss - A) < 1e-6, (I_ss, A)
# geometric decay at rate |a|
ratios = [R[t+1]/R[t] for t in range(25) if abs(R[t]) > 1e-9]
assert max(abs(x - a) for x in ratios) < 1e-7
# total repricing equals the whole premium A*/phi
assert abs(sum(R) - A/phi) < 1e-6, (sum(R), A/phi)
# issuance share runs from 0 to 1
assert share[0] < 1e-9 and share[-1] > 0.999

print(f"A.3 PASSED: I*=A*={A}; float constant; repricing decays at |1-theta*phi|={abs(a):.2f}; "
      f"sum(repricing)={sum(R):.4f}=A*/phi; issuance share 0 -> 1.")
