# Part 5 — Consonance

Review date: 15 November 2026. Base: `4478a7c2`. Source and sampled-preview QA;
final narrated production remains open.

## Changes

- Correct the stopped-string explanation: half the open length sounds an octave above the open string;
  the two halves themselves are in unison. State that Euler's ratio is reduced before taking its LCM.
  Correct the rational-approximation denominator limit to 400 and scope its failure to exact integer measures.
- Distinguish exact mathematical periodicity from a long-period rational approximation. Explain the beat
  signal as a carrier times an envelope while retaining two spectral lines; identify the illustrative plot.
- Separate sensory roughness, harmonicity/fusion and musical preference. Scope the pure-tone roughness
  findings to the pitches and model used, and allow nearly pure instrument tones.
- Extend both seven-partial diagrams to include all seven upper partials. Explain the 91 modeled pairs;
  several strong partials coincide at the octave, rather than every partial of a finite spectrum.
- Name septimal intervals, identify the shifted octave-region roughness valley without redefining the
  octave, and scope the timbre rule to modeled roughness.
- Distinguish the arithmetic common-series fundamental from Rameau's fundamental bass and a chord's
  musical root. Qualify the relation among historical theories and the missing-fundamental percept.
  Wrap the triad comparison's column heading and values; identify its landscape as a sampled grid.
- Treat the nearly equal major/minor roughness as a result for these parameters, not a theorem from
  matching interval types. Qualify explanations of major/minor character.
- Explain the Tsimane' evidence as strong dependence of Western consonance preference on exposure,
  without claiming that every preference is entirely learned. Qualify infant evidence and shared auditory
  machinery, and distinguish changes in tuning from changes in practice and theory. Align recap and notes; identify the free-bar modal ratios without claiming a central strike excites them all.

## Verification

The numerical items and lab were generated. The closing clip uses an explicit `next` → `nextpart` loader alias for cold builds. Numerical computations and sound waveforms are unchanged.

- Chapter, consonance, audio and clip-loader tests: **30 passed**, one `audioop` deprecation warning;
  `/workspace/scratch/music5-final-tests.log`.
- `python -m videos.music.labs 5`: passed; `/workspace/scratch/music5-lab.log`.
- All twelve 48-sample baseline contact sheets were inspected. Revised chapter previews and repaired
  captions were checked again, including the last refreshed recap/problems. No chapter source postdates its render.
- Three native 1920×1080 stills inspected: Euler's rule, the full partial worked example, and the wrapped
  triad table. `/workspace/scratch/music5-native/images/music5_native/`.
- Source-based narration estimate: 40.6 minutes, including 2.5 minutes of listening; not a final runtime.

- `python tools/qa_sound.py music5`: **12 scenes, zero failures**; `/workspace/scratch/music5-final-sound.log`.
- Motion detector: **12 scenes, 16 listening windows, zero failures**, at 4 fps; no blank/sparse runs
  ≥1.5 seconds or still-listening runs ≥2.5 seconds. `/workspace/scratch/music5-motion-results.json`.
- Source/movie/cue hashes: `renders/qa/music5/source-receipt.json`; measured silent-narration preview
  duration **49.20 minutes**, not a final narrated runtime.

## Production gates still open

Regenerate changed narration, inspect pronunciation and continuous listening/playback, measure final-film
alignment, and check complete-episode joins, native motion and mastering. No publication was performed.
