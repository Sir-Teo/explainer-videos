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
    where="pp. 111-114 (the design); the experiments ran over six years from 1955",
    read="the JSTOR copy",
    checked="2026-11-18",
    data={
        "began": 1955,
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
ALL = {t.key: t for t in PART1}
