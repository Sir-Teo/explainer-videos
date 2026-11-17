# Psychology, Built: Part 42, Does Therapy Work?

The part opens with the care card: this is education, not diagnosis or treatment, and here is where help is found;
it touches on trauma and self-harm. In 1952 Hans Eysenck surveyed the outcome studies and concluded that about two
thirds of neurotic patients improve with or without psychotherapy. The claim was infuriating and nearly impossible to
answer without proper controls and a method for adding up studies. In 1977 Smith and Glass used that method,
meta-analysis, to answer him. Then came the harder questions: compared with what, by which ingredient, and how much
of the published effect is real.

The viewer is shown two graphs and asked which one shows therapy working, and predicts four numbers. Then the trial:
regression to the mean on the Pool, how the control sets the effect, and researcher allegiance (computed);
meta-analysis from Glass's standardized difference to a random-effects forest plot built by hand; the dodo bird, the
alliance and specific ingredients; the four families of therapy and dialectical behaviour therapy; therapy against
medication, and relapse after each stops; the registered and published antidepressant trials, a filtered literature
(computed) and "Was Eysenck right after all?"; Jacobson and Truax's reliable change and cut-off, derived and applied
to four clients; treatments that harm; lobotomy and ECT; and the dose-response curve and the treatment gap.

## Where the numbers come from

| What | Source |
|---|---|
| The trial simulator: each person's mean score N(14, 5²), each occasion N(0, 5²); 200 people per arm enrol at a score of 20 or more (mean 23.5) and are scored again; end means 18.9 (waiting list, a small harm of 1 point), 17.9 (no treatment), 15.9 (placebo therapy, 2 points of common factors) and 13.9 (active therapy, 4 points); the active arm's d is 0.75 against the waiting list, 0.59 against no treatment and 0.27 against placebo therapy (2,000 per arm) | Psyche (`clinic.therapy_trial`, `trial_effect`), item `arms` |
| Researcher allegiance: 60 comparisons of two equally good therapies, half run by each side's loyal team (bias 0.25): pooled advantage +0.01; by A's loyalists +0.28, by B's -0.25 | Psyche (`clinic.allegiance`), item `allegiance` |
| A forest plot: twelve simulated trials of a true effect of 0.5 (between-trial SD 0.15); DerSimonian-Laird estimate 0.51, SE 0.07, tau² 0.010, I² 18% | Psyche (`clinic.random_effects`), item `forest` |
| A filtered literature: 400 trials of a true effect of 0.3, 10 to 80 per arm; 173 published (the significant ones and a fifth of the rest), 69% of them significant; pooled published effect 0.43, all trials 0.29 | Psyche (`clinic.publication_filter`, `random_effects`), item `bias` |
| Reliable change for a scale with SD 7 and reliability 0.85: a change of 7.5 points; the cut-off between a clinical group (28, SD 6) and a well group (7, SD 5): 16.5; four clients (30 to 14, 30 to 25, 22 to 15, 34 to 20) with RCI -4.17, -1.30, -1.83, -3.65 | Psyche (`clinic.reliable_change`, `jt_cutoff`), item `rci` |
| Jacobson and Truax's categories in 2,000 people per arm of the trial simulator (SD 7.07, reliability 0.85, cut-off 20.8 between the enrolled and the population): recovered 30% with no treatment, 26% on the waiting list, 43% with placebo therapy and 56% with active therapy; a therapy 3 points worse than none: reliable deterioration 5.7% against 2.2%, and 16% still recovered | Psyche (`clinic.jt_categories`), item `categories` |
| The dose-response curve: a log-normal through half improved by 8 sessions and three quarters by 26 | Psyche (`clinic.dose_response`), item `dose` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

