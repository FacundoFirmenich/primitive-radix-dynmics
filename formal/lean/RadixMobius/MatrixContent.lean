import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Data.Matrix.Notation
import Mathlib.Data.Int.GCD
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace RadixMobius
abbrev Mat2 := Matrix (Fin 2) (Fin 2) ℤ

def branchT (B k : ℤ) : Mat2 := !![B, -k; 0, 1]
def branchS (B k : ℤ) : Mat2 := !![1, 0; 1-B-k, B]

theorem branchT_det (B k : ℤ) : (branchT B k).det = B := by
  simp [branchT, Matrix.det_fin_two]

theorem branchS_det (B k : ℤ) : (branchS B k).det = B := by
  simp [branchS, Matrix.det_fin_two]

def content (v : Fin 2 → ℤ) : ℕ := Int.gcd (v 0) (v 1)

theorem content_dvd_det (M : Mat2) (v : Fin 2 → ℤ)
    (hv : content v = 1) : (content (M.mulVec v) : ℤ) ∣ M.det := by
  let d : ℤ := content (M.mulVec v)
  have h0 : d ∣ M 0 0 * v 0 + M 0 1 * v 1 := by
    simpa [d, content, Matrix.mulVec, dotProduct, Fin.sum_univ_two] using
      (show (Int.gcd (M.mulVec v 0) (M.mulVec v 1) : ℤ) ∣ M.mulVec v 0 from Int.gcd_dvd_left)
  have h1 : d ∣ M 1 0 * v 0 + M 1 1 * v 1 := by
    simpa [d, content, Matrix.mulVec, dotProduct, Fin.sum_univ_two] using
      (show (Int.gcd (M.mulVec v 0) (M.mulVec v 1) : ℤ) ∣ M.mulVec v 1 from Int.gcd_dvd_right)
  have hp : d ∣ M.det * v 0 := by
    have h := dvd_sub (dvd_mul_of_dvd_right h0 (M 1 1)) (dvd_mul_of_dvd_right h1 (M 0 1))
    convert h using 1; simp only [Matrix.det_fin_two]; ring
  have hq : d ∣ M.det * v 1 := by
    have h := dvd_sub (dvd_mul_of_dvd_right h1 (M 0 0)) (dvd_mul_of_dvd_right h0 (M 1 0))
    convert h using 1; simp only [Matrix.det_fin_two]; ring
  have bez := Int.gcd_eq_gcd_ab (v 0) (v 1)
  have hb : v 0 * Int.gcdA (v 0) (v 1) + v 1 * Int.gcdB (v 0) (v 1) = 1 := by
    rw [← bez]
    exact_mod_cast hv
  have h := dvd_add (dvd_mul_of_dvd_left hp (Int.gcdA (v 0) (v 1)))
    (dvd_mul_of_dvd_left hq (Int.gcdB (v 0) (v 1)))
  convert h using 1
  nlinarith [congrArg (fun x => M.det*x) hb]

theorem content_dvd_natAbs_det (M : Mat2) (v : Fin 2 → ℤ)
    (hv : content v = 1) : content (M.mulVec v) ∣ M.det.natAbs := by
  exact Int.natCast_dvd.mp (content_dvd_det M v hv)

theorem content_dvd_image (M : Mat2) (v : Fin 2 → ℤ) :
    content v ∣ content (M.mulVec v) := by
  apply Int.natCast_dvd_natCast.mp
  apply Int.dvd_coe_gcd
  · have h0 : (content v : ℤ) ∣ v 0 := Int.gcd_dvd_left
    have h1 : (content v : ℤ) ∣ v 1 := Int.gcd_dvd_right
    have h := dvd_add (dvd_mul_of_dvd_right h0 (M 0 0)) (dvd_mul_of_dvd_right h1 (M 0 1))
    simpa [Matrix.mulVec, dotProduct, Fin.sum_univ_two] using h
  · have h0 : (content v : ℤ) ∣ v 0 := Int.gcd_dvd_left
    have h1 : (content v : ℤ) ∣ v 1 := Int.gcd_dvd_right
    have h := dvd_add (dvd_mul_of_dvd_right h0 (M 1 0)) (dvd_mul_of_dvd_right h1 (M 1 1))
    simpa [Matrix.mulVec, dotProduct, Fin.sum_univ_two] using h

theorem content_of_integral_left_inverse (M N : Mat2) (hNM : N*M = 1) (v : Fin 2 → ℤ) :
    content (M.mulVec v) = content v := by
  have hb := content_dvd_image N (M.mulVec v)
  rw [Matrix.mulVec_mulVec, hNM, Matrix.one_mulVec] at hb
  exact Nat.dvd_antisymm hb (content_dvd_image M v)

theorem unimodular_content (U : Mat2ˣ) (v : Fin 2 → ℤ) :
    content ((U : Mat2).mulVec v) = content v := by
  exact content_of_integral_left_inverse (U : Mat2) (↑(U⁻¹) : Mat2) (by simp) v

end RadixMobius
