# Music, Built: Part 9, Drums, Bars and Bells

Part 9 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the last part of Act I. Strings and columns of air are long and thin, and
their overtones are nearly whole multiples of the fundamental. Skins, bars, plates and bells are not so obliging:
nature tunes them badly, and for three thousand years makers have been retuning them, with air, paste, a knife, a
lathe and a hammer. The part computes what nature gives and what the makers did about it, and ends on the
opposite question, Kac's: if you knew every overtone of a drum, would you know its shape? The instruments are
Monochord's (`explainer/music/monochord/instruments/percussion.py`); every sound is computed in `compute.py`.
Dates and attributions are the published ones, listed under Sources.

* **Can one hear the shape of a drum?** A string and a drum on the same lowest frequency; their overtones (1, 2,
  3, 4 against 1, 1.59, 2.14, 2.30); Kac's question (1966) and the two drums of 1992; the plan.
* **1. A skin.** The modes of a round skin: still diameters and still circles; a worked example (the zeros of two
  Bessel functions, 3.832/2.405 = 1.593: 806 cents, not an interval); an ear question (struck at the centre, or
  off it?); why the modes with no diameter die fast, and where a timpanist strikes.
* **2. A drum with a note.** The ringing modes of an ideal skin (1, 1.34, 1.66, 1.98, 2.29); an estimate of the
  air's load (1, 1.42, 1.83, 2.24, 2.64); a kettledrum as measured (1, 1.50, 1.98, 2.44, 2.91); an ear question
  (a bare skin and a kettledrum); four notes; which octave the ear hears, and what a model of the ear says.
* **3. A patch of paste.** Raman on the tabla (1920): a fundamental and four harmonics; a skin with a centre ten
  times as heavy, out to 0.4 of the radius: nine modes gathered at 1, 2, 3, 4, 5 (the worst miss falls from 569
  cents to 56); the bare and the loaded skin compared.
* **4. Bars.** A worked example (a bar's frequency goes as thickness over length squared: half the length is two
  octaves); the modes of a free bar (1 : 2.76 : 5.40); the arch: 65% deep for a marimba (1 : 4.00 : 10.0, and the
  note itself 1.6 octaves lower), 18% for a xylophone (1 : 3.00 : 6.1); an ear question (plain or carved?); the
  stopped tube under each bar; a soft mallet and a hard one (1.6 and 0.25 ms on the bar).
* **5. Bells.** The partials of a tuned bell (hum, prime, tierce, quint, nominal ...); the Hemonys and van Eyck
  (1644); five partials heard one at a time, and then the bell; the strike note as a missing fundamental (the ear model, given the partials at 2, 3 and 4, returns the
  prime's 262 Hz); the minor third in every bell; an ear question (the old kind and the new); the major-third
  bell of the 1980s; a major chord on each kind.
* **6. Plates and sand.** Chladni's figures (1787), in Ritz's approximation; Napoleon's prize, Sophie Germain
  (1816), Kirchhoff, Ritz; a violin maker's glitter.
* **7. Gongs and cymbals.** When pitch depends on loudness: a gong that falls a whole tone as it fades and one
  that rises; a cymbal as 420 partials with no pattern, and the cascade that makes a crash (a sketch).
* **8. The steelpan.** Trinidad, the 1930s and 1940s; a note as a small dome; tuning the dome's first three modes
  to 1 : 2 : 3 with a hammer; the note before tuning and built up.
* **9. Hearing a shape.** Weyl's law: the overtones give the area and the rim; a worked example (twice the area:
  the hundredth mode falls from 1000 to 707 Hz); Gordon, Webb and Wolpert's two drums (1992), computed: six
  eigenvalues of each, equal to thirteen decimal places, and within 0.1% of Driscoll's published values; why they
  agree (a mode of one, cut into seven triangles, reassembles on the other); an ear question (two of three drums have the same notes); the answer to Kac.
* **10. Frontier: what the ear knows about things.** Hearing material, size and shape; which outlines can be
  heard; the cymbal's cascade; design run backwards, from the overtones wanted to a shape. ★ research problem.
* **Variation 9, recap and problems.** The Tune on a marimba, bells, a steelpan and kettledrums; the ledger; what
  we found; five problems; where it comes back; in practice; references; the end of Act I, and Part 10.

## What is computed, and what is heard

