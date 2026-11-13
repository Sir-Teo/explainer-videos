# Music, Built: Part 6, Tuning

Part 6 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). Part 5 found that the smoothest intervals are the ones at which partials line up:
2:1, 3:2, 5:4. This part asks whether an instrument can have them all at once. It cannot, for a reason that lies in
the integers, and every tuning system is a decision about where to put the error. The systems are Monochord's
(`explainer/music/monochord/tuning.py`), exact where they can be and checked against Barbour's tables; every sound
is computed in `compute.py`. Dates and attributions are the published ones, listed under Sources.

* **In tune, and sinking.** One progression of four chords, sung four times in perfectly pure chords, ends 86 cents
  flat; the first chord and the last; Zhu Zaiyu's twelfth root of two (1584), to twenty-four decimal places; the plan.
* **1. The circle that will not close.** Twelve pure fifths, folded into one octave, and the thirteenth note: the
  Pythagorean comma, 531441/524288 = 23.46 cents; a worked example (can any number of fifths equal a number of
  octaves? never: odd against even); Pythagorean tuning, eleven pure fifths and a wolf of 678.5 cents; its thirds.
* **2. The other comma.** Four pure fifths against a pure third: the syntonic comma, 81/80 = 21.5 cents (an ear
  question); three pure thirds against an octave: the diesis, 128/125 = 41 cents; just intonation as a lattice of
  fifths and thirds; its own wolf, the fifth D to A at 40:27.
* **3. The comma pump.** A worked example: once round I–vi–ii–V–I in exact fractions (the D that goes with A is
  10/9, not 9/8), and the tonic returns at 80/81; four rounds; Benedetti's letters; the question every keyboard has
  to answer.
* **4. Pure thirds, and a wolf.** Aron's meantone (1523); a worked example (each fifth gives up a quarter of the
  comma: 696.6 cents, the fourth root of five); the chord of C major in Pythagorean tuning, equal temperament and
  meantone; round the circle: a wolf fifth 36 cents wide and four thirds 41 cents wide; an ear question (the chord on
  C and on A flat); two centuries of use, and split keys.
* **5. Well tempered.** Werckmeister III (1691): the Pythagorean comma taken from four fifths; the major third in
  every key for four tunings; an ear question (the chords on C, E and F sharp: 4, 16 and 22 cents wide); key
  character; Bach's title (1722).
* **6. Equal.** Two cents from every fifth; the twelfth root of two; a worked example (a square root, a square root
  and a cube root; the first fret of a 650 mm guitar string is 36.5 mm from the nut); an ear question (a pure third
  and the piano's, 13.7 cents wide, beating ten times a second); a worked example (the fifth A3–E4 beats 0.74 times a
  second) and the tuner's table; three centuries to win.
* **7. Why twelve?** The best fifth and the best third of every equal division from 4 to 60; a worked example (the
  continued fraction of log₂(3/2): 1/2, 3/5, 7/12, 24/41, 31/53); five and seven as the black and the white keys;
  the major chord in 12, 19, 31 and 53 steps; Jing Fang, Huygens, and an organ with 31 notes to the octave.
* **8. The piano's stretched octaves.** Stiff strings have sharp partials (Part 1), so the smooth octave is a wide
  one (Part 5); an exact and a stretched octave on very stiff strings; a model of Railsback's curve (1938), from 20
  cents flat at the bottom to 26 sharp at the top.
* **9. What players do.** Fixed and free instruments; four habits of good intonation; the open strings of a
  quartet, and the comma between the cello's C and the violin's E; do choirs drift? (Howard, 2007; D'Amario and
  colleagues, 2020); the pitch of A, from about 415 to 440 Hz.
* **10. Frontier: tuning that moves.** Adaptive tuning; Lehman's reading of the loops on Bach's title page (2005)
  and the replies; what is not known. ★ research problem.
* **Variation 6, recap and problems.** The Tune with chords, a phrase at a time, in Pythagorean tuning, meantone in
  C, meantone in the wolf key, Werckmeister III, and 12, 19, 31 and 53 equal steps; the ledger; what we found; five
  problems; where it comes back; in practice; references; a plucked string, and Part 7.

## What is computed, and what is heard

`python -m videos.music.music6.compute` (a few seconds) fills `.cache/music6/`.

