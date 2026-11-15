# Music, Built: Part 48, Digital Audio

Part 48 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act IX, *Electric Sound*. Why 44,100 samples a second? Because the
first digital recorders stored audio on video cassettes: three samples a line, 245 lines, 60 fields. Behind the accident
is a theorem that sounds impossible: a smooth wave can be recovered exactly from its samples. This part builds the
theorem as a sum of sincs, folds frequencies, takes the stair-step apart, measures six decibels a bit, dither, noise
shaping and jitter, and listens to one-bit audio. The tools are Monochord's (`explainer/music/monochord/digital.py`);
every converter is simulated. Differences near the threshold of hearing are played as residues (the difference from the
original, amplified by a stated gain), since this video's own soundtrack is lossy (SYLLABUS §3).

* **One bit or sixteen?** An ear question (the Tune stored as 16-bit samples and as one bit at 3.072 MHz: which is which?);
  the errors measured (the music at −20 dB, the one-bit version's error at −83, the 16-bit version's at −96); the
  questions; the plan.
* **1. Why 44,100?** Audio on videotape (the PCM adaptor; Sony's PCM-1600); the arithmetic (3 × 245 × 60 = 3 × 294 × 50
  = 44,100; colour NTSC's 44,056); the compact disc (1,411,200 bits a second); why that high and no higher.
* **2. The sampling theorem.** The statement; one sinc for every sample, their sum the signal (error 0.007 with 33
  samples); why it works (spectral copies and the ideal low-pass); a real filter's finitely many samples (largest error
  0.25 with 4, 0.06 with 16, 0.0006 with 64, 0.00004 with 128); Whittaker, Nyquist, Kotelnikov, Shannon.
* **3. Aliasing.** A fast wave and a slow one through the same samples; folding at 8 kHz sampling; three tones heard (3, 5
  and 7 kHz come out as 3, 3 and 1); an ear question (a sweep sampled with and without a filter: in which does the pitch
  turn round?); the anti-aliasing filter.
* **4. The stair-step myth.** The picture in every advertisement, and the smooth curve; where the stairs go; a 1 kHz
  tone through a zero-order hold at 44.1 kHz (images 33 dB down near 44 kHz, 39 near 88; droop of 3.2 dB at 20 kHz); the
  stairs heard, before and after the filter; how converters really do it.
* **5. Quantization.** Rounding to the nearest level; six decibels a bit, derived; the rule against the measurement
  (49.9 dB measured at 8 bits, 98.1 at 16; only at 2 bits does it fail, 8.9 against 13.8); where the floor sits; an ear
  question (the Tune at 4 bits, with and without dither: which had the noise added?).
* **6. Dither.** Noise as a cure; the error's average and spread for every input, under no, rectangular and triangular
  dither (TPDF: mean zero, variance a quarter of a step squared everywhere); a tone 0.4 of a step high, silent without
  dither and alive with it, heard; a piano note fading at 8 bits, its errors heard (+30 dB); the theory (Lipshitz,
  Wannamaker and Vanderkooy).
* **7. Noise shaping.** Error feedback (Cutler); the Tune's error spectra flat and shaped (below 4 kHz −26, −36, −44 dB;
  total −18, −15, −10); the two errors heard (+24 dB); shaping to the ear (Gerzon and Craven).
* **8. One bit.** A delta-sigma modulator (Inose, Yasuda and Murakami); 600 bits of a slow sine; one bit measured (9 dB
  and 15 dB per doubling of the rate for first and second order; 75 dB at 64 times); one bit at three speeds, heard (0, 17
  and 62 dB); one bit in practice (DSD at 2,822,400 bits a second).
* **9. Jitter and clocks.** A sample taken late; a 10 kHz sine with 0.1, 1, 10 and 100 ns of jitter (104, 84, 64 and 44
  dB, each within 0.1 dB of −20 log₁₀ 2πfσ); periodic jitter's sidebands (−70.1 dB measured and predicted); jitter in
  practice.
* **10. Resampling and the high-resolution debate.** Changing the rate (147 : 160); an ear question (a groove at 16 kHz
  and 48 kHz); Meyer and Moran (2007); Reiss (2016); testing it properly (blind, level-matched, enough trials: 12 of 16 by
  chance 3.8 per cent of the time); what to conclude.
* **11. Frontier: converter limits, and sampling below Nyquist.** What limits a converter (thermal noise; roughly 120 to
  130 dB, about 20 usable bits); finite rate of innovation and compressed sensing; ★ research problem: how far below
  Nyquist can music be sampled before listeners notice?
* **Variation 48, recap and problems.** The Tune's first phrase: the errors at 16 and 8 bits (+60 and +24 dB), without
  and with dither; the Tune at 4 bits both ways, at 1 bit, and as a one-bit stream at 64 times the rate; the ledger
  (77 dB at 16 bits, 29 at 8, 5 at 4; one bit at 64 times 62 dB); what we found; five problems; where it comes back; in
  practice; references; Part 49.

## What is computed, and what is heard

