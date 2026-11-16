# Part 65 — Machines that Compose

Review date: 16 November 2026. Source and sampled-preview review complete; final production remains open.

## Changes

Scope prediction/copying tradeoffs to the tested models, distinguish melody-generator holdouts from the broader harmonizer corpus, qualify beam and pseudo-Gibbs sampling and exact-run originality tests. Repair cold-cache audio aliases.

Preserve transparent piano-roll frames while dimming the free/constrained comparison; avoid white backgrounds obscuring the notes.

Render sampled key accidentals with LaTeX flat/sharp commands so the transformer chapter compiles.

Align comparison bars to a common baseline and fit their bit/copy labels within the frame.

Add playback cursors to the free/constrained rolls using the rendering tempo and fermata pauses.

## Verification

- Chapter/module/audio/loader tests: 17 passed; `/workspace/scratch/music65-tests.log`.
- Lab and length-estimate logs: `/workspace/scratch/music65-lab.log`, `/workspace/scratch/music65-length.log`.
- 4 selected native 1920×1080 stills inspected; `/workspace/scratch/music65-native/`.
- All 13 chapter preview sheets inspected; 13 sound cases and 13 listening-window motion checks pass. Silent-narration previews: 39.46 minutes. Source hashes and freshness verified; identities: `renders/qa/music65/source-receipt.json`.

## Production gates still open

Regenerate changed narration, inspect pronunciation and continuous listening/playback, measure final-film alignment, and check complete-episode joins, native motion and mastering. No publication was performed.
