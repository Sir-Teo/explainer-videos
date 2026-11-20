# Economics, Built: Part 33, Crises

Part 33 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the ninth and last of Act VI, *Money and the Cycle*. It asks why financial systems
blow up, and why it is so hard to see it coming. Its answer: finance amplifies. Debt fixed in money, net worth that
sets the cost of borrowing, collateral whose price depends on who can borrow against it, and leverage that rises in
good times and vanishes in bad ones turn small losses into large ones. And it is hard to see coming because the
warning, a credit boom, is visible but noisy: it raises the odds of a crisis several times over, yet most booms end
quietly, and the timing is hard to call.

It opens on the Queen's question at the London School of Economics on 5 November 2008, as reported "why did nobody
notice it?", and the British Academy's answer of 22 July 2009: "principally a failure of the collective imagination
of many bright people, both in this country and internationally, to understand the risks to the system as a whole".
From there it covers:

- a game: the eight largest postwar credit booms in eighteen rich countries, chosen by a rule and shown unlabelled;
  which ended in a crisis within three years? (five did);
- Kindleberger's anatomy of manias and Minsky's hedge, speculative and Ponzi borrowers, on the Island: the same
  debts at a doubled interest rate leave 48% of borrowers hedged and make 15% Ponzi;
- Fisher's debt deflation, computed, and America in 1929-33, when bank loans fell 44% yet loans to GDP rose from 48%
  to 58%; 8,812 commercial banks suspended, and Bernanke's argument that their failure destroyed information;
- the costly-state-verification contract and the financial accelerator: at leverage 2 the Island's firms pay a
  premium of 1.9% and 3.3% default; a 10% loss of net worth cuts investment 2.5%, against nothing without the friction;
- Kiyotaki and Moore's collateral cycle, solved exactly: a 1% loss for the farmers cuts their land 0.67% with the land
  price held fixed and 5.3% once it feeds back; output falls 0.74%, over twice the direct loss, and stays down;
- Geanakoplos's leverage cycle: borrowing raises the price from 0.68 to 0.75 by changing whose opinion sets it; in two
  periods the price falls from 0.95 to 0.69 on news that lowers the old marginal buyer's value by 9%, while margins
  rise from 27% to 71%; fire sales and liquidity spirals;
- 2008 in order: house prices down 27%, mortgage delinquencies from 1.4% to 11.5%, BNP Paribas, Bear Stearns,
  Lehman, AIG, the TED spread at 4.6 points, and the Fed's balance sheet from $0.93 to $2.25 trillion in fourteen
  weeks;
- an intermission without narration: bank loans to GDP across eighteen economies since 1870, with each year's
  crises, as a tune;