| Item | What it computes | Checked against |
|---|---|---|
| `pump` | I–vi–ii–V–I four times in pure triads with common tones held; the tonic after each round | every chord 4:5:6 or 10:12:15; 80/81 a round, exactly |
| `circle` | twelve pure fifths folded into the octave; Pythagorean tuning's fifths and thirds | 3¹²/2¹⁹; the wolf at 678.5 cents |
| `syntonic` | (3/2)⁴ against 5/4; (5/4)³ against 2; the lattice of just intonation; the fifth D–A | 81/80, 128/125, 40/27 |
| `meantone` | quarter-comma meantone: every fifth, third and the wolf; three tunings of C major | Barbour's table (to 0.05 cent) |
| `well` | the thirds and fifths of four tunings in every key; Werckmeister III | Barbour's table |
| `equal` | the twelfth root of two by integer arithmetic; errors; the tuner's beat rates; fret positions | 24 decimals; F3–A3 at 6.93 beats a second |
| `why12` | the continued fraction of log₂(3/2); fifth and third errors of every division from 2 to 60 | convergents 7/12, 24/41, 31/53 |
| `piano` | beatless octaves on strings with a model inharmonicity, summed across the keyboard | the shape and size of Railsback's curve |
| `tune` | Variation 6 in eight tunings; the error of each version's chords | 1 cent (53 equal) to 31 cents (the wolf key) |

Monochord's tuning layer is held against Barbour's tables and exact arithmetic in `tests/music/test_tuning.py`;
this part's claims and clips in `tests/music/test_music6.py`.

**Sounds.** Fourteen clips, labelled on screen. `synthesized`: tones of seven partials in the proportions 1, 0.88,
0.88² … (the same tone as Part 5), sustained so that beats can be heard; for the piano's octave the partials are
those of a stiff string. `physical model`: Part 1's plucked string, at the end. There are no recordings.

**What the models are, and are not.** The tunings are exact. The piano curve is a model: every octave beatless
(judged by the 6:3 partials in the bass, 4:2 in the middle and 2:1 in the treble), on strings whose inharmonicity
rises from 0.0001 in the tenor to 0.016 at the top, values of the size reported for grand pianos (Fletcher and
Rossing, ch. 12); real tuners also weigh other intervals, and real curves are bumpier. The row of loops in chapter
10 is a sketch of the pattern on Bach's title page (three kinds of loop, eleven in all), not a facsimile. The
history of pitch in chapter 9 shows typical values; pitch varied widely from place to place. The "adaptive"
curve in chapter 10 is a sketch, and says so.

## Build

