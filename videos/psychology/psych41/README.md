# Psychology, Built: Part 41, Psychosis, Addiction and Development

The part opens with the care card: this is education, not diagnosis or treatment, and here is where help is found.
Then a mask of a face, seen from behind, looks like an ordinary face bulging outward to almost everyone: a prior
strong enough to overrule both eyes. In small studies, many people with schizophrenia see it as hollow. The part
uses the series' own models as a language for three kinds of condition: perception and belief with priors weighted
wrongly, learning systems captured by a drug, and brains that develop along a different path.

The viewer judges shaded discs as bumps or dents (light from above) and predicts four numbers. Then schizophrenia's
three kinds of symptom, its course and four identical sisters; chlorpromazine, the dose that follows D2 binding, and
the revised dopamine hypothesis; aberrant salience, computed; the hollow mask on a Gaussian observer, conditioned
hallucinations on a learner, and the puzzle of priors too weak and too strong; causes (twin heritability, hundreds of
small genetic effects, C4 and pruning, cannabis, cities and migration, and the "schizophrenogenic mother");
addiction's four mechanisms, wanting without liking and steep discounting; Redish's model of a prediction error that
cannot be learned away, computed, and the blocking test it failed; Rat Park, the Vietnam veterans and contingency
management; autism's histories, the vaccine fraud, priors as a trade-off (computed), rising diagnoses and
facilitated communication; ADHD, relative age and the MTA trial; and three dials that recur across diagnoses.

## Where the numbers come from

| What | Source |
|---|---|
| The hollow mask on a Gaussian observer: prior at +1, stereo signal at -1 with precision 4; the chance of seeing a face against the prior's precision (one half where the precisions are equal), and in two simulated groups of 2,000 with log-normal prior precision (medians 8 and 3): 86% and 37% see a face | Psyche (`clinic.hollow_mask`), item `mask` |
| The expected squared error of a prior's estimate when the world matches it 95% or 60% of the time: best prior precision 5.0 and 0.6 | Psyche (`clinic.prior_tradeoff`), item `mask` |
| Conditioned hallucinations: a light with a threshold tone, less often in each of four blocks of 30 trials; 200 learners with prior weight 0.3 hear a tone on 11% of silent trials, with weight 1.5 on 24% | Psyche (`clinic.conditioned_hallucinations`), item `halluc` |
| Aberrant salience: 20 cues, one rewarded, 2,000 Rescorla-Wagner trials; with dopamine bursts on 0, 10, 20 and 30% of trials, 0, 0, 4 and 15 irrelevant cues end above 0.25 (the run with the median count of 21) | Psyche (`clinic.aberrant_salience`), item `salience` |
| Redish's model: a natural reward's value settles at 1 (at 0 with a cost of 1); a drug (reward 0.5, surge 0.2) reaches 6.3 after 300 uses, and 6.0 with a cost of 1 | Psyche (`clinic.redish`), item `redish` |
| Hyperbolic discounting with k = 0.01 and 0.05 a day: 100 later beats 50 now until a delay of 100 and 20 days | Psyche (`clinic.discount`), item `discount` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

Schematic panels (the hollow-mask group pictures, the onset curve, the dose and binding cloud, the liability
threshold, wanting and liking, the MTA bars) are labelled as schematic on screen. The autism surveillance rates and
the relative-age diagnosis rates are the published values.

## Built in this part

* `explainer/psychology/psyche/clinic.py` gains the hollow mask on a Gaussian observer, the trade-off of a prior's
  strength, conditioned hallucinations, aberrant salience, Redish's non-compensable drug signal and hyperbolic
  discounting. Tested in `tests/psychology/test_clinic.py`.
* The Ledger gains eight rows; the deferred declarations of Parts 10, 16 and 17 about addiction are resolved.
* The course's interactive is shading on you: discs lit from different directions, judged as bumps or dents, and
  set against what a prior that light comes from above predicts.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| People with schizophrenia are less often fooled by the hollow-mask illusion than other people | Emrich 1989 | replicated |
