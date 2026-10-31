# Part3 source preparation: four verified leads

Read-only review completed 2026-10-31T16:27:56.721829+00:00. Repository HEAD `5c59c4d065a707be467358a234131f3662b48c05`.

All four queued leads are supported by source. This is preparation only; no Part3 implementation,compute,rendering or tests were performed. Part3 has19manifestscenes(38bilingualcases). Its local cache directory is absent.

The key distinction: the standalone JL theorem/proof with success probability at least1/n is valid; the separately computed worst-distortion curve inverts a failure bound equal to1, which certifies no positive success probability. SGNS has an unsafe resume contract, but no corrupted checkpoint is established.

## Findings

### recall-at-10-denominator (P1)

Status: source-confirmed-semantic-defect.

Source references: [videos/ai/ai3/compute.py:1445](/workspace/explainer-videos/videos/ai/ai3/compute.py:1445), [videos/ai/ai3/compute.py:1454](/workspace/explainer-videos/videos/ai/ai3/compute.py:1454), [videos/ai/ai3/compute.py:1441](/workspace/explainer-videos/videos/ai/ai3/compute.py:1441), [videos/ai/ai3/s18_netflix.py:262](/workspace/explainer-videos/videos/ai/ai3/s18_netflix.py:262), [videos/ai/ai3/s18_netflix.py:287](/workspace/explainer-videos/videos/ai/ai3/s18_netflix.py:287).

Counterexample: 20 relevant unseen films, all 10 recommendations relevant: current score=1; recall@10=0.5.

**Semantics**

Current helper averages hits/min(|targets|,10) over users with nonempty targets. It is a capped-denominator top-10 retrieval score, not macro recall@10 and not precision@10. True per-user recall is hits/|unique relevant targets|. Ratings-world items are sampled without replacement, so duplicate-target inflation is not established in the present generator.

**Proposed repair**

- Use a pure metric helper with explicit macro-recall definition and target/seen eligibility rules; report evaluated-user/target counts and empty-target handling.
- Use the same metric implementation for raw towers, optional ablation and popularity baseline.
- Retain a differently named capped metric only as an explicit extra; do not keep it under recall fields.
- Update English/Chinese labels, narration and regenerated values; re-evaluate plot limits from corrected data.

**Concrete regression cases to implement**

- 20 targets/10 hits =>0.5; 20 targets/5 hits=>0.25.
- 3 targets/2 hits =>2/3; zero hits=>0.
- Macro average differs from micro on unequal target counts; e.g. users1/2 and10/20 both0.5.
- Deduplicate target identities; reject/document target/seen overlaps and filter seen recommendations.
- Empty-target users excluded consistently, with evaluated count exposed; empty cohort result explicitly unavailable rather than misleading success.
- Same ranking fixture gives consistent raw/prior/popularity metric values.

**Cache and recomputation requirements**

- Invalidate or semantically version twotower.json and any companion arrays whenever metric definition/candidate filtering/splits change.
- Current outputs store aggregate curves and summaries, not per-user rankings or a trained tower checkpoint; exact corrected metrics cannot be reconstructed from old aggregate means.
- An authenticated reusable trained model could permit re-evaluation, but no such artifact is currently returned by compute_twotower; otherwise an authorized training rerun is necessary.


### corrected-sampled-logits-and-prior (P1)

Status: source-confirmed-training-narration-inconsistency.

Source references: [videos/ai/ai3/compute.py:1443](/workspace/explainer-videos/videos/ai/ai3/compute.py:1443), [videos/ai/ai3/compute.py:1468](/workspace/explainer-videos/videos/ai/ai3/compute.py:1468), [videos/ai/ai3/compute.py:1471](/workspace/explainer-videos/videos/ai/ai3/compute.py:1471), [videos/ai/ai3/compute.py:1477](/workspace/explainer-videos/videos/ai/ai3/compute.py:1477), [videos/ai/ai3/compute.py:1492](/workspace/explainer-videos/videos/ai/ai3/compute.py:1492), [videos/ai/ai3/compute.py:1494](/workspace/explainer-videos/videos/ai/ai3/compute.py:1494), [videos/ai/ai3/s18_netflix.py:265](/workspace/explainer-videos/videos/ai/ai3/s18_netflix.py:265), [videos/ai/ai3/s18_netflix.py:271](/workspace/explainer-videos/videos/ai/ai3/s18_netflix.py:271), [videos/ai/ai3/s18_netflix.py:285](/workspace/explainer-videos/videos/ai/ai3/s18_netflix.py:285), [videos/ai/ai3/README.md:85](/workspace/explainer-videos/videos/ai/ai3/README.md:85), [videos/ai/ai3/zh_lines.py:428](/workspace/explainer-videos/videos/ai/ai3/zh_lines.py:428).

