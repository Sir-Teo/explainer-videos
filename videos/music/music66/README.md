# Music, Built: Part 66, Generative Audio

Part 66 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act XI, *Listening Machines*. In 2016 a network wrote sound one sample at
a time, sixteen thousand decisions a second, and its piano noodled nowhere; eight years later a line of text returned a
finished song with a singer, and the record labels went to court. This part explains the ideas that closed the gap and
builds the smallest honest version of each: a network that writes samples, spectrograms and their way back to sound, a
codec's tokens and a language model over them, a diffusion model, a network that plays a synthesizer (DDSP), and the means
of judging and marking what such machines make. The tools are Monochord's (`explainer/music/monochord/genaudio.py`, with
*AI, Built*'s pocket transformer); every training sound was made by Monochord, so what each model learnt from is known
exactly. Results are reported as they are, including the failures.

* **Sixteen thousand decisions a second.** An ear question (Part 9's bowed string and a DDSP network's copy from its pitch
  and loudness: which is the network? the first, 6.7 dB from the string by spectrum); from WaveNet (2016) through Jukebox,
  MusicLM and MusicGen to the lawsuits of 2024; the plan.
* **1. Why raw audio is hard.** A second at three magnifications; the numbers (a CD second is 1.4 million bits; a song
  three million decisions); mu-law; equal steps against mu-law on a quiet phrase, heard (18 against 37 dB).
* **2. One sample at a time.** WaveNet; Monochord's network over the last 256 samples, trained on 49 s of the string model
  (about 4.3 bits a sample on its training notes, 8.4 on a phrase it never heard: worse than a blind guess on that held-out phrase; the loss gap alone does not prove literal memorization); half a second continued for one second, heard (278 s of computing); the lesson: split structure from detail.
* **3. Spectrograms and vocoders.** A phrase as a 64-band mel spectrogram; rebuilt by pseudo-inverse and Griffin-Lim,
  heard (15.4 dB away; the true spectrum with an invented phase, 3.8); 16, 64 and 256 bands, heard (20.6, 15.4 and
  8.3 dB); neural vocoders.
* **4. Tokens from a codec.** Vector quantization; SoundStream and EnCodec; Monochord's residual vector quantizer on log
  spectra (256-entry codebooks, 62.5 frames a second); an ear question (one, two and four tokens a frame, in order: they
  differ by only 0.2 dB, since one codebook holds most of one instrument's frames); bits against fidelity (0.5 kbit/s:
  4.3 dB; 2 kbit/s: 4.1; the phase floor 3.7).
* **5. Language models over sound.** AudioLM, MusicLM, MusicGen; MusicGen's delay pattern; a tune as tokens (44 of 256
  codewords in 240 frames); the pocket transformer (845,440 weights) on 152,965 tokens of 91 piano chorale tunes (about 41
  minutes), stopped at step 850 on tunes set aside; a tune it never learnt continued for six seconds, heard; its longest
  run copied token for token, 64 frames (one second).
* **6. Diffusion.** Adding and removing noise; a diffusion model of a bowed tone's 24-harmonic profile, conditioned on
  pitch, learnt from 300 notes; a profile drawn step by step; measured and drawn tones at three pitches, heard (each drawn
  profile 3.7 to 4.9 dB a harmonic from its nearest training profile); latent diffusion and flow matching.
* **7. Differentiable DSP.** Engel et al. (2020); Monochord's DDSP (24,249 weights: 40 harmonics and 16 noise bands set
  250 times a second), trained on the string model by a five-resolution spectral loss; the Tune's opening, never heard,
  resynthesized (6.0 dB away, against 28.8 for noise), heard; the controls it sets (each note starts bright and darkens:
  brightness against loudness, r = −0.73); a vibrato and a glide it never saw, heard; timbre transfer.
* **8. Singing and cloned voices.** Singing synthesis from rules to Vocaloid; one performance in three of Part 8's voices,
  heard; voice conversion and cloning; the law, for now (dated).
