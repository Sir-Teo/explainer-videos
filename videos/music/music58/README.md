# Music, Built: Part 58, Compression for the Ear

Part 58 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth part of Act X, *The Studio and the Stage*. The engineer tuning the first MP3
encoder tested it on an unaccompanied voice, Suzanne Vega's "Tom's Diner", because on that voice it sounded dreadful.
Years of research into what the ear cannot hear produced a file a tenth the size, and a few years later those files helped disrupt
the record industry. This part builds the two kinds of compression: a lossless coder that rebuilds every bit,
and a perceptual coder on Part 4's masking, with the MDCT, rate control, window sizes and mid-side stereo; then it asks how
controlled tests can establish limits on codec discrimination. The tools are Monochord's (`explainer/music/monochord/codec.py`); every
codec heard here is Monochord's own, not MP3, AAC or Opus.

* **A voice that sounded dreadful.** An ear question (the Tune sung alone, through our coder at 64 kbit/s, as recorded, and
  at 16 kbit/s: which was the original? the second; the first targets 64 kbit/s and estimates about 60 kbit/s on this signal); *Tom's Diner* and the MP3; two
  kinds of compression; the plan.
* **1. Entropy and lossless coding.** Entropy; prediction; how much prediction saves (the voice from 13.0 to 3.5 bits a
  sample at order 4, the mix to 9.5 at order 2); Rice codes; a lossless coder, round trip (voice 23 %, mix 55 %, every
  sample exact); better predictors.
* **2. What the ear cannot hear.** A masking model; how far masking reaches (Schroeder's spreading, Johnston's offsets);
  one frame's mask; an ear question (white noise and mask-shaped noise of the same power, 10 dB under the music: in which
  can you hear the noise? the white); masking in time.
* **3. The MDCT.** Why a special transform; the modified discrete cosine transform; one frame's aliases; the aliases cancel
  (to 7 × 10⁻¹⁵, and 2 × 10⁻¹³ on the mix); aliases heard, from every other frame; a bank of filters.
* **4. A perceptual coder.** Monochord's coder; bit allocation by step size; rate control; the voice and the mix at five
  rates (the mix 19 dB under the mask at 128 kbit/s, 3 at 64, 17 over at 16); five rates heard.
* **5. Window switching and pre-echo.** Time against frequency; 30 ms before a hit (at equal noise-to-mask, long blocks
  leave 5.5 dB more noise before each hit, and short blocks cost three times the bits); an ear question (which had a swish
  before each hit? the long blocks); window switching.
* **6. Stereo coding.** Mid and side (the side 11 dB under the mid); the same 64 kbit/s spent two ways (about 4 dB better
  per channel as mid-side); heard; intensity and parametric stereo.
* **7. MP3, AAC and Opus.** Five codecs; MP3's hybrid filter bank; AAC; Opus; the file that broke a business.
* **8. Listening tests.** An ABX trial (X was B); counting right answers (12 of 16, 59 of 100); the power of an ABX test (a
  listener right 70 % of the time passes 16 trials 45 % of the time); BS.1116 and MUSHRA.
* **9. Generations.** Transcoding; five generations (SNR from 8.5 dB to about 2); heard; in practice.
* **10. Vectors and residuals.** Vector quantization; residual vector quantization; stage by stage (5 dB less error per
  stage); heard; neural codecs.
* **11. Frontier: neural codecs and learned metrics.** What neural codecs change; learned metrics; ★ research problem: can a
  learned metric predict listeners' ratings for a kind of codec that did not exist when it was trained?
* **Variation 58, recap and problems.** The Tune by our session at 128, 64, 32, 24 and 16 kbit/s, then what the 32 kbit/s
  version discarded, alone; the ledger; what we found; five problems; where it comes back; in practice; references; Part 59.

## What is computed, and what is heard

