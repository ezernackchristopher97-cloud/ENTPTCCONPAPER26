# Toroidal Manifolds and Recursive Neural Dynamics

The manuscript distinguishes circular phase coordinates, sampled population topology, invariant manifolds, and dynamical attraction. Its simulations are mathematical examples in arbitrary units, not neural recordings or fits.

See [the initial claim audit](docs/toroidal_claim_audit.md) for the evidence boundaries and exact analytic results. Its approved corrections were committed locally as `0e24f8f`, based on `2e971a431a640545bf031617445f3d61a7d5e722`. The [follow-up mathematical audit](docs/followup_math_audit.md) and editorial revision were approved and committed locally as `d9397f5`.

The [source and mathematical recheck](docs/source_math_recheck.md) covers all 54 original bibliography entries, the newly cited correction notice, the manuscript's equations, and repeat numerical verification. Its additional source corrections and the structural revision are included in the continuation revision. The author explicitly approved publication of the completed revision to `main` on 2026-11-05.

The [editorial revision record](docs/editorial_revision.md) maps the supplied handwritten comments and writing guide to the earlier revision. The [paper structure revision](docs/paper_structure_revision.md) records the subsequent reorganization: abstract, introduction, methods and principal equations, results, discussion, and conclusion. Detailed derivations, data processing, provenance records, numerical checks, and extended models follow in Appendices A–H. The main text develops the argument without requiring readers to work through the audit or proofs first.

The [continued review](docs/continuation_review.md) corrects cancellation near zero time in the critical-locking formula and rejects quantizer bins outside floating-point integer precision. All 34 tests pass. The numerical limits are documented in Appendix D; the scientific conclusions are unchanged.

## Reproduce the checks

With Python 3.12 and the versions in `requirements-validation.txt`, run from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/oscillator_validation.py
python scripts/information_validation.py
python scripts/audit_empirical_provenance.py
```

The simulation writes CSV trajectories, convergence and threshold tables, a labeled figure, and a JSON summary to `outputs/oscillator_validation/`. The provenance audit writes `outputs/claim_audit/empirical_provenance.json` and does not overwrite legacy data. The validation commands have no network dependency or random sampling. Float results can differ slightly between platforms; analytic tests use stated tolerances.

The supplementary script writes `outputs/information_validation/`: a finite resolution binary-code example, an exact critical-locking benchmark, projection-closure checks, and unit conversions. It does not estimate neural memory, thermal entropy production, or biological coupling across scales.

## Build the paper

XeLaTeX is required for the Unicode Lean examples. With TeX Live, Latin Modern fonts, and DejaVu Sans Mono installed:

```bash
cd paper/figures
pdflatex -interaction=nonstopmode -halt-on-error fig_grid_cell_hex.tex
pdflatex -interaction=nonstopmode -halt-on-error fig_toroidal_manifold.tex
pdflatex -interaction=nonstopmode -halt-on-error fig_entropy_funnel.tex
pdflatex -interaction=nonstopmode -halt-on-error fig_recursive_loop.tex
cd ..
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The resulting PDF is `paper/build/main.pdf`. The review copy at `paper/main.pdf` is copied from that build. The other named historical PDFs are unchanged and do not represent this revision.

## Recording selection

The old activity builder pooled separate recordings on a single time axis and merged repeated cell labels. The existing root-level empirical outputs are retained for provenance, not validated simultaneous population evidence. New analysis requires explicit selection, for example:

```bash
python scripts/preprocessing.py --session Hafting_Fig2c_Trial1.mat
```

All empirical command line scripts use the same `--session` option and write to `outputs/sessions/<recording>/`, which is excluded from version control. `build_activity_matrix` rejects multiple files unless a single filename is explicitly selected. Rate map export rejects a multi-recording call to prevent trial overwrites.

`scripts/run_pipeline.py --session <filename>` also requires Ripser, Persim, and optionally UMAP. That full pipeline has not been rerun or calibrated by the mathematical audit. It computes only H0/H1 in its current entry point, and is not an H2 or attractor validation. The incomplete Lean prototypes have no pinned build and were not machine checked.

## Entropy and position semantics

The legacy function and column names are retained for compatibility. `neural_entropy` is Shannon entropy of normalized neuron activity shares within each time bin, conditional on positive activity; it is not joint population-process entropy. `temporal_entropy` is entropy of activity mass allocated to at most the requested number of contiguous windows, not an entropy rate or memory statistic. When sample count is not divisible by window count, window lengths differ by one sample and the resulting distribution depends on those exposures.

Silent rows, empty distributions, and missing rate maps are `NaN`, not measured zero entropy. Summary statistics exclude undefined rows and report total, defined, and undefined bin counts. Zero probability contributes exactly zero without clipping. Negative or infinite weights fail validation; `NaN` spatial bins indicate unobserved positions and are excluded.

Spike-to-position alignment now selects the nearest retained timestamp (ties use the earlier sample), correcting the previous systematic selection of the following sample. Missing tracking intervals are not interpolated. The retained rate-map method still approximates occupancy with sample count times median sampling interval; irregular sampling and long tracking gaps require additional treatment before quantitative biological interpretation. The legacy maps remain unchanged.
