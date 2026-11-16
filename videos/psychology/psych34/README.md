# Psychology, Built: Part 34, Social Influence

In the summer of 1961, in the basement of Linsly-Chittenden Hall at Yale, an experimenter in a grey coat told men
who had answered a newspaper ad to give another man electric shocks, fifteen volts stronger for every mistake.
Twenty-six of the first forty went to the last switch. Milgram's study, Asch's lines and Zimbardo's prison became
the public face of psychology. This part tells each as it was run, as it was retold and as the record now shows it,
and then builds the mathematics of influence that the famous studies never had.

The shock generator as a trial strip and the psychiatrists' prediction; Sherif's moving light and Jacobs and
Campbell's decaying traditions; Asch's lines, his 36.8%, the quarter who never went along and the one ally, then
Bond and Smith's 133 studies and a 2023 replication at 33%; the viewer predicts four numbers and can take Asch's task;
Milgram's variations as a dose-response curve, Haslam, Loughnan and Perry's synthesis of 21 conditions at 43.6%,
Burger's partial replication, Perry's archives and the engaged-followership reading; the Stanford prison experiment
against Le Texier's archives and the BBC prison study; the 38 witnesses as a parable, Darley and Latané's intercom
and smoke, an algebra of diffusion, Fischer et al.'s meta-analysis and Philpot et al.'s cameras; Triplett's reels,
Zajonc's drive and the cockroaches twice, and social loafing; polarization, groupthink and its evidence, a consistent
minority and the hidden profile; Hovland's programme, the sleeper effect, the two routes of persuasion, Cialdini's
principles and the hotel towels twice. Then Psyche computes Granovetter's thresholds, DeGroot's consensus, bounded
confidence, simple and complex contagion on rewired rings, Galton's ox and the diversity identity, rounds of
influence on a guessing crowd, and a music market. The practice chapter is rooms, ratings and reach; the frontier is
contagion against homophily, algorithmic amplification and open questions.

## Where the numbers come from

