# Music, Built: Part 21, Form

Part 21 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth part of Act III. Parts 16 to 20 built music a few bars at a time; this part
asks what holds minutes together. It starts from the speech-to-song illusion, teaches the small forms (phrase, period,
sentence) and the large ones (binary, ternary, rondo, variation, sonata, song), builds a picture in which repetition can
be seen (the self-similarity matrix) and a program that finds a piece's sections from its sound alone (Foote's novelty
curve), measures how much tunes repeat themselves, tests the golden-section claims against chance, and ends with the
experiments on whether listeners hear large-scale form at all. The form tools are Monochord's
(`explainer/music/monochord/form.py`); the pieces are composed in `compute.py` from the Tune and played on Part 7's
piano; the looped phrase is spoken by the series' own narrator voice. Published findings are the ones listed under
Sources.

* **Say it again.** Deutsch's discovery (mid-1990s) and her 2011 study; a phrase, "sometimes behave so strangely", spoken
  by the narrator's voice and repeated ten times, heard; form as the plan of what returns; the plan.
* **1. Phrase, period, sentence.** Cadence and phrase; Caplin's period and sentence (1998); an ear question (which of two
  themes on the Tune is the period?); the Tune's opening as a contrasting period; Beethoven's first sonata.
* **2. Binary and ternary.** ‖: A :‖: B :‖, rounded binary and the Baroque suite; A B A, the da capo aria and the minuet
  and trio; their self-similarity pictures.
* **3. Seeing repetition.** Foote's self-similarity matrix (1999): a chroma column per beat, cosine similarity; the
  Tune (A B C C A B) read as stripes and blocks; the same picture from the sound of the Tune with its harmony, heard.
* **4. Finding the seams.** Foote's checkerboard kernel and novelty curve (2000); on the Tune's sound, 5 of 5 phrase ends
  found within two beats, with 5 extra peaks at chord changes; the kernel's width sets the scale of form it sees.
* **5. Rondo and variation.** An ear question (how many times does the opening strain return?): A B A C A on the Tune,
  with B in G and C the opening of *Ode to Joy* in F, heard; rondo and variation pictures; Mozart's variations on the
  Tune; this series as a set of variations.
* **6. Sonata: a drama of keys.** Exposition, development, recapitulation; a miniature sonata on the Tune whose second
  theme is its opening inverted, its keys over time from Part 15's key finder (C, G; A minor, F, D minor, G; C);
  Hepokoski and Darcy's medial caesura and essential closures (2006).
* **7. Song forms.** Strophic, AABA, verse and chorus (a rondo in disguise), and the twelve-bar blues on the Tune's head,
  heard.
* **8. Form from sound.** The segmenter on the whole sonata, heard: 9 of its 11 boundaries within two beats, 2 false
  alarms; on every piece of this part (best of three kernel widths): sonata 82 in a hundred, rondo and ternary 50,
  verse-chorus 44, AABA 40, binary 17, variations 14; one setting for all, 44; what novelty cannot see (a seam between a
  passage and its own repeat).
* **9. Why so much repetition?** In Part 14's 54 tunes, 32 notes in a hundred belong to a four-note figure (intervals and
  rhythm) heard earlier in the same tune, against 1 when the notes are shuffled; the Tune, 64; mere exposure (Zajonc
  1968); Margulis's *On Repeat* (2014).
* **10. The golden section, tested.** The claims (Lendvai, Howat, Putz 1995); if a larger part lies anywhere between half
  and three-quarters of the whole, a hit within 0.02 of 0.618 happens 16 times in a hundred by chance (simulated: 16.1);
  this part's sonata, composed without regard to it, divides at 0.625; climaxes of the 54 tunes: 37 in the first half,
  2 within 0.02 of 0.618, as chance predicts (2.2).
* **11. Must the ending be home?** An ear question (two short pieces, one ending in G, one in C: which ends where it
  began?); Cook (1987): a home ending preferred only for pieces under about a minute; Karno and Konečni (1992): a
  rearranged Mozart movement liked about as well.
* **12. Frontier: form at scale.** Local and global structure in perception (Tillmann and Bigand); the SALAMI annotations
  (2011) and annotator disagreement; Music Transformer (2018) and long-range structure. ★ research problem: memory for
  themes and memory for keys, measured separately.
* **Variation 21, recap and problems.** The miniature sonata, heard whole; the ledger; what we found; five problems;
  where it comes back; in practice; references; Part 22.

## What is computed, and what is heard

