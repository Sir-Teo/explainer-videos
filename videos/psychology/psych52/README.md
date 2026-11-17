# Psychology, Built: Part 52, Designing for Minds

In the late 1980s a telephone company was about to buy new workstations for its operators, expected to save time on
every call. Wayne Gray, Bonnie John and Michael Atwood modelled the operators' perception, thinking and keystrokes
on paper and predicted the opposite: the new workstation would be slower, by about two thirds of a second a call,
because the keystrokes it saved were made while the customer was talking and the steps it added fell on the critical
path. The field trial agreed. Project Ernestine is the claim of this part: enough of psychology is quantitative to do
engineering with.

The viewer is offered a pointing task and predicts four numbers. Then the Model Human Processor and predictions by
adding cycles; GOMS, the keystroke-level model and CPM-GOMS; pointing measured as throughput with the effective width,
and the steering law; edges, corners and menu depth against breadth; information foraging and the marginal value
theorem; Norman's gulfs, affordances and signifiers; the problem-discovery curve and why five users find less than
promised; Cleveland and McGill's ranking, Stevens's exponents for area and what pops out; contrast, colour-vision
deficiency and motor tolerance; habit formation, variable schedules and dark patterns; and conversational machines.

## Where the numbers come from

| What | Source |
|---|---|
| The Model Human Processor: perceptual 100 ms (50 to 200), cognitive 70 ms (25 to 170), motor 70 ms (30 to 100); a simple reaction 240 ms (105 to 470), a physical match 310, a name match 380 | Card, Moran and Newell (1983) as reported; Psyche (`work.mhp_reaction`), item `mhp` |
| Keystroke-level operators K 0.28 s, P 1.1 s, B 0.1 s, H 0.4 s, M 1.35 s; deleting a word by shortcut 2.75 s, double-click 5.3 s, menu 8.35 s | Card, Moran and Newell (1980) as reported; Psyche (`work.klm_time`), item `klm` |
| A toy critical path for the hook: a call of 11.2 s becomes 11.8 s when a step is added to the path and keystrokes are saved off it | illustrative, item `ernestine` |
| Pointing: 16 conditions (distances 64 to 512, widths 8 to 64), 24 movements each, MT = 0.2 + 0.2 log2(D/W + 1) s with noise; fitted 0.19 + 0.20 ID, r = 0.998; mean throughput 3.8 bit/s | Psyche (`work.fitts_effective`), item `pointing` |
| The steering law: a + b A/W with a = 0.2 s, b = 0.08 s (illustrative constants) | Psyche (`work.steering_time`), item `steering` |
| Menus for 64 items: depth log_b 64, each level a Hick choice (0.2 + 0.15 log2(b + 1) s) or a linear scan (0.25 s an item) plus a 0.6 s point; practised: fastest at 64 items in one menu; unfamiliar: fastest at 8 | Psyche (`work.menu_time`), item `menus` |
| Foraging: a patch gives 10(1 - exp(-t/30)) facts; optimal stays 10, 16, 22, 29, 39 and 50 s for travel times 2, 5, 10, 20, 40 and 80 s | Psyche (`work.mvt_leave`), item `foraging` |
| Problem discovery: mean p = 0.31; 1 - (1 - p)^n gives 84% at five users; with problems' p drawn from Beta(0.6, 1.34) (same mean), 63% at five and 82% at twenty (100 problems, 400 replicates) | Psyche (`work.discovery`), item `discovery` |
| Graphical perception: perceived ratio = true ratio to the Stevens exponent (position and length 1, angle 0.85, area 0.7, volume 0.6, colour 0.5) times lognormal noise (SD 0.09 to 0.25, ordered as in Cleveland and McGill); mean absolute errors 3.7, 4.3, 7.3, 12.2, 16.5 and 21.0 points | Psyche (`work.graphical_error`), item `charts`; the exponents for angle and colour and the noise levels are illustrative |
| WCAG contrast: black on white 21, #767676 on white 4.54, #959595 on white 3.0, red on green 1.3, yellow on white 1.07, white on navy 16.0 | Psyche (`work.contrast_ratio`), item `contrast` |
| Habit: automaticity reaching 95% of its plateau at 66 days; 96 simulated people with a lognormal spread around that median (5% within 21 days; range 15 to 260) | Psyche (`work.habit_curve`, `habit_people`), item `habit`, after Lally et al. (2010) |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/work.py` gains the Model Human Processor's cycle times, the keystroke-level model with
  a simplified placement of mental operators, pointing with the effective width and throughput, the steering law, a
  menu model of depth against breadth, the marginal value theorem for an information forager, the problem-discovery
  curve with equal and unequal detectability, graphical perception as Stevens's law plus noise, WCAG contrast, and
  habit curves. Tested in `tests/psychology/test_work.py`.
* The Ledger gains four rows.
* The course's interactive: eighteen targets to click; the page fits the reader's own Fitts's law line and
  throughput from where the clicks landed.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Adding standard operator times predicts skilled users' error-free task times to within about 20%. | Card, Moran and Newell 1980 | replicated |
| People judge quantities from charts most accurately by position along a common scale, then length, then angle, then area, volume and shading. | Cleveland and McGill 1984 | replicated |
| A usability test with five users finds about 85% of an interface's usability problems. | Nielsen and Landauer 1993 | contested |
| A new habit forms in about 21 days of repetition. | Maltz 1960 | failed |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Gray, John and Atwood; Card, Moran
and Newell (1983). Fitts's law is Part 25's row.

## Build it

```bash
python -m videos.psychology.psych52.compute            # every number (seconds)
python tools/qa_scene.py psych52 Charts                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych52 -q l   # the whole part, silent preview
python tools/build.py psych52                          # 1080p30 with narration
python tools/qa_scene.py psych52 Usability --lang zh   # the Chinese edition of one chapter
python tools/make.py psych52                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 52                    # the lab: KLM, throughput, menus, foraging, discovery
python tools/check_ledger.py psych52                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's work module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Two thirds of a second | Project Ernestine; why fewer keystrokes can be slower; the question; objectives |
| 1 | On you: point and click, and four numbers | The pointing task; four predictions |
| 2 | The Model Human Processor | Three processors, three memories; predictions by adding cycles |
| 3 | GOMS and the keystroke-level model | GOMS; the operators; three ways to delete a word; CPM-GOMS |
| 4 | Pointing, measured | Sixteen conditions on one line; throughput; the steering law |
| 5 | Fitts and Hick in the interface | Edges, corners and touch; menu depth against breadth |
| 6 | Information foraging | The marginal value theorem; information scent |
| 7 | Gulfs, affordances and signifiers | Norman's two gulfs; affordances and signifiers |
| 8 | How many users? | The problem-discovery curve; tests, questionnaires and experiments |
| 9 | Seeing data | Cleveland and McGill's ranking; why area misleads; what pops out |
| 10 | Accessibility as psychophysics | Contrast computed; colour-vision deficiency; size, time and motor tolerance |
| 11 | Habit and attention by design | How long a habit takes; variable schedules; dark patterns |
| 12 | Talking to machines | Expectation; conversation, designed |
| 13 | The Ledger | Four rows; what they have in common |
| 14 | In practice: a checkout form, predicted | Where this is a job; two forms by keystroke-level model; what the model leaves out |
| 15 | Frontier: simulated users | What is new; open problems |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; payoffs; problems; references; Part 53 |

