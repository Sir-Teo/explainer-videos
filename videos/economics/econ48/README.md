# Economics, Built: Part 48, Environment and Climate

Part 48 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth of Act IX, *The Fields*. It asks what a tonne of carbon dioxide is worth,
and what the answer turns on. Its answer: between about 30 and 200 dollars on most estimates, and more if the newest
work on global damage is right; above all it turns on the discount rate, a judgment about how much the future counts,
then on how large and how lasting the damage is, and on the risk of the worst. Where things have owners, prices
manage scarcity; where they do not, a price has to be built.

It opens on the bet: in 1980 Julian Simon bet Paul Ehrlich that any raw materials he chose would be cheaper, after
inflation, in ten years. Ehrlich chose chromium, copper, nickel, tin and tungsten, $200 of each; all five fell, and in
October 1990 he mailed Simon a cheque for $576.07. The three of those metals the World Bank prices (copper, nickel and
tin, from its Pink Sheet, deflated by the US CPI) lost 38% as a bundle over the decade of the bet. From there it
covers:

- exhaustible resources: Hotelling's rule derived from the owner's arbitrage, an Island mine whose price climbs to
  its choke price as the rent grows 5% a year (the mine is empty in year 43), a falling extraction cost that makes the
  price fall for 20 years before it rises (Slade's U), and the record: from 1960 to 2024 the real prices of copper,
  nickel and tin ended within about a third of where they started (1.27, 0.97 and 1.29 times), while a rent growing
  at 5% would have grown more than twentyfold;
- the bet rerun for every ten-year window from 1960 to 2014: Ehrlich would have won 28 of 55, about half; Kiel,
  Matheson and Golembiewski's rerun with all five metals over 1900-2008 gives him 61.6% of 99 decades;
- the fishery: Gordon's sustained-yield curve, open access against a sole owner or a quota (stock 0.2 against 0.6 of
  its natural size), Smith's fleet dynamics with an overshoot to 3% of the natural stock, a traded quota that keeps it
  at 72%; FAO's share of assessed stocks overexploited, 10% in 1974 and 35.5% in 2021; Costello, Gaines and Lynham on
  catch shares;
- the climate in four equations (the IPCC's four-box carbon impulse response, the concentration, forcing with other
  gases and sulphur, a two-layer energy balance with an equilibrium sensitivity of 3 degrees), fitted here to Mauna
  Loa (0.8 ppm average error) and HadCRUT5 (the last decade 1.30 degrees in the model and in the thermometers);
- a DICE-style model built on it: the Ramsey economy of Part 20 with DICE-2023's damages (3.1% of output at
  3 degrees), its backstop ($515 a tonne in 2050) and an optimal emissions-control path; business as usual reaches
  3.1 degrees in 2100, the optimum 2.6, with 38% of emissions cut by 2050 at a carbon price of $110 (DICE-2023: 2.6
  degrees, 39%, $115);
- Play it: the reader chooses a discount rate; the social cost of carbon is $561 at 1%, $183 at 2%, $88 at 3% and
  $37 at 5% (DICE-2023: $485, $176, $87, $32), with 31% of it, at 3%, from damage after 2100;
- the Ramsey rule r = rho + eta g; with rho 1.5% and eta 1.45 a tonne costs $63 and warming peaks at 2.7 degrees;
  with the Stern Review's 0.1% and log utility it costs $408, emissions end by 2060 and warming peaks at 1.9; an
  is/ought card; official and academic estimates (DICE-2016R $31, the US interim figure $51, DICE-2023 $66, Rennert et
  al. $185, EPA $190);
- an intermission of HadCRUT5's warming since 1850-1900, year by year, as stripes and as a tune;
- fat tails: with the same median sensitivity, thin tails give a 0.3% chance of more than 6 degrees and fat tails
  5.5%; with damages that steepen above 6 degrees, the certainty-equivalent loss is about 5% under thin tails whatever
  the cut-off, and 8% to 96% under fat tails as the cut-off rises from 6 to 20 degrees (Weitzman's dismal theorem in
  miniature); Dietz et al.'s tipping points (+25%, with a 10% chance of doubling);
- instruments: prices against quantities when damage is flat (Weitzman, as in Part 15); British Columbia's
  revenue-neutral tax (C$10 in 2008 to C$30 in 2012, C$80 in 2024, abolished in April 2025); the EU's permit market
  (2005; above EUR 100 for the first time in February 2023); standards and subsidies;
- leakage and the EU's border adjustment (reporting from October 2023, paying from January 2026); a climate club on
  the Island that unravels to nobody without a penalty tariff and holds all fifteen countries with one of 9%;
