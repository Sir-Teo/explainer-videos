# Music, Built: Part 8, Pipes, Reeds and Voices

Part 8 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). Part 7 ended on the bow, which turns a steady pull into a vibration by gripping
and letting go in time with a string. This part is the same loop with air: a column of air that resonates, and a
valve that lets breath through in time with it. The flute, the clarinet, the oboe and saxophone, the trumpet, the
organ and the voice differ in the shape of the column and in the kind of valve. The instruments are Monochord's
(`explainer/music/monochord/instruments/winds.py`); every sound is computed in `compute.py`, and nothing was
recorded. Dates and attributions are the published ones, listed under Sources.

* **Two pipes of the same length.** An ear question: a pipe 60 cm long blown across its end and blown through a
  reed (281 and 140 Hz: an octave apart, and the lower one hollow); one voice, two notes at once; the plan.
* **1. A column of air.** Open ends and closed ends; a pipe open at both ends (every multiple) and closed at one
  (an octave lower, the odd multiples); a reed closes its end; Monochord's input impedance of the pipe (peaks at
  139, 421, 703 Hz for a reed; valleys at 280, 562, 844 Hz for a flute); the end correction; a worked example (a
  flute for middle C is 65.6 cm long; a clarinet for the D below, 58.4 cm).
* **2. A valve that pressure closes.** The reed's flow against the pressure across it: it rises, tops out at a
  third of the closing pressure and falls; one puff followed four times along the pipe; the mouthpiece pressure,
  nearly a square wave, with odd harmonics; an ear question (blown steadily harder: silence, then a note that
  brightens); why a third (below it the valve fights the wave, above it the valve feeds it); 0.37 with losses.
* **3. Holes.** A hole as wide as the pipe is nearly a saw cut; smaller holes act like holes further down (32, 81
  and 184 cents flat of the cut); a worked example (where the holes go: 8/9, 4/5, 3/4, 2/3, 3/5, 1/2: a flute is a
  monochord made of air); the register hole, which puts the lowest resonance out of tune so that the reed takes
  the next (140 to 433 Hz: a twelfth); the clarinet's nineteen semitones and the break.
* **4. Cones.** A cone closed at the reed has the notes of an open pipe (231, 463, 701 Hz against the cylinder's
  139, 421, 703); the missing tip and the mouthpiece that replaces its volume (1 : 2.06 : 3.16 becomes
  1 : 2.01 : 3.04); an ear question (one note on a cone and on a cylinder); lengths (72 cm against 43); Sax.
* **5. Lips and brass.** A valve that the breath opens, with a frequency of its own; a plain tube (60, 183, 307,
  431 Hz: odd) against a trumpet's shape (230, 348, 473, 593, 704 Hz: 2 to 6 times 116 Hz); what the bell does;
  the lips set to one frequency after another climb a staircase of resonances; a call of eight notes on one
  length of tube; the pedal note, which the model found unasked; a worked example (valves 1 and 3 together add
  31.2% where 33.5% is needed: 30 cents sharp).
* **6. A jet and an edge.** The flute's valve is a ribbon of air; its travel time must be about half a period
  (Coltman); blown harder, the note creeps sharp and then breaks to the octave; an ear question (which
  overblows an octave, which a twelfth?); the organ: five stops at 8, 4, 2⅔, 2 and 1⅗ feet are harmonics 1 to 5.
* **7. The voice: a source and a filter.** The vocal folds; the glottal pulse and its spectrum (falling 13 dB an
  octave); why the folds, unlike a reed, choose their own pitch; formants; the vowel ah as source times filter;
  the pulses alone and through three filters.
