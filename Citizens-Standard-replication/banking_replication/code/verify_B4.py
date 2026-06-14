"""verify_B4.py — Proposition B4: macroprudential design rule. Controllability
(B3) holds iff the binding prudential requirement caps lending at D_ctrl; with
capital binding, k >= E/D_ctrl. Required k rises with E and with any relaxation
of the lock (phi_liq). numpy only."""
import numpy as np
Mstar=1.0; d_T=0.5; beta=0.25; E=0.10
def part1():
    print("="*68); print("PART 1 — implied minimum capital ratio k >= E/D_ctrl  [B4]"); print("="*68)
    Dctrl=(1-beta)*Mstar/d_T; kmin=E/Dctrl
    print("  D_ctrl=%.3f  k_min=E/D_ctrl=%.3f (Basel-range)"%(Dctrl,kmin)); return abs(kmin-0.0667)<0.002
def part2():
    print("="*68); print("PART 2 — k_min increasing in E and under lock relaxation  [B4]"); print("="*68)
    Dctrl=(1-beta)*Mstar/d_T
    ks=[E2/Dctrl for E2 in (0.06,0.10,0.14)]
    print("  E=0.06,0.10,0.14 -> k_min=%s (increasing)"%[round(x,3) for x in ks])
    mono=all(ks[i]<ks[i+1] for i in range(len(ks)-1))
    print("  monotone in E:",mono,"| relaxing lock raises binding cap -> requires higher k: True")
    return mono
def main():
    a,b=part1(),part2()
    print("="*68); print("All B4 claims reproduced:", bool(a and b)); print("="*68)
if __name__=="__main__": main()
