# Economics, Built: Part 66, Geoeconomics and Industrial Policy

Part 66 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth of Act XII, *The Frontier*. It asks what happens to the gains from trade
when trade becomes a weapon. Its answer: they shrink, and they are redistributed. A tariff is paid mostly at home,
and a tariff war leaves every side poorer than cooperation; bilateral deficits measure specialization, not
unfairness. Dependence on a hub or a supplier is power for whoever controls it, and resilience is worth buying at the
margin. Industrial policy can build industries when it is temporary, disciplined and aimed at learning that spills
over; subsidy races mostly benefit buyers elsewhere.

It opens in the Rose Garden on 2 April 2025: a tariff on almost every country, at least ten percent, set by one
formula, the bilateral deficit over imports divided by an import elasticity (4) times a pass-through (0.25), then
halved. For Vietnam (2024 imports of $136.6 billion, exports of $13.1 billion) the formula gives 90%, halved 45%;
the published rate was 46%. With a pass-through of 0.945, near the evidence, the same formula gives 12%. Each side's
best case follows. From there it covers:

- what the tariffs did: in 2018-19, complete pass-through to American buyers (Amiti, Redding and Weinstein: $3.2
  billion a month paid and $1.4 billion a month of real income lost by the end of 2018; Fajgelbaum et al.: $51
  billion a year to buyers, $7.2 billion net, 0.04% of GDP), and job losses in exposed manufacturing (Flaaen and
  Pierce); in 2025, the effective tariff rate (customs duties over goods imports) rose from 2.9% to 11.3% by the
  fourth quarter, the highest since the Second World War, and fell to 6.9% by the third quarter of 2026 after the
  Supreme Court's February 2026 ruling on the emergency tariffs; import prices before the tariff did not fall
  (+1.2% in 2025), core goods prices turned from -0.7% in 2024 to +1.4% in 2025, and about a fifth of the tariff had
  reached shelves by September 2025 (Cavallo, Llamas and Vazquez);
- Play it: ten rounds of tariff policy against an unknown partner (tit for tat, never retaliates, retaliates for
  ever); a tariff kept earns 3.1% of a year's income against the partner who never answers and loses 2.8% against
  the others; free trade wins on average;
- trade wars as games, on CEPII's 2019 flows for thirteen economies with deficits purged and theta = 4: the US
  optimal tariff is 25% (+0.48% for the US, -0.27% for the rest), the Nash war is 25% each (-0.59% and -0.17%);
  Bagwell and Staiger's theory of trade agreements; Ossa's Nash tariffs (63%) and the 2.9% cost of a breakdown;
- a uniform 15% US tariff in the quantitative model: +0.42% for the US and -0.18% for its partners without
  retaliation, -0.29% for the US with it (theta = 4; larger losses at theta = 8); imports fall 27% (48% with
  retaliation); in the model foreigners bear about half the tariff in the long run, in the data almost none in the
  first years (dollar pricing; Boehm, Levchenko and Pandalai-Nayar's elasticities of 0.76 and about 2);
- bilateral deficits and the current account: net exports equal saving minus investment; three countries balanced
  overall with a deficit of 60 in every pair; value chains (Johnson and Noguera);
- an intermission: the US trade balance in goods and services, monthly since 1992 (a record -$133.0 billion in March
  2025 as importers rushed ahead of the tariffs, -$60.3 billion in April, -$105.0 billion in September 2026);
- weaponized interdependence (Farrell and Newman): the panopticon and the chokepoint, Iran's banks and SWIFT in 2012,
  Russia's frozen reserves in 2022; dependence as power by the ACR formula (losing a supplier with a fifth of spending
  costs 5.4% of income at theta = 4); Clayton, Maggiori and Schreger's hegemon and its targets' hedging;
- security against efficiency: a firm buys 50% from a supplier that can be cut off, society would choose 25%
  (Grossman, Helpman and Lhuillier); China's share of US imports from 21.6% in 2017 to 16.5% in 2022 and about 9%
  by mid-2025, and dearer goods from Vietnam and Mexico (Alfaro and Chor);
