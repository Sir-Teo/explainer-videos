# Computer Science, Built — sequential polish

Work on `computer-science-built`, one video at a time. Current video: **cs1,
What Is a Computation?** Do not advance to cs2 yet. This ledger describes the new
polish pass; the syllabus's earlier draft-preview claims are separate.

## Checkpoint, 8 November 2026

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

1. Repair Universal next: its completed English capture has 20 states and a
   `blank-narration-beat` warning at 61.0 s, confirmed in its contact sheet.
   `machine_u()` waits on bookmark `a` over an empty screen while saying
   “Now the key idea.” Show a relevant visual immediately, rerender and review.
   The before capture is retained in the checkpoint. Then continue English from
   Models onward in manifest order, inspecting every result, warning and sheet.
2. Continue Chinese cs1 from Engines onward. Keep narration translation, geometry,
   and visual inspection separate from mere successful execution.
3. Review motion around tape updates, diagonalization, reductions, and busy-beaver
   displays, including native-resolution readability. Resolve educational/source
   issues discovered by those checks.
4. Complete narrated synchronization and listening checks, retaining the exact
   backend/voice and coverage. The existing Kokoro pilot covers only the English
   pebble demonstration; no Qwen or Chinese listening approval is implied.
5. Commit the remaining cs1 repairs and checkpoint before advancing to cs2.

Activate the existing toolchain first:

```bash
source /workspace/environment/activate.sh
.venv/bin/python tools/qa_series.py cs1 --lang en --cached-only --resume --timeout 600
.venv/bin/python tools/qa_series.py cs1 --lang zh --cached-only --resume --timeout 600
```

The shell activation supplies the existing user-local `dvisvgm` and Chinese TeX
resources. Without it the first render failed with a missing `dvisvgm`; that
environment issue was resolved without changing project source.

cs2–cs61 remain queued for this polish pass. No whole-video completion is claimed.
