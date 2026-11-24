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
    # --- Visa, fiscal year to 30 September 2026 ----------------------------------------------------------------------
    r("visa.rev", 45.90, "USD bn", "Visa net revenue, fiscal 2026 (2025: $40.00bn)", "Visa Form 10-K FY2026 (SEC "
      "company facts: RevenueFromContractWithCustomerExcludingAssessedTax)", CF.format(1403161), "FY2026"),
    r("visa.oi", 28.11, "USD bn", "Visa operating income, fiscal 2026 (2025: $23.99bn)", "Visa Form 10-K FY2026 (SEC "
      "company facts: OperatingIncomeLoss)", CF.format(1403161), "FY2026"),
    # --- moats that drained ---------------------------------------------------------------------------------------------
    r("news.ads.2005", 49.4, "USD bn", "US newspaper industry's estimated advertising revenue, 2005 (circulation "
      "$10.7bn)", "Pew Research Center, 'Estimated advertising and circulation revenue of the newspaper industry' "
      "(News Media Alliance through 2012)", "https://www.pewresearch.org/journalism/chart/sotnm-newspapers-newspaper-"
      "industry-estimated-advertising-and-circulation-revenue/", "2005", kind="tracker"),
    r("kodak.sales.2008", 9.42, "USD bn", "Eastman Kodak net sales, 2008 (2011: $6.02bn; 2017: $1.53bn)", "Eastman "
      "Kodak Forms 10-K (SEC company facts: SalesRevenueNet)", CF.format(31235), "2008"),
    r("kodak.sales.2017", 1.53, "USD bn", "Eastman Kodak net sales, 2017, after its chapter 11 reorganization",
      "Eastman Kodak Form 10-K 2017 (SEC company facts)", CF.format(31235), "2017"),
)
