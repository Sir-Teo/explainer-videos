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
    Part(
        n=10, level="U", widget="treadmill", prereq=(4, 5, 6),
        question="Why do farmers grow ever more, and keep so little of what we pay?",
        story="The part opens on Norman Borlaug's dwarf wheat: Mexico self-sufficient by 1956, India and Pakistan from the "
              "mid-1960s, the Nobel Peace Prize in 1970, and wheat yields up 3.4 to 4.2 times since 1961; yet farms got "
              "12.6 cents of an American food dollar in 2025. The viewer farms 296 acres of corn through three real "
              "seasons (2012, 2014, 2020), choosing how much to sell ahead and whether to store, and finds that no rule "
              "wins every year. USDA's costs and returns show a 2025 acre bringing in $782 and costing $901, with "
              "break-evens of $2.30 (cash) and $4.55 (all costs) against a $3.93 price, and corn below its full costs in "
              "19 of 30 years. The food dollar splits into thirteen industries (restaurants 35.5 cents, processing 17.2, "
              "farms' own work about 6); the wheat in a loaf is about 5% of its price. Cochrane's treadmill turns better "
              "seed into lower prices: US corn yields x7 since before 1935, farms from 6.81 to 1.87 million. The input "
              "makers (CF's profit x10 in 2022), the grain traders (ADM's 2.7% margin; the soybean crush), futures, the "
              "beef packers (four firms buy 85% of fed cattle) and the brand owners form a margin 'smile' from field to "
              "shop. After a century of farm income, the state's payments ($57bn in 2020, $47bn forecast for 2026) and "
              "India's rice export ban, the land is shown to keep the gains (returns since 1990: 2.5% from farming, 4.6% "
              "from land values; Ricardo's rent). Cocoa's 2024 spike and the world's food supply per person (2,180 to "
              "3,010 kilocalories since 1961) lead to the landscape; Ehrlich's 1968 Population Bomb is scored, and the "
              "series calls the 2026 farm share above 2025's.",
        handoff="Part 11 follows the heavy materials, steel and cement; Part 12 the chemicals, fertilizer among them; Part 22 "
                "returns to processed food and brands, and the retail parts to the supermarket.",
        outside="Percentages and arithmetic; Part 4's cost curve; Part 5's moats; Part 6's cycle.",
        objectives={
            "U": ["Explain why a farmer is a price taker, and why better methods lower the price rather than raise incomes.",
                  "Explain where a US food dollar goes, and why the farm share is small and smaller still in restaurants.",
                  "Explain why the companies around the farm keep more of each dollar than the farm does."],
            "M": ["Compute an acre's cash and full break-even prices from its costs and yield.",
                  "Compute the revenue from a forward sale and from storage, and why a hedge in a drought becomes a bet.",
                  "Compute the price change from a supply increase under a given demand elasticity."],
            "D": ["Score a famous forecast of famine (Ehrlich, 1968) against the record of food supply, and say what it "
                  "left out.",
                  "State a falsifiable forecast for the farm share with a probability and the evidence for and against."],
            "I": ["Read USDA's costs and returns, the food dollar and farm income statistics.",
                  "Place a company on the chain: inputs, traders, packers, brand owners, retailers."],
        },
        results=[
            ("Break-even price", r"p^{*} = \frac{\text{costs per acre}}{\text{bushels per acre}}"),
            ("A forward sale", r"h\,\bar{q}\,p_0 + (q - h\,\bar{q})\,p_1"),
            ("The treadmill", r"\frac{p_1}{p_0} = \left(\frac{Q_1}{Q_0}\right)^{1/\varepsilon}"),
            ("The crush margin", r"\tfrac{44}{60}\,p_{\text{meal}} + \tfrac{11}{60}\,p_{\text{oil}} - p_{\text{beans}}"),
            ("Ricardo's rent", r"\text{rent} = p\,q - \text{all other costs}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 8, "s10_intermission", 9, 10, 11, 12, 13), I=(7,), D=(14,),
        also=(("The Register's rows for Part 10", "explainer/industry/data/rows_p10.py"),
              ("The acre, the forward sale, the treadmill and the margin ladder", "explainer/industry/works/farm.py"),
              ("USDA's food dollar, costs and returns and farm income; FAO yields; food prices", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=11, level="U", widget="millglut", prereq=(4, 5, 6),
        question="Why do the things everything is made of earn so little?",
        story="The part opens in Cheltenham on 13 August 1856, where a Welsh ironmaster laughed at 'a fellow come down from "
              "London to read a paper on the manufacture of malleable iron without fuel': Henry Bessemer, who burned the "
              "carbon out of pig iron with a blast of air. The world now makes 1,849 Mt of steel, about 3.8 billion "
              "tonnes of cement and 74 Mt of aluminium, and a kilogram of steel sheet (94 cents) costs less than one of "
              "bananas. The viewer runs a blast furnace through a glut: running full loses least ($308m) for one mill, "
              "but if every mill runs full the price sinks to $482 and banking the furnace wins. Steel is made from ore "
              "and coal (2.34 t of CO2 a tonne) or scrap and electricity (0.69); Nucor's $1,008 ton holds $385 of scrap "
              "and a $623 spread, and its profit swung from $0.7bn (2020) to $7.6bn (2022) while Cleveland-Cliffs lost "
              "money at the same price. Fixed costs keep mills running (US capacity utilization 50% in 1982, 51% in "
              "2009); minimills climbed from rebar to sheet (38% to 71% of US steel, 1992-2025) and Nucor out-earned US "
              "Steel $30bn to $3bn over 2010-2024. China went from 13% to 52% of world steel and doubled its exports "
              "as home demand fell. Cement travels badly, so every plant owns a circle; Europe's makers kept a 'home "
              "market' rule from 1983 and were fined about EUR 250m in 1994. Aluminium is electricity in solid form "
              "(13,880 kWh a tonne): China makes 60%, the Gulf's output halved in April 2026 and the price hit $3,658. "
              "Packaging consolidates; stone, the cheapest of all, has the steadiest prices (the real price from $10.52 "
              "in 2000 to $19.39) because quarries near cities cannot be copied, and Vulcan makes $8.66 a ton. Cement "
              "and steel are among the largest emitters; hydrogen would cost $108-271 a tonne of iron; the EU's border "
              "charge began in 2026. worldsteel's China forecasts were too high three years running, and the series "
              "calls 2026's fall above 2.0%.",
        handoff="Part 12 turns oil, gas and salt into chemicals; Part 14 follows construction and housing, where cement, "
                "steel and stone are used; the energy parts return to the power that smelters and furnaces buy.",
        outside="Percentages and arithmetic; Part 4's cost curve; Part 5's moats; Part 6's cycle.",
        objectives={
            "U": ["Explain the two ways of making steel and why scrap-rich countries use electric furnaces.",
                  "Explain why heavy plants keep running in a glut, and why that makes gluts last and profits swing.",
                  "Explain why cement and stone markets are local, and why quarries near cities earn steady profits."],
            "M": ["Compute a mill's break-even price at full and partial output, and compare running, cutting and banking.",
                  "Compute a minimill's metal spread from its price, scrap cost and yield, in short and gross tons.",
                  "Compute a plant's market area and the price it can charge near home from gate costs and haulage."],
            "D": ["Score a forecaster's year-ahead forecasts (worldsteel on China) against the outcomes and look for a bias.",
                  "Work out the CO2 of calcination and of carbon reduction, and the hydrogen and electricity a tonne of "
                  "iron would need instead, and say what the arithmetic leaves out."],
            "I": ["Read worldsteel's and USGS's tables and a steelmaker's 10-K for price, scrap cost and utilization.",
                  "Place a company on the map: integrated steel, minimill, cement, aggregates, aluminium, packaging."],
        },
        results=[
            ("Break-even at a rate", r"p^{*}(r) = c + \frac{F}{r\,K}"),
            ("Metal spread", r"p - 1.1\,s\,\tfrac{2000}{2240}"),
            ("A plant's reach", r"d^{*} = \frac{p - c}{t}"),
            ("Calcination", r"\text{CO}_2 = x_{\text{CaO}}\,\frac{44.01}{56.08}"),
            ("Hydrogen for iron", r"\frac{3 \times 2.016}{2 \times 55.85} \approx 0.054\ \text{t per t of Fe}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, "s10_intermission", 9, 10, 11, 13), I=(12,), D=(14,),
        also=(("The Register's rows for Part 11", "explainer/industry/data/rows_p11.py"),
              ("Transcribed tables: worldsteel, Nucor, the International Aluminium Institute", "explainer/industry/data/tables.py"),
              ("The mills, the glut game, kilns and the chemistry", "explainer/industry/works/mill.py"),
              ("USGS history, producer prices, the Global Carbon Budget, the companies' accounts",
               "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=12, level="U", widget="cracker", prereq=(4, 6, 8),
        question="How does a molecule of gas become a thousand products, and where in the chain is the money?",
        story="The part opens with Fritz Haber's patent of 13 October 1908 on the synthesis of ammonia from its elements, "
              "and Carl Bosch's plant: the world made 4.8 Mt of nitrogen as ammonia in 1950 and about 160 Mt in 2025, "
              "while the number of people rose from 1.7 to 8 billion. The viewer builds a $6bn cracker in 2012, in Texas "
              "on ethane or in Europe on naphtha: with real gas and oil prices Texas earns about $12bn by 2026 and pays "
              "back by 2020, Europe barely covers its costs. A tonne of ethane yields 81% ethylene, of naphtha 39%; at "
              "2026 prices a tonne of ethylene costs about $360 in Texas and $1,097 in Europe. Shale lifted American "
              "ethane from about 500 to 3,361 thousand barrels a day and opened a gap of about $600 a tonne. Everyone "
              "builds in the good years, so four commodity makers earned $15bn in 2021 and lost $5bn in 2025. Ammonia "
              "is gas in another form (CF: 34.6 MMBtu a ton): in 2022 the gas in a ton cost $1,298 in Europe against a "
              "$1,070 price and $225 in America, and CF closed its British plants. Industrial gas companies sign "
              "10-20 year take-or-pay contracts and keep 17% of sales; paint makers keep 49 cents of each dollar after "
              "costs against Dow's 6. Germany's chemical output is 23% below 2021; plastics grew from 2 to 460 Mt and "
              "9% of waste is recycled; Bhopal (2,660 killed at once) and PFAS (3M's $10.5-12.5bn) show the bill for "
              "harm. The EIA's 2005 outlook expected LNG imports of 6.4 Tcf in 2025; America exported 5.5. The series "
              "calls Germany's chemical output in 2027 below 79.8 (75%).",
        handoff="Part 13 follows gas into electricity; Part 10 used the fertilizer; Part 8 produced the oil and gas; the "
                "medicines branch of the tree returns in the pharmaceuticals part.",
        outside="Percentages and arithmetic; Part 4's cost curve; Part 6's cycle; Part 8's oil and gas.",
        objectives={
            "U": ["Explain how a cracker turns ethane or naphtha into ethylene, and why its feedstock is most of its cost.",
                  "Explain why shale gave American crackers and ammonia plants an advantage, and what dear gas did to Europe.",
                  "Explain why commodity chemical profits swing while industrial gases and paint earn steadily."],
            "M": ["Compute a cracker's cash cost of a tonne of ethylene from yields, feed, by-product, fuel and other costs.",
                  "Compute the gas cost of a ton of ammonia from gas use per ton and the gas price, and compare it with the price.",
                  "Compute a take-or-pay plant's cash when the customer takes less, and compare it with selling by the tonne."],
            "D": ["Score a government outlook (the EIA's AEO2005) against outcomes and say which input decided the misses.",
                  "Turn a drinking-water limit in parts per trillion into a physical picture, and say what the arithmetic assumes."],
            "I": ["Read a chemical company's 10-K for gas use, contracts, gross margin and write-downs.",
                  "Place a company on the map: commodity chemicals, industrial gases, fertilizer, specialty."],
        },
        results=[
            ("Haber-Bosch", r"\text{N}_2 + 3\,\text{H}_2 \rightarrow 2\,\text{NH}_3"),
            ("Cost of a tonne of ethylene", r"c = \frac{p_{\text{feed}} - \text{credits}}{y_{\text{ethylene}}} + e\,p_{\text{gas}} + o"),
            ("Gas in a ton of ammonia", r"c_{\text{NH}_3} = 34.6\,p_{\text{gas}}"),
            ("Take-or-pay cash", r"F + \max(q, q_{\min})\,p - q\,c"),
            ("Recycled share", r"\frac{\text{recycled}}{\text{all plastic waste}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8, 9, 10, 12), I=(11,), D=(13,),
        also=(("The Register's rows for Part 12", "explainer/industry/data/rows_p12.py"),
              ("The cracker, the gas plant and Haber's arithmetic", "explainer/industry/works/cracker.py"),
              ("Gas, oil and chemical prices, NGLs, Eurostat, plastics, the companies' accounts",
               "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=13, level="U", widget="meritorder", prereq=(4, 6, 8),
        question="How is a product that cannot be stored sold every second, and who pays for the wires?",
        story="The part opens in Boston on 25 February 1910, where Samuel Insull described a Chicago block of 193 "
              "apartments: its customers' own peaks added to 68.5 kW, a load factor of 5.5%, but their combined peak was "
              "20 kW, 19%. The viewer runs a gas plant through a week with a cold snap: selling at spot it makes about "
              "$213m; sold forward and frozen, it loses about $214m, as Vistra lost $2.2bn in February 2021. Supply must "
              "equal demand every instant; ERCOT's 2025 peak was 83.6 GW and its load factor 67%, with the top tenth of "
              "the peak needed for 511 hours. On EIA's costs a new combined-cycle plant makes power for about $40 a MWh "
              "against nuclear's $109; the cheapest plants run first and the last one sets the price, so ERCOT's price "
              "follows gas (about $5.8 a MWh for each $1). The wires are a monopoly: a kWh in 2020 was 5.8 cents of "
              "generation, 1.4 of transmission and 3.3 of distribution, and Duke's commissions allowed returns of 9.5% to "
              "10.3%. In February 2021 Texas shed 20,000 MW, 4.5 million people lost power and at least 210 died, while "
              "the price sat at $9,000. Sales grew 9% a year in the 1950s and not at all from 2007 to 2021. California's "
              "solar deepens the duck curve and its batteries charge at noon; more solar earns less, and a battery needs "
              "bad evenings. Britain's suppliers fell from 70 to 23 as 29 failed. China makes more electricity than "
              "America and the EU together. Data centres and utilities' capital spending are rising; the EIA's 2005 "
              "outlook was 30% too high for 2025, and the series calls 2027's sales more than 1.5% above 2026's (65%).",
        handoff="Part 14 follows the other networks, water and waste; the energy transition part returns to wind, sun, "
                "storage and grids; the data centre part takes up the new load.",
        outside="Percentages and arithmetic; Part 4's cost curve and merit order; Part 5's moats; Part 6's cycle; Part 8's gas.",
        objectives={
            "U": ["Explain why electricity must be made the instant it is used, and what load factor means for its cost.",
                  "Explain the merit order: which plants run, and why the last one needed sets the price.",
                  "Explain how a regulated utility earns, and why a market can run out of power in a storm."],
            "M": ["Compute a load factor from energy and peak, and a diversity factor from customers' peaks.",
                  "Compute a plant's cost a kW-year at a capacity factor, and where two technologies cross.",
                  "Compute a utility's revenue requirement and the price of a kWh from its rate base and allowed return."],
            "D": ["Score a government outlook (AEO2005) against outcomes and say which assumption failed.",
                  "Price a hedge: show when selling forward is safe and when it is the most dangerous choice."],
            "I": ["Read EIA-930 hourly data, a rate case table in a utility's 10-K and a market monitor's report.",
                  "Place a company on the map: regulated utility, merchant generator, equipment maker."],
        },
        results=[
            ("Load factor", r"\text{LF} = \frac{\text{energy}}{\text{peak} \times 8760}"),
            ("Screening curve", r"C(f) = F + v \cdot 8.76\, f"),
            ("Merit order", r"p = c_{\text{marginal}}"),
            ("Revenue requirement", r"RR = O\&M + D + T + r_{\text{wacc}} \cdot RB"),
            ("Battery arbitrage", r"\pi = \eta \sum_{\text{dear}} p_h - \sum_{\text{cheap}} p_h"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8, 9, 10, 12), I=(11,), D=(13,),
        also=(("The Register's rows for Part 13", "explainer/industry/data/rows_p13.py"),
              ("Load factor, the screening curve, dispatch, the utility, Run it, the battery and the retailer",
               "explainer/industry/works/power.py"),
              ("EIA-930, the Monthly Energy Review, FRED, Our World in Data and the companies' accounts",
               "explainer/industry/data/SOURCES.md")),
    ),
]
