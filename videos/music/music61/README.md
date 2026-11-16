# Music, Built: Part 61, Pitch, Onsets and Transcription

Part 61 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act XI, *Listening Machines*. In 1770 the fourteen-year-old Mozart
heard Allegri's *Miserere* in the Sistine Chapel and wrote it out from memory; for machines, hearing music and writing down
its notes has been called the holy grail of music computing. Act XI turns the series' chain around, sound in and notes
out, and this part builds the first listeners: YIN for one voice's pitch and what noise does to it, salience and the
octave that hides in a chord, spectral flux for onsets, non-negative matrix factorization with note templates, a small
network that learns from examples, what both do on timbres they never heard, how to keep score, and how performed seconds
become written beats. The tools are Monochord's (`explainer/music/monochord/mir/transcribe.py` and `neural.py`); every
piece is rendered by Monochord, so commanded note labels are known; acoustic boundaries and pedal still require interpretation.

* **The holy grail.** An ear question (the Tune with chords twice: which is the performance and which a network's
  transcription played back? the second was the original; the copy found 21 of 30 notes and added 43); Mozart and the
  *Miserere*; why a listening machine needs an answer key (160 training pieces, 2,252 notes; 12 test pieces); the plan.
* **1. One voice's pitch.** The problem; the difference function; the missing fundamental (partials 2 to 8 of 220 Hz, found
  at 220.0); YIN's steps (normalization, a threshold, interpolation: a bias of 0.02 cents against 1.8 for plain
  autocorrelation); YIN's track played as a sine beside the voice, heard; uses.
* **2. Pitch in noise.** The sung Tune with noise 20, 0 and −10 dB down, tracked and heard; gross errors against noise (YIN
  9 % at 0 dB, 60 % at −5, where autocorrelation is still at 10 %: in heavy white noise the plainer method is the more
  robust); lessons.
* **3. Many notes at once.** Why a chord is harder; an ear question (C–E–G against C–E–G–C: not the same); salience, its
  peak on C3, an octave below the lowest note played; iterative cancellation (Klapuri); the hidden octave.
* **4. Where notes begin.** Spectral flux; the Tune on piano and on bowed strings, heard with the onsets drawn (F 0.90 and
  0.74); precision against recall as the threshold moves; what makes onsets hard.
