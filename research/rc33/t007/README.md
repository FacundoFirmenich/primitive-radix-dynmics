# T007 sister-branch certificates

Run `make t007-verify` for the original Frontera VII verifier, an orthogonal exhaustive n=16..20 implementation, exact tower/Gauss controls, all 43 good-prime elliptic constraints and the quick Q<=500 hexagon replay. `make t007-full-hexagon` repeats the complete Q<=5000 census. The full run has already been executed; its source hash and actual execution record are in `saved/`.

The C++ implementation explicitly restricts Qmax to 1..5000; its arithmetic fits 32-bit signed integers in that domain. `check_hexagon.py` independently enumerates literal ranges through Q=30 and checks all three terminal unit obstructions. No full six-state classification or five-state arithmetic closure is claimed.

[Seven claim cards](RESULTS.md) retain their target branch and scope.
