# Part 13 — Intervals and Chords

Review date: 16 November 2026. Source and sampled-preview pass complete. Base: `fe7843ce`.

## Changes

- Qualify Rameau’s contribution and earlier inversion theories, and distinguish root analysis from missing-fundamental pitch.
- Scope the interval-quality line to the displayed spelling range; include class zero alongside six nonzero interval classes. Major/minor are basic diatonic forms rather than the only possible qualities.
- Treat the tertian census as a chosen spacing constraint rather than a universal acoustic derivation of harmony. Distinguish audible bass from the root ambiguity of symmetric augmented pitch classes.
- Qualify I/IV/V coverage, inversion stability, dominant resolution, doubling, omissions and chord-scale choices by musical context. The shared diatonic tritone does not determine a tonic among relative modes.
- Identify ERB width estimates, constrained voicing search and equal-tempered approximations to harmonic-series spacing.
- Correct distortion discussion: a pure 5:4 third also shares a harmonic grid. Identify the actual smooth tanh saturator and separate intermodulation from auditory roughness. Distorted thirds remain a musical option.
- Qualify published consonance rankings and benchmark dates, synthetic recognition scores and corpus/metric dependence. Align recap and notes.

## Verification

- Initial chapter/chords/staff/audio/loader tests: 37 passed, one audioop warning; `/workspace/scratch/music13-tests.log`.
- Lab passed; `/workspace/scratch/music13-lab.log`.
- Numerical items generated; descriptive voicing/doubling clip metadata refreshed.
- Three native 1920×1080 stills inspected: interval line, root ambiguity table and frontier benchmark card; `/workspace/scratch/music13-native/images/music13_native/`.
- All 13 chapter previews rendered and visually sampled; Roots, Voicing and Net layout/label refreshes reviewed. Silent-narration previews total 51.49 minutes.
- All 13 sound-gate cases and 27 listening-window motion checks passed. Source hashes and render freshness verified; local receipt: `renders/qa/music13/source-receipt.json`.

## Production gates still open

Regenerate changed narration, inspect pronunciation and continuous listening/playback, measure final-film alignment, and check complete-episode joins, native motion and mastering. No publication was performed.
