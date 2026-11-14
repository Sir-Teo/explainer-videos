# Music, Built: Part 22, Analysis

Part 22 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act III. Parts 16 to 21 built tonal music's grammar from the
bottom; this part asks what an analysis of it is. It takes Schenker's claim, that every tonal masterpiece elaborates
one stepwise descent to the tonic, seriously as a theory: states reduction as rules (Lerdahl and Jackendoff's
grouping, metre and time-span reduction), writes harmony as a probabilistic context-free grammar (after Rohrmeier),
parses with it, trains it on Bach's chorales and scores it against chord n-grams on held-out chorales, runs a grammar
of melodic elaboration forwards to regrow the Tune, surveys other approaches, sets out the argument over the theory and
its author, and asks whether harmony is recursive. The reductions and grammars are Monochord's
(`explainer/music/monochord/grammar.py`); the chord sequences are Part 17's chorales cut at their fermatas; everything
heard is played on Part 7's piano. Published findings are the ones listed under Sources.

* **One line, walking down.** The Tune and its time-span reduction at spans of 2, 4, 8 and 16 beats, heard (C G A G F E
  D C …; C C G G C C; C G C); Schenker's *Der freie Satz* (1935); the plan.
* **1. Reduction and prolongation.** Passing, neighbour, arpeggiation, repetition; an ear question (the first strain and
  two skeletons, C G E C against C A F C: which fits?); prolongation at every scale.
* **2. The *Ursatz*.** The fundamental line and the bass arpeggiation; an ear question (F F E E D D C over a tonic pedal
  and over IV I V I: which closes?); 22 of Part 14's 51 major tunes end on a stepwise descent to the tonic (6 from the
  fifth, 16 from the third), against about 3.4 when their notes are shuffled; what the claim explains and costs.
* **3. Grouping and metre.** *A Generative Theory of Tonal Music* (1983): well-formedness and preference rules; three
  grouping rules put the five strongest boundaries of the Tune exactly on its five phrase ends; the metrical grid;
  computational GTTM (Hamanaka, Hirata and Tojo).
* **4. A time-span reduction.** The head of each span by a sum of preferences (chord tone, stable degree, metrical
  strength); the Tune's levels read as letters; I–V–I at the top; prolongational reduction and Part 19's tension.
* **5. Harmony as a grammar.** Rohrmeier (2011): six rules over tonic, dominant and subdominant regions; trees for
  I IV V I and I vi ii V I; recursion.
* **6. Parsing and ambiguity.** The CYK algorithm; 5 trees for I vi ii V I; for I followed by repeated IV V I, 2, 14,
  132 and 1,430 trees at 4, 7, 10 and 13 chords (Catalan numbers); I IV I V I has no tree without a plagal rule.
* **7. A grammar learned from Bach.** 934 training phrases and 231 held out, 42 chord symbols, inside-outside training;
  bits per chord on held-out phrases: no context 3.93, chord pairs 3.33, triples 3.57, the six-rule grammar 3.90, a
  grammar with 12 invented symbols 3.46; what the six-rule grammar learned (its subdominant symbol drifted to emitting I);
  prediction against explanation.
* **8. Growing a melody.** The elaboration grammar from the Tune's skeleton; an ear question (which melody is the
  grammar's?); the missing copy rule and Chomsky's hierarchy; three derivations.
* **9. Other ways to analyse.** Meyer, Narmour and Huron (expectation); Ratner's topics; Lewin's transformations;
  Nattiez's three levels.
* **10. A theory and its author.** Schenker's life and views; Ewell's 2019 plenary talk and 2020 article; the *Journal of
  Schenkerian Studies* volume of 2020 and its aftermath; the positions, and what testing can add.
* **11. Is harmony recursive?** Depth of the best trees of held-out phrases (about as deep as they are long, where the
  six rules parse them: about a fifth); Hauser, Chomsky and Fitch (2002); Koelsch and colleagues' nested chorales (2013);
  Part 21's limits.
* **12. Frontier: grammars from data.** Induced grammars and their drifting categories; jazz parsing and Rohrmeier's
  syntax of jazz harmony (2020). ★ research problem: measuring a listener's reduction directly.
* **Variation 22, recap and problems.** The Tune's skeleton, a note every four beats, regrown along a different
  derivation (12 notes grown into 37; on 15 of 24 strong beats a chord tone); the ledger; what we found; five problems;
  where it comes back; in practice; references; Part 23.

## What is computed, and what is heard

