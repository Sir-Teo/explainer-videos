# Music, Built: Part 1, One String

Part 1 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). The founding legend of music theory, Pythagoras and the blacksmith's hammers, is
false; the monochord is true. This part asks why a string has a pitch at all, answers it from Newton's law, and
ends with the discovery that one string is already a chord. Every string in it is simulated by the series' own
instrument, Monochord (`explainer/music/monochord`), in `compute.py`; every sound is that simulation, played. Dates
and attributions are the published ones, listed under Sources.

* **The hammers.** The Tune's first phrase on one string; the legend (weights 12, 9, 8, 6; octave, fifth, fourth) as
  Nicomachus and Boethius tell it; why it is false twice (an anvil's ring belongs to the anvil; a string under twice
  the weight rises by half an octave, 600 cents, measured on the simulated string); Vincenzo Galilei's weights
  (4 : 1 for the octave); the monochord, where the ratios do hold; the two questions of the part and the series.
* **1. One string, four numbers.** The monochord (the *kanon*); the open string and its stops at 1/2, 2/3 and 3/4,
  each simulated and its frequency measured; frequency ratio = 1 / length ratio; an interval is a ratio, and
  intervals multiply (a fifth and a fourth make an octave; their difference is the tone, 9 : 8); the tetractys; a
  first question for the ear (which pair is the fifth?).
* **2. What sets the pitch.** Length, tension and mass, one at a time, on the simulated string; Mersenne's laws
  (*Harmonie universelle*, 1636) and Mersenne's count of a slow string's swings; the test: twenty-four random
  strings, pitch measured from the motion alone, exponents fitted (−1, 1/2, −1/2) and the constant (1/2).
* **3. A wave on a string.** A bump on a rope: it keeps its shape, travels at a steady speed, reflects upside down;
  the reflection as an image wave on an imaginary rope; superposition; the speed √(T/μ), timed in the simulation;
  the pitch of a string as the number of round trips per second, f = c / 2L, heard and seen in slow motion.
