# Continued numerical and source review

Review date: November 4, 2026, America/Chicago.

The main article remains nine pages, with detailed workings beginning on page 10.
The complete PDF remains 29 pages. This pass retains the earlier restructuring
and source corrections and repairs two floating-point edge cases in the
mathematical verification code.

## Numerical corrections

The critical phase solution is evaluated as `2*atan(u/(1+u))`, where
`u = epsilon*t`. The algebraically equivalent expression `1 - 1/(1+u)`
loses relative precision for small positive `u`: at `epsilon = 0.2` and
`t = 1e-18`, it returned zero instead of approximately `4e-19` radians.
The corrected expression preserves the initial slope `2*epsilon`. If the
positive product exceeds the floating-point range, the limiting angle is
already indistinguishable from `pi/2` at that precision.

The binary quantizer now rejects nonfinite scaled coordinates and bin labels
at or above `2**53`. Previously, a width near the smallest positive float
produced two infinite labels; their apparent equality incorrectly returned
zero bits. A request outside representable bin precision now fails explicitly.
Rounding near bin boundaries and long-time underflow remain documented limits.

Three additional regression tests cover the initial slope, extreme finite
positive products, and unrepresentable quantizer labels. All **34 tests pass**.
The information-validation outputs were regenerated. The maximum change in
the critical-solution CSV is `2.7755575615628914e-16` radians. Its summary,
the binary-information output, the oscillator parameters, and all reported
scientific conclusions are unchanged.

## Mathematical and source checks

The locking threshold, both equilibrium branches, critical asymptotic,
mean phase-slip rate, radial distance law, tangent domination bound,
forced invariant graph, finite-time injectivity, and projection closure
conditions were read again. No additional analytic correction was needed.

The primary records for Hermansen et al. (2024), Berger and Bounemoura,
and the di Sarra et al. correction were checked again:

- https://www.nature.com/articles/s41467-024-49703-1
- https://arxiv.org/abs/1109.3280
- https://doi.org/10.1371/journal.pcbi.1013623

The correction replaces duplicated panels in a synthetic torus calibration
figure. The manuscript already cites it and distinguishes that calibration
from neural recordings. The companion observer paper's first-author name
was corrected to Giovanni di Sarra and the correction notice was added there.

## Verification boundary

The final XeLaTeX build has no unresolved references, citation warnings,
duplicate labels, or overfull boxes. The four changed pages were rendered and
visually inspected. The paper makes no new biological claim, estimates no
neural memory lifetime, and does not claim a completed Lean formalization.

The prior automatic publication review restricted the toroidal changes to
local commits. On 2026-11-05 the author explicitly approved publishing the
completed revision to `main`. Publication uses the verified prior head
`2e971a431a640545bf031617445f3d61a7d5e722` as its parent and preserves all
unmodified repository files.
