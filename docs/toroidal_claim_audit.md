# Toroidal claim audit and proposed corrections

Initial audit date: November 2, 2026, America/Chicago. Base: `2e971a431a640545bf031617445f3d61a7d5e722`. The user approved this patch on November 3, and it was committed locally as `0e24f8f`. The findings below record the initial audit; [the follow-up audit](followup_math_audit.md) documents subsequent corrections. Publication to the remote repository remains pending.

## Finding

The retained measurements and the phase equations do **not** establish an attracting invariant torus in the biological grid cell population. This does not refute published toroidal population topology or continuous attractor models. The unsupported step is the inference from spatial tuning or sampled topology to transverse dynamical attraction and to a particular temporal oscillator mechanism.

The original sentence in `paper/main.tex` was:

> The empirical reconstruction in Section 2 provides the necessary justification for treating these phase spaces as dynamical attractors in the grid cell system.

The proposed replacement reads:

> The reconstruction in Section 2 does not justify treating these phase spaces as dynamically attracting neural tori. Spatial tuning, compatibility of a point cloud with T², invariance under a specified flow, and normal attraction are separate claims. Published population topology supports neural representation models, but does not verify the transverse dynamics of these equations.

The section number is rendered from the manuscript reference. The full source diff records the exact LaTeX changes, including changes to the abstract, introduction, methods, captions, dynamics, entropy interpretation, formalization status, and conclusion.

## What each claim requires

| Claim | Mathematical or empirical basis | What it does not imply |
| --- | --- | --- |
| A periodic spatial code factors through a torus | A common lattice Λ gives ℝ²/Λ ≅ T²; wrap coefficients in the lattice basis | An injective population embedding, temporal oscillations, or attraction |
| Two circular phase coordinates give T² | Each phase is defined modulo 2π and the pair is independently specifiable | Independence of random variables, dense trajectories, or normal stability |
| The equations define a flow on T² | C¹ coupling periodic in both phases | A torus attracting nearby states in a larger neural state space |
| An independent orbit is dense | Nonzero frequencies with irrational ratio; for n phases no nonzero integer relation k·ω = 0 | Attraction or proof of irrationality from finite data |
| A pair synchronizes | The specified sine coupling and strict locking threshold | Dense two dimensional quasi periodic motion |
| A torus is normally attracting | An ambient state space and contraction of displacements normal to the torus | Attraction to one timed trajectory or preservation of every encoded distinction |
| A normally hyperbolic manifold persists | Compactness, regularity, domination, and a sufficiently small perturbation in the required norm | Preservation of quasi periodic internal motion |
| A sampled point cloud has toroidal topology | Adequate coverage, metric and noise controls, qualified H0/H1/H2 evidence | Invariance, a basin, a contraction exponent, or causal neural mechanism |
| Entropy constrains a proposed neural model | A defined probability measure, encoded variable, dynamics, and energy/information relation | A deduction from low dimension, spatial entropy, or recurrence alone |

Even Betti numbers (1, 2, 1) do not uniquely identify a general space: the wedge S¹ ∨ S¹ ∨ S² shares those three ranks with T². Additional geometric assumptions or richer invariants are needed. An unresolved H2 feature is inconclusive about the underlying biological topology, not proof of absence.

## Analytic checks

For the specified attractive sine pair,

```text
φ̇1 = ω1 + ε sin(φ2 − φ1)
φ̇2 = ω2 + ε sin(φ1 − φ2)
δ = φ2 − φ1, Δω = ω2 − ω1, ε > 0
δ̇ = Δω − 2ε sin δ
ψ̇ = (ω1 + ω2)/2, using a local lift ψ = (φ1 + φ2)/2
```

For |Δω| < 2ε, the stable branch has δ* = arcsin(Δω/(2ε)) and exponent −√(4ε² − Δω²). The other branch π − δ* is unstable. The stable set is an S¹ in T². It is a periodic orbit if the common frequency is nonzero, or an equilibrium family if that frequency is zero. The common phase remains neutral. At equality the exponent vanishes, so exponential stability cannot be inferred. Outside the threshold, the signed mean slip rate is sgn(Δω)√(Δω² − 4ε²); a nonzero slip rate alone does not prove density.

Adding ṙi = −λ(ri − 1), λ > 0, gives an invariant torus r1 = r2 = 1 embedded in ℝ⁴ with exact normal decay exp(−λt). For the sine pair, λ > 2|ε| is a sufficient normal domination bound because the tangent Jacobian has eigenvalues 0 and −2ε cos δ. Reversing the sign of λ leaves the vector field on the torus unchanged but makes its normal directions repelling. This is a concrete counterexample to inferring attraction from on-manifold trajectories.

