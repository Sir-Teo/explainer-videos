# Economics, Built: Part 3, The Measure

Part 3 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act I, *The Question*. It asks how you put a number on an economy, and answers
with the national accounts: what each producer adds, checked against what is spent and what is earned, divided by a
price index whose basket is chosen with care, compared across countries at the same prices, and read with its
omissions in mind.

It opens in 1932, three years into the Depression, when nobody could say how much America's income had fallen, and
follows Simon Kuznets's report to the Senate of January 1934: income produced down 53 percent, interest still paid
almost in full, wages in the mines, factories and railways down by six tenths, and a warning on page seven that the
welfare of a nation can scarcely be inferred from its income. From there it covers:

- Petty's *Verbum Sapienti* (1665), which already added up England twice, by spending and by income; King, Kuznets,
  Meade and Stone, the System of National Accounts (1953 to 2025);
- GDP three ways on the Island: Dara's books, value added against double counting, C + I + G + X − M, wages, profits
  and taxes; a Sankey diagram of the circular flow; saving, investment and the trade balance; the United States in
  2025, its statistical discrepancy, and where its output has gone since 1929;
- the production boundary: imputed rent (left out in 1934, counted today), the Island's unpaid work, BEA's
  household-production account, the informal economy and free goods;
- real and nominal: US GDP since 1929 in current and in 2017 dollars; Kuznets's deflation; Laspeyres (1871) and
  Paasche (1874);
- a game: Bo's two baskets, the three named answers and the true one, read off his indifference curve; chain drift
  over twelve stormy and calm seasons;
- the consumer price index: how it is built and what is tied to it, the Boskin Commission's 1.1 points (1996)
  source by source, hedonic quality adjustment on the Island's boats, and the chained CPI's measured gap;
- an intermission without narration: the US unemployment rate month by month since 1948, under the same numbers
  played as a tune, with a rest where October 2025 has no number;
- across countries: exchange rates against purchasing power, the Penn effect, the world redrawn from market rates
  to PPP, and the 2005 price comparisons that shrank China and India;
- unemployment as a survey: the two questions, Dara's survey of the Island's 100 adults and its six rates, the
  United States in October 2026, participation, and the month that does not exist;
- who gets the income: the Island's forty households, the Lorenz curve and the Gini coefficient, 131 countries, and
  the distributional national accounts and their critics;
- Leontief's input-output table, the rounds of extra output behind $10 of exports, his inverse and its multipliers,
  and trade in value added;
- revisions: 2008 as each vintage saw it, every quarter's first estimate against today's since 1965, and why
  estimates are revised;
- beyond GDP: Nordhaus and Tobin's measure of economic welfare, the Human Development Index, and Jones and Klenow's
  consumption-equivalent welfare;