* **4. The wave equation.** The string as beads on a thread (Johann Bernoulli, Lagrange); the force on one bead,
  (T/h)(u₊ − 2u + u₋): each bead is pulled towards the midpoint of its neighbours; Newton's law for the bead is the
  simulation's whole physics (two lines of `physics/string.py`); 5, 15 and 199 beads, heard (the partials of a few
  beads are flat); the limit h → 0: ∂²u/∂t² = c² ∂²u/∂x² (d'Alembert, 1747); acceleration = c² × curvature, and
  why a plucked string can only start moving at its corner.
* **5. Two travelling waves.** f(x − ct) solves the equation for any f; d'Alembert's solution; a string released
  from rest is two half-height copies of its shape going opposite ways; the plucked string as straight lines and two
  running corners; the bead simulation against d'Alembert's formula (they differ by rounding error); the period
  2L/c, so f = (1/2L)√(T/μ): Mersenne's law derived, and independent of the shape.
* **6. Standing waves.** Shapes that swing in place: sin(nπx/L), frequencies n f₁; the first eight modes, their
  nodes, and each as a tone; the monochord's ratios are the ratios between neighbouring modes; a standing wave is
  two travelling waves; the touched harmonic, simulated (a finger at 1/2 leaves the even modes, at 1/3 modes 3, 6,
  9); Wallis's paper riders.
* **7. The quarrel.** d'Alembert (1747), Euler (1748), Daniel Bernoulli (1753), Lagrange (1759): can a sum of smooth
  sines make a corner?; the sum, added up and heard (1, 2, 3, 5, 10, 30 modes; the largest gap falls like 1/N);
  Fourier (1807) and Dirichlet (1829); thirty standing modes against two travelling shapes: one motion.
* **8. The plucked string.** Fourier's recipe as a question put to a shape (multiply by the mode, take the area);
  the result, aₙ ∝ sin(nπβ)/n²; modes with a node at the plucking point are missing; what the bridge feels,
  sin(nπβ)/n; four plucking points, simulated against the formula and heard; *sul tasto* and *sul ponticello*.
* **9. One string is a chord.** Mersenne's overtones and Sauveur's explanation; the spectrogram; one pluck taken
  apart, partial by partial: C, C, G, C, E, G, a flat B♭, C; partials 4, 5, 6 are a major chord; hearing one partial
  inside the whole; partial, fundamental, harmonic, overtone, timbre; how long each partial lasts.
* **10. Why the ratios?** Two strings as two ladders of partials: at 2 : 1 every partial of the upper meets one of
  the lower; at 3 : 2 and 4 : 3 fewer; at the tritone none, and near misses; beats (a fifth mistuned by 12 cents);
  a first answer to Pythagoras after Helmholtz (1863), and the three things it leaves out.
* **11. Real strings.** The ideal string never stops; where the energy goes; two loss terms, and each partial's
  decay rate, simulated against the model; stiffness, fₙ = n f₁ √(1 + Bn²), and what a stiffer wire sounds like.
* **12. Frontier: when the string stretches.** The tension is not constant (Kirchhoff, 1883; Carrier, 1945): a hard
  pluck starts sharp and glides down, simulated and heard; a scheme that conserves its energy exactly; what the
  model cannot do (Legge and Fletcher's missing modes that return), and what is open: strings that hit things.
* **13. What we will build.** Six answers to "why do simple ratios sound good?" in twenty-five centuries; Monochord
  and its layers; the Chain; the Tune and the Variations; the series' three rules.
* **Variation 1, recap and problems.** The Tune on one simulated string with one bridge in six positions; the
  ledger's first row; the recap; five problems; where this comes back; in practice; the reading list; Part 2.

## What is computed, and what is heard

`python -m videos.music.music1.compute` (under a minute) fills `.cache/music1/`. The string is the monochord's:
one metre of 0.5 mm steel wire, tuned to C3 (130.81 Hz), with the stiffness of that wire and losses chosen so that
its brightness fades before its pitch does (`explainer/music/monochord/instruments/plucked.py`).

| Item | What it computes | Checked against |
|---|---|---|
| `hammers` | the legend's weights on a string: √2 for 12 : 6, measured on the simulated string | the square-root law |
| `ratios` | the stops at 1/2, 2/3, 3/4: frequency measured from the motion | 2, 3/2, 4/3 (to 0.2 cents) |
| `mersenne` | pitch against L, T, μ; a power law fitted to 24 random strings | exponents −1, 1/2, −1/2; constant 1/2 |
| `pulse` | travelling, reflected and crossing pulses; the wave speed, timed | √(T/μ) |
| `beads` | the modes of 5, 15 and 199 beads | (cN/πL) sin(nπ/2N) |
| `dalembert` | the plucked ideal string by finite differences | d'Alembert's formula (10⁻¹⁵) |
| `modes` | a finger at 1/2 and 1/3 of a ringing string (a point damper) | which modes have a node there |
| `fourier` | partial sums of the pluck and their error | the 1/N law |
| `pluck` | partial levels of the bridge force at four plucking points | sin(nπβ)/n (to 0.4 dB) |
| `real` | each partial's decay, and its sharpening by stiffness | σ₀ + σ₁(nπ/L)²; n f₁√(1 + Bn²) |
| `nonlinear` | the stretching string (Kirchhoff–Carrier); the scheme's energy | √(mean tension) as a lower estimate; exact conservation |
| `tune` | Variation 1, and each note's interval above the open string | its ratio (to 0.6 cents) |

The three routes to the string's motion (beads, d'Alembert's formula, the sum of modes) are held against each other
in `tests/music/test_string.py`. The loudness meter that sets every clip's level is checked against ffmpeg's
`ebur128` in `tests/music/test_audio.py`.

**Sounds.** Thirty-odd clips, all labelled on screen: `physical model` (the bridge force of the simulated string,
by the sum of its modes or by finite differences) or `synthesized` (pure tones). There are no recordings. The only
composition rendered is the Tune, *Ah! vous dirai-je, maman* (anonymous, France, 18th century; public domain).
Clips that place two strings left and right are marked as needing headphones for the split; nothing in the part
depends on stereo.

## Build

```bash
python -m videos.music.music1.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music1 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music1                                # the sound gates
python tools/build.py music1                                   # 1080p30, narrated
python -m pytest -q tests/music                                # Monochord against its references
python -m videos.music.labs 1                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **A string's numbers.** A string 65 cm long with a mass of 3 g per metre is tuned to 110 Hz. Find its tension
   and the speed of a wave on it. What interval does it rise by if the tension is doubled?

   *Solution.* f = c / 2L, so c = 2Lf = 2 × 0.65 × 110 = **143 m/s**. c² = T/μ, so T = μc² = 0.003 × 143² =
   **61.3 N**, the weight of about 6.3 kg. Doubling T multiplies c, and so f, by √2: the string rises by
   1200 log₂ √2 = **600 cents, half an octave** (a tritone, to 155.6 Hz). This is the interval the legend's weights
   12 and 6 really give; an octave takes four times the tension.

2. **What the bridge feels.** Show that the force a plucked ideal string puts on its bridge is a rectangular wave
   that is high for the fraction β of each period, and recover the amplitudes sin(nπβ)/n from it.

   *Solution.* With F the odd, 2L-periodic extension of the plucked shape, u = ½[F(x − ct) + F(x + ct)]. The force
   on the end at x = 0 is T ∂u/∂x = ½T[F′(−ct) + F′(ct)] = T F′(ct), because the derivative of an odd function is
   even. For a pluck of height h at βL, F′ takes only two values: h/(βL) where |z| < βL (mod 2L), and
   −h/((1 − β)L) elsewhere. As ct runs through one period 2L, the first holds for a length 2βL, a fraction **β of
   the period**. A rectangular wave that is A for |θ| < πβ and B otherwise has cosine coefficients
   (2/π)(A − B) sin(nπβ)/n; here A − B = h/(Lβ(1 − β)), giving (2Th / πLβ(1 − β)) · **sin(nπβ)/n**. That is exactly
   T · aₙ · nπ/L with the aₙ of chapter 8. The narrow pulse of a string plucked near its end is why such a tone is
   bright, and why its peaks stand far above its loudness.

3. **Ear.** The lab plays three plucks of one note (`python -m videos.music.labs 1` writes
   `renders/labs/music/lab01.wav`). One was plucked a quarter of the way along. Which, and which partials told you?

   *Solution.* A pluck at 1/4 has no fourth, eighth or twelfth partial: every mode with a node at the plucking
   point is missing. On C3 the fourth partial is the C two octaves up (523 Hz) and the eighth the C above that.
   The pluck in the middle is the hollow one (no even partials at all), the pluck at a tenth is the bright, thin
   one, and the pluck at a quarter is between them, full in its low partials but without that high C. The lab's
   last row gives the order for the seed you ran.

4. **Build.** A hammer gives a string speed, not shape. Add a struck start to `simulate` in
   `explainer/music/monochord/physics/string.py` (an initial velocity v over a short stretch around βL, zero
   displacement) and show that its modes fall as 1/n where a pluck's fall as 1/n².

   *Solution.* The scheme needs the step before the start: for a pluck u(−k) = u(+k); for a strike u(−k) = u(0) −
   k v. Projecting the motion on the modes, a narrow strike gives velocity amplitudes ∝ sin(nπβ), hence
   displacement amplitudes ∝ sin(nπβ)/ωₙ ∝ **sin(nπβ)/n**. On the ideal monochord string struck over 2 cm at
   β = 1/5 (400 segments), the simulated mode amplitudes relative to the first are 0, −1.9, −5.5, −12.3 dB for
   n = 1…4 and −15.4 dB for n = 6, against 0, −1.8, −5.4, −12.0 and −15.6 dB from sin(nπβ)/n; the fifth mode is
   absent in both. A pluck at the same point gives 0, −7.9, −14.9, −24.1 and −31.1 dB. A struck string is brighter
   than a plucked one by a factor n in amplitude, 6 dB per octave: one reason a piano does not sound like a harp.
   At the bridge the factor n appears once more, so the force spectrum of an ideal strike is flat up to the
   hammer's width.

5. **★ A string against a curved bridge.** Model a string that meets a curved bridge as it swings (a sitar's or a
   tanpura's), with a scheme whose energy balance is exact, and compare its spectrum over time with the
   instrument's.

   *What is known.* A string that wraps and unwraps round a curved bridge changes its sounding length within each
   cycle, and energy is fed continually into its high partials: the instrument's buzz (*jawari*). Raman (1921)
   noted that the usual rule for a plucked string's missing partials fails on these instruments. Burridge, Kappraff
   and Morshedi (1982) analysed the sitar string as a string against a rigid, inelastic obstacle. Naive contact
   schemes are unstable. Stable ones treat the contact as a stiff one-sided spring whose potential is included in a
   conserved discrete energy (Bilbao, Torin and Chatziioannou, 2015), or work in modal coordinates with a penalty
   force (Issanchou et al., 2017).

   *How to attack it.* Add to the string's energy a term Σ (K/(α + 1)) [b(xᵢ) − uᵢ]₊^(α+1) for a barrier of shape
   b(x); derive the update from the discrete energy balance, so that the scheme is implicit only at the beads in
   contact; verify that energy is conserved to rounding when losses are off; then compare the spectral centroid
   over the first second with a measurement of a tanpura string. Open questions include how the bridge's own
   compliance and the cotton thread under the string (the *jiva*) should enter, and which features listeners
   actually use.

   *Where to start.* `simulate` and `energy` in `explainer/music/monochord/physics/string.py`; the series needs the
   result in Part 34.

## Sources

**Textbooks.** N. H. Fletcher and T. D. Rossing, *The Physics of Musical Instruments* (2nd ed., Springer, 1998),
ch. 2 (the string), sec. 2.11–2.18 (damping, stiffness, nonlinearity). A. H. Benade, *Fundamentals of Musical
Acoustics* (Oxford, 1976). S. Bilbao, *Numerical Sound Synthesis* (Wiley, 2009), ch. 6–8 (the schemes used here,
their stability and their energy). J. W. S. Rayleigh, *The Theory of Sound* (1877), ch. 6. H. von Helmholtz, *On
the Sensations of Tone* (1863; tr. Ellis), part II (beats and consonance).

**History.** H. F. Cohen, *Quantifying Music: The Science of Music at the First Stage of the Scientific
Revolution, 1580–1650* (Reidel, 1984), on Vincenzo Galilei and Mersenne. Galilei's experiments with weights are
usually dated to about 1588 and were printed in his *Discorso* of 1589; the film says "the fifteen-eighties". The
legend of the hammers is in Nicomachus, *Manual of Harmonics* (c. 100 CE), ch. 6, and Boethius, *De institutione
musica* (c. 510), I.10. M. Mersenne, *Harmonie universelle* (1636). J. Wallis, letter in *Philosophical
Transactions* 12 (1677), on the nodes. J. Sauveur, "Système général des intervalles des sons" (1701). B. Taylor
(1713). J. le Rond d'Alembert, "Recherches sur la courbe que forme une corde tendue mise en vibration" (1747).
L. Euler, "Sur la vibration des cordes" (1748). D. Bernoulli, "Réflexions et éclaircissements sur les nouvelles
vibrations des cordes" (1753). J.-L. Lagrange, "Recherches sur la nature et la propagation du son" (1759).
J. Fourier's memoir of 1807 and *Théorie analytique de la chaleur* (1822). For the quarrel as a whole: C. Truesdell,
*The Rational Mechanics of Flexible or Elastic Bodies, 1638–1788* (1960).

**The frontier.** C. V. Raman, "On some Indian stringed instruments", *Proc. Indian Assoc. Cultiv. Sci.* 7 (1921).
R. Burridge, J. Kappraff and C. Morshedi, "The sitar string, a vibrating string with a one-sided inelastic
constraint", *SIAM J. Appl. Math.* 42 (1982). G. Kirchhoff, *Vorlesungen über Mechanik* (1883); G. F. Carrier, "On the non-linear vibration
problem of the elastic string", *Quart. Appl. Math.* 3 (1945). K. A. Legge and N. H. Fletcher, "Nonlinear generation
of missing modes on a vibrating string", *J. Acoust. Soc. Am.* 76 (1984) 5–12. S. Bilbao, A. Torin and
V. Chatziioannou, "Numerical modeling of collisions in musical instruments", *Acta Acustica united with Acustica*
101 (2015) 155–173. C. Issanchou, S. Bilbao, J.-L. Le Carrou, C. Touzé and O. Doaré, "A modal-based approach to the
nonlinear vibration of strings against a unilateral obstacle", *J. Sound Vib.* 393 (2017) 229–251.

**Not claimed.** The film does not give lengths or counts for Mersenne's long strings, and it calls its estimate of
the pitch rise from stretching what it is, an estimate (the simulation gives about a fifth more).