| What | Source |
|---|---|
| Sherif's design: three people's estimates, alone, together and alone again (an illustration of the design, not his data) | Psyche (simulated), item `sherif` |
| Granovetter's crowd: thresholds 0 to 99 give 100 rioters; raising one threshold from 1 to 2 gives 1; thresholds drawn as normal quantiles with mean 25 jump from none to everyone at an SD of about 13 | Psyche (`social.cascade`, `cascade_curve`), item `riot` |
| DeGroot: five people, consensus 0.569 against a plain mean of 0.53; the middle person's weight 0.31 | Psyche (`social.degroot`, `influence_weights`), item `degroot` |
| Bounded confidence: 60 opinions; 7, 4 and 1 camps at eps 0.05, 0.12 and 0.30 | Psyche (`social.bounded_confidence`), item `camps` |
| Contagion on rings of 400 (degree 4): simple contagion reaches all in 99 steps on the ring and 6 on the rewired network; complex contagion fills the ring in 198 steps and stalls at its 4 seeds when rewired; rewiring 1% of ties cuts complex reach to 13% (mean of 8 rewirings) | Psyche (`social.ring_lattice`, `rewire`, `contagion`), item `contagion` |
| A guessing crowd of 144 (log scale): collective error 0.073 = average error 0.577 - diversity 0.504; the mean beats 72% of guessers; moving 40% toward the mean each round, diversity falls from 0.50 to 0.003 while the collective error stays at 0.073, and by round 4 the truth is outside every guess | Psyche (`social.crowd`, `influence_rounds`), item `crowd` |
| A music market, 48 songs, 2,700 listeners, 8 worlds of each kind: mean Gini 0.52 independent, 0.68 social; unpredictability 0.0045 against 0.0119 | Psyche (`social.music_market`), item `market` |
| Bystanders: one person helps with chance 0.85; with each helping as 0.85 N^-1, the chance anyone helps is 0.85, 0.67, 0.61, 0.59 and 0.58 for 1, 2, 5, 10 and 20 | Psyche (`social.bystanders`), item `bystanders` |
| Drive on an easy and a hard task; the information-sampling curve 1 - 0.7^k | Psyche (`social.drive`, `mentions`), item `impact` |
| Two worlds of 4,000 friend pairs with correlations 0.35 (influence) and 0.37 (a shared hidden trait) | Psyche (simulated), item `twins` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/social.py` (committed ahead of the part): Granovetter's thresholds; DeGroot
  averaging and influence weights; Hegselmann-Krause bounded confidence; ring lattices, degree-preserving rewiring
  and threshold contagion; the diversity prediction identity and rounds of influence; a cumulative-advantage
  market with Gini and unpredictability; bystanders, social impact, drive and information sampling; and, for Part
  35, an inverse planner, Kelley's cube and the Dunning-Kruger plot from noise. Tested in
  `tests/psychology/test_social.py`.
* The Ledger gains ten rows.
* The course's interactive is Asch's lines: twelve trials alone, then twelve with five scripted answers shown before
  yours, eight of them unanimous and wrong; it reports your errors in each condition.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| People often give an answer they can see is wrong when a unanimous group gives it first | Asch 1956 | replicated, smaller |
| Most ordinary people will give apparently dangerous shocks to another person when an experimenter tells them to | Milgram 1963 | not directly tested |
| Randomly assigned to be guards, ordinary students spontaneously became abusive: a role takes over the person | Zimbardo and colleagues 1971 | story and record |
| Thirty-eight neighbours watched Kitty Genovese's murder and none called the police | Gansberg (The New York Times) 1964 | story and record |
| The more bystanders there are, the less likely each one is to help | Darley and Latané 1968 | replicated |
| The presence of others improves performance on simple tasks and impairs it on complex ones | Zajonc, Heingartner and Herman 1969 | contested |
| People exert less effort on a collective task than when working alone | Latané, Williams and Harkins 1979 | replicated |
| Cohesive, insulated groups under directive leaders seek consensus and make defective decisions | Janis 1972 | contested |
| Telling guests that most guests reuse their towels increases towel reuse more than an environmental appeal | Goldstein, Cialdini and Griskevicius 2008 | contested |
| Seeing others' estimates reduces a crowd's diversity without making it more accurate | Lorenz, Rauhut, Schweitzer and Helbing 2011 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Sherif and Jacobs and Campbell,
Milgram's variations, Haslam and Reicher's readings, Triplett and Stroebe, Stoner and Moscovici and Zavalloni,
Moscovici, Lage and Naffrechoux, Stasser and Titus, Hovland's programme, Petty, Cacioppo and Goldman, Cialdini's
principles, Granovetter, DeGroot, Hegselmann and Krause, Centola, Galton, Salganik, Dodds and Watts, Muchnik, Aral
and Taylor, Bond et al., Shalizi and Thomas, and Huszár et al.

## Build it

```bash
python -m videos.psychology.psych34.compute            # every number (a few seconds)
python tools/qa_scene.py psych34 Thresholds            # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych34 -q l   # the whole part, silent preview
python tools/build.py psych34                          # 1080p30 with narration
python tools/qa_scene.py psych34 Norms --lang zh       # the Chinese edition of one chapter
python tools/make.py psych34                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 34                    # the lab: thresholds, opinions, contagion, crowds, markets
python tools/check_ledger.py psych34                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's social module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | 1961: the shock generator | The basement; the trial strip and the prods; prediction against result; the question; objectives |
| 1 | Norms and lines | Sherif's light; Asch's lines; what happened; seventy years later |
| 2 | On you: four numbers | Four predictions; Asch's task on you |
| 3 | Obedience | The variations as a curve; all the conditions at once; Burger; the archives; engaged followership |
| 4 | The prison that wasn't | The textbook version; Le Texier's record; the BBC prison study |
| 5 | Bystanders | The 38 witnesses; the intercom and the smoke; the algebra of diffusion; what cameras show |
| 6 | The presence of others | Triplett; Zajonc's drive; the cockroaches twice; social loafing |
| 7 | Groups deciding | Polarization; groupthink and its evidence; a consistent minority; the hidden profile |
| 8 | Persuasion | The Yale programme and the sleeper effect; two routes; six principles; the hotel towels twice |
| 9 | Thresholds | Granovetter's hundred; change one person; smooth crowds, sudden outcomes |
| 10 | Opinions on a network | DeGroot; bounded confidence; simple and complex contagion; how much randomness |
| 11 | The wisdom and the herd | Galton's ox; the diversity identity; influence rounds; a music market |
| 12 | The Ledger | Ten rows and the tally |
| 13 | In practice: rooms, ratings and reach | Designing the room; ratings that herd; spreading a behaviour |
| 14 | Frontier: influence at scale | Contagion or homophily; algorithmic amplification; open questions |
| | Recap, problems, and the road ahead | Your numbers; ten lines; Kant's three objections; payoffs; problems; references; Part 35 |

