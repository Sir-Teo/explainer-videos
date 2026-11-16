# Music, Built: Part 20, Canon and Fugue

Part 20 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth part of Act III. Parts 16 to 19 set lines against other lines; this part
sets a line against itself. It starts in Potsdam in 1747 with the king's theme and the *Musical Offering*, and asks
which melodies can be combined with themselves: rounds, canons at every interval, the four forms of a line and the
group they make, invertible counterpoint, augmentation and riddle canons, the crab canon, the endlessly rising canon,
and the fugue's subject, answer, countersubject and stretto, built on the Tune; then *The Art of Fugue* and fugues by
machine. The canon tools are Monochord's (`explainer/music/monochord/canon.py`); the tunes are Part 14's corpus
(`explainer/music/monochord/tunes.py`); everything heard is computed in `compute.py` and played on Part 18's plucked
string over Part 7's soundboard, the endless canon in Part 4's Shepard tones. Published findings are the ones listed
under Sources.

* **A king's theme.** Potsdam, 7 May 1747; the royal theme heard (rhythm simplified); the *Musical Offering*; the
  plan.
* **1. Rounds.** *Frère Jacques* in three voices, heard; why a round works (compatible overlapping two-bar pieces; *Sumer is icumen in*); every one of Part 14's 54 tunes sung against itself in three voices at its best delay,
  judged on the strong beats: *Frère Jacques*, *Row, Row, Row Your Boat* and *Three Blind Mice*, the three known
  rounds, rank 1st, 3rd and 4th (the 2nd, *Go Tell Aunt Rhody*, has a harmony that never moves).
* **2. Canon at every interval.** The Goldberg canons (1741), unison to ninth; a solver that counts canons exactly by
  dynamic programming over the leader's last three notes: 12 notes, follower 2 beats later, from 1,378,924 at the
  fifth and 1,371,456 at the octave down to 479,936 at the fourth, of 738,663,910 melodies (1 in 536 at the fifth, 1
  in 1,539 at the fourth); below the leader the counts change at every interval but the octave (the ninth below
  552,984 against 884,555 above); three solver canons heard (unison, second, fifth below).
* **3. Four forms of a line.** An ear question (the phrase, then backwards or upside down?); prime, inversion,
  retrograde, retrograde inversion, heard; inversion within the scale (C C F F E E F) against exact inversion
  (C C F F E♭ E♭ F); their table, checked on the Tune: Klein's four-group.
* **4. Invertible counterpoint.** At the octave every interval of s steps becomes 7 − s: fifths become fourths; an ear
  question (two counter-lines moved above the phrase: the one written freely has 2 dissonant beats, the one without
  fifths 0); at the tenth thirds become octaves, at the twelfth sixths become sevenths.
* **5. Slower, and in riddles.** The phrase against itself in augmentation, heard (3 of 8 strong beats clash: the
  Tune was not designed for it); mensuration canons and Ockeghem's *Missa prolationum*; puzzle canons and
  *quaerendo invenietis*.
* **6. The crab canon.** A line against its own retrograde; filled from both ends at once; counted exactly: 468 of 4
  notes, 11,738 of 6, 299,320 of 8, 7,604,514 of 10, 193,459,554 of 12 (about 25 times more for every two notes); one
  built on the Tune's C, G, A, heard; Hofstadter's crab-canon dialogue (1979).
* **7. A canon that never arrives.** The *Canon per tonos*; a solver canon played seven times, a tone higher each lap,
  in Shepard tones (the seventh lap is the first, sample for sample); pitch height and chroma (Part 4); strange loops.
* **8. Subject and answer.** The fugue's parts; an ear question (real or tonal answer: which stays closer to home?):
  G G D D E E D against G G C C E E D; the tonal answer as a rule.
* **9. An exposition, built.** Subject, tonal answer with a countersubject found by Viterbi search (no fifths), the
  subject in the bass with the countersubject above it (one note altered) and a free voice; heard; 16 beats of two or
  three voices: 0 dissonant, 0 parallels; an episode, a four-note fragment sequenced down a step a bar against its
  inversion, heard (0 clashes in 16 beats).
