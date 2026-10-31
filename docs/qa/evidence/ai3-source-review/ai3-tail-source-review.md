# Part 3 tail source review

Read-only Part3 manifest positions11–19, Spectra through Outro. All nine chapter sources read in full, relevant compute/translation/docs sections inspected; no rendered QA.

Completed 2026-10-31T16:48:54.072449+00:00; observed HEAD `5c59c4d065a707be467358a234131f3662b48c05` on `qa/ai-series-cloud-20261031`. Separate from the four earlier parent leads and six first-half findings.

## Inventory

| Position | Scene | Source | Direct cache items |
|---:|---|---|---|
| 11 | Spectra | videos/ai/ai3/s11_spectra.py | mp |
| 12 | GaLore | videos/ai/ai3/s12_galore.py | galore, galorectl |
| 13 | Words | videos/ai/ai3/s13_words.py | words |
| 14 | SGNS | videos/ai/ai3/s14_sgns.py | sgns, words |
| 15 | HighDim | videos/ai/ai3/s15_highdim.py | highdim |
| 16 | JL | videos/ai/ai3/s16_jl.py | jl |
| 17 | Geometry | videos/ai/ai3/s17_geometry.py | gpt2, words |
| 18 | Netflix | videos/ai/ai3/s18_netflix.py | mf, twotower |
| 19 | Outro | videos/ai/ai3/s19_outro.py | einsum, galore, gpt2, highdim, image, jl, mf, mp, norms, power, project, sgns |

## New findings

### AI3-T01: Power-law xmin selection uses an incomplete Kolmogorov–Smirnov distance (P1)

source-confirmed-statistic-defect; tiny NumPy reproduction; production impact unmeasured.

Code compares F(x_i) only with (i-1)/n. Correct continuous one-sample D=max(max(i/n-F(x_i)),max(F(x_i)-(i-1)/n)). Eleven positive distinct fixture values yield current0.5256246556 versus correct0.6165337465. Understating D can change the chosen xmin/alpha; no production spectrum was loaded.

References: [videos/ai/ai3/compute.py:591](/workspace/explainer-videos/videos/ai/ai3/compute.py:591), [videos/ai/ai3/compute.py:593](/workspace/explainer-videos/videos/ai/ai3/compute.py:593), [videos/ai/ai3/s11_spectra.py:157](/workspace/explainer-videos/videos/ai/ai3/s11_spectra.py:157).

Repair: Use both ECDF sides, preserve explicit min-tail/candidate policy, and add pure deterministic regression. Do not claim a goodness-of-fit test from this fitted-distance statistic alone.

Cache/regression implications: Version mp fitting semantics and regenerate alpha/xmin/KS/n_tail diagnostics. Authenticated existing eigenvalues can support a cheap derived-fit migration; cache currently absent. Regress Spectra and any recap/captions consuming changed summaries.

Fixture: `ks_both_ecdf_sides` in [ai3-tail-symbolic-fixtures.json](/workspace/runtime/ai3-tail-symbolic-fixtures.json).

### AI3-T02: Nearest-neighbour ranking can return self under cosine ties (P2)

source-confirmed-ranking-defect; tiny NumPy reproduction; actual words affected unmeasured.

Both helpers drop the first sorted item instead of excluding the query ID. For two identical normalized vectors and query index1, argsort gives index0 first, leaving index1 in returned neighbours. Zero-norm and finite-value policies also need definition, especially first-k projections.

References: [videos/ai/ai3/compute.py:855](/workspace/explainer-videos/videos/ai/ai3/compute.py:855), [videos/ai/ai3/compute.py:857](/workspace/explainer-videos/videos/ai/ai3/compute.py:857), [videos/ai/ai3/s13_words.py:161](/workspace/explainer-videos/videos/ai/ai3/s13_words.py:161), [videos/ai/ai3/s13_words.py:164](/workspace/explainer-videos/videos/ai/ai3/s13_words.py:164).

Repair: Mask the actual query score before ranking; return k eligible finite candidates with documented tie policy. Apply consistently to compute.neighbours and the local trajectory helper; add tie and zero-norm fixtures.

Cache/regression implications: words and sgns stored neighbour/snapshot lists depend on helper semantics; invalidate or authenticate/rebuild derived lists. words retains E, but current final sgns output does not retain full trained embeddings, so migration must not invent unseen vectors. Coordinate with existing SGNS provenance repair before training.

Fixture: `self_exclusion_under_ties` in [ai3-tail-symbolic-fixtures.json](/workspace/runtime/ai3-tail-symbolic-fixtures.json).

