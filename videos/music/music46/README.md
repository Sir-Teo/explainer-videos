# Music, Built: Part 46, Expectation and Emotion

Part 46 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act VIII, *The Mind*. In 2011 PET supported striatal dopamine release during pleasurable music, while fMRI distinguished anticipatory and peak-related activity. Meyer had argued in 1956
that musical emotion is expectation delayed and fulfilled. This part builds a listener model, measures surprise and
uncertainty in bits, and engineers three endings for the Tune. The tools are Monochord's
(`explainer/music/monochord/listener.py`). The listener is trained on the series' corpus of folk and public-domain tunes;
published findings (Salimpoor, Cheung, Witek, Juslin and others) are quoted, not reproduced, and are listed under
Sources.

* **Wanting, then getting.** An ear question (three endings for the Tune: which surprised the listener most and least?
  F♯ 10.9 bits, A 5.5, C 1.2); chills and dopamine; the plan.
* **1. Expectation.** Hanslick and the expression theories; Meyer; Huron's ITPRA; three kinds of expectation; dynamic
  expectation heard (a motive's leap costs 4.8 bits, then 2.1 and 2.0, then 7.4 when changed); what expectation leaves
  out.
* **2. Statistical learning.** Saffran's infants; an ear question (a stream of tone words, then a word and a part-word;
  transitional probability 1 inside words, 0.4 across); probe tones heard (C 2.0, D 4.8, F♯ 8.6 bits); a lifetime of
  counting; growing up a listener.
* **3. A listener model.** How it works (PPM, long- and short-term models, after IDyOM); surprise and uncertainty;
  viewpoints; the Tune note by note, heard (1.98 bits a note, falling from 2.6 in the first phrase to 1.3 in the last);
  the listener sings; the whole corpus (1,788 notes; surprise and uncertainty correlate 0.23).
* **4. Surprise across melodies.** Mean surprise for the Tune, Ode to Joy, Part 42's kept and rejected drafts (3.1 and
  3.8 bits), its chains, random notes (3.9); the drafts heard; random notes and the order-4 chain heard; does the model
  hear as we do?; the inverted U.
* **5. Three endings.** Expected, delayed, denied, heard; their surprise note by note (the deceptive turn 6.3 bits, then
  the final C 0.9, against 1.2 undelayed; F♯ 10.9); the denied ending three times running (10.9, 3.0, 2.2 bits); how scale
  degrees feel; devices of delay; a suspension heard.
* **6. The brain at a wrong chord.** The ERAN; a Neapolitan ending heard; music and language (the P600); automatic
  prediction (the mismatch negativity); reward.
* **7. Surprise and uncertainty together.** Cheung and colleagues' interaction; where pleasure lies, sketched on our
  corpus; the two corners heard; tension as uncertainty; uncertainty engineered.
* **8. Groove.** Groove and syncopation; four patterns of rising syncopation (index 0, 3, 4, 11), heard; Witek's inverted
  U; is groove in the timing?; moving to a beat.
* **9. Expressed emotion.** An ear question (the Tune in four settings: happy, sad, angry, tender); the cues (after
  Juslin and Laukka); chills; eight mechanisms; the pleasure of sad music; music and memory; what does not replicate.
* **10. Frontier: the predicting brain.** Predictive processing; expectation across cultures; models as listeners;
  ★ research problem: how much of musical pleasure do surprise and uncertainty alone predict?
* **Variation 46, recap and problems.** The Tune's last two phrases with three endings, with the listener's surprise at
  each note; the ledger; what we found; five problems; where it comes back; in practice; references; Part 47.

## What is computed, and what is heard

`python -m videos.music.music46.compute` (under a minute) fills `.cache/music46/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `endings`, `again`, `tune46` | endings priced in bits; a denial repeated; Variation 46 | delay lowers the arrival's surprise (tests) |
| `tune`, `corpus`, `compare`, `extremes`, `drafts` | the listener on the Tune, the corpus and other melodies | random > the Tune; rejected > kept (tests) |
| `learn` | a Saffran-style stream and test | transitional probabilities (tests) |
| `probe`, `rep`, `sing` | probe tones; dynamic expectation; a sampled melody | probe ranking (tests) |
| `susp`, `neap`, `corners` | a suspension; a Neapolitan; the two corners | — |
| `groove`, `emotion` | four syncopation patterns; four expressive settings | the syncopation index (tests) |

Monochord's tools are held in `tests/music/test_listener.py`; this part's claims and clips in `tests/music/test_music46.py`.

**Sounds.** Part 7's piano and Part 38's bass (physical models), the additive orchestra, Part 40's drums, sine tones.
There are no recordings; the songs of Cheung's study are under copyright and are not played.

**What the models are, and are not.** *The listener* uses one viewpoint (pitch relative to the tonic) and a corpus of 51
tunes; IDyOM uses many viewpoints and far more music. *Its surprise* is a model's, not a measurement of any listener.
*The shaded regions* of chapter 7 sketch Cheung's published pattern on our notes; they are not his data. *Witek's curve*
is sketched, not reproduced.

## Build

```bash
python -m videos.music.music46.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music46 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music46 --sync                         # the sound gates
python tools/dead_air.py renders/music46_480p.mp4 --sound music46  # no empty screen; no sound over a still one
python tools/lecture_length.py music46                          # 30 to 60 minutes, listening included
python tools/build.py music46                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 46                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A model gives the next note probability 1/8. What is its surprise? And for 1/1000?

   *Solution.* −log₂(1/8) = 3 bits; −log₂(1/1000) = log₂ 1000 ≈ 9.97 bits. Each halving of the probability adds one bit.

