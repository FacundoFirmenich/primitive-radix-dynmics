import RadixMobius.ActualCycles
import RadixMobius.MatrixCocycle
import RadixMobius.CycleBudget
import Mathlib.Tactic.FinCases

namespace RadixMobius

def integerLift (x : FractionPair) : Fin 2 → ℤ := ![(x.p : ℤ), (x.q : ℤ)]

def actualMatrix (B : ℕ) (a : Letter) (x : FractionPair) : Mat2 :=
  match a with
  | .T => branchT (B : ℤ) ((B*x.p/x.q : ℕ) : ℤ)
  | .S => branchS (B : ℤ) ((B*(x.q-x.p)/x.p : ℕ) : ℤ)

theorem pairT_num_conservation (B : ℕ) (x : FractionPair) (hx : PairPrimitive x) :
    (B*x.p)%x.q = Nat.gcd B x.q * (pairT B x).p := by
  unfold pairT reducePair
  rw [radix_gcd B x.p x.q hx]
  have hd : Nat.gcd B x.q ∣ (B*x.p)%x.q := by
    rw [← radix_gcd B x.p x.q hx]
    exact Nat.gcd_dvd_left _ _
  simpa [Nat.mul_comm] using (Nat.div_mul_cancel hd).symm

theorem pairS_den_conservation (B : ℕ) (x : FractionPair) (hpq : x.p ≤ x.q)
    (hx : PairPrimitive x) :
    x.p+(B*(x.q-x.p))%x.p = Nat.gcd B x.p * (pairS B x).q := by
  unfold pairS reducePair
  rw [mobius_gcd B x.p x.q hpq hx]
  have hd : Nat.gcd B x.p ∣ x.p+(B*(x.q-x.p))%x.p := by
    rw [← mobius_gcd B x.p x.q hpq hx]
    exact Nat.gcd_dvd_right _ _
  simpa [Nat.mul_comm] using (Nat.div_mul_cancel hd).symm

theorem actual_branch_lift (B : ℕ) (a : Letter) (x : FractionPair)
    (hh : PairHigh x) (hx : PairPrimitive x) :
    (actualMatrix B a x).mulVec (integerLift x) =
      (defect B a x : ℤ) • integerLift (pairStep B a x) := by
  cases a with
  | T =>
    have hnum := congrArg (fun n : ℕ => (n : ℤ)) (pairT_num_conservation B x hx)
    have hden := congrArg (fun n : ℕ => (n : ℤ)) (pairT_den_conservation B x hx)
    have hmod := congrArg (fun n : ℕ => (n : ℤ)) (Nat.mod_add_div (B*x.p) x.q)
    push_cast at hnum hden hmod
    funext i
    fin_cases i <;>
      simp [actualMatrix, branchT, Matrix.mulVec, dotProduct, Fin.sum_univ_two,
        integerLift, pairStep, defect] <;> nlinarith
  | S =>
    have hpq := le_of_lt hh.2.1
    have hnum := congrArg (fun n : ℕ => (n : ℤ)) (pairS_num_conservation B x hpq hx)
    have hden := congrArg (fun n : ℕ => (n : ℤ)) (pairS_den_conservation B x hpq hx)
    have hmod := congrArg (fun n : ℕ => (n : ℤ)) (Nat.mod_add_div (B*(x.q-x.p)) x.p)
    push_cast at hnum hden hmod
    simp only [Nat.cast_sub hpq] at hden hmod
    funext i
    fin_cases i <;>
      simp [actualMatrix, branchS, Matrix.mulVec, dotProduct, Fin.sum_univ_two,
        integerLift, pairStep, defect, Nat.cast_sub hpq] <;> nlinarith

theorem actualMatrix_det (B : ℕ) (a : Letter) (x : FractionPair) :
    (actualMatrix B a x).det = (B : ℤ) := by
  cases a <;> simp [actualMatrix, branchT_det, branchS_det]

