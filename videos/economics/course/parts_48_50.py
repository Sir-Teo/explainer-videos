"""Act IX, The Fields (Parts 43-50), second block (Parts 48-50)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=48, level="U", widget="carbonprice", prereq=(15, 20, 23, 35),
        question="What is a tonne of carbon dioxide worth, and what does the answer turn on?",
        story="The part opens on the bet: in 1980 Julian Simon bet Paul Ehrlich that any raw materials he chose would "
              "be cheaper after inflation in ten years; Ehrlich chose five metals, and in 1990 mailed a cheque for "
              "$576.07. Three of them, from the World Bank's prices, lost 38% as a bundle. Hotelling's rule is "
              "derived from the owner's arbitrage and run on an Island mine, with Slade's U when costs fall, against "
              "the record: real metal prices barely moved in sixty years. The bet is rerun for every decade since "
              "1960 (Ehrlich wins about half). The fishery shows why resources without owners are overused: Gordon's "
              "yield curve, Smith's overshooting fleet, quotas, FAO's stocks and catch shares. Then the climate in "
              "four equations, fitted to Mauna Loa and HadCRUT5, and a DICE-style model built on it that reproduces "
              "DICE-2023's optimal path and its social cost of carbon at every discount rate. The viewer chooses a "
              "discount rate; Ramsey's rule, Stern against a modest time preference, and an is/ought card follow. "
              "After an intermission of the warming as stripes and a tune come fat tails and tipping points, taxes "
              "against permits with British Columbia and the EU, leakage, the EU's border adjustment and a climate "
              "club, solar's learning curve and directed technical change, damages estimated here from ERA5 and "
              "World Bank data, and an electricity market where withholding pays, with California in 2000. Three "
              "dials, practice, Hubbert's 1956 peak and a frontier of global damage, stranded reserves and "
              "adaptation close it.",
        handoff="Part 49 takes the economist's model of choice from the planet to the rest of life: crime, the "
                "family, addiction and identity.",
        outside="Part 15: externalities, public goods and prices against quantities; Part 20: the Ramsey model; "
                "Part 23: discounting and the Gordon formula; Part 35: tariffs; Statistics, Built: panel regression "
                "with fixed effects and clustered errors.",
        objectives={
            "U": ["Explain Hotelling's rule and why real resource prices need not rise.",
                  "Say why a fishery without owners is overused and how a quota fixes it.",
                  "Explain what the social cost of carbon is and why the discount rate moves it so much."],
            "M": ["Derive Hotelling's rule and solve a mine's price path with a choke price.",
                  "Build and fit a small carbon-cycle and energy-balance model, and compute a social cost of carbon "
                  "from an emissions pulse.",
                  "Compare a tax and a cap under cost uncertainty, and estimate a temperature-growth panel."],
            "D": ["State Weitzman's dismal theorem and what fat tails do to cost-benefit analysis.",
                  "State the open questions about global damage, persistence and adaptation."],
            "I": ["Read a merit order, spot profitable withholding, and use a social cost of carbon in a "
                  "cost-benefit analysis."],
        },
        results=[
            ("Hotelling's rule", r"p_{t+1} - c = (1 + r)\,(p_t - c)"),
            ("The sustained catch", r"Y(E) = qEK\,(1 - qE/g)"),
            ("Ramsey's discount rate", r"r = \rho + \eta\, g"),
            ("The social cost of carbon", r"\mathrm{SCC} = \sum_t \frac{-\,\partial C_t / \partial E_0}{(1+\rho)^t}"
                                          r"\left(\frac{c_t}{c_0}\right)^{-\eta}"),
            ("Wright's law", r"\log p = a + b \log Q, \quad 1 - 2^{\,b} = \text{learning rate}"),
        ],
        U=(0, 1, 2, 3, 4, 6, "s09_intermission", 9, 10, 11, 13), D=(8, 16), I=(15,),
        also=(("Agora's climate", "explainer/economics/agora/climate.py"),
              ("The Island's planted truths", "explainer/economics/island.py")),
    ),
    Part(
        n=49, level="U", widget="deter", prereq=(5, 11, 17, 38),
        question="How far can the model of choice under constraint be pushed into the rest of life?",
        story="The part opens on a parking space: in the 1960s Gary Becker, late for an oral examination at "
              "Columbia, weighed a car park against the chance and size of a fine, parked on the street, and began "
              "to think of crime as a choice. Becker's offenders are built on the Island, with his planner's answer "
              "(the largest fine, the thinnest enforcement) and why penalties are not like that. The viewer chooses "
              "whether to double the chance of being caught or the sentence: the answer depends on the offenders, and "
              "the data (Nagin; Lee and McCrary) say the chance. Police and crime are measured three ways on the "
              "Island's blocks, then by Buenos Aires's guards and London's bombings; the 1950 murder rates show how "
              "an estimate can follow its controls. The household is a small factory; women's work since 1948; a "
              "Choo-Siow marriage market reads the gains from each match from the counts; quantity and quality, "
              "fertility since 1950 and China before its one-child policy, Angrist and Evans's same-sex siblings on "
              "the 1980 census, the pill; bargaining and the UK child benefit. After an intermission of the world's "
              "fertility, schools on real data (California's districts, Tennessee's STAR, Maimonides' rule, teachers' "
              "value added and the move test), early childhood and what replicates, Grossman's health capital and "
              "doctor visits, patents, deaths of despair and the triplicate states, rational addiction and cigarette "
              "demand by 2SLS, and the critics (the day-care fine, paid blood donors). Three dials, practice, "
              "DiIulio's super-predators and a frontier of very low fertility and sex ratios close it.",
        handoff="Part 50, the capstone of the act, writes a policy memo: a child allowance, from the question to the "
                "evidence to the Island and the advice.",
        outside="Part 5: choice under a budget; Part 11: equilibrium; Part 17: matching markets; Part 38: labour "
                "supply; Statistics, Built: instrumental variables, regression discontinuity, shrinkage.",
        objectives={
            "U": ["Explain Becker's model of crime and why the chance of being caught may deter more than the "
                  "sentence.",
                  "Say why comparing places is a poor way to measure the effect of police, and what works instead.",
                  "Explain the household as a producer, the quantity-quality trade-off, and why it matters whose "
                  "purse the money reaches."],
            "M": ["Solve Becker's planner's problem and compute the offence rate under different attitudes to risk "
                  "and time.",
                  "Estimate a Choo-Siow surplus from counts, a Wald estimate from same-sex siblings, and a class-size "
                  "effect from STAR within schools.",
                  "Shrink teachers' value added and test it with teacher moves; estimate cigarette demand by 2SLS."],
            "D": ["Derive the rational addict's response to an announced price rise.",
                  "State the open questions about very low fertility, sex ratios and saving."],
            "I": ["Read a deterrence, class-size or value-added estimate critically, and recognise when a price may "
                  "change the meaning of an act."],
        },
        results=[
            ("Becker's offender", r"\text{offend if } (1-p)\,u(g) + p\,u(g - F) > u(0)"),
            ("Choo and Siow", r"\mu_{ij} = \sqrt{\mu_{i0}\,\mu_{0j}}\; e^{\Phi_{ij}/2}"),
            ("Quantity and quality", r"\max\ \log c + a\log n + b \log q \ \text{ s.t. } c + n(\pi + q) = Y"),
            ("The Wald estimator", r"\beta = \frac{E[y \mid z=1] - E[y \mid z=0]}{E[d \mid z=1] - E[d \mid z=0]}"),
            ("Shrinkage", r"\hat\mu_j = \frac{\sigma^2_\mu}{\sigma^2_\mu + \sigma^2_e / n}\; \bar y_j"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7, "s09_intermission", 8, 13), D=(12, 16), I=(15,),
        also=(("Agora's economic approach", "explainer/economics/agora/family.py"),
              ("The Island's planted truths", "explainer/economics/island.py")),
    ),
]
