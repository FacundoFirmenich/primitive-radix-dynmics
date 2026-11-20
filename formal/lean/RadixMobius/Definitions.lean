import Mathlib.Data.Rat.Floor
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
Exact rational definitions for RGΦ. Author: Facundo Firmenich.
The interval is open; neither endpoint is included.
-/
namespace RadixMobius

abbrev High (x : ℚ) : Prop := 1 / 2 < x ∧ x < 1

def radix (B : ℕ) (x : ℚ) : ℚ := (B : ℚ) * x - (⌊(B : ℚ) * x⌋ : ℚ)

def phi (x : ℚ) : ℚ := 1 / (1 + x)

def phiInv (x : ℚ) : ℚ := (1 - x) / x

def mobius (B : ℕ) (x : ℚ) : ℚ := phi (radix B (phiInv x))

theorem high_pos {x : ℚ} (hx : High x) : 0 < x := by
  rcases hx with ⟨hx, _⟩
  linarith

theorem high_ne_zero {x : ℚ} (hx : High x) : x ≠ 0 := ne_of_gt (high_pos hx)

theorem phi_phiInv {x : ℚ} (hx : x ≠ 0) : phi (phiInv x) = x := by
  unfold phi phiInv
  field_simp

theorem phiInv_phi {x : ℚ} (hx : 1 + x ≠ 0) : phiInv (phi x) = x := by
  unfold phi phiInv
  field_simp

theorem high_phiInv {x : ℚ} (hx : High x) : 0 < phiInv x ∧ phiInv x < 1 := by
  have hp := high_pos hx
  rcases hx with ⟨hl, hu⟩
  unfold phiInv
  constructor
  · exact div_pos (by linarith) hp
  · apply (div_lt_iff₀ hp).2
    linarith

theorem phi_high {y : ℚ} (hy0 : 0 < y) (hy1 : y < 1) : High (phi y) := by
  have hp : 0 < 1 + y := by linarith
  unfold High phi
  constructor
  · apply (lt_div_iff₀ hp).2
    linarith
  · apply (div_lt_iff₀ hp).2
    linarith

end RadixMobius
