# Music, Built: Part 68, The Variations

The last part of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act XII, *Coda*. Bach's *Goldberg Variations* end by playing the opening
aria again, note for note, and it does not sound the same. This part runs the series' whole chain once, from a score
to a listener and back to a score, measures what survives the journey, orders the sixty-seven Variations into a
suite and plays it, counts what was built, and ends with Variation 1 again. Its tools are Monochord's
(`explainer/music/monochord/roundtrip.py`, with Part 61's transcription and Part 63's features).

* **The aria again.** An ear question (Variation 1, exactly as Part 1 made it: what do you hear now?); the
  *Goldberg Variations* (1741: an aria, thirty variations, every third a canon, the aria *da capo*; the Goldberg
  story is from 1802); the series map; the plan.
* **1. The chain, once more.** The Chain with every link lit, and the way back; which act built which link; the
  experiment (the whole Tune, 42 notes, through a performance, Part 38's piano, a room, a microphone, a master and
  Part 58's coder, and back by onsets, pitch, a drifting tempo, a key and a fingerprint); what is measured.
* **2. Down the chain.** Five stages heard; each measured by what it changes (onsets 123 ms from a strict
  tempo; reverberation 3.1 dB under the direct sound; noise 33 dB under the music; crest factor
  14.6 to 8.8 dB; the coder's noise -13 dB against its mask at 128 kbit/s and +5 at 16);
  four spectrograms; an ear question (the end of the chain at 16 kbit/s: can you still sing it?); the coder rate by
  rate, and what its fallback band does at 16 kbit/s (the melody's band 82 dB down; 37 of 42 keys
  wrong), heard.
* **3. Back up the chain.** How the machine listens (onsets by spectral flux or SuperFlux; pitch by YIN or by the
  harmonics gained at each onset); settings chosen on four other tunes (Frère Jacques, Mary Had a Little Lamb, London Bridge, Ode to Joy): YIN 34 % of keys
  wrong, Part 61's flux with the onset reading 23 %, SuperFlux 20 %; the Tune: wrong keys by
  stage (as written 6; performed 6; room 8; microphone 8; master 14; 128 12; 64 15; 32 14; 16 kbit/s 12); which notes go wrong (every change of key found as written, 17 of 24 at worst; repeated notes the weak spot, 9 to 14 of 18 found; the coder's false onsets at 32 and 16 kbit/s); beside Part 61's network; the first two phrases written and recovered; the key, G major by the recovered lengths and C major by the notes; an ear question (three
  recovered scores, replayed: which came from where?).
* **4. What survives.** Thresholded spectrogram occupancy (changed by the room, master and coder) against the notes that change key, stage by stage; does it still sound like itself (the fingerprinter's match: 689 aligned votes on the performance, 25 through the room, and from the master on hardly more than the next best; tempo; the key, C major at 6 of 9); the room alone,
  heard; why notation kept pitch and time (Part 10's 168 bits); what the experiment does not show.
* **5. Ordering a suite.** An excerpt rule fixed in advance; the excerpts mapped by Part 63's features; path
  lengths (as made 636, nearest-next 390, 2000 random orders 653 to 745); an ear question
  (the suite's longest and shortest steps, Variations 27 to 28 and 31 to 32); the nearest-next order,
  heard; the order chosen: as made.
* **6–8. The suite.** Three movements: Variations 1–22 (Acts I–III), 23–44 (IV–VII) and 45–67 (VIII–XII),
  8.5 seconds of each, 10.1 minutes in all, each cell lit as it plays with its ledger title.
* **9. What was built.** Monochord counted (95 modules, about 25,531 lines, 879 tests, 999 sounds,
  4.3 hours, 68 labs); its layers; how it was checked; what you can now do.
* **10. The ledger.** All sixty-eight rows, page by page; what the ledger is.
* **11. Frontier: what is still unknown.** Part 1's question; an ear question (a fifth at 3:2 and one mistuned by 1 %:
  partials 392 and 389 Hz beat about 4 times a second); physics, ear, timbre and culture; what is
  still open (44 research problems from the parts); ★ research problem: separate the ear's part from the culture's.
* **Variation 68, recap, and the aria again.** The ledger's last row; what we found; five problems; from here;
  references; Variation 1 again, on the drawn monochord; the end.

## What is computed, and what is heard

`python -m videos.music.music68.compute` (some minutes: the chain is run for the Tune and four other tunes) fills
`.cache/music68/`.

| Item | What it computes | Checked against |
|---|---|---|
| `chain`, `pictures`, `wide` | the Tune at nine stages down the chain, each stage's measure, spectrograms; the coder's fallback band | the coder's bit rates (tests) |
| `calibrate` | the transcriber's settings, chosen on four other tunes over every stage | the Tune is not among them (tests) |
| `roundtrip`, `back` | the line transcribed, quantized and keyed at each stage; three recovered scores replayed | the written score (edit distance) |
| `identify`, `survive` | fingerprints, tempo and key at each stage; brightness against wrong keys; the room alone | — |
| `order`, `pairs`, `nearest` | the excerpts' features, classical scaling, path lengths, 2000 random orders | the rule's definition (tests) |
| `suite`, `hook`, `fifths` | the three movements from every part's stored Variation; Variation 1; two fifths | the ledger (tests) |
| `built` | Monochord and the series counted from the repository | — |

Monochord's tools are held in `tests/music/test_roundtrip.py`; this part's claims and clips in `tests/music/test_music68.py`.

**Sounds.** Part 38's piano through the chain; every part's own Variation, as stored; Part 1's string.

**What the models are, and are not.** *The chain* has one piano, one tune, one room, one take, and a performance
made by rule; real chains have more links and worse ones. *The transcriber* listens for one line; it would do worse
on a chorus or a band. *The coder* is Part 58's: at 16 kbit/s its table has no band, and the chain uses 5.5 kHz,
between its entries for 12 and 24 kbit/s; the fallback is shown separately. *The ordering features* measure bands,
chroma and flux, not everything a listener hears; the excerpt rule was fixed before the suite was heard.

## Build

```bash
python -m videos.music.music68.compute                          # numbers and sounds
EXPLAINER_TTS=silent python tools/build.py music68 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music68 --sync                         # the sound gates
python tools/dead_air.py renders/music68_480p.mp4 --sound music68  # no empty screen; no sound over a still one
python tools/lecture_length.py music68                          # 30 to 60 minutes, listening included
python tools/build.py music68                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 68                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A line of 42 notes comes back with one note missed near the start. How many positions disagree, and
   what is the edit distance?

   *Solution.* Compared position by position, every note after the gap is shifted by one, so up to 41 positions
   disagree (fewer where neighbouring notes repeat). The edit distance is 1: insert the missed note. That is why the
   film counts wrong keys by edit distance (`roundtrip.edit_distance`).

2. **Prove.** Show that the greedy nearest-neighbour order can be longer than the best order by a factor that grows
   with the number of pieces.

   *Solution.* Rosenkrantz, Stearns and Lewis (1977) built point sets on which nearest-neighbour tours are Θ(log n)
   times longer than the optimum, and proved the ratio is at most ½(⌈log₂ n⌉ + 1) for distances obeying the triangle
   inequality. The construction places points so that each greedy choice is locally shortest but leaves a far
   cluster to be fetched later, recursively at every scale; summing the detours over log n scales gives the factor.

3. **Ear.** The lab sends a tune of your choice down the chain. At which bit rate can you no longer sing it back?

   *Solution.* Set `KBPS` from 128 down to 16 (the lab cuts the band to 5.5 kHz at 16, as the film does). For most
   listeners the tune stays singable at every rate; what goes first is the sound's cleanness. The lab's table shows
   where the machine's wrong keys begin to rise, which is usually earlier than where a listener loses the tune.

4. **Build.** Add a stage to the chain (a phone's loudspeaker, Part 54) and find what it costs the round trip.

   *Where to look.* In the lab's `chain`, band-limit the master to 300 Hz to 8 kHz (or use Part 54's loudspeaker
   response) before the coder. The fundamentals of low notes go, the harmonics stay: the onset reading still finds
   most keys, YIN may jump an octave. Compare the two readings' wrong keys.

5. ★ **Why do simple ratios sound good? Design the experiment that would separate the ear's part from the culture's.**

   *Where the frontier is.* Play the same chords with harmonic and with stretched partials to listeners of many
   musical cultures and to some with little musical experience; measure perceived roughness, fusion and pitch apart
   from preference, with enough trials for the effects expected (Part 67). McDermott et al. (2016) and later
   cross-cultural studies are the place to start.

## Sources

* J. S. Bach, *Clavier-Übung* IV (the *Goldberg Variations*, 1741); J. N. Forkel, *Über Johann Sebastian Bachs
  Leben, Kunst und Kunstwerke* (1802), the source of the Goldberg story.
* H. von Helmholtz, *On the Sensations of Tone* (1863); J. H. McDermott, A. F. Schultz, E. A. Undurraga and R. A. Godoy,
  "Indifference to dissonance in native Amazonians reveals cultural variation in music perception", *Nature* (2016).
* M. Müller, *Fundamentals of Music Processing* (2nd ed., 2021); A. de Cheveigné and H. Kawahara, "YIN, a fundamental
  frequency estimator for speech and music", *JASA* (2002); S. Böck and G. Widmer, "Maximum filter vibrato
  suppression for onset detection" (SuperFlux), *DAFx* (2013); A. T. Cemgil and B. Kappen, "Monte Carlo methods for
  tempo tracking and rhythm quantization", *JAIR* (2003).
* V. I. Levenshtein, "Binary codes capable of correcting deletions, insertions and reversals" (1966); D. J.
  Rosenkrantz, R. E. Stearns and P. M. Lewis, "An analysis of several heuristics for the traveling salesman
  problem", *SIAM J. Computing* (1977); W. S. Torgerson, "Multidimensional scaling" (1952).
* J. O. Smith, *Physical Audio Signal Processing* (2010).

Review scope: pitch-change/restrike detection counts match onset proximity within 80 ms and do not verify pitch; the separate note F-score requires pitch and a 50 ms onset window. Compact notation bit counts rely on shared decoding assumptions. The 16 kbit/s chain uses an explicit 5.5 kHz cutoff override. Feature-space ordering is not a validated perceptual optimum.
