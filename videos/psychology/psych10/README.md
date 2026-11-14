# Psychology, Built: Part 10, Chemistry and Clocks

In the early summer of 1938 two men walked into Mammoth Cave in Kentucky and stayed for thirty-two days. Nathaniel
Kleitman, a physiologist of forty-three, and his student Bruce Richardson, who was twenty-five, lived there by a
day of twenty-eight hours, to find out whether the body's daily rhythm is a habit copied from the sun or
something the body keeps by itself. Richardson's temperature rhythm stretched toward the cave's schedule.
Kleitman's kept its twenty-four-hour course for the whole month. As an experiment on two people it settles
nothing, and it was still the first sign of a clock that took sixty more years to pin down.

This part is about the body the brain lives in, and why the same mind is so different at four in the afternoon
and at four in the morning. The route: the clock (its period, where it sits, and why a 28-hour day defeats it);
how light sets it, and what a flight across time zones does; sleep as the laboratory found it, with its stages,
cycles and dreams; the two processes that decide when sleep comes, and what they predict for a night without
sleep; the viewer's own chronotype; what two weeks of short sleep do to attention, and why the sleeper does not
notice; what sleep is for, where one answer has experiments behind it and the rest is argument; hormones, through
a stress loop that switches itself off; four ways a drug can change a synapse; dose and response, half-lives and
three coffees; and tolerance and withdrawal as one process seen at two times. The practice chapter covers school
start times, the treatment of insomnia and rosters; the frontier is the question of why animals sleep at all.

It closes Act II, *The Wet Machine*.

## Where the numbers come from

