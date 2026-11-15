# Music, Built: Part 52, Synthesis II: FM, Grains and Physical Models

Part 52 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth part of Act IX, *Electric Sound*. In 1967 John Chowning turned a vibrato up
until it was faster than the note itself and heard bells. The mathematics is a Bessel function per sideband, the patent
made Stanford a fortune, and the DX7 (1983) put the sound on a decade's records. This part builds FM, then the other ways
out of the oscillator: grains, spectral models, samplers, and the physical models (Karplus–Strong tuned, digital
waveguides, modes), each checked against Part 1's and Part 7's finite-difference string. The tools are Monochord's
(`explainer/music/monochord/synth2.py`); every sound is computed.

* **Bells from a vibrato.** An ear question (Part 9's bell from its eight measured partials, or two sine oscillators in the
  ratio 1 : 1.4: which used two?); the two spectra; Chowning, Stanford's patent and the DX7; the plan.
* **1. Frequency modulation.** A vibrato speeding up from 4 to 220 Hz, heard with its spectrogram; one line of
  mathematics (lines at fc + k fm sized J_k(I)); predicted and measured (fc 1000, fm 250, I = 2: agreement to 2.5
  millionths); Bessel's functions (the carrier vanishes at 2.405); the index swept from 0 to 8, heard; Carson's rule.
* **2. Ratios, indices and Chowning's instruments.** Four ratios and their series (1 : 2 odd; 5 : 7 a bell; 2 : 7 sparse);
  sidebands below zero fold with a sign; three ratios heard; brass, bell and drum (1973); the three heard; FM against the
  filter.
* **3. Operators and algorithms.** Operators; four algorithms; an operator modulating itself (feedback 1.5: the 2nd, 3rd
  and 4th harmonics at −7.1, −11.2, −14.3 dB, near a sawtooth's); an electric piano, a bass and a bell, heard; the sound of
  a decade (155 parameters a voice).
* **4. Granular synthesis.** Gabor's acoustical quanta; three grains (5, 20 and 80 ms: 176, 43 and 10 Hz wide; length
  times width about 0.85); a five-knob engine; Part 8's voice frozen, stretched four times, raised a fifth and scattered
  into a cloud, heard; the cloud grain by grain; grains at work.
* **5. Spectral models.** Sines and the rest (McAulay and Quatieri; Serra and Smith); Part 7's piano note partial by partial;
  its stretched partials (the 24th 171 cents sharp; B = 3.8 × 10⁻⁴); the note as sines, residual (−10 dB in the first
  80 ms, −77 after 0.3 s) and made harmonic, heard; what the model is for.
* **6. Samplers.** The Mellotron to Akai; one recording over four octaves against the piano computed there, heard
  (8.4 s and 0.53 s long); why one recording is not enough; multisampling and velocity layers; what brute force costs
  (about 4.1 GB for one multisampled piano).
* **7. Karplus–Strong, tuned.** The loop; tuning note by note (rounded: up to 33 cents out at C7; with Jaffe and Smith's
  all-pass: within 0.6 of a cent); the all-pass; in and out of tune, heard; more from one loop.
* **8. Digital waveguides.** d'Alembert's two rails; against the finite-difference string (equal to 3 × 10⁻¹⁴); a clarinet
  as a waveguide (McIntyre, Schumacher and Woodhouse); its threshold (between 0.60 and 0.65 of the reed's closing
  pressure, shut again above 1.0) and odd harmonics; a crescendo and the Tune, heard; waveguides at work (the VL1).
* **9. Modal synthesis.** An instrument as its modes; the stiff string as modes; where the bead simulation errs (its
  partials flat, 16 cents by the 24th; −21 dB overall); an ear question (modes or beads?); modes at work.
* **10. What each method costs and controls.** One second of sound timed for nine methods; what a player gets to turn;
  which method for which job.
* **11. Frontier: neural and differentiable physical models.** DDX7, differentiable modal resonators, DDSP-Piano; black,
  grey and white boxes; ★ research problem: how few parameters can match an instrument across its range, including
  playing it never heard?
