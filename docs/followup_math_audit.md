# Follow-up mathematical audit

Review date: November 3, 2026, America/Chicago. Base: approved local commit `0e24f8fc5e711c8e91718bab75ec460243006b55`. This follow-up is prepared for review and is not yet committed. No changes have been published to GitHub.

The first audit's central conclusion remains: the retained biological measurements do not establish an attracting invariant torus. This pass examines remaining mathematical implications, information measures, and implementation errors. Synthetic examples below are not biological evidence.

## Additional corrections

| Location | Previous claim or behavior | Correction |
| --- | --- | --- |
| Coupled oscillator section | The locking threshold had only a zero-exponent caveat | Give the exact positive-threshold solution, its algebraic approach, and its failure of Lyapunov stability |
| Information persistence | Contraction and information loss were not separated at finite time | Smooth deterministic flow is injective on its finite-time domain; a specified finite-resolution observation can nevertheless lose a label |
| Entropy | Differential entropy, Shannon statistics, and physical entropy could still be conflated | Derive the normal-coordinate differential entropy change and keep it separate from both label information and thermodynamic production |
| Continuity across scales | A consistency equation was proposed without a testable closure criterion | Require preservation of observation classes, state the necessary projected-vector-field equation, and give success/failure examples |
| Quaternion representation | T³ was described as not naturally embedded in S³ | Prove that no continuous embedding exists, using invariance of domain and the distinct fundamental groups |
| Ordered phase test | Order-conditioned differences were presented as evidence of noncommutative phase composition | Ordinary torus translations commute; ordered sampling can reflect delays or other dynamics without identifying quaternion operators |
| Coupling statistics | PAC and wPLI were both called symmetric marginals | PAC assigns different roles to phase and amplitude; wPLI measures pairwise phase synchronization; neither specifies a three-operator law |
| Thermodynamic balance | The total entropy change was called production; strict negative export followed from nonnegative production | Distinguish change, production, and exchange; at stationarity export is nonpositive and strictly negative only for positive production |
| Hierarchical compression | Every neural level was said to reduce description length | Make this conditional on a coding scheme and model; the cited MDL preprint does not establish monotonic biological compression |
| Wave equation | Moving charges were linked directly to a vacuum wave equation | State vacuum assumptions and the separate homogeneous Ohmic equation; neural sources and dispersive material response require more than a constant loss term |
| Frequency and energy scales | Inverse kinetic times were treated as coherent frequencies; a 10–12 decade gap was claimed | Remove the unsupported kinetic frequency range; compute the stated separation as 6–10 decades and distinguish THz photon energies from bond dissociation or neural coherence |
| Topological recovery | A finite torus sample was said to yield two persistent classes unconditionally | Require adequate sampling, metric selection, and noise controls |
| Entropy code | Zero probabilities were clipped, silence and missing maps could be reported as measured zero, window count could exceed the request | Use exact zero terms, undefined values for zero mass or missing data, explicit summary denominators, and a bounded partition of all samples |
| Spike alignment | A function documented as nearest-sample alignment always selected the following sample | Compare both neighboring timestamps; break exact ties toward the earlier sample; reject invalid time axes and exclude all nonfinite coordinates |

The exact manuscript and code replacements are in the accompanying follow-up source diff. The new mathematical passages are also reproduced below with their assumptions.

## Critical locking calculation

For Δω = 2ε > 0 and δ(0) = 0, set u = tan(δ/2). The difference equation becomes

```text
u' = ε(u − 1)²
u(t) = εt/(1 + εt)
δ(t) = 2 arctan[εt/(1 + εt)]
π/2 − δ(t) ~ 1/(εt)
```

This is algebraic approach from below, not exponential stability. Immediately above π/2 the velocity is positive, so initially nearby states depart before winding around the circle. The critical equilibrium is therefore not Lyapunov stable. The negative-detuning case has the corresponding sign-reversed description; the numerical benchmark uses the positive case only.

`critical_locking.csv` compares the exact expression with DOP853 over [0, 200], using the existing reference tolerances (relative 10⁻¹², absolute 10⁻¹³, maximum step 0.1). Maximum phase-difference error is approximately 2.59 × 10⁻¹³. The theorem is the analytic calculation, not agreement of finite samples.

## Information and observation

Let B be an equiprobable binary label and x_B(0) ∈ {0.25, 0.75}. Under x' = −2x, the two exact states are distinct at every finite time. Thus I(B; x_B(t)) = 1 bit under exact observation. A coarse observation QΔ(x) = floor(x/Δ) maps both values to bin zero for t > log(0.75/Δ)/2. The observed mutual information then vanishes. The times are 1.0074515103 for Δ = 0.1 and 1.3540251006 for Δ = 0.05, in arbitrary units.

These numbers depend on the initial code, quantizer, alignment, and resolution. They do not estimate biological memory or a universal information-decay rate. Long-time floating-point trajectories eventually lose distinctions; finite-time injectivity is a statement about the exact differential equation. Two adaptive integrations agree with the exact displacement trajectories to 2.17 × 10⁻¹² on [0, 3]; finite inverse reconstruction differs from the original displacements by at most 2.65 × 10⁻¹² there.

