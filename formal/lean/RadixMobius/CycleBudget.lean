import RadixMobius.ActualCycles

namespace RadixMobius
open scoped BigOperators

def TIndices (n : ℕ) (a : ℕ → Letter) : Finset ℕ :=
  (Finset.range n).filter (fun i => a i = .T)
def SIndices (n : ℕ) (a : ℕ → Letter) : Finset ℕ :=
  (Finset.range n).filter (fun i => a i = .S)

def cycleReduction (B n : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter) : ℚ :=
  ∏ i ∈ Finset.range n, (defect B (a i) (x i) : ℚ)

theorem letter_count_partition (n : ℕ) (a : ℕ → Letter) :
    (TIndices n a).card + (SIndices n a).card = n := by
  have hu : TIndices n a ∪ SIndices n a = Finset.range n := by
    ext i
    cases ha : a i <;> simp [TIndices, SIndices, ha]
  have hd : Disjoint (TIndices n a) (SIndices n a) := by
    apply Finset.disjoint_left.mpr
    intro i ht hs
    have hT := (Finset.mem_filter.mp ht).2
    have hS := (Finset.mem_filter.mp hs).2
    rw [hT] at hS
    cases hS
  simpa [hu] using (Finset.card_union_of_disjoint hd).symm

theorem defect_pos (B : ℕ) (a : Letter) (x : FractionPair) (hh : PairHigh x) :
    0 < defect B a x := by
  cases a with
  | T => exact Nat.gcd_pos_of_pos_right B (lt_trans hh.1 hh.2.1)
  | S => exact Nat.gcd_pos_of_pos_right B hh.1

theorem strict_edge_product (B n : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter)
    (hh : ∀ i < n, PairHigh (x i))
    (hs : ∃ i < n, 1 < defect B (a i) (x i)) : 2 ≤ cycleReduction B n x a := by
  obtain ⟨i, hi, hd⟩ := hs
  have hp : defect B (a i) (x i) ≤ ∏ j ∈ Finset.range n, defect B (a j) (x j) :=
    Finset.single_le_prod' (f := fun j => defect B (a j) (x j))
      (fun j hj => defect_pos B (a j) (x j) (hh j (Finset.mem_range.mp hj)))
      (Finset.mem_range.mpr hi)
  have h2 : 2 ≤ ∏ j ∈ Finset.range n, defect B (a j) (x j) := by omega
  unfold cycleReduction
  exact_mod_cast h2

theorem actual_cycle_T_product (B n : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter)
    (hh : ∀ i ≤ n, PairHigh (x i)) (hp : ∀ i < n, PairPrimitive (x i))
    (he : ∀ i < n, x (i+1) = pairStep B (a i) (x i)) (hc : x n = x 0) :
    cycleReduction B n x a = ∏ i ∈ TIndices n a, value (x (i+1))/value (x i) := by
  simpa only [cycleReduction, TIndices, Finset.prod_filter] using
    (actual_cycle_balance B n x a hh hp he hc).1

theorem actual_cycle_S_product (B n : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter)
    (hh : ∀ i ≤ n, PairHigh (x i)) (hp : ∀ i < n, PairPrimitive (x i))
    (he : ∀ i < n, x (i+1) = pairStep B (a i) (x i)) (hc : x n = x 0) :
    cycleReduction B n x a = ∏ i ∈ SIndices n a, value (x i)/value (x (i+1)) := by
  simpa only [cycleReduction, SIndices, Finset.prod_filter] using
    (actual_cycle_balance B n x a hh hp he hc).2

theorem strict_cycle_mixed (B n : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter)
    (hh : ∀ i ≤ n, PairHigh (x i)) (hp : ∀ i < n, PairPrimitive (x i))
    (he : ∀ i < n, x (i+1) = pairStep B (a i) (x i)) (hc : x n = x 0)
    (hr : 1 < cycleReduction B n x a) :
    (TIndices n a).Nonempty ∧ (SIndices n a).Nonempty := by
  constructor
  · by_contra h
    have hz := Finset.not_nonempty_iff_eq_empty.mp h
    have hb := actual_cycle_T_product B n x a hh hp he hc
    simp [hz] at hb
    linarith
  · by_contra h
    have hz := Finset.not_nonempty_iff_eq_empty.mp h
    have hb := actual_cycle_S_product B n x a hh hp he hc
    simp [hz] at hb
    linarith

