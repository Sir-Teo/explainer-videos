# Psychology, Built: Part 13, The Eye and the Code

New York, 1942. In a laboratory at Columbia University an observer sits in total darkness for forty minutes, then
watches for a tiny, brief flash of blue-green light off to one side. Selig Hecht, Simon Shlaer and Maurice Pirenne
measured the flash in quanta, and found that it was seen when somewhere between fifty-four and a hundred and
forty-eight reached the front of the eye, of which only five to fourteen were absorbed, spread over about five hundred
rods. A rod must respond to a single quantum: the eye is about as sensitive as physics allows. Then the steepness of
the observers' frequency-of-seeing curves gave the same small number by a second route, with no need to know how much
light the eye wastes.

But the eye does not send the brain a picture of the light. It sends differences, across space, time and wavelength,
and every stage can be written down as a filter. This part follows them: the Poisson argument; the optics and the
cone mosaic, which stop detail near sixty cycles per degree; gain control, which spans ten log units of light and
gives Weber's law on the way; the retina's centre minus surround, a band-pass filter, Mach bands, and why differences
are worth sending; the cortex's edge detectors, Gabor fields, simple and complex cells; the viewer's own contrast
sensitivity function and a hybrid image that it splits; channels and divisive normalization. Then colour as linear
algebra: three cone types, matching as a 3-by-3 solve checked against Stiles and Burch's 1955 matches, metamers as the
null space, the 1931 diagram; Hering's opponent colours and colour blindness as a lost dimension; colour constancy and
the dress; and the two visual streams, with patient D.F. The practice chapter is the screens, cameras, codecs and
palettes built on all of it; the frontier is what the first stage of cortex does with real scenes, the retina's many
output types, and a tetrachromat. For Kant's first objection this is the strongest reply in the series so far: a
threshold counted in quanta, and colour matches predicted by a matrix.

## Where the numbers come from

| What | Source |
|---|---|
| 40 minutes in the dark; 510 nm flashes; 2.1 to 5.7 × 10⁻¹⁰ erg = 54 to 148 quanta at the cornea; 4% reflected, about 50% absorbed by the media, at most 20% of the rest caught; 5 to 14 absorbed over about 500 rods; 5 to 8 from the curves' shapes; observers mostly the authors | Hecht, Shlaer and Pirenne (1942), from the abstract and later accounts; registered in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md) |
| One absorbed quantum gives a toad rod a current of about 1 pA, 5% of its dark current; quantum efficiency about 0.5 | Baylor, Lamb and Yau (1979), from the abstract |
| Single photons in two-interval forced choice: 30,767 trials, 2,420 single-photon events, 51.6% ± 1.0% correct, P = 0.0545; about 60% on high-confidence trials | Tinsley et al. (2016), as quoted in summaries and in van der Reep et al. (2022) |
| The square-root law of photon noise | de Vries (1943), Rose (1948), as registered for Part 11 |
| A single stretch receptor: impulses of one size whose rate rises with load and falls while it stays on | Adrian and Zotterman (1926), from later accounts; Hartline and Graham (1932) for the eye of *Limulus* |
| On-centre and off-centre ganglion cells with an antagonistic surround | Kuffler (1953) |
| Cells driven by a line at one orientation; the story of the slide's edge | Hubel and Wiesel (1959), with the story from their later recollections; simple and complex cells (1962); monkeys (1968) |
| Thalamic cells connect to simple cells whose subregions they overlap | Reid and Alonso (1995), from the abstract |
| A band-pass CSF peaking near 3 to 5 cycles per degree | Campbell and Robson (1968), from secondary accounts |
| Adapting to a grating raises thresholds up to fivefold near its frequency and orientation | Blakemore and Campbell (1969), from the abstract |
| A four-parameter CSF estimated in about fifty trials | Lesmes et al. (2010), as registered for Part 11 |
| Cone fundamentals (peaks 570, 545, 445 nm); the CIE 1931 functions; Stiles and Burch's 1955 2° pilot matches (10 observers, primaries 645.2, 526.3, 444.4 nm); the scotopic curve (peak 505 nm) | the tables of the Colour & Vision Research Laboratory (cvrl.org), downloaded and transcribed into `archive/_colour_tables.py` |
| The 1931 standard observer rests on Wright's and Guild's matches, seventeen observers | the usual account, from memory |
| About 8% of men and 0.5% of women of northern European ancestry have red-green deficiency | the NIH's genetics reference and reviews |
| The dress: about 1,400 online, 57% blue-black, 30% white-gold, 11% blue-brown, 2% other; white-gold more common among older people and women | Lafer-Sousa, Hermann and Conway (2015), from the authors' university's release |
| Two surveys of 8,084 and 5,333; assuming shadow went with white and gold | Wallisch (2017), from the release and abstract |
| D.F.: carbon monoxide poisoning; matching a slot's angle near chance; posting a card accurately | Milner et al. (1991) and Goodale et al. (1991), from reviews |
| One of 24 obligate carriers of deuteranomaly behaved as a tetrachromat on every test | Jordan, Deeb, Bosten and Mollon (2010), from the abstract |
| About twenty types of retinal ganglion cell in primates, more than forty in mice | reviews and a 2023 release on cross-species work |
| Okabe and Ito's eight colours | Okabe and Ito (2008), hex values from memory |

