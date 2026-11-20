"""The Data Room of *Economics, Built* (videos/economics/SYLLABUS.md, section 2.6): real data, with source and vintage.

    from explainer.economics import data
    world = data.maddison_world()                 # {"year": [...], "World": [...], "Western Europe": [...], ...}
    uk = data.maddison_country("GBR")             # {"year": [...], "gdppc": [...], "pop": [...]}
    ip = data.fred("INDPRO")                      # {"date": [...], "value": [...]} as frozen on DATASETS[...]["vintage"]
    data.cite("maddison2023")                     # the line for an on-screen data tag

Every dataset is registered in :data:`DATASETS` with its publisher, URL, licence, the date it was retrieved (its
vintage) and the SHA-256 of the raw download, and described in ``SOURCES.md`` beside this file.  The films read
small frozen extracts committed here (``*.csv``), so a build needs no network and every number on screen can be
traced to a file.  ``python -m explainer.economics.data --refresh NAME`` downloads the source again into
``.cache/economics/raw/``, reports whether it changed since the recorded vintage, and rewrites the extract; a film
that should use the new vintage must then say so (its frozen date moves).

Numbers transcribed from a publication (a table in a paper, a passage in a book) are in :mod:`.tables`, each with
its citation, page and the date it was checked.

This module needs numpy only (openpyxl to refresh the spreadsheets); it imports without manim, so the labs can use
it.
"""

from __future__ import annotations

import argparse
import csv
import functools
import hashlib
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RAW = ROOT / ".cache" / "economics" / "raw"

# ---------------------------------------------------------------------------
# The registry
# ---------------------------------------------------------------------------
FRED_SERIES = {
    # id: (title, units, frequency, source agency)
    "GDPCA": ("Real gross domestic product", "billions of chained 2017 dollars", "annual",
              "U.S. Bureau of Economic Analysis"),
    "GDPC1": ("Real gross domestic product", "billions of chained 2017 dollars, seasonally adjusted annual rate",
              "quarterly", "U.S. Bureau of Economic Analysis"),
    "UNRATE": ("Unemployment rate", "percent, seasonally adjusted", "monthly", "U.S. Bureau of Labor Statistics"),
    "M0892AUSM156SNBR": ("Unemployment rate for the United States, 1929-1942",
                         "percent, seasonally adjusted (National Industrial Conference Board estimates)",
                         "monthly", "NBER Macrohistory Database, series m08292a"),
    "INDPRO": ("Industrial production: total index", "index 2017 = 100, seasonally adjusted", "monthly",
               "Board of Governors of the Federal Reserve System"),
    "CPIAUCNS": ("Consumer price index for all urban consumers: all items", "index 1982-84 = 100, not seasonally "
                 "adjusted", "monthly", "U.S. Bureau of Labor Statistics"),
    # Part 3: the national accounts, annual, billions of current dollars
    "GDPA": ("Gross domestic product", "billions of dollars", "annual", "U.S. Bureau of Economic Analysis"),
    "GDIA": ("Gross domestic income", "billions of dollars", "annual", "U.S. Bureau of Economic Analysis"),
    "PCECA": ("Personal consumption expenditures", "billions of dollars", "annual", "U.S. Bureau of Economic Analysis"),
    "GPDIA": ("Gross private domestic investment", "billions of dollars", "annual",
              "U.S. Bureau of Economic Analysis"),
    "GCEA": ("Government consumption expenditures and gross investment", "billions of dollars", "annual",
             "U.S. Bureau of Economic Analysis"),
    "EXPGSA": ("Exports of goods and services", "billions of dollars", "annual", "U.S. Bureau of Economic Analysis"),
    "IMPGSA": ("Imports of goods and services", "billions of dollars", "annual", "U.S. Bureau of Economic Analysis"),
    "A033RC1A027NBEA": ("National income: compensation of employees, paid", "billions of dollars", "annual",
                        "U.S. Bureau of Economic Analysis"),
    "A191RD3A086NBEA": ("Gross domestic product: implicit price deflator", "index 2017 = 100", "annual",
                        "U.S. Bureau of Economic Analysis"),
    # Part 3: the household survey's measures of labour underutilization, monthly, seasonally adjusted
    "U1RATE": ("U-1: unemployed 15 weeks or longer, as a percent of the civilian labor force", "percent", "monthly",
               "U.S. Bureau of Labor Statistics"),
    "U2RATE": ("U-2: job losers and persons who completed temporary jobs, as a percent of the civilian labor force",
               "percent", "monthly", "U.S. Bureau of Labor Statistics"),
    "U4RATE": ("U-4: total unemployed plus discouraged workers, as a percent of the labor force plus discouraged "
               "workers", "percent", "monthly", "U.S. Bureau of Labor Statistics"),
    "U5RATE": ("U-5: U-4 plus all other persons marginally attached to the labor force", "percent", "monthly",
               "U.S. Bureau of Labor Statistics"),
    "U6RATE": ("U-6: U-5 plus persons employed part time for economic reasons", "percent", "monthly",
               "U.S. Bureau of Labor Statistics"),
    "CIVPART": ("Labor force participation rate", "percent", "monthly", "U.S. Bureau of Labor Statistics"),
    "EMRATIO": ("Employment-population ratio", "percent", "monthly", "U.S. Bureau of Labor Statistics"),
    # Part 3: price indexes, monthly
    "CPIAUCSL": ("Consumer price index for all urban consumers: all items", "index 1982-84 = 100, seasonally "
                 "adjusted", "monthly", "U.S. Bureau of Labor Statistics"),
    "SUUR0000SA0": ("Chained consumer price index for all urban consumers (C-CPI-U): all items",
                    "index December 1999 = 100, not seasonally adjusted", "monthly", "U.S. Bureau of Labor Statistics"),
    "PCEPI": ("Personal consumption expenditures: chain-type price index", "index 2017 = 100, seasonally adjusted",
              "monthly", "U.S. Bureau of Economic Analysis"),
    # Part 3: the labour share (Penn World Table, via FRED)
    "LABSHPUSA156NRUG": ("Share of labour compensation in GDP at current national prices for the United States",
                         "ratio", "annual", "Penn World Table, Groningen Growth and Development Centre"),
    # Part 5: the population, for spending per head
    "B230RC0A052NBEA": ("Population (midperiod)", "thousands of persons", "annual", "U.S. Bureau of Economic Analysis"),
    # Part 7: the Euler equation's data: real consumption, its price index and the Treasury bill rate
    "PCECCA": ("Real personal consumption expenditures", "billions of chained 2017 dollars", "annual",
               "U.S. Bureau of Economic Analysis"),
    "DPCERG3A086NBEA": ("Personal consumption expenditures (implicit price deflator, chain-type price index)",
                        "index 2017 = 100", "annual", "U.S. Bureau of Economic Analysis"),
    "TB3MS": ("3-month Treasury bill secondary market rate, discount basis", "percent", "monthly",
              "Board of Governors of the Federal Reserve System"),
}
# Part 5: personal consumption expenditures by type of product (NIPA tables 2.4.4 and 2.4.5), annual, 1929 on: the
# fifteen categories that make up all of PCE, each as a price index (2017 = 100) and as spending (billions of dollars)
PCE_CATEGORIES = {
    "DMOT": "motor vehicles and parts", "DFDH": "furnishings and durable household equipment",
    "DREQ": "recreational goods and vehicles", "DODG": "other durable goods",
    "DFXA": "food and beverages purchased for off-premises consumption", "DCLO": "clothing and footwear",
    "DGOE": "gasoline and other energy goods", "DONG": "other nondurable goods", "DHUT": "housing and utilities",
    "DHLC": "health care", "DTRS": "transportation services", "DRCA": "recreation services",
    "DFSA": "food services and accommodations", "DIFS": "financial services and insurance",
    "DOTS": "other services (including nonprofit institutions' final consumption)",
}
for _c, _name in PCE_CATEGORIES.items():
    FRED_SERIES[f"{_c}RG3A086NBEA"] = (f"Personal consumption expenditures: {_name} (chain-type price index)",
                                       "index 2017 = 100", "annual", "U.S. Bureau of Economic Analysis")
    FRED_SERIES[f"{_c}RC1A027NBEA"] = (f"Personal consumption expenditures: {_name}", "billions of dollars", "annual",
                                       "U.S. Bureau of Economic Analysis")
# Part 9: the law of one price in crude oil, Brent (North Sea) against West Texas Intermediate (Cushing, Oklahoma)
FRED_SERIES["MCOILBRENTEU"] = ("Crude oil prices: Brent - Europe", "dollars per barrel, not seasonally adjusted",
                               "monthly", "U.S. Energy Information Administration")
FRED_SERIES["MCOILWTICO"] = ("Crude oil prices: West Texas Intermediate (WTI) - Cushing, Oklahoma",
                             "dollars per barrel, not seasonally adjusted", "monthly",
                             "U.S. Energy Information Administration")
# Part 10: pass-through from green coffee to the shelf: the average retail price of ground coffee (BLS)
FRED_SERIES["APU0000717311"] = ("Average price: coffee, 100%, ground roast, all sizes (cost per pound/453.6 grams) in "
                                "U.S. city average", "dollars per pound, not seasonally adjusted", "monthly",
                                "U.S. Bureau of Labor Statistics")