* **Variation 52, recap and problems.** The Tune on FM keys and bells, dissolved into grains and back; the ledger (FM's
  lines within 0.000002 of Bessel's; 2,793 grains in ten seconds); what we found; five problems; where it comes back; in
  practice; references; Part 53.

## What is computed, and what is heard

`python -m videos.music.music52.compute` (under a minute; the loops are compiled by numba when it is installed) fills
`.cache/music52/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `vib2fm`, `bessel`, `ratios`, `chowning` | FM tones, lines, sweeps; Chowning's three instruments | Bessel's functions (tests) |
| `dx` | four-operator patches; feedback's harmonics | the simple FM formula (tests) |
| `gabor`, `grains` | Gaussian grains; a granular engine on Part 8's voice | Gabor's uncertainty (tests) |
| `spectral`, `sampler` | partial tracks, inharmonicity, residual; one sample over four octaves | synthetic partials (tests) |
| `ks`, `waveguide`, `clarinet`, `modal` | tuned Karplus–Strong; waveguides; a reed; modes | the finite-difference string (tests) |
| `costs`, `tune52` | timings; Variation 52 | — |

Monochord's tools are held in `tests/music/test_synth2.py`; this part's claims and clips in `tests/music/test_music52.py`.

**Sounds.** FM, granular and spectral sounds are labelled synthesized; Part 7's piano, Part 8's voice, Part 9's bell,
Karplus–Strong strings, the waveguide clarinet and the modal string are labelled physical model.

**What the models are, and are not.** *The clarinet* has a reed with no mass (a memoryless curve), a cylindrical bore of
whole samples at four times the rate, and a one-pole bell; no tone holes, no register key. *The spectral model* tracks a
single note's harmonic partials, not arbitrary peaks. *The costs* are this part's Python and numba on one computer; they
rank methods only roughly.

## Build

```bash
python -m videos.music.music52.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music52 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music52 --sync                         # the sound gates
python tools/dead_air.py renders/music52_480p.mp4 --sound music52  # no empty screen; no sound over a still one
python tools/lecture_length.py music52                          # 30 to 60 minutes, listening included
python tools/build.py music52                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 52                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A carrier at 400 Hz is modulated at 100 Hz with index 1. Using Carson's rule, how wide is the spectrum,
   and which lines does it hold?

   *Solution.* B ≈ 2(I + 1) fm = 2 × 2 × 100 = 400 Hz, so from about 200 to 600 Hz: the lines at 200, 300, 400, 500 and
   600 Hz (k = −2 … 2), with sizes J₂(1) = 0.11, J₁(1) = 0.44, J₀(1) = 0.77, 0.44, 0.11. The next pair, J₃(1) = 0.02, is
   below 2 per cent.

2. **Prove.** Prove that the energy of an FM tone does not depend on its index: Σ J_k(I)² = 1.

   *Solution.* The generating function of the Bessel functions is e^{iI sin θ} = Σ_k J_k(I) e^{ikθ}. Its modulus is 1 for
   every θ, so by Parseval's theorem over one period, 1 = (1/2π) ∫|e^{iI sin θ}|² dθ = Σ_k |J_k(I)|². Equivalently, FM
   only moves the carrier's phase, and a sine's power does not depend on its phase.

3. **Ear.** The lab plays FM tones at random ratios; say which are harmonic and which are bells.

   *Solution.* The lab prints them. Whole-number ratios (1, 2, 3) give a clear pitch; irrational or awkward ratios (√2,
   1.4, 2.76) give lines that are harmonics of a very low fundamental or of none, heard as a clang.

4. **Build.** Add a bow to the waveguide string (a friction curve at the contact point) and find its threshold.

   *Where to look.* Split each rail at the bow point; there the string's velocity v and the bow's velocity v_b give a
   friction force from a curve such as μ(v − v_b) = μ_d + (μ_s − μ_d)/(1 + |v − v_b|/v₀) (Smith; Woodhouse). Solve the
   junction each sample (the force and the velocity together), inject the force into both rails, and sweep bow force and
   speed: Part 7's Schelleng wedge should appear.

5. ★ **How few parameters can match an instrument across its range, including playing it never heard?**

   *Where the frontier is.* Record an instrument across its range and dynamics, hold out notes and playing styles, fit a
   sampler, a differentiable FM engine (DDX7), a modal model and a waveguide to the rest, and compare blind on the
   held-out playing against model size.

## Sources

* J. M. Chowning, "The synthesis of complex audio spectra by means of frequency modulation", *JAES* (1973);
  J. Chowning and D. Bristow, *FM Theory and Applications* (1986); J. R. Carson, "Notes on the theory of modulation",
  *Proc. IRE* (1922).
* D. Gabor, "Theory of communication" (1946) and "Acoustical quanta and the theory of hearing", *Nature* (1947);
  C. Roads, *Microsound* (2001); B. Truax, "Real-time granular synthesis with a digital signal processor", *CMJ* (1988).
* R. J. McAulay and T. F. Quatieri, "Speech analysis/synthesis based on a sinusoidal representation", *IEEE TASSP*
  (1986); X. Serra and J. O. Smith, "Spectral modeling synthesis", *CMJ* (1990).
* K. Karplus and A. Strong, "Digital synthesis of plucked-string and drum timbres", *CMJ* (1983); D. A. Jaffe and
  J. O. Smith, "Extensions of the Karplus-Strong plucked-string algorithm", *CMJ* (1983).
* J. O. Smith, "Physical modeling using digital waveguides", *CMJ* (1992), and *Physical Audio Signal Processing* (2010);
  M. E. McIntyre, R. T. Schumacher and J. Woodhouse, "On the oscillations of musical instruments", *JASA* (1983);
  P. R. Cook and G. P. Scavone, the Synthesis ToolKit (1999 onward).
* J.-M. Adrien, "The missing link: modal synthesis", in *Representations of Musical Signals* (1991); K. van den Doel and
  D. K. Pai, "The sounds of physical shapes", *Presence* (1998); S. Bilbao, *Numerical Sound Synthesis* (2009).
* F. Caspe, A. McPherson and M. Sandler, "DDX7: differentiable FM synthesis of musical instrument sounds", ISMIR (2022);
  R. Diaz, B. Hayes, C. Saitis, G. Fazekas and M. Sandler, "Rigid-body sound synthesis with differentiable modal
  resonators", ICASSP (2023); L. Renault, R. Mignot and A. Roebel, "DDSP-Piano: a neural sound synthesizer informed by
  instrument knowledge", *JAES* (2023).
