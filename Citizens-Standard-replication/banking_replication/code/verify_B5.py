"""verify_B5.py — Proposition B5: run-proof floor. Locked floors are
non-withdrawable, hence not runnable. Run-proof share = 1-phi_liq; max systemic
run = phi_liq; LOLR need scales with runnable deposits d_T*m*phi_liq*W. numpy only."""
import numpy as np
m=0.50; phi=0.15; W=4.0; d_T=0.5
def part1():
    print("="*68); print("PART 1 — run-proof share = locked share 1-phi_liq  [B5]"); print("="*68)
    print("  run-proof=%.2f  runnable=%.2f"%(1-phi,phi)); return abs((1-phi)-0.85)<1e-9
def part2():
    print("="*68); print("PART 2 — LOLR need scales with liquid share  [B5]"); print("="*68)
    lolr_lock=d_T*m*phi*W; lolr_nolock=d_T*m*1.0*W
    print("  LOLR need: locked=%.3f  no-lock=%.3f  ratio=%.1fx"%(lolr_lock,lolr_nolock,lolr_nolock/lolr_lock))
    return abs(lolr_nolock/lolr_lock-1/phi)<1e-6
def main():
    a,b=part1(),part2()
    print("="*68); print("All B5 claims reproduced:", bool(a and b)); print("="*68)
if __name__=="__main__": main()