### AI3-T03: Outro labels a generalized shifted-PMI experiment as ordinary PMI minus log k (P2)

source-confirmed-recap/formula-mismatch; symbolic reproduction; unrendered.

Tile uses lg_exact full-rank data whose theoretical x is log(pair/(nw*pn))-logK, with smoothed negative pn restricted/renormalized to300 words. Ordinary empirical PMI-logK generally differs. Main SGNS scene already correctly qualifies the generalized ratio and Pn=P(c) special case.

References: [videos/ai/ai3/s19_outro.py:76](/workspace/explainer-videos/videos/ai/ai3/s19_outro.py:76), [videos/ai/ai3/s19_outro.py:83](/workspace/explainer-videos/videos/ai/ai3/s19_outro.py:83), [videos/ai/ai3/compute.py:968](/workspace/explainer-videos/videos/ai/ai3/compute.py:968), [videos/ai/ai3/compute.py:1068](/workspace/explainer-videos/videos/ai/ai3/compute.py:1068), [videos/ai/ai3/compute.py:1074](/workspace/explainer-videos/videos/ai/ai3/compute.py:1074), [videos/ai/ai3/s14_sgns.py:145](/workspace/explainer-videos/videos/ai/ai3/s14_sgns.py:145).

Repair: Label recap generalized shifted PMI, or show the actual log-count-ratio formula with negative distribution defined. Preserve the correct special-case problem statement where Pn=P(c) is explicit.

Cache/regression implications: Caption/narration refresh and EN/ZH outro rerender; no data recomputation needed if authentic generalized data remain the intended experiment.

Fixture: `smoothed_negative_caption` in [ai3-tail-symbolic-fixtures.json](/workspace/runtime/ai3-tail-symbolic-fixtures.json).

### AI3-T04: No-overfit branch asserts a worse unregularized endpoint without comparing endpoints (P2)

source-confirmed-conditional-verdict-defect; synthetic counterexample; actual production branch unknown.

overfit compares unregularized final RMSE with its own minimum. Its else says no penalty ends a little worse regardless of regularized endpoint. Regularized final.9 and monotonically improving unregularized1,.85,.8 take that branch despite unregularized ending better.

References: [videos/ai/ai3/s18_netflix.py:169](/workspace/explainer-videos/videos/ai/ai3/s18_netflix.py:169), [videos/ai/ai3/s18_netflix.py:171](/workspace/explainer-videos/videos/ai/ai3/s18_netflix.py:171), [videos/ai/ai3/s18_netflix.py:174](/workspace/explainer-videos/videos/ai/ai3/s18_netflix.py:174), [videos/ai/ai3/zh_lines.py:421](/workspace/explainer-videos/videos/ai/ai3/zh_lines.py:421).

Repair: Branch independently on within-run overfit and final regularized-versus-unregularized gap, with an explicit near-tie policy. State measured values rather than force worse/better. Also label lambda0 as no vector penalty because fixed bias penalty remains.

Cache/regression implications: Narration logic/caption change; authentic histories can be reused. Regress Netflix EN/ZH endpoint/motion/narration.

Fixture: `unregularized_verdict_branch` in [ai3-tail-symbolic-fixtures.json](/workspace/runtime/ai3-tail-symbolic-fixtures.json).

### AI3-T05: Peak layer cosine is narrated as the final network layer value (P2)

source-confirmed-index/wording-mismatch; synthetic counterexample; actual GPT-2 peak location unmeasured.

hi=max(L[1:],key=cos) selects any non-input layer; English says at the top and Chinese says top layer. A sequence [.1,.9,.6,.7] selects.9 at layer1 rather than final.7.

References: [videos/ai/ai3/s17_geometry.py:126](/workspace/explainer-videos/videos/ai/ai3/s17_geometry.py:126), [videos/ai/ai3/s17_geometry.py:130](/workspace/explainer-videos/videos/ai/ai3/s17_geometry.py:130), [videos/ai/ai3/zh_lines.py:401](/workspace/explainer-videos/videos/ai/ai3/zh_lines.py:401).

Repair: Use L[-1] for the final-layer statement or state the peak value with its actual layer index. Preserve both metrics separately if useful.

Cache/regression implications: No measured data recomputation needed; narration and any peak/final callouts must agree with existing authenticated L.

Fixture: `layer_peak_vs_final` in [ai3-tail-symbolic-fixtures.json](/workspace/runtime/ai3-tail-symbolic-fixtures.json).

### AI3-T06: Spectral escapee counts apply an undisclosed 2% margin beyond the plotted edge (P2)

source-confirmed-measurement-threshold/label-mismatch; synthetic counterexample; actual counts unmeasured.

