import RadixMobius.CycleBalance
import RadixMobius.FractionBridge

namespace RadixMobius
open scoped BigOperators

def pairStep (B : ℕ) (a : Letter) : FractionPair → FractionPair :=
  match a with | .T => pairT B | .S => pairS B

def defect (B : ℕ) (a : Letter) (x : FractionPair) : ℕ :=
  match a with | .T => Nat.gcd B x.q | .S => Nat.gcd B x.p

theorem pairT_den_conservation (B : ℕ) (x : FractionPair) (hx : PairPrimitive x) :
    x.q = Nat.gcd B x.q * (pairT B x).q := by
  rw [pairT_denominator B x hx, Nat.mul_comm]
  exact (Nat.div_mul_cancel (Nat.gcd_dvd_right B x.q)).symm

theorem pairS_num_conservation (B : ℕ) (x : FractionPair)
    (hpq : x.p ≤ x.q) (hx : PairPrimitive x) :
    x.p = Nat.gcd B x.p * (pairS B x).p := by
  rw [pairS_numerator B x hpq hx, Nat.mul_comm]
  exact (Nat.div_mul_cancel (Nat.gcd_dvd_right B x.p)).symm

theorem actual_step_conservation (B : ℕ) (a : Letter) (x : FractionPair)
    (hh : PairHigh x) (hx : PairPrimitive x) :
    match a with
    | .T => x.q = defect B a x * (pairStep B a x).q
    | .S => x.p = defect B a x * (pairStep B a x).p := by
  cases a with
  | T => exact pairT_den_conservation B x hx
  | S => exact pairS_num_conservation B x (le_of_lt hh.2.1) hx

theorem actual_cycle_balance (B n : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter)
    (hh : ∀ i ≤ n, PairHigh (x i))
    (hp : ∀ i < n, PairPrimitive (x i))
    (he : ∀ i < n, x (i+1) = pairStep B (a i) (x i)) (hc : x n = x 0) :
    (∏ i ∈ Finset.range n, (defect B (a i) (x i) : ℚ)) =
      (∏ i ∈ Finset.range n, if a i = .T then value (x (i+1))/value (x i) else 1) ∧
    (∏ i ∈ Finset.range n, (defect B (a i) (x i) : ℚ)) =
      (∏ i ∈ Finset.range n, if a i = .S then value (x i)/value (x (i+1)) else 1) := by
  let p : ℕ → ℚ := fun i => (x i).p
  let q : ℕ → ℚ := fun i => (x i).q
  let d : ℕ → ℚ := fun i => defect B (a i) (x i)
  have hp0 : ∀ i ≤ n, p i ≠ 0 := by
    intro i hi
    change ((x i).p : ℚ) ≠ 0
    exact_mod_cast (ne_of_gt (hh i hi).1)
  have hq0 : ∀ i ≤ n, q i ≠ 0 := by
    intro i hi
    change ((x i).q : ℚ) ≠ 0
    exact_mod_cast (ne_of_gt (lt_trans (hh i hi).1 (hh i hi).2.1))
  have hed : ∀ i < n, match a i with
      | .T => q i = d i*q (i+1)
      | .S => p i = d i*p (i+1) := by
    intro i hi
    have h := actual_step_conservation B (a i) (x i) (hh i (by omega)) (hp i hi)
    rw [← he i hi] at h
    cases ha : a i with
    | T =>
      rw [ha] at h
      simpa [ha, p, q, d] using congrArg (fun k : ℕ => (k : ℚ)) h
    | S =>
      rw [ha] at h
      simpa [ha, p, q, d] using congrArg (fun k : ℕ => (k : ℚ)) h
  have hpn : p n = p 0 := congrArg (fun y : FractionPair => (y.p : ℚ)) hc
  have hqn : q n = q 0 := congrArg (fun y : FractionPair => (y.q : ℚ)) hc
  simpa only [p, q, d, value] using cycle_balance n p q d a hp0 hq0 hed hpn hqn

end RadixMobius
