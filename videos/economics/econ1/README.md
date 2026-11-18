# Economics, Built: Part 1, Who Feeds Paris?

Part 1 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), opening Act I, *The Question*. It asks how millions of strangers, none of them in
charge, manage to feed a city, and what it takes to study an order that nobody designed and that sometimes fails.

It opens in the 1840s with Frédéric Bastiat's wonder at a sleeping Paris that would starve in days if supplies
stopped, and with the Queen's question at the London School of Economics on 5 November 2008. From there it covers:

- a pit market played by the viewer: twenty traders with private cards, a continuous double auction over six
  periods, and the competitive band the prices find; Chamberlin's market of 1948 against Smith's of 1962, and what
  zero-intelligence traders (Gode and Sunder 1993) show about the work done by the rules;
- one person and two goods: diminishing returns, the production possibilities frontier traced hour by hour,
  opportunity cost as its slope, the margin, and the best day where worth equals cost;
- two people and comparative advantage: Crusoe is faster at both goods and both still gain; the competitive price
  of their trade, the kinked joint frontier, and Ricardo's four numbers of 1817;
- Adam Smith's pin factory, 4,800 pins a man against at most 20, his three reasons, the extent of the market, and
  Leonard Read's *I, Pencil*;
- Hayek's tin: sixty users who see only a price, a mine that closes, the price that clears, who cuts back, and what
  equal rationing would waste and would need to know;
- incentives, and the day-care fine in Haifa that raised late pick-ups (Gneezy and Rustichini 2000), as a
  difference in differences;
- the long view: income per head from the year 1 to 2022, compounding and the rule of 70, the log scale, the Great
  Divergence and the convergence since;
- an intermission without narration: two hundred years of every country's income in thirty-three seconds, under
  the world's income played as a tune;
