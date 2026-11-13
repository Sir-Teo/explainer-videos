# Music, Built: Part 3, The Spectrum

Part 3 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). Parts 1 and 2 explained sounds by taking them apart into partials. This part makes
that idea exact: how to find the recipe of any wave, how a computer does it, what the ear seems to do with it, how
to watch a recipe change in time, the hard limit on doing so, and what the recipe leaves out. Every transform in it
is Monochord's own (`explainer/music/monochord/dsp/fourier.py`), checked against numpy and scipy; every sound is
computed in `compute.py`. Dates and attributions are the published ones, listed under Sources.

* **The Academy says no.** A square wave assembled from 1, 2, 3, 5, 10 and 30 pure tones; Fourier's memoir of 1807
  and Lagrange's objection (the quarrel of Part 1 again); three questions; the plan.
* **1. A sum of sines.** Why sines: the only shapes a resonant system leaves unchanged (a sine comes out a sine to
  10⁻¹⁴; a square does not). The coefficients as averages of the wave times each sine, computed for a square
  (4/πn, odd n only); partial sums and their shrinking average error (Dirichlet, 1829); Gibbs's overshoot (8.95%
  of the jump, for ever); the transform of a sound that happens once (lines merging into a continuous spectrum);
  an ear question (square or sawtooth?).
* **2. From a recipe to a machine.** The discrete Fourier transform and its N² cost; Cooley and Tukey's fast
  algorithm (1965; Gauss, 1805), written out and timed (four thousand samples: 609 ms against 0.5 ms here), equal
  to numpy's to 15 places; the spectrum of Part 1's pluck; a worked example (how long must you listen to separate
  two notes a semitone apart at 110 Hz? 0.15 s).
* **3. What the ear does with it.** Ohm's law of hearing (1843); Helmholtz's resonators (1863), each a bottle from
  Part 2; ten resonators on our string against the transform (within 0.8 dB on the strong partials); the string
  heard through one resonator; a worked example (a clarinet and six globes); Seebeck's objection.
* **4. The other half of the recipe.** Phase; two waves with one spectrum; at C5 they sound alike, at C2 they do
  not (an ear question); why: the ear hears phase where it cannot separate the partials.
* **5. Time and frequency together.** The short-time transform, built up column by column on the Tune's opening;
  how to read a spectrogram; ours against scipy's (to 15 places); a horn passing (Part 2), its partials sliding
  down together.
