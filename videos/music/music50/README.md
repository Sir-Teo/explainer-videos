# Music, Built: Part 50, Dynamics, Distortion and Pitch

Part 50 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act IX, *Electric Sound*. Two accidents made two genres. A damaged
amplifier in 1951 gave rock its fuzz. In 1998 a pitch corrector, invented by a geophysicist who had used autocorrelation
to find oil, was set to act instantly, and the sound of a voice snapping between notes became a style. This part builds
the effects that are not linear, or that change with the signal: shapers and their harmonics, intermodulation and
aliasing, compressors and their relatives, and the machinery that unties pitch from time. The tools are Monochord's
(`explainer/music/monochord/dynamics.py`); the voice is Part 8's, the guitar and drums Part 40's.

* **Two accidents, two genres.** An ear question (the Tune sung a little out of tune, then hard-tuned: which was
  corrected? A median 28 cents off, then 0.6); the pitch tracks; Rocket 88 and Believe; the plan.
* **1. Nonlinearity makes new frequencies.** New frequencies; three ways to bend (hard clip, tanh, cubic); what each bend
  adds (a 1 kHz sine driven three times past the bend: the hard clip's third at −11 dB, fifth −18.5, seventh −27.5); three
  bends heard on one guitar note; a riff clean and driven, heard; why only odd harmonics; valves, transistors and tape.
* **2. Chebyshev's exact harmonics.** Tₙ(cos θ) = cos nθ; a shaper built from its spectrum (asked for 1, ½, ¼ at
  harmonics 1, 3, 5: measured −6.02 and −12.04 dB, the even ones below −180); one shaper at three input levels, heard (at a
  quarter of full size the upper harmonics fade, while the third rises nearly to the fundamental); waveshaping synthesis.
* **3. Intermodulation and the power chord.** Two tones in, many out; a fifth and a third through tanh (products on
  multiples of 110 Hz and of 55); a power chord and a major chord distorted, heard; the difference tone.
* **4. Aliasing in nonlinear effects.** Harmonics that fold; an ear question (a sweep through a hard clip at 48 kHz and 8
  times oversampled: which has tones moving the wrong way?); three ways to compute a shaper (alias energy −26.8 dB plain,
  −32.5 with antiderivative antialiasing, −47.3 oversampled); aliasing hides everywhere.
* **5. Compressors.** An automatic hand on the fader; the static curve (ratios 2, 4, 10, a 6 dB knee); attack and release
  (12 ms to 90 per cent; about 0.3 s to let go); release heard (pumping at 25 ms); an ear question (a groove plain and
  compressed at the same loudness: which?, the loudness spread 9.1 dB against 4.9); punch (the crest factor rises, 16.3 to
  21.2 dB); what the compressor hears.
* **6. Limiters, gates and sidechains.** The family; a gate, heard; a sidechain ducking a pad, heard; more uses; looking
  ahead.
* **7. Time and pitch.** Pitch and time, tied; a fifth higher by resampling and by PSOLA, heard; PSOLA; speed and pitch in
  the studio; pitch and formants.
* **8. Overlap-add and the phase vocoder.** Overlap-add; the phase vocoder (Flanagan and Golden; Laroche and Dolson); the
  phrase stretched twice two ways, heard; limits and uses; extreme stretching; stretching at work.
* **9. Pitch correction.** Finding the pitch; YIN, step by step; the target at three speeds; three speeds heard; from
  repair to style; editing pitch by hand.
* **10. Vocoders and ring modulation.** Dudley's vocoder; what it sends (16 bands); the voice, the chord, vocoded and
  ring-modulated, heard; the talk box; the vocoder in music; ring modulation.
* **11. Frontier: neural models of analog gear.** Amplifiers learned; white, black and grey boxes; antialiasing
  nonlinearities; ★ research problem: how small can a neural amplifier model be, indistinguishable at every setting and
  alias-free?
* **Variation 50, recap and problems.** The Tune sung, hard-tuned, vocoded and stretched eightfold; the ledger (28 cents
  sung, 0.6 corrected; one second stretched to 7.7); what we found; five problems; where it comes back; in practice;
  references; Part 51.

## What is computed, and what is heard

`python -m videos.music.music50.compute` (under a minute) fills `.cache/music50/`.

| Item | What it computes | Checked against |
|---|---|---|
| `shapers`, `shapers3`, `cheblevels`, `fuzz` | harmonics of three shapers; Chebyshev's exact harmonics; a riff driven | Tₙ(cos θ) = cos nθ (tests) |
| `imd` | two-tone products for a fifth and a third | common divisors 110 and 55 Hz (tests) |
| `alias` | a clipped sweep; alias energy plain, by ADAA, 8× oversampled | oversampling best (tests) |
| `curves`, `comp`, `pump`, `gate`, `duck` | static curves; attack and release; loudness spread and crest; pumping; a gate; a sidechain | the static gain (tests) |
| `pitch`, `stretch` | resampling against PSOLA; overlap-add against the phase vocoder | length and pitch kept (tests) |
| `hook`, `correct`, `speeds` | YIN pitch tracks; correction targets at three speeds; PSOLA | the scale notes (tests) |
| `vocoder` | a 16-band channel vocoder and ring modulation | — |

