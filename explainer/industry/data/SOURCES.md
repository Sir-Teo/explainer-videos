# The Filing Room: sources

Every source *Industry, Built* draws a figure from, with what it is, its terms and where its rows are. Figures are
entered as rows of the Register (`rows_pNN.py`), each with its URL, the date it describes and the date it was
checked; nothing is downloaded at render time and no third-party dataset is committed. `python tools/check_register.py
industryN` checks a part's rows.

| Source | Kind | Terms | Used in |
|---|---|---|---|
| SEC EDGAR: Forms 10-K, 20-F and 6-K, and the XBRL company facts (Apple, Qualcomm, Micron, Broadcom, Corning, Skyworks, Qorvo, Cirrus Logic, TSMC) | filing | US government work, public domain | Part 1 |
| Company results not filed with the SEC: Samsung Electronics, SK hynix, Xiaomi (HKEX), Hon Hai, Sony, Transsion | filing, or as reported where the company's own release could not be read (marked `press`) | the companies' public releases | Part 1 |
| IDC Worldwide Quarterly Mobile Phone Tracker, press releases (2026-01-13, 2026-08-28) | tracker | public press releases; figures quoted, not redistributed | Part 1 |
| Counterpoint Research: shipments (Q3 2026), operating-profit share (Q2 2023), revenue share (Q2 2026), the iPhone 18 Pro Max bill of materials | tracker | public insights pages, or as reported | Part 1 |
| TrendForce: the iPhone 18 Pro bill of materials and memory prices (as reported by MacRumors, 2026-08-10) | tracker | as reported | Part 1 |
| The Wall Street Journal's memory-cost estimates (as reported by MacRumors, 2026-07-10) | press | as reported | Part 1 |
| Omdia: Africa smartphone shipments, 2025 (as reported by TelecomLead) | tracker | as reported | Part 1 |
| Linden, Kraemer and Dedrick (2007), *Who Captures Value in a Global Innovation System? The case of Apple's iPod*, eScholarship (UC Irvine) | study | open access | Part 1 |
| Xing and Detert (2010), *How the iPhone Widens the United States Trade Deficit with the People's Republic of China*, ADBI Working Paper 257 | study | open access | Part 1 |
| T-Mobile US and AT&T Forms 10-K, 2025 (equipment and service revenues and costs) | filing | public domain | Part 1 |
| Apple Newsroom, results release of 2026-01-29 (installed base of 2.5 billion active devices) | filing | the company's public release | Part 1 |
| *United States v. Google LLC*, memorandum opinion, D.D.C., 2024-08-05 (Google's payment to Apple), as reported by NPR | official | public court record | Part 1 |
| FRED: DEXCHUS, DEXKOUS (daily exchange rates, averaged by year) | official | public domain (Federal Reserve Board H.10) | Part 1 |
| Apple list prices as reported by MacRumors (2026-09-09, 2026-09-12) | press | as reported | Part 1 |
| Forms 10-K of Amazon, Walmart, UnitedHealth Group, McKesson, NVIDIA, Alphabet, Microsoft and Meta (revenue, operating income, employees, segments; SEC frames and filings) | filing | public domain | Part 2 |
| BEA, GDP by industry: value added, its components and shares of GDP, 2025 (`ValueAdded.xlsx`: TVA105, TVA110, TVA112, released 2026-09-30) and 1947-1997 (`AllTablesHist.zip`) → `bea_va_2025.csv`, `bea_va_history.csv` | official | US government work, public domain | Part 2 |
| BEA, input-output use table after redefinitions, sector level, 2023, producers' prices, with its final uses (`AllTablesIO.zip`) → `bea_io_2023.csv` | official | public domain | Part 2 |
| BLS Current Employment Statistics, annual averages by industry, and the Federal Reserve's manufacturing output index (OUTMS), via FRED → `fred_jobs.csv` | official | public domain | Part 2 |
| World Bank, World Development Indicators: NV.IND.MANF.ZS, NV.AGR.TOTL.ZS, NV.SRV.TOTL.ZS, NV.IND.MANF.CD → `wb_shares.csv`, `wb_mfg_usd.csv` | official | CC BY 4.0 | Part 2 |
| US Census Bureau, NAICS 2022 | official | public domain | Part 2 |
| US Census Bureau, Statistics of US Businesses, 2022 (released 2025-04-10): firms, establishments, employment and receipts by enterprise size, US and by sector → `census_susb_2022.csv` | official | public domain | Part 2 |
| BEA, real value added and value-added prices by industry, chain-type indexes, 1997-2025 (`ValueAdded.xlsx`: TVA103-A, TVA104-A) → `bea_real.csv` | official | public domain | Part 2 |
| SEC EDGAR company facts: annual 10-K revenue, operating income, net income, operating cash flow, capital spending, assets, equity, depreciation and inventories for the companies in `SEC_COMPANIES` → `sec_annual.csv` | filing | public domain | Parts 3, 5, 6 |
| BLS consumer price indexes (US city average) and average hourly earnings of production and nonsupervisory employees, annual averages since 2000, via FRED → `fred_prices.csv` | official | public domain | Part 2 |
| Leontief (1936), *Review of Economics and Statistics* 18(3); Leontief (1983), National Academy of Engineering; the Nobel Foundation (1973) | study | quoted | Part 2 |
| Antràs, Chor, Fally and Hillberry (2012), *AER Papers and Proceedings* 102(3) (upstreamness: the method, not data) | study | method | Part 2 |
| US Census Bureau, 2022 Economic Census, Concentration of Largest Firms for the U.S. (`ECNSIZE2022.zip`, released 2025-04-24): the share of sales of the 4, 8, 20 and 50 largest firms, firms and sales for every six-digit industry with a published figure → `census_conc_2022.csv` | official | public domain | Part 5 |
| FRED (Federal Reserve Bank of St. Louis): the NBER Macrohistory Database's monthly wholesale price of hogs and live hog receipts at Chicago (1858-1940) and hogs slaughtered in the US (1879-1957); the Census Bureau's housing starts, units under construction and completed, and months' supply of new houses; WTI crude; retail sales and manufacturers' new orders; industrial production of semiconductors (`FRED_CYCLE`) → `fred_cycle.csv` | official | public domain (NBER, Census, EIA, Fed) | Part 6 |
| A.P. Moller - Maersk A/S annual reports 2020, 2022, 2024 and 2025, ESEF (inline XBRL) filings as converted to xBRL-JSON by filings.xbrl.org: group revenue, EBIT and depreciation, 2019-2025 → `esef_maersk.csv` | filing | public filings | Part 6 |
| SEC EDGAR company facts: quarterly revenue and operating income of Micron and Intel from Forms 10-Q and 10-K (fourth quarters derived from the year less three quarters) → `sec_quarterly.csv` | filing | public domain | Part 6 |
| Our World in Data, 'Technology adoption by households in the United States' (Comin and Hobijn (2004) and later sources): the share of households using about forty technologies, year by year → `owid_tech.csv` | study | CC BY 4.0 | Part 7 |
| FRED: the Census Bureau's Annual Integrated Economic Survey for bottled water manufacturing (shipments, employees), the BLS's producer price index for bottled water, the US population, e-commerce's share of retail sales (Census) and the number of US households (Census, CPS) (`FRED_MARKET`) → `fred_market.csv` | official | public domain | Part 7 |
| Aswath Damodaran, NYU Stern, "Excess Returns (EVA) by industry, US companies", the tables for 2015-2024 (archive, each published the following January) and 2025 (published January 2026): firms, return on capital, cost of capital, book capital → `damodaran_roc.csv` | study | freely published for teaching; cited | Part 5 |
