"""Register rows for Part 20, *Pharmaceuticals*.  Checked 2026-11-27.

Pfizer's 2012 annual report (Form 10-K, Exhibit 13); the Forms 10-K 2025 of Eli Lilly and Merck; BIO, Informa and QLS's
*Clinical Development Success Rates 2011-2020* (2021); the FDA's study of generic competition and prices (2019) and its
lists of novel drug approvals; CMS's fact sheet on the first negotiated Medicare prices.  Series are the Filing Room's SEC
and FRED extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (20,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
PFE12 = SEC + "78003/000007800313000006/pfe-12312012xex13.htm"
LLY25 = SEC + "59478/000005947826000013/lly-20251231.htm"
MRK25 = SEC + "310158/000031015826000063/mrk-20251231.htm"
BIO = "https://go.bio.org/rs/490-EHZ-999/images/ClinicalDevelopmentSuccessRates2011_2020.pdf"
FDAG = "https://www.fda.gov/media/133509/download"
FDAN = "https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-"
CMS = ("https://www.cms.gov/newsroom/fact-sheets/medicare-drug-price-negotiation-program-negotiated-prices-initial-price-"
       "applicability-year-2026")


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def pfe(key, value, unit, definition, fact="2012"):
    return r(key, value, unit, definition, "Pfizer Inc., Form 10-K 2012 (Exhibit 13, Financial Review)", PFE12, fact)


def lly(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Eli Lilly and Company, Form 10-K 2025", LLY25, fact)


def mrk(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Merck & Co., Inc., Form 10-K 2025", MRK25, fact)


def bio(key, value, unit, definition, fact="2011-2020"):
    return r(key, value, unit, definition, "BIO, Informa Pharma Intelligence and QLS Advisors, Clinical Development Success "
             "Rates 2011-2020 (2021)", BIO, fact, "study")


def fda(key, value, unit, definition, fact="2019"):
    return r(key, value, unit, definition, "US Food and Drug Administration, Generic Competition and Drug Prices: New "
             "Evidence Linking Greater Generic Competition and Lower Generic Drug Prices (2019)", FDAG, fact, "official")


add(
    # Lipitor
    pfe("pfe.lipitor.2010", 10733, "US$ million", "Lipitor revenues, 2010", fact="2010"),
    pfe("pfe.lipitor.2011", 9577, "US$ million", "Lipitor revenues, 2011", fact="2011"),
    pfe("pfe.lipitor.2012", 3948, "US$ million", "Lipitor revenues, 2012: down 59%"),
    pfe("pfe.lipitor.loe", 2011, "year", "'We lost exclusivity for Lipitor in the U.S. in November 2011. The entry of "
        "multi-source generic competition in the U.S. began in May 2012'; Japan June 2011, Australia April 2012, most of "
        "developed Europe March and May 2012"),
    # Lilly
    # (Lilly's 2025 revenue, R&D, Mounjaro and Zepbound are Part 3's rows: lly.rev, lly.rd, lly.mounjaro, lly.zepbound)
    lly("lly20.rev.2024", 45.043, "US$ billion", "revenue, 2024 (2025: 65.179, up 45%)", fact="2024"),
    lly("lly20.mounjaro.2024", 11.540, "US$ billion", "Mounjaro revenue, 2024", fact="2024"),
    lly("lly20.zepbound.2024", 4.926, "US$ billion", "Zepbound revenue, 2024", fact="2024"),
    lly("lly20.mounjaro.us", 13.651, "US$ billion", "Mounjaro revenue in the US, 2025 (outside the US 9.315; 2024: 2.590)"),
    lly("lly20.mounjaro.ex", 9.315, "US$ billion", "Mounjaro revenue outside the US, 2025"),
    lly("lly20.mounjaro.ex2024", 2.590, "US$ billion", "Mounjaro revenue outside the US, 2024", fact="2024"),
    lly("lly20.zepbound.us", 13.484, "US$ billion", "Zepbound revenue in the US, 2025 (outside the US 0.058); 'Tirzepatide is "
        "marketed for obesity under the brand name Zepbound in Canada, Japan, and the U.S.'"),
    lly("lly20.capex.2023", 3.448, "US$ billion", "Purchases of property and equipment, 2023 (cash flow statement)", "2023"),
    lly("lly20.capex.2024", 5.058, "US$ billion", "Purchases of property and equipment, 2024 (cash flow statement)", "2024"),
    lly("lly20.capex.2025", 7.841, "US$ billion", "Purchases of property and equipment, 2025: 'Capital expenditures were $7.8 "
        "billion during 2025, compared to $5.1 billion in 2024'"),
    lly("lly20.sites", 10, "locations", "'Investments to increase our manufacturing capacity include new sites in North Carolina, "
        "Wisconsin, Indiana, Virginia, Texas, Alabama, Pennsylvania, Ireland, Germany, and the Netherlands'"),
    lly("lly20.commit", 10, "US$ billion", "Supply agreements 'could, under certain circumstances, require us to pay up to "
        "approximately $10 billion if we do not purchase specified amounts of goods or services'"),
    lly("lly20.share", 56, "percent", "'Mounjaro and Zepbound accounted for 56 percent of our total revenues in 2025'"),
    r("lly.guide2025", 61.0, "US$ billion", "6 February 2025: '2025 guidance issued with revenue in the range of $58.0 billion "
      "to $61.0 billion'", "Eli Lilly and Company, Form 8-K of 6 February 2025 (Exhibit 99, Q4 2024 results)",
      SEC + "59478/000005947825000037/q424lillysalesandearningsp.htm", "2025 (forecast)"),
    r("lly.guide2026", 83, "US$ billion", "4 February 2026: '2026 guidance issued with revenue in the range of $80 billion to "
      "$83 billion'", "Eli Lilly and Company, Form 8-K of 4 February 2026 (Exhibit 99, Q4 2025 results)",
      SEC + "59478/000005947826000008/q425lillysalesandearningsp.htm", "2026 (forecast)"),
    r("lly.guide2026.oct", 92.0, "US$ billion", "29 October 2026: raised 2026 revenue guidance 'to be in the range of $91.0 "
      "to $92.0 billion'; third-quarter revenue $24.397bn, up 39%", "Eli Lilly and Company, Form 8-K of 29 October 2026 "
      "(Exhibit 99, Q3 2026 results)", SEC + "59478/000005947826000104/q326lillysalesandearningsp.htm", "2026 (forecast)"),
    r("lly.q3.2026", 24.397, "US$ billion", "revenue in the third quarter of 2026, up 39% (Q3 2025: 17.601)", "Eli Lilly and "
      "Company, Form 8-K of 29 October 2026 (Exhibit 99)", SEC + "59478/000005947826000104/q326lillysalesandearningsp.htm",
      "2026-09-30"),
    # Merck
    mrk("mrk.keytruda", 31641, "US$ million", "Keytruda sales, 2025 (2024: 29,482; 2023: 25,011)"),
    mrk("mrk.keytruda.2023", 25011, "US$ million", "Keytruda sales, 2023", fact="2023"),
    mrk("mrk.keytruda.share", 49, "percent", "'in 2025, sales of Keytruda represented 49% of the Company's total sales'"),
    mrk("mrk.cidara", 9.2, "US$ billion", "'In January 2026, Merck acquired Cidara, a biotechnology company developing drug-Fc "
        "conjugate (DFC) therapeutics, for approximately $9.2 billion'", fact="2026-01"),
    mrk("mrk.keytruda.us", 2028, "year", "Keytruda's US compound patent expires in 2028 (two further patents in 2029, which "
        "the company expects to be litigated); EU 2031, Japan 2032-2033, China 2028"),
    # the odds (BIO 2021)
    bio("bio.p1", 52.0, "percent", "Phase I to Phase II transition success rate (n=4,414)"),
    bio("bio.p2", 28.9, "percent", "Phase II to Phase III transition success rate (n=4,933), the lowest"),
    bio("bio.p3", 57.8, "percent", "Phase III to NDA/BLA submission success rate (n=1,928)"),
    bio("bio.nda", 90.6, "percent", "probability of FDA approval after an NDA or BLA submission (n=1,453)"),
    bio("bio.loa", 7.9, "percent", "likelihood of approval from Phase I, all candidates, 2011-2020"),
    bio("bio.years", 10.5, "years", "average time from Phase I to approval: 2.3 years in Phase I, 3.6 in Phase II, 3.3 in "
        "Phase III, 1.3 at the regulatory stage"),
    bio("bio.loa.hem", 23.9, "percent", "likelihood of approval from Phase I: hematology, the highest"),
    bio("bio.loa.onc", 5.3, "percent", "likelihood of approval from Phase I: all oncology (immuno-oncology 12.4%)"),
    bio("bio.onc.n", 1628, "programmes", "oncology programmes in the Phase I sample (n=1,628 of 4,414 overall), the largest "
        "disease area"),
    bio("bio.loa.rare", 17.0, "percent", "likelihood of approval from Phase I: rare diseases"),
    bio("bio.loa.chronic", 5.9, "percent", "likelihood of approval from Phase I: chronic, high-prevalence diseases"),
    # generics (FDA 2019)
    fda("fda.gen1", 39, "percent", "with one generic producer, the generic average manufacturer price is 39% below the "
        "brand's before generic competition (31% using invoice prices)"),
    fda("fda.gen2", 54, "percent", "with two competitors, generic prices 54% below the brand's (AMP; 44% invoice)"),
    fda("fda.gen4", 79, "percent", "with four competitors, 79% below (AMP; 73% invoice)"),
    fda("fda.median", 40, "percent", "'Combining all competition groups, we find median price of generics relative to brands "
        "using AMP is 40% for the drugs in our sample' (49% using invoice prices)"),
    fda("fda.gen6", 95, "percent", "with six or more competitors, 'price reductions of more than 95%'"),
    *[r(f"fda.generic.{y}", n, "applications", f"generic drug applications fully approved by the FDA in {y}", "US Food "
        "and Drug Administration, Generic Competition and Drug Prices (list of studies)", "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/generic-competition-and-drug-prices", str(y), "official")
      for y, n in ((2021, 633), (2022, 742), (2023, 773), (2024, 720))],
    *[bio(f"bio.p2.{k}", v, "percent", f"Phase II to Phase III transition success rate: {name}")
      for k, name, v in (("hem", "hematology", 48.1), ("met", "metabolic", 45.0), ("inf", "infectious disease", 38.4),
                         ("neu", "neurology", 26.8), ("onc", "oncology", 24.6), ("cv", "cardiovascular", 21.0),
                         ("uro", "urology", 15.0))],
    # novel approvals (FDA, CDER)
    *[r(f"fda.novel.{y}", n, "drugs", f"novel drugs approved by CDER in {y} (rows of the FDA's list)", "US Food and Drug "
        "Administration, Novel Drug Approvals for " + str(y), FDAN + (str(y) if y != 2025 else "2025"), str(y), "official")
      for y, n in ((2021, 50), (2022, 37), (2023, 55), (2024, 50), (2025, 46))],
    # Medicare negotiation (CMS)
    r("cms.saving", 6, "US$ billion", "if the negotiated prices for the first ten drugs had applied in 2023 they 'would have "
      "saved an estimated $6 billion in net covered prescription drug costs, which would have represented 22% lower net "
      "spending'; effective 1 January 2026; about 8.8 million of 54 million Part D enrollees used the drugs in 2023",
      "Centers for Medicare & Medicaid Services, fact sheet on the negotiated prices for 2026", CMS, "2023", "official"),
    r("cms.pct", 22, "percent", "lower net spending on the ten drugs had the negotiated prices applied in 2023",
      "Centers for Medicare & Medicaid Services, fact sheet on the negotiated prices for 2026", CMS, "2023", "official"),
    r("cms.users", 8.8, "million people", "Part D enrollees dispensed the ten selected drugs in 2023 (of 54 million)",
      "Centers for Medicare & Medicaid Services, fact sheet on the negotiated prices for 2026", CMS, "2023", "official"),
)
