# Music, Built: Part 14, Melody

Part 14 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). Part 13 stacked notes into chords; this part puts them in a line. It asks, of
each thing melodies are said to do, whether they do it, and whether any string of notes in a small range would do
it anyway. It counts the moves, ranges and phrase shapes of fifty-four tunes that half the world can sing; shows
that the old rule "after a leap, turn back" is obeyed more faithfully by shuffled notes than by real tunes, and
why; finds what chance does not explain (tendency tones, momentum, repetition, phrases that ask and answer);
measures the information in a note; and trains a model that is surprised by the Tune exactly where a listener is.
The melody module is Monochord's (`explainer/music/monochord/melody.py`), the corpus is
`explainer/music/monochord/tunes.py`, the pictures are in `explainer/music/melodyviz.py`, and every sound is
computed in `compute.py`. Published findings are the ones listed under Sources.

* **A rule that noise obeys.** "After a leap, turn back": in 54 tunes there are 446 leaps of a minor third or
  more, and 63 in a hundred are followed by a turn back; the Tune and the same fourteen notes shuffled, heard; in
  shuffled tunes the figure is 79; the plan.
* **1. The shape of a tune.** An ear question: one famous tune with its octaves scrambled (every note right, the
  shape gone) and with its intervals doubled (every note wrong, the shape kept); contour first, then intervals,
  then rhythm (Deutsch 1972; Dowling 1978); the Tune on C and on F♯: no note in common, the same tune; Parsons's
  code of ups, downs and repeats: eight moves tell all 54 tunes apart.
* **2. Small steps.** 1,844 moves: half steps, a quarter repeats, a quarter leaps; mean two semitones; 99 in a
  hundred within a fifth; steps mostly fall (396 whole tones down, 313 up), fourths mostly rise (63 to 37); why:
  the voice, and the ear: a gallop that splits into two streams when its middle note is far away (heard); an ear
  question: notes drawn at random against moves drawn at random.
* **3. Room to sing.** Ranges: the median is an octave; 42 of 54 fit in one; Hot Cross Buns and the opening of
  The Star-Spangled Banner, heard; notes crowd the middle of a tune's range: 59 in a hundred within a tone or so
  of its median, the top note one note in eleven.
* **4. The arch.** Two phrases of the Ode to Joy, heard; 275 phrases sorted by shape: falling 87, arch 79, rising
  60, valley 36; their average is an arch that ends half a semitone below where it began (Huron 1996); speech
  does the same; where a tune's highest note first arrives: a quarter of the way through in the median, not two
  thirds.
* **5. The rule that chance obeys.** Twenty-four notes from an urn, heard; a leap away from the middle lands
  near an edge, and most of the urn lies back the way it came: regression to the mean; a die: after a rise of two
  or more, the next roll falls in 40 of 60 cases and rises in 10; a predict-pause (a leap toward the middle);
  by where the leap lands: away from the middle 75 in a hundred turn back (shuffled: 95), across it 78 (87),
  toward it 20 (22) (von Hippel and Huron 2000); the method: ask what chance would do under the same constraints.
* **6. Where notes want to go.** Meyer's gap-fill: 38 leaps in a hundred are filled, against 22 by chance from
  the same moves in the same range; momentum: after a step down the next move is down 70 times in a hundred
  (chance 55), after a step up, up 57 (47); leaps land on degrees 1, 3 or 5, 77 in a hundred; where each degree
  goes: 7 to 1, 4 to 3, 6 to 5, 2 to 1; an ear question (one phrase, three last notes).
* **7. Saying it twice.** Sequences in two tunes, heard; 60 of 275 phrases repeat an earlier phrase exactly; 13
  tunes contain a sequence; Frère Jacques against itself; the plan of a tune in letters (the Tune is ABCCAB).
* **8. Question and answer.** Phrases of eight beats; last notes 2.2 times as long as the others; the Ode to
  Joy's two phrases, heard: one ends on the second degree, the other on the first; a final phrase ends on the
  first degree 96 times in a hundred.