`python -m videos.music.music21.compute` (a few minutes) fills `.cache/music21/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | the spoken phrase, looped ten times | — |
| `phrase` | a sentence and a period on the Tune | — |
| `forms` | self-similarity matrices of binary, ternary, rondo, variations, AABA and verse-chorus plans | symmetric, unit diagonal |
| `tune` | the Tune with harmony: chroma from notes and sound, self-similarity, novelty at two widths, boundaries | the Tune's phrase ends |
| `rondo` | A B A C A, heard | — |
| `sonata` | the miniature sonata: keys over time, novelty, boundaries | its section starts |
| `blues` | twelve bars on the Tune's head | — |
| `segment` | the segmenter on every piece, three kernel widths | the pieces' change boundaries |
| `repetition` | repeated four-note figures in the 54 tunes | shuffled tunes |
| `golden` | climax positions; the chance of a golden hit | a simulation |
| `closure` | two short pieces, one ending away | — |

Monochord's form tools are held in `tests/music/test_form.py`; this part's claims and clips in
`tests/music/test_music21.py`.

**Sounds.** Part 7's piano (a struck string through the soundboard, `physical model`) in twelve-tone equal temperament;
the looped phrase is the series' synthesized narrator voice (`synthesized`). There are no recordings.

**What the models are, and are not.** *The pieces* are composed for this part on the Tune and on *Ode to Joy*, with
block chords every two beats; they are demonstrations of plans, not stylistic imitations. *Chroma from the sound* gives
each short-time spectrum's energy to the nearest of the twelve pitch classes between 60 Hz and 2 kHz, and is averaged
per beat with the beat known; real systems must find the beat first (Part 62). *The novelty curve* uses Foote's tapered
checkerboard; boundaries are scored only where the material changes (between different sections), within two beats,
since a seam between a passage and its own repeat produces no novelty, and the film says so. *Repetition* is measured
on four-note figures with their rhythm, transposition allowed, in Part 14's tunes, which were written out from memory.
*The golden-section base rate* assumes the larger part is equally likely anywhere between half and three-quarters of the
whole; other assumptions change the number but not the point. *The perception experiments* are summarized from the
publications, not recomputed.

## Build

```bash
python -m videos.music.music21.compute                          # numbers and sounds (a few minutes)
EXPLAINER_TTS=silent python tools/build.py music21 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music21 --sync                         # the sound gates
python tools/dead_air.py renders/music21_480p.mp4 --sound music21  # no empty screen; no sound over a still one
python tools/lecture_length.py music21                          # 30 to 60 minutes, listening included
python tools/build.py music21                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 21                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Label the phrases of *Ode to Joy* (Part 14's version) and say whether its first eight bars are a period
   or a sentence.

   *Solution.* Its four two-bar phrases are A B A B′: E E F G G F E D | C C D E E. D D, then the same again with the
   ending E. D C C. The first four bars end on D over the dominant (open), the second four on C (closed), and both halves
   begin alike: a parallel period, the classic case.

2. **Prove.** Show that a self-similarity matrix is symmetric with ones on its diagonal, and that a passage repeated after
   d beats makes a stripe on the d-th diagonal.

   *Solution.* S(i, j) is the cosine of the angle between columns i and j, which is symmetric in i and j and equals 1
   when i = j (for any non-zero column). If the music from beat a to beat a + L is repeated exactly from beat a + d,
   columns a + k and a + d + k are equal for k < L, so S(a + k, a + d + k) = 1 along a segment of the d-th diagonal: a
   bright stripe parallel to the main one, offset by d.

3. **Ear.** The lab plays six short forms on the Tune. For each, name the plan: AABB, ABA, ABACA, AABA, or variations.

   *Solution.* The lab prints the answers. Count the returns of the opening strain and listen for whether a contrasting
   section comes back (rondo) or never does (binary); variations keep the harmony and change the surface.

4. **Build.** Add a stripe detector to the segmenter, so that it finds the seam between a passage and its own repeat, and
   score it on this part's pieces.

   *Where to look.* Smooth the matrix along its diagonals, then look for bright segments on off-diagonals (a time-lag
   matrix makes them horizontal lines); the start of each segment and the start of its repeat are boundaries. Score
   with `form.boundary_score` against all section starts, not only the change boundaries; the binary piece's middle
   seam (A|A) should appear.

5. ★ **Themes or keys?** Design an experiment that measures listeners' memory for themes and for keys separately, over
   minutes.

   *Where the frontier is.* Cook's design manipulates the final key; a complementary design manipulates whether the final
   theme returns, crossing the two, at several piece lengths, with recognition and completeness ratings and with
   musicians and non-musicians. If the theme manipulation survives at lengths where the key manipulation fades, form
   works through thematic memory.

## Sources

* D. Deutsch, T. Henthorn and R. Lapidis, "Illusory transformation from speech to song", *JASA* 129 (2011).
* W. E. Caplin, *Classical Form* (1998); J. Hepokoski and W. Darcy, *Elements of Sonata Theory* (2006); C. Rosen,
  *Sonata Forms* (1980).
* J. Foote, "Visualizing music and audio using self-similarity", ACM Multimedia (1999); "Automatic audio segmentation
  using a measure of audio novelty", ICME (2000).
* E. H. Margulis, *On Repeat* (2014); R. B. Zajonc, "Attitudinal effects of mere exposure", *JPSP* 9 (1968).
* J. Putz, "The golden section and the piano sonatas of Mozart", *Mathematics Magazine* 68 (1995); E. Lendvai, *Béla
  Bartók: An Analysis of His Music* (1971); R. Howat, *Debussy in Proportion* (1983).
* N. Cook, "The perception of large-scale tonal closure", *Music Perception* 5 (1987); M. Karno and V. J. Konečni,
  "The effects of structural interventions in the first movement of Mozart's Symphony in G minor, K. 550, on aesthetic
  preference", *Music Perception* 10 (1992); B. Tillmann and E. Bigand, "The relative importance of local and global
  structures in music perception", *JAAC* 62 (2004).
* J. B. L. Smith, J. A. Burgoyne, I. Fujinaga, D. De Roure and J. S. Downie, "Design and creation of a large-scale
  database of structural annotations", ISMIR (2011); C.-Z. A. Huang and others, "Music Transformer", ICLR (2019).
* Part 14 for the tunes; Part 15 for the key finder; Part 7 for the piano.
