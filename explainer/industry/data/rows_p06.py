"""Register rows for Part 6, *The Cycle*.  Checked 2026-11-24.

UNCTAD's Review of Maritime Transport for the ships on order against the fleet; Intel's 2021 announcement for the
part's dated call of a peak; Ezekiel's paper for the cobweb.  Company accounts are the Filing Room's ``sec_annual.csv``,
``sec_quarterly.csv`` (Micron, Intel, Exxon, D.R. Horton) and ``esef_maersk.csv`` (Maersk); hogs, housing, oil and
orders are ``fred_cycle.csv``.
"""

from explainer.industry.register import Row, add

C = "2026-11-24"
P = (6,)
RMT24 = "https://unctad.org/system/files/official-document/rmt2024ch2_en.pdf"
RMT25 = "https://unctad.org/system/files/official-document/rmt2025ch2_en.pdf"


def r(key, value, unit, definition, source, url, fact, kind="official", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def unctad25(key, value, definition, fact):
    return r(key, value, "share", definition, "UNCTAD, Review of Maritime Transport 2025, chapter II, p. 56 (figure "
             "II.9 and text; UNCTAD's calculations from Clarksons Research)", RMT25, fact,
             note="orderbook as a share of the active fleet's gross tonnage, at the start of the year")


add(
    # --- ships on order against the fleet ----------------------------------------------------------------------------
    unctad25("ships.book.2009", 0.52, "world ships on order as a share of the active fleet, 2009", "2009"),
    unctad25("ships.book.2014", 0.19, "world ships on order as a share of the active fleet, 2014 and 2015", "2014"),
    unctad25("ships.book.2023", 0.111, "world ships on order as a share of the active fleet, start of 2023", "2023"),
    unctad25("ships.book.2024", 0.123, "world ships on order as a share of the active fleet, start of 2024", "2024"),
    unctad25("ships.book.2025", 0.15, "world ships on order as a share of the active fleet, early 2025", "2025"),
    unctad25("ships.book.lng.2025", 0.513, "LNG carriers on order as a share of the LNG fleet (cubic metres), early 2025",
             "2025"),
    unctad25("ships.book.box.2025", 0.246, "container ships on order as a share of the container fleet (TEU), "
             "early 2025 (LNG carriers: 51.3%)", "2025"),
    r("ships.book.bulk.2009", 0.78, "share", "dry bulk carriers on order as a share of the bulk fleet's deadweight "
      "tonnage in the 2009 downturn (2022: 8.3%; first quarter of 2024: 9.7%)", "UNCTAD, Review of Maritime "
      "Transport 2024, chapter II, p. 38 (UNCTAD's calculations from Clarksons Research)", RMT24, "2009"),
    r("ships.delivered.box.2024", 0.413, "share", "container ships' share of all gross tonnage delivered in 2024 "
      "(71.7 million gross tons delivered in all; bulkers 26.6%)", "UNCTAD, Review of Maritime Transport 2025, "
      "chapter II, p. 57", RMT25, "2024"),
    # --- Intel's 2021 announcement ------------------------------------------------------------------------------------
    r("intel.az.2021", 20, "USD bn", "Intel's announced investment in two new chip factories in Arizona, 23 March 2021 "
      "('IDM 2.0'): 'an estimated $20 billion'", "Intel, press release 'Intel CEO Pat Gelsinger Announces IDM 2.0 "
      "Strategy for Manufacturing, Innovation and Product Leadership', 23 March 2021",
      "https://www.intc.com/news-events/press-releases/detail/1451/intel-ceo-pat-gelsinger-announces-idm-2-0-strategy",
      "2021-03-23", kind="filing"),
    # --- the cobweb ---------------------------------------------------------------------------------------------------
    r("ezekiel.1938", 1938, "year", "Mordecai Ezekiel, 'The Cobweb Theorem', Quarterly Journal of Economics 52(2), "
      "February 1938, pp. 255-280: output planned from the last price, delivered a period later",
      "Quarterly Journal of Economics", "https://www.jstor.org/stable/1881734", "1938", kind="study"),
    r("coase.1935", 1935, "year", "R. H. Coase and R. F. Fowler, 'Bacon Production and the Pig-Cycle in Great "
      "Britain', Economica 2 (1935), p. 142: a critique of the cobweb account of the pig cycle", "Economica",
      "https://chicagounbound.uchicago.edu/journal_articles/3070", "1935", kind="study"),
    r("eia.crude.2010", 5.484, "million barrels a day", "US field production of crude oil, 2010 (2008: 5.0; 2025: 13.66)",
      "US Energy Information Administration, U.S. Field Production of Crude Oil (MCRFPUS2), annual",
      "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=MCRFPUS2&f=A", "2010"),
    r("eia.crude.2015", 9.433, "million barrels a day", "US field production of crude oil, 2015 (2016: 8.86)",
      "US Energy Information Administration, U.S. Field Production of Crude Oil (MCRFPUS2), annual",
      "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=MCRFPUS2&f=A", "2015"),
    r("chips.inventory.2019", 40, "days", "median inventory of semiconductor products held by buyers, 2019 (2021: "
      "less than 5 days, and smaller in key industries)", "US Department of Commerce, 'Results from Semiconductor "
      "Supply Chain Request for Information', 25 January 2022",
      "https://www.commerce.gov/news/blog/2022/01/results-semiconductor-supply-chain-request-information", "2019"),
    r("chips.inventory.2021", 5, "days", "median inventory of semiconductor products held by buyers, 2021: 'less "
      "than 5 days' (the value is the bound)", "US Department of Commerce, 'Results from Semiconductor Supply Chain "
      "Request for Information', 25 January 2022",
      "https://www.commerce.gov/news/blog/2022/01/results-semiconductor-supply-chain-request-information", "2021"),
    r("clark.1917", 1917, "year", "J. Maurice Clark, 'Business Acceleration and the Law of Demand: A Technical "
      "Factor in Economic Cycles', Journal of Political Economy 25(3), March 1917, pp. 217-235: demand for capital goods follows "
      "the growth of demand for the goods they make", "Journal of Political Economy",
      "https://doi.org/10.1086/252958", "1917", kind="study"),
    r("lee.1997", 1997, "year", "H. L. Lee, V. Padmanabhan and S. Whang, 'The Bullwhip Effect in Supply Chains', "
      "Sloan Management Review 38(3), Spring 1997: orders swing more than sales, and more at each step up the chain",
      "MIT Sloan Management Review", "https://sloanreview.mit.edu/article/the-bullwhip-effect-in-supply-chains/",
      "1997", kind="study"),
)
