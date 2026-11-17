# Psychology, Built: Part 14, Seeing as Inference

Two squares on a checkerboard, one out in the light and one in a soft shadow. Square A looks dark grey, square B
light grey, and nobody hesitates. Measure them and they send the eye exactly the same light. Edward Adelson made the
classic version in 1995; this part draws its own, and at the end explains it with a model that does what the viewer
did: it sees the surfaces, with the shadow taken out.

That is the theme. The image on the retina does not fix the world that made it: a small thing near and a large thing
far cast the same image, and a light square in shadow sends the same light as a dark square in the sun. So seeing
must add assumptions, and Helmholtz's phrase for it, unconscious inference, can now be written down as Bayes's rule.
The part follows the assumptions in turn: grouping and the Gestalt laws, read as priors, with Kanizsa's triangle and
Rubin's vase; depth from two eyes, with the disparity derived and Julesz's random-dot stereogram to free-fuse; size
constancy, and the Ponzo and Müller-Lyer illusions it produces when it is applied to a page, with the carpentered-world
hypothesis and its 2025 reopening. Then the mathematics: a normal prior times a normal likelihood, completing the
square, precisions that add, shrinkage, and why a biased percept can be the more accurate one. Then cue combination,
predicted in advance from each sense alone and tested on Psyche and by Ernst and Banks; the ventriloquist explained
by Alais and Burr; and two priors the viewer can see: light from above (and Adams, Graf and Ernst retraining it) and
slow motion (Thompson's faint gratings, fog on the road, and the aperture problem solved by Weiss, Simoncelli and
Adelson's MAP velocity). Then objects and faces: why pixel templates fail, Marr's stages, geons and views, Thorpe's
150 ms; Yin's inverted faces, a schematic Thatcher illusion, the fusiform face area and the expertise dispute. Then
deep networks: Yamins and DiCarlo's IT predictions, and a small network trained here that learns texture rather than
shape, and learns shape when its diet changes. The practice chapter is headsets, camouflage and
machines that see for us; the frontier is where priors come from, from Molyneux's question to a child's head camera,
what "Bayesian" commits you to, and Gibson's challenge. For Kant's third objection, that watching a mental state
changes it, the part offers cue weights read from choices rather than reports, and an illusion that knowing does not
undo.

## Where the numbers come from

| What | Source |
|---|---|
| A checkerboard (reflectances 0.4 and 0.8) under a soft shadow that halves the light: squares A and B both send 0.40; retinex's surfaces 0.50 and 0.96 | Psyche (`infer.checker_shadow`, `infer.retinex`), after Adelson (1995); the image is drawn, not reproduced |
| Size = 2 × distance × tan(angle / 2), for a 2° image | geometry |
| The Ames room, built in the 1940s | the usual account; the decade only |
| Gestalt laws, 1923; Kanizsa's triangle, 1955; Rubin's vase, 1915; V2 cells for illusory contours (1984) and border ownership (2000) | Wertheimer; Kanizsa; Rubin; von der Heydt, Peterhans and Baumgartner; Zhou, Friedman and von der Heydt, from the abstracts and later accounts |
| Disparity δ = IΔd / d(d + Δd), I = 6.3 cm: 1 cm of depth gives 8.49′ at 0.5 m, 0.54′ at 2 m, 0.022′ at 10 m; good observers' thresholds of a few to about ten seconds of arc | Psyche (`infer.disparity_arcmin`); stereoacuity from the usual accounts |
| The stereoscope, read to the Royal Society in June 1838 | Wheatstone (1838) |
| Random-dot stereograms, Bell Labs, 1960 | Julesz (1960) |
| Ponzo (1911); Müller-Lyer (1889); Gregory's inappropriate constancy scaling (1963) | the usual accounts |
| More than a dozen societies; San foragers least susceptible | Segall, Campbell and Herskovits (1966), from later accounts |
| Newly sighted children aged 8 to 16 see the Ponzo and Müller-Lyer illusions within 48 hours of surgery | Gandhi, Kalia, Ganesh and Sinha (2015) |
| The cross-cultural evidence reopened; the illusion in many animals | Amir and Firestone (2025) |
| Prior N(0, 1.5²), measurement 4 with σ = 1: posterior 2.77, σ 0.83; weight 0.692; mean squared error 0.69 against 1 | Psyche (`infer.posterior`) |
| A ridge seen in a random-dot stereogram and felt with two force-feedback arms; four levels of visual noise; four observers | Ernst and Banks (2002), from the abstract and later accounts |
| Psyche at σ_V = 1.5, 3, 4.5, 6 mm and σ_H = 4 mm: weights predicted 0.88, 0.64, 0.44, 0.31 and measured 0.88, 0.65, 0.44, 0.31; combined σ predicted 1.40, 2.41, 3.01, 3.34 and measured 1.42, 2.42, 2.99, 3.37 (2,000 trials a point) | Psyche (`infer.two_interval`, `infer.fit_cumulative`, `infer.combine`) |
| Blurred flashes and clicks: the ventriloquist effect reverses | Alais and Burr (2004) |
| Children below about eight to ten years do not combine vision and touch optimally | Gori et al. (2008), from the abstract |
| Many departures from optimality | Rahnev and Denison (2018) |
| Shape from shading assumes light from above; above and a little to the left | Ramachandran (1988); Sun and Perona (1998), from later accounts |
| Haptic training shifts the light-from-above prior, and the shift transfers to a lightness task | Adams, Graf and Ernst (2004), from the abstract |
| Low contrast looks slower | Thompson (1982) |
| Psyche's slow-prior model: 0.92, 0.50, 0.10 of the true speed at contrasts 1, 0.3 and 0.1 (the model's numbers, not people's) | Psyche (`infer.speed_estimate`), after Weiss, Simoncelli and Adelson (2002) |
| Uniform fog in a simulator: speeds look slower and people drive faster; fog that thickens with distance: speeds look faster | Snowden, Stimpson and Ruddle (1998); Pretto, Bresciani, Rainer and Bülthoff (2012), from the abstracts |
| Edges at 20° and 60°, true velocity (1, 0): MAP direction −0.0°, −7.9°, −30.5° and speed 1.00, 0.82, 0.44 at likelihood widths 0.02, 0.3, 1.0; the vector average at −41° | Psyche (`infer.edge_constraints`, `infer.map_velocity`, `infer.vector_average`) |
| Retinex | Land and McCann (1971) |
| Perceived depth changes lightness; perceived curvature changes lightness | Gilchrist (1977); Knill and Kersten (1991) |
| Pixel distances from a 40 × 40 square: moved 18.5, turned 9.4, a disc 6.9 | Psyche (`compute.py`, item `templates`) |
| Marr's *Vision*, 1982, after his death at 35 | the usual account |
| Recognition by components; deleting joints versus midsegments | Biederman (1987) |
| Bent-wire objects recognized near learned views | Bülthoff and Edelman (1992) |
| Photographs flashed for 20 ms; brain responses differ at about 150 ms; latencies of about 50 ms in V1 and 100 ms in IT | Thorpe, Fize and Marlot (1996); the latencies are approximate, from the usual accounts |
| Inversion hurts faces most | Yin (1969) |
| The composite face | Young, Hellawell and Hay (1987) |
| The Thatcher illusion | Thompson (1980); drawn with a schematic face |
| A face-selective region in 12 of 15 people | Kanwisher, McDermott and Chun (1997) |
| 97% of visually responsive cells in a monkey face patch prefer faces | Tsao, Freiwald, Tootell and Livingstone (2006), from the abstract |
| Developmental prosopagnosia in about 2 in 100, by one estimate | Kennerknecht et al. (2006), from later accounts |
| Super-recognizers | Russell, Duchaine and Nakayama (2009) |
| Greebles and the face area | Gauthier et al. (1999) |
| A performance-optimized network predicts 168 IT sites, about half of the predictable variance; middle layers predict V4 | Yamins et al. (2014), from the abstract |
| Networks trained on ImageNet follow texture on cue-conflict images; people follow shape; Stylized-ImageNet raises the shape bias | Geirhos et al. (2019) |
| A one-layer network (8 filters of 5 × 5, global average pooling, softmax readout) on 600 images of three shapes: with each shape's own texture, 100% correct on 300 new images and 283 of 299 conflict answers by texture; with textures shuffled, 50% correct (chance 33%) and 147 by shape to 66 by texture | Psyche (`infer.TinyConvNet`, `infer.texture_bias`) |
| The vergence-accommodation conflict slows fusion and causes fatigue | Hoffman, Girshick, Akeley and Banks (2008) |
| Paper moths with edge patches survive birds better | Cuthill et al. (2005) |
| Stickers make a network read a stop sign as a speed limit | Eykholt et al. (2018) |
| Edge statistics in natural images predict contour grouping | Geisler et al. (2001) |
| Observers' speed priors fitted from their judgments: peaked at zero, heavy-tailed | Stocker and Simoncelli (2006) |
| Molyneux's letter to Locke, 1688; newly sighted children fail to match felt to seen shapes at first, and improve within days | Held et al. (2011), from the abstract |
| 61 hours of head-camera video from one child aged 6 to 25 months, about 1% of waking hours | Vong et al. (2024) |
| Bayesian just-so stories | Bowers and Davis (2012) |
| Affordances and the optic array | Gibson (1979) |

Psyche's numbers are computed by `compute.py`; the simulated observers run 2,000 trials a point, so the numbers shown
are close to the model's own and no single run is chosen.

## Built in this part

* `explainer/psychology/psyche/infer.py`: the normal posterior and reliability-weighted combination; a two-interval
  observer with one cue or two, a conflict, and a cumulative-normal fit; speed under a slow prior; edge constraints, the
  MAP velocity and the vector average; the checkerboard under a shadow and retinex; disparity, random-dot stereograms,
  size-distance invariance; textured-shape images and a one-layer convolutional network in numpy, with its texture
  bias on cue-conflict images. Tested in `tests/psychology/test_infer.py`.
* The Ledger gains four rows and the Archive fifteen datasets.
* The course's interactive measures the reader's own Müller-Lyer illusion by two interleaved staircases and reports
  the point of subjective equality.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Two senses reporting one property are combined roughly as an optimal observer would | Ernst and Banks 2002 | replicated |
| Low-contrast motion looks slower | Thompson 1982 | replicated |
| The Müller-Lyer illusion is much weaker without rectangular buildings | Segall, Campbell and Herskovits 1966 | contested |
| A fusiform region responds much more to faces than to other objects | Kanwisher, McDermott and Chun 1997 | replicated |

The second row's note records that above about 8 Hz the results are mixed; the fourth keeps the expertise dispute.
Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Adelson's checkerboard (a
demonstration), Adams, Graf and Ernst (a single experiment told as an example), Yin's inversion (history; faces are
entered with the face area), Yamins et al. (a modelling result; deep networks as models are entered in Part 60),
Geirhos et al. (a property of networks, not of minds), Vong et al. (learning from an infant's experience is entered in
Part 30) and Wheatstone's stereoscope (the history of an instrument).

