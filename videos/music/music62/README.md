# Music, Built: Part 62, Beat, Chords and Structure

Part 62 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act XI, *Listening Machines*. A child can clap along to a song; for
decades a program could not, and today's programs still tap at half or double speed and lose their place in a rubato.
This part builds the listeners that make DJ software, practice apps and accompaniment systems work: novelty and tempo,
beat tracking by dynamic programming, downbeats, chroma and chord recognition with Part 18's chorale statistics as the
prior, dynamic time warping offline and live, and form from self-similarity and repetition. The tools are Monochord's
(`explainer/music/monochord/mir/rhythm.py`, on Part 61's spectral flux); every performance is rendered by Monochord, so
every beat, chord and section is known exactly.

* **Clapping along.** An ear question (the session with a click track 80 ms late and one on the beat: which is on the
  beat? the second); how people hear the beat (entrainment, tapping ahead, a preferred tempo near 120); clapping along;
  what these listeners run; the plan.
* **1. Where the beats might be.** What to listen for; the session's novelty curve; the drums alone against the whole band,
  heard; other novelty curves; what makes a beat strong; a tempogram (bright at 100, 200 and 50).
* **2. Tempo, and its octave.** Choosing one tempo (the autocorrelation times a prior near 120: 100 on the session); a slow
  piece written at 50, read at 100 with the prior and 50 without, heard with both click tracks; tempo in real performances;
  which level.
* **3. Tracking the beat.** Ellis's dynamic programme; forty years of beat trackers; the session tracked (F 0.94), heard; a
  rubato piano performance tracked (the tempo misjudged at 125 against 106; F at best 0.58), heard; scoring beats.
* **4. Bars and downbeats.** An ear question (where do the bars start? the second); a clue in the bass (beats one and three
  strong, but not which is first); other meters; what tells us where the bar starts.
* **5. Chroma.** Folding octaves; chroma's relatives; the Tune's chroma, heard; chord templates; what else chroma is for.
* **6. Recognizing chords.** Chords in context (an HMM, Viterbi, two priors); the three recognizers compared (44 %, 51 % and
  76 % of frames right); what the frame-by-frame matcher confuses (chords heard a fifth up); what a prior does.
* **7. Time warping.** One score, two timings, heard; dynamic time warping (median 13 ms offline, 13 ms online, 206 ms at
  worst live); a tempo curve from the path; where time warping came from; what alignment is for.
* **8. Following a soloist.** Computer accompaniment (Dannenberg and Vercoe, 1984; Raphael); Monochord's accompanist; the
  follower following; what human accompanists do; how close it plays (a median 96 ms behind the voice).
* **9. Structure.** The whole Tune against itself, heard; Foote's novelty (weak, misplaced peaks: nothing in the texture
  changes); repetition (phrases a b c c a b: A B A; mean chroma cannot tell them apart); forms a machine might find;
  structure in practice.
* **10. Covers, and how far people agree.** An ear question (which is not the Tune? the third, Frère Jacques); key-invariant
  matching (the cover found five semitones up); covers in the wild; how far people agree.
* **11. Frontier: expressive and non-Western meter.** Whose meter; joint models; listening live; ★ research problem: how
  close to a human accompanist can a predictive follower play, and on what music does it fail?
* **Variation 62, recap and problems.** The Tune sung freely by Part 8's voice, accompanied by a piano that ignores it, then
  by one that listens; the ledger; what we found; five problems; where it comes back; in practice; references; Part 63.

## What is computed, and what is heard

`python -m videos.music.music62.compute` (about a minute) fills `.cache/music62/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `drums`, `tempo`, `halfdouble` | click tracks; novelty; the tempogram; prior-weighted tempo | the tempo played (tests) |
| `beats`, `downbeat` | Ellis's tracker on the session and on rubato; the low band by bar position | the beats rendered (tests) |
| `chords` | chroma; templates, an HMM, an HMM with Bach's transitions; confusions | the chords played (tests) |
| `align`, `follow` | offline and online DTW; the path's tempo curve; a live accompanist | the beat times rendered (tests) |
| `structure`, `cover` | self-similarity, Foote's novelty, repetition; key-invariant DTW | the sections and the transposition (tests) |

Monochord's tools are held in `tests/music/test_rhythm.py`; this part's claims and clips in `tests/music/test_music62.py`.

**Sounds.** Part 56's session, Part 38's piano (strict, with rubato, and a slow piece), Part 8's voice, Part 40's kit.

**What the models are, and are not.** *The beat tracker* is Ellis's (2007) with a fixed period from one tempo estimate; real
systems track a changing tempo. *The chord recognizer* has 24 triads and "no chord", a cosine emission and a hand-set
stay probability; the Bach prior is Part 18's Roman-numeral bigrams mapped to C major, so it is right only for music in C.
*The follower* is causal DTW with no prediction, and its 60 ms processing delay is assumed. *The structure labeller* uses
phrase lengths from the beat tracker and a fixed threshold.

## Build

```bash
python -m videos.music.music62.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music62 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music62 --sync                         # the sound gates
python tools/dead_air.py renders/music62_480p.mp4 --sound music62  # no empty screen; no sound over a still one
python tools/lecture_length.py music62                          # 30 to 60 minutes, listening included
python tools/build.py music62                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 62                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A tracker's beats are each 50 ms late. Within a 70 ms tolerance, what is its F-measure? And if they are 80 ms
   late?

   *Solution.* At 50 ms every estimate is within tolerance of its reference beat: precision and recall are 1, F = 1. At
   80 ms none is (each is 80 ms from one beat and, at any tempo slower than about 400 a minute, further from the next):
   F = 0. The tolerance turns a small shift into all or nothing, which is why continuity measures are reported too.

