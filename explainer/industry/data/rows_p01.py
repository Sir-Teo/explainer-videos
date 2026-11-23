"""Register rows for Part 1, *Where the Money Goes* (the smartphone).  Checked 2026-11-23 unless stated.

Money is in US dollars unless the unit says otherwise; company totals in billions.  Exchange rates are FRED's annual
averages of daily noon rates (rows ``fx.*``).
"""

from explainer.industry.register import Row, add

C = "2026-11-23"
EDGAR = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
APPLE_10K_26 = "https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm"
APPLE_10K_25 = "https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm"
IDC_Q425 = "https://www.idc.com/resource-center/press-releases/q425mobilephonetop5/"
IPOD = "https://escholarship.org/uc/item/1770046n"

add(
    # --- the 2007 iPod study (Linden, Kraemer and Dedrick) --------------------------------------------------------
    Row("ipod.price", 299, "USD", "Retail price of the 30GB fifth-generation (video) iPod at the time of the teardown",
        "Linden, Kraemer and Dedrick (2007), Who Captures Value in a Global Innovation System? The case of Apple's iPod",
        IPOD, "2005-06", C, "study"),
    Row("ipod.inputs", 144.40, "USD", "Factory cost of all inputs, including assembly and test (Portelligent's estimate)",
        "Linden, Kraemer and Dedrick (2007), text and Table 1", IPOD, "2005", C, "study"),
    Row("ipod.drive", 73.39, "USD", "Factory price of the 30GB hard drive, made by Toshiba in China", "Linden et al. "
        "(2007), Table 1", IPOD, "2005", C, "study"),
    Row("ipod.display", 20.39, "USD", "Display module, Toshiba-Matsushita, made in Japan", "Linden et al. (2007), "
        "Table 1", IPOD, "2005", C, "study"),
    Row("ipod.broadcom", 8.36, "USD", "Video and multimedia processor, Broadcom", "Linden et al. (2007), Table 1",
        IPOD, "2005", C, "study"),
    Row("ipod.assembly", 3.70, "USD", "Insertion, test and assembly by Inventec in China", "Linden et al. (2007), "
        "Table 1", IPOD, "2005", C, "study"),
    Row("ipod.assembly_kept", 0.11, "USD", "Value the authors estimate Inventec captured: $3.70 at its 3% gross margin",
        "Linden et al. (2007), Table 1", IPOD, "2005", C, "study"),
    Row("ipod.apple", 80, "USD", "Apple's gross profit per unit: 75% of $299 (wholesale) less inputs", "Linden et al. "
        "(2007), text and note 6", IPOD, "2005", C, "study"),
    Row("ipod.retail", 45, "USD", "Retail margin (15% of the retail price)", "Linden et al. (2007), Figure 3", IPOD,
        "2005", C, "study"),
    Row("ipod.distribution", 30, "USD", "Distribution margin (10% of the retail price)", "Linden et al. (2007), "
        "Figure 3", IPOD, "2005", C, "study"),

    # --- the iPhone 3G and the trade statistics (Xing and Detert 2010) --------------------------------------------
    Row("iphone3g.cost", 178.96, "USD", "Manufacturing cost of an iPhone 3G, booked in full as a Chinese export",
        "Xing and Detert (2010), How the iPhone Widens the United States Trade Deficit with the People's Republic of "
        "China, ADBI Working Paper 257, after iSuppli's teardown", "https://www.adb.org/publications/how-iphone-widens-"
        "united-states-trade-deficit-peoples-republic-china", "2009", C, "study"),
    Row("iphone3g.china", 6.50, "USD", "Value added in China: assembly by Foxconn (3.6% of the cost)", "Xing and "
        "Detert (2010)", "https://www.adb.org/publications/how-iphone-widens-united-states-trade-deficit-peoples-"
        "republic-china", "2009", C, "study"),
    Row("iphone3g.deficit", 1.9, "USD bn", "The iPhone's contribution to the 2009 US trade deficit with China in gross "
        "trade statistics", "Xing and Detert (2010)", "https://www.adb.org/publications/how-iphone-widens-united-"
        "states-trade-deficit-peoples-republic-china", "2009", C, "study"),

    # --- Apple: filings -------------------------------------------------------------------------------------------
    Row("apple.revenue.fy2026", 478.834, "USD bn", "Apple total net sales, fiscal year to 26 September 2026",
        "Apple Form 10-K, FY2026 (filed 2026-11-03)", APPLE_10K_26, "FY2026", C),
    Row("apple.iphone_sales.fy2026", 254.098, "USD bn", "iPhone net sales, FY2026", "Apple Form 10-K FY2026, net "
        "sales by category", APPLE_10K_26, "FY2026", C),
    Row("apple.services_sales.fy2026", 123.301, "USD bn", "Services net sales, FY2026", "Apple Form 10-K FY2026",
        APPLE_10K_26, "FY2026", C),
    Row("apple.gm_products.fy2026", 0.393, "share", "Products gross margin percentage, FY2026", "Apple Form 10-K FY2026",
        APPLE_10K_26, "FY2026", C),
    Row("apple.gm_products.fy2025", 0.368, "share", "Products gross margin percentage, FY2025", "Apple Form 10-K FY2026",
        APPLE_10K_26, "FY2025", C),
    Row("apple.gm_services.fy2026", 0.762, "share", "Services gross margin percentage, FY2026", "Apple Form 10-K FY2026",
        APPLE_10K_26, "FY2026", C),
    Row("apple.opex.fy2025", 62.151, "USD bn", "Operating expenses (R&D 34.55, SG&A 27.60), FY2025", "Apple Form 10-K "
        "FY2025", APPLE_10K_25, "FY2025", C),
    Row("apple.revenue.fy2025", 416.161, "USD bn", "Total net sales, FY2025", "Apple Form 10-K FY2025", APPLE_10K_25,
        "FY2025", C),
    Row("apple.iphone_sales.fy2025", 209.586, "USD bn", "iPhone net sales, FY2025", "Apple Form 10-K FY2025",
        APPLE_10K_25, "FY2025", C),
    Row("apple.taxrate.fy2025", 0.156, "share", "Provision for income taxes over pre-tax income, FY2025 "
        "(20,719 / 132,729)", "Apple Form 10-K FY2026, income statement", APPLE_10K_26, "FY2025", C),
    Row("apple.net_income.fy2026", 132.175, "USD bn", "Net income, FY2026", "Apple Form 10-K FY2026", APPLE_10K_26,
        "FY2026", C),
    Row("apple.indirect_share.fy2026", 0.60, "share", "Share of net sales through indirect channels (carriers, "
        "resellers), FY2026", "Apple Form 10-K FY2026, Item 1", APPLE_10K_26, "FY2026", C),
    Row("apple.employees.fy2026", 167_000, "people", "Full-time equivalent employees, 26 September 2026",
        "Apple Form 10-K FY2026", APPLE_10K_26, "2026-09-26", C),
    Row("apple.greater_china_sales.fy2026", 82.378, "USD bn", "Net sales in Greater China, FY2026", "Apple Form 10-K "
        "FY2026, segment table", APPLE_10K_26, "FY2026", C),

    # --- iPhone prices (US, before sales tax) -------------------------------------------------------------------------
    Row("price.17pro.256", 1099, "USD", "iPhone 17 Pro, 256GB, US launch price (September 2025)", "MacRumors, "
        "2026-09-09: the 18 Pro, at $1,199, is $100 above the 17 Pro",
        "https://www.macrumors.com/2026/09/09/iphone-18-pro-pricing/", "2025-09", C, "press",
        note="Apple's list price, as reported"),
    Row("price.18pro.256", 1199, "USD", "iPhone 18 Pro, 256GB, US launch price (September 2026)", "MacRumors, "
        "2026-09-12, prices for every storage tier", "https://www.macrumors.com/2026/09/12/how-much-each-iphone-18-"
        "pro-model-costs/", "2026-09", C, "press", note="Apple's list prices as listed by MacRumors on 2026-09-12"),
    Row("price.17promax.tiers", 0, "USD", "iPhone 17 Pro Max list prices: 256GB $1,199; 512GB $1,399; 1TB $1,599; "
        "2TB $1,999", "MacRumors (the 18 Pro Max's increases by tier: +$100, +$100, +$300, +$500)",
        "https://www.macrumors.com/2026/09/09/iphone-18-pro-pricing/", "2025-09", C, "press",
        note="Derived from the 2026 prices and the reported increases"),
    Row("price.18promax.tiers", 0, "USD", "iPhone 18 Pro Max list prices: 256GB $1,299; 512GB $1,499; 1TB $1,899; "
        "2TB $2,499", "MacRumors, 2026-09-12", "https://www.macrumors.com/2026/09/12/how-much-each-iphone-18-pro-"
        "model-costs/", "2026-09", C, "press", note="Apple's list prices as listed by MacRumors"),

    # --- component costs (trackers; estimates) ---------------------------------------------------------------------
    Row("bom.17pro", 520, "USD", "Component cost (bill of materials) of a 256GB iPhone 17 Pro. This series' central "
        "figure: memory of $52 (WSJ) at TrendForce's 10% share of the bill; range across published estimates",
        "TrendForce (via MacRumors, 2026-08-10); Wall Street Journal estimates (via MacRumors, 2026-07-10); "
        "Counterpoint (via MacRumors, 2026-07-10)", "https://www.macrumors.com/2026/08/10/iphone-18-pro-build-cost-"
        "rise/", "2025-09", C, "tracker", lo=450, hi=570,
        note="No teardown house publishes its full iPhone 17 Pro bill openly; the range brackets the reported ones"),
    Row("bom.memory_share.2025", 0.10, "share", "Memory (DRAM and NAND) as a share of a 256GB iPhone Pro's component "
        "cost, a year before Q3 2026", "TrendForce smartphone analysis, via MacRumors 2026-08-10",
        "https://www.macrumors.com/2026/08/10/iphone-18-pro-build-cost-rise/", "2025-Q3", C, "tracker"),
    Row("bom.memory_share.2026", 0.34, "share", "The same share in Q3 2026 (iPhone 18 Pro, 256GB)", "TrendForce, via "
        "MacRumors 2026-08-10", "https://www.macrumors.com/2026/08/10/iphone-18-pro-build-cost-rise/", "2026-Q3", C,
        "tracker"),
    Row("bom.rise.18pro", 0.38, "share", "Rise in the component cost of a 256GB iPhone 18 Pro over the 17 Pro",
        "TrendForce, via MacRumors 2026-08-10", "https://www.macrumors.com/2026/08/10/iphone-18-pro-build-cost-rise/",
        "2026-Q3", C, "tracker"),
    Row("memory.dram.2025", 39, "USD", "DRAM cost per iPhone 18 Pro at 2025 prices (12GB)", "Wall Street Journal "
        "estimate, via MacRumors 2026-07-10", "https://macrumors.com/2026/07/10/iphone-18-pro-max-costs-could-rise",
        "2025", C, "press", note="WSJ's estimate as quoted by MacRumors"),
    Row("memory.dram.2026", 145, "USD", "DRAM cost per iPhone 18 Pro at 2026 prices", "Wall Street Journal estimate, "
        "via MacRumors 2026-07-10", "https://macrumors.com/2026/07/10/iphone-18-pro-max-costs-could-rise", "2026", C,
        "press", note="WSJ's estimate as quoted by MacRumors; matches the reported ~$145 contract price of a 12GB "
                      "LPDDR5X chip (Wccftech, 2026-07-09)"),
    Row("memory.nand256.2025", 13, "USD", "Flash storage cost per 256GB iPhone at 2025 prices", "Wall Street Journal "
        "estimate, via MacRumors 2026-07-10", "https://macrumors.com/2026/07/10/iphone-18-pro-max-costs-could-rise",
        "2025", C, "press", note="WSJ's estimate as quoted by MacRumors"),
    Row("memory.nand256.2026", 51, "USD", "Flash storage cost per 256GB iPhone at 2026 prices", "Wall Street Journal "
        "estimate, via MacRumors 2026-07-10", "https://macrumors.com/2026/07/10/iphone-18-pro-max-costs-could-rise",
        "2026", C, "press", note="WSJ's estimate as quoted by MacRumors"),
    Row("memory.nand1tb.2026", 250, "USD", "Flash storage cost of a 1TB iPhone 18 Pro Max (\"over $250\")",
        "Counterpoint Research BOM infographic, via MacRumors and Wccftech, 2026-07-09/10",
        "https://www.counterpointresearch.com/en/insights/infographic-iphone-17promax-and-iphone-18promax-e-bom-cost-"
        "comparison/", "2026", C, "tracker"),
    Row("memory.price_rise", 6.0, "times", "Rise in memory prices since the start of 2025 (\"five- to sevenfold\")",
        "TrendForce, via MacRumors 2026-08-10", "https://www.macrumors.com/2026/08/10/iphone-18-pro-build-cost-rise/",
        "2025-01 to 2026-08", C, "tracker", lo=5, hi=7),
    Row("memory.lowend_share", 0.65, "share", "Memory as a share of a low-end phone's component cost (\"over 65%\"); "
        "memory costs \"up nearly 300%\" in a year", "IDC press release, 2026-08-28 (Q2 2026)",
        "https://www.idc.com/promo/Smartphone-market-share/vendor", "2026-Q2", C, "tracker"),

    # --- the market (trackers) -------------------------------------------------------------------------------------
    Row("market.units.2025", 1260.3, "million", "Smartphone shipments worldwide, 2025 (preliminary)", "IDC Quarterly "
        "Mobile Phone Tracker, 2026-01-13", IDC_Q425, "2025", C, "tracker", lo=1250, hi=1290,
        note="Omdia: 1.25 billion; Counterpoint: +3%"),
    Row("market.units.2024", 1236.3, "million", "Smartphone shipments worldwide, 2024", "IDC, 2026-01-13", IDC_Q425,
        "2024", C, "tracker"),
    Row("share.apple.units.2025", 247.8, "million", "Apple smartphone shipments, 2025 (19.7%)", "IDC, 2026-01-13",
        IDC_Q425, "2025", C, "tracker"),
    Row("share.samsung.units.2025", 241.2, "million", "Samsung, 2025 (19.1%)", "IDC, 2026-01-13", IDC_Q425, "2025", C,
        "tracker"),
    Row("share.xiaomi.units.2025", 165.3, "million", "Xiaomi, 2025 (13.1%)", "IDC, 2026-01-13", IDC_Q425, "2025", C,
        "tracker"),
    Row("share.vivo.units.2025", 103.9, "million", "vivo, 2025 (8.2%)", "IDC, 2026-01-13", IDC_Q425, "2025", C,
        "tracker"),
    Row("share.oppo.units.2025", 102.0, "million", "OPPO, 2025 (8.1%)", "IDC, 2026-01-13", IDC_Q425, "2025", C,
        "tracker"),
    Row("share.others.units.2025", 400.0, "million", "All other brands, 2025 (31.7%)", "IDC, 2026-01-13", IDC_Q425,
        "2025", C, "tracker"),
    Row("share.apple.units.q4_2024", 77.5, "million", "Apple, Q4 2024 (for the fiscal-year unit estimate)",
        "IDC, 2026-01-13", IDC_Q425, "2024-Q4", C, "tracker"),
    Row("share.apple.units.q4_2025", 81.3, "million", "Apple, Q4 2025", "IDC, 2026-01-13", IDC_Q425, "2025-Q4", C,
        "tracker"),
    Row("market.units.q2_2026", 276.3, "million", "Shipments in Q2 2026, down 7.4% on a year earlier", "IDC press "
        "release, 2026-08-28", "https://www.idc.com/promo/Smartphone-market-share/vendor", "2026-Q2", C, "tracker"),
    Row("market.q3_2026_change", -0.20, "share", "Change in shipments, Q3 2026 on Q3 2025: the lowest third quarter "
        "since 2012 (IDC reportedly -22%)", "Counterpoint Research Market Monitor, preliminary, 2026-10-12",
        "https://www.fonearena.com/blog/494790/global-smartphone-shipments-q3-2026-counterpoint.html", "2026-Q3", C,
        "tracker", lo=-0.22, hi=-0.20, note="Counterpoint's note as reported by FoneArena; IDC's -22% via a secondary "
                                            "report"),
    Row("market.q3_2026_share.samsung", 0.23, "share", "Samsung's share of shipments, Q3 2026", "Counterpoint, "
        "2026-10-12", "https://www.fonearena.com/blog/494790/global-smartphone-shipments-q3-2026-counterpoint.html",
        "2026-Q3", C, "tracker"),
    Row("market.q3_2026_share.apple", 0.22, "share", "Apple's share of shipments, Q3 2026 (first Q3 above 20%)",
        "Counterpoint, 2026-10-12", "https://www.fonearena.com/blog/494790/global-smartphone-shipments-q3-2026-"
        "counterpoint.html", "2026-Q3", C, "tracker"),
    Row("market.q3_2026_xiaomi_change", -0.30, "share", "Xiaomi's shipments, Q3 2026 on a year earlier (\"more than "
        "30%\" down; share 10%)", "Counterpoint, 2026-10-12", "https://www.fonearena.com/blog/494790/global-"
        "smartphone-shipments-q3-2026-counterpoint.html", "2026-Q3", C, "tracker"),
    Row("market.retail_price_rise.2026", 0.20, "share", "Rise in smartphone retail prices so far in 2026",
        "Counterpoint, 2026-10-12", "https://www.fonearena.com/blog/494790/global-smartphone-shipments-q3-2026-"
        "counterpoint.html", "2026-01 to 2026-09", C, "tracker"),
    Row("india.share.2025", 0.25, "share", "Share of new iPhones assembled in India (about 55 million in 2025, "
        "36 million in 2024)", "Bloomberg, via GSMArena and Tech Wire Asia, 2026-03", "https://techwireasia.com/2026/"
        "03/apple-iphone-production-india-25-percent-global-output/", "2025", C, "press",
        note="Bloomberg's estimate; Counterpoint expects about 26% in 2026"),

    # --- suppliers and rivals: filings -------------------------------------------------------------------------------
    Row("micron.revenue.fy2026", 133.19, "USD bn", "Micron revenue, fiscal year to 3 September 2026",
        "Micron Form 10-K FY2026 (XBRL company facts)", EDGAR + "0000723125&type=10-K", "FY2026", C),
    Row("micron.gm.fy2026", 0.807, "share", "Micron gross margin FY2026 (gross profit 107.50 / revenue 133.19)",
        "Micron Form 10-K FY2026", EDGAR + "0000723125&type=10-K", "FY2026", C),
    Row("micron.revenue.fy2025", 37.38, "USD bn", "Micron revenue, FY2025", "Micron Form 10-K FY2025",
        EDGAR + "0000723125&type=10-K", "FY2025", C),
    Row("micron.gm.fy2025", 0.398, "share", "Micron gross margin FY2025 (14.87 / 37.38)", "Micron Form 10-K FY2025",
        EDGAR + "0000723125&type=10-K", "FY2025", C),
    Row("micron.gm.fy2023", -0.091, "share", "Micron gross margin FY2023 (a loss: -1.42 / 15.54)", "Micron Form 10-K "
        "FY2023", EDGAR + "0000723125&type=10-K", "FY2023", C),
    Row("skhynix.opm.q3_2026", 0.80, "share", "SK hynix operating margin, Q3 2026 (KRW 83.3tn on 104.6tn)",
        "SK hynix 3Q26 results, 2026-10-28 (preliminary), via the Korea Times and Herald", "https://www.koreatimes.co."
        "kr/business/companies/20261028/sk-hynix-logs-record-q3-operating-profit-of-628-bil", "2026-Q3", C, "press",
        note="Company release as reported; 79.7% before rounding"),
    Row("samsung.ds_op.q3_2026", 106.5, "KRW tn", "Samsung DS (chips) division operating profit, Q3 2026",
        "Samsung Electronics, Third Quarter 2026 Results, 2026-10-29", "https://news.samsung.com/global/samsung-"
        "electronics-announces-third-quarter-2026-results", "2026-Q3", C),
    Row("samsung.ds_rev.q3_2026", 147.1, "KRW tn", "Samsung DS division revenue, Q3 2026", "Samsung Electronics, "
        "2026-10-29", "https://news.samsung.com/global/samsung-electronics-announces-third-quarter-2026-results",
        "2026-Q3", C),
    Row("samsung.mx_op.q3_2026", -0.6, "KRW tn", "Samsung MX (mobile) and Networks operating profit, Q3 2026: a loss",
        "Samsung Electronics, 2026-10-29", "https://news.samsung.com/global/samsung-electronics-announces-third-"
        "quarter-2026-results", "2026-Q3", C),
    Row("samsung.mx_rev.q3_2026", 37.7, "KRW tn", "Samsung MX and Networks revenue, Q3 2026", "Samsung Electronics, "
        "2026-10-29", "https://news.samsung.com/global/samsung-electronics-announces-third-quarter-2026-results",
        "2026-Q3", C),
    Row("samsung.mx_op.q3_2025", 3.6, "KRW tn", "Samsung MX and Networks operating profit, Q3 2025", "Samsung "
        "Electronics, 2026-10-29 (comparison)", "https://news.samsung.com/global/samsung-electronics-announces-third-"
        "quarter-2026-results", "2025-Q3", C),
    Row("samsung.mx_opm.2025", 0.10, "share", "Samsung MX and Networks operating margin, 2025 (KRW 12.9tn on 129.5tn)",
        "Samsung Electronics, Fourth Quarter and FY 2025 Results, 2026-01-29", "https://news.samsung.com/global/"
        "samsung-electronics-announces-fourth-quarter-and-fy-2025-results", "2025", C),
    Row("tsmc.gm.q4_2025", 0.623, "share", "TSMC gross margin, Q4 2025", "TSMC, Reports Fourth Quarter EPS of "
        "NT$19.50, 2026-01-15", "https://pr.tsmc.com/english/news/3281", "2025-Q4", C),
    Row("tsmc.gm.q3_2026", 0.664, "share", "TSMC gross margin, Q3 2026 (revenue $46.72bn, up 41.2%)", "TSMC Form 6-K, "
        "3Q26 earnings release, 2026-10-15", "https://www.sec.gov/Archives/edgar/data/1046179/000104617926000726/"
        "a3q26e_withguidancexfinal.htm", "2026-Q3", C),
    Row("tsmc.smartphone_share.2025", 0.29, "share", "Smartphones' share of TSMC revenue, 2025 (HPC 58%)",
        "TSMC 4Q25 management report, via earnings coverage", "https://pr.tsmc.com/english/news/3281", "2025", C,
        "press", note="TSMC's platform split as reported in coverage of its 4Q25 call"),
    Row("tsmc.smartphone_share.q3_2026", 0.21, "share", "Smartphones' share of TSMC revenue, Q3 2026 (HPC 68%)",
        "TSMC 3Q26 management report, via coverage", "https://iphonewired.com/industry/1200143/", "2026-Q3", C, "press",
        note="Platform split as reported; smartphone revenue rose 10% on the quarter"),
    Row("qcom.handsets.fy2026", 24.072, "USD bn", "Qualcomm QCT handset revenue, fiscal year to 27 September 2026 "
        "(FY2025: 27.793)", "Qualcomm Form 10-K FY2026", "https://www.sec.gov/Archives/edgar/data/804328/"
        "000080432826000128/qcom-20260927.htm", "FY2026", C),
    Row("qcom.qct_ebt.fy2026", 0.27, "share", "Qualcomm QCT (chips) earnings before tax as a share of revenue, FY2026",
        "Qualcomm Form 10-K FY2026", "https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-"
        "20260927.htm", "FY2026", C),
    Row("qcom.qtl_ebt.fy2026", 0.72, "share", "Qualcomm QTL (patent licensing) EBT margin, FY2026; licensing revenue "
        "$5.556bn", "Qualcomm Form 10-K FY2026", "https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/"
        "qcom-20260927.htm", "FY2026", C),
    Row("foxconn.gm.2025", 0.0615, "share", "Hon Hai (Foxconn) gross margin, 2025 (revenue NT$8.1tn)",
        "Hon Hai, FY2025 results, as reported by I-Connect007", "https://iconnect007.com/article/149221/foxconn-"
        "reports-record-fy2025-revenue-strong-ai-growth-and-historic-dividend/149218/ein", "2025", C, "press",
        note="Company results as reported; operating margin 3.20%, net 2.34%"),
    Row("foxconn.opm.2025", 0.032, "share", "Hon Hai operating margin, 2025", "Hon Hai FY2025 results, as reported",
        "https://iconnect007.com/article/149221/foxconn-reports-record-fy2025-revenue-strong-ai-growth-and-historic-"
        "dividend/149218/ein", "2025", C, "press", note="Company results as reported"),
    Row("xiaomi.phone_rev.2025", 186.44, "CNY bn", "Xiaomi smartphone revenue, 2025 (down 2.8%)", "Xiaomi annual "
        "results announcement, HKEX, 2026-03-24", "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0324/"
        "2026032400608.pdf", "2025", C),
    Row("xiaomi.phone_units.2025", 165.2, "million", "Xiaomi smartphone shipments, 2025", "Xiaomi annual results, "
        "2026-03-24", "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0324/2026032400608.pdf", "2025", C),
    Row("xiaomi.phone_gm.2025", 0.109, "share", "Xiaomi smartphone gross margin, 2025 (12.6% in 2024; 8.3% in Q4 "
        "2025)", "Xiaomi annual results, 2026-03-24", "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0324/"
        "2026032400608.pdf", "2025", C),
    Row("transsion.revenue.2025", 65.6, "CNY bn", "Transsion revenue, 2025 (down 4.5%; net profit down 53% to "
        "CNY 2.58bn)", "Transsion 2025 annual report (Shanghai STAR Market), as summarised by Quartr and TechNode",
        "https://technode.com/2026/02/26/transsions-2025-profit-halves-market-value-falls-over-60/", "2025", C,
        "press", note="Company report as summarised; Transsion blamed the rise in memory prices"),
    Row("transsion.gm.2025", 0.193, "share", "Transsion gross margin, 2025 (down 2.1 points)", "Transsion 2025 annual "
        "report, via Quartr", "https://quartr.com/events/shenzhen-transsion-holdings-ltd-688036-q4-2025_Fgm8rDrN",
        "2025", C, "press", note="Company report as summarised by Quartr"),
    Row("transsion.units.2025", 106.9, "million", "Transsion smartphone shipments, 2025 (8.6% share)", "Industry "
        "tracker as reported by Jiemian, 2026", "https://en.jiemian.com/article/12402310.html", "2025", C, "press",
        lo=100, hi=110, note="The report does not name its tracker; treated as approximate"),
    Row("transsion.phone_rev_share", 0.84, "share", "Smartphones' share of Transsion's revenue (estimate)", "Third-party "
        "analysis; Transsion's report splits mobile phones from other products", "https://technode.com/2026/02/26/"
        "transsions-2025-profit-halves-market-value-falls-over-60/", "2025", C, "assumption", lo=0.78, hi=0.88),
    Row("sony.iss_opm.fy2025", 0.166, "share", "Sony Imaging & Sensing Solutions operating margin, fiscal year to "
        "March 2026 (JPY 357.3bn on 2,151.5bn)", "Sony Group FY2025 results, via Zacks and Digital Camera World",
        "https://www.sec.gov/Archives/edgar/data/0000313838/000110465926057456/tm2613222d2_6k.htm", "FY2025", C,
        "press", note="Sony's Form 6-K results as reported"),
    Row("corning.gm.2025", 0.360, "share", "Corning gross margin, 2025 (5.62 / 15.63)", "Corning Form 10-K 2025",
        EDGAR + "0000024741&type=10-K", "2025", C),
    Row("skyworks.gm.fy2026", 0.407, "share", "Skyworks gross margin, fiscal year to 2 October 2026 (1.61 / 3.96); "
        "operating margin 5.6%", "Skyworks Form 10-K FY2026", EDGAR + "0000004127&type=10-K", "FY2026", C),
    Row("broadcom.gm.fy2025", 0.678, "share", "Broadcom gross margin, fiscal year to 2 November 2025 "
        "(43.29 / 63.89)", "Broadcom Form 10-K FY2025", EDGAR + "0001730168&type=10-K", "FY2025", C),

    # --- exchange rates (FRED, annual averages) --------------------------------------------------------------------
    Row("fx.cny.2025", 7.188, "CNY per USD", "Average 2025", "FRED DEXCHUS", "https://fred.stlouisfed.org/series/"
        "DEXCHUS", "2025", C, "official"),
    Row("fx.krw.2025", 1421.4, "KRW per USD", "Average 2025", "FRED DEXKOUS", "https://fred.stlouisfed.org/series/"
        "DEXKOUS", "2025", C, "official"),
    Row("fx.krw.2026", 1448.4, "KRW per USD", "Average January-October 2026", "FRED DEXKOUS",
        "https://fred.stlouisfed.org/series/DEXKOUS", "2026", C, "official"),

    # --- the forecast that was wrong -----------------------------------------------------------------------------------
    Row("call.ballmer", 0, "quote", "\"There's no chance that the iPhone is going to get any significant market share. "
        "No chance. It's a $500 subsidized item.\" Steve Ballmer, Microsoft, USA Today CEO Forum, April 2007",
        "USA Today, 2007-04-29, as quoted by MacRumors 2007-04-30", "https://www.macrumors.com/2007/04/30/ballmer-on-"
        "iphone-marketshare/", "2007-04", C, "press", note="USA Today's original page is no longer online"),

    # --- this series' own assumptions --------------------------------------------------------------------------------
    Row("assume.channel_margin", 0.10, "share", "Average margin a carrier or reseller keeps on an iPhone it sells. "
        "Carriers often sell near cost to win a contract; the range spans that and a retailer's margin",
        "This series' assumption; Linden et al. (2007) used 25% (10% distribution + 15% retail) for the iPod", IPOD,
        "2025", C, "assumption", lo=0.03, hi=0.15),
    Row("assume.assembly", 30, "USD", "Assembly, test and inbound logistics per premium iPhone", "This series' "
        "assumption, bracketing teardown houses' published assembly estimates", "", "2025", C, "assumption",
        lo=20, hi=45),
    Row("assume.other_cogs", 40, "USD", "Other cost of sales per iPhone: warranty, freight to market, licences and "
        "royalties", "This series' assumption", "", "2025", C, "assumption", lo=25, hi=60),
)

