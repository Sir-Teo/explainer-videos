# Part 6 — Tuning

Review date: 15 November 2026. Base: `426569a7`. Source and sampled-preview QA; final narrated production remains open.

## Changes

- Scope the comma pump to its explicit common-tone rule, rather than a universal rule for good singers.
  Describe matching partials without claiming that a whole complex signal contains no beating.
- Replace claims that every piano, guitar and synthesizer uses exact equal temperament. Distinguish
  numerical roots from exact rational tuning calculations and preference from arithmetic approximation.
- Correct the twelve-note Pythagorean explanation: eight major thirds use four pure fifths; four cross
  the wolf and differ. State positive exponents in the odd/even proof and wrap the circle's instruction.
- Distinguish the syntonic and Pythagorean commas without claiming no relationship. Explain eleven pure
  fifths on a twelve-note keyboard, and tempering as distributing a discrepancy rather than erasing it.
- Scope meantone purity to eight major thirds. Qualify historical usage and listener judgments, and
  acknowledge uncertainty about Bach's exact temperament.
- Give the four-temperament chart aligned zero baselines, signed interval errors and common 20/40-cent
  guides. Move the just-intonation caption into frame. Fit the guitar derivation and equal-tuning summary.
- Distinguish five/seven equal divisions from pentatonic/diatonic collections with unequal steps. Use the
  exact logarithm in the continued fraction, identify capped absolute errors and the displayed 4–60 range,
  and explain tradeoffs among equal divisions without declaring one universally best.
- Describe piano stretch as a balance among selected partial pairs and other intervals. Avoid implying
  that every partial pair becomes beatless or that octave matching alone determines a complete tuning.
- Specify held major thirds in performance advice; name the harmonic seventh; qualify instrument range,
  tuning practices and accompaniment. Separate modern Baroque A=415 from historical measurements.
- Repair the closing clip's cold-build prefix (`nextpart.pluck`), retaining its waveform. Add a regression
  check that stored clip prefixes name computation items. Explain that a motion penalty alone neither
  imposes equal temperament nor anchors an adaptive tuner's absolute pitch.

## Verification

Numerical items and lab generated. Computed tuning values and audio waveforms are unchanged; the closing
clip's storage name was corrected.

- Chapter/tuning/audio/loader tests: **28 passed**, one `audioop` deprecation warning;
  `/workspace/scratch/music6-final-tests.log`.
- `python -m videos.music.labs 6`: passed; `/workspace/scratch/music6-lab.log`.
- All twelve endpoint sheets and all twelve 48-sample full-preview sheets inspected. Revised layouts
  checked again; the circle and meantone captions were refreshed. The closing preview was rendered
  after its final source edits and reused directly. No chapter source postdates its final render.
- Three native 1920×1080 stills inspected: four-tuning comparison, guitar frets and historical pitch
  references. The comparison's common scales and aligned baselines were inspected again.
- `python tools/qa_sound.py music6`: **12 scenes, zero failures**;
  `/workspace/scratch/music6-final-sound.log`.
- Motion detector: **12 scenes, 16 listening windows, zero failures**, at 4 fps; no blank/sparse
  runs ≥1.5 seconds or still-listening runs ≥2.5 seconds. `/workspace/scratch/music6-motion-results.json`.
- Source/movie/cue identities: `renders/qa/music6/source-receipt.json`. Silent-narration previews total
  **47.19 minutes**. Source-based narration estimate: 38.9 minutes, including 2.3 minutes
  of listening; neither is a measured final narrated runtime.

## Production gates still open

Regenerate changed narration, inspect pronunciation and continuous listening/playback, measure final-film
alignment, and check complete-episode joins, native motion and mastering. No publication was performed.
