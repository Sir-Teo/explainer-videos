# Psychology, Built: Part 37, Bonds and Bargains

Offer a stranger one coin out of ten, take it or both get nothing. A responder who wants only money accepts, and a
proposer who knows that offers the minimum. In the first ultimatum experiments, in 1982, proposers offered about
37%; a meta-analysis of 37 papers found 40%; and responders reject low offers, paying to refuse a split they see as
unfair. This part follows cooperation from two-person bargains to groups and societies, and then turns to the closest
bonds, where a science of attraction meets machine learning and finds how little can be predicted about a particular
couple.

The hook is the ultimatum game, its textbook prediction and what people do; the viewer plays the responder and
predicts four numbers. Then five games as experiments and the prisoner's dilemma; four routes to cooperation and a
tournament of strategies (computed); public goods that decay, punishment that sustains them (computed, with Fehr and
Gächter) and antisocial punishment across sixteen pools; inequity aversion as a utility function and the proposer's
problem (computed); the same game in fifteen small-scale societies; proximity, mere exposure and matching; stated
preferences against desire in speed dating, and machine learning that cannot predict a pair's chemistry; 11,196
couples, a divorce classifier scored in and out of sample (computed), attachment and commitment; mate preferences in
37 cultures and 45 countries; and loneliness, isolation and survival. The practice chapter is markets, teams and
dating apps; the frontier is chemistry and machines.

## Where the numbers come from

| What | Source |
|---|---|
| Inequity-averse responders: 30% with alpha = 0 and 70% with alpha spread evenly over 0.3 to 1.5; each accepts a share of at least alpha / (1 + 2 alpha); a selfish proposer's best offer is 38%, keeping an expected 62% of the sum | Psyche (`social.fs_threshold`, `ultimatum`), item `ultimatum` |
| A round-robin of seven strategies over 200 moves of the prisoner's dilemma (3, 0, 5, 1): with exact moves grim trigger scores 2.67 per move, tit for tat 2.61 and always defect 1.87; with 5% of moves flipped, tit for two tats and win-stay lose-shift lead at 2.24 | Psyche (`social.ipd_tournament`), item `tournament` |
| Public goods in 200 groups of four, ten rounds, conditional cooperators and a quarter free riders: contributions fall from 46% to 8% without punishment and rise to 75% with it | Psyche (`social.public_goods`), item `goods` |
| A divorce classifier on 56 couples and 30 variables, one weakly informative, fitted 200 times: 89% accurate on the couples it was fitted to, 56% by leave-one-out, against 66% for always guessing the commoner outcome | Psyche (`social.overfit_divorce`), item `divorce` |
| A marriage market of 200 people a side, paired by deferred acceptance, median of 50 markets: when everyone wants the most attractive partner (plus private taste, SD 0.5) partners' attractiveness correlates 0.90; when everyone wants someone like themselves, 0.91 | Psyche (`social.stable_matching`), item `market` |
| Hamilton's rule: helping pays when B/C exceeds 2 for a full sibling and 8 for a first cousin | computed, item `hamilton` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/social.py` (committed with Part 36): Fehr and Schmidt's utility and the responder's
  threshold; the proposer's problem; a public-goods game with conditional cooperators, free riders and optional
  punishment; a tournament of repeated prisoner's dilemma strategies with noise; a divorce classifier scored in and
  out of sample; a marriage market solved by Gale and Shapley's deferred acceptance. Tested in `tests/psychology/test_social.py`.
* The Ledger gains seven rows.
* The course's interactive is the ultimatum game as the responder: ten scripted offers out of ten coins; it reports
  the smallest offer you accepted throughout and where that sits among Psyche's responders.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| In the ultimatum game proposers offer far more than the minimum, and responders reject low offers at a cost to themselves | Guth, Schmittberger and Schwarze 1982 | replicated |
| When group members can punish free riders at a cost to themselves, contributions to a public good hold up instead of decaying | Fehr and Gachter 2002 | replicated |
| Repeated exposure to a stimulus increases liking for it | Zajonc 1968 | replicated |
| The partner qualities people say they want, and the sex differences in them, predict whom they come to desire when they meet | Buss 1989 | failed |
| Observing how a couple argues predicts which couples will divorce with about 90% accuracy | Gottman and colleagues 1998 | contested |
| Across cultures, men say they value physical attractiveness and youth in a partner more than women do, and women value earning prospects more | Buss 1989 | replicated |
| People with stronger social relationships are more likely to survive over follow-up periods | Holt-Lunstad, Smith and Layton 2010 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Festinger, Schachter and Back, and
Hazan and Shaver with Rusbult.

## Build it

