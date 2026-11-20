# Economics, Built: Part 26, Banks and Runs

Part 26 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act VI, *Money and the Cycle*. It asks why banks are fragile, and whether
they can be made safe, and answers: banks are fragile because they do something valuable. They turn long, illiquid
loans into deposits anyone can take out at once, and so a bank that is sound if everyone stays can fail if enough
people fear it will. Deposit insurance, a lender of last resort and capital make them much safer, at the price of
watching them closely; but wherever short funding meets long assets, inside the banks or outside them, the run can
come back.

It opens on thirty-six hours in March 2023, when the customers of Silicon Valley Bank withdrew 42 billion dollars in a
day, mostly from their phones, asked for 100 billion more overnight, and found the bank closed on Friday morning; in the
same week, deposits at America's small banks fell by 149 billion dollars. From there it covers:

- what a bank does: its balance sheet as T-accounts, and maturity transformation;
- a game: you have a deposit and a rumour that half the other depositors will withdraw tomorrow; stay or withdraw?
  (stay: you get 1.26 against 1.16, but beyond 59% withdrawing, everyone should run);
- Diamond and Dybvig (1983) derived: the deposit contract insures depositors against their own impatience
  ($c_1 = 1.160$, $c_2 = 1.420$ against 1 and 1.5 alone);
- two equilibria, the bank and the run: the payoff table, sequential service (86% are paid, the rest get nothing), and
  sunspots;
- the cures: suspension of convertibility, deposit insurance (insurance never paid is free), and America's bank
  suspensions, from 3,891 in 1933 to 44 in 1934;
- Bagehot's rule (1873) after Overend, Gurney (1866): a fire sale turns illiquidity into insolvency (equity $-3.3$),
  a lender of last resort does not (equity 9);
- the price: deposit insurance as a put (Merton 1977); the savings and loans; too big to fail;
- capital: American banks' equity ratio since 1988; risk weights against interest-rate risk (a ten-year bond loses 24%
  when yields rise three points); Silicon Valley Bank's held-to-maturity portfolio; Admati and Hellwig;
- an intermission without narration: deposits at small and large banks, week by week, 2022–2024, as a tune;
- runs without depositors: repo haircuts (Gorton and Metrick 2012) and the money funds of 2008;
- global games (Morris and Shin 1998; Goldstein and Pauzner 2005): one equilibrium after all, failure exactly below
  $\theta^* = c/R$, and why better insurance for the impatient means more runs;
- runs in the data: the Depression's four banking crises, mostly fundamentals until 1933 (Calomiris and Mason 2003);
  2023's unrealized losses and uninsured depositors (Jiang, Matvos, Piskorski and Seru);
- banks as monitors (Diamond 1984) and what is lost when they fail (Bernanke 1983);
- two dials (the deposit beta and the output cost of a banking crisis, both new), stress tests, the treasury desk and
  deposit pricing with *Called it?* on the 2022 stress scenario (wrong), and a frontier chapter on digital runs, the
  weekend of 12 March 2023, narrow banking and stablecoins.

## Build it

