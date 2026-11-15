# Music, Built: Part 57, Mastering and Loudness

Part 57 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act X, *The Studio and the Stage*. In 2008 fans of a rock band found
that the version of its new album inside a video game sounded better than the CD, which had been mastered so loud that
the peaks were shaved flat. The loudness war had a casualty with waveforms to prove it. Then streaming services began
turning loud records down, and the incentive vanished. This part builds the instruments of both the war and the peace: a
gated loudness meter and a true-peak meter (the series' own, checked against ffmpeg), a look-ahead limiter, a mastering
chain, platform normalization and dither. The tools are Monochord's (`explainer/music/monochord/master.py`, with
`loudness.py`); the music is Part 56's session and earlier parts' Variations.

* **A record too loud for its own good.** An ear question (Part 56's mix mastered gently and for loudness, played at the
  same loudness: which was mastered for loudness? the second, its peak-to-loudness ratio 6.7 dB against 13); *Death
  Magnetic* and *Guitar Hero III*; how the war ended; the plan.
* **1. What mastering is for.** Between the mix and the listener; Monochord's chain (tilt EQ, glue compression, a
  look-ahead limiter, dither), stage by stage, and heard; an album, not a track.
* **2. Meters.** Sample peak, VU and PPM; three meters on one drum hit (the VU 22 dB below the peak); K-weighting; two
  tones at one voltage, 6 LU apart, heard; what one number can and cannot say.
* **3. LUFS and gating.** BS.1770 in four lines; the gates at work (a quiet start: −21.9 LUFS gated, −23.6 ungated); the
  meter against ffmpeg's (integrated within 0.05 LU, true peak within 0.1 dB); momentary, short-term, integrated and the
  loudness range; targets (R 128's −23, A/85's −24, the services' −14 to −16, this series' −16).
* **4. Inter-sample peaks.** A sine whose samples miss its peaks by 3.01 dB; measuring the true peak by oversampling;
  overs in a clipped master (+2.5 dBTP with every sample legal); why it matters; inside the converter.
* **5. Limiters and clippers.** A look-ahead limiter; 0.6 seconds close up (the gain glides down before each hit); clipping
  against limiting at the same loudness, heard; clippers on purpose.
* **6. The loudness war in numbers.** An arms race; one mix, six masters (PLR from 15.2 to 6.7 dB, the limiter topping out
  near −7.7 LUFS, the loudness range hardly moving, as Deruty and Tardieu found); what loudness costs; the sausage; three
  masters heard as a CD would play them.
* **7. Normalization.** One gain per track; three masters normalized to −14 LUFS (the loud one turned down 6 dB, its peaks
  now the lowest); an ear question (which was mastered loudest? the first); tracks and albums.
* **8. Comparing at equal loudness.** An ear question (two masters: which sounds better? the same master, the second 1 dB
  louder); the loudness bias; the method (matched, quick, blind, counted); this series' rule.
* **9. Dither.** Cutting the word length (98 dB at 16 bits); rounding with and without dither; where the error goes
  (rounded, dithered, noise-shaped); a fading piano note at 8 bits, heard; when to dither.
* **10. Vinyl, files and this series.** The groove (159 µm at 50 Hz, 1.6 µm at 5 kHz for 5 cm/s); the RIAA curve (+19.3,
  −19.6 dB); a record played without it, heard; one master for each medium; how this series is mastered.
* **11. Frontier: loudness and preference.** What experiments found; after the war; machines that master; ★ research
  problem: once everything is normalized, what peak-to-loudness ratio do listeners prefer, and does it depend on where
  they listen?
* **Variation 57, recap and problems.** An album side of four Variations matched at −16 LUFS, then Variation 56 mastered
  gently and war-mastered, matched; the ledger (the war master's PLR 6.6 dB against 13.0); what we found; five problems;
  where it comes back; in practice; references; Part 58.

## What is computed, and what is heard

`python -m videos.music.music57.compute` (about a minute) fills `.cache/music57/`; the `meters` item runs ffmpeg.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `war`, `chain` | Part 56's mix mastered by Monochord's chain at several targets | the targets; −1 dBTP (tests) |
| `meters` | K-weighting, VU, PPM, gated blocks, LRA; two tones | ffmpeg's ebur128 (tests) |
| `truepeak`, `limiter` | inter-sample peaks; clipping against limiting | +3.01 dB; the ceiling (tests) |
| `norm`, `matched` | streaming normalization; the same master 1 dB louder | the gains (tests) |
| `dither` | rounding, TPDF dither and noise shaping at 8 bits | the error's spectrum (tests) |
| `vinyl` | the RIAA curve, groove excursions, a record without de-emphasis | ±19.3/19.6 dB (tests) |
| `series` | this series' levels, measured | — |
| `tune57` | Variation 57 | — |

Monochord's tools are held in `tests/music/test_master.py`; this part's claims and clips in `tests/music/test_music57.py`.

**Sounds.** Part 56's session (Part 8's voice, Part 38's piano, guitar and bass, Part 40's drums), mixed close and dry and
mastered here; Part 38's piano for dither; sine tones; the Variations of Parts 52 to 55.

