# Economics, Built: Part 27, The Keynesian Revolution

Part 27 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act VI, *Money and the Cycle*. It asks how a whole economy can be short
of buyers, and answers: when people want to hold more money, or spend less, than the economy's income allows, output
does most of the adjusting, not prices, because wages and prices move slowly. Spending sets output, the multiplier
spreads every change, and saving more can mean saving less. More money cures it unless interest rates are already at
zero; then the government's own spending must, or a promise of easy money later. In the long run prices adjust, but
the long run can be long.

It opens on Capitol Hill in the 1970s, where a babysitting co-operative of about 150 couples paid in coupons fell
into recession because everyone wanted a reserve of coupons and nobody went out (Sweeney and Sweeney 1977, retold by
Krugman 1998), and on the Island's own co-op, which manages 0.12 evenings out a couple each week until the board
prints coupons, and then 0.21. From there it covers:

- the Great Depression in the data: real GNP down 27% and prices down 26% from 1929 to 1933, unemployment above a
  fifth; Say's law and why it failed;
- a game: you hold three coupons and want ten; spend or hoard? (hoarding is wise for you and ruinous for all);
- the co-op as a model: evenings out against coupons per couple, a recession on the left, excess demand on the
  right, the most evenings near 8 coupons a couple;
- Keynes (1936): effective demand, the consumption function, the cross, and Kahn's multiplier (1931) as a geometric
  series ($1/(1-b) = 2.5$);
- the paradox of thrift, with investment fixed (saving unchanged) and rising with income (saving falls);
- Hicks's IS–LM (1937) derived, with fiscal crowding out (a multiplier of 1.54) and monetary policy;
- the liquidity trap: money adds nothing, spending has its full multiplier; Japan's and America's zero rates;
  Krugman's promise (1998);
- Phillips's water machine (1949), and a water version of the multiplier;
- an intermission without narration: American industrial production month by month, 1919–1945, as a tune;
- why wages do not fall: Keynes's two objections, Fisher's debt deflation, Bewley's interviews and the spike at zero;
- aggregate demand and supply, demand and supply shocks, and the neoclassical synthesis;
- what ended the Depression: gold (Eichengreen and Sachs 1985), money (Romer 1992), and war;
- the critics (Hayek, Friedman and Schwartz, Lucas and Sargent), and *Called it?* on Keynes's *Economic Consequences
  of the Peace* (partly right);
