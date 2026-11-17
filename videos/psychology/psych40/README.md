# Psychology, Built: Part 40, Fear and Sadness

The part opens with the care card: this is education, not diagnosis or treatment, and here is where help is found;
it touches on suicide, under safe-messaging rules (no method detail, help on screen). In 1967 dogs that had received
shocks they could not escape later lay down and took shocks they could escape. The finding became a theory of
depression, and fifty years later its own authors reversed the explanation: passivity is the default, and what is
learned is control. The part builds anxiety and depression out of the learning and choice models of Acts IV and V,
and weighs what trials say about the drugs.

The hook is Seligman and Maier's triadic design and the 2016 revision; the viewer sees a dot-probe trial (unscored)
and predicts four numbers. Then Mowrer's two factors and an avoidance loop that never unlearns (computed); extinction
as context-bound learning, renewal (computed) and the principles for making exposure last; the anxiety disorders in
one frame and the panic spiral; attention to threat, the unreliable dot-probe score and the failed bias-modification
trials; depression's cognitive accounts; the triadic design as a belief about control (computed); anhedonia and
Rutledge and colleagues' model of momentary mood (simulated and fitted); the monoamine story and the 2022 umbrella
review; Kirsch's analysis and the 522-trial network meta-analysis; life events, and the gene-by-stress finding that
did not survive large samples; and bipolar disorder, lithium, and why suicide cannot be predicted well for
individuals. The practice chapter maps treatments onto the models; the frontier is subtypes, fast-acting treatments
and computational phenotyping.

## Where the numbers come from

| What | Source |
|---|---|
| A Rescorla-Wagner learner with 20 signal-shock pairings, then 60 trials without shock: allowed to avoid (at most 95% of trials, extinction rate 0.08) it avoids 95% of trials and its fear ends at 0.78 (median of 21 runs); with response prevention, fear ends at 0.01 | Psyche (`clinic.avoidance`), item `avoid` |
| Fear learned in context A and extinguished in B: about 0 in B, back near 1 in A and in a new context C | Psyche (`clinic.renewal`), item `renewal` |
| Extinction spread over 1 to 6 contexts, each sharing a quarter of its features with a new place: fear in the new place falls from 0.74 to 0.18 of its peak | Psyche (`clinic.renewal_contexts`), item `contexts` |
| A risk factor with sensitivity and specificity 0.8, for a death with a yearly base rate of 1 in 2,000, in 10,000 people: 5 deaths, 4 flagged, 1,999 others flagged; 0.2% of those flagged | Psyche (`clinic.screen`), item `suicide` |
| The triadic design as a Beta belief about control, 200 animals per group: escapable first 98% escaping across 10 test trials, inescapable first 13%, no shock first 69% and rising | Psyche (`clinic.helplessness`), item `helpless` |
| The behavioural-activation trap: 90 days choosing between an activity (reward 0.6 on average, learned only by doing it, estimated at -0.5 after a loss) and rest (0.2, known); left alone the median run is active on 0% of the last 30 days, with the activity scheduled for the first 14 days on 97% | Psyche (`clinic.activation`), item `activation` |
| A 90-trial gambling task with happiness simulated from Rutledge and colleagues' model (weights 0.5, 0, 0.25, 0.6; forgetting 0.65): the fit recovers the prediction-error weight as 0.55 with forgetting 0.70 (R² 0.70); blunting prediction errors to 40% cuts the SD of happiness from 0.46 to 0.29 | Psyche (`clinic.mood_task`, `fit_mood`), item `mood` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

Schematic panels (the dot-probe test-retest cloud, the drug and placebo bars, the odds-ratio forest, the
gene-by-stress lines, the mood course in bipolar disorder) are labelled as schematic on screen; where a value is
shown on them, it is the published value.

## Built in this part

* `explainer/psychology/psyche/clinic.py` gains Mowrer's avoidance loop, Bouton's context-bound extinction and
  extinction spread over several contexts, the
  triadic design as a belief about control, the trap that behavioural activation breaks, and Rutledge and colleagues' model of momentary mood with its fit.
  Tested in `tests/psychology/test_clinic.py`.
