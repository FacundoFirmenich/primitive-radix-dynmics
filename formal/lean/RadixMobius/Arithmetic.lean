import Mathlib.Data.Nat.GCD.Basic

/-! Exact reduction factors; no high-image assumption is needed for these gcd identities. -/
namespace RadixMobius

theorem radix_gcd (B p q : ℕ) (h : p.Coprime q) :
    Nat.gcd ((B*p)%q) q = Nat.gcd B q := by
  calc
    Nat.gcd ((B*p)%q) q = Nat.gcd q (B*p) := (Nat.gcd_rec q (B*p)).symm
    _ = Nat.gcd (B*p) q := Nat.gcd_comm _ _
    _ = Nat.gcd B q := h.gcd_mul_right_cancel B

theorem mobius_gcd (B p q : ℕ) (hpq : p ≤ q) (h : p.Coprime q) :
    Nat.gcd p (p+(B*(q-p))%p) = Nat.gcd B p := by
  have hc : (q-p).Coprime p := (Nat.coprime_sub_self_left hpq).2 h.symm
  calc
    Nat.gcd p (p+(B*(q-p))%p) = Nat.gcd p ((B*(q-p))%p) := Nat.gcd_self_add_right _ _
    _ = Nat.gcd ((B*(q-p))%p) p := Nat.gcd_comm _ _
    _ = Nat.gcd p (B*(q-p)) := (Nat.gcd_rec p (B*(q-p))).symm
    _ = Nat.gcd (B*(q-p)) p := Nat.gcd_comm _ _
    _ = Nat.gcd B p := hc.gcd_mul_right_cancel B

theorem gcd_periodic (B t M d : ℕ) (hd : d ∣ M) :
    Nat.gcd (B+t*M) d = Nat.gcd B d := by
  have hdiv : d ∣ t*M := dvd_mul_of_dvd_right hd t
  have hmod : (B+t*M)%d = B%d := by
    simp [Nat.add_mod, Nat.mod_eq_zero_of_dvd hdiv]
  rw [Nat.gcd_comm (B+t*M) d, Nat.gcd_rec d (B+t*M), hmod,
    ← Nat.gcd_rec d B, Nat.gcd_comm d B]

end RadixMobius