add(
    Row("qcom.handsets.fy2025", 27.793, "USD bn", "Qualcomm QCT handset revenue, FY2025", "Qualcomm Form 10-K FY2026",
        "https://www.sec.gov/Archives/edgar/data/804328/000080432826000128/qcom-20260927.htm", "FY2025", C),
    Row("qcom.handsets_reason.fy2026", 0, "quote", "Qualcomm: lower handset revenue in FY2026 was \"primarily due to "
        "lower chipset shipments to certain major OEMs (primarily driven by customers adjusting build plans to reduce "
        "their inventory levels as a result of the negative effects of recent memory supply constraints and related "
        "price increases)\"", "Qualcomm Form 10-K FY2026, MD&A", "https://www.sec.gov/Archives/edgar/data/804328/"
        "000080432826000128/qcom-20260927.htm", "FY2026", C),
    Row("qcom.risk_vertical", 0, "quote", "Qualcomm risk factor: \"Our business, particularly our semiconductor "
        "business, may suffer as a result of our customers vertically integrating (i.e., developing their own "
        "integrated circuit products).\"", "Qualcomm Form 10-K FY2026, Item 1A", "https://www.sec.gov/Archives/edgar/"
        "data/804328/000080432826000128/qcom-20260927.htm", "FY2026", C),
    Row("apple.own_chips", 0, "event", "Apple's own chips replacing bought ones: the A4 processor (2010), the C1 modem "
        "(iPhone 16e, February 2025), the N1 wireless chip (iPhone 17 line, September 2025)", "Apple Newsroom "
        "releases of those dates", "https://www.apple.com/newsroom/", "2010-2025", C, "filing"),
    Row("skyworks.rev.fy2023", 4.77, "USD bn", "Skyworks revenue FY2023 (operating margin 23.5%: 1.12 / 4.77)",
        "Skyworks Form 10-K FY2023", EDGAR + "0000004127&type=10-K", "FY2023", C),
    Row("skyworks.opm.fy2026", 0.056, "share", "Skyworks operating margin FY2026 (0.22 / 3.96)", "Skyworks Form 10-K "
        "FY2026", EDGAR + "0000004127&type=10-K", "FY2026", C),
    Row("apple.rd.fy2026", 45.765, "USD bn", "Apple research and development expense, FY2026", "Apple Form 10-K "
        "FY2026", APPLE_10K_26, "FY2026", C),
    Row("transsion.africa_share.2025", 0.48, "share", "Transsion's share of smartphone shipments in Africa, 2025 "
        "(40.5 million phones)", "Omdia, via TelecomLead, 2026-02", "https://telecomlead.com/smart-phone/africa-"
        "smartphone-market-grows-13-in-2025-to-84-4-mn-omdia-forecasts-23-decline-in-2026-124751", "2025", C,
        "tracker"),
)