- what a model is (Borges's map, Friedman's billiard player, Rodrik's library of models), and Hume's line between
  *is* and *ought*;
- 1929 against 2008 in four charts, the forecasters' call for 2009, and the British Academy's letter to the Queen;
- the economy as plumbing, from Quesnay's *Tableau* (1758) and Phillips's water machine (1949) to the series map;
- the series' devices: Agora, the Island, the Facts, the Dials, Called it?, and the tags on every number;
- where economists work, and a frontier chapter on Coase's question and Simon's Martian.

## Build it

```bash
python -m videos.economics.econ1.compute              # every number (about ten seconds), into .cache/econ1/
python tools/qa_scene.py econ1 Pit                    # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ1 -q l   # the whole part, silent preview
python tools/build.py econ1                           # 1080p30 with narration and the series' computed score
python tools/build.py econ1 --no-score                # the same, without the score
python -m explainer.economics.data                    # the Data Room: what is frozen, and when
python -m pytest tests/economics                      # Agora, the Data Room, the Facts, the Dials, the score
```

The data are frozen extracts in `explainer/economics/data/`, retrieved on 18 November 2026 and registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md); `python -m explainer.economics.data --refresh
maddison2023 fred spf` downloads them again and reports whether they changed.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Who feeds Paris? | Paris at night as Bastiat saw it, eighty departments sending supplies with no plan; the title; the Queen's question and the British Academy's answer; the order and its failure; three questions; objectives |
| 1 | Play it: the pit | Your card: a buyer at $2.70. The rules of Smith's double auction; a prediction; six periods of trading by Agora's learning traders; the cards turned into demand and supply; the band $2.20 to $2.30; Chamberlin, Smith, and zero-intelligence traders; the first Fact |
| 2 | One person, two goods | Crusoe's ten hours; F = 3√h and C = 4√(10 − h); the hour-by-hour cost of a fish; the frontier traced; opportunity cost as its slope, derived; the margin; the best day, where the two slopes equal 1.63 |
| 3 | Two people: comparative advantage | Crusoe faster at both; the opportunity-cost table; alone, then specialized; the competitive price 0.6 inside the band 0.5 to 0.8; both outside their own frontiers; the kinked joint frontier; Ricardo's cloth and wine |
| 4 | The pin factory | Smith's eighteen operations; 12 pounds × 4,000 = 48,000 pins for ten men; 4,800 against at most 20, to scale; dexterity, time, machines; the extent of the market; *I, Pencil* |
| 5 | Prices as messages | Hayek's tin; sixty users with their own elasticities; a mine closes; the price climbs to 1.172; cuts from 3% to 33% by substitute; equal rationing leaves last units worth 1.09 to 2.81 and loses 3.5% more; 120 numbers against one; the dials, and two caveats |
| 6 | Incentives | People respond to incentives; the Haifa day-care fine; the weekly data; the difference in differences, about 9 more late pick-ups a week; a fine is a price; the record |
| 7 | The long view | GDP per head from the year 1; England from 1252; the hockey stick; compounding, doubling times of 423 and 52 years; the log scale; the Great Divergence and the convergence; the second Fact |
| | Intermission: two hundred years | No narration: every country's GDP per head and population, 1820 to 2022, under the world's GDP per head as a tune; the story so far |
| 8 | What a model is | Borges's map; the pit as a model, what it kept and left out; Friedman and Rodrik; Hume, and the is/ought card |
| 9 | When the order fails | 1929 and 2008 from their peaks: industrial production, unemployment, prices, real GDP; Called it?: the forecasters' August 2008 call for 2009; the British Academy's letter |
| 10 | The economy as plumbing | Quesnay's zigzag and Phillips's machine, drawn; the Tableau, sealed, with the part that opens each pipe; the twelve acts |
| 11 | How we will know | Agora's first three modules; the Island and its cast; the Facts; the Dials; the tags on every number |
| 12 | In practice: what economists are paid to do | The central bank, the treasury, the competition authority, the platform, development, the firm |
| 13 | Frontier: how much of the economy is a market? | Coase's question of 1937; Simon's Martian of 1991, drawn; three open questions; the research problem |
| | Recap, problems, and the road ahead | The answer; ten lines; problems; reading; a boat comes ashore with Part 2's problem |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora, the Data Room or a transcribed table, and the narration
states the cached numbers.

- **The pit** (`agora.market`): ten buyers' values ($3.40 down to $1.50) and ten sellers' costs ($1.20 up to $3.00),
  so the competitive quantity is 6 and every price from $2.20 to $2.30 clears the market; the largest possible
  gain is $6.70. Forty-one runs of six periods each, by Cliff's (1997) margin-adjusting traders and by Gode and
  Sunder's (1993) zero-intelligence traders. The run shown is the median of the 41 by last-period convergence,
  chosen by rule. Smith's coefficient α falls from about 12 to about 2 for the learning traders, and stays near 16
  for the random ones, which still capture about 95% of the gains.
- **Crusoe** (`agora.crusoe`): F = 3√h, C = 4√(10 − h), U = 0.6 ln F + 0.4 ln C; best day at h = 6, with the
  marginal rate of substitution and of transformation both 1.633.
- **Crusoe and Friday**: 1 and 2 hours per fish, 2 and 2.5 per coconut, 12 hours each, the same tastes; the
  competitive equilibrium is found by root-finding and checked to lie strictly inside the band of opportunity costs.
- **Hayek's tin** (`agora.signals`): sixty users with demands a·p^(−ε), sizes lognormal and ε from 0.1 to 2.5
  (seed 1945); a 20% cut in supply; the clearing price, reached also by tâtonnement; the value given up, by
  numerical integration under each user's inverse demand, for the price and for equal rationing.
- **The fine**: Gneezy and Rustichini's Table 1 transcribed (ten centres, twenty weeks) and checked against their
  Table 2 (whose twelve-week means are truncated, not rounded, to one decimal); averages and the difference in
  differences computed.
