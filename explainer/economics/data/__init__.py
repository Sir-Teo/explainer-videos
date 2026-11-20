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
# Part 24: the labour market's stocks and flows: unemployment by duration, the labour force, job openings, hires and
# separations (JOLTS), and the Congressional Budget Office's natural rate
FRED_SERIES["UNEMPLOY"] = ("Unemployment level", "thousands of persons, seasonally adjusted", "monthly",
                           "U.S. Bureau of Labor Statistics")
FRED_SERIES["UEMPLT5"] = ("Number unemployed for less than 5 weeks", "thousands of persons, seasonally adjusted",
                          "monthly", "U.S. Bureau of Labor Statistics")
FRED_SERIES["UEMP27OV"] = ("Number unemployed for 27 weeks and over", "thousands of persons, seasonally adjusted",
                           "monthly", "U.S. Bureau of Labor Statistics")
FRED_SERIES["CLF16OV"] = ("Civilian labor force level", "thousands of persons, seasonally adjusted", "monthly",
                          "U.S. Bureau of Labor Statistics")
FRED_SERIES["JTSJOL"] = ("Job openings: total nonfarm", "level in thousands, seasonally adjusted", "monthly",
                         "U.S. Bureau of Labor Statistics")
FRED_SERIES["JTSHIL"] = ("Hires: total nonfarm", "level in thousands, seasonally adjusted", "monthly",
                         "U.S. Bureau of Labor Statistics")
FRED_SERIES["JTSTSL"] = ("Total separations: total nonfarm", "level in thousands, seasonally adjusted", "monthly",
                         "U.S. Bureau of Labor Statistics")
FRED_SERIES["JTSQUL"] = ("Quits: total nonfarm", "level in thousands, seasonally adjusted", "monthly",
                         "U.S. Bureau of Labor Statistics")
FRED_SERIES["OPHNFB"] = ("Nonfarm business sector: labor productivity (output per hour) for all workers",
                         "index 2017 = 100, seasonally adjusted", "quarterly", "U.S. Bureau of Labor Statistics")
FRED_SERIES["NROU"] = ("Noncyclical rate of unemployment", "percent, not seasonally adjusted", "quarterly",
                       "U.S. Congressional Budget Office")
# Part 25: money
FRED_SERIES["M2SL"] = ("M2", "billions of dollars, seasonally adjusted", "monthly",
                       "Board of Governors of the Federal Reserve System (US)")
FRED_SERIES["M1SL"] = ("M1", "billions of dollars, seasonally adjusted (savings deposits included from May 2020)",
                       "monthly", "Board of Governors of the Federal Reserve System (US)")
FRED_SERIES["BOGMBASE"] = ("Monetary base; total", "billions of dollars, not seasonally adjusted", "monthly",
                           "Board of Governors of the Federal Reserve System (US)")
FRED_SERIES["CURRCIR"] = ("Currency in circulation", "billions of dollars, not seasonally adjusted", "monthly",
                          "Board of Governors of the Federal Reserve System (US)")
FRED_SERIES["TOTRESNS"] = ("Reserves of depository institutions: total", "billions of dollars, not seasonally "
                           "adjusted", "monthly", "Board of Governors of the Federal Reserve System (US)")
FRED_SERIES["M2V"] = ("Velocity of M2 money stock", "ratio, seasonally adjusted", "quarterly",
                      "Federal Reserve Bank of St. Louis")
FRED_SERIES["GDP"] = ("Gross domestic product", "billions of dollars, seasonally adjusted annual rate", "quarterly",
                      "U.S. Bureau of Economic Analysis")
# Part 26: banks and runs
FRED_SERIES["X14AICBS"] = ("Suspensions among all incorporated commercial banks", "number", "annual",
                           "Board of Governors of the Federal Reserve System, Banking and Monetary Statistics (NBER)")
FRED_SERIES["M09036USM155NNBR"] = ("Number of suspended banks, all banks, United States", "number", "monthly",
                                   "NBER Macrohistory Database")
FRED_SERIES["FEDFUNDS"] = ("Federal funds effective rate", "percent, not seasonally adjusted", "monthly",
                           "Board of Governors of the Federal Reserve System (US)")
FRED_SERIES["SNDR"] = ("National deposit rate: savings", "percent, not seasonally adjusted", "monthly",
                       "Federal Deposit Insurance Corporation")
FRED_SERIES["NDR12MCD"] = ("National deposit rate: 12-month CD", "percent, not seasonally adjusted", "monthly",
                           "Federal Deposit Insurance Corporation")
FRED_SERIES["GS10"] = ("Market yield on US Treasury securities at 10-year constant maturity", "percent, monthly "
                       "average", "monthly", "Board of Governors of the Federal Reserve System (US)")
FRED_SERIES["GS2"] = ("Market yield on US Treasury securities at 2-year constant maturity", "percent, monthly average",
                      "monthly", "Board of Governors of the Federal Reserve System (US)")
FRED_SERIES["DPSSCBW027SBOG"] = ("Deposits, small domestically chartered commercial banks", "billions of dollars, "
                                 "seasonally adjusted", "weekly", "Board of Governors of the Federal Reserve System (US)")
FRED_SERIES["DPSLCBW027SBOG"] = ("Deposits, large domestically chartered commercial banks", "billions of dollars, "
                                 "seasonally adjusted", "weekly", "Board of Governors of the Federal Reserve System (US)")
FRED_SERIES["EQTA"] = ("Equity capital to total assets for all US banks", "percent, not seasonally adjusted",
                       "quarterly", "Federal Financial Institutions Examination Council (US)")
FRED_SERIES["MMMFFAQ027S"] = ("Money market funds; total financial assets, level", "millions of dollars, not "
                              "seasonally adjusted", "quarterly", "Board of Governors of the Federal Reserve System (US)")
FRED_SERIES["GNPCA"] = ("Real gross national product", "billions of chained 2017 dollars", "annual", "BEA")
FRED_SERIES["USREC"] = ("NBER based recession indicators for the United States, from the period following the peak "
                        "through the trough", "1 = recession, 0 = expansion", "monthly",
                        "Federal Reserve Bank of St. Louis, from the NBER's business cycle dates")
FRED_SERIES["M1476BUSM027NNBR"] = ("Monetary gold stock for the United States", "billions of dollars, not seasonally "
                                   "adjusted", "monthly", "NBER Macrohistory Database")
FRED_SERIES["GDPPOT"] = ("Real potential gross domestic product", "billions of chained 2017 dollars", "quarterly",
                         "Congressional Budget Office")
FRED_SERIES["IRSTCI01JPM156N"] = ("Interest rates: immediate rates (< 24 hours): call money/interbank rate: total for "
                                  "Japan", "percent a year", "monthly", "OECD Main Economic Indicators")
FRED_SERIES["MICH"] = ("University of Michigan: inflation expectation (median expected price change over the next 12 "
                       "months)", "percent", "monthly", "University of Michigan, Surveys of Consumers")
FRED_SERIES["T5YIEM"] = ("5-year breakeven inflation rate", "percent, monthly average", "monthly",
                         "Federal Reserve Bank of St. Louis, from Treasury yields")
FRED_SERIES["CPILFESL"] = ("Consumer price index for all urban consumers: all items less food and energy",
                           "index 1982-84 = 100, seasonally adjusted", "monthly", "BLS")
FRED_SERIES["GPDIC1"] = ("Real gross private domestic investment", "billions of chained 2017 dollars, seasonally "
                         "adjusted annual rate", "quarterly", "BEA")
FRED_SERIES["HOANBS"] = ("Nonfarm business sector: hours worked for all workers", "index 2017 = 100, seasonally "
                         "adjusted", "quarterly", "BLS")
FRED_SERIES["A011RA3Q086SBEA"] = ("Real gross private domestic investment: fixed investment: residential (chain-type "
                                  "quantity index)", "index 2017 = 100, seasonally adjusted", "quarterly", "BEA")
FRED_SERIES["A008RA3Q086SBEA"] = ("Real gross private domestic investment: fixed investment: nonresidential (chain-type "
                                  "quantity index)", "index 2017 = 100, seasonally adjusted", "quarterly", "BEA")

FRED_SERIES["GDPDEF"] = ("Gross domestic product: implicit price deflator", "index 2017 = 100, seasonally adjusted",
                         "quarterly", "BEA")
FRED_SERIES["PCEPILFE"] = ("Personal consumption expenditures excluding food and energy (chain-type price index)",
                           "index 2017 = 100, seasonally adjusted", "monthly", "BEA")
FRED_SERIES["CORESTICKM159SFRBATL"] = ("Sticky price consumer price index less food and energy", "percent change from "
                                       "a year ago, seasonally adjusted", "monthly", "Federal Reserve Bank of Atlanta")
FRED_SERIES["COREFLEXCPIM159SFRBATL"] = ("Flexible price consumer price index less food and energy", "percent change "
                                         "from a year ago, seasonally adjusted", "monthly",
                                         "Federal Reserve Bank of Atlanta")

FRED_SERIES["WALCL"] = ("Federal Reserve: total assets (Wednesday level)", "millions of dollars", "weekly",
                        "Board of Governors of the Federal Reserve System")
FRED_SERIES["WRESBAL"] = ("Reserve balances with Federal Reserve Banks (week average)", "millions of dollars", "weekly",
                          "Board of Governors of the Federal Reserve System")
FRED_SERIES["IOER"] = ("Interest rate on excess reserves (discontinued July 2021)", "percent", "daily",
                       "Board of Governors of the Federal Reserve System")
FRED_SERIES["IORB"] = ("Interest rate on reserve balances", "percent", "daily",
                       "Board of Governors of the Federal Reserve System")
FRED_SERIES["DGS10"] = ("10-year Treasury constant maturity yield", "percent", "daily",
                        "Board of Governors of the Federal Reserve System")
FRED_SERIES["DFII10"] = ("10-year Treasury inflation-indexed constant maturity yield", "percent", "daily",
                         "Board of Governors of the Federal Reserve System")
FRED_SERIES["GS1"] = ("1-year Treasury constant maturity yield", "percent", "monthly",
                      "Board of Governors of the Federal Reserve System")
FRED_SERIES["PPIACO"] = ("Producer price index by commodity: all commodities", "index 1982 = 100", "monthly", "BLS")
FRED_SERIES["ECBDFR"] = ("ECB deposit facility rate for the euro area", "percent", "daily", "European Central Bank")
FRED_SERIES["RESPPLLOPNWW"] = ("Federal Reserve: earnings remittances due to the U.S. Treasury (Wednesday level; "
                               "negative: the deferred asset)", "millions of dollars", "weekly",
                               "Board of Governors of the Federal Reserve System")
FRED_SERIES["FYFSGDA188S"] = ("Federal surplus or deficit as a percent of GDP (fiscal years)", "percent", "annual",
                              "Office of Management and Budget")
FRED_SERIES["GFDEGDQ188S"] = ("Federal debt: total public debt as a percent of GDP", "percent", "quarterly",
                              "Office of Management and Budget; Federal Reserve Bank of St. Louis")
