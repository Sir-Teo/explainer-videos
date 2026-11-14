# Music, Built: Part 32, The Geometry of Chords

Part 32 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth part of Act V. Part 31 named the moves between triads; this part puts every
chord in a space. Following Tymoczko (2006) and Callender, Quinn and Tymoczko (2008), it folds the plane of voices by
octave and permutation into a Möbius strip for two notes and a twisted prism for three, measures the size of a voice
leading, tests the claim that nearly even chords are the ones that reach their own transpositions cheaply, treats scales
as chords and the circle of fifths as a map of shortest paths, counts chords under the five OPTIC symmetries, reads
chords' Fourier magnitudes, and measures how close Bach's chorales come to the shortest paths. The geometry is
Monochord's (`explainer/music/monochord/geometry.py`); Bach's chorales are Part 17's; every chord is played on Part 7's
piano, and the gliding voices of the hook are synthesized. Published findings are the ones listed under Sources.

* **Two voices, one chord.** An ear question: two voices that cross and two that meet and turn back (no one can tell:
  at every instant they hold the same two pitches); *Science*, 2006; the plan.
* **1. Chords as points.** Two voices as a point of the plane and a voice leading as a path; octave and permutation
  fold the plane (a torus, then half of it, glued with a twist, with the unisons as an edge); a short history; why fold.
* **2. The Möbius strip.** All 78 two-note chords of twelve-note equal temperament, unisons on the one edge, tritones down
  the middle; parallel, contrary and oblique motion as three directions, heard; crossing and bouncing as one path; Fux's
  cantus with Part 16's best first-species line as a path whose every step is a shortest one (52 semitones, the
  minimum), heard.
* **3. Three notes: a triangle in a prism.** The 91 shapes of three-note chords in a triangle, the augmented triad at the
  centre; from a cluster to the augmented triad, heard (distance from even 4.24, 2.83, 1.41, 0.82, 0); C major to C minor
  by quarter-semitones through the neutral triad, heard; the twisted prism; four notes and the tetrahedron, the
  diminished seventh at its centre; the smallest voice leading from C major to every triad (1 to C and E minor, 6 to D,
  F sharp and B flat major).
* **4. The size of a voice leading.** An ear question (C major to F major two ways: 3 semitones against 15); three norms
  (sum, Euclidean, largest leap) on three voice leadings; chords of different sizes; how the minimum is found.
* **5. Nearly even chords.** Evenness against the smallest voice leading to a different transposition, for all 12 three-note
  and 29 four-note chord types: only (037), (0258), (0358) and (0157) beat moving every voice a semitone, and the
  perfectly even chords do not; C major to E major and C7 to E♭7 in 2 semitones, the C major scale to G major in 1,
  heard; Chopin's E minor prelude; why it matters.
* **6. Scales are chords too.** The 38 seven-note scale types by evenness: diatonic, then melodic minor, then harmonic
  minor and major; C, G and D major, one semitone apart, heard; the circle of fifths measured (the smallest voice
  leading from C major to each major scale is its number of steps round the circle); scales in jazz; two levels at once.
* **7. Five symmetries.** O, P, T, I, C; C major and its mirror image, F minor, heard; chord counts by brute force (three
  notes: 364 under OP, 298 under OPC, 31 under OPT, 19 under OPTIC; four notes: 1,365 and 48); what each space is called.
* **8. What each Fourier coefficient hears.** The discrete Fourier transform of a pitch-class set; six portraits; an ear
  question (which six-note chord is built from fifths? the pentatonic, |F₅| = 3.73); phases; the history (Lewin, Quinn,
  Amiot, Yust).
* **9. How smooth is Bach?** The first phrase of *Wachet auf* (BWV 140.7), heard, with Bach's motion and the minimum under
  every change; all 364 chorales: in 17,339 changes of chord, the upper three voices take the minimum 67 times in 100
  (mean 5.9 semitones against 3.8, and 8.6 with the voices shuffled), all four voices 40 times; an ear question (Bach's
  voices or the same chords with their upper notes reassigned: 51 semitones against 103); why the excess is always even;
  what the measurement does not show.
* **10. Frontier: what the geometry does not explain.** Function, the bass, register, rhythm, timbre; the argument;
  rival geometries; beyond twelve notes; ★ research problem: does voice-leading size predict how smooth a progression
  sounds?
* **Variation 32, recap and problems.** The Tune's first two phrases harmonized by the smallest voice leadings among the
  chords of C major (C C Am C F Am Dm C, 16 semitones), then among chords outside C major (C C A C Fm C Gm C, 18); the
  ledger; what we found; five problems; where it comes back; in practice; references; Part 33.

## What is computed, and what is heard

