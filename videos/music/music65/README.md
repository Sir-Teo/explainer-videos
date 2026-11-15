# Music, Built: Part 65, Machines that Compose

Part 65 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth part of Act XI, *Listening Machines*. In 1997 an audience in Oregon heard three
pieces, one by Bach, one by a professor in Bach's style and one by David Cope's program EMI, and, as it was reported, took
the program's for Bach's. This part builds composing machines that learn from music, from a Markov chain to a small
transformer, on the melodies of Bach's chorales, and measures the trade none of them escapes: a model that copies less
also coheres less. The tools are Monochord's (`explainer/music/monochord/machines.py`, on Part 17's chorale table and
harmonizer and *AI, Built*'s pocket transformer); every generated tune is checked against the training tunes for copying.

* **Bach, a professor and a program.** An ear question (three pairs of harmonized chorale phrases: which is Bach's? the
  second, BWV 166.6, never seen by the machines; the others a Markov chain's and a transformer's, each the first draw that
  stayed in the key and could be harmonized); Hofstadter's concert in Eugene; the plan.
* **1. Dice, rules and chance.** Composing machines from the dice minuet (1792) to the Music Transformer (2018); rules,
  chance and statistics; the corpus (364 chorales; 163 in major keys and 4/4, transposed to C; only 114 different hymn
  tunes, so split by tune: 132 chorales to learn from, 23 tunes kept back), a chorale heard.
* **2. Counting what comes next.** Variable-order Markov chains; bits per note on the tunes kept back by order (5.22 at
  order 0, 3.40 at order 2, the best, 3.83 at order 8); where a tune surprises (at the phrase boundaries); orders 1, 2 and
  8 heard.
* **3. Novelty and copying.** Longest copied run and share inside copied runs of eight, by order (order 1: 4.9 notes and
  none; order 8: 26 notes and 91 %), against Bach's own tunes kept back (8.2 and 11 %); an order-8 tune's 40-note copy of
  BWV 226.2, heard beside it; the trade, prediction against copying.
* **4. Constraints.** A chain cannot plan an ending (0.66 % of free 32-note draws end legally); backward messages and
  forward sampling (Pachet and Roy, 2011); free and constrained draws heard.
* **5. Recombination.** Cope's recombinancy; four phrases from four chorales joined by steps and harmonized, heard (79 %
  inside copied runs; only the joins are new); is it composing?
* **6. Music as tokens.** A chorale's opening three ways (146 note tokens; 34 pitch-and-length symbols; a 27-symbol grid);
  what the choice trades.