- two dials (the propensity to spend, from Part 22, and Okun's coefficient, new), the forecasting desk with two
  Facts (Okun's law; long expansions and short recessions), and a frontier chapter on supply shocks that cut demand
  (Guerrieri, Lorenzoni, Straub and Werning 2022).

## Build it

```bash
python -m videos.economics.econ27.compute              # every number (half a minute), into .cache/econ27/
python tools/qa_scene.py econ27 ISLM                   # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ27 -q l   # the whole part, silent preview
python tools/build.py econ27                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 27                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): from FRED, real GNP and the GDP deflator from 1929, the
NBER's unemployment rate for 1929–1942, industrial production since 1919, America's monetary gold stock for
1914–1946, real GDP against the CBO's potential, the unemployment rate and the CBO's natural rate, the NBER's
recession months since 1854, the federal funds rate, and Japan's overnight call rate.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | How can a whole economy be short of buyers? | The Capitol Hill co-op; the Island's co-op: 0.12 evenings a couple a week with 4 coupons, 0.21 once the board prints to 9; the question; objectives |
| 1 | The Depression in data | Real GNP $-27\%$ and the deflator $-26\%$, 1929–1933; back to 1929's output only in 1937; unemployment 1.4% (1929) to 23% (1933) in the NBER's monthly series; Say's law |
| 2 | Play it: hoard or spend? | Three coupons, a wanted reserve of ten; 26% of couples offer to sit and 12% go out, so an offer to sit finds a job 45% of the time; the fallacy of composition |
| 3 | The co-op as a model | The rules; evenings against coupons per couple (1 to 24): the shorter queue; the most, 0.21, near 8; recession left, excess demand right; three lessons |
| 4 | Keynes | Effective demand; $C = a + b(Y - T)$ with $b = 0.6$; the cross at $Y = 1{,}600$; $G$ up 100 gives 1,850; Kahn's series 100, 60, 36, ... to 250 |
| 5 | The paradox of thrift | Saving 50 more: income 1,250 to 1,125, saving stays 300; with $I = 300 + 0.1Y$, saving falls from 467 to 450; Mandeville |
| 6 | IS–LM | Hicks's two curves derived; they cross at $Y = 1{,}446$, $i = 2.5\%$; $G$ up 50: $Y = 1{,}523$, $i = 3.2\%$, a multiplier of 1.54; $M$ up 100: the same $Y$, $i = 1.2\%$ |
| 7 | The liquidity trap | Investment collapses by 150: $Y = 1{,}215$; doubling the extra money adds 10; spending 50 adds 125 (2.5); Japan's call rate from 8% (1990) to below 0.5% (late 1995); America at zero for 109 months; Krugman: at $i = 0$, expected deflation of 2% gives 1,100, expected inflation of 2% gives 1,350 |
| 8 | Phillips's machine | Croydon, 1949, about fourteen built; spending 0.6 of disposable income, taxes 20%: income 673 rises to 769 when $G$ rises 50 (a multiplier of 1.92) |
| — | Intermission | Industrial production 1919–1945 (1929 peak 7.9, 1932 trough 3.7, wartime peak 16.8, on 2017 = 100); the story so far |
| 9 | Why wages do not fall | Keynes's two objections; Fisher's debt deflation; Bewley's 336 interviews; the Island: 40% of workers due a cut, 32% frozen at exactly zero, 8% cut; Card and Hyslop; Dickens and coauthors' sixteen countries |
| 10 | Aggregate demand and supply | AD from IS–LM, vertical in the trap; sticky-wage AS; a money shock: (1,448, 0.995) to (1,417, 0.890); a cost shock: to (1,422, 1.056); the neoclassical synthesis; "in the long run we are all dead" |
| 11 | What ended the Depression? | Gold and the golden fetters; the gold stock: \$4.0 billion (March 1933), \$7.1 billion after revaluation, \$22.8 billion (1941); Romer: nearly all the recovery before 1942 from money; then the war |
| 12 | Keynes's critics | Hayek, Friedman and Schwartz, Lucas and Sargent, and what each left; *Called it?* on *The Economic Consequences of the Peace* (partly right) |
| 13 | The Dials | The propensity to spend a windfall (from Part 22); Okun's coefficient (depends on the setting): Okun about $-0.33$, Ball, Leigh and Loungani $-0.45$ (US), $-0.15$ (Japan), $-0.85$ (Spain), this film $-0.62$ |
| 14 | In practice | The forecasting desk: $C + I + G + NX$; America's output and unemployment gaps since 1949; the Okun fact ($-0.62$, $R^2 = 0.78$); expansions 41 months and recessions 17 since 1854, 64 and 10 since 1945, the longest 128 months from 2009 |
| 15 | Frontier | Keynesian supply shocks: the shutdowns of 2020; why one sector cannot produce them and two can; weaker fiscal stimulus, stronger monetary policy; four open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 28, *Inflation and Expectations* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's Keynesian economy (`explainer.economics.agora.keynes`) with
the Island's Part 27 truths, or from the Data Room; the narration states the cached numbers.

- **The co-op.** 150 couples, a wanted reserve of 10 coupons; a couple goes out with probability
  $0.3\min(1, b/10)$ and, if not going out, sits with probability $0.3\,\mathrm{clip}(2 - b/10, 0, 1)$; evenings are
  the shorter queue, paired at random; 200 weeks, printing in week 100. The curve averages weeks 60–260 at each level.
- **The cross, thrift and IS–LM.** Linear: $C = 200 + 0.6(Y - 100)$, $I = 300 - 25r$, $G = 200$, money demand
  $0.5Y - 50i$, $M = 600$, $i \ge 0$, $r = i - \pi^e$, with rates in percent.
- **AS–AD.** AD is IS–LM's output at each price level; AS is $Y = 1{,}450 + 300(P - 1)$, shifted up by 0.15 for the
  cost shock.
- **The machine.** $Y_{t+1} = Y_t + 0.25\,(0.6 \cdot 0.8\,Y_t + 150 + G - Y_t)$, with $G$ from 200 to 250.
- **Wages.** Notional changes $N(1\%, 4\%)$; 80% of cuts become freezes.
- **Okun's law.** Quarterly, 1949–2025: the unemployment rate (quarterly mean; quarters with a missing month, such as
  October 2025, are dropped) less the CBO's natural rate, regressed on real GDP's percentage gap from the CBO's
  potential.
- **Cycles.** Runs of FRED's NBER-based recession indicator, monthly since December 1854, dropping spells cut off by
  either end.

## Problems and solutions

**1.** *The cross: with $C = a + b(Y - T)$, derive equilibrium income and the multipliers of $G$ and of $T$; show that
a rise in $G$ paid by an equal rise in $T$ raises $Y$ one for one.*

*Solution.* Equilibrium is $Y = a + b(Y - T) + I + G$, so $Y = (a - bT + I + G)/(1 - b)$. Then $dY/dG = 1/(1-b)$ and
$dY/dT = -b/(1-b)$. Raising both by $\Delta$ changes $Y$ by $\Delta/(1-b) - b\Delta/(1-b) = \Delta$: the balanced-budget
multiplier is one. On the Island, $G$ and $T$ both up 100 raise income from 1,600 to 1,700.

**2.** *Kahn's series: sum $\Delta G(1 + b + b^2 + \cdots)$; after how many rounds is 90% of the effect felt with
$b = 0.6$?*

*Solution.* The partial sum after $n$ rounds is $\Delta G(1 - b^n)/(1 - b)$, a share $1 - b^n$ of the limit
$\Delta G/(1-b)$. We need $0.6^n \le 0.1$, so $n \ge \ln 0.1/\ln 0.6 = 4.5$: five rounds.

**3.** *Thrift: with $I = I_0 + hY$, show that a fall in $a$ lowers saving when $h > 0$.*

*Solution.* With no government, $Y = a + bY + I_0 + hY$, so $Y = (a + I_0)/(1 - b - h)$, and saving equals investment:
$S = I_0 + hY$. A fall in $a$ lowers $Y$ by $\Delta a/(1-b-h)$, and therefore lowers saving by $h\,\Delta a/(1-b-h)$.
With $h = 0$, saving is pinned at $I_0$ and does not change.

**4.** *IS–LM: solve for $Y$ and $i$; find the fiscal multiplier $dY/dG$ and show it falls as $d$ rises and as $h$
falls.*

*Solution.* Substituting $i = (kY - M/P)/h$ into $Y(1-b) = A - d\,i$ gives
$Y = (A + dM/(Ph))/(1 - b + dk/h)$, so $dY/dG = 1/(1 - b + dk/h)$. The term $dk/h$ is the crowding out: a higher
income raises money demand by $k$, which raises the interest rate by $k/h$, which cuts investment by $dk/h$. It
grows with $d$ (investment is more sensitive to the rate) and as $h$ falls (the rate must rise more to clear the money
market). On the Island, $1/(0.4 + 0.25) = 1.54$.

**5.** *The trap: show that when $i = 0$ binds, $dY/dM = 0$ and $dY/dG = 1/(1-b)$; what do expectations of inflation
do?*

*Solution.* At the floor the nominal rate is fixed at zero, so $Y = (A + d\,\pi^e)/(1-b)$ from the IS curve alone: $M$
does not appear, and $dY/dG = 1/(1-b)$ because nothing is crowded out. Expected inflation lowers the real rate
$r = -\pi^e$ and raises $Y$ by $d/(1-b)$ per point; expected deflation does the opposite, which is why falling prices
can deepen a slump at the zero bound.

**6.** *Phillips's machine: with taxes at rate $\tau$, show the multiplier is $1/(1 - b(1-\tau))$; how fast does the gap
close?*

*Solution.* At rest, $Y = b(1-\tau)Y + I + G$, so $Y = (I + G)/(1 - b(1-\tau))$, and $dY/dG = 1/(1 - b(1-\tau))$:
$1/(1 - 0.48) = 1.92$ on the Island. The dynamics are $Y_{t+1} - Y^* = (1 - s(1 - b(1-\tau)))(Y_t - Y^*)$ with speed
$s = 0.25$, so the gap shrinks by a factor $1 - 0.25 \times 0.52 = 0.87$ a period: half of it closes in about five
periods.

**7.** *AS–AD: a money shock and a cost shock; sign the effects on $Y$ and $P$, short run and long run.*

*Solution.* A fall in $M$ shifts AD left: in the short run, along the upward AS curve, $Y$ and $P$ both fall. In the
long run expected prices and wages fall, AS shifts right until $Y$ is back at $Y^*$, and only $P$ is lower. A cost
shock shifts AS up: $Y$ falls and $P$ rises (stagflation); in the long run, with AD unchanged, the shock to costs
eventually passes and $Y$ returns to $Y^*$, unless policy accommodates it with more money, which keeps $P$ higher.

**8.** $\bigstar$ *The co-op: with $N$ couples each wanting a reserve $m^*$, explain why evenings fall when
$M/N < m^*$ and when $M/N \gg m^*$; what would a price of evenings in coupons do?*

*Solution.* Evenings need a buyer and a seller. Below the reserve, couples want to earn coupons more than to spend
them, so the queue of goers is short and evenings are limited by it: a demand shortage. Far above it, nobody needs to
earn, the queue of sitters is short and evenings are limited by that: excess demand. If the co-op let the price of an
evening in coupons float, it would fall when coupons are scarce (each coupon buys more sitting, so the real value of
everyone's coupons rises to the reserve they want) and rise when they are plentiful; with a price that moved quickly
enough, the co-op would always be at its best, which is why the stickiness of prices is the heart of the matter.

## Lab and interactive

- `python -m videos.economics.labs 27`: run the co-op and cure it, sum Kahn's series, watch thrift lower saving, solve
  IS–LM with a zero bound, shock AS–AD, freeze wage cuts, and estimate Okun's law and the length of expansions on
  FRED's data.
- The interactive (course site): run the co-op. The reader is the board: set the coupons per couple and the reserve
  couples want, and watch a year of weeks and the curve of evenings against money.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[27]`; Okun's coefficient is a dial
(`explainer/economics/dials.py`), with the propensity to spend from Part 22; Okun's law has its Agora column in
`explainer/economics/facts.py`; Keynes's forecast of 1919 is a *Called it?* entry (`explainer/economics/calls.py`). FRED's
series were retrieved on 2026-11-20. The co-op's story follows Krugman's retelling of Sweeney and Sweeney; sources differ
on what one coupon bought, so the film does not say. Bewley's count of interviews is from Howitt's review; the
unemployment rate for the 1930s is the NBER's monthly series, and the film says that other estimates differ.