* **9. How much news is in a note?** Twenty notes: 4.3 bits each if nothing is known; 3.2 given which are
  common; 2.6 given the note before; longer memories do not help on 54 tunes; the guessing game: right first
  time 33 in a hundred, within three guesses 77; patterns of two moves follow Zipf's law (slope −1.3).
* **10. A model that is surprised.** A variable-order Markov model (the core of Pearce's IDyOM) trained on 53
  tunes; the Tune's surprise note by note, heard: 5.1 bits at the leap of a fifth, about two elsewhere; every tune
  scored by a model trained on the rest: the Ode to Joy is easiest (1.9 bits a note), a minor-key Russian tune
  hardest (5.5), heard; three melodies made up by the model, heard.
* **11. Words and tune.** Mandarin's four tones on Part 8's voice, heard; Cantonese songs follow their tones
  about nine times in ten (Wong and Diehl 2002); speech glides, song holds; a spoken phrase repeated becomes song
  (Deutsch and others 2011).
* **12. Frontier: predicting the listener.** Three predictors scored on unseen tunes: common notes 3.2 bits,
  nearness 3.2, the counting model 2.6; IDyOM and what listeners and their brains report; memory for melody and
  the tunes that stick (Jakubowski and others 2017); medium surprise is liked best (Gold and others 2019).
  ★ research problem: which tunes will be remembered.
* **Variation 14, recap and problems.** Mozart's K. 265; the Tune's first phrase as it is, with neighbour notes,
  with its leap filled in, with turns, upside down, backwards, and continued as the model expects (1.1 bits a
  note) and as it expects least (7.8); the ledger; what we found; five problems; where it comes back; in
  practice; references; Part 15.

## What is computed, and what is heard

`python -m videos.music.music14.compute` (under a minute) fills `.cache/music14/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | leaps and what follows them in 54 tunes and in 200 shufflings | 63 against 79 in a hundred |
| `contour` | Frère Jacques with scrambled octaves and with doubled intervals | the first keeps every note name; the second every direction |
| `steps` | every move; shares of steps, repeats, leaps; two random melodies; the streaming demonstration | Huron's counts for the Essen collection have the same shape |
| `range` | each tune's span; how its notes lie about its median | — |
| `arch` | nine shapes of phrase; the average of 275 phrases | Huron (1996): an arch |
| `leaps` | turns back after leaps, by where the leap lands: tunes, shuffled tunes, an urn | von Hippel and Huron (2000) |
| `tendency` | gap-fill against three kinds of chance; where each degree goes; three endings | 7→1, 4→3, 6→5 |
| `motive` | repeats and sequences; a tune against itself | — |
| `phrase` | phrase lengths, final lengthening, the degrees phrases end on | — |
| `info` | entropy; leave-one-out cross-entropy for orders 0 to 5; Zipf's law for pairs of moves | — |
| `model` | the Tune's information content under a model trained on the other 53; melodies sampled at orders 0, 1, 2 | the peak is the leap of a fifth |
| `tone` | four pitch contours (Chao's 55, 35, 214, 51) on one vowel | — |
| `frontier` | bits a note for three predictors | — |
| `more` | transposition; contour codes; a die; where the top note comes; momentum; plans in letters; the guessing game; the easiest and hardest tunes | the die: 40, 10 and 10 of 60, exactly |
| `tune` | Variation 14 | the ledger row |

Monochord's melodies are held against these in `tests/music/test_melody.py`; this part's claims and clips in
`tests/music/test_music14.py`.

**Sounds.** Eighteen clips. Melodies are on Part 7's piano (`physical model`), in twelve-tone equal temperament;
the streaming demonstration is organ tones (`synthesized`); the four tones are Part 8's source-filter voice on
the vowel *ah*. There are no recordings.

**The corpus.** Fifty-four traditional or long-out-of-copyright tunes, most of them from western Europe and
North America, with one each from China, Russia and Mexico. They were written out from memory for this series, in
scale degrees, in the versions most often sung; they are not a scholarly edition, the rhythms of some are
simplified, a few stop after their first strain, and phrase ends were marked by hand. Fifty-four tunes is a small
sample, and a sample of one kind of music: every count in the film is a count of *these* tunes. Where the film
says a pattern has been found more widely, the source is a published study of a far larger collection (chiefly
the Essen folksong collection).

**What the models are, and are not.** *Shuffling* a tune keeps its notes and loses their order; it is the control
that von Hippel and Huron used. *The urn* draws notes independently from a bell-shaped spread over an octave.
*The random walks* draw each move from the corpus's histogram of moves, inside an octave, on the notes of the
major scale: they have the tunes' step sizes and range and nothing else. *Gap-fill* is counted by one simple
rule (at least two of the four moves after a leap of a fourth or more are steps back into the gap); other
definitions give other numbers, and larger studies (von Hippel 2000) find less left over than we do. *The
counting model* is a variable-order Markov model on pitch alone, with PPM-style escape; it knows nothing of
rhythm, metre, scale degree as such, or phrase position, which is why it cannot tell a final note from any
other. It is the core of IDyOM, not IDyOM. *Bits per note* are leave-one-out on 54 tunes, so longer contexts are
starved of data. *The hardest tune for the model* is hard because the corpus is mostly in major keys: the number
measures the model's upbringing, not the tune. *The four tones* are idealised contours on a synthetic vowel,
without consonants or the durations and voice quality of real speech. *The inverted U* of the frontier chapter is
drawn as a sketch of a published finding, not from data of ours.

## Build

```bash
python -m videos.music.music14.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music14 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music14 --sync                         # the sound gates
python tools/dead_air.py renders/music14_480p.mp4 --sound music14  # no empty screen; no sound over a still one
python tools/lecture_length.py music14                          # 30 to 60 minutes, listening included
python tools/build.py music14                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 14                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **One tune, described.** Write the first two phrases of *Happy Birthday* as scale degrees. Give every move in
   semitones, the share that are steps, the range, and the shape of each phrase.

   *Solution.* 5 5 6 5 1 7 / 5 5 6 5 2 1, where the 5s, 6s and the 7 lie below the tonic (the tune begins on the
   fifth degree below it). The moves are
   0, +2, −2, +5, −1, then −4 across the phrase break, then 0, +2, −2, +7, −2. Of eleven moves six are steps,
   two are repeats and three are leaps; the range is a perfect fifth below the tonic to a major second above:
   seven semitones in these two phrases (the whole tune spans an octave). Each phrase begins on its lowest note
   and ends above its average: both are "rising" in Huron's nine shapes. The lab prints all of this.

2. **The leap rule for a die.** Notes are drawn independently and uniformly from 1, 2, …, n. Given that a leap
   has just gone up and landed on k, what is the chance that the next note is lower? Average over where upward
   leaps land, and explain the leap rule.

   *Solution.* The next note is independent of everything before it, so it is lower than k with probability
   (k − 1)/n, higher with (n − k)/n and equal with 1/n; among the notes that move, the share that go down is
   (k − 1)/(n − 1), which is more than half as soon as k is above the middle. An upward leap of two or more can
   only land on 3, …, n, and lands high more often than low (there are k − 2 ways to arrive at k). For a
   six-sided die: 60 ways to rise by two or more; afterwards 40 falls, 10 rises and 10 repeats, so 4/5 of the
   moves turn back. Nothing here knows about leaps: a leap is evidence that the note is far from the middle,
   and a note far from the middle is usually followed by one nearer to it.

3. **Ear.** The lab plays eight melodies: some are from the corpus, some have the same notes shuffled, some were
   made by the model. Say which is which.

   *Solution.* The lab prints the answers. Shuffled melodies give themselves away by leaps in both directions
   and no repeated pattern; the model's by plausible steps that go nowhere: no arch, no long note at a phrase
   end, no return. Real tunes repeat themselves within a few seconds.

4. **Build.** With `melody.NGram`, train on every tune but one and plot that tune's surprise. Which note of
   *Frère Jacques* surprises the model most? Then let the model also see rhythm, and see whether phrase endings
   get cheaper.

   *Solution.* In the lab, with `LEFT_OUT = "Frère Jacques"` and a memory of two notes, the peak (7.2 bits) is
   the G that begins the third pair of phrases after "E, C": a leap of a fifth, as in the Tune. The second
   largest is the drop to the low G in "ding, dang, dong". To add rhythm, make the model's symbols pairs (pitch,
   duration) or run a second model on durations and add the bits; long notes at phrase ends then become
   predictable from the long note before them, and with a feature for position in the bar (as IDyOM's "viewpoints"
   have) the final tonic becomes cheap.

