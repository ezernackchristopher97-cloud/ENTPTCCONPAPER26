# Source and mathematical recheck

Review date: November 4, 2026, America/Chicago. Baseline: approved local commit `d9397f5f401d9cd7a42ccede633529ac35d7bc22`. The source corrections described here were initially a separate follow-up and are now included in the local continuation commit. GitHub `main` was read after the blocked publication attempt and remained at `2e971a431a640545bf031617445f3d61a7d5e722`.

## Findings

The central mathematical conclusions survive this recheck. Circular phase coordinates do not establish normal attraction. The sine pair locks onto a circle under the stated strict threshold. The amplitude extension has an attracting invariant torus because its normal dynamics are explicitly contracting. The retained neural artifacts do not establish that biological mechanism.

The bibliography initially contained 54 entries: 29 cited by the revised manuscript and 25 unused. Every entry was checked against a publication, author, publisher, or bibliographic record. The checks below distinguish claim support from bibliographic identity. They are not a complete proof audit of every cited book or external paper. Some full texts were unavailable through the accessible sources; publisher abstracts, indexed author abstracts, and catalogs were used where indicated. Exact equations in this manuscript were checked independently rather than inferred from a title or abstract.

This pass found four erroneous unused records and one incomplete cited record:

| Entry | Correction |
| --- | --- |
| `Ashwin2024` | The matching article is by Peter Ashwin, Muhammed Fadera, and Claire Postlethwaite; article 102818, DOI `10.1016/j.conb.2023.102818`. The previous coauthors, article number, and DOI did not match. |
| `Northoff2019` | Add coauthors Soren Wainio-Theberge and Kathinka Evers. Retain the 2020 journal year; 2019 is the online publication year and legacy key. |
| `Northoff2022` | Add Federico Zilio; correct volume 424, article 113788, and DOI `10.1016/j.bbr.2022.113788`. |
| `Pu2025` | Replace the unverified Advanced Science record with the identifiable Pu et al. review, *A new horizon for neuroscience: terahertz biotechnology in brain research*, Neural Regeneration Research 20(2), 309–325, DOI `10.4103/NRR.NRR-D-23-00872`. The corrected authors are Zhengping Pu, Yu Wu, Zhongjie Zhu, Hongwei Zhao, and Donghong Cui. This remains an unused reference, not new evidence for a claim. |
| `BergerBounemoura2013` | Add the verified page range 567–581. |

Di Sarra et al. have a published correction dated October 29, 2025. It replaces two duplicated panels in their synthetic torus calibration Figure 2. The notice does not report changes to the spike-jitter results summarized here. The correction is now cited explicitly, bringing the bibliography to 55 records and the manuscript to 30 cited records. No external experiment is claimed to have been reproduced.

The manuscript also now describes Yoon et al.'s evidence for continuous attractor dynamics explicitly. Their empirical argument uses conservation of relationships among simultaneous cells under ongoing perturbations. It should not be reduced to a claim about a toroidal point cloud alone, or transferred to this repository's invalid pooled matrix.

The normal hyperbolicity statement now specifies domination of tangent growth in forward and backward time and small autonomous perturbations of the vector field. This clarifies the theorem's scope; it changes none of the numerical parameters or calculated results.

## Cited source checks

Each linked record was consulted for the stated purpose. “Background” means the citation motivates a model or supplies standard context, not that the source proves this manuscript's neural interpretation.

