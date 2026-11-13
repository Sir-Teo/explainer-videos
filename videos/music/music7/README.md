# Music, Built: Part 7, Strings, Hammers and Bows

Part 7 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). For six parts the series has had one instrument, a plucked string, heard directly.
This part builds real instruments round it: a guitar, a piano and a violin. A string can be set going in three
ways, by plucking, striking and bowing, and each way is a different piece of physics; and no string can be heard
until it is fastened to a box. The instruments are Monochord's (`explainer/music/monochord/instruments/strings.py`);
every sound is computed in `compute.py`, and no instrument was recorded. Dates and attributions are the published
ones, listed under Sources.

* **Which is the Stradivari?** Four notes three times: plucked, struck, bowed, all from one string; the blind
  tests of Indianapolis (2010: thirteen of twenty-one players would take a new violin home) and Paris (2012: six
  of ten soloists); the plan.
* **1. A string cannot be heard.** A string is too thin to move air; a body takes its energy and radiates it; an
  ear question (the force on the bridge, bare and through a guitar's body: what did the body do?); the body as a
  filter with peaks; a knuckle on the bridge; the bargain a body makes (loud or long).
* **2. A plate, a hole and a box of air.** A guitar's two lowest resonances: Part 2's bottle with a flexible lid;
  the two-mass model; a worked example (cover the hole and the plate rings at 185 Hz, the air alone at 130: the
  pair appears at 98 and 204, pushed apart, and the squares add up); the dip between them; where the low E falls.
* **3. A pluck in three lines.** Karplus and Strong (1983): a loop of random numbers and an average; listening to
  the loop round by round; why three lines are enough (the loop is a string: a delay for the travelling wave, an
  average for the loss of high partials); the loop's length is the pitch, and why it is 2.8 cents out.
* **4. The hammer.** Cristofori (c. 1700): a hammer that is thrown; felt whose force rises as the squeeze to the
  power 2.5; three touches (contact 2.5, 2.1 and 1.9 ms; force 2, 7 and 20 N; brightness 380, 471 and 559 Hz); an
  ear question (struck hard and turned down, or struck softly and turned up?); a worked example (struck near an
  eighth of its length, the string takes up little of the blow in its eighth partial: 18 dB down).
* **5. A string that is also a bar.** Stiffness sharpens the high partials: f_n = n f₁ √((1 + Bn²)/(1 + B)); a
  worked example (B = 0.00038: the tenth partial is 32 cents sharp); an ear question (the real string, or its
  partials straightened?); wound bass strings, why pianos are long, the stretched octaves of Part 6.
* **6. Three strings for one note.** Loud or long; an ear question (one string; two in perfect unison; two a cent
  apart); Weinreich (1977): strings that move together are heard and die, strings that move oppositely are silent
  and last; the two-stage decay (31 dB a second, then 3); the tuner's imperfect unison; the soft pedal.
* **7. Stick and slip.** Rosin: sticky when still, slippery when sliding; the string's speed under the bow (stuck
  for nine tenths of the period, flying back for one tenth, 8.6 times as fast); Helmholtz's corner (1863); the
  force on the bridge is a sawtooth (partials as 1/n, to 0.2 dB), in ten steps because the bow sits at a tenth
  of the length; the bare force and the same force through a violin's body.
