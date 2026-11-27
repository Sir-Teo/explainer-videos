"""Parts 22-28."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=22, level="U", widget="brandrun", prereq=(3, 4, 5, 20),
        question="Why can a company charge double for soap, for a hundred years?",
        story="The part opens on Procter & Gamble: $87.0bn of sales in fiscal 2026 against $43.4bn of cost of products, "
              "2.01 times; $10.2bn of advertising; Walmart 16% of its sales and its ten largest customers 43%. The viewer "
              "runs a detergent brand beside a store label at half the price: cutting the advertising earns $13m more in "
              "the first year and loses about a billion dollars of value over eight as share slides from 45% to 30%; cutting "
              "the price wins 67% of the shelf and earns less on every bottle. A dollar of P&G's sales is 50 cents of making, "
              "12 of advertising and 23 of operating profit; advertising is five times research. Gross margins run from "
              "Philip Morris International's 67% and Coca-Cola's 62% to Mondelez's 28%. Advertising wears off and is a fixed "
              "cost, so the biggest spenders pay least per unit: P&G's budget is larger than all of Clorox's sales. Walmart "
              "takes 26% of Clorox's sales and 22% of General Mills'; Costco's own label earns it higher margins than "
              "national brands. Coca-Cola's concentrate is 85% of its cases and 59% of its revenue, at a 62% gross margin "
              "against its bottler's 40%. P&G raised prices 9% in fiscal 2023 and lost 3% of volume; Hershey's margin fell "
              "from 47.3% to 33.5% on cocoa and tariffs. Altria shipped 10% fewer cigarettes in 2025 and offset most of it "
              "with price, at a 63% margin; Marlboro has led for over fifty years; PMI's smoke-free products reached 41% of "
              "its revenue. P&G's guidance ran high in fiscal 2025 and 2026; the series gives fiscal 2027 organic growth of "
              "3% or more 40%.",
        handoff="Part 23, fashion and luxury, turns to two industries that sell clothes and run on opposite rules.",
        outside="Percentages and present value; Part 3's accounts; Part 4's fixed costs; Part 5's moats; Economics, Built's "
                "logit demand, high-low pricing and reference prices.",
        objectives={
            "U": ["Explain why a branded product sells far above its cost and what the gap pays for.",
                  "Explain why advertising is a fixed cost that favours the biggest brands.",
                  "Explain the retailer's power: its size, its shelf and its own label."],
            "M": ["Model a brand's share with an advertising stock and a logit, and value holding, cutting and promoting.",
                  "Split a company's dollar of sales into making, advertising, other costs and profit.",
                  "Split sales growth into volume, price, mix and currency."],
            "D": ["Score a consumer-goods company's organic sales guidance against outcomes.",
                  "Make and state a dated, scorable forecast against a company's guidance range."],
            "I": ["Read a maker's largest-customer disclosure, advertising costs and net sales change drivers.",
                  "Read a beverage company's concentrate and finished-product split."],
        },
        results=[
            ("Advertising stock", r"S_t = (1-\delta) S_{t-1} + A_t,\quad S^* = A/\delta"),
            ("The brand's share (logit)", r"s = \frac{e^{k\sqrt{S} - \beta p + c}}{e^{k\sqrt{S} - \beta p + c} + e^{-\beta p_s}}"),
            ("Price over cost", r"\frac{\text{sales}}{\text{cost of sales}} = \frac{1}{1 - \text{gross margin}}"),
            ("Sales growth", r"g \approx g_{\text{volume}} + g_{\text{price}} + g_{\text{mix}} + g_{\text{fx}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8), I=(9,), D=(10,),
        also=(("The Register's rows for Part 22", "explainer/industry/data/rows_p22.py"),
              ("The brand against a store label", "explainer/industry/works/brand.py"),
              ("The SEC and FRED extracts", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=23, level="U", widget="seasonbuy", prereq=(4, 5, 6, 22),
        question="How do two industries that sell clothes run on opposite rules?",
        story="The part opens on Inditex, EUR 39.9bn of sales from 5,460 shops, and Hermès, EUR 16.0bn with 41% kept as "
              "operating profit, and on Inditex's gross margin quarter by quarter: 60.6%, 56.4%, 62.2%, 54.8%, the "
              "saw-tooth of clearing what did not sell. The viewer buys a season of a new T-shirt: $40, 100,000 customers on "
              "average, a 60% forecast error months ahead; $12 a shirt from far away, $16 from nearby once the season shows, "
              "$8 in the sale. The newsvendor's rule orders 162,000 shirts early and earns $2.32m, clearing 70,000; ordering "
              "late earns $2.19m; a base of 111,000 early with the hits chased late earns $2.49m at a 59.4% gross margin. "
              "NIKE's goods come from 416 contract factories it does not own, its shoes 52% from Vietnam; China exported "
              "$152bn of clothes in 2023 and quotas ended in 2005; American jobs making clothes fell from 903,000 to 79,000, "
              "and clothes got 57% cheaper against other prices. Stock sits 58 days at Ross, 71 at Inditex, 103 at NIKE and "
              "170 at Tapestry. Inditex sources within the season close to home and owes EUR 4.2bn more than it holds in "
              "stock and receivables. TJX buys from 21,000 vendors at 20-60% below full price and has doubled its sales "
              "since 2015 while Macy's and Kohl's shrank. A dollar of NIKE's sales is 57 cents of product and 10 of demand "
              "creation; it turned back to wholesale. A euro of Hermès's revenue is 29 cents of making and 41 of operating "
              "profit, from 24 leather workshops; LVMH's leather goods keep 35%, its perfumes 9%. Gucci fell from EUR 10.5bn "
              "to EUR 6.0bn while Hermès rose to EUR 16.0bn. Rana Plaza killed at least 1,132 people in 2013. The series gives "
              "Inditex's FY2026 gross margin of 58.5% or more 55%.",
        handoff="Part 24, construction, opens Act IV, Building: how the buildings and roads around us get built.",
        outside="Probability and expected value; Part 4's costs; Part 5's moats; Part 6's cycles; Part 22's brands; "
                "Economics, Built's newsvendor and reference prices.",
        objectives={
            "U": ["Explain why clothes must be ordered before demand is known and how markdowns record a wrong guess.",
                  "Explain the three answers: speed (fast fashion), buying others' mistakes (off-price), scarcity (luxury).",
                  "Explain why brands use contract factories, and what that means for the people who work in them."],
            "M": ["Solve the newsvendor problem with the critical ratio, and value a base order with a later top-up.",
                  "Compute days of stock and operating working capital from a balance sheet.",
                  "Split a company's dollar or euro of sales into making, selling and profit."],
            "D": ["Score a fashion company's gross margin guidance against its half-year results.",
                  "Make and state a dated, scorable forecast with the arithmetic of what the rest of the year needs."],
            "I": ["Read a brand's manufacturing disclosure: factories, countries, contractors and concentration.",
                  "Read a luxury group's results by business group and a fashion retailer's quarterly income statement."],
        },
        results=[
            ("The critical ratio", r"P(D \le Q^*) = \frac{p - c}{p - s}"),
            ("Expected sales, lognormal demand", r"E[\min(D,Q)] = m\,\Phi\!\left(\frac{\ln Q-\mu-\sigma^2}{\sigma}\right) + Q\left(1-\Phi\!\left(\frac{\ln Q-\mu}{\sigma}\right)\right)"),
            ("Days of stock", r"\text{days} = 365 \times \frac{\text{inventory}}{\text{cost of sales}}"),
            ("Operating working capital", r"\text{OWC} = \text{inventory} + \text{receivables} - \text{payables}"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s07_intermission", 6, 7, 8, 9), I=(10,), D=(11,),
        also=(("The Register's rows for Part 23", "explainer/industry/data/rows_p23.py"),
              ("The season bought early, late or chased", "explainer/industry/works/fashion.py"),
              ("The SEC, FRED and UN Comtrade extracts", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=24, level="U", widget="sealedbid", prereq=(3, 4, 5, 6),
        question="Why has almost everything become cheaper to make, except a building?",
        story="The part opens on the Empire State Building, opened 410 days after ground was broken in 1930, and on "
              "California's high-speed railway, about $33bn in its 2008 plan and $126.1bn by a cheaper route, or $231.3bn as "
              "first designed, in its 2026 plan; and on real output per worker since 1970, 5.66 times in manufacturing and "
              "0.63 in construction. The viewer bids for five tenders against four rivals who add 8% to estimates that are "
              "5% off either way: the lowest bid usually comes from the lowest estimate, so adding 8% keeps 1.7% on work "
              "won, adding 2% loses money, and the best markup is about 8%. Real general contractors keep about 3 cents of "
              "each dollar; quarries, equipment renters and concession owners keep far more. Fluor now takes 81% of its "
              "backlog on reimbursable terms after charges on fixed-price work; Tutor Perini lost money in four of seven "
              "years. A contractor is paid before it pays, so a growing order book floods it with cash and a shrinking one "
              "drains it: Carillion made provisions of £845m and then £1.05bn in 2017, lost £655m of cash from operations "
              "and collapsed in January 2018. Construction's prices rose 19 times from 1970 to 2025 against 6.4 for the "
              "economy. Nine in ten megaprojects run over budget; rail projects average 44.7% over with 51.4% fewer "
              "passengers. Ferrovial keeps 4.7% building and 52% owning toll roads. Quanta's backlog reached $63.7bn on the "
              "power and data-centre boom. The series gives 70% that California's trains will not carry fare-paying "
              "passengers between Merced and Bakersfield before 2034.",
        handoff="Part 25, homes, turns to the largest thing most people ever buy.",
        outside="Probability, expected value and the normal distribution; Part 3's accounts and working capital; Part 4's "
                "costs; Part 5's moats; Economics, Built's auctions (the winner's curse) and reference classes.",
        objectives={
            "U": ["Explain why sealed-bid contracting leaves builders thin margins: the winner's curse.",
                  "Explain how contract form (fixed price or cost plus) decides who carries the risk of a wrong estimate.",
                  "Explain why construction's output per worker has not grown and its prices have."],
            "M": ["Compute the chance of winning and the expected margin of a sealed bid against rivals with noisy estimates.",
                  "Model a contractor's cash from billing, payment lags and retention, and show cash and profit diverging.",
                  "Compute real output per worker and relative prices from value-added indexes and employment."],
            "D": ["Read a project's own cost and schedule forecasts against the reference class of similar projects.",
                  "Make and state a dated, scorable forecast about a megaproject's schedule."],
            "I": ["Read a contractor's backlog by contract type, its charges and its segment margins.",
                  "Read an audit office's account of a contractor's collapse."],
        },
        results=[
            ("Winning a sealed bid", r"P(\text{win} \mid b) = \prod_{j} P(b_j > b)"),
            ("The winner's margin", r"E[\,b - C \mid \text{win}\,] < m\,C"),
            ("Real output per worker", r"\frac{Q_t / L_t}{Q_0 / L_0}"),
            ("A concession's implied value", r"V = \frac{\text{price paid}}{\text{share bought}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s07_intermission", 6, 7, 8), I=(9,), D=(10,),
        also=(("The Register's rows for Part 24", "explainer/industry/data/rows_p24.py"),
              ("The tender and the contractor's cash", "explainer/industry/works/contractor.py"),
              ("The SEC, FRED and BEA extracts", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=25, level="U", widget="landbet", prereq=(3, 5, 6, 24),
        question="Where does the price of a house come from: the house, the land or the loan?",
        story="The part opens on one house: the median new American house cost $354.8k in January 2021 at a 2.74% "
              "mortgage rate and $391.3k in October 2026 at 7.33%, and the monthly payment with 10% down went from $1,301 "
              "to $2,421, most of the rise from the rate. The viewer buys land for homes to be sold in three years, owning "
              "the lot or optioning it: owning earns $21.1k a home on average and loses $29.7k in a bust; optioning earns "
              "$18.2k and loses only its $10k deposit, 182% on the money tied up against 21%; above a 48% chance of a bust "
              "it earns more even per home. D.R. Horton closed 84,202 homes in fiscal 2026 at a 20.2% gross margin and "
              "owned only 23% of its 570,600 lots; Lennar controlled 98% of its homesites by option, paid $62.7k of "
              "incentives a home and walked away from 15,500 homesites; NVR holds 169,250 lots on $920.1m of deposits. "
              "Since 2000 house prices rose 3.14 times, building materials 2.27 and consumer prices 1.87: the gap is land "
              "near jobs and the permission to build on it. The payment on the median new house took 22% of median income "
              "in 2020 and 33% in 2025. Brokers, portals, iBuyers and lenders keep little; Home Depot sells five times "
              "what the largest builder does. The series gives 60% that D.R. Horton closes fewer than 81,500 homes in "
              "fiscal 2027.",
        handoff="Part 26, property, turns to the offices, shops and warehouses that companies rent, and the investors who "
                "own them.",
        outside="Probability and expected value; options as the right but not the duty to buy; the annuity formula; Part "
                "3's accounts and inventory; Part 5's moats; Part 6's cycle; Part 24's construction; Economics, Built's "
                "city (land rent and the monocentric city) and credit chapters.",
        objectives={
            "U": ["Explain why what a buyer can borrow, and so the mortgage rate, sets what a buyer can pay.",
                  "Explain why house prices have outrun building costs: land near jobs and the permission to build.",
                  "Explain why the largest builders control most of their land by option rather than own it."],
            "M": ["Compute the expected profit and return on capital of owning against optioning land under two futures.",
                  "Compute a fixed-rate mortgage payment and split a change in it into the effects of price and rate.",
                  "Compute price-to-income ratios and the payment's share of income from published series."],
            "D": ["Read a builder's guidance against its outcome, and make and state a dated, scorable forecast."],
            "I": ["Read a homebuilder's closings, margins, incentives and land position in its filings.",
                  "Read a mortgage guarantor's book and forecasts, and a broker's and a lender's margins."],
        },
        results=[
            ("Owning against optioning", r"E[\pi] = (1 - p)\,\pi_{\text{boom}} + p\,\pi_{\text{bust}}, \quad \pi^{\text{opt}}_{\text{bust}} = \max(\pi, -D)"),
            ("The crossing point", r"p^{*} = \frac{\pi^{\text{own}}_{\text{boom}} - \pi^{\text{opt}}_{\text{boom}}}{(\pi^{\text{own}}_{\text{boom}} - \pi^{\text{opt}}_{\text{boom}}) + (\pi^{\text{opt}}_{\text{bust}} - \pi^{\text{own}}_{\text{bust}})}"),
            ("A fixed-rate mortgage payment", r"M = P\,\frac{r}{1 - (1 + r)^{-n}}"),
            ("Price over income", r"\frac{\text{median price}}{\text{median household income}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s07_intermission", 6, 7), I=(8,), D=(9,),
        also=(("The Register's rows for Part 25", "explainer/industry/data/rows_p25.py"),
              ("The land deal and the mortgage", "explainer/industry/works/builder.py"),
              ("The SEC and FRED extracts", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=26, level="U", widget="refinance", prereq=(3, 4, 6, 25),
        question="What is a building worth, and why does that number move so much when the building does not?",
        story="The part opens on the Federal Reserve's commercial property price index, down 39% from 2007 to 2009 and 13% "
              "from 2023 to 2025 while the buildings stood still, and on a 2022 study's estimate that New York's offices lost "
              "45% of their value in 2020. The viewer owns an office bought in 2019 for $200m with a $130m loan: by 2026 it is "
              "65% let, its income has fallen from $10m to $3m because its costs are fixed, buyers want 7.5% instead of 5%, and "
              "it is worth $40m; a lender will lend $24m, leaving a $106m gap, so the owner pays in, hands back the keys or "
              "asks for time. A warehouse bought the same year, its rents up by half, refinances with money to spare. A point "
              "of rate takes 20% off a building at 4%; Realty Income paid prices yielding 5.5% in 2021 and 7.4% in 2024. The "
              "lease is the asset: WeWork owed $47bn of rent over 14 years against members committed for 15 months, lost "
              "$13bn in four years and filed for bankruptcy in 2023. Banks hold $3.2tn of commercial property loans; "
              "delinquencies have doubled since 2019 but are far from 1991's 12%. Storage, malls and warehouses keep over 45 "
              "cents of each dollar, offices and senior housing under ten; BXP's offices fell from 93% let to 87% and San "
              "Francisco to 77%, while Prologis re-let warehouses at rents about 50% higher. CBRE, the largest services firm, "
              "runs other people's buildings for 3 cents on the dollar. The series gives 55% that BXP's occupancy will be 91% "
              "or more at the end of 2027.",
        handoff="Part 27, shipping and ports, opens Act V, Moving, with how moving a tonne across an ocean became nearly free.",
        outside="Present values and yields; leverage and loan-to-value; Part 3's accounts and depreciation; Part 4's fixed "
                "costs; Part 6's cycle; Part 25's homes and mortgages; Economics, Built's assets (the user cost and the "
                "option to wait), city and bank chapters.",
        objectives={
            "U": ["Explain why a building's value is its income divided by a capitalization rate, and why rates move it.",
                  "Explain why a building's income moves more than its rent: fixed running costs.",
                  "Explain why the lease, its tenant and its length, is what a landlord really owns."],
            "M": ["Compute value, the effect of a one-point change in the cap rate and a building's break-even occupancy.",
                  "Compute the largest new loan by loan-to-value, interest-cover and debt-yield tests, and the refinancing gap.",
                  "Compute a development's margin and the cap rate implied by its stabilized yield."],
            "D": ["Read a landlord's own occupancy promise against outcomes, and make and state a dated, scorable forecast."],
            "I": ["Read a REIT's occupancy, rent changes on renewal, impairments and acquisition yields in its filings.",
                  "Read the Federal Reserve's financial stability reports on commercial property and its lenders."],
        },
        results=[
            ("Value as income over a rate", r"V = \frac{\text{NOI}}{r}, \quad \frac{V_{r + 0.01}}{V_r} = \frac{r}{r + 0.01}"),
            ("Net operating income", r"\text{NOI} = A \cdot p \cdot s - F"),
            ("The new loan", r"L = \min\left(0.6\,V,\ \frac{\text{NOI}}{1.25\,i},\ \frac{\text{NOI}}{0.10}\right)"),
            ("A development's margin", r"m = \frac{y}{r} - 1"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s07_intermission", 6, 7, 8), I=(9,), D=(10,),
        also=(("The Register's rows for Part 26", "explainer/industry/data/rows_p26.py"),
              ("The building, the loan and the development", "explainer/industry/works/building.py"),
              ("The SEC and FRED extracts", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=27, level="U", widget="slowsteam", prereq=(4, 6, 8),
        question="How did moving a tonne across an ocean become nearly free, and why do the companies that do it swing between "
                 "fortune and ruin?",
        story="The part opens on a pair of trainers whose ocean voyage cost about 62 cents in 2025 at ZIM's average freight "
              "of $1,551 a TEU, and on the Suez Canal, where traffic fell from about 55 ships a day to two when the Ever Given "
              "blocked it in March 2021. The viewer owns ships for thirty years in a market where a ship earns $10k a day "
              "when the fleet is idle and $100k when it is full, and ships ordered today arrive in three: ordering with the "
              "market buys ships at $112m that arrive into the bust and returns 8%; ordering against it buys at $66m and "
              "returns 136%. Fuel a day rises with the cube of speed, so ships sail slowly. The world's ports handled 913m TEU "
              "in 2024; the fleet grew from 25m TEU to 33.3m in four years, with 11.3m more on order. ZIM's freight went "
              "from $1,009 a TEU in 2019 to $3,240 in 2022 and $1,203 in 2023; it earned $4.6bn in 2021 and lost $2.7bn in "
              "2023, while the lessors that rent it ships kept steady margins. Houthi attacks halved traffic through Suez "
              "and nearly doubled it round the Cape; in 2026 the Strait of Hormuz fell from 85 ships a day to about three, "
              "and Frontline's tankers earned $148,500 a day against a $24,100 breakeven. Forwarders keep steady thin "
              "margins; the Jones Act protects half of Matson's ocean revenue. The series gives 60% that Hapag-Lloyd "
              "completes its purchase of ZIM by 30 June 2027.",
        handoff="Part 28, airlines, turns to the industry that made distance fast and has lost money over most of its history.",
        outside="Cubes and squares; expected value; Part 4's fixed costs; Part 6's cycle; Part 8's oil; Part 24's toll roads; "
                "Economics, Built's trade (gravity and trade costs) and its cobweb cycles.",
        objectives={
            "U": ["Explain why a full fleet can charge almost anything and a half-empty one almost nothing.",
                  "Explain why ships ordered in a boom arrive into a bust, and why the boom builds the bust.",
                  "Explain why a few canals and straits can move the whole market."],
            "M": ["Compute a voyage's fuel and time at different speeds and find the cheapest speed.",
                  "Simulate a freight cycle with delivery lags and compare ordering rules by their returns.",
                  "Compute the freight cost per unit of goods from a rate per TEU."],
            "D": ["Read a company's changing forecasts of its own year, and make and state a dated, scorable forecast."],
            "I": ["Read a container line's freight rate, volumes and fleet, and a tanker owner's TCE and breakeven.",
                  "Read chokepoint transit data and port traffic to track disruptions."],
        },
        results=[
            ("Fuel and speed", r"\text{fuel a day} \propto v^{3}, \quad \text{fuel a mile} \propto v^{2}"),
            ("A voyage's cost", r"C(v) = \frac{D}{24v}\left(c_{\text{ship}} + p_{\text{fuel}}\,f_{0}\left(\frac{v}{v_{0}}\right)^{3}\right)"),
            ("Utilization", r"u = \frac{\text{cargo}}{\text{fleet}}, \quad e(u)\ \text{steep as}\ u \to 1"),
            ("Freight per unit", r"\frac{\text{rate per TEU} \times \text{TEU per box}}{\text{units per box}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s07_intermission", 6, 7, 8), I=(9,), D=(10,),
        also=(("The Register's rows for Part 27", "explainer/industry/data/rows_p27.py"),
              ("The shipping market and the voyage", "explainer/industry/works/ship.py"),
              ("The SEC, IMF PortWatch, World Bank and FRED extracts", "explainer/industry/data/SOURCES.md")),
    ),
]