Monochord's tools are held in `tests/music/test_dynamics.py`; this part's claims and clips in `tests/music/test_music50.py`.

**Sounds.** Part 8's voice (a source-filter model), Part 40's guitar, drums and pad, a plucked bass, sawtooth chords and
sine tones, through this part's effects. The songs named (Rocket 88, Believe and others) are described, not played.

**What the models are, and are not.** *The shapers* are memoryless; real amplifiers filter before and after, and have
memory. *The compressor* is one feedforward design with a peak detector; real units differ in detection and character.
*The pitch corrector* is YIN, a nearest-note target and PSOLA; commercial correctors add formant handling, note-change
detection and much else. *The voice* was sung out of tune on purpose, by random detuning of each note.

## Build

```bash
python -m videos.music.music50.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music50 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music50 --sync                         # the sound gates
python tools/dead_air.py renders/music50_480p.mp4 --sound music50  # no empty screen; no sound over a still one
python tools/lecture_length.py music50                          # 30 to 60 minutes, listening included
python tools/build.py music50                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 50                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A compressor has threshold −20 dB, ratio 4 and no knee. What comes out for −8 dB in?

   *Solution.* −8 is 12 dB over the threshold; at 4 : 1 that becomes 3 dB over: −20 + 12/4 = −17 dB out, a gain reduction
   of 9 dB.

2. **Prove.** Prove that an odd shaper, f(−x) = −f(x), fed a pure tone, makes only odd harmonics.

   *Solution.* Let x(t) = cos ωt and y(t) = f(x(t)). Shifting time by half a period, t → t + π/ω, turns cos ωt into
   −cos ωt, so y(t + π/ω) = f(−x(t)) = −y(t): the output is half-wave antisymmetric. Its Fourier coefficient at harmonic n
   picks up a factor e^{−inπ} = (−1)ⁿ under the shift, while the antisymmetry multiplies it by −1. So (−1)ⁿ = −1 for every
   non-zero coefficient: n is odd.

3. **Ear.** The lab plays the Tune hard-tuned or natural, in random order; say which is which.

   *Solution.* The lab prints them. The hard-tuned voice holds each note dead steady and jumps between notes with no
   scoop; the natural one drifts slightly within notes and glides between them.

4. **Build.** Add a look-ahead to the compressor, so that no sample exceeds the threshold.

   *Where to look.* Delay the audio by L samples (a few milliseconds) and run the detector on the undelayed signal; take
   the maximum gain reduction needed over the next L samples (a sliding maximum) and smooth it with an attack no longer than
   L. With an infinite ratio, check that the delayed output never exceeds the threshold.

5. ★ **How small can a neural amplifier model be, indistinguishable at every setting and alias-free?**

   *Where the frontier is.* Record one amplifier across a grid of knob settings; train networks of decreasing size,
   conditioned on the knobs; test them blind at unseen settings, and measure their aliasing at 48 kHz against
   oversampled and ADAA versions.

## Sources

* U. Zölzer (ed.), *DAFX: Digital Audio Effects* (2nd ed., 2011); J. O. Smith, *Spectral Audio Signal Processing* (2011).
* M. Le Brun, "Digital waveshaping synthesis", *JAES* (1979); D. Arfib, "Digital synthesis of complex spectra by means of
  multiplication of nonlinear distorted sine waves", *JAES* (1979).
* J. D. Parker, V. Zavalishin and E. Le Bivic, "Reducing the aliasing of nonlinear waveshaping using continuous-time
  convolution", DAFx (2016); S. Bilbao, F. Esqueda, J. D. Parker and V. Välimäki, "Antiderivative antialiasing for
  memoryless nonlinearities", *IEEE Signal Processing Letters* (2017).
* D. Giannoulis, M. Massberg and J. D. Reiss, "Digital dynamic range compressor design: a tutorial and analysis", *JAES*
  (2012).
* J. L. Flanagan and R. M. Golden, "Phase vocoder", *Bell System Technical Journal* (1966); J. Laroche and M. Dolson,
  "Improved phase vocoder time-scale modification of audio", *IEEE Trans. Speech and Audio Processing* (1999);
  E. Moulines and F. Charpentier, "Pitch-synchronous waveform processing techniques for text-to-speech synthesis using
  diphones", *Speech Communication* (1990).
* A. de Cheveigné and H. Kawahara, "YIN, a fundamental frequency estimator for speech and music", *JASA* (2002);
  H. A. Hildebrand, "Pitch detection and intonation correction apparatus and method", US patent 5,973,252 (1999).
* H. Dudley, "Remaking speech", *JASA* (1939).
* A. Wright, E.-P. Damskägg and V. Välimäki, "Real-time black-box modelling with recurrent neural networks", DAFx
  (2019); A. Wright, E.-P. Damskägg, L. Juvela and V. Välimäki, "Real-time guitar amplifier emulation with deep
  learning", *Applied Sciences* (2020).