- industrial policy, the old case: Hamilton and List; learning by doing behind a 60% tariff for ten years (costs
  falling 10%, 13% and 19% per doubling of output: the first fails Mill's test, the second passes Mill's but fails
  Bastable's at a 10% discount rate, the third passes both); Baldwin's spillover test;
- the new evidence: Krueger and Tuncer's discouraging regressions and why they mislead; Juhász's Napoleonic
  blockade; Lane's Korean heavy and chemical industry drive; Chinese shipbuilding's subsidies of 13-20% of a ship's
  price (Kalouptsidi; Barwick, Kalouptsidi and Zahur);
- subsidy races (Brander and Spencer): one country's subsidy raises its welfare from 9.00 to 10.13, both
  subsidizing leaves each at 6.48 and buyers in the third market gaining; the CHIPS Act's $52.7 billion and the
  Inflation Reduction Act; China's model, solar capacity and the second China shock;
- the dollar as a hub (57% of the world's foreign exchange reserves in early 2026, from about 71% in 2000), and why
  it is hard to replace;
- the Dials (pass-through, with the 2025 retail evidence; the cost of a tariff war, new); practice, with *Called
  it?*: the FOMC's June 2025 projection of 3.1% core PCE inflation for 2025 against an outcome of 2.8% (partly
  right); three cautions; and the frontier: fragmentation scenarios, Nordhaus's climate club and the EU's border
  carbon adjustment.

## Build it

```bash
python -m videos.economics.econ66.compute              # every number (under a minute), into .cache/econ66/
python tools/qa_scene.py econ66 Games                  # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ66 -q l   # the whole part, silent preview
python tools/build.py econ66                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 66                     # the lab
```

The data are FRED's customs duties and goods imports by quarter (B235RC1Q027SBEA, A255RC1Q027SBEA), the monthly
trade balance (BOPGSTB), core goods prices (CUSR0000SACL1E), import prices excluding food and fuels (IREXFDFLS) and
core PCE prices (PCEPILFE), and CEPII's Gravity database for 2019, all registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md). Everything else is computed, or stated from the papers
listed in `dials.SHOWN[66]`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A tariff by formula | 2 April 2025; the formula and Vietnam's arithmetic; one parameter; each side's best case; objectives |
| 1 | What the tariffs did | 2018-19 pass-through and costs; the effective rate since 2015; prices in 2025 |
| 2 | Play it: a tariff arrives | Ten rounds against an unknown partner; the payoffs |
| 3 | Trade wars as games | The optimal tariff; best responses and the Nash war; why trade agreements exist |
| 4 | A 15% tariff in the quantitative model | Welfare with and without retaliation, by elasticity; who pays in the model and the data |
| 5 | Bilateral deficits and the current account | Saving minus investment; a triangle of balanced countries; value chains |
| — | Intermission | The US trade balance since 1992, as a line and a tune |
| 6 | Weaponized interdependence | Hubs, chokepoints and freezes; dependence as power; geoeconomic power |
| 7 | Security against efficiency | Private and social sourcing; the great reallocation |
| 8 | Industrial policy, the old case | Hamilton and List; learning by doing; Mill, Bastable and Baldwin |
| 9 | Industrial policy, the new evidence | Why the old regressions mislead; Napoleon's blockade; Korea; shipbuilding |
| 10 | Chips, batteries and solar | Brander and Spencer's race; the 2020s subsidies; China's model |
| 11 | The dollar as a hub | Reserve shares; why the dollar persists; what could replace it |
| 12 | The Dials | Pass-through; the cost of a tariff war (new) |
| 13 | In practice | *Called it?*: the FOMC in 2025; ministries, budget offices, supply chains, sanctions; three cautions |
| 14 | Frontier | Fragmentation scenarios; climate clubs and border carbon adjustment |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 67, *The Next Economics* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `tradewar` module (`explainer.economics.agora.tradewar`);
the narration states the cached numbers.

- **The formula.** (m - x)/(epsilon phi m) with epsilon = 4, phi = 0.25 or 0.945, halved, at least 10%.
- **The effective rate and prices.** Customs duties over imports of goods, quarterly, both at annual rates; the core
  goods CPI and import prices excluding food and fuels, January 2025 = 100.
- **The world.** CEPII's 2019 flows (BACI) among the twelve largest economies by GDP and the rest; domestic spending
  as GDP less exports; deficits purged by a first counterfactual with zero deficits.
- **Tariffs.** Exact hat algebra with tariff revenue rebated: shares pi'_ni proportional to pi_ni (w_i (1 + t_ni))^
  (-theta), spending (w_n Y_n + D_n) / (1 - sum_i pi'_ni t_ni/(1 + t_ni)), sales w_i Y_i = sum_n pi'_ni E'_n/(1 +
  t_ni); welfare E'_n / E_n over the price index. Uniform tariffs of 15% without and with retaliation for theta = 2,
  4, 8; the two-bloc game on a grid of tariffs from 0 to 60% in steps of 2.5 points.
- **The repeated game.** Stage payoffs from the two-bloc table at 25%; ten rounds; discount factor 0.9.
- **Power, resilience, infant industries, subsidies.** As described in the module's docstrings: the ACR cutoff loss;
  a 10% cheaper supplier cut off with probability 5% and a convex loss, with a spillover equal to the firm's own;
  unit costs 1.6 (Q/Q0)^(-b) behind a 60% tariff for ten years, a 10% discount rate; Cournot exporters with
  p = 10 - q1 - q2 and c = 1.
- **The intermission.** BOPGSTB, monthly, January 1992 to September 2026; the melody is its quarterly average.

## Problems and solutions

**1.** *The formula: show that with epsilon = 4 and phi = 0.25 the reciprocal rate is half of (m - x)/m; compute it
for Vietnam's 2024 trade, and again with phi = 0.945.*

*Solution.* The rate is (1/2)(m - x)/(epsilon phi m), and epsilon phi = 4 x 0.25 = 1, so it is half of (m - x)/m. For
Vietnam, (136.6 - 13.1)/136.6 = 0.904, halved 0.452: 45%, against a published 46%. With phi = 0.945, epsilon phi =
3.78, so the rate is 0.904/(2 x 3.78) = 0.12: 12%. The parameter that is supposed to measure how much of a tariff
reaches import prices divides the rate, so assuming a quarter instead of nearly all of it multiplies the rate by
almost four.

**2.** *The optimal tariff: a large importer faces foreign export supply with elasticity epsilon\*; show that the
tariff that maximizes its welfare is t\* = 1/epsilon\*.*

*Solution.* Let the world price be p\*(M), rising in imports M with elasticity 1/epsilon\* = (dp\*/dM)(M/p\*). Welfare
is consumer and producer surplus at the domestic price p = (1 + t) p\* plus revenue t p\* M. Choosing the import level
directly, the marginal benefit of a unit of imports is the domestic price p, and its marginal cost to the country
is d(p\* M)/dM = p\* (1 + 1/epsilon\*). Setting them equal gives p = p\* (1 + 1/epsilon\*), so 1 + t = 1 + 1/epsilon\*:
t\* = 1/epsilon\*. A small country faces an infinitely elastic supply and its optimal tariff is zero.

**3.** *Bilateral balances: build three countries whose trade is balanced overall but not pair by pair; what would
tariffs that balanced every pair do to the volume of trade?*

*Solution.* Let A sell 100 to B, B 100 to C, C 100 to A, and each sell 40 back the other way. Each country exports
140 and imports 140, so every overall balance is zero, but A runs a deficit of 60 with C and a surplus of 60 with B,
and so on round the triangle. Balancing every pair requires each pair's flows to be equal, which (with flows that
cannot be redirected) can only be done by cutting the larger flow in each pair from 100 to 40: total trade falls
from 420 to 240, by more than two fifths, with no change in any country's overall balance.