* **7. A transformer.** *AI, Built*'s pocket transformer (344,160 weights) on 13,487 tokens, and on the same tunes in
  twelve keys (161,844); training curves on tunes set aside (the tunes-alone model turns round near step 100, the twelve-key
  one near 300); bits on the test tunes (3.76 and 3.49, against the order-2 chain's 3.40); a network trained too long
  recites 40 notes of BWV 322, heard; the first three tunes it draws from nothing, heard.
* **8. Temperature.** Reshaping the odds; an ear question (one opening continued at 0.5, 1.0 and 1.5: in order); over 46
  continuations each, intervals closest to Bach's at 1.0, notes outside the key from 6 to 19 % (Bach 2 %), cadences on
  the tonic chord most often when cool, copying near none; top-k, nucleus and beam search.
* **9. Four parts.** DeepBach and Gibbs sampling; Monochord's pipeline (the transformer's tune, Part 17's harmony); a
  machine's chorale heard (no parallel fifths or octaves); Bach's harmony beside Part 17's on a tune kept back, heard.
* **10. Judging machines.** An ear question (which is copied? the second, an order-8 chain's, every note inside a copied
  run); every machine before the same judges (only copying separates them); pitfalls; listening tests.
* **11. Frontier: form, control and attribution.** Relative attention and long-range form; control and infilling;
  attribution and training data; ★ research problem: is there a frontier of novelty against quality, and can a model be
  moved past it?
* **Variation 65, recap and problems.** The Tune's first phrase continued by the transformer at five temperatures, one draw
  each, uncurated (longest copied run 4 notes); the ledger; what we found; five problems; where it comes back; in practice;
  references; Part 66.

## What is computed, and what is heard

`python -m videos.music.music65.compute` (some minutes: four transformer runs, two long and two stopped where the tunes set
aside say) fills `.cache/music65/`.

| Item | What it computes | Checked against |
|---|---|---|
| `corpus` | the tunes, the split by hymn tune, three representations | the chorale table (tests) |
| `markov`, `surprise`, `copy` | bits per note by order; surprise note by note; copying by order and Bach's own | the training tunes (tests) |
| `constrained`, `recombine` | an order-2 chain sampled exactly under constraints; recombined phrases | the constraints; the sources (tests) |
| `transformer`, `samples` | two transformers, curves, bits, copying; an overtrained one reciting | the test tunes; the training tunes (tests) |
| `temperature`, `judge`, `copyquiz` | continuations at three temperatures; every machine judged alike | held-out Bach (tests) |
| `harmony`, `bachvs17`, `hook` | tunes harmonized by Part 17; Bach beside Part 17 | the voice-leading rules (tests) |
| `tune65` | Variation 65 | the training tunes (tests) |

Monochord's tools are held in `tests/music/test_machines.py`; this part's claims and clips in `tests/music/test_music65.py`.

**Sounds.** Every tune is played on Part 17's organ tones, with Part 17's fermata pauses; harmonized tunes use Part 17's
chord model and voice-leading search. Bach's chorales are in the public domain; the table keeps only pitches, times and
fermatas (see `explainer/music/monochord/chorales.py`).

**What the models are, and are not.** *The corpus* is small: 6,937 notes of melody, so every model here is data-starved,
and the transformer's comparison with counting says more about small data than about transformers. *The best order* is a property of the split as well as of the music: Part 67 re-ran it over ten splits by tune, and order 2 was best in 7, order 1 in 3, with order 2's bits per note ranging from 3.40 to 4.16. *The Markov chains*
blend orders by PPM's escape method, over whole notes. *The transformer* is three layers and 96 dimensions, trained without
dropout; it is stopped where loss on nine tunes set aside from the training tunes was lowest. *Copying* is measured by
exact runs; near copies (a note changed, a rhythm altered) are not counted, so these numbers are lower bounds. *Draws
shown harmonized* are the first that stayed in the key and could be harmonized, as the film says.

## Build

```bash
python -m videos.music.music65.compute                          # numbers and sounds (the transformers train)
EXPLAINER_TTS=silent python tools/build.py music65 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music65 --sync                         # the sound gates
python tools/dead_air.py renders/music65_480p.mp4 --sound music65  # no empty screen; no sound over a still one
python tools/lecture_length.py music65                          # 30 to 60 minutes, listening included
python tools/build.py music65                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 65                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A corpus has 7,000 notes and 146 distinct notes. Roughly how many order-3 contexts are possible, and how
   many can it have seen?

   *Solution.* 146³ ≈ 3.1 million contexts of three notes are possible; the corpus has at most about 7,000 positions, so it
   can have seen at most 7,000 contexts (fewer distinct ones), well under one in four hundred. Most order-3 contexts in a
   new tune have therefore been seen rarely or never, which is why order 3 already predicts worse than order 2.

2. **Prove.** Show that sampling forward with weights P(x | s) β_{k−1}(s′) draws exactly from the chain conditioned on the
   constraints.

   *Solution.* By induction, β_k(s) is the probability, under the chain, that the next k notes from s satisfy the
   constraints. The conditional probability of the next note x given s and given that the constraints will hold is
   P(x | s) β_{k−1}(s′) / β_k(s), by Bayes' rule; drawing x with weights P(x | s) β_{k−1}(s′) draws from exactly this.
   Multiplying the conditionals along the sequence gives P(sequence) / P(constraints hold) for every legal sequence and 0
   for every other: the chain conditioned on the constraints.

3. **Ear.** The lab plays tunes from orders 1 to 6 in random order; rank them by how Bach-like they sound, then check how
   much each copied.

   *Solution.* The lab prints the orders and, for each order, the share inside copied runs. If the tunes you ranked most
   Bach-like came from the high orders, the copying column shows why: they are Bach's.

4. **Build.** Add a maximum-order constraint: forbid any run of more than 6 notes copied from one tune, and measure the cost
   in bits.

   *Where to look.* Papadopoulos, Roy and Pachet (2014) build an automaton of the forbidden runs and sample the chain
   intersected with it; a simpler version rejects, at each step, any note that would complete a copied run of seven (a
   suffix check against `train_grams`), and backs off when nothing is left. Measure bits per note of the constrained
   sampler's own distribution on the test tunes, and the copying, against the unconstrained chain.

5. ★ **Is there a frontier of novelty against quality, and can a model be moved past it?**

   *Where the frontier is.* Train generators of many sizes on a corpus whose every piece is known; measure likelihood on
   unseen music and copying by exact and near matches; collect blind preferences; ask whether any training method (more
   data, augmentation, constraints, retrieval) moves a model past the curve the others share.

## Sources

* J.-P. Briot, G. Hadjeres and F.-D. Pachet, *Deep Learning Techniques for Music Generation* (2020); G. Nierhaus,
  *Algorithmic Composition* (2009).
* L. A. Hiller and L. M. Isaacson, *Experimental Music* (1959); I. Xenakis, *Formalized Music* (1971); D. Cope,
  *Experiments in Musical Intelligence* (1996) and *Virtual Music* (2001), with D. Hofstadter, "Staring Emmy straight in the
  eye".
* M. T. Pearce, *The Construction and Evaluation of Statistical Models of Melodic Structure* (thesis, 2005); F. Pachet and
  P. Roy, "Markov constraints: steerable generation of Markov sequences", *Constraints* (2011); A. Papadopoulos, P. Roy and
  F. Pachet, "Avoiding plagiarism in Markov sequence generation" (AAAI, 2014).
* G. Hadjeres, F. Pachet and F. Nielsen, "DeepBach: a steerable model for Bach chorales generation" (ICML, 2017);
  C.-Z. A. Huang et al., "Music Transformer" (ICLR, 2019); Y.-S. Huang and Y.-H. Yang, "Pop Music Transformer" (REMI,
  ACM Multimedia, 2020); A. Holtzman et al., "The curious case of neural text degeneration" (ICLR, 2020).
* L.-C. Yang and A. Lerch, "On the evaluation of generative models in music", *Neural Computing and Applications* (2020).
