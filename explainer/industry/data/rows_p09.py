"""Register rows for Part 9, *Mining and Metals*.  Checked 2026-11-24.

Escondida's discovery (Francisco Ortiz's account) and its 2025 results (BHP); Freeport-McMoRan's grades, costs and the
Grasberg mud rush (its Form 10-K for 2025); the US Geological Survey's Mineral Commodity Summaries 2026; Vale's
announcement of quarterly iron ore pricing (1 April 2010); and the Simon-Ehrlich wager.  Prices, the historical unit
values, and the companies' accounts are the Filing Room's FRED, USGS and SEC extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-24"
P = (9,)
ORTIZ = "https://cesco.cl/wp-content/uploads/2024/12/El-descubrimiento-de-Escondida.-Por-Francisco-Ortiz-1.pdf"
BHP25 = "https://announcements.asx.com.au/asxpdf/20250819/pdf/06n0rljcxbmtqy.pdf"
FCX25 = "https://www.sec.gov/Archives/edgar/data/831259/000083125926000012/fcx-20251231.htm"
MCS = "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-{}.pdf"
VALE10 = "https://echanges.dila.gouv.fr/OPENDATA/AMF/CNS/2010/04/FCCNS026242_20100401.pdf"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def ortiz(key, value, unit, definition, fact="1981-03"):
    return r(key, value, unit, definition, "Francisco Ortiz, 'El descubrimiento del yacimiento Escondida' (CESCO, "
             "December 2024), the account of the project's chief geologist", ORTIZ, fact, "study")


def bhp(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "BHP, results for the year ended 30 June 2025 (ASX release, 19 August 2025), "
             "Escondida", BHP25, fact)


def fcx(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Freeport-McMoRan Inc., Form 10-K for 2025", FCX25, fact)


def mcs(key, value, unit, definition, metal, fact="2025"):
    return r(key, value, unit, definition, f"US Geological Survey, Mineral Commodity Summaries 2026, '{metal.replace('-', ' ')}'",
             MCS.format(metal), fact, "official")


add(
    # --- Escondida: found, built, and fading ---------------------------------------------------------------------
    ortiz("esc.holes", 9, "holes", "reconnaissance holes drilled 3-21 March 1981 on the Llano Zaldivar and Cerro Colorado "
          "Grande (2,240 metres in all); the first five, on the Llano Zaldivar, found nothing worth mining"),
    ortiz("esc.found", 1981, "year", "hole No. 6, on Cerro Colorado Grande, finished on 14 March 1981, found the Escondida "
          "porphyry copper deposit"),
    ortiz("esc.first_estimate", 300, "Mt", "the first, conservative estimate: about 300 million tonnes of enriched ore at "
          "1.3-1.5% copper (the best zone, 2.5 km away, about 3%)"),
    ortiz("esc.cost", 3.0, "USD m", "what the regional exploration project had spent when it found Escondida, a little more "
          "than two years after it began (about $10.4m in today's dollars)"),
    ortiz("esc.opened", 1991, "year", "the mine was inaugurated on 14 March 1991 with an initial capacity of 320,000 tonnes "
          "of copper a year", "1991-03-14"),
    bhp("esc.output.2025", 1305, "kt", "Escondida's copper production, year to June 2025 (100%; 1,125 kt a year earlier)"),
    bhp("esc.cost.2025", 1.19, "USD/lb", "Escondida's unit cost, year to June 2025 (US$1.45 a year earlier)"),
    bhp("esc.ebitda.2025", 8.6, "USD bn", "Escondida's underlying EBITDA, year to June 2025 (US$5.8bn a year earlier)"),
    bhp("esc.grade.2025", 1.02, "%", "Escondida's concentrator feed grade, year to June 2025"),
    bhp("esc.grade.2026", 0.85, "%", "the feed grade BHP expects for the year to June 2026, with output of 1,150-1,250 kt",
        "2026"),
    bhp("esc.medium", 950, "kt", "BHP's medium-term outlook for Escondida, the average for FY2027-FY2031: 900-1,000 kt a "
        "year at a unit cost of US$1.50-1.80/lb", "2027-2031"),
    # --- Freeport-McMoRan: grades, costs, Grasberg --------------------------------------------------------------------
    fcx("fcx.grasberg.grade", 1.10, "%", "copper grade of ore milled at PT Freeport Indonesia's Grasberg district, 2025 "
        "(1.27% in 2024); gold 0.77 grams a tonne"),
    fcx("fcx.grasberg.cost", -0.55, "USD/lb", "PT Freeport Indonesia's unit net cash costs, 2025: a credit, because gold, silver "
        "and other by-products paid for more than all its costs (excluding $625m of mud-rush costs)"),
    fcx("fcx.sa.cost", 2.43, "USD/lb", "unit net cash costs, net of by-product credits, of Freeport's South America operations "
        "(Cerro Verde, mill grade 0.30%), 2025"),
    fcx("fcx.us.cost", 3.05, "USD/lb", "unit net cash costs, net of by-product credits, of Freeport's US copper mines (mill "
        "grade 0.31%, leach 0.21%), 2025"),
    fcx("fcx.us.leach", 0.21, "%", "average copper grade of ore placed on leach stockpiles at Freeport's North American mines, "
        "2025"),
    fcx("lme.copper.2025", 4.51, "USD/lb", "LME copper settlement price, 2025 average (low $3.87, high $5.68; $5.67 on 31 "
        "December)"),
    fcx("fcx.gold.price", 3418, "USD/oz", "PT Freeport Indonesia's average realized gold price, 2025 ($2,418 in 2024)"),
    fcx("fcx.mudrush", 7, "people", "killed in the mud rush at the Grasberg Block Cave mine on 8 September 2025; a phased "
        "restart of the block cave is planned from the second quarter of 2026", "2025-09-08"),
    fcx("fcx.ptfi.state", 51.24, "%", "share of PT Freeport Indonesia held by Indonesian state-owned and regional interests "
        "since December 2018 (MIND ID 26.24%, PTI 25.00%); Freeport holds 48.76%", "2018-12-21"),
    fcx("fcx.us.prod", 1304, "Mlb", "copper production of Freeport's US mines, 2025 (million recoverable pounds)"),
    fcx("fcx.sa.prod", 1064, "Mlb", "copper production of Freeport's South America operations, 2025"),
    fcx("fcx.ptfi.prod", 1015, "Mlb", "copper production of PT Freeport Indonesia, 2025 (1,800 in 2024, before the mud rush)"),
    # --- USGS, Mineral Commodity Summaries 2026 ---------------------------------------------------------------------
    mcs("usgs.cu.mine", 23000, "kt", "world copper mine production, 2025 (estimate)", "copper"),
    mcs("usgs.cu.refined", 29000, "kt", "world refined copper production, 2025 (estimate)", "copper"),
    mcs("usgs.cu.china.refined", 14000, "kt", "China's refined copper production, 2025 (estimate; its mines produced 1,800 kt)",
        "copper"),
    mcs("usgs.cu.chile", 5300, "kt", "Chile's copper mine production, 2025 (estimate; Congo 3,200, Peru 2,700)", "copper"),
    mcs("usgs.cu.mine.chl", 5300, "kt", "copper mine production of Chile, 2025 (estimate)", "copper"),
    mcs("usgs.cu.mine.cod", 3200, "kt", "copper mine production of Congo (Kinshasa), 2025 (estimate)", "copper"),
    mcs("usgs.cu.mine.per", 2700, "kt", "copper mine production of Peru, 2025 (estimate)", "copper"),
    mcs("usgs.cu.mine.chn", 1800, "kt", "copper mine production of China, 2025 (estimate)", "copper"),
    mcs("usgs.cu.mine.rus", 1300, "kt", "copper mine production of Russia, 2025 (estimate)", "copper"),
    mcs("usgs.cu.mine.usa", 1000, "kt", "copper mine production of the United States, 2025 (estimate)", "copper"),
    mcs("usgs.cu.mine.zmb", 940, "kt", "copper mine production of Zambia, 2025 (estimate)", "copper"),
    mcs("usgs.cu.mine.aus", 730, "kt", "copper mine production of Australia, 2025 (estimate)", "copper"),
    mcs("usgs.cu.mine.idn", 710, "kt", "copper mine production of Indonesia, 2025 (estimate)", "copper"),
    mcs("usgs.cu.mine.kaz", 710, "kt", "copper mine production of Kazakhstan, 2025 (estimate)", "copper"),
    mcs("usgs.cu.ref.chn", 14000, "kt", "refined copper production of China, 2025 (estimate)", "copper"),
    mcs("usgs.cu.ref.cod", 2800, "kt", "refined copper production of Congo (Kinshasa), 2025 (estimate)", "copper"),
    mcs("usgs.cu.ref.chl", 1700, "kt", "refined copper production of Chile, 2025 (estimate)", "copper"),
    mcs("usgs.cu.ref.jpn", 1400, "kt", "refined copper production of Japan, 2025 (estimate)", "copper"),
    mcs("usgs.cu.ref.rus", 950, "kt", "refined copper production of Russia, 2025 (estimate)", "copper"),
    mcs("usgs.cu.ref.usa", 850, "kt", "refined copper production of the United States, 2025 (estimate)", "copper"),
    mcs("usgs.au.price.2021", 1801, "USD/oz", "gold, 2021 average (Engelhard)", "gold", "2021"),
    mcs("usgs.au.price.2022", 1802, "USD/oz", "gold, 2022 average (Engelhard)", "gold", "2022"),
    mcs("usgs.au.price.2023", 1945, "USD/oz", "gold, 2023 average (Engelhard)", "gold", "2023"),
    mcs("usgs.au.price.2024", 2388, "USD/oz", "gold, 2024 average (Engelhard)", "gold", "2024"),
    mcs("usgs.cu.reserves", 980, "Mt", "world copper reserves", "copper"),
    mcs("usgs.cu.comex", 4.80, "USD/lb", "COMEX copper, 2025 average (projected; a record, 14% above 2024), attributed to "
        "uncertainty over US tariffs on copper; LME cash about $4.40", "copper"),
    mcs("usgs.cu.imports", 1700, "kt", "US imports of refined copper, 2025 (estimate; 903 kt in 2024)", "copper"),
    mcs("usgs.cu.critical", 2025, "year", "copper was added to the US list of critical minerals published on 7 November 2025",
        "copper", "2025-11-07"),
    mcs("usgs.li.price.2022", 63700, "USD/t", "battery-grade lithium carbonate, annual average, real (2021: 11,700; 2023: "
        "39,000; 2024: 11,800)", "lithium", "2022"),
    mcs("usgs.li.price.2025", 9000, "USD/t", "battery-grade lithium carbonate, 2025 annual average, real", "lithium"),
    mcs("usgs.li.batteries", 88, "%", "batteries' share of global lithium end use", "lithium"),
    mcs("usgs.co.congo", 73, "%", "Congo (Kinshasa)'s share of world cobalt mine output, 2025 (Indonesia 14%); Congo "
        "temporarily banned cobalt exports from February 2025", "cobalt"),
    mcs("usgs.ree.china", 270, "kt", "China's rare-earth mine production, 2025 (world about 390 kt); China tightened export "
        "controls in April and October 2025", "rare-earths"),
    mcs("usgs.ni.indonesia", 2600, "kt", "Indonesia's nickel mine production, 2025 (estimate; world 3,900 kt)", "nickel"),
    mcs("usgs.fe.australia", 980, "Mt", "Australia's usable iron ore production, 2025 (Brazil 420, India 310, China 290; "
        "world 2,600)", "iron-ore"),
    mcs("usgs.au.price", 3300, "USD/oz", "gold, 2025 average (a record, 38% above 2024)", "gold"),
    mcs("usgs.au.mine", 3300, "t", "world gold mine production, 2025 (China, Russia, Australia, Canada and the United "
        "States the largest)", "gold"),
    mcs("usgs.au.cb", 21, "%", "central banks' and other institutions' share of gold consumption, excluding ETFs, 2025 "
        "(jewellery 40%, bars 24%, coins 7%)", "gold"),
    # --- iron ore: the end of the benchmark ---------------------------------------------------------------------------
    r("vale.2010", 97, "%", "share of Vale's clients (90% of contract volumes) that had agreed to a new iron ore pricing "
      "regime based on short-term market references with quarterly price changes, replacing annual prices",
      "Vale S.A., press release 'Vale on iron ore pricing', 1 April 2010 (filed with the AMF)", VALE10, "2010-04-01"),
    # --- the wager ----------------------------------------------------------------------------------------------------
    r("bet.cheque", 576.07, "USD", "the cheque Paul Ehrlich mailed Julian Simon in October 1990, settling their bet of 29 "
      "September 1980 on $1,000 of chromium, copper, nickel, tin and tungsten ($200 each)",
      "Paul Sabin, The Bet: Paul Ehrlich, Julian Simon, and Our Gamble over Earth's Future (Yale University Press, 2013)",
      "https://yalebooks.yale.edu/book/9780300198973/the-bet/", "1990-10", "study"),
)