| What | Source |
|---|---|
| Mammoth Cave, 1938: 32 days on a 28-hour day; the student (25) adapted, Kleitman (43) did not and grew sleepy at about ten each evening | Kleitman (1939), from the 1938 magazine report, a National Park Service account and a book excerpt; registered in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md) |
| The clock's own period: 24.18 hours in 24 people, young and old, on a 28-hour day for about a month; earlier estimates near 25 hours came from self-selected light | Czeisler et al. (1999), from the abstract |
| 20 detailed dream reports from 27 awakenings during eye movements | Aserinsky and Kleitman (1953), from a reprint of the text |
| Sleep pressure rises with a time constant of 18.18 hours and falls with 4.2 | Borbély (1982); Daan, Beersma and Borbély (1984), from the figure legend of the model's 2016 reappraisal |
| 8, 6 or 4 hours in bed for 14 days, or none for 3; lapses rise with every hour awake beyond 15.84; six hours for two weeks matched up to two nights without sleep; sleepiness ratings levelled off | Van Dongen et al. (2003), from the abstract |
| 66 people on 3, 5, 7 or 9 hours in bed for a week (the Ledger's record) | Belenky et al. (2003), from the abstract |
| An odour present at learning and given again in slow-wave sleep improved memory for card locations; not in REM sleep, not awake, not without the odour at learning | Rasch et al. (2007), from the abstract |
| 91 experiments, 2,004 people: g = 0.29 (0.21 to 0.38) in non-REM sleep, none in REM sleep or waking | Hu et al. (2020), from the abstract |
| Activation-synthesis (1977), and the dissociation of dreaming from REM sleep (2000) | Hobson and McCarley (1977); Solms (2000), from summaries |
| 16 studies, 1.4 million people: short sleepers 12% more likely to die in the follow-up, long sleepers 30% | Cappuccio et al. (2010), from the abstract |
| Chronotype latest at about 19.5 (women) and 21 (men); social jetlag | Roenneberg et al. (2004); Wittmann et al. (2006) |
| Testosterone before birth and adult behaviour in guinea pigs: organizing against activating | Phoenix et al. (1959), from reviews |
| The Yerkes-Dodson experiment of 1908 and the later history of its "law" | Teigen (1994), from summaries |
| Opponent processes | Solomon and Corbit (1974), from summaries |
| One large dose of heroin (15 mg/kg): deaths of 32% in the usual room, 64% in another room, 96% with no history | Siegel et al. (1982), from the paper's table as quoted |
| Seattle: start moved 55 minutes, from 7:50 to 8:45; 34 minutes more sleep; grades 4.5% higher | Dunster et al. (2018), from the university's summary |
| Behavioural therapy for insomnia: 20 trials, 1,162 people; asleep 19 minutes sooner, 26 minutes less awake, +9.9 points of sleep efficiency | Trauer et al. (2015), from the abstract |
| In mice the space between brain cells widened by 60% in sleep (2013); clearance measured otherwise was lower in sleep (2024) | Xie et al. (2013); Miao et al. (2024), from the abstracts |

Everything else is computed by `compute.py` with Psyche's `body` module, and is a model's behaviour, tagged as
such on screen. The clock is a van der Pol oscillator driven by light, of the kind Kronauer's group fitted to
people, with its period set near the published one (it comes out at 24.15 hours); it was not fitted to anything
here. The two-process model uses the published time constants and thresholds chosen to give an ordinary night, so
its eight hours are a setting and its recovery sleep and second wind are predictions. The lapse curves draw the
published rule (lapses in proportion to hours awake beyond 15.84) on an arbitrary vertical scale. The stress loop,
the opponent process and the tolerance simulation are illustrations whose constants were chosen for shape; the
three death rates of the tolerance model were fitted to Siegel's three, and the film says so. Half-lives are five
hours for caffeine and about two for nicotine. Drawings that are not data (the cave's temperature curves, the
eye-movement trace, the four brain-wave traces, the typical night, the ratings that level off, the pattern of
individual differences) carry a note saying so.

Two things the models are *not* used for. In the clock model a flight east is made up faster than a flight west,
the opposite of what travellers usually report; the film shows this as a caution and takes only the timescale
from the model. And the alertness curve has no dip in the early afternoon, so the film claims none.

## Built in this part

* `explainer/psychology/psyche/body.py`: the clock (free running, entrained, a phase response curve, re-entrainment
  after a shift); the two-process model with forced waking, and an alertness curve from it; lapses under short
  sleep; a three-stage hormone loop with feedback; receptor occupancy with a competitive blocker and a Hill
  coefficient; first- and zero-order elimination and repeated dosing; an opponent process that strengthens with
  use; tolerance tied to a place; midsleep and social jetlag. Tested in `tests/psychology/test_body.py`.
* The Ledger gains four rows and the Archive sixteen datasets.
* The course gains its first interactive that measures the reader over time: a vigilance task set beside the
  reader's own rating of their alertness.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Sleep contains recurring periods of rapid eye movement, and people woken from them usually report a dream | Aserinsky and Kleitman 1953 | replicated |
| Too little sleep, night after night, impairs sustained attention, and the impairment accumulates | Van Dongen and colleagues 2003 | replicated |
| Reactivating a memory during slow-wave sleep strengthens it | Rasch and colleagues 2007 | replicated, smaller |
| Sleeping too little shortens your life | Cappuccio and colleagues 2010 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: the cave (an experiment on two
people, told as history), the clock's period (physiology), the two-process model (a model, tested against its own
predictions), the two accounts of dreaming (an open dispute, entered with consciousness in Part 27), chronotype
across life (a survey description; Part 31), the guinea pigs (animal physiology), the Yerkes-Dodson history (the
law is examined in Part 28), the opponent process (a theory; Part 41), Siegel's rats (conditioning is entered in
Part 16), the Seattle schools (a before-and-after comparison, described as that), the insomnia trials (therapies
are entered in Part 42), and the two mouse studies of clearance (a finding and its dispute).

## Build it