* **8. Vowels.** A worked example (a mouth at rest is a tube 17.5 cm long: 490, 1470, 2450 Hz, the vowel of
  "the"); two-tube shapes for ah and ee against Peterson and Barney's measurements; the map of two formants;
  an ear question (who'd, hod, heed on one note); one vowel on three notes.
* **9. What singers do.** An ear question (which voice carries?); the singer's formant: the third, fourth and
  fifth resonances drawn together near 3 kHz (+17 dB), where an orchestra is weak and the ear acute; a
  soprano's high A and the first formant raised onto it; overtone singing: two resonances merged onto one
  harmonic, and the Tune's first phrase on harmonics 8, 12 and 13.
* **10. Frontier: the parts we cannot yet compute.** The folds themselves; the player's own vocal tract; shock
  waves in loud brass; the jet; instruments designed by running the calculation backwards. ★ research problem.
* **Variation 8, recap and problems.** The Tune for a flute, a clarinet, a saxophone, a trumpet and a voice, a
  phrase each and then together; the ledger; what we found; five problems; where it comes back; in practice;
  references; overtones that are not harmonics, and Part 9.

## What is computed, and what is heard

`python -m videos.music.music8.compute` (about five minutes; three of them tuning the instruments of the
Variation) fills `.cache/music8/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | a jet and a reed on pipes 60 cm long; a model voice whose overtones are picked out one at a time | the octave between an open and a stopped pipe |
| `column` | input impedance of the pipe by transfer matrices, with wall losses and a radiating end | odd multiples of c/4L and all multiples of c/2L, with the end correction |
| `reed` | the reed's flow curve; mouthpiece pressure and flow; a scan of blowing pressure; a crescendo | the flow's maximum at 1/3; threshold just above 1/3; a square wave's odd harmonics |
| `holes` | one open hole of three sizes against a cut tube; the pipe with and without a register hole | the cut tube; the second resonance at three times the first |
| `cone` | resonances of a cylinder, a truncated cone and a cone with a mouthpiece; a reed on each | a complete cone's harmonic series; the mouthpiece-volume rule |
| `lips` | a trumpet's profile and resonances; lips set to 43 frequencies; a call; valve arithmetic | resonances 2 to 8 within 35 cents of multiples of 116.2 Hz (B flat is 116.5) |
| `jet` | the flute model's register against blowing pressure; a crescendo; five organ ranks | octave, then twelfth; hysteresis |
| `voice` | Rosenberg's glottal pulse and its spectrum; three formant filters; their output | a source slope near −12 dB an octave |
| `vowels` | formants of a plain tube and of two-tube shapes; the ten vowels | Peterson and Barney's averages for 33 men, within a semitone |
| `singers` | a filter with a singer's formant; a first formant moved onto a high note; overtone singing | a boost near 3 kHz of the size Sundberg reports |
| `tune` | Variation 8; every wind note measured after tuning | each within 8 cents of its pitch |

Monochord's wind instruments are held against these references in `tests/music/test_winds.py`; this part's
claims and clips in `tests/music/test_music8.py`.

**Sounds.** Fifteen clips, labelled on screen. `physical model`: the reed, lip and jet instruments, radiated
through their own bores. `synthesized`: the voice, which is a drawn pulse through formant filters. There are no
recordings.

**What the models are, and are not.** *The bores* carry plane waves, with wall losses and a radiating open end
(Levine and Schwinger's result in Norris and Sheng's fit); cones and bells are cut into short cylinders; a side
hole is a short open tube. There are no tone-hole lattices, pads or bends, and the trumpet's dimensions are
plausible ones chosen so that its resonances come out near a B flat instrument's, not measurements of a
particular trumpet (its tube is 1.37 m; a real one is 1.48 m with a differently shaped bell). *The reed* is the
quasi-static valve of McIntyre, Schumacher and Woodhouse, with no mass and no upstream tube; time is stepped
with the bore's reflection function. Its register hole gives a twelfth 50 cents wide; real clarinets are voiced
to correct that. *The saxophone* is a cone with a mouthpiece of the missing tip's volume. *The lips* are one
mass on a spring, blown open, which is the simplest model that plays; real lips also move along the flow. The
pedal note appears in the model at two lip frequencies without being asked for. *The flute* is schematic: a loop
of delay for the pipe and a second, shorter delay with smoothing and a saturating curve for the jet. It
reproduces what matters here (the half-period condition, the sharpening with blowing pressure, the breaks to the
octave and the twelfth, hysteresis) and is labelled as a model of a jet, not a calculation of one. *The voice*
is a source and a filter and nothing else: Rosenberg's pulse with a little jitter, shimmer and breath, through a
cascade of resonators at Peterson and Barney's formants; the two-tube mouths are Fant's cartoons. The soprano's
gain from tuning her first formant (36 dB here) is larger than in a real mouth, which is lossier, and the film
says so. The orchestra's spectrum in chapter 9 is a schematic slope after Sundberg, and is labelled as one.

## Build

```bash
python -m videos.music.music8.compute                          # numbers and sounds (about five minutes)
EXPLAINER_TTS=silent python tools/build.py music8 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music8 --sync                         # the sound gates
python tools/dead_air.py renders/music8_480p.mp4 --sound music8   # no empty screen; no sound over a still one
python tools/lecture_length.py music8                          # 30 to 60 minutes, listening included
python tools/build.py music8                                   # 1080p30, narrated
python -m pytest -q tests/music                                # Monochord against its references; this part's claims and clips
python -m videos.music.labs 8                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Two pipes.** A pipe is 40 cm long and 2 cm wide. Find its three lowest resonances when it is open at both
   ends, and when it is closed at one, with and without the end correction of 0.61 of the radius for each open end.

   *Solution.* Open at both ends: c/2L = 343/0.8 = 429 Hz, and its multiples 858 and 1286. Each open end adds
   0.61 × 1 cm, so the effective length is 41.2 cm: 416, 832, 1248 Hz, half a semitone lower. Closed at one end:
   c/4L = 214 Hz and the odd multiples 643 and 1072; with one open end corrected, L = 40.6 cm: 211, 633, 1056.
   The correction matters more for a short fat pipe than a long thin one, which is why organ builders cannot
   scale a rank of pipes by length alone. (The lab computes all twelve numbers, and Monochord's own values with
   wall losses, which are a few hertz lower still.)

2. **A third.** The flow through a reed is u = ζ(1 − Δ)√Δ, where Δ is the pressure across it as a fraction of the
   closing pressure. Show that u is greatest at Δ = 1/3, and explain why a clarinet cannot speak below it.

   *Solution.* du/dΔ = ζ[(1 − Δ)/(2√Δ) − √Δ] = ζ(1 − 3Δ)/(2√Δ), which is zero at Δ = 1/3, positive below and
   negative above. With the player blowing at a steady pressure, Δ is that pressure less the pressure in the
   mouthpiece, so a small rise p in the mouthpiece lowers Δ by p and changes the flow by −(du/dΔ)p. Below a third
   the flow falls when the mouthpiece pressure rises: the reed takes energy from the wave, like a resistor. Above
   a third the flow rises with the pressure: the reed gives energy to the wave. In a pipe with no losses that
   is the threshold exactly; with losses the reed must also supply what the walls and the open end remove, and
   the threshold moves up a little (0.37 for Monochord's pipe).

3. **Ear.** The lab sings one note on four vowels, in a random order. Name the four words, and say which formant
   told you each.

   *Solution.* The lab prints the words and their first two formants. A high second formant (above 1700 Hz)
   means the tongue is forward: heed, hid, head, had, in order of a rising first formant as the jaw opens. A
   low second formant with a low first means who'd or hood; with a high first, hod or hawed. Most listeners sort
   front from back vowels instantly and then need the first formant to choose within the group.

4. **Build.** With `winds.Bore`, put six holes of 4 mm radius in the 60 cm clarinet so that opening them in turn
   gives a major scale. How far are they from where a saw would cut?

   *Solution.* For each note, slide one open hole along the pipe until the first impedance peak is at the note
   (bisection: a hole nearer the reed gives a higher note). The lab finds holes at 51.5, 45.9, 42.8, 37.6, 33.5
   and 29.3 cm from the reed, each about 3 cm above the place where a saw would cut the pipe for the same note. A
   hole of 2 mm radius must sit about 7 cm above the cut, and a hole as wide as the bore about 1.5 cm. In a
   real instrument the open holes below the first also matter (they form a lattice with a cutoff frequency that
   shapes the tone), and the same holes must serve the upper register, so makers adjust position, diameter and
   undercutting together.

5. ★ **The player's tract.** Give the reed a second tube, upstream: the player's vocal tract. When does a
   resonance of the tract capture the note, and can the model bend a clarinet's pitch the way players do?

   *Where the frontier is.* The pressure across the reed is the mouth pressure less the mouthpiece pressure, so
   the two tubes act in series and the reed sees the sum of their impedances. Fritz and Wolfe (2005) measured
   clarinettists' tracts and found resonances that players move; Scavone, Lefebvre and da Silva (2008) and
   Chen, Smith and Wolfe (2008, 2009) measured the pressure on both sides of the reed while people played, and
   showed that in the saxophone's altissimo register and in the clarinet's glissando the tract's peak is as tall
   as the bore's and takes control. A model needs the tract's impedance as the player shapes it, which is not
   known in advance, and a reed with mass, since the effect is strongest where the reed's own resonance is
   near. Whether tuning the tract is a matter of pitch alone or also of tone is still argued.

## Sources

Books: A. H. Benade, *Fundamentals of Musical Acoustics* (1976), chs. 20–22 for woodwinds and brass, including
the trumpet's bell and the pedal note; N. H. Fletcher and T. D. Rossing, *The Physics of Musical Instruments*
(2nd ed., 1998), chs. 13–17; A. Chaigne and J. Kergomard, *Acoustics of Musical Instruments* (2016), for
transfer matrices, the reed's characteristic and its threshold; J. Sundberg, *The Science of the Singing Voice*
(1987); G. Fant, *Acoustic Theory of Speech Production* (1960), for the source-filter theory and the two-tube
vowels; H. von Helmholtz, *On the Sensations of Tone* (1863), ch. 5, for reed pipes and the vowels.

Papers: J. Backus, "Small-vibration theory of the clarinet", *JASA* 35 (1963); T. A. Wilson and G. S. Beavers,
"Operating modes of the clarinet", *JASA* 56 (1974); M. E. McIntyre, R. T. Schumacher and J. Woodhouse, "On the
oscillations of musical instruments", *JASA* 74 (1983); J.-P. Dalmont, J. Gilbert, J. Kergomard and
S. Ollivier, "An analytical prediction of the oscillation and extinction thresholds of a clarinet", *JASA* 118
(2005); H. Levine and J. Schwinger, "On the radiation of sound from an unflanged circular pipe", *Physical
Review* 73 (1948); A. N. Norris and I. C. Sheng, "Acoustic radiation from a circular pipe with an infinite
flange", *Journal of Sound and Vibration* 135 (1989); J. W. Coltman, "Sounding mechanism of the flute and organ
pipe", *JASA* 44 (1968); P. R. Cook, "A meta-wind-instrument physical model, and a meta-controller for real-time
performance control", *Proc. ICMC* (1992); S. Adachi and M. Sato, "Trumpet sound simulation using a
two-dimensional lip vibration model", *JASA* 99 (1996); A. E. Rosenberg, "Effect of glottal pulse shape on the
quality of natural vowels", *JASA* 49 (1971); G. E. Peterson and H. L. Barney, "Control methods used in a study
of the vowels", *JASA* 24 (1952); D. H. Klatt, "Software for a cascade/parallel formant synthesizer", *JASA* 67
(1980); K. Ishizaka and J. L. Flanagan, "Synthesis of voiced sounds from a two-mass model of the vocal cords",
*Bell System Technical Journal* 51 (1972); J. Sundberg, "Articulatory interpretation of the 'singing formant'",
*JASA* 55 (1974); E. Joliveau, J. Smith and J. Wolfe, "Tuning of vocal tract resonance by sopranos", *Nature*
427 (2004); C. Bergevin et al., "Overtone focusing in biphonic Tuvan throat singing", *eLife* 9 (2020);
A. Hirschberg, J. Gilbert, R. Msallam and A. P. J. Wijnands, "Shock waves in trombones", *JASA* 99 (1996);
C. Fritz and J. Wolfe, "How do clarinet players adjust the resonances of their vocal tracts for different
playing effects?", *JASA* 118 (2005); G. P. Scavone, A. Lefebvre and A. R. da Silva, "Measurement of vocal-tract
influence during saxophone performance", *JASA* 123 (2008); J.-M. Chen, J. Smith and J. Wolfe, "Experienced
saxophonists learn to tune their vocal tracts", *Science* 319 (2008), and "Pitch bending and glissandi on the
clarinet: roles of the vocal tract and partial tone hole closure", *JASA* 126 (2009).
