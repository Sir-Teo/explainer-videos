# Music, Built: Part 17, Four Voices

Part 17 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act III. Part 16 kept two voices apart; here there are four,
and every moment is also a chord. The part takes 364 of Bach's four-part chorales as data, measures where each
voice sings and how it moves, states the rules of four-part writing and counts how often Bach breaks them, looks
at his chords, cadences and passing notes, and builds a harmonizer, a search over chords and voicings together,
which it judges against Bach on tunes the harmonizer has never seen. The chorales are Monochord's table
(`explainer/music/monochord/chorales.py`), the rules and the harmonizer are `explainer/music/monochord/fourpart.py`,
the choir is `explainer/music/monochord/instruments/choir.py`, and every sound is computed in `compute.py`.
Published findings are the ones listed under Sources.

* **One tune, two harmonizers.** The St Matthew Passion (1727) and Hassler's tune of 1601, sung five times in it;
  its last setting's first two phrases, alone, as Bach set them, and as a chord-chooser sets them (Bach's commonest
  chords under each note, nothing else): six parallel fifths or octaves in fifteen moves, and inner voices that
  hardly move; the plan.
* **1. A book of chorales.** C. P. E. Bach's edition (Breitkopf, 1784–87, 371 chorales); the data: 364 chorales,
  185 in major and 178 in minor, 84,737 notes, 230 different tunes, 59 set more than once, the Passion Chorale
  eleven times; its first phrase the first and the last time it is sung in the Passion, heard.
* **2. Four ranges.** Where each voice sings, against the textbook ranges (C4–A5, G3–D5, C3–A4, E2–D4): outside
  them, five soprano notes in a hundred thousand and 0.76 bass notes in a hundred; spacing: soprano to alto 5.3
  semitones on average, alto to tenor 5.8, tenor to bass 8.7, more than an octave 0.3, 0.9 and 19 times in a
  hundred; doubling: in root position the root 87 times in a hundred, with the third in the bass root, third and
  fifth about a third each.
* **3. Every voice a line.** Mean moves 1.9, 1.7, 2.0 and 3.1 semitones (soprano to bass); steps 85, 84, 81 and 66
  in a hundred; the alto alone, heard; the law of the shortest way (Bruckner, after Sechter): Bach's alto and
  tenor move 3.6 semitones a beat where 2.4 would do, take the very shortest way 68 times in a hundred and come
  within two semitones of it 80.
* **4. The rules for four.** Four families; four rules each heard as two chords wrong and right: parallel fifths
  and octaves between any of six pairs; the leading note rises; a seventh falls; the upper voices within an octave.
* **5. How often Bach breaks them.** At 29,326 changes of chord, 52 parallel fifths and 23 octaves: once in 391,
  about once in five chorales; by pair (soprano and tenor the most); 51 of 75 between the beats, through a passing
  note; two on the beat, heard; contrary fifths and octaves 85, hidden 157, overlaps 1,735 (one move in 17),
  crossings 2.5 chords in a hundred: rules obeyed between 94 and 99.7 times in a hundred.
* **6. Chords on the beat.** Labels as Roman numerals (nine beats in a hundred carry no chord); in major I, V, vi,
  IV, ii, then II (the dominant's dominant); in minor i, then III, iv, V; what follows what; the same chord on the
  next beat 23 times in a hundred.
* **7. Where phrases end.** At 1,216 fermatas in major: V–I 246, II–V 114, V7–I 80; in minor V–i 107, VII–III 98
  (a cadence in the relative major); three cadences heard; 104 of 176 minor chorales end on a major chord (the
  Picardy third), 11 on the minor one.
* **8. Between the beats.** Notes that begin between beats, by voice and kind: passing notes the majority in every
  voice, the bass with the most, the soprano the fewest; 55 beats in a hundred have something moving inside them;
  an ear question (Bach's chords as blocks, and as he wrote them).
* **9. Harmonizing as search.** The problem; the lattice for the hook's sixteen beats (192 to 446 chord-and-voicing
  pairs a beat, about 10⁴⁰ paths); the Viterbi algorithm (0.4 s); the cost terms and where each comes from; the
  hook harmonized: the same chord as Bach on 8 of 16 beats, no parallels, and a major chord at a phrase's end where
  Bach stays minor.
* **10. Ours against Bach.** A split by tune (280 chorales to learn from, 83 to test, 4,438 beats, no test tune in
  training in any setting); the same chord as Bach 42 times in a hundred (the chord-chooser 41), the same bass 40
  (24); parallel fifths and octaves: the chord-chooser 769, Bach 77, the search 0; inner-voice motion 1.7
  semitones a beat against Bach's 3.5; an ear question (ours or Bach's).
