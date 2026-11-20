import RadixMobius.Discriminant
import Mathlib.Data.Rat.Lemmas
import Mathlib.Tactic.FieldSimp

namespace RadixMobius

abbrev conicAlpha (u v w U W : ℤ) : ℤ := u*U^2+v*U*W+w*W^2
abbrev conicBeta (u v K U V W : ℤ) : ℤ := 2*u*U*V+v*V*W-K*W^2
abbrev conicGamma (u V W : ℤ) : ℤ := u*(V^2-W^2)
abbrev conicZ (u v w K U V W : ℤ) : ℤ :=
  (v^2-4*u*w)*V^2-2*K*(2*u*U+v*W)*V+K^2*W^2+4*u*(u*U^2+v*U*W+w*W^2)

theorem integer_quadratic_discriminant_square (a b c : ℤ) (q : ℚ)
    (hq : (a : ℚ)*q^2+(b : ℚ)*q+c = 0) : IsSquare (b^2-4*a*c) := by
  apply Rat.isSquare_intCast_iff.mp
  refine ⟨2*(a : ℚ)*q+b, ?_⟩
  push_cast
  nlinarith [congrArg (fun x => 4*(a : ℚ)*x) hq]

theorem square_factor_cancel (W Z : ℤ) (hW : W ≠ 0)
    (hs : IsSquare (W^2*Z)) : IsSquare Z := by
  apply Rat.isSquare_intCast_iff.mp
  obtain ⟨r, hr⟩ := hs
  have hrq := congrArg (fun z : ℤ => (z : ℚ)) hr
  push_cast at hrq
  have hWq : (W : ℚ) ≠ 0 := by exact_mod_cast hW
  refine ⟨(r : ℚ)/(W : ℚ), ?_⟩
  field_simp
  nlinarith

theorem eliminated_quadratic (u v w K U V W q s : ℚ)
    (hf : u*(s^2-1)+v*s*q+w*q^2=K*q)
    (hl : W*s=U*q+V) :
    (u*U^2+v*U*W+w*W^2)*q^2 + (2*u*U*V+v*V*W-K*W^2)*q + u*(V^2-W^2) = 0 := by
  nlinarith [congrArg (fun z => W^2*z) hf,
    congrArg (fun z => u*z^2) hl, congrArg (fun z => v*q*W*z) hl]

theorem conic_filter_nonzero_W (u v w K U V W : ℤ) (q s : ℚ)
    (hW : W ≠ 0)
    (hf : (u : ℚ)*(s^2-1)+v*s*q+w*q^2=K*q)
    (hl : (W : ℚ)*s=U*q+V) : IsSquare (conicZ u v w K U V W) := by
  apply square_factor_cancel W _ hW
  rw [← conic_discriminant_factorization]
  apply integer_quadratic_discriminant_square _ _ _ q
  push_cast
  exact eliminated_quadratic _ _ _ _ _ _ _ q s hf hl

theorem zero_W_discriminant_identity (u v w K U V : ℤ) :
    (-v*V*U)^2 - 4*(u*U^2)*(w*V^2-u*U^2+K*V*U) =
      U^2*conicZ u v w K U V 0 := by
  unfold conicZ
  ring

theorem conic_filter_zero_W (u v w K U V : ℤ) (q s : ℚ)
    (hU : U ≠ 0)
    (hf : (u : ℚ)*(s^2-1)+v*s*q+w*q^2=K*q)
    (hl : (U : ℚ)*q+V=0) : IsSquare (conicZ u v w K U V 0) := by
  apply square_factor_cancel U _ hU
  rw [← zero_W_discriminant_identity]
  apply integer_quadratic_discriminant_square _ _ _ s
  push_cast
  have hl' : (U : ℚ)*q = -(V : ℚ) := by linarith
  nlinarith [congrArg (fun z => (U : ℚ)^2*z) hf,
    congrArg (fun z => (w : ℚ)*z^2) hl',
    congrArg (fun z => (v : ℚ)*s*U*z) hl',
    congrArg (fun z => (K : ℚ)*U*z) hl']

theorem conic_square_filter_sound (u v w K U V W : ℤ) (q s : ℚ)
    (hf : (u : ℚ)*(s^2-1)+v*s*q+w*q^2=K*q)
    (hl : (W : ℚ)*s=U*q+V) : IsSquare (conicZ u v w K U V W) := by
  by_cases hW : W = 0
  · subst W
    by_cases hU : U = 0
    · subst U
      have hV : V = 0 := by exact_mod_cast (by simpa using hl : (0 : ℚ) = V).symm
      subst V
      exact ⟨0, by simp [conicZ]⟩
    · apply conic_filter_zero_W u v w K U V q s hU hf
      simpa using hl.symm
  · exact conic_filter_nonzero_W u v w K U V W q s hW hf hl

def ResidueSquare (m Z : ℤ) : Prop :=
  ∃ r : ℤ, 0 ≤ r ∧ r < m ∧ (r*r)%m = Z%m

theorem square_has_residue (m Z : ℤ) (hm : 0 < m) (hZ : IsSquare Z) :
    ResidueSquare m Z := by
  obtain ⟨r, hr⟩ := hZ
  refine ⟨r%m, Int.emod_nonneg _ (ne_of_gt hm), Int.emod_lt_of_pos _ hm, ?_⟩
  rw [← Int.mul_emod, ← hr]

theorem nonsquare_residue_rejects (m Z : ℤ) (hm : 0 < m)
    (hr : ¬ ResidueSquare m Z) : ¬ IsSquare Z := by
  exact fun hs => hr (square_has_residue m Z hm hs)

theorem conic_modular_rejection (m u v w K U V W : ℤ) (hm : 0 < m)
    (hr : ¬ ResidueSquare m (conicZ u v w K U V W)) :
    ¬ ∃ q s : ℚ,
      (u : ℚ)*(s^2-1)+v*s*q+w*q^2=K*q ∧ (W : ℚ)*s=U*q+V := by
  intro ⟨q, s, hf, hl⟩
  exact nonsquare_residue_rejects _ _ hm hr (conic_square_filter_sound _ _ _ _ _ _ _ q s hf hl)

theorem two_conics_require_square (u v w P h z K J : ℤ) (q s : ℚ)
    (hq : q ≠ 0)
    (h₁ : (u : ℚ)*(s^2-1)+v*s*q+w*q^2=K*q)
    (h₂ : (P : ℚ)*(1-s^2)+h*q+z*q^2=J*s*q) :
    IsSquare (conicZ u v w K (P*w+u*z) (u*h-P*K) (u*J-P*v)) := by
  apply conic_square_filter_sound _ _ _ _ _ _ _ q s h₁
  push_cast
  exact conic_linear_elimination _ _ _ _ _ _ _ _ q s h₁ h₂ hq

theorem two_conics_modular_rejection (m u v w P h z K J : ℤ) (hm : 0 < m)
    (hr : ¬ ResidueSquare m (conicZ u v w K (P*w+u*z) (u*h-P*K) (u*J-P*v))) :
    ¬ ∃ q s : ℚ, q ≠ 0 ∧
      (u : ℚ)*(s^2-1)+v*s*q+w*q^2=K*q ∧
      (P : ℚ)*(1-s^2)+h*q+z*q^2=J*s*q := by
  intro ⟨q, s, hq, h₁, h₂⟩
  exact nonsquare_residue_rejects _ _ hm hr (two_conics_require_square _ _ _ _ _ _ _ _ q s hq h₁ h₂)

end RadixMobius
