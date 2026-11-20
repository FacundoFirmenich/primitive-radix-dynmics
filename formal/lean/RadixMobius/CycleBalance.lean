import RadixMobius.Definitions
import RadixMobius.FiniteWitness
import Mathlib.Algebra.Order.BigOperators.Ring.Finset

namespace RadixMobius
open scoped BigOperators

theorem coordinate_num_balance (p q p' q' d : ℚ) (a : Letter)
    (hp : p ≠ 0) (hq' : q' ≠ 0)
    (he : match a with | .T => q = d*q' | .S => p = d*p') :
    d*(p'/p) = if a = .T then (p'/q')/(p/q) else 1 := by
  cases a with
  | T =>
    change q = d*q' at he
    change d*(p'/p) = (p'/q')/(p/q)
    field_simp [hp, hq']
    nlinarith [congrArg (fun z => p'*z) he, congrArg (fun z => p'*p*z) he]
  | S =>
    change p = d*p' at he
    change d*(p'/p) = 1
    rw [← mul_div_assoc, ← he, div_self hp]

theorem coordinate_den_balance (p q p' q' d : ℚ) (a : Letter)
    (hq : q ≠ 0) (hp' : p' ≠ 0)
    (he : match a with | .T => q = d*q' | .S => p = d*p') :
    d*(q'/q) = if a = .S then (p/q)/(p'/q') else 1 := by
  cases a with
  | T =>
    change q = d*q' at he
    change d*(q'/q) = 1
    rw [← mul_div_assoc, ← he, div_self hq]
  | S =>
    change p = d*p' at he
    change d*(q'/q) = (p/q)/(p'/q')
    field_simp [hq, hp']
    nlinarith [congrArg (fun z => q'*z) he, congrArg (fun z => q'*q*z) he]

theorem prod_coordinate_ratios (p : ℕ → ℚ) :
    ∀ n, (∀ i ≤ n, p i ≠ 0) →
      (∏ i ∈ Finset.range n, p (i+1)/p i) = p n / p 0 := by
  intro n
  induction n with
  | zero => intro hp; simp [hp 0 (by omega)]
  | succ n ih =>
    intro hp
    rw [Finset.prod_range_succ, ih (fun i hi => hp i (by omega))]
    field_simp [hp 0 (by omega), hp n (by omega)]
    ring

theorem path_num_balance (n : ℕ) (p q d : ℕ → ℚ) (a : ℕ → Letter)
    (hp : ∀ i ≤ n, p i ≠ 0) (hq : ∀ i ≤ n, q i ≠ 0)
    (he : ∀ i < n, match a i with | .T => q i = d i*q (i+1) | .S => p i = d i*p (i+1)) :
    (∏ i ∈ Finset.range n, d i) * (p n/p 0) =
      ∏ i ∈ Finset.range n, if a i = .T then (p (i+1)/q (i+1))/(p i/q i) else 1 := by
  rw [← prod_coordinate_ratios p n hp, ← Finset.prod_mul_distrib]
  apply Finset.prod_congr rfl
  intro i hi
  have hi' := Finset.mem_range.mp hi
  exact coordinate_num_balance _ _ _ _ _ _ (hp i (by omega))
    (hq (i+1) (by omega)) (he i hi')

theorem path_den_balance (n : ℕ) (p q d : ℕ → ℚ) (a : ℕ → Letter)
    (hp : ∀ i ≤ n, p i ≠ 0) (hq : ∀ i ≤ n, q i ≠ 0)
    (he : ∀ i < n, match a i with | .T => q i = d i*q (i+1) | .S => p i = d i*p (i+1)) :
    (∏ i ∈ Finset.range n, d i) * (q n/q 0) =
      ∏ i ∈ Finset.range n, if a i = .S then (p i/q i)/(p (i+1)/q (i+1)) else 1 := by
  rw [← prod_coordinate_ratios q n hq, ← Finset.prod_mul_distrib]
  apply Finset.prod_congr rfl
  intro i hi
  have hi' := Finset.mem_range.mp hi
  exact coordinate_den_balance _ _ _ _ _ _ (hq i (by omega))
    (hp (i+1) (by omega)) (he i hi')

theorem cycle_balance (n : ℕ) (p q d : ℕ → ℚ) (a : ℕ → Letter)
    (hp : ∀ i ≤ n, p i ≠ 0) (hq : ∀ i ≤ n, q i ≠ 0)
    (he : ∀ i < n, match a i with | .T => q i = d i*q (i+1) | .S => p i = d i*p (i+1))
    (hpn : p n = p 0) (hqn : q n = q 0) :
    (∏ i ∈ Finset.range n, d i) =
      (∏ i ∈ Finset.range n, if a i = .T then (p (i+1)/q (i+1))/(p i/q i) else 1) ∧
    (∏ i ∈ Finset.range n, d i) =
      (∏ i ∈ Finset.range n, if a i = .S then (p i/q i)/(p (i+1)/q (i+1)) else 1) := by
  constructor
  · simpa [hpn, hp 0 (by omega)] using path_num_balance n p q d a hp hq he
  · simpa [hqn, hq 0 (by omega)] using path_den_balance n p q d a hp hq he

theorem high_ratio_lt_two {x y : ℚ} (hx : High x) (hy : High y) :
    0 < y/x ∧ y/x < 2 := by
  constructor
  · exact div_pos (high_pos hy) (high_pos hx)
  · apply (div_lt_iff₀ (high_pos hx)).2
    rcases hx with ⟨hl, _⟩
    rcases hy with ⟨_, hu⟩
    linarith

theorem selected_ratios_lt_two_power (s : Finset ℕ) (x y : ℕ → ℚ)
    (hs : s.Nonempty) (hx : ∀ i ∈ s, High (x i)) (hy : ∀ i ∈ s, High (y i)) :
    (∏ i ∈ s, y i / x i) < (2 : ℚ)^s.card := by
  have h := Finset.prod_lt_prod_of_nonempty
    (fun i hi => (high_ratio_lt_two (hx i hi) (hy i hi)).1)
    (fun i hi => (high_ratio_lt_two (hx i hi) (hy i hi)).2) hs
  simpa using h

end RadixMobius
