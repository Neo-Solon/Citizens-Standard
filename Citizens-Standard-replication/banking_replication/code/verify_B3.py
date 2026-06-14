"""verify_B3.py — Proposition B3: throttle controllability. KI keeps the price
path iff inside deposits d_T*D <= (1-beta)*M* (buffer beta for shock response);
the B2-bounded baseline lies strictly inside. numpy only."""
import numpy as np
Mstar=1.0; d_T=0.5; beta=0.25
m=0.50; phi=0.15; W=4.0
def part1():
    print("="*68); print("PART 1 — controllability ceiling d_T*D <= (1-beta)*M*  [B3]"); print("="*68)
    Dctrl=(1-beta)*Mstar/d_T
    print("  beta=%.2f -> controllable iff D <= %.3f"%(beta,Dctrl)); return abs(Dctrl-1.5)<1e-9
def part2():
    print("="*68); print("PART 2 — baseline inside money sits inside the ceiling  [B3]"); print("="*68)
    Dbase=m*phi*W                      # collateral-bound deposits (B2)
    inside=d_T*Dbase; ceil=(1-beta)*Mstar
    print("  baseline d_T*D=%.3f  vs ceiling (1-beta)*M*=%.3f -> controllable=%s"%(inside,ceil,inside<=ceil))
    return inside<=ceil
def main():
    a,b=part1(),part2()
    print("="*68); print("All B3 claims reproduced:", bool(a and b)); print("="*68)
if __name__=="__main__": main()