For independent phases, the perturbed radial equation ṙi = −λ(ri − 1) + a sin φi has exact invariant graph

```text
ri*(φi) = 1 + a(λ sin φi − ωi cos φi)/(λ² + ωi²)
d/dt [ri − ri*(φi)] = −λ[ri − ri*(φi)]
```

The graph has positive radii if |a| < min_i √(λ² + ωi²). Graph displacement bounds distance to this new torus from above. Convergence to the original unit torus is not required. This special solvable perturbation verifies the calculation without claiming persistence under arbitrary perturbations.

These analytic identities supply the proofs for the constructed models. They are separate from the finite numerical tests. Generic normal manifold persistence does not require frequency nonresonance; quasi periodic flow persistence invokes additional arithmetic and nondegeneracy assumptions in the relevant theorem.

## Finite numerical results

All parameters are synthetic and time has arbitrary units. No biological parameters are fitted. Phase runs use initial phases (0.2, 0.9), horizon 200, and RK4 step 0.02. The irrational model assumes exact √2 analytically; floating point numbers do not prove irrationality.

| Case | Parameters | Verified behavior |
| --- | --- | --- |
| Independent irrational | (ω1, ω2) = (1, √2), ε = 0 | Agreement with the exact rotation solution; a 0.2 radian phase displacement stays neutral |
| Independent rational | (1, 3/2), ε = 0 | Exact periodic return at 4π; the full phase coordinate space is still T² |
| Coupled drift | (1, √2), ε = 0.1 | Mean slip 0.362729755126058 analytically; full cycle timing 0.362729755126058 numerically |
| Phase locking | (1, √2), ε = 0.6 | δ* = 0.3524284019; exact exponent −1.1262447002; local fitted exponent −1.1262427746 |
| Normal attraction | λ = 2, initial radii (0.7, 1.3), a = 0 | Normal decay exp(−2t), with both independent and locked phase flows |
| Deformed attracting torus | Independent phases, λ = 2, a = 0.1 | Agreement with the exact invariant graph and its normal decay |
| Sign controls | λ = 2, 0, −2, small radial displacement | Attracting, neutral, and repelling normals with identical dynamics on the unit torus |

Refinement uses steps 0.08, 0.04, 0.02, and 0.01 over the fixed interval [0, 20]. The reference is DOP853 with rtol 10⁻¹², atol 10⁻¹³, and maximum step 0.1. A tighter DOP853 run and independent RK45 run check the locked case. At step 0.01, maximum absolute errors against the reference are approximately 3.9 × 10⁻¹³ (drift), 7.1 × 10⁻¹² (locking), 1.5 × 10⁻¹⁰ (unforced radial), and 1.5 × 10⁻¹⁰ (forced radial). Observed orders are approximately four before numerical floors. Reference tolerance tightening changes the locked trajectory by 2.9 × 10⁻¹⁴; RK45 differs by 1.3 × 10⁻¹² on the comparison grid.

For the scalar normal mode, the RK4 stability polynomial at −λh has modulus below one at all tested steps (maximum λh = 0.16). This is a case-specific numerical check, not a guarantee for arbitrary steps or stiff neural models. Near the locking threshold the decay or slip rate tends to zero; `threshold.csv` compares finite horizons 40 and 200 at 0.99, 1, and 1.01 times the critical coupling. Finite windows cannot establish asymptotic locking or density. No stochastic noise robustness or neural topology calibration is performed.

## Empirical provenance findings

`outputs/claim_audit/empirical_provenance.json` includes input SHA256 hashes and an inventory reproducible from the retained files.

