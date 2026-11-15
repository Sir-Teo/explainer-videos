# Music, Built: Part 54, Microphones and Loudspeakers

Part 54 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act X, *The Studio and the Stage*. Plug headphones into a microphone
socket and speak into them: they work. A loudspeaker is a microphone run backwards. When microphones became electrical in
1925, singers no longer had to fill a hall, and the intimate voice of the crooner was invented. This part builds both ends
of the chain as circuits: patterns and proximity, noise and balanced lines, a lumped-element loudspeaker simulator checked
against Small's and Thiele's closed forms, horns, crossovers, an adaptive noise canceller and a steerable array. The tools
are Monochord's (`explainer/music/monochord/transducer.py`); every microphone, cable, box and loudspeaker is simulated.

* **A loudspeaker run backwards.** An ear question (the Tune sung into a measurement microphone and into headphones used as a
  microphone: which was the headphones?); the headphone's response (6 dB less per octave above its 110 Hz resonance);
  electrical recording and the crooner; the plan.
* **1. Transducers and their circuits.** Dynamic, condenser, ribbon and electret; one number both ways (e = Bl v, F = Bl i);
  the condenser in two lines; three kinds of circuit; which microphone for which job.
* **2. Polar patterns.** Pressure and its gradient; the first-order family r = A + (1 − A) cos θ; a walk round a cardioid,
  heard; directivity (cardioid and figure-8 4.8 dB, hypercardioid 6.0, twice an omni's distance); patterns at high
  frequencies; an ear question (a piano behind a singer through an omni, a cardioid and a figure-8: which heard least?
  the cardioid, 30 dB down); choosing a pattern.
* **3. The proximity effect.** The gradient of a spherical wave (1 + 1/(jkr)); the bass rise by distance (at 100 Hz: +1.1 dB
  at 1 m, +11.5 at 15 cm, +20.8 at 5 cm); taming the effect; three distances heard; playing the effect.
* **4. Noise and balanced lines.** Thermal noise (0.25 µV, −129.7 dBu for 200 Ω); a noise budget (a dynamic microphone's
  floor like 16 dB SPL); phantom power; a balanced line; hum unbalanced and balanced, heard (40 dB less with 1 % imbalance);
  from millivolts to volts.
* **5. The loudspeaker as a filter.** A mass on a spring with a motor (Rice and Kellogg, 1925); a woofer in Thiele–Small
  parameters (fs 40 Hz, Qts 0.36, Vas 50 L); the amplifier as a brake; its impedance (66 Ω at resonance); efficiency
  (0.78 %, 92 dB at 1 m for 2.83 V) and Hofmann's iron law.
* **6. Sealed and vented boxes.** The back of the cone; three sealed boxes; the simulation checked (−3 dB points within
  0.1 Hz of Small's formula; Thiele's B4 at 40.0 Hz); the vented box (76 Hz sealed to 40 vented in 35 L); how long is the
  port?; what the amplifier sees (two impedance peaks).
* **7. Three loudspeakers.** A phone's, a bookshelf speaker and a floor-stander simulated (−3 dB at 844, 98 and 39 Hz);
  measuring a loudspeaker; one groove through each, heard; bass you cannot hear.
* **8. Horns.** An acoustic transformer; the throat's resistance against a bare piston (19 dB better at 200 Hz above a
  109 Hz cutoff); waveguides for tweeters; horns at work.
* **9. Crossovers and amplifiers.** Two drivers, one speaker; adding the sections back (Butterworth in phase: a hole;
  inverted: +3 dB; Linkwitz–Riley: flat); a hole at the crossover, heard; crossovers in software; amplifier classes.
* **10. Headphones and noise cancelling.** A loudspeaker on the ear; cancelling sound with sound; filtered-x LMS; how much
  it cancels by band (−33, −28 and −25 dB below 1 kHz; none above 2 kHz); feedforward, feedback and transparency; a cabin
  heard, off and on.
* **11. Frontier: arrays, beamforming and linearization.** An array's pattern; an ear question (one microphone or eight
  steered at a tenor beside a soprano?); MEMS microphones; making a small speaker behave; ★ research problem: how much
  louder and deeper can a small speaker be made to sound, safely, by control alone?
* **Variation 54, recap and problems.** The Tune sung with a piano behind, through an omni, a cardioid and a figure-8, then
  the cardioid's version through a phone, a bookshelf speaker and a floor-stander; the ledger (the cardioid takes the piano
  30 dB down; the phone reaches 844 Hz, the floor-stander 39); what we found; five problems; where it comes back; in
  practice; references; Part 55.

## What is computed, and what is heard

