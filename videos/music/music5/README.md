# Music, Built: Part 5, Consonance

Part 5 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). With a string (Part 1), a spectrum (Part 3) and an ear (Part 4), the oldest question
in the science of music can be computed: why do some notes belong together? Six answers have been given in 2,500
years. This part runs each of them as a calculation (`explainer/music/monochord/consonance.py`), plays the sound on
which each one fails, and ends with three layers: the membrane, the nerve, and the listener. Every sound is computed
in `compute.py`. Dates and attributions are the published ones, listed under Sources.

* **An octave that sounds wrong.** Two notes exactly an octave apart that grind, and two 84 cents too far apart
  that are smooth; six answers in 2,500 years (Pythagoras, Galileo, Rameau, Euler, Helmholtz, Stumpf); the plan.
* **1. Number.** The monochord's ratios and the tetractys; Zarlino's six; Euler's *gradus suavitatis* (1739), a
  worked example (3:2 scores 4; 5:4 scores 7); his number for thirteen intervals against what musicians call them;
  an ear question: a fifth of 3:2 and one five cents wide, whose nearest simple ratio is 173:115 and whose Euler
  number is 199. A small change in a sound cannot be a huge change in its sweetness.
* **2. Pulses that coincide.** Galileo (1638); two trains of clicks, three against two, a hundred times faster by
  the end: a rhythm becomes a fifth; the length of the repeating pattern as a measure; the same flaw; and why to
  keep the idea (Part 4: the nerve fires in time with the wave).
* **3. Beats.** Two close tones add up to one tone that swells and fades at the difference of their frequencies
  (the sum-to-product identity); 1, 4 and 12 beats a second; a worked example (220 and 222 Hz: two beats a
  second), and one tone lowered onto another until the beats stop; from flutter to roughness; Helmholtz's theory.
* **4. Roughness, measured.** Plomp and Levelt (1965): roughest a quarter of a critical band apart, smooth beyond
  one band; an ear question: two pure tones, one climbing an octave (roughest in the first second, and nothing at
  all at the tritone, the fifth or the octave); a pure fifth and a pure tritone, both smooth.
* **5. A curve with no ratios in it.** Seven partials each, ninety-one pairs; a worked example (in a fifth,
  partials 3 and 2, and 6 and 4, coincide; in a tritone they miss by 49 and 57 Hz); the dissonance curve, whose
  valleys are 6:5, 5:4, 4:3, 3:2, 5:3 and 2:1 (and 7:6, 7:5, 7:4) to within a cent; the curve heard as one
  note climbs through an octave.
* **6. Bend the timbre.** Sethares (1993): partials stretched so that each doubling is 2.1; every valley moves to
  its old ratio raised to log₂2.1 (to four decimal places); an ear question: an octave and a wide octave in the
  ordinary tone and in the bent one; pianos, bells, the gamelan, synthesizers.