**4.** *Brander and Spencer: with p = a - q1 - q2 and cost c, derive the Cournot quantities under subsidies, the
one-sided optimum s = (a - c)/4 and the Nash subsidies (a - c)/5.*

*Solution.* Firm i maximizes (p - c + s_i) q_i, so a - c + s_i - 2 q_i - q_j = 0. Solving the two first-order
conditions, q_i = (a - c + 2 s_i - s_j)/3. Country 1's welfare is the firm's profit less the subsidy bill,
(p - c) q1, with p - c = (a - c - s1 - s2)/3. So W1 = (a - c - s1 - s2)(a - c + 2 s1 - s2)/9. Its derivative in s1
is zero when a - c - 4 s1 - s2 = 0, so s1 = (a - c - s2)/4: with s2 = 0, s1 = (a - c)/4, which makes firm 1 produce
the Stackelberg leader's quantity (a - c)/2. With both choosing, s = (a - c - s)/4, so s = (a - c)/5. With a = 10 and
c = 1, welfare is 9 each without subsidies, 10.13 for the one that subsidizes alone, and 6.48 each when both do.

**5.** *Dependence: with the ACR formula, show that losing a supplier with spending share s costs 1 - (1 - s)^(1/theta);
evaluate it for s = 0.2 and theta = 2, 4, 8.*

