# Music, Built: Part 51, Synthesis I: Oscillators and Filters

Part 51 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act IX, *Electric Sound*. One early large-scale electrical instrument weighed nearly two
hundred tons: Thaddeus Cahill's Telharmonium (1906) summed the near-sines of dynamos and sent them down telephone lines,
and it failed. Sixty years later Robert Moog's modules did the job by subtraction, and *Switched-On Bach* sold over a
million copies. This part builds a synthesizer: oscillators that do not alias, the Moog ladder run against its own circuit
equations, envelopes, modulation, wavetables, drums made of resonators, and a search that sets the knobs to imitate a
sound. The tools are Monochord's (`explainer/music/monochord/synth.py`); every sound is computed, and none is sampled.

* **Two hundred tons.** An ear question (forty sines set by hand, and a two-oscillator patch a search fitted to them:
  which is the original?); the two harmonic by harmonic (the patch 3.0 dB away on average, missing the bump near 1.1 kHz
  that a low-pass cannot make); the Telharmonium; Moog and *Switched-On Bach*; the plan.
* **1. Additive synthesis: dynamos and drawbars.** A sawtooth from 1, 2, 3, 5, 10 and 40 sines (Gibbs's 9 per cent);
  Fourier's list; the Hammond (1935): 91 tonewheels and nine drawbars; three registrations heard (8' alone, 888000000,
  all nine); the tempered drawbars (the fifths 2.0 cents flat, the third 13.7 sharp); what additive synthesis costs
  (Risset's trumpets, the Synclavier, the K5).
* **2. Subtractive synthesis.** Take away; four sources and their harmonics (sawtooth, square, triangle, a 25 % pulse);
  oscillator, filter, amplifier and voltage control (1 V an octave); a filter sweep heard without and with resonance, with
  its spectrogram; from cords to keyboards (Buchla, the Minimoog, the Prophet-5).
* **3. Why digital sawtooths alias.** The drop between samples; one high note's spectrum naive and band-limited (D7, ten
  true harmonics); aliasing against pitch over six octaves (naive 25.6 dB down at 110 Hz to 10.3 at 3.5 kHz, 3 dB worse an
  octave; PolyBLEP 14 to 16 dB better, 5 to 8 more at twice the rate; BLIT near 64; additive exact); PolyBLEP's two
  parabolas drawn; an ear question (a high phrase naive and PolyBLEP: which aliases?); BLIT, BLEP, PolyBLEP, wavetables.
* **4. The ladder filter.** Four poles and a loop (Moog's patent, filed 1966); the linear ladder in three lines,
  1/((1 + s/ωc)⁴ + k); five responses (a peak of 14.3 dB at k = 3.8); why k = 4 is the edge ((1 + j)⁴ = −4); resonance
  costs bass (1/(1 + k): −12.0 dB at k = 3); a bass line at three resonances, heard.
* **5. Running the circuit.** Huovilainen's equations (four capacitors charged through tanh); three ways to step them
  against a Runge–Kutta reference: forward steps (−11.9 dB at 48 kHz, 6 dB better per doubling), the half-sample
  correction (−14.4), and the trapezoid with Newton, zero-delay feedback (−37.2, 12 dB per doubling, about 2.5 times the
  cost a sample); an ear question (the circuit against its equations without tanh, driven hard); the harmonics (the 4th
  at +3.3 dB linear, −19.5 in the circuit); past k = 4 (oscillating within about 20 cents of the cutoff); the filter sings
  the Tune.
* **6. Envelopes and modulation.** ADSR (Ussachevsky); pluck, brass and pad; one patch with three envelopes, heard; LFOs
  (vibrato, tremolo, a wobble), heard; any source to any destination (keyboard tracking, velocity, FM ahead).
* **7. Pulse width, sync and unison.** Width as a knob (zeros at |sin πkw|/k); hard sync (the slave restarted by the
  master); PWM and sync heard; seven sawtooths over 36 cents (seven lines over 22 Hz at the 8th harmonic); a supersaw
  heard; perfect and imperfect (drift, virtual analogue).
* **8. Wavetables.** A wave from memory (PPG, 1981); eight stored cycles; a scan heard; three positions' spectra (the
  hollow middle); wavetables alias too (at C6, 18.3 dB down naive, 55.8 with only the 19 harmonics below 20 kHz: mipmaps);
  wavetables now.
