# Music, Built: Part 49, Filters, Delay and Reverb

Part 49 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act IX, *Electric Sound*. In 1947 an engineer put a loudspeaker and a
microphone in his studio's tiled bathroom and sold the echo as art. In 1962 Manfred Schroeder at Bell Labs built a room out
of arithmetic: four comb filters and two all-passes. The linear and modulated effects here use delays, weighted sums and feedback, and this part
builds it: convolution, poles and zeros, equalizers, phase, combs and their moving relatives, a simulated room measured by
a sweep and checked against Sabine, Schroeder's reverberator, a feedback delay network, a steel plate by finite
differences and a spring. The tools are Monochord's (`explainer/music/monochord/effects.py`); every room, plate and spring
is simulated here, and no recorded impulse response is used.

* **A room made of arithmetic.** An ear question (the Tune in a simulated tiled room and in Schroeder's reverberator, both
  ringing 1.2 s: which is the arithmetic?); Putnam's bathroom, plates and springs; the plan.
* **1. Impulse responses and convolution.** One click says everything; convolution sample by sample (four samples against
  four taps); the simplest effect, an echo, heard (two taps, 180 ms); convolution at scale (the FFT); finite and infinite
  impulse responses.
* **2. Poles and zeros.** The one-pole low-pass (down 3 dB near 805 Hz); the z-plane; a pole near the circle rings, heard
  (a band-pass at 440 Hz with Q 2 and Q 50, poles at radius 0.986 and 0.9994); the biquad; stability.
* **3. Equalizers.** Five cookbook biquads drawn; an ear question (a groove through a high-pass, a 12 dB peak and a
  low-pass, shuffled: which was which?); analogue prototypes and the bilinear transform (our Butterworth matches SciPy's to
  rounding); the parametric equalizer; equalizing in practice.
* **4. Phase.** Timing, frequency by frequency; an ear question (a snare dry and through 60 all-passes: which was
  filtered?, every level unchanged to a millionth of a decibel); the all-passes' group delay (about 24 ms at the bottom, 0.07
  at the top); linear and minimum phase.
* **5. Combs, flangers, choruses and phasers.** One delay added back (notches every kilohertz, or peaks); noise in, a note
  out, heard (220 Hz from a 218-sample comb); a pad through a flanger, a chorus and a phaser, heard; a thumb on a reel; combs
  by accident.
* **6. The room's response.** The image-source method (Allen and Berkley); a tiled room's response (2.6 × 2.1 × 2.5 m, 5 %
  absorption; the direct sound at 4.3 ms, early reflections, the tail); how we hear a room (the precedence effect); the
  room heard; Schroeder's backward integration (RT60 1.22 s); its modes and Schroeder frequency (about 600 Hz); Sabine (1.28
  s) and Eyring (1.24 s) checked.
* **7. Measuring a room.** A click or a sweep?; Farina's exponential sweep, heard; the room recovered (error 19 dB below
  the response); distortion's harmonics arriving early; why this sweep.
* **8. Schroeder's reverberator.** Imitate the ear, not the room; four combs (29.7, 37.1, 41.1, 43.7 ms) and two all-passes
  (5.0 and 1.7 ms), set to 2 s and measuring 2.00; echo density (the room reaches noise-like density within tens of
  milliseconds, Schroeder's stays near 0.2); four snares through it and through a delay network, heard; Moorer's
  improvements.
* **9. Feedback delay networks.** Delays that talk to each other (Jot and Chaigne); eight lines and a Hadamard matrix; two
  impulse responses; reverberation time in octave bands (the room 1.8 s at 125 Hz to 1.3 at 4 kHz; the plate 2.6 to 1.0;
  the network nearly flat); a cathedral of eight delay lines, heard (4.2 s); reverbs in practice.
* **10. Plates and springs.** EMT's 140; the plate by finite differences (Kirchhoff's equation with Bilbao's
  frequency-dependent loss; 246 × 123 points, 8.1 mm apart; stability number 0.239); its response and spectrogram (the
  highest frequencies first); the plate heard; a spring as a loop of 80 all-passes, heard (1.3 s); plates and springs in
  practice.
