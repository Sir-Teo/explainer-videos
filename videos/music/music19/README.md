# Music, Built: Part 19, Chromatic Harmony

Part 19 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act III. Part 18 measured the syntax of harmony inside a key;
this part leaves the key. It starts from the opening of *Tristan und Isolde* and walks the road that leads there:
borrowed leading notes and borrowed chords, the Neapolitan and the augmented sixths, the diminished seventh's
symmetry and the enharmonic trapdoors it opens, the comma those trapdoors hide, chromatic mediants and the
hexatonic cycle; then it builds a pathfinder between keys and a tension measure from Lerdahl's tonal pitch space,
and returns to the four readings of the Tristan chord. The chromatic toolkit is Monochord's
(`explainer/music/monochord/chromatic.py`); Bach's counts come from Part 17's chorales
(`explainer/music/monochord/chorales.py`); every example is realized in four voices in `compute.py` and played on
Part 7's piano. Published findings are the ones listed under Sources.

* **Four notes, and 160 years.** *Tristan und Isolde* (1859, staged 1865): the opening chord and its resolution,
  twice, heard; four readings; the plan.
* **1. One borrowed leading note.** F♯ leans on G as B leans on C: V7 of V; a chain of applied dominants in C,
  heard; Part 15's key finder two chords at a time hears F, G, A minor, D minor, the whole passage C major
  (tonicization against modulation); in Bach's major chorales, a major chord or dominant seventh where the key has a
  minor chord (or a seventh on the tonic) on 934 of 10,014 beats, 9 in a hundred: II most of all (263, and 168 with a
  seventh).
* **2. Borrowing from the minor.** Mixture: iv, ♭VI, ♭VII and ♭III in C major, heard; Schubert's major and minor;
  Bach's major chorales borrow on only 70 of 10,014 beats (54 of them ♭VII), but 105 of the 116 minor chorales that
  end on their tonic end on a major chord: the Picardy third, heard.
* **3. The Neapolitan.** An ear question (i–iv6–V7–i against i–N6–V7–i: which chord is further from home?);
  ♭II as a predominant; the diminished third D♭–B; Beethoven's *Moonlight* sonata.
* **4. Augmented sixths.** A♭ and F♯ closing on G from both sides; the Italian, French and German sixths in C
  minor, heard; the German sixth sounds like a dominant seventh; its parallel fifths into V, the cadential 6/4 that
  avoids them, and Mozart fifths.
* **5. The diminished seventh.** B D F A♭ on the twelve-note clock: a square, only three such chords; one chord
  resolved to C, E♭, F♯ and A minor, heard; spelled four ways.
* **6. Enharmonic trapdoors.** An ear question (the same third chord twice: which passage leaves C?): a German sixth
  resolving home, and the same keys as the dominant seventh of D♭; F♯ = G♭ on the keyboard; doors from C to
  E♭, F♯ and A in a single chord.
* **7. The comma it hides.** An ear question (four minor thirds and the octave, pure then equal: which agree?): four
  pure minor thirds overshoot the octave by 62.6 cents and beat at about 10 Hz against it; three pure major
  thirds fall 41.1 cents short (the diesis); a choir singing C, E, A♭, C in pure thirds sinks 41.1 cents a lap, 205
  in five; meantone's G♯ and A♭, split keys, well and equal temperament.
* **8. Chromatic mediants.** C to E to A♭ to C, one note held and two moving by a semitone; P and L; the hexatonic
  cycle (Cohn 1996), every step one semitone of motion; both heard.
* **9. The shortest way to any key.** Breadth-first search on 24 keys, step by step (312 connections with pivots): with pivot chords only, 11 keys one step from C
  and 12 two steps; with the German sixth, the diminished seventh and the Neapolitan as doors, 19 one step and 4 two;
  C to F♯ major through E minor, or directly by a respelled diminished seventh.
