# Economics, Built: Part 2, The Scissors

Part 2 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act I, *The Question*. It asks what sets a price, and answers with Marshall's
two blades: what the last unit is worth to the last buyer, and what it costs the last seller.

It opens at Purdue University in January 1956, where Vernon Smith ran his first double auction expecting the
competitive model to fail, and watched it converge. From there it covers:

- Smith's paradox of water and diamonds (1776), the cost theories of Ricardo and Marx, Whately's pearl divers, and
  value at the margin (Jevons, Menger, Walras, 1871 to 1874);
- demand built one buyer at a time: Ana's cups, three drinkers added sideways, and crowds of 10 to 10,000 buyers
  whose staircase becomes a straight line; the law of demand and its two reasons;
- supply built from rising costs, Marshall's scissors (1890), and the four cards that fix the band in Part 1's pit;
- a lopsided market played by the viewer, Smith's worry that convergence was "an accident of symmetry", and the
  test of whether zero-intelligence traders find its price (they do not: Cliff and Bruten 1997);
- elasticity along a straight line, spending and the price where it is greatest, the midpoint formula on the
  Island's calm and stormy days, and petrol's short and long run;
- shifts: storms on the Island, comparative statics, and Brazil's black frost of July 1975, which cut the world's
  coffee crop by a sixth and multiplied the price of Arabica 5.7 times;
- an intermission without narration: sixty-six years of eight commodities' real prices, under the real price of
  coffee played as a tune;
- surplus from Dupuit's bridges (1844) to the triangle a market loses when trade stops short;
- who pays a tax: the pit taxed from either side, the incidence formula, and two field studies in which who remits
  the tax does matter;
- price controls: a cap and a floor in the pit, the lottery loss on top of the triangle, petrol queues, and
  San Francisco's rent control; the is/ought card;
- the Dials' first row (the price elasticity of staples), work that uses all of this, and a frontier chapter on
  prices set by algorithms.

## Build it