* **6. What a window costs.** Leakage; rectangular, Hann and Blackman windows: side lobes of −13, −31 and −58 dB,
  main lobes of 2, 4 and 6 bins (Harris's table); a tone 46 dB down that only a window reveals.
* **7. The limit.** One sound through a short and a long window; why (count the cycles); Δt·Δf ≥ 1/4π (Gabor,
  1946), measured for four shapes; a tone of 200, 50, 12 and 3 ms; an ear question (which pair is a semitone
  apart, at 5 ms and at 120 ms?).
* **8. A ruler for music.** Equal bins in hertz against equal steps in ratio; the constant-Q transform (Brown,
  1991), Q = 34 at a quarter-tone per bin; the Tune's opening on both rulers.
* **9. Sounds with no pitch.** White, pink and brown noise (measured slopes 0.0, −3.0, −6.0 dB per octave); why a
  noise spectrum must be averaged; noise in instruments, studios, and (Voss and Clarke, 1975) in music's own
  fluctuations.
* **10. More than the spectrum.** One pluck forwards, backwards (the same magnitude spectrum to 16 places) and
  with its attack removed: three different instruments; attack, brightness and their change in time; Schaeffer's
  cut bell (1948), Grey's timbre space (1977).
* **11. Frontier: sharper than the limit.** Reassignment (Kodera et al., 1976; Auger and Flandrin, 1995): the
  same energy in 2.6 times fewer cells; listeners who beat the uncertainty limit (Oppenheim and Magnasco, 2013);
  what a listening machine should start from. ★ research problem.
* **Variation 3, recap and problems.** The Tune assembled from pure tones, 1, 2, 3, 5, 8 and 16 partials phrase by
  phrase; the ledger; what we found; five problems; where it comes back; in practice; references; a tone with no
  fundamental, and Part 4.

## What is computed, and what is heard

`python -m videos.music.music3.compute` (about a minute) fills `.cache/music3/`.

| Item | What it computes | Checked against |
|---|---|---|
| `square` | partial sums of a square wave; its coefficients by projection; the overshoot at 10, 100, 1,000 terms; a sine and a square through a resonator; pulse trains | 4/πn; Gibbs's 8.95% |
| `dft` | our FFT against numpy's; multiplication counts; timings; the pluck's spectrum | (N/2) log₂N; partials at multiples of 130.8 Hz |
| `ohm` | ten resonators on the plucked string | each partial cut out of the full spectrum (0.8 dB) |
| `phase` | harmonic complexes with crest and with random phases at C2 and C5 | identical magnitudes (0.4 dB, 0.05 dB) |
| `stft` | the spectrogram of the Tune's opening; a passing horn | `scipy.signal.stft` (10⁻¹⁶) |
| `windows` | main and side lobes of four windows; a weak tone beside a strong one | Harris (1978), table 1 |
| `gabor` | Δt·Δf for a Gaussian, a Hann window, a decaying ring, a rectangle; tone bursts; one signal, two windows | 1/4π (the Gaussian exactly) |
| `cq` | a constant-Q transform of the Tune's opening | each note in the bin of its pitch (7 of 7) |
| `noise` | white, pink, brown: octave-band slopes; one frame against the mean of 351 | 0, −3.01, −6.02 dB per octave |
| `timbre` | a pluck forwards, backwards, without its attack: spectra, attack time, centroid, flux | reversal leaves every magnitude unchanged |
| `reassign` | an ordinary and a reassigned spectrogram of a sweep, a click and a tone | the ridge on the sweep's true frequency |
| `tune` | Variation 3, additive; brightness and partial count of each phrase | 1, 2, 3, 5, 8 partials counted from the sound |
| `missing` | a tone of partials 4 to 8 | no energy at the fundamental (−159 dB) |

The transforms are held against numpy and scipy in `tests/music/test_fourier.py`; this part's claims and clips in
`tests/music/test_music3.py`.

**Sounds.** Thirteen clips, labelled on screen. `synthesized`: sums of sines (the square wave, the phase pairs,
the tone bursts, the noises, the Variation, the tone with no fundamental) and Part 2's passing horn.
`physical model`: Part 1's plucked string, whole, through a resonator, backwards and with its attack removed.
There are no recordings.

**Two things the film simplifies.** "The ear's resonators" in chapter 4 are a picture, made exact in Part 4
(critical bands). The claim that phase is inaudible for the high note is the standard result for well-separated
partials (see Hartmann, ch. 6); it is not checked here by a listening test.

## Build

```bash
python -m videos.music.music3.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music3 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music3 --sync                         # the sound gates
python tools/dead_air.py renders/music3_480p.mp4 --sound music3   # no empty screen; no sound over a still one
python tools/lecture_length.py music3                          # 30 to 60 minutes, listening included
python tools/build.py music3                                   # 1080p30, narrated
python -m pytest -q tests/music                                # Monochord against its references; this part's claims and clips
python -m videos.music.labs 3                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **A sawtooth.** Find the Fourier coefficients of a sawtooth wave by Fourier's recipe. Which is the first
   harmonic more than 40 dB below the fundamental? Compare with a square wave.

   *Solution.* Take the sawtooth f(x) = (π − x)/2 on (0, 2π). Then bₙ = (1/π) ∫₀^{2π} f(x) sin nx dx = 1/n, by one
   integration by parts: every harmonic is present and falls as 1/n. Forty decibels is a factor of 100 in
   amplitude, so the first harmonic more than 40 dB down is the 101st. A square wave also falls as 1/n but has
   only odd harmonics; its 101st is likewise the first beyond 40 dB. (Both are slow: a corner in the wave's
   *slope*, as in the triangle wave or the plucked string of Part 1, gives 1/n², and reaches 40 dB at n = 11.)

2. **Backwards.** Show that playing a signal backwards replaces its transform X[k] by its complex conjugate (times
   a phase ramp), so that no magnitude changes. What happens to the phases?

   *Solution.* Let y[n] = x[N − 1 − n] for real x. Then Y[k] = Σ x[N−1−n] e^{−2πikn/N} = Σ x[m] e^{−2πik(N−1−m)/N}
   = e^{2πik/N} Σ x[m] e^{+2πikm/N} = e^{2πik/N} X[k]*. The factor in front has modulus one, so |Y[k]| = |X[k]|.
   Every phase changes sign (and gains the same linear ramp, which is only a shift in time). A spectrum that
   shows magnitudes cannot tell a sound from its reversal; the ear can, because the order of events in time is
   carried by the phases.

3. **Ear.** The lab (`python -m videos.music.labs 3`) plays three tones on one note. Put them in order of
   brightness, and say which one has only odd harmonics.

   *Solution.* The three are a sawtooth with 4 harmonics, a sawtooth with 16, and a square wave with 16 (odd
   only), in an order the lab prints after you have listened. Brightness follows the spectral centroid, which the
   lab also prints: the 4-harmonic tone is the dullest; the square is the hollow one, like the stopped pipe of
   Part 2.

4. **Build.** Write the inverse of `fourier.stft` by overlap and add, and show that a Hann window with a hop of a
   quarter gives back the sound exactly.

   *Solution sketch.* Inverse-transform each column, multiply it by the window again, and add it into the output
   at its place; divide by the sum of the squared windows at each sample. With the periodic Hann window and a hop
   of N/4, Σ w²(n − mH) = 3/2 for every n (the squared Hann window is 3/8 − ½cos + ⅛cos 2·, and the cosines cancel
   over four hops), so the division is by a constant and the reconstruction is exact to rounding (about 10⁻¹⁶)
   away from the first and last window. This is the engine of every phase vocoder, spectral effect and audio
   codec in Parts 50 and 58.

5. **★ Research.** Build a reassigned constant-Q transform, and measure how accurately it finds the onsets and
   pitches of Monochord's notes against an ordinary one.

   *Pointers.* Reassignment needs, for each constant-Q kernel, the same kernel multiplied by time and its
   derivative; see Auger and Flandrin (1995) for the general operators and Holighaus et al. (2013) for an
   invertible constant-Q framework. Score onsets by the F-measure within 50 ms and pitches by raw pitch accuracy,
   as in the MIREX evaluations; Monochord's notes give exact ground truth. Open questions: how reassignment
   behaves where partials of different notes share a bin, and whether a learned front end (Parts 61 to 64) ends
   up computing something similar.

## Sources

Books: W. M. Hartmann, *Signals, Sound, and Sensation* (1997); M. Müller, *Fundamentals of Music Processing* (2nd
ed., 2021), ch. 2; J. O. Smith, *Mathematics of the Discrete Fourier Transform* (2nd ed., 2007); H. von Helmholtz,
*On the Sensations of Tone* (1863; tr. Ellis), ch. 2–4; I. Grattan-Guinness, *Joseph Fourier, 1768–1830* (1972), for
the memoir of 1807 and its examiners (Lagrange, Laplace, Monge, Lacroix).

Papers: J. Fourier, *Théorie analytique de la chaleur* (1822); G. S. Ohm, "Über die Definition des Tones",
*Annalen der Physik* 59 (1843); A. Seebeck, *Annalen der Physik* 53 (1841) and 60 (1843); H. Wilbraham (1848) and
J. W. Gibbs, *Nature* 59 (1899), for the overshoot; J. W. Cooley and J. W. Tukey, "An algorithm for the machine
calculation of complex Fourier series", *Mathematics of Computation* 19 (1965) 297–301; M. T. Heideman, D. H.
Johnson and C. S. Burrus, "Gauss and the history of the fast Fourier transform", *IEEE ASSP Magazine* 1 (1984);
D. Gabor, "Theory of communication", *Journal of the IEE* 93 (1946) 429–457; W. Koenig, H. K. Dunn and L. Y. Lacy,
"The sound spectrograph", *JASA* 18 (1946); F. J. Harris, "On the use of windows for harmonic analysis with the
discrete Fourier transform", *Proceedings of the IEEE* 66 (1978) 51–83; J. C. Brown, "Calculation of a constant Q
spectral transform", *JASA* 89 (1991) 425–434; R. F. Voss and J. Clarke, "1/f noise in music and speech", *Nature*
258 (1975) 317–318; J. M. Grey, "Multidimensional perceptual scaling of musical timbres", *JASA* 61 (1977)
1270–1277; P. Schaeffer, *À la recherche d'une musique concrète* (1952), for the cut bell of 1948; K. Kodera,
C. de Villedary and R. Gendrin, *Physics of the Earth and Planetary Interiors* 12 (1976) 142–150, and *IEEE Trans.
ASSP* 26 (1978); F. Auger and P. Flandrin, "Improving the readability
of time-frequency and time-scale representations by the reassignment method", *IEEE Trans. Signal Processing* 43
(1995); J. N. Oppenheim and M. O. Magnasco, "Human time-frequency acuity beats the Fourier uncertainty principle",
*Physical Review Letters* 110 (2013) 044301.
