# Residual review fixes

The Part3 README now describes finite SGNS optimization against the generalized target, and raw conditional-score two-tower inference. Empty/unavailable retrieval cohorts now branch before comparisons, omit missing curves/baselines and report eligibility counts. Six tests execute the actual complete scene with drawing stubs; ten narration tests cover the independently translated availability/outcome branches and literal summary delimiter. These are conditional fixtures, not claims that default cohorts are empty. Actual default-data/layout rendering remains pending data generation.

A real caption-import mistake exposed that the merge helper accepted nested metadata as translation values. The table was corrected immediately; no dataset/model input changed. The helper now validates supported shapes before any write. Seven actual CLI tests cover rejection without writes, valid merges, literal caption keys, conflict handling and concurrency. Existing failed/in-flight captures stay historical and are rerun.

The actual bilingual branch regression is now included in `tests/test_ai3_narration_review.py` at commit `a276671`; it was accidentally omitted from the preceding source-fix push. The published rerun receipt records all ten narration tests passing, including seven availability/outcome combinations and the exact nested summary delimiter.
