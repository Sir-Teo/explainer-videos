# Music, Built: Part 18, Progressions

Part 18 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act III. Part 17 counted which chord follows which and used
the table without asking why; this part asks. It measures the syntax of harmony on Bach's chorales (the order of
harmonic functions, root motion, how predictable the next chord is, sequences, harmonic rhythm), then goes to
eighteenth-century Naples for the rule of the octave and the galant schemata, builds a detector for schemata,
and ends with four centuries of ground basses. The syntax is Monochord's
(`explainer/music/monochord/progression.py`), measured on Part 17's chorales
(`explainer/music/monochord/chorales.py`); the galant examples are realized in `compute.py` and played on a
plucked string over Part 7's soundboard. Published findings are the ones listed under Sources.

* **Orphans, and a bass.** Naples's four conservatories, orphanages that trained musicians; partimenti; a bass
  climbing and falling a scale, alone and with the rule of the octave above it, heard; the plan.
* **1. Three jobs, in order.** Riemann's tonic, subdominant and dominant (1893); in Bach's major chorales
  T→S 1,246, S→D 788, D→T 1,412 (3,446 round the cycle), T→D 913, against the cycle 1,038 (D→S only 290); an
  ear question (I–IV–V–I against I–V–IV–I).
* **2. How roots move.** Root motion in the major chorales: falling fifths 39 in a hundred, then rising steps and
  falling thirds; Meeùs's forward and backward progressions (2000): forward 69 in a hundred; an ear question
  (vi–ii–V–I against I–V–ii–vi); why the falling fifth: the overtones, the voices, Rameau's fundamental bass (1722).
* **3. How predictable is harmony?** The guessing game (after IV: I 33 in a hundred, V 14, ii 9; after V: I 52);
  bits per chord on 84 chorales whose tunes the model never saw: 6.1 if all chords were equally likely, 4.0 from
  their frequencies, 3.4 from the chord before, 4.9 for the same chords shuffled; in minor 3.8 (5.5); two chords
  back, too little data to help.
* **4. The same step, again.** The descending-fifths sequence in C major, heard (F to B the one diminished fifth);
  runs of falling fifths in the chorales: 770 of three chords, 205 of four, 68 of five, 21 of six or seven.
* **5. When chords change.** A new chord on beat 1 of a bar of four 78 times in a hundred, beat 3 79, beats 2 and
  4 65 and 60: harmonic rhythm follows the metre of Part 11.
* **6. Naples and the partimento.** Campion's rule of the octave (1716); Durante, Leo, Fenaroli; Pergolesi,
  Paisiello, Cimarosa; Gjerdingen (2007) and Sanguinetti (2012); the rule up and down, heard: plain triads only on
  the first and fifth degrees, and different chords rising and falling.
* **7. Bach and the rule.** Where Bach's bass passes by step through a degree (804 beats in major chorales), his
  chord's notes lie within the rule's chord 49 times in a hundred, its exact figure 28; rising through the leading
  note 74, falling through the third 71, through the second degree rarely.
* **8. Galant schemata.** Gjerdingen's stock phrases; Riepel's Monte, Fonte and Ponte (1755); eight realized in
  four voices and heard: Do-Re-Mi, Romanesca, Meyer, Prinner, Fonte, Monte, Ponte, Quiescenza.
* **9. A phrase from parts.** Do-Re-Mi, Prinner ‖ Fonte, Monte, Ponte, cadence, chained by the shortest way, heard.
* **10. Where the schemata are.** A strict detector on the chorales' beats finds 13 in 185 major chorales (2 in
  shuffled ones): Bach's chorales are not galant music; the schemata's melodies in the series' 51 major tunes:
  6-5-4-3 in 11 (0.4 shuffled), 4-3-2-1 in 23 (1.6), 5-4-3-2-1 in 15 (0.3); the Tune's A A G F F E E is a
  Prinner's melody.
* **11. Ground basses.** An ear question (four grounds, which is major?); the lament (Monteverdi 1638, Purcell
  1689), la Folia (Corelli 1700), the passamezzo antico, the Romanesca and Pachelbel's canon, the chromatic lament
  in rock.