```bash
python -m videos.economics.econ2.compute              # every number (about a minute), into .cache/econ2/
python tools/qa_scene.py econ2 PlayIt                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ2 -q l   # the whole part, silent preview
python tools/build.py econ2                           # 1080p30 with narration and the series' computed score
python -m explainer.economics.data --refresh pinksheet psd_coffee   # the data again, with a report of changes
python -m videos.economics.labs 2                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, retrieved on 18 November 2026 and registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the World Bank's Pink Sheet (update of 3 November
2026), USDA's coffee balance sheets, and the US consumer price index from FRED. The Bureau of Labor Statistics never
published an index for October 2025, during the federal shutdown; that one month is filled log-linearly from its
neighbours wherever a price is deflated, and the films say so on their data tags.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | What sets a price? | Purdue, 1955: Smith's doubt and his plan, in his own words; January 1956 and his amazement; his prediction, to be scored; water and diamonds; the title; the Tableau's first two pipes open; objectives |
| 1 | Water and diamonds | Smith's paradox and value in use and in exchange; Ricardo and Marx; Whately's pearl divers; Jevons, Menger and Walras; the value of one more litre, the whole area against the last height; a price measures the margin |
| 2 | Demand, one buyer at a time | Ana's four cups and her staircase; three drinkers added sideways, 6 cups at $1.50; crowds of 10, 100, 1,000 and 10,000 buyers; the line they tend to; the law of demand and its two reasons |
| 3 | Supply, and the scissors | A farm's rising cost per sack; Marshall's scissors in 1890 and in the fifth edition; the pit's four marginal cards and the band $2.20 to $2.30; the cards that do not matter; both blades |
| 4 | Play it: guess the price | Smith's "accident of symmetry"; the lopsided cards; the tempting guesses $1.73 and $2.05; the band $2.25 to $2.30; buyers keep $1.23, sellers $6.47; Agora's traders converge by the third period; zero-intelligence traders stop near $2.10 |
| 5 | Why it converges | Excess supply above the band, excess demand below; Gode and Sunder; four markets, two kinds of trader: random traders miss by 17 to 25 cents when the market is lopsided; why; Called it?: Smith's prediction, wrong; the first Fact's columns |
| 6 | Elasticity | Percent over percent; steep and flat; elasticity and spending along the fish market's line, −1 at $3.00; the midpoint formula on calm and stormy days (−0.82, −1.26, −1.02); petrol's −0.09 and −0.31 |
| 7 | Shifts: a frost in Brazil | The Island's 120 days and its storms, sliding along the planted demand line; which blade moved; 18 July 1975; Brazil's crop −60%, the world's −16%; Arabica from $1.23 to $7.00 a kilo; a rough elasticity of −0.16 and its caveats; the 1994 frosts; 2025's nominal record against 1977's real one |
| | Intermission: sixty-six years of prices | No narration: the real prices of oil, coffee, cocoa, sugar, wheat, copper, tin and gold, 1960 to 2026, under the real price of coffee as a tune; the story so far |
| 8 | Surplus | Dupuit's bridge: the tolls, the surplus above them, the crossings prevented; the pit's $3.40 and $3.30; one pair fewer, one pair more; the fish market's surpluses and the deadweight loss |
| 9 | Who pays a tax? | A 40-cent tax on the pit's sellers: buyers pay $2.46, sellers keep $2.06, one unit lost; the same tax on buyers; the incidence formula; the fish market's 57%; salience (Chetty, Looney and Kroft) and evasion (Kopczuk and others) |
| 10 | Price controls | A cap at $2.00: five sellers, seven buyers; 98.5% with the right buyers, 83% by lottery, 84% in the pit; petrol queues; San Francisco's rent control; a floor at $2.60; the is/ought card |
| 11 | When the picture fails | What the picture assumed; where each failure is taken up |
| 12 | The Dials: how much do people respond? | The first dial filled: petrol, cigarettes, beer, wine, spirits; the first sixteen dials |
| 13 | In practice: who sets prices for a living | Commodity desks, pricing teams, tax analysts, competition authorities |
| 14 | Frontier: prices set by algorithms | Q-learning sellers that learn to keep prices high (Calvano and others 2020); German petrol stations (Assad and others 2024); three open questions; the research problem |
| | Recap, problems, and the road ahead | The answer; ten lines; problems; reading; Kuznets and Part 3 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora, the Data Room or a primary text, and the narration
states the cached numbers.

- **Water and diamonds** (illustrative): the value of one more litre with q litres already in hand, 30e^(−q/28)
  dollars (plus a fraction of a cent), so the first 150 litres are worth about $837 and the 150th about 14 cents.
- **Demand**: Ana's cups ($4.00, $2.50, $1.20, $0.40), Bo's and Chidi's, sorted into one staircase; crowds of 10,
  100, 1,000 and 10,000 buyers with values uniform on $0 to $6 (`agora.curves.crowd`), drawn per head against the
  line Q/n = 1 − p/6.
- **The pit and its designs** (`agora.market`): Part 1's twenty cards; the lopsided design (buyers $2.60 to $2.15,
  sellers $0.60 to $2.85), a flat supply at $2.00 and a flat demand at $2.60, planted in `explainer.economics.island`
  (Part 2's truths). Forty-one runs of six periods for each design and each kind of trader (Cliff's learning traders
  and Gode and Sunder's zero-intelligence ones); the run shown in chapter 4 is the median of the 41 by final-period
  convergence. The double auction takes a tax remitted by either side and a legal maximum or minimum price.
- **The fish market** (the Island, simulated): each day 400 buyers' values are drawn afresh on $0 to $6, and a
  storm (probability 0.15) keeps a third of the 400 fish's worth of catch ashore; each day's cards are cleared at the
  competitive price. The planted lines are Q = 400(1 − p/6) and Q = 400(p − 0.5)/4.5.
- **Elasticity, surplus, tax and controls on the lines** (`agora.curves.Linear`): exact formulas; the lottery loss
  of a cap is checked in the tests against a simulated crowd of 200,000 traders.
- **The frost**: monthly Arabica and Robusta prices from the World Bank's Pink Sheet (nominal US dollars a kilo);
  Brazil's and the world's coffee production by marketing year from USDA's PSD Online (the world is the sum of every
  country in the file); prices in October 2026 dollars deflated by the US CPI (CPIAUCNS). The rough elasticity uses
  midpoint changes between the 1975/76 and 1976/77 world crops and the 1975 and 1977 average prices.
- **The intermission**: eight Pink Sheet series, deflated, each divided by its average in its first twelve months;
  the data melody maps the real price of Arabica (annual means, log scale) to D dorian.
- **The Dials**: the rows of `explainer.economics.dials` for the price elasticity of staples, each with where it was
  read and the date checked.
- **The score** (`explainer/economics/score.py`): the scissors theme, chapter stings, beds under the pauses, and the
  close. Synthesized from sines; nothing recorded.

## Problems and solutions

**1.** *A household's value of one more litre of water a day, with q litres already, is 30e^(−q/28) dollars. Show
that the first 150 litres are worth about $836 in all, while the 150th is worth about 14 cents. Which of the two
numbers does the price of water measure?*

*Solution.* The total is the area under the curve: ∫₀¹⁵⁰ 30e^(−q/28) dq = 30 × 28 × (1 − e^(−150/28)) = 840 × (1 −
0.0047) ≈ $836. The 150th litre is worth 30e^(−150/28) ≈ 30 × 0.0047 ≈ $0.14. A household buys litres until the
next one is worth no more than its price, so the price measures the value of the last litre, the 14 cents, and says
nothing about the $836. Smith's "value in use" was the area; "value in exchange" is the height at the margin.

**2.** *Ana's cups are worth $4.00, $2.50, $1.20 and $0.40; Bo's $3.00, $1.50 and $0.60; Chidi's $5.00 and $2.00.
Draw the market's demand. How many cups are bought at $1.00, and at $2.25?*

*Solution.* Sort every cup by its value: $5.00 (Chidi), $4.00 (Ana), $3.00 (Bo), $2.50 (Ana), $2.00 (Chidi), $1.50
(Bo), $1.20 (Ana), $0.60 (Bo), $0.40 (Ana). The demand curve is the staircase through these heights, one cup wide
each. At $1.00 every cup worth at least a dollar is bought: 7 cups (Ana 3, Bo 2, Chidi 2). At $2.25: 4 cups (Ana 2,
Bo 1, Chidi 1).

**3.** *In Part 1's pit the band is $2.20 to $2.30. Which one card, changed, would narrow it to $2.20 to $2.25?
Which would raise it, and why can the keenest buyer's card rise as far as you like without moving it?*

*Solution.* With six units traded the band is [max(c₆, v₇), min(v₆, c₇)] = [max($2.20, $2.10), min($2.30, $2.40)].
Lowering the seventh seller's cost from $2.40 to $2.25 (or the sixth buyer's value from $2.30 to $2.25) makes the
upper end $2.25, and six units still trade. Raising the seventh buyer's value from $2.10 to anything between $2.20
and $2.30, say $2.28, lifts the lower end to $2.28; raising the sixth seller's cost to $2.25 lifts it to $2.25. The
keenest buyer's card is not one of the four (v₆, v₇, c₆, c₇): she trades at any price in the band, and raising her
card only raises her own surplus.

**4.** *On the demand line Q = 400(1 − p/6), find the elasticity at $2, $3 and $4, and the price at which buyers spend
the most. Show that the answer is the price where the elasticity is −1.*

*Solution.* dQ/dp = −400/6, so ε = (dQ/dp)(p/Q) = −p/(6 − p): −0.5 at $2, −1 at $3, −2 at $4. Spending is
pQ = 400p − 400p²/6, with derivative 400(1 − p/3), zero at p = $3, where spending is 400 × 3 × 0.5 = $600. In
general d(pQ)/dp = Q(1 + ε), which is zero exactly where ε = −1, positive where demand is inelastic and negative
where it is elastic.

**5.** *With that demand and supply Q = 400(p − 0.5)/4.5, a tax of 40 cents a fish is levied on the fishers. Find the
price buyers pay, the price fishers keep, and the buyers' share of the tax; check it against
ε_S/(ε_S + |ε_D|), and show the answer is the same if the buyers pay the tax.*

*Solution.* Write b = 400/6 ≈ 66.7 and d = 400/4.5 ≈ 88.9. Untaxed, 400 − bp = d(p − 0.5) gives p ≈ $2.857 and
Q ≈ 209.5. With the tax, buyers pay p_b and fishers keep p_b − 0.40, and 400 − bp_b = d(p_b − 0.40 − 0.5) gives
p_b ≈ $3.086, so fishers keep ≈ $2.686 and Q ≈ 194.3. Buyers bear (3.086 − 2.857)/0.40 ≈ 57.1%. At the untaxed point
ε_D = −bp/Q ≈ −0.909 and ε_S = dp/Q ≈ 1.212, and ε_S/(ε_S + |ε_D|) = d/(b + d) ≈ 0.571: on straight lines the
formula is exact. If the buyers remit the tax, buyers pay p + 0.40 and fishers keep p, and the same equation results
with p_b = p + 0.40: the same prices paid and kept, the same quantity. The revenue is 0.40 × 194.3 ≈ $77.7 a day and
the deadweight loss ½ × 0.40 × (209.5 − 194.3) ≈ $3.05.

**6.** *On the same lines a cap holds the price at $2.26. Find the shortage, the triangle, and the extra loss if the
fish go by lottery among everyone who wants one. Why can the lottery cost more than the triangle?*

*Solution.* At $2.26 fishers supply Q_S = d(2.26 − 0.5) ≈ 156.4 and buyers want Q_D = 400 − 2.26b ≈ 249.3: a
shortage of about 92.9 fish a day. The triangle is ½ × (209.5 − 156.4) × (P_D(156.4) − 2.26), with
P_D(156.4) = (400 − 156.4)/b ≈ $3.653, so about ½ × 53.1 × 1.393 ≈ $37.0. If the 156.4 fish went to the keenest
buyers, their values would average (6 + 3.653)/2 ≈ $4.83; drawn at random from everyone with a value above $2.26,
they average (6 + 2.26)/2 = $4.13. The difference, 156.4 × (4.83 − 4.13) ≈ $109 a day, is lost on top of the
triangle. The triangle counts only the fish that are not caught; the lottery loses something on almost every fish
that is, and when the shortage is large that is the bigger sum.

**7.** *★ Replace the pit's learning sellers with two Q-learning sellers who meet day after day. Under what
conditions does their price stay above the band, and what evidence would tell a court it was collusion?*

*Solution (a research sketch, not a closed answer).* Each seller's state can be the pair of last prices, its actions
a grid of prices, its reward its profit; the buyers can stay Agora's learning buyers or be replaced by a demand
curve. Calvano and others (2020) found supra-competitive prices sustained by a short punishment after a deviation,
when the sellers are patient (a discount factor near one), explore slowly and see each other's prices; with many
sellers, impatience or noisy prices the result weakens. What separates collusion from competition is not the level
of the price, which demand and costs can also explain, but the response to a deviation: force one seller to cut its
price once and watch whether the other punishes it and both return. In the field, Assad and others (2024) used the
timing of adoption and the structure of local markets; a court would add the algorithms' code and training. The
legal question, whether tacit coordination by programs is an agreement, is open.

## Where it comes back

| Idea | Where |
|---|---|
| prices across goods and years | Part 3, *The Measure* |
| identifying a demand curve from shifts in supply | Part 4, *The Evidence* |
| demand rebuilt from choice; Giffen goods | Part 5, *What People Want*; Part 6, *Demand* |
| the welfare theorems | Part 9, *The Invisible Hand, Proved* |
| one seller, or a few | Part 10, *The Price Maker*; Part 12, *Competition among the Few* |
| hidden quality; spillovers | Part 13, *Lemons and Signals*; Part 15, *Spillovers* |
| the minimum wage | Part 38 |
| tax incidence in public finance | Part 41 |
| market definition and algorithms in competition cases | Part 61 |

## Sources

**Primary texts.**
- A. Smith, *An Inquiry into the Nature and Causes of the Wealth of Nations* (1776), Book I, ch. 4 (Project
  Gutenberg text 3300).
- A. Marshall, *Principles of Economics* (1890), and the third (1895) and fifth (1907) editions, Book V, ch. 3
  (Internet Archive scans principlesecono00marsgoog, principlesofecon01marsrich, principlesofecon01marsuoft). The
  1890 text has the blades of a pair of scissors; the sentence about the upper and under blade is from the later
  editions.
- R. Whately, *Introductory Lectures on Political Economy*, 2nd ed. (1832), Lecture IX (Internet Archive scan
  introductorylect0000unse).
- J. Dupuit, "De la mesure de l'utilité des travaux publics", *Annales des ponts et chaussées*, 2nd series, 8
  (1844).
- V. L. Smith, autobiography, The Nobel Prize in Economic Sciences 2002 (nobelprize.org): the autumn of 1955, the
  plan, January 1956 and the lopsided design.

**Papers.**
- V. L. Smith, "An Experimental Study of Competitive Market Behavior", *Journal of Political Economy* 70 (1962)
  111–137.
- D. K. Gode and S. Sunder, "Allocative Efficiency of Markets with Zero-Intelligence Traders", *Journal of
  Political Economy* 101 (1993) 119–137.
- D. Cliff and J. Bruten, "Zero Is Not Enough: On the Lower Limit of Agent Intelligence for Continuous Double
  Auction Markets", HP Laboratories (1997).
- T. Havranek, Z. Irsova and K. Janda, "Demand for Gasoline Is More Price-Inelastic than Commonly Thought", *Energy
  Economics* 34 (2012) 201–207.
- C. A. Gallet and J. A. List, "Cigarette Demand: A Meta-Analysis of Elasticities", *Health Economics* 12 (2003)
  821–835 (the mean as reported by *Tobacco in Australia*, section 13.1).
- A. C. Wagenaar, M. J. Salois and K. A. Komro, "Effects of Beverage Alcohol Price and Tax Levels on Drinking",
  *Addiction* 104 (2009) 179–190.
- R. Chetty, A. Looney and K. Kroft, "Salience and Taxation: Theory and Evidence", *American Economic Review* 99
  (2009) 1145–1177.
- W. Kopczuk, J. Marion, E. Muehlegger and J. Slemrod, "Does Tax-Collection Invariance Hold? Evasion and the
  Pass-Through of State Diesel Taxes", *American Economic Journal: Economic Policy* 8(2) (2016) 251–286.
- E. L. Glaeser and E. F. P. Luttmer, "The Misallocation of Housing Under Rent Control", *American Economic Review*
  93 (2003) 1027–1046.
- R. T. Deacon and J. Sonstelie, "Rationing by Waiting and the Value of Time: Results from a Natural Experiment",
  *Journal of Political Economy* 93 (1985) 627–647.
- R. Diamond, T. McQuade and F. Qian, "The Effects of Rent Control Expansion on Tenants, Landlords, and Inequality:
  Evidence from San Francisco", *American Economic Review* 109 (2019) 3365–3394.
- E. Calvano, G. Calzolari, V. Denicolò and S. Pastorello, "Artificial Intelligence, Algorithmic Pricing, and
  Collusion", *American Economic Review* 110 (2020) 3267–3297.
- S. Assad, R. Clark, D. Ershov and L. Xu, "Algorithmic Pricing and Competition: Empirical Evidence from the German
  Retail Gasoline Market", *Journal of Political Economy* 132 (2024) 723–771.

**Data.**
- World Bank, Commodity Price Data (The Pink Sheet), monthly prices, update of 3 November 2026; retrieved 18
  November 2026 (CC BY 4.0).
- USDA Foreign Agricultural Service, Production, Supply and Distribution Online, coffee; retrieved 18 November 2026.
- Federal Reserve Bank of St. Louis, FRED: CPIAUCNS (Bureau of Labor Statistics); retrieved 18 November 2026.

**Textbooks.** A. Marshall, *Principles of Economics*, Book V; H. Varian, *Intermediate Microeconomics* (chs 1,
15–16); N. G. Mankiw, *Principles of Economics* (chs 4–8); P. Krugman and R. Wells, *Economics* (chs 3–5).
