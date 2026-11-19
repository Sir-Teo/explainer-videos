# Economics, Built (经济学，从零搭建)

**Status (2026-11-19): Parts 1 to 12, [*Who Feeds Paris?*](econ1/README.md), [*The Scissors*](econ2/README.md),
[*The Measure*](econ3/README.md), [*The Evidence*](econ4/README.md), [*What People Want*](econ5/README.md),
[*Demand*](econ6/README.md), [*Time and Risk*](econ7/README.md), [*The Firm*](econ8/README.md),
[*The Invisible Hand, Proved*](econ9/README.md), [*The Price Maker*](econ10/README.md), [*Games*](econ11/README.md)
and [*Competition among the Few*](econ12/README.md), are built in English (Acts I to III are complete), each with its computed score,
lab and game; the shared code
(Agora, the Island, the Facts, the Dials, the Data Room, the instruments and the score) is in `explainer/economics/`.** This file is the plan; the standard every part meets, the devices and all
sixty-eight parts chapter by chapter are in [`SYLLABUS.md`](SYLLABUS.md), with progress in its §9. The decisions the
building started from are at the end of this file.

This is a sixty-eight-part course in economics on video: **an undergraduate degree, the first-year PhD core, the
fields, the work economists are paid for, and a research tier**. It covers choice, firms and markets, general
equilibrium, games, information, auctions and market design, growth, consumption, unemployment, money, banks, the
business cycle, monetary and fiscal policy, crises, exchange rates, trade, cities, labour, inequality, taxation,
social insurance, industrial organization, behavioural economics, development, political economy and climate. Then
it covers the tools of a PhD (recursive methods, heterogeneous agents, information economics, structural and
macro-econometrics), the places economics is a job (the central bank, the budget office, the antitrust case, the
pricing desk, the platform, the firm) and the research frontier (networks, machine learning, the economics of AI,
geoeconomics). The videos will be `econ1` … `econ68`, in `videos/economics/econN/`.

Each part is a **30–60 minute lecture** (most will land at 45–55) in the manner of 3Blue1Brown, and it is technical
on purpose. Economics is usually filmed as opinion with stock footage. Here every central idea is a model that is
derived on screen, built in code, solved, and confronted with data: a demand curve from a preference, a price from
a fixed point, a bank run from two equilibria, a recession from a co-op that ran short of scrip, a growth miracle
from one differential equation, an optimal tax from three numbers. Every part is also one story, and every part
puts the viewer inside a market.

## The story: who feeds Paris?

In 1845 Frédéric Bastiat walked into Paris and was struck by a thought. A million people lived there who would
all be dead within days if food stopped arriving, and that night they were asleep, and not one of them was
worried. Nobody was in charge of feeding Paris. Nobody knew how much bread it needed tomorrow. The bread came.

On 5 November 2008, opening a new building at the London School of Economics, Queen Elizabeth II was shown a
chart of the financial crisis and asked the economists in the room why nobody had noticed it coming. It took the
British Academy eight months to send a three-page answer.

The series lives between the wonder and the question: an order that nobody designed, that works well enough to
feed a city and fails badly enough to stop the world, studied by a science that could explain the first and did
not see the second. It puts three questions to every topic:

1. **Who chooses, and facing what?** The people, firms and governments in the story, what each wants, what each
   knows and what each cannot do. Written as mathematics, and first played by you: your bid, your reservation
   wage, your decision to stay in the bank or run.
2. **What happens when the choices meet?** An equilibrium, derived and then computed in running code, and a
   verdict on it: who gains, who loses, and whether anything better was possible.
3. **How would we know?** A plot of prices against quantities is a cloud that traces neither supply nor demand
   (Working, 1927). So every number the series relies on is entered on a board with how it was identified, how
   far the estimates disagree, and what happened when a model that used it made a forecast.

The series tells three stories at once.

* **Building an economy.** The order of the parts is the order of construction. One castaway choosing between
  fish and rest; a second person, and trade; a village and a price; firms; a whole economy in equilibrium;
  monopolies, games and contracts; a market designed on purpose; capital and ideas; money (stone wheels, then
  paper), a bank, a recession, a central bank, a treasury, a crisis; a second island and an exchange rate; a
  labour market, a tax system, a welfare state. Then a hundred thousand different households solved on a
  computer, the tools, the work and the frontier.
* **The history of the field, 1758 to now.** Quesnay's *Tableau*, Smith's pin factory, Ricardo, Malthus and
  Marx; the marginalists of the 1870s; Marshall; the Depression and Keynes; Arrow, Debreu and Samuelson's
  mathematics; Friedman, Lucas and the fight over the cycle; game theory and information; the credibility
  revolution; 2008, 2020 and after. Each part opens in its era, and the dead ends are told too: the labour
  theory of value, the stable Phillips curve, the Soviet plan, the Washington Consensus as first written.
* **A science learning to check itself.** It starts with that cloud of dots. The methods invented to read it
  (instruments, natural experiments, randomized trials, structural models, forecasts scored in public) and
  their failures run through the whole series.

## The devices that hold it together

1. **Agora** (`explainer/economics/agora/`). *Agora* is Greek for the gathering place that became the market.
   It is the economy the series builds: a small, tested Python library that gains one mechanism in each part,
   from a consumer and an exchange economy to an auction house, a matching clearinghouse, a growth model, a
   bank that can be run on, a New Keynesian model with a central bank, a quantitative trade model and a
   heterogeneous-agent economy. Later parts reuse earlier modules on screen: the consumer of Part 6 becomes the
   household of Part 22 and one of the hundred thousand in Part 52. Each module is checked against an
   independent reference (a closed form, a published calibration reproducing its published table, QuantEcon,
   Dynare's documented examples, or *Statistics, Built*'s statkit).