* **10. Stretto.** Every delay and interval at which the phrase can enter against itself: 11, the closest 2 beats
  behind a fourth below, and a third entry in the bass 4 beats in, an octave and a fifth below, heard; by inversion
  15, 6 of them two beats behind (the stretto fugues of *The Art of Fugue*); 41 of the 54
  tunes' opening phrases allow a stretto by their midpoint; the king's theme (rhythm simplified) none until its second
  entry waits 23 of its 26 beats.
* **11. *The Art of Fugue*.** One subject, about twenty pieces; B–A–C–H heard; the unfinished final fugue and what
  scholars now think of C. P. E. Bach's note.
* **12. Frontier: fugues by machine.** Computational fugue analysis (Giraud, Groult, Leguy and Levé 2015); EMI;
  networks trained on chorales and the 2019 doodle; recognizing transformed melodies (Dowling 1972). ★ research
  problem: does the ear follow a fugue's entries?
* **Variation 20, recap and problems.** The whole Tune as a canon at the fourth below, two beats behind (2 dissonant
  beats in 46); a crab canon on its first notes; the three-voice exposition; the ledger; what we found; five problems;
  where it comes back; in practice; references; Part 21.

## What is computed, and what is heard

`python -m videos.music.music20.compute` (about a minute) fills `.cache/music20/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | the royal theme (rhythm simplified) | — |
| `rounds` | *Frère Jacques* in three voices; every tune ranked as a round | the known rounds |
| `canons` | canons counted at nine intervals, above and below; three sampled | brute force on short canons (tests) |
| `forms` | the four forms of the phrase; their table | the table acting on the phrase |
| `invertible` | two counter-lines and their inversions at the octave; the interval maps | — |
| `augment` | the phrase against its augmentation | — |
| `crab` | crab canons counted; one sampled from the Tune's head | brute force on short crabs (tests) |
| `rising` | a canon a tone higher each lap, in Shepard tones | lap 7 = lap 1 |
| `answers` | real and tonal answers | — |
| `exposition` | a three-voice exposition | no dissonant beat, no parallels |
| `episode` | a fragment sequenced against its inversion | no dissonant beat, no parallels |
| `stretto` | the phrase's strettos, as it is and inverted; the corpus; the royal theme | — |
| `bach` | B–A–C–H | — |
| `tune` | Variation 20 | — |

Monochord's canon tools are held in `tests/music/test_canon.py`; this part's claims and clips in
`tests/music/test_music20.py`.

**Sounds.** A string plucked near its end, as a harpsichord's quill plucks it, through Part 7's soundboard
(`physical model`), in twelve-tone equal temperament; the endless canon in Shepard tones (`synthesized`). There are no
recordings.

**What the models are, and are not.** *The judge of harmony* asks only that every pair of voices sounding on a beat
make a third, fifth, sixth, unison or octave (a fourth allowed above the lowest voice), and that no two voices move in
parallel fifths or octaves; it hears no dissonance between beats and knows nothing of shape, so passing notes in real
music would count as faults if they fell on beats. *The canon counts* are for one note a beat in C major within
C4 to G5, starting and ending on C, with no repeated notes and leaps of at most a fifth or an octave; other choices
can change both the numbers and their order. *The rounds* are judged at each tune's best delay, a whole number of bars of
two beats, on strong beats only, with three voices in unison. *The two Bach subjects* (the royal theme and the head of
*The Art of Fugue*) are written out for the series with their rhythm simplified; no score files were available
offline, so the stretto search was not run on Bach's fugues, and the film says so. *The exposition* is one note a beat
in its counter-lines; a real countersubject would have its own rhythm.

## Build

```bash
python -m videos.music.music20.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music20 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music20 --sync                         # the sound gates
python tools/dead_air.py renders/music20_480p.mp4 --sound music20  # no empty screen; no sound over a still one
python tools/lecture_length.py music20                          # 30 to 60 minutes, listening included
python tools/build.py music20                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 20                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Write the tonal answer to a subject beginning G C B C D (in C major), and say which notes change and
   why.

   *Solution.* The head moves between the dominant (G) and the tonic (C), so those are swapped: G is answered by C and
   C by G, the rising fourth G–C becoming the rising fifth C–G. After the head, the rest goes up a fifth in the scale:
   B → F♯ in G major, C → G, D → A. The answer is C G F♯ G A. A real answer, D G F♯ G A, would begin on D and assert
   G major at once; the tonal answer begins on C, inside the home key.

