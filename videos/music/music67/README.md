# Music, Built: Part 67, Doing Research in Music

Part 67 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act XII, *Coda*. In 1993 a study of thirty-six students reported that ten
minutes of Mozart raised a spatial score, and within five years a governor proposed a classical CD for every newborn in his
state; the effect did not replicate as claimed. This part asks how each kind of music research knows what it claims, and
gives each something to compute: a manuscript tradition recovered from its errors, a canon set against a wider corpus, a
literature bent by selective publication, the power of listening tests, leakage and annotation uncertainty, and an audit of
this series' own verdicts. The tools are Monochord's (`explainer/music/monochord/research.py`) and *Statistics, Built*'s kit.

* **Ten minutes of Mozart.** An ear question (an ABX trial: X was B, the coder at 48 kbit/s; one trial proves nothing);
  Rauscher, Shaw and Ky (1993), Georgia's CDs, Chabris (1999), Pietschnig et al. (2010); the plan.
* **1. Kinds of knowing.** Sources, analysis, fieldwork, experiment, computation and practice, where each appears in the
  series; one question (where does the Tune come from?) asked six ways; each kind's failure and check.
* **2. Sources and editions.** Copies of copies and Lachmann's method; the Tune copied for four generations (33 manuscripts,
  19 surviving, each with 2 to 9 notes wrong); three copies heard; neighbour joining on shared errors recovers 7 of the 8
  true groupings; an ear question (which is the corrupt copy? the second); the original rebuilt by majority (2 wrong) and
  by one vote a branch (1 wrong); other evidence in the sources.
* **3. Analysis and the corpus.** Arguments and counts; a chorale tune and a folk tune heard; "melodies move mostly by step":
  83 % of moves in Bach's chorale tunes (82 to 84) against 67 % in Part 14's tunes (63 to 71); corpus studies done well.
* **4. Fieldwork and ethics.** Learning by taking part (Nettl); consent, archives and repatriation, credit and pay;
  transcription as interpretation (Bartók, Seeger); what notation discards, measured on a sung phrase (29 % of its
  moments within 10 cents of a written note).
* **5. Experiments and their literatures.** How a literature misleads; a simulated one (true effect 0.1; 120 studies; 33
  published): the funnel with a bite out of it, the first significant study at 0.86, the published pooled at 0.27, all
  studies at 0.12, a large replication at 0.08, Egger p = 0.07 and PET 0.06; analysts' choices (Simmons, Nelson and
  Simonsohn: 4 % false positives with one test, 61 % with all the choices); remedies.
* **6. Listening tests and their power.** The hook's test counted (20 trials need 15 right; a 60 % listener passes 13 % of
  the time); power by trials (90 %: 8 trials; 75 %: 23; 60 %: 158; 55 %: 620); a harder ABX trial heard (X was A; the
  coder at 128 kbit/s); listeners for MUSHRA (a 5-point difference: 73); listening panels.
* **7. Datasets, leakage and agreement.** Part 65's chain split by chorale (3.22 bits) against by hymn tune (3.80); this
  series' leaks; its own duplicates (13 of 59 Variations recur in another clip); annotator agreement; two simulated tappers
  (0.94 and 0.72 against the performance, 0.88 against each other), heard.
* **8. The series audits itself.** Five verdicts re-run: Part 61's YIN at 0 dB (6 to 13 %; holds), Part 63's fingerprinter
  at 0 dB (58 to 71 %; holds; one missed query heard), Part 64's median filter (7.8 dB; holds), Part 65's best order (2 in
  7 of 10 splits, 1 in 3: weaker than said), Part 66's detector (no false alarms in 60); the order's spread; errata.
* **9. Standards and reporting.** Pitch, loudness, listening-test and MIR standards; the Tune at A = 440, 415 and 466,
  heard; units; what to report; a Part 65 number reproduced to the last digit.
* **10. Reading papers, and practice as research.** How to read a paper; what to check first, by subfield; the 1993 paper
  read that way; practice as research.
* **11. Frontier: the open problems of this series.** 44 open questions from the parts' notes, by act; six drawn at random;
  the problems grouped; how this series could be wrong; finding a problem; ★ research problem: an open benchmark of the
  verdicts of music research, re-run each year.
* **Variation 67, recap and problems.** The Tune's critical edition: as written, as its most corrupt copy has it (9 notes
  wrong), and rebuilt from the 19 copies (2 wrong); the ledger; what we found; five problems; where it comes back; in
  practice; references; Part 68.

## What is computed, and what is heard