```bash
python -m videos.music.music6.compute                          # numbers and sounds (a few seconds)
EXPLAINER_TTS=silent python tools/build.py music6 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music6 --sync                         # the sound gates
python tools/dead_air.py renders/music6_480p.mp4 --sound music6   # no empty screen; no sound over a still one
python tools/lecture_length.py music6                          # 30 to 60 minutes, listening included
python tools/build.py music6                                   # 1080p30, narrated
python -m pytest -q tests/music                                # Monochord against its references; this part's claims and clips
python -m videos.music.labs 6                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **A tuner's third.** In equal temperament with A4 = 440 Hz, find the frequencies of F3 and A3 and the beat rate
   of the major third between them. How fast does the same third beat an octave higher?

   *Solution.* A3 = 220 Hz. F3 is four semitones below it: 220 / 2^(4/12) = 174.61 Hz. A pure third would put the
   fourth partial of A3 on the fifth partial of F3: 4 × 220 = 880 against 5 × 174.61 = 873.07. They differ by 6.93
   Hz, so the third beats about seven times a second, wide. An octave higher both frequencies double and so does
   the difference: 13.86. Tuners use this: thirds beat faster, steadily, as they climb the keyboard. (The lab
   computes both.)

2. **The wolf, and the diesis.** Show that in quarter-comma meantone the diminished sixth G♯–E♭ exceeds a pure
   fifth by 35.7 cents, and that three pure major thirds fall short of an octave by 128/125.

   *Solution.* Twelve fifths must total seven octaves, 8400 cents. Eleven of them are 696.58 cents (a pure fifth,
   701.96, less a quarter of the syntonic comma, 5.38): 7662.36 in all. The twelfth is 8400 − 7662.36 = 737.64
   cents, which is 35.68 above pure. Equivalently: it is wide by eleven quarter-commas less the Pythagorean comma,
   11 × 5.377 − 23.460 = 35.68. For the thirds: (5/4)³ = 125/64, and 2 ÷ 125/64 = 128/125, or 41.06 cents. In
   meantone, where the thirds C–E and E–G♯ are pure, the "third" G♯–C is what is left of the octave: a pure third
   plus the diesis, 427 cents.

3. **Ear.** The lab (`python -m videos.music.labs 6`) plays the major chord on C in four tunings, in a random
   order. Rank them from stillest to busiest, and name the equal-tempered one.

   *Solution.* The four are just intonation (no beats), quarter-comma meantone (a pure third, and a fifth 5.4 cents
   narrow that wavers about 2.4 times a second), twelve equal steps (a third 13.7 cents wide, beating about ten
   times a second) and Pythagorean (a third 21.5 cents wide, beating about sixteen times a second). The lab prints
   the order it played, and each chord's root-mean-square error in cents: 0.0, 3.8, 9.8 and 15.2.

4. **Build.** Add sixth-comma meantone and Vallotti's temperament to `tuning.py`, and draw their thirds round the
   circle. Which keys does each favour?

   *Solution sketch.* `meantone(Fraction(1, 6))` already gives the first: fifths 698.4 cents, thirds 7 cents wide in
   the eight good keys, and a much milder wolf (a fifth 16 cents wide). Vallotti's (c. 1750) is a well
   temperament: `from_fifths("Vallotti", {n: narrow for n in ("F", "C", "G", "D", "A", "E")})` with `narrow` a pure
   fifth less a sixth of the Pythagorean comma, the other six pure. Its thirds run from 6 cents wide on F, C and G
   to 22 cents on B, F♯ and C♯ and back: like Werckmeister III, but more evenly graded and centred on the same
   plain keys.

5. **★ Research.** Write an adaptive tuner: given the notes sounding, choose the pitches that minimise Part 5's
   roughness, with a penalty for moving a held note. Run it on the comma pump. How small can the penalty be before
   the pitch drifts?

   *Pointers.* This is the problem of Sethares's adaptive tuning (1994) and of commercial schemes such as Hermode
   tuning; see also Stange, Wick and Hinrichsen, "Playing music in just intonation: a dynamically adaptive tuning
   scheme" (*Computer Music Journal*, 2018), who model the notes as joined by springs. With no penalty the tuner
   reproduces the pump and sinks a comma a round; with a large one it stays in equal temperament. In between it
   must distribute the comma, and the open questions are perceptual: how fast may a held note glide before the
   glide is heard, and do listeners prefer the result?

## Sources

Books: J. M. Barbour, *Tuning and Temperament: A Historical Survey* (1951), for the tables of meantone and
Werckmeister III; R. W. Duffin, *How Equal Temperament Ruined Harmony (and Why You Should Care)* (2007); W. A.
Sethares, *Tuning, Timbre, Spectrum, Scale* (2nd ed., 2005); G. J. Cho, *The Discovery of Musical Equal Temperament in
China and Europe in the Sixteenth Century* (2003); M. Lindley, *Lutes, Viols and Temperaments* (1984); N. H. Fletcher
and T. D. Rossing, *The Physics of Musical Instruments* (2nd ed., 1998), ch. 12, for the inharmonicity of piano
strings; R. Steblin, *A History of Key Characteristics in the Eighteenth and Early Nineteenth Centuries* (2nd ed.,
2002), for Schubart.

Sources and papers: P. Aron, *Toscanello in musica* (1523); G. B. Benedetti, *Diversarum speculationum mathematicarum
et physicarum liber* (1585), for the letters to Cipriano de Rore; Zhu Zaiyu, *Lülü jingyi* (1584–96); S. Stevin,
*Vande spiegheling der singconst* (c. 1605; published 1884); M. Mersenne, *Harmonie universelle* (1636); A.
Werckmeister, *Musicalische Temperatur* (1691); C. Huygens, "Lettre touchant le cycle harmonique" (1691); J. S. Bach,
*Das wohltemperirte Clavier* (1722); C. F. D. Schubart, *Ideen zu einer Ästhetik der Tonkunst* (written 1784–85,
published 1806); O. L. Railsback, "Scale temperament as applied to piano tuning", *JASA* 9 (1938); B. Lehman,
"Bach's extraordinary temperament: our Rosetta Stone", *Early Music* 33 (2005), and the replies by M. Lindley and
I. Ortgies and by J. O'Donnell, *Early Music* 34 (2006); D. M. Howard, "Intonation drift in a capella soprano, alto,
tenor, bass quartet singing with key modulation", *Journal of Voice* 21 (2007); S. D'Amario, D. M. Howard,
H. Daffern and N. Pennill, "A longitudinal study of intonation in an a cappella singing quintet", *Journal of
Voice* 34 (2020); W. A. Sethares, "Adaptive tunings for musical scales", *JASA* 96 (1994).
