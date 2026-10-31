# Part3 cross-chapter educational continuity review

Source-only review of19 manifest scenes,38 first/last main narration blocks in EN/ZH,17 chapter-intro calls, recap/payoff/problem/next/reference sections,31 current manifests (553 entries), the Part3 README, series syllabus and working guide. No source edits, compute, scene/model/cache loads, renders or listening.

## Findings

### C1 · medium · concrete mathematical scope mismatch in a chapter-to-chapter callback

Chapter8 proves unregularized full-matrix Frobenius rank-k approximation. The currently visible Netflix problem adds vector and bias penalties. Full observation alone does not turn that penalized objective into the unregularized truncated-SVD problem. The on-screen generic full-table caption is true in isolation, but the voiceover connects it directly to the shown regularized problem without a qualifier.

- `videos/ai/ai3/s18_netflix.py:135`: \Big[(r_{ui} - \hat r_{ui})^2 + \lambda\big(|\mathbf{p}_u|^2 + |\mathbf{q}_i|^2\big) + 0.01(b_u^2+b_i^2)\Big]
- `videos/ai/ai3/s18_netflix.py:153`: A full table would have chapter eight's answer; with holes there is no formula, and we descend the gradient.
- `videos/ai/ai3/s09_lowrank.py:84`: If B has rank at most k, then ||A-B||_F >= ||A-A_k||_F; A_k keeps the k biggest pieces.

Even without biases, the full scalar table [a] with vector penalty has minimum over x=pq of (a-x)^2+2 lambda |x|, because min_{pq=x}(p^2+q^2)=2|x|. For a>lambda>0 its optimum is x=a-lambda; unregularized rank1 SVD returns x=a. This is an algebraic counterexample, not a production experiment.

Proposed qualification for parent review: For an unregularized full-table approximation, chapter eight gives the answer; with missing ratings we optimize the observed entries.
Chinese: 不加正则化、对完整表做低秩近似，第8章就给出了答案；有缺失评分时，我们只在已观测的格子上优化。

### C2 · low · educational abstraction/absolute wording issue; no observed numerical defect

Part1 explicitly has several letter-context counters and a word-context sample; the actual bridge is from exact-context statistics to learned semantic sharing. Hook correctly starts with letters/contexts, while Words changes this to every word as its own island. Literal shared suffixes and short-order counts do transfer between the two example phrases, so taught nothing about is too absolute if read literally. The intended lack of semantic transfer is sound. Chinese mirrors the same abstraction and absolute statement; this is not an isolated translation omission.

- `videos/ai/ai3/s01_hook.py:31`: Every context was its own island. Reading the dog barked a hundred times taught it nothing about the hound barked.
- `videos/ai/ai3/s13_words.py:49`: Part 1's counting model treated every word as an island.
- `videos/ai/ai1/s10_counting.py:68`: Pick each letter by what followed the previous one in our books ... Six: phrases ... Count whole words instead, and it almost scans.
- `videos/ai/ai1/compute.py:316`: Counts of (context of order symbols, next symbol); probabilities with add-alpha smoothing.

Proposed qualification for parent review: Part 1 shared exact patterns by counting, but did not learn that dog and hound are related in meaning.
Chinese: 第1部分靠计数共享完全相同的模式，却没有学会dog和hound在意义上相近。

### C3 · low · optional cross-part unit clarification, not a wrong current equation

Part1 measures surprise/information in bits, while Part3 PMI examples and logistic dot-product identities use natural logarithms. Words says Part1's way without naming this base change. The SGNS e^x identity makes its convention mathematically inferable; counted and learned Part3 targets agree. An ln/nats note would prevent cross-part numerical-unit confusion. No production data was loaded or recomputed.

- `videos/ai/ai3/s13_words.py:79`: PMI(w,c)=log(P(w,c)/(P(w)P(c))); Part 1's way
- `videos/ai/ai3/compute.py:1100`: np.log(...) is used for counted PMI and generalized shifted-PMI targets
- `videos/ai/ai1/compute.py:343`: -log2 P(...)

Proposed qualification for parent review: Here log means the natural logarithm; Part1 used base2 to measure bits.
Chinese: 这里log指自然对数；第1部分用以2为底的对数来量比特。

### D1 · informational · stale draft/planning wording, not a rendered continuity failure

The syllabus still describes the old20-part baseline as current. All31 current manifest files exist with553 scene entries, and the syllabus itself supplies the correct20-to31 mapping. Treat4.9h/26h as historical/planned text, not measured durations of the current31 source manifests. This review does not establish current runtime or lecture-length compliance.

- `videos/ai/SYLLABUS.md:6`: Currently the twenty parts total about 4.9 hours. This plan totals about 26 hours across 31 parts.

## Actual chapter coverage