Counterexample: p(A|u)=0.6,p(B|u)=0.4 and q(A)=0.1,q(B)=0.9. Raw s=log p ranks A first; adding log q produces masses0.06 and0.36, reversing the ranking.

**Derivation**

- Let s(u,i)=(U·I)/tau and negative sampling marginal q(i). The sampled candidate classifier needs logits log p(i|u)-log q(i)+C(u) under the usual independent-negative idealization.
- Training supplies logits s-log q. Hence its intended raw s is log p(i|u)+C(u), while corrected training logits, not raw s, carry the density-ratio/PMI-like quantity.
- Equivalently q(i)*exp(s-log q(i)) is exp(s), so the implied full-catalog conditional distribution is softmax(s).
- Adding log prior to s at inference multiplies this conditional by the prior again. The implementation uses a smoothed prior, so it is a popularity-weighted empirical ablation, not algebraic recovery of the conditional.
- Finite batches, duplicate-negative masking, target-excluded histories, normalized finite-capacity towers and optimization prevent claiming the actual fitted scores equal this ideal optimum exactly.

**Proposed repair**

- Keep existing sampled-logit correction and recommend using raw tower scores; use current raw-evaluation curve columns2/3 and recall_warm/recall_cold field semantics after correcting recall itself.
- Optionally retain prior-added columns4/5 as a named popularity-prior ablation with separately reported empirical results.
- Alternative: remove training correction and explain raw density-ratio scores plus an inference prior, requiring retraining. Do not mix the two derivations.
- Revise PMI/prior-addback narration in s18_netflix.py, README and zh_lines; regenerate narration captures/translations from changed source.

**Concrete regression cases to implement**

- For positive p,q, corrected candidate logits from s=log p give implied normalized q*exp(logits)=p.
- Hold s fixed and vary q: corrected implied full-catalog probabilities remain softmax(s).
- Use0.6/0.4 vs0.1/0.9 fixture to prove a prior-added branch is a distinct ranking, and ensure default inference chooses intended branch.
- Check selected curve columns/summary names agree with chosen raw or explicitly labeled ablation branch.
- Verify q=0/unseen-item policy and smoothing are explicit; no infinities/NaNs introduced.
- Do not assert neural training exactly reaches the analytic optimum or must beat popularity.

**Cache and recomputation requirements**

- Version twotower objective/inference/metric metadata, including tau, q construction/smoothing, duplicate masking, splits and seeds.
- Choosing raw inference alone does not require a different training objective, but corrected recall still requires new evaluation; present aggregate artifacts cannot support it.
- If training correction changes, invalidate all twotower learned/evaluation outputs and any future checkpoints.


### jl-confidence-bound (P1)

Status: source-confirmed-worst-chart-guarantee-defect-with-valid-classic-theorem.

Source references: [videos/ai/ai3/compute.py:1158](/workspace/explainer-videos/videos/ai/ai3/compute.py:1158), [videos/ai/ai3/compute.py:1161](/workspace/explainer-videos/videos/ai/ai3/compute.py:1161), [videos/ai/ai3/compute.py:1214](/workspace/explainer-videos/videos/ai/ai3/compute.py:1214), [videos/ai/ai3/compute.py:1218](/workspace/explainer-videos/videos/ai/ai3/compute.py:1218), [videos/ai/ai3/s16_jl.py:92](/workspace/explainer-videos/videos/ai/ai3/s16_jl.py:92), [videos/ai/ai3/s16_jl.py:125](/workspace/explainer-videos/videos/ai/ai3/s16_jl.py:125), [videos/ai/ai3/s16_jl.py:214](/workspace/explainer-videos/videos/ai/ai3/s16_jl.py:214), [videos/ai/ai3/s16_jl.py:221](/workspace/explainer-videos/videos/ai/ai3/s16_jl.py:221), [videos/ai/ai3/s16_jl.py:224](/workspace/explainer-videos/videos/ai/ai3/s16_jl.py:224), [videos/ai/ai3/s16_jl.py:230](/workspace/explainer-videos/videos/ai/ai3/s16_jl.py:230), [videos/ai/ai3/zh_lines.py:388](/workspace/explainer-videos/videos/ai/ai3/zh_lines.py:388).

**Derivation**

