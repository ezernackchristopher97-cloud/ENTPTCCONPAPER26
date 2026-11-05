# Paper structure revision

Revision date: November 4, 2026, America/Chicago.

The main text has been rewritten around the argument and findings. The supplied `How to write a technical document.docx` was read again in full. Its document guidance calls for a broad-to-specific introduction, a logical progression from methods to results and discussion, connected paragraph topics, precise language, and a brief conclusion. The user's additional instruction places the detailed workings at the back.

## Main paper

The main paper occupies pages 1–9, including the title and abstract. Its order is abstract, introduction, methods, results, discussion, and conclusion. The introduction states the central findings before describing the paper's organization. The methods introduce the data, model, and verification approach. Results follow that same order. The discussion explains what those results require of a neural interpretation.

Six numbered equations carry the main argument: the coupled phase pair, relative-phase dynamics, radial dynamics, locking and its stability exponent, normal distance decay, and the compatibility of fine and coarse flows. Detailed algebra, numerical settings, and file inventories no longer interrupt that argument. The conditions needed to understand the results remain in the main text, including positive coupling, the strict locking inequality, positive normal contraction, and the role of the observation map.

## Supporting workings

The appendices begin on page 10. The complete document is 29 pages, including references.

| Appendix | Supporting material |
| --- | --- |
| A. Geometry and Phase Dynamics | Lattice coordinates, schematic figure, Betti-rank limitation, torus parametrization, general phase equations, locking branches, critical solution, and slip-rate calculation. |
| B. Normal Attraction and Perturbation Calculations | Exact radial solution and distance proof, positive-radius domain, normal hyperbolicity, explicit tangent Jacobian bound, forced invariant graph, and limits of persistence theorems. |
| C. Data Processing and Provenance | Recording inventory, binning and map parameters, entropy definitions, retained-output audit, reported controls, and sampling and calibration limits. |
| D. Numerical Methods and Verification | Initial conditions, durations, solver settings, perturbation controls, synthetic comparison figure, error measurements, step refinement, and finite-run limitations. |
| E. Observation Maps and Entropy Calculations | Observation classes, repeated processing, exact and quantized binary codes, differential entropy, projection consistency, and thermodynamic entropy balance. |
| F. Quaternion Operators and Phase Coordinates | Embedding obstruction, quaternion equation, and the assumptions required for an operator interpretation. |
| G. Physical Assumptions Across Frequency Scales | Wave equations, material assumptions, frequency ratios, and photon and thermal energy comparisons. |
| H. Formalization and Reproducibility | Limits of the Lean prototypes and instructions for reproducing the calculations. |

The former prose claim that the tangent Jacobian has norm at most twice the coupling magnitude is now accompanied by the explicit matrix and forward/inverse propagation bounds. This supplies the working behind the existing sufficient normal-hyperbolicity condition. The negative normal-rate example is explicitly restricted to the positive-radius coordinate neighborhood. No numerical result or model parameter changes.

## Verification and review state

The final XeLaTeX build has no unresolved citations or references, duplicate labels, overfull boxes, underfull boxes, or warnings. All 30 cited sources are retained. Appendix equations have section-specific numbers and the body links to the corresponding calculations. All pages were rendered and visually checked. Bibliography spacing was adjusted to remove an otherwise isolated final DOI line.

At the structural-revision stage, scripts, tests, stored outputs, and validation dependencies were unchanged from commit `d9397f5`; the prior 31-test pass and 15 reproduced artifacts applied to that version. The subsequent [continued review](continuation_review.md) repairs two precision edge cases, adds three tests, and regenerates the critical-solution CSV. All 34 tests pass in that version. The mathematical and empirical boundaries established by the preceding audits are preserved.

The structural revision and preceding source corrections were initially prepared for review and are now included in the local continuation commit. The cumulative patch records both stages. The earlier publication block remains unresolved; no remote write to this repository was attempted during the continuation pass.