```bash
python -m videos.psychology.psych37.compute            # every number (a few seconds)
python tools/qa_scene.py psych37 Punishment            # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych37 -q l   # the whole part, silent preview
python tools/build.py psych37                          # 1080p30 with narration
python tools/qa_scene.py psych37 Couples --lang zh     # the Chinese edition of one chapter
python tools/make.py psych37                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 37                    # the lab: ultimatum, tournament, public goods, divorce
python tools/check_ledger.py psych37                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's social module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | 1982: take it or leave it | The ultimatum game; what people do; the question; objectives |
| 1 | On you: an offer, and four numbers | An offer of two out of ten; four predictions |
| 2 | Games as experiments | Five games; the prisoner's dilemma |
| 3 | Why cooperate? | Four routes to cooperation; a tournament of strategies |
| 4 | Public goods and punishment | Ten rounds of a public good; punishing the cooperators |
| 5 | Social preferences | Inequity aversion; the proposer's problem; where the model strains |
| 6 | Fifteen societies | The same game, far from campus |
| 7 | Attraction | Who lives nearby; mere exposure; similarity, reciprocity, matching |
| 8 | What people say they want | The ideal partner and the real one; three sources of desire |
| 9 | Predicting relationships | Eleven thousand couples; ninety percent, in sample; attachment and commitment |
| 10 | Mate preferences across cultures | Thirty-seven cultures, then forty-five countries; two readings |
| 11 | Loneliness and health | 148 studies; association, or cause? |
| 12 | The Ledger | Seven rows and the tally |
| 13 | In practice: markets, teams and dating apps | Designing for cooperation; what a matching algorithm can know |
| 14 | Frontier: chemistry and machines | New players; open questions |
| | Recap, problems, and the road ahead | Your numbers; eleven lines; Kant's three objections; payoffs; problems; references; Part 38 |

## Sources

* W. Güth, R. Schmittberger and B. Schwarze, An experimental analysis of ultimatum bargaining, *Journal of Economic
  Behavior and Organization* 3 (1982) 367-388; H. Oosterbeek, R. Sloof and G. van de Kuilen, Cultural differences in
  ultimatum game experiments, *Experimental Economics* 7 (2004) 171-188.
* W. D. Hamilton, The genetical evolution of social behaviour (1964); R. Axelrod, Effective choice in the
  prisoner's dilemma (1980) and *The Evolution of Cooperation* (1984); A. Rapoport, D. A. Seale and A. M. Colman, Is
  tit-for-tat the answer?, *PLoS ONE* (2015).
* E. Fehr and S. Gächter, Altruistic punishment in humans, *Nature* 415 (2002) 137-140; B. Herrmann, C. Thöni and S.
  Gächter, Antisocial punishment across societies, *Science* 319 (2008).
* E. Fehr and K. M. Schmidt, A theory of fairness, competition, and cooperation, *Quarterly Journal of Economics*
  114(3) (1999) 817-868; J. Dana, D. M. Cain and R. M. Dawes, What you don't know won't hurt me, *Organizational
  Behavior and Human Decision Processes* (2006).
* J. Henrich, R. Boyd, S. Bowles, C. Camerer, E. Fehr, H. Gintis and R. McElreath, In search of homo economicus,
  *American Economic Review* 91 (2001) 73-78.
* L. Festinger, S. Schachter and K. Back, *Social Pressures in Informal Groups* (1950); R. B. Zajonc, Attitudinal
  effects of mere exposure, *Journal of Personality and Social Psychology Monograph* (1968); R. F. Bornstein,
  *Psychological Bulletin* 106(2) (1989); R. M. Montoya et al., *Psychological Bulletin* (2017).
* P. W. Eastwick and E. J. Finkel, Sex differences in mate preferences revisited, *Journal of Personality and Social
  Psychology* 94(2) (2008); S. Joel, P. W. Eastwick and E. J. Finkel, Is romantic desire predictable?,
  *Psychological Science* (2017); S. Joel et al., Machine learning uncovers the most robust self-report predictors of
  relationship quality across 43 longitudinal couples studies, *PNAS* 117(32) (2020).
* S. M. Kalick and T. E. Hamilton, The matching hypothesis reexamined, *Journal of Personality and Social
  Psychology* 51(4) (1986) 673-682; D. Gale and L. S. Shapley, College admissions and the stability of marriage,
  *American Mathematical Monthly* 69 (1962) 9-15.
* J. M. Gottman, J. Coan, S. Carrère and C. Swanson, *Journal of Marriage and the Family* 60 (1998); R. E. Heyman and
  A. M. Smith Slep, The hazards of predicting divorce without crossvalidation, *Journal of Marriage and Family* 63
  (2001).
* C. Hazan and P. Shaver, Romantic love conceptualized as an attachment process, *Journal of Personality and Social
  Psychology* 52(3) (1987) 511-524; C. E. Rusbult, *Journal of Experimental Social Psychology* (1980).
* D. M. Buss, Sex differences in human mate preferences, *Behavioral and Brain Sciences* 12 (1989); K. V. Walter et
  al., Sex differences in mate preferences across 45 countries, *Psychological Science* 31(4) (2020).
* J. Holt-Lunstad, T. B. Smith and J. B. Layton, Social relationships and mortality risk, *PLoS Medicine* 7(7) (2010)
  e1000316; J. Holt-Lunstad et al., *Perspectives on Psychological Science* 10(2) (2015).
* C. F. Camerer, *Behavioral Game Theory* (2003); E. J. Finkel et al., Online dating, *Psychological Science in the
  Public Interest* (2012).

## Problems and solutions

1. **The responder's threshold.** Offered s of a pie of 1, the responder gets s and the proposer 1 − s, so for
   s < 1/2 the utility is s − α(1 − 2s); rejection gives 0. Accept iff s − α(1 − 2s) ≥ 0, that is,
   s(1 + 2α) ≥ α, so s ≥ α/(1 + 2α). For α = 0.5 the threshold is 1/4; for α = 2 it is 2/5.
2. **The proposer's best offer.** With thresholds uniform on [0, 0.4], P(accept s) = s/0.4 for s ≤ 0.4, so the
   proposer maximizes (1 − s)s/0.4, whose derivative (1 − 2s)/0.4 is positive throughout [0, 0.4]: the best offer is
   0.4, with an expected share of 0.6.
3. **Defection and Grim Trigger.** Whatever the other does, defecting gives T > R or P > S, so it is dominant in one
   round. In the repeated game, cooperating forever against Grim Trigger is worth R/(1 − δ); deviating gives T now and
   P forever after, T + δP/(1 − δ). Cooperation is a best response when R/(1 − δ) ≥ T + δP/(1 − δ), that is,
   δ ≥ (T − R)/(T − P): with (5, 3, 1), δ ≥ 1/2.
4. **Hamilton's rule.** Help when rB > C, so B/C > 1/r: more than 2 for a full sibling (r = 1/2) and more than 8
   for a first cousin (r = 1/8).
5. **Fitting any couples exactly.** With p + 1 ≥ n columns in general position, the design matrix has rank n, so
   the least-squares fit can match any vector of outcomes exactly: in-sample accuracy is 100% whatever the truth.
   In-sample accuracy measures flexibility, not prediction, which is why it must be estimated on couples the model has
   not seen.
6. **An odds ratio.** Survival odds in the reference group are 0.8/0.2 = 4; times 1.5 gives 6, so the share is
   6/7 ≈ 86%: a gain of about six points, which is not "50% more likely to survive".
7. **★ Finding pair-specific compatibility.** Measure the same people with many partners (a round-robin, as in speed
   dating), and estimate actor, partner and relationship variance. Compatibility exists if a model built before
   meeting predicts the relationship component on held-out pairs: who will like whom beyond how choosy each person is
   and how desirable each partner is. Preregister the model and the held-out pairs.

## Open checks

Checked against the articles, their abstracts or official pages, or named secondary summaries of them
(2026-11-16): Güth et al.'s average offer near 37%; Oosterbeek et al.'s 37 papers and 40%; Axelrod's first tournament
(14 entries, 200 moves, Tit for Tat by Anatol Rapoport) and the second; Rapoport, Seale and Colman (2015); Fehr and
Gächter's result; Herrmann, Thöni and Gächter's 16 pools and their correlates; Henrich et al.'s 15 societies, 26% to
58% and about 44% in industrial societies; the Dana, Cain and Dawes exit; the computer-offer result (Blount, via a
secondary source); the Westgate study's design; Bornstein's 208 experiments and r = .26; Montoya et al.'s 268 curves
from 81 articles; Eastwick and Finkel's result; Joel, Eastwick and Finkel's 4-18% and 7-27%; Joel et al.'s 43
datasets, 29 laboratories, 11,196 couples, 45% and 21%; Heyman and Slep's argument; Hazan and Shaver's newspaper quiz
and about 56% secure; Buss's 10,047 people in 37 cultures; Walter et al.'s 14,399 people in 45 countries; Holt-Lunstad
et al.'s 148 studies, 308,849 people, OR 1.50 and 1.91, and 1.29 and 1.26 in 2015; Kalick and Hamilton's
1986 simulations (via secondary summaries and Grow's 2021 re-examination).

Still to recheck against the full texts before the final cut:

* Rejection rates for low ultimatum offers, stated without numbers.
* Gottman's "about 90%" figure, from secondary summaries of the 1998 paper.
* The Westgate percentages, which the film does not state.
* Rusbult's investment model (1980), cited from standard accounts.
* "Many people send and many repay" in trust games, and contributions "about half at first" in public-goods games,
  stated from the standard literature without numbers.