# Part 12: rockets and feathers: the average retail price of regular unleaded gasoline (BLS), against WTI crude
FRED_SERIES["APU000074714"] = ("Average price: gasoline, unleaded regular (cost per gallon/3.785 liters) in U.S. city "
                               "average", "dollars per gallon, not seasonally adjusted", "monthly",
                               "U.S. Bureau of Labor Statistics")
# Part 13: lemons: the CPI for used cars and trucks, and for new vehicles (BLS)
FRED_SERIES["CUSR0000SETA02"] = ("Consumer Price Index for All Urban Consumers: used cars and trucks in U.S. city "
                                 "average", "index 1982-1984 = 100, seasonally adjusted", "monthly",
                                 "U.S. Bureau of Labor Statistics")
FRED_SERIES["CUSR0000SETA01"] = ("Consumer Price Index for All Urban Consumers: new vehicles in U.S. city average",
                                 "index 1982-1984 = 100, seasonally adjusted", "monthly",
                                 "U.S. Bureau of Labor Statistics")
# The date each series was retrieved (its vintage); a series not listed was retrieved on DATASETS["fred"]["vintage"]
# Part 22: consumption against income: real PCE (quarterly), real disposable personal income (monthly), the saving rate
FRED_SERIES["PCECC96"] = ("Real personal consumption expenditures", "billions of chained 2017 dollars, seasonally "
                          "adjusted annual rate", "quarterly", "U.S. Bureau of Economic Analysis")
FRED_SERIES["DSPIC96"] = ("Real disposable personal income", "billions of chained 2017 dollars, seasonally adjusted "
                          "annual rate", "monthly", "U.S. Bureau of Economic Analysis")
FRED_SERIES["PSAVERT"] = ("Personal saving rate", "percent, seasonally adjusted annual rate", "monthly",
                          "U.S. Bureau of Economic Analysis")
FRED_SERIES["PCE"] = ("Personal consumption expenditures", "billions of dollars, seasonally adjusted annual rate",
                      "monthly", "U.S. Bureau of Economic Analysis")
FRED_SERIES["PCEND"] = ("Personal consumption expenditures: nondurable goods", "billions of dollars, seasonally "
                       "adjusted annual rate", "monthly", "U.S. Bureau of Economic Analysis")
FRED_SERIES["PCES"] = ("Personal consumption expenditures: services", "billions of dollars, seasonally adjusted "
                       "annual rate", "monthly", "U.S. Bureau of Economic Analysis")
FRED_SERIES["DNDGRG3M086SBEA"] = ("Personal consumption expenditures: nondurable goods (chain-type price index)",
                                  "index 2017 = 100, seasonally adjusted", "monthly", "U.S. Bureau of Economic Analysis")
FRED_SERIES["DSERRG3M086SBEA"] = ("Personal consumption expenditures: services (chain-type price index)",
                                  "index 2017 = 100, seasonally adjusted", "monthly", "U.S. Bureau of Economic Analysis")
# Part 23: housing as an asset: the national home price index against the CPI's rent of primary residence
FRED_SERIES["CSUSHPINSA"] = ("S&P CoreLogic Case-Shiller U.S. National Home Price Index", "index January 2000 = 100, "
                             "not seasonally adjusted", "monthly", "S&P Dow Jones Indices LLC")
FRED_SERIES["CUSR0000SEHA"] = ("Consumer Price Index for All Urban Consumers: rent of primary residence in U.S. city "
                               "average", "index 1982-1984 = 100, seasonally adjusted", "monthly",
                               "U.S. Bureau of Labor Statistics")

FRED_RETRIEVED = {s: "2026-11-19" for s in (
    "GDPA", "GDIA", "PCECA", "GPDIA", "GCEA", "EXPGSA", "IMPGSA", "A033RC1A027NBEA", "A191RD3A086NBEA", "U1RATE",
    "U2RATE", "U4RATE", "U5RATE", "U6RATE", "CIVPART", "EMRATIO", "CPIAUCSL", "SUUR0000SA0", "PCEPI",
    "LABSHPUSA156NRUG", "B230RC0A052NBEA", "PCECCA", "DPCERG3A086NBEA", "TB3MS", "MCOILBRENTEU", "MCOILWTICO", "APU0000717311", "APU000074714", "CUSR0000SETA02", "CUSR0000SETA01", *(f"{c}{t}" for c in PCE_CATEGORIES for t in ("RG3A086NBEA",
                                                                                         "RC1A027NBEA")))}
FRED_RETRIEVED.update({s: "2026-11-20" for s in ("PCECC96", "DSPIC96", "PSAVERT", "PCE", "PCEND", "PCES",
                                                  "DNDGRG3M086SBEA", "DSERRG3M086SBEA", "CSUSHPINSA",
                                                  "CUSR0000SEHA")})

SPF_FILES = ("median_rgdp_level", "median_rgdp_growth", "median_recess_level")
SPF_URL = ("https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/"
           "data-files/files/{}.xlsx")
PINK_URL = ("https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/"
            "CMO-Historical-Data-Monthly.xlsx")

