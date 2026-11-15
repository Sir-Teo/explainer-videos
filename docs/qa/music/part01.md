# Part 1 — One String

Review date: 15 November 2026. Base: `eae705a04e5ae8f9ba0a596bf960bc65f53e0075`.
Initial disclosure/quiz repairs: `3b72a1b8`. This is source and preview QA, not final production approval.

## What changed

- Disclose exaggerated displacement in the opening vibration envelope.
- Bring the legend's hanging strings and hammers inside the frame. The strings previously started at
  −7.15 with the frame ending at −7.111; the repaired string and hammer clearances exceed 0.3 scene units.
- Move reflection captions out of the moving waves' swept area.
- Reserve a gutter for the mode gallery's octave/fifth/fourth braces; label its slow motion and exaggerated
  displacement. The fifth/fourth labels previously ran off the left edge.
- Keep sound-source tags clear of the Monochord quiz, Pluck comparison legend and Overtones question card.
- Align the Fourier target and sum by their physical axes. Different support bounding boxes had introduced
  a 0.09875-unit offset even when the displayed shapes were identical; the corrected offset is zero.
- Draw d'Alembert's comparison line from the independently evaluated left/right travelling waves, with
  dots from the bead simulation. Previously both pictures read the bead frames. Independent maximum error
  is 2.525757381022231 × 10⁻¹⁵.
- Describe the asymmetric pluck's intervening segment as straight with zero curvature, rather than horizontal.
  Distinguish the common round-trip time from the shorter periods possible for individual higher modes.
- Correct the near-bridge claim: the first few partials are closer in level, but plucking at one tenth still
  removes the tenth partial. The stored measured tenth is below −60 dB; a regression checks this and the
  first three partials' relative levels.
- Qualify the major-chord example: this pluck contains partials 4/5/6; other plucking points can remove them.
  Scope the lowest-partial description of the fundamental to the string being demonstrated.
- Replace the misleading "six times as stiff" description with κ × 6, bending rigidity × 36 at fixed mass.
  Label the stiff-string formula's flexible-string reference explicitly; it is not the actual first partial.
  The numerical clips and payloads are unchanged. A regression checks the factor of 36 and the first-mode shift.
- Show the actual conserved discrete energy, including its cross-time stretch product and discrete velocity.
  State the stable-grid condition and limit the conservation demonstration to the ideal linear string;
  the nonlinear glide is a separate experiment, not an energy-conservation proof.
- Wrap historical-table names in their own column, constrain the Tune description to the frame, and use actual
  stored travelling-wave motion in the series overview instead of making a triangular pluck breathe as one mode.
- Clarify the historical analytic-formula restriction, rather than claiming a triangle cannot have one formula.
  Align the recap's lowest-frequency and proportional-amplitude wording with the derivations.

## Verification and local evidence

All fifteen numerical items were generated. `compute.py`, Monochord's physics and the sound payloads were not
edited by this pass. Narration wording changed where the original scientific claim was inaccurate; production
speech must be regenerated for those lines.

- `python -m pytest -q tests/music/test_music1.py tests/music/test_string.py tests/music/test_audio.py`:
  **38 passed**, one `audioop` deprecation warning; final log `/workspace/scratch/music1-final-tests.log`.
- `python -m videos.music.labs 1`: passed; produces `renders/labs/music/lab01.png` and `lab01.wav`.
- All fifteen chapters rendered as silent-narration 480p15 previews. Baseline contact sheets were inspected
  chapter by chapter; repaired chapters were rerendered and reviewed at their changed sections. Current sheets
  are `renders/qa/music1/<Scene>_en.png`, with 48 samples per chapter except Mersenne's unchanged 36-sample sheet.
  These are sampled visual checks, not continuous human playback.
- Nine additional repair-target frames were inspected in `/workspace/scratch/music1-targets.png`.
  The opening/Monochord quiz also have isolated after-render samples from the initial repair commit.
- Native 1920×1080 stills of the energy derivation, eight-mode gallery and historical roadmap were rendered
  and inspected in `/workspace/scratch/music1-native/images/music1_native/`. They establish those static
  layouts' readability only, not native-resolution motion or whole-episode acceptance.
- `python tools/qa_sound.py music1`: **15 scenes, zero failures**. Log:
  `/workspace/scratch/music1-final-sound.log`. Checks cue/narration overlap, labels, clip-driven pictures,
  music-stem peaks, levels and small-speaker/stereo qualifications.
- The existing `tools/dead_air.py` detector was run at its default 4 fps on each preview, using its own
  chapter-local cue sheet. The adapter only supplies the local listening-window offsets, because the normal
  `--sound` lookup expects a stitched production film. **15 scenes, 40 listening windows, zero failures**;
  no blank/sparse runs ≥1.5 seconds were reported. Reports: `renders/qa/music1/<Scene>_dead_air.log`;
  adapter and summary: `/workspace/scratch/music1_check_previews.py`, `music1-motion-results.json`.
  The final recap-only refresh was rerendered and visually inspected, then rescanned with zero blank,
  sparse or still-listening failures (`/workspace/scratch/music1-outro-final-motion.log`).

Current source/movie/cue hashes and measured chapter durations are in
`renders/qa/music1/source-receipt.json`. The chapter durations are those of silent-narration previews;
the source-based narrated estimate is 46.3 minutes including 2.2 minutes of listening, not a final runtime.

## Production gates still open

Generate the revised neural narration; inspect speech pronunciation, music/narration joins and full playback;
measure final-film sound/picture alignment; check whole-episode native-resolution motion and final mastering.
The source and sampled-preview pass does not close those gates. No upload or publication was performed.