* **12. Frontier: harmony at scale.** Rock (de Clercq and Temperley 2011), the Billboard corpus, the Annotated
  Beethoven Corpus (2018); a grammar of harmony (Rohrmeier 2011) and schemata as a construction grammar
  (Gjerdingen and Bourne 2015). ★ research problem: chains, trees, or stock phrases, for listeners.
* **Variation 18, recap and problems.** The Tune's two phrases over the Romanesca with a cadence, over the
  chromatic lament (in minor), and over a tonic and then a dominant pedal; the ledger; what we found; five problems;
  where it comes back; in practice; references; Part 19.

## What is computed, and what is heard

`python -m videos.music.music18.compute` (about a minute) fills `.cache/music18/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | the rule of the octave up and down over a scale | `fourpart.parallels` (none) |
| `functions` | T, S, D transitions in the chorales; two orders of I, IV, V | — |
| `motion` | root motion by interval class; falling and rising fifths, heard | — |
| `predict` | cross-entropy of n-gram chord models on chorales held out by tune; the guessing game | the same chords shuffled |
| `sequence` | the descending-fifths sequence; runs of falling fifths | — |
| `rhythm` | chord changes by beat of the bar | — |
| `octave` | the rule realized; Bach's chords on stepwise basses against it | Campion's figures |
| `schemata` | eight schemata realized; a phrase of them | no parallels |
| `census` | schemata in the chorales and the schemata's melodies in the tunes | shuffled controls |
| `grounds` | four ground basses realized | — |
| `tune` | Variation 18 | every chord holds the Tune's note; no parallels |

Monochord's syntax of harmony is held in `tests/music/test_progression.py`; this part's claims and clips in
`tests/music/test_music18.py`.

**Sounds.** A string plucked near its end, as a harpsichord's quill plucks it (Part 1's monochord, retuned for each
note), through Part 7's soundboard (`physical model`), in twelve-tone equal temperament. There are no recordings.

**What the models are, and are not.** *Functions* are read off the root alone (iii counted as tonic, vii° as
dominant); Riemann's own theory is subtler. *Root motion and n-gram models* use Part 17's beat labels, with
repeated chords merged and unlabelled beats dropped; with 280 training chorales a model of chord triples is
starved of data, which is why it does worse than pairs. *The rule of the octave* is Campion's in its common form;
Neapolitan versions differ in details, and comparing Bach with it is anachronistic in spirit: it measures how much
of his practice the rule captures, not what he was taught. *The schemata* are realized in their simplest textbook
forms; real galant music ornaments them, and the detector, which demands every note in place on the beats, finds
only plain instances. The chorales are the wrong corpus for galant schemata, and the film says so; no galant
corpus was available offline. *Ground basses* are reduced to one chord per half bar. *The frontier's corpus
findings* are summarized from the publications, not recomputed.

## Build

```bash
python -m videos.music.music18.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music18 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music18 --sync                         # the sound gates
python tools/dead_air.py renders/music18_480p.mp4 --sound music18  # no empty screen; no sound over a still one
python tools/lecture_length.py music18                          # 30 to 60 minutes, listening included
python tools/build.py music18                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 18                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Write the descending-fifths sequence in G major, roots and bass. Where is the one diminished fifth,
   and why must it be there?

   *Solution.* G, C, F♯, B, E, A, D, G: I, IV, vii°, iii, vi, ii, V, I. The step from C down to F♯ is a diminished
   fifth (six semitones); every other step is a perfect fifth (seven). It must be there because the cycle stays in
   the key: seven perfect fifths down from G would reach C, F, B♭, … and leave G major after the second chord.
   Seven steps of a fifth span 7 × 7 = 49 semitones in all, four octaves and a semitone, so to come back to G after
   seven steps (48 semitones) exactly one step must be a semitone short.

