import RadixMobius.ActualCycles
import RadixMobius.Realization

namespace RadixMobius

theorem old_family_defects (t : ℕ) (i : Fin 5) :
    defect (oldBase+t*oldPeriod) .T (oldCarrier i) = 1 ∧
    defect (oldBase+t*oldPeriod) .S (oldCarrier i) = (if i=3 then 3 else 1) := by
  constructor
  · change Nat.gcd (oldBase+t*oldPeriod) (oldCarrier i).q = 1
    rw [gcd_periodic _ _ _ _ (oldCarrier_period_divisibility i).2, Nat.gcd_comm]
    exact oldCarrier_T_defects i
  · change Nat.gcd (oldBase+t*oldPeriod) (oldCarrier i).p = _
    rw [gcd_periodic _ _ _ _ (oldCarrier_period_divisibility i).1, Nat.gcd_comm]
    exact oldCarrier_strict_edge i

theorem new_family_defects (t : ℕ) (i : Fin 5) :
    defect (newBase+t*newPeriod) .T (newCarrier i) = 1 ∧
    defect (newBase+t*newPeriod) .S (newCarrier i) = (if i=3 then 2 else 1) := by
  constructor
  · change Nat.gcd (newBase+t*newPeriod) (newCarrier i).q = 1
    rw [gcd_periodic _ _ _ _ (newCarrier_period_divisibility i).2, Nat.gcd_comm]
    exact newCarrier_T_defects i
  · change Nat.gcd (newBase+t*newPeriod) (newCarrier i).p = _
    rw [gcd_periodic _ _ _ _ (newCarrier_period_divisibility i).1, Nat.gcd_comm]
    exact newCarrier_strict_edge i

end RadixMobius