- **The long view and the intermission**: the Maddison Project Database 2023, world and regional series (1820 to
  2022) and 169 countries; growth rates from endpoints in logs; the data film interpolates log GDP per head between
  benchmark years. The data melody maps the world's GDP per head (log scale) to D dorian.
- **The collapses**: FRED series retrieved 18 November 2026: industrial production (INDPRO), consumer prices
  (CPIAUCNS), unemployment (UNRATE from 1948; NBER m08292a for 1929 to 1942, National Industrial Conference Board
  estimates), real GDP (GDPCA), each from the NBER peaks of August 1929 and December 2007.
- **Called it?**: the Survey of Professional Forecasters' median forecasts (2008 surveys) against real GDP as now
  measured; 2009's fall is checked to be the largest since 1946.
- **The score** (`explainer/economics/score.py`): the scissors theme, chapter stings in which the two voices close
  in chapter by chapter, beds under the pauses, and the close. Synthesized from sines; nothing recorded.

## Problems and solutions

**1.** *Crusoe catches F = 3√h fish and gathers C = 4√(10 − h) coconuts. Show that a fish costs (4/3)√(h/(10 − h))
coconuts; evaluate it at h = 5, and say why it rises with h.*

*Solution.* dF/dh = 3/(2√h) and dC/dh = −4/(2√(10 − h)) (an hour moved to fishing is taken from the palms). The
cost of a fish is −dC/dF = (dC/dh)/(dF/dh) in magnitude: [4/(2√(10 − h))]/[3/(2√h)] = (4/3)√(h/(10 − h)). At h = 5
it is 4/3 ≈ 1.33 coconuts. It rises with h for two reasons at once: each extra hour of fishing adds fewer fish (the
marginal product of fishing falls), and each hour taken from the palms is taken from a smaller stock, so it costs
more coconuts (the marginal product of gathering rises as hours there shrink). The frontier therefore bows outward.

**2.** *Ana needs 2 hours per fish and 3 per coconut; Bo needs 4 and 4. Who has an absolute advantage in what, who
a comparative advantage, and at what prices (coconuts per fish) do both gain from trade?*

*Solution.* Ana is faster at both (2 < 4 and 3 < 4), so she has the absolute advantage in both. A fish costs Ana
2/3 of a coconut and Bo 1 coconut, so Ana has the comparative advantage in fish; a coconut costs Ana 1.5 fish and
Bo 1 fish, so Bo has it in coconuts. Any price strictly between 2/3 and 1 coconut per fish makes both better off:
Ana sells fish for more coconuts than they cost her to make, and Bo buys fish for fewer coconuts than they would
cost him.

**3.** *Buyers' cards: $5, $4, $3, $2, $1. Sellers' cards: $1.50, $2.50, $3.50, $4.50, $5.50. Find the competitive
quantity, the price band and the largest total gain. A sixth seller arrives with a $1.00 card: what changes?*

*Solution.* Pair the values from the highest down with the costs from the lowest up: 5 ≥ 1.5, 4 ≥ 2.5, but 3 < 3.5,
so two units trade. The price must leave exactly two willing buyers and two willing sellers: at least the second
seller's $2.50 and the third buyer's $3, and at most the second buyer's $4 and the third seller's $3.50; the band
is $3.00 to $3.50. The largest gain is (5 + 4) − (1.5 + 2.5) = $5. With the new seller the costs are 1, 1.5, 2.5,
3.5, ...: now 3 ≥ 2.5, so three units trade; the band is max(2.5, 2) = $2.50 to min(3, 3.5) = $3.00, and the gain is
(5 + 4 + 3) − (1 + 1.5 + 2.5) = $7. More supply: a lower price, more trade, and $2 more surplus.

**4.** *In Haifa the fined centres averaged 8.0, 16.4 and 18.7 late pick-ups a week before, during and after the
fine; the others 10.0, 9.2 and 8.25. Compute the difference in differences for each period, and state the
assumption it rests on.*