2. **Prove.** Show that a cycle of seven falling fifths through a major key visits every degree once, and that it
   cannot be done with perfect fifths only.

   *Solution.* Falling by a fifth within the scale means moving four degrees down (or three up), so after k steps
   the root is degree 1 + 3k (mod 7). Since 3 and 7 share no factor, k = 0, …, 6 give seven different degrees, and
   k = 7 returns to the start. With perfect fifths only, k steps move 7k semitones, which is a multiple of 12 only
   when k is a multiple of 12; after seven steps the root is 49 mod 12 = 1 semitone away from where it began, a
   note outside the key. So one step must be diminished, as in problem 1.

3. **Ear.** The lab plays eight two-chord progressions. For each, say whether the root falls a fifth, rises a fifth,
   or moves by step.

   *Solution.* The lab prints the answers. A falling fifth sounds like a small arrival (V–I, ii–V); a rising fifth
   like a step away (I–V); a move by step changes every note of the chord (IV–V) and has no common tone.

4. **Build.** Extend the schema detector to allow the melody notes to be ornamented (other notes between them). How
   many more schemata does it find in the chorales, and how many in shuffled ones?

   *Where to look.* Replace the consecutive match in `progression.find_schemata` by a subsequence match within a
   window (for example, the schema's events in order within twice as many beats), and keep the bass events
   consecutive. The count rises, but so does the shuffled count, and the ratio between them is what matters. Allowing
   gaps quickly lets chance produce "schemata", which is why published detectors constrain metre and voice leading as
   well.

5. ★ **Chains, trees or phrases?** Design an experiment to tell whether listeners hear harmony as a chain of pairs, as
   a tree, or as stock phrases.

   *Where the frontier is.* The three accounts predict different things when a progression is interrupted or
   rearranged. A chain predicts that what matters is only the last chord; a tree predicts that a chord far back (an
   opening tonic, say) still shapes expectations at the end, so swapping two distant chords changes judgements; a
   phrase account predicts that intact schemata are recognized as units, so cutting one in half is worse than cutting
   between two. Experiments with reordered and interrupted progressions, probe chords and reaction times (Bigand and
   Parncutt 1999; Woolhouse, Cross and Horton 2016; Rohrmeier and Cross 2014) give partial and mixed answers; the
   question is open, and may have different answers for listeners raised on different music.

## Sources

Books: R. O. Gjerdingen, *Music in the Galant Style* (2007) and *Child Composers in the Old Conservatories* (2020);
G. Sanguinetti, *The Art of Partimento* (2012); F. Campion, *Traité d'accompagnement et de composition selon la
règle des octaves de musique* (1716); J.-P. Rameau, *Traité de l'harmonie* (1722); J. Riepel, *Grundregeln zur
Tonordnung insgemein* (1755); H. Riemann, *Vereinfachte Harmonielehre* (1893); S. G. Laitz, *The Complete Musician*
(4th ed., 2015).

Papers: N. Meeùs, "Toward a post-Schoenbergian grammar of tonal and pre-tonal harmonic progressions", *Music Theory
Online* 6 (2000); M. Rohrmeier, "Towards a generative syntax of tonal harmony", *Journal of Mathematics and Music* 5
(2011); T. de Clercq and D. Temperley, "A corpus analysis of rock harmony", *Popular Music* 30 (2011); J. A.
Burgoyne, J. Wild and I. Fujinaga, "An expert ground truth set for audio chord recognition and music analysis",
*ISMIR* (2011); M. Neuwirth, D. Harasim, F. C. Moss and M. Rohrmeier, "The Annotated Beethoven Corpus (ABC)",
*Frontiers in Digital Humanities* 5 (2018); R. O. Gjerdingen and J. Bourne, "Schema theory as a construction
grammar", *Music Theory Online* 21 (2015); E. Bigand and R. Parncutt, "Perceiving musical tension in long chord
sequences", *Psychological Research* 62 (1999); M. Rohrmeier and I. Cross, "Modelling unsupervised online-learning
of artificial grammars: linking implicit and statistical learning", *Consciousness and Cognition* 27 (2014).