```bash
python -m videos.psychology.psych10.compute            # every number (about a minute), into .cache/psych10/
python tools/qa_scene.py psych10 TwoProcess            # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych10 -q l   # the whole part, silent preview
python tools/build.py psych10                          # 1080p30 with narration
python tools/qa_scene.py psych10 TwoProcess --lang zh  # the Chinese edition of one chapter
python tools/make.py psych10                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 10                    # the lab: a clock, a pressure, a brake and a dose
python tools/check_ledger.py psych10                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's body module, the Pool, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A month in a cave | The cave and its 28-hour day; two temperature rhythms; the brain lives in a body; objectives |
| 1 | A clock inside | 24.18 hours, and the model clock's drift; where the clock is and the loop inside each cell; locking to a day, and the days it cannot follow |
| 2 | Light sets the clock | The eye's third kind of light cell and melatonin; a phase response curve, computed; a flight across time zones |
| 3 | Sleep, found in the laboratory | The eyes of sleepers and 20 dreams in 27 awakenings; four stages; the architecture of a night |
| 4 | Two processes | The pressure and its two time constants; the clock's gate; a night without sleep and the recovery; the second wind |
| 5 | On you: your chronotype | Four numbers; the middle of sleep; three sleepers and their social jetlag |
| 6 | What sleep loss does | Sleep assigned by lot; two weeks of lapses; ratings that level off |
| 7 | What sleep is for | Roses in deep sleep and four controls; 91 experiments; two accounts of dreaming |
| 8 | The stress loop | A synapse against a hormone; three glands and a brake; a stressor with the brake whole and worn; organizing and activating, and the Yerkes-Dodson curve |
| 9 | Four ways to change a synapse | Mimic, block, hold, amplify; caffeine and the pressure gauge; where a drug starts is not where it ends |
| 10 | Dose and response | Occupancy from mass action; a blocker and a steeper curve; half-lives and alcohol's constant rate; three coffees |
| 11 | Tolerance and withdrawal | The opponent process; ten doses; the same dose in a different room |
| 12 | The Ledger | REM sleep, sleep loss and attention, sleep and memory, short sleep and death |
| 13 | In practice: schedules, schools and insomnia | Seattle's school start; a treatment built from the two processes; rosters, clinics and drug trials |
| 14 | Frontier: why do we sleep? | Four proposals; does sleep wash the brain; open questions |
| | Recap, problems, and the road ahead | Ten lines; what today adds to the reply to Kant; payoffs; problems; references; Part 11 |

## Sources

**Books.** N. Kleitman, *Sleep and Wakefulness* (revised ed., 1963). K. Miller, *Mapping the Darkness* (2023).
T. Roenneberg, *Internal Time* (2012). J. S. Meyer and L. F. Quenzer, *Psychopharmacology: Drugs, the Brain, and
Behavior* (2nd ed., 2013).

**Papers.**
- N. Kleitman, *Sleep and Wakefulness* (1939), for the cave; "Science: Cave Men", *Time*, 18 July 1938.
- C. A. Czeisler et al., "Stability, precision, and near-24-hour period of the human circadian pacemaker",
  *Science* 284 (1999) 2177–2181.
- E. Aserinsky and N. Kleitman, "Regularly occurring periods of eye motility, and concomitant phenomena, during
  sleep", *Science* 118 (1953) 273–274.
- W. Dement and N. Kleitman, "Cyclic variations in EEG during sleep and their relation to eye movements, body
  motility, and dreaming", *Electroencephalography and Clinical Neurophysiology* 9 (1957) 673–690.
- A. A. Borbély, "A two process model of sleep regulation", *Human Neurobiology* 1 (1982) 195–204; S. Daan, D. G.
  M. Beersma and A. A. Borbély, "Timing of human sleep: recovery process gated by a circadian pacemaker",
  *American Journal of Physiology* 246 (1984) R161–R178; A. A. Borbély, S. Daan, A. Wirz-Justice and T. Deboer,
  "The two-process model of sleep regulation: a reappraisal", *Journal of Sleep Research* 25 (2016) 131–143.
- H. P. A. Van Dongen, G. Maislin, J. M. Mullington and D. F. Dinges, "The cumulative cost of additional
  wakefulness", *Sleep* 26 (2003) 117–126.
- G. Belenky et al., "Patterns of performance degradation and restoration during sleep restriction and subsequent
  recovery", *Journal of Sleep Research* 12 (2003) 1–12.
- T. Roenneberg et al., "A marker for the end of adolescence", *Current Biology* 14 (2004) R1038–R1039; M.
  Wittmann, J. Dinich, M. Merrow and T. Roenneberg, "Social jetlag: misalignment of biological and social time",
  *Chronobiology International* 23 (2006) 497–509.
- B. Rasch, C. Büchel, S. Gais and J. Born, "Odor cues during slow-wave sleep prompt declarative memory
  consolidation", *Science* 315 (2007) 1426–1429.
- X. Hu, L. Y. Cheng, M. H. Chiu and K. A. Paller, "Promoting memory consolidation during sleep: a meta-analysis
  of targeted memory reactivation", *Psychological Bulletin* 146 (2020) 218–244.
- J. A. Hobson and R. W. McCarley, "The brain as a dream state generator", *American Journal of Psychiatry* 134
  (1977) 1335–1348; M. Solms, "Dreaming and REM sleep are controlled by different brain mechanisms", *Behavioral
  and Brain Sciences* 23 (2000) 843–850.
- F. P. Cappuccio, L. D'Elia, P. Strazzullo and M. A. Miller, "Sleep duration and all-cause mortality", *Sleep* 33
  (2010) 585–592.
- C. H. Phoenix, R. W. Goy, A. A. Gerall and W. C. Young, "Organizing action of prenatally administered
  testosterone propionate on the tissues mediating mating behavior in the female guinea pig", *Endocrinology* 65
  (1959) 369–382.
- R. M. Yerkes and J. D. Dodson, "The relation of strength of stimulus to rapidity of habit-formation", *Journal
  of Comparative Neurology and Psychology* 18 (1908) 459–482; K. H. Teigen, "Yerkes-Dodson: a law for all
  seasons", *Theory & Psychology* 4 (1994) 525–547.
- R. L. Solomon and J. D. Corbit, "An opponent-process theory of motivation: I. Temporal dynamics of affect",
  *Psychological Review* 81 (1974) 119–145.
- S. Siegel, R. E. Hinson, M. D. Krank and J. McCully, "Heroin 'overdose' death: contribution of drug-associated
  environmental cues", *Science* 216 (1982) 436–437.
- G. P. Dunster et al., "Sleepmore in Seattle", *Science Advances* 4 (2018) eaau6200.
- J. M. Trauer et al., "Cognitive behavioral therapy for chronic insomnia: a systematic review and
  meta-analysis", *Annals of Internal Medicine* 163 (2015) 191–204.
- L. Xie et al., "Sleep drives metabolite clearance from the adult brain", *Science* 342 (2013) 373–377; A. Miao
  et al., "Brain clearance is reduced during sleep and anesthesia", *Nature Neuroscience* 27 (2024) 1046–1050.

## Problems and solutions

**1.** *A clock left in the dark has a period of 24.18 hours. How many minutes a day does it drift, and which
way? After how many days is it twelve hours out? What must morning light do each day to hold it at 24 hours?*

It runs 0.18 hours long, so each day its low point comes 0.18 × 60 = 10.8 minutes later by the wall clock. It is
twelve hours out after 12 / 0.18 ≈ 67 days: a person kept in constant dim light for two months would be sleeping
through the day. To hold it at 24 hours, light has to advance it by those eleven minutes every day, and advances
come from light after the low point, that is, in the morning. This is why the loss of morning light (a dark
winter commute, a curtained room) lets a clock slide later.

**2.** *In the two-process model the pressure rises as 1 − (1 − S₀)e^(−t/18.18) and falls as S₀e^(−t/4.2) (t in
hours). From S = 0.17 on waking, find S after 16 hours and after 40 hours awake. From each, how long must sleep
last to return to 0.17? Why is recovery sleep not proportional to the time awake?*

After 16 hours: 1 − 0.83 e^(−0.880) = 1 − 0.83 × 0.415 = 0.656. After 40 hours: 1 − 0.83 e^(−2.200) = 1 − 0.83 ×
0.111 = 0.908. Falling back to 0.17 takes t = 4.2 ln(S / 0.17): 4.2 ln 3.86 = 5.7 hours from 0.656, and 4.2 ln
5.34 = 7.0 hours from 0.908. Twenty-four more hours awake cost 1.4 more hours of sleep. Two things flatten the
relation. The pressure saturates: it approaches a ceiling, so the second day awake adds less than the first. And
it decays exponentially, so the time to pay it off grows only with the logarithm of its height. (The film's
figures, 8.1 and 8.6 hours, differ from these because there the waking threshold moves with the clock.)

**3.** *Lapses grow each day by 0.15 for every hour awake beyond 15.84. Compare fourteen days on 6 hours in bed
with fourteen days on 7. How much sleep keeps the count level?*

On 6 hours a person is awake 18, which is 2.16 over the line: 0.324 lapses more each day, 4.5 more after fourteen
days. On 7 hours, 17 awake and 1.16 over: 0.174 a day, 2.4 after fourteen. One hour less sleep nearly doubles the
deficit (2.16 / 1.16 = 1.86), because what counts is the excess over about sixteen hours and not the total. The
count stays level at 24 − 15.84 = 8.16 hours of sleep.

**4.** *A drug has K = 2 mg/L. What concentration occupies 80% of its receptors? With a blocker present at four
times its own K_B, what concentration gives the same 80%? With three sites that must all be filled, p = D³/(D³ +
K³): what is the ratio of the doses that give 90% and 10%?*

D / (D + 2) = 0.8 gives D = 8 mg/L, four times K. The blocker multiplies K by 1 + 4 = 5, so K behaves as 10 mg/L
and the dose for 80% is 40 mg/L: five times as much, for any target occupancy. With three sites, p = 0.9 needs
D³ = 9K³ and p = 0.1 needs D³ = K³/9, so the ratio of doses is 81^(1/3) = 4.3, against 81 for one site. The
margin between "barely works" and "nearly everything" is some twenty times narrower.

**5.** *Caffeine's half-life is 5 hours. You take 100 mg at 8:00 and 100 mg at 14:00 (absorbed at once). How
much is left at 23:00? When would a single 200 mg dose have to be taken to leave the same? Alcohol leaves at a
constant rate r: what doubles when the dose doubles?*

The morning dose has had 15 hours, three half-lives: 12.5 mg. The afternoon dose has had 9 hours, 1.8 half-lives:
100 × 2^(−1.8) = 28.7 mg. Together 41.2 mg, of which the later cup supplies 70%. A single 200 mg leaves 41.2 mg
after 5 log₂(200 / 41.2) = 11.4 hours, so it would have to be taken at about 11:35. For alcohol the time to
clear a dose is dose / r, so doubling the dose doubles the time. For a drug with a half-life, doubling the dose
adds one half-life and no more.

**6.** *With `explainer.psychology.psyche.body`: use `entrain` to find the day lengths the clock locks to at 300
lux and at 3,000 lux. Then use `two_process` with `keep_awake` to plot recovery sleep against hours awake.*

At 300 lux the clock locks to days of 23, 24 and 25 hours; at 3,000 lux to days from 21 to 27, and still not to
28. Brighter light pushes harder, so it can make up a larger daily difference; a cave lit like an office could
not have held anyone to a 28-hour day by light alone. Keeping the model awake for 16, 28, 40, 52 and 64 hours
from a 7:00 waking gives recovery sleeps of 8.0, 4.7, 8.6, 5.6 and 8.7 hours. It does not grow in proportion
(problem 2), and it zigzags: after 28 or 52 hours the model goes to bed at eleven in the morning, and the clock's
rising threshold wakes it within five hours although the pressure is far from paid off. That is the night
worker's short daytime sleep.

**7.** ★ *Short sleepers die sooner, and so do long sleepers. Design the study that could tell sleep as a cause
from sleep as a symptom, and say what result would count against a causal effect.*

A sketch. No one can assign decades of short sleep, so combine designs with different weak points, as in Part 9.
(a) A cohort with sleep measured by a wrist monitor and not by self-report, with illness recorded at entry, and
the analysis repeated after dropping deaths in the first five or ten years: if short sleep is a symptom of
disease already under way, the association should weaken as those deaths are removed. (b) Mendel's lottery: gene
variants that shift habitual sleep by a few minutes are assigned at conception and cannot be caused by later
illness, so compare lifespans across them (and within families, to remove stratification). (c) Randomized trials
that extend the sleep of habitual short sleepers for months and measure intermediate outcomes such as blood
pressure and glucose control. Fix beforehand the outcomes and the size of effect that would matter. Against a
causal effect: an association that vanishes once early deaths are excluded, no gradient across the genetic
variants, and no change in the intermediate outcomes when sleep is extended. The long sleepers are the control
that keeps everyone honest: nobody proposes that an extra hour in bed kills, so whatever explains their excess
(undiagnosed illness, most plausibly) is a candidate explanation for the short sleepers' too.

## Where it comes back

The retina and the cells that see without pictures: Part 13. Conditioning, and the room that switches on
tolerance: Part 16. Reward, dopamine and what drugs take over: Part 17. What it means to consolidate a memory:
Part 20. Dreaming and consciousness: Part 27. Motivation, arousal, the Yerkes-Dodson curve and the opponent
process: Part 28. Adolescence and the late clock: Part 31. Depression, the stress loop and addiction: Parts 40
and 41. Whether drugs and therapies work: Part 42. Psyche's `body` module supplies the clock, the sleep pressure
and the dose-response curves those parts use.

## Open checks

Before the narrated master:

* Kleitman's cave: no primary source was read. The dates within 1938 ("early summer"; the magazine report is
  dated 18 July), "one of very few scientists anywhere who studied sleep" and "the newspapers suggested age" rest
  on the magazine report and a book excerpt found by search. Sources differ on the cave's depth, which is not
  given. The temperature curves on screen are a drawing of the reported pattern.
* The clock model's form and constants are from memory of Kronauer's light-driven van der Pol models; they were
  chosen so that the free period, the entrained phase and the phase response curve have the published shapes, and
  were not checked against the papers. "An oscillator of a kind engineers have used for a century" refers to van
  der Pol's work of the 1920s.
* The suprachiasmatic nucleus: "about twenty thousand neurons" is twice the per-side figure of about ten
  thousand given for rodents in a review; the lesion studies (1972) and the hamster transplants (1990) were
  confirmed from reviews, and their authors are not named in the film. That each cell keeps time by a loop of
  genes whose proteins switch them off is the textbook account (the work honoured in 2017).
* The light-sensitive ganglion cells were established in 2002; the film says "around the year 2000". "Experiments
  on people give a curve of this shape" refers to human phase response curves (Khalsa et al. 2003), from memory.
  "Most travellers report the opposite" (west easier than east) is the usual statement in reviews, from memory.
* Aserinsky: "graduate student", the pen recorders and "two pages" are from histories; the paper's count for
  awakenings during ocular quiet (19 of 23 with no recall, from memory) is not given. The number of sleepers
  differs between sources and is not given. "Before it, sleep was thought of as the brain idling" is a summary.
* The stages: "about half the night" in light sleep, cycles of "about ninety minutes", "four or five in a night"
  and the paralysis of the body's muscles in REM sleep are textbook figures. The traces and the typical night are
  drawings.
* The two-process model: the thresholds (0.67 and 0.17, moved by 0.12 of a skewed daily wave) follow Daan et al.
  (1984) from memory and are described in the film as set to make an ordinary night come out right. Adenosine as
  "one ingredient" of sleep pressure is from memory of the animal work of the 1990s. "After a lost night people
  sleep somewhat longer, and much more deeply" is the textbook summary of recovery sleep.
* "The stretch that people who study accidents on the night shift worry about most" is a general statement; no
  accident statistics are shown.
* Van Dongen et al. (2003): the sample size was not confirmed and is not given. "Philadelphia", the ten-minute
  task and the definition of a lapse as a response slower than half a second (used in the course interactive)
  are from memory of the psychomotor vigilance task. Belenky et al. (2003) found that the 5- and 7-hour groups
  levelled off at a reduced level while the 3-hour group kept declining; the Ledger's record line says so.
* Rasch et al. (2007): "in Germany" and the hippocampal replay "idea" (recordings in rats in the 1990s) are from
  memory; the paper's sample sizes and percentages are not given. The year-by-year decline for sounds timed to
  slow waves was found by search (a 2023 analysis) and is not in the Archive.
* Hobson "revised his theory" (the later AIM model) is from memory.
* Hormones: cortisol's actions and the anatomy are textbook. In people cortisol is lowest around midnight; the
  model's lowest point is earlier (19:44), and the film says "lowest in the evening". "A weakened brake in this
  loop is one of the oldest biological findings in severe depression" refers to dexamethasone non-suppression,
  from memory; it is examined in Part 40. "A team in Kansas" for Phoenix et al. is from memory.
* The drugs' sites of action (nicotine, morphine, caffeine, naloxone, the serotonin reuptake inhibitors, cocaine,
  alcohol and the benzodiazepines) are textbook pharmacology and were not checked against a current text. That an
  overdose can return when naloxone clears first is standard clinical teaching, from memory. "For depression
  that simple story has not held up well" refers to reviews of the serotonin hypothesis, from memory, and is
  deferred to Parts 40 and 42.
* Half-lives: about five hours for caffeine and two for nicotine were found by search in secondary sources; that
  caffeine's differs severalfold with genes, pregnancy and smoking is from memory. No number is given for
  alcohol's rate.
* Solomon and Corbit's theory is described from secondary sources. "Some overdoses are the usual dose in an
  unusual place" is Siegel's proposal; his interviews with overdose survivors were not checked.
* Seattle: the year of the change is not stated in the film; the grades figure is the median in the classes
  studied, as the university's summary gives it.
* "The treatment that guidelines put first" (behavioural therapy before drugs for chronic insomnia) is from
  memory of the American College of Physicians' 2016 guideline. That transport and military organizations use
  descendants of the two-process model for rosters is from memory of the fatigue-modelling literature.
* The frontier: sleep-like states in flies, worms and jellyfish (the jellyfish study of 2017 was confirmed by
  search); the synaptic downscaling proposal is described from memory; the stability of individual differences
  in vulnerability to sleep loss was confirmed from a review, and the picture of it is a drawing; "some drugs
  suppress REM sleep for years" (many antidepressants) is from memory.
* Fechner's insight "on the morning of 22 October 1850, lying in bed" is the traditional account, confirmed from
  histories; Part 11 should give it as his own later telling.