Counters use eigenvalue>1.02*lambda_plus, while line is at lambda_plus and narration says none beyond it when the tolerance count is0. Values1.01*edge and1.03*edge give actual beyond-edge count2 versus displayed tolerance count1.

References: [videos/ai/ai3/compute.py:618](/workspace/explainer-videos/videos/ai/ai3/compute.py:618), [videos/ai/ai3/compute.py:626](/workspace/explainer-videos/videos/ai/ai3/compute.py:626), [videos/ai/ai3/compute.py:632](/workspace/explainer-videos/videos/ai/ai3/compute.py:632), [videos/ai/ai3/s11_spectra.py:104](/workspace/explainer-videos/videos/ai/ai3/s11_spectra.py:104), [videos/ai/ai3/s11_spectra.py:107](/workspace/explainer-videos/videos/ai/ai3/s11_spectra.py:107), [videos/ai/ai3/s11_spectra.py:115](/workspace/explainer-videos/videos/ai/ai3/s11_spectra.py:115).

Repair: Either label/count strictly beyond the displayed edge, or explicitly define the 2% margin in captions/legend/narration and draw its threshold. Keep finite-sample limiting-law qualification, avoiding a hard finite-n spectral support guarantee.

Cache/regression implications: A label-only margin disclosure can reuse counts; changing threshold requires derived-count versioning/migration from authenticated eigenvalues.

Fixture: `edge_count_threshold` in [ai3-tail-symbolic-fixtures.json](/workspace/runtime/ai3-tail-symbolic-fixtures.json).

### AI3-T07: Matrix-factorization baselines and low-rank results use different fitting sets (P1)

source-confirmed-comparison-fairness-defect; mask-only reproduction; measured score impact unknown.

Mean and bias baselines fit80% train; final low-rank test runs and replay fit90% train|valid after lambda selection. Ranks scene describes the RMSE gap as adding taste vectors without disclosing additional fitting ratings. A ten-rating split reproduces8 versus9 observations.

References: [videos/ai/ai3/compute.py:1314](/workspace/explainer-videos/videos/ai/ai3/compute.py:1314), [videos/ai/ai3/compute.py:1318](/workspace/explainer-videos/videos/ai/ai3/compute.py:1318), [videos/ai/ai3/compute.py:1322](/workspace/explainer-videos/videos/ai/ai3/compute.py:1322), [videos/ai/ai3/compute.py:1343](/workspace/explainer-videos/videos/ai/ai3/compute.py:1343), [videos/ai/ai3/compute.py:1350](/workspace/explainer-videos/videos/ai/ai3/compute.py:1350), [videos/ai/ai3/s18_netflix.py:225](/workspace/explainer-videos/videos/ai/ai3/s18_netflix.py:225).

Repair: After regularizer selection, refit mean/bias final baselines on the same train|valid set as low-rank models, with common test set; retain validation-only tuning separation. Store fitting/evaluation counts and split fingerprints.

Cache/regression implications: Version mf baseline fitting semantics; regenerate baseline outputs and dependent captions. Unchanged authentic low-rank training can be reused only if split/model lineage validates; do not mix incomparable old summaries. Regress Netflix ranks/replay and Outro.

Fixture: `matrix_factorization_fitting_sets` in [ai3-tail-symbolic-fixtures.json](/workspace/runtime/ai3-tail-symbolic-fixtures.json).

## Chapter checks, units and render queue

### 11. Spectra

MP support/density for q<=1; variance-one standardization; log-density Jacobian lambda*ln(10); shuffled-number control; tail alpha density units; novels model initialization comparison reviewed. The log-density Jacobian is correct.

Density per unit log10(lambda) is correctly different from density per lambda; alpha is a density exponent. All exceedance counters use a 2% margin over the limiting MP edge, which is not disclosed in current labels (T06).

Native-check the theorem/Wigner split, long log-axis label and tail-band caption. Disclose any alpha>=7.9 cap and lower spectral-bin clamping rather than plotting overflow as an ordinary observation. Show fit tail-size/KS diagnostics, and describe a fitted power law as a descriptive fit until goodness-of-fit/model comparison supports it. External empirical range 1.5–5 and accuracy association require primary-source verification before factual sign-off; this read-only task checked internal references only.

### 12. GaLore

Layer-gradient outer-product/rank bound, approximate low-rank qualification, squared-energy top8 share, top singular-vector window, optimizer-memory counts, Adam split-step control and effective-rank definition reviewed. Compute chooses the shorter projection side while displayed equation illustrates the left variant.