- Set g(eps)=eps^2/2-eps^3/3 and B=n(n-1)*exp(-k*g(eps)/2). Current inversion sets B=1, so the certified success lower bound1-B is zero.
- The separate classic theorem is valid: k>=4ln(n)/g(eps) yields B<=n(n-1)/n^2=1-1/n and success>=1/n. Do not misreport this part as the same bug.
- For specified0<delta<1, solve B<=delta; target g(eps)>=2ln(n(n-1)/delta)/k. Then success>=1-delta for all squared-distance pairs simultaneously.
- g is increasing on(0,1), with supremum1/6. No epsilon<1 satisfies the bound when the required target is>=1/6; return an explicitly unavailable result.
- All these are probability statements over the projection, not deterministic guarantees for each measured random matrix. The scene separately labels ordinary-distance10% in squeeze and squared-distance distortion in tails/worst; those units should remain explicit.

**Proposed repair**

- Introduce explicit delta in jl_bound_eps and cache metadata; choose and visibly label a meaningful confidence such as95%.
- Either parameterize the theorem/proof display consistently, or retain its classic1/n statement while clearly identifying the separate confidence level in the measured comparison.
- Rename/display unavailable bound points honestly; handle zero finite bound points without next(...)/StopIteration.
- Refresh English/Chinese worst-chart narration and legend; retain measured five-seed spread as measurement, not guaranteed compliance.

**Concrete regression cases to implement**

- For a feasible finite epsilon, recompute logB and require logB<=ln(delta), with monotonic bisection tolerance.
- Tighter delta or larger n cannot reduce epsilon at fixed k; larger k cannot increase it.
- Validate k>0,n>=2,0<delta<1 and finite inputs; define integer constraints.
- At target>=1/6 return unavailable; test the epsilon<1 boundary without an arbitrary0.999 cutoff.
- All unavailable fine-grid bounds must render/format without StopIteration or fabricated guarantee.
- Check classic theorem algebra gives1/n lower success bound, distinct from chosen chart confidence.

**Cache and recomputation requirements**

- Version jl.json bound metadata with delta, squared-relative-error units and formula revision.
- Existing authenticated measured projections/chi-square statistics can be preserved by an explicit cheap derived-bound migration; a bound-only change need not rerun GPT-2/model loading/projections.
- Cached-only QA must reject an old/no-delta item as stale rather than silently migrate or recompute it.
- In this workspace no ai3 cache exists, so there is no local measured artifact to migrate.


### sgns-checkpoint-provenance (P1)

Status: source-confirmed-resume-risk-not-observed-corruption.

Source references: [videos/ai/ai3/compute.py:846](/workspace/explainer-videos/videos/ai/ai3/compute.py:846), [videos/ai/ai3/compute.py:849](/workspace/explainer-videos/videos/ai/ai3/compute.py:849), [videos/ai/ai3/compute.py:960](/workspace/explainer-videos/videos/ai/ai3/compute.py:960), [videos/ai/ai3/compute.py:968](/workspace/explainer-videos/videos/ai/ai3/compute.py:968), [videos/ai/ai3/compute.py:977](/workspace/explainer-videos/videos/ai/ai3/compute.py:977), [videos/ai/ai3/compute.py:998](/workspace/explainer-videos/videos/ai/ai3/compute.py:998), [videos/ai/ai3/compute.py:1002](/workspace/explainer-videos/videos/ai/ai3/compute.py:1002), [videos/ai/ai3/compute.py:1025](/workspace/explainer-videos/videos/ai/ai3/compute.py:1025), [videos/ai/ai3/compute.py:1034](/workspace/explainer-videos/videos/ai/ai3/compute.py:1034), [videos/ai/ai3/compute.py:1049](/workspace/explainer-videos/videos/ai/ai3/compute.py:1049).

**Semantics**

- book_words rebuilds most-common ordered vocabulary from current corpus. Changed corpus/tie order can change token-row meaning while keeping10000rows.
- Resume unconditionally restores embeddings,optimizer,NumPy generator,Torch RNG,loss/snapshot arrays and epoch. No corpus/vocabulary/hyperparameter fingerprint is stored or checked.
- State-dict shape validation can catch a dimension change but cannot catch equal-size row permutation or changes to context/negative-sampling semantics.
- Identical unchanged inputs appear designed to resume correctly: corpus/subsampling sequence is regenerated from the same seed, then post-epoch NumPy/Torch RNG states are restored. This has not been executed here.
- SGNS also compares against independently cached words embeddings using current vocabulary/indices; the existing words.vocab must match exactly before row comparisons.
- Final sgns output lacks a corpus/vocabulary/recipe provenance envelope; fixing only the transient checkpoint would not protect completed-cache reuse.

