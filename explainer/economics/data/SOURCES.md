# The Data Room: sources

Every dataset *Economics, Built* shows, with its publisher, licence and vintage. The films read the frozen extracts
in this folder; `python -m explainer.economics.data --refresh NAME` downloads the source again into
`.cache/economics/raw/` and rewrites the extract (and says if the download differs from the recorded vintage). A
film that moves to a new vintage says so on screen.

## Frozen extracts

| File | Dataset | Publisher | Licence | Retrieved |
|---|---|---|---|---|
| `maddison2023_world.csv` | Maddison Project Database 2023, sheet "Regional data": world and eight regions, GDP per head, 1820-2022 | Groningen Growth and Development Centre (Bolt and van Zanden 2024) | CC BY 4.0 | 2026-11-18 |
| `maddison2023_countries.csv` | Maddison Project Database 2023, sheet "Full data": GDP per head and population; every year for the 37 countries in `MADDISON_FULL`, benchmark years (1820, 1850, 1870, ..., every second year from 1950, 2022) for the rest | as above | CC BY 4.0 | 2026-11-18 |
| `fred_GDPCA.csv` | real GDP, annual, chained 2017 dollars | BEA, via FRED | public domain | 2026-11-18 |
| `fred_GDPC1.csv` | real GDP, quarterly, SAAR | BEA, via FRED | public domain | 2026-11-18 |
| `fred_UNRATE.csv` | unemployment rate, monthly, SA, from 1948 | BLS, via FRED | public domain | 2026-11-18 |
| `fred_M0892AUSM156SNBR.csv` | unemployment rate, monthly, SA, 1929-1942 (National Industrial Conference Board estimates, published by G. H. Moore, *Business Cycle Indicators*) | NBER Macrohistory Database, series m08292a, via FRED | free, with the NBER's suggested citation | 2026-11-18 |
| `fred_INDPRO.csv` | industrial production, total index, monthly, SA | Federal Reserve Board, via FRED | public domain | 2026-11-18 |
| `fred_CPIAUCNS.csv` | consumer price index, all urban consumers, monthly, NSA | BLS, via FRED | public domain | 2026-11-18 |
| `spf_2006_2011.csv` | Survey of Professional Forecasters: median forecasts of real GDP (levels and growth) and of the probability of a decline, surveys of 2006-2011 | Federal Reserve Bank of Philadelphia | free with attribution | 2026-11-18 |
| `pinksheet_monthly.csv` | World Bank Commodity Price Data (The Pink Sheet), sheet "Monthly Prices", update of 3 November 2026: 23 monthly price series in nominal US dollars (oil, coal, US gas, cocoa, Arabica and Robusta coffee, tea, maize, rice, wheat, soybeans, sugar, beef, bananas, cotton, rubber, aluminium, copper, tin, nickel, zinc, gold, silver; columns in `PINK_COLUMNS`), 1960-01 to 2026-10 | World Bank, Prospects Group | CC BY 4.0 | 2026-11-18 |
| `psd_coffee.csv` | Production, Supply and Distribution Online, green coffee: production, domestic consumption, exports and ending stocks by marketing year, 1960-2026, for the world (the sum of every country in the file) and the producers in `PSD_COUNTRIES`, thousands of 60 kg bags | USDA Foreign Agricultural Service | public domain | 2026-11-18 |
| `fred_GDPA.csv`, `fred_GDIA.csv`, `fred_PCECA.csv`, `fred_GPDIA.csv`, `fred_GCEA.csv`, `fred_EXPGSA.csv`, `fred_IMPGSA.csv`, `fred_A033RC1A027NBEA.csv`, `fred_A191RD3A086NBEA.csv` | the national accounts, annual, 1929-2025: GDP, GDI, consumption, investment, government, exports, imports, compensation of employees (billions of current dollars), the GDP deflator (2017 = 100) | BEA, via FRED | public domain | 2026-11-19 |
| `fred_U1RATE.csv`, `fred_U2RATE.csv`, `fred_U4RATE.csv`, `fred_U5RATE.csv`, `fred_U6RATE.csv`, `fred_CIVPART.csv`, `fred_EMRATIO.csv` | the household survey's alternative measures of labour underutilization (U-1 and U-2 from 1948 and 1967, U-4 to U-6 from 1994), the participation rate and the employment-population ratio, monthly, SA, to October 2026 (October 2025 is missing: the survey was not taken during the shutdown) | BLS, via FRED | public domain | 2026-11-19 |
| `fred_CPIAUCSL.csv`, `fred_SUUR0000SA0.csv`, `fred_PCEPI.csv` | the CPI-U (SA), the chained CPI-U (from December 1999, NSA) and the PCE price index (SA), monthly | BLS and BEA, via FRED | public domain | 2026-11-19 |
| `fred_LABSHPUSA156NRUG.csv` | the share of labour compensation in GDP, United States, annual, 1950-2023 | Penn World Table (Groningen Growth and Development Centre), via FRED | CC BY 4.0 | 2026-11-19 |
| `fred_B230RC0A052NBEA.csv`, `fred_DMOTRG3A086NBEA.csv`, `fred_DMOTRC1A027NBEA.csv`, `fred_DFDHRG3A086NBEA.csv`, `fred_DFDHRC1A027NBEA.csv`, `fred_DREQRG3A086NBEA.csv`, `fred_DREQRC1A027NBEA.csv`, `fred_DODGRG3A086NBEA.csv`, `fred_DODGRC1A027NBEA.csv`, `fred_DFXARG3A086NBEA.csv`, `fred_DFXARC1A027NBEA.csv`, `fred_DCLORG3A086NBEA.csv`, `fred_DCLORC1A027NBEA.csv`, `fred_DGOERG3A086NBEA.csv`, `fred_DGOERC1A027NBEA.csv`, `fred_DONGRG3A086NBEA.csv`, `fred_DONGRC1A027NBEA.csv`, `fred_DHUTRG3A086NBEA.csv`, `fred_DHUTRC1A027NBEA.csv`, `fred_DHLCRG3A086NBEA.csv`, `fred_DHLCRC1A027NBEA.csv`, `fred_DTRSRG3A086NBEA.csv`, `fred_DTRSRC1A027NBEA.csv`, `fred_DRCARG3A086NBEA.csv`, `fred_DRCARC1A027NBEA.csv`, `fred_DFSARG3A086NBEA.csv`, `fred_DFSARC1A027NBEA.csv`, `fred_DIFSRG3A086NBEA.csv`, `fred_DIFSRC1A027NBEA.csv`, `fred_DOTSRG3A086NBEA.csv`, `fred_DOTSRC1A027NBEA.csv` | the population (thousands), and personal consumption expenditures by type of product (NIPA tables 2.4.4 and 2.4.5), annual, 1929-2025, for the fifteen categories that make up all of PCE: each one's chain-type price index (`RG3A086NBEA`, 2017 = 100) and spending (`RC1A027NBEA`, billions of dollars); `data.pce_by_type()` turns them into quantities per head | BEA, via FRED | public domain | 2026-11-19 |
| `fred_PCECCA.csv`, `fred_DPCERG3A086NBEA.csv`, `fred_TB3MS.csv` | real personal consumption expenditures (billions of chained 2017 dollars) and the PCE price index (2017 = 100), annual, 1929-2025; the 3-month Treasury bill rate (secondary market, discount basis, percent), monthly, January 1934 to October 2026 | BEA and the Federal Reserve Board, via FRED | public domain | 2026-11-19 |
| `wdi_2015_2025.csv` | World Development Indicators for the 217 economies (not aggregates), 2015-2025: GDP and GDP per head at market exchange rates (current US dollars) and at purchasing power parity (current international dollars), population, Gini index; with each economy's region and income group | World Bank (API, last updated 11 November 2026) | CC BY 4.0 | 2026-11-19 |
| `hdr2025_1990_2023.csv` | Human Development Report 2025, composite indices time series: the HDI, life expectancy, expected and mean years of schooling, GNI per head (2021 PPP dollars), 1990-2023, for the 195 countries (aggregates dropped) | UNDP Human Development Report Office | CC BY 3.0 IGO | 2026-11-19 |
| `draft1970.csv` | the draft lottery of 1 December 1969: the rank drawn for each of the 366 birthdays (day, month, rank) | U.S. Selective Service System, via the Journal of Statistics Education's data archive (Starr 1997, `draft70yr.dat`) | public record; JSE tabulation free for education | 2026-11-19 |
| `rtdsm_2006_2010.csv` | real GDP for 2006Q1-2010Q4 as reported by every quarterly vintage from 2007Q1 to 2026Q4 | Federal Reserve Bank of Philadelphia, Real-Time Data Set for Macroeconomists (ROUTPUT) | free with attribution | 2026-11-19 |
| `rtdsm_first_latest.csv` | for every quarter from 1965Q4: annualized real GDP growth in the first vintage that reported it and in the latest (2026Q4), computed from the same workbook | as above | free with attribution | 2026-11-19 |

