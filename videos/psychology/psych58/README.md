# Psychology, Built: Part 58, The Efficient, Predictive Brain

In 1961 Horace Barlow proposed that sensory neurons exist to remove redundancy from their input. In 1996 Bruno
Olshausen and David Field asked a network to describe patches of natural photographs with as few active units as
possible, and its units turned into the oriented, localized receptive fields Hubel and Wiesel had found in cortex.
An optimization principle produced biology. The part opens with that optimization run on screen on Psyche's
dead-leaves images, then follows its most ambitious descendants, up to a theory that claims to explain everything a
brain does, and asks what each would have to risk.

The viewer adapts to tilted gratings and sees the tilt after-effect, then predicts four numbers. Then efficient
coding (Attneave, Barlow, Laughlin's fly and its histogram-matching code, whitening and the centre-surround filter
it implies); sparse coding written out and compared with principal components; efficient-coding biases (the tilt
after-effect from adaptation in a population code, Wei and Stocker's repulsion, Weber's law, capacity, value);
rate-distortion theory and Shepard's law of generalization; normalization as a canonical computation; predictive
coding built small enough to watch, and what the physiology does and does not support; the free energy derived step
by step, the principle, and the charge of unfalsifiability; the Bayesian brain and its critics; resource
rationality and "one and done"; learning rules (feedback alignment, predictive coding as approximate
backpropagation, meta-learning); and unified theories from Newell to the common model, with a scorecard of what
each principle risked.

## Where the numbers come from

