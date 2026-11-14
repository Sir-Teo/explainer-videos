# Music, Built: Part 12, Scales and Modes

Part 12 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). Part 11 said when; this part says which: the few notes a piece of music chooses
out of all there could be. It derives the pentatonic, diatonic and chromatic scales from one interval, the fifth
of Part 1; puts the seven modes in order of brightness; asks what is special about the white keys and gets three
answers (they are maximally even, every interval in them comes in two sizes, and they are deep); meets minor's
three forms, scales of five, six and eight notes, tetrachords, the seventy-two melakartas, maqam and slendro;
and counts every shape a scale can have on twelve notes. The scale module is Monochord's
(`explainer/music/monochord/scales.py`), the pictures are in `explainer/music/scaleviz.py`, and every sound is
computed in `compute.py`. Published findings are the ones listed under Sources.

* **Seven white keys and five black.** The white keys and the black keys, heard; the question (why seven and
  five, and why the black keys come as a two and a three); the plan.
* **1. Stacking fifths.** Pure fifths from F, folded into an octave and drawn round a circle; the steps they
  leave: two sizes at five notes (294 and 204 cents), three at six, two at seven (204 and 90), three from eight
  to eleven, two at twelve (114 and 90); why the stack never closes: the thirteenth note misses the first by
  the Pythagorean comma of Part 3, 23.5 cents; the three stacks played: pentatonic, diatonic, chromatic.
* **2. Three gaps.** The three-gap theorem (1958); the number of sizes for stacks of up to sixty notes; a
  predict-pause (why a sixth note makes three sizes); two sizes at 2, 3, 5, 7, 12, 17, 29, 41, 53: Arabic
  theory's 17, Jing Fang's 53, and the denominators of Part 6's continued fraction.
* **3. Seven notes, seven modes.** The white keys as a chain of fifths, F C G D A E B; a mode for each choice of
  home note, bright to dark along the chain; all seven on C, each the one before with one note lowered; an ear
  question (Dorian and Mixolydian); the seven degrees and their names (tonic, supertonic, mediant, subdominant,
  dominant, submediant, leading note); relative and parallel: A minor has C major's notes and another home, C
  minor has C major's home and three other notes; why the Tune, which has no seventh, is the same in Ionian and
  Mixolydian.
* **4. Why this scale.** Maximal evenness (Clough and Douthett, 1991): note k at ⌊(12k + 5)/7⌋ gives C D E F G
  A B, and the five places left over are the black keys; every kind of interval in two sizes, with the tritone
  as the one landmark; the interval vector ⟨2, 5, 4, 3, 6, 1⟩: a deep scale; a scale moved up a fifth keeps six
  notes, up a semitone only two (heard on C, G and D flat).
* **5. Minor's three forms.** Natural, harmonic (a step of three semitones) and melodic; two endings (an ear
  question): the leading note.
* **6. Fewer notes, and more.** Pentatonic, whole-tone, octatonic and blues scales; how many transpositions each
  has (12, 2, 3, 12): modes of limited transposition; scales with no landmark and no home; a random walk on
  each scale, heard: what the choice of notes does before any melody is composed.
* **7. A scale in two halves.** Tetrachords: the six ways to fill a fourth; the major scale as two equal halves;
  a scale of two other halves; Venkatamakhin's rule and the 72 melakartas (2 × 6 × 6); Mayamalavagowla.
* **8. Other maps of the octave.** A major scale, Rast in quarter tones, five equal steps as a stand-in for
  slendro, and Mayamalavagowla, as bars of cents and as sound; the neutral third, 350 cents, between minor and
  major (an ear question); a caution: a maqam, a raga and a gamelan's tuning are more than rows of pitches;
  what nearly all scales share.
* **9. Every scale there is.** Burnside's lemma on a necklace of four beads, counted by hand (six, not
  sixteen); 2048 sets of notes that contain the home note; on twelve places: 352 shapes, by
  size 1, 1, 6, 19, 43, 66, 80, 66, 43, 19, 6, 1, 1; all 66 shapes of seven notes; three made only of whole and
  half steps (an ear question); one with its half steps as far apart as possible.
* **10. Frontier: why five to seven unequal steps?** The 66 seven-note shapes scored by evenness, by number of
  fifths and by Part 5's roughness: the white keys come first on all three; seven equal steps (an ear
  question): no major or minor, no landmark; Trehub's infants (1999); four explanations, none settled.
  ★ research problem.
* **Variation 12, recap and problems.** The Tune in the seven modes, brightest to darkest, then in pentatonic,
  whole-tone and octatonic scales, with a second voice two places below and a held C; the ledger; what we found;
  five problems; where it comes back; in practice; references; Part 13.

## What is computed, and what is heard

