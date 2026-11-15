# Part 2 — Waves in Air

Review date: 15 November 2026. Base: `85280665`. This is source and sampled-preview QA,
not final narrated production approval.

## Changes

- Clarify that the one-way piston push leaves a small parcel displacement; it does not return every parcel
  to its starting point. Label the pulse's slow motion and exaggerated displacement.
- Add a force diagram before the pressure derivation. Keep the numerical example above the equations,
  define the progressive-wave assumption, and distinguish instantaneous intensity from its rms-based mean.
  Label the pressure table as rms and displacement as the peak excursion of a 1 kHz tone.
- Move the vacuum scene's sound-source tag clear of its heading and preview the medium names before their
  speed bars appear.
- Extend the temperature graph to include the actual Krakatoa equivalent-temperature point. Use the stored
  observed speed and the same ideal-gas curve as the room-temperature calculation instead of clamping the
  point to an incorrect graph location. Define kelvin and the specific gas constant; qualify the atmospheric
  inference for stratification and winds.
- State the progressive-plane-wave/rms conditions on the decibel card. Explain the hearing reference as
  approximate and frequency-dependent. Correct the five distance doublings from 1 to 32 metres.
- Draw the interference example with its actual 34 cm path difference, and state the phase and equal-amplitude
  assumptions for complete cancellation. Explain headphone cancellation at the ear.
- Correct the bottle's Q interpretation: amplitude falls to 1/e in Q/pi cycles, about eleven here. Remove
  the initial mass/spring captions before the formula ladder appears. Clarify the two-tube solution's flow
  sign convention in the notes.
- Distinguish specific impedance from volume-flow impedance, area from diameter, and normal-incidence power
  fractions from pressure reflection. Scope the horn numbers to transmission into the wider simulated tube.
- Label the Doppler example as a two-semitone approach-to-retreat change.
- Label all four nonlinear-wave sample distances accurately; scope the Fubini comparison to the first three
  harmonic amplitudes. Distinguish propagation-added brightness from the harmonics produced by the lips,
  and qualify shock distances as lossless constant-bore estimates.
- Qualify the recap's temperature dependence by fixed gas composition and distance loss by an open point source.

## Verification and local evidence

All fifteen numerical items were generated; `compute.py` and the numerical sound payloads are unchanged.
The lab ran (`python -m videos.music.labs 2`). Two new numerical regressions cover the rms/peak conversion
and the one-way push's residual displacement.

- `python -m pytest -q tests/music/test_music2.py tests/music/test_air.py tests/music/test_audio.py`:
  **29 passed**, one `audioop` deprecation warning. Log: `/workspace/scratch/music2-final-tests.log`.
- Silent-narration 480p15 chapter renders and 48-sample contact sheets are under `renders/qa/music2/`.
  All fourteen chapters were visually sampled in sequence. Changed chapters were rerendered, with repaired
  sections checked again. This is sampled review, not continuous human playback.
- Native 1920×1080 stills of the pressure/intensity and bottle derivations were inspected:
  `/workspace/scratch/music2-native/images/music2_native/`. These verify those static layouts only.
- `python tools/qa_sound.py music2`: **14 scenes, zero failures**.
  Log: `/workspace/scratch/music2-final-sound.log`. Checks include labels, cue/narration separation,
  clip-driven pictures, levels and small-speaker qualifications.

- The existing `tools/dead_air.py` detector passed **14 scenes and 18 listening windows**, at its default
  4 fps. No blank/sparse runs ≥1.5 seconds or still listening runs ≥2.5 seconds were reported. The adapter
  supplies chapter-local cue offsets because the normal sound lookup expects a stitched film.
  Logs: `renders/qa/music2/<Scene>_dead_air.log`; adapter/results:
  `/workspace/scratch/music2_check_previews.py`, `music2-motion-results.json`.

Source/movie/cue hashes and measured durations are in `renders/qa/music2/source-receipt.json`.
The silent-narration previews total 42.18 minutes; this is not the final narrated runtime.

## Remaining gates

Regenerate revised narration, check pronunciation and full listening,
measure final-film synchronization, and verify complete-episode joins, native-resolution motion and mastering.
No publication was performed.
