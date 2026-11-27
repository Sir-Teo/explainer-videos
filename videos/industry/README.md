# Industry, Built (产业，从零搭建)

**Status (2026-11-27): Parts 1-24, [*Where the Money Goes*](industry1/README.md), [*The Economy on One
Page*](industry2/README.md), [*The Accounts*](industry3/README.md), [*The Cost Curve*](industry4/README.md), [*The
Moat*](industry5/README.md), [*The Cycle*](industry6/README.md), [*Sizing a Market*](industry7/README.md), [*Oil and
Gas*](industry8/README.md), [*Mining and Metals*](industry9/README.md), [*Farming and Food*](industry10/README.md),
[*Heavy Materials*](industry11/README.md), [*Chemicals*](industry12/README.md), [*Electricity*](industry13/README.md), [*Water and
Waste*](industry14/README.md), [*Semiconductors*](industry15/README.md), [*Electronics*](industry16/README.md),
[*Automobiles*](industry17/README.md), [*Aerospace and Defence*](industry18/README.md),
[*Machinery*](industry19/README.md), [*Pharmaceuticals*](industry20/README.md), [*Medical
Technology*](industry21/README.md), [*Consumer Goods*](industry22/README.md), [*Fashion and
Luxury*](industry23/README.md) and [*Construction*](industry24/README.md), are built, in English, with their labs and
interactives: Acts I to III are complete and Act IV has begun. Parts 25-64 are planned.** This file is the plan. The standard every part meets, the
devices, the data plan and all sixty-four parts chapter by chapter are in [`SYLLABUS.md`](SYLLABUS.md), with
progress in its §9. The decisions the plan rests on, and the ones still open, are at the end of this file.

This is a sixty-four-part course on video about **how each industry works**: what it sells, how the thing is
made or done, what one more unit costs, where the customer's money goes along the chain, why the profit stays
where it does, what makes the industry cycle or break, who is in it today and what is changing. It covers oil,
mines, farms, steel, chemicals and power; chips, electronics, cars, aircraft, machines, drugs, devices, packaged
goods and fashion; construction, homes and property; ships, airlines, railways and telecoms; grocers, online
shops, wholesalers, restaurants and hotels; software, the cloud, advertising, media, games, music and AI; banks,
investment banks, insurers, fund managers, private equity, payments and the toll collectors of finance;
hospitals, health insurers, universities, professional firms, outsourcers and sports. Then it covers what cuts
across them (the energy transition, chokepoints, the giants, how industries are born and how they die, and the
same industry in five countries) and the job of analysing an industry for a living. The videos will be
`industry1` … `industry64`, in `videos/industry/industryN/`.

Each part is a **30–60 minute lecture** (most will land at 45–55) in the manner of 3Blue1Brown. Industry is
usually filmed as a company's story with stock footage, or sold as an analyst's report behind a paywall. Here
every industry is a **machine that is built on screen**: a model company in running code (an airline with a
fleet and a fare ladder, a fab with a yield curve, a bank with a loan book) whose accounts are computed from its
physical operations and then laid beside the filings of real companies. Where the model and the filings
disagree, the film says so and finds out why.

*Economics, Built* is the theory this series applies; it stops at the door of real industries
(*The Expert Witness*, *The Price*, *Economics at the Platforms*, *Inside the Firm*, *The Economy as a Network*).
This series walks through the door.

## The story: where does the money go?

