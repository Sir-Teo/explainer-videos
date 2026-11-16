# Psychology, Built: Part 36, Us and Them

Henri Tajfel was born in Poland and was Jewish; captured in 1940 as a soldier in the French army, he survived the war
as a prisoner. At Bristol he asked what the least is that it takes for people to discriminate. In 1971 he and his
colleagues divided schoolboys by a trivial test, in one study their preference between pictures said to be by Klee
and by Kandinsky, and had each boy share points between a boy in his own group and a boy in the other. Nobody met,
competed or gained, and the boys still favoured their own group, often giving up points so that it would come out
ahead. This part asks how little it takes to make a group, how prejudice is measured, what a bias score means for a
person and for a crowd, and what changes behaviour, as opposed to scores.

The hook is the paintings and the matrices; the viewer takes a boy's place and predicts four numbers. Then social
identity and self-categorization, Balliet, Wu and De Dreu's 212 studies of ingroup cooperation, Robbers Cave as run
and as staged; stereotypes as categories, the stereotype content model and an illusory correlation (computed);
measuring prejudice by asking, with a list experiment (computed); by speed, with the Implicit Association Test as
two blocks of diffusion decisions (computed), its retest reliability, its correlations with behaviour and Forscher
et al.'s 492 studies; and by behaviour, with Bertrand and Mullainathan's résumés, Quillian et al.'s 25 years of
audits and the power an audit needs (computed). Then stereotype threat, the adjustment that hid the gap and a
registered test, against a filtered literature (computed); contact, from Allport to the 27 randomized studies;
prejudice reduction's review, the Rwandan radio drama and diversity training; deep canvassing, faked and then done;
and a promotion ladder on which a small bias compounds (computed). The practice chapter is audits and structure;
the frontier is the bias of crowds.

## Where the numbers come from

| What | Source |
|---|---|
| Tajfel's matrix, 7..19 for the own group against 1..25 for the other: maximum joint and ingroup profit at the right end (19 and 25), maximum difference at the left (7 and 1), equality at 13 and 13 | Psyche (`social.tajfel_matrix`, `allocate`), item `matrix` |
| Hamilton and Gifford's counts (18 and 8 against 9 and 4): with the rare group's rare acts remembered 1.6 times as strongly, its undesirable share is remembered as 42% instead of 31% | Psyche (`social.illusory_correlation`), item `illusory` |
| The list experiment: 2,000 surveys of 1,000 people, true prevalence 20%: estimates centred on 0.20 with an SD of 0.057, about 4.5 times a direct question's | Psyche (`social.list_experiment`), item `listexp` |
| The IAT: 400 simulated people, each with a stable association (mean 0.15, SD 0.10) and an occasion-to-occasion part (SD 0.07), 60 trials per block: test-retest 0.52, correlation with a behaviour 0.20 (0.24 with no occasion part), mean D 0.39 with t = 24 | Psyche (`social.iat_d`, `iat_study`), item `iat` |
| An audit study: callbacks at an illustrative 9.6% against 6.4% need about 1,125 applications per group for 80% power | computed (two-proportion power), item `audit` |
| A filtered literature: 60 laboratories test a null effect with 25 per group; 15 studies are published, pooling to d = 0.51, against a large study's 0.06 | Psyche (`evidence.literature`), item `threat` |
| The ladder: eight levels, the top half promoted, a 0.1 SD advantage: the other group's share falls from 50% to 36% (43% for 0.05 SD, 24% for 0.2 SD) | Psyche (`social.pipeline`), item `ladder` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/social.py` (committed with Part 35): Tajfel's matrices and an allocation rule; an IAT
  as diffusion decisions with stable and occasion-to-occasion parts; the list experiment; a promotion ladder solved
  exactly from normal tails; an illusory-correlation model; and, written ahead for Part 37, inequity aversion
  (`fs_utility`, `fs_threshold`, `ultimatum`), a public-goods game with and without punishment (`public_goods`), an
  iterated prisoner's dilemma tournament (`ipd_tournament`) and a divorce classifier scored in and out of sample
  (`overfit_divorce`). Tested in `tests/psychology/test_social.py`.