The raw Maddison workbook (`mpd2023_web.xlsx`, dataverse file 421302) had SHA-256
`ecc5916ca12789b983fc4be437f8a354bbf4291323605324ac3e0aea4c57cbb6` when the extract was made. The raw Pink Sheet
(`CMO-Historical-Data-Monthly.xlsx`, update of 3 November 2026) had SHA-256
`3c8d9d8dbb48342fdbf24777c39a8ce8964cc2fd0958f72f6779e6e4ad99cde2`, and the PSD coffee archive
(`psd_coffee_csv.zip`) `967633a200af10d2a196816dd0169e732c61ed8dff4a83574bfa0b435c50ee66`. The Pink Sheet's
prices are nominal; a film that compares them across decades deflates them with `fred_CPIAUCNS.csv` and says so.
The UNDP's composite-indices file (`HDR25_Composite_indices_complete_time_series.csv`, Latin-1 encoded) had SHA-256
`61ed82e5b66c88dfca8ff9fac775c63981ecab6a254862af97acacc41c143117`, and the Philadelphia Fed's `routputqvqd.xlsx`
`6a7971b31b7336551705465de8a0855826f3652abe112406f52b2c2ed0994c0c`; the JSE's `draft70yr.dat.txt`
`973f258e63c94812b705c2007652fba34a02d579719dc74c569286106053f8d0`. The World Bank's API returns JSON pages that
are not kept; the extract records the API's "last updated" date instead.