* The Ledger gains eight rows.
* The course's interactive is the dot-probe: twenty trials with neutral and threat words, timed, with the bias
  shown only as the group-level idea it is (no score is given, as the series' care rules require).

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Treatments built on exposure reduce anxiety more than control conditions | Wolpe 1958 | replicated |
| Extinguished fear returns with a change of context, with time, or after a reminder | Bouton and Bolles 1979 | replicated |
| Animals given uncontrollable shock later fail to escape, because they learned responding does not matter | Seligman and Maier 1967 | replicated |
| Training attention away from threat reduces anxiety | MacLeod and colleagues 2002 | failed |
| Depression is caused by a shortage of serotonin | Schildkraut and the monoamine hypothesis 1965 | failed |
| Antidepressants relieve depression more than placebo | Kirsch and colleagues 2008 | replicated, smaller |
| Stressful events cause depression more often in carriers of the short 5-HTTLPR allele | Caspi and colleagues 2003 | failed |
| Known risk factors predict which individuals will attempt suicide with useful accuracy | Pokorny 1983 | failed |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Mowrer; Craske and colleagues;
Clark; Beck and Abramson, Seligman and Teasdale; Schildkraut; Brown and Harris; Cade.

## Build it

```bash
python -m videos.psychology.psych40.compute            # every number (a few seconds)
python tools/qa_scene.py psych40 Avoid                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych40 -q l   # the whole part, silent preview
python tools/build.py psych40                          # 1080p30 with narration
python tools/qa_scene.py psych40 Mood --lang zh        # the Chinese edition of one chapter
python tools/make.py psych40                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 40                    # the lab: avoidance, renewal, control, mood
python tools/check_ledger.py psych40                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's clinic module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | 1967: dogs that stopped trying | The care card; the triadic design; fifty years later; the question; objectives |
| 1 | On you: a dot, and four numbers | A dot-probe trial; four predictions |
| 2 | Fear that never unlearns | Two factors; the loop, computed |
| 3 | Exposure, and the return of fear | Extinction is new learning; making exposure last; many places, computed |
| 4 | The anxiety disorders in one frame | What is feared and what keeps it going; the panic spiral; compulsion as habit |
| 5 | Attention to threat | A bias, a measure and a treatment |
| 6 | Depression and thought | Three cognitive accounts |
| 7 | Helplessness and control | The triadic design, computed |
| 8 | Reward and mood | Anhedonia; momentary mood, modelled; the trap of doing less, computed |
| 9 | The chemical story | Two accidents and a hypothesis; what the evidence on serotonin shows |
| 10 | Do antidepressants work? | Drug, placebo, and the gap; 522 trials |
| 11 | Stress, life events and genes | Social origins; a gene, stress, and a failed interaction |
| 12 | Bipolar disorder, lithium, and suicide | Highs and lows; why suicide is so hard to predict; the base rate in natural frequencies |
| 13 | The Ledger | Eight rows and the tally |
| 14 | In practice: treatments as models | Each therapy acts on a model |
| 15 | Frontier: subtypes, speed and computation | Three frontiers; open questions |
| | Recap, problems, and the road ahead | Your numbers; eleven lines; Kant's three objections; payoffs; problems; references; Part 41 |

## Sources

* M. E. P. Seligman and S. F. Maier, *Journal of Experimental Psychology* 74 (1967) 1-9; S. F. Maier and M. E. P.
  Seligman, Learned helplessness at fifty, *Psychological Review* 123 (2016) 349-367.
* O. H. Mowrer, On the dual nature of learning, *Harvard Educational Review* 17 (1947); J. Wolpe, *Psychotherapy by
  Reciprocal Inhibition* (1958).
* M. E. Bouton, Context, ambiguity, and unlearning, *Biological Psychiatry* 52 (2002) 976-986; M. E. Bouton and
  R. C. Bolles, *Learning and Motivation* 10 (1979); B. Vervliet, M. G. Craske and D. Hermans, *Annual Review of
  Clinical Psychology* 9 (2013); M. G. Craske et al., *Behaviour Research and Therapy* 58 (2014) 10-23; J. K.
  Carpenter et al., *Depression and Anxiety* 35 (2018).
* D. M. Clark, A cognitive approach to panic, *Behaviour Research and Therapy* 24 (1986) 461-470.
* C. M. Gillan et al., Disruption in the balance between goal-directed behavior and habit learning in
  obsessive-compulsive disorder, *American Journal of Psychiatry* 168 (2011) 718-726; C. M. Gillan, M. Kosinski,
  R. Whelan, E. A. Phelps and N. D. Daw, Characterizing a psychiatric symptom dimension related to deficits in
  goal-directed control, *eLife* 5 (2016) e11305.
* D. A. Richards et al., Cost and outcome of behavioural activation versus cognitive behavioural therapy for
  depression (COBRA), *Lancet* 388 (2016) 871-880.
* C. MacLeod et al., *Journal of Abnormal Psychology* 111 (2002); I. A. Cristea, R. N. Kok and P. Cuijpers, *British
  Journal of Psychiatry* 206 (2015) 7-16.
* A. T. Beck, *Depression* (1967); L. Y. Abramson, M. E. P. Seligman and J. D. Teasdale, *Journal of Abnormal
  Psychology* 87 (1978); S. Nolen-Hoeksema, *Journal of Abnormal Psychology* 100 (1991).
* R. B. Rutledge, N. Skandali, P. Dayan and R. J. Dolan, A computational and neural model of momentary subjective
  well-being, *PNAS* 111 (2014) 12252-12257.
* J. J. Schildkraut, *American Journal of Psychiatry* 122 (1965); J. Moncrieff et al., The serotonin theory of
  depression, *Molecular Psychiatry* (2022).
* I. Kirsch et al., *PLoS Medicine* 5 (2008) e45; A. Cipriani et al., *Lancet* 391 (2018) 1357-1366.
* G. W. Brown and T. Harris, *Social Origins of Depression* (1978); A. Caspi et al., *Science* 301 (2003) 386-389;
  R. C. Culverhouse et al., *Molecular Psychiatry* 23 (2018); R. Border et al., *American Journal of Psychiatry* 176
  (2019).
* J. F. J. Cade, Lithium salts in the treatment of psychotic excitement, *Medical Journal of Australia* (1949);
  A. D. Pokorny, *Archives of General Psychiatry* 40 (1983); J. C. Franklin et al., *Psychological Bulletin* 143
  (2017) 187-232.

## Problems and solutions

1. **Exposures avoidance allows.** A Rescorla-Wagner learner has fear $V = 0.9$ and avoids on every trial with probability $0.95\,\sigma(10(V - 0.3))$. With extinction rate $0.08$, how many full exposures does it take to bring $V$ below 0.3, and roughly how many trials will that take?

   *Solution.* Each full exposure multiplies V by 0.92. From 0.9, V < 0.3 needs n with
   0.9 × 0.92ⁿ < 0.3, so n > ln(1/3)/ln(0.92) ≈ 13.2: 14 exposures. While V is high the learner avoids on 95% of
   trials, so one exposure comes about every 20 trials: roughly 280 trials (fewer as V falls and avoidance weakens).
2. **Renewal.** In the renewal model, excitation $E$ is expressed everywhere and inhibition $I$ only in context B. Write the fear in A, B and C after extinction, and suggest one way to make extinction generalize.

   *Solution.* After extinction, fear in B is E − I ≈ 0, in A and in C it is E. Extinction generalizes better when
   it is practised in several contexts, or when retrieval cues from the extinction context are carried into others.
3. **Belief about control.** A learner starts with a Beta(1, 1) belief about control. After 10 tries that all fail, what is its probability of trying? After 10 that all succeed?

   *Solution.* Beta(1, 1) after 10 failures is Beta(1, 11): it tries with probability 1/12 ≈ 0.08. After
   10 successes, Beta(11, 1): 11/12 ≈ 0.92.
4. **A mood.** Happiness $H_t = w_0 + w_3 \sum_j \gamma^{t-j} \delta_j$. If every prediction error is 0.5 for ten trials, find $H_{10}$ for $\gamma = 0.7$, $w_0 = 0.5$, $w_3 = 0.6$.

   *Solution.* H₁₀ = 0.5 + 0.6 × 0.5 × (1 − 0.7¹⁰)/(1 − 0.7) = 0.5 + 0.3 × 0.9718/0.3 ≈ 0.5 + 0.97 = 1.47.
5. **Effect size and NNT.** A drug and a placebo improve depression by 9.6 and 7.8 points, with SD 8 in both groups. What is the standardized effect size, and how many people need to be treated for one extra response if response rates are 50% and 40%?

   *Solution.* d = (9.6 − 7.8)/8 ≈ 0.23. With response rates 50% and 40%, the number needed to treat is
   1/(0.5 − 0.4) = 10.
6. **A risk factor's yield.** A risk factor has sensitivity 0.8 and specificity 0.8 for suicide death within a year, where the base rate is 1 in 2{,}000. What share of people it flags will die by suicide in that year?

   *Solution.* Per 2,000 people, one dies; the factor flags 0.8 of that person and 0.2 × 1,999 ≈ 400
   others: the share of flagged people who die is 0.8/400.6 ≈ 0.2%, about 1 in 500.
7. ★ **Liking, learning or effort.** Design a study that could tell whether a person's anhedonia is a problem of liking, of learning or of effort.

   *Solution.* Measure hedonic ratings of rewards as received (liking); fit a learning model to
   choices in a probabilistic reward task (learning rate and reward sensitivity); and offer choices between low-effort
   small rewards and high-effort large ones (effort). A person whose ratings are normal but whose learning is
   blunted differs from one whose effort is the problem; preregister which parameter each hypothesis predicts will
   differ, and test it in people with and without anhedonia.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Seligman and Maier's design and result; Maier and Seligman's 2016 conclusions; Mowrer's two factors; Bouton's
account and Bouton and Bolles's renewal; Craske et al.'s principles; Clark's model; MacLeod et al. (2002) and Cristea
et al.'s conclusion; the dot-probe's low test-retest reliability (the schematic r ≈ 0.15 is illustrative); Beck,
Abramson et al. and Nolen-Hoeksema; Gillan et al.'s two studies (the devaluation result in OCD, and the transdiagnostic compulsivity dimension in online
samples); behavioural activation's equivalence to cognitive behavioural therapy (Richards et al., 2016); Rutledge et
al.'s model and its smartphone replication; the reserpine and
iproniazid history; Moncrieff et al.'s conclusion and the replies; Kirsch et al.'s 1.8 points and severity finding;
Cipriani et al.'s 522 trials, 116,477 people, 21 drugs and odds ratios 1.37 to 2.13; Brown and Harris's findings;
Caspi et al. (2003), Culverhouse et al.'s 38,802 people and Border et al.'s conclusion; Cade's discovery; Pokorny's
study (about 4,800 patients); Franklin et al.'s 365 studies and conclusion; the evidence that asking about suicidal
thoughts does not increase them; ketamine's rapid effect; and every page range in Sources.
