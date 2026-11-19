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
| `wdi_2015_2025.csv` | World Development Indicators for the 217 economies (not aggregates), 2015-2025: GDP and GDP per head at market exchange rates (current US dollars) and at purchasing power parity (current international dollars), population, Gini index; with each economy's region and income group | World Bank (API, last updated 11 November 2026) | CC BY 4.0 | 2026-11-19 |
| `hdr2025_1990_2023.csv` | Human Development Report 2025, composite indices time series: the HDI, life expectancy, expected and mean years of schooling, GNI per head (2021 PPP dollars), 1990-2023, for the 195 countries (aggregates dropped) | UNDP Human Development Report Office | CC BY 3.0 IGO | 2026-11-19 |
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
`6a7971b31b7336551705465de8a0855826f3652abe112406f52b2c2ed0994c0c`. The World Bank's API returns JSON pages that
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