* The Ledger gains eight rows.
* The course's interactive is a minimal group: pick a picture, then share points eight times between a member of
  your group and a member of the other, in two kinds of matrix; it reports your average lead against what the most
  points for everyone, or equality, would have given.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Assigning people to groups by a trivial criterion is enough for them to favour their own group | Tajfel, Billig, Bundy and Flament 1971 | replicated |
| On average, people sort faster when categories and attributes are paired as common associations pair them | Greenwald, McGhee and Schwartz 1998 | replicated |
| A person's IAT score predicts their discriminatory behaviour well enough to judge or select individuals, and changing it changes behaviour | Greenwald and colleagues 2009 | failed |
| Identical applications receive fewer callbacks when the name signals a Black applicant | Bertrand and Mullainathan 2004 | replicated |
| Reminding people of a negative stereotype about their group lowers their test performance | Steele and Aronson 1995 | contested |
| Contact between members of different groups reduces prejudice | Pettigrew and Tropp 2006 | replicated |
| A single conversation at the door can durably reduce prejudice | LaCour and Green 2014 | replicated |
| Competition between groups of boys at a summer camp produced hostility, and shared goals removed it | Sherif and colleagues 1954 | story and record |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Tajfel and Turner, Turner et
al., Fiske, Cuddy, Glick and Xu, Hamilton and Gifford, Paluck (2009), Paluck, Porat, Clark and Green, Chang et al.,
and Payne, Vuletich and Lundberg with Connor and Evers.

## Build it