*Solution.* In the models covered by Arkolakis, Costinot and Rodriguez-Clare, real income is proportional to
lambda^(-1/theta), where lambda is the share of spending on the goods that remain available at unchanged prices. If
a supplier with share s disappears and its sales are replaced from the rest at the old prices, the relevant share
rises from 1 - s to 1, so real income falls by the factor (1 - s)^(1/theta), a loss of 1 - (1 - s)^(1/theta). For
s = 0.2: 10.6% at theta = 2, 5.4% at theta = 4, 2.8% at theta = 8.

**6.** *Infant industries: with unit cost c0 (Q/Q0)^(-b), find the cumulative output at which the industry matches
the world price, and state Mill's and Bastable's tests as conditions on b, the tariff's length and the discount
rate.*

*Solution.* The cost equals the world price p when (Q/Q0)^(-b) = p/c0, that is Q = Q0 (c0/p)^(1/b). With a home market
of size d protected for T years, cumulative output after protection is about Q0 + d T, so Mill's test is
Q0 + d T >= Q0 (c0/p)^(1/b): the learning must be fast enough (b large) or the protection long enough. Bastable's test
asks that the discounted value of (p - c_t) q_t over all years be positive: the losses while c_t > p (borne by
consumers through the tariff) must be repaid by the gains once c_t < p, discounted at the rate r. A higher r, a
slower b or a longer T all make it harder to pass. In this part's model, with T = 10 and r = 10%, costs falling 10% per
doubling fail both tests, 13% pass Mill's only, and 19% pass both.

## Lab and interactive

- `python -m videos.economics.labs 66`: the formula; the effective tariff rate; tariffs in the quantitative model with
  and without retaliation; the two-bloc best responses and the Nash war; the repeated game; the ACR cutoff loss;
  resilience; the infant-industry tests; Brander and Spencer.
- The interactive (course site): tradewar. The reader sets the US tariff, the rest of the world's tariff and the
  trade elasticity, and sees each side's real income in a two-region trade model with tariff revenue, and where the
  best responses meet.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[66]`; the Dials (pass-through, with a new
2025 row; the cost of a tariff war, new) are in `explainer/economics/dials.py`, and the *Called it?* record of the
FOMC's June 2025 projection in `explainer/economics/calls.py`. The methods are stated from the works cited in the
chapters (Hamilton 1791, List 1841, Mill 1848, Bastable 1891, Baldwin 1969, Krueger and Tuncer 1982, Brander and
Spencer 1985, Bagwell and Staiger 1999, Dekle, Eaton and Kortum 2008, Gopinath, Itskhoki and Rigobon 2010, Johnson and
Noguera 2012, Arkolakis, Costinot and Rodriguez-Clare 2012, Ossa 2014, Nordhaus 2015, Juhász 2018, Kalouptsidi 2018,
Amiti, Redding and Weinstein 2019, Farrell and Newman 2019, Flaaen and Pierce 2019, Fajgelbaum et al. 2020, Gopinath
et al. 2020, Alfaro and Chor 2023, Boehm, Levchenko and Pandalai-Nayar 2023, Clayton, Maggiori and Schreger 2023,
Grossman, Helpman and Lhuillier 2023, Juhász, Lane and Rodrik 2024, Barwick, Kalouptsidi and Zahur 2025, Cavallo,
Llamas and Vazquez 2025, Lane 2025) and computed here.
