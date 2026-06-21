"""
verify_proposition_8.py
-----------------------
Reproduces Proposition 8 (Section 5.6 / Appendix A.11) of Neo-Solon (2026e):
the welfare-optimal consumer-dividend share. Two-phase household,
  c1 = h + kappa*G ,  c2 = 1 + (1-kappa)*G*(1+r) ,
  W  = ln c1 - chi*h^(1+1/nu)/(1+1/nu) + beta*Omega*ln c2 ,
labor h chosen optimally, floor locked. Retention premium R = beta*Omega*(1+r).
Parts: (i) wealth max at kappa=0; (ii) FOC c2/c1=R and baseline kappa*~0.795;
(iii) kappa* falls in R, wealth-max corner kappa*=0 only for R>~1.21;
(iv) labor distortion second-order (envelope) to machine precision.
numpy only.
"""
import numpy as np
nu=0.5; chi=1.0; G=0.20; r=0.045

def labor(b, wedge=0.0):            # chi*h^(1/nu) = (1-wedge)/(h+b)
    lo,hi=1e-9,5.0
    for _ in range(100):
        h=0.5*(lo+hi)
        if chi*h**(1/nu) < (1.0-wedge)/(h+b): lo=h
        else: hi=h
    return 0.5*(lo+hi)
def c1(k,wedge=0.0): return labor(k*G,wedge)+k*G
def c2(k): return 1.0+(1-k)*G*(1+r)
def W(k,beta,Om,wedge=0.0):
    h=labor(k*G,wedge); return np.log(h+k*G)-chi*h**(1+1/nu)/(1+1/nu)+beta*Om*np.log(c2(k))
def kstar_FOC(beta,Om):
    R=beta*Om*(1+r); k=0.5
    for _ in range(300):
        h=labor(k*G); k=min(1,max(0,(1+G*(1+r)-R*h)/(G*((1+r)+R))))
    return k,R
def kstar_grid(beta,Om,wedge=0.0):
    ks=np.linspace(0,1,40001); return ks[int(np.argmax([W(k,beta,Om,wedge) for k in ks]))]

def part1():
    print("="*70); print("PART 1 — terminal wealth maximised at kappa=0  [Prop 8(i)]"); print("="*70)
    vals=[(k,(1-k)*G*(1+r)) for k in (0.0,0.25,0.5,0.795,1.0)]
    for k,w in vals: print("  kappa=%.3f : retained floor (terminal wealth)=%.4f"%(k,w))
    ok=all(vals[i][1]>vals[i+1][1] for i in range(len(vals)-1))
    print("  strictly decreasing in kappa -> wealth-max at kappa=0:", ok); return ok

def part2():
    print("="*70); print("PART 2 — welfare optimum c2/c1=R, baseline kappa*~0.795  [Prop 8(ii)]"); print("="*70)
    kF,R=kstar_FOC(0.90,1.0); kG=kstar_grid(0.90,1.0)
    print("  baseline beta=0.90, Omega=1, r=4.5%%: R=%.4f"%R)
    print("  kappa*_FOC=%.4f  kappa*_grid=%.4f  c2/c1=%.4f"%(kF,kG,c2(kF)/c1(kF)))
    ok=abs(kF-0.795)<0.01 and abs(kF-kG)<1e-3 and abs(c2(kF)/c1(kF)-R)<1e-3
    print("  [paper: kappa*~0.795, FOC c2/c1=R]:", ok); return ok

def part3():
    print("="*70); print("PART 3 — kappa* decreasing in R; wealth-max corner ~1.21  [Prop 8(iii)]"); print("="*70)
    ks=[]
    for beta in (0.80,0.90,0.96,1.00):
        kF,R=kstar_FOC(beta,1.0); ks.append(kF); print("  beta=%.2f R=%.3f kappa*=%.3f"%(beta,R,kF))
    Rcorner=c2(0)/c1(0)
    print("  wealth-max corner threshold R = c2/c1|_{kappa=0} = %.3f"%Rcorner)
    print("  bequest Omega<1 raises payout: ", end="")
    print(", ".join("Om=%.1f->kappa*=%.2f"%(Om,kstar_FOC(0.95,Om)[0]) for Om in (1.0,0.7,0.4)))
    mono=all(ks[i]>=ks[i+1]-1e-9 for i in range(len(ks)-1))
    print("  monotone-decreasing & corner~1.21:", mono and abs(Rcorner-1.21)<0.02); return mono and abs(Rcorner-1.21)<0.02

def part4():
    print("="*70); print("PART 4 — labor distortion second-order (envelope)  [Prop 8(iv)]"); print("="*70)
    beta,Om=0.90,1.0; k0,_=kstar_FOC(beta,Om); e=1e-6
    dW=(W(k0+e,beta,Om)-W(k0-e,beta,Om))/(2*e)
    foc=c2(k0)/c1(k0)-beta*Om*(1+r)
    h=labor(k0*G); dWdh=(np.log(h+e+k0*G)-np.log(h-e+k0*G))/(2*e)-chi*((h+e)**(1+1/nu)-(h-e)**(1+1/nu))/(2*e*(1+1/nu))
    print("  dW/dkappa at optimum   = %.2e"%dW)
    print("  FOC residual c2/c1 - R = %.2e"%foc)
    print("  dW/dh at hh optimum    = %.2e  (labor term first-order only if !=0)"%dWdh)
    kw=kstar_grid(beta,Om,wedge=0.20)
    print("  with 20%% labor wedge: kappa* shifts %.3f -> %.3f (first-order under a wedge)"%(k0,kw))
    ok=abs(dW)<1e-6 and abs(foc)<1e-9 and abs(dWdh)<1e-6
    print("  envelope (all ~0 without wedge):", ok); return ok

def main():
    a,b,c,d=part1(),part2(),part3(),part4()
    print("="*70); print("All Proposition 8 claims reproduced:", bool(a and b and c and d)); print("="*70)

if __name__=="__main__": main()
