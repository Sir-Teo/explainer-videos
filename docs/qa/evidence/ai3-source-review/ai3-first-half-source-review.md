# Part 3 first-half source review

Read-only first 10 of 19 Part 3 manifest scenes, rounding first half upward; Hook through Norms. Source derivations/semantics and visual-validation queue only.

Completed 2026-10-31T16:40:03.901681+00:00; branch `qa/ai-series-cloud-20261031`, observed HEAD `5c59c4d065a707be467358a234131f3662b48c05`. No repository edits, Part 3 imports, data/model work or renders.

Manifest has 19 scenes. This review takes positions 1–10 (Hook through Norms); Spectra through Outro remain outside this assignment. The four parent leads on recall, sampled logits, JL confidence and SGNS provenance are retained separately.

## Inventory

| Position | Scene | Source | Cache dependencies |
|---:|---|---|---|
| 1 | Hook | videos/ai/ai3/s01_hook.py | gpt2 |
| 2 | Vectors | videos/ai/ai3/s02_vectors.py | gpt2 |
| 3 | Einsum | videos/ai/ai3/s03_einsum.py | einsum |
| 4 | Matrices | videos/ai/ai3/s04_matrices.py | none directly |
| 5 | Projection | videos/ai/ai3/s05_projection.py | project |
| 6 | Eigen | videos/ai/ai3/s06_eigen.py | none directly |
| 7 | Power | videos/ai/ai3/s07_power.py | power |
| 8 | SVD | videos/ai/ai3/s08_svd.py | none directly |
| 9 | LowRank | videos/ai/ai3/s09_lowrank.py | image, letters |
| 10 | Norms | videos/ai/ai3/s10_norms.py | depth, galore, norms |

## New source findings

### AI3-FH01 — Attention head-merge einsum introduces absent output index (P1)

source-confirmed-notation-defect; standalone NumPy reproduction passed; unrendered.

bhqe,hed->btd rejects output subscript t absent from all inputs; corrected bhqe,hed->bqd yields shape (2,4,6), exactly matching flatten-heads matrix multiplication in the tiny fixture.

References: [videos/ai/ai3/s03_einsum.py:174](/workspace/explainer-videos/videos/ai/ai3/s03_einsum.py:174), [videos/ai/ai3/s03_einsum.py:171](/workspace/explainer-videos/videos/ai/ai3/s03_einsum.py:171).

Proposed repair: Use bhqe,hed->bqd consistently with prior query-index row, or consistently rename q to t on input/output rows. Add a focused all-four-contractions shape fixture. Refresh EN/ZH on-screen text if needed; do not alter measured MAC counts.

Tiny reproduction key: `attention_einsum` in [ai3-first-half-symbolic-fixtures.json](/workspace/runtime/ai3-first-half-symbolic-fixtures.json).

Render verification queue: Four-row attention notation reveal/hold in EN/ZH; No new clipping after string change; Index color and kept/summed explanations agree.

### AI3-FH02 — Antiparallel Cauchy-Schwarz equality is outside the displayed parabola domain (P2)

source-confirmed-geometry-coverage-defect; symbolic reproduction; unrendered.

a=(2.4,0), |b|=1.3. At animated theta=pi the zero/vertex is t=-2.4/1.3=-1.846153846, outside [-0.5,3.5]. The example shows the positive-alignment equality but cannot show its antiparallel counterpart.

References: [videos/ai/ai3/s02_vectors.py:182](/workspace/explainer-videos/videos/ai/ai3/s02_vectors.py:182), [videos/ai/ai3/s02_vectors.py:196](/workspace/explainer-videos/videos/ai/ai3/s02_vectors.py:196), [videos/ai/ai3/s02_vectors.py:228](/workspace/explainer-videos/videos/ai/ai3/s02_vectors.py:228), [videos/ai/ai3/zh_lines.py:60](/workspace/explainer-videos/videos/ai/ai3/zh_lines.py:60).

Proposed repair: Extend to a symmetric t domain containing +/-2.4/1.3 and update the plotted clipping calculations together, or explicitly select/reframe the equality demonstration. Preserve discriminant reasoning and negative cosine readout.

Tiny reproduction key: `cauchy_schwarz_chart` in [ai3-first-half-symbolic-fixtures.json](/workspace/runtime/ai3-first-half-symbolic-fixtures.json).