theorem actual_path_matrix_content (B n : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter)
    (hh : ∀ i < n, PairHigh (x i)) (hp : ∀ i < n, PairPrimitive (x i))
    (he : ∀ i < n, x (i+1) = pairStep B (a i) (x i)) :
    (chronologicalProduct (fun i => actualMatrix B (a i) (x i)) n).mulVec (integerLift (x 0)) =
      (∏ i ∈ Finset.range n, (defect B (a i) (x i) : ℤ)) • integerLift (x n) := by
  apply matrix_content_path (fun i => actualMatrix B (a i) (x i))
    (fun i => integerLift (x i)) (fun i => (defect B (a i) (x i) : ℤ)) n
  intro i hi
  rw [he i hi]
  exact actual_branch_lift B (a i) (x i) (hh i hi) (hp i hi)

theorem actual_path_determinant (B n : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter) :
    (chronologicalProduct (fun i => actualMatrix B (a i) (x i)) n).det = (B : ℤ)^n := by
  apply matrix_path_determinant
  intro i hi
  exact actualMatrix_det B (a i) (x i)

theorem actual_cycle_matrix_content (B n : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter)
    (hh : ∀ i < n, PairHigh (x i)) (hp : ∀ i < n, PairPrimitive (x i))
    (he : ∀ i < n, x (i+1) = pairStep B (a i) (x i)) (hc : x n = x 0) :
    (chronologicalProduct (fun i => actualMatrix B (a i) (x i)) n).mulVec (integerLift (x 0)) =
      (∏ i ∈ Finset.range n, (defect B (a i) (x i) : ℤ)) • integerLift (x 0) := by
  rw [actual_path_matrix_content B n x a hh hp he, hc]

theorem actual_cycle_spectrum (B n : ℕ) (x : ℕ → FractionPair) (a : ℕ → Letter)
    (hh : ∀ i ≤ n, PairHigh (x i)) (hp : ∀ i < n, PairPrimitive (x i))
    (he : ∀ i < n, x (i+1) = pairStep B (a i) (x i)) (hc : x n = x 0) :
    let M := chronologicalProduct (fun i => actualMatrix B (a i) (x i)) n
    let Δ := ∏ i ∈ Finset.range n, (defect B (a i) (x i) : ℤ)
    Δ ∣ (B : ℤ)^n ∧ M 0 0+M 1 1=Δ+(B : ℤ)^n/Δ ∧
      (M 0 0+M 1 1)^2-4*(B : ℤ)^n=((B : ℤ)^n/Δ-Δ)^2 := by
  let M := chronologicalProduct (fun i => actualMatrix B (a i) (x i)) n
  let Δ := ∏ i ∈ Finset.range n, (defect B (a i) (x i) : ℤ)
  change Δ ∣ (B : ℤ)^n ∧ M 0 0+M 1 1=Δ+(B : ℤ)^n/Δ ∧
    (M 0 0+M 1 1)^2-4*(B : ℤ)^n=((B : ℤ)^n/Δ-Δ)^2
  have hvec := actual_cycle_matrix_content B n x a (fun i hi => hh i (by omega)) hp he hc
  have h0 : M 0 0*(x 0).p+M 0 1*(x 0).q=Δ*(x 0).p := by
    simpa [M, Δ, Matrix.mulVec, dotProduct, Fin.sum_univ_two, integerLift] using congrFun hvec 0
  have h1 : M 1 0*(x 0).p+M 1 1*(x 0).q=Δ*(x 0).q := by
    simpa [M, Δ, Matrix.mulVec, dotProduct, Fin.sum_univ_two, integerLift] using congrFun hvec 1
  have hv : ((x 0).p : ℤ) ≠ 0 ∨ ((x 0).q : ℤ) ≠ 0 :=
    Or.inl (by exact_mod_cast (ne_of_gt (hh 0 (Nat.zero_le n)).1))
  have hΔ : 0 < Δ := by
    apply Finset.prod_pos
    intro i hi
    exact_mod_cast defect_pos B (a i) (x i) (hh i (by have := Finset.mem_range.mp hi; omega))
  have hd := actual_path_determinant B n x a
  change M.det = (B : ℤ)^n at hd
  rw [Matrix.det_fin_two] at hd
  simpa only [hd] using integer_eigenvalue_identities _ _ _ _ _ _ Δ hv (ne_of_gt hΔ) h0 h1

end RadixMobius
