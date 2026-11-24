"""Act II, Out of the Ground (Parts 8-14)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=8, level="U", widget="oilshock", prereq=(4, 6),
        question="What does a barrel cost, and who decides what it sells for?",
        story="The part opens on 20 April 2020, when WTI for May delivery settled at -$37.63 with Cushing's tanks 76% "
              "full, and on 2026, when war closed the Strait of Hormuz and Brent rose from $61 to $118 in a quarter "
              "and averaged $124 in October. The viewer runs an oil company choosing between a conventional field, a "
              "deepwater platform and a shale pad across 400 price paths. Oil is followed from source rock to trap; "
              "Spindletop (1901) shows a well fading, Arps's curves a conventional and a shale well (9% and 60% in the "
              "first year), and the Works' basin needs 44 new wells a month to hold a million barrels a day. "
              "ExxonMobil's proved reserves fall from 22.4 to 15.2bn barrels in 2020 with nothing pumped. Aramco "
              "lifts a barrel for $3.51 while Texas drillers need $66 for a new well (Dallas Fed); the last barrel sets "
              "the price, and Aramco paid the Saudi state about $204bn in 2025. A gallon of gasoline is split by EIA's "
              "components; benchmarks, futures and storage explain the negative price; inelastic demand and supply "
              "turn a 5% shortage into a two-thirds price rise, and 2026's numbers imply a demand response of about "
              "-0.05. After eighty years of real prices, OPEC's share (58%, 28%, 35%) and Saudi Arabia's swing (9.9 to "
              "3.4m b/d, 1980-1985) show a cartel's arithmetic; shale cut rigs 80% and output 11% and made the US a "
              "net exporter; the 3-2-1 crack spread and Valero, gas prices in three markets and US LNG, and the "
              "service companies' falls (Halliburton -52%) complete the chain. Hubbert's 1956 forecasts are scored "
              "against EIA's data, and the series calls Brent below $90 for 2027.",
        handoff="Part 9 digs for metals with the same arithmetic of grades, costs and long projects; Part 13 returns to "
                "gas in power plants, and the finance and geopolitics parts to oil's money and its states.",
        outside="Percentages and arithmetic; Part 4's cost curve; Part 6's cycle and accelerator.",
        objectives={
            "U": ["Explain where oil comes from and why shale wells must be drilled continuously.",
                  "Explain why a barrel can cost $3.51 to lift in one place and $66 to drill in another, and which sets "
                  "the price.",
                  "Explain why small shortages move the oil price so much, with 2020 and 2026 as examples."],
            "M": ["Fit and use Arps's decline curve, and compute a field's break-even price from its cash flows.",
                  "Compute the price multiple that clears a supply loss under given elasticities.",
                  "Compute the 3-2-1 crack spread from product and crude prices."],
            "D": ["Score a resource forecast (Hubbert, 1956) against the record and explain where it failed.",
                  "Estimate a rough demand elasticity from a supply shock and state what it leaves out."],
            "I": ["Read proved reserves as a price-dependent forecast in a 10-K, and a lifting cost from an annual report.",
                  "Place a company in the industry's map: national, major, independent, refiner, services, LNG, trader."],
        },
        results=[
            ("Arps's decline", r"q(t) = \frac{q_0}{(1 + b\,D\,t)^{1/b}}"),
            ("Break-even", r"\sum_t \frac{\text{cash}_t(p^{*})}{(1+r)^t} = 0"),
            ("Clearing a shortage", r"\frac{p_1}{p_0} = (1 - \ell)^{1/(\varepsilon_d - \varepsilon_s)}"),
            ("3-2-1 crack", r"\frac{2\,p_{\text{gasoline}} + p_{\text{diesel}} - 3\,p_{\text{crude}}}{3}"),
            ("Hubbert's logistic", r"Q(t) = \frac{U}{1 + e^{-k(t - t_m)}}"),
        ],
        U=(0, 1, 2, 3, 5, 6, 7, 8, 9, "s11_intermission", 10, 11, 13, 15), I=(4, 12, 14), D=(16,),
        also=(("The Register's rows for Part 8", "explainer/industry/data/rows_p08.py"),
              ("Wells, fields, the shale treadmill, clearing prices and the crack spread", "explainer/industry/works/oil.py"),
              ("EIA's petroleum, international, pump-price and gas extracts; energy prices", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=9, level="U", widget="minegrade", prereq=(4, 6, 8),
        question="Why is a mine worth a fortune in one decade and nothing in the next?",
        story="The part opens in the Atacama in March 1981: nine holes paid for, five drilled dry, and the sixth finding "
              "Escondida, about 300 million tonnes of ore at 1.3-1.5% copper, for a $3m search. In the year to June "
              "2025 it produced 1,305 kt and $8.6bn of operating profit, but its feed grade falls from 1.02% to about "
              "0.85%. The viewer owns the Works' model deposit (600 Mt at 0.5%, $3bn to build, break-even $3.61 a "
              "pound) and chooses to build, wait or sell across 400 price paths. Copper is followed from pit to "
              "cathode, with about 350 tonnes of rock moved for a tonne of copper at 1%, and by leaching at Freeport's "
              "0.21% ore. Grade sets the rock, the cost and the break-even; a mine plan takes the richest rock first, "
              "and the option to wait says build only about 35% above break-even (Dixit and Pindyck). Four real "
              "operations make a cost curve (Grasberg's gold puts it below zero), Escondida's block moves as its grade "
              "falls, and the US Geological Survey shows Chile digging the most copper while China refines 48% of it. "
              "Iron ore moves from one negotiated price a year to a market quoted in China (Vale, April 2010). The "
              "exchanges set every miner's price; 2025's tariff fear split New York from London and nearly doubled US "
              "imports. After a century of copper in constant dollars, the supercycle (copper x5.7 and iron ore x13.2, "
              "2002-2011) and the bust (Vale -$12.1bn in 2015), the state's share (36% of the model mine's profit; "
              "Indonesia's 51% of Grasberg; Congo's cobalt quotas; Indonesia's nickel), critical minerals (lithium's "
              "boom and bust, China's rare-earth controls) and gold (a 5.5-metre cube worth about $350bn; Newmont's "
              "record) lead to the landscape of November 2026. Simon and Ehrlich's 1980 wager is re-run for every "
              "decade since 1900 (Ehrlich would have won 61%), and the series calls Escondida below 1,100 kt in the "
              "year to June 2027.",
        handoff="Part 10 turns from rock to soil; Part 11 follows the metals into steel, cement and aluminium; the "
                "energy-transition and geopolitics parts return to critical minerals and the state.",
        outside="Percentages and arithmetic; Part 4's cost curve; Part 6's cycle; Part 8's break-even and reserves.",
        objectives={
            "U": ["Explain why grade decides how much rock a mine moves and what its copper costs.",
                  "Explain why every miner takes the exchange's price, and why the low-cost mine survives the bust.",
                  "Explain where copper is mined and where it is refined, and what makes a mineral critical."],
            "M": ["Compute rock per tonne of metal from grade, recovery and strip ratio.",
                  "Compute a mine's break-even price from its cash flows, and the value of waiting a year to build.",
                  "Compute the state's share of a mine's profit from a royalty and an income tax."],
            "D": ["Test a famous resource wager (Simon and Ehrlich, 1980) over every window of the record, and say what "
                  "the result does and does not show.",
                  "State a falsifiable forecast for a mine's output with a probability, and the evidence for and "
                  "against it."],
            "I": ["Read a miner's results for production, grade, unit cost and guidance, and a by-product credit.",
                  "Place a company on the map: diversified majors, copper and gold miners, lithium producers, state "
                  "miners."],
        },
        results=[
            ("Rock per tonne of metal", r"\frac{1 + s}{g \, \rho}"),
            ("Break-even", r"\sum_t \frac{\text{cash}_t(p^{*})}{(1+r)^t} = 0"),
            ("The option to wait", r"V_{\text{wait}} = \frac{\mathbb{E}\,[\max(\text{NPV}(p_1), 0)]}{1+r}"),
            ("The state's share", r"\frac{\text{royalty} + \text{tax}}{\text{revenue} - \text{costs}}"),
            ("The wager", r"\frac{1}{5}\sum_m \frac{p_m(t+10)}{p_m(t)} \gtrless 1"),
        ],
        U=(0, 1, 2, 3, 5, 6, 7, 8, "s10_intermission", 9, 10, 12, 13), I=(11,), D=(14,),
        also=(("The Register's rows for Part 9", "explainer/industry/data/rows_p09.py"),
              ("Grade, the model mine, the option to wait, the cost curve and the wager", "explainer/industry/works/mine.py"),
              ("The USGS's historical prices, the IMF's metal prices and the miners' 20-F accounts",
               "explainer/industry/data/SOURCES.md")),
    ),
]
