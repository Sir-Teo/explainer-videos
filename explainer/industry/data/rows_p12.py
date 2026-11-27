"""Register rows for Part 12, *Chemicals*.  Checked 2026-11-27.

The Nobel Foundation on Haber and Bosch; Haber's 1908 patent (Erisman et al., Nature Geoscience 2008); the USGS's
Mineral Commodity Summaries 2026 (nitrogen, potash); EIA's Today in Energy on ethylene capacity and INEOS Project One,
and its AEO2026 assumptions (cracker yields, in ``works/cracker.py``) and AEO2005 (the Called it?); Forms 10-K of Linde,
Air Products and CF Industries; 8-Ks of 3M and Chemours (PFAS settlements); the EPA's PFAS rule; the Supreme Court of
India's 1989 judgment on Bhopal.  Series are the Filing Room's FRED, EIA, Eurostat, USGS, OWID and SEC extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (12,)
MCS = "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-{}.pdf"
HABER = "https://www.nobelprize.org/prizes/chemistry/1918/haber/facts/"
BOSCH = "https://www.nobelprize.org/prizes/chemistry/1931/bosch/facts/"
ERISMAN = "https://www.nature.com/articles/ngeo325"
TIE_CAP = "https://www.eia.gov/todayinenergy/detail.php?id=48056"
TIE_NGL = "https://www.eia.gov/todayinenergy/detail.php?id=67387"
AEO05 = "https://www.eia.gov/outlooks/archive/aeo05/pdf/0383(2005).pdf"
LIN = "https://www.sec.gov/Archives/edgar/data/1707925/000162828026011430/lin-20251231.htm"
APD = "https://www.sec.gov/Archives/edgar/data/2969/000000296926000050/apd-20260930.htm"
CF = "https://www.sec.gov/Archives/edgar/data/1324404/000132440426000007/cf-20251231.htm"
DOW = "https://www.sec.gov/Archives/edgar/data/1751788/000175178826000018/dow-20251231.htm"
CF23 = "https://www.sec.gov/Archives/edgar/data/1324404/000132440424000008/cf-20231231.htm"
MMM = "https://www.sec.gov/Archives/edgar/data/66740/000006674023000048/mmm-20230622.htm"
CC = "https://www.sec.gov/Archives/edgar/data/1627223/000095017023025888/cc-20230601.htm"
EPA = "https://www.federalregister.gov/documents/2024/04/26/2024-07773/pfas-national-primary-drinking-water-regulation"
SCI = "https://hcraj.nic.in/sci/1988/3-3187-1988_1989-05-04.pdf"


def r(key, value, unit, definition, source, url, fact, kind="official", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def usgs(key, value, unit, definition, chapter, fact="2025", **kw):
    return r(key, value, unit, definition, f"US Geological Survey, Mineral Commodity Summaries 2026 (February 2026), "
             f"'{chapter.title()}'", MCS.format(chapter), fact, **kw)


def filing(key, value, unit, definition, who, url, fact="2025", **kw):
    return r(key, value, unit, definition, f"{who}, Form 10-K", url, fact, "filing", **kw)


add(
    # --- Haber and Bosch ---------------------------------------------------------------------------------------------
    r("haber.prize", 1918, "year", "Fritz Haber, Nobel Prize in Chemistry 1918 'for the synthesis of ammonia from its "
      "elements' (received in 1919)", "The Nobel Foundation, 'Fritz Haber - Facts'", HABER, "1918", "study"),
    r("haber.patent", 1908, "year", "Haber filed his patent on the 'synthesis of ammonia from its elements' on 13 October "
      "1908", "Erisman, Sutton, Galloway, Klimont and Winiwarter, 'How a century of ammonia synthesis changed the world', "
      "Nature Geoscience 1 (2008)", ERISMAN, "1908-10-13", "study"),
    r("bosch.prize", 1931, "year", "Carl Bosch, Nobel Prize in Chemistry 1931 (shared) 'in recognition of their "
      "contributions to the invention and development of chemical high pressure methods'; 'around 1913 Carl Bosch "
      "developed an apparatus' that made Haber's method industrial", "The Nobel Foundation, 'Carl Bosch - Facts'", BOSCH,
      "1931", "study"),
    r("bosch.1913", 1913, "year", "Bosch's industrial apparatus for ammonia, around 1913", "The Nobel Foundation, 'Carl "
      "Bosch - Facts'", BOSCH, "1913", "study"),
    # --- USGS: nitrogen and potash ---------------------------------------------------------------------------------------
    usgs("usgs.n.world.2025", 160000, "thousand tonnes of N", "World ammonia production, 2025 (estimated)", "nitrogen"),
    usgs("usgs.n.china.2025", 49000, "thousand tonnes of N", "China's ammonia production, 2025", "nitrogen"),
    usgs("usgs.n.india.2025", 15000, "thousand tonnes of N", "India's ammonia production, 2025", "nitrogen"),
    usgs("usgs.n.russia.2025", 15000, "thousand tonnes of N", "Russia's ammonia production, 2025", "nitrogen"),
    usgs("usgs.n.us.2025", 14000, "thousand tonnes of N", "US ammonia production, 2025", "nitrogen"),
    usgs("usgs.n.us.plants", 38, "plants", "US ammonia plants, 2025 (18 companies, 19 states)", "nitrogen"),
    usgs("usgs.n.us.fert", 88, "% of production", "Share of US ammonia production used for fertilizer", "nitrogen"),
    usgs("usgs.n.us.gulf", 57, "% of capacity", "Share of US ammonia capacity in Louisiana, Oklahoma and Texas",
         "nitrogen"),
    *[usgs(f"usgs.n.price.{y}", v, "$ a short ton", f"Average US Gulf Coast ammonia price, fob, {y}", "nitrogen", str(y))
      for y, v in ((2021, 578), (2022, 1070), (2023, 470), (2024, 440), (2025, 450))],
    usgs("usgs.potash.canada.2025", 15000, "thousand tonnes of K2O", "Canada's potash mine production, 2025", "potash"),
    usgs("usgs.potash.belarus.2025", 6000, "thousand tonnes of K2O", "Belarus's potash mine production, 2025", "potash"),
    usgs("usgs.potash.china.2025", 6300, "thousand tonnes of K2O", "China's potash mine production, 2025", "potash"),
    usgs("usgs.potash.russia.2025", 10000, "thousand tonnes of K2O", "Russia's potash mine production, 2025 (estimated)",
         "potash"),
    usgs("usgs.potash.world.2025", 49000, "thousand tonnes of K2O", "World potash mine production, 2025 (rounded)",
         "potash"),
    usgs("usgs.potash.us.canada", 79, "% of imports", "Canada's share of US potash imports, 2021-24", "potash", "2021-2024"),
    usgs("usgs.potash.us.imports.2025", 5600, "thousand tonnes of K2O", "US imports of potash, 2025", "potash"),
    usgs("usgs.potash.us.prod.2025", 500, "thousand tonnes of K2O", "US potash production, 2025", "potash"),
    # --- EIA ------------------------------------------------------------------------------------------------------------------
    r("eia.ethylene.cap.2013", 27, "million tonnes a year", "US ethylene capacity, first quarter of 2013, when the first "
      "additions to crackers in over a decade came online", "EIA, Today in Energy, 21 May 2021", TIE_CAP, "2013 Q1"),
    r("eia.ethylene.cap.2020", 40, "million tonnes a year", "US ethylene capacity, 2020 (almost 40)", "EIA, Today in "
      "Energy, 21 May 2021", TIE_CAP, "2020"),
    r("eia.ineos.antwerp", 80, "thousand barrels a day of ethane", "INEOS Project One, Antwerp: slated for the third "
      "quarter of 2026, about 80,000 b/d of (imported US) ethane, 'the largest [cracker] in Europe'", "EIA, Today in "
      "Energy, 30 March 2026", TIE_NGL, "2026"),
    r("aeo05.lng.2025", 6.4, "trillion cubic feet", "AEO2005's projection of US net LNG imports in 2025 (0.4 in 2003)",
      "EIA, Annual Energy Outlook 2005 (February 2005)", AEO05, "2005 projection for 2025", "tracker"),
    r("aeo05.lng.2003", 0.4, "trillion cubic feet", "US net LNG imports, 2003", "EIA, Annual Energy Outlook 2005",
      AEO05, "2003"),
    r("aeo05.bulkchem", 1.0, "% a year", "AEO2005's projected growth of US bulk chemical output, 2003-2025 (1.7% in "
      "AEO2004)", "EIA, Annual Energy Outlook 2005, 'Changing Trends in the Bulk Chemicals and Pulp and Paper "
      "Industries'", AEO05, "2005 projection", "tracker"),
    r("aeo05.agchem", 0.6, "% a year", "AEO2005's projected growth of US agricultural chemicals (nitrogen fertilizers "
      "included), cut from 1.3% because of 'increased competition from foreign suppliers due to relatively high U.S. "
      "natural gas prices'", "EIA, Annual Energy Outlook 2005", AEO05, "2005 projection", "tracker"),
    # --- companies ------------------------------------------------------------------------------------------------------------
    filing("linde.onsite", 15, "years", "Linde's on-site supply contracts: 'total requirement contracts with terms "
           "typically ranging from 10-20 years and containing minimum purchase requirements and price escalation "
           "provisions'", "Linde plc", LIN, lo=10, hi=20),
    filing("linde.merchant", 5, "years", "Linde's merchant (bulk liquid) customer agreements: 'usually three to seven "
           "year supply agreements', which 'generally do not contain minimum purchase requirements'", "Linde plc", LIN,
           lo=3, hi=7),
    filing("apd.onsite", 17.5, "years", "Air Products' sale-of-gas arrangements for large on-site customers: 'long-term "
           "contracts ranging from 15- to 20-years'", "Air Products and Chemicals", APD, "fiscal 2026", lo=15, hi=20),
    filing("apd.charges.2025", 3.0, "$ billion", "Air Products' after-tax charges for business and asset actions, fiscal "
           "2025, 'primarily associated with previously announced project exit decisions'", "Air Products and Chemicals",
           APD, "fiscal 2025"),
    filing("apd.charges.2026", 2.4, "$ billion", "Air Products' after-tax charges for business and asset actions, fiscal 2026",
           "Air Products and Chemicals", APD, "fiscal 2026"),
    filing("apd.adj_oi.2026", 3.2, "$ billion", "Air Products' adjusted operating income, fiscal 2026 (up 11%; a non-GAAP "
           "measure that leaves out the charges)", "Air Products and Chemicals", APD, "fiscal 2026"),
    filing("cf.gas.2025", 350, "million MMBtu", "Natural gas consumed by CF Industries' plants, 2025", "CF Industries",
           CF),
    filing("cf.ammonia.2025", 10120, "thousand short tons", "CF Industries' gross ammonia production, 2025",
           "CF Industries", CF),
    filing("cf.gascost.2025", 3.31, "$ per MMBtu", "CF's cost of natural gas used in production, 2025 ($2.40 in 2024)",
           "CF Industries", CF),
    filing("cf.uk", 2022, "year", "CF closed its Ince plant in 2022 and in 2023 ceased ammonia production at Billingham, "
           "'due to the substantial increase in the cost of natural gas in the United Kingdom'", "CF Industries", CF23,
           "2022-2023"),
    filing("dow.bohlen", 2027, "year", "Dow plans to shut down its ethylene cracker in Böhlen, Germany, by the end of 2027 "
           "(a 2025 strategic review of its European assets)", "Dow Inc.", DOW, "2025"),
    r("mmm.pfas", 12.5, "$ billion", "3M's settlement with US public water suppliers over PFAS: $10.5-12.5 billion "
      "(nominal), a $10.3 billion charge", "3M, Form 8-K, 22 June 2023", MMM, "2023-06-22", "filing", lo=10.5, hi=12.5),
    r("cc.pfas", 1.185, "$ billion", "Chemours, DuPont and Corteva's water-district settlement fund over PFAS",
      "The Chemours Company, Form 8-K, 2 June 2023", CC, "2023-06", "filing"),
    r("epa.pfas.mcl", 4.0, "parts per trillion", "The EPA's maximum contaminant levels for PFOA and PFOS in drinking "
      "water (89 FR 32532)", "US EPA, 'PFAS National Primary Drinking Water Regulation', Federal Register, 26 April 2024",
      EPA, "2024-04-26"),
    r("bhopal.deaths", 2660, "people", "Immediate deaths from the gas leak at Union Carbide's Bhopal plant at midnight "
      "on 2 December 1984, as the Union of India's plaint gave them (30,000 to 40,000 seriously injured)",
      "Supreme Court of India, Union Carbide Corporation v. Union of India, 4 May 1989", SCI, "1984-12-02"),
    r("bhopal.settlement", 470, "$ million", "The settlement Union Carbide paid, ordered by the Supreme Court of India "
      "in February 1989", "Supreme Court of India, 4 May 1989", SCI, "1989"),
)
