# Part 9 — Drums, Bars and Bells

Review date: 15 November 2026. Base: `611e81e6`. Source and sampled-preview review complete; final production remains open.

## Changes

- Replace claims that inharmonic instruments are naturally badly tuned. Scope the harmonic comparison to
  ideal tensioned strings and air columns; distinguish Western minor-third bells from all bell traditions.
- Correct the Bessel-zero claim: fixed-order zeros approach equal spacing, while the full membrane spectrum
  does not form an integer harmonic series. Qualify strike position, radiation and real decay.
- Describe kettledrum air loading as part of a coupled system; separate pitch-model salience from listeners'
  certainty and musical octave labels.
- Identify the tabla's right-hand dayan and the simplified central-density model. Qualify harmonic groups,
  the chosen patch optimum and modal weighting; disclose clip level matching.
- Scope width cancellation to slender-beam theory, qualify marimba/xylophone tuning targets by register and
  maker, and replace absolute mallet and resonator statements with preferential excitation/radiation.
- Identify bell ratios as representative published tuning targets, not measurements of a specific bell.
  Qualify founding history, tierce colour and preference. Align listening captions with the data's scope.
- Identify Chladni images as approximate computed patterns and correct the displayed numbers from alleged
  pitches to schematic m²+n² indices; qualify violin plate-tuning practice and avoid
  suggesting that two target modes alone guarantee a finished instrument's quality.
- Identify the cymbal's schematic spectrum and nonlinear cascade; acknowledge real-time reduced models.
  Describe steelpan development through Trinidadian makers and identify the schematic fifths layout.
- Scope Weyl's formula and the area exercise as asymptotic estimates. State wave-speed and boundary
  assumptions for spectral invariants; qualify smooth-domain uniqueness theorems. Label tabulated
  eigenvalues as scaled squared frequencies and distinguish numerical agreement from floating-point limits.
- Explain that equal eigenfrequencies do not ensure identical struck sounds: the listening example matches
  modal weights and decays, while real excitation, damping and radiation can differ.
- Qualify material recognition, game-sound synthesis and Guido's role in staff-based teaching.

## Verification

Numerical items generated; numerical payloads and waveforms unchanged.

- Chapter/percussion/audio/loader tests: **26 passed**, one `audioop` deprecation warning;
  `/workspace/scratch/music9-final-tests.log`.
- `python -m videos.music.labs 9`: passed; `/workspace/scratch/music9-lab.log`.
- Five native 1920×1080 stills inspected: timpani ratios, loaded membrane modes, inverse-spectrum summary
  free-bar shapes and Chladni patterns; `/workspace/scratch/music9-native/images/`.
- All twelve full chapter previews rendered and their 48-sample contact sheets inspected. Hook, Bells,
  Plates and Frontier refreshes were reviewed. No chapter source postdates its final render.
- Sound gate: **12 scenes, zero failures**; `/workspace/scratch/music9-final-sound.log`. The final Frontier
  change wraps a caption and does not alter narration or audio; it was rescanned for motion.
- Motion gate: **12 scenes, 16 listening windows, zero failures**, at 4 fps; no blank/sparse runs ≥1.5 s
  or still-listening runs ≥2.5 s. `/workspace/scratch/music9-motion-results.json`.
- Source/movie/cue identities: `renders/qa/music9/source-receipt.json`; silent-narration previews total
  **44.70 minutes**.
- Source-based narration estimate: 36.7 minutes, including 1.8 minutes of listening; not final runtime.

## Production gates still open

Regenerate changed narration, inspect pronunciation and continuous listening/playback, measure final-film
alignment, and check complete-episode joins, native motion and mastering. No publication was performed.