2. **Prove.** Prove that a line and its retrograde inversion, sounded together, make the same intervals at times t and
   T − t, and say what that implies for a mirror crab canon.

   *Solution.* Let the line be p(t) and its retrograde inversion q(t) = 2a − p(T − t). At time t the interval is
   p(t) − q(t) = p(t) + p(T − t) − 2a; at time T − t it is p(T − t) + p(t) − 2a, the same. So such a canon is
   palindromic in its intervals: whatever is consonant in the first half is consonant in the second, and only half the
   piece needs checking, as in the crab solver, which fills both ends at once.

3. **Ear.** The lab plays eight forms of three short phrases. For each, say: the phrase, inverted, backwards, or both?

   *Solution.* The lab prints the answers. Listen for the rhythm first: a backwards form reverses it (long notes move
   to the other end), an inversion keeps it. Then the direction of the first leap tells inversion from the original.

4. **Build.** Give the stretto finder a fugue subject of your choice in score, find all its strettos, and compare them
   with those the composer used.

   *Where to look.* Encode the subject as (midi, onset, duration) in beats and call `canon.strettos`, adding the
   inverted form (`diatonic_invert`) as a follower. Many of Bach's subjects admit strettos he did not use, and some he
   used break the simple rules (a dissonance on a beat, resolved as a suspension); the finder needs a rule for
   suspensions before its list matches a composer's.

5. ★ **Does the ear follow a fugue?** Design an experiment that tells whether listeners follow a fugue's entries by ear,
   or only on paper.

   *Where the frontier is.* One design: listeners press a key whenever they hear the subject begin, in fugues where the
   entries are known; measure hits, misses and false alarms against training and against the entry's voice (inner
   voices are hardest) and form (Dowling found inversions and retrogrades hard to recognize). Comparing real fugues with
   versions whose entries have been moved tests whether the structure is heard as structure.

## Sources

* J. S. Bach, *Musikalisches Opfer* (1747) and *Die Kunst der Fuge* (1751); C. Wolff, *Johann Sebastian Bach: The
  Learned Musician* (2000), for the visit to Potsdam and the history of *The Art of Fugue*.
* A. Mann, *The Study of Fugue* (1958); R. Gauldin, *A Practical Approach to Eighteenth-Century Counterpoint* (1988).
* D. R. Hofstadter, *Gödel, Escher, Bach* (1979): the crab canon and the endlessly rising canon.
* R. N. Shepard, "Circularity in judgments of relative pitch", *JASA* 36 (1964); Part 4 for Shepard tones.
* W. J. Dowling, "Recognition of melodic transformations: inversion, retrograde, and retrograde inversion",
  *Perception & Psychophysics* 12 (1972).
* M. Giraud, R. Groult, E. Leguy and F. Levé, "Computational fugue analysis", *Computer Music Journal* 39 (2015).
* D. Cope, *Experiments in Musical Intelligence* (1996); C.-Z. A. Huang and others, "Counterpoint by convolution",
  ISMIR (2017).
* Part 14 for the tunes; Part 16 for the rules of two voices; Part 17 for Viterbi search.

## Interpretation limits

The round test checks the overlaps produced by a chosen delay; three voices do not require every pair of sections to sound together. The exact canon counts and interval ranking apply only to the stated pitch range, rhythm and rules. They are not measures of Bach’s difficulty or complete historical style. The sampled harmony checker cannot establish that a passage is universally consonant or artistically successful.

The four-form table uses a fixed axis, or identifies sequences up to transposition when the axis follows the first note. Forty-eight row labels need not mean forty-eight distinct sequences for a symmetric row. Real and tonal answers require contextual musical judgment beyond this teaching heuristic. Bach’s tonal inversions can include chromatic adjustments. The cause of the unfinished final fugue and its intended continuation remain uncertain.