DATASETS = {
    "maddison2023": {
        "title": "Maddison Project Database 2023",
        "publisher": "Groningen Growth and Development Centre, University of Groningen",
        "citation": "Bolt, J. and van Zanden, J. L. (2024), Maddison-style estimates of the evolution of the world "
                    "economy: a new 2023 update, Journal of Economic Surveys 1-41",
        "short": "Maddison Project Database 2023 (Bolt and van Zanden 2024)",
        "url": "https://dataverse.nl/api/access/datafile/421302",
        "page": "https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023",
        "licence": "CC BY 4.0; the MPD asks that the original country sources be cited when the data are shown "
                   "in a graph (SOURCES.md lists those used)",
        "units": "real GDP per head in 2011 international dollars; population in thousands",
        "vintage": "2026-11-18",
        "sha256": "ecc5916ca12789b983fc4be437f8a354bbf4291323605324ac3e0aea4c57cbb6",
        "files": ("maddison2023_world.csv", "maddison2023_countries.csv"),
    },
    "fred": {
        "title": "FRED, Federal Reserve Bank of St. Louis",
        "publisher": "Federal Reserve Bank of St. Louis (series from the agencies in FRED_SERIES)",
        "citation": "Federal Reserve Bank of St. Louis, FRED; each series retrieved on its date in FRED_RETRIEVED "
                    "(2026-11-18 unless listed there)",
        "short": "FRED, retrieved 18 Nov 2026",
        "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}",
        "licence": "BEA, BLS and Federal Reserve series are in the public domain; the NBER Macrohistory series is "
                   "used with its suggested citation; the Penn World Table's labour share is CC BY 4.0",
        "vintage": "2026-11-18",
        "files": tuple(f"fred_{s}.csv" for s in FRED_SERIES),
    },
    "spf": {
        "title": "Survey of Professional Forecasters, median forecasts",
        "publisher": "Federal Reserve Bank of Philadelphia",
        "citation": "Federal Reserve Bank of Philadelphia, Survey of Professional Forecasters, historical median "
                    "forecasts (files median_rgdp_level, median_rgdp_growth, median_recess_level), retrieved "
                    "2026-11-18",
        "short": "Philadelphia Fed, Survey of Professional Forecasters",
        "url": SPF_URL,
        "licence": "free to use with attribution to the Federal Reserve Bank of Philadelphia",
        "vintage": "2026-11-18",
        "files": ("spf_2006_2011.csv",),
    },
    "pinksheet": {
        "title": "World Bank Commodity Price Data (The Pink Sheet), monthly prices",
        "publisher": "World Bank, Prospects Group",
        "citation": "World Bank, Commodity Price Data (The Pink Sheet), CMO-Historical-Data-Monthly.xlsx, updated "
                    "3 November 2026, retrieved 2026-11-18",
        "short": "World Bank Pink Sheet, Nov 2026",
        "url": PINK_URL,
        "page": "https://www.worldbank.org/en/research/commodity-markets",
        "licence": "CC BY 4.0 (World Bank open data)",
        "units": "nominal US dollars, monthly averages (units per column in PINK_COLUMNS)",
        "vintage": "2026-11-18",
        "sha256": "3c8d9d8dbb48342fdbf24777c39a8ce8964cc2fd0958f72f6779e6e4ad99cde2",
        "files": ("pinksheet_monthly.csv",),
    },
    "psd_coffee": {
        "title": "Production, Supply and Distribution: coffee, green",
        "publisher": "U.S. Department of Agriculture, Foreign Agricultural Service",
        "citation": "USDA Foreign Agricultural Service, Production, Supply and Distribution Online, coffee "
                    "(psd_coffee_csv.zip), retrieved 2026-11-18",
        "short": "USDA FAS, PSD Online (coffee)",
        "url": "https://apps.fas.usda.gov/psdonline/downloads/psd_coffee_csv.zip",
        "licence": "U.S. government work, public domain",
        "units": "thousands of 60 kg bags, by marketing year",
        "vintage": "2026-11-18",
        "sha256": "967633a200af10d2a196816dd0169e732c61ed8dff4a83574bfa0b435c50ee66",
        "files": ("psd_coffee.csv",),
    },
    "wdi": {
        "title": "World Development Indicators: GDP at market exchange rates and at purchasing power parity, "
                 "population, Gini index",
        "publisher": "World Bank",
        "citation": "World Bank, World Development Indicators (API, last updated 11 November 2026), indicators "
                    "NY.GDP.MKTP.CD, NY.GDP.MKTP.PP.CD, NY.GDP.PCAP.CD, NY.GDP.PCAP.PP.CD, SP.POP.TOTL, SI.POV.GINI, "
                    "retrieved 2026-11-19",
        "short": "World Bank WDI, Nov 2026",
        "url": "https://api.worldbank.org/v2/country/all/indicator/{}?format=json&date=2015:2025&per_page=20000",
        "licence": "CC BY 4.0 (World Bank open data)",
        "units": "current US dollars; current international (PPP) dollars; persons; Gini index 0-100",
        "vintage": "2026-11-19",
        "files": ("wdi_2015_2025.csv",),
    },
    "hdr": {
        "title": "Human Development Report 2025: composite indices, complete time series",
        "publisher": "United Nations Development Programme, Human Development Report Office",
        "citation": "UNDP, Human Development Report 2025, HDR25_Composite_indices_complete_time_series.csv, "
                    "retrieved 2026-11-19",
        "short": "UNDP, Human Development Report 2025",
        "url": "https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_complete_time_series.csv",
        "licence": "CC BY 3.0 IGO (UNDP open data), with attribution",
        "units": "HDI 0-1; life expectancy in years; schooling in years; GNI per head in 2021 PPP dollars",
        "vintage": "2026-11-19",
        "sha256": "61ed82e5b66c88dfca8ff9fac775c63981ecab6a254862af97acacc41c143117",
        "files": ("hdr2025_1990_2023.csv",),
    },
    "warheads": {
        "title": "Estimated nuclear warhead stockpiles, by country, 1945-2026",
        "publisher": "Federation of American Scientists (estimates); Our World in Data (compilation)",
        "citation": "Federation of American Scientists (2026), \"Estimated Global Nuclear Warhead Inventories\", with "
                    "minor processing by Our World in Data, grapher nuclear-warhead-stockpiles (last updated "
                    "2026-05-13), retrieved 2026-11-19",
        "short": "Federation of American Scientists, via Our World in Data",
        "url": "https://ourworldindata.org/grapher/nuclear-warhead-stockpiles.csv?v=1&csvType=full&"
               "useColumnShortNames=true",
        "licence": "CC BY 4.0 (Our World in Data); the estimates are the Federation of American Scientists', cited",
        "units": "warheads in military stockpiles (retired warheads awaiting dismantlement excluded), end of year",
        "vintage": "2026-11-19",
        "sha256": "2f38e76406e3de5e726cf7d5026af345776afeb6f46cf5ceef22fbc01ddc36ea",
        "files": ("warheads_1945_2026.csv",),
    },
    "so2": {
        "title": "Sulphur dioxide emissions from all sectors, by country and region, 1900-2022",
        "publisher": "Community Emissions Data System (Hoesly et al. 2024); Our World in Data (compilation)",
        "citation": "R. M. Hoesly et al. (2024), Community Emissions Data System (CEDS) v_2024_07_08, with minor "
                    "processing by Our World in Data, grapher so-emissions-by-world-region-in-million-tonnes, "
                    "retrieved 2026-11-19",
        "short": "CEDS (Hoesly et al. 2024), via Our World in Data",
        "url": "https://ourworldindata.org/grapher/so-emissions-by-world-region-in-million-tonnes.csv?v=1&"
               "csvType=full&useColumnShortNames=true",
        "licence": "CC BY 4.0 (Our World in Data and CEDS)",
        "units": "tonnes of SO2 a year",
        "vintage": "2026-11-19",
        "sha256": "8465848ae578ec07c5636ca207d470bf99551fa72b7e0fcb9ea77d691a3a519c",
        "entities": ("World", "United States", "United Kingdom", "China", "India", "Germany", "Japan", "Europe",
                     "Asia", "North America", "Africa", "South America"),
        "files": ("so2_1900_2022.csv",),
    },
    "marriage": {
        "title": "Crude marriage rate (marriages a year per 1,000 people), by country",
        "publisher": "OECD Family Database; US Census Bureau (1949); Centers for Disease Control and Prevention; Our "
                     "World in Data (compilation)",
        "citation": "OECD (2025), OECD Family Database, Marriage and Divorce Rates; US Census Bureau (1949), Vital "
                    "Statistics; CDC (2020), Marriage Rates in the United States, with minor processing by Our World in "
                    "Data, grapher marriage-rate-per-1000-inhabitants, retrieved 2026-11-19",
        "short": "OECD, US Census Bureau and CDC, via Our World in Data",
        "url": "https://ourworldindata.org/grapher/marriage-rate-per-1000-inhabitants.csv?v=1&csvType=full&"
               "useColumnShortNames=true",
        "licence": "CC BY 4.0 (Our World in Data); sources' terms",
        "units": "marriages a year per 1,000 people",
        "vintage": "2026-11-19",
        "sha256": "bddc3f12a677f36a7c0af65118b8e3c37869582eac1e5f638bd850c7d214c979",
        "entities": ("United States", "United Kingdom", "Japan", "Italy", "Sweden", "South Korea", "Germany",
                     "France", "Netherlands", "Denmark"),
        "files": ("marriage_rate.csv",),
    },
    "democracy": {
        "title": "Electoral democracy index (V-Dem), by country and for the world, 1789-2025",
        "publisher": "Varieties of Democracy (V-Dem) Institute; Our World in Data (compilation)",
        "citation": "V-Dem (2026), Democracy Report v16, electoral democracy index (central estimate), processed by Our "
                    "World in Data, grapher electoral-democracy-index, retrieved 2026-11-19",
        "short": "V-Dem v16 (2026), via Our World in Data",
        "url": "https://ourworldindata.org/grapher/electoral-democracy-index.csv?v=1&csvType=full&"
               "useColumnShortNames=true",
        "licence": "CC BY 4.0 (Our World in Data); V-Dem's terms (free with citation)",
        "units": "index from 0 to 1",
        "vintage": "2026-11-19",
        "sha256": "a0843a64486708e1638e5051be67dde8ddb0c82ae7be264c512173f503445afc",
        "entities": ("World", "United States", "United Kingdom", "France", "India", "Germany", "Japan", "Brazil",
                     "South Africa", "China"),
        "files": ("democracy_vdem.csv",),
    },
    "millennium": {
        "title": "A millennium of macroeconomic data for the UK (version 3.1): England's population, real consumption "
                 "wages and real GDP per head, 1209-2016",
        "publisher": "Bank of England",
        "citation": "Thomas, R. and Dimsdale, N. (2017), A Millennium of UK Data, Bank of England OBRA dataset, version "
                    "3.1, sheet A1 (headline series): population of England (A21), real consumption wages (A48), real "
                    "consumption earnings adjusted for days worked (A48, after Humphries and Weisdorf) and "
                    "England's real GDP per head in 2013 prices (A21, from Broadberry, Campbell, Klein, Overton "
                    "and van Leeuwen 2015 before 1700), retrieved 2026-11-19",
        "short": "Bank of England, A Millennium of Macroeconomic Data (v3.1)",
        "url": "https://www.bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/"
               "a-millennium-of-macroeconomic-data-for-the-uk.xlsx",
        "licence": "Bank of England; free to reuse with attribution under the Bank's terms",
        "units": "population in thousands; real wages, 1900 = 100; GDP per head, 2013 pounds",
        "vintage": "2026-11-19",
        "sha256": "4c23dd392a498691eac92659aec283fb43f28118bd80511dc87fc595974195eb",
        "files": ("boe_millennium_england.csv",),
    },
    "longrun": {
        "title": "Long-run population (from 10,000 BCE), life expectancy (from 1543), children per woman (from 1891 or "
                 "1950) and men's height (by decade of birth, from 1710), for the world and nine countries",
        "publisher": "Our World in Data (compilation of HYDE, Gapminder, the UN World Population Prospects, Riley, "
                     "Zijdeman and Ribeira da Silva, the Human Mortality and Fertility Databases, Baten and Blum, "
                     "NCD-RisC)",
        "citation": "Our World in Data, grapher population, life-expectancy, children-born-per-woman and "
                    "average-height-of-men-for-selected-countries (each with the sources it names), retrieved "
                    "2026-11-19",
        "short": "HYDE, Gapminder, UN WPP, Riley and others, via Our World in Data",
        "urls": {k: f"https://ourworldindata.org/grapher/{k}.csv?v=1&csvType=full&useColumnShortNames=true"
                 for k in ("population", "life-expectancy", "children-born-per-woman",
                           "average-height-of-men-for-selected-countries")},
        "columns": {"population": "population_historical", "life-expectancy": "life_expectancy_0",
                    "children-born-per-woman": "fertility_rate_hist",
                    "average-height-of-men-for-selected-countries": "height"},
        "licence": "CC BY 4.0 (Our World in Data); sources' terms",
        "units": "people; years; children per woman; centimetres",
        "vintage": "2026-11-19",
        "sha256": {"population": "31c97de9a52df079", "life-expectancy": "6336e80067d72cd9",
                   "children-born-per-woman": "c4398f67298b5e78",
                   "average-height-of-men-for-selected-countries": "30402c6b431193c2"},
        "entities": ("World", "United Kingdom", "Sweden", "France", "Netherlands", "China", "India", "Japan",
                     "South Korea", "Nigeria", "United States"),
        "files": ("longrun_owid.csv",),
    },
    "pwt": {
        "title": "Penn World Table version 11.0: output, population, employment, hours, human capital, capital "
                 "stocks, labour shares, investment shares and TFP, 185 countries, 1950-2023",
        "publisher": "Groningen Growth and Development Centre (Feenstra, Inklaar and Timmer)",
        "citation": "Feenstra, R. C., R. Inklaar and M. P. Timmer (2015), \"The Next Generation of the Penn World "
                    "Table\", American Economic Review 105(10): 3150-3182; Penn World Table 11.0 (2025), DataverseNL, "
                    "doi:10.34894/FABVLR, file pwt110.xlsx, sheet Data, retrieved 2026-11-19",
        "short": "Penn World Table 11.0 (Feenstra, Inklaar and Timmer)",
        "url": "https://dataverse.nl/api/access/datafile/554105",
        "licence": "CC BY 4.0",
        "units": "rgdpo, rgdpna, cn, rnna in millions of 2021 US dollars (PPP); pop and emp in millions; avh hours a "
                 "year; hc an index; labsh, csh_i, delta, irr shares; ctfp relative to the US = 1",
        "vintage": "2026-11-19",
        "sha256": "7b337e94f39dfe304bc459e433f8ce0624496c812707ae0c924888f5142b3ab3",
        "files": ("pwt110.csv",),
    },
    "ajr": {
        "title": "Acemoglu, Johnson and Robinson's base sample of 64 former colonies: log GDP per head in 1995, "
                 "average protection against expropriation risk 1985-95, settler mortality, latitude and continent",
        "publisher": "Acemoglu, Johnson and Robinson (2001), as distributed in the R package hdm (Chernozhukov, "
                     "Hansen and Spindler), dataset AJR",
        "citation": "D. Acemoglu, S. Johnson and J. A. Robinson, \"The Colonial Origins of Comparative Development: "
                    "An Empirical Investigation\", American Economic Review 91(5) (2001): 1369-1401; hdm 0.3.2 "
                    "(CRAN, 2024), data/AJR.rda, retrieved 2026-11-20",
        "short": "Acemoglu, Johnson and Robinson (2001), via the R package hdm",
        "url": "https://cran.r-project.org/src/contrib/hdm_0.3.2.tar.gz",
        "licence": "MIT (hdm); the data are AJR's, published with their paper",
        "units": "GDP: log GDP per head, 1995 (PPP); Exprop: 0-10; Mort: settler deaths per 1,000 a year",
        "vintage": "2026-11-20",
        "sha256": "3354b22752f0aa0c0d9c8c12b38810202b6380f2587e539be11d9a358412fe6a",
        "files": ("ajr_hdm.csv",),
    },
    "shiller": {
        "title": "Robert Shiller's annual US stock market data with consumption: the S&P composite price, dividends and "
                 "earnings, the one-year and long interest rates, the CPI, the real one-year rate, real consumption "
                 "per head, and the real return on the S&P composite, 1871 onward",
        "publisher": "Robert J. Shiller, Yale University (an update of chapter 26 of Market Volatility, 1989)",
        "citation": "R. J. Shiller, Market Volatility (MIT Press, 1989), ch. 26, and Irrational Exuberance (Princeton, "
                    "2015); data file chapt26.xlsx, sheet Data, from www.econ.yale.edu/~shiller/data.htm, retrieved "
                    "2026-11-20",
        "short": "Shiller, Market Volatility ch. 26 data (annual, updated)",
        "url": "http://www.econ.yale.edu/~shiller/data/chapt26.xlsx",
        "licence": "made freely available by the author for research and teaching, with citation",
        "units": "P, D, E: index points and dollars a share; R, RLONG: percent; RealR: gross real one-year return; C: "
                 "real consumption per head (2005 dollars); RealP, RealD: in the latest year's dollars; Return: real "
                 "gross-minus-one return on the S&P composite over the year; Pstar, PstarR, PstarC: the present value of "
                 "the real dividends that followed, discounted at a constant rate, at the one-year rate and by "
                 "consumption growth (Shiller's ex post rational prices)",
        "vintage": "2026-11-20",
        "sha256": "d255bb1230a9a94c450ee4738d914ec8c6c79ceae58f1cc89559c7f40fa7c9c0",
        "files": ("shiller_annual.csv",),
    },
    "draft1970": {
        "title": "The draft lottery of 1 December 1969 (for men born 1944-50): the rank drawn for each birthday",
        "publisher": "U.S. Selective Service System; as tabulated by the Journal of Statistics Education data archive",
        "citation": "Selective Service System, Semiannual Report of the Director (July-December 1971), p. 60; N. Starr, "
                    "\"Nonrandom Risk: The 1970 Draft Lottery\", Journal of Statistics Education 5(2) (1997), data "
                    "file draft70yr.dat; retrieved 2026-11-19",
        "short": "Selective Service System, draft lottery of 1 Dec 1969 (JSE data archive)",
        "url": "https://jse.amstat.org/datasets/draft70yr.dat.txt",
        "licence": "a U.S. government record (public domain); the JSE archive's tabulation, free for education",
        "units": "rank (1 = drafted first) for each day of the year, 1 January (day 1) to 31 December (day 366)",
        "vintage": "2026-11-19",
        "sha256": "973f258e63c94812b705c2007652fba34a02d579719dc74c569286106053f8d0",
        "files": ("draft1970.csv",),
    },
    "rtdsm": {
        "title": "Real-Time Data Set for Macroeconomists: real GDP (ROUTPUT), quarterly vintages",
        "publisher": "Federal Reserve Bank of Philadelphia",
        "citation": "Federal Reserve Bank of Philadelphia, Real-Time Data Set for Macroeconomists, routputqvqd.xlsx "
                    "(vintages 1965Q4-2026Q4), retrieved 2026-11-19",
        "short": "Philadelphia Fed, Real-Time Data Set",
        "url": "https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/real-time-data/data-files/xlsx/"
               "routputqvqd.xlsx",
        "licence": "free to use with attribution to the Federal Reserve Bank of Philadelphia",
        "units": "real GDP, billions of chained (or constant) dollars of each vintage's base year, SAAR",
        "vintage": "2026-11-19",
        "sha256": "6a7971b31b7336551705465de8a0855826f3652abe112406f52b2c2ed0994c0c",
        "files": ("rtdsm_2006_2010.csv", "rtdsm_first_latest.csv"),
    },
}

