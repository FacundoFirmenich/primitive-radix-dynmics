import RadixMobius.FiniteWitness

/-! Complete 36-action semigroup and minimum rank two, checked in the kernel. -/
namespace RadixMobius
abbrev ActionCode := Fin 5 × Fin 5 × Fin 5 × Fin 5 × Fin 5

def codeOf (w : List Letter) : ActionCode :=
  (runGraph w 0, runGraph w 1, runGraph w 2, runGraph w 3, runGraph w 4)

def prependCode (a : Letter) (m : ActionCode) : ActionCode :=
  match a with
  | .T => (m.2.1, m.1, m.2.2.2.1, m.2.2.1, m.2.2.2.2)
  | .S => (m.2.2.2.2, m.2.2.1, m.2.1, m.1, m.1)

def actionCodes : List ActionCode := [
  (0, 1, 2, 3, 4),
  (1, 0, 3, 2, 4),
  (4, 2, 1, 0, 0),
  (4, 3, 0, 1, 1),
  (2, 4, 0, 1, 0),
  (0, 1, 2, 4, 4),
  (3, 4, 1, 0, 1),
  (1, 0, 3, 4, 4),
  (0, 0, 4, 2, 2),
  (1, 0, 4, 2, 4),
  (1, 1, 4, 3, 3),
  (0, 1, 4, 3, 4),
  (0, 0, 2, 4, 2),
  (2, 4, 0, 0, 0),
  (4, 4, 0, 1, 1),
  (1, 1, 3, 4, 3),
  (3, 4, 1, 1, 1),
  (4, 4, 1, 0, 0),
  (2, 2, 0, 0, 0),
  (4, 2, 0, 0, 0),
  (4, 4, 1, 0, 1),
  (1, 0, 4, 4, 4),
  (3, 3, 1, 1, 1),
  (4, 3, 1, 1, 1),
  (4, 4, 0, 1, 0),
  (0, 1, 4, 4, 4),
  (0, 0, 2, 2, 2),
  (0, 0, 2, 4, 4),
  (1, 1, 4, 4, 4),
  (1, 1, 3, 3, 3),
  (1, 1, 3, 4, 4),
  (0, 0, 4, 4, 4),
  (0, 0, 4, 2, 4),
  (4, 4, 1, 1, 1),
  (1, 1, 4, 3, 4),
  (4, 4, 0, 0, 0)]

def generatingWords : List (List Letter) := [
  [],
  [.T],
  [.S],
  [.S, .T],
  [.T, .S],
  [.S, .S],
  [.T, .S, .T],
  [.S, .S, .T],
  [.S, .T, .S],
  [.T, .S, .S],
  [.S, .T, .S, .T],
  [.T, .S, .S, .T],
  [.T, .S, .T, .S],
  [.S, .S, .T, .S],
  [.S, .T, .S, .S],
  [.T, .S, .T, .S, .T],
  [.S, .S, .T, .S, .T],
  [.S, .T, .S, .S, .T],
  [.S, .T, .S, .T, .S],
  [.T, .S, .S, .T, .S],
  [.T, .S, .T, .S, .S],
  [.S, .S, .T, .S, .S],
  [.S, .T, .S, .T, .S, .T],
  [.T, .S, .S, .T, .S, .T],
  [.T, .S, .T, .S, .S, .T],
  [.S, .S, .T, .S, .S, .T],
  [.S, .S, .T, .S, .T, .S],
  [.S, .T, .S, .S, .T, .S],
  [.S, .T, .S, .T, .S, .S],
  [.S, .S, .T, .S, .T, .S, .T],
  [.S, .T, .S, .S, .T, .S, .T],
  [.S, .T, .S, .T, .S, .S, .T],
  [.T, .S, .T, .S, .S, .T, .S],
  [.S, .S, .T, .S, .T, .S, .S],
  [.T, .S, .T, .S, .S, .T, .S, .T],
  [.S, .S, .T, .S, .T, .S, .S, .T]]

theorem codeOf_cons (a : Letter) (w : List Letter) :
    codeOf (a::w) = prependCode a (codeOf w) := by
  cases a <;> rfl

set_option maxRecDepth 100000 in
theorem actionCodes_closed_table :
    ∀ m ∈ actionCodes, prependCode .T m ∈ actionCodes ∧ prependCode .S m ∈ actionCodes := by decide

theorem actionCodes_closed (m : ActionCode) (hm : m ∈ actionCodes) (a : Letter) :
    prependCode a m ∈ actionCodes := by
  cases a with
  | T => exact (actionCodes_closed_table m hm).1
  | S => exact (actionCodes_closed_table m hm).2

set_option maxRecDepth 100000 in
theorem actionCodes_generated : actionCodes = generatingWords.map codeOf := by decide

theorem actionCodes_cardinality : actionCodes.Nodup ∧ actionCodes.length = 36 := by decide

theorem all_word_actions (w : List Letter) : codeOf w ∈ actionCodes := by
  induction w with
  | nil => exact (by decide : codeOf [] ∈ actionCodes)
  | cons a w ih => rw [codeOf_cons]; exact actionCodes_closed _ ih a

theorem reachable_action_iff (m : ActionCode) : (∃ w, codeOf w = m) ↔ m ∈ actionCodes := by
  constructor
  · intro ⟨w, hw⟩
    rw [← hw]
    exact all_word_actions w
  · intro hm
    rw [actionCodes_generated] at hm
    obtain ⟨w, _, hw⟩ := List.mem_map.mp hm
    exact ⟨w, hw⟩

def codeRank (m : ActionCode) : Nat :=
  [m.1, m.2.1, m.2.2.1, m.2.2.2.1, m.2.2.2.2].eraseDups.length

set_option maxRecDepth 100000 in
theorem action_rank_lower : ∀ m ∈ actionCodes, 2 ≤ codeRank m := by decide

set_option maxRecDepth 100000 in
theorem rank_two_attained : ∃ m ∈ actionCodes, codeRank m = 2 := by decide

theorem no_rank_one_word (w : List Letter) : 2 ≤ codeRank (codeOf w) :=
  action_rank_lower _ (all_word_actions w)

theorem rank_two_word_exists : ∃ w, codeRank (codeOf w) = 2 := by
  obtain ⟨m, hm, hr⟩ := rank_two_attained
  obtain ⟨w, hw⟩ := (reachable_action_iff m).2 hm
  exact ⟨w, hw.symm ▸ hr⟩

end RadixMobius
