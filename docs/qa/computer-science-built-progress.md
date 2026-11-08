# Computer Science, Built — sequential polish

Work on `computer-science-built`, one video at a time. Current video: **cs1,
What Is a Computation?** Do not advance to cs2 yet. This ledger describes the new
polish pass; the syllabus's earlier draft-preview claims are separate.

## Latest checkpoint, 8 November 2026 — semantic and motion repairs

The current source has **34 clean endpoint cases: 17 English (320 states) and
17 Chinese (321 states)**. Every chapter's contact-sheet overview was inspected,
including the Chinese closing credits. All 17 source-current English silent
motion previews have zero warnings and no blank/sparse runs of at least 1.5 s.
Their 40-frame contact-sheet overviews were inspected; all 58,395 movie frames
were decoded successfully. These are preview and sampled-review gates, not
continuous perceptual playback or production approval.

Additional repairs after the opening checkpoint:

- Finish fading full-view annotations before Euclid's zoom; restore them after
  returning home, eliminating enlarged/clipped ghosts during camera movement.
  The focused 1080p15 clip retains its 127.066667 s duration.
- Show the universal definition, software comparison and halting table during
  their introductions. Remove empty introductory holds from Rice, practice,
  busy-beaver and recap sections.
- State Rice's theorem precisely for nontrivial properties of computed partial
  functions, with matching English/Chinese examples and narration.
- Include Act XI's research parts in the tour and correct the stale Part 55
  ending reference. Translation source coverage is 113/113 blocks.

All 24 numerical JSON/NPZ files retain their earlier hashes. Fifteen real English
Kokoro utterances from Hook/Algorithms have current, completed automated audio
reports with zero signal/alignment issues. Full listening and narrated playback
are still open.

[Latest source-bound evidence](evidence/cs1-semantics-20261108/README.md).

## Earlier opening checkpoint — `176c9ab6`

- cs1's 17 numerical items completed locally. The machine suite passed 8 tests;
  the Pebble core suite passed 14 tests.
- Repaired the opening: show each subtraction beside the pebble piles; wait for
  the final equality bookmark before emphasizing the two equal counts.
- Repaired the Euclid chapter: hide dimension labels during the sliver zoom,
  restore them on returning home, and show al-Khwarizmi's history card as its
  narration begins instead of holding an empty screen.
- English endpoint captures and contact-sheet overview review: Hook, Algorithms,
  Engines, Hilbert, Machine, Programming, Robust. Chinese: Hook, Algorithms.
  All nine current captures passed with zero warnings (190 captured states).
- Focused English 1080p15 silent movies cover the pebble demonstration and the
  rectangle/definition sections. Their contact sheets and a native zoom frame
  were inspected. A real Kokoro English pebble pilot rendered at 480p15; its
  contact sheet was inspected. A scheduling replay reaches the spoken equality
  bookmark before starting the equality emphasis (0.0 s measured delay).
- Full-frame decoding completed for those three movies. Dense temporal sheets
  were generated, but their exhaustive visual review remains open. This is not
  continuous playback, listening, or final-production approval.

Evidence, exact source/data hashes, reports and reproduction commands:
[cs1 polish checkpoint](evidence/cs1-polish-20261108/README.md).

## Continue here

1. Continue Chinese motion review and broader native-resolution checks. English
   motion contact sheets were inspected for all 17 scenes; no continuous-playback
   approval is claimed. The focused native Euclid decoder generated 195 samples,
   whose exhaustive perceptual review remains open.
2. Complete narrated synchronization and listening checks, retaining the exact
   backend/voice and coverage. The existing Kokoro pilot covers only the English
   pebble demonstration; no Qwen or Chinese listening approval is implied.
3. Keep cs1's production gates open until those checks are complete, then advance
   to cs2. The two source polish checkpoints preserve bounded QA evidence.

Activate the existing toolchain first:

```bash
source /workspace/environment/activate.sh
.venv/bin/python tools/qa_series.py cs1 --lang en --cached-only --resume --timeout 900
.venv/bin/python tools/qa_series.py cs1 --lang zh --cached-only --resume --timeout 900
.venv/bin/python tools/qa_series.py cs1 --lang en --motion --cached-only --resume --timeout 900
PYTHONPATH=. .venv/bin/python docs/qa/evidence/cs1-semantics-20261108/decode_movies.py
```

The shell activation supplies the existing user-local `dvisvgm` and Chinese TeX
resources. Without it the first render failed with a missing `dvisvgm`; that
environment issue was resolved without changing project source.

cs2–cs61 remain queued for this polish pass. No whole-video completion is claimed.
