# Quant, Built: polish record

What each polish pass on the series changed, how it was checked, and what is still open. The per-part review logs
of the earlier passes (which chapters were inspected at which source revision) are in [`quant/`](quant/), moved
out of the part READMEs unchanged.

## Pass of 12 November 2026: the course layer

**Finding.** The 43 films were complete and in good shape: the series' tests passed, every part estimated at
52-69 minutes, and the layout preflight (`tools/qa_series.py`) on the two parts computed in this pass (1 and 10,
41 chapters) reported no warnings; rendered chapters of both were looked at. What the series lacked was
everything around the films: there was no course site, no statement of level per chapter, no hands-on material
a student could run without building a film, 26 part READMEs ended in QA logs, and the series README and
SYLLABUS still promised that hold-out outcomes are shown, which the shipped films do not do.

**Added.**

| What | Where | Check |
|---|---|---|
| A lab for every part on the House library: seeded, seconds, simulated data, asserts its own result, one figure | `videos/quant/labs/lab01.py` … `lab43.py` | `tests/test_quant_labs.py` (47 tests); also run in an environment with no manim or torch |
| The course table: level, prerequisites, question, story, hand-off, objectives per track, key results, chapter tiers | `videos/quant/course/` | `tests/test_quant_course.py` checks every chapter number against every manifest |
| The course site: a page per part, course, tracks, labs, reading and syllabus pages | `tools/course_site.py`, `videos/quant/course/site/` | built and opened in a browser: 48 pages, no script errors, no unrendered math (838 formulas), no horizontal overflow at 390, 768 and 1280 px |
| 44 interactives, one per part and one for the course page, canvas only | `videos/quant/course/site/widgets/` | each screenshotted and read; sliders exercised by the defaults; every one states its assumptions |
| GitHub Pages workflow | `.github/workflows/course-site.yml` | its commands were run verbatim in a clean Python 3.12 environment: 98 passed, site built in 67 s |
| `SharpePrecision`, an animated instrument for "what can Y years prove" | `explainer/quant/viz.py` | rendered in the four chapters below |

**Changed in the films.** The precision beat of the registration chapters was an equation and a text card. It
is now the same arithmetic as a moving picture: the sampling densities of an estimated Sharpe ratio for a
strategy with no skill and for a skilled one, narrowing as the years of test grow, with the t = 2 hurdle walking
in and live readouts. Narration is unchanged, so the Chinese narration tables are untouched; three on-screen
strings were added to `videos/quant/quant_text_zh.json`.

| Part | Chapter | Rendered (silent, 480p) | Chinese dry run |
|---|---|---|---|
| 24 | 13. Registration and holdout accounting | yes, frames read | passes, 0 strings left |
| 25 | 11. Registration and holdout accounting | yes, frames read | passes |
| 26 | 15. Registration and evaluation accounting | yes, frames read | passes |
| 33 | 10. An evaluation protocol | yes, frames read | passes, 0 strings left |

**Changed in the documents.** Review logs moved from 26 part READMEs to `docs/qa/quant/partNN.md`. The series
README and SYLLABUS now say what the films show about the Track Record (the evaluation protocol and its
arithmetic, not hold-out outcomes); SYLLABUS gained Section 1a, the standard for levels, tracks, labs and the
site.

**Not done, and why.**

- *No film was re-rendered at production quality and no narrated build was made.* Only the four changed chapters
  and four sample chapters of Parts 1 and 10 were rendered, silently, at 480p.
- *Only Parts 1 and 10 were computed here.* The READMEs of several later parts say not to run their full
  `compute` (it would register or open strategy experiments), so their caches were not rebuilt and their chapters
  were not preflighted in this pass.
- *About 65 other chapters are still mostly cards and equations* (a scan for chapters with at most one drawn
  object; list below). They are the natural next targets for instruments like `SharpePrecision`. The remaining
  registration chapters (Parts 27-32) have no precision beat to replace.
- *The site has no video embeds.* The films are not hosted from this repository; a part's page gives the build
  commands instead.
- *The site is English with each part's Chinese notes included from its README.* The course table (stories,
  objectives) has no Chinese edition yet.
- *GitHub Pages must be switched on once* by the repository owner: Settings → Pages → Source: GitHub Actions.

Chapters that are still text-led, by part (module names): 3 `s19_industry`; 5 `s22_research`; 17 `s12_production`;
18 `s11_rv`; 20 `s08_defaults`, `s09_altman`, `s15_whale`; 24 `s06_profit`, `s13_firms`; 25 `s08_fgx`; 26
`s03_survivor`; 27 `s15_firms`, `s16_envelope`; 28 `s10_transformers`, `s11_llms`, `s17_envelope`; 29 `s11_china`,
`s12_highflyer`, `s13_humans`, `s14_envelope`; 30 `s13_envelope`; 31 `s02_law`, `s12_envelope`; 32 `s04_voltarget`,
`s08_calendar`, `s09_envelope`, `s11_research`; 33 `s02_history`; 34 `s02_models`, `s04_pods`, `s06_risk`,
`s07_tech`, `s09_interview`, `s10_culture`; 35 `s10_hft`; 36 `s07_deep`; 38 `s02_business`, `s05_tick`, `s06_etf`,
`s08_industry`; 39 `s08_carry`; 40 `s03_coherent`, `s07_stress`, `s10_frtb`; 41 `s04_firesales`; 42 `s04_sims`,
`s06_llm`, `s09_stability`; 43 `s06_record`, `s08_open`, `s10_journey`; and the House chapters of Parts 7, 8, 17,
18, 20, 22, 24, 28-32, 39 and 42. The scan counts drawing calls in the scene file only, so a chapter that draws
through its part's `common.py` may be listed wrongly.