* **11. Frontier: virtual analog and differentiable effects.** Circuits simulated; effects that learn (DDSP); rooms from the
  wave equation; ★ research problem: how small can a feedback delay network be and still pass for a given room?
* **Variation 49, recap and problems.** The Tune's first phrase dry, in the tiled room, on the plate, on the spring and in
  the cathedral; the ledger (1.2, 1.9, 1.3 and 4.2 s); what we found; five problems; where it comes back; in practice;
  references; Part 50.

## What is computed, and what is heard

`python -m videos.music.music49.compute` (about five minutes; the plate takes longest) fills `.cache/music49/`.

| Item | What it computes | Checked against |
|---|---|---|
| `conv`, `echo` | convolution by hand; a two-tap echo | `numpy.convolve` |
| `onepole`, `biquads`, `ring`, `eq` | one-pole and cookbook filters; poles and zeros; a ringing band-pass; an EQ quiz | the specs; SciPy's Butterworth (tests) |
| `phase` | 60 all-passes on a snare; their group delay | unit magnitude (tests) |
| `combs`, `mods` | feedforward and feedback combs; flanger, chorus, phaser | the comb's pitch (tests) |
| `room`, `bands` | image sources; energy decay; RT60, Sabine and Eyring; octave bands; Schroeder frequency | Eyring within 10 % (tests) |
| `sweep` | Farina's sweep, inverse filter, recovery and harmonic separation | the true response (tests) |
| `schroeder`, `cathedral` | Schroeder's reverberator; feedback delay networks; echo density | the set decay (tests) |
| `plate`, `spring` | a finite-difference plate; a dispersive spring loop | the stability bound (tests) |

Monochord's tools are held in `tests/music/test_effects.py`; this part's claims and clips in `tests/music/test_music49.py`.

**Sounds.** Part 7's piano, Part 40's drums and pad, a plucked bass, noise and clicks, through the filters, rooms and
reverberators of this part. Every reverb is labelled synthesized.

**What the models are, and are not.** *The room* is a perfect rectangle with frequency-independent absorption and a gentle
loss with distance, high-passed at 40 Hz as a measurement chain would be; real rooms scatter and absorb by frequency. *The
plate* is a simply supported Kirchhoff plate with two loss terms; a real EMT is suspended at its corners, damped by a pad,
and driven and picked up by transducers with their own responses. *The spring* is a stand-in for a coil's dispersion, not a
model of its physics. *The cathedral* is a delay network, not a building.

## Build