FRED_SERIES["FYGFGDQ188S"] = ("Federal debt held by the public as a percent of GDP", "percent", "quarterly",
                              "Office of Management and Budget; Federal Reserve Bank of St. Louis")
FRED_SERIES["A091RC1Q027SBEA"] = ("Federal government current expenditures: interest payments", "billions of "
                                  "dollars, SAAR", "quarterly", "BEA")
FRED_SERIES["IRLTLT01GRM156N"] = ("Long-term (10-year) government bond yield, Greece", "percent", "monthly",
                                  "OECD Main Economic Indicators")
FRED_SERIES["FEDTARMDLR"] = ("FOMC Summary of Economic Projections: the federal funds rate, median, longer run",
                             "percent", "quarterly (from 2012)", "Board of Governors of the Federal Reserve System")
FRED_SERIES["DFEDTAR"] = ("Federal funds target rate (discontinued December 2008)", "percent", "daily",
                          "Board of Governors of the Federal Reserve System")
FRED_SERIES["DFEDTARU"] = ("Federal funds target range, upper limit (from December 2008)", "percent", "daily",
                           "Board of Governors of the Federal Reserve System")
FRED_SERIES["DRSFRMACBS"] = ("Delinquency rate on single-family residential mortgages, booked in domestic offices, "
                             "all commercial banks", "percent, seasonally adjusted", "quarterly",
                             "Board of Governors of the Federal Reserve System")
FRED_SERIES["TEDRATE"] = ("TED spread (3-month LIBOR minus 3-month Treasury bill; discontinued January 2022)",
                          "percent", "daily", "Federal Reserve Bank of St. Louis")
FRED_SERIES["SWPT"] = ("Assets: other: central bank liquidity swaps (Wednesday level)", "millions of dollars", "weekly",
                       "Board of Governors of the Federal Reserve System")
FRED_SERIES["BAA10Y"] = ("Moody's seasoned Baa corporate bond yield relative to the 10-year Treasury", "percent",
                         "daily", "Federal Reserve Bank of St. Louis (Moody's)")
FRED_SERIES["HDTGPDUSQ163N"] = ("Household debt to GDP for the United States", "percent of GDP", "quarterly",
                                "International Monetary Fund")
for _c, _n in (("TH", "Thai baht"), ("KO", "South Korean won"), ("MX", "Mexican peso")):
    FRED_SERIES[f"EX{_c}US"] = (f"{_n}s to one US dollar", "currency units per dollar, not seasonally adjusted",
                                "monthly", "Board of Governors of the Federal Reserve System (H.10)")
for _c, _n in (("IT", "Italy"), ("ES", "Spain"), ("DE", "Germany"), ("GB", "the United Kingdom")):
    FRED_SERIES[f"IRLTLT01{_c}M156N"] = (f"Long-term (10-year) government bond yield, {_n}", "percent", "monthly",
                                         "OECD Main Economic Indicators")

FRED_RETRIEVED = {s: "2026-11-19" for s in (
    "GDPA", "GDIA", "PCECA", "GPDIA", "GCEA", "EXPGSA", "IMPGSA", "A033RC1A027NBEA", "A191RD3A086NBEA", "U1RATE",
    "U2RATE", "U4RATE", "U5RATE", "U6RATE", "CIVPART", "EMRATIO", "CPIAUCSL", "SUUR0000SA0", "PCEPI",
    "LABSHPUSA156NRUG", "B230RC0A052NBEA", "PCECCA", "DPCERG3A086NBEA", "TB3MS", "MCOILBRENTEU", "MCOILWTICO", "APU0000717311", "APU000074714", "CUSR0000SETA02", "CUSR0000SETA01", *(f"{c}{t}" for c in PCE_CATEGORIES for t in ("RG3A086NBEA",
                                                                                         "RC1A027NBEA")))}
FRED_RETRIEVED.update({s: "2026-11-20" for s in ("PCECC96", "DSPIC96", "PSAVERT", "PCE", "PCEND", "PCES",
                                                  "DNDGRG3M086SBEA", "DSERRG3M086SBEA", "CSUSHPINSA",
                                                  "CUSR0000SEHA", "UNEMPLOY", "UEMPLT5", "UEMP27OV", "CLF16OV",
                                                  "JTSJOL", "JTSHIL", "JTSTSL", "JTSQUL", "NROU", "OPHNFB",
                                                  "M2SL", "M1SL", "BOGMBASE", "CURRCIR", "TOTRESNS", "M2V", "GDP",
                                                  "X14AICBS", "M09036USM155NNBR", "FEDFUNDS", "SNDR", "NDR12MCD",
                                                  "GS10", "GS2", "DPSSCBW027SBOG", "DPSLCBW027SBOG", "EQTA",
                                                  "MMMFFAQ027S", "GNPCA", "USREC", "M1476BUSM027NNBR",
                                                  "GDPPOT", "IRSTCI01JPM156N", "MICH", "T5YIEM", "CPILFESL",
                                                  "GPDIC1", "HOANBS", "A011RA3Q086SBEA",
                                                  "A008RA3Q086SBEA", "GDPDEF", "PCEPILFE",
                                                  "CORESTICKM159SFRBATL", "COREFLEXCPIM159SFRBATL", "WALCL",
                                                  "WRESBAL", "IOER", "IORB", "DGS10", "DFII10", "GS1", "PPIACO",
                                                  "IRLTLT01ITM156N", "IRLTLT01ESM156N", "IRLTLT01DEM156N",
                                                  "ECBDFR", "RESPPLLOPNWW", "DFEDTAR", "DFEDTARU",
                                                  "FEDTARMDLR", "IRLTLT01GBM156N", "FYFSGDA188S", "GFDEGDQ188S",
                                                  "FYGFGDQ188S", "A091RC1Q027SBEA", "IRLTLT01GRM156N")})
OPEN_FRED = ("EXUSUK", "EXGEUS", "EXJPUS", "EXSZUS", "EXCAUS", "EXUSEU", "EXUSAL", "EXUSNZ", "DEXCHUS",
             *(f"IR3TIB01{c}M156N" for c in ("US", "GB", "JP", "CH", "CA", "DE", "AU", "NZ")), "IR", "TWEXBMTH",
             "DTWEXBGS", "IIPUSNETIQ", "IEABC", "TRESEGGBM052N", "VIXCLS", "DEXUSUK", "DEXJPUS", "DEXCAUS",
             "DEXSZUS", "IREXFUELS")
for _k, _d in (("EXUSUK", "US dollars to one UK pound"), ("EXGEUS", "German marks to one US dollar (to 2001)"),
               ("EXJPUS", "Japanese yen to one US dollar"), ("EXSZUS", "Swiss francs to one US dollar"),
               ("EXCAUS", "Canadian dollars to one US dollar"), ("EXUSEU", "US dollars to one euro (from 1999)"),
               ("EXUSAL", "US dollars to one Australian dollar"), ("EXUSNZ", "US dollars to one New Zealand dollar")):
    FRED_SERIES[_k] = (_d, "monthly average, not seasonally adjusted", "monthly",
                       "Board of Governors of the Federal Reserve System (H.10)")
for _k, _d in (("DEXUSUK", "US dollars to one UK pound"), ("DEXJPUS", "Japanese yen to one US dollar"),
               ("DEXCAUS", "Canadian dollars to one US dollar"), ("DEXSZUS", "Swiss francs to one US dollar")):
    FRED_SERIES[_k] = (_d, "noon buying rates in New York", "daily",
                       "Board of Governors of the Federal Reserve System (H.10)")
FRED_SERIES["DEXCHUS"] = ("Chinese yuan renminbi to one US dollar", "noon buying rates in New York", "daily",
                          "Board of Governors of the Federal Reserve System (H.10)")
for _c, _n in (("US", "the United States"), ("GB", "the United Kingdom"), ("JP", "Japan"), ("CH", "Switzerland"),
               ("CA", "Canada"), ("DE", "Germany (the euro area from 1999)"), ("AU", "Australia"),
               ("NZ", "New Zealand")):
    FRED_SERIES[f"IR3TIB01{_c}M156N"] = (f"3-month interbank rate, {_n}", "percent a year", "monthly",
                                        "OECD Main Economic Indicators")
FRED_SERIES["IR"] = ("Import price index (end use): all commodities", "index 2000 = 100", "monthly",
                     "US Bureau of Labor Statistics")
FRED_SERIES["IREXFUELS"] = ("Import price index (end use): all imports excluding fuels", "index December 2001 = 100",
                            "monthly", "US Bureau of Labor Statistics")
FRED_SERIES["TWEXBMTH"] = ("Trade weighted US dollar index: broad (goods), discontinued 2019",
                           "index January 1997 = 100", "monthly", "Board of Governors of the Federal Reserve System")
FRED_SERIES["DTWEXBGS"] = ("Nominal broad US dollar index (goods and services)", "index January 2006 = 100", "daily",
                           "Board of Governors of the Federal Reserve System")
FRED_SERIES["IIPUSNETIQ"] = ("US net international investment position", "millions of dollars", "quarterly", "BEA")
FRED_SERIES["IEABC"] = ("US balance on current account", "millions of dollars, seasonally adjusted", "quarterly",
                        "BEA")
FRED_SERIES["TRESEGGBM052N"] = ("Total reserves excluding gold for the United Kingdom", "millions of US dollars",
                                "monthly", "IMF International Financial Statistics")
FRED_SERIES["VIXCLS"] = ("CBOE volatility index: VIX", "index", "daily", "Chicago Board Options Exchange")
JST_FRED = ("DRSFRMACBS", "TEDRATE", "SWPT", "BAA10Y", "HDTGPDUSQ163N", "EXTHUS", "EXKOUS", "EXMXUS")
FRED_RETRIEVED.update({s: "2026-11-20" for s in JST_FRED})
FRED_RETRIEVED.update({s: "2026-11-20" for s in OPEN_FRED})
TRADE_FRED = ("B235RC1A027NBEA", "A255RC1A027NBEA", "A640RC1A027NBEA", "A650RC1A027NBEA", "B641RC1A027NBEA",
              "B651RC1A027NBEA", "A642RC1A027NBEA", "A652RC1A027NBEA")
FRED_SERIES["B235RC1A027NBEA"] = ("Federal government current tax receipts: taxes on production and imports: customs "
                                  "duties", "billions of dollars", "annual", "U.S. Bureau of Economic Analysis")
FRED_SERIES["A255RC1A027NBEA"] = ("Current payments to the rest of the world: imports of goods", "billions of dollars",
                                  "annual", "U.S. Bureau of Economic Analysis")
