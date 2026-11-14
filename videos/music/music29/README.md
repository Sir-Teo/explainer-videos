# Music, Built: Part 29, Twelve Tones

Part 29 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act V. Part 28 loosened the key with symmetric scales and new
rhythms; this part follows Vienna, where Schoenberg gave the key up and then looked for a law to replace it. It builds
the mathematics theorists later found underneath, pitch-class sets, their classes and interval vectors, Z-relations, the
hexachord theorem, rows, all-interval rows and combinatoriality, verifying every count by enumeration and proving the
theorems on screen, and asks whether listeners can hear any of it. The tools are Monochord's
(`explainer/music/monochord/atonal.py`). Two pieces are played from the music21 corpus's encodings, both now in the
public domain: Schoenberg's Six Little Piano Pieces, Op. 19, Nos. 2 and 6 (1911), and Webern's canon *Dormi Jesu*,
Op. 16 No. 2 (1924). The rows of Schoenberg's Op. 25 and Berg's *Lyric Suite* are shown as rows; every other example is
ours.

* **The air of another planet.** Schoenberg's Second String Quartet (1908); Op. 19 No. 6, whole, heard; the plan.
* **1. Atonality, free.** The emancipation of the dissonance; Op. 19 No. 2, whole, heard; its pitch classes counted (G
  and B tower, all twelve used); the two bell chords of No. 6, each a stack of fourths; Vienna's expressionism.
* **2. Pitch-class sets.** Transposition and inversion on the clock; an ear question (is B a transposition or an
  inversion of A?); prime forms (the Tristan chord and the half-diminished seventh share (0 2 5 8)); Lewin's operations;
  interval vectors.
* **3. Counting the chords.** 224 set classes by brute force; the twelve trichords heard; Burnside's lemma, (4096 + ...)/24
  = 224; Forte's table matched (12, 29, 38, 50, 38, 29, 12).
* **4. Same intervals, different sets.** The two all-interval tetrachords heard; 23 Z-pairs (15 among hexachords); the
  hexachord theorem, checked on all 924 hexachords; a hexachord and its complement heard; the proof by double counting,
  with the general difference (12 − 2k)(1,1,1,1,1,½).
* **5. The row and its forty-eight forms.** The method; Schoenberg's life; the Op. 25 row heard (three tetrachords, ends a
  tritone apart); the matrix; an ear question (retrograde or inversion?); Webern's *Dormi Jesu* analysed (all 45 intervals
  inverted, all 46 durations equal, the clarinet a bar ahead), Webern's life, and the canon heard whole.
* **6. All-interval rows.** Berg's row heard; rows and machines (the *Illiac Suite*); 3,856 all-interval rows found by
  search, 176 equal to their own retrograde a tritone higher; the one-line proof that first and last notes are a tritone
  apart; Berg.
* **7. Combinatoriality.** Aggregates; a row of ours and its combinatorial inversion heard; the six all-combinatorial
  hexachords; Webern's Op. 21 row (24 forms, not 48); Babbitt.
* **8. Total serialism.** Messiaen, Boulez, Darmstadt; a pointillist passage of ours heard; minimalism's reaction;
  Stravinsky and Copland turn serial; Xenakis, Ligeti and Cage on the cloud of points.
* **9. Can anyone hear it?** An ear question (which line is a form of the row?); Francès, Krumhansl and colleagues;
  Lerdahl's cognitive constraints; rows in film and jazz; a shared hexachord by chance, 1 in 924.
* **10. Frontier: homometry and perception.** Patterson's homometric sets; Lutyens, Crawford Seeger, Hauer, Cage; the
  Fourier view (Lewin, Quinn, Amiot); ★ research problem: do listeners hear interval content, or only surface features?
* **Variation 29, recap and problems.** A row grown from the Tune's intervals (0 7 9 11 1 2 4 6 8 10 3 5) and a pointillist
  variation on three of its forms; the ledger; what we found; five problems; where it comes back; in practice; Part 30.

## What is computed, and what is heard

