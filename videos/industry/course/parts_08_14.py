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
]