`python -m videos.music.music58.compute` (about five minutes; the vector quantizer's training takes the longest) fills
`.cache/music58/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `rates`, `tune58` | the perceptual coder at several rates on the voice and the mix | the bit rate met; margins ordered (tests) |
| `lossless` | entropy by predictor order; a Rice-coded lossless coder | bit-exact decoding (tests) |
| `masking` | one frame's mask; white and mask-shaped noise | a tone's mask (tests) |
| `mdct` | basis, aliases, overlap-add | reconstruction to 1e-11 (tests) |
| `preecho` | long and short blocks at equal noise-to-mask | the pre-echo ordering (tests) |
| `stereo` | left/right against mid/side at one rate | SNR (tests) |
| `abx` | thresholds and power of ABX tests; one trial | the binomial (tests) |
| `transcode`, `rvq` | five generations; residual vector quantization | errors fall stage by stage (tests) |

Monochord's tools are held in `tests/music/test_codec.py`; this part's claims and clips in `tests/music/test_music58.py`.

**Sounds.** Part 8's voice singing the Tune alone, Part 56's session (mono and stereo), Part 40's clave as castanets, all
through Monochord's coders.

**What the models are, and are not.** *The perceptual coder* is mono, with one block size per run, no bit reservoir, no
Huffman tables (Rice codes per band instead), a nominal six-bit scale-factor cost and a low-pass by target rate. Scale factors are not actually quantized and serialized, so these are estimated model rates, not measured complete files. It is a teaching coder, and
its rates are not comparable one for one with MP3's or AAC's. *The masking model* is Johnston's (1988) in outline: Bark
bands, Schroeder's spreading, a tonality offset from the spectral flatness, and Terhardt's threshold in quiet (capped at
60 dB SPL), with a full-scale sine taken to play at 96 dB SPL. *The lossless coder* uses Shorten's fixed predictors, not
FLAC's fitted ones. *The vector quantizer* codes normalized MDCT vectors, not learned features.

## Build

```bash
python -m videos.music.music58.compute                          # numbers and sounds (about five minutes)
EXPLAINER_TTS=silent python tools/build.py music58 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music58 --sync                         # the sound gates
python tools/dead_air.py renders/music58_480p.mp4 --sound music58  # no empty screen; no sound over a still one
python tools/lecture_length.py music58                          # 30 to 60 minutes, listening included
python tools/build.py music58                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 58                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A band allows noise of power 10⁻⁴ per coefficient. What step size puts the noise exactly there, and 6 dB
   under?

   *Solution.* A uniform quantizer's noise is Δ²/12, so Δ = √(12 × 10⁻⁴) = 0.0346; 6 dB under halves the step (power down
   by 4): Δ = 0.0173.

2. **Prove.** Show that the MDCT's window must satisfy w²ₙ + w²ₙ₊ₙ = 1 for the aliases to cancel.

   *Solution.* In the overlap between frame i's second half and frame i + 1's first half, windowing twice and adding
   gives the signal times wₙ₊ₙ² + wₙ², plus two aliases (time-reversed copies of the overlap) with opposite signs, each
   multiplied by a product of window values; for a window symmetric about its centre (w at n equal to w at 2N − 1 − n)
   the two products are equal and the aliases cancel. What remains is the signal times wₙ² + wₙ₊ₙ², so it is recovered
   exactly if and only if wₙ² + wₙ₊ₙ² = 1: the Princen–Bradley condition, which the sine window meets because
   sin² + cos² = 1.

3. **Ear.** The lab codes a sound at random rates and plays them after the original; order them by bit rate.

   *Solution.* The lab prints the order. Listen for the top of the spectrum first (low rates low-pass it), then for a
   watery roughness on the sustained notes.

4. **Build.** Add window switching to the coder: short blocks when an attack is detected, with start and stop windows.

   *Where to look.* Detect attacks from the energy of short sub-blocks (a jump of 10 dB or more); in those frames use eight
   MDCTs of N/8 with their own scale factors; between long and short frames use asymmetric start and stop windows whose
   halves still satisfy the Princen–Bradley condition with their neighbours; check reconstruction first, then pre-echo.

5. ★ **Can a learned metric predict listeners' ratings for a kind of codec that did not exist when it was trained?**

   *Where the frontier is.* Collect MUSHRA ratings for classical and neural codecs on varied music; train metrics on some
   codecs and test on unseen ones; measure prediction codec by codec, with confidence intervals.

## Sources

* M. Bosi and R. E. Goldberg, *Introduction to Digital Audio Coding and Standards* (2003); J. Sterne, *MP3: The Meaning of
  a Format* (2012); K. Brandenburg, "MP3 and AAC explained", AES Conference (1999); T. Painter and A. Spanias, "Perceptual
  coding of digital audio", *Proc. IEEE* (2000).
* C. E. Shannon, "A mathematical theory of communication" (1948); S. W. Golomb, "Run-length encodings" (1966); R. F. Rice,
  "Some practical universal noiseless coding techniques" (JPL, 1979); T. Robinson, "SHORTEN" (Cambridge, 1994).
* M. R. Schroeder, B. S. Atal and J. L. Hall, "Optimizing digital speech coders by exploiting masking properties of the
  human ear", *JASA* (1979); J. D. Johnston, "Transform coding of audio signals using perceptual noise criteria", *IEEE
  JSAC* (1988); E. Terhardt, "Calculating virtual pitch" (1979).
* J. P. Princen and A. B. Bradley, "Analysis/synthesis filter bank design based on time domain aliasing cancellation",
  *IEEE Trans. ASSP* (1986).
* J.-M. Valin, G. Maxwell, T. B. Terriberry and K. Vos, "High-quality, low-delay music coding in the Opus codec", AES
  Convention (2013).
* ITU-R BS.1116 (1994), BS.1534 (MUSHRA, 2001), BS.1387 (PEAQ, 1998); D. Clark, "High-resolution subjective testing using a
  double-blind comparator", *JAES* (1982).
* S. P. Lloyd, "Least squares quantization in PCM" (1957; 1982); Y. Linde, A. Buzo and R. M. Gray, "An algorithm for vector
  quantizer design", *IEEE Trans. Comm.* (1980); N. Zeghidour et al., "SoundStream: an end-to-end neural audio codec"
  (2021); A. Défossez et al., "High fidelity neural audio compression" (EnCodec, 2022).
