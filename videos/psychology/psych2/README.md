# Psychology, Built: Part 2, The Experiment

Berlin, 1904. A horse named Hans answers arithmetic with his hoof, and a commission of thirteen, with a circus
manager, a zoo director and the head of Berlin's Psychological Institute among them, finds no trick. One student,
Oskar Pfungst, changes one thing at a time and counts. Hans is right 98 times in 100 when the questioner knows the
answer and 8 in 100 when he does not. Nobody cheated: the questioners were giving the answer away with a movement
of the head of about a millimetre, too small for them to feel, and 23 of 25 people did the same for Pfungst in the
laboratory.

Every rule of experimental design in psychology is a way of asking a mind a question without telling it the
answer, and most of them are in that story. The part builds them one at a time on a single example, a game said to
sharpen your reactions, studied on the Pool where the truth is known: the comparison, the control group, the
shuffled deck (which psychologists used first, in 1884), each person as their own control, the blind, the
factorial design, four kinds of validity, and the rules that protect the people in an experiment. Kant's second
objection, that there can be no experiment on the mind, is answered; his third, that the observer disturbs, gets
its first reply.

## Where the numbers come from

| What | Source |
|---|---|
| Hans, the commission of 12 September 1904, Pfungst's counts, the laboratory tests | Pfungst (1907; transl. 1911), read from the translation; registered in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md) |
| The shuffled deck of 1884 | Peirce and Jastrow, "On small differences in sensation" |
| The "bright" and "dull" rats, day by day | Rosenthal and Fode (1963), Table 1 |
| Teacher expectancy by weeks of contact | Raudenbush (1984) |
| Detection dogs | Lit, Schweitzer and Oberbauer (2011) |
| Demand effects, measured | de Quidt, Haushofer and Roth (2018) |
| Unblinding in a drug trial | Mitchell et al. (2021) |
| The model of Hans | `explainer.psychology.psyche.cueing`: four parameters fitted by maximum likelihood to Pfungst's eight conditions |
| Every study of "the game" | `explainer.psychology.lab` on the Pool. Simulated: the truth is planted (zero, or −8 ms), and each example study shown is the median of 101, not a chosen one |
| The run-of-four figure, the predictor's hit rates | computed in `compute.py` (`be_random`) |

Two things on screen are illustrative and say so: the scatter in the regression-to-the-mean picture, and the room
in the detection-dog scene.

## Built in this part

* `explainer/psychology/lab.py`, the laboratory: assignment by shuffle, balance, Welch and paired comparisons, the
  randomization test, Latin and Williams squares, power for between- and within-person designs, the interaction
  contrast, and a `Lab` that runs the randomized experiment, the cross-over and Campbell and Stanley's six unsound
  designs on the Pool with the truth known. Also a predictor of two-key sequences, the one the interactive uses.
* `explainer/psychology/psyche/cueing.py`: Clever Hans as a mechanism. A questioner who gives a cue only if he
  knows the answer; a reader whose chance of seeing it falls with distance as a psychometric function.
* The Pool gains repeat sessions (practice, day-to-day variation) and an eagerness to sign up for things, which
  goes with being young and quick. Part 1's people are unchanged.
* No new gear on the Homunculus map. Parts 2 to 4 build the laboratory, the ruler and the rules of evidence.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| An animal reads its handler | Pfungst 1907 | replicated |
| "Bright" rats learn faster | Rosenthal and Fode 1963 | not directly tested |
| Teachers' expectations raise IQ | Rosenthal and Jacobson 1968 | replicated, smaller |
| Subjects do what they think is wanted | Orne 1962 | replicated |
| People cannot be random | Wagenaar 1972 | replicated |

## Build it