top8 is share of Frobenius norm squared, not share of nuclear norm. opt_numbers counts optimizer state/projector numbers for block matrices only, excluding weights and other parameter states. Effective rank uses entropy of normalized singular values, as labeled. Learning-rate selection uses seed0 validation; selected rates then run seeds1/2, and reported values include seed0.

Label top8 narration as squared gradient energy; retain block-only memory caption and add left/right projection orientation cue. State seed0 tuning plus 3 selected-rate seeds. Improve table/legend spacing, show min–max bands around averaged training curves if available, disclose 8-sample moving smoothing and any hard 3..9 loss clipping. The replay currently overlays four spectra and a complete share curve; synchronized step emphasis/cursor would strengthen temporal correspondence. Do not assert all gradients are low rank solely from the title; body already qualifies approximate behavior.

### 13. Words

Symmetric context-window cooccurrence, smoothed context distribution, positive log-count ratio, truncated SVD embedding weighting/normalization, neighbour trajectories, analogy projection, test exclusion and category purity reviewed.

Displayed PPMI heatmap is the smoothed positive table, while show_pairs examples are ordinary unsmoothed PMI; the smoothing note is present. Category purity selects nearest neighbours only among categorized words, not among all 10,000 vocabulary words; add that candidate-pool qualification near the percentage. Analogy accuracy is over eligible ordered pair-of-pairs and 10k candidate vocabulary excluding a,b,c.

Fix query masking under cosine ties (T02), and define zero-norm policy. Align neighbour text/bar columns at fixed pitch; label bars as cosine. Keep ordinary PMI example and smoothed-table caption visually connected. Show a clear 2D projection disclaimer on analogy arrows, retaining actual 100D nearest-word ranks. Source computes a heuristic first-k settling threshold (3 of 5 among final top10); label that criterion rather than imply all later neighbour lists are identical.

### 14. SGNS

Two-vector SGNS objective, positive versus negative terms, generalized shifted-PMI optimum for observed cells, finite-dimensional approximation, smoothed negative distribution, exact full-rank versus low-rank tests, real-run correlation and matched-book comparison reviewed. Existing checkpoint lineage lead is not duplicated.

sgns_exact measures errors only on observed pairs with count>=5; output cells is that selected count, not all 300^2 cells. Real diagnostic uses pairs>=50 among top2000 words, stats across all eligible pairs but samples at most3000 and draws every second sample. The finite training is 3000 Adam iterations; no convergence certificate is stored. losses[::200] samples actual steps1,201,... while replay labels0,200,... .

Use log-objective rather than loss on the positive-log derivation. Label scatter samples and min-count cohort; expose finite-optimization errors instead of implying a certified complete minimum. Exact scatter clips y to percentile limits but leaves x outside, so native-check panel spill and add overflow counts/markers rather than silently accumulating boundary dots. Real scatter clips both coordinates; mark that policy. Add a visible baseline/theory equality line and robust fixed-column neighbour layout during crossfades. Subsampling changes actual context sequences; disclose it when comparing nominally equal windows.

### 15. HighDim

Gaussian-normalized random directions, angle standard deviations in degrees, heuristic variance derivation plus exact sphere statement, full 10000-direction pairwise maximum, conservative integer angular interval, Gaussian length delta method and uniform-ball shell fraction reviewed.

Angle histogram bins are 5 degrees and heights are fractions of 20k pairs; norm histograms plot |x|/sqrt(d), not raw length, with 20k denominator and finite [0,2] support. Norm spread result is absolute length sd approaching1/sqrt2, distinct from the narrowing normalized histogram. Shell fraction is uniform ball volume1-.99^d, distinct from Gaussian radial mass.

Add normalized-length axis caption and keep Gaussian-length versus uniform-ball transition explicit. In angle sweep dims10 and100 both use bookmark c; native-check that the narration saying100 does not linger on10. Use count/percentage y-axis cue for unlabelled histogram bars. Preserve schematic/exaggerated-shell labels and provide sign-independent angle examples without implying 2D fan angles are the measured 768D geometry.

### 16. JL

Squeeze uses ordinary Euclidean distances and 2000 sampled pairs with one map per k; statement/proof/fine tests use squared distances. Gaussian row projection, chi-square MGF/Chernoff exponent and union-bound pair/two-tail factor reviewed. Classic success>=1/n derivation remains valid; existing confidence-inversion lead is not duplicated.

Squeeze within10 is ordinary-distance relative deviation; fine fail and worst are squared-distance relative deviation. Fine fail stores five map outcomes, averaged in tails; exact_fail is one-pair probability while empirical pairs share each projection and are dependent. Worst display bars are min–max across five maps with mean dot.