* **10. Measuring tension.** Lerdahl's basic space (2001); δ = i + j + k; C to G 5, to A minor 7, to D minor 8, C
  major to F♯ major 23; tension curves within the key (at most 7), through mixture and the Neapolitan (up to 19)
  and through a trapdoor (18 at the turn); Lerdahl and Krumhansl (2007); tension on a tree: D minor costs 5 as a
  step but carries 10 hanging from G7 and the final C.
* **11. Four readings of one chord.** The Tristan opening again; a French sixth with an appoggiatura, a
  half-diminished seventh, an altered dominant, Kurth's chord of pure tension (1920); as pitch classes it reaches the
  dominant seventh E G♯ B D with two semitones of motion.
* **12. Frontier: extended tonality.** The least voice-leading distance between all 24 triads (24 pairs one semitone
  apart: P and L; 60 two apart); Weitzmann (1853), Riemann, Cohn (1996, 2012), Tymoczko (2006); corpus measures of
  chromaticism; film music (Lehman 2018). ★ research problem: a chromaticism measure listeners agree with.
* **Variation 19, recap and problems.** The Tune's two phrases with mixture and applied dominants, in minor with
  the Neapolitan, and through a diminished-seventh trapdoor into A♭; the ledger; what we found; five problems; where
  it comes back; in practice; references; Part 20.

## What is computed, and what is heard

`python -m videos.music.music19.compute` (about a minute) fills `.cache/music19/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | the *Tristan* opening reduced to its harmony, twice | — |
| `applied` | a chain of applied dominants; applied-dominant beats in Bach's major chorales | — |
| `mixture` | iv; ♭VI–♭VII; ♭III in C major | — |
| `neapolitan` | i–iv6–V7–i and i–N6–V7–i in C minor | — |
| `sixths` | the Italian, French and German sixths in C minor, each to V | `chromatic.augmented_sixths` |
| `dim7` | one diminished seventh resolved to four minor keys | `chromatic.dim7_resolutions` (eight keys) |
| `trapdoor` | a German sixth to C, and the same keys to D♭ | `chromatic.german_as_dominant` |
| `comma` | pure and equal minor thirds against the octave (organ tones) | `chromatic.enharmonic_drift` |
| `mediants` | major-third cycle; the hexatonic cycle | each hexatonic step one semitone |
| `paths` | fewest steps from C to every key, with and without the doors | breadth-first search |
| `tension` | Lerdahl's distance; three tension curves | Lerdahl's worked values (I–V 5) |
| `tristan` | the four readings; the least voice leading to the resolution | — |
| `tune` | Variation 19 | every chord holds the Tune's note; no parallels |

Monochord's chromatic toolkit is held in `tests/music/test_chromatic.py`; this part's claims and clips in
`tests/music/test_music19.py`.

**Sounds.** Part 7's piano (a struck string through the soundboard, `physical model`) in twelve-tone equal
temperament, except chapter 7's pure and equal thirds, which are organ tones synthesized at exact frequencies.
There are no recordings.

**What the models are, and are not.** *The Tristan excerpt* is reduced to its harmony, four voices, with the cello's
opening line omitted; it is a reduction, not a performance. *Applied dominants in Bach* are counted from Part 17's
beat labels: a major triad or dominant seventh on a degree where the key itself has a minor chord, or a seventh on
the tonic; a few such chords are borrowings or passing chords rather than applied dominants. *The pathfinder's steps*
are a simplification: one step is any single chord that can belong to both keys, either as a shared triad or through
one of the three doors; real modulations take several chords, and composers weigh steps unequally (problem 4).
*Lerdahl's distance* is implemented in its chord-to-chord form, with chords placed in keys by hand; his full model
measures tension on a prolongational tree, which this part does not build (Part 22 builds trees). *The frontier's
corpus and perception findings* are summarized from the publications, not recomputed.

## Build

```bash
python -m videos.music.music19.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music19 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music19 --sync                         # the sound gates
python tools/dead_air.py renders/music19_480p.mp4 --sound music19  # no empty screen; no sound over a still one
python tools/lecture_length.py music19                          # 30 to 60 minutes, listening included
python tools/build.py music19                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 19                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Spell the diminished seventh on G♯ four ways, and resolve each to its tonic in four voices.

   *Solution.* G♯ B D F resolves to A (major or minor): G♯→A, B→A or C, D→C♯ or C, F→E. Respelled as B D F A♭ it
   is vii°7 of C; as D F A♭ C♭, of E♭; as E♯ G♯ B D, of F♯. In each case the root of the spelling is the leading
   note and rises a semitone; the seventh falls a semitone; the other two voices move to the nearest notes of the
   tonic triad, which usually doubles the third in the resolution.

