# Economics, Built: Part 25, Money

Part 25 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act VI, *Money and the Cycle*. It asks what money is, and what happens when
there is too much of it, and answers: money is whatever people accept in order to pass it on, a social convention and a
kind of memory that saves the double coincidence of barter. Today it is mostly bank deposits, created when banks lend.
Too much of it raises prices one for one in the long run; printed to pay a government's bills, it becomes a tax that
people flee, and only a believable change of fiscal regime, or another money, ends the flight.

It opens on Yap, where the money was limestone wheels quarried hundreds of miles away and a stone lost at the bottom of
the sea still made its owners rich (Furness 1910), and with Milton Friedman's comparison (1991) to the Bank of France's
gold in a New York basement. From there it covers:

- barter and its double coincidence (Jevons 1875, with Mademoiselle Zélie's pigs and coconuts): one chance in 81 with
  ten goods against one in 9 with money; money's three jobs; money as memory (Kocherlakota 1998);
- a game: salt, coconuts and fish on the Island, three kinds of islander; which good is passed on? (salt);
- Kiyotaki and Wright (1989): the search economy simulated; smoked fish becomes money too; the equilibrium check by a
  two-state Bellman equation; where each pattern of trade is an equilibrium; fiat money; the laboratory (Duffy and Ochs
  1999);
- from Lydia's coins to Song China's *jiaozi* (1024), goldsmiths' notes, gold, Bretton Woods and 15 August 1971;
- the quantity theory: $MV = PY$; 146 countries' money growth and inflation, 1990–2024 (slope 0.96, correlation 0.96),
  against a year-by-year correlation of 0.28; America's M2 velocity since 1959;
- hyperinflation: Hanke and Krus's peaks (Germany 1923 to Hungary 1946); Cagan's money demand; the inflation tax's
  Laffer curve, highest at $1/\alpha$; *Called it?* on Cagan's revenue ceiling (wrong);
- how four big inflations ended (Sargent 1982), and why a printed deficit has two steady states, a stable one and an
  explosive one; Zimbabwe 2008 and Venezuela 2018 in the same framework;
- an intermission without narration: American base money, M2 and prices since 1959, M2 as a tune;
- the demand for money: Baumol and Tobin's square-root rule derived, and American M1 demand against the bill rate,
  broken in the 1980s;
- what money is today: currency, reserves and deposits; a loan creates a deposit (McLeay, Radia and Thomas 2014); the
  multiplier's collapse after 2008;
- the Fisher equation decade by decade; neutrality and superneutrality (Sidrauski 1967);
- the optimum quantity of money (Friedman 1969) with a cash-in-advance Island, against Lucas's (2000) estimate;
- one dial (the interest semi-elasticity of money demand, new), reserves and payments in practice, and a frontier
  chapter on stablecoins (Gorton and Zhang 2023) and central bank digital money.

## Build it

```bash
python -m videos.economics.econ25.compute              # every number (a minute), into .cache/econ25/
python tools/qa_scene.py econ25 KW                     # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ25 -q l   # the whole part, silent preview
python tools/build.py econ25                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 25                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the World Bank's money growth, inflation and output growth
by country since 1960; from FRED, M1, M2, the monetary base, currency, reserves, M2's velocity, nominal GDP, the CPI
and the three-month bill rate; and Hanke and Krus's hyperinflation peaks, transcribed in `tables.py`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | What is money, and what happens when there is too much of it? | Yap's stones, the one on the seabed, the painted crosses; Friedman and the Bank of France; objectives |
| 1 | Barter, and what money does | Jevons's singer; the double coincidence: $1/(n-1)^2$ against $1/(n-1)$, 1 in 81 against 1 in 9 with ten goods; 99 prices against 4,950 with a hundred goods; money as memory |
| 2 | Play it: which good becomes money? | Ana eats salt and makes coconuts, Bo eats coconuts and makes fish, Dara eats fish and makes salt; storage 0.1, 0.2, 0.6; Agora's run: salt is passed on in every such trade; Bo holds salt half the time |
| 3 | Kiyotaki and Wright | Smoked fish (0.25): salt 58% and fish 42% of passed-on trades; $V_f - V_c = -0.63$ fresh, $+0.14$ smoked; the equilibrium map over storage cost and patience; fiat money; Duffy and Ochs |
| 4 | From coin to paper | Lydia, the *jiaozi* of 1024, goldsmiths' receipts, the Bank of England (1694), gold by law, Bretton Woods, 15 August 1971; commodity, convertible and fiat money |
| 5 | The quantity theory | $MV = PY$ and in growth rates; 146 countries, slope 0.96, correlation 0.96, 0.98 net of output growth; 3,550 country-years with inflation below 10%: correlation 0.28; M2 velocity 1.77 (1959), 2.19 (1997), 1.42 now |
| 6 | Hyperinflation and the inflation tax | Peaks: Germany 29,500% a month (prices doubling in 3.7 days), Yugoslavia, Zimbabwe, Hungary $4.19 \times 10^{16}$% (15 hours); Cagan's demand; the Laffer curve with $\alpha = 5$: most revenue at 20% a month, 7.4% of real balances; *Called it?* |
| 7 | How four big inflations ended | Austria (1922), Germany (1923), Hungary and Poland (1924); regime change and credibility; Wicker's critique; a 4% deficit: steady states 5.6% and 39% a month; slow expectations settle, fast ones explode; a deficit beyond the peak has no steady state |
| 8 | Zimbabwe and Venezuela | Zimbabwe's 79.6 billion percent a month, the 100-trillion-dollar note and dollarization; Venezuela's oil collapse, the IMF's million percent and the five zeros; the same framework |
| — | Intermission | US base money, M2 and the CPI from 1959 (×108, ×82, ×12), M2 as a tune; the story so far |
| 9 | The demand for money | Baumol and Tobin: $n^* = \sqrt{iY/2b}$, $M^* = \sqrt{bY/2i}$; the Island: 548 at 1% a month; US M1: $-0.067$ a point before 1981, $-0.032$ after 1994; the 1980s break; Lucas and Nicolini |
| 10 | What money is today | Currency (11% of M2), reserves, deposits; a loan to Ana creates a deposit; the multiplier: M2 was 8.9 times the base in 2007 and 2.8 in 2014, as the base rose from 837 to 4,075 billion |
| 11 | Money, interest and prices | $i \approx r + \pi^e$; the bill rate against inflation by decade (real rates from $-1.2$ to $+3.3$ points); neutrality, superneutrality, Sidrauski |
| 12 | The optimum quantity of money | The Friedman rule; the cash-in-advance Island: 10% inflation costs 0.88% of consumption, 50% costs 8.3%; Lucas (2000): slightly less than 1% of income; why central banks aim for 2% |
| 13 | The Dial | The interest semi-elasticity of money demand (contested): Ball $-0.05$, Ireland above $-0.02$, this film $-0.067$ and $-0.032$ |
| 14 | In practice: reserves and payments | Reserves 43.5 billion (2007) and 2,842 billion (2014); interest on reserves; ample reserves; Fedwire, UPI, Pix, FedNow, M-Pesa |
| 15 | Frontier | Stablecoins ($205 billion to $306 billion in 2025), the GENIUS Act; Gorton and Zhang's wildcat banks; central bank digital currency; four open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 26, *Banks and Runs* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's money (`explainer.economics.agora.money`) with the Island's
Part 25 truths, or from the Data Room; the narration states the cached numbers.

- **Kiyotaki and Wright.** 300 islanders of each kind, 400 periods of random pairwise meetings; holdings and media of
  exchange averaged over the second half. The equilibrium check is type 1's Bellman equation over its two holdings,
  given the simulated distribution and everyone else's strategy, solved by value iteration ($u = 1$, $\beta = 0.9$).
- **The world.** For each economy with at least 20 years of data in 1990–2024: the means of $\ln(1 + \text{money
  growth})$ and $\ln(1 + \text{inflation})$; least squares across economies. Year by year: country-years with
  inflation between 0 and 10%.
- **Cagan.** Real balances $e^{-\alpha\pi}$, $\alpha = 5$ months; the Laffer curve $\mu e^{-\alpha\mu}$. The deficit
  model is monthly and discrete: money grows by $d/m$, seigniorage is $\frac{\pi}{1+\pi}m$, expectations adapt at 10% or
  50% a month.
- **US money demand.** Quarterly $\ln(\text{M1}/\text{GDP})$ on the three-month bill rate, 1959–2019, by period.
- **Cash in advance.** Utility $\ln c - n$, $c = n$, $\beta = 0.96$; $c = 1/(1 + i)$ with $1 + i = (1+\mu)/\beta$; the
  loss is the share of consumption that makes the household indifferent to the Friedman rule.

## Problems and solutions

**1.** *Barter: with $n$ goods, show that a random meeting allows a trade with probability $1/(n-1)^2$ under barter and
$1/(n-1)$ with money; count the prices needed each way.*

*Solution.* You hold one good and want one of the other $n-1$. A stranger holds a good you want with probability
$1/(n-1)$ and, independently, wants yours with probability $1/(n-1)$: barter needs both. With money you need only one
side, a seller of what you want or a buyer of what you have. Every pair of goods needs its own rate of exchange,
$n(n-1)/2$ of them; with a unit of account, $n - 1$.

**2.** *Kiyotaki–Wright: under the fundamental strategies, show that Bo holds salt exactly half the time in a steady
state.*

*Solution.* Ana always holds coconuts and Dara always holds salt. Bo holding fish swaps it for salt when he meets Dara
(she eats fish; he accepts salt because it is cheaper to keep); Bo holding salt swaps it for coconuts when he meets Ana
(he eats them and catches new fish). Each meeting happens with the same probability, a third, so in a steady state the
flow from fish to salt, $p_f/3$, equals the flow back, $p_s/3$: $p_f = p_s = \tfrac12$.

**3.** *The quantity equation: from $MV = PY$, derive $\pi = \mu + \Delta\ln V - g$; with M2 growing 6%, velocity steady
and output 2.5%, what inflation?*

*Solution.* Take logs and differences: $\Delta\ln M + \Delta\ln V = \Delta\ln P + \Delta\ln Y$. So $\pi = 6 - 2.5 = 3.5\%$.
America's 2010s had M2 growing about 6% and inflation under 2%: velocity fell.

**4.** *Cagan: show that steady-state seigniorage $\mu e^{-\alpha\mu}$ is largest at $\mu = 1/\alpha$, and find its
maximum.*

*Solution.* The derivative is $e^{-\alpha\mu}(1 - \alpha\mu)$, zero at $\mu = 1/\alpha$, and the second derivative is
negative there. The maximum is $e^{-1}/\alpha$: with $\alpha = 5$ months, 20% a month and 7.4% of the real balances held
at zero inflation, each month.

**5.** *Two steady states: show that a deficit $d$ financed by $\pi e^{-\alpha\pi} = d$ has two solutions if
$d < e^{-1}/\alpha$ and none if $d > e^{-1}/\alpha$.*

*Solution.* $h(\pi) = \pi e^{-\alpha\pi}$ is zero at 0, rises to $e^{-1}/\alpha$ at $1/\alpha$, and falls toward zero as
$\pi \to \infty$; it is continuous and strictly monotone on each side of the peak. So the line $h = d$ crosses it once
on each side when $d$ is below the peak, touches it when equal, and misses it when above. With adaptive expectations the
low crossing is stable when expectations adapt slowly, and the high one is not.

**6.** *Baumol–Tobin: derive $n^* = \sqrt{iY/2b}$ and $M^* = \sqrt{bY/2i}$, and the income and interest elasticities.*

*Solution.* Minimize $C(n) = iY/(2n) + bn$: $C'(n) = -iY/(2n^2) + b = 0$ gives $n^* = \sqrt{iY/2b}$, and
$M^* = Y/(2n^*) = \sqrt{bY/2i}$. In logs, $\ln M^* = \tfrac12\ln b + \tfrac12\ln Y - \tfrac12\ln 2 - \tfrac12\ln i$: an
income elasticity of $\tfrac12$ and an interest elasticity of $-\tfrac12$.

**7.** *T-accounts: Ana borrows 100 and withdraws 20 in cash. Write the three balance sheets. Does broad money change?
Base money?*

*Solution.* The bank: assets $+100$ loan and $-20$ reserves; liabilities $+80$ deposit. Ana: assets $+80$ deposit and
$+20$ currency; liabilities $+100$ loan. The central bank: liabilities $-20$ reserves and $+20$ currency. Broad money
(deposits plus currency) rises by 100 in all, exactly as without the withdrawal; base money (reserves plus currency) is
unchanged, its composition shifted from reserves to currency.

**8.** *★ Cash in advance: with utility $\ln c - an$, $c = n$ and $Pc \le M$, derive $c = 1/(a(1+i))$ and show the
welfare cost is zero only at $i = 0$.*

*Solution.* A unit of work earns a dollar that can be spent only next period, after it has lost value to inflation and
forgone the interest it could have earned: the marginal rate of substitution must equal one over the gross nominal rate,
$\frac{1/c}{a} = 1 + i$, so $c = 1/(a(1+i))$. Welfare $\ln c - ac$ is maximized over $c$ at $c = 1/a$, that is at
$i = 0$, which by Fisher's equation means $\mu = \beta - 1$. Any positive $i$ lowers consumption below the efficient
level, and the cost rises with $i$: on the Island, 0.88% of consumption at 10% inflation.

## Lab and interactive

- `python -m videos.economics.labs 25`: run the Kiyotaki–Wright economy and its equilibrium checks, test the quantity
  theory on the World Bank's data, find the inflation tax's peak and the two steady states of a printed deficit, and
  price inflation with cash in advance.
- The interactive (course site): print to pay the bills. The reader sets the deficit, the semi-elasticity and how fast
  expectations adapt, and watches the Laffer curve and the path of inflation: settled or runaway.

## Sources

Hanke and Krus's peaks and Cagan's German figures are transcribed in `tables.HANKE_KRUS_2012`; the studies the film
states are listed with what each shows in `dials.SHOWN[25]`; the money-demand estimates are a dial
(`explainer/economics/dials.py`), and Cagan's ceiling is a *Called it?* entry (`explainer/economics/calls.py`). The World
Bank's extract and FRED's money series were retrieved on 2026-11-20. Cagan's own monthly series are not reproduced:
the film quotes his German average and revenue-maximizing rate from secondary summaries, and computes his model on the
Island.