5. ★ **Which tunes stick?** Among melodies of equal average surprise, which are remembered after one hearing?
   Propose a measurement that needs no listeners' opinions of quality.

   *Where the frontier is.* Recognition experiments (Halpern and Bartlett's reviews; Müllensiefen and Halpern
   2014) find that tunes with *rare motifs* are recognised better and that familiarity ratings follow *common*
   features; involuntary recall ("earworms", Jakubowski and others 2017) favours fast tunes with common overall
   contours and unusual intervals; the Hooked on Music experiment (Burgoyne and others 2013) measured how fast
   listeners recognise a hook. A measurement without opinions: play each melody once, and after a delay test
   recognition against lures matched for surprise (the model's own samples). What predicts the hit rate once
   average surprise is held fixed: where in the phrase the surprise falls, how much is repeated, or how singable
   the range is, is not settled.

## Sources

Books: D. Huron, *Sweet Anticipation: Music and the Psychology of Expectation* (2006), chs. 5–6; D. Temperley,
*Music and Probability* (2007); L. B. Meyer, *Emotion and Meaning in Music* (1956) and *Explaining Music* (1973);
E. Narmour, *The Analysis and Cognition of Basic Melodic Structures* (1990); A. S. Bregman, *Auditory Scene
Analysis* (1990); E. H. Margulis, *On Repeat: How Music Plays the Mind* (2014); D. Parsons, *The Directory of
Tunes and Musical Themes* (1975); Y. R. Chao, "A system of tone letters", *Le Maître Phonétique* 45 (1930).

Papers: C. E. Shannon, "A mathematical theory of communication", *Bell System Technical Journal* 27 (1948), and
"Prediction and entropy of printed English", 30 (1951); D. Deutsch, "Octave generalization and tune
recognition", *Perception & Psychophysics* 11 (1972); W. J. Dowling, "Scale and contour: two components of a
theory of memory for melodies", *Psychological Review* 85 (1978); P. G. Vos and J. M. Troost, "Ascending and
descending melodic intervals: statistical findings and their perceptual relevance", *Music Perception* 6 (1989);
D. Huron, "The melodic arch in Western folksongs", *Computing in Musicology* 10 (1996); P. von Hippel and
D. Huron, "Why do skips precede reversals? The effect of tessitura on melodic structure", *Music Perception* 18
(2000); P. von Hippel, "Redefining pitch proximity: tessitura and mobility as constraints on melodic
intervals", *Music Perception* 17 (2000); P. C. M. Wong and R. L. Diehl, "How can the lyrics of a song in a tone
language be understood?", *Psychology of Music* 30 (2002); M. T. Pearce, *The Construction and Evaluation of
Statistical Models of Melodic Structure in Music Perception and Composition* (PhD thesis, City University
London, 2005), and "Statistical learning and probabilistic prediction in music cognition", *Annals of the New
York Academy of Sciences* 1423 (2018); D. Deutsch, T. Henthorn and R. Lapidis, "Illusory transformation from
speech to song", *Journal of the Acoustical Society of America* 129 (2011); K. Jakubowski, S. Finkel, L. Stewart
and D. Müllensiefen, "Dissecting an earworm: melodic features and song popularity predict involuntary musical
imagery", *Psychology of Aesthetics, Creativity, and the Arts* 11 (2017); B. P. Gold, M. T. Pearce, E.
Mas-Herrero, A. Dagher and R. J. Zatorre, "Predictability and uncertainty in the pleasure of music: a reward for
learning?", *Journal of Neuroscience* 39 (2019).
