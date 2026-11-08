# Computer Science, Built — sequential polish

Work on `computer-science-built`, one video at a time, with separate commits.
Current video: **cs2, Proof and Counting**. CS1's source/preview polish checkpoint
is complete at the scope below. Its production release gates remain open; this
ledger does not treat sampled previews as listening or final-production approval.
The syllabus's earlier draft-preview claims are separate.

## Final CS1 preview checkpoint, 8 November 2026

- 34 current endpoint cases pass with zero warnings: English 319 states and
  Chinese 320 states. Every chapter's visual overview was inspected.
- 34 current silent 480p15 motion previews: 17 English and 17 Chinese. All 1,360
  sampled contact-sheet frames were inspected. Every movie decodes successfully:
  117,504 frames total. English has zero warnings. Chinese has 16 zero-warning
  cases and one reviewed Frontier transition alert.
- The Chinese pass caught a seven-second heading-only hold before the million-
  round data table. Show the table during its introduction. The remaining
  two-second scanner alert spans the section fade and table reveal; the saved
  12-frame sequence was inspected. Raw `needs-review` status remains intact.
- All 113 English Kokoro `af_heart` narration blocks have current, completed
  automated signal/alignment reports with zero issues, plus waveform hashes.
- Complete English Hook/Algorithms narrated previews decode with audio and have
  inspected 40-frame overviews. A real-speech scheduling replay checks 38
  bookmark calls with none requested more than 250 ms late. Listening is pending.
- Three focused Chinese 1080p15 clips have inspected contact sheets/native stills
  and 2,030 decoded frames. All 195 selected temporal samples from the English
  Euclid clip were reviewed as thumbnails across 25 sheets.
- All 24 numerical data hashes remain unchanged. No simulator or math code was
  changed; the earlier 22 passing tests remain linked evidence.

[Final source-bound evidence](evidence/cs1-semantics-20261108/README.md).

CS1 release work still open: continuous narrated audiovisual/listening review
beyond the two English opening chapters, Chinese speech/listening approval, and
native-resolution review of the whole video beyond focused pilots. No published
or final-production video is claimed.

## Earlier semantic checkpoint — `b9332b7b`

That checkpoint had **34 clean endpoint cases: 17 English (320 states) and
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

At that checkpoint, all 24 numerical files retained their earlier hashes. Fifteen
English Kokoro utterances had completed automated reports with zero issues. The
final checkpoint above supersedes that bounded audio coverage.

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

1. Run cs2's numerical computations and existing counting tests; preserve their
   evidence. Read its source and begin with the 15-puzzle opening.
2. Review cs2's English/Chinese endpoints, then motion and educational accuracy.
   Repair concrete defects and recheck affected evidence before committing.
3. Keep release gates distinct from this source/preview polish pass. CS1's open
   listening and native-production work remains listed above.

Activate the existing toolchain first, then start cs2:

```bash
source /workspace/environment/activate.sh
.venv/bin/python -m videos.cs.cs2.compute
.venv/bin/python -m unittest discover -s tests -p test_cs2_counting.py -q
.venv/bin/python tools/qa_series.py cs2 --lang en --cached-only --resume --timeout 900
.venv/bin/python tools/qa_series.py cs2 --lang zh --cached-only --resume --timeout 900
```

Inspect endpoints before the full motion pass. CS1 reproduction commands remain
in its linked evidence packet.

The shell activation supplies the existing user-local `dvisvgm` and Chinese TeX
resources. Without it the first render failed with a missing `dvisvgm`; that
environment issue was resolved without changing project source.

cs2 is active; cs3–cs61 remain queued. No whole-course or production completion is claimed.
