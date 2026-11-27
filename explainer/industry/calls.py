"""Called it? (SYLLABUS §2.10): dated forecasts about each industry, other people's and this series' own.

Other people's calls are taken from dated primary documents (or the best surviving record of one) and shown with what
happened.  The series' own calls are logged with the date made, the rule that will score them and the date they come
due; a refresh scores the ones that have come due (SYLLABUS §7, phase 3).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Call:
    part: int
    who: str
    made: str          # ISO date (or month) the call was made
    claim: str
    source: str
    outcome: str = ""  # what happened, with its source; empty while pending
    rule: str = ""     # for the series' own calls: how it will be scored
    due: str = ""      # when it can be scored
    ours: bool = False


CALLS = [
    Call(1, "Steve Ballmer, chief executive of Microsoft", "2007-04",
         "\"There's no chance that the iPhone is going to get any significant market share. No chance.\"",
         "USA Today CEO Forum, 2007-04-29, as quoted by MacRumors 2007-04-30",
         outcome="Apple's share of smartphone shipments was 19.7% in 2025 (IDC) and its iPhone sales $254.1bn in "
                 "fiscal 2026 (10-K): about a fifth of the phones and most of the industry's profit"),
    Call(1, "Industry, Built", "2026-11-23",
         "Smartphone shipments worldwide in calendar 2026 will be below 1.15 billion (2025: 1.26 billion).",
         "This series, Part 1, chapter 15; reasoning: IDC's -7.4% in Q2 and Counterpoint's -20% in Q3 2026",
         rule="IDC's first full-year release for 2026 (preliminary figure); true if below 1,150 million",
         due="2027-01", ours=True),
    Call(2, "Wassily Leontief", "1983",
         "\"The role of humans as the most important factor of production is bound to diminish in the same way that "
         "the role of horses in agricultural production was first diminished and then eliminated by the introduction "
         "of tractors.\"", "Leontief (1983), in The Long-Term Impact of Technology on Employment and Unemployment, "
                          "National Academy of Engineering, p. 3",
         outcome="US payroll employment rose from 90.3 million (1983) to 158.4 million (2025) (BLS via FRED); the "
                 "work moved between industries rather than disappearing, so far"),
    Call(2, "Industry, Built", "2026-11-23",
         "In 2030, health care and social assistance will employ more people than manufacturing and retail trade "
         "combined (2025: 23.3 million against 28.1 million). Probability: 40%.",
         "This series, Part 2, chapter 18; health care added about 0.78 million jobs in 2025, manufacturing and "
         "retail were flat",
         rule="BLS Current Employment Statistics annual averages for 2030: CES6562000001 against MANEMP + USTRADE",
         due="2031-02", ours=True),
    Call(3, "Bethany McLean, Fortune", "2001-03-05",
         "\"How exactly does Enron make its money?\" Enron trades at about 55 times earnings, earns about 7% on its "
         "invested capital, and its operating cash flow fell to $100 million in the first nine months of 2000.",
         "Fortune, \"Is Enron Overpriced?\", 5 March 2001",
         outcome="Enron restated 1997-2000 net income down by $591m (Form 8-K, 8 November 2001) and filed for "
                 "chapter 11 on 2 December 2001 (Form 8-K, 17 December 2001)"),
    Call(3, "Industry, Built", "2026-11-23",
         "Microsoft's free cash flow in fiscal 2027 (operating cash flow less additions to property and equipment) "
         "will be below fiscal 2026's $67.0bn, while its operating income rises above fiscal 2026's $155.2bn. "
         "Probability: 65%.",
         "This series, Part 3, chapter 14; Q1 FY2027 free cash $18.6bn against $25.7bn a year earlier; capex "
         "guidance about $170bn including finance leases",
         rule="Microsoft Form 10-K FY2027, cash-flow statement and income statement: both conditions must hold",
         due="2027-08", ours=True),
    Call(4, "International Energy Agency", "2010-05-11",
         "World solar photovoltaic capacity \"could reach\" 200 GW in 2020, 900 GW in 2030 and 2,000 GW in 2040.",
         "IEA, Technology Roadmap: Solar Photovoltaic Energy (2010), foldout",
         outcome="721 GW were installed by 2020 and 2,397 GW by 2025 (IRENA, via Our World in Data): the roadmap's "
                 "2040 figure was passed fifteen years early"),
    Call(4, "Industry, Built", "2026-11-23",
         "In at least one calendar month of 2027, US utility-scale solar plants will generate more electricity than "
         "US coal plants (electric power sector). Probability: 55%.",
         "This series, Part 4, chapter 12; EIA's November 2026 outlook puts April-June 2027 at 126.0 TWh of solar "
         "against 135.0 TWh of coal, and solar's spring peak meets coal's spring maintenance",
         rule="EIA Electric Power Monthly, net generation by source, electric power sector, final 2027 data: true if "
              "utility-scale solar exceeds coal in any month of 2027",
         due="2028-03", ours=True),
    Call(5, "Warren Buffett, Berkshire Hathaway", "2008-02",
         "Airlines are \"the worst sort of business\": they grow fast, need capital to grow, \"and then earn little or "
         "no money\"; \"a durable competitive advantage has proven elusive ever since the days of the Wright "
         "Brothers.\"", "Berkshire Hathaway, letter to shareholders for 2007, p. 8",
         outcome="Damodaran's figures for US airlines, 2015-2025: return on capital averaged 6.5% a year against an "
                 "average cost of capital of 6.0%: high after consolidation (14-19% in 2015-2019), losses in 2020 "
                 "and 2021, about 8% since"),
    Call(5, "Industry, Built", "2026-11-24",
         "At least seven of the ten US industries with the highest return on capital in Aswath Damodaran's table "
         "for 2025 will be among the twenty highest in his table for 2028. Probability: 75%.",
         "This series, Part 5, chapter 16; in his tables for 2015-2025, seven or more of a year's top ten were in the "
         "top twenty three years later in 7 of 8 windows",
         rule="Damodaran's 'Excess Returns (EVA) by industry, US companies' for 2028, published January 2029: count "
              "the 2025 top ten (by return on capital) among the 2028 top twenty; a renamed or dropped industry "
              "counts as a miss",
         due="2029-01", ours=True),
    Call(6, "Intel (Pat Gelsinger, chief executive)", "2021-03-23",
         "\"IDM 2.0\": Intel would build its way back to leadership, starting with an estimated $20 billion for two "
         "new chip factories in Arizona, announced in the middle of the 2021 chip shortage.",
         "Intel press release, 23 March 2021",
         outcome="Intel's capital spending rose from $14.3bn (2020) to $25.8bn (2023); its operating income fell from "
                 "$19.5bn (2021) to a loss of $11.7bn (2024), and it cut spending to $14.6bn in 2025 (Forms 10-K)"),
    Call(6, "Industry, Built", "2026-11-24",
         "Before the end of 2028, Micron will report a quarter whose revenue is at least 25% below its highest "
         "earlier quarter (so far $54.2bn, the quarter to 3 September 2026). Probability: 55%.",
         "This series, Part 6, chapter 16; after each of Micron's four earlier peaks since 2010, quarterly revenue "
         "fell by 21%, 37%, 43% and 57% within two years; spending was 3.2 times depreciation in fiscal 2026",
         rule="Micron's Forms 10-Q and 10-K: for every fiscal quarter ending on or before 31 December 2028, compare "
              "its three-month revenue with the highest of all earlier quarters; true if any is 25% or more below",
         due="2029-01", ours=True),
    Call(7, "Beverage Marketing Corporation", "2025-05",
         "US bottled water consumption per person (47.3 gallons in 2024) will reach about 50 gallons 'by the end of "
         "this decade or the start of the next'.",
         "Beverage Marketing Corporation, news release, May 2025",
         outcome="pending: 46.4 gallons in 2023, 47.3 in 2024 (the same release)"),
    Call(7, "Industry, Built", "2026-11-24",
         "The Census Bureau's shipments of US bottled water manufacturers for 2026 will be above $7.5bn (2024: $7.46bn). "
         "Probability: 65%.",
         "This series, Part 7, chapter 14; reasoning: volume growing about 2% a year (Beverage Marketing), producer "
         "prices flat since 2023, against a series that fell from $8.7bn to $7.2bn in 2023",
         rule="the Annual Integrated Economic Survey's first published figure for 2026 (FRED AIES312112RCTUS); true if "
              "above 7,500,000 thousand dollars",
         due="2028-06", ours=True),
    Call(8, "M. King Hubbert, Shell Development Company", "1956-03",
         "US crude oil production 'must culminate at about 1965' if the ultimate is 150 billion barrels, or 'about "
         "1970' if it is 200 billion; world production would peak 'at about the year 2000'.",
         "Hubbert, 'Nuclear Energy and the Fossil Fuels', American Petroleum Institute, San Antonio, March 1956",
         outcome="US production peaked in 1970 at 9.64m b/d and fell to 5.0m b/d in 2008; shale then took it to 13.66m "
                 "b/d in 2025, and cumulative output passed 258bn barrels. World crude output reached 84.5m b/d in "
                 "2025 (EIA). Right on the date of the US peak, wrong on the ultimate and on the world."),
    Call(8, "Industry, Built", "2026-11-24",
         "Brent crude will average less than $90 a barrel in 2027 (EIA's November 2026 forecast: $86). Probability: 60%.",
         "This series, Part 8, chapter 16; reasoning: shut-ins down from 10.9m b/d (May) to 2.5m (October), demand "
         "recovering, stocks to be rebuilt; against: the strait's flows remain at risk, and stocks are low",
         rule="EIA's annual average Europe Brent spot price FOB for 2027 (series RBRTE), as first published; true if "
              "below $90.00",
         due="2028-01", ours=True),
    Call(9, "Paul Ehrlich (with John Harte and John Holdren)", "1980-09-29",
         "A basket of $200 each of chromium, copper, nickel, tin and tungsten, bought in 1980, would be worth more, after "
         "inflation, in 1990: the metals would grow scarcer.",
         "Paul Sabin, The Bet (Yale, 2013); the wager with Julian Simon was formalized on 29 September 1980",
         outcome="All five real prices fell; in October 1990 Ehrlich mailed Simon a cheque for $576.07. On USGS's yearly "
                 "unit values the basket fell to about $625 in 1980 dollars; over every ten-year window from 1900-1910 to "
                 "2009-2019, Ehrlich would have won 61% of the time."),
    Call(9, "Industry, Built", "2026-11-24",
         "Escondida will produce less than 1,100 thousand tonnes of copper in BHP's fiscal year to June 2027 (FY2025: "
         "1,305 kt; FY2026 guidance 1,150-1,250 kt). Probability: 75%.",
         "This series, Part 9, chapter 14; reasoning: the feed grade falls from 1.02% to about 0.85% in FY2026 and BHP's "
         "medium-term outlook is 900-1,000 kt a year for FY2027-FY2031; against: leaching and higher throughput beat "
         "expectations in FY2025",
         rule="BHP's operational review or annual report for the year to 30 June 2027: Escondida copper production, 100% "
              "basis; true if below 1,100 kt",
         due="2027-08", ours=True),
    Call(10, "Paul Ehrlich", "1968",
         "\"The battle to feed all of humanity is over.\" The Population Bomb predicted that hundreds of millions of "
         "people would starve to death in the coming decades, whatever crash programmes were started.",
         "Paul R. Ehrlich, The Population Bomb (Ballantine, 1968); Smithsonian Magazine (January 2018)",
         outcome="Food supply per person rose: the world's from about 2,180 kilocalories a day in 1961 to about 3,010 in "
                 "2024, India's from about 2,060 to 2,720 and China's from about 1,430 to 3,500 (FAO via Our World in "
                 "Data), while the world's population more than doubled. Famines still struck, but nothing on the "
                 "predicted scale."),
    Call(10, "Industry, Built", "2026-11-27",
         "In USDA's next food dollar release (covering 2026), the farm share of the US food dollar for 2026 will be "
         "higher than for 2025 in the same release (12.6 cents in the November 2026 release). Probability: 70%.",
         "This series, Part 10, chapter 14; reasoning: the world prices of maize, wheat, soybeans and beef averaged 5-18% "
         "more in January-September 2026 than a year earlier, and the farm share has moved with farm prices; against: "
         "the shift of spending to restaurants, and revisions",
         rule="USDA ERS Food Dollar Series, release covering 2026 (expected late 2027): all-food farm share, 2026 against "
              "2025 in that same release; true if 2026 is higher",
         due="2027-12", ours=True),
]


def calls(part: int | None = None, ours: bool | None = None) -> list[Call]:
    return [c for c in CALLS if (part is None or c.part == part) and (ours is None or c.ours == ours)]