* **8. How hard to press.** Speed, force and place; an ear question (too much, right, too little); Schelleng's
  diagram (1973), with Monochord's own limits beside his formulas; a worked example (twice as near the bridge: the
  largest force doubles, the smallest quadruples, the sound is 6 dB louder and brighter); sul ponticello and sul
  tasto; the note has to be started (the bite; Guettler's diagram, 2002).
* **9. The violin's box.** The body's response: the air (275 Hz), the two body modes (460 and 540 Hz), the hill
  between 2 and 3 kHz; the open G below every resonance; vibrato moves each partial along the curve, so the
  recipe changes six times a second (by up to 7 dB); the wolf note.
* **10. Frontier: what makes a great violin?** The hotel room again, and the concert halls (137 listeners, 2017);
  what nobody can do yet: predict a preference, explain rosin, draw the true wedge, model felt; instruments made of
  arithmetic, from 244 numbers to millions. ★ research problem.
* **Variation 7, recap and problems.** The Tune on a guitar, a piano and a violin, alone, in pairs and together;
  the ledger; what we found; five problems; where it comes back; in practice; references; the bow's loop with air
  in place of rosin, and Part 8.

## What is computed, and what is heard

`python -m videos.music.music7.compute` (about fifteen seconds) fills `.cache/music7/`.

| Item | What it computes | Checked against |
|---|---|---|
| `three` | four notes by a plucked, a struck and a bowed model | every clip labelled and inside the loudness window |
| `body` | a plucked string's bridge force, bare and through a guitar body; the body's response; a tap | peaks of the response at the body's modes |
| `twomass` | a plate coupled to a Helmholtz resonator: the two coupled resonances and the dip | f₋² + f₊² = f_h² + f_p², to rounding |
| `ks` | Karplus–Strong, lap by lap; its pitch | the loop's true period, N + ½ samples: 2.8 cents |
| `hammer` | a felt hammer (F = K xᵖ) on a stiff, lossy string, by modal time-stepping, at three speeds | contact about 2 ms and shorter when harder (Hall; Chaigne and Askenfelt); little above the seventh partial |
| `stiff` | the partials of the stiff string; the same note with them straightened | Fletcher's formula; B = 0.00038 for middle C |
| `unison` | two strings on one yielding bridge: one, a perfect pair, a pair a cent apart | Weinreich: a pair in unison decays twice as fast; mistuned, in two stages |
| `bow` | a bowed string with a friction curve, by travelling waves: speed under the bow, bridge force | slip for the fraction β; flyback (1 − β)/β; partials as 1/n to 0.2 dB |
| `schelleng` | the largest and smallest bow force at eight bow positions; three notes | Schelleng's formulas: slopes −1.1 and −2.5 against −1 and −2 |
| `violin` | a violin body's response; one bowed note held still and with vibrato | signature modes at 275, 460 and 540 Hz; a hill at 2.5 kHz |
| `tune` | Variation 7: the Tune for the three instruments | the plan of who plays each phrase |

Monochord's string instruments are held against these references in `tests/music/test_strings.py`; this part's
claims and clips in `tests/music/test_music7.py`.

**Sounds.** Twelve clips, labelled on screen. `physical model`: the plucked, struck and bowed strings and the bodies
they drive. `synthesized`: Karplus and Strong's loop, which is noise in a delay line. The straightened note of chapter 5 is
the struck-string model with its partials moved onto whole multiples. There are no recordings.

**What the models are, and are not.** The string is Part 1's: stiff, lossy, linear. *The guitar and violin bodies*
are filters: a sum of resonances with chosen frequencies, strengths and dampings (a guitar's first two from the
two-mass model; a violin's signature modes and hill at typical published values), not a solved wooden box, and
they radiate in no particular direction. *The hammer* is the standard power-law felt with no hysteresis. *The
paired strings* are two modes coupled through a purely resistive bridge, the simplest case of Weinreich's
analysis; a real bridge is also reactive, and a real string has two polarisations (Problem 4). *The bow* is a
point, with a friction that depends only on sliding speed, on a string without torsion: the model of McIntyre,
Schumacher and Woodhouse, which reproduces the Helmholtz motion and Schelleng's limits in outline but is known to
be wrong in detail (chapter 10). Its minimum bow force is two to six times Schelleng's, and was found by easing
the force down from a note already sounding, because the motion is hysteretic. *Vibrato* is the bowed force read
at a wavering speed and then filtered by the body, which is the right order. The violins of the blind tests are
not modelled at all: the film reports the published results.

## Build

```bash
python -m videos.music.music7.compute                          # numbers and sounds (about fifteen seconds)
EXPLAINER_TTS=silent python tools/build.py music7 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music7 --sync                         # the sound gates
python tools/dead_air.py renders/music7_480p.mp4 --sound music7   # no empty screen; no sound over a still one
python tools/lecture_length.py music7                          # 30 to 60 minutes, listening included
python tools/build.py music7                                   # 1080p30, narrated
python -m pytest -q tests/music                                # Monochord against its references; this part's claims and clips
python -m videos.music.labs 7                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **A stiff string.** A piano string has B = 0.0004 and a fundamental of 262 Hz. Find the frequencies of its 2nd,
   4th and 8th partials, and how many cents sharp each is of a whole multiple.

   *Solution.* f_n = n f₁ √((1 + Bn²)/(1 + B)). For n = 2 the factor is √(1.0016/1.0004) = 1.00060, so the
   partial is at 524.3 Hz, 1.0 cent sharp of 524. For n = 4: √(1.0064/1.0004) = 1.00299, 1051.1 Hz, 5.2 cents.
   For n = 8: √(1.0256/1.0004) = 1.01252, 2122.2 Hz, 21.5 cents. The sharpness grows nearly as n² − 1: each
   doubling of n multiplies it by about four. An octave tuned so that the upper note's fundamental matches this
   string's second partial is 1 cent wide; tuned to the fourth partial of the note two octaves down, 5 cents.
   (The lab computes all three.)

2. **Helmholtz's corner.** For a string in Helmholtz motion bowed at a fraction β of its length from the bridge,
   show that it slips for the fraction β of each period, and that it flies back (1 − β)/β times as fast as the bow.

   *Solution.* The corner travels at the wave speed c and goes once round the string, a distance 2L, in one
   period T = 2L/c. The string under the bow slips while the corner is between the bow and the bridge: it passes
   the bow going towards the bridge, travels βL, reflects and travels βL back, which takes 2βL/c = βT. For the
   remaining (1 − β)T the string sticks and moves with the bow at speed v, a distance v(1 − β)T. In a steady
   motion the string must be back where it began after one period, so the slip covers the same distance the other
   way in the time βT: its speed is v(1 − β)T / (βT) = v(1 − β)/β. At β = 1/10 that is nine times the bow's
   speed; Monochord's simulated string, with rounded corners, manages 8.6.

3. **Ear.** The lab plays one bowed note at five bow forces, in a random order. Put them in order of force, and
   say which lie outside Schelleng's wedge.

   *Solution.* The lab prints the order and the regime of each. Too little force gives a thin, whistling tone an
   octave or more above the note mixed with it (several slips a period); too much gives a growl at a lower,
   unsteady pitch. Within the wedge the pitch is steady and the notes differ only in brightness: more force, a
   sharper corner, more high partials. Two of the lab's five are outside, one on each side.

4. **Build.** Add a second polarisation to `strings.pair`: each string can also move parallel to the soundboard,
   where the bridge hardly yields. Does one string alone now decay in two stages?

   *Solution.* Yes, if the hammer's blow is not exactly perpendicular to the soundboard or the bridge couples the
   two directions slightly. The motion perpendicular to the board drives the bridge hard and decays quickly; the
   motion parallel to it meets a nearly rigid bridge and decays slowly. One string is then itself a pair of
   oscillators with a fast and a slow mode, and its level against time has the same knee as the mistuned pair's.
   Weinreich (1977) gives both mechanisms; in a real piano the polarisations account for the two-stage decay of
   single-strung bass notes, and the mistuned unisons shape it in the rest of the compass.

5. ★ **Warm rosin.** Replace the bow's friction curve by one that depends on the rosin's temperature, warmed by
   sliding and cooled by conduction. How do Schelleng's limits and the starting transient change?

   *Where the frontier is.* Smith and Woodhouse (2000) measured rosin's friction in a stick-slip rig and found
   that it is not a function of sliding speed: plotted against speed it traces a loop, and a model in which the
   friction depends on the temperature of a thin layer of rosin fits much better. Woodhouse (2003) put that model
   into a bowed-string simulation; it is more ready to settle into the Helmholtz motion, as real strings are.
   Galluzzo and Woodhouse (2014) measured both Schelleng's and Guettler's diagrams with a bowing machine and
   compared them with the two models: each gets some features right and neither gets them all. A model of the
   contact that predicts both diagrams for a real string, with a finite width of hair and with torsion, has not
   been written.

## Sources

Books: N. H. Fletcher and T. D. Rossing, *The Physics of Musical Instruments* (2nd ed., 1998), chs. 9–12, for the
guitar's two-mass model, the bowed string and the piano; L. Cremer, *The Physics of the Violin* (1984); A. Chaigne
and J. Kergomard, *Acoustics of Musical Instruments* (2016); S. Bilbao, *Numerical Sound Synthesis* (2009);
H. von Helmholtz, *On the Sensations of Tone* (1863; trans. Ellis), ch. 5 and appendix 6, for the vibration
microscope and the bowed string's motion; S. Pollens, *The Early Pianoforte* (1995), for Cristofori and the Medici
inventory of 1700.

Papers: G. Weinreich, "Coupled piano strings", *JASA* 62 (1977); H. Fletcher, "Normal vibration frequencies of a
stiff piano string", *JASA* 36 (1964); D. E. Hall, "Piano string excitation in the case of small hammer mass",
*JASA* 79 (1986), and its sequels; A. Chaigne and A. Askenfelt, "Numerical simulations of piano strings", I and
II, *JASA* 95 (1994); K. Karplus and A. Strong, "Digital synthesis of plucked-string and drum timbres", and D. A.
Jaffe and J. O. Smith, "Extensions of the Karplus-Strong plucked-string algorithm", *Computer Music Journal* 7
(1983); O. Christensen and B. B. Vistisen, "Simple model for low-frequency guitar function", *JASA* 68 (1980);
C. V. Raman, "On the mechanical theory of the vibrations of bowed strings", *Bulletin of the Indian Association
for the Cultivation of Science* 15 (1918); J. C. Schelleng, "The bowed string and the player", *JASA* 53 (1973);
M. E. McIntyre, R. T. Schumacher and J. Woodhouse, "On the oscillations of musical instruments", *JASA* 74
(1983); K. Guettler, "On the creation of the Helmholtz motion in bowed strings", *Acta Acustica united with
Acustica* 88 (2002); E. Schoonderwaldt, K. Guettler and A. Askenfelt, "An empirical investigation of bow-force
limits in the Schelleng diagram", *Acta Acustica united with Acustica* 94 (2008); J. H. Smith and J. Woodhouse,
"The tribology of rosin", *Journal of the Mechanics and Physics of Solids* 48 (2000); J. Woodhouse, "Bowed string
simulation using a thermal friction model", *Acta Acustica united with Acustica* 89 (2003); P. M. Galluzzo and
J. Woodhouse, "High-performance bowing machine tests of bowed-string transients", *Acta Acustica united with
Acustica* 100 (2014); M. V. Mathews and J. Kohut, "Electronic simulation of violin resonances", *JASA* 53 (1973);
J. Woodhouse, "The acoustics of the violin: a review", *Reports on Progress in Physics* 77 (2014); A. Stulov,
"Hysteretic model of the grand piano hammer felt", *JASA* 97 (1995); C. Fritz, J. Curtin, J. Poitevineau,
P. Morrel-Samuels and F.-C. Tao, "Player preferences among new and old violins", *PNAS* 109 (2012); C. Fritz et
al., "Soloist evaluations of six Old Italian and six new violins", *PNAS* 111 (2014); C. Fritz et al., "Listener
evaluations of new and Old Italian violins", *PNAS* 114 (2017); C. Saitis, B. L. Giordano, C. Fritz and G. P.
Scavone, "Perceptual evaluation of violins: a quantitative analysis of preference judgments by experienced
players", *JASA* 132 (2012).