2. **Prove.** Prove that a chord which divides the octave into equal parts has as many distinct transpositions as
   its step, and count them for the augmented triad and the diminished seventh.

   *Solution.* A chord whose notes are 0, s, 2s, … (mod 12), with s dividing 12, is mapped to itself by transposition
   by s. Transposing by t gives the same set exactly when t is a multiple of s, so the transpositions 0, 1, …, s − 1
   give distinct sets and every other transposition repeats one of them: there are s. The augmented triad (s = 4) has
   four transpositions, the diminished seventh (s = 3) three, the tritone (s = 6) six.

3. **Ear.** The lab plays ten cadences in C minor. For each, name the chord before V: iv6, N6, or an augmented sixth
   (which?).

   *Solution.* The lab prints the answers. iv6 is F minor over A♭ in the bass; N6 is D♭ major over F, darker,
   its D♭ falling by a diminished third to B; the augmented sixths have A♭ in the bass and F♯
   above it, the outer voices opening to an octave on G; the French adds the whole-tone colour of D, the German the
   fuller sound of E♭ (and its parallel fifths with G, which composers often hide behind a 6/4).

4. **Build.** Give the pathfinder a cost for each kind of step, and find the cheapest route from C to every key.
   Which keys change their route?

   *Where to look.* Replace the breadth-first search in `chromatic.distances` by Dijkstra's algorithm with a cost for
   each kind of edge (for example, a shared triad 1, a German sixth 2, a diminished seventh 2, a Neapolitan 3). Keys
   reached by a door in one step but by pivots in two, such as A♭ major or D♭ major, change when a door costs more
   than two pivots. A cost model is a theory of how surprising each modulation is, and could be fitted to a corpus.

5. ★ **A measure of chromaticism.** Design a corpus measure of chromaticism that a listener would agree with, and
   say how you would test it.

   *Where the frontier is.* Simple measures count notes outside the key, the variety of keys, or how evenly the
   twelve pitch classes are used in a window; each misjudges something (a chromatic passing note is not a
   modulation; an enharmonic trapdoor uses few chromatic notes). A test would ask listeners to rate how far from
   home passages sound, and compare the ratings with each measure, controlling for tempo and texture. Lerdahl and
   Krumhansl's tension studies and the corpus studies of tonal complexity are the starting points.

## Sources

* Wagner, *Tristan und Isolde* (1859; Munich, 1865), prelude, bars 1–7, reduced.
* S. G. Laitz, *The Complete Musician* (4th ed., 2015); E. Aldwell and C. Schachter, *Harmony and Voice Leading*
  (4th ed., 2011): applied chords, mixture, the Neapolitan, augmented sixths, enharmonic modulation.
* F. Lerdahl, *Tonal Pitch Space* (2001); F. Lerdahl and C. L. Krumhansl, "Modeling tonal tension", *Music
  Perception* 24 (2007).
* R. Cohn, "Maximally smooth cycles, hexatonic systems, and the analysis of late-Romantic triadic progressions",
  *Music Analysis* 15 (1996); *Audacious Euphony* (2012).
* D. Tymoczko, "The geometry of musical chords", *Science* 313 (2006); *A Geometry of Music* (2011).
* C. F. Weitzmann, *Der übermässige Dreiklang* (1853); H. Riemann, *Vereinfachte Harmonielehre* (1893).
* E. Kurth, *Romantische Harmonik und ihre Krise in Wagners Tristan* (1920).
* F. Lehman, *Hollywood Harmony* (2018).
* Part 6 for the commas; Part 15 for keys and pivot chords; Part 17 for the chorales and voice leading.