- learning curves: solar module prices fell 99.9% from 1975 to 2025, about 30% with each doubling of installed
  capacity in 2000-2025; a toy of Acemoglu, Aghion, Bursztyn and Hemous's directed technical change;
- damages measured: Dell, Jones and Olken; Burke, Hsiang and Miguel's specification run here on ERA5 temperatures and
  World Bank growth for 185 countries, 1961-2023 (output peaks near 10.5 degrees; a degree warmer costs a country
  averaging 25 degrees about a point of growth); air conditioning and heat deaths; the Huai River;
- electricity: the Island's merit order, a day's prices, and a firm that multiplies its profit 28 times by holding
  back 2 of its 14 gigawatts at the peak; California's summer of 2000 (59% of the rise in spending was market power);
- three dials (the social cost of carbon; the price elasticity of gasoline and electricity; the effect of a warmer
  year on growth), practice, *Called it?* on Hubbert's 1956 peak (partly right) and a frontier of global damage
  estimates, stranded reserves and adaptation.

## Build it

```bash
python -m videos.economics.econ48.compute              # every number (about a minute), into .cache/econ48/
python tools/qa_scene.py econ48 Dice                   # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ48 -q l   # the whole part, silent preview
python tools/build.py econ48                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 48                     # the lab
```

The data are in `explainer/economics/data/`: the World Bank's Pink Sheet (copper, nickel, tin, oil) and the US CPI;
NOAA's Mauna Loa CO2; HadCRUT5; the Global Carbon Budget's emissions and CEDS sulphur dioxide via Our World in Data;
ERA5 country temperatures via Our World in Data and the World Bank's GDP per head; IRENA's solar prices and capacity,
FAO's fish stocks and the Energy Institute's oil production, via Our World in Data; all registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The bet | Simon and Ehrlich; three metals through the decade; the question; objectives |
| 1 | Exhaustible resources | Hotelling's rule derived; the Island's mine; falling costs; the record since 1960 |
| 2 | The bet, rerun | Every ten-year window since 1960; Kiel et al.; right or lucky |
| 3 | Renewable resources: the fishery | Sustained yield, open access and quotas; the fleet's overshoot; FAO; catch shares |
| 4 | The largest externality | Emissions; the four equations; the fits to Mauna Loa and HadCRUT5 |
| 5 | A climate-economy model, built | The structure; business as usual against the optimum; against DICE-2023 |
| 6 | Play it: choose the discount rate | A tonne's damage stream; your rate; the social cost by rate |
| 7 | The social cost of carbon: ethics and evidence | Ramsey's rule; two worlds; is and ought; official estimates |
| — | Intermission | The world's warming, 1850-2025, as stripes and a tune |
| 8 | Fat tails | Thin and fat beliefs; the cut-off; tipping points |
| 9 | Taxes, permits and standards | Prices against quantities; British Columbia; the EU's market; other instruments |
| 10 | Leakage, borders and clubs | Leakage and the CBAM; the club and its tariff |
| 11 | Learning curves and directed technical change | Solar's prices; Wright's law; a toy of AABH |
| 12 | Damages measured | The design; the curve estimated here; heat, air conditioning, the Huai River |
| 13 | Electricity markets | The merit order and what a carbon price does to it; a day; withholding; California, 2000 |
| 14 | The Dials | Carbon, energy elasticities, warm years |
| 15 | In practice: energy, carbon and regulation | Who uses this; *Called it?* (partly right) |
| 16 | Frontier | Global damage and its social cost of carbon; the reserves left unburned; adaptation |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 49, *The Economic Approach* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's climate (`explainer.economics.agora.climate`) with the
Island's Part 48 truths, or from the data named above; the narration states the cached numbers.

- **Metals and the bet.** Annual means of the Pink Sheet's monthly prices, divided by the annual US CPI; for every
  starting year the real change in an equal-value bundle of copper, nickel and tin over ten years.
- **The mine.** Linear demand q = 10 - p, a stock of 200, interest 5%, extraction cost 2 (or 6 falling 4% a year); the
  rent at year 0 solved so that cumulative extraction equals the stock.
- **The fishery.** Logistic growth 0.5 S (1 - S), catch E S, price 1, cost 0.2 per unit of effort; open access by
  dE/dt = 2 x profit per unit of effort; the quota caps the catch at 0.1 a year.
- **The climate.** Emissions (fossil, and land use weighted by a fitted 0.55) into the IPCC AR5 four-box impulse
  response (Joos et al. 2013) with its three finite timescales scaled by a fitted 0.47; forcing 5.35 ln(C/278) times
  a fitted 1.36 for the other gases, less a fitted 0.44 W/m2 per 100 Mt of SO2; a two-layer energy balance (heat
  capacities 7.3 and 106, exchange 0.73) with an equilibrium sensitivity of 3 degrees. The fits minimize squared
  errors against Mauna Loa (1959-2025) and HadCRUT5 (1850-2025, against its 1850-1900 mean).
