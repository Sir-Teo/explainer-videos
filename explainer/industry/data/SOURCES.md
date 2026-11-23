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