# The Pink Sheet columns kept in the extract: (key, the column's heading in the sheet, units)
PINK_COLUMNS = (
    ("oil", "Crude oil, average", "$/bbl"), ("coal", "Coal, Australian", "$/mt"),
    ("gas_us", "Natural gas, US", "$/mmbtu"), ("cocoa", "Cocoa", "$/kg"), ("arabica", "Coffee, Arabica", "$/kg"),
    ("robusta", "Coffee, Robusta", "$/kg"), ("tea", "Tea, avg 3 auctions", "$/kg"), ("maize", "Maize", "$/mt"),
    ("rice", "Rice, Thai 5%", "$/mt"), ("wheat", "Wheat, US HRW", "$/mt"), ("soybeans", "Soybeans", "$/mt"),
    ("sugar", "Sugar, world", "$/kg"), ("beef", "Beef **", "$/kg"), ("banana", "Banana, US", "$/kg"),
    ("cotton", "Cotton, A Index", "$/kg"), ("rubber", "Rubber, RSS3", "$/kg"), ("aluminum", "Aluminum", "$/mt"),
    ("copper", "Copper", "$/mt"), ("tin", "Tin", "$/mt"), ("nickel", "Nickel", "$/mt"), ("zinc", "Zinc", "$/mt"),
    ("gold", "Gold", "$/troy oz"), ("silver", "Silver", "$/troy oz"),
)
# The coffee producers kept by name in the PSD extract (the rest are in the world total)
PSD_COUNTRIES = ("Brazil", "Vietnam", "Colombia", "Indonesia", "Ethiopia", "Honduras", "India", "Uganda", "Mexico",
                 "Peru", "Cote d'Ivoire")

# Countries kept at full (annual) resolution in the Maddison extract; every other country is kept at the
# benchmark years in MADDISON_YEARS (enough for the data films).
MADDISON_FULL = ("GBR", "NLD", "ITA", "FRA", "ESP", "SWE", "DEU", "USA", "JPN", "CHN", "IND", "KOR", "PRK", "NGA",
                 "BRA", "MEX", "ARG", "EGY", "TUR", "ZAF", "IDN", "ETH", "AUS", "CAN", "BWA", "VNM", "RUS", "SUN",
                 "POL", "BGD", "PAK", "GHA", "KEN", "CHL", "IRN", "SGP", "TWN")