* **9. Judging generated sound.** The Fréchet distance (FAD); against the training strings: the training notes replayed
  6.5 (a copier scores best), another real phrase 15.7, DDSP 20.0, mel and Griffin-Lim 41.1, the sample-level network
  44.9, white noise 203; what the distance misses; listening tests for generators.
* **10. Watermarks and detection.** A spread-spectrum mark 35 dB down, standardized against 30 unused keys; an ear question
  (which carries it? the first: 31 against −0.8); through Part 58's coder 25.6; shifted 37 samples at 16 kHz (2.3 ms), −0.4, unless the
  detector searches shifts (73); in a room 1.1; ten wrong keys at most 3.4 (mean 0.7); detectors and provenance.
* **11. Frontier: data, consent and what is unsolved.** Training data; the courts (dated); what changed for musicians; form,
  control, attribution and evaluation; the smallest honest versions; ★ research problem: can training-data attribution for
  generated audio be made accurate enough to pay on?
* **Variation 66, recap and problems.** The Tune sung by Part 8's alto, its pitch and loudness driving the DDSP string an
  octave up, and its first phrase on the piano continued for five seconds by the token model; the ledger; what we found;
  five problems; where it comes back; in practice; references; Part 67.

## What is computed, and what is heard

`python -m videos.music.music66.compute` (an hour or so on a busy machine: five networks train, and the sample-level one
writes its second slowly) fills `.cache/music66/`.

| Item | What it computes | Checked against |
|---|---|---|
| `corpus`, `rates`, `zoom` | the string and piano corpora; mu-law against equal steps; a second magnified | by construction (tests) |
| `ar` | a sample-level network: bits per sample, a continuation | a phrase it never heard (tests) |
| `vocoder`, `melbands` | mel spectrograms back to sound | the original phrase (tests) |
| `codec`, `tokpic`, `tokenlm` | residual VQ at 1, 2, 4 stages; a transformer over tokens; copying | held-out tunes; the training tokens (tests) |
| `diffusion` | a diffusion model of harmonic profiles | the nearest training profile (tests) |
| `ddsp`, `vibrato`, `hook` | DDSP trained on the string model; resynthesis; new controls | a phrase it never heard (tests) |
| `fad` | Fréchet distances in Part 63's embedding | the training strings (tests) |
| `watermark` | marks at −25 and −35 dB through a coder, a shift and a room; wrong keys | unmarked audio and unused keys (tests) |
| `voices`, `tune66` | one performance in three voices; Variation 66 | — |

Monochord's tools are held in `tests/music/test_genaudio.py`; this part's claims and clips in `tests/music/test_music66.py`.

**Sounds.** Part 9's bowed string (training notes at random pitches, lengths and levels; the Tune held out), Part 38's piano
playing Part 65's chorale tunes (split by hymn tune), Part 8's voices. Everything is generated at 16 kHz and resampled to
48 kHz for the film.

**What the models are, and are not.** *The sample-level network* is two dense layers over 256 samples, not WaveNet's
dilated stack; it generalizes poorly on the held-out phrase. *The codec* has no learnt encoder or decoder: k-means codebooks on log spectra and
Griffin-Lim's phase, so reconstruction error includes both phase estimation and spectral quantization; the phase-only reference is not a universal bound. *The token model* has one codebook stream and forty minutes
of one instrument. *The diffusion model* draws a 24-number profile, not audio. *The DDSP model* learns one synthetic string
whose timbre does not depend on loudness, and has no reverb. *The Fréchet distance* uses Part 63's hand-made embedding
reduced to 8 directions, from few chunks, so its values are rough. *The watermark* is a textbook spread-spectrum mark; it
does not survive a room, and nothing here was tested against an attacker.

## Build