*Solution.* During: (16.4 − 8.0) − (9.2 − 10.0) = 8.4 + 0.8 = 9.2 more late pick-ups a week per centre. After the
fine was removed: (18.7 − 8.0) − (8.25 − 10.0) = 10.7 + 1.75 = 12.45. The estimate assumes parallel trends: without
the fine, the fined centres would have changed by as much as the others did. Random assignment makes that
plausible, since nothing but chance distinguishes the two groups; with only ten centres, chance differences can
still be sizable, which is why the paper's finding needs replication (Part 45).

**5.** *Derive the rule of 70. How long does income take to double at 0.164% a year, and at 1.334%? By what factor
does it rise in a century at 2%?*

*Solution.* With continuous growth at rate g, y(T) = y(0)e^(gT); doubling means e^(gT) = 2, so T = ln 2 / g ≈ 0.693/g,
which is 69.3 divided by the growth rate in percent: "about 70". At 0.164%, T = 0.693/0.00164 ≈ 423 years; at
1.334%, T ≈ 52 years. A century at 2% multiplies income by e^2 ≈ 7.4 (or 1.02^100 ≈ 7.2 with annual compounding).

**6.** *A city fines littering, and complaints about litter rise. Give two explanations other than "the fine caused
more littering", and a design that would tell them apart.*

*Solution.* (a) Measurement: the fine made people more aware of litter, or gave them a reason to report it, so
complaints rose with no change in littering. (b) Timing: littering was rising anyway (more visitors, a festival
season, fewer street cleaners) and the fine coincided with it. (c) The day-care mechanism itself, which is what the
question excludes. A design: choose districts at random to get the fine, and count litter directly on fixed routes,
before and after, in fined and unfined districts alike; compare the changes. Counting litter rather than complaints
separates (a) from the rest, and the unfined districts measure (b).

**7.** ★ *Simon's Martian, measured: for one country, estimate how much economic activity is coordinated inside
firms rather than between them through markets. What data would you need, and what would mislead you?*

*Solution (a research sketch, not a closed answer).* Input–output tables record purchases between industries: those
are market transactions between firms, which the Martian sees as red lines. Value added and employment by firm
record what happens inside the green areas. A first measure is the share of gross output that is value added within
firms rather than bought from other firms, by industry and over time. Trade statistics that separate transactions
between related parties (a parent and its affiliates) from arm's-length ones show the line inside firms that cross
borders. What misleads: an industry table aggregates many firms, so purchases inside a firm with several
establishments can appear as market transactions; transfer prices inside multinationals look like prices but are
set by authority; platforms (a ride-hailing app, a marketplace) are firms that run markets, and franchises and
long-term contracts sit between the two. The place to start in the series is the production network of Part 63 and
the economics of the firm in Part 62.

## Where it comes back

| Idea | Where |
|---|---|
| demand and supply built from the cards | Part 2, *The Scissors* |
| what people want, and the best choice | Part 5, *What People Want*; Part 6, *Demand* |
| why firms exist and where they end | Part 8, *The Firm*; Part 62, *Inside the Firm* |
| an economy-wide price system, and the calculation debate | Part 9, *The Invisible Hand, Proved* |
| incentives and contracts | Part 14, *Incentives*; Part 45, *Behavioural Economics* |
| designed markets | Part 16, *Auctions*; Part 17, *Markets by Design* |
| the long-run escape | Parts 19 to 21 |
| crises and forecasts | Part 26, *Banks and Runs*; Part 33, *Crises*; Part 57, *Reading the Economy in Real Time* |
| comparative advantage between countries, and who loses | Part 35, *Trade I* |
| the difference in differences | Part 4, *The Evidence* |

## Sources

**Primary texts.**
- F. Bastiat, *Economic Sophisms*, First Series (1845), ch. 18, "There Are No Absolute Principles"; transl. A.
  Goddard (Foundation for Economic Education, 1964).
- A. Smith, *An Inquiry into the Nature and Causes of the Wealth of Nations* (1776), Book I, chs 1 and 3 (Cannan
  edition, 1904).
