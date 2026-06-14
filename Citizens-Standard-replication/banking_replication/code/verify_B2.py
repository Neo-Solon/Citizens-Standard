"""verify_B2.py — Proposition B2: inside money is bounded by min(capital,reserves,
collateral); locked floors are non-pledgeable so collateral binds at the baseline
(sigma~0.13). Removing the lock enlarges the collateral BASE ~1/phi (~7x); a
prudential cap then binds at a far higher realized share (~0.375). numpy only."""
import numpy as np
k=0.08; rho=0.10; m=0.50; phi=0.15; E=0.10; Rb=0.12; W=4.0; d_T=0.5; Mo=1.0
def caps(phi_liq): return dict(capital=E/k, reserves=Rb/rho, collateral=m*phi_liq*W)
def share(L): return d_T*L/(Mo+d_T*L)
def part1():
    print("="*68); print("PART 1 — collateral binds because floors are non-pledgeable  [B2]"); print("="*68)
    c=caps(phi); Lmax=min(c.values()); binding=min(c,key=c.get)
    for kk,vv in c.items(): print("  %-11s = %.3f"%(kk,vv))
    print("  L_max=%.3f binding=%s ; sigma=%.3f"%(Lmax,binding,share(Lmax)))
    return binding=="collateral" and abs(Lmax-0.30)<1e-9 and abs(share(Lmax)-0.13)<0.005
def part2():
    print("="*68); print("PART 2 — the lock shrinks the collateral BASE ~1/phi (~7x)  [B2]"); print("="*68)
    base_lock=m*phi*W; base_nolock=m*1.0*W
    print("  collateral base: locked=%.2f  unlocked=%.2f  ratio=%.1fx (=1/phi)"%(base_lock,base_nolock,base_nolock/base_lock))
    return abs(base_nolock/base_lock-1/phi)<1e-6
def part3():
    print("="*68); print("PART 3 — removing the lock: a prudential cap binds, share ~3x  [B2]"); print("="*68)
    c=caps(1.0); Ln=min(c.values()); binding=min(c,key=c.get)
    print("  unlocked caps: %s -> binding=%s at L=%.2f, sigma=%.3f"%({x:round(v,2) for x,v in c.items()},binding,Ln,share(Ln)))
    print("  realized share ratio no-lock/lock = %.1fx"%(share(Ln)/share(0.30)))
    return binding!="collateral" and share(Ln)>0.3 and (share(Ln)/share(0.30))>2
def main():
    a,b,c=part1(),part2(),part3()
    print("="*68); print("All B2 claims reproduced:", bool(a and b and c)); print("="*68)
if __name__=="__main__": main()
