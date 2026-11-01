# Arithmetic row timing repair

Only s09_arithmetic.py changes. Both encoder row loops use remaining speech-cue budgets with explicit frame reservation; the nested add_row receives optional scroll_time=0.5, preserving other calls/defaults. Narration, all marks, math, row order, data and speech-master metadata remain unchanged.

Six focused runtime tests pass1.597s. Actual source nested add_row executes inside a real closure (nonlocal lines preserved), with controlled object interfaces and installed frame-clock methods. All24 supplied targets across10utterances reconstruct exactly. Original second-loop0.17s overrun is reproduced. Both loops pass18current checks at15/30/60fps and adverse0/0.49/1frame phases, with unchanged animation arguments exceptduration. Full per-stage requested/quantized times and conservative settled-row reading estimates are in phase-proof.json/receipt.json.

No Scene, render, decoder, data producer/provider or audio access occurred. Synthetic shapes/numbers serve only the actual function's constructor interface; this does not verify default-data geometry. The initial fixture's nonlocal compile failure is preserved, and its correction wraps the untouched nested function rather than changing its semantics.

Controlled preflight source clearance only. Source-clock completion/retention is not visible-pixel readability, full motion or listening approval. Root775fullsuite predates this repair. Physically impossible budgets retain positive frames and no synchronization guarantee. No source overlay registration, staging, commit or push was performed.

Root integration preserves every original fixture and the initial nonlocal-closure fixture error. The same six tests are now portable at `tests/test_ai1_arithmetic_timing.py`, loading exact gzip fixtures from this directory; that portable run passed in1.567seconds. Original runtime test passed separately; counts are not added. The earlier775 whole-repository run predates this source and is not claimed for it. Strictv9 registration and actual production-frame/pacing/listening approval remain pending; all ten speech masters are preserved as supplied metadata, not locally verified audio bytes.
