import RadixMobius.ActionMonoid
import RadixMobius.Realization
import Mathlib.Tactic.FinCases

namespace RadixMobius

theorem code_eq_iff_word_actions (u v : List Letter) :
    codeOf u = codeOf v ↔ ∀ i : Fin 5, runGraph u i = runGraph v i := by
  constructor
  · intro h i
    have h0 := congrArg (fun m : ActionCode => m.1) h
    have h1 := congrArg (fun m : ActionCode => m.2.1) h
    have h2 := congrArg (fun m : ActionCode => m.2.2.1) h
    have h3 := congrArg (fun m : ActionCode => m.2.2.2.1) h
    have h4 := congrArg (fun m : ActionCode => m.2.2.2.2) h
    fin_cases i <;> first
      | exact h0
      | exact h1
      | exact h2
      | exact h3
      | exact h4
  · intro h
    simp only [codeOf, h]

theorem rational_word_actions_eq_iff (B : ℕ) (x : Fin 5 → ℚ)
    (hinj : Function.Injective x)
    (hT : ∀ i, radix B (x i) = x (graphT i))
    (hS : ∀ i, mobius B (x i) = x (graphS i)) (u v : List Letter) :
    (∀ i, runRational B u (x i) = runRational B v (x i)) ↔ codeOf u = codeOf v := by
  constructor
  · intro h
    apply (code_eq_iff_word_actions u v).mpr
    intro i
    apply hinj
    rw [← runRational_intertwines B x hT hS, ← runRational_intertwines B x hT hS]
    exact h i
  · intro h i
    rw [runRational_intertwines B x hT hS, runRational_intertwines B x hT hS,
      (code_eq_iff_word_actions u v).mp h i]

theorem old_family_action_classification (t : ℕ) (u v : List Letter) :
    (∀ i, runRational (oldBase+t*oldPeriod) u (value (oldCarrier i)) =
      runRational (oldBase+t*oldPeriod) v (value (oldCarrier i))) ↔ codeOf u = codeOf v :=
  rational_word_actions_eq_iff _ _ oldCarrier_values_injective
    (oldCarrier_rational_edges t).1 (oldCarrier_rational_edges t).2 u v

theorem new_family_action_classification (t : ℕ) (u v : List Letter) :
    (∀ i, runRational (newBase+t*newPeriod) u (value (newCarrier i)) =
      runRational (newBase+t*newPeriod) v (value (newCarrier i))) ↔ codeOf u = codeOf v :=
  rational_word_actions_eq_iff _ _ newCarrier_values_injective
    (newCarrier_rational_edges t).1 (newCarrier_rational_edges t).2 u v

end RadixMobius