| What | Source |
|---|---|
| Six 128 by 128 dead-leaves images (discs with radius density proportional to r^-3 between 1.5 and 40 pixels, uniform grey levels, occluding); 20,000 random 8 by 8 patches, mean removed | Psyche (`efficient.dead_leaves`, `patches`), items `images` and `sparse` |
| Patch spectrum and whitening (ZCA, regularized at 1% of the largest eigenvalue); the whitening filter for one pixel: centre about 6.3, nearest surround about -0.6 to -0.7 | Psyche (`efficient.zca`), item `images` |
| Sparse coding: 64 basis functions, whitened patches (regularized at 100%, a low-pass roll-off), lambda 0.4, ISTA with 80 steps per batch of 500, 400 dictionary steps; median localization 0.80 (energy in the strongest 3 by 3 spot) against 0.25 for principal components and 0.26 for random patterns; orientedness 0.36 against 0.22 and 0.13 | Psyche (`efficient.learn_dictionary`, `localization`), item `sparse` |
| Laughlin's code: local contrasts in Psyche's images, 20 levels: 4.21 bits per response at the quantiles, 3.68 evenly spaced (4.32 at most) | Psyche (`efficient.laughlin`), items `laughlin` and `codes` |
| Efficient-coding bias with a cardinal prior (density 2 - abs(sin 2 theta)), encoding noise 0.08 in the warped space: repulsive biases up to 2.6 degrees | Psyche (`efficient.efficient_bias`), item `bias` |
| Rate-distortion on 41 points with squared-error cost at beta = 0.02, 0.1, 0.5: rates 1.2, 2.2 and 3.3 bits | Psyche (`efficient.blahut_arimoto`), item `rd` |
| Normalization: n = 2, sigma = 0.15, masks 0, 0.2 and 0.5 | Psyche (`efficient.normalization`), item `norm` |
| Predictive coding: 16 inputs, 4 causes, prior precision 1; error activity 0.16 for an expected input and 5.7 for a surprising one at the start | Psyche (`efficient.predictive_coding`), item `pc` |
| Free energy: prior N(0, 1), x = 2, noise SD 0.5; posterior mean 1.6, surprise 2.63 nats | Psyche (`efficient.free_energy_gaussian`), item `fe` |
| Tilt after-effect: 72 units with tuning width 20 degrees, gain lost up to 50% near the adapter; shifts peak at 4.3 degrees about 25 degrees away (4 degrees at 20) | Psyche (`efficient.tilt_aftereffect`), item `tilt` |
| One and done: each sample right with probability 0.65, cost 0.02 per sample; reward rate best at one sample | Psyche (`efficient.samples_value`), item `samples` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/efficient.py`: dead-leaves images, patches, whitening, sparse coding by ISTA with
  dictionary learning and a localization measure, Laughlin's code, an efficient-coding observer, Blahut-Arimoto
  rate-distortion and generalization, normalization, a predictive-coding network, a Gaussian free energy, the tilt
  after-effect and resource-rational sampling. Tested in `tests/psychology/test_efficient.py`.
* The Ledger gains four rows.
* The course's interactive: adapt to a grating, then judge test lines, and see the after-effect predicted by a
  population of adapting units.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| A code that describes natural image patches with as few active units as possible learns localized, oriented, band-pass basis functions like the receptive fields of simple cells in primary visual cortex. | Olshausen and Field 1996 | replicated |
| An encoder that spends its precision where stimuli are common, read out by a Bayesian decoder, predicts biases away from the common values, and a lawful link between bias and discrimination threshold. | Wei and Stocker 2015 | replicated |
| Cortex is organized as predictive coding requires: predictions sent down a hierarchy, and distinct neurons that signal the error between prediction and input sent up. | Rao and Ballard 1999 | contested |
| Everything a brain does, perceiving, learning and acting, minimizes variational free energy, a bound on the surprise of its sensory states. | Friston 2010 | not directly tested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Barlow; Laughlin; Sims;
Carandini and Heeger; Bowers and Davis; Vul and colleagues; Lieder and Griffiths; Lillicrap and colleagues; Newell.

## Build it

```bash
python -m videos.psychology.psych58.compute            # every number (a minute)
python tools/qa_scene.py psych58 Sparse                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych58 -q l   # the whole part, silent preview
python tools/build.py psych58                          # 1080p30 with narration
python tools/qa_scene.py psych58 Free --lang zh        # the Chinese edition of one chapter
python tools/make.py psych58                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 58                    # the lab: sparse coding, efficient biases, after-effects
python tools/check_ledger.py psych58                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's efficient module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A network that grew receptive fields | Sparse coding on screen; the question; objectives |
| 1 | On you: an after-effect, and four numbers | The tilt after-effect, experienced; four predictions |
| 2 | Efficient coding | Redundancy; a fly's contrast code; centre-surround derived |
| 3 | Sparse coding | The objective; sparse against principal components; how far it goes |
| 4 | Efficiency explains biases | The tilt after-effect predicted; repulsive biases; Weber, capacity and value |
| 5 | Rate-distortion | Shannon's other theorem; Shepard's law derived |
| 6 | Normalization | One equation; the same equation everywhere |
| 7 | Predictive coding | Predictions down, errors up; error units; what the evidence supports |
| 8 | The free-energy principle | Variational inference step by step; a small model's free energy; the claims |
| 9 | The Bayesian brain and its critics | Successes; critics; how to keep it honest |
| 10 | Resource rationality | One and done; optimal use of limited computation |
| 11 | Learning rules | Backpropagation and the brain; learning to learn |
| 12 | Unified theories | Newell's twenty questions; what each principle risked |
| 13 | The Ledger | Four rows; what they have in common |
| 14 | In practice: codecs and representations | Where this is a job; twenty levels, worked |
| 15 | Frontier: one principle? | What is new; open problems |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; payoffs; problems; references; Part 59 |

## Sources

* F. Attneave, Some informational aspects of visual perception, *Psychological Review* 61 (1954) 183-193; H. B.
  Barlow, Possible principles underlying the transformations of sensory messages, in W. A. Rosenblith (ed.),
  *Sensory Communication* (MIT Press, 1961) 217-234; S. Laughlin, A simple coding procedure enhances a neuron's
  information capacity, *Zeitschrift fur Naturforschung C* 36 (1981) 910-912; J. J. Atick and A. N. Redlich, What
  does the retina know about natural scenes?, *Neural Computation* 4 (1992) 196-210; E. P. Simoncelli and B. A.
  Olshausen, Natural image statistics and neural representation, *Annual Review of Neuroscience* 24 (2001)
  1193-1216.
