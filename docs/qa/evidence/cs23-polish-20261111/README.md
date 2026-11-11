# CS23 Optimization — source and preview checkpoint

Status: **source/preview checkpoint verified**. Candidate04 is frozen at
`5cc09b851821127c6e83461a7482c3376c20693ef6ea281e2f7b8886eae149e7`.
The strict verifier passes against the actual current artifacts. This checkpoint
covers source, numerical integrity and sampled previews; the four production
release gates below remain open.

## Source and numerical work

The instrument now checks finite compatible inputs and explicit stopping states;
uses exact determinants, knapsack ratios and branch bounds; handles graph iterators
and empty instances; and uses stable logarithmic weights. The local vector
MAX-CUT objective is distinguished from independently certified dual upper bounds.
The finite polytope experiment certifies boundedness before enumerating vertices.

All 15 producers were forced under one source snapshot. Every payload changes
from the preserved original. Schema-2 caches bind complete compute, instrument and
reference source hashes. Ten timing groups retain three raw trials each; input
preparation and independent validation are outside the measured intervals.

- All 27 unit tests pass. A separate C++ reference, compiled with UBSan and GMP,
  agrees on all 1,491 fixtures, including all illustrated determinant minors,
  measured integer knapsacks and exact cuts.
- Independent numerical checks include 33 exact Klee–Minty cases, 201 perturbed
  or random LPs, eight ellipsoid regions, 36 barrier points, 201 matching LP
  certificates, 41 integer knapsacks, 101 vertex covers, 66 set covers, 42 small
  TSP optima and 31 exact cuts.
- Full-trace references check 25 paging results and nine cyclic examples.
  Six Hedge horizons, four game rows and 101 certified bounded polytopes also
  pass. Full inputs, choices, certificates and source hashes are retained in
  `rebuilt-numerical-audit.json` and the payloads under `final-data/`.

The bilingual revision distinguishes theorem assumptions, finite observations,
local certificates, arithmetic and bit costs, and executed algorithms from cited
research. It includes three executed stopping/rounding/dual-bound witnesses,
68 exact narration pairs and six worked bilingual exercises. Pebble guidance is
a bounded fixed-size design with an independently checked arithmetic trace;
no Pebble port or emulator execution is claimed.

## Preserved findings and repairs

The original source, history, all original producers and all 32 original bilingual
endpoint captures were preserved and inspected before source changes. Eighteen
original endpoint reviews passed; fourteen required repair.

Candidate01 retained a measured ellipsoid cue 6.675 seconds late. Candidate02
moves the volume-bound cue after the first two cuts while retaining all nine
cuts and their original animation speeds. Its actual 226 cue requests pass.

Native inspection of candidate02 exposed an obsolete `O(mn)` tableau caption.
The full tableau includes slack columns, so candidate03 corrects that caption
to `O(m(n+m))` in both languages. Earlier sampled approvals that missed it are
explicitly superseded. Another native inspection found transportation “store”
headers translated using the memory term “writeback.” Candidate04 adds three
episode-local Chinese destination labels. Both findings and every completed
superseded movie, raw receipt and reviewed image remain in the candidate archives.
Candidate03's stopped cue audit covers 50 blocks and is explicitly partial.

Review inheritance requires identical actual PNG bytes for chapter sheets, or
identical complete actual movie bytes for native/narrated clips. Pending and
negative reviews cannot be inherited. Reviews made after archiving retain the
original archive-time reports and a separate dated review history. Raw render
receipts retain their actual source fingerprint throughout.

## Current validation

All 32 candidate04 endpoint previews and 32 silent chapter movies pass sampled
visual review: 572 endpoint appearance states, 1,280 temporal samples and 84,870
decoded motion frames. Thirty-seven chapter reviews inherit only through identical
actual PNG bytes; 27 receive fresh inspection. The corrected Chinese transportation
endpoint and both full-tableau captions receive fresh inspection.

All 94 focused 1080p15 native clips (47 methods in each language) decode 76,384
frames. Their 2,256 samples and 94 full native stills have positive sampled reviews:
29 inherit through identical complete movie hashes, and 65 receive fresh review.
Four actual English narrated pilots—Simplex, IntegerPrograms, MaxCut and Frontier—
decode 13,352 frames plus audio. All 160 samples and four stills have positive
sampled visual reviews; IntegerPrograms and MaxCut preserve positive reviews
through identical complete archived movie bytes. Continuous listening is pending.

All 68 current English speech blocks pass automated signal/alignment checks
(45.9646 minutes), and all 226 actual cue requests meet the 250 ms threshold.
Every normalized engine token sequence matches its input; no phonemizer warning
leads remain. Canonical source pairs and actual runtime captures each cover 68/68
bilingual blocks. All 589 captured captions have zero unresolved explanatory
translation leads; all 31 retained names/notation and four numeric-unit leads are
individually classified.

Five raw sparse-content warnings remain unchanged. Fresh inspection of all five
40-sample overviews and three exact movie frames per interval records their
dispositions in `warning-reviews.json`: English Tsp (3 seconds), English Frontier
(1.5 seconds), English Convex (4 seconds), Chinese Convex (4.25 seconds), and the
Chinese Hook introductory title interval (7.75 seconds). The Hook interval shows
the outgoing diet fade, the “three kinds of answer” title during its introductory
sentence, then the LP figure at its content bookmark. The other four span section
fades, titles and the first explanatory content. All five have zero scanner blank
runs. These sampled visual dispositions do not close listening or production-pace
review. The motion queue's return code 1 records those original warnings; complete
actual movies and the strict accepted-disposition checks pass.

## Evidence and reproduction

`source-freeze.json` binds the exact source, numerical payloads and runtime
narration captures. `compute-revised-completion.json`,
`rebuilt-numerical-audit.json`, `native-complete-verification.json` and
`tests-final.log` retain the numerical receipts. `candidate04-*.log` and
`candidate04-automated-completion.json` record the actual queue outcomes.
`verify_checkpoint.py` passes against the final actual artifacts; its
`verification.json`, `final-frame-integrity.json` and `verify-checkpoint-final.log`
are the final integrity records. Original, negative, partial and superseded
receipts remain preserved alongside the final evidence.

From the repository root, activate `/workspace/environment/activate.sh` and run
the packet's `verify_checkpoint.py` with `PYTHONPATH=.`,
`OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`. Recomputing benchmarks produces
a new measurement snapshot; preserve this packet before rebuilding data or
rendering with changed sources.

Four production release gates remain open: continuous narrated audiovisual and
listening review; Chinese synthesized speech and listening; whole-video native
production review; and production runtime at the selected narration pace.