`python -m videos.music.music54.compute` (about a minute; Part 7's piano notes take the longest) fills `.cache/music54/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | a dynamic driver as a microphone | 6 dB an octave above resonance (tests) |
| `patterns`, `capture`, `rotate` | the first-order family; three patterns in a room; a walk round a cardioid | DF = 4 at A = 1/4 (tests) |
| `proximity` | the gradient of a spherical wave at three distances | the closed form (tests) |
| `noise`, `hum` | Johnson noise; a noise budget; balanced and unbalanced lines | 4kTRB; 40 dB at 1 % (tests) |
| `driver`, `speakers` | a lumped-element simulator: baffle, sealed and vented boxes; three loudspeakers | Small's and Thiele's closed forms (tests) |
| `horn`, `crossover`, `xover` | throat resistance; crossover sums; a hole heard | the cutoff; LR4 flat (tests) |
| `anc`, `beam` | a filtered-x LMS canceller; a delay-and-sum array | a cancelled tone; the array's gain (tests) |
| `tune54` | Variation 54 | — |

Monochord's tools are held in `tests/music/test_transducer.py`; this part's claims and clips in `tests/music/test_music54.py`.

**Sounds.** Part 8's voice, Part 7's piano and Part 50's groove (Part 40's drums and a plucked bass), passed through
simulated microphones, cables, loudspeakers, a canceller and an array.

**What the models are, and are not.** *The microphones* are ideal first-order patterns at every frequency (real ones narrow
in the treble). *The room* is a burst of filtered noise, not Part 49's image-source room. *The loudspeakers* are lumped
circuits: no cone break-up, no beaming, no nonlinearity; the treble roll-off is a stated filter. *The canceller* has a fixed
secondary path; real ones move.

## Build

```bash
python -m videos.music.music54.compute                          # numbers and sounds (about a minute)
EXPLAINER_TTS=silent python tools/build.py music54 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music54 --sync                         # the sound gates
python tools/dead_air.py renders/music54_480p.mp4 --sound music54  # no empty screen; no sound over a still one
python tools/lecture_length.py music54                          # 30 to 60 minutes, listening included
python tools/build.py music54                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 54                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A woofer with fs = 30 Hz, Qts = 0.35 and Vas = 80 L goes in a 40 L sealed box. Find fc and Qtc.

   *Solution.* Vas/Vb = 2, so the factor is √3 = 1.732: fc = 30 × 1.732 = 52.0 Hz and Qtc = 0.35 × 1.732 = 0.61.

2. **Prove.** Prove that A + (1 − A) cos θ has its greatest directivity at A = 1/4.

   *Solution.* The random-energy efficiency is REE(A) = ½∫₀^π (A + (1 − A)cos θ)² sin θ dθ = A² + (1 − A)²/3 (the cross
   term integrates to zero). Its derivative 2A − 2(1 − A)/3 vanishes at A = 1/4, where REE = 1/16 + 9/48 = 1/4: DF = 4,
   6.0 dB, the hypercardioid.

3. **Ear.** The lab plays a voice-like tone at random distances from a figure-8; order them, near to far.

   *Solution.* The lab prints them. The nearest is the boomiest: its fundamental and second harmonic rise by 15 dB and
   more against the upper harmonics.

4. **Build.** Add a second-order passive crossover to the simulator and find the sum's response with real drivers.

   *Where to look.* Put the crossover's coils and capacitors in series with each driver's electrical impedance (the
   simulator's `Z` against frequency), solve each branch's current, then each driver's pressure; the drivers' impedance
   is not a resistor, so the filters no longer sit where the formulas put them, which is why designers add a Zobel network.

5. ★ **How much louder and deeper can a small speaker be made to sound, safely, by control alone?**

   *Where the frontier is.* Model a micro-speaker's Bl(x), K(x) and coil heating; estimate them while it plays; pre-distort
   through the inverse and limit excursion and temperature; measure distortion and loudness, and test blind.

## Sources

* J. Eargle, *The Microphone Book* (2nd ed., 2004); L. L. Beranek and T. J. Mellow, *Acoustics: Sound Fields and
  Transducers* (2012); H. F. Olson, *Acoustical Engineering* (1957).
* E. C. Wente, "A condenser transmitter as a uniformly sensitive instrument for the absolute measurement of sound
  intensity", *Physical Review* (1917); G. M. Sessler and J. E. West, "Self-biased condenser microphone with high
  capacitance", *JASA* (1962); J. B. Johnson and H. Nyquist, *Physical Review* (1928).
* C. W. Rice and E. W. Kellogg, "Notes on the development of a new type of hornless loud speaker", *Trans. AIEE* (1925);
  A. N. Thiele, "Loudspeakers in vented boxes" (1961; *JAES* 1971); R. H. Small, "Closed-box loudspeaker systems" and
  "Vented-box loudspeaker systems", *JAES* (1972–73); A. G. Webster, "Acoustical impedance and the theory of horns" (1919).
* S. H. Linkwitz, "Active crossover networks for noncoincident drivers", *JAES* (1976).
* P. Lueg, US patent 2,043,416 (1936); B. Widrow and M. E. Hoff, "Adaptive switching circuits" (1960); S. M. Kuo and
  D. R. Morgan, *Active Noise Control Systems* (1996).
* W. Klippel, "Loudspeaker nonlinearities: causes, parameters, symptoms", *JAES* (2006); J. Benesty, J. Chen and Y. Huang,
  *Microphone Array Signal Processing* (2008).