The Maddison Project asks that the original country sources be cited when its data are shown in a graph. The
workbook's "Sources" sheet lists them; each part's README names those for the series it draws (Part 1: England and
the UK, Holland, the year 1, China, India, Japan, Korea, Nigeria and Ethiopia, the United States).

## Transcribed tables

`tables.py` holds numbers and passages transcribed from publications, each with its citation, where it is in the
publication, the copy that was read and the date the transcription was checked:

| Key | What | Checked |
|---|---|---|
| `bastiat_1845` | the Paris passage, *Economic Sophisms*, First Series, ch. 18 (Goddard translation) | 2026-11-18 |
| `british_academy_2009` | Besley and Hennessy's letter to the Queen, *British Academy Review* 14 | 2026-11-18 |
| `smith_1776` | the pin factory, *The Wealth of Nations*, Book I, ch. 1 | 2026-11-18 |
| `read_1958` | *I, Pencil*: the inputs and the line about knowing how | 2026-11-18 |
| `hayek_1945` | the tin passage and the dials | 2026-11-18 |
| `smith_1962` | the design of Smith's double auction | 2026-11-18 |
| `chamberlin_1948` | the design and finding of Chamberlin's market (from secondary summaries) | 2026-11-18 |
| `gneezy_rustichini_2000` | Table 1 (late pick-ups by centre and week), checked against Table 2 | 2026-11-18 |
| `simon_1991` | the visitor from Mars | 2026-11-18 |
| `ricardo_1817` | England and Portugal, cloth and wine | 2026-11-18 |
| `kuznets_1934` | *National Income, 1929-32* (Senate Document 124): tables 1-3, the exclusions and the passage on uses and abuses | 2026-11-19 |
| `petty_1665` | Petty's *Verbum Sapienti*: the people's expense, the stock's yield and the labour's | 2026-11-19 |
| `cpi_bias` | the CPI's bias by source: the Boskin Commission (1996), Lebow and Rudd (2003), Moulton (2018), Gordon's retrospective (2006) | 2026-11-19 |
| `deaton_heston_2010` | the 2005 ICP's revision of China and India | 2026-11-19 |
| `jones_klenow_2016` | consumption-equivalent welfare and income for 13 countries | 2026-11-19 |
| `nordhaus_tobin_1972` | the growth of the measure of economic welfare against NNP, 1929-65 | 2026-11-19 |
| `psz_2018` | distributional national accounts: the bottom half's and the top 1%'s shares (and Auten and Splinter's estimate of the top 1%'s rise) | 2026-11-19 |
| `moore_1914` | Moore's upward-sloping "law of demand" for pig iron, and Wright's 1915 reply | 2026-11-19 |
| `leamer_1983` | "Let's Take the Con out of Econometrics", p. 37 | 2026-11-19 |
| `lalonde_1986` | table 5: the NSW experiment against non-experimental estimates for men | 2026-11-19 |
| `card_2001` | table 2: OLS and IV estimates of the return to schooling | 2026-11-19 |
| `lucas_1976` | "Econometric Policy Evaluation: A Critique", p. 41, the syllogism (as quoted in the secondary literature) | 2026-11-19 |
| `samuelson_1938` | the programme: "dropping off the last vestiges of the utility analysis" | 2026-11-19 |
| `harbaugh_2001` | tables 1-2: GARP violations and Afriat's index for 7- and 11-year-olds and undergraduates, and for random choice | 2026-11-19 |
| `choi_2007` | the published consistency results (93 subjects, 50 budgets) and the random-choice benchmarks | 2026-11-19 |
| `ckms_2014` | 1,182 Dutch adults' consistency, its gaps by group, and its link to wealth | 2026-11-19 |
| `andreoni_miller_2002` | altruism according to GARP: 176 subjects, over 98% consistent | 2026-11-19 |
| `chen_2023` | GPT's and humans' CCEIs in four domains, and the literature's range | 2026-11-19 |
| `saez_2010` | the EITC's schedule (2008 dollars) and the elasticities implied by bunching at its first kink | 2026-11-19 |
| `mcfadden_bart` | the BART forecast: official 15%, McFadden's 6.3%, actual 6.2% | 2026-11-19 |
| `jensen_miller_2008` | the Hunan and Gansu voucher experiment: design, diets, calories per yuan, table 3's elasticities, figure 2's range; Marshall (1895) and Stigler (1987) as they quote them | 2026-11-19 |
| `hausman_1997` | Apple-Cinnamon Cheerios: the virtual price, consumer's surplus and the cereal CPI's bias | 2026-11-19 |
| `costa_2001` | CPI bias by period from Engel curves, 1888-1994, and Hamilton's (2001) estimates as she reports them | 2026-11-19 |
| `engel_1857` | Engel's law in Zimmerman's translation; Houthakker's confirmation and food elasticity; Seale and Regmi's elasticities by income group | 2026-11-19 |
| `ers_food_2024` | food spending and its share of income by income quintile, 2024 | 2026-11-19 |
| `jaravel_2019` | inflation inequality, 2004-2015; Jaravel and Lashkari's correction for income-dependent preferences | 2026-11-19 |
| `bls_cpi_methods` | the CPI's geometric means (1999) and the chained CPI (2002) | 2026-11-19 |
| `slutsky_1915` | Slutsky's article and its rediscovery | 2026-11-19 |
| `bernoulli_1738` | the St Petersburg game: Nicolaus Bernoulli's letter (1713), Cramer's square root (1728), Daniel Bernoulli's logarithm (1738) and his twenty ducats | 2026-11-19 |
| `samuelson_1937` | discounted utility and Samuelson's own two caveats (via Frederick, Loewenstein and O'Donoghue 2002) | 2026-11-19 |
| `allais_1953` | Allais's two pairs, the 1952 colloquium and Savage's answers; Kahneman and Tversky's problem 1 (82%) | 2026-11-19 |
| `ellsberg_1961` | the urn (30 red, 60 black or yellow), the four $100 bets and the frequent pattern | 2026-11-19 |
| `rabin_2000` | the calibration theorem's examples and tables I and II | 2026-11-19 |
| `thaler_1981` | $15 now against one month, one year and ten years: medians and implied annual rates | 2026-11-19 |
| `holt_laury_2005` | the paired-lottery menu and average safe choices by stakes, real and hypothetical, 2002 and 2004 | 2026-11-19 |
| `hayden_platt_2009` | bids for the St Petersburg game, real (20) and hypothetical (220), and for truncated games | 2026-11-19 |
| `madrian_shea_2001` | automatic enrolment: participation 86% against 37%, and 76% at the 3% default | 2026-11-19 |
| `thaler_benartzi_2004` | Save More Tomorrow: saving rates 3.5% to 13.6% in 40 months | 2026-11-19 |
| `barsky_1997` | the HRS income gambles; mean risk tolerance and EIS | 2026-11-19 |
| `post_2008` | Deal or No Deal: the break-even effect | 2026-11-19 |
| `mehra_prescott_1985` | the equity premium, about 6 points a year, 1889-1978 | 2026-11-19 |
| `cobb_douglas_1928` | Cobb and Douglas's data, American manufacturing 1899-1922 (output, labour, capital, 1899 = 100), and Felipe and Adams's re-estimates | 2026-11-19 |
