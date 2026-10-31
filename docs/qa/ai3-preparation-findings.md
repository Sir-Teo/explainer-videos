# Part 3 original source leads and disposition

Parent read-only review at c73844a supplied these original leads. All four were independently verified and repaired in implementation commit `4a20866`; actual regression evidence is in [the source-review package](evidence/ai3-source-review/). This retained list records the original hypotheses rather than current unfixed defects. Default affected-data recomputation and rendered verification continue under the sequential Part 3 queue.

- Recall@10: compute.py1454 divides hits by min(number of targets,10), while s18_netflix.py262/287 calls the value
  recall or share of held-out favorites. Twenty relevant films and ten hits yields1.0 instead of standard recall.5.
  Verify and test the metric/labels, then regenerate affected measured outputs with provenance.
- Two-tower correction: training logits s−log q at compute.py1492–1494 imply raw s estimates log conditional item
  probability, rather than PMI. compute.py1471–1479 and scene285–287 reportedly add popularity back, potentially
  double-counting the prior. Verify derivation/data; choose consistent inference or label an empirical ablation.
- JL confidence: jl_bound_eps at compute.py1158–1171 solves a union failure bound equal to1, yielding only a trivial
  success lower bound. s16_jl.py221/230–231 reportedly presents it as a promised distortion. Introduce explicit
  confidence delta in n(n−1)exp(−k g(epsilon)/2)≤delta or label the threshold correctly, without a deterministic guarantee.
- SGNS resume: checkpoint load at compute.py998–1007 lacks corpus/ordered-vocabulary/hyperparameter fingerprints,
  while book_words846–851 rebuilds ranked vocabulary. Equal vocabulary lengths can conceal changed row meanings.
  Verify legacy/mismatch handling and cached-only behavior before restoring or recomputing. Current corruption is
  not established by the source finding alone.

The repair batch covers the standard recall denominator, raw conditional-score inference, explicit 95% JL-confidence bounds and schema/lineage-validated SGNS resumes. Empty-cohort scene and bilingual narration branches have additional executed regressions. The first nine data-ready scenes have bilingual endpoint review; later affected scenes remain pending real input completion. This source-lead list alone supplies no playback or listening approval.
