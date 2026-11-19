"""Act I, The Question (Parts 1-4)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=1, level="U", widget="pit",
        question="How do millions of strangers, none of them in charge, manage to feed a city, and how would we know "
                 "when that order is about to fail?",
        story="The part opens on Bastiat's night in Paris in the 1840s: a million people who would starve within days "
              "if supplies stopped, asleep, while eighty departments send food with no plan. Then the Queen's "
              "question at the London School of Economics in November 2008: why had nobody noticed the crisis "
              "coming? The viewer plays a pit market as a buyer with a $2.70 card; Agora's learning traders find the "
              "competitive band of $2.20 to $2.30 in three periods, and the cards, turned over, become demand and "
              "supply. Crusoe alone shows opportunity cost as the slope of a bowed frontier; Crusoe and Friday show "
              "that both gain at a price of 0.6 coconut a fish although Crusoe is faster at both; Smith's pin "
              "factory multiplies output 240 times; Hayek's tin market reaches sixty users with one price where "
              "equal rationing would need 120 numbers. A fine for late parents in Haifa raises late pick-ups, and "
              "the long view shows income per head growing at 0.16% a year before 1700 and 1.33% since 1820. After "
              "a wordless intermission, the part asks what a model is for, sets 1929 beside 2008 and scores the "
              "forecasters' call for 2009, draws the economy as plumbing, and ends on Coase's and Simon's question "
              "of how much of the economy is a market at all.",
        handoff="Part 2 builds demand and supply from the pit's cards, and Part 4 asks when data like the Haifa "
                "study can be trusted. Crusoe's best day returns as the theory of choice in Parts 5 and 6, "
                "comparative advantage between countries in Part 35, the price system as a whole in Part 9, Hayek's "
                "calculation debate in Parts 9 and 64, incentives in Parts 14 and 45, the long run in Parts 19 to "
                "21, crises and forecasts in Parts 26, 33 and 57, and Coase's firm in Parts 8 and 62.",
        outside="School arithmetic for most chapters. Chapter 2 differentiates a square root; chapter 7 uses the "
                "exponential and the natural logarithm.",
        objectives={
            "U": ["Find the competitive quantity and price band from buyers' and sellers' cards, and the largest "
                  "total gain.",
                  "Compute opportunity costs from a table of hours, say who has a comparative advantage in what, and "
                  "give the range of prices at which both sides gain from trade.",
                  "Explain why a price can coordinate users who know nothing of its cause, and why a fine can raise "
                  "the behaviour it prices."],
            "M": ["Derive the opportunity cost of a good as the slope of a production possibilities frontier with "
                  "diminishing returns, and the condition for the best point on it.",
                  "Compute a difference in differences from period means and state the assumption it rests on.",
                  "Derive the doubling time of steady growth and read growth rates off a log-scale chart."],
            "D": ["State Coase's question and Simon's argument about firms and markets, and propose data that would "
                  "measure how much of an economy is coordinated by each.",
                  "Explain what zero-intelligence traders show about how much of a market's efficiency comes from its "
                  "rules rather than its traders' learning."],
            "I": ["Read a forecast against its outcome, and say what a probability of a fall adds to a point "
                  "forecast.",
                  "Separate a positive claim about what a policy does from the value judgment needed to recommend "
                  "it, and name the judgment."],
        },
        results=[
            ("The competitive band", r"q^*=\max\{k: v_{(k)}\ge c_{(k)}\},\quad "
                                     r"p\in[\max(c_{(q^*)},v_{(q^*+1)}),\,\min(v_{(q^*)},c_{(q^*+1)})]"),
            ("Opportunity cost", r"-\frac{dC}{dF}=\frac{\partial C/\partial h_C}{\partial F/\partial h_F}"
                                 r"=\frac{4}{3}\sqrt{\frac{h}{10-h}}"),
            ("The best day", r"\text{MRS}=\frac{0.6/F}{0.4/C}=\text{MRT}=1.63"),
            ("Comparative advantage", r"\frac{h^{A}_{F}}{h^{A}_{C}}<p<\frac{h^{B}_{F}}{h^{B}_{C}}"
                                      r"\ \Rightarrow\ \text{both gain}"),
            ("Difference in differences", r"(\bar y^{T}_{1}-\bar y^{T}_{0})-(\bar y^{C}_{1}-\bar y^{C}_{0})"
                                          r"=8.4+0.8=9.2"),
            ("Doubling time", r"y_t=y_0e^{gt}\ \Rightarrow\ T_2=\frac{\ln 2}{g}\approx\frac{70}{g\,\%}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, "s09_intermission"), D=(13,), I=(12,),
        also=(("Agora's market", "explainer/economics/agora/market.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=2, level="U", widget="scissors",
        question="What sets a price, and what happens to it when a frost, a tax or the law gets in the way?",
        story="The part opens at Purdue in January 1956, where Vernon Smith ran a double auction expecting the "
              "competitive model to fail, and watched it converge. Smith's paradox of water and diamonds is "
              "dissolved by value at the margin (Jevons, Menger, Walras), and Whately's pearl divers dispose of the "
              "labour theory. Demand is built from Ana's cups and three drinkers added sideways, until crowds of "
              "10,000 buyers turn the staircase into a line; supply from a farm's rising costs; and Marshall's "
              "scissors join them. In Part 1's pit, four cards fix the band. The viewer plays a lopsided market, "
              "where Agora's learning traders find $2.25 to $2.30 but zero-intelligence traders stop at $2.10: zero "
              "is not enough (Cliff and Bruten), and Smith's prediction is scored wrong. Elasticity is measured "
              "along the Island's fish market and with the midpoint formula on its stormy days; Brazil's black "
              "frost of July 1975 cut the world's coffee crop by 16% and raised Arabica 5.7 times, still the real "
              "record. After an intermission of sixty-six years of commodity prices, Dupuit's bridges give surplus, "
              "a 40-cent tax in the pit falls the same way whoever remits it, a price cap loses 16% of the gains "
              "rather than the triangle's 1.5%, and San Francisco's rent control shrank the rental stock. The "
              "frontier is pricing by algorithm.",
        handoff="Part 3 adds up prices across goods and years. The picture's failures return as monopoly and "
                "oligopoly (Parts 10 to 12), hidden quality (13), spillovers (15), asset prices and crises (23, 33) "
                "and designed markets (16, 17); demand is rebuilt from choice in Parts 5 and 6, the welfare theorem "
                "in Part 9, the identification of a demand curve in Part 4, incidence in public finance in Part 41, "
                "the minimum wage in Part 38 and market definition in Part 61.",
        outside="School algebra. Chapter 6 uses the elasticity of a straight line; the problems use one integral.",
        objectives={
            "U": ["Build a market demand curve from buyers' reservation values and a supply curve from sellers' "
                  "costs, and find the competitive quantity and the band of prices that clears it.",
                  "Compute an elasticity by the midpoint formula, and say whether spending rises or falls when a "
                  "price changes.",
                  "Work out who bears a tax and the deadweight loss it causes, and what a binding price cap or floor "
                  "costs."],
            "M": ["Derive the elasticity along a straight demand line and the price that maximizes spending.",
                  "Derive the incidence of a tax on straight lines, and show that it does not depend on who remits "
                  "it.",
                  "Compute the loss from a binding price control under efficient rationing and under a lottery."],
            "D": ["Explain why zero-intelligence traders find the competitive price only in balanced markets, and "
                  "design a test of how much intelligence convergence needs.",
                  "State what is open about pricing algorithms and collusion, and propose a simulation that would "
                  "settle part of it."],
            "I": ["Say who pays a proposed excise tax and how its revenue depends on the elasticities.",
                  "Read a commodity shock from price and quantity data: which curve moved, and a rough short-run "
                  "elasticity with its caveats."],
        },
        results=[
            ("Value at the margin", r"p^{*}=MV(q^{*})=MC(q^{*})"),
            ("Elasticity", r"\varepsilon=\frac{dQ/Q}{dP/P}\approx\frac{\Delta Q/\bar Q}{\Delta P/\bar P}"),
            ("A straight demand line", r"Q=a-bp:\quad \varepsilon(p)=\frac{-bp}{a-bp},\quad "
                                       r"\arg\max_p\,pQ=\frac{a}{2b}\ (\varepsilon=-1)"),
            ("Incidence", r"\text{buyers' share}=\frac{\varepsilon_S}{\varepsilon_S+|\varepsilon_D|}"),
            ("Deadweight loss of a tax", r"\text{DWL}=\tfrac12\,t\,\Delta Q"),
            ("Rationing by lottery", r"\text{extra loss}=\tfrac12\,q_S\,\big(P_D(q_S)-\bar p\big)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, "s09_intermission"), D=(14,), I=(13,),
        also=(("Agora's curves", "explainer/economics/agora/curves.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
    Part(
        n=3, level="U", widget="measure",
        question="How do you put a number on an economy, and what does the number leave out?",
        story="The part opens in 1932, when nobody could say how far America's income had fallen, and follows Simon "
              "Kuznets's report to the Senate of January 1934: income produced down 53%, interest still paid almost "
              "in full, wages in the mines and factories down by six tenths, and a warning that the welfare of a "
              "nation can scarcely be inferred from its income. Petty had already added England up twice, by "
              "spending and by income, in 1665. On the Island, Dara keeps the books: $975 of sales, $740 of value "
              "added, the same $740 as consumption, investment, government and net exports, and again as wages, "
              "profits and taxes; saving equals investment plus the trade balance. America's GDP of $30.9 trillion "
              "in 2025 is built the same way, with a statistical discrepancy. Unpaid work is 31% of the Island's "
              "output. The viewer prices Bo's two baskets after a storm doubles the price of fish: Laspeyres says "
              "50%, Paasche 33%, the truth on his indifference curve 41.4%, which Fisher's index finds; chained "
              "Laspeyres drifts to 2.03 over twelve seasons. The CPI's bias (Boskin's 1.1 points), hedonic quality "
              "adjustment on the boatyard's boats, and the chained CPI's measured gap follow. After an intermission "
              "of seventy-eight years of unemployment, with one month missing, the part compares countries at "
              "purchasing power (China's economy $38 trillion, not $19), measures unemployment with a survey (U-1 to "
              "U-6), distributes income (Lorenz, Gini, and the dispute over the top 1%), traces $10 of exports "
              "through Leontief's inverse, revises 2008 vintage by vintage, and tries measures beyond GDP. The "
              "frontier is intangibles, night lights and the 2025 SNA.",
        handoff="Part 4 asks when data can answer an economic question. The accounts return as aggregate demand "
                "(Part 27), the price index as inflation (Part 28), real-time data as policy (Part 31), saving and "
                "the current account in the open economy (Part 34), trade in value added (Part 36), Kaldor's facts "
                "in growth (Part 20), unemployment's flows (Part 24), the labour share (Part 39), inequality (Part 40) "
                "and the measurement of AI (Part 65).",
        outside="School algebra and percentages. Chapter 10 uses a matrix inverse (explained on screen); the problems "
                "use a 2x2 inverse and one logarithm.",
        objectives={
            "U": ["Compute GDP by output, spending and income from a small economy's accounts, and explain why the "
                  "three agree and what the statistical discrepancy is.",
                  "Deflate a nominal series by a price index, and compute Laspeyres, Paasche and Fisher indexes for "
                  "two baskets.",
                  "Compute U-3 and the broader rates from a labour survey, and a Gini coefficient from a list of "
                  "incomes."],
            "M": ["Show that Laspeyres overstates and Paasche understates a homothetic consumer's cost of living, and "
                  "that chained Laspeyres drifts when prices bounce.",
                  "Derive S = I + (X - M) from the spending identity, and compute a Leontief inverse and its output "
                  "multipliers.",
                  "Estimate a pure price change with a hedonic regression, and compare PPP and market-rate GDP."],
            "D": ["Explain the disagreements over the top 1%'s share in distributional national accounts and what "
                  "data would settle them.",
                  "Design a test of reported growth with night lights, and state what would confound it."],
            "I": ["Read a jobs report and a GDP release, including what a revision can do to them.",
                  "Say how biased the CPI is, source by source, and what that bias costs an indexed budget."],
        },
        results=[
            ("GDP three ways", r"\sum_j (x_j - \textstyle\sum_i z_{ij} - m_j)=C+I+G+X-M=W+\Pi+T"),
            ("Saving and the trade balance", r"S \equiv Y-C-G = I+(X-M)"),
            ("Laspeyres and Paasche", r"P_L=\frac{\sum p_1q_0}{\sum p_0q_0},\quad P_P=\frac{\sum p_1q_1}{\sum p_0q_1},\quad "
                                      r"P_P\le P^{*}\le P_L"),
            ("Fisher's ideal index", r"P_F=\sqrt{P_L\,P_P}"),
            ("Leontief's inverse", r"x=(I-A)^{-1}f=f+Af+A^2f+\cdots"),
            ("The Gini coefficient", r"G=\frac{\sum_i\sum_j|y_i-y_j|}{2n^2\bar y}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, "s08_intermission"), D=(15,), I=(14,),
        also=(("Agora's national accounts", "explainer/economics/agora/accounts.py"),
              ("Agora's index numbers", "explainer/economics/agora/indices.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
]
