# Music, Built: Part 64, Source Separation

Part 64 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act XI, *Listening Machines*. A mix is a sum; a listener hears the
voice, the bass and the drums in it at once, but for a machine un-mixing one channel is like un-baking a cake. This part
builds the separators in order of what they assume: centre cancellation and panning for stereo, independent component
analysis for clean two-channel mixtures, median filtering for harmonic against percussive, supervised non-negative
matrix factorization, the oracle masks that bound every masking method, Griffin and Lim's phase, and a small network;
then how separation is measured, and where the measure and the ear part company. The tools are Monochord's
(`explainer/music/monochord/mir/separate.py`); the music is Part 56's session, whose every stem Monochord mixed itself,
so every separation is scored exactly.

* **Un-baking a cake.** An ear question (a voice and a piano on one track, then the voice twice: which was separated? the
  first, 12 dB from the truth); a demo cassette lifted apart decades later; the plan.
* **1. The mixing model.** A mix as a sum; why separation needs assumptions; the test set (vocals, bass, drums, other, as in
  MUSDB18); the four stems heard alone and mixed (the voice a third of the energy).
* **2. Where things are panned.** Centre cancellation (left minus right, 11 dB quieter: the centred voice, bass and drums
  gone), heard; a panning index per bin (the piano at 2.7 dB SDR); the session's energy by panning index (a tall centre,
  broad shoulders).
* **3. Independent components.** Blind separation; what ICA sees; the session's voice and band as a cloud of samples,
  before and after; kurtosis along every direction (the voice 1.61, the microphones 1.34 and 0.82: the most non-Gaussian
  direction is the voice); dry and in a room, heard (correlation 0.99999, then 0.12).
* **4. Harmonic and percussive.** Lines and stripes; the harmonic mask; the split heard (tonal stems 7.8 dB, drums 1.0);
  the filter's length (63 frames: tonal 10.1, drums 3.4); short and long filters heard.
* **5. Factorization, again.** Templates for sources; the voice's combs and the drums' smears; the separated stems
  (drums 8.5 dB, vocals 7.7, bass 5.4, piano and guitar 5.2); how many templates (5.3 dB with one, 7.7 with six, 7.9 with
  twenty-four); the vocals heard.
* **6. Masks and their bounds.** Oracle masks; the vocals' ideal binary and ratio masks as pictures; the ceilings (vocals:
  NMF 7.7, binary 8.3, ratio 9.3, ratio with true phase 12.7; for the drums the binary mask wins); the oracles heard.