* **11. Where we lose.** What the search does not know (a plan, the end of a piece, notes between beats, lines,
  words); passing notes added by rule, heard; notes a beat in the lower voices: 0.69, 0.74 with the rule, Bach
  1.13.
* **12. Frontier: machines that write chorales.** CHORAL (Ebcioğlu 1988), Allan and Williams's hidden Markov model
  (2005), BachBot (2016), DeepBach and Coconet (2017), the Bach Doodle (2019); four ways to judge a style, each
  flawed. ★ research problem: what is a style, in numbers?
* **Variation 17, recap and problems.** The Tune as a chorale, with a pause at each phrase end: chosen chord by
  chord (six parallel fifths or octaves), then corrected by the full search (none); the ledger; what we found; five
  problems; where it comes back; in practice; references; Part 18.

## What is computed, and what is heard

`python -m videos.music.music17.compute` (about five minutes) fills `.cache/music17/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | the Passion Chorale's first two phrases: Bach's, the chord-chooser's, the search's | `fourpart.parallels` |
| `book` | the collection: modes, metres, notes, tunes, settings | the table's tests |
| `ranges` | ranges, spacing, doubling | the textbook ranges |
| `motion` | moves by voice; the shortest way for alto and tenor | — |
| `rules` | four rules, wrong and right | `parallels`, `spacing_ok` |
| `census` | every parallel, hidden interval, overlap, crossing in the chorales | — |
| `vocab` | chord frequencies and transitions on the beat | — |
| `cadences` | chords at the fermatas; final chords | — |
| `decoration` | notes between the beats, by voice and kind | — |
| `harmonizer` | the lattice under the hook; the search's answer | — |
| `evaluation` | the search and the chord-chooser on 83 held-out chorales | split by tune (`chorales.split`) |
| `improve` | passing notes added by rule | — |
| `tune` | Variation 17 | no parallels after correction |

Monochord's chorales, rules, harmonizer and choir are held in `tests/music/test_fourpart.py`; this part's claims
and clips in `tests/music/test_music17.py`.

**Sounds.** The chorales are sung by a model choir: Part 8's source-filter voice (Rosenberg pulses through the
formants of the vowel "ah", scaled for each part), one continuous voice for each part, legato, with a little
vibrato (`synthesized`); the rules are heard on organ tones. Equal temperament, with a pause at each fermata. There
are no recordings.

**What the models are, and are not.** *The data* are 364 encodings from the music21 corpus, not a critical edition;
a few have parts in unusual ranges or modes mislabelled as major or minor, and nothing here was corrected by hand.
*Chord labels* are the plainest triad or seventh chord that fits the four notes sounding on a beat; a passing note
on the beat can make a beat unlabelled or mislabelled, and inversions and sevenths are counted with their chords
only where stated. *The rules* are textbook rules made exact (parallels need both voices to move; hidden fifths are
outer voices only); other definitions give other counts. *The harmonizer* is a first-order model, one chord a beat,
with hand-set penalties whose weights were tuned on a validation split of the training chorales; it does not
write notes between the beats (except by the rule of chapter 11) and does not see phrase structure. *Agreement with
Bach* is not a measure of quality: chapter 1 shows that Bach sets one tune several ways. The choir is a model, not
singers.

## Build

```bash
python -m videos.music.music17.compute                          # numbers and sounds (about five minutes)
EXPLAINER_TTS=silent python tools/build.py music17 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music17 --sync                         # the sound gates
python tools/dead_air.py renders/music17_480p.mp4 --sound music17  # no empty screen; no sound over a still one
python tools/lecture_length.py music17                          # 30 to 60 minutes, listening included
python tools/build.py music17                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 17                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** Harmonize the Tune's first phrase, C C G G A A G, one chord to a note, using only I, IV and V. How
   many choices of chords are there, before voicing?

   *Solution.* C lies in I and IV (C E G, F A C); G in I and V (C E G, G B D); A only in IV. So the choices are
   2 × 2 × 2 × 2 × 1 × 1 × 2 = 32. A sensible one, I I I I IV IV I (or V at the last G), avoids repeating the
   same chord across the A–A–G and ends the phrase on a chord that holds the G; the plain and full harmonizers
   of Variation 17 both choose I I I I IV IV I.