`python -m videos.music.music9.compute` (about ten seconds) fills `.cache/music9/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | Part 1's string and an ideal drum on one note | the Bessel ratios |
| `skin` | the modes of a round skin; how strongly a blow at each radius starts them | zeros of J₀ … J₅ (SciPy); a central blow starts only m = 0 |
| `timpani` | the (m,1) modes bare and with an estimate of the air's load; a kettledrum's measured modes as sound | Rossing's measurements (1, 1.50, 1.98, 2.44, 2.91) |
| `tabla` | a skin with a heavy central disc, by finite differences in the radius; the miss against the patch's weight | no load gives Bessel's zeros; Ramakrishna and Sondhi's patch (0.4, 9.76) |
| `bars` | a free bar of any thickness profile, by beam finite elements; arches tuned to 1 : 4 and 1 : 3 | the uniform bar's 1 : 2.7565 : 5.4039 : 8.9330 |
| `bells` | a bell from published partials; the pitch a model of the ear gives its partials at 2, 3 and 4 | the prime, to a fraction of a cent |
| `plates` | eight Chladni figures of a free square plate | Ritz's two-term approximation (not a solved plate) |
| `gongs` | modes whose frequency depends on their amplitude; a cymbal sketched from 420 partials | — |
| `shape` | the two isospectral drums by finite elements on a criss-cross mesh; a square of the same area; Weyl's count | each other (1e-13); Driscoll's 2.53794, 3.65551, 5.17556 (within 0.1%) |
| `tune` | Variation 9 | the plan of who plays each phrase |

Monochord's percussion is held against these references in `tests/music/test_percussion.py`; this part's claims
and clips in `tests/music/test_music9.py`.

**Sounds.** Sixteen clips, labelled on screen. `physical model`: sounds made from modes that Monochord computed
(the skins, the bars, the three drums of chapter 9) or that were measured on a real instrument and are cited (the
kettledrum). `synthesized`: sounds made from a list of partials that was not computed here (bells, the steelpan),
or from a rule (the gongs, the cymbal). There are no recordings.

**What the models are, and are not.** Every sound in this part is *modal*: a sum of partials, each with a
frequency, a strength and a rate of decay. The frequencies are the content; strengths and decays are plausible
choices (a blow's strength in each mode of a skin follows the mode's shape at the point struck; modes of a drum
with no nodal diameter are made to die four times as fast, because they radiate well). *The kettledrum's* air
loading is estimated by one formula, the mass of air a wave of given wavelength carries; it moves the modes the
right way and about half far enough, and the film shows the measured values beside it. *The tabla* is a membrane
with a step in its density; a real syahi is also stiff and graded. *The bar* is an Euler-Bernoulli beam; real
bars are thick enough for shear to matter in the higher modes, and makers cut in more than one place. *The bell*
is not computed: its partials are the published ratios of a tuned bell, and the major-third bell differs only in
its tierce. *Chladni's figures* use Ritz's first approximation. *The gongs* are single modes with an
amplitude-dependent frequency, the simplest thing that glides; *the cymbal* is a sketch in which the late arrival
of the high partials was written in by hand, and the film says so. *The steelpan* is a list of partials. The
ear model is Part 4's; it is used for two statements (the bell's strike note from three partials, and the
kettledrum's sub-octave), and the second is reported as a disagreement with what listeners say.

## Build

```bash
python -m videos.music.music9.compute                          # numbers and sounds (about ten seconds)
EXPLAINER_TTS=silent python tools/build.py music9 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music9 --sync                         # the sound gates
python tools/dead_air.py renders/music9_480p.mp4 --sound music9   # no empty screen; no sound over a still one
python tools/lecture_length.py music9                          # 30 to 60 minutes, listening included
python tools/build.py music9                                   # 1080p30, narrated
python -m pytest -q tests/music                                # Monochord against its references; this part's claims and clips
python -m videos.music.labs 9                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **A drumhead.** The first zeros of the Bessel functions J₀, J₁, J₂ are 2.405, 3.832 and 5.136. A drumhead 60 cm
   across has its lowest mode at 80 Hz. Find its next two modes in hertz and in cents above the lowest, and the
   speed of waves on the skin.

   *Solution.* The frequencies are in proportion to the zeros: 80 × 3.832/2.405 = 127.5 Hz and 80 × 5.136/2.405 =
   170.8 Hz. In cents, 1200 log₂(1.593) = 806 and 1200 log₂(2.136) = 1314: a narrow minor sixth, and an octave and a
   wide semitone. A mode's frequency is f = c z/(2πa), so c = 2π × 0.30 × 80/2.405 = 62.7 m/s, a fifth of the
   speed of sound in air. (The lab computes all of these.)

2. **A bar.** A bar's stiffness goes as its width times the cube of its thickness, and its mass per length as width
   times thickness. Show, by dimensions, that its frequency goes as thickness over length squared, and that the
   width cancels.

   *Solution.* The bending stiffness is EI with I = wh³/12, and the mass per length is ρwh. The only combination
   of EI (N m²), ρwh (kg/m) and the length L (m) with the dimensions of a frequency is √(EI/(ρwh))/L². Inside the
   root w cancels and h³/h leaves h²: f ∝ (h/L²)√(E/ρ). So the frequency is proportional to the thickness, to the
   inverse square of the length, and to the speed of sound in the material; and a marimba maker can choose the
   width of a bar for the player's convenience.

3. **Ear.** The lab strikes five bells in a random order: some have a minor third among their partials, some a major
   third. Say which is which.

   *Solution.* The lab prints the order. The two differ in one partial, at 1.2 or 1.25 times the note: 316 or 386
   cents above the prime, 70 cents apart. Most people hear the minor-third bell as darker and more "bell-like", and
   the major-third bell as sweeter and a little like a struck glass; it is easier in chords than on single notes.

