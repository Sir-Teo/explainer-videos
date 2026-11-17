# Psychology, Built: Part 54, The Science of Learning

In 1984 Benjamin Bloom reported that pupils tutored one to one scored about two standard deviations above pupils
taught in a class, and challenged education to find group methods as good. Forty years on the two sigma has shrunk
to under one, still among the largest effects in education, and the study methods with the strongest evidence are
ones students rate as less effective than rereading. This part turns Parts 20 and 21's memory research into an
engineering problem, and asks why learners choose the opposite of what works.

The viewer is offered two word lists, one massed and one spaced, and predicts four numbers. Then the testing effect
in the laboratory and the classroom; the spacing ridgeline as a design rule and interleaving; learning against
performance, with Psyche cramming and spacing; Dunlosky and colleagues' ten techniques; cognitive load and worked
examples; learning styles and other myths; tutoring measured again and how tutoring systems model a learner; four
review schedules raced on Psyche; the simple view of reading and the end of the reading wars; growth-mindset lessons
at national scale; and feedback that makes things worse.

## Where the numbers come from

| What | Source |
|---|---|
| Review schedules: 60 items studied on day 0, four reviews each before day 28, a test on day 60; Part 21's Pavlik-Anderson activation with each trace's decay capped at 1 (uncapped, presentations minutes apart overflow), items 0.6 harder than Part 21's default with SD 0.25; recall 17% massed, 67% expanding (gaps doubling), 71% equal, 71% for the schedule the model chooses (the best of fifteen with growing, equal or shrinking gaps) | Psyche (`work.schedule`, `pa_activation_capped`), item `policies` |
| Reviews per item: massed 15% to 25% for one to eight reviews; spaced over 28 days 41% to 76% | Psyche, item `budget` |
| Recall over 60 days for one item: crammed 92% on day 5 and 14% on day 60; spaced 32% on day 5 (a review due) and 74% on day 60 | Psyche, item `curves` |
| The spacing ridgeline: best gaps 2, 21, 35 and 90 days for tests 7, 35, 70 and 350 days later | Part 21's `memory.spacing_ridge`, item `ridge` |
| The simple view of reading: 400 simulated children, decoding and language comprehension each Beta(4, 2), comprehension their product plus noise; good listeners who cannot decode 0.29, good decoders who do not understand 0.28, both good 0.59 | Psyche (`work.simple_view`), item `reading` |
| The bars for Roediger and Karpicke (81% and 75% at five minutes, 42% and 56% at a week), tutoring (2.0, 0.79, 0.76, 0.37 SD) and mindset (0.08 and about 0.1) | the studies as reported; the bar for "early small studies" of mindset is illustrative |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/work.py` gains a capped Pavlik-Anderson activation, a review scheduler comparing
  massed, expanding, equal and model-chosen schedules at equal study, and the simple view of reading. Tested in
  `tests/psychology/test_work.py`.
* The Ledger gains five rows; testing and spacing are Part 21's rows.
* The course's interactive: two lists of word pairs, one studied massed and one spaced, with the reader's prediction
  and then the test.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Mixing problem types during practice improves later performance compared with practising each type in a block, though blocked practice looks better during learning. | Rohrer and Taylor 2007 | replicated |
| Teaching matched to a learner's preferred style (visual, auditory, kinaesthetic) improves learning. | Dunn and Dunn 1978 | failed |
| One-to-one tutoring raises achievement by about two standard deviations over conventional classroom teaching. | Bloom 1984 | replicated, smaller |
| Teaching students that ability can grow improves their academic achievement. | Blackwell, Trzesniewski and Dweck 2007 | replicated, smaller |
| Students who take notes by hand learn more from a lecture than those who type them. | Mueller and Oppenheimer 2014 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Bloom; VanLehn; VanLehn with
Nickow and colleagues; Roediger and Karpicke; Deslauriers and colleagues; Dunlosky and colleagues; Sweller; Settles
and Meeder; Castles, Rastle and Nation; Kluger and DeNisi.

## Build it

```bash
python -m videos.psychology.psych54.compute            # every number (a minute)
python tools/qa_scene.py psych54 Scheduler             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych54 -q l   # the whole part, silent preview
python tools/build.py psych54                          # 1080p30 with narration
python tools/qa_scene.py psych54 Bjork --lang zh       # the Chinese edition of one chapter
python tools/make.py psych54                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 54                    # the lab: schedules, budgets and the simple view
python tools/check_ledger.py psych54                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's work module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Two sigma | Bloom's challenge; forty years on; the question; objectives |
| 1 | On you: two lists, and four numbers | Massed and spaced lists; four predictions |
| 2 | Retrieval practice | Study or test; in classrooms |
| 3 | Spacing and interleaving | The ridgeline as a design rule; interleaving |
| 4 | Learning against performance | Cramming wins the week and loses the term; the illusion of fluency |
| 5 | Ten techniques, ranked | Dunlosky et al.'s ratings; why the top two work |
| 6 | Cognitive load | Sweller's theory; worked examples and the expertise reversal |
| 7 | Myths | The learning-styles test; other myths, tested |
| 8 | Tutoring | Two sigma measured again; how a tutoring system models the learner |
| 9 | Scheduling reviews | From boxes to models; four schedules raced; more reviews or better-placed ones |
| 10 | Learning to read | The simple view of reading; the reading wars |
| 11 | Beliefs about ability | Growth mindset at scale; for whom and where |
| 12 | Feedback | A third of the time, worse; feedback that works |
| 13 | The Ledger | Five rows; what they have in common |
| 14 | In practice: a course's study plan, redesigned | Where this is a job; a worked redesign |
| 15 | Frontier: AI tutors and what transfers | What is new; open problems |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; payoffs; problems; references; Part 55 |

