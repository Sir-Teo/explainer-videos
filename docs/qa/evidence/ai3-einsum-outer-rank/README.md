# Einsum outer-product rank qualification

The six-operation caption and EN/ZH narration now say **rank at most one**. The actual `i,j->ij` expression produces rank zero if either vector is zero, and rank one when both are nonzero. No data, cache recipe, palette or einsum expression changed.

Applied source SHA256: `4cf32fd13a907723f2478104b8be2de7dd38df693fa330558edb15d1716ed23e`.
Local Chinese narration SHA256: `a487167b7052952ca30ff29028efb76cf204b9ea172d3c2c19f17f866fbdc38e`.

Three executed **manual QA fixtures** pass: zero-input rank, nonzero-input rank, and linked caption/EN/ZH wording with bookmarks. These demonstrate the edge case and authoring linkage; they are not a new repository test-suite file. The authored fixture and exact execution logs are preserved under gzip. The baseline wording check fails as expected; the qualified version passes.

Actual applied pre-voiceover geometry fits in both languages, using the proposed caption translation as an in-memory overlay. The real production narration translator returns qualified Chinese with the same `abcdef` bookmark sequence. The source scanner covers 130/130 lines; its existing unused helper/branch-key notices are retained in the log. Root owns the global-caption merge from the exact [strings-only handoff](captions.json).

**Narration changed:** English adds “at most”; Chinese adds “至多.” Bookmark IDs remain, but spoken duration and later bookmark arrival times may increase. Fresh rendered/narrated validation remains necessary. No scene render, model run, data mutation or full-suite rerun was performed for this manual checkpoint. Root owns the existing narration/integration checks after caption merge.

Current before-source, EN/ZH movies and render records were copied before the edit; their paths and hashes are in the preservation ledger. The earlier [legend-polish evidence](../ai3-einsum-polish-regression/README.md) remains historical evidence for its exact `def7543b…` source and movies. This qualification does not update or relabel that review.

[manifest.json](manifest.json) authenticates byte-preserved gzip fixtures, logs and receipts. Read the full receipt with `gzip -dc applied-handoff.json.gz`; read the original fixture with `gzip -dc test_ai3_einsum_rank.proposed.py.gz`. Verify packaged files with `sha256sum -c SHA256SUMS`. Absolute runtime paths are historical provenance and may not exist outside the original cloud workspace.