`python -m videos.music.music32.compute` (about a minute) fills `.cache/music32/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | crossing and bouncing glides (an ear question) | the same two pitches at every instant |
| `strip`, `duet` | the 78 dyads on the strip; three kinds of motion; Fux's cantus and a first-species line | brute-force minimal sizes |
| `triangle`, `neutral` | the 91 shapes and their evenness; a walk to the centre; major to minor by quarter-tones | — |
| `vlsize` | three voice leadings and three norms (an ear question); C major to all 24 triads | brute force with octaves (tests) |
| `even` | evenness and nearest transposition for every 3- and 4-note set class; three demonstrations | — |
| `scales` | the 38 seven-note types by evenness; three keys; the circle of fifths measured | — |
| `mirror`, `optic` | a chord and its inversion; chord counts under each combination of symmetries | set-class counts (Part 29) |
| `fourier` | magnitudes and champions for sizes 3 to 7; an ear question | — |
| `bach` | Bach's voice leading against the minimum, with a shuffled control; *Wachet auf*; an ear question | the parity theorem |
| `tune`, `variation` | Variation 32: two Viterbi harmonizations by smallest voice leading | — |

Monochord's tools are held in `tests/music/test_geometry.py`; this part's claims and clips in
`tests/music/test_music32.py`.

**Sounds.** Part 7's piano (a physical model), retuned for the quarter-tone chords; the hook's gliding voices are
synthesized. Bach's chorale is played from the music21 corpus encoding, as in Part 17. There are no recordings.

**What the models are, and are not.** *Voice-leading size* here is a sum of semitones between pitch classes; Bach's
measured motion uses real pitches, so octave leaps count. *The minimum* ignores register, ranges and every other rule of
part writing. *The beat chords* are the notes sounding on each beat; passing notes between beats are not counted.
*Evenness* is the Euclidean distance to the nearest perfectly even chord; other measures (Fourier magnitudes among them)
rank chords a little differently. *The prism and tetrahedron* are described, not drawn in three dimensions.

## Build

```bash
python -m videos.music.music32.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music32 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music32 --sync                         # the sound gates
python tools/dead_air.py renders/music32_480p.mp4 --sound music32  # no empty screen; no sound over a still one
python tools/lecture_length.py music32                          # 30 to 60 minutes, listening included
python tools/build.py music32                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 32                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Find the smallest voice leading from C major to A♭ minor, and from C⁷ to F♯⁷.

   *Solution.* C, E, G to C♭ (B), E♭, A♭: C down to B, E down to E♭, G up to A♭: 3 semitones, the hexatonic pole of Part 31.
   C, E, G, B♭ to F♯, A♯, C♯, E: E and B♭ (A♯) hold, C up to C♯, G down to F♯: 2 semitones, the tritone substitution.

2. **Prove.** Prove that the excess of any voice leading over the minimal one between the same two chords is even.

   *Solution.* For any assignment σ of the second chord's notes to the first chord's voices, the total motion Σ|bσ(i) − aᵢ|
   has the parity of Σ(bσ(i) − aᵢ) = Σb − Σa, whatever σ is, and whether the moves are real (any octave) or the shortest
   way round (they differ from the real moves by multiples of 12). So every voice leading between the two chords has the
   same parity, and the difference of two of them is even.

3. **Ear.** The lab plays pairs of progressions; one in each pair is the minimal voice leading. Find it.

   *Solution.* The lab prints the answers. The minimal one keeps a common tone and moves the others by steps; the other
   moves every voice the same way by a leap.

4. **Build.** Draw the Möbius strip of two-note chords in 19-note equal temperament, and place its thirds.

   *Where to look.* `geometry.dyad_strip` works for any real pitch classes: scale a 19-step pitch class k to 12k/19 and plot
   all 190 dyads; the 19-tone major third (6 steps, 379 cents) and minor third (5 steps, 316 cents) sit close to the
   12-tone ones but on a different lattice, and the tritone line holds no dyad because 19 is odd.

5. ★ **Does voice-leading size predict how smooth a progression sounds?**

   *Where the frontier is.* Choose pairs of progressions that are equally short under one measure (voice-leading size,
   PLR distance, Lerdahl's chord distance) and not under others; ask listeners which is smoother and which belongs
   together, with register, spacing and timbre held fixed; fit each measure to the judgements and compare predictions on
   held-out pairs with intervals; report whether musical training changes the winner.

## Sources

* D. Tymoczko, "The geometry of musical chords", *Science* (2006); C. Callender, I. Quinn and D. Tymoczko, "Generalized
  voice-leading spaces", *Science* (2008); D. Tymoczko, *A Geometry of Music* (2011).
* D. Lewin, "Re: Intervallic relations between two collections of notes", *Journal of Music Theory* (1959); I. Quinn,
  "General equal-tempered harmony", *Perspectives of New Music* (2006–07); E. Amiot, *Music Through Fourier Space* (2016);
  J. Yust, "Schubert's harmonic language and Fourier phase space", *Journal of Music Theory* (2015).
* C. Callender, "Continuous transformations", *Music Theory Online* (2004); J. Roeder, *A Theory of Voice Leading for
  Atonal Music* (1984); R. Cohn, *Audacious Euphony* (2012).
* D. Huron, *Voice Leading: The Science behind a Musical Art* (2016); J. Hook, "Why are there twenty-nine tetrachords?",
  *Music Theory Online* (2007).
* Part 12 for maximal evenness; Part 16 for Fux; Part 17 for the chorales; Part 29 for set classes; Part 31 for the
  Tonnetz.
