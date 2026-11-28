"""Register rows for Part 33, *The Middlemen*.  Checked 2026-11-28.

The Forms 10-K of McKesson (fiscal 2026, to 31 March 2026), Cencora (fiscal 2026, to 30 September 2026), Cardinal Health
(fiscal 2026, to 30 June 2026), Sysco (fiscal 2026, to 27 June 2026), US Foods, W.W. Grainger and Bunge (2025); Mitsui &
Co.'s consolidated results for the years to March 2026 and the half-year to September 2026 (Tokyo Stock Exchange filings);
Chemdex's prospectus of July 1999 and Ventro's 10-K for 2000.  Series are the Filing Room's SEC and FRED extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-28"
P = (33,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
MCK = SEC + "927653/000092765326000069/mck-20260331.htm"
COR = SEC + "1140859/000114085926000044/cor-20260930.htm"
CAH = SEC + "721371/000072137126000038/cah-20260630.htm"
SYY = SEC + "96021/000009602126000033/syy-20260627.htm"
USFD = SEC + "1665918/000166591826000008/usfd-20251227.htm"
GWW = SEC + "277135/000027713526000011/gww-20251231.htm"
BG = SEC + "1996862/000162828026009842/bg-20251231.htm"
CHEMDEX = SEC + "1047499/0001012870-99-002531.txt"
VENTRO = SEC + "1047499/000109581101001551/f69503e10-k.txt"
MITSUI = "https://www.mitsui.com/jp/en/ir/library/meeting/pdf/en_263_4q_ta.pdf"
MITSUI_H1 = "https://www.mitsui.com/jp/en/ir/library/meeting/pdf/en_273_2q_ta.pdf"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def mck(key, value, unit, definition, fact="FY2026 (to 2026-03-31)"):
    return r(key, value, unit, definition, "McKesson, Form 10-K for fiscal 2026", MCK, fact)


def cor(key, value, unit, definition, fact="FY2026 (to 2026-09-30)"):
    return r(key, value, unit, definition, "Cencora, Form 10-K for fiscal 2026", COR, fact)


def cah(key, value, unit, definition, fact="FY2026 (to 2026-06-30)"):
    return r(key, value, unit, definition, "Cardinal Health, Form 10-K for fiscal 2026", CAH, fact)


def gww(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "W.W. Grainger, Form 10-K for 2025", GWW, fact)


def mi(key, value, unit, definition, fact="FY March 2026"):
    return r(key, value, unit, definition, "Mitsui & Co., consolidated financial results for the year ended 31 March 2026 (IFRS), "
             "1 May 2026", MITSUI, fact)


def wk(key, value, unit, definition, lo, hi):
    return r(key, value, unit, definition, "this series' assumption", "", "", kind="assumption", lo=lo, hi=hi)


add(
    # The drug wholesalers
    mck("mk33.cvs", 24, "percent", "sales to its largest customer, CVS Health, as a share of revenue, fiscal 2026; the next two 11% and 10%"),
    mck("mk33.top10", 73, "percent", "sales to its ten largest customers, including group purchasing organizations, as a share of revenue"),
    mck("mk33.next2", 21, "percent", "sales to its second and third largest customers, 11% and 10% of revenue"),
    mck("mk33.cvs.ar", 21, "percent", "CVS's share of McKesson's trade accounts receivable at 31 March 2026; the ten largest customers about 43%", "2026-03-31"),
    mck("mk33.dcs", 27, "distribution centers", "U.S. Pharmaceutical distribution centers, including two strategic redistribution centers"),
    mck("mk33.emp", 43400, "people", "approximately 38,000 employees in the U.S., 5,000 in Canada and 400 in the rest of the world"),
    mck("mk33.opioid", 5.7, "US$ billion", "'estimated litigation liability of $5.7 billion as of March 31, 2026 payable under the terms of various "
        "settlement agreements for opioid-related claims'", "2026-03-31"),
    cor("co33.wag", 23, "percent", "Walgreens' share of revenue, fiscal 2026 (and about 33% of accounts receivable); Evernorth Health Services 11%"),
    cor("co33.evernorth", 11, "percent", "Evernorth Health Services' share of revenue, fiscal 2026"),
    cor("co33.top5", 43, "percent", "the top five customers, including governmental agencies, as a share of revenue"),
    cor("co33.supp", 36, "percent", "the five largest suppliers' share of purchases, fiscal 2026"),
    cor("co33.glp1", 8.0, "US$ billion", "'Sales of products labeled for diabetes and/or weight loss in the GLP-1 class increased $8.0 billion, or "
        "22.2%, from the prior fiscal year'"),
    cah("ca33.glp1", 1, "flag", "'With respect to GLP-1 medications, during fiscal 2026, we experienced increased demand ... however, increased "
        "GLP-1 sales did not meaningfully contribute to segment profit'"),
    cah("ca33.nosa", 374, "US$ million", "'In July 2026, we made our sixth annual payment of $374 million under the National Opioid Settlement "
        "Agreement', which became effective on 2 April 2022 ($366m the year before)", "2026-07"),
    cah("ca33.redoak", 1, "flag", "the Red Oak Sourcing, LLC venture with CVS Health, which sources generic pharmaceuticals"),

    # Food service
    r("sy33.dcs", 333, "distribution facilities", "'As of June 27, 2026, we operated 333 distribution facilities' in North America and Europe; "
      "'Our operating sites offer daily delivery to certain customer locations'", "Sysco, Form 10-K for fiscal 2026", SYY, "2026-06-27"),
    r("sy33.brand", 35.4, "percent", "Sysco brand penetration for U.S. Broadline, fiscal 2026 (45.8% for local customers)",
      "Sysco, Form 10-K for fiscal 2026", SYY, "FY2026"),
    r("sy33.brand.local", 45.8, "percent", "Sysco brand penetration for U.S. Broadline local customers, fiscal 2026",
      "Sysco, Form 10-K for fiscal 2026", SYY, "FY2026"),
    r("us33.cust", 250000, "customer locations", "'We supply approximately 250,000 customer locations nationwide'; 'over 70 distribution "
      "facilities and fleet of over 6,500 trucks, along with over 90 cash and carry locations'", "US Foods, Form 10-K for 2025", USFD, "2025"),
    r("us33.trucks", 6500, "trucks", "a fleet of over 6,500 trucks", "US Foods, Form 10-K for 2025", USFD, "2025"),
    r("us33.dcs", 70, "distribution facilities", "over 70 distribution facilities", "US Foods, Form 10-K for 2025", USFD, "2025"),

    # Industrial supply
    gww("gw33.ht.sales", 13.993, "US$ billion", "High-Touch Solutions N.A. net sales, 2025 ($13,720m in 2024; gross profit $5,832m, operating earnings $2,354m)"),
    gww("gw33.ht.gp", 5.832, "US$ billion", "High-Touch Solutions N.A. gross profit, 2025"),
    gww("gw33.ht.op", 2.354, "US$ billion", "High-Touch Solutions N.A. operating earnings, 2025"),
    gww("gw33.ea.sales", 3.625, "US$ billion", "Endless Assortment (Zoro and MonotaRO) net sales, 2025 ($3,134m in 2024; cost of goods $2,540m, operating earnings $345m)"),
    gww("gw33.ea.cogs", 2.540, "US$ billion", "Endless Assortment cost of goods sold, 2025"),
    gww("gw33.ea.op", 0.345, "US$ billion", "Endless Assortment segment operating earnings, 2025"),
    gww("gw33.cust", 4.6, "million", "'more than 4.6 million customers worldwide'"),
    gww("gw33.stocked", 1.5, "million", "'more than 1.5 million products stocked in Distribution Centers (DCs) and branches globally'"),
    gww("gw33.zoro", 13, "million", "products offered by Zoro (MonotaRO about 29 million; the high-touch businesses about 2 million)"),
    gww("gw33.monotaro", 29, "million", "products offered through MonotaRO"),

    # Traders
    r("bg33.what", 1, "flag", "'We are a premier agribusiness solutions company, connecting farmers to consumers ... as we partner with farmers "
      "to move crops from where they are grown to where they are needed'", "Bunge Global, Form 10-K for 2025", BG, "2025"),
    mi("mi33.rev", 13995.2, "JPY billion", "revenue, year to March 2026 (14,662.6 a year before)"),
    mi("mi33.gp", 1328.2, "JPY billion", "gross profit, year to March 2026"),
    mi("mi33.equity", 447.4, "JPY billion", "share of profit of investments accounted for using the equity method, year to March 2026"),
    mi("mi33.div", 178.7, "JPY billion", "dividend income, year to March 2026"),
    mi("mi33.profit", 834.0, "JPY billion", "profit for the year attributable to owners of the parent, year to March 2026 (900.3 a year before)"),
    mi("mi33.fx", 151.09, "JPY per US$", "average exchange rate, year to March 2026, as stated among the forecast assumptions"),
    mi("mi33.cf.mm", 330.4, "JPY billion", "core operating cash flow, Mineral & Metal Resources"),
    mi("mi33.cf.en", 262.0, "JPY billion", "core operating cash flow, Energy"),
    mi("mi33.cf.en.prev", 363.4, "JPY billion", "core operating cash flow, Energy, year to March 2025", "FY March 2025"),
    mi("mi33.cf.mi", 184.1, "JPY billion", "core operating cash flow, Machinery & Infrastructure"),
    mi("mi33.cf.ch", 102.6, "JPY billion", "core operating cash flow, Chemicals"),
    mi("mi33.cf.is", 17.9, "JPY billion", "core operating cash flow, Iron & Steel Products"),
    mi("mi33.cf.li", 7.8, "JPY billion", "core operating cash flow, Lifestyle"),
    mi("mi33.cf.ic", 46.4, "JPY billion", "core operating cash flow, Innovation & Corporate Development"),
    mi("mi33.cf.total", 978.9, "JPY billion", "core operating cash flow, consolidated"),
    mi("mi33.fc.may", 920.0, "JPY billion", "forecast of profit attributable to owners of the parent for the year to March 2027, May 2026", "2026-05-01"),
    r("mi33.fc", 1050.0, "JPY billion", "revised forecast of profit attributable to owners of the parent for the year to March 2027, announced "
      "November 2026 (920.0 in May)", "Mitsui & Co., consolidated financial results for the six months to 30 September 2026, 4 November 2026",
      MITSUI_H1, "2026-11-04"),
    r("mi33.h1", 574.9, "JPY billion", "profit attributable to owners of the parent, six months to 30 September 2026 (423.7 a year before)",
      "Mitsui & Co., consolidated financial results for the six months to 30 September 2026, 4 November 2026", MITSUI_H1, "2026-09-30"),

    # Chemdex
    r("cd33.claim", 1, "flag", "'The life sciences research products industry is particularly well suited for business-to-business e-commerce "
      "because of its high degree of fragmentation and because of the inefficiencies inherent in its traditional paper-based purchasing "
      "process'; 'the Chemdex Marketplace will appeal to suppliers as being less costly than traditional distribution'",
      "Chemdex, prospectus (Form 424B4), July 1999", CHEMDEX, "1999-07"),
    r("cd33.margin", 1, "flag", "'Our gross margins on sales of life sciences research products are small relative to the margins earned by "
      "traditional distributors of life sciences research products'", "Chemdex, prospectus (Form 424B4), July 1999", CHEMDEX, "1999-07"),
    r("cd33.q2rev", 2.8, "US$ million", "'revenues for the three months ended June 30, 1999 are approximately $2.8 million'",
      "Chemdex, prospectus (Form 424B4), July 1999", CHEMDEX, "1999-06-30"),
    r("cd33.shut", 1, "flag", "'In December 2000 the Board of Directors concluded that the Chemdex Marketplace would be discontinued. This "
      "decision was based, in part, upon an analysis of operating expenses required to support the marketplace, revenue and gross margin "
      "growth below expectations, and expectations of the need to continue investing significant cash'", "Ventro, Form 10-K for 2000",
      VENTRO, "2000-12"),
    r("cd33.loss", 93.5, "US$ million", "'the net loss from continuing operations was $93.5 million in 2000'", "Ventro, Form 10-K for 2000",
      VENTRO, "2000"),

    # The Works
    wk("wk33.sales", 5000.0, "US$ million a year", "a regional distributor's sales when every order is filled", 2000.0, 10000.0),
    wk("wk33.lead", 14.0, "days", "time from ordering to receiving from the maker", 7.0, 21.0),
    wk("wk33.review", 14.0, "days", "time between orders to the maker", 7.0, 21.0),
    wk("wk33.cv", 1.0, "ratio", "variability of a line's daily demand (standard deviation over mean)", 0.5, 1.5),
    wk("wk33.loss", 0.02, "share per point", "sales lost for each point of fill rate below 99%", 0.01, 0.04),
    wk("wk33.wacc", 0.08, "share a year", "the cost of capital", 0.06, 0.10),
    wk("wk33.dropkeep", 0.55, "share", "sales kept when customers must wait for drop-shipped orders", 0.4, 0.8),
    wk("wk33.dropgm", 0.02, "share of sales", "the margin for passing an order on without holding the stock", 0.01, 0.03),
    wk("wk33.route", 900.0, "US$ a day", "a delivery truck and driver for a day", 700.0, 1200.0),
    wk("wk33.drop", 5000.0, "US$", "goods delivered at a pharmacy stop", 2000.0, 10000.0),
    wk("wk33.density", 1.0, "per square mile", "customers of one kind per square mile in a town", 0.3, 3.0),
)