- a new dial (the CPI's measurement bias), Kaldor's facts and the labour share, the people who make the numbers,
  and a frontier chapter on intangibles, night lights and the 2025 SNA.

## Build it

```bash
python -m videos.economics.econ3.compute              # every number (a few seconds), into .cache/econ3/
python tools/qa_scene.py econ3 PlayIt                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ3 -q l   # the whole part, silent preview
python tools/build.py econ3                           # 1080p30 with narration and the series' computed score
python -m explainer.economics.data --refresh wdi hdr rtdsm   # the data again, with a report of changes
python -m videos.economics.labs 3                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, retrieved on 19 November 2026 and registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): FRED's national accounts, labour-market and price
series (from BEA and BLS) and the Penn World Table's labour share; the World Bank's World Development Indicators;
the UNDP's Human Development Report 2025; and the Philadelphia Fed's Real-Time Data Set. The household survey was
not taken in October 2025, during the federal government shutdown, so the unemployment rates have no value for that
month; the films show the gap rather than fill it. Tables and passages transcribed from publications are in
`explainer/economics/data/tables.py`, each with where it was read and the date it was checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | How do you put a number on an economy? | Industrial production halved, 1929 to 1932; La Follette's resolution; Kuznets; the report of 4 January 1934; income produced −53%, paid out −40%, businesses paying out $9.5 billion more than they earned; payments by type in 1932 (interest 96.7% of 1929, wages in the selected industries 39.8%); the warning on page 7; the question; the title; a meter on every pipe; objectives |
| 1 | Counting a country | Petty in 1665: six million people at £6 13s 4d, £40 million; the stock's £15 million and labour's £25 million; spending equals income; his tax of £375,000 on property and £625,000 on the people; King; Kuznets; Keynes, Meade and Stone (April 1941); the SNA, 1953 to 2025; GNP to GDP in 1991; three Nobel prizes |
| 2 | GDP three ways | Dara's books: four businesses, $975 of sales, double counting; value added, $740; C + I + G + X − M = 610 + 120 + 30 + 120 − 140; wages, profits and taxes, 450 + 250 + 40; the Sankey diagram; S = I + (X − M): 100 = 120 − 20; the US in 2025 ($30.86 trillion; GDI $30.91 trillion; discrepancy −$46 billion); expenditure shares since 1929 (government 48% in 1944) |
| 3 | What is in, and what is left out | The production boundary; imputed rent; the Island's unpaid work, $230 (31% of GDP); Bo, Ana and the cooking; BEA's household production (+39% in 1965, +25.7% in 2010); the ILO's 61% informal; the median $48 to give up Facebook for a month |
| 4 | Real and nominal: whose basket? | US GDP 1929–2025: ×295 nominal, ×20 real (6.1% and 3.2% a year); 1929–33, −45% and −26%; Kuznets's real income paid out, −25%; Laspeyres and Paasche |
| 5 | Play it: two baskets | Bo's $100 split evenly; fish from $2 to $4; four answers; Laspeyres +50%, Paasche +33%, Fisher +41.4%; the indifference curve: $150 overpays, $141.42 is exact; chained Laspeyres 2.03 and Paasche 0.49 after twelve seasons, chained Fisher 1.00 |
| 6 | The consumer price index | The basket, 75 urban areas, annual weights; what is indexed; the Boskin Commission: 0.15 + 0.25 + 0.10 + 0.60 = 1.1 points (0.8–1.6), about $1 trillion of debt; the boatyard's boats: +25.5% on average, +2.5% for the same boat (truth 3%); CPI-U 2.62% a year since December 1999, chained 2.36%, PCE 2.26% |
| | Intermission: seventy-eight years of unemployment | No narration: the unemployment rate, January 1948 to October 2026, under the same numbers as a tune; 2025–26 magnified, October 2025 a rest; the story so far |
| 7 | Across countries | 2024 GDP at market rates (US $29.3 trillion, China $18.7 trillion, India $3.8 trillion); the haircut; purchasing power parities; the Penn effect; the world redrawn (world GDP $111 trillion to $197 trillion, China $38 trillion, India $15.6 trillion); the 2005 revision (China −40%, India −36%); the Big Mac |
| 8 | Unemployment is a survey | The Current Population Survey; two questions; Dara's 100 adults: U-3 = 5/67 = 7.5%; U-1 to U-6 (3.0% to 18.3%); the US in October 2026 (1.9% to 7.9%); U-3 and U-6 since 1994; participation 61.9% (peak 67.3% in 2000); 946 months, one missing |
| 9 | Who gets the income? | The Island's forty households (average $17.50; Friday and Crusoe a quarter of the income); Lorenz (1905) and Gini (1912): 0.39, wages alone 0.26; 131 countries' Ginis; Piketty, Saez and Zucman (bottom half 20% → 12%, top 1% 12% → 20%, 1980–2014) and Auten and Splinter (+4.4 points pre-tax, +1.4 after) |
| 10 | Input and output | Leontief (1936); the Island's table and coefficients; $10 more fish exports: $10, $1.97, $0.31, ...; total output $12.32; the inverse and its multipliers (1.23, 1.04, 1.20, 1.27); 92% of exports is value added on the Island; trade in value added |
| 11 | Revisions | 2008 by vintage: the NBER's call of 1 December 2008; 2008 Q4 first −3.8%, today −8.5%; 233 quarters since 1965: typical revision 1.5 points, 17 sign flips, correlation 0.89; advance, second, third, annual and comprehensive estimates; R&D counted as investment in 2013 |
| 12 | Beyond GDP | Nordhaus and Tobin (1972): MEW per head 1.1% a year against NNP's 1.7%, 1929–65; the HDI against income (correlation 0.96 with log income; Cuba and Tonga above, Qatar, Brunei and Guyana below); Jones and Klenow: France's welfare 92% of America's on 67% of its income |
| 13 | The Dials: how biased is the price index? | The new dial: Boskin 1.10, Lebow and Rudd 0.87, Gordon 1.25 (1995–96 revisited) and 0.8 (2006), Moulton 0.85; the sources compared; Kaldor's six facts; US GDP per head on a log line (1.7% a year since 1870); the labour share, 63% to 57% |
| 14 | In practice: the people who make the numbers | National accountants, price statisticians, survey methodologists, nowcasters, country economists, data scientists; the jobs report at 8:30 on a Friday |
| 15 | Frontier: measuring what has no price | Intangibles (Corrado, Hulten and Sichel: $800 billion a year missing in 2003); free goods and AI; night lights (Henderson, Storeygard and Weil 2012; Martinez 2022: autocracies overstate growth by about 35%); the 2025 SNA |
| | Recap, problems, and the road ahead | The answer; ten lines; problems; reading; Working's cloud and Part 4 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora, the Data Room or a transcribed table, and the narration
states the cached numbers.

- **Kuznets's tables** (`tables.KUZNETS_1934`): tables 1 and 2 of *National Income, 1929–32* in millions of current
  dollars; real income paid out is income paid out divided by the BLS cost-of-living index (1929 = 100).
- **The Island's accounts** (`agora.accounts.IOTable`, planted in `explainer.economics.island`, Part 3's truths):
  four industries' purchases from each other, their final sales to households, investment, the council and visiting
  ships, imported inputs and cloth, and the wages, profits and taxes they pay. `IOTable.check()` confirms that GDP is
  $740 by output, spending and income. The Sankey diagram splits each final use into the value added of each
  industry it embodies, v·(I − A)⁻¹·f.
- **The United States** (FRED, annual): GDP, GDI, consumption, investment, government, exports and imports in
  billions of current dollars, 1929–2025; real GDP in chained 2017 dollars and the GDP deflator.
- **Bo's baskets** (`agora.indices`): Cobb–Douglas demand with equal shares; Laspeyres, Paasche, Fisher and
  Törnqvist indexes; the exact cost-of-living index; chained indexes over twelve alternating seasons.
- **The boatyard's boats** (simulated): 30 boats a year, lengths drawn from N(5.0, 0.6) and N(5.6, 0.6) metres,
  price = 2·L^1.6·1.03^year·e^ε with ε ~ N(0, 0.06²), seed 1996; least squares of log price on log length and a year
  dummy.
- **The CPI**: the CPI-U (CPIAUCSL), the chained CPI-U (SUUR0000SA0) and the PCE price index (PCEPI), each rebased to
  December 1999 = 100, with average annual growth to October 2026 (September for PCE); the audits from
  `tables.CPI_BIAS`.
- **The world**: WDI 2024 GDP at market rates and at PPP for every economy with a million people or more; the price
  level is market GDP over PPP GDP; the cartogram places the 70 largest at PPP near their capitals (an
  equirectangular projection) and relaxes the circles apart, with the US the same size in both maps.
- **Unemployment**: Dara's survey (planted, 100 adults) and BLS's definitions of U-1 to U-6; US rates, participation
  and the employment ratio from FRED.
- **Distribution**: forty households (planted: wages lognormal with σ = 0.45 over 38 households, profits to Friday,
  Crusoe and eight small owners, seed 1934); the Gini as the mean absolute difference over twice the mean; the WDI
  Gini, latest survey 2015–2024, for 131 countries of a million people or more.
- **Leontief**: A = Z·diag(x)⁻¹ and L = (I − A)⁻¹ from the Island's table; the rounds are f, Af, A²f, …
- **Revisions**: the Philadelphia Fed's ROUTPUT vintages; growth is annualized, 100·((Y_t/Y_{t−1})⁴ − 1), within each
  vintage; first estimates from the first vintage reporting each quarter, latest from 2026Q4, quarters 1965Q4–2023Q4.
- **Beyond GDP**: the HDI and GNI per head (2021 PPP dollars) for 2023 from the HDR 2025; `tables.JONES_KLENOW_2016`
  and `tables.NORDHAUS_TOBIN_1972`.
- **Kaldor**: US GDP per head from the Maddison Project (1870–2022), with a log-linear trend; the labour share from
  the Penn World Table via FRED (1950–2023).
- **The intermission**: the unemployment rate, January 1948 to October 2026; the data melody maps annual means
  (1948–2024) and then each month of 2025–26 to D dorian, with no note for October 2025.
- **The score** (`explainer/economics/score.py`): the scissors theme, chapter stings, beds under the pauses, and the
  close. Synthesized from sines; nothing recorded.

## Problems and solutions

**1.** *An island has two firms. The farm sells $100 of grain, $30 of it to the bakery; it imports $10 of seed and
pays $50 in wages. The bakery sells $120 of bread to households and pays $40 in wages. Find GDP by output, by
spending and by income, and each firm's profit.*

*Solution.* Value added: the farm 100 − 10 = 90, the bakery 120 − 30 = 90, so GDP by output is 180. By spending:
households buy $70 of grain and $120 of bread, C = 190, and imports are 10, so GDP = 190 − 10 = 180. Profits are
value added less wages: the farm 90 − 50 = 40, the bakery 90 − 40 = 50. By income, wages 90 plus profits 90 make
180. The $30 of grain is counted once, inside the bread.

**2.** *Show from Y = C + I + G + X − M that national saving Y − C − G equals I + (X − M). The Island's council now
buys $20 more coconuts, and the grove sells $20 fewer abroad to supply them. What happens to national saving,
investment and the trade balance, and how much is the Island now borrowing?*

*Solution.* Subtract C and G from both sides of the spending identity: Y − C − G = I + (X − M). Output is unchanged
(the grove sells the same coconuts to a different buyer), G rises by 20 and X falls by 20. National saving falls
from 100 to 80, investment stays at 120, and the trade balance goes from −20 to −40: 80 = 120 − 40. The Island now
borrows $40 a year from abroad, twice as much, though nobody decided to borrow more; the identity did it.

**3.** *Fish triples to $6 while coconuts stay at $1, and Bo still spends half of his $100 on each. Find the
Laspeyres, Paasche and Fisher indexes, and the income that leaves him exactly as well off.*

*Solution.* Before, Bo buys 25 fish and 50 coconuts; after, 50/6 ≈ 8.33 fish and 50 coconuts. Laspeyres: (25 × 6 +
50)/(25 × 2 + 50) = 200/100 = 2.00. Paasche: (8.33 × 6 + 50)/(8.33 × 2 + 50) = 100/66.7 = 1.50. Fisher: √(2.00 ×
1.50) = √3 ≈ 1.732. With half his spending on each good, Bo's true index is the geometric mean of the price
relatives, √(3 × 1) = √3, so $173.21 leaves him as well off: Fisher is exact again, Laspeyres overstates by 27
points and Paasche understates by 23.

**4.** *Over one storm and one calm, show that chained Laspeyres multiplies to 1.5 × 0.75 = 1.125, chained Paasche
to 0.889, and chained Fisher to exactly 1.*

*Solution.* Calm to storm, Laspeyres prices the calm basket (25, 50): 150/100 = 1.5; storm to calm, it prices the
storm basket (12.5, 50): (12.5 × 2 + 50)/(12.5 × 4 + 50) = 75/100 = 0.75. The product is 1.125, though prices are back
where they started. Paasche uses the other basket each time: 100/75 = 1.333, then 100/150 = 0.667, product 0.889.
Fisher's links are √(1.5 × 1.333) = √2 and √(0.75 × 0.667) = 1/√2, product exactly 1. Each Laspeyres link
overstates the rise or understates the fall because the basket is the one from before people switched.

**5.** *The boatyard's regression gives log p = 0.756 + 1.56 log L + 0.024 · this year. What is the pure price change?
This year's boats average 5.71 m, last year's 5.00 m: roughly what rise in the average price does the regression
imply?*

*Solution.* Holding length fixed, this year's price is e^0.024 ≈ 1.024 times last year's: a pure price rise of about
2.4%. For the average boat, the length term adds 1.56 × ln(5.71/5.00) = 1.56 × 0.133 ≈ 0.207 to the log price, a
factor of e^0.207 ≈ 1.23; with the 2.4% that is 1.23 × 1.024 ≈ 1.26, a rise of about 26%, close to the 25.5% seen
in the averages. Nine tenths of the rise is quality.

**6.** *On the Island, the two discouraged islanders start looking again, and find nothing. What happens to U-3,
U-4 and the participation rate? Which of them gives the better reading of the labour market?*

*Solution.* They move from outside the labour force to unemployed. U-3 rises from 5/67 = 7.5% to 7/69 = 10.1%. U-4,
which already counted them, stays at 7/69 = 10.1%. Participation rises from 67% to 69%. Nothing about jobs changed:
the official rate rose because two people's search behaviour did. U-4, which counts them either way, reads the slack
more steadily; it is why the broader rates are published.

**7.** *Two industries with A = (0.1 0.2; 0.3 0.1). Find (I − A)⁻¹ and both output multipliers, and the extra output
of each industry for $10 more final demand for the second.*

*Solution.* I − A = (0.9 −0.2; −0.3 0.9), with determinant 0.81 − 0.06 = 0.75, so (I − A)⁻¹ = (1/0.75)(0.9 0.2; 0.3
0.9) = (1.2 0.267; 0.4 1.2). The multipliers are the column sums, 1.6 and 1.467. For f = (0, 10), output rises by
(2.67, 12.0): the second industry makes its $10 and $2 more for its own inputs and the first industry's needs, and
the first makes $2.67.

**8.** ⋆ *Design a test of whether a country's official growth is inflated, using night lights. What could make
lights grow faster than output in an honest country?*

*Solution sketch.* Regress the growth of reported GDP on the growth of lights across countries and years, with
country and year effects, and let the elasticity differ with a measure of democracy (Martinez 2022 uses Freedom
House's ratings); a larger elasticity in autocracies, robust to controls for the composition of output, urbanization
and electrification, suggests exaggeration. Check timing (does the gap open before elections or after a change of
regime?) and placebo years. Lights can outgrow output honestly where electricity spreads to the poor, where output
shifts from agriculture to cities and industry, or where satellites' sensors change, so those must be controlled or
the test compares like with like (within a country, across its own regimes).

## Where it comes back

| Idea | Where |
|---|---|
| what data can identify | Part 4, *The Evidence* |
| Kaldor's facts explained | Part 20, *Growth I: Capital* |
| unemployment's flows | Part 24, *Looking for Work* |
| C + I + G as demand | Part 27, *The Keynesian Revolution* |
| the price index and inflation | Part 28, *Inflation and Expectations* |
| policy in real time | Part 31, *The Central Bank* |
| saving, investment and the current account | Part 34, *The Open Economy* |
| trade in value added | Part 36, *Trade II: Scale, Firms and Gravity* |
| the labour share's fall | Part 39, *The Wage Structure* |
| inequality, measured and contested | Part 40, *Inequality and Mobility* |
| measuring AI | Part 65, *The Economics of AI* |

## Sources

**Primary texts.**
- U.S. Department of Commerce, Bureau of Foreign and Domestic Commerce (S. Kuznets and others, with the National
  Bureau of Economic Research), *National Income, 1929–32*, Senate Document No. 124, 73rd Congress, 2nd session
  (1934): chapter I, section 4 (pp. 5–7), tables 1–3 (pp. 10, 14) and the exclusions on p. 11, read in BEA's reprint
  in the *Survey of Current Business*, September 2020; tables 2 and 3 checked against NBER Bulletin 49 (7 June 1934).
- W. Petty, *Verbum Sapienti* (written 1665, printed 1691), chs. 1–2 and 4, in *The Economic Writings of Sir William
  Petty*, ed. C. H. Hull (1899), vol. 1 (Internet Archive scan economicwritings01pettuoft).
- BEA, "Gross Domestic Product as a Measure of U.S. Production", *Survey of Current Business*, August 1991; the UN
  Statistical Commission's adoption of the 2025 SNA (56th session, March 2025).
- BLS, *Handbook of Methods*: the Consumer Price Index and the Current Population Survey.

**Papers.**
- M. Boskin, E. Dulberger, R. Gordon, Z. Griliches and D. Jorgenson, *Toward a More Accurate Measure of the Cost of
  Living*, final report to the Senate Finance Committee (December 1996), as tabulated by Gordon (2006) and Moulton
  (2018).
- D. E. Lebow and J. B. Rudd, "Measurement Error in the Consumer Price Index: Where Do We Stand?", *Journal of
  Economic Literature* 41 (2003) 159–201.
- R. J. Gordon, "The Boskin Commission Report: A Retrospective One Decade Later", NBER Working Paper 12311 (2006).
- B. R. Moulton, *The Measurement of Output, Prices, and Productivity: What's Changed Since the Boskin Commission?*
  (Brookings, July 2018), table 5.
- B. Bridgman, A. Dugan, M. Lal, M. Osborne and S. Villones, "Accounting for Household Production in the National
  Accounts, 1965–2010", *Survey of Current Business*, May 2012.
- International Labour Organization, *Women and Men in the Informal Economy: A Statistical Picture*, 3rd ed. (2018).
- E. Brynjolfsson, A. Collis and F. Eggers, "Using Massive Online Choice Experiments to Measure Changes in
  Well-being", *PNAS* 116 (2019) 7250–7255.
- A. Deaton and A. Heston, "Understanding PPPs and PPP-based National Accounts", *American Economic Journal:
  Macroeconomics* 2(4) (2010) 1–35 (NBER Working Paper 14499).
- B. Balassa, "The Purchasing-Power Parity Doctrine: A Reappraisal", *Journal of Political Economy* 72 (1964)
  584–596; P. A. Samuelson, "Theoretical Notes on Trade Problems", *Review of Economics and Statistics* 46 (1964)
  145–154.
- T. Piketty, E. Saez and G. Zucman, "Distributional National Accounts: Methods and Estimates for the United
  States", *Quarterly Journal of Economics* 133 (2018) 553–609; G. Auten and D. Splinter, "Income Inequality in the
  United States: Using Tax Data to Measure Long-Term Trends", *Journal of Political Economy* 132 (2024).
- W. Leontief, "Quantitative Input and Output Relations in the Economic System of the United States", *Review of
  Economics and Statistics* 18 (1936) 105–125.
- W. D. Nordhaus and J. Tobin, "Is Growth Obsolete?", in *Economic Research: Retrospect and Prospect*, vol. 5
  (NBER, 1972).
- C. I. Jones and P. J. Klenow, "Beyond GDP? Welfare across Countries and Time", *American Economic Review* 106
  (2016) 2426–2457 (NBER Working Paper 16352, revised April 2015).
- N. Kaldor, "Capital Accumulation and Economic Growth", in F. A. Lutz and D. C. Hague (eds.), *The Theory of
  Capital* (1961).
- C. Corrado, C. Hulten and D. Sichel, "Intangible Capital and U.S. Economic Growth", *Review of Income and Wealth*
  55 (2009) 661–685.
- J. V. Henderson, A. Storeygard and D. N. Weil, "Measuring Economic Growth from Outer Space", *American Economic
  Review* 102 (2012) 994–1028.
- L. R. Martinez, "How Much Should We Trust the Dictator's GDP Growth Estimates?", *Journal of Political Economy*
  130 (2022) 2731–2769.

**Data.** FRED (Federal Reserve Bank of St. Louis): series from BEA and BLS and the Penn World Table's labour share,
retrieved 19 November 2026; the Maddison Project Database 2023; the World Bank's World Development Indicators (last
updated 11 November 2026); the UNDP's Human Development Report 2025 composite indices; the Federal Reserve Bank of
Philadelphia's Real-Time Data Set for Macroeconomists (ROUTPUT). Details, licences and checksums are in the Data
Room's [`SOURCES.md`](../../../explainer/economics/data/SOURCES.md).