2. **The Island** (`explainer.economics.island`). Economics has always thought on islands: Crusoe's, the
   stone money of Yap, Diamond's coconuts, Phelps's and Lucas's islands. The series has one. It is Agora
   running as a seeded, simulated world with a cast that persists from part to part, and it grows as the series
   does: one castaway in Part 1, a fish market in Part 2, a bank in Part 26, a second island in Part 34, a
   hundred thousand households by Part 52. In the real economy the truth is hidden. On the Island it is known,
   so a method can be graded: whether an instrument recovers the demand elasticity that was planted, whether a
   VAR finds the monetary shock that was actually sent, how often a difference-in-differences gets the sign
   right. Always labelled `simulated`.
3. **The Tableau** (`tableau_map`). In 1758 François Quesnay, a court physician, drew the economy as a
   circulation, like blood. In 1949 Bill Phillips built it out of water tanks and pumps (the MONIAC). The
   series map is that machine: households, firms, banks, a government and the rest of the world, joined by
   pipes. Each part adds or opens one pipe, and the map is redrawn with that part flowing. What is still
   drawn as a sealed box at the end is the list of open problems.
4. **The Facts** (`explainer.economics.facts`). About forty regularities, fixed for the whole series, that any
   account of an economy has to reproduce: Engel's law, the law of one price and its failures, Kaldor's six
   facts, Okun's law, the Beveridge curve, consumption smoother than income, investment three times as volatile
   as output, hump-shaped responses to a monetary shock, the equity premium, Zipf's law for cities, Pareto
   tails in wealth, the gravity equation. Each has three columns: **the data**, **Agora's result**, and
   **your guess** (asked before either is shown). In the last part Agora sits the whole list, and the
   scorecard shows what the built economy can and cannot yet do.
5. **The Dials** (`explainer.economics.dials`). Economics runs on perhaps sixty numbers: the elasticity of
   labour supply, the marginal propensity to consume, the fiscal multiplier, the slope of the Phillips curve,
   the return to a year of school, the employment effect of a minimum wage, the trade elasticity, the
   elasticity of taxable income, the discount rate under the social cost of carbon. Each is a dial with a row:
   the range of estimates, each estimate's identification strategy, sample and year, how the answer changes
   policy, and the date the row was checked. A dial can be `settled within a range`, `contested`,
   `depends on the setting` or `not identified`. It plays the role of *Psychology, Built*'s Replication Ledger
   and *Statistics, Built*'s Coverage Board, and `tools/check_dials.py econN` will be its gate.
6. **The Data Room** (`explainer.economics.data`). Real data, with source and vintage on screen: the
   Maddison Project and the Penn World Table, FRED and ALFRED (so a number can be shown as it was first
   published), the Jordà–Schularick–Taylor macrohistory database, the World Inequality Database, Comtrade,
   Shiller's series; and the historical tables transcribed from their publications: Engel's budgets (1857),
   Phillips's wage data (1958), Douglas's factory series (1928), Friedman and Schwartz's money stock, Card and
   Krueger's restaurants. Each film freezes its data on a stated date.
7. **Play it.** Every part runs one game, auction or decision on the viewer, with a pause, and then shows
   the published distribution of what people actually do: a double auction, a guess of two-thirds of the
   average, a sealed bid, a bank run, a turn as the central banker, an offer in a matching market. On the
   course site each part's interactive is the game itself, played in the browser against Agora's agents, with
   nothing stored or sent.
8. **On every chapter card:** the timeline strip (1750–2030); the **scale strip**, which lights the level the
   chapter works at (person, household, firm, market, city, nation, world) and its horizon (a day, a year, a
   decade, a century); and payoff cards ("where this comes back"). Each part closes with an *In practice* card
   (the jobs and decisions the idea serves) and a *Frontier* chapter (what is open). Cross-series links point
   to *Statistics, Built* (causal inference, time series), *Quant, Built* (finance), *Psychology, Built*
   (judgment and choice), *AI, Built* (learning) and *Philosophy, Built* (justice, rationality) instead of
   repeating them.

## Made to be watched to the end

A fifty-minute lecture is finished by people who are never left alone with a wall of algebra and never unsure
why the next step matters. This is an educational mission, so finishing is the measure. Every part is built to
the same shape (the rules are in the syllabus, §1.3):

* **A cold open.** Sixty to ninety seconds before the title, on a scene with stakes: a prisoner-of-war camp where
  cigarettes become money, eighteen farmers signing a secret contract in 1978, a napkin with a curve on it, a
  bank that lost forty-two billion dollars of deposits in a day.
* **One question, kept in view.** The part's question sits in a corner of every chapter card, and the recap
  answers it.
* **You play before you are told.** The Play-it game comes in the first third, before the theory that explains
  it, so the model arrives as the explanation of something the viewer has just done.
* **Something changes every four minutes.** A chapter is three to four minutes and ends on a prediction the
  viewer is asked to make. No derivation runs longer than ninety seconds without the picture it describes
  moving beside it.
* **The Island is a serial.** The same characters, drawn the same way, meet the part's problem at the start
  and live with its solution at the end. Parts end on the problem the next one opens with.
* **Called it?** Once a part, a prediction made in advance is put beside what happened: Malthus on population,
  Keynes on the fifteen-hour week, Friedman on stagflation (right), McFadden on a railway's ridership (right),
  the exchange-rate models against a coin (wrong), the forecasts of 2008 and of 2021.
* **An intermission.** Near the midpoint, thirty to forty-five seconds with no narration: a *data film* (two
  centuries of income in two hundred countries, the yield curve breathing since 1960, the world trade network
  thickening, lights coming on across Asia at night) under the score, then a one-card "the story so far".
* **A score you can hear.** `explainer/economics/score.py` will compute a small score (nothing recorded,
  nothing third-party, synthesized on Monochord, the instrument *Music, Built* builds) and `tools/build.py`
  already mixes such a score into the master. The theme is the scissors: two voices, one rising and one
  falling, that cross on a single note. They start an octave apart under the hook, move one step closer at
  each chapter card, and meet in the outro. A bed breathes under Play-it pauses, and in the intermission the
  part's own data series is played as a melody (unemployment since 1948 is a tune). It sits 8 to 18 LU below
  the narration; `--no-score` leaves it out.
* **Places.** The trading pit, the Tsukiji tuna auction, the port of Rotterdam, a village market in
  Maharashtra, the gold room of the Bank of England: each drawn in the series' own hand as a twenty-second
  vignette, never stock footage.