In 2007 three researchers in California took apart a music player that sold for $299 and asked who got the
money. The label on the back said it was assembled in China, and the trade statistics booked the whole factory
price as a Chinese export. The money told a different story: the largest single slice stayed with the company in
California that designed it, the next with the Japanese firm that made the disk drive, and the assembly that the
label named kept a few dollars (Linden, Kraemer and Dedrick; verify the figures at Part 1's sweep). The label,
the statistics and the money gave three different answers to the question of who makes the thing.

Around 1980 a telephone company asked a consulting firm how many mobile phones there would be in America by the
year 2000. The answer, as the story is told, was 900,000. The outcome was over a hundred million (verify; the
story is told by *The Economist*, 1999). The firm was not stupid. It sized the market for the product in front
of it, at the price in front of it, and the product and the price both changed.

The series lives between those two stories: every price a customer pays is a chain of other people's revenues
that can be traced link by link, and every number about a market is a measurement with a definition, a source
and a date. It puts five questions to every industry:

1. **What is sold?** The unit: a seat-mile, a wafer, a barrel, a premium, a click, a bed-day. What the customer
   is buying and how it is priced.
2. **How is it made, and what does one more cost?** The process, physical and operational, and the cost
   structure that follows from it: what is fixed, what is marginal, where scale and learning come from.
3. **Where does the dollar go?** The chain from the customer's payment down to every supplier's margin, and who
   keeps what.
4. **Why does it stay there?** The structure: concentration, entry, switching costs, regulation, and what the
   returns on capital have been.
5. **What moves it?** The cycle, the shocks and the technology; then the landscape as of a stated date, by
   region, and what is changing.

Underneath all five is the question the second story asks: **how do we know, and as of when?**

## The devices that hold it together

- **The Works** (`explainer/industry/works/`, numpy and scipy only): the model companies, one or more per part,
  built from physical primitives (a fleet, a network, a reactor, a store, a loan book) through an operating
  model to three financial statements. A part's lab runs its model company; its interactive lets the viewer run
  it. By the end the model companies buy from each other: the airline of Part 28 flies the aircraft of Part 18
  on the fuel of Part 8, financed by the bank of Part 43.
- **The Unit:** one card per industry: the thing sold, its price, its cost, its margin, as a strip that is
  drawn the same way in every part.
- **The Dollar:** the customer's payment as a waterfall down the chain, each link's revenue split into its
  suppliers, its labour, its capital and its profit. The series' signature picture.
- **The Stack:** the industry's supply curve built from its producers' unit costs, with demand drawn through
  it; who is making money at this price, and who closes first.
- **The Map:** the landscape as of a stated date: segments across, regions down, companies sized by revenue and
  shaded by margin. Every number on it comes from the Register.
- **The Board:** the same ten numbers for every industry (revenue pool, value added, employment, gross margin,
  capital intensity, return on invested capital, concentration, cyclicality, growth, research intensity). It
  fills in over the series, and by Part 56 it is the picture of the whole economy that Part 2 promised.
- **The Register** (`explainer/industry/register.py`, gated by `tools/check_register.py industryN`): every
  market figure a part shows is a row with its definition, its primary source, the date of the fact, the date it
  was checked, and the range across sources where they disagree. A figure with no row does not reach the screen.
- **The Filing Room** (`explainer/industry/data/`): frozen, cited extracts of company filings and of the public
  data regulators and statistical offices collect, each registered in `data/SOURCES.md` with its licence and
  retrieval date.
- **Run it:** in the first third of every part the viewer runs the business for a few turns (sets the fare,
  orders the fab, writes the policy) before the model that explains what happened.
- **Called it?:** one dated forecast about the industry per part, with who made it, on what reasoning, and what
  happened. The series logs its own, to be scored later.

## How the market research is done

The usual sources for industry numbers (syndicated reports, broker research, paid terminals) are paywalled,
unlicensed for reuse and often unverifiable. The series does not use them. It works from primary sources:
company filings (annual reports, 10-Ks and 20-Fs, prospectuses, investor-day material), the data regulators
collect (transport, energy, banking, insurance, telecoms, health), national accounts and input-output tables,
censuses of business, trade data, and the statistics of international bodies and trade associations. A market's
size is built bottom-up (units times prices, or the summed revenues of named companies plus a stated remainder)
and shown as a range. SYLLABUS §3 lists the sources sector by sector.

Three rules follow. Every figure carries an as-of date on screen. A part's landscape chapter draws its numbers
from the Register at render time, so a yearly refresh re-renders that chapter and not the film. And nothing in
the syllabus that was written from memory reaches a film until its part's sweep has checked it against a
primary source.

## The acts

| Act | Parts | Question |
|---|---|---|
| **I. Reading an Industry** | 1–7 | How do you take an industry apart: its dollar, its accounts, its costs, its moat, its cycle, and the size of its market? |
| **II. Out of the Ground** | 8–14 | What does it take to pull energy, metal, food and materials out of the earth and sell a commodity? |
| **III. Making** | 15–23 | How are chips, phones, cars, aircraft, machines, drugs and brands made, and who keeps the margin? |
| **IV. Building** | 24–26 | Why is building so hard to make cheaper, and how is land turned into an asset? |
| **V. Moving** | 27–30 | What does a network cost to build and to run, and who pays for it? (ships, aircraft, rails, signals) |
| **VI. Selling and Serving** | 31–35 | How does a penny of margin on a basket become a fortune, and who owns the customer? |
| **VII. Information** | 36–42 | What happens to an industry when one more copy costs nothing? |
| **VIII. Money** | 43–49 | How do firms that make nothing physical earn so much, and what do they do for it? |
| **IX. People** | 50–55 | What happens when the product is an hour of a skilled person's time? |
| **X. Systems** | 56–61 | What do you see only when the industries are put side by side? |
| **XI. The Job** | 62–64 | How is an industry analysed for a living, and can you do it from a blank page? |

## The parts

| # | Part | Hook | The machine: what is explained | The Works gains | Run it |
|---|---|---|---|---|---|
| **I** | **Reading an Industry** | | | | |
| 1 | Where the Money Goes | a $299 music player taken apart, 2007 | value added, the chain, who captures what and why the label and the trade data mislead; the five questions; the series map | a product with a bill of materials and a chain | split the price of a phone among the firms that made it |
| 2 | The Economy on One Page | Leontief's table of 1936 | classifications (SIC, NAICS, ISIC, GICS), input-output tables, three maps of the economy (value added, jobs, profits), upstream and downstream, the Board | an input-output economy of model sectors | rank ten industries by size, three ways |
| 3 | The Accounts | Pacioli's ledger, 1494; Du Pont's chart, 1919 | the three statements built from operations, accruals against cash, margins, turns, leverage, return on invested capital, unit economics, reading a filing | the generic firm: operations to statements | which company is which, from the ratios alone |
| 4 | The Cost Curve | Wright's aircraft, 1936; Bain's plants, 1956 | fixed and marginal cost, scale, scope, learning, capacity and utilization, operating leverage, the industry supply stack | cost functions; the Stack | price a product with a big plant and an empty order book |
| 5 | The Moat | Bain's barriers, 1956; Porter's five forces, 1979 | concentration, entry and exit, switching costs, networks, brands, regulation; which returns persist; structure tested on data | a market with entry and five kinds of barrier | spend a budget defending a market against an entrant |
| 6 | The Cycle | Ezekiel's cobweb, 1938; the tanker market, 1973 | lead times and overbuilding, the capital cycle, inventories and the bullwhip, operating and financial leverage through a downturn | a capacity-cycle economy with lead times | order ships at the top, or do not |
| 7 | Sizing a Market | 900,000 mobile phones by 2000 | definitions, top-down and bottom-up, triangulation, diffusion and S-curves, surveys and panels, forecast records; the Register and the sweep | a market sizer with ranges; a diffusion model | size a market before the answer is shown |
| **II** | **Out of the Ground** | | | | |
| 8 | Oil and Gas | Spindletop, 1901; negative oil, 2020 | reserves and decline curves, the cost of a barrel, OPEC and swing supply, shale, pipelines, refining margins, LNG, national against listed companies | an oil field, a refinery, a price deck | drill or wait at $60 |
| 9 | Mining and Metals | Escondida found, 1981 | exploration odds, grade, the mine plan, the cost curve by mine, iron ore and copper, royalties and resource nationalism, critical minerals | a mine with a grade and a life | develop a deposit across a price cycle |
| 10 | Farming and Food | Borlaug's wheat, 1960s | yields and land, inputs (seed, fertilizer, machinery), the grain traders, futures and hedging, meat packing, subsidy and trade policy | a farm, an elevator, a packer | plant, hedge and sell a crop |
| 11 | Heavy Materials | the Bessemer converter, 1856 | steel by blast furnace and by arc, cement and the reach of a kiln, aluminium and power, glass and paper; freight, local markets, overcapacity | a mill and a kiln with a delivery radius | run a steel mill through a glut |
| 12 | Chemicals | Haber and Bosch, 1909–13 | the cracker and its feedstock, the chain from gas to plastics, fertilizer, industrial gases and on-site contracts, commodity against specialty | a cracker with a feedstock choice | choose a feedstock and a site |
| 13 | Electricity | Insull's Chicago, 1890s; California, 2000–01 | load and the merit order, the grid, the regulated utility and its rate base, wholesale markets, renewables, storage, who pays for reliability | a power system with dispatch; a utility | bid a plant into tomorrow's market |
| 14 | Water and Waste | London's sewers, 1858 | the regulated water company, route density in collection, the landfill as a moat, recycling's economics, privatization's record | a water utility; a collection route | price a landfill's airspace |
| **III** | **Making** | | | | |
| 15 | Semiconductors | Moore's paper, 1965; Morris Chang's foundry, 1987 | how a chip is made, the node and its cost, yield, design against fabrication, equipment and design software, memory's cycle, the chain's chokepoints | a fab with yield learning; a fabless designer | build a fab or book a foundry |
| 16 | Electronics | the smiling curve, 1992 | contract manufacturing, the bill of materials, components and modules, the cluster, brands against assemblers, the phone and the PC | an assembler and a brand on one device | take an order at a 3% margin |
| 17 | Automobiles | Highland Park, 1913; Toyota's Ohno | platforms and scale, the assembly plant, tiered suppliers, dealers and franchise law, captive finance, electric vehicles and batteries, China | a car maker with platforms and a finance arm | price a launch and fill a plant |
| 18 | Aerospace and Defence | the 747 bet, 1966 | the learning curve and launch aid, programme accounting, the duopoly, engines sold at a loss, the single buyer, cost-plus contracts | an aircraft programme; an engine with service | launch an aircraft programme |
| 19 | Machinery | McCormick's reaper on credit, 1850s | capital goods and the installed base, service and parts, dealers, order books and the cycle, automation, the conglomerate and its breakup | a machine maker with an installed base | sell the machine cheap or the service dear |
| 20 | Pharmaceuticals | Lipitor's patent ends, 2011 | discovery to approval, the cost and odds of a trial, patents and exclusivity, the cliff, generics and biosimilars, list and net prices, biotech's funding | a drug pipeline as a set of options | fund a pipeline with a fixed budget |
| 21 | Medical Technology | the first pacemakers, 1958–60 | devices and their approval route, the surgeon as customer, hospital purchasing, consumables on an installed base, diagnostics, tools and contract research | a device with a consumable | place the capital or sell the consumable |
| 22 | Consumer Goods | Procter & Gamble's brand men, 1931 | brands and their advertising, shelf space, the retailer's own label, bottlers and distributors, pricing power, tobacco and drink | a brand against a store label | set a price and a promotion calendar |
| 23 | Fashion and Luxury | Zara's fifteen days; the Birkin wait | the apparel chain, lead times and markdowns, fast fashion, luxury's pricing and scarcity, the groups, resale | a fashion buyer with markdowns; a luxury house | buy a season's stock before the weather is known |
| **IV** | **Building** | | | | |
| 24 | Construction | the Empire State Building in 410 days, 1931 | bidding and thin margins, subcontracting, why productivity has not risen, megaprojects and overruns, concessions, engineering firms | a contractor bidding with risk | bid for a job you can lose money on |
| 25 | Homes | Levittown, 1947 | the house builder and its land, the mortgage and who funds it, brokers and commissions, zoning and supply, rents against prices | a builder with a land bank; a mortgage | buy land a cycle ahead |
| 26 | Property | the cap rate; Zeckendorf's deals, 1950s | commercial property as a bond with a building attached, leases, capitalization rates, development, REITs, warehouses and data halls, offices after 2020 | a building with leases and debt | refinance a tower when rates double |
| **V** | **Moving** | | | | |
| 27 | Shipping and Ports | McLean's *Ideal-X*, 1956 | the container, liners and tramps, freight rates, alliances, the shipbuilding cycle, ports and terminals, canals | a fleet on a rate cycle; a terminal | charter long or ride the spot rate |
| 28 | Airlines | deregulation, 1978; Crandall's fares | the seat-mile, hubs and point-to-point, yield management, fuel and labour, aircraft and lessors, airports, loyalty schemes, alliances | an airline with a network and fare classes | set fares on a route as the seats sell |
| 29 | Rail, Trucks and Parcels | the Staggers Act, 1980; Memphis at midnight, 1973 | density on a network, railways' operating ratio, trucking's entry and exit, the integrators' hubs, the last mile, warehouses | a railway, a carrier, a parcel hub | price a lane with an empty backhaul |
| 30 | Telecoms | the breakup of Bell, 1984; the 3G auctions, 2000 | spectrum and its auctions, towers and fibre, revenue per user and churn, cable and broadband, satellites, the pipe against what runs over it | a mobile network with spectrum and churn | bid for spectrum |
| **VI** | **Selling and Serving** | | | | |
| 31 | Grocery and Mass Retail | Walton's Bentonville; Aldi's 1,400 items | turns and the penny margin, negative working capital, private label, the warehouse club's fee, distribution centres, suppliers' terms, discounters | a store, a distribution centre, a club | run a store on a 2% margin |
| 32 | E-commerce | Amazon's 1997 letter; Singles' Day | the take rate, fulfilment's cost, the marketplace and its advertising, China's models, direct brands and the cost of a customer | a marketplace with fulfilment and ads | set the take rate and the delivery promise |
| 33 | The Middlemen | the trading houses of Japan | why wholesalers exist, turns against margin, drug and food distributors, electronics distribution, commodity trading houses, group purchasing | a distributor with credit and stock | carry stock or drop-ship |
| 34 | Restaurants and Franchising | Kroc and the land under the store, 1950s | the economics of one store, the franchise contract and its royalty, the property play, labour, delivery platforms, cafes and chains | a franchisor and its franchisees | open a store, then sell the model |
| 35 | Travel and Hotels | Hilton, Marriott and the sale of the hotels | the owner, the brand and the operator, revenue per room, online agents, cruises, casinos and parks | a hotel with a brand contract | fill the rooms: rate, channel or loyalty |
| **VII** | **Information** | | | | |
| 36 | Software | Gates's letter to hobbyists, 1976; Salesforce, 1999 | zero marginal cost, licences to subscriptions, retention and expansion, the cost of a sale, switching costs, open source, the stack from chip to application | a subscription company with cohorts | spend on sales or on product |
| 37 | Cloud and Data Centres | S3 goes live, 2006 | the data hall, power and cooling, utilization, the hyperscalers' capital spending, pricing and commitments, colocation, the network edge | a data centre and a cloud region | build ahead of demand, and how far |
| 38 | Advertising | GoTo's bids, 1998; the Mad Men's 15% | attention as inventory, the auction, targeting and measurement, the ad stack and its take, agencies, privacy rules, retail media | an ad auction with a publisher | set reserve prices and ad load |
| 39 | Media and Streaming | *House of Cards*, 2013; the bundle | windows, the cable bundle, the cost of content and its amortization, churn, sports rights, cinema, news and its funding | a streamer and a studio slate | green-light a slate |
| 40 | Video Games | Nintendo's seal, 1985 | the console sold at cost, the platform fee, hits and budgets, live services, free-to-play, engines, stores | a console platform; a studio | price the console and the fee |
| 41 | Music, Books and Creators | Napster, 1999; Spotify's pool | copyrights as assets, labels and publishers, the streaming pool, catalogues, live music and ticketing, books, the creator economy | a catalogue; a streaming pool | split a streaming payout |
| 42 | Artificial Intelligence | AlexNet's two GPUs, 2012 | the stack from chips to applications, training against inference cost, the price of a token, capital spending, open weights, who captures the margin | a model lab: compute, training, serving | price a model against its compute |
| **VIII** | **Money** | | | | |
| 43 | Banks | Bagehot's Lombard Street, 1873; March 2023 | deposits and loans, the interest margin, credit losses through a cycle, capital and leverage, the return on equity taken apart, regulation | a bank with a loan book and deposits | grow the loan book into a boom |
| 44 | Investment Banks and Markets | May Day, 1975; Salomon's desk | underwriting and its fee, advice on mergers, market making and its balance sheet, prime broking, the league table, pay | a dealer with inventory and capital | quote a block trade |
| 45 | Insurance | Lloyd's coffee house; Buffett's float | pooling and pricing risk, the combined ratio, float, the underwriting cycle, reinsurance and catastrophe bonds, life insurance and annuities | an insurer with a book and reserves | write business in a soft market |
| 46 | Asset Management | Bogle's fund, 1976 | fees on assets, active against index, scale, distribution, exchange-traded funds, hedge funds, pensions, wealth managers | a fund family with flows | cut the fee or keep it |
| 47 | Private Equity and Venture Capital | RJR Nabisco, 1988; ARD and Digital, 1957 | the buyout's arithmetic, the fund and its fees, the J-curve, venture's power law, private credit, the measurement of returns | a buyout and a venture fund | structure a buyout |
| 48 | Payments | BankAmericard's drop in Fresno, 1958 | the four parties, interchange, networks, acquirers and processors, instant payment systems, wallets, cross-border, buy now pay later | a card network with two sides | set interchange |
| 49 | The Toll Collectors | Moody's manual, 1909 | exchanges and clearing, index providers, rating agencies and who pays them, credit bureaus, market data, benchmarks as standards | a benchmark with licensees | price a data feed |
| **IX** | **People** | | | | |
| 50 | Hospitals and Doctors | Baylor's plan for teachers, 1929 | who pays the hospital and how, the price list nobody pays, payment by diagnosis, physician practices, staffing, long-term care; systems compared | a hospital with a payer mix | set a budget with a fixed payer mix |
| 51 | Health Insurance and the Drug Channel | where a prescription's dollar goes | the insurer's loss ratio, managed care, pharmacy benefit managers and rebates, distributors and pharmacies, single payers | a health plan; a drug channel | design a plan's network and premium |
| 52 | Education | Bologna, 1088; Bowen's rule | the university's budget, list and net tuition, endowments, research funding, why costs rise, for-profit colleges, testing and publishing | a university with aid and an endowment | set tuition and aid |
| 53 | Professional Services | Cravath's system, 1900s | leverage, utilization and rate, the partnership, the audit firms, consulting, law, why these firms stay private | a partnership with a pyramid | staff a pyramid |
| 54 | Outsourcing and Staffing | Bangalore, 1990s | labour arbitrage, the delivery pyramid, body shops and platforms, staffing agencies, facilities services, gig work | an offshore services firm; a staffing agency | bid a fixed-price contract |
| 55 | Sports and Live Entertainment | Rozelle's television deal, 1961 | the league as a cartel, media rights, salary caps and drafts, promotion and relegation, club values, venues and tickets | a league with shared revenue | split the television money |
| **X** | **Systems** | | | | |
| 56 | The Energy Transition | Swanson's law; a solar auction's record low | learning curves for solar, wind and batteries, the cost of capital, grids and intermittency, the electric car's chain, hydrogen and nuclear, subsidy races | a transition path with learning | allocate a subsidy budget |
| 57 | Chokepoints | one fire at one resin plant | chains by stage and by country, concentration at each stage, single sources, inventories against resilience, export controls | the Works joined into one web | find the weakest link |
| 58 | The Giants | Sloan's General Motors; Berkshire | conglomerates and their discount, capital allocation, the technology giants as conglomerates, business groups in Asia, the holding company | a group allocating capital | allocate a group's capital |
| 59 | Birth | 274 car makers, then three | how an industry starts: the S-curve, the dominant design, the shakeout; space, autonomy and others in their early years | an industry life cycle with entry and shakeout | pick the survivors |
| 60 | Decline | Kodak's digital camera, 1975 | what decline looks like in the accounts: newspapers, film, department stores, coal; harvesting, consolidation, exit | a firm in a shrinking market | harvest or reinvest |
| 61 | One Industry, Five Countries | steel in five countries | the same industry under different owners, banks, states and labour markets: America, China, Europe, Japan and Korea, India | one sector under five national regimes | run the same firm under five rules |
| **XI** | **The Job** | | | | |
| 62 | The Analyst | the first industry report | who analyses industries for money and how: brokers, investors, consultants, strategists; channel checks, expert calls, alternative data, the law | an analyst's model of one company | forecast a quarter |
| 63 | Due Diligence | a buyer's six weeks | commercial diligence end to end on one target: market, customers, competitors, the model, the risks | a diligence pack as code | find what the seller left out |
| 64 | The Report | a blank page | an industry the series has not covered, analysed from nothing with registered sources, and a dated forecast logged for scoring | the report pipeline | (the viewer's own industry) |

## Four ways through it

- **The whole thing:** Parts 1–64 in order. About 55 hours.
- **The method only:** Act I, then Parts 57–64. How to take any industry apart.
- **One sector:** Act I's Parts 1, 3 and 4, then any act. Each act after the first stands on Act I alone.
- **By mechanism:** SYLLABUS §5 lists the mechanisms that recur (the razor and the blade, the regulated return,
  the capacity cycle, the split of owner and operator, the toll booth, float, the hit) and the parts that show
  each.

## What it follows

No single textbook covers this. The method follows Porter (*Competitive Strategy*), Tirole and the industrial
organization of *Economics, Built* Parts 10–12, 43–44 and 59–63; Koller, Goedhart and Wessels (*Valuation*) for
the accounts; Greenwald and Kahn (*Competition Demystified*); Chancellor (*Capital Returns*) for the cycle;
Scherer and Ross for structure and performance. Each industry follows its own standard works (Yergin on oil,
Levinson on the container, Miller on chips, Womack, Jones and Roos on cars, Stopford on shipping, Belobaba on
airlines, and so on); SYLLABUS gives a *Reading* line for every part.

## Standards (as *Economics, Built*, plus this series' own)

- The watching standard of *Economics, Built* (SYLLABUS §1.3 there): a cold open, the question card, Run it in
  the first third, the four-minute rule, an intermission with a data film, the computed score.
- Every figure on screen has a Register row and an as-of date. Market sizes are ranges.
- Primary sources only. No syndicated reports, no broker research, no figures taken from news articles when
  the filing they quote can be read.
- Real companies are named and described from their own filings. No logos. No investment advice, no price
  targets, no judgement on whether a share is cheap.
- Each part meets the coverage checklist of SYLLABUS §1.1, so that "deep dive" means the same thing in every
  part.
- Each part's landscape covers America, China, Europe, Japan and Korea, and India, or says why a region does
  not matter to it.

## Shared code (planned)

`explainer/industry/`: the Works (`works/`, one module per industry over a generic firm), the Register
(`register.py`), the Filing Room (`data/`, with readers for company facts and for each regulator's files), the
Board (`board.py`), Called it? (`calls.py`), the instruments (`viz.py`: the Unit strip, the Dollar waterfall,
the Stack, the Map, the Board, the statement view) and the score. Tests in `tests/industry/`. It borrows
Agora's `io`, `pricing`, `revenue`, `merger`, `platform`, `network`, `bank`, `auctions` and `contracts` from
`explainer/economics/` and the House from `explainer/quant/` where a part needs them, and does not copy them.

## Decisions taken

1. **Sixty-four parts in eleven acts,** the full series (the user's choice, 2026-11-23), built act by act.
2. **Audience:** the general public (the user's choice, 2026-11-23), with a deep dive into each industry and a heavy
   use of visuals: every chapter is drawn, not read. The arithmetic and the sources stay in, for viewers who want
   them, in the labs and the Register.
3. **Primary sources only,** with a Register row and an as-of date behind every figure.
4. **A global landscape,** anchored on American data where regulators publish the most, with China, Europe,
   Japan and Korea, and India in every part's map.
5. **Three pilots before the rest:** Part 1, then Parts 28 (Airlines) and 15 (Semiconductors) built out of
   order (SYLLABUS §7).

## Decisions still open

1. **Chinese narration from the first part, or after the English series?** The plan assumes from the first part
   (`narration_zh.json`, `industry_text_zh.json`, a term guide), as *AI, Built* does.
2. **The refresh cadence** for landscape chapters: yearly is assumed.
3. **Whether the model companies get names and a shared world** (as the Island does in *Economics, Built*), or
   stay anonymous. The plan assumes named model companies in one web.