* **5. Factorizing the spectrogram.** NMF; the multiplicative updates; components found blind; note templates from
  isolated piano notes; a test piece factorized and heard; its transcription played back (9 of 10 notes found, 17 added,
  mostly on the range's edges); limits.
* **6. A network that listens.** Design (five frames of log spectrum in, 37 note probabilities out); training on 48,160
  frames; results (piano note F 0.67 against NMF's 0.49); inside the network; a test piece heard; how many notes at once
  (from 0.91 on single lines to 0.54 with six voices; NMF from 0.63 to 0.45).
* **7. Timbres never heard.** One piece on piano, harp, organ and strings, heard; the scores (the network falls to 0.24 on
  the harp, NMF to 0.35); an ear question on the organ (the first was the original); why.
* **8. Keeping score.** Note-level precision, recall and F; an example; an ear question (two transcriptions at F 0.82 and
  0.83: the first is missing 9 of 30 notes, the second has 5 an octave out); frame-level scores; what the keys contain.
* **9. From notes to a score.** Seconds are not beats; the Tune's opening with rubato, its exact onsets quantized: one fixed
  tempo (180 a minute) puts 1 of 14 on the written beat, a tempo that may drift puts all 14; the tempo curve it chose (108
  to 135 around the written 120); the performance and the score, heard; key (C major, r = 0.97) and spelling; the rest of a
  score.
* **10. Fifty years of transcription.** Early systems (Moorer, 1977); data and benchmarks; what the ear still does better.
* **11. Frontier: many instruments, and scores.** Multi-instrument transcription; audio to score; ★ research problem: can a
  transcriber stay calibrated on a timbre it has never heard?
* **Variation 61, recap and problems.** The Tune performed, transcribed and re-rendered, five times round (note F against
  the original 0.53 after one round, 0.10 after five); the ledger; what we found; five problems; where it comes back; in
  practice; references; Part 62.

## What is computed, and what is heard

`python -m videos.music.music61.compute` (an hour or more on a busy machine: the network trains, once, into
`.cache/music61/net.pt`) fills `.cache/music61/`.

| Item | What it computes | Checked against |
|---|---|---|
| `data` | 160 training and 12 test pieces of random polyphony, C3 to C6 | by construction |
| `pitch`, `pitchheard` | YIN and autocorrelation on the sung Tune in noise; the missing fundamental; the track as a sine | the notes sung (tests) |
| `chords` | salience, NMF and the network on C–E–G and C–E–G–C | the notes played (tests) |
| `onsets` | spectral flux and peak picking on piano and strings; a threshold sweep | the onsets played (tests) |
| `nmf`, `nmfheard` | templates; NMF transcription of every test piece on four instruments | the notes played (tests) |
| `net`, `polyphony`, `timbres`, `hook` | the network's transcriptions; F against polyphony; unseen timbres | the notes played (tests) |
| `scoreheard` | two transcriptions at the same F, by dropping and by octave errors | by construction (tests) |
| `score` | fixed-tempo and drifting-tempo quantization of a rubato performance; key | the written beats (tests) |
| `tune61` | Variation 61's five rounds | the original notes (tests) |

Monochord's tools are held in `tests/music/test_transcribe.py`; this part's claims and clips in
`tests/music/test_music61.py`.

**Sounds.** Part 38's piano (with the damper that ends each note's string force over 80 ms); a Karplus–Strong harp; an
organ; Part 9's bowed strings; Part 8's voice; white noise.

**What the models are, and are not.** *YIN* here has no voicing model beyond its aperiodicity; *the onset detector* is
spectral flux with a moving threshold. *NMF* has one fixed template per pitch, learnt from isolated notes of one piano.
*The network* sees five frames of a log-frequency spectrogram and outputs 37 independent note probabilities; it has no
onset head, no language model of notes and no data beyond random polyphony on one piano, so it is far from Onsets and
Frames or MT3. *The quantizers* see exact onsets; with a real transcription, its errors come first.

## Build

```bash
python -m videos.music.music61.compute                          # numbers and sounds (the network trains once)
EXPLAINER_TTS=silent python tools/build.py music61 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music61 --sync                         # the sound gates
python tools/dead_air.py renders/music61_480p.mp4 --sound music61  # no empty screen; no sound over a still one
python tools/lecture_length.py music61                          # 30 to 60 minutes, listening included
python tools/build.py music61                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 61                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A transcriber reports 40 notes, of which 30 match the 36 played. What are its precision, recall and
   F-measure?

   *Solution.* Precision 30/40 = 0.75; recall 30/36 = 0.833; F = 2PR/(P + R) = 2 × 0.75 × 0.833 / 1.583 ≈ 0.79.

2. **Prove.** Show that the multiplicative update for H leaves the KL divergence unchanged when V = WH exactly.

   *Solution.* The update is H ← H ⊙ (Wᵀ(V ⊘ WH)) ⊘ (Wᵀ1). If V = WH, then V ⊘ WH = 1 (all ones), so the numerator is Wᵀ1
   and the factor is exactly 1 in every entry: H does not change, and neither does the divergence, which is zero, its
   minimum. (More generally, the update never increases the divergence, by Lee and Seung's auxiliary-function argument.)

3. **Ear.** The lab plays chords with and without an added octave; which have it? Then check the transcriber.

   *Solution.* The lab prints which chords had the octave and what the transcriber reported. An added octave mostly
   brightens the chord rather than adding a note one hears separately; Chapter 3's network missed the added C5 for the
   same reason, its partials lying on the lower C's.

4. **Build.** Train the network on piano and harp together; measure it on the organ and the strings.

   *Where to look.* Render the training pieces on both instruments (half each, or every piece twice), keep the test pieces
   and their gains, and compare the note F on the organ and strings with the piano-only network's 0.52 and 0.53. Mixed
   training usually trades a little on each seen timbre for more on unseen ones.

5. ★ **Can a transcriber stay calibrated on a timbre it has never heard?**

   *Where the frontier is.* A calibrated transcriber's note probabilities match how often it is right. Measure calibration
   (reliability diagrams, expected calibration error) on seen and unseen timbres, then try temperature scaling on a few
   labelled seconds, conformal note sets, or self-training on the new timbre.

## Sources

* M. Müller, *Fundamentals of Music Processing* (2nd ed., 2021); A. Klapuri and M. Davy (eds.), *Signal Processing
  Methods for Music Transcription* (2006); E. Benetos, S. Dixon, Z. Duan and S. Ewert, "Automatic music transcription: an
  overview", *IEEE Signal Processing Magazine* (2019).
* A. de Cheveigné and H. Kawahara, "YIN, a fundamental frequency estimator for speech and music", *JASA* (2002); A. P.
  Klapuri, "Multiple fundamental frequency estimation based on harmonicity and spectral smoothness", *IEEE TSAP* (2003).
* J. P. Bello et al., "A tutorial on onset detection in music signals", *IEEE TSAP* (2005); S. Dixon, "Onset detection
  revisited" (DAFx, 2006).
* D. D. Lee and H. S. Seung, "Algorithms for non-negative matrix factorization" (NIPS, 2001); P. Smaragdis and J. C. Brown,
  "Non-negative matrix factorization for polyphonic music transcription" (WASPAA, 2003).
* C. Hawthorne et al., "Onsets and Frames: dual-objective piano transcription" (ISMIR, 2018) and "Enabling factorized piano
  music modeling and generation with the MAESTRO dataset" (ICLR, 2019); J. Gardner et al., "MT3: multi-task multitrack music
  transcription" (ICLR, 2022); C. Raffel et al., "mir_eval" (ISMIR, 2014).
* A. T. Cemgil and B. Kappen, "Monte Carlo methods for tempo tracking and rhythm quantization", *JAIR* (2003); J. A. Moorer,
  "On the transcription of musical sound by computer", *Computer Music Journal* (1977).

Note scoring uses maximum-cardinality one-to-one matching with exact integer MIDI pitches and stated timing tolerances; it does not call mir_eval. Network activations are not demonstrated to be calibrated probabilities.
