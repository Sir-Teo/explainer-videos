# Music, Built: Part 42, Composing

Part 42 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act VII, *The Craft*. Beethoven's sketchbooks of 1822 to 1824 show
the Ode to Joy approached in draft after draft; in 1757 Kirnberger published a way to compose minuets with dice; in 1957
a computer in Illinois wrote a string quartet by generating notes and rejecting those that broke rules. This part treats
composing as search under constraints and builds a searcher: the motive and its operations, developing variation, kinds
of variation, planned tension, constraints counted exactly, the dice games, generate and test, Markov chains, grammars
and evolution, and a generate-and-test composer whose critics are the series' own rules, shown with the drafts it threw
away. The tools are Monochord's (`explainer/music/monochord/composer.py`). Every motive, table and melody is ours or was
generated here; the Ode to Joy (1824) and the Tune are in the public domain. Published findings are the ones listed
under Sources.

* **Draft after draft.** An ear question (two melodies from the same motive and chords: which did the program keep?);
  Beethoven's search; the Ode to Joy's first two phrases (29 moves: 20 steps, 9 repeated notes, no leap), heard; the plan.
* **1. The motive and its operations.** Schoenberg's definition; our motive (E D C G); eight operations, each heard; an
  ear question (upside down or backwards?); diatonic operations; motives that carry pieces.
* **2. Developing variation.** Schoenberg's sentence; a sentence of ours grown from the motive, heard (41 notes, every
  one before the cadence from the motive); what it is made of; "Brahms the Progressive"; unity and variety, measured.
* **3. Kinds of variation.** Theme and variations (Mozart's K. 265 on the Tune, the *Goldberg* and *Diabelli*
  variations); the Tune varied four ways, heard (ornamental, rhythmic, harmonic, character); what each keeps; grounds.
* **4. Planning tension.** What makes tension (Krumhansl; Farbood; Lerdahl and Krumhansl); one motive, two plans, with
  the searcher's results (correlation 0.94 with a late plan, 0.61 with an early one); both heard; where the peak goes.
* **5. Constraints as engines.** The funnel: 2,562,890,625 eight-note melodies on fifteen white keys, then 102,515,625,
  800,243, 12,271, 9,872 and 9,252 as five rules are added, counted by dynamic programming; how; Stravinsky; constraints
  that made music.
* **6. Dice games.** Kirnberger (1757), C. P. E. Bach, the 1792 game printed under Mozart's name; our table of 176 bars;
  two minuets thrown, heard; the count (11^16 naively, about 1.6 × 10^13 distinct); what the dice favour (41.0 bits
  against 43.9 if every minuet were equally likely); what the dice game is.
* **7. Generate and test: the *Illiac Suite*.** Hiller and Isaacson; our rules; one run draw by draw; the line, heard; 200
  runs (277 draws a line on average; 69% of rejections at the cadence); the four experiments.
* **8. Chains, grammars and evolution.** Markov chains over the series' 51 major-key tunes; an ear question (which chain
  remembers four notes?); copying measured (longest verbatim run: 6.1 notes for order 1, 11.7 for order 4); grammars;
  a genetic algorithm (best fitness 0.84 to 0.98 in 40 generations); its fittest melody, heard.
* **9. A searcher with critics.** Hard and soft critics from Parts 14, 16 and 18 and chapters 2 and 4; the loop; 2,000
  drafts (1,312 refused for leaps, 332 for parallels, 178 for range, 14 for harmony; 164 scored); three rejected drafts,
  heard; the best score so far; the kept draft (number 1,205), heard; David Cope's recombination.
* **10. Frontier: judging creativity.** Boden's three kinds; this part's programs in her terms; evaluation (Ritchie;
  Jordanous; Pearce and Wiggins); co-creative tools; ★ research problem: can novelty and value be measured separately,
  and do they trade off?
* **Variation 42, recap and problems.** The searcher composes eight bars from the Tune's first four notes (draft 1,554 of
  3,000 kept; 2,829 rejected; 171 scored), shown with four of the drafts it threw away; the ledger; what we found; five
  problems; where it comes back; in practice; references; Part 43.

## What is computed, and what is heard

