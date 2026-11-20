import RadixMobius.FractionBridge
import Mathlib.Data.Finset.Image
import Mathlib.Tactic.FinCases

namespace RadixMobius

def rationalStep (B : ℕ) (a : Letter) : ℚ → ℚ :=
  match a with | .T => radix B | .S => mobius B

def runRational (B : ℕ) : List Letter → ℚ → ℚ
  | [], x => x
  | a::w, x => runRational B w (rationalStep B a x)

def HighComponent (B : ℕ) (F : Finset ℚ) : Prop :=
  2 ≤ B ∧ (∀ x ∈ F, High x) ∧
  (∀ x ∈ F, radix B x ∈ F ∧ mobius B x ∈ F) ∧
  (∀ x ∈ F, ∀ y ∈ F, ∃ w : List Letter, runRational B w x = y)

theorem runRational_intertwines (B : ℕ) (x : Fin 5 → ℚ)
    (hT : ∀ i, radix B (x i) = x (graphT i))
    (hS : ∀ i, mobius B (x i) = x (graphS i))
    (w : List Letter) (i : Fin 5) :
    runRational B w (x i) = x (runGraph w i) := by
  induction w generalizing i with
  | nil => rfl
  | cons a w ih =>
    cases a with
    | T => simpa [runRational, rationalStep, runGraph, graphStep, hT] using ih (graphT i)
    | S => simpa [runRational, rationalStep, runGraph, graphStep, hS] using ih (graphS i)

theorem realization_from_graph (B : ℕ) (x : Fin 5 → ℚ) (hB : 2 ≤ B)
    (hh : ∀ i, High (x i)) (hinj : Function.Injective x)
    (hT : ∀ i, radix B (x i) = x (graphT i))
    (hS : ∀ i, mobius B (x i) = x (graphS i)) :
    ∃ F : Finset ℚ, HighComponent B F ∧ F.card = 5 ∧
      ¬ Set.InjOn (mobius B) (F : Set ℚ) := by
  classical
  let F := Finset.univ.image x
  have hm (i : Fin 5) : x i ∈ F := Finset.mem_image.mpr ⟨i, Finset.mem_univ i, rfl⟩
  refine ⟨F, ?_, ?_, ?_⟩
  · refine ⟨hB, ?_, ?_, ?_⟩
    · intro z hz
      obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hz
      exact hh i
    · intro z hz
      obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hz
      exact ⟨by rw [hT]; exact hm (graphT i), by rw [hS]; exact hm (graphS i)⟩
    · intro z hz y hy
      obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hz
      obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hy
      obtain ⟨w, hw⟩ := graph_strongly_connected i j
      exact ⟨w, by rw [runRational_intertwines B x hT hS, hw]⟩
  · simpa [F] using Finset.card_image_of_injective Finset.univ hinj
  · intro h
    have he : mobius B (x 3) = mobius B (x 4) := by rw [hS, hS]; rfl
    have h34 := hinj (h (hm 3) (hm 4) he)
    exact (by decide : (3 : Fin 5) ≠ 4) h34

theorem pairT_periodic (B t M : ℕ) (x : FractionPair) (hM : x.q ∣ M) :
    pairT (B+t*M) x = pairT B x := by
  have hdiv : x.q ∣ t*M*x.p := dvd_mul_of_dvd_left (dvd_mul_of_dvd_right hM t) x.p
  simp only [pairT, Nat.add_mul, Nat.add_mod, Nat.mod_eq_zero_of_dvd hdiv, Nat.add_zero, Nat.mod_mod]

theorem pairS_periodic (B t M : ℕ) (x : FractionPair) (hM : x.p ∣ M) :
    pairS (B+t*M) x = pairS B x := by
  have hdiv : x.p ∣ t*M*(x.q-x.p) := dvd_mul_of_dvd_left (dvd_mul_of_dvd_right hM t) (x.q-x.p)
  simp only [pairS, Nat.add_mul, Nat.add_mod, Nat.mod_eq_zero_of_dvd hdiv, Nat.add_zero, Nat.mod_mod]