**What the models are, and are not.** *The limiter* looks ahead by having its gain look ahead rather than delaying the
audio, which gives the same result without latency; its detector is the 4× oversampled peak. *The mastering chain* is
deliberately simple (no multiband processing, no clipper), which is why it tops out near −7.7 LUFS on this mix. *The
record* is only the RIAA filters: no groove, no stylus, no surface noise. *The dither* is shown at 8 bits so that it can be
heard; at 16 bits the same effects lie near −96 dBFS.

## Build

```bash
python -m videos.music.music57.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music57 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music57 --sync                         # the sound gates
python tools/dead_air.py renders/music57_480p.mp4 --sound music57  # no empty screen; no sound over a still one
python tools/lecture_length.py music57                          # 30 to 60 minutes, listening included
python tools/build.py music57                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 57                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A track measures −9 LUFS with a true peak of −0.3 dBTP. What does a service at −14 LUFS play it at, and
   where are its peaks?

   *Solution.* The service turns it down by −14 − (−9) = −5 dB, so it plays at −14 LUFS with its peaks at −5.3 dBTP. A
   master made at −14 LUFS with a −1 dBTP ceiling plays at the same loudness with peaks 4.3 dB higher.

2. **Prove.** Show that a sine at f_s/4, sampled 45° from its peaks, has a true peak 3.01 dB above its sample peak.

   *Solution.* The samples are sin(πn/2 + π/4), which takes only the values ±sin(π/4) = ±1/√2. The continuous sine
   reaches ±1. The ratio is √2, 20 log₁₀ √2 = 3.01 dB.

3. **Ear.** The lab masters a small groove at several targets and plays the masters matched in loudness; order them by
   how hard they were limited.

   *Solution.* The lab prints the order. Listen to the kick's attack and the space after each hit: the harder the
   limiting, the softer the attack and the louder the space.

4. **Build.** Add a soft clipper before the limiter, and find how much loudness it buys for 0.1 % distortion.

   *Where to look.* Put a tanh stage (Part 50) before `master.limiter`, scaled so that it only touches the largest few
   peaks; measure loudness at the −1 dBTP ceiling against its drive, and the distortion as the residual of a sine through
   the same chain. A clipper in front lowers the PLR the limiter has to work against, so the same limiting reaches a few
   tenths of a decibel more, and on transient-heavy material more.

5. ★ **Once everything is normalized, what peak-to-loudness ratio do listeners prefer, and does it depend on where they
   listen?**

   *Where the frontier is.* Master mixes in several genres at several PLRs, normalize them all, play them in a studio, a
   living room and on earbuds in recorded street noise, and collect blind preferences; model them against the music, the
   place and the listener.

## Sources

* B. Katz, *Mastering Audio: The Art and the Science* (3rd ed., 2015); B. Owsinski, *The Mastering Engineer's Handbook*
  (4th ed., 2016).
* ITU-R BS.1770-4, *Algorithms to measure audio programme loudness and true-peak audio level* (2015); EBU R 128 (2010) and
  Tech 3341, 3342 (2016); ATSC A/85; AES TD1004 (2015); G. A. Soulodre, "Evaluation of objective loudness meters", AES
  Convention (2004).
* E. Vickers, "The loudness war: background, speculation and recommendations", AES Convention (2010); E. Deruty and
  D. Tardieu, "About dynamic processing in mainstream music", *JAES* (2014).
* N. B. H. Croghan, K. H. Arehart and J. M. Kates, "Quality and loudness judgments for music subjected to compression
  limiting", *JASA* (2012); J. Hjortkjær and M. Walther-Hansen, "Perceptual effects of dynamic range compression in popular
  music recordings", *JAES* (2014).
* J. Vanderkooy and S. P. Lipshitz, "Dither in digital audio", *JAES* (1987); S. P. Lipshitz, R. A. Wannamaker and
  J. Vanderkooy, "Quantization and dither: a theoretical survey", *JAES* (1992).
* RIAA, *Standard recording and reproducing characteristic* (1954); D. Clark, "High-resolution subjective testing using a
  double-blind comparator", *JAES* (1982).
