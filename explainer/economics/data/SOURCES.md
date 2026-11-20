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
| `fred_PCECC96.csv`, `fred_DSPIC96.csv`, `fred_PSAVERT.csv`, `fred_PCE.csv`, `fred_PCEND.csv`, `fred_PCES.csv`, `fred_DNDGRG3M086SBEA.csv`, `fred_DSERRG3M086SBEA.csv` | consumption against income (Part 22): real PCE (quarterly, chained 2017 dollars, from 1947), real disposable personal income, the personal saving rate, PCE in total, on nondurable goods and on services (monthly, SAAR, from 1959) and the price indexes of nondurables and services (monthly, 2017 = 100) | BEA, via FRED | public domain | 2026-11-20 |
| `fred_CSUSHPINSA.csv`, `fred_CUSR0000SEHA.csv` | housing as an asset (Part 23): the S&P CoreLogic Case-Shiller U.S. National Home Price Index (monthly, NSA, from 1987) and the CPI's rent of primary residence (monthly, SA, from 1981) | S&P Dow Jones Indices LLC and BLS, via FRED | the index © S&P Dow Jones Indices LLC, distributed by FRED and shown with citation; the CPI public domain | 2026-11-20 |
| `fred_UNEMPLOY.csv`, `fred_UEMPLT5.csv`, `fred_UEMP27OV.csv`, `fred_CLF16OV.csv`, `fred_JTSJOL.csv`, `fred_JTSHIL.csv`, `fred_JTSTSL.csv`, `fred_JTSQUL.csv`, `fred_NROU.csv`, `fred_OPHNFB.csv` | the labour market's stocks and flows (Part 24): unemployment in total, under 5 weeks and 27 weeks and over, the labour force (monthly, SA, from 1948), job openings, hires, separations and quits (JOLTS, monthly, SA, from December 2000), CBO's noncyclical rate of unemployment (quarterly, with projections), and output per hour in the nonfarm business sector (quarterly) | BLS and CBO, via FRED | public domain | 2026-11-20 |
| `fred_M2SL.csv`, `fred_M1SL.csv`, `fred_BOGMBASE.csv`, `fred_CURRCIR.csv`, `fred_TOTRESNS.csv`, `fred_M2V.csv`, `fred_GDP.csv` | money (Part 25): M2 and M1 (monthly, SA, from 1959; M1 includes savings deposits from May 2020), the monetary base, currency in circulation and banks' total reserves (monthly, NSA, billions), M2's velocity and nominal GDP (quarterly, SA) | Board of Governors of the Federal Reserve System, Federal Reserve Bank of St. Louis and BEA, via FRED | public domain | 2026-11-20 |
| `fred_X14AICBS.csv`, `fred_M09036USM155NNBR.csv`, `fred_FEDFUNDS.csv`, `fred_SNDR.csv`, `fred_NDR12MCD.csv`, `fred_GS10.csv`, `fred_GS2.csv`, `fred_DPSSCBW027SBOG.csv`, `fred_DPSLCBW027SBOG.csv`, `fred_EQTA.csv`, `fred_MMMFFAQ027S.csv` | banks and runs (Part 26): bank suspensions (annual 1921-1941, all incorporated commercial banks; monthly 1921-1933, all banks), the federal funds rate, the FDIC's national deposit rates on savings and 12-month CDs (monthly, from April 2021), 10- and 2-year Treasury yields (monthly averages), deposits at small and large domestically chartered banks (weekly, SA), banks' equity capital to assets (quarterly, 1988-2020), and money market funds' total financial assets (quarterly) | Federal Reserve Board, NBER Macrohistory Database, FDIC and FFIEC, via FRED | public domain | 2026-11-20 |
| `fred_GNPCA.csv`, `fred_USREC.csv`, `fred_M1476BUSM027NNBR.csv`, `fred_GDPPOT.csv`, `fred_IRSTCI01JPM156N.csv` | the Keynesian revolution (Part 27): real GNP (annual, from 1929, chained 2017 dollars), the NBER's recession months (monthly, from December 1854), America's monetary gold stock (monthly, 1914-1946, billions of dollars), the CBO's real potential GDP (quarterly; values after the latest quarter are projections and are not used), and Japan's overnight call rate (monthly, from 1985) | BEA, NBER via the Federal Reserve Bank of St. Louis, NBER Macrohistory Database, Congressional Budget Office and OECD Main Economic Indicators, via FRED | public domain (OECD data: OECD terms) | 2026-11-20 |
| `fred_MICH.csv`, `fred_T5YIEM.csv`, `fred_CPILFESL.csv` | inflation and expectations (Part 28): the University of Michigan's median expected price change over the next twelve months (monthly, from 1978), the 5-year breakeven inflation rate (monthly average, from 2003), and the CPI less food and energy (monthly, SA, from 1957) | University of Michigan Surveys of Consumers, the Federal Reserve Bank of St. Louis and BLS, via FRED | the Surveys of Consumers' data are the University of Michigan's, reproduced as a cited extract; the others public domain | 2026-11-20 |
| `fred_GPDIC1.csv`, `fred_HOANBS.csv`, `fred_A011RA3Q086SBEA.csv`, `fred_A008RA3Q086SBEA.csv` | the business cycle (Part 29): real gross private domestic investment (quarterly, SAAR, chained 2017 dollars), residential and nonresidential fixed investment (chain-type quantity indexes, 2017 = 100) and hours worked in the nonfarm business sector (quarterly, index 2017 = 100), from 1947 | BEA and BLS, via FRED | public domain | 2026-11-20 |
| `fred_LABSHPUSA156NRUG.csv` | the share of labour compensation in GDP, United States, annual, 1950-2023 | Penn World Table (Groningen Growth and Development Centre), via FRED | CC BY 4.0 | 2026-11-19 |
| `fred_B230RC0A052NBEA.csv`, `fred_DMOTRG3A086NBEA.csv`, `fred_DMOTRC1A027NBEA.csv`, `fred_DFDHRG3A086NBEA.csv`, `fred_DFDHRC1A027NBEA.csv`, `fred_DREQRG3A086NBEA.csv`, `fred_DREQRC1A027NBEA.csv`, `fred_DODGRG3A086NBEA.csv`, `fred_DODGRC1A027NBEA.csv`, `fred_DFXARG3A086NBEA.csv`, `fred_DFXARC1A027NBEA.csv`, `fred_DCLORG3A086NBEA.csv`, `fred_DCLORC1A027NBEA.csv`, `fred_DGOERG3A086NBEA.csv`, `fred_DGOERC1A027NBEA.csv`, `fred_DONGRG3A086NBEA.csv`, `fred_DONGRC1A027NBEA.csv`, `fred_DHUTRG3A086NBEA.csv`, `fred_DHUTRC1A027NBEA.csv`, `fred_DHLCRG3A086NBEA.csv`, `fred_DHLCRC1A027NBEA.csv`, `fred_DTRSRG3A086NBEA.csv`, `fred_DTRSRC1A027NBEA.csv`, `fred_DRCARG3A086NBEA.csv`, `fred_DRCARC1A027NBEA.csv`, `fred_DFSARG3A086NBEA.csv`, `fred_DFSARC1A027NBEA.csv`, `fred_DIFSRG3A086NBEA.csv`, `fred_DIFSRC1A027NBEA.csv`, `fred_DOTSRG3A086NBEA.csv`, `fred_DOTSRC1A027NBEA.csv` | the population (thousands), and personal consumption expenditures by type of product (NIPA tables 2.4.4 and 2.4.5), annual, 1929-2025, for the fifteen categories that make up all of PCE: each one's chain-type price index (`RG3A086NBEA`, 2017 = 100) and spending (`RC1A027NBEA`, billions of dollars); `data.pce_by_type()` turns them into quantities per head | BEA, via FRED | public domain | 2026-11-19 |
| `fred_PCECCA.csv`, `fred_DPCERG3A086NBEA.csv`, `fred_TB3MS.csv` | real personal consumption expenditures (billions of chained 2017 dollars) and the PCE price index (2017 = 100), annual, 1929-2025; the 3-month Treasury bill rate (secondary market, discount basis, percent), monthly, January 1934 to October 2026 | BEA and the Federal Reserve Board, via FRED | public domain | 2026-11-19 |
| `fred_MCOILBRENTEU.csv`, `fred_MCOILWTICO.csv` | crude oil prices, Brent (Europe) and West Texas Intermediate (Cushing, Oklahoma), dollars a barrel, monthly, May 1987 and January 1986 to October 2026 | U.S. Energy Information Administration, via FRED | public domain | 2026-11-19 |
| `fred_APU0000717311.csv` | the average retail price of ground coffee (100%, ground roast, all sizes), U.S. city average, dollars a pound, monthly, January 1980 to October 2026 | U.S. Bureau of Labor Statistics, via FRED | public domain | 2026-11-19 |
| `fred_APU000074714.csv` | the average retail price of regular unleaded gasoline, U.S. city average, dollars a gallon, monthly, January 1976 to October 2026 | U.S. Bureau of Labor Statistics, via FRED | public domain | 2026-11-19 |
| `fred_CUSR0000SETA02.csv`, `fred_CUSR0000SETA01.csv` | the consumer price indexes for used cars and trucks and for new vehicles, U.S. city average (1982-84 = 100, seasonally adjusted), monthly, January 1953 to October 2026 | U.S. Bureau of Labor Statistics, via FRED | public domain | 2026-11-19 |
| `wdi_2015_2025.csv` | World Development Indicators for the 217 economies (not aggregates), 2015-2025: GDP and GDP per head at market exchange rates (current US dollars) and at purchasing power parity (current international dollars), population, Gini index; with each economy's region and income group | World Bank (API, last updated 11 November 2026) | CC BY 4.0 | 2026-11-19 |
| `wdi_money_1960_2024.csv` | World Development Indicators for the economies (not aggregates), 1960-2024 (Part 25): broad money growth, consumer-price inflation, GDP-deflator inflation and real GDP growth (annual %), and broad money as a share of GDP; with each economy's region and income group | World Bank (API, last updated 11 November 2026) | CC BY 4.0 | 2026-11-20 |
| `hdr2025_1990_2023.csv` | Human Development Report 2025, composite indices time series: the HDI, life expectancy, expected and mean years of schooling, GNI per head (2021 PPP dollars), 1990-2023, for the 195 countries (aggregates dropped) | UNDP Human Development Report Office | CC BY 3.0 IGO | 2026-11-19 |
| `warheads_1945_2026.csv` | estimated nuclear warhead stockpiles by country (military stockpiles; retired warheads queued for dismantlement excluded), 1945-2026 | Federation of American Scientists, "Estimated Global Nuclear Warhead Inventories", via Our World in Data (nuclear-warhead-stockpiles, updated 2026-05-13) | CC BY 4.0 (Our World in Data); FAS estimates cited | 2026-11-19 |
| `so2_1900_2022.csv` | sulphur dioxide emissions from all sectors, tonnes a year, 1900-2022, for the world, five regions and six countries (United States, United Kingdom, China, India, Germany, Japan) | Community Emissions Data System v_2024_07_08 (Hoesly et al. 2024), via Our World in Data (grapher so-emissions-by-world-region-in-million-tonnes) | CC BY 4.0 | 2026-11-19 |
| `marriage_rate.csv` | crude marriage rate (marriages a year per 1,000 people): the United States 1886-2022 (with gaps), and the United Kingdom, Japan, Italy, Sweden, South Korea, Germany, France, the Netherlands and Denmark from 1960 (France from 1994) | OECD Family Database, US Census Bureau (1949) and CDC (2020), via Our World in Data (grapher marriage-rate-per-1000-inhabitants) | CC BY 4.0 (Our World in Data); sources' terms | 2026-11-19 |
| `democracy_vdem.csv` | V-Dem's electoral democracy index (0-1, central estimate), 1789-2025, for the world (Our World in Data's aggregate) and the United States, the United Kingdom, France, India, Germany, Japan, Brazil, South Africa (from 1900) and China | V-Dem Institute, Democracy Report v16 (2026), via Our World in Data (grapher electoral-democracy-index) | CC BY 4.0 (Our World in Data); V-Dem's terms | 2026-11-19 |
| `boe_millennium_england.csv` | A millennium of macroeconomic data for the UK (version 3.1), England: population (thousands, 1086-2016), real consumption wages from daily wage rates (1900 = 100, from 1209), the same adjusted for days worked a year before 1750 (after Humphries and Weisdorf), and real GDP per head (2013 pounds, from 1270; Broadberry, Campbell, Klein, Overton and van Leeuwen before 1700) | Bank of England (Thomas and Dimsdale 2017) | Bank of England; free to reuse with attribution | 2026-11-19 |
| `longrun_owid.csv` | long-run population (from 10,000 BCE; HYDE, Gapminder, UN WPP), life expectancy at birth (from 1543; Riley, Zijdeman and Ribeira da Silva, HMD, UN WPP), children per woman (from 1891 for Sweden, 1950 otherwise; HFD, UN WPP) and men's average height by decade of birth (from 1660; Baten and Blum, NCD-RisC), for the world and ten countries | Our World in Data (compilation) | CC BY 4.0; sources' terms | 2026-11-19 |
| `pwt110.csv` | Penn World Table 11.0, sheet Data: real GDP (output side, national accounts, expenditure side), population, employment, hours, human capital, capital stocks (current PPPs and constant national prices), labour share, investment share, depreciation, TFP level, internal rate of return on capital, for 185 countries, 1950-2023, in 2021 US dollars | Groningen Growth and Development Centre (Feenstra, Inklaar and Timmer) | CC BY 4.0 | 2026-11-19 |
| `ajr_hdm.csv` | Acemoglu, Johnson and Robinson's (2001) base sample of 64 former colonies: log GDP per head (1995), protection against expropriation (1985-95), settler mortality and its log, latitude, neo-Europe and continent dummies (no country names in this copy) | the R package hdm 0.3.2 (CRAN), data/AJR.rda, read by `explainer/psychology/rdata.py` without evaluating anything | MIT (hdm); the data are AJR's | 2026-11-20 |
| `shiller_annual.csv` | Robert Shiller's annual US series, 1871-2016 (Part 23): the S&P composite price, dividends and earnings, the one-year and long interest rates, the CPI, the real one-year return, real consumption per head (from 1889, NIPA and Kendrick), and the real return on the S&P composite | R. J. Shiller, *Market Volatility* (1989), ch. 26, updated; www.econ.yale.edu/~shiller/data/chapt26.xlsx | free for research and teaching, with citation | 2026-11-20 |
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
| `radford_1945` | Radford's account of the camp economy: the parcel, the padre, the cigarette standard, the salmon in a transit camp, the halving of August 1944, the Bully Mark, the liberation | 2026-11-19 |
| `edgeworth_1881` | Edgeworth's three demonstrations on contract and competition (p. 20) and his naming of the contract-curve (p. 21) | 2026-11-19 |
| `hsieh_klenow_2009` | Hsieh and Klenow's dispersion of revenue productivity and the TFP gains from equalizing it, China, India and the United States (tables 2, 4 and 6) | 2026-11-19 |
| `bils_klenow_ruane_2021` | Bils, Klenow and Ruane's correction of those gains for measurement error (India 20%, the United States 60%) | 2026-11-19 |
| `kehoe_2014` | Kehoe's table of Mexican imports from North America by industry, 1989-2009, against the Sobarzo model's 1992 forecasts and the least-traded-products prediction | 2026-11-19 |
| `dleu_2020` | De Loecker, Eeckhout and Unger's aggregate markup, 1980 and 2016, and the profit rate | 2026-11-19 |
| `traina_2018` | Traina's finding that public-firm markups rose only modestly, and the aggregate flat or falling | 2026-11-19 |
| `nakamura_zerom_2010` | Nakamura and Zerom's decomposition of incomplete pass-through in coffee (local costs, markups, menu costs) | 2026-11-19 |
| `dube_misra_2023` | Dube and Misra's personalized-pricing experiment: profits against uniform pricing, and who gains | 2026-11-19 |
| `nagel_1995` | Nagel's guessing-game sessions: design, and the first-period means and medians for p = 1/2, 2/3 and 4/3 | 2026-11-19 |
| `thaler_ft_1997` | the Financial Times guessing contest of 1997: its mean and winning number (secondary accounts) | 2026-11-19 |
| `flood_1952` | the Flood-Dresher experiment of January 1950: a hundred rounds, the joint outcomes, and Nash's comment (via Poundstone) | 2026-11-19 |
| `henrich_2001` | ultimatum offers in fifteen small-scale societies: the range of mean offers | 2026-11-19 |
| `chc_2004` | Camerer, Ho and Chong's cognitive hierarchy: the typical number of thinking steps | 2026-11-19 |
| `axelrod_1980` | Axelrod's two computer tournaments: entries, rounds and the winner | 2026-11-19 |
| `lysine_connor_1998` | the lysine cartel: US prices stated in Connor's text, ADM's cost, the meetings, the mole, the raid, the fines and the overcharge range | 2026-11-19 |
| `connor_2014` | Connor's long-run median and mean cartel overcharges (2014) | 2026-11-19 |
| `boyer_kotchoni_2015` | Boyer and Kotchoni's bias-corrected mean and median overcharges | 2026-11-19 |
| `merger_guidelines` | the HHI thresholds of the 2023 Merger Guidelines and the 2010 Horizontal Merger Guidelines | 2026-11-19 |
| `akerlof_1970` | Akerlof's lemons paper: its pages, the three rejections and the Nobel | 2026-11-19 |
| `efc_2010` | Einav, Finkelstein and Cullen's demand and cost estimates for Alcoa, and the welfare cost of selection | 2026-11-19 |
| `cutler_zeckhauser_1998` | Harvard's PPO, 1992-97: the employee's charge, enrollment, the reform and the spiral; Cutler and Reber's welfare loss | 2026-11-19 |
| `tyler_2000` | the GED's signalling value for young dropouts | 2026-11-19 |
| `info_tests` | tests for private information: Chiappori and Salanié, Finkelstein and McGarry, Cabral and Hortaçsu | 2026-11-19 |
| `hkk_2015` | Hackmann, Kolstad and Kowalski's mandate gain; Handel's inertia | 2026-11-19 |
| `lazear_2000` | Safelite's switch to piece rates: the productivity gain, its split, and the wage rise | 2026-11-19 |
| `piece_rates` | piece rates in a field experiment (Shearer) and against relative incentives (Bandiera, Barankay and Rasul) | 2026-11-19 |
| `incentive_cases` | Ford's five-dollar day, China's rural reform and teacher cheating in Chicago | 2026-11-19 |
| `tenancy` | Tenancy reform in West Bengal (Operation Barga) and sharecropped against owned plots in India | 2026-11-19 |
| `crowding` | Frey and Oberholzer-Gee's Swiss survey: accepting a nuclear-waste repository with and without compensation | 2026-11-19 |
| `coase_1960` | Coase's steers and crops: the arithmetical example and the bargain | 2026-11-19 |
| `cheung_1973` | Cheung's beekeepers: the rent per hive in money and in nectar, by season | 2026-11-19 |
| `acid_rain` | the SO2 allowance market: emissions, costs and benefits, and allowance prices (Schmalensee and Stavins) | 2026-11-19 |
| `roads` | the fundamental law of road congestion (Duranton and Turner) and the Stockholm trial | 2026-11-19 |
| `currie_walker_2011` | E-ZPass and infant health | 2026-11-19 |
| `uk_3g_2000` | Britain's 3G auction: licences, bidders, rounds and revenue (Binmore and Klemperer) | 2026-11-19 |
| `euro_3g_2000` | the European 3G auctions of 2000: revenue per head, and the Dutch and Swiss sales (Klemperer) | 2026-11-19 |
| `bazerman_samuelson_1983` | the jar of coins: estimates, winning bids and the winner's loss | 2026-11-19 |
| `collusion_signals` | signalling in spectrum auctions: trailing digits in the FCC's DEF-block auction, Mannesmann's bids in Germany | 2026-11-19 |
| `reserve_prices` | Ostrovsky and Schwarz's field experiment on reserve prices in sponsored search | 2026-11-19 |
| `treasury_format` | the Treasury's move from multiple-price to single-price auctions, and its evidence | 2026-11-19 |
| `incentive_auction` | the FCC's broadcast incentive auction: forward and reverse totals, spectrum cleared | 2026-11-19 |
| `roth_2012` | the market for American doctors, Roth's table of clearinghouses, New York's high-school match and kidney chains (Roth's Nobel lecture) | 2026-11-19 |
| `school_effects` | exam-school offers in Boston (regression discontinuity) and Denver's charter schools (the deferred-acceptance lottery) | 2026-11-19 |
| `vsl` | the value of a statistical life: DOT's and EPA's values, Ashenfelter and Greenstone's speed limits, Kniesner et al.'s panel estimates | 2026-11-19 |
| `duverger` | Duverger's law and Riker's history of it | 2026-11-19 |
| `malthus_1798` | Malthus's two powers and two ratios, *Essay on the Principle of Population* (1798), ch. 1, pp. 13-14 of the first edition | 2026-11-19 |
| `nordhaus_light` | the labour price of light, hours of work per 1,000 lumen-hours, from the open fire to the compact fluorescent bulb, and the traditional indexes' overstatement, Nordhaus (1996), table 1.6 and section 1.5 | 2026-11-20 |
| `bloom_2020` | research effort (×23 since the 1930s) and research productivity (÷41, -5.1% a year) in the US aggregate; Moore's law (18 times the researchers); the aggregate decline of 5.3% a year, Bloom, Jones, Van Reenen and Webb (2020), NBER WP 23782 | 2026-11-20 |
| `mpc_studies` | what households did with windfalls (Part 22): the 2001 rebates (Johnson, Parker and Souleles, AER 2006), the 2008 payments (Parker, Souleles, Johnson and McClelland, AER 2013), the 2020 payments (Parker, Schild, Erhard and Johnson, NBER WP 29648), Alaska's dividend (Hsieh, AER 2003; Kueng, QJE 2018), Norwegian lottery prizes (Fagereng, Holm and Natvik, AEJ: Macro 2021), the Italian survey (Jappelli and Pistaferri, AEJ: Macro 2014), hypothetical gains and losses (Fuster, Kaplan and Zafar, REStud 2021), the hand-to-mouth (Kaplan, Violante and Weidner, BPEA 2014), spending through unemployment (Ganong and Noel, AER 2019; NBER WP 25417): each from the abstract or the NBER summary | 2026-11-20 |
| `hanke_krus_2012` | the hyperinflation peaks (Part 25): the highest monthly inflation in Germany (October 1923), Yugoslavia (January 1994), Zimbabwe (November 2008) and Hungary (July 1946), from Hanke and Krus's table (Cato WP 8, 2012), Hungary's doubling time from Hanke's commentary; Cagan's German average (322% a month, August 1922 to November 1923) and revenue-maximizing rate (about 20% a month), from secondary summaries of his 1956 table | 2026-11-20 |
| `svb_2023` | Silicon Valley Bank (Part 26): withdrawals of $42 billion on 9 March 2023 and $100 billion requested for 10 March (Barr's testimony, 28 March 2023); about 94% of deposits uninsured and a CET1 ratio of 12% at year-end 2022 (the Federal Reserve's review, April 2023); the held-to-maturity portfolio of $91 billion with a fair value $15 billion below cost (year-end 2022 accounts, as reported) | 2026-11-20 |
| `stress_2022` | the Federal Reserve's 2022 severely adverse scenario (February 2022): the 10-year Treasury yield falling to 3/4 percent in 2022Q1, flat in Q2 and Q3, rising to 1 1/2 percent by the end; short rates near zero throughout; unemployment rising to 10% (the intermediate quarters of the path are interpolated for the chart) | 2026-11-20 |