add(
    Row("micron.revenue.fy2023", 15.54, "USD bn", "Micron revenue, FY2023", "Micron Form 10-K FY2023",
        EDGAR + "0000723125&type=10-K", "FY2023", C),
)

add(
    Row("share.apple.op_profit.q2_2023", 0.85, "share", "Apple's share of global smartphone operating profit, Q2 2023 "
        "(a June-quarter record; the industry's operating profit was under $13bn that quarter)", "Counterpoint "
        "Research, 2023", "https://counterpointresearch.com/en/insights/apples-smartphone-revenue-operating-profit-"
        "hit-june-quarter-records-q2-2023", "2023-Q2", C, "tracker"),
    Row("share.apple.revenue.q2_2026", 0.49, "share", "Apple's share of global smartphone revenue, Q2 2026 (a record)",
        "Counterpoint Research, via 9to5Mac 2026-07-31", "https://9to5mac.com/2026/07/31/report-apple-hit-a-record-49-"
        "share-of-global-smartphone-revenue-for-q2/", "2026-Q2", C, "tracker"),
)

TMUS_10K = "https://www.sec.gov/Archives/edgar/data/1283699/000128369926000010/tmus-20251231.htm"
ATT_10K = "https://www.sec.gov/Archives/edgar/data/732717/000073271726000120/t-20251231.htm"
add(
    # --- the carriers (chapter 6) -----------------------------------------------------------------------------------
    Row("tmus.equipment_rev.2025", 15.972, "USD bn", "T-Mobile US equipment revenues, 2025", "T-Mobile US Form 10-K "
        "2025, consolidated statement of operations", TMUS_10K, "2025", C),
    Row("tmus.equipment_cost.2025", 21.277, "USD bn", "T-Mobile US cost of equipment sales, 2025", "T-Mobile US Form "
        "10-K 2025", TMUS_10K, "2025", C),
    Row("tmus.service_rev.2025", 71.306, "USD bn", "T-Mobile US total service revenues, 2025", "T-Mobile US Form 10-K "
        "2025", TMUS_10K, "2025", C),
    Row("tmus.service_cost.2025", 11.497, "USD bn", "T-Mobile US cost of services (excluding depreciation), 2025",
        "T-Mobile US Form 10-K 2025", TMUS_10K, "2025", C),
    Row("att.equipment_rev.2025", 24.490, "USD bn", "AT&T equipment revenues, 2025 (service revenues $101.158bn)",
        "AT&T Form 10-K 2025", ATT_10K, "2025", C),
    # --- after the sale (chapter 8) ----------------------------------------------------------------------------------
    Row("apple.installed_base.2026", 2.5, "billion devices", "Apple's installed base of active devices, \"more than "
        "2.5 billion\", announced with its results for the quarter to December 2025", "Apple Newsroom, Apple reports "
        "first quarter results, 2026-01-29", "https://www.apple.com/newsroom/2026/01/apple-reports-first-quarter-"
        "results/", "2026-01", C),
    Row("google.pays_apple.2022", 20, "USD bn", "Google's estimated payment to Apple in 2022 to be Safari's default "
        "search engine (about double 2020's)", "United States v. Google LLC, memorandum opinion, D.D.C., 2024-08-05, "
        "as reported by NPR", "https://www.npr.org/2024/08/05/nx-s1-5064624/google-justice-department-antitrust-"
        "search", "2022", C, "official"),
    Row("apple.app_store_commission", 0.30, "share", "Apple's standard App Store commission on digital goods (15% for "
        "small developers and for subscriptions after their first year)", "Apple, App Store Review Guidelines and "
        "Small Business Program", "https://developer.apple.com/app-store/small-business-program/", "2026", C),
    # --- memory's boom and bust (chapter 11) --------------------------------------------------------------------------
    Row("micron.gm.history", 0, "share", "Micron gross margin by fiscal year (to late August or early September): "
        "2016 20.2%, 2017 41.5%, 2018 58.9%, 2019 45.7%, 2020 30.6%, 2021 37.6%, 2022 45.2%, 2023 -9.1%, 2024 22.4%, "
        "2025 39.8%, 2026 80.7%; revenue $12.4bn, 20.3, 30.4, 23.4, 21.4, 27.7, 30.8, 15.5, 25.1, 37.4, 133.2",
        "Micron Forms 10-K, FY2016-FY2026 (XBRL company facts: revenue, gross profit or cost of goods sold)",
        EDGAR + "0000723125&type=10-K", "FY2016-FY2026", C),
)

add(
    Row("apple.gross_profit.fy2026", 233.602, "USD bn", "Apple total gross margin (gross profit), FY2026; services "
        "$93.943bn of it", "Apple Form 10-K FY2026", APPLE_10K_26, "FY2026", C),
)
