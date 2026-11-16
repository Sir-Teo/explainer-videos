# Music, Built: Part 45, The Scene

Part 45 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act VIII, *The Mind*. Send jumping notes to each ear and the listener
hears two smooth scales, one on each side, which neither ear was given (Deutsch, 1975; headphones). The ear receives one
pressure wave and the mind returns a scene of separate voices. This part builds the rules of that separation, models the
streaming boundary, and shows the rules of Part 16 falling out of them. The tools are Monochord's
(`explainer/music/monochord/scene.py`). The demonstrations are built as the classic experiments built theirs (sine
tones, harmonic complexes, noise, Shepard tones), with the series' own instruments where a real timbre matters. Published
findings are the ones listed under Sources.

* **Two scales, two ears.** An ear question (headphones: does the right ear's melody step or leap?); each ear alone;
  one wave, a whole scene; the plan.
* **1. Streaming.** ABA- triplets at four settings, heard; six semitones at 90 ms, thirty times (the split builds up);
  principles of sequential grouping; streaming in other animals; build-up.
* **2. A model of the boundary.** Van Noorden's two boundaries; one semitone, fast (below the fission boundary), heard;
  a competition model of ours (capture strength e^(−Δt/τ) e^(−|Δz|/w), two streams when Δz > (w/τ) T); fitted to points
  read from van Noorden's figure: w/τ = 32.4 ERB-numbers a second, 0.28 semitone rms; streaming in neurons; what the
  model leaves out.
* **3. Melodies hidden in melodies.** An ear question (a tune interleaved with another line, crossing it 15 times in 16
  notes: name it); Dowling's experiment; implied polyphony, one line slow and fast, heard; Bach's solo suites;
  hocket, the trick reversed.
* **4. Sounds at the same moment.** Simultaneous grouping; a harmonic mistuned by 0, 1, 3 and 8%, heard; a harmonic
  starting 80 ms early, heard; common fate (three harmonics given a vibrato), heard; place (one harmonic to one ear),
  heard; common fate and place.
* **5. What fills a gap.** A glide through silence and through noise, heard; the Tune's first phrase interrupted, heard;
  phonemic restoration; old plus new.
* **6. Counterpoint as scene analysis.** Huron's derivation; parallel fifths and contrary motion, heard; crossing scales
  heard as bouncing; the rules and their principles; onsets and independence; when the rules relax.
* **7. A timbre space of our instruments.** Thirteen of the series' instruments, heard; five measurements; their space
  by multidimensional scaling (two axes carrying 37% and 31% of the variation); streaming by timbre alone, heard; beyond
  the map; timbre and grouping.
* **8. Pitch and its illusions.** Height and chroma; the octave-scrambled Tune, heard; the pitch of a bell; an ear
  question (24 Shepard steps up: two octaves higher?); Risset's endless glide, heard; the tritone paradox.
* **9. Absolute pitch and pitch memory.** Absolute pitch; two pitch-memory trials after Deutsch (1970), heard; everyday
  pitch memory (Levitin); relative pitch; pitch in tone languages.
* **10. Frontier: machines that hear scenes.** Deep networks as models of auditory cortex; machines that separate;
  when scene analysis fails (implants, hearing aids); ★ research problem: do networks trained on natural sound
  reproduce human streaming boundaries?
* **Variation 45, recap and problems.** The Tune's first two phrases interleaved with a line crossing it 13 times on the
  same piano, then released by timbre (the other line on the chip's thin pulse) and by register; the ledger; what we
  found; five problems; where it comes back; in practice; references; Part 46.

## What is computed, and what is heard

`python -m videos.music.music45.compute` (under a minute) fills `.cache/music45/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `each` | the scale illusion (stereo), each ear alone | each ear leaps, the heard lines step (tests) |
| `aba`, `fission`, `ambig`, `boundary` | streaming stimuli; the fitted model | the model's straight-line boundary (tests) |
| `inter`, `compound`, `tune` | interleaved melodies; implied polyphony; Variation 45 | crossings counted (tests) |
| `mistune`, `onset`, `fate`, `place` | grouping stimuli | the mistuned harmonic's frequency (tests) |
| `cont`, `melcont` | the continuity illusion | the gap is silent (tests) |
| `fuse`, `bounce` | parallel and contrary duets; crossing scales | — |
| `timbre`, `tstream` | features of 13 instruments; MDS; streaming by timbre | attack, decay and odd/even on test signals (tests) |
| `shepard`, `risset`, `octaves`, `memory` | pitch illusions and memory trials | Shepard tones return to the start (tests) |

Monochord's tools are held in `tests/music/test_scene.py`; this part's claims and clips in `tests/music/test_music45.py`.

**Sounds.** Sine tones, harmonic complexes, noise, Shepard tones and the chip are synthesized; Part 7's piano and Part
38's plucked bass are physical models; the additive orchestra and Part 17's voice as before. Two clips are stereo and want
headphones. There are no recordings.

**What the models are, and are not.** *The streaming model* is ours: two exponentials and a competition, one constant,
no build-up, attention or ambiguity. *Van Noorden's points* were read from a reproduction of his figure, good to about a
semitone. *The timbre space* is built from measurements, not listeners' judgements. *The fission boundary* is quoted as a
single typical value.

## Build

```bash
python -m videos.music.music45.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music45 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music45 --sync                         # the sound gates
python tools/dead_air.py renders/music45_480p.mp4 --sound music45  # no empty screen; no sound over a still one
python tools/lecture_length.py music45                          # 30 to 60 minutes, listening included
python tools/build.py music45                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 45                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** With the fitted model, at what tone repetition time do 7 semitones at 1 kHz split into two streams?

   *Solution.* Seven semitones above 1 kHz is 1,498 Hz; the ERB-number distance is 21.4 log₁₀(1 + 0.00437 × 1498) −
   21.4 log₁₀(1 + 0.00437 × 1000) = 18.79 − 15.62 = 3.16. Two streams when 3.16 > 32.4 T, so T < 0.098 s: faster than
   about 100 ms onset to onset.

2. **Prove.** Prove that the competition model's boundary is a straight line in T, and find its slope in ERB-numbers.

   *Solution.* The next A is 2T away at the same pitch, B is T away at distance Δz. Two streams when e^(−2T/τ) >
   e^(−T/τ) e^(−Δz/w), that is e^(−T/τ) > e^(−Δz/w), that is Δz > (w/τ) T: a line through the origin with slope w/τ,
   fitted at 32.4 ERB-numbers a second.

3. **Ear.** The lab plays ABA- triplets at random intervals and speeds; say one stream or two.

   *Solution.* The lab prints the model's verdicts. Compare yours: the model has no build-up, so near the boundary you may
   hear one stream for the first seconds and two afterwards.

4. **Build.** Add a sixth measurement to the timbre space (say, spectral flux) and redraw it.

   *Where to look.* `scene.features` computes the measurements and `timbre_space` takes a list of keys; add the flux
   (the mean change of the normalised spectrum between successive frames) to `features`, pass the longer key list, and
   see which axis it joins.

5. ★ **Do networks trained on natural sound reproduce human streaming boundaries?**

   *Where the frontier is.* Read out the streams a trained separation network produces for ABA- sequences across
   interval and speed; map its boundary; compare with van Noorden's and with listeners' build-up curves; if they agree,
   test whether training on artificial sound changes the boundary.

## Sources

* A. S. Bregman, *Auditory Scene Analysis* (1990); D. Deutsch (ed.), *The Psychology of Music* (3rd ed., 2013).
* D. Deutsch, "Two-channel listening to musical scales", *JASA* (1975); "Tones and numbers: specificity of interference
  in immediate memory", *Science* (1970); "Octave generalization and tune recognition", *Perception & Psychophysics*
  (1972); "A musical paradox", *Music Perception* (1986); D. Deutsch and others on absolute pitch and tone language (2006).
* L. P. A. S. van Noorden, *Temporal Coherence in the Perception of Tone Sequences* (thesis, 1975); S. Anstis and
  S. Saida (1985); C. Micheyl and others, *Neuron* (2005); J. Rankin and others, *PLoS Computational Biology* (2015).
* W. J. Dowling, "The perception of interleaved melodies", *Cognitive Psychology* (1973); D. Huron, "Tone and voice: a
  derivation of the rules of voice-leading from perceptual principles", *Music Perception* (2001).
* B. C. J. Moore, B. R. Glasberg and R. W. Peters (1986); C. J. Darwin on onset asynchrony; S. McAdams, "Spectral fusion,
  spectral parsing and the formation of auditory images" (1984); R. M. Warren, "Perceptual restoration of missing
  speech sounds", *Science* (1970).
* J. M. Grey (1977); S. McAdams and others (1995); P. Iverson, "Auditory stream segregation by musical timbre", *JEP:
  HPP* (1995); R. N. Shepard, "Circularity in judgments of relative pitch", *JASA* (1964); D. J. Levitin (1994) and
  D. J. Levitin and P. R. Cook (1996).
* A. J. E. Kell and others, *Neuron* (2018); E. C. Cherry, *JASA* (1953); S. A. MacDougall-Shackleton and others
  (1998).

## Interpretation limits

Illusion reports, side assignments and streaming boundaries vary with listener, attention, stimulus and task. The boundary error is an in-sample fit to approximate digitized points, not a held-out prediction. Grouping principles help explain selected voice-leading goals without deriving every historical convention. The timbre map uses standardized acoustic features, not listener similarity ratings. Absolute-pitch prevalence is sample-dependent; familiar-song memory is approximate. Source-separation models need not implement the same mechanisms as human hearing.
