# Itô retained-row reveal regression

Source `3cbd2023…` uses local `transform=False` for four new-row reveals. Both original complete selected-image reviews remain historical. Fresh EN/ZH movies resolve the observed transient retained-row doubling.

| Scope | EN | ZH |
| --- | ---: | ---: |
| Automatically decoded native RGB frames | 2,399 | 2,485 |
| Changed frames (four 18-frame runs) | 72 | 72 |
| Current selected-time union | 468 | 460 |
| Every encoded proof-window frame actually viewed (includes neighbors) | 80 | 80 |
| Novel nonwindow images actually viewed | 3 | 4 |
| Other selected times inherited by exact PNG from completed actual review | 385 | 376 |
| Chronological sheets actually viewed | 11 | 11 |
| Additional native854×480 critical checks | 3 | 3 |
| Held endpoint exact-PNG inheritances | 14 | 15 |

All 4,740 other decoded frames are pixel-identical to the before movies; every old/new decoded PTS is exactly equal. This automatic whole-file comparison does not mean every frame was perceptually inspected. All four changed windows plus one encoded neighbor on each side were inspected as chronological still images. Every new selected image was viewed; unchanged selected images inherit only exact PNG matches to recorded actual prior views. The six native before/after pairs show new partial lines separated from clean retained identities. No further visual defect was found in this scoped regression.

EN raw status remains `needs-review` with `source-changed-during-render`; ZH is `passed`, no warnings. Both endpoint records passed without warnings. Raw records, direct source and data hashes remain preserved. These direct observations do not assert all historical imported bytes or broad aggregate-source currency.

Each language folder contains compressed exact per-time mappings, original actual review, current actual page receipts, all-frame RGB hashes, exact PTS comparison and raw records. The original decode comparison uses nominal frame-index/15 run times; `pts-comparison.json.gz` supplies actual mux-quantized PTS. A local extraction wrapper first failed on a logical `frames/` path mismatch; its failure is retained, complete existing EN PNGs were reconciled before continuation, and no producer/source/movie was modified.

This is silent480p15 selected-image/every-frame-window QA. Continuous perceptual playback, listening, narration sync and native1080 motion remain unverified. No movie is stored in this Git evidence package; frozen full movies and full selected PNGs remain in cloud runtime.