Render verification queue: Both aligned and antiparallel vertices visible at zero; Parabola stays within axes/frame for entire theta sweep; Negative t axis labels and formula do not collide.

### AI3-FH03 — Muon replay starts from a different normalization than its actual recorded step zero (P2)

source-confirmed-chart-replay-inconsistency; symbolic reproduction; unrendered.

g_sv=s/sigma1 is shown while counter says Newton-Schulz step 0. Actual history ns[0] comes from G/(||G||_F+1e-7); loop skips ns[0] and transforms to ns[1]. For spectrum [4,3], displayed initial values [1,.75] differ from actual approximately [.8,.6].

References: [videos/ai/ai3/s10_norms.py:208](/workspace/explainer-videos/videos/ai/ai3/s10_norms.py:208), [videos/ai/ai3/s10_norms.py:224](/workspace/explainer-videos/videos/ai/ai3/s10_norms.py:224), [videos/ai/ai3/s10_norms.py:227](/workspace/explainer-videos/videos/ai/ai3/s10_norms.py:227), [videos/ai/ai3/s10_norms.py:258](/workspace/explainer-videos/videos/ai/ai3/s10_norms.py:258), [videos/ai/ai3/compute.py:803](/workspace/explainer-videos/videos/ai/ai3/compute.py:803), [videos/ai/ai3/compute.py:812](/workspace/explainer-videos/videos/ai/ai3/compute.py:812), [explainer/lm/pocket.py:211](/workspace/explainer-videos/explainer/lm/pocket.py:211).

Proposed repair: Start the iteration curve from ns[0]. Retain g_sv for the relative-to-largest statistic or as a separately labeled reference with explicit scale. No training rerun is needed if authentic ns[0] history already exists.

Tiny reproduction key: `muon_step_zero_scale` in [ai3-first-half-symbolic-fixtures.json](/workspace/runtime/ai3-first-half-symbolic-fixtures.json).

Render verification queue: Counter 0 corresponds exactly to ns[0]; Each counter k corresponds to ns[k]; Reference and iteration curve normalization labels remain visible; Check actual iteration values against y-axis bounds.

### AI3-FH04 — Stable-rank narration claims matched random shapes but computes one MLP-shaped reference (P2)

source-confirmed-comparison-design/wording-mismatch; measured results not executed.

Only a 768x3072 random matrix is computed, while trained categories include 768x768 and 768x2304. The scene identifies the single reference correctly, but the conditional verdict says every trained kind is below a random matrix of the same shape. Aspect ratio changes expected stable rank (source formula gives about 192 square, 309 attention-in, 341 MLP), so one threshold does not establish all matched-shape comparisons.

References: [videos/ai/ai3/s10_norms.py:10](/workspace/explainer-videos/videos/ai/ai3/s10_norms.py:10), [videos/ai/ai3/s10_norms.py:73](/workspace/explainer-videos/videos/ai/ai3/s10_norms.py:73), [videos/ai/ai3/s10_norms.py:88](/workspace/explainer-videos/videos/ai/ai3/s10_norms.py:88), [videos/ai/ai3/compute.py:512](/workspace/explainer-videos/videos/ai/ai3/compute.py:512), [videos/ai/ai3/zh_lines.py:214](/workspace/explainer-videos/videos/ai/ai3/zh_lines.py:214).

Proposed repair: Either qualify the verdict to the displayed MLP-shaped reference, or compute/store appropriately matched baselines and draw them with explicit category/shape provenance. Do not state a measured matched-shape conclusion without those data.

Tiny reproduction key: `random_stable_rank_theory` in [ai3-first-half-symbolic-fixtures.json](/workspace/runtime/ai3-first-half-symbolic-fixtures.json).

Render verification queue: Reference line labels match real shape(s); Narration branches match chosen comparison; Legend/reference lines remain distinguishable in EN/ZH.

### AI3-FH05 — Power-rate two-decimal agreement predicate does not imply displayed decimal equality (P2)

source-confirmed-conditional-wording-defect; actual production branch/result unverified.

abs(rate-ratio)<.01 does not establish equality rounded to two decimal places: .244 and .253 differ by .009 yet format as .24 and .25. No Part 3 cached rates were loaded.