## Sources

* W. D. Gray, B. E. John and M. E. Atwood, Project Ernestine: validating a GOMS analysis for predicting and
  explaining real-world task performance, *Human-Computer Interaction* 8 (1993) 237-309.
* S. K. Card, T. P. Moran and A. Newell, *The Psychology of Human-Computer Interaction* (Erlbaum, 1983); S. K. Card,
  T. P. Moran and A. Newell (1980); J. R. Olson and G. M. Olson (1990); B. E. John and D. E. Kieras (1996).
* P. M. Fitts (1954); I. S. MacKenzie (1992); R. W. Soukoreff and I. S. MacKenzie, Towards a standard for pointing
  device evaluation, *International Journal of Human-Computer Studies* 61 (2004) 751-789; J. Accot and S. Zhai,
  Beyond Fitts' law: models for trajectory-based HCI tasks, *Proceedings of CHI 1997*, 295-302.
* K. L. Norman, *The Psychology of Menu Selection* (Ablex, 1991); P. Pirolli and S. Card, Information foraging,
  *Psychological Review* 106 (1999) 643-675; E. L. Charnov, Optimal foraging, the marginal value theorem,
  *Theoretical Population Biology* 9 (1976) 129-136.
* D. A. Norman, *The Design of Everyday Things* (revised edition, Basic Books, 2013); J. J. Gibson, *The Ecological
  Approach to Visual Perception* (Houghton Mifflin, 1979).
* J. Nielsen and T. K. Landauer (1993); J. Spool and W. Schroeder (2001); L. Faulkner (2003); J. Brooke, SUS: a
  "quick and dirty" usability scale, in *Usability Evaluation in Industry* (Taylor and Francis, 1996) 189-194.