## Sources

* M. Sherif, A study of some social factors in perception, *Archives of Psychology* (1935); R. C. Jacobs and D. T.
  Campbell, The perpetuation of an arbitrary tradition through several generations of a laboratory
  microculture, *Journal of Abnormal and Social Psychology* (1961).
* S. E. Asch, Opinions and social pressure, *Scientific American* 193(5) (1955) 31-35; Studies of independence and
  conformity: I. A minority of one against a unanimous majority, *Psychological Monographs* 70(9) (1956).
* R. Bond and P. B. Smith, Culture and conformity, *Psychological Bulletin* (1996); A. Franzen and S. Mader, The
  power of social influence: a replication and extension of the Asch experiment, *PLOS ONE* 18 (2023) e0294325.
* S. Milgram, Behavioral study of obedience, *Journal of Abnormal and Social Psychology* 67 (1963) 371-378;
  *Obedience to Authority* (1974).
* J. M. Burger, Replicating Milgram: would people still obey today?, *American Psychologist* 64 (2009).
* N. Haslam, S. Loughnan and G. Perry, Meta-Milgram: an empirical synthesis of the obedience experiments, *PLOS ONE*
  9 (2014) e93927.
* G. Perry, *Behind the Shock Machine* (2012); G. Perry, A. Brannigan, R. A. Wanner and H. Stam, Credibility and
  incredulity in Milgram's obedience experiments, *Social Psychology Quarterly* 83 (2020) 88-106.
* S. A. Haslam and S. D. Reicher, Contesting the "nature" of conformity, *PLoS Biology* 10(11) (2012) e1001426; S. A.
  Haslam, S. D. Reicher and K. Millard, Shock treatment, *PLOS ONE* (2015).
* T. Le Texier, Debunking the Stanford Prison Experiment, *American Psychologist* 74 (2019) 823-839; S. Reicher and
  S. A. Haslam, Rethinking the psychology of tyranny: the BBC prison study, *British Journal of Social Psychology*
  45 (2006) 1-40.
* M. Gansberg, 37 who saw murder didn't call the police, *The New York Times* (27 March 1964); R. Manning, M.
  Levine and A. Collins, The Kitty Genovese murder and the social psychology of helping, *American Psychologist* 62
  (2007) 555-562.
* J. M. Darley and B. Latané, Bystander intervention in emergencies, *JPSP* 8 (1968) 377-383; B. Latané and J. M.
  Darley, Group inhibition of bystander intervention in emergencies, *JPSP* 10 (1968) 215-221.
* P. Fischer et al., The bystander-effect, *Psychological Bulletin* 137 (2011) 517-537; R. Philpot, L. S. Liebst, M.
  Levine, W. Bernasco and M. R. Lindegaard, Would I be helped?, *American Psychologist* 75 (2020) 66-75.
* N. Triplett, The dynamogenic factors in pacemaking and competition, *American Journal of Psychology* (1898); W.
  Stroebe, The truth about Triplett (1898), but nobody seems to care, *Perspectives on Psychological Science* 7
  (2012) 54-57.
* R. B. Zajonc, Social facilitation, *Science* (1965); R. B. Zajonc, A. Heingartner and E. M. Herman (1969); E.
  Halfmann, J. Bredehöft and J. A. Häusser, Replicating roaches, *Psychological Science* 31 (2020) 332-337.
* B. Latané, K. Williams and S. Harkins, Many hands make light the work (1979); S. J. Karau and K. D. Williams,
  Social loafing: a meta-analytic review (1993).