```bash
python -m videos.music.music66.compute                          # numbers and sounds (the networks train)
EXPLAINER_TTS=silent python tools/build.py music66 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music66 --sync                         # the sound gates
python tools/dead_air.py renders/music66_480p.mp4 --sound music66  # no empty screen; no sound over a still one
python tools/lecture_length.py music66                          # 30 to 60 minutes, listening included
python tools/build.py music66                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 66                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A codec has 8 codebooks of 1,024 entries at 75 frames a second. What is its bit rate, and how many tokens is
   a three-minute song?

   *Solution.* Each token is log₂ 1024 = 10 bits; 8 tokens a frame at 75 frames a second is 8 × 10 × 75 = 6,000 bit/s,
   6 kbit/s (EnCodec's setting at 6 kbit/s is exactly this). A three-minute song is 180 × 75 = 13,500 frames, so 108,000
   tokens: still long for a transformer, which is why the streams are delayed or modelled coarse first.

2. **Prove.** Show that if x_t = √ᾱ_t x₀ + √(1 − ᾱ_t) ε, predicting ε and predicting x₀ are equivalent.

   *Solution.* Given x_t and t, the relation is invertible in either unknown: x₀ = (x_t − √(1 − ᾱ_t) ε) / √ᾱ_t and
   ε = (x_t − √ᾱ_t x₀) / √(1 − ᾱ_t). A network that outputs ε̂ thereby outputs x̂₀, and conversely; their squared errors
   differ by the factor ᾱ_t / (1 − ᾱ_t), which is why the two parametrizations weight the steps differently in training
   while describing the same denoiser.

3. **Ear.** The lab plays a codec at 1 to 4 stages and marked and unmarked phrases; order and spot them, then check.

   *Solution.* The lab prints the order and which phrase was marked. On its synthetic melodies the stages differ by tenths of
   a decibel, as in the film, and the mark at −35 dB is found by the detector with a score above 20 while hard to hear.

4. **Build.** Give the DDSP synthesizer a learnt reverb (Part 49) and train it on the string in a room.

   *Where to look.* Append to `_torch_synth` a convolution with a learnable impulse response (a second or so of free
   parameters, initialized as decaying noise); render the training notes through Part 49's room; train as before and compare
   the spectral distance with and without the reverb, and the learnt response with the room's.

5. ★ **Can training-data attribution for generated audio be made accurate enough to pay on?**

   *Where the frontier is.* Render a corpus whose every recording is known, train token and diffusion models of several
   sizes, and for each output estimate which recordings it draws on (by influence functions, by embedding similarity, by
   retraining without candidates); score the estimates against the truth, which here is known.

## Sources

* A. van den Oord et al., "WaveNet: a generative model for raw audio" (2016); P. Dhariwal et al., "Jukebox" (2020).
* R. Kumar et al., "MelGAN" (NeurIPS, 2019); J. Kong, J. Kim and J. Bae, "HiFi-GAN" (NeurIPS, 2020).
* N. Zeghidour et al., "SoundStream: an end-to-end neural audio codec" (2021); A. Défossez et al., "High fidelity neural
  audio compression" (EnCodec, 2022).
* Z. Borsos et al., "AudioLM" (2022); A. Agostinelli et al., "MusicLM" (2023); J. Copet et al., "Simple and controllable
  music generation" (MusicGen, NeurIPS, 2023).
* J. Sohl-Dickstein et al., "Deep unsupervised learning using nonequilibrium thermodynamics" (ICML, 2015); J. Ho, A. Jain
  and P. Abbeel, "Denoising diffusion probabilistic models" (NeurIPS, 2020); Z. Evans et al., "Fast timing-conditioned
  latent audio diffusion" (Stable Audio, 2024); Y. Lipman et al., "Flow matching for generative modeling" (2022).
* J. Engel, L. Hantrakul, C. Gu and A. Roberts, "DDSP: differentiable digital signal processing" (ICLR, 2020).
* K. Kilgour et al., "Fréchet Audio Distance" (Interspeech, 2019); R. San Roman et al., "Proactive detection of voice
  cloning with localized watermarking" (AudioSeal, 2024).

Review qualifications: codec frames advance every 16 ms (62.5 Hz), not every sixteenth of a second. Exact matches and FAD-style distances are reference-dependent checks, not proofs of originality, causal attribution or perceptual quality. Current lawsuit and licensing status requires checking dated primary records. The formant-voice demonstration switches explicit synthesis parameters rather than implementing a trained voice converter.

Token payload rates count code indices only and exclude codebooks and metadata; the unquantized-spectrum row is a reconstruction reference, not a zero-rate codec.