for _k, _d in (("A640RC1A027NBEA", "Exports of goods: capital goods, except automotive"),
               ("A650RC1A027NBEA", "Imports of goods: capital goods, except automotive"),
               ("B641RC1A027NBEA", "Exports of goods: automotive vehicles, engines, and parts"),
               ("B651RC1A027NBEA", "Imports of goods: automotive vehicles, engines, and parts"),
               ("A642RC1A027NBEA", "Exports of goods: consumer goods, except food and automotive"),
               ("A652RC1A027NBEA", "Imports of goods: consumer goods, except automotive")):
    FRED_SERIES[_k] = (_d, "billions of dollars", "annual", "U.S. Bureau of Economic Analysis (NIPA table 4.2.5)")
FRED_RETRIEVED.update({s: "2026-11-20" for s in TRADE_FRED})
CHINA_FRED = ("IMPCH", "EXPCH", "MANEMP")
FRED_SERIES["IMPCH"] = ("U.S. imports of goods by customs basis from China", "millions of dollars", "monthly",
                        "U.S. Census Bureau")
FRED_SERIES["EXPCH"] = ("U.S. exports of goods by F.A.S. basis to China", "millions of dollars", "monthly",
                        "U.S. Census Bureau")
FRED_SERIES["MANEMP"] = ("All employees, manufacturing", "thousands of persons, seasonally adjusted", "monthly",
                         "U.S. Bureau of Labor Statistics")
FRED_RETRIEVED.update({s: "2026-11-20" for s in CHINA_FRED})
# Part 37: the S&P CoreLogic Case-Shiller indices of the twenty metropolitan areas, and working from home
CASE_SHILLER_METROS = {"AT": "Atlanta", "BO": "Boston", "CR": "Charlotte", "CH": "Chicago", "CE": "Cleveland",
                       "DA": "Dallas", "DN": "Denver", "DE": "Detroit", "LV": "Las Vegas", "LX": "Los Angeles",
                       "MI": "Miami", "MN": "Minneapolis", "NY": "New York", "PH": "Phoenix", "PO": "Portland",
                       "SD": "San Diego", "SF": "San Francisco", "SE": "Seattle", "TP": "Tampa", "WD": "Washington"}
CITY_FRED = (*(f"{k}XRSA" for k in CASE_SHILLER_METROS), "WFHCOVIDMATQUESTION")
for _k, _n in CASE_SHILLER_METROS.items():
    FRED_SERIES[f"{_k}XRSA"] = (f"S&P CoreLogic Case-Shiller {_n} Home Price Index", "index January 2000 = 100, "
                                "seasonally adjusted", "monthly", "S&P Dow Jones Indices LLC")
FRED_SERIES["WFHCOVIDMATQUESTION"] = ("Work from home rate (Survey of Working Arrangements and Attitudes)",
                                      "percent of full paid working days, not seasonally adjusted; 2019 from the "
                                      "American Time Use Survey", "monthly",
                                      "J. M. Barrero, N. Bloom and S. J. Davis (CC BY 4.0)")
FRED_RETRIEVED.update({s: "2026-11-20" for s in CITY_FRED})
# Part 38: the federal minimum wage
FRED_SERIES["FEDMINNFRWG"] = ("Federal minimum hourly wage for nonfarm workers for the United States",
                              "dollars an hour, not seasonally adjusted", "monthly",
                              "U.S. Department of Labor, Wage and Hour Division")
FRED_RETRIEVED["FEDMINNFRWG"] = "2026-11-20"
# Part 39: the wage structure: median weekly earnings of full-time workers by education and sex, the deciles, the
# employment of college and high-school graduates, the labour share, and prime-age employment (BLS)
_LEU = "Employed full time: median usual weekly nominal earnings (second quartile): wage and salary workers"
WAGE_FRED = {
    "LEU0252918500A": (f"{_LEU}: bachelor's degree and higher: 25 years and over", "dollars a week", "annual"),
    "LEU0252917300A": (f"{_LEU}: high school graduates, no college: 25 years and over", "dollars a week", "annual"),
    "LEU0252916700A": (f"{_LEU}: less than a high school diploma: 25 years and over", "dollars a week", "annual"),
    "LEU0252881500A": (f"{_LEU}: 16 years and over", "dollars a week", "annual"),
    "LEU0252881600A": ("Employed full time: median usual weekly real earnings: wage and salary workers: 16 years and "
                       "over", "1982-84 dollars a week", "annual"),
    "LEU0252881900A": ("Employed full time: median usual weekly real earnings: wage and salary workers: 16 years and "
                       "over: men", "1982-84 dollars a week", "annual"),
    "LEU0252882800A": ("Employed full time: median usual weekly real earnings: wage and salary workers: 16 years and "
                       "over: women", "1982-84 dollars a week", "annual"),
    "LEU0252911200A": ("Employed full time: usual weekly nominal earnings (first decile): wage and salary workers: 16 "
                       "years and over", "dollars a week", "annual"),
    "LEU0252911500A": ("Employed full time: usual weekly nominal earnings (ninth decile): wage and salary workers: 16 "
                       "years and over", "dollars a week", "annual"),
    "LNU02027662": ("Employment level: bachelor's degree and higher, 25 years and over", "thousands of persons, not "
                    "seasonally adjusted", "monthly"),
    "LNU02027660": ("Employment level: high school graduates, no college, 25 years and over", "thousands of persons, "
                    "not seasonally adjusted", "monthly"),
    "PRS85006173": ("Nonfarm business sector: labor share for all workers", "index 2017 = 100, seasonally adjusted",
                    "quarterly"),
    "LNS12300060": ("Employment-population ratio: 25-54 years", "percent, seasonally adjusted", "monthly"),
}
for _k, (_t, _u, _f) in WAGE_FRED.items():
    FRED_SERIES[_k] = (_t, _u, _f, "U.S. Bureau of Labor Statistics")
FRED_RETRIEVED.update({s: "2026-11-20" for s in WAGE_FRED})

SPF_FILES = ("median_rgdp_level", "median_rgdp_growth", "median_recess_level")
SPF_URL = ("https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/"
           "data-files/files/{}.xlsx")
RAMEY_URL = "https://econweb.ucsd.edu/~vramey/research/{}"
HLW_URL = ("https://www.newyorkfed.org/medialibrary/media/research/economists/williams/data/"
           "Holston_Laubach_Williams_current_estimates.xlsx")
