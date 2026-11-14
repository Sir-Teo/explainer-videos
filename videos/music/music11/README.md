# Music, Built: Part 11, Rhythm and Meter

Part 11 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). Part 10 wrote down how long a note lasts; but a length on a page is only a ratio.
This part is about those ratios played in time, to a listener: the pulse and how fast it can be, metre as pulses
nested in pulses, what makes a beat strong, syncopation as a number, three against two, beats of unequal length,
swing, and what happens to a rhythm played too fast to count. The rhythm engine is Monochord's
(`explainer/music/monochord/rhythm.py`), the drums are Part 9's struck things cut short
(`explainer/music/monochord/instruments/drumkit.py`), and the pictures are in `explainer/music/rhythmviz.py`;
every sound is computed in `compute.py`. Published findings are the ones listed under Sources.

* **Tick, tock.** Sixteen identical strokes, heard in pairs (an ear question); measured: no difference between
  any two; Bolton (1894); the brain's larger response to a change on a "tick" (2003); metre is added by the
  listener; the plan.
* **1. A pulse.** Tempo in beats per minute and in seconds; clicks from one every 2.5 seconds to fifty a second;
  the window of the beat (about 0.25 s to 2 s), divisions down to about 100 ms, a flutter, a tone; taps that
  land ahead of the click: the beat as a prediction; two tempos five per cent apart (an ear question).
