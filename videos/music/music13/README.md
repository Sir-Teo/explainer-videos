# Music, Built: Part 13, Intervals and Chords

Part 13 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). Part 12 chose the notes; this part sounds them together. It names intervals
exactly and finds their qualities on the line of fifths; shows that the four triads are what is left when three
notes may not be neighbours; tests Rameau's claim that a chord has a root whichever way up it stands, and finds
where the root comes from; adds sevenths, and the tritone that makes harmony move; computes why the same chord is
clear in the middle of the piano and muddy at the bottom, what to double and what to leave out; writes a chord
four ways; and lays all the triads out on Euler's lattice. The chord module is Monochord's
(`explainer/music/monochord/chords.py`), the pictures are in `explainer/music/chordviz.py`, the engraver
(`explainer/music/staff.py`) now draws chords and a grand staff, and every sound is computed in `compute.py`.
Published findings are the ones listed under Sources.

* **Three notes, one name.** C, E and G in three orders, heard; Rameau's claim (1722) that they are one chord;
  the same three notes close together at the bottom of the piano, and spread (a growl, and a clear chord); the
  plan.
* **1. Naming a distance.** An interval's number, counted in letters, both ends included; its quality; all
  thirteen intervals from C to the octave, heard; the line of fifths: one step apart is perfect, two to five
  major (sharpward) or minor (flatward), six augmented or diminished; inversion (the numbers add to nine, the
  qualities swap) and the six interval classes; one key with two names: C–F♯ and C–G♭ in quarter-comma meantone,
  579 and 621 cents, against the piano's 600; an ear question (which of three is the tritone).
* **2. Three notes.** Two sizes of third, four triads, heard; Zarlino (1558): a major triad is 4 : 5 : 6, a minor
  triad 10 : 12 : 15; of the nineteen shapes of three notes on twelve (Part 12), the four with no two notes a tone
  or less apart are exactly the four triads, and the three with no tritone either are major, minor and augmented;
  an ear question (major or minor).
* **3. The chords of a scale.** A triad on each degree of C major: three major, three minor, one diminished;
  Roman numerals, which name a chord's job and not its key; I, IV and V hold every note of the scale; I–IV–V–I,
  heard.
* **4. Rameau's claim.** Root position and two inversions, and the figures a continuo player reads (5/3, 6,
  6/4); Rameau's fundamental bass: stack the notes in thirds and take the bottom (Lippius had the triad and its
  inversions in 1612); a predict-pause (F, G, B, D: the root is G, the figure 4/2); one chord over each of its
  notes in the bass: settled, lighter, unstable; the six-four that falls to five-three; an ear question (which
  has the root in the bass).
* **5. Where the root comes from.** A major triad is harmonics 4, 5 and 6 of a note two octaves below its root:
  three pure tones and the fundamental they imply, heard; Parncutt's model (1988): each note votes for the roots
  it could be a harmonic of (10, 5, 3, 2, 1): C–E–G gives C 18 votes, C–E♭–G gives C 15 and E♭ 13; a
  predict-pause (B–D–F: a four-way tie that includes G, a note that is not in the chord; heard with the G put
  under it); a table of chords by ambiguity (A–C–E–G goes to C by one vote; the augmented triad ties three ways,
  the diminished seventh eight); Part 4's ear model on the same triads as sound.
* **6. Four notes, and more.** Five seventh chords, heard; the sevenths of a major scale: one dominant seventh,
  the only major triad that carries the scale's tritone; B and F resolving to C and E, alone and inside G7; an
  ear question: a seventh chord in the piano's tuning and as harmonics 4 : 5 : 6 : 7 (the seventh at 969 cents);
  thirds stacked to the thirteenth: the whole scale, every other note.
* **7. Same chord, different sound.** One major third on five Cs, heard: by Part 5's model eleven times rougher
  at the bottom than at the top; why: the third is 1.5 critical bands wide on C5 and 0.3 on C1; roughness of a
  minor third, major third, fifth and octave with the lower note on every key, and the lowest note at which each
  stays as smooth as a major third on C3 (low-interval limits); all 41 four-voice spacings of C major over a low
  C: the roughest, the smoothest and the harmonic series' own spacing, heard.
