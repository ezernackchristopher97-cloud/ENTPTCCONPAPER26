# Response to the annotated manuscript and writing guide

This record describes the November 3 revision. Its structure and page count are superseded by the November 4 [paper structure revision](paper_structure_revision.md), which moves the detailed workings into appendices and rebuilds the main argument.

Revision date: November 3, 2026, America/Chicago. The sources reviewed were the complete 21-page scanned `Chris paper 2.pdf` and `How to write a technical document.docx`. The scanned draft is dated June 3, 2026 and ends partway through its Colab discussion. Page numbers below refer to that supplied scan, not the revised manuscript.

The revision applies the guide's requirements for precise words, one principal thought per sentence, one topic per paragraph, connected topic sentences, a broad-to-specific introduction, reproducible methods, and a brief conclusion. It preserves the checked mathematical conditions and distinguishes synthetic calculations from neural measurements. The title is retained.

## Comment resolution

| Supplied page | Comment or issue | Revision |
| --- | --- | --- |
| 1 | Page numbering requested, then acknowledged | The revised title page also displays a page number. |
| 3 | Lead with the important point; split two ideas; connect the next paragraph | The introduction starts with the role of grid cell populations. Individual tuning, population topology, and dynamical models are introduced in successive paragraphs. The Nobel aside is removed. |
| 4–5 | Combine related Gardner material and reorder the oscillation discussion | Published evidence is summarized once in context. The introduction moves from spatial representation to attractor models, oscillator descriptions, the present comparison, and the paper's organization. |
| 6 | Merge the scope statement into the argument | A single scope paragraph specifies the four claims being compared and the work performed here. Repeated scope disclaimers and separate claim labels are consolidated. |
| 7 | What framework? Define it in a topic sentence | The framework is explicitly defined as a comparison of assumptions, measurements, and conclusions for spatial periodicity, topology, attraction, and information. The unreproduced seven-layer proposal is not introduced as an established model. |
| 8 | Explain how the spatial-code paragraph follows from the model | The lattice quotient is introduced directly, followed by the additional conditions needed for a population map to represent it faithfully. |
| 9–10 | Connect published measurements to the preceding geometry; lead with the result; combine repeated paragraphs | The population-evidence subsection begins by explaining what simultaneous recordings test. Gardner and Hermansen are discussed together, followed by the distinct timing and modeling result from di Sarra. |
| 12 | Define the framework before evaluating consistency; put methods after that discussion | The evidence requirements now precede the data and audit methods. The methods identify the retained files and computations rather than claiming an unreproduced Gardner experiment. |
| 13–14 | Organize the reconstruction and its interpretation coherently | Recording methods precede results. Local topology outputs and draft-only reconstruction claims are reported in separate paragraphs with their provenance. |
| 15 | Explain the transition to entropy; repeated trajectory material | Entropy is defined in methods with its categorical variable and normalization. Results then report the matching statistic. Repeated reconstruction narratives are removed. |
| 16 | Repetition in the UMAP interpretation | Metric distortion is stated once. Sampling density is not asserted to explain a weak gap without a control. |
| 18 | Explain the purpose of parameter variations before listing controls | The audit explains which control implementations are retained. Unsupported control outcomes are not promoted to measured findings. Spatial smoothing, temporal smoothing, and whitening are distinguished. |
| 20–21 | Abrupt transition to the Colab notebook; reader loses the argument | The notebook is identified as a draft-reported analysis with unavailable executable artifacts. It is not introduced as a second unexplained pipeline in the results. The exact draft claims are recorded below for follow-up. |

## New evidence supplied by the scan

The scan contains rendered scientific figures that were not present as matching analysis artifacts in the repository checkout. This changes the document inventory, but does not supply the recordings, notebooks, persistence arrays, or full configuration needed to reproduce those results. The manuscript now acknowledges the figures explicitly.

| Scan location | Draft report | Status in this revision |
| --- | --- | --- |
| pp. 12–13 | Gardner Rat R Day 1 Module 2, 168 cells; eight displayed rate maps | Raster evidence of a reported analysis; underlying recording and export are not supplied. |
| pp. 14–15 | 560 H1 intervals; leading lifetimes 0.772, 0.668, 0.623; 89 H2 intervals; leading lifetimes 0.216, 0.208, 0.174 | These differ from values in the repository manuscript. Neither set is selected as verified without source artifacts. The draft's gap threshold is not treated as a calibrated noise test. |
| pp. 16–18 | Gardner Module 1, 166 cells; UMAP embedding and H1 lifetimes 1.0838, 0.9248, 0.4792 | A separate dataset/module and changed metric cannot be treated as a like-for-like replication of the Module 2 calculation. |
| pp. 18–20 | Timestamp shuffle, 100/500 ms jitter, whitening comparison, and synthetic torus calibration | Executable controls and numerical arrays are not supplied. The term “smoothing ablation” does not describe removing PCA whitening. Reordering timestamps alone leaves a histogram unchanged. |
| pp. 20–21 | A strict Colab analysis with six components, 700/450 sampled points, a parameter sweep, and 149-cell filtering | The supplied excerpt ends before the sweep is complete and contains no executable notebook. No reproduction is claimed. |

The corrected paper does not infer topology or attraction from those raster plots. It also does not claim that the draft-only experiments never occurred. Their reproducibility remains unresolved. The retained Hafting-file audit and its independently checkable provenance findings remain the local numerical basis.

## Structure and scope

The main argument follows this order: introduction; spatial coding and evidence requirements; data and audit methods; audit results; phase dynamics; normal attraction; numerical checks; information and observer mappings; discussion; conclusion.

The exact locking threshold, stability exponent, drift rate, radial contraction, forced invariant graph, numerical convergence limits, and information examples are retained. The initial phase constant is renamed theta_i,0 to distinguish it from the time-dependent phases in the coupled model. The numerical section now separates design, analytic benchmarks, and error checks.

Quaternion topology and operator assumptions are retained in Appendix A. Electromagnetic equations and frequency/energy comparisons are retained in Appendix B. Appendix C states the incomplete formalization status and gives reproduction instructions. The long illustrative Lean listing is removed from the manuscript; the repository prototypes remain available. Repeated conceptual diagrams and speculative narratives are condensed into the discussion. Their scientific status is not strengthened by the editorial changes.

This is an editorial revision of the checked manuscript, not a new neural experiment. No numerical scripts or tests were changed in this pass. The previous 31-test result continues to apply to the unchanged code. Hash comparison confirmed that all ten code, test, and numerical-output files in the preceding follow-up manifest are unchanged.

The final XeLaTeX build produces 26 pages with no warnings, overfull or underfull boxes, or unresolved references. All pages were rendered and visually reviewed, with additional full-size inspection of the locking and information equations. Removing custom section wrappers keeps headings with their following text; paragraph widow and orphan control also improves page breaks. The introduction now fits on one page. Whitespace checks pass.

The updated source and compiled PDF are prepared locally for review; no additional commit or remote publication is included. The accompanying cumulative patch supersedes the earlier follow-up patch and includes both the pending mathematical corrections and this editorial revision.