2. **Prove.** Show that if every voice moves to the nearest note of the next chord, two voices can still make
   parallel fifths. Give the smallest example, and the rule that prevents it.

   *Solution.* Take C major root position with the soprano on G and the tenor on C (a fifth), moving to D minor:
   the nearest note to G in D minor is A, and to C it is D, so both voices rise a step, still a fifth apart:
   parallel fifths, each voice having moved as little as possible. The shortest way is a rule about each voice
   alone; parallels are about pairs, so a separate rule (and in the harmonizer, a separate penalty) is needed.
   Moving the upper voices down, against the bass (G to F, E to D, C to A over C to D), costs a little more
   motion and has no parallels.

3. **Ear.** The lab plays eight short cadences from the chorales. Name each: authentic, half, or ending on a major
   chord in a minor key.

   *Solution.* The lab prints the answers. An authentic cadence lands on a chord that sounds like home, the bass
   falling a fifth (or rising a fourth) into it. A half cadence stops on a chord that wants to go on, usually
   with a bass that has risen by step to it. The Picardy ending is a minor passage whose last chord is suddenly
   brighter: listen to the top of the final chord.

4. **Build.** Change the harmonizer's chord model to look two chords back instead of one. Does it find Bach's chord
   more often on the test chorales? Why might it not?

   *Where to look.* `fourpart.ChordModel` counts pairs; a model of triples needs the state of the Viterbi search
   to be a pair of chords, which squares its size. With 280 chorales and about 25 chords in each mode, most
   triples are seen a few times or never, so the estimates are noisy and smoothing dominates; the gain, if any, is
   small unless the counts are pooled (by function, or by backing off to pairs). Bach's agreement with himself
   across settings of one tune sets a ceiling well below 100 in a hundred.

5. ★ **A fair listening test.** Design a listening test that could show a machine's chorales are as good as
   Bach's. What would a fair test control for?

   *Where the frontier is.* The published tests (BachBot's, DeepBach's) asked listeners whether a short excerpt
   was Bach. A fair test controls the excerpt's length (short excerpts hide planning), the tune (machine and Bach
   on the same held-out tune), the performance (the same synthesis for both, or the same singers), the listeners'
   training (report results by expertise), and the question (preference, or attribution, or a teacher's grade).
   It should also include Bach against Bach, two settings of one tune, to measure how often listeners call real
   Bach machine-made. No standard test exists.

## Sources

Books: J. S. Bach, *371 vierstimmige Choralgesänge*, ed. C. P. E. Bach (Breitkopf, 1784–87); E. Aldwell and
C. Schachter, *Harmony and Voice Leading* (4th ed., 2011); S. Kostka and D. Payne, *Tonal Harmony* (8th ed., 2018);
D. Huron, *Voice Leading: The Science behind a Musical Art* (2016); S. Sechter, *Die Grundsätze der musikalischen
Komposition* (1853–54).

Papers: K. Ebcioğlu, "An expert system for harmonizing four-part chorales", *Computer Music Journal* 12 (1988);
M. Allan and C. K. I. Williams, "Harmonising chorales by probabilistic inference", *Advances in Neural Information
Processing Systems* 17 (2005); F. Liang, *BachBot: Automatic composition in the style of Bach chorales*, MPhil
thesis, Cambridge (2016); G. Hadjeres, F. Pachet and F. Nielsen, "DeepBach: a steerable model for Bach chorales
generation", *ICML* (2017); C.-Z. A. Huang, T. Cooijmans, A. Roberts, A. Courville and D. Eck, "Counterpoint by
convolution", *ISMIR* (2017); C.-Z. A. Huang and others, "The Bach Doodle: approachable music composition with
machine learning at scale", *ISMIR* (2019); M. S. Cuthbert and C. Ariza, "music21: a toolkit for computer-aided
musicology and symbolic music data", *ISMIR* (2010).