* **7. The phase problem.** A mask keeps the mixture's phase; Griffin-Lim's phase heard (−3.2 dB against 8.7 with the
  mixture's); its inconsistency falls from −4 to −20 dB while its SDR stays near −3; an ear question on the phase gap
  (9.3 against 12.7 dB); separating waveforms (Wave-U-Net, Demucs).
* **8. Networks that separate.** Monochord's separator (five frames of log spectrum in, the vocal mask out), trained on the
  middle phrases transposed five ways; training; heard (6.9 dB); every method compared (below NMF's 7.7: a network is only
  as good as its data); what a leak is worth (trained on stretches that repeat or include the test: 8.5 dB).
* **9. Measuring separation.** SDR, SI-SDR and BSS Eval; an ear question (two estimates at exactly 8.0 dB, one leaking the
  band, one with bins switched off); a perfect estimate changed (half as loud 6.0 dB; upside down −6.0; low-passed at
  2 kHz 36.6; a millisecond late −0.6), heard; what the numbers miss.
* **10. What separation is for.** Uses; an ear question on a remix (vocals up 6 dB, drums down 6, from separated stems: the
  first; 13.7 dB from the true remix, where the original mix is 7.0); rights; listeners.
* **11. Frontier: generative and query-based separation.** Separators that invent; sources named by a query; better
  metrics; ★ research problem.
* **Variation 64, recap and problems.** The session's Tune a cappella and as karaoke, from the network and from the true
  stems (the voice 6.9 dB, the karaoke 10.0); the ledger; what we found; five problems; where it comes back; in practice;
  references; Part 65.

## What is computed, and what is heard

`python -m videos.music.music64.compute` (about half an hour on a busy machine: the networks train) fills
`.cache/music64/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `meet` | a voice separated from a piano by NMF; the four stems heard | the stems as rendered (tests) |
| `pan`, `panmap` | centre cancellation; per-bin panning index; the energy at each index | the stage's pan angles (tests) |
| `ica`, `icascatter` | FastICA dry and in a room; the sample cloud; kurtosis by direction | the sources mixed (tests) |
| `hpss`, `hpsssweep`, `hpssknob` | median-filter masks; filter length and mask power | the true stems (tests) |
| `nmf`, `nmfrank` | supervised NMF with templates from other phrases; templates per source | the true stems (tests) |
| `oracle`, `maskimg`, `truephase` | ideal binary and ratio masks, with the true phase; mask pictures | by definition the bounds (tests) |
| `phase`, `glcurve` | the mixture's phase and Griffin-Lim's; inconsistency against SDR | the true vocals (tests) |
| `net`, `netleak` | the vocal-mask network, honest and leaked | the true vocals (tests) |
| `metrics`, `gain`, `remix` | equal-SDR estimates; SDR's blind spots; a remix from separated stems | the true stems (tests) |

Monochord's tools are held in `tests/music/test_separate.py`; this part's claims and clips in
`tests/music/test_music64.py`.

**Sounds.** Part 56's session (vocals by Part 8's voice, double-tracked; Part 38's piano, guitar and bass; Part 40's kit),
first two phrases for testing; its middle phrases for training; Part 56's stage for panning; a simulated room for ICA.

**What the models are, and are not.** *The session* is clean and dry, with stems that never bleed into each other's
microphones; real multitracks bleed. *The test* uses the Tune's opening; its last two phrases repeat the opening note for
note, so no method here learns from them (the leaked network in Chapter 8 shows why). *The network* is two hidden layers on
five frames, trained on seconds of one band; Demucs and its successors train on hundreds of songs, with waveform branches
and attention. *SDR* is computed directly as the energy ratio, not by BSS Eval's projections, so gains count as error.

## Build

```bash
python -m videos.music.music64.compute                          # numbers and sounds (the networks train)
EXPLAINER_TTS=silent python tools/build.py music64 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music64 --sync                         # the sound gates
python tools/dead_air.py renders/music64_480p.mp4 --sound music64  # no empty screen; no sound over a still one
python tools/lecture_length.py music64                          # 30 to 60 minutes, listening included
python tools/build.py music64                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 64                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A source is panned at θ = 70° by a sine-cosine law. What is its panning index, and how much of it survives
   L − R?

   *Solution.* Here θ is measured as in Chapter 2, with 45° the centre and L = sin θ · s, R = cos θ · s. At 70°,
   sin θ = 0.940 and cos θ = 0.342, so the index (|L| − |R|) / (|L| + |R|) = 0.598 / 1.282 ≈ 0.47. L − R = 0.598 s; against
   its level in the mid channel (L + R)/2 = 0.641 s, that is 0.6 dB quieter: almost all of it survives, where a centred
   source would vanish.

2. **Prove.** Show that the ideal ratio mask minimizes the squared error of a masked estimate when the sources' phases agree
   in every bin.

   *Solution.* If every source in a bin has the phase of the mixture, then S_j = a_j e^{iφ} and X = (Σ a_k) e^{iφ}, with
   a_k ≥ 0. The error of M X is |a_j − M Σ a_k|², minimized over real M at M = a_j / Σ a_k, the ratio mask, with zero error.
   When phases differ, |X| < Σ|S_k| and no real mask reaches zero: the least-squares mask is then Re(S_j X*) / |X|², the
   phase-sensitive mask, and the remaining error is the phase gap of Chapter 7.

3. **Ear.** The lab plays separations at several SDRs, some by leakage and some by artifacts; rank them, then check.

   *Solution.* The lab prints each separation's SDR. Most listeners rank leakage of a quiet other instrument above musical
   noise at the same SDR; compare your ranking with the numbers and note where they disagree.

4. **Build.** Train the network on all four stems at once, and compare its drums with the median filter's.

   *Where to look.* Replace the sigmoid output with four masks per bin passed through a softmax, so they share each bin;
   train on the same transposed phrases with the four true ratio masks as targets; score each stem's SDR against the
   median filter's percussive half at its best length (3.4 dB) and NMF's (8.5).

5. ★ **Can a metric rank separators as listeners do, including generative ones that invent?**

   *Where the frontier is.* Render mixtures whose stems are known across many instruments and rooms, separate them with
   masking and generative methods, collect MUSHRA-style ratings, and test which measures (SDR, SI-SDR, perceptual and
   learned ones) predict the ratings, and whether any notices invention.

## Sources

* E. Vincent, T. Virtanen and S. Gannot (eds.), *Audio Source Separation and Speech Enhancement* (2018); Z. Rafii et al.,
  "An overview of lead and accompaniment separation in music", *IEEE/ACM TASLP* (2018); A. S. Bregman, *Auditory Scene
  Analysis* (1990).
* C. Avendano, "Frequency-domain source identification and manipulation in stereo mixes" (WASPAA, 2003); A. Hyvärinen,
  J. Karhunen and E. Oja, *Independent Component Analysis* (2001); D. FitzGerald, "Harmonic/percussive separation using
  median filtering" (DAFx, 2010).
* P. Smaragdis, "Non-negative matrix factor deconvolution" (ICA, 2004); T. Virtanen, "Monaural sound source separation by
  nonnegative matrix factorization with temporal continuity and sparseness criteria", *IEEE TASLP* (2007).
* D. W. Griffin and J. S. Lim, "Signal estimation from modified short-time Fourier transform", *IEEE Trans. ASSP* (1984);
  D. Stoller, S. Ewert and S. Dixon, "Wave-U-Net" (ISMIR, 2018); A. Défossez et al., "Music source separation in the
  waveform domain" (2019); Z. Rafii et al., "The MUSDB18 corpus for music separation" (2017).
* E. Vincent, R. Gribonval and C. Févotte, "Performance measurement in blind audio source separation", *IEEE TASLP* (2006);
  J. Le Roux et al., "SDR: half-baked or well done?" (ICASSP, 2019).