Everything else is computed by `compute.py` with Psyche's `vision` module and is a model's behaviour, tagged as such
on screen. The radar of earlier parts is gone; the drawings here are the dark room, the cone mosaic, the brain's two
routes and the receptive-field diagrams, and they say so. D.F.'s polar plots are simulated trials with the published
pattern, not her data. The dress is a stand-in swatch with colours like the photograph's, which is not reproduced.

| Number on screen | Value | How |
|---|---|---|
| Steepness of P(seen) per tenfold step at its midpoint, k = 1, 6, 9 | 0.80, 2.20, 2.71 | Poisson tails |
| Psyche (k = 6, 9% absorbed), 7 intensities × 50 flashes: fitted k and absorption | 6 and 9.2% | maximum likelihood; the median of 101 experiments |
| Share of the 101 experiments whose fitted k is within one of 6 | 80% | the same |
| Diffraction cutoff for a 2, 3 and 6 mm pupil (555 nm) | 63, 94 and 189 cycles per degree | D/λ |
| The modelled eye's MTF at 60 c/deg; its line spread (full width at half height) | 0.002; 1.35 arcmin | diffraction × a Gaussian blur of 0.5 arcmin |
| Nyquist limit of cones 0.5 arcmin apart; an 80 c/deg grating sampled at 120 per degree appears at | 60; 40 c/deg | one cycle per two cones |
| Increment threshold over background with gain control | 4.1%, over ten log units | Naka-Rushton, σ following the background |
| Neighbouring correlation (two pixels apart) in a 1/f texture, before and after a DoG | 0.60; 0.11 | the retina's filter |
| A Gabor complex cell's half-width at half height | 22° | the energy model |
| The CSF: acuity it implies; fitted peak and width from 8 simulated thresholds | 56 c/deg; 3.7 c/deg, 3.1 octaves | a truncated log-parabola; the median fit of 101 |
| Threshold elevation after adapting to 8 c/deg | up to 5× | a bank of one-octave channels |
| Derived colour-matching functions against Stiles and Burch: correlation, each function | 0.9999, 0.9995, 0.9994 | P⁻¹ times the cone curves, one scale factor each |
| Matching 580 nm with their primaries; 500 nm | red 2.27, green 0.66, blue −0.01; red −0.27 | the same |
| A metamer pair under a 2856 K lamp: change in M and in S | 1% and 4% | a null-space metamer |
| Where the red-green channel (L − 1.5 M) crosses zero | 581 nm | weighted differences |
| Smallest colour difference (CIE ΔE) in a rainbow palette: normal, without L, without M; in Okabe and Ito's | 39, 7, 10; 26, 23, 17 | dichromacy as a projection |
| A stand-in swatch discounted under 3000 K and under 12000 K light | blue and near-black; white and gold | von Kries |
| Colour stored at a quarter of the resolution (4:2:0) | 76,800 samples become 38,400 | YCbCr |

## Built in this part

* `explainer/psychology/psyche/vision.py`: frequency of seeing as a Poisson tail, its slope, and a maximum-likelihood
  fit of k and the loss; the diffraction MTF, a blurred eye, the line spread, Nyquist and aliasing; the Naka-Rushton
  function and increment thresholds with and without gain control; the difference of Gaussians in space and
  frequency, Mach bands, a 2-D DoG; gratings, Gabor fields, simple and complex cells, orientation tuning; divisive
  normalization and a masked contrast response; a truncated log-parabola CSF, its fit, the acuity it implies, the
  Campbell-Robson chart and CSF filtering; the cone fundamentals, CIE 1931 and Stiles-Burch tables on a common grid;
  cone excitations, matching, colour-matching functions for any primaries, null-space metamers, chromaticity, sRGB;
  opponent channels, dichromacy, Planck spectra, von Kries. Tested in `tests/psychology/test_vision.py`.
