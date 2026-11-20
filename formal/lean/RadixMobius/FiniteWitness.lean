import Std.Tactic

/-!
Kernel-checked primitive-fraction witnesses. Author: Facundo Firmenich.
This module depends only on the Lean distribution; no external computation
result is assumed. Its bridge to rational conjugate maps is proved separately.
-/
namespace RadixMobius

inductive Letter where
  | T | S
  deriving DecidableEq, Repr

structure FractionPair where
  p : Nat
  q : Nat
  deriving DecidableEq, Repr

abbrev PairHigh (x : FractionPair) : Prop := 0 < x.p ∧ x.p < x.q ∧ x.q < 2*x.p

abbrev PairPrimitive (x : FractionPair) : Prop := Nat.gcd x.p x.q = 1

def reducePair (p q : Nat) : FractionPair :=
  let g := Nat.gcd p q
  ⟨p/g, q/g⟩

def pairT (B : Nat) (x : FractionPair) : FractionPair :=
  reducePair ((B*x.p)%x.q) x.q

def pairS (B : Nat) (x : FractionPair) : FractionPair :=
  reducePair x.p (x.p + (B*(x.q-x.p))%x.p)

def graphT (i : Fin 5) : Fin 5 :=
  match i.val with
  | 0 => 1 | 1 => 0 | 2 => 3 | 3 => 2 | _ => 4

def graphS (i : Fin 5) : Fin 5 :=
  match i.val with
  | 0 => 4 | 1 => 2 | 2 => 1 | _ => 0

def graphStep (a : Letter) : Fin 5 → Fin 5 :=
  match a with | .T => graphT | .S => graphS

def runGraph : List Letter → Fin 5 → Fin 5
  | [], i => i
  | a::w, i => runGraph w (graphStep a i)

theorem runGraph_append (u v : List Letter) (i : Fin 5) :
    runGraph (u++v) i = runGraph v (runGraph u i) := by
  induction u generalizing i with
  | nil => rfl
  | cons a u ih => exact ih (graphStep a i)

def toRoot (i : Fin 5) : List Letter :=
  match i.val with
  | 0 => [] | 1 => [.T] | 2 => [.S,.T] | _ => [.S]

def fromRoot (i : Fin 5) : List Letter :=
  match i.val with
  | 0 => [] | 1 => [.T] | 2 => [.T,.S] | 3 => [.T,.S,.T] | _ => [.S]

theorem toRoot_correct : ∀ i : Fin 5, runGraph (toRoot i) i = 0 := by decide
theorem fromRoot_correct : ∀ i : Fin 5, runGraph (fromRoot i) 0 = i := by decide

theorem graph_strongly_connected (i j : Fin 5) :
    ∃ w : List Letter, runGraph w i = j := by
  refine ⟨toRoot i ++ fromRoot j, ?_⟩
  rw [runGraph_append, toRoot_correct, fromRoot_correct]

theorem graphS_not_injective : ¬ (∀ i j : Fin 5, graphS i = graphS j → i = j) := by
  intro h
  have he : (3 : Fin 5) = 4 := h 3 4 (by rfl : graphS 3 = graphS 4)
  exact (by decide : (3 : Fin 5) ≠ 4) he

def oldBase : Nat := 88011536665779
def oldPeriod : Nat := 223336848698040
def newBase : Nat := 2720751096305053288157586672376
def newPeriod : Nat := 3245172386374697665101193455750

def oldCarrier (i : Fin 5) : FractionPair :=
  match i.val with
  | 0 => ⟨406,731⟩ | 1 => ⟨712,731⟩ | 2 => ⟨712,1265⟩
  | 3 => ⟨1218,1265⟩ | _ => ⟨406,557⟩

def newCarrier (i : Fin 5) : FractionPair :=
  match i.val with
  | 0 => ⟨1089859,2087631⟩ | 1 => ⟨1627375,2087631⟩
  | 2 => ⟨1627375,3121631⟩ | 3 => ⟨2179718,3121631⟩
  | _ => ⟨1089859,2105745⟩

set_option maxRecDepth 100000 in
theorem oldCarrier_primitive : ∀ i, PairPrimitive (oldCarrier i) := by decide

theorem oldCarrier_high : ∀ i, PairHigh (oldCarrier i) := by decide

theorem oldCarrier_distinct : ∀ i j : Fin 5, oldCarrier i = oldCarrier j → i = j := by decide

set_option maxRecDepth 100000 in
theorem oldCarrier_T_edges : ∀ i, pairT oldBase (oldCarrier i) = oldCarrier (graphT i) := by decide

set_option maxRecDepth 100000 in
theorem oldCarrier_S_edges : ∀ i, pairS oldBase (oldCarrier i) = oldCarrier (graphS i) := by decide

set_option maxRecDepth 100000 in
theorem newCarrier_primitive : ∀ i, PairPrimitive (newCarrier i) := by decide

theorem newCarrier_high : ∀ i, PairHigh (newCarrier i) := by decide

theorem newCarrier_distinct : ∀ i j : Fin 5, newCarrier i = newCarrier j → i = j := by decide

set_option maxRecDepth 100000 in
theorem newCarrier_T_edges : ∀ i, pairT newBase (newCarrier i) = newCarrier (graphT i) := by decide

set_option maxRecDepth 100000 in
theorem newCarrier_S_edges : ∀ i, pairS newBase (newCarrier i) = newCarrier (graphS i) := by decide

set_option maxRecDepth 100000 in
theorem oldCarrier_strict_edge :
    ∀ i : Fin 5, Nat.gcd (oldCarrier i).p oldBase = (if i=3 then 3 else 1) := by decide

set_option maxRecDepth 100000 in
theorem newCarrier_strict_edge :
    ∀ i : Fin 5, Nat.gcd (newCarrier i).p newBase = (if i=3 then 2 else 1) := by decide

set_option maxRecDepth 100000 in
theorem oldCarrier_T_defects : ∀ i : Fin 5, Nat.gcd (oldCarrier i).q oldBase = 1 := by decide

set_option maxRecDepth 100000 in
theorem newCarrier_T_defects : ∀ i : Fin 5, Nat.gcd (newCarrier i).q newBase = 1 := by decide

end RadixMobius