* B. A. Olshausen and D. J. Field (1996); A. J. Bell and T. J. Sejnowski (1997); J. H. van Hateren and A. van der
  Schaaf (1998); D. L. Ringach (2002); M. S. Lewicki, Efficient coding of natural sounds, *Nature Neuroscience* 5
  (2002) 356-363; D. H. Hubel and T. N. Wiesel, Receptive fields of single neurones in the cat's striate cortex,
  *Journal of Physiology* 148 (1959) 574-591.
* X.-X. Wei and A. A. Stocker (2015, 2017); D. Ganguli and E. P. Simoncelli, Efficient sensory encoding and Bayesian
  inference with heterogeneous neural populations, *Neural Computation* 26 (2014) 2103-2134; C. W. G. Clifford et
  al., Visual adaptation: neural, psychological and computational aspects, *Vision Research* 47 (2007) 3125-3131.
* C. E. Shannon, Coding theorems for a discrete source with a fidelity criterion, *IRE National Convention Record*
  (1959) 142-163; R. Blahut, Computation of channel capacity and rate-distortion functions, *IEEE Transactions on
  Information Theory* 18 (1972) 460-473; R. N. Shepard, Toward a universal law of generalization for psychological
  science, *Science* 237 (1987) 1317-1323; C. R. Sims, Efficient coding explains the universal law of generalization
  in human perception, *Science* 360 (2018) 652-656.
* D. J. Heeger, Normalization of cell responses in cat striate cortex, *Visual Neuroscience* 9 (1992) 181-197; M.
  Carandini and D. J. Heeger, Normalization as a canonical neural computation, *Nature Reviews Neuroscience* 13
  (2012) 51-62; J. H. Reynolds and D. J. Heeger, The normalization model of attention, *Neuron* 61 (2009) 168-185;
  O. Schwartz and E. P. Simoncelli, Natural signal statistics and sensory gain control, *Nature Neuroscience* 4
  (2001) 819-825.
* R. P. N. Rao and D. H. Ballard (1999); G. B. Keller, T. Bonhoeffer and M. Hubener (2012); K. S. Walsh et al.
  (2020).
* K. Friston (2010); M. Andrews (2021); T. Parr, G. Pezzulo and K. J. Friston, *Active Inference* (MIT Press, 2022).
* M. O. Ernst and M. S. Banks, Humans integrate visual and haptic information in a statistically optimal fashion,
  *Nature* 415 (2002) 429-433; K. P. Kording and D. M. Wolpert, Bayesian integration in sensorimotor learning,
  *Nature* 427 (2004) 244-247; Y. Weiss, E. P. Simoncelli and E. H. Adelson, Motion illusions as optimal percepts,
  *Nature Neuroscience* 5 (2002) 598-604; J. S. Bowers and C. J. Davis, Bayesian just-so stories in psychology and
  neuroscience, *Psychological Bulletin* 138 (2012) 389-414; M. Jones and B. C. Love, Bayesian fundamentalism or
  enlightenment?, *Behavioral and Brain Sciences* 34 (2011) 169-188; D. Rahnev and R. N. Denison, Suboptimality in
  perceptual decision making, *Behavioral and Brain Sciences* 41 (2018) e223.
* E. Vul, N. Goodman, T. L. Griffiths and J. B. Tenenbaum, One and done? Optimal decisions from very few samples,
  *Cognitive Science* 38 (2014) 599-637; F. Lieder and T. L. Griffiths, Resource-rational analysis, *Behavioral and
  Brain Sciences* 43 (2020) e1.
* T. P. Lillicrap, D. Cownden, D. B. Tweed and C. J. Akerman, Random synaptic feedback weights support error
  backpropagation for deep learning, *Nature Communications* 7 (2016) 13276; J. C. R. Whittington and R. Bogacz, An
  approximation of the error backpropagation algorithm in a predictive coding network with local Hebbian synaptic
  plasticity, *Neural Computation* 29 (2017) 1229-1262; T. P. Lillicrap, A. Santoro, L. Marris, C. J. Akerman and G.
  Hinton, Backpropagation and the brain, *Nature Reviews Neuroscience* 21 (2020) 335-346; J. X. Wang et al.,
  Prefrontal cortex as a meta-reinforcement learning system, *Nature Neuroscience* 21 (2018) 860-868.