* **9. Drum circuits.** A drum is a struck resonator (τ = 2Q/2πf); the kick from the circuit (52 Hz, Q 74: decay 0.453 s
  predicted, 0.454 measured; a chirp from 63 Hz to 52); snare, clap and hats; a kit of circuits heard; the ladder struck
  near self-oscillation as three toms (decays 0.25, 0.16 and 0.10 s; the low tom rising from 77 Hz to 79); circuits and
  samples (the 808, the 909's 6-bit cymbals).
* **10. Fitting a patch.** The inverse problem; a distance between two tones (levels at every multiple of half the note,
  floored at −60 dB); the search checked on a hidden patch (1400 Hz, k = 2, mix 0.5 found as 1365 Hz, 2, 0.5, 0.69 dB);
  the landscape; the hook's target slot by slot (the bump missed by up to 9 dB); an organ no setting can make (27 dB,
  heard); why fitting is hard.
* **11. Frontier: sound matching and differentiable synthesizers.** Learning the inverse (Yee-King, Fedden and d'Inverno;
  InverSynth; the Flow Synthesizer); differentiable synthesizers (DDSP; differentiable IIR filters); where the gradients
  go wrong (Turian and Henry); ★ research problem: can gradient descent fit an analogue patch to a recorded note as
  reliably as a search?
* **Variation 51, recap and problems.** The Tune switched on: a lead alone, then four monophonic tracks (lead, square bass,
  pulse arpeggio, unison pad) layered; the ledger (354 notes on four tracks; the lead's aliasing 34 dB below its
  harmonics, 18 if naive); what we found; five problems; where it comes back; in practice; references; Part 52.

## What is computed, and what is heard

`python -m videos.music.music51.compute` (about half a minute; the loops are compiled by numba when it is installed)
fills `.cache/music51/`.

| Item | What it computes | Checked against |
|---|---|---|
| `fit`, `hook` | a grid search over cutoff, feedback and mix; a hidden patch recovered; the hook's target; an organ | the hidden settings (tests) |
| `partials`, `organ`, `waves` | partial sums; tempered drawbars; four sources' harmonics | the tempered cents (tests) |
| `sweep`, `alias` | a resonant sweep and its spectrogram; aliasing for five oscillators over six octaves | 3 dB an octave; additive exact (tests) |
| `ladder`, `ladder3`, `drive`, `sing` | the linear response; three solvers against Runge–Kutta; saturation; self-oscillation | −12.04 dB at the cutoff; 6 and 12 dB a doubling (tests) |
| `env`, `mod`, `pwmsync`, `unison` | envelopes, LFOs, PWM, hard sync, unison | the pulse's zeros; sync's period (tests) |
| `table` | eight cycles, a scan, band-limited copies | the sine at position 0 (tests) |
| `drums`, `toms` | struck resonators, noise and squares; the ladder struck | τ = 2Q/2πf (tests) |
| `tune51` | four tracks, one patch each | the note count (tests) |

Monochord's tools are held in `tests/music/test_synth.py`; this part's claims and clips in `tests/music/test_music51.py`.

**Sounds.** Every sound in this part is synthesized here: oscillators, filters, envelopes, resonators and noise. The
Hammond is a computed model of its drawbars, and the hats are Part 40's six square waves.

**What the models are, and are not.** *The ladder* is Huovilainen's model: ideal tanh stages and capacitors, no thermal
noise, no mismatch between transistors, no change of tuning with temperature. *The Hammond* has no key click, no
leakage between tonewheels, no percussion and no rotating speaker. *The drums* are schematic circuits, not schematics of
the 808. *The patch fitting* matches steady spectra only.

## Build

