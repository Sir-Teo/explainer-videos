# Economics, Built: Part 36, Trade II: Scale, Firms and Gravity

Part 36 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act VII, *The World Economy*. It asks why most trade is between similar
countries, and what a generation of imports from China did. Its answer: because people want variety and firms have
fixed costs, similar countries trade different versions of the same goods; and because trade falls with distance and
stops at borders, most of it is between large neighbours. Only the best firms export, and trade raises productivity
by moving output to them. Imports from China raised America's income as a whole and devastated the places that made
the same things, and those places have not recovered.

It opens on the *Ideal X* leaving Port Newark on 26 April 1956 with fifty-eight trailers on deck, and on the trade web
of 2019 drawn from CEPII's data. From there it covers:

- two-way trade: America's Grubel-Lloyd indices by end use since 1967 (cars and parts 0.93 in 1967, two years after
  the Auto Pact; capital goods 0.77 in 2025);
- Krugman's love of variety and economies of scale: two identical islands trading raise real wages 26% with
  σ = 4; the home-market effect (55% of demand attracts 59% of the industry);
- a game: did Spain sell more in 2019 to Portugal, Japan or Brazil? ($26.0 billion, $3.2 billion and $3.0
  billion; gravity predicts all three closely);
- gravity on all 28,107 country pairs of 2019: Germany's exports, per dollar of the partner's GDP, fall with distance with a slope of −1.09; least
  squares gives a distance elasticity of −1.18 and PPML with exporter and importer fixed effects −0.71; McCallum's
  border puzzle and Anderson and van Wincoop's multilateral resistance;
- firms: Bernard and Jensen's exporters (10.4% of plants in 1976, 14.6% in 1987, over half of shipments), and the
  Island's firms (19% export and sell 67% of output, nine times larger than the rest);
- Melitz's model derived and computed: opening makes 22% of surviving firms exit and raises productivity and real
  wages 5.9%; the gains grow as shipping gets cheaper; Pavcnik's and Trefler's evidence;
- Eaton and Kortum's Ricardo with a distribution: the trade-share formula against a simulation of 20,000 goods;
- an intermission without narration: America's imports of goods from China, 1985-2025, as a tune;
- one formula for the gains (Arkolakis, Costinot and Rodríguez-Clare) computed for fifteen economies and the rest of
  the world on 2019 data (autarky would cost America 2.8% and Germany 9.1% with θ = 4), and a counterfactual by exact
  hat algebra: trade costs between America and China up 25% cost America 0.22% and China 0.34%, while Mexico gains;
- the China shock: imports from China ($19 billion in 1991, $321 billion in 2007), manufacturing employment (17.3
  million in 2000, 11.5 million in 2010), Autor, Dorn and Hanson's design (−0.596 points per $1,000 per worker; a
  quarter of the decline), and the shift-share logic reproduced on the Island's 400 zones;
- the tariffs of 2018-19 (complete pass-through; buyers lost $51 billion a year, $7.2 billion net) and of 2025
  (America's average tariff on goods 2.6% to 8.0%);
- value chains: the iPhone's accounting (China's value added $6.50 a phone);
- three dials: the trade elasticity (new), pass-through (two rows added), and the local effect of import competition
  (new); the Facts of gravity and few exporters get Agora's column, and two-way trade is explained; *Called it?* on
  Krugman's 1995 estimate of trade and wages (partly right); a frontier chapter.

## Build it

