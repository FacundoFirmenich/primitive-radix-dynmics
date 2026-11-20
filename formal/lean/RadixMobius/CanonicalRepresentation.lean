import RadixMobius.Realization
import RadixMobius.CycleBudget

namespace RadixMobius
open scoped BigOperators

def canonicalPair (x : ℚ) : FractionPair := ⟨x.num.natAbs, x.den⟩

theorem primitive_value_mk (x : FractionPair) (hq : x.q ≠ 0) (hp : PairPrimitive x) :
    value x = Rat.mk' (x.p : ℤ) x.q hq (by simpa using hp) := by
  rw [Rat.mk'_eq_divInt, Rat.divInt_eq_div]
  simp [value]

theorem primitive_value_num (x : FractionPair) (hq : x.q ≠ 0) (hp : PairPrimitive x) :
    (value x).num = (x.p : ℤ) := by rw [primitive_value_mk x hq hp]

theorem primitive_value_den (x : FractionPair) (hq : x.q ≠ 0) (hp : PairPrimitive x) :
    (value x).den = x.q := by rw [primitive_value_mk x hq hp]

theorem canonical_primitive (x : ℚ) : PairPrimitive (canonicalPair x) := x.reduced

theorem canonical_value (x : ℚ) (hx : 0 ≤ x) : value (canonicalPair x) = x := by
  have hn : ((x.num.natAbs : ℕ) : ℤ) = x.num := by
    rw [Int.natCast_natAbs, abs_of_nonneg (Rat.num_nonneg.mpr hx)]
  have hnq : ((x.num.natAbs : ℕ) : ℚ) = (x.num : ℚ) := by
    have h := congrArg (fun z : ℤ => (z : ℚ)) hn
    simpa only [Int.cast_natCast] using h
  change (x.num.natAbs : ℚ) / x.den = x
  rw [hnq, Rat.num_div_den]

theorem canonical_inverse (x : FractionPair) (hq : x.q ≠ 0) (hp : PairPrimitive x) :
    canonicalPair (value x) = x := by
  unfold canonicalPair
  rw [primitive_value_num x hq hp, primitive_value_den x hq hp]
  simp only [Int.natAbs_natCast]

theorem pairHigh_of_value (x : FractionPair) (hq : 0 < x.q) (hx : High (value x)) :
    PairHigh x := by
  have hqQ : 0 < (x.q : ℚ) := by exact_mod_cast hq
  have hpQ : 0 < (x.p : ℚ) := by
    have h := (lt_div_iff₀ hqQ).mp (high_pos hx)
    simpa [value] using h
  have hltQ : (x.p : ℚ) < x.q := by
    have h := (div_lt_iff₀ hqQ).mp hx.2
    simpa [value] using h
  have htwQ : (x.q : ℚ) < 2*x.p := by
    have h := (lt_div_iff₀ hqQ).mp hx.1
    linarith
  exact ⟨by exact_mod_cast hpQ, by exact_mod_cast hltQ, by exact_mod_cast htwQ⟩

theorem canonical_high (x : ℚ) (hx : High x) : PairHigh (canonicalPair x) := by
  apply pairHigh_of_value _ x.den_pos
  rw [canonical_value x (le_of_lt (high_pos hx))]
  exact hx

theorem every_high_rational_has_primitive_coordinates (x : ℚ) (hx : High x) :
    ∃ p : FractionPair, PairHigh p ∧ PairPrimitive p ∧ value p = x := by
  exact ⟨canonicalPair x, canonical_high x hx, canonical_primitive x,
    canonical_value x (le_of_lt (high_pos hx))⟩

theorem reduced_pair_primitive (p q : ℕ) (hq : 0 < q) :
    PairPrimitive (reducePair p q) :=
  Nat.coprime_div_gcd_div_gcd (Nat.gcd_pos_of_pos_right p hq)

theorem reduced_pair_den_pos (p q : ℕ) (hq : 0 < q) : 0 < (reducePair p q).q := by
  change 0 < q / Nat.gcd p q
  exact Nat.div_pos (Nat.gcd_le_right q hq) (Nat.gcd_pos_of_pos_right p hq)

theorem canonical_radix (B : ℕ) (x : ℚ) (hx : 0 ≤ x) :
    canonicalPair (radix B x) = pairT B (canonicalPair x) := by
  have hv : value (pairT B (canonicalPair x)) = radix B x := by
    rw [pairT_value _ _ x.den_pos, canonical_value x hx]
  rw [← hv]
  exact canonical_inverse _ (ne_of_gt (reduced_pair_den_pos _ _ x.den_pos))
    (reduced_pair_primitive _ _ x.den_pos)

theorem canonical_mobius (B : ℕ) (x : ℚ) (hx : High x) :
    canonicalPair (mobius B x) = pairS B (canonicalPair x) := by
  have hh := canonical_high x hx
  have hv : value (pairS B (canonicalPair x)) = mobius B x := by
    rw [pairS_value _ _ hh.1 (le_of_lt hh.2.1), canonical_value x (le_of_lt (high_pos hx))]
  have hd : 0 < (canonicalPair x).p + (B*((canonicalPair x).q-(canonicalPair x).p))%(canonicalPair x).p := by omega
  rw [← hv]
  exact canonical_inverse _ (ne_of_gt (reduced_pair_den_pos _ _ hd))
    (reduced_pair_primitive _ _ hd)

theorem canonical_step (B : ℕ) (a : Letter) (x : ℚ) (hx : High x) :
    canonicalPair (rationalStep B a x) = pairStep B a (canonicalPair x) := by
  cases a with
  | T => exact canonical_radix B x (le_of_lt (high_pos hx))
  | S => exact canonical_mobius B x hx

theorem canonical_trajectory (B n : ℕ) (x : ℕ → ℚ) (a : ℕ → Letter)
    (hh : ∀ i ≤ n, High (x i))
    (he : ∀ i < n, x (i+1)=rationalStep B (a i) (x i)) :
    ∀ i < n, canonicalPair (x (i+1)) = pairStep B (a i) (canonicalPair (x i)) := by
  intro i hi
  rw [he i hi]
  exact canonical_step B (a i) (x i) (hh i (by omega))

theorem rational_cycle_balance (B n : ℕ) (x : ℕ → ℚ) (a : ℕ → Letter)
    (hh : ∀ i ≤ n, High (x i))
    (he : ∀ i < n, x (i+1)=rationalStep B (a i) (x i)) (hc : x n=x 0) :
    cycleReduction B n (fun i => canonicalPair (x i)) a =
      (∏ i ∈ Finset.range n, if a i = .T then x (i+1)/x i else 1) ∧
    cycleReduction B n (fun i => canonicalPair (x i)) a =
      (∏ i ∈ Finset.range n, if a i = .S then x i/x (i+1) else 1) := by
  have hpair := canonical_trajectory B n x a hh he
  have hv : ∀ i ≤ n, value (canonicalPair (x i)) = x i := by
    intro i hi
    exact canonical_value _ (le_of_lt (high_pos (hh i hi)))
  have hb := actual_cycle_balance B n (fun i => canonicalPair (x i)) a
    (fun i hi => canonical_high _ (hh i hi)) (fun i hi => canonical_primitive _)
    hpair (congrArg canonicalPair hc)
  constructor
  · rw [show cycleReduction B n (fun i => canonicalPair (x i)) a = _ from hb.1]
    apply Finset.prod_congr rfl
    intro i hi
    have hin := Finset.mem_range.mp hi
    rw [hv i (by omega), hv (i+1) (by omega)]
  · rw [show cycleReduction B n (fun i => canonicalPair (x i)) a = _ from hb.2]
    apply Finset.prod_congr rfl
    intro i hi
    have hin := Finset.mem_range.mp hi
    rw [hv i (by omega), hv (i+1) (by omega)]

theorem rational_no_strict_short_cycle (B n : ℕ) (x : ℕ → ℚ) (a : ℕ → Letter)
    (hn : n ≤ 3) (hh : ∀ i ≤ n, High (x i))
    (he : ∀ i < n, x (i+1)=rationalStep B (a i) (x i)) (hc : x n=x 0) :
    ¬ (∃ i < n, 1 < defect B (a i) (canonicalPair (x i))) := by
  exact no_strict_cycle_length_le_three B n (fun i => canonicalPair (x i)) a hn
    (fun i hi => canonical_high _ (hh i hi)) (fun i _ => canonical_primitive _)
    (canonical_trajectory B n x a hh he) (congrArg canonicalPair hc)

theorem rational_cycle_letter_budget (B n : ℕ) (x : ℕ → ℚ) (a : ℕ → Letter)
    (hh : ∀ i ≤ n, High (x i))
    (he : ∀ i < n, x (i+1)=rationalStep B (a i) (x i)) (hc : x n=x 0)
    (hr : 1 < cycleReduction B n (fun i => canonicalPair (x i)) a) :
    cycleReduction B n (fun i => canonicalPair (x i)) a <
      (2 : ℚ)^min (TIndices n a).card (SIndices n a).card := by
  exact actual_cycle_letter_budget B n (fun i => canonicalPair (x i)) a
    (fun i hi => canonical_high _ (hh i hi)) (fun i _ => canonical_primitive _)
    (canonical_trajectory B n x a hh he) (congrArg canonicalPair hc) hr

end RadixMobius
