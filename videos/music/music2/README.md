# Music, Built: Part 2, Waves in Air

Part 2 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). A string on its own is nearly silent; what reaches the ear is the air. This part
asks what a sound wave is, why it travels at the speed it does, how its strength is measured, and why it bends round
walls, hums in a bottle and drops in pitch as it passes. Every picture of air in it is simulated by Monochord's
second layer (`explainer/music/monochord/physics/air.py`), and every sound is computed in `compute.py`. Dates and
attributions are the published ones, listed under Sources.

* **Krakatoa.** The Tune's first phrase on six bottles; the eruption of 27 August 1883, heard at Batavia (160 km),
  Perth (3,110 km) and Rodrigues (4,800 km, about four hours later); the pressure pulse recorded by barographs
  seven times in five days, at 674 to 726 miles an hour (the Royal Society's report): the speed of sound. The
  part's questions.
* **1. Sound needs air.** Boyle's watch in the jar (1660); a small source radiates power in proportion to the
  density round it; the monochord in the jar with all, a tenth, a hundredth and a thousandth of the air; sound
  in other media (helium 1,007 m/s, water 1,481, a steel rod about 5,000): speed = √(stiffness / density).
* **2. What moves.** A row of simulated parcels carries a push and each parcel stays home; pressure against
  displacement in a steady tone; longitudinal waves; how small the motion is (speech: 0.02 Pa, 11 nm at 1 kHz).
* **3. The speed of sound.** Newton's √(P/ρ) (1687), 15 percent short; Laplace's adiabatic correction (1816); the
  two gas laws raced in the simulation (280 and 331 m/s, no speed written into the code); c = √(γRT); a pipe 25
  degrees warmer is 74 cents sharper; why Krakatoa's pulse ran at 313 m/s.
* **4. How loud.** Intensity and its range; the bel and the decibel; +10, +3 and +6 dB; four notes 6 dB apart; one
  string, two and ten (this group +7.9 dB, the average of 24 groups +9.8); an ear question (3 dB or 6 dB?).
* **5. Spreading out.** The inverse-square law from the area of a sphere; the simulated spherical ray falls as
  r^−1.000, 6.02 dB per doubling (in the plane of our pictures, about 3); a string at 1, 2, 4 and 8 metres.
* **6. Round the corner.** Wavelength, from 17 m to 17 mm; a four-metre wall at 170 Hz and at 1,360 Hz (Huygens,
  1678); the loss behind it at each frequency, within 2 dB of Maekawa's chart (1968); the Tune in the open and
  behind the wall.
* **7. Two sources.** Waves add; the striped field of two sources 1.2 m apart at 850 Hz; path differences of whole
  and half wavelengths (Young, 1801); a walk across the pattern, simulated against the exact field.
* **8. Air in a pipe.** Reflection at closed and open ends; f = n c/2L and (2n − 1) c/4L, simulated to a
  hundredth of a cent; the pipes struck and blown; the end correction measured on a pipe in the plane (and 0.61 r
  for a round pipe: Levine and Schwinger, 1948); an ear question (open or stopped?).
* **9. A bottle.** Helmholtz's resonator as a mass on a spring; a 330 ml bottle by the formula (177.4 Hz), by the
  exact two-tube root (171.8) and simulated (171.7); its note as it fills; where the same resonator hides.
* **10. Why a string needs a box.** Impedance; a pulse at a pipe four times as wide (−0.59 comes back; formula
  −0.60); air to water (0.11 percent gets in); a flare against a sudden opening (98 percent against 22).
* **11. A source that moves.** Crowded and stretched wavefronts (Doppler, 1842); Buys Ballot's trumpeters on the
  Utrecht–Maarssen line (1845) and the 71 km/h a semitone each way needs; why the pitch glides; an ear question
  (which car was faster?).
* **12. Frontier: when sound is too loud to be linear.** Steepening; the gas chain against Fubini's solution (1935)
  to 0.0001; shock waves in trombones (Hirschberg et al., 1996) and the "brassy" sound; thermoacoustics; Tonga
  2022. ★ research problem.
* **Variation 2, recap and problems.** The Tune on six bottles, tuned by their water; the ledger; what we found;
  five problems; where it comes back; in practice; references; Part 3.

## What is computed, and what is heard

`python -m videos.music.music2.compute` (about two minutes) fills `.cache/music2/`.

| Item | What it computes | Checked against |
|---|---|---|
| `krakatoa` | travel times at the reported speed of the pulse; the Tune's first phrase on bottles | the Royal Society's figures (cited) |
| `vacuum` | the level of a small source at 1, 1/10, 1/100, 1/1000 atmosphere | power ∝ density |
| `parcels` | a pulse and a tone in a row of gas parcels; pressure, velocity and displacement at 30 to 130 dB | p = ρc u |
| `speed` | the pulse's speed under Boyle's law and under the adiabatic law; a pipe at 5 and 30 °C | √(P/ρ) and √(γP/ρ) (to 0.1%); c ∝ √T |
| `decibel` | steps of 6 dB; one, two and ten strings, one group and the mean of 24 | 10 log₁₀ k |
| `spread` | pressure against distance on a spherical ray and in the plane | r⁻¹ (exponent −1.000) and r^−½ |
| `diffraction` | the field round a 4 m wall; the loss at the listener from 80 Hz to 1.7 kHz | Maekawa's chart (within 2.1 dB) |
| `interfere` | the field of two sources and its rms along a line | the exact two-source field (Hankel functions), within 8% of the peak |
| `tubes` | resonances of open and stopped pipes; a stopped pipe radiating in the plane | n c/2L, (2n − 1) c/4L (0.01 cents); the end correction, measured |
| `bottle` | a neck on a body by simulation; its note at nine fillings | the exact two-tube root (0.6 cents); Helmholtz's formula (56 cents sharp) |
| `impedance` | reflection at a 1 : 4 step; energy through a 1 : 16 opening, sudden and flared | (S₁ − S₂)/(S₁ + S₂); 4r/(1 + r)² |
| `doppler` | a passing source by retarded time; the picture of a moving source in the plane | f c/(c ∓ v) |
| `nonlinear` | a 161 dB tone steepening in the gas chain; harmonics at four distances | Fubini's solution (to 0.0001); the shock distance |
| `tune` | Variation 2: six fillings from the two-tube root, each bottle simulated and its pitch measured | its note (within 1 cent) |

The simulators are held against their references in `tests/music/test_air.py`; this part's claims and clips in
`tests/music/test_music2.py`.

**Sounds.** Nineteen clips, all labelled on screen. `physical model`: the monochord's string from Part 1 (at
computed levels), and pipes and bottles given one push of air or a breath of noise, heard as the simulated flow at
the mouth. `synthesized`: the tone walked through the interference pattern and the passing horn, whose level and
pitch come from the computed field and from retarded time. There are no recordings. Short, sharp sounds (struck
pipes and bottles) are set by their peaks, not their loudness, so that nothing passes the peak ceiling.