```bash
python -m videos.psychology.psych2.compute            # every number (a few seconds), into .cache/psych2/
python tools/qa_scene.py psych2 Pfungst               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych2 -q l   # the whole part, silent preview
python tools/build.py psych2                          # 1080p30 with narration
python tools/qa_scene.py psych2 Pfungst --lang zh     # the Chinese edition of one chapter
python tools/make.py psych2                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 2                    # the lab: six wrong designs and one right one
python tools/check_ledger.py psych2                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                     # the laboratory, the Pool, the Ledger and the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md). Code on screen stays as it is run; its comments are translated.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Clever Hans | The courtyard; the commission of thirteen and its report; Kant's scoreboard; the question; objectives |
| 1 | Who knows the answer? | Pfungst's "procedure without knowledge" (98% against 8%); blinders (89% against 6%); the cue; the questioner moved away, with the cue-reading model; Pfungst as the horse, 23 of 25 |
| 2 | On you: the pendulum and the coin | Chevreul's pendulum and ideomotor action; be a coin; why a program can guess you |
| 3 | Compared with what? | Variables and an operational definition; a useless game that "works" in one group tested twice; the control group |
| 4 | Six ways to fool yourself | Testing, history, maturation, regression, selection, attrition, each run on the Pool with the truth zero; regression to the mean; the confound; the randomized experiment 500 times |
| 5 | Shuffling the cards | Peirce and Jastrow, 1884; what a shuffle balances, measured or not, and by how much; the randomization test |
| 6 | Between people and within them | An effect seen through people's differences; pairing and the correlation of a person with themselves; order effects and counterbalancing; Latin and Williams squares |
| 7 | The experimenter is a subject too | Rosenthal and Fode's rats; Pygmalion and its record; detection dogs; demand characteristics, measured; who is blind |
| 8 | It depends | Factorial designs; parallel, fanning and crossing lines; an interaction that vanishes on a logarithmic scale |
| 9 | Four ways to be wrong | Statistical-conclusion, internal, construct and external validity; who gets studied; designs for when you cannot shuffle |
| 10 | The subject is a person | Deception; Milgram; Tuskegee; the Belmont principles; the rules for this series' own experiments |
| 11 | A design is a program | The laboratory as code; Hans as four numbers against Pfungst's counts; the map |
| 12 | The Ledger | One row in full (the bright rats); today's five rows |
| 13 | In practice: who is blind? | A/B tests, clinical trials, user studies; five questions for any study |
| 14 | Frontier: when the blind cannot be kept | A double-blind trial whose participants could tell; the balanced placebo design and its price; three open questions; the research problem |
| | Recap, problems, and the road ahead | Ten lines; Kant's scoreboard; payoffs; problems; references; Part 3 |

## Sources

**Books.** O. Pfungst, *Clever Hans (The Horse of Mr. von Osten)* (1907; transl. C. L. Rahn, 1911; in the public
domain). R. Rosenthal, *Experimenter Effects in Behavioral Research* (1966). D. T. Campbell and J. C. Stanley,
*Experimental and Quasi-Experimental Designs for Research* (1963). W. R. Shadish, T. D. Cook and D. T. Campbell,
*Experimental and Quasi-Experimental Designs for Generalized Causal Inference* (2002). R. A. Fisher, *The Design of
Experiments* (1935). *The Belmont Report* (1979).

**Papers.**
- C. S. Peirce and J. Jastrow, "On small differences in sensation", *Memoirs of the National Academy of Sciences* 3
  (1885) 73–83 (read 1884).
- R. Rosenthal and K. L. Fode, "The effect of experimenter bias on the performance of the albino rat", *Behavioral
  Science* 8 (1963) 183–189.
- R. Rosenthal, "On the social psychology of the psychological experiment", *American Scientist* 51 (1963) 268–283.
- R. Rosenthal and L. Jacobson, *Pygmalion in the Classroom* (1968).
- S. W. Raudenbush, "Magnitude of teacher expectancy effects on pupil IQ as a function of the credibility of
  expectancy induction", *Journal of Educational Psychology* 76 (1984) 85–97.
- M. T. Orne, "On the social psychology of the psychological experiment", *American Psychologist* 17 (1962)
  776–783.
- J. de Quidt, J. Haushofer and C. Roth, "Measuring and bounding experimenter demand", *American Economic Review*
  108 (2018) 3266–3302.
- L. Lit, J. B. Schweitzer and A. M. Oberbauer, "Handler beliefs affect scent detection dog outcomes", *Animal
  Cognition* 14 (2011) 387–394.
- S. Milgram, "Behavioral study of obedience", *Journal of Abnormal and Social Psychology* 67 (1963) 371–378.
- W. A. Wagenaar, "Generation of random sequences by human subjects", *Psychological Bulletin* 77 (1972) 65–72;
  R. Falk and C. Konold, "Making sense of randomness", *Psychological Review* 104 (1997) 301–318.
- J. J. Arnett, "The neglected 95%", *American Psychologist* 63 (2008) 602–614; J. Henrich, S. J. Heine and
  A. Norenzayan, "The weirdest people in the world?", *Behavioral and Brain Sciences* 33 (2010) 61–83.
- J. M. Mitchell et al., "MDMA-assisted therapy for severe PTSD: a randomized, double-blind, placebo-controlled
  phase 3 study", *Nature Medicine* 27 (2021) 1025–1033.

## Problems and solutions

**1.** *Pfungst ran 42 tests in which the questioner knew the number on the card and 49 in which he did not; Hans
was right in 98% and 8%. How many answers is that in each? If Hans stopped at a number from 1 to 12 chosen
blindly, what share would he get right?*

0.98 × 42 ≈ 41 right of 42, and 0.08 × 49 ≈ 4 right of 49. A blind stop at one of twelve counts is right one time
in twelve, 8.3%. So without a questioner who knew the answer Hans did no better than a horse that stops at random,
which is what Pfungst concluded: "the few exceptional cases must be regarded as fortuitous".

**2.** *A supplement is tested on 60 volunteers: their memory score rises 4 points over eight weeks. Name four
threats to the conclusion that the supplement works, and the change of design that removes each.*

Any four of these. *Testing*: the second sitting of a memory test is easier than the first; a control group that
takes the same two tests removes it. *History*: something else changed over the eight weeks (term ended, the
season changed); a concurrent control group lives through the same weeks. *Regression*: people volunteer for a
memory supplement when their memory seems worst, and an unusually bad stretch is followed by a more ordinary one;
a control group recruited the same way regresses equally. *Expectancy*: they know they are taking it and expect to
improve; give the control group a placebo and keep both groups, and the testers, blind. *Selection*: volunteers
are not the general population, and if they are compared with non-volunteers the groups differed from the start;
assign volunteers to supplement or placebo by shuffle. *Attrition*: if those who felt no benefit stopped coming,
the finishers flatter the supplement; analyse everyone as randomized. One design answers all of them: a
randomized, placebo-controlled, double-blind trial.

**3.** *n people are dealt at random into two equal groups. A trait has standard deviation σ. Show that the
difference between the group means has standard deviation 2σ/√n, and find n for which it is σ/20.*

Each group mean is an average of n/2 values, so its variance is σ²/(n/2) = 2σ²/n. Treating the two groups as
independent draws, the variances add: Var = 4σ²/n, and the standard deviation is 2σ/√n. (Dealing from one finite
group makes the two means slightly negatively related; the exact result for the sample at hand is the same
expression with the sample's own σ.) For σ/20 we need √n = 40, so n = 1,600. With 200 people the figure is 0.14σ,
which is the spread the film shows for a trait nobody measured.

**4.** *An effect of 8 ms; people differ with SD 24 ms; a person's two sessions correlate 0.89. For 80% power at
the 5% level (z₀.₉₇₅ + z₀.₈₀ = 2.80), how many people does a two-group design need, and a within-person one? Why
does a simulation ask for a few more than the second number?*

d = 8/24 = 1/3. Two groups: n per group = 2(2.80/d)² = 2 × 70.6 ≈ 142, so 284 people. Within-person: the
difference of a person's two scores has variance 2σ²(1 − ρ), so n = 2(1 − ρ)(2.80/d)² = 0.22 × 70.6 ≈ 16 people
in all. The formula uses the normal curve, as if σ were known. With 16 people the standard deviation is estimated
on 15 degrees of freedom and the test is a t test, whose 5% critical value is 2.13 and not 1.96; on the Pool the
count that reaches 80% is about 19. (The film's 139 and 15 use the Pool's own values, 23.8 ms and 0.892.)

**5.** *Cell means: quick people 200 ms without the game and 180 with it; slow people 240 and 216. Compute the
interaction contrast in milliseconds and in log milliseconds. What would you report?*

In milliseconds the game's effect is −20 for the quick and −24 for the slow: an interaction of −4 ms. In logs,
ln(180/200) = ln(216/240) = ln 0.9 = −0.105 for both: an interaction of zero. Report the simple fact that produces
both: the game cuts reaction time by a tenth for everyone. "The game helps slow people more" is true in
milliseconds and says nothing about the game treating slow people differently. An interaction whose lines cross
would have survived the change of scale; one whose lines only fan need not.

**6.** *With `explainer.psychology.lab`: run the `regression` design with screening tests of 5, 20 and 80 trials
(`Lab(pool, n_trials=...)`). How does the spurious effect change, and why?*

```python
from explainer.psychology import lab
from explainer.psychology.pool import Pool
pool = Pool()
for k in (5, 20, 80):
    print(k, lab.Lab(pool, n_trials=k).replicate("regression", 100, n=200).mean())
