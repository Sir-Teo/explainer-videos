# Psychology, Built: Part 57, Health and Care

In 1991 volunteers rated their stress, took nose drops containing a cold virus and were quarantined; the more stress
they had reported, the more of them caught the cold, in a dose-response line. The first half of this part is the
evidence that psychological states change physical health and that sugar pills change pain. The second half is
logistics: most people with a treatable condition get no treatment, and the solutions are systems. The part opens
with the care card (education, not diagnosis or treatment, and where help is found).

The viewer predicts the result of an open-label placebo trial and four numbers. Then stress and illness, allostatic
load, status and childhood adversity, and the limits of the correlations; the powerful placebo reconsidered, placebo
analgesia and open-label placebo; expectation as a prior on bodily signals, nocebo and sham surgery; chronic pain
and its treatment; adherence; the health belief model, stages of change and the intention-behaviour gap with
their records, and COM-B; the Diabetes Prevention Program; CBT for insomnia in Part 10's model;
mindfulness's clinical evidence and the school null; the treatment gap and three ways to run a service, simulated;
England's national programme; measurement-based care; the Friendship Bench and digital therapeutics; and Type A and
a mindset study.

## Where the numbers come from

| What | Source |
|---|---|
| Pain as inference: stimulus 6, expectation 6 or 4 (placebo), sensory SD 1, prior SD 1.5; felt pain 6.0 and 5.4 (weight on expectation 0.31); the placebo effect 0.2, 0.6, 1.0, 1.3, 1.6 points as the sensory SD goes from 0.5 to 3 (illustrative precisions) | Psyche (`work.placebo_pain`, `placebo_by_noise`), item `placebo` |
| A service: 100 referrals a week (30% severe); 70 guided self-help starts (6 weeks) and 30 therapy starts (12 weeks) a week; recovery 45% after self-help (halved if severe) and 55% after therapy; 1% a week naturally while waiting; two years simulated, outcomes for the first year's referrals. Therapy only: mean wait 47 weeks, 29% recovered within 26 weeks, 62% by the end; matched: 1 week, 49%, 49%; stepped: 14 weeks, 53%, 77%; stepped with 100 and 60 starts (enough for the six in ten who step up): under a week, 73%, 73% | Psyche (`work.stepped_care`), item `care` |
| The cold-study bars (about 27% to 47% across five stress levels) and the Diabetes Prevention Program's incidence (about 11.0, 7.8 and 4.8 per 100 person-years) | as reported, approximately |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/work.py` gains an expectation model of placebo analgesia and a stepped-care
  simulator with waiting lists and stepping up. Tested in `tests/psychology/test_work.py`.
* The Ledger gains seven rows.
* The course's interactive: predict the open-label placebo trial's result, then see it, and try the stepped-care
  service with your own capacities.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| People under more psychological stress are more likely to develop a cold after exposure to a cold virus. | Cohen, Tyrrell and Smith 1991 | replicated |
| Placebos reduce reported pain, partly through the brain's own opioids. | Levine, Gordon and Fields 1978 | replicated |
| Placebo treatments produce large improvements in clinical conditions generally, including objective outcomes. | Beecher 1955 | failed |
| Placebos given openly, with patients told they are inert, still improve symptoms. | Kaptchuk and colleagues 2010 | contested |
| An intensive lifestyle programme reduces the incidence of type 2 diabetes in people at high risk. | Tuomilehto and colleagues (Finnish Diabetes Prevention Study) 2001 | replicated |
| The Type A behaviour pattern (hurried, competitive, hostile) causes coronary heart disease. | Rosenman and colleagues (Western Collaborative Group Study) 1975 | failed |
| Telling hotel workers that their work counts as exercise improves their weight and blood pressure. | Crum and Langer 2007 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Cohen, Tyrrell and Smith;
Felitti and colleagues; Hrobjartsson and Gotzsche; the Diabetes Prevention Program; Goyal and colleagues; Kuyken
and colleagues; Clark; Lambert and colleagues; Chibanda and colleagues; Friedman and Rosenman.

## Build it

