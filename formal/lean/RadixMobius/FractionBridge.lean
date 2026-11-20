import RadixMobius.Definitions
import RadixMobius.Arithmetic
import RadixMobius.FiniteWitness
import Mathlib.Data.Nat.Cast.Field

namespace RadixMobius

def value (x : FractionPair) : ℚ := (x.p : ℚ) / x.q

theorem value_reducePair (p q : ℕ) : value (reducePair p q) = (p : ℚ)/q := by
  exact Nat.cast_div_div_div_cancel_right (Nat.gcd_dvd_right p q) (Nat.gcd_dvd_left p q)

theorem radix_fraction (B p q : ℕ) (hq : 0 < q) :
    radix B ((p : ℚ)/q) = (((B*p)%q : ℕ) : ℚ)/q := by
  have hq0 : (q : ℚ) ≠ 0 := by exact_mod_cast (ne_of_gt hq)
  have hfloor : (⌊((B*p : ℕ) : ℚ)/(q : ℚ)⌋ : ℤ) = ((B*p/q : ℕ) : ℤ) := by
    simpa only [Int.natCast_ediv] using Rat.floor_natCast_div_natCast (B*p) q
  have hmod := congrArg (fun n : ℕ => (n : ℚ)) (Nat.mod_add_div (B*p) q)
  push_cast at hmod
  unfold radix
  rw [← mul_div_assoc, ← Nat.cast_mul, hfloor]
  simp only [Int.cast_natCast, Nat.cast_mul]
  field_simp
  nlinarith

theorem phiInv_fraction (p q : ℕ) (hp : 0 < p) (hpq : p ≤ q) :
    phiInv ((p : ℚ)/q) = ((q-p : ℕ) : ℚ)/p := by
  have hp0 : (p : ℚ) ≠ 0 := by exact_mod_cast (ne_of_gt hp)
  have hq0 : (q : ℚ) ≠ 0 := by exact_mod_cast (ne_of_gt (lt_of_lt_of_le hp hpq))
  unfold phiInv
  rw [Nat.cast_sub hpq]
  field_simp

theorem pairT_value (B : ℕ) (x : FractionPair) (hq : 0 < x.q) :
    value (pairT B x) = radix B (value x) := by
  unfold pairT
  rw [value_reducePair]
  exact (radix_fraction B x.p x.q hq).symm

theorem pairS_value (B : ℕ) (x : FractionPair) (hp : 0 < x.p) (hpq : x.p ≤ x.q) :
    value (pairS B x) = mobius B (value x) := by
  have hp0 : (x.p : ℚ) ≠ 0 := by exact_mod_cast (ne_of_gt hp)
  unfold pairS mobius
  rw [value_reducePair]
  unfold value
  rw [phiInv_fraction x.p x.q hp hpq, radix_fraction B (x.q-x.p) x.p hp]
  unfold phi
  push_cast
  field_simp

theorem pairHigh_value {x : FractionPair} (hx : PairHigh x) : High (value x) := by
  have hp : 0 < (x.p : ℚ) := by exact_mod_cast hx.1
  have hq : 0 < (x.q : ℚ) := by exact_mod_cast (lt_trans hx.1 hx.2.1)
  have hpq : (x.p : ℚ) < x.q := by exact_mod_cast hx.2.1
  have hqp : (x.q : ℚ) < 2*x.p := by exact_mod_cast hx.2.2
  unfold High value
  constructor
  · exact (lt_div_iff₀ hq).2 (by linarith)
  · exact (div_lt_iff₀ hq).2 (by simpa using hpq)

theorem pairT_denominator (B : ℕ) (x : FractionPair) (h : PairPrimitive x) :
    (pairT B x).q = x.q / Nat.gcd B x.q := by
  unfold pairT reducePair
  rw [radix_gcd B x.p x.q h]

theorem pairS_numerator (B : ℕ) (x : FractionPair) (hpq : x.p ≤ x.q)
    (h : PairPrimitive x) : (pairS B x).p = x.p / Nat.gcd B x.p := by
  unfold pairS reducePair
  rw [mobius_gcd B x.p x.q hpq h]

end RadixMobius
