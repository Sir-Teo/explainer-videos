"""Register rows for Part 14, *Water and Waste*.  Checked 2026-11-27.

Hansard for July and August 1858 and for 16 June 2026; the EPA's Solid Waste Dilemma (1989), its MSW Facts and
Figures for 2009, its Historic Tipping Fees (2015), its drinking water and clean watersheds needs surveys and its
count of public water systems; 40 CFR Part 258 (1991); Waste Management's Forms 10-K for 2018 and 2025, Republic
Services' and American Water's Forms 10-K for 2025, Sabesp's Form 20-F for 2025 and Veolia's ESEF annual report for
2024; the Independent Water Commission's final report (July 2025); the CMA's PR24 redeterminations (March 2026);
GOV.UK on the Thames Tideway Tunnel.  Series are the Filing Room's BLS, FRED, EPA, World Bank and SEC extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (14,)
HANS = "https://api.parliament.uk/historic-hansard/commons/1858/jul/15/first-reading"
HANS_AUG = "https://api.parliament.uk/historic-hansard/lords/1858/aug/02/speech-of-the-lords-commissioners"
HANS26 = "https://hansard.parliament.uk/commons/2026-06-16/debates/6ED8138C-6701-4E39-A5ED-8747A1EE1FA9/ThamesWater"
TIDEWAY = "https://www.gov.uk/government/publications/thames-tideway-tunnel-government-support-package-contract-documents"
EPA89 = "https://permanent.fdlp.gov/lps77733/33564.pdf"
EPA09 = "https://archive.epa.gov/epawaste/nonhaz/municipal/web/pdf/msw2009rpt.pdf"
EPATIP = ("https://www.epa.gov/sites/default/files/2015-12/documents/historic_tipping_fees_and_commodity_values_"
          "02062015_508.pdf")
DWINSA = "https://www.epa.gov/dwsrf/epas-7th-drinking-water-infrastructure-needs-survey-and-assessment"
CWNS = "https://www.epa.gov/cwns"
PWS = "https://www.epa.gov/dwreginfo/information-about-public-water-systems"
CFR258 = "https://www.ecfr.gov/current/title-40/chapter-I/subchapter-I/part-258"
WM = "https://www.sec.gov/Archives/edgar/data/823768/000110465926012049/wm-20251231x10k.htm"
WM18 = "https://www.sec.gov/Archives/edgar/data/823768/000155837019000662/wm-20181231x10k.htm"
RSG = "https://www.sec.gov/Archives/edgar/data/1060391/000106039126000094/rsg-20251231.htm"
AWK = "https://www.sec.gov/Archives/edgar/data/1410636/000141063626000034/awk-20251231.htm"
SBS = "https://www.sec.gov/Archives/edgar/data/1170858/000129281426002681/sbsform20f_2025.htm"
VEO = "https://filings.xbrl.org/969500LENY69X51OOT31/2024-12-31/ESEF/FR/0/veolia-2024-12-31-1-fr.json"
IWC = ("https://assets.publishing.service.gov.uk/media/687dfcc4312ee8a5f0806be6/"
       "Independent_Water_Commission_-_Final_Report_-_21_July.pdf")
CLH = "https://www.sec.gov/Archives/edgar/data/822818/000082281826000009/clh-20251231.htm"
CMA = "https://assets.publishing.service.gov.uk/media/69afb3e2917847c0a4c89a23/PR24_Final_determinations_summary.pdf"


def r(key, value, unit, definition, source, url, fact, kind="official", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def wm(key, value, unit, definition, fact="2025", **kw):
    return r(key, value, unit, definition, "Waste Management, Inc., Form 10-K 2025", WM, fact, "filing", **kw)


def rsg(key, value, unit, definition, fact="2025", **kw):
    return r(key, value, unit, definition, "Republic Services, Inc., Form 10-K 2025", RSG, fact, "filing", **kw)


def awk(key, value, unit, definition, fact="2025", **kw):
    return r(key, value, unit, definition, "American Water Works Company, Inc., Form 10-K 2025", AWK, fact, "filing",
             **kw)


def sbs(key, value, unit, definition, fact="2025", **kw):
    return r(key, value, unit, definition, "Companhia de Saneamento Básico do Estado de São Paulo (Sabesp), Form 20-F "
             "2025", SBS, fact, "filing", **kw)


def iwc(key, value, unit, definition, fact="2025", **kw):
    return r(key, value, unit, definition, "Independent Water Commission (Sir Jon Cunliffe), Final Report, 21 July "
             "2025", IWC, fact, **kw)


def cma(key, value, unit, definition, fact="PR24, 2025-30", **kw):
    return r(key, value, unit, definition, "Competition and Markets Authority, Water PR24 price redeterminations: "
             "final determinations summary (March 2026)", CMA, fact, **kw)


add(
    # the Great Stink
    r("stink.cost", 3.0, "£ million", "Disraeli's estimate of the cost of the main drainage of the metropolis ('cannot, "
      "indeed, be computed at much less than £3,000,000')", "Hansard, HC Deb 15 July 1858 vol 151 cc1508-40 "
      "(Metropolis Local Management Act Amendment Bill)", HANS, "1858-07-15", "official"),
    r("stink.rate", 3, "pence in the pound", "the rate Disraeli proposed to pay for it ('not more than 3d. in the "
      "pound')", "Hansard, HC Deb 15 July 1858 vol 151 cc1508-40", HANS, "1858-07-15"),
    r("stink.years", 40, "years", "the term of the rate ('levied for a term of forty years')", "Hansard, HC Deb 15 July "
      "1858 vol 151 cc1508-40", HANS, "1858-07-15"),
    r("stink.days", 18, "days", "from Disraeli's motion for leave to bring in the bill (15 July 1858) to the Lords "
      "Commissioners' speech announcing royal assent to 'the Act ... for the Purification of that noble River' "
      "(2 August 1858)", "Hansard, HC Deb 15 July 1858; HL Deb 2 August 1858 vol 151 cc2317-20", HANS_AUG,
      "1858-07-15 to 1858-08-02"),
    r("tideway.licence", 2015, "year", "the year Ofwat awarded the project licence to design, build, finance, operate "
      "and maintain the Thames Tideway Tunnel to Bazalgette Tunnel Limited (24 August 2015)", "GOV.UK, Thames Tideway "
      "Tunnel: government support package contract documents (updated 1 July 2026)", TIDEWAY, "2015-08-24"),
    # the EPA's 1989 forecast and what followed
    r("epa89.tons", 160, "million tons", "municipal solid waste generated 'last year' (1988)", "US EPA, The Solid "
      "Waste Dilemma: An Agenda for Action (EPA/530-SW-89-019, February 1989)", EPA89, "1988"),
    r("epa89.tons2000", 190, "million tons", "the EPA's projection for 2000", "US EPA, The Solid Waste Dilemma (1989)",
      EPA89, "2000 projection"),
    r("epa89.landfilled", 80, "%", "share of garbage landfilled ('Eighty percent of garbage is landfilled')",
      "US EPA, The Solid Waste Dilemma (1989)", EPA89, "1988"),
    r("epa89.recycled", 10, "%", "share of the nation's waste managed by recycling", "US EPA, The Solid Waste Dilemma "
      "(1989)", EPA89, "1988"),
    r("epa89.full", 33.3, "% of landfills", "'One-third of the nation's landfills will be full by 1991'", "US EPA, The "
      "Solid Waste Dilemma (1989)", EPA89, "forecast for 1991"),
    r("epa.landfills.1988", 7924, "landfills", "municipal solid waste landfills in the United States", "US EPA, "
      "Municipal Solid Waste in the United States: 2009 Facts and Figures (EPA530-R-10-012), Figure ES-5", EPA09,
      "1988"),
    r("epa.landfills.2009", 1908, "landfills", "municipal solid waste landfills reported in the United States",
      "US EPA, MSW in the United States: 2009 Facts and Figures, Table 28", EPA09, "2009"),
    r("epa.tip.1982", 19.48, "$ a ton (2013 dollars)", "national average landfill tipping fee (NSWMA data)", "US EPA, "
      "Historic Tipping Fees and Commodity Values (February 2015), Figure 1", EPATIP, "1982"),
    r("epa.tip.1985", 17.75, "$ a ton (2013 dollars)", "national average landfill tipping fee, the series' low",
      "US EPA, Historic Tipping Fees and Commodity Values (2015), Figure 1", EPATIP, "1985"),
    r("epa.tip.1995", 49.21, "$ a ton (2013 dollars)", "national average landfill tipping fee, after the rise of "
      "1985-1995", "US EPA, Historic Tipping Fees and Commodity Values (2015), Figure 1", EPATIP, "1995"),
    r("epa.tip.2013", 49.78, "$ a ton (2013 dollars)", "national average landfill tipping fee", "US EPA, Historic "
      "Tipping Fees and Commodity Values (2015), Figure 1", EPATIP, "2013"),
    # the 1991 landfill rule
    r("cfr.liner", 60, "mil", "minimum thickness of an HDPE membrane in the composite liner of a new landfill unit "
      "(over at least two feet of compacted soil with hydraulic conductivity of no more than 1e-7 cm/s)", "40 CFR "
      "258.40(b) (56 FR 51016, 9 October 1991)", CFR258, "1991"),
    r("cfr.clay", 2, "feet", "minimum compacted soil layer beneath the membrane of a composite liner", "40 CFR "
      "258.40(b)", CFR258, "1991"),
    r("cfr.leachate", 30, "cm", "maximum depth of leachate over the liner the collection system must maintain",
      "40 CFR 258.40(a)(2)", CFR258, "1991"),
    r("cfr.postclosure", 30, "years", "post-closure care required after a landfill unit closes", "40 CFR 258.61(a)",
      CFR258, "1991"),
    # America's water systems
    r("epa.dw.need", 625, "$ billion", "drinking water systems' infrastructure needs over 20 years", "US EPA, 7th "
      "Drinking Water Infrastructure Needs Survey and Assessment (2023)", DWINSA, "2021-2040"),
    r("epa.dw.dist", 422.9, "$ billion", "of which distribution and transmission: replacing or rehabilitating pipes",
      "US EPA, 7th DWINSA (2023)", DWINSA, "2021-2040"),
    r("epa.dw.treat", 107, "$ billion", "of which treatment", "US EPA, 7th DWINSA (2023)", DWINSA, "2021-2040"),
    r("epa.dw.storage", 56.1, "$ billion", "of which storage", "US EPA, 7th DWINSA (2023)", DWINSA, "2021-2040"),
    r("epa.dw.source", 25.2, "$ billion", "of which source (intakes, wells, water rights)", "US EPA, 7th DWINSA (2023)",
      DWINSA, "2021-2040"),
    r("epa.dw.lead", 4, "million", "lead service lines estimated still in use", "US EPA, 7th DWINSA, lead service "
      "line information (2023 update)", DWINSA, "2023"),
    r("epa.cw.need", 630.1, "$ billion", "clean water (wastewater and stormwater) needs reported over 20 years",
      "US EPA, Clean Watersheds Needs Survey 2022", CWNS, "2022"),
    r("epa.potw", 17544, "plants", "publicly owned treatment works reported", "US EPA, CWNS 2022", CWNS, "2022"),
    r("epa.potw_pop", 270.4, "million people", "population served by publicly owned treatment works", "US EPA, CWNS "
      "2022", CWNS, "2022"),
    r("epa.pws", 148000, "systems", "public water systems in the United States ('over 148,000')", "US EPA, Information "
      "about Public Water Systems", PWS, "2026"),
    # Waste Management
    wm("wm.landfills", 257, "landfills", "landfills owned or operated (253 solid waste, 4 hazardous)"),
    wm("wm.life.0_5", 24, "landfills", "landfills with 0-5 years of remaining permitted and expansion airspace"),
    wm("wm.life.6_10", 23, "landfills", "landfills with 6-10 years"),
    wm("wm.life.11_20", 55, "landfills", "landfills with 11-20 years"),
    wm("wm.life.21_40", 61, "landfills", "landfills with 21-40 years"),
    wm("wm.life.41", 94, "landfills", "landfills with more than 40 years"),
    wm("wm.life_avg", 38, "years", "weighted average remaining life of its landfills on permitted airspace (about 39 "
       "with expansion airspace)"),
    wm("wm.transfer", 342, "stations", "transfer stations"),
    wm("wm.mrf", 113, "facilities", "recycling facilities"),
    wm("wm.rev.collection", 15.421, "$ billion", "net revenue from collection (commercial, industrial, residential, "
       "other)"),
    wm("wm.rev.commercial", 5.630, "$ billion", "net revenue from commercial collection"),
    wm("wm.rev.industrial", 3.106, "$ billion", "net revenue from industrial collection"),
    wm("wm.rev.residential", 3.510, "$ billion", "net revenue from residential collection"),
    wm("wm.rev.landfill", 3.781, "$ billion", "net revenue from landfills (after its own trucks' tipping fees)"),
    wm("wm.rev.landfill_gross", 5.347, "$ billion", "gross landfill revenue, including 1.566 paid by its own "
       "collection operations"),
    wm("wm.rev.transfer", 1.502, "$ billion", "net revenue from transfer stations"),
    wm("wm.rev.recycling", 1.492, "$ billion", "net revenue from recycling processing and sales"),
    wm("wm.rev.energy", 0.478, "$ billion", "net revenue from renewable energy (landfill gas)"),
    wm("wm.rev.health", 2.508, "$ billion", "net revenue from Healthcare Solutions (medical waste, acquired with "
       "Stericycle in November 2024)"),
    wm("wm.rev.total", 25.204, "$ billion", "total net operating revenue"),
    wm("wm.depletion", 6.96, "$ a ton", "average landfill airspace depletion expense per ton received ($6.36 in "
       "2024)"),
    wm("wm.tons", 129, "million tons", "tons received at its landfills, net of redirected waste"),
    r("wm18.china", 2018, "year", "China's ban on certain imported materials, including mixed waste paper and mixed "
      "plastics, effective 1 January 2018 (announced in 2017)", "Waste Management, Inc., Form 10-K 2018", WM18,
      "2018-01-01", "filing"),
    # Republic
    rsg("rsg.landfills", 207, "landfills", "active landfills"),
    rsg("rsg.air.2024", 4745, "million cubic yards", "permitted airspace, 31 December 2024"),
    rsg("rsg.air.2025", 4872, "million cubic yards", "permitted airspace, 31 December 2025"),
    rsg("rsg.air.used", 86, "million cubic yards", "airspace consumed in 2025 (87 in 2024)"),
    rsg("rsg.air.permits", 145, "million cubic yards", "permits granted (net of closures) added in 2025"),
    rsg("rsg.air.acq", 71, "million cubic yards", "airspace added by landfills acquired, net of divestitures, 2025"),
    rsg("rsg.air.total", 5027, "million cubic yards", "permitted plus probable expansion airspace, end-2024 and "
        "end-2025 alike"),
    rsg("rsg.internal", 67, "%", "share of the solid waste it collected that went to landfills it owns or operates "
        "(internalization), 2024 and 2025"),
    rsg("rsg.recy.2025", 135, "$ a ton", "average price of its recycled commodities, excluding glass and organics"),
    rsg("rsg.recy.2024", 164, "$ a ton", "the same, 2024", fact="2024"),
    rsg("rsg.recy.sens", 13, "$ million", "change in annual revenue and operating income from a $10 a ton change in "
        "recycled commodity prices"),
    # American Water
    awk("awk.people", 14, "million people", "people served with drinking water, wastewater and related services"),
    awk("awk.states", 24, "states", "states served"),
    awk("awk.mains", 55000, "miles", "transmission, distribution and collection mains and pipes"),
    awk("awk.capex10", 47, "$ billion", "planned capital investment over the next ten years", lo=46, hi=48),
    awk("awk.ky.roe", 9.70, "%", "authorized return on equity in its Kentucky subsidiary's 2025 rate case"),
    awk("awk.ky.rb", 667, "$ million", "authorized rate base in the same case"),
    awk("awk.ky.eq", 52.26, "%", "common equity in the authorized capital structure"),
    # Sabesp
    sbs("sbs.state.before", 50.26, "%", "the State of São Paulo's interest in Sabesp before its privatization",
        fact="2024-07-22"),
    sbs("sbs.state.after", 18.00, "%", "the State's interest after the secondary offering of 22 July 2024",
        fact="2024-07-22"),
    sbs("sbs.water", 29.9, "million people", "people provided with water services"),
    sbs("sbs.sewer", 27.0, "million people", "people provided with sewage services"),
    sbs("sbs.capex.2023", 6.3, "R$ billion", "investment", fact="2023"),
    sbs("sbs.capex.2024", 6.9, "R$ billion", "investment", fact="2024"),
    sbs("sbs.capex.2025", 15.2, "R$ billion", "investment"),
    sbs("sbs.plan", 70, "R$ billion", "investment anticipated from 2024 to 2029"),
    sbs("sbs.target", 2029, "year", "year by which 99% of the population must have drinking water and 90% sewage "
        "collection and treatment (brought forward from 2033)", fact="concession of 2024"),
    # Veolia
    r("veo.rev.2024", 44.692, "€ billion", "revenue from contracts with customers", "Veolia Environnement, document "
      "d'enregistrement universel 2024 (ESEF)", VEO, "2024", "filing"),
    r("veo.ebit.2024", 2.881, "€ billion", "operating income", "Veolia Environnement, ESEF annual report 2024", VEO,
      "2024", "filing"),
    # England
    iwc("iwc.wascs", 10, "companies", "water and sewerage companies listed at privatization in 1989", fact="1989"),
    iwc("iwc.listed", 3, "companies", "water and sewerage companies still listed (7 privately owned, 1 not for "
        "profit)"),
    iwc("iwc.wocs.1989", 29, "companies", "water-only companies at privatization", fact="1989"),
    iwc("iwc.wocs.2025", 5, "companies", "water-only companies today"),
    iwc("iwc.gear.1991", 4, "%", "average gearing of the water and sewerage companies", fact="1991"),
    iwc("iwc.gear.2009", 72, "%", "average gearing of the water and sewerage companies", fact="2009"),
    iwc("iwc.roe", 5.1, "% real", "Ofwat's allowed return on equity at PR24, at 55% notional gearing (7.2% nominal "
        "with 2% inflation)", fact="PR24 final determination"),
    iwc("iwc.wacc19", 2.96, "% real", "allowed weighted average cost of capital, PR19", fact="PR19"),
    iwc("iwc.wacc24", 4.03, "% real", "allowed weighted average cost of capital, PR24", fact="PR24"),
    iwc("iwc.wacc_bill", 43, "£ a year", "rise in the average bill from 2024/25 to 2025/26 due to the higher allowed "
        "return (about a third of the rise)", fact="2025/26"),
    iwc("iwc.bill", 603, "£ a year", "average water and sewerage bill in England and Wales (Water UK)",
        fact="2025/26"),
    iwc("iwc.enh", 44, "£ billion", "enhancement expenditure in the 2025-30 plans"),
    iwc("iwc.equity", 10, "£ billion", "new equity the companies need to finance it", lo=7, hi=13),
    iwc("iwc.thames.debt", 16.8, "£ billion", "Thames Water's debt when Ofwat penalized its PR24 business plan"),
    iwc("iwc.thames.penalty", 141, "£ million", "the penalty (0.3 percentage points on its return)"),
    cma("cma.allow.pr24", 104, "£ billion (2022/23 prices)", "Ofwat's PR24 expenditure allowances for the sector, "
        "2025-30"),
    cma("cma.allow.pr19", 62, "£ billion (2022/23 prices)", "the same in PR19, 2020-25", fact="PR19, 2020-25"),
    cma("cma.bill_rise", 31, "£ a year", "Ofwat's PR24: industry average increase in annual bills of £31 per year "
        "(before inflation) between 2024/25 and 2029/30"),
    cma("cma.wacc", 4.20, "% real", "the CMA's allowed rate of return for the five disputing companies (Ofwat: "
        "4.03%)"),
    cma("cma.roe", 5.70, "% real", "the CMA's allowed return on equity (Ofwat: 5.10%)"),
    cma("cma.debt", 2.97, "% real", "the CMA's allowed cost of debt (Ofwat: 3.15%)"),
    r("thames.customers", 16, "million", "Thames Water's customers", "Hansard, HC Deb 16 June 2026, Thames Water "
      "(statement by the Secretary of State for Environment, Food and Rural Affairs)", HANS26, "2026-06-16"),
    wm("wm.contract_life", 4, "years", "weighted average remaining life of its collection and recycling contracts, "
       "whose variable elements include annual rate changes based on the consumer price index, fuel prices or other "
       "operating costs"),
    r("clh.incinerators", 10, "incinerators", "commercial hazardous waste incinerators it operates (the newest at "
      "Kimball, Nebraska, from late 2024)", "Clean Harbors, Inc., Form 10-K 2025", CLH, "2025", "filing"),
    r("clh.landfills", 7, "landfills", "commercial landfills in the US and Canada, six of them for hazardous waste",
      "Clean Harbors, Inc., Form 10-K 2025", CLH, "2025", "filing"),
    r("clh.airspace", 33.0, "million cubic yards", "remaining capacity of its six commercial hazardous waste "
      "landfills", "Clean Harbors, Inc., Form 10-K 2025", CLH, "2025-12-31", "filing"),
    r("clh.facilities", 100, "facilities", "waste disposal facilities in its network ('over 100')", "Clean Harbors, "
      "Inc., Form 10-K 2025", CLH, "2025", "filing"),
    iwc("iwc.rcv", 103, "£ billion (nominal)", "the regulatory capital value of the water companies of England and "
        "Wales, 2024/25 (from Ofwat's RCV updates)", fact="2024/25"),
    r("bls.water.ytd2026", 4.91, "%", "CPI-U water and sewerage maintenance, US city average, not seasonally adjusted: "
      "January-September 2026 average over January-September 2025 (October 2025 was not collected)", "BLS, CPI flat "
      "file cu.data.12.USHousing (series CUUR0000SEHG01)", "https://download.bls.gov/pub/time.series/cu/cu.data.12.USHousing",
      "2026-01 to 2026-09"),
    awk("awk.quality5", 4.1, "$ billion", "capital expenditure over the next five years to address water quality "
        "issues, most of it for compliance with environmental laws and regulations"),
    awk("awk.quality26", 0.788, "$ billion", "the same, in 2026", fact="2026 plan"),
    awk("awk.pfas_deadline", 2029, "year", "under the current rule, utilities must comply with the PFAS maximum contaminant "
        "levels by April 2029; the EPA has indicated its intent to extend the deadline to 2031", fact="2025"),
)
