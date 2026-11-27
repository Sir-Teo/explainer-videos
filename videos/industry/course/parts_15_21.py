"""Act III, Making (Parts 15-21)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=15, level="U", widget="fab", prereq=(4, 5, 6),
        question="Why do the most advanced chips come from so few factories?",
        story="The part opens with Gordon Moore's article of April 1965 (the components on the most economical chip "
              "doubling every year, 65,000 by 1975) and with Hsinchu in 1987, where TSMC set out to make other "
              "companies' chips and design none of its own; in 2025 it made 12,682 products for 534 customers. The "
              "viewer chooses between building a $20bn fab and booking a foundry at $17,000 a wafer: at 5,000 wafers a "
              "month a good die costs $29 from the foundry and $183 from a half-empty fab still learning its process, "
              "and owning first pays at about 32,000. A chip is a loop of film, resist, light and etch repeated layer on "
              "layer; a 300 mm wafer holds about 640 dies of 100 mm2, and random defects make an 800 mm2 die yield half "
              "as often. TSMC spends a third to a half of its revenue on fabs every year, used about 88% of its capacity "
              "in 2025 and earned about $8,100 a wafer. The industry split into fabless designers (Nvidia, from $6.9bn "
              "to $215.9bn of revenue without a fab) and foundries, while Intel's foundry lost $10.3bn in 2025; ASML is "
              "the only maker of EUV machines. America's chip output rose about 5,089 times since 1972 as the real price "
              "fell 98%. Memory swings from loss to boom (Micron, from a $2.3bn quarterly operating loss to $43.8bn of "
              "operating profit in a quarter); the analog makers ride cars and factories. High-performance computing rose "
              "from 43% to 68% of TSMC's revenue; its three 2-3 nm fabs are all in Taiwan; America subsidizes fabs at "
              "home and restricts who may buy. WSTS forecast $975bn for 2026 and sales passed $1.22 trillion by "
              "September; the series calls more than $1.8 trillion for the year (65%).",
        handoff="Part 16, electronics, follows the chips into the devices, and asks why the company that builds the device "
                "keeps the least of it.",
        outside="Percentages, logarithms and exponentials; Part 4's fixed and variable costs; Part 5's moats; Part 6's cycle.",
        objectives={
            "U": ["Explain how a chip is made, and why a fab costs the same whether it is full or empty.",
                  "Explain the split between fabless designers, foundries and integrated makers, and why it happened.",
                  "Explain why the most advanced chips come from a few fabs, one foundry and one maker of machines."],
            "M": ["Compute gross dies on a wafer, the yield at a defect density and the cost of a good die.",
                  "Compute a fab's cost per wafer at a given loading and the volume at which owning beats booking.",
                  "Compute a doubling time from two counts, and what operating leverage does to a memory maker's profit."],
            "D": ["Score two forecasts (Moore's of 1965 and WSTS's of December 2025) and say which assumption failed.",
                  "Judge how much of the 2026 boom is price and how much volume, and what would end it."],
            "I": ["Read a foundry's revenue by node and platform, its utilization and its capital spending in a 20-F.",
                  "Place a chip company on the map: foundry, fabless, integrated, memory, equipment, design software."],
        },
        results=[
            ("Gross dies", r"N = \frac{\pi r^2}{A} - \frac{\pi d}{\sqrt{2A}}"),
            ("Yield", r"Y = e^{-A D}"),
            ("Cost of a good die", r"c = \frac{F/(12v) + c_w}{N\,Y}"),
            ("Doubling time", r"T = \frac{t_1 - t_0}{\log_2(n_1/n_0)}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, "s09_intermission", 8, 9, 10, 11), I=(12,), D=(13,),
        also=(("The Register's rows for Part 15", "explainer/industry/data/rows_p15.py"),
              ("Dies, yield, the learning curve, the fab and Run it", "explainer/industry/works/fab.py"),
              ("TSMC's fabs", "explainer/industry/data/tables.py"),
              ("FRED, Our World in Data, the SEC's foreign filers and the companies' accounts",
               "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=16, level="U", widget="assembler", prereq=(1, 4, 5, 15),
        question="Why does the company that builds the device keep the least of it?",
        story="The part opens with Stan Shih, the founder of Acer, who in 1992 drew the value added along the computer "
              "industry and found 'a smile-shaped curve', with manufacturing at the bottom. In 2025 Hon Hai (Foxconn) took "
              "in NT$8.1 trillion, about $260bn, and kept 2.3 cents in the dollar; Apple kept 28 cents of $479bn. The viewer "
              "runs an assembler offered 20 million devices a year at $30 each if it builds an $800m plant: worth -$194m "
              "if the brand moves the work after three years and +$420m if it renews, so the plant pays only above a 32% "
              "chance of renewal. A device is assembled on a surface-mount line and by hand; Apple's hardware is made by "
              "partners in China, India, Japan, South Korea, Taiwan and Vietnam. The Works' $900 device splits into parts, "
              "a $30 fee and the brand's $260 of profit: the smile from arithmetic. Six contract manufacturers kept 0-5 "
              "cents a year for fifteen years; turnkey revenue makes the margin look thin (3% against 50% on the fee), and "
              "Hon Hai turns its assets 1.6 times a year for a 9.6% return on equity. Its servers overtook its phones in "
              "2025, its largest customer fell from 54% to 44% of revenue, and its servers arm earned 4.7 cents against "
              "1.4. Apple's services earn a 76% gross margin. Connector makers keep 10-20 cents; LG Display lost money in "
              "six of ten years. Televisions' price index fell 99.4% since 1951. Intel's PC chips earned 29-35% while HP's "
              "and Dell's PCs earned 5-8%, and HP's printing 18.7%. US server imports rose from $23bn (2017) to $165bn "
              "(2025). Hon Hai's assets in China shrank while Vietnam's, America's, Mexico's and India's grew. Tariffs "
              "from 2018 hardly moved phones or laptops until 2023-25; then China's share of US phone imports fell from 81% "
              "to 45% and of laptops from 66% to 18%, and the Supreme Court struck down the emergency tariffs in February "
              "2026. The Commerce Secretary's 2025 forecast that iPhone assembly would come to America has not come true; "
              "the series calls India above half of US smartphone imports in 2026 (55%).",
        handoff="Part 17, cars, turns to a product whose makers also struggle to keep much of what they sell.",
        outside="Percentages and discounting; Part 1's phone and its dollar; Part 4's fixed costs; Part 5's moats; Part 15's chips.",
        objectives={
            "U": ["Explain Shih's smile: why value added is high at the parts and brand ends and low in assembly.",
                  "Explain how a device is assembled, and who does the work for which brands.",
                  "Explain why tariffs moved assembly slowly, and where it went."],
            "M": ["Value a plant built for one customer's order, with and without renewal, and find the break-even chance.",
                  "Show how turnkey revenue changes an assembler's margin without changing its profit.",
                  "Decompose a return on equity into margin, asset turnover and leverage."],
            "D": ["Score a forecast (the Commerce Secretary's, April 2025) against trade and employment data.",
                  "Judge how far a quality-adjusted price index measures what buyers gained."],
            "I": ["Read an assembler's segment, customer and geographic notes (Hon Hai's) and a brand's gross margins.",
                  "Read customs data by partner to see where a product is assembled, and when it moved."],
        },
        results=[
            ("Plant value", r"V(p) = V_{\text{order}} + p\,V_{\text{renewal}}"),
            ("Break-even renewal", r"p^* = -V_{\text{order}} / V_{\text{renewal}}"),
            ("Turnkey margin", r"m = \frac{\pi}{q\,(\text{parts} + \text{fee})}"),
            ("DuPont", r"\frac{NI}{E} = \frac{NI}{S}\cdot\frac{S}{A}\cdot\frac{A}{E}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, "s09_intermission", 8, 9, 10, 11), I=(12,), D=(13,),
        also=(("The Register's rows for Part 16", "explainer/industry/data/rows_p16.py"),
              ("The device, the assembler and Run it", "explainer/industry/works/device.py"),
              ("UN Comtrade, BLS, FRED, the SEC extracts and Hon Hai's statements", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=17, level="U", widget="carmaker", prereq=(4, 5, 6, 16),
        question="Why is it so hard to make money making the most desired product of the century?",
        story="The part opens on 2025, a year in which Ford lost 4.4 cents on every dollar of revenue, Stellantis 14.5 and "
              "Honda 1.9, Volkswagen kept 2.1 and Toyota 7.6 (in its year to March 2026). Then three arrivals: Ford's moving "
              "line at Highland Park, which cut the time to assemble a chassis from 12 hours 28 minutes to 1 hour 33 minutes "
              "in 1913-14; Toyota's production system (jidoka and just-in-time, in Toyota's words); and the electric car "
              "and China, whose car exports rose from $4bn (2015) to $110bn (2025). The viewer runs a plant whose orders come "
              "in 30% below plan while a rival's identical plant sells just as slowly: discounting $3,000 is the better reply "
              "to either move, so both discount and both lose $486m instead of $90m; cutting a shift each loses $63m. A car "
              "plant follows Toyota's five steps; America's 2022 census counts 213,363 people in 210 assembly plants and "
              "roughly 44 hours of work per vehicle. Of a dollar shipped by the assembly plants, 76 cents paid other "
              "companies for parts and materials and 4.7 paid the plants' payroll; the dealer kept 4.9 cents of the price "
              "of a new car. R&D per vehicle runs from $971 at Toyota to $76,472 at Lucid; profit per vehicle from Ferrari's "
              "$132,366 to Lucid's -$170,321. The Works' plant breaks even at 66% of capacity; America's plants have "
              "averaged 77% since 1948 and ran at 65% in 2025; Rivian built 42,284 cars in a plant for 215,000. Lean "
              "production cut stock until the chip shortage of 2021 emptied the dealers' lots (0.42 months of sales in "
              "January 2022), though chips were 1.1% of what the assemblers bought. Suppliers kept no more than their "
              "customers. A dealer earns almost half its gross profit from parts and service and almost a third from "
              "finance and insurance; GM Financial earned $2.8bn and Ford Credit $2.6bn. Ford Pro earned $4,599 a "
              "vehicle, Ford Blue $1,109 and Model e lost $27,000; Honda's motorcycles earned ¥732bn while its cars lost "
              "¥1.41tn. Battery packs fell 90% in cost (DOE); electric cars reached 25% of world sales and 53% of China's; "
              "the old makers wrote off about $40bn of electric plans in 2025. China sold 34.4 million vehicles, 47.9% "
              "new energy; America and Europe raised tariffs against its electric cars. The 2023 UAW contract raised wages "
              "27% by 2027, about 1.3 cents of a plant's dollar of shipments; the strike cost GM $1.1bn. Tesla's 2016 plan "
              "of 500,000 cars by 2018 was met in 2020; the EIA's 2017 outlook was close for 2025; China's 2017 plan "
              "undershot 2025 by more than half. The series calls the world's electric share for 2026 below 32% (65%).",
        handoff="Part 18, aerospace, turns to an industry with only two makers of large airliners, and why the engine "
                "maker sells at a loss.",
        outside="Percentages, break-even and present value; Part 4's fixed and variable costs; Part 5's moats; Part 6's "
                "cycle; Part 16's assemblers; Economics, Built Part 43 on car demand.",
        objectives={
            "U": ["Explain why a car plant's profit depends so strongly on volume, and why the upside is capped.",
                  "Explain how a car's price divides between suppliers, the maker and the dealer.",
                  "Explain what lean production changed and what it bet on."],
            "M": ["Find a plant's break-even volume from its contribution margin and fixed costs.",
                  "Solve a two-firm pricing game and show it is a prisoner's dilemma.",
                  "Compute R&D and profit per vehicle from a carmaker's accounts and units."],
            "D": ["Score forecasts of the electric car (Tesla 2016, EIA 2017, China 2017 and 2020) against outcomes.",
                  "Make and state a dated, scorable forecast from a fitted logistic curve."],
            "I": ["Read a carmaker's segment results (Ford's three businesses, GM's finance arm) and a dealer's gross "
                  "profit by line.",
                  "Read the Economic Census for an industry's materials, payroll and employment."],
        },
        results=[
            ("Break-even volume", r"q^* = \frac{F + s\,C_{\text{shift}}}{p - c}"),
            ("Contribution margin", r"m = p - c"),
            ("Own- and cross-price demand", r"q_i = A\,(p_i/\bar p)^{-\varepsilon_o}(p_j/\bar p)^{\varepsilon_c}"),
            ("Logistic share", r"s(t) = \frac{100}{1 + e^{-(a + b t)}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, "s09_intermission", 8, 9, 10, 11, 12, 13), I=(14,), D=(15,),
        also=(("The Register's rows for Part 17", "explainer/industry/data/rows_p17.py"),
              ("The plant, the platform, the duel and the loan", "explainer/industry/works/auto.py"),
              ("The SEC, FRED, Census, UN Comtrade, EIA and IEA extracts", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=18, level="U", widget="airframer", prereq=(4, 5, 6, 17),
        question="Why are there only two makers of large airliners, and why does the engine maker sell at a loss?",
        story="The part opens on 2025: Airbus delivered 793 airliners and Boeing 600, Airbus had 8,754 more on order, Boeing "
              "had lost $36bn from 2019 to 2024, and GE's commercial engine business sold $8.3bn of new engines against "
              "$25.0bn of spare parts and servicing. The viewer chooses between a new airliner ($20bn, seven years, 20% less "
              "fuel) and new engines on the old one ($3bn, four years, 14%) while a rival chooses too: re-engining is the "
              "better reply either way, as Airbus and Boeing chose in 2010-11, but with a bigger leap both build new and both "
              "end worse off. An airliner is assembled from sections, wings and engines made in many places; Boeing bought "
              "Spirit AeroSystems, its 737 fuselage maker, for $8.4bn in December 2025. In the Works' programme the first "
              "aircraft costs $450m against a $110m price, the learning curve brings the 137th below the price, and the "
              "programme spends $20bn before its first delivery, bottoms out at -$25.7bn and breaks even in year 15 after "
              "990 aircraft; at 90% learning it never does. Program accounting books each delivery at the average cost and "
              "defers the rest ($2.7bn on the undelivered 777X); the 777X, promised for 2020, is now expected in 2027 after "
              "$8.4bn of reach-forward losses. The two makers hold 11.0 and 10.2 years of orders; a newcomer far up its "
              "learning curve needs about $100m a jet to break even, while an incumbent's 9,240th costs about $33m. Launch "
              "aid moves a flop's losses to governments; the WTO let America tax $7.5bn of European goods a year and Europe "
              "$4.0bn of American ones, until a 2025 agreement restored tariff-free trade in aircraft. A turbofan's fan "
              "pushes most of its air around the core; the Works' engine sold $3m below cost pays back in year 14 from "
              "servicing. TransDigm, with 90% proprietary parts and 55% aftermarket sales, kept 18.4 cents of each dollar "
              "since 2015 while Boeing lost 2.1 and Spirit 5.5. AerCap owns 1,501 aircraft and sold 108 old ones for $819m "
              "above book. Lockheed takes 72% of its sales from the US government and 27% from the F-35; defence primes keep "
              "5% to 10%; America spent $1,125bn on defence in 2025 and the world $2.77tn (SIPRI). Boeing's 787 was three "
              "years late and the 777X seven; the series gives the first 777-9 delivery by the end of 2027 55%.",
        handoff="Part 19, machinery, turns to the industry that makes the machines that make everything else.",
        outside="Percentages and present value; Part 4's learning curve and fixed costs; Part 5's moats; Part 6's cycle; "
                "Part 17's duel; Economics, Built's game theory and Part 44 on industrial organization.",
        objectives={
            "U": ["Explain why a new airliner takes tens of billions and a thousand aircraft to pay back.",
                  "Explain why the industry has only two makers of large airliners.",
                  "Explain why engines and many parts are sold for the servicing that follows."],
            "M": ["Compute unit costs on a learning curve and the unit at which cost falls below price.",
                  "Value an engine sold below cost from its discounted servicing, and find its payback year.",
                  "Solve the new-or-re-engine game and show how a parameter flips it into a dilemma."],
            "D": ["Score Boeing's first-delivery targets for the 787 and 777X against outcomes.",
                  "Make and state a dated, scorable forecast of a first delivery."],
            "I": ["Read program accounting: accounting quantities, deferred production costs and reach-forward losses.",
                  "Read a defence contractor's customer and contract mix, and SIPRI's budgets."],
        },
        results=[
            ("Wright's learning curve", r"c(n) = c_1\,n^{\log_2 \ell}"),
            ("Unit at which cost falls below price", r"n^* = (c_1/p)^{1/(-\log_2 \ell)}"),
            ("Present value of servicing", r"PV = s\,\frac{1 - (1+r)^{-T}}{r}"),
            ("Buyers' split by fuel burn", r"s_i = \frac{b_i^{-k}}{\sum_j b_j^{-k}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, "s09_intermission", 8, 9, 10, 11), I=(12,), D=(13,),
        also=(("The Register's rows for Part 18", "explainer/industry/data/rows_p18.py"),
              ("The programme, the engine, launch aid and the duel", "explainer/industry/works/aircraft.py"),
              ("The SEC, FRED and SIPRI extracts", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=19, level="U", widget="tender", prereq=(4, 5, 6, 18),
        question="How do the companies that make the machines earn more from them after the sale than at it?",
        story="The part opens on Otis, which in 2025 sold $5.0bn of new elevators at a 4.8% margin and $9.4bn of service at "
              "25.1%, looking after about 2.5 million lifts and escalators; on Caterpillar's backlog, $30bn at the end of "
              "2024 and $78bn by September 2026; and on the 5 million industrial robots at work. The viewer bids for a fleet "
              "of 100 machines whose servicing is worth $0.6m each: cutting the price below cost is the better reply either "
              "way, so both makers cut and each earns $25m instead of $45m; if only 30% of owners buy service from the maker, "
              "holding pays, and the threshold is an 83% attach rate. Caterpillar sold $67.6bn in 2025, its largest segment "
              "now engines and turbines; Deere $45.7bn, with $6.3bn from financing. Equipment investment swings from 7.9% of "
              "GDP (1979) to 4.6% (2009); machinery orders fell 29% in 2009; Caterpillar's sales fell 41% from 2012 to 2016. "
              "Otis's service is 65% of its sales and 91% of its segment profit; a model maker's service revenue falls 2% in "
              "a year when new sales fall 44%. Caterpillar's 150 dealers serve 190 countries; Deere has 2,050 dealer "
              "locations in North America; financing is 13.8% of Deere's revenue; United Rentals owns 1.1 million machines. "
              "Machinery book-to-bill fell to 0.90 in 2009; Caterpillar's profit fell in a record year as prices fell and "
              "tariffs raised costs, until the Supreme Court struck down the IEEPA tariffs in February 2026. Since 1990 "
              "America's machinery output rose 16% while its jobs fell 23%. China installed 354,000 robots in 2025, 59% of "
              "the world's, 55% of them made by Chinese makers; South Korea has 1,066 robots per 10,000 factory workers. "
              "China's excavator exports rose from $1.2bn (2015) to $10.8bn (2025), passing Japan. GE, 3M and Honeywell "
              "split themselves up between 2023 and 2026. The IFR's one-year robot forecasts were close and its medium-term "
              "one high; the series gives 2026 installations below the IFR's 655,000 55%.",
        handoff="Part 20, pharmaceuticals, turns to an industry where most of the cost is in the discovery.",
        outside="Percentages and present value; Part 5's moats; Part 6's cycle; Part 18's engines sold for their "
                "servicing; Economics, Built's game theory and Part 62 on the diversification discount.",
        objectives={
            "U": ["Explain why an installed base earns more, and more steadily, than new machine sales.",
                  "Explain why capital goods swing harder than the economy.",
                  "Explain what dealers, captive lenders and rental companies do."],
            "M": ["Solve the tender and find the attach rate at which makers fight for the sale.",
                  "Compute segment margins and shares of profit from a filing.",
                  "Compute book-to-bill and read a backlog."],
            "D": ["Score the IFR's robot forecasts against outcomes.",
                  "Make and state a dated, scorable forecast against an industry body's own."],
            "I": ["Read a machine maker's segments, backlog and profit bridge.",
                  "Read the IFR's installations and density by country."],
        },
        results=[
            ("A machine's value to its maker", r"v = p - c + s\,a"),
            ("The attach threshold for cutting", r"a^* = \frac{(p_h - c)/2 - (p_c - c)}{s/2}"),
            ("Book-to-bill", r"B = \frac{\text{orders}}{\text{shipments}}"),
            ("Installed base", r"N_t = \sum_{k=t-L+1}^{t} q_k"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8, 9), I=(10,), D=(11,),
        also=(("The Register's rows for Part 19", "explainer/industry/data/rows_p19.py"),
              ("The tender and the installed base", "explainer/industry/works/machine.py"),
              ("The SEC, FRED, robot and Comtrade extracts", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=20, level="U", widget="pipeline", prereq=(4, 5, 6, 19),
        question="Why does a pill that costs cents to make sell for dollars, and then one day for cents?",
        story="The part opens on Lipitor: Pfizer sold $10.7bn of it in 2010 and $3.9bn in 2012, the year after its US "
              "exclusivity ended; on Lilly's tirzepatide, $36.5bn in 2025 and 56% of Lilly's revenue; and on Keytruda, 49% "
              "of Merck's sales, whose main US patent ends in 2028. The viewer decides whether to pay $250m for Phase III "
              "once Phase II has shown how big the market may be: going on is worth $2.6bn if it is big and loses $108m if it "
              "is small, and the right to stop is worth $76m. With BIO's odds for 2011-2020, 52% of drugs pass Phase I, 29% "
              "Phase II, 58% Phase III and 91% the FDA's review: 7.9% of candidates entering trials are approved, after 10.5 "
              "years, and one approval needs 12.7 candidates entering Phase I. Phase II success runs from 48% in hematology "
              "to 15% in urology; approval from 24% in hematology to 5% in oncology. With illustrative stage costs, an "
              "approved drug costs about $1.2bn out of pocket and $2.6bn with the waiting counted; research is 41% of "
              "Regeneron's revenue and 6% of Teva's, and $103bn across fourteen companies in 2025. A model drug that peaks "
              "at $2bn a year earns 96% of its value before its exclusivity ends; the FDA finds generic prices 39% below "
              "the brand's with one maker and over 95% below with six. Drug producer prices rose 8.3 times since 1982 "
              "against 3.3 for all consumer prices; about fifty novel drugs are approved a year. Pfizer's revenue doubled "
              "in the pandemic years and fell back; Merck bought Cidara for $9.2bn. Medicare's first ten negotiated prices "
              "would have saved $6bn, 22%, in 2023, and took effect on 1 January 2026. Lilly spent $7.8bn on plant in "
              "2025 and its third-quarter revenue in 2026 rose 39%; Moderna's revenue fell from $19.3bn (2022) to $1.9bn "
              "(2025); a dollar of thirteen companies' revenue went 26 cents on making, 20 on research, 36 on everything "
              "else and 18 to profit. Lilly beat the top of its 2025 guidance by 7%; the series gives its 2026 revenue at "
              "least $92.0bn, the top of its raised range, 55%.",
        handoff="Part 21, medical technology, turns to the devices, where the product is a machine and the customer is "
                "often a surgeon.",
        outside="Probability and present value; Part 4's cost curve; Part 5's moats; Part 6's cycle; Statistics, Built's "
                "trials and Economics, Built's pricing and patents.",
        objectives={
            "U": ["Explain why each approved medicine must pay for many failures and for years of waiting.",
                  "Explain why a protected drug's price is set by its value, not its cost of making, and what happens at "
                  "the patent cliff.",
                  "Explain what rebates, list and net prices, and Medicare's negotiation are."],
            "M": ["Compute the probability of approval and the cost per approved drug from phase odds and costs.",
                  "Value the option to stop before Phase III.",
                  "Value a drug's life before and after its exclusivity ends."],
            "D": ["Score a drug company's own guidance against its results.",
                  "Make and state a dated, scorable forecast against a company's raised guidance."],
            "I": ["Read a drug company's revenue by product, its research spending and its patent table.",
                  "Read BIO's phase success rates and the FDA's study of generic prices."],
        },
        results=[
            ("Probability of approval", r"P = \prod_{k=1}^{4} q_k"),
            ("Cost per approved drug", r"C = \frac{1}{P} \sum_{k=1}^{4} c_k \prod_{j<k} q_j"),
            ("Capitalized cost", r"C_{cap} = \frac{1}{P} \sum_{k} c_k \Big(\prod_{j<k} q_j\Big) (1+r)^{T - t_k}"),
            ("The option to stop", r"V = p\,\max(V_b, 0) + (1-p)\,\max(V_s, 0) - \big(p V_b + (1-p) V_s\big)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8, 9, 10), I=(11,), D=(12,),
        also=(("The Register's rows for Part 20", "explainer/industry/data/rows_p20.py"),
              ("The pipeline, the drug and the option to stop", "explainer/industry/works/pharma.py"),
              ("The SEC and FRED extracts", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=21, level="U", widget="placement", prereq=(4, 5, 19, 20),
        question="Who is the customer when the one who uses it, the one who chooses it and the one who pays are three "
                 "different people?",
        story="The part opens on Intuitive's da Vinci robots: about 3.15 million operations in 2025 on 11,106 robots, a robot "
              "selling for $0.7m to $3.1m and each operation bringing $900 to $3,700 of instruments; and on the surgeon who "
              "chooses, the hospital that buys, the insurer that pays and the patient. The viewer sells a robot for $2m or "
              "places it free for $1,000 an operation: selling brings 61 of 101 hospitals and $258m, placing all 101, 30,300 "
              "operations a year and $232m, with eleven placements losing money; at about $1,160 an operation placing pays "
              "as well; Intuitive had 1,810 robots paid by use at the end of 2025. Medtronic sold $36.4bn in fiscal 2026; GE "
              "HealthCare $7.0bn of its $20.6bn was service; Dexcom grew from $100m to $4.7bn; Quest earned about $44 on each "
              "of 244 million requisitions. The FDA cleared about 3,140 devices a year by comparison (510(k)) against 29 new "
              "premarket approvals and 35 De Novo grants. Insurers pay 39% of Quest's revenue and patients 12%; benign "
              "operations rise when deductibles are met. 84% of Intuitive's revenue recurs; GE HealthCare keeps 51 cents of a "
              "service dollar and 35 of a product dollar; a hospital's five years with one robot cost about $5.3m, half of it "
              "instruments; hospitals' antitrust case over instrument repair cost Intuitive a $450m settlement charge. "
              "Quest's price per requisition barely moved while its volume grew 12%; Abbott's COVID-19 tests fell from $8.4bn "
              "to $0.3bn. Instrument producer prices halved against consumer prices since 1986. Pulsed field ablation took "
              "Boston Scientific's electrophysiology sales from $0.8bn to $3.3bn in two years. Thermo Fisher, Danaher, IQVIA, "
              "Agilent and Illumina sell to the laboratories and drug makers; China buys devices in volume and rations "
              "surgical robots. A device dollar goes 39 cents to making, 8 to research, 40 to everything else and 12 to "
              "profit. Intuitive beat its 2025 procedure guidance; the series gives 2026 growth of 15% or more 45%.",
        handoff="Part 22, consumer goods, turns to brands, where the customer is one person and the rival is the shop.",
        outside="Percentages and present value; Part 5's moats; Part 19's installed base; Part 20's medicines; Economics, "
                "Built's two-part tariffs and the agent who is not the payer.",
        objectives={
            "U": ["Explain who chooses, buys, pays for and uses a medical device, and what each wants.",
                  "Explain why most devices reach the market by comparison and what that does to competition.",
                  "Explain why an installed base earns more than the sale of the machine."],
            "M": ["Solve the sell-or-place decision and find the buying threshold and the break-even volume.",
                  "Compute recurring revenue, gross margins by products and services, and a hospital's cost per operation.",
                  "Separate a laboratory's revenue growth into price, volume and acquisitions."],
            "D": ["Score a device maker's procedure guidance against outcomes.",
                  "Make and state a dated, scorable forecast against a company's narrowed guidance."],
            "I": ["Read a device maker's revenue by kind, installed base and leases.",
                  "Read openFDA's clearances, approvals and recalls."],
        },
        results=[
            ("A hospital buys a robot if", r"A\,\big(N (v - c) - s\big) \ge P"),
            ("A placed robot breaks even at", r"N^* = \frac{M / A + s_c}{c + f - k}"),
            ("Annuity factor", r"A = \frac{1 - (1+r)^{-T}}{r}"),
            ("Recurring share", r"\frac{\text{instruments} + \text{service} + \text{leases}}{\text{revenue}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8, 9), I=(10,), D=(11,),
        also=(("The Register's rows for Part 21", "explainer/industry/data/rows_p21.py"),
              ("Selling or placing a robot; a hospital's five years", "explainer/industry/works/medtech.py"),
              ("The SEC, FRED and openFDA extracts", "explainer/industry/data/SOURCES.md")),
    ),
]