**Three things the film simplifies.** The pictures of sound "from above" are two-dimensional: sound in a sheet of
air spreads as r^−½, not r⁻¹, which chapter 5 says on screen. The pipes and bottles are struck or fed with noise;
a blown pipe is a self-sustained oscillation, which Part 8 builds. The radiation losses of the pipes and the
bottle are chosen (a quality factor of about 33), as the string's losses were in Part 1.

## Build

```bash
python -m videos.music.music2.compute                          # numbers and sounds (about two minutes)
EXPLAINER_TTS=silent python tools/build.py music2 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music2 --sync                         # the sound gates
python tools/dead_air.py renders/music2_480p.mp4 --sound music2   # no empty screen; no sound over a still one
python tools/lecture_length.py music2                          # 30 to 60 minutes, listening included
python tools/build.py music2                                   # 1080p30, narrated
python -m pytest -q tests/music                                # Monochord against its references; this part's claims and clips
python -m videos.music.labs 2                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **An organ pipe.** A pipe open at both ends sounds 440 Hz at 20 °C. How long is it (ignore the end correction)?
   What does it sound at 10 °C, and how many cents flat is that?

   *Solution.* At 20 °C, c = √(γRT) = 343.2 m/s, and an open pipe sounds c/2L, so L = 343.2 / 880 = 0.390 m. At
   10 °C, c = 337.3 m/s and the pipe sounds 337.3 / 0.780 = 432.4 Hz. The interval is 1200 log₂(337.3 / 343.2) =
   −30 cents: nearly a third of a semitone flat. (In general the pitch moves by half the relative change in
   absolute temperature: about 3 cents per degree.)

2. **Helmholtz's formula.** Derive it from the mass of the air in the neck and the adiabatic stiffness of the air
   in the body, and show that it is the long-wavelength limit of tan(kLₙ) tan(k L_b) = Aₙ / A_b.

   *Solution.* The air in the neck has mass m = ρ Aₙ Lₙ. Push it in by x: the body's volume falls by Aₙ x, and
   adiabatically its pressure rises by γP Aₙ x / V = ρc² Aₙ x / V. The force back on the plug is that pressure
   times Aₙ, so the spring constant is k = ρc² Aₙ² / V and ω² = k/m = c² Aₙ / (V Lₙ): f = (c/2π) √(Aₙ / (V Lₙ)).
   For the two-tube model, the body (closed at the bottom) presents the impedance −i (ρc/A_b) cot(k L_b) to the
   neck, and the neck, open at the top, needs i (ρc/Aₙ) tan(k Lₙ) at its lower end; equating them gives
   tan(kLₙ) tan(k L_b) = Aₙ / A_b. When both lengths are much shorter than a wavelength, tan θ ≈ θ and
   k² Lₙ L_b = Aₙ / A_b, that is k² = Aₙ / (Lₙ V) with V = A_b L_b: Helmholtz's formula. The next term of the
   tangent makes the true root lower, which is why the formula runs sharp (56 cents for the film's bottle).

3. **Ear.** The lab (`python -m videos.music.labs 2`) plays a horn passing three times. Put the passes in order of
   speed, and estimate the fastest from the interval it falls by.

   *Solution.* The horn passes at 10, 20 and 35 m/s in an order the lab prints after you have listened. The whole
   fall, from approach to retreat, is 1200 log₂((c + v)/(c − v)) cents: 101, 202 and 354 cents, so the three are a
   semitone, a whole tone and a minor third and a half. Turning it round, a fall by the ratio r gives
   v = c (r − 1)/(r + 1); a fall of 354 cents is r = 1.227 and v = 35 m/s (126 km/h).

4. **Build.** Give `air.tube` a side hole (a short open branch) and find where to drill one in a 60 cm pipe to
   raise its note by a whole tone.

   *Solution sketch.* A branch is one more cell joined to a face: its flow leaves the main pipe there, and its far
   end is open (pressure zero). A hole as wide as the bore is nearly an open end, so the pipe sounds as if it
   stopped at the hole: for a whole tone (9 : 8) in a pipe open at both ends, the sounding length must be 8/9 of
   60 cm, and the hole goes 6.7 cm from the end. A narrower or deeper hole is a weaker short circuit (it is a
   small mass of air, as in the bottle's neck), so it must be drilled further up to do the same job; your
   simulation should approach 6.7 cm as the hole widens and move toward the top as it narrows. This is the first
   step of Part 8's flute.

5. **★ Research.** Model a trombone's bore with nonlinear propagation and a radiating bell, and predict the
   playing level at which its spectrum turns brassy.

   *Pointers.* Start from the gas chain of this part with a varying cross-section (the quasi-one-dimensional
   Euler equations), add wall losses, and terminate it with a bell whose radiation impedance you take from the
   literature. Hirschberg et al. (1996) give measured mouthpiece pressures; Gilbert, Campbell, Myers and Pyle's
   "brassiness potential" (2007 onward) is the design number to reproduce; Msallam et al. (2000) is a
   time-domain model to compare with. Open questions: how much of the brightness is steepening and how much is
   the lips; and how bore profile trades brassiness against intonation.

## Sources

Books: L. E. Kinsler, A. R. Frey, A. B. Coppens and J. V. Sanders, *Fundamentals of Acoustics* (4th ed., 2000);
A. D. Pierce, *Acoustics* (3rd ed., 2019); T. D. Rossing, F. R. Moore and P. A. Wheeler, *The Science of Sound*
(3rd ed., 2002); N. H. Fletcher and T. D. Rossing, *The Physics of Musical Instruments* (2nd ed., 1998), ch. 6–8;
H. von Helmholtz, *On the Sensations of Tone* (1863; tr. Ellis) for the resonator.

History: R. Boyle, *New Experiments Physico-Mechanicall, Touching the Spring of the Air* (1660), experiment 27;
I. Newton, *Principia* (1687), Book II, prop. 49–50 (979 feet a second); P.-S. Laplace, "Sur la vitesse du son dans
l'air et dans l'eau", *Annales de chimie et de physique* 3 (1816); C. Huygens, *Traité de la lumière* (written 1678);
T. Young, Bakerian lecture (1801); C. Doppler (1842) and C. H. D. Buys Ballot, "Akustische Versuche auf der
Niederländischen Eisenbahn", *Annalen der Physik* 66 (1845); G. J. Symons (ed.), *The Eruption of Krakatoa and
Subsequent Phenomena* (Royal Society, 1888), for the distances, the seven passages and the speed of the pulse.

Papers: H. Levine and J. Schwinger, "On the radiation of sound from an unflanged circular pipe", *Physical Review*
73 (1948) 383–406; Z. Maekawa, "Noise reduction by screens", *Applied Acoustics* 1 (1968) 157–173; E. Fubini,
"Anomalie nella propagazione di onde acustiche di grande ampiezza", *Alta Frequenza* 4 (1935) 530–581;
A. Hirschberg, J. Gilbert, R. Msallam and A. P. J. Wijnands, "Shock waves in trombones", *JASA* 99 (1996)
1754–1758; G. W. Swift, "Thermoacoustic engines", *JASA* 84 (1988) 1145–1180.