* `explainer/psychology/archive/_colour_tables.py`: the four colour tables at 5 nm, transcribed by script.
* The Ledger gains five rows, including the rate code deferred from Part 5, and the Archive eleven datasets.
* The course's interactive measures the reader's contrast sensitivity at four spatial frequencies by staircase and
  draws the curve.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| A dark-adapted eye sees a flash when a handful of quanta, about five to fourteen, are absorbed; a rod responds to one | Hecht, Shlaer and Pirenne 1942 | replicated |
| A sensory fibre codes strength as a rate of impulses of fixed size, and adapts | Adrian and Zotterman 1926 | replicated |
| V1 neurons are tuned to orientation; simple cells are built from aligned centre-surround inputs | Hubel and Wiesel 1959 | replicated |
| Contrast sensitivity is band-pass, and adaptation lowers it only near the adapting frequency | Campbell and Robson 1968 | replicated |
| Seeing the dress as white and gold goes with assuming bluish light | Lafer-Sousa, Hermann and Conway 2015 | replicated |

The first row's note records that single-photon detection by people rests on one study at the edge of significance.
Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: D.F. (a single case; vision
without awareness is entered in Part 27), the tetrachromat (one person, at the frontier), the colour tables (standard
measurements, not a finding) and Okabe and Ito's palette (a design recommendation).

## Build it