`python -m videos.music.music42.compute` (under a minute) fills `.cache/music42/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `search` | the searcher's 2,000 drafts, rejections, survivors and kept draft | the counts add up (tests) |
| `ode` | the Ode to Joy's moves | steps + repeats + leaps (tests) |
| `motive`, `quiz` | the eight operations; the quiz | inverses and lengths (tests) |
| `develop`, `kinds` | the sentence; four variations of the Tune | — |
| `tension` | the searcher aimed at two plans | the later plan peaks later (tests) |
| `funnel` | exact counts under growing rules | brute force on small cases (tests) |
| `dice` | the table, two minuets, distinct pieces, entropy | 11^16; the entropy of two dice (tests) |
| `illiac` | generate and test with backtracking | every kept note obeys every rule (tests) |
| `chains` | Markov chains of order 1 and 4; copying | more memory copies more (tests) |
| `evolve` | a genetic algorithm with the critics as fitness | — |
| `tune`, `variation` | Variation 42 | the ledger (tests) |

Monochord's tools are held in `tests/music/test_composer.py`; this part's claims and clips in `tests/music/test_music42.py`.

**Sounds.** Every clip is Part 7's piano (a struck string on a soundboard) with Part 38's plucked bass: physical models.
There are no recordings.

**What the models are, and are not.** *The critics* are the series' rules, not a theory of what makes a good melody;
they refuse and rank, and someone chose their weights. *The tension measure* is crude: height, non-chord tones, the
chord's distance and density, bar by bar. *The dice table* is ours, built in the eighteenth-century format; Mozart's
count is quoted. *The chains* learn from the series' small corpus of folk and public-domain tunes.

## Build

```bash
python -m videos.music.music42.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music42 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music42 --sync                         # the sound gates
python tools/dead_air.py renders/music42_480p.mp4 --sound music42  # no empty screen; no sound over a still one
python tools/lecture_length.py music42                          # 30 to 60 minutes, listening included
python tools/build.py music42                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 42                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A dice game has 16 bars; bars 8 and 16 have one option, the rest 11 distinct ones. How many distinct
   pieces?

   *Solution.* The choices are independent from bar to bar, so the counts multiply: 11^14 × 1 × 1 = 379,749,833,583,241,
   about 3.8 × 10^14. The table printed under Mozart's name is usually quoted at about 7.6 × 10^14 distinct minuets, by
   the same kind of count.

2. **Prove.** Prove that the entropy of two dice's sum is about 3.27 bits, and that a piece's entropy is the sum over its
   bars.

   *Solution.* The sum s has probability (6 − |s − 7|)/36 for s = 2, …, 12; −Σ p log₂ p = 3.274 bits. The bars are chosen
   by independent throws, and the entropy of independent choices adds: H(X₁, …, X₁₆) = Σ H(Xᵢ). When two sums choose the
   same bar, merge their probabilities first; that is why our game has 41.0 bits rather than 14 × 3.27 = 45.8 (the two
   cadence bars carry none).

3. **Ear.** The lab plays melodies from chains of random order; say which order made each.

   *Solution.* The lab prints the orders and how many notes each copied. Order 1 wanders with no phrase; order 2 makes
   short plausible turns; order 4 sounds like a real tune for long stretches, because it often is one.

4. **Build.** Add a critic of your own to the searcher and compare what it keeps.

   *Where to look.* `composer.judge` collects the verdicts; add a measure (for example, the share of notes on the beat
   that repeat the previous note, or a penalty for the same rhythm in every bar), add it to the score or the hard list,
   and rerun `compose` with the same seed: compare the kept drafts and the rejection counts.

5. ★ **Can novelty and value be measured separately, and do they trade off?**

   *Where the frontier is.* Have a searcher, a chain and human composers write to one brief; measure each output's
   copying against what its maker was shown; collect blind listener ratings of value and surprise; model value as a
   function of novelty, maker and listener.

## Sources

* A. Schoenberg, *Fundamentals of Musical Composition* (1967) and "Brahms the Progressive" (1947).
* J. P. Kirnberger, *Der allezeit fertige Polonoisen- und Menuettencomponist* (1757); the *Musikalisches Würfelspiel*
  attributed to Mozart (1792, K. 516f).
* L. Hiller and L. Isaacson, *Experimental Music: Composition with an Electronic Computer* (1959); F. P. Brooks,
  A. L. Hopkins, P. G. Neumann and W. V. Wright, "An experiment in musical composition", *IRE Transactions on Electronic
  Computers* (1957).
* C. L. Krumhansl, "A perceptual analysis of Mozart's Piano Sonata K. 282", *Music Perception* (1996); F. Lerdahl and
  C. L. Krumhansl, "Modeling tonal tension", *Music Perception* (2007); M. M. Farbood, "A parametric, temporal model of
  musical tension", *Music Perception* (2012).
* I. Stravinsky, *Poetics of Music* (1942); M. J. Steedman, "A generative grammar for jazz chord sequences", *Music
  Perception* (1984); J. A. Biles, "GenJam: a genetic algorithm for generating jazz solos" (1994).
* D. Cope, *Experiments in Musical Intelligence* (1996); M. A. Boden, *The Creative Mind* (1990; 2nd ed. 2004);
  G. Ritchie, "Some empirical criteria for attributing creativity to a computer program", *Minds and Machines* (2007);
  A. Jordanous, "A standardised procedure for evaluating creative systems", *Cognitive Computation* (2012); M. T. Pearce
  and G. A. Wiggins, "Evaluating cognitive models of musical composition" (2007).
* C.-Z. A. Huang and others, "The Bach Doodle: approachable music composition with machine learning at scale" (2019);
  B. L. Sturm, J. F. Santos, O. Ben-Tal and I. Korshunova, "Music transcription modelling and composition using deep
  learning" (2016).

## Interpretation limits

Unity checks pre-cadential normalized shapes from the motive or its initial fragments followed by up to two operations, ignoring transposition and the final duration. Variety counts unique normalized figures, so transpositions count as repeats. Parallel-motion checks sample consecutive bar downbeats. Tension scores, creativity labels and fitness are chosen proxies, not listener validation. Higher-order walks have longer matching runs in this small corpus, not a general law or a plagiarism determination. Dice entropy is a lower bound on average binary coding length; compatibility does not guarantee artistic quality.
