# Music, Built: Part 31, Transformations

Part 31 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act V. Parts 27 to 30 followed harmony past the edge of the key;
this part asks what logic connects chords when no key holds them. It names Riemann's moves P, L and R, builds the PLR
and T/I groups by brute force and shows they are dual, draws every triad on Euler's Tonnetz closed into a torus, walks
the hexatonic and octatonic cycles, Beethoven's chain and every tour of the 24 triads, hears the moves in film and jazz,
and ends at the frontier: which geometry of chords matches what listeners hear. The moves, groups and walks are
Monochord's (`explainer/music/monochord/neoriemann.py`); every progression is ours, played on Part 7's piano and bowed
string. Published findings are the ones listed under Sources.

* **Two chords that share no key.** A film-style progression of our own (C, E, C, A flat, F, C), heard; each pair keeps
  one note; an ear question.
* **1. Naming the moves.** P, L and R from C major, each keeping two notes (an ear question: which is P?); the same three
  from A minor (to A, F and C major); a table of what each move does to a major and a minor triad; Riemann's dualism;
  two-step moves (LP to E, PL to A flat, RP to A), heard; Lewin.
* **2. Two groups, one duality.** The PLR group and the T/I group built by brute force: 24 elements each, commuting,
  each acting on the 24 triads in exactly one way; the commuting square (T₃ then P, P then T₃: E flat minor either way),
  heard; the orders of the moves (2, 2, 2; PL 3, PR 4, LR 12) and P = R(LR)³, so L and R alone generate a dihedral
  group of order 24; distance; what the duality means.
* **3. The Tonnetz.** Euler's lattice (1739); the moves as flips of triangles; the torus; how far every triad is from C
  major (1, 3, 6, 8, 5 and 1 at 0 to 5 steps; B flat minor alone at five); a random walk of eight moves, heard; the
  history of the map; the syntonic comma that keeps it open in just intonation (386.3 against 407.8 cents, 21.5 cents
  apart), heard; isomorphic keyboards.
* **4. Hexatonic and octatonic cycles.** P, L repeated (six triads) and P, R repeated (eight), heard; the scales they
  make (Part 28's); Cohn's hexatonic systems; the four hexatonic and three octatonic families; octatonic families in
  Rimsky-Korsakov and Stravinsky; Weitzmann's region (1853), the augmented triad resolving to its six neighbours, heard.
* **5. The long chain.** Beethoven's Ninth (Cohn's reading): nineteen triads by R and L, heard; an ear question (which
  chain stays in one key?); the full chain of 24; why it must visit every triad; 62 tours of all 24 triads, counted by
  search, one of them (11 P, 9 L, 4 R) heard.
* **6. Wonder, and the uncanny.** Chromatic mediants; an ear question (which pair shares no note? the hexatonic pole);
  three trips from C major (to E, A flat and F sharp major), heard; Lehman's *Hollywood Harmony*; scoring with moves;
  where the moves came from.
* **7. Thirds in jazz.** Coltrane changes, named (the tune is in copyright and is not played); three keys a major third
  apart on the Tonnetz; the skeleton of the idea in our own voicing (B, D7, G, B♭7, E♭, F♯7, B), heard; seventh chords:
  ten dominant and half-diminished sevenths within two semitones of C7 (nine moving two voices a semitone, one moving one
  voice a whole tone), with the tritone substitution and the move inside *Tristan*'s first chords, heard; beyond triads.
* **8. Frontier: other spaces, real listeners.** Krumhansl's ratings; PLR distance against voice-leading distance for all
  23 triads (correlation 0.74; D, F sharp and B flat major need six semitones); other spaces; learned chord embeddings;
  an audit of what this part measured; ★ research problem: which geometry of triads matches what listeners hear?
* **Variation 31, recap and problems.** The Tune harmonized by a walk on the Tonnetz (at most two moves every two beats,
  to a triad holding the melody note, ending at home): C, C, A minor, C, F, C, G, C; the ledger; what we found; five
  problems; where it comes back; in practice; references; Part 32.

## What is computed, and what is heard