```

About −8.0, −3.9 and −2.8 ms. A longer test averages away more of the trial-to-trial noise, so a score is less
luck and more person (its retest correlation in the Pool rises from 0.82 to 0.91 to 0.93), and the slowest at
screening are more nearly the truly slowest. The effect does not go to zero, because a person's mean also wobbles
from day to day, and no number of trials on one day removes that. Regression to the mean is as large as the
measure is unreliable, which is one reason Part 3 is about reliability.

**7.** ★ *A trial's participants can tell which arm they are in. Design a study, acceptable to an ethics board,
that separates the treatment's effect from the effect of knowing.*

There is no settled answer. Things a good one weighs: (a) the balanced placebo design crosses what is given with
what is said and identifies both effects and their interaction, but half the participants are told something false
about what is in their bodies, which a board will rarely allow for an active drug; an *authorized* version tells
everyone in advance that the label may be wrong. (b) An active placebo with noticeable effects of its own keeps
more people guessing, but changes the comparison. (c) Several doses: belief should not track dose once people know
they have had the drug, so a dose-response relation among the unblinded is evidence for the drug. (d) Measure the
guesses and the expectations of everyone before the outcome, and estimate how much of the difference they carry;
this needs the assumption that guesses are not themselves caused by early improvement, which is usually false, and
is the hard part. (e) Outcomes rated by assessors who never meet the treatment sessions remove the rater's
expectancy, not the participant's. A complete answer states its assumption and says what result would have shown
the assumption wrong.

## Where it comes back

What a measurement measures, and construct validity: Part 3. The randomization test, and the analyst as the last
unblinded observer: Part 4. The curve fitted to Hans's eyesight, as the psychometric function: Part 11. The dogs'
false alarms, as a criterion: Part 12. Milgram's study and its record: Part 34. Which findings travel beyond
Western samples: Part 38. Placebos and the trials of therapy: Part 42. One study in many laboratories: Part 43.
The laboratory (`lab.py`) is used by every later part that shows a design.

## Open checks

Before the narrated master:

* Read against the primary source: Milgram (1963), 26 of 40 continuing to 450 volts; the Tuskegee study's dates and
  the count of 399 men; the three principles of the Belmont Report. All three are confirmed here from secondary
  sources only.
* Arnett's figures on samples (68% from the United States, 96% from Western industrial countries) and the 12% of
  the world's population in Henrich, Heine and Norenzayan are from secondary sources; check the papers.
* Wagenaar (1972) and Falk and Konold (1997) on produced randomness are known here from summaries; the film's "six
  in ten" for the rate of switching should be checked against Falk and Konold's table.
* Chevreul's pendulum (1833), his observation that looking away stopped it, and Carpenter's "ideo-motor" (1852) are
  stated from standard histories.
* The Ledger row for the "bright" rats says we know of no independent direct replication. That is a statement
  about a search, made on 2026-11-13; search again before release.