* **7. One note or two?** Stumpf's fusion (1890); an ear question: three high pure tones at 4:5:6 and the low note
  they imply (Part 4's pitch model: 261.6 Hz, middle C); Rameau's fundamental bass (1722); the model's single
  pitch for an octave, fifth, fourth and third, weaker as the common period grows: Galileo's pulses, counted by the
  nerve; for headphones, a minor second in both ears and then one tone to each; McDermott, Lehr and Oxenham (2010).
* **8. Major and minor.** An ear question: two chords of the same three intervals; roughness 0.97 and 0.99; as
  whole numbers 4:5:6 and 10:12:15, with fundamental basses two and 3.3 octaves down; the diminished and augmented
  triads, and the warning that listeners rank those two the other way round; a map of every chord of three notes,
  whose valleys are the major and minor triads, their inversions, and two stacked fourths.
* **9. What is learned.** A history of what counted as consonant; the major third of the early theorists (81:64)
  beside the pure one (5:4); the Tsimane' (McDermott et al., 2016); three layers.
* **10. Frontier: one model for all of it.** Harrison and Pearce (2020): roughness, harmonicity and familiarity
  together; Marjieh et al. (2024): 235,440 judgments online, preferences that move with the partials; what is not
  known (major and minor as bright and dark, the augmented chord, infants, chords in motion). ★ research problem.
* **Variation 5, recap and problems.** The Tune in a bent tone on a stretched scale, alone, then in parallel
  "fifths" of 751 cents, then the same notes with ordinary partials (3.7 times as rough), then bent again; the
  ledger; what we found; five problems; where it comes back; in practice; references; twelve pure fifths against
  seven octaves, and Part 6.

## What is computed, and what is heard

`python -m videos.music.music5.compute` (a few seconds) fills `.cache/music5/`.

| Item | What it computes | Checked against |
|---|---|---|
| `bent` | an exact octave and one of 2.1:1 in a tone with stretched partials | roughness 0.40 against 0.02 |
| `number` | Euler's gradus, Galileo's coincidences and Tenney's height for thirteen just intervals; a fifth 5 cents wide | Euler's own table (2, 4, 5, 7, 8 … 14) |
| `pulses` | two click trains, 3 and 2 a second, accelerated a hundredfold | they end at 300 and 200 Hz |
| `beats` | pairs of pure tones 1, 4 and 12 Hz apart; a tone lowered onto another | the envelope 2\|cos π(f₁−f₂)t\| bounds the sum |
| `plomp` | Plomp and Levelt's curve; two pure tones gliding apart; a pure fifth and tritone | the peak at a quarter of a band; under 2% of it at both |
| `curve` | the dissonance curve of a tone of seven partials; its minima; one note climbing an octave | Sethares's minima: 7:6, 6:5, 5:4, 4:3, 7:5, 3:2, 5:3, 7:4, 2:1 |
| `worked` | every pair of partials of a fifth and of a tritone that share a band | 3 = 2 × 1.5 and 6 = 4 × 1.5 coincide |
| `stretched` | the same curve with partials at k^(log₂2.1) | each minimum at its old ratio ^ log₂2.1 (0.0003) |
| `fusion` | Part 4's pitch model on dyads and on 4:5:6 in pure tones; a minor second, diotic and dichotic | the fundamental bass, within 5 cents |
| `triads` | roughness and fundamental bass of four triads; roughness of every three-note chord on a grid | major and minor within 1.5% of each other |
| `culture` | a major third of 81:64 against 5:4 | 21.5 cents; 16 beats a second on middle C |
| `tune` | Variation 5 and the roughness of its dyads in both timbres | 3.7 times |
| `nextpart` | middle C and the C twelve pure fifths on | the Pythagorean comma, 23.46 cents |

Monochord's consonance layer is held against Euler's table, Sethares's minima and the fundamental bass in
`tests/music/test_consonance.py`; this part's claims and clips in `tests/music/test_music5.py`.

**Sounds.** Fifteen clips, all `synthesized` and labelled on screen: sums of sines with seven partials in the
proportions 1, 0.88, 0.88² …, either at whole multiples of the fundamental or stretched; pairs of pure tones; two
trains of clicks. One clip (the minor second, one tone to each ear) needs headphones and says so. There are no
recordings.

**What the models are, and are not.** Roughness is Plomp and Levelt's curve in Sethares's parameterisation, summed
over pairs of partials with the weaker amplitude of each pair; it ignores masking and level. With it, the
diminished triad is rougher than the augmented, which is not how listeners rank them, and the film says so. Harmonicity is measured by Part 4's summary autocorrelation with a taper towards the
longest period that is still heard as a pitch (30 Hz); it is a fair account of dyads wider than a critical band
and says nothing sensible about seconds, where the two notes share a band. Stumpf's bar chart shows the order he
reported, with schematic heights. The Tsimane' results are described in words, from the paper's abstract and
figures; no data from it are plotted.

## Build

```bash
python -m videos.music.music5.compute                          # numbers and sounds (a few seconds)
EXPLAINER_TTS=silent python tools/build.py music5 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music5 --sync                         # the sound gates
python tools/dead_air.py renders/music5_480p.mp4 --sound music5   # no empty screen; no sound over a still one
python tools/lecture_length.py music5                          # 30 to 60 minutes, listening included
python tools/build.py music5                                   # 1080p30, narrated
python -m pytest -q tests/music                                # Monochord against its references; this part's claims and clips
python -m videos.music.labs 5                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Two sevenths.** Compute Euler's number for the minor seventh 16:9 and for the "harmonic seventh" 7:4. Which
   does his formula prefer? Which sits in a valley of this part's roughness curve?

   *Solution.* lcm(16, 9) = 144 = 2⁴·3², so Γ = 1 + 4·1 + 2·2 = 9. lcm(7, 4) = 28 = 2²·7, so Γ = 1 + 2·1 + 6 = 9.
   Euler's formula cannot choose between them. The roughness curve can: 7:4 (969 cents) is one of its valleys,
   because the seventh partial of the lower note meets the fourth of the upper, while 16:9 (996 cents) lies on the
   slope beside it. The formula charges a prime its full size however it is used; the ear only asks whether partials
   meet. (The lab prints both numbers.)

2. **Which partials meet.** Two notes have harmonic partials and stand in the ratio p:q in lowest terms. Show that
   partial m of the upper coincides with partial n of the lower exactly when m is a multiple of q and n the same
   multiple of p. What fraction of the upper note's partials coincide?

   *Solution.* The upper note's partials are at m·(p/q)·f and the lower's at n·f, so they coincide when mp = nq.
   Since p and q share no factor, q must divide m: m = kq, and then n = kp. So the coinciding partials of the upper
   note are numbers q, 2q, 3q …: one in every q. For a fifth (3:2) every second partial of the upper note meets a
   partial of the lower; for a major third (5:4) every fourth; for 45:32, every thirty-second, which with seven
   partials means none. Galileo's "repeats every q cycles" and the count of coinciding partials are the same number.

3. **Ear.** The lab (`python -m videos.music.labs 5`) plays one interval twice: once in an ordinary tone, once in a
   tone whose partials were stretched. Say which version is smoother, and so whether the interval is an octave or a
   stretched octave.

   *Solution.* If the ordinary tone is the smooth one, the interval is 2:1; if the stretched tone is, it is 2.1:1.
   The lab prints the interval and Monochord's roughness for both versions (0.04 against 0.40, or 0.41 against
   0.02) after you have listened.

4. **Build.** Compute the dissonance curve of a tone with partials at 1, 2.76, 5.40 and 8.93 (a bar struck at its
   middle), and list its valleys. Build a five-note scale from them and play the Tune on it.

   *Solution sketch.* The lab does the first half with `PARTIALS = [1, 2.76, 5.40, 8.93]`. Sharp valleys lie
   wherever a partial of one tone meets a partial of the other, at the ratios between the partials: 1.654
   (8.93/5.40), 1.957 (5.40/2.76) and 2.76; broad ones lie where no two partials are close (near 1.44, 1.79 and
   2.26). A five-note scale could take 1, 1.44, 1.654, 1.957 and 2.26 within a "pseudo-octave" of 2.76, with the
   Tune's degrees 1, 2, 3, 4, 5, 6 mapped to scale steps in order and its "octave" to 2.76. This is how Sethares
   derives scales for bars and bells; a marimba maker does the opposite, carving an arch under each bar to pull
   2.76 up to 4.

5. **★ Research.** Fit weights for roughness, harmonicity and familiarity to published ratings of the twelve
   intervals, and predict the rating of every triad. Where is the fit worst, and what would a fourth term have to
   measure?

   *Pointers.* Ratings for dyads and triads are tabulated in Bowling et al. (2018) and reanalysed by Harrison and
   Pearce (2020), whose R package `incon` implements sixteen models. Monochord supplies the first two terms;
   for familiarity, count chord types in a corpus of chorales (Part 18 builds one). The augmented triad is the
   known failure of roughness and harmonicity together (Johnson-Laird et al., 2012, propose tonal context; Cook and
   Fujisawa, 2006, propose a "tension" term for equal stacked intervals). An open question is whether such a term
   is acoustic or learned: the experiments of Marjieh et al. (2024) with altered timbres are one way to test it.

## Sources

Books: H. von Helmholtz, *On the Sensations of Tone* (1863; tr. Ellis), part II; W. A. Sethares, *Tuning, Timbre,
Spectrum, Scale* (2nd ed., 2005); J. Tenney, *A History of 'Consonance' and 'Dissonance'* (1988); D. Deutsch (ed.),
*The Psychology of Music* (3rd ed., 2013), ch. 4 (W. F. Thompson, "Intervals and scales"); C. Stumpf,
*Tonpsychologie*, vol. 2 (1890); J.-P. Rameau, *Traité de l'harmonie* (1722); G. Zarlino, *Le istitutioni
harmoniche* (1558); Galileo Galilei, *Discorsi e dimostrazioni matematiche intorno a due nuove scienze* (1638; tr.
Crew and de Salvio), First Day, for the pulses and the "perpetual torment" of the eardrum.

Papers: L. Euler, *Tentamen novae theoriae musicae* (1739); J. Sauveur, *Mémoires de l'Académie royale des
sciences* (1701), for beats as a measure of frequency; R. Plomp and W. J. M. Levelt, "Tonal consonance and critical
bandwidth", *JASA* 38 (1965); W. A. Sethares, "Local consonance and the relationship between timbre and scale",
*JASA* 94 (1993); J. H. McDermott, A. J. Lehr and A. J. Oxenham, "Individual differences reveal the basis of
consonance", *Current Biology* 20 (2010); P. N. Johnson-Laird, O. E. Kang and Y. C. Leong, "On musical dissonance",
*Music Perception* 30 (2012); N. D. Cook and T. X. Fujisawa, "The psychophysics of harmony perception", *Empirical
Musicology Review* 1 (2006); J. H. McDermott, A. F. Schultz, E. A. Undurraga and R. A. Godoy, "Indifference to
dissonance in native Amazonians reveals cultural variation in music perception", *Nature* 535 (2016); D. L. Bowling,
D. Purves and K. Z. Gill, "Vocal similarity predicts the relative attraction of musical chords", *PNAS* 115 (2018);
P. M. C. Harrison and M. T. Pearce, "Simultaneous consonance in music perception and composition", *Psychological
Review* 127 (2020); R. Marjieh, P. M. C. Harrison, H. Lee, F. Deligiannaki and N. Jacoby, "Timbral effects on
consonance disentangle psychoacoustic mechanisms and suggest perceptual origins for musical scales", *Nature
Communications* 15 (2024); L. J. Trainor and B. M. Heinmiller, "The development of evaluative responses to music:
infants prefer to listen to consonance over dissonance", *Infant Behavior and Development* 21 (1998); J. Plantinga
and S. E. Trehub, "Revisiting the innate preference for consonance", *Journal of Experimental Psychology: Human
Perception and Performance* 40 (2014).
