# Music, Built: Part 53, MIDI, Sequencers and the DAW

Part 53 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act IX, *Electric Sound*. In January 1983, on a trade-show floor, two
synthesizers from rival firms were joined by a five-pin cable, and a key pressed on one sounded the other. The
specification fitted on a few pages and has run the industry for forty years. This part reads it byte by byte, then
builds what sits on top: files, sequencers, a pattern language, and an audio engine with its hard real-time deadline.
The tools are Monochord's (`explainer/music/monochord/daw.py`); the cable, the deadlines and the dropouts are simulated.

* **A five-pin cable.** An ear question (a twelve-note chord, all at once and as MIDI delivers it: which was the cable?);
  the arrivals (the last note 7.0 ms after the first); Dave Smith, Ikutaro Kakehashi and the 1983 handshake; the plan.
* **1. Machines that play.** Music as instructions (the Banū Mūsā's cylinder, about 850; the music box, 1796); a computed
  music box, heard; paper rolls; forty notes a second on Part 7's piano, heard; Nancarrow; the arithmetic of a tempo canon.
* **2. MUSIC N and unit generators.** Max Mathews's MUSIC (1957) and MUSIC III's unit generators (1960); an orchestra and a
  score; the score played, heard; MUSIC's descendants (Csound, Max, Pure Data, SuperCollider); real time arrives.
* **3. MIDI, byte by byte.** One byte on the wire (31,250 baud, 320 µs); one note in three bytes; inside a keyboard
  (velocity from two contacts); running status (the Tune's first phrase: 42 bytes to 29); how long a chord takes (16 notes:
  15.4 ms plainly, 10.6 with running status); the other messages.
* **4. MIDI's limits, MPE and MIDI 2.0.** Seven bits (a sweep in 31-cent steps); an ear question (a resonant sweep by a
  7-bit controller or smoothly: which was the controller?); one bend per channel (0.024 cents a step over ±2 semitones);
  MPE (2018); MIDI 2.0 (2020); what MIDI got right.