* J. A. F. Stoner, MIT master's thesis (1961); S. Moscovici and M. Zavalloni, The group as a polarizer of attitudes
  (1969); S. Moscovici, E. Lage and M. Naffrechoux, Influence of a consistent minority (1969).
* I. L. Janis, *Victims of Groupthink* (1972); S. R. Fuller and R. J. Aldag, Organizational Tonypandy,
  *Organizational Behavior and Human Decision Processes* 73 (1998) 163-184; R. S. Baron (2005).
* G. Stasser and W. Titus, Pooling of unshared information in group decision making, *JPSP* 48 (1985) 1467-1478.
* C. I. Hovland and W. Weiss, The influence of source credibility on communication effectiveness, *Public Opinion
  Quarterly* (1951); C. I. Hovland, I. L. Janis and H. H. Kelley, *Communication and Persuasion* (1953); G. T.
  Kumkale and D. Albarracín, The sleeper effect in persuasion: a meta-analytic review (2004).
* R. E. Petty, J. T. Cacioppo and R. Goldman, Personal involvement as a determinant of argument-based persuasion,
  *JPSP* 41 (1981) 847-855; R. B. Cialdini, *Influence* (1984).
* N. J. Goldstein, R. B. Cialdini and V. Griskevicius, A room with a viewpoint, *Journal of Consumer Research* 35
  (2008) 472-482; G. Bohner and L. E. Schlüter, A room with a viewpoint revisited, *PLOS ONE* 9 (2014) e104086.
* M. Granovetter, Threshold models of collective behavior, *American Journal of Sociology* 83 (1978) 1420-1443; M. H.
  DeGroot, Reaching a consensus (1974); R. Hegselmann and U. Krause, Opinion dynamics and bounded confidence,
  *JASSS* 5(3) (2002); D. Centola, The spread of behavior in an online social network experiment, *Science* 329
  (2010).
* F. Galton, Vox populi, *Nature* (7 March 1907); K. F. Wallis, Revisiting Francis Galton's forecasting competition,
  *Statistical Science* (2014); J. Lorenz, H. Rauhut, F. Schweitzer and D. Helbing, How social influence can
  undermine the wisdom of crowd effect, *PNAS* 108 (2011) 9020-9025; J. Becker, D. Brackbill and D. Centola, *PNAS*
  114 (2017) E5070-E5076.
* M. J. Salganik, P. S. Dodds and D. J. Watts, Experimental study of inequality and unpredictability in an
  artificial cultural market, *Science* 311 (2006) 854-856.
* L. Muchnik, S. Aral and S. J. Taylor, Social influence bias: a randomized experiment, *Science* 341 (2013)
  647-651; R. M. Bond et al., A 61-million-person experiment in social influence and political mobilization,
  *Nature* (2012).
* C. R. Shalizi and A. C. Thomas, Homophily and contagion are generically confounded in observational social network
  studies, *Sociological Methods & Research* 40 (2011) 211-239; F. Huszár et al., Algorithmic amplification of
  politics on Twitter, *PNAS* (2022).

## Problems and solutions

1. **Granovetter's cascade.** Let F(k) be the number of thresholds at most k. Starting from 0, the number in after
   each step is F of the number before, so the process climbs to the first fixed point k* with F(k*) = k*. For
   thresholds 0, ..., n − 1, F(k) = k + 1 for every k < n, so there is no fixed point below n and all n join. Raise
   the threshold of 1 to 2: F(0) = 1, F(1) = 1, a fixed point, and the cascade stops at one person.
2. **DeGroot's consensus.** If W is row-stochastic and primitive, Perron-Frobenius gives W^t → 1π^⊤, with π the
   unique left eigenvector for eigenvalue 1 normalized to sum to 1. So x_t = W^t x_0 → (π^⊤x_0)1. If W is doubly
   stochastic, 1^⊤W = 1^⊤, so π = 1/n and the consensus is the plain mean.
3. **The diversity identity.** Write x_i − θ = (x_i − x̄) + (x̄ − θ); square and average. The cross term averages to
   (x̄ − θ) times the average of (x_i − x̄), which is zero, so the average squared error is the diversity plus
   (x̄ − θ)².