| Antipsychotic drugs reduce the positive symptoms of schizophrenia and prevent relapse better than placebo | Delay and Deniker 1952 | replicated |
| People who hear voices weight prior expectations more heavily, and so are more prone to conditioned hallucinations | Powers, Mathys and Corlett 2017 | contested |
| Rats housed in a large, social, enriched colony drink far less morphine than rats housed alone | Alexander, Coambs and Hadaway 1978 | contested |
| Paying people for drug-free urine samples increases abstinence during treatment | Higgins and colleagues 1991 | replicated |
| The measles, mumps and rubella vaccine causes autism | Wakefield and colleagues 1998 | retracted |
| Non-speaking autistic people can communicate fluent thoughts by typing with a facilitator steadying their hand | Biklen 1990 | failed |
| Stimulant medication reduces the symptoms of ADHD in children more than behavioural treatment alone | MTA Cooperative Group 1999 | replicated, smaller |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Gregory; Rosenthal; Seeman and
colleagues, Creese, Burt and Snyder; Howes and Kapur; Kapur; Sterzer and colleagues; Sullivan, Kendler and Neale,
Trubetskoy and colleagues, Sekar and colleagues; Marconi and colleagues; Fromm-Reichmann; Robinson and Berridge;
Redish; Panlilio and colleagues; Robins; Kanner and Asperger; Pellicano and Burr; the CDC's surveillance network;
Faraone and Larsson; Layton and colleagues.

## Build it