## Build it

```bash
python -m videos.psychology.psych14.compute            # every number (about three minutes), into .cache/psych14/
python tools/qa_scene.py psych14 Cues                  # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych14 -q l   # the whole part, silent preview
python tools/build.py psych14                          # 1080p30 with narration
python tools/qa_scene.py psych14 Cues --lang zh        # the Chinese edition of one chapter
python tools/make.py psych14                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 14                    # the lab: posteriors, cue combination, the aperture problem
python tools/check_ledger.py psych14                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's inference module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Two squares | The checkerboard; equal light; seeing is a bet; objectives |
| 1 | The inverse problem | One image, many worlds; the Ames room from above |
| 2 | Grouping and the Gestalt laws | Proximity, similarity, continuation, closure as priors; Kanizsa's triangle; figure and ground |
| 3 | Depth from two eyes | Disparity derived; its square law; Wheatstone's stereoscope; a random-dot stereogram to fuse; cues for one eye |
| 4 | Constancy, and illusions | Size constancy; Ponzo; Müller-Lyer and Gregory; the carpentered world reopened |
| 5 | Bayes for perception | The rule; a normal prior, likelihood and posterior; completing the square; shrinkage; why bias can pay |
| 6 | Combining cues | The rule and its two predictions; Ernst and Banks; Psyche at the bench; the ventriloquist; how optimal |
| 7 | Priors made visible | Bumps and dents; retraining the prior; low contrast looks slower; fog; the aperture problem and the MAP velocity |
| 8 | The two squares, explained | Light as surface times illumination; retinex; what it sees; where edges are not enough |
| 9 | Recognizing objects | Templates fail; Marr's stages; geons, and the rival of remembered views; 150 milliseconds |
| 10 | Faces | Inversion and wholes; the Thatcher illusion; face-selective cortex; faces or expertise |
| 11 | Deep networks as models | IT predicted; a small network that learns texture, and then shape |
| 12 | The Ledger | Cue combination; contrast and speed; the carpentered world; the face area |
| 13 | In practice: headsets, camouflage and machine vision | The vergence-accommodation conflict; camouflage against the priors; machines in the loop |
| 14 | Frontier: where priors come from | What is solid and argued; priors as statistics; Molyneux answered; a child's head camera; what "Bayesian" commits to; Gibson |
| | Recap, problems, and the road ahead | Ten lines; the third objection; payoffs; problems; references; Part 15 |

## Sources

**Books.** S. E. Palmer, *Vision Science: Photons to Phenomenology* (MIT Press, 1999). J. P. Frisby and J. V. Stone,
*Seeing: The Computational Approach to Biological Vision*, 2nd ed. (MIT Press, 2010). D. Marr, *Vision* (Freeman,
1982). D. C. Knill and W. Richards (eds.), *Perception as Bayesian Inference* (Cambridge University Press, 1996). J. J.
Gibson, *The Ecological Approach to Visual Perception* (Houghton Mifflin, 1979). H. von Helmholtz, *Handbuch der
physiologischen Optik* (Voss, 1856–1867). M. H. Segall, D. T. Campbell and M. J. Herskovits, *The Influence of Culture
on Visual Perception* (Bobbs-Merrill, 1966).

**Papers.** E. H. Adelson, Lightness perception and lightness illusions, in M. Gazzaniga (ed.), *The New Cognitive
Neurosciences*, 2nd ed. (MIT Press, 2000) 339–351. M. Wertheimer, Untersuchungen zur Lehre von der Gestalt II,
*Psychol. Forsch.* 4 (1923) 301–350. G. Kanizsa, Margini quasi-percettivi in campi con stimolazione omogenea, *Riv.
Psicol.* 49 (1955) 7–30. R. von der Heydt, E. Peterhans and G. Baumgartner, Illusory contours and cortical neuron
responses, *Science* 224 (1984) 1260–1262. H. Zhou, H. S. Friedman and R. von der Heydt, Coding of border ownership
in monkey visual cortex, *J. Neurosci.* 20 (2000) 6594–6611. C. Wheatstone, Contributions to the physiology of
vision, Part the first, *Phil. Trans. R. Soc.* 128 (1838) 371–394. B. Julesz, Binocular depth perception of
computer-generated patterns, *Bell Syst. Tech. J.* 39 (1960) 1125–1162. R. L. Gregory, Distortion of visual space as
inappropriate constancy scaling, *Nature* 199 (1963) 678–680. T. Gandhi, A. Kalia, S. Ganesh and P. Sinha, Immediate
susceptibility to visual illusions after sight onset, *Curr. Biol.* 25 (2015) R358–R359. D. Amir and C. Firestone,
Is visual perception WEIRD? The Müller-Lyer illusion and the cultural byproduct hypothesis, *Psychol. Rev.* (2025).
M. O. Ernst and M. S. Banks, Humans integrate visual and haptic information in a statistically optimal fashion,
*Nature* 415 (2002) 429–433. D. Alais and D. Burr, The ventriloquist effect results from near-optimal bimodal
integration, *Curr. Biol.* 14 (2004) 257–262. M. Gori, M. Del Viva, G. Sandini and D. C. Burr, Young children do not
integrate visual and haptic form information, *Curr. Biol.* 18 (2008) 694–698. D. Rahnev and R. N. Denison,
Suboptimality in perceptual decision making, *Behav. Brain Sci.* 41 (2018) e223. V. S. Ramachandran, Perception of
shape from shading, *Nature* 331 (1988) 163–166. J. Sun and P. Perona, Where is the sun?, *Nat. Neurosci.* 1 (1998)
183–184. W. J. Adams, E. W. Graf and M. O. Ernst, Experience can change the 'light-from-above' prior, *Nat.
Neurosci.* 7 (2004) 1057–1058. P. Thompson, Perceived rate of movement depends on contrast, *Vision Res.* 22 (1982)
377–380. P. Thompson, K. Brooks and S. T. Hammett, Speed can go up as well as down at low contrast, *Vision Res.* 46
(2006) 782–786. Y. Weiss, E. P. Simoncelli and E. H. Adelson, Motion illusions as optimal percepts, *Nat. Neurosci.*
5 (2002) 598–604. R. J. Snowden, N. Stimpson and R. A. Ruddle, Speed perception fogs up as visibility drops, *Nature*
392 (1998) 450. P. Pretto, J.-P. Bresciani, G. Rainer and H. H. Bülthoff, Foggy perception slows us down, *eLife* 1
(2012) e00031. E. H. Land and J. J. McCann, Lightness and retinex theory, *J. Opt. Soc. Am.* 61 (1971) 1–11. A. L.
Gilchrist, Perceived lightness depends on perceived spatial arrangement, *Science* 195 (1977) 185–187. D. C. Knill and
D. Kersten, Apparent surface curvature affects lightness perception, *Nature* 351 (1991) 228–230. I. Biederman,
Recognition-by-components, *Psychol. Rev.* 94 (1987) 115–147. H. H. Bülthoff and S. Edelman, Psychophysical support
for a two-dimensional view interpolation theory of object recognition, *PNAS* 89 (1992) 60–64. S. Thorpe, D. Fize
and C. Marlot, Speed of processing in the human visual system, *Nature* 381 (1996) 520–522. R. K. Yin, Looking at
upside-down faces, *J. Exp. Psychol.* 81 (1969) 141–145. A. W. Young, D. Hellawell and D. C. Hay, Configurational
information in face perception, *Perception* 16 (1987) 747–759. P. Thompson, Margaret Thatcher: a new illusion,
*Perception* 9 (1980) 483–484. N. Kanwisher, J. McDermott and M. M. Chun, The fusiform face area, *J. Neurosci.* 17
(1997) 4302–4311. D. Y. Tsao, W. A. Freiwald, R. B. H. Tootell and M. S. Livingstone, A cortical region consisting
entirely of face-selective cells, *Science* 311 (2006) 670–674. I. Kennerknecht et al., First report of prevalence of
non-syndromic hereditary prosopagnosia, *Am. J. Med. Genet. A* 140 (2006) 1617–1622. R. Russell, B. Duchaine and K.
Nakayama, Super-recognizers, *Psychon. Bull. Rev.* 16 (2009) 252–257. I. Gauthier et al., Activation of the middle
fusiform 'face area' increases with expertise in recognizing novel objects, *Nat. Neurosci.* 2 (1999) 568–573. D. L.
K. Yamins et al., Performance-optimized hierarchical models predict neural responses in higher visual cortex, *PNAS*
111 (2014) 8619–8624. R. Geirhos et al., ImageNet-trained CNNs are biased towards texture, *ICLR* (2019). D. M. Hoffman, A. R. Girshick, K. Akeley and M. S.
Banks, Vergence-accommodation conflicts hinder visual performance and cause visual fatigue, *J. Vis.* 8(3) (2008) 33.
I. C. Cuthill et al., Disruptive coloration and background pattern matching, *Nature* 434 (2005) 72–74. K. Eykholt et al., Robust physical-world attacks on deep
learning visual classification, *CVPR* (2018). W. S. Geisler, J. S. Perry, B. J. Super and D. P. Gallogly, Edge
co-occurrence in natural images predicts contour grouping performance, *Vision Res.* 41 (2001) 711–724. A. A. Stocker
and E. P. Simoncelli, Noise characteristics and prior expectations in human visual speed perception, *Nat. Neurosci.*
9 (2006) 578–585. R. Held et al., The newly sighted fail to match seen with felt, *Nat. Neurosci.* 14 (2011) 551–553.
W. K. Vong, W. Wang, A. E. Orhan and B. M. Lake, Grounded language acquisition through the eyes and ears of a single
child, *Science* 383 (2024) 504–511. J. S. Bowers and C. J. Davis, Bayesian just-so stories in psychology and
neuroscience, *Psychol. Bull.* 138 (2012) 389–414.

## Problems and solutions

**1. The normal posterior.** log p(s | x) = −(x − s)²/2σ² − (s − μ₀)²/2σ₀² + c = −½(1/σ² + 1/σ₀²)s² + (x/σ² +
μ₀/σ₀²)s + c′. A quadratic with negative leading coefficient is a normal log density: its precision is the
coefficient, 1/σ² + 1/σ₀², and its mean is (x/σ² + μ₀/σ₀²)/(1/σ² + 1/σ₀²) = wx + (1 − w)μ₀ with w = (1/σ²)/(1/σ² +
1/σ₀²). Since the precision exceeds each term, σ_post < min(σ, σ₀).

**2. Vision and touch.** w_V = (1/4)/(1/4 + 1/16) = 0.8, w_H = 0.2; σ = (1/4 + 1/16)^(−1/2) = 1.79 mm, below vision's 2.
The combined percept is 0.8 × 3 + 0.2 × (−3) = 1.8 mm taller than the standard: it follows vision, but not all the way.

**3. When two eyes stop helping.** δ ≈ IΔd/d²: at 0.5 m, 0.063 × 0.01 / 0.25 = 2.52 × 10⁻³ rad ≈ 520″ (8.7′); at
5 m, 2.52 × 10⁻⁵ rad ≈ 5.2″. The second is below a 10″ threshold: invisible to that observer, though the best
observers, at 2″ to 5″, might just see it.

**4. A giant from a distance.** The angle is 2 arctan(0.9/10) = 10.3°. Taken to be 5 m away, the person looks
2 × 5 × tan(5.14°) = 0.90 m tall: half the distance, half the size. The Ames room does the reverse to the person in the
near corner.

**5. The aperture problem with a prior.** With the two normals as the rows of N and the measured normal speeds s, the
log posterior is −|Nv − s|²/2σ² − |v|²/2σ_p², maximized by v̂ = (NᵀN/σ² + I/σ_p²)⁻¹Nᵀs/σ² = (NᵀN + (σ²/σ_p²)I)⁻¹Nᵀs:
ridge regression. As σ → 0 it tends to (NᵀN)⁻¹Nᵀs = N⁻¹s, the intersection of the constraint lines (N is invertible
when the edges are not parallel). As σ grows, ridge regression shrinks most the component of v that N measures
least, the direction along both edges, so v̂ slows and turns toward the edges' normals, and the vector average.

**6. When the diet tips.** See the table below; with the training of `compute.py` (600 images, 400 steps, seed 0) the
share of conflict answers that follow texture rises steeply with q, and crosses one half when only a small minority
of the images are matched: texture is learned from far less evidence than shape, because a 5 × 5 filter sees it
everywhere.

| share of training images with their shape's own texture, q | 0 | 0.02 | 0.05 | 0.10 | 0.15 | 0.2 | 0.4 | 0.6 | 0.8 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|
| conflict answers that follow texture | 31% | 37% | 53% | 58% | 72% | 81% | 90% | 94% | 97% | 95% |

The crossing is near q = 0.05: thirty matched images out of six hundred are enough to make the network answer by
texture as often as by shape.

**7. ★ Learned or present at birth.** Test the prior before the relevant experience could have taught it, and after
experience that contradicts it. Newly sighted people (as in Project Prakash) give a natural test for visual priors: if
a prior is present within hours of sight onset, as the Müller-Lyer illusion was, it was not learned from seeing.
Animals reared in controlled worlds give another: Hershberger (1970) reared chicks with light only from below, and they still pecked at photographed grains as if the light came from above, which points to an inborn prior in chickens. Then retrain it, as Adams, Graf and Ernst did:
a prior that moves with an hour of contrary experience is at least being maintained by learning. A decisive design
needs both, the earliest possible test and a manipulation of the experience, with the prediction of each account
written down beforehand.

## Where it comes back

The other senses, and combining them: Part 15. Priors and prediction errors in learning: Part 17. Attention, and seeing
what you expect: Part 18. What infants know before they learn: Part 30. Displays, headsets and the human in the loop:
Part 51. The predictive brain: Part 58. Deep networks as models of minds: Part 60. Psyche's `infer` module supplies the
posterior, the cue combiner and the observers those parts use.

## Open checks

Before the narrated master:

* Adelson (1995): the board is our own; the values (0.4, 0.8, a shadow of 0.5) are chosen, not Adelson's.
* The Ames room "in the 1940s" is the usual account; the year is not stated.
* Kanizsa's "slightly brighter" triangle and the brightness of illusory figures are the usual account.
* Stereoacuity "a few seconds of arc" and "about 10 arcsec" for a good observer are general statements, as is
  "several people in every hundred" with little or no stereo vision.
* Segall et al.: "more than a dozen societies" and the ordering are from later accounts. Amir and Firestone (2025):
  the summary of their argument is from the abstract and press accounts.
* Ernst and Banks: four observers, the force-feedback arms and the four noise levels are from the abstract and later
  accounts; their weights and thresholds are described, not plotted.
* Ramachandran (1988) and Sun and Perona (1998): "above and a little to the left" is from later accounts.
* Adams, Graf and Ernst (2004): "an hour or two" of training and the lightness task are from the abstract.
* Snowden et al. (1998) and Pretto et al. (2012): from the abstracts.
* Biederman's "few dozen" geons (36 in the paper) and the deletion experiment are from later accounts.
* Thorpe et al. (1996): 20 ms and 150 ms from the abstract; the V1 and IT latencies are approximate.
* Tsao et al. (2006): 97% from the abstract. Kennerknecht et al. (2006): "about 2 in 100" is their estimate (2.5%).
* Yamins et al. (2014): "about half of the predictable variance" is from summaries.
* Held et al. (2011): "within two days" and "within days" are from the abstract.
* Vong et al. (2024): 61 hours, 6 to 25 months and about 1% are from the paper's abstract and summaries.
* Hershberger (1970), in problem 7, is cited from memory as an example of a rearing study.