4. **Build.** With `percussion.bar_modes`, find a cut, not a simple arch, that puts a bar's overtones at exactly 4
   and 10 times its note. Where must wood come off to move the third mode alone?

   *Solution.* One handle moves one ratio: a round arch deep enough for 1 : 4 leaves the second overtone at 9.35.
   The shape of the cut is a second handle. An arch with a flatter bottom (in the lab, the exponent 3 in place of
   2, 65% deep) gives 1 : 4.00 : 10.0. In general, wood removed where a mode bends most lowers that mode most. The
   lowest mode bends most at the centre; the second has no bending there and bends most about a quarter of the
   way from each end; the third bends at the centre and near a sixth of the way in. So a maker lowers the first
   and third together at the centre, the second alone at the quarter points, and corrects the third against the
   first near the sixths (Bork, 1995).

5. ★ **A harmonic plate.** Design a flat plate, by varying its thickness from place to place, whose five lowest modes
   are in the ratios 1 : 2 : 3 : 4 : 5. Is there more than one answer, and what does Kac's question say about that?

   *Where the frontier is.* This is the makers' problem stated for a computer, and it has been solved for bells:
   Schoofs and colleagues (1987) reshaped a bell's profile until its tierce became a major third, and McLachlan,
   Keramati Nigjeh and Hasell (2003) designed bells with up to seven partials in a harmonic series, which now
   hang in Melbourne. Bharaj and colleagues (2015) optimized the outlines of flat bars so that arbitrary shapes
   play in tune. There are many answers: the set of shapes with five prescribed frequencies is large, and the
   isospectral drums show that even all the frequencies need not fix a shape. What is not understood is the map
   from the remaining freedom to what a listener hears: the strengths and decays of the partials, and how the
   object radiates.

## Sources

Books: T. D. Rossing, *Science of Percussion Instruments* (2000); N. H. Fletcher and T. D. Rossing, *The Physics of
Musical Instruments* (2nd ed., 1998), chs. 3 and 18–21, for membranes, bars, plates, the kettledrum's modes, the
tabla, bells and gongs; Lord Rayleigh, *The Theory of Sound* (1877), chs. 8–10; E. F. F. Chladni, *Entdeckungen
über die Theorie des Klanges* (1787); A. Lehr, *The Art of the Carillon in the Low Countries* (1991); S. Stuempfle,
*The Steelband Movement* (1995).

Papers: C. V. Raman and S. Kumar, "Musical drums with harmonic overtones", *Nature* 104 (1920); B. S. Ramakrishna
and M. M. Sondhi, "Vibrations of Indian musical drums regarded as composite membranes", *JASA* 26 (1954); T. D.
Rossing, "The physics of kettledrums", *Scientific American* 247 (1982); R. S. Christian, R. E. Davis, A. Tubis,
C. A. Anderson, R. I. Mills and T. D. Rossing, "Effects of air loading on timpani membrane vibrations", *JASA* 76
(1984); I. Bork, "Practical tuning of xylophone bars and resonators", *Applied Acoustics* 46 (1995); W. Ritz,
"Theorie der Transversalschwingungen einer quadratischen Platte mit freien Rändern", *Annalen der Physik* 28
(1909); T. D. Rossing and N. H. Fletcher, "Nonlinear vibrations in plates and gongs", *JASA* 73 (1983); A. J. G.
Schoofs, F. van Asperen, P. Maas and A. Lehr, "A carillon of major-third bells. I. Computation of bell profiles
using structural optimization", *Music Perception* 4 (1987); N. McLachlan, B. Keramati Nigjeh and A. Hasell, "The
design of bells with harmonic overtones", *JASA* 114 (2003); H. Weyl, "Das asymptotische Verteilungsgesetz der
Eigenwerte linearer partieller Differentialgleichungen", *Mathematische Annalen* 71 (1912); M. Kac, "Can one hear
the shape of a drum?", *American Mathematical Monthly* 73 (1966); C. Gordon, D. Webb and S. Wolpert, "One cannot
hear the shape of a drum", *Bulletin of the AMS* 27 (1992); S. Sridhar and A. Kudrolli, "Experiments on not
'hearing the shape' of drums", *Physical Review Letters* 72 (1994); T. A. Driscoll, "Eigenmodes of isospectral
drums", *SIAM Review* 39 (1997); S. Zelditch, "Inverse spectral problem for analytic domains, II: Z₂-symmetric
domains", *Annals of Mathematics* 170 (2009); R. P. Wildes and W. A. Richards, "Recovering material properties
from sound", in *Natural Computation* (1988); C. Carello, K. L. Anderson and A. J. Kunkler-Peck, "Perception of
object length by sound", *Psychological Science* 9 (1998); A. J. Kunkler-Peck and M. T. Turvey, "Hearing shape",
*Journal of Experimental Psychology: Human Perception and Performance* 26 (2000); G. Bharaj, D. I. W. Levin,
J. Tompkin, Y. Fei, H. Pfister, W. Matusik and C. Zheng, "Computational design of metallophone contact sounds",
*ACM Transactions on Graphics* 34 (2015).