- **The DICE-style model.** Annual, 2025-2300: population rising to 10.3 billion, output $150 trillion in 2025 (2019
  dollars at PPP), capital share 0.3, depreciation 5%, saving 25%, TFP growth 1.2% a year declining; emissions
  intensity falling 1.5% a year (the decline slowing 0.1% a year); land-use emissions 4.4 GtCO2 falling 2% a year;
  abatement cost theta1 mu^2.6 with the backstop at $515 in 2050 (rising 1% a year back to 2025, falling 0.1% a year
  after); damages 0.031/9 T^2; welfare with rho and eta; the optimal path by L-BFGS-B over control rates at 5-year
  nodes, never falling and rising at most 15 points in five years (capital turns over slowly); the social cost of
  carbon from a 1 GtCO2 pulse in 2025.
- **Fat tails.** 200,000 draws of the sensitivity: log-normal (median 3, log-sd 0.25) or log-Student-t with 2 degrees
  of freedom; damages 1 - 1/(1 + 0.00344 T^2 + (T/6.5)^7); certainty equivalents with relative risk aversion 2.
- **The club.** Fifteen countries with log-normal sizes and costs and damages that vary around 1% and 3% of output;
  best-response leaving and joining until stable.
- **Directed technical change.** Clean and dirty inputs with elasticity 3; scientists to the sector with the larger
  (subsidized, taxed) profit index A^(eps-1); productivity grows 2% a year where they work.
