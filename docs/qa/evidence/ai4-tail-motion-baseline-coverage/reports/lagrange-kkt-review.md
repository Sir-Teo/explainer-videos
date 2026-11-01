# Lagrange/KKT English and Chinese motion review

No held/narrated-state visual defect found in reviewed selected times. Ordinary temporary old-row-copy overlaps documented during TransformMatchingTex; no required repair.

All 128 unique sheets and 47 targeted reveal sheets were actually viewed. The 1,521 selected times map by exact PNG SHA256 to 1,010 representatives. Another 362 frame views cover every encoded frame in the declared reveal windows. Sixteen priority frames were also inspected at native 854×480. Continuous perceptual playback and audio listening were not performed.

| Case | Decoded | Selected | Unique PNGs / sheets | Reveal frames / sheets | Native | Max selected gap |
|---|---:|---:|---:|---:|---:|---:|
| en/Lagrange | 2,746 | 377 | 268 / 34 | 100 / 13 | 4 | 1.000000 s |
| zh/Lagrange | 2,902 | 386 | 274 / 35 | 88 / 11 | 4 | 1.000000 s |
| en/KKT | 3,024 | 364 | 223 / 28 | 105 / 14 | 4 | 1.000000 s |
| zh/KKT | 3,149 | 394 | 245 / 31 | 69 / 9 | 4 | 1.000000 s |

## Findings

Native English and Chinese views confirm the gradient and constraint legend, zero tangential reading at the circle candidate, and all three held derivation rows with regularity and necessary-but-not-sufficient caveats. The displayed candidate x = (0.783, 0.622), lambda = 0.626, residual 2e-8 and solver verdict agree with the recorded inputs. The maximum-entropy constraints, softmax, inverse-temperature beta = 0.371, six probability bars and 1e-4 comparison tolerance are readable. The RL panel states the positive beta/reference assumptions and distinct temperature convention; both probability panels and the tolerance label are clear. Open contours meet the declared rectangular sampling bounds and are expected clipping.

Native English and Chinese views confirm constraint qualification, multiplier/slackness conditions, and the inactive/active wall examples with mu = 0 and 1.6. The finite-grid note states x in [-2.2, 2.2], x spacing 1e-5, mu spacing 0.01, and the uncertified continuous-bound caveat. The plots show grid estimates p = -1.07, d = -1.75 and gap = 0.68. The SVM objectives both round to 0.726908. Solver residuals/tolerances and intercept stationarity are readable. Three support-point rings match three multiplier bars and the numerical legend: alpha threshold about 7e-7 and margin threshold 1e-6. The positive-multiplier implication and degenerate reverse caveat are visible. Separator and margin lines meet the intentional plot rectangle.

Temporary moving copies overlap equations and occasionally prior notes for about 0.73–1.00 s. Each clears before the held annotations. No persistent ghost, clipped held equation, broken legend, or inconsistent support/slackness count was observed. The table gives conservative visually observed copy spans and the next clean frame.

| Case / method / step | Copy frames | First clean frame / time |
|---|---|---|
| en/Lagrange / derive / 1 | 859–870 | 871 / 58.066341 s |
| en/Lagrange / derive / 2 | 959–969 | 970 / 64.666341 s |
| en/Lagrange / maxent / 1 | 1572–1585 | 1586 / 105.732682 s |
| en/Lagrange / maxent / 2 | 1648–1661 | 1662 / 110.799349 s |
| zh/Lagrange / derive / 1 | 919–930 | 931 / 62.066341 s |
| zh/Lagrange / derive / 2 | 1014–1024 | 1025 / 68.333008 s |
| zh/Lagrange / maxent / 1 | 1660–1673 | 1674 / 111.599349 s |
| zh/Lagrange / maxent / 2 | 1742–1755 | 1756 / 117.066016 s |
| en/KKT / duality / 1 | 979–990 | 991 / 66.066341 s |
| en/KKT / duality / 2 | 1142–1155 | 1156 / 77.066341 s |
| en/KKT / duality / 3 | 1268–1279 | 1280 / 85.333008 s |
| zh/KKT / duality / 1 | 1046–1057 | 1058 / 70.533008 s |
| zh/KKT / duality / 2 | 1218–1232 | 1233 / 82.199674 s |
| zh/KKT / duality / 3 | 1343–1356 | 1357 / 90.466341 s |

## Evidence and limits

All four original structured statuses are `passed` with `warnings: []`. Every raw render log preserves the Manim warning that the `shortest=1` option and metadata comment were unused. The broad fingerprint `12e053536905bd3fac33441c6d0781b7b32eb676ab743c59340aea886a30f5a3` matches all four records. Direct saved scene/helper/language-table/tool hashes, input metadata and input SHA256 identities match current disk. Original and frozen movie/result hashes also match at completion. Full paths and hashes are in `lagrange-kkt-review.json` and each case’s `freeze.json`.

Copied `qa_motion` provenance is null; `freeze.json` explicitly binds each original result and movie. Original automated-audit pending-review fields were preserved. Manual completion is recorded in `actual-views.json`, checked against every expected sheet and hash. `unique/review-plan.json` maps every selected time to the exact-PNG representative actually viewed.

All encoded frames were decoded and analyzed, but frames outside selected times and targeted windows were not all visually inspected. The original unextracted gaps remain enumerated in each `audit/result.json`; targeted windows add coverage without rewriting that original record. Low-resolution thresholds and a maximum selected gap of 1 s cannot prove continuous perceptual quality. Saved-source hash equality does not independently reconstruct loaded interpreter modules.

## Optional local edit proposals

No repair is required by the held-state evidence, and no edits were made. If readability during every intermediate transform is desired, the observed copied-row motion could be removed with local `step(..., transform=False)` calls while keeping the shared ladder unchanged:

- `Lagrange.derive`: steps 1 and 2, `s16_lagrange.py:160,162`.
- `Lagrange.maxent`: steps 1 and 2, `s16_lagrange.py:203,205`.
- `KKT.duality`: steps 1, 2 and 3, `s17_kkt.py:143,145,147`.

These are optional editorial proposals supported by the frame spans above, not unresolved held-state bugs.

No repository, cache, source, endpoint-package or handoff-package edits, renders, model runs, recomputations, deletion or commits were performed by this reviewer. No blockers remain.
