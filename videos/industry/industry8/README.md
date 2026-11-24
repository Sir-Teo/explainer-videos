# Industry, Built: Part 8, Oil and Gas

Part 8 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act II, *Out of the Ground*. It asks: what does a barrel cost, and who
decides what it sells for? It answers with the US Energy Information Administration's production, price, trade and
gasoline data since 1859; the Commodity Futures Trading Commission's account of 20 April 2020; EIA's reports on the 2026
war and the Strait of Hormuz; Saudi Aramco's Annual Report 2025; the Dallas Fed Energy Survey; ExxonMobil's, Chevron's,
the shale producers', the refiners', the service companies' and Cheniere's filings; the Handbook of Texas on
Spindletop; Hubbert's 1956 paper; and the Works' model wells and fields. The answer: a barrel costs a few dollars to
lift from the best fields and sixty-odd to drill anew in Texas; over time the last barrel the world needs sets the
price, and the owner of the rock, usually a state, keeps most of the difference. In the short run neither buyers nor
sellers can change much, so small shortages move the price a long way, which invites cartels and punishes them, and
leaves room for the short-cycle barrels of shale.

It opens on two prices of the same liquid: minus $37.63 for WTI on 20 April 2020, when Cushing's tanks were 76% full,
and Brent's $124 average in October 2026, after the Strait of Hormuz closed. From there it covers:

- Run it: a conventional field, a deepwater platform and a shale pad (the Works' models), across 400 price paths;
- under the ground: source rock, reservoir and trap, and the four ways oil is produced (conventional, shale, deep
  water, oil sands);
- a well, and how it fades: Spindletop (10 January 1901; 100,000 barrels a day, 10,000 by 1904), Arps's curves (a 9%
  and a 60% first-year decline), and the shale treadmill (44 new wells a month to hold a million barrels a day; stop
  and output falls 21% in a year);
- reserves are an economic number: ExxonMobil's 22.4bn barrels (2019), 15.2bn (2020; 3.1bn at Kearl no longer
  counted), 18.5bn (2021) and 19.3bn (2025), with nothing pumped or lost;
- what a barrel costs: Aramco's $3.51 lifting cost and $8.0 of capital spending per barrel; the Dallas Fed's $43 to
  keep a US well running and $66 to drill a new one ($67 in the Permian); the world's cost curve;
- who owns the oil: the largest producers in 2025 and OPEC's 35%; Aramco's 247bn barrels against ExxonMobil's 19.3bn;
  about $204bn from Aramco to the Saudi state in 2025 in royalties, taxes and dividends;
- where a gallon's dollar goes: August 2026's $4.06 (crude 204 cents, refining 99, distribution 51, taxes 52) and the
  shares since 2000 (taxes from 32% to 13%);
- one price, many barrels: WTI, Brent and Dubai; the 2026 spread ($25 on 31 March); futures, contango and storage,
  and how the May 2020 contract went below zero;
- why the price swings so hard: a 5% loss with responses of 0.05 nearly doubles the price; 2026's shut-ins (10.9m
  b/d at the peak) against a 41% rise in Brent and 1.9% less oil used (about -0.05);
- an intermission: eighty years of a barrel in today's dollars;
- OPEC: its share (58% in 1973, 28% in 1985, 35% in 2025), Saudi Arabia's swing from 9.9m to 3.4m b/d (1980-1985)
  and the flood of 1986; 2014, OPEC+ and the 9.7m b/d cut of 2020; 2026;
- shale: US output by region since 2000, past its 1970 peak in 2018 and near 14m b/d in 2026; oil rigs -80% and
  output -11% in 2014-2016; the US a net exporter since 2020;
- refining: the column, the 3-2-1 crack spread since 1987 ($8 in 2020, $35 in 2022, $39 in 2026 so far) and Valero's
  profits; pipelines as regulated tolls;
- gas: Henry Hub against Europe and Asia ($70 against $8.8 in August 2022), the LNG chain, US exports to 15.1bn
  cubic feet a day in 2025, and Cheniere;
- the drillers' drillers: SLB and Halliburton (revenue -43% and -52%, 2014-2016) against rigs and ExxonMobil's
  spending;
- the landscape, November 2026: national companies, majors, independents, refiners, services, LNG and traders, and
  where the market stood after the war;
- *Called it?*: Hubbert's 1956 forecasts against EIA's data (the US peak in 1970, then shale; the world's still
  rising in 2025); and this series' call that Brent will average below $90 in 2027 (60%).

