"""Numbers and passages transcribed from publications, for *Economics, Built*.

Each entry is a :class:`Table`: the numbers or the words, the citation, where in the publication they are, the
edition or copy that was read, and the date the transcription was checked against it.  A scene that shows one cites
it on screen with ``tag``; the part's README lists it under its sources.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Table:
    key: str
    cite: str  # the full citation
    tag: str  # the short line for an on-screen tag
    where: str  # the page, table or chapter
    read: str  # the copy that was read
    checked: str  # the date the transcription was checked
    data: dict = field(default_factory=dict)
    note: str = ""


# ---------------------------------------------------------------------------
# Part 1
# ---------------------------------------------------------------------------
BASTIAT_1845 = Table(
    key="bastiat_1845",
    cite="Frédéric Bastiat, Economic Sophisms, First Series (1845), ch. 18, \"There Are No Absolute Principles\"; "
         "translated by Arthur Goddard (Foundation for Economic Education, 1964)",
    tag="Bastiat, Economic Sophisms (1845), ch. 18",
    where="First Series, chapter 18",
    read="Library of Economics and Liberty (econlib.org), Goddard translation",
    checked="2026-11-18",
    data={
        "million": "Here are a million human beings who would all die in a few days if supplies of all sorts did "
                   "not flow into this great metropolis.",
        "sleeping": "And yet all are sleeping peacefully at this moment, without being disturbed for a single "
                    "instant by the idea of so frightful a prospect.",
        "departments": "eighty departments have worked today, without co-operative planning or mutual "
                       "arrangements, to keep Paris supplied.",
        "how": "How does each succeeding day manage to bring to this gigantic market just what is necessary, "
               "neither too much nor too little?",
        "suffering": "Although there may be much suffering within your walls, although misery, despair, and "
                     "perhaps starvation, cause more tears to flow than your warmhearted charity can wipe away",
    },
    note="Bastiat wrote the passage as an argument for free trade; the series quotes his question, not his "
         "conclusion, and gives the other side in the same part.",
)

BRITISH_ACADEMY_2009 = Table(
    key="british_academy_2009",
    cite="Tim Besley and Peter Hennessy, letter to Her Majesty The Queen, 22 July 2009, \"The Global Financial "
         "Crisis: Why Didn't Anybody Notice?\", British Academy Review 14 (November 2009), 8-10",
    tag="Besley and Hennessy, letter to the Queen, 22 July 2009",
    where="British Academy Review, issue 14, pp. 8-10",
    read="the British Academy's PDF of issue 14",
    checked="2026-11-18",
    data={
        "visit": "5 November 2008",  # the caption of figure 1: shown a display by Professor Luis Garicano
        "shown_by": "Professor Luis Garicano",
        "question": "why had nobody noticed that the credit crunch was on its way?",
        "forum": "17 June 2009",
        "sent": "22 July 2009",
        "answer": "the failure to foresee the timing, extent and severity of the crisis and to head it off, while "
                  "it had many causes, was principally a failure of the collective imagination of many bright "
                  "people, both in this country and internationally, to understand the risks to the system as a "
                  "whole.",
        "foresaw": "Many people did foresee the crisis. However, the exact form that it would take and the timing "
                   "of its onset and ferocity were foreseen by nobody.",
    },
    note="The letter paraphrases the Queen's question; the Review's introduction gives it as \"if these things "
         "were so large, how come everyone missed them?\"",
)

SMITH_1776 = Table(
    key="smith_1776",
    cite="Adam Smith, An Inquiry into the Nature and Causes of the Wealth of Nations (1776), Book I, chapter 1",
    tag="Adam Smith, The Wealth of Nations (1776), Book I, ch. 1",
    where="Book I, chapter 1, \"Of the Division of Labour\"",
    read="Library of Economics and Liberty, Cannan edition (1904)",
    checked="2026-11-18",
    data={
        "operations": 18, "men": 10, "pounds_per_day": 12, "pins_per_pound": 4000, "pins_per_day": 48000,
        "per_person": 4800, "alone_at_most": 20, "alone_perhaps": 1,
        "ratio_low": 240, "ratio_high": 4800,
        "steps": ["draws out the wire", "straights it", "cuts it", "points it", "grinds it at the top for receiving "
                  "the head", "makes the head", "puts it on", "whitens the pins", "puts them into the paper"],
    },
)

HAYEK_1945 = Table(
    key="hayek_1945",
    cite="Friedrich A. Hayek, \"The Use of Knowledge in Society\", American Economic Review 35(4), 1945, 519-530",
    tag="Hayek, \"The Use of Knowledge in Society\" (1945)",
    where="sections IV and V",
    read="Library of Economics and Liberty",
    checked="2026-11-18",
    data={
        "tin": "Assume that somewhere in the world a new opportunity for the use of some raw material, say, tin, "
               "has arisen, or that one of the sources of supply of tin has been eliminated. It does not matter "
               "for our purpose, and it is very significant that it does not matter, which of these two causes "
               "has made tin more scarce.",
        "economize": "All that the users of tin need to know is that some of the tin they used to consume is now "
                     "more profitably employed elsewhere and that, in consequence, they must economize tin.",
        "dials": "a system of telecommunications which enables individual producers to watch merely the movement "
                 "of a few pointers, as an engineer might watch the hands of a few dials",
        "marvel": "The marvel is that in a case like that of a scarcity of one raw material, without an order "
                  "being issued, without more than perhaps a handful of people knowing the cause, tens of "
                  "thousands of people whose identity could not be ascertained by months of investigation, are "
                  "made to use the material or its products more sparingly",
    },
)

SMITH_1962 = Table(
    key="smith_1962",
    cite="Vernon L. Smith, \"An Experimental Study of Competitive Market Behavior\", Journal of Political Economy "
         "70(2), 1962, 111-137",
    tag="Vernon Smith (1962), JPE 70: 111-137",
    where="pp. 111-114 (the design); the first session was in January 1956 and variations followed until 1960, "
          "by Smith's own account (Nobel autobiography, 2002)",
    read="the JSTOR copy",
    checked="2026-11-18",
    data={
        "began": 1956,
        "period_minutes": (5, 10),
        "rules": ["each buyer and each seller holds a card with a private limit price",
                  "a buyer may call out a bid at or below his card, a seller an offer at or above hers",
                  "anyone may accept a standing bid or offer: a binding contract",
                  "the pair drop out for the rest of the period; the market reopens each period with the same "
                  "cards"],
        "example_bid": ("$2.50 card", "Buy at $1.00"),
        "example_offer": ("$1.50 card", "Sell at $3.60"),
    },
)

CHAMBERLIN_1948 = Table(
    key="chamberlin_1948",
    cite="Edward H. Chamberlin, \"An Experimental Imperfect Market\", Journal of Political Economy 56(2), 1948, "
         "95-108",
    tag="Chamberlin (1948), JPE 56: 95-108",
    where="the results as summarized by Roth (1995), Handbook of Experimental Economics, ch. 1",
    read="secondary summaries (Roth 1995; Berczi 1979); the original was not re-read",
    checked="2026-11-18",
    data={"design": "students with private reservation prices, bargaining in pairs, moving freely around the room",
          "finding": "the number of units traded met or exceeded the competitive quantity in every session"},
)

GNEEZY_RUSTICHINI_2000 = Table(
    key="gneezy_rustichini_2000",
    cite="Uri Gneezy and Aldo Rustichini, \"A Fine Is a Price\", Journal of Legal Studies 29(1), 2000, 1-17",
    tag="Gneezy and Rustichini (2000), J. Legal Studies 29: 1-17, Table 1",
    where="Table 1 (number of late-coming parents per week, by day-care centre)",
    read="the authors' copy at rady.ucsd.edu",
    checked="2026-11-18",
    data={
        "city": "Haifa", "when": "January to June 1998", "weeks": 20,
        "fine_from_week": 5, "fine_until_week": 16, "fine_nis": 10, "late_minutes": 10,
        "fee_nis_month": 1400, "nis_per_usd": 3.68,
        "test": [1, 2, 3, 4, 5, 6], "control": [7, 8, 9, 10],
        # centre: (children, [late arrivals in weeks 1..20])
        "centres": {
            1: (37, [8, 8, 7, 6, 8, 9, 9, 12, 13, 13, 15, 13, 14, 16, 14, 15, 16, 13, 15, 17]),
            2: (35, [6, 7, 3, 5, 2, 11, 14, 9, 16, 12, 10, 14, 14, 16, 12, 17, 14, 10, 14, 15]),
            3: (35, [8, 9, 8, 9, 3, 5, 15, 18, 16, 14, 20, 18, 25, 22, 27, 19, 20, 23, 23, 22]),
            4: (34, [10, 3, 14, 9, 6, 24, 8, 22, 22, 19, 25, 18, 23, 22, 24, 17, 15, 23, 25, 18]),
            5: (33, [13, 12, 9, 13, 15, 10, 27, 28, 35, 10, 24, 32, 29, 29, 26, 31, 26, 35, 29, 28]),
            6: (28, [5, 8, 7, 5, 5, 9, 12, 14, 19, 17, 14, 13, 10, 15, 14, 16, 6, 12, 17, 13]),
            7: (35, [7, 10, 12, 6, 4, 13, 7, 8, 5, 12, 3, 5, 6, 13, 7, 4, 7, 10, 4, 6]),
            8: (34, [12, 9, 14, 18, 10, 11, 6, 15, 14, 13, 7, 12, 9, 9, 17, 8, 5, 11, 8, 13]),
            9: (34, [3, 4, 9, 3, 3, 5, 9, 5, 2, 7, 6, 6, 9, 4, 9, 2, 3, 8, 3, 5]),
            10: (32, [15, 13, 13, 12, 10, 9, 15, 15, 15, 10, 17, 12, 13, 11, 14, 17, 12, 9, 15, 13]),
        },
        # Table 2's period means, used to check the transcription (its weeks 5-16 means are truncated to one
        # decimal, not rounded: centre 1's 151/12 = 12.58 is printed 12.5)
        "table2": {1: (7.25, 9.5, 12.5, 15.25), 2: (5.25, 9, 12.2, 13.25), 3: (8.5, 10.25, 16.8, 22),
                   4: (9, 15, 19.1, 20.25), 5: (11.75, 20, 24.6, 29.5), 6: (6.25, 10, 13.1, 12),
                   7: (8.75, 8, 7.2, 6.75), 8: (13.25, 10.5, 10.9, 9.25), 9: (4.75, 5.5, 5.5, 4.75),
                   10: (13.25, 12.25, 13.1, 12.25)},
    },
    note="Week 11 had four days of observation; the authors scaled it by 5/4.  The six test centres were chosen "
         "at random from the ten.  A later survey-based study (Metcalf et al.) did not find the same effect in "
         "its setting; the series enters the finding with its record in Part 45.",
)

SIMON_1991 = Table(
    key="simon_1991",
    cite="Herbert A. Simon, \"Organizations and Markets\", Journal of Economic Perspectives 5(2), 1991, 25-44",
    tag="Simon, \"Organizations and Markets\" (1991), JEP 5(2): 27-28",
    where="pp. 27-28, \"The Ubiquity of Organizations\"",
    read="the JEP copy",
    checked="2026-11-18",
    data={
        "green": "The firms reveal themselves, say, as solid green areas with faint interior contours marking out "
                 "divisions and departments.",
        "red": "Market transactions show as red lines connecting firms, forming a network in the spaces between "
               "them.",
        "blue": "the approaching visitor also sees pale blue lines, the lines of authority connecting bosses with "
                "various levels of workers.",
        "message": "large green areas interconnected by red lines",
        "not": "a network of red lines connecting green spots",
    },
)

RICARDO_1817 = Table(
    key="ricardo_1817",
    cite="David Ricardo, On the Principles of Political Economy and Taxation (1817), chapter 7, \"On Foreign Trade\"",
    tag="Ricardo, Principles (1817), ch. 7",
    where="chapter 7",
    read="Library of Economics and Liberty (econlib.org)",
    checked="2026-11-18",
    data={"england": {"cloth": 100, "wine": 120}, "portugal": {"cloth": 90, "wine": 80},
          "units": "the labour of so many men for a year"},
)

READ_1958 = Table(
    key="read_1958",
    cite="Leonard E. Read, \"I, Pencil: My Family Tree as told to Leonard E. Read\", The Freeman, December 1958",
    tag="Leonard Read, \"I, Pencil\" (1958)",
    where="the whole essay",
    read="the Foundation for Economic Education's text (fee.org)",
    checked="2026-11-18",
    data={
        "nobody": "not a single person on the face of this earth knows how to make me.",
        "inputs": [("cedar", "Northern California and Oregon"), ("graphite", "Ceylon"),
                   ("factice for the eraser", "rapeseed oil from the Dutch East Indies"), ("pumice", "Italy"),
                   ("the brass ferrule", "zinc and copper"), ("six coats of lacquer", "castor beans and castor oil")],
    },
)

PART1 = (BASTIAT_1845, BRITISH_ACADEMY_2009, SMITH_1776, READ_1958, HAYEK_1945, SMITH_1962, CHAMBERLIN_1948,
         GNEEZY_RUSTICHINI_2000, SIMON_1991, RICARDO_1817)


# ---------------------------------------------------------------------------
# Part 3
# ---------------------------------------------------------------------------
KUZNETS_1934 = Table(
    key="kuznets_1934",
    cite="U.S. Department of Commerce, Bureau of Foreign and Domestic Commerce (Simon Kuznets, with Robert F. Martin, "
         "Robert R. Nathan and others, in cooperation with the National Bureau of Economic Research), National "
         "Income, 1929-32, Senate Document No. 124, 73d Congress, 2d session (Government Printing Office, 1934); "
         "transmitted to the Senate on 4 January 1934",
    tag="National Income, 1929-32 (Senate Document 124, 1934)",
    where="chapter I, section 4, \"Uses and abuses of national income measurements\" (pp. 5-7); tables 1-3 "
          "(pp. 10, 14); the exclusions on p. 11",
    read="the Bureau of Economic Analysis's reprint of the whole report in the Survey of Current Business, "
         "September 2020; tables 2-3 checked against NBER Bulletin 49 (7 June 1934), whose figures the report's "
         "table 3 confirms where the reprint's scan is unclear",
    checked="2026-11-19",
    data={
        "years": (1929, 1930, 1931, 1932),
        # table 1, millions of dollars
        "paid_out": (81136, 75410, 63247, 48894),
        "business_savings": (1896, -5065, -8604, -9529),
        "produced": (83032, 70345, 54643, 39365),
        "cost_of_living": (100.0, 97.4, 88.9, 80.4),        # BLS, 1929 = 100
        "wholesale": (100.0, 90.7, 76.6, 68.0),
        # table 2, millions of dollars
        "salaries_selected": (5702, 5661, 4738, 3383),
        "wages_selected": (17179, 14210, 10542, 6840),
        "salaries_wages_other": (29052, 27794, 24622, 20302),
        "labour": (52793, 48582, 40896, 31533),
        "dividends": (5964, 5795, 4313, 2588),
        "interest": (5677, 5815, 5649, 5491),
        "property": (12206, 12226, 10498, 8472),
        "rents_royalties": (4116, 3475, 2752, 1865),
        "withdrawals": (12020, 11127, 9102, 7024),
        "entrepreneurial": (16136, 14602, 11853, 8890),
        "imputed_rent_1930": 2.7e3,     # owner-occupied homes, excluded (p. 11)
        "king_1920_21_drop": 14.4,      # percent, the earlier depression in King's series (p. 10)
        "welfare": "The welfare of a nation can, therefore, scarcely be inferred from a measurement of national "
                   "income as defined above.",
        "housewives": "A student of social affairs who is interested in the total productivity of the nation, "
                      "including those efforts which, like housewives' services, do not appear on the market, can "
                      "therefore use our measures only with some qualifications.",
        "abuse": "a decline of 30 percent in the national income (in terms of \"constant\" dollars) means a 30 "
                 "percent decline in the total productivity of the nation, and a corresponding decline in its "
                 "welfare",
        "precision": "the definiteness of the result suggests, often misleadingly, a precision and simplicity in "
                     "the outlines of the object measured.",
    },
    note="The report's table 2 gives entrepreneurial income in 1932 as 8,890 (8,390 in the bulletin's scan is a "
         "misreading; 8,890 / 81,136 x 100 matches table 3's share).",
)

PETTY_1665 = Table(
    key="petty_1665",
    cite="William Petty, Verbum Sapienti (written 1665, published 1691), chapters 1-2, in The Economic Writings of "
         "Sir William Petty, ed. Charles Henry Hull (Cambridge University Press, 1899), vol. 1",
    tag="Petty, Verbum Sapienti (1665), chs. 1-2",
    where="chapter 1, paragraph 1; chapter 2, paragraph 1; Hull's note on the date",
    read="Hull's edition, vol. 1 (Internet Archive, economicwritings01pettuoft)",
    checked="2026-11-19",
    data={
        "people": 6.0e6, "expense_per_head": "6l. 13s. 4d.", "expense": 40.0e6,
        "stock_yields": 15.0e6, "labour_yields": 25.0e6, "land_rent": 8.0e6,
        "expense_quote": "about six Millions, whose Expence at 6l. 13s. 4d. per Annum ... for Food, Housing, "
                         "Cloaths, and all other necessaries, amount to 40 Millions per Annum.",
        "labour_quote": "if the Annual proceed of the Stock, or Wealth of the Nation, yields but 15 millions, and the "
                        "expence be 40. Then the labour of the People must furnish the other 25",
    },
    note="Hull dates the manuscript to the latter part of 1665 (Petty's own list puts it opposite that year); it was "
         "first printed in 1691.",
)

CPI_BIAS = Table(
    key="cpi_bias",
    cite="Advisory Commission to Study the Consumer Price Index (Boskin, Dulberger, Gordon, Griliches and Jorgenson), "
         "Toward a More Accurate Measure of the Cost of Living, final report to the Senate Finance Committee, "
         "December 1996; David E. Lebow and Jeremy B. Rudd, \"Measurement Error in the Consumer Price Index: Where "
         "Do We Stand?\", Journal of Economic Literature 41(1): 159-201 (2003); Brent R. Moulton, The Measurement "
         "of Output, Prices, and Productivity: What's Changed Since the Boskin Commission? (Brookings Institution, "
         "July 2018); Robert J. Gordon, \"The Boskin Commission Report: A Retrospective One Decade Later\", NBER "
         "Working Paper 12311 (2006)",
    tag="Boskin et al. (1996); Lebow and Rudd (2003); Moulton (2018)",
    where="Moulton (2018), table 5 (from Boskin et al. 1996, p. 44, and Lebow and Rudd 2003, p. 161); Gordon "
          "(2006), table 1 and abstract",
    read="Moulton's report (brookings.edu) and Gordon's working paper (nber.org); the Lebow-Rudd abstract (RePEc)",
    checked="2026-11-19",
    data={
        "components": ("upper-level substitution", "lower-level substitution", "new products and quality",
                       "new outlets", "weighting"),
        # percentage points a year, in the order of "components"
        "boskin_1996": (0.15, 0.25, 0.60, 0.10, 0.0), "boskin_range": (0.80, 1.60), "boskin_total": 1.10,
        "lebow_rudd_2003": (0.30, 0.05, 0.37, 0.05, 0.10), "lebow_rudd_range": (0.30, 1.40),
        "lebow_rudd_total": 0.87,
        "moulton_2018": (0.25, 0.05, 0.37, 0.08, 0.10), "moulton_range": (0.30, 1.40), "moulton_total": 0.85,
        "moulton_pce_total": 0.47,
        "gordon_1995_96": (1.2, 1.3), "gordon_2006": 0.8,
        "debt_1997_2008": 1.07e12,   # the Commission's figure for the bias's addition to the debt (Gordon, note 1)
        "appointed": "June 1995",
    },
)

DEATON_HESTON_2010 = Table(
    key="deaton_heston_2010",
    cite="Angus Deaton and Alan Heston, \"Understanding PPPs and PPP-based National Accounts\", American Economic "
         "Journal: Macroeconomics 2(4): 1-35 (2010); NBER Working Paper 14499 (2008)",
    tag="Deaton and Heston (2010)",
    where="abstract",
    read="NBER Working Paper 14499 (nber.org)",
    checked="2026-11-19",
    data={"china_smaller": 40, "india_smaller": 36, "round": 2005},
)

JONES_KLENOW_2016 = Table(
    key="jones_klenow_2016",
    cite="Charles I. Jones and Peter J. Klenow, \"Beyond GDP? Welfare across Countries and Time\", American "
         "Economic Review 106(9): 2426-2457 (2016); NBER Working Paper 16352 (2010, revised April 2015)",
    tag="Jones and Klenow (2016)",
    where="table 2 (welfare across countries), and the France example of section 1",
    read="NBER Working Paper 16352, revised April 2015 (nber.org)",
    checked="2026-11-19",
    data={
        # consumption-equivalent welfare and income per person, US = 100, micro data (about 2005)
        "rows": (("U.S.", 100.0, 100.0), ("U.K.", 96.6, 75.2), ("France", 91.8, 67.2), ("Italy", 80.2, 66.1),
                 ("Spain", 73.3, 61.1), ("Mexico", 21.9, 28.6), ("Russia", 20.7, 37.0), ("Brazil", 11.1, 17.2),
                 ("South Africa", 7.4, 16.0), ("China", 6.3, 10.1), ("Indonesia", 5.0, 7.8), ("India", 3.2, 5.6),
                 ("Malawi", 0.9, 1.3)),
        "france": {"consumption": 60, "life_expectancy": (80.1, 77.4), "hours": (535, 877),
                   "sd_log_c": (0.422, 0.538)},
        "correlation": 0.98,
    },
)

NORDHAUS_TOBIN_1972 = Table(
    key="nordhaus_tobin_1972",
    cite="William D. Nordhaus and James Tobin, \"Is Growth Obsolete?\", in Economic Research: Retrospect and "
         "Prospect, Volume 5: Economic Growth (NBER, 1972), pp. 1-80",
    tag="Nordhaus and Tobin (1972)",
    where="the observations on table 2",
    read="the NBER chapter (nber.org, c7620)",
    checked="2026-11-19",
    data={"mew_growth": 1.1, "nnp_growth": 1.7, "period": "1929-65"},
)

PSZ_2018 = Table(
    key="psz_2018",
    cite="Thomas Piketty, Emmanuel Saez and Gabriel Zucman, \"Distributional National Accounts: Methods and "
         "Estimates for the United States\", Quarterly Journal of Economics 133(2): 553-609 (2018); Gerald Auten "
         "and David Splinter, \"Income Inequality in the United States: Using Tax Data to Measure Long-Term "
         "Trends\", Journal of Political Economy 132(7) (2024)",
    tag="Piketty, Saez and Zucman (2018); Auten and Splinter (2024)",
    where="PSZ, introduction (pre-tax national income per adult); Auten and Splinter, abstract",
    read="PSZ's version of 25 September 2017 (eml.berkeley.edu); Auten and Splinter's abstract (search-level)",
    checked="2026-11-19",
    data={
        "bottom50_share": (20.0, 12.0), "top1_share": (12.0, 20.0), "years": (1980, 2014),
        "bottom50_income": 16000, "average_growth": 60, "average_2014": 64500,
        "top1_income": (420000, 1.3e6), "ratio": (27, 81),
        "as_top1_pretax_rise": 4.4, "as_top1_aftertax_rise": 1.4, "as_years": (1979, 2019),
    },
)

PART3 = (KUZNETS_1934, PETTY_1665, CPI_BIAS, DEATON_HESTON_2010, JONES_KLENOW_2016, NORDHAUS_TOBIN_1972, PSZ_2018)


# ---------------------------------------------------------------------------
# Part 4
# ---------------------------------------------------------------------------
MOORE_1914 = Table(
    key="moore_1914",
    cite="Henry L. Moore, Economic Cycles: Their Law and Cause (Macmillan, 1914), p. 126; Philip G. Wright, "
         "\"Moore's Economic Cycles\", Quarterly Journal of Economics 29(2): 631-641 (1915)",
    tag="Moore, Economic Cycles (1914), p. 126; Wright (1915)",
    where="Moore p. 126; Wright's review",
    read="both as quoted and summarized in the editorial of The Econometrics Journal 28(1) (2025), \"Philip G. Wright, "
         "directed acyclic graphs, and instrumental variables\" (arXiv 2501.16395v2)",
    checked="2026-11-19",
    data={
        "moore": "Unlike the law of demand for the crops, the law of demand for a representative producers' good is "
                 "such that as the supply increases the price rises, and as the supply decreases the price falls.",
        "wright_1915": "rainfall shifts the supply of crops but, through business conditions, the demand for a "
                       "producers' good like pig iron; Moore's upward-sloping curve for pig iron may be closer to a "
                       "supply curve",
    },
    note="The 1915 sentence is the editorial's summary of Wright's argument, not a quotation.",
)

LEAMER_1983 = Table(
    key="leamer_1983",
    cite="Edward E. Leamer, \"Let's Take the Con out of Econometrics\", American Economic Review 73(1): 31-43 (1983)",
    tag="Leamer, AER (1983), p. 37",
    where="p. 37",
    read="a scan of the article (gwern.net)",
    checked="2026-11-19",
    data={"quote": "Hardly anyone takes data analyses seriously. Or perhaps more accurately, hardly anyone takes "
                   "anyone else's data analyses seriously.",
          "birds": "Like elaborately plumed birds who have long since lost the ability to procreate but not the "
                   "desire, we preen and strut and display our t-values."},
)

LALONDE_1986 = Table(
    key="lalonde_1986",
    cite="Robert J. LaLonde, \"Evaluating the Econometric Evaluations of Training Programs with Experimental Data\", "
         "American Economic Review 76(4): 604-620 (1986)",
    tag="LaLonde, AER (1986), table 5",
    where="table 5 (male participants), and the text on table 4 (women)",
    read="a scan of the article (gwern.net)",
    checked="2026-11-19",
    data={
        "units": "1982 dollars; standard errors in parentheses in the paper",
        "experiment": (886, 476), "women_experiment": (851, 317),
        # comparison group: (1978 difference, unadjusted; adjusted; difference in differences without age; with age)
        "PSID-1": (-15578, -8067, 425, -749), "CPS-SSA-1": (-8870, -4416, 1714, 195),
        "PSID-3": (697, -509, 242, -1325), "CPS-SSA-3": (-1300, 224, -1637, -1388),
    },
)

CARD_2001 = Table(
    key="card_2001",
    cite="David Card, \"Estimating the Return to Schooling: Progress on Some Persistent Econometric Problems\", "
         "Econometrica 69(5): 1127-1160 (2001); NBER Working Paper 7769 (2000)",
    tag="Card, Econometrica (2001), table 2",
    where="table 2 (OLS and IV estimates with instruments based on features of the school system)",
    read="NBER Working Paper 7769 (nber.org)",
    checked="2026-11-19",
    data={"rows": (
        # (study, sample, OLS, IV, IV standard error), returns per year of schooling
        ("Angrist and Krueger (1991)", "US men born 1920-29, quarter of birth", 0.070, 0.101, 0.033),
        ("Angrist and Krueger (1991)", "US men born 1930-39", 0.063, 0.060, 0.030),
        ("Angrist and Krueger (1991)", "US men born 1940-49", 0.052, 0.078, 0.030),
        ("Staiger and Stock (1997)", "US men born 1930-39, LIML", 0.063, 0.098, 0.015),
        ("Kane and Rouse (1993)", "US women, tuition and distance", 0.080, 0.091, 0.033),
        ("Card (1995)", "US men, a college nearby", 0.073, 0.132, 0.049),
        ("Conneely and Uusitalo (1997)", "Finnish men, a university town", 0.085, 0.110, 0.024),
        ("Harmon and Walker (1995)", "British men, school-leaving age", 0.061, 0.153, 0.015),
        ("Lemieux and Card (1998)", "Ontario veterans, 1971 census", 0.070, 0.164, 0.053),
        ("Maluccio (1997)", "rural Philippines, distance to school", 0.073, 0.145, 0.041),
        ("Duflo (1999)", "Indonesia, school building", 0.078, 0.064, 0.025),
    )},
    note="Rows measured per year of schooling only (Card's rows 7 and 9, with schooling as a dummy, are left out).",
)

LUCAS_1976 = Table(
    key="lucas_1976",
    cite="Robert E. Lucas, Jr., \"Econometric Policy Evaluation: A Critique\", Carnegie-Rochester Conference Series "
         "on Public Policy 1: 19-46 (1976)",
    tag="Lucas (1976), p. 41",
    where="p. 41, the 'single syllogism'",
    read="the sentence as quoted with its page in the secondary literature (the Wikipedia article's footnote and "
         "the papers it cites); the article itself was not read",
    checked="2026-11-19",
    data={"quote": "Given that the structure of an econometric model consists of optimal decision rules of economic "
                   "agents, and that optimal decision rules vary systematically with changes in the structure of "
                   "series relevant to the decision maker, it follows that any change in policy will "
                   "systematically alter the structure of econometric models."},
)

PART4 = (MOORE_1914, LEAMER_1983, LALONDE_1986, CARD_2001, LUCAS_1976)
# ---------------------------------------------------------------------------
# Part 5
# ---------------------------------------------------------------------------
SAMUELSON_1938 = Table(
    key="samuelson_1938",
    cite="Paul A. Samuelson, \"A Note on the Pure Theory of Consumer's Behaviour\", Economica, New Series, 5(17): "
         "61-71 (February 1938)",
    tag="Samuelson, Economica (1938)",
    where="the programme stated in the paper's opening pages",
    read="the phrase as found by a full-text search of the article; its context from I. Moscati, \"Not a "
         "behaviorist: Samuelson's contributions to utility theory in the Harvard years, 1936-1940\" (LSE eprint "
         "90415, 2019), which warns against reading Samuelson as a strict behaviourist",
    checked="2026-11-19",
    data={"vestiges": "dropping off the last vestiges of the utility analysis"},
)

HARBAUGH_2001 = Table(
    key="harbaugh_2001",
    cite="William T. Harbaugh, Kate Krause and Timothy R. Berry, \"GARP for Kids: On the Development of Rational "
         "Choice Behavior\", American Economic Review 91(5): 1539-1545 (2001)",
    tag="Harbaugh, Krause and Berry, AER (2001), tables 1-2",
    where="section III (protocol) and tables 1 and 2",
    read="the authors' copy (harbaugh.uoregon.edu)",
    checked="2026-11-19",
    data={"sets": 11, "goods": ("bags of potato chips", "boxes of fruit juice"),
          "groups": {"second graders": {"n": 31, "age": 7, "violations": 4.3, "afriat": 0.93, "zero": 0.26},
                     "sixth graders": {"n": 42, "age": 11, "violations": 2.1, "afriat": 0.96, "zero": 0.62},
                     "undergraduates": {"n": 55, "age": 21, "violations": 2.0, "afriat": 0.94, "zero": 0.65},
                     "random (uniform)": {"violations": 8.91, "afriat": 0.648},
                     "random (bootstrap)": {"violations": 8.29, "afriat": 0.749, "zero": 0.02}},
          "animals": {"rats": 0.87, "pigeons": 0.81}},
    note="'zero' is the share of each group with no GARP violations (table 2). The animals line is Harbaugh et al.'s "
         "summary of Kagel, Battalio and Green (1995): the share that reduced consumption of a good after an "
         "income-compensated rise in its price.",
)

CHOI_2007 = Table(
    key="choi_2007",
    cite="Syngjoo Choi, Raymond Fisman, Douglas Gale and Shachar Kariv, \"Consistency and Heterogeneity of "
         "Individual Behavior under Uncertainty\", American Economic Review 97(5): 1921-1938 (2007)",
    tag="Choi, Fisman, Gale and Kariv, AER (2007)",
    where="the published results as reported by Choi, Kariv, Mueller and Silverman (2014), footnote 5; the random "
          "benchmarks from the working paper's section 3",
    read="Choi et al. (2014), AER version (eml.berkeley.edu/~kariv); the working paper CFGK_I.pdf",
    checked="2026-11-19",
    data={"subjects": 93, "budgets": 50, "above_95": 60, "mean_ccei": 0.954,
          "random": {"budgets_50": {"mean_ccei": 0.60, "above_90_of_25000": 12},
                     "budgets_25": {"consistent": 0.043, "above_95": 0.143, "above_90": 0.289},
                     "budgets_10": {"consistent": 0.202, "above_95": 0.373, "above_90": 0.506}}},
)

CKMS_2014 = Table(
    key="ckms_2014",
    cite="Syngjoo Choi, Shachar Kariv, Wieland Mueller and Dan Silverman, \"Who Is (More) Rational?\", American "
         "Economic Review 104(6): 1518-1550 (2014)",
    tag="Choi, Kariv, Mueller and Silverman, AER (2014)",
    where="sections I-III; the introduction for the wealth result",
    read="the AER version (eml.berkeley.edu/~kariv/CKMS_I_AER.pdf)",
    checked="2026-11-19",
    data={"subjects": 1182, "budgets": 25, "mean_ccei": 0.881, "panel": "CentERpanel, the Netherlands",
          "gaps": {"low income": 3.3, "low education": 2.6, "women": 2.4, "old": 5.1},
          "wealth_per_sd": (0.15, 0.19)},
    note="'gaps': how many more percentage points of their budgets each group leaves on the table than its "
         "comparison group (high income, high education, men, young).",
)

ANDREONI_MILLER_2002 = Table(
    key="andreoni_miller_2002",
    cite="James Andreoni and John Miller, \"Giving According to GARP: An Experimental Test of the Consistency of "
         "Preferences for Altruism\", Econometrica 70(2): 737-753 (2002)",
    tag="Andreoni and Miller, Econometrica (2002)",
    where="the introduction and section 2",
    read="the published article (econweb.ucsd.edu)",
    checked="2026-11-19",
    data={"subjects": 176, "consistent": 0.98, "selfish": 0.25},
    note="'consistent': over 98% made choices consistent with utility maximization; 'selfish': about a quarter were "
         "selfish money-maximizers.",
)

CHEN_2023 = Table(
    key="chen_2023",
    cite="Yiting Chen, Tracy Xiao Liu, You Shan and Songfa Zhong, \"The Emergence of Economic Rationality of GPT\", "
         "Proceedings of the National Academy of Sciences 120(51) (2023); arXiv 2305.12763",
    tag="Chen, Liu, Shan and Zhong, PNAS (2023)",
    where="section 3 (rationality score) and figure D1",
    read="arXiv 2305.12763v3 (6 November 2023)",
    checked="2026-11-19",
    data={"gpt": {"risk": 0.998, "time": 0.997, "social": 0.997, "food": 0.999},
          "humans": {"risk": 0.980, "time": 0.985, "social": 0.967, "food": 0.963},
          "literature": {"low": 0.81, "high": 0.99, "mean": 0.918}},
)

SAEZ_2010 = Table(
    key="saez_2010",
    cite="Emmanuel Saez, \"Do Taxpayers Bunch at Kink Points?\", American Economic Journal: Economic Policy 2(3): "
         "180-212 (2010)",
    tag="Saez, AEJ: Policy (2010)",
    where="the introduction and table 1, panel B",
    read="the author's copy (eml.berkeley.edu/~saez)",
    checked="2026-11-19",
    data={"one_child_2008": {"phase_in": (0, 8580, 0.34), "plateau": (8580, 15740), "phase_out": (15740, 33995,
                                                                                                  0.16)},
          "two_children_2008": {"phase_in": (0, 12060, 0.40), "plateau": (12060, 15740), "phase_out": (15740,
                                                                                                    38646, 0.21)},
          "elasticity": {"all": 0.25, "self_employed": 1.0, "wage_earners": 0.0}},
    note="Dollars of 2008. The elasticities are of reported earnings, implied by the bunching at the first kink.",
)

MCFADDEN_BART = Table(
    key="mcfadden_bart",
    cite="Daniel McFadden, \"The Path to Discrete-Choice Models\", Access 20 (Spring 2002), from his Nobel lecture "
         "\"Economic Choices\", American Economic Review 91(3) (2001)",
    tag="McFadden, Access 20 (2002)",
    where="the BART forecast",
    read="Access magazine's article (accessmagazine.org); the Library of Economics and Liberty's biography",
    checked="2026-11-19",
    data={"official": 0.15, "mcfadden": 0.063, "actual": 0.062, "year_forecast": 1973, "year_actual": 1975},
    note="Shares of work trips taken on BART in the San Francisco Bay Area.",
)

PART5 = (SAMUELSON_1938, HARBAUGH_2001, CHOI_2007, CKMS_2014, ANDREONI_MILLER_2002, CHEN_2023, SAEZ_2010,
         MCFADDEN_BART)

# ---------------------------------------------------------------------------
# Part 6
# ---------------------------------------------------------------------------
JENSEN_MILLER_2008 = Table(
    key="jensen_miller_2008",
    cite="Robert T. Jensen and Nolan H. Miller, \"Giffen Behavior and Subsistence Consumption\", American Economic "
         "Review 98(4): 1553-1577 (2008)",
    tag="Jensen and Miller, AER (2008)",
    where="sections II-IV, tables 1-3 and figure 2",
    read="the authors' manuscript of January 2008, \"forthcoming, American Economic Review\" "
         "(nmiller.web.illinois.edu)",
    checked="2026-11-19",
    data={
        "design": {"households": 1300, "per_province": 650, "individuals": 3661, "counties": 11,
                   "cuts_yuan_per_jin": (0.10, 0.20, 0.30), "rice_price_hunan": 1.20, "flour_price_gansu": 1.04,
                   "subsidy_months": "June-October 2006", "rounds": ("April 2006", "September 2006",
                                                                    "December 2006"),
                   "voucher_cap_g_per_person_day": 750, "attrition_households": 11},
        "diet": {"rice_g_per_day_hunan": 330, "rice_calorie_share_hunan": 0.64, "wheat_g_per_day_gansu": 344,
                 "wheat_calorie_share_gansu": 0.69, "meat_g_per_day_hunan": 42, "meat_calorie_share_hunan": 0.07,
                 "meat_calorie_share_gansu": 0.01},
        "calories_per_yuan": {"rice (Hunan)": 1399, "wheat flour (Gansu)": 1655, "wheat": 1221, "millet": 537,
                              "pork": 331, "bean curd": 239, "cabbage": 141},
        # Table 3, Hunan: the arc percent change in rice on the arc percent change in its price, county x round
        # fixed effects, standard errors clustered by household
        "hunan": {"full": (0.224, 0.149, 1258), "full_controls": (0.235, 0.140, 1258),
                  "share_le_080": (0.451, 0.170, 997), "share_gt_080": (-0.61, 0.296, 261),
                  "share_060_080": (0.640, 0.192, 513), "meat_full": (-0.325, 0.472, 997),
                  "meat_over_50g": (-1.125, 0.625, 452), "p_full": 0.14},
        "hunan_local": {"positive_from": 0.53, "positive_to": 0.84, "significant_from": 0.63,
                        "significant_to": 0.75, "peak": 0.85, "peak_at": 0.70, "turns_negative": 0.80},
        "gansu": {"positive_from": 0.40, "positive_to": 0.60, "range_040_060": 1.07, "meat_over_50g": 1.3},
        "marshall_1895": "As Mr. Giffen has pointed out, a rise in the price of bread makes so large a drain on the "
                         "resources of the poorer labouring families and raises so much the marginal utility of "
                         "money to them, that they are forced to curtail their consumption of meat and the more "
                         "expensive farinaceous foods: and, bread being still the cheapest food which they can get "
                         "and will take, they consume more, and not less of it.",
        "stigler_1987": "if an economist were to demonstrate its failure in a particular market at a particular "
                        "time, he would be assured of immortality, professionally speaking, and rapid promotion "
                        "while still alive.",
    },
    note="1 jin = 500 g; 1 yuan was about $0.13.  Marshall's passage is from the third edition of his Principles "
         "(1895), p. 208, and Stigler's from The Theory of Price, 4th edition (1987), p. 23, both as quoted by "
         "Jensen and Miller.  The published article's tables carry the same estimates.",
)

HAUSMAN_1997 = Table(
    key="hausman_1997",
    cite="Jerry A. Hausman, \"Valuation of New Goods under Perfect and Imperfect Competition\", in T. F. "
         "Bresnahan and R. J. Gordon (eds.), The Economics of New Goods, NBER Studies in Income and Wealth 58, "
         "University of Chicago Press (1997), chapter 5",
    tag="Hausman, in The Economics of New Goods (1997)",
    where="sections 5.2-5.6",
    read="the NBER chapter (nber.org/chapters/c6068)",
    checked="2026-11-19",
    data={"introduced": 1989, "virtual_price": 7.14, "virtual_price_ase": 1.33, "average_price": 3.48,
          "cs_per_city_week": 32268, "cs_us_year_million": 78.1, "cs_per_person_year": 0.3136,
          "cs_imperfect_us_year_million": 66.8, "imperfect_share": 0.856, "cereal_cpi_overstated": 0.25,
          "cereal_cpi_overstated_imperfect": 0.20, "new_brands_1980_92": 190, "existing_brands": 160,
          "segment_own_price_elasticity": -2.0},
    note="Prices are per unit of the brand as sold in his scanner data (dollars of the early 1990s).",
)

COSTA_2001 = Table(
    key="costa_2001",
    cite="Dora L. Costa, \"Estimating Real Income in the United States from 1888 to 1994: Correcting CPI Bias "
         "Using Engel Curves\", Journal of Political Economy 109(6): 1288-1310 (2001)",
    tag="Costa, JPE (2001)",
    where="the abstract and section VI, pp. 1305-1306",
    read="a copy of the published article (gwern.net/doc/economics/2001-costa.pdf)",
    checked="2026-11-19",
    data={"bias_per_year": {"1888-1919": -0.1, "1919-1935": 0.7, "1960-1972": 0.4, "1972-1982": 2.7,
                            "1982-1994": 0.6, "1972-1994": 1.6},
          "hamilton_2001": {"1974-1982": 2.7, "1982-1991": 0.6, "overall": 1.6},
          "nordhaus_1997": 1.5},
    note="Percentage points a year by which the CPI overstated the rise in the cost of living.  Hamilton's figures "
         "(American Economic Review 91(3): 619-630, 2001, from the Panel Study of Income Dynamics) are as Costa "
         "reports them.",
)

ENGEL_1857 = Table(
    key="engel_1857",
    cite="Ernst Engel, \"Die Productions- und Consumtionsverhältnisse des Königreichs Sachsen\" (1857), as "
         "translated in C. C. Zimmerman, \"Ernst Engel\'s Law of Expenditures for Food\", Quarterly Journal of "
         "Economics 47(1): 78-101 (1932); H. S. Houthakker, \"An International Comparison of Household Expenditure "
         "Patterns, Commemorating the Centenary of Engel\'s Law\", Econometrica 25(4): 532-551 (1957); J. L. "
         "Seale and A. Regmi, \"Modeling International Consumption Patterns\", Review of Income and Wealth 52(4): "
         "603-624 (2006)",
    tag="Engel (1857), via Zimmerman (1932); Houthakker (1957)",
    where="as quoted and summarized by R. Anker, \"Engel\'s Law Around the World 150 Years Later\", PERI "
          "Working Paper 247 (2011), pp. 1-3",
    read="Anker's working paper (peri.umass.edu)",
    checked="2026-11-19",
    data={"engel": "The poorer is a family, the greater is the proportion of the total outgo [family "
                   "expenditures] which must be used for food. ... The proportion of the outgo used for food, other "
                   "things being equal, is the best measure of the material standard of living of a population.",
          "houthakker": "Engel's law, formulated in 1857, is confirmed by all surveys.",
          "houthakker_food_elasticity": 0.6, "houthakker_surveys": 40, "houthakker_countries": 30,
          "seale_regmi": {"low income": 0.7, "lower middle income": 0.6, "upper middle income": 0.5,
                          "high income": (0.1, 0.3)}},
    note="Engel's budgets were the Belgian working families of Ducpétiaux's survey (1853-55) and his own Saxon "
         "data.  Seale and Regmi's are income elasticities of food expenditure across countries by income group.",
)

ERS_FOOD_2024 = Table(
    key="ers_food_2024",
    cite="USDA Economic Research Service, \"Food spending as a share of income declines as income rises\" (W. "
         "Sinclair and H. Stewart, Ag and Food Statistics: Charting the Essentials, 30 April 2026), from the BLS "
         "Consumer Expenditure Survey, 2024",
    tag="USDA ERS (2026), from the BLS Consumer Expenditure Survey, 2024",
    where="Food Prices and Spending, the chart and its text",
    read="ers.usda.gov, Ag and Food Statistics: Charting the Essentials, Food Prices and Spending",
    checked="2026-11-19",
    data={"lowest": {"food": 5498, "share": 0.330}, "middle": {"food": 9097, "share": 0.122},
          "highest": {"food": 16989, "share": 0.064},
          "us_calories_2025": 3902, "nigeria_calories_2025": 2470},
    note="Dollars a household a year; shares are of before-tax income, by income quintile.",
)

JARAVEL_2019 = Table(
    key="jaravel_2019",
    cite="Xavier Jaravel, \"The Unequal Gains from Product Innovations: Evidence from the U.S. Retail Sector\", "
         "Quarterly Journal of Economics 134(2): 715-783 (2019); X. Jaravel and D. Lashkari, \"Measuring Growth "
         "in Consumer Welfare with Income-Dependent Preferences: Nonparametric Methods and Estimates for the "
         "United States\", Quarterly Journal of Economics 139(1): 477-532 (2024)",
    tag="Jaravel, QJE (2019); Jaravel and Lashkari, QJE (2024)",
    where="the abstracts",
    read="the abstracts as listed on EconPapers and by the LSE's Centre for Economic Performance",
    checked="2026-11-19",
    data={"retail_gap": (0.661, 0.0535), "retail_gap_variety": (0.8846, 0.0739), "full_basket_gap": (0.368, 0.0502),
          "years": "2004-2015", "share_explained": 0.5,
          "lashkari_1955_understated": 0.115, "lashkari_growth_bp": 18},
    note="Percentage points a year by which annual inflation was higher for the bottom income quintile than the "
         "top (standard errors in the second place).  Jaravel and Lashkari: real consumption per household in "
         "1955 understated by 11.5% by the uncorrected measure; growth 1955-2019 lower by 18 basis points a year.",
)

BLS_CPI_METHODS = Table(
    key="bls_cpi_methods",
    cite="U.S. Bureau of Labor Statistics, Handbook of Methods, \"Consumer Price Index: Calculation\"; "
         "\"Chained CPI: questions and answers\"",
    tag="BLS, Handbook of Methods: the CPI",
    where="Calculation; the chained CPI",
    read="bls.gov, as quoted in search results of the Handbook and the chained CPI pages",
    checked="2026-11-19",
    data={"geometric_mean_since": "January 1999", "chained_published": 2002, "chained_from": "January 2000",
          "chained_formula": "Tornqvist", "item_area_indexes": 7776},
    note="The geometric mean is used within most item strata (it allows substitution between, say, varieties of "
         "apples); the chained index (C-CPI-U) also allows substitution across strata.",
)

SLUTSKY_1915 = Table(
    key="slutsky_1915",
    cite="Eugen Slutsky, \"Sulla teoria del bilancio del consumatore\", Giornale degli Economisti e Rivista di "
         "Statistica 51 (July 1915); J. R. Hicks and R. G. D. Allen, \"A Reconsideration of the Theory of "
         "Value\", Economica (1934); H. Schultz, \"Interrelations of Demand, Price, and Income\", Journal of "
         "Political Economy (1935); R. G. D. Allen, \"Professor Slutsky\'s Theory of Consumers\' Choice\", "
         "Review of Economic Studies (1936); J. R. Hicks, Value and Capital (1939)",
    tag="Slutsky (1915); Chipman and Lenfant, HOPE (2002)",
    where="J. S. Chipman and J.-S. Lenfant, \"Slutsky\'s 1915 Article: How It Came to Be Found and "
          "Interpreted\", History of Political Economy 34(3): 553-597 (2002), the opening pages",
    read="the article's first page (Project MUSE) and its abstract (RePEc)",
    checked="2026-11-19",
    data={"published": "July 1915", "sent_from": "Kiev", "rediscovered_by": ("Henry Schultz", "Hicks and Allen",
                                                                            "R. G. D. Allen"),
          "hicks_and_allen": 1934, "allen": 1936, "hicks_name": "the Fundamental Equation of Value Theory"},
    note="Hicks and Allen reached the decomposition in 1934 without knowing of Slutsky's paper; Hicks later wrote "
         "that it had to be rediscovered.",
)

PART6 = (JENSEN_MILLER_2008, HAUSMAN_1997, COSTA_2001, ENGEL_1857, ERS_FOOD_2024, JARAVEL_2019, BLS_CPI_METHODS,
         SLUTSKY_1915)

# ---------------------------------------------------------------------------
# Part 7
# ---------------------------------------------------------------------------
BERNOULLI_1738 = Table(
    key="bernoulli_1738",
    cite="Daniel Bernoulli, \"Specimen Theoriae Novae de Mensura Sortis\", Commentarii Academiae Scientiarum "
         "Imperialis Petropolitanae 5: 175-192 (1738); translated by Louise Sommer as \"Exposition of a New Theory "
         "on the Measurement of Risk\", Econometrica 22(1): 23-36 (1954)",
    tag="Bernoulli (1738); the St Petersburg paradox",
    where="the Stanford Encyclopedia of Philosophy, \"The St. Petersburg Paradox\", on Nicolaus Bernoulli's letter, "
          "Cramer's and Daniel Bernoulli's answers; Bernoulli's twenty ducats as quoted by Hayden and Platt (2009), "
          "p. 2, from Baron (1998)",
    read="the encyclopedia entry; Hayden and Platt's article (journal.sjdm.org)",
    checked="2026-11-19",
    data={"posed": "Nicolaus Bernoulli, in a letter to Pierre Remond de Montmort, 9 September 1713",
          "cramer": "Gabriel Cramer, in a letter to Nicolaus Bernoulli (1728): the square root of money; the game "
                    "worth about 2.9", "daniel": 1738, "utility": "the logarithm of wealth",
          "twenty_ducats": "any fairly reasonable man would sell his chance, with great pleasure, for twenty ducats",
          "game": "one ducat if heads first appears on the first toss, two on the second, four on the third, and "
                  "so on"},
    note="Daniel Bernoulli acknowledged that Cramer had reached a similar answer ten years before him.",
)

SAMUELSON_1937 = Table(
    key="samuelson_1937",
    cite="Paul A. Samuelson, \"A Note on Measurement of Utility\", Review of Economic Studies 4(2): 155-161 (1937)",
    tag="Samuelson, RES (1937)",
    where="pp. 159 and 161, as quoted by Frederick, Loewenstein and O'Donoghue, \"Time Discounting and Time "
          "Preference: A Critical Review\", Journal of Economic Literature 40(2): 351-401 (2002), pp. 355-356",
    read="Frederick, Loewenstein and O'Donoghue (2002), the published article",
    checked="2026-11-19",
    data={"arbitrary": "It is completely arbitrary to assume that the individual behaves so as to maximize an "
                       "integral of the form envisaged", "disavowed": "any connection between utility as discussed "
                       "here and any welfare concept is disavowed",
          "koopmans": "Tjalling Koopmans (1960) later derived discounted utility from axioms on preferences"},
)

ALLAIS_1953 = Table(
    key="allais_1953",
    cite="Maurice Allais, \"Le comportement de l'homme rationnel devant le risque: critique des postulats et "
         "axiomes de l'ecole americaine\", Econometrica 21(4): 503-546 (1953); L. J. Savage, The Foundations of "
         "Statistics (1954), ch. 5; D. Kahneman and A. Tversky, \"Prospect Theory: An Analysis of Decision under "
         "Risk\", Econometrica 47(2): 263-291 (1979)",
    tag="Allais, Econometrica (1953); Kahneman and Tversky (1979)",
    where="the colloquium on risk of the CNRS, Paris, May 1952, as told by Savage (1954) and in the secondary "
          "literature; Kahneman and Tversky's problems 1 and 2",
    read="Savage's account (secondary sources); Kahneman and Tversky (1979), p. 265",
    checked="2026-11-19",
    data={"pairs": {"1A": "$1 million for sure", "1B": "10%: $5 million; 89%: $1 million; 1%: nothing",
                    "2A": "11%: $1 million; 89%: nothing", "2B": "10%: $5 million; 90%: nothing"},
          "colloquium": "Paris, May 1952", "savage": "Savage's own first answers broke the independence axiom; in "
                        "his book he wrote that on reflection he changed them",
          "kt_problem1_sure": 0.82},
    note="Kahneman and Tversky's version uses 2,400 and 2,500 Israeli pounds: in their problem 1, 82% chose 2,400 "
         "for sure over a 33% chance of 2,500, 66% of 2,400 and 1% of nothing.",
)

ELLSBERG_1961 = Table(
    key="ellsberg_1961",
    cite="Daniel Ellsberg, \"Risk, Ambiguity, and the Savage Axioms\", Quarterly Journal of Economics 75(4): "
         "643-669 (1961)",
    tag="Ellsberg, QJE (1961), pp. 653-655",
    where="pp. 653-655",
    read="the published article (a copy hosted at UC Irvine)",
    checked="2026-11-19",
    data={"urn": {"red": 30, "black_or_yellow": 60}, "prize": 100,
          "bets": {"I": "red", "II": "black", "III": "red or yellow", "IV": "black or yellow"},
          "pattern": "A very frequent pattern of response is: action I preferred to II, and IV preferred to III.",
          "take_your_time": "Take your time!",
          "abide": ("G. Debreu", "R. Schlaifer", "P. Samuelson")},
    note="Ellsberg names Debreu, Schlaifer and Samuelson among those who do not violate the axioms, or say they "
         "won't.",
)

RABIN_2000 = Table(
    key="rabin_2000",
    cite="Matthew Rabin, \"Risk Aversion and Expected-Utility Theory: A Calibration Theorem\", Econometrica 68(5): "
         "1281-1292 (2000)",
    tag="Rabin, Econometrica (2000), tables I and II",
    where="p. 1282 (the two examples) and tables I and II",
    read="the published article (dklevine.com copy)",
    checked="2026-11-19",
    data={"example": "Suppose that, from any initial wealth level, a person turns down gambles where she loses $100 "
                     "or gains $110, each with 50% probability. Then she will turn down 50-50 bets of losing $1,000 "
                     "or gaining any sum of money.",
          "example2": "A person who would always turn down 50-50 lose $1,000/gain $1,050 bets would always turn "
                      "down 50-50 bets of losing $20,000 or gaining any sum.",
          # table I: turning down lose $100 / gain g at every wealth; for each loss L the largest G still turned down
          "table1_g110": {400: 550, 600: 990, 800: 2090, 1000: float("inf"), 2000: float("inf")},
          "table1_g101": {400: 400, 600: 600, 800: 800, 1000: 1010, 2000: 2320, 4000: 5750, 6000: 11810,
                          8000: 34940, 10000: float("inf"), 20000: float("inf")},
          # table II: turning down lose $100 / gain $110 only at wealth below $300,000, starting from $290,000
          "table2_g110": {1000: 718_190, 2000: 12_210_880, 10000: 1_300_000_000},
          "rabin_thaler_2001": "M. Rabin and R. H. Thaler, \"Anomalies: Risk Aversion\", Journal of Economic "
                               "Perspectives 15(1): 219-232 (2001): they felt \"much like the customer in the pet "
                               "shop, beating at a dead parrot\", and closed that expected utility is \"an "
                               "ex-hypothesis\""},
    note="Rabin and Thaler's two phrases as quoted by A. Rubinstein, Econometrica 74(4) (2006), and by J. C. Cox and "
         "V. Sadiraj (working paper, Georgia State); checked 2026-11-19.",
)

THALER_1981 = Table(
    key="thaler_1981",
    cite="Richard Thaler, \"Some Empirical Evidence on Dynamic Inconsistency\", Economics Letters 8(3): 201-207 "
         "(1981)",
    tag="Thaler (1981), via Frederick, Loewenstein and O'Donoghue (2002)",
    where="as reported by Frederick, Loewenstein and O'Donoghue, JEL 40(2) (2002), p. 360",
    read="Frederick, Loewenstein and O'Donoghue (2002)",
    checked="2026-11-19",
    data={"now": 15, "months": (1, 12, 120), "median_equivalent": (20, 50, 100), "annual_rate": (3.45, 1.20, 0.19),
          "reversal": "$110 in 31 days over $100 in 30 days, but $100 today over $110 tomorrow"},
    note="The rates are continuously compounded annual rates; the reversal is the textbook example of the same "
         "survey's pattern.",
)

HOLT_LAURY_2005 = Table(
    key="holt_laury_2005",
    cite="Charles A. Holt and Susan K. Laury, \"Risk Aversion and Incentive Effects\", American Economic Review "
         "92(5): 1644-1655 (2002); \"Risk Aversion and Incentive Effects: New Data without Order Effects\", "
         "American Economic Review 95(3): 902-904 (2005)",
    tag="Holt and Laury, AER (2002, 2005)",
    where="Holt and Laury (2005), table 1",
    read="the 2005 note (copy hosted at UCSD)",
    checked="2026-11-19",
    data={"menu": {"A": (2.00, 1.60), "B": (3.85, 0.10)},
          "real_2002": {1: 5.2, 20: 6.0, 50: 6.8, 90: 7.2}, "hypothetical_2002": {20: 4.9, 50: 5.1, 90: 5.3},
          "real_ordered_2004": {1: 6.1, 20: 7.1}, "real_unordered_2004": {1: 5.7, 20: 6.7},
          "hypothetical_unordered_2004": {1: 5.6, 20: 5.7}, "subjects_2002": 208, "subjects_2004": 216,
          "top_stakes": "the 90x treatment paid from $9.00 to $346.50"},
    note="Average number of safe choices out of ten; a risk-neutral chooser makes four.",
)

HAYDEN_PLATT_2009 = Table(
    key="hayden_platt_2009",
    cite="Benjamin Y. Hayden and Michael L. Platt, \"The mean, the median, and the St. Petersburg paradox\", "
         "Judgment and Decision Making 4(4): 256-272 (2009)",
    tag="Hayden and Platt, JDM (2009)",
    where="section 3 and figure 2",
    read="the published article (journal.sjdm.org)",
    checked="2026-11-19",
    data={"real": {"n": 20, "median_bid": 1.75}, "hypothetical": {"n": 220, "median_bid": 1.50, "max_bid": 50_000,
                                                                 "refused": 14, "below_1": 26, "at_1": 68,
                                                                 "at_2": 43, "above_2": 56},
          "truncated": {"tosses": (3, 5, 8, 10, 15), "ev": (2.50, 3.50, 5.0, 6.0, 8.50), "bids": "$1.50 or $2"},
          "finding": "bids were typically lower than twice the smallest payoff"},
)

MADRIAN_SHEA_2001 = Table(
    key="madrian_shea_2001",
    cite="Brigitte C. Madrian and Dennis F. Shea, \"The Power of Suggestion: Inertia in 401(k) Participation and "
         "Savings Behavior\", Quarterly Journal of Economics 116(4): 1149-1187 (2001)",
    tag="Madrian and Shea, QJE (2001); NBER WP 7682",
    where="NBER Working Paper 7682 (2000), pp. 10-11 and section on contribution rates",
    read="the NBER working paper",
    checked="2026-11-19",
    data={"date": "1 April 1998", "default_rate": 0.03, "default_fund": "the money market fund",
          "participation": {"auto-enrolled (3-15 months' tenure)": 0.86, "hired the year before, same tenure": 0.37},
          "at_default": 0.76, "others_at_3pct": 0.10},
    note="The published version's figures are close to the working paper's; these are the working paper's.",
)

THALER_BENARTZI_2004 = Table(
    key="thaler_benartzi_2004",
    cite="Richard H. Thaler and Shlomo Benartzi, \"Save More Tomorrow: Using Behavioral Economics to Increase "
         "Employee Saving\", Journal of Political Economy 112(S1): S164-S187 (2004)",
    tag="Thaler and Benartzi, JPE (2004)",
    where="the abstract and the first implementation",
    read="the article's abstract and summary",
    checked="2026-11-19",
    data={"before": 0.035, "after": 0.136, "months": 40},
    note="The participants chose to join, so the rise is not a randomized effect.",
)

BARSKY_1997 = Table(
    key="barsky_1997",
    cite="Robert B. Barsky, F. Thomas Juster, Miles S. Kimball and Matthew D. Shapiro, \"Preference Parameters "
         "and Behavioral Heterogeneity: An Experimental Approach in the Health and Retirement Study\", Quarterly "
         "Journal of Economics 112(2): 537-579 (1997)",
    tag="Barsky, Juster, Kimball and Shapiro, QJE (1997)",
    where="the survey's income gambles; the abstract",
    read="the NBER working paper's abstract and summary",
    checked="2026-11-19",
    data={"question": "a job with your current income for life, or one with a 50-50 chance of doubling it or cutting "
                      "it by a third; then by a half, or by a fifth",
          "cuts": (0.5, 1 / 3, 0.2), "mean_risk_tolerance": 0.25, "mean_eis": 0.2,
          "correlated": "risk tolerance and the EIS are essentially uncorrelated across people"},
)

POST_2008 = Table(
    key="post_2008",
    cite="Thierry Post, Martijn J. van den Assem, Guido Baltussen and Richard H. Thaler, \"Deal or No Deal? "
         "Decision Making under Risk in a Large-Payoff Game Show\", American Economic Review 98(1): 38-71 (2008)",
    tag="Post, van den Assem, Baltussen and Thaler, AER (2008)",
    where="the abstract",
    read="the abstract",
    checked="2026-11-19",
    data={"finding": "risk aversion falls after contestants' expectations are shattered by opening high-value "
                     "cases, or surpassed: the break-even effect; choices depend on the path, which points to "
                     "reference dependence"},
)

MEHRA_PRESCOTT_1985 = Table(
    key="mehra_prescott_1985",
    cite="Rajnish Mehra and Edward C. Prescott, \"The Equity Premium: A Puzzle\", Journal of Monetary Economics "
         "15(2): 145-161 (1985)",
    tag="Mehra and Prescott, JME (1985)",
    where="the abstract and introduction; table 1 (means and standard deviations, 1889-1978)",
    read="secondary summaries; the table's figures as reproduced from the paper",
    checked="2026-11-20",
    data={"premium": 0.06, "period": (1889, 1978), "plausible_rra": 10, "stock": 0.0698, "sd_stock": 0.1654,
          "bill": 0.0080, "sd_bill": 0.0567, "premium_mean": 0.0618, "sd_premium": 0.1667, "growth": 0.0183,
          "sd_growth": 0.0357, "model_max_premium": 0.0035},
    note="About six points a year of excess return on stocks over short-term bonds; Mehra and Prescott took relative "
         "risk aversion of ten or less as plausible, and the model with such values cannot produce it.",
)

# ---------------------------------------------------------------------------
# Part 8
# ---------------------------------------------------------------------------
COBB_DOUGLAS_1928 = Table(
    key="cobb_douglas_1928",
    cite="C. W. Cobb and P. H. Douglas, \"A Theory of Production\", American Economic Review 18(1), supplement "
         "(March 1928) 139-165; the data as reproduced by J. Felipe and F. G. Adams, \"'A Theory of Production': The "
         "Estimation of the Cobb-Douglas Function: A Retrospective View\", Eastern Economic Journal 31(3) (2005) "
         "427-445, table 1 (from Pesaran and Pesaran 1997, data file CD.FIT)",
    tag="Cobb and Douglas (1928), via Felipe and Adams (2005), table 1",
    where="Felipe and Adams (2005), table 1 (indices, 1899 = 100) and table 2 (regressions); checked against the "
          "logarithms tabulated by Smirnov and Wang (arXiv 1910.06739)",
    read="Felipe and Adams (2005), the published article; Smirnov and Wang (2019)",
    checked="2026-11-19",
    data={"years": tuple(range(1899, 1923)),
          # output (Day's index of physical production), labour (wage earners employed), capital (fixed capital in
          # constant dollars), American manufacturing, 1899 = 100
          "output": (100, 101, 112, 122, 124, 122, 143, 152, 151, 126, 155, 159, 153, 177, 184, 169, 189, 225, 227,
                     223, 218, 231, 179, 240),
          "labour": (100, 105, 110, 118, 123, 116, 125, 133, 138, 121, 140, 144, 145, 152, 154, 149, 154, 182, 196,
                     200, 193, 193, 147, 161),
          "capital": (100, 107, 114, 122, 131, 138, 149, 163, 176, 185, 198, 208, 216, 226, 236, 244, 266, 298, 335,
                      366, 387, 407, 417, 431),
          "felipe_adams": {"unrestricted": {"labour": 0.807, "capital": 0.233},
                           "trend": {"trend": 0.0468, "labour": 0.906, "capital": -0.526},
                           "growth": {"labour": 1.39, "capital": -1.51},
                           "to_1920": {"labour": 1.09, "capital": 0.08}},
          "verdict": "if computer technology had allowed Cobb and Douglas to perform the analysis carried out here, "
                     "their results would have been dismissed",
          "cobb": "Douglas went to his friend Charles W. Cobb, of the mathematics faculty at Amherst, and asked for a "
                  "function to measure the effect of each factor; the paper was presented at the American Economic "
                  "Association's meetings of 1927",
          "solow": "we would not now be concerned with the question had Paul Douglas found labor's share of American "
                   "output to be twenty-five per cent and capital's share seventy-five instead of the other way around",
          "solow_cite": "Solow, as quoted by F. M. Fisher (1969), p. 572, and by Felipe and Adams (2005)"},
    note="Douglas plotted the three indices on a logarithmic scale and noticed that output lay about a quarter of the "
         "way from labour's curve to capital's (Felipe and Adams 2005, p. 428).",
)

PART8 = (COBB_DOUGLAS_1928,)

# ---------------------------------------------------------------------------
# Part 9
# ---------------------------------------------------------------------------
RADFORD_1945 = Table(
    key="radford_1945",
    cite="R. A. Radford, \"The Economic Organisation of a P.O.W. Camp\", Economica, New Series 12(48): 189-201 "
         "(November 1945)",
    tag="Radford, Economica 12(48) (1945)",
    where="pp. 189-201: the introduction (p. 190), the development of the market (pp. 190-192), the cigarette "
          "currency (pp. 194-195), paper currency (pp. 196-197), the conclusion (pp. 200-201)",
    read="the article as printed (a scan of the journal pages)",
    checked="2026-11-19",
    data={
        "camps": "Oflags (officers' camps) of between 1,200 and 2,500 prisoners, in bungalows of about 200",
        "parcel": ("tinned milk", "jam", "butter", "biscuits", "bully", "chocolate", "sugar", "cigarettes"),
        "first_parcel": "a quarter of a Red Cross food parcel each, a week after reaching a transit camp in Italy, "
                        "about a fortnight after capture",
        "equal": "Everyone receives a roughly equal share of essentials; it is by trade that individual preferences "
                 "are given expression and comfort increased.",
        "padre": "Stories circulated of a padre who started off round the camp with a tin of cheese and five "
                 "cigarettes and returned to his bed with a complete parcel in addition to his original cheese and "
                 "cigarettes; the market was not yet perfect.",
        "standard": "The cigarette became the standard of value.",
        "offer": "cheese for seven",
        "salmon": "The price of a tin of salmon is known to have varied by two cigarettes in 20 between one end of a "
                  "hut and the other.",
        "salmon_spread": (2, 20),
        "moosburg": "Stalag VIIA at Moosburg in Bavaria, autumn 1943: up to 50,000 prisoners of all nationalities",
        "supply": "the Red Cross issue of 50 or 25 cigarettes per man per week",
        "halved": "In August, 1944, the supplies of parcels and cigarettes were both halved.",
        "bully_mark": "paper money backed 100 per cent. by food: one BMk. was worth one cigarette at first, and fell "
                      "to four-fifths of a cigarette",
        "blizzard": "in February the supplies of food parcels were exhausted and the depression became a blizzard",
        "liberation": "On 12th April, with the arrival of elements of the 30th U.S. Infantry Division, the ushering "
                      "in of an age of plenty demonstrated the hypothesis that with infinite means economic "
                      "organisation and activity would be redundant",
        "bread": "Bread was issued on Thursday and Monday ... by Wednesday and Sunday night it had risen at least one "
                 "cigarette per ration, from seven to eight",
    },
    note="The quotations are verbatim from the printed text; only line breaks differ.",
)

HSIEH_KLENOW_2009 = Table(
    key="hsieh_klenow_2009",
    cite="Chang-Tai Hsieh and Peter J. Klenow, \"Misallocation and Manufacturing TFP in China and India\", "
         "Quarterly Journal of Economics 124(4): 1403-1448 (2009)",
    tag="Hsieh and Klenow, QJE 124(4) (2009)",
    where="the abstract; table 2 (dispersion of TFPR), table 4 (gains from equalizing TFPR within industries), "
          "table 6 (gains relative to 1997 US gains)",
    read="the December 2008 accepted version (it thanks the referees and editors), whose abstract matches the "
         "published one",
    checked="2026-11-19",
    data={
        "sigma": 3.0,
        "sd_log_tfpr": {"China": {1998: 0.74, 2001: 0.68, 2005: 0.63}, "India": {1987: 0.69, 1991: 0.67, 1994: 0.67},
                        "US": {1977: 0.45, 1987: 0.41, 1997: 0.49}},
        "full": {"China": {1998: 115.1, 2001: 95.8, 2005: 86.6}, "India": {1987: 100.4, 1991: 102.1, 1994: 127.5},
                 "US": {1977: 36.1, 1987: 30.7, 1997: 42.9}},
        "to_us_1997": {"China": {1998: 50.5, 2001: 37.0, 2005: 30.5}, "India": {1987: 40.2, 1991: 41.4, 1994: 59.2}},
        "abstract": "When capital and labor are hypothetically reallocated to equalize marginal products to the extent "
                    "observed in the U.S., we calculate manufacturing TFP gains of 30-50% in China and 40-60% in "
                    "India.",
    },
    note="Gains are percent increases in manufacturing TFP; \"full\" equalizes revenue productivity across plants "
         "within each industry, \"to US 1997\" only to the dispersion of the United States in 1997.",
)

BILS_KLENOW_RUANE_2021 = Table(
    key="bils_klenow_ruane_2021",
    cite="Mark Bils, Peter J. Klenow and Cian Ruane, \"Misallocation or Mismeasurement?\", Journal of Monetary "
         "Economics 124(S): S39-S56 (2021); NBER Working Paper 26711 (2020)",
    tag="Bils, Klenow and Ruane, JME (2021); NBER WP 26711",
    where="the working paper's abstract",
    read="NBER Working Paper 26711 (January 2020)",
    checked="2026-11-19",
    data={"india_cut": 0.20, "us_cut": 0.60, "india_years": "1985-2013", "us_years": "1978-2013",
          "abstract": "For Indian manufacturing from 1985-2013, our correction lowers potential gains from "
                      "reallocation by 20%. For the U.S. the effect is even more dramatic, reducing potential gains by "
                      "60%"},
)

KEHOE_2014 = Table(
    key="kehoe_2014",
    cite="Timothy J. Kehoe, \"The Challenges of Predicting the Impact of Trade Reforms\", chapter 1 of NAFTA at 20 "
         "(Federal Reserve Bank of Dallas, 2014), table 1, from Kehoe, Rossbach and Ruhl (2014) and Kehoe (2014); the "
         "evaluation is T. J. Kehoe, \"An Evaluation of the Performance of Applied General Equilibrium Models of the "
         "Impact of NAFTA\", in Frontiers in Applied General Equilibrium Modeling (Cambridge, 2005)",
    tag="Kehoe, NAFTA at 20 (Dallas Fed, 2014), table 1",
    where="table 1: changes in Mexican imports from North America relative to Mexican GDP, by industry (percent)",
    read="the Dallas Fed's conference volume, chapter 1 (pp. 16-20)",
    checked="2026-11-19",
    data={
        "industries": ("Agriculture", "Beverages", "Chemicals", "Electrical machinery", "Food", "Iron and steel",
                       "Leather", "Metal products", "Mining", "Nonelectrical machinery", "Nonferrous metals",
                       "Nonmetallic mineral products", "Other manufactures", "Paper", "Petroleum", "Rubber",
                       "Textiles", "Tobacco", "Transportation equipment", "Wearing apparel", "Wood"),
        "actual": (61.0, 189.0, 218.5, 66.3, 128.8, 92.0, 60.0, 94.8, 79.4, 115.8, 113.9, 64.3, 96.7, 49.7, -71.2,
                   178.2, 131.3, 575.5, 97.7, 29.2, 2.9),
        "sobarzo": (3.4, -1.8, -2.7, 9.6, -5.0, 17.7, -0.4, 9.5, 13.2, 20.7, 9.8, 10.9, 4.2, -4.7, -6.8, -0.1, -1.2,
                    -11.6, 11.2, 4.5, 11.7),
        "ltp": (77.2, 143.2, 115.9, 53.2, 94.7, 115.7, 245.5, 90.9, 97.3, 76.9, 84.2, 215.0, 95.3, 70.9, 68.1, 67.1,
                175.7, 340.5, 56.7, 107.9, 65.6),
        "weighted_corr": {"sobarzo": -0.12, "ltp": 0.47},
        "years": "1989-2009",
        "quote": "if we look at the correlations of what we predicted with what happened, they average about zero",
        "usitc": "USITC, Economy-wide Modeling of the Economic Implications of a FTA with Mexico and a NAFTA with "
                 "Mexico and Canada, USITC publication 2516 (May 1992)",
    },
    note="The weights of the weighted correlations are not given in the chapter; the film recomputes only the "
         "unweighted correlation from the table and labels it so.",
)

EDGEWORTH_1881 = Table(
    key="edgeworth_1881",
    cite="F. Y. Edgeworth, Mathematical Psychics: An Essay on the Application of Mathematics to the Moral Sciences "
         "(London: C. Kegan Paul, 1881)",
    tag="Edgeworth, Mathematical Psychics (1881), pp. 20-21",
    where="p. 20 (the three demonstrations) and p. 21 (the contract-curve named)",
    read="a scan of the 1881 edition",
    checked="2026-11-19",
    data={"answer": "(a) Contract without competition is indeterminate, (b) Contract with perfect competition is "
                    "perfectly determinate, (c) Contract with more or less perfect competition is less or more "
                    "indeterminate.",
          "name": "which locus it is here proposed to call the contract-curve"},
    note="Edgeworth labels the three cases with Greek letters (alpha, beta, gamma); the box diagram itself was drawn "
         "later.",
)

PART9 = (RADFORD_1945, EDGEWORTH_1881, HSIEH_KLENOW_2009, BILS_KLENOW_RUANE_2021, KEHOE_2014)

# ---------------------------------------------------------------------------
# Part 10
# ---------------------------------------------------------------------------
DLEU_2020 = Table(
    key="dleu_2020",
    cite="Jan De Loecker, Jan Eeckhout and Gabriel Unger, \"The Rise of Market Power and the Macroeconomic "
         "Implications\", Quarterly Journal of Economics 135(2): 561-644 (2020)",
    tag="De Loecker, Eeckhout and Unger, QJE 135(2) (2020)",
    where="the abstract",
    read="the published abstract (EconPapers listing)",
    checked="2026-11-19",
    data={"markup_1980": 1.21, "markup_now": 1.61, "now": 2016, "profit_rate": (0.01, 0.08),
          "median": "the median is unchanged", "since": 1955},
    note="Earlier working-paper versions report 18% and 67%; the published abstract's 21% and 61% are used.",
)

TRAINA_2018 = Table(
    key="traina_2018",
    cite="James Traina, \"Is Aggregate Market Power Increasing? Production Trends Using Financial Statements\", "
         "Stigler Center Working Paper 272 (2018)",
    tag="Traina, Stigler Center WP 272 (2018)",
    where="the abstract",
    read="the abstract (RePEc listing)",
    checked="2026-11-19",
    data={"finding": "public firm markups increased only modestly over this time period, and are within historical "
                     "variation", "aggregate": "a flat or even decreasing aggregate markup"},
)

NAKAMURA_ZEROM_2010 = Table(
    key="nakamura_zerom_2010",
    cite="Emi Nakamura and Dawit Zerom, \"Accounting for Incomplete Pass-Through\", Review of Economic Studies "
         "77(3): 1192-1230 (2010); NBER Working Paper 15255 (2009)",
    tag="Nakamura and Zerom, REStud 77(3) (2010)",
    where="the abstract",
    read="NBER Working Paper 15255 (August 2009)",
    checked="2026-11-19",
    data={"local_costs": 0.59, "markups": 0.33, "menu_cost_share_of_revenue": 0.0023, "horizon_quarters": 6,
          "abstract": "Local costs reduce long-run pass-through (after 6 quarters) by a factor of 59% relative to a CES "
                      "benchmark. Markup adjustment reduces pass-through by an additional factor of 33%"},
)

DUBE_MISRA_2023 = Table(
    key="dube_misra_2023",
    cite="Jean-Pierre Dube and Sanjog Misra, \"Personalized Pricing and Consumer Welfare\", Journal of Political "
         "Economy 131(1): 131-189 (2023)",
    tag="Dube and Misra, JPE 131(1) (2023)",
    where="the abstract",
    read="the published abstract (EconPapers listing)",
    checked="2026-11-19",
    data={"profit_vs_uniform": 0.19, "profit_vs_status_quo": 0.86, "share_who_gain": 0.60,
          "setting": "a large-scale field experiment at ZipRecruiter, an online recruiting platform"},
    note="Total consumer surplus falls under personalized pricing, but over 60% of consumers benefit.",
)

PART10 = (DLEU_2020, TRAINA_2018, NAKAMURA_ZEROM_2010, DUBE_MISRA_2023)


# ---------------------------------------------------------------------------
# Part 11
# ---------------------------------------------------------------------------
NAGEL_1995 = Table(
    key="nagel_1995",
    cite="Rosemarie Nagel, \"Unraveling in Guessing Games: An Experimental Study\", American Economic Review 85(5): "
         "1313-1326 (1995)",
    tag="Nagel, American Economic Review 85(5) (1995)",
    where="section III (design) and section IV.A and Figure 1 (first-period choices)",
    read="the published article (JSTOR copy)",
    checked="2026-11-19",
    data={"p_2_3": {"sessions": 4, "subjects": 67, "mean": 36.73, "median": 33, "above_67": 0.10},
          "p_1_2": {"sessions": 3, "subjects": 48, "mean": 27.05, "median": 17},
          "p_4_3": {"sessions": 3, "mean": 60.12, "median": 66},
          "group_size": (15, 18), "prize_dm": 20, "rounds": 4, "step3_or_higher": (0.06, 0.10)},
    note="Fifteen to eighteen subjects a session chose numbers from 0 to 100; the one closest to p times the mean won "
         "20 DM. Over all sessions only 6-10 percent of first-period choices were at iteration step 3 or higher.",
)

THALER_FT_1997 = Table(
    key="thaler_ft_1997",
    cite="Richard Thaler's guessing contest in the Financial Times (1997), as reported in R. Thaler, \"Keynes's "
         "'Beauty Contest'\", Chicago Booth Review (2015) and later accounts",
    tag="Thaler's contest, Financial Times (1997)",
    where="the reported mean and winning number",
    read="secondary accounts (Chicago Booth Review; The National)",
    checked="2026-11-19",
    data={"p": 2 / 3, "range": (0, 100), "mean": 18.9, "winner": 13},
    note="Readers chose a whole number from 0 to 100; the winner was closest to two-thirds of the average. The "
         "original newspaper report was not re-read.",
)

FLOOD_1952 = Table(
    key="flood_1952",
    cite="Merrill M. Flood, \"Some Experimental Games\", RAND Research Memorandum RM-789-1 (1952), and Management "
         "Science 5(1): 5-26 (1958); as reported in W. Poundstone, Prisoner's Dilemma (1992), ch. 6",
    tag="Flood, RAND RM-789-1 (1952), via Poundstone (1992)",
    where="the Flood-Dresher experiment of January 1950",
    read="Poundstone's account and the Stanford Encyclopedia of Philosophy's entry \"Prisoner's Dilemma\"",
    checked="2026-11-19",
    data={"rounds": 100, "mutual_cooperation": 60, "mutual_defection": 14, "players": ("Armen Alchian",
          "John D. Williams"), "year": 1950,
          "nash": "the flaw in this experiment as a test of equilibrium point theory is that the experiment really "
                  "amounts to having the players play one large multimove game"},
    note="The payoff table was asymmetric; the counts of joint outcomes are Poundstone's from the report.",
)

HENRICH_2001 = Table(
    key="henrich_2001",
    cite="Joseph Henrich, Robert Boyd, Samuel Bowles, Colin Camerer, Ernst Fehr, Herbert Gintis and Richard "
         "McElreath, \"In Search of Homo Economicus: Behavioral Experiments in 15 Small-Scale Societies\", American "
         "Economic Review 91(2): 73-78 (2001)",
    tag="Henrich et al., AER 91(2) (2001)",
    where="the text and Table 1",
    read="the published paper (Papers and Proceedings)",
    checked="2026-11-19",
    data={"societies": 15, "mean_offer_range": (0.26, 0.58), "industrial_mean": 0.44, "lowest": "Machiguenga"},
    note="Mean ultimatum offers ranged from 26 to 58 percent of the pie, against about 44 percent in industrial "
         "societies; the canonical selfish model was not supported in any society studied.",
)

CHC_2004 = Table(
    key="chc_2004",
    cite="Colin F. Camerer, Teck-Hua Ho and Juin-Kuan Chong, \"A Cognitive Hierarchy Model of Games\", Quarterly "
         "Journal of Economics 119(3): 861-898 (2004)",
    tag="Camerer, Ho and Chong, QJE 119(3) (2004)",
    where="the abstract and the conclusion",
    read="the published abstract and the authors' working paper",
    checked="2026-11-19",
    data={"tau": 1.5, "range": (1.0, 2.0), "games": "nearly 100"},
    note="An average of about 1.5 steps of thinking fits data from many games; values between 1 and 2 explain results "
         "for nearly 100 games.",
)

AXELROD_1980 = Table(
    key="axelrod_1980",
    cite="Robert Axelrod, \"Effective Choice in the Prisoner's Dilemma\" and \"More Effective Choice in the "
         "Prisoner's Dilemma\", Journal of Conflict Resolution 24(1) and 24(3) (1980); The Evolution of Cooperation "
         "(1984)",
    tag="Axelrod, Journal of Conflict Resolution 24 (1980)",
    where="the two tournaments",
    read="the published abstracts and the 1984 book's account",
    checked="2026-11-19",
    data={"first_entries": 14, "first_rounds": 200, "winner": "TIT FOR TAT", "entrant": "Anatol Rapoport",
          "second_entries": "more than sixty", "second_winner": "TIT FOR TAT"},
    note="Axelrod also reported that TIT FOR TWO TATS would have won the first tournament had it been entered.",
)

PART11 = (NAGEL_1995, THALER_FT_1997, FLOOD_1952, HENRICH_2001, CHC_2004, AXELROD_1980)


# ---------------------------------------------------------------------------------------------------------------
# Part 12: competition among the few

LYSINE_CONNOR_1998 = Table(
    key="lysine_connor_1998",
    cite="John M. Connor, \"Lysine: A Case Study in International Price-Fixing\", Choices 13(3), Third Quarter 1998, "
         "pp. 13-19",
    tag="Connor, Choices 13(3) (1998)",
    where="the chronology and the section on injuries (text, not the figure)",
    read="the article (National Agricultural Law Center reprint)",
    checked="2026-11-19",
    data={
        # US lysine prices, dollars a pound, as the text states them; months between are not stated
        "points": (("1990", 1.30), ("1991-01", 1.20), ("1992-07", 0.64)),
        "spans": (("1992-11", "1993-01", 0.98, 0.98), ("1993-10", "1994-08", 1.08, 1.13)),
        "after_1994_08": "rose again to about $1.20 for another six months",
        "asian_price_late_1980s": (1.00, 2.00),
        "adm_cost": (0.65, 0.70),
        "adm_plant": {"committed": 1989, "cost_musd": 150, "production": "1991-02", "town": "Decatur, Illinois"},
        "first_meeting": ("1992-06", "Mexico City"),
        "mole": ("1992-11", "1995-06"),
        "raid": "the night of 28 June 1995, more than 70 FBI agents",
        "adm_fine_musd": 70,
        "overcharge_musd": (65, 140),
        "sales_musd": (495, 550),
        "overcharge_pct": (12, 28),
        "stock_fall": "24 percent ($2.4 billion) in the three months after the raid",
    },
    note="Connor's text says the first price war took prices to the $0.60-0.70 range for about a year after ADM's "
         "plant opened in 1991, and that output growth was held to half its historical rate.",
)

CONNOR_2014 = Table(
    key="connor_2014",
    cite="John M. Connor, \"Price-Fixing Overcharges: Revised 3rd Edition\" (SSRN, 2014); published as \"Cartel "
         "Overcharges\", in The Law and Economics of Class Actions, Research in Law and Economics 26 (2014): 249-387",
    tag="Connor, Research in Law and Economics 26 (2014)",
    where="the abstract, as quoted by Boyer and Kotchoni (2015)",
    read="the abstract and its citations",
    checked="2026-11-19",
    data={"median_pct": 23.0, "mean_pct_at_least": 49.0, "scope": "all cartels of all times, long run"},
    note="Connor's later fourth edition reports a median of 25 percent; the film uses the 2014 figure that Boyer and "
         "Kotchoni corrected.",
)

BOYER_KOTCHONI_2015 = Table(
    key="boyer_kotchoni_2015",
    cite="Marcel Boyer and Rachidi Kotchoni, \"How Much Do Cartels Overcharge?\", Review of Industrial Organization "
         "47(2) (2015): 119-153",
    tag="Boyer and Kotchoni, RIO 47(2) (2015)",
    where="the abstract",
    read="the abstract (journal and RePEc)",
    checked="2026-11-19",
    data={"bias_corrected_mean_pct": 15.47, "bias_corrected_median_pct": 16.01,
          "corrects": "estimation, publication and endogeneity biases in Connor's database"},
    note="The raw estimates in the same database are substantially higher; the authors' earlier working papers are "
         "withdrawn in favour of the published article.",
)

MERGER_GUIDELINES = Table(
    key="merger_guidelines",
    cite="U.S. Department of Justice and Federal Trade Commission, Merger Guidelines (18 December 2023); Horizontal "
         "Merger Guidelines (19 August 2010)",
    tag="DOJ and FTC, Merger Guidelines (2023)",
    where="Guideline 1 (2023); section 5.3 (2010)",
    read="the guidelines",
    checked="2026-11-19",
    data={"2023": {"highly_concentrated": 1800, "presumption_delta": 100, "share_test": (30, 100)},
          "2010": {"highly_concentrated": 2500, "presumption_delta": 200}},
    note="In 2023 a merger is presumed to lessen competition substantially if it leaves a highly concentrated market "
         "(HHI above 1,800) and raises the HHI by more than 100, or creates a firm with more than 30 percent of the "
         "market with a change above 100.  Before 2010 the threshold for a highly concentrated market was also 1,800.",
)

PART12 = (LYSINE_CONNOR_1998, CONNOR_2014, BOYER_KOTCHONI_2015, MERGER_GUIDELINES)



# ---------------------------------------------------------------------------------------------------------------
# Part 13: lemons and signals

AKERLOF_1970 = Table(
    key="akerlof_1970",
    cite="George A. Akerlof, \"The Market for 'Lemons': Quality Uncertainty and the Market Mechanism\", Quarterly "
         "Journal of Economics 84(3) (1970): 488-500; \"Writing 'The Market for Lemons': A Personal and Interpretive "
         "Essay\" (Nobel Foundation, 2003)",
    tag="Akerlof, QJE 84(3) (1970); Akerlof (2003)",
    where="the article; the essay's account of its rejections, as excerpted in secondary sources",
    read="the article; excerpts of the essay",
    checked="2026-11-19",
    data={"pages": (488, 500), "rejected_by": ("American Economic Review", "Review of Economic Studies",
                                               "Journal of Political Economy"),
          "aer_res": "turned down as trivial: the journals did not publish papers on such subjects",
          "jpe": "the referees held it was wrong: if it were correct, no goods could be traded",
          "nobel": 2001},
    note="The essay recalls the Journal of Political Economy's editor's comment as \"If this is correct, economics "
         "would be different\"; the exact wording is from the essay's secondary accounts.",
)

EFC_2010 = Table(
    key="efc_2010",
    cite="Liran Einav, Amy Finkelstein and Mark R. Cullen, \"Estimating Welfare in Insurance Markets Using Variation "
         "in Prices\", Quarterly Journal of Economics 125(3) (2010): 877-921; NBER Working Paper 14414 (2008)",
    tag="Einav, Finkelstein and Cullen, QJE 125(3) (2010)",
    where="the working paper's Table 4 and section 4",
    read="NBER Working Paper 14414 (October 2008)",
    checked="2026-11-19",
    data={"demand": (0.940, -0.00070), "demand_se": 0.00032, "cost": (391.690, 0.15524), "cost_se": 0.06388,
          "n_demand": 3779, "n_cost": 2465, "p_eq": 463, "p_eff": 264, "share_drop_pp": 14, "gap_at_eq": 138,
          "loss": 9.55, "loss_share_surplus": 0.03, "loss_share_max": 0.023, "max_at_stake": 414,
          "price_range": (384, 659), "subsidy_cost": 45},
    note="Alcoa's salaried workers with family coverage; the relative price of the more generous plan varied across "
         "the company's divisions. Working-paper numbers; the published version's may differ slightly.",
)

CUTLER_ZECKHAUSER_1998 = Table(
    key="cutler_zeckhauser_1998",
    cite="David M. Cutler and Richard J. Zeckhauser, \"Adverse Selection in Health Insurance\", Frontiers in Health "
         "Policy Research 1 (1998): 1-31; David M. Cutler and Sarah J. Reber, \"Paying for Health Insurance: The "
         "Trade-Off between Competition and Adverse Selection\", Quarterly Journal of Economics 113(2) (1998): "
         "433-466",
    tag="Cutler and Zeckhauser (1998); Cutler and Reber, QJE 113(2) (1998)",
    where="the Harvard section and figures 1.3-1.4 of the chapter; Cutler and Reber's abstract",
    read="the chapter (NBER reprint); the article's abstract",
    checked="2026-11-19",
    data={"employees": 10000, "plans_from": 1992,
          # the employee's extra charge for the PPO, 1996 dollars, family policy, and the PPO's share of employees
          "path": ((1994, 450, 0.20), (1995, 1000, 0.15), (1996, 2000, 0.09)),
          "charge_1992_94": (400, 500), "reform": "an equal contribution to every plan: half the employees in 1995, "
                                                  "the rest in 1996",
          "hmo_cut_1995": 1000, "ages_1995": (46, 51), "leavers_1996_healthier": 0.20, "disbanded": 1997,
          "welfare_loss_share": (0.02, 0.04), "premium_cut": (0.05, 0.08)},
    note="The 1994 charge is given as \"about $500\" and the 1996 one as \"more than $2,000\"; 1994's enrollment as "
         "about 20% and 1996's as about 9%.",
)

TYLER_2000 = Table(
    key="tyler_2000",
    cite="John H. Tyler, Richard J. Murnane and John B. Willett, \"Estimating the Labor Market Signaling Value of the "
         "GED\", Quarterly Journal of Economics 115(2) (2000): 431-468",
    tag="Tyler, Murnane and Willett, QJE 115(2) (2000)",
    where="the abstract",
    read="the abstract and its citations",
    checked="2026-11-19",
    data={"white": (0.10, 0.19), "nonwhite": "no statistically discernible effect",
          "design": "differences between states' passing standards", "sample": "16-21-year-old dropouts who "
                                                                                "attempted the GED in 1990"},
    note="The effect is for young white dropouts on the margin of passing.",
)

INFO_TESTS = Table(
    key="info_tests",
    cite="P.-A. Chiappori and B. Salanié, Journal of Political Economy 108(1) (2000): 56-78; A. Finkelstein and K. "
         "McGarry, American Economic Review 96(4) (2006): 938-958; L. Cabral and A. Hortaçsu, Journal of Industrial "
         "Economics 58(1) (2010): 54-78",
    tag="Chiappori and Salanié (2000); Finkelstein and McGarry (2006); Cabral and Hortaçsu (2010)",
    where="the abstracts",
    read="the abstracts and their citations",
    checked="2026-11-19",
    data={"chiappori_salanie": "young French drivers (licensed less than three years): no correlation between "
                               "comprehensive cover and accidents",
          "finkelstein_mcgarry": "long-term care insurance: people's own beliefs predict both buying and using care, "
                                 "but the cautious buy more and use less, so the insured are no likelier to use care",
          "cabral_hortacsu": "eBay: after a seller's first negative feedback, weekly sales growth turns sharply "
                             "negative, and later negatives arrive faster"},
)

HKK_2015 = Table(
    key="hkk_2015",
    cite="Martin B. Hackmann, Jonathan T. Kolstad and Amanda E. Kowalski, \"Adverse Selection and an Individual "
         "Mandate: When Theory Meets Practice\", American Economic Review 105(3) (2015): 1030-1066; Benjamin R. "
         "Handel, \"Adverse Selection and Inertia in Health Insurance Markets: When Nudging Hurts\", American Economic "
         "Review 103(7) (2013): 2643-2682",
    tag="Hackmann, Kolstad and Kowalski, AER 105(3) (2015); Handel, AER 103(7) (2013)",
    where="the abstracts",
    read="the abstracts",
    checked="2026-11-19",
    data={"hkk_gain": 0.041, "hkk_total_musd": 51.1, "hkk_penalty": 2190,
          "handel_loss": 0.082, "handel": "reducing inertia by three quarters doubles the welfare loss from adverse "
                                         "selection, to 8.2% of premiums"},
    note="Hackmann et al.: the welfare gain per person from the Massachusetts mandate's reduction in adverse "
         "selection, as a share of what the study measures (abstract).",
)

PART13 = (AKERLOF_1970, EFC_2010, CUTLER_ZECKHAUSER_1998, TYLER_2000, INFO_TESTS, HKK_2015)



# ---------------------------------------------------------------------------------------------------------------
# Part 14: incentives

LAZEAR_2000 = Table(
    key="lazear_2000",
    cite="Edward P. Lazear, \"Performance Pay and Productivity\", American Economic Review 90(5) (2000): 1346-1361; "
         "NBER Working Paper 5672 (1996)",
    tag="Lazear, AER 90(5) (2000)",
    where="the published estimate as summarized by the Stanford GSB and later papers; the working paper's abstract and "
          "conclusion",
    read="NBER Working Paper 5672; secondary summaries of the published version",
    checked="2026-11-19",
    data={"firm": "Safelite Glass", "switch": "from hourly wages to piece rates, 1994-95", "gain_published": 0.44,
          "split": "about half from incentives (the same workers producing more), about half from sorting",
          "gain_wp": (0.20, 0.36), "wage_rise": 0.096,
          "passed_on": "about half of the worker-specific gain in productivity, in higher wages"},
    note="The 1996 working paper puts the gain at 20 to 36 percent, depending on what is held constant, with more "
         "than half from incentives; the published paper's 44 percent is the figure usually cited.",
)

PIECE_RATES = Table(
    key="piece_rates",
    cite="Bruce Shearer, \"Piece Rates, Fixed Wages and Incentives: Evidence from a Field Experiment\", Review of "
         "Economic Studies 71(2) (2004): 513-534; Oriana Bandiera, Iwan Barankay and Imran Rasul, \"Social "
         "Preferences and the Response to Incentives: Evidence from Personnel Data\", Quarterly Journal of Economics "
         "120(3) (2005): 917-962",
    tag="Shearer, REStud 71(2) (2004); Bandiera, Barankay and Rasul, QJE 120(3) (2005)",
    where="the abstracts",
    read="the abstracts",
    checked="2026-11-19",
    data={"shearer": 0.20, "shearer_structural": 0.217, "shearer_setting": "tree planters in British Columbia, "
                                                                            "randomly assigned to piece rates or "
                                                                            "fixed wages",
          "bbr": 0.50, "bbr_setting": "fruit pickers on a British farm: piece rates against relative incentives"},
)

INCENTIVE_CASES = Table(
    key="incentive_cases",
    cite="Daniel M. G. Raff and Lawrence H. Summers, \"Did Henry Ford Pay Efficiency Wages?\", Journal of Labor "
         "Economics 5(4) (1987): S57-S86; Justin Yifu Lin, \"Rural Reforms and Agricultural Growth in China\", "
         "American Economic Review 82(1) (1992): 34-51; Brian A. Jacob and Steven D. Levitt, \"Rotten Apples\", "
         "Quarterly Journal of Economics 118(3) (2003): 843-877",
    tag="Raff and Summers (1987); Lin (1992); Jacob and Levitt (2003)",
    where="the abstracts",
    read="the abstracts",
    checked="2026-11-19",
    data={"ford": "the five-dollar day of 1914: long queues for Ford jobs, and higher productivity and profits",
          "lin": "decollectivization accounts for about half of farm output growth in 1978-84; higher procurement "
                 "prices also helped",
          "jacob_levitt": 0.04},
    note="Jacob and Levitt: serious cheating by teachers or administrators in at least 4 to 5 percent of Chicago's "
         "elementary classrooms each year.",
)

TENANCY = Table(
    key="tenancy",
    cite="Abhijit V. Banerjee, Paul J. Gertler and Maitreesh Ghatak, \"Empowerment and Efficiency: Tenancy Reform in "
         "West Bengal\", Journal of Political Economy 110(2) (2002): 239-280; Radwan Ali Shaban, \"Testing between "
         "Competing Models of Sharecropping\", Journal of Political Economy 95(5) (1987): 893-920",
    tag="Banerjee, Gertler and Ghatak, JPE 110(2) (2002); Shaban, JPE 95(5) (1987)",
    where="the abstract of Banerjee, Gertler and Ghatak (as posted by Gertler); Shaban's design as later papers using "
          "his data describe it",
    read="the abstract; secondary descriptions of Shaban",
    checked="2026-11-19",
    data={"barga_share_of_growth": 0.28, "barga_year": 1978,
          "barga": "Operation Barga registered sharecroppers, giving them security of tenure and a legal floor on "
                   "their share of the crop",
          "shaban": "the same households' own plots against the plots they sharecropped, in ICRISAT's Indian "
                    "villages: lower output and fewer inputs on the sharecropped plots"},
    note="Banerjee, Gertler and Ghatak cannot separate the reform's direct and indirect effects; Shaban's exact gap "
         "is not quoted here, since only secondary figures for it were found.",
)

CROWDING = Table(
    key="crowding",
    cite="Bruno S. Frey and Felix Oberholzer-Gee, \"The Cost of Price Incentives: An Empirical Analysis of "
         "Motivation Crowding-Out\", American Economic Review 87(4) (1997): 746-755",
    tag="Frey and Oberholzer-Gee, AER 87(4) (1997)",
    where="section III.B, p. 749-750",
    read="the published article (a copy at gwern.net)",
    checked="2026-11-19",
    data={"accept_unpaid": 0.508, "oppose_unpaid": 0.449, "indifferent": 0.043, "accept_paid": 0.246,
          "offers_usd_per_year": (2175, 4350, 6525), "offers_n": (117, 102, 86),
          "what": "a repository for short-lived low- and mid-level radioactive waste, in the respondent's community",
          "where_": "two adjacent communities in central Switzerland designated as potential sites; 305 interviews, "
                    "spring 1993"},
    note="Compensation was offered to every resident of the host community, per person and year; acceptance with "
         "compensation is over all three amounts.",
)

PART14 = (LAZEAR_2000, PIECE_RATES, INCENTIVE_CASES, TENANCY, CROWDING)


COASE_1960 = Table(
    key="coase_1960",
    cite="R. H. Coase, \"The Problem of Social Cost\", Journal of Law and Economics 3 (1960): 1-44",
    tag="Coase, JLE 3 (1960)",
    where="pp. 3 and 6-7: the arithmetical example and the bargain over the third steer",
    read="the article (University of Chicago Law School's copy)",
    checked="2026-11-19",
    data={"steers": (1, 2, 3, 4), "crop_loss_tons": (1, 3, 6, 10), "marginal_loss": (1, 2, 3, 4),
          "crop_price": 1.0, "fence": 9.0,
          "bargain": "with a herd of 3, the farmer would pay up to $3 to cut it to 2, up to $5 for 1, up to $6 to end "
                     "cattle-raising"},
)

CHEUNG_1973 = Table(
    key="cheung_1973",
    cite="Steven N. S. Cheung, \"The Fable of the Bees: An Economic Investigation\", Journal of Law and Economics "
         "16(1) (1973): 11-33",
    tag="Cheung, JLE 16(1) (1973)",
    where="the survey (p. 16) and the decomposition of the rent per hive (pp. 25-27)",
    read="the article",
    checked="2026-11-19",
    data={"survey": "spring 1972: nine beekeepers, about 10,000 spring colonies, in Washington State",
          "state": "about 60 beekeepers with 100 colonies or more; about 90,000 colonies at the peak",
          "crops": {"cherry": "pollination, no surplus honey", "mint": "honey, no pollination needed",
                    "alfalfa": "both"},
          "pollination_season": {"total": 9.65, "money": 9.02, "nectar": 0.64, "n": 13},
          "honey_season": {"total": 8.07, "money": 1.30, "nectar": 6.77, "n": 23},
          "corr_money_nectar": -0.973, "apple": "apple blossoms yield little or no surplus honey"},
    note="Rents per hive per crop season, dollars of 1971; the money fee is negative (an apiary rent paid by the "
         "beekeeper) for some honey crops.",
)

ACID_RAIN = Table(
    key="acid_rain",
    cite="Richard Schmalensee and Robert N. Stavins, \"The SO2 Allowance Trading System: The Ironic History of a "
         "Grand Policy Experiment\", Journal of Economic Perspectives 27(1) (2013): 103-122 (NBER Working Paper 18306)",
    tag="Schmalensee and Stavins, JEP 27(1) (2013)",
    where="the working paper's text and Table 1",
    read="NBER Working Paper 18306",
    checked="2026-11-19",
    data={"utility_so2_mt": {1990: 15.9, 2004: 10.2, 2010: 5.1}, "goal_mt": 8.95, "goal_year": 2007,
          "coal_generation_rise_1990_2004": 0.25, "fine_per_ton": 2000, "savings_vs_command": (0.15, 0.90),
          "benefits_bn": (59, 116), "costs_bn": (0.5, 2.0), "health_share": 0.95,
          "prices": {"2004 auction": 273, "2005 auction": 703, "2005 peak": 1200, "11 July 2008, before": 315,
                     "11 July 2008, after": 115, "2008 auction": 390, "2009 auction": 70, "2012 spot auction": 0.56,
                     "2012 seven-year advance": 0.12},
          "portney": "some studies at enactment predicted benefits about equal to costs (Portney 1990)"},
)

ROADS = Table(
    key="roads",
    cite="Gilles Duranton and Matthew A. Turner, \"The Fundamental Law of Road Congestion: Evidence from US Cities\", "
         "American Economic Review 101(6) (2011): 2616-2652; Jonas Eliasson and others on the Stockholm trial "
         "(Transportation Research Part A 43(3) (2009): 240-250), as summarized",
    tag="Duranton and Turner, AER 101(6) (2011)",
    where="Duranton and Turner: the abstract, Table 3 (pooled OLS, 0.86) and Table 5 (TSLS, panel A); Stockholm: "
          "secondary summaries of Eliasson et al.",
    read="the authors' copy of Duranton and Turner; summaries of the Stockholm evaluation",
    checked="2026-11-19",
    data={"ols": 0.86, "iv": 1.03, "iv_se": 0.11, "iv_range": (0.92, 1.04),
          "instruments": "1835 exploration routes, 1898 railroads, the 1947 interstate plan",
          "stockholm_trial": "January to July 2006", "stockholm_traffic": -0.22, "stockholm_yes_city": 0.53,
          "stockholm_permanent": 2007},
    note="Stockholm: the cordon traffic fall (about a fifth) and the city's 53% vote are from summaries of the "
         "official evaluation, not re-read; the county as a whole voted no.",
)

CURRIE_WALKER_2011 = Table(
    key="currie_walker_2011",
    cite="Janet Currie and Reed Walker, \"Traffic Congestion and Infant Health: Evidence from E-ZPass\", American "
         "Economic Journal: Applied Economics 3(1) (2011): 65-90",
    tag="Currie and Walker, AEJ: Applied 3(1) (2011)",
    where="the abstract",
    read="the abstract and the NBER working paper (15413)",
    checked="2026-11-19",
    data={"prematurity": -0.108, "low_birth_weight": -0.118, "near_km": 2, "control_km": (2, 10)},
)

PART15 = (COASE_1960, CHEUNG_1973, ACID_RAIN, ROADS, CURRIE_WALKER_2011)


# ---------------------------------------------------------------------------------------------------------------
# Part 16: auctions

UK_3G_2000 = Table(
    key="uk_3g_2000",
    cite="Ken Binmore and Paul Klemperer, \"The Biggest Auction Ever: the Sale of the British 3G Telecom Licences\", "
         "Economic Journal 112(478) (2002): C74-C96",
    tag="Binmore and Klemperer, EJ 112(478) (2002)",
    where="the introduction and the account of the auction",
    read="the authors' copy",
    checked="2026-11-19",
    data={"start": "6 March 2000", "end": "27 April 2000", "licences": 5, "bidders": 13, "rounds": 150,
          "revenue_bn_gbp": 22.5, "revenue_bn_usd": 34, "share_of_gnp": 0.025, "vs_media_estimates": (5, 10),
          "incumbents": 4, "winners": "the four incumbents and one entrant (the largest licence was reserved for a "
                                      "newcomer)",
          "vodafone_bn_gbp": 6, "other_incumbents_bn_gbp": 4, "cheapest_over_bn_gbp": 4},
)

EURO_3G_2000 = Table(
    key="euro_3g_2000",
    cite="Paul Klemperer, \"How (Not) to Run Auctions: the European 3G Telecom Auctions\", European Economic Review "
         "46(4-5) (2002): 829-845",
    tag="Klemperer, EER 46 (2002)",
    where="Table 1 (revenue per head) and the accounts of the Dutch and Swiss auctions",
    read="the author's copy",
    checked="2026-11-19",
    data={"per_capita_eur": {"Austria": 100, "Germany": 615, "Italy": 240, "Netherlands": 170, "Switzerland": 20,
                             "United Kingdom": 650},
          "year": 2000,
          "netherlands": {"month": "July 2000", "licences": 5, "incumbents": 5, "revenue_bn_eur_below": 3,
                          "forecast_bn_eur": 10, "entrant": "Versatel, which stopped bidding after a letter from "
                                                            "the incumbent Telfort threatening legal action"},
          "switzerland": {"month": "November-December 2000"}},
)

BAZERMAN_SAMUELSON_1983 = Table(
    key="bazerman_samuelson_1983",
    cite="Max H. Bazerman and William F. Samuelson, \"I Won the Auction But Don't Want the Prize\", Journal of "
         "Conflict Resolution 27(4) (1983): 618-634",
    tag="Bazerman and Samuelson, JCR 27(4) (1983)",
    where="the design and results sections",
    read="the article",
    checked="2026-11-19",
    data={"classes": 12, "auctions": 48, "per_class": 4, "value": 8.00,
          "jars": ("800 pennies", "160 nickels", "200 large paper clips worth 4 cents each",
                   "400 small paper clips worth 2 cents each"),
          "mean_estimate": 5.13, "mean_winning_bid": 10.01, "sd_winning_bid": 5.48, "mean_loss": 2.01,
          "group_sizes": (4, 26), "format": "sealed bids; the highest bidder pays its bid and receives the jar's value"},
)

COLLUSION_SIGNALS = Table(
    key="collusion_signals",
    cite="Peter Cramton and Jesse A. Schwartz, \"Collusive Bidding: Lessons from the FCC Spectrum Auctions\", Journal "
         "of Regulatory Economics 17(3) (2000): 229-252; Paul Klemperer, \"What Really Matters in Auction Design\", "
         "Journal of Economic Perspectives 16(1) (2002): 169-189 (CEPR Discussion Paper 2581)",
    tag="Cramton and Schwartz, JRE 17(3) (2000); Klemperer, JEP 16(1) (2002)",
    where="Cramton and Schwartz's account of the DEF-block auction; Klemperer's footnotes on the German auction",
    read="Klemperer's discussion paper; Cramton and Schwartz as quoted there and in the authors' copy",
    checked="2026-11-19",
    data={"def_auction": "the FCC's DEF-block PCS auction, August 1996 to January 1997",
          "trailing": {"rochester_market": 378, "uswest_bid_round": 59, "uswest_bid": 313378, "mcleod_round": 60,
                       "mcleod_bid": 345000, "uswest_wins_rochester_round": 64},
          "germany_1999": {"licences": 10, "min_raise": 0.10, "mannesmann_1_5": 18.18, "mannesmann_6_10": 20.0,
                           "tmobil_round2_1_5": 20.0, "rounds": 2, "units": "million DM per MHz",
                           "quote": "There were no agreements with Mannesmann. But Mannesmann's first bid was a clear "
                                    "offer.", "quote_source": "Frankfurter Allgemeine Zeitung, 29 October 1999"},
          "us_1997": {"expected_m": 1800, "raised_below_m": 14}},
)

RESERVE_PRICES = Table(
    key="reserve_prices",
    cite="Michael Ostrovsky and Michael Schwarz, \"Reserve Prices in Internet Advertising Auctions: A Field "
         "Experiment\", working paper (24 December 2009)",
    tag="Ostrovsky and Schwarz (2009)",
    where="section 5 and Tables 4-6",
    read="the working paper",
    checked="2026-11-19",
    data={"treatment": 438632, "control": 23016, "depth_change": -0.9125,
          "revenue_naive": 0.1285, "revenue_naive_p": 0.0915,
          "effect": {"all": (0.0271, 4.73), "under 10 searches a day": (-0.0219, -2.36),
                     "10 or more a day": (0.0330, 2.32)},
          "high_volume": {"share_keywords": 0.127, "share_searches": 0.74, "share_revenue": 0.81},
          "old_reserve_cents": 10},
)

TREASURY_FORMAT = Table(
    key="treasury_format",
    cite="Kenneth D. Garbade and Jeffrey F. Ingber, \"The Treasury Auction Process: Objectives, Structure, and Recent "
         "Adaptations\", Federal Reserve Bank of New York, Current Issues in Economics and Finance 11(2) (2005)",
    tag="Garbade and Ingber, NY Fed Current Issues 11(2) (2005)",
    where="\"Auction format\" and Box 2",
    read="the published note",
    checked="2026-11-19",
    data={"bills_first": 1929, "coupons_first": "early 1970s", "experiment": "September 1992: two- and five-year "
          "notes in the single-price format", "all_single_price": "October 1998", "advocates": "Carson (1959), "
          "Friedman (1960, 1963), Smith (1966)", "max_award": 0.35,
          "evidence": "multiple-price auctions cleared at yields significantly above the when-issued market; "
                      "single-price ones could not be told apart from zero, nor from multiple-price ones"},
)

INCENTIVE_AUCTION = Table(
    key="incentive_auction",
    cite="Federal Communications Commission, the broadcast incentive auction (Auction 1000), closing results announced "
         "13 April 2017",
    tag="FCC, Auction 1000 (2017)",
    where="the closing announcement's totals",
    read="the FCC's announcement, as reported",
    checked="2026-11-19",
    data={"forward_bn": 19.8, "reverse_bn": 10.05, "stations": 175, "mhz": 84, "mhz_licensed": 70,
          "mhz_unlicensed": 14, "winning_bidders": 50, "closed": "13 April 2017"},
)

PART16 = (UK_3G_2000, EURO_3G_2000, BAZERMAN_SAMUELSON_1983, COLLUSION_SIGNALS, RESERVE_PRICES, TREASURY_FORMAT,
          INCENTIVE_AUCTION)


# ---------------------------------------------------------------------------------------------------------------
# Part 17: markets by design

ROTH_2012 = Table(
    key="roth_2012",
    cite="Alvin E. Roth, \"The Theory and Practice of Market Design\", Nobel Prize lecture, 8 December 2012, in *Les "
         "Prix Nobel 2012* (Nobel Foundation, 2013); Roth, \"The Evolution of the Labor Market for Medical Interns and "
         "Residents\", Journal of Political Economy 92(6) (1984): 991-1016; Roth, \"A Natural Experiment in the "
         "Organization of Entry-Level Labor Markets\", American Economic Review 81(3) (1991): 415-440",
    tag="Roth, Nobel lecture (2012)",
    where="the lecture's account of the medical market, its table of clearinghouses, and its accounts of New York's "
          "high schools and kidney exchange",
    read="the published lecture (nobelprize.org)",
    checked="2026-11-19",
    data={"interns": {"two_years_before_by": 1940, "schools_withhold_info": 1945, "offer_days_1945": 10,
                      "offer_days_1946": 8, "twelve_hours_too_long_by": 1950},
          "clearinghouses": [("NRMP (US doctors)", True, True), ("Edinburgh, 1969", True, True),
                             ("Cardiff", True, True), ("Birmingham", False, False), ("Edinburgh, 1967", False, False),
                             ("Newcastle", False, False), ("Sheffield", False, False), ("Cambridge", False, True),
                             ("London Hospital", False, True), ("osteopaths before 1994", False, False),
                             ("osteopaths from 1994", True, True), ("pharmacists", True, True)],
          "single_school_exceptions": "Cambridge and the London Hospital each matched one medical school's students "
                                      "to one hospital",
          "nrmp_positions": 25000, "british_positions": "a couple of hundred",
          "women_students": {"1950s": "almost none", "1970s": 0.10, "2012": 0.50},
          "nyc": {"entering": 90000, "unassigned_before": 30000, "unassigned_after": 3000},
          "kidney": {"two_way_rooms": 4, "three_way_rooms": 6, "first_chain_people": 20, "first_chain_transplants": 10,
                     "large_chain_people": 60, "large_chain_transplants": 30}},
)

SCHOOL_EFFECTS = Table(
    key="school_effects",
    cite="Atila Abdulkadiroğlu, Joshua Angrist and Parag Pathak, \"The Elite Illusion: Achievement Effects at Boston "
         "and New York Exam Schools\", NBER Working Paper 17264 (2011), published in Econometrica 82(1) (2014): "
         "137-196; Atila Abdulkadiroğlu, Joshua Angrist, Yusuke Narita and Parag Pathak, \"Research Design Meets "
         "Market Design: Using Centralized Assignment for Impact Evaluation\", IZA Discussion Paper 10429 (2016), "
         "published in Econometrica 85(5) (2017): 1373-1432",
    tag="Abdulkadiroğlu, Angrist and Pathak (2014); Abdulkadiroğlu, Angrist, Narita and Pathak (2017)",
    where="the exam schools: the working paper's Table 4 (Boston reduced forms, all schools, nonparametric) and the "
          "introduction; Denver: Table 6 of the discussion paper",
    read="the working papers",
    checked="2026-11-19",
    data={"exam_offer": {"math": (-0.035, 0.027), "english": (0.022, 0.028)},
          "newton_waltham": {"newton": 412000, "waltham": 316000, "proficient_newton": 0.92,
                             "proficient_waltham": 0.78},
          "denver": {"first_stage": (0.420, 0.024), "math": (0.415, 0.052), "reading": (0.166, 0.053),
                     "writing": (0.274, 0.058), "math_no_score_controls": (0.231, 0.030),
                     "math_ols_no_controls": (0.230, 0.010), "always_takers": 0.44, "never_takers_below": 0.20}},
)

PART17 = (ROTH_2012, SCHOOL_EFFECTS)


# ---------------------------------------------------------------------------------------------------------------
# Part 18: social choice and welfare

VSL = Table(
    key="vsl",
    cite="U.S. Department of Transportation, \"Departmental Guidance on Valuation of a Statistical Life in Economic "
         "Analysis\" (table of values by base year); U.S. Environmental Protection Agency, \"Mortality Risk "
         "Valuation\" and its Guidelines for Preparing Economic Analyses (the $7.4 million central estimate, 2006 "
         "dollars); Orley Ashenfelter and Michael Greenstone, \"Using Mandated Speed Limits to Measure the Value of a "
         "Statistical Life\", Journal of Political Economy 112(S1) (2004): S226-S267; Thomas J. Kniesner, W. Kip "
         "Viscusi, Christopher Woock and James P. Ziliak, \"The Value of a Statistical Life: Evidence from Panel "
         "Data\", Review of Economics and Statistics 94(1) (2012): 74-87",
    tag="DOT guidance; EPA; Ashenfelter and Greenstone, JPE 112(S1) (2004); Kniesner et al., REStat 94(1) (2012)",
    where="DOT: the table of VSL by base year; EPA: the mortality risk valuation page (a Weibull fit to 26 studies, "
          "mean $7.4m, s.d. $4.7m, 2006 dollars); Ashenfelter and Greenstone: the abstract; Kniesner et al.: the "
          "abstract",
    read="the agencies' pages and the articles' abstracts, as reported",
    checked="2026-11-19",
    data={"dot": {2022: 12.5, 2023: 13.2, 2024: 13.7, 2025: 14.2}, "dot_sensitivity_2023": (7.9, 18.5),
          "epa_2006": 7.4, "epa_sd_2006": 4.7, "epa_studies": 26,
          "ag_1997": 1.54, "ag_se_share": 1 / 3, "ag_speed": "65 mph limits from 1987: speeds up about 2.5 mph (4%), "
                                                             "fatality rates up about 35%",
          "ag_hours_per_life": 125000,
          "kniesner_range": (4.0, 10.0)},
)

DUVERGER = Table(
    key="duverger",
    cite="Maurice Duverger, *Les partis politiques* (1951; English edition 1954); William H. Riker, \"The Two-Party "
         "System and Duverger's Law: An Essay on the History of Political Science\", American Political Science "
         "Review 76(4) (1982): 753-766",
    tag="Duverger (1951); Riker, APSR 76(4) (1982)",
    where="the law as stated, and Riker's history of it",
    read="Riker's essay",
    checked="2026-11-19",
    data={"law": "plurality rule in single-member districts tends to produce a two-party system",
          "us_presidents_since": 1853, "exceptions": ("Canada", "India", "the United Kingdom")},
)

PART18 = (VSL, DUVERGER)


MALTHUS_1798 = Table(
    key="malthus_1798",
    cite="[T. R. Malthus], *An Essay on the Principle of Population, as it affects the future improvement of society. "
         "With remarks on the speculations of Mr. Godwin, M. Condorcet, and other writers* (London: J. Johnson, 1798), "
         "first edition, published anonymously; preface dated 7 June 1798",
    tag="Malthus, An Essay on the Principle of Population (1798), ch. 1",
    where="chapter 1, pp. 13-14 of the first edition",
    read="a scan of the first edition (Internet Archive, essayonprincipl00malt), the passage read on the page",
    checked="2026-11-19",
    data={"powers": "the power of population is indefinitely greater than the power in the earth to produce "
                    "subsistence for man",
          "ratios": "Population, when unchecked, increases in a geometrical ratio. Subsistence increases only in an "
                    "arithmetical ratio.",
          "preface_dated": "7 June 1798"},
)

PART19 = (MALTHUS_1798,)


# ---------------------------------------------------------------------------
# Part 21
# ---------------------------------------------------------------------------
NORDHAUS_LIGHT = Table(
    key="nordhaus_light",
    cite="William D. Nordhaus, \"Do Real-Output and Real-Wage Measures Capture Reality? The History of Lighting "
         "Suggests Not\", in T. F. Bresnahan and R. J. Gordon (eds), The Economics of New Goods (NBER Studies in "
         "Income and Wealth 58, University of Chicago Press, 1996): 27-70",
    tag="Nordhaus (1996), table 1.6",
    where="table 1.6, Labor Price of Light (hours of work per 1,000 lumen-hours); the bias of traditional indexes in "
          "section 1.5",
    read="the NBER chapter PDF (c6064), the table read on the page image",
    checked="2026-11-20",
    data={"rows": (
              # (device, technology, date for the chart, date as printed, hours of work per 1,000 lumen-hours)
              ("open fire", "wood", None, "from earliest time", 58.0),
              ("Neolithic lamp", "animal or vegetable fat", None, "38,000-9000 B.C.", 50.0),
              ("Babylonian lamp", "sesame oil", -1750, "1750 B.C.", 41.50),
              ("candle", "tallow", 1800, "1800", 5.37),
              ("candle", "sperm", 1800, "1800", 12.21),
              ("candle", "tallow", 1830, "1830", 3.00),
              ("candle", "sperm", 1830, "1830", 6.91),
              ("lamp", "whale oil", 1830, "1815-45", 4.90),
              ("town gas", "early lamp", 1827, "1827", 7.398),
              ("town gas", "Silliman's experiment", 1855, "1855", 2.978),
              ("town gas", "early lamp", 1880, "1875-85", 0.326),
              ("town gas", "Welsbach mantle", 1890, "1885-95", 0.083),
              ("town gas", "Welsbach mantle", 1916, "1916", 0.012),
              ("kerosene lamp", "Silliman's experiment", 1855, "1855", 0.2306),
              ("kerosene lamp", "19th century", 1880, "1875-85", 0.2253),
              ("kerosene lamp", "Coleman lantern", 1993, "1993", 0.0098),
              ("electric lamp", "Edison carbon lamp", 1883, "1883", 0.750239),
              ("electric lamp", "carbon filament", 1900, "1900", 0.220431),
              ("electric lamp", "carbon filament", 1910, "1910", 0.092096),
              ("electric lamp", "filament lamp", 1920, "1920", 0.013538),
              ("electric lamp", "filament lamp", 1930, "1930", 0.010396),
              ("electric lamp", "filament lamp", 1940, "1940", 0.005490),
              ("electric lamp", "filament lamp", 1950, "1950", 0.001883),
              ("electric lamp", "filament lamp", 1960, "1960", 0.001016),
              ("electric lamp", "filament lamp", 1970, "1970", 0.000551),
              ("electric lamp", "filament lamp", 1980, "1980", 0.000678),
              ("electric lamp", "filament lamp", 1990, "1990", 0.000605),
              ("electric lamp", "compact fluorescent", 1992, "1992", 0.000119)),
          "traditional_overstatement": "a factor of between nine hundred and sixteen hundred relative to the true price "
                                       "(1800-1992)",
          "traditional_bias": 0.036},
)

BLOOM_2020 = Table(
    key="bloom_2020",
    cite="Nicholas Bloom, Charles I. Jones, John Van Reenen and Michael Webb, \"Are Ideas Getting Harder to Find?\", "
         "American Economic Review 110(4) (2020): 1104-1144",
    tag="Bloom, Jones, Van Reenen and Webb (2020)",
    where="section on the aggregate economy (figure 2) and the conclusion (table 6); NBER working paper 23782",
    read="NBER working paper 23782 (2017, revised), the text read",
    checked="2026-11-20",
    data={"effort_factor": 23, "effort_growth": 0.043, "productivity_factor": 41, "productivity_growth": -0.051,
          "moore_factor": 18, "aggregate_decline": 0.053, "half_life": 13},
)

PART21 = (NORDHAUS_LIGHT, BLOOM_2020)

# Part 22: what households do with windfalls, transcribed from the abstracts and summaries named in each row
MPC_STUDIES = Table(
    key="mpc_studies",
    cite="Johnson, Parker and Souleles, AER 96(5) (2006): 1589-1610; Parker, Souleles, Johnson and McClelland, AER "
         "103(6) (2013): 2530-2553; Parker, Schild, Erhard and Johnson, NBER WP 29648 (2022); Hsieh, AER 93(1) (2003): "
         "397-405; Kueng, QJE 133(4) (2018): 1693-1751; Fagereng, Holm and Natvik, AEJ: Macro 13(4) (2021): 1-54; "
         "Jappelli and Pistaferri, AEJ: Macro 6(4) (2014): 107-136; Fuster, Kaplan and Zafar, REStud 88(4) (2021): "
         "1760-1795; Kaplan, Violante and Weidner, BPEA Spring 2014: 77-138; Ganong and Noel, AER 109(7) (2019): "
         "2383-2424 (NBER WP 25417)",
    tag="the studies' abstracts",
    where="each paper's abstract (or, where noted, its NBER summary or working paper)",
    read="abstracts and NBER summaries",
    checked="2026-11-20",
    data={
        "jps": {"episode": "2001 tax rebates, $300 or $600, to about two-thirds of households",
                "design": "mailing week set by the second-to-last digit of the Social Security number, late July to "
                          "late September",
                "lo": 0.20, "hi": 0.40, "measure": "nondurables, the quarter received",
                "cumulative": "about two-thirds over that quarter and the next (nondurables)",
                "who": "largest for households with low liquid wealth or low income"},
        "parker2013": {"episode": "2008 economic stimulus payments", "lo": 0.12, "hi": 0.30,
                       "measure": "nondurables, the quarter received", "total_lo": 0.50, "total_hi": 0.90,
                       "total": "including durables, mainly vehicles"},
        "parker2022": {"episode": "2020 economic impact payments", "value": 0.10, "se": 0.034,
                       "measure": "nondurable goods and services, the three months of arrival",
                       "low_liquid": 0.217, "low_liquid_se": 0.064},
        "hsieh": {"episode": "the Alaska Permanent Fund dividend", "finding": "no response to the large, predictable "
                  "dividend in survey data; a response to income-tax refunds"},
        "kueng": {"episode": "the Alaska Permanent Fund dividend, account data", "value": 0.25,
                  "measure": "nondurables and services, within a quarter",
                  "high_income": "above 0.5 for high-income households with substantial liquid assets"},
        "fhn": {"episode": "Norwegian lottery prizes", "small_low_liquid": 1.0, "large_high_liquid": "slightly "
                "below one-half", "measure": "spending within the year of winning; back to normal within five years",
                "small_prize": "around US$1,500"},
        "jp": {"episode": "Italy's 2010 Survey of Household Income and Wealth", "value": 0.48,
               "measure": "reported share of a transitory income gain consumed", "who": "higher at low cash-on-hand"},
        "fkz": {"episode": "a US survey of hypothetical gains, losses, news and loans", "findings": [
            "many would spend nothing of a gain, others a large share", "cuts after losses are larger and more common",
            "very few would spend on news of a future gain", "almost no one takes a one-year interest-free loan"]},
        "kvw": {"htm_share": "about one-third of US households", "wealthy_of_htm": "over two-thirds"},
        "ganong_noel": {"onset": 0.06, "exhaustion": 0.12, "measure": "monthly nondurable spending",
                        "source": "NBER WP 25417"},
    },
)

PART22 = (MPC_STUDIES,)

HANKE_KRUS_2012 = Table(
    key="hanke_krus_2012",
    cite="Steve H. Hanke and Nicholas Krus, \"World Hyperinflations\", Cato Working Paper no. 8 (15 August 2012), "
         "the Hanke-Krus Hyperinflation Table; published in R. Parker and R. Whaples (eds.), The Routledge Handbook of "
         "Major Events in Economic History (2013)",
    tag="Hanke and Krus (2012), the hyperinflation table",
    where="the table (peak month and the highest monthly inflation rate); Hungary's doubling time from Hanke's "
          "commentary",
    read="the table as reproduced by Cato and summarized by the American Numismatic Society",
    checked="2026-11-20",
    data={
        "hungary": {"country": "Hungary", "month": "July 1946", "monthly_pct": 4.19e16, "doubling_hours": 15.0},
        "zimbabwe": {"country": "Zimbabwe", "month": "November 2008", "monthly_pct": 7.96e10},
        "yugoslavia": {"country": "Yugoslavia", "month": "January 1994", "monthly_pct": 3.13e8},
        "germany": {"country": "Germany", "month": "October 1923", "monthly_pct": 2.95e4},
        "cagan_germany": {"note": "Cagan (1956): German prices rose 322% a month on average, August 1922 to November "
                                  "1923 (a ratio of about 1.02e10); his estimates imply revenue-maximizing inflation "
                                  "of about 20% a month",
                          "average_pct": 322.0, "revenue_max_pct": 20.0},
    },
)
PART25 = (HANKE_KRUS_2012,)

SVB_2023 = Table(
    key="svb_2023",
    cite="M. S. Barr, testimony before the Senate Committee on Banking, Housing, and Urban Affairs, 28 March 2023; "
         "Board of Governors of the Federal Reserve System, Review of the Federal Reserve's Supervision and Regulation "
         "of Silicon Valley Bank (April 2023), \"Evolution of Silicon Valley Bank\"",
    tag="Barr (2023); the Federal Reserve's review (April 2023)",
    where="the testimony (the withdrawals of 9 March and the requests for 10 March); the review (uninsured share, "
          "capital ratio); the held-to-maturity portfolio and its fair value from the bank's year-end 2022 accounts as "
          "reported by the ICAEW",
    read="testimony, review and reporting",
    checked="2026-11-20",
    data={
        "withdrawn_mar9": 42e9, "requested_mar10": 100e9, "uninsured_share": 0.94, "cet1": 0.12,
        "htm_book": 91e9, "htm_gap": 15e9,
    },
)
STRESS_2022 = Table(
    key="stress_2022",
    cite="Board of Governors of the Federal Reserve System, 2022 Stress Test Scenarios (February 2022): the severely "
         "adverse scenario",
    tag="the Federal Reserve's 2022 stress test scenarios",
    where="the scenario's description of interest rates and unemployment",
    read="the scenario document as quoted",
    checked="2026-11-20",
    data={
        "ten_year_trough": 0.75, "ten_year_trough_when": "2022Q1", "ten_year_end": 1.5, "short_rates": "near zero "
        "throughout", "unemployment_peak": 10.0, "unemployment_peak_when": "2023Q3",
        "path": ((2021.75, 1.5), (2022.0, 0.75), (2022.25, 0.75), (2022.5, 0.75), (2022.75, 0.85), (2023.0, 0.95),
                 (2023.25, 1.05), (2023.5, 1.15), (2023.75, 1.25), (2024.0, 1.35), (2024.75, 1.5)),
    },
)
PART26 = (SVB_2023, STRESS_2022)


# ---------------------------------------------------------------------------
# Part 35
# ---------------------------------------------------------------------------
SAMUELSON_ULAM = Table(
    key="samuelson_ulam",
    cite="P. A. Samuelson, \"The Way of an Economist\", in P. A. Samuelson (ed.), International Economic Relations: "
         "Proceedings of the Third Congress of the International Economic Association (Macmillan, 1969), pp. 1-11",
    tag="Samuelson (1969), as widely quoted",
    where="the anecdote of Stanislaw Ulam's challenge and Samuelson's answer, comparative advantage",
    read="the passage as reproduced in several secondary sources (Reason, FEE, Econlib), which agree on the wording; "
         "the 1969 volume itself was not read",
    checked="2026-11-20",
    data={"answer": "Ricardo's theory of comparative advantage",
          "quote": "That it is logically true need not be argued before a mathematician; that it is not trivial is "
                   "attested by the thousands of important and intelligent men who have never been able to grasp the "
                   "doctrine for themselves or to believe it after it was explained to them."},
    note="the wording of Ulam's question and the date it was asked differ between accounts; the film says 'as "
         "Samuelson told it'",
)
RICARDO_1817 = Table(
    key="ricardo_1817",
    cite="D. Ricardo, On the Principles of Political Economy and Taxation (John Murray, 1817), chapter 7, \"On Foreign "
         "Trade\"",
    tag="Ricardo (1817), ch. 7",
    where="the four numbers: the labour of men for a year to make a quantity of cloth and of wine",
    read="the standard text of chapter 7",
    checked="2026-11-20",
    data={"England": {"cloth": 100, "wine": 120}, "Portugal": {"cloth": 90, "wine": 80}},
)
BERNHOFEN_BROWN_2004 = Table(
    key="bernhofen_brown_2004",
    cite="D. M. Bernhofen and J. C. Brown, \"A Direct Test of the Theory of Comparative Advantage: The Case of Japan\", "
         "Journal of Political Economy 112(1): 48-67 (2004)",
    tag="Bernhofen and Brown, JPE 112(1) (2004)",
    where="table 1 (the composition of Japanese trade, 1868-75, percent of imports or exports) and table 2 (the "
          "inner product of autarky prices of 1851-53 and each year's net exports, millions of ryo)",
    read="the published article (the authors' posted copy)",
    checked="2026-11-20",
    data={
        "exports": {"silk": 35.9, "silkworm eggs": 15.7, "tea": 28.2, "other foods": 8.2, "other manufactures": 4.3,
                    "other raw materials": 2.9, "vegetable wax and cotton": 2.7, "fuel": 1.9, "textiles": 0.2},
        "imports": {"woolens": 19.2, "cotton cloth": 18.4, "cotton yarn": 15.1, "miscellaneous manufactures": 11.2,
                    "rice": 10.8, "sugar": 9.9, "other foods": 4.2, "other raw materials": 3.1,
                    "weapons and ammunition": 2.7, "vegetable wax and cotton": 2.2, "other textiles": 1.8,
                    "machinery and instruments": 1.4},
        "years": (1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875),
        "imports_observed": (-2.24, -4.12, -8.44, -7.00, -5.75, -5.88, -7.15, -7.98),
        "woolens": (-0.98, -0.82, -1.29, -1.56, -2.16, -2.50, -1.56, -2.33),
        "imports_approx": (-1.10, -0.95, -0.70, -0.85, -1.51, -2.08, -1.60, -2.65),
        "exports_observed": (4.07, 3.40, 4.04, 5.16, 4.99, 4.08, 5.08, 4.80),
        "exports_approx": (0.09, 0.03, 0.07, 0.07, 0.15, 0.07, 0.11, 0.10),
        "total": (-0.18, -2.47, -6.31, -4.17, -4.28, -6.31, -5.11, -8.06),
        "autarky": "1851-53", "opened": 1859,
    },
    note="figure 4's price changes (exports' prices rising, in some cases almost doubling; imports' falling) are "
         "described in words, since the figure's points were not transcribed",
)
BERNHOFEN_BROWN_2005 = Table(
    key="bernhofen_brown_2005",
    cite="D. M. Bernhofen and J. C. Brown, \"An Empirical Assessment of the Comparative Advantage Gains from Trade: "
         "Evidence from Japan\", American Economic Review 95(1): 208-225 (2005)",
    tag="Bernhofen and Brown, AER 95(1) (2005)",
    where="the abstract: an upper bound on the gains of about 8 to 9 percent of GDP",
    read="the abstract and the authors' working-paper summary",
    checked="2026-11-20",
    data={"upper_bound_lo": 8.0, "upper_bound_hi": 9.0},
)
IRWIN_2005 = Table(
    key="irwin_2005",
    cite="D. A. Irwin, \"The Welfare Cost of Autarky: Evidence from the Jeffersonian Trade Embargo, 1807-09\", Review "
         "of International Economics 13(4): 631-645 (2005)",
    tag="Irwin, Review of International Economics 13(4) (2005)",
    where="the abstract: about 5 percent of 1807 GNP (the 2001 working paper had 8 percent); trade about 13 percent of "
          "GNP",
    read="the abstract and the NBER Reporter summary (2006)",
    checked="2026-11-20",
    data={"cost": 5.0, "cost_wp": 8.0, "trade_share": 13.0, "from": "December 1807", "to": "March 1809"},
)
LEONTIEF_1953 = Table(
    key="leontief_1953",
    cite="W. Leontief, \"Domestic Production and Foreign Trade: The American Capital Position Re-examined\", "
         "Proceedings of the American Philosophical Society 97(4): 332-349 (1953)",
    tag="Leontief (1953)",
    where="the table of capital and labour needed per million dollars of US exports and of competitive import "
          "replacements, 1947",
    read="the table as reproduced in textbooks and in the secondary literature (several copies agree)",
    checked="2026-11-20",
    data={"exports": {"capital": 2550780, "labour": 182.313}, "imports": {"capital": 3091339, "labour": 170.004}},
)
TREFLER_1995 = Table(
    key="trefler_1995",
    cite="D. Trefler, \"The Case of the Missing Trade and Other Mysteries\", American Economic Review 85(5): "
         "1029-1046 (1995)",
    tag="Trefler, AER 85(5) (1995)",
    where="the abstract and table 1 as reported in the literature: the sign test (about 0.50) and the variance of "
          "measured relative to predicted factor content (0.032)",
    read="the abstract; the statistics as reported by later papers; this film recomputes both from the data",
    checked="2026-11-20",
    data={"sign_test": 0.50, "variance_ratio": 0.032, "countries": 33, "factors": 9, "year": 1983},
)
IRWIN_SMOOT_HAWLEY = Table(
    key="irwin_smoot_hawley",
    cite="D. A. Irwin, \"The Smoot-Hawley Tariff: A Quantitative Assessment\", Review of Economics and Statistics "
         "80(2): 326-334 (1998), and Peddling Protectionism: Smoot-Hawley and the Great Depression (Princeton, 2011)",
    tag="Irwin (1998, 2011)",
    where="the average tariff on dutiable imports: about 40 percent in 1929, 59 percent in 1932, 14 percent in 1948; "
          "much of the rise came from deflation, since many duties were specific (cents per unit)",
    read="Irwin's NBER chapter and working paper as summarized; the book's decomposition was not read",
    checked="2026-11-20",
    data={"dutiable": {1929: 40.0, 1932: 59.0, 1948: 14.0}},
)
ACR_2012 = Table(
    key="acr_2012",
    cite="C. Arkolakis, A. Costinot and A. Rodriguez-Clare, \"New Trade Models, Same Old Gains?\", American Economic "
         "Review 102(1): 94-130 (2012)",
    tag="Arkolakis, Costinot and Rodriguez-Clare, AER 102(1) (2012)",
    where="section on the welfare formula's application to the United States: a domestic share of about 0.93 and a "
          "trade elasticity between -5 and -10 give gains of 0.7 to 1.4 percent",
    read="the published article as summarized",
    checked="2026-11-20",
    data={"lambda": 0.93, "eps": (-5.0, -10.0), "gains": (0.7, 1.4)},
)
GOLDBERG_MAGGI_1999 = Table(
    key="goldberg_maggi_1999",
    cite="P. K. Goldberg and G. Maggi, \"Protection for Sale: An Empirical Investigation\", American Economic Review "
         "89(5): 1135-1155 (1999)",
    tag="Goldberg and Maggi, AER 89(5) (1999)",
    where="the abstract: US protection in 1983 fits the model, and the government weighs welfare many times more than "
          "contributions (50 to 88 times in the NBER working paper's estimates)",
    read="the abstracts of the article and of NBER working paper 5942",
    checked="2026-11-20",
    data={"year": 1983, "weight_lo": 50, "weight_hi": 88},
)
COSTINOT_DONALDSON_2012 = Table(
    key="costinot_donaldson_2012",
    cite="A. Costinot and D. Donaldson, \"Ricardo's Theory of Comparative Advantage: Old Idea, New Evidence\", "
         "American Economic Review: Papers and Proceedings 102(3): 453-458 (2012)",
    tag="Costinot and Donaldson, AER P&P 102(3) (2012)",
    where="the abstract and the main regression: 17 crops, 1.6 million parcels, 55 countries; log output on log "
          "predicted output, slope 0.21",
    read="the NBER working paper (w17969) as summarized",
    checked="2026-11-20",
    data={"crops": 17, "parcels": 1.6e6, "countries": 55, "slope": 0.21},
)
TAA = Table(
    key="taa",
    cite="Trade Expansion Act of 1962, Public Law 87-794 (11 October 1962); Congressional Research Service, R41922; "
         "B. Hyman, \"Can Displaced Labor Be Retrained? Evidence from Quasi-Random Assignment to Trade Adjustment "
         "Assistance\" (working paper, 2018)",
    tag="PL 87-794 (1962); CRS R41922; Hyman (2018)",
    where="the Act's purposes; the CRS history of TAA; Hyman's abstract: about $50,000 more cumulative earnings ten "
          "years out for approved workers, from about 300,000 workers in Census data",
    read="the statute's title page, the CRS report and the working paper's abstract",
    checked="2026-11-20",
    data={"enacted": "11 October 1962", "law": "PL 87-794", "hyman_gain": 50000, "hyman_workers": 300000,
          "hyman_years": 10},
)
PART35 = (SAMUELSON_ULAM, RICARDO_1817, BERNHOFEN_BROWN_2004, BERNHOFEN_BROWN_2005, IRWIN_2005, LEONTIEF_1953,
          TREFLER_1995, IRWIN_SMOOT_HAWLEY, ACR_2012, GOLDBERG_MAGGI_1999, COSTINOT_DONALDSON_2012, TAA)


# ---------------------------------------------------------------------------
# Part 36
# ---------------------------------------------------------------------------
IDEAL_X = Table(
    key="ideal_x",
    cite="Port Authority of New York and New Jersey; J.-P. Rodrigue, The Geography of Transport Systems, \"The First "
         "Containership, Ideal-X, 1956\"; M. Levinson, The Box (Princeton, 2006)",
    tag="Rodrigue, \\emph{The Geography of Transport Systems}; \\ Levinson, \\emph{The Box} (2006)",
    where="the voyage of 26 April 1956 from Port Newark to Houston with 58 trailers; McLean's estimate of loading "
          "costs, $5.83 a ton by hand against under 16 cents in containers",
    read="the cited web accounts, which agree; The Box was not read",
    checked="2026-11-20",
    data={"date": "26 April 1956", "trailers": 58, "hand": 5.83, "box": 0.16},
)
BERNARD_JENSEN_1995 = Table(
    key="bernard_jensen_1995",
    cite="A. B. Bernard and J. B. Jensen, \"Exporters, Jobs, and Wages in U.S. Manufacturing: 1976-1987\", Brookings "
         "Papers on Economic Activity: Microeconomics (1995), 67-119",
    tag="Bernard and Jensen, \\emph{BPEA Micro} (1995)",
    where="the abstract: exporting plants were 10.4% of manufacturing plants in 1976 and 14.6% in 1987, with over half "
          "of shipments",
    read="the paper as summarized in its abstract",
    checked="2026-11-20",
    data={"share_1976": 10.4, "share_1987": 14.6, "shipments": 50},
)
ADH_2013 = Table(
    key="adh_2013",
    cite="D. H. Autor, D. Dorn and G. H. Hanson, \"The China Syndrome: Local Labor Market Effects of Import Competition "
         "in the United States\", American Economic Review 103(6): 2121-2168 (2013); NBER Working Paper 18054",
    tag="Autor, \\ Dorn and Hanson, \\emph{AER} 103(6) (2013)",
    where="the abstract (one-quarter of the decline in manufacturing employment), table 3, column 6 (-0.596 per $1,000 "
          "per worker over a decade, 2SLS; OLS -0.171), and the text on exposure ($1,140 in 1990-2000, $1,839 in "
          "2000-07; implied falls of 0.68 and 1.10 points against actual falls of 2.07 and 2.00)",
    read="NBER Working Paper 18054 (2012)",
    checked="2026-11-20",
    data={"beta": -0.596, "ols": -0.171, "ols_lag": -0.273, "exposure_90s": 1140, "exposure_00s": 1839,
          "implied_90s": 0.68, "implied_00s": 1.10, "actual_90s": 2.07, "actual_00s": 2.00, "share": 0.25},
)
FAJGELBAUM_2020 = Table(
    key="fajgelbaum_2020",
    cite="P. D. Fajgelbaum, P. K. Goldberg, P. J. Kennedy and A. K. Khandelwal, \"The Return to Protectionism\", "
         "Quarterly Journal of Economics 135(1): 1-55 (2020); M. Amiti, S. J. Redding and D. E. Weinstein, \"The "
         "Impact of the 2018 Tariffs on Prices and Welfare\", Journal of Economic Perspectives 33(4): 187-210 (2019)",
    tag="Fajgelbaum et al., \\emph{QJE} 135(1) (2020); \\ Amiti, \\ Redding and Weinstein, \\emph{JEP} 33(4) (2019)",
    where="the abstracts: import prices did not fall (complete pass-through); losses to buyers of imports $51 billion "
          "(0.27% of GDP); the aggregate real income loss net of revenue and producer gains $7.2 billion (0.04%)",
    read="the published abstracts",
    checked="2026-11-20",
    data={"buyers_loss": 51e9, "buyers_share": 0.27, "net_loss": 7.2e9, "net_share": 0.04, "passthrough": 1.0},
)
BOEHM_2023 = Table(
    key="boehm_2023",
    cite="C. E. Boehm, A. A. Levchenko and N. Pandalai-Nayar, \"The Long and Short (Run) of Trade Elasticities\", "
         "American Economic Review 113(4): 861-905 (2023)",
    tag="Boehm, \\ Levchenko and Pandalai-Nayar, \\emph{AER} 113(4) (2023)",
    where="the abstract: -0.76 in the short run, about -2 in the long run, seven to ten years to converge",
    read="the published abstract and the NBER working paper's",
    checked="2026-11-20",
    data={"short": 0.76, "long": 2.0, "years": (7, 10)},
)
KRUGMAN_1995 = Table(
    key="krugman_1995",
    cite="P. R. Krugman, \"Growing World Trade: Causes and Consequences\", Brookings Papers on Economic Activity 1995(1): "
         "327-377; P. R. Krugman, \"Trade and Wages, Reconsidered\", Brookings Papers on Economic Activity 2008(1)",
    tag="Krugman, \\emph{BPEA} (1995, 2008)",
    where="the 1995 estimate that trade with developing countries raised the skilled-unskilled wage ratio by about 3 "
          "percentage points, as tabulated in the 2008 paper beside Lawrence (3), Cline (7) and Borjas, Freeman and "
          "Katz (1.4)",
    read="the 2008 paper's table as reported; the 1995 paper's opening",
    checked="2026-11-20",
    data={"krugman": 3, "lawrence": 3, "cline": 7, "bfk": 1.4},
)
XING_DETERT_2010 = Table(
    key="xing_detert_2010",
    cite="Y. Xing and N. Detert, \"How the iPhone Widens the United States Trade Deficit with the People's Republic of "
         "China\", ADBI Working Paper 257 (December 2010)",
    tag="Xing and Detert, \\ ADBI WP 257 (2010)",
    where="the abstract and summaries: the iPhone added $1.9 billion to the 2009 US deficit with China; China's value "
          "added was $6.50 per iPhone 3G; in value added, the trade would show a US surplus of $48 million; the cost "
          "breakdown they use (iSuppli's teardown, 2009): components $172.46 and manufacturing $6.50, $178.96 in all",
    read="the abstract and the authors' later summaries",
    checked="2026-11-20",
    data={"deficit": 1.9e9, "china_va": 6.50, "va_surplus": 48e6, "year": 2009, "total": 178.96, "parts": 172.46},
)
MCCALLUM_1995 = Table(
    key="mccallum_1995",
    cite="J. McCallum, \"National Borders Matter: Canada-U.S. Regional Trade Patterns\", American Economic Review "
         "85(3): 615-623 (1995); J. E. Anderson and E. van Wincoop, \"Gravity with Gravitas\", American Economic "
         "Review 93(1): 170-192 (2003)",
    tag="McCallum, \\emph{AER} 85(3) (1995); \\ Anderson and van Wincoop, \\emph{AER} 93(1) (2003)",
    where="McCallum: trade between Canadian provinces about 22 times trade with US states of the same size and distance "
          "(1988); Anderson and van Wincoop: a much smaller border effect once multilateral resistance is included",
    read="the papers as summarized",
    checked="2026-11-20",
    data={"factor": 22, "year": 1988},
)
PART36 = (IDEAL_X, BERNARD_JENSEN_1995, ADH_2013, FAJGELBAUM_2020, BOEHM_2023, KRUGMAN_1995, XING_DETERT_2010,
          MCCALLUM_1995)


# ---------------------------------------------------------------------------
# Part 37: Cities and Regions
SAIZ_2010 = Table(
    key="saiz_2010",
    cite="A. Saiz, \"The Geographic Determinants of Housing Supply\", Quarterly Journal of Economics 125(3): "
         "1253-1296 (2010)",
    tag="Saiz, \\ \\emph{QJE} 125(3) (2010)",
    where="Table VI, supply elasticities for metropolitan areas with population over 500,000 (pp. 1283-1284); the "
          "population-weighted (1.75) and unweighted (2.5) averages in the introduction and the conclusion, and the "
          "common elasticity (1.54) of Table III, column (1)",
    read="the published article (pdf)",
    checked="2026-11-20",
    data={"weighted": 1.75, "unweighted": 2.5, "common": 1.54,
          "metros": {"Miami": 0.60, "Los Angeles": 0.63, "Fort Lauderdale": 0.65, "San Francisco": 0.66,
                     "San Diego": 0.67, "Oakland": 0.70, "Salt Lake City": 0.75, "New York": 0.76, "San Jose": 0.76,
                     "Chicago": 0.81, "Boston": 0.86, "Seattle": 0.88, "Riverside": 0.94, "Tampa": 1.00,
                     "Cleveland": 1.02, "Portland": 1.07, "Orlando": 1.12, "Pittsburgh": 1.20, "Baltimore": 1.23,
                     "Detroit": 1.24, "Las Vegas": 1.39, "Minneapolis": 1.45, "Denver": 1.53, "Washington": 1.61,
                     "Phoenix": 1.61, "Philadelphia": 1.65, "Dallas": 2.18, "Nashville": 2.24, "Houston": 2.30,
                     "St. Louis": 2.36, "Atlanta": 2.55, "Columbus": 2.71, "San Antonio": 2.98, "Austin": 3.00,
                     "Charlotte": 3.09, "Kansas City": 3.19, "Oklahoma City": 3.29, "Indianapolis": 4.00,
                     "Fort Wayne": 5.36, "Wichita": 5.45}},
    note="Table VI ranks 95 metropolitan areas; the 40 here include the twenty with Case-Shiller indices",
)
CDGR_2010 = Table(
    key="cdgr_2010",
    cite="P.-P. Combes, G. Duranton, L. Gobillon and S. Roux, \"Estimating Agglomeration Economies with History, "
         "Geology, and Worker Effects\", in E. L. Glaeser (ed.), Agglomeration Economics, University of Chicago Press "
         "(2010), pp. 15-66",
    tag="Combes, \\ Duranton, \\ Gobillon and Roux (2010)",
    where="section 1.1: the raw elasticity of mean wages to density, the estimates controlling for the quantity and "
          "the quality of labour, and the preferred estimate; 306 French employment areas, 1976-1996",
    read="the NBER chapter (c7978, pdf)",
    checked="2026-11-20",
    data={"raw": 0.05, "quantity": 0.04, "quality": 0.033, "both": 0.027, "preferred": 0.02, "tfp_raw": 0.04,
          "typical_lo": 0.04, "typical_hi": 0.10},
)
ARSW_2015 = Table(
    key="arsw_2015",
    cite="G. M. Ahlfeldt, S. J. Redding, D. M. Sturm and N. Wolf, \"The Economics of Density: Evidence from the "
         "Berlin Wall\", Econometrica 83(6): 2127-2189 (2015)",
    tag="Ahlfeldt, \\ Redding, \\ Sturm and Wolf, \\ \\emph{Econometrica} 83(6) (2015)",
    where="the introduction and Table V, column (3): production externalities lambda = 0.0710 (s.e. 0.0054), their "
          "decay delta = 0.3617, residential externalities eta = 0.1553, decay rho = 0.7595; commuting nu = 0.07 per "
          "minute and epsilon = 6.83; 'towards the high end of the 3-8 percent range' of Rosenthal and Strange (2004)",
    read="NBER Working Paper 20354 (2014, pdf)",
    checked="2026-11-20",
    data={"lambda": 0.0710, "delta": 0.3617, "eta": 0.1553, "rho": 0.7595, "nu": 0.07, "epsilon": 6.83,
          "rs_lo": 3, "rs_hi": 8, "years": (1936, 1986, 2006)},
)
CICCONE_HALL_1996 = Table(
    key="ciccone_hall_1996",
    cite="A. Ciccone and R. E. Hall, \"Productivity and the Density of Economic Activity\", American Economic Review "
         "86(1): 54-70 (1996); NBER Working Paper 4313 (1993)",
    tag="Ciccone and Hall, \\ \\emph{AER} 86(1) (1996)",
    where="US states' gross output; a doubling of employment density raises labour productivity by about 5 to 6 "
          "percent, controlling for education; density explains more than half of the differences in productivity "
          "between states (the working paper's abstract)",
    read="the working paper's abstract (scanned pdf) and secondary summaries for the 5-6 percent",
    checked="2026-11-20",
    data={"lo": 5.0, "hi": 6.0, "share_explained": 0.5},
)
DMQ_2019 = Table(
    key="dmq_2019",
    cite="R. Diamond, T. McQuade and F. Qian, \"The Effects of Rent Control Expansion on Tenants, Landlords, and "
         "Inequality: Evidence from San Francisco\", American Economic Review 109(9): 3365-3394 (2019)",
    tag="Diamond, \\ McQuade and Qian, \\ \\emph{AER} 109(9) (2019)",
    where="the abstract: a 1994 law change; rent control limits renters' mobility by 20 percent; treated landlords "
          "reduce rental housing supply by 15 percent by selling to owner-occupants and redeveloping",
    read="the AEA's abstract page",
    checked="2026-11-20",
    data={"year": 1994, "mobility": -0.20, "supply": -0.15, "built_before": 1980},
)
CHK_2016 = Table(
    key="chk_2016",
    cite="R. Chetty, N. Hendren and L. F. Katz, \"The Effects of Exposure to Better Neighborhoods on Children: New "
         "Evidence from the Moving to Opportunity Experiment\", American Economic Review 106(4): 855-902 (2016)",
    tag="Chetty, \\ Hendren and Katz, \\ \\emph{AER} 106(4) (2016)",
    where="the abstract (NBER WP 21156): children whose families took up an experimental voucher before age 13 earn "
          "$3,477 (31%) more a year in their mid-twenties, against a control mean of $11,270 (treatment on the "
          "treated); moving as an adolescent has slightly negative effects; the experiment enrolled 4,604 families "
          "in Baltimore, Boston, Chicago, Los Angeles and New York, 1994-1998, in three arms (vouchers usable only "
          "in tracts with under 10% poverty, ordinary vouchers, control)",
    read="the NBER and AEA abstracts; NBER WP 21156, section 2",
    checked="2026-11-20",
    data={"gain": 3477, "control": 11270, "pct": 31, "age": 13, "families": 4604, "cities": 5, "start": 1994,
          "end": 1998, "poverty": 10},
)
HSIEH_MORETTI_2019 = Table(
    key="hsieh_moretti_2019",
    cite="C.-T. Hsieh and E. Moretti, \"Housing Constraints and Spatial Misallocation\", American Economic Journal: "
         "Macroeconomics 11(2): 1-39 (2019); B. Greaney, \"Housing Constraints and Spatial Misallocation: Comment\", "
         "American Economic Journal: Macroeconomics 18(2): 409-428 (2026)",
    tag="Hsieh and Moretti (2019); \\ Greaney (2026)",
    where="the abstracts: housing constraints lowered aggregate US growth by 36 percent from 1964 to 2009 (220 "
          "metropolitan areas); the comment finds coding errors (the counterfactual as coded would lower output), "
          "and in a unit-invariant version the effect is two orders of magnitude smaller than the 3.7 percent of GDP "
          "reported for relaxing three cities' rules",
    read="the AEA's abstract pages",
    checked="2026-11-20",
    data={"growth_cut": 36, "metros": 220, "gdp_three": 3.7, "greaney_orders": 2},
)
DONALDSON_2018 = Table(
    key="donaldson_2018",
    cite="D. Donaldson, \"Railroads of the Raj: Estimating the Impact of Transportation Infrastructure\", American "
         "Economic Review 108(4-5): 899-934 (2018)",
    tag="Donaldson, \\ \\emph{AER} 108(4-5) (2018)",
    where="the abstract (railroads cut trade costs and price gaps, raised trade and real income); the 16 percent rise "
          "in real agricultural income in a district reached by the railroad, from the NBER working paper and MIT's "
          "summary of the published paper",
    read="the AEA's abstract page; MIT News (27 April 2018)",
    checked="2026-11-20",
    data={"income": 16},
)
BAUM_SNOW_2007 = Table(
    key="baum_snow_2007",
    cite="N. Baum-Snow, \"Did Highways Cause Suburbanization?\", Quarterly Journal of Economics 122(2): 775-805 (2007)",
    tag="Baum-Snow, \\ \\emph{QJE} 122(2) (2007)",
    where="the abstract: one new highway through a central city reduces its population by about 18 percent; without "
          "the interstates central-city population would have grown about 8 percent rather than falling 17 percent "
          "(1950-1990); instruments from the 1947 plan",
    read="the abstract (RePEc)",
    checked="2026-11-20",
    data={"per_highway": -18, "counterfactual": 8, "actual": -17},
)
KLINE_MORETTI_2014 = Table(
    key="kline_moretti_2014",
    cite="P. Kline and E. Moretti, \"Local Economic Development, Agglomeration Economies, and the Big Push: 100 Years "
         "of Evidence from the Tennessee Valley Authority\", Quarterly Journal of Economics 129(1): 275-331 (2014)",
    tag="Kline and Moretti, \\ \\emph{QJE} 129(1) (2014)",
    where="the abstract (NBER WP 19293): agricultural gains reversed when transfers lapsed; manufacturing gains kept "
          "growing; the local agglomeration gains were offset elsewhere; the infrastructure raised national "
          "manufacturing productivity by more than its cost",
    read="the NBER abstract",
    checked="2026-11-20",
    data={"start": 1933},
)
SHENZHEN = Table(
    key="shenzhen",
    cite="Shenzhen Statistical Bureau (1979 population, as tabulated by Wikipedia's 'Demographics of Shenzhen'); "
         "the Seventh National Population Census of China (2020)",
    tag="Shenzhen Statistical Bureau; \\ China's 2020 census",
    where="1979: 314,100 residents; 2020 census: 17.56 million; the special economic zone approved in August 1980",
    read="the census figure as reported; the 1979 figure from the tabulation",
    checked="2026-11-20",
    data={"pop1979": 314100, "pop2020": 17.56e6, "sez": 1980},
)
SCHELLING_1971 = Table(
    key="schelling_1971",
    cite="T. C. Schelling, \"Dynamic Models of Segregation\", Journal of Mathematical Sociology 1(2): 143-186 (1971); "
         "R. Hegselmann, \"Thomas C. Schelling and James M. Sakoda: The Intellectual, Technical, and Social History "
         "of a Model\", Journal of Artificial Societies and Social Simulation 20(3): 15 (2017)",
    tag="Schelling, \\ \\emph{J. Math. Sociol.} 1(2) (1971); \\ Hegselmann (2017)",
    where="the model first in a 1969 RAND memorandum, then the 1971 paper and Micromotives and Macrobehavior (1978); "
          "Sakoda's precursor in his 1949 dissertation, published in the journal's first issue",
    read="Hegselmann's history (JASSS)",
    checked="2026-11-20",
    data={"memo": 1969, "paper": 1971, "book": 1978, "sakoda": 1949},
)
PART37 = (SAIZ_2010, CDGR_2010, ARSW_2015, CICCONE_HALL_1996, DMQ_2019, CHK_2016, HSIEH_MORETTI_2019, DONALDSON_2018,
          BAUM_SNOW_2007, KLINE_MORETTI_2014, SHENZHEN, SCHELLING_1971)

# ---------------------------------------------------------------------------
# Part 38: Work and Wages
CK_1994 = Table(
    key="ck_1994",
    cite="D. Card and A. B. Krueger, \"Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New "
         "Jersey and Pennsylvania\", American Economic Review 84(4): 772-793 (1994)",
    tag="Card and Krueger, \\ \\emph{AER} 84(4) (1994)",
    where="Table 3 (full-time-equivalent employment per store: Pennsylvania 23.33 before and 21.17 after, New Jersey "
          "20.44 and 21.03), reproduced exactly from the public data; New Jersey's minimum rose from $4.25 to $5.05 "
          "on 1 April 1992; 410 stores surveyed in February-March and again in November-December 1992",
    read="the public data (njmin.zip) and its codebook",
    checked="2026-11-20",
    data={"m0": 4.25, "m1": 5.05, "stores": 410, "nj": 331, "pa": 79},
)
NW_2000 = Table(
    key="nw_2000",
    cite="D. Neumark and W. Wascher, \"Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New "
         "Jersey and Pennsylvania: Comment\", American Economic Review 90(5): 1362-1396 (2000); D. Card and A. B. "
         "Krueger, \"... Reply\", American Economic Review 90(5): 1397-1420 (2000)",
    tag="Neumark and Wascher; \\ Card and Krueger, \\ \\emph{AER} 90(5) (2000)",
    where="the payroll records of 230 restaurants (NBER WP 5224): employment 4.6% lower in New Jersey relative to "
          "Pennsylvania, an elasticity of -0.24 with respect to the minimum wage; the reply's BLS ES-202 records: "
          "similar or slightly faster growth in New Jersey",
    read="the NBER working papers' abstracts (5224, 6386) and summaries",
    checked="2026-11-20",
    data={"stores": 230, "effect": -4.6, "elasticity_mw": -0.24},
)
CDLZ_2019 = Table(
    key="cdlz_2019",
    cite="D. Cengiz, A. Dube, A. Lindner and B. Zipperer, \"The Effect of Minimum Wages on Low-Wage Jobs\", Quarterly "
         "Journal of Economics 134(3): 1405-1454 (2019)",
    tag="Cengiz, \\ Dube, \\ Lindner and Zipperer, \\ \\emph{QJE} 134(3) (2019)",
    where="the abstract and conclusion: 138 state minimum-wage increases, 1979-2016; the number of low-wage jobs "
          "essentially unchanged over five years, missing jobs below the new minimum offset by excess jobs at and "
          "just above it; an own-wage employment elasticity of 0.41 (s.e. 0.43)",
    read="the accepted manuscript (UCL Discovery) and NBER WP 25434",
    checked="2026-11-20",
    data={"events": 138, "owe": 0.41, "owe_se": 0.43, "first": 1979, "last": 2016},
)
JARDIM_2022 = Table(
    key="jardim_2022",
    cite="E. Jardim, M. C. Long, R. Plotnick, E. van Inwegen, J. Vigdor and H. Wething, \"Minimum-Wage Increases and "
         "Low-Wage Employment: Evidence from Seattle\", American Economic Journal: Economic Policy 14(2): 263-314 "
         "(2022)",
    tag="Jardim et al., \\ \\emph{AEJ: Policy} 14(2) (2022)",
    where="the abstract: Seattle's minimum to $11 (2015) and $13 (2016); hours at low wages fell relative to a "
          "synthetic control; employment elasticities of -0.2 to -2.0, mostly on the intensive margin",
    read="the AEA's abstract page",
    checked="2026-11-20",
    data={"m2015": 11, "m2016": 13, "lo": -2.0, "hi": -0.2},
)
CABS = Table(
    key="cabs",
    cite="C. Camerer, L. Babcock, G. Loewenstein and R. Thaler, \"Labor Supply of New York City Cabdrivers: One Day "
         "at a Time\", Quarterly Journal of Economics 112(2): 407-441 (1997); H. S. Farber, \"Why You Can't Find a "
         "Taxi in the Rain and Other Labor Supply Lessons from Cab Drivers\", Quarterly Journal of Economics "
         "130(4): 1975-2026 (2015); J. D. Angrist, S. Caldwell and J. V. Hall, \"Uber versus Taxi: A Driver's Eye "
         "View\", American Economic Journal: Applied Economics 13(3): 272-308 (2021)",
    tag="Camerer et al.\\ (1997); \\ Farber (2015); \\ Angrist, \\ Caldwell and Hall (2021)",
    where="Camerer et al.: a negative elasticity of daily hours to the day's hourly earnings (a pure daily target "
          "gives -1); Farber: every New York taxi trip of 2009-2013, positive responses to anticipated and "
          "unanticipated earnings; Angrist et al.: Boston Uber drivers offered random fee changes, an intertemporal "
          "elasticity of about 1.2",
    read="the abstracts and summaries (NBER WP 20604; the AEA's abstract page)",
    checked="2026-11-20",
    data={"target": -1.0, "uber_frisch": 1.2, "farber_years": (2009, 2013)},
)
CHETTY_2011 = Table(
    key="chetty_2011",
    cite="R. Chetty, A. Guren, D. Manoli and A. Weber, \"Are Micro and Macro Labor Supply Elasticities Consistent? A "
         "Review of Evidence on the Intensive and Extensive Margins\", American Economic Review 101(3): 471-475 "
         "(2011)",
    tag="Chetty, \\ Guren, \\ Manoli and Weber, \\ \\emph{AER P\\&P} 101(3) (2011)",
    where="the recommended values from the micro evidence: Hicksian 0.3 (intensive) and 0.25 (extensive); Frisch 0.5 "
          "(intensive) and 0.25 (extensive); micro Frisch elasticities an order of magnitude below what business "
          "cycles need",
    read="the AEA's abstract and NBER WP 16729 as summarized",
    checked="2026-11-20",
    data={"hicks_int": 0.3, "hicks_ext": 0.25, "frisch_int": 0.5, "frisch_ext": 0.25},
)
SS_2021 = Table(
    key="ss_2021",
    cite="A. Sokolova and T. Sorensen, \"Monopsony in Labor Markets: A Meta-Analysis\", ILR Review 74(1): 27-55 (2021)",
    tag="Sokolova and Sorensen, \\ \\emph{ILR Review} 74(1) (2021)",
    where="IZA DP 11966's abstract: about 800 published estimates of the labour supply elasticity facing a firm; "
          "systematic variation by method and country (more competitive in Europe, less in developing countries); "
          "publication bias against negative estimates",
    read="IZA Discussion Paper 11966 (pdf)",
    checked="2026-11-20",
    data={"estimates": 801},
)
AK_1991 = Table(
    key="ak_1991",
    cite="J. D. Angrist and A. B. Krueger, \"Does Compulsory School Attendance Affect Schooling and Earnings?\", "
         "Quarterly Journal of Economics 106(4): 979-1014 (1991); J. Bound, D. A. Jaeger and R. M. Baker, \"Problems "
         "with Instrumental Variables Estimation When the Correlation between the Instruments and the Endogenous "
         "Explanatory Variable Is Weak\", Journal of the American Statistical Association 90(430): 443-450 (1995)",
    tag="Angrist and Krueger (1991); \\ Bound, \\ Jaeger and Baker (1995)",
    where="NBER WP 3572's abstract: up to 25% of potential dropouts stay in school because of compulsory schooling "
          "laws; the IV estimate of the return is remarkably close to least squares; Bound et al.: random 'quarters "
          "of birth' reproduce estimates close to least squares, a sign of weak instruments",
    read="the working paper's abstract (scanned) and summaries of Bound et al.",
    checked="2026-11-20",
    data={"dropouts": 25},
)
OREOPOULOS_2006 = Table(
    key="oreopoulos_2006",
    cite="P. Oreopoulos, \"Estimating Average and Local Average Treatment Effects of Education when Compulsory "
         "Schooling Laws Really Matter\", American Economic Review 96(1): 152-175 (2006)",
    tag="Oreopoulos, \\ \\emph{AER} 96(1) (2006)",
    where="the abstract: Britain's school-leaving age rose from 14 to 15 (1947), sending almost half of 14-year-olds "
          "to stay a year longer; a regression-discontinuity design; returns very large whether laws bind for many or "
          "few",
    read="the AEA's abstract page",
    checked="2026-11-20",
    data={"from": 14, "to": 15},
)
MARIEL = Table(
    key="mariel",
    cite="D. Card, \"The Impact of the Mariel Boatlift on the Miami Labor Market\", ILR Review 43(2): 245-257 (1990); "
         "G. J. Borjas, \"The Wage Impact of the Marielitos: A Reappraisal\", ILR Review 70(5): 1077-1110 (2017); G. "
         "Peri and V. Yasenov, \"The Labor Market Effects of a Refugee Wave\", Journal of Human Resources 54(2): "
         "267-309 (2019)",
    tag="Card (1990); \\ Borjas (2017); \\ Peri and Yasenov (2019)",
    where="Card: some 125,000 Cubans arrived from May to September 1980, raising Miami's labour force 7% (and its "
          "Cuban labour force 20%); no measurable effect on less-skilled workers' wages or unemployment; Borjas: the "
          "wage of "
          "non-Hispanic male high-school dropouts fell 10 to 30 percent; Peri and Yasenov: synthetic controls on "
          "non-Cuban dropouts, no significant difference, and small subsamples can produce large ones",
    read="the papers' abstracts and summaries",
    checked="2026-11-20",
    data={"year": 1980, "arrivals": 125000, "labour_force": 7, "cuban_lf": 20, "borjas_lo": 10, "borjas_hi": 30},
)
KEARL_1979 = Table(
    key="kearl_1979",
    cite="J. R. Kearl, C. L. Pope, G. C. Whiting and L. T. Wimmer, \"A Confusion of Economists?\", American Economic "
         "Review 69(2): 28-37 (1979)",
    tag="Kearl, \\ Pope, \\ Whiting and Wimmer, \\ \\emph{AER P\\&P} 69(2) (1979)",
    where="of 211 economists, 90% agreed, or agreed with provisos, that 'a minimum wage increases unemployment "
          "among young and unskilled workers' (as reported in later surveys; the fieldwork year is given variously)",
    read="secondary accounts (Fuller and Geide-Stevenson; Econlib)",
    checked="2026-11-20",
    data={"agree": 90, "n": 211},
)
PART38 = (CK_1994, NW_2000, CDLZ_2019, JARDIM_2022, CABS, CHETTY_2011, SS_2021, AK_1991, OREOPOULOS_2006, MARIEL,
          KEARL_1979)

# ---------------------------------------------------------------------------
# Part 39: The Wage Structure
KM_1992 = Table(
    key="km_1992",
    cite="L. F. Katz and K. M. Murphy, \"Changes in Relative Wages, 1963-1987: Supply and Demand Factors\", Quarterly "
         "Journal of Economics 107(1): 35-78 (1992)",
    tag="Katz and Murphy, \\ \\emph{QJE} 107(1) (1992)",
    where="the relative-demand regression of the college/high-school premium on a trend and relative supply, "
          "1963-87: a supply coefficient of about -0.709, an elasticity of substitution of 1/0.709 = 1.41",
    read="O. Blanchard's account of the regression (Federal Reserve Bank of New York Economic Policy Review, 1995) "
         "and later summaries",
    checked="2026-11-20",
    data={"sigma": 1.41, "coef": -0.709, "first": 1963, "last": 1987},
)
SIGMA_SKILL = Table(
    key="sigma_skill",
    cite="D. Card and T. Lemieux, Quarterly Journal of Economics 116(2): 705-746 (2001); A. Ciccone and G. Peri, "
         "Review of Economics and Statistics 87(4): 652-663 (2005); D. Autor, C. Goldin and L. F. Katz, AEA Papers "
         "and Proceedings 110: 347-351 (2020)",
    tag="Card and Lemieux (2001); \\ Ciccone and Peri (2005); \\ Autor, \\ Goldin and Katz (2020)",
    where="Card and Lemieux: an elasticity of about 2.5 between high-school and college workers (and about 5 between "
          "age groups); Ciccone and Peri: about 1.5 from US states, 1950-90, with schooling laws as instruments; "
          "Autor, Goldin and Katz: rising educational differentials explain 75% of the rise in US wage inequality "
          "in 1980-2000 and 38% in 2000-17",
    read="the abstracts",
    checked="2026-11-20",
    data={"cl": 2.5, "cl_age": 5.0, "cp": 1.5, "agk_8000": 75, "agk_0017": 38},
)
ALM_2003 = Table(
    key="alm_2003",
    cite="D. H. Autor, F. Levy and R. J. Murnane, \"The Skill Content of Recent Technological Change: An Empirical "
         "Exploration\", Quarterly Journal of Economics 118(4): 1279-1333 (2003); D. Acemoglu and D. Autor, \"Skills, "
         "Tasks and Technologies\", Handbook of Labor Economics 4B (2011); D. Autor and D. Dorn, American Economic "
         "Review 103(5): 1553-1597 (2013)",
    tag="Autor, \\ Levy and Murnane (2003); \\ Acemoglu and Autor (2011); \\ Autor and Dorn (2013)",
    where="computers substitute for routine tasks, cognitive and manual, and complement non-routine analytic and "
          "interactive tasks; the employment and wage polarization of 1980-2005 (Autor and Dorn's abstract)",
    read="the abstracts; the polarization data are Autor and Dorn's replication files",
    checked="2026-11-20",
    data={},
)
AR_2020 = Table(
    key="ar_2020",
    cite="D. Acemoglu and P. Restrepo, \"Robots and Jobs: Evidence from US Labor Markets\", Journal of Political "
         "Economy 128(6): 2188-2244 (2020)",
    tag="Acemoglu and Restrepo, \\ \\emph{JPE} 128(6) (2020)",
    where="across commuting zones, one more robot per thousand workers lowers the employment-to-population ratio by "
          "0.2 percentage points and wages by 0.42% (the published abstract; the working paper's range is 0.18-0.34 "
          "points and 0.25-0.5 percent); the effects are distinct from those of imports from China and Mexico, the "
          "decline of routine jobs, offshoring and other IT capital, and the most exposed areas show no differential "
          "trends before 1990",
    read="the JPE abstract (via EconPapers), NBER Working Paper 23285 and MIT's summary",
    checked="2026-11-20",
    data={"emp_pp": 0.2, "wage_pct": 0.42, "emp_lo": 0.18, "emp_hi": 0.34, "wage_lo": 0.25, "wage_hi": 0.5},
)
CHK_2013 = Table(
    key="chk_2013",
    cite="D. Card, J. Heining and P. Kline, \"Workplace Heterogeneity and the Rise of West German Wage Inequality\", "
         "Quarterly Journal of Economics 128(3): 967-1015 (2013)",
    tag="Card, \\ Heining and Kline, \\ \\emph{QJE} 128(3) (2013)",
    where="Table 3 of NBER Working Paper 18522: the variance of log wages rose from 0.137 (1985-91) to 0.249 "
          "(2002-09); the establishment effects' share from 18.5% to 21.2%, twice the covariance of worker and "
          "establishment effects from 2.3% to 16.4%; of the rise, worker effects 39%, establishment effects 25%, "
          "sorting 34%",
    read="the working paper's Table 3; the abstract for the conclusion",
    checked="2026-11-20",
    data={"var1": 0.137, "var4": 0.249, "psi1": 18.5, "psi4": 21.2, "cov1": 2.3, "cov4": 16.4, "rise_alpha": 39,
          "rise_psi": 25, "rise_cov": 34},
)
ADKPV_2020 = Table(
    key="adkpv_2020",
    cite="D. Autor, D. Dorn, L. F. Katz, C. Patterson and J. Van Reenen, \"The Fall of the Labor Share and the Rise of "
         "Superstar Firms\", Quarterly Journal of Economics 135(2): 645-709 (2020); S. Rosen, \"The Economics of "
         "Superstars\", American Economic Review 71(5): 845-858 (1981)",
    tag="Rosen (1981); \\ Autor et al., \\ \\emph{QJE} 135(2) (2020)",
    where="the fall in the aggregate labour share is largely a reallocation of value added towards firms with low "
          "labour shares, and industries where concentration rose most saw the largest falls in the labour share",
    read="the abstract",
    checked="2026-11-20",
    data={},
)
UNIONS = Table(
    key="unions",
    cite="U.S. Bureau of Labor Statistics, \"Union Members - 2024\", news release USDL-25-0105 (28 January 2025)",
    tag="BLS, \\ Union Members 2024",
    where="union membership was 20.1% of wage and salary workers in 1983, the first year of comparable data, and 9.9% "
          "in 2024; 32.2% in the public sector and 5.9% in the private sector in 2024",
    read="the news release",
    checked="2026-11-20",
    data={"y1983": 20.1, "y2024": 9.9, "public": 32.2, "private": 5.9},
)
MAS_PALLAIS_2017 = Table(
    key="mas_pallais_2017",
    cite="A. Mas and A. Pallais, \"Valuing Alternative Work Arrangements\", American Economic Review 107(12): "
         "3722-3759 (2017)",
    tag="Mas and Pallais, \\ \\emph{AER} 107(12) (2017)",
    where="in a discrete choice experiment among applicants to a national call centre, the average worker would give "
          "up 20% of wages to avoid a schedule set by the employer on short notice, and 8% for the option to work "
          "from home",
    read="the AEA abstract",
    checked="2026-11-20",
    data={"avoid_short_notice": 20, "wfh": 8},
)
BM_2004 = Table(
    key="bm_2004",
    cite="M. Bertrand and S. Mullainathan, \"Are Emily and Greg More Employable Than Lakisha and Jamal? A Field "
         "Experiment on Labor Market Discrimination\", American Economic Review 94(4): 991-1013 (2004)",
    tag="Bertrand and Mullainathan, \\ \\emph{AER} 94(4) (2004)",
    where="White names receive 50 percent more callbacks; callbacks respond more to resume quality for White names; "
          "the gap is uniform across occupation, industry and employer size (abstract); the data recomputed from "
          "openintro's copy",
    read="the AEA abstract and the data",
    checked="2026-11-20",
    data={"ratio": 1.5},
)
DISCRIMINATION = Table(
    key="discrimination",
    cite="C. Goldin and C. Rouse, \"Orchestrating Impartiality\", American Economic Review 90(4): 715-741 (2000); L. "
         "Quillian, D. Pager, O. Hexel and A. H. Midtboen, \"Meta-analysis of field experiments shows no change in "
         "racial discrimination in hiring over time\", PNAS 114(41): 10870-10875 (2017); G. S. Becker, The Economics "
         "of Discrimination (1957); E. S. Phelps, American Economic Review 62(4) (1972); K. J. Arrow (1973)",
    tag="Goldin and Rouse (2000); \\ Quillian et al.\\ (2017)",
    where="Goldin and Rouse: the screen increases the probability a woman will be advanced and hired, though some "
          "estimates have large standard errors and one effect runs the other way; Quillian et al.: in 24 field "
          "experiments since 1989, White applicants received 36% more callbacks than African Americans and 24% more "
          "than Latinos, with no change over time for African Americans",
    read="the abstracts and the PNAS summary",
    checked="2026-11-20",
    data={"meta_black": 36, "meta_latino": 24, "meta_studies": 24, "meta_since": 1989},
)
GENDER = Table(
    key="gender",
    cite="C. Goldin, \"A Grand Gender Convergence: Its Last Chapter\", American Economic Review 104(4): 1091-1119 "
         "(2014); H. Kleven, C. Landais and J. E. Sogaard, \"Children and Gender Inequality: Evidence from Denmark\", "
         "American Economic Journal: Applied Economics 11(4): 181-209 (2019)",
    tag="Goldin (2014); \\ Kleven, \\ Landais and S\\o{}gaard (2019)",
    where="Goldin: the gap would shrink and might vanish if firms did not disproportionately reward long hours and "
          "particular hours; Kleven et al.: children create a long-run gender gap in earnings of about 20%, through "
          "hours, participation and wage rates; the share of gender inequality due to children rose from about 40% in "
          "1980 to about 80% in 2013 (working paper)",
    read="the AEA abstracts; NBER Working Paper 24219 for the 40% and 80%",
    checked="2026-11-20",
    data={"penalty": 20, "share1980": 40, "share2013": 80},
)
FRONTIER39 = Table(
    key="frontier39",
    cite="Z. Cullen and B. Pakzad-Hurson, \"Equilibrium Effects of Pay Transparency\", Econometrica 91(3): 765-802 "
         "(2023); J. Dastin, \"Amazon scraps secret AI recruiting tool that showed bias against women\", Reuters, 10 "
         "October 2018",
    tag="Cullen and Pakzad-Hurson, \\ \\emph{Econometrica} 91(3) (2023); \\ Reuters (2018)",
    where="US state pay-transparency laws lowered wages by about 2%, least where workers' individual bargaining power "
          "was low; Amazon's experimental resume-scoring tool, trained on ten years of resumes mostly from men, "
          "penalized the word 'women's' and was dropped",
    read="the abstract; Reuters's report as syndicated",
    checked="2026-11-20",
    data={"transparency": -2},
)
LEONTIEF_1983 = Table(
    key="leontief_1983",
    cite="W. Leontief, \"National Perspective: The Definition of Problem and Opportunity\", in The Long-Term Impact of "
         "Technology on Employment and Unemployment, National Academy of Engineering symposium, 30 June 1983, p. 3",
    tag="Leontief (1983)",
    where="'the role of humans as the most important factor of production is bound to diminish in the same way that "
          "the role of horses in agricultural production was first diminished and then eliminated by the "
          "introduction of tractors'",
    read="secondary listings (Wikiquote; the 'For Work / Against Work' bibliography)",
    checked="2026-11-20",
    data={"year": 1983},
)
PART39 = (KM_1992, SIGMA_SKILL, ALM_2003, AR_2020, CHK_2013, ADKPV_2020, UNIONS, MAS_PALLAIS_2017, BM_2004,
          DISCRIMINATION, GENDER, FRONTIER39, LEONTIEF_1983)

# Part 40: Inequality and Mobility
PEN_1971 = Table(
    key="pen_1971",
    cite="J. Pen, Income Distribution: Facts, Theories, Policies, translated by T. S. Preston, Allen Lane (1971), "
         "chapter 3",
    tag="Pen, \\ \\emph{Income Distribution} (1971)",
    where="the parade: the whole population marches past in an hour, each person as tall as their income, the "
          "average income at average height; dwarfs for most of the hour, giants in the last minutes",
    read="the book's account as retold in later texts (Atkinson; Milanovic)",
    checked="2026-11-20",
    data={"minutes": 60},
)
ATKINSON_1970 = Table(
    key="atkinson_1970",
    cite="A. B. Atkinson, \"On the Measurement of Inequality\", Journal of Economic Theory 2(3): 244-263 (1970)",
    tag="Atkinson, \\ \\emph{JET} 2(3) (1970)",
    where="the index 1 - (equally distributed equivalent income)/(mean), for a social welfare function with constant "
          "inequality aversion epsilon; Lorenz curves that cross cannot be ranked without a value judgement",
    read="the article's statement as summarized in Cowell, Measuring Inequality",
    checked="2026-11-20",
    data={},
)
PIKETTY_SAEZ_2003 = Table(
    key="piketty_saez_2003",
    cite="T. Piketty and E. Saez, \"Income Inequality in the United States, 1913-1998\", Quarterly Journal of "
         "Economics 118(1): 1-39 (2003), with series updated to 2022",
    tag="Piketty and Saez, \\ \\emph{QJE} 118(1) (2003), \\ updated to 2022",
    where="top income shares from federal income tax returns, 1913 on; the series is in the Data Room (saez)",
    read="the paper and the updated tables (TabFig2022.xlsx)",
    checked="2026-11-20",
    data={},
)
AUTEN_SPLINTER_2024 = Table(
    key="auten_splinter_2024",
    cite="G. Auten and D. Splinter, \"Income Inequality in the United States: Using Tax Data to Measure Long-Term "
         "Trends\", Journal of Political Economy 132(7): 2179-2227 (2024); T. Piketty, E. Saez and G. Zucman, "
         "\"Income Inequality in the United States: A Comment\" (2024)",
    tag="Auten and Splinter, \\ \\emph{JPE} 132(7) (2024); \\ Piketty, \\ Saez and Zucman (2024)",
    where="Auten and Splinter: the top 1% share of pre-tax national income rose 2.6 percentage points from the early "
          "1960s to 2019 (4.4 points since 1979); of after-tax income, 1.4 points since 1979; the top 1% share of "
          "fiscal income rose from 9% to 19% in 1962-2019, a third of it around the 1986 tax reform. Piketty, Saez "
          "and Zucman's after-tax-and-transfer share rose from about 9% in 1960 to 15% in 2019; they attribute the "
          "difference to the allocation of untaxed business income, untaxed capital income and non-cash income",
    read="the published paper's abstract and introduction as quoted; the Brookings primer; PSZ's comment",
    checked="2026-11-20",
    data={"as_pretax_pp": 2.6, "as_pretax_pp_1979": 4.4, "as_aftertax_pp_1979": 1.4, "fiscal_1962": 9,
          "fiscal_2019": 19, "psz_after_1960": 9, "psz_after_2019": 15},
)
PARETO_1896 = Table(
    key="pareto_1896",
    cite="V. Pareto, Cours d'\u00e9conomie politique, Lausanne (1896-97); D. G. Champernowne, \"A Model of Income "
         "Distribution\", Economic Journal 63: 318-351 (1953); X. Gabaix, \"Power Laws in Economics and Finance\", "
         "Annual Review of Economics 1: 255-293 (2009)",
    tag="Pareto (1896); \\ Champernowne (1953); \\ Gabaix (2009)",
    where="Pareto: the number of people with income above x falls like x to a power, the same in every country he "
          "examined; Champernowne and Gabaix: random proportional growth with a floor or with births and deaths "
          "gives a Pareto tail",
    read="Gabaix's review",
    checked="2026-11-20",
    data={},
)
GLLM_2016 = Table(
    key="gllm_2016",
    cite="X. Gabaix, J.-M. Lasry, P.-L. Lions and B. Moll, \"The Dynamics of Inequality\", Econometrica 84(6): "
         "2071-2111 (2016)",
    tag="Gabaix, \\ Lasry, \\ Lions and Moll, \\ \\emph{Econometrica} 84(6) (2016)",
    where="standard random growth models produce transitions far too slow to explain the rise of top incomes since "
          "the 1970s (an order of magnitude too slow, in the working paper); scale dependence or type dependence "
          "(high-growth types, as in theories of superstar entrepreneurs and managers) can produce fast transitions",
    read="the published abstract and NBER Working Paper 21363",
    checked="2026-11-20",
    data={},
)
CAPITAL_2014 = Table(
    key="capital_2014",
    cite="T. Piketty, Capital in the Twenty-First Century, Harvard University Press (2014); M. Rognlie, \"Deciphering "
         "the Fall and Rise in the Net Capital Share\", Brookings Papers on Economic Activity (Spring 2015); P. "
         "Krusell and A. A. Smith, \"Is Piketty's 'Second Law of Capitalism' Fundamental?\", Journal of Political "
         "Economy 123(4): 725-748 (2015)",
    tag="Piketty (2014); \\ Rognlie (2015); \\ Krusell and Smith (2015)",
    where="r > g as a force for concentrating wealth; replies: the rise in the net capital share is largely "
          "housing (Rognlie); with depreciation, the capital-income ratio does not explode as growth slows "
          "(Krusell and Smith); a rising capital share as capital accumulates needs an elasticity of substitution "
          "above one, while most estimates are below it",
    read="the book; the two papers' abstracts",
    checked="2026-11-20",
    data={},
)
KUZNETS_1955 = Table(
    key="kuznets_1955",
    cite="S. Kuznets, \"Economic Growth and Income Inequality\", American Economic Review 45(1): 1-28 (1955)",
    tag="Kuznets, \\ \\emph{AER} 45(1) (1955)",
    where="inequality widens in the early phases of growth, as people move from agriculture to industry, becomes "
          "stable, then narrows; the paper is 'perhaps 5 per cent empirical information and 95 per cent "
          "speculation, some of it possibly tainted by wishful thinking'",
    read="the article (via the NBER chapter and Wikiquote's extract)",
    checked="2026-11-20",
    data={"year": 1955},
)
IGE_STUDIES = Table(
    key="ige_studies",
    cite="G. Solon, \"Intergenerational Income Mobility in the United States\", American Economic Review 82(3): "
         "393-408 (1992); B. Mazumder, \"Fortunate Sons: New Estimates of Intergenerational Mobility in the United "
         "States Using Social Security Earnings Data\", Review of Economics and Statistics 87(2): 235-255 (2005); M. "
         "Corak, \"Income Inequality, Equality of Opportunity, and Intergenerational Mobility\", Journal of Economic "
         "Perspectives 27(3): 79-102 (2013), and testimony to the US Senate (2012)",
    tag="Solon (1992); \\ Mazumder (2005); \\ Corak (2013)",
    where="Solon: the elasticity of sons' earnings with respect to fathers' is 0.4 or higher, once fathers' earnings "
          "are averaged over several years; Mazumder: averaging over longer spells of Social Security earnings, "
          "about 0.6; Corak: across 22 countries, from less than 0.2 in Denmark, Norway and Finland to almost 0.7 "
          "in Peru, higher where inequality is higher (Krueger's 'Great Gatsby curve', 2012)",
    read="the abstracts; Corak's testimony; Mazumder's working paper",
    checked="2026-11-20",
    data={"solon": 0.4, "mazumder": 0.6, "corak_lo": 0.2, "corak_hi": 0.7},
)
CHETTY_2014 = Table(
    key="chetty_2014",
    cite="R. Chetty, N. Hendren, P. Kline and E. Saez, \"Where is the Land of Opportunity? The Geography of "
         "Intergenerational Mobility in the United States\", Quarterly Journal of Economics 129(4): 1553-1623 "
         "(2014)",
    tag="Chetty, \\ Hendren, \\ Kline and Saez, \\ \\emph{QJE} 129(4) (2014)",
    where="the rank-rank slope is 0.341; the log-log elasticity of child on parent family income is 0.344 (and "
          "unstable to specification); the chance of reaching the top fifth from the bottom fifth is 4.4% in "
          "Charlotte and 12.9% in San Jose",
    read="the published paper and NBER Working Paper 19843",
    checked="2026-11-20",
    data={"rank_slope": 0.341, "ige": 0.344, "charlotte": 4.4, "san_jose": 12.9},
)
CHETTY_2017 = Table(
    key="chetty_2017",
    cite="R. Chetty, D. Grusky, M. Hell, N. Hendren, R. Manduca and J. Narang, \"The Fading American Dream: Trends "
         "in Absolute Income Mobility since 1940\", Science 356(6336): 398-406 (2017)",
    tag="Chetty et al., \\ \\emph{Science} 356 (2017)",
    where="the share of children earning more than their parents at 30 (in real terms) fell from about 90% for those "
          "born in 1940 to 50% for those born in the 1980s; for the 1980 cohort, restoring the growth rates of "
          "the 1940s and 1950s with today's distribution would raise it only to 62%, while today's growth shared as "
          "in the 1940 cohort would raise it to 80%; the data are in the Data Room (opportunity, absmob)",
    read="the paper, its NBER abstract and the authors' VoxEU column",
    checked="2026-11-20",
    data={"growth_only": 62, "sharing_only": 80},
)
PLACES = Table(
    key="places",
    cite="R. Chetty and N. Hendren, \"The Impacts of Neighborhoods on Intergenerational Mobility I: Childhood "
         "Exposure Effects\", Quarterly Journal of Economics 133(3): 1107-1162 (2018); R. Chetty, N. Hendren and L. "
         "Katz, \"The Effects of Exposure to Better Neighborhoods on Children: New Evidence from the Moving to "
         "Opportunity Experiment\", American Economic Review 106(4): 855-902 (2016)",
    tag="Chetty and Hendren, \\ \\emph{QJE} 133(3) (2018); \\ Chetty, \\ Hendren and Katz, \\ "
        "\\emph{AER} 106(4) (2016)",
    where="children who move converge to the outcomes of the destination's permanent residents at about 4% a year "
          "of childhood spent there; in Moving to Opportunity (1994-98, five cities), children whose families used "
          "a voucher to move to a lower-poverty area before 13 earned $3,477 (31%) more in their mid-twenties than "
          "the control group's mean of $11,270; moves after 13 did not help",
    read="the abstracts (NBER Working Papers 23001 and 21156)",
    checked="2026-11-20",
    data={"exposure": 4, "mto_dollars": 3477, "mto_pct": 31, "mto_control": 11270},
)
GLOBAL = Table(
    key="global",
    cite="C. Lakner and B. Milanovic, \"Global Income Distribution: From the Fall of the Berlin Wall to the Great "
         "Recession\", World Bank Economic Review 30(2): 203-232 (2016); B. Milanovic, Global Inequality, Harvard "
         "University Press (2016)",
    tag="Lakner and Milanovic, \\ \\emph{WBER} 30(2) (2016)",
    where="the growth of real income by percentile of the global distribution, 1988-2008 (the 'elephant curve'): "
          "the largest gains around the global median, mostly in Asia; essentially none around the 80th to 85th "
          "percentiles, largely the lower middle classes of rich countries; large gains at the top 1%",
    read="the paper's summary and Milanovic's own account (World Economic Forum, 2016)",
    checked="2026-11-20",
    data={"stagnant_lo": 80, "stagnant_hi": 85, "first": 1988, "last": 2008},
)
MATTERS = Table(
    key="matters",
    cite="R. Chetty, M. Stepner, S. Abraham, S. Lin, B. Scuderi, N. Turner, A. Bergeron and D. Cutler, \"The "
         "Association Between Income and Life Expectancy in the United States, 2001-2014\", JAMA 315(16): "
         "1750-1766 (2016)",
    tag="Chetty et al., \\ \\emph{JAMA} 315(16) (2016)",
    where="at 40, the gap in life expectancy between the richest 1% and the poorest 1% was 14.6 years for men and "
          "10.1 years for women; between 2001 and 2014 it widened",
    read="the abstract (PubMed)",
    checked="2026-11-20",
    data={"men": 14.6, "women": 10.1},
)
FRONTIER40 = Table(
    key="frontier40",
    cite="T. Piketty, E. Saez and G. Zucman, \"Distributional National Accounts: Methods and Estimates for the "
         "United States\", Quarterly Journal of Economics 133(2): 553-609 (2018); K. Jakobsen, K. Jakobsen, H. Kleven "
         "and G. Zucman, \"Wealth Taxation and Wealth Accumulation: Theory and Evidence from Denmark\", Quarterly "
         "Journal of Economics 135(1): 329-388 (2020); S. E. Black, P. J. Devereux, P. Lundborg and K. Majlesi, "
         "\"Poor Little Rich Kids? The Role of Nature versus Nurture in Wealth and Other Economic Outcomes and "
         "Behaviours\", Review of Economic Studies 87(4): 1683-1725 (2020)",
    tag="Piketty, \\ Saez and Zucman (2018); \\ Jakobsen et al. (2020); \\ Black et al. (2020)",
    where="distributional national accounts allocate all of national income to people; in Denmark wealth taxes had "
          "clear short- and medium-run effects on wealth, larger at the top, and a sizeable long-run elasticity at "
          "the top; among Swedish adoptees, adoptive parents' wealth predicts the child's far more than biological "
          "parents' wealth, more so once bequests are counted",
    read="the abstracts",
    checked="2026-11-20",
    data={},
)
FORBES_400 = Table(
    key="forbes_400",
    cite="O. S. Klass, O. Biham, M. Levy, O. Malcai and S. Solomon, \"The Forbes 400 and the Pareto Wealth "
         "Distribution\", Economics Letters 90(2): 290-295 (2006)",
    tag="Klass et al., \\ \\emph{Economics Letters} 90(2) (2006)",
    where="the wealth of the Forbes 400, 1988-2003, follows a Pareto distribution with an average exponent of 1.49",
    read="the abstract",
    checked="2026-11-20",
    data={"alpha": 1.49},
)
PART40 = (PEN_1971, ATKINSON_1970, PIKETTY_SAEZ_2003, AUTEN_SPLINTER_2024, PARETO_1896, GLLM_2016, CAPITAL_2014,
          KUZNETS_1955, IGE_STUDIES, CHETTY_2014, CHETTY_2017, PLACES, GLOBAL, MATTERS, FRONTIER40, FORBES_400)


# Part 41: Taxes
LAFFER_1974 = Table(
    key="laffer_1974",
    cite="J. Wanniski, \"Taxes, Revenues, and the 'Laffer Curve'\", The Public Interest 50 (Winter 1978); "
         "Smithsonian Magazine, \"How a Restaurant Doodle Launched a Political Movement\" (2017); The New York Times, "
         "\"This Is Not Arthur Laffer's Famous Napkin\" (13 October 2017)",
    tag="Wanniski (1978); \\ Smithsonian (2017); \\ \\emph{New York Times} (2017)",
    where="in 1974, at the Two Continents restaurant in Washington, Arthur Laffer sketched for Dick Cheney, then a "
          "White House aide, a curve on which a tax rate of zero and one of a hundred percent both raise nothing; "
          "Jude Wanniski arranged the meeting and named the curve; accounts differ on the date and the guests, and "
          "the cloth napkin in the National Museum of American History, dated 13 September 1974, may be a later copy",
    read="the three accounts cited",
    checked="2026-11-20",
    data={"year": 1974},
)
HARBERGER_1962 = Table(
    key="harberger_1962",
    cite="A. C. Harberger, \"The Incidence of the Corporation Income Tax\", Journal of Political Economy 70(3): "
         "215-240 (1962); C. Fuest, A. Peichl and S. Siegloch, \"Do Higher Corporate Taxes Reduce Wages? Micro "
         "Evidence from Germany\", American Economic Review 108(2): 393-418 (2018)",
    tag="Harberger, \\ \\emph{JPE} 70(3) (1962); \\ Fuest, \\ Peichl and Siegloch, \\ \\emph{AER} 108(2) "
        "(2018)",
    where="Harberger: in a closed economy with a fixed stock of capital, capital bears about the whole burden of the "
          "corporate tax; Fuest, Peichl and Siegloch, from about 6,800 changes in German municipalities' local "
          "business tax over twenty years: about 51% of the burden falls on workers (about 40% in the 2015 working "
          "paper)",
    read="Harberger's summary in later surveys; the AER article's authors' summary (LSE Business Review)",
    checked="2026-11-20",
    data={"fps_workers": 51, "fps_wp": 40, "changes": 6800},
)
RAMSEY_1927 = Table(
    key="ramsey_1927",
    cite="F. P. Ramsey, \"A Contribution to the Theory of Taxation\", Economic Journal 37(145): 47-61 (1927); P. A. "
         "Diamond and J. A. Mirrlees, \"Optimal Taxation and Public Production\", American Economic Review 61(1, 3) "
         "(1971); A. B. Atkinson and J. E. Stiglitz, \"The Design of Tax Structure: Direct versus Indirect "
         "Taxation\", Journal of Public Economics 6: 55-75 (1976)",
    tag="Ramsey (1927); \\ Diamond and Mirrlees (1971); \\ Atkinson and Stiglitz (1976)",
    where="Ramsey: taxes on goods should cut every good's demand by the same proportion, which for independent "
          "demands means rates inversely proportional to the elasticities; Diamond and Mirrlees: an optimal system "
          "keeps production efficient, so it does not tax intermediate goods; Atkinson and Stiglitz: with a good "
          "income tax and separable preferences, differential commodity taxes are not needed",
    read="the papers' results as stated in Salanie, The Economics of Taxation",
    checked="2026-11-20",
    data={},
)
MIRRLEES_1971 = Table(
    key="mirrlees_1971",
    cite="J. A. Mirrlees, \"An Exploration in the Theory of Optimum Income Taxation\", Review of Economic Studies "
         "38(2): 175-208 (1971); P. A. Diamond, \"Optimal Income Taxation: An Example with a U-Shaped Pattern of "
         "Optimal Marginal Tax Rates\", American Economic Review 88(1): 83-95 (1998); E. Saez, \"Using Elasticities "
         "to Derive Optimal Income Tax Rates\", Review of Economic Studies 68(1): 205-229 (2001); E. Saez, "
         "\"Optimal Income Transfer Programs: Intensive versus Extensive Labor Supply Responses\", Quarterly "
         "Journal of Economics 117(3): 1039-1073 (2002)",
    tag="Mirrlees (1971); \\ Diamond (1998); \\ Saez (2001, \\ 2002)",
    where="the government sees income, not ability, so taxes must respect incentive constraints; Diamond's formula "
          "for quasi-linear preferences and its U-shaped rates; Saez's top rate 1/(1 + a e) and the schedule in "
          "terms of elasticities and the income distribution; when responses are at the extensive margin, "
          "transfers that rise with earnings at the bottom (like the EITC) can be optimal",
    read="the abstracts and Diamond and Saez's 2011 survey",
    checked="2026-11-20",
    data={},
)
DIAMOND_SAEZ_2011 = Table(
    key="diamond_saez_2011",
    cite="P. Diamond and E. Saez, \"The Case for a Progressive Tax: From Basic Research to Policy "
         "Recommendations\", Journal of Economic Perspectives 25(4): 165-190 (2011); T. Piketty, E. Saez and S. "
         "Stantcheva, \"Optimal Taxation of Top Labor Incomes: A Tale of Three Elasticities\", American Economic "
         "Journal: Economic Policy 6(1): 230-271 (2014)",
    tag="Diamond and Saez, \\ \\emph{JEP} 25(4) (2011); \\ Piketty, \\ Saez and Stantcheva (2014)",
    where="with a Pareto parameter of 1.5 and an elasticity of 0.25, the revenue-maximizing top rate is 73% (all "
          "taxes combined); if part of top earners' response is bargaining over pay, the optimal top rate is higher",
    read="the formula and secondary summaries (Cato Journal, EPI); PSS's abstract",
    checked="2026-11-20",
    data={"a": 1.5, "e": 0.25, "rate": 73},
)
ETI_STUDIES = Table(
    key="eti_studies",
    cite="M. Feldstein, \"The Effect of Marginal Tax Rates on Taxable Income: A Panel Study of the 1986 Tax Reform "
         "Act\", Journal of Political Economy 103(3): 551-572 (1995); J. Gruber and E. Saez, \"The Elasticity of "
         "Taxable Income: Evidence and Implications\", Journal of Public Economics 84(1): 1-32 (2002); E. Saez, J. "
         "Slemrod and S. H. Giertz, \"The Elasticity of Taxable Income with Respect to Marginal Tax Rates: A Critical "
         "Review\", Journal of Economic Literature 50(1): 3-50 (2012)",
    tag="Feldstein (1995); \\ Gruber and Saez (2002); \\ Saez, \\ Slemrod and Giertz (2012)",
    where="Feldstein, from a Treasury panel of more than 4,000 returns around the 1986 reform: an elasticity of "
          "taxable income of at least one; Gruber and Saez, with more years and reforms: about 0.4; the review: "
          "the elasticity is not a fixed parameter but depends on the tax base and on enforcement, which policy "
          "chooses",
    read="the abstracts; Gruber and Saez's figure as summarized in later work",
    checked="2026-11-20",
    data={"feldstein": 1.0, "gruber_saez": 0.4, "panel": 4000},
)
BUNCHING = Table(
    key="bunching",
    cite="E. Saez, \"Do Taxpayers Bunch at Kink Points?\", American Economic Journal: Economic Policy 2(3): 180-212 "
         "(2010); H. J. Kleven and M. Waseem, \"Using Notches to Uncover Optimization Frictions and Structural "
         "Elasticities: Theory and Evidence from Pakistan\", Quarterly Journal of Economics 128(2): 669-723 (2013)",
    tag="Saez, \\ \\emph{AEJ: Policy} 2(3) (2010); \\ Kleven and Waseem, \\ \\emph{QJE} 128(2) (2013)",
    where="bunching at the first kink of the EITC, but only among the self-employed, whose income is self-reported; "
          "notches, where the average rate jumps, leave a hole that reveals how many taxpayers fail to optimize",
    read="the abstracts",
    checked="2026-11-20",
    data={},
)
CLK_2009 = Table(
    key="clk_2009",
    cite="R. Chetty, A. Looney and K. Kroft, \"Salience and Taxation: Theory and Evidence\", American Economic "
         "Review 99(4): 1145-1177 (2009)",
    tag="Chetty, \\ Looney and Kroft, \\ \\emph{AER} 99(4) (2009)",
    where="in a supermarket in early 2006, tags showing tax-inclusive prices on about 750 products (cosmetics, hair "
          "care, deodorants) for three weeks cut their sales by about 8% against control products and stores; the "
          "sales tax was 7.375%",
    read="the abstract and the working paper",
    checked="2026-11-20",
    data={"drop": 8, "tax": 7.375, "products": 750},
)
CAPITAL_TAX = Table(
    key="capital_tax",
    cite="C. Chamley, \"Optimal Taxation of Capital Income in General Equilibrium with Infinite Lives\", "
         "Econometrica 54(3): 607-622 (1986); K. L. Judd, \"Redistributive Taxation in a Simple Perfect Foresight "
         "Model\", Journal of Public Economics 28(1): 59-83 (1985); L. Straub and I. Werning, \"Positive Long-Run "
         "Capital Taxation: Chamley-Judd Revisited\", American Economic Review 110(1): 86-119 (2020)",
    tag="Chamley (1986); \\ Judd (1985); \\ Straub and Werning, \\ \\emph{AER} 110(1) (2020)",
    where="Chamley and Judd: the optimal tax on capital income is zero in the long run; Straub and Werning: in "
          "Judd's main model the long-run tax is positive and significant whenever the intertemporal elasticity "
          "of substitution is below one",
    read="the abstracts",
    checked="2026-11-20",
    data={},
)
HAVENS = Table(
    key="havens",
    cite="G. Zucman, \"The Missing Wealth of Nations: Are Europe and the U.S. Net Debtors or Net Creditors?\", "
         "Quarterly Journal of Economics 128(3): 1321-1364 (2013); T. Torslov, L. Wier and G. Zucman, \"The Missing "
         "Profits of Nations\", Review of Economic Studies 90(3): 1499-1534 (2023); OECD/G20 Inclusive Framework, "
         "Statement on a Two-Pillar Solution (8 October 2021)",
    tag="Zucman (2013); \\ T\\o{}rsl\\o{}v, \\ Wier and Zucman (2023); \\ OECD (2021)",
    where="about 8% of households' financial wealth is held in tax havens, mostly unrecorded; 36% of multinational "
          "profits were shifted to tax havens in 2015 (close to 40% in the working paper); 136 of 140 jurisdictions "
          "agreed a 15% global minimum tax on multinationals with revenue of 750 million euros or more",
    read="the abstracts; secondary reports of the OECD statement",
    checked="2026-11-20",
    data={"wealth": 8, "profits": 36, "minimum": 15, "countries": 136, "members": 140},
)
EVASION = Table(
    key="evasion",
    cite="M. G. Allingham and A. Sandmo, \"Income Tax Evasion: A Theoretical Analysis\", Journal of Public "
         "Economics 1(3-4): 323-338 (1972); H. J. Kleven, M. B. Knudsen, C. T. Kreiner, S. Pedersen and E. Saez, "
         "\"Unwilling or Unable to Cheat? Evidence from a Tax Audit Experiment in Denmark\", Econometrica 79(3): "
         "651-692 (2011)",
    tag="Allingham and Sandmo (1972); \\ Kleven et al., \\ \\emph{Econometrica} 79(3) (2011)",
    where="Denmark, 2007-08: about 42,800 taxpayers, half chosen at random for thorough audits; evasion was 0.3% of "
          "income that third parties report and 37% of self-reported income; prior audits and threat letters "
          "raised self-reported income",
    read="the NBER working paper's abstract (the published abstract states the pattern without the numbers)",
    checked="2026-11-20",
    data={"third_party": 0.3, "self": 37, "n": 42800},
)
FRONTIER41 = Table(
    key="frontier41",
    cite="H. J. Kleven, C. Landais and E. Saez, \"Taxation and International Migration of Superstars: Evidence from "
         "the European Football Market\", American Economic Review 103(5): 1892-1924 (2013)",
    tag="Kleven, \\ Landais and Saez, \\ \\emph{AER} 103(5) (2013)",
    where="in 14 European first leagues since 1985, the number of foreign players responds to the net-of-tax rate "
          "with an elasticity of about one, domestic players about 0.15",
    read="the abstract",
    checked="2026-11-20",
    data={"foreign": 1.0, "domestic": 0.15},
)
TCJA_2017 = Table(
    key="tcja_2017",
    cite="S. Mnuchin, remarks as quoted by the Joint Economic Committee (2017); Congressional Budget Office, The "
         "Budget and Economic Outlook: 2018 to 2028 (April 2018)",
    tag="Mnuchin (2017); \\ CBO (April 2018)",
    where="'not only will this tax plan pay for itself, but it will pay down debt'; CBO: the 2017 act adds about $1.9 "
          "trillion to deficits over 2018-2028, after a macroeconomic feedback of about $0.6 trillion and about $0.6 "
          "trillion of added interest",
    read="secondary reports quoting CBO's table and the remark",
    checked="2026-11-20",
    data={"cbo_total": 1.9, "feedback": 0.6, "interest": 0.6},
)
PART41 = (LAFFER_1974, HARBERGER_1962, RAMSEY_1927, MIRRLEES_1971, DIAMOND_SAEZ_2011, ETI_STUDIES, BUNCHING,
          CLK_2009, CAPITAL_TAX, HAVENS, EVASION, FRONTIER41, TCJA_2017)
PART7 = (BERNOULLI_1738, SAMUELSON_1937, ALLAIS_1953, ELLSBERG_1961, RABIN_2000, THALER_1981, HOLT_LAURY_2005,
         HAYDEN_PLATT_2009, MADRIAN_SHEA_2001, THALER_BENARTZI_2004, BARSKY_1997, POST_2008, MEHRA_PRESCOTT_1985)
ALL = {t.key: t for t in (*PART1, *PART3, *PART4, *PART5, *PART6, *PART7, *PART8, *PART9, *PART10, *PART11, *PART12, *PART13, *PART14, *PART15, *PART16, *PART17, *PART18, *PART19, *PART21, *PART22, *PART25, *PART26, *PART35, *PART36, *PART37, *PART38, *PART39, *PART40, *PART41)}