For a two-dimensional random displacement with a density and finite differential entropy, X(t) = exp(−λt)X(0) gives h(X(t)) = h(X(0)) − 2λt in nats in fixed coordinates. A change in differential entropy is compatible with an invertible transformation. Neither that change nor loss under quantization supplies a heat or thermodynamic entropy production measurement.

## Projection and autonomous coarse dynamics

The relation π ∘ F_t = G_ct ∘ π requires that equal observations remain equal under evolution. Differentiation gives Dπ_x f(x) = c g(π(x)). These are necessary conditions; existence and regularity of a quotient flow require the relevant additional assumptions.

For the sine pair, projection to φ₁ fails: (0, 0) and (0, π/2) have the same first phase but first-phase velocities ω₁ and ω₁ + ε. With ε = 0.6 and ω₁ = 1, the velocities are 1.0 and 1.6. Their projected states separate immediately.

The circular sum σ = (φ₁ + φ₂) mod 2π instead obeys σ' = ω₁ + ω₂. Numerical sum-phase error is approximately 2.84 × 10⁻¹⁴ over [0, 20]. The sum is globally well defined on T²; the average of the two phases is only used with a local lift elsewhere in the manuscript.

## Entropy implementation and recording smoke check

The code normalizes nonnegative finite weights without adding probability mass. All-zero weights define no probability distribution, so the result is NaN. NaN spatial bins are unobserved and excluded. Missing maps remain missing. Negative or infinite weights fail validation. A single positive category has exactly zero entropy; uniform mass on k categories has log₂ k bits.

Window allocation uses min(requested windows, sample count) nonempty contiguous groups. Their sample counts differ by at most one, and every sample is used once. This is an allocation statistic, not an entropy rate or information-persistence measure. Window lengths and binning still affect it. Permuting complete windows leaves it unchanged.

The recording-specific rate-map and entropy CLIs completed for `Hafting_Fig2c_Trial1.mat`. The 59,992 activity bins contained 13,388 bins with positive activity and 46,604 silent bins. The activity-share summary reports both counts and conditions its mean on defined bins. These are implementation smoke checks, not new topology or attractor results; the generated session outputs are not promoted into the manuscript's empirical findings.

The provenance audit still exactly reproduces the legacy pooled activity matrix. Recomputed retained spatial entropies differ from the initial audit by at most 1.78 × 10⁻¹⁵ bits, ordinary floating-point rounding; the retained legacy output files are unchanged. The nearest-position correction changes only newly generated maps. Occupancy still uses sample count times median tracking interval, so irregular sampling and long gaps require further treatment before quantitative biological interpretation.

## Verification and limits

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/information_validation.py
python scripts/audit_empirical_provenance.py
python scripts/rate_maps.py --session Hafting_Fig2c_Trial1.mat
python scripts/entropy.py --session Hafting_Fig2c_Trial1.mat
```

The test suite contains 31 passing tests, including the original step-refinement and solver checks plus the new threshold, observation, entropy, and alignment cases. Supplementary CSVs and JSON are retained under `outputs/information_validation/`. The original mathematical simulations and empirical legacy artifacts remain unchanged. No full neural persistent-homology analysis, H₂ reconstruction, stochastic robustness study, or Lean compilation was added.

Before the subsequent editorial revision, this mathematical revision built to 45 pages with no final-pass LaTeX warnings or unresolved references. All pages were rendered for layout review, with detailed inspection of the new threshold and information equations. Python compilation and whitespace checks passed. The current structure and response to the supplied annotated draft are recorded in [the editorial revision record](editorial_revision.md).

## Primary sources checked

- Hatcher, *Algebraic Topology* (2002), [Theorem 2B.3 and Corollary 2B.4](https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf), p. 172: invariance of domain and compact equal-dimensional manifold embeddings.
- Tort et al. (2010), [Measuring Phase-Amplitude Coupling](https://doi.org/10.1152/jn.00106.2010): distinct phase and amplitude roles.
- Vinck et al. (2011), [weighted phase lag index](https://doi.org/10.1016/j.neuroimage.2011.01.055): imaginary cross-spectrum weighting for pairwise synchronization.
- Tong, [electromagnetism lecture notes](https://www.damtp.cam.ac.uk/user/tong/em.html), and Fitzpatrick, [waves in conducting media](https://farside.ph.utexas.edu/teaching/jk1/lectures/node70.html): Maxwell equations, Ohmic response, and dispersion assumptions.
- NIST, [SI defining constants](https://www.nist.gov/si-redefinition/meet-constants): E = hν yields 0.41356677–41.35667697 meV over 0.1–10 THz, and kBT = 26.71373311 meV at 310 K. These are unit conversions, not biological measurements.
- Prada et al., [arXiv:2505.14635v2](https://arxiv.org/abs/2505.14635v2): an external model-specific MDL proposal, not a general theorem about biological hierarchy.
