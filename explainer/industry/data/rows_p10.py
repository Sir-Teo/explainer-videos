"""Register rows for Part 10, *Farming and Food*.  Checked 2026-11-27.

Borlaug and the Green Revolution (the Nobel Foundation); the number and size of US farms (USDA NASS, ERS); Cargill's
revenue (its annual report); beef packers' concentration (USDA ERS); cocoa (the ICCO's Quarterly Bulletin); India's
rice export ban (DGFT notifications as reported); a bushel's flour and loaves (Kansas Wheat); Cochrane's treadmill and
Ehrlich's 1968 book.  The food dollar, costs and returns, farm income, yields, prices and the companies' accounts are
the Filing Room's ERS, Our World in Data, FRED and SEC extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (10,)
NOBEL = "https://www.nobelprize.org/prizes/peace/1970/borlaug/facts/"
NASS25 = "https://esmis.nal.usda.gov/sites/default/release-files/795776/fnlo0226.pdf"
ERS_FARMS = "https://www.ers.usda.gov/data-products/ag-and-food-statistics-charting-the-essentials/farming-and-farm-income"
CARGILL = "https://www.cargill.com/doc/1432279934974/2025-cargill-annual-report.pdf"
ERS_MEAT = ("https://www.ers.usda.gov/amber-waves/2024/january/concentration-in-u-s-meatpacking-industry-and-how-it-"
            "affects-competition-and-cattle-prices")
ICCO = "https://www.icco.org/wp-content/uploads/Production_QBCS-LI-No.-1.pdf"
KSWHEAT = "https://kswheat.com/news/what-does-a-bushel-of-wheat-mean-to-me"
RICE = "https://theprint.in/economy/govt-lifts-curb-on-non-basmati-white-rice-exports-removes-floor-price/2325342"


def r(key, value, unit, definition, source, url, fact, kind="official", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def nobel(key, value, unit, definition, fact="1970"):
    return r(key, value, unit, definition, "The Nobel Foundation, 'Norman Borlaug - Facts', NobelPrize.org", NOBEL, fact,
             "study")


def icco(key, value, unit, definition, fact):
    return r(key, value, unit, definition, "International Cocoa Organization, Quarterly Bulletin of Cocoa Statistics, "
             "Vol. LI No. 1 (28 February 2025), production of cocoa beans", ICCO, fact)


add(
    # --- Borlaug -------------------------------------------------------------------------------------------------------
    nobel("borlaug.prize", 1970, "year", "Norman Borlaug was awarded the Nobel Peace Prize 'for having given a "
          "well-founded hope - the green revolution'; he worked for the International Maize and Wheat Improvement "
          "Center in Mexico City"),
    nobel("borlaug.mexico", 1956, "year", "the year Mexico became self-sufficient in wheat, after Borlaug's work there in "
          "the 1940s and 1950s and his dwarf wheat adapted to Mexican conditions", "1956"),
    nobel("borlaug.india", 1965, "year", "the mid-1960s, when Borlaug introduced dwarf wheat into India and Pakistan and "
          "'production increased enormously'", "1965"),
    nobel("borlaug.born", 1914, "year", "Borlaug was born on 25 March 1914 in Cresco, Iowa (died 12 September 2009)",
          "1914-03-25"),
    # --- farms -----------------------------------------------------------------------------------------------------------
    r("nass.farms.2025", 1865, "thousand", "number of US farms, 2025 (15,000 fewer than in 2024; 2.02 million in 2018)",
      "USDA NASS, Farms and Land in Farms 2025 Summary (February 2026)", NASS25, "2025"),
    r("nass.acres.2025", 469, "acres", "average size of a US farm, 2025 (466 acres in 2024; 444 in 2018)",
      "USDA NASS, Farms and Land in Farms 2025 Summary (February 2026)", NASS25, "2025"),
    r("nass.land.2025", 873.95, "million acres", "land in US farms, 2025", "USDA NASS, Farms and Land in Farms 2025 "
      "Summary (February 2026)", NASS25, "2025"),
    r("ers.farms.1935", 6.81, "million", "the peak number of US farms, 1935 (average size about 155 acres)",
      "USDA ERS, Ag and Food Statistics: Charting the Essentials, 'Farming and farm income' (from the Census of "
      "Agriculture)", ERS_FARMS, "1935"),
    r("ers.acres.1935", 155, "acres", "average size of a US farm, 1935", "USDA ERS, Ag and Food Statistics: Charting the "
      "Essentials, 'Farming and farm income'", ERS_FARMS, "1935"),
    # --- the traders and the packers -------------------------------------------------------------------------------------
    r("cargill.revenue.2025", 154, "USD bn", "Cargill's revenue in its fiscal year to 31 May 2025 (privately held; it "
      "publishes no profit figures)", "Cargill, 2025 Annual Report", CARGILL, "FY2025 (to 2025-05-31)", "filing"),
    r("ers.beef.cr4", 85, "%", "share of US steer and heifer purchases made by the four largest beef packers (36% in "
      "1980)", "USDA ERS, Amber Waves, 'Concentration in U.S. Meatpacking Industry and How It Affects Competition and "
      "Cattle Prices' (January 2024)", ERS_MEAT, "2019-2023"),
    r("ers.beef.cr4.1980", 36, "%", "share of US steer and heifer purchases made by the four largest beef packers, 1980",
      "USDA ERS, Amber Waves (January 2024), from USDA's Packers and Stockyards data", ERS_MEAT, "1980"),
    # --- cocoa -----------------------------------------------------------------------------------------------------------
    icco("icco.civ.2023", 2241, "kt", "Côte d'Ivoire's cocoa bean production, 2022/23", "2022/23"),
    icco("icco.gha.2023", 654, "kt", "Ghana's cocoa bean production, 2022/23", "2022/23"),
    icco("icco.world.2023", 5043, "kt", "world cocoa bean production, 2022/23", "2022/23"),
    icco("icco.civ.2024", 1674, "kt", "Côte d'Ivoire's cocoa bean production, 2023/24 (estimate)", "2023/24"),
    icco("icco.gha.2024", 530, "kt", "Ghana's cocoa bean production, 2023/24 (estimate)", "2023/24"),
    icco("icco.world.2024", 4489, "kt", "world cocoa bean production, 2023/24 (estimate)", "2023/24"),
    # --- rice ------------------------------------------------------------------------------------------------------------
    r("india.rice.ban", 2023, "year", "India banned exports of non-basmati white rice on 20 July 2023; the ban was replaced "
      "by a minimum export price of $490 a tonne in late September 2024 and the minimum price removed on 23 October 2024",
      "Directorate General of Foreign Trade notifications, as reported by ThePrint (23 October 2024)", RICE,
      "2023-07-20", "press", note="the dates are the Government of India's, in DGFT notifications"),
    # --- bread -----------------------------------------------------------------------------------------------------------
    r("kswheat.flour", 42, "lb", "white flour from one 60-pound bushel of wheat, 'enough for about 70 one-pound loaves of "
      "white bread'", "Kansas Wheat, 'What does a bushel of wheat mean to me?'", KSWHEAT, "2024", "press",
      note="Kansas Wheat's (the state's wheat commission) rule of thumb, not a measured average"),
    r("kswheat.loaves", 70, "loaves", "one-pound loaves of white bread from one bushel of wheat", "Kansas Wheat, 'What does "
      "a bushel of wheat mean to me?'", KSWHEAT, "2024", "press",
      note="Kansas Wheat's (the state's wheat commission) rule of thumb, not a measured average"),
    # --- the soybean crush ---------------------------------------------------------------------------------------------
    r("cme.crush.oil", 11, "lb", "soybean oil from one 60-pound bushel of soybeans in the exchange's standard 'board crush' "
      "(with 44 lb of 48%-protein meal)", "CME Group, Soybean Crush Reference Guide",
      "https://www.cmegroup.com/trading/agricultural/files/pm374-cbot-soybeans-crush-reference-guide.pdf", "2024"),
    r("cme.crush.meal", 44, "lb", "soybean meal from one 60-pound bushel of soybeans in the standard board crush",
      "CME Group, Soybean Crush Reference Guide",
      "https://www.cmegroup.com/trading/agricultural/files/pm374-cbot-soybeans-crush-reference-guide.pdf", "2024"),
    # --- the books -------------------------------------------------------------------------------------------------------
    r("cochrane.treadmill", 1958, "year", "Willard Cochrane described the treadmill of farm technology: early adopters "
      "profit, everyone follows, output rises, the price falls and the gain passes to consumers",
      "Willard W. Cochrane, Farm Prices: Myth and Reality (University of Minnesota Press, 1958)",
      "https://www.upress.umn.edu/9780816601837/farm-prices/", "1958", "study"),
    r("ehrlich.bomb", 1968, "year", "Paul Ehrlich's The Population Bomb opened 'The battle to feed all of humanity is "
      "over' and predicted that hundreds of millions of people would starve to death despite any crash programmes",
      "Paul R. Ehrlich, The Population Bomb (Ballantine, 1968); Smithsonian Magazine, 'The Book That Incited a "
      "Worldwide Fear of Overpopulation' (January 2018)",
      "https://www.smithsonianmag.com/innovation/book-incited-worldwide-fear-overpopulation-180967499/", "1968", "study"),
)