```bash
python -m videos.psychology.psych36.compute            # every number (a few seconds)
python tools/qa_scene.py psych36 IAT                   # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych36 -q l   # the whole part, silent preview
python tools/build.py psych36                          # 1080p30 with narration
python tools/qa_scene.py psych36 Audits --lang zh      # the Chinese edition of one chapter
python tools/make.py psych36                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 36                    # the lab: matrices, list experiment, IAT, audits, ladder
python tools/check_ledger.py psych36                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's social module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | 1971: Klee or Kandinsky | Tajfel; the paintings; the matrix; the question; objectives |
| 1 | On you: a group, and four numbers | A boy's choice on you; four predictions |
| 2 | Identity and competition | Social identity; how big favouritism is; Robbers Cave; as run, and as staged |
| 3 | Stereotypes | A stereotype is a category; warmth and competence; a correlation that is not there |
| 4 | Measuring by asking | What people will say; the list experiment |
| 5 | Measuring by speed | The IAT; Psyche takes it; the same person twice; reliability and prediction; changing the score |
| 6 | Measuring by behaviour | Emily and Greg, Lakisha and Jamal; twenty-five years of audits; how many applications |
| 7 | Stereotype threat | A test called diagnostic; what the adjustment hid; many small studies and one large one |
| 8 | Contact | Allport's conditions; only the randomized studies |
| 9 | Reducing prejudice | Hundreds of experiments; a radio drama in Rwanda; diversity training |
| 10 | Deep canvassing | A study too good to be true; the real experiment |
| 11 | From bias to system | Eight rungs of a ladder; the limits of individual explanation |
| 12 | The Ledger | Eight rows and the tally |
| 13 | In practice: audits and structure | What to buy instead of a training; paired testing; auditing an algorithm |
| 14 | Frontier: bias in crowds | The bias of crowds; open questions |
| | Recap, problems, and the road ahead | Your numbers; eleven lines; Kant's three objections; payoffs; problems; references; Part 37 |

## Sources

* H. Tajfel, M. G. Billig, R. P. Bundy and C. Flament, Social categorization and intergroup behaviour, *European
  Journal of Social Psychology* 1(2) (1971) 149-178.
* H. Tajfel and J. C. Turner, An integrative theory of intergroup conflict (1979); J. C. Turner et al.,
  *Rediscovering the Social Group: A Self-Categorization Theory* (1987).
* D. Balliet, J. Wu and C. K. W. De Dreu, Ingroup favoritism in cooperation: a meta-analysis, *Psychological
  Bulletin* 140(6) (2014) 1556-1581.
* M. Sherif, O. J. Harvey, B. J. White, W. R. Hood and C. W. Sherif, *Intergroup Conflict and Cooperation: The
  Robbers Cave Experiment* (1961); G. Perry, *The Lost Boys: Inside Muzafer Sherif's Robbers Cave Experiment* (2018).
* D. L. Hamilton and R. K. Gifford, Illusory correlation in interpersonal perception, *Journal of Experimental
  Social Psychology* (1976).
* S. T. Fiske, A. J. C. Cuddy, P. Glick and J. Xu, A model of (often mixed) stereotype content, *Journal of
  Personality and Social Psychology* 82(6) (2002).
* A. G. Greenwald, D. E. McGhee and J. L. K. Schwartz, Measuring individual differences in implicit cognition: the
  implicit association test, *Journal of Personality and Social Psychology* 74(6) (1998); A. G. Greenwald and C. K.
  Lai, Implicit social cognition, *Annual Review of Psychology* 71 (2020).
* A. G. Greenwald et al., Understanding and using the Implicit Association Test III, *Journal of Personality and
  Social Psychology* 97(1) (2009); F. L. Oswald, G. Mitchell, H. Blanton, J. Jaccard and P. E. Tetlock, Predicting
  ethnic and racial discrimination, *Journal of Personality and Social Psychology* 105(2) (2013).
* P. S. Forscher et al., A meta-analysis of procedures to change implicit measures, *Journal of Personality and
  Social Psychology* 117(3) (2019) 522-559.
* M. Bertrand and S. Mullainathan, Are Emily and Greg more employable than Lakisha and Jamal?, *American Economic
  Review* 94(4) (2004) 991-1013; L. Quillian, D. Pager, O. Hexel and A. H. Midtbøen, Meta-analysis of field
  experiments shows no change in racial discrimination in hiring over time, *PNAS* 114(41) (2017).
* C. M. Steele and J. Aronson, Stereotype threat and the intellectual test performance of African Americans,
  *Journal of Personality and Social Psychology* 69(5) (1995); P. R. Sackett, C. M. Hardison and M. J. Cullen,
  *American Psychologist* 59(1) (2004); P. C. Flore, J. Mulder and J. M. Wicherts, *Comprehensive Results in
  Social Psychology* 3(2) (2018) 140-174; P. C. Flore and J. M. Wicherts, a meta-analysis, *Journal of School
  Psychology* (2015).
* G. W. Allport, *The Nature of Prejudice* (1954); T. F. Pettigrew and L. R. Tropp, A meta-analytic test of
  intergroup contact theory, *Journal of Personality and Social Psychology* 90(5) (2006); E. L. Paluck, S. A. Green
  and D. P. Green, The contact hypothesis re-evaluated, *Behavioural Public Policy* 3(2) (2019) 129-158.
* E. L. Paluck, Reducing intergroup prejudice and conflict using the media: a field experiment in Rwanda, *Journal
  of Personality and Social Psychology* (2009); E. L. Paluck, R. Porat, C. S. Clark and D. P. Green, Prejudice
  reduction: progress and challenges, *Annual Review of Psychology* 72 (2021) 533-560.
* E. H. Chang, K. L. Milkman et al., The mixed effects of online diversity training, *PNAS* (2019).
* M. J. LaCour and D. P. Green, When contact changes minds, *Science* (2014), retracted 2015; D. Broockman and J.
  Kalla, Durably reducing transphobia: a field experiment on door-to-door canvassing, *Science* 352 (2016) 220-224.
* B. K. Payne, H. A. Vuletich and K. B. Lundberg, The bias of crowds, *Psychological Inquiry* 28(4) (2017); P.
  Connor and E. R. K. Evers, The bias of individuals (in crowds), *Perspectives on Psychological Science* (2020).
* M. R. Banaji and A. G. Greenwald, *Blindspot* (2013).

## Problems and solutions

1. **Tajfel's matrix.** The joint total (7 + j) + (1 + 2j) = 8 + 3j and the ingroup's 7 + j both rise with j, so
   both are maximized at j = 12 (19 and 25). The lead (7 + j) − (1 + 2j) = 6 − j is largest at j = 0 (7 and 1).
   Equality needs 7 + j = 1 + 2j, so j = 6 (13 and 13). A chooser who moves left of the right end is trading
   points for the ingroup, and for everyone, against a lead.
2. **The illusory correlation.** A's undesirable share is 8/26 = 0.31 whatever b is. B's remembered share is
   4(1 + b)/(9 + 4(1 + b)), which is 0.31 at b = 0 and rises with b: 0.42 at b = 0.6, 0.47 at b = 1.
3. **The list experiment.** The treatment count is C + Z with C the control count and Z the sensitive item, so its
   mean is E[C] + π and the difference in means has expectation π. With independent arms of n, the variance is
   (Var(C) + Var(C + Z))/n = (2 Σ p_j(1 − p_j) + π(1 − π))/n: the control items' variance enters twice, which is
   the price of privacy.
4. **Attenuation.** Write the measure X = T + E with E independent of T and of the behaviour Y. Then
   Cov(X, Y) = Cov(T, Y) = r SD(T) SD(Y), and Corr(X, Y) = r SD(T)/SD(X) = r √ρ_xx, since ρ_xx = Var(T)/Var(X) is
   the reliability. With extra noise in Y the correlation is smaller still.
5. **Sizing an audit.** n = (1.96 + 0.84)² (0.096 × 0.904 + 0.064 × 0.936)/(0.032)² ≈ 1,125 per group.
6. **The ladder.** With shares 1 − s and s, normal scores shifted by δ for the advantaged group, and a fraction k
   promoted, the cut-off c solves (1 − s) Q(c − δ) + s Q(c) = k, where Q is the normal upper tail, and the new share
   is s Q(c)/k. Since Q(c − δ) > Q(c) for δ > 0, the promoted fraction of the disadvantaged group, Q(c), is below k,
   so s Q(c)/k < s at every level.
7. **★ Evaluating a training.** Randomize the training across teams (not individuals, who share hiring
   decisions), measure behaviour (who is interviewed, offered and promoted, from records) for at least a year, and
   attitudes as a secondary outcome. With a 2-point difference in an offer rate near 20% and a design effect from
   clustering, the number of teams needed follows from the power calculation of chapter six inflated by the design
   effect; preregister the outcomes before the data arrive.

## Open checks

Checked against the articles, their abstracts or official pages, or named secondary summaries of them
(2026-11-16): Tajfel's biography (captured in 1940, a prisoner of war, his work with orphans, Bristol from 1967);
the 1971 studies' ages, groups and allocations; Balliet, Wu and De Dreu's 212 studies, d = 0.19 and 0.42; Robbers
Cave's 22 boys, Eagles and Rattlers and superordinate goals; Middle Grove and Perry's archive; Hamilton and Gifford's
group sizes and ratio; the stereotype content model; Greenwald et al.'s r = .236 and .117; Oswald et al.'s
conclusion; retest near .5 and internal consistency near .8 (Greenwald and Lai, as summarized); Forscher et al.'s
492 studies and 87,418 people; Bertrand and Mullainathan's cities, 50% and about 10 against 15 résumés per callback;
Quillian et al.'s 28 studies, 55,842 applications, 1989 to 2015, 36% and 24% (as quoted by the Russell Sage
Foundation); Sackett et al.'s point about the SAT adjustment; Flore, Mulder and Wicherts's 2,064 pupils; Allport's
conditions; Pettigrew and Tropp's more than 500 studies; Paluck, Green and Green's 27 studies; Paluck's Rwandan
experiment; Paluck et al.'s 418 experiments; Chang et al.'s 3,016 employees; the LaCour and Green retraction;
Broockman and Kalla's ten points, ten-minute conversations and non-transgender canvassers; Payne et al. and Connor
and Evers.

Still to recheck against the full texts before the final cut:

* The number of boys and of matrices in Tajfel et al. (1971), which the film does not state.
* That the Robbers Cave boys burned a flag, and that staff provoked conflict (Perry's account), from secondary
  summaries.
* The steep fall in expressed prejudice over the second half of the twentieth century, stated without numbers.
* The placebo topic (recycling) and the exact duration (three months) in Broockman and Kalla (2016).
* That meta-analyses of stereotype threat found signs of publication bias (Flore and Wicherts 2015), stated without
  numbers.
* The callback rates 9.6% and 6.4% are illustrative; the film says so.