`python -m videos.music.music31.compute` (about a minute) fills `.cache/music31/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | the film-style progression and its moves, heard | — |
| `plr`, `minor`, `compound` | P, L and R from C major (an ear question) and A minor; two-step moves; voice leading in semitones | definitions (tests) |
| `groups`, `commute`, `relations` | both groups by closure; commutation; simple transitivity; orders; P = R(LR)³ | brute force |
| `spheres`, `walk`, `vl` | breadth-first distances from C; a random walk; PLR against voice-leading distance | — |
| `cycles`, `systems`, `weitzmann` | the hexatonic and octatonic cycles and families; Weitzmann's region, heard | — |
| `chain`, `keys`, `hamilton` | the R-L chain; an ear question; every Hamiltonian cycle of the PLR graph | the L-R graph's single tour |
| `poles`, `film3` | the hexatonic pole (an ear question); three trips from C | — |
| `thirds`, `sevenths` | three keys a major third apart through their dominants; seventh-chord neighbours of C7 | — |
| `comma` | the pure third against four pure fifths, heard | Part 6's comma |
| `tune`, `variation` | Variation 31: the Tune harmonized by a dynamic-programming walk on the Tonnetz | — |

Monochord's tools are held in `tests/music/test_neoriemann.py`; this part's claims and clips in
`tests/music/test_music31.py`.

**Sounds.** Part 7's piano and bowed string (physical models). There are no recordings. The progressions are ours;
Beethoven's chain is heard only as its skeleton of triads in our voicing (the chain itself, not his orchestration), and
the Coltrane changes are a progression, not the tune.

**What the models are, and are not.** *Voice leading* here is the fewest semitones three (or four) voices must move,
with octaves ignored; real voice leading also weighs register, doubling and which voice moves. *Distance* is counted in
P, L and R steps; a theory with other moves (Cohn's, Tymoczko's, the circle of keys) would count differently. *The
harmonizer* uses only the moves and the melody: it knows nothing of function, cadence or style, which is why its
rediscovery of tonic, subdominant and dominant is worth noticing. *Film and listener claims* are cited, not measured.

## Build

```bash
python -m videos.music.music31.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music31 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music31 --sync                         # the sound gates
python tools/dead_air.py renders/music31_480p.mp4 --sound music31  # no empty screen; no sound over a still one
python tools/lecture_length.py music31                          # 30 to 60 minutes, listening included
python tools/build.py music31                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 31                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Find the shortest PLR word from C major to F♯ major, and count the semitones the voices move.

   *Solution.* Four steps, for instance P, R, P, R (C, C minor, E flat, E flat minor, F sharp), the most any major triad
   needs. C, E, G to C♯, F♯, A♯ moves each voice: C to C♯ (1), E to F♯ (2), G to A♯ (3): 6 semitones, the most any
   triad needs from C major; the two chords share no note.

2. **Prove.** Prove that P, L and R each commute with every transposition Tₙ.

   *Solution.* Each move is defined from a triad's root and quality alone: P keeps the root, L(r major) = (r + 4)
   minor, R(r major) = (r + 9) minor, and the inverse formulas for minor triads. Transposing adds n to the root and keeps
   the quality, so Tₙ(L(r major)) = (r + 4 + n) minor = L((r + n) major) = L(Tₙ(r major)), and the same for P, R and
   minor triads. (Each move also commutes with inversion, because it is itself defined by inversion about the interval it
   keeps, and inverting conjugates one such inversion into another.)

3. **Ear.** The lab plays eight pairs of triads; each pair is P, L or R. Name them.

   *Solution.* The lab prints the moves. P changes the colour (major to minor) and keeps the root in the bass; L moves a
   voice by a semitone and the bass by a major third; R moves one voice a whole tone and the bass by a minor third.

4. **Build.** Write a program that harmonizes any melody by a walk on the Tonnetz, and compare it with Part 17's
   harmonizer.

   *Where to look.* `neoriemann.harmonize` is dynamic programming over the 24 triads: the state is the current triad,
   the cost of a step is zero to stay and 3k plus the voice leading for k ≤ 2 moves. Run it and Part 17's Viterbi
   harmonizer on the chorale melodies Part 17 held out, and compare agreement with Bach's chords; expect the Tonnetz
   walk to do worse on cadences, which it cannot see, and to wander less.

5. ★ **Which geometry of triads matches what listeners hear?**

   *Where the frontier is.* Choose pairs of triads that the circle of keys, PLR distance and voice-leading distance rank
   differently (the hexatonic pole is close by voice leading and far by key); collect similarity and fit ratings from
   listeners with varied training; fit a model on each distance, and on combinations, and compare their predictions on
   held-out pairs with intervals; report whether training or film exposure changes which distance wins.

## Sources

* D. Lewin, *Generalized Musical Intervals and Transformations* (1987); R. Cohn, *Audacious Euphony* (2012);
  D. Tymoczko, *A Geometry of Music* (2011); F. Lehman, *Hollywood Harmony* (2018).
* R. Cohn, "Maximally smooth cycles, hexatonic systems, and the analysis of late-Romantic triadic progressions", *Music
  Analysis* (1996); R. Cohn, "Neo-Riemannian operations, parsimonious trichords, and their *Tonnetz* representations",
  *Journal of Music Theory* (1997); A. S. Crans, T. M. Fiore and R. Satyendra, "Musical actions of dihedral groups",
  *American Mathematical Monthly* (2009).
* C. L. Krumhansl, "Perceived triad distance: evidence supporting the psychological reality of neo-Riemannian
  transformations", *Journal of Music Theory* (1998).
* L. Euler, *Tentamen novae theoriae musicae* (1739); C. F. Weitzmann, *Der übermässige Dreiklang* (1853); H. Riemann,
  *Ideen zu einer "Lehre von den Tonvorstellungen"* (1914–15).
* A. Childs, "Moving beyond neo-Riemannian triads: exploring a transformational model for seventh chords", *Journal of
  Music Theory* (1998); E. Gollin, "Some aspects of three-dimensional *Tonnetze*", *Journal of Music Theory* (1998).
* Part 6 for the comma; Part 13 for triads; Part 19 for the hexatonic cycle; Part 27 for *Tristan*; Part 28 for the
  symmetric scales; Part 29 for inversion.
