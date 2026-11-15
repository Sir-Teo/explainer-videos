# Part 7 — Strings, Hammers and Bows

Review date: 15 November 2026. Base: `dff44b26`. Source and sampled-preview review complete; final production remains open.

## Changes

- Qualify blind violin tests as evidence from selected instruments and settings, rather than equivalence of
  every old/new violin. Wrap the identification result. State that piano string counts vary by register.
- Replace the absolute claim that bare strings cannot be heard; distinguish acoustic soundboards and
  membranes from electrical amplification. Label independently normalized spectra and qualify guitar modes.
- Bring the guitar plate label into frame, scope the coupled-frequency identity to its two-mode model,
  distinguish the covered-hole plate plus trapped air, and qualify low-note radiation and real measurements.
- Remove unsupported Karplus–Strong student/home-computer details and universal game-music claims.
  Call random noise a simplified excitation; show the actual stored lap (144), rather than a false 170.
- Distinguish early leather-covered Cristofori hammers from modern felt. Qualify harpsichord dynamics and
  the role of hammer speed; include pedals, timing and initial state. Use newtons and kgf for tension.
  Label loudness matching as modeled and avoid treating the seventh partial as inherently unmusical.
- Identify stiff-string quiz signals as models, qualify wound-string stiffness and illustrative bass length,
  and avoid universal instrument-preference claims. Scope coupled-string decay and tuners' unison practice.
- Identify the friction law and Helmholtz corner as idealizations; disclose schematic slow motion and real
  rounding. Distinguish plucked displacement's n^-2 envelope from bridge force, which adds a factor of n.
- Explain +6 dB as bridge-force level, with brightness changes requiring contact/rounded-corner dynamics.
  Qualify the piano/violin control comparison. Wrap the bow-force example and closing feedback diagram.
- Label the violin body as schematic, explain vibrato as both pitch and colour change, and describe wolf
  notes as coupled instabilities rather than a universal exact meeting of Schelleng limits. Wrap its caption.
- Distinguish the modal hammer from the waveguide bow. Explain model mismatch as potentially missing
  physics, parameters or excitation; avoid claiming a universal measurement rule predicts preference.

## Verification

Numerical items and lab generated. `compute.py` and numerical waveforms are unchanged.

- Chapter/string/audio/loader tests: **28 passed**, one `audioop` deprecation warning;
  `/workspace/scratch/music7-final-tests.log`.
- `python -m videos.music.labs 7`: passed; `/workspace/scratch/music7-lab.log`.
- All twelve full chapter previews rendered and their 48-sample contact sheets inspected. The Hook
  identification caption was refreshed and reviewed. No chapter source postdates its final render.
- Three native 1920×1080 stills inspected: guitar coupling, hammer force and bow-force worked example;
  `/workspace/scratch/music7-native/images/music7_native/`.
- `python tools/qa_sound.py music7`: **12 scenes, zero failures**; `/workspace/scratch/music7-final-sound.log`.
- Motion detector: **12 scenes, 12 listening windows, zero failures**, at 4 fps; no blank/sparse
  runs ≥1.5 seconds or still-listening runs ≥2.5 seconds. `/workspace/scratch/music7-motion-results.json`.
- Source/movie/cue identities: `renders/qa/music7/source-receipt.json`. Silent-narration previews total
  **50.71 minutes**. Source-based narration estimate: 42.3 minutes, including 1.7 minutes
  of listening; not a final narrated runtime.

## Production gates still open

Regenerate changed narration, inspect pronunciation and continuous listening/playback, measure final-film
alignment, and check complete-episode joins, native motion and mastering. No publication was performed.
