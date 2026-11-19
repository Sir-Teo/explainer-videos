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
ALL = {t.key: t for t in (*PART1, *PART3, *PART4, *PART5, *PART6)}