* **2. Meter.** One bar of four-four as five nested pulses; a pulse's weight is the number of levels it belongs
  to (Lerdahl and Jackendoff's grid); three-four and six-eight as two nestings of the same six eighths; a toy
  pulse finder, which taps the Tune at 0.55 s, the tempo it was played at, and cannot find the bar.
* **3. Accent.** Every third tone louder, longer, higher; pairs that fade in (an ear question): the loud sound
  begins a pair, the long one ends it (Woodrow, 1909).
* **4. Dividing the beat.** A beat cut in one, two, three and four; the triplet; at 109 beats to the minute,
  550, 275, 183 and 138 ms; a predict-pause (a triplet at 120: 167 ms); simple and compound metres.
* **5. Syncopation.** A note on a weak pulse before a silent strong one; Longuet-Higgins and Lee's index (1984),
  worked for the son clave (4); four rhythms scoring 0, 4, 6 and 7; two to compare (an ear question: 2 and 5);
  strokes that are the beat until a drum arrives between them (index 0, then 7): syncopation needs a grid that
  something else holds; Witek's arch (2014): the urge to move is greatest at moderate syncopation.
* **6. Three against two.** Six eighths as 3 + 3 and 2 + 2 + 2, alternating: hemiola; both at once: a cycle of
  six with strokes 2, 1, 1, 2 apart; four against three on a cycle of twelve (3, 1, 2, 2, 1, 3); a rhythm against
  a late copy of itself (5, 1 and 0 strokes together at delays of 0, 2 and 8 pulses): phasing.
* **7. Long beats and short.** Seven pulses as 2 + 2 + 3, 2 + 3 + 2 and 3 + 2 + 2; the number of metres made of
  twos and threes: a(n) = a(n−2) + a(n−3), so 2 for five pulses, 3 for seven, 5 for nine, 12 for twelve; four
  Balkan dances.
* **8. Swing.** Eighth notes at one, two and three to one; Friberg and Sundström (2002): about 3.5 to 1 at slow
  tempos, 1 to 1 at the fastest, the short note near 100 ms; so the ratio is (beat − 100 ms)/100 ms, two to one
  at 200 beats to the minute only; what the page does not say.
* **9. Where rhythm becomes pitch.** Three against two, sped up from 0.75 to 100 cycles a second (an ear
  question); at the end 200 Hz and 300 Hz, 702 cents: a perfect fifth; every interval of Part 1 as a
  polyrhythm; Cowell (1930); two patterns at 110 cycles a second: one pitch, two spectra: the pattern inside
  the cycle becomes the tone colour.
* **10. Frontier: what the listener expects.** The telephone game on three-interval rhythms, as a simulation:
  one chain heard, drifting to 2 : 1 : 1; two simulated listeners with different expectations; Jacoby and
  McDermott (2017) and Jacoby and others (2024): small-integer ratios in every one of 39 groups, weighted by
  culture; a cockatoo and a sea lion that keep a beat; what is not known (the source of the ratios, microtiming, why we move, machines). ★ research problem.
* **Variation 11, recap and problems.** The Tune in four, as a waltz, in five, in seven, swung and with a
  hemiola; the ledger; what we found; five problems; where it comes back; in practice; references; Part 12.

## What is computed, and what is heard

`python -m videos.music.music11.compute` (under a minute) fills `.cache/music11/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | sixteen copies of one stroke; the level of each | the largest difference is 0 dB |
| `tempo` | a click train whose rate grows by equal ratios; two tempos 5% apart | the rate at the start and the end |
| `meter` | metres as nested groupings; a pulse finder on the Tune's onsets | the tempo the Tune was played at (0.55 s); every note falls on a tap |
| `accent` | every third tone louder, longer, higher; loud-soft and long-short pairs with faded ends | — (the listeners' answers are Woodrow's, not computed) |
| `divide` | one beat cut in one to four; durations at 109 and 120 | arithmetic |
| `sync` | Longuet-Higgins and Lee's index for four rhythms and a pair | 0 for rhythms on the beats; the clave's 4 by hand |
| `hemiola` | six pulses grouped two ways; 3 : 2 and 4 : 3 on their common grids | the gaps 2 1 1 2 and 3 1 2 2 1 3 |
| `additive` | every composition of n into twos and threes | Padovan's recurrence |
| `swing` | swung eighths at three ratios; the ratio a 100 ms short note gives at each tempo | 2 : 1 at 200, 1 : 1 at 300 |
| `continuum` | two click trains locked 3 : 2, accelerating; the spectrum of the last two seconds | 200 Hz and 300 Hz; 702 cents |
| `frontier` | the telephone game for two simulated listeners; one chain as sound | the cloud gathers at the listeners' own ratios |
| `tune` | Variation 11 | the forty-two pitches are the Tune's |

Monochord's rhythm engine is held against these in `tests/music/test_rhythm.py`; this part's claims and clips in
`tests/music/test_music11.py`.

**Sounds.** Nineteen clips, labelled on screen. `physical model`: the kit (a bass drum, a tom, a wood block, a
clave and a rim stroke, each a set of Part 9's modes with heavy damping) and Part 7's piano. `synthesized`: the
click trains, the organ tones of chapter 3, and the hi-hat, which is filtered noise. There are no recordings.

**What the models are, and are not.** *The pulse finder* is a toy: it scores steady grids against the onsets of a
melody and prefers periods near half a second. It finds the Tune's beat; it knows nothing of accent, harmony or
loudness, and it would fail on most real music. *The metric weights* are Lerdahl and Jackendoff's dots, one per
level; *the syncopation index* is Longuet-Higgins and Lee's, applied to a pattern that repeats. Other indices
exist and rank some rhythms differently. *Subjective rhythmization, the grouping law and the arch of syncopation
against the urge to move* are reported from the literature, not computed; the arch is drawn schematically, and
the film says so. *The swing curve* is not Friberg and Sundström's data: it is the consequence of their finding
that the short note stays near 100 ms, capped at the largest ratio they report. *The telephone game* is a
simulation in which a listener's expectations are bumps at chosen whole-number rhythms, what is heard is blurred,
and what is tapped is drawn from the product of the two; the two listeners' expectations were chosen by hand to
differ. It illustrates the method and why it converges on a listener's expectations; it is not a model of any
population. *The drums* mark time; they are not studies of real drums.

## Build

```bash
python -m videos.music.music11.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music11 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music11 --sync                         # the sound gates
python tools/dead_air.py renders/music11_480p.mp4 --sound music11  # no empty screen; no sound over a still one
python tools/lecture_length.py music11                          # 30 to 60 minutes, listening included
python tools/build.py music11                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 11                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **A jig.** A jig is marked 132 beats to the minute in six-eight, the beat a dotted quarter. How long, in
   milliseconds, is a bar, a beat and an eighth note? How fast could the tempo go before the eighth notes reached
   the limit of 100 ms?

   *Solution.* A beat lasts 60/132 = 0.4545 s, or 455 ms. A bar is two beats, 909 ms; an eighth is a third of a
   beat, 152 ms. The eighths reach 100 ms when the beat is 300 ms, which is 200 beats to the minute. (Presto jigs
   are in fact played near that speed, and are felt one beat to the bar.)

2. **Twos and threes.** Let a(n) be the number of ways to fill n pulses with beats of two and three. Show that
   a(n) = a(n−2) + a(n−3), and find a(12). Which of the twelve have four beats?

   *Solution.* Every filling begins with a beat of two, leaving n − 2 pulses to fill in a(n−2) ways, or with a
   beat of three, leaving n − 3 in a(n−3) ways; the two kinds are different fillings, and there are no others.
   With a(0) = 1, a(1) = 0, a(2) = 1: a(3) = 1, a(4) = 1, a(5) = 2, a(6) = 2, a(7) = 3, a(8) = 4, a(9) = 5, a(10) =
   7, a(11) = 9, a(12) = 12. A filling of 12 with k beats has 12 − 2k threes, so k = 4 needs four threes: only
   3 + 3 + 3 + 3 (twelve-eight). Five beats means two threes and three twos, in 10 orders; six beats is
   2 + 2 + 2 + 2 + 2 + 2. (These are the Padovan numbers.)

3. **Ear.** The lab plays eight bars of six eighth notes in a random order, each grouped 3 + 3 or 2 + 2 + 2 by its
   accents. Say which is which.

   *Solution.* The lab prints the order. Count the bass drum: two strokes to the bar is 3 + 3, three is
   2 + 2 + 2. With practice the two feel different before they are counted: one swings in two, like a jig; the
   other steps in three, like a waltz at speed.

4. **Build.** With `rhythm.syncopation`, find the rhythm of five notes on sixteen pulses with the largest index,
   and the largest among those that sound the downbeat. Play both: can you still feel the beat?

   *Solution.* The lab tries all 4,368. The largest index is 12, for `.x.x.x...x...x..`: five notes on the
   weakest pulses, each followed by silence on a stronger one, and nothing on any beat. Among rhythms that sound
   the downbeat the largest is 8, for `xx.x.x...x......`. Played alone, the first is heard as a plain rhythm
   starting on its own first note: a listener moves the grid to fit, which is why the film plays every rhythm
   over a drum that keeps the beat. Syncopation exists only against a metre that something else maintains, even
   if that something is the listener's memory of the bar before.

5. ★ **Where do the ratios come from?** Design an experiment that could tell whether listeners' preference for
   small-integer rhythms comes from hearing and moving, or from the music they have heard. Who would your
   listeners be, and what result would settle it?

   *Where the frontier is.* The telephone game (Jacoby and McDermott, 2017; Jacoby and others, 2024) shows that
   every group tested has expectations at small-integer ratios and that their weights follow local music, which
   argues for a shared scaffold and a learned emphasis. It cannot say where the scaffold comes from. Candidates
   for a decisive test: infants before much musical exposure (the method needs tapping, so it would have to be
   replaced by looking-time or EEG measures of surprise); people with little exposure to metric music, who are
   now very hard to find; other species that entrain to a beat; or training studies that try to install a
   non-integer category in adults and see whether it holds. Each has a flaw, and stating the flaws is the
   exercise. A result that would count against a purely learned origin is an integer-ratio bias for ratios
   absent from everything a listener has heard; the 2024 study reports hints of this and is careful about it.

## Sources

Books: J. London, *Hearing in Time: Psychological Aspects of Musical Meter* (2nd ed., 2012), for the limits of
pulse and metre; F. Lerdahl and R. Jackendoff, *A Generative Theory of Tonal Music* (1983), ch. 4, for the
metrical grid; W. A. Sethares, *Rhythm and Transforms* (2007); H. Cowell, *New Musical Resources* (1930), for
rhythm and interval as one scale of ratios; P. Fraisse, *Psychologie du rythme* (1974); C. Brăiloiu, "Le rythme
aksak", *Revue de musicologie* 33 (1951); G. Toussaint, *The Geometry of Musical Rhythm* (2013), for rhythms on a
circle.

Papers: T. L. Bolton, "Rhythm", *American Journal of Psychology* 6 (1894); H. Woodrow, "A quantitative study of
rhythm: the effect of variations in intensity, rate and duration", *Archives of Psychology* 14 (1909); J. R.
Iversen, A. D. Patel and K. Ohgushi, "Perception of rhythmic grouping depends on auditory experience", *JASA* 124
(2008); H. C. Longuet-Higgins and C. S. Lee, "The rhythmic interpretation of monophonic music", *Music
Perception* 1 (1984); D.-J. Povel and P. Essens, "Perception of temporal patterns", *Music Perception* 2 (1985);
R. Parncutt, "A perceptual model of pulse salience and metrical accent in musical rhythms", *Music Perception* 11
(1994); L. van Noorden and D. Moelants, "Resonance in the perception of musical pulse", *Journal of New Music
Research* 28 (1999); C. Drake and M.-C. Botte, "Tempo sensitivity in auditory sequences", *Perception &
Psychophysics* 54 (1993); A. Friberg and A. Sundström, "Swing ratios and ensemble timing in jazz performance:
evidence for a common rhythmic pattern", *Music Perception* 19 (2002); R. Brochard, D. Abecasis, D. Potter,
R. Ragot and C. Drake, "The 'ticktock' of our internal clock: direct brain evidence of subjective accents in
isochronous sequences", *Psychological Science* 14 (2003); R. Bååth, "Subjective rhythmization: a replication and
an assessment of two theoretical explanations", *Music Perception* 33 (2015); M. A. G. Witek, E. F. Clarke,
M. Wallentin, M. L. Kringelbach and P. Vuust, "Syncopation, body-movement and pleasure in groove music", *PLoS
ONE* 9 (2014); M. Davies, G. Madison, P. Silva and F. Gouyon, "The effect of microtiming deviations on the
perception of groove in short rhythms", *Music Perception* 30 (2013); G. Aschersleben, "Temporal control of movements in sensorimotor synchronization", *Brain and Cognition* 48
(2002); B. H. Repp, "Sensorimotor synchronization: a review of the tapping literature", *Psychonomic Bulletin &
Review* 12 (2005); A. D. Patel, J. R. Iversen, M. R. Bregman and I. Schulz, "Experimental evidence for
synchronization to a musical beat in a nonhuman animal", *Current Biology* 19 (2009); P. Cook, A. Rouse, M. Wilson
and C. Reichmuth, "A California sea lion (*Zalophus californianus*) can keep the beat", *Journal of Comparative
Psychology* 127 (2013); N. Jacoby and J. H. McDermott, "Integer
ratio priors on musical rhythm revealed cross-culturally by iterated reproduction", *Current Biology* 27 (2017);
N. Jacoby and others, "Commonality and variation in mental representations of music revealed by a cross-cultural
comparison of rhythm priors in 15 countries", *Nature Human Behaviour* 8 (2024); K. Stockhausen, "… wie die Zeit
vergeht …", *Die Reihe* 3 (1957).
