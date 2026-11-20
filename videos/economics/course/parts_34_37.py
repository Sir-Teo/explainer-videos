"""Act VII, The World Economy (Parts 34-37)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=34, level="U", widget="peg", prereq=(3, 23, 27, 28, 30, 31),
        question="What sets the price of one money in terms of another, and what can a country not have at once?",
        story="The part opens on Wednesday 16 September 1992 in four acts, as the Bank of England raises its rate, "
              "announces another rise, spends its reserves and leaves the Exchange Rate Mechanism by evening. It "
              "reads the balance of payments as accounts, puts the viewer in the governor's chair with reserves "
              "draining, and shows with Obstfeld's model why a peg in a middle zone falls if traders expect it to. "
              "It tests purchasing power parity with the Big Mac index and 150 years of real exchange rates, "
              "uncovered parity with Fama's regression and the carry trade, and every model against the random walk "
              "with Meese and Rogoff's horse race rerun; derives Mundell-Fleming's trilemma and Dornbusch's "
              "overshooting; and after an intermission of the pound since 1971 turns to three generations of "
              "currency crises, the IMF and its critics, the euro, global imbalances and the dollar's dominance; two "
              "dials, Meese and Rogoff as Called it?, and a frontier where finance, not trade, moves currencies.",
        handoff="Part 35 turns from money to goods with comparative advantage; Part 36 measures the pass-through of "
                "tariffs; Part 66 returns to the dollar's power, sanctions and trade wars.",
        outside="Part 3: the national accounts; Part 23: asset prices and no arbitrage; Part 27: IS-LM; Part 28: "
                "expectations; Part 30: sticky prices; Part 31: the central bank. Chapter 4 uses Newey-West standard "
                "errors for overlapping horizons; chapter 7 a first-order differential equation; chapter 12 a "
                "distributed-lag regression.",
        objectives={
            "U": ["Read the balance of payments, and explain the current account as saving minus investment.",
                  "Explain purchasing power parity, the Big Mac index and the Balassa-Samuelson effect, and why real "
                  "exchange rates return to parity only slowly.",
                  "State the trilemma, and describe the three generations of currency crises with an example of "
                  "each."],
            "M": ["Derive the effects of fiscal and monetary policy under fixed and floating rates in "
                  "Mundell-Fleming.",
                  "Derive Dornbusch's overshooting and its impact factor.",
                  "Estimate a PPP half-life, Fama's regression with overlapping-horizon standard errors, and an "
                  "out-of-sample horse race against the random walk."],
            "D": ["Solve the timing of a first-generation attack and the band of self-fulfilling crises.",
                  "Explain the exchange-rate disconnect and the financial explanations at the frontier: limited "
                  "intermediaries and financial shocks."],
            "I": ["Read a reserve-adequacy or currency-strategy note: carry, parity, pass-through and the dollar's "
                  "role."],
        },
        results=[
            ("The current account", r"CA = S - I = (S_p - I) + (T - G)"),
            ("Uncovered interest parity", r"E_t[s_{t+h}] - s_t = i_t - i^*_t"),
            ("Fama's regression", r"s_{t+h} - s_t = \alpha + \beta\,(i_t - i^*_t) + \varepsilon_{t+h}, \quad "
                                  r"\hat\beta < 1"),
            ("The PPP half-life", r"q_t = \rho\, q_{t-1} + \varepsilon_t, \qquad t_{1/2} = \ln 0.5 / \ln \rho"),
            ("Overshooting", r"s_0 - \bar s = \frac{\Delta m}{\lambda\theta}"),
            ("Krugman's attack", r"T = (\bar s - \alpha\mu - d_0)/\mu"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s09_intermission", 8, 9, 10, 11, 12, 13), D=(15,), I=(14,),
        also=(("Agora's open economy", "explainer/economics/agora/openecon.py"),
              ("The Island's planted truths", "explainer/economics/island.py"),
              ("The Data Room's sources", "explainer/economics/data/SOURCES.md")),
    ),
]
