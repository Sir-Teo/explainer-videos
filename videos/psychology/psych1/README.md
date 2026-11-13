# Psychology, Built — Part 1: Kant's Wager

Part 1 of a sixty-two-part course in psychology (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), opening Act I, *Asking a Mind a Question*. It asks whether a mind can be measured at
all, and answers with the first measurements that were made.

It opens in 1786 with Kant's three reasons why psychology could never be a science: no mathematics, no experiment,
and an observer who disturbs what is observed. The part keeps score against them. From there it covers:

- your own simple and choice reaction time (the first demonstration on the viewer), and the right-skewed shape of
  a reaction-time distribution;
- Helmholtz's 1850 measurement of the speed of a nerve signal, his arithmetic, and the fifteen-year dispute over
  the human value that ended by finding temperature;
- Donders' three methods (1868), his subtraction, and the first model of the series: a chain of stages whose
  durations add;
- what subtraction assumes (pure insertion), Wundt's objection, a rival model with the same three means, the
  distributional test (variances must add), and Sternberg's additive factors;
- Fechner's law, derived from Weber's fraction by counting just-noticeable steps;
- Wundt's laboratory, Ebbinghaus's forgetting data, James, and the dispute that introspection could not settle;
- behaviourism, and the two findings from inside it that needed something in the head: Tolman's maps and Lashley's
  plans;
- the cognitive revolution of 1956, Shannon's bit and Hick's law;
- Marr's three levels of explanation, with his cash register;
- the homunculus, and Dennett's rule for discharging it;
- the series' four devices: Psyche, the Pool, the Battery and the Ledger;
- the first five rows of the Ledger; reaction time in practice; and a frontier chapter on what a reaction time
  measures.

Every number on screen is computed in [`compute.py`](compute.py), taken from the Archive with its source, or cited:

- **Historical data** (the Archive, [`explainer/psychology/archive`](../../../explainer/psychology/archive/__init__.py),
  with checks in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md)): Kant's Preface in Bax's 1883
  translation; Helmholtz's nerve lengths, delays and speeds as reported by Schmidgen (2002); Donders' three means as
  given by Roelofs (2018); Ebbinghaus's retention table from chapter VII of *Memory*; the summary statistics of
  Woods et al. (2015).
- **Psyche** (orange on screen): stage models of reaction time. The stage durations of the Donders model are his
  two differences. The choice stages used for the shape of a reaction-time distribution in Chapter 1 are
  illustrative and are tagged so.
- **The Pool** (grey-blue, tagged `simulated`): Donders' experiment on 300 simulated people, and one person on
  three devices. The device delays are illustrative.
- **Schematics**, tagged: the twitch curves and Donders' drum record, the Weber fraction of one tenth, the curves
  after Tolman and Honzik (1930), Lashley's time line.

**Built in this part:**

- **`psyche.chronometry`** ([`explainer/psychology/psyche/chronometry.py`](../../../explainer/psychology/psyche/chronometry.py)):
  serial stage models with gamma stages (exact mean, variance and third moment; densities by convolution), Donders'
  models and a rival with the same means, the subtraction with standard errors, the distributional test of pure
  insertion, additive-factor tables, Hick's law, and the ex-Gaussian with a maximum-likelihood fit. Checked against
  closed forms and SciPy in `tests/psychology/test_chronometry.py`.
- **The Pool** ([`explainer/psychology/pool.py`](../../../explainer/psychology/pool.py)): 100,000 simulated people
  with planted reaction-time stages, a general speed factor, an age slope and, for half of them, a decision inside
  go/no-go. `tests/psychology/test_pool.py` checks that the planted values are recoverable.
- **The Battery** ([`explainer/psychology/battery.py`](../../../explainer/psychology/battery.py)): the list of
  thirteen tasks and the trial-level data format; task 1 (reaction time) runs.
- **The Ledger** ([`explainer/psychology/ledger.py`](../../../explainer/psychology/ledger.py)) and **the Archive**.
- **The instruments** ([`explainer/psychology/viz.py`](../../../explainer/psychology/viz.py)): the Homunculus map,
  the On-you stage, the trial strip, stage bars, study and Ledger cards.

The Ledger gains five rows:

| Finding | Original | Status |
|---|---|---|
| The nerve signal travels at a finite, measurable speed | Helmholtz 1850 | replicated (the human value depended on temperature) |
| Mental operations take measurable time: a < c < b | Donders 1868 | replicated |
| Donders' differences are the durations of pure stages | Donders 1868 | contested (Wundt 1880; Roelofs 2018) |
| Choice time grows with the logarithm of the number of alternatives | Hick 1952 | replicated (derived in Part 25) |
| Simple reaction times have slowed since the Victorians | Woodley et al. 2013 | contested (Woods et al. 2015: hardware delays) |

## Build it

```bash
python -m videos.psychology.psych1.compute            # every number (a few seconds), into .cache/psych1/
python tools/qa_scene.py psych1 Donders               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych1 -q l   # the whole part, silent preview
python tools/build.py psych1                          # 1080p30 with narration
python tools/qa_scene.py psych1 Donders --lang zh     # the Chinese edition of one chapter
python tools/make.py psych1                           # both editions, with the checks a long build needs
python -m pytest tests/psychology                     # Psyche, the Pool, the Ledger and the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Kant's wager | Kant's three objections, drawn; the wager; the morning of 22 October 1850; the series' three questions; objectives |
| 1 | How fast are you? | On you: three simple reactions and four choices. What people get: 213 ms for a simple reaction in 1,469 adults; a choice is slower and its distribution leans. The puzzle: what is the extra time? |
| 2 | The speed of a nerve | Helmholtz's frog preparation and two stimulation sites; v = Δx/Δt gives 25 to 43 m/s; the human measurements from 1850 to 1869; the tenth of a second left over for the brain |
| 3 | Subtracting one task from another | Donders' drum, the three methods a, b and c, his means 201, 284 and 237 ms; c − a = 36 ms and b − c = 47 ms; Psyche's stage model reproduces them |
| 4 | What subtraction assumes | Pure insertion; Wundt's objection; a rival model with the same means; Donders' notebook; the convolution picture and the variance check in two model worlds; additive factors |
| 5 | Measuring a sensation | Weber's fraction; Fechner's count of just-noticeable steps; S = (1/k) ln(I/I₀) derived |
| 6 | The first laboratories | Wundt's two tools; Ebbinghaus's savings after seven intervals with his own fitted curve; James; imageless thought and the stalemate of introspection |
| 7 | Banning the mind | Watson's manifesto; the black box; Tolman's latent learning; Lashley's pianist |
| 8 | The mind comes back | The computer as a licence; 11 September 1956; bits; Hick's law as a prediction for Psyche |
| 9 | Three levels of explanation | Marr's cash register at three levels; reaction time at three levels; the levels strip |
| 10 | The little person in the head | The homunculus regress; Dennett's rule; the map of twenty faculties; the first gear |
| 11 | What the series builds | Psyche; the Pool, where the group average of b − c describes no one; the Battery; the series map |
| 12 | The Ledger opens | Why a ledger; the seven statuses; one row in full; today's five rows |
| 13 | In practice: reaction time at work | Road design, interface latency, clinical screening, the false-start rule; the practice card |
| 14 | Frontier: what is a reaction time measuring? | The "Victorians were faster" claim and hardware delays; one person on three devices; three open questions; the research problem |
| | Recap, problems, and the road ahead | Ten lines; Kant's scoreboard; payoffs; problems; references; Part 2 |

## Sources

**Books.** E. G. Boring, *A History of Experimental Psychology* (2nd ed., 1950). K. Danziger, *Constructing the
Subject* (1990). R. D. Luce, *Response Times* (1986). R. S. Woodworth, *Experimental Psychology* (1938). D. Marr,
*Vision* (1982), ch. 1. D. C. Dennett, *Brainstorms* (1978). H. Gardner, *The Mind's New Science* (1985).

**Papers and primary texts.**
- I. Kant, *Metaphysische Anfangsgründe der Naturwissenschaft* (1786), Preface; English by E. B. Bax (1883).
- H. Helmholtz, "Vorläufiger Bericht über die Fortpflanzungsgeschwindigkeit der Nervenreizung", *Archiv für
  Anatomie, Physiologie und wissenschaftliche Medicin* (1850) 71–73.
- H. Schmidgen, "Of frogs and men: the origins of psychophysiological time experiments, 1850–1865", *Endeavour* 26
  (2002) 142–148.
- G. T. Fechner, *Elemente der Psychophysik* (1860).
- F. C. Donders, "Over de snelheid van psychische processen" (1868); transl. W. G. Koster, *Acta Psychologica* 30
  (1969) 412–431.
- A. Roelofs, "One hundred fifty years after Donders", *Acta Psychologica* 191 (2018) 228–233.
- H. Ebbinghaus, *Über das Gedächtnis* (1885); transl. Ruger and Bussenius, *Memory* (1913).
- J. B. Watson, "Psychology as the behaviorist views it", *Psychological Review* 20 (1913) 158–177.
- E. C. Tolman and C. H. Honzik (1930); E. C. Tolman, "Cognitive maps in rats and men", *Psychological Review* 55
  (1948) 189–208.
- K. S. Lashley, "The problem of serial order in behavior" (1951).
- W. E. Hick, "On the rate of gain of information", *QJEP* 4 (1952) 11–26; R. Hyman (1953); R. W. Proctor and
  D. W. Schneider, "Hick's law for choice reaction time: a review", *QJEP* 71 (2018) 1281–1299.
- S. Sternberg, "The discovery of processing stages: extensions of Donders' method", *Acta Psychologica* 30 (1969)
  276–315.
- J. L. McClelland, "On the time relations of mental processes: an examination of systems of processes in cascade",
  *Psychological Review* 86 (1979) 287–330.
- G. A. Miller, "The cognitive revolution: a historical perspective", *Trends in Cognitive Sciences* 7 (2003)
  141–144.
- M. A. Woodley, J. te Nijenhuis and R. Murphy, *Intelligence* 41 (2013) 843–850; D. L. Woods et al., *Frontiers in
  Human Neuroscience* 9 (2015) 131.

## Problems and solutions

**1.** *A nerve is stimulated at two points 55 mm apart, and the twitch from the farther point begins 1.7 ms
later. What speed does that give, and how long would such a signal take to travel one metre?*

v = Δx/Δt = 0.055 m / 0.0017 s ≈ 32.4 m/s. One metre takes 1/32.4 s ≈ 31 ms. That is inside Helmholtz's range of
25 to 43 m/s, and it shows why conduction alone cannot account for a reaction time of 200 ms.

**2.** *Donders' means were 201 ms (a), 237 ms (c) and 284 ms (b). Compute his two differences. Now suppose
go/no-go contains a 30 ms decision, and the choice task a 25 ms stage that programs the response. What are the
durations of discrimination and of choice?*

Donders: c − a = 36 ms (discrimination), b − c = 47 ms (choice). In the rival model c = a + discrimination + 30, so
discrimination = 6 ms; and b = a + discrimination + choice + 25, so 284 = 201 + 6 + choice + 25 and choice = 52 ms.
The three means are the same in both models. Means alone do not identify the stages: the answer depends on which
stages you assume are present. (`chronometry.prepared_models()` is this model.)

**3.** *Show that if RT_c = RT_a + D with D independent of RT_a, then Var[RT_c] = Var[RT_a] + Var[D]. A subject's
variances are 900 ms² in task a and 700 ms² in task c. What follows?*

Var[X + D] = Var[X] + Var[D] + 2 Cov[X, D], and the covariance of independent variables is zero. With the
subject's numbers Var[D] = 700 − 900 = −200 ms², which no random variable has. So, sampling error aside, task c is
not task a plus an independent stage: either the stages shared by the two tasks behaved differently in c (were less
variable), or the extra stage's duration is negatively related to the rest. Before concluding, put a standard
error on the difference of variances (a bootstrap, as in `chronometry.insertion_test`).

**4.** *Two factors multiply the mean duration of the same 50 ms stage by 1.4 and by 1.6. Write the 2 × 2 table of
mean reaction times (the other stages total 250 ms) and its interaction contrast. Repeat with the factors acting
on two different 50 ms stages.*

Same stage: the stage takes 50, 70, 80 or 50 × 1.4 × 1.6 = 112 ms.

| | factor 2 easy | factor 2 hard |
|---|---|---|
| factor 1 easy | 300 | 330 |
| factor 1 hard | 320 | 362 |

Interaction: 362 − 320 − 330 + 300 = 12 ms, which is 50 × 0.4 × 0.6. Different stages (two stages of 50 ms, the
others totalling 200 ms so that the baseline is again 300): 300, 330, 320 and 350. Interaction: 0. Additive
effects are what separate stages predict; an interaction says the factors meet somewhere.

**5.** *A website reports that phone users have slower reaction times than laptop users. Give three explanations
other than "phone users are slower", and a design that would separate them.*

(i) The devices: a touch screen and a phone display add delays a keyboard and monitor do not, and a constant delay
shifts every time. (ii) The response: a tap on glass and a key press are different movements with different motor
stages. (iii) The people and the setting: phone users may be older or younger, and are more often walking,
distracted or holding the device in one hand. (iv) Selection: who chooses to take a reaction-time test on a phone.
Designs: measure each device's delay with an external sensor and subtract it; test the same people on both devices
in counterbalanced order; or report a difference between two conditions (choice minus simple), which a constant
delay cannot change. Random assignment of people to devices removes (iii) and (iv).

**6.** *With `explainer.psychology.psyche.chronometry`: simulate 2,000 choice reaction times, fit an ex-Gaussian,
then double the mean of the choice stage and fit again. Which of μ, σ, τ move?*

```python
import numpy as np
from explainer.psychology.psyche import chronometry as ch
rng = np.random.default_rng(0)
b = ch.donders_models()["b"]
print(ch.fit_exgauss(b.sample(2000, rng)))
print(ch.fit_exgauss(b.with_stage("choose", mean=94.0).sample(2000, rng)))
```

With seed 0: μ goes from 254 to 279 ms, σ from 27 to 38, τ from 31 to 52. All three move. Lengthening one stage
does not change one ex-Gaussian parameter: the ex-Gaussian describes the shape of the distribution well, but its
parameters are not the durations of stages. That caution returns in Part 25.

**7 (★, research).** *Design an experiment on Battery task 1 whose reaction-time distributions would separate
discrete stages from a cascade.*

What is known. Discrete serial stages with selectively influenced durations predict additive effects on mean RT
and, more strongly, that the effect of each factor is a convolution: the cumulants of the factor effects add
(the "summation test" on whole distributions). McClelland's cascade (1979) passes activation forward
continuously; it also produces additive means when factors change the rates of different levels, but a factor
that changes a level's asymptote rather than its rate produces interactions, and the distributional predictions
differ. How a researcher would attack it: choose two factors with good evidence of selective influence (stimulus
contrast; number of alternatives), collect enough trials per cell and per person for stable distributions (several
hundred), and test the summation prediction with the distribution-level tests of Ashby and Townsend (1980) and
Roberts and Sternberg (1993) instead of a test on means; then fit both model classes to the same trial-level data
with a recovery check (Part 48). The place to start in this repository is `chronometry.insertion_test` and
`factorial_means`, generalized from two tasks to a 2 × 2 design, with a cascade model to be written beside them.

## Where it comes back

- Fechner's law and your own threshold: Part 11. Signal detection replaces the threshold: Part 12.
- Donders' subtraction as the logic of brain imaging, with its pure-insertion problem: Part 8.
- Additive factors and memory scanning: Part 19. Ebbinghaus's curve: Parts 20 and 21.
- The shape of reaction-time distributions, the diffusion model and Hick's law derived: Part 25; in interfaces,
  Part 52.
- The group average that describes no one: Parts 47 and 48. Difference scores as measures of people: Parts 3 and 59.
- Kant's third objection: Part 2 (Clever Hans) and Part 4 (the replication crisis).
- The Homunculus's last drawing, and Psyche on the whole Battery: Part 62.

## Open checks

Before the narrated master, read the full text of Roelofs (2018) and of Koster's translation of Donders for the
three means and the task details; neither could be retrieved when the part was written (see
[`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md)). The practice figures of Chapter 13 (the 2.5 s of
highway design, the 0.1 s of interface response, the 0.100 s false-start rule) are stated from the standard
references named on screen and should be checked against their current editions.