|Scene|First main narration|Last main narration|Construct methods|
|---|---|---|---|
|Hook|`videos/ai/ai3/s01_hook.py:30`|`videos/ai/ai3/s01_hook.py:223`|islands, cloud, barcodes, era, plan|
|Vectors|`videos/ai/ai3/s02_vectors.py:58`|`videos/ai/ai3/s02_vectors.py:342`|arrows, two_moves, law_of_cosines, cauchy_schwarz, words, logits|
|Einsum|`videos/ai/ai3/s03_einsum.py:72`|`videos/ai/ai3/s03_einsum.py:251`|tensors, convention, examples, attention, order|
|Matrices|`videos/ai/ai3/s04_matrices.py:24`|`videos/ai/ai3/s04_matrices.py:198`|moving, columns, composition, determinant, rank|
|Projection|`videos/ai/ai3/s05_projection.py:60`|`videos/ai/ai3/s05_projection.py:280`|line, subspace, fit, gram_schmidt, stability|
|Eigen|`videos/ai/ai3/s06_eigen.py:43`|`videos/ai/ai3/s06_eigen.py:242`|stay_put, symmetric, proof, rayleigh, pca|
|Power|`videos/ai/ai3/s07_power.py:52`|`videos/ai/ai3/s07_power.py:195`|live, derive, measured, uses|
|SVD|`videos/ai/ai3/s08_svd.py:54`|`videos/ai/ai3/s08_svd.py:168`|three_moves, derive, norm|
|LowRank|`videos/ai/ai3/s09_lowrank.py:65`|`videos/ai/ai3/s09_lowrank.py:272`|pieces, proof, mosaic, letters, vowels, today|
|Norms|`videos/ai/ai3/s10_norms.py:44`|`videos/ai/ai3/s10_norms.py:243`|two_sizes, gpt2, depth, condition, muon|
|Spectra|`videos/ai/ai3/s11_spectra.py:60`|`videos/ai/ai3/s11_spectra.py:216`|law, trained, tails, novels|
|GaLore|`videos/ai/ai3/s12_galore.py:50`|`videos/ai/ai3/s12_galore.py:293`|derive, measured, method, compare, lora|
|Words|`videos/ai/ai3/s13_words.py:48`|`videos/ai/ai3/s13_words.py:264`|history, table, neighbours, directions, analogy|
|SGNS|`videos/ai/ai3/s14_sgns.py:41`|`videos/ai/ai3/s14_sgns.py:301`|game, replay, derive, exact, real, compare|
|HighDim|`videos/ai/ai3/s15_highdim.py:37`|`videos/ai/ai3/s15_highdim.py:177`|angles, orthogonal, room, lengths|
|JL|`videos/ai/ai3/s16_jl.py:89`|`videos/ai/ai3/s16_jl.py:281`|squeeze, statement, proof, tails, worst|
|Geometry|`videos/ai/ai3/s17_geometry.py:45`|`videos/ai/ai3/s17_geometry.py:184`|anisotropy, directions, layers, linear|
|Netflix|`videos/ai/ai3/s18_netflix.py:111`|`videos/ai/ai3/s18_netflix.py:435`|prize, model, replay, ranks, towers, today|
|Outro|`videos/ai/ai3/s19_outro.py:134`|`videos/ai/ai3/s19_outro.py:259`|recap, payoffs, problems, next_time, references|

All38 first/last expressions match local Chinese prefixes; bookmark sequences and placeholder-expression roles match in all38. No new runtime translation or conditional-data branch resolution is claimed. Exact EN expressions, Chinese text, SHA hashes and reference lines are in `extracted-source-with-zh.json`; complete structural checks and31 manifest contents/hashes are in `structural-checks.json`.

## Transitions and prerequisites

