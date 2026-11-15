# Part 4 — The Ear

Review date: 15 November 2026. Base: `c55dcb3f`. This is source and sampled-preview QA;
final narrated production remains open.

## Changes

- Add a schematic active-feedback diagram to Gold's history section. Label the opening scope as a 16 ms
  waveform window. Distinguish the synthesized two-tone signal from distortion in an actual loudspeaker;
  hearing a combination tone alone does not establish whether the ear or playback equipment made it.
- Explain the delayed emission as a cochlear response rather than ruling out every reflection process.
  Qualify emission loss as associated with outer-hair-cell damage; it does not screen every cause of hearing loss.
- Define the middle-ear calculation as a simplified real effective entrance load, distinct from bulk fluid
  impedance. Explain pressure/motion exchange without creating power. Label the canal's particle-motion
  envelope and the threshold curve as an approximation based on measurements.
- Disclose normalized displacement and the cochlear film's slow motion. Scope exact octave/place spacing to
  the model, and describe attenuation toward the apex without claiming identically zero motion everywhere beyond.
- Replace the ambiguous musical phrase "a tenth apart" with 10% frequency separation. Qualify the connection
  between filter overlap and phase sensitivity. Remove the categorical claim that one nerve fibre cannot fire
  at 250 spikes per second, and avoid claiming a single exact human temporal cutoff.
- Label digital level matching separately from calibrated pressure at the listener. Restrict the displayed
  phon/sone relation to 40 phons and above; use 40-to-80 phons as four modeled doublings, rather than extending
  the power law down to threshold. State equal-player/incoherent-power assumptions for the violin estimate.
- Distinguish masking from injury, explain codec quantization allocation more accurately, wrap its application
  captions into a reserved column, and bring the cochlea's base caption fully into frame.
- Qualify high-frequency interval judgments by listener and task. Remove the claim that all melodic instruments
  stop at the piano's upper note or that only timing can convey pitch.
- Identify NIOSH's 85 dBA/3 dB rule as a recommended occupational criterion, distinct from the US legal OSHA
  limit and from a guarantee of safe exposure. State actual fitted attenuation in the earplug calculation;
  remove the promise that foam guarantees more than a day of safe listening. Scope distance loss to an isolated
  point source in the open, and wrap the habits table without clipping.
- Make exposure-bar heights proportional to hours, so successive 3 dB steps visibly halve their heights.
  Display the schematic audiogram's loss as positive threshold shifts. Qualify the common 3–6 kHz notch and
  distinguish it from a universal or diagnostic injury pattern.
- Scope the damping reduction as an active-like surrogate and the cube-root response as a resonant cubic Hopf
  model. Define plot level references and distinguish dynamic range from an absolute level. Explain cochlear
  compression as one contributor to loudness, alongside neural processing. Align the recap and notes.

## Verification

The numerical items and lab were generated; `compute.py` and the numerical sound payloads are unchanged.

- `python -m pytest -q tests/music/test_music4.py tests/music/test_ear.py tests/music/test_audio.py`:
  **31 passed**, one `audioop` deprecation warning; `/workspace/scratch/music4-final-tests.log`.
- `python -m videos.music.labs 4`: passed; `/workspace/scratch/music4-lab.log`.
- All thirteen chapters rendered as silent-narration 480p15 previews. All 48-sample baseline sheets were
  inspected in sequence. Repaired sections were checked again, including the feedback diagram and masking
  caption in isolated frames. Sheets: `renders/qa/music4/<Scene>_en.png`; targets:
  `/workspace/scratch/music4-feedback.png`, `music4-mask-after.png`, and `music4-*-repairs.png`.
- Three native 1920×1080 stills were rendered and inspected: the historical cards, linear exposure chart and
  wrapped habits table. Files: `/workspace/scratch/music4-native/images/music4_native/`. These establish those
  static layouts, not whole-episode native motion.
- The motion detector passed thirteen scenes and sixteen listening windows at its default 4 fps, with no
  blank/sparse runs ≥1.5 seconds or still-listening runs ≥2.5 seconds. The final Mask-only clearance refresh
  was rescanned and passed. The adapter supplies chapter-local cue offsets; logs/results:
  `renders/qa/music4/<Scene>_dead_air.log`, `/workspace/scratch/music4-motion-results.json`,
  `music4-mask-motion-results.json`, and `music4-mask-final-motion.log`.
- `python tools/qa_sound.py music4`: **13 scenes, zero failures**, including the refreshed Mask render.
  Log: `/workspace/scratch/music4-final-sound.log`.
- Source-based narrated estimate: 50.3 minutes including 1.9 minutes of listening, not a final runtime.

Source/movie/cue hashes and measured durations are in `renders/qa/music4/source-receipt.json`.
The silent-narration previews total 60.10 minutes, not a final narrated runtime.

## Production gates still open

Regenerate changed narration, inspect pronunciation and continuous listening/playback, measure final-film
alignment, and check complete-episode joins, native motion and mastering. No publication was performed.

## Clean-cache follow-up

A later series preflight exposed a clip prefix that differs from its computation item.
The shared loader now accepts explicit aliases; this part maps `next` to `nextpart`, so its closing clip
can be computed on first use. Three isolated loader regression cases pass (cold lookup, cache reuse and
an actionable missing-clip error). This changes lookup only; cached clip content and picture timing are
unchanged. The local source receipt was refreshed for the alias declaration; preview media were retained.