- households: Mian and Sufi's design on the Island's counties, with the spending response rising with leverage
  (Mian, Rao and Sufi's estimate: 5 to 7 cents per dollar of housing wealth);
- a hundred and fifty years of the Macrohistory Database: a crisis follows within three years in 18% of the fastest
  credit booms and 33% when house prices boom too, against 6% after the slowest; the Schularick-Taylor predictor
  scores 0.73 in sample but 0.56 out of sample since 1950; financial recessions leave output 7.7 points lower five
  years on than normal ones;
- your guesses scored, with the model's chances fitted only on earlier years (its ranking of the eight scores 0.60);
- fighting a crisis: Bagehot's rule, guarantees, recapitalization, the 2009 stress tests, swap lines of $583 billion
  in 2008 and $449 billion in 2020;
- macroprudential policy, with Basel III's credit-gap guide computed: it would have demanded Spain's full buffer every
  year from 1999, and on bank loans it barely moves for the United States;
- sudden stops and original sin: the peso, the baht and the won;
- two dials: the output cost of a crisis (two rows added) and the warning value of a credit boom (new); *Called it?*
  on Rajan at Jackson Hole in 2005 (right); a frontier chapter on nonlinear macro-finance and runs outside banks.

## Build it

```bash
python -m videos.economics.econ33.compute              # every number (about half a minute), into .cache/econ33/
python tools/qa_scene.py econ33 Collateral             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ33 -q l   # the whole part, silent preview
python tools/build.py econ33                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 33                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the Jordà-Schularick-Taylor Macrohistory Database
(release 6, CC BY-NC-SA 4.0), and from FRED the Case-Shiller index, mortgage delinquencies, the TED and Baa spreads,
the Federal Reserve's balance sheet and swap lines, money market funds' assets, the baht, won and peso, and the NBER's
bank suspensions.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Why did nobody notice it? | The Queen's question and the British Academy's letter; the question; objectives |
| 1 | Play it: eight credit booms | The rule; the eight booms, unlabelled; your guesses |
| 2 | The pattern: Kindleberger and Minsky | The anatomy of a mania; hedge, speculative and Ponzi borrowers on the Island |
| 3 | Debt deflation, and banks as information | Fisher's arithmetic; America 1929-33; bank suspensions and Bernanke |
| 4 | The financial accelerator | Costly verification; the premium against leverage; net worth and investment; the loop |
| 5 | Collateral cycles | Kiyotaki and Moore's model; the static and dynamic multipliers; persistence |
| 6 | Leverage, margins and fire sales | Natural buyers; the two-period leverage cycle; spirals |
| 7 | 2008 in order | Houses; where the losses sat; the run; the response |
| — | Intermission | Bank loans to GDP in eighteen economies since 1870, as a tune |
| 8 | Households: debt and spending | Leverage and losses; the Island's counties |
| 9 | A hundred and fifty years, eighteen countries | Odds by credit boom; the predictor in and out of sample; recessions |
| 10 | Your guesses, scored | The answers; the model's chances |
| 11 | Fighting a crisis | The toolkit; swap lines in 2008 and 2020 |
| 12 | Macroprudential policy | The tools and evidence; Basel's guide for Spain and the United States |
| 13 | Sudden stops | Mexico, Thailand, Korea; original sin |
| 14 | The Dials | The cost of a crisis; the warning value of a credit boom (new) |
| 15 | In practice | Financial-stability departments; *Called it?* on Rajan |
| 16 | Frontier | Brunnermeier and Sannikov; money funds; open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 34, *The Open Economy* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's credit (`explainer.economics.agora.credit`) with the
Island's Part 33 truths, or from the Data Room; the narration states the cached numbers.

- **The booms.** From the Macrohistory Database, the rise in bank loans to GDP over five years ending in each year
  from 1955 to 2015, excluding windows with a crisis inside them and years in which output per head fell; the
  largest, one per country. A crisis "follows" if JST's `crisisJST` marks one in the next three years.
- **The predictors.** Logits for a crisis starting in year t, war years (1914-19, 1939-47) left out: Schularick and
  Taylor's five lags of real loan growth with country effects; and one pooled regressor, the rise in loans to GDP over
  the five years before. Out of sample, each year from 1950 is predicted by a model fitted only on earlier years. Two
  measures were tried; the better is shown, and the film says so.
- **Recessions.** A peak is a year whose real GDP per head exceeds both neighbours; a recession is financial if a
  crisis starts within two years of the peak; paths are means over peaks with six years of data.
- **The debt contract.** Lognormal returns with log standard deviation 0.35 and monitoring cost 0.15; the premium
  and leverage traced over the default threshold from the contract's first-order conditions; the accelerator with
  capital's return falling as $K^{-0.3}$.
- **Kiyotaki and Moore.** $R = 1.1$, $a = 1$, $c = 0.5$, user cost $u = a(k/k^*)^{1/\eta}$ with $\eta = 2$; the
  date-0 landholding found by root-finding on the exact perfect-foresight path (land price as the discounted sum of
  future user costs). In this calibration a 2% shock has no equilibrium.
- **The leverage cycle.** Agents uniform on [0, 1] with one unit of cash and one of the asset; payoffs 1 or 0.2;
  four equations (two market clearings, two marginal buyers) solved together.
- **Basel's guide.** Bank loans to GDP for all credit; the trend by a one-sided Hodrick-Prescott filter with
  $\lambda = 400{,}000/4^4$ (annual data); a gap of 2 to 10 points mapped to a buffer of 0 to 2.5%.

## Problems and solutions

**1.** *Minsky: a borrower has cash flow 1 and debt 12, due over 20 years. At what interest rates is it hedge,
speculative, Ponzi?*

*Solution.* Principal falls due at 12/20 = 0.6 a year. Hedge needs $1 \ge 12r + 0.6$, so $r \le 3.3\%$.
Speculative: $12 r \le 1 < 12 r + 0.6$, so $3.3\% < r \le 8.3\%$. Ponzi: $12 r > 1$, $r > 8.3\%$. Doubling a 3%
rate to 6% turns a hedge borrower speculative without anything else changing.

**2.** *Debt deflation: debt is one year of income; prices fall 10% a year, real income 5%, and 5% of the debt is
repaid each year. Find the ratio after four years.*

*Solution.* Each year $b' = b(1 - 0.05)/\big((1 - 0.10)(1 - 0.05)\big) = b/0.9$: the repayment exactly offsets the
fall in real income, and deflation does the rest. After four years $b = 1/0.9^4 = 1.52$.

**3.** *Costly verification: show that with $\omega$ lognormal of mean one, $G(\bar\omega) = \Phi(z - \sigma)$ where
$z = (\ln \bar\omega + \sigma^2/2)/\sigma$.*

*Solution.* With $\ln \omega \sim N(\mu, \sigma^2)$ and $\mu = -\sigma^2/2$, the partial expectation is
$E[\omega; \omega < \bar\omega] = e^{\mu + \sigma^2/2}\,\Phi\big((\ln\bar\omega - \mu - \sigma^2)/\sigma\big)$. Since
$e^{\mu + \sigma^2/2} = 1$ and $(\ln\bar\omega + \sigma^2/2 - \sigma^2)/\sigma = z - \sigma$, $G = \Phi(z - \sigma)$.

**4.** *Kiyotaki and Moore: derive the steady state $u^* = a$, $q^* = Ra/(R-1)$, and the persistence
$k_t/k^* = (k_{t-1}/k^*)^{\eta/(1+\eta)}$.*

*Solution.* With correct expectations $R b_{t-1} = q_t k_{t-1}$, so net worth is $(a + q_t)k_{t-1} - q_t k_{t-1} =
a k_{t-1}$ and $k_t u_t = a k_{t-1}$. In a steady state $k_t = k_{t-1}$, so $u^* = a$; and $u = q - q/R$ gives
$q^* = R a/(R - 1)$. Out of it, $u_t = a (k_t/k^*)^{1/\eta}$ gives $(k_t/k^*)^{1 + 1/\eta} = k_{t-1}/k^*$, the
stated power.

**5.** *Leverage: with beliefs uniform on $[0, 1]$ and payoffs 1 or $d$, solve for the price with and without
borrowing; evaluate at $d = 0.2$.*

*Solution.* The marginal buyer $h$ values the asset at $p = h + (1 - h)d$. Without borrowing, buyers' cash $1 - h$
pays for the $h$ units sold: $p h = 1 - h$, giving $(1 - d)h^2 + (1 + d)h - 1 = 0$; at $d = 0.2$, $h = 0.596$,
$p = 0.677$. With borrowing of $d$ per unit, $p h = 1 - h + d$: $0.8h^2 + 1.2h - 1.2 = 0$, $h = 0.686$, $p = 0.749$.

**6.** *Households: a house worth 100 with a mortgage of 80 loses 20%. Compute the owner's loss as a share of equity;
repeat with a mortgage of 50.*

*Solution.* With a mortgage of 80, equity is 20 and the loss of 20 wipes out all of it: 100%. With 50, equity is 50 and
the same loss is 40% of it. The lender loses nothing in either case until the house is worth less than the mortgage.

**7.** *Prediction: a test flags 20% of years and catches 60% of crises when the base rate is 4%. What share of flagged
years are followed by a crisis?*

*Solution.* Of 100 years, 4 have crises and the test catches 2.4 of them, among 20 flagged years: 2.4/20 = 12%.
Three times the base rate, and still eight false alarms in ten.

**8.** *$\bigstar$ Original sin: a firm has assets worth 100 baht and owes \$2, at 25 baht per dollar. At what exchange
rate is its equity wiped out?*

*Solution.* Its debt is $2e$ baht at $e$ baht per dollar; equity $100 - 2e$ vanishes at $e = 50$. At 25 it owes 50
baht and has equity of 50; a fall in the baht to 50 per dollar, about what happened between June 1997 and January
1998, wipes it out without any change in its business.

## Lab and interactive

- `python -m videos.economics.labs 33`: Minsky's borrowers, debt deflation, the debt contract and the accelerator,
  Kiyotaki and Moore, the leverage cycle, the Island's counties, the crisis predictors in and out of sample, odds by
  credit boom, recessions, and Basel's guide.
- The interactive (course site): the leverage cycle. The reader sets how much lenders will lend and how bad the bad
  news is, and watches the price, the marginal buyer and the margins before and after the news.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[33]`; the cost of a crisis and the
warning value of a credit boom are dials (`explainer/economics/dials.py`); Rajan's 2005 paper is a *Called it?* entry
(`explainer/economics/calls.py`). The Macrohistory Database (release 6) was retrieved on 2026-11-20 from
macrohistory.net, and FRED's series on 2026-11-19 and 2026-11-20. The British Academy's letter and Fisher's sentence
were checked against the documents themselves; the Queen's words are as reported, since accounts differ; Lehman's
$639 billion of assets, the SCAP results and Thailand's float of 2 July 1997 were checked against contemporary reports.