## Build it

```bash
python -m videos.industry.industry8.compute               # every number, printed (instant)
EXPLAINER_TTS=silent python tools/build.py industry8 -q l  # the whole part, silent preview
python tools/build.py industry8                           # 1080p30 with narration
python -m videos.industry.labs 8                          # the lab
python -m pytest tests/industry                           # the Register and the Works (tests/industry/test_oil.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p08.py`) or comes from the Filing Room: EIA's
petroleum, international, gasoline-component and gas extracts (`eia_petroleum.csv`, `eia_intl.csv`, `eia_pump.csv`,
`eia_gas.csv`), FRED's energy prices and the CPI (`fred_energy.csv`), and companies' filings (`sec_annual.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Minus thirty-seven dollars | 20 April 2020 at Cushing; the Strait of Hormuz in 2026; the title |
| 1 | Run it: drill, wait or buy back | Three projects and a fourth choice; 400 price paths |
| 2 | Under the ground | Source, reservoir, trap; four ways oil is produced |
| 3 | A well, and how it fades | Spindletop; Arps's curves; the shale treadmill |
| 4 | Reserves are an economic number | Three nested totals; ExxonMobil, 2019-2025 |
| 5 | What a barrel costs | Aramco against the Dallas Fed; the world's cost curve |
| 6 | Who owns the oil | Producers and OPEC; Aramco and ExxonMobil; the Saudi state's take |
| 7 | Where a gallon's dollar goes | EIA's components, August 2026 and since 2000 |
| 8 | One price, many barrels | Benchmarks; futures, contango, storage; the negative price |
| 9 | Why the price swings so hard | Steep curves; 2026's arithmetic |
| — | Intermission | Eighty years of a barrel; the story so far |
| 10 | OPEC: a cartel's arithmetic | Its share; Saudi Arabia's swing; 2014, 2016, 2020, 2026 |
| 11 | Shale: oil from a factory | Output by region; rigs against output; net exports |
| 12 | Refining: a business of spreads | The column; the crack spread; Valero; pipelines |
| 13 | Gas, and the ships that made it global | Three prices; the LNG chain; US exports and Cheniere |
| 14 | The drillers' drillers | SLB, Halliburton, rigs and ExxonMobil's spending |
| 15 | The landscape, November 2026 | The map of companies; the market after the war |
| 16 | Called it? | Hubbert, 1956; this series' call on Brent in 2027 |
| — | The barrel, and what comes next | The answers; Part 9, mining and metals |

## What is computed, and from what

`compute.py` reads EIA's bulk files for US production (annual since 1859, monthly since 1920 with Texas, North Dakota
and the federal Gulf), oil rigs, prices and trade, and for crude production by country since 1973; WTI since 1946 is
deflated by the CPI to October 2026 dollars. Hubbert's two US curves are redrawn as logistic curves with his ultimate
totals (150bn and 200bn barrels) and peak years (1965 and 1970), passing through the cumulative output to 1955 (EIA:
52.6bn barrels, against his 52.5bn). The 3-2-1 crack spread uses New York Harbor gasoline and heating oil against Brent.
Aramco's payments to the state add royalties and other taxes, income taxes and zakat, and the Government's 81.48% of
dividends (SAR 320.4bn at 3.75 riyals to the dollar). The 2026 elasticity divides EIA's change in world consumption
(-2.0m of 104.4m b/d) by the change in Brent's yearly average ($69 to $97). The prospects, price paths, treadmill and
clearing multiples are the Works' `oil.py`, labelled as models on screen.

## Problems and solutions

**1.** *A shale well starts at 800 barrels a day and follows Arps's curve with D = 1.5 a year and b = 1. What is its
rate after one year and after three?*

*Solution.* q(t) = 800 / (1 + 1.5 t). After one year: 800 / 2.5 = 320 barrels a day, a 60% fall. After three years:
800 / 5.5 = 145. Most of the well's oil comes in its first two years, which is why a shale basin must keep drilling.

**2.** *A field costs $500m to develop and will produce 20 million barrels in a single year, two years from now. Lifting
costs $15 a barrel, and the state takes 20% of revenue as royalty. At a 10% discount rate, what price breaks even?*

*Solution.* The development pays if 0.8 p × 20m − 15 × 20m, discounted by 1.1² = 1.21, equals $500m. So 16m p − 300m =
605m, and p = 905 / 16 = $56.6 a barrel. Without the two-year wait it would be (500 + 300) / 16 = $50: waiting adds about an eighth to the price needed.

**3.** *World supply falls by 4%. Buyers and sellers each respond 0.08% for every 1% change in price. By how much must
the price rise?*

*Solution.* The multiple is (1 − 0.04)^(1 / (−0.08 − 0.08)) = 0.96^(−6.25) = e^(6.25 × 0.0408) = e^0.255 = 1.29: a rise
of about 29%. With responses of 0.04 each, the same shortage raises the price by about two-thirds.

**4.** *Gasoline sells for $3.00 a gallon and heating oil for $3.20 when crude costs $70 a barrel. What is the 3-2-1 crack
spread?*

*Solution.* Two barrels of gasoline: 2 × 42 × 3.00 = $252. One of heating oil: 42 × 3.20 = $134.40. Three of crude:
$210. The spread is (252 + 134.40 − 210) / 3 = $58.80 a barrel of crude, very wide by the standard of the chart.

**5.** *Hubbert expected US output to peak around 1970 if 200bn barrels would ever be produced. By 2025 the United States had
produced about 258bn. What did his method leave out?*

*Solution.* His ultimate was the oil recoverable with the techniques and prices he could foresee. Horizontal drilling
and hydraulic fracturing made the source rock itself a reservoir, and high prices paid for it. The peak date was
right for conventional oil; the ultimate, and so the tail, was not. A resource's size depends on price and
technology as well as geology.

## Glossary

- **Barrel:** 42 US gallons (about 159 litres).
- **Source rock, reservoir, trap:** where oil forms, the porous rock it moves into, and the seal that holds it.
- **Shale (tight) oil:** oil produced from the source rock itself by horizontal wells and hydraulic fracturing.
- **Decline curve:** how a well's output falls over time (Arps, 1945).
- **Proved reserves:** oil that can be produced economically at the past year's average price, by the SEC's rules.
- **Lifting cost:** the cost of producing a barrel from an existing well, excluding royalty, exploration and
  depreciation.
- **Benchmark:** a crude whose price others are quoted against (WTI, Brent, Dubai).
- **Contango:** a futures curve in which later delivery costs more, paying for storage.
- **Crack spread:** the value of products less the cost of the crude they are made from.
- **LNG:** natural gas cooled to a liquid, about 600 times smaller, so it can be shipped.

## Lab and interactive

- `python -m videos.industry.labs 8`: the negative price and the 2026 shock; Aramco against the Dallas Fed; the
  Works' break-evens, price paths and treadmill; ExxonMobil's reserves; a gallon's dollar; clearing multiples and
  2026's elasticity; OPEC's share and Saudi Arabia's swing; crack spreads; gas and LNG; the services' falls;
  Hubbert's curves against the record.
- The interactive (course site): an oil shock. Set the share of supply lost and how strongly buyers and sellers
  respond, and see the price that clears the market against 2026's peak shut-in.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p08.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- US Energy Information Administration: petroleum and international bulk files; Gasoline Pump Components History;
  natural gas exports and production; Today in Energy (27 April 2020; September 2020; 11 March 2024; 1 April 2024; June
  2025; 7 April 2026); Short-Term Energy Outlook, 10 November 2026; Energy Explained, 'Liquefied natural gas'.
- US Commodity Futures Trading Commission, Interim Staff Report on trading in NYMEX WTI around 20 April 2020 (2020).
- Saudi Aramco, Annual Report 2025.
- Federal Reserve Bank of Dallas, Dallas Fed Energy Survey, first quarter 2026.
- Exxon Mobil Corporation, Forms 10-K for 2019, 2020, 2021 and 2025; Chevron, ConocoPhillips, EOG, Occidental, Devon,
  Valero, Marathon Petroleum, SLB, Halliburton and Cheniere, Forms 10-K (SEC company facts).
- FRED: WTI since 1946; Henry Hub; the IMF's European gas and Asian LNG prices; the consumer price index.
- Handbook of Texas Online, 'Spindletop Oilfield'.
- US Department of State, Office of the Historian, 'Oil Embargo, 1973-1974'; OPEC, 'Brief History'.
- J. J. Arps, 'Analysis of Decline Curves', *Transactions of the AIME* 160 (1945).
- M. King Hubbert, 'Nuclear Energy and the Fossil Fuels', American Petroleum Institute, San Antonio, March 1956.