| Earlier assertion | Retained evidence and proposed correction |
| --- | --- |
| 17 neurons, including 13 Hafting and 4 rat_10925 | Five files contain 7, 7, 3, 3, and 3 cell recordings. There are 23 recordings and 13 distinct labels, with repeat labels across trials. The paper now reports these counts without assuming a simultaneous pooled population. |
| A valid temporal population reconstruction | The old builder merges files and repeated cell labels on one time axis. The audit exactly reproduces the saved (59,992, 13) matrix from that rule. Legacy population diagnostics cannot support simultaneous dynamics. |
| Gardner Rat R Day 1 Module 2 was reanalyzed here | No matching raw data, implementation, or output is retained. The claimed 566 H1 features, 800/400 point analyses, and related numerical H2 values cannot be verified here. They are excluded from conclusions. |
| H2 was computed and resolved no dominant feature | No retained H2 output exists; the tracked topology entry point computes maxdim=1. The earlier numerical claim is not endorsed as a verified local result. Even a reproduced weak H2 result would not decide attraction. |
| Two leading H1 generators and a noise floor | The saved legacy diagrams instead contain 32 and 84 finite H1 intervals, with maxima 0.668947 and 4.001927 in different metrics. No noise-floor calibration is retained. The diagrams are stored computations, not valid population evidence. |
| Spatial entropy was about 1.49 bits | The retained map entropies average 10.85994366 bits, with 2,500-bin uniform reference log₂(2,500) ≈ 11.288. The saved population statistic is 0.260240 bits and inherits invalid pooling. These measures cannot be interchanged. |
| Jitter and shuffling establish a temporal mechanism | The retained ablation script shuffles binned activity values, not spike timestamp events, and has no reported jitter implementation. Merely reordering timestamp entries before binning would not change the train. Spatial smoothing does not establish temporal integration. |
| A persistence figure displays local topology | `fig_persistence_buildspec.png` is absent. A claimed H2 barcode actually included the conceptual entropy funnel PDF. Those misleading figure uses are removed. |
| Lean verifies the geometry and evidence claims | Sources include `sorry`, undefined identifiers, missing theorem names, and no pinned build. Text and appendix now identify them as incomplete prototypes or illustrative definitions. No Lean validation is claimed. |

The new activity builder requires one selected recording and guards against combining unrelated files. The rate map builder guards against overwriting identically named cells across trials. All empirical CLIs use `--session` and a recording-specific output namespace. Original data and legacy numerical outputs are preserved, with their limitations documented.

## Related mathematical interpretation corrections

The revised paper also distinguishes spatial lattice phases from temporal oscillator phases; coordinate spaces from the image of an observation map; normal recovery from recovery of information along a manifold; recurrence from self reference; and lower dimension from lower thermodynamic or information theoretic entropy. A possible consistency condition π ∘ F_t = G_ct ∘ π is explicitly an additional assumption for comparing fine and coarse flows, not a theorem connecting physical scales.

The quaternion operator equation is retained as an optional rotation equation, with an explicit statement that it does not encode all phase triples or derive T³ dynamics. The stale T³ ⊂ S³ drawing is corrected. The entropy and recursive schematics are labeled conceptual hypotheses rather than measured mechanisms. The Broer book authors/DOI and di Sarra first name are corrected against the primary publication records.

## Scope and outstanding work

The checked scope is the toroidal dynamics argument, related empirical provenance, and directly connected information interpretations. This is not a complete validation of the paper's speculative consciousness, molecular, terahertz, microbiome, or cognitive mechanisms. The original data and valid conditional mapping results remain available. The full biological PCA/UMAP/Ripser pipeline was not rerun, H2 was not newly computed, and the unfinished Lean project was not repaired or executed. Further empirical attraction claims need simultaneous population data, calibrated topology recovery, and independent dynamical recovery evidence.

## Primary sources checked

Gardner et al., *Nature* 602, 123–128 (2022): [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8810387/), [DOI](https://doi.org/10.1038/s41586-021-04268-7). External population topology evidence, waking/sleep comparisons, and distinct binning/smoothing/visualization methods.

Hermansen, Klindt, and Dunn, *Nature Communications* 15, 5429 (2024): [DOI](https://doi.org/10.1038/s41467-024-49703-1). External evidence that population code topology need not match behavioral task dimension.

di Sarra, Jha, and Roudi, *PLOS Computational Biology* 21, e1012776 (2025): [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12165393/), [DOI](https://doi.org/10.1371/journal.pcbi.1012776). External spike timing perturbations and the independent rate modulated Poisson model; this is not a local experiment.

Berger and Bounemoura, *Dynamical Systems* 28(4) (2013): [author preprint](https://arxiv.org/abs/1109.3280), [DOI](https://doi.org/10.1080/14689367.2013.835386). Persistence of normally hyperbolic invariant manifolds under appropriately small perturbations.

Broer, Huitema, and Sevryuk, *Quasi-Periodic Motions in Families of Dynamical Systems*, LNM 1645 (1996): [publisher record](https://link.springer.com/book/10.1007/978-3-540-49613-7). Quasi periodic persistence is distinct from normal manifold persistence.
