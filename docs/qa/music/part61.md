# Part 61 — Pitch, Onsets and Transcription

Review date: 16 November 2026. Source and sampled-preview review complete; final production remains open.

## Changes

Replace greedy note matching with maximum-cardinality one-to-one matching and add a counterexample regression. Qualify synthetic label exactness, network calibration, YIN limits, spectral additivity and chromatic spelling. Repair cold-cache tune alias.

## Verification

- Chapter/module/audio/loader tests: 18 passed; `/workspace/scratch/music61-tests.log`.
- Lab and length-estimate logs: `/workspace/scratch/music61-lab.log`, `/workspace/scratch/music61-length.log`.
- 3 selected native 1920×1080 stills inspected; `/workspace/scratch/music61-native/`.
- All 13 chapter preview sheets inspected; 13 sound cases and 14 listening-window motion checks pass. Silent-narration previews: 39.05 minutes. Source hashes and freshness verified; identities: `renders/qa/music61/source-receipt.json`.

## Production gates still open

Regenerate changed narration, inspect pronunciation and continuous listening/playback, measure final-film alignment, and check complete-episode joins, native motion and mastering. No publication was performed.