- D. Ricardo, *On the Principles of Political Economy and Taxation* (1817), ch. 7.
- D. Hume, *A Treatise of Human Nature*, Book III (1740), Part I, section I.
- F. Quesnay, *Tableau économique* (1758).
- J. L. Borges, "Del rigor en la ciencia" (1946).
- L. E. Read, "I, Pencil", *The Freeman*, December 1958.

**Papers.**
- F. A. Hayek, "The Use of Knowledge in Society", *American Economic Review* 35 (1945) 519–530.
- R. H. Coase, "The Nature of the Firm", *Economica* 4 (1937) 386–405.
- E. H. Chamberlin, "An Experimental Imperfect Market", *Journal of Political Economy* 56 (1948) 95–108.
- V. L. Smith, "An Experimental Study of Competitive Market Behavior", *Journal of Political Economy* 70 (1962)
  111–137.
- D. K. Gode and S. Sunder, "Allocative Efficiency of Markets with Zero-Intelligence Traders", *Journal of
  Political Economy* 101 (1993) 119–137.
- D. Cliff, "Minimal-Intelligence Agents for Bargaining Behaviours in Market-Based Environments", HP Laboratories
  Technical Report HPL-97-91 (1997).
- U. Gneezy and A. Rustichini, "A Fine Is a Price", *Journal of Legal Studies* 29 (2000) 1–17.
- M. Friedman, "The Methodology of Positive Economics", in *Essays in Positive Economics* (1953).
- H. A. Simon, "Organizations and Markets", *Journal of Economic Perspectives* 5(2) (1991) 25–44.
- A. W. Phillips, "Mechanical Models in Economic Dynamics", *Economica* 17 (1950) 283–305.
- T. Besley and P. Hennessy, letter to Her Majesty The Queen, 22 July 2009, *British Academy Review* 14 (2009) 8–10.

**Data.**
- J. Bolt and J. L. van Zanden, "Maddison-style estimates of the evolution of the world economy: a new 2023
  update", *Journal of Economic Surveys* (2024); the Maddison Project Database 2023 (CC BY 4.0). Country sources for
  the series drawn: England and the UK, S. Broadberry, B. Campbell, A. Klein, M. Overton and B. van Leeuwen,
  *British Economic Growth 1270–1870* (2015); Holland, J. L. van Zanden and B. van Leeuwen, *Explorations in Economic
  History* 49 (2012); the year 1, W. Scheidel and S. J. Friesen, *Journal of Roman Studies* 99 (2009); China, S.
  Broadberry, H. Guan and D. D. Li, *Journal of Economic History* 78 (2018); India, S. Broadberry, J. Custodis and
  B. Gupta, *Explorations in Economic History* 55 (2015); Japan, J.-P. Bassino, S. Broadberry, K. Fukao, B. Gupta and
  M. Takashima (2018); Korea, M. S. Cha et al., *Historical Statistics of Korea* (2020); Nigeria and Ethiopia, S.
  Broadberry and L. Gardner, *Explorations in Economic History* 83 (2022); the United States, *Historical Statistics
  of the United States* (2006).
- Federal Reserve Bank of St. Louis, FRED: INDPRO (Federal Reserve Board), CPIAUCNS and UNRATE (Bureau of Labor
  Statistics), GDPCA and GDPC1 (Bureau of Economic Analysis), M0892AUSM156SNBR (NBER Macrohistory Database, m08292a);
  retrieved 18 November 2026.
- Federal Reserve Bank of Philadelphia, Survey of Professional Forecasters, median forecasts of real GDP and of the
  probability of a decline; retrieved 18 November 2026.

**Textbooks.** The CORE Team, *The Economy* (units 1–2); N. G. Mankiw, *Principles of Economics* (chs 1–3); R.
Heilbroner, *The Worldly Philosophers*; D. Rodrik, *Economics Rules* (2015).
