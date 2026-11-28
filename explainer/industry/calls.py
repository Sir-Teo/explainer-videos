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
    Call(11, "World Steel Association, Short Range Outlooks", "2022-10",
         "Each October, a forecast of China's steel demand for the year ahead: flat in 2023 (October 2022), flat in 2024 "
         "(October 2023), down 1.0% in 2025 (October 2024), down 1.0% in 2026 (October 2025).",
         "worldsteel press releases of 19 October 2022, 17 October 2023, 14 October 2024 and 13 October 2025",
         outcome="China's apparent steel use fell 2.3% in 2023, 5.4% in 2024 and 7.1% in 2025 (World Steel in Figures "
                 "2026; worldsteel itself cites 'a 7.1% contraction' for 2025 in April 2026): each year-ahead forecast was "
                 "too high, and in October 2026 the 2026 forecast was cut to -2.0%"),
    Call(11, "Industry, Built", "2026-11-27",
         "When worldsteel publishes China's steel demand for 2026 (its April 2027 Short Range Outlook), it will show a "
         "fall of more than 2.0%, the figure it forecast in October 2026. Probability: 70%.",
         "This series, Part 11, chapter 14; reasoning: the October forecasts were too high three years running, and "
         "China's crude steel output was 2.8% lower in January-October 2026 than a year before (worldsteel, 24 November "
         "2026); against: exports and manufacturing holding up, and revisions",
         rule="worldsteel Short Range Outlook, April 2027: the change in China's steel demand (apparent use of finished "
              "steel) in 2026; true if below -2.0%", due="2027-04", ours=True),
    Call(12, "US Energy Information Administration, Annual Energy Outlook 2005", "2005-02",
         "Projections for 2025: US net imports of LNG rising from 0.4 trillion cubic feet (2003) to 6.4; bulk chemical "
         "output growing 1.0% a year (1.7% in AEO2004); agricultural chemicals, nitrogen fertilizers included, 0.6% a "
         "year (cut from 1.3%) because of 'increased competition from foreign suppliers due to relatively high U.S. "
         "natural gas prices'.", "EIA, Annual Energy Outlook 2005 (DOE/EIA-0383(2005))",
         outcome="America exported 5.5 trillion cubic feet of LNG in 2025 (EIA); US ammonia output grew 2.3% a year, "
                 "2003-2025 (USGS); the Federal Reserve's index of basic chemicals 0.5% a year, plastics and resins 0.0%, "
                 "all chemicals -0.1%: right that bulk chemicals would grow slowly, wrong about the gas that would "
                 "bring fertilizer back"),
    Call(12, "Industry, Built", "2026-11-27",
         "Germany's chemical output (Eurostat, manufacture of chemicals, C20, seasonally and calendar adjusted, "
         "2021 = 100) will average below 79.8 in 2027, at least 20% below its 2021 level. Probability: 75%.",
         "This series, Part 12, chapter 13; reasoning: European gas at about eight times America's in September 2026, "
         "the index at 77.0 that month and closures announced (Dow's Böhlen cracker by the end of 2027); against: "
         "a fall in gas prices, a recovery in demand, revisions",
         rule="Eurostat sts_inpr_m, C20, Germany, SCA, I21: the mean of the twelve monthly values for 2027 as first "
              "published in full; true if below 79.8",
         due="2028-03", ours=True),
    Call(13, "US Energy Information Administration, Annual Energy Outlook 2005", "2005-02",
         "Total US electricity consumption, purchases and on-site generation, rising from 3,657 billion kWh in 2003 to "
         "5,467 billion in 2025 (1.8% a year), led by 'rapid growth in electricity use for computers, office equipment, "
         "and a variety of electrical appliances'.", "EIA, Annual Energy Outlook 2005 (DOE/EIA-0383(2005))",
         outcome="US electricity end use was 4,195 billion kWh in 2025 (EIA, Monthly Energy Review, Table 7.6): growth of "
                 "0.6% a year, and sales were flat from 2007 to 2021; growth returned from 2022, with data centres"),
    Call(13, "Industry, Built", "2026-11-27",
         "US retail sales of electricity in 2027 will be more than 1.5% above 2026's. Probability: 65%.",
         "This series, Part 13, chapter 13; reasoning: sales grew 2.6% in 2024, 2.1% in 2025 and 2.0% in January-August "
         "2026 (EIA), with data centres' use projected at 325-580 TWh by 2028 (LBNL for DOE) and utilities' capital "
         "spending rising; against: weather, a slowdown, efficiency, delays in connecting new load",
         rule="EIA, Monthly Energy Review, Table 7.6, total retail sales (ESTCPUS), the first annual figures for 2027 and "
              "2026 as published together; true if 2027 exceeds 2026 by more than 1.5%",
         due="2028-03", ours=True),
    Call(14, "US Environmental Protection Agency", "1989-02",
         "\"One-third of the nation's landfills will be full by 1991\"; \"we're running out of space to bury it in "
         "existing landfills\".", "EPA, The Solid Waste Dilemma: An Agenda for Action (EPA/530-SW-89-019, February 1989)",
         outcome="Small landfills did close: 7,924 in 1988, 1,908 in 2009 (EPA, 2009 Facts and Figures, which found that "
                 "'at the national level, capacity does not appear to be a problem'). But the tonnage landfilled stayed "
                 "near 140 million tons a year to 2018 (EPA), in fewer, larger, lined landfills; in 2025 Waste "
                 "Management reported about 38 years of permitted life and Republic as much airspace at the end of the "
                 "year as at the start (Forms 10-K)"),
    Call(14, "Industry, Built", "2026-11-27",
         "The US consumer price index for water and sewerage maintenance will average more than 4.0% higher in 2027 "
         "than in 2026. Probability: 70%.",
         "This series, Part 14, chapter 13; reasoning: the index has never fallen since 1953, rose 4.2-5.2% a year in "
         "2022-2025 and 4.9% in January-September 2026 over a year earlier (BLS), with $625bn of drinking water and "
         "$630bn of clean water needs (EPA) to be paid through bills; against: lower general inflation, as in "
         "2017-2021 when it rose 3.1-3.7% a year",
         rule="BLS, CPI-U, US city average, not seasonally adjusted, CUUR0000SEHG01: the annual average for 2027 against "
              "2026's as first published together; true if more than 4.0% higher",
         due="2028-01", ours=True),
    Call(15, "Gordon E. Moore, Fairchild Semiconductor", "1965-04-19",
         "\"The complexity for minimum component costs has increased at a rate of roughly a factor of two per year ... "
         "by 1975, the number of components per integrated circuit for minimum cost will be 65,000.\"",
         "G. E. Moore, 'Cramming more components onto integrated circuits', Electronics 38 (8), 19 April 1965",
         outcome="In 1975 Moore plotted a 16,384-bit charge-coupled memory chip at the complexity the annual doubling "
                 "predicted, and revised the slope to a doubling every two years ('Progress in Digital Integrated "
                 "Electronics', IEDM 1975); transistors per microprocessor then doubled about every 2.0 years from 1971 "
                 "to 2021 (Rupp, via Our World in Data)"),
    Call(15, "World Semiconductor Trade Statistics (WSTS)", "2025-12",
         "World semiconductor sales in 2026 of $975.5 billion, up 26.3% ('Global Semiconductor Market Approaches $1T in "
         "2026'), with memory at $294.8 billion.", "WSTS, Autumn 2025 forecast (released December 2025)",
         outcome="Sales were $702 billion in the first half of 2026 (WSTS) and $517.7 billion in the third quarter (SIA, "
                 "3 November 2026): $1.22 trillion by September. WSTS raised its 2026 forecast to $1,511 billion in May "
                 "and $1,655 billion in August 2026; its May forecast for memory was $803.9 billion"),
    Call(15, "Industry, Built", "2026-11-27",
         "World semiconductor sales in 2026, as WSTS first reports the full year, will be more than $1.8 trillion. "
         "Probability: 65%.",
         "This series, Part 15, chapter 13; reasoning: $1,219.7 billion was sold by September (WSTS's first half plus "
         "SIA's third quarter), so the fourth quarter needs about $580 billion, 12% more than the third, after growth of "
         "more than 20% a quarter for three quarters (SIA); against: memory booms end abruptly, and buyers who stocked "
         "up early stop ordering",
         rule="WSTS's first release of world semiconductor sales for the calendar year 2026 (its Q4 release, or SIA's "
              "annual release of WSTS data); true if above $1,800 billion",
         due="2027-03", ours=True),
    Call(16, "Howard Lutnick, US Secretary of Commerce", "2025-04-06",
         "\"The army of millions and millions of human beings screwing in little- little screws to make iPhones, that "
         "kind of thing is going to come to America. It's going to be automated.\"",
         "CBS News, transcript of Face the Nation with Margaret Brennan, 6 April 2025",
         outcome="US imports of smartphones were $52.4bn in 2025 against $51.5bn in 2024 (UN Comtrade, HS 851713), from "
                 "China $23.7bn (2024: $41.7bn) and from India $22.1bn (2024: $7.0bn); US employment in computer and "
                 "electronic products manufacturing averaged 1.00 million in 2025 against 1.03 million in 2024 (BLS). "
                 "Not so far: assembly moved to India, not to America"),
    Call(16, "Industry, Built", "2026-11-27",
         "India will supply more than half of the United States' smartphone imports, by value, in calendar 2026. "
         "Probability: 55%.",
         "This series, Part 16, chapter 13; reasoning: India supplied 58% from January to August 2026 (UN Comtrade), but "
         "in September-December 2025 China supplied most of the launch months; if those months repeat, the year ends near "
         "50.1%",
         rule="UN Comtrade, reporter United States, imports, HS 851713, annual 2026: partner India over partner World, as "
              "first published; true if above 50%",
         due="2027-06", ours=True),
    Call(17, "Tesla Motors", "2016-05-04",
         "\"we have decided to advance our 500,000 total unit build plan (combined for Model S, Model X, and Model 3) to "
         "2018, two years earlier than previously planned\"",
         "Tesla Motors, First Quarter 2016 Update (Form 8-K, Exhibit 99.1, filed 4 May 2016)",
         outcome="Tesla produced 254,530 vehicles in 2018 and 509,737 in 2020 (Forms 10-K): the plan was met on its "
                 "original date, two years after the accelerated one"),
    Call(17, "US Energy Information Administration", "2017-01",
         "Battery electric and plug-in hybrid vehicles would be 3.7% of new US light-vehicle sales in 2020 and 8.4% in "
         "2025 (Annual Energy Outlook 2017, Reference case)",
         "EIA, Annual Energy Outlook 2017, supplement table 39",
         outcome="2.3% in 2020 and 10% in 2025 (IEA, Global EV Outlook 2026): too high early, too low late, close in the end"),
    Call(17, "China's Ministry of Industry and Information Technology, NDRC and MOST", "2017-04-06",
         "New energy vehicle production and sales of 2 million a year by 2020; above 20% of vehicle production and sales by "
         "2025 (restated by the State Council in October 2020 as 'about 20%' of new vehicle sales)",
         "汽车产业中长期发展规划 (工信部联装〔2017〕53号); 新能源汽车产业发展规划（2021—2035年） (国办发〔2020〕39号)",
         outcome="1.37 million in 2020 and 47.9% of sales in 2025 (CAAM, via the China Securities Journal and Xinhua): short "
                 "at first, then more than twice the target"),
    Call(17, "Industry, Built", "2026-11-27",
         "The electric share of new cars sold worldwide in 2026, as the IEA counts it, will be below 32%, the figure a "
         "logistic curve fitted to 2021-2025 points to (2025: 25%). Probability: 65%.",
         "This series, Part 17, chapter 15; reasoning: China is already above half of sales, the US repealed its tax "
         "credits in 2025, and the fitted curve ran ahead of the actual figure for 2025",
         rule="IEA, Global EV Outlook 2027 (or its data explorer), world electric car sales share for 2026 as first "
              "published; true if below 32%",
         due="2027-06", ours=True),
    Call(18, "The Boeing Company", "2006-02",
         "\"In early 2004, we received the initial launch order for the 787 ... Entry into service is targeted for 2008.\"",
         "The Boeing Company, Form 10-K 2005",
         outcome="\"We delivered the first 787-8 airplane in September 2011\" (Form 10-K 2011): three years late"),
    Call(18, "The Boeing Company", "2014-02",
         "\"In November 2013 we launched the 777X and first delivery is expected in 2020.\"",
         "The Boeing Company, Form 10-K 2013",
         outcome="Not delivered by November 2026; 'We continue to expect first delivery of the 777-9 to occur in 2027' (Form "
                 "10-Q, third quarter of 2026), after reach-forward losses of $3.5bn in 2024 and $4.9bn in 2025"),
    Call(18, "Industry, Built", "2026-11-27",
         "Boeing will deliver its first 777-9 to a customer by 31 December 2027, as it now expects. Probability: 55%.",
         "This series, Part 18, chapter 13; reasoning: Boeing's last two new-model targets slipped three and seven years, "
         "but this one is a year away, with the final phases of flight testing expected to be approved by the end of 2026 "
         "and an engine durability fix still to certify",
         rule="The Boeing Company, Form 10-K 2027: true if it reports one or more 777X (777-9) deliveries in 2027 or a first "
              "777-9 delivery dated in 2027",
         due="2028-02", ours=True),
    Call(19, "International Federation of Robotics", "2022-10-13",
         "\"global robot installations are expected to grow by 10% to almost 570,000 units in 2022 ... From 2022 to 2025, "
         "average annual growth rates in the medium to upper single-digit range are forecast\"",
         "IFR press release, 13 October 2022 (World Robotics 2022)",
         outcome="552,946 robots installed in 2022 (IFR, 24 September 2024), 3% short; 'more than 600,000' in 2025 (IFR, 24 "
                 "September 2026), below the 660,000 to 740,000 the growth range implied"),
    Call(19, "International Federation of Robotics", "2024-09-24",
         "\"Global robot installations are expected to level off at 541,000 units\" in 2024",
         "IFR press release, 24 September 2024 (World Robotics 2024)",
         outcome="About 542,000 installed in 2024 (IFR via the AI Index Report 2026): right on"),
    Call(19, "Industry, Built", "2026-11-27",
         "World installations of industrial robots in 2026 will come in below the IFR's forecast of 655,000. Probability: 55%.",
         "This series, Part 19, chapter 11; reasoning: the IFR's medium-term forecast of 2022 ran high and Japan and Germany "
         "bought fewer robots in 2025, but its one-year forecasts have been close and China's installations rose 20%",
         rule="IFR, World Robotics press release of autumn 2027: world installations in 2026 as first published; true if "
              "below 655,000",
         due="2027-10", ours=True),
    Call(20, "Eli Lilly and Company", "2025-02-06",
         "\"2025 guidance issued with revenue in the range of $58.0 billion to $61.0 billion\"",
         "Eli Lilly and Company, Form 8-K of 6 February 2025 (Exhibit 99, fourth-quarter 2024 results)",
         outcome="Revenue of $65.179bn in 2025 (Form 10-K 2025), 6.9% above the top of the range"),
    Call(20, "Eli Lilly and Company", "2026-02-04",
         "\"2026 guidance issued with revenue in the range of $80 billion to $83 billion\"",
         "Eli Lilly and Company, Form 8-K of 4 February 2026 (Exhibit 99, fourth-quarter 2025 results)",
         outcome="Pending; raised to $91.0 billion to $92.0 billion on 29 October 2026 (Form 8-K, Exhibit 99), after "
                 "third-quarter revenue of $24.397bn, up 39%"),
    Call(20, "Industry, Built", "2026-11-27",
         "Eli Lilly's revenue for 2026 will be at least $92.0 billion, the top of its raised range. Probability: 55%.",
         "This series, Part 20, chapter 12; reasoning: Lilly beat the top of its 2025 range by 7% and has raised its 2026 "
         "range twice, but a raise in late October leaves one quarter to surprise and its realized US prices are falling",
         rule="Eli Lilly and Company, Form 8-K with its fourth-quarter 2026 results or Form 10-K 2026: total revenue for 2026 "
              "as first reported; true if $92.0 billion or more",
         due="2027-02", ours=True),
    Call(21, "Intuitive Surgical", "2025-01-23",
         "\"The Company expects worldwide da Vinci procedures to increase approximately 13% to 16% in 2025\"",
         "Intuitive Surgical, Inc., Form 8-K of 23 January 2025 (Exhibit 99.1, fourth-quarter 2024 results)",
         outcome="Approximately 18% growth, 3,153,000 procedures (Form 10-K 2025): above the top of the range"),
    Call(21, "Intuitive Surgical", "2026-01-22",
         "\"Worldwide da Vinci procedure growth of approximately 13% to 15% in 2026\"",
         "Intuitive Surgical, Inc., Form 8-K of 22 January 2026 (Exhibit 99.1, fourth-quarter 2025 results)",
         outcome="Pending; narrowed to 14% to 15% on 20 October 2026, 'closer to the midpoint', after nine months at about "
                 "15% and a third quarter at about 14%"),
    Call(21, "Industry, Built", "2026-11-27",
         "Intuitive will report worldwide da Vinci procedure growth of 15% or more for 2026. Probability: 45%.",
         "This series, Part 21, chapter 11; reasoning: nine months grew about 15% and Intuitive beat its 2025 range, but the "
         "third quarter slowed to 14% and the company points to the middle of a 14-15% range",
         rule="Intuitive Surgical, Form 8-K with its fourth-quarter 2026 results (January 2027): worldwide da Vinci procedure "
              "growth for 2026 as it reports it; true if 15% or more",
         due="2027-01", ours=True),
    Call(22, "The Procter & Gamble Company", "2024-07-30",
         "\"The Company expects organic sales growth in the range of three to five percent\" for fiscal 2025",
         "The Procter & Gamble Company, Form 8-K of 30 July 2024 (Exhibit 99.1)",
         outcome="Organic sales up 2% in fiscal 2025 (Form 10-K for fiscal 2025): below the bottom of the range"),
    Call(22, "The Procter & Gamble Company", "2025-07-29",
         "\"The Company expects organic sales growth in the range of flat to up four percent\" for fiscal 2026",
         "The Procter & Gamble Company, Form 8-K of 29 July 2025 (Exhibit 99.1)",
         outcome="Organic sales up 1% in fiscal 2026 (Form 10-K for fiscal 2026): inside the range, in its lower half"),
    Call(22, "The Procter & Gamble Company", "2026-07-29",
         "\"The Company also expects organic sales growth in the range of one to three percent\" for fiscal 2027",
         "The Procter & Gamble Company, Form 8-K of 29 July 2026 (Exhibit 99.1)",
         outcome="Pending; first quarter of fiscal 2027 up 4% organically, guidance maintained (Form 8-K of 22 October 2026)"),
    Call(22, "Industry, Built", "2026-11-27",
         "P&G's organic sales growth for fiscal 2027 will be 3% or more, the top of its range. Probability: 40%.",
         "This series, Part 22, chapter 10; reasoning: a 4% first quarter with volume back, but about $1 billion after tax "
         "of higher costs, a forecast left unchanged, and two years at or below the lower part of its range",
         rule="The Procter & Gamble Company, Form 8-K with its fiscal 2027 results or Form 10-K for fiscal 2027: organic "
              "sales growth for the year as reported; true if 3% or more",
         due="2027-08", ours=True),
    Call(23, "Industria de Diseño Textil (Inditex)", "2026-03",
         "\"For 2026, Inditex expects a stable gross margin (+/-50 bps)\", against 58.3% in FY2025",
         "Inditex, FY2025 results (to 31 January 2026)",
         outcome="Pending; gross margin of 58.7% in 1H2026, 40 basis points above 1H2025, guidance repeated (interim 1H2026 "
                 "results)"),
    Call(23, "Industry, Built", "2026-11-27",
         "Inditex's gross margin for FY2026, the year to January 2027, will be 58.5% or more. Probability: 55%.",
         "This series, Part 23, chapter 11; reasoning: the first half ran at 58.7%, up 40 basis points, and the second half "
         "needs about 58.3% if its sales grow as the first half's did, about last year's 58.2%; but the second half holds "
         "the winter sale, whose quarter ran at 54.8% last year, and 58.5% sits near the top of the guidance",
         rule="Inditex, FY2026 results (March 2027): gross margin for the year as reported; true if 58.5% or more",
         due="2027-03", ours=True),
    Call(24, "California High-Speed Rail Authority", "2008-11",
         "The backbone from Los Angeles and Anaheim to San Francisco 'is expected to cost about $33 billion, in 2008 dollars'",
         "California High-Speed Rail Authority, Business Plan, November 2008",
         outcome="The 2026 Business Plan puts Phase 1 at $126.1 billion by a cheaper route, finished in 2039 with full service "
                 "in 2040, and the full buildout as first designed at about $231.3 billion in today's dollars; the first "
                 "stretch, Merced to Bakersfield, at $35.7 billion, finished in 2032"),
    Call(24, "California High-Speed Rail Authority", "2026-06",
         "Merced to Bakersfield: completion in 2032, 2033 the first full year of service",
         "California High-Speed Rail Authority, 2026 Business Plan",
         outcome="Pending; the 2026 plan moved completion back a year; 81 of 119 Central Valley miles built and ready for rail"),
    Call(24, "Industry, Built", "2026-11-27",
         "California's high-speed trains will not carry fare-paying passengers between Merced and Bakersfield before 1 "
         "January 2034. Probability: 70%.",
         "This series, Part 24, chapter 10; reasoning: about one large project in ten is on schedule (Flyvbjerg); the "
         "segment was moved back a year in 2026; track, electrification and trains were still to be procured; against: 81 "
         "of 119 miles of guideway built",
         rule="The California High-Speed Rail Authority's own reports at the end of 2033: true if no fare-paying passenger "
              "service between Merced and Bakersfield has begun before 1 January 2034",
         due="2034-01", ours=True),
    Call(25, "D.R. Horton", "2025-10-28",
         "For fiscal 2026: consolidated revenues of $33.5 billion to $35.0 billion and 86,000 to 88,000 homes closed",
         "D.R. Horton, Inc., Form 8-K of 28 October 2025",
         outcome="Missed: 84,202 homes closed and consolidated revenues of $33.0 billion in fiscal 2026 (Form 8-K of 29 October "
                 "2026); fiscal 2027 guided to 79,000-84,000 homes and $30-32 billion"),
    Call(25, "Fannie Mae", "2026-02",
         "Total single-family mortgage originations will increase from about $1.94 trillion in 2025 'by approximately 24%' "
         "in 2026, to about $2.41 trillion, refinancings from $560 billion to $917 billion",
         "Fannie Mae, Form 10-K for 2025",
         outcome="Pending; the thirty-year rate averaged about 6.1% in the first quarter of 2026, then rose above 7% in October "
                 "(Freddie Mac via FRED)"),
    Call(25, "Industry, Built", "2026-11-27",
         "D.R. Horton will close fewer than 81,500 homes in fiscal 2027, the year to 30 September 2027, the middle of its "
         "own guided range. Probability: 60%.",
         "This series, Part 25, chapter 9; reasoning: it closed 84,202 homes in fiscal 2026, below the bottom of its range; "
         "fourth-quarter orders fell 7% to 18,619; the thirty-year rate passed 7% in October 2026; against: the range was "
         "already cut, and it held its volume in a year it called challenging",
         rule="D.R. Horton's fiscal 2027 results (Form 8-K, October 2027): homes closed as reported; true if fewer than 81,500",
         due="2027-10", ours=True),
    Call(26, "The We Company (WeWork)", "2019-08-14",
         "'Among the approximately 255 million potential members across our 280 target cities globally, we estimate a total "
         "opportunity of $3.0 trillion'",
         "The We Company, Form S-1 of 14 August 2019",
         outcome="Its revenue was $2.6-3.5 billion a year from 2019 to 2022, with a net loss every year; WeWork Inc. filed for "
                 "Chapter 11 on 6 November 2023 (Forms 10-K via SEC company facts; Form 8-K of 7 November 2023)"),
    Call(26, "BXP", "2026-02",
         "'we remain on track to achieve occupancy improvements by year-end 2026, consistent with the targets outlined at our "
         "September 2025 Investor Day' (86.7% occupied at the end of 2025)",
         "BXP, Inc., Form 10-K for 2025",
         outcome="Pending; 89.4% occupied and 91.9% leased at 30 September 2026, the fourth quarterly gain in a row (Form 8-K of "
                 "27 October 2026)"),
    Call(26, "Industry, Built", "2026-11-27",
         "BXP's total portfolio occupancy will be 91.0% or more at 31 December 2027. Probability: 55%.",
         "This series, Part 26, chapter 10; reasoning: 91.9% was already leased in September 2026, occupancy had risen four "
         "quarters running and new office construction had 'effectively halted'; against: occupancy fell every year from 2019 "
         "to 2025, San Francisco was 77% let, and tenants leaving at the end of their leases or a weaker economy could undo it",
         rule="BXP's results for 2027 (Form 8-K or 10-K, early 2028): total (in-service) portfolio occupancy at 31 December "
              "2027 as reported; true if 91.0% or more",
         due="2028-01", ours=True),
    Call(27, "ZIM Integrated Shipping Services", "2026-08-19",
         "Full-year 2026 Adjusted EBITDA between $2.0 billion and $2.4 billion (no guidance had been given in March because of "
         "the proposed sale to Hapag-Lloyd)",
         "ZIM, second-quarter 2026 results (Form 6-K of 19 August 2026)",
         outcome="Raised to $2.7-3.0 billion on 6 October and $3.3-3.5 billion on 18 November 2026 (Forms 6-K); the year's "
                 "outcome comes with ZIM's or Hapag-Lloyd's results for 2026"),
    Call(27, "Alphaliner, as quoted by ZIM", "2021-12-31",
         "Container shipping demand 'projected to increase by 6.7%' against fleet growth of 4.5% in 2021, 'therefore the "
         "increase in ship capacity is expected to be less than the increase in demand for container shipping for a second "
         "consecutive year'",
         "ZIM Integrated Shipping Services, Form 20-F for 2021",
         outcome="The boom's orders arrived: fleet growth of 10.3% in 2024 and 7.3% in 2025 against demand growth of 3.5% in "
                 "2025 (Alphaliner via ZIM's Form 20-F for 2025); ZIM's average freight fell from $3,240 a TEU in 2022 to "
                 "$1,203 in 2023"),
    Call(27, "Industry, Built", "2026-11-27",
         "Hapag-Lloyd's purchase of ZIM will be completed by 30 June 2027. Probability: 60%.",
         "This series, Part 27, chapter 10; reasoning: agreed on 16 February 2026, approved by ZIM's shareholders on 30 April "
         "and targeted to close in the first quarter of 2027, leaving a quarter to spare; against: the State of Israel's "
         "Special State Share, the termination of the original application and the need to file a new one",
         rule="Hapag-Lloyd's or ZIM's announcements: true if the acquisition is completed on or before 30 June 2027",
         due="2027-07", ours=True),
    Call(28, "The United States Congress", "1978-10-24",
         "The Airline Deregulation Act: 'to encourage, develop, and attain an air transportation system which relies on "
         "competitive market forces to determine the quality, variety, and price of air services'",
         "Public Law 95-504, 92 Stat. 1705",
         outcome="On price, delivered: American airline fares fell 43% after inflation from 2000 to 2025 (BLS CPI) and "
                 "boardings reached 983 million in 2024 (BTS). The airlines kept about three cents of each dollar of revenue "
                 "over 2009-2025, and four carriers took 87% of the revenue of eight listed American airlines in 2025 "
                 "(Forms 10-K)"),
    Call(28, "Delta Air Lines", "2026-01-13",
         "Full-year 2026 earnings per share of $6.50 to $7.50, about 20% more than in 2025 (repeated in July)",
         "Delta Air Lines, results release of 13 January 2026 (Form 8-K)",
         outcome="Cut to $5.10-5.60 on 9 October 2026, 'absorbing a $6 billion increase in fuel costs' after the Strait of "
                 "Hormuz closed; the year's outcome comes with Delta's results in January 2027"),
    Call(28, "Industry, Built", "2026-11-27",
         "The price of kerosene-type jet fuel on the US Gulf Coast will average more than $3.00 a gallon over 2027. "
         "Probability: 40%.",
         "This series, Part 28, chapter 9; reasoning: it averaged $3.25 in the first eight months of 2026 with the Strait of "
         "Hormuz all but shut, and $3.72 in August; against: it averaged $2.12 in 2025, disruptions end, high prices bring out "
         "supply, and Frontline expects the Middle East's production to be restored",
         rule="The EIA's monthly Gulf Coast kerosene-type jet fuel price (FRED: MJFUELUSGULF), the mean of January to December "
              "2027 as first published; true if above $3.00",
         due="2028-02", ours=True),
    Call(29, "The United States Congress", "1980-10-14",
         "The Staggers Rail Act: 'The purpose of this Act is to provide for the restoration, maintenance, and improvement of "
         "the physical facilities and financial stability of the rail system of the United States'",
         "Public Law 96-448, 94 Stat. 1895",
         outcome="Financial stability, achieved: the four large American railways' operating ratios fell from about 75% in "
                 "2009 to 59.8-67.9% in 2025 (Forms 10-K), against truckload carriers' 97-100%; rail prices after inflation "
                 "fell 32% from 1981 to 2001 and in 2025 were 13% below 1981's (BLS PPI and CPI)"),
    Call(29, "Aurora Innovation", "2022-03",
         "'We plan to initially launch Aurora Horizon, our driverless trucking product, in late 2023 in Texas'",
         "Aurora Innovation, Form 10-K for 2021",
         outcome="Launched in April 2025 with Hirschbach and Uber Freight (Form 10-K for 2025); 500,000 driverless miles by "
                 "September 2026 and 20+ driverless trucks built; Aurora now aims 'to exit 2027 with more than 1,000 "
                 "driverless trucks in operation' (third-quarter 2026 letter), to be scored in 2028"),
    Call(29, "Industry, Built", "2026-11-27",
         "Union Pacific will complete its acquisition of Norfolk Southern on or before 31 December 2027. Probability: 40%.",
         "This series, Part 29, chapter 10; reasoning: both companies' shareholders approved in November 2025, the Surface "
         "Transportation Board accepted the revised application on 28 May 2026 and adopted a procedural schedule on 18 August, "
         "and the companies expect completion 'in the second half of 2027'; against: the first application was rejected as "
         "incomplete, parties moved to dismiss, and a review of this size with conditions to negotiate can run past 2027",
         rule="Union Pacific's or Norfolk Southern's announcements: true if the acquisition is completed on or before "
              "31 December 2027",
         due="2028-01", ours=True),
    Call(30, "DISH Network", "2020-02",
         "'we committed to offer 5G broadband service to at least 70% of the U.S. population and to have deployed a core "
         "network no later than June 14, 2023' (600 MHz licences), as it set out to become a fourth national network",
         "DISH Network, Form 10-K for 2019",
         outcome="The build-out requirements were met, but in August 2025 EchoStar (formerly DISH) 'terminated our deployment of "
                 "our 5G Network', sold spectrum to AT&T for $22.65bn (closed 28 July 2026) and to SpaceX for about $20bn, "
                 "and moved its customers onto AT&T's network (EchoStar, Form 10-K for 2025; AT&T, 10-Q for 2026 Q3)"),
    Call(30, "Industry, Built", "2026-11-27",
         "Comcast will report fewer total domestic broadband customers at 31 December 2027 than at 31 December 2026. "
         "Probability: 80%.",
         "This series, Part 30, chapter 10; reasoning: it lost 411,000 in 2024 and 711,000 in 2025, its 2026 filings attribute "
         "lower broadband revenue to fewer customers and lower rates, and fixed wireless and fibre keep adding homes; against: "
         "new pricing and bundles with its mobile service could stop the loss",
         rule="Comcast's Form 10-K for 2027: total domestic broadband customers at the two year-ends as reported; unscored if "
              "Comcast no longer reports the figure",
         due="2028-02", ours=True),
]


def calls(part: int | None = None, ours: bool | None = None) -> list[Call]:
    return [c for c in CALLS if (part is None or c.part == part) and (ours is None or c.ours == ours)]
