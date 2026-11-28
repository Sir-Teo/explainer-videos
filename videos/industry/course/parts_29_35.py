"""Parts 29-35."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=29, level="U", widget="lanerun", prereq=(4, 5, 28),
        question="Why is one freight industry a set of regional monopolies, and the next a market of half a million firms?",
        story="The part opens on the Staggers Rail Act of 1980, which found railway earnings 'the lowest of any "
              "transportation mode', against Union Pacific's operating ratio of 59.8% in 2025, and on FMCSA's register of "
              "533,278 active for-hire trucking firms, 272,151 of them with one truck. The viewer prices a lane: a truck "
              "costs $2.61 a mile driven, loaded or empty; a load to Atlanta at $2.84 a loaded mile looks like a $166 profit "
              "and becomes a $1,716 loss when the truck drives home empty, needing $5.23 a loaded mile; a load home below "
              "cost still helps, and a network that runs 13.9% of its miles empty, as Knight-Swift did, needs about $3.04. "
              "Rail earns 5.4 cents a ton-mile; intermodal $1.70 a mile against truckload's $2.84; Old Dominion $492 for a "
              "1,477-pound shipment; UPS $13.21 a parcel. A railway's cost per ton-mile falls with traffic on its own track; "
              "rail prices after inflation fell 32% to 2001 and rose after. Truckload margins fell to a few cents in a "
              "prolonged downcycle; the Works' market shows how fast entry makes the rate swing. Old Dominion's 260 "
              "service centers let it raise prices with tons down 9%; Yellow went bankrupt in 2023. UPS cut its Amazon "
              "volume, closed 93 buildings and cut 48,000 positions; FedEx spun off FedEx Freight. A parcel costs $1.28 "
              "to deliver in the city and $5.80 in the countryside in the Works; the Postal Service delivers 2.4 pieces to "
              "each address a day, down from 5.5, and lost $9.0bn. Aurora launched driverless trucks in April 2025 against "
              "a promise of late 2023. The series gives 40% that Union Pacific completes its purchase of Norfolk Southern "
              "by 31 December 2027.",
        handoff="Part 30, telecoms, turns to the companies that carry everything and capture so little of what it is worth.",
        outside="Averages and fixed costs; Part 4's cost curve; Part 5's moats; Part 6's cycle; Part 28's perishable seats; "
                "Economics, Built's pricing (Ramsey prices for captive shippers) and its congestion part.",
        objectives={
            "U": ["Explain why the price of a lane is set by the trip home, and why big networks run fewer empty miles.",
                  "Explain why a railway's ownership of its track gives it margins truckers cannot reach.",
                  "Explain why the last mile is the dearest part of a parcel's journey."],
            "M": ["Compute a truck's cost a mile and the rate a loaded mile needs at a given share of empty miles.",
                  "Compute a railway's average cost per ton-mile from fixed and variable costs and traffic density.",
                  "Compute the cost of delivering a parcel from stop spacing, dwell time and the driver's hourly cost."],
            "D": ["Read a company's forecast of a new technology against what happened, and make and state a dated, "
                  "scorable forecast on a regulatory decision."],
            "I": ["Read operating ratios, revenue per load, per hundredweight and per piece, and empty-mile shares in filings.",
                  "Read FMCSA's carrier census, the BTS's freight series and the PPIs for trucking and rail."],
        },
        results=[
            ("A truck's cost a mile", r"c = c_0 + \frac{p_{\text{diesel}}}{\text{mpg}}"),
            ("The rate a loaded mile needs", r"r^{*} = \frac{c}{1 - e}, \quad e = \text{share of miles empty}"),
            ("A railway's average cost", r"AC(d) = \frac{F}{d} + v, \quad d = \frac{\text{ton-miles}}{\text{route miles}}"),
            ("A parcel at the door", r"\frac{w H}{n\,k}, \quad n = \frac{60 H}{t_{\text{dwell}} + 60\,s / v}"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s07_intermission", 6, 7, 8), I=(9,), D=(10,),
        also=(("The Register's rows for Part 29", "explainer/industry/data/rows_p29.py"),
              ("The lane, the trucking market, the railway and the route", "explainer/industry/works/freight.py"),
              ("The SEC and FRED extracts", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=30, level="U", widget="spectrumclock", prereq=(4, 5, 29),
        question="Why do the companies that carry everything capture so little of what it is worth?",
        story="The part opens on Verizon, AT&T and T-Mobile, whose revenue rose from $311bn in 2015 to $352bn in 2025 while "
              "Alphabet, Meta and Netflix grew from $100bn to $649bn, and on telephone prices 53% lower after inflation than "
              "in 1998. The viewer bids for eight blocks of airwaves in a clock auction against three rivals: asking for "
              "every block worth the price ends the auction at $6.75bn a block and leaves $5.25bn; asking for two ends it at "
              "$4.75bn and leaves $9.00bn, and the auction raises $38bn instead of $54bn. A Verizon account pays $147 a month "
              "for 2.95 lines and leaves at 0.92% a month, nine years on average; Verizon sold $25.5bn of phones that cost "
              "$29.0bn. Of its dollar, 21 cents is operating profit; capital spending runs 11-21% of the carriers' revenue, "
              "and Alphabet's $91bn exceeds the three carriers' $48bn together. Verizon won $45.5bn of C-Band licences; "
              "EchoStar sold spectrum to AT&T for $22.65bn and to SpaceX for about $20bn and took its network apart. American "
              "Tower keeps 80 cents of each dollar of American rent, and each extra tenant is nearly pure profit. T-Mobile's "
              "merger with Sprint left three national networks with near-identical churn. Comcast lost 711,000 broadband "
              "customers in 2025 while fixed wireless and fibre grew. DISH promised a fourth network by 2023 and abandoned it "
              "in 2025; the series gives 80% that Comcast ends 2027 with fewer broadband customers than 2026.",
        handoff="Part 31, grocery and mass retail, turns to the business of selling everything else, a few cents at a time.",
        outside="Expected value and auctions; Part 4's fixed costs; Part 5's moats; Part 26's landlords; Part 29's networks; "
                "Economics, Built's auctions (uniform-price clocks and demand reduction), platforms and mergers.",
        objectives={
            "U": ["Explain why spectrum is sold like land and paid for before it earns anything.",
                  "Explain why three look-alike networks compete away their margins while tower owners keep theirs.",
                  "Explain why the services that run over the networks earn more than the networks."],
            "M": ["Run a uniform-price clock auction and show why demand reduction can pay.",
                  "Compute a subscriber's lifetime value from monthly revenue, margin, churn and acquisition cost.",
                  "Compute a tower's return as tenants are added."],
            "D": ["Read a company's commitment to regulators against what it did, and make and state a dated, scorable forecast."],
            "I": ["Read carriers' ARPA, churn, connections per account and capital spending in their filings.",
                  "Read a tower company's segment revenue, costs, customer concentration and churn."],
        },
        results=[
            ("Uniform-price clock", r"p^{*} = \min\{p : \textstyle\sum_i d_i(p) \le S\}, \quad \text{surplus}_i = \sum_{k \le d_i} v_{ik} - d_i p^{*}"),
            ("A subscriber's worth", r"\text{LTV} = \frac{\text{ARPA} \cdot m}{c} - \text{CAC}"),
            ("A tower's yield", r"y(n) = \frac{n R - O}{K}"),
            ("Capital intensity", r"\frac{\text{capital spending}}{\text{revenue}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s07_intermission", 6, 7, 8), I=(9,), D=(10,),
        also=(("The Register's rows for Part 30", "explainer/industry/data/rows_p30.py"),
              ("The auction, the subscriber and the tower", "explainer/industry/works/telco.py"),
              ("The SEC and FRED extracts", "explainer/industry/data/SOURCES.md")),
    ),
]
