# Planning a part's expansion (shared brief for every planning agent)

Goal: a plan that turns Part N of *Quant, Built* (`videos/quant/quantN/`) into a 50–60 minute lecture that can
replace a university course: 3Blue1Brown-grade moving visuals, full technical depth, hands-on like *AI, Built*
(models fitted and trained on screen and replayed, code labs, simulations running live), complete coverage of the
part's textbooks and papers, and how hedge funds, banks, exchanges and trading firms actually do it (public record),
plus the 2023–2026 frontier. The owner's words: "as complete as possible (all the textbooks, papers, and frontier
systems by hedge funds or trading things), heavy focus on visualization so that users can see how cool those are";
"people might actually watch this in replacement of the college lectures (think of 3b1b)"; "should have some
hands-on things — see how the AI series actually visualizes and trains a lot".

Write the plan to `/tmp/claude-0/-home-user-explainer-videos/e79d9910-3070-5b5d-804d-ed98af9b99fd/scratchpad/plans/quantN.md`
(about 600 lines). Edit no repository file. A finished example of the format: `videos/quant/plans/quant5.md`; the
implementation brief the next agent will follow is `videos/quant/plans/IMPLEMENT.md` (read both first).

## Read

`CLAUDE.md`; `videos/quant/SYLLABUS.md` section 1 (the standard: chapters of about 3 minutes, 16–20 per part, a
signature visual per chapter, derivations with reasons, labs, replays, industry and frontier chapters) and your
part's section-6 entry; `videos/quant/READING.md` (your part's textbook map and paper list);
`videos/ai/LECTURE_GUIDE.md`; your part's existing code (`manifest.py`, `compute.py`, every scene, `README.md`);
the instruments in `explainer/quant/__init__.py` and `explainer/quant/viz.py` (`lab_card`/`lab_run`,
`TrainingReplay`, `seed_band`); the House library in `explainer/quant/house/`; neighbouring parts' plans in
`videos/quant/plans/` so you do not duplicate their material. Measure with `python tools/lecture_length.py quantN`.

## The plan's sections (as in quant5.md)

1. Current state: chapter by chapter, minutes, depth, what is computed, what is missing.
2. Audit: (a) syllabus items → chapters; (b) every core section of each textbook in READING.md → proposed chapter
   or another part (check tables of contents against the publisher; mark anything unconfirmed *(verify)*);
   (c) every paper on the part's list → where it appears; propose additions (2023–2026 especially).
3. The chapter list: hook + 16–19 chapters + outro, 50–60 min in total. Per chapter: goal; narration beats; every
   derivation step in LaTeX with its one-line reason; a concrete Manim design for the signature visual (3D where there
   are two inputs; things that move, fill, converge, re-weight); the computed experiment with data source and
   expected output (run it on the cached data where feasible, so numbers are real); hands-on elements; a
   pause-and-predict question; module name (keep existing module names for kept chapters).
   3b. Hands-on summary: at least three labs (exact House functions and line ranges, ≤12 lines), every fit/training as
   a replay with seeds as bands, live simulations, compute items with CPU-minute estimates (about 2 CPU-hours total,
   seeded, resumable).
4. Industry and frontier: facts with URLs to primary sources (regulators' orders, exchange rulebooks, company
   filings, papers). Firms only from the public record, "as reported by X", allegations labelled as allegations.
   Anything you could not confirm: marked *(unverified)*.
5. A paste-ready revised SYLLABUS.md section-6 entry.
6. Minutes per chapter, new House functions with tests, data needed (through the data layer), risks.

## Rules

Many agents run in parallel on a 4-core machine and share one web-search budget: be economical (prefer WebFetch on
primary sources you can name; at most about 30 searches), use `.venv/bin/python` with `OMP_NUM_THREADS=1` for probe
runs, keep probes under a few CPU-minutes each, put probe scripts and downloads in the scratchpad (never in the
repo), and do not modify `videos/quant/data/manifest.json`. No installs. No model identifiers or personal emails.
Report briefly when done: current vs planned minutes, the biggest gaps, numbers you ran, what remains unverified,
and decisions for the lead.