`python -m videos.music.music67.compute` (some minutes: earlier parts' verdicts are re-run) fills `.cache/music67/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `abx2`, `power`, `mushra` | ABX trials; exact binomial power; listeners for MUSHRA | the binomial and noncentral t (tests) |
| `stemma`, `copies`, `tune67` | a simulated manuscript tradition; neighbour joining; reconstruction | the true tree and the Tune (tests) |
| `canon`, `canonheard` | step, leap and repeat shares, resampled by tune | — |
| `notation`, `pitchstd` | a sung phrase against equal temperament; three pitch standards | — |
| `meta`, `phack` | a simulated literature; Egger and PET; the p-hacking simulation | the true effect (tests) |
| `leakage`, `dupes`, `tappers`, `tapsheard` | a leaky split; duplicates in the library; annotator agreement | the honest split (tests) |
| `audit`, `audit63`, `auditheard`, `repro` | five verdicts re-run; one number reproduced | the parts' stored numbers (tests) |
| `stars` | every part's research problem | the parts' READMEs |

Monochord's tools are held in `tests/music/test_research.py`; this part's claims and clips in `tests/music/test_music67.py`.

**Sounds.** Part 38's piano, organ tones, Part 8's voice, Part 58's coder, Part 63's simulated bar.

**What the models are, and are not.** *The manuscript tradition* has only substitutions, no omissions, no contamination
between branches and no scribe who corrects; real traditions have all of them. *The literature* is simulated, with the
Mozart effect's history as its motivation, not its data: its numbers are not the real studies'. *The tappers* are
simulated people. *The audit* re-runs five verdicts of the series, chosen because they were cheap to re-run, not at random.

## Build

```bash
python -m videos.music.music67.compute                          # numbers and sounds
EXPLAINER_TTS=silent python tools/build.py music67 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music67 --sync                         # the sound gates
python tools/dead_air.py renders/music67_480p.mp4 --sound music67  # no empty screen; no sound over a still one
python tools/lecture_length.py music67                          # 30 to 60 minutes, listening included
python tools/build.py music67                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 67                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A listener hears a difference 70 % of the time. How many ABX trials give 80 % power at the 5 % level?

   *Solution.* With n trials the test passes at the smallest c with P(Bin(n, ½) ≥ c) ≤ 0.05; the power is P(Bin(n, 0.7) ≥ c).
   Searching n upward, the first with power at least 0.8 is n = 37 (`research.abx_trials_needed(0.7)`): roughly double the
   twenty that many published tests use.

2. **Prove.** Show that if study i is published only when θ̂ᵢ / sᵢ > 1.96, small published studies overestimate θ most.

   *Solution.* With θ̂ ~ N(θ, s²), a published estimate is drawn from the normal truncated below at 1.96 s, whose mean is
   θ + s λ((1.96 s − θ)/s), with λ the inverse Mills ratio φ/(1 − Φ). For fixed θ ≥ 0 the term s λ(1.96 − θ/s) grows
   with s, since λ is increasing and its argument grows towards 1.96 as s does. So the bias of the published estimate grows
   with the standard error: the smallest studies overestimate most, which is the funnel's missing corner.

3. **Ear.** The lab plays the Tune, its worst copy and the rebuilt original; find the wrong notes by ear, then check.

   *Solution.* The lab prints the positions where the worst copy differs. Two in three wrong notes are a step or a tone off, which a listener who
   knows the Tune can usually hear; those in repeated-note passages are easier to miss. The same counting answers an ABX run:
   with h hits in 40 trials the one-sided p-value is P(Bin(40, ½) ≥ h), about 0.04 for 26 hits and 0.08 for 25.

4. **Build.** Add contamination to the manuscript tradition (a scribe copying from two exemplars) and test the tree.

   *Where to look.* In `copy_tradition`, let a copy take each note from one of two exemplars, chosen at random per passage;
   neighbour joining then sees a witness between two branches, and the recovered splits fall. Measure the Robinson-Foulds
   share against the share of contaminated copies, and compare majority and per-branch reconstruction.

5. ★ **Build an open benchmark of the verdicts of music research, re-run each year.**

   *Where the frontier is.* Collect claims with their data and code (from this series, from shared tasks, from replication
   projects), re-run them on schedule with new seeds, splits and data, and publish which hold, which weaken and which fail,
   as this part did for five of its own.

## Sources

* E. Clarke and N. Cook (eds.), *Empirical Musicology* (2004); B. Nettl, *The Study of Ethnomusicology* (3rd ed., 2015);
  J. Grier, *The Critical Editing of Music* (1996); C. Seeger, "Prescriptive and descriptive music-writing", *Musical
  Quarterly* (1958).
* F. H. Rauscher, G. L. Shaw and K. N. Ky, "Music and spatial task performance", *Nature* (1993); C. F. Chabris, "Prelude or
  requiem for the 'Mozart effect'?", *Nature* (1999); J. Pietschnig, M. Voracek and A. K. Formann, "Mozart effect–Shmozart
  effect: a meta-analysis", *Intelligence* (2010).
* M. Egger et al., "Bias in meta-analysis detected by a simple, graphical test", *BMJ* (1997); J. P. Simmons, L. D. Nelson
  and U. Simonsohn, "False-positive psychology", *Psychological Science* (2011).
* N. Saitou and M. Nei, "The neighbor-joining method", *Molecular Biology and Evolution* (1987); D. F. Robinson and L. R.
  Foulds, "Comparison of phylogenetic trees", *Mathematical Biosciences* (1981).
* B. L. Sturm, "The GTZAN dataset" (2013) and "A simple method to determine if a music information retrieval system is a
  horse" (2014); ITU-R BS.1116 and BS.1534 (MUSHRA); ISO 16 (1975).

Review qualifications: annotator pairwise agreement is not a universal model-performance ceiling. Power calculations assume the stated independent-trial or paired-rating model; finite synthetic audits are scoped checks. The series discusses fieldwork but its computations are not substitutes for community-based ethnographic research.