## Sources

* B. S. Bloom (1984); K. VanLehn (2011); A. Nickow, P. Oreopoulos and V. Quan (2020).
* H. L. Roediger and J. D. Karpicke, Test-enhanced learning, *Psychological Science* 17 (2006) 249-255; N. J.
  Cepeda, E. Vul, D. Rohrer, J. T. Wixted and H. Pashler, Spacing effects in learning: a temporal ridgeline of optimal
  retention, *Psychological Science* 19 (2008) 1095-1102; J. D. Karpicke and H. L. Roediger, Expanding retrieval
  practice promotes short-term retention, but equally spaced retrieval enhances long-term retention, *Journal of
  Experimental Psychology: Learning, Memory, and Cognition* 33 (2007) 704-719.
* D. Rohrer and K. Taylor (2007); D. Rohrer et al. (2020); M. Brunmair and T. Richter (2019).
* E. L. Bjork and R. A. Bjork, Making things hard on yourself, but in a good way, in *Psychology and the Real World*
  (Worth, 2011) 56-64; N. Kornell and R. A. Bjork, Learning concepts and categories: is spacing the "enemy of
  induction"?, *Psychological Science* 19 (2008) 585-592; L. Deslauriers, L. S. McCarty, K. Miller, K. Callaghan and
  G. Kestin, Measuring actual learning versus feeling of learning in response to being actively engaged in the
  classroom, *Proceedings of the National Academy of Sciences* 116 (2019) 19251-19257; S. Freeman et al., Active
  learning increases student performance in science, engineering, and mathematics, *Proceedings of the National
  Academy of Sciences* 111 (2014) 8410-8415.
* J. Dunlosky, K. A. Rawson, E. J. Marsh, M. J. Nathan and D. T. Willingham, Improving students' learning with
  effective learning techniques, *Psychological Science in the Public Interest* 14 (2013) 4-58.
* J. Sweller, Cognitive load during problem solving: effects on learning, *Cognitive Science* 12 (1988) 257-285; S.
  Kalyuga, P. Ayres, P. Chandler and J. Sweller, The expertise reversal effect, *Educational Psychologist* 38 (2003)
  23-31.