`python -m videos.music.music48.compute` (about a minute) fills `.cache/music48/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `speeds`, `deltasigma` | one-bit delta-sigma at 64 times, decimated; three speeds; SNR against oversampling | 9 and 15 dB an octave (tests) |
| `rate44` | the video arithmetic | 44,100 both ways (tests) |
| `sampling`, `stairstep`, `stairs` | sinc reconstruction and its truncation; the hold's images and droop | sinc(f/fs); error falls with taps (tests) |
| `tones`, `alias`, `rate` | folding at 8 kHz; a sweep with and without a filter; a groove at 16 kHz | the folding formula (tests) |
| `quant`, `moments`, `lowsine`, `fade` | SNR by word length; dither's moments; a sub-step sine; a fading note | 6.02 N + 1.76; LWV's moments (tests) |
| `shaping` | error spectra for orders 0, 1, 2 | noise moved up (tests) |
| `jitter`, `sidebands` | random and periodic jitter | −20 log₁₀ 2πfσ; 20 log₁₀ πfa (tests) |

Monochord's tools are held in `tests/music/test_digital.py`; this part's claims and clips in `tests/music/test_music48.py`.

**Sounds.** Part 7's piano and Part 40's drums (physical models), sine tones, and the converters of this part. Residues
are labelled with their gain on screen.

**What the models are, and are not.** *The converters* are ideal apart from the one effect under study: no analogue
noise, no filter ripple. *The decimation filter* for one-bit audio is an exact frequency-domain low-pass, as no real
converter's is. *The modulators* are first and second order; real converters use higher orders and a few bits.
*The SNR figures for the Tune* are against the Tune itself, at the level it was converted, not against full scale.

## Build

```bash
python -m videos.music.music48.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music48 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music48 --sync                         # the sound gates
python tools/dead_air.py renders/music48_480p.mp4 --sound music48  # no empty screen; no sound over a still one
python tools/lecture_length.py music48                          # 30 to 60 minutes, listening included
python tools/build.py music48                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 48                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A 30 kHz tone is sampled at 44.1 kHz with no filter. At what frequency is it heard?

   *Solution.* Fold it: 44.1 − 30 = 14.1 kHz. (30 kHz lies between the Nyquist frequency, 22.05 kHz, and the rate, so it
   folds once.)

2. **Prove.** Prove that triangular dither of two steps makes the error's mean and variance independent of the input.

   *Solution.* Take the step as 1. With dither d added before rounding, the total error is ε = Q(x + d) − x. Lipshitz,
   Wannamaker and Vanderkooy show that the m-th moment of ε is independent of x exactly when the dither's characteristic
   function φ(w) and its first m − 1 derivatives vanish at every w = 2πk, k ≠ 0. One uniform dither on [−½, ½] has
   φ(w) = sin(w/2)/(w/2), which vanishes at those points but whose derivative does not: the mean is freed, the variance is
   not. The sum of two independent uniforms has φ(w) = (sin(w/2)/(w/2))², which vanishes there to second order: the first
   two moments are freed. Then E[ε] = E[d] = 0, and E[ε²] = 1/12 (the rounding, now uniform and independent of the
   signal) + 1/6 (the dither's own variance) = 1/4 of a step squared, as chapter 6 measured.

3. **Ear.** The lab plays the Tune at 4 bits, with and without dither, in random order; say which is which.

   *Solution.* The lab prints them. Without dither the error follows the music: a gritty, buzzing distortion that changes
   with every note. With dither it is a steady hiss, and the piano sounds clean inside it.

4. **Build.** Write a third-order delta-sigma modulator and measure its gain per octave of oversampling.

   *Where to look.* Add a third integrator to `delta_sigma` (s3 += s2 − y) and measure `band_snr_db` at 16, 32 and 64
   times. Theory gives 21 dB an octave, (2L + 1) × 3 for order L; a naive third-order loop with a one-bit quantizer is
   unstable, so scale the input down or weight the integrators (the CIFB structure in Schreier and Temes).

5. ★ **How far below Nyquist can music be sampled before listeners notice?**

   *Where the frontier is.* Measure how sparse short frames of music are in good bases (MDCT, wavelets, learned
   dictionaries); sample at random below the Nyquist rate and recover by ℓ1 minimisation; then run blind, level-matched
   listening tests across sample counts and kinds of music.

## Sources

* K. C. Pohlmann, *Principles of Digital Audio* (6th ed., 2010); J. Watkinson, *The Art of Digital Audio* (3rd ed.,
  2001); the PCM adaptor's history (Sony PCM-1600, 1978; PCM-1610 and 1630 for CD mastering).
* E. T. Whittaker (1915); H. Nyquist, "Certain topics in telegraph transmission theory" (1928); V. A. Kotelnikov (1933);
  C. E. Shannon, "Communication in the presence of noise", *Proc. IRE* (1949); J. O. Smith, *Mathematics of the Discrete
  Fourier Transform* (2007).
* S. P. Lipshitz, R. A. Wannamaker and J. Vanderkooy, "Quantization and dither: a theoretical survey", *JAES* (1992);
  R. A. Wannamaker, "The theory of dithered quantization" (thesis, 2003); C. C. Cutler, US patent 2,927,962 (1960, filed
  1954); M. A. Gerzon and P. G. Craven, "Optimal noise shaping and dither of digital signals", AES (1989).
* H. Inose, Y. Yasuda and J. Murakami, "A telemetering system by code modulation: delta-sigma modulation" (1962);
  R. Schreier and G. C. Temes, *Understanding Delta-Sigma Data Converters* (2005); Sony and Philips, the Super Audio CD
  (1999).
* J. Dunn, "Jitter theory", Audio Precision technical notes; B. Brannon, "Sampled systems and the effects of clock phase
  noise and jitter", Analog Devices AN-756.
* E. B. Meyer and D. R. Moran, "Audibility of a CD-standard A/D/A loop inserted into high-resolution audio playback",
  *JAES* (2007); J. D. Reiss, "A meta-analysis of high resolution audio perceptual evaluation", *JAES* (2016).
* M. Vetterli, P. Marziliano and T. Blu, "Sampling signals with finite rate of innovation", *IEEE Trans. Signal
  Processing* (2002); E. J. Candès, J. Romberg and T. Tao (2006); D. L. Donoho, "Compressed sensing" (2006).
