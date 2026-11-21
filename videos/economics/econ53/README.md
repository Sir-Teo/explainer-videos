# Economics, Built: Part 53, Information and Persuasion

Part 53 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act X, *The Graduate Core*. It asks how someone who controls only what
others learn gets them to do what she wants. Its answer: by choosing what they will learn, and committing to it. An
investigation splits the audience's beliefs so that, on average, they remain right, but they land where the audience
acts as the designer wants: just past the threshold, never wasted beyond it. Without commitment, talk carries only as
much information as interests are aligned; with many receivers, the designer can coordinate them; and everything rests
on what people infer from what they see, which in practice is less, and less reliable, than the theory assumes.

It opens on Kamenica and Gentzkow's prosecutor: 30% of defendants are guilty, the judge convicts only if guilt is more
likely than not, and the prosecutor cannot lie but chooses the investigation. No investigation convicts nobody; a
perfect one convicts the 30 guilty; one that flags every guilty defendant and 30 of the 70 innocent ones convicts 60,
with the judge following the evidence every time. From there it covers:

- Play it: which share of innocent defendants should the investigation flag (0, 20%, 3 in 7, 60%)? Three in seven:
  the judge's belief after a flag is exactly one half and 60% are convicted; one step further and the flag means
  nothing;
- Bayesian games after Harsanyi: a Cournot duopoly in which firm 1 does not know whether firm 2's cost is 4 or 1
  (firm 1 makes 2.83, between the 2.33 and 3.33 it would make if it knew; firm 2 makes 1.58 or 3.08; knowing would be
  worth 8.28 against 8.03);
- beliefs on and off the path: perfect Bayesian equilibrium, Cho and Kreps's beer and quiche, two pooling equilibria,
  and the intuitive criterion that keeps beer and drops quiche;
- cheap talk after Crawford and Sobel: partition equilibria with 5, 3, 2 and 1 messages at biases of 0.02, 0.05, 0.1
  and 0.25 (at 0.05 the messages split at 0.13 and 0.47), and the decision maker's loss rising, with a kink at each lost message, to babble;
- Bayesian persuasion: beliefs split into posteriors that average to the prior; the concave closure of the sender's
  value (0.6 at the prior of 0.3); a judge with a middle verdict (0.45); three states by linear programming;
- information design for many receivers after Bergemann and Morris: two investors, a project good 40% of the time;
  telling nothing gets no investment, telling everything 0.8 investors on average, the best obedient recommendation
  (invest whenever good and two times in three when bad) 1.6;
- Blackwell's order: an experiment and its garbling, a third that cannot be ranked against the first, and their values
  to bold and cautious decision makers;