* **8. Which notes matter.** Doubling, by the root model: root, then fifth, then third; the fifth can be left
  out (it is the root's third harmonic, 8 dB down in Part 7's piano), the third cannot; shells: root, third and
  seventh, heard for three seventh chords; two plucked strings through a hard clipper: by the roughness model a
  distorted major third is twice as rough as a distorted fifth: the power chord.
* **9. Writing a chord down.** One progression as figured bass, Roman numerals, lead-sheet symbols and Nashville
  numbers; played in C and in E♭: the letters change, the numbers do not; the grammar of a lead-sheet symbol,
  which Monochord parses; one set of notes with two names (Am7/C and C6).
* **10. A map of chords.** Euler's lattice (1739): fifths one way, major thirds another; upward triangles are
  major triads, downward ones minor; the three flips that keep two notes (P, L and R), heard; the cycle of six
  triads by semitone steps, heard, which ends three major thirds from where it began: the same key on a piano,
  41 cents away in pure tuning (Part 6's diesis); all 24 triads in one chain, heard: 36 semitones of motion.
* **11. Frontier: what makes a chord sound as it does?** Listeners rank the triads major, minor, diminished,
  augmented; roughness and fusion both put augmented above diminished; Harrison and Pearce (2020): interference,
  harmonicity and familiarity; a chord listener (spectrum, twelve notes, 24 templates): 96 of 96 on clean piano
  chords, 19 of 24 on this part's Variation, four of the five mistakes being C major heard as A minor;
  annotators agree on the root about three times in four (Koops and others, 2019). ★ research problem: from chord
  names to Roman numerals.
* **Variation 13, recap and problems.** The Tune over I, IV and V, each phrase voiced another way: block triads,
  re-voiced, spread, shells of sevenths, close chords over a bass, a full close; the ledger; what we found; five
  problems; where it comes back; in practice; references; Part 14.

## What is computed, and what is heard

`python -m videos.music.music13.compute` (under a minute) fills `.cache/music13/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | C–E–G in three positions; close and spread at the bottom of the piano | roughness 3.9 against 2.6 |
| `intervals` | the thirteen intervals from C: number, quality, place on the line of fifths, inversion, class; the two meantone tritones | the names in any harmony book; 579.5 and 620.5 cents |
| `triads` | the four triads; all nineteen three-note shapes, their interval vectors and roughness | four shapes have no step; three of those no tritone |
| `scale` | the triads on the degrees of C major, with Roman numerals and symbols | I ii iii IV V vi vii° |
| `inversion` | figures of each position; Rameau's reduction of F–G–B–D | 5/3, 6, 6/4; G7 in 4/2 position |
| `roots` | Parncutt's saliences for eight chords; the ear model's pitch for each triad | root ambiguity of a major triad 1.87, the published value of the reference implementation |
| `sevenths` | five seventh chords; those of the scale; the 4 : 5 : 6 : 7 chord; a thirteenth chord | 968.8 cents |
| `voicing` | a major third's roughness and width in critical bands by register; four intervals on every key; 41 spacings ranked | the order minor third, major third, fifth, octave |
| `doubling` | root ambiguity with each note doubled or left out; partial levels of a piano note; clipped dyads | — |
| `symbols` | eight symbols parsed; one progression in four notations and two keys | round trips in `test_chords.py` |
| `tonnetz` | the lattice; P, L, R; cycles of 6, 8 and 24 triads, voice-led | each move keeps two notes; LR visits all 24 |
| `tune` | Variation 13; how far three voices travel in root position and re-voiced | 372 semitones against 60 |
| `frontier` | the four triads by roughness and by fusion; the chord listener on clean chords and on the Variation | 96 of 96; 19 of 24 |

Monochord's chords are held against these in `tests/music/test_chords.py`; the engraver's chords in
`tests/music/test_staff.py`; this part's claims and clips in `tests/music/test_music13.py`.

**Sounds.** Twenty-seven clips. Most are Part 7's piano (`physical model`), in twelve-tone equal temperament. The
two tritones are organ tones in quarter-comma meantone; the missing-fundamental demonstration is three pure tones
at 4, 5 and 6 times 130.8 Hz and an organ tone at 130.8 Hz; the two seventh chords of chapter 6 are organ tones,
one equal-tempered and one at 4 : 5 : 6 : 7 (all `synthesized`). The distorted dyads are Part 1's plucked strings
through a hard clipper (tanh). There are no recordings.

**What the models are, and are not.** *Interval names* are those of common-practice notation; other traditions
count differently. *The census of three-note shapes* treats notes a tone or less apart as "neighbours"; that
threshold is the critical band only in the middle of the keyboard, and the argument is about why thirds, not a
claim that seconds never occur in chords. *The root model* is Parncutt's revision of Terhardt's, with the
weights of his later papers (10, 5, 3, 2, 1) and no weighting for the bass or for register; it is a model of
isolated chords, and in music the bass and the context usually settle what it leaves tied. *The ear model* is
Part 4's summary autocorrelation, which hears a pitch only down to about 30 Hz. *Roughness* is Part 5's
Plomp–Levelt model on seven-partial harmonic tones: it knows nothing of masking by level, of the piano's real
spectrum in each register, or of beats between mistuned harmonics, and its low-interval limits are narrower than
the tables arrangers use (which also differ among themselves); the ordering of the intervals is the robust
part. *The clipper* is a memoryless tanh, not a guitar amplifier. *The order in which listeners rank the triads*
is from published experiments on Western listeners (Roberts 1986; Johnson-Laird and others 2012). *The chord
listener* is a template matcher on a folded spectrum, the starting point of the field in 1999 and nothing like
the state of the art; its 19 of 24 is a property of this Variation and this piano. *The Tonnetz* is drawn in
equal temperament's names; in pure tuning its notes do not repeat. *Dates for the notations* are approximate.
*The Variation's harmony* is one chord to every two beats, only I, IV and V (V7 at the close).

## Build

```bash
python -m videos.music.music13.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music13 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music13 --sync                         # the sound gates
python tools/dead_air.py renders/music13_480p.mp4 --sound music13  # no empty screen; no sound over a still one
python tools/lecture_length.py music13                          # 30 to 60 minutes, listening included
python tools/build.py music13                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 13                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Four intervals.** Name each interval and its inversion: D up to F♯; E up to C; B up to F; A♭ up to F♯. How
   many steps apart are the two notes of each on the line of fifths?

   *Solution.* D–F♯ spans three letters and four semitones: a major third; its inversion is a minor sixth; F♯ is
   four steps sharpward of D (D, A, E, B, F♯). E–C spans six letters and eight semitones: a minor sixth,
   inverting to a major third; C is four steps flatward of E. B–F spans five letters and six semitones: a
   diminished fifth, inverting to an augmented fourth; F is six steps flatward of B. A♭–F♯ spans six letters and
   ten semitones: an augmented sixth, inverting to a diminished third; F♯ is ten steps sharpward of A♭. The
   distances 4, 4, 6 and 10 fall in the bands that give major or minor (2 to 5) and augmented or diminished (6
   to 12), and the direction gives which.

2. **Why thirds.** Three notes divide the twelve-note circle into three steps that add up to twelve. Prove that
   if every step is at least three semitones, the notes form a major, minor, diminished or augmented triad, and
   nothing else.

   *Solution.* Let the steps be a ≤ b ≤ c with a + b + c = 12 and a ≥ 3. Then a is 3 or 4 (if a ≥ 5 the sum is
   at least 15). If a = 4 then b = c = 4: the augmented triad. If a = 3 then b + c = 9 with 3 ≤ b ≤ c, so (b, c)
   is (3, 6) or (4, 5). Steps 3, 3, 6 in any order round the circle are one shape, the diminished triad (with
   its inversions). Steps 3, 4, 5 can be arranged round a circle in two ways that are not rotations of each
   other: 3, 4, 5 (a minor third, then a major third, then a fourth: the minor triad) and 4, 3, 5 (the major
   triad). That is four shapes, and the lab lists all nineteen shapes of three notes to confirm it.

3. **Ear.** The lab plays ten triads. For each, say whether it is major, minor, diminished or augmented, and
   which of its notes is in the bass.

   *Solution.* The lab prints the answers. Listen first for stability: major and minor are at rest, diminished
   and augmented are not. Between major and minor, sing the lowest three notes as an arpeggio and listen for the
   size of the third above the root. For the inversion, listen for the widest gap: a fourth between the upper
   two notes means the third is in the bass, a fourth between the lower two means the fifth is. An augmented
   triad sounds the same in every inversion, so "which note is in the bass" has no answer by ear.

4. **Build.** With `chords.voicings` and `chords.spacing_roughness`, find the smoothest five-voice spacing of a
   G seventh chord over the G at the bottom of the bass staff. Which note does it double? And if one note may be
   left out?

   *Solution.* The lab does this. Of the 114 spacings within three octaves, the smoothest is G2, G3, B4, D5, F5
   (roughness 2.0): the root doubled at the octave, nothing else below middle C, and the upper three notes
   close together at the top. The roughest is G2, B2, D3, F3, G3 (7.1). Left free to omit a note, the model
   drops the fifth: G2, G3, B4, F5 (1.2) is root, root, third, seventh, which is the shell of chapter 8 over a
   doubled bass, and what harmony books recommend for an incomplete dominant seventh.

5. ★ **A heavier bass.** The root model ties on the diminished triad and splits A, C, E, G almost evenly. Give
   the lowest note extra weight. How much weight makes the model agree with the chord symbols in a songbook, and
   what does it then get wrong?

   *Where the frontier is.* In the lab, with A lowest, any weight above about 1.1 makes A the root of A–C–E–G
   (A 17 + 1 > C 18 needs the bass counted a little more than once); but the same weight applied to C–E–G with
   E lowest eventually makes E the root (above a weight of 15/7, about 2.1), which no musician hears. So a single number does
   not do it: a first inversion keeps its root and a "slash chord" does not, and the difference is in the
   context. Parncutt's later models add weights for register and for the preceding chords; corpus-trained
   models (Temperley's Bayesian key and root finding; neural chord estimators) learn them from data; none
   matches annotators on ambiguous chords, and annotators do not match each other (Koops and others 2019).

## Sources

Books: J.-P. Rameau, *Traité de l'harmonie réduite à ses principes naturels* (1722; trans. P. Gossett, 1971), and
*Nouveau système de musique théorique* (1726); G. Zarlino, *Le istitutioni harmoniche* (1558), part 3;
J. Lippius, *Synopsis musicae novae* (1612); L. Euler, *Tentamen novae theoriae musicae* (1739); T. Christensen,
*Rameau and Musical Thought in the Enlightenment* (1993); R. Parncutt, *Harmony: A Psychoacoustical Approach*
(1989); S. Laitz, *The Complete Musician* (4th ed., 2015), chs. 1–6; D. Tymoczko, *A Geometry of Music* (2011),
chs. 2–3; M. Levine, *The Jazz Piano Book* (1989), for shells; C. Williams, *The Nashville Number System* (1988).

Papers: E. Terhardt, "The concept of musical consonance: a link between music and psychoacoustics", *Music
Perception* 1 (1984); R. Parncutt, "Revision of Terhardt's psychoacoustical model of the root(s) of a musical
chord", *Music Perception* 6 (1988); L. A. Roberts, "Consonance judgements of musical chords by musicians and
untrained listeners", *Acustica* 62 (1986); R. Cohn, "Neo-Riemannian operations, parsimonious trichords, and
their Tonnetz representations", *Journal of Music Theory* 41 (1997); T. Fujishima, "Realtime chord recognition
of musical sound", *Proceedings of the International Computer Music Conference* (1999); P. N. Johnson-Laird,
O. E. Kang and Y. C. Leong, "On musical dissonance", *Music Perception* 30 (2012); H. V. Koops, W. B. de Haas,
J. A. Burgoyne and others, "Annotator subjectivity in harmony annotations of popular music", *Journal of New
Music Research* 48 (2019); P. M. C. Harrison and M. T. Pearce, "Simultaneous consonance in music perception and
composition", *Psychological Review* 127 (2020); G. Micchi, M. Gotham and M. Giraud, "Not all roads lead to
Rome: pitch representation and model architecture for automatic harmonic analysis", *Transactions of the
International Society for Music Information Retrieval* 3 (2020); N. Nápoles López, M. Gotham and I. Fujinaga,
"AugmentedNet: a Roman numeral analysis network with synthetic training examples and additional tonal tasks",
*Proceedings of ISMIR* (2021).