* H. Pashler et al. (2008); B. A. Rogowsky et al. (2015); P. A. Mueller and D. M. Oppenheimer (2014); K. Morehead
  et al. (2019); H. L. Urry et al. (2021).
* A. T. Corbett and J. R. Anderson (1995); S. Leitner, *So lernt man lernen* (1972); P. A. Wozniak, SuperMemo
  algorithm SM-2 (1987); B. Settles and B. Meeder, A trainable spaced repetition model for language learning,
  *Proceedings of ACL 2016*, 1848-1858.
* P. B. Gough and W. E. Tunmer, Decoding, reading, and reading disability, *Remedial and Special Education* 7 (1986)
  6-10; National Reading Panel, *Teaching Children to Read* (2000); A. Castles, K. Rastle and K. Nation, Ending the
  reading wars, *Psychological Science in the Public Interest* 19 (2018) 5-51.
* L. S. Blackwell et al. (2007); V. F. Sisk et al. (2018); D. S. Yeager et al. (2019).
* A. N. Kluger and A. DeNisi, The effects of feedback interventions on performance, *Psychological Bulletin* 119
  (1996) 254-284.

## Problems and solutions

1. **The ridgeline.** In Psyche's ridgeline the best gap for a test 70 days away is about 35 days, and for 35 days
   about 21, so for 60 days about a month; Cepeda et al.'s data put the optimum nearer 10 to 20% of the delay for
   long delays (one to two weeks). Either way, err long: the cost of too long a gap is small.
2. **Schedules.** Equal: days 0, 9.3, 18.7, 28. Doubling: the unit is 28/7 = 4 days, so 0, 4, 12, 28.
3. **The simple view.** 0.4 x 0.9 = 0.36; decoding is the limit, so phonics and fluency work helps more than
   vocabulary for this child.
4. **Power for a small effect.** n = 2 (1.96 + 0.84)^2 / 0.08^2 = about 2,450 students per arm.
5. **Knowledge tracing.** P(known | wrong) = 0.5 x 0.1 / (0.5 x 0.1 + 0.5 x 0.8) = 0.11.
6. **The learning-styles test.** Classify learners by style, randomize each to matched or mismatched teaching, test
   all on the same measure; the hypothesis needs a crossover interaction, with each group learning best from its own
   method. A main effect of method, or of style, does not support it.
7. **A redesign.** Start-of-class retrieval quizzes; cumulative questions in every set and a cumulative final;
   interleaved, unlabelled problem types; worked examples faded to problems; and a delayed test against a previous
   cohort, with students told why the course feels harder.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Bloom's two sigma and its studies; VanLehn's 0.79 and 0.76; Nickow et al.'s 0.37 and its moderators; Roediger and
Karpicke's percentages at five minutes and a week; Karpicke and Roediger (2007); Rohrer and Taylor (2007) and the
2020 classroom trial; Brunmair and Richter (2019); Kornell and Bjork (2008); Deslauriers et al. (2019); Freeman et
al.'s 225 studies and failure ratio; Dunlosky et al.'s ratings of each technique; Sweller (1988) and the expertise
reversal effect; Pashler et al.'s review and the Dunns' model; Rogowsky et al. (2015); Mueller and Oppenheimer (2014),
Morehead et al. (2019) and Urry et al. (2021); Leitner's boxes, SM-2's year and rule; Settles and Meeder (2016);
Gough and Tunmer (1986); the National Reading Panel; Castles et al. (2018); Blackwell et al. (2007); Sisk et al.'s
0.08; Yeager et al.'s sample, lesson length and effects; Kluger and DeNisi's number of effects, mean and share
negative; Pashler, Cepeda, Wixted and Rohrer (2005) on right-or-wrong against correct-answer feedback; Butler, Karpicke
and Roediger (2008) on feedback after low-confidence correct answers; the hypercorrection of high-confidence errors;
Richland, Kornell and Kao (2009) on pretesting; the randomized trials of language-model tutors and of assistants in
practice; and every page range in Sources. The load budget in chapter six is schematic, and its heights are not
measurements.
