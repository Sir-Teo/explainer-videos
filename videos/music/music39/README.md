# Music, Built: Part 39, Changes

Part 39 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth part of Act VI. 5 May 1959: John Coltrane records *Giant Steps*, twenty-six
chords in sixteen bars, moving through three keys a major third apart at nearly 290 beats a minute. This part explains
why those changes are hard, draws them on Part 31's Tonnetz, and builds an improviser. On the way: bebop and the
contrafact, the bebop scale (with a proof), targets, enclosures and formulas, chord scales and avoid notes, modal jazz and
quartal voicings, reharmonisation, free jazz, and what improvisers are doing. The tools are Monochord's
(`explainer/music/monochord/changes.py`, with Part 38's `blues.py`). Well-known tunes appear only as their chord
progressions, as lead sheets give them; no melody of theirs is played. Every line heard is ours or the program's.
Published findings are the ones listed under Sources.

* **Twenty-six chords in sixteen bars.** An ear question (Giant Steps' changes, comped: how many keys?); the same changes
  at 286 beats a minute with the improviser; 5 May 1959; the plan.
* **1. Bebop and the contrafact.** Minton's and the founders; contrafacts and rhythm changes; the A section of rhythm
  changes with a head and a chorus by the program, heard; the players; a shared language.
* **2. The bebop scale.** The problem; sixteen eighths down over C7 (mixolydian: 5 of 8 beats on chord tones; bebop
  scale: 8 of 8); both heard; why it works (chord tones at every other position of an eight-note cycle), checked for every
  chord tone and direction (the plain mode averages 64%); a general trick; teaching it.
* **3. Enclosures and formulas.** Targets and guide tones; three ways to reach E; the three heard; Owens's and Norgaard's
  formulas; one figure of ours in C, F and B♭, heard; vocabulary.
* **4. Chord scales.** The idea; five chords on C with their scales and avoid notes; the five heard; an ear question (which
  held note clashes over Cmaj7?); Russell and Berklee; a critique.
* **5. Modal jazz and quartal voicings.** *Kind of Blue*; *So What*'s 32 bars and two chords; a voicing in fourths; a
  modal vamp of ours with the improviser, heard; after *Kind of Blue*.
* **6. Third cycles.** The tonics on the pitch-class circle (an augmented triad of keys); the tonic triads in a line on the
  Tonnetz; keys a fifth apart share six notes, a major third apart three; Coltrane's substitute for ii–V–I; both heard
  with the improviser; a cycle with a history.
* **7. Reharmonisation.** The rule; a phrase of ours harmonised diatonically, with secondary dominants and with tritone
  substitutes; the three heard; the art of it.
* **8. An improviser.** A phrase grammar in five steps; an ear question (improviser or random line?); judged over fifty
  choruses (chord tones on 90% of beats against 57% and 34%; guide tones at 91% of changes against 28% and 13%); what it
  lacks.
* **9. Free jazz, and what improvisers do.** Ornette Coleman; after 1959; a toy free duo that answers, heard; Pressing's
  model; Johnson-Laird on real time; a conversation.
* **10. Frontier: patterns, machines and the scanner.** Pattern mining; machine improvisers; improvising in the scanner;
  ★ research problem: how much of a solo is recalled, and how much invented?
* **Variation 39, recap and problems.** The Tune as a bebop head (each note enclosed), a chorus by the program over its
  changes (86% of beats on chord tones, guide tones at 96% of changes), then its opening carried through C, A♭ and E over
  Coltrane's cycle; the ledger; what we found; five problems; where it comes back; in practice; references; Part 40.

## What is computed, and what is heard

`python -m videos.music.music39.compute` (under a minute) fills `.cache/music39/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `fast` | Giant Steps' changes comped; the improviser over them at 286 | 26 chords, three tonics (tests) |
| `contrafact`, `formula` | rhythm changes with the program's lines; a figure in three keys | — |
| `bebop` | the bebop-scale claim, every chord tone and direction | exhaustive check (tests) |
| `scales`, `avoid` | five chord scales and their avoid notes | the semitone rule (tests) |
| `modal`, `thirds` | a modal vamp; Coltrane's substitute; key centres | shared notes, all twelve keys (tests) |
| `reharm` | three harmonisations of a phrase | the melody stays a chord tone or tension (tests) |
| `improv`, `echo` | the improviser against random lines; a toy duo that answers | the baselines (tests) |
| `tune`, `variation` | Variation 39 | — |

Monochord's tools are held in `tests/music/test_changes.py`; this part's claims and clips in
`tests/music/test_music39.py`.

**Sounds.** Part 38's instruments: Part 7's piano; the retuned plucked string for bass; a modal ride cymbal and a noise
hi-hat; additive horns (labelled `synthesized`). There are no recordings.

**What the models are, and are not.** *The improviser* chooses each half-bar's figure by dice, aims at guide tones, and
never listens; its measures reward safe choices. *The baselines* are deliberately simple. *The reharmoniser* follows one
rule per scheme. *The voicings* are guide tones and one quartal shape. *The free duo* is a toy, not a model of free jazz.

## Build

```bash
python -m videos.music.music39.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music39 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music39 --sync                         # the sound gates
python tools/dead_air.py renders/music39_480p.mp4 --sound music39  # no empty screen; no sound over a still one
python tools/lecture_length.py music39                          # 30 to 60 minutes, listening included
python tools/build.py music39                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 39                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** For F7, list the bebop scale and check that a run down from E♭ lands chord tones on every beat for two
   octaves.

   *Solution.* F G A B♭ C D E♭ E. Down from E♭ in eighths: E♭ D C B♭ A G F E | E♭ D C ...; the notes on the beats are E♭, C,
   A, F, E♭, C, A, F, all chord tones of F7 (F A C E♭). The lab checks any chord.

2. **Prove.** Prove that two major scales a major third apart share exactly three notes.

   *Solution.* By transposition it is enough to compare C major {0, 2, 4, 5, 7, 9, 11} with E major {4, 6, 8, 9, 11, 1,
   3}: the common notes are 4, 9 and 11 (E, A, B), three. (A fifth apart, C and G share all but F and F♯: six.)

3. **Ear.** The lab plays lines by the improviser and by random choice; say which is which.

   *Solution.* The lab prints the answers. Listen for phrasing (the improviser rests) and for arrival: at each chord
   change the improviser lands on the third or seventh of the new chord.

4. **Build.** Give the improviser motifs: repeat and transpose its own figures, and judge the result.

   *Where to look.* In `changes.improvise`, keep the last few figures; with some probability, reuse one transposed so that
   its first note is a chord tone of the current chord. Judge with `changes.judge`, and add a measure of repetition
   (the share of figures that recur, as in pattern mining) to see the trade-off.

5. ★ **How much of an improvised solo is recalled, and how much invented?**

   *Where the frontier is.* Collect solos with recordings, transcriptions and the players' commentary; model each note as
   a recalled pattern or a local choice; fit the mixture per player; test it on new solos and against players' reports.

## Sources

* T. Owens, *Charlie Parker: Techniques of Improvisation* (dissertation, 1974) and *Bebop: The Music and Its Players*
  (1995); P. F. Berliner, *Thinking in Jazz* (1994); I. Monson, *Saying Something* (1996).
* M. Levine, *The Jazz Theory Book* (1995); G. Russell, *The Lydian Chromatic Concept of Tonal Organization* (1953);
  N. Slonimsky, *Thesaurus of Scales and Melodic Patterns* (1947).
* L. Porter, *John Coltrane: His Life and Music* (1998); A. Kahn, *Kind of Blue: The Making of the Miles Davis
  Masterpiece* (2000).
* J. Pressing, "Improvisation: methods and models", in J. Sloboda (ed.), *Generative Processes in Music* (1988);
  P. N. Johnson-Laird, "How jazz musicians improvise", *Music Perception* (2002); M. Norgaard, "How jazz musicians
  improvise: the central role of auditory and motor patterns", *Music Perception* (2014).
* C. J. Limb and A. R. Braun, "Neural substrates of spontaneous musical performance: an fMRI study of jazz
  improvisation", *PLoS ONE* (2008); G. F. Donnay and others, "Neural substrates of interactive musical improvisation:
  an fMRI study of 'trading fours' in jazz", *PLoS ONE* (2014).
* J. A. Biles, "GenJam: a genetic algorithm for generating jazz solos" (1994); F. Pachet, "The Continuator: musical
  interaction with style", *Journal of New Music Research* (2003).
* Part 18 for progressions; Part 31 for the Tonnetz; Part 38 for swing, guide tones and the tritone substitution.

## Interpretation limits

Contrafacts and shared changes do not establish a blanket rights exemption. The 1942–44 recording ban limited studio documentation; earlier live recordings survive. An even-length scale can alternate chord tones only when its pitch ordering actually interleaves them, as in the chosen examples. Avoid-note labels are a voicing heuristic, not universal perceptual laws. Quartal spacing can still contain thirds and express a clear mode. Fifty generated choruses compare designed descriptors against simple baselines, not listener quality; scale-only output has higher scale adherence. The response toy exchanges symbolic notes rather than listening to audio.