theorem actual_cycle_letter_budget (B n : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter)
    (hh : ∀ i ≤ n, PairHigh (x i)) (hp : ∀ i < n, PairPrimitive (x i))
    (he : ∀ i < n, x (i+1) = pairStep B (a i) (x i)) (hc : x n = x 0)
    (hr : 1 < cycleReduction B n x a) :
    cycleReduction B n x a < (2 : ℚ)^min (TIndices n a).card (SIndices n a).card := by
  obtain ⟨hT, hS⟩ := strict_cycle_mixed B n x a hh hp he hc hr
  have ht : cycleReduction B n x a < (2 : ℚ)^(TIndices n a).card := by
    rw [actual_cycle_T_product B n x a hh hp he hc]
    apply selected_ratios_lt_two_power _ _ _ hT
    · intro i hi
      exact pairHigh_value (hh i (by have := Finset.mem_range.mp (Finset.mem_filter.mp hi).1; omega))
    · intro i hi
      exact pairHigh_value (hh (i+1) (by have := Finset.mem_range.mp (Finset.mem_filter.mp hi).1; omega))
  have hs : cycleReduction B n x a < (2 : ℚ)^(SIndices n a).card := by
    rw [actual_cycle_S_product B n x a hh hp he hc]
    apply selected_ratios_lt_two_power _ _ _ hS
    · intro i hi
      exact pairHigh_value (hh (i+1) (by have := Finset.mem_range.mp (Finset.mem_filter.mp hi).1; omega))
    · intro i hi
      exact pairHigh_value (hh i (by have := Finset.mem_range.mp (Finset.mem_filter.mp hi).1; omega))
  rcases le_total (TIndices n a).card (SIndices n a).card with h | h
  · simpa [Nat.min_eq_left h] using ht
  · simpa [Nat.min_eq_right h] using hs

theorem no_strict_cycle_length_le_three (B n : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter)
    (hn : n ≤ 3) (hh : ∀ i ≤ n, PairHigh (x i)) (hp : ∀ i < n, PairPrimitive (x i))
    (he : ∀ i < n, x (i+1) = pairStep B (a i) (x i)) (hc : x n = x 0) :
    ¬ (∃ i < n, 1 < defect B (a i) (x i)) := by
  intro hs
  have hr := strict_edge_product B n x a (fun i hi => hh i (by omega)) hs
  have hb := actual_cycle_letter_budget B n x a hh hp he hc (by linarith)
  have hcount := letter_count_partition n a
  have hm : min (TIndices n a).card (SIndices n a).card ≤ 1 := by omega
  have hpow : (2 : ℚ)^min (TIndices n a).card (SIndices n a).card ≤ 2 := by
    have heq : min (TIndices n a).card (SIndices n a).card = 0 ∨
        min (TIndices n a).card (SIndices n a).card = 1 := by omega
    rcases heq with h | h <;> norm_num [h]
  linarith

theorem one_block_product (B n split : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter)
    (hsplit : split ≤ n)
    (hh : ∀ i ≤ n, PairHigh (x i)) (hp : ∀ i < n, PairPrimitive (x i))
    (he : ∀ i < n, x (i+1) = pairStep B (a i) (x i)) (hc : x n = x 0)
    (hword : ∀ i < n, a i = if i < split then .T else .S) :
    cycleReduction B n x a = value (x split)/value (x 0) := by
  have hinds : TIndices n a = Finset.range split := by
    ext i
    constructor
    · intro hi
      obtain ⟨hin, hT⟩ := Finset.mem_filter.mp hi
      have hin' := Finset.mem_range.mp hin
      rw [hword i hin'] at hT
      by_cases his : i < split
      · exact Finset.mem_range.mpr his
      · simp [his] at hT
    · intro hi
      have his := Finset.mem_range.mp hi
      have hin : i < n := by omega
      exact Finset.mem_filter.mpr ⟨Finset.mem_range.mpr hin, by rw [hword i hin]; simp [his]⟩
  rw [actual_cycle_T_product B n x a hh hp he hc, hinds]
  apply prod_coordinate_ratios (fun i => value (x i)) split
  intro i hi
  exact high_ne_zero (pairHigh_value (hh i (by omega)))

theorem no_strict_one_block_cycle (B n split : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter)
    (hsplit : split ≤ n)
    (hh : ∀ i ≤ n, PairHigh (x i)) (hp : ∀ i < n, PairPrimitive (x i))
    (he : ∀ i < n, x (i+1) = pairStep B (a i) (x i)) (hc : x n = x 0)
    (hword : ∀ i < n, a i = if i < split then .T else .S) :
    ¬ (∃ i < n, 1 < defect B (a i) (x i)) := by
  intro hs
  have hr := strict_edge_product B n x a (fun i hi => hh i (by omega)) hs
  rw [one_block_product B n split x a hsplit hh hp he hc hword] at hr
  have hb := (high_ratio_lt_two (pairHigh_value (hh 0 (by omega)))
    (pairHigh_value (hh split hsplit))).2
  linarith

end RadixMobius