| Key | Source checked | Supported use and boundary |
| --- | --- | --- |
| `Hafting2005` | [Nature article](https://doi.org/10.1038/nature03721) | Triangular spatial firing grids. Does not verify the identity or simultaneity of all locally pooled columns. |
| `Gardner2022` | [Nature article and methods](https://www.nature.com/articles/s41586-021-04268-7) | Simultaneous module recordings, persistent cohomology, and toroidal organization across conditions. Methods specify 10 ms spike bins, separate 50 ms Gaussian smoothing, and downsampling for visualization. These are different operations. |
| `Yoon2013` | [Author abstract and article record](https://pubmed.ncbi.nlm.nih.gov/23852111/) | Conserved relationships despite deformed individual responses and evidence supporting a continuous attractor. The new paragraph preserves this stronger empirical argument while keeping its provenance separate. |
| `Wu2016` | [Full review](https://pmc.ncbi.nlm.nih.gov/articles/PMC4752021/) | Continuous families of bump states and neutral directions along a represented feature. Model background, not a fit of the sine pair. |
| `Buzsaki2006` | [Publisher book record and abstract](https://academic.oup.com/book/11166) | Oscillatory organization as background. Full book not reaudited. |
| `Canolty2006` | [Author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC2628289/) | Human cortical phase-amplitude coupling. Does not identify the manuscript's symmetric phase-phase coupling law. |
| `Tort2009` | [Author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC2791641/) | Rat hippocampal coupling associated with learning. Correlation and modulation are not an autonomous torus-attraction measurement. |
| `Hermansen2024` | [Nature Communications article](https://www.nature.com/articles/s41467-024-49703-1) | Toroidal population representation during one dimensional behavior, including wheel running. Population topology can differ from immediate task dimension. |
| `DiSarra2025` | [Full PLOS article](https://doi.org/10.1371/journal.pcbi.1012776) | Distinguishes timing perturbations, spatial grid scores, and topology; includes independent rate-modulated Poisson simulations. Simulation and recording findings remain distinct. |
| `DiSarra2025Correction` | [Correction notice](https://doi.org/10.1371/journal.pcbi.1013623) | Corrected synthetic Figure 2 panels; added to the manuscript. |
| `Winfree2001` | [Publisher record and contents](https://link.springer.com/book/10.1007/978-1-4757-3484-3) | Phase description and cyclic biological dynamics; second edition confirmed. No exact neural model inferred from the book. |
| `Strogatz2015` | [Author's second-edition page](https://www.stevenstrogatz.com/press/2015/4/11/qa-with-steven-strogatz-about-nonlinear-dynamics-and-chaos-2nd-edition), [edition record](https://search.worldcat.org/title/1018004504) | Standard phase dynamics background. The 2015 second-edition record is valid; the publisher also has later editions. Density and locking calculations were checked directly. |
| `Kuramoto1984` | [Publisher record and contents](https://link.springer.com/book/10.1007/978-3-642-69689-3) | Phase description and mutual entrainment background. The factor of two in this paper follows from its two symmetric coupling terms, not an assumed normalization of an N-oscillator model. |
| `Strogatz2000` | [Published article](https://doi.org/10.1016/S0167-2789(00)00094-4) | Kuramoto synchronization background. Its large-population transition is not substituted for the exact two-oscillator threshold. |
| `BergerBounemoura2013` | [Full author manuscript, Definition 1 and Theorem 2.1](https://arxiv.org/pdf/1109.3280), [publication record](https://doi.org/10.1080/14689367.2013.835386) | Compact invariant normally hyperbolic submanifolds persist under small C1 perturbations. The stated theorem is for diffeomorphisms; its application to autonomous flows uses a fixed-time map and local uniqueness. It does not guarantee quasiperiodicity. |
| `Broer1996` | [Publisher record, description, and contents](https://link.springer.com/book/10.1007/978-3-540-49613-7) | Parameter-dependent quasiperiodic persistence requires context-specific hypotheses. No detailed theorem from the book is invoked without its assumptions. |
| `Kolmogorov1954` | [Original-paper translation](https://courses.seas.harvard.edu/climate/eli/Courses/APM203/2003fall/Kolmogorov-KAM-1954.pdf), [record](https://cds.cern.ch/record/430016) | Hamiltonian setting and substantial regularity assumptions. Historical KAM context, not a dissipative-neural theorem. |
| `Arnold1963` | [Journal record](https://www.mathnet.ru/eng/rm6404) | Title, year, volume, issue, pages, and Hamiltonian scope confirmed. No reproof of the external KAM theorem claimed. |
| `Moser1962` | [Original-edition catalog](https://katalog.bibliothek.kit.edu/bib/509387), [translated publication](https://www.mathnet.ru/eng/mat236) | Annulus map and area-preserving scope; original 20-page edition distinguished from the Russian translation's pagination. |
| `Prigogine1977` | [Book record](https://catalogue.library.cern/legacy/105309), [digitized book record and contents](https://books.google.com/books?id=CPK7AAAACAAJ) | Nonequilibrium thermodynamics background. Full book not reaudited. The entropy balance and steady-state sign implication were checked independently. |
| `LiVitanyi2008` | [Publisher third-edition record and description](https://link.springer.com/book/10.1007/978-0-387-49820-1) | Description length and coding background, not a theorem of decreasing biological entropy. |
| `RaoBallard1999` | [Published article](https://doi.org/10.1038/4580) | Hierarchical predictions and residual errors in a visual model. Does not establish monotonic compression at every biological layer. |
| `Prada2025` | [Version 2 full text](https://arxiv.org/html/2505.14635v2) | An explicitly identified preprint linking predictive coding and MDL under model assumptions. Its generalization and convergence claims are not adopted as biological facts or independently certified here. |
| `Hatcher2002` | [Author's Chapter 2, p. 172](https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf) | Theorem 2B.3 and Corollary 2B.4 justify the equal-dimensional embedding obstruction. The T3 versus S3 fundamental-group contradiction is explicit. |
| `Tort2010` | [Full methods article](https://doi.org/10.1152/jn.00106.2010) | Phase and amplitude play different roles; neither this statistic nor ordered sampling defines quaternion operators. |
| `Vinck2011` | [Authors' institutional record and abstract](https://dare.uva.nl/id/3eec1b14-41c3-4434-963d-14766c93a608) | wPLI weights phase leads/lags by the magnitude of the imaginary cross-spectrum. No three-operator composition law follows. |
| `Tong2015` | [Author's lecture notes](https://www.damtp.cam.ac.uk/user/tong/em.html), [2015 title page](https://www.damtp.cam.ac.uk/user/tong/em/el1.pdf) | Vacuum and material Maxwell equations; conducting-media section distinguishes frequency-dependent conductivity. The manuscript's constant-coefficient Ohmic equation requires its stated narrower assumptions. |
| `NISTConstants` | [SI constants](https://www.nist.gov/si-redefinition/meet-constants) | Exact defining values of h, e, and kB; energy conversions reproduced. They do not establish biological coherence. |
| `Markelz2008` | [Author's publication record](https://markelz.physics.buffalo.edu/node/195), [institutional record](https://researchconnect.buffalo.edu/en/publications/terahertz-dielectric-sensitivity-to-biomolecular-structure-and-fu/) | Biomolecular THz spectroscopy background. Metadata confirmed; no claim of measured grid-cell coupling. |
| `Frohlich1968` | [Original article and abstract](https://doi.org/10.1002/qua.560020505) | A theoretical energy-supply/coherence proposal, correctly identified as a proposal. |

## Unused bibliography checks

These entries remain in the BibTeX database but are not cited or printed in the revised paper. Confirmation of a record does not endorse every claim in that work.

| Key | Record checked | Result |
| --- | --- | --- |
| `Sahu2013` | [Authors' institution](https://samurai.nims.go.jp/articles/d7914b5a-4175-4000-9d31-7abf6ba95728) | Title, seven authors, venue, pages, year, DOI match. |
| `Jaynes1976` | [Author's society](https://www.julianjaynes.org/about/about-julian-jaynes/), [book record](https://books.google.com/books?id=nHF-AAAAMAAJ) | Book identity, author, original year, and publisher match. |
| `Cryan2019` | [Original article](https://doi.org/10.1152/physrev.00018.2018) | Author list, title, journal, volume, pages, year, DOI match. |
| `Bonaz2018` | [Article record](https://pubmed.ncbi.nlm.nih.gov/29467611/) | Metadata match. |
| `Hofstadter1979` | [Publisher](https://shop.hachettebookgroup.com/products/godel-escher-bach) | Author/title/imprint identified; original 1979 edition retained, not the current reprint date. No scientific inference relies on this unused book. |
| `Godel1931` | [Journal record](https://doi.org/10.1007/BF01700692) | Author, title, journal, year, volume, pages match. |
| `Northoff2019` | [Published article](https://doi.org/10.1016/j.plrev.2019.05.002) | Two missing coauthors restored; journal year is 2020. |
| `Northoff2022` | [Published article](https://doi.org/10.1016/j.bbr.2022.113788) | Coauthor, volume, article number, and DOI corrected. |
| `Buzsaki2004` | [Article record](https://pubmed.ncbi.nlm.nih.gov/15218136/) | Metadata match. |
| `Ashwin2024` | [Published article](https://doi.org/10.1016/j.conb.2023.102818) | Two coauthors, article number, and DOI corrected. |
| `Penrose1989` | [Publisher](https://academic.oup.com/book/40643) | Book identity, author, year, and publisher match. |
| `Hameroff2014` | [Article record](https://pubmed.ncbi.nlm.nih.gov/24070914/) | Metadata match; theory review remains unused. |
| `Fulling2019` | [Article record](https://pubmed.ncbi.nlm.nih.gov/30897366/) | Metadata match, including pages 998–1002. |
| `Dinan2017` | [Article record](https://pubmed.ncbi.nlm.nih.gov/27641441/) | Metadata match; 2017 issue date differs from 2016 online date. |
| `Tononi2008` | [Article record](https://pubmed.ncbi.nlm.nih.gov/19098144/) | Author, title, journal, year, volume, pages match. |
| `Lisman2005` | [Article record](https://pubmed.ncbi.nlm.nih.gov/16161035/) | Identity, author, venue, year, pages, DOI match. The indexed title spells “occuring”; the existing BibTeX spelling “occurring” is not a different work. |
| `Bellmund2018` | [Published article](https://doi.org/10.1126/science.aat6766) | Metadata match. |
| `Mayer2011` | [Published article](https://doi.org/10.1038/nrn3071) | Metadata match. |
| `Yano2015` | [Published article](https://doi.org/10.1016/j.cell.2015.02.047), [erratum](https://doi.org/10.1016/j.cell.2015.09.017) | Original metadata match. An erratum exists; this unused work supplies no current manuscript conclusion. The correction notice's substantive content was not available in the retrieved record. |
| `Friston2010` | [Published article](https://doi.org/10.1038/nrn2787) | Metadata match; no variational-free-energy/thermodynamic-entropy equivalence imported. |
| `Deco2008` | [Full published article](https://doi.org/10.1371/journal.pcbi.1000092) | Metadata match. |
| `Stensola2012` | [Article record](https://pubmed.ncbi.nlm.nih.gov/23222610/) | Metadata match. |
| `Pu2025` | [Journal record](https://www.sjzsyj.com.cn/EN/abstract/abstract25660.shtml) | Replace the unverified entry with the identified review; details above. |
| `Kandel2013` | [Publisher copyright page](https://neurology.mhmedical.com/content.aspx?bookid=1049&sectionid=59138139) | Fifth-edition identity, publisher, and 2013 copyright confirmed; not a full textbook audit. |
| `Dehaene2014` | [Publisher](https://www.penguinrandomhouse.com/books/308282/consciousness-and-the-brain-by-stanislas-dehaene/9780698151406/) | Book identity, author, and 2014 publication confirmed. |

## Mathematical checks

All 23 numbered equations and the intervening claims in the source-review version were read again. The subsequent [paper structure revision](paper_structure_revision.md) relocates these calculations to appendices, retains the principal equations in the main text, and changes their numbering. The following checks refer to the mathematical statements rather than their new equation numbers.

1. **Topology and orbit structure.** A rank-two lattice quotient is R2/Lambda, homeomorphic to T2. The standard R3 parametrization is an embedding for R > r > 0. Constant independent rotations are periodic for a rational nonzero frequency ratio and dense for an irrational ratio. For n phases the correct condition is k dot omega != 0 for every nonzero integer vector k. These density claims are analytic; machine representations and finite traces do not prove them. The wedge S1 vee S1 vee S2 and T2 have the same stated Betti ranks, so ranks alone are insufficient.
2. **Locking.** Subtracting the symmetric sine equations gives delta' = Delta omega - 2 epsilon sin(delta). Adding gives the constant lifted common-phase speed. For epsilon > 0 and |Delta omega| < 2 epsilon, there are two phase-difference equilibria modulo 2 pi. The stable branch has derivative -2 epsilon cos(delta*) and exponent -sqrt(4 epsilon^2 - Delta omega^2). The other branch has positive derivative. The common direction is neutral. Nonzero common speed yields a periodic circle; zero common speed gives a circle of equilibria.
3. **Critical solution.** With u = epsilon t/(1 + epsilon t), delta = 2 atan(u). Both delta' and 2 epsilon(1 - sin(delta)) reduce to 2 epsilon/(1 + 2 epsilon t + 2 epsilon^2 t^2). Also pi/2 - delta is asymptotic to 1/(epsilon t). A perturbation above pi/2 departs before returning around the circle, disproving Lyapunov stability. No negative constant recovery exponent exists at the threshold.
4. **Slip rate.** For Delta omega > 2 epsilon, the period integral over one phase-difference cycle is 2 pi/sqrt(Delta omega^2 - 4 epsilon^2). Reversing detuning reverses the slip sign. Closure of a full trajectory still depends on the common and slip frequencies, not simply the natural frequency ratio.
5. **Normal contraction.** In positive-radius product polar coordinates, distance to the unit product torus is the Euclidean norm of r - 1. Solving r' = -lambda(r - 1) gives the stated exact distance law. Reversing lambda gives local repulsion with unchanged on-torus flow. Negative-rate trajectories need only be considered while they remain in the positive-radius coordinate neighborhood.
6. **Domination.** The tangent Jacobian is epsilon cos(delta) times the matrix with rows (-1,1) and (1,-1). Its Euclidean operator norm is at most 2|epsilon|. Forward and inverse tangent propagators are bounded by exp(2|epsilon|t), so lambda > 2|epsilon| is a sufficient normal domination bound. Attraction of the explicit unit torus already holds for every positive lambda; the stronger bound supplies robust normal hyperbolicity.
7. **Forced graph.** Differentiating g(phi) = 1 + a(lambda sin(phi) - omega cos(phi))/(lambda^2 + omega^2) gives omega g' = -lambda(g - 1) + a sin(phi). Its radial modulation amplitude is |a|/sqrt(lambda^2 + omega^2), giving the stated positive-radius condition. The residual satisfies (r - g)' = -lambda(r - g). This proves local attraction to the deformed graph, not convergence to the original unit torus or persistence under arbitrary forcing.
8. **Numerical stability.** Classical RK4 applied to x' = -lambda x has amplification 1 - z + z^2/2 - z^3/6 + z^4/24, z = lambda h. The tested maximum z = 0.16 is stable; the existing z = 3 test demonstrates numerical growth despite exact decay. Convergence is assessed at a fixed finite horizon against adaptive solvers; rounding and long-time phase error remain limitations.
9. **Information and entropy.** Uniqueness gives injectivity of the exact smooth finite-time flow on its domain. The two equiprobable distinct displacements retain one bit under exact observation. The specified floor quantizer maps both to zero after log(0.75/Delta)/2. This is conditional on that code and measurement. For two continuous normal coordinates, the log determinant is -2 lambda t, producing the differential entropy change in nats. It is not a physical entropy-production calculation. The categorical entropy bounds and zero-mass exclusions match the code; window allocation is not an entropy rate.
10. **Coarse dynamics.** Differentiating pi composed with F_t = G_ct composed with pi gives Dpi f = c g composed with pi. Equal observations must have equal projected evolution. Projection onto phi1 fails for the two exhibited states, whereas the circular sum has a well-defined autonomous rotation. The average of two circular phases is only used on a lift.
11. **Quaternion topology.** Invariance of domain, compactness, and connectedness would make a continuous embedding T3 into S3 a homeomorphism, contradicting their fundamental groups. For pure Omega, the real part of Omega vanishes, so differentiating |q|^2 under q' = Omega q/2 gives zero. Torus translations commute independently of quaternion multiplication.
12. **Physical equations and units.** Taking the curl of Faraday's equation and using zero divergence yields the vacuum wave equation. Constant homogeneous Ohmic response adds the stated -mu sigma partial_t E term. Source currents, dispersion, and boundary conditions are separate assumptions. Steady thermodynamic balance implies exchange = -production <= 0, strictly negative only for positive production. Photon and thermal energies and the six-to-ten-decade frequency separation agree with SI constants.

## Repeat computational results

The full suite passed again: **31 tests**. The oscillator and information scripts were rerun into separate review directories. All **15 retained simulation artifacts** reproduced byte for byte, including both JSON summaries, trajectories, convergence tables, and the oscillator figure. No code changes were needed in this pass.

| Check | Repeated result |
| --- | --- |
| Stable phase difference | 0.35242840190761004 rad |
| Stable relative-phase exponent | -1.1262447002078144 per model time unit |
| Mean slip from full cycles | 0.3627297551260575 rad per model time unit |
| Standard versus tighter adaptive integration | 2.842170943040401e-14 maximum difference |
| Critical exact-solution comparison | 2.5912605394751154e-13 maximum error |
| RK4 h = 0.01 errors, drift / locking / radial / forced radial | 3.872e-13 / 7.077e-12 / 1.500e-10 / 1.464e-10 |
| Radial displacement / finite inverse checks | 2.168e-12 / 2.648e-12 maximum error |
| Coarse circular sum | 2.842e-14 maximum circular error |

The empirical provenance audit also reproduced its findings. The only differences from the older stored JSON were individual spatial entropies at at most 1.7763568394002505e-15 bits, consistent with the previously corrected entropy arithmetic. The mean remains 10.859943659807303 bits. All other audit fields match. There are still 23 cell recordings, 13 distinct labels, 13 retained maps, an exactly reproduced invalid pooled legacy matrix, and no retained H2 output.

These checks do not complete the Lean formalization, estimate biological memory, establish a neural noise floor, reproduce the external population-topology studies, or certify every theorem in the cited literature. The manuscript makes none of those claims.