Schematic panels (the alliance scatter, the two-graphs problem's lines, Eysenck's bars at his reported percentages,
the relapse bars at Hollon and colleagues' percentages) are labelled or described as such; where a value is shown on
them, it is the published value.

## Built in this part

* `explainer/psychology/psyche/clinic.py` gains the therapy-trial simulator, the effect against each control, the
  publication filter, DerSimonian and Laird's random-effects meta-analysis, researcher allegiance, Jacobson and
  Truax's reliable change index, cut-off and categories, and the dose-response curve. Tested in `tests/psychology/test_clinic.py`.
* The Ledger gains seven rows; the deferred declarations of Parts 2, 6 and 10 about treatments are resolved.
* The course's interactive is the two-graphs problem, case by case: six study designs, each judged as able, or not
  able, to show that a therapy worked.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| People who receive psychotherapy end better off than comparable people who receive none | Smith and Glass (meta-analysis) 1977 | replicated |
| Psychotherapy for adult depression has a large effect, near g = 0.7 against control conditions, as the whole published literature suggests | Cuijpers and colleagues (all trials) 2019 | replicated, smaller |
| All bona fide psychotherapies are about equally effective | Luborsky, Singer and Luborsky 1975 | contested |
| The quality of the working alliance between client and therapist correlates with how well therapy goes | Horvath and Symonds (meta-analysis) 1991 | replicated |
| Dialectical behaviour therapy reduces self-harm in people with borderline personality disorder | Linehan and colleagues 1991 | replicated |
| A single session of psychological debriefing soon after a trauma prevents post-traumatic stress | Mitchell 1983 | failed |
| Taking young offenders to visit prisons, to be confronted by inmates, deters them from crime | Scared Straight!, the programme and the documentary 1978 | failed |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Eysenck; Driessen and colleagues;
Hollon and colleagues; Turner and colleagues; Moniz; Cerletti and Bini; Howard and colleagues.

## Build it

```bash
python -m videos.psychology.psych42.compute            # every number (a few seconds)
python tools/qa_scene.py psych42 Trial                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych42 -q l   # the whole part, silent preview
python tools/build.py psych42                          # 1080p30 with narration
python tools/qa_scene.py psych42 Bias --lang zh        # the Chinese edition of one chapter
python tools/make.py psych42                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 42                    # the lab: trials, controls, meta-analysis, bias, change
python tools/check_ledger.py psych42                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's clinic module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | 1952: two thirds recover anyway | The care card; Eysenck's challenge; an answer and harder questions; the question; objectives |
| 1 | On you: two graphs, and four numbers | Which graph shows therapy working; four predictions |
| 2 | The trial, and the control problem | Everyone improves; the control sets the effect; whose therapy wins? |
| 3 | Meta-analysis is born | One scale for every study; a forest plot, by hand |
| 4 | The dodo bird | "Everybody has won"; the alliance; where ingredients matter |
| 5 | The therapies | Four families; a therapy built for self-harm |
| 6 | Pills, talk, or both | Head to head; after treatment stops |
| 7 | How big is it really? | Two piles of trials; a filtered literature, computed; was Eysenck right after all? |
| 8 | Clinical significance | Two questions about one person; four clients; recovered without treatment |
| 9 | Treatments that harm | Good intentions, bad outcomes; why harm goes unseen; could a clinic see the harm? |
| 10 | The body treatments | A Nobel Prize; ECT, then and now |
| 11 | How much therapy? | The dose-response curve; most people get none |
| 12 | The Ledger | Seven rows and the tally |
| 13 | In practice: guidelines, choices and monitoring | From evidence to a person |
| 14 | Frontier: mechanisms, matching and psychedelics | Three frontiers; open questions |
| | Recap, problems, and the road ahead | Your numbers; eleven lines; Kant's three objections; payoffs; problems; references; Part 43 |

## Sources

* H. J. Eysenck, The effects of psychotherapy: an evaluation, *Journal of Consulting Psychology* 16 (1952)
  319-324; G. V. Glass, Primary, secondary, and meta-analysis of research, *Educational Researcher* 5 (1976) 3-8;
  M. L. Smith and G. V. Glass, Meta-analysis of psychotherapy outcome studies, *American Psychologist* 32 (1977)
  752-760; M. L. Smith, G. V. Glass and T. I. Miller, *The Benefits of Psychotherapy* (1980); H. J. Eysenck, An
  exercise in mega-silliness, *American Psychologist* 33 (1978) 517.
* R. DerSimonian and N. Laird, Meta-analysis in clinical trials, *Controlled Clinical Trials* 7 (1986) 177-188.
* S. Rosenzweig, Some implicit common factors in diverse methods of psychotherapy, *American Journal of
  Orthopsychiatry* 6 (1936) 412-415; L. Luborsky, B. Singer and L. Luborsky (1975); B. E. Wampold et al. (1997);
  D. F. Tolin (2010); B. E. Wampold and Z. E. Imel, *The Great Psychotherapy Debate* (2nd edition, 2015).
* A. O. Horvath and B. D. Symonds (1991); C. Flückiger et al. (2018).
* A. T. Beck, *Cognitive Therapy and the Emotional Disorders* (1976); M. M. Linehan et al. (1991, 2006); C. R.
  DeCou, K. A. Comtois and S. J. Landes (2019).
* S. D. Hollon et al., Prevention of relapse following cognitive therapy vs medications in moderate to severe
  depression, *Archives of General Psychiatry* 62 (2005) 417-422.
* E. H. Turner, A. M. Matthews, E. Linardatos, R. A. Tell and R. Rosenthal, Selective publication of antidepressant
  trials and its influence on apparent efficacy, *New England Journal of Medicine* 358 (2008) 252-260; E. Driessen
  et al. (2015); P. Cuijpers et al. (2019).
* N. S. Jacobson and P. Truax, Clinical significance: a statistical approach to defining meaningful change in
  psychotherapy research, *Journal of Consulting and Clinical Psychology* 59 (1991) 12-19.
* J. T. Mitchell (1983); S. Rose et al. (2002); R. A. Mayou, A. Ehlers and M. Hobbs (2000); A. Petrosino et al.
  (2013); S. O. Lilienfeld, Psychological treatments that cause harm, *Perspectives on Psychological Science* 2
  (2007) 53-70.
* E. Moniz, *Tentatives opératoires dans le traitement de certaines psychoses* (Masson, 1936); E. S. Valenstein,
  *Great and Desperate Cures* (1986); U. Cerletti, Old and new information about electroshock, *American Journal of
  Psychiatry* 107 (1950) 87-94; UK ECT Review Group, Efficacy and safety of electroconvulsive therapy in depressive
  disorders, *Lancet* 361 (2003) 799-808.
* K. I. Howard, S. M. Kopta, M. S. Krause and D. E. Orlinsky, The dose-effect relationship in psychotherapy,
  *American Psychologist* 41 (1986) 159-164.

## Problems and solutions

1. **Regression to the mean.** Given a screened score x, the expected mean is 14 + (25/50)(x - 14) = 19 for x = 24,
   and the next score's expectation is the same: 19. Five points of improvement are expected with no treatment.
2. **Three controls.** Against the waiting list d = (18.85 - 13.85)/6.7 = 0.75; against placebo therapy
   (15.85 - 13.85)/6.7 = 0.30; the same therapy has an effect less than half as large against the stronger control.
3. **A small meta-analysis.** Weights 25, 50, 20 (sum 95): the fixed-effect estimate is (10 + 30 + 4)/95 = 0.463 with
   SE 1/√95 = 0.103. Q = 25(0.063)² + 50(0.137)² + 20(0.263)² = 2.42 on 2 df, so
   τ² = (2.42 - 2)/(95 - 3525/95) = 0.42/57.9 = 0.0073.
4. **Reliable change.** S_diff = √2 × 7 × √0.15 = 3.83, so a reliable change exceeds 1.96 × 3.83 = 7.5 points. From
   26 to 20, RCI = -6/3.83 = -1.56: not reliable.
5. **The cut-off.** c = (6 × 7 + 5 × 28)/(6 + 5) = 182/11 = 16.5.
6. **A significance filter.** With 20 per arm, SE ≈ √(2/20) = 0.316, so significance needs d > 1.96 × 0.316 = 0.62.
   Power = P(Z > 1.96 - 0.3/0.316) = P(Z > 1.01) ≈ 0.16. The published mean is the mean of a normal (0.3, 0.316)
   above 0.62: 0.3 + 0.316 × φ(1.01)/(1 - Φ(1.01)) = 0.3 + 0.316 × 0.240/0.156 ≈ 0.79, more than two and a half
   times the truth.
7. **Ingredient against common factors.** Randomize to the full therapy, the same therapy without the ingredient
   (a dismantling arm, delivered with equal warmth, rationale and time), and a credible placebo therapy; rate the
   alliance and measure the proposed mechanism every session; preregister that the ingredient's arm should beat
   the dismantled one, that mechanism change should precede symptom change within people (a lagged multilevel
   model, Part 47), and that the alliance alone should not account for the difference.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Eysenck's figures (44% for psychoanalysis, 64% for eclectic therapy, 72% for custodial care) and his "two thirds";
Glass's naming of meta-analysis (1976); Smith and Glass's 375 studies and 0.68, and "better off than 75%";
Eysenck's "mega-silliness" (1978); Rosenzweig (1936); Luborsky et al. (1975) and the dodo quotation; Wampold et al.
(1997); Tolin (2010); Horvath and Symonds' 0.26; Flückiger et al.'s 295 studies and 0.28; Linehan et al. (1991:
44 women, and the outcomes described) and (2006: 101 women, about half the rate of suicide attempts); DeCou et al.
(2019); the equivalence of cognitive therapy and antidepressants in the short term and the advantage of combining
them; Hollon et al.'s relapse rates (about 31%, 76% and 47%); Turner et al.'s 74 trials, twelve drugs, 51% and 94%,
and an inflation of about a third; Driessen et al.'s quarter of unpublished trials; Cuijpers et al. (2019), the
overall g near 0.7 and the smaller adjusted effect; the evidence that waiting lists may harm; Jacobson and Truax's
formulas; Mitchell (1983), Rose et al. (2002) and Mayou et al.'s three-year result; Petrosino et al. (2013) on Scared
Straight; the evidence on recovered-memory techniques and conversion therapy; the share of clients who deteriorate
(5 to 10%); Moniz's dates (1935 operations, 1936 publication, 1949 Nobel Prize) and the scale of Freeman's
operations; Cerletti and Bini (1938) and modern ECT's evidence against sham; Howard et al.'s half by 8 sessions and
three quarters by 26; the "good enough level" findings; stepped care; the evidence that outcome feedback reduces
deterioration; treatment-selection models; the 2024 decision on MDMA-assisted therapy; and every page range in
Sources.
