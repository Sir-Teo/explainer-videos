# Music, Built: sequential polish and QA

## Scope and checkpoint — 15 November 2026

Review all 68 episodes in order, with educational clarity, aesthetic quality and explanatory visualization as
the priorities. Start from source `eae705a04e5ae8f9ba0a596bf960bc65f53e0075` fetched from `origin/main`.
The initial local checkout was older than the entire Music series; that discovery is resolved.

**Current episode: Part 1, One String. No episode is approved for final production yet.**
Do not advance to Part 2 until the Part 1 chapter review and repairs are completed at the declared preview scope.
Narrated playback, listening, native-resolution readability and complete-episode joins are separate gates.

## Part 1 evidence so far

- Generated all 15 numerical items and their sound clips with `python -m videos.music.music1.compute`.
  Log: `/workspace/scratch/music1-compute.log`.
- 37 tests passed after the initial two source repairs:
  `python -m pytest -q tests/music/test_music1.py tests/music/test_string.py tests/music/test_audio.py`.
  Log: `/workspace/scratch/music1-tests-after.log`. The warning is Python's deprecated `audioop` module.
- `tools/lecture_length.py music1` estimates 45.8 minutes, including 2.2 minutes of listening.
  This is an estimate, not the duration of a final narrated film.
- Rendered Hook (246 s), Monochord (230 s), Mersenne (294 s), Wave (228 s) and Modes (252 s)
  as silent-narration 480p15 previews. Visually inspected each 36-frame contact sheet in
  `renders/qa/music1/<Scene>_en.png`. These are sampled layout checks, not continuous playback.
- The first sound-gate run on Hook, Monochord and Wave checked 3 scenes with zero failures:
  `/workspace/scratch/music1-sound.log`. It checks cue/narration overlap, clip-driven pictures, labels, levels,
  peaks and small-speaker/stereo qualifications. It does not certify measured final-film synchronization.

## Repairs reviewed

1. Hook cold opening: label the visible blur as a vibration envelope with exaggerated displacement.
   No sound, words or timings changed. Rendered `Hook.cold_open()` via an isolated subclass;
   inspected eight samples in `/workspace/scratch/music1-opening.png`. Caption clears the instrument,
   note names and sound label.
2. Monochord listening quiz: lower the question card from a 0.6 to a 1.0 scene-unit upper margin.
   Baseline sample at 201.1 s showed contact with the upper-right sound label. Rendered
   `Monochord.quiz()` via an isolated subclass and inspected 3, 8, 12 and 18 s in
   `/workspace/scratch/music1-quiz.png`; the listening sample has clear separation.

The full Hook and Monochord baseline renders started before these edits. Their old sheets must not be
described as full current-source regressions; only the isolated changed sections have after-render review.

## Next work, still within Part 1

1. Repair the legend's four hanging strings: measured left edge is −7.15 in a frame ending at −7.111…;
   move the group in from the left and review the legend section. The initial hammers also have little margin.
2. Wave reflection explanation: sampled 53.8/60.2 s shows the imaginary pulse crossing its caption, and the
   reflected pulse crosses the fixed-point caption. Move annotations outside the full swept wave area and
   rerender `Wave.flick()`.
3. Modes gallery: 115.5/122.5 s samples show the 3:2 and 4:3 ratio annotations clipped at the left edge.
   Reserve space for braces and labels before laying out the two columns; add an explicit slow-motion label.
4. Complete rendered review of Equation, DAlembert, Quarrel, Pluck, Overtones, Ratios, RealStrings,
   Frontier, Series and Outro (ten chapters). Review transitions and listening windows, not just endpoints.
5. Rerender changed full chapters, run sound gates across all 15 chapters, inspect any reported dead-air
   or static-picture intervals, and run appropriate numerical regression. Final narrated/audio/native-resolution
   gates remain open until actually exercised.

## Remaining episodes

Parts 2–68: queued, no new polish or QA acceptance claimed by this pass.
