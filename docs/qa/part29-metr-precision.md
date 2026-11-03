# Part 29: pinned METR precision follow-up

This is a new independent correction, not recovery of the unavailable old handoff.
The public YAML was retrieved on **3 November 2026 at 00:33:01.452530 UTC**:
https://metr.org/assets/benchmark_results_1_1.yaml

SHA-256: `aae31902b0519a4da73e16643915e5e8aca13cd3315c3aac893ce3d6dfe92ad9`.
This does **not** establish identity with any October 29 historical download.
The source and public-facts regression fixture preserve all 26 model labels,
release dates, frontier flags and the 960-minute central-estimate fit cutoff.
All four numerical columns retain the full precision published in this snapshot.
Six early-model 50% CI endpoints differ from the old literals beyond rounding;
other differences are ordinary precision loss. Changes in the unweighted fitted
slopes come from point-estimate precision, not the CI corrections.

The first three models (GPT-2, GPT-3/davinci-002, GPT-3.5/instruct) are TH1.0
measurements **stitched into** the TH1.1 series, not TH1.1 re-estimates:
https://metr.org/blog/2026-01-29-time-horizon-1-1/
Public benchmark and task-suite version identifiers are retained in
`METR_PROVENANCE` and each newly computed product. No network access is needed
for computation or tests; the facts are embedded, not fetched at render time.

Only `metr` gains recipe `metr-th1.1-20261103-aae31902b051-v1`. Its reader rejects
legacy/unversioned products, mismatched snapshot provenance and NPZ metadata
shadowing, under the existing atomic lock. Existing six corrected recipes and
all unrelated reader semantics are unchanged. Explicit reviewed regeneration is
required; a render cache miss never triggers computation. Existing broad source
fingerprinting can separately mark other products stale; that is not a change
to their scientific recipes and does not authorize regenerating them.

The OLS protocol, seeded 4,000-resample descriptive bootstrap, and model masks
are unchanged. Deterministic full-precision point fits (days per doubling):

- 50% horizon since 2023: 128.74380265078 (14 points)
- 50% horizon all-time stitched: 187.77754378812733 (17 points)
- 80% horizon since 2023: 133.4053133040359 (14 points)

The bootstrap resamples model rows, not METR task-level uncertainty; it must not
be represented as reproducing METR's published confidence-interval methodology.
No model training is involved. Numerical agreement does not establish causal
per-step error reduction. This source-only follow-up does not repair or accept
s07's CI clipping/layout or its causal narration; those remain explicit review
gates. No METR rendering, ZH rendering, full-motion or listening acceptance is
claimed. Private computed products and audit/render evidence are not committed.