* **5. MIDI files.** Chunks (the first 22 bytes of the Tune's file); variable-length times; from ticks to seconds; the
  whole Tune in 423 bytes against 6.9 MB of audio, read back exactly; MIDI files at work.
* **6. Sequencers: steps, rolls and trackers.** A sixteen-step line with accents and slides, heard; the piano roll; the
  Tune's first phrase in a tracker (Soundtracker, 1987); the workstation.
* **7. A pattern language and live coding.** Five rules (after TidalCycles); two lines expanded over four cycles; how the
  pattern is read (a tree); the two lines heard; live coding.
* **8. The audio callback.** A block at a time against a clock (128 samples at 48 kHz: 2.67 ms); blocks must not change
  the music (identical to the last bit in blocks of 32 to 2048); what a block costs (measured: small blocks cost more
  than their share); a missed deadline heard (5 of 1,500 blocks late, simulated); the rules of the audio thread; a
  lock-free queue.
* **9. Timing inside a block.** A sequencer that looks at the clock once a block (hi-hats up to 21 ms early with
  1024-sample blocks); an ear question (placed to the sample or snapped: which was snapped?); the latency budget;
  sample-accurate scheduling.
* **10. The graph, plug-ins and delay compensation.** The processing graph; plug-ins (VST to CLAP); two paths, one late
  (a 5 ms look-ahead limiter in parallel); delay compensation heard; why it sounded hollow (notches every 200 Hz from
  100); freezing and bouncing.
* **11. Frontier: learning in the audio thread; networked performance.** Neural effects under a deadline (RAVE);
  networked performance (5 ms per 1000 km of fibre; ensembles hold tempo up to about 20–25 ms); the browser as a studio;
  ★ research problem: what is the best-sounding model meeting a specified deadline under explicit platform assumptions?
* **Variation 53, recap and problems.** The Tune as a four-channel tracker module, then as a tempo canon at 3 : 4 : 5 : 6
  meeting on the last note; the ledger (32 tracker rows; meeting after 30.7 s; block and offline renders identical); what
  we found; five problems; where it comes back; in practice; references; Part 54.

## What is computed, and what is heard

`python -m videos.music.music53.compute` (under a minute) fills `.cache/music53/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `bytes` | a chord's arrival on the wire; the Tune's first phrase as bytes, with and without running status | the byte timing (tests) |
| `musicbox`, `pianola`, `musicn` | a music box, a roll on Part 7's piano, a MUSIC-style orchestra | — |
| `zipper` | a 7-bit controller sweep against a smooth one | the step size (tests) |
| `smf` | the whole Tune written as a MIDI file and read back | the notes and times (tests) |
| `steps`, `pattern` | a sixteen-step line; two lines of the pattern language | the pattern's expansion (tests) |
| `callback`, `timing` | the engine in seven block sizes, its cost and dropouts; block-snapped timing | bit-identical renders (tests) |
| `pdc` | parallel compression with and without delay compensation | the comb's notches (tests) |
| `tune53` | Variation 53: a tracker module and a tempo canon | convergence; identical renders (tests) |

Monochord's tools are held in `tests/music/test_daw.py`; this part's claims and clips in `tests/music/test_music53.py`.

**Sounds.** The engine's sawtooth voice, Part 51's ladder and drum circuits, Part 52's Karplus–Strong strings, Part 7's
piano and a computed music box. The cable's timing is computed from the specification; the dropouts are simulated.

**What the models are, and are not.** *The cable* is ideal: no other traffic, no jitter in the sender. *The costs* are
this part's Python and numba on one computer. *The dropouts* come from a model of a heavy session (60 per cent load and
rare stalls), not from a real audio interface. *The pattern language* is a small subset of TidalCycles' mini-notation.

## Build

```bash
python -m videos.music.music53.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music53 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music53 --sync                         # the sound gates
python tools/dead_air.py renders/music53_480p.mp4 --sound music53  # no empty screen; no sound over a still one
python tools/lecture_length.py music53                          # 30 to 60 minutes, listening included
python tools/build.py music53                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 53                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** With running status, how long does a 10-note chord take to arrive, and how long without?

   *Solution.* With running status: 3 + 9 × 2 = 21 bytes, 21 × 320 µs = 6.72 ms. Without: 30 bytes, 9.6 ms.

2. **Prove.** Prove that a variable-length quantity of n bytes holds every number below 2^{7n}, and that the code is
   prefix-free (no code is the start of another).

   *Solution.* Each byte carries seven bits, so n bytes carry 7n bits: every number below 2^{7n} has such a code (with
   leading zero groups dropped, the shortest one). The top bit is set on every byte but the last, so a reader knows a code
   has ended exactly when it meets a byte with the top bit clear; no proper prefix of a code ends that way, so no code is
   the start of another, and a stream of codes needs no separators.

3. **Ear.** The lab plays a groove with notes snapped to blocks or placed exactly, at random; say which.

   *Solution.* The lab prints them. Snapped grooves limp: the gaps between hats vary by up to a block (21 ms at 1024
   samples), so some pairs crowd and some drag.

4. **Build.** Add a tempo change to the MIDI writer (a second tempo event) and make the reader honour it.

   *Where to look.* Write a meta event FF 51 03 tt tt tt at its tick in the tempo track; in `read_smf`, keep a sorted list
   of (tick, tempo) and convert each event's tick to seconds by summing over the tempo segments before it.

5. ★ **What is the best-sounding model that is meeting a specified deadline under explicit platform assumptions?**

   *Where the frontier is.* Measure observed maxima and tail latency per block; finite trials do not prove a worst-case bound. State platform and scheduling assumptions when arguing a guarantee. Measure the cost of neural effects inside a real-time
   engine; trade model size against block size and look-ahead (whose latency the graph must compensate); judge each by blind
   listening; and look for architectures whose cost is constant by construction.

## Sources

* MIDI Manufacturers Association, *The Complete MIDI 1.0 Detailed Specification* (1983–96), *Standard MIDI Files 1.0*
  (1988), MIDI Polyphonic Expression (2018), MIDI 2.0 (2020); D. Smith and C. Wood, "The 'USI', or Universal
  Synthesizer Interface", AES (1981).
* M. V. Mathews, *The Technology of Computer Music* (1969); C. Roads, *The Computer Music Tutorial* (2nd ed., 2023);
  M. Puckette, *The Theory and Technique of Electronic Music* (2007); J. McCartney, "Rethinking the computer music
  language: SuperCollider", *CMJ* (2002); B. Vercoe, Csound (1986).
* K. Gann, *The Music of Conlon Nancarrow* (1995); T. Koetsier, "On the prehistory of programmable machines: musical
  automata, looms, calculators", *Mechanism and Machine Theory* (2001).
* A. McLean, "Making programming languages to dance to: live coding with Tidal", FARM (2014); S. Aaron and A. Blackwell,
  "From Sonic Pi to Overtone" (2013); G. Wang, *The ChucK Audio Programming Language* (2008).
* R. Bencina, "Real-time audio programming 101: time waits for nothing" (2011); Steinberg, VST (1996); CLAP (2022).
* C. Chafe, M. Gurevich, G. Leslie and S. Tyan, "Effect of time delay on ensemble accuracy", ISMA (2004); J.-P. Cáceres
  and C. Chafe, "JackTrip" (2010); A. Caillon and P. Esling, "RAVE: a variational autoencoder for fast and high-quality
  neural audio synthesis" (2021).