## Four ways through it

Every part is written so that its chapters climb. The opening chapters are the principles course: the puzzle,
the game, the picture. The middle chapters are the intermediate and graduate course: the model derived, solved
and estimated. The closing chapters are the Dials, *In practice* and the *Frontier*. The course site's four
tracks follow from that (the tiers of `videos/coursekit`):

| Track | Who it is for | What it is |
|---|---|---|
| **U** · Principles and the major | anyone; school algebra at the start, calculus from Part 5 | the opening chapters of Parts 1–50: a complete principles course, then intermediate micro, macro and the fields |
| **M** · The graduate course | an economics graduate, or anyone with multivariable calculus, linear algebra and probability | the model chapters of every part, and Act X (Parts 51–56) |
| **D** · The research tier | a PhD student | every part's Frontier chapter, and Act XII (Parts 63–68) |
| **I** · Practice | central-bank and treasury staff, consultants, tech and pricing economists, analysts, policy staff, data scientists | every part's In practice chapter, and Act XI (Parts 57–62) |

Milestones mark the degree: Part 50 is the capstone (a policy memo, written from question to recommendation),
Part 56 is the core exam, and Part 68 is the dissertation.

## The acts

| Act | Parts | Question |
|---|---|---|
| **I. The Question** | 1–4 | How does an order nobody designed arise, how is an economy measured, and how do we avoid fooling ourselves? |
| **II. Choosing** | 5–8 | What do people and firms want, and what can be read from what they do? |
| **III. Markets** | 9–12 | What happens when the choices meet? (general equilibrium, monopoly, games, oligopoly) |
| **IV. Failure and Design** | 13–18 | When do markets fail, and can better ones be built? (information, incentives, spillovers, auctions, matching, collective choice) |
| **V. The Long Run** | 19–24 | Why are some countries rich, and what do households and firms do across time? (the escape from Malthus, growth, saving, capital, unemployment) |
| **VI. Money and the Cycle** | 25–33 | What is money, why do economies slump, and what can a central bank or a treasury do about it? |
| **VII. The World Economy** | 34–37 | What changes when there is more than one economy, and where does activity locate? (exchange rates, trade, cities) |
| **VIII. Work and the State** | 38–42 | Who earns what, and what should a government take and give? (wages, inequality, taxes, social insurance) |
| **IX. The Fields** | 43–50 | What do economists do all day? (industrial organization, behaviour, development, politics, climate, the family) Then the capstone. |
| **X. The Graduate Core** | 51–56 | How is an economy solved on a computer and a model taken to data? Then the core exam. |
| **XI. Economics at Work** | 57–62 | Where is economics a job? (the forecast, the budget office, the courtroom, the pricing desk, the platform, the firm) |
| **XII. The Frontier** | 63–68 | Where does the field stop knowing, and how do you push it? (networks, machine learning, AI, geoeconomics, the field's own reform, the dissertation) |

## How it looks

The series draws in the manner of 3Blue1Brown with the instruments of `explainer/ai/viz.py` and
`explainer/ai/lecture.py`, plus its own in `explainer/economics/viz.py` (list in the syllabus, §3).

* **Curves come from somewhere.** A demand curve is never drawn freehand. It is traced on screen by a budget
  line swinging across an indifference map, or summed from the Islanders' own reservation prices, and it keeps
  the colour of where it came from.
* **Equilibrium is a motion.** Prices grope, bids arrive, a best response chases another across a plane, a
  phase diagram's saddle path is found by shooting and missing. The fixed point is shown being reached, and
  where it is not reached that is shown too.
* **Money is a balance sheet.** Every monetary operation (a loan, a run, quantitative easing, a currency
  defence) is drawn as T-accounts that move, with both sides lit at once.
* **Identification is a picture.** Every empirical result is drawn as its design before its estimate: the
  two states and the border between them, the cutoff, the lottery, the instrument's one path. The same design
  is then run on the Island, where the truth is a dashed green line.
* **Model against data, always in the same colours.** Data are white, Agora is orange, the Island's planted
  truth is dashed green. Demand is blue and supply is amber everywhere. Households, firms, banks, the
  government and the rest of the world keep one colour each from the Tableau to the last balance sheet.
* **The camera travels the scales.** From one stall in a market to the city, the national accounts, the map of
  world trade, and back down to one household's budget.
* **Real numbers.** Everything plotted is `computed` (the part's `compute.py`), `data` (the Data Room, with
  source and vintage), `published` (cited), `simulated` (the Island), `illustrative` or `schematic`, and tagged
  as such.
* **Ideas are drawn, not listed.** Mechanisms, typologies and debates use the diagram instruments already in
  `explainer/psychology/viz.py` (`flow_chain`, `quadrant`, `theory_card` with `verdict_row`), promoted to a
  shared module in Phase 0.

## The parts

| # | Part | Hook | Ideas, models and mathematics | Agora gains | Play it |
|---|---|---|---|---|---|
| **I** | **The Question** | | | | |
| 1 | Who Feeds Paris? | Bastiat walks into Paris, 1845; the Queen's question, 2008 | scarcity and opportunity cost, the margin, incentives, specialization and the pin factory, comparative advantage in one table, the hockey stick of income, what a model is, positive and normative, the Tableau | Crusoe alone: a frontier and a choice; the Tableau, empty | a pit market: you hold one card with a value on it |
| 2 | The Scissors | Chamberlin's classroom, 1948, and Vernon Smith's, 1956 | the diamond–water paradox and the marginal revolution, demand and supply built from reservation prices, equilibrium and its stability, elasticity, surplus, tax incidence, price ceilings and floors, traders with zero intelligence | a double auction; a market solver | guess the price before the market finds it |
| 3 | The Measure | Kuznets reports to the Senate, 1934 | GDP three ways, the accounts as a matrix, real and nominal, Laspeyres, Paasche, Fisher and chain indices, the Boskin bias, PPP, unemployment as a survey, Lorenz and Gini, input–output tables, what GDP leaves out, revisions | the Island's national accounts; an index-number lab | which basket: how much did prices rise? |
| 4 | The Evidence | Working's cloud of dots, 1927 | simultaneity, Philip Wright's instrument (1928), Haavelmo, omitted variables, Leamer's "con", LaLonde's test, natural experiments, randomized trials, the Lucas critique, structural and reduced-form, forecasts as tests | the Island's econometrician; the Dials | draw the demand curve through the cloud |
| **II** | **Choosing** | | | | |
| 5 | What People Want | Samuelson, 1938: can wants be read from purchases? | preference axioms, utility representation, indifference maps, budget sets, Lagrange's method, revealed preference, Afriat's theorem tested on real choices, what rationality does and does not assume | a consumer; a revealed-preference tester | are your own choices consistent? |
| 6 | Demand | the rice of Hunan: a Giffen good found, 2008 | Marshallian and Hicksian demand, the Slutsky equation derived, duality, Engel curves, compensating and equivalent variation, exact welfare from a demand curve, demand systems, the cost of living | a demand system; a welfare calculator | split a price change into its two effects |
| 7 | Time and Risk | the St Petersburg game, 1738 | Fisher's two-period diagram and the Euler equation, expected utility and the von Neumann–Morgenstern theorem, risk aversion, insurance, stochastic dominance, Allais, Ellsberg, Rabin's calibration, discounting and present bias | an intertemporal chooser; an expected-utility maximizer | the Allais pair, with the published split |
| 8 | The Firm | Douglas's chart: a share that holds still, 1927 | technology and isoquants, returns to scale, cost minimization and duality, cost curves, profit maximization and supply, entry and the long run, why firms exist (Coase 1937), boundaries and hold-up | a firm; an industry with entry | run a factory: hire until it stops paying |
| **III** | **Markets** | | | | |
| 9 | The Invisible Hand, Proved | cigarettes in a prisoner-of-war camp, 1943-45 | the Edgeworth box, the core, Walras's law, existence by a fixed point, both welfare theorems proved, tâtonnement and Scarf's counterexample, computing equilibria, anything goes (Sonnenschein–Mantel–Debreu), the calculation debate | an exchange and production economy solver | trade in the box until nobody can gain |
| 10 | The Price Maker | Dupuit and the third-class carriage, 1849 | monopoly and the markup rule, deadweight loss, three degrees of price discrimination, two-part tariffs, bundling, the durable-goods problem, natural monopoly, Ramsey prices and regulation | a monopolist with a pricing menu | set the fare for a ferry that costs nothing to run |
| 11 | Games | RAND, January 1950: the first prisoner's dilemma | dominance, Nash equilibrium and existence, mixed strategies tested on penalty kicks, extensive forms and backward induction, repeated games and the folk theorem, Axelrod's tournaments, focal points, evolutionary stability, level-k | a game solver; a tournament | two-thirds of the average |
| 12 | Competition among the Few | "our customers are the enemy": the lysine tapes, 1992-95 | Cournot, Bertrand and Stackelberg, capacity, Hotelling's line and product differentiation, monopolistic competition, cartels and their detection, entry deterrence, concentration and mergers in one formula | an oligopoly lab | name your price against one rival, then twenty |
| **IV** | **Failure and Design** | | | | |
| 13 | Lemons and Signals | Akerlof's paper, rejected three times, 1967–70 | adverse selection and unravelling, signalling, screening and separating contracts, the death spiral in a real health plan, testing for asymmetric information, cost curves for selection markets | a lemons market; an insurance market | buy a used car you cannot inspect |
| 14 | Incentives | eighteen thumbprints in Xiaogang, 1978 | moral hazard, the principal–agent problem solved, risk against incentives, multitasking, tournaments, career concerns, efficiency wages, piece rates at Safelite, incomplete contracts and ownership | a contract designer | write the contract, then watch the agent |
| 15 | Spillovers | Meade's bees and Cheung's beekeepers, 1952–73 | externalities and Pigou's tax, Coase's theorem and its fine print, public goods and Samuelson's condition, free riding, the commons and Ostrom's exceptions, permits, prices against quantities, congestion | a commons; a permit market | contribute to the pot, ten rounds |
| 16 | Auctions | £22.5 billion for air, London, 2000 | four formats, Vickrey's truth-telling, revenue equivalence proved, Myerson's optimal auction, the winner's curse, spectrum and ad auctions, collusion and bad designs | an auction house | bid in a first-price and a second-price auction |
| 17 | Markets by Design | the scramble for medical interns, 1945–51 | the revelation principle, VCG, the Myerson–Satterthwaite impossibility, deferred acceptance and its proof, the residents' match, school choice, top trading cycles and kidney exchange, unravelling and congestion | a clearinghouse | rank your schools: should you tell the truth? |
| 18 | Social Choice and Welfare | Condorcet's cycle, 1785; Arrow's thesis, 1950 | voting paradoxes, Arrow's theorem proved, the median voter, strategy-proofness, welfare functions from Bentham to Rawls, Harsanyi's veil, Sen, cost–benefit analysis and the value of a statistical life | a voting lab; a welfare evaluator | vote under five rules, get five winners |
| **V** | **The Long Run** | | | | |
| 19 | The Great Escape | Malthus's essay, 1798, published on the eve of its own refutation | ten thousand years of flat income, the Malthusian model derived, the Black Death as a test, why Britain and why 1760, the Great Divergence, the demographic transition, unified growth | a Malthusian economy that can escape | place the year the line turns up |
| 20 | Growth I: Capital | two Koreas from orbit | Kaldor's facts, the Solow model derived, the golden rule, convergence and its tests, growth and development accounting, the residual, Ramsey's problem and the saddle path | Solow and Ramsey | choose a saving rate for a century |
| 21 | Growth II: Ideas and Institutions | Nordhaus prices light, from Babylon to the LED | non-rival ideas, Romer's model, creative destruction, scale effects and ideas getting harder to find, misallocation, institutions and the settler-mortality debate, geography and culture, directed technical change | an idea-driven economy; a misallocation measure | how many hours of work for an evening of light? |
| 22 | Consumption and Saving | rebate cheques mailed by Social Security digit, 2001 | the consumption function, permanent income and the life cycle, Hall's random walk, precautionary saving and buffer stocks, the marginal propensity to consume measured, the hand-to-mouth, Ricardian equivalence, overlapping generations and pensions | a life-cycle household; an OLG economy | a windfall arrives: how much do you spend? |
| 23 | Capital and Asset Prices | the equity premium that should not exist, 1985 | present value, the user cost and Tobin's q, irreversibility, Modigliani–Miller, the Lucas tree and the stochastic discount factor, the equity premium and risk-free puzzles, excess volatility, bubbles | a Lucas tree; an investing firm | price a tree that pays fruit |
| 24 | Looking for Work | Diamond's coconuts, 1982 | stocks and flows, the Beveridge curve, the reservation wage, the matching function, the Diamond–Mortensen–Pissarides model derived, bargaining and efficiency, the volatility puzzle, job ladders, the natural rate | a search and matching labour market | take the offer or keep looking? |
| **VI** | **Money and the Cycle** | | | | |
| 25 | Money | the stone money of Yap | what money does, commodity and fiat, money from search (Kiyotaki–Wright), the quantity theory, Cagan's hyperinflations, seigniorage, how four big inflations ended, money demand, how banks create money | a monetary exchange economy; a hyperinflation | which object becomes money? |
| 26 | Banks and Runs | forty-two billion dollars in a day, March 2023 | maturity transformation, Diamond–Dybvig derived, two equilibria, Bagehot's rule, deposit insurance and moral hazard, repo and shadow banks, global games, capital and liquidity rules | a bank that can be run on | stay or withdraw? |
| 27 | The Keynesian Revolution | the babysitting co-op that had a recession | the Depression in data, Say's law, the multiplier, the paradox of thrift, IS–LM derived, the liquidity trap, aggregate demand and supply, Phillips's water machine | the co-op; IS–LM | hoard or spend your scrip? |
| 28 | Inflation and Expectations | Friedman's forecast, December 1967 | the Phillips curve and its collapse, the natural rate, adaptive and rational expectations, Lucas's islands, the Lucas critique, time inconsistency, Volcker, independence and targets, 2021–23 | an expectations-augmented economy; a policy game | forecast next year's inflation, twelve times |
| 29 | The Cycle as Equilibrium | Kydland and Prescott's provocation, 1982 | business-cycle facts and filters, the Bellman equation, value function iteration, the stochastic growth model, calibration, log-linearization and the saddle-path condition, impulse responses, what the model misses | a dynamic programming solver; an RBC model | which series leads the cycle? |
| 30 | Sticky Prices | how often does a price change? | monopolistic competition, menu costs, Calvo pricing, the New Keynesian Phillips curve derived, the dynamic IS curve, the Taylor rule and principle, the three-equation model solved, optimal policy, the zero bound, medium-scale models | a New Keynesian model | guess the price that never moved |
| 31 | The Central Bank | "whatever it takes", 26 July 2012 | how a rate is set and enforced, the transmission, identifying a monetary shock four ways, the zero bound, quantitative easing and forward guidance, the neutral rate, balance sheets, communication | a central bank with a balance sheet | set the rate through the 1970s |
| 32 | The Treasury | a spreadsheet's missing rows, 2010–13 | the government's budget constraint, multipliers in theory and in four kinds of evidence, tax changes, austerity, debt dynamics and r against g, the fiscal theory of the price level, sovereign default | a fiscal authority; a default model | stabilize the debt without a slump |
| 33 | Crises | "why did nobody notice it?" | manias and Minsky, debt deflation, the financial accelerator, collateral cycles, the anatomy of 2008, household debt, a hundred and fifty years of credit booms, the gold standard, macroprudential policy, the lender of last resort in action | a leveraged economy with a collateral constraint | spot the boom that ends badly |
| **VII** | **The World Economy** | | | | |
| 34 | The Open Economy | Black Wednesday, 16 September 1992 | the balance of payments, purchasing power and interest parity, the random walk nobody could beat, the trilemma, Mundell–Fleming, overshooting derived, three generations of currency crisis, currency areas and the euro, the dollar | a second island; an exchange rate | defend the peg or let it go? |
| 35 | Trade I: Comparative Advantage | Ulam's challenge to Samuelson | Ricardo's model, a continuum of goods, Heckscher–Ohlin and its four theorems, the Leontief paradox, who loses from trade, tariffs and quotas, the optimal tariff, protection for sale, Japan's opening as a test | a Ricardian and a factor-proportions world | who should make what? |
| 36 | Trade II: Scale, Firms and Gravity | a box on a ship, April 1956 | love of variety, the home-market effect, heterogeneous firms (Melitz) derived, gravity from Tinbergen to its micro-foundations, one formula for the gains from trade, the China shock, tariff pass-through, value chains | a quantitative trade model | predict the trade between two countries |
| 37 | Cities and Regions | Schelling's checkerboard, 1969 | von Thünen's rings, the monocentric city, agglomeration, Zipf's law, the core and the periphery, spatial equilibrium, housing supply and rent control, neighbourhoods and mobility, the Berlin Wall as an experiment | a city; a system of cities | move if fewer than a third are like you |
| **VIII** | **Work and the State** | | | | |
| 38 | Work and Wages | 410 fast-food restaurants on a state line, 1992 | labour supply and its elasticities, labour demand, the minimum wage and what bunching shows, monopsony, human capital and Mincer's equation, the return to schooling by five designs, selection, immigration | a labour market with monopsony | the minimum wage rises: predict employment |
| 39 | The Wage Structure | Emily, Greg, Lakisha and Jamal, 2004 | the race between education and technology, tasks and polarization, robots, firms and worker–firm sorting, unions, compensating differentials, taste and statistical discrimination, the gender gap and the child penalty | a task-based labour market | which jobs did the computer take? |
| 40 | Inequality and Mobility | a parade of dwarfs and a few giants (Pen, 1971) | measuring inequality, top shares from tax data, Pareto tails and where they come from, wealth and r against g, the Kuznets curve, mobility and the Gatsby curve, places and opportunity, global inequality | a random-growth wealth model | where are you in the parade? |
| 41 | Taxes | a curve on a napkin, 1974 | incidence, deadweight loss, Ramsey's rule, Mirrlees's problem and the top-rate formula derived, the elasticity of taxable income, bunching, salience, taxing capital and corporations, evasion and havens | an optimal-tax calculator | set the top rate from three numbers |
| 42 | Social Insurance | a lottery for health insurance, Oregon, 2008 | why markets underinsure, optimal unemployment insurance in one formula, moral hazard measured, health insurance experiments, pensions and defaults, disability, the EITC and cash transfers, basic income trials, the value of public funds | an insurance designer; a pension system | how generous should benefits be? |
| **IX** | **The Fields** | | | | |
| 43 | Measuring Market Power | the cereal aisle | from concentration to conduct, the logit and its red-bus problem, random-coefficients demand (BLP) derived and estimated, merger simulation, production functions and markups, entry thresholds, has market power risen? | a demand estimator and merger simulator | which merger raises prices more? |
| 44 | Dynamics, Platforms and Antitrust | Harold Zurcher's bus engines, 1987 | dynamic discrete choice, dynamic oligopoly, vertical restraints, two-sided markets, network effects and tipping, innovation and competition, killer acquisitions, pricing algorithms that learn to collude, the antitrust debate | a platform; a dynamic choice estimator | replace the engine now or wait? |
| 45 | Behavioural Economics | paying not to go to the gym, 2006 | reference dependence in the field, present bias and commitment, defaults, inattention and salience, social preferences, do anomalies survive markets?, behavioural welfare, nudges at scale, rational inattention, expectations that overreact | behavioural agents for the Island | sell the mug you were just given |
| 46 | Development | a bed net: free, or sixty cents? | measuring poverty, poverty traps, structural change, the productivity gap in farming, microcredit, cash, graduation programmes, schooling and health experiments, risk sharing in villages, history that persists, the debate over experiments | a village economy with a trap | spend the aid budget |
| 47 | Political Economy | core samples from Indonesian roads, 2007 | collective action, rent seeking, do voters choose policies?, lobbying, capture, state capacity, democracy and growth, corruption measured four ways, conflict, media, persistence, populism | a political economy with lobbying | fund the public good, or lobby? |
| 48 | Environment and Climate | Simon and Ehrlich's bet, 1980–90 | exhaustible resources and Hotelling's rule, the fishery, a climate–economy model built, the social cost of carbon, the fight over the discount rate, fat tails, taxes against permits, leakage, learning curves, electricity markets, damages measured | a climate–economy model | choose the discount rate, see the carbon price |
| 49 | The Economic Approach | Becker pays for parking, or does not | crime and deterrence, the family, marriage as a matching market, fertility, class size and teacher value added, early childhood, health capital, physicians and prices, patents and drugs, deaths of despair | a marriage market; a deterrence model | does the size of the fine matter? |
| 50 | **The Policy Memo** (capstone) | one real proposal, one deadline | a policy analysis from question to recommendation: the market, the incidence, the general-equilibrium effects, the evidence and its Dials, the budget cost, the distribution, the uncertainty, the memo | the capstone memo | what would you advise? |
| **X** | **The Graduate Core** | | | | |
| 51 | Computing Economies | Bellman names it "dynamic programming", 1950 | the contraction mapping theorem, value and policy iteration, endogenous grids, projection and perturbation, continuous time and the HJB equation, accuracy and Euler errors, the curse of dimensionality | `agora.solve`: the solution harness | which grid is fine enough? |
| 52 | Many Agents | whom does the representative agent represent? | incomplete markets, the Aiyagari economy solved, the wealth distribution, aggregate shocks and approximate aggregation, the continuous-time system, HANK and the two channels of monetary policy, sequence-space Jacobians, firm dynamics | a heterogeneous-agent economy | whose spending moves when rates fall? |
| 53 | Information and Persuasion | a prosecutor who convicts twice as often as she should | Bayesian games and refinements, cheap talk, Bayesian persuasion by concavification, information design, common knowledge and the email game, global games, herding and cascades, reputation, bargaining, relational contracts | a persuasion and signalling solver | design the test the judge will see |
| 54 | Estimating Models | McFadden forecasts a railway that is not built yet | the method of moments generalized, maximum likelihood, simulated moments and indirect inference, discrete choice, dynamic models, identification and sensitivity, sufficient statistics against structure, validating a model with an experiment | `agora.estimate`: the estimation harness | which moment pins down which parameter? |
| 55 | Identifying Macro | the price puzzle | VARs and five ways to identify them, local projections, narrative and high-frequency shocks, estimating a DSGE model, regional evidence and the missing intercept, forecasts as tests, what macro data can and cannot say | `agora.macrometrics` on the Island | which shock was it? |
| 56 | **The Core Exam** | the night before | twelve first-year exam problems, micro, macro and econometrics, solved on screen with the grader's eye | the exam's numbers | try each before the solution |
| **XI** | **Economics at Work** | | | | |
| 57 | Reading the Economy in Real Time | nine of the last five recessions | how the numbers are made and revised, seasonal adjustment, nowcasting, forecast evaluation, the yield curve, fan charts, prices scraped online, card and satellite data, text as data | a nowcaster; a forecast scorer | nowcast the quarter, release by release |
| 58 | Scoring the Bill | "benefits to whomsoever they may accrue", 1936 | cost–benefit analysis as practised, discounting, valuing life, time and nature, budget scoring and dynamic scoring, microsimulation, distribution tables, computable general equilibrium, regulatory impact | a microsimulation model | score a tax change |
| 59 | The Expert Witness | Staples and Office Depot, 1997 | market definition, diversion and upward pricing pressure, merger simulation in court, bargaining models, cartel damages, labour-market cases, regulated prices, what survives cross-examination | a merger-review toolkit | is this one market or two? |
| 60 | The Price | American Airlines against People Express, 1985 | measuring willingness to pay, price experiments, revenue management, dynamic pricing, versioning and bundles, subscriptions, promotions, behavioural pricing, algorithmic pricing and its law | a revenue manager | sell a hundred seats before the plane leaves |
| 61 | Economics at the Platforms | New Year's Eve, and the surge that failed | marketplace design, search and ranking, reputation, surge pricing, ad auctions in practice, experiments with interference, causal machine learning in production, the gig economy, data and attention | a two-sided marketplace | set the commission |
| 62 | Inside the Firm | twenty textile plants near Mumbai, 2008 | management as a technology, productivity dispersion, personnel economics, executive pay, capital structure and agency, corporate governance, private equity, why firms price uniformly, organizational economics | a firm with managers | which practice pays? |
| **XII** | **The Frontier** | | | | |
| 63 | The Economy as a Network | an earthquake's shadow down the supply chain, 2011 | input–output and Hulten's theorem, granular firms, when small shocks do not average out, non-linear propagation, supply chains, financial contagion and clearing, social networks and diffusion, games on networks | a production network; a clearing system | which firm's failure matters most? |
| 64 | Machines that Learn | a judge, a defendant and an algorithm | prediction policy problems, double machine learning, heterogeneous effects, text and images as data, deep learning as a solution method, reinforcement learners as agents, language models as subjects, fairness | deep solvers and learning agents | judge or algorithm? |
| 65 | The Economics of AI | Keynes's grandchildren, 1930, due in 2030 | tasks and automation, general-purpose technologies and the productivity J-curve, what the experiments find, exposure and wages, growth with automated ideas, market structure of AI, distribution and policy, agents that transact | an economy with automatable tasks | when does the growth rate take off? |
| 66 | Geoeconomics and Industrial Policy | a tariff formula, 2 April 2025 | tariffs measured, trade wars as games, sanctions and chokepoints, security against efficiency, the infant-industry argument and its evidence, subsidies and chips, friend-shoring, reserve currencies | a trade war on the quantitative model | retaliate or not? |
| 67 | The Next Economics | 50,000 tests and a hump just past 1.96 | replication in economics, specification searching, pre-analysis plans, administrative data, the empirical turn, structure and design reconciled, complexity and agent-based models, who becomes an economist, automated research | a model of a research field | pick the result that will replicate |
| 68 | **The Dissertation** | back to Paris | how research is done: a question, a design, a model, a paper carried from idea to result, the final Dials, Agora against the Facts, the Tableau's sealed boxes, the open problems | the thesis | the last market |

## What it follows

The series reads like the reading lists of a strong department. [`READING.md`](READING.md) maps the textbooks, the
field's major models and its classic papers to the parts that plan and teach them, and says what the series leaves
out; it is written by `python -m videos.economics.reading` from the syllabus and the built parts, and
`tests/economics/test_reading.py` keeps it true. The spines (each part's reference card names its
own, and the syllabus lists them with the papers):

| Tier | Main texts |
|---|---|
| Principles | Mankiw, *Principles of Economics*; Krugman & Wells; Acemoglu, Laibson & List; The CORE Team, *The Economy*; Heilbroner, *The Worldly Philosophers* |
| The major | Varian, *Intermediate Microeconomics*; Nicholson & Snyder; Jones, *Macroeconomics*; Blanchard, *Macroeconomics*; Stock & Watson, *Introduction to Econometrics*; Angrist & Pischke, *Mostly Harmless Econometrics*; Osborne, *An Introduction to Game Theory*; Krugman, Obstfeld & Melitz, *International Economics*; Mishkin; Cabral, *Introduction to Industrial Organization*; Borjas, *Labor Economics*; Gruber, *Public Finance and Public Policy*; Ray, *Development Economics*; Weil, *Economic Growth* |
| Graduate micro | Mas-Colell, Whinston & Green; Kreps, *Microeconomic Foundations*; Jehle & Reny; Fudenberg & Tirole, *Game Theory*; Osborne & Rubinstein; Bolton & Dewatripont, *Contract Theory*; Krishna, *Auction Theory*; Milgrom, *Putting Auction Theory to Work*; Roth & Sotomayor, *Two-Sided Matching*; Börgers, *An Introduction to the Theory of Mechanism Design*; Tirole, *The Theory of Industrial Organization* |
| Graduate macro | Romer, *Advanced Macroeconomics*; Ljungqvist & Sargent, *Recursive Macroeconomic Theory*; Stokey, Lucas & Prescott; Acemoglu, *Introduction to Modern Economic Growth*; Galí, *Monetary Policy, Inflation, and the Business Cycle*; Woodford, *Interest and Prices*; Walsh, *Monetary Theory and Policy*; Obstfeld & Rogoff, *Foundations of International Macroeconomics*; Pissarides, *Equilibrium Unemployment Theory*; Cochrane, *Asset Pricing*; Freixas & Rochet, *Microeconomics of Banking* |
| Econometrics and computation | Hayashi, *Econometrics*; Wooldridge, *Econometric Analysis of Cross Section and Panel Data*; Hansen, *Econometrics*; Hamilton, *Time Series Analysis*; Kilian & Lütkepohl, *Structural Vector Autoregressive Analysis*; Train, *Discrete Choice Methods with Simulation*; Judd, *Numerical Methods in Economics*; Sargent & Stachurski, *Quantitative Economics* |
| The fields | Feenstra, *Advanced International Trade*; Cahuc, Carcillo & Zylberberg, *Labor Economics*; Atkinson & Stiglitz, *Lectures on Public Economics*; Salanié, *The Economics of Taxation*; Banerjee & Duflo, *Poor Economics*; Persson & Tabellini, *Political Economics*; Dhami, *The Foundations of Behavioral Economic Analysis*; Fujita, Krugman & Venables, *The Spatial Economy*; Nordhaus, *A Question of Balance*; Jackson, *Social and Economic Networks*; the North-Holland *Handbooks* |
| Practice | Blinder, *Central Banking in Theory and Practice*; Boardman et al., *Cost-Benefit Analysis*; Davis & Garcés, *Quantitative Techniques for Competition and Antitrust Analysis*; Talluri & van Ryzin, *The Theory and Practice of Revenue Management*; Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments*; Lazear & Gibbs, *Personnel Economics in Practice*; Athey & Luca (2019) |
| History | Smith, Ricardo, Marx, Marshall and Keynes in the original; Blaug, *Economic Theory in Retrospect*; Friedman & Schwartz, *A Monetary History of the United States*; Kindleberger, *Manias, Panics, and Crashes*; Clark, *A Farewell to Alms*; Koyama & Rubin, *How the World Became Rich*; Warsh, *Knowledge and the Wealth of Nations*; Tooze, *Crashed* |

## Standards (as *AI, Built* and *Psychology, Built*, plus economics' own)

* **Every number is real.** Computed in the part's `compute.py` and cached in `.cache/econN/`, loaded from the
  Data Room with its source and vintage, or cited. Island results are labelled `simulated`.
* **Every empirical claim carries its design.** What varied, why that variation is as good as random (or why it
  is not), the estimate with its interval, and its Dial. A regression coefficient is never shown without the
  picture of where its variation comes from.
* **Every model is confronted with data.** A model on screen is solved and set beside the fact it is meant to
  explain, and the screen shows where it fits and where it fails. Calibrated numbers are labelled as
  calibrated, estimated numbers as estimated.
* **What is and what ought.** A card marks the moment a part moves from what a policy does to whether it
  should be done, and names the value judgment that the second step needs.
* **Each side gets its best case.** On open controversies (the minimum wage, the size of the multiplier, the
  costs of trade, immigration and wages, what caused the inflation of 2021–23, how much to discount the
  future, whether market power has risen, how far to redistribute) the strongest version of each position is
  presented with its evidence, in its defenders' words where possible, and the narration says that the
  question is open. The series takes no party's side and no school's.
* **Not advice.** The films are education. Nothing in them is investment, tax or legal advice, and the parts
  that touch on personal finance say so.
* **Care.** Poverty, unemployment, discrimination, famine and crisis are things that happen to people; they
  are shown with the people in view. Group comparisons are shown with full distributions and with what the
  data cannot say.
* **Bilingual.** English and Chinese, as the other series: `narration_zh.json`, `economics_text_zh.json`,
  `ECONOMICS_ZH_GUIDE.md`. The series is written for both audiences from the start: Xiaogang's contract,
  the first paper money in Song-dynasty Sichuan, the Needham question, the dual-track reforms, the Huai River
  heating line and the growth of Shenzhen are in the plan as cases, not added in translation.

## Shared code

`explainer/economics/` holds what every part shares (the modules for later parts are added as they are built):

| Module | What it is |
|---|---|
| `agora/` | Agora, the economy: one module per mechanism (`consumer`, `firm`, `market`, `ge`, `games`, `oligopoly`, `info`, `contracts`, `auctions`, `matching`, `growth`, `household`, `assets`, `search`, `money`, `bank`, `islm`, `dp`, `nk`, `fiscal`, `open`, `trade`, `city`, `labour`, `tax`, `io`, `hetero`, `network`, …), each tested against an independent reference |
| `island.py` | the Island: the seeded world, its cast, its planted truths and its history from part to part; always tagged *simulated* |
| `facts.py` | the Facts: the forty regularities, each with its data, its source and the test Agora must pass |
| `dials.py` | the Dials: one validated row per number, with estimates, designs, sources and the date checked; `tools/check_dials.py econN` is its gate |
| `data/` | the Data Room: frozen, cited extracts and their loaders, with source, licence and vintage (`data/SOURCES.md` registers every dataset); passages and tables transcribed from publications in `data/tables.py` |
| `metrics.py` | the econometrics the series needs beyond statkit: BLP, dynamic discrete choice, GMM with simulated moments, SVAR identification schemes, local projections |
| `score.py` | the computed score: the scissors theme, chapter stings, the bed, the data melodies |
| `__init__.py`, `viz.py`, `style.py` | chapter cards with the timeline and scale strips, the Tableau, the game stage, dial and fact cards, the instruments, the palette |

Tests will be in `tests/economics/`. The code reuses `explainer.stats.kit` (`quasi`, `causal`, `ts`, `optim`,
`ols`, `ppl`, `survey`), `explainer.quant.house` and `explainer.quant.data` (asset pricing and market data),
`explainer.ai.autodiff` (deep solution methods), `explainer.psychology.psyche` (prospect theory and the
decision models) and `explainer.music.monochord` (the score). The course material follows `videos/coursekit`
(a course entry, a lab and an interactive per part); for this series the interactive is the part's game,
played against Agora's agents.

## Decisions taken

Building began on 2026-11-18 on the defaults (the first option in each). Details and open risks are in the syllabus,
§8. The Chinese edition (decision 5) is planned but not yet made: Part 1 is English for now.

1. **Scope: sixty-eight parts, about 63 hours at the planned lengths.** The alternative is a first season of
   Parts 1–50 (the degree, about 46 hours) with Acts X–XII committed to later; or a shorter first season of
   Parts 1–18 (the micro course, about 16 hours), which stands on its own.
2. **Length: 30–60 minutes, most at 45–55**, as asked.
3. **Order: micro, then macro, then the fields.** The alternative puts money and the cycle earlier (Acts V–VI
   after Act I), which is what most people come to economics for; it costs the macro parts their foundations.
   Part 1 previews the whole series either way.
4. **Video names `econ1` … `econ68`** in `videos/economics/` (the series key is `economics`, the prefix
   `econ`, as `psych` is to `psychology`).
5. **Bilingual from the start**, like the recent series, or English first.
6. **The watching experience** (cold opens, the Island as a serial, Play it, the intermission and its data
   films, *Called it?*, the computed score): all on by default. Each can be turned off without touching the
   rest.
7. **Names:** Agora, the Island, the Tableau, the Facts, the Dials, the Data Room.
8. **Finance stays with *Quant, Built*.** This series has one part on asset prices (23), one on banks (26) and
   one on crises (33), and points to that series for derivatives, portfolios and market microstructure.
   Econometric method stays with *Statistics, Built* (Parts 35–38 and 62 there); this series teaches
   identification inside economic questions and adds only what is specific to economics (Parts 4, 54, 55).