```bash
python -m videos.music.music49.compute                          # numbers and sounds (about five minutes)
EXPLAINER_TTS=silent python tools/build.py music49 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music49 --sync                         # the sound gates
python tools/dead_air.py renders/music49_480p.mp4 --sound music49  # no empty screen; no sound over a still one
python tools/lecture_length.py music49                          # 30 to 60 minutes, listening included
python tools/build.py music49                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 49                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A room is 10 by 8 by 4 m, its surfaces absorbing 20 %. What reverberation time does Sabine predict?

   *Solution.* V = 320 m³; S = 2(80 + 32 + 40) = 304 m². RT60 = 0.161 × 320 / (304 × 0.2) = 51.5 / 60.8 ≈ 0.85 s. (Eyring
   gives 0.161 × 320 / (−304 ln 0.8) ≈ 0.76 s.)

2. **Prove.** Prove that a first-order all-pass H(z) = (c + z⁻¹)/(1 + c z⁻¹) has |H| = 1 on the unit circle.

   *Solution.* On the circle z = e^{iω}, so z⁻¹ = e^{−iω}. Then H = (c + e^{−iω}) / (1 + c e^{−iω}) = e^{−iω}(c e^{iω} + 1) /
   (1 + c e^{−iω}). For real c, the numerator's bracket c e^{iω} + 1 is the complex conjugate of the denominator 1 + c
   e^{−iω}, so the two have the same modulus, and |e^{−iω}| = 1. Hence |H| = 1 at every frequency.

3. **Ear.** The lab plays a groove through a random filter; say which kind, and roughly where.

   *Solution.* The lab prints them. A low-pass sounds muffled (the cymbals dull), a high-pass thin (no kick, no bass), a
   peak honky or nasal around its frequency; 400 Hz sounds boxy, 1 kHz nasal, 3 kHz harsh.

4. **Build.** Fit a feedback delay network's line gains to match the tiled room's RT60.

   *Where to look.* Each line's gain is 10^(−3 D / (fs T60)): set `t60` in `fdn` to the room's 1.22 s and compare
   `rt60` of the two impulse responses, then in octave bands (`octave_rt60` in this part's compute): the room's bass rings
   longer, so make the one-pole damping in each loop a shelf that shortens the highs, and fit it.

5. ★ **How small can a feedback delay network be and still pass for a given room?**

   *Where the frontier is.* Measure rooms by sweep; fit networks of 4, 8, 16 lines to each room's decay in every band and
   its echo density, by hand or by gradient descent through a differentiable network; then run blind, level-matched
   listening tests on speech and music.

## Sources

* J. O. Smith, *Introduction to Digital Filters* (2007) and *Physical Audio Signal Processing* (2010); U. Zölzer (ed.),
  *DAFX: Digital Audio Effects* (2nd ed., 2011); R. Bristow-Johnson, "Cookbook formulae for audio EQ biquad filter
  coefficients"; S. Butterworth, "On the theory of filter amplifiers" (1930); G. Massenburg, "Parametric equalization"
  (AES, 1972).
* M. R. Schroeder, "Natural sounding artificial reverberation", *JAES* (1962), and "New method of measuring reverberation
  time", *JASA* (1965); J. A. Moorer, "About this reverberation business", *Computer Music Journal* (1979).
* J. B. Allen and D. A. Berkley, "Image method for efficiently simulating small-room acoustics", *JASA* (1979); W. C.
  Sabine, *Collected Papers on Acoustics* (1922); C. F. Eyring, "Reverberation time in 'dead' rooms", *JASA* (1930);
  H. Wallach, E. B. Newman and M. R. Rosenzweig, "The precedence effect in sound localization" (1949); H. Haas (1951).
* A. Farina, "Simultaneous measurement of impulse response and distortion with a swept-sine technique", AES (2000).
* J.-M. Jot and A. Chaigne, "Digital delay networks for designing artificial reverberators", AES (1991); J. S. Abel and
  P. Huang, "A simple, robust measure of reverberation echo density", AES (2006); V. Välimäki, J. D. Parker, L. Savioja,
  J. O. Smith and J. S. Abel, "Fifty years of artificial reverberation", *IEEE Trans. Audio, Speech, and Language
  Processing* (2012).
* S. Bilbao, *Numerical Sound Synthesis* (2009); EMT 140 documentation; V. Välimäki, J. Parker and J. S. Abel,
  "Parametric spring reverberation effect", *JAES* (2010).
* A. Fettweis, "Wave digital filters: theory and practice", *Proc. IEEE* (1986); J. Engel, L. Hantrakul, C. Gu and
  A. Roberts, "DDSP: differentiable digital signal processing", ICLR (2020).

## Interpretation limits

LTI convolution applies to fixed linear systems; moving modulation is time-varying, and nonlinear processors need other models. Pole stability assumes a causal rational system with uncancelled poles. Group delay is minus the phase derivative; linear phase does not eliminate ringing, and minimum phase is not universal among analog filters. EQ cutoffs depend on the source. Image sources and Sabine/Eyring use geometric and diffuse-field approximations. Orthogonal FDN mixing is a useful design choice, and finite integer delays still have common multiples. Echo density is a chosen Gaussian-reference statistic, not a complete perceptual equivalence test.