* A. Newell, You can't play 20 questions with nature and win, in W. G. Chase (ed.), *Visual Information Processing*
  (Academic Press, 1973) 283-308; J. R. Anderson, *How Can the Human Mind Occur in the Physical Universe?* (Oxford
  University Press, 2007); J. E. Laird, C. Lebiere and P. S. Rosenbloom, A standard model of the mind, *AI Magazine*
  38 (2017) 13-26.

## Problems and solutions

1. **Laughlin's rule.** Laughlin's rule: contrasts are uniform on $[-1, 1]$. The best response curve? And if they are normal?

   *Solution.* The response is the cumulative distribution: for contrasts uniform on [-1, 1], the straight
   line (c + 1)/2; for normal contrasts, the normal CDF, a sigmoid steepest at the mean.
2. **Whitening.** Image power falls as $1/f^2$. How must a whitening filter's gain grow with $f$, and what does that do to noise?

   *Solution.* Power falls as 1/f^2, so amplitude as 1/f; the filter's gain must grow as f to flatten it. That
   amplifies high-frequency noise without limit, so a real filter rolls off where noise dominates (the retina's
   band-pass shape).
3. **Normalization.** Normalization with $n = 2$, $\sigma = 0.15$: the response to $c = 0.15$ alone, and with a mask of 0.15?

   *Solution.* Alone: 0.0225/(0.0225 + 0.0225) = 0.5. With a mask of 0.15: 0.0225/0.0675 = 1/3.
4. **Variational inference by hand.** Prior N(0, 1), reading $x = 2$ with noise SD 0.5. The posterior mean and variance, and the surprise?

   *Solution.* Posterior precision 1 + 4 = 5, variance 0.2, mean (2 x 4)/5 = 1.6. Surprise:
   -log N(2; 0, 1.25) = 0.5 log(2 pi x 1.25) + 4/2.5 = 1.03 + 1.6 = 2.63 nats.
5. **A majority of three.** Each sample is right with probability 0.65. The accuracy of a majority of three?

   *Solution.* p^3 + 3p^2(1 - p) = 0.275 + 0.444 = 0.718.
6. **Against free energy.** "The brain minimizes free energy." What observation would count against it?

   *Solution.* As a principle, nothing: any behaviour has some generative model under which it
   minimizes free energy. A specific model (a stated generative model with measured priors and precisions) can be
   refuted by behaviour or physiology it does not predict; that is where the principle's content is tested.
7. ★ **Predictive coding against adaptation.** Design an experiment that separates predictive coding from adaptation as the cause of a mismatch response.

   *Solution.* Use a many-standards control: present the deviant tone in a sequence
   where it is as rare as in the oddball sequence but no standard sets a prediction. Adaptation predicts the same
   response in both (equal rarity); predictive coding predicts a larger response in the oddball sequence. Add
   omissions (a predicted tone left out): adaptation predicts no response, predictive coding an error response.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Hubel and Wiesel's 1959 paper; Attneave (1954); Barlow (1961) and its pages; Laughlin (1981)'s cells and habitat
measurements; Atick and Redlich (1992); Olshausen and Field (1996) and its patch sizes; Bell and Sejnowski (1997);
van Hateren and van der Schaaf (1998); Ringach (2002); Lewicki (2002); Wei and Stocker (2015, 2017) and the 2017
rule's form; Ganguli and Simoncelli (2014); Shannon (1959); Blahut (1972) and Arimoto; Shepard (1987); Sims (2018)'s
claim and data; Heeger (1992); Reynolds and Heeger (2009); Schwartz and Simoncelli (2001); Rao and Ballard (1999)
and end-stopping; Keller, Bonhoeffer and Hubener (2012); Walsh et al. (2020); Friston (2010); Andrews (2021); Ernst
and Banks (2002); Kording and Wolpert (2004); Weiss, Simoncelli and Adelson (2002); Bowers and Davis (2012); Jones
and Love (2011); Rahnev and Denison (2018); Vul et al. (2014); Lieder and Griffiths (2020); Lillicrap et al. (2016,
2020); Whittington and Bogacz (2017); Wang et al. (2018) and Harlow's learning sets; Newell (1973); Laird, Lebiere
and Rosenbloom (2017); and every page range in Sources.
