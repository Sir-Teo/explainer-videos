# Music, Built: Part 15, Key

Part 15 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the last part of Act II. Scales, chords and melody all turned out to lean on
one thing, a home note; this part is about that. It runs Krumhansl and Kessler's probe-tone experiment, shows that
a listener's ranking of the twelve notes matches how often they occur in music, gives the chords of a key their
three jobs and names the cadences, builds a key finder and scores it on the series' fifty-four tunes in all twelve
keys, asks which notes give a key away, maps the twenty-four keys, and follows music from one key to another. The
key module is Monochord's (`explainer/music/monochord/key.py`), the pictures are in `explainer/music/keyviz.py`,
and every sound is computed in `compute.py`. Published findings are the ones listed under Sources.

* **One tone, after four chords.** Four chords and then a tone with no octave, twice: one that fits (rated 6.35
  out of 7 by Krumhansl and Kessler's listeners) and one that does not (2.52); a key as an expectation for all
  twelve notes; the plan.
* **1. The note that fits.** The probe-tone method (1979, 1982) and the major profile; its four levels: the
  tonic, the rest of its triad, the rest of the scale, the five notes outside; the minor profile; an ear question
  (three probes).
* **2. Where the ranking comes from.** The time on each note in the 54 tunes against the ratings: r = 0.92;
  Castellano, Bharucha and Krumhansl (1984): newcomers to Indian music rate by what they have just heard;
  Trainor and Trehub (1992, 1994): infants hear in-key and out-of-key changes alike, adults miss the in-key
  ones, children acquire key membership by five and harmony by seven.
* **3. Three jobs.** The seven triads sorted by the resting and leaning notes they hold: the chords on four and
  five carry every leaning note; Riemann's tonic, predominant and dominant (1893); three progressions, heard
  (I–IV–V–I, I–ii–V7–I, I–V–IV–I); each degree belongs to three triads; the Tune alone and then harmonized by
  function, heard.
* **4. Four endings.** Authentic, half, plagal and deceptive cadences, heard; one authentic cadence with the
  melody ending on the first degree and on the third (perfect and imperfect), heard; an ear question (which is
  deceptive, in another key).
* **5. Finding the key.** The Krumhansl–Schmuckler algorithm: correlate the notes with 24 profiles; a
  probabilistic key finder listening to the Tune note by note, heard: after nine notes it believes F major (58
  in a hundred), and it is sure of C major only after eleven.
* **6. How well, and how fast.** 648 tests (54 tunes, 12 keys): the listeners' ratings 81 in a hundred, a
  probabilistic finder 96, profiles counted from music 98, "the first note" 33, "the last note" 91; the mistakes:
  72 of 120 name the key a fifth above, 36 the minor key on the third degree; profiles learnt from 53 tunes and
  tested on the other: 94; by number of notes: five are enough for 91.
* **7. Which notes tell.** Major scales containing C and G: six; C, D, E: three; a predict-pause (B and F: two;
  with C: one); the rarest interval is the best clue (Browne 1981); the Tune's six notes belong to C major and F
  major alike: a key is weights, not membership.
* **8. A map of keys.** The circle of fifths (Heinichen 1728): 6, 5, 4, 3, 2, 2 notes shared; key signatures as
  addresses, the order of sharps and of flats; closeness as the correlation of profiles: A minor 0.65, G and F
  0.59, F♯ −0.68; one cadence moved to G major, A minor and F♯ major, heard; the 24 keys on Krumhansl and
  Kessler's torus, computed by multidimensional scaling.
* **9. Leaving home.** The dominant of the dominant; pivot chords; triads shared by keys one, two and three
  fifths apart: 4, 2 and 0; an ear question: a tonicization and a modulation; the key finder's reading of both.
* **10. Minor, and neither.** One phrase in C major, C minor (four notes shared, the same home) and A minor
  (seven shared, another home), heard; the minor key's borrowed dominant, heard; a Dorian tune that the key
  finder misreads, and pentatonic tunes that it reads correctly.
* **11. Does it matter which key?** One cadence in C and in D♭, heard: in equal temperament every key is the
  same key, moved; Levitin (1994): people sing remembered songs near their recorded key; Werckmeister's
  temperament: the third on C is 390 cents, on F♯ 408: where the characters of keys came from.
* **12. Frontier: is a key learned?** Tonal hierarchies in north India, Bali and Sami yoiks; major and minor
  condensing out of the modes between 1400 and 1750 (Albrecht and Huron 2014); rock harmony (de Clercq and
  Temperley 2011). ★ research problem: what a listener stores.
* **Variation 15, recap and problems.** The Tune through all twelve keys, a fifth lower each phrase, each home
  chord turned into the next key's dominant seventh, ending on a deceptive cadence, with the key finder naming
  every key; the ledger; what we found; five problems; where it comes back; in practice; references; Act III.

## What is computed, and what is heard

`python -m videos.music.music15.compute` (under a minute) fills `.cache/music15/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `profile` | contexts and probes; the published profiles; the corpus's own | the ratings are Krumhansl and Kessler's (1982), as printed in Krumhansl (1990) |
| `functions` | resting and leaning notes in each triad; three progressions | Part 14's degree transitions |
| `cadences` | four cadences, voiced by least motion | — |
| `meter` | the posterior over 24 keys after each note of the Tune | — |
| `finder` | five key finders on 648 cases; accuracy by number of notes; leave-one-out profiles | — |
| `rare` | major scales containing sets of notes | the interval vector ⟨2, 5, 4, 3, 6, 1⟩ |
| `keymap` | correlations between key profiles; the torus by classical scaling | Krumhansl and Kessler's table: 0.651, 0.591, 0.536, 0.511, −0.683 |
| `modulate` | a tonicization and a modulation; a three-chord key tracker | — |
| `minor` | one phrase in three keys; five tunes the finder may misread | — |
| `more` | harmonization; two authentic cadences; near misses; shared triads; the minor dominant; Werckmeister's thirds | Part 6's tuning tables |
| `tune` | Variation 15 | the key finder names 14 of 14 phrases |

Monochord's keys are held against these in `tests/music/test_key.py`; this part's claims and clips in
`tests/music/test_music15.py`.

**Sounds.** Fourteen clips, on Part 7's piano (`physical model`) in twelve-tone equal temperament; the probe
tones are Shepard tones (partials in every octave under a fixed envelope), as in the experiments. There are no
recordings.

**What the models are, and are not.** *The profiles* are averages over the listeners of one laboratory in 1982
(and of Temperley's counts from the examples of one harmony textbook); they are not constants of nature, and the
film says so. *The corpus* is Part 14's fifty-four tunes, nearly all in major keys and nearly all European or
American: "r = 0.92" is a statement about those tunes. *The key finders* see pitch classes and durations only:
no chords, no order, no metre; the probabilistic one is the simplest form of Temperley's, a multinomial over
notes with a flat prior over keys. Scores on 648 "tests" count each tune twelve times, once in each key, so they
measure 54 tunes, not 648. The *Well-Tempered Clavier*, on which the syllabus meant to score the key finder,
was not available to this build (no score files or libraries offline). *Function* is presented as Riemann's
three categories read off the leaning notes of Part 14; other accounts (scale-degree theory, Schenker's) carve
harmony differently. *The torus* is a four-dimensional classical scaling of profile correlations; it holds 82%
of the variance, not all of it. *The key tracker* of chapter 9 uses a window of three chords. *Werckmeister III*
is one of many unequal temperaments. The curve in the frontier chapter is a sketch of a published finding, not
data of ours.

## Build

```bash
python -m videos.music.music15.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music15 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music15 --sync                         # the sound gates
python tools/dead_air.py renders/music15_480p.mp4 --sound music15  # no empty screen; no sound over a still one
python tools/lecture_length.py music15                          # 30 to 60 minutes, listening included
python tools/build.py music15                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 15                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Signatures and relations.** Name the key with four sharps and its relative minor; the key with three flats
   and its parallel minor. How many notes does each pair share, and how many steps apart are E major and E♭
   major on the circle of fifths?

   *Solution.* Four sharps (F♯, C♯, G♯, D♯) is E major, four steps clockwise from C; its relative minor is C♯
   minor, a minor third below, with the same seven notes. Three flats (B♭, E♭, A♭) is E♭ major; its parallel
   minor, E♭ minor, has six flats and shares four notes with it (E♭, F, A♭, B♭). E major and E♭ major are a
   semitone apart as notes and five steps apart on the circle (four sharps to three flats is seven steps one
   way, five the other): they share only two notes, G♯/A♭ and D♯/E♭.

2. **Rare intervals.** A major scale's interval vector is ⟨2, 5, 4, 3, 6, 1⟩. Prove that a pair of notes forming
   interval class k lies in exactly v_k major scales (twice that for the tritone), and so explain why the tritone
   is the best clue to a key.

   *Solution.* Fix an interval class k between 1 and 5, and a pair of notes x, x + k. A major scale on tonic t
   contains the pair exactly when the pair (x − t, x − t + k) is one of the v_k places where that interval
   occurs in the scale on 0. Each of those v_k places gives one value of t, and different places give different
   t, so there are v_k scales. For the tritone, the pair {x, x + 6} is the same set as {x + 6, x + 12}: each of
   the scale's v_6 = 1 tritones can be matched to the pair in two ways, giving two scales (C and F♯ for B–F).
   So a fifth lies in six scales and tells you little; a semitone or a tritone lies in two. And of those, the
   tritone's two scales are as far apart as keys can be, so a single further note decides.

3. **Ear.** The lab plays eight short progressions. Name each cadence: authentic, half, plagal or deceptive.

   *Solution.* The lab prints the answers. Listen to the bass. Falling a fifth (or rising a fourth) to a chord
   that sounds like home: authentic. Stopping on a chord that wants to go on: half. The bass falling a fourth
   to home, without a leading note: plagal. The bass stepping up one note where it should have fallen a fifth,
   onto a minor chord: deceptive.

4. **Build.** With `key.learn_profiles`, count profiles from the corpus and use them in `key.bayes_key`. Test
   each tune with profiles learnt from the others. Which tunes are still misread, and what do they have in
   common?

   *Solution.* The lab does this: 612 of 648, or 94 in a hundred. With C as home, three major tunes are read as
   minor: *We Wish You a Merry Christmas* and *Aura Lee* as A minor, *Alle meine Entchen* as D minor. All three
   spend an unusual share of their time on the sixth or second degree (long or repeated As and Ds) and little
   on the fifth, so their note counts look like the relative or supertonic minor. (The three minor tunes are all
   read correctly.) Nothing in a count of notes says which note the tune ends on, which would have settled all
   three.

5. ★ **Counts or grammar?** Design an experiment to tell whether listeners store a key as counts of notes or as
   a grammar of chords. What would each account predict for a passage with the right notes in the wrong order?

   *Where the frontier is.* A count model predicts that scrambling the order of a passage leaves its key, and
   the probe-tone ratings after it, unchanged; a grammar predicts weaker or different ratings. The evidence is
   mixed. West and Fryer (1990) and later Smith and Schmuckler (2004) found that random orderings of the right
   notes in the right proportions still produce the standard profile, which favours counts. But Butler (1989)
   and Brown, Butler and Jones (1994) showed that the *order* of the same few notes changes which tonic
   listeners choose (the tritone resolving one way or the other), and priming studies of chords (Bharucha and
   Stoeckig 1986; Tillmann and others 2000) show expectations for what comes next that no table of counts
   contains. Current models (Temperley 2007; Harrison and Pearce 2020 for harmony) combine both; which carries
   how much, and whether the answer differs by musical culture, is open.

## Sources

Books: C. L. Krumhansl, *Cognitive Foundations of Musical Pitch* (1990); D. Temperley, *The Cognition of Basic
Musical Structures* (2001) and *Music and Probability* (2007); F. Lerdahl, *Tonal Pitch Space* (2001); H.
Riemann, *Vereinfachte Harmonielehre* (1893); J. D. Heinichen, *Der General-Bass in der Composition* (1728);
G. Weber, *Versuch einer geordneten Theorie der Tonsetzkunst* (1817–21); S. Laitz, *The Complete Musician* (4th
ed., 2015), chs. 7–12.

Papers: C. L. Krumhansl and R. N. Shepard, "Quantification of the hierarchy of tonal functions within a diatonic
context", *Journal of Experimental Psychology: Human Perception and Performance* 5 (1979); C. L. Krumhansl and
E. J. Kessler, "Tracing the dynamic changes in perceived tonal organization in a spatial representation of
musical keys", *Psychological Review* 89 (1982); R. Browne, "Tonal implications of the diatonic set", *In Theory
Only* 5 (1981); M. A. Castellano, J. J. Bharucha and C. L. Krumhansl, "Tonal hierarchies in the music of North
India", *Journal of Experimental Psychology: General* 113 (1984); E. J. Kessler, C. Hansen and R. N. Shepard,
"Tonal schemata in the perception of music in Bali and in the West", *Music Perception* 2 (1984); L. J. Trainor
and S. E. Trehub, "A comparison of infants' and adults' sensitivity to Western musical structure", *JEP: HPP* 18
(1992), and "Key membership and implied harmony in Western tonal music: developmental perspectives", *Perception
& Psychophysics* 56 (1994); D. J. Levitin, "Absolute memory for musical pitch: evidence from the production of
learned melodies", *Perception & Psychophysics* 56 (1994); C. L. Krumhansl, P. Toivanen, T. Eerola, P.
Toiviainen, T. Järvinen and J. Louhivuori, "Cross-cultural music cognition: cognitive methodology applied to
North Sami yoiks", *Cognition* 76 (2000); T. de Clercq and D. Temperley, "A corpus analysis of rock harmony",
*Popular Music* 30 (2011); J. Albrecht and D. Huron, "A statistical approach to tracing the historical
development of major and minor pitch distributions, 1400–1750", *Music Perception* 31 (2014).