MADDISON_YEARS = (1820, 1850, 1870, 1880, 1890, 1900, 1913, 1929, 1938, *range(1950, 2023, 2), 2022)


def cite(name: str) -> str:
    """The short source line for an on-screen data tag."""
    d = DATASETS[name]
    return d["short"]


def vintage(name: str) -> str:
    return DATASETS[name]["vintage"]


def fred_cite(*series: str) -> str:
    """The data tag for FRED series: "FRED, retrieved 19 Nov 2026" (the latest retrieval date of those named)."""
    import datetime as _dt  # noqa: PLC0415

    day = max(FRED_RETRIEVED.get(s, DATASETS["fred"]["vintage"]) for s in series)
    d = _dt.date.fromisoformat(day)
    return f"FRED, retrieved {d.day} {d.strftime('%b')} {d.year}"


# ---------------------------------------------------------------------------
# Loaders (the committed extracts)
# ---------------------------------------------------------------------------
def _read(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _num(x: str):
    if x is None or x == "":
        return float("nan")
    return float(x)


@functools.lru_cache(maxsize=None)
def maddison_world() -> dict:
    """World and regional GDP per head, 1820-2022, from the MPD's regional sheet: ``{"year": [...], name: [...]}``.
    Missing values are NaN (several regions start after 1820)."""
    rows = _read(HERE / "maddison2023_world.csv")
    cols = [c for c in rows[0] if c != "year"]
    out = {"year": [int(r["year"]) for r in rows]}
    for c in cols:
        out[c] = [_num(r[c]) for r in rows]
    return out


@functools.lru_cache(maxsize=None)
def _maddison_rows() -> list[dict]:
    return _read(HERE / "maddison2023_countries.csv")


def maddison_country(code: str) -> dict:
    """One country's series from the extract: ``{"code", "name", "region", "year", "gdppc", "pop"}``.  Only years
    with a GDP-per-head estimate are kept.  Full annual series for :data:`MADDISON_FULL`, benchmark years for the
    rest."""
    rows = [r for r in _maddison_rows() if r["code"] == code]
    if not rows:
        raise KeyError(f"no Maddison series for {code!r} in the extract")
    return {"code": code, "name": rows[0]["country"], "region": rows[0]["region"],
            "year": [int(r["year"]) for r in rows], "gdppc": [_num(r["gdppc"]) for r in rows],
            "pop": [_num(r["pop"]) for r in rows]}


def maddison_year(year: int) -> list[dict]:
    """Every country with an estimate in ``year``: ``[{"code", "country", "region", "gdppc", "pop"}]``."""
    return [{"code": r["code"], "country": r["country"], "region": r["region"], "gdppc": _num(r["gdppc"]),
             "pop": _num(r["pop"])} for r in _maddison_rows() if int(r["year"]) == year]


@functools.lru_cache(maxsize=None)
def fred(series: str) -> dict:
    """A FRED series as frozen on the vintage date: ``{"date": ["YYYY-MM-DD", ...], "value": [...], "title",
    "units", "frequency", "source"}`` (missing observations are NaN)."""
    rows = _read(HERE / f"fred_{series}.csv")
    title, units, freq, source = FRED_SERIES[series]
    return {"date": [r["date"] for r in rows], "value": [_num(r["value"]) for r in rows], "title": title,
            "units": units, "frequency": freq, "source": source, "series": series,
            "retrieved": FRED_RETRIEVED.get(series, DATASETS["fred"]["vintage"])}


@functools.lru_cache(maxsize=None)
def pce_by_type(first: int = 1929, last: int = 2025) -> dict:
    """America's spending as one consumer's choices: for each year, the fifteen PCE categories' price indexes
    (2017 = 100) and quantities per head (spending in dollars per person divided by the price index, so in 2017
    dollars per person).  Returns ``{"years", "codes", "names", "prices" (n x 15), "quantities" (n x 15),
    "spending" (n x 15, dollars per head), "population" (thousands)}``."""
    import numpy as _np  # noqa: PLC0415

    def annual(series):
        d = fred(series)
        return {int(t[:4]): v for t, v in zip(d["date"], d["value"])}

    pop = annual("B230RC0A052NBEA")
    years = list(range(first, last + 1))
    codes = list(PCE_CATEGORIES)
    price = {c: annual(f"{c}RG3A086NBEA") for c in codes}
    spend = {c: annual(f"{c}RC1A027NBEA") for c in codes}
    P = _np.array([[price[c][y] for c in codes] for y in years], float)
    E = _np.array([[spend[c][y] for c in codes] for y in years], float) * 1e9 / (
        _np.array([pop[y] for y in years], float)[:, None] * 1e3)
    return {"years": years, "codes": codes, "names": [PCE_CATEGORIES[c] for c in codes], "prices": P,
            "quantities": E / P * 100.0, "spending": E, "population": [pop[y] for y in years]}


@functools.lru_cache(maxsize=None)
def spf() -> list[dict]:
    """Median forecasts from each survey of 2006-2011: ``[{"year", "quarter", "rgdp_a", "rgdp_b", "growth_q": [...],
    "recess": [...]}]``.  ``rgdp_a``, ``rgdp_b``: the median forecast of the annual-average level of real GDP in the
    survey's year and the next; ``growth_q``: annualized quarterly growth for the survey quarter and the four after
    (DRGDP2-6); ``recess``: the probability (percent) of a decline in real GDP in the survey quarter and the four
    after (RECESS1-5)."""
    out = []
    for r in _read(HERE / "spf_2006_2011.csv"):
        out.append({"year": int(r["year"]), "quarter": int(r["quarter"]), "rgdp_a": _num(r["rgdp_a"]),
                    "rgdp_b": _num(r["rgdp_b"]),
                    "growth_q": [_num(r[f"drgdp{k}"]) for k in range(2, 7)],
                    "recess": [_num(r[f"recess{k}"]) for k in range(1, 6)]})
    return out


@functools.lru_cache(maxsize=None)
def pinksheet(key: str) -> dict:
    """A Pink Sheet monthly price series: ``{"month": ["1960-01", ...], "value": [...], "name", "units"}`` (nominal
    US dollars; NaN where the sheet has no price).  ``key`` is one of :data:`PINK_COLUMNS`' keys ("arabica", "oil",
    "tin", ...)."""
    cols = {k: (name, units) for k, name, units in PINK_COLUMNS}
    if key not in cols:
        raise KeyError(f"no Pink Sheet column {key!r}; choose from {sorted(cols)}")
    rows = _read(HERE / "pinksheet_monthly.csv")
    return {"month": [r["month"] for r in rows], "value": [_num(r[key]) for r in rows], "name": cols[key][0],
            "units": cols[key][1], "key": key}


@functools.lru_cache(maxsize=None)
def psd_coffee() -> dict:
    """World coffee balance by marketing year from USDA's PSD: ``{"year": [...], "world": {attribute: [...]},
    country: {attribute: [...]}}`` for attributes ``production``, ``consumption``, ``exports``, ``ending_stocks``
    (thousands of 60 kg bags).  ``world`` sums every country in the PSD file."""
    rows = _read(HERE / "psd_coffee.csv")
    years = sorted({int(r["year"]) for r in rows})
    out = {"year": years}
    for r in rows:
        place = out.setdefault(r["country"], {})
        series = place.setdefault(r["attribute"], [float("nan")] * len(years))
        series[years.index(int(r["year"]))] = _num(r["value"])
    return out


@functools.lru_cache(maxsize=None)
def wdi(year: int | None = None) -> list[dict]:
    """Countries (not regional aggregates) from the WDI extract: ``[{"code", "country", "region", "income", "lon",
    "lat", "year",
    "gdp_usd", "gdp_ppp", "gdppc_usd", "gdppc_ppp", "pop", "gini"}]`` (NaN where missing), every year 2015-2025 or
    only ``year``."""
    out = []
    for r in _read(HERE / "wdi_2015_2025.csv"):
        if year is not None and int(r["year"]) != year:
            continue
        row = {k: r[k] for k in ("code", "country", "region", "income")}
        row["lon"], row["lat"] = _num(r["lon"]), _num(r["lat"])   # the capital's coordinates
        row["year"] = int(r["year"])
        for k in ("gdp_usd", "gdp_ppp", "gdppc_usd", "gdppc_ppp", "pop", "gini"):
            row[k] = _num(r[k])
        out.append(row)
    return out


@functools.lru_cache(maxsize=None)
def hdr() -> list[dict]:
    """Countries in the Human Development Report 2025's time series: ``[{"code", "country", "region", "hdi": {year:
    value}, "le", "eys", "mys", "gnipc"}]`` for 1990-2023 (missing years absent)."""
    out = []
    for r in _read(HERE / "hdr2025_1990_2023.csv"):
        row = {"code": r["iso3"], "country": r["country"], "region": r["region"]}
        for k in ("hdi", "le", "eys", "mys", "gnipc"):
            row[k] = {}
        out.append(row)
    by = {o["code"]: o for o in out}
    for r in _read(HERE / "hdr2025_1990_2023.csv"):
        for k in ("hdi", "le", "eys", "mys", "gnipc"):
            for y in range(1990, 2024):
                v = r.get(f"{k}_{y}", "")
                if v not in ("", None):
                    by[r["iso3"]][k][y] = float(v)
    return out


@functools.lru_cache(maxsize=None)
def rtdsm() -> dict:
    """Real GDP as each vintage reported it: ``{"quarters": ["2006:Q1", ...], "vintages": ["2007Q1", ...],
    "level": {vintage: [...]}}`` for observation quarters 2006-2010 and vintages 2007Q1 onward (NaN where a vintage had
    no figure yet), and ``{"first_latest": [{"quarter", "first", "latest"}]}``: each quarter's annualized growth in
    the first vintage that reported it and in the latest."""
    rows = _read(HERE / "rtdsm_2006_2010.csv")
    vintages = [c for c in rows[0] if c != "quarter"]
    out = {"quarters": [r["quarter"] for r in rows], "vintages": vintages,
           "level": {v: [_num(r[v]) for r in rows] for v in vintages}}
    out["first_latest"] = [{"quarter": r["quarter"], "first": _num(r["first"]), "latest": _num(r["latest"])}
                           for r in _read(HERE / "rtdsm_first_latest.csv")]
    return out


@functools.lru_cache(maxsize=None)
def draft1970() -> dict:
    """The draft lottery drawn on 1 December 1969: ``{"day": [1..366], "month": [...], "rank": [...]}``, the rank
    (order of call) drawn for each birthday of the year (366 days, with 29 February)."""
    rows = _read(HERE / "draft1970.csv")
    return {"day": [int(r["day"]) for r in rows], "month": [int(r["month"]) for r in rows],
            "rank": [int(r["rank"]) for r in rows]}


# ---------------------------------------------------------------------------
# Refreshing from the sources
# ---------------------------------------------------------------------------
def _download(url: str, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "explainer-videos-data-room/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        blob = r.read()
    dest.write_bytes(blob)
    return hashlib.sha256(blob).hexdigest()


def refresh_maddison() -> None:
    import openpyxl  # noqa: PLC0415  (only needed to refresh)

    d = DATASETS["maddison2023"]
    raw = RAW / "mpd2023.xlsx"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"maddison2023: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    wb = openpyxl.load_workbook(raw, read_only=True, data_only=True)
    rows = list(wb["Regional data"].iter_rows(values_only=True))
    names = [n for n in rows[1][1:9]]
    with open(HERE / "maddison2023_world.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "World", *names])
        for r in rows[2:]:
            if not isinstance(r[0], (int, float)):
                continue
            w.writerow([int(r[0]), _fmt(r[9]), *[_fmt(x) for x in r[1:9]]])
    keep = set(MADDISON_YEARS)
    with open(HERE / "maddison2023_countries.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["code", "country", "region", "year", "gdppc", "pop"])
        for r in wb["Full data"].iter_rows(min_row=2, values_only=True):
            cc, name, region, year, g, p = r[:6]
            if g is None or year is None:
                continue
            if cc in MADDISON_FULL or int(year) in keep:
                w.writerow([cc, name, region, int(year), _fmt(g), _fmt(p)])


def _fmt(x) -> str:
    if x is None or x == "":
        return ""
    return f"{float(x):.4f}".rstrip("0").rstrip(".")


def refresh_fred(series=None) -> None:
    """Download FRED's series again (all of them, or just ``series``) and rewrite the extracts."""
    for s in (series or FRED_SERIES):
        raw = RAW / f"fred_{s}.csv"
        _download(DATASETS["fred"]["url"].format(s), raw)
        with open(raw, newline="") as f:
            rows = list(csv.reader(f))
        with open(HERE / f"fred_{s}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["date", "value"])
            for r in rows[1:]:
                w.writerow([r[0], "" if r[1] in (".", "") else r[1]])


def refresh_spf() -> None:
    import openpyxl  # noqa: PLC0415

    tabs = {}
    for name in SPF_FILES:
        raw = RAW / f"spf_{name}.xlsx"
        _download(SPF_URL.format(name), raw)
        ws = openpyxl.load_workbook(raw, read_only=True, data_only=True).worksheets[0]
        rows = list(ws.iter_rows(values_only=True))
        head = [str(h).lower() for h in rows[0]]
        tabs[name] = {(int(r[0]), int(r[1])): dict(zip(head, r)) for r in rows[1:] if isinstance(r[0], (int, float))}
    with open(HERE / "spf_2006_2011.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        cols = ["rgdp_a", "rgdp_b", *[f"drgdp{k}" for k in range(2, 7)], *[f"recess{k}" for k in range(1, 6)]]
        w.writerow(["year", "quarter", *cols])
        for (y, q) in sorted(tabs["median_rgdp_level"]):
            if not 2006 <= y <= 2011:
                continue
            lv, gr, rc = (tabs[n].get((y, q), {}) for n in SPF_FILES)
            vals = [lv.get("rgdpa"), lv.get("rgdpb"), *[gr.get(f"drgdp{k}") for k in range(2, 7)],
                    *[rc.get(f"recess{k}") for k in range(1, 6)]]
            w.writerow([y, q, *[_fmt(v) if isinstance(v, (int, float)) else "" for v in vals]])


def refresh_pinksheet() -> None:
    import openpyxl  # noqa: PLC0415

    d = DATASETS["pinksheet"]
    raw = RAW / "pinksheet_monthly.xlsx"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"pinksheet: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    ws = openpyxl.load_workbook(raw, read_only=True, data_only=True)["Monthly Prices"]
    rows = list(ws.iter_rows(values_only=True))
    head = [str(h).strip() if h else "" for h in rows[4]]
    idx = {k: head.index(name) for k, name, _ in PINK_COLUMNS}
    with open(HERE / "pinksheet_monthly.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["month", *idx])
        for r in rows[6:]:
            if not r[0] or "M" not in str(r[0]):
                continue
            y, m = str(r[0]).split("M")
            vals = [r[i] if isinstance(r[i], (int, float)) else None for i in idx.values()]
            if all(v is None for v in vals):
                continue
            w.writerow([f"{y}-{m}", *[_fmt(v) for v in vals]])


def refresh_psd_coffee() -> None:
    import io  # noqa: PLC0415
    import zipfile  # noqa: PLC0415

    d = DATASETS["psd_coffee"]
    raw = RAW / "psd_coffee_csv.zip"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"psd_coffee: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    with zipfile.ZipFile(raw) as z:
        text = z.read("psd_coffee.csv").decode("utf-8")
    keep = {"Production": "production", "Domestic Consumption": "consumption", "Exports": "exports",
            "Ending Stocks": "ending_stocks"}
    world: dict = {}
    named = []
    for r in csv.DictReader(io.StringIO(text)):
        a = keep.get(r["Attribute_Description"])
        if a is None:
            continue
        y, v = int(r["Market_Year"]), float(r["Value"])
        world[(y, a)] = world.get((y, a), 0.0) + v
        if r["Country_Name"] in PSD_COUNTRIES:
            named.append((r["Country_Name"], y, a, v))
    with open(HERE / "psd_coffee.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["country", "year", "attribute", "value"])
        for (y, a), v in sorted(world.items()):
            w.writerow(["world", y, a, _fmt(v)])
        for c, y, a, v in sorted(named):
            w.writerow([c, y, a, _fmt(v)])


WDI_INDICATORS = {"gdp_usd": "NY.GDP.MKTP.CD", "gdp_ppp": "NY.GDP.MKTP.PP.CD", "gdppc_usd": "NY.GDP.PCAP.CD",
                  "gdppc_ppp": "NY.GDP.PCAP.PP.CD", "pop": "SP.POP.TOTL", "gini": "SI.POV.GINI"}


def refresh_wdi() -> None:
    import json  # noqa: PLC0415

    raw = RAW / "wdi_countries.json"
    _download("https://api.worldbank.org/v2/country?format=json&per_page=400", raw)
    meta = {c["id"]: c for c in json.loads(raw.read_text())[1] if c["region"]["id"] != "NA"}
    vals: dict = {}
    for col, ind in WDI_INDICATORS.items():
        f = RAW / f"wdi_{ind}.json"
        _download(DATASETS["wdi"]["url"].format(ind), f)
        for r in json.loads(f.read_text())[1]:
            code = r["countryiso3code"]
            if code in meta and r["value"] is not None:
                vals.setdefault((code, int(r["date"])), {})[col] = r["value"]
    with open(HERE / "wdi_2015_2025.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["code", "country", "region", "income", "lon", "lat", "year", *WDI_INDICATORS])
        for (code, year) in sorted(vals):
            c = meta[code]
            v = vals[(code, year)]
            w.writerow([code, c["name"], c["region"]["value"].strip(), c["incomeLevel"]["value"], c["longitude"],
                        c["latitude"], year, *[_fmt(v.get(k)) for k in WDI_INDICATORS]])


def refresh_hdr() -> None:
    d = DATASETS["hdr"]
    raw = RAW / "hdr25_composite.csv"
    sha = _download(d["url"], raw)
    if d.get("sha256") and sha != d["sha256"]:
        print(f"hdr: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    with open(raw, newline="", encoding="latin-1") as f:   # the HDRO's file is Latin-1 (Cote d'Ivoire's o)
        rows = list(csv.DictReader(f))
    keep = ["iso3", "country", "region"] + [f"{k}_{y}" for k in ("hdi", "le", "eys", "mys", "gnipc")
                                             for y in range(1990, 2024)]
    with open(HERE / "hdr2025_1990_2023.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(keep)
        for r in rows:
            if not r["iso3"] or r["iso3"].startswith("ZZ"):
                continue  # regional and world aggregates
            w.writerow([r.get(k, "") for k in keep])


def _quarter_key(q: str) -> tuple:
    y, n = q.split(":Q")
    return int(y), int(n)


def refresh_rtdsm() -> None:
    import openpyxl  # noqa: PLC0415
    from openpyxl.reader import excel  # noqa: PLC0415

    d = DATASETS["rtdsm"]
    raw = RAW / "routputqvqd.xlsx"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"rtdsm: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    # the workbook's document properties carry a date openpyxl cannot parse; they are not needed
    excel.ExcelReader.read_properties = lambda self: None
    rows = list(openpyxl.load_workbook(raw, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    vint = [h.replace("ROUTPUT", "") for h in head[1:]]          # e.g. "65Q4"

    def full(v: str) -> str:
        yy = int(v[:2])
        return f"{1900 + yy if yy >= 60 else 2000 + yy}Q{v[-1]}"

    vint = [full(v) for v in vint]
    num = lambda x: float(x) if isinstance(x, (int, float)) else float("nan")  # noqa: E731
    data = {str(r[0]): [num(x) for x in r[1:]] for r in rows[1:] if r[0]}
    quarters = sorted(data, key=_quarter_key)
    keep_v = [i for i, v in enumerate(vint) if v >= "2007Q1"]
    with open(HERE / "rtdsm_2006_2010.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["quarter", *[vint[i] for i in keep_v]])
        for q in quarters:
            if 2006 <= _quarter_key(q)[0] <= 2010:
                w.writerow([q, *[_fmt(data[q][i]) if data[q][i] == data[q][i] else "" for i in keep_v]])
    # each quarter's annualized growth in the first vintage that reports it, and in the latest vintage
    with open(HERE / "rtdsm_first_latest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["quarter", "first", "latest"])
        for k in range(1, len(quarters)):
            q, p = quarters[k], quarters[k - 1]
            first = None
            for i in range(len(vint)):
                a, b = data[q][i], data[p][i]
                if a == a and b == b:
                    # a quarter already in the earliest vintage (1965Q4) has no first estimate in the data set
                    first = 100 * ((a / b) ** 4 - 1) if i > 0 else None
                    break
            a, b = data[q][-1], data[p][-1]
            latest = 100 * ((a / b) ** 4 - 1) if a == a and b == b else None
            if first is not None and latest is not None:
                w.writerow([q, f"{first:.3f}", f"{latest:.3f}"])


def refresh_draft1970() -> None:
    d = DATASETS["draft1970"]
    raw = RAW / "draft70yr.dat.txt"
    sha = _download(d["url"], raw)
    if d.get("sha256") and sha != d["sha256"]:
        print(f"draft1970: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    rows = [line.split() for line in raw.read_text().splitlines() if line.strip()]
    with open(HERE / "draft1970.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["day", "month", "rank"])
        for r in rows:
            w.writerow([int(r[0]), int(r[2]), int(r[1])])


@functools.lru_cache(maxsize=None)
def warheads(entity: str) -> dict:
    """A country's estimated nuclear warhead stockpile, 1945-2026 (``entity`` as Our World in Data names it, e.g.
    "United States", "Russia" (the Soviet Union before 1992)): ``{"year": [...], "value": [...]}``."""
    rows = [r for r in _read(HERE / "warheads_1945_2026.csv") if r["entity"] == entity]
    if not rows:
        raise KeyError(entity)
    return {"year": [int(r["year"]) for r in rows], "value": [int(r["number_of_warheads"]) for r in rows]}


def refresh_warheads() -> None:
    d = DATASETS["warheads"]
    raw = RAW / "nuclear-warhead-stockpiles.csv"
    sha = _download(d["url"], raw)
    if d.get("sha256") and sha != d["sha256"]:
        print(f"warheads: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    with open(raw, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(HERE / "warheads_1945_2026.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entity", "code", "year", "number_of_warheads"])
        for r in rows:
            w.writerow([r["entity"], r["code"], r["year"], r["number_of_warheads"]])


@functools.lru_cache(maxsize=None)
def so2(entity: str) -> dict:
    """Sulphur dioxide emissions, tonnes a year, 1900-2022, for one of the entities kept in the extract (as Our World
    in Data names them: "World", "United States", "China", ...): ``{"year": [...], "value": [...]}``."""
    rows = [r for r in _read(HERE / "so2_1900_2022.csv") if r["entity"] == entity]
    if not rows:
        raise KeyError(entity)
    return {"year": [int(r["year"]) for r in rows], "value": [float(r["so2_tonnes"]) for r in rows]}


def refresh_so2() -> None:
    d = DATASETS["so2"]
    raw = RAW / "so-emissions-by-world-region.csv"
    sha = _download(d["url"], raw)
    if d.get("sha256") and sha != d["sha256"]:
        print(f"so2: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    print(f"so2: sha256 {sha}")
    with open(raw, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["entity"] in d["entities"] and int(r["year"]) >= 1900]
    with open(HERE / "so2_1900_2022.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entity", "code", "year", "so2_tonnes"])
        for r in rows:
            w.writerow([r["entity"], r["code"], r["year"], r["emissions__pollutant_so2__sector_all_sectors"]])


def marriage(entity: str) -> dict:
    """Marriages a year per 1,000 people, for one of the countries kept in the extract (the United States from 1886,
    with gaps; the others from 1960): ``{"year": [...], "value": [...]}``."""
    rows = [r for r in _read(HERE / "marriage_rate.csv") if r["entity"] == entity]
    if not rows:
        raise KeyError(entity)
    return {"year": [int(r["year"]) for r in rows], "value": [float(r["rate"]) for r in rows]}


def refresh_marriage() -> None:
    d = DATASETS["marriage"]
    raw = RAW / "marriage-rate-per-1000-inhabitants.csv"
    sha = _download(d["url"], raw)
    if d.get("sha256") and sha != d["sha256"]:
        print(f"marriage: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    print(f"marriage: sha256 {sha}")
    with open(raw, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["entity"] in d["entities"]]
    with open(HERE / "marriage_rate.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entity", "code", "year", "rate"])
        for r in rows:
            w.writerow([r["entity"], r["code"], r["year"], r["value__gender_both__indicator_marriage_rate"]])


def democracy(entity: str) -> dict:
    """V-Dem's electoral democracy index (0 to 1, central estimate), 1789-2025 (South Africa from 1900), for one of
    the entities kept in the extract; "World" is Our World in Data's aggregate of the countries:
    ``{"year": [...], "value": [...]}``."""
    rows = [r for r in _read(HERE / "democracy_vdem.csv") if r["entity"] == entity]
    if not rows:
        raise KeyError(entity)
    return {"year": [int(r["year"]) for r in rows], "value": [float(r["index"]) for r in rows]}


def refresh_democracy() -> None:
    d = DATASETS["democracy"]
    raw = RAW / "electoral-democracy-index.csv"
    sha = _download(d["url"], raw)
    if d.get("sha256") and sha != d["sha256"]:
        print(f"democracy: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    print(f"democracy: sha256 {sha}")
    with open(raw, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["entity"] in d["entities"]]
    with open(HERE / "democracy_vdem.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entity", "code", "year", "index"])
        for r in rows:
            w.writerow([r["entity"], r["code"], r["year"], r["electdem_vdem__estimate_best"]])


MILLENNIUM_COLUMNS = {25: "population_000s", 42: "real_wage_1900_100"}     # sheet A1
MILLENNIUM_GDPPC = 8                                                        # sheet A21: England, real, 2013 pounds
MILLENNIUM_DAYS = 6          # sheet A48: real consumption earnings adjusted for days worked before 1750, 1900 = 100


def millennium() -> dict:
    """England from the Bank of England's millennium dataset: ``{"year": [...], "population": [...] (thousands),
    "real_wage": [...] (real consumption wages from daily wage rates, 1900 = 100), "earnings_days": [...] (the same
    adjusted for days worked a year before 1750, from Humphries and Weisdorf), "gdppc": [...] (real GDP per head, 2013
    pounds)}``, nan where a series has no value (wages from 1209, GDP per head from 1270, population from 1086)."""
    rows = _read(HERE / "boe_millennium_england.csv")
    return {"year": [int(r["year"]) for r in rows], "population": [_num(r["population_000s"]) for r in rows],
            "real_wage": [_num(r["real_wage_1900_100"]) for r in rows],
            "gdppc": [_num(r["gdppc_2013_pounds"]) for r in rows],
            "earnings_days": [_num(r["real_earnings_days_1900_100"]) for r in rows]}


def refresh_millennium() -> None:
    import openpyxl

    d = DATASETS["millennium"]
    raw = RAW / "a-millennium-of-macroeconomic-data-for-the-uk.xlsx"
    sha = _download(d["url"], raw)
    if d.get("sha256") and sha != d["sha256"]:
        print(f"millennium: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    print(f"millennium: sha256 {sha}")
    wb = openpyxl.load_workbook(raw, read_only=True, data_only=True)
    ws = wb["A1. Headline series"]
    out = []
    for row in ws.iter_rows(min_row=8, values_only=True):
        y = row[0]
        if not isinstance(y, (int, float)) or not 1086 <= y <= 2016:
            continue
        vals = {k: (row[j] if isinstance(row[j], (int, float)) else None) for j, k in MILLENNIUM_COLUMNS.items()}
        out.append((int(y), vals))
    gdppc, days = {}, {}
    for row in wb["A21. GDP per capita 1086+"].iter_rows(min_row=6, values_only=True):
        if isinstance(row[0], (int, float)) and isinstance(row[MILLENNIUM_GDPPC], (int, float)):
            gdppc[int(row[0])] = row[MILLENNIUM_GDPPC]
    for row in wb["A48. Real Earnings "].iter_rows(min_row=6, values_only=True):
        if isinstance(row[0], (int, float)) and isinstance(row[MILLENNIUM_DAYS], (int, float)):
            days[int(row[0])] = row[MILLENNIUM_DAYS]
    cols = [*MILLENNIUM_COLUMNS.values(), "gdppc_2013_pounds", "real_earnings_days_1900_100"]
    with open(HERE / "boe_millennium_england.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", *cols])
        for y, v in out:
            v["gdppc_2013_pounds"] = gdppc.get(y)
            v["real_earnings_days_1900_100"] = days.get(y)
            w.writerow([y, *[_fmt(v[k]) if v[k] is not None else "" for k in cols]])


def longrun(series: str, entity: str) -> dict:
    """One long-run series for one entity: ``series`` is "population", "life-expectancy", "children-born-per-woman"
    or "height" (men, by decade of birth): ``{"year": [...], "value": [...]}``."""
    key = {"height": "average-height-of-men-for-selected-countries"}.get(series, series)
    rows = [r for r in _read(HERE / "longrun_owid.csv") if r["series"] == key and r["entity"] == entity]
    if not rows:
        raise KeyError((series, entity))
    return {"year": [int(r["year"]) for r in rows], "value": [float(r["value"]) for r in rows]}


def refresh_longrun() -> None:
    d = DATASETS["longrun"]
    out = []
    for key, url in d["urls"].items():
        raw = RAW / f"{key}.csv"
        sha = _download(url, raw)
        rec = d["sha256"].get(key)
        if rec and not sha.startswith(rec):
            print(f"longrun {key}: the download differs from the recorded vintage ({sha[:16]} vs {rec})")
        print(f"longrun {key}: sha256 {sha}")
        col = d["columns"][key]
        with open(raw, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["entity"] in d["entities"] and r.get(col, "") != "":
                    out.append((key, r["entity"], r["code"], r["year"], r[col]))
    with open(HERE / "longrun_owid.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["series", "entity", "code", "year", "value"])
        w.writerows(out)


PWT_COLUMNS = ("countrycode", "country", "year", "rgdpo", "rgdpna", "rgdpe", "pop", "emp", "avh", "hc", "cn", "rnna",
               "labsh", "csh_c", "csh_i", "csh_g", "delta", "ctfp", "cgdpo", "ck", "irr")


def pwt(code: str | None = None, year: int | None = None) -> list[dict]:
    """Rows of the Penn World Table 11.0 extract (numbers as floats, nan where missing), for one country, one year,
    or all."""
    out = []
    for r in _read(HERE / "pwt110.csv"):
        if code and r["countrycode"] != code:
            continue
        if year and int(r["year"]) != year:
            continue
        row = {"countrycode": r["countrycode"], "country": r["country"], "year": int(r["year"])}
        for k in PWT_COLUMNS[3:]:
            row[k] = _num(r[k])
        out.append(row)
    return out


def refresh_pwt() -> None:
    import openpyxl

    d = DATASETS["pwt"]
    raw = RAW / "pwt110.xlsx"
    sha = _download(d["url"], raw)
    if d.get("sha256") and sha != d["sha256"]:
        print(f"pwt: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    print(f"pwt: sha256 {sha}")
    wb = openpyxl.load_workbook(raw, read_only=True, data_only=True)
    rows = wb["Data"].iter_rows(values_only=True)
    head = list(next(rows))
    idx = [head.index(c) for c in PWT_COLUMNS]
    with open(HERE / "pwt110.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(PWT_COLUMNS)
        for r in rows:
            vals = [r[i] for i in idx]
            if all(v is None for v in vals[3:]):
                continue
            w.writerow([vals[0], vals[1], int(vals[2])] + [_fmt(v) if isinstance(v, (int, float)) else ""
                                                           for v in vals[3:]])


AJR_COLUMNS = ("GDP", "Exprop", "Mort", "logMort", "Latitude", "Neo", "Africa", "Asia", "Namer", "Samer")


def ajr() -> dict:
    """Acemoglu, Johnson and Robinson's 64 countries (no names in this copy): ``{column: [values]}`` for
    :data:`AJR_COLUMNS`."""
    rows = _read(HERE / "ajr_hdm.csv")
    return {c: [float(r[c]) for r in rows] for c in AJR_COLUMNS}


def refresh_ajr() -> None:
    import tarfile

    from explainer.psychology import rdata

    d = DATASETS["ajr"]
    raw = RAW / "hdm_0.3.2.tar.gz"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"ajr: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    print(f"ajr: sha256 {sha}")
    with tarfile.open(raw, "r:gz") as tf:
        member = tf.getmember("hdm/data/AJR.rda")
        blob = tf.extractfile(member).read()
    tmp = RAW / "AJR.rda"
    tmp.write_bytes(blob)
    obj = rdata.load(tmp)[0][1]
    names = obj["attrs"]["names"]["value"]
    cols = {n: c["value"] for n, c in zip(names, obj["value"])}
    n = len(cols["GDP"])
    with open(HERE / "ajr_hdm.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(AJR_COLUMNS)
        for i in range(n):
            w.writerow([_fmt(float(cols[c][i])) for c in AJR_COLUMNS])


SHILLER_COLUMNS = ("year", "P", "D", "E", "R", "RLONG", "CPI", "RealR", "C", "RealP", "Pstar", "PstarR", "PstarC", "RealD",
                   "Return")


def shiller() -> dict:
    """Shiller's annual series (``{column: [values]}``, NaN where blank): see ``DATASETS["shiller"]["units"]``.
    ``Return`` for year t is the real return from January of t to January of t + 1; ``RealR`` the gross real return on
    a one-year bond bought in January of t; ``C`` real consumption per head in year t."""
    rows = _read(HERE / "shiller_annual.csv")
    return {c: [(_num(r[c]) if c != "year" else int(r[c])) for r in rows] for c in SHILLER_COLUMNS}


def refresh_shiller() -> None:
    import openpyxl

    d = DATASETS["shiller"]
    raw = RAW / "shiller_chapt26.xlsx"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"shiller: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    print(f"shiller: sha256 {sha}")
    wb = openpyxl.load_workbook(raw, read_only=True, data_only=True)
    idx = {"year": 0, "P": 1, "D": 2, "E": 3, "R": 4, "RLONG": 5, "CPI": 6, "RealR": 7, "C": 8, "RealP": 10,
           "Pstar": 11, "PstarR": 12, "PstarC": 13, "RealD": 14, "Return": 15}
    with open(HERE / "shiller_annual.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(SHILLER_COLUMNS)
        for r in wb["Data"].iter_rows(values_only=True):
            if not isinstance(r[0], (int, float)):
                continue
            w.writerow([int(r[0])] + [_fmt(r[idx[c]]) if isinstance(r[idx[c]], (int, float)) else ""
                                      for c in SHILLER_COLUMNS[1:]])


REFRESH = {"draft1970": refresh_draft1970, "ajr": refresh_ajr, "maddison2023": refresh_maddison, "fred": refresh_fred, "spf": refresh_spf,
           "pinksheet": refresh_pinksheet, "psd_coffee": refresh_psd_coffee, "wdi": refresh_wdi, "hdr": refresh_hdr,
           "rtdsm": refresh_rtdsm, "warheads": refresh_warheads, "so2": refresh_so2,
           "marriage": refresh_marriage, "democracy": refresh_democracy, "millennium": refresh_millennium,
           "longrun": refresh_longrun, "pwt": refresh_pwt, "shiller": refresh_shiller}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", nargs="*", choices=list(REFRESH), help="download again and rewrite the extract")
    args = ap.parse_args()
    for name in args.refresh or []:
        print(f"refreshing {name} ...")
        REFRESH[name]()
    if not args.refresh:
        for name, d in DATASETS.items():
            print(f"{name:14s} {d['vintage']}  {d['title']}  ({', '.join(d['files'])})")


if __name__ == "__main__":
    main()