References: [videos/ai/ai3/s07_power.py:147](/workspace/explainer-videos/videos/ai/ai3/s07_power.py:147), [videos/ai/ai3/zh_lines.py:161](/workspace/explainer-videos/videos/ai/ai3/zh_lines.py:161).

Proposed repair: Say within 0.01 under the current predicate, or compare the intended formatted/rounded values explicitly. Preserve data-dependent verdicts and translation.

Tiny reproduction key: `decimal_agreement` in [ai3-first-half-symbolic-fixtures.json](/workspace/runtime/ai3-first-half-symbolic-fixtures.json).

Render verification queue: Displayed rates and spoken verdict agree for actual cached data; Longer revised legend/verdict fits EN/ZH.

### AI3-FH06 — Spectral-theorem summary should say an orthonormal eigenbasis (P2)

source-confirmed-mathematical-qualification-opportunity; proof already has distinct-eigenvalue condition; unrendered.

Summary says eigenvectors are perpendicular without the repeated-eigenvalue qualification, whereas the proof correctly qualifies distinct eigenvalues. Identity matrix eigenvectors (1,0) and (1,1) are not perpendicular; a symmetric matrix admits an orthonormal eigenbasis.

References: [videos/ai/ai3/s06_eigen.py:87](/workspace/explainer-videos/videos/ai/ai3/s06_eigen.py:87), [videos/ai/ai3/s06_eigen.py:110](/workspace/explainer-videos/videos/ai/ai3/s06_eigen.py:110), [videos/ai/ai3/s06_eigen.py:123](/workspace/explainer-videos/videos/ai/ai3/s06_eigen.py:123), [videos/ai/ai3/zh_lines.py:138](/workspace/explainer-videos/videos/ai/ai3/zh_lines.py:138).

Proposed repair: Use admits an orthonormal eigenbasis in theorem/summary and Chinese counterpart; retain correct distinct-eigenvalue proof. Do not imply the existing spectral decomposition or illustrative distinct-eigenvalue matrix is wrong.

Tiny reproduction key: `repeated_eigenvalue` in [ai3-first-half-symbolic-fixtures.json](/workspace/runtime/ai3-first-half-symbolic-fixtures.json).

Render verification queue: Revised theorem card still fits EN/ZH; Summary and proof assumptions agree.

## Chapter checks and visual enhancement queue

### 1. Hook

Context-island motivation to GPT-2 cloud, coordinate barcodes, history and course map. PCA shadow qualification and timeline not-to-scale annotation are explicit.

Cloud label/leader interactions with top-left category legend during rotation and animal zoom need native render review; labels avoid each other but legend is not a declared obstacle. Barcode signs have position/color encoding; add concise sign/magnitude key if previews lack one. Consider local roadmap enlargement only after measuring EN/ZH bounds, as in Part 2.

### 2. Vectors

Arrow/list equivalence, vector arithmetic/basis, law-of-cosines expansion, Cauchy-Schwarz discriminant with b=0 handled in narration, cosine examples and tied logits reviewed.

Cauchy-Schwarz antiparallel equality is outside the selected t domain (finding FH02). Check diagram/ladder gutters and 768-tick barcode aliasing at native preview size. Logit bars use a best-minus-1.5 floor and clamp lower bars; annotate that shifted/clipped display rather than imply raw positive heights. No claim that current unknown logits actually hit the clamp.

### 3. Einsum

Named axes, kept/summed-index rule, six examples, attention contractions and matrix-chain cost formulas reviewed. Chain MAC counts are 40,000,000 versus 800,000 (50x) directly from declared shapes.

Fix invalid output subscript (FH01). Make the projection row label state Q/K/V plus output projection (4 total); check its long left label and numeric right label at native EN/ZH sizes. Preserve per-index colors and align table baselines.

### 4. Matrices

Column images and numeric [1,2] to [0,3] example, noncommutative shear/rotation, determinant/signed orientation, rank-one/null direction and rank-nullity reviewed. The null direction [1,-2] is correct.

Add or retain an explicit oriented-area qualifier in determinant narration: area is absolute determinant; existing on-screen note already uses absolute value. Check column-space/null-space note cards against long crossing lines and composition history-card transition.