- **Hook → Vectors:** Promised chapter1 similarity measure is delivered by dot product, Cauchy–Schwarz and GPT2 cosine examples. Word/token simplification is corrected by explicit50257-token/768-coordinate disclosure in Hook; exact-context/semantic-sharing qualification remains C2.
- **Vectors → Einsum:** Numeric lists and dot products expand into named tensor axes; GPT2 tied-score softmax callback has a real Part1 likelihood/score introduction. Attention is explicitly a Part13 forward use.
- **Einsum → Matrices:** Contraction-order cost ends the tensor chapter; matrix chapter restarts with linear maps. Computational association order and noncommuting map composition are different uses of order, with explicit examples rather than contradictory claims.
- **Matrices → Projection:** Rank/column/null spaces are introduced before projection onto the column space; full-column-rank condition for inverse is stated in the subspace block.
- **Projection → Eigen:** Orthonormal bases and QR stability precede symmetric-matrix eigenbases. No forward prerequisite was silently substituted for the projection result.
- **Eigen → Power:** Covariance/Rayleigh/PCA directions motivate computing a dominant eigenvector. Power explicitly supplies a nonzero dominant component, with the particular symmetric example; near-orthogonality callback goes to actual chapter14.
- **Power → SVD:** Symmetric eigenvector methods lead to the nonsymmetric/rectangular SVD. SVD opener explicitly allows reflections; no assumption all coordinate changes are rotations.
- **SVD → LowRank:** Singular stretches and spectral norm lead to rank-one pieces and Eckart–Young. Chapter8 points forward to chapter9 for Frobenius/singular-value identity; chapter9 explicitly pays off this missing step.
- **LowRank → Norms:** Rank approximation feeds Frobenius/spectral norm/stable rank. Chapter12 word-counting, Part15 bottleneck and Part27 LoRA callbacks match current manifests; LSA historical word-document example differs openly from the later word-context experiment.
- **Norms → Spectra:** Norms uses one MLP-shaped random reference, with shape qualifier; Spectra names the same random-matrix shape and compares eigenvalue distributions of trained versus shuffled weights. Random reference is not called a universal shape-matched control.
- **Spectra → GaLore:** Weights and their spectra are distinguished from gradients and their spectra. GaLore opener says often approximately low rank and explicitly defers chain-rule construction to Part4. No title-level rank assertion was treated as an independent theorem.
- **GaLore → Words:** Return from low-rank training to semantic representation is a topical cut. LoRA rank-limited total change and moving-window accumulated changes are separate. Root owns the currently refreshed GaLore qualification review; this text check does not replace that render check.
- **Words → SGNS:** Same novels/vocabulary and nominal window connect counting to guessing; SGNS explicitly notes subsampling changes the effective context stream. Ordinary PMI versus smoothed generalized target is stated; finite optimization is not presented as theorem-certified convergence.
- **SGNS → HighDim:** Static100-coordinate learned/count vectors transition to768-dimensional GPT2 examples. The latter dimension is named, so it is not implicitly the dimension of the local SGNS run. Two training vectors per word versus one chosen static representation is a conventional abstraction, not automatically a contradiction.
- **HighDim → JL:** Concentration motivates projection. JL opener labels ordinary-distance empirical errors; theorem/tail sections explicitly switch to squared-distance errors; final confidence comparison is separated from existence theorem.
- **JL → Geometry:** Nearly perpendicular independent random directions are contrasted with learned anisotropic token vectors. Geometry identifies its restricted sampled token-ID range and full-vocabulary centering mean, so these are not presented as the same sampling population.
- **Geometry → Netflix:** Meaningful directions and prior analogy are revisited before an explicitly synthetic user/film world. Netflix historical prize data is separated from4000/1200 local synthetic data. The chapter8 regularized/unregularized callback remains C1.
- **Netflix → Outro:** Recap uses12 selected results rather than promising17 one-per-chapter tiles. Synthetic low-rank completion is generalized as helpful rather than guaranteed; generalized shifted PMI, reflections and probability qualifiers survive the recap.
- **Outro → Part4:** Next-part title Change and number4 match current manifest. Taking gradients on trust is explicitly disclosed before the next derivative/chain-rule/autodiff part; Part4 opener independently recalls Part1 score derivative, so no Part2/old-renumbering collision was found.

## Payoffs and problems

Chapter references1,8,9,12,14 match the current17 numbered chapters. Later uses in Parts4,9,11,13,14,15,27,29,30 agree with current manifest subjects. No stale20-part renumbering was found in those lesson references. Part2 is a historical interlude, so Part3 recalling Part1 does not imply a missing prerequisite.

All8 displayed problems map to8 EN and8 ZH README solutions: triangle inequality, full-rank projection, Rayleigh expansion, norm inequalities, SGNS scalar optimum, random-direction variance, chi-squared Chernoff proof, rank-k storage/error. This verifies their correspondence and prerequisite coverage, not a new full independent solution audit.

## Coverage limits

- No production compute, model/scene imports, cache loads, renders, audio or movie playback performed.
- No claim about actual timing, pronunciation, listening quality, measured current part duration, encoded assembly continuity, frame geometry or production fingerprints.
- Only first/last main narration blocks, chapter intros, explicit reference lines and selected supporting middle blocks were substantively read;94 main blocks inventoried does not mean all94 newly reviewed in full.
- Cross-part destinations checked against31 manifests plus bounded supporting source for Part1/Part4/Part15/Part29; not a full factual review of future parts.
- Historical/primary papers were not reverified by this continuity pass; no new niche historical claim asserted.
- GaLore qualifications are the parent’s current source/render batch, separately reviewed; source hashes identify the exact text snapshot here.
- Conditional numeric results in first/last source expressions are reviewed as templates/roles, not newly resolved current-cache results.
- Source changes require parent review; this task writes runtime evidence only.