`python -m videos.music.music22.compute` (about ten minutes: the grammars train) fills `.cache/music22/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | the Tune's time-span reduction, every level, and four of them heard | — |
| `skeleton` | the first strain and two candidate skeletons | — |
| `cadence` | the second phrase over a tonic pedal and over IV I V I | — |
| `urlinie` | stepwise descents to the tonic at the ends of the major tunes | shuffled tunes |
| `grouping` | grouping preference strengths on the Tune | its phrase ends |
| `parses` | Viterbi trees and parse counts under the six-rule grammar | Catalan numbers |
| `learned` | grammars trained by inside-outside; n-grams; bits per chord on held-out phrases; tree depths | brute-force parse counts (tests) |
| `growth` | three derivations from the skeleton; a quiz | — |
| `tune` | Variation 22 | — |

Monochord's grammars are held in `tests/music/test_grammar.py`; this part's claims and clips in
`tests/music/test_music22.py`.

**Sounds.** Part 7's piano (`physical model`) in twelve-tone equal temperament. There are no recordings.

**What the models are, and are not.** *The time-span reduction* chooses heads by a fixed sum of three preferences,
not Lerdahl and Jackendoff's full rule set, and the Tune's harmony is the one of Part 21. *The six-rule grammar* is the
core of Rohrmeier's (2011), without his rules for applied dominants, modulation or plagal motion; chord symbols are
Part 17's beat labels as Roman numerals with repeated chords merged and rare symbols (fewer than five uses) pooled.
*Bits per chord* count the end of each phrase as a symbol for every model, so a grammar (which assigns probability to
whole phrases) and an n-gram are compared on the same footing. *The latent grammar* is trained from one random start;
others find different grammars. *The elaboration grammar* chooses rules independently at each note and has no rule for
motivic repetition, which is the point of chapter 8. *The account of the 2019–2020 controversy* is a summary of public
events and published positions; readers should consult the sources.

## Build

```bash
python -m videos.music.music22.compute                          # numbers and sounds (about ten minutes)
EXPLAINER_TTS=silent python tools/build.py music22 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music22 --sync                         # the sound gates
python tools/dead_air.py renders/music22_480p.mp4 --sound music22  # no empty screen; no sound over a still one
python tools/lecture_length.py music22                          # 30 to 60 minutes, listening included
python tools/build.py music22                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 22                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Reduce *Ode to Joy*'s first eight bars (Part 14's version) to a note every four beats, by hand, using
   this part's score.

   *Solution.* Without harmony (the score's chord term left out), each four-beat span keeps its most stable note on the
   strongest beat: E G | C E | E G | C C (the program in `grammar.reduce_levels` gives the same). The first half ends on
   E, the third, open; the second closes on C. With the chords put back (I, then V under the D's), the spans that hold D
   over V keep D instead, and the end of the second half shows the 3–2–1 descent: E D C.

2. **Prove.** Prove that the number of binary trees over n leaves is the Catalan number C_{n−1}, and say why the parse
   counts of chapter 6 are Catalan numbers.

   *Solution.* Let T(n) count binary trees with n leaves; the root splits the leaves into k and n − k, so
   T(n) = Σ_{k=1}^{n−1} T(k) T(n − k), T(1) = 1, the Catalan recurrence with T(n) = C_{n−1}. In chapter 6 every IV V pair
   must form a dominant region (SR DR → DR), so I (IV V) I (IV V) I … has 2m + 1 units, and the rules TR → DR TR,
   TR → TR TR, TR → TR DR let them be bracketed in every binary way: C_{2m} trees, which are 2, 14, 132, 1,430 for
   m = 1 … 4.

3. **Ear.** The lab plays eight short passages and two skeletons for each. Choose the skeleton that fits.

   *Solution.* The lab prints the answers. The fitting skeleton's notes belong to the chords under them on strong beats;
   the wrong one moves a note to a neighbour that clashes.

4. **Build.** Add the rule TR → SR TR to the grammar, retrain it, and report its bits per chord and coverage.

   *Where to look.* Append ("TR", "SR", "TR") to `grammar.RULES`, train `PCFG` on the same phrases, and score with
   `pcfg_bits` and `coverage`. The plagal rule lets I IV I parse and should improve the share of phrases the strict
   grammar parses; whether it lowers the bits per chord depends on how often Bach's IV returns straight to I.

5. ★ **A listener's reduction.** Design an experiment that measures a listener's reduction of a melody directly.

   *Where the frontier is.* Chapter 1's question is one design: present a passage and two skeletons and ask which fits,
   varying which notes the skeletons keep; another asks listeners to tap the 'important' notes, or to judge similarity
   between passages that share skeletons but not surfaces. A good design separates memory for the surface from
   recognition of the structure, as Dowling's experiments with contour did.

## Sources

* H. Schenker, *Der freie Satz* (1935); A. Cadwallader and D. Gagné, *Analysis of Tonal Music: A Schenkerian Approach*
  (3rd ed., 2011).
* F. Lerdahl and R. Jackendoff, *A Generative Theory of Tonal Music* (1983); F. Lerdahl, *Tonal Pitch Space* (2001);
  M. Hamanaka, K. Hirata and S. Tojo, "Implementing 'A Generative Theory of Tonal Music'", *Journal of New Music
  Research* 35 (2006).
* M. Rohrmeier, "Towards a generative syntax of tonal harmony", *Journal of Mathematics and Music* 5 (2011); "The syntax
  of jazz harmony", *Music Theory and Analysis* 7 (2020).
* S. Koelsch, M. Rohrmeier, R. Torrecuso and S. Jentschke, "Processing of hierarchical syntactic structure in music",
  *PNAS* 110 (2013); M. D. Hauser, N. Chomsky and W. T. Fitch, "The faculty of language", *Science* 298 (2002).
* L. B. Meyer, *Emotion and Meaning in Music* (1956); E. Narmour, *The Analysis and Cognition of Basic Melodic
  Structures* (1990); D. Huron, *Sweet Anticipation* (2006); L. G. Ratner, *Classic Music* (1980); D. Lewin, *Generalized
  Musical Intervals and Transformations* (1987); J.-J. Nattiez, *Music and Discourse* (1990).
* P. Ewell, "Music theory and the white racial frame", *Music Theory Online* 26 (2020); the *Journal of Schenkerian
  Studies* 12 (2020) and the statements of the Society for Music Theory's executive board.
* Part 14 for the tunes; Part 17 for the chorales; Part 18 for the n-gram models; Part 19 for Lerdahl's tension; Part 21
  for Cook's experiment.