```bash
python -m videos.psychology.psych57.compute            # every number (seconds)
python tools/qa_scene.py psych57 Gap                   # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych57 -q l   # the whole part, silent preview
python tools/build.py psych57                          # 1080p30 with narration
python tools/qa_scene.py psych57 Placebo --lang zh     # the Chinese edition of one chapter
python tools/make.py psych57                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 57                    # the lab: placebo as inference, stepped care
python tools/check_ledger.py psych57                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's work module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Nose drops and stress | The care card; the cold studies; the question; objectives |
| 1 | On you: a pill with nothing in it, and four numbers | The open-label prediction; four predictions |
| 2 | Stress and illness | From a stress response to a life; what the correlations cannot say |
| 3 | Placebo | The powerful placebo reconsidered; placebo analgesia; open-label placebo |
| 4 | Expectation as a prior | Pain as inference; nocebo and sham |
| 5 | Chronic pain | Pain that stays; treating it |
| 6 | Behaviour is the treatment | Adherence; preventing diabetes |
| 7 | Sleep, treated | CBT for insomnia; why it works in Part 10's model |
| 8 | Mindfulness | The clinical evidence; mindfulness in schools |
| 9 | The treatment gap | Prevalence against capacity; three ways to run a service; a national programme that counts |
| 10 | Measurement-based care | Routine outcome monitoring; what it needs |
| 11 | Help at scale | The Friendship Bench; digital therapeutics |
| 12 | Personality and the heart | Type A; exercise by mindset |
| 13 | The Ledger | Seven rows; what they have in common |
| 14 | In practice: a stepped-care service, planned | Where this is a job; a worked capacity plan |
| 15 | Frontier: care in the moment | What is new; open problems |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; payoffs; problems; references; Part 58 |

## Sources

* S. Cohen, D. A. J. Tyrrell and A. P. Smith (1991); S. Cohen et al. (1998, 2012); B. S. McEwen, Protective and
  damaging effects of stress mediators, *New England Journal of Medicine* 338 (1998) 171-179; M. G. Marmot et al.,
  Health inequalities among British civil servants: the Whitehall II study, *Lancet* 337 (1991) 1387-1393; V. J.
  Felitti et al., Relationship of childhood abuse and household dysfunction to many of the leading causes of death in
  adults, *American Journal of Preventive Medicine* 14 (1998) 245-258.
* H. K. Beecher (1955); A. Hrobjartsson and P. C. Gotzsche (2001, 2010); J. D. Levine, N. C. Gordon and H. L. Fields
  (1978); F. Benedetti et al. (2005); T. J. Kaptchuk et al. (2010); C. Carvalho et al. (2016); M. von Wernsdorff et
  al. (2021).
* F. Wood et al., N-of-1 trial of a statin, placebo, or no treatment to assess side effects, *New England Journal of
  Medicine* 383 (2020) 2182-2184; J. B. Moseley et al., A controlled trial of arthroscopic surgery for osteoarthritis
  of the knee, *New England Journal of Medicine* 347 (2002) 81-88.
* J. W. S. Vlaeyen and S. J. Linton, Fear-avoidance and its consequences in chronic musculoskeletal pain, *Pain* 85
  (2000) 317-332; A. C. de C. Williams, E. Fisher, L. Hearn and C. Eccleston, Psychological therapies for the
  management of chronic pain (excluding headache) in adults, *Cochrane Database of Systematic Reviews* (2020)
  CD007407.
* World Health Organization, *Adherence to Long-Term Therapies* (2003); J. Tuomilehto et al. (2001); Diabetes
  Prevention Program Research Group (2002, 2009).
* A. A. Borbely, A two process model of sleep regulation, *Human Neurobiology* 1 (1982) 195-204; A. Qaseem et al.,
  Management of chronic insomnia disorder in adults, *Annals of Internal Medicine* 165 (2016) 125-133.
* W. Kuyken et al., Efficacy of mindfulness-based cognitive therapy in prevention of depressive relapse, *JAMA
  Psychiatry* 73 (2016) 565-574; M. Goyal et al., Meditation programs for psychological stress and well-being, *JAMA
  Internal Medicine* 174 (2014) 357-368; W. Kuyken et al., Effectiveness and cost-effectiveness of universal
  school-based mindfulness training compared with normal school provision (MYRIAD), *Evidence-Based Mental Health* 25
  (2022) 99-109.
* R. C. Kessler et al., the World Mental Health surveys; D. M. Clark, Realizing the mass public benefit of
  evidence-based psychological therapies: the IAPT program, *Annual Review of Clinical Psychology* 14 (2018) 159-183.
* M. J. Lambert, J. L. Whipple and M. Kleinstauber, Collecting and delivering progress feedback, *Psychotherapy* 55
  (2018) 520-537.
* D. Chibanda et al., Effect of a primary care-based psychological intervention on symptoms of common mental
  disorders in Zimbabwe, *JAMA* 316 (2016) 2618-2626; A. Baumel, F. Muench, S. Edan and J. M. Kane, Objective user
  engagement with mental health apps, *Journal of Medical Internet Research* 21 (2019) e14567; US Federal Trade
  Commission, the 2023 order against an online therapy provider.
* M. Friedman and R. H. Rosenman, Association of specific overt behavior pattern with blood and cardiovascular
  findings, *Journal of the American Medical Association* 169 (1959) 1286-1296; R. H. Rosenman et al. (1975); R. B.
  Shekelle et al. (1985); Y. Chida and A. Steptoe (2009); A. J. Crum and E. J. Langer (2007); A. J. Crum et al. (2011).

## Problems and solutions

1. **The placebo effect.** Placebo against no treatment: 40% and 30% improve. Placebo against baseline: 40%. Which number is the placebo effect?

   *Solution.* Placebo against no treatment: 40% - 30% = 10 points. The 40% against baseline includes
   natural recovery and regression to the mean.
2. **Pain as inference.** Pain as inference: stimulus 7, expectation 5, sensory SD 1, prior SD 2. The felt intensity?

   *Solution.* The weight on expectation is (1/4)/(1/4 + 1) = 0.2; felt = 0.2 x 5 + 0.8 x 7 = 6.6.
3. **Cases prevented.** Diabetes: 11 cases per 100 person-years on placebo, 58% fewer on lifestyle. Cases prevented per 100 person-years?

   *Solution.* 11 x 0.58 = 6.4 cases per 100 person-years.
4. **Little's law.** A service gets 80 referrals a week; therapy lasts 10 weeks. How many therapy places must be open at once?

   *Solution.* Places in use = arrivals x duration = 80 x 10 = 800 at once (if everyone needs therapy).
5. **Adherence.** Adherence 50%; a drug halves risk in those who take it. The effect in everyone prescribed it?

   *Solution.* Half the people get half the risk: 0.5 x 1 + 0.5 x 0.5 = 0.75, a 25% reduction in everyone
   prescribed.
6. **Open-label placebo.** An open-label placebo trial: why can it not be blinded, and what outcome would persuade a sceptic?

   *Solution.* Patients know whether they take a pill, so self-reports can carry expectation and
   gratitude; an objective or observer-rated outcome that also improved, with an active comparison (an equally
   attentive no-pill condition), would persuade more.
7. ★ **An app's evaluation.** Plan an evaluation of a mental health app for a health system: trial, engagement, outcomes, and privacy.

   *Solution.* A randomized trial against usual care with a pre-registered outcome; engagement measured
   from logs (and the outcome analysed for everyone randomized); outcomes at follow-up; adverse events; and a
   privacy review of what data leave the device and to whom.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Cohen, Tyrrell and Smith's sample, quarantine and rates; McEwen's allostatic load; the Whitehall gradients; Felitti
et al.'s findings; Beecher's 35% and 15 trials; Hrobjartsson and Gotzsche (2001, 2010); Levine, Gordon and Fields
(1978); Benedetti et al. (2005); Kaptchuk et al.'s 80 patients, three weeks, 59% and 35%; Carvalho et al. (2016);
von Wernsdorff et al. (2021); the 2020 statin n-of-1 trial; Moseley et al. (2002); the fear-avoidance model and the
Cochrane review; the WHO's 50%; Tuomilehto et al. (2001); the Diabetes Prevention Program's 3,234 adults, goals, 58%
and 31% and the ten-year follow-up; Borbely (1982); the ACP guideline; Kuyken et al. (2016) on MBCT; Goyal et al.
(2014); MYRIAD's 8,000 students, 84 schools and results; the World Mental Health surveys' treatment rates; IAPT's
start, design and recovery rate; Lambert et al. (2018); Chibanda et al.'s trial and results; Baumel et al. on app
retention; the prescription-app company's bankruptcy; the FTC action; Friedman and Rosenman; the Western
Collaborative Group Study's 3,000 men and twofold risk; MRFIT; Chida and Steptoe (2009); tobacco-industry funding
of Type A research; Crum and Langer's 84 women and seven hotels; Jacobson and Truax (1991); and every page
range in Sources. The regression-to-the-mean simulation, the adherence arithmetic (a drug illustratively 30%
effective) and the reliable-change example (an illustrative scale with SD 5 and reliability 0.85) are worked
illustrations, not data.