Add sampled-pairs/single-map caption on squeeze and make the shift to squared-distance units explicit. Add min–max bands for the five failure-fraction samples already cached, with clear mean-of-five legend. Mark floor-clamped probabilities and omitted worst>1 points; do not imply absent values passed. Preserve no-finite-bound state for parent confidence repair, and show its delta in legend. Annotate the weaker lower-tail bound rather than saying the exact lower-tail expression is the same.

### 17. Geometry

Cosine anisotropy, global centering and top-PC removal, PCA share, vocabulary-ID proxy qualification, layer raw/centered cosines and rogue-coordinate contributions reviewed. Correct-inner-product qualification on linear representation hypothesis is present.

Random tokens are sampled from IDs1000..19999, not uniformly all50257. Histogram range[-.3,.6] omits tails then normalizes included counts. PC covariance uses all token embeddings; top3_share is signed selected-coordinate contribution divided by total estimated cosine, not a fraction of squared variance. Layer peak is currently called top layer (T05).

Label token cohort and clipped histogram mass. Keep vocabulary ID as a rough merge-order proxy, not a measured corpus-frequency rank. Show signed rogue-coordinate contributions if negatives/ratios outside[0,1] occur, and state layer/sample provenance. Check long x-axis normalization caption, token-frequency legend and right-hand rogue-dimension callout in both languages. Add tiny mean-removal/PC-removal diagram for continuity from projection.

### 18. Netflix

Synthetic-world labels, rating matrix/bias-plus-factor model, training versus held-out RMSE in stars, rank/regularizer selection, replay PCA, genre-neighbour metrics and two-tower consumers reviewed. Recall denominator and sampled-logit/prior leads are referenced only.

MF training optimizes raw predictions while evaluation clamps predictions to[1,5]. Lambda0 removes vector penalty only; 0.01 bias penalty remains. Large genre centroids are intentionally magnified2.5x and labeled. Chance genre_nn baseline includes self-probability sum p_c^2 while nearest films explicitly exclude self; exact without-self chance would use (n_c-1)/(N-1), a small finite-population distinction. Final mean/bias baselines and low-rank models use different fitting masks (T07).

Repair data-dependent penalty verdict (T04). Align final baselines to the same fitting data, disclose fixed bias regularization and clipped RMSE. Tie a replay cursor and partially revealed RMSE curves to the same epoch as film vectors; currently complete curves appear before vector replay advances. Add unknown-user5-history input highlight, and label corrected recall/inference branch when parent repairs it. Use separate warm/cold popularity styles or labels to distinguish same-grey dashed lines. All numeric changes require cache versioning and honest rerender, not manual text replacement.

### 19. Outro

Twelve tiles trace actual items; eight problem statements/solutions, payoff part references, illustrative gradient vector field and primary bibliography list reviewed. All tile data are upstream dependencies, so numerical/caption repairs must regress the outro.

SGNS tile depicts generalized shifted-PMI experiment but labels ordinary PMI (T03). Spectra mini-histograms normalize each series by its own maximum, so heights are shape-only and not directly comparable densities. Norms tile has fixed140 y top while full scene uses370; verify actual ranges.

Keep recap qualifier nearly perpendicular and related cooccurrence statistics rather than unconditional perpendicular/same table. Preserve rectangular-SVD/reflection caveat in concise recap wording. Label mini-histograms as separately peak-normalized if comparison scale matters. Increase/verify small tile captions and split dense references into paced pages if native preview cannot read them. Add full-column-rank assumption to projection problem. Ensure all repaired main-scene facts/terms propagate to EN/ZH recap and problem translations.

## Provenance and limits

Exact method line ranges, file SHA256 values and frozen source copies: [ai3-tail-source-review.json](/workspace/runtime/ai3-tail-source-review.json); snapshots under /workspace/runtime/ai3-tail-source-evidence. Tiny fixtures are standalone NumPy only and do not estimate effects in actual production datasets.

- All findings are source-level or tiny synthetic mathematical reproductions. No Part3 production source/helper was imported; fixtures import NumPy only.
- No production data/model/checkpoint was read, generated or downloaded. Actual cache values, affected neighbour words, peak layer, escapee counts and RMSE impacts remain unmeasured.
- No source/test/global caption edits, rendering, playback or audio review. Layout, palette, typography, pacing and animation suggestions remain hypotheses until native EN/ZH renders.
- Existing parent recall/logit/JL-confidence/SGNS-provenance leads and six first-half findings are referenced, not relabeled as new.
- Historical/empirical attributions were checked for internal consistency with README/bibliography only. Primary-source verification remains needed for external claims, including fitted-tail range and accuracy association.