4. **Bystanders.** With p_N = p/N, the chance that nobody helps is (1 − p/N)^N → e^{−p}, so someone helps with
   probability tending to 1 − e^{−p}. For p = 0.85 that is 0.57, against 0.85 for one person alone: much less help
   from each, somewhat less from the crowd.
5. **The hidden profile.** A fact known to all four comes up with chance 1 − 0.7⁴ = 0.76; a fact known to one, with
   chance 0.3. Shared facts are 2.5 times as likely to be discussed by arithmetic alone.
6. **Bounded confidence.** If x_i ≤ x_j, every opinion within ε of x_i but not of x_j lies below the shared window,
   and every one within ε of x_j but not x_i lies above it, so the mean of i's window is at most the mean of j's:
   order is preserved. Opinions within 2ε of one another draw together until camps sit more than ε apart, so an
   even spread on [0, 1] ends with roughly one camp per 2ε.
7. **★ Separating influence from homophily.** Randomize the treatment of one friend (for example, an invitation, a
   message or a product) and measure the other's behaviour: randomization breaks the link to any shared hidden
   trait. Without an experiment, use variation the friends do not choose (a plausibly random exposure), compare
   with sham ties (pairs who are not friends but are matched on observables), and test for "influence" on
   behaviour that could not have spread (a placebo outcome). Each check removes one route by which homophily can
   imitate contagion.

## Open checks

Checked against the articles, their abstracts or official pages, or named secondary summaries of them
(2026-11-16): Asch's 18 trials, 12 critical, 123 men, 36.8%, the quarter who never conformed and the single ally;
Bond and Smith's 133 studies in 17 countries; Franzen and Mader's 210 students, 33%, 25% and 38%; Linsly-Chittenden
Hall, the ads and 26 of 40, defiance from 300 volts and the wall-pounding at 300 and 315; the four prods; the
psychiatrists' prediction; the variations (30%, 20.5%, 47.5%, 10%) and the range 0% to 92.5%; Haslam, Loughnan and
Perry's 23 conditions, 780 people, 21 conditions, 740 people and 43.6%; Burger's 70 adults, 70% against 82.5% and
the 79%; Perry's archives, the 656 questionnaires and the improvised prods; Haslam, Reicher and Millard's restaging;
the prison study's 24 students, six days of fourteen and the coin-flip assignment; Le Texier's archives and 15
interviews; the BBC prison study's eight days and its result; the Times headline and date and the dozen witnesses;
Darley and Latané's 85%, 62% and 31%; the smoke study's 75%, 38% and 10%; Fischer et al.'s 105 effects and g =
-0.35; Philpot et al.'s 219 conflicts in three countries and nine in ten; Stroebe on Triplett; the cockroach
replication; the shouting study's 82% and 74%; Karau and Williams's 78 studies; Stoner, and Moscovici and Zavalloni's
French students; Moscovici, Lage and Naffrechoux's design and about 8%; the groupthink reviews; Stasser and Titus;
Hovland and Weiss and the sleeper effect's meta-analysis; Petty, Cacioppo and Goldman's design; the hotel towels'
1,058 chances, 44.1% and 35.1%, and Bohner and Schlüter's two hotels; Granovetter's example; Hegselmann and Krause;
Centola's 1,528 people and health forum; Galton's 787 tickets, 1,207 and 1,198, and Wallis's reanalysis; Lorenz et
al.'s 144 people; Salganik et al.'s 14,341 people and 48 songs; Muchnik et al.'s 32% and 25%; Bond et al.'s 61
million and 0.39%; Shalizi and Thomas; Huszár et al.'s six of seven countries.

Still to recheck against the full texts before the final cut:

* Asch's control condition: "almost nobody erred" is drawn as a bar of about 1%, from secondary summaries.
* The exact size of the one-ally effect ("about a quarter") and the majority-size curve, which secondary sources
  report differently; the film describes both qualitatively.
* Moscovici, Lage and Naffrechoux's inconsistent-condition figure, drawn as about 1%.
* Latané, Williams and Harkins's 82% and 74%, from secondary summaries.
* The Times's 2016 description of its own reporting as flawed, from secondary reports.
* The Princeton MusicLab data are behind a browser challenge, so the market chapter is simulated; the real worlds'
  shares would replace it if the data can be fetched by a plain request.