### 5. Projection

Line projection, full-column-rank normal equations and projector, seeded illustrative fit, residual checks, Gram-Schmidt/QR and Hilbert stability comparison reviewed. Independent-column and nonzero assumptions are present.

Two log-log stability panels have small 20-point multi-line legends; prioritize panel width/gutters and stable below-axis caption space in EN/ZH renders. Keep the schematic label on the perspective-plane diagram. Guard future normal-equation numerical failure as an observed pathology, not fabricated finite data; no such failure was executed here.

### 6. Eigen

Non-symmetric eigenlines, symmetric decomposition, real/distinct-eigenvalue/orthogonal-complement proof, Rayleigh quotient and illustrative covariance/PCA reviewed. Distinct-eigenvalue qualification is correct in proof.

Qualify summary wording to an orthonormal eigenbasis (FH06). Check finite-sample centering: np.cov centers X but projected points use x dot top through the origin; explicitly center the illustrative cloud if showing PCA reconstruction. This is a source consistency opportunity, no measured offset/render defect established.

### 7. Power

Live positive symmetric example, dominant-eigenvalue and nonzero-start assumptions in derivation, geometric angular bound, doubled Rayleigh rate, measured cache consumers and applications reviewed.

Live intro says start anywhere while derivation correctly requires a nonzero dominant component; align introductory wording. Replace blanket no-formula wording with no general formula in radicals. Label measured sin-angle versus dashed tan upper bound explicitly, and fix the two-decimal predicate (FH05).

### 8. SVD

Positive-determinant example explicitly uses rotations; general narration permits reflection and rectangular projection. A^T A positivity, nonzero singular-value division and basis completion, orthogonality, spectral norm sweep reviewed.

Keep generality note legible while the ellipse/diagram moves. The moving graph dot wraps its x coordinate at exactly 2pi; check final hold for an unwanted right-to-left jump before deciding whether to clamp to endpoint. No rendered jump claimed.

### 9. LowRank

Rank-one pieces, Weyl-based Eckart-Young lower bound and attained tail, image storage/error calculations, square-root letter table, correspondence-analysis normalization and applications reviewed.

Clarify rank-one square-root table as a separable approximation, rather than the product of original marginals; fixture shows the distinction, while the rank-one/Eckart-Young calculation itself is valid. Add tiny row+column previous/next axis cues to the letter heatmaps; 11-point row letters are a readability risk. Check clamped negative reconstruction cells and quantized/clipped displayed images against unclipped float-error claims; clearly label the numeric error as raw SVD error.

### 10. Norms

Frobenius/spectral inequalities, nonzero stable rank, all 48 weight consumers, depth illustration, perturbation inequality and Muon dual-norm derivation reviewed.

Fix Muon step-zero scale and random-reference wording (FH03/FH04). Use a thin-SVD qualifier for rectangular UV^T. Check the fixed y tops and any capped float32 error values with explicit overflow markers rather than silently flattening actual large errors. Keep step labels and original-gradient reference scales explicit.

## Important interpretation limits

The square-root-table fixture distinguishes a best separable approximation from independence formed from original marginals. It does not establish an error in the SVD or Eckart–Young computation. Similarly, the eigenvector example qualifies summary wording; the existing proof already correctly states the distinct-eigenvalue condition. All proposed typography, spacing, sign keys, palette cues and transition changes require actual EN/ZH render verification before being called visual improvements.

Exact method line ranges, source SHA256 values and source snapshots are in [ai3-first-half-source-review.json](/workspace/runtime/ai3-first-half-source-review.json); source copies are under /workspace/runtime/ai3-first-half-source-evidence. The standalone NumPy script/output includes the requested invalid/corrected attention contraction and five tiny mathematical counterexamples.

- No Part 3 scene, common module, compute module or loader was imported; the standalone fixtures import NumPy only.
- No measured data loaded, generated or downloaded; no model/training/checkpoint work.
- No Part 3 render or audio/playback validation. Readability and transition opportunities remain hypotheses until actual EN/ZH output is reviewed.
- Historical attributions are cross-checked for internal agreement with README/reference list only; no independent primary-source historical audit performed.
- Source review of the remaining nine scenes is outside this first-half assignment. Prior four parent findings are referenced, not duplicated as new.
