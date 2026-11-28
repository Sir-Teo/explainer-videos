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
    Part(
        n=31, level="U", widget="storeyear", prereq=(3, 4, 22),
        question="How does a business that keeps two or three cents of every dollar become one of the largest on earth?",
        story="The part opens on Walmart: $713bn of revenue in the year to January 2026, 2.1 million people and $21.9bn of "
              "profit, about three cents a dollar; and on Costco, whose $5.9bn of membership fees came to almost two-thirds of "
              "its $9.2bn of profit. The viewer runs a supermarket on $50m of sales at Kroger's 23.3% gross margin and keeps "
              "$1.15m; prices set by rivals nearby leave little room either way; a 1% price cut needs 6.1% more sales; staffing "
              "too thin or too thick costs profit; a 10% fall in sales cuts profit by seven-tenths. Walmart's dollar is 75.8 "
              "cents of goods, 20.9 of running costs and 4.2 of operating profit; clubs keep 13-19 cents after the goods and "
              "dollar stores over 30, but almost all end with one to seven cents. Goods sit 40 days at Walmart and are paid for "
              "after 43; suppliers fund $4bn of Walmart's stock and $84bn of Amazon's. Costco sells about three times as much "
              "per square foot as Walmart's American stores; its fees are half its operating income; 92.3% of members renew. "
              "Clorox sells 26% of its goods to Walmart. A court blocked Kroger and Albertsons in December 2024; Kroger "
              "closed its Ocado warehouses and took $2.5bn of charges. The series gives 55% that Costco reports more than "
              "87 million paid members at the end of fiscal 2027.",
        handoff="Part 32, e-commerce, asks whether selling online is a shop, a toll road or an advertising business.",
        outside="Percentages and fixed costs; Part 3's accounts; Part 4's fixed costs; Part 22's brands and buyers; Economics, "
                "Built's pricing (uniform chain prices, high-low against everyday low prices) and mergers.",
        objectives={
            "U": ["Explain why a grocer's margin is set by the rivals nearby, and why price wars are so costly.",
                  "Explain how fast-turning stock and slow payment let suppliers fund a retailer.",
                  "Explain the warehouse club's model: goods near cost, profit from the fee."],
            "M": ["Compute the extra sales a price cut needs to break even, and a store's operating leverage.",
                  "Compute inventory and payables days and the cash suppliers fund.",
                  "Compute a return on assets as margin times turns."],
            "D": ["Read a company's plan against its later write-down, and make and state a dated, scorable forecast."],
            "I": ["Read a retailer's segment sales, store counts, square feet and margins in its filings.",
                  "Read a supplier's largest-customer disclosure and a club's membership statistics."],
        },
        results=[
            ("Break-even volume for a price cut", r"\Delta V = \frac{\pi + F}{S\,[(1 - c)(1 - o) - (1 - g)]} - 1"),
            ("Days of stock and of payables", r"d_{\text{inv}} = \frac{I}{\text{COGS}/365}, \quad d_{\text{pay}} = \frac{AP}{\text{COGS}/365}"),
            ("Return on assets", r"\text{ROA} = \frac{\text{profit}}{\text{sales}} \times \frac{\text{sales}}{\text{assets}}"),
            ("Sales density", r"\frac{\text{sales}}{\text{square feet}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s07_intermission", 6, 7, 8), I=(9,), D=(10,),
        also=(("The Register's rows for Part 31", "explainer/industry/data/rows_p31.py"),
              ("The store and the float", "explainer/industry/works/store.py"),
              ("The SEC and FRED extracts", "explainer/industry/data/SOURCES.md")),
    ),
    Part(
        n=32, level="U", widget="marketrun", prereq=(3, 5, 31),
        question="Is selling online a shop, a toll road or an advertising business?",
        story="The part opens on Amazon's letter of 1997 (1.5 million customers, $147.8m of revenue, 'Day 1') and of 2000 "
              "(shares down more than 80%), and on its $717bn of revenue in 2025, of which AWS was 18% but made 57% of the "
              "operating income. The viewer runs a marketplace: buyers and sellers each come for the other; revenue peaks at a "
              "take rate near 25% and profit near 30%; ads are nearly pure profit until about 4% of sales; one-day delivery "
              "pays only at scale. A $40 order on a marketplace leaves the seller about $7.60 after a 15% referral fee, delivery "
              "fees and ads; the FTC alleged in 2023 that many Amazon sellers pay close to 50%. Take rates run from Shopify's 3% "
              "to Etsy's 24%. Amazon's shipping costs rose from $11.5bn (2015) to $102.7bn (2025); its advertising, $68.6bn in "
              "2025, exceeded its shops' whole operating income in every year since 2019; the cloud carried the shops through "
              "a $10.6bn loss in 2022. Temu lifted PDD's revenue to $62bn before the de minimis exemption ended in 2025. Direct "
              "brands live or die by the cost of a customer; Wish's users fell 68% when it cut its ads, and it sold its business "
              "for $162m. The series gives 45% that the Census Bureau's first estimate of e-commerce's share for 2027 Q4 is "
              "19.0% or more.",
        handoff="Part 33, the middlemen, asks why wholesalers and distributors are still among the largest companies anywhere.",
        outside="Percentages, logs and fixed costs; Part 3's accounts; Part 5's network effects; Part 31's retail margins; "
                "Economics, Built's two-sided platforms, sponsored slots and the commission.",
        objectives={
            "U": ["Explain the difference between a retailer and a marketplace, and why it changes what counts as revenue.",
                  "Explain why a marketplace's take rate is bounded by what both buyers and sellers can do instead.",
                  "Explain why fast delivery is a fixed-cost game and why on-site advertising is so profitable."],
            "M": ["Compute a take rate and split an order between the goods, the platform's fees, ads and the seller.",
                  "Compute the cost of an order as a fixed network spread over volume.",
                  "Compute a customer's lifetime contribution and payback from the cost of acquiring them."],
            "D": ["Read a company's description of itself against what followed, and make and state a dated, scorable forecast."],
            "I": ["Read a platform's GMV, take rate, revenue by kind and segment profit in its filings.",
                  "Read the Census Bureau's e-commerce series and a fee schedule."],
        },
        results=[
            ("Take rate", r"\tau = \frac{\text{revenue}}{\text{GMV}}"),
            ("Cost of an order", r"c(n, d) = v + \frac{s}{d} + \frac{K}{d\,n}"),
            ("A customer's lifetime contribution", r"L = m\,f + m\,r\,\frac{\rho}{1 - \rho} - \text{CAC}"),
            ("Two-sided participation", r"B = \bar B\,\Lambda(\beta_0 + \beta_s \ln S - \dots), \quad S = \bar S\,\Phi\!\left(\frac{\ln[g(m - \tau - a)] - \mu}{\sigma}\right)"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s07_intermission", 6, 7, 8), I=(9,), D=(10,),
        also=(("The Register's rows for Part 32", "explainer/industry/data/rows_p32.py"),
              ("The marketplace and the direct brand", "explainer/industry/works/marketplace.py"),
              ("Amazon's revenue and segment tables", "explainer/industry/data/tables.py"),
              ("The SEC and FRED extracts", "explainer/industry/data/SOURCES.md")),
    ),
]
