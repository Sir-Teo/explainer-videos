# Music, Built: Part 38, Blues and Swing

Part 38 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth part of Act VI. "What is swing?" The proverbial answer is that if you have to
ask, you will never know; but it can be measured. This part builds the twelve-bar blues and its blue notes, the AAB
verse, ragtime (Joplin's *Maple Leaf Rag*, played from its score and counted), swing as a ratio that falls with tempo
and as late downbeats, the swing band's riffs, the walking bass and the ride cymbal, guide tones, ii–V–I, turnarounds
and the tritone substitution. The tools are Monochord's (`explainer/music/monochord/blues.py`): chord symbols, the
twelve-bar forms, a swing model, a walking-bass generator and a guide-tone solver (both shortest paths), tritone
substitutes and a syncopation count. *Maple Leaf Rag* (1899, in the public domain) is played from its encoding in the
music21 corpus; every other line, riff and verse is ours. Published findings are the ones listed under Sources.

* **If you have to ask.** An ear question (a swung line: how much longer is the long note?); the same line straight;
  swing can be measured; the plan.
* **1. The twelve-bar blues.** Where the blues came from; the form in C, three lines of four; one chorus, heard, with
  piano, walking bass, ride and hi-hat; the quick change and a jazz blues; the seventh as home; a shared map.
* **2. Blue notes.** An ear question (which third is neither minor nor major?); where blue notes live (third, fifth,
  seventh); a region, not a note; the blues scale and its limits; Kubik on where blue notes come from.
* **3. Call and response: the blues lyric.** An AAB verse of ours; the twelve bars with sung lines and guitar answers,
  heard; who answers; the singers; why AAB.
* **4. Ragtime and stride.** Joplin and ragtime; *Maple Leaf Rag*, bars 1–16, heard; bars 1–4 hand by hand, heard; the
  strain counted (right hand: 46 of 85 attack times between the eighths, 8 held across the next stronger position;
  left hand: 3 of 45 and 2); the march form; stride.
* **5. Swing, measured.** The model (3:1 at 120 beats a minute to 1:1 at 300) and the short note it implies (near
  100 ms above about 160); the ride pattern at 100, 180 and 260, heard; Friberg and Sundström, Benadon; late downbeats
  (Nelias and colleagues), a line on time and 30 ms late, heard; groove and participatory discrepancies.
* **6. The swing band.** The swing era; the sections; a riff chart of ours on the twelve-bar blues, heard; riffs and
  Kansas City; the arrangers.
* **7. Walking bass and the ride.** The rhythm section's jobs; the generator's four rules (root on each chord's first
  beat, a semitone approach before it, chord or scale tones between, no leap beyond a fifth; least total motion);
  two choruses of a jazz blues, heard; the line counted (all 15 changes approached by a semitone; 38 of 47 moves steps);
  the bassists.
* **8. Sevenths and guide tones.** Five seventh chords; guide tones through ii–V–I (F/C, F/B, E/B: 2 semitones in
  all); guide tones through ii–V–I and the jazz blues, heard; the jazz blues counted (32 semitones over 14 changes, no
  step above 3); voicings.
* **9. ii–V–I, turnarounds and the tritone substitution.** Two-five-one; an ear question (in which version does the
  bass slide by semitones?); G7 and D♭7 share F and B; a turnaround three ways, heard; bebop and after.
* **10. Frontier: microtiming and jazz corpora.** Prögler; Datseris and colleagues (2019); Nelias and colleagues
  (2022); a line on the grid and with random deviations, heard; the Weimar Jazz Database; ★ research problem: what makes
  a performance swing, and for whom?; credit and royalties.
* **Variation 38, recap and problems.** The Tune as a twelve-bar blues sung with thirds 35 cents below E, as a rag
  (its notes turned into short-long-short figures over an oom-pah left hand: 18 of 44 right-hand attacks syncopated),
  and as a riff chart (swung 2.7 to 1 at 150 beats a minute); the ledger; what we found; five problems; where it comes
  back; in practice; references; Part 39.

## What is computed, and what is heard

`python -m videos.music.music38.compute` (under a minute) fills `.cache/music38/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `swing`, `delay`, `jitter` | swung lines by the model; the ride pattern at three tempos; late and random timing | the model's formula (tests) |
| `form`, `blue`, `callresp` | the twelve-bar forms; one phrase with three thirds; an AAB verse | — |
| `rag` | *Maple Leaf Rag*, bars 1–16, from the encoding; attacks and syncopations by hand | hand counts (tests) |
| `band` | a riff chart | — |
| `walking` | the walking-bass generator over a jazz blues | its rules, in every key (tests) |
| `guide`, `subs` | guide tones by shortest path; ii–V–I with and without a tritone substitute; turnarounds | brute force (tests) |
| `tune`, `variation` | Variation 38 | — |

Monochord's tools are held in `tests/music/test_blues.py`; this part's claims and clips in
`tests/music/test_music38.py`.

**Sounds.** The piano is Part 7's struck string on a soundboard; bass and guitar are Part 35's retuned plucked string
through Part 7's body; the ride cymbal is a modal model with designed, dense treble modes and a stick's click; hi-hat
and snare are filtered noise with Part 9's membrane; the voice is Part 17's model (it sings vowels, not words); the
horns are additive (labelled `synthesized`). There are no recordings.

**What the models are, and are not.** *The swing model* is a straight line through a published trend, not a fit to
measured points; real swing varies by player, phrase and tempo. *The late-downbeat demonstration* uses 30 ms, a value of
ours, not the study's. *The walking bass* obeys four rules and nothing else: real lines vary rhythm and register and
surprise. *The horns* are additive tones, not models of saxophones or trumpets. *The blue third* is placed by us; sung
blue notes move. *The ensembles and verses* are ours.

## Build

```bash
python -m videos.music.music38.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music38 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music38 --sync                         # the sound gates
python tools/dead_air.py renders/music38_480p.mp4 --sound music38  # no empty screen; no sound over a still one
python tools/lecture_length.py music38                          # 30 to 60 minutes, listening included
python tools/build.py music38                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 38                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Using the model, compute the swing ratio and the short note's length at 140 and 240 beats a minute.

   *Solution.* r(140) = 3 − 2 × (140 − 120)/180 ≈ 2.78; a beat is 60/140 ≈ 0.429 s, so the short note is
   0.429/(1 + 2.78) ≈ 113 ms. r(240) = 3 − 2 × 120/180 ≈ 1.67; a beat is 0.25 s and the short note 0.25/2.67 ≈ 94 ms.
   The lab prints any tempo.

2. **Prove.** Prove that exactly two dominant seventh chords contain any given tritone.

   *Solution.* A dominant seventh on root r has pitch classes r, r + 4, r + 7, r + 10. Of its six pairs only one, (r + 4,
   r + 10), is six semitones apart, so each dominant seventh holds exactly one tritone, {r + 4, r + 10}. That equals a
   given tritone {a, a + 6} when r + 4 = a or r + 4 = a + 6, that is r = a − 4 or r = a + 2: two roots, a tritone apart.
   For {F, B}: G7 and D♭7.

3. **Ear.** The lab plays ii–V–I's, some with tritone substitutes; say which.

   *Solution.* The lab prints the answers. Listen to the bass: a substitute makes it slide down by semitones into the
   tonic; the plain progression falls a fifth and rises a fourth.

4. **Build.** Extend the walking-bass generator with skips and triplets, and keep its rules.

   *Where to look.* `blues.walking_bass` chooses one note a beat by dynamic programming. Add a second layer that may
   replace a beat with a swung triplet (a ghost note leading to the next beat) when the step allows a chromatic passing
   note, keep the root and approach rules on the beats, and check every chord still starts on its root.

5. ★ **What makes a performance swing, and for whom?**

   *Where the frontier is.* Take solos from a corpus such as the Weimar Jazz Database, resynthesise them with controlled
   changes to swing ratio, downbeat delay, dynamics and articulation, one at a time and together, ask listeners of
   different experience to rate swing, and model the ratings with uncertainty.

## Sources

* G. Kubik, *Africa and the Blues* (1999); P. Oliver, *The Story of the Blues* (1969).
* E. A. Berlin, *Ragtime: A Musical and Cultural History* (1980); S. Joplin, *School of Ragtime* (1908).
* G. Schuller, *Early Jazz* (1968) and *The Swing Era* (1989); P. F. Berliner, *Thinking in Jazz* (1994); M. Levine,
  *The Jazz Theory Book* (1995).
* A. Friberg and J. Sundström, "Swing ratios and ensemble timing in jazz performance: evidence for a common rhythmic
  pattern", *Music Perception* (2002); F. Benadon, "Slicing the beat: jazz eighth-notes as expressive microrhythm",
  *Ethnomusicology* (2006).
* C. Keil, "Participatory discrepancies and the power of music", *Cultural Anthropology* (1987); J. A. Prögler,
  "Searching for swing: participatory discrepancies in the jazz rhythm section", *Ethnomusicology* (1995).
* G. Datseris and others, "Does it swing? Microtiming deviations and swing feeling in jazz", *Scientific Reports*
  (2019); C. Nelias and others, "Downbeat delays are a key component of swing in jazz", *Communications Physics* (2022).
* M. Pfleiderer, K. Frieler, J. Abeßer, W.-G. Zaddach and B. Burkhart (eds.), *Inside the Jazzomat* (2017), on the
  Weimar Jazz Database.
* Part 13 for seventh chords; Part 18 for progressions; Part 32 for voice leading as distance; Part 37 for timelines.
