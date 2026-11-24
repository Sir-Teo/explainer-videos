"""Register rows for Part 8, *Oil and Gas*.  Checked 2026-11-24.

The day a barrel cost less than nothing (the CFTC's staff report, EIA); the 2026 shock (EIA's Today in Energy and its
November Short-Term Energy Outlook); the cost of a barrel (Saudi Aramco's Annual Report 2025, the Dallas Fed Energy
Survey); reserves as an economic number (ExxonMobil's 10-Ks); Spindletop (the Handbook of Texas); Hubbert's 1956
forecasts; OPEC+'s 2020 cut (EIA).  Prices, production, rigs, trade, gasoline's components, gas and companies'
accounts are the Filing Room's EIA, FRED and SEC extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-24"
P = (8,)
CFTC = "https://cftc.gov/media/5296/InterimStaffReportNYMEX_WTICrudeOil/download"
TIE20 = "https://www.eia.gov/todayinenergy/detail.php?id=43495"
TIE26 = "https://www.eia.gov/todayinenergy/detail.php?id=67424"
STEO = "https://www.eia.gov/outlooks/steo/report/global_oil.php"
HORMUZ = "https://www.eia.gov/todayinenergy/detail.php?id=65504"
OPEC20 = "https://www.eia.gov/todayinenergy/detail.php?id=45236"
ARAMCO = ("https://www.aramco.com/-/media/publications/corporate-reports/reports-and-presentations/2025/fy/"
          "saudi-aramco-ara-2025-english.pdf")
DALLAS = "https://www.dallasfed.org/research/surveys/des/2026/2601"
XOM19 = "https://www.sec.gov/Archives/edgar/data/34088/000003408820000016/xom10k2019.htm"
XOM20 = "https://www.sec.gov/Archives/edgar/data/34088/000003408821000012/xom-20201231.htm"
XOM21 = "https://www.sec.gov/Archives/edgar/data/34088/000003408822000011/xom-20211231.htm"
TSHA = "https://www.tshaonline.org/handbook/entries/spindletop-oilfield"
HUBBERT = "https://www.resilience.org/stories/2006-03-08/nuclear-energy-and-fossil-fuels/"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def steo(key, value, unit, definition, fact="2026"):
    return r(key, value, unit, definition, "US Energy Information Administration, Short-Term Energy Outlook, 10 "
             "November 2026 ('Global oil markets')", STEO, fact, "official")


def aramco(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Saudi Aramco, Annual Report 2025", ARAMCO, fact)


def dallas(key, value, unit, definition):
    return r(key, value, unit, definition, "Federal Reserve Bank of Dallas, Dallas Fed Energy Survey, first quarter "
             "2026 (special questions, collected 11-19 March 2026)", DALLAS, "2026-03", "official")


add(
    # --- 20 April 2020 ---------------------------------------------------------------------------------------------
    r("cftc.wti.settle.2020", -37.63, "USD/bbl", "settlement price of NYMEX WTI crude oil futures for May 2020 delivery "
      "on 20 April 2020, the day before the contract expired", "US Commodity Futures Trading Commission, Interim Staff "
      "Report: Trading in NYMEX WTI Crude Oil Futures Contract Leading up to, on, and around April 20, 2020 (November "
      "2020)", CFTC, "2020-04-20", "official"),
    r("cftc.wti.prior.2020", 17.73, "USD/bbl", "the same contract's settlement on the previous trading day, 17 April "
      "2020", "US Commodity Futures Trading Commission, Interim Staff Report (November 2020)", CFTC, "2020-04-17",
      "official"),
    r("eia.cushing.2020", 76, "%", "share of Cushing's working storage capacity (76m barrels) in use on 17 April 2020: "
      "58m barrels in its tank farms, of 60m in inventory", "US Energy Information Administration, Today in Energy, "
      "'Low liquidity and limited available storage pushed WTI crude oil futures prices below zero', 27 April 2020",
      TIE20, "2020-04-17", "official"),
    r("eia.wti.low.2020", -40.32, "USD/bbl", "the front-month WTI futures price's low, about 2:30 pm ET on 20 April 2020",
      "US Energy Information Administration, Today in Energy, 27 April 2020", TIE20, "2020-04-20", "official"),
    r("eia.brent.2020", 19.33, "USD/bbl", "Brent futures for June 2020 delivery at the close on 21 April 2020, while the "
      "expiring WTI contract was below zero", "US Energy Information Administration, Today in Energy, 27 April 2020",
      TIE20, "2020-04-21", "official"),
    r("eia.runs.2020", 12.8, "mb/d", "US refinery runs in the week ending 17 April 2020, 4.1 mb/d (24%) below a year "
      "earlier", "US Energy Information Administration, Today in Energy, 27 April 2020", TIE20, "2020-04-17",
      "official"),
    r("eia.wti.since", 1983, "year", "the year NYMEX WTI futures began trading; 20 April 2020 was the first time the "
      "front-month price was negative", "US Energy Information Administration, Today in Energy (2020)", TIE20,
      "2020-04-20", "official"),
    # --- 2026 ---------------------------------------------------------------------------------------------------------
    r("eia.2026.brent.start", 61, "USD/bbl", "Brent front-month futures price at the start of 2026", "US Energy "
      "Information Administration, Today in Energy, 'Crude oil and petroleum product prices increased sharply in the "
      "first quarter of 2026', 7 April 2026", TIE26, "2026-01", "official"),
    r("eia.2026.brent.q1end", 118, "USD/bbl", "Brent front-month futures price at the end of March 2026, after "
      "military action in the Middle East on 28 February and the de facto closure of the Strait of Hormuz; the "
      "largest quarterly rise, adjusted for inflation, in data back to 1988", "US Energy Information Administration, "
      "Today in Energy, 7 April 2026", TIE26, "2026-03", "official"),
    r("eia.2026.spread", 25, "USD/bbl", "peak of the Brent-WTI futures spread (May delivery), 31 March 2026; about $4 "
      "at the start of the quarter", "US Energy Information Administration, Today in Energy, 7 April 2026", TIE26,
      "2026-03-31", "official"),
    steo("eia.steo.brent.oct", 124, "USD/bbl", "Brent spot price, October 2026 average: the highest since July 2022 "
         "in real terms", "2026-10"),
    steo("eia.steo.shutin.peak", 10.9, "mb/d", "crude oil production shut in across the Middle East at the peak, in "
         "May 2026 (EIA's assessment)", "2026-05"),
    steo("eia.steo.shutin.oct", 2.5, "mb/d", "Middle East crude production shut in, October 2026 average", "2026-10"),
    steo("eia.steo.demand.2026", -2.0, "mb/d", "change in global liquid fuels consumption in 2026 (estimate), mostly "
         "China and the Middle East"),
    steo("eia.steo.brent.2026", 97, "USD/bbl", "Brent spot price, 2026 average (2024: $81; 2025: $69)"),
    steo("eia.steo.brent.2027", 86, "USD/bbl", "EIA's forecast of the Brent spot price, 2027 average; $77 in the fourth "
         "quarter", "2027"),
    steo("eia.steo.supply.2025", 106.3, "mb/d", "global liquid fuels production, 2025", "2025"),
    steo("eia.steo.supply.2026", 101.7, "mb/d", "global liquid fuels production, 2026 (estimate)"),
    r("eia.hormuz.2024", 20, "mb/d", "oil flow through the Strait of Hormuz, 2024 average: about 20% of world "
      "petroleum liquids consumption", "US Energy Information Administration, Today in Energy, 'Amid regional "
      "conflict, the Strait of Hormuz remains critical oil chokepoint', June 2025", HORMUZ, "2024", "official"),
    # --- OPEC+ in 2020 --------------------------------------------------------------------------------------------------
    r("eia.opec.cut.2020", 9.7, "mb/d", "the initial cut agreed by OPEC+ in April 2020, from May 2020, tapering through "
      "April 2022; OPEC's crude output fell 6.0 mb/d from April to May", "US Energy Information Administration, Today "
      "in Energy, September 2020", OPEC20, "2020-05", "official"),
    # --- the cost of a barrel -----------------------------------------------------------------------------------------
    aramco("aramco.lifting", 3.51, "USD/boe", "average upstream lifting cost: production costs, taxes other than income "
           "taxes, related overheads; excluding exploration, royalty, R&D and depreciation (2024: $3.53)"),
    aramco("aramco.capex", 8.0, "USD/boe", "upstream capital spending per barrel of oil equivalent produced (2024: "
           "$8.3)"),
    aramco("aramco.production", 12.891, "mboe/d", "total hydrocarbon production (liquids 10.678 mb/d)"),
    aramco("aramco.msc", 12.0, "mb/d", "crude oil maximum sustainable capacity, at the end of 2025"),
    aramco("aramco.reserves", 247.2, "bn boe", "reserves under the Concession at the end of 2025, including 186.5bn "
           "barrels of crude oil and condensate"),
    aramco("aramco.price", 69.2, "USD/bbl", "average realized crude oil price, 2025 (2024: $80.2)"),
    aramco("aramco.royalties", 40.4, "USD bn", "royalties and other taxes, 2025 (2024: $53.5bn)"),
    aramco("aramco.tax", 94.0, "USD bn", "income taxes and zakat, 2025"),
    aramco("aramco.net", 93.4, "USD bn", "net income, 2025 (adjusted: $104.7bn)"),
    dallas("dallas.new", 66, "USD/bbl", "WTI price firms said they need to profitably drill a new well, average of all "
           "firms (Q1 2025: $65); $62-$70 by region"),
    dallas("dallas.new.permian", 67, "USD/bbl", "the same, Permian Basin average"),
    dallas("dallas.new.large", 59, "USD/bbl", "the same, large firms (10,000 b/d or more); small firms $68"),
    dallas("dallas.existing", 43, "USD/bbl", "WTI price needed to cover operating expenses of existing wells, average "
           "(Q1 2025: $41); $34-$47 by region; large firms $32, small $46"),
    # --- reserves are an economic number ------------------------------------------------------------------------------
    r("xom.reserves.2019", 22.4, "bn boe", "ExxonMobil's proved reserves at the end of 2019", "Exxon Mobil Corporation, "
      "Form 10-K for 2019", XOM19, "2019"),
    r("xom.reserves.2020", 15.2, "bn boe", "ExxonMobil's proved reserves at the end of 2020, on the SEC's basis (the "
      "average first-of-month price of the previous twelve months)", "Exxon Mobil Corporation, Form 10-K for 2020",
      XOM20, "2020"),
    r("xom.reserves.2021", 18.5, "bn boe", "ExxonMobil's proved reserves at the end of 2021", "Exxon Mobil "
      "Corporation, Form 10-K for 2021", XOM21, "2021"),
    r("xom.reserves.2025", 19.3, "bn boe", "ExxonMobil's proved reserves at the end of 2025 (36% undeveloped)",
      "Exxon Mobil Corporation, Form 10-K for 2025",
      "https://www.sec.gov/Archives/edgar/data/34088/000003408826000045/xom-20251231.htm", "2025"),
    r("xom.kearl", 3.1, "bn bbl", "bitumen at Kearl (Canadian oil sands) that no longer qualified as proved reserves "
      "at the end of 2020; also 0.6bn at Cold Lake and 0.5bn boe in the US, and 1.5bn boe from lower capital spending",
      "Exxon Mobil Corporation, Form 10-K for 2020", XOM20, "2020"),
    # --- Spindletop ----------------------------------------------------------------------------------------------------
    r("spindletop.date", 1901, "year", "the Lucas well at Spindletop, near Beaumont, Texas, blew in on 10 January 1901 "
      "at 1,139 feet", "Handbook of Texas Online (Texas State Historical Association), 'Spindletop Oilfield'", TSHA,
      "1901-01-10", "study"),
    r("spindletop.flow", 100000, "bbl/d", "the Lucas gusher's estimated flow before it was capped on 19 January 1901",
      "Handbook of Texas Online, 'Spindletop Oilfield'", TSHA, "1901-01", "study"),
    r("spindletop.1902", 17.5, "m bbl", "Spindletop's output in 1902; by February 1904 its wells were down to 10,000 "
      "barrels a day", "Handbook of Texas Online, 'Spindletop Oilfield'", TSHA, "1902", "study"),
    r("arps.1945", 1945, "year", "J. J. Arps, 'Analysis of Decline Curves', Transactions of the AIME 160 (1945): the "
      "exponential, hyperbolic and harmonic declines petroleum engineers still fit", "J. J. Arps, Transactions of the "
      "AIME 160(1), 228-247 (1945)", "https://doi.org/10.2118/945228-G", "1945", "study"),
    # --- Hubbert, 1956 -------------------------------------------------------------------------------------------------
    r("hubbert.us.150", 150, "bn bbl", "Hubbert's estimate of the ultimate US crude oil production (land and offshore), "
      "with which US output 'must culminate at about 1965'; 52.5bn barrels had been produced by 1 January 1956",
      "M. King Hubbert, 'Nuclear Energy and the Fossil Fuels', American Petroleum Institute, San Antonio, March 1956 "
      "(Shell Development Company Publication No. 95)", HUBBERT, "1956", "study"),
    r("hubbert.us.200", 200, "bn bbl", "Hubbert's alternative: if the ultimate were 50bn barrels higher, the "
      "culmination would be 'retarded only until about 1970'", "Hubbert (1956)", HUBBERT, "1956", "study"),
    r("hubbert.world", 1250, "bn bbl", "Hubbert's ultimate world crude oil production, with a peak 'at about the year "
      "2000'", "Hubbert (1956)", HUBBERT, "1956", "study"),
)
