import RadixMobius.MatrixContent
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic.FieldSimp

namespace RadixMobius
open scoped BigOperators

def chronologicalProduct (M : ℕ → Mat2) : ℕ → Mat2
  | 0 => 1
  | n+1 => M n * chronologicalProduct M n

theorem matrix_content_path (M : ℕ → Mat2) (v : ℕ → Fin 2 → ℤ) (d : ℕ → ℤ) :
    ∀ n, (∀ i < n, (M i).mulVec (v i) = d i • v (i+1)) →
      (chronologicalProduct M n).mulVec (v 0) =
        (∏ i ∈ Finset.range n, d i) • v n := by
  intro n
  induction n with
  | zero => intro h; simp [chronologicalProduct]
  | succ n ih =>
    intro h
    rw [chronologicalProduct, ← Matrix.mulVec_mulVec,
      ih (fun i hi => h i (by omega)), Matrix.mulVec_smul, h n (by omega),
      Finset.prod_range_succ, smul_smul]

theorem matrix_path_determinant (M : ℕ → Mat2) (B : ℤ) :
    ∀ n, (∀ i < n, (M i).det = B) → (chronologicalProduct M n).det = B^n := by
  intro n
  induction n with
  | zero => intro h; simp [chronologicalProduct]
  | succ n ih =>
    intro h
    rw [chronologicalProduct, Matrix.det_mul, h n (by omega), ih (fun i hi => h i (by omega)), pow_succ]
    ring

theorem matrix_cycle_content (M : ℕ → Mat2) (v : ℕ → Fin 2 → ℤ) (d : ℕ → ℤ)
    (n : ℕ) (he : ∀ i < n, (M i).mulVec (v i) = d i • v (i+1))
    (hc : v n = v 0) :
    (chronologicalProduct M n).mulVec (v 0) = (∏ i ∈ Finset.range n, d i) • v 0 := by
  rw [matrix_content_path M v d n he, hc]

theorem two_by_two_characteristic (a b c d p q δ : ℚ)
    (hv : p ≠ 0 ∨ q ≠ 0)
    (h0 : a*p+b*q = δ*p) (h1 : c*p+d*q = δ*q) :
    δ^2 - (a+d)*δ + (a*d-b*c) = 0 := by
  rcases hv with hp | hq
  · have h : p*(δ^2-(a+d)*δ+(a*d-b*c)) = 0 := by
      nlinarith [congrArg (fun x => d*x) h0,
        congrArg (fun x => δ*x) h0, congrArg (fun x => b*x) h1]
    exact (mul_eq_zero.mp h).resolve_left hp
  · have h : q*(δ^2-(a+d)*δ+(a*d-b*c)) = 0 := by
      nlinarith [congrArg (fun x => a*x) h1,
        congrArg (fun x => δ*x) h1, congrArg (fun x => c*x) h0]
    exact (mul_eq_zero.mp h).resolve_left hq

theorem cycle_trace (a b c d p q δ : ℚ)
    (hv : p ≠ 0 ∨ q ≠ 0) (hδ : δ ≠ 0)
    (h0 : a*p+b*q = δ*p) (h1 : c*p+d*q = δ*q) :
    a+d = δ+(a*d-b*c)/δ := by
  have h := two_by_two_characteristic a b c d p q δ hv h0 h1
  field_simp
  nlinarith

theorem cycle_square_discriminant (a b c d p q δ : ℚ)
    (hv : p ≠ 0 ∨ q ≠ 0) (hδ : δ ≠ 0)
    (h0 : a*p+b*q = δ*p) (h1 : c*p+d*q = δ*q) :
    (a+d)^2 - 4*(a*d-b*c) = ((a*d-b*c)/δ-δ)^2 := by
  rw [cycle_trace a b c d p q δ hv hδ h0 h1]
  field_simp
  ring

theorem integer_characteristic (a b c d p q δ : ℤ)
    (hv : p ≠ 0 ∨ q ≠ 0)
    (h0 : a*p+b*q = δ*p) (h1 : c*p+d*q = δ*q) :
    δ^2-(a+d)*δ+(a*d-b*c)=0 := by
  have hvq : (p : ℚ) ≠ 0 ∨ (q : ℚ) ≠ 0 := by exact_mod_cast hv
  have h := two_by_two_characteristic (a : ℚ) b c d p q δ hvq
    (by exact_mod_cast h0) (by exact_mod_cast h1)
  exact_mod_cast h

theorem integer_eigenvalue_identities (a b c d p q δ : ℤ)
    (hv : p ≠ 0 ∨ q ≠ 0) (hδ : δ ≠ 0)
    (h0 : a*p+b*q = δ*p) (h1 : c*p+d*q = δ*q) :
    δ ∣ a*d-b*c ∧ a+d = δ+(a*d-b*c)/δ ∧
      (a+d)^2-4*(a*d-b*c)=((a*d-b*c)/δ-δ)^2 := by
  have hc := integer_characteristic a b c d p q δ hv h0 h1
  have hd : a*d-b*c = δ*(a+d-δ) := by nlinarith
  have hdiv : (a*d-b*c)/δ = a+d-δ := by rw [hd]; simp [hδ]
  refine ⟨⟨a+d-δ, hd⟩, ?_, ?_⟩
  · linarith
  · rw [hdiv, hd]
    ring

end RadixMobius
