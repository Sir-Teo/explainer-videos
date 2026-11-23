"""Act I, Reading an Industry (Parts 1-7)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=1, level="U", widget="splitprice",
        question="When you pay for something, who gets the money, and why them?",
        story="The part opens in 2007 with a $299 iPod that said assembled in China: Linden, Kraemer and Dedrick "
              "followed its money and found that assembly came to $3.70, of which the assembler kept about 11 cents, "
              "while Apple took $80 and a Toshiba hard drive $73. The viewer then guesses how the $1,099 of a 256GB "
              "iPhone 17 Pro divides into five piles. The phone is taken apart into six layers made by companies in at "
              "least six economies; its parts cost about $520; value added shows why adding up sales counts the same "
              "dollar again at every link. The Dollar of one phone gives about $66 to the shop or carrier, $520 to the "
              "parts, $30 to assembly and about $244 of profit to Apple, checked against Apple's own 28 cents of profit "
              "per dollar of sales. Margins from filings, from Foxconn's 6% to Apple's services' 76%, show that the "
              "links hardest to replace keep the most. T-Mobile's accounts show a carrier selling phones below cost to win "
              "the monthly bill, and Apple's show services bringing 40% of its gross profit after the sale; an iPhone "
              "leaves about eighteen times the gross profit of a Xiaomi phone. After an intermission of iPhone sales since 2008, the label is set against value added "
              "(the iPhone 3G's $178.96 import with $6.50 of Chinese work), Micron's margins show memory's cycle from 2016 "
              "to 2025, and then the turn: in 2026 memory became the scarce link, memory prices rose five- to sevenfold, Micron's gross margin went from 40% to 81% and "
              "Samsung's chip division earned 106.5 trillion won in a quarter while its phones lost money. The part "
              "ends on the landscape as of November 2026, Ballmer's 2007 forecast, and the series' first call.",
        handoff="Part 2 measures every industry three ways with Leontief's input-output table; Part 3 reads the "
                "accounts behind the margins; Part 4 is the cost curve behind one more phone against the next design; "
                "Part 5 is the moat; Part 15 returns to the chips and Part 16 to the assemblers; Part 57 joins every "
                "model company into one web and looks for the chokepoints.",
        outside="Percentages and arithmetic. Nothing else.",
        objectives={
            "U": ["Explain why the factory named on a label can keep a few cents of a product's price.",
                  "Split a retail price into the shop, the parts, assembly, the brand's costs and its profit, and say "
                  "which pile is largest for a premium phone.",
                  "Explain why the companies hardest to replace keep the most, with an example from the phone."],
            "M": ["Compute value added along a chain from each firm's sales and show it sums to the final price.",
                  "Compute revenue and gross profit per unit from a company's segment revenue, units and margin.",
                  "Compare a price rise with a cost rise tier by tier and say who absorbs the difference."],
            "D": ["Bound a modelled profit per phone from the ranges of its inputs, and say which input matters most.",
                  "State a forecast about the industry with a date and a scoring rule, and say what would make it "
                  "wrong."],
            "I": ["Find a company's segment sales, margins, channel mix and manufacturing locations in its 10-K.",
                  "Tell a gross margin from an operating or pre-tax margin, and a unit share from a revenue share, "
                  "when comparing companies.",
                  "Draw a dated landscape of an industry's links and companies, by region."],
        },
        results=[
            ("Value added sums to the price", r"\sum_i (S_i - S_{i-1}) = S_n = \text{price}"),
            ("The Dollar", r"p = c + b + a + o + \text{opex} + \text{tax} + \pi"),
            ("Profit per unit", r"\pi_{\text{unit}} = \frac{\text{segment revenue}}{\text{units}} \times "
                                r"\text{gross margin}"),
            ("Who keeps the money", r"\text{margin rises as the number of substitutes falls}"),
            ("Pass-through by tier", r"\Delta p_k \;\text{vs}\; \Delta\text{DRAM} + G_k\,\Delta(\text{flash per GB})"),
        ],
        U=(0, 1, 2, 3, 4, 5, 8, 9, "s09_intermission", 12), I=(6, 7, 10, 14), D=(13, 15),
        also=(("The Register's rows for Part 1", "explainer/industry/data/rows_p01.py"),
              ("The chain arithmetic", "explainer/industry/works/chain.py")),
    ),
    Part(
        n=2, level="U", widget="ripple", prereq=(1,),
        question="How big is each industry, and compared with what?",
        story="The part opens in 1936 with Wassily Leontief's table of the American economy of 1919: every industry's "
              "purchases from every other on one page, which won him the Nobel prize in 1973. The viewer guesses the "
              "biggest American business three ways: by sales Amazon and Walmart (about $717bn and $713bn), by "
              "operating profit Apple, NVIDIA, Alphabet and Microsoft (about $130bn each), by employees Walmart (2.1 "
              "million) while NVIDIA employs 42 thousand. McKesson sells as much as Apple but keeps 3.6 cents of each "
              "dollar after paying for the medicines; sales count the same dollar again at every step, so the honest "
              "size of an industry is its value added, and over a country value added is GDP. Amazon shows why "
              "companies do not fit industries: by sales a retailer, by profit (AWS's $46bn of its $80bn) a cloud "
              "company. Census counts show 6.4 million businesses with employees, two in three with fewer than five "
              "people, while 2,262 firms with 5,000 or more have 36% of the jobs and half of retail's jobs sit in "
              "firms of 20,000 or more. The 2025 economy is drawn three ways, by value added ($30.9 trillion: real estate 13.7%, "
              "government 11%, manufacturing 9.5%), by jobs (158 million: government, health care and business "
              "services first) and by value added per job (utilities $845 thousand, restaurants and hotels $76 "
              "thousand), with who gets the value added, sector by sector. BEA's 2023 input-output table is read "
              "down a column (manufacturing buys 62 cents of inputs per dollar) and along a row; rounds of buying "
              "converge to the Leontief inverse ($2.25 of output for a dollar of manufactured goods), and "
              "upstreamness ranks farms and mines furthest from the final buyer. After an intermission of eighty "
              "years of GDP shares, GDP is counted again from the buyers' side, and a household's dollar is followed "
              "back through the table: two cents spent on business services become eleven cents of their value "
              "added, and about ten cents goes abroad. The part follows factory jobs from two in five (1943) to one "
              "in twelve while output rose, and prices since 2000 (school fees and childcare +175%, computers -92%) "
              "show Baumol's cost disease; it sets the United States beside other economies (China adds 27% of the world's "
              "manufacturing value added), finds the profit in a handful of technology companies and the margins "
              "from NVIDIA's 60 cents per dollar of sales to McKesson's one and a half, defines the "
              "Board's ten rows, and ends with Leontief's 1983 forecast about people and horses and the series' "
              "call on health care against manufacturing and retail in 2030.",
        handoff="Part 3 reads one company's accounts the way this part reads the economy's; Part 4 is the cost curve; "
                "Parts 8 to 55 each fill a column of the Board; Part 42 asks whether AI changes Leontief's answer; "
                "Part 57 builds the web of model companies on this table; Part 61 takes one industry through five "
                "countries.",
        outside="Percentages and arithmetic; the Student track uses a little matrix algebra, explained in the lab.",
        objectives={
            "U": ["Explain why adding up companies' sales overstates an industry, and what value added measures "
                  "instead.",
                  "Name the largest American sectors by value added and by jobs, and say why the two lists differ.",
                  "Explain why an industry's value added per job is not a measure of how hard its people work."],
            "M": ["Read an input-output table down a column (an industry's recipe) and along a row (its customers).",
                  "Follow a buyer's dollar back through the table to each industry's value added and to imports.",
                  "Compute a sector's total requirement as the sum of rounds of buying and as the Leontief inverse, "
                  "and its upstreamness for a simple chain."],
            "D": ["Say what an input-output multiplier assumes and when an impact study that uses one misleads.",
                  "State the evidence for each of the four forces behind the shift from goods to services and where "
                  "economists disagree about their weights."],
            "I": ["Find a sector's value added, its components and its share of GDP in BEA's tables, and its jobs in "
                  "the BLS's.",
                  "Separate a company's segments into the industries the statistics put them in, as for Amazon and "
                  "AWS.",
                  "Fill the Board's first three rows for an industry from public data."],
        },
        results=[
            ("Value added", r"VA_j = X_j - \sum_i Z_{ij}, \qquad \sum_j VA_j = \text{GDP}"),
            ("Direct requirements", r"a_{ij} = Z_{ij} / X_j"),
            ("The Leontief inverse", r"x = (I - A)^{-1} f = (I + A + A^2 + \cdots)\, f"),
            ("Upstreamness", r"U = (I - \Delta)^{-1}\mathbf{1}, \quad \Delta_{ij} = \frac{Z_{ij}}{Y_i - X_i + M_i - N_i}"),
            ("Value added per job", r"VA_j / E_j"),
        ],
        U=(0, 1, 2, 4, 5, 6, 11, 12, 13, 14, 15, 16, "s11_intermission"), I=(3, 7, 8, 17), D=(9, 10, 18),
        also=(("The Register's rows for Part 2", "explainer/industry/data/rows_p02.py"),
              ("BEA's and the BLS's extracts", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=3, level="U", widget="bakery", prereq=(1, 2),
        question="What do a company's accounts say about the business underneath?",
        story="The part opens in Venice in 1494, where Luca Pacioli printed the merchants' method of writing every "
              "transaction twice, and in 1914 at DuPont, where Donaldson Brown turned the books into one number, the "
              "return on investment, split into profit per dollar of sales times sales per dollar invested. The "
              "viewer is shown six real companies with their names removed (Costco, Microsoft, JPMorgan Chase, "
              "NextEra Energy, Delta and Eli Lilly) and asked to match them by five ratios. A model bakery's books are "
              "kept entry by entry until the balance sheet balances by construction; its year becomes an income "
              "statement, a balance sheet and a cash-flow statement, and a fast-growing version of it stays "
              "profitable and runs out of cash in its second year. A dollar of sales runs down five real income "
              "statements (Costco keeps 4 cents, Microsoft 47); five balance sheets show who funds each business "
              "(deposits at the bank, suppliers at Costco, customers' tickets and miles at Delta); Microsoft's "
              "fiscal 2026 profit of $134bn becomes $67bn of free cash after $116bn of spending on data centres. "
              "After an intermission of Microsoft's capital spending since 2010, Costco is shown to be paid by its "
              "members before it pays its suppliers and to earn half its operating income from membership fees; "
              "the Du Pont identity places the six on a map of margin against speed and multiplies by borrowing; "
              "the return on capital is set against its cost; Delta's seat mile rebuilds its operating income and "
              "American Express pays it more per seat than it keeps; Microsoft's segments show the profit in Office "
              "and the growth in the cloud, and two names bring Lilly 56% of its revenue; six traps in the accounts are named; the 10-K "
              "is mapped; the six are revealed. It ends with Bethany McLean's 2001 question about Enron, Enron's "
              "own figures, the restatement and the bankruptcy, and the series' call on Microsoft's free cash flow "
              "in fiscal 2027.",
        handoff="Part 4 is the cost curve behind the income statement; Part 5 the moat behind a high return on "
                "capital; Part 6 the cycle behind the cash; every industry part from 8 reads its companies' accounts "
                "this way, and the Board's margin, capital and return rows come from them.",
        outside="Percentages and arithmetic.",
        objectives={
            "U": ["Explain why a balance sheet always balances, using double entry.",
                  "Say where a dollar of sales goes at a grocer, a software company and an airline, and why the "
                  "shapes differ.",
                  "Explain how a profitable business can run out of cash."],
            "M": ["Build the three statements of a simple firm from its operations and reconcile them.",
                  "Decompose a return on equity into margin, speed and borrowing, and compute each from a 10-K.",
                  "Compute a return on invested capital and compare it with a cost of capital."],
            "D": ["Say what an accounting return can and cannot tell about value, and how leverage and buybacks "
                  "distort return on equity.",
                  "State a dated forecast about a company's cash flow with a scoring rule, and say what would make "
                  "it wrong."],
            "I": ["Find a company's segments, operating statistics and non-GAAP reconciliations in its 10-K.",
                  "Read the cash-flow statement against the income statement and name the items that separate them.",
                  "Spot the six common traps: expensed research, stock pay, paper gains, goodwill, adjusted measures "
                  "and estimates."],
        },
        results=[
            ("The balance sheet identity", r"\text{assets} = \text{liabilities} + \text{equity}"),
            ("Cash from operations", r"CFO = NI + \text{depreciation} - \Delta\text{receivables} - "
                                     r"\Delta\text{inventory} + \Delta\text{payables}"),
            ("The Du Pont identity", r"\frac{NI}{E} = \frac{NI}{S} \times \frac{S}{A} \times \frac{A}{E}"),
            ("Return on invested capital", r"ROIC = \frac{EBIT\,(1-t)}{E + D}"),
            ("Value of a stream", r"V = \frac{\text{earnings}}{r}: \; V > I \iff ROIC > r"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s07_intermission", 6, 9, 10, 13), I=(11, 12), D=(7, 8, 14),
        also=(("The Register's rows for Part 3", "explainer/industry/data/rows_p03.py"),
              ("The generic firm", "explainer/industry/works/firm.py")),
    ),
    Part(
        n=4, level="U", widget="pricewar", prereq=(1, 3),
        question="What does one more cost, and why does that decide almost everything?",
        story="The part opens in Buffalo in 1936, where Theodore Wright of Curtiss-Wright found that the labour in an "
              "aeroplane fell by about a fifth each time the number built doubled. The viewer runs a half-empty "
              "factory and is offered an order below its average cost, and takes it, because only the cost of one "
              "more counts. Delta's $57.5bn of 2025 costs are sorted by how soon cancelling flying avoids them; "
              "fixed, variable, avoidable and sunk become a two-by-two, and the Concorde fallacy is named. EIA's "
              "costs for new plants show a megawatt-hour's cost rising as a plant runs less, from $109 to nearly "
              "$1,000 for a reactor; a tank, the six-tenths rule and three pairs of real machines show economies of "
              "scale, and a market of efficient plants shows how many firms an industry has room for. Delta's belly "
              "cargo and its $8.2bn from American Express show scope; a delivery street shows density. Solar module "
              "prices fall more than a thousandfold since 1975 and, plotted against capacity built, follow Wright's "
              "law at about 30% per doubling. After an intermission of America's plants squeezed from capacity to "
              "output, Delta's seat map breaks even at 76% full against 84% flown; a hotel and a temp agency show "
              "operating leverage and Delta's 2020 shows it in fact. The Stack lines up every US power plant by "
              "the cost of one more megawatt-hour and runs a summer day on it; memory chips show the price war and "
              "the four ways out; Microsoft's segments show zero marginal cost and its limit. It ends with the IEA's "
              "2010 solar roadmap, passed fifteen years early, and the series' call on solar against coal in 2027.",
        handoff="Part 5 asks how any firm keeps a return above its cost of capital when costs fall for everyone; "
                "Part 6 is the cycle that high fixed costs and long lead times produce; the power, airline, chip and "
                "software parts return to the Stack, the seat mile, the memory cycle and zero marginal cost.",
        outside="Percentages and arithmetic; a logarithmic scale is explained in the film.",
        objectives={
            "U": ["Explain why a firm with idle capacity can profit from an order priced below its average cost.",
                  "Sort a company's costs into fixed and variable for a given horizon, and say which are sunk.",
                  "Explain why the last plant needed sets the price of electricity, and who keeps the gap."],
            "M": ["Compute a plant's cost per unit at any utilization from its capital cost, fixed and variable "
                  "costs and a cost of capital.",
                  "Fit Wright's law to prices and cumulative output and report the learning rate.",
                  "Build a merit order from capacities and marginal costs and clear it against demand."],
            "D": ["Say what an experience curve can and cannot identify, separating learning from scale, subsidy "
                  "and the feedback from price to demand.",
                  "State a dated forecast about an industry's costs or output with a scoring rule."],
            "I": ["Compute an airline's break-even load factor and the value of a point of load factor from its "
                  "10-K's seat-mile statistics.",
                  "Measure operating leverage from two years of a company's revenue and costs.",
                  "Recognize the conditions for a price war and the four ways industries escape one."],
        },
        results=[
            ("Average cost", r"AC(q) = \frac{F}{q} + c"),
            ("Cost per unit of a plant", r"\frac{\text{capital charge} + \text{fixed O\&M}}{8760\,u} + c"),
            ("Wright's law", r"c_n = c_1\, n^{-b},\qquad 2^{-b} = 1 - \text{learning rate}"),
            ("Break-even load factor", r"LF^{*} = \frac{\text{cost per seat mile}}"
                                       r"{\text{revenue per filled seat mile}}"),
            ("Operating leverage", r"DOL = \frac{(p - c)\,q}{(p - c)\,q - F}"),
            ("The marginal plant sets the price", r"p = c_{m},\quad \text{rent}_i = (p - c_i)\,q_i"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 9), I=(7, 8, 10), D=(12,),
        also=(("The Register's rows for Part 4", "explainer/industry/data/rows_p04.py"),
              ("The cost functions and the Stack", "explainer/industry/works/stack.py")),
    ),
]