theorem oldCarrier_period_divisibility :
    ∀ i : Fin 5, (oldCarrier i).p ∣ oldPeriod ∧ (oldCarrier i).q ∣ oldPeriod := by decide

theorem newCarrier_period_divisibility :
    ∀ i : Fin 5, (newCarrier i).p ∣ newPeriod ∧ (newCarrier i).q ∣ newPeriod := by decide

theorem oldCarrier_rational_edges (t : ℕ) :
    (∀ i, radix (oldBase+t*oldPeriod) (value (oldCarrier i)) = value (oldCarrier (graphT i))) ∧
    (∀ i, mobius (oldBase+t*oldPeriod) (value (oldCarrier i)) = value (oldCarrier (graphS i))) := by
  constructor
  · intro i
    rw [← pairT_value _ _ (lt_trans (oldCarrier_high i).1 (oldCarrier_high i).2.1),
      pairT_periodic _ _ _ _ (oldCarrier_period_divisibility i).2, oldCarrier_T_edges]
  · intro i
    rw [← pairS_value _ _ (oldCarrier_high i).1 (le_of_lt (oldCarrier_high i).2.1),
      pairS_periodic _ _ _ _ (oldCarrier_period_divisibility i).1, oldCarrier_S_edges]

theorem newCarrier_rational_edges (t : ℕ) :
    (∀ i, radix (newBase+t*newPeriod) (value (newCarrier i)) = value (newCarrier (graphT i))) ∧
    (∀ i, mobius (newBase+t*newPeriod) (value (newCarrier i)) = value (newCarrier (graphS i))) := by
  constructor
  · intro i
    rw [← pairT_value _ _ (lt_trans (newCarrier_high i).1 (newCarrier_high i).2.1),
      pairT_periodic _ _ _ _ (newCarrier_period_divisibility i).2, newCarrier_T_edges]
  · intro i
    rw [← pairS_value _ _ (newCarrier_high i).1 (le_of_lt (newCarrier_high i).2.1),
      pairS_periodic _ _ _ _ (newCarrier_period_divisibility i).1, newCarrier_S_edges]

set_option maxRecDepth 100000 in
theorem oldCarrier_values_injective : Function.Injective (fun i => value (oldCarrier i)) := by
  intro i j h
  fin_cases i <;> fin_cases j <;> norm_num [value, oldCarrier] at *

set_option maxRecDepth 100000 in
theorem newCarrier_values_injective : Function.Injective (fun i => value (newCarrier i)) := by
  intro i j h
  fin_cases i <;> fin_cases j <;> norm_num [value, newCarrier] at *

theorem oldBase_valid (t : ℕ) : 2 ≤ oldBase+t*oldPeriod := by
  unfold oldBase
  omega

theorem newBase_valid (t : ℕ) : 2 ≤ newBase+t*newPeriod := by
  unfold newBase
  omega

theorem old_infinite_family (t : ℕ) :
    ∃ F : Finset ℚ, HighComponent (oldBase+t*oldPeriod) F ∧ F.card = 5 ∧
      ¬ Set.InjOn (mobius (oldBase+t*oldPeriod)) (F : Set ℚ) := by
  exact realization_from_graph _ (fun i => value (oldCarrier i)) (oldBase_valid t)
    (fun i => pairHigh_value (oldCarrier_high i)) oldCarrier_values_injective
    (oldCarrier_rational_edges t).1 (oldCarrier_rational_edges t).2

theorem new_infinite_family (t : ℕ) :
    ∃ F : Finset ℚ, HighComponent (newBase+t*newPeriod) F ∧ F.card = 5 ∧
      ¬ Set.InjOn (mobius (newBase+t*newPeriod)) (F : Set ℚ) := by
  exact realization_from_graph _ (fun i => value (newCarrier i)) (newBase_valid t)
    (fun i => pairHigh_value (newCarrier_high i)) newCarrier_values_injective
    (newCarrier_rational_edges t).1 (newCarrier_rational_edges t).2

end RadixMobius
