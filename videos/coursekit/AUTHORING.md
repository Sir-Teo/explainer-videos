# Writing a part's course material

Every part of a course carries three things beside its film, and `tools/series_site.py` puts them on the part's
page. The worked example is *Statistics, Built* Part 12: read all three files before writing your own.

| What | Where | Example |
|---|---|---|
| The course entry | `videos/<series>/course/parts_AA_BB.py`, a `Part(...)` in `PARTS` | `videos/stats/course/parts_11_15.py` |
| The lab | `videos/<series>/labs/labNN.py` | `videos/stats/labs/lab12.py` |
| The interactive | `videos/<series>/course/site/widgets/parts_AA_BB.js`, `W.<name> = function (el) {...}` | `videos/stats/course/site/widgets/parts_11_15.js` |

Check your parts with `python tools/check_course.py <series> N N ...`. It checks the entry against the manifest,
runs the lab, builds the page, and opens it in a browser at desktop and phone width, dragging every slider to both
ends and pressing every button. It must end with `ALL OK`. Then look at the page yourself: take a screenshot of the
interactive and of the lab's figure (the page is in the folder the checker prints) and fix what reads badly.

## Sources: read these first, for every part

The film is the authority. The course material describes what the film teaches, so before writing a part read:

1. its `manifest.py` (the chapters, in order, with their numbers);
2. its `README.md` (what the part covers, what is computed, the problems, the sources);
3. its entry in the series' `SYLLABUS.md` (`Part N · ` heading) and its row in the series' `README.md`;
4. the scene files (`sNN_*.py`) wherever the README does not tell you what a chapter derives or which numbers it
   shows. Read the narration (`self.voiceover(...)`) of the chapters you tag and of anything you quote.

Do not run a part's `compute.py` or build a film. Do not state a number, a date or an attribution that the part
does not state; if you need one, take it from the README or the narration.

## The course entry

`Part` is documented in `videos/coursekit/__init__.py`. What each field must be:

- `level`: the tier at which the part can first be followed, `"U"`, `"M"` or `"D"`. The series' `course/__init__.py`
  says what the tiers are called there. A part of a doctoral stage is `"D"`; a part anyone on the first track can
  start is `"U"`.
- `question`: the one question the part opens with, in plain words, ending in a question mark.
- `story`: the arc in one paragraph (five to eight sentences): where it opens, what is built or proved, where it
  turns, how it ends. Concrete nouns from the film (the historical episode, the device, the dataset), no praise.
- `handoff`: what the part leaves for later parts, naming them ("returns as ... in Part 23").
- `outside`: what a viewer needs from outside the series, or from which earlier stage.
- `prereq`: the earlier parts of the same series to watch first (a tuple of numbers, at most four).
- `objectives`: for each of `"U"`, `"M"`, `"D"`, `"I"`, one to three things a student can *do* afterwards, each a
  full sentence starting with a verb (Compute, Derive, Prove, Explain, Implement, Diagnose, ...), specific to this
  part. `"D"` is the research tier (prove it in generality, state the open problem); `"I"` is practice (use it, report
  it, know where it fails in the field).
- `results`: three to six key results as `(name, TeX)`. Raw strings, no dollar signs, KaTeX-compatible
  (`\operatorname`, `\mathbb`, `\tfrac`, `\Bigl ... \Bigr` are fine; no `\begin{align}`; use `\text{...}` for words).
  Keep each one to what fits a card about 460px wide: `\text{...}` does not wrap, so split a long statement into
  two results. When a formula is split over adjacent strings, leave a space after a command at the join
  (`r"...,\qquad " r"Cr(...)"`), or the two join into `\qquadCr`.
  For a part whose results are not formulas (history, software practice, ethics), state them as short
  propositions in `\text{...}` or as the defining inequality, law or recurrence the part uses. Check every formula.
- `U`, `D`, `I`: the chapters whose home tier that is, by the number in the chapter's title (0 is the cold open).
  Chapters in none of them are `M` (in a `"D"`-level part they default to `D`, in an `"M"`-level part to `M`). The
  last chapter (the recap) belongs to every track and is never listed. A chapter without a number is listed by
  its scene module name (`"s12_exam"`). Tag from what the chapter does, not from its position: `U` if a
  first-track student can follow it, `D` for the full-generality proof, the frontier and open problems, `I` for
  how it is used, measured, shipped, or how it failed in the field. Most parts have some of each; a part needs at
  least one `D` or `I` chapter.
