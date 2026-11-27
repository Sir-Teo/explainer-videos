"""Register rows for Part 17, *Automobiles*.  Checked 2026-11-27.

Henry Ford's *My Life and Work* (1922) on the first moving lines; Toyota's own pages on its plants and its production
system; the Forms 10-K of General Motors (2025 and 2023), Ford (2025 and 2023), Tesla (2025, 2020, 2018), Rivian, Lucid
and AutoNation (2025), Tesla's first-quarter 2016 update and Lucid's 2025 production release (Forms 8-K); the Forms 20-F
of Toyota and Honda (fiscal 2026, to March 2026), Stellantis and Ferrari (2025); Volkswagen's Annual Report 2025 and
BYD's 2025 annual results announcement (HKEX); China's 2017 and 2020 plans for the industry (gov.cn) and the China
Association of Automobile Manufacturers' results as reported by Xinhua and the China Securities Journal; the US Trade
Representative's notice of September 2024 and the European Commission's countervailing duty regulation of October 2024.
Series are the Filing Room's SEC, FRED, Census, UN Comtrade, EIA and IEA extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (17,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
FORD = "https://archive.org/download/mylifeandwork00crowgoog/mylifeandwork00crowgoog_djvu.txt"
TOY_TOURS = "https://global.toyota/en/company/plant-tours/"
TOY_TPS = "https://www.toyota-global.com/company/vision_philosophy/toyota_production_system/"
GM25 = SEC + "1467858/000146785826000013/gm-20251231.htm"
GM23 = SEC + "1467858/000146785824000031/gm-20231231.htm"
F25 = SEC + "37996/000003799626000015/f-20251231.htm"
F23 = SEC + "37996/000003799624000009/f-20231231.htm"
TSLA25 = SEC + "1318605/000162828026003952/tsla-20251231.htm"
TSLA20 = SEC + "1318605/000156459021004599/tsla-10k_20201231.htm"
TSLA18 = SEC + "1318605/000156459019003165/tsla-10k_20181231.htm"
TSLA16 = SEC + "1318605/000119312516577582/d158845dex991.htm"
RIVN25 = SEC + "1874178/000187417826000008/rivn-20251231.htm"
LCID25 = SEC + "1811210/000162828026011053/lcid-20251231.htm"
LCID_PR = SEC + "1811210/000162828026000236/fy25ex991-productionanddel.htm"
AN25 = SEC + "350698/000162828026007800/an-20251231.htm"
STLA25 = SEC + "1605484/000160548426000021/stellantis-20251231.htm"
RACE25 = SEC + "1648416/000164841626000024/race-20251231.htm"
TM26 = SEC + "1094517/000119312526264811/d101983d20f.htm"
HMC26 = SEC + "715153/000119312526274991/d116494d20f.htm"
VW25 = "https://annualreport2025.volkswagen-group.com/_assets/downloads/add-additional-information-vw-ar25.pdf"
BYD25 = "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032702644.pdf"
CN17 = "https://www.gov.cn/gongbao/content/2017/content_5230289.htm"
CN20 = "https://www.gov.cn/zhengce/content/2020-11/02/content_5556716.htm"
XH26 = "https://www.news.cn/fortune/20260114/cbbd861081c349d8ae238167ca418fa3/c.html"
CS21 = "https://cs.com.cn/xwzx/hg/202101/t20210113_6129910.html"
USTR = "https://www.govinfo.gov/content/pkg/FR-2024-09-18/pdf/2024-21217.pdf"
EU = "https://eur-lex.europa.eu/eli/reg_impl/2024/2754/oj"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def k(key, value, unit, definition, who, form, url, fact, **kw):
    return r(key, value, unit, definition, f"{who}, Form {form}", url, fact, **kw)


def ford(key, value, unit, definition):
    return r(key, value, unit, definition, "Henry Ford with Samuel Crowther, My Life and Work (1922), chapter V, "
             "'Getting into Production', pp. 81-83", FORD, "1913-1914", "study")


def gm(key, value, unit, definition, fact="2025", url=GM25, form="10-K 2025"):
    return k(key, value, unit, definition, "General Motors", form, url, fact)


def fd(key, value, unit, definition, fact="2025", url=F25, form="10-K 2025"):
    return k(key, value, unit, definition, "Ford Motor Company", form, url, fact)


def an(key, value, unit, definition, fact="2025"):
    return k(key, value, unit, definition, "AutoNation", "10-K 2025", AN25, fact)


def tm(key, value, unit, definition, fact="fiscal 2026 (to 2026-03-31)"):
    return k(key, value, unit, definition, "Toyota Motor Corporation", "20-F, fiscal 2026", TM26, fact)


def hmc(key, value, unit, definition, fact="fiscal 2026 (to 2026-03-31)"):
    return k(key, value, unit, definition, "Honda Motor Co.", "20-F, fiscal 2026", HMC26, fact)


def eu(key, value, group):
    return r(key, value, "percent", f"definitive countervailing duty on new battery electric cars from China made by "
             f"{group}, on the net free-at-Union-frontier price before duty", "European Commission, Implementing "
             "Regulation (EU) 2024/2754 of 29 October 2024, Article 1(2)", EU, "from 2024-10-30", "official")


def caam(key, value, unit, definition, fact, url=XH26, who="Xinhua, 14 January 2026"):
    return r(key, value, unit, definition, f"China Association of Automobile Manufacturers (CAAM), as reported by {who}",
             url, fact, "press", note="CAAM's own release is not machine-readable on its site; the figures are CAAM's, "
             "quoted by the state news agency")


add(
    # Highland Park
    ford("ford.line.year", 1913, "year", "'Along about April 1, 1913, we first tried the experiment of an assembly "
         "line. We tried it on assembling the fly-wheel magneto.'"),
    ford("ford.magneto.before", 20, "minutes", "time for one workman to assemble a fly-wheel magneto before the line "
         "('thirty-five to forty pieces in a nine-hour day, or about twenty minutes to an assembly')"),
    ford("ford.magneto.after", 5, "minutes", "the magneto's assembly time on the line after the speed was settled"),
    ford("ford.chassis.before", 12 + 28 / 60, "hours", "'About the best we had done in stationary chassis assembling "
         "was an average of twelve hours and twenty-eight minutes per chassis'"),
    ford("ford.chassis.rope", 5 + 50 / 60, "hours", "chassis assembly time when drawn by rope and windlass down a line "
         "250 feet long"),
    ford("ford.chassis.line", 1 + 33 / 60, "hours", "chassis assembly time on the elevated line, early 1914 ('one hour "
         "thirty-three minutes')"),
    # Toyota
    r("toyota.parts", 30_000, "parts", "'Cars are made up of some 30,000 parts'", "Toyota Motor Corporation, 'Plant "
      "tours' (stamping, welding, painting, assembly, inspection and shipping)", TOY_TOURS, "current"),
    r("toyota.koromo", 1938, "year", "the year Kiichiro Toyoda introduced chain-conveyor flow production at the Koromo "
      "Plant", "Toyota Motor Corporation, 'Toyota Production System'", TOY_TPS, "1938"),
    tm("tm.china", 1, "flag", "'In China, however, consumer sentiment stayed weak amid a slowdown in the real estate "
       "market and employment concerns, and consumption growth remained sluggish due to continued price stagnation and "
       "intense price competition.'"),
    tm("tm.units", 9_595, "thousand vehicles", "consolidated vehicle unit sales"),
    tm("tm.units.prev", 9_362, "thousand vehicles", "consolidated vehicle unit sales, fiscal 2025",
       fact="fiscal 2025 (to 2025-03-31)"),
    tm("tm.rev", 50_684.9, "yen billion", "sales revenues"),
    tm("tm.op", 3_766.2, "yen billion", "operating income, down 21.5% from fiscal 2025"),
    tm("tm.op.prev", 4_795.5, "yen billion", "operating income, fiscal 2025", fact="fiscal 2025 (to 2025-03-31)"),
    tm("tm.ni", 3_848.0, "yen billion", "net income attributable to Toyota Motor Corporation"),
    tm("tm.tariff", 1_380.0, "yen billion", "the impact of US tariffs on operating income"),
    tm("tm.auto.rev", 45_417.7, "yen billion", "sales revenues of the automotive operations"),
    tm("tm.auto.op", 2_777.0, "yen billion", "operating income of the automotive operations"),
    tm("tm.fs.rev", 4_857.1, "yen billion", "sales revenues of the financial services operations"),
    tm("tm.fs.op", 851.7, "yen billion", "operating income of the financial services operations"),
    # General Motors
    gm("gm.us.sales", 2_853, "thousand vehicles", "GM's total vehicle sales in the United States (17.2% share)"),
    gm("gm.us.share", 17.2, "percent", "GM's share of US vehicle sales"),
    gm("us.industry", 16_631, "thousand vehicles", "US industry vehicle sales (GM's table)"),
    gm("us.cars", 2_719, "thousand vehicles", "US industry sales of cars (GM's table)"),
    gm("us.trucks", 4_592, "thousand vehicles", "US industry sales of trucks (GM's table)"),
    gm("us.crossovers", 9_320, "thousand vehicles", "US industry sales of crossovers (GM's table)"),
    gm("gm.us.cars", 57, "thousand vehicles", "GM's US car sales (2.1% of the segment)"),
    gm("gm.us.trucks", 1_517, "thousand vehicles", "GM's US truck sales (33.0% of the segment)"),
    gm("gm.us.crossovers", 1_280, "thousand vehicles", "GM's US crossover sales (13.7% of the segment)"),
    gm("world.industry", 90_730, "thousand vehicles", "worldwide industry vehicle sales (GM's table)"),
    gm("gm.world.sales", 6_184, "thousand vehicles", "GM's worldwide vehicle sales, joint ventures included"),
    gm("gm.china.share", 7.1, "percent", "GM's share of China's vehicle sales, joint ventures included (2023: 8.4%)"),
    gm("gm.china.share.2023", 8.4, "percent", "GM's share of China's vehicle sales, 2023", fact="2023"),
    gm("gm.gmna.rev", 154_317, "US$ million", "GM North America: total net sales and revenue"),
    gm("gm.gmna.ebit", 10_452, "US$ million", "GM North America: EBIT-adjusted (6.8% margin; 2024: $14,528m)"),
    gm("gm.gmna.wholesale", 3_296, "thousand vehicles", "GM North America: wholesale vehicle sales"),
    gm("gm.gmf.rev", 17_060, "US$ million", "GM Financial: total revenue"),
    gm("gm.gmf.ebt", 2_802, "US$ million", "GM Financial: earnings before income taxes, adjusted"),
    gm("gm.ev_charges", 7.7, "US$ billion", "charges due to GM's 'EV strategic realignment'"),
    gm("gm.tariffs", 3.1, "US$ billion", "increase in material and freight costs due to tariffs"),
    gm("gm.rnd", 8.5, "US$ billion", "research and development expenses (2024: $9.2bn; 2023: $9.9bn)"),
    gm("gm.strike.ebit", 1.1, "US$ billion", "estimated unfavorable impact of the UAW strike on GMNA EBIT-adjusted, "
       "2023", fact="2023", url=GM23, form="10-K 2023"),
    gm("gm.strike.ni", 0.8, "US$ billion", "estimated unfavorable impact of the UAW strike on net income attributable "
       "to stockholders, 2023", fact="2023", url=GM23, form="10-K 2023"),
    gm("uaw.wage.ratify", 11, "percent", "general wage increase on ratification of the 2023 UAW agreement",
       fact="2023-11", url=GM23, form="10-K 2023"),
    gm("uaw.wage.yearly", 3, "percent", "general wage increase in September of 2024, 2025 and 2026",
       fact="2024-2026", url=GM23, form="10-K 2023"),
    gm("uaw.wage.last", 5, "percent", "general wage increase in September 2027", fact="2027", url=GM23,
       form="10-K 2023"),
    gm("uaw.bonus", 5_000, "US$", "lump sum ratification bonus per eligible employee", fact="2023", url=GM23,
       form="10-K 2023"),
    gm("gm.union.us", 46_000, "employees", "GM's US employees represented by unions (46%), mostly by the UAW",
       fact="2023-12-31", url=GM23, form="10-K 2023"),
    # Ford
    fd("f.blue.wholesale", 2_728, "thousand vehicles", "Ford Blue (petrol and hybrid vehicles for retail customers): "
       "wholesale units"),
    fd("f.blue.rev", 101_019, "US$ million", "Ford Blue: revenue"),
    fd("f.blue.ebit", 3_024, "US$ million", "Ford Blue: EBIT (3.0% margin; 2024: $5,269m)"),
    fd("f.e.wholesale", 178, "thousand vehicles", "Ford Model e (electric vehicles): wholesale units (2024: 105)"),
    fd("f.e.wholesale.2024", 105, "thousand vehicles", "Ford Model e: wholesale units, 2024", fact="2024"),
    fd("f.e.rev", 6_670, "US$ million", "Ford Model e: revenue"),
    fd("f.e.ebit", -4_806, "US$ million", "Ford Model e: EBIT (margin -72.1%)"),
    fd("f.e.ebit.2024", -5_105, "US$ million", "Ford Model e: EBIT, 2024", fact="2024"),
    fd("f.pro.wholesale", 1_488, "thousand vehicles", "Ford Pro (commercial, government and rental customers): "
       "wholesale units"),
    fd("f.pro.rev", 66_286, "US$ million", "Ford Pro: revenue"),
    fd("f.pro.ebit", 6_843, "US$ million", "Ford Pro: EBIT (10.3% margin; 2024: $9,007m)"),
    fd("f.credit.ebt", 2_557, "US$ million", "Ford Credit: earnings before taxes"),
    fd("f.ev_impairment", 10_657, "US$ million", "special item: Model e asset impairment and EV program cancellations"),
    fd("f.uaw", 59_000, "employees", "Ford's US employees covered by the 2023 UAW agreement", fact="2023",
       url=F23, form="10-K 2023"),
    # Tesla
    k("tsla.plan.units", 500_000, "vehicles", "'we have decided to advance our 500,000 total unit build plan (combined "
      "for Model S, Model X, and Model 3) to 2018, two years earlier than previously planned'", "Tesla Motors, First "
      "Quarter 2016 Update (Form 8-K, Exhibit 99.1, filed 2016-05-04)", "8-K", TSLA16, "2016-05-04"),
    k("tsla.prod.2018", 254_530, "vehicles", "total production, 2018 (deliveries 245,506)", "Tesla", "10-K 2018",
      TSLA18, "2018"),
    k("tsla.prod.2020", 509_737, "vehicles", "vehicles produced, 2020 (deliveries 499,647)", "Tesla", "10-K 2020",
      TSLA20, "2020"),
    k("tsla.prod.2025", 1.66, "million vehicles", "'In 2025, we produced approximately 1.66 million consumer vehicles "
      "and delivered approximately 1.64 million'", "Tesla", "10-K 2025", TSLA25, "2025"),
    k("tsla.deliv.2025", 1.64, "million vehicles", "consumer vehicles delivered, 2025", "Tesla", "10-K 2025", TSLA25,
      "2025"),
    k("tsla.auto.gm", 17.8, "percent", "gross margin for total automotive (2024: 18.4%)", "Tesla", "10-K 2025", TSLA25,
      "2025"),
    k("tsla.credits", 1_993, "US$ million", "automotive regulatory credits revenue (2024: $2,763m)", "Tesla",
      "10-K 2025", TSLA25, "2025"),
    # the newcomers
    k("rivn.prod", 42_284, "vehicles", "vehicles produced, 2025", "Rivian Automotive", "10-K 2025", RIVN25, "2025"),
    k("rivn.deliv", 42_247, "vehicles", "vehicles delivered, 2025", "Rivian Automotive", "10-K 2025", RIVN25, "2025"),
    k("rivn.capacity", 215_000, "vehicles a year", "the Normal Factory's capacity after its 2025 paint shop upgrade "
      "('up to 215,000 vehicles annually when the equipment is operated at full rate and on multiple shifts')",
      "Rivian Automotive", "10-K 2025", RIVN25, "2025"),
    k("lcid.prod", 18_378, "vehicles", "vehicles produced, 2025", "Lucid Group, production and delivery release (Form "
      "8-K, Exhibit 99.1, 2026-01-05)", "8-K", LCID_PR, "2025"),
    k("lcid.deliv", 15_841, "vehicles", "vehicles delivered, 2025", "Lucid Group, production and delivery release "
      "(Form 8-K, Exhibit 99.1, 2026-01-05)", "8-K", LCID_PR, "2025"),
    k("lcid.capacity", 90_000, "vehicles a year", "installed capacity at AMP-1, Casa Grande, Arizona", "Lucid Group",
      "10-K 2025", LCID25, "2024-2025"),
    # Europe's groups
    k("stla.ship", 5_484, "thousand vehicles", "consolidated shipments", "Stellantis", "20-F 2025", STLA25, "2025"),
    k("stla.rev", 153.5, "euro billion", "net revenues", "Stellantis", "20-F 2025", STLA25, "2025"),
    k("stla.loss", -22.3, "euro billion", "net loss", "Stellantis", "20-F 2025", STLA25, "2025"),
    k("stla.charges", 18.803, "euro billion", "charges from the reassessment of its electrification strategy: platform "
      "impairments (6.6), product plan realignments and program cancellations (9.1), battery joint ventures (2.1), the "
      "hydrogen fuel cell program (1.1)", "Stellantis", "20-F 2025", STLA25, "2025"),
    k("stla.merger", 2021, "year", "'On January 16, 2021, PSA merged with and into FCA': Stellantis 'is the result of "
      "the merger of FCA and PSA'; its brands include Abarth, Alfa Romeo, Chrysler, Citroen, Dodge, DS, FIAT, Jeep, "
      "Lancia, Maserati, Opel, Peugeot and Ram", "Stellantis", "20-F 2025", STLA25, "2021-01-16"),
    k("race.ship", 13_640, "cars", "total shipments (2024: 13,752)", "Ferrari", "20-F 2025", RACE25, "2025"),
    r("vw.units", 9_022, "thousand vehicles", "vehicle sales, Chinese joint ventures included", "Volkswagen Group, "
      "Annual Report 2025, Five-Year Review", VW25, "2025"),
    r("vw.rev", 321_913, "euro million", "sales revenue", "Volkswagen Group, Annual Report 2025, Five-Year Review",
      VW25, "2025"),
    r("vw.op", 8_868, "euro million", "operating result (2024: 19,060)", "Volkswagen Group, Annual Report 2025, "
      "Five-Year Review", VW25, "2025"),
    r("vw.op.2024", 19_060, "euro million", "operating result, 2024", "Volkswagen Group, Annual Report 2025, "
      "Five-Year Review", VW25, "2024"),
    r("vw.eat", 6_904, "euro million", "earnings after tax", "Volkswagen Group, Annual Report 2025, Five-Year Review",
      VW25, "2025"),
    r("vw.staff", 667, "thousand employees", "employees, yearly average", "Volkswagen Group, Annual Report 2025, "
      "Five-Year Review", VW25, "2025"),
    # Honda
    hmc("hmc.auto.units", 2_711, "thousand vehicles", "consolidated unit sales of automobiles"),
    hmc("hmc.auto.rev", 13_863.3, "yen billion", "Automobile business: sales revenue from external customers"),
    hmc("hmc.auto.op", -1_411.1, "yen billion", "Automobile business: operating loss ('due mainly to the impact of "
        "EV-related losses as well as tariff impacts')"),
    hmc("hmc.moto.units", 14_673, "thousand units", "consolidated unit sales of motorcycles, ATVs and side-by-sides"),
    hmc("hmc.moto.rev", 4_018.8, "yen billion", "Motorcycle business: sales revenue from external customers"),
    hmc("hmc.moto.op", 731.9, "yen billion", "Motorcycle business: operating profit"),
    hmc("hmc.fs.op", 275.5, "yen billion", "Financial services business: operating profit"),
    hmc("hmc.op", -414.3, "yen billion", "group operating loss"),
    hmc("hmc.rev", 21_796.6, "yen billion", "consolidated sales revenue"),
    hmc("hmc.ni", -423.9, "yen billion", "loss for the year attributable to owners of the parent"),
    hmc("hmc.rev.prev", 21_688.7, "yen billion", "consolidated sales revenue, fiscal 2025", fact="fiscal 2025"),
    hmc("hmc.ni.prev", 835.8, "yen billion", "profit attributable to owners of the parent, fiscal 2025",
        fact="fiscal 2025"),
    # BYD
    r("byd.rev", 803_964.958, "RMB million", "revenue", "BYD Company, 2025 Annual Results Announcement (HKEX, 27 March "
      "2026)", BYD25, "2025"),
    r("byd.gp", 142_659.797, "RMB million", "gross profit", "BYD Company, 2025 Annual Results Announcement", BYD25,
      "2025"),
    r("byd.profit", 32_619.022, "RMB million", "profit attributable to owners of the parent (2024: 40,254)", "BYD "
      "Company, 2025 Annual Results Announcement", BYD25, "2025"),
    r("byd.profit.2024", 40_254.346, "RMB million", "profit attributable to owners of the parent, 2024", "BYD Company, "
      "2025 Annual Results Announcement", BYD25, "2024"),
    r("byd.nev", 4.60, "million vehicles", "annual sales of new energy vehicles (preliminary, 'quick report')", "BYD "
      "Company, 2025 Annual Results Announcement, chairman's statement", BYD25, "2025"),
    r("byd.export", 1.05, "million vehicles", "overseas export volume of new energy vehicles (preliminary)", "BYD "
      "Company, 2025 Annual Results Announcement, chairman's statement", BYD25, "2025"),
    r("byd.rnd", 63.4, "RMB billion", "R&D investment", "BYD Company, 2025 Annual Results Announcement, chairman's "
      "statement", BYD25, "2025"),
    # the dealer
    an("an.stores", 245, "stores", "'one of the largest automotive retailers in the United States': 323 new vehicle "
       "franchises from 245 stores at 31 December 2025", fact="2025-12-31"),
    an("an.rev.new", 13_501.3, "US$ million", "revenue: new vehicles"),
    an("an.rev.used", 7_814.0, "US$ million", "revenue: used vehicles"),
    an("an.rev.fi", 1_464.4, "US$ million", "revenue: finance and insurance, net"),
    an("an.rev.ps", 4_835.4, "US$ million", "revenue: parts and service"),
    an("an.gp.new", 664.8, "US$ million", "gross profit: new vehicles"),
    an("an.gp.used", 462.6, "US$ million", "gross profit: used vehicles"),
    an("an.gp.fi", 1_464.4, "US$ million", "gross profit: finance and insurance"),
    an("an.gp.ps", 2_355.1, "US$ million", "gross profit: parts and service"),
    an("an.new.units", 259_264, "vehicles", "new vehicles retailed"),
    an("an.new.price", 52_075, "US$", "average revenue per new vehicle retailed"),
    an("an.new.gp", 2_564, "US$", "gross profit per new vehicle retailed"),
    an("an.new.gp.2023", 4_342, "US$", "gross profit per new vehicle retailed, 2023", fact="2023"),
    an("an.new.gp.2024", 3_045, "US$", "gross profit per new vehicle retailed, 2024", fact="2024"),
    an("an.fi.per", 2_769, "US$", "finance and insurance gross profit per vehicle retailed"),
    k("lcid.dealer_law", 1, "flag", "'state laws regulate the manufacture, distribution, sale and service of "
      "automobiles, and generally require motor vehicle manufacturers and dealers to be licensed in order to sell "
      "vehicles directly to residents. Certain states do not permit automobile manufacturers to be licensed as dealers'",
      "Lucid Group", "10-K 2025", LCID25, "2025"),
    # China
    r("cn.plan17.nev2020", 2.0, "million vehicles", "target: '到2020年，新能源汽车年产销达到200万辆' (new energy vehicle "
      "production and sales of 2 million a year by 2020)", "Ministry of Industry and Information Technology, NDRC and "
      "Ministry of Science and Technology, 汽车产业中长期发展规划 (Medium- and Long-Term Development Plan for the "
      "Automobile Industry), 工信部联装〔2017〕53号, 6 April 2017", CN17, "2017-04-06", "official"),
    r("cn.plan17.share2025", 20, "percent", "target: '到2025年，新能源汽车占汽车产销20%以上' (new energy vehicles above 20% "
      "of vehicle production and sales by 2025)", "MIIT, NDRC and MOST, Medium- and Long-Term Development Plan for the "
      "Automobile Industry, 6 April 2017", CN17, "2017-04-06", "official"),
    r("cn.plan20.share2025", 20, "percent", "goal: new energy vehicles 'about 20%' of new vehicle sales by 2025",
      "General Office of the State Council, 新能源汽车产业发展规划（2021—2035年）, 国办发〔2020〕39号, 20 October 2020", CN20,
      "2020-10-20", "official"),
    caam("caam.2020.nev", 1.367, "million vehicles", "new energy vehicle sales in China, 2020 (production 1.366m)",
         "2020", url=CS21, who="the China Securities Journal, 13 January 2021"),
    caam("caam.2020.total", 25.311, "million vehicles", "vehicle sales in China, 2020", "2020", url=CS21,
         who="the China Securities Journal, 13 January 2021"),
    caam("caam.2025.total", 34.40, "million vehicles", "vehicle sales in China, 2025 (production 34.531m)", "2025"),
    caam("caam.2025.nev", 16.49, "million vehicles", "new energy vehicle sales in China, 2025 (47.9% of new vehicle "
         "sales; above 50% of domestic sales)", "2025"),
    caam("caam.2025.export", 7.0, "million vehicles", "vehicle exports from China, 2025 ('over 7 million'; new energy "
         "vehicles 2.615 million)", "2025"),
    caam("caam.2025.nev_export", 2.615, "million vehicles", "new energy vehicle exports from China, 2025", "2025"),
    # the tariffs
    r("ustr.ev", 100, "percent", "Section 301 duty on electric vehicles from China: 'Electric vehicles—Increase rate "
      "to 100% in 2024', effective for goods entered on or after 27 September 2024", "Office of the US Trade "
      "Representative, Notice of Modification, 89 FR 76581, 18 September 2024", USTR, "2024-09-27", "official"),
    eu("eu.cvd.byd", 17.0, "the BYD Group"),
    eu("eu.cvd.geely", 18.8, "the Geely Group"),
    eu("eu.cvd.saic", 35.3, "the SAIC Group"),
    eu("eu.cvd.tesla", 7.8, "Tesla (Shanghai)"),
    eu("eu.cvd.other", 20.7, "other cooperating companies"),
)