2. **Prove.** Prove that uncertainty is largest when every next note is equally likely, and equals log₂ n.

   *Solution.* Maximise H = −Σ pᵢ log₂ pᵢ subject to Σ pᵢ = 1. With a Lagrange multiplier, −log₂ pᵢ − 1/ln 2 = λ for every
   i, so all pᵢ are equal, pᵢ = 1/n, and H = log₂ n. H is concave, so this stationary point is the maximum. (Gibbs's
   inequality gives the same in one line.)

3. **Ear.** The lab plays word and part-word triplets after a stream; say which was the word.

   *Solution.* The lab prints them. A word's three tones always came together in the stream, so it sounds complete; a
   part-word straddles a boundary and sounds subtly wrong. Listening twice to the stream helps.

4. **Build.** Train the listener on a different corpus and compare the Tune's surprise.

   *Where to look.* `Listener(corpus, order)` takes any list of pitch sequences relative to their tonics: try only the
   minor tunes, only the Christmas carols, or Part 42's chain outputs, and compare the Tune's mean surprise and which
   notes become surprising.

5. ★ **How much of musical pleasure do surprise and uncertainty alone predict?**

   *Where the frontier is.* Collect continuous pleasure ratings and physiology for many pieces; model each moment with
   surprise, uncertainty and their interaction from listener models trained on different amounts of music; report the
   variance explained per listener, and what remains.

## Sources

* L. B. Meyer, *Emotion and Meaning in Music* (1956); E. Hanslick, *On the Musically Beautiful* (1854); D. Huron, *Sweet
  Anticipation* (2006) and "Tone and voice" (2001).
* V. N. Salimpoor and others, "Anatomically distinct dopamine release during anticipation and experience of peak emotion
  to music", *Nature Neuroscience* (2011); L. Ferreri and others, *PNAS* (2019).
* J. R. Saffran, R. N. Aslin and E. L. Newport (1996); J. R. Saffran and others, "Statistical learning of tone sequences
  by human infants and adults", *Cognition* (1999); C. L. Krumhansl and R. N. Shepard (1979); L. J. Trainor and S. E.
  Trehub (1994); E. Bigand and B. Poulin-Charronnat (2006).
* M. T. Pearce, "The construction and evaluation of statistical models of melodic structure" (thesis, 2005); M. T. Pearce
  and others, *NeuroImage* (2010); D. Conklin and I. H. Witten, "Multiple viewpoint systems for music prediction" (1995).
* S. Koelsch and others, "Brain indices of music processing", *J. Cognitive Neuroscience* (2000); A. D. Patel and others
  (1998); S. Koelsch, P. Vuust and K. Friston, "Predictive processes and the peculiar case of music", *TICS* (2019).
* V. K. M. Cheung and others, "Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and
  auditory cortex activity", *Current Biology* (2019).
* P. Janata and others (2012); M. A. G. Witek and others, *PLoS ONE* (2014); H. C. Longuet-Higgins and C. S. Lee (1984);
  M. Davies and others (2013); J. Frühauf and others (2013); M. Zentner and T. Eerola (2010).
* P. N. Juslin and P. Laukka, *Psychological Bulletin* (2003); P. N. Juslin, "From everyday emotions to aesthetic
  emotions", *Physics of Life Reviews* (2013); J. A. Sloboda (1991); O. Grewe and others (2007); J. K. Vuoskoski and
  T. Eerola on sad music; C. L. Krumhansl and J. A. Zupnick (2013); D. E. Berlyne, *Aesthetics and Psychobiology*
  (1971); F. H. Rauscher and others (1993) and later meta-analyses of the "Mozart effect".

## Interpretation limits

PET and fMRI provide complementary evidence; they do not directly resolve two timed dopamine pulses. Surprise is minus log probability, not a literal guess count. This symbolic transition model is an analogy to statistical learning, not a complete infant or brain model. Probe-tone fit and predictability differ; corpus comparisons do not validate pleasure. Part 42’s tension proxy does not compute entropy, and predictive precision is not reciprocal Shannon entropy. Cheung’s reported chord results are sketched on our note data, not re-estimated. Emotion labels and inverted-U effects depend on listener and stimulus; mode changes alter pitches as well as performance.