```bash
python -m videos.economics.econ26.compute              # every number (seconds), into .cache/econ26/
python tools/qa_scene.py econ26 Global                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ26 -q l   # the whole part, silent preview
python tools/build.py econ26                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 26                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): from FRED, bank suspensions 1921–1941 and month by month
to 1933, deposits at small and large banks week by week, the federal funds rate, the FDIC's national savings and CD
rates, the two- and ten-year Treasury yields, banks' equity to assets, money market funds' assets and real GDP; Silicon
Valley Bank's numbers and the 2022 stress scenario, transcribed in `tables.py`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Why are banks fragile, and can they be made safe? | Thirty-six hours at Silicon Valley Bank: 42 billion withdrawn in a day, 100 billion more asked for, 94% of deposits uninsured; small banks lose 149 billion in a week while large banks gain 54; not financial advice; objectives |
| 1 | What a bank does | The balance sheet as T-accounts: deposits at par on demand, loans and bonds that pay over years, equity first to lose; maturity transformation |
| 2 | Play it: stay or withdraw? | One coconut deposited; 1.16 tomorrow or 1.42 later; a rumour that half will withdraw; staying still pays 1.26, but beyond 59% it pays less than running |
| 3 | Diamond and Dybvig | Patient and impatient depositors ($t = 1/4$), $R = 1.5$, $\gamma = 2$; the optimal contract $c_1 = 1.160$, $c_2 = 1.420$; a demand deposit implements it if only the impatient withdraw |
| 4 | Two equilibria | The payoff table; sequential service: 862 of 1,000 paid in full, the rest nothing; sunspots |
| 5 | Suspension and deposit insurance | Suspension at a quarter: a stayer is sure of 1.42; insurance that is never paid costs nothing; suspensions: 8,812 banks in 1930–33, 3,891 in 1933, 44 in 1934 |
| 6 | Bagehot's rule | Overend, Gurney and Black Friday, 1866; lend freely, at a penalty rate, against good collateral; the Island's bank: a fire sale at 60% leaves equity $-3.3$, Bagehot's lender 9 |
| 7 | The price: moral hazard | Merton's put: at 25% volatility it is worth 5.3 and the owners' stake 15.3, not 10; the savings and loans (up to about \$124 billion); too big to fail |
| 8 | Capital | Equity to assets 6.1% (1988), 10.3% (2020); risk weights: 17% of risk-weighted assets, but a three-point rise in yields costs 7.1 on 30 of bonds (duration 9.2), leaving 3.1% of assets; Silicon Valley Bank's \$91 billion held to maturity, \$15 billion under water; Admati and Hellwig's 20–30% |
| — | Intermission | Deposits at small and large banks, first week of 2022 = 100, to the end of 2024; small banks' deposits as a tune; the story so far |
| 9 | Runs without depositors | Repo and its haircut: assets at most equity over the haircut, 25 times at 4%, 5 times at 20%: sell 80 of 100; the Reserve Primary Fund breaks the buck (16 September 2008); money funds' assets rose as money fled prime funds; shadow banking |
| 10 | Global games | Private noise gives one equilibrium; 2,000 simulated depositors; failure exactly below $\theta^* = c/R = 0.5$; the Laplacian belief; a deposit paying 1.2 fails below 0.6 (Goldstein and Pauzner) |
| 11 | Runs in the data | Monthly suspensions 1929–1933 and Friedman and Schwartz's four crises (522 banks in October 1931); Calomiris and Mason: fundamentals until early 1933; Jiang, Matvos, Piskorski and Seru: \$2 trillion of unrealized losses, about 190 banks at risk if half the uninsured left |
| 12 | Banks as monitors | Delegated monitoring: 1,000 checks or one; a bank's chance of failing: 10% with one loan, 7% with ten, 0.004% with a hundred; Bernanke (1983); the 2022 Nobel prize |
| 13 | The Dials | The deposit beta (depends on the setting): about 0.6 in 2004–06, under 0.4 in 2015–19, 0.39 by 2022 Q4, 0.385 for all deposits by 2023 Q3, this film 0.08 (savings) and 0.33 (CDs); the output cost of a banking crisis (contested): Reinhart and Rogoff over 9%, Cerra and Saxena 10%, Romer and Romer 6%, America 3.8% peak to trough and 17.6% below its 1990–2007 trend by 2019 |
| 14 | In practice | The 2022 stress scenario (the ten-year at 0.75%) against 2022 (the ten-year to 4%, federal funds to 4.1%); *Called it?* (wrong); deposit pricing, February 2022 to December 2023: betas 0.08 and 0.33; the deposit franchise; duration, liquidity coverage, the discount window |
| 15 | Frontier | Digital runs and social media (Cookson and coauthors); the weekend of 12 March 2023 (every depositor protected, loans against bonds at par); narrow banking from the Chicago Plan and Fisher's *100% Money*; USDC at 88 cents; four open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 27, *The Keynesian Revolution* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's banks (`explainer.economics.agora.bank`) with the Island's
Part 26 truths, or from the Data Room; the narration states the cached numbers.

- **Diamond and Dybvig.** CRRA utility with $\gamma = 2$, $t = 1/4$, $R = 1.5$, liquidation at 1. The stayers' payment
  when a share $f$ withdraws is $R(1 - fc_1)/(1 - f)$ while the bank lasts; the run is 1,000 depositors in random
  order, each paid $c_1$ until the cash runs out.
- **The balance sheet.** Reserves 10, loans 60, ten-year bonds 30 with a 1.5% coupon bought at par, deposits 90,
  equity 10; risk weights 0, 1, 0; yields rise from 1.5% to 4.5%.
- **Merton's put.** Assets 100, insured deposits 90, one year, a zero interest rate; Black and Scholes.
- **The global game.** A withdrawer gets $c$, a stayer $R = 2$ if the bank survives; signals $\theta + 0.05\varepsilon$;
  2,000 depositors use the equilibrium cutoff $x^* = \theta^* + \sigma\Phi^{-1}(\theta^*)$.
- **Delegated monitoring.** Loans repay 1.3 with probability 0.9, depositors are promised 1 a loan: the bank fails when
  fewer than $\lceil n/1.3 \rceil$ loans repay, a binomial tail.
- **Deposit betas.** The change in the FDIC's national rate over the change in the federal funds rate, February 2022 to
  December 2023.
- **The 2008 output loss.** Real GDP (chained dollars), 2007 Q4 to 2009 Q2; the 2019 Q4 gap below a log-linear trend
  fitted to 1990–2007.

## Problems and solutions

**1.** *Diamond–Dybvig: with $u(c) = c^{1-\gamma}/(1-\gamma)$, derive $c_1 = 1/(t + (1-t)R^{1/\gamma - 1})$; show
$c_1 > 1$ exactly when $\gamma > 1$, and compute $c_1, c_2$ for $\gamma = 2$, $R = 1.5$, $t = 1/4$.*

*Solution.* Maximize $t\,u(c_1) + (1-t)\,u(c_2)$ subject to $t c_1 + (1-t) c_2/R = 1$. The first-order condition is
$u'(c_1) = R\,u'(c_2)$, so $c_1^{-\gamma} = R c_2^{-\gamma}$ and $c_2 = R^{1/\gamma} c_1$. Substituting into the budget,
$c_1[t + (1-t)R^{1/\gamma - 1}] = 1$. Since $R > 1$, $R^{1/\gamma - 1} < 1$ exactly when $\gamma > 1$, and then the
bracket is below one and $c_1 > 1$: the impatient get more than they could alone. With the numbers, $R^{-1/2} = 0.8165$,
the bracket is $0.8624$, $c_1 = 1.160$ and $c_2 = 1.2247 \times 1.160 = 1.420$.

**2.** *The run threshold: if a share $f$ withdraws $c_1$, stayers get $R(1 - fc_1)/(1-f)$. Show that waiting stops
paying once $f > (R - c_1)/(c_1(R-1))$.*

*Solution.* Waiting pays less than withdrawing when $R(1 - fc_1)/(1 - f) < c_1$, that is $R - Rfc_1 < c_1 - c_1 f$, or
$R - c_1 < f c_1 (R - 1)$. Dividing, $f > (R - c_1)/(c_1(R - 1))$. With $R = 1.5$ and $c_1 = 1.160$ the threshold is
$0.340/0.580 = 0.587$: once 59% of depositors are expected to withdraw, everyone should.

**3.** *Sequential service: if everyone runs and the bank can raise 1 per depositor, what share is paid? Who gets
nothing?*

*Solution.* The bank has 1 per depositor and pays $c_1$ to each in turn, so it pays $1/c_1 = 1/1.160 = 86.2\%$ of them
in full. The last 13.8% to arrive get nothing, patient or impatient: what matters is the place in the queue, which is
why everyone hurries.

**4.** *Bagehot: reserves 10, loans 90, deposits 90, equity 10; 30 is withdrawn. Find equity after a fire sale at 60%
and after borrowing at 5%.*

*Solution.* The bank pays 10 from reserves and needs 20 more. Selling loans at 60% of their value, it must sell
$20/0.6 = 33.3$ of loans, a loss of $13.3$, and equity falls from 10 to $-3.3$: insolvent. Borrowing 20 against its
loans at 5% costs 1 in interest, and equity is 9: it survives. The fire sale, not the withdrawal, made it insolvent.

**5.** *Merton: with $r = 0$, show that equity $=$ put $+ V - D$, so a flat premium hands the put to the owners.*

*Solution.* Equity is a call on the assets with strike $D$; the insurer's liability is a put with the same strike. A
call minus a put pays $V_T - D$ in every state, so with no discounting $C - P = V - D$ (put–call parity), and
$C = P + (V - D)$. Anything that raises the put's value, such as riskier assets, raises equity one for one; if the
premium does not rise with risk, the owners keep the whole gain.

**6.** *Repo: a dealer with equity 4 holds 100 of bonds at a 4% haircut. The haircut rises to 20%. How much must it
sell?*

*Solution.* With haircut $h$ it can borrow $(1-h)$ of what it holds, so its holdings are at most $E/h$: 100 at 4% (with
96 of repo), 20 at 20%. It must sell 80, and its repo falls from 96 to 16. Its lenders have withdrawn 80 without anyone
queueing at a door.

**7.** *Global games: using the Laplacian belief at the cutoff, show $\theta^* = c/R$; what happens to failures when $c$
rises?*

*Solution.* The depositor at the cutoff $x^*$ is indifferent: $R \cdot \Pr(\text{survive} \mid x^*) = c$. Since
everyone uses the same cutoff, at the cutoff she cannot tell where her signal stands among the others', so the share
of other depositors withdrawing is, to her, uniform on $[0, 1]$. As the noise vanishes, $\theta \to x^* \to \theta^*$,
and the bank survives when the share withdrawing is below $\theta^*$, which happens with probability $\theta^*$. Hence
$R\theta^* = c$ and $\theta^* = c/R$. Raising $c$ raises $\theta^*$: with $R = 2$, from 0.5 at $c = 1$ to 0.6 at
$c = 1.2$. Banks with strength between the two now fail.

**8.** $\bigstar$ *Delegated monitoring: loans repay $R$ with probability $p$; show the bank's failure probability goes
to 0 as $n \to \infty$ when $pR > D$, and compute it for $n = 10$, $p = 0.9$, $R = 1.3$.*

*Solution.* Let $X$ be the number of loans that repay, binomial with $n$ and $p$. The bank fails when $XR < nD$, that
is $X/n < D/R$. When $pR > D$, $D/R < p$, and by the law of large numbers $X/n \to p$, so the probability goes to zero;
Hoeffding's inequality bounds it by $\exp(-2n(p - D/R)^2)$, which falls exponentially in $n$. With $n = 10$ and
$D = 1$, the bank needs $\lceil 10/1.3 \rceil = 8$ repayments, and $\Pr(X \le 7) = 0.070$. Ten loans already cut the
failure rate from 10% to 7%, and a hundred loans to 0.004%.

## Lab and interactive

- `python -m videos.economics.labs 26`: solve Diamond and Dybvig's contract and its run threshold, run a bank with
  sequential service, price deposit insurance as a put, compute the repo squeeze, simulate the global game and check
  $\theta^* = c/R$, and diversify a bank's loans.
- The interactive (course site): run on the bank. The reader is a depositor among many, sees a noisy signal of the
  bank's strength and decides to stay or withdraw; the bank fails if too many leave. A slider sets how generous the
  deposit is, and the failure threshold moves.

## Sources

Silicon Valley Bank's numbers and the 2022 stress scenario are transcribed in `tables.SVB_2023` and
`tables.STRESS_2022`; the studies the film states are listed with what each shows in `dials.SHOWN[26]`; the deposit
betas and crisis costs are dials (`explainer/economics/dials.py`), and the stress scenario is a *Called it?* entry
(`explainer/economics/calls.py`). FRED's series were retrieved on 2026-11-20. Figures stated from papers and reports
(the savings-and-loan cost, the Reserve Primary Fund's Lehman paper, the unrealized losses of 2023, the stock-price
effect of Twitter exposure, USDC's low) are quoted as the sources give them, and are not recomputed.