2. **Prove.** Show that the Viterbi recursion finds the most likely state sequence of an HMM, by induction on the frame.

   *Solution.* Let δ_t(j) be the largest probability of any state sequence ending in j at frame t, jointly with the
   observations so far. For t = 1, δ_1(j) = π_j b_j(x_1). Any sequence ending in j at t + 1 passes through some i at t, and
   its probability factors as (its first t states' joint probability) × A_ij × b_j(x_{t+1}); the first factor is at most
   δ_t(i), with equality for the best sequence to i. So δ_{t+1}(j) = max_i δ_t(i) A_ij b_j(x_{t+1}), and following the
   maximizing i back from the best final state recovers the most likely sequence.

3. **Ear.** The lab plays a drum pattern with click tracks shifted by random amounts; which are late? Find your threshold.

   *Solution.* The lab prints the shifts. Most listeners hear 40 ms as slightly late and 80 ms as clearly so; 20 ms is near
   the threshold for clicks against drums.

4. **Build.** Add a tempo that drifts to the beat tracker: let the period itself be a hidden state.

   *Where to look.* Replace the fixed P in the DP by a state (time, period) with transitions that change the period by at
   most a few percent a beat; score with the same novelty and log-ratio penalty; the search grows by the number of periods
   allowed. Test on the rubato performance of Chapter 3.

5. ★ **How close to a human accompanist can a predictive follower play, and on what music does it fail?**

   *Where the frontier is.* Model the soloist's timing (phrase arches, held cadences), predict each next beat with an
   uncertainty, schedule the accompaniment ahead of it, and compare asynchronies with human duos on the same music, by
   style and tempo.

## Sources

* M. Müller, *Fundamentals of Music Processing* (2nd ed., 2021); A. Lerch, *An Introduction to Audio Content Analysis*
  (2nd ed., 2022).
* E. W. Large and M. R. Jones, "The dynamics of attending", *Psychological Review* (1999); D. Moelants, "Preferred tempo
  reconsidered" (ICMPC, 2002); B. H. Repp, "Sensorimotor synchronization: a review of the tapping literature",
  *Psychonomic Bulletin & Review* (2005).
* D.-J. Povel and P. Essens, "Perception of temporal patterns", *Music Perception* (1985); E. D. Scheirer, "Tempo and beat
  analysis of acoustic musical signals", *JASA* (1998); M. Goto, "An audio-based real-time beat tracking system", *JNMR*
  (2001); S. Dixon, "Automatic extraction of tempo and beat from expressive performances", *JNMR* (2001); D. P. W. Ellis,
  "Beat tracking by dynamic programming", *JNMR* (2007); S. Böck, F. Krebs and G. Widmer, "Joint beat and downbeat tracking
  with recurrent neural networks" (ISMIR, 2016).
* T. Fujishima, "Realtime chord recognition of musical sound" (ICMC, 1999); A. Sheh and D. P. W. Ellis, "Chord segmentation
  and recognition using EM-trained hidden Markov models" (ISMIR, 2003); E. Gómez, *Tonal description of music audio
  signals* (thesis, 2006); M. Müller, F. Kurth and M. Clausen, "Audio matching via chroma-based statistical features"
  (ISMIR, 2005).
* H. Sakoe and S. Chiba, "Dynamic programming algorithm optimization for spoken word recognition", *IEEE Trans. ASSP*
  (1978); S. Dixon, "Live tracking of musical performances using on-line time warping" (DAFx, 2005); R. B. Dannenberg, "An
  on-line algorithm for real-time accompaniment" (ICMC, 1984); B. Vercoe, "The synthetic performer in the context of live
  performance" (ICMC, 1984); R. B. Dannenberg and C. Raphael, "Music score alignment and computer accompaniment", *CACM*
  (2006).
* J. Foote, "Automatic audio segmentation using a measure of audio novelty" (ICME, 2000); B. McFee and D. P. W. Ellis,
  "Analyzing song structure with spectral clustering" (ISMIR, 2014); J. B. L. Smith et al., "Design and creation of a
  large-scale database of structural annotations" (SALAMI, ISMIR, 2011).
