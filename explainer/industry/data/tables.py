"""Transcribed tables: series read from published documents (yearbooks, annual filings, statistics portals) that have
no machine-readable download we can use, each with its source, URL and the date it was read.

    from explainer.industry.data.tables import table
    table("worldsteel.china")          # {1992: 80.935, ...}  (million tonnes)

A Register row holds one figure; a table holds a series of the same figure.  ``tests/industry/test_tables.py`` checks
that every table names a source, a URL and a checked date, and that its values are numbers.  Like the Register,
nothing here is fetched at render time.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Table:
    key: str
    unit: str
    definition: str
    source: str
    url: str
    checked: str
    data: dict
    note: str = ""
    parts: tuple = field(default=())


TABLES: dict[str, Table] = {}
USED: set[str] = set()


def add(*ts: Table) -> None:
    for t in ts:
        if t.key in TABLES:
            raise ValueError(f"tables: {t.key} entered twice")
        TABLES[t.key] = t


def table(key: str) -> dict:
    USED.add(key)
    return dict(TABLES[key].data)


def info(key: str) -> Table:
    return TABLES[key]


# ---------------------------------------------------------------------------------------------------------- Part 11
C = "2026-11-27"
P11 = (11,)
WSIF26 = "https://worldsteel.org/wp-content/uploads/World-Steel-in-Figures-2026.pdf"
SSY02 = "https://worldsteel.org/wp-content/uploads/Steel-Statistical-Yearbook-2002.pdf"
SSY11 = "https://worldsteel.org/wp-content/uploads/Steel-Statistical-Yearbook-2011.pdf"
SSY20 = "https://worldsteel.org/wp-content/uploads/Steel-Statistical-Yearbook-2020-concise-version.pdf"
WSIF22 = "https://worldsteel.org/wp-content/uploads/World-Steel-in-Figures-2022.pdf"
WSIF24 = "https://worldsteel.org/wp-content/uploads/World-Steel-in-Figures-2024.pdf"
NUCOR_10K = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000073309&type=10-K"
IAI_E = "https://international-aluminium.org/statistics/primary-aluminium-smelting-energy-intensity/"
IAI_P = "https://international-aluminium.org/statistics/primary-aluminium-production/"
SRO = "https://worldsteel.org/media/press-releases/"

add(
    Table("worldsteel.world", "million tonnes", "World crude steel production, by year (all qualities)",
          "World Steel Association, World Steel in Figures 2026 (data finalised 8 June 2026), 'World crude steel "
          "production, 1950 to 2025'", WSIF26, C,
          {1950: 189, 1955: 270, 1960: 347, 1965: 456, 1970: 595, 1975: 644, 1980: 717, 1985: 719, 1990: 770,
           1995: 753, 2000: 850, 2005: 1148, 2010: 1435, 2011: 1540, 2012: 1563, 2013: 1654, 2014: 1676, 2015: 1626,
           2016: 1634, 2017: 1738, 2018: 1831, 2019: 1879, 2020: 1883, 2021: 1963, 2022: 1889, 2023: 1904,
           2024: 1887, 2025: 1849}, parts=P11),
    Table("worldsteel.china", "million tonnes", "China's crude steel production, by year; each year from the latest "
          "worldsteel publication that gives it",
          "World Steel Association: Steel Statistical Yearbooks 2002 (1992-2000), 2011 (2001-2009) and 2020 (2010-2019), "
          "World Steel in Figures 2022 (2020-2021), 2024 (2022-2023) and 2026 (2024-2025)", WSIF26, C,
          {1992: 80.935, 1993: 89.539, 1994: 92.613, 1995: 95.360, 1996: 101.237, 1997: 108.911, 1998: 114.588,
           1999: 123.954, 2000: 127.236, 2001: 151.634, 2002: 182.366, 2003: 222.336, 2004: 282.911, 2005: 353.240,
           2006: 419.149, 2007: 489.288, 2008: 500.312, 2009: 573.567, 2010: 638.743, 2011: 701.968, 2012: 731.040,
           2013: 822.000, 2014: 822.306, 2015: 803.825, 2016: 807.609, 2017: 870.855, 2018: 928.260, 2019: 996.342,
           2020: 1064.7, 2021: 1032.8, 2022: 1019.1, 2023: 1019.1, 2024: 1005.1, 2025: 960.8},
          note=f"Yearbooks: {SSY02}; {SSY11}; {SSY20}; {WSIF22}; {WSIF24}; {WSIF26}.  Vintages differ by a few "
               "per cent where a later yearbook revised a year (2010: 626.7 in 2011's, 638.7 in 2020's).", parts=P11),
    Table("worldsteel.us_eaf", "million tonnes", "US crude steel made in electric furnaces, by year",
          "World Steel Association, Steel Statistical Yearbook 2002, Table 11", SSY02, C,
          {1992: 32.031, 1993: 34.948, 1994: 35.880, 1995: 38.471, 1996: 40.711, 1997: 43.099, 1998: 44.513,
           1999: 45.063, 2000: 47.850, 2001: 42.745}, parts=P11),
    Table("worldsteel.us_total", "million tonnes", "US crude steel production, by year",
          "World Steel Association, Steel Statistical Yearbook 2002, Table 4", SSY02, C,
          {1992: 84.322, 1993: 88.793, 1994: 91.244, 1995: 95.191, 1996: 95.535, 1997: 98.485, 1998: 98.658,
           1999: 97.427, 2000: 101.803, 2001: 90.104}, parts=P11),
    Table("worldsteel.eaf_share", "% of crude steel", "Share of crude steel made in electric furnaces, the US",
          "World Steel Association: Steel Statistical Yearbook 2002 (1992, 2000: Tables 4 and 11), Steel Statistical "
          "Yearbook 2020 (2019) and World Steel in Figures 2026 (2025)", WSIF26, C,
          {1992: 38.0, 2000: 47.0, 2019: 68.0, 2025: 71.3}, parts=P11),
    Table("worldsteel.china_asu", "million tonnes", "China's apparent steel use (finished steel products), by year",
          "World Steel Association, World Steel in Figures 2026, 'Apparent steel use, 2021 to 2025'", WSIF26, C,
          {2021: 954.4, 2022: 926.7, 2023: 905.1, 2024: 856.6, 2025: 796.0}, parts=P11),
    Table("worldsteel.sro_china", "% change", "worldsteel's October forecasts of the change in China's steel demand "
          "(apparent use of finished steel) for the year of the forecast (same) and the year after (next)",
          "World Steel Association, Short Range Outlook press releases of 19 October 2022, 17 October 2023, 14 October "
          "2024, 13 October 2025 and 12 October 2026; and of 14 April 2026 (the published 2025 figure)", SRO, C,
          {2022: {"same": -4.0, "next": 0.0}, 2023: {"same": 2.0, "next": 0.0}, 2024: {"same": -3.0, "next": -1.0},
           2025: {"same": -2.0, "next": -1.0}, 2026: {"same": -2.0, "next": -1.0}},
          note="2022: 'likely to fall by 4.0%', 2023 'expected to remain flat'; 2023: '2.0% growth', 2024 'may sustain "
               "the level of 2023'; 2024: 'a 3.0% decline in 2024 and a further 1.0% in 2025'; 2025: 'falling by "
               "approximately 2.0%', 2026 '1.0%'; 2026: 'contract by 2.0% in 2026', 2027 'narrow to 1.0%'.  April 2026: "
               "'The now published official figure for China is a 7.1% contraction' (for 2025).", parts=P11),
    Table("nucor.utilization", "% of capacity", "Average utilization rate of all operating facilities in Nucor's steel "
          "mills segment, by year",
          "Nucor Corporation, Forms 10-K for 2003-2025 (Item 2, Properties)", NUCOR_10K, C,
          {2003: 94, 2004: 97, 2005: 82, 2006: 89, 2007: 87, 2008: 80, 2009: 54, 2010: 70, 2011: 74, 2012: 74,
           2013: 74, 2014: 78, 2015: 68, 2016: 80, 2017: 85, 2018: 91, 2019: 84, 2020: 82, 2021: 94, 2022: 77,
           2023: 78, 2024: 76, 2025: 83}, parts=P11),
    Table("nucor.scrap", "$ a gross ton", "Average cost of scrap and scrap substitutes used in Nucor's steel mills",
          "Nucor Corporation, Forms 10-K for 2005, 2008, 2009 and 2019-2025 (Item 7)", NUCOR_10K, C,
          {2003: 137, 2004: 238, 2005: 244, 2006: 246, 2007: 278, 2008: 438, 2009: 303, 2018: 361, 2019: 314,
           2020: 290, 2021: 469, 2022: 492, 2023: 421, 2024: 394, 2025: 392},
          note="The 10-Ks for 2010-2017 do not state it in their text.  'On average, it takes approximately 1.1 tons "
               "of scrap and scrap substitutes to produce one ton of steel' (10-K 2025).", parts=P11),
    Table("nucor.mill_price", "$ a ton", "Average sales price per ton in Nucor's steel mills segment",
          "Nucor Corporation, Forms 10-K for 2019-2025 (Item 7; each year as stated in the next year's 10-K where "
          "restated)", NUCOR_10K, C,
          {2018: 817, 2019: 748, 2020: 671, 2021: 1195, 2022: 1324, 2023: 1084, 2024: 1013, 2025: 1008}, parts=P11),
    Table("iai.energy_world", "kWh a tonne", "Primary aluminium smelting energy intensity, total energy (AC), world "
          "average", "International Aluminium Institute, statistics, 'Primary Aluminium Smelting Energy Intensity'",
          IAI_E, C,
          {1980: 16951, 1985: 16580, 1990: 16083, 1995: 15878, 2000: 15381, 2005: 15080, 2010: 14777, 2015: 14239,
           2020: 14243, 2021: 14209, 2022: 14119, 2023: 14096, 2024: 14004, 2025: 13880}, parts=P11),
    Table("iai.energy_2025", "kWh a tonne", "Primary aluminium smelting energy intensity (AC), 2025, by region",
          "International Aluminium Institute, statistics, 'Primary Aluminium Smelting Energy Intensity'", IAI_E, C,
          {"World": 13880, "China": 13203, "Gulf Cooperation Council": 14891, "North America": 14721,
           "Europe": 15482}, parts=P11),
    Table("iai.production", "thousand tonnes", "Primary aluminium production, by year: the world, China (estimated) "
          "and the Gulf Cooperation Council",
          "International Aluminium Institute, statistics, 'Primary Aluminium Production' (monthly, summed by year)",
          IAI_P, C,
          {"World": {1973: 12017, 1980: 15390, 1990: 19514, 2000: 24657, 2005: 31905, 2010: 42353, 2015: 58456,
                     2020: 65325, 2021: 67092, 2022: 69038, 2023: 70716, 2024: 73009, 2025: 74032},
           "China": {2000: 2794, 2005: 7806, 2010: 17331, 2015: 31518, 2020: 37337, 2021: 38837, 2022: 40430,
                     2023: 41666, 2024: 43396, 2025: 44219},
           "GCC": {2010: 2724, 2015: 5104, 2020: 5833, 2021: 5889, 2022: 6074, 2023: 6217, 2024: 6346, 2025: 6159}},
          parts=P11),
    Table("iai.gcc_monthly", "thousand tonnes", "Primary aluminium production in the Gulf Cooperation Council, month by "
          "month, 2025-2026", "International Aluminium Institute, statistics, 'Primary Aluminium Production'", IAI_P, C,
          {"2025-01": 527, "2025-02": 473, "2025-03": 523, "2025-04": 505, "2025-05": 522, "2025-06": 507,
           "2025-07": 523, "2025-08": 521, "2025-09": 506, "2025-10": 523, "2025-11": 508, "2025-12": 521,
           "2026-01": 499, "2026-02": 469, "2026-03": 465, "2026-04": 274, "2026-05": 281, "2026-06": 276,
           "2026-07": 305, "2026-08": 318, "2026-09": 325, "2026-10": 352}, parts=P11),
)


# ---------------------------------------------------------------------------------------------------------- Part 15
P15 = (15,)
TSM20F = "https://www.sec.gov/Archives/edgar/data/1046179/000162828026025362/tsm-20251231.htm"
TSM_FABS = "TSMC, Form 20-F 2025 (Item 4, 'Semiconductor Manufacturing Capacity and Technology': fabs in operation as of 28 February 2026)"

add(
    Table("tsm.fabs.nm", "nanometres", "Most advanced technology in volume production at each of TSMC's fabs and its "
          "subsidiaries' fabs in operation, by location (as of the end of 2025), keyed by fab number",
          TSM_FABS, TSM20F, C,
          {"Hsinchu": {2: 450, 3: 150, 5: 150, 8: 110, 12: 40, 20: 2}, "Southern Taiwan": {6: 110, 14: 16, 18: 3, 22: 2},
           "Central Taiwan": {15: 7}, "Washington, US": {11: 150}, "Shanghai, China": {10: 150},
           "Nanjing, China": {16: 16}, "Arizona, US": {21: 5}, "Kumamoto, Japan": {23: 28}},
          note="ESMC's Fab 24 in Dresden is under construction ('where Fab 24 and related facilities will be located').",
          parts=P15),
    Table("tsm.fabs.year", "year", "Year each TSMC fab began commercial production", TSM_FABS, TSM20F, C,
          {2: 1990, 3: 1995, 5: 1997, 6: 2000, 8: 1998, 10: 2004, 11: 1998, 12: 2001, 14: 2004, 15: 2012, 16: 2018,
           18: 2020, 20: 2025, 21: 2024, 22: 2025, 23: 2024}, parts=P15),
    Table("tsm.fabs.wafer", "inches", "Wafer size of each TSMC fab", TSM_FABS, TSM20F, C,
          {2: 6, 3: 8, 5: 8, 6: 8, 8: 8, 10: 8, 11: 8, 12: 12, 14: 12, 15: 12, 16: 12, 18: 12, 20: 12, 21: 12, 22: 12,
           23: 12}, parts=P15),
)
