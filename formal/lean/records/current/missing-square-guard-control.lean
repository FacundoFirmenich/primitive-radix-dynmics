import RadixMobius
namespace RadixMobius
example : ¬ (IsSquare ((2 : ℤ))) := by 
  rintro ⟨r, hr⟩
  have h1 : r < 2 := by nlinarith
  have h2 : -2 < r := by nlinarith
  have h : r = -1 ∨ r = 0 ∨ r = 1 := by omega
  rcases h with h | h | h <;> subst r <;> norm_num at hr
end RadixMobius
