# Industry, Built: the syllabus (plan of record, draft 1)

Goal: a deep dive into every major industry, on video, to the level of the primer an analyst is handed in the
first week of covering it, and built so that the viewer can run the business and not only hear about it. It
aims to be **as broad as the economy's own accounts, as concrete as a plant tour, as numerate as a company's
filings, and as careful about its figures as a statistical office**. It is told as one question, *where does the
money go?* ([README](README.md)). Each part runs **30–60 minutes**, most at 45–55. Sixty-four parts come to
about **55 hours**.

The plan has the shape of the economy, from the ground up:

- **Act I** is the method: the chain, the map of the economy, the accounts, costs, structure, the cycle and the
  measurement of a market.
- **Acts II–IV** are the physical economy: extraction, materials and power; manufacturing; building and
  property.
- **Acts V–VI** are distribution: transport and networks; retail, wholesale and hospitality.
- **Act VII** is information: software, the cloud, advertising, media, games, music and AI.
- **Act VIII** is finance, treated as seven industries with products, costs and customers.
- **Act IX** is the industries whose product is a person's time: health care, education, professional
  services, outsourcing and sport.
- **Act X** puts the industries side by side: the energy transition, chokepoints, conglomerates, the birth and
  death of industries, and national models.
- **Act XI** is the job: how industries are analysed for money, a commercial due diligence, and a report
  written from a blank page.

The order inside Acts II–IX follows the input-output table of Part 2: an industry comes after the ones it buys
from, as far as that is possible.

**Every date, number, name and attribution in this draft is written from memory and is to be treated as
(verify) until its part's sweep (§1.2), whether or not it is marked.** Nothing here has been checked against a
source yet. The marks single out the ones most likely to be wrong.

## 1. The standard every part meets

1. **One question, five answers.** The part's question is on its card and stays in the corner. The part answers
   the series' five questions in order: what is sold; how it is made and what one more costs; where the dollar
   goes; why it stays there; what moves it.
2. **A machine, built.** Every part builds at least one model company in the Works from physical primitives,
   computes its statements, and lays them beside the filings of at least three real companies. The comparison
   is shown as a table with the differences explained, not as a claim that the model is right.
3. **Run it** comes within the first fifteen minutes and before the model that explains it.
4. **The process is shown.** The physical or operational process (a wafer through a fab, a claim through an
   insurer, a container through a port) is animated step by step, with the quantities that matter at each step.
   No chapter is only text.
5. **The Dollar is drawn** for one representative transaction, to the last link the sources can support, with
   the unsupported remainder shown as a grey bar and labelled.
6. **The Board gets its ten rows** (§2.6), each with a Register row.
7. **The landscape is dated.** The Map chapter states its as-of date on screen, covers the five regions (§1.1,
   item 12) and draws its numbers from the Register at render time.
8. **Called it?** One dated forecast about the industry, shown with its outcome. Right and wrong calls both
   appear. Where the series makes its own call it is logged with a date and a rule for scoring.
9. **No advice.** No view on any security. Real companies are described from their own filings, by name,
   without logos.
10. **The watching standard** of *Economics, Built* (its SYLLABUS §1.3): cold open of 60–90 s with a person, a
    place, a date and something at stake; the four-minute rule; an intermission near the midpoint with a data
    film under the computed score; the recap answers the question card in one sentence; the last scene is the
    next part's problem.
11. **The course material** of `videos/coursekit/AUTHORING.md`: a course entry, a runnable lab (the part's
    model company, numpy and scipy only) and an interactive (Run it, on the site). The README's problems are
    of the kind an analyst is set: size this market, rebuild this margin, explain this ratio.
12. **Narration reads as prose,** since each part's page is its lecture notes (`tools/lecture_text.py`).

### 1.1 The coverage checklist

"Deep dive" means every part covers all of the following, each in a chapter or a named segment of one. A part
that leaves one out says why in its README.

1. **The product and its segments:** what is sold, to whom, in what units, and how the industry divides itself.
2. **Five dates:** the history that explains today's structure, in five events.
3. **The process:** how the thing is made or done.
4. **Unit economics:** price, cost and margin of one unit, and the drivers of each.
5. **Cost structure:** fixed against variable, capital intensity, scale, learning, the cost curve.
6. **Demand:** who buys, what moves the quantity, how sensitive it is to price and income.
7. **Pricing:** how the price is set in practice (contract, auction, list, negotiation, regulation).
8. **The chain:** suppliers, the industry, channels, customers; the Dollar.
9. **Structure:** concentration, entry and exit, the sources of advantage, returns on capital over time.
10. **The state:** regulation, licences, subsidies, public ownership, antitrust history.
11. **The cycle and the risks:** what the industry's downturns look like and what has bankrupted its firms.
12. **The landscape:** segments and leading companies, in America, China, Europe, Japan and Korea, and India
    (or the regions that matter, with a reason for the rest), as of a stated date.
13. **Labour:** who works in it, how they are paid, unions and skills.
14. **What is changing:** technology, entrants, regulation; the open questions, stated as questions.
15. **How to read it:** the industry's own measures and jargon (load factor, combined ratio, same-store sales),
    where they appear in a filing, and how they mislead.

### 1.2 The sweep

A part's chapter list is locked only after its sweep, which is done at build time with access to the sources:

1. Read the latest annual filings of the companies on the part's Map (at least the three largest per region)
   and the regulator's latest statistical release.
2. Enter every figure the part will show as a Register row: definition, source, the date of the fact, the date
   checked. Where two primary sources disagree, enter both and show the range.
3. Check every date, name and attribution in the part's syllabus entry against a primary source or a standard
   history, and correct the entry.
4. Size the market bottom-up in the part's `compute.py`, and reconcile it with the national accounts' figure
   for the industry where one exists. Record the gap.
5. List the events of the last twenty-four months that changed the structure, with dates.
6. Check each dataset's licence before it enters the Filing Room; record it in `data/SOURCES.md`.

### 1.3 Keeping it true

- Every Register row has a `checked` date and a `stale_after` date. `tools/check_register.py --stale` lists the
  rows that have passed theirs.
- Dated numbers are computed at render time and recorded with `tools/lecture_text.py <video> --record`, so the
  page and the film agree.
