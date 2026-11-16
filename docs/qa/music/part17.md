# Part 17 — Four Voices

Review date: 16 November 2026. Source and sampled-preview review complete; final production remains open.

## Changes

- Scope chorale statistics to selected encodings and automatic labels/detectors. A note-change event is not necessarily a harmonic change, and off-beat position alone does not establish a passing tone.
- Distinguish unlabeled beats from absence of harmony, and applied dominants from diatonic common-chord pivots. Qualify Picardy-third explanations and the interpretation of other final labels.
- Correct the spacing rule to adjacent upper-voice pairs. Qualify grouping, doubling and leading-note behavior as style-dependent guidelines.
- Distinguish candidate filters and finite soft penalties from universal rule compliance. Zero detected parallels is the reported result, not proof that every textbook rule is satisfied.
- Remove the unsupported claim of a reproduced validation/tuning procedure: the build uses fixed hand-set weights. Keep the tune-grouped training/test split distinct from that issue.
- Label the harmonizer lattice as a restricted, pruned candidate search. Its displayed dots aggregate candidates and its gold path is schematic, not the computed optimum.
- Qualify algorithmic-composition history and listening-test interpretations. Align source captions, recap and notes.

## Verification

- Chapter/fourpart/audio/loader tests: 25 passed, one audioop warning; `/workspace/scratch/music17-tests.log`.
- Lab passed; `/workspace/scratch/music17-lab.log`.
- All numerical items generated; numerical algorithms unchanged.
- Three native 1920×1080 stills inspected: detector statistics, candidate lattice and held-out evaluation table. Lattice labeling refreshed and reviewed again; `/workspace/scratch/music17-native/images/music17_native/`.
- All 14 chapter preview sheets inspected. Fourteen sound-gate cases and 14 listening-window motion checks pass. Silent-narration previews: 40.17 minutes. Source hashes and freshness verified; local identities: `renders/qa/music17/source-receipt.json`.

## Production gates still open

Regenerate changed narration, inspect pronunciation and continuous listening/playback, measure final-film alignment, and check complete-episode joins, native motion and mastering. No publication was performed.