```bash
python -m videos.psychology.psych13.compute            # every number (seconds), into .cache/psych13/
python tools/qa_scene.py psych13 Matching              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych13 -q l   # the whole part, silent preview
python tools/build.py psych13                          # 1080p30 with narration
python tools/qa_scene.py psych13 Matching --lang zh    # the Chinese edition of one chapter
python tools/make.py psych13                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 13                    # the lab: quanta, filters, colour matching
python tools/check_ledger.py psych13                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's vision module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A dark room, 1942 | The experiment; from the cornea to the rods; the eye sends differences; objectives |
| 1 | Counting quanta | Poisson arrivals; the curve's steepness gives k; Psyche in the dark room; one rod, one quantum, one photon; photon noise and the square-root law |
| 2 | Optics and the mosaic | The MTF and the diffraction limit; the cone mosaic, Nyquist and aliasing; 20/20 |
| 3 | Ten billion to one | The range of light; a response curve that slides; gain control gives Weber's law |
| 4 | The retina sends differences | Adrian's rate code; Kuffler's centre and surround; the difference of Gaussians; Mach bands; why send differences |
| 5 | Edges in the cortex | Hubel and Wiesel's bar; the Gabor field and its tuning; simple and complex cells; a first hierarchy |
| 6 | On you: your contrast sensitivity | The Campbell-Robson chart; the CSF and its four numbers; a hybrid image |
| 7 | Channels and normalization | A bank of channels; Blakemore and Campbell's adaptation; divisive normalization |
| 8 | Three numbers for a spectrum | Newton to Young; the cone fundamentals; univariance; a spectrum projected to three numbers |
| 9 | Colour matching as linear algebra | The matching experiment and negative weights; derived functions against Stiles and Burch; metamers; the 1931 diagram |
| 10 | Opponent colours and colour blindness | Hering's puzzle; opponent channels; dichromacy as a lost dimension |
| 11 | Constancy and the dress | Discounting the light; one swatch, two illuminants; who saw what |
| 12 | Two streams | What and where, or how; D.F. and the slot |
| 13 | The Ledger | Few quanta; the rate code; orientation cells; the CSF and channels; the dress |
| 14 | In practice: screens, codecs and palettes | Engineering on the standard observer; chroma subsampling; designing for colour-blind readers |
| 15 | Frontier: what V1 does with the world | What is solid and argued; how close we are to V1; twenty output types and a fourth cone; open questions |
| | Recap, problems, and the road ahead | Ten lines; the first objection; payoffs; problems; references; Part 14 |

## Sources

**Books.** B. A. Wandell, *Foundations of Vision* (1995). R. W. Rodieck, *The First Steps in Seeing* (1998).
D. H. Hubel, *Eye, Brain, and Vision* (1988).

**Papers.** S. Hecht, S. Shlaer and M. H. Pirenne, Energy, quanta, and vision, *J. Gen. Physiol.* 25 (1942) 819–840.
D. A. Baylor, T. D. Lamb and K.-W. Yau, Responses of retinal rods to single photons, *J. Physiol.* 288 (1979)
613–634. J. N. Tinsley et al., Direct detection of a single photon by humans, *Nat. Commun.* 7 (2016) 12172. E. D.
Adrian and Y. Zotterman, The impulses produced by sensory nerve-endings, Part II, *J. Physiol.* 61 (1926) 151–171.
H. K. Hartline and C. H. Graham, Nerve impulses from single receptors in the eye, *J. Cell. Comp. Physiol.* 1 (1932)
277–295. S. W. Kuffler, Discharge patterns and functional organization of mammalian retina, *J. Neurophysiol.* 16
(1953) 37–68. R. W. Rodieck, Quantitative analysis of cat retinal ganglion cell response to visual stimuli, *Vision
Res.* 5 (1965) 583–601. D. H. Hubel and T. N. Wiesel, Receptive fields of single neurones in the cat's striate
cortex, *J. Physiol.* 148 (1959) 574–591; Receptive fields, binocular interaction and functional architecture in the
cat's visual cortex, *J. Physiol.* 160 (1962) 106–154; Receptive fields and functional architecture of monkey striate
cortex, *J. Physiol.* 195 (1968) 215–243. R. C. Reid and J.-M. Alonso, Specificity of monosynaptic connections from
thalamus to visual cortex, *Nature* 378 (1995) 281–284. E. H. Adelson and J. R. Bergen, Spatiotemporal energy models
for the perception of motion, *J. Opt. Soc. Am. A* 2 (1985) 284–299. F. W. Campbell and J. G. Robson, Application of
Fourier analysis to the visibility of gratings, *J. Physiol.* 197 (1968) 551–566. C. Blakemore and F. W. Campbell,
On the existence of neurones in the human visual system selectively sensitive to the orientation and size of retinal
images, *J. Physiol.* 203 (1969) 237–260. D. J. Heeger, Normalization of cell responses in cat striate cortex, *Vis.
Neurosci.* 9 (1992) 181–197. M. Carandini and D. J. Heeger, Normalization as a canonical neural computation, *Nat.
Rev. Neurosci.* 13 (2012) 51–62. L. A. Lesmes et al., the quick CSF, *J. Vis.* 10(3) (2010) 17. W. S. Stiles and
J. M. Burch, Interim report to the CIE (1955). A. Stockman and L. T. Sharpe, *Vision Res.* 40 (2000) 1711–1737. L.
M. Hurvich and D. Jameson, An opponent-process theory of color vision, *Psychol. Rev.* 64 (1957) 384–404. G. Jordan,
S. S. Deeb, J. M. Bosten and J. D. Mollon, The dimensionality of color vision in carriers of anomalous trichromacy,
*J. Vis.* 10(8) (2010) 12. R. Lafer-Sousa, K. L. Hermann and B. R. Conway, *Curr. Biol.* 25 (2015) R545–R546. P.
Wallisch, *J. Vis.* 17(4) (2017) 5. C. Witzel, C. Racey and J. K. O'Regan, *J. Vis.* 17(2) (2017) 1. A. D. Milner et
al., Perception and action in 'visual form agnosia', *Brain* 114 (1991) 405–428. M. A. Goodale, A. D. Milner, L. S.
Jakobson and D. P. Carey, *Nature* 349 (1991) 154–156. L. G. Ungerleider and M. Mishkin, Two cortical visual systems
(1982). M. A. Goodale and A. D. Milner, Separate visual pathways for perception and action, *Trends Neurosci.* 15
(1992) 20–25. B. A. Olshausen and D. J. Field, How close are we to understanding V1?, *Neural Comput.* 17 (2005)
1665–1699.

## Problems and solutions

**1. The shape gives k.** With N ~ Poisson(λ), λ = aq, P(seen) = P(N ≥ k) = Q(k, λ), the regularized upper incomplete
gamma function of λ alone. On a log axis, log λ = log a + log q, so changing a shifts the curve by log a without
changing its shape. Its slope at the midpoint, dP/d log₁₀ q = ln 10 · λ · P(N = k − 1), depends only on k: 0.80 for
k = 1, 2.20 for k = 6, 2.71 for k = 9.

**2. Hecht's arithmetic.** 54 × 0.96 × 0.5 × 0.2 = 5.2 and 148 × 0.096 = 14.2: five to fourteen. With n quanta in 500
rods, P(no rod has two) = ∏ᵢ (500 − i)/500 for i < n: 98% for n = 5, 83% for n = 14. So a rod catching two happens on
2% to 17% of flashes; the argument needs only that most seen flashes involve no rod with two, which holds.

**3. The mosaic.** Spacing 0.5 arcmin = 1/120 degree; one cycle needs two samples, so the Nyquist frequency is 60
c/deg. A 90 c/deg grating sampled at 120 per degree appears at |90 − 120| = 30 c/deg.

**4. The DoG's peak.** With unit-area Gaussians, H(f) = exp(−2π²σc²f²) − exp(−2π²σs²f²). Setting dH/df = 0 gives
σc² e^{−2π²σc²f²} = σs² e^{−2π²σs²f²}, so f* = √(ln(σs²/σc²) / (2π²(σs² − σc²))). With σs = 3σc, f* =
√(ln 9 / (16π²σc²)) = √(2.197/157.9)/σc ≈ 0.118/σc cycles per unit of distance.

**5. Metamers by projection.** P = I − Aᵀ(AAᵀ)⁻¹A is symmetric and P² = P; AP = A − A = 0, so for any v, A(s + Pv) =
As: the same three cone excitations. Its rank is N − 3, the dimension of the null space (76 on a 79-point grid). A
physical metamer also needs s + Pv ≥ 0, which bounds how large Pv can be.

**6. A modern display's primaries.** `vision.matching_functions((630, 532, 467))` gives one row per wavelength. The red
function is negative from about 470 to 530 nm, the blue from about 535 to 625 nm, and the green below about 465 nm
and above about 635 nm; every set of three real primaries has negative lobes, which is why no display covers the
spectral locus.

**7. ★ A fourth dimension.** A trichromat's matches are fixed by three numbers, so a fourth cone shows up only as
matches that trichromats accept and the observer rejects: give the observer a Rayleigh-type match (a mixture of two
long-wave lights against a single one) and show that no setting satisfies them, or that the accepted settings form a
point where a trichromat's form a line. Jordan et al. used such matches and discrimination thresholds along
directions a trichromat cannot see. Ordinary three-primary matching misses it because with only three knobs, an
observer with four cones can never be satisfied, and a careless experimenter records the closest setting as a match.

## Where it comes back

Seeing as inference, of which the dress was a preview: Part 14. The other senses, each with its own code: Part 15.
Attention as gain and normalization: Part 18. Seeing without knowing, D.F. and blindsight: Part 27. Displays,
warnings and colour in design: Parts 51 and 52. Efficient coding: Part 58. Psyche's `vision` module supplies the
filters, the CSF and the colour machinery those parts use.

## Open checks

Before the narrated master:

* Hecht et al.: "a faint point" for fixation, "tiny, brief" for the flash, and "off to one side" are the usual
  account; the field size, duration and eccentricity are not stated on screen. That most observers were the authors
  is from a summary.
* Tinsley et al. (2016): the numbers are quoted from summaries and a reanalysis; the 60% on high-confidence trials is
  as the reanalysis gives it. The number of observers is not given on screen.
* Adrian and Zotterman: the frog muscle, the weights and the adaptation are from later accounts; no rates are
  quoted, and the trains are schematic.
* Hubel and Wiesel: the slide's edge is their later recollection; 1958 and Johns Hopkins are from those accounts.
* The tuning half-width of about 20° "in the range recorded" is a general statement, from memory.
* Campbell and Robson (1968): the peak near 3 to 5 c/deg is from secondary accounts; the peak sensitivity of the
  model (200) and the acuity it implies (56 c/deg) are the model's.
* Blakemore and Campbell (1969): "up to fivefold" is from the abstract; the channel model's width (one octave) is a
  common assumption, not their measurement.
* The 1931 standard observer from Wright's and Guild's seventeen observers is from memory, as are the 1983
  microspectrophotometry and the 1960s pigment measurements.
* Hurvich and Jameson (1957): hue cancellation is described from memory; the channel weights on screen (L − 1.5 M)
  are chosen, not fitted to their data. Unique yellow "about 575 to 580 nm" is the usual range.
* Dalton's 1794 account and the X-linked genes are from general knowledge.
* The dress: the swatch's colours are like the photograph's, chosen by eye; the 3000 K and 12000 K lights are
  illustrations. The survey shares are from the authors' university's release.
* D.F.: 1988 and "could still see colours and textures" are from accounts of the case; the polar plots are simulated.
* The number of retinal ganglion cell types (about twenty in primates, more than forty in mice) is from a release and
  a review; estimates differ.
* Okabe and Ito's hex values are from memory.