**Proposed repair**

- Store a checkpoint schema and semantic fingerprint before restoring any model/optimizer/RNG state.
- Fingerprint normalized corpus/token stream, exact ordered vocabulary,subsampled sequence/context recipe,negative distribution and seeds; include VOCAB,DIM,WINDOW,SG_K,SG_B,epoch/checkpoint schedule,optimizer/hyperparameters,dtype and relevant recipe version.
- Classify missing/legacy/mismatched checkpoints explicitly; normal compute may start a fresh authenticated run under the item lock, while retaining/quarantining evidence if useful. Never silently reinterpret rows or partially restore mismatched optimizer/RNG state.
- Apply the same provenance contract to completed words/sgns results; validate exact words.vocab alignment before overlap/neighbour comparisons.
- Keep checkpoint and final item writes atomic/whole-or-absent under a single compute owner; metadata sidecars must authenticate their matching checkpoint bytes.

**Concrete regression cases to implement**

- Equal vocabulary size but swapped row order rejects checkpoint before state restoration.
- Same-sized corpus change,window/K/DIM/batch/seed/negative-distribution change rejects or explicitly starts fresh.
- Legacy metadata-less checkpoint,malformed metadata and inconsistent epoch/snapshot counters handled deterministically.
- Matching metadata restores all model/optimizer/NumPy/Torch state; a tiny isolated interrupted-vs-uninterrupted fixture yields matching next-step behavior.
- words cache ordered-vocabulary mismatch aborts comparison; matching vocabulary passes.
- Cached-only stale/missing completed item never restores a checkpoint or calls book_words/ai1 text loaders that can compute. Mock compute entrypoints to fail if touched.

**Cache and recomputation requirements**

- Version both sgns checkpoint and completed words/sgns lineage. Validate semantic content, not only file existence or array shape.
- Require part-local cache_current(name) and load(name) indirection for cached-only QA, normal compute and CLI to share validation.
- A missing/legacy final artifact is stale; cached-only reports it and never recomputes. Normal authorized compute handles repair under cache lock.
- No local .cache/ai3 or sgns.ckpt exists; current checkpoint corruption is not established.

## Shared cache contract

- Current ai3 compute.py53–54 uses base Cache and bound load alias; no cache_current/schema/lineage validation is present.
- Base Cache.load75–95 computes missing data; Cache.main130–137 skips any existing JSON. Both paths need item-local semantic validation for the repaired items.
- Use a dynamic def load(name):return CACHE.load(name) wrapper so qa_series cached-only instance guard can intercept before a schema-upgrade loader computes.
- Existing qa_series.py301–309 checks cache_current only when a part exposes it; Part2 SchemaCache/current/load implementation offers a local pattern without changing global cache semantics.
- Expose stale-vs-missing outcomes with exact item/reason; do not equate completed JSON or successful process exit with valid scientific semantics.
- Update EN/ZH generated narration and text tables after source changes; preserve old artifacts and measured-data provenance rather than manually replacing numbers.

## Next sequential validation

1. After Part2 rendered review closes, implement pure metric/probability/provenance validators and focused tests first.
2. Add cache schema/lineage enforcement and cached-only stale/no-compute tests before any production data work.
3. Have one compute owner rebuild only affected measured items and dependencies with logs/fingerprints; never render while prerequisites are being written.
4. Proceed sequentially through all19Part3scenes, beginning Hook; review revised SGNS,JL,Netflix and recap consumers when reached.
5. Run EN/ZH endpoints then dense time-indexed motion review,narration/audio alignment where available; retain continuous-playback limitation.

## Provenance and limits

README documents roughly50minutes of content and1–2CPUhours of numerical precompute, not measured here. Additional bilingual rendering/audio QA cost remains unmeasured.

Compute source SHA256 `c2b214d772419593c484487120966dc05fea9287199c3e4a0472ab90c0efda34`. All supporting file hashes are retained in companion JSON.

- Read-only source inspection and symbolic derivations only; no production data/model computation,no ai3 imports,checkpoint deserialization,network,rendering or tests executed.
- No repository source/tests/global tables edited in this preparation task.
- No claim of actual training performance changes,checkpoint corruption,rendered layout quality,full playback or listening.
- The four leads are verified; other Part3 source/factual/visual behavior is not comprehensively audited.