`python -m videos.music.music29.compute` (about a minute) fills `.cache/music29/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `op19` | Op. 19 Nos. 6 and 2 from the encodings; pitch-class time; simultaneities' set classes | Part 27's measures |
| `sets`, `classes`, `trichords` | two chords related by inversion; prime forms and vectors; 224 classes two ways; the twelve trichords | Forte's table |
| `zhex`, `hexpair` | Z-pairs; the hexachord theorem on all 924 hexachords; an example pair | the proof |
| `row`, `op25` | a row's 48 forms and matrix; Webern's canon compared line against line; the Op. 25 row | the encoding |
| `allint`, `combin` | all 3,856 all-interval rows; the six all-combinatorial hexachords; a combinatorial pair | published counts |
| `total`, `hear` | a pointillist passage; a form against a reordering; the chance of a shared hexachord | 1/924 |
| `tune` | Variation 29 | — |

Monochord's tools are held in `tests/music/test_atonal.py`; this part's claims and clips in
`tests/music/test_music29.py`.

**Sounds.** Part 7's piano and bowed string (physical models); Part 17's synthetic voice singing a vowel for the soprano
of *Dormi Jesu* (synthesized). There are no recordings.

**What the models are, and are not.** *Prime forms* follow Rahn's packing rule, which differs from Forte's for a handful
of sets; the counts do not depend on the rule. *Op. 19* is played at a fixed tempo without Schoenberg's dynamics and
pedal. *Webern's canon* is sung on a vowel, not the Latin text, and the clarinet is replaced by Part 7's bowed string.
*The row forms* are played in one octave, so an interval and its complement can sound alike. *The perception claims*
are those of the published studies; the film's ear questions are illustrations, not experiments.

## Build

```bash
python -m videos.music.music29.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music29 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music29 --sync                         # the sound gates
python tools/dead_air.py renders/music29_480p.mp4 --sound music29  # no empty screen; no sound over a still one
python tools/lecture_length.py music29                          # 30 to 60 minutes, listening included
python tools/build.py music29                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 29                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Find the prime form and interval vector of {2, 5, 9, 11}. Which familiar chord is it?

   *Solution.* D, F, A, B: rotated to B, D, F, A it spans 10 semitones as 0, 3, 6, 10; its inversion packs tighter as
   0, 2, 5, 8, the prime form. The vector is [012111]. It is the half-diminished seventh on B (and, as a set class, also
   the dominant seventh).

2. **Prove.** Show that a hexachord and its complement have the same number of tritones.

   *Solution.* The twelve pitch classes form six tritone pairs. Let t pairs lie inside the hexachord, t′ inside the
   complement and a across. Counting the hexachord's six notes, 2t + a = 6; counting the complement's, 2t′ + a = 6. So
   t = t′.

3. **Ear.** The lab plays a row and then eight lines; four are forms of it and four are the row with two notes swapped.
   Which are forms?

   *Solution.* The lab prints the answer. Swapped lines keep most of the row's contour and so sound closer than many
   true forms; listen for the intervals between neighbours rather than for the notes.

4. **Build.** Write a program that finds, in a twelve-tone piece's encoding, which forms of its row each passage uses.

   *Where to look.* Read the notes with `romantic.parse_all`, take each voice's pitch classes in order, and slide a window
   of twelve along them, testing against `atonal.forms(row)` with `atonal.find_form` for partial matches at the edges;
   allow repeated notes and chords, which composers use freely, by collapsing immediate repetitions and reading chords
   in register order.

5. ★ **Do listeners hear interval content, or only surface features?**

   *Where the frontier is.* Choose chord pairs that are Z-related, in the same class, or unrelated, voice them with
   matched register, spacing and loudness, collect similarity judgements from trained and untrained listeners, and fit a
   model in which similarity depends on the interval vectors (or the Fourier magnitudes) and on surface features;
   report how much each explains, with intervals.

## Sources

* J. N. Straus, *Introduction to Post-Tonal Theory* (4th ed., 2016); A. Forte, *The Structure of Atonal Music* (1973);
  J. Rahn, *Basic Atonal Theory* (1980); D. Lewin, *Generalized Musical Intervals and Transformations* (1987).
* A. Schoenberg, "Composition with twelve tones" (1941), in *Style and Idea*; M. Babbitt, "Some aspects of twelve-tone
  composition" (1955) and *Collected Essays* (2003).
* A. L. Patterson, "Ambiguities in the X-ray analysis of crystal structures", *Physical Review* (1944); E. Amiot, *Music
  Through Fourier Space* (2016); I. Quinn, "General equal-tempered harmony", *Perspectives of New Music* (2006–07).
* C. L. Krumhansl, G. J. Sandell and D. C. Sergeant, "The perception of tone hierarchies and mirror forms in twelve-tone
  serial music", *Music Perception* (1987); R. Francès, *La perception de la musique* (1958); F. Lerdahl, "Cognitive
  constraints on compositional systems" (1988).
* M. S. Cuthbert and C. Ariza, "music21" (*ISMIR* 2010), whose corpus holds the Schoenberg and Webern encodings.
* Part 3 for the Fourier transform; Part 12 for Burnside's lemma; Part 22 for hierarchy; Part 27 for chromaticism;
  Part 28 for symmetric sets.