* W. S. Cleveland and R. McGill (1984); J. Heer and M. Bostock (2010); S. S. Stevens, *Psychophysics* (Wiley, 1975);
  C. Ware, *Information Visualization: Perception for Design* (Morgan Kaufmann).
* W3C, *Web Content Accessibility Guidelines (WCAG) 2.1* (2018), success criterion 1.4.3 and the definitions of
  relative luminance and contrast ratio.
* P. Lally et al. (2010); M. Maltz (1960); A. Mathur et al., Dark patterns at scale: findings from a crawl of 11K
  shopping websites, *Proceedings of the ACM on Human-Computer Interaction* 3 (CSCW, 2019) 81.
* B. Reeves and C. Nass, *The Media Equation* (Cambridge University Press, 1996).

## Problems and solutions

1. **A keystroke-level model.** Predict with the keystroke-level model: `H M P B B H M K K K K` (K = 0.28 s).

   *Solution.* H + M + P + B + B + H + M + 4K = 0.4 + 1.35 + 1.1 + 0.1 + 0.1 + 0.4 + 1.35 + 1.12 =
   5.92 s.
2. **Fitts's law.** Fitts's law $MT = 0.2 + 0.2\,ID$, $ID = \log_2(D/W + 1)$: a 20-pixel button 300 pixels away.

   *Solution.* ID = log2(300/20 + 1) = 4 bits; MT = 0.2 + 0.2 x 4 = 1.0 s.
3. **Throughput.** Endpoints with SD 6 pixels, distance 256, mean time 0.9 s: find $W_e$, $ID_e$ and the throughput.

   *Solution.* We = 4.133 x 6 = 24.8 px; IDe = log2(256/24.8 + 1) = 3.50 bits; TP = 3.50/0.9 = 3.9 bit/s.
4. **Discovery.** Each problem is found by each user with $p = 0.2$: what share do 5 users find, and how many users for 90%?

   *Solution.* 1 - 0.8^5 = 0.67; 1 - 0.8^n >= 0.9 needs n >= ln 0.1/ln 0.8 = 10.3, so 11 users (if every problem
   really had p = 0.2).
5. **The marginal value theorem.** A patch gives $g(t) = 10(1 - e^{-t/30})$ facts; travel takes 20 s. Check that leaving at about 29 s satisfies $g'(t) = g(t)/(t + 20)$.

   *Solution.* g(29) = 10(1 - e^(-0.967)) = 6.20; g'(29) = (10/30) e^(-0.967) = 0.127; g/(t + 20)
   = 6.20/49 = 0.127. Equal.
6. **Contrast.** Relative luminances 0.18 and 1.0: find the contrast ratio. Does it pass AA for normal text?

   *Solution.* (1.0 + 0.05)/(0.18 + 0.05) = 4.57: it passes AA for normal text (4.5), narrowly.
7. ★ **A test plan.** Plan a test of a redesigned settings page: a keystroke-level comparison, a usability test, and an experiment, with what each can and cannot tell you.

   *Solution.* A keystroke-level comparison of the old and new pages for the common tasks (fast, for skilled
   users, no errors); a think-aloud test with five to eight users per round, iterated, to find problems (not rates);
   then a randomized experiment on live traffic with a preregistered metric (task completion, time, support
   contacts) and a sample size from a power analysis. Each answers a different question: how fast an expert could
   be, what goes wrong, and whether the change helps on average.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Project Ernestine's details (the company, the size of the predicted and observed differences per call, the cost per
second, the trial's length and number of operators, and the decision not to buy); the Model Human Processor's cycle
times and ranges; the keystroke-level operator times, Card, Moran and Newell's 1,280 interactions and 21% error;
Olson and Olson (1990); John and Kieras (1996); MacKenzie's throughput ranges for the mouse; ISO 9241-9 and the
4.133 factor; Accot and Zhai's steering law; menu depth-breadth findings; Pirolli and Card (1999); Charnov (1976);
Norman's gulfs and the "Norman door"; Nielsen and Landauer's average p of 0.31 and the eleven studies; Spool and
Schroeder (2001); Faulkner's range; the SUS average of about 68; Cleveland and McGill's ranking and error measure;
Heer and Bostock (2010); Stevens's exponents for area and volume; the WCAG contrast thresholds and formula; the
prevalence of red-green colour-vision deficiency; Lally et al.'s 96 participants, 66-day median and 18-254 range;
Maltz's 21 days; Mathur et al.'s 11,000 sites and the share with dark patterns; Reeves and Nass (1996); the 200 ms
gap between conversational turns; and every page range in Sources.