`python -m videos.music.music12.compute` (under a minute) fills `.cache/music12/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | the white keys from C and the black keys, on Part 7's piano | — |
| `stack` | one to twelve pure fifths folded into an octave; their steps in cents | 294/204, 204/90 and 114/90 cents; the comma, 23.46 |
| `gaps` | the number of sizes of step for stacks of 2 to 60 notes | never more than three; two at 2, 3, 5, 7, 12, 17, 29, 41, 53 |
| `modes` | the seven modes on C, spelled; their brightness; which degrees of the Tune each changes | each is the one before with one note lowered |
| `why` | the maximally even seven of twelve; evenness of every seven-note set; interval vectors; common tones | ⟨2, 5, 4, 3, 6, 1⟩; six notes kept a fifth away |
| `minor` | three forms of A minor; two cadences | — |
| `fewer` | four scales and their numbers of distinct transpositions | 12, 2, 3, 12 |
| `halves` | the six tetrachords; the 72 melakartas by Venkatamakhin's rule | 72 different scales; six of the seven modes among them |
| `maps` | Rast in quarter tones, five equal steps, Mayamalavagowla | each adds up to 1200 cents |
| `every` | all necklaces of twelve beads in two colours, listed; Burnside's count | 352 both ways; by size; C(11, 6) = 462 |
| `frontier` | every seven-note shape by evenness, fifths and mean roughness of its pairs (Part 5's model) | the diatonic is first of 66 on each |
| `tune` | Variation 12 | every note is in its phrase's scale |

Monochord's scales are held against these in `tests/music/test_scales.py`; this part's claims and clips in
`tests/music/test_music12.py`.

**Sounds.** Sixteen clips, all on Part 7's piano (`physical model`), some over a held C from an organ tone. The
scales of chapter 1 are in pure fifths; Rast, the five equal steps and the seven equal steps are tuned in cents;
everything else is in twelve-tone equal temperament. There are no recordings.

**What the models are, and are not.** *The stack of fifths* is exact arithmetic. *Brightness* is the sum of a
mode's notes in semitones above its first; it orders the modes as their home notes lie along the chain of fifths,
and it is a convention, not a measurement of anything heard. *Evenness* is the size of one Fourier coefficient of
a set of notes; other measures agree on which seven notes come first. *Roughness* is Part 5's Plomp–Levelt model
on equal-tempered pairs of seven-partial tones, averaged over a scale's 21 pairs; it is one model of consonance,
and the ranking of the middle of the field would change with another, though not the winner. *Rast* is given in
the quarter-tone approximation of twentieth-century Arabic theory (steps of 4, 3, 3, 4, 4, 3, 3 quarter tones);
practice differs by region and by player. *Slendro* is represented by five equal steps, which no gamelan plays
exactly: each is tuned to itself. *The melakartas* are generated by rule; their names and the ragas assigned to
them are not. *The second voice of the Variation* is two scale steps below the melody, with no regard for
harmony; it is there so that the seventh degree, which the Tune lacks, is heard.

## Build

```bash
python -m videos.music.music12.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music12 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music12 --sync                         # the sound gates
python tools/dead_air.py renders/music12_480p.mp4 --sound music12  # no empty screen; no sound over a still one
python tools/lecture_length.py music12                          # 30 to 60 minutes, listening included
python tools/build.py music12                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 12                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Five fifths.** A pure fifth is 702 cents. Stack five of them from C and fold them into one octave. Name the
   five notes, give the steps between them in cents, and say which interval of the major scale is missing from
   this scale altogether.

   *Solution.* The fifths give C, G (702), D (1404 − 1200 = 204), A (906), E (1608 − 1200 = 408). In order: C, D,
   E, G, A, at 0, 204, 408, 702 and 906 cents, with steps of 204, 204, 294, 204 and 294 (the last back up to C).
   There is no semitone anywhere, and so no tritone either: the scale's interval vector is ⟨0, 3, 2, 1, 4, 0⟩.
   That is why any two notes of a pentatonic scale can be sounded together without a harsh clash.

2. **Necklaces of six.** Use Burnside's lemma to count the shapes of scale on six notes to the octave (necklaces
   of six beads in two colours), and list them. Which of them maps onto itself when turned?

   *Solution.* The rotations of six places are by 0, 1, 2, 3, 4 and 5; a rotation by 6/d places (there are φ(d)
   of each kind) leaves 2^(6/d) colourings unchanged. So the count is (1·2⁶ + 1·2³ + 2·2² + 2·2¹)/6 = (64 + 8 + 8
   + 4)/6 = 14. By number of notes: 1, 1, 3, 4, 3, 1, 1. Those that map onto themselves under a turn of less
   than a full circle are the empty set, the full set, the two notes a tritone apart (steps 3 3), the three
   evenly spaced notes (2 2 2), and the four notes with steps 1 2 1 2. A shape with a prime number of notes
   out of a number it does not divide, such as seven of twelve, can never do this, which is one reason diatonic
   scales have twelve distinct transpositions.