GB_URL = ("https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/greenbook-data/documentation/"
          "GBweb_Row_Format.xlsx")
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
    "wdi_money": {
        "title": "World Development Indicators, 1960 onward: broad money growth, consumer-price inflation, GDP-deflator "
                 "inflation, real GDP growth, and broad money as a share of GDP, by country and year",
        "publisher": "World Bank",
        "citation": "World Bank, World Development Indicators (API, last updated 11 November 2026), indicators "
                    "FM.LBL.BMNY.ZG, FP.CPI.TOTL.ZG, NY.GDP.DEFL.KD.ZG, NY.GDP.MKTP.KD.ZG, FM.LBL.BMNY.GD.ZS, "
                    "retrieved 2026-11-20",
        "short": "World Bank WDI (money and prices), Nov 2026",
        "url": "https://api.worldbank.org/v2/country/all/indicator/{}?format=json&date={}:{}&per_page=5000",
        "licence": "CC BY 4.0 (World Bank open data)",
        "units": "annual percent changes (money, CPI, deflator, real GDP); percent of GDP (broad money)",
        "vintage": "2026-11-20",
        "files": ("wdi_money_1960_2024.csv",),
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
    "greenbook": {
        "title": "Tealbook (formerly Greenbook) projections: the price index for GDP (gPGDP), with the Survey of "
                 "Professional Forecasters' median forecasts of the same index",
        "publisher": "Federal Reserve Bank of Philadelphia (from the Board of Governors' Greenbooks)",
        "citation": "Federal Reserve Bank of Philadelphia, Philadelphia Fed's Tealbook (formerly Greenbook) Data Set, "
                    "GBweb_Row_Format.xlsx, sheet gPGDP (Greenbooks of 1967-2020); Survey of Professional "
                    "Forecasters, median_pgdp_growth.xlsx; retrieved 2026-11-20",
        "short": "Philadelphia Fed, Tealbook (Greenbook) Data Set and SPF",
        "url": GB_URL,
        "licence": "free to use with attribution to the Federal Reserve Bank of Philadelphia",
        "units": "annualized quarter-on-quarter growth of the GDP (before December 1991, GNP) price index, percent",
        "vintage": "2026-11-20",
        "sha256": "2a676d7e545021ef42ace3670325c0892dcf7d1e121c1e58f7ff79ef33b84d28",
        "files": ("greenbook_pgdp.csv", "spf_pgdp_growth.csv"),
    },
    "hlw": {
        "title": "Holston, Laubach and Williams: estimates of the natural rate of interest (r*), trend growth and "
                 "other determinants, one-sided, quarterly from 1961",
        "publisher": "Federal Reserve Bank of New York",
        "citation": "Federal Reserve Bank of New York, Measuring the Natural Rate of Interest, "
                    "Holston_Laubach_Williams_current_estimates.xlsx (final data point 2026Q2), retrieved 2026-11-20; "
                    "the model of Holston, Laubach and Williams, FRBNY Staff Report 1063 (2023)",
        "short": "New York Fed, Holston-Laubach-Williams estimates",
        "url": HLW_URL,
        "licence": "public research data of the Federal Reserve Bank of New York, used with attribution",
        "units": "percent a year (r* and trend growth g); z in percentage points",
        "vintage": "2026-11-20",
        "sha256": "120f1587a5501d9623f00fb65e492df714b303559806e60f728bc3e575b5aa46",
        "files": ("hlw_rstar.csv",),
    },
    "ramey_zubairy": {
        "title": "Ramey and Zubairy's US quarterly data, 1889-2015: government purchases, GDP, prices, population, "
                 "unemployment, military spending news, potential output, the T-bill rate and a zero-bound dummy",
        "publisher": "Valerie A. Ramey and Sarah Zubairy (replication files)",
        "citation": "V. A. Ramey and S. Zubairy, \"Government Spending Multipliers in Good Times and in Bad: Evidence "
                    "from U.S. Historical Data\", Journal of Political Economy 126(2) (2018), replication files "
                    "(rzdatnew.csv), retrieved 2026-11-20",
        "short": "Ramey and Zubairy (2018), replication data",
        "url": RAMEY_URL.format("Ramey_Zubairy_replication_codes.zip"),
        "licence": "posted by the authors for replication; used with citation",
        "units": "nominal values in billions of dollars at annual rates; news in billions (present value); percent",
        "vintage": "2026-11-20",
        "sha256": "e268f8d4abc997227401d5b5f218d0cfa3c527cb9091f6e715baa5a7a6391d07",
        "files": ("ramey_zubairy.csv",),
    },
    "ramey_tax": {
        "title": "Ramey's Handbook tax data, 1945-2015, quarterly: GDP, prices, population, tax receipts and Romer and "
                 "Romer's exogenous and endogenous tax changes as ratios to GDP",
        "publisher": "Valerie A. Ramey (replication files for the Handbook of Macroeconomics)",
        "citation": "V. A. Ramey, \"Macroeconomic Shocks and Their Propagation\", Handbook of Macroeconomics 2A "
                    "(2016), replication files (homtaxdat.xlsx), with C. D. Romer and D. H. Romer's narrative tax "
                    "changes (AER 100(3), 2010); retrieved 2026-11-20",
        "short": "Ramey (2016), Handbook tax data (Romer and Romer's tax changes)",
        "url": RAMEY_URL.format("Ramey_HOM_tax.zip"),
        "licence": "posted by the author for replication; used with citation",
        "units": "nominal values in billions of dollars at annual rates; tax changes as a share of GDP",
        "vintage": "2026-11-20",
        "sha256": "41cfe9a71f7c8e352227a448c6680d682c59d10b627135b899b5c1da82eb84f9",
        "files": ("ramey_tax.csv",),
    },
    "blanchard_leigh": {
        "title": "Blanchard and Leigh's forecast-error data: IMF spring 2010 forecasts of growth and of the structural "
                 "balance, and growth as reported in fall 2012, for 2009-2011",
        "publisher": "Olivier Blanchard and Daniel Leigh (NBER data appendix to w18779)",
        "citation": "O. Blanchard and D. Leigh, \"Growth Forecast Errors and Fiscal Multipliers\", NBER Working Paper "
                    "18779 (2013) and American Economic Review 103(3): 117-120 (2013), replication files (dta.xlsx), "
                    "retrieved 2026-11-20",
        "short": "Blanchard and Leigh (2013), replication data",
        "url": "https://www.nber.org/data-appendix/w18779/replication%20files.zip",
        "licence": "posted by the authors for replication; used with citation",
        "units": "percent growth of real GDP; percent of potential GDP (structural balance)",
        "vintage": "2026-11-20",
        "sha256": "55d5f985c7b43cffceb3b0c7e51cab75710f979bc421cf564b0e5c1a5e77e7a4",
        "files": ("blanchard_leigh.csv",),
    },
    "rr_hap": {
        "title": "Reinhart and Rogoff's working spreadsheet as processed by Herndon, Ash and Pollin: public debt to GDP "
                 "and real GDP growth, 20 advanced economies, 1946-2009",
        "publisher": "Thomas Herndon, Michael Ash and Robert Pollin (PERI, University of Massachusetts Amherst)",
        "citation": "T. Herndon, M. Ash and R. Pollin, \"Does High Public Debt Consistently Stifle Economic Growth? A "
                    "Critique of Reinhart and Rogoff\", Cambridge Journal of Economics 38(2): 257-279 (2014), "
                    "replication files (RR-keycolumns.xlsx), retrieved 2026-11-20",
        "short": "Herndon, Ash and Pollin (2014), RR key columns",
        "url": "https://peri.umass.edu/images/RR-keycolumns.xlsx",
        "licence": "open source under the BSD 2-clause licence (the authors' replication files)",
        "units": "percent of GDP; percent a year",
        "vintage": "2026-11-20",
        "sha256": "80bdd2503328d6bac29c6b33dc3113e40c0ba319da38907804de275294cf4179",
        "files": ("rr_hap.csv",),
    },
    "jst": {
        "title": "The Jorda-Schularick-Taylor Macrohistory Database, release 6: 18 advanced economies, 1870-2020",
        "publisher": "Oscar Jorda, Moritz Schularick and Alan M. Taylor (macrohistory.net)",
        "citation": "O. Jorda, M. Schularick and A. M. Taylor, \"Macrofinancial History and the New Business Cycle "
                    "Facts\", NBER Macroeconomics Annual 2016, vol. 31 (University of Chicago Press, 2017); "
                    "JSTdatasetR6.xlsx, retrieved 2026-11-20",
        "short": "Jorda, Schularick and Taylor, Macrohistory Database R6",
        "url": "https://www.macrohistory.net/app/download/9834512569/JSTdatasetR6.xlsx",
        "licence": "CC BY-NC-SA 4.0 (the extract here is shared under the same licence; commercial data providers "
                   "may not integrate it)",
        "units": "national currency, percent and indices as in the database's documentation",
        "vintage": "2026-11-20",
        "sha256": "c1bb91fe56ea50d4f27af5c0fc897d481e89ae38ce41eaecab62134c9354981d",
        "files": ("jst.csv",),
    },
    "cepii_gravity": {
        "title": "The CEPII Gravity database, V202211: bilateral trade, GDP, distance, borders, languages and trade "
                 "agreements for every pair of countries, 2019 (an extract)",
        "publisher": "CEPII",
        "citation": "M. Conte, P. Cotterlaz and T. Mayer, \"The CEPII Gravity database\", CEPII Working Paper 2022-05 "
                    "(2022); Gravity_csv_V202211.zip, retrieved 2026-11-20",
        "short": "CEPII Gravity database V202211",
        "url": "https://www.cepii.fr/DATA_DOWNLOAD/gravity/data/Gravity_csv_V202211.zip",
        "licence": "Etalab Open Licence 2.0 (attribution)",
        "units": "trade in thousands of current US dollars (BACI); GDP in thousands of current US dollars; distance in "
                 "kilometres (population-weighted, harmonic)",
        "vintage": "2026-11-20",
        "sha256": "7ffea0510a536587f2f9295bbafef4a312a36b366acc256eb6d9770fe35e44b1",
        "files": ("cepii_gravity_2019.csv",),
    },
    "census_cbsa": {
        "title": "Annual estimates of the resident population for metropolitan and micropolitan statistical areas, "
                 "April 1, 2020 to July 1, 2024 (CBSA-EST2024-ALLDATA)",
        "publisher": "U.S. Census Bureau, Population Estimates Program",
        "citation": "U.S. Census Bureau, Vintage 2024 population estimates, cbsa-est2024-alldata.csv, retrieved "
                    "2026-11-20",
        "short": "Census Bureau, Vintage 2024 CBSA estimates",
        "url": "https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/metro/totals/"
               "cbsa-est2024-alldata.csv",
        "licence": "public domain (U.S. government work)",
        "units": "persons",
        "vintage": "2026-11-20",
        "sha256": "8bb9e59c3193ce1fc4f1bd08308fe435b2840d0a80a521f51db99b4185d28ea0",
        "files": ("cbsa_2020_2024.csv",),
    },
    "urban_share": {
        "title": "Share of the population living in urban areas, 1500-2025, for the world, its regions and 21 "
                 "countries (an extract of the HYDE 3.5 series)",
        "publisher": "PBL Netherlands Environmental Assessment Agency (HYDE 3.5), via Our World in Data",
        "citation": "HYDE (2025), with minor processing by Our World in Data, \"Population share in urban areas\", "
                    "grapher chart urbanization-last-500-years (updated 2026-06-08), retrieved 2026-11-20",
        "short": "HYDE 3.5, via Our World in Data",
        "url": "https://ourworldindata.org/grapher/urbanization-last-500-years.csv?v=1&csvType=full&"
               "useColumnShortNames=true",
        "licence": "CC BY 4.0",
        "units": "percent of the population",
        "vintage": "2026-11-20",
        "sha256": "85f781e9247ecdc6c20b0ba47f3276325075635f02ac9a1e0b6bb3ee3e7ddebe",
        "files": ("urban_share_1500_2025.csv",),
    },
    "njmin": {
        "title": "Card and Krueger's survey of 410 fast-food restaurants in New Jersey and eastern Pennsylvania, "
                 "February-March and November-December 1992 (public.dat)",
        "publisher": "David Card, data posted for Card and Krueger, Myth and Measurement (1995), chapter 2",
        "citation": "D. Card and A. B. Krueger, \"Minimum Wages and Employment: A Case Study of the Fast-Food "
                    "Industry in New Jersey and Pennsylvania\", American Economic Review 84(4): 772-793 (1994); "
                    "njmin.zip from davidcard.berkeley.edu/data_sets, retrieved 2026-11-20",
        "short": "Card and Krueger (1994), public data",
        "url": "https://davidcard.berkeley.edu/data_sets/njmin.zip",
        "licence": "posted by the author for public use; cited as Card and Krueger (1994)",
        "units": "employees (full-time, part-time, managers) per store; starting wage, dollars an hour; prices, "
                 "dollars",
        "vintage": "2026-11-20",
        "sha256": "41a29aec6b489658b20030d044a2b20a5f5a04b871cde41df057afd6013ba587",
        "files": ("njmin_1992.csv",),
    },
    "wooldridge": {
        "title": "Five labour datasets from Wooldridge's Introductory Econometrics, as distributed in the R package "
                 "wooldridge: card (Card's 1995 extract of the National Longitudinal Survey of Young Men, 1976), "
                 "wage1 (the Current Population Survey, 1976), wage2 (the National Longitudinal Survey, 1980), "
                 "wagepan (Vella and Verbeek's panel of 545 young men, 1980-87) and cps78_85 (the Current Population "
                 "Survey, 1978 and 1985)",
        "publisher": "J. M. Wooldridge's textbook data, R package wooldridge (J. Shea), CRAN",
        "citation": "J. M. Wooldridge, Introductory Econometrics: A Modern Approach; D. Card, \"Using Geographic "
                    "Variation in College Proximity to Estimate the Return to Schooling\", in Aspects of Labour "
                    "Market Behaviour (1995); wooldridge 1.4-7 (CRAN), data/card.RData, wage1.RData, wage2.RData, "
                    "wagepan.RData, cps78_85.RData, retrieved 2026-11-20; F. Vella and M. Verbeek, Journal of Applied "
                    "Econometrics 13(2): 163-183 (1998)",
        "short": "Wooldridge's data, via the R package wooldridge",
        "url": "https://cran.r-project.org/src/contrib/wooldridge_1.4-7.tar.gz",
        "licence": "GPL-3 (the package); the data are the cited surveys and studies",
        "units": "hourly wages in dollars (1976 or 1980) and their logs; years of schooling and experience; IQ",
        "vintage": "2026-11-20",
        "sha256": "2f790f58898225e53dd69d690df118d985ce1553dd554cc7a1f634e0f1bba746",
        "files": ("card1995.csv", "wage1_1976.csv", "wage2_1980.csv", "wagepan_1980_87.csv", "cps78_85.csv"),
    },
    "autor_dorn": {
        "title": "Autor and Dorn's replication data for \"The Growth of Low-Skill Service Jobs and the Polarization of "
                 "the US Labor Market\": employment shares and wage changes by percentile of the 1980 occupational "
                 "wage distribution, 1980-2005, the routine share by percentile, and employment shares and wages of "
                 "330 occupations (occ1990dd), 1950-2005",
        "publisher": "David Dorn's data page (ddorn.net/data.htm), file archive for Autor and Dorn (2013)",
        "citation": "D. Autor and D. Dorn, American Economic Review 103(5): 1553-1597 (2013); "
                    "Autor-Dorn-LowSkillServices-FileArchive.zip, dta/emp-bypctile-1980-2005-rewt-0-czall.dta, "
                    "dwg-byperc-1980-2005-czall.dta, RTI-bypctile-1980.dta, occ1990dd_data2012.dta and "
                    "occ-means-by-decade-1980-2005-czall.dta, retrieved 2026-11-20",
        "short": "Autor and Dorn (2013), replication data",
        "url": "https://www.ddorn.net/data/Autor-Dorn-LowSkillServices-FileArchive.zip",
        "licence": "posted by the authors for research use with citation of Autor and Dorn (2013)",
        "units": "employment shares (percent of employment in each 1980 percentile, or share of all employment); "
                 "changes in mean log hourly wages; routine task intensity",
        "vintage": "2026-11-20",
        "sha256": "a4c9b8200a39d357c1141cfe3cb8b54b7ed586dcf9768e3b1c6689d79c45be0b",
        "files": ("polarization_1980_2005.csv", "occ1990dd_1950_2005.csv"),
    },
    "resume": {
        "title": "Bertrand and Mullainathan's correspondence experiment: 4,870 fictitious resumes sent to help-wanted "
                 "advertisements in Boston and Chicago, 2001-02, as distributed in the R package openintro",
        "publisher": "R package openintro (D. Diez, M. Cetinkaya-Rundel, C. Barr, OpenIntro), CRAN",
        "citation": "M. Bertrand and S. Mullainathan, \"Are Emily and Greg More Employable Than Lakisha and Jamal?\", "
                    "American Economic Review 94(4): 991-1013 (2004); openintro 2.5.1 (CRAN), data/resume.rda, "
                    "retrieved 2026-11-20",
        "short": "Bertrand and Mullainathan (2004), via openintro",
        "url": "https://cran.r-project.org/src/contrib/openintro_2.5.1.tar.gz",
        "licence": "GPL-3 (the package); the data are the cited experiment's",
        "units": "one row per resume: the advertisement, the city, the job, the name and the race and sex it signals, "
                 "the resume's contents, and whether the employer called back",
        "vintage": "2026-11-20",
        "sha256": "b1c53f2e1eef9bf20cf38bbd09b604933a4ed8d6776b91ff9978f55237ee76a8",
        "files": ("resume_2001.csv",),
    },
    "trefler_hov": {
        "title": "Trefler's data for \"The Case of the Missing Trade and Other Mysteries\": the factor content of trade, "
                 "endowments and GDP for 33 countries and 9 factors, 1983",
        "publisher": "Daniel Trefler (NBER)",
        "citation": "D. Trefler, \"The Case of the Missing Trade and Other Mysteries\", American Economic Review 85(5): "
                    "1029-1046 (1995); data file hov_pub.dat (15 November 1994), retrieved 2026-11-20",
        "short": "Trefler (1995), replication data",
        "url": "https://www.nber.org/ftp/trefler/HOV/hov_pub.dat",
        "licence": "no licence stated; the author's replication data, posted for public use and redistributed here as "
                   "a cited extract",
        "units": "factor content of trade and endowments in the factor's units (capital in 1983 dollars, labour in "
                 "workers, land in hectares); GDP and the trade balance in dollars; GDP per head (PWT)",
        "vintage": "2026-11-20",
        "sha256": "b3272c32ecec5642cf18082eeaba976f5b64342ac210288e393ea51c19e4ca33",
        "files": ("trefler_hov.csv",),
    },
    "bigmac": {
        "title": "The Economist's Big Mac index: local prices, exchange rates, dollar prices, raw and GDP-adjusted "
                 "valuations, 2000-2026",
        "publisher": "The Economist",
        "citation": "The Economist, big-mac-data (GitHub: TheEconomist/big-mac-data), "
                    "output-data/big-mac-full-index.csv, retrieved 2026-11-20",
        "short": "The Economist, Big Mac index",
        "url": "https://raw.githubusercontent.com/TheEconomist/big-mac-data/master/output-data/big-mac-full-index.csv",
        "licence": "CC BY 4.0 (the data generated by The Economist)",
        "units": "local currency; currency units per dollar; dollars; fractions over- or undervalued",
        "vintage": "2026-11-20",
        "sha256": "faf0bc0dd4e01b15d6c647c6229dbba0d992f073dc7bbbe9bd37a89d3cf85789",
        "files": ("bigmac.csv",),
    },
    "wdi_ca": {
        "title": "World Development Indicators: current account balance, percent of GDP (BN.CAB.XOKA.GD.ZS), "
                 "selected economies, 1980-2025",
        "publisher": "World Bank",
        "citation": "World Bank, World Development Indicators, BN.CAB.XOKA.GD.ZS, retrieved 2026-11-20",
        "short": "World Bank, WDI, current account",
        "url": "https://api.worldbank.org/v2/country/{}/indicator/BN.CAB.XOKA.GD.ZS?format=json&per_page=2000"
               "&date=1980:2025",
        "licence": "CC BY 4.0",
        "units": "percent of GDP",
        "vintage": "2026-11-20",
        "files": ("wdi_ca.csv",),
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
        "files": ("rtdsm_2006_2010.csv", "rtdsm_first_latest.csv", "rtdsm_q1_vintages.csv"),
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
def rtdsm_q1() -> dict:
    """Real GDP as each first-quarter vintage from 1966Q1 reported it: ``{"quarters": ["1947:Q1", ...], "vintages":
    ["1966Q1", ...], "level": {vintage: [...]}}`` (NaN where a vintage had no figure; each vintage in its own base
    year's dollars)."""
    rows = _read(HERE / "rtdsm_q1_vintages.csv")
    vintages = [c for c in rows[0] if c != "quarter"]
    return {"quarters": [r["quarter"] for r in rows], "vintages": vintages,
            "level": {v: [_num(r[v]) for r in rows] for v in vintages}}


@functools.lru_cache(maxsize=None)
def greenbook() -> dict:
    """The Fed staff's projections of GDP-price inflation, one row per Greenbook (Tealbook), 1967-2020: ``{"gb":
    [{"date": "1967-03-29", "quarter": "1967Q1", "b1": ..., "f": [F0, ..., F4]}]}`` (annualized quarter-on-quarter
    percent; ``b1`` the staff's estimate for the quarter before, ``F0`` the current quarter), and the Survey of
    Professional Forecasters' medians for the same index, ``{"spf": [{"quarter": "1968Q4", "f": [F0, ..., F4]}]}``
    (DPGDP2-6)."""
    gb = [{"date": r["date"], "quarter": r["quarter"], "b1": _num(r["b1"]),
           "f": [_num(r[f"f{k}"]) for k in range(5)]} for r in _read(HERE / "greenbook_pgdp.csv")]
    spf_ = [{"quarter": r["quarter"], "f": [_num(r[f"f{k}"]) for k in range(5)]}
            for r in _read(HERE / "spf_pgdp_growth.csv")]
    return {"gb": gb, "spf": spf_}


@functools.lru_cache(maxsize=None)
def hlw() -> dict:
    """Holston, Laubach and Williams's one-sided estimates, quarterly from 1961Q1: ``{"date": [...], "g_us",
    "z_us", "rstar_us", "rstar_ca", "rstar_ea": [...]}`` (NaN where there is no estimate; the euro area from
    1972)."""
    rows = _read(HERE / "hlw_rstar.csv")
    return {k: [r[k] if k == "date" else _num(r[k]) for r in rows]
            for k in ("date", "g_us", "z_us", "rstar_us", "rstar_ca", "rstar_ea")}


def _cols(name: str) -> dict:
    rows = _read(HERE / name)
    return {k: [_num(r[k]) if k not in ("country", "wdicode") else r[k] for r in rows] for k in rows[0]}


@functools.lru_cache(maxsize=None)
def ramey_zubairy() -> dict:
    """Ramey and Zubairy's quarterly US data, 1889Q1-2015Q4: ``{"quarter": [1889.0, 1889.25, ...], "ngov", "ngdp",
    "pgdp", "pop", "unemp", "news", "rgdp", "rgdp_pott6", "rgdp_potcbo", "tbill", "zlb_dummy",
    "nfedcurrreceipts_nipa", "pubfeddebt_treas": [...]}`` (NaN where missing)."""
    return _cols("ramey_zubairy.csv")


@functools.lru_cache(maxsize=None)
def ramey_tax() -> dict:
    """Ramey's Handbook tax data, 1945Q1-2015Q4: ``{"quarter", "ngdp", "rgdp", "pgdp", "pop", "ngov",
    "ntaxrev", "nfedtaxrev", "exog_rr", "endog_rr": [...]}``; ``exog_rr`` and ``endog_rr`` are Romer and Romer's
    exogenous and endogenous tax changes as ratios to GDP."""
    return _cols("ramey_tax.csv")


@functools.lru_cache(maxsize=None)
def blanchard_leigh() -> dict:
    """Blanchard and Leigh's data for 2009-2011: ``{"country", "wdicode", "year", "eu", "growth_fall2012",
    "growth_spring2010", "sb_spring2010": [...]}``: real GDP growth as reported in the IMF's fall 2012 WEO and as
    forecast in spring 2010, and the structural balance (percent of potential GDP) as forecast in spring 2010."""
    return _cols("blanchard_leigh.csv")


JST_COLS = ("year", "country", "iso", "pop", "rgdpmad", "rgdpbarro", "gdp", "iy", "cpi", "ca", "money", "stir",
            "ltrate", "hpnom", "unemp", "debtgdp", "xrusd", "tloans", "tmort", "thh", "tbus", "lev", "ltd", "noncore",
            "crisisJST", "eq_tr", "housing_tr", "bond_tr", "bill_rate", "imports", "exports")


@functools.lru_cache(maxsize=None)
def jst() -> dict:
    """The Jorda-Schularick-Taylor Macrohistory Database (release 6), 18 countries, 1870-2020, one row per country
    and year: ``{"year", "country", "iso", "pop", "rgdpmad" (real GDP per head, 1990 dollars), "rgdpbarro" (real GDP
    per head, index 2005 = 100), "gdp" (nominal GDP), "iy", "cpi", "ca", "money", "stir", "ltrate", "hpnom" (nominal
    house prices), "unemp", "debtgdp" (public debt), "xrusd", "tloans", "tmort", "thh", "tbus" (bank loans: total,
    mortgages, households, business; nominal), "lev", "ltd", "noncore", "crisisJST" (1 in the first year of a
    systemic financial crisis), "eq_tr", "housing_tr", "bond_tr", "bill_rate", "imports", "exports" (nominal, national currency): [...]}``
    (NaN where missing)."""
    rows = _read(HERE / "jst.csv")
    return {k: [r[k] if k in ("country", "iso") else _num(r[k]) for r in rows] for k in JST_COLS}


BIGMAC_COLS = ("date", "iso_a3", "currency_code", "name", "local_price", "dollar_ex", "dollar_price", "USD_raw",
               "GDP_bigmac", "USD_adjusted")
WDI_CA = ("USA", "CHN", "DEU", "JPN", "GBR", "SAU", "KOR", "THA")


@functools.lru_cache(maxsize=None)
def bigmac() -> dict:
    """The Economist's Big Mac index, one row per country and date: ``{"date", "iso_a3", "currency_code", "name",
    "local_price", "dollar_ex", "dollar_price", "USD_raw" (over- or undervaluation against the dollar), "GDP_bigmac"
    (GDP per head, where the adjusted index uses it), "USD_adjusted": [...]}`` (NaN where missing)."""
    rows = _read(HERE / "bigmac.csv")
    txt = ("date", "iso_a3", "currency_code", "name")
    return {k: [r[k] if k in txt else _num(r[k]) for r in rows] for k in BIGMAC_COLS}


@functools.lru_cache(maxsize=None)
def wdi_ca() -> dict:
    """Current account balances as a percent of GDP, 1980-2025, for the United States, China, Germany, Japan, the
    United Kingdom, Saudi Arabia, Korea and Thailand: ``{iso3: {"year": [...], "value": [...]}}``."""
    out: dict = {}
    for r in _read(HERE / "wdi_ca.csv"):
        d = out.setdefault(r["code"], {"year": [], "value": []})
        d["year"].append(int(r["year"]))
        d["value"].append(_num(r["value"]))
    return out


GRAVITY_COLS = ("iso3_o", "iso3_d", "distw_harmonic", "contig", "comlang_off", "col_dep_ever", "gdp_o", "gdp_d",
                "fta_wto", "eu_o", "eu_d", "tradeflow_baci", "manuf_tradeflow_baci")


@functools.lru_cache(maxsize=None)
def gravity() -> dict:
    """CEPII's Gravity database, 2019, one row per ordered pair of existing countries with BACI trade recorded:
    ``{"iso3_o", "iso3_d", "distw_harmonic" (km), "contig", "comlang_off", "col_dep_ever", "gdp_o", "gdp_d" (thousands
    of dollars), "fta_wto", "eu_o", "eu_d", "tradeflow_baci", "manuf_tradeflow_baci" (thousands of dollars): [...]}``
    (NaN where missing)."""
    rows = _read(HERE / "cepii_gravity_2019.csv")
    return {k: [r[k] if k in ("iso3_o", "iso3_d") else _num(r[k]) for r in rows] for k in GRAVITY_COLS}


NJMIN_COLS = ("sheet", "chain", "co_owned", "state", "empft", "emppt", "nmgrs", "wage_st", "hrsopen", "pentree",
              "status2", "empft2", "emppt2", "nmgrs2", "wage_st2", "hrsopen2", "pentree2")
WOOLDRIDGE_COLS = {
    "card": ("lwage", "wage", "educ", "exper", "expersq", "black", "smsa", "south", "smsa66", "nearc2", "nearc4",
             "reg661", "reg662", "reg663", "reg664", "reg665", "reg666", "reg667", "reg668", "reg669", "IQ", "KWW",
             "fatheduc", "motheduc", "age"),
    "wage1": ("wage", "lwage", "educ", "exper", "tenure", "female", "nonwhite", "married"),
    "wage2": ("wage", "lwage", "educ", "exper", "tenure", "IQ", "KWW", "meduc", "feduc", "black", "urban", "south",
              "married"),
    "wagepan": ("nr", "year", "lwage", "union", "educ", "exper", "expersq", "married", "black", "hisp", "hours",
                "manuf", "south"),
    "cps78_85": ("year", "lwage", "educ", "exper", "expersq", "female", "union", "nonwhite", "married", "south"),
}
WOOLDRIDGE_FILES = {"card": "card1995.csv", "wage1": "wage1_1976.csv", "wage2": "wage2_1980.csv",
                    "wagepan": "wagepan_1980_87.csv", "cps78_85": "cps78_85.csv"}
RESUME_COLS = ("job_ad_id", "job_city", "job_type", "job_industry", "received_callback", "firstname", "race", "gender",
               "years_college", "college_degree", "honors", "years_experience", "computer_skills", "special_skills",
               "volunteer", "military", "employment_holes", "has_email_address", "resume_quality")
RESUME_TEXT = ("job_city", "job_type", "job_industry", "firstname", "race", "gender", "resume_quality")
# Dorn's occupation groups (subfile_occ1990dd_occgroups.do): occ1990dd code ranges
OCC_GROUPS = {
    "managers": ((3, 22),), "management-related": ((23, 37),), "professionals": ((43, 200),),
    "technicians": ((203, 235),), "financial sales": ((243, 258),), "retail sales": ((274, 283),),
    "clerical and administrative": ((303, 389),), "police and fire": ((417, 423),),
    "cleaning and housekeeping": ((405, 408),), "food preparation and service": ((433, 444),),
    "health service aides": ((445, 447),), "building and grounds": ((448, 455),),
    "guards": ((415, 415), (425, 427)), "personal appearance": ((457, 458),), "recreation and hospitality": ((459, 467),), "child care": ((468, 468),), "other personal care": ((469, 472),),
    "farmers and farm managers": ((473, 475),), "other agricultural": ((479, 498),),
    "mechanics and repairers": ((503, 549),), "construction trades": ((558, 599),), "extraction": ((614, 617),),
    "precision production": ((628, 699),), "machine operators and assemblers": ((703, 799),),
    "transport and material moving": ((803, 889),),
}


@functools.lru_cache(maxsize=None)
def njmin() -> dict:
    """Card and Krueger's 410 restaurants, one row each: ``{column: [...]}`` for :data:`NJMIN_COLS` (NaN where
    missing; ``state`` 1 for New Jersey; ``status2`` 3 for closed for good)."""
    rows = _read(HERE / "njmin_1992.csv")
    return {k: [_num(r[k]) for r in rows] for k in NJMIN_COLS}


@functools.lru_cache(maxsize=None)
def wooldridge(name: str) -> dict:
    """One of Wooldridge's labour datasets (``card``, ``wage1`` or ``wage2``): ``{column: [...]}`` (NaN where
    missing)."""
    rows = _read(HERE / WOOLDRIDGE_FILES[name])
    return {k: [_num(r[k]) for r in rows] for k in WOOLDRIDGE_COLS[name]}


@functools.lru_cache(maxsize=None)
def autor_dorn(table: str = "pctile") -> dict:
    """Autor and Dorn's data.  ``pctile``: one row per percentile of the 1980 occupational wage distribution (1-100):
    the percent of employment in it in 1980, 1990, 2000 and 2005 (100 percentiles of 1% each in 1980), the change in
    mean log hourly wages over each period, and the 1980 share of its employment in routine-intensive occupations.
    ``occ``: one row per occ1990dd occupation: percent of all employment, 1950-2005 (NaN where not coded), mean log
    hourly wages in 1980 and 2005, and the 1980 routine task intensity."""
    f = {"pctile": "polarization_1980_2005.csv", "occ": "occ1990dd_1950_2005.csv"}[table]
    rows = _read(HERE / f)
    return {k: [_num(r[k]) for r in rows] for k in rows[0]}


def occ_group(code: int) -> str:
    """Dorn's occupation group of an occ1990dd code (``OCC_GROUPS``), or '' if none."""
    for name, ranges in OCC_GROUPS.items():
        if any(a <= code <= b for a, b in ranges):
            return name
    return ""


@functools.lru_cache(maxsize=None)
def resume() -> dict:
    """Bertrand and Mullainathan's 4,870 resumes: ``{column: [...]}`` for :data:`RESUME_COLS` (text columns as
    strings; ``race`` is 'white' or 'black', ``gender`` 'f' or 'm', ``received_callback`` 0 or 1)."""
    rows = _read(HERE / "resume_2001.csv")
    return {k: ([r[k] for r in rows] if k in RESUME_TEXT else [_num(r[k]) for r in rows]) for k in RESUME_COLS}


@functools.lru_cache(maxsize=None)
def cbsa(kind: str = "Metropolitan Statistical Area") -> dict:
    """The Census Bureau's Vintage 2024 population estimates, one row per core-based statistical area of the given
    kind ("Metropolitan Statistical Area" or "Micropolitan Statistical Area"): ``{"cbsa", "name", "pop2020" (the
    estimates base, April 2020), "pop2024" (July 2024): [...]}``."""
    rows = [r for r in _read(HERE / "cbsa_2020_2024.csv") if r["lsad"] == kind]
    return {"cbsa": [r["cbsa"] for r in rows], "name": [r["name"] for r in rows],
            "pop2020": [int(r["pop2020"]) for r in rows], "pop2024": [int(r["pop2024"]) for r in rows]}


@functools.lru_cache(maxsize=None)
def urban_share(entity: str) -> dict:
    """The share of an entity's population living in urban areas (HYDE 3.5, via Our World in Data), percent:
    ``{"year": [...], "value": [...]}`` from 1500 (centuries, then decades, then years)."""
    rows = [r for r in _read(HERE / "urban_share_1500_2025.csv") if r["entity"] == entity]
    if not rows:
        raise KeyError(entity)
    return {"year": [int(r["year"]) for r in rows], "value": [float(r["share"]) for r in rows]}


@functools.lru_cache(maxsize=None)
def trefler() -> dict:
    """Trefler's (1995) data: one row per country and factor, 33 countries and 9 factors in 1983: ``{"country",
    "factor", "at" (the factor content of net exports, A T), "v" (the endowment), "y" (GDP), "b" (the trade balance),
    "ypc" (GDP per head), "pop": [...]}``."""
    rows = _read(HERE / "trefler_hov.csv")
    return {k: [r[k] if k in ("country", "factor") else _num(r[k]) for r in rows]
            for k in ("country", "factor", "at", "v", "y", "b", "ypc", "pop")}


@functools.lru_cache(maxsize=None)
def rr_hap() -> dict:
    """Reinhart and Rogoff's data as processed by Herndon, Ash and Pollin, 1946-2009: ``{"country", "year",
    "debtgdp", "growth": [...]}`` (public debt, percent of GDP; real GDP growth, percent)."""
    return _cols("rr_hap.csv")


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
    # every first-quarter vintage, 1966Q1 to the latest: real GDP for every quarter it reported (Part 31's real-time
    # output gaps)
    keep_q1 = [i for i, v in enumerate(vint) if v.endswith("Q1") and v >= "1966Q1"]
    with open(HERE / "rtdsm_q1_vintages.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["quarter", *[vint[i] for i in keep_q1]])
        for q in quarters:
            w.writerow([q, *[_fmt(data[q][i]) if data[q][i] == data[q][i] else "" for i in keep_q1]])
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


def refresh_greenbook() -> None:
    import openpyxl  # noqa: PLC0415
    from openpyxl.reader import excel  # noqa: PLC0415

    d = DATASETS["greenbook"]
    raw = RAW / "GBweb_Row_Format.xlsx"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"greenbook: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    excel.ExcelReader.read_properties = lambda self: None
    rows = list(openpyxl.load_workbook(raw, read_only=True, data_only=True)["gPGDP"].iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    num = lambda x: x if isinstance(x, (int, float)) else None  # noqa: E731
    with open(HERE / "greenbook_pgdp.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "quarter", "b1", *[f"f{k}" for k in range(5)]])
        for r in rows[1:]:
            if not isinstance(r[0], (int, float)):
                continue
            rec = dict(zip(head, r))
            gd = str(int(rec["GBdate"]))
            y, q = str(r[0]).split(".")
            vals = [num(rec["gPGDPB1"]), *[num(rec[f"gPGDPF{k}"]) for k in range(5)]]
            w.writerow([f"{gd[:4]}-{gd[4:6]}-{gd[6:]}", f"{y}Q{q}", *[_fmt(v) if v is not None else "" for v in vals]])
    raw2 = RAW / "spf_median_pgdp_growth.xlsx"
    _download(SPF_URL.format("median_pgdp_growth"), raw2)
    ws = openpyxl.load_workbook(raw2, read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    head = [str(h).lower() for h in rows[0]]
    with open(HERE / "spf_pgdp_growth.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["quarter", *[f"f{k}" for k in range(5)]])
        for r in rows[1:]:
            if not isinstance(r[0], (int, float)):
                continue
            rec = dict(zip(head, r))
            vals = [num(rec.get(f"dpgdp{k}")) for k in range(2, 7)]
            w.writerow([f"{int(r[0])}Q{int(r[1])}", *[_fmt(v) if v is not None else "" for v in vals]])


def refresh_hlw() -> None:
    import openpyxl  # noqa: PLC0415
    from openpyxl.reader import excel  # noqa: PLC0415

    d = DATASETS["hlw"]
    raw = RAW / "Holston_Laubach_Williams_current_estimates.xlsx"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"hlw: the download differs from the recorded vintage ({sha[:12]} vs {d['sha256'][:12]})")
    excel.ExcelReader.read_properties = lambda self: None
    rows = list(openpyxl.load_workbook(raw, read_only=True, data_only=True)["HLW Estimates"].iter_rows(
        values_only=True))
    num = lambda x: _fmt(x) if isinstance(x, (int, float)) else ""  # noqa: E731
    with open(HERE / "hlw_rstar.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "g_us", "z_us", "rstar_us", "rstar_ca", "rstar_ea"])
        for r in rows:
            if hasattr(r[0], "year"):
                w.writerow([r[0].strftime("%Y-%m-%d"), num(r[2]), num(r[6]), num(r[10]), num(r[11]), num(r[12])])


def _zip_member(raw: Path, suffix: str) -> bytes:
    import zipfile  # noqa: PLC0415

    with zipfile.ZipFile(raw) as z:
        name = [n for n in z.namelist() if n.endswith(suffix)][0]
        return z.read(name)


def refresh_ramey_zubairy() -> None:
    raw = RAW / "Ramey_Zubairy_replication_codes.zip"
    print("ramey_zubairy:", _download(DATASETS["ramey_zubairy"]["url"], raw)[:12])
    text = _zip_member(raw, "rzdatnew.csv").decode("utf-8", "replace").splitlines()
    rows = list(csv.DictReader(text))
    keep = ("quarter", "ngov", "ngdp", "pgdp", "pop", "unemp", "news", "rgdp", "rgdp_pott6", "rgdp_potcbo", "tbill",
            "zlb_dummy", "nfedcurrreceipts_nipa", "pubfeddebt_treas")
    with open(HERE / "ramey_zubairy.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(keep)
        for r in rows:
            w.writerow([r.get(k, "").strip() for k in keep])


def refresh_ramey_tax() -> None:
    import io  # noqa: PLC0415

    import openpyxl  # noqa: PLC0415

    raw = RAW / "Ramey_HOM_tax.zip"
    print("ramey_tax:", _download(DATASETS["ramey_tax"]["url"], raw)[:12])
    wb = openpyxl.load_workbook(io.BytesIO(_zip_member(raw, "homtaxdat.xlsx")), read_only=True, data_only=True)
    rows = list(wb["homtaxdat"].iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    keep = {"quarter": "quarter", "ngdp": "ngdp", "rgdp": "rgdp", "pgdp": "pgdp", "pop": "pop", "ngov": "ngov",
            "ntaxrev": "ntaxrev", "nfedtaxrev": "nfedtaxrev", "EXOGENRRATIO": "exog_rr", "ENDOGNRRATIO": "endog_rr"}
    with open(HERE / "ramey_tax.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(list(keep.values()))
        for r in rows[1:]:
            rec = dict(zip(head, r))
            w.writerow([_fmt(rec[k]) if isinstance(rec.get(k), (int, float)) else "" for k in keep])


def refresh_blanchard_leigh() -> None:
    import io  # noqa: PLC0415

    import openpyxl  # noqa: PLC0415

    raw = RAW / "blanchard_leigh_replication.zip"
    print("blanchard_leigh:", _download(DATASETS["blanchard_leigh"]["url"], raw)[:12])
    wb = openpyxl.load_workbook(io.BytesIO(_zip_member(raw, "dta.xlsx")), read_only=True, data_only=True)
    rows = list(wb.worksheets[0].iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    cols = {"country": "country", "wdicode": "wdicode", "year": "year", "eu": "eu",
            "ngdp_rpch2012fall": "growth_fall2012", "ngdp_rpch2010spring": "growth_spring2010",
            "ggsb_gdp2010spring": "sb_spring2010"}
    with open(HERE / "blanchard_leigh.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(list(cols.values()))
        for r in rows[1:]:
            rec = dict(zip(head, r))
            if rec.get("year") not in (2009, 2010, 2011):
                continue
            w.writerow([rec[k] if k in ("country", "wdicode") else
                        (_fmt(rec[k]) if isinstance(rec.get(k), (int, float)) else "") for k in cols])


def refresh_rr_hap() -> None:
    import openpyxl  # noqa: PLC0415

    raw = RAW / "RR-keycolumns.xlsx"
    print("rr_hap:", _download(DATASETS["rr_hap"]["url"], raw)[:12])
    rows = list(openpyxl.load_workbook(raw, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    with open(HERE / "rr_hap.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["country", "year", "debtgdp", "growth"])
        for r in rows[1:]:
            rec = dict(zip(head, r))
            num = lambda x: _fmt(float(x)) if x not in (None, "", "NA") else ""  # noqa: E731
            w.writerow([rec["Country"], int(float(rec["Year"])), num(rec["debtgdp"]), num(rec["dRGDP"])])


def refresh_bigmac() -> None:
    raw = RAW / "big-mac-full-index.csv"
    sha = _download(DATASETS["bigmac"]["url"], raw)
    if sha != DATASETS["bigmac"]["sha256"]:
        print(f"bigmac: the download differs from the recorded vintage ({sha[:12]})")
    with open(raw, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(HERE / "bigmac.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(BIGMAC_COLS)
        for r in rows:
            w.writerow([r.get(k, "") for k in BIGMAC_COLS])


def refresh_wdi_ca() -> None:
    import json  # noqa: PLC0415

    raw = RAW / "wdi_ca.json"
    _download(DATASETS["wdi_ca"]["url"].format(";".join(WDI_CA)), raw)
    recs = json.loads(raw.read_text())[1]
    with open(HERE / "wdi_ca.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["code", "year", "value"])
        for r in sorted(recs, key=lambda r: (r["countryiso3code"], int(r["date"]))):
            if r["countryiso3code"] in WDI_CA:
                w.writerow([r["countryiso3code"], int(r["date"]), "" if r["value"] is None else _fmt(r["value"])])


def refresh_cepii_gravity() -> None:
    import io  # noqa: PLC0415
    import zipfile  # noqa: PLC0415

    raw = RAW / "Gravity_csv_V202211.zip"
    sha = _download(DATASETS["cepii_gravity"]["url"], raw)
    if sha != DATASETS["cepii_gravity"]["sha256"]:
        print(f"cepii_gravity: the download differs from the recorded vintage ({sha[:12]})")
    with zipfile.ZipFile(raw) as z, z.open("Gravity_V202211.csv") as f, \
            open(HERE / "cepii_gravity_2019.csv", "w", newline="", encoding="utf-8") as g:
        r = csv.DictReader(io.TextIOWrapper(f, encoding="utf-8"))
        w = csv.writer(g)
        w.writerow(GRAVITY_COLS)
        for rec in r:
            if rec["year"] != "2019" or rec["country_exists_o"] != "1" or rec["country_exists_d"] != "1":
                continue
            if rec["iso3_o"] == rec["iso3_d"] or not rec["tradeflow_baci"]:
                continue
            w.writerow([rec[k] for k in GRAVITY_COLS])


def refresh_njmin() -> None:
    import zipfile  # noqa: PLC0415

    d = DATASETS["njmin"]
    raw = RAW / "njmin.zip"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"njmin: the download differs from the recorded vintage ({sha[:12]})")
    names = ("SHEET CHAIN CO_OWNED STATE SOUTHJ CENTRALJ NORTHJ PA1 PA2 SHORE NCALLS EMPFT EMPPT NMGRS WAGE_ST "
             "INCTIME FIRSTINC BONUS PCTAFF MEALS OPEN HRSOPEN PSODA PFRY PENTREE NREGS NREGS11 TYPE2 STATUS2 DATE2 "
             "NCALLS2 EMPFT2 EMPPT2 NMGRS2 WAGE_ST2 INCTIME2 FIRSTIN2 SPECIAL2 MEALS2 OPEN2R HRSOPEN2 PSODA2 PFRY2 "
             "PENTREE2 NREGS2 NREGS112").lower().split()
    with zipfile.ZipFile(raw) as z:
        lines = [ln.split() for ln in z.read("public.dat").decode("latin-1").splitlines() if ln.strip()]
    with open(HERE / "njmin_1992.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(NJMIN_COLS)
        for ln in lines:
            rec = dict(zip(names, ln))
            w.writerow(["" if rec[k] == "." else _fmt(float(rec[k])) for k in NJMIN_COLS])


def refresh_wooldridge() -> None:
    import tarfile  # noqa: PLC0415

    from explainer.psychology import rdata  # noqa: PLC0415

    d = DATASETS["wooldridge"]
    raw = RAW / "wooldridge_1.4-7.tar.gz"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"wooldridge: the download differs from the recorded vintage ({sha[:12]})")
    with tarfile.open(raw, "r:gz") as tf:
        for name, cols in WOOLDRIDGE_COLS.items():
            blob = tf.extractfile(f"wooldridge/data/{name}.RData").read()
            tmp = RAW / f"wooldridge_{name}.RData"
            tmp.write_bytes(blob)
            obj = rdata.load(tmp)[0][1]
            names = obj["attrs"]["names"]["value"]
            data = {n: c["value"] for n, c in zip(names, obj["value"])}
            n = len(data[cols[0]])
            with open(HERE / WOOLDRIDGE_FILES[name], "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(cols)
                for i in range(n):
                    row = []
                    for c in cols:
                        v = data[c][i]
                        row.append("" if v is None or (isinstance(v, float) and v != v) else _fmt(float(v)))
                    w.writerow(row)


def refresh_autor_dorn() -> None:
    import zipfile  # noqa: PLC0415

    from explainer.economics.data.stata import read_dta  # noqa: PLC0415

    d = DATASETS["autor_dorn"]
    raw = RAW / "Autor-Dorn-LowSkillServices-FileArchive.zip"
    # the site may answer automated requests with a browser check; a copy downloaded by hand (with its recorded
    # SHA-256) in .cache/economics/raw is used as is
    if raw.exists() and hashlib.sha256(raw.read_bytes()).hexdigest() == d["sha256"]:
        sha = d["sha256"]
    else:
        sha = _download(d["url"], raw)
    if not zipfile.is_zipfile(raw):
        raise RuntimeError("autor_dorn: the download is not the archive (download it by hand from the data page)")
    if sha != d["sha256"]:
        print(f"autor_dorn: the download differs from the recorded vintage ({sha[:12]})")
    pre = "Autor-Dorn-LowSkillServices-FileArchive.zip Folder/dta/"
    tables = {}
    with zipfile.ZipFile(raw) as z:
        for name in ("emp-bypctile-1980-2005-rewt-0-czall", "dwg-byperc-1980-2005-czall", "RTI-bypctile-1980",
                     "occ1990dd_data2012", "occ-means-by-decade-1980-2005-czall"):
            tmp = RAW / f"{name}.dta"
            tmp.write_bytes(z.read(pre + name + ".dta"))
            tables[name] = read_dta(tmp)[0]
    emp = tables["emp-bypctile-1980-2005-rewt-0-czall"]
    share = {(int(y), int(p)): v for y, p, v in zip(emp["year"], emp["perc"], emp["empshare"])}
    wg, rti = tables["dwg-byperc-1980-2005-czall"], tables["RTI-bypctile-1980"]
    wk = {int(p): k for k, p in enumerate(wg["pctile"])}
    rk = {int(p): k for k, p in enumerate(rti["pctile"])}
    with open(HERE / "polarization_1980_2005.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pctile", "emp1980", "emp1990", "emp2000", "emp2005", "dwage8090", "dwage9000", "dwage0005",
                    "dwage8005", "routine_share1980"])
        for p in range(1, 101):
            w.writerow([p, *(_fmt(share[(y, p)]) for y in (1980, 1990, 2000, 2005)),
                        *(_fmt(wg[c][wk[p]]) for c in ("czall_dpercwg8090", "czall_dpercwg9000", "czall_dpercwg0005",
                                                        "czall_dpercwg8005")),
                        _fmt(rti["perc_R33a"][rk[p]])])
    occ, means = tables["occ1990dd_data2012"], tables["occ-means-by-decade-1980-2005-czall"]
    rti_occ = {int(o): r for o, r, y in zip(means["occ1990dd"], means["RTI_3a"], means["year"]) if int(y) == 1980}
    cols = ["sh_empl1950", "sh_empl1970", "sh_empl1980", "sh_empl1990", "sh_empl2000", "sh_empl2005",
            "avg_hrwage1980", "avg_hrwage2005"]
    with open(HERE / "occ1990dd_1950_2005.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["occ1990dd", *cols, "rti1980"])
        for k, o in enumerate(occ["occ1990dd"]):
            vals = [occ[c][k] for c in cols]
            r = rti_occ.get(int(o), float("nan"))
            # shares are written in percent, so that four decimals keep small occupations' shares precise
            vals = [v * 100 if c.startswith("sh_") else v for c, v in zip(cols, vals)]
            w.writerow([int(o), *("" if v != v else _fmt(float(v)) for v in vals), "" if r != r else _fmt(float(r))])


def refresh_resume() -> None:
    import tarfile  # noqa: PLC0415

    from explainer.psychology import rdata  # noqa: PLC0415

    d = DATASETS["resume"]
    raw = RAW / "openintro_2.5.1.tar.gz"
    if raw.exists() and hashlib.sha256(raw.read_bytes()).hexdigest() == d["sha256"]:
        sha = d["sha256"]
    else:
        sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"resume: the download differs from the recorded vintage ({sha[:12]})")
    with tarfile.open(raw, "r:gz") as tf:
        tmp = RAW / "openintro_resume.rda"
        tmp.write_bytes(tf.extractfile("openintro/data/resume.rda").read())
    obj = rdata.load(tmp)[0][1]
    names = obj["attrs"]["names"]["value"]
    data = {n: c["value"] for n, c in zip(names, obj["value"])}
    with open(HERE / "resume_2001.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(RESUME_COLS)
        for i in range(len(data["job_ad_id"])):
            row = []
            for c in RESUME_COLS:
                v = data[c][i]
                if c in RESUME_TEXT:
                    row.append("" if v is None else str(v))
                else:
                    row.append("" if v is None or (isinstance(v, float) and v != v) else _fmt(float(v)))
            w.writerow(row)

def refresh_census_cbsa() -> None:
    d = DATASETS["census_cbsa"]
    raw = RAW / "cbsa-est2024-alldata.csv"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"census_cbsa: the download differs from the recorded vintage ({sha[:12]})")
    with open(raw, newline="", encoding="latin-1") as f:
        rows = list(csv.DictReader(f))
    with open(HERE / "cbsa_2020_2024.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cbsa", "name", "lsad", "pop2020", "pop2024"])
        for r in rows:
            if r["LSAD"] in ("Metropolitan Statistical Area", "Micropolitan Statistical Area"):
                w.writerow([r["CBSA"], r["NAME"], r["LSAD"], r["ESTIMATESBASE2020"], r["POPESTIMATE2024"]])


URBAN_ENTITIES = ("World", "United States", "China", "India", "Japan", "United Kingdom", "Germany", "France",
                  "Italy", "Brazil", "Mexico", "Nigeria", "Indonesia", "Russia", "South Korea", "Egypt", "Pakistan",
                  "Bangladesh", "Ethiopia", "Netherlands", "Spain", "Canada")


def refresh_urban_share() -> None:
    d = DATASETS["urban_share"]
    raw = RAW / "urbanization-last-500-years.csv"
    sha = _download(d["url"], raw)
    if sha != d["sha256"]:
        print(f"urban_share: the download differs from the recorded vintage ({sha[:12]})")
    with open(raw, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(HERE / "urban_share_1500_2025.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entity", "code", "year", "share"])
        for r in rows:
            if int(r["year"]) >= 1500 and (r["entity"] in URBAN_ENTITIES or not r["code"]):
                w.writerow([r["entity"], r["code"], r["year"], _fmt(float(r["urbc_c_share"]))])


def refresh_trefler_hov() -> None:
    raw = RAW / "hov_pub.dat"
    sha = _download(DATASETS["trefler_hov"]["url"], raw)
    if sha != DATASETS["trefler_hov"]["sha256"]:
        print(f"trefler_hov: the download differs from the recorded vintage ({sha[:12]})")
    with open(HERE / "trefler_hov.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["country", "factor", "at", "v", "y", "b", "ypc", "pop"])
        for line in raw.read_text().splitlines():
            if line.strip():
                w.writerow([line[0:12].strip(), line[13:25].strip(), *line[26:].split()])


def refresh_jst() -> None:
    import openpyxl  # noqa: PLC0415

    raw = RAW / "JSTdatasetR6.xlsx"
    sha = _download(DATASETS["jst"]["url"], raw)
    if sha != DATASETS["jst"]["sha256"]:
        print(f"jst: the download differs from the recorded vintage ({sha[:12]})")
    rows = list(openpyxl.load_workbook(raw, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    with open(HERE / "jst.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(JST_COLS)
        for r in rows[1:]:
            rec = dict(zip(head, r))
            out = []
            for k in JST_COLS:
                v = rec.get(k)
                if k in ("country", "iso"):
                    out.append(str(v))
                elif k == "year":
                    out.append(int(v))
                else:
                    out.append(_fmt(float(v)) if isinstance(v, (int, float)) else "")
            w.writerow(out)


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


WDI_MONEY = {"money": "FM.LBL.BMNY.ZG", "cpi": "FP.CPI.TOTL.ZG", "deflator": "NY.GDP.DEFL.KD.ZG",
             "growth": "NY.GDP.MKTP.KD.ZG", "m_gdp": "FM.LBL.BMNY.GD.ZS"}


def wdi_money() -> list[dict]:
    """The money-and-prices extract of the WDI: one row per country and year (1960 on, countries only, no aggregates),
    ``code``, ``country``, ``region``, ``income``, ``year`` and the :data:`WDI_MONEY` columns (NaN where missing)."""
    out = []
    for r in _read(HERE / "wdi_money_1960_2024.csv"):
        row = {k: r[k] for k in ("code", "country", "region", "income")}
        row["year"] = int(r["year"])
        for k in WDI_MONEY:
            row[k] = _num(r[k])
        out.append(row)
    return out


def refresh_wdi_money() -> None:
    import json  # noqa: PLC0415

    raw = RAW / "wdi_countries.json"
    _download("https://api.worldbank.org/v2/country?format=json&per_page=400", raw)
    meta = {c["id"]: c for c in json.loads(raw.read_text())[1] if c["region"]["id"] != "NA"}
    vals: dict = {}
    for col, ind in WDI_MONEY.items():
        for a in range(1960, 2025, 5):   # the API times out on the whole span at once
            f = RAW / f"wdimoney_{ind}_{a}.json"
            if not (f.exists() and f.stat().st_size > 1000):   # resume: keep chunks already fetched
                _download(DATASETS["wdi_money"]["url"].format(ind, a, min(a + 4, 2024)), f)
            for r in json.loads(f.read_text())[1] or []:
                code = r["countryiso3code"]
                if code in meta and r["value"] is not None:
                    vals.setdefault((code, int(r["date"])), {})[col] = r["value"]
    with open(HERE / "wdi_money_1960_2024.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["code", "country", "region", "income", "year", *WDI_MONEY])
        for (code, year) in sorted(vals):
            c = meta[code]
            v = vals[(code, year)]
            w.writerow([code, c["name"], c["region"]["value"].strip(), c["incomeLevel"]["value"], year,
                        *[_fmt(v.get(k)) for k in WDI_MONEY]])


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
           "rtdsm": refresh_rtdsm, "warheads": refresh_warheads, "census_cbsa": refresh_census_cbsa,
           "njmin": refresh_njmin, "wooldridge": refresh_wooldridge,
           "urban_share": refresh_urban_share, "so2": refresh_so2,
           "marriage": refresh_marriage, "democracy": refresh_democracy, "millennium": refresh_millennium,
           "longrun": refresh_longrun, "pwt": refresh_pwt, "shiller": refresh_shiller,
           "wdi_money": refresh_wdi_money, "greenbook": refresh_greenbook,
           "hlw": refresh_hlw, "ramey_zubairy": refresh_ramey_zubairy, "ramey_tax": refresh_ramey_tax,
           "blanchard_leigh": refresh_blanchard_leigh, "rr_hap": refresh_rr_hap, "jst": refresh_jst,
           "bigmac": refresh_bigmac, "wdi_ca": refresh_wdi_ca, "trefler_hov": refresh_trefler_hov,
           "cepii_gravity": refresh_cepii_gravity, "autor_dorn": refresh_autor_dorn, "resume": refresh_resume}


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