- The chapters of a part are either **durable** (the process, the cost structure, the mechanism) or **dated**
  (the Map, what is changing, the Board's rows). The manifest marks which. A refresh rebuilds the dated scenes
  only; narration and render caches are keyed by scene, so the durable scenes are untouched.
- A refresh that changes a durable chapter's argument is a new edition of the part, and its README says so.

### 1.4 Care

- Companies are described by what they file and what regulators and courts have found, with the source named.
  Allegations are called allegations.
- People who are alive are quoted only from the public record, with the date.
- Where an industry does harm (tobacco, gambling, opioids, emissions) the part states the evidence plainly in
  the chapter on the state and does not editorialize elsewhere.
- Rankings and shares are given with their definition (by revenue, by units, by capacity), because the order
  changes with it.

## 2. The devices

### 2.1 The Works

`explainer/industry/works/`, numpy and scipy only, tested in `tests/industry/`.

- `firm.py`: the generic firm. Operations (capacity, utilization, units, prices, input use) produce an income
  statement, a balance sheet and a cash flow statement that reconcile by construction; ratios; a DuPont
  breakdown; return on invested capital. Built in Part 3 and used by every part after.
- One module per industry (`oil.py`, `fab.py`, `airline.py`, `bank.py`, …), each a small set of physical
  primitives over `firm.py`. Each has a `calibrate` that sets its parameters from Register rows and a `compare`
  that lays its statements beside real companies' facts from the Filing Room.
- `stack.py` (the industry supply curve from producers' unit costs), `cycle.py` (capacity with lead times),
  `chain.py` (the Dollar: a transaction's revenue followed through the links), `size.py` (bottom-up market
  sizes with ranges), `diffusion.py`.
- **The web.** Each model company is given a name and a home. From Part 8 on a model company buys its inputs at
  prices set by earlier parts' model companies, through a shared price deck (`works/world.py`). The coupling is
  light: prices and quantities pass along the chain; there is no general equilibrium. Part 57 joins the web and
  breaks links in it.

A model company is a teaching model with a dozen parameters. It is checked for order of magnitude and for the
sign and size of its sensitivities, and the film shows where it fails.

### 2.2 The Unit

A strip drawn the same way in every part: the unit, its price, the stack of its costs, the margin. A second
strip beneath gives the unit of capacity and what it costs to add (a seat, a wafer start, a megawatt, a room).

### 2.3 The Dollar

A waterfall of one customer payment. Each link's bar is split into purchases from the next link, labour,
capital charges, tax and profit. The picture is drawn to the same scale in every part, so a viewer can compare
where the dollar goes for a flight, a pill and a search. Sources are filings' segment data, input-output
tables and regulators' cost data; what cannot be sourced is grey.

### 2.4 The Stack

Producers ordered by unit cost, width by capacity, with demand through it. It shows the marginal producer, the
rents of the others, and what a fall in demand does. Built on real cost data where it is public (power plants,
airlines' unit costs, mines from company reports) and on the model company's rivals elsewhere.

### 2.5 The Map

Segments across, regions down, companies as blocks sized by segment revenue and shaded by operating margin,
with the as-of date in the corner. A second view shows the same companies along the chain. Every block is a
Register row. Private and state-owned firms without filings are drawn hatched, with their source.

### 2.6 The Board

Ten rows per industry, defined once (Part 2) and never changed:

1. Revenue pool (global and American), as a range.
2. Value added, and its share of the economy's.
3. Employment.
4. Gross margin (median of the Map's listed companies).
5. Capital intensity (invested capital per dollar of revenue).
6. Return on invested capital, ten-year median and spread.
7. Concentration (share of the four largest, and the definition of the market it is taken over).
8. Cyclicality (the fall in revenue and in profit in the last two downturns).
9. Growth (ten-year, real).
10. Research and development as a share of revenue.

The Board is the series' cumulative picture. Part 2 shows it empty; each part fills a column; Act X reads
across it.

### 2.7 The Register

`explainer/industry/register.py`. A row is: a key, the figure (or a low and a high), its unit, its definition
in one sentence, the source (document, page or table, URL), the date of the fact, the date checked, the date
after which it is stale, and a note where sources disagree. `tools/check_register.py industryN` fails a part
that shows a figure with no row (scenes take figures only through `register.get`), and fails a row with no
primary source. Transcribed tables and passages go in `data/tables.py` with the date checked, as in the Data
Room of *Economics, Built*.

### 2.8 The Filing Room

`explainer/industry/data/`, with `SOURCES.md`. Frozen extracts, each with its licence and retrieval date, read
through one function per source and refreshed with `python -m explainer.industry.data --refresh NAME`. §3 is
the plan of what goes in it.

### 2.9 Run it

The viewer runs the model company for a few turns against the model's world. In the film it is a paused
decision with the outcome computed for each choice. On the site it is the part's interactive: a game on a small
kit (`course/site/widgets/00_run.js`), which stores and sends nothing, and which `tools/check_course.py` plays
with a scripted player.

### 2.10 Called it?

`explainer/industry/calls.py`: who forecast what about the industry, when, on what reasoning, and what
happened. Forecasts are taken from dated primary documents (a company's plan, an agency's outlook, a
consultant's published report). The series' own calls are entered with a scoring rule and a date to score
them.

## 3. The data plan

The series' market research is the sweep (§1.2) run over these sources. All are public; each one's licence and
terms of automated access are checked before it is used, and a source that does not allow reuse is cited and
linked but not redistributed.

**Across all parts**

- Company facts: the SEC's EDGAR (10-K, 20-F, S-1, the structured company-facts data); companies' annual
  reports and investor-day material elsewhere (Europe's ESEF filings, Japan's EDINET, the exchanges of Hong
  Kong, Shanghai, Shenzhen, Korea and India).
- The economy's accounts: the BEA's input-output and industry accounts; the Census Bureau's Economic Census
  (including concentration ratios), Annual Business Survey and Quarterly Financial Report; the BLS's employment
  and wages by industry and its producer prices; Eurostat's structural business statistics; the OECD's
  input-output and trade-in-value-added tables; China's National Bureau of Statistics; Japan's METI and e-Stat;
  India's MOSPI and Annual Survey of Industries; UN Comtrade and the WTO for trade; the World Bank.
- Competition and courts: decisions and market definitions from the FTC, the Department of Justice, the
  European Commission, the UK's CMA and China's SAMR, which state market shares on the record.

**By act** (the main public sources; each part's *Sources* line adds its own)

| Act | Sources |
|---|---|
| II. Out of the Ground | EIA (production, prices, refinery data, plant-level power data); the Energy Institute's Statistical Review; OPEC's bulletins; IEA's free tables; USGS Mineral Commodity Summaries; USDA (NASS, ERS, the WASDE); FAO; FERC's Form 1 and the system operators' market data; the EPA's water and waste data; Ofwat's cost data |
| III. Making | WSTS and SIA summaries; chip makers' filings (cost per wafer, capital spending); OICA and national registration data; the FAA and the manufacturers' order and delivery tables; defence budgets and contract data (USAspending); the FDA's Orange Book and approvals; ClinicalTrials.gov; CMS drug spending dashboards; the Census's manufacturing surveys |
| IV. Building | the Census's construction spending and housing starts; the Federal Reserve's and FHFA's mortgage and price data; the GSEs' disclosures; REIT filings; the BLS's productivity series |
| V. Moving | the BTS's Form 41 and T-100 airline data and DB1B fare sample; the Surface Transportation Board's railway reports (R-1); the FMCSA; UNCTAD's Review of Maritime Transport; port authorities; the FCC's reports and auction results; the ITU; Ofcom |
| VI. Selling and Serving | the Census's retail and e-commerce series; retailers' filings (stores, space, turns); franchise disclosure documents; the BLS's consumer expenditure survey; hotel companies' filings |
| VII. Information | filings (segment revenue, capital spending, retention where disclosed); the regulators' ad-market studies (the CMA's 2020 study, the ACCC's inquiry); court records of the platform antitrust cases; the system operators' and utilities' data-centre load filings |
| VIII. Money | the FDIC's call reports and Quarterly Banking Profile; the Federal Reserve's H.8, Y-9C and stress-test disclosures; the BIS; the NAIC's and state filings, insurers' statutory statements; the SEC's fund filings (N-PORT, 13F, Form ADV, Form PF aggregates); the Federal Reserve's payments studies; the central banks' payment statistics |
| IX. People | CMS's National Health Expenditure accounts, hospital cost reports and price-transparency files; the OECD's health statistics; IPEDS and the College Scorecard; the Census's services survey; India's NASSCOM summaries and the IT firms' filings; leagues' public accounts (the listed clubs, the Green Bay Packers' report) |
| X. Systems | IRENA's cost database; Lazard's published cost summaries; national auction results; the OECD's and WTO's chain data; export-control lists; all of the above |

**What cannot be had,** and what the series does instead:

- *Market shares by product in private markets.* Use competition authorities' decisions, and bottom-up sums of
  named companies' segment revenues with the remainder shown as a range.
- *Private and state-owned companies' accounts.* Use what they publish (bond prospectuses, state filings),
  hatch them on the Map, and say so.
- *Contract prices* (drug net prices, cloud discounts, freight contracts). Use regulators' and courts' records
  and companies' disclosed averages; show list against realized where both exist; leave the rest grey.
- *Cost curves by plant.* Public for power and partly for airlines, mines and refineries; elsewhere the Stack
  is built from company-level unit costs and labelled as such.

## 4. Part by part

Minutes in brackets are targets. Each entry gives the part's question and story; its unit and its Dollar; its
chapters (0 is the cold open and 1 is Run it unless noted; the last four are always the Map, *What is
changing*, the Board and *In practice*, and are listed only where they need a note); the model company the
Works gains and the filings it is laid beside; the game; the segments and companies the Map is expected to
place (to be fixed at the sweep); the forecast scored; the sources beyond §3; what it borrows from the other
series; and its reading. Chapter lists are a first draft: each is locked after the part's sweep.

Companies are named here as the ones the sweep should start from. A name on this list is not a claim about its
rank or share.

## Act I · Reading an Industry

### Part 1 · Where the Money Goes (~48)
*Question:* when you pay for something, who gets the money, and why them?
*Story:* a $299 music player on a bench in Irvine, 2007: the label says China, the trade data say China, the
money says California and Japan. Then 900,000 mobile phones by 2000. The whole method is run once, in
miniature, on a smartphone.
*Unit:* one phone. *Dollar:* retail price → carrier or retailer → brand → components (display, processor,
memory, camera, modem) → assembly → the makers of the tools that made the components.
0. Cold open: the teardown; the three answers; the title; the question card.
1. Run it: split a phone's price among eight firms before the answer is shown.
2. Value added: revenue minus purchases; why adding up revenues counts everything twice; the chain as a sum of
   value added that equals the price.
3. The teardown as a method: the bill of materials, what a teardown sees (parts) and misses (design, software,
   licences, marketing, the retailer's cut).
4. Who captures the value, and a first look at why: the part with one supplier against the part with ten.
5. The label and the statistics: gross exports against value added in trade (the OECD's tables); why a bilateral
   trade balance in phones says little.
6. The same phone as five questions: unit, process and cost, dollar, structure, change.
7. How we will know: the Register, the as-of stamp, the range; the mobile-phone forecast as the warning.
8. The series map: the acts on the input-output table, sealed; the Board, empty.
9. In practice: who needs this (the supplier pricing a part, the investor, the trade negotiator).
*The Works:* `chain.py` (a product with a bill of materials and a chain); laid beside the brand's, the
assembler's and three component makers' gross margins from their filings.
*Run it:* on the site, the split with the filing-based answer and the viewer's error.
*Map:* none (the series map takes its place).
*Called it?* the mobile-phone forecast (verify the source and the numbers; if it cannot be sourced to a primary
document it is told as a story and marked as one).
*Sources:* Linden, Kraemer and Dedrick (2009) and Kraemer, Linden and Dedrick (2011) on the iPod and iPhone;
the OECD's trade in value added; filings of the brand, the assembler and component makers.
*Borrowed:* *Economics, Built* Part 3 (value added, input-output) and Part 36 (trade in tasks).
*Reading:* the two teardown papers; Xing and Detert (2010); Baldwin, *The Great Convergence*; Gereffi,
Humphrey and Sturgeon (2005) on governance of chains.

### Part 2 · The Economy on One Page (~50)
*Question:* how big is each industry, and compared with what?
*Story:* Wassily Leontief's table of the American economy, 1936 (verify): 500,000 numbers on cards, and one
page that showed who buys from whom. The part draws the economy three ways and gets three different pictures.
*Unit:* a dollar of final demand. *Dollar:* a dollar spent by a household, followed back through every
industry it touches.
1. Run it: rank ten industries by size; then by jobs; then by profit. The three orders differ.
2. What an industry is: SIC, NAICS, ISIC, and the investors' GICS; why a company is not an industry (segments);
   the trouble with conglomerates and platforms.
3. Revenue, value added, employment, profit, market value: five sizes of the same industry, and when each is
   the right one.
4. The input-output table: reading a row and a column; the Leontief inverse as "everything a car needs".
5. Upstream and downstream: the series' order derived from the table.
6. The map by region: what America, China, Germany, Japan and India each make more of than their share.
7. A century of structure: farms to factories to services, in employment and in value added (and why the two
   lines differ: productivity and relative prices).
8. Where profit sits against where value added sits: returns on capital by industry, a first look.
9. The Board: its ten rows defined, with the sources for each; the first column filled for the whole economy.
*The Works:* `world.py` (an input-output economy of the model sectors, which the later parts' companies will
populate); laid beside the BEA's summary table.
*Run it:* the ranking game on the site, with real figures.
*Map:* the whole economy by sector and region.
*Called it?* Colin Clark's and Fourastié's forecasts of the service economy (1940s); or a published forecast of
industry employment shares against the outcome (the BLS's own projections, scored).
*Sources:* the BEA's input-output and GDP-by-industry accounts; the OECD's inter-country tables; the Census's
concentration ratios; the BLS's employment projections and their evaluations.
*Borrowed:* *Economics, Built* Part 3 (`accounts`: Leontief) and Part 63 (`network`: Domar weights,
upstreamness).
*Reading:* Leontief (1936, 1986); Antràs, Chor, Fally and Hillberry (2012) on upstreamness; Herrendorf,
Rogerson and Valentinyi (2014) on structural change; Baumol (1967).

### Part 3 · The Accounts (~55)
*Question:* what do a company's accounts say about the business underneath?
*Story:* Luca Pacioli prints the method in Venice, 1494; Donaldson Brown draws Du Pont's chart of return on
investment, about 1914–19 (verify), and takes it to General Motors. The part builds a company from its
operations and shows the statements falling out.
*Unit:* a dollar of invested capital. *Dollar:* a dollar of revenue down the income statement of five very
different companies.
1. Run it: six sets of ratios, six companies (a grocer, a bank, a software firm, a utility, an airline, a
   drug maker). Match them.
2. Operations first: capacity, units, prices and inputs; the income statement as their consequence.
3. The balance sheet: what the business had to buy and who paid for it; working capital and why a grocer is
   paid before it pays.
4. Cash against profit: accruals, depreciation, capital spending; a profitable company that runs out of cash.
5. The ratios that travel: gross and operating margin, turns, leverage; the Du Pont identity.
6. Return on invested capital, and the cost of capital in one chapter; growth that destroys value.
7. Unit economics: the same accounts per seat, per subscriber, per store; contribution margin and payback.
8. Where the accounts mislead: leases, goodwill, stock pay, research that is expensed, adjusted earnings,
   segments.
9. Reading a filing: where things are in a 10-K and a 20-F; the notes worth reading; the structured data.
*The Works:* `firm.py`, the generic firm, tested so that its three statements reconcile for any input; laid
beside the six companies of the game.
*Run it:* the matching game; then build a firm with sliders and watch the statements change.
*Map:* none; a table of the six.
*Called it?* a company whose reported profit and cash flow parted for years before it failed (Enron, 2001, or
Carillion, 2018; choose at the sweep).
*Sources:* EDGAR's company facts; IFRS and US GAAP on leases and revenue.
*Borrowed:* *Quant, Built*'s fundamentals where it has them.
*Reading:* Koller, Goedhart and Wessels, *Valuation*, chs on ROIC; Penman, *Financial Statement Analysis*;
Mauboussin on the base rates of returns; Chandler, *The Visible Hand*, on Du Pont and General Motors.

### Part 4 · The Cost Curve (~55)
*Question:* what does one more cost, and why does that decide almost everything?
*Story:* T. P. Wright measures how the labour in an airframe falls as more are built, 1936. A railway in the
1880s with a bridge paid for and a train half empty quotes almost any fare. Costs are the industry's physics.
*Unit:* the marginal unit. *Dollar:* a dollar of revenue at 60% and at 95% utilization.
1. Run it: a plant with a large fixed cost and an empty order book. A buyer offers below average cost. Take it?
2. Fixed, variable, sunk, avoidable: four words, four different decisions.
3. Scale: why big plants are cheaper per unit (the two-thirds rule, indivisibility, set-up), and where it
   stops; minimum efficient scale against the size of the market.
4. Scope and density: the second product on the same asset; the second customer on the same street.
5. Learning: Wright's law; the experience curve; what is learning and what is scale.
6. Capacity and utilization: operating leverage; the break-even load.
7. The industry's supply curve: the Stack, built for power plants from public data; the marginal producer sets
   the price; rents.
8. High fixed cost and price wars: why railways, airlines and memory chips fight to the death, and what
   industries do to stop it (cartels, mergers, capacity discipline, differentiation).
9. Zero marginal cost, the limiting case; a first look at Act VII.
*The Works:* `stack.py` and the cost functions; laid beside EIA plant data and airlines' unit costs.
*Run it:* the pricing game over ten periods against a rival with the same plant.
*Called it?* a learning-curve forecast against its outcome (solar module prices; Part 56 returns to it).
*Sources:* EIA Form 923/860; BTS Form 41; Wright (1936); the Boston Consulting Group's *Perspectives on
Experience* (1968).
*Borrowed:* *Economics, Built* Part 8 (`firm`: costs, entry), Part 12 (`oligopoly`: Bertrand with capacity) and
Part 48 (`climate`: Wright's law).
*Reading:* Scherer and Ross, chs 4 and 8; Pratten on scale; Chandler, *Scale and Scope*; Sutton, *Sunk Costs
and Market Structure*; Thompson (2012) on learning by doing.

### Part 5 · The Moat (~56)
*Question:* why do some industries earn high returns for decades while others never do?
*Story:* Joe Bain counts the barriers to entry in twenty industries, 1956; Michael Porter turns the field into
five forces, 1979. Then the test: the spread of returns on capital across industries, and whether structure
explains it.
*Unit:* a point of return above the cost of capital. *Dollar:* the same dollar of revenue in a commodity and in
a monopoly.
1. Run it: an entrant is coming. You have a budget: cut the price, build capacity, advertise, lobby, or lock
   customers in.
2. The facts first: returns on capital by industry over forty years; how far they persist; how much is the
   industry and how much the firm (Schmalensee 1985; McGahan and Porter 1997).
3. Concentration: shares, the four-firm ratio, the HHI; what it measures and what it does not; the market
   definition problem.
4. Barriers that are costs: scale against market size, sunk investment, learning.
5. Barriers that are customers: switching costs, search, habit, brands.
6. Barriers that are networks: each user makes the next more valuable; tipping; two sides.
7. Barriers that are law: licences, patents, standards, spectrum, landing slots.
8. The other forces: buyers and suppliers with power; substitutes; who holds the scarce link (Part 1 again).
9. Moats that drained: what ended the returns of newspapers, of Kodak, of the integrated steel mill.
*The Works:* `moat.py`: a market with free entry and five switches for the five kinds of barrier; the long-run
return under each.
*Run it:* the incumbent's game on the site.
*Called it?* an industry the five forces would have called unattractive that paid, or the reverse (airlines
after consolidation; tobacco after 1998).
*Sources:* company facts over forty years for returns by industry; the Census's concentration ratios;
competition authorities' decisions.
*Borrowed:* *Economics, Built* Parts 12, 43 and 44 (`oligopoly`, `io`): entry, markups, platforms.
*Reading:* Bain (1956); Porter (1979, 1980); Sutton (1991); Greenwald and Kahn; McGahan and Porter (1997);
De Loecker, Eeckhout and Unger (2020) and its critics.

### Part 6 · The Cycle (~54)
*Question:* why do industries keep building too much at the top?
*Story:* Mordecai Ezekiel's cobweb of hog prices, 1938. In 1973 shipowners have tankers on order equal to much
of the fleet afloat (verify); the oil price quadruples; the ships are delivered into a market that no longer
needs them and are laid up in Norwegian fjords.
*Unit:* a unit of capacity ordered today and delivered in three years. *Dollar:* a dollar of revenue at the
peak and at the trough.
1. Run it: freight rates are at a record. A yard quotes a ship for delivery in three years. Order?
2. The cobweb: a lead time and a forecast made from today's price.
3. The capital cycle: high returns, entry and expansion, oversupply, losses, exit; the same loop in ships,
   chips, mines, hotels and offices.
4. Why it does not get competed away: lead times, lumpy plants, the rival's order you cannot see, lenders who
   lend at the top.
5. Inventories: the bullwhip, from the shop to the chip maker.
6. Leverage twice: operating leverage times financial leverage; who survives a trough.
7. Demand cycles against supply cycles: durable goods, the accelerator, replacement.
8. Reading where you are: order books, capital spending against depreciation, utilization, second-hand prices.
9. Who profits: the low-cost producer, the one who buys at the bottom, the supplier paid in advance.
*The Works:* `cycle.py`: capacity with lead times and firms that forecast from current prices; laid beside the
order book and the fleet in shipping and capital spending in memory chips.
*Run it:* thirty years of a shipping market; the viewer's fleet against naive rivals.
*Called it?* a dated call of a peak (an industry's record capital spending announced in a boom year, and what
followed).
*Sources:* UNCTAD; Clarkson's public summaries; chip makers' filings.
*Borrowed:* *Economics, Built* Part 2 (the cobweb in `market`) and Part 67 (Brock and Hommes).
*Reading:* Ezekiel (1938); Stopford, *Maritime Economics*; Chancellor (ed.), *Capital Returns*; Kalouptsidi
(2014) on time to build; Lee, Padmanabhan and Whang (1997) on the bullwhip; Greenwood and Hanson (2015).

### Part 7 · Sizing a Market (~55)
*Question:* how big is a market, and how would anyone know?
*Story:* the 900,000 phones. Then a prospectus that put its "total addressable market" in the trillions
(choose a primary example at the sweep). The part does a market sizing live, three ways, and gets three
answers.
*Unit:* a market: buyers × purchases × price, with a definition. *Dollar:* none; the Register takes its place.
1. Run it: size a market (bottled water in one country) from six facts on screen. Commit to a number.
2. Definition is most of it: which products, which buyers, at which level of the chain (maker's price or
   retail), which year, which currency.
3. Top-down: from the national accounts and the census. What the statistical offices measure, and their lags.
4. Bottom-up: units × price; and the sum of named companies' segment revenues plus a remainder.
5. Triangulation: when the three disagree, which is wrong and why; showing a range.
6. Surveys and panels: what scanner, card and app data see; samples that are not the population.
7. Forecasts: diffusion and the Bass model; S-curves; forecasting the price as well as the quantity; the
   record of long-range industry forecasts.
8. How the commercial numbers are made, and why two firms' estimates differ by a factor of two; addressable
   markets in prospectuses.
9. The Register and the sweep, as the series will run them; the as-of stamp.
*The Works:* `size.py` (ranges, reconciliation with the accounts) and `diffusion.py`; tested on markets whose
size is known from a census.
*Run it:* the sizing game with the reconciled answer.
*Called it?* the phone forecast in full; a set of dated technology-adoption forecasts scored.
*Sources:* the Economic Census; company segment data; prospectuses; the EIA's and IEA's published
retrospectives on their own forecasts.
*Borrowed:* *Statistics, Built* (survey sampling; `survey`); *Economics, Built* Part 57 (forecast scoring).
*Reading:* Bass (1969); Rogers, *Diffusion of Innovations*; Griliches (1957) on hybrid corn; Tetlock on
forecast records; Smil on energy forecasts.

## Act II · Out of the Ground

### Part 8 · Oil and Gas (~58)
*Question:* what does a barrel cost, and who decides what it sells for?
*Story:* Spindletop blows in, Texas, January 1901, and the price of oil falls to cents. On 20 April 2020 a
futures contract for American crude settles below zero. In between: a product nobody can do without for a
month, that takes years to bring on, and that costs anything from a few dollars to eighty to produce.
*Unit:* a barrel (and a million British thermal units of gas). *Dollar:* a litre of petrol at the pump →
tax → retailer → refiner → pipeline and tanker → producer → the state that owns the rock → the service
companies that drilled it.
2. Geology in one chapter: source, reservoir, trap; conventional fields, shale, deep water, oil sands.
3. Finding and developing: exploration odds, the well, the decline curve; reserves as an economic number (the
   categories and what a booking means).
4. The cost of a barrel: finding, development, lifting, transport, the state's take; the Stack for world oil.
5. Who owns it: the national oil companies, the majors, the independents; concessions, production sharing and
   service contracts.
6. The price: benchmarks (Brent, WTI, Dubai), the futures curve, storage; why demand and supply are both
   inelastic in the short run and what that does to price.
7. OPEC: a cartel's arithmetic with one swing producer; quotas and cheating; 1973, 1986, 2014, 2020.
8. Shale: a factory process with a steep decline; the short-cycle barrel; what it did to the price ceiling.
9. Midstream and refining: pipelines as regulated tolls; the refinery as a spread business (the crack spread),
   complexity, closures.
10. Gas and LNG: a regional commodity made global by liquefaction; long-term contracts and oil indexation;
    Europe, 2022.
11. Oilfield services: day rates and the sharpest cycle in the industry.
*The Works:* `oil.py`: a field (reserves, decline, capital and operating cost, fiscal terms), a refinery
(yields, crack spread) and the price deck that later parts buy from; laid beside two majors, two shale
producers and a refiner.
*Run it:* a company with three prospects and a price that wanders: drill, wait or buy back.
*Map:* national companies (Saudi Aramco, ADNOC, CNPC/PetroChina, Sinopec, Rosneft, Petrobras, ONGC), majors
(ExxonMobil, Chevron, Shell, BP, TotalEnergies), independents and shale producers, services (SLB, Halliburton,
Baker Hughes), refiners (Valero, Marathon, Reliance), LNG (QatarEnergy, Cheniere), traders (Vitol, Trafigura,
Glencore).
*Called it?* Hubbert's 1956 forecast of the American peak (right for 1970, then overturned by shale); the
"peak oil" calls of 2005–08.
*Sources:* EIA; the Energy Institute's Statistical Review; OPEC's Annual Statistical Bulletin; companies'
reserve disclosures; the CME's settlement data for April 2020.
*Borrowed:* *Economics, Built* Part 48 (`climate`: Hotelling's paths) and Part 12 (cartels, Green and Porter).
*Reading:* Yergin, *The Prize* and *The Quest*; Adelman on the cost of oil; Hamilton (2009) on oil shocks;
Kilian (2009); Anderson, Kellogg and Salant (2018) on Hotelling under pressure.

### Part 9 · Mining and Metals (~52)
*Question:* why is a mine worth a fortune in one decade and nothing in the next?
*Story:* Escondida, a copper deposit hidden under the Atacama desert, is found by a drilling programme in 1981
(verify) and becomes the largest copper mine on earth. A mine is a bet of billions on a price thirty years
out.
*Unit:* a tonne of metal (and a tonne of ore at a grade). *Dollar:* a dollar of copper wire → fabricator →
refiner and smelter (treatment charges) → mine → royalty and tax → equipment and energy.
2. From rock to metal: exploration, the resource and the reserve, open pit and underground, crushing,
   concentrating, smelting, refining.
3. Grade is destiny: tonnes moved per tonne of metal; falling grades and what they do to cost.
4. The mine plan: capital up front, a life, a closure bill; net present value under a price deck; the option
   to wait.
5. The cost curve by mine: cash cost, all-in sustaining cost, by-product credits; the Stack for copper and
   for iron ore.
6. Iron ore: three companies, two regions, one customer; the end of the annual benchmark, 2010.
7. How metals are priced: the London Metal Exchange, treatment charges, premiums; the smelter's position.
8. The supercycle: China's demand, 2003–11, the response, and the write-offs that followed.
9. The state: royalties, resource nationalism, licences revoked; artisanal mining.
10. Critical minerals: lithium, cobalt, nickel, rare earths; small markets, concentrated processing, wild
    prices.
11. Gold: a mine with a product nobody uses up; streaming and royalty companies.
*The Works:* `mine.py`: a deposit with tonnage and grade, a plan, a cost position; laid beside three
diversified miners and a pure copper producer.
*Run it:* develop, delay or sell a deposit as the price cycles; the viewer's NPV against the mine's realized
life.
*Map:* diversified (BHP, Rio Tinto, Vale, Glencore, Anglo American), copper (Codelco, Freeport-McMoRan,
Southern Copper), China (Zijin, CMOC, China Shenhua for coal), India (Coal India, Vedanta), gold (Newmont,
Barrick), lithium and rare earths (SQM, Albemarle, Ganfeng, China Northern Rare Earth), royalty companies.
*Called it?* the Simon–Ehrlich bet (1980–90) on five metals; forecasts of the lithium price.
*Sources:* USGS Mineral Commodity Summaries; companies' technical reports (NI 43-101, JORC) and cost
disclosures; Cochilco.
*Borrowed:* *Economics, Built* Part 48 (the bet over every window; Hotelling) and Part 23 (the option to wait).
*Reading:* Tilton and Guzmán, *Mineral Economics and Policy*; Radetzki; Brennan and Schwartz (1985);
Humphreys, *The Remaking of the Mining Industry*.

### Part 10 · Farming and Food (~55)
*Question:* why are farmers price takers, and who along the chain is not?
*Story:* Norman Borlaug's dwarf wheat in Mexico and then the Punjab, 1960s: yields double and the predicted
famines do not come. The farmer who grew it captured little of the gain. The part follows a bushel to a loaf.
*Unit:* a bushel or a tonne; a hectare. *Dollar:* a dollar of food at the till → retailer → processor and
packer → trader and elevator → farmer → seed, fertilizer, machinery, land rent (the USDA's food dollar).
2. A farm's arithmetic: yield × price − inputs − rent; land as the residual claimant.
3. Why supply does not fall when prices do: many producers, fixed land, the treadmill of technology (Cochrane).
4. Inputs, where the concentration is: seed and traits, crop chemicals, fertilizer (Part 12), machinery
   (Part 19).
5. The grain trade: elevators, basis, storage, the big traders' thin margins and logistics.
6. Futures: hedging a crop; the Chicago contracts; speculators; what a futures price forecasts.
7. Meat: feed conversion, contract growers, the packers; four firms and the cattle price.
8. Processing and brands: where a bushel becomes a box, and the margin with it (Part 22).
9. The state: price supports, crop insurance, the Common Agricultural Policy, tariffs, export bans; minimum
   support prices in India; grain reserves in China.
10. Land: who owns it, rents against prices, farmland as an asset.
11. Plantation and tropical crops: palm oil, coffee, cocoa; smallholders and boards.
*The Works:* `farm.py`: a farm with a crop choice and a hedge, an elevator, a packer; laid beside the USDA's
cost-of-production accounts and two processors' and two input makers' filings.
*Run it:* three seasons: choose the crop, the hedge and the day to sell.
*Map:* traders (ADM, Bunge, Cargill, Louis Dreyfus, COFCO), inputs (Bayer, Corteva, Syngenta, Nutrien, Deere),
meat (JBS, Tyson, WH Group), cooperatives (Amul, CHS, Fonterra), palm oil (Wilmar), state buyers.
*Called it?* Ehrlich's *Population Bomb* (1968) on famine in the 1970s; the USDA's baseline projections scored.
*Sources:* USDA ERS (the food dollar, costs and returns), NASS and the WASDE; FAOSTAT; CME data.
*Borrowed:* *Economics, Built* Part 2 (the scissors on Pink Sheet data) and Part 46 (`village`).
*Reading:* Gardner, *American Agriculture in the Twentieth Century*; Cochrane on the treadmill; Morgan,
*Merchants of Grain*; Working (1949) on storage; MacDonald on concentration in packing.

### Part 11 · Heavy Materials (~52)
*Question:* why do the things everything is made of earn so little?
*Story:* Henry Bessemer's converter, 1856: steel from a luxury to a rail. Then Nucor's first thin-slab caster
at Crawfordsville, 1989 (verify), and the big integrated mills retreat from one product after another.
*Unit:* a tonne of steel; a tonne of cement. *Dollar:* a dollar of steel beam → service centre → mill → ore,
coking coal, scrap, power; and a dollar of ready-mix → cement → fuel and limestone.
2. Steel two ways: the blast furnace and the oxygen converter against the electric arc furnace; ore and coke
   against scrap and power.
3. The mill's costs: a huge fixed plant that must run; the spread over raw materials.
4. Minimills and disruption from below: rebar, then beams, then sheet.
5. Overcapacity: China makes about half the world's steel (verify); exports, tariffs, anti-dumping cases; why
   capacity does not close.
6. Cement: limestone, a kiln and fuel; heavy and cheap, so a plant's market is a circle on a map; local
   oligopolies and their cartel cases.
7. Aluminium: electricity in solid form; smelters follow cheap power.
8. Glass, paper and packaging: continuous processes, consolidation, the box as an index of trade.
9. Aggregates: the quarry as a local monopoly with a permit.
10. Carbon: the two largest industrial emitters; hydrogen steel, clinker substitutes, a border carbon price.
*The Works:* `mill.py`: an integrated mill, a minimill and a cement kiln with a delivery radius; laid beside
two steel makers by each route, two cement groups and an aluminium producer.
*Run it:* a mill through a glut: cut price, cut output, or idle a furnace that costs a fortune to restart.
*Map:* steel (China Baowu, ArcelorMittal, Nippon Steel, POSCO, Nucor, Tata Steel, JSW), cement (Holcim,
Heidelberg Materials, Cemex, CNBM, Anhui Conch, UltraTech), aluminium (Chalco, Hongqiao, Rio Tinto, Alcoa,
Hindalco), packaging and paper (International Paper, Smurfit Westrock), aggregates (Vulcan, Martin Marietta).
*Called it?* forecasts of China's steel peak, made yearly from about 2010.
*Sources:* the World Steel Association's yearbook; USGS on cement and aluminium; the European Commission's
cement cartel decision; companies' cost disclosures.
*Borrowed:* *Economics, Built* Part 12 (Hotelling's line, capacity) and Part 43 (Bresnahan and Reiss's
thresholds for local markets).
*Reading:* Christensen, *The Innovator's Dilemma*, ch. on minimills; Collard-Wexler and De Loecker (2015);
Syverson (2004) on ready-mix concrete; Smil, *Making the Modern World*; Misa, *A Nation of Steel*.

### Part 12 · Chemicals (~52)
*Question:* how does a molecule of gas become a thousand products, and where in the chain is the money?
*Story:* Fritz Haber fixes nitrogen on a bench in 1909; Carl Bosch scales it at Oppau by 1913. About half the
nitrogen in human bodies now comes through that process (verify). The part walks the tree from methane and
ethane to fertilizer and plastics.
*Unit:* a tonne of ethylene; a tonne of ammonia. *Dollar:* a dollar of plastic packaging → converter →
polymer maker → cracker → feedstock (gas liquids or naphtha).
2. The tree: seven base chemicals from oil, gas and salt; intermediates; polymers, fertilizers, solvents.
3. The cracker: a furnace the size of a district; feedstock is most of the cost; ethane against naphtha.
4. The feedstock advantage: the Gulf Coast after shale, the Middle East, coal-to-chemicals in China; the
   global cost curve.
5. The commodity cycle: world-scale plants arriving in waves; margins from peak to trough.
6. Fertilizer: nitrogen from gas, potash and phosphate from mines; a cartel in potash; food prices and gas
   prices tied together.
7. Industrial gases: the plant at the customer's fence, the fifteen-year take-or-pay contract; the most
   stable returns in the sector.
8. Specialty chemicals: sold on performance, not weight; small volumes, high margins, formulations.
9. The integrated site (the Verbund) against the focused company; the breakups of the conglomerates.
10. The state and harm: plant safety (Bhopal, 1984), persistent chemicals, plastics rules, energy prices in
    Europe after 2022.
*The Works:* `cracker.py`: a cracker with a feedstock choice and a product slate; an on-site gas plant with a
contract; laid beside two commodity producers, an industrial gas company and a specialty company.
*Run it:* choose the feedstock and the site for a cracker that will run for forty years.
*Map:* integrated (BASF, Dow, LyondellBasell, SABIC, Sinopec, Reliance, Formosa, Wanhua), gases (Linde, Air
Liquide, Air Products), fertilizer (Nutrien, Yara, CF, Mosaic), specialties (Sherwin-Williams, Givaudan,
Shin-Etsu), Japan's and Korea's groups (Mitsubishi Chemical, LG Chem).
*Called it?* forecasts of American chemical decline before shale (about 2005) against the investment wave
after 2012.
*Sources:* the American Chemistry Council's and Cefic's published statistics; EIA on gas liquids; companies'
segment data; the IFA on fertilizer.
*Borrowed:* *Economics, Built* Part 14 (contracts) and Part 8 (hold-up at the fence).
*Reading:* Smil, *Enriching the Earth*; Aftalion, *A History of the International Chemical Industry*; Arora,
Landau and Rosenberg (eds), *Chemicals and Long-Term Economic Growth*; Joskow (1987) on contract length.

### Part 13 · Electricity (~58)
*Question:* how is a product that cannot be stored sold every second, and who pays for the wires?
*Story:* Samuel Insull in Chicago in the 1890s works out that a power station's cost is its peak, and sells
cheap power off-peak to fill it. In California in 2000–01 a redesigned market, a drought and traders with
names for their schemes turn the lights off (verify the details at the sweep).
*Unit:* a megawatt-hour of energy and a megawatt of capacity. *Dollar:* a household's bill → retail →
distribution → transmission → generation → fuel; and taxes and levies.
2. The physics that makes it different: supply equals demand every instant; the load curve; the grid as one
   machine.
3. Generation: the technologies as fixed cost against running cost; the screening curve; baseload, mid-merit,
   peakers.
4. Dispatch: the merit order (the Stack, from plant data); the marginal plant sets the price; gas sets it more
   often than it supplies.
5. The regulated utility: the rate base, the allowed return, the rate case; the incentive to build.
6. Markets: the pool, the day-ahead auction, locational prices, capacity markets, scarcity pricing; what went
   wrong in California and in Texas in February 2021.
7. Wind and solar: zero running cost; what they do to the merit order and to their own revenue; levelized
   cost and why it is not the whole cost.
8. Storage and flexibility: batteries as arbitrage; pumped hydro; demand response.
9. Networks: transmission as a natural monopoly; queues to connect; who pays.
10. Retail: the supplier's thin margin and its hedges; the failures of 2021–22 in Britain.
11. Around the world: State Grid and the five generators in China; EDF's nuclear fleet; India's distribution
    losses; new load from data centres (Part 37).
*The Works:* `power.py`: a system of plants dispatched against a load curve, a regulated utility with a rate
base, a merchant plant; laid beside a regulated utility, a merchant generator and a renewables developer.
*Run it:* bid a gas plant into a day-ahead market for a week that includes a cold snap.
*Map:* regulated American utilities (NextEra, Duke, Southern), merchant generators (Vistra, Constellation),
Europe (EDF, Enel, Iberdrola, RWE, Ørsted), China (State Grid, Huaneng, Three Gorges), India (NTPC, Adani,
Tata Power), Japan and Korea (TEPCO, KEPCO), equipment (GE Vernova, Siemens Energy, Vestas).
*Called it?* the forecasts of American electricity demand of the 1970s and the plants cancelled after;
forecasts of flat demand in the 2010s against data-centre load.
*Sources:* EIA Forms 860, 861, 923 and 930; FERC Form 1; the system operators' price data; Ofgem.
*Borrowed:* *Economics, Built* Part 48 (`climate`: a merit-order market with withholding), Part 10 (Ramsey
prices, the Averch–Johnson firm) and Part 16 (uniform-price auctions).
*Reading:* Hughes, *Networks of Power*; Stoft, *Power System Economics*; Borenstein (2002) on California;
Joskow (1997, 2011); Wolak; Borenstein, Bushnell and Wolak (2002).

### Part 14 · Water and Waste (~45)
*Question:* why are the businesses nobody thinks about among the steadiest there are?
*Story:* the Great Stink of London, 1858; Parliament, beside the river, votes for Bazalgette's sewers in
eighteen days (verify). A century later, a rubbish hauler in Chicago starts buying its rivals and then the
landfills they tip into.
*Unit:* a cubic metre of water; a tonne of waste; a stop on a route. *Dollar:* a household's waste bill →
collection → transfer → landfill or incinerator; a water bill → operations → the capital programme → the
owners of the regulated assets.
2. Water as a system: source, treatment, pipes, sewers; almost all cost is fixed, in assets that last a
   century.
3. The regulated water company: the asset base, the price review, leverage; England's privatization of 1989
   and its record, including Thames Water.
4. Public and private elsewhere: municipal systems in America; concessions in France; tariffs below cost in
   India; desalination.
5. Waste collection: route density; why the second truck on a street loses money.
6. The landfill: a permit nobody will grant twice; airspace as an inventory that is depleted and priced;
   vertical integration from truck to tip.
7. Recycling and incineration: commodity prices for bales; China's import ban of 2018; who pays for sorting.
8. Hazardous, medical and industrial waste: regulation creates the market.
9. Returns: why these firms are bought by infrastructure funds; inflation-linked contracts.
*The Works:* `utility.py` (a regulated asset base under a price cap) and `route.py` (collection density and a
landfill's airspace); laid beside two water companies and two waste companies.
*Run it:* price a landfill's remaining airspace as the next one takes fifteen years to permit.
*Map:* waste (Waste Management, Republic Services, Veolia, Waste Connections), water (American Water, Severn
Trent, United Utilities, Veolia and Suez, Beijing Enterprises Water, Sabesp), municipal systems.
*Called it?* the "landfill crisis" forecasts of the late 1980s against capacity since.
*Sources:* Ofwat's cost models and annual performance reports; the EPA's waste and water data; companies'
airspace disclosures.
*Borrowed:* *Economics, Built* Part 10 (the regulated firm), Part 59 (`merger`: a price cap with resets) and
Part 43 (local market thresholds).
*Reading:* Halliday, *The Great Stink of London*; Helm on British utility regulation; Richard Porter, *The
Economics of Waste*; Crooks, *Giants of Garbage*.

## Act III · Making

### Part 15 · Semiconductors (~60)
*Question:* why does the most valuable manufactured product on earth come from so few factories?
*Story:* Gordon Moore's four-page article, 1965: the number of components on a chip will double every year.
Morris Chang, passed over in Texas, opens a factory in Hsinchu in 1987 that will make other people's chips and
design none of its own. The industry splits in two, and the split decides everything after.
*Unit:* a wafer, a die, a transistor; a wafer start per month of capacity. *Dollar:* a dollar of processor →
designer → foundry → equipment, materials, design software and licensed cores → packaging and test.
2. How a chip is made: silicon to wafer; deposit, pattern, etch, hundreds of times; lithography and the
   wavelength; packaging and test.
3. The node: what the number means and no longer means; cost per transistor; the cost of a mask set and of a
   design.
4. Yield: defects per area, die size, the yield curve; learning on a new node; why the leader earns the
   profit.
5. The fab: tens of billions, a five-year life for the tools, and utilization as the whole income statement.
6. Fabless and foundry: why the split happened; the foundry's scale and trust; the integrated makers that
   remained.
7. The tools: lithography from one company, a few makers for each other step; design software from three;
   licensed cores.
8. Memory: a commodity with a brutal cycle; from twenty makers to three; the price of a bit.
9. Analog, power and the trailing edge: old fabs, long product lives, steady margins; the shortage of 2021.
10. The end markets: phones, PCs, data centres, cars; accelerators for AI and what they did to the mix
    (Part 42).
11. Geography and the state: Taiwan, Korea, America, Japan, the Netherlands, China; export controls since
    2022; subsidy programmes; what a fab costs in each place.
*The Works:* `fab.py`: a fab with a node, a capital bill, a yield learning curve and a loading; a fabless
designer that books it; laid beside a foundry, an integrated maker, a memory maker, a fabless designer and an
equipment maker.
*Run it:* you design chips. Build your own fab or book a foundry, at three levels of volume.
*Map:* foundry (TSMC, Samsung, GlobalFoundries, UMC, SMIC), integrated (Intel, Texas Instruments, Infineon,
STMicroelectronics, Renesas), fabless (Nvidia, Qualcomm, Broadcom, AMD, MediaTek), memory (Samsung, SK Hynix,
Micron, Kioxia, YMTC, CXMT), equipment (ASML, Applied Materials, Lam, Tokyo Electron, KLA), software and cores
(Synopsys, Cadence, Arm), packaging (ASE, Amkor).
*Called it?* Moore's own 1965 extrapolation and its 1975 revision; the International Technology Roadmap's
dates against delivery.
*Sources:* WSTS and SIA summaries; filings (capital spending, wafer prices where disclosed); SEMI's public
summaries; the export-control rules as published.
*Borrowed:* *Economics, Built* Part 21 (ideas), Part 44 (learning and dynamics) and Part 66 (`tradewar`:
learning by doing, subsidy races); *Computer Science, Built* for what a chip does.
*Reading:* Miller, *Chip War*; Moore (1965); Irwin and Klenow (1994) on learning spillovers; Flamm,
*Mismanaged Trade?*; Khan, Hounshell and Fuchs (2018) on the end of Moore's law.

### Part 16 · Electronics (~50)
*Question:* why does the company that builds the device keep the least of it?
*Story:* Stan Shih of Acer draws a curve like a smile in 1992: profit at the two ends, design and brand, and
almost none in the middle where the thing is assembled. A campus in Shenzhen and another in Zhengzhou employ
several hundred thousand people in the middle.
*Unit:* a device; a board. *Dollar:* Part 1's phone again, now with every link's capital and labour.
2. From design to box: architecture, components, the board, final assembly, test, logistics.
3. Contract manufacturing: why brands gave up their factories; the assembler's 2–4% margin and fast-turning
   capital.
4. The bill of materials: commodity parts against sole-source parts; how purchasing scale becomes margin.
5. Components with moats: displays (a capital-heavy cycle), image sensors, passives, connectors, batteries.
6. The cluster: Shenzhen and the Pearl River Delta; suppliers within an hour; why moving assembly is slow;
   Vietnam and India.
7. The brand's side: the operating system, the ecosystem, the service revenue on the installed base.
8. The PC as the earlier case: modularity, Wintel taking the profit, the box makers' margins.
9. Consumer electronics that commoditized: televisions, and what happened to Japan's makers.
10. Tariffs, entity lists and the reshuffling of the chain since 2018.
*The Works:* `device.py`: a brand and an assembler on one device, with a bill of materials and a ramp; laid
beside two brands, two assemblers and three component makers.
*Run it:* you are the assembler. A brand offers a huge order at a thin margin and wants a new plant in a year.
*Map:* brands (Apple, Samsung, Xiaomi, Lenovo, HP, Dell, Sony), assemblers (Hon Hai/Foxconn, Pegatron,
Luxshare, Quanta, Wistron, Flex, Jabil, Dixon in India), components (BOE, LG Display, Murata, TDK, Sony's
sensors, Amphenol, Sunny Optical).
*Called it?* forecasts that assembly would leave China quickly after the tariffs of 2018.
*Sources:* filings; customs data by product; the brands' published supplier lists.
*Borrowed:* *Economics, Built* Part 8 (hold-up, make or buy), Part 36 and Part 63 (specific inputs).
*Reading:* Sturgeon (2002) on modular production; Baldwin and Clark, *Design Rules*; Dedrick, Kraemer and
Linden (2010); Huang, *The Hardware Hacker*; Fuller on China's electronics firms.

### Part 17 · Automobiles (~58)
*Question:* why is it so hard to make money making the most desired consumer product of the century?
*Story:* Highland Park, 1913: the moving line cuts the hours to assemble a Model T from twelve to about one
and a half (verify). In the 1950s Taiichi Ohno, with no money for Ford's inventory, builds a system that works
without it. Then a third arrival: the electric car, and China.
*Unit:* a vehicle; a plant of 250,000 a year. *Dollar:* a dollar of car → dealer → maker (assembly, engineering,
warranty, marketing) → tier-one suppliers → tier two and materials; plus the loan.
2. How a car is made: press, body, paint, assembly; the engine and gearbox plants; four years and a billion
   to develop a model.
3. Scale and platforms: fixed cost over volume; one platform under many models; why groups merge.
4. The plant's break-even: utilization, the launch curve, the cost of incentives when it is missed.
5. Lean production: stock as hidden waste, the pull system, the supplier relationship; what the studies
   measured.
6. Suppliers: most of a car's value is bought in; the tiers; who has pricing power over whom.
7. Dealers: franchise laws, the dealer's own income (used cars, service, finance); direct sales.
8. The finance arm: a bank attached to a factory; leasing and residual values.
9. Where the profit is: pickups and luxury; trucks and tractors as a different business.
10. The electric car: the battery as the engine; a simpler car and a different chain; software; charging.
11. China: joint ventures to national champions; price wars and exports; Europe's and America's tariffs.
12. Labour: unions, the transplants, the strike of 2023.
*The Works:* `auto.py`: a car maker with platforms, plants, a launch cadence, dealers and a finance arm; laid
beside two volume makers, a premium maker, an electric maker and two suppliers.
*Run it:* launch a model: set the price, the incentive and the plant's shifts as orders come in.
*Map:* volume (Toyota, Volkswagen, Hyundai–Kia, Stellantis, GM, Ford, Honda, Renault–Nissan, Suzuki/Maruti),
premium (BMW, Mercedes-Benz), electric and China (Tesla, BYD, Geely, SAIC, Chery), India (Tata, Mahindra),
suppliers (Bosch, Denso, Magna, ZF, CATL, LG Energy Solution), dealers and used-car groups.
*Called it?* forecasts of electric vehicle share made in 2015–17 against the outcome by region.
*Sources:* OICA; national registration data; filings (units, incentives, the finance arms' accounts); the
unions' contracts; NHTSA.
*Borrowed:* *Economics, Built* Part 43 (`io`: the BLP car market and merger simulation), Part 8 and Part 66.
*Reading:* Womack, Jones and Roos, *The Machine That Changed the World*; Sloan, *My Years with General
Motors*; Berry, Levinsohn and Pakes (1995); Helper on suppliers; Klier and Rubenstein, *Who Really Made Your
Car?*

### Part 18 · Aerospace and Defence (~56)
*Question:* why are there only two makers of large airliners, and why does the engine maker sell at a loss?
*Story:* in 1966 Boeing commits more than the company is worth to the 747, on an order from Pan Am for
twenty-five (verify). Thirty years later a European consortium that had been a political project sells more
aircraft than Boeing. In defence the customer writes the specification, pays for the development and is the
only buyer.
*Unit:* an aircraft; a flight hour of engine service. *Dollar:* a dollar of airliner → airframer → engines,
avionics, structures → forgings and composites; and the airline's lifetime spend on the engine.
2. A programme's arithmetic: ten billion or more before the first delivery; break-even at several hundred
   aircraft; the learning curve.
3. Why two: scale, learning, the family of aircraft, the installed base; the entrants that failed and COMAC.
4. Launch aid and subsidy: the longest trade dispute at the WTO.
5. Programme accounting: profit booked on an estimate of the whole run; what happens when the estimate moves.
6. Engines: sold below cost, paid back over twenty-five years of parts and service; power by the hour.
7. The supply chain: a few risk-sharing partners; sole sources; the squeeze on suppliers and its cost;
   certification and the 737 MAX.
8. The order book and the cycle: ten years of backlog; lessors; deferrals.
9. Defence: one buyer; cost-plus and fixed-price contracts; the consolidation of 1993 onward; exports.
10. Defence budgets by country; why a fighter costs what it costs; drones and the cheap end.
11. Business jets, helicopters, maintenance; space is in Part 59.
*The Works:* `aircraft.py`: a programme with development cost, a learning curve and a delivery ramp; an engine
with an aftermarket annuity; laid beside the two airframers, two engine makers and two defence primes.
*Run it:* launch a new airliner or re-engine the old one, with a rival making the same choice.
*Map:* airframers (Airbus, Boeing, Embraer, COMAC), engines (GE Aerospace/CFM, RTX's Pratt & Whitney,
Rolls-Royce, Safran), defence (Lockheed Martin, RTX, Northrop Grumman, General Dynamics, BAE, AVIC, HAL,
Mitsubishi Heavy, Hanwha), suppliers (Spirit AeroSystems, Howmet, TransDigm), lessors (AerCap).
*Called it?* the forecasts for the A380 at its launch in 2000 against deliveries.
*Sources:* the manufacturers' order and delivery tables; filings; the WTO panel reports; the US defence
budget's justification books; SIPRI.
*Borrowed:* *Economics, Built* Part 66 (Brander and Spencer), Part 14 (contracts, the ratchet) and Part 4 of
this series.
*Reading:* Newhouse, *The Sporty Game*; Benkard (2000, 2004) on learning and the L-1011; Irwin and Pavcnik
(2004); Rogerson (1994) on defence procurement; Gansler, *Democracy's Arsenal*.

### Part 19 · Machinery (~50)
*Question:* how do the companies that make the machines earn more from them after the sale than at it?
*Story:* Cyrus McCormick sells reapers in the 1850s on credit, with a guarantee, through agents who also
repair them (verify). The machine was half the product. The other half (finance, parts, service, the dealer)
is where the industry's steady money has been ever since.
*Unit:* a machine; an installed machine-year. *Dollar:* a dollar of excavator → dealer → maker → components
(engines, hydraulics, bearings, controls) → castings and steel; then the dollars of parts over twenty years.
2. Capital goods: sold to businesses, bought when they are confident; orders fall by half in a recession.
3. The installed base: parts and service at double the margin; attach rates; the cost of a machine that is
   down.
4. Dealers and finance: Caterpillar's dealers; rental as a channel; the captive lender.
5. Reading the cycle: book-to-bill, backlog, pricing against material cost.
6. Niches: hundreds of products each with three makers; the German and Japanese mid-sized specialists;
   machine tools.
7. Automation: robots, controls and their software; density by country; who buys them.
8. Farm and construction machinery; trucks; elevators (a service business with a factory); HVAC.
9. The conglomerate: General Electric's century, from Edison to the three-way split; the "business system"
   companies.
10. China's makers: from buyers to competitors in excavators, cranes and robots.
*The Works:* `machine.py`: a maker with new sales on a cycle and an installed base that throws off service
revenue; laid beside four makers with different aftermarket shares.
*Run it:* a tender: cut the machine's price to win the base, or hold it.
*Map:* construction and farm (Caterpillar, Komatsu, Deere, CNH, Sany, XCMG), automation (Siemens, ABB, Fanuc,
Keyence, Rockwell, Schneider), elevators (Otis, Schindler, Kone), tools and components (DMG Mori, Atlas Copco,
Parker Hannifin, SKF), conglomerates (Honeywell, Hitachi, Larsen & Toubro), trucks (Daimler Truck, Volvo,
Paccar).
*Called it?* a machine-tool or robot forecast; General Electric's own targets in 2000 against its path.
*Sources:* filings; the International Federation of Robotics' public summaries; VDMA and the Japanese
machine-tool orders series.
*Borrowed:* *Economics, Built* Part 62 (`org`: the diversification discount) and Part 10 (the Coase problem
for durables).
*Reading:* Hounshell, *From the American System to Mass Production*; Simon, *Hidden Champions*; Gryta and
Mann, *Lights Out*; Cohen, Agrawal and Agrawal (2006) on winning in the aftermarket.

### Part 20 · Pharmaceuticals (~58)
*Question:* why does a pill that costs cents to make sell for dollars, and then one day for cents?
*Story:* on 30 November 2011 the American patent on Lipitor expires. It had been the best-selling drug in
history; within a year most of its revenue is gone (verify). Every drug company is a portfolio of such
dates, and of bets to replace them.
*Unit:* a course of treatment; a patent-year. *Dollar:* a dollar of drug spending → pharmacy → wholesaler →
rebates to the benefit manager and insurer → the maker (and inside it: manufacturing, sales, research,
profit). Part 51 follows the channel.
2. From target to pill: discovery, preclinical work, three phases of trials, approval; ten years.
3. The odds: about one in ten of the drugs that enter trials is approved (verify by phase and by field);
   the cost of a new drug with the failures and the time included, and the argument about that number.
4. A drug as an option: stage by stage, spend to learn; the value of stopping early.
5. Patents and exclusivity: the twenty years, what is left at launch, extensions, the thicket.
6. The cliff: generic entry, the first filer's 180 days, prices against the number of entrants.
7. Biologics: made in cells, hard to copy; biosimilars and their slower erosion.
8. The price: list against net; rebates; launch prices and what sets them; reference pricing and
   cost-effectiveness bodies abroad; Medicare's negotiation since 2022.
9. Selling: detailing, direct-to-consumer advertising, the specialist drug.
10. Biotech: the small company, venture and public funding, the partnership and the acquisition; who does the
    early research (the NIH's part).
11. Generics and contract makers: India and China in the supply of ingredients; shortages of cheap sterile
    drugs.
12. Harm and the law: the opioid cases.
*The Works:* `pharma.py`: a pipeline of candidates with stage costs and probabilities, a launch curve and a
cliff; laid beside four large companies' research spending and revenue by product age, and a generics maker.
*Run it:* a fixed research budget and twelve candidates: which to take forward at each stage.
*Map:* large companies (Pfizer, Merck, Johnson & Johnson, Eli Lilly, AbbVie, Novartis, Roche, AstraZeneca,
Novo Nordisk, Sanofi, GSK, Takeda), biotech (Amgen, Gilead, Vertex, Regeneron, BeiGene), generics (Teva,
Sandoz, Sun, Dr. Reddy's, Cipla), contract makers (Lonza, Samsung Biologics, WuXi), China (Hengrui).
*Called it?* published peak-sales forecasts at launch against outcomes; the "productivity crisis" calls of
about 2010.
*Sources:* the FDA's Orange and Purple Books and approval data; ClinicalTrials.gov; CMS's drug spending data;
filings (revenue by product); the Congressional Budget Office's studies.
*Borrowed:* *Economics, Built* Part 21 (patents), Part 23 (options), Part 10 (price discrimination across
countries) and Part 44 (killer acquisitions).
*Reading:* DiMasi, Grabowski and Hansen (2016) and its critics; Scannell et al. (2012), "Eroom's law"; Wong,
Siah and Lo (2019) on success rates; Scott Morton and Kyle (2011); Pisano, *Science Business*; Werth, *The
Billion-Dollar Molecule*.

### Part 21 · Medical Technology (~50)
*Question:* who is the customer when the user, the chooser and the payer are three different people?
*Story:* Minneapolis, 1957–58: Earl Bakken builds a battery pacemaker in a garage for a surgeon whose patients
had died in a power cut (verify). The surgeon chooses the device, the hospital buys it, an insurer pays, and
the patient wears it.
*Unit:* a procedure; an implant; a test. *Dollar:* the payment for a hip replacement → hospital → implant
maker → components; and the payment for a blood test → laboratory → instrument and reagent maker.
2. The kinds of device: implants, capital equipment, consumables, diagnostics; four different businesses.
3. Approval: the two American routes and why most devices take the shorter; Europe's rules; recalls.
4. The surgeon's preference: training, the representative in the operating theatre, switching costs made of
   skill.
5. The hospital's side: committees, group purchasing, bundled payment; the price nobody may disclose.
6. The installed base again: imaging scanners with service contracts; surgical robots with instruments per
   procedure; analysers with reagents.
7. Diagnostics: central laboratories (scale, routes, payers) against the test makers.
8. Life-science tools and contract research: selling picks and shovels to Part 20.
9. Incremental innovation and many small acquisitions; why the big firms are roll-ups.
10. China's volume-based procurement and what it did to prices; India's price caps on stents.
*The Works:* `medtech.py`: capital equipment placed with a consumable stream, and an implant sold
through a hospital contract; laid beside five companies across the four kinds.
*Run it:* place the machine free and sell the consumable, or sell the machine.
*Map:* devices (Medtronic, Abbott, Boston Scientific, Stryker, Johnson & Johnson MedTech, Intuitive Surgical,
Edwards), imaging (Siemens Healthineers, GE HealthCare, Philips, United Imaging), diagnostics and tools (Roche
Diagnostics, Danaher, Thermo Fisher, Illumina, Labcorp, Quest), contract research (IQVIA), Japan (Olympus,
Terumo), China (Mindray).
*Called it?* forecasts for a device category (drug-eluting stents, 2003) against its path.
*Sources:* the FDA's device databases; CMS payment rates by procedure; filings (procedures and installed
base where disclosed).
*Borrowed:* *Economics, Built* Part 10 (two-part tariffs) and Part 14 (the agent who is not the payer).
*Reading:* Gelijns and Rosenberg on device innovation; Grennan (2013) on price discrimination in stents;
Grennan and Swanson (2020) on price transparency; Christensen, *The Innovator's Prescription*.

### Part 22 · Consumer Goods (~52)
*Question:* why can a company charge double for soap, for a hundred years?
*Story:* on 13 May 1931 Neil McElroy, running advertising for Camay at Procter & Gamble, writes a memo of three
pages asking for a team for each brand (verify). The brand becomes the unit of management. The retailer that
sells it becomes its largest rival.
*Unit:* a case; a point of shelf share. *Dollar:* a dollar of breakfast cereal → retailer → trade promotion
back to the retailer → maker (ingredients, packaging, factory, freight, advertising, profit).
2. What a brand is, economically: a promise that saves search; a price premium that pays for the advertising
   that sustains it.
3. The factory is the easy part: cheap to make, expensive to sell; gross margins of a half and where they go.
4. Advertising as a fixed cost and a barrier (Sutton); the leader's share that never moves.
5. The shelf: slotting fees, category captains, trade spending; price promotions and what they train
   shoppers to do.
6. The retailer strikes back: own labels, the discounters, the buyer with a fifth of your sales.
7. Distribution systems: bottlers and concentrate; direct store delivery; three tiers for alcohol.
8. Pricing power tested: the inflation of 2021–23, volumes against price, pack sizes.
9. Growth by acquisition and by emerging markets; the small brand and the cost of entry online; zero-based
   budgets and their limits.
10. Tobacco and drink: the most profitable legal products; regulation as a barrier; the settlement of 1998.
*The Works:* `brand.py`: a brand with advertising stock and a retailer with a store label and shelf to
allocate; laid beside four makers across food, home, beauty and drink, and a retailer's own-label share.
*Run it:* a year as a brand manager: price, promotion and advertising against a store label.
*Map:* home and personal (Procter & Gamble, Unilever, L'Oréal, Colgate, Kao, Hindustan Unilever), food and
drink (Nestlé, PepsiCo, Coca-Cola and its bottlers, Mondelez, Danone, Kraft Heinz, Mengniu, Nongfu Spring,
ITC), alcohol (AB InBev, Diageo, Kweichow Moutai), tobacco (Philip Morris International, BAT, China National
Tobacco).
*Called it?* the "death of brands" after Marlboro Friday, 2 April 1993.
*Sources:* filings (organic growth split into price and volume, advertising spend); the BLS's price data; the
FTC's slotting-fee study; the Master Settlement Agreement.
*Borrowed:* *Economics, Built* Part 43 (`io`: Nevo's cereal margins), Part 60 (`revenue`: high-low against
everyday low prices) and Part 45 (reference prices).
*Reading:* Sutton, *Sunk Costs and Market Structure*; Nevo (2001); Bronnenberg, Dhar and Dubé (2009) on
persistent shares; Tedlow, *New and Improved*; Dyer, Dalzell and Olegario, *Rising Tide*.

### Part 23 · Fashion and Luxury (~50)
*Question:* how do two industries that sell clothes run on opposite rules?
*Story:* a design leaves a studio in Arteixo, Galicia, and is in shops on three continents fifteen days later
(verify). A leather bag from a workshop in France cannot be bought at any price by a customer the house does
not know. One industry sells speed and the other sells the wait.
*Unit:* a garment; a season's stock. *Dollar:* a dollar of T-shirt → retailer (rent, staff, markdowns) →
brand → factory (cut, make, trim) → fabric → fibre; and a dollar of handbag.
2. The apparel chain: fibre, yarn, fabric, cutting and sewing, shipping; the countries at each stage; the
   end of the quota system in 2005.
3. The buyer's problem: order six months ahead, sell in twelve weeks; the markdown as the cost of a wrong
   forecast (the newsvendor).
4. Fast fashion: short lead times bought with nearby production and spare capacity; fewer markdowns.
5. The ultra-fast model: small batches tested online and reordered; direct from factory by air.
6. The factory's side: wages, the price the buyer pays, Rana Plaza (2013) and audits.
7. Luxury: prices that rise with demand; scarcity that is managed; the atelier and the licence; why luxury
   owns its shops.
8. The groups: the house as a portfolio; leather goods against fashion against watches and jewellery.
9. Sport: the brand, the athlete, the contract factory; wholesale against direct.
10. The Chinese and Indian consumer; resale, rental and counterfeits; department stores (Part 60).
*The Works:* `fashion.py`: a retailer buying a season under uncertainty with a choice of lead time, and a
luxury house choosing volume and price; laid beside a fast-fashion group, a luxury group, a sportswear brand
and a contract manufacturer.
*Run it:* buy the season: how much, how early, and when to mark down.
*Map:* fast fashion (Inditex, H&M, Fast Retailing/Uniqlo, Shein), luxury (LVMH, Hermès, Kering, Richemont,
Chanel), sport (Nike, Adidas, Anta, Lululemon), makers (Shenzhou, Crystal, Arvind), off-price (TJX), jewellery
(Titan).
*Called it?* forecasts of luxury demand in China made before 2012 and before 2020.
*Sources:* filings (inventory, markdown commentary, own-store share); the WTO's textile and clothing trade
data; wage data from the ILO.
*Borrowed:* *Economics, Built* Part 60 (the newsvendor in `revenue`) and Part 45 (reference dependence).
*Reading:* Ghemawat and Nueno's Zara case (2003); Fisher and Raman, *The New Science of Retailing*; Kapferer
and Bastien, *The Luxury Strategy*; Rivoli, *The Travels of a T-Shirt in the Global Economy*; Veblen (1899);
Bagwell and Bernheim (1996).

## Act IV · Building

### Part 24 · Construction (~52)
*Question:* why has almost everything become cheaper to make except a building?
*Story:* the Empire State Building goes up in 410 days in 1930–31, ahead of schedule and under budget
(verify). A century on, large projects run late and over more often than not, and measured productivity in
construction is flat or lower than it was in 1970.
*Unit:* a square metre built; a contract. *Dollar:* a dollar of building → developer or owner → main
contractor (a 2–3% margin) → subcontractors by trade → labour, materials, plant hire; and design fees.
2. How a building is procured: owner, designer, main contractor, subcontractors; who carries which risk.
3. The bid: a sealed price for a thing not yet designed in full; the winner's curse; claims and change orders
   as the real margin.
4. A contractor's balance sheet: paid in advance, pays in arrears; negative working capital and sudden
   failures (Carillion, 2018).
5. Why productivity has not risen: every site a prototype; fragmentation; regulation; the measurement
   problem.
6. Megaprojects: the reference class of overruns; why estimates are low; what the on-time ones did.
7. Prefabrication and its record, from Operation Breakthrough to Katerra.
8. Infrastructure: concessions and public-private partnerships; availability payments; who really bears
   demand risk.
9. Engineering firms: selling hours (Part 53) against selling fixed-price projects.
10. Materials and equipment rental; labour, migrants and the trades.
11. China's builders and the Belt and Road; India's road programme; Japan's general contractors.
*The Works:* `contractor.py`: a contractor bidding for jobs with uncertain cost, with a cash cycle; a
concession; laid beside three contractors, an engineering firm and a concession owner.
*Run it:* five tenders against four rivals. Win too many at too low a price and the cash runs out.
*Map:* contractors (Vinci, ACS, Bouygues, Bechtel, Fluor, Skanska, China State Construction, China Railway
Group, Larsen & Toubro, Kajima, Obayashi), engineers (Jacobs, AECOM, WSP), concessions (Ferrovial, Transurban,
Vinci's motorways), rental (United Rentals, Ashtead).
*Called it?* the opening budget and date of a megaproject (the Channel Tunnel, the Big Dig, California's
high-speed rail) against the outcome.
*Sources:* the Census's construction spending; the BLS's productivity series; audit offices' project reports;
filings (margins, backlog).
*Borrowed:* *Economics, Built* Part 16 (`auctions`: the winner's curse) and Part 58 (`appraisal`: reference
classes).
*Reading:* Flyvbjerg and Gardner, *How Big Things Get Done*; Goolsbee and Syverson (2023) on construction
productivity; Bajari and Tadelis (2001) on contract form; Brooks and Liscow (2023) on highway costs.

### Part 25 · Homes (~54)
*Question:* where does the price of a house come from: the house, the land or the loan?
*Story:* Levittown, Long Island, 1947: a house every sixteen minutes at the peak (verify), sold to veterans
with a thirty-year loan the government insured. The house was a manufactured product. The loan was the
invention.
*Unit:* a home; a lot; a mortgage. *Dollar:* a dollar of new house → land → builder (materials, trades,
overhead, margin) → the broker's commission; and a dollar of mortgage payment → servicer → investor →
guarantor.
2. A builder's arithmetic: land, sticks and bricks, the sales rate; land as the thing that is scarce.
3. Land strategy: owning against optioning; the land bank through a cycle; 2007.
4. Why supply is slow: permits, zoning, minimum lots; prices against construction cost by city.
5. The mortgage: the thirty-year fixed loan as an American exception; who funds it elsewhere.
6. The mortgage chain: originator, servicer, securitizer, guarantor, investor; the right to prepay and who
   pays for it.
7. The broker: a commission that did not fall when search became free; the 2024 settlement.
8. Renting: the landlord's yield; institutional owners; rent regulation's evidence.
9. Renovation and the big-box stores; manufactured housing.
10. China: pre-sales, land revenue for local governments, the developers' collapse from 2021.
11. India, Japan (houses that depreciate), Germany (renters), Singapore (public housing).
*The Works:* `builder.py`: a builder with a land bank, a build cycle and a sales rate; a mortgage with
prepayment; laid beside three builders that own and one that options, and a mortgage originator.
*Run it:* buy land for delivery in three years, through a rate cycle.
*Map:* builders (D.R. Horton, Lennar, NVR, Barratt, Sekisui House, Vanke, Country Garden, DLF), mortgages
(Fannie Mae, Freddie Mac, Rocket, the banks), brokers and portals (Anywhere, Compass, Zillow, Rightmove, KE
Holdings), landlords (Invitation Homes, Vonovia), home improvement (Home Depot, Lowe's).
*Called it?* the housing forecasts of 2005–06 by the industry's economists against 2007–11; forecasts of
China's property sales in 2020.
*Sources:* the Census's housing data; FHFA and Case-Shiller indices; the GSEs' disclosures; builders' filings
(lots owned and optioned); China's NBS.
*Borrowed:* *Economics, Built* Part 37 (`city`: the monocentric city, housing supply), Part 33 (`credit`) and
Part 26 (banks).
*Reading:* Glaeser and Gyourko on supply; Shiller, *Irrational Exuberance*; Green and Wachter (2005) on the
American mortgage; Hsieh and Moretti (2003) on brokers; Rogoff and Yang (2021) on China.

### Part 26 · Property (~50)
*Question:* what is a building worth, and why does that number move so much when the building does not?
*Story:* William Zeckendorf in the 1950s cuts a building into pieces (the land, the lease, the mortgage) and
sells each to the buyer who values it most (verify). A commercial building is a bond with a roof, and its
value is its rent divided by a rate.
*Unit:* a square metre let; a dollar of net operating income. *Dollar:* a dollar of rent → operating costs
and tax → interest → the owner; and the tenant's side, rent as a share of sales.
2. Net operating income and the capitalization rate; value as their ratio; what a one-point move in the rate
   does.
3. The lease: term, steps, who pays the costs; the tenant's credit; the rent roll as the asset.
4. Debt: loan to value, refinancing, the maturity wall; who lends (banks, insurers, securitizations).
5. The sectors as different businesses: offices, shops and malls, warehouses, flats, hotels (Part 35), data
   halls (Part 37), cell towers (Part 30), storage.
6. Development: land, permits, construction, lease-up; the developer's option and its timing.
7. Owners: REITs and their rules, private funds, insurers, sovereign funds; listed against appraised values.
8. The services firms: brokers, managers, the asset-light giants.
9. Cycles: eighteen years, or not; 1990, 2008, and offices after 2020.
10. Malls and the internet; warehouses and the internet.
11. Hong Kong and Singapore's landlords; Japan's 1989; China's commercial property; India's office parks and
    REITs.
*The Works:* `building.py`: a building with a rent roll, costs, a loan and a cap rate; a development with a
start option; laid beside five REITs in five sectors.
*Run it:* your loan matures as rates double and a third of the building is empty.
*Map:* industrial (Prologis, Goodman), towers and data (American Tower, Equinix), retail (Simon, Unibail,
Link), office (BXP, Mitsubishi Estate, Mitsui Fudosan), diversified and Asia (Sun Hung Kai, CapitaLand, DLF,
Embassy), managers (Blackstone, Brookfield), services (CBRE, JLL).
*Called it?* forecasts of office occupancy made in 2020–21; mall forecasts of 2010.
*Sources:* REIT filings; the Federal Reserve's commercial property data; the FDIC on bank exposure; published
cap-rate surveys.
*Borrowed:* *Economics, Built* Part 23 (`assets`: the user cost, the option to wait) and Part 37.
*Reading:* Geltner, Miller, Clayton and Eichholtz, *Commercial Real Estate Analysis and Investments*;
Wheaton (1987, 1999) on office cycles; Gupta, Mittal and Van Nieuwerburgh (2022) on offices after the
pandemic.

## Act V · Moving

### Part 27 · Shipping and Ports (~54)
*Question:* how did moving a tonne across an ocean become nearly free, and why do the companies that do it
swing between fortune and ruin?
*Story:* on 26 April 1956 a converted tanker, the *Ideal-X*, leaves Newark with fifty-eight truck bodies on
deck. Loading loose cargo cost $5.83 a ton; Malcom McLean's boxes cost about 16 cents (verify). Part 6's
tankers return as the standing example of the cycle.
*Unit:* a container (TEU) moved; a tonne-mile; a ship-day. *Dollar:* the freight on a pair of trainers from
Vietnam to a shop in Ohio: ocean freight, terminal charges, drayage, rail or truck; the ship's daily cost
(capital, crew, fuel).
2. The kinds of ship and of trade: containers on schedules (liners); bulk and tankers hired by the voyage
   (tramps); gas carriers, car carriers.
3. The box: what it changed on the quay, in the port city and in the factory's location.
4. A ship's economics: the newbuilding price, operating cost, fuel and speed; slow steaming as a capacity
   decision.
5. Freight rates: perfectly inelastic supply at full use; the spot and the time charter; the indices.
6. The cycle in full: orders, deliveries, scrapping, lay-up; yards and their subsidies.
7. Liner shipping: a network with fixed schedules and huge fixed cost; conferences, alliances and their
   antitrust treatment; the consolidation of 2016–18; 2021's rates.
8. Ports and terminals: a concession on a piece of coast; the global operators; automation and dockers.
9. Chokepoints: Suez, Panama, Hormuz, Malacca; the *Ever Given*, 2021; the Red Sea, 2023–24.
10. Owners, flags and finance: Greek families, Chinese lessors, the open registries; the Jones Act.
11. Fuel and emissions rules; the cost of new fuels.
*The Works:* `ship.py`: a fleet on a simulated rate cycle with orders, charters and scrapping; a container
line with a network; a terminal; laid beside three liner companies, a tanker owner and a terminal operator.
*Run it:* thirty years as an owner: order, charter out, buy second-hand, scrap.
*Map:* liners (MSC, Maersk, CMA CGM, COSCO, Hapag-Lloyd, ONE, Evergreen, HMM), bulk and tankers (Frontline,
Star Bulk, Angelicoussis, China Merchants), yards (CSSC, HD Hyundai, Hanwha Ocean, Imabari), terminals (PSA,
Hutchison, DP World, APM, Adani Ports), lessors and brokers.
*Called it?* the liner forecasts behind the orders of 2021–22 against rates after.
*Sources:* UNCTAD's Review of Maritime Transport; liner companies' filings; port authorities' statistics; the
canal authorities.
*Borrowed:* this series' Part 6; *Economics, Built* Part 36 (trade costs and gravity).
*Reading:* Levinson, *The Box*; Stopford, *Maritime Economics*; Kalouptsidi (2014); Bernhofen, El-Sahli and
Kneller (2016); Greenwood and Hanson (2015) on waves in ship prices.

### Part 28 · Airlines (~58)
*Question:* why has an industry that changed the world lost money over most of its history?
*Story:* the Airline Deregulation Act, October 1978. Fares fall, new airlines arrive, and within a decade most
of them and several of the old ones are gone. At American, Robert Crandall's analysts build a system that
sells the same seat at twenty prices. (A pilot film; see §7.)
*Unit:* an available seat-mile; revenue per seat-mile against cost per seat-mile. *Dollar:* a dollar of
ticket → taxes and airport charges → fuel → labour → aircraft ownership and maintenance → distribution → the
airline's margin; and what the loyalty scheme adds.
2. A flight's arithmetic: seats, stage length, load factor, yield; why costs per seat-mile fall with distance.
3. The seat as the perfect perishable: marginal cost near zero until the next aircraft.
4. Yield management: fare classes, booking limits, overbooking; the business traveller pays for the route.
5. Networks: hub and spoke against point to point; connecting banks; the fortress hub and its fares.
6. Low-cost carriers: one aircraft type, fast turns, secondary airports; the ultra-low-cost model and its
   fees.
7. Costs you do not control: fuel and hedging; labour, seniority and contracts; maintenance.
8. Aircraft: buy, lease or sale-and-leaseback; the lessors; the order book (Part 18).
9. Airports and slots: the regulated airport, the slot as property, retail and parking.
10. Distribution: the reservation systems, agents, direct sales.
11. Loyalty: selling miles to banks; the scheme valued above the airline.
12. Bankruptcy, mergers and four airlines with most of the American market; alliances and joint ventures;
    state carriers and the Gulf; cargo.
*The Works:* `airline.py`: a network of routes, a fleet, fare classes with a booking curve, a cost model by
aircraft and stage; laid beside six American carriers' Form 41 data and two European and two Asian carriers'
filings.
*Run it:* one route, one hundred and eighty seats, sixty days of bookings: set the fares as it fills.
*Map:* network carriers (American, Delta, United, Lufthansa, IAG, Air France–KLM, the three Chinese groups,
ANA, JAL, Singapore, Emirates, Qatar, Turkish), low-cost (Southwest, Ryanair, easyJet, IndiGo, AirAsia,
Spring), cargo and integrators (Part 29), lessors (AerCap, Air Lease, BOC Aviation), airports (Aena, Fraport,
Heathrow, AAI), systems (Amadeus, Sabre).
*Called it?* the forecasts of the deregulators in 1978 (on fares, right; on the number of airlines, wrong);
IATA's traffic forecasts of early 2020.
*Sources:* BTS Form 41, T-100 and the DB1B fare sample; filings; Eurocontrol and airport regulators; IATA's
public summaries.
*Borrowed:* *Economics, Built* Part 60 (`revenue`: Littlewood's rule, EMSR-b, overbooking, dynamic pricing of
a flight) and Part 10 (price discrimination); it does not rebuild them.
*Reading:* Belobaba, Odoni and Barnhart (eds), *The Global Airline Industry*; Borenstein (1989, 1992, 2011);
Borenstein and Rose (2014), "How Airline Markets Work… or Do They?"; Petzinger, *Hard Landing*; Smith,
Leimkuhler and Darrow (1992) on yield management at American.

### Part 29 · Rail, Trucks and Parcels (~54)
*Question:* why is one freight industry a set of regional monopolies and the next one a market of half a
million firms?
*Story:* the Staggers Act, October 1980, lets American railways set their own rates and drop their losing
lines; a bankrupt industry becomes one of the most profitable. Seven years earlier in Memphis, Frederick
Smith's fourteen aircraft carry 186 packages on the first night (verify).
*Unit:* a ton-mile; a load; a parcel; a stop. *Dollar:* the cost of moving a container inland by rail and by
truck; a parcel's dollar across pickup, linehaul, sort and the last mile.
2. The network's economics: density, length of haul, balance; the empty backhaul.
3. Railways: owning the track; the operating ratio; captive shippers and rate regulation; precision scheduled
   railroading and its critics.
4. Passenger rail: who pays for the track; Japan's privatization; Europe's separation of track and trains;
   China's high-speed network and its debt.
5. Trucking: no barrier to entry, an owner-operator at the margin; spot against contract; the cycle in
   capacity; brokers and their software.
6. Less-than-truckload: terminals make it a network business with a handful of players.
7. The integrators: hub and spoke for parcels; the air network; density at the door.
8. The last mile: the cost of a stop; the post office's universal service; a retailer building its own
   network (Part 32).
9. Warehouses and contract logistics; forwarders, who own nothing.
10. Labour: drivers, the Teamsters, contractors; automation.
11. India's freight corridors and China's express firms; Europe's fragmented road freight.
*The Works:* `freight.py`: a railway with density, a truckload carrier in a spot market, a parcel network with
a hub; laid beside two railways, a truckload carrier, an LTL carrier and two integrators.
*Run it:* price a lane with a full load out and nothing booked back.
*Map:* railways (Union Pacific, BNSF, CSX, Norfolk Southern, Canadian National, CPKC, Deutsche Bahn, JR East
and Central, China Railway, Indian Railways), parcels (UPS, FedEx, DHL, SF Express, ZTO, Yamato, Delhivery),
truckload and LTL (J.B. Hunt, Knight-Swift, Old Dominion), forwarders (Kuehne+Nagel, DSV), the posts.
*Called it?* forecasts of driverless trucks' arrival made in 2016–18.
*Sources:* the STB's R-1 reports and waybill sample summaries; the FMCSA's carrier census; filings (operating
ratio, yield per package); postal regulators.
*Borrowed:* *Economics, Built* Part 10 (Ramsey prices for captive shippers) and Part 15 (congestion).
*Reading:* Gallamore and Meyer, *American Railroads*; Keeler, *Railroads, Freight, and Public Policy*; Belzer,
*Sweatshops on Wheels*; Rose (1987) on trucking deregulation; Frock, *Changing How the World Does Business*.

### Part 30 · Telecoms (~55)
*Question:* why do the companies that carry everything capture so little of what it is worth?
*Story:* on 1 January 1984 the Bell System is broken into eight companies. In the spring of 2000 Britain
auctions five licences for third-generation mobile and raises £22.5 billion (verify); Germany raises more;
the buyers' share prices fall for two years. The pipe is essential, costly and hard to tell apart from the
next pipe.
*Unit:* a subscriber-month (revenue per user); a megahertz of spectrum per head of population; a gigabyte.
*Dollar:* a dollar of mobile bill → the network (spectrum, sites, radio equipment, backhaul, power) → handset
subsidy → sales and service → the operator's margin; and the tower company's dollar.
2. How a network works in one chapter: the cell, the spectrum band, the tower, backhaul, the core; fibre and
   cable to the home.
3. Spectrum: a licence to an invisible piece of land; how it is auctioned and valued.
4. The cost of coverage against the cost of capacity; a generation every ten years; capital spending as a
   fifth of revenue.
5. Subscribers: acquisition cost, churn, lifetime value; contracts, bundles, the family plan.
6. Three or four: the number of networks a market can carry; mergers and what regulators found about prices.
7. Towers: selling the mast and renting it back; co-location as pure margin; the tower company as a landlord.
8. Fixed lines: cable against fibre against wireless; the cost per home passed; overbuilding; universal
   service.
9. The pipe and what runs over it: messaging, voice and video taken by others; net neutrality.
10. Equipment: from a dozen makers to three; Huawei and the bans; open radio networks.
11. India's price war of 2016 and the consolidation to three; China's state operators; Europe's hundred
    operators; satellites in low orbit.
*The Works:* `telco.py`: a mobile operator with spectrum, sites, a subscriber base with churn, and a
generation upgrade; a tower company; laid beside operators in five regions and two tower companies.
*Run it:* a spectrum auction against three rivals, with a business case that depends on what they win.
*Map:* operators (Verizon, AT&T, T-Mobile, Comcast, Charter, Deutsche Telekom, Vodafone, Orange, Telefónica,
China Mobile, NTT, KDDI, SoftBank, SK Telecom, Reliance Jio, Bharti Airtel), towers (American Tower, Cellnex,
China Tower, Indus), equipment (Huawei, Ericsson, Nokia, Samsung), satellites (SpaceX's Starlink, SES).
*Called it?* the 3G business cases of 2000 against data revenue by 2005; the forecast in the README's story.
*Sources:* the FCC's competition reports and auction results; Ofcom; TRAI; the ITU; filings (revenue per
user, churn, capital spending).
*Borrowed:* *Economics, Built* Part 16 (`auctions`: spectrum, the exposure problem), Part 44 (platforms) and
Part 59 (`merger`).
*Reading:* Wu, *The Master Switch*; Klemperer (2002) and Binmore and Klemperer (2002) on the auctions;
Hausman on telecoms regulation; Genakos, Valletti and Verboven (2018) on mobile mergers; Crandall on the
breakup.

## Act VI · Selling and Serving

### Part 31 · Grocery and Mass Retail (~54)
*Question:* how does a business that keeps two pennies of every dollar become one of the largest on earth?
*Story:* Sam Walton in Bentonville flies his own aircraft over small towns to choose sites, and builds his
shops around a warehouse and not the other way round. In Germany the Albrecht brothers cut the range to a few
hundred items and take the phone numbers out of the directory to save on calls (verify).
*Unit:* a basket; a square foot of selling space; a stock turn. *Dollar:* a dollar at the till → cost of
goods (three-quarters) → store labour → rent → distribution → the 2–3% that is left.
2. The retailer's identity: margin × turns = return; negative working capital; the float on suppliers.
3. A store's model: sales per square foot, labour scheduling, shrink, the catchment.
4. Logistics as the product: distribution centres, cross-docking, the store within a day's drive; data shared
   with suppliers.
5. Buying power: what the largest customer gets; allowances; the supplier's dependence.
6. Own label: margin, leverage over brands, and the discounters' whole model.
7. Formats: supermarket, hypermarket, hard discounter, warehouse club (whose profit is roughly its membership
   fee), convenience, dollar stores.
8. Pricing: everyday low against high-low; loyalty cards and their data; loss leaders.
9. Density and entry: why discounters spread ring by ring; mergers and local markets.
10. Online grocery: who pays for picking and the last mile.
11. Europe's concentration; Japan's convenience stores; China's community buying; India's kiranas and the
    rules on foreign retailers.
*The Works:* `store.py`: a store with space, range, turns and a labour model; a distribution centre; a club
with a fee; laid beside a hypermarket chain, a supermarket chain, a club and a discounter.
*Run it:* a store for a year: range, price and staffing on a two per cent margin.
*Map:* Walmart, Costco, Kroger, Albertsons, Target, Aldi and Lidl (Schwarz), Tesco, Carrefour, Ahold Delhaize,
Seven & i, Aeon, CR Vanguard, Reliance Retail, DMart, Dollar General.
*Called it?* forecasts of online grocery share made in 2015 and in 2020.
*Sources:* filings (space, turns, payables days, membership income); the Census's retail series; the CMA's
and FTC's grocery merger decisions.
*Borrowed:* *Economics, Built* Part 60 (`revenue`: uniform pricing by chains, high-low) and Part 43.
*Reading:* Walton, *Made in America*; Basker (2007) and Holmes (2011) on Walmart; Jia (2008); Hausman and
Leibtag (2007); Brandes, *Bare Essentials*; Fisher and Raman.

### Part 32 · E-commerce (~56)
*Question:* is selling online a shop, a toll road or an advertising business?
*Story:* the 1997 letter to Amazon's shareholders says the company will be run for cash flow in the long
term and not for profit now. On one day in November each year Alibaba's platforms handle more sales than
many countries' retailers do in a quarter. The same word covers a shop that owns its stock and a market that
owns none.
*Unit:* an order; a dollar of merchandise value; the take rate. *Dollar:* a dollar spent on a marketplace →
the seller → the platform's commission, fulfilment fee and advertising fee (together a third or more, verify)
→ carriers and warehouses → payment fees.
2. Retailer against marketplace: who owns the stock, who sets the price, what is counted as revenue.
3. Fulfilment: the warehouse, picking, the last mile; cost per order against basket size; why speed is a
   fixed-cost game.
4. The marketplace as a two-sided business; the take rate and what bounds it.
5. Advertising inside the shop: sellers bid for placement; the most profitable line on the page.
6. The subscription that pays for shipping, and the cloud that paid for the losses (Part 37).
7. Private labels, copies and the antitrust cases; parity clauses.
8. China's models: the mall, the bazaar, group buying, the livestream; logistics built by the platforms.
9. Direct brands: the cost of acquiring a customer, and what happened when it rose.
10. Cross-border direct from factory; duty thresholds; returns.
11. India, Southeast Asia and Latin America; cash on delivery; quick commerce.
*The Works:* `marketplace.py`: a platform with sellers, buyers, a fulfilment network and an ad auction; a
direct brand with cohorts; laid beside four platforms' segment data and two direct brands.
*Run it:* set the take rate, the delivery promise and the ad load, and watch sellers and buyers respond.
*Map:* Amazon, Walmart online, Shopify, eBay, Alibaba, JD, PDD/Temu, Shein, Douyin's shop, MercadoLibre, Sea's
Shopee, Coupang, Rakuten, Flipkart, Meesho, Zalando.
*Called it?* e-commerce share forecasts made in 1999 and in 2020 against the Census's series.
*Sources:* the Census's e-commerce series; filings (segment results, fulfilment cost, seller-services
revenue); the FTC's 2023 complaint and European decisions.
*Borrowed:* *Economics, Built* Part 44 (two-sided platforms) and Part 61 (`platform`: sponsored slots, the
commission); this series' Part 38.
*Reading:* Stone, *The Everything Store*; Hagiu and Wright (2015) on marketplace or reseller; Khan (2017);
Clark, *Alibaba*; Brynjolfsson, Hu and Smith (2003).

### Part 33 · The Middlemen (~48)
*Question:* if the internet removes the middleman, why are the middlemen among the largest companies in every
country?
*Story:* Japan's trading houses, descended from the firms that handled the country's trade after 1868, deal in
everything from noodles to satellites on margins of a per cent or two. The three largest American drug
wholesalers each turn over more than most drug makers and keep about a penny on the dollar (verify).
*Unit:* a line item delivered; a turn of stock. *Dollar:* a dollar through a distributor: 98–99 cents to the
supplier; the rest pays for the warehouse, the trucks, credit and a sliver of profit.
2. What a wholesaler does: breaks bulk, holds stock, extends credit, delivers tomorrow; each priced.
3. Thin margin, high turn, high return: the arithmetic on a small capital base.
4. Scale and density in distribution; why three firms.
5. Drug wholesalers; food service distributors; electronics distributors; industrial supply.
6. Group purchasing and buying alliances.
7. The trading house: from commission agent to investor in mines and convenience stores.
8. Commodity traders (Parts 8–10): moving goods in space, time and form; financing; the scandals.
9. Disintermediation that happened and that did not: travel agents against drug wholesalers.
10. Hong Kong's sourcing agents; India's distributors and the stockist system.
*The Works:* `distributor.py`: a distributor with stock, receivables and delivery density; laid beside three
drug wholesalers, a food distributor, an industrial distributor and a trading house's segments.
*Run it:* hold the stock or drop-ship from the maker: service level against capital.
*Map:* McKesson, Cencora, Cardinal Health, Sysco, US Foods, Arrow, Avnet, WPG, W.W. Grainger, Fastenal,
Mitsubishi Corp., Mitsui, Itochu, Sumitomo, Marubeni, Li & Fung, Sinopharm, Redington.
*Called it?* the "disintermediation" forecasts of the late 1990s, sector by sector.
*Sources:* the Census's wholesale trade survey; filings; the trading houses' integrated reports.
*Borrowed:* *Economics, Built* Part 25 (why intermediaries: search) and Part 14.
*Reading:* Spulber, *Market Microstructure: Intermediaries and the Theory of the Firm*; Rubinstein and
Wolinsky (1987); Yoshino and Lifson, *The Invisible Link*; Blas and Farchy, *The World for Sale*.

### Part 34 · Restaurants and Franchising (~50)
*Question:* who actually owns a fast-food restaurant, and who is making the money?
*Story:* Ray Kroc is losing money on a 1.9% royalty until Harry Sonneborn tells him in 1956 that he is not in
the hamburger business; he is in the property business (verify). The company leases the land, sublets it to
the franchisee and collects a rent tied to sales.
*Unit:* a store; a ticket. *Dollar:* a dollar of burger → food and paper (about 30%) → labour (about 30%) →
rent → royalty and advertising fund → delivery commission → the operator's profit.
2. The economics of one restaurant: sales per week, prime cost, the four-wall margin, the payback on a new
   unit.
3. The franchise contract: royalty, advertising fund, territory, term; who invests and who bears the risk.
4. Why franchise at all: capital, effort and local knowledge; company-owned against franchised.
5. The property layer; the asset-light franchisor and its multiple.
6. The system: supply chain, menu engineering, the drive-through's seconds.
7. Labour: wages as a third of sales; minimum wages; the joint-employer question.
8. Delivery platforms: a 15–30% commission on a business with a 15% margin; ghost kitchens.
9. Full service against quick service against coffee; alcohol; the independent's failure rate.
10. Master franchisees abroad: Yum China, Jollibee, Jubilant in India.
*The Works:* `franchise.py`: a store with a daily demand curve and a labour schedule; a franchisor collecting
royalty and rent from a growing system; laid beside two franchisors, a company-owned chain and a large
franchisee.
*Run it:* open a store as a franchisee; then switch sides and set the royalty.
*Map:* McDonald's, Yum, Restaurant Brands, Starbucks, Chipotle, Darden, Domino's, Yum China, Luckin, Haidilao,
Jubilant FoodWorks, Jollibee, Compass and Sodexo (contract catering), DoorDash, Meituan, Zomato.
*Called it?* delivery platforms' own forecasts of profitability.
*Sources:* franchise disclosure documents (unit economics as filed); filings; the BLS on wages.
*Borrowed:* *Economics, Built* Part 14 (`contracts`: sharecropping, incentives) and Part 38 (monopsony and
minimum wages).
*Reading:* Lafontaine and Shaw (1999, 2005); Blair and Lafontaine, *The Economics of Franchising*; Love,
*McDonald's: Behind the Arches*; Kalnins and Lafontaine (2004).

### Part 35 · Travel and Hotels (~50)
*Question:* why do the biggest hotel companies own almost no hotels?
*Story:* in 1993 Marriott splits itself in two: one company keeps the buildings and the debt, the other keeps
the name and the contracts (verify). The second is worth more. A hotel is three businesses in one building:
a property, a brand and an operation.
*Unit:* a room-night; revenue per available room. *Dollar:* a dollar of room rate → the online agent's
commission → the brand's fees → the operator → labour, energy, tax → the owner's debt and return.
2. Occupancy × rate; the fixed building and the perishable night; flow-through.
3. Owner, brand, operator: the franchise and management contracts and their fees.
4. Why the brand is worth it: the reservation system and the loyalty scheme against the commission.
5. Online travel agents: merchant and agency models; parity clauses; the duopoly and the metasearch layer.
6. Short-term rentals: a platform on other people's homes; cities' rules.
7. Revenue management outside the airline (Part 28).
8. Cruise lines: a hotel that moves, sold full, earning on board.
9. Casinos: the hold, the high roller, Macau and Las Vegas, online betting and its regulation.
10. Theme parks: the gate against in-park spending; capital cycles.
11. Tour operators and packages; China's outbound and domestic travel; India's budget chains.
*The Works:* `hotel.py`: a hotel with seasonal demand, a brand contract and channels with different costs;
laid beside two asset-light brands, a hotel REIT, an online agent and a cruise line.
*Run it:* fill a hotel for a season: rate, channel mix and loyalty discounts.
*Map:* Marriott, Hilton, IHG, Accor, Hyatt, Jin Jiang, H World, Indian Hotels, OYO, Host Hotels, Booking,
Expedia, Trip.com, Airbnb, MakeMyTrip, Carnival, Royal Caribbean, Las Vegas Sands, Galaxy, Flutter, Disney's
parks, Oriental Land.
*Called it?* forecasts in 2020 of when travel would recover.
*Sources:* filings (rooms by contract type, fee rates, RevPAR); the gaming regulators' revenue reports; the
competition cases on parity clauses.
*Borrowed:* *Economics, Built* Part 60 (`revenue`) and Part 44.
*Reading:* deRoos (2010) on management agreements; Kosová, Lafontaine and Perrigot (2013); Schwartz, *Roll
the Bones*; Hunold et al. (2018) on parity clauses; Farronato and Fradkin (2022) on Airbnb.

## Act VII · Information

### Part 36 · Software (~58)
*Question:* what is a business worth when the second copy costs nothing?
*Story:* in February 1976 Bill Gates, twenty years old, writes an open letter to hobbyists who are copying his
BASIC: who can afford to do professional work for nothing? In 1999 a company in a San Francisco flat starts
renting software over the internet with a logo that crosses out the word.
*Unit:* a seat or a unit of use; a dollar of annual recurring revenue. *Dollar:* a dollar of subscription →
hosting (the gross margin is 70–80%) → sales and marketing (often the largest cost) → engineering → stock pay
→ what is left.
2. Cost structure: all fixed, all up front; gross margin and what "cost of revenue" contains.
3. Licence to subscription: the revenue moves from now to later; the J-curve; bookings, billings, deferred
   revenue.
4. Cohorts: gross and net retention; expansion; a customer's lifetime value against the cost of winning it;
   payback.
5. Selling it: self-serve, inside sales, the field; the "rule of forty"; why sales costs do not fall.
6. Switching costs: data, integrations, training; the system of record.
7. Platforms and ecosystems: operating systems, app stores, developers; bundling (Office, Teams).
8. Open source: free code as a strategy; the companies built on it; the clouds that host it.
9. The stack: infrastructure, databases, middleware, applications, security; horizontal and vertical.
10. Enterprise against consumer; games and ads are their own parts.
11. Consolidation: private equity's playbook for software (Part 47); pricing by seat when the seats are
    agents (Part 42).
12. Europe's one giant; China's weak enterprise market; India's products against its services (Part 54).
*The Works:* `saas.py`: a subscription company as cohorts with churn, expansion, a sales force with ramp and
quota, and deferred revenue; laid beside six companies at different scales.
*Run it:* a fixed budget for three years: sales or product, and when to raise the price.
*Map:* Microsoft, Oracle, SAP, Salesforce, Adobe, ServiceNow, Workday, Intuit, Snowflake, Databricks,
Atlassian, Palo Alto Networks, CrowdStrike, Dassault, Kingdee, Zoho, Freshworks, Constellation Software.
*Called it?* "software is eating the world" (2011) scored by sector; forecasts of on-premises decline.
*Sources:* filings (retention where disclosed, remaining performance obligations, sales cost); S-1s for
cohort data.
*Borrowed:* *Economics, Built* Part 44 (lock-in, platforms) and Part 10 (bundling, versioning).
*Reading:* Shapiro and Varian, *Information Rules*; Cusumano, *The Business of Software*; Campbell-Kelly,
*From Airline Reservations to Sonic the Hedgehog*; Lerner and Tirole (2002) on open source.

### Part 37 · Cloud and Data Centres (~54)
*Question:* how did renting computers become one of the most profitable businesses ever built, and what does
it run on?
*Story:* on 14 March 2006 Amazon opens a storage service that charges 15 cents a gigabyte a month, with no
contract (verify). Nine years later it reports the business's profit for the first time and analysts find it
is most of the company's.
*Unit:* a server-hour; a kilowatt of critical load; a rack. *Dollar:* a dollar of cloud revenue → servers and
chips (depreciation) → the building → power → network → engineering and sales → margin; a colocation
landlord's dollar.
2. A data hall: land, shell, power, cooling, racks; cost per megawatt; efficiency measured as PUE.
3. The server: its life, its depreciation, and what a change in assumed life does to profit.
4. Utilization: pooling many customers' peaks; virtualization; why the big get cheaper.
5. Pricing: on demand, reserved, spot; committed spend; the charge for taking data out.
6. Three layers of service, and where the margin rises: infrastructure, platforms, managed software.
7. Three hyperscalers and the rest: capital spending as the barrier; the fight for enterprise accounts.
8. Colocation and wholesale: the data centre as property (Part 26); interconnection as a network effect.
9. Networks: submarine cables, content delivery, the edge.
10. Power: the binding constraint; siting, grid queues, long-term contracts, nuclear deals (Part 13).
11. Accelerated computing: racks at ten times the power; whose chips (Parts 15 and 42).
12. Sovereignty: China's separate clouds; Europe's rules; India's data-centre build.
*The Works:* `cloud.py`: a region with capacity built ahead of demand, a pricing menu and utilization; a
colocation hall with leases; laid beside the three hyperscalers' segment data and two data-centre landlords.
*Run it:* build capacity a year ahead: too little and customers leave, too much and it depreciates empty.
*Map:* Amazon Web Services, Microsoft Azure, Google Cloud, Oracle, Alibaba Cloud, Huawei Cloud, Tencent Cloud,
Equinix, Digital Realty, NTT, CoreWeave, Cloudflare, Akamai, server makers (Dell, Supermicro, Quanta), power
and cooling (Vertiv, Schneider).
*Called it?* forecasts of data-centre electricity use made in 2007 and in 2020 against the meters.
*Sources:* filings (segment margin, capital spending, useful-life changes); utilities' load filings;
published price lists over time; Uptime Institute's public surveys.
*Borrowed:* this series' Part 4; *Economics, Built* Part 10 (menus) and Part 44.
*Reading:* Barroso, Hölzle and Ranganathan, *The Datacenter as a Computer*; Greenstein, *How the Internet
Became Commercial*; Masanet et al. (2020) on data-centre energy; Byrne, Corrado and Sichel (2018) on cloud
prices.

### Part 38 · Advertising (~56)
*Question:* how does attention get a price, and who collects it?
*Story:* in February 1998 a search engine called GoTo starts selling the top of its results to the highest
bidder, a cent at a time (verify). For a century before, an agency had bought space and kept 15%. Two
companies now collect something like half of the world's digital advertising (verify).
*Unit:* a thousand impressions; a click; a conversion. *Dollar:* an advertiser's dollar → agency → buying
platform → exchange → selling platform → publisher; the "ad tech tax"; and the dollar that goes straight to a
walled garden.
2. Why firms advertise, and what a firm will pay for a customer.
3. The old model: reach, frequency, ratings, the upfront, the agency's commission.
4. Search: intent, the auction (generalized second price), quality scores, the reserve.
5. Social and video: the feed as inventory; ad load; targeting by behaviour; the auction for an impression.
6. The open web: the stack between advertiser and publisher; who takes what; the 2023–25 cases.
7. Measurement: last click, lift, experiments; how much advertising works at all.
8. Privacy: cookies, the 2021 change to phone tracking and its cost; GDPR.
9. Retail media: the shop as an ad network (Part 32).
10. Agencies: from commission to fees; the holding companies; in-housing.
11. What it did to those who used to live on it: newspapers (Part 60), television (Part 39).
12. China's platforms; India's cheap data and ad market; outdoor and radio.
*The Works:* `ads.py`: a publisher with inventory, a quality-scored auction with a reserve, advertisers with
values; an intermediary chain with fees; laid beside two platforms, a publisher and an agency group.
*Run it:* you are the publisher: set ad load and the reserve, and watch users and revenue.
*Map:* Alphabet, Meta, Amazon's ads, Microsoft, ByteDance (TikTok, Douyin), Tencent, Baidu, The Trade Desk,
AppLovin, agencies (WPP, Publicis, Omnicom, Dentsu), outdoor (JCDecaux), measurement (Nielsen).
*Called it?* forecasts of the damage from the 2021 privacy change; "half my advertising is wasted" tested.
*Sources:* filings; the CMA's 2020 market study; the ACCC's inquiry; trial records of the search and ad-tech
cases; advertisers' experiments as published.
*Borrowed:* *Economics, Built* Part 16 (`auctions`: generalized second price) and Part 61 (`platform`: search
ads by attribution, regression and experiment; Lewis and Rao).
*Reading:* Edelman, Ostrovsky and Schwarz (2007); Varian (2007); Blake, Nosko and Tadelis (2015); Lewis and
Rao (2015); Auletta, *Googled*; Hwang, *Subprime Attention Crisis*.

### Part 39 · Media and Streaming (~56)
*Question:* why did the most profitable arrangement in entertainment collapse, and has what replaced it ever
paid?
*Story:* on 1 February 2013 a DVD-rental company releases thirteen episodes of *House of Cards* at once. The
cable bundle, which had sent a few dollars a month from nearly every American home to every channel whether
watched or not, starts to lose subscribers that year and has lost them every year since (verify).
*Unit:* a subscriber-month; an hour viewed; a title. *Dollar:* a dollar of cable bill → the distributor →
affiliate fees to channels → sports rights → studios and talent; and a dollar of streaming subscription.
2. Content as a fixed cost with uncertain demand: nobody knows anything; the hit pays for the slate.
3. Windows: cinema, home video, pay television, free television; the same film sold five times.
4. The bundle: why selling channels together raised revenue; who paid for sport.
5. The studio's accounts: capitalizing a film and amortizing it against forecast revenue; participations.
6. Streaming: one global window; subscriber acquisition, churn, content spend; the scale needed; the return
   of advertising and of bundles.
7. Sports rights: the last thing watched live; what leagues extract (Part 55).
8. Cinema: the split of the box office; the exhibitor's popcorn.
9. News: advertising gone, subscriptions for a few; the local paper (Part 60).
10. Television stations, retransmission fees; public broadcasters and the licence fee.
11. Talent and guilds: residuals, the strikes of 2023.
12. Bollywood and the south Indian industries; China's box office and quota; Korea's exports; Japan's anime.
*The Works:* `studio.py`: a slate of titles with skewed returns, windows and amortization; a streamer with
cohorts and content spend; laid beside three media groups, a streamer and an exhibitor.
*Run it:* green-light a slate of ten from thirty pitches with a fixed budget.
*Map:* Netflix, Disney, Comcast/NBCUniversal, Warner Bros. Discovery, Paramount, Sony, Amazon and Apple's
video, YouTube, Charter, Fox, News Corp, the New York Times, Tencent Video, iQiyi, Reliance–Disney's JioStar,
Zee, CJ ENM, Toho, the BBC.
*Called it?* cord-cutting forecasts of 2012; streaming subscriber forecasts of 2020–21.
*Sources:* filings (subscribers, content assets and amortization); the FCC's video competition reports; box
office data; the guilds' contracts.
*Borrowed:* *Economics, Built* Part 10 (bundling) and Part 60 (large bundles).
*Reading:* De Vany, *Hollywood Economics*; Caves, *Creative Industries*; Vogel, *Entertainment Industry
Economics*; Crawford and Yurukoglu (2012) on bundling; Epstein, *The Big Picture*.

### Part 40 · Video Games (~50)
*Question:* how did games come to out-earn films and music together, and who takes the 30%?
*Story:* after the American games market collapses in 1983, Nintendo launches a console in 1985 with a chip
that will not run a cartridge it has not approved, and a gold seal on the box. The platform owner decides what
is sold and takes a fee on each copy. The fee is still there.
*Unit:* a copy; a monthly active user; revenue per paying user. *Dollar:* a dollar spent on a game → the
store or platform (about 30%) → publisher → developer → engine licence → marketing.
2. The console: hardware at or below cost, the royalty on software; generations and resets.
3. The two-sided problem: players want games and developers want players; exclusives.
4. A big game's budget and the hit distribution; sequels as risk management.
5. Publishers and developers: advances, milestones, royalties; crunch and layoffs.
6. Live services: a game as a subscription that never ends; battle passes; the few games that hold most of
   the hours.
7. Free to play: a few per cent of players pay; whales; loot boxes and their regulation.
8. Mobile: the two app stores and their fee; the court cases; user acquisition as arbitrage.
9. PC: one dominant store; engines and their licences.
10. Subscriptions and the cloud; consolidation and the largest acquisition in the industry's history.
11. China: licences, playtime limits, Tencent and NetEase; Japan's and Korea's publishers; India's mobile
    players and the real-money gaming ban.
12. Esports, streaming and user-made games.
*The Works:* `console.py`: a platform choosing hardware price and fee, with developers and players entering;
a studio with a hit-driven slate; laid beside three platform holders and four publishers.
*Run it:* launch a console: the hardware subsidy and the fee, against a rival.
*Map:* Sony, Microsoft, Nintendo, Valve, Tencent, NetEase, Electronic Arts, Take-Two, Ubisoft, Roblox, Epic,
Unity, miHoYo, Nexon, Krafton, Square Enix, Capcom, Embracer, Apple's and Google's stores.
*Called it?* forecasts for virtual reality in 2016 and for cloud gaming in 2019.
*Sources:* filings (hardware and software units, engagement); the *Epic v. Apple* record; the CMA's decision
on Microsoft and Activision.
*Borrowed:* *Economics, Built* Part 44 (Armstrong's platform) and Part 45 (behavioural pricing).
*Reading:* Rochet and Tirole (2003); Lee (2013) on exclusives; Sheff, *Game Over*; Schreier, *Blood, Sweat,
and Pixels*; Hagiu on platform pricing.

### Part 41 · Music, Books and Creators (~52)
*Question:* when a song is played, who is paid, and how much?
*Story:* in June 1999 a student's file-sharing program reaches the internet; American recorded music revenue
falls by half over the next fifteen years and then climbs back on subscriptions (verify). A stream is worth a
fraction of a cent, divided among people most listeners have never heard of.
*Unit:* a stream; a copyright; a ticket. *Dollar:* a dollar of streaming subscription → the service (about
30%) → the recording's owner → the artist's royalty; → the song's publishers and writers; and a concert
ticket's dollar.
2. Two copyrights in every track: the recording and the song; who owns each.
3. The label: an investor in artists; advances, recoupment, the royalty; three majors.
4. The streaming pool: revenue shared in proportion to streams; what that does to niche artists; alternatives.
5. Publishing and the collecting societies; rates set by tribunals.
6. Catalogues as assets: an annuity bought with debt; the boom of 2020–21.
7. Live music: the tour's economics; promoter, venue and ticket seller in one company; resale.
8. Books: the publisher's list, advances, returns; one dominant retailer; audiobooks; academic publishing's
   margins.
9. Creators: platforms' revenue shares, sponsorship, subscriptions; the long tail's actual shape.
10. Generated music and text, and the cases over training data (Part 42).
11. K-pop's agencies; India's film music; China's licensing.
*The Works:* `catalogue.py`: a catalogue with decay curves and royalty splits; a streaming pool; a tour; laid
beside the three majors, a streaming service, a live company and a publisher.
*Run it:* split a month's streaming revenue among labels, publishers and artists under two rules.
*Map:* Universal Music, Sony Music, Warner Music, Spotify, Apple Music, Tencent Music, YouTube, Live Nation,
CTS Eventim, HYBE, Penguin Random House, Hachette, Amazon's books, RELX and Springer Nature, Patreon,
Substack.
*Called it?* forecasts in 2010 that recorded music would never recover.
*Sources:* the RIAA's and IFPI's revenue series; filings; the Copyright Royalty Board's determinations; the
UK Parliament's 2021 streaming inquiry and the CMA's study.
*Borrowed:* *Music, Built* for what is being sold; *Economics, Built* Part 10 and Part 38 (superstars).
*Reading:* Krueger, *Rockonomics*; Rosen (1981); Waldfogel, *Digital Renaissance*; Witt, *How Music Got
Free*; Aguiar and Waldfogel (2018).

### Part 42 · Artificial Intelligence (~58)
*Question:* an industry spending hundreds of billions a year on machines: who is earning it back?
*Story:* in 2012 a network trained on two gaming graphics cards in a bedroom in Toronto wins an image
contest by a margin nobody expected. A decade later the maker of those cards is among the most valuable
companies on earth, and its largest customers are racing to spend more on its products than they earn from
what they build with them.
*Unit:* a million tokens; a GPU-hour; a gigawatt of capacity. *Dollar:* a dollar spent on an AI application
→ the application → the model provider → the cloud → the chip designer → the foundry and memory makers
(Parts 15 and 37 joined).
2. The stack: energy, chips, data centres, models, applications; where the money enters and where it stops.
3. Training: a fixed cost that has grown by orders of magnitude; what it buys; how long a model stays ahead.
4. Inference: a marginal cost that is not zero; price per token falling by an order of magnitude a year
   (verify); margins.
5. A lab's accounts: revenue, compute, people; the round-trip of investment and cloud spending.
6. The chip layer: one designer's share and margin; custom chips by the clouds; memory and packaging as
   bottlenecks.
7. Capital spending: what is being built, how it is financed, the useful life of an accelerator.
8. Open weights against closed; the price of the model as a complement to something else.
9. Distribution: subscriptions, the API, the assistant inside existing software; who owns the customer.
10. Data: licensing deals, the copyright cases.
11. Demand: where usage is measured (code, support, search) and what firms report.
12. America and China: export controls, domestic chips, cheap models; Europe, the Gulf and India.
*The Works:* `lab.py`: a model lab with a training budget, a serving cost per token, a price and a
depreciation schedule for its compute; laid beside the disclosed figures of labs, clouds and the chip maker.
*Run it:* price a model's API against its compute bill and a rival's cheaper model.
*Map:* Nvidia, AMD, Broadcom, TSMC, SK Hynix, Microsoft, Alphabet, Amazon, Meta, Oracle, OpenAI, Anthropic,
xAI, Mistral, DeepSeek, Alibaba, ByteDance, Baidu, Huawei, CoreWeave, application companies by segment.
*Called it?* a set of dated forecasts of AI revenue and capital spending; the series logs its own for scoring.
*Sources:* filings (capital spending, segment growth, purchase commitments); published API price lists over
time; disclosed funding terms; export-control rules; court filings.
*Borrowed:* *AI, Built* for what a model is; *Economics, Built* Part 65 (`automation`: a free-entry toy of
frontier models, Hulten's arithmetic for AI).
*Reading:* chosen at the sweep, since the literature dates within months; Korinek and Vipra (2024) on market
structure; the chip makers' and clouds' filings as the primary texts.

## Act VIII · Money

### Part 43 · Banks (~58)
*Question:* what does a bank sell, and why can one that was profitable on Wednesday be gone by Friday?
*Story:* Walter Bagehot describes Lombard Street in 1873: a few people holding other people's money on a sliver
of their own. On 9 March 2023 customers of a bank in California ask for $42 billion in one day (verify). The
part builds a bank from a deposit and a loan and reads its accounts as those of a business.
*Unit:* a dollar of assets; the net interest margin; a dollar of equity. *Dollar:* a dollar of loan interest →
interest paid to depositors → expected credit losses → operating cost (branches, people, systems) → tax →
return on the equity behind the loan.
2. The balance sheet first: deposits, loans, securities, equity; ten or more of assets to one of equity.
3. The spread: what loans earn, what deposits cost; the deposit franchise and why cheap deposits are the
   moat; deposit betas when rates rise.
4. Credit: underwriting, expected and unexpected loss, provisions, the credit cycle; why losses arrive
   together.
5. Return on equity taken apart: margin, fees, cost-to-income, credit cost, leverage.
6. Interest rate risk: long assets, short liabilities; held-to-maturity securities; 2023.
7. Liquidity and runs; deposit insurance; the lender of last resort.
8. Capital rules: risk weights, Basel, stress tests; what they changed in returns since 2008.
9. The lines of business: retail and cards, mortgages, commercial lending, transaction banking, wealth.
10. Scale and scope: what technology costs; community banks, regionals, universals; consolidation.
11. Outside the bank: private credit and nonbanks (Part 47); fintech and banking as a service (Part 48).
12. China's state banks and directed lending; Europe's low returns; India's public and private banks and the
    bad-loan cycle; Japan's megabanks after decades of zero rates.
*The Works:* `bank.py`: a bank with a loan book by vintage, a deposit base with betas, a securities book,
capital and provisions through a simulated cycle; laid beside call-report data for banks of four sizes and
filings of banks in four regions.
*Run it:* grow the loan book through a boom, with the losses arriving three years later.
*Map:* JPMorgan Chase, Bank of America, Wells Fargo, Citigroup, the American regionals, HSBC, BNP Paribas,
Santander, UBS, ICBC, China Construction Bank, Agricultural Bank, Bank of China, MUFG, SMFG, HDFC Bank, State
Bank of India, ICICI, Royal Bank of Canada, Commonwealth Bank, DBS, Itaú.
*Called it?* banks' own stress scenarios before 2008 and before 2023.
*Sources:* the FDIC's call reports and Quarterly Banking Profile; the Federal Reserve's stress-test
disclosures; Pillar 3 reports; the EBA's transparency exercise; the RBI.
*Borrowed:* *Economics, Built* Part 26 (`bank`: runs, duration, capital, deposit betas) and Part 33
(`credit`); it does not rebuild them.
*Reading:* Bagehot, *Lombard Street*; Admati and Hellwig, *The Bankers' New Clothes*; Drechsler, Savov and
Schnabl (2017, 2021) on the deposit franchise; Berger and Bouwman, *Bank Liquidity Creation*; Gorton,
*Slapped by the Invisible Hand*.

### Part 44 · Investment Banks and Markets (~54)
*Question:* what are the fees for?
*Story:* on 1 May 1975 fixed commissions on the New York Stock Exchange end, and the partnerships that lived
on them have to find another business. They find several: trading for their own account, advising on
takeovers, and inventing securities. In 1999 the last of the big partnerships sells shares to the public.
*Unit:* a deal; a dollar of risk-weighted assets; a trade. *Dollar:* a dollar of underwriting fee → the
syndicate → the bankers' pay (about half of revenue, in the old rule) → capital, technology and conduct
costs.
2. Three businesses under one roof: advice, underwriting, and making markets.
3. The underwriting fee: 7% on a small American listing, for decades; what the issuer gets for it; first-day
   pops.
4. Advice on mergers: the league table, the relationship, the boutique.
5. Making markets: quoting both sides, holding inventory, earning the spread; flow against position.
6. Fixed income, currencies and commodities against equities; derivatives; clearing.
7. Prime broking: lending cash and shares to funds; the margin call (Archegos, 2021).
8. The balance sheet after 2008: capital, the rule against proprietary trading, lower returns.
9. The firms that took the trading: electronic market makers (*Quant, Built* covers how).
10. Pay: the bonus pool, deferral, the partnership's ghost.
11. Research and conflicts of interest: the 2003 settlement; paying for research in Europe.
12. Europe's retreat; Japan's brokers; China's securities firms; Hong Kong, Singapore and Mumbai as
    listing venues.
*The Works:* `dealer.py`: a dealer quoting with inventory limits and a capital charge; a fee book of deals
with a cyclical pipeline; laid beside five banks' segment disclosures and two boutiques.
*Run it:* a client wants to sell a large block now: quote a price and manage what you are left holding.
*Map:* Goldman Sachs, Morgan Stanley, JPMorgan, Bank of America, Citigroup, Barclays, Deutsche Bank, UBS,
Nomura, CITIC Securities, CICC, Kotak, boutiques (Evercore, Lazard, Centerview), market makers (Citadel
Securities, Jane Street, Virtu).
*Called it?* a celebrated deal's projected synergies against the outcome (AOL and Time Warner, 2000).
*Sources:* filings (segment revenue, pay ratios, value at risk); the SEC's data on underwriting spreads;
public league-table summaries; the Federal Reserve's dealer statistics.
*Borrowed:* *Quant, Built* for market making and microstructure; *Economics, Built* Part 16 and Part 13.
*Reading:* Chen and Ritter (2000), "The Seven Percent Solution"; Morrison and Wilhelm, *Investment Banking:
Institutions, Politics, and Law*; Lewis, *Liar's Poker*; Duffie (2010) on dealer failure; Ellis, *The
Partnership*.

### Part 45 · Insurance (~56)
*Question:* how does a company that expects to pay out more than it takes in stay in business for three
centuries?
*Story:* a coffee house on Tower Street in the 1680s where a merchant passes round a slip and others write
their names under the risk (verify). In Omaha, three centuries on, an investor explains that his insurers'
real product is the money they hold between the premium and the claim.
*Unit:* a dollar of premium; the combined ratio; a dollar of float. *Dollar:* a dollar of motor premium →
claims (65–75 cents) → claims handling → commission → expenses → underwriting result; plus the investment
income on the float.
2. Pooling: independent risks and the law of large numbers; what is and is not insurable.
3. Pricing: frequency × severity, loadings, rating factors; adverse selection and moral hazard as they show
   up in a book.
4. Reserves: the claim not yet reported; the triangle; how a reserve is a forecast, and what its error does.
5. The combined ratio and the float; underwriting at a loss on purpose.
6. The underwriting cycle: capital, prices, the soft and hard market.
7. Distribution: agents, brokers, direct; commissions; the price-comparison site.
8. Lines: personal (motor, home), commercial, specialty, the long tail (asbestos).
9. Reinsurance and catastrophe: the layer, the model, catastrophe bonds; Andrew (1992) and Katrina (2005);
   climate and the retreat from some states.
10. Life insurance and annuities: a balance-sheet business; asset and liability matching; private equity's
    insurers (Part 47).
11. Regulation: solvency, state rate approval; mutuals against stock companies.
12. Lloyd's; Europe's composites; China's and India's state life insurers; Japan's postal insurer.
*The Works:* `insurer.py`: a book of policies with a loss distribution, a reserve triangle, float invested and
a capital constraint, through a pricing cycle; a reinsurance layer; laid beside statutory data for four
motor insurers, a reinsurer and a life insurer.
*Run it:* rivals are cutting prices. Keep your book or keep your price.
*Map:* Berkshire Hathaway (GEICO, reinsurance), Progressive, State Farm, Allstate, Chubb, AIG, Travelers,
Allianz, AXA, Zurich, Munich Re, Swiss Re, Lloyd's, Ping An, China Life, LIC of India, Tokio Marine, Nippon
Life, MetLife, Prudential, Athene, brokers (Marsh McLennan, Aon).
*Called it?* the catastrophe models' loss estimates before a major event against the claims.
*Sources:* NAIC statutory data; state rate filings; insurers' loss-development triangles as filed; Lloyd's
annual report; EIOPA.
*Borrowed:* *Economics, Built* Part 13 (`info`: Rothschild–Stiglitz, the positive-correlation test) and Part
7 (risk); *Statistics, Built* for the loss distributions.
*Reading:* Buffett's letters on float (as primary texts); Cummins and Weiss on the industry's structure;
Froot (2001) on catastrophe risk; Koijen and Yogo (2015); Bernstein, *Against the Gods*.

### Part 46 · Asset Management (~52)
*Question:* why does a business whose product can be had for almost nothing still earn margins of 30%?
*Story:* on 31 August 1976 John Bogle launches a fund that will buy every stock in an index and try to beat
nothing. It raises $11 million against a target of $150 million and is called un-American (verify). Fifty
years later index funds hold more American equities than active ones.
*Unit:* a dollar under management; a basis point of fee. *Dollar:* a dollar of fee → distribution (platforms
and advisers) → portfolio management → operations → the manager's margin.
2. The arithmetic: revenue = assets × fee; costs mostly fixed; the market does half the growing.
3. Active management's record: the average fund after fees; persistence; why money still pays for it.
4. Indexing: scale without limit; three firms; fees approaching zero and securities lending.
5. The ETF: a wrapper and its plumbing; the tax advantage in America.
6. Distribution is the moat: advisers, platforms, retirement plans, defaults.
7. Hedge funds: two and twenty in practice; capacity; the multi-manager platforms.
8. Institutional money: pensions, endowments, sovereign funds and their consultants.
9. Alternatives move in: private markets sold to individuals (Part 47).
10. Wealth management: charging on assets for advice; the private bank; robo-advisers.
11. The retirement systems that create the assets: America's 401(k), Australia's superannuation, Japan's
    GPIF, India's systematic plans, China's young fund industry.
12. Voting and ownership: three firms as the largest holder of most large companies.
*The Works:* `fund.py`: a fund family with flows that chase returns, a fee schedule and fixed costs; an index
provider's rival; laid beside six managers' filings and fund-level fee data.
*Run it:* an index rival halves its fee. Cut yours, or keep it and lose flows.
*Map:* BlackRock, Vanguard, State Street, Fidelity, Capital Group, T. Rowe Price, Amundi, UBS, Schroders,
Nomura AM, E Fund, SBI Funds, hedge funds (Bridgewater, Citadel, Millennium), wealth (Morgan Stanley, Charles
Schwab, St. James's Place).
*Called it?* Bogle's fund's reception in 1976; Buffett's ten-year bet against funds of hedge funds (2008–17).
*Sources:* the SEC's fund filings; the Investment Company Institute's fact book; published scorecards of
active against index; Form ADV.
*Borrowed:* *Quant, Built* (performance measurement, the Track Record).
*Reading:* Bogle, *Common Sense on Mutual Funds*; Sharpe (1991), "The Arithmetic of Active Management";
Fama and French (2010); Berk and Green (2004); Gennaioli, Shleifer and Vishny (2015), "Money Doctors";
French (2008) on the cost of active investing.

### Part 47 · Private Equity and Venture Capital (~56)
*Question:* how do you buy a company with its own money, and why does anyone let you?
*Story:* in the autumn of 1988 a firm with a few dozen employees bids $25 billion for the maker of Oreos and
Camels (verify) and wins. Thirty years earlier, a fund in Boston put $70,000 into a start-up called Digital
Equipment and turned it into several hundred million.
*Unit:* a fund; a deal; a multiple of money. *Dollar:* a dollar of fund return → the management fee → carried
interest → fees charged to the companies → the investors' net.
2. The buyout's arithmetic: price, debt, the three sources of return (growth, multiple, leverage); a model in
   ten rows.
3. The debt: senior, junior, covenants; who lends; what happens in a default.
4. The fund: commitments, drawdowns, ten years; 2 and 20, the hurdle, the catch-up.
5. Measuring returns: internal rates and their tricks; public-market equivalents; what the evidence says net
   of fees.
6. What they do to companies: the evidence on jobs, productivity, prices and bankruptcy.
7. Venture capital: the power law; stages; terms (preferences, anti-dilution); why most funds lose and a few
   return everything.
8. The start-up's side: dilution, the option pool, the down round.
9. Private credit: lending moved out of banks; who holds it; insurers as funding.
10. The firms themselves: fee earnings against carry; going public; permanent capital.
11. Exits: sales, listings, continuation funds; what happens when exits stop.
12. Growth equity and sovereign money; China's venture market and state funds; India's start-ups; SoftBank.
*The Works:* `buyout.py`: a leveraged buyout with a debt schedule and exit; a fund with a fee waterfall; a
venture portfolio drawn from a power law; laid beside listed managers' filings and pension funds' published
returns by fund.
*Run it:* structure a buyout: how much debt, what price, and survive a recession in year three.
*Map:* Blackstone, KKR, Apollo, Carlyle, Brookfield, EQT, CVC, Ares, Sequoia, Andreessen Horowitz, Accel,
Tiger Global, SoftBank Vision Fund, HongShan, Temasek, the large public pension investors.
*Called it?* the forecasts in the RJR bid documents against the result; a vintage of venture funds scored.
*Sources:* listed managers' filings; public pension funds' fund-level returns (CalPERS, CalSTRS, Oregon); the
SEC's Form PF aggregates; court records of the RJR deal.
*Borrowed:* *Economics, Built* Part 62 (`org`: buyouts against matched firms) and Part 14.
*Reading:* Kaplan and Strömberg (2009); Kaplan and Schoar (2005); Harris, Jenkinson and Kaplan (2014);
Phalippou, *Private Equity Laid Bare*; Burrough and Helyar, *Barbarians at the Gate*; Gompers and Lerner,
*The Venture Capital Cycle*.

### Part 48 · Payments (~54)
*Question:* when you tap a card, who is paid, and why is it so hard to compete with them?
*Story:* in September 1958 Bank of America mails 60,000 working credit cards to the residents of Fresno,
unasked (verify). Fraud and delinquency are ruinous, and the bank persists, because a card nobody holds is a
card no shop accepts.
*Unit:* a transaction; a dollar of payment volume; a basis point. *Dollar:* a $100 purchase: the merchant
receives about $97.50; of the rest, most goes to the bank that issued the card (and back to the cardholder as
rewards), a slice to the merchant's acquirer, and a thin slice to the network (verify by country).
2. The four parties: cardholder, issuer, merchant, acquirer; and the network between them.
3. Interchange: a price set by the network, paid by one bank to another; why it flows that way.
4. The chicken and the egg; rewards as the weapon; who pays for them.
5. The network: a few cents per transaction on nearly no capital; the highest margins in finance.
6. Acquirers and processors: a scale business; the new software-led processors; the terminal.
7. Regulation: Europe's cap, the Durbin amendment, Australia; what happened to fees and rewards.
8. Account-to-account: India's UPI (free to users, billions of transactions a month), Brazil's Pix, instant
   payments; China's two wallets.
9. Cross-border: correspondent banks, the fee on remittances, SWIFT; stablecoins as a rail.
10. Buy now, pay later: the merchant pays for the credit.
11. Wallets on phones: the fee for the tap.
12. Cash: who still uses it and what it costs.
*The Works:* `cards.py`: a card network with two sides, an interchange rate, issuers competing
on rewards and merchants choosing to accept; laid beside two networks, two acquirers, an issuer's card
segment and UPI's published volumes.
*Run it:* set interchange: too low and issuers leave, too high and merchants do.
*Map:* Visa, Mastercard, American Express, China UnionPay, JCB, issuers (JPMorgan, Capital One), acquirers and
processors (Fiserv, Global Payments, Adyen, Stripe, Block), wallets (PayPal, Apple Pay, Alipay, WeChat Pay,
PhonePe, Google Pay, Paytm), NPCI, Pix, remittances (Wise, Western Union), Klarna, Affirm.
*Called it?* forecasts of the "death of cash" by date; forecasts that mobile wallets would displace cards in
America.
*Sources:* the Federal Reserve's payments studies and interchange data; the networks' filings; NPCI's and
the Banco Central do Brasil's statistics; the European Commission's decisions; the 2024 American settlement
record.
*Borrowed:* *Economics, Built* Part 44 (two-sided platforms) and Part 25 (`money`).
*Reading:* Evans and Schmalensee, *Paying with Plastic*; Rochet and Tirole (2002, 2011); Nocera, *A Piece of
the Action*; Rysman and Wright (2014).

### Part 49 · The Toll Collectors (~50)
*Question:* who earns a fee every time finance moves, without lending or investing a dollar?
*Story:* John Moody publishes ratings of railway bonds in 1909, sold to investors by subscription. In the
1970s the agencies turn the model round: the issuer pays (verify). The businesses in this part sell a standard,
and a standard has one natural supplier.
*Unit:* a rated issue; a contract cleared; a licence. *Dollar:* a dollar of exchange revenue; a dollar of
index fee from an ETF; a dollar of rating fee: each mostly margin.
2. Exchanges: from members' clubs to listed companies; listing, trading, clearing, data; where the profit
   moved.
3. Clearing: the central counterparty, margin, the vertical silo; a default.
4. Market data: the feed nobody can trade without; the pricing disputes.
5. Index providers: a list of stocks licensed for a fee on assets; inclusion moves prices.
6. Rating agencies: issuer pays; three firms; 2008; the regulatory licence.
7. Credit bureaus and scores: data given free by lenders, sold back to them.
8. Terminals, analytics and benchmarks; LIBOR's end.
9. Custody and fund administration: scale and tiny fees on trillions.
10. Why these moats hold: standards, embedded workflows, regulation that names the product.
11. Exchanges in Hong Kong, Shanghai, Shenzhen, Mumbai, Tokyo; state ownership and competition.
*The Works:* `standard.py`: a benchmark with licensees and switching costs, pricing over time; an exchange
with trading, clearing and data lines; laid beside four exchanges, two rating agencies, an index provider and
a bureau.
*Run it:* raise the price of a data feed every year and find where customers finally leave.
*Map:* CME, ICE, Nasdaq, LSEG, Deutsche Börse, HKEX, NSE and BSE, Japan Exchange, S&P Global, Moody's, Fitch,
MSCI, FTSE Russell, Bloomberg, FactSet, Equifax, Experian, TransUnion, FICO, DTCC, BNY, State Street.
*Called it?* the ratings of 2006–07 mortgage securities against their defaults.
*Sources:* filings (segment margins); the SEC's reports on rating agencies and market data; the Financial
Crisis Inquiry Commission's record.
*Borrowed:* *Quant, Built* (exchanges and microstructure); *Economics, Built* Part 13 (certification).
*Reading:* White (2010) on the rating agencies; Budish, Lee and Shim (2024) on exchange competition;
Petry, Fichtner and Heemskerk (2021) on index providers; Duffie and Zhu (2011) on clearing.

## Act IX · People

### Part 50 · Hospitals and Doctors (~58)
*Question:* why does nobody know what a hospital stay costs, including the hospital?
*Story:* Dallas, 1929: Baylor University Hospital offers schoolteachers twenty-one days of care a year for
fifty cents a month (verify), to fill its beds in a depression. Payment for care is separated from the person
receiving it, and has been ever since.
*Unit:* an admission; a bed-day; a procedure; a relative value unit. *Dollar:* a dollar of hospital revenue →
nurses and other staff (over half) → supplies and drugs (Parts 20–21) → physicians → buildings and
equipment → administration and billing.
2. The triangle: patient, provider, payer; who decides, who receives, who pays.
3. How a hospital is paid: per day, per case (diagnosis groups, 1983), per service, per head; what each makes
   it do.
4. The price list nobody pays: charges, negotiated rates, Medicare's rates; the same scan at ten prices.
5. Payer mix as the business model: who subsidizes whom; the emergency room.
6. Costs: fixed capacity, staffing ratios, agency nurses; the length of stay.
7. Doctors: fee for service and the fee schedule; practices bought by hospitals, insurers and investors;
   training limits.
8. Mergers: prices after hospital consolidation; non-profit status.
9. Outside the hospital: surgery centres, urgent care, dialysis, nursing homes and home care.
10. Other systems: Britain's single provider, Germany's funds, Japan's fee schedule, Singapore's accounts;
    spending and outcomes compared.
11. India's private hospital chains and public insurance; China's public hospitals and drug procurement.
12. Labour: nurses, residents, shortages and pay.
*The Works:* `hospital.py`: a hospital with beds, a case mix, staffing and three payers at three price
levels; laid beside Medicare cost-report data for hospitals of four kinds and filings of listed operators.
*Run it:* a fixed payer mix and a rising wage bill: balance the budget without closing a service the town
needs.
*Map:* HCA, Tenet, CommonSpirit, Kaiser Permanente, Mayo Clinic, the NHS trusts, Helios (Fresenius), Ramsay,
Apollo Hospitals, Fortis, IHH, China's public hospitals, DaVita, physician groups, staffing firms.
*Called it?* the cost projections for Medicare at its founding in 1965 against the outcome.
*Sources:* CMS's National Health Expenditure accounts, hospital cost reports and price-transparency files;
the OECD's health statistics; the American Hospital Association's summary data.
*Borrowed:* *Economics, Built* Part 42 (`insurance`: Oregon, coinsurance) and Part 59 (a hospital merger).
*Reading:* Arrow (1963); Starr, *The Social Transformation of American Medicine*; Cooper, Craig, Gaynor and
Van Reenen (2019), "The Price Ain't Right?"; Gaynor, Ho and Town (2015); Cutler, *Your Money or Your Life*.

### Part 51 · Health Insurance and the Drug Channel (~56)
*Question:* where does the money go between the premium and the pill?
*Story:* a vial of insulin with a list price near $300 and a net price to its maker of perhaps a third of
that (verify): the difference passes through a wholesaler, a pharmacy, a benefit manager and an insurer, and
part of it comes back as a rebate that the patient at the counter never sees.
*Unit:* a member-month; the medical loss ratio; a prescription. *Dollar:* a dollar of premium → medical
claims (80–85 cents by law) → administration → margin; and a dollar of brand-drug list price through the
channel.
2. An insurer's income statement: premiums, claims, the loss ratio rule; a 3–5% margin on a huge base.
3. Underwriting and risk adjustment: selection after community rating; the incentive to code.
4. Managed care: networks, prior authorization, the negotiated rate; who has leverage in which city.
5. The employer: self-insured plans; the insurer as administrator.
6. Medicare Advantage and Medicaid managed care: government programmes run by private insurers.
7. The benefit manager: formularies, rebates, spread pricing, its own pharmacies; three firms.
8. Wholesalers (Part 33) and pharmacies: the chains' retreat; the independent pharmacy.
9. List against net, link by link; who gains from a high list price.
10. Vertical integration: the insurer that owns the benefit manager, the pharmacy and the doctors.
11. Single payers and regulated funds abroad; what administration costs in each system.
12. India's and China's public insurance schemes; out-of-pocket spending.
*The Works:* `healthplan.py`: a plan with members, a claims distribution, a network and a loss-ratio floor;
`rx.py`: a prescription through maker, wholesaler, benefit manager, pharmacy and plan; laid beside five
insurers' filings and the FTC's benefit-manager findings.
*Run it:* design a plan: premium, deductible and network width, with selection against you.
*Map:* UnitedHealth (and Optum), Elevance, CVS Health (Aetna, Caremark), Cigna (Express Scripts), Humana,
Centene, the Blue plans, Walgreens, the wholesalers of Part 33, Germany's statutory funds, Ping An Health, Star
Health, the NHS as a payer.
*Called it?* the Congressional Budget Office's 2010 projections of exchange enrolment against the outcome.
*Sources:* insurers' filings and statutory statements; CMS's loss-ratio and Medicare Advantage data; the FTC's
2024–25 interim reports on benefit managers; state drug-transparency reports.
*Borrowed:* *Economics, Built* Part 13 (`info`: the Einav–Finkelstein triangle, the death spiral), Part 42
and Part 58 (the budget office's record).
*Reading:* Einav and Finkelstein, *We've Got You Covered*; Cutler and Zeckhauser (2000); Geruso and Layton
(2020) on upcoding; Kakani, Chernew and Chandra (2020) on rebates; Feldman, *Drugs, Money, and Secret
Handshakes*.

### Part 52 · Education (~52)
*Question:* why does the price of a degree rise faster than almost anything else?
*Story:* at Bologna in the eleventh century the students hire the teachers and fine them for being late
(verify). In 1980 Howard Bowen states the rule that universities raise all the money they can and spend all
they raise. A university is a non-profit that sells a place in a queue.
*Unit:* a student-year; list price against net price; a research grant. *Dollar:* a dollar of tuition →
instruction (under a third at many, verify) → student services → administration → aid given back to other
students → buildings and debt.
2. A university's accounts: tuition, state funding, research grants, gifts, the endowment, the hospital, the
   stadium.
3. List and net: the discount rate; price discrimination by aid; merit aid as a bid for rankings.
4. Why costs rise: Baumol's string quartet; Bowen's rule; amenities; administrators; which the data support.
5. The top and the rest: selectivity as the product; why the best do not expand; enrolment cliffs and
   closures.
6. Who pays: states' retreat, student loans, income-contingent systems abroad.
7. Research: grants and their overhead; the doctoral labour force.
8. For-profit colleges: marketing spend, federal aid, outcomes, enforcement.
9. Schools: public systems, charters, private schools; textbooks and testing as oligopolies; tutoring.
10. Online education and the forecasts of 2012; boot camps; credentials.
11. International students as a business model (Britain, Australia, Canada); China's tutoring crackdown of
    2021; India's coaching towns and private universities.
12. Returns to a degree and signalling, briefly.
*The Works:* `university.py`: a university choosing list price, aid by student type, class size and
endowment spending, subject to a ranking; laid beside IPEDS data for five kinds of institution and two listed
education companies.
*Run it:* set tuition and aid for a class, and see who enrols.
*Map:* by type and country (the American tiers, Britain's Russell Group, Australia's Group of Eight, China's
Project 985 universities, India's IITs and private groups), companies (Pearson, McGraw Hill, Coursera,
Duolingo, New Oriental, TAL, PhysicsWallah), lenders and servicers.
*Called it?* "in fifty years there will be ten universities" (2012) and the MOOC forecasts.
*Sources:* IPEDS; the College Scorecard; the Delta Cost Project's series; NACUBO's discounting and endowment
studies; the OECD's *Education at a Glance*.
*Borrowed:* *Economics, Built* Part 13 (Spence), Part 38 (returns to schooling) and Part 49 (class size).
*Reading:* Bowen, *The Costs of Higher Education*; Baumol and Bowen (1966); Winston (1999), "Subsidies,
Hierarchy and Peers"; Archibald and Feldman, *Why Does College Cost So Much?*; Hoxby (2009) on selectivity;
Deming, Goldin and Katz (2012) on for-profits.

### Part 53 · Professional Services (~50)
*Question:* how does a firm with no assets but its staff make its partners rich?
*Story:* in the first years of the twentieth century Paul Cravath sets out how his law firm will run: hire
the best graduates, train them, pay them a salary, and after some years promote a few to partner and send the
rest away (verify). Law, audit and consulting firms have run that way since.
*Unit:* a billable hour; a partner; a fee-earner. *Dollar:* a dollar of fees → salaries of the staff who did
the work → offices and support → the partners' profit (a third or more at the top law firms, verify).
2. The three levers: leverage (staff per partner), utilization and rate; profit per partner as their product.
3. The pyramid and up-or-out: a tournament for partnership; what it does to juniors' hours.
4. Why partnerships: the product is judgment, the assets go home at night; why they rarely list.
5. Pricing: by the hour, by the project, by value, by the retainer; discounts and write-offs.
6. Law: the top of the market against the rest; lateral hiring; litigation finance.
7. Audit: four firms, a mandated product, liability, and the conflict with advice; Enron and Arthur
   Andersen, 2002; the splits proposed since.
8. Strategy consulting: what is sold; the alumni network; the public-sector work and its critics.
9. Engineers, architects, advertising agencies, executive search; investment banking's advice (Part 44).
10. What software does to the base of the pyramid.
11. India's rules on foreign law firms; China's local audit firms; the Big Four as networks, country by
    country.
*The Works:* `partnership.py`: a firm with a pyramid, promotion and attrition rates, utilization and rates,
and profit shared among partners; laid beside published law-firm financials, the Big Four's transparency
reports and listed consultancies.
*Run it:* staff a pyramid for five years: how many to hire, how many to promote.
*Map:* law (Kirkland & Ellis, Latham & Watkins, the Magic Circle, King & Wood Mallesons), audit (Deloitte,
PwC, EY, KPMG, BDO, Grant Thornton), consulting (McKinsey, BCG, Bain, Accenture, Booz Allen), search and
others.
*Called it?* forecasts of the Big Four's breakup; forecasts of automation in legal work.
*Sources:* the audit firms' transparency reports; published surveys of law-firm financials; listed
consultancies' filings; regulators' audit-quality reports.
*Borrowed:* *Economics, Built* Part 14 (`contracts`: tournaments, career concerns) and Part 62 (`org`:
knowledge hierarchies).
*Reading:* Maister, *Managing the Professional Service Firm*; Galanter and Palay, *Tournament of Lawyers*;
Levin and Tadelis (2005) on partnerships; Garicano and Hubbard (2007); Gow and Kells, *The Big Four*.

### Part 54 · Outsourcing and Staffing (~50)
*Question:* how did selling other people's hours across a border become a quarter-trillion-dollar industry?
*Story:* Bangalore in the 1990s: a satellite link, a time difference that turns the client's night into a
working day, and engineers at a tenth of the client's wage. The millennium bug gives the industry its first
flood of work, and it does not go back (verify).
*Unit:* a billed person-month; a seat; a placement. *Dollar:* a dollar of contract → the engineer's wage
(offshore and onsite) → the bench (unbilled staff) → sales and visas → a 20–25% margin (verify); a staffing
agency's dollar is nearly all wage.
2. The arbitrage: the wage gap, the billing rate, and how fast the gap closes.
3. The delivery model: onsite and offshore mix, the pyramid, utilization, attrition, campus hiring by the
   tens of thousands.
4. Contracts: time and materials against fixed price; managed services; renewals.
5. Moving up: from maintenance to consulting; what the margin says about how far.
6. Visas and politics: the H-1B and its lottery.
7. Business process outsourcing: call centres and back offices; the Philippines.
8. Global capability centres: clients building their own.
9. Staffing agencies: a spread on a wage; the cycle's first casualty; temporary work and the law.
10. Facilities, catering and security: thin margins, huge headcounts, contracts re-tendered every few years.
11. Gig platforms: the contractor question; pay, utilization and the take rate.
12. What generated code and automated service do to a business priced by headcount.
*The Works:* `services.py`: an offshore firm with a pyramid, a bench, wage inflation and a contract mix; a
staffing agency through a cycle; laid beside five Indian firms' filings, two global ones and two staffing
agencies.
*Run it:* bid a fixed-price contract whose scope you only half understand.
*Map:* TCS, Infosys, HCLTech, Wipro, Cognizant, Accenture, Capgemini, IBM's services, Genpact, Concentrix,
Teleperformance, Randstad, Adecco, Recruit, ManpowerGroup, Compass, ISS, Uber and DoorDash as labour
platforms, Upwork.
*Called it?* Blinder's 2007 estimate of offshorable jobs against what moved.
*Sources:* filings (headcount, utilization, attrition, revenue by geography); NASSCOM's public summaries;
USCIS's H-1B data; the BLS on temporary help.
*Borrowed:* *Economics, Built* Part 35 (comparative advantage), Part 39 (tasks) and Part 65 (`automation`).
*Reading:* Arora and Gambardella (eds), *From Underdogs to Tigers*; Blinder (2006, 2009); Autor (2003) on
temporary help; Dossani and Kenney (2007); Weil, *The Fissured Workplace*.

### Part 55 · Sports and Live Entertainment (~50)
*Question:* why are sports teams run as a cartel, and why is that legal?
*Story:* in 1961 Pete Rozelle persuades the owners of the National Football League to sell their television
rights as one and split the money equally, and persuades Congress to exempt the arrangement from the antitrust
laws (verify). The smallest city in the league has kept its team ever since.
*Unit:* a game; a seat; a season of rights. *Dollar:* a dollar of league revenue → media rights, gate and
sponsorship in → players (about half, by agreement) → clubs → owners; a club's dollar in a European league.
2. The peculiar economics: a team needs its rivals; competitive balance as a product.
3. Media rights: the last appointment television; cycles of bidding; what happens when a broadcaster cannot
   pay.
4. Sharing revenue, salary caps, the draft: restraints agreed among competitors, and with the union.
5. Closed leagues against promotion and relegation: franchise values against the arms race; why European
   clubs lose money and American ones do not.
6. Players: free agency (1975, and Bosman, 1995), agents, guaranteed contracts, the superstar's share.
7. Stadiums: public subsidies and the evidence on them.
8. Franchise values: scarcity, trophy assets, private equity and sovereign owners.
9. College sport: an unpaid labour force until the 2020s.
10. Cricket's Indian Premier League: an auction for teams, players and rights; the fastest-grown league.
11. Global events: the Olympics' costs, the World Cup; betting's return (Part 35).
12. Live entertainment beside it: arenas, tours and tickets (Part 41).
*The Works:* `league.py`: a league of clubs with unequal markets under revenue sharing, a cap and a draft, or
under relegation; win probabilities and finances; laid beside the Green Bay Packers' accounts, listed clubs
and the leagues' published figures.
*Run it:* as commissioner, split the television money and set the cap; watch balance and club profits.
*Map:* NFL, NBA, MLB, the Premier League, La Liga, the Bundesliga, UEFA, the IPL, Formula One, the UFC and
WWE (TKO), listed clubs (Manchester United, Borussia Dortmund, Juventus), owners' groups, broadcasters and
streamers as buyers.
*Called it?* stadium economic-impact studies against the measured effects.
*Sources:* the Packers' annual report; listed clubs' filings; UEFA's and Deloitte's public club reports; the
leagues' collective agreements; court records.
*Borrowed:* *Economics, Built* Part 12 (cartels), Part 38 (superstars) and Part 16 (the IPL's auctions).
*Reading:* Rottenberg (1956); Neale (1964); Szymanski, *Money and Football* and (2003) on league design;
Fort and Quirk (1995); Coates and Humphreys (2008) on stadium subsidies; Zimbalist, *Circus Maximus*.

## Act X · Systems

### Part 56 · The Energy Transition (~58)
*Question:* what does it cost to rebuild the energy system, and who is making the equipment?
*Story:* the price of a solar module falls by about a fifth every time the world's output doubles, for forty
years (verify; the rule is named after Richard Swanson). Forecasters who knew the rule kept forecasting that
it would stop. The part reads Parts 8, 9, 13, 15 and 17 as one system.
*Unit:* a dollar per watt; a dollar per kilowatt-hour of battery; a tonne of carbon avoided. *Dollar:* a
dollar of solar farm → modules → cells → wafers → polysilicon; and installation, land, grid connection and
the cost of capital.
1. Run it: a subsidy budget to split among five technologies at different points on their curves.
2. Learning curves, measured: solar, wind, batteries, electrolysers; which technologies learn and which
   (nuclear) have not.
3. The cost of capital as the largest input: why the same solar farm costs twice as much in one country as
   in another.
4. Solar's chain, stage by stage: who makes what; overcapacity and margins near zero.
5. Wind: turbines that grew; the makers' losses in 2022–23; offshore auctions with no bidders.
6. Batteries: chemistry, the cell factory, the price per kilowatt-hour; the chain from lithium (Part 9) to
   the pack.
7. The electric car as demand for all of it (Part 17); charging networks.
8. The grid: intermittency, storage, transmission; the system cost that the levelized cost leaves out
   (Part 13).
9. Hard cases: steel and cement (Part 11), heat, aviation and shipping; hydrogen's arithmetic.
10. Nuclear: costs that rose; the countries that built cheaply; small reactors.
11. Policy as industry: feed-in tariffs, the Inflation Reduction Act, China's five-year plans, Europe's
    carbon price and border adjustment; India's auctions.
12. The oil companies' side (Part 8): demand forecasts and capital discipline.
*The Works:* `transition.py`: technologies on learning curves with deployment, a cost of capital and a
subsidy; a power system (Part 13's) with rising renewable share; laid beside module, turbine and cell makers'
filings.
*Map:* solar (LONGi, Jinko, Tongwei, First Solar), wind (Vestas, Siemens Gamesa, Goldwind, GE Vernova),
batteries (CATL, BYD, LG Energy Solution, Panasonic), developers (NextEra, Ørsted, Adani Green), electrolysers
and nuclear vendors, grid equipment (Hitachi Energy, Siemens Energy).
*Called it?* the IEA's solar forecasts, year by year, against installations.
*Sources:* IRENA's cost database; national auction results; the EIA's and IEA's outlooks and their
retrospectives; makers' filings.
*Borrowed:* *Economics, Built* Part 48 (`climate`: Wright's law, directed technical change) and Part 66.
*Reading:* Way, Ives, Mealy and Farmer (2022); Nemet, *How Solar Energy Became Cheap*; Lovering, Yip and
Nordhaus (2016) on nuclear costs; Smil, *Energy Transitions*; Acemoglu, Aghion, Bursztyn and Hemous (2012).

### Part 57 · Chokepoints (~55)
*Question:* which single factories does the world economy depend on?
*Story:* on 31 March 2012 an explosion at a chemical plant in Marl, Germany, stops production of a resin
that goes into the fuel lines of most of the world's cars; the car makers discover within days that they all
buy it, at three removes, from the same place (verify). The part joins the Works' model companies into one web
and pulls links out.
*Unit:* a link; days of inventory; a share of world supply. *Dollar:* a product's dollar by country and by
stage, with the stages where one country or one firm has most of the supply marked.
1. Run it: a chain of six stages. Find the link whose loss stops the most output.
2. Chains as networks: tiers, visibility (firms rarely know their suppliers' suppliers), substitutability.
3. Concentration by stage: the series' Maps re-read along the chain: lithography, advanced logic, rare-earth
   processing, pharmaceutical ingredients, solar wafers, neon, helium.
4. Why chokepoints form: scale and learning (Part 4), clusters, and nobody paying for the second source.
5. Inventory against resilience: lean production's hidden bet (Part 17); the chip shortage of 2021 in cars.
6. Shocks traced: the 2011 earthquake and floods, 2020–21, the Suez blockage, the Red Sea.
7. Chokepoints as weapons: export controls, entity lists, the 2010 rare-earth episode, gas in 2022.
8. What firms did: dual sourcing, stockpiles, nearshoring; what it cost; what the trade data show.
9. What states did: subsidies, stockpiles, friend-shoring; the bill.
10. Private against social resilience: who should pay for the spare capacity.
*The Works:* `world.py` completed: every model company linked by its inputs; shocks propagated downstream and
upstream; laid beside trade data by product and the disclosed supplier lists.
*Map:* the chokepoint table: stage, product, leading firm or country, share, source, as of.
*Called it?* forecasts of reshoring made in 2020–22 against trade and investment data.
*Sources:* UN Comtrade by product; the OECD's chain data; USGS on processing shares; companies' supplier
lists; the export-control rules.
*Borrowed:* *Economics, Built* Part 63 (`network`: an earthquake through a supply web, O-ring, fragility) and
Part 66 (`tradewar`: private against social resilience); it applies them to the series' own web.
*Reading:* Barrot and Sauvagnat (2016); Carvalho, Nirei, Saito and Tahbaz-Salehi (2021); Elliott, Golub and
Leduc (2022); Farrell and Newman, *Underground Empire*; Baldwin and Freeman (2022).

### Part 58 · The Giants (~54)
*Question:* why are some companies in twenty industries at once, and is that ever a good idea?
*Story:* Alfred Sloan's General Motors in the 1920s: divisions that run themselves and a head office that
allocates capital. In the 1960s conglomerates are the fashion; in the 1980s they are broken up for profit. Yet
the largest companies on earth today are each in a dozen of this series' industries.
*Unit:* a dollar of capital allocated. *Dollar:* a group's cash flow by segment against its investment by
segment: who funds whom.
1. Run it: a group with five businesses and one pool of cash. Allocate it for ten years.
2. The multidivisional firm; the head office as an internal capital market.
3. The conglomerate discount: measured, disputed, and what selection does to the measurement.
4. When it works: Berkshire's float (Part 45), Danaher's system (Part 19), the trading houses (Part 33).
5. The technology giants as conglomerates: one profitable core funding the rest; segment accounts read
   closely.
6. Bundling, self-preferencing and the antitrust cases of the 2020s.
7. Business groups: Korea's chaebol, Japan's keiretsu, India's houses, the family holding companies of
   Europe; pyramids and control.
8. State-owned groups: China's central enterprises; Singapore's holding company; the Gulf funds.
9. Capital allocation as the chief executive's job: reinvest, acquire, pay out, buy back; the record of
   acquisitions.
10. Spin-offs and breakups: the evidence; activist investors.
*The Works:* `group.py`: a holding company allocating cash among Works companies from earlier parts, with a
head-office cost and cross-subsidies; laid beside segment data of six groups.
*Map:* Alphabet, Amazon, Microsoft, Apple, Meta, Tencent, Alibaba, Berkshire Hathaway, Samsung, SK, Hyundai,
Tata, Reliance, Adani, Mitsubishi, SoftBank, LVMH, Siemens, CITIC, Temasek's portfolio, by segment.
*Called it?* the conglomerate boom's own claims in the 1960s against the breakups.
*Sources:* segment disclosures; the Korean and Indian regulators' group filings; antitrust case records.
*Borrowed:* *Economics, Built* Part 62 (`org`: the diversification discount with selection) and Part 8.
*Reading:* Chandler, *Strategy and Structure*; Sloan; Villalonga (2004); Khanna and Yafeh (2007) on business
groups; Morck, Wolfenzon and Yeung (2005); Thorndike, *The Outsiders*.

### Part 59 · Birth (~52)
*Question:* how does a new industry begin, and why do most of its first companies die?
*Story:* in 1909 there are about 270 companies making cars in America (verify). By 1929 three have most of the
market. The same curve (a rush in, a shakeout, a few survivors) has been drawn for tyres, televisions and
penicillin. The part then looks at industries that are on the first half of that curve now.
*Unit:* a firm-year of survival. *Dollar:* an infant industry's dollar: mostly investors' money, not
customers'.
1. Run it: twenty entrants in a new industry, each with three numbers. Pick the five that survive.
2. The life cycle, measured: entry, the peak in the number of firms, the shakeout, the stable oligopoly.
3. Why the shakeout: the dominant design, process innovation and scale; early entrants' advantage.
4. Where entrants come from: spin-offs and the places they cluster (Detroit, Akron, Silicon Valley).
5. Adoption: S-curves again (Part 7); the chasm; the cost curve that makes the market (Part 4).
6. Financing the rush: bubbles as the way capital reaches new industries; railways, fibre, and after.
7. Space: launch cost per kilogram and what reuse did to it; constellations; who the customers are.
8. Autonomy: robotaxis and their unit economics per mile; humanoid robots; drones.
9. Others in infancy at the sweep (candidates: obesity drugs as a new category, quantum computing, fusion,
   cultivated meat): each given the same four numbers.
10. What the state does at birth: procurement as the first customer, standards, safety rules.
*The Works:* `lifecycle.py`: an industry with entry, learning by doing and exit, producing a shakeout; laid
beside the historical counts for cars and tyres and the current counts for launch providers.
*Map:* the newborns' table: segment, firms, funding, revenue, unit cost against the incumbent's.
*Called it?* the series' own calls on which of these industries will have passed its shakeout, logged.
*Sources:* Klepper's datasets as published; launch records; regulators' robotaxi reports; filings.
*Borrowed:* *Economics, Built* Part 21 (Schumpeter) and Part 44 (dynamics); this series' Part 47.
*Reading:* Gort and Klepper (1982); Klepper (1996, 2002) and *Experimental Capitalism*; Utterback, *Mastering
the Dynamics of Innovation*; Jovanovic and MacDonald (1994); Perez, *Technological Revolutions and Financial
Capital*; Janeway, *Doing Capitalism in the Innovation Economy*.

### Part 60 · Decline (~50)
*Question:* what does a dying industry look like from the inside, and can it be a good business?
*Story:* in December 1975 Steven Sasson, an engineer at Kodak, shows his managers a camera the size of a
toaster that records a picture on a cassette tape (verify). Kodak files for bankruptcy in January 2012. For
most of the years between, film was still one of the best businesses in the world.
*Unit:* a year of remaining cash flow. *Dollar:* a declining firm's dollar: where it goes when there is
nothing to reinvest in.
1. Run it: a profitable business shrinking 8% a year. Harvest, reinvest in the successor, or sell.
2. The shapes of decline: slow erosion (tobacco), a cliff (film), a squeeze from one side (department
   stores), a policy death (coal in Europe).
3. Why incumbents see it and still fail: the new product earns less per unit; the organization is built for
   the old one.
4. Newspapers: classified advertising gone in a decade; the accounts of a chain from 2000 to 2020.
5. Film and cameras: Kodak against Fujifilm, which survived.
6. Department stores and malls; video rental; landline telephones.
7. Coal: seams, demand, pensions, bankruptcies; the towns.
8. The endgame's strategies: last one standing, harvest, niche, exit; consolidation; who buys declining
   assets.
9. Liabilities that outlive the business: pensions, clean-up, leases.
10. Labour and place: what happens to the workers and the town.
11. Industries declared dead that were not: radio, vinyl, cinemas, railways.
*The Works:* `decline.py`: a firm in a shrinking market with fixed costs and legacy liabilities, with rivals
choosing when to exit; laid beside the filings of a newspaper chain, Kodak, a department store and a coal
producer over twenty years.
*Map:* a table of declining industries with their peak year, the fall since, and who is left.
*Called it?* forecasts of the newspaper's death by date; Kodak's own 1981 internal report on digital
photography (verify).
*Sources:* twenty years of filings; the Newspaper Association's and Pew's series; the EIA on coal;
bankruptcy court records.
*Borrowed:* *Economics, Built* Part 44 (Arrow's replacement effect) and Part 8 (selection).
*Reading:* Harrigan, *Strategies for Declining Businesses*; Ghemawat and Nalebuff (1985, 1990) on exit;
Christensen, *The Innovator's Dilemma*; Tripsas and Gavetti (2000) on Polaroid; Abernathy, *The Productivity
Dilemma*.

### Part 61 · One Industry, Five Countries (~56)
*Question:* why does the same industry look so different from one country to the next?
*Story:* steel, 1970–2025: America's mills shrink and its minimills grow; Japan's are rationalized by a
ministry; Korea builds one from nothing on a beach with reparations money; China builds half the world's
capacity; India privatizes and then consolidates. Same furnace, five industries.
*Unit:* the same firm under five sets of rules. *Dollar:* the same product's dollar in five countries: labour,
capital, energy, the state.
1. Run it: one company, five rule books. Choose your investments under each.
2. What differs: who owns firms, who finances them, how labour is hired and fired, what the state buys and
   builds.
3. America: capital markets, entry and exit, antitrust that waxes and wanes.
4. Germany and its neighbours: bank and family ownership, co-determination, apprenticeships, the
   export-oriented mid-sized firm.
5. Japan and Korea: groups, main banks, lifetime employment; the developmental state and its record.
6. China: state banks, local governments competing, subsidies, entry on a vast scale, then overcapacity;
   national champions and private giants.
7. India: licences until 1991; services before manufacturing; family groups; the production-linked
   incentives.
8. Four industries compared across the five: steel, cars, banks and telecoms, from the series' Maps.
9. Industrial policy scored: where it built an industry (Korean steel, Chinese solar, Airbus) and where it
   burned the money; what the studies can identify.
10. Convergence or not; the Board, read across countries.
*The Works:* `regimes.py`: one Works company run under five parameter sets (cost of capital, labour
adjustment cost, entry, subsidy); laid beside the five countries' steel, car, bank and telecoms companies from
earlier parts.
*Map:* the Board by country.
*Called it?* "Japan as Number One" (1979) and its sequels about each rising country.
*Sources:* the Board; the OECD's and national accounts; subsidy inventories where published.
*Borrowed:* *Economics, Built* Part 21 (institutions), Part 66 (`tradewar`: Mill's and Bastable's tests) and
Part 47.
*Reading:* Hall and Soskice (eds), *Varieties of Capitalism*; Johnson, *MITI and the Japanese Miracle*;
Amsden, *Asia's Next Giant*; Studwell, *How Asia Works*; Lane (2022) on Korea's heavy industry drive;
Juhász, Lane and Rodrik (2024).

## Act XI · The Job

### Part 62 · The Analyst (~52)
*Question:* who is paid to understand industries, and how do they actually do it?
*Story:* a broker's analyst initiates coverage with a ninety-page report on an industry; a consultant sizes a
market in two weeks for a client who has already decided; an investor spends a month finding out whether one
number in a filing is true. Three jobs, one craft.
1. Run it: forecast a company's next quarter from its filings and three public data series; your error
   against the published consensus.
2. The jobs: sell-side research, buy-side analysis, strategy consulting, corporate strategy and competitive
   intelligence, credit rating, antitrust economics, journalism.
3. The primer: what the first report on an industry contains (the coverage checklist of §1.1 is modelled on
   it).
4. The company model: revenue drivers, costs, capital; three statements; scenarios.
5. Primary research: customers, suppliers, former employees; channel checks; trade shows; site visits.
6. Alternative data: card receipts, app usage, satellites, job postings, shipping records; what each sees.
7. Expert networks and the law: material non-public information; the cases.
8. Incentives: who pays for research and what that does to it; ratings that never say sell.
9. How forecasts are scored: consensus error, the record of long-range forecasts (Part 7).
10. What a language model does to this work, and what it does not.
11. The series' own method, restated as a procedure anyone can run.
*The Works:* `analyst.py`: a company model with drivers, fitted to filings, producing a forecast with a
range; scored on held-out quarters.
*Called it?* a famous initiation or short report and what followed.
*Sources:* filings; the 2003 global research settlement; published studies of forecast accuracy.
*Borrowed:* *Economics, Built* Part 57 (`nowcast`) and Part 64; *Statistics, Built* (forecast scoring).
*Reading:* Koller, Goedhart and Wessels; Mauboussin and Rappaport, *Expectations Investing*; Bradshaw (2011)
on analysts' forecasts; Hong and Kubik (2003) on career concerns; Fisher, *Common Stocks and Uncommon
Profits*, ch. on "scuttlebutt".

### Part 63 · Due Diligence (~54)
*Question:* six weeks to decide whether to buy a company: what do you check?
*Story:* a buyer is given a data room, a management presentation and a deadline. The seller's banker has
written a book in which every chart rises to the right. The part runs a commercial diligence end to end on a
target in the Works' world, where the truth is known and something has been left out.
1. Run it: the seller's deck. Find the three things it does not say.
2. The question behind the diligence: what must be true for the price to be right.
3. The market: size it yourself (Part 7); growth; what the seller's "addressable market" includes.
4. Customers: concentration, retention by cohort, calls with customers, why they buy.
5. Competitors: the Map of the niche; share; who is gaining; win and loss analysis.
6. Unit economics rebuilt from the ledger, not the presentation.
7. Quality of earnings: adjustments, one-offs, working capital, capitalized costs (Part 3).
8. The model: a base case, a downside, and the debt that the downside must carry (Part 47).
9. Risks: one customer, one supplier, one regulator, one person.
10. The memo: a recommendation in two pages; what would change it.
11. Looking back: what diligence missed in deals that failed.
*The Works:* `diligence.py`: a target with planted facts and a seller's presentation generated from it; the
checks as code; the memo's numbers computed.
*Called it?* a diligence failure on the public record (HP and Autonomy, 2011) and what the filings showed
beforehand.
*Sources:* court and regulatory records of failed acquisitions; published studies of acquirers' returns.
*Borrowed:* this series' Parts 3, 5, 7 and 47; *Economics, Built* Part 59 (market definition) and Part 13.
*Reading:* Bruner, *Deals from Hell*; Moeller, Schlingemann and Stulz (2005); Koller et al. on synergies;
Rosenbaum and Pearl, *Investment Banking*, on the process.

### Part 64 · The Report (~58)
*Question:* can you take apart an industry the series never covered, starting from nothing?
*Story:* a blank page and an industry chosen at build time from those the series left out. The film is the
report being made: the sweep, the Register filling, the model company built and laid beside the filings, the
Map drawn, a forecast written down with a date.
1. The choice of industry, and why it was left out.
2. The sweep, shown at speed: sources found, licences checked, rows entered.
3. The unit and the process.
4. The cost structure and the Stack.
5. The Dollar.
6. The model company, built and compared; where it fails.
7. Structure and returns.
8. The cycle and the risks.
9. The Map, dated.
10. What is changing.
11. Three forecasts, each with a date and a scoring rule, entered in `calls.py`.
12. What this report cannot know, and what would change its conclusions.
13. The series' own calls, scored so far; the Board complete; where to go next.
*The Works:* `report.py`: the pipeline from sources to Register to model to Map, as one runnable script, so a
viewer can point it at another industry.
*Run it:* on the site, the template with the viewer's own industry: the fifteen checklist items and the ten
Board rows to fill.
*Sources:* found during the part.
*Reading:* the series.

## 5. Threads that cross the parts

The same few mechanisms explain most industries. Each is introduced once, named, and called back by name.

| Mechanism | First built | Returns in |
|---|---|---|
| High fixed cost, low marginal cost, and the price war that follows | 4 | 8, 11, 15, 27, 28, 30, 36, 39 |
| The capacity cycle with a lead time | 6 | 8, 9, 12, 15, 25, 26, 27, 37, 45 |
| The learning curve | 4 | 15, 18, 20, 42, 56, 59 |
| The scarce link takes the margin | 1 | 15, 16, 18, 42, 57 |
| The razor and the blade (an installed base that pays later) | 19 | 18, 21, 40, 37 |
| The regulated return on an asset base | 13 | 14, 29, 30 |
| The toll booth (a standard with one supplier) | 49 | 30, 36, 40, 48 |
| Two sides and a fee | 5 | 32, 35, 38, 40, 48 |
| Owner, brand and operator split apart | 34 | 26, 30, 35, 37 |
| Float and negative working capital | 3 | 24, 31, 33, 45, 48 |
| Margin against turns | 3 | 16, 31, 33 |
| Borrowing short to hold long | 43 | 25, 26, 44, 45, 47 |
| The hit (a skewed distribution of outcomes) | 20 | 39, 40, 41, 47, 59 |
| Selling hours, and the pyramid | 53 | 24, 44, 54 |
| The chooser is not the payer | 21 | 20, 50, 51, 52 |
| The single buyer or the single seller | 10 | 16, 18, 22, 31, 50 |
| A local market set by transport cost | 11 | 14, 31, 50 |
| The state as owner, customer or rule-maker | 8 | every part's chapter on the state; 61 |

Other threads: the Board, filled a column at a time and read across in Act X; the web of model companies,
joined in Part 57; the five regions, compared in Part 61; the series' own forecasts, logged from Part 7 and
scored in Part 64 and at each refresh.

## 6. What the series is not

- Not investment research. It explains how industries work and says nothing about what any security is worth.
- Not company profiles. Companies appear as examples of a mechanism and as blocks on a dated Map.
- Not business news. Events enter as dated facts in a chapter built to be refreshed.
- Not a strategy course. It describes what firms do and what happened, and leaves advice to the viewer.
- Not economics (*Economics, Built*) or finance (*Quant, Built*), though it uses both and sends the viewer to
  them for the theory.
- Not a summary of other people's market reports. Every figure is rebuilt from a primary source or left out.

## 7. Phases

0. **Infrastructure.**
   - `explainer/industry/`: ACTS and PARTS, the chapter card with the question in the corner, `style.py`;
     `works/firm.py` with its reconciliation tests, `chain.py`, `stack.py`, `cycle.py`, `size.py`;
     `register.py` and `tools/check_register.py`; `board.py`; `calls.py`; `viz.py` (the Unit strip, the Dollar
     waterfall, the Stack, the Map, the Board, the statement view, the as-of stamp); the score, on Monochord,
     as *Economics, Built*'s.
   - The Filing Room: a reader for the SEC's company facts, tested on a dozen companies against their printed
     statements; `data/SOURCES.md`; one regulator dataset end to end (the BTS's Form 41) as the pattern.
   - Check that the build environment can reach the sources (the SEC asks automated clients to identify
     themselves; decide what the client string says). Record each source's terms.
   - Tools: a `Course` entry for `industry` in `tools/series_site.py` with its count in
     `tests/test_series_site.py`; `industry` in `videos/coursekit.SERIES`; `--series industry` for the QA and
     packaging tools; the Run-it kit (`course/site/widgets/00_run.js`) and its scripted player for
     `tools/check_course.py`.
   - The manifest's durable/dated mark and a `tools/build.py` option that rebuilds dated scenes only.
   - `READING.md`, generated and tested as *Economics, Built*'s.
   - `tests/industry/`: the generic firm reconciles for any input; Register rows have sources; a silent smoke
     render.
1. **Pilots.** Part 1 first: it fixes the tone, the Dollar, the Register and the watching devices. Then two
   industry parts chosen to stress the method in opposite ways, built out of order: **Part 28 (Airlines)**,
   where public data is richest (every American carrier's costs by aircraft type) and the theory is already in
   Agora's `revenue`; and **Part 15 (Semiconductors)**, which is global, fast-moving and poorly served by
   public data. (The site counts a series' parts from 1 without gaps, so the two pilots are reviewed from
   previews and contact sheets and reach the site in their turn.) After the pilots, decide:
   - whether a landscape chapter built only from public sources is good enough to carry the series;
   - whether the model company's comparison with filings teaches or only decorates;
   - how long a sweep takes, and so how long sixty-four parts will take.
   If the first answer is no, the series narrows to the industries with good public data or stops.
2. **Act by act,** reviewing at each milestone:
   - Act I (Parts 1–7): the method. A complete short course on its own.
   - Acts II–IV (Parts 8–26): the physical economy.
   - Acts V–VI (Parts 27–35): distribution.
   - Act VII (Parts 36–42): information.
   - Act VIII (Parts 43–49): finance.
   - Act IX (Parts 50–55): people.
   - Acts X–XI (Parts 56–64): systems and the job. These need every Map and the whole Board, so they come
     last.

   Each part goes through: the sweep (§1.2) and its Register rows; licence checks; locking the chapter list;
   the Works module with tests and `compute.py`; English scenes and the QA gates, including
   `tools/check_register.py` and the review of the watching standard on the contact sheet; the course entry,
   lab and interactive; the Chinese edition and its gates; commit and push.
3. **Refresh.** Yearly: `tools/check_register.py --stale` across the series, a sweep of the stale rows, a
   rebuild of the dated scenes, and the scoring of the series' own calls that have come due.

## 8. Decisions, and open risks

**Decisions taken** are in the README. **Open:**

1. **Chinese from the first part,** or after the English series. The plan assumes from the first part. The
   Map's Chinese company names and the term guide (`INDUSTRY_ZH_GUIDE.md`) would be settled in Phase 0.
2. **30–60 minutes per part, most at 45–55.** Parts 8, 13, 15, 17, 20, 28, 36, 42, 43 and 50 are planned at
   the top of the range. An industry that needs more is split at the sweep, not stretched.
3. **Named model companies in one world,** or anonymous ones. The plan assumes named.
4. **The capstone's industry** (Part 64) is chosen at build time. Candidates among those the series leaves
   out: shipbuilding, funeral services, agriculture equipment dealers, the lottery, testing and inspection.
5. **Industries left out** and where they are touched: tobacco and alcohol (22), gambling (35), postal
   services (29), forestry and fishing (10, 11), the public sector as an employer (50, 52), crypto (48),
   cybersecurity (36), biotech tools (21), space (59). Any of these could be a part if the series is extended.

**Risks:**

1. **Staleness.** The Map dates the day it is rendered. §1.3 is the answer; it costs a sweep a year.
2. **Public data may not be enough** for some industries (private markets, contract prices, state-owned
   firms). The pilots test this; §3 says what is done instead; a part may ship with grey bars.
3. **Memory.** This draft is written without sources. Its stories, dates and figures are the most likely
   things to be wrong, and the sweep exists to catch them.
4. **Breadth against depth.** Fifteen checklist items in fifty minutes is tight. The checklist is the floor;
   the chapters after the process and the Dollar may be brief where the industry is simple.
5. **The model company may mislead** by looking more exact than it is. Every comparison shows its misses.
6. **Naming real companies** carries a duty of accuracy. Filings and official findings only; §1.4.
7. **Licences.** Some statistical sources allow reading and not redistribution. They are cited and fetched on
   use, not committed, as *Psychology, Built*'s open data is.
8. **Overlap with *Economics, Built*.** Airlines' pricing, banks' runs, mergers and platforms are already
   built there. This series calls those modules and spends its minutes on the industry.
9. **Scale.** Sixty-four sweeps are sixty-four small research projects. The pilots give the rate.

## 9. Progress

| Part | Sweep | Works module | Scenes | QA | Course material | Chinese |
|---|---|---|---|---|---|---|
| 1 · Where the Money Goes | done 2026-11-23 (118 Register rows) | `works/chain.py` | 18 scenes | silent and narrated previews reviewed | entry, lab, interactive | not started |
| 2 · The Economy on One Page | done 2026-11-23 (37 Register rows; BEA, BLS, Census and World Bank extracts) | — (the BEA table itself) | 21 scenes | silent and narrated previews reviewed | entry, lab, interactive | not started |
| 3 · The Accounts | done 2026-11-23 (119 Register rows; the SEC extract) | `works/firm.py` | 17 scenes | silent and narrated previews reviewed | entry, lab, interactive | not started |
| 4 · The Cost Curve | done 2026-11-23 (83 Register rows; EIA's Electric Power Annual and AEO2026 assumptions) | `works/stack.py` | 15 scenes, illustrated and animated (`draw.py`) | silent and narrated previews reviewed | entry, lab, interactive | not started |
| 5 · The Moat | done 2026-11-24 (31 Register rows; Damodaran's returns 2015-2025, the Census's concentration ratios, the SEC extract) | — (the game in chapter 1 and the course site) | 19 scenes | silent preview reviewed; narrated cut extended to thirty minutes | entry, lab, interactive | not started |
| 6 · The Cycle | done 2026-11-24 (18 Register rows; FRED's hogs, housing, oil and orders; Maersk's ESEF filings; Micron's quarters) | `works/cycle.py` | 19 scenes | silent previews reviewed; narrated cut extended to thirty minutes | entry, lab, interactive | not started |
| 7 · Sizing a Market | done 2026-11-24 (28 Register rows; Uber's and WeWork's prospectuses, Primo's 10-K, the Census's bottled water, home centers, nail salons, e-commerce and households, BLS price indexes, Our World in Data's adoption curves) | `works/diffusion.py` | 17 scenes | silent previews reviewed | entry, lab, interactive | not started |
| 8 · Oil and Gas | done 2026-11-24 (56 Register rows; EIA's bulk files, gasoline components and gas data; the CFTC on April 2020; EIA on 2026; Aramco's Annual Report 2025; the Dallas Fed survey; ExxonMobil's 10-Ks; Hubbert 1956) | `works/oil.py` | 19 scenes | silent preview reviewed | entry, lab, interactive | not started |

Phase 0 is done in the form Part 1 needed: the palette and kit (`style.py`, `kit.py`), the instruments (`viz.py`: the
phone and its exploded view, the region map, the Dollar column, the margin ladder, the treemap, plain axes), the
Register (`register.py`, `data/rows_p01.py`, `tools/check_register.py`), Called it? (`calls.py`) and the course
scaffolding. Still to build: the generic firm (`works/firm.py`, with Part 3), the filings reader, the score, and the
durable/dated split in the manifest.

Part 1 departs from its draft entry where the sweep found more than the plan knew: the 2026 memory shock became two
chapters (9 and 10), the iPhone 17 Pro replaced a generic phone, and the guess, the intermission and the landscape
were added. Its sweep corrected three things the draft had from memory: the mobile-phone forecast story is not used
(no primary source was found), Qualcomm's own 10-K attributes its 2026 fall in handset revenue to memory, not to
Apple's modem, and Apple's 85% share of the industry's operating profit is Counterpoint's figure for Q2 2023, not a
current one.

Part 2 departs from its draft entry in three places. It uses BEA's 2023 sector table itself rather than a model
economy (`works/world.py` waits for the model companies it is meant to hold, Part 57). Its *Called it?* is Leontief's
own 1983 forecast about people and horses, scored against payroll employment, with the series' call on health care
against manufacturing and retail in 2030; Clark's and Fourastié's forecasts are left for Act X. The "500,000 numbers on
cards" in the draft story was not found in a primary source and is not used; the 1936 table's 44 sectors (41
producing) are from the paper and Bjerkholt (2016). The Filing Room's first extracts (`data/fetch.py`) serve it: BEA's
value added and use tables, the BLS's payroll series and the World Bank's shares, each committed as a small CSV with
its URL and retrieval date. The narrated cut came in under thirty minutes, so four chapters were added beyond the
draft: firms by size (Census), who buys and a household's dollar followed back through the table (BEA's final uses),
and who is growing (BEA's real value added), with prices since 2000 and hourly pay by industry inside two others.

Part 3 follows its draft closely. Its six companies are Costco, Microsoft, JPMorgan Chase, NextEra Energy, Delta and
Eli Lilly; its *Called it?* is Bethany McLean's 2001 Fortune article on Enron, scored against Enron's own 10-K, its
restatement and its bankruptcy, with the series' call on Microsoft's fiscal 2027 free cash flow. The generic firm
(`works/firm.py`) is built: a double-entry ledger and a firm whose three statements are tested to reconcile for any
operations.

Part 4 changes the series' look. The user found the first three parts short of pictures and motion, so Part 4 adds a
drawing library (`explainer/industry/draw.py`: power plants, factories, conveyors, planes, cabins, wafers, skylines,
coins, live numbers built from cached digits) and sets all on-screen text through LaTeX, as the rest of the repository
does; every chapter is built around a moving picture (a day on the grid, a seat map filling, a chart morphing from a
linear scale to Wright's law). It departs from its draft entry in three places. Scope and density are one chapter, with
Delta's cargo and American Express miles for scope and an illustrative delivery street for density; the price-war
chapter uses Micron's margins and the DOJ's DRAM fines rather than railways; *Called it?* is the IEA's 2010 solar
roadmap, scored against IRENA's capacity, with the series' call on solar against coal in 2027 (BCG's 1968
*Perspectives on Experience* is not used: no primary copy was consulted). The Run it game is the course site's price
war against a rival with the same plant.

Parts 1-3 were then redrawn in Part 4's style: every chapter of the three now opens on a picture and moves (Pacioli's
book above Venice's water, the bakery's ledger in glyphs, the iPhone's parts flying out of the phone, the economy's
jobs as a crowd), and `tools/dead_air.py` finds no blank or sparse stretch in any of them.

Part 5 follows its draft with three changes. Its industry evidence is Aswath Damodaran's published returns on capital
(2015-2025) and the Census Bureau's 2022 concentration ratios, matched by hand for eight industries; its walls are
shown with real companies (See's and FlightSafety from Berkshire's 2007 letter, Costco, Visa and Mastercard, tobacco,
newspapers and Kodak); and its *Called it?* is Buffett's 2008 view of airlines, scored against Damodaran's airline
returns, with the series' call on the persistence of the 2025 top ten. The first narrated cut ran 26.5 minutes, so
the fade was measured in fifths, Visa and Mastercard, a margin map of nine companies, a worked merger and four tests
of reward against toll were added.

Part 6 departs from its draft in its evidence: the 1973 tankers are replaced by UNCTAD's orderbook (52% of the fleet in
2009) and Maersk's own filings; the hog cycle is tested on the NBER's Chicago data, 1880-1940 (a swing of about 3.6
years, not the cobweb's two); memory chips are Micron's quarters since 2009; and the Works' `cycle.py` (a fleet with
lead times, the cobweb, a bullwhip chain, leverage) is tested. Clark's accelerator and a chapter on the data-centre build-out (Microsoft, Alphabet, Amazon and Meta's spending
against depreciation and cash) were added, with the 2021 car-chip shortage in the bullwhip chapter, to reach thirty
minutes. Its *Called it?* is Intel's 2021 plan against its later losses, with the series' call on Micron's next fall.

Part 7 departs from its draft in its cases: bottled water is the market sized three ways (the Census's factory-gate
shipments, Primo Brands' retail figure, the viewer's sum from Beverage Marketing's gallons), Uber's and WeWork's
prospectuses are the addressable markets (the Uber Eats figures were corrected in the sweep: $795bn is the
serviceable market of delivery, takeaway and drive-through, of which home delivery is $161bn), and the S-curves are
Our World in Data's adoption table, fitted with Bass's model in the Works' `diffusion.py` (tested). Beyond the draft,
the first narrated length called for a home-centers chapter (Home Depot and Lowe's against the census, with nail
salons as the opposite case), a price-and-quantity chapter, a replacement chapter (a model with an assumed life,
labelled), e-commerce's share of retail as a moving window, a sensitivity chart and a fan of S-curves with fixed
ceilings. Its *Called it?* is WeWork's opportunity against its bankruptcy, with the series' call on the Census's
bottled-water shipments for 2026.

Part 8 opens Act II. Its sweep found the year's defining event, which the draft could not know: the war of 28 February
2026 and the closing of the Strait of Hormuz (Brent from $61 to $118 in a quarter, $124 in October; up to 10.9m b/d
shut in), so the price, inelasticity, OPEC and landscape chapters are built on EIA's own accounts of it. The cost of a
barrel is Aramco's reported lifting cost against the Dallas Fed's break-evens (Rystad's cost curve, a tracker, is not
used; the world cost curve is drawn as labelled illustrative blocks around those two figures). Reserves are taught with
ExxonMobil's 2020 de-booking. Spindletop's 'oil at three cents' was not found in a primary source and is not used; the
Handbook of Texas's flow and decline figures are. Hubbert is scored with his own 150bn and 200bn totals redrawn as
logistic curves through EIA's cumulative output to 1955; the peak-oil calls of 2005-08 are left out for want of a
primary source, and his 1956 world peak (about 2000) stands in for them. The Works' `oil.py` (Arps decline, field cash
flows and break-evens, the shale treadmill, clearing multiples, the crack spread) is tested.

