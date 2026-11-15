# Part 8 — Pipes, Reeds and Voices

Review date: 15 November 2026. Base: `9e278560`. Source and sampled-preview review complete; final production remains open.

## Changes

- Distinguish ideal pipe resonances from produced harmonics. State acoustic lengths before end corrections,
  identify the B-flat clarinet example, and label normalized input impedance and model pressure/flow.
- Correct the returning suction pulse: it closes the reed further. Scope the one-third threshold to the
  quasi-static small-signal model and distinguish player controls from its single pressure parameter.
- Identify the hole-position example as ideal just intonation. Explain register-hole weakening and shifting,
  rather than detuning alone. Distinguish a cone's harmonic series from literal open-end boundary conditions.
- Qualify missing-tip volume compensation, natural-brass history, lip inertia and pedal-note generation.
  Separate nonlinear oscillation from the ear's missing fundamental. Identify illustrative valve lengths.
- Present half-period jet delay as a regime-dependent guide, distinguish flue and reed organ pipes,
  and qualify nominal pipe lengths and harmonic fusion.
- Identify the drawn glottal pulse and source–filter approximation, include tissue recoil and tract feedback,
  and qualify population pitch ranges. Distinguish tract gain from independently normalized output and
  disclose lip radiation. Formants filter existing harmonics rather than adding harmonic tones.
- Scope the uniform-tract example and vowel map to their assumptions, speaker population and dialect.
  Correct the claim that different fundamentals share no harmonics.
- Distinguish modeled singer's-formant boost from demonstrated orchestral projection. Label separate dB
  references and the schematic orchestra's offset; qualify epilaryngeal geometry, soprano vowel choices and
  overtone singing. A modeled filter gain is not a measured hall gain.
- Describe what these models omit without claiming the physics cannot be computed. Distinguish linear bore
  propagation from nonlinear excitation, and reduced jet calculations from resolved fluid simulations.
- Align recap, practice and problems with those limits; qualify speech-codec claims and the transition from
  harmonic strings/air columns to an ideal circular membrane's distinct modal ratios.

## Verification

Numerical items generated; numerical payloads and waveforms unchanged.

- Chapter/wind/audio/loader tests: **29 passed**, one `audioop` deprecation warning;
  `/workspace/scratch/music8-final-tests.log`.
- `python -m videos.music.labs 8`: passed; `/workspace/scratch/music8-lab.log`.
- Three native 1920×1080 stills inspected: pipe-length derivation, voice source–filter spectrum and soprano
  resonance tuning; `/workspace/scratch/music8-native/images/music8_native/`.
- All twelve full chapter previews rendered; their 48-sample contact sheets inspected. Column, Reed and
  Holes axis-label refreshes were reviewed. No chapter source postdates its final render.
- Sound gate: **12 scenes, zero failures**; `/workspace/scratch/music8-final-sound.log`. The final Holes
  refresh also passed its scene sound check.
- Motion gate: **12 scenes, 15 listening windows, zero failures**, at 4 fps; no blank/sparse runs ≥1.5 s
  or still-listening runs ≥2.5 s. The final Holes refresh was rescanned successfully.
- Source/movie/cue identities: `renders/qa/music8/source-receipt.json`; silent-narration previews total
  **52.99 minutes**.
- Source-based narration estimate: 44.7 minutes, including 1.6 minutes of listening; not final narrated runtime.

## Production gates still open

Regenerate changed narration, inspect pronunciation and continuous listening/playback, measure final-film
alignment, and check complete-episode joins, native motion and mastering. No publication was performed.
