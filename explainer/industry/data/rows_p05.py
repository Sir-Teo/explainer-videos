"""Register rows for Part 5, *The Moat*.  Checked 2026-11-24.

Berkshire Hathaway's 2007 letter for the three businesses the part opens with; McGahan and Porter's decomposition of
profitability; Visa's accounts; the moats that drained (newspapers, Kodak).  The returns on capital by industry are the
Filing Room's ``damodaran_roc.csv`` and the concentration ratios its ``census_conc_2022.csv``.
"""

from explainer.industry.register import Row, add

C = "2026-11-24"
P = (5,)
BRK07 = "https://www.berkshirehathaway.com/letters/2007ltr.pdf"
CF = "https://data.sec.gov/api/xbrl/companyfacts/CIK{:010d}.json"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def brk(key, value, unit, definition, fact="2007"):
    return r(key, value, unit, definition, "Berkshire Hathaway, letter to shareholders for 2007 (February 2008), "
             "pp. 6-8", BRK07, fact, kind="filing")


add(
    # --- Berkshire Hathaway's three businesses (2007 letter) ----------------------------------------------------------
    brk("brk.moat", 0, "quote", "\"A truly great business must have an enduring 'moat' that protects excellent returns "
        "on invested capital. The dynamics of capitalism guarantee that competitors will repeatedly assault any "
        "business 'castle' that is earning high returns.\""),
    brk("sees.price", 25, "USD m", "price Blue Chip Stamps paid for See's Candies in 1972 (sales then $30m, pre-tax "
        "earnings under $5m, capital required $8m)", "1972"),
    brk("sees.capital.1972", 8, "USD m", "capital required to run See's in 1972", "1972"),
    brk("sees.pretax.1972", 5, "USD m", "See's pre-tax earnings in 1972 ('less than $5 million')", "1972"),
    brk("sees.sales.2007", 383, "USD m", "See's sales in 2007 (31 million pounds of candy, against 16 million in "
        "1972: 2% growth a year)"),
    brk("sees.pretax.2007", 82, "USD m", "See's pre-tax profit in 2007"),
    brk("sees.capital.2007", 40, "USD m", "capital required to run See's in 2007: $32m reinvested since 1972"),
    brk("sees.total", 1350, "USD m", "See's pre-tax earnings, 1972-2007 in total; all but $32m sent to Berkshire",
        "1972-2007"),
    brk("fsi.pretax.1996", 111, "USD m", "FlightSafety's pre-tax operating earnings when Berkshire bought it in 1996 "
        "(net fixed assets $570m)", "1996"),
    brk("fsi.assets.1996", 570, "USD m", "FlightSafety's net investment in fixed assets in 1996, when Berkshire bought "
        "it", "1996"),
    brk("fsi.extra", 509, "USD m", "FlightSafety's extra net investment in fixed assets, 1996-2007 (to $1,079m)",
        "1996-2007"),
    brk("fsi.capex", 1635, "USD m", "FlightSafety's capital spending, 1996-2007, mostly flight simulators (each can "
        "cost more than $12m; 273 of them); depreciation $923m", "1996-2007"),
    brk("fsi.pretax.2007", 270, "USD m", "FlightSafety's pre-tax operating earnings in 2007: $159m more than in 1996 on "
        "$509m of extra investment"),
    brk("brk.airlines", 0, "quote", "\"The worst sort of business is one that grows rapidly, requires significant "
        "capital to engender the growth, and then earns little or no money. Think airlines. ... if a farsighted "
        "capitalist had been present at Kitty Hawk, he would have done his successors a huge favor by shooting Orville "
        "down.\""),
    # --- how much does the industry matter --------------------------------------------------------------------------
    r("mp.industry", 0.19, "share", "McGahan and Porter (1997): share of the variance in business units' profitability "
      "explained by their industry (year 2%, corporate parent 4%, business-specific 32%; the rest unexplained); US "
      "public corporations, 1981-1994", "McGahan and Porter, 'How much does industry matter, really?', Strategic "
      "Management Journal 18(S1):15-30 (1997), abstract", "https://ideas.repec.org/a/bla/stratm/v18y1997is1p15-30.html",
      "1981-1994", kind="study"),
    r("mp.business", 0.32, "share", "McGahan and Porter (1997): share of the variance explained by the business unit "
      "itself", "McGahan and Porter (1997), abstract", "https://ideas.repec.org/a/bla/stratm/v18y1997is1p15-30.html",
      "1981-1994", kind="study"),
    r("mp.parent", 0.04, "share", "McGahan and Porter (1997): share explained by the corporate parent",
      "McGahan and Porter (1997), abstract", "https://ideas.repec.org/a/bla/stratm/v18y1997is1p15-30.html",
      "1981-1994", kind="study"),
    r("mp.year", 0.02, "share", "McGahan and Porter (1997): share explained by the year",
      "McGahan and Porter (1997), abstract", "https://ideas.repec.org/a/bla/stratm/v18y1997is1p15-30.html",
      "1981-1994", kind="study"),
    r("porter.1979", 1979, "year", "Michael E. Porter, 'How Competitive Forces Shape Strategy', Harvard Business Review "
      "57(2), March-April 1979: rivalry, the threat of new entrants, the threat of substitutes, and the bargaining "
      "power of buyers and of suppliers", "Harvard Business Review, March 1979", "https://hbr.org/1979/03/how-"
      "competitive-forces-shape-strategy", "1979-03", kind="study"),
    r("hhi.2023", 1800, "HHI", "US merger guidelines (2023), Guideline 1: markets with an HHI greater than 1,800 are "
      "highly concentrated, and a change of more than 100 points is a significant increase; a merger that creates "
      "or further consolidates a highly concentrated market with such an increase is presumed to lessen competition "
      "(the 2010 guidelines used 2,500)", "US Department of Justice and Federal Trade Commission, Merger Guidelines "
      "(18 December 2023), Guideline 1", "https://www.justice.gov/atr/merger-guidelines/applying-merger-guidelines/"
      "guideline-1", "2023-12", kind="official"),
    r("smoke.1965", 0.42, "share", "share of US adults who smoked cigarettes in 1965 (the first year of the national "
      "series)", "CDC press release, 'U.S. Adult Tobacco Product Use Decreased from 2019 to 2020', 18 March 2022",
      "https://archive.cdc.gov/www_cdc_gov/media/releases/2022/p0318-US-tobacco-use.html", "1965", kind="official"),
    r("smoke.2022", 0.116, "share", "share of US adults who currently smoked cigarettes in 2022 (about 28.8 million "
      "people; National Health Interview Survey)", "CDC, MMWR 73(29), 'Adult Smoking Cessation - United States, "
      "2022' (2024)", "https://www.cdc.gov/mmwr/volumes/73/wr/mm7329a1.htm", "2022", kind="official"),
    # --- Visa, fiscal year to 30 September 2026 ----------------------------------------------------------------------
    r("visa.rev", 45.90, "USD bn", "Visa net revenue, fiscal 2026 (2025: $40.00bn)", "Visa Form 10-K FY2026 (SEC "
      "company facts: RevenueFromContractWithCustomerExcludingAssessedTax)", CF.format(1403161), "FY2026"),
    r("visa.oi", 28.11, "USD bn", "Visa operating income, fiscal 2026 (2025: $23.99bn)", "Visa Form 10-K FY2026 (SEC "
      "company facts: OperatingIncomeLoss)", CF.format(1403161), "FY2026"),
    r("law.patent", 20, "years", "term of a US utility patent: 20 years from the date the application was filed "
      "(35 U.S.C. 154(a)(2))", "United States Code, title 35, section 154", "https://www.law.cornell.edu/uscode/text/"
      "35/154", "current", kind="official"),
    # --- moats that drained ---------------------------------------------------------------------------------------------
    r("news.ads.2005", 49.4, "USD bn", "US newspaper industry's estimated advertising revenue, 2005 (circulation "
      "$10.7bn)", "Pew Research Center, 'Estimated advertising and circulation revenue of the newspaper industry' "
      "(News Media Alliance through 2012)", "https://www.pewresearch.org/journalism/chart/sotnm-newspapers-newspaper-"
      "industry-estimated-advertising-and-circulation-revenue/", "2005", kind="tracker"),
    r("news.ads.2020", 9.60, "USD bn", "US newspaper industry's estimated advertising revenue, 2020 ($9,601m; "
      "circulation $11,054m, now the larger; 2008: advertising $37.8bn; 2010: $25.8bn)", "Pew Research Center, "
      "'Estimated advertising and circulation revenue of the newspaper industry', 29 June 2021 (Pew's estimates from "
      "SEC filings for 2013-2020)", "https://www.pewresearch.org/journalism/chart/sotnm-newspapers-newspaper-industry-"
      "estimated-advertising-and-circulation-revenue/", "2020", kind="tracker", note="Pew's estimate from the filings "
      "of publicly traded newspaper companies"),
    r("news.circ.2020", 11.05, "USD bn", "US newspaper industry's estimated circulation revenue, 2020 (2005: $10.7bn)",
      "Pew Research Center, 29 June 2021", "https://www.pewresearch.org/journalism/chart/sotnm-newspapers-newspaper-"
      "industry-estimated-advertising-and-circulation-revenue/", "2020", kind="tracker", note="Pew's estimate"),
    r("kodak.sales.2008", 9.42, "USD bn", "Eastman Kodak net sales, 2008 (2011: $6.02bn; 2017: $1.53bn)", "Eastman "
      "Kodak Forms 10-K (SEC company facts: SalesRevenueNet)", CF.format(31235), "2008"),
    r("kodak.ch11", 2012, "year", "Eastman Kodak and its US subsidiaries filed for chapter 11 on 19 January 2012 "
      "(Southern District of New York, case 12-10202)", "Eastman Kodak Form 8-K, 19 January 2012, Item 1.03",
      "https://www.sec.gov/Archives/edgar/data/31235/000119312512016443/d285282d8k.htm", "2012-01-19"),
    r("kodak.sales.2017", 1.53, "USD bn", "Eastman Kodak net sales, 2017, after its chapter 11 reorganization",
      "Eastman Kodak Form 10-K 2017 (SEC company facts)", CF.format(31235), "2017"),
)