```bash
python -m videos.economics.econ36.compute              # every number (about a minute), into .cache/econ36/
python tools/qa_scene.py econ36 Gravity                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ36 -q l   # the whole part, silent preview
python tools/build.py econ36                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 36                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): CEPII's Gravity database (V202211, Etalab 2.0), an
extract of 2019; from FRED, the Census Bureau's imports from and exports to China, the BLS's manufacturing employment,
the BEA's end-use trade, customs duties and imports of goods; and tables transcribed from Autor, Dorn and Hanson,
Bernard and Jensen, Fajgelbaum et al., Boehm et al., Xing and Detert, McCallum, Krugman and accounts of the *Ideal X*.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Fifty-eight boxes | The *Ideal X*; the trade web of 2019; the question; objectives |
| 1 | Cars for cars | The Grubel-Lloyd index for America since 1967 |
| 2 | Variety and scale | Krugman's model; the gain from trading with an identical country; the home-market effect |
| 3 | Play it: guess the trade | Spain's exports to Portugal, Japan and Brazil, and gravity's predictions |
| 4 | Gravity | Germany's exports against distance; least squares and PPML; borders |
| 5 | Exporters are rare | Bernard and Jensen; the Island's firms |
| 6 | Melitz: selection | Cutoffs, exit and reallocation; gains against shipping costs; the evidence |
| 7 | Eaton and Kortum | Ricardo with a distribution: the formula and a simulation |
| — | Intermission | America's imports from China, 1985-2025, as a tune |
| 8 | One formula, and a counterfactual | The ACR gains on 2019 data; hat algebra for US-China trade costs |
| 9 | The China shock | Imports and jobs; Autor, Dorn and Hanson; shift-share on the Island |
| 10 | The tariffs of 2018 and 2025 | Pass-through and the bill |
| 11 | Value chains | The iPhone's gross and value-added accounting |
| 12 | The Dials | The trade elasticity; pass-through; import competition and local jobs |
| 13 | In practice | Trade-policy modelling and supply chains; *Called it?* on Krugman (1995) |
| 14 | Frontier | Market power, services, time, adjustment, geography |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 37, *Cities and Regions* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's trade (`explainer.economics.agora.trade`, part II) with the
Island's Part 36 truths, or from the Data Room; the narration states the cached numbers.

- **Gravity.** CEPII's 2019 rows for pairs of existing countries with BACI trade recorded; least squares of log trade
  on log GDPs, log population-weighted distance, a shared border, a common official language, a colonial tie and a
  WTO-notified trade agreement; PPML in levels on the same recorded flows (BACI records positive flows), with exporter and importer fixed
  effects concentrated out by their first-order conditions and Newton steps for the rest.
- **The Play-it predictions.** The least-squares gravity equation without the colonial and agreement terms.
- **Krugman.** 1,000 workers, a fixed cost of one worker per variety, σ = 4; the home-market effect with freeness
  φ = 0.3 and an outside good that equalizes wages.
- **Melitz.** Pareto productivity with shape 4.25 and minimum 1, σ = 4, fixed costs of 1 (producing), 1.5 (exporting)
  and 2 (entry), shipping 1.3, exit rate 0.1, two symmetric countries; 4,000 simulated draws for the firms chapter.
- **Eaton and Kortum.** Three islands with technologies 1, 2 and 0.5, θ = 4 and the shipping costs in `island.py`;
  20,000 goods with Fréchet draws.
- **The counterfactual.** The fifteen largest economies by 2019 GDP and the rest of the world; spending on home goods
  is GDP less goods exports (a rough proxy, since GDP is value added and services are left out); exact hat algebra
  with θ = 4 and each region's deficit fixed in units of world income.
- **The Island's zones.** 400 zones with random industry mixes over 30 industries; each industry's import rise has a
  supply part (also seen by other rich countries) and a demand part that raises imports and jobs together; the planted
  effect is −0.6.

## Problems and solutions

**1.** *Variety: with σ = 4, how much do real wages rise when two identical countries trade? When ten do?*

*Solution.* The real wage is proportional to the number of varieties to the power 1/(σ − 1). Doubling varieties raises
it by 2^{1/3} − 1 = 26%; ten countries, by 10^{1/3} − 1 = 115%. Firm size and the markup σ/(σ − 1) = 4/3 are
unchanged: the whole gain is choice.

**2.** *Grubel-Lloyd: America exported $713 billion of capital goods and imported $1,133 billion. Compute the index, and
say what aggregation does to it.*

*Solution.* 1 − |713 − 1,133|/(713 + 1,133) = 1 − 420/1,846 = 0.77. Aggregating different goods into one category raises
the index, since exports of one good can offset imports of another; Grubel and Lloyd's finding survives at fine levels
of detail, but the level of the index depends on the classification.

**3.** *Gravity: with trade ∝ Y_o Y_d / D, how does trade with a partner 5,000 km away compare with one 500 km away of
the same size?*

*Solution.* With a distance elasticity of −1, ten times as far means a tenth of the trade. With the PPML estimate of
−0.71 it is 10^{−0.71} = 0.19, about a fifth; with the least-squares −1.18, 0.066.

**4.** *Home market: with φ = 0.3, show that 55% of demand gives about 59% of firms, and find the share of demand that
attracts all of them.*

*Solution.* s_n = 1/2 + (1 + φ)/(1 − φ)(s_L − 1/2) = 0.5 + (1.3/0.7)(0.05) = 0.593. All firms locate in the larger
country when s_n = 1: s_L = 1/2 + (0.7/1.3)(1/2) = 0.77.

**5.** *Melitz: with Pareto shape 4.25, σ = 4, τ = 1.3 and f_x/f = 1.5, find the share of firms that export.*

*Solution.* The export cutoff is φ_x = τ(f_x/f)^{1/(σ − 1)} φ* = 1.3 × 1.5^{1/3} φ* = 1.488 φ*. With Pareto
productivity the share of survivors above it is 1.488^{−4.25} = 0.185.

**6.** *Gains: America spends 89.4% of its income on home goods. Find the loss from autarky with θ = 4 and with θ = 2.*

*Solution.* 1 − 0.894^{1/4} = 2.8%; 1 − 0.894^{1/2} = 5.4%. A long-run elasticity of two, as Boehm and coauthors
estimate, doubles the measured gains.

**7.** *China shock: exposure rose $1,839 per worker in 2000-07. With a coefficient of −0.596, what fall in the
manufacturing share follows?*

*Solution.* 1.839 × 0.596 = 1.10 percentage points of the working-age population, against an actual fall of 2.00
points over those years: a little over half in that period, and about a quarter of the decline over 1990-2007 by the
authors' conservative reckoning.

**8.** *$\bigstar$ Eaton-Kortum: derive π_ni = T_i (w_i d_ni)^{−θ}/Φ_n from Fréchet productivity draws.*

*Solution.* With P(Z_i ≤ z) = exp(−T_i z^{−θ}), the delivered price p_ni = w_i d_ni / Z_i has
P(p_ni ≥ p) = exp(−T_i (w_i d_ni)^{−θ} p^θ) = exp(−φ_ni p^θ). The probability that i is cheapest is
∫ φ_ni θ p^{θ−1} exp(−φ_ni p^θ) Π_{k≠i} exp(−φ_nk p^θ) dp = φ_ni/Σ_k φ_nk, the stated share; with a continuum of goods
it is also the share of spending, since the distribution of the price paid does not depend on the source.

## Lab and interactive

- `python -m videos.economics.labs 36`: Krugman's gains and the home-market effect, gravity by least squares and PPML
  on CEPII's 2019 data, Melitz's cutoffs and firms, Eaton and Kortum's shares by formula and simulation, the gains
  formula and hat algebra on 2019 trade, and the shift-share design on the Island.
- The interactive (course site): gravity. The reader sets the two countries' sizes, the distance and the distance
  elasticity, and sees the predicted trade and how it compares with real pairs.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[36]`; the trade elasticity, pass-through
and the local effect of import competition are dials (`explainer/economics/dials.py`); Krugman's 1995 estimate is a
*Called it?* entry (`explainer/economics/calls.py`). CEPII's Gravity database (V202211) and FRED's series were
retrieved on 2026-11-20. Autor, Dorn and Hanson's coefficient and exposure figures were checked against NBER Working
Paper 18054; Fajgelbaum et al.'s and Boehm et al.'s numbers against their abstracts; the iPhone figures against Xing and
Detert's abstract and later summaries; the *Ideal X*'s loading costs are McLean's estimates as reported, $5.83 a ton
(the plan's $5.86 was not found in any source).
