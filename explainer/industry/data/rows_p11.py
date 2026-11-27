"""Register rows for Part 11, *Heavy Materials*.  Checked 2026-11-27.

worldsteel's World Steel in Figures 2026 and its climate policy paper (October 2025); the USGS Mineral Commodity
Summaries 2026 (iron and steel, scrap, cement, aluminium, crushed stone); the 1994 European Commission cement cartel
decision and the 2000 judgment that cut its fines; the EU's carbon border regulation; Forms 10-K of Nucor,
Cleveland-Cliffs, Vulcan, Martin Marietta and Alcoa; Nucor's own history; Bessemer's 1856 paper and Christensen's
book.  Series (worldsteel's yearbooks, Nucor's 10-Ks year by year, the International Aluminium Institute) are in
``tables.py``; the companies' accounts, prices and US history are the Filing Room's SEC, FRED, USGS and OWID extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (11,)
WSIF = "https://worldsteel.org/wp-content/uploads/World-Steel-in-Figures-2026.pdf"
WSCC = "https://worldsteel.org/wp-content/uploads/Policy-Paper-climate-change-and-the-production-of-steel.pdf"
MCS = "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-{}.pdf"
EU94 = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:31994D0815"
CURIA = "https://curia.europa.eu/en/actu/communiques/cp00/aff/cp0016en.htm"
CBAM = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32023R0956"
NUE = "https://www.sec.gov/Archives/edgar/data/73309/000119312526071575/nue-20251231.htm"
NUE_HIST = "https://nucor.com/history"
CLF = "https://www.sec.gov/Archives/edgar/data/764065/000076406526000025/clf-20251231.htm"
VMC = "https://www.sec.gov/Archives/edgar/data/1396009/000162828026009546/vmc-20251231.htm"
MLM = "https://www.sec.gov/Archives/edgar/data/916076/000119312526059193/mlm-20251231.htm"
AA = "https://www.sec.gov/Archives/edgar/data/1675149/000119312526077167/aa-20251231.htm"
SRO26 = "https://worldsteel.org/media/press-releases/2026/worldsteel-short-range-outlook-october-2026/"
WSPROD = "https://worldsteel.org/media/press-releases/2026/october-2026-crude-steel-production/"
BESSEMER = "https://archive.org/details/sirhenrybessemer00bessuoft"
CHRISTENSEN = "https://www.hbs.edu/faculty/Pages/item.aspx?num=46"


def r(key, value, unit, definition, source, url, fact, kind="official", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def ws(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "World Steel Association, World Steel in Figures 2026 (data finalised 8 June "
             "2026)", WSIF, fact)


def wscc(key, value, unit, definition, fact="2024", **kw):
    return r(key, value, unit, definition, "World Steel Association, 'Climate change and the production of iron and "
             "steel', policy paper (October 2025)", WSCC, fact, **kw)


def usgs(key, value, unit, definition, chapter, fact="2025", **kw):
    return r(key, value, unit, definition, f"US Geological Survey, Mineral Commodity Summaries 2026 (February 2026), "
             f"'{chapter.replace('-', ' ').title()}'", MCS.format(chapter), fact, **kw)


def filing(key, value, unit, definition, who, url, fact="2025", **kw):
    return r(key, value, unit, definition, f"{who}, Form 10-K for 2025", url, fact, "filing", **kw)


COMPANIES = {"baowu": ("China Baowu Group", 124.76), "arcelormittal": ("ArcelorMittal", 63.43),
             "nippon": ("Nippon Steel", 57.78), "ansteel": ("Ansteel Group", 57.61), "hbis": ("HBIS Group", 42.49),
             "shagang": ("Shagang Group", 39.10), "jianlong": ("Jianlong Group", 38.02), "posco": ("POSCO Holdings", 37.36),
             "delong": ("Delong Steel", 32.03), "tata": ("Tata Steel Group", 30.46), "jsw": ("JSW Steel", 30.28),
             "shougang": ("Shougang Group", 30.23), "jfe": ("JFE Steel", 22.69), "nucor": ("Nucor", 22.33),
             "sail": ("SAIL", 19.44), "hyundai": ("Hyundai Steel", 17.95), "cliffs": ("Cleveland-Cliffs", 17.06),
             "gerdau": ("Gerdau", 13.03), "stld": ("Steel Dynamics", 10.70), "thyssenkrupp": ("thyssenkrupp", 9.41)}
COUNTRIES = {"china": 960.8, "india": 164.9, "us": 81.9, "japan": 80.7, "russia": 67.9, "korea": 62.2,
             "turkiye": 38.1, "germany": 34.1, "brazil": 33.4, "iran": 32.0, "vietnam": 24.7}
EAF = {"world": 30.3, "china": 10.6, "us": 71.3, "eu": 45.8, "india": 57.7, "japan": 25.8, "korea": 27.0,
       "turkiye": 72.2}

add(
    # --- worldsteel: countries, companies, routes, trade, use ---------------------------------------------------------
    *[ws(f"ws.crude.{k}.2025", v, "million tonnes", f"Crude steel production, {k}, 2025") for k, v in COUNTRIES.items()],
    ws("ws.crude.world.2025", 1849, "million tonnes", "World crude steel production, 2025"),
    ws("ws.crude.china.2024", 1005.1, "million tonnes", "China's crude steel production, 2024", "2024"),
    *[ws(f"ws.company.{k}.2025", v, "million tonnes", f"{n}: crude steel production, 2025 (worldsteel's top-50 "
         "table: more than 50% ownership counted in full, 30-50% pro rata)") for k, (n, v) in COMPANIES.items()],
    *[ws(f"ws.eaf.{k}.2025", v, "% of crude steel", f"Share of crude steel made in electric furnaces, {k}, 2025")
      for k, v in EAF.items()],
    ws("ws.bof.world.2025", 69.4, "% of crude steel", "Share of world crude steel made in oxygen converters, 2025"),
    ws("ws.exports.china.2025", 133.6, "million tonnes", "China's exports of semi-finished and finished steel, 2025"),
    ws("ws.netexports.china.2025", 126.6, "million tonnes", "China's net exports of steel, 2025"),
    r("ws.exports.china.2021", 66.2, "million tonnes", "China's exports of semi-finished and finished steel, 2021",
      "World Steel Association, World Steel in Figures 2022, 'Major importers and exporters of steel, 2021'",
      "https://worldsteel.org/wp-content/uploads/World-Steel-in-Figures-2022.pdf", "2021"),
    ws("ws.imports.eu.2025", 43.7, "million tonnes", "The EU's imports of steel from outside the EU, 2025"),
    ws("ws.asu_pc.world.2025", 209, "kg a person", "World apparent steel use per person (finished steel), 2025"),
    ws("ws.asu_pc.china.2025", 562, "kg a person", "China's apparent steel use per person (finished steel), 2025"),
    ws("ws.asu_pc.us.2025", 262, "kg a person", "US apparent steel use per person (finished steel), 2025"),
    ws("ws.asu_pc.india.2025", 109, "kg a person", "India's apparent steel use per person (finished steel), 2025"),
    ws("ws.asu.world.2025", 1718.2, "million tonnes", "World apparent steel use (finished steel products), 2025"),
    r("ws.sro.china.2027", -1.0, "% change", "worldsteel's forecast of the change in China's steel demand in 2027",
      "World Steel Association, Short Range Outlook, 12 October 2026", SRO26, "2027 (forecast)", "tracker"),
    r("ws.sro.china.2026", -2.0, "% change", "worldsteel's forecast of the change in China's steel demand in 2026",
      "World Steel Association, Short Range Outlook, 12 October 2026", SRO26, "2026 (forecast)", "tracker"),
    r("ws.prod.china.jan_oct.2026", 795.6, "million tonnes", "China's crude steel production, January-October 2026 "
      "(-2.8% on a year before)", "World Steel Association, 'October 2026 crude steel production' (24 November 2026)",
      WSPROD, "January-October 2026"),
    r("ws.prod.china.jan_oct.change", -2.8, "% change", "China's crude steel production, January-October 2026 against "
      "January-October 2025", "World Steel Association, 'October 2026 crude steel production' (24 November 2026)",
      WSPROD, "January-October 2026"),
    # --- worldsteel: emissions -------------------------------------------------------------------------------------------
    wscc("ws.ghg.avg.2024", 2.18, "t CO2e a tonne", "Average greenhouse gas emissions per tonne of crude steel (scope 1, "
         "2 and 3)"),
    wscc("ws.ghg.total.2024", 4.1, "billion t CO2e", "The steel industry's total greenhouse gas emissions, 2024 (75% "
         "direct)"),
    wscc("ws.ghg.share.2024", 7.5, "% of global GHG", "The steel industry's share of global anthropogenic greenhouse gas "
         "emissions", lo=7.0, hi=8.0),
    wscc("ws.co2.bfbof", 2.34, "t CO2 a tonne", "Average CO2 per tonne of crude steel: blast furnace and oxygen "
         "converter"),
    wscc("ws.co2.scrapeaf", 0.69, "t CO2 a tonne", "Average CO2 per tonne of crude steel: scrap in an electric furnace"),
    wscc("ws.co2.drieaf", 1.47, "t CO2 a tonne", "Average CO2 per tonne of crude steel: directly reduced iron in an "
         "electric furnace"),
    wscc("ws.scrap.avoids.co2", 1.5, "t CO2", "CO2 avoided by each tonne of scrap used in steelmaking"),
    wscc("ws.scrap.avoids.ore", 1.4, "t", "Iron ore avoided by each tonne of scrap used"),
    wscc("ws.scrap.avoids.coal", 740, "kg", "Coal avoided by each tonne of scrap used"),
    wscc("ws.capex.facilities", 1.2, "US$ trillion", "worldsteel's estimate of the capital spending the transition needs "
         "in new and adapted steel facilities (plus US$2.5-4 trillion upstream and downstream)", "estimate"),
    # --- USGS: steel and scrap -------------------------------------------------------------------------------------------
    usgs("usgs.steel.us.raw.2025", 82, "million tonnes", "US raw steel production, 2025 (estimated)", "iron-steel"),
    usgs("usgs.steel.us.value.2025", 149, "$ billion", "Estimated sales value of US iron and steel, 2025", "iron-steel"),
    usgs("usgs.steel.us.integrated", 2, "companies", "Companies operating integrated steel mills (blast furnaces) at the "
         "start of 2025, at eight active locations", "iron-steel"),
    usgs("usgs.steel.us.minimills", 102, "minimills", "Minimills making raw steel in electric arc furnaces (47 companies)",
         "iron-steel"),
    usgs("usgs.steel.us.minimill_cos", 47, "companies", "Companies making raw steel in electric arc furnaces", "iron-steel"),
    usgs("usgs.steel.us.capacity.2025", 105, "million tonnes a year", "US raw steel capacity, 2025", "iron-steel"),
    usgs("usgs.steel.us.construction", 31, "% of shipments", "Construction's share of US steel shipments, 2025",
         "iron-steel"),
    usgs("usgs.steel.us.auto", 15, "% of shipments", "Automotive share of US steel shipments, 2025", "iron-steel"),
    usgs("usgs.steel.tariff.march2025", 25, "%", "Section 232 tariff on imported steel from March 2025, all countries",
         "iron-steel"),
    usgs("usgs.steel.tariff.june2025", 50, "%", "Section 232 tariff on imported steel from June 2025", "iron-steel"),
    usgs("usgs.steel.us.imports.2025", 24, "million tonnes", "US imports of steel mill products, 2025 (estimated)",
         "iron-steel"),
    usgs("usgs.scrap.cars", 13, "million tonnes a year", "Steel recycled from automobiles in North America (more than "
         "280 shredders)", "iron-steel-scrap"),
    usgs("usgs.scrap.structural", 97, "%", "Recycling rate of structural steel from construction", "iron-steel-scrap"),
    usgs("usgs.scrap.price.2025", 319, "$ a tonne", "No. 1 heavy melting scrap, composite delivered price, 2025",
         "iron-steel-scrap"),
    # --- USGS: cement ------------------------------------------------------------------------------------------------------
    usgs("usgs.cement.us.2025", 84, "million tonnes", "US cement production (portland, blended and masonry), 2025",
         "cement"),
    usgs("usgs.cement.us.plants", 97, "plants", "US cement plants, 2025 (in 34 states and Puerto Rico)", "cement"),
    usgs("usgs.cement.us.price.2025", 160, "$ a tonne", "Average mill value of US cement, 2025", "cement"),
    usgs("usgs.cement.us.price.2021", 127, "$ a tonne", "Average mill value of US cement, 2021", "cement", "2021"),
    usgs("usgs.cement.us.value.2025", 17, "$ billion", "Value of US cement shipments, 2025", "cement"),
    usgs("usgs.cement.us.readymix", 72.5, "% of sales", "Share of US cement sold to ready-mixed concrete producers, 2025",
         "cement", lo=70, hi=75),
    usgs("usgs.cement.us.imports.2025", 23, "million tonnes", "US imports of hydraulic cement, 2025", "cement"),
    usgs("usgs.cement.us.blended", 63, "% of shipments", "Blended cement's share of US cement shipments, first nine "
         "months of 2025 (95% of it portland-limestone cement)", "cement"),
    usgs("usgs.cement.world.2025", 3800, "million tonnes", "World cement production, 2025 (estimated)", "cement"),
    usgs("usgs.cement.china.2025", 1700, "million tonnes", "China's cement production, 2025 (estimated)", "cement"),
    usgs("usgs.cement.india.2025", 470, "million tonnes", "India's cement production, 2025 (estimated)", "cement"),
    usgs("usgs.cement.vietnam.2025", 100, "million tonnes", "Viet Nam's cement production, 2025 (estimated)", "cement"),
    # --- USGS: aluminium and stone -------------------------------------------------------------------------------------------
    usgs("usgs.alu.us.primary.2025", 660, "thousand tonnes", "US primary aluminium production, 2025", "aluminum"),
    usgs("usgs.alu.us.smelters", 6, "smelters", "US primary aluminium smelters operated in 2025 (three companies, five "
         "states; two shut since 2022 and 2024)", "aluminum"),
    usgs("usgs.alu.us.price.2025", 180, "cents a pound", "Average US market (spot) price of aluminium ingot, 2025",
         "aluminum"),
    usgs("usgs.alu.us.price.2024", 129.5, "cents a pound", "Average US market (spot) price of aluminium ingot, 2024",
         "aluminum", "2024"),
    usgs("usgs.alu.us.transport", 36, "% of consumption", "Transportation's share of US aluminium use, 2025", "aluminum"),
    usgs("usgs.alu.us.packaging", 24, "% of consumption", "Packaging's share of US aluminium use, 2025", "aluminum"),
    usgs("usgs.alu.world.2025", 74000, "thousand tonnes", "World primary aluminium production, 2025", "aluminum"),
    usgs("usgs.alu.tariff.june2025", 50, "%", "US tariff on aluminium from June 2025 (most countries)", "aluminum"),
    usgs("usgs.stone.us.2025", 1500, "million tonnes", "US crushed stone production, 2025", "stone-crushed"),
    usgs("usgs.stone.us.value.2025", 27, "$ billion", "Value of US crushed stone, 2025", "stone-crushed"),
    usgs("usgs.stone.us.quarries", 3500, "quarries", "US crushed stone quarries (1,400 companies), 2025", "stone-crushed"),
    usgs("usgs.stone.us.price.2025", 18.50, "$ a tonne", "Average unit value of US crushed stone, 2025",
         "stone-crushed"),
    usgs("usgs.stone.us.aggregate", 72, "% of output", "Share of US crushed stone used as construction aggregate",
         "stone-crushed"),
    usgs("usgs.stone.us.cement", 17, "% of output", "Share of US crushed stone used to make cement", "stone-crushed"),
    # --- the European cement cartel ----------------------------------------------------------------------------------------
    r("eu.cement.decision", 1994, "year", "Commission Decision 94/815/EC of 30 November 1994 (Cases IV/33.126 and 33.322, "
      "Cement): an agreement 'designed to ensure non-transhipment to home markets'", "European Commission, Decision "
      "94/815/EC, Official Journal L 343, 30 December 1994", EU94, "1994-11-30"),
    r("eu.cement.start", 1983, "year", "The meeting of 14 January 1983 at which the industry agreed the rule of "
      "'non-transhipment to home markets'", "Court of First Instance, Press Release No 16/00 (15 March 2000)", CURIA,
      "1983-01-14"),
    r("eu.cement.parties", 42, "undertakings and associations", "Addressees found to have taken part in the single "
      "infringement", "Court of First Instance, Press Release No 16/00 (15 March 2000)", CURIA, "1994"),
    r("eu.cement.fine", 250, "EUR million", "Total fines imposed by the Commission (approximately)", "Court of First "
      "Instance, Press Release No 16/00 (15 March 2000)", CURIA, "1994"),
    r("eu.cement.cut", 140, "EUR million", "Reduction of the fines by the Court of First Instance (almost)", "Court of "
      "First Instance, Press Release No 16/00 (15 March 2000)", CURIA, "2000-03-15"),
    r("eu.cement.haul", 0.07, "ECU a tonne-km", "Unit cost of road transport of cement, 1989, for 450-499 km (between "
      "ECU 0.06 and 0.08)", "European Commission, Decision 94/815/EC, recital 10", EU94, "1989", lo=0.06, hi=0.08),
    r("eu.cement.price.uk", 70, "ECU a tonne", "The British cement price around 1981 (Cembureau figures cited in the "
      "decision)", "European Commission, Decision 94/815/EC, recital 9", EU94, "1981"),
    r("eu.cbam.start", 2026, "year", "Regulation (EU) 2023/956, the carbon border adjustment mechanism: importers' "
      "obligations (Articles 4, 6-9) apply from 1 January 2026, after a transitional period from 1 October 2023; it "
      "covers cement, iron and steel, aluminium, fertilisers, electricity and hydrogen", "Regulation (EU) 2023/956 of "
      "10 May 2023, Article 36 and Annex I", CBAM, "2026-01-01"),
    # --- companies ----------------------------------------------------------------------------------------------------------
    filing("nucor.price.2025", 1008, "$ a ton", "Average sales price per ton, Nucor's steel mills segment, 2025",
           "Nucor Corporation", NUE),
    filing("nucor.scrap.2025", 392, "$ a gross ton", "Average cost of scrap and scrap substitutes used, 2025",
           "Nucor Corporation", NUE),
    filing("nucor.scrap.per_ton", 1.1, "tons", "Scrap and scrap substitutes needed for one ton of steel, on average",
           "Nucor Corporation", NUE),
    filing("nucor.util.2025", 83, "% of capacity", "Average utilization of Nucor's steel mills, 2025",
           "Nucor Corporation", NUE),
    r("nucor.darlington", 1969, "year", "Nucor's first mini mill, Darlington, South Carolina, goes into production",
      "Nucor Corporation, 'History' (company website)", NUE_HIST, "1969", "filing"),
    r("nucor.crawfordsville", 1989, "year", "Thin-slab casting goes online at Nucor's Crawfordsville, Indiana, mini mill, "
      "'the first mini mill in the world to make quality flat-rolled steel using the technology'", "Nucor Corporation, "
      "'History' (company website)", NUE_HIST, "1989", "filing",
      note="Nucor's timeline heads the entry 1992 but says that in 1992, 'after three years of successfully producing "
           "sheet using thin-slab technology', it opened a second sheet mill: production began in 1989.  Films say "
           "'at the end of the 1980s'."),
    filing("clf.hrc.2025", 851, "$ a net ton", "Average US hot-rolled coil index price, 2025", "Cleveland-Cliffs", CLF),
    filing("clf.hrc.2024", 772, "$ a net ton", "Average US hot-rolled coil index price, 2024", "Cleveland-Cliffs", CLF,
           "2024"),
    filing("clf.asp.2025", 1005, "$ a ton", "Average selling price per ton of steel products, 2025", "Cleveland-Cliffs",
           CLF),
    filing("clf.margin.2025", -5, "% of revenue", "Steelmaking gross margin, 2025", "Cleveland-Cliffs", CLF),
    filing("clf.pellets", 1.4, "net tons", "Iron ore pellets needed for one net ton of raw steel in a blast furnace "
           "(with 0.3-0.4 net tons of coke and 0.3 of scrap)", "Cleveland-Cliffs", CLF),
    filing("clf.coke", 0.35, "net tons", "Coke needed for one net ton of raw steel", "Cleveland-Cliffs", CLF, lo=0.3,
           hi=0.4),
    filing("clf.coal_per_coke", 1.4, "net tons", "Coal needed for one net ton of coke", "Cleveland-Cliffs", CLF),
    filing("clf.scrap.bof", 0.3, "net tons", "Scrap or substitutes charged with one net ton of blast-furnace steel",
           "Cleveland-Cliffs", CLF),
    filing("clf.idled.2025", 6, "operations", "Operations Cliffs decided in 2025 to fully or partially idle, or close "
           "(Dearborn's blast furnace idled; Steelton, Conshohocken and Riverdale closed)", "Cleveland-Cliffs", CLF),
    filing("vmc.shipments.2025", 226.8, "million tons", "Vulcan's aggregates shipments, 2025 (short tons)",
           "Vulcan Materials", VMC),
    filing("vmc.price.2025", 21.98, "$ a ton", "Vulcan's freight-adjusted aggregates sales price, 2025", "Vulcan Materials",
           VMC),
    filing("vmc.gp.2025", 8.66, "$ a ton", "Vulcan's aggregates gross profit per ton, 2025", "Vulcan Materials", VMC),
    filing("vmc.cashgp.2025", 11.33, "$ a ton", "Vulcan's aggregates cash gross profit per ton, 2025 (non-GAAP)",
           "Vulcan Materials", VMC),
    filing("vmc.reserves", 16.6, "billion tons", "Vulcan's proven and probable aggregates reserves, end of 2025",
           "Vulcan Materials", VMC),
    filing("vmc.truck", 80, "% of shipments", "Share of Vulcan's aggregates delivered by truck straight from the "
           "quarry", "Vulcan Materials", VMC),
    filing("mlm.crh.2024", 2.1, "$ billion", "Martin Marietta's sale of its South Texas cement business to CRH, "
           "completed 9 February 2024", "Martin Marietta Materials", MLM, "2024-02-09"),
    filing("alcoa.power_share", 24, "% of costs", "Electric power's share of Alcoa's primary aluminium production costs, "
           "2025", "Alcoa", AA),
    # --- history and ideas ----------------------------------------------------------------------------------------------------
    r("bessemer.1856", 1856, "year", "Henry Bessemer reads his paper on 'the manufacture of iron without fuel' to the "
      "Mechanical Section of the British Association at Cheltenham on the morning of 13 August 1856, the day after he "
      "left London ('Tuesday, the 12th August, 1856')", "Sir Henry Bessemer, F.R.S.: An Autobiography (London: "
      "Engineering, 1905), chapter on the Cheltenham meeting", BESSEMER, "1856-08-13", "study"),
    r("bessemer.carbon", 5, "% carbon", "Bessemer's working assumption: 'crude iron contains about 5 per cent. of "
      "carbon', which burns at a white heat when air is blown through it", "Bessemer (1905), 'The Cheltenham Paper, "
      "1856'", BESSEMER, "1856", "study"),
    r("bessemer.charge", 7, "hundredweight", "His first apparatus converted 'about 7 cwt. of crude pig iron into malleable "
      "iron in thirty minutes'", "Bessemer (1905), 'The Cheltenham Paper, 1856'", BESSEMER, "1856", "study"),
    r("bessemer.minutes", 30, "minutes", "Time to convert a charge of pig iron in Bessemer's first apparatus",
      "Bessemer (1905), 'The Cheltenham Paper, 1856'", BESSEMER, "1856", "study"),
    r("christensen.1997", 1997, "year", "Clayton Christensen, The Innovator's Dilemma (Harvard Business School Press, "
      "1997), on minimills' disruption of integrated mills", "Christensen (1997)", CHRISTENSEN, "1997", "study"),
)