```bash
python -m videos.psychology.psych41.compute            # every number (a few seconds)
python tools/qa_scene.py psych41 Inference             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych41 -q l   # the whole part, silent preview
python tools/build.py psych41                          # 1080p30 with narration
python tools/qa_scene.py psych41 Redish --lang zh      # the Chinese edition of one chapter
python tools/make.py psych41                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 41                    # the lab: masks, priors, voices, salience, drugs, delays
python tools/check_ledger.py psych41                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's clinic module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The face that is not there | The care card; the hollow mask; not everyone is fooled; the question; objectives |
| 1 | On you: bumps, dents, and four numbers | Shaded discs and the light-from-above prior; four predictions |
| 2 | Schizophrenia | Three kinds of symptom; course, and four sisters |
| 3 | Dopamine | A drug from surgery; the dose follows the receptor; version three |
| 4 | Aberrant salience | When everything seems to mean something; salience, computed |
| 5 | Perception and hallucination as inference | The hollow mask, computed; hearing what is expected; conditioned hallucinations; too weak and too strong |
| 6 | Causes | Many genes, each tiny; environments that raise risk; a theory that did harm |
| 7 | From use to compulsion | Four mechanisms; wanting without liking; now or later |
| 8 | Addiction as learning gone wrong | An error that never goes away; the model, computed; a prediction, tested |
| 9 | Cages, wars and vouchers | Rat Park; coming home; paying for clean samples |
| 10 | Autism | Two first descriptions; a fraud; a world too real; more diagnoses; whose words? |
| 11 | ADHD | What it is; the youngest in the class; the largest trial |
| 12 | Across the diagnoses | Three dials, many diagnoses |
| 13 | The Ledger | Eight rows and the tally |
| 14 | In practice: services, trade-offs and harm reduction | What helps |
| 15 | Frontier: precision, polygenic scores and new drugs | Three frontiers; open questions |
| | Recap, problems, and the road ahead | Your numbers; eleven lines; Kant's three objections; payoffs; problems; references; Part 42 |

## Sources

* R. L. Gregory, Knowledge in perception and illusion, *Philosophical Transactions of the Royal Society B* 352
  (1997) 1121-1127, and *Eye and Brain* (5th edition, 1997); H. M. Emrich (1989); U. Schneider et al. (2002); D.
  Dima et al. (2009): see the Ledger row.
* E. Bleuler, *Dementia Praecox oder Gruppe der Schizophrenien* (1911; the term from 1908); D. Rosenthal (ed.),
  *The Genain Quadruplets* (Basic Books, 1963).
* J. Delay, P. Deniker and J. M. Harl (1952); P. Seeman, T. Lee, M. Chau-Wong and K. Wong, Antipsychotic drug doses
  and neuroleptic/dopamine receptors, *Nature* 261 (1976) 717-719; I. Creese, D. R. Burt and S. H. Snyder, Dopamine
  receptor binding predicts clinical and pharmacological potencies of antischizophrenic drugs, *Science* 192 (1976)
  481-483; O. D. Howes and S. Kapur, The dopamine hypothesis of schizophrenia: version III, *Schizophrenia
  Bulletin* 35 (2009) 549-562; S. Leucht et al. (2012, 2017).
* S. Kapur, Psychosis as a state of aberrant salience, *American Journal of Psychiatry* 160 (2003) 13-23.
* A. R. Powers, C. Mathys and P. R. Corlett (2017); E. Kafadar et al. (2022); P. Sterzer et al., The predictive
  coding account of psychosis, *Biological Psychiatry* 84 (2018) 634-643.
* P. F. Sullivan, K. S. Kendler and M. C. Neale, Schizophrenia as a complex trait, *Archives of General Psychiatry*
  60 (2003) 1187-1192; V. Trubetskoy et al., Mapping genomic loci implicates genes and synaptic biology in
  schizophrenia, *Nature* 604 (2022) 502-508; A. Sekar et al., Schizophrenia risk from complex variation of
  complement component 4, *Nature* 530 (2016) 177-183; A. Marconi, M. Di Forti, C. M. Lewis, R. M. Murray and
  E. Vassos, Meta-analysis of the association between the level of cannabis use and risk of psychosis, *Schizophrenia
  Bulletin* 42 (2016) 1262-1269; F. Fromm-Reichmann, Notes on the development of treatment of schizophrenics by
  psychoanalytic psychotherapy, *Psychiatry* 11 (1948) 263-273.
* T. E. Robinson and K. C. Berridge, The neural basis of drug craving: an incentive-sensitization theory of
  addiction, *Brain Research Reviews* 18 (1993) 247-291; A. D. Redish, Addiction as a computational process gone
  awry, *Science* 306 (2004) 1944-1947; L. V. Panlilio, E. B. Thorndike and C. W. Schindler, Blocking of
  conditioning to a cocaine-paired stimulus, *Pharmacology Biochemistry and Behavior* 86 (2007) 774-777.
* B. K. Alexander et al. (1978); B. F. Petrie (1996); L. N. Robins, *The Vietnam Drug User Returns* (1974), and
  L. N. Robins, Vietnam veterans' rapid recovery from heroin addiction, *Addiction* 88 (1993) 1041-1054; S. T.
  Higgins et al. (1991); M. Prendergast et al. (2006).
* L. Kanner, Autistic disturbances of affective contact, *Nervous Child* 2 (1943) 217-250; H. Asperger (1944); H.
  Czech, Hans Asperger, National Socialism, and "race hygiene" in Nazi-era Vienna, *Molecular Autism* 9 (2018) 29;
  B. Bettelheim, *The Empty Fortress* (1967); A. J. Wakefield et al. (1998, retracted); A. Hviid et al. (2019); E.
  Pellicano and D. Burr, When the world becomes "too real", *Trends in Cognitive Sciences* 16 (2012) 504-510;
  M. J. Maenner et al., Prevalence and characteristics of autism spectrum disorder among children aged 8 years,
  *MMWR Surveillance Summaries* 72 (2023); D. Biklen (1990); D. L. Wheeler et al. (1993); J. W. Jacobson et al.
  (1995).
* S. V. Faraone and H. Larsson, Genetics of attention deficit hyperactivity disorder, *Molecular Psychiatry* 24
  (2019) 562-575; T. J. Layton, M. L. Barnett, T. R. Hicks and A. B. Jena, Attention deficit-hyperactivity disorder
  and month of school enrollment, *New England Journal of Medicine* 379 (2018) 2122-2130; MTA Cooperative Group
  (1999); P. S. Jensen et al. (2007); S. Cortese et al. (2018).
* U. Frith, *Autism: Explaining the Enigma* (2nd edition, 2003).

## Problems and solutions

1. **The hollow mask.** The hollow mask: a prior at $+1$ with precision 6 meets a stereo signal at $-1$ with precision 4. Find the posterior mean. Is a face seen? At what prior precision is the posterior exactly 0?

   *Solution.* The posterior mean is (6 × 1 + 4 × (-1)) / (6 + 4) = 0.2 > 0: a face is seen. It is exactly
   0 when the prior precision equals the eyes' precision, 4.
2. **The best prior.** The expected error of a prior with weight $w$ is $(1 - w)^2/\pi_e + (1 - p)(2w)^2$. Find the best $w$, and the best prior precision, for $\pi_e = 4$ and $p = 0.95$, then $p = 0.6$.

   *Solution.* Setting the derivative of (1 - w)²/π_e + 4(1 - p)w² to zero gives
   w = (1/π_e) / (1/π_e + 4(1 - p)). For π_e = 4 and p = 0.95, w = 0.25/0.45 = 0.556, and the prior precision
   w π_e / (1 - w) = 5.0. For p = 0.6, w = 0.25/1.85 = 0.135 and the precision is 0.625.
3. **Redish's bound.** In Redish's model, $\delta = \max(r - V + D, D)$. Show that $V$ grows by at least $\alpha D$ per use, and bound $V$ after 300 uses with $\alpha = 0.1$, $D = 0.2$.

   *Solution.* Since δ ≥ D whatever V is, each use adds αδ ≥ αD to V. After 300 uses,
   V ≥ 300 × 0.1 × 0.2 = 6 (Psyche's run with a cost of 1 ends at 6.0, the bound exactly, because the cost keeps δ
   at D).
4. **A reversal.** With $V = A/(1 + kD)$ and $k = 0.05$ per day, compare 50 now with 100 in 30 days, then 50 in 60 days with 100 in 90 days. What happens, and why does it matter for relapse?

   *Solution.* Now: 50 against 100/(1 + 1.5) = 40, so 50 now wins. Sixty days ahead: 50/(1 + 3) = 12.5
   against 100/(1 + 4.5) = 18.2, so the larger, later reward wins. Preferences reverse as the smaller reward comes
   close: a plan to abstain made in advance gives way when the drug is at hand.
5. **Aberrant salience.** A Rescorla-Wagner cue gets bursts of size $b$ on a share $q$ of trials and no reward. Find its average learned value. Evaluate it for $q = 0.2$, $b = 1$.

   *Solution.* At equilibrium the expected change is zero: E[δ] = 0 - V + qb = 0, so V = qb = 0.2.
6. **Relative age.** Children born in August are diagnosed with ADHD at 85.1 per 10{,}000, those born in September at 63.6. If the whole difference is due to relative age, what share of the August-born diagnoses does it account for?

   *Solution.* The excess is 85.1 - 63.6 = 21.5 per 10,000, which is 21.5/85.1 ≈ 25% of the August-born
   diagnoses.
7. ★ **Trait or state.** Design a study that could tell whether a tendency to conditioned hallucinations is a stable trait or tracks a person's current state.

   *Solution.* Run the conditioned-hallucination task repeatedly in the same people over months, alongside
   ratings of current hallucination severity, in people with and without a history of hearing voices. A trait
   predicts stable individual differences that persist when symptoms remit; a state predicts that a person's own
   score rises and falls with their symptoms. A multilevel model separates between-person from within-person
   variance (Part 47); preregister which component each account predicts.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Gregory's account of the hollow mask; Emrich (1989), Schneider et al. (2002) and Dima et al. (2009), and their
sample sizes; Bleuler's term and its date; the Genain quadruplets and Rosenthal's 1963 book; the lifetime risk of
schizophrenia (shown as "about one person in 200 to 300"); Laborit and Delay and Deniker's 1952 report; Seeman et
al. and Creese, Burt and Snyder (1976); Howes and Kapur (2009); Leucht et al. (2012, 2017) and their findings;
Kapur (2003); Powers, Mathys and Corlett (2017), its groups and findings; Kafadar et al. (2022); Sterzer et al.
(2018); Sullivan, Kendler and Neale's heritability of about 0.81; Trubetskoy et al.'s 287 loci; Sekar et al.'s C4
result; Marconi et al.'s odds of about four for the heaviest users; the urbanicity and migration findings;
Fromm-Reichmann (1948); Robinson and Berridge (1993); Redish (2004); Panlilio et al. (2007) and their blocking
result; Alexander et al. (1978) and Petrie (1996); Robins's figure of about 5% re-addicted within a year; Higgins et
al. (1991); Prendergast et al. (2006); Kanner's eleven children; Asperger's 1944 paper and Czech's 2018 history;
Bettelheim (1967); Wakefield et al. (1998), the 2010 retraction and the erasure from the register; Hviid et al.'s
657,461 children; Pellicano and Burr (2012); the CDC network's rates (1 in 150 for 2000 to 1 in 36 for 2020, and
the intermediate values plotted); Biklen (1990) and Wheeler et al. (1993); Faraone and Larsson's 0.74; Layton et
al.'s rates of 85.1 and 63.6 per 10,000; the MTA trial's 579 children and Jensen et al.'s three-year result;
Cortese et al. (2018); the 2024 approval of a muscarinic antipsychotic; the evidence on opioid substitution,
naloxone and needle exchange; and every page range in Sources.
