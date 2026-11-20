import Lake
open Lake DSL
package «radix-mobius» where
  version := v!"0.3.3"
require mathlib from git "https://github.com/leanprover-community/mathlib4.git" @ "c44e0c8ee63ca166450922a373c7409c5d26b00b"
@[default_target]
lean_lib RadixMobius