```bash
python -m videos.music.music51.compute                          # numbers and sounds (about half a minute)
EXPLAINER_TTS=silent python tools/build.py music51 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music51 --sync                         # the sound gates
python tools/dead_air.py renders/music51_480p.mp4 --sound music51  # no empty screen; no sound over a still one
python tools/lecture_length.py music51                          # 30 to 60 minutes, listening included
python tools/build.py music51                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 51                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A ladder has its cutoff at 500 Hz and k = 2. What are its gains, in dB, at 0 Hz and at 500 Hz?

   *Solution.* At 0 Hz, H = 1/(1 + k) = 1/3: −9.5 dB. At the cutoff, (1 + j)⁴ = −4, so H = 1/(−4 + 2) and |H| = 1/2:
   −6.0 dB. (With no feedback the cutoff would be at −12.0 dB; the feedback has raised it 6 dB and cut the bass 9.5.)

2. **Prove.** Prove that a pulse of width w (high for a fraction w of each cycle) has harmonics of size proportional to
   |sin(πkw)|/k.

   *Solution.* Take the pulse p(t) = 1 for 0 ≤ t < w and 0 for w ≤ t < 1, period 1 (a constant offset changes only the
   zeroth coefficient). Its k-th complex Fourier coefficient is c_k = ∫₀^w e^{−2πikt} dt = (1 − e^{−2πikw})/(2πik) =
   e^{−πikw} (e^{πikw} − e^{−πikw})/(2πik) = e^{−πikw} sin(πkw)/(πk). So |c_k| = |sin(πkw)|/(πk), which is zero exactly
   when kw is a whole number.

3. **Ear.** The lab plays high notes on a naive or a PolyBLEP sawtooth, at random; say which is which.

   *Solution.* The lab prints them. The naive ones carry a faint, inharmonic halo, tones that do not belong to the note
   and sound rough or gritty; on a sustained note they can sound like a quiet second pitch.

4. **Build.** Add a peaking filter to the patch and refit the hook's target: how far does the distance fall?

   *Where to look.* Put Part 49's peaking biquad (`effects.biquad("peak", ...)`) after the ladder, with its frequency and
   gain as two more knobs, and widen `fit_patch`'s grid (or search them by a few rounds of coordinate descent). The target's
   bump is near 1.1 kHz and about 9 dB above what the ladder alone gives there.

5. ★ **Can gradient descent fit an analogue patch to a recorded note as reliably as a search?**

   *Where the frontier is.* Render notes from a two-oscillator patch with the ladder and two envelopes at hidden
   settings; fit them by grid search, by a network trained to invert the synthesizer, and by gradient descent through a
   differentiable ladder (the trapezoidal solver is smooth in its knobs) from many starts; map the success rate against
   pitch, resonance and the distance used (spectral, multi-resolution, or learned); then fit notes from real analogue
   instruments and judge the fits blind.

## Sources

* C. Roads, *The Computer Music Tutorial* (2nd ed., 2023); W. Pirkle, *Designing Software Synthesizer Plug-Ins in C++*
  (2nd ed., 2021); T. Pinch and F. Trocco, *Analog Days: The Invention and Impact of the Moog Synthesizer* (2002);
  R. Weidenaar, *Magic Music from the Telharmonium* (1995).
* T. Stilson and J. O. Smith, "Alias-free digital synthesis of classic analog waveforms", ICMC (1996), and "Analyzing the
  Moog VCF with considerations for digital implementation", ICMC (1996); E. Brandt, "Hard sync without aliasing", ICMC
  (2001); V. Välimäki and A. Huovilainen, "Oscillator and filter algorithms for virtual analog synthesis", *Computer Music
  Journal* (2006), and "Antialiasing oscillators in subtractive synthesis", *IEEE Signal Processing Magazine* (2007).
* R. A. Moog, US patent 3,475,623, "Electronic high-pass and low-pass filters employing the base to emitter diode
  resistance of bipolar transistors" (filed 1966, granted 1969); A. Huovilainen, "Non-linear digital implementation of the
  Moog ladder filter", DAFx (2004); V. Zavalishin, *The Art of VA Filter Design* (2012, rev. 2018).
* J.-C. Risset, *An Introductory Catalogue of Computer Synthesized Sounds* (Bell Laboratories, 1969).
* M. Yee-King, L. Fedden and M. d'Inverno, "Automatic programming of VST sound synthesizers using deep networks and other
  techniques", *IEEE Trans. Emerging Topics in Computational Intelligence* (2018); O. Barkan and others, "InverSynth: deep
  estimation of synthesizer parameter configurations from audio signals", *IEEE/ACM TASLP* (2019); P. Esling and others,
  "Flow synthesizer: universal audio synthesizer control with normalizing flows", *Applied Sciences* (2020).
* J. Engel, L. Hantrakul, C. Gu and A. Roberts, "DDSP: differentiable digital signal processing", ICLR (2020);
  B. Kuznetsov, J. D. Parker and F. Esqueda, "Differentiable IIR filters for machine learning applications", DAFx (2020);
  J. Turian and M. Henry, "I'm sorry for your loss: spectrally-based audio distances are bad at pitch" (2020); B. Hayes
  and others, "A review of differentiable digital signal processing for music and speech synthesis", *Frontiers in
  Signal Processing* (2024).
* C. Dodge and T. A. Jerse, *Computer Music: Synthesis, Composition, and Performance* (2nd ed., 1997); T. Holmes, *Electronic and Experimental Music* (6th ed., 2020), for the history from the Telharmonium on.

## Interpretation limits

The Telharmonium was not the first electrically generated tone device. Classic Hammond generators use geared shafts, and tempered-drawbar offsets refer to this simplified model. Phase audibility depends on harmonic resolution and envelopes. PolyBLEP reduces aliasing rather than eliminating it, and off-grid-energy metrics include windowing effects. The ladder’s k=4 boundary belongs to the ideal linear model; nonlinear oscillation needs a perturbation and amplitude limiting. Numerical comparisons use an oversampled reference rather than exact physical truth. Patch fitting is a finite sampled search with a chosen spectral metric, not a proof of perceptual identity or impossibility.
