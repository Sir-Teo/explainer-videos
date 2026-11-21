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
| `pinksheet_monthly.csv` | World Bank Commodity Price Data (The Pink Sheet), sheet "Monthly Prices", update of 3 November 2026: 25 monthly price series in nominal US dollars (oil, coal, US gas, cocoa, Arabica and Robusta coffee, tea, maize, rice, wheat, soybeans, sugar at world, US and EU prices, beef, bananas, cotton, rubber, aluminium, copper, tin, nickel, zinc, gold, silver; columns in `PINK_COLUMNS`; the US and EU sugar columns added 2026-11-20 from the same workbook), 1960-01 to 2026-10 | World Bank, Prospects Group | CC BY 4.0 | 2026-11-18 |
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
| `fred_GDPDEF.csv`, `fred_PCEPILFE.csv`, `fred_CORESTICKM159SFRBATL.csv`, `fred_COREFLEXCPIM159SFRBATL.csv` | sticky prices (Part 30): the GDP deflator (quarterly) and the core PCE price index (monthly), and the Atlanta Fed's sticky-price and flexible-price CPIs less food and energy (Bryan and Meyer's split by how often items' prices change; 12-month percent changes, monthly) | BEA and the Federal Reserve Bank of Atlanta, via FRED | public domain | 2026-11-20 |
| `fred_WALCL.csv`, `fred_WRESBAL.csv`, `fred_IOER.csv`, `fred_IORB.csv`, `fred_DGS10.csv`, `fred_DFII10.csv`, `fred_GS1.csv`, `fred_PPIACO.csv`, `fred_IRLTLT01ITM156N.csv`, `fred_IRLTLT01ESM156N.csv`, `fred_IRLTLT01DEM156N.csv`, `fred_IRLTLT01GBM156N.csv`, `fred_ECBDFR.csv`, `fred_RESPPLLOPNWW.csv`, `fred_DFEDTAR.csv`, `fred_DFEDTARU.csv`, `fred_FEDTARMDLR.csv` | the central bank (Part 31): the Federal Reserve's total assets and reserve balances (weekly), the interest rates on excess reserves and on reserve balances (daily), the 10-year nominal and inflation-indexed Treasury yields (daily), the 1-year Treasury yield (monthly), the PPI for all commodities (monthly), and 10-year government bond yields for Italy, Spain, Germany and the United Kingdom (monthly, OECD), the ECB's deposit facility rate (daily), the Federal Reserve's earnings remittances due to the Treasury (weekly; negative values are the deferred asset), the federal funds target rate and the upper limit of its range (daily), and the FOMC's median longer-run projection of the funds rate (from 2012) | Federal Reserve Board, BLS, OECD and ECB, via FRED | public domain (OECD data under the OECD's terms) | 2026-11-20 |
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
| `democracy_vdem.csv` | V-Dem's electoral democracy index (0-1, central estimate), 1789-2025, for the world (Our World in Data's aggregate) and the United States, the United Kingdom, France, India, Germany, Japan, Brazil, South Africa (from 1900) and China; South Korea, Chile, Spain, Indonesia, Poland, Ghana, Taiwan, Russia, Hungary, Turkey and Venezuela added 2026-11-20 from the same file | V-Dem Institute, Democracy Report v16 (2026), via Our World in Data (grapher electoral-democracy-index) | CC BY 4.0 (Our World in Data); V-Dem's terms | 2026-11-19 |
| `boe_millennium_england.csv` | A millennium of macroeconomic data for the UK (version 3.1), England: population (thousands, 1086-2016), real consumption wages from daily wage rates (1900 = 100, from 1209), the same adjusted for days worked a year before 1750 (after Humphries and Weisdorf), and real GDP per head (2013 pounds, from 1270; Broadberry, Campbell, Klein, Overton and van Leeuwen before 1700) | Bank of England (Thomas and Dimsdale 2017) | Bank of England; free to reuse with attribution | 2026-11-19 |
| `longrun_owid.csv` | long-run population (from 10,000 BCE; HYDE, Gapminder, UN WPP), life expectancy at birth (from 1543; Riley, Zijdeman and Ribeira da Silva, HMD, UN WPP), children per woman (from 1891 for Sweden, 1950 otherwise; HFD, UN WPP) and men's average height by decade of birth (from 1660; Baten and Blum, NCD-RisC), for the world and ten countries | Our World in Data (compilation) | CC BY 4.0; sources' terms | 2026-11-19 |
| `pwt110.csv` | Penn World Table 11.0, sheet Data: real GDP (output side, national accounts, expenditure side), population, employment, hours, human capital, capital stocks (current PPPs and constant national prices), labour share, investment share, depreciation, TFP level, internal rate of return on capital, for 185 countries, 1950-2023, in 2021 US dollars | Groningen Growth and Development Centre (Feenstra, Inklaar and Timmer) | CC BY 4.0 | 2026-11-19 |
| `ajr_hdm.csv` | Acemoglu, Johnson and Robinson's (2001) base sample of 64 former colonies: log GDP per head (1995), protection against expropriation (1985-95), settler mortality and its log, latitude, neo-Europe and continent dummies (no country names in this copy) | the R package hdm 0.3.2 (CRAN), data/AJR.rda, read by `explainer/psychology/rdata.py` without evaluating anything | MIT (hdm); the data are AJR's | 2026-11-20 |
| `shiller_annual.csv` | Robert Shiller's annual US series, 1871-2016 (Part 23): the S&P composite price, dividends and earnings, the one-year and long interest rates, the CPI, the real one-year return, real consumption per head (from 1889, NIPA and Kendrick), and the real return on the S&P composite | R. J. Shiller, *Market Volatility* (1989), ch. 26, updated; www.econ.yale.edu/~shiller/data/chapt26.xlsx | free for research and teaching, with citation | 2026-11-20 |
| `draft1970.csv` | the draft lottery of 1 December 1969: the rank drawn for each of the 366 birthdays (day, month, rank) | U.S. Selective Service System, via the Journal of Statistics Education's data archive (Starr 1997, `draft70yr.dat`) | public record; JSE tabulation free for education | 2026-11-19 |
| `rtdsm_2006_2010.csv` | real GDP for 2006Q1-2010Q4 as reported by every quarterly vintage from 2007Q1 to 2026Q4 | Federal Reserve Bank of Philadelphia, Real-Time Data Set for Macroeconomists (ROUTPUT) | free with attribution | 2026-11-19 |
| `rtdsm_first_latest.csv` | for every quarter from 1965Q4: annualized real GDP growth in the first vintage that reported it and in the latest (2026Q4), computed from the same workbook | as above | free with attribution | 2026-11-19 |
| `rtdsm_q1_vintages.csv` | real GDP (real GNP before 1992) for every quarter from 1947Q1, as reported by each first-quarter vintage from 1966Q1 to 2026Q1, each in its own base year's dollars (Part 31's real-time output gaps) | Federal Reserve Bank of Philadelphia, Real-Time Data Set for Macroeconomists (ROUTPUT) | free with attribution | 2026-11-20 |
| `greenbook_pgdp.csv` | the Federal Reserve staff's Greenbook (Tealbook) projections of GDP-price inflation (GNP before December 1991), annualized quarter on quarter, for the quarter before, the current quarter and four ahead, every Greenbook from March 1967 to December 2020 | Federal Reserve Bank of Philadelphia, Philadelphia Fed's Tealbook (formerly Greenbook) Data Set, GBweb_Row_Format.xlsx | free with attribution | 2026-11-20 |
| `spf_pgdp_growth.csv` | Survey of Professional Forecasters: median forecasts of GDP-price inflation (DPGDP2-6), every survey from 1968Q4 | Federal Reserve Bank of Philadelphia, Survey of Professional Forecasters, median_pgdp_growth.xlsx | free with attribution | 2026-11-20 |
| `hlw_rstar.csv` | Holston, Laubach and Williams's one-sided estimates of the natural rate of interest for the United States, Canada and the euro area, with US trend growth and other determinants, quarterly 1961Q1-2026Q2 | Federal Reserve Bank of New York, Holston_Laubach_Williams_current_estimates.xlsx | public research data, with attribution | 2026-11-20 |
| `fred_FYFSGDA188S.csv`, `fred_GFDEGDQ188S.csv`, `fred_FYGFGDQ188S.csv`, `fred_A091RC1Q027SBEA.csv`, `fred_IRLTLT01GRM156N.csv` | the treasury (Part 32): the federal surplus or deficit as a share of GDP (fiscal years, from 1929), total public debt and debt held by the public as shares of GDP (quarterly), federal interest payments (quarterly), and Greece's 10-year bond yield (monthly, OECD) | OMB, BEA, the Federal Reserve Bank of St. Louis and OECD, via FRED | public domain (OECD data under the OECD's terms) | 2026-11-20 |
| `ramey_zubairy.csv` | Ramey and Zubairy's quarterly US data, 1875-2015 (used from 1889): nominal government purchases and GDP, the GDP deflator, population, unemployment, military spending news, real GDP and potential output, the T-bill rate, a zero-bound dummy, federal receipts and public debt | Ramey and Zubairy, JPE 126(2) (2018), replication files (rzdatnew.csv) | posted by the authors for replication | 2026-11-20 |
| `ramey_tax.csv` | Ramey's Handbook tax data, 1945-2015, quarterly: GDP, prices, population, purchases, tax receipts, and Romer and Romer's exogenous and endogenous tax changes as ratios to GDP | Ramey, Handbook of Macroeconomics 2A (2016), replication files (homtaxdat.xlsx); Romer and Romer, AER 100(3) (2010) | posted by the author for replication | 2026-11-20 |
| `blanchard_leigh.csv` | the IMF's spring 2010 forecasts of real GDP growth and of the structural balance, and growth as reported in fall 2012, by country, 2009-2011 | Blanchard and Leigh, NBER WP 18779 (2013), replication files (dta.xlsx) | posted by the authors for replication | 2026-11-20 |
| `rr_hap.csv` | Reinhart and Rogoff's public debt to GDP and real GDP growth for 20 advanced economies, 1946-2009, as processed by Herndon, Ash and Pollin | Herndon, Ash and Pollin, CJE 38(2) (2014), replication files (RR-keycolumns.xlsx) | BSD 2-clause (the authors' files) | 2026-11-20 |
| `jst.csv` | the Jorda-Schularick-Taylor Macrohistory Database, release 6: 18 advanced economies, 1870-2020, annual: population, real GDP per head, nominal GDP, prices, bank loans (total, mortgage, household, business), house prices, interest rates, public debt, the current account, bank leverage and funding, the systemic crisis chronology (`crisisJST`), asset returns, and imports and exports (31 of the database's columns) | Jorda, Schularick and Taylor, NBER Macroeconomics Annual 2016 (2017); macrohistory.net (JSTdatasetR6.xlsx) | CC BY-NC-SA 4.0 (the extract is shared under the same licence) | 2026-11-20 |
| `fred_DRSFRMACBS.csv`, `fred_TEDRATE.csv`, `fred_SWPT.csv`, `fred_BAA10Y.csv`, `fred_HDTGPDUSQ163N.csv`, `fred_EXTHUS.csv`, `fred_EXKOUS.csv`, `fred_EXMXUS.csv` | crises (Part 33): the delinquency rate on single-family mortgages (quarterly), the TED spread (daily, to January 2022), the Federal Reserve's central bank liquidity swaps (weekly), the Baa corporate spread over Treasuries (daily), US household debt to GDP (quarterly, IMF), and the baht, won and peso per dollar (monthly, H.10) | the Federal Reserve Board, the Federal Reserve Bank of St. Louis, Moody's and the IMF, via FRED | public domain (Moody's and IMF data under their terms, as FRED redistributes them) | 2026-11-20 |
| `fred_EXUSUK.csv`, `fred_EXGEUS.csv`, `fred_EXJPUS.csv`, `fred_EXSZUS.csv`, `fred_EXCAUS.csv`, `fred_EXUSEU.csv`, `fred_EXUSAL.csv`, `fred_EXUSNZ.csv`, `fred_DEXCHUS.csv`, `fred_IR3TIB01USM156N.csv`, `fred_IR3TIB01GBM156N.csv`, `fred_IR3TIB01JPM156N.csv`, `fred_IR3TIB01CHM156N.csv`, `fred_IR3TIB01CAM156N.csv`, `fred_IR3TIB01DEM156N.csv`, `fred_IR3TIB01AUM156N.csv`, `fred_IR3TIB01NZM156N.csv`, `fred_IR.csv`, `fred_TWEXBMTH.csv`, `fred_DTWEXBGS.csv`, `fred_IIPUSNETIQ.csv`, `fred_IEABC.csv`, `fred_TRESEGGBM052N.csv`, `fred_VIXCLS.csv`, `fred_DEXUSUK.csv`, `fred_DEXJPUS.csv`, `fred_DEXCAUS.csv`, `fred_DEXSZUS.csv`, `fred_IREXFUELS.csv` | the open economy (Part 34): monthly exchange rates of the pound, mark, yen, Swiss franc, Canadian, Australian and New Zealand dollars and the euro against the dollar, and daily rates for the pound, yen, Canadian dollar, Swiss franc and yuan (H.10); three-month interbank rates for eight economies (OECD); US import prices, all and excluding fuel (BLS); the broad dollar indexes, goods (to 2019) and goods and services; the US current account and net international investment position (BEA, quarterly); the UK's reserves excluding gold (IMF); the VIX (daily) | the Federal Reserve Board, the OECD, the BLS, the BEA, the IMF and Cboe, via FRED | public domain (OECD, IMF and Cboe data under their terms, as FRED redistributes them) | 2026-11-20 |
| `fred_B235RC1A027NBEA.csv`, `fred_A255RC1A027NBEA.csv`, `fred_A640RC1A027NBEA.csv`, `fred_A650RC1A027NBEA.csv`, `fred_B641RC1A027NBEA.csv`, `fred_B651RC1A027NBEA.csv`, `fred_A642RC1A027NBEA.csv`, `fred_A652RC1A027NBEA.csv` | trade (Part 35): federal customs duties and current payments for imports of goods, annual since 1929, and exports and imports of capital goods, automotive vehicles and parts, and consumer goods, annual since 1967 (NIPA tables 3.2, 4.1 and 4.2.5) | the U.S. Bureau of Economic Analysis, via FRED | public domain | 2026-11-20 |
| `cepii_gravity_2019.csv` | CEPII's Gravity database, 2019: every ordered pair of existing countries with BACI trade recorded, with population-weighted distance, a shared border, a common official language, a colonial tie, GDPs (thousands of current dollars), WTO-notified trade agreements, EU membership, and total and manufacturing trade flows (BACI, thousands of current dollars) | M. Conte, P. Cotterlaz and T. Mayer, CEPII WP 2022-05; Gravity_csv_V202211.zip | Etalab Open Licence 2.0 | 2026-11-20 |
| `fred_IMPCH.csv`, `fred_EXPCH.csv`, `fred_MANEMP.csv` | the China shock (Part 36): US imports of goods from China and exports to China (monthly, Census), and manufacturing employment (monthly, BLS) | the U.S. Census Bureau and Bureau of Labor Statistics, via FRED | public domain | 2026-11-20 |
| `trefler_hov.csv` | Trefler's data for "The Case of the Missing Trade and Other Mysteries": the factor content of net exports, endowments, GDP, the trade balance, GDP per head and population for 33 countries and 9 factors (capital, six kinds of labour, cropland, pasture), 1983 | D. Trefler, AER 85(5) (1995); hov_pub.dat (15 November 1994) at nber.org/ftp/trefler/HOV | no licence stated; the author's replication data, redistributed as a cited extract | 2026-11-20 |
| `bigmac.csv` | The Economist's Big Mac index, every survey since April 2000: local price, exchange rate, dollar price, raw valuation against the dollar, GDP per head and the GDP-adjusted valuation, by country | The Economist, big-mac-data (GitHub: TheEconomist/big-mac-data), output-data/big-mac-full-index.csv | CC BY 4.0 | 2026-11-20 |
| `wdi_ca.csv` | the current account balance as a percent of GDP (BN.CAB.XOKA.GD.ZS), 1980-2025, for the United States, China, Germany, Japan, the United Kingdom, Saudi Arabia, Korea and Thailand | World Bank, World Development Indicators (API) | CC BY 4.0 | 2026-11-20 |
| `fred_ATXRSA.csv`, `fred_BOXRSA.csv`, `fred_CRXRSA.csv`, `fred_CHXRSA.csv`, `fred_CEXRSA.csv`, `fred_DAXRSA.csv`, `fred_DNXRSA.csv`, `fred_DEXRSA.csv`, `fred_LVXRSA.csv`, `fred_LXXRSA.csv`, `fred_MIXRSA.csv`, `fred_MNXRSA.csv`, `fred_NYXRSA.csv`, `fred_PHXRSA.csv`, `fred_POXRSA.csv`, `fred_SDXRSA.csv`, `fred_SFXRSA.csv`, `fred_SEXRSA.csv`, `fred_TPXRSA.csv`, `fred_WDXRSA.csv` | house prices in the twenty Case-Shiller metropolitan areas (Part 37): monthly, seasonally adjusted, January 2000 = 100, from 1987 (Atlanta and Detroit from 1991, Minneapolis and Phoenix 1989, Seattle 1990, Dallas 2000) | S&P Dow Jones Indices LLC, via FRED | the indices © S&P Dow Jones Indices LLC, distributed by FRED and shown with citation | 2026-11-20 |
| `fred_WFHCOVIDMATQUESTION.csv` | working from home (Part 37): the percent of full paid working days worked from home, monthly from May 2020, with a 2019 value from the American Time Use Survey (Survey of Working Arrangements and Attitudes) | J. M. Barrero, N. Bloom and S. J. Davis, via FRED | CC BY 4.0 (cite Barrero, Bloom and Davis, NBER WP 28731) | 2026-11-20 |
| `cbsa_2020_2024.csv` | the resident population of every metropolitan and micropolitan statistical area: the April 2020 estimates base and the July 2024 estimate (Vintage 2024) | U.S. Census Bureau, Population Estimates Program (cbsa-est2024-alldata.csv) | public domain | 2026-11-20 |
| `urban_share_1500_2025.csv` | the share of the population living in urban areas, 1500-2025 (centuries to 1700, then decades, then years), for the world, five regions and 21 countries | HYDE 3.5 (PBL Netherlands Environmental Assessment Agency), via Our World in Data (urbanization-last-500-years, updated 2026-06-08) | CC BY 4.0 | 2026-11-20 |
| `njmin_1992.csv` | Card and Krueger's 410 fast-food restaurants in New Jersey and eastern Pennsylvania (Burger King, KFC, Roy Rogers, Wendy's): employees full-time, part-time and managers, the starting wage, hours open and the price of an entrée, in February-March and November-December 1992, and each store's status at the second interview | D. Card and A. B. Krueger (1994), public.dat in njmin.zip posted by David Card | posted for public use; cite Card and Krueger (1994) | 2026-11-20 |
| `card1995.csv`, `wage1_1976.csv`, `wage2_1980.csv`, `wagepan_1980_87.csv`, `cps78_85.csv` | Wooldridge's labour datasets: Card's (1995) National Longitudinal Survey of Young Men, 1976 (3,010 men: log wage, schooling, experience, college nearby, region, IQ), the Current Population Survey of 1976 (526 workers), the National Longitudinal Survey of 1980 (935 men, with IQ), Vella and Verbeek's panel of 545 young men, 1980-87 (log wage, union membership, experience, marriage, race), and the Current Population Survey of 1978 and 1985 (1,084 workers: log wage, sex, union, schooling, experience) | J. M. Wooldridge, via the R package wooldridge 1.4-7 (CRAN) | GPL-3 (the package); the data are the cited surveys | 2026-11-20 |
| `fred_FEDMINNFRWG.csv` | the federal minimum hourly wage for nonfarm workers, monthly from October 1938 | U.S. Department of Labor, via FRED | public domain | 2026-11-20 |
| `fred_LEU0252918500A.csv`, `fred_LEU0252917300A.csv`, `fred_LEU0252916700A.csv`, `fred_LEU0252881500A.csv`, `fred_LEU0252881600A.csv`, `fred_LEU0252881900A.csv`, `fred_LEU0252882800A.csv`, `fred_LEU0252911200A.csv`, `fred_LEU0252911500A.csv` | median usual weekly earnings of full-time wage and salary workers: 25 and over with a bachelor's degree or more, high-school graduates with no college, and without a diploma; all 16 and over (nominal and in 1982-84 dollars); men and women (1982-84 dollars); the first and ninth deciles (from 2000); annual from 1979 | U.S. Bureau of Labor Statistics, Current Population Survey, via FRED | public domain | 2026-11-20 |
| `fred_LNU02027662.csv`, `fred_LNU02027660.csv`, `fred_LNS12300060.csv`, `fred_PRS85006173.csv` | employment of people 25 and over with a bachelor's degree or more and of high-school graduates with no college (monthly, from 1992; October 2025 not collected); the employment-population ratio at ages 25-54; the labour share of the nonfarm business sector (quarterly, from 1947) | U.S. Bureau of Labor Statistics, via FRED | public domain | 2026-11-20 |
| `polarization_1980_2005.csv`, `occ1990dd_1950_2005.csv` | Autor and Dorn's replication data: for each percentile of the 1980 occupational wage distribution, its percent of employment in 1980, 1990, 2000 and 2005, the change in mean log hourly wages over each period and its 1980 routine share; for each of 330 occ1990dd occupations, its percent of all employment in 1950-2005, mean log hourly wages in 1980 and 2005 and its 1980 routine task intensity (read from the archive's Stata files by the Data Room's own reader, `stata.py`) | D. Autor and D. Dorn (2013), Autor-Dorn-LowSkillServices-FileArchive.zip from David Dorn's data page | posted for research use; cite Autor and Dorn (2013) | 2026-11-20 |
| `resume_2001.csv` | Bertrand and Mullainathan's 4,870 fictitious resumes sent to 1,323 help-wanted advertisements in Boston and Chicago, 2001-02: the advertisement, city, job and industry, the first name and the race and sex it signals, the resume's contents and quality, and whether the employer called back | M. Bertrand and S. Mullainathan (2004), via the R package openintro 2.5.1 (CRAN) | GPL-3 (the package); the data are the cited experiment's | 2026-11-20 |
| `sportscards_1998.csv` | List's sports-card experiment: 148 traders at a trading-card show in Orlando, Florida, 1998, each given one of two collectibles of about equal value and offered a swap; dealer status, trades a month, years trading, demographics, and whether they swapped | J. A. List (2003), via the R package AER 1.2-17 (CRAN), from the online complements to Stock and Watson (2007) | GPL-2 or GPL-3 (the package); the data are the cited experiment's | 2026-11-21 |
| `saez_top_shares_1913_2022.csv` | Piketty and Saez's top income shares for the United States from tax returns, 1913-2022: the shares of the top 10%, 5%, 1%, 0.5%, 0.1% and 0.01% of tax units, excluding and including capital gains (the top 10% and 5% from 1917), the number of tax units and average income in 2022 dollars (Tables A0, A1 and A3 of TabFig2022.xlsx) | T. Piketty and E. Saez (2003), updated by E. Saez | posted by the author for public use with citation | 2026-11-20 |
| `chetty_by_parent_pctile.csv`, `chetty_absmob_1940_1984.csv`, `chetty_cz_2014.csv` | children born in 1980-82 by their parents' income percentile: parents' mean income, the children's mean rank and income at 31-32, college attendance, and the share in each quintile of their own generation (summed from the 100 x 100 transition matrix, onlinedata1.dta); the share of children earning more than their parents at 30, by birth cohort 1940-1984 and parent percentile; absolute and relative mobility, the chance of rising from the bottom to the top fifth, and 18 characteristics of 741 commuting zones (Online Data Tables V and VIII) | Opportunity Insights: Chetty, Hendren, Kline and Saez (2014); Chetty, Grusky, Hell, Hendren, Manduca and Narang (2017) | posted by Opportunity Insights for public use with citation | 2026-11-20 |
| `wid_top1_selected.csv` | the share of pre-tax national income received by the richest 1%, in years without extrapolation, for the United States, the United Kingdom, France, Germany, Sweden, the Netherlands, Japan, China, India, Russia, Brazil, South Africa and the world | World Inequality Database (WID.world, 2026), via Our World in Data | CC BY 4.0 | 2026-11-20 |
| `fred_WFRBST01134.csv`, `fred_WFRBSN09161.csv`, `fred_WFRBSN40188.csv`, `fred_WFRBSB50215.csv` | shares of household net worth held by the top 1%, the 90th to 99th percentiles, the 50th to 90th and the bottom half of the wealth distribution, quarterly from 1989 (the Distributional Financial Accounts) | Board of Governors of the Federal Reserve System, via FRED | public domain | 2026-11-20 |
| `fred_GINIALLRH.csv` | the Gini index of household money income, annual from 1967 | U.S. Census Bureau, Current Population Survey, via FRED | public domain | 2026-11-20 |
| `fred_IITTRHB.csv`, `fred_IITTIHB.csv` | the top statutory rate of the US individual income tax and the taxable income above which it applies (married couples filing jointly), annual 1913-2018 | Internal Revenue Service, Statistics of Income, Historical Table 23, via FRED | public domain | 2026-11-20 |
| `fred_FYFRGDA188S.csv`, `fred_FYFSGDA188S.csv` | federal receipts and the federal surplus or deficit as percentages of GDP, fiscal years from 1929 | U.S. Office of Management and Budget, via FRED | public domain | 2026-11-20 |
| `fred_CCSA.csv`, `fred_ICSA.csv`, `fred_IURSA.csv` | continued and initial claims for state unemployment insurance and the insured unemployment rate, weekly, seasonally adjusted, from 1967 (the rate from 1971) | U.S. Department of Labor, Employment and Training Administration, via FRED | public domain | 2026-11-20 |
| `fred_W825RC1.csv` | unemployment insurance benefits paid to persons, billions of dollars at a seasonally adjusted annual rate, monthly from 1959 | U.S. Bureau of Economic Analysis, via FRED | public domain | 2026-11-20 |
| `fred_UEMPMED.csv` | median duration of unemployment in weeks, monthly from 1967 | U.S. Bureau of Labor Statistics, via FRED | public domain | 2026-11-20 |
| `fred_CPATAX.csv`, `fred_CP.csv` | corporate profits after tax, with and without the inventory valuation and capital consumption adjustments, billions of dollars at a seasonally adjusted annual rate, quarterly from 1947 | U.S. Bureau of Economic Analysis, via FRED | public domain | 2026-11-20 |
| `rust_buses.csv` | Rust's Madison bus panel: 162 buses in eight groups, monthly odometer readings and engine replacements, December 1974 to May 1985 (one row per bus and month) | Rust (1987), via OpenSourceEconomics' zurcher-data mirror of his files | MIT (mirror); the data are Rust's | 2026-11-20 |
| `blp_cars.csv` | Berry, Levinsohn and Pakes's automobile data: 2,217 model-years, 1971-1990 (price in thousands of 1983 dollars, horsepower over weight, air conditioning, miles per gallon, size, share, firm) | Berry, Levinsohn and Pakes (1995), via the R package BLPestimatoR 0.3.4 (CRAN) | GPL-3 (package); the data are BLP's | 2026-11-20 |
| `wdi_poverty_1981_2025.csv` | the share of people living below $3.00 a day (2021 PPP), by survey year, for the world, sub-Saharan Africa, South Asia, East Asia and Pacific, Latin America and the Caribbean, the Middle East and North Africa, Europe and Central Asia, China and India (indicator SI.POV.DDAY) | World Bank, World Development Indicators (Poverty and Inequality Platform) | CC BY 4.0 | 2026-11-21 |
| `wdi_agriculture_2015_2025.csv` | for each country, the latest year from 2015 with all three: agriculture's share of employment (SL.AGR.EMPL.ZS) and of value added (NV.AGR.TOTL.ZS), and GDP per head at PPP in constant 2021 dollars (NY.GDP.PCAP.PP.KD) | World Bank, World Development Indicators | CC BY 4.0 | 2026-11-21 |
| `thornton_hiv_2004.csv` | Thornton's experiment in rural Malawi, 2004: 4,820 people in 125 villages (2,894 with a recorded collection), tested for HIV and randomly offered cash incentives of up to about $3 to learn their results at centres placed at random; the village, distance to the centre, incentive, whether they collected their result, age and HIV status | Thornton (2008), via the R package causaldata 0.1.4 (CRAN) | MIT (package); the data are Thornton's | 2026-11-21 |
| `insure_china.csv` | Cai, de Janvry and Sadoulet's weather-insurance experiment in rural China: the package's extract of 1,410 rice-farming households in 166 villages, randomly assigned a simple or an intensive information session and a default; take-up, the session, the default, age, rice area, perceived disaster probability, risk aversion, literacy and the take-up of the household's friends in the earlier round | Cai, de Janvry and Sadoulet (2015), via the R package causaldata 0.1.4 (CRAN) | MIT (package); the data are the authors' | 2026-11-21 |
| `panes_uruguay.csv` | Manacorda, Miguel and Vigorito's households near the eligibility cutoff of Uruguay's PANES transfer programme (2005-07): the standardized eligibility score, education, age, participation, and support for the government | Manacorda, Miguel and Vigorito (2011), via the R package causaldata 0.1.4 (CRAN) | MIT (package); the data are the authors' | 2026-11-21 |
| `rdsenate_1914_2010.csv` | Cattaneo, Frandsen and Titiunik's 1,390 U.S. Senate elections, 1914-2010: state, year, Senate class, the Democratic margin at election t, the Democratic share of the vote at t and at the same seat's next election, open seats and midterms | Cattaneo, Frandsen and Titiunik (2015), via the R package rdrobust 4.1.2 (CRAN) | GPL-3 (package); the data are the authors' compilation of election returns | 2026-11-20 |
| `co2_mlo_annual.csv` | Mauna Loa's annual mean atmospheric CO2, 1959-2025, in parts per million, with its uncertainty | NOAA Global Monitoring Laboratory (Scripps before 1974), co2_annmean_mlo.csv | U.S. government work, freely available with credit to NOAA GML | 2026-11-21 |
| `hadcrut5_global_annual.csv` | HadCRUT5's global mean surface temperature anomaly, 1850-2025, relative to 1961-1990, with 95% limits (analysis version 5.0.2.0) | Met Office Hadley Centre and CRU (Morice et al. 2021) | Open Government Licence v3 | 2026-11-21 |
| `gcp_co2_world.csv` | the world's CO2 emissions in billions of tonnes a year: fossil fuels and industry, 1750-2025, and land-use change, 1850-2025 | Global Carbon Budget 2026, via Our World in Data (annual-co2-emissions-per-country, co2-land-use) | CC BY 4.0 | 2026-11-21 |
| `era5_country_annual.csv` | annual mean surface air temperature for 193 countries, 1940-2025 (complete years), the mean of ERA5's monthly latitude-weighted country averages | Copernicus Climate Change Service (ERA5), via Our World in Data (average-monthly-surface-temperature); annual means computed here | CC BY 4.0; Copernicus licence (contains modified Copernicus Climate Change Service information) | 2026-11-21 |
| `wdi_gdppc_kd.csv` | GDP per head in constant 2015 US dollars (NY.GDP.PCAP.KD), 1960-2025, for 213 countries | World Bank, World Development Indicators | CC BY 4.0 | 2026-11-21 |
| `solar_pv.csv` | solar photovoltaic module prices in constant 2025 dollars per watt, 1975-2025, and the world's installed solar capacity in gigawatts, 2000-2025 | IRENA and other sources, via Our World in Data (solar-pv-prices, installed-solar-pv-capacity) | CC BY 4.0 | 2026-11-21 |
| `fao_fish_stocks.csv` | the shares of the world's assessed fish stocks within biologically sustainable levels and overexploited, 1974-2021 | FAO, The State of World Fisheries and Aquaculture (2025), via Our World in Data | CC BY 4.0; FAO's terms | 2026-11-21 |
| `oil_production.csv` | oil production (crude, shale, oil sands, condensates and natural gas liquids) in terawatt-hours a year, 1900-2025, for the world and the United States | Energy Institute, Statistical Review of World Energy (2026), Etemad and Luciani (1991) and the U.S. EIA, via Our World in Data (oil-production-by-country) | CC BY 4.0 | 2026-11-21 |
| `wdi_state_2015_2025.csv` | for each country, the latest year from 2015 of tax revenue as a percent of GDP (GC.TAX.TOTL.GD.ZS), the Worldwide Governance Indicators' control of corruption estimate (GOV_WGI_CC.EST, about -2.5 to +2.5) and GDP per head at PPP in constant 2021 dollars (NY.GDP.PCAP.PP.KD), each with its year | World Bank, World Development Indicators and Worldwide Governance Indicators | CC BY 4.0 | 2026-11-20 |
| `fred_LNS11300002.csv`, `fred_LNS11300001.csv` | labour force participation rates of women and of men 16 and over, percent, monthly, seasonally adjusted, from 1948 | U.S. Bureau of Labor Statistics, via FRED | public domain | 2026-11-21 |
| `fred_PPU18US00000A156NCEN.csv`, `fred_PPAAUS00000A156NCEN.csv` | the official poverty rate of children under 18 and of everyone, percent, annual from 1989 (1990 and 1991 missing), from the Small Area Income and Poverty Estimates; the official measure counts cash income before taxes, so it leaves out tax credits | U.S. Census Bureau, via FRED | public domain | 2026-11-21 |
| `star_1985_1989.csv` | Tennessee's Project STAR: 11,598 pupils assigned at random within schools to small classes, regular classes or regular classes with an aide; gender, ethnicity, birth quarter, class type, reading and maths scaled scores, free lunch, school type, teacher's experience and ethnicity and school id in kindergarten; class types in grades 1-3 and scores in grade 3 | the Project STAR public access data set (Tennessee State Department of Education), via the R package AER 1.2-17 (CRAN), from the online complements to Stock and Watson (2007) | GPL-2 or GPL-3 (the package); the data are the project's | 2026-11-21 |
| `caschools_1999.csv` | California's 420 K-6 and K-8 school districts, 1998-99: enrolment, teachers, the shares on income assistance, reduced-price lunch and learning English, computers, spending per pupil, average income, reading and maths scores | California Department of Education, as compiled by Stock and Watson (2007), via the R package AER 1.2-17 (CRAN) | GPL-2 or GPL-3 (the package); public records | 2026-11-21 |
| `fertility_1980.csv` | AER's random subsample of 30,000 of Angrist and Evans's (1998) married women aged 21-35 with two or more children in the 1980 US Census: a third child, the sexes of the first two, age, ethnicity, weeks worked in 1979 | Angrist and Evans (1998), via the R package AER 1.2-17 (CRAN), from the online complements to Stock and Watson (2007) | GPL-2 or GPL-3 (the package); public-use census microdata | 2026-11-21 |
| `cigarettes_1985_1995.csv` | cigarettes in the 48 continental US states, 1985 and 1995: CPI, population, packs a head, personal income, excise taxes, price including sales tax, all taxes (cents a pack, nominal) | Stock and Watson (2007), from *The Tax Burden on Tobacco*, via the R package AER 1.2-17 (CRAN) | GPL-2 or GPL-3 (the package); public records | 2026-11-21 |
| `doctor_visits_1977.csv` | the 1977-78 Australian Health Survey: 5,190 adults' doctor visits in two weeks, sex, age, income, illness, days of reduced activity, a health score, private insurance, free government insurance for low income and for age or service, chronic conditions | Cameron and Trivedi (1986), via the R package AER 1.2-17 (CRAN), from the Journal of Applied Econometrics Data Archive | GPL-2 or GPL-3 (the package); the data are the survey's | 2026-11-21 |
| `murder_rates_1950.csv` | murder in 44 US states, 1950: murders per 100,000, convictions per murder, executions per conviction, median months served, median family income, labour force participation, non-white share, southern | Maddala (2001), Table 8.4, after McManus (1985), via the R package AER 1.2-17 (CRAN) | GPL-2 or GPL-3 (the package); public records | 2026-11-21 |

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
| `samuelson_ulam` | Ulam's challenge and Samuelson's answer, comparative advantage, as Samuelson told it in 1969 (the wording as several sources reproduce it) | 2026-11-20 |
| `ricardo_1817` | Ricardo's four numbers: the labour of men for a year to make cloth and wine in England (100, 120) and Portugal (90, 80), *Principles*, ch. 7 | 2026-11-20 |
| `bernhofen_brown_2004` | Japan's trade composition, 1868-75 (table 1), and the inner product of autarky prices and net exports, 1868-75, by component (table 2), Bernhofen and Brown, JPE 112(1) (2004) | 2026-11-20 |
| `bernhofen_brown_2005` | the upper bound on Japan's gains from opening, 8-9% of GDP, AER 95(1) (2005), abstract | 2026-11-20 |
| `irwin_2005` | the welfare cost of the Jeffersonian embargo, about 5% of 1807 GNP (8% in the 2001 working paper), Review of International Economics 13(4) (2005) | 2026-11-20 |
| `leontief_1953` | capital and labour per million dollars of US exports and import replacements, 1947, Leontief (1953) | 2026-11-20 |
| `trefler_1995` | the sign test (0.50) and variance ratio (0.032) of Trefler (1995), as reported; recomputed from his data | 2026-11-20 |
| `irwin_smoot_hawley` | the average US tariff on dutiable imports, 1929, 1932 and 1948, Irwin (1998, 2011) | 2026-11-20 |
| `acr_2012` | the gains-from-trade formula applied to the United States: domestic share 0.93, elasticities 5-10, gains 0.7-1.4%, Arkolakis, Costinot and Rodriguez-Clare, AER 102(1) (2012) | 2026-11-20 |
| `goldberg_maggi_1999` | protection for sale fitted to US tariffs in 1983: welfare weighed 50-88 times contributions (NBER WP 5942), AER 89(5) (1999) | 2026-11-20 |
| `costinot_donaldson_2012` | 17 crops, 1.6 million parcels, 55 countries, slope 0.21, AER P&P 102(3) (2012) | 2026-11-20 |
| `taa` | trade adjustment assistance: the Trade Expansion Act (PL 87-794, 11 October 1962), CRS R41922, and Hyman's estimate of about $50,000 more cumulative earnings over ten years (2018) | 2026-11-20 |
| `ideal_x` | the Ideal X's voyage of 26 April 1956 with 58 trailers, and McLean's loading costs ($5.83 a ton by hand, under 16 cents in containers) | 2026-11-20 |
| `bernard_jensen_1995` | exporting plants as a share of US manufacturing plants, 1976 (10.4%) and 1987 (14.6%), with over half of shipments | 2026-11-20 |
| `adh_2013` | Autor, Dorn and Hanson's coefficients (-0.596 by 2SLS, -0.171 by OLS), exposure ($1,140 and $1,839 per worker) and implied falls, from NBER WP 18054 | 2026-11-20 |
| `fajgelbaum_2020` | the 2018-19 tariffs: complete pass-through, buyers' loss $51bn (0.27% of GDP), net loss $7.2bn (0.04%); Amiti, Redding and Weinstein (2019) | 2026-11-20 |
| `boehm_2023` | trade elasticities: -0.76 in the short run, about -2 in the long run, seven to ten years to converge | 2026-11-20 |
| `krugman_1995` | trade with developing countries and the skilled-unskilled wage ratio: Krugman's 3 points (1995) beside Lawrence, Cline and Borjas-Freeman-Katz, as tabulated in Krugman (2008) | 2026-11-20 |
| `xing_detert_2010` | the iPhone and the 2009 US deficit with China ($1.9bn gross), China's value added ($6.50 a phone), and a $48m US surplus in value added | 2026-11-20 |
| `mccallum_1995` | McCallum's border effect (about 22 times, 1988) and Anderson and van Wincoop's correction | 2026-11-20 |
| `saiz_2010` | housing supply elasticities for 40 of the 95 large metropolitan areas of Table VI (Miami 0.60 to Wichita 5.45), the population-weighted mean 1.75, unweighted 2.5, common 1.54 | 2026-11-20 |
| `cdgr_2010` | the elasticity of wages to density in France: raw about 0.05, 0.033 with worker effects, 0.027 with both corrections, 0.02 preferred | 2026-11-20 |
| `arsw_2015` | the Berlin Wall's structural estimates: production externalities 0.071 decaying at 0.36, residential 0.155 at 0.76, commuting 0.07 a minute, Frechet 6.83 | 2026-11-20 |
| `ciccone_hall_1996` | productivity and density across US states: 5-6 percent per doubling of employment density | 2026-11-20 |
| `dmq_2019` | San Francisco's 1994 rent-control expansion: tenants' mobility down 20 percent, landlords' rental supply down 15 percent | 2026-11-20 |
| `chk_2016` | Moving to Opportunity: children who moved before 13 earn $3,477 (31%) more in their mid-twenties, on a control mean of $11,270 | 2026-11-20 |
| `hsieh_moretti_2019` | housing constraints and growth: 36 percent of growth 1964-2009 (Hsieh and Moretti 2019), and Greaney's (2026) comment: coding errors, an effect two orders of magnitude smaller | 2026-11-20 |
| `donaldson_2018` | railroads in colonial India: real agricultural income up 16 percent in districts reached | 2026-11-20 |
| `baum_snow_2007` | highways and suburbs: one new highway, central-city population down about 18 percent; without the interstates +8 percent instead of -17 percent, 1950-1990 | 2026-11-20 |
| `kline_moretti_2014` | the Tennessee Valley Authority: agricultural gains reversed, manufacturing gains persisted, local gains offset nationally | 2026-11-20 |
| `shenzhen` | Shenzhen's population: 314,100 in 1979, 17.56 million in the 2020 census | 2026-11-20 |
| `schelling_1971` | Schelling's segregation model: the 1969 memorandum, the 1971 paper, the 1978 book, and Sakoda's 1949 precursor | 2026-11-20 |
| `ck_1994` | Card and Krueger's minimum-wage case study: $4.25 to $5.05 in New Jersey, 410 stores, Table 3's employment means | 2026-11-20 |
| `nw_2000` | Neumark and Wascher's payroll records (-4.6%, an elasticity of -0.24 to the minimum) and Card and Krueger's BLS reply | 2026-11-20 |
| `cdlz_2019` | the bunching estimator: 138 state increases, low-wage jobs unchanged over five years, an own-wage elasticity of 0.41 (0.43) | 2026-11-20 |
| `jardim_2022` | Seattle's $11 and $13 minimums: hours down; elasticities -0.2 to -2.0 | 2026-11-20 |
| `cabs` | cab drivers' daily labour supply (Camerer et al. 1997; Farber 2015) and Uber drivers' intertemporal elasticity of about 1.2 | 2026-11-20 |
| `chetty_2011` | micro labour supply elasticities: Hicksian 0.3 and 0.25, Frisch 0.5 and 0.25 (intensive, extensive) | 2026-11-20 |
| `ss_2021` | the meta-analysis of firm-level labour supply elasticities (about 800 estimates) | 2026-11-20 |
| `ak_1991` | quarter of birth: compulsory schooling keeps up to 25% of potential dropouts in school; IV close to OLS; weak instruments | 2026-11-20 |
| `oreopoulos_2006` | Britain's school-leaving age from 14 to 15: a discontinuity, and large returns | 2026-11-20 |
| `mariel` | the Mariel boatlift: Card (no effect), Borjas (-10 to -30% for non-Hispanic male dropouts), Peri and Yasenov (no significant effect) | 2026-11-20 |
| `kearl_1979` | the survey: 90% of 211 economists agreed, at least with provisos, that a minimum wage raises unemployment among the young and unskilled | 2026-11-20 |
| `km_1992` | Katz and Murphy's relative-demand regression, 1963-87: a supply coefficient of about -0.709, an elasticity of 1.41 | 2026-11-20 |
| `sigma_skill` | other elasticities between college and high-school workers (Card and Lemieux about 2.5; Ciccone and Peri about 1.5) and Autor, Goldin and Katz's shares of rising inequality due to education (75% in 1980-2000, 38% in 2000-17) | 2026-11-20 |
| `alm_2003` | tasks: computers substitute for routine tasks and complement non-routine ones; polarization, 1980-2005 | 2026-11-20 |
| `ar_2020` | robots: one more per thousand workers lowers a commuting zone's employment rate 0.2 points and wages 0.42% | 2026-11-20 |
| `chk_2013` | West Germany's AKM decomposition: firm effects 18.5% to 21.2% of the variance, twice the covariance 2.3% to 16.4% (1985-91 to 2002-09) | 2026-11-20 |
| `adkpv_2020` | superstar firms and the falling labour share; Rosen's superstars | 2026-11-20 |
| `unions` | union membership: 20.1% of employees in 1983, 9.9% in 2024 (public sector 32.2%, private 5.9%) | 2026-11-20 |
| `mas_pallais_2017` | the price of flexibility: 20% of wages to avoid short-notice schedules, 8% to work from home | 2026-11-20 |
| `bm_2004` | the resumes: White names receive 50% more call-backs; callbacks respond more to quality for White names | 2026-11-20 |
| `discrimination` | blind auditions (Goldin and Rouse 2000); the meta-analysis of US field experiments since 1989 (Quillian et al. 2017: 36% more call-backs, no change); Becker, Phelps and Arrow | 2026-11-20 |
| `gender` | Goldin's last chapter (long and particular hours); the child penalty in Denmark (about 20% in the long run; the share of gender inequality due to children about 40% in 1980 and 80% in 2013) | 2026-11-20 |
| `frontier39` | pay transparency laws lower wages about 2% (Cullen and Pakzad-Hurson 2023); Amazon's experimental resume screen (Reuters 2018) | 2026-11-20 |
| `leontief_1983` | Leontief's horses: the role of humans as a factor of production bound to diminish, as horses' was by tractors | 2026-11-20 |
| `pen_1971` | Pen's parade: the population marching past in an hour, each as tall as their income | 2026-11-20 |
| `atkinson_1970` | Atkinson's index of inequality and the ranking of crossing Lorenz curves | 2026-11-20 |
| `piketty_saez_2003` | the top income shares from tax returns, 1913 on (the series itself is the Data Room's saez) | 2026-11-20 |
| `auten_splinter_2024` | the measurement dispute: Auten and Splinter's top 1% shares (pre-tax +2.6 points since the early 1960s; after-tax +1.4 points since 1979; fiscal income 9% to 19%, 1962-2019) and Piketty, Saez and Zucman's after-tax share (9% in 1960, 15% in 2019) | 2026-11-20 |
| `pareto_1896` | Pareto's law; random growth with a floor or with births and deaths (Champernowne 1953; Gabaix 2009) | 2026-11-20 |
| `gllm_2016` | the dynamics of inequality: standard random growth is too slow; scale and type dependence | 2026-11-20 |
| `capital_2014` | r > g and the replies: housing (Rognlie 2015), depreciation (Krusell and Smith 2015), the elasticity of substitution | 2026-11-20 |
| `kuznets_1955` | Kuznets's inverted U and his own description of the paper (5 per cent information, 95 per cent speculation) | 2026-11-20 |
| `ige_studies` | the intergenerational elasticity: Solon (0.4 or higher), Mazumder (about 0.6), Corak's 22 countries (below 0.2 to almost 0.7) | 2026-11-20 |
| `chetty_2014` | the rank-rank slope 0.341, the elasticity 0.344, Charlotte 4.4% and San Jose 12.9% | 2026-11-20 |
| `chetty_2017` | absolute mobility: about 90% for children born in 1940, 50% for the 1980s | 2026-11-20 |
| `places` | childhood exposure effects (about 4% a year) and Moving to Opportunity (+$3,477, 31%, for moves before 13) | 2026-11-20 |
| `global` | the elephant curve, 1988-2008: gains around the global median and at the top 1%, none around the 80th-85th percentiles | 2026-11-20 |
| `matters` | life expectancy at 40: the richest 1% against the poorest 1%, 14.6 years for men and 10.1 for women | 2026-11-20 |
| `frontier40` | distributional national accounts; Denmark's wealth taxes; Swedish adoptees' wealth | 2026-11-20 |
| `forbes_400` | the Forbes 400's wealth: a Pareto exponent of 1.49 on average, 1988-2003 | 2026-11-20 |
| `laffer_1974` | the Laffer curve's origin: the 1974 dinner, Wanniski's account and the disputed napkin | 2026-11-20 |
| `harberger_1962` | corporate tax incidence: Harberger's closed economy; workers bear about 51% in German municipalities (Fuest, Peichl and Siegloch) | 2026-11-20 |
| `ramsey_1927` | Ramsey's rule; Diamond and Mirrlees's production efficiency; Atkinson and Stiglitz | 2026-11-20 |
| `mirrlees_1971` | the optimal income tax: Mirrlees; Diamond's U-shape; Saez's top rate and the extensive margin | 2026-11-20 |
| `diamond_saez_2011` | the revenue-maximizing top rate: 73% with a = 1.5 and e = 0.25; bargaining raises it (Piketty, Saez and Stantcheva) | 2026-11-20 |
| `eti_studies` | the elasticity of taxable income: Feldstein (at least one), Gruber and Saez (about 0.4), the 2012 review | 2026-11-20 |
| `bunching` | bunching at kinks (Saez 2010: the EITC's first kink, self-employed only) and notches (Kleven and Waseem 2013) | 2026-11-20 |
| `clk_2009` | salience: tax-inclusive tags cut sales about 8% (7.375% sales tax, about 750 products) | 2026-11-20 |
| `capital_tax` | Chamley-Judd's zero long-run capital tax and Straub and Werning's revision | 2026-11-20 |
| `havens` | offshore wealth (8% of household financial wealth), shifted profits (36%), the 15% global minimum (136 of 140) | 2026-11-20 |
| `evasion` | Allingham and Sandmo; Denmark's audit experiment (0.3% and 37%) | 2026-11-20 |
| `frontier41` | footballers' migration: elasticities of about one (foreign) and 0.15 (domestic) | 2026-11-20 |
| `tcja_2017` | the 2017 tax act: 'it will pay for itself'; CBO's $1.9 trillion | 2026-11-20 |
| `oregon_2008` | Oregon's Medicaid lottery: about 90,000 on the list, about 30,000 drawn, 10,000 places; the first stage, care, depression, blood pressure, emergency visits | 2026-11-20 |
| `rand_hie` | the RAND Health Insurance Experiment: design, spending by plan, the -0.2 summary | 2026-11-20 |
| `arrow_1963` | Arrow on the welfare economics of medical care | 2026-11-20 |
| `ui_theory` | Baily and Chetty's formula; Chetty's 60% liquidity share | 2026-11-20 |
| `ui_evidence` | Meyer; Card, Chetty and Weber; Schmieder, von Wachter and Bender; Gruber; Ganong and Noel | 2026-11-20 |
| `chetty_dk_2014` | Denmark's active and passive savers; one cent per dollar of subsidy | 2026-11-20 |
| `disability_2013` | Maestas, Mullen and Strand's examiner design | 2026-11-20 |
| `eitc_2025` | the 2025 EITC schedule for three or more children; Eissa and Liebman | 2026-11-20 |
| `nit_1968` | the negative income tax experiments, as summarized by Robins | 2026-11-20 |
| `ubi_trials` | Finland's basic income experiment, OpenResearch's cash study, GiveDirectly's Kenyan study | 2026-11-20 |
| `mvpf_2020` | Hendren and Sprung-Keyser's 133 policies; the value of Medicaid | 2026-11-20 |
| `pensions` | workers per Social Security beneficiary, 1960-2035; the depletion date | 2026-11-20 |
| `ss_1983` | the 1983 amendments' 75-year solvency and today's depletion date | 2026-11-20 |
| `frontier42` | Part 42's frontier, stated in words | 2026-11-20 |
| `cereal_ftc` | the FTC's 1972 'shared monopoly' complaint against the cereal makers, its dismissal in 1981 and 1982, and the 1980 shares | 2026-11-20 |
| `nevo_2001` | Nevo's measurement of market power in ready-to-eat cereal: what it estimated and found | 2026-11-20 |
| `bain_1951` | Bain's 42 industries, 1936-40, and their profit rates; Demsetz's objection | 2026-11-20 |
| `bresnahan_1982` | Bresnahan's and Lau's identification of conduct by a rotation of demand | 2026-11-20 |
| `lancaster_1966` | Lancaster's characteristics, McFadden's conditional logit, Berry's inversion | 2026-11-20 |
| `blp_1995` | Berry, Levinsohn and Pakes: 2,217 model-years, 1971-1990, the random-coefficient estimator | 2026-11-20 |
| `petrin_2002` | Petrin's minivan and the value of new products | 2026-11-20 |
| `production_1996` | Olley and Pakes, Levinsohn and Petrin, Ackerberg, Caves and Frazer; Syverson's 90/10 ratio of 1.92 | 2026-11-20 |
| `dlw_2012` | De Loecker and Warzynski's markup formula; De Loecker, Eeckhout and Unger's 1.21 and 1.61 | 2026-11-20 |
| `markup_critique` | Traina, Basu and Bond et al. on markups from production data | 2026-11-20 |
| `br_1991` | Bresnahan and Reiss's isolated towns and entry thresholds | 2026-11-20 |
| `merger_2023` | the 2023 Merger Guidelines' presumptions and the 2010 thresholds; Farrell and Shapiro; Werden | 2026-11-20 |
| `millercoors` | the 2008 MillerCoors clearance and the two studies of its effects | 2026-11-20 |
| `axtell_2001` | Axtell's Zipf law for 5.5 million American firms | 2026-11-20 |
| `frontier43` | Part 43's frontier, stated in words | 2026-11-20 |
| `rust_1987` | Rust's bus engine model, data and the rejection of myopia; Hotz and Miller's CCPs | 2026-11-20 |
| `dynamic_io` | Ericson and Pakes, Pakes and McGuire, Bajari, Benkard and Levin, Ryan's cement | 2026-11-20 |
| `vertical` | double marginalization, the Chicago critique, resale price maintenance after Leegin | 2026-11-20 |
| `platforms` | Rochet and Tirole, Armstrong, Rysman's Yellow Pages, Ohio v. American Express | 2026-11-20 |
| `qwerty` | David's QWERTY, Liebowitz and Margolis's reply, Arthur's lock-in | 2026-11-20 |
| `innovation` | Arrow's replacement effect, the inverted U, killer acquisitions | 2026-11-20 |
| `algorithms` | Q-learning collusion and German petrol stations' algorithms | 2026-11-20 |
| `antitrust` | Standard Oil, Microsoft, Google's liability and remedies, the neo-Brandeisian critique | 2026-11-20 |
| `regulation` | Baron and Myerson; Laffont and Tirole | 2026-11-20 |
| `retrospectives` | Kwoka's merger retrospectives and their critics | 2026-11-20 |
| `apple` | Ballmer's 2007 remark and IDC's 2023 shipments | 2026-11-20 |
| `frontier44` | Part 44's frontier, stated in words | 2026-11-20 |
| `gym_2006` | DellaVigna and Malmendier's gym contracts and attendance (Part 45) | 2026-11-20 |
| `departures_2009` | DellaVigna's three classes of departures (Part 45) | 2026-11-20 |
| `kkt_1990` | Kahneman, Knetsch and Thaler's mug experiments; Tversky and Kahneman's 1992 parameters (Part 45) | 2026-11-20 |
| `list_2003` | List's sports-card traders (Part 45) | 2026-11-20 |
| `reference_field` | marathon finishing times, PGA putts and Boston condominium sellers (Part 45) | 2026-11-20 |
| `present_bias` | Phelps and Pollak, Laibson, O'Donoghue and Rabin, DellaVigna and Malmendier (2004) (Part 45) | 2026-11-20 |
| `seed_2006` | Ashraf, Karlan and Yin's commitment savings trial (Part 45) | 2026-11-20 |
| `defaults_45` | Madrian and Shea; Save More Tomorrow; Carroll et al. (Part 45) | 2026-11-20 |
| `inattention_45` | Gabaix and Laibson's shrouded attributes; left-digit bias in car prices (Part 45) | 2026-11-20 |
| `social_45` | Fehr and Schmidt; Gneezy and List; List's dictator games (Part 45) | 2026-11-20 |
| `welfare_45` | Bernheim and Rangel; libertarian paternalism; the limits of arbitrage (Part 45) | 2026-11-20 |
| `nudges_2022` | DellaVigna and Linos's two nudge units against the academic journals (Part 45) | 2026-11-20 |
| `limits_45` | rational inattention, sparsity, diagnostic expectations (Part 45) | 2026-11-20 |
| `practice_45` | Part 45's practice chapter, stated in words | 2026-11-20 |
| `frontier45` | Part 45's frontier, stated in words | 2026-11-20 |
| `cohen_dupas_2010` | Cohen and Dupas's randomized bed-net prices at Kenyan prenatal clinics (Part 46) | 2026-11-20 |
| `poverty_lines` | the international poverty line's history, Chen and Ravallion's 2008 revision, Deaton on prices (Part 46) | 2026-11-20 |
| `traps_46` | Kraay and McKenzie on poverty traps; Balboni et al.'s Bangladesh threshold (Part 46) | 2026-11-20 |
| `dual_46` | Lewis's dual economy; Gollin, Lagakos and Waugh's agricultural productivity gap (Part 46) | 2026-11-20 |
| `credit_46` | Aleem's moneylenders; six microcredit trials; Meager; returns to capital in Sri Lanka and Mexico (Part 46) | 2026-11-20 |
| `cash_46` | PROGRESA's design and Schultz; Haushofer and Shapiro; Egger et al.'s multiplier; PANES and political support (Part 46) | 2026-11-20 |
| `graduation_2015` | the graduation programme in six countries (Part 46) | 2026-11-20 |
| `schools_46` | Duflo's Indonesian schools; Teaching at the Right Level; learning poverty (Part 46) | 2026-11-20 |
| `health_46` | Miguel and Kremer's deworming and the 2015 re-analyses; Thornton's HIV-results incentives (Part 46) | 2026-11-20 |
| `risk_46` | Townsend's village insurance; rainfall insurance take-up; Cai et al.'s networks (Part 46) | 2026-11-20 |
| `farms_46` | Duflo, Kremer and Robinson's fertilizer offers; Suri and Jack's mobile money (Part 46) | 2026-11-20 |
| `history_46` | Dell's mita; Nunn's slave trades (Part 46) | 2026-11-20 |
| `debate_46` | Deaton's critique, the 2019 prize, Vivalt on generalizing, China's poverty reduction (Part 46) | 2026-11-20 |
| `practice_46` | GiveWell's cost per life; Sachs's 2005 forecast; the Millennium Villages' evaluation (Part 46) | 2026-11-20 |
| `frontier46` | scaling; poverty from satellites and phones; Togo's Novissi (Part 46) | 2026-11-20 |
| `olken_2007` | Olken's road audits, perceptions and missing rice (Part 47) | 2026-11-21 |
| `olson_1965` | Olson's collective action; GAO on the sugar program; the number of sugar farms (Part 47) | 2026-11-21 |
| `rents_47` | Tullock's rectangle; Krueger's rents in India and Turkey (Part 47) | 2026-11-21 |
| `voters_47` | voters elect rather than affect policies; Lee's incumbency estimate and its critics (Part 47) | 2026-11-21 |
| `capture_47` | Stigler's capture; protection for sale and Goldberg and Maggi; Fisman's political connections (Part 47) | 2026-11-21 |
| `agency_47` | Barro and Ferejohn's agency model; Ferraz and Finan's audited mayors (Part 47) | 2026-11-21 |
| `corruption_47` | diplomats' parking tickets; Uganda's school grants (Part 47) | 2026-11-21 |
| `franchise_47` | Acemoglu and Robinson's franchise; democracy and growth (Part 47) | 2026-11-21 |
| `state_47` | Besley and Persson's state capacity (Part 47) | 2026-11-21 |
| `conflict_47` | rainfall, growth and civil conflict; the resource curse (Part 47) | 2026-11-21 |
| `media_47` | the Fox News effect; trade exposure and polarization (Part 47) | 2026-11-21 |
| `cycles_47` | the political business cycle; delegation to a conservative central bank (Part 47) | 2026-11-21 |
| `practice_47` | the Treasury's 2016 short-term forecast and what followed (Part 47) | 2026-11-21 |
| `frontier47` | populist leaders and the economy; V-Dem (Part 47) | 2026-11-21 |
| `bet_1980` | Simon and Ehrlich's wager and Kiel, Matheson and Golembiewski's rerun (Part 48) | 2026-11-21 |
| `hotelling_1931` | Hotelling's rule (Part 48) | 2026-11-21 |
| `fish_48` | Costello, Gaines and Lynham on catch shares (Part 48) | 2026-11-21 |
| `dice_2023` | DICE-2023's damages, control rates, temperatures and social cost of carbon (Part 48) | 2026-11-21 |
| `scc_us` | Rennert et al.'s and EPA's social cost of carbon (Part 48) | 2026-11-21 |
| `stern_2006` | the Stern Review's discounting and social cost of carbon (Part 48) | 2026-11-21 |
| `weitzman_2009` | Weitzman's dismal theorem and Dietz et al.'s tipping points (Part 48) | 2026-11-21 |
| `instruments_48` | British Columbia's carbon tax and the EU ETS's prices (Part 48) | 2026-11-21 |
| `clubs_2015` | Nordhaus's climate clubs and Acemoglu et al.'s directed technical change (Part 48) | 2026-11-21 |
| `damages_48` | Dell, Jones and Olken; Burke, Hsiang and Miguel (Part 48) | 2026-11-21 |
| `health_48` | heat, air conditioning and the Huai River (Part 48) | 2026-11-21 |
| `california_2000` | Borenstein, Bushnell and Wolak on California's electricity market (Part 48) | 2026-11-21 |
| `elasticity_48` | gasoline and electricity price elasticities (Part 48) | 2026-11-21 |
| `hubbert_1956` | Hubbert's peak and Deming's review (Part 48) | 2026-11-21 |
| `frontier48` | Bilal and Känzig's global temperature shocks; McGlade and Ekins's unburnable reserves (Part 48) | 2026-11-21 |
| `becker_1968` | Becker's parking space, his 1968 paper and Nobel lecture (Part 49) | 2026-11-21 |
| `police_49` | police and crime: Buenos Aires, London, measurement error, Levitt's and Evans and Owens's elasticities (Part 49) | 2026-11-21 |
| `certainty_49` | certainty against severity: Nagin's review, Lee and McCrary's age-18 discontinuity (Part 49) | 2026-11-21 |
| `murder_1950` | Ehrlich's executions, Leamer's and McManus's critiques (Part 49) | 2026-11-21 |
| `family_49` | the household, marriage (Becker, Choo and Siow) and the pill (Part 49) | 2026-11-21 |
| `fertility_49` | Angrist and Evans's same-sex siblings; China's population policy (Part 49) | 2026-11-21 |
| `bargain_49` | Lundberg, Pollak and Wales on the UK child benefit (Part 49) | 2026-11-21 |
| `schools_49` | STAR, Maimonides' rule and its redux, teachers' value added (Part 49) | 2026-11-21 |
| `early_49` | Perry Preschool, Head Start, Tennessee's pre-K trial, the Heckman curve (Part 49) | 2026-11-21 |
| `health_49` | Grossman, caesarean sections, hospital prices (Part 49) | 2026-11-21 |
| `drugs_49` | deaths of despair and the origins of the opioid crisis (Part 49) | 2026-11-21 |
| `addiction_49` | rational addiction and its test (Part 49) | 2026-11-21 |
| `critics_49` | economics imperialism and crowding out: fines, blood, a nuclear site (Part 49) | 2026-11-21 |
| `frontier49` | sex ratios and saving; fertility and women's work (Part 49) | 2026-11-21 |
| `ctc_2021` | the 2021 child tax credit, its monthly payments, child poverty on two measures, parents' work (Part 50) | 2026-11-21 |
| `allowance_50` | a permanent allowance simulated; Canada's Child Benefit; Canadian benefits and children; Mothers' Pensions (Part 50) | 2026-11-21 |
| `credits_50` | the child tax credit before and in 2021, and the 2021 EITC (Part 50) | 2026-11-21 |
| `frontier50` | Baby's First Years at age four; Quebec's allowance for newborns; how the 2021 payments were spent (Part 50) | 2026-11-21 |
