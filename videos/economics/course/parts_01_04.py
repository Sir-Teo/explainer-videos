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
]