3. **Ear.** The lab plays eight scales on C in a random order, each one of the seven modes. Name each, or at
   least say whether it is brighter or darker than the one before.

   *Solution.* The lab prints the order. Listen for the third first (major in Lydian, Ionian and Mixolydian;
   minor in the rest), then for the one note that tells neighbours apart: the raised fourth of Lydian, the
   lowered seventh of Mixolydian, the raised sixth of Dorian against Aeolian, the lowered second of Phrygian,
   and the lowered fifth of Locrian.

4. **Build.** With `scales.stack`, use a generator other than the pure fifth: a fifth of 697 cents (meantone) and
   one of 709. At which numbers of notes do the steps come in two sizes now?

   *Solution.* In the lab set `GENERATOR`. At 697 cents the list is 2, 3, 5, 7, 12, 19, 31: the same up to
   twelve, and then the meantone divisions of Part 6 (19 and 31 equal steps) in place of 17 and 29. At 709 cents
   it is 2, 3, 5, 7, 12, 17, 22, 39. Five, seven and twelve survive any fifth between about 686 and 720 cents:
   they do not depend on the fifth being pure, only on its being roughly seven twelfths of an octave. What
   changes is which of the two steps is the larger: at twelve notes a 697-cent fifth gives steps of 115 and 79
   cents, a pure fifth 114 and 90, and at exactly 700 the two are equal.

5. ★ **Nineteen notes.** On nineteen equal notes to the octave, which seven are maximally even? Is that scale
   deep, and does it have a landmark interval? What would its "black keys" be?

   *Where the frontier is.* The formula ⌊19k/7⌋ gives notes 0, 2, 5, 8, 10, 13, 16, with steps 2, 3, 3, 2, 3,
   3, 3: five large steps and two small, in the diatonic pattern, and it is the scale generated by 19-equal's
   fifth (11 steps). Every generic interval comes in two sizes, so it has Myhill's property, and its tritone
   analogue occurs once. It is not deep in the strict sense (its interval vector, ⟨0, 2, 5, 0, 4, 3, 0, 6, 1⟩,
   has repeated zeros), though its non-zero entries are all different. The complement has twelve notes, with
   steps 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2: a nineteen-note keyboard has seven white keys and twelve black,
   which is how such instruments have been built since the sixteenth century. The open questions are
   perceptual: which of the diatonic scale's properties listeners actually use, and whether scales built to
   have them in other tunings can be learned as readily (see Balzano 1980; Trehub and others 1999; and the
   microtonal literature in Sethares 2005).

## Sources

Books: D. Tymoczko, *A Geometry of Music* (2011), ch. 4; W. A. Sethares, *Tuning, Timbre, Spectrum, Scale* (2nd
ed., 2005); H. Powers and others, "Mode", in *The New Grove Dictionary of Music and Musicians* (2nd ed., 2001);
O. Messiaen, *Technique de mon langage musical* (1944); H. Glarean, *Dodecachordon* (1547); P. Sambamoorthy,
*South Indian Music* (1958–69), for the melakarta scheme; H. Farmer, *A History of Arabian Music* (1929), and
S. Marcus, *Music in Egypt* (2007), for the seventeen-note and quarter-tone systems; J. Kunst, *Music in Java*
(3rd ed., 1973); T. Johnson, *Foundations of Diatonic Theory* (2003).

Papers: V. T. Sós, "On the distribution mod 1 of the sequence nα", *Annales Universitatis Scientiarum
Budapestinensis, Sectio Mathematica* 1 (1958); S. Świerczkowski, "On successive settings of an arc on the
circumference of a circle", *Fundamenta Mathematicae* 46 (1958); C. Gamer, "Some combinational resources of
equal-tempered systems", *Journal of Music Theory* 11 (1967); G. Balzano, "The group-theoretic description of
12-fold and microtonal pitch systems", *Computer Music Journal* 4 (1980); J. Clough and G. Myerson, "Variety and
multiplicity in diatonic systems", *Journal of Music Theory* 29 (1985); N. Carey and D. Clampitt, "Aspects of
well-formed scales", *Music Theory Spectrum* 11 (1989); J. Clough and J. Douthett, "Maximally even sets",
*Journal of Music Theory* 35 (1991); S. E. Trehub, E. G. Schellenberg and S. B. Kamenetsky, "Infants' and adults'
perception of scale structure", *Journal of Experimental Psychology: Human Perception and Performance* 25
(1999); K. Z. Gill and D. Purves, "A biological rationale for musical scales", *PLoS ONE* 4 (2009); J. M. McBride
and T. Tlusty, "Cross-cultural data shows musical scales evolved to maximise imperfect fifths" (preprint,
arXiv:1906.06171, 2019).