- **The panel.** Growth of log GDP per head on temperature and its square, with country and year fixed effects and
  country-specific linear and quadratic trends, clustered by country (Burke, Hsiang and Miguel's specification);
  observations with growth beyond 50% either way dropped; the poorer half are countries below the median GDP per head
  in their first year from 1980.
- **The power market.** Seven plants (capacities and costs in the island file), a price cap of 250, a day's load; a
  firm's profit as it withholds capacity from its costliest plant first. A carbon price of $50 a tonne adds 50 times
  each plant's typical tonnes per MWh (coal 1.0, the two gas plants 0.37 and 0.40, peakers 0.55, oil 0.75) to its
  cost, and the merit order is sorted again.

## Problems and solutions

**1.** *Hotelling: the interest rate is 5%, extraction costs 2 a ton and the price today is 5. What does the rule
predict for the price in ten years? What if the cost falls 4% a year?*

*Solution.* The rent today is 5 - 2 = 3, and it grows at 5%: 3 x 1.05^10 = 4.89. With a constant cost the price in
ten years is 2 + 4.89 = 6.89. If the cost falls 4% a year it is 2 x 0.96^10 = 1.33, and the price is 1.33 + 4.89 =
6.22: the rule fixes the rent's path, and the price depends on what happens to cost.

**2.** *The fishery: stock grows 0.5 S(1 - S), catch is E S, fish sell at 1 and effort costs 0.2. Find the
open-access effort and stock, the rent-maximizing effort and its rent, and the maximum sustainable yield.*

*Solution.* In a steady state growth equals catch, so S = 1 - 2E and the sustained catch is Y(E) = E - 2E^2. Open
access drives effort until revenue equals cost: 1 - 2E = 0.2, so E = 0.4 and S = 0.2. Rent Y - 0.2E is greatest
where 1 - 4E = 0.2: E = 0.2, S = 0.6 and the rent is 0.2 - 0.08 - 0.04 = 0.08. The maximum sustainable yield is at
1 - 4E = 0, E = 0.25, a catch of 0.125: the rent-maximizing fleet is smaller even than that.

**3.** *Discounting: what is a dollar of damage in 75 years worth today at 1%, 3% and 5%? And 5 dollars a year
forever?*

*Solution.* 1/1.01^75 = 0.47, 1/1.03^75 = 0.11 and 1/1.05^75 = 0.026. A perpetuity of 5 a year from next year is
worth 5/r: 500, 167 and 100.

**4.** *Ramsey: with growth of 1.75% a year, find the discount rate for rho = 0.1%, eta = 1 and for rho = 1.5%,
eta = 1.45.*

*Solution.* r = rho + eta g: 0.1 + 1 x 1.75 = 1.85%, and 1.5 + 1.45 x 1.75 = 4.04%. The model's social cost of carbon
is about $408 a tonne with the first and $63 with the second.

**5.** *Prices or quantities: damage is a flat 50 a tonne; the cost of cutting q tonnes is theta + q at the margin,
with theta = 30 or 50, equally likely. Compare a tax of 50 with a cap at the expected optimum.*

*Solution.* The optimum cuts until theta + q = 50: q = 20 if theta = 30, and q = 0 if theta = 50. A tax of 50 makes
firms cut exactly that in each case, so it loses nothing. A cap fixes q at the expected optimum, 10. If theta = 30
it cuts 10 too few, losing the area between 50 and 30 + q from 10 to 20: 50. If theta = 50 it cuts 10 too many,
losing the area between 50 + q and 50 from 0 to 10: 50. The cap's expected loss is 50; the tax's is zero, because
the damage line is flat.

**6.** *Learning: with a learning rate of 20%, how far has the price fallen after five doublings of output?*

*Solution.* Each doubling multiplies the price by 0.8, so five give 0.8^5 = 0.33: a fall of 67%. In Wright's law
log p = a + b log Q, b = log2(0.8) = -0.32.

**7.** *Withholding: using the Island's power plants and a load of 35 GW, find Dynamo's profit when it offers
everything and when it holds back just over 2 GW of gas B.*

*Solution.* In merit order the plants offer 5 (hydro), 13, 23, 30 (gas A, Dynamo's) and 37 GW (gas B, Dynamo's), so
gas B is the last plant needed and the price is 48. Dynamo earns (48 - 45) x 7 = 21 on gas A and nothing on gas B:
21 thousand dollars an hour. Holding back just over 2 GW of gas B leaves just under 35 GW of plants up to gas B, so
the peakers set the price at 95. Dynamo earns (95 - 45) x 7 = 350 on gas A and (95 - 48) x 5 = 235 on what gas B
still sells: about 585, nearly 28 times as much.

**8.** *A tonne's damage starts at D0 a year and grows at g forever. Find its social cost at a discount rate r > g,
and explain why the answer is so sensitive when r is close to g.*

*Solution.* Summing D0 (1 + g)^(t-1)/(1 + r)^t over t = 1, 2, ... gives D0/(r - g) (in continuous time, the same
formula exactly): the Gordon formula of Part 23. With D0 = 1 and g = 2%, it is 100 at 3%, 200 at 2.5% and 33 at 5%.
Its proportional sensitivity to r is -1/(r - g), which grows without bound as r approaches g: when damages grow
almost as fast as the discount rate, distant years count almost as much as near ones, and a small change in the rate
moves the whole sum. That is chapter six's lesson in one line.

## Lab and interactive

- `python -m videos.economics.labs 48`: Hotelling's paths; the bet over every window; the fishery's three efforts and
  the fleet; the climate model fitted to the record; the DICE-style model's paths and its social cost of carbon by
  discount rate; fat tails; the club; Wright's law; the merit order and withholding.
- The interactive (course site): price a tonne. The reader chooses a discount rate, or rho and eta, and sees the
  model's damage stream discounted year by year, the social cost of carbon, and how much of it comes after 2100.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[48]`; the three dials (`discount`,
`energy_elasticity`, `warming_output`) are in `explainer/economics/dials.py`; Hubbert's forecast is a *Called it?*
entry (`explainer/economics/calls.py`); the tables are `PART48` in `explainer/economics/data/tables.py`. The data
were retrieved on 2026-11-21 and are registered with their licences in the Data Room. The studies' statements were
checked on 2026-11-21: DICE-2023 against the published article's text and Tables 1-2 (damages, control rates,
temperatures, carbon prices, the SCC at 1-5%); the wager against accounts of it (dates, $200 a metal, $576.07); Kiel,
Matheson and Golembiewski's 61.6% of 99 decades as quoted from their Table 1; Rennert et al. ($185, $44-413), EPA
($190) and the interim $51; the Stern Review's 0.1% and its SCC of over $300 a tonne of carbon; Weitzman (2009); Dietz
et al. (25%, 10%); Costello, Gaines and Lynham; British Columbia's tax (2008-2025) and the EU ETS (EUR 100 in February
2023) and CBAM (2023, 2026); Nordhaus (2015); Dell, Jones and Olken (1.3 points); Burke, Hsiang and Miguel (13
degrees, 166 countries); Barreca et al. (75%; 600 and 3,600 deaths); Chen et al. and Ebenstein et al. (5.5 and 3.1
years, 0.64 years per 10 ug/m3); Borenstein, Bushnell and Wolak ($2.04 and $8.98 billion; 21, 20 and 59%; 25% and 50%);
Hughes, Knittel and Sperling; Deryugina, MacKay and Reif; Hubbert and Deming; Bilal and Känzig (12%; their SCC in
several versions); McGlade and Ekins. Not verified, so not stated: DICE-2016R's discounting parameters (the film's
rho and eta are its own choice), the exact number of minerals in Slade's study, and the IEA's past solar forecasts.
