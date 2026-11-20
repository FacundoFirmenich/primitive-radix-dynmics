import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! The exact integer square instrument used by the all-height index search. -/
namespace RadixMobius

theorem conic_discriminant_factorization (u v w K U V W : ℤ) :
    (2*u*U*V + v*V*W - K*W^2)^2
      - 4*(u*U^2 + v*U*W + w*W^2)*(u*(V^2-W^2)) =
    W^2 * ((v^2-4*u*w)*V^2 - 2*K*(2*u*U+v*W)*V
      + K^2*W^2 + 4*u*(u*U^2+v*U*W+w*W^2)) := by
  ring

theorem conic_linear_elimination (u v w P h z K J q s : ℚ)
    (h₁ : u*(s^2-1)+v*s*q+w*q^2 = K*q)
    (h₂ : P*(1-s^2)+h*q+z*q^2 = J*s*q)
    (hq : q ≠ 0) :
    (u*J-P*v)*s = (P*w+u*z)*q + (u*h-P*K) := by
  apply (mul_right_cancel₀ hq)
  nlinarith [congrArg (fun x => P*x) h₁, congrArg (fun x => u*x) h₂]

end RadixMobius