- an intermission film of what American households expected inflation to be over the next year (the University of
  Michigan's median, peaking at 10.4% in 1980) against what it was, 1978-2026, as lines and a tune;
- common knowledge: Aumann's agreement theorem; Geanakoplos and Polemarchakis's dialogue (1/3, 1/2, 1/3, 1/3);
  Rubinstein's email game, where each general believes with probability 0.53 that the other saw one message fewer and
  nobody ever attacks;
- global games after Carlsson and van Damme and Morris and Shin: the regime falls below a strength of 0.6 when attacking
  costs 0.4; with sharp public information, three equilibria again;
- herds after Banerjee and Bikhchandani, Hirshleifer and Welch: with hints right 70% of the time, 84.5% of queues end
  on the better choice and 15.5% on the worse for ever, exactly and in 20,000 simulated queues;
- reputation: Selten's chain-store paradox and Kreps and Wilson's resolution, with a 5% chance of a tough store
  deterring entry in all but the last 4 of 20 towns;
- bargaining: Nash's axioms, Rubinstein's alternating offers (shares from 2/3 to about 1/2 as patience rises), and a
  seller who cannot commit (price 0.52 now and 0.4 later, the low-value buyer waiting half the time, profit 0.42 against
  0.5 with commitment);
- relational contracts after Bull and Levin: a self-enforcing bonus buys effort 2 delta theta / c, as good as a
  contract from delta = 1/2;
- the Dials: the depth of strategic reasoning (one to two steps, four for newspaper readers), and DellaVigna and
  Kaplan's persuasion rate for Fox News (3 to 8% of viewers not already Republican);
- in practice (ratings, disclosure, stress tests, central-bank statements, platforms) and *Called it?* on the 2006
  triple-A ratings of mortgage securities (wrong); a frontier of robust design (a prosecutor unsure of the judge's
  standard gives up 60% for a sure 55%) and learning, inattentive and algorithmic receivers.

## Build it

```bash
python -m videos.economics.econ53.compute              # every number (under a minute), into .cache/econ53/
python tools/qa_scene.py econ53 Persuasion             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ53 -q l   # the whole part, silent preview
python tools/build.py econ53                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 53                     # the lab
```

The only data are the University of Michigan's median expected inflation and the CPI, via FRED, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md); every other number is computed.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The prosecutor's arithmetic | Three investigations; the question; objectives |
| 1 | Play it: design the investigation | Four designs; convictions and the judge's belief; Bayes's rule |
| 2 | Bayesian games | Harsanyi's types; Cournot with an unknown rival; the value of knowing |
| 3 | Beliefs on and off the path | Perfect Bayesian equilibrium; beer or quiche; the intuitive criterion |
| 4 | Cheap talk | Crawford and Sobel's partitions; loss by bias |
| 5 | Bayesian persuasion | Splitting beliefs; the concave closure; a middle verdict |
| 6 | Information design for many | Two investors; three policies; Bayes correlated equilibrium |
| 7 | Blackwell's order | Garblings; experiments that cannot be ranked |
| — | Intermission | Expected against actual inflation, 1978-2026, as lines and a tune; the story so far |
| 8 | Common knowledge | Aumann; the dialogue to agreement; the email game |
| 9 | Global games | The threshold; precise public information |
| 10 | Herds and cascades | Queues; the exact chain; accuracy by hint quality |
| 11 | Reputation | The chain-store paradox; Kreps and Wilson's equilibrium |
| 12 | Bargaining | Nash; Rubinstein; Coase and delay |
| 13 | Relational contracts | The self-enforcing bonus; effort by patience |
| 14 | The Dials: how deeply people reason | The reasoning-depth dial; the persuasion rate |
| 15 | In practice: designing what people learn | Information designers; *Called it?* (wrong) |
| 16 | Frontier: robust design, learning receivers | A robust prosecutor; open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 54, *Estimating Models* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's information and persuasion module
(`explainer.economics.agora.persuade`) and the Island's Part 53 truths; the narration states the cached numbers.

- **Persuasion.** The prosecutor in closed form; convictions over a grid of 201 flag rates; concave closures by the
  upper convex hull on 401 beliefs; three states by linear programming over a grid of posteriors (multiples of 1/30).
- **Cheap talk.** The uniform-quadratic model's boundaries a_i = i/N + 2 b i (i - N), at the largest feasible N.
- **Bayes-Nash.** Linear demand P = 10 - Q; firm 1's cost 2; firm 2's 4 or 1, equally likely; closed forms.
- **Beer or quiche.** 90% strong; breakfast worth 1, avoiding a duel 2; the bully duels when weak is more likely.
- **Information design.** Investing pays 1 (good, 40%) or -3 (bad), plus 1 if the other invests; the designer
  maximizes expected investment over obedient recommendations by linear programming.
- **Blackwell.** P = [[0.9, 0.1], [0.2, 0.8]], its garbling by [[0.8, 0.2], [0.3, 0.7]], R = [[0.99, 0.01],
  [0.55, 0.45]]; garbling feasibility by linear programming; values for threshold decision makers with a prior of 1/2.
- **Common knowledge.** Nine equally likely states; Ann's partition {1-3}, {4-6}, {7-9}; Bob's {1-4}, {5-8}, {9}; the
  event {3, 4}; the true state 1.
- **Global games.** Cost 0.4, private noise 0.1, public signals of s.d. 0.4, 0.2 and 0.158 around 0.5.
- **Cascades.** Hints right 70% of the time; the net count of revealed hints as a Markov chain absorbed at plus or
  minus 2; 20,000 simulated queues of 30.
- **Reputation.** 20 towns; a 5% chance of a tough store; entrants gain 0.5 if accommodated and lose 0.5 if fought.
- **Bargaining and relational contracts.** Rubinstein's closed form; Nash on the quarter circle; the two-period seller
  with values 1 and 0.4, discount 0.8; effort worth e and costing e^2/2.

## Problems and solutions

**1.** *The prosecutor: with a prior of 0.4 and a judge who convicts at 0.6, design the best investigation. What
share is convicted?*

*Solution.* Flag every guilty defendant and a share p of the innocent, chosen so that the belief after a flag is
exactly 0.6: 0.4 / (0.4 + 0.6 p) = 0.6 gives p = 4/9. The share convicted is 0.4 + 0.6 x 4/9 = 2/3, which is the prior
divided by the threshold, as in the film (0.3/0.5 = 0.6).

**2.** *Concavification: a sender gets 1 if the receiver's belief is at least 0.75 and nothing otherwise. Find her best
value at a prior of 0.3, and the split that achieves it.*

*Solution.* The concave closure is the straight line from (0, 0) to (0.75, 1), then flat at 1. At 0.3 it is
0.3/0.75 = 0.4. It is achieved by splitting the prior between posteriors 0 and 0.75 with weights 0.6 and 0.4, which
average to 0.3.

**3.** *Cheap talk: with b = 0.1, find the boundaries of the two-message equilibrium, and the decision maker's
expected loss.*

*Solution.* With N = 2, a_1 = 1/2 + 2 b (1)(1 - 2) = 0.5 - 0.2 = 0.3, so the messages say "below 0.3" and "above". The
decision maker's loss is the variance within each interval, weighted: (0.3^3 + 0.7^3)/12 = 0.370/12 = 0.031, against
1/12 = 0.083 with no information.

**4.** *Bayes-Nash: in the Cournot example, show that firm 1's quantity is (a - 2c_1 + E c_2)/3.*

*Solution.* Each type of firm 2 best-responds to firm 1: q_2(c) = (a - c - q_1)/2. Firm 1 best-responds to the
average: q_1 = (a - c_1 - E q_2)/2, with E q_2 = (a - E c_2 - q_1)/2. Substituting, 4 q_1 = 2a - 2c_1 - a + E c_2 + q_1,
so q_1 = (a - 2c_1 + E c_2)/3: with a = 10, c_1 = 2 and E c_2 = 2.5, q_1 = 2.83.

**5.** *Beer or quiche: explain why the quiche equilibrium fails the intuitive criterion.*

*Solution.* In it, both types eat quiche and are not fought: the strong get 2, the weak 3. A switch to beer could at
best (no duel) give the strong 1 + 2 = 3, more than 2, and the weak 0 + 2 = 2, less than 3. So only the strong could
gain; the bully should believe a beer drinker strong and not fight; but then the strong would switch, so the
equilibrium does not survive.

**6.** *Common knowledge: in the nine-state dialogue, show what Ann's first announcement tells Bob.*

*Solution.* Ann says 1/3. She would have said 1/3 in states 1 to 3 (one of the three, state 3, is in the event) and in
states 4 to 6 (state 4), but 0 in states 7 to 9. So her announcement tells Bob the state is between 1 and 6. Bob's cell
{1, 2, 3, 4} lies inside, so he says 2/4 = 1/2, which tells Ann the state is 1 to 4; she still says 1/3, which rules out
4 (where she would have said 1); and Bob, left with {1, 2, 3}, says 1/3.

**7.** *The global game: show that the marginal speculator's belief about the share attacking is uniform, and derive
theta* = 1 - c.*

*Solution.* With a flat prior, theta given the signal x* is normal with mean x* and s.d. sigma. The share attacking at
strength theta is A(theta) = Phi((x* - theta)/sigma), which, given x*, is Phi of a standard normal: uniform on (0, 1).
The regime falls when A(theta) >= theta, that is when theta <= theta*, where A(theta*) = theta*. So
Pr(fall | x*) = Pr(A >= theta*) = 1 - theta*, and indifference sets this equal to c: theta* = 1 - c.

**8.** *Cascades: with hints right with probability q, show that a cascade on the better choice eventually forms with
probability q^2/(q^2 + (1 - q)^2).*

*Solution.* Before a cascade each choice reveals its hint, so the net count d moves up with probability q and down
with 1 - q, and a cascade starts at d = 2 or -2. Let p_d be the chance of reaching +2 first. Then p_1 = q + (1 - q) p_0,
p_-1 = q p_0, and p_0 = q p_1 + (1 - q) p_-1 = q^2 + 2q(1 - q) p_0, so p_0 = q^2/(1 - 2q(1 - q)) = q^2/(q^2 + (1 - q)^2):
0.845 for q = 0.7.

## Lab and interactive

- `python -m videos.economics.labs 53`: the prosecutor's design and its concave closure; cheap talk by bias; the
  Bayes-Nash Cournot quantities; the best Bayes correlated equilibrium for the investors; a garbling check; the dialogue;
  the global game's thresholds; cascades exactly and simulated; the chain store; bargaining; relational effort.
- The interactive (course site): persuade. The reader designs the investigation for a judge with a prior and a standard
  of their choosing and watches the judge's beliefs and the convictions.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[53]`; the reasoning-depth dial is in
`explainer/economics/dials.py`; the 2006 ratings are a *Called it?* entry (`explainer/economics/calls.py`); the
inflation expectations are in the Data Room. Checked on 2026-11-21: DellaVigna and Kaplan's Fox News persuasion rates
(3 to 8% of non-Republican viewers on inclusive audience measures, 11 to 28% on narrower ones); the Financial Crisis
Inquiry Commission's and the Senate subcommittee's accounts of the downgrades of 2006's triple-A mortgage securities
(stated without a figure, since the sources' figures differ by measure). The models are stated from the papers cited
in the chapters (Nash 1950, Blackwell 1953, Harsanyi 1967-68, Coase 1972, Aumann 1976, Selten 1978, Crawford and Sobel
1982, Geanakoplos and Polemarchakis 1982, Kreps and Wilson 1982, Milgrom and Roberts 1982, Rubinstein 1982 and 1989,
Bull 1987, Cho and Kreps 1987, Banerjee 1992, Bikhchandani, Hirshleifer and Welch 1992, Carlsson and van Damme 1993,
Morris and Shin 1998, Levin 2003, Bergemann and Morris 2005 and 2016, Kamenica and Gentzkow 2011) and computed here.