- `widget`: the name of the part's interactive, lowercase letters and digits, unique in the series, specific to
  the idea (`leastsquares`, not `demo12`).
- `also`: optional `(label, repo path)` pairs for companion material in this repository (another film, a library
  module). The path must exist.

Write the prose as the series' READMEs do: plain declarative sentences, the film's own terms, no marketing words,
no em dashes (use a colon, a comma or a full stop), straight quotes.

## The lab

A lab is one experiment that makes the part's central claim checkable: simulate or compute, compare with what the
theory says, assert the comparison, draw it. See `videos/coursekit/labs.py` for the contract and the helpers
(`labs.Lab`, `labs.figure`, the palette `labs.BLUE`, `labs.GOLD`, ...).

- The docstring starts `Lab N: ` and says what the lab does in one line. `TITLE`, `GOAL` (one or two sentences),
  `TASKS` (exactly three concrete things to change next, each a sentence a student can act on), `run(seed=0)`.
- numpy, scipy and matplotlib only, plus the series' own library where it imports without manim: `explainer.stats.kit`,
  `explainer.stats.world`, `explainer.stats.prob`, `explainer.stats.museum`; the non-drawing modules under
  `explainer/cs/` (Pebble in `explainer/cs/pebble/`, and the per-topic packages); `explainer.philosophy.reasoner`;
  `explainer.ai.autodiff`. Prefer the series' library: the lab is that library in miniature. Read the module
  before calling it. Modules that import manim (`viz.py`, `gates.py`, each package's `__init__.py`) cannot be used.
  `from videos.coursekit import labs` must come before any `explainer` import (it is what lets the libraries
  import without manim), whatever an import sorter says. A part's own numpy-only modules
  (`videos/ai/ai19/attn.py`) may be imported too.
  No torch, pandas, sklearn or statsmodels; no files, no downloads, no network.
- Seeded: all randomness from `np.random.default_rng(seed)` (or the library's own seed argument), so two runs
  print the same table.
- It runs in a few seconds (aim under 10; the limit is 60) and asserts its result inside `run()`: a Monte Carlo
  estimate against its closed form, an algorithm's output against a brute-force answer, an inequality that must
  hold. An assertion that cannot fail is not a check. Tolerances wide enough to pass for other seeds too (try
  seeds 1 and 2).
- `lab.row(label, value)` at least three times: the numbers a student should look at, with the theoretical value
  beside the measured one. `lab.note`: one sentence saying what the numbers mean.
- One figure, `labs.figure(...)`, usually two panels, titled, axes labelled, legend where there are several
  series. It must read on its own.

## The interactive

One canvas widget per part, on the site's small library: read `videos/quant/course/site/widgets/00_core.js`
(`QB.widget`, `Axes` with `line`, `area`, `bars`, `dots`, `hline`, `vline`, `text`, `legend`; `QB.rng`, `QB.mean`,
`QB.sd`, `QB.hist`, `QB.linspace`, `QB.cdf`, `QB.fmt`, `QB.pct`; the colours `QB.C`) and two or three widgets in
`videos/quant/course/site/widgets/` for the idiom. Your file wraps its widgets in one IIFE, as the example does.

- It lets the reader *move the idea*: two to four sliders (and buttons such as "New sample") whose effect on the
  picture is the point of the part. The best ones show a claim holding and then breaking.
- `title`, `sub` (two or three sentences: what is drawn and what to try), `readout` (the numbers that change),
  `note` (the assumptions; say "Simulated data." when it is). One or two panels; `height` about 300.
- Everything is computed in the browser, in plain ES5-style JavaScript, seeded with `QB.rng(s.seed)`: no network,
  no libraries, no `innerHTML`, no globals. Keep the work per redraw small (it redraws while a slider moves): under
  about 20 ms.
- No value may become `NaN`, `Infinity` or `undefined` anywhere in the sliders' ranges, alone or together; the
  checker drives every slider to both ends at once and reads the readout. Guard divisions and logarithms.
- Custom drawing beyond `Axes` (a graph, a grid of cells, a machine's tape) uses `g.ctx` or `g[i].ctx` with
  `g[i].box` directly; keep text at 11px or more and inside its box at 390px width (panels stack on phones).
- Colours carry meaning consistently within the widget and are named in a legend or in the text.

## What not to touch

Write only your own three kinds of files for your own parts. Do not edit the kit, the tools, the tests, the
series' `course/__init__.py`, another range's files, the films, or their READMEs; do not commit. If the kit or
the checker is wrong or missing something, say so in your report instead.
