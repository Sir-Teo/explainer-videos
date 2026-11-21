# Economics, Built: the syllabus (plan of record, draft 1)

Goal: a university education in economics on video, from the first lecture of a principles course to the level
of a first-year PhD core exam and a field paper, followed by the curriculum that central banks, ministries,
courts and companies work from. It aims to be **as comprehensive as the textbooks, as technical as a graduate
core, as practical as a working economist's knowledge, and as honest about its evidence as the field has
learned to be**. It is told as one story, *who feeds Paris?* ([README](README.md)). Each part runs **30–60
minutes**, most at 45–55, and its content decides where in that range it lands. Sixty-eight parts come to about
**63 hours** at the planned lengths: a degree in fifty parts (46 hours), a graduate core in six, the practice in
six and a research tier in six.

The plan has the shape of a degree plus a career:

- **Act I** is principles, measurement and the logic of evidence (Mankiw; CORE; Stock & Watson; Angrist &
  Pischke).
- **Acts II–IV** are microeconomics, from intermediate to the graduate core (Varian; Mas-Colell, Whinston &
  Green; Kreps; Fudenberg & Tirole; Bolton & Dewatripont; Krishna; Roth & Sotomayor).
- **Acts V–VI** are macroeconomics, from intermediate to the graduate core (Jones; Blanchard; Romer; Acemoglu;
  Ljungqvist & Sargent; Galí; Woodford).
- **Act VII** is international economics and economic geography (Krugman, Obstfeld & Melitz; Obstfeld & Rogoff;
  Feenstra; Fujita, Krugman & Venables).
- **Act VIII** is labour and public economics (Borjas; Cahuc, Carcillo & Zylberberg; Gruber; Atkinson &
  Stiglitz; Salanié).
- **Act IX** is the field courses: industrial organization, behavioural economics, development, political
  economy, environmental economics and the economics of the family, and ends on the degree's capstone (Tirole;
  Dhami; Ray; Banerjee & Duflo; Persson & Tabellini; Nordhaus; Becker).
- **Act X is the graduate core's toolkit**: recursive and numerical methods, heterogeneous agents, information
  economics, structural and macro-econometrics (Stokey, Lucas & Prescott; Judd; Train; Hayashi; Kilian &
  Lütkepohl), and ends on a core exam.
- **Act XI is the practice**: forecasting and nowcasting, policy analysis and scoring, antitrust, pricing,
  platforms, and the economics of the firm.
- **The research tier** runs through the whole series and ends in its own act. Every part closes with a
  *Frontier* chapter (§1.1). **Act XII** then covers networks, machine learning in economics, the economics of
  AI, geoeconomics, the field's own reform, and how research is done.

Each part's **Reading** line names the textbooks, the classic papers and the recent papers it follows. Each
part's **In practice** line names the jobs and decisions it maps to. §2.8 maps the series onto a degree and onto
the roles graduates fill.

**Every date, number and attribution in this draft is written from memory of the literature and is to be treated
as (verify) until its part's frontier sweep (§1), whether or not it is marked.** The marks single out the ones
most likely to be wrong.

## 1. The standard every part meets

The standard is *AI, Built*'s ([`../ai/SYLLABUS.md`](../ai/SYLLABUS.md) §1 and
[`../ai/LECTURE_GUIDE.md`](../ai/LECTURE_GUIDE.md)), with *Computer Science, Built*'s research tier and
*Psychology, Built*'s study cards and evidence gate, plus the rules specific to economics, marked **(Econ)**.

**A part is one story.** It opens on a hook that a person off the street would stop for: cigarettes used as
money in a prison camp, a napkin with a curve on it, a bank emptied from a phone in an afternoon. It then:

1. shows the puzzle and **puts the viewer in it** (Play it);
2. tells how it was found (the people, the year, the argument, the dead ends);
3. builds the model: who chooses, what they want and face, the equilibrium derived step by step, and the code
   that solves it;
4. confronts the model with data, and shows where it fits and where it fails;
5. enters the numbers in **the Dials**: how big, how sure, identified how;
6. closes with *In practice*, the *Frontier*, and the problem the next part opens with.

A chapter that does not serve the part's story is cut, or moved to the part it serves.

**A chapter is a lecture segment of 3–4 minutes,** twelve to sixteen to a part. It runs in this order:

1. A motivating question, episode or picture, drawn.
2. A definition card, in words and then in symbols.
3. The derivation or the empirical design on screen, every step, each with a margin reason ("first-order
   condition", "envelope theorem", "market clearing", "the instrument moves supply only", "parallel trends").
4. A computed experiment: Agora solved, a fit to Data Room data, or a method run on the Island.
5. A *pause-and-predict* question. **(Econ)** Predictions are about what happens: "who ends up paying the
   tax?", "which way does the exchange rate jump?".
6. The takeaway, with a forward link (a payoff card).

**Per part:**
- An objectives card.
- Definition, model, theorem, study and history cards. **(Econ)** A *study card* always shows the design (what
  varied and why), the sample, the estimate with its interval, and the Dial it moves.
- **(Econ)** One **Play it** segment (§2.7) in the first third.
- **(Econ)** One or more rows of **the Dials** (§2.5) and at least one of **the Facts** (§2.4), with Agora's
  column filled.
- **(Econ)** One **Called it?** card (§1.3) where the part has a dated prediction to score.
- **(Econ)** An **is / ought** card at the point the part turns from what a policy does to whether to do it.
- A problem set: 5–6 problems, about 90 s on screen, with full solutions in the part's README. The mix: a
  derivation, a model computation with Agora, a design critique ("what is the identifying assumption, and what
  would break it?"), a data problem on the Data Room or the Island, a policy problem ("advise the minister"),
  and one research problem (★, §1.1).
- A reference card: textbooks, the classic papers, recent papers.
- An *In practice* card in the outro.
- A *Frontier* chapter before the outro (§1.1).

**The history thread.** Every part opens with its era (2–3 min), lit on the timeline strip (1750–2030). Every
idea is credited with its people and year, its dead ends included: the wages fund, the labour theory of value,
the Soviet material balances, the hydraulic Keynesianism of the 1960s, monetary targeting, the Great
Moderation's self-congratulation. Schools outside the mainstream (Marxian, Austrian, post-Keynesian,
institutionalist, complexity) appear where their argument bears on the part's question, with their best case.

**Numbers and claims.**
- Computed numbers come from the part's `compute.py`, cached under `.cache/econN/`. Narration that states a
  result is an f-string over the cached data, and branches on it when the verdict depends on the outcome (a
  model matches a moment or misses it, a method recovers the Island's truth or does not).
- **(Econ)** Data are loaded through the Data Room with source, licence and vintage; each film states the date
  its data were frozen. Where a first release was later revised, the film can show both (ALFRED).
- **(Econ)** Published estimates are cited on screen with design, sample and interval, and enter the Dials.
- **(Econ)** Island results are labelled `simulated`. A simulation shows what a method can and cannot recover;
  it is never offered as evidence about the world.
- **(Econ)** A calibrated parameter is labelled `calibrated` with its target; an estimated one `estimated` with
  its standard error.
- Schematics are labelled `schematic` and made-up examples `illustrative`.
- `assert`s in `compute.py` are for invariants: Walras's law holds to tolerance, Euler-equation errors are
  below a bound, an estimator recovers planted parameters, revenue equivalence holds in simulation.
- CPU budget: at most 1 h per part by default, seeded and resumable. Named exceptions (the heterogeneous-agent
  economies of Parts 52 and 55, BLP in Part 43, dynamic oligopoly in Part 44, the quantitative trade and
  spatial models of Parts 36, 37 and 66, deep solvers in Part 64) get up to 6 h.

**Frontier sweep.** Before a part is written, its literature is checked against primary sources up to the
writing date: the *Journal of Economic Literature*, the *Journal of Economic Perspectives*, the *Annual Review
of Economics*, the *Handbooks*, the top general and field journals, NBER and CEPR working papers, and the
relevant central-bank and agency publications. Results the plan relies on that are recent or disputed are
marked **(verify)** below. **(Econ)** Because estimates move, each Dial row carries the date it was checked.

**Bilingual standard (as *AI, Built*).** Every narration line has its entry in `narration_zh.json`, or in the
part's `zh_lines.py` template when the line is computed. Every on-screen string is in
`economics_text_zh.json`, and `tools/collect_text.py --check econN` is clean. `ECONOMICS_ZH_GUIDE.md` is the
glossary and follows the standard terms of Chinese economics (边际效用, 一般均衡, 纳什均衡, 逆向选择, 道德风险,
全要素生产率, 流动性陷阱, 菲利普斯曲线, 工具变量, 双重差分).

**Gates per part:** `tools/lecture_length.py` (floor 30 min; a part that would pass 60 is split or trimmed),
`contact_sheet.py`, `dead_air.py`, `collect_text.py --check`, `check_narration.py`, `zh_lines.py --verify`,
`check_course.py economics N`, the part's `tests/economics/test_*.py`, and **(Econ)** the Dials gate,
`tools/check_dials.py econN`: every estimate a part shows (each author and year in a source tag, each Data
Room dataset its scenes use) has a Dial row with its design, sources and the date checked, or a `dials.shown`
declaration that says why it has none.

### 1.1 The research tier

Every part ends its content with a **Frontier** chapter (4–7 minutes), written for a PhD student. It does four
things:

1. **What is not known**, stated precisely: the competing models and the evidence that would separate them.
2. **The best current evidence**, with dates: the cleanest design, the largest sample, the most recent survey.
3. **Two or three recent papers** and what each changed, checked in the frontier sweep.
4. **A research problem (★)** in the problem set: open-ended, possibly open. The README says what is known,
   how a researcher would attack it, and which Agora module or Data Room dataset is the place to start.

### 1.2 Care and balance **(Econ)**

Economics is argued about in public, with money and votes at stake. These rules bind every part.

- **Positive before normative.** The series says what a policy does, to whom, with what confidence. The *is /
  ought* card names the value judgment (a welfare weight, a discount rate, a view of desert) that turns an
  effect into a recommendation, and shows how the answer changes when the judgment does.
- **No party and no school.** On each controversy listed in the README the strongest case of each side is
  given, with its evidence, by the same narrator in the same tone. Living politicians are named only as
  historical actors in a dated event.
- **Not advice.** No investment, tax, legal or career advice. Parts 7, 22, 23, 26 and 42 touch personal
  finance and open with a card that says so.
- **People in view.** Unemployment, poverty, famine, debt and displacement are shown with what they did to the
  people who lived them (Sen on the Bengal famine, the Jarrow march, the *xiagang* layoffs of the 1990s), not
  only as areas under curves.
- **Group comparisons** (sex, race and ethnicity, class, country) are shown with the full distributions, the
  design that separates a gap from its causes, and what the data cannot show.
- **The profession's own record** is told plainly: the advice that failed (shock therapy as first applied,
  the pre-2008 view of financial regulation), the conflicts of interest, and who has and has not been in the
  room.
- **Play it never scores a person.** The games show the viewer a phenomenon and the distribution of what people
  do. They do not rate the viewer's rationality or risk tolerance.
- **No harm in the games.** Nothing is staked, nothing is stored or sent, and nothing deceives the viewer for
  longer than the game.

### 1.3 Made to be watched **(Econ)**

The series is measured by whether people finish the parts. These are rules, checked at the contact-sheet review.

- **Cold open:** 60–90 s before the title card, one scene with a person, a place, a date and something at
  stake. No definitions, no agenda.
- **The question card** follows the title and its text stays in the corner of every chapter card.
- **Play it** is placed before the model that explains it, within the first fifteen minutes.
- **Four-minute rule:** every chapter ends on a pause-and-predict; no derivation runs past 90 s without the
  picture it describes moving on the same screen; no chapter is only text.
- **The Island serial:** each part has an Island scene in the hook (the cast meets the problem) and in the
  recap (they live with the solution); the cast, the map and the colours persist (§2.2).
- **Called it?:** one card per part where a dated prediction exists: who predicted what, when, on what model,
  and what happened. Right and wrong calls are both shown; a list is kept in `explainer/economics/calls.py`.
- **The intermission:** near the midpoint, 30–45 s without narration: a data film under the score (§3), then a
  single card, "the story so far", with the question and what has been established.
- **Places:** at most one 20-second drawn vignette of a real place per part, where the story has one.
- **The score** (`explainer/economics/score.py`, mixed by `tools/build.py` through the music-stem path, as
  *Psychology, Built*'s is): computed on Monochord, nothing recorded. Four cues placed from the film's own
  timeline:
  - *the scissors*, the theme, under the hook: two voices in contrary motion from an octave apart, crossing on
    one note;
  - *a sting* at each chapter card: the two voices one scale step closer than at the last card, so the ear
    hears the part converge; each act has its own mode and timbre;
  - *the bed* under Play-it pauses and long animations: a quiet open chord that breathes;
  - *the data melody* in the intermission: the part's own series mapped to the scale (one bar a year or a
    quarter), over the bed; and *the close* in the outro, where the two voices meet.
  Narration is mastered to −16 LUFS; the score sits 8 to 18 LU below it. `--no-score` leaves it out.
- **The ending:** the recap answers the question card in one sentence, and the last scene is the next part's
  problem arriving on the Island.

## 2. The devices

### 2.1 Agora, the economy

`explainer/economics/agora/` is a Python library (numpy and scipy; no manim), tested in `tests/economics/`, that
gains one module per part. Rules:

- **One interface.** Every model is an object with `solve()` returning an equilibrium (prices, allocations,
  policy functions or strategies) and `simulate(shocks)` returning data in the same tidy form the Data Room
  returns, so that every estimator in the series runs unchanged on real data and on the Island.
- **Independent references.** Each module's tests compare it with something it did not compute itself: a
  closed form, a published table reproduced from its published calibration (Aiyagari's Table II, Mehra and
  Prescott's bound, Krusell and Smith's R², the textbook New Keynesian impulse responses in Galí), QuantEcon's
  lectures, statkit, or a second algorithm for the same problem.
- **Reuse on screen.** A later part imports an earlier module and says so with a payoff card.
- **Modules, by part** (the list in §4 is authoritative): `consumer` (5–7), `firm` (8), `market` (2), `ge`
  (9), `pricing` (10), `games` (11), `oligopoly` (12), `info` (13), `contracts` (14), `public` (15),
  `auctions` (16), `matching` (17), `choice` (18), `malthus` and `growth` (19–21), `household` and `olg` (22),
  `assets` (23), `search` (24), `money` (25), `bank` (26), `islm` (27), `expectations` (28), `dp` and `rbc`
  (29), `nk` (30), `cb` (31), `fiscal` (32), `credit` (33), `open` (34), `trade` (35–36), `city` (37),
  `labour` (38–39), `distribution` (40), `tax` (41), `insurance` (42), `io` (43–44), `behave` (45), `village`
  (46), `politics` (47), `climate` (48), `family` (49), `solve` (51), `hetero` (52), `persuade` (53),
  `estimate` (54), `macrometrics` (55), `nowcast` (57), `microsim` (58), `merger` (59), `revenue` (60),
  `platform` (61), `org` (62), `network` (63), `learn` (64), `automation` (65), `tradewar` (66), `field` (67).

### 2.2 The Island

`explainer.economics.island` runs Agora as one seeded world that persists across the series.

- **The cast.** Crusoe (Part 1), then Friday, then a village of a dozen named households and a handful of
  firms (the fishing company, the coconut grove, the boatyard, the ferry), a bank, a council, a central bank,
  and from Part 34 a second island with its own currency. Each is one glyph, one colour and one name on screen
  for sixty-eight parts. From Part 22 the named cast sits inside a population (10,000 households, then 100,000
  in Part 52) drawn from it.
- **Planted truths.** Every structural parameter of the Island (demand and supply elasticities, the returns to
  schooling, the matching elasticity, price stickiness, the monetary rule and its shocks) is set in code and
  can be shown as a dashed green line. Methods are graded against it: Part 4 recovers a demand curve by OLS
  (wrong) and by an instrument (right); Part 38 runs a minimum-wage border design; Part 55 identifies a
  monetary shock five ways.
- **A history.** The Island's past is saved from part to part, so the recession of Part 27, the inflation of
  Part 28 and the bank run of Part 26 are in the data that Part 55's econometrician is handed.
- **Always `simulated`.** The tag is on every Island plot. The Island teaches what a method can recover; the
  world is in the Data Room.

### 2.3 The Tableau

`tableau_map` is the series map: five sectors (households, firms, banks, the government, the rest of the
world) joined by flows of goods, labour, money and claims, drawn as Phillips drew it, as plumbing. Part 1 shows
it sealed. Each part opens one pipe or one tank (the goods market in Part 2, the labour market in 24 and 38,
the banking system in 26, the central bank in 31, the foreign sector in 34) and the chapter card lights the
part of the machine that chapter is about. Part 68 shows what is still sealed.

### 2.4 The Facts

`explainer.economics.facts`: about forty regularities with their data, sources and Agora's test. A fact is
introduced with **your guess** first (a pause), then the data, then, in the part that builds the mechanism,
Agora's column. Draft list (to be fixed in Phase 0):

- *Households and firms:* Engel's law; demand curves slope down (and the one that did not); consumption is
  smoother than income; saving rises with lifetime income; firm sizes and city sizes follow Zipf; productivity
  differs two to one among plants in one industry; most prices change less than once a quarter.
- *Markets:* double auctions converge in a few rounds; the law of one price holds for gold and fails for
  haircuts; the winner's curse in common-value auctions; pass-through of costs is incomplete.
- *Growth:* Kaldor's six facts; income per head was flat for millennia; conditional convergence; the labour
  share was stable, then fell; the price of light.
- *Cycles:* Okun's law; the Beveridge curve; investment is about three times as volatile as output and
  consumption less volatile; hours are procyclical; the response of output to a monetary shock is
  hump-shaped and peaks after a year or more; inflation is persistent; long expansions, short recessions.
- *Money and finance:* inflation tracks money growth across countries in the long run and not in the short;
  the equity premium; returns are hard to predict and volatility is not; the yield curve inverts before
  recessions; credit booms precede crises.
- *The world:* gravity; exchange rates are a random walk at short horizons and return to purchasing power
  parity over years; rich countries trade similar goods with each other; exporters are few, big and
  productive.
- *Distribution:* log wages are roughly linear in schooling; top incomes and wealth have Pareto tails; the
  Gatsby curve; the gender gap opens at the first child.

### 2.5 The Dials

`explainer.economics.dials`: one validated row per number. A row has the quantity and its units; each estimate
with author, year, design (`RCT`, `IV`, `RD`, `DiD`, `event study`, `structural`, `calibration`, `survey`,
`narrative`), sample and interval; the status (`settled within a range`, `contested`, `depends on the
setting`, `not identified`); what changes in policy across the range; and the date checked. A *dial card* on
screen shows the estimates as ticks on one axis, coloured by design. Draft list of dials and the parts that
enter them:

the price elasticity of demand for a few staples (2, 6) · the elasticity of intertemporal substitution and
risk aversion (7, 23) · the output elasticity of capital (8, 20) · markups (10, 43) · the return to a year of
school (38) · labour-supply elasticities: Hicksian, Frisch, extensive (38, 41) · the employment elasticity of
the minimum wage (38) · the elasticity of substitution between skilled and unskilled labour (39) · the
intergenerational elasticity of income (40) · the elasticity of taxable income (41) · the duration elasticity
of unemployment benefits (42) · the marginal propensity to consume (22) · the matching elasticity (24) · the
frequency of price changes (30) · the slope of the Phillips curve (28, 30) · the sacrifice ratio (28) · the
interest elasticity of money demand (25) · the effect of a 100-basis-point shock on output and prices (31, 55)
· the government-spending and tax multipliers (32) · the neutral real rate (31) · the trade elasticity (36) ·
the pass-through of tariffs and of exchange rates (34, 36, 66) · the agglomeration elasticity and the
elasticity of housing supply (37) · the return to capital for small firms in poor countries (46) · the value
of a statistical life (18, 58) · the social discount rate and the social cost of carbon (48, 58) · the price
elasticity of gasoline and of electricity (48) · loss aversion and present bias (45) · the productivity
effect of generative AI on a task (65).

### 2.6 The Data Room

`explainer.economics.data`, registered in `explainer/economics/data/SOURCES.md` with licence, retrieval date
and checksum. Open data are fetched on first use and checked by SHA-256 (as `explainer.psychology.opendata`);
nothing large is committed. Draft sources:

- *Long run:* Maddison Project Database; Penn World Table; Clark's English wages and prices; Allen's real
  wages; the Jordà–Schularick–Taylor Macrohistory Database; Our World in Data's assembled series (each traced
  to its primary source).
- *United States:* FRED and ALFRED; BEA national accounts and input–output tables; BLS (CPS, CES, JOLTS, CPI
  microdata summaries); the Survey of Consumer Finances; the Federal Reserve's historical forecasts
  (Greenbook), the Survey of Professional Forecasters.
- *World:* World Bank WDI and the Poverty and Inequality Platform; OECD; IMF IFS and WEO vintages; BIS; UN
  Comtrade and CEPII's gravity data; the World Inequality Database; Eurostat; the National Bureau of
  Statistics of China.
- *Historical tables, transcribed with source:* Engel (1857); Giffen-era bread prices; Douglas (1928); Phillips
  (1958); Kuznets (1934); Friedman and Schwartz (1963); Cagan (1956); Nordhaus's light (1996); Radford (1945).
- *Replication packages* (used under their licences, cited): Card and Krueger (1994); Angrist and Krueger
  (1991); Acemoglu, Johnson and Robinson (2001); Autor, Dorn and Hanson (2013); Berry, Levinsohn and Pakes's
  automobile data; Nevo's simulated cereal data; Rust's bus data; Mankiw, Romer and Weil (1992); the Oregon
  Health Insurance Experiment public-use files; the PROGRESA evaluation data.
- *Already in the repository:* *Statistics, Built*'s Museum (NSW job training, Card and Krueger's means, the
  Prop 99 panel, Mroz's women, US macro data) and `explainer.quant.data`.

Restricted microdata (IPUMS extracts, PSID, administrative tax data) are cited and summarized, not stored.

### 2.7 Play it

One game per part. In the film: a framed stage, the rules in one card, a countdown, a pause to decide, then the
reveal: the distribution of what subjects did in the published experiment, the equilibrium prediction, and the
gap between them. On the course site the interactive is the game, played against Agora's agents on a shared
kit (`course/site/widgets/00_games.js`, `EB.game`: a pit market, a sealed-bid form, a matrix game, a
slider-and-outcome loop, a matching form), with nothing stored or sent; `tools/check_course.py` plays a
scripted player against it. The games that recur: the pit market (Parts 1, 2, 9, 25), the guessing game (11,
28, 53), the sealed bid (16, 61), the bank queue (26, 33), the central banker's chair (31, 34), the minister's
budget (32, 41, 46, 58).

### 2.8 The degree and the practice

| A course in a degree | Parts |
|---|---|
| Principles of economics | the opening chapters of 1–4, 9, 15, 20, 25–28, 35 |
| Intermediate microeconomics | 5–15 |
| Game theory; information and market design | 11, 13–14, 16–18, 53 |
| Intermediate macroeconomics | 3, 19–34 |
| Econometrics (with *Statistics, Built* 12, 35–38) | 4, 54, 55 |
| Money and banking; international economics | 25–26, 31, 33; 34–36 |
| Labour; public; industrial organization | 38–40; 41–42, 58; 43–44, 59 |
| Development; political economy; environmental; behavioural; urban; economic history | 46; 47; 48; 45; 37; 19 and the history thread |
| PhD micro core (MWG) | the model chapters of 5–18, and 53 |
| PhD macro core (Ljungqvist & Sargent; Galí) | the model chapters of 20–33, and 51–52 |
| PhD econometrics for economists | 54–55 with *Statistics, Built* Stages III–IV |

| A job | Parts |
|---|---|
| Central-bank economist | 25–31, 33, 52, 55, 57 |
| Treasury, budget office, regulator | 32, 41–42, 48, 58 |
| Competition economist, expert witness | 10, 12, 43–44, 59 |
| Tech and marketplace economist | 16–17, 54, 60–61, 64 |
| Pricing and revenue | 6, 10, 60 |
| Development practitioner, evaluator | 4, 46, 58 |
| Macro strategist, forecaster | 28–34, 55, 57 (and *Quant, Built*) |
| Management and strategy | 8, 12, 14, 62 |

## 3. Visual instruments

`explainer/economics/viz.py`, built as parts need them (the part that first builds each is in brackets):

- **`MarketCross`** [2]: demand and supply assembled from reservation prices, with surplus areas, wedges,
  controls and shifts as animations; the pit market's price path beside it.
- **`IndifferenceMap`**, **`BudgetLine`**, **`PriceOfferCurve`** [5, 6]: the consumer's problem, with the demand
  curve traced in a linked panel as the budget line swings; Slutsky's decomposition as two moves.
- **`Isoquants`** and **`CostCurves`** [8]; **`EdgeworthBox`** with the contract curve, the core and a price
  line that gropes [9]; **`SimplexMap`** for fixed points and Scarf's cycle [9].
- **`GameMatrix`**, **`GameTree`**, **`BestResponsePlane`** [11, 12]; **`AuctionRoom`** (bidders with values on
  cards, the clock, the payment) [16]; **`MatchingBoard`** (proposals, holds and rejections) [17].
- **`TAccounts`** [25, 26]: balance sheets as linked boxes; every operation moves both sides.
- **`Tableau`** [1] and **`FlowSankey`** [3]: the circular flow and the national accounts as widths.
- **`SolowDiagram`**, **`PhaseDiagram`** (nullclines, the saddle path, shooting) [20, 34];
  **`PolicySurface`** and **`ValueIteration`** [29, 51]; **`ImpulsePanel`** (model orange, data white, bands)
  [29–31, 55]; **`DistributionFlow`** (a wealth distribution moving under a policy function) [52].
- **`IdentificationPicture`** [4]: the design drawn before the estimate: `border`, `cutoff`, `lottery`,
  `instrument`, `event`; then the same design on the Island with the truth in dashed green.
- **`DialCard`**, **`FactCard`** (your guess, the data, Agora), **`CallCard`** (Called it?), **`StudyCard`**,
  **`IsOughtCard`** [1–4].
- **`WorldMap`** (choropleths and trade flows) [3, 36], **`CityMap`** (rings, a checkerboard, a rent gradient)
  [37], **`NetworkGraph`** (input–output, interbank) [63].
- **`LorenzParade`** [40], **`BeveridgePlane`** [24], **`YieldCurve`** [31], **`TaxSchedule`** with bunching
  [41].
- **Data films** (`data_film`): `two_hundred_years` (income and life expectancy by country), `curve_breathing`
  (the yield curve by month), `lights` (night lights), `trade_web`, `price_of_light`, `parade`,
  `cities_grow`. Each is 30–45 s, plays under the data melody, and carries its source.
- The diagram instruments shared with *Psychology, Built* (`point_cards`, `flow_chain`, `quadrant`, `pyramid`,
  `rings`, `theory_card`, `verdict_row`) for ideas that are not curves.

Palette: data white, Agora orange, the Island's truth dashed green; demand blue, supply amber; households
teal, firms amber, banks violet, government red, the rest of the world grey-blue; a treated unit filled, a
control hollow; a prediction purple and its miss red.

## 4. Part by part

Minutes in brackets are targets. Each entry gives the part's question and story, its chapters (0 is the hook;
the last three are always the Dials, *In practice* and the *Frontier*, and are listed only where they need a
note), what Agora gains, the game, the Dials and Facts it enters, the prediction it scores, and its reading.
Chapter lists are a first draft: each is locked after the part's frontier sweep.

## Act I · The Question

### Part 1 · Who Feeds Paris? (~48)
*Question:* how do millions of strangers, none of them in charge, manage to feed a city, and what does it take to
study that?
*Story:* Bastiat's wonder at a sleeping Paris, 1845, and the Queen's question at the LSE, 2008. One castaway
shows what an economic problem is; a second person shows what trade is; a pin factory shows why it makes
everyone richer; and a line that was flat for ten thousand years and then was not shows what is at stake. The
part ends with the map of the series, sealed.
0. Cold open: Paris asleep, 1845; the title; the Queen at the LSE; the three questions; objectives.
1. Play it: a pit market in ninety seconds (Chamberlin 1948; Smith 1962). You hold one card. Watch the price.
2. Crusoe: scarcity, the production frontier, opportunity cost as a slope; the choice at the margin.
3. Friday arrives: absolute and comparative advantage in one two-by-two table; the gains drawn.
4. The pin factory (Smith 1776, eighteen operations, 48,000 pins): specialization and the extent of the market;
   *I, Pencil* (Read 1958).
5. Prices as messages: Hayek (1945) and the tin example; what a planner would need to know.
6. Incentives: when they work and when they bite back (transported convicts paid per arrival, 1790s; a
   fine for late parents, Gneezy and Rustichini 2000).
7. The long view: income per head, year 1 to now (Maddison); the hockey stick; a first data film.
8. What a model is: a map at the wrong scale on purpose (Robinson; Rodrik 2015); assumptions that matter and
   assumptions that do not; positive and normative; the first *is / ought* card.
9. The order failing: 1929 and 2008 in four charts; what the British Academy's letter said (2009).
10. Quesnay's *Tableau* (1758) and Phillips's machine (1949): the series map, sealed; the acts.
11. How we will know: the Facts, the Dials, the Island. 12. In practice: what economists are hired to do.
13. Frontier: how much of the order is designed after all (firms, platforms, central banks)?

*Agora:* `market` (a pit of traders with values and costs) and a one-person economy (frontier, preferences, the
optimum). The Tableau, sealed. The Island: Crusoe and Friday.
*Play it:* the pit market; on the site, twelve rounds against zero-intelligence traders, with the price path.
*Facts:* income per head was flat for millennia; double auctions converge.
*Called it?* the Survey of Professional Forecasters' call for 2009, made in November 2008 (built; the draft's
call, Smith's pin arithmetic against a modern count, Pratten 1980, suits Part 8 better).
*In practice:* the series' map of jobs (§2.8). *Frontier:* the boundary between markets and planning inside the
economy (Coase 1937; Simon 1991, "Organizations and Markets").
*Reading:* Smith 1776, Book I chs 1–3; Bastiat 1845; Hayek 1945; Chamberlin 1948; Smith 1962; Rodrik,
*Economics Rules*; Heilbroner; CORE, *The Economy*, units 1–2; Mankiw chs 1–3.

### Part 2 · The Scissors (~52)
*Question:* what sets a price?
*Story:* for a century economists argued whether value came from cost or from usefulness, and could not say why
water was cheap and diamonds dear. The answer of the 1870s was that it is set at the margin, and Marshall's
picture of it has two blades. In 1956 Vernon Smith tested the picture in a classroom, expecting it to fail.
0. Hook: Chamberlin's market that missed (1948), Smith's that hit (1956–62); the question; objectives.
1. Water and diamonds: Smith's paradox; the labour theory in Ricardo and Marx; Jevons, Menger, Walras (1871–74).
2. Demand built from reservation prices, one buyer at a time; the step function; the law of demand.
3. Supply built from costs; Marshall's scissors (1890); equilibrium; who is the marginal trader.
4. Play it: guess the clearing price from the cards before the market opens.
5. Why it converges: surplus on the table; Smith's rounds; Gode and Sunder's zero-intelligence traders (1993):
   how much of the result is the institution.
6. Elasticity defined, drawn and computed; revenue and the midpoint; short and long run.
7. Shifts: a frost in Brazil; comparative statics as a habit of thought.
8. Surplus: Dupuit (1844) and Marshall; the triangle that taxes destroy.
9. Tax incidence: the side that cannot move pays; it does not matter who writes the cheque (and the
   evidence that sometimes it does).
10. Price controls: rent ceilings and queues; price floors; the gasoline lines of 1973–74; who gains.
11. When the picture fails: few sellers, hidden quality, spillovers (the payoff cards to Acts III and IV).
12. Dials. 13. In practice: commodity desks, pricing teams, tax drafting. 14. Frontier: price discovery in
    thin and algorithmic markets.

*Agora:* `market`: demand and supply from primitives, the clearing price, comparative statics, wedges and
controls; the double auction with human-like, zero-intelligence and equilibrium traders.
*Play it:* the film's guess; on the site, set a tax and predict who bears it.
*Dials:* price elasticities of a few staples (gasoline, cigarettes, housing services). *Facts:* double auctions
converge within a few rounds.
*Called it?* Smith's own expectation that the competitive model would fail in his classroom.
*Reading:* Marshall 1890, Book V; Smith 1962; Gode & Sunder 1993; Varian chs 1, 15–16; Mankiw chs 4–8;
Krugman & Wells chs 3–5.

### Part 3 · The Measure (~55)
*Question:* how do you put a number on an economy?
*Story:* in 1934 Simon Kuznets hands the US Senate the first national income accounts, with a warning about what
they leave out. The number becomes the most watched statistic in the world. The part builds it for the Island,
three ways that must agree, then asks how to compare it across years and across countries.
0. Hook: Kuznets's report and his warning; the question; objectives.
1. Petty and King count England (1665, 1696); the Depression without data; Kuznets, Meade and Stone.
2. GDP three ways on the Island: output, income, expenditure; the identity as a Sankey diagram.
3. What is in and out: home production, the informal economy, intangibles, free digital goods.
4. Real and nominal; Laspeyres and Paasche disagree; Fisher's ideal index; chaining.
5. Play it: two baskets, one year: how much did prices rise?
6. The CPI: substitution, quality and new goods; the Boskin Commission's 1.1 points (1996); hedonics.
7. Across countries: exchange rates against purchasing power; the Big Mac; the Penn World Table; what a
   revision of PPPs did to China's and India's size (2005, 2011) (verify).
8. Unemployment as a survey: the definitions, the flows, U-3 to U-6.
9. Distribution: the Lorenz curve, the Gini, top shares; the accounts distributed (Piketty, Saez and Zucman
   2018).
10. Input–output: Leontief's table (1936) and its inverse; value added in trade.
11. Revisions and vintages: the recession that was revised away; real-time data.
12. Beyond GDP: Nordhaus and Tobin (1972), the HDI, Jones and Klenow's welfare measure (2016).
13. Dials. 14. In practice: statistical agencies, country analysts. 15. Frontier: measuring intangibles and AI.

*Agora:* the Island's national accounts (a social accounting matrix) and an index-number lab.
*Play it:* the two baskets; on the site, build a price index and watch chaining fix it.
*Facts:* Kaldor's facts stated (answered in Part 20); the labour share.
*Reading:* Kuznets 1934; Petty 1665; Coyle, *GDP: A Brief but Affectionate History*; Lequiller & Blades,
*Understanding National Accounts*; Leontief, *Input-Output Economics*; Boskin et al. 1996; Lebow & Rudd 2003; Moulton
2018; Deaton & Heston 2010; Nordhaus & Tobin 1972; Piketty, Saez & Zucman 2018; Jones & Klenow 2016; Corrado, Hulten &
Sichel 2009; Henderson, Storeygard & Weil 2012; Martinez 2022.

### Part 4 · The Evidence (~56)
*Question:* when can data answer an economic question?
*Story:* in 1914 Henry Moore fits a line through the prices and quantities of pig iron, finds it sloping up, and
calls it a new law of demand; a year later Philip Wright explains that business booms moved demand along supply, and
in 1927 Elmer Working asks what such clouds show. In 1928, in an appendix to a book on vegetable oils, Wright invents
the instrument (Stock and Trebbi's stylometry says the father, not his son Sewall). Fifty years on the profession
barely believes its own regressions, and then learns to find experiments.
0. Hook: Moore's pig iron and Wright's reply; the Island's cloud; Working's question; objectives.
1. Play it: four lines through the Island's fish-market data; the truth appears in dashed green.
2. Simultaneity: both curves shift; four kinds of day; the probability limit of least squares.
3. The instrument: storms move supply only and trace demand, feasts trace supply; the Wald ratio and 2SLS;
   Wright (1928) and his arrows.
4. Haavelmo (1944) and the Cowles Commission: systems of equations; identification; the order condition.
5. Omitted variables and selection: schooling and ability, the formula, a new school as instrument; who signs up for
   training (Ashenfelter's dip).
6. Leamer's "Let's take the con out of econometrics" (1983); LaLonde's test (1986) and Dehejia and Wahba's sequel;
   *Called it?*
7. Intermission: the draft lottery of 1969, capsule by capsule, as a data melody.
8. The credibility revolution: the draft lottery (Angrist 1990), quarters of birth, two states and a border; the
   designs (pointers to *Statistics, Built* 35–37); Nobel 2021.
9. Experiments: the Island's apprenticeship by choice and by lottery; the negative income tax trials; PROGRESA; the
   lab, the field, policy trials, A/B tests.
10. The Lucas critique (1976): the American Phillips curve of the 1960s and 1970s; the Island's council and its menu.
11. Structure and design: the local average treatment effect; Deaton, Imbens and Heckman (2010); sufficient
    statistics; identified moments.
12. The Dials: the return to a year of school from eleven natural experiments; weak instruments on the Island.
13. In practice: who evaluates for a living; planning a trial; power. 14. Frontier: spillovers and general
    equilibrium in randomized-saturation trials.

*Agora:* the Island's econometrician (`agora.econometrician`): every Island dataset comes with its planted truth; OLS,
Wald and 2SLS over statkit's `quasi`; omitted ability; the apprenticeship; Lucas's islands; the village trial.
`dials.py`'s second dial.
*Play it:* the cloud; on the site, choose an instrument from four candidates and see which recovers the truth.
*Called it?* LaLonde's non-experimental estimates against the experiment.
*Reading:* Moore 1914; Wright 1915, 1928 (and Stock & Trebbi 2003); Working 1927; Haavelmo 1944; Leamer 1983;
LaLonde 1986; Dehejia & Wahba 1999; Angrist 1990; Angrist & Krueger 1991; Card & Krueger 1994; Imbens & Angrist 1994;
Bound, Jaeger & Baker 1995; Staiger & Stock 1997; Card 2001; Lucas 1976; Angrist & Pischke 2009, 2010; Deaton 2010;
Imbens 2010; Heckman 2010; Chetty 2009; Nakamura & Steinsson 2018; Crépon et al. 2013; Egger et al. 2022;
Muralidharan, Niehaus & Sukhtankar 2023; Stock & Watson, *Introduction to Econometrics*, chs 1–3, 12–13; Cunningham,
*The Mixtape*; Acemoglu, Laibson & List ch 2.

## Act II · Choosing

### Part 5 · What People Want (~52)
*Question:* can you tell what someone wants from what they buy, and what does "rational" assume?
*Story:* in 1938 Paul Samuelson, aged twenty-two, tries to purge utility from economics by keeping only what
can be observed: choices. Thirty years later Sidney Afriat shows the two are the same thing, with a test that
runs on a grocery receipt.
0. Hook: Bo's receipts; from Jevons to Hicks and Allen; Samuelson's programme; the question; objectives.
1. Play it: eleven budget lines, pick a bundle on each (the design of Harbaugh et al. 2001, crossing lines as in
   Choi, Fisman, Gale and Kariv 2007). Kept for later.
2. Preferences as a ranking: completeness, transitivity, continuity; the money pump.
3. Utility as a label: Debreu's representation; ordinal against cardinal; the lexicographic order; the MRS.
4. Convexity and the marginal rate of substitution; perfect substitutes, complements, Cobb–Douglas, CES.
5. The budget set; the tangency; Lagrange's method with the multiplier's meaning.
6. Corner solutions and kinks; non-linear budgets (a bulk price, the EITC's first kink and Saez's bunching).
7. Intermission: a century of the American basket, as a data melody.
8. Revealed preference: WARP, SARP, GARP; Afriat's theorem and its inequalities as a linear programme.
9. The test on data: your eleven choices scored (Afriat's efficiency index); its power against random choice
   (Bronars 1987); children (Harbaugh et al. 2001), students and Dutch households (Choi et al. 2007, 2014);
   America as one consumer, 1929–2025.
10. Recovering preferences: bounds on indifference curves from finite data (Varian 1982), and a forecast.
11. What rationality does not assume: selfishness, calculation, a human chooser; Becker's irrational consumers
    (1962) and why demand still slopes down.
12. Dials (consistency) and *Called it?* (McFadden's BART forecast). 13. In practice: conjoint studies,
    recommenders, discrete choice and the value of time. 14. Frontier: stochastic choice and random utility;
    revealed preference in scanner data; the consistency of a language model.

*Agora:* `consumer`: preferences, the constrained optimum (corners and kinks), a GARP tester, Afriat's index and
LP, Varian's bounds, Bronars's power, Becker's random consumers, the EITC, a logit.
*Play it:* the eleven budgets; on the site, the same with a live consistency score (no rating of the player).
*Reading:* Samuelson 1938; Houthakker 1950; Debreu 1954; Afriat 1967; Varian 1982; Becker 1962; Bronars 1987;
Harbaugh, Krause & Berry 2001; Andreoni & Miller 2002; Choi et al. 2007, 2014; Saez 2010; Blundell, Browning &
Crawford 2008; McFadden 1974; Kitamura & Stoye 2018; Chen et al. 2023; MWG chs 1–3; Kreps chs 1–4; Nicholson &
Snyder chs 2–4; Jehle & Reny ch 1; Chambers & Echenique, *Revealed Preference Theory*.

### Part 6 · Demand (~45)
*Question:* when a price changes, what happens to what people buy and to how well off they are?
*Story:* for a century the Giffen good, a good people buy more of when its price rises, was a textbook rumour.
In 2006 Robert Jensen and Nolan Miller subsidized rice for poor households in Hunan, and the poor-but-not-poorest
ate less of it. The equation that explains it was written by Slutsky in 1915 and went unread for twenty years.
0. Hook: the rice vouchers (1,300 households, 11 county towns, cuts of 0.10–0.30 yuan on 1.20); +0.45 for
   households under 80% of calories from rice; Marshall (1895) and Stigler's "immortality" (1987); Slutsky and
   Hicks and Allen; the question; objectives.
1. Play it: a week of food on $21 (14,000 calories; coconuts $1.20 for 1,400, fish $2 for 700); coconuts rise to
   $1.50 and the viewer buys more of them.
2. The demand function: price- and income-consumption curves (Bo), the demand and Engel curves; homogeneity;
   elasticities and the adding-up rules.
3. The Slutsky equation drawn as two moves (Hicks's and Slutsky's compensation); the equation and its elasticity
   form; the recipe for Giffen behaviour.
4. Giffen behaviour: the rumour (Stigler 1947, Rosen 1999); the subsistence model's three zones and its elasticity
   r/(1 − r); Jensen and Miller's design and table 3 (+0.22, +0.45, −0.61, +0.64; the inverted U, peak 0.85 at a
   0.70 rice share); Gansu; the same design on 1,300 simulated households with the truth planted.
5. Duality: the four functions, Roy's identity, Shephard's lemma, the concave expenditure function; the identities
   checked numerically on four systems.
6. Integrability: the Slutsky matrix's symmetry; a loop of prices that pumps money (Green's theorem).
7. Intermission: a century of relative prices, fifteen kinds of spending, as a data film and melody.
8. Engel curves: Engel 1857; America's century and 2024's quintiles; Hamilton 2001 and Costa 2001 (CPI bias from
   Engel drift), Almås 2012; *Called it?*: Engel's law.
9. Welfare: CV, EV and consumer's surplus; Willig 1976; Hausman 1981's exact surplus and deadweight loss.
10. The cost of living: Konüs; the substitution bias; Hicks's virtual prices and Hausman's Apple-Cinnamon Cheerios;
    the Boskin Commission's pieces.
11. Demand systems: the LES (Stone 1954), the AIDS (Deaton and Muellbauer 1980) estimated and tested on an island
    survey; Gorman's aggregation.
12. Dials (staples' price elasticities with Hunan's rows; food's income elasticity, new). 13. In practice: the CPI's
    geometric means and chained index; food prices and poor households (Deaton 1989); Ramsey taxes. 14. Frontier:
    inflation inequality (Jaravel 2019), new goods (Feenstra 1994; Redding and Weinstein 2020), income-dependent
    preferences (Jaravel and Lashkari 2024; Atkin et al. 2024).

*Agora:* `demand`: four demand systems with all four dual functions and their identities checked numerically, the
Slutsky matrix and decompositions, the subsistence diet and the voucher experiment, CV/EV/surplus with Willig and
Hausman, price indices and Feenstra, Working–Leser and Hamilton's drift, AIDS estimation with tests, the
integrability loop.
*Dials:* staples' price elasticities (Hunan's rows added); food's income elasticity (new); CPI bias (Hamilton's and
Costa's rows added). *Facts:* Engel's law. *Called it?* Engel 1857.
*Reading:* Slutsky 1915; Hicks and Allen 1934; Hicks, *Value and Capital*; Jensen & Miller 2008; Stigler 1947;
Rosen 1999; Roy 1947; Shephard 1953; Hurwicz & Uzawa 1971; Konüs 1924; Willig 1976; Hausman 1981, 1997; Stone 1954;
Deaton & Muellbauer 1980 and *Economics and Consumer Behavior*; Gorman 1953; Houthakker 1957; Hamilton 2001; Costa
2001; Almås 2012; Deaton 1989; Ramsey 1927; Feenstra 1994; Jaravel 2019; Redding & Weinstein 2020; Jaravel &
Lashkari 2024; Atkin et al. 2024; MWG chs 2–3; Varian chs 6–10, 14; Nicholson & Snyder chs 5–6.

### Part 7 · Time and Risk (~50)
*Question:* how do people choose when the pay-off comes later, or may not come at all?
*Story:* in 1713 Nicolaus Bernoulli posed a coin game whose expected prize is infinite; in 1738 his cousin Daniel
answered with the logarithm of wealth, the first utility function. Two centuries later von Neumann and Morgenstern
gave it axioms, Allais broke one of them over lunch with Savage, and Fisher's diagram of today against tomorrow
became the atom of macroeconomics.
0. Hook: the St Petersburg game played ($1, doubling); each ending worth 50 cents; a pause to name a price; a
   million simulated games (half pay $1, the average about $11 and still rising); Nicolaus Bernoulli, Cramer, Daniel
   Bernoulli ($4.36, $5.97, $10.94 at $100, $1,000, $1 million); the question; objectives; not financial advice.
1. Fisher's two periods (1930): Chidi's harvest, Dara's 10%; the Euler equation and the EIS; the rate rises to 30%
   (substitution −3.1, income +3.3, magnified); saving against the rate for EIS 2, ½ and ⅛.
2. Discounting: present values; Samuelson (1937) and his two caveats; Koopmans (1960); exponential, hyperbolic and
   beta–delta functions and the price of a year's wait.
3. Lotteries and expected utility: Ana's reef and open sea; the von Neumann–Morgenstern axioms; the triangle on $0,
   $1M, $5M with straight, parallel lines.
4. Play it: Allais's two pairs, chosen by the viewer; Kahneman and Tversky's 82%; the common-consequence algebra; the
   parallel moves in the triangle; Paris, May 1952.
5. Risk aversion: the certainty equivalent ($90 against $120) and premium; γ = 0, 1, 2, 4 and the switch at 1.26;
   Arrow–Pratt and ½Aσ²; CARA against CRRA.
6. Insurance and the risky asset: Mossin's full cover at fair odds, partial cover under loadings, the most Ana pays
   ($27.27); deductibles' implied γ (26, 98, 203; Sydnor 2010); Merton's share.
7. Intermission: Hall's century, the real bill rate against consumption growth per head, 1935–2025 (OLS 0.07, IV
   −0.02), as a data film and melody.
8. Stochastic dominance: first and second order; mean-preserving spreads (Rothschild and Stiglitz 1970).
9. Allais and Ellsberg in the triangle: Machina's fanning out (Chew's weighted utility); Ellsberg's urn (1961) and
   maxmin expected utility; Knight; prospect theory in one card (pointers to *Psychology, Built* 26 and Part 45).
10. Rabin's calibration (2000): the power function computed (γ = 91 at $100,000) and his tables I and II; Rabin and
    Thaler's parrot.
11. Time meets risk: one γ for two attitudes; the plane of estimates; Epstein–Zin and early resolution; Mehra and
    Prescott, Weil, Bansal and Yaron.
12. Present bias: Thaler (1981); reversals; Strotz; beta–delta; Chidi's store; Pollak; commitment; Imai et al.
13. Measuring it: Holt and Laury (2002, 2005) and their stakes; the menu on 400 simulated islanders; the HRS gambles
    (Barsky et al. 1997); Deal or No Deal (Post et al. 2008); *Called it?*: Bernoulli against Hayden and Platt.
14. Dials (relative risk aversion and the EIS, both new, both contested). 15. In practice: pooling, pension defaults
    (Madrian and Shea 2001; Save More Tomorrow), the social discount rate as an is/ought card. 16. Frontier:
    ambiguity and robustness (Gilboa–Schmeidler; Hansen–Sargent), stated beliefs (Manski; Hurd and McGarry), the
    Global Preference Survey.

*Agora:* `risk`: CRRA, CARA and log utility, certainty equivalents, Arrow–Pratt, dominance, the triangle and
weighted utility, Allais and Ellsberg (maxmin), insurance and deductibles, Merton's share, Rabin's calibration for the
power function, the St Petersburg game (Bernoulli's and Cramer's prices, truncations, the median heuristic), Fisher,
discount functions and reversals, Epstein–Zin early resolution, beta–delta plans, Hall's regression, Holt and Laury's
menu with noisy respondents, the HRS thresholds, Tversky and Kahneman's curves.
*Dials:* relative risk aversion (new); the elasticity of intertemporal substitution (new). *Called it?* Bernoulli
1738, partly right.
*Reading:* Bernoulli 1738; Fisher 1930; Samuelson 1937; Koopmans 1960; von Neumann & Morgenstern 1944; Savage 1954;
Allais 1953; Ellsberg 1961; Pratt 1964; Arrow 1965; Mossin 1968; Merton 1969; Rothschild & Stiglitz 1970; Kahneman &
Tversky 1979; Machina 1982; Kreps & Porteus 1978; Epstein & Zin 1989; Mehra & Prescott 1985; Weil 1989; Hall 1988;
Strotz 1955–56; Laibson 1997; Rabin 2000; Holt & Laury 2002; Barsky et al. 1997; Hayden & Platt 2009; Hansen &
Sargent 2008; Manski 2004; MWG ch 6; Kreps chs 5–6; Gollier 2001; Varian chs 10–13.

### Part 8 · The Firm (~54)
*Question:* how does a firm decide what to make and how, and why is there a firm at all?
*Story:* Paul Douglas's chart of 1927 puts American manufacturing's output a quarter of the way from labour to
capital, year after year; the mathematician Charles Cobb gives him P′ = 1.01 L^¾ C^¼, and labour's share of
income turns out to be the exponent. Ten years later Ronald Coase asks the question the function hides: if markets
coordinate so well, why is so much of the economy run by command inside firms?
0. Hook: Douglas's chart, 1899–1922 on a log scale (capital ×4.31, labour ×1.61, output ×2.40); Cobb; the 1928
   formula refitted (labour 0.746, capital 0.254); the PWT's US labour share, near 62% for fifty years and 56.8%
   in 2023; Robertson's "islands of conscious power"; the question; objectives.
1. Technology: Crusoe's boatyard, q = 2K^0.25 L^0.5; marginal products by discrete steps (2.83, 1.17, 0.90, 0.76);
   isoquants; the technical rate of substitution.
2. Cobb and Douglas refitted, and broken: unrestricted, with a time trend (capital −0.53), in growth rates (Felipe
   and Adams 2005); CES and σ (Arrow, Chenery, Minhas and Solow 1961); shares as exponents.
3. Returns to scale; a pipe's steel against its capacity, the six-tenths rule (Williams 1947), Chenery (1949); why
   not one firm?
4. Cost minimization (eight boats for $8,841.68); conditional factor demands; the cost function and Shephard's lemma
   checked numerically.
5. Cost curves from the technology: fixed, variable, average and marginal; the envelope of short-run curves.
6. Play it: run the boatyard; hire three, where p·MP_L = w; sunk slipways change the profit, not the decision.
7. Profit and supply: price = marginal cost; break-even $1,094 and shut-down $200; supply elasticities 1 and 3; Le
   Chatelier (Samuelson) and Hotelling.
   Intermission: Douglas's chart redrawn year by year, the output index as a tune.
8. The industry: free entry, zero profit and a flat long-run supply (about 20 yards); with fixed costs from $2,000
   to $8,000, 27 yards, rents of $14,620 a month and an upward-sloping supply (Ricardo).
9. Do firms maximize profit? Hall and Hitch (1939); Alchian (1950); Friedman's billiard player (1953); Alchian's
   survival run on 200 island yards (the middle half of markups from 22–75% to 46–57%, 479 closures).
10. Coase (1937): the cost of using the price mechanism; the boundary at a margin; Williamson's make-or-buy.
11. Hold-up: invest 100 together, 25 apart; GM and Fisher Body (1919, 1926); Klein, Crawford and Alchian (1978) and
    the 2000 *Journal of Law and Economics* dispute (Coase, Klein, Freeland, Casadesus-Masanell and Spulber).
12. Grossman, Hart and Moore: residual control rights; surplus 8.50, 8.29, 6.50, 6.38; a pointer to Parts 14 and 62.
13. Dials (capital's output elasticity, settled within a range; σ between capital and labour, contested).
    14. In practice: the six-tenths rule, Wright's learning curve (1936), capacity as a newsvendor (113 boats).
    15. Frontier: intangibles (Haskel and Westlake 2018), generative AI at work (Brynjolfsson, Li and Raymond), the
    Coasean singularity (Shahidi et al. 2025).

*Agora:* `firm`: Cobb–Douglas, CES and Leontief technologies with conditional demands and costs, Shephard's and
Hotelling's lemmas checked by differences, short-run costs, supply and Le Chatelier, U-shaped costs, free entry with
identical and heterogeneous firms, Cobb and Douglas's regressions, hold-up, Grossman–Hart–Moore ownership,
make-or-buy, the boatyard game and Alchian's selection. The Island's yard, larger yard and industry get their truths.
*Dials:* the output elasticity of capital (new); the elasticity of substitution between capital and labour (new).
*Facts:* the labour share (near 62% in 1950–99 in the PWT, 56.8% in 2023). No *Called it?*: the part's claims are
theorems and records, and Coase's remark about the telephone is a comparative static, not a dated forecast.
*Reading:* Cobb & Douglas 1928; Douglas 1976; Felipe & Adams 2005; Arrow, Chenery, Minhas & Solow 1961; Chenery 1949;
Hall & Hitch 1939; Alchian 1950; Friedman 1953; Coase 1937; Williamson 1975, 1985; Klein, Crawford & Alchian 1978;
the *JLE* 2000 symposium on Fisher Body; Grossman & Hart 1986; Hart & Moore 1990; Hart 1995; Gollin 2002; Chirinko
2008; Gechert et al. 2022; Oberfield & Raval 2021; Karabarbounis & Neiman 2014; Wright 1936; Haskel & Westlake 2018;
Brynjolfsson, Li & Raymond 2025; Varian chs 19–24; MWG ch 5.

## Act III · Markets

### Part 9 · The Invisible Hand, Proved (~58)
*Question:* can a whole economy of selfish traders reach a state nobody could improve on, and will it?
*Story:* R. A. Radford, back from officers' prisoner-of-war camps in Italy and Germany, describes in *Economica*
(1945) a market grown from equal Red Cross parcels: a padre's arbitrage, cigarettes as money, one price where the
Exchange and Mart boards were read, slump when the parcels stopped, and liberation on 12 April 1945. In 1954 Arrow
and Debreu prove that such an order can exist in any economy of their kind. What they could not prove is that an
economy gets there.
0. Hook: Radford's camps (the parcel, the padre, "cheese for seven", the board, the salmon, August 1944, the Bully
   Mark, February 1945, liberation); Arrow and Debreu (1954); the question; objectives.
1. Play it: four proposed trades between Ana and Bo, accepted or refused.
2. The Edgeworth box: indifference maps, the lens, Pareto efficiency, the contract curve (Edgeworth's name).
3. Prices: budget lines, offer curves, the equilibrium at 1.018 baskets a fish, Walras's law; the law of one price
   as a Fact (Brent against WTI; price levels across countries; Agora's two villages; Radford's salmon).
4. The core and Edgeworth's conjecture: a blocking coalition; the core of the replicated box, computed for 1 to 20
   copies; Debreu and Scarf (1963), Aumann (1964).
5. The first welfare theorem in five lines; its assumptions as the map of Act IV.
6. The second welfare theorem: a target, its supporting price, the lump-sum transfer, the separating hyperplane;
   why lump-sum transfers are rare.
   Intermission: Brent and WTI month by month, 1987-2026, the gap as a tune.
7. Existence: the price simplex, Brouwer's fixed point, Sperner's colouring and Scarf's door-to-door walk (grids of
   6, 12 and 48).
8. Stability: tatonnement, gross substitutes (Arrow, Block and Hurwicz 1959), Scarf's cycle with its two conserved
   quantities, and its laboratory test (Anderson, Plott, Shimomura and Granat 2004).
9. Computing an equilibrium: the Island's five goods and twelve islanders, by Newton (6 steps) and the auctioneer
   (238).
10. Production: Crusoe decentralized into a firm and a household; convexity, and increasing returns.
11. Anything goes: three equilibria in a two-trader economy; Sonnenschein, Mantel and Debreu; Kirman; Brown and
    Matzkin.
12. Time and uncertainty: Arrow securities share Ana's and Chidi's weather risk; a bond alone shares nothing.
13. The calculation debate: Mises, Lange, Hayek; Kantorovich's programme for the yard's machines and its resolving
    multipliers.
14. Dials (misallocation, new). 15. In practice: computable general equilibrium models; *Called it?*: the 1992 NAFTA
    forecasts against 1989-2009 (Kehoe). 16. Frontier: PPAD; Shapley and Scarf's housing market and top trading
    cycles; Budish's course market.

*Agora:* `ge`: traders (Cobb-Douglas, CES, Leontief), the Edgeworth box, offer curves, the core of the replicated
economy by coalition checks, Sperner's labelling and Scarf's walk, tatonnement and Scarf's cycle, Newton, Crusoe,
three equilibria, Arrow securities and a bond economy, Kantorovich's programme with duals, misallocation with Hsieh
and Klenow's formula, top trading cycles. The whole Island cleared at once.
*Dials:* the TFP gain from equalizing marginal products (new; contested). *Facts:* the law of one price. *Called
it?* Sobarzo's 1992 forecasts of NAFTA, wrong.
*Reading:* Radford 1945; Edgeworth 1881; Walras 1874; Arrow & Debreu 1954; McKenzie 1954; Debreu, *Theory of Value*;
Debreu & Scarf 1963; Aumann 1964; Arrow, Block & Hurwicz 1959; Scarf 1960, 1967, 1973; Anderson et al. 2004;
Sonnenschein 1973; Mantel 1974; Debreu 1974; Kirman 1992; Brown & Matzkin 1996; Arrow 1953; Mises 1920; Lange
1936-37; Hayek 1945; Kantorovich 1939; Hsieh & Klenow 2009; Bils, Klenow & Ruane 2021; Kehoe 2005, 2014;
Papadimitriou 1994; Daskalakis, Goldberg & Papadimitriou 2009; Shapley & Scarf 1974; Roth 1982; Budish 2011; MWG chs
15-19; Kreps; Jehle & Reny ch 5.

### Part 10 · The Price Maker (~54)
*Question:* what does a seller do when the price is hers to set?
*Story:* Jules Dupuit, a French engineer of bridges and roads, argues in 1844 that a bridge is worth what crossing
it is worth to everyone who crosses, so a toll on a crossing that costs nothing turns value away for no saving. In
1849 he explains that the railway does not leave third-class carriages without roofs to save the cost of a roof: it
does it to keep anyone who could pay for second class from travelling third. Price discrimination, screening and
the modern airline fare are all in that paragraph.
0. Hook: the bridge and the toll (1844); the roofless carriage (1849, paraphrased); the menu everywhere; the
   question; objectives.
1. Play it: set one fare for Bo's ferry against a hundred islanders' values.
2. Marginal revenue; the monopoly optimum; no supply curve; the Lerner index and the inverse-elasticity rule.
3. Deadweight loss; Harberger's small triangles (1954) and Posner's larger rectangle (1975), with Tullock (1967).
4. First-degree discrimination: all the surplus, no waste; Pigou's three degrees (1920).
5. Third-degree: students and townsfolk; a market opened; Schmalensee (1981) and Varian's output test (1985).
6. Second-degree: the two-type screening menu (Mussa and Rosen 1978), the bottom of the menu cut, the information
   rent; damaged goods (Deneckere and McAfee 1996).
   Intermission: green arabica and the shelf price of ground coffee month by month, 1980-2026, the shelf price as a
   tune.
7. Two-part tariffs (Oi's Disneyland, 1971): identical visitors, then two ordinary visitors to one keen one.
8. Bundling (Stigler 1963; Adams and Yellen 1976): two visitors, then four hundred with correlated values.
9. Durable goods: the Coase conjecture (1972) solved for one to 365 price changes a year; renting, commitment,
   planned obsolescence, reputation.
10. Natural monopoly: average-cost pricing, Ramsey–Boiteux prices against one uniform markup.
11. Regulation: rate of return and gold plating (Averch and Johnson 1962); price caps (Littlechild 1983).
12. Monopsony in one diagram, with a minimum wage (a pointer to Part 38).
13. Pass-through: a half and one and a half; incomplete pass-through as a Fact, measured on coffee; Nakamura and
    Zerom's accounting (2010).
14. Dials (markups, new). 15. In practice: fare fences and Littlewood's rule (1972); a pointer to Part 60.
16. Frontier: personalized pricing learned from an experiment (Dubé and Misra 2023), rerun in Agora; pricing
    algorithms (Calvano et al. 2020; Assad et al. 2024).

*Agora:* `pricing`: linear and constant-elasticity demand, the monopoly price and pass-through, the ferry, first-,
second- and third-degree discrimination, two-part tariffs, bundling, the Coase equilibrium, Ramsey prices, the
Averch–Johnson firm, monopsony, Littlewood's rule, personalized prices learned from a price experiment.
*Dials:* markups over marginal cost (new; contested). *Facts:* incomplete pass-through. *Called it?* none: the
theory of one seller makes no dated public forecast that can be checked against what followed.
*Reading:* Dupuit 1844, 1849; Pigou 1920; Robinson 1933; Lerner 1934; Harberger 1954; Tullock 1967; Posner 1975;
Schmalensee 1981; Varian 1985; Mussa & Rosen 1978; Maskin & Riley 1984; Deneckere & McAfee 1996; Oi 1971; Stigler
1963; Adams & Yellen 1976; McAfee, McMillan & Whinston 1989; Coase 1972; Stokey 1981; Bulow 1982, 1986; Gul,
Sonnenschein & Wilson 1986; Ramsey 1927; Boiteux 1956; Averch & Johnson 1962; Littlechild 1983; Littlewood 1972;
Nakamura & Zerom 2010; Weyl & Fabinger 2013; Hall 1988; De Loecker & Warzynski 2012; De Loecker, Eeckhout & Unger
2020; Traina 2018; Dubé & Misra 2023; Calvano et al. 2020; Assad et al. 2024; Tirole, *Industrial Organization*,
chs 1–4; Belleflamme & Peitz; Varian chs 25–27; Talluri & van Ryzin.

### Part 11 · Games (~58)
*Question:* what happens when my best choice depends on yours, and yours on mine?
*Story:* at the start of 1950, at RAND, Merrill Flood and Melvin Dresher have two colleagues, Armen Alchian and John
Williams, play a new game a hundred times, to test a new idea by a Princeton student. Both cooperate in 60 rounds
and both defect, as the theory says, in only 14. John Nash's reply: it was one long game, not a hundred short ones.
0. Hook: the hundred rounds (the joint outcomes, as Poundstone counted them from Flood's report); Nash's comment;
   Tucker's prisoners; games everywhere; the question; objectives.
1. Play it: guess two-thirds of the average (an Island crowd; Nagel 1995; the Financial Times, 1997).
2. Strategic form; dominance in the prisoner's dilemma; iterated elimination (Gibbons's example); the guessing game's
   descent to 0, and how few take three steps.
3. Nash equilibrium (1950); best responses crossing three times in the battle of the sexes; existence by a fixed
   point (the simplex of Part 9); von Neumann (1928).
4. Coordination, battle of the sexes, chicken, stag hunt: one grammar of social life.
5. Mixed strategies: indifference; the test on penalty kicks (Chiappori, Levitt and Groseclose 2002;
   Palacios-Huerta 2003) and Wimbledon serves (Walker and Wooders 2001).
6. Extensive form; backward induction; subgame perfection (Selten 1965); an empty threat; credibility (the chain
   store, 1978).
   Intermission: the American and Soviet (later Russian) nuclear stockpiles, 1945-2026, with the treaties; their
   total as a tune.
7. The centipede and the limits of induction (Rosenthal 1981; McKelvey and Palfrey 1992); the ultimatum game (Güth,
   Schmittberger and Schwarze 1982) in fifteen societies (Henrich et al. 2001).
8. Repeated games: the discount factor that sustains grim trigger; the folk theorem drawn as a region (Friedman
   1971; Fudenberg and Maskin 1986); the finite horizon (Kreps, Milgrom, Roberts and Wilson 1982; Selten and Stoecker
   1986).
9. Axelrod's tournaments (1980): tit for tat; Agora's round robin and ecology; one mistake, and win-stay, lose-shift
   (Nowak and Sigmund 1993).
10. Focal points (Schelling 1960); correlated equilibrium (Aumann 1974) as a traffic light, by linear programming.
11. Evolution and learning: hawk and dove, evolutionarily stable strategies (Maynard Smith and Price 1973),
    rock-paper-scissors cycles (Sinervo and Lively 1996), fictitious play (Brown, Robinson 1951; Shapley 1964).
12. Level-k and cognitive hierarchy fitted to the guessing game (Stahl and Wilson 1994; Camerer, Ho and Chong 2004);
    *Called it?*
13. Bayesian games in one example (Harsanyi 1967-68; pointers to Parts 13, 16 and 53).
14. Dials (depth of reasoning, new), with Keynes's beauty contest. 15. In practice: bargaining (Rubinstein 1982),
    standards (Sweden, 1967), arms control (Schelling and Halperin 1961). 16. Frontier: regret matching (Hart and
    Mas-Colell 2000), solved poker (Bowling et al. 2015), Libratus and Pluribus (*AI, Built*).

*Agora:* `games`: pure and mixed equilibria (support enumeration), iterated elimination, the cognitive hierarchy and
its fit, game trees and backward induction (the entry game, the centipede), Rubinstein's split, grim trigger and the
folk region, a strategy library with matches, a noisy round robin and the ecology, correlated equilibrium by LP, the
replicator, ESS checks, fictitious play, regret matching, Bayesian equilibria.
*Play it:* the guessing game; on the site, an Axelrod tournament the reader enters with a strategy.
*Dials:* the depth of strategic reasoning (new; depends on the setting). *Called it?* the Nash prediction for the
guessing game (0) against the winning guess: wrong the first time.
*Reading:* Nash 1950, 1951; von Neumann 1928; Flood 1952; Schelling, *The Strategy of Conflict*; Selten 1965, 1978;
Harsanyi 1967-68; Aumann 1974; Axelrod 1980, 1984; Nowak & Sigmund 1993; Nagel 1995; Stahl & Wilson 1994; Camerer,
Ho & Chong 2004; Henrich et al. 2001; Palacios-Huerta 2003; Rubinstein 1982; Hart & Mas-Colell 2000; Osborne;
Osborne & Rubinstein; Fudenberg & Tirole chs 1–5; Gibbons; Camerer, *Behavioral Game Theory*.

### Part 12 · Competition among the Few (~57)
*Question:* how do a handful of firms compete, and when do they stop?
*Story:* in 1991 Archer Daniels Midland's new lysine plant in Decatur starts a price war that takes the American
price from $1.30 a pound to 64 cents, below ADM's own cost; in June 1992 the "lysine association" meets in Mexico
City, from November the head of ADM's lysine division records its meetings for the FBI, and prices climb back above
a dollar until the raid of June 1995. On a tape played at the trial, ADM's president describes a company slogan: "Our
competitors are our friends. Our customers are the enemy." The economics of why cartels form, cheat and fall is on
those tapes too.
0. Hook: the plant, the price war and the cartel's prices as Connor (1998) states them; the informant and the raid;
   the slogan; the $100 million fine; Connor's 12-28%; markets of a few; the question; objectives.
1. Play it: name your price against Crusoe's $40 repair; then against twenty yards.
2. Cournot (1838): the mineral springs; best replies and their path; the prisoner's dilemma in quantities; the
   price with N firms.
3. Bertrand's reply (1883): the undercutting spiral; the paradox; unequal costs.
4. Resolving it: Edgeworth (1897) and Edgeworth cycles (Maskin and Tirole 1988); Kreps and Scheinkman (1983);
   differentiated prices as strategic complements; repetition.
5. Hotelling's line (1929) and his two parties; d'Aspremont, Gabszewicz and Thisse (1979); Salop's circle (1979) and
   excess entry.
6. Monopolistic competition: Chamberlin and Robinson (1933); Dixit and Stiglitz (1977); the gains from variety
   (Krugman 1979).
   Intermission: crude oil and the pump price of gasoline, 1986-2026, in October 2026 dollars; the pump price as a
   tune.
7. Stackelberg (1934) and commitment; Dixit's credible capacity (1980) and its three regimes (Bain 1956); Fudenberg
   and Tirole's animals (1984).
8. Collusion as a repeated game: the threshold with N firms in quantities and in prices (Friedman 1971); Stigler
   (1964) and what helps a cartel (Bernheim and Whinston 1990); *Called it?*
9. Cartels in the data: the Joint Executive Committee (Porter 1983); Green and Porter's price wars (1984) simulated;
   the lysine overcharge; leniency (the US policy of 1993).
10. Tacit collusion and the law: the Sherman Act and Article 101, *Twombly* (2007), *Wood Pulp* (1993);
    price-matching promises; the airline fare-database case (1992-94); rockets and feathers (Borenstein, Cameron and
    Gilbert 1997) tested on the Data Room's monthly prices.
11. Concentration: the Herfindahl index; Cowling and Waterson's $L = H/\varepsilon$ (1976); the 2010 and 2023
    merger guidelines.
12. Mergers: the merger paradox (Salant, Switzer and Reynolds 1983); Farrell and Shapiro's needed savings (1990);
    Deneckere and Davidson (1985); Williamson's trade-off (1968).
13. Contestable markets (Baumol, Panzar and Willig 1982); limit pricing (Milgrom and Roberts 1982); predation (McGee
    1958; Kreps and Wilson 1982; *Brooke Group* 1993).
14. Dials (cartel overcharges, new), with the sentencing guidelines' 10%. 15. In practice: the hypothetical
    monopolist and critical loss (Katz and Shapiro 2003), *FTC v. Staples* (1997), the economist's kit (Parts 43,
    44, 59). 16. Frontier: common ownership (Azar, Schmalz and Tecu 2018; Dennis, Gerardi and Schenone 2022; O'Brien
    and Salop's MHHI); pricing algorithms (Calvano et al. 2020; Assad et al. 2024); the RealPage case.

*Agora:* `oligopoly`: Cournot with any costs, reaction curves and their path, homogeneous and differentiated
Bertrand, Kreps and Scheinkman's check, Hotelling and Salop, Dixit-Stiglitz, Stackelberg, Dixit's credible capacity
and its regimes, collusion thresholds, Green and Porter's price wars, the leniency game, the HHI, the merger paradox
and the needed savings, Williamson's trade-off, the modified HHI.
*Play it:* a price war against Crusoe; on the site, a cartel the reader can keep or cheat on, and a bad season that
starts a war nobody chose.
*Dials:* cartel overcharges (new; contested). *Called it?* Stigler (1964): secret price cuts as what breaks cartels;
partly right (Levenstein and Suslow 2006).
*Reading:* Cournot 1838; Bertrand 1883; Hotelling 1929; Chamberlin 1933; Stigler 1964; Dixit & Stiglitz 1977; Dixit
1980; Kreps & Scheinkman 1983; Porter 1983; Green & Porter 1984; Salant, Switzer & Reynolds 1983; Farrell & Shapiro
1990; Connor 1998, 2014; Levenstein & Suslow 2006; Tirole chs 5–9; Cabral; Motta; Whinston.

## Act IV · Failure and Design

### Part 13 · Lemons and Signals (~50)
*Question:* what happens to a market when one side knows more than the other?
*Story:* George Akerlof's thirteen pages on used cars were turned down by the *American Economic Review* and the
*Review of Economic Studies* as trivial, and by the *Journal of Political Economy*, whose referees held that if the
paper were right no goods could be traded. The *Quarterly Journal of Economics* printed it in 1970. The part follows
the idea from boats to the health plans that destroyed themselves.
0. Hook: the rejections; the paper and the Nobel; private information everywhere; the question; objectives.
1. Play it: buy a boat from Bo you cannot inspect (the best blind offer, and the boats left unsold).
2. Akerlof's market (1970): the value of the average boat offered against the price; partial unravelling; Akerlof's
   own example, in which nothing trades; Gresham's law; *Called it?*
3. Guarantees that are cheap only for honest sellers; reputations, brands, chains, inspectors, licences; their cost.
4. Signalling (Spence 1973): schooling that teaches nothing; separating and pooling equilibria; the intuitive
   criterion (Cho and Kreps 1987; Riley 1979).
5. Is school a signal? human capital against signals; sheepskin effects; the GED (Tyler, Murnane and Willett 2000);
   compulsory schooling (Part 4); Caplan (2018).
6. Screening (Rothschild and Stiglitz 1976): the separating menu; why an equilibrium may not exist.
   Intermission: the prices of used cars and of new vehicles against all consumer prices, 1953-2026; the used-car
   line as a tune.
7. The death spiral: Harvard's PPO, 1995-97 (Cutler and Zeckhauser 1998; Cutler and Reber 1998), and Agora's.
8. The Einav-Finkelstein diagram, rebuilt from Einav, Finkelstein and Cullen's estimates for Alcoa (2010); what a
   subsidy would cost.
9. Testing for asymmetric information: the positive-correlation test (Chiappori and Salanié 2000) on simulated
   drivers, and why it can fail (advantageous selection, Finkelstein and McGarry 2006).
10. Credit rationing (after Stiglitz and Weiss 1981); a pointer to Parts 26 and 46.
11. Mandates, subsidies and risk adjustment: the Affordable Care Act, Massachusetts (Hackmann, Kolstad and Kowalski
    2015), inertia (Handel 2013).
12. Online markets: Bayes's rule for a new seller's reviews; eBay (Cabral and Hortaçsu 2010).
13. Dials (the welfare cost of adverse selection, new). 14. In practice: underwriting, telematics, annuities
    (Finkelstein and Poterba 2004), *Test-Achats* (2011). 15. Frontier: selection on moral hazard (Einav,
    Finkelstein, Ryan, Schrimpf and Cullen 2013); data, genes and the end of pooling (GINA 2008).

*Agora:* `info`: lemons with additive and proportional premiums and a single buyer's offers, a guarantee's
separation, Spence's equilibria, the Rothschild-Stiglitz market and its existence, the Einav-Finkelstein welfare
calculation, a death spiral, the positive-correlation test, credit rationing, reputation by Bayes's rule.
*Play it:* a blind offer for Bo's boat; on the site, forty boats to buy blind, a market to watch unravel, and an
inspection to pay for.
*Dials:* the welfare cost of adverse selection (new; depends on the setting). *Called it?* the referees who called
the paper trivial or wrong: wrong.
*Reading:* Akerlof 1970; Spence 1973; Rothschild & Stiglitz 1976; Stiglitz & Weiss 1981; Cho & Kreps 1987; Einav &
Finkelstein 2011; Einav, Finkelstein & Cullen 2010; Cutler & Reber 1998; Chiappori & Salanié 2000; Finkelstein &
McGarry 2006; Bolton & Dewatripont chs 2–3; MWG ch 13; Laffont & Martimort.

### Part 14 · Incentives (~55)
*Question:* how do you get someone to work for you when you cannot see what they do?
*Story:* late in 1978, eighteen farmers in Xiaogang, Anhui, put their thumbprints on a secret contract: divide the
commune's land, deliver each family's quota and keep the rest, and raise each other's children if the leaders are
jailed for it. The next harvest was far larger (accounts differ on the numbers, not on that). The contract is a
solved principal–agent problem.
0. Hook: the commune's eighteenth; the thumbprints; the result, not the effort, everywhere; the question; objectives.
1. Play it: write Friday's contract (a fixed pay and a share of the harvest), and see effort and profit.
2. Team production and the free rider (Alchian and Demsetz 1972; Holmström 1982): one-eighteenth of the effort; the
   residual claimant and the budget breaker.
3. The principal–agent model (Ross 1973; Mirrlees 1975; Holmström 1979; Grossman and Hart 1983): two efforts, two
   harvests; the participation and incentive constraints in utility space; pay as an inference.
4. The trade-off: insurance against incentives; the linear contract solved (Holmström and Milgrom 1987); the optimal
   share in one formula; Prendergast's tenuous trade-off (1999, 2002).
5. The informativeness principle (Holmström 1979): the common shock removed; CEOs paid for luck (Bertrand and
   Mullainathan 2001).
6. Piece rates at Safelite (Lazear 2000): output up 44%, about half from sorting; tree planters (Shearer 2004) and
   fruit pickers (Bandiera, Barankay and Rasul 2005).
   Intermission: GDP per head in China and India, 1950-2022; China's line as a tune.
7. Multitasking (Holmström and Milgrom 1991): what you pay for is what you get; teaching to the test; Kerr (1975);
   *Called it?* on cheating in Chicago (Jacob and Levitt 2003).
8. Tournaments and promotions (Lazear and Rosen 1981; Rosen 1986); golf (Ehrenberg and Bognanno 1990), mutual funds
   (Brown, Harlow and Starks 1996), sabotage (Lazear 1989).
9. Career concerns (Holmström 1999; Gibbons and Murphy 1992) and the ratchet in planned economies (Weitzman 1980);
   commitment and price caps.
10. Efficiency wages (Shapiro and Stiglitz 1984): unemployment as a discipline device; Ford's five dollars (Raff and
    Summers 1987); gift exchange in the laboratory and the field.
11. Sharecropping from Marshall to Cheung and Stiglitz; Shaban (1987); Operation Barga (Banerjee, Gertler and Ghatak
    2002); the household responsibility system measured (Lin 1992).
12. When incentives backfire: crowding out (Gneezy and Rustichini 2000; Frey and Oberholzer-Gee 1997; Bénabou and
    Tirole 2003, 2006).
13. Dials. 14. In practice: compensation design, franchising, procurement (Laffont and Tirole 1993); incomplete
    contracts and ownership by reference to Part 8. 15. Frontier: relational contracts (Baker, Gibbons and Murphy
    2002; Levin 2003); incentives for machines (specification gaming; Hadfield-Menell and Hadfield 2019; Gao,
    Schulman and Hilton 2023).

*Agora:* `contracts`: teams, the linear and the two-outcome principal–agent problems, relative performance, multitask,
tournaments, the ratchet, career concerns, an efficiency-wage labour market, sharecropping, relational contracts.
*Play it:* a share of Friday's harvest; on the site, a fixed pay and a share to set against luck and risk aversion,
with forty days of harvests and pay.
*Dials:* the output response to piece rates (new; settled within a range). *Called it?* Holmström and Milgrom's
multitasking against Chicago's test scores: right.
*Reading:* Holmström 1979, 1982; Holmström & Milgrom 1987, 1991; Lazear 2000; Lazear & Rosen 1981; Shapiro & Stiglitz
1984; Lin 1992; Bolton & Dewatripont chs 4, 6, 8, 11; Laffont & Martimort; Milgrom & Roberts.

### Part 15 · Spillovers (~54)
*Question:* what happens when my choice lands on you, and nobody pays?
*Story:* James Meade (1952) used the orchard and the beekeeper as the textbook example of a benefit no market
could price. In 1972 Steven Cheung went to Washington State and found the contracts: orchards paid pollination fees,
and for honey crops the beekeepers paid apiary rents (Cheung 1973). The part is about when Coase is right and when
Pigou is.
0. Hook: the fable and the contracts; spillovers everywhere; the question; objectives.
1. Play it: the shared pot (four islanders, twenty shells, the pot multiplied by 1.6).
2. The wedge between private and social cost: Bo's kiln and Ana's fish; the first welfare theorem's missing market.
3. Pigou's tax (1920); the efficient amount of pollution is not zero; Pigouvian subsidies.
4. Coase (1960): his own table of the cattle and the corn; bargaining under either rule; transaction costs.
5. The fable of the bees investigated: Cheung's rents per hive in money and in nectar.
6. Public goods: rivalry and exclusion; Samuelson's condition (1954); Lindahl prices; the lighthouse (Coase 1974).
   Intermission: sulphur dioxide in four countries, 1900-2022; the US line as a tune.
7. Free riding measured: conditional cooperators, punishment (Fehr and Gächter 2000), antisocial punishment.
8. The commons: Gordon's fishery (1954), Hardin (1968), the northern cod (1992), Ostrom's design principles (1990).
9. Permits: Dales (1968), Montgomery (1972); the US sulphur dioxide market, its record and its prices (Schmalensee
   and Stavins 2013).
10. Prices against quantities (Weitzman 1974): the slopes that decide; carbon (Pizer 2002).
11. Congestion: Vickrey's bottleneck (1969) and the toll; Stockholm's trial and the vote after it.
12. Network externalities and lock-in (Rohlfs 1974; Katz and Shapiro 1985; Arthur 1989; David 1985); knowledge
    spillovers (Jaffe, Trajtenberg and Henderson 1993), with pointers to Parts 21 and 44.
13. Dials (the fundamental law of road congestion, Duranton and Turner 2011). 14. In practice: carbon taxes, permit
    markets, quotas, spectrum, road charges, standards. 15. Frontier: measuring the damage (Chay and Greenstone 2003;
    Currie and Walker 2011; Deryugina et al. 2019).

*Agora:* `public`: an externality market with Pigou's tax; Coase's table with bargaining and transaction costs; a
public good with Samuelson, Nash and Lindahl; a voluntary-contribution game with typed players and punishment; Gordon's
fishery; Weitzman's comparison; Vickrey's bottleneck; Arthur's lock-in.
*Play it:* the shared pot; on the site, ten rounds against three typed islanders, with and without punishment.
*Dials:* traffic's response to roads (new; settled within a range). *Called it?* the forecast that the acid-rain
programme's benefits would about equal its costs: wrong.
*Reading:* Pigou 1920; Coase 1960, 1974; Samuelson 1954; Cheung 1973; Weitzman 1974; Ostrom 1990; Fehr & Gächter
2000; Schmalensee & Stavins 2013; Gruber chs 5–9; MWG ch 11.

### Part 16 · Auctions (~56)
*Question:* how should something be sold when nobody knows what it is worth to the buyers?
*Story:* in spring 2000 the British government sells five licences for third-generation mobile spectrum in an
auction designed by game theorists. It runs for 150 rounds and raises £22.5 billion, about 2.5% of GDP. The
same year the Netherlands, with the same design and as many licences as incumbents, raises less than a third of what was
forecast.
0. Hook: London and The Hague, 2000; the question; objectives.
1. Play it: one object, sealed bids: first-price, then second-price. Your bids are kept.
2. Four formats: English, Dutch, first-price sealed, second-price sealed; which are the same game.
3. Vickrey (1961): bidding your value is dominant in a second-price auction. The proof by two cases.
4. First-price bidding: shading; the equilibrium bid derived for uniform values.
5. Revenue equivalence: the theorem, by the envelope formula; simulated in four formats.
6. Your bids against the equilibrium and against the published experiments (overbidding; Kagel).
7. Myerson (1981): virtual values, the optimal reserve price; why a seller should sometimes not sell.
8. Common values and the winner's curse: the oil tracts (Capen, Clapp and Campbell 1971); the jar of coins.
9. When equivalence fails: risk aversion, affiliation (Milgrom and Weber 1982), asymmetry, collusion.
10. Designing the spectrum auctions: the simultaneous ascending auction (FCC 1994); the exposure problem;
    package bidding.
11. What went wrong: signalling by trailing digits, the Dutch and Swiss sales (Klemperer 2002).
12. Ad auctions: the generalized second price (Edelman, Ostrovsky and Schwarz 2007; Varian 2007); why it is
    not Vickrey's.
13. Treasury auctions, electricity markets, procurement: uniform against discriminatory prices.
14. Dials. 15. In practice: Part 61; auction desks at regulators. 16. Frontier: auto-bidders, learning
    reserve prices, the 2017 incentive auction.

*Agora:* `auctions`: an auction house (private, common and affiliated values; four formats; reserves), a
generalized second-price position auction, a simultaneous ascending auction.
*Facts:* the winner's curse. *Called it?* revenue forecasts for the 2000 European auctions against outcomes.
*Reading:* Vickrey 1961; Myerson 1981; Milgrom & Weber 1982; Klemperer 2002, 2004; Binmore & Klemperer 2002;
Edelman, Ostrovsky & Schwarz 2007; Krishna; Milgrom, *Putting Auction Theory to Work*.

### Part 17 · Markets by Design (~56)
*Question:* can a market be engineered, when prices cannot do the work?
*Story:* by 1945 American hospitals were offering internships to medical students two years before graduation,
with hours to decide. In 1952 the hospitals adopted a clearinghouse. Thirty years later Alvin Roth showed that
they had rediscovered, a decade early, an algorithm that Gale and Shapley published in 1962 as a puzzle about
marriage.
0. Hook: exploding offers; the question; objectives.
1. Play it: rank three schools under the Boston rule. Should you list your true first choice?
2. Mechanisms: the revelation principle in one picture.
3. Vickrey–Clarke–Groves: charge each person the harm they do to the rest; its virtues and its flaws.
4. Myerson and Satterthwaite (1983): no mechanism gets two-sided bargaining right. Proved in a diagram.
5. Stable matching: blocking pairs; Gale and Shapley's deferred acceptance, run on a board; the proof.
6. The lattice: the proposing side's optimum; who should propose; strategy-proofness for one side only.
7. The residents' match: Roth (1984); couples and the 1998 redesign (Roth and Peranson 1999).
8. School choice: the Boston mechanism against deferred acceptance (Abdulkadiroğlu and Sönmez 2003); New
   York and Boston redesigned; Chinese college admissions and the parallel mechanism.
9. Houses and kidneys: top trading cycles (Shapley and Scarf 1974); kidney exchange and chains (Roth, Sönmez
   and Ünver 2004).
10. Why markets fail to form: unravelling, congestion, unsafe truth-telling, repugnance (Roth 2007).
11. Matching with money: assignment games (Shapley and Shubik); a pointer to Parts 39 and 49.
12. What a lottery reveals: using the match to measure school effects (Abdulkadiroğlu et al. 2017).
13. Dials. 14. In practice: clearinghouses, platforms' matching teams. 15. Frontier: refugee resettlement,
    matching with learning, large markets.

*Agora:* `matching`: deferred acceptance, top trading cycles, the Boston mechanism, VCG, a kidney-exchange
optimizer; manipulation checks.
*Called it?* Roth's test: which regional matches in Britain survived, by whether they were stable.
*Reading:* Gale & Shapley 1962; Roth 1984, 2002, 2007; Myerson & Satterthwaite 1983; Abdulkadiroğlu & Sönmez
2003; Roth, Sönmez & Ünver 2004; Roth & Sotomayor; Roth, *Who Gets What and Why*; Börgers.

### Part 18 · Social Choice and Welfare (~55)
*Question:* can the wants of many people be added up into what society wants?
*Story:* in 1785 the Marquis de Condorcet finds that a majority can prefer A to B, B to C and C to A. In 1950 a
graduate student, Kenneth Arrow, shows that the trouble is not majority rule: every rule fails. The part then
asks what is left for anyone who has to choose a policy.
0. Hook: Condorcet's cycle on three voters; the question; objectives.
1. Play it: one electorate, five voting rules, five winners.
2. Borda against Condorcet; agendas and who sets them.
3. Arrow's conditions; the theorem proved by the pivotal voter (Geanakoplos's proof), step by step.
4. Ways out: single-peaked preferences and the median voter (Black 1948; Downs 1957); May's theorem.
5. Strategic voting: Gibbard and Satterthwaite; the link back to Part 17.
6. More information: interpersonal comparisons; Sen's enlargement of the framework.
7. Welfare functions: Bentham's sum, Rawls's minimum, everything between (Atkinson's ε).
8. Harsanyi's veil (1955) against Rawls's (1971): the same thought experiment, two answers.
9. Pareto and its limits: compensation tests (Kaldor, Hicks, Scitovsky); the Paretian liberal (Sen 1970).
10. Cost–benefit analysis as applied social choice: willingness to pay, distributional weights, an
    *is / ought* card.
11. The value of a statistical life: where the number comes from and what it is not.
12. Discounting the future as an ethical parameter (a pointer to Part 48).
13. Capabilities and what to measure (Sen); a pointer to *Philosophy, Built*.
14. Dials. 15. In practice: Part 58. 16. Frontier: welfare with behavioural agents; quadratic voting;
    preference aggregation for AI systems.

*Agora:* `choice`: a voting lab (rules, profiles, manipulation), a welfare evaluator with adjustable weights.
*Dials:* the value of a statistical life; inequality aversion implied by tax schedules.
*Reading:* Arrow 1951; Sen 1970, 2017; Black 1948; Harsanyi 1955; Rawls 1971; Atkinson 1970; Geanakoplos 2005;
Viscusi & Aldy 2003; MWG chs 21–22.

## Act V · The Long Run

### Part 19 · The Great Escape (~52)
*Question:* why was almost everyone poor for almost all of history, and what changed?
*Story:* in 1798 the Reverend Thomas Malthus explains why living standards can never rise for long. As a
description of every century before his, the theory is good. It is published in the one country, in the one
generation, where it has just stopped being true.
0. Hook: Malthus's essay and the line that turns; the question; objectives.
1. Play it: on a blank axis from the year 1000, mark where income per head begins to climb.
2. The Malthusian model: land, diminishing returns, births and deaths that respond to income; the trap as a
   stable point. Derived, then run.
3. Its predictions tested: better technology buys people, not income (Ashraf and Galor 2011); English real
   wages 1200–1800 (Clark; Allen).
4. The Black Death as an experiment: a third of Europe dies and wages double (verify); the long reversal.
5. Why 1760, why Britain: high wages and cheap coal (Allen 2009); a culture of improvement (Mokyr);
   constitutions and credit (North and Weingast 1989); each with its best case and its critics.
6. Why not China? The Needham question; Pomeranz's coal and colonies; the Yangzi delta against England.
7. The Industrial Revolution in numbers: slow at first (Crafts and Harley); Engels's pause in wages.
8. The demographic transition: mortality, then fertility; the quantity–quality trade-off (Becker and Lewis
   1973).
9. Unified growth theory (Galor and Weil 2000): one model with a trap, an escape and sustained growth.
10. The Great Divergence and the great convergence since 1990; a data film.
11. Was it good? heights, hours and life expectancy; the standard-of-living debate.
12. Dials. 13. In practice: long-run forecasting, development strategy. 14. Frontier: deep roots (Spolaore and
    Wacziarg) and what persistence studies can prove (Kelly 2019).

*Agora:* `malthus`: a Malthusian economy; the same economy with human capital and a transition.
*Facts:* income per head was flat for millennia. *Called it?* Malthus (1798), and Ehrlich's replay (1968).
*Reading:* Malthus 1798; Clark, *A Farewell to Alms*; Allen 2009; Mokyr, *A Culture of Growth*; Pomeranz 2000;
Galor, *Unified Growth Theory*; Koyama & Rubin; Ashraf & Galor 2011; Weil chs 4–5.

### Part 20 · Growth I: Capital (~56)
*Question:* can a country save its way to being rich?
*Story:* a satellite photograph of the Korean peninsula at night: the south a web of light, the north dark,
Pyongyang one dot. In 1956 Robert Solow wrote down one equation for what capital can and cannot do. Its
uncomfortable answer was that most growth comes from something the model does not explain.
0. Hook: the peninsula; the question; objectives.
1. Kaldor's six facts (1961), each checked against the Penn World Table.
2. The Harrod–Domar knife edge and the planners who used it.
3. The Solow model derived: the production function in per-worker form, the fundamental equation, the
   diagram; the steady state.
4. Play it: choose a saving rate and watch a century; then find the golden rule.
5. Transition dynamics and the speed of convergence, derived by linearizing; 2% a year?
6. Convergence: absolute (none), conditional (Barro 1991), and clubs; Mankiw, Romer and Weil's augmented
   model fitted (1992).
7. Growth accounting: Solow's residual (1957), seven-eighths unexplained; what is in it.
8. The East Asian argument: perspiration or inspiration (Young 1995; Krugman 1994; Hsieh 2002).
9. Development accounting: capital explains less than half of income gaps (Hall and Jones 1999; Caselli 2005).
10. Why capital does not flow to poor countries (Lucas 1990).
11. Ramsey's problem (1928): saving chosen, not assumed; the Hamiltonian; the Euler equation; the phase
    diagram and its saddle path, found by shooting.
12. China's growth in the model: reallocation, saving and state firms (Song, Storesletten and Zilibotti
    2011).
13. Dials. 14. In practice: potential-output estimates, long-term fiscal projections. 15. Frontier: the
    growth slowdown since 2005; convergence since 2000 (Kremer, Willis and You 2022).

*Agora:* `growth`: Solow (with human capital), growth and development accounting on the Penn World Table, the
Ramsey model solved by shooting and by time elimination. The Island gets capital.
*Dials:* capital's share; the speed of convergence. *Facts:* Kaldor's facts; conditional convergence.
*Called it?* Solow-model forecasts for Asia; Samuelson's textbook on Soviet overtaking.
*Reading:* Solow 1956, 1957; Ramsey 1928; Cass 1965; Mankiw, Romer & Weil 1992; Young 1995; Hall & Jones 1999;
Jones & Vollrath, *Introduction to Economic Growth*; Jones, *Macroeconomics*, chs 4–6; Acemoglu chs 2–3, 8; Romer
chs 1–2.

### Part 21 · Growth II: Ideas and Institutions (~58)
*Question:* where does the growth that capital cannot explain come from?
*Story:* William Nordhaus measures the price of light in hours of labour, from sesame-oil lamps in Babylon to
the compact fluorescent bulb: it falls by a factor of several hundred thousand (verify). No statistical agency
recorded it. An idea, unlike a lamp, can be used by everyone at once, and Paul Romer built growth theory on
that sentence in 1990.
0. Hook: the price of light; a data film; the question; objectives.
1. Play it: how many hours of work bought an evening's light in 1800, 1900 and 1992?
2. Rival and non-rival goods; why ideas imply increasing returns, and why that breaks perfect competition.
3. The AK model and learning by doing (Arrow 1962; Romer 1986): growth without end, and its scale problem.
4. Romer (1990) derived: varieties, a research sector, monopoly profits as the prize; the balanced path.
5. Creative destruction (Aghion and Howitt 1992): quality ladders; the business-stealing and
   knowledge-spillover wedges; too much research or too little?
6. Scale effects against the data (Jones 1995); semi-endogenous growth; are ideas getting harder to find?
   (Bloom, Jones, Van Reenen and Webb 2020): research effort up, productivity of research down.
7. Diffusion: technology adoption lags (Comin and Hobijn 2010); appropriate technology.
8. Misallocation: the same inputs, less output; the Hsieh–Klenow measure derived; China and India against the
   United States (2009).
9. Institutions: settler mortality as an instrument (Acemoglu, Johnson and Robinson 2001), the reversal of
   fortune, and the critique of the data (Albouy 2012).
10. Borders as experiments: the Koreas, Nogales, the Peruvian *mita* (Dell 2010).
11. Geography, disease and culture: the rival fundamentals, each with its best evidence.
12. Directed technical change (Acemoglu 2002): why innovation leans toward the abundant factor.
13. Patents, prizes and public research: what the evidence says moves innovation.
14. Dials. 15. In practice: R&D policy, productivity analysis. 16. Frontier: a pointer to Part 65; growth
    with declining population (Jones 2022).

*Agora:* an idea-driven economy (Romer; a quality ladder; the semi-endogenous variant) and a misallocation
measure run on the Island's firms.
*Dials:* the social return to R&D; the TFP gain from removing misallocation. *Facts:* the price of light.
*Called it?* scale-effect models against the post-war research boom.
*Reading:* Romer 1990; Aghion & Howitt 1992; Jones 1995, 2005; Bloom et al. 2020; Hsieh & Klenow 2009;
Acemoglu, Johnson & Robinson 2001; Nordhaus 1996; Acemoglu chs 13–15; Warsh.

### Part 22 · Consumption and Saving (~56)
*Question:* how do households decide how much to spend today?
*Story:* in the summer of 2001 the US Treasury mails ten weeks of tax-rebate cheques in an order set by the
last two digits of each taxpayer's Social Security number. The order is random. The theory of the day,
Friedman's, says the date of a cheque known in advance should not matter. It mattered.
0. Hook: the mailing schedule; the question; objectives. A card: not financial advice.
1. Play it: a windfall of a month's income arrives: how much do you spend this quarter?
2. Keynes's consumption function and Kuznets's puzzle: flat in the cross-section, proportional over time.
3. The permanent income hypothesis (Friedman 1957) and the life cycle (Modigliani and Brumberg 1954), from
   Part 7's Euler equation.
4. Hall's random walk (1978): consumption changes should be unpredictable. The test and its failures.
5. Excess sensitivity and excess smoothness (Flavin; Campbell and Mankiw's rule-of-thumb share).
6. Precautionary saving: prudence; the consumption function bends (Zeldes 1989); buffer-stock saving
   (Deaton 1991; Carroll 1997), solved on a grid.
7. The rebate studies: 20–40% spent on nondurables within a quarter (Johnson, Parker and Souleles 2006) and
   the 2008 and 2020 repeats (verify).
8. The wealthy hand-to-mouth (Kaplan and Violante 2014): illiquid houses and high marginal propensities.
9. Your answer against the surveys (Jappelli and Pistaferri 2014; Fuster et al. 2021).
10. Ricardian equivalence (Barro 1974): when a tax cut is not wealth; why it fails.
11. Overlapping generations (Samuelson 1958; Diamond 1965): saving for old age; dynamic inefficiency; when
    a pay-as-you-go pension is a free lunch.
12. Bequests, housing and the saving of the rich; China's saving rate.
13. Dials. 14. In practice: stimulus design, pension reform. 15. Frontier: marginal propensities from
    account data (Ganong and Noel 2019); a pointer to Part 52.

*Agora:* `household` (the life-cycle and buffer-stock problem by the endogenous grid method) and `olg` (Diamond's
economy). The Island's households get a horizon.
*Dials:* the marginal propensity to consume out of a transitory windfall. *Facts:* consumption is smoother
than income. *Called it?* Hall's prediction for anticipated income changes.
*Reading:* Friedman 1957; Modigliani & Brumberg 1954; Hall 1978; Deaton, *Understanding Consumption*; Carroll
1997; Johnson, Parker & Souleles 2006; Kaplan & Violante 2014; Barro 1974; Diamond 1965; Romer ch 8.

### Part 23 · Capital and Asset Prices (~55)
*Question:* what is a claim on the future worth, and how does that decide what gets built?
*Story:* in 1985 Rajnish Mehra and Edward Prescott feed a century of US consumption into the standard model and
ask what stocks should have paid over bills. The model says a fraction of one percent. The record says six
(verify). The gap is still called a puzzle.
0. Hook: the two numbers; the question; objectives. A card: not investment advice.
1. Present value; the Gordon formula; what a change in the discount rate does to a long-lived asset.
2. Investment: the user cost of capital (Jorgenson 1963); Tobin's q (1969); adjustment costs and marginal q
   (Hayashi 1982).
3. Lumpy and irreversible investment: the option to wait (Dixit and Pindyck); uncertainty shocks (Bloom 2009).
4. Modigliani and Miller (1958): the pie and how it is sliced; what breaks it.
5. Play it: price a tree that pays fruit, in good times and bad.
6. The Lucas tree (1978): asset prices from the Euler equation; the stochastic discount factor.
7. Risk premia as covariance with bad times; the consumption CAPM.
8. The equity premium puzzle computed; the Hansen–Jagannathan bound; the risk-free rate puzzle.
9. Three repairs: habits (Campbell and Cochrane 1999), long-run risk (Bansal and Yaron 2004), rare
   disasters (Rietz 1988; Barro 2006).
10. Excess volatility (Shiller 1981) and return predictability; efficient markets in one card (a pointer to
    *Quant, Built* 1, 23–25, 43).
11. Bubbles: rational bubbles and their conditions; experimental bubbles (Smith, Suchanek and Williams 1988).
12. Housing as an asset: the user cost; price-to-rent ratios.
13. Dials. 14. In practice: capital budgeting, valuation, pension discount rates. 15. Frontier: the return
    on everything (Jordà et al. 2019); intermediary asset pricing.

*Agora:* `assets` (a Lucas tree with CRRA, habit and disaster variants; the Hansen–Jagannathan bound) and an
investing firm with adjustment costs. Reuses `explainer.quant.house`.
*Dials:* risk aversion implied by the premium; the investment elasticity to the user cost. *Facts:* the equity
premium; investment's volatility.
*Reading:* Lucas 1978; Mehra & Prescott 1985; Shiller 1981; Hansen & Jagannathan 1991; Tobin 1969; Hayashi
1982; Modigliani & Miller 1958; Cochrane chs 1–2, 21; Romer ch 9.

### Part 24 · Looking for Work (~55)
*Question:* why are there unemployed workers and unfilled jobs at the same time?
*Story:* Peter Diamond imagines an island where coconuts grow on tall palms and a taboo forbids eating your own.
Climbing is only worth it if you expect to meet someone else who climbed. The island has many equilibria, some
of them bad. From that parable comes the model every central bank uses for the labour market.
0. Hook: the coconut taboo; the question; objectives.
1. Stocks and flows: millions of jobs created and destroyed in a quiet month (Davis and Haltiwanger).
2. Play it: wage offers arrive one at a time. Take it or keep looking?
3. Search (Stigler 1961; McCall 1970): the reservation wage derived; your stopping rule against the optimum.
4. The Beveridge curve in US data since 1951 and in JOLTS; its shifts in 2009 and 2021.
5. The matching function: constant returns, estimated (Petrongolo and Pissarides 2001).
6. The Diamond–Mortensen–Pissarides model derived: the job-creation curve, the wage curve, tightness.
7. Nash bargaining and the split of the surplus; comparative statics of benefits, productivity, separations.
8. Efficiency: congestion and thick-market externalities; the Hosios condition (1990).
9. The volatility puzzle (Shimer 2005): the model moves unemployment a tenth as much as the data. Wage
   rigidity (Hall 2005) and the small-surplus calibration (Hagedorn and Manovskii 2008).
10. Ins against outs: what drives unemployment over the cycle (Shimer 2012; Elsby, Michaels and Solon 2009).
11. Job ladders and wage dispersion (Burdett and Mortensen 1998); the wage growth of job switchers.
12. The natural rate and its estimates; duration dependence and scarring.
13. Dials. 14. In practice: labour-market desks, job platforms. 15. Frontier: online vacancies; remote
    work and the geography of search.

*Agora:* `search`: McCall's problem, the DMP model (steady state and dynamics), a job ladder. The Island's
labour market gets frictions.
*Dials:* the matching elasticity; the worker's bargaining share. *Facts:* the Beveridge curve.
*Called it?* the DMP model's predicted volatility against the data.
*Reading:* Diamond 1982; Mortensen & Pissarides 1994; Pissarides, *Equilibrium Unemployment Theory*; Shimer
2005; Hall 2005; Rogerson, Shimer & Wright 2005; Cahuc, Carcillo & Zylberberg chs 5, 9.

## Act VI · Money and the Cycle

### Part 25 · Money (~56)
*Question:* what is money, and what happens when there is too much of it?
*Story:* on the island of Yap the money is limestone wheels, some too large to move. One lies on the seabed,
lost from a raft generations ago, and its owners are still rich. When German administrators wanted roads
built, they painted black crosses on the stones to mark them confiscated, and the islanders went to work
(Furness 1910). In 1932 the Bank of France asked New York to earmark its gold; a drawer was labelled.
0. Hook: the stone on the seabed; the question; objectives.
1. Barter's double coincidence (Jevons 1875); money as medium, unit and store; money as memory
   (Kocherlakota 1998).
2. Play it: three goods, three types of trader: which good ends up as money?
3. Kiyotaki and Wright (1989): money as an equilibrium of search; commodity and fiat money, simulated.
4. From coin to paper: Song-dynasty *jiaozi* (about 1024), goldsmiths' notes, the gold standard, 1971.
5. The quantity equation; velocity; Friedman and Schwartz's long-run evidence; a cross-country scatter.
6. Hyperinflation: Cagan's seven cases (1956); the demand for real balances; the inflation tax and its Laffer
   curve.
7. How four big inflations ended (Sargent 1982): overnight, with a fiscal regime change.
8. Zimbabwe 2008 and Venezuela 2018 in the same framework.
9. Money demand: Baumol–Tobin's trips to the bank derived; the instability of the 1980s.
10. What money is today: the central bank's liabilities and the banks'; T-accounts; how a loan creates a
    deposit (McLeay, Radia and Thomas 2014); the multiplier story and what is wrong with it.
11. Money, interest and prices: the Fisher equation; neutrality and superneutrality.
12. The optimum quantity of money (Friedman 1969).
13. Dials. 14. In practice: reserve management, payments. 15. Frontier: stablecoins as private banknotes,
    central-bank digital currency (a pointer to *Quant, Built* 39).

*Agora:* `money`: a Kiyotaki–Wright economy, a cash-in-advance economy, Cagan's model with adaptive and rational
expectations. The Island gets stone money, then paper.
*Dials:* the interest semi-elasticity of money demand. *Facts:* money growth and inflation in the long run.
*Called it?* Cagan's revenue-maximizing inflation rate against what governments chose.
*Reading:* Jevons 1875; Furness 1910; Friedman 1991 (Yap); Kiyotaki & Wright 1989; Cagan 1956; Sargent 1982;
Friedman & Schwartz 1963; McLeay et al. 2014; Walsh chs 1–4.

### Part 26 · Banks and Runs (~55)
*Question:* why are banks fragile, and can they be made safe?
*Story:* on Thursday 9 March 2023 the customers of Silicon Valley Bank ask to withdraw 42 billion dollars, a
quarter of its deposits, mostly from their phones. A further 100 billion is queued for the morning. The bank
is closed before it opens (verify). The model that explains it was written in 1983, and it explains Overend
Gurney in 1866 as well.
0. Hook: thirty-six hours in March; the question; objectives. A card: not financial advice.
1. What a bank does: liquid deposits, illiquid loans; the balance sheet as T-accounts.
2. Play it: you have a deposit, and a rumour. Stay or withdraw?
3. Diamond and Dybvig (1983) derived: patient and impatient depositors; the contract that insures them.
4. Two equilibria: the same bank, sound and run. Sunspots.
5. Suspension of convertibility; deposit insurance; why insurance that is never paid is cheap.
6. Bagehot's rule (1873): lend freely, at a penalty rate, on good collateral. The Bank of England in 1866.
7. The price: moral hazard; the savings-and-loan crisis; too big to fail.
8. Capital: the buffer and the debate over how much (Admati and Hellwig 2013); risk weights.
9. Runs without depositors: repo and the run of 2007–08 (Gorton and Metrick 2012); money-market funds.
10. One equilibrium after all: global games (Morris and Shin 1998; Goldstein and Pauzner 2005).
11. Runs in the data: the Depression's bank failures (Calomiris and Mason); uninsured deposits in 2023.
12. Banks as monitors (Diamond 1984) and what is lost when they fail (Bernanke 1983).
13. Dials. 14. In practice: supervision, treasury management, deposit pricing. 15. Frontier: digital runs,
    narrow banking, stablecoins.

*Agora:* `bank`: the Diamond–Dybvig economy, a run with sequential service, a global-games threshold, a bank
with a balance sheet and a capital rule. The Island gets a bank.
*Dials:* deposit betas; the output cost of a bank failure. *Called it?* the stress-test scenarios of 2022
against 2023's rate shock.
*Reading:* Diamond & Dybvig 1983; Bagehot, *Lombard Street*; Diamond 1984; Gorton & Metrick 2012; Morris &
Shin 1998; Admati & Hellwig; Freixas & Rochet; Mishkin; Gorton, *Misunderstanding Financial Crises*.

### Part 27 · The Keynesian Revolution (~56)
*Question:* how can a whole economy be short of buyers?
*Story:* on Capitol Hill in the 1970s about 150 couples run a babysitting co-operative on scrip: one coupon, one
half-hour. Couples want a reserve of coupons before a busy season, so they stay in and offer to sit. Nobody
goes out, so nobody can earn. The co-op has a recession, and it ends when the board prints coupons (Sweeney
and Sweeney 1977).
0. Hook: the co-op; the question; objectives.
1. The Depression in data: output, prices, unemployment, 1929–39; what the classics said (Say's law).
2. Play it: you hold three coupons. Hoard or spend?
3. The co-op as a model: desired balances, a general glut, the monetary fix.
4. Keynes (1936): effective demand; the consumption function; Kahn's multiplier (1931) as a geometric series.
5. The paradox of thrift, computed.
6. Hicks's IS–LM (1937) derived: the goods market, the money market, the crossing; fiscal and monetary
   policy in the diagram.
7. The liquidity trap: when the LM curve goes flat; Japan in the 1990s; Krugman's return to it (1998).
8. Phillips's machine: IS–LM in coloured water; what a hydraulic model gets right.
9. Aggregate supply: why prices do not fall enough; sticky wages (Keynes; Bewley's interviews, 1999);
   downward nominal rigidity in pay data.
10. AS–AD; demand and supply shocks; the neoclassical synthesis.
11. What ended the Depression: gold (Eichengreen), money (Romer 1992), war.
12. Keynes's critics then and since: Hayek, the monetarists, the new classicals (the payoff cards).
13. Dials. 14. In practice: desk forecasting still starts here. 15. Frontier: demand shortages from supply
    shocks (Guerrieri, Lorenzoni, Straub and Werning 2022).

*Agora:* the co-op (a monetary economy with precautionary balances) and `islm` (IS–LM and AS–AD with a zero
bound). The Island has a recession.
*Facts:* Okun's law; long expansions and short recessions. *Called it?* Keynes's *Economic Consequences of
the Peace* (1919) on reparations.
*Reading:* Keynes 1936; Hicks 1937; Sweeney & Sweeney 1977; Krugman 1998; Bewley 1999; Eichengreen, *Golden
Fetters*; Romer 1992; Blanchard chs 3–9; Skidelsky.

### Part 28 · Inflation and Expectations (~58)
*Question:* can a country buy lower unemployment with higher inflation?
*Story:* in December 1967 Milton Friedman tells the American Economic Association that the trade-off its members
are steering by will vanish as soon as people come to expect the inflation. Within a decade the United States
has both more inflation and more unemployment than at any time since the war.
0. Hook: the address; the question; objectives.
1. Phillips's curve (1958): a century of British wages; Samuelson and Solow's menu (1960).
2. Play it: forecast next year's inflation, twelve years running, from the history so far.
3. Friedman (1968) and Phelps (1967): the natural rate; the curve shifts with expectations; acceleration.
4. The Great Inflation in data; oil; the curve dissolving.
5. Adaptive expectations, and your forecasts against that rule.
6. Rational expectations (Muth 1961): forecasts consistent with the model; what it does and does not claim.
7. Lucas's islands (1972): a signal-extraction problem; only surprises matter; the policy-ineffectiveness
   result (Sargent and Wallace 1975).
8. The Lucas critique on the Island: a Phillips curve estimated under one rule fails under another.
9. Time inconsistency (Kydland and Prescott 1977; Barro and Gordon 1983): the inflation bias as a game.
10. Volcker, 1979–82: the disinflation and its cost; sacrifice ratios (Ball 1994).
11. Fixes: a conservative central banker (Rogoff 1985), independence (Alesina and Summers 1993), inflation
    targets (New Zealand 1990).
12. The flat Phillips curve of 2000–19; anchored expectations; regional and micro estimates (Hazell,
    Herreño, Nakamura and Steinsson 2022).
13. 2021–23: supply, demand, or a non-linear curve (Bernanke and Blanchard 2023; Benigno and Eggertsson
    2023); each account's best case.
14. Dials. 15. In practice: inflation forecasting, wage bargaining. 16. Frontier: how households and firms
    actually form expectations (Coibion and Gorodnichenko; Weber et al. 2022).

*Agora:* `expectations`: an expectations-augmented economy under adaptive, rational and learning agents; the
signal-extraction islands; the Barro–Gordon game. The Island has an inflation.
*Dials:* the slope of the Phillips curve; the sacrifice ratio. *Facts:* inflation is persistent.
*Called it?* Friedman's 1967 forecast; "team transitory", 2021.
*Reading:* Phillips 1958; Friedman 1968; Phelps 1967; Lucas 1972, 1976; Kydland & Prescott 1977; Barro &
Gordon 1983; Sargent, *The Conquest of American Inflation*; Hazell et al. 2022; Romer ch 6, 12.

### Part 29 · The Cycle as Equilibrium (~58)
*Question:* could booms and slumps be the best response of an economy to shocks it cannot avoid?
*Story:* in 1982 Finn Kydland and Edward Prescott take the growth model, add random shocks to technology, and
claim that the result looks like the US business cycle. If so, recessions are not failures and policy has
nothing to fix. The claim was mostly wrong, and the method won completely: this is the part that teaches it.
0. Hook: the claim; the question; objectives.
1. What a cycle is: Burns and Mitchell (1946); trends and filters (Hodrick–Prescott, band-pass, Hamilton's
   objection); the table of volatilities and comovements.
2. Play it: six unlabelled series around a recession: which one leads?
3. Dynamic programming from scratch: the cake-eating problem; the Bellman equation; the principle of
   optimality.
4. Value function iteration, shown converging; the policy function; why it is a contraction.
5. The stochastic growth model (Brock and Mirman 1972): a closed form, and the general case on a grid.
6. Labour supply in the model: intertemporal substitution; indivisible labour (Hansen 1985; Rogerson 1988).
7. Calibration: choosing parameters from growth facts and micro evidence; the argument with estimation.
8. Log-linearization; the system in matrix form; the saddle-path (Blanchard–Kahn) condition as counting
   eigenvalues.
9. Impulse responses and simulated moments beside the data's.
10. What fits and what does not: hours and productivity; the Solow residual as a measure of shocks.
11. The critics: Summers's sceptical observations (1986); technology shocks that lower hours (Galí 1999);
    money's non-neutrality.
12. What survived: the method, wedges (Chari, Kehoe and McGrattan 2007), news and uncertainty shocks.
13. Dials. 14. In practice: every structural model in a policy institution. 15. Frontier: a pointer to Parts
    51–52.

*Agora:* `dp` (value and policy iteration on grids, Markov chains by Tauchen and Rouwenhorst) and `rbc` (the model
solved globally and by linearization; moments and impulse responses). The Island gets a cycle.
*Dials:* the Frisch elasticity of labour supply (micro against macro). *Facts:* the relative volatilities of
consumption, investment and hours.
*Called it?* the RBC prediction for hours after a technology shock.
*Reading:* Kydland & Prescott 1982; Long & Plosser 1983; King & Rebelo 1999; Prescott 1986; Summers 1986;
Galí 1999; Stokey, Lucas & Prescott chs 1–4; Ljungqvist & Sargent chs 3–4, 12; Romer ch 5.

### Part 30 · Sticky Prices (~58)
*Question:* why does money move the real economy, and what is the best a central bank can do?
*Story:* in 2004 Mark Bils and Peter Klenow open the price collectors' records behind the US consumer price
index and count how often each price changes: every four months or so at the median, far more often than
macroeconomists had assumed, and yet not often enough for money to be neutral. Three equations came out of
that fact and now sit inside every central bank.
0. Hook: the price collectors; the question; objectives.
1. Play it: guess how long a magazine's cover price, a haircut and a litre of petrol go unchanged.
2. The evidence on price setting: Bils and Klenow (2004), Nakamura and Steinsson (2008), sales against
   regular prices; Cecchetti's magazines; Blinder's survey of firms.
3. Why prices stick: menu costs (Mankiw 1985; Akerlof and Yellen 1985): small frictions, large cycles.
4. Monopolistic competition from Part 12: the desired markup.
5. Calvo's fairy (1983): the price-setting problem; the New Keynesian Phillips curve derived.
6. The household's Euler equation as a dynamic IS curve.
7. A rule for the central bank: Taylor (1993) fitted to the Greenspan years.
8. Three equations solved: determinacy and the Taylor principle; impulse responses to a monetary, a demand
   and a cost-push shock.
9. The natural rate of interest; the divine coincidence, and when it fails.
10. Optimal policy: the welfare loss from price dispersion derived; discretion against commitment (Clarida,
    Galí and Gertler 1999).
11. State-dependent pricing (Golosov and Lucas 2007): the selection effect; how much stickiness is left.
12. The zero lower bound: the trap, forward guidance and its puzzle (Del Negro, Giannoni and Patterson).
13. Medium-scale models: habits, wages, capital, indexation (Christiano, Eichenbaum and Evans 2005; Smets
    and Wouters 2007); what each friction buys.
14. Dials. 15. In practice: policy simulations at central banks. 16. Frontier: the model after 2021; a
    pointer to Part 52.

*Agora:* `nk`: the three-equation model and a medium-scale variant, solved by linearization; optimal policy
under discretion and commitment; the zero bound by a piecewise-linear method. The Island gets sticky prices.
*Dials:* the frequency of price changes; the slope of the New Keynesian Phillips curve. *Facts:* most prices
change less than once a quarter; the hump-shaped response.
*Reading:* Calvo 1983; Mankiw 1985; Taylor 1993; Clarida, Galí & Gertler 1999; Bils & Klenow 2004; Nakamura &
Steinsson 2008; Christiano, Eichenbaum & Evans 2005; Smets & Wouters 2007; Galí chs 2–5; Woodford.

### Part 31 · The Central Bank (~58)
*Question:* what does a central bank actually do, and how do we know what it achieves?
*Story:* on 26 July 2012, with Spanish and Italian bond yields at levels that would end the euro, Mario Draghi
adds an unscripted sentence to a speech in London: the ECB will do whatever it takes, "and believe me, it will
be enough." Yields fall for two years. The programme he announced was never used.
0. Hook: the sentence and the yields; the question; objectives.
1. The balance sheet; reserves; how a rate is set: corridors and floors, drawn as T-accounts.
2. Play it: the central banker's chair, 1965–85: set the rate each year with the data of the day.
3. Transmission: rates, credit, asset prices, the exchange rate, expectations.
4. The identification problem: policy responds to the economy. The price puzzle.
5. Four answers: narrative shocks (Romer and Romer 1989, 2004), recursive VARs (Christiano, Eichenbaum and
   Evans 1999), high-frequency surprises around announcements (Kuttner 2001; Gertler and Karadi 2015), and
   the information effect (Nakamura and Steinsson 2018). All four run on the Island, where the shock is
   known.
6. The consensus response: output down after a year or more, prices slower still.
7. Real-time policy: the Taylor rule with the data of the day (Orphanides 2001).
8. The zero bound in practice: 2008, Japan before it.
9. Quantitative easing: what it is in T-accounts; the event-study evidence (Krishnamurthy and
   Vissing-Jorgensen 2011); "works in practice, not in theory".
10. Forward guidance, negative rates, yield-curve control; what each achieved.
11. The neutral rate estimated (Laubach and Williams 2003) and its fall.
12. Lender of last resort and the euro: Draghi's sentence as an equilibrium selection (Part 26).
13. Communication as policy: the dots, the minutes, credibility.
14. Dials. 15. In practice: monetary-policy staff, rates strategy. 16. Frontier: balance-sheet runoff,
    the 2021–24 cycle, central-bank losses.

*Agora:* `cb`: a central bank with a balance sheet and a reaction function inside the Part 30 model; the Island's
monetary history with its true shocks.
*Dials:* the peak effect of a 100-basis-point shock on output and on prices; the neutral real rate; the
yield effect of asset purchases. *Called it?* the Greenbook's forecasts (Romer and Romer 2000).
*Reading:* Romer & Romer 1989, 2004; Christiano, Eichenbaum & Evans 1999; Gertler & Karadi 2015; Nakamura &
Steinsson 2018; Bernanke 2020; Laubach & Williams 2003; Blinder; Ramey 2016.

### Part 32 · The Treasury (~56)
*Question:* what can a government's budget do for the economy, and how much debt is too much?
*Story:* in 2010 Carmen Reinhart and Kenneth Rogoff report that growth falls sharply once public debt passes
90% of GDP, and finance ministers cite it for austerity. In 2013 a graduate student, Thomas Herndon, asked to
replicate it for a class, finds that a spreadsheet formula left out five countries.
0. Hook: the missing rows; the question; objectives.
1. The government's budget constraint; the primary balance; debt dynamics and r minus g, with a simulator.
2. Play it: the minister's budget: stabilize the debt without causing a slump.
3. The multiplier in theory: Keynesian cross, crowding out, the New Keynesian model with and without a zero
   bound.
4. The multiplier in evidence, four designs: structural VARs (Blanchard and Perotti 2002), military news
   (Ramey 2011), regions (Nakamura and Steinsson 2014; Chodorow-Reich 2019), forecast errors (Blanchard and
   Leigh 2013). Why they differ, and the missing intercept.
5. Tax changes: the narrative record (Romer and Romer 2010).
6. Automatic stabilizers; stimulus cheques from Part 22.
7. Austerity: expansionary contractions (Alesina and Ardagna) and the reply; the 90% result after Herndon,
   Ash and Pollin.
8. Is debt a burden? Barro's neutrality, Diamond's crowding out, Blanchard's r below g (2019).
9. Tax smoothing (Barro 1979): why debt should absorb wars.
10. The fiscal theory of the price level (Sims; Cochrane): who backs the money. Unpleasant monetarist
    arithmetic (Sargent and Wallace 1981).
11. Sovereign default: why countries repay at all (Eaton and Gersovitz 1981); the quantitative model
    (Arellano 2008); Argentina and Greece.
12. Modern monetary theory: what it claims, where it agrees with the mainstream, where it does not.
13. Dials. 14. In practice: Part 58; debt-management offices. 15. Frontier: fiscal space with r near g;
    debt and climate investment.

*Agora:* `fiscal`: a fiscal authority in the Part 30 model; debt dynamics; a sovereign-default model by value
iteration. The Island gets a treasury.
*Dials:* the government-spending multiplier (by state of the economy and by design); the tax multiplier.
*Called it?* IMF growth forecasts for the consolidations of 2010–11.
*Reading:* Blanchard & Perotti 2002; Ramey 2011, 2019; Nakamura & Steinsson 2014; Chodorow-Reich 2019; Romer
& Romer 2010; Herndon, Ash & Pollin 2014; Blanchard 2019; Arellano 2008; Barro 1974, 1979.

### Part 33 · Crises (~58)
*Question:* why do financial systems blow up, and why is it so hard to see it coming?
*Story:* the Queen's question, asked at the LSE on 5 November 2008. The answer the British Academy sent her in
July 2009 ends: a failure of the collective imagination of many bright people to understand the risks to the
system as a whole. The part reconstructs what there was to see.
0. Hook: the question and the letter; objectives.
1. Play it: eight credit booms from history, unlabelled: which end in a crisis?
2. The pattern: Kindleberger's anatomy; Minsky's hedge, speculative and Ponzi finance.
3. Debt deflation (Fisher 1933); the Depression's bank failures as lost information (Bernanke 1983).
4. The financial accelerator (Bernanke, Gertler and Gilchrist 1999): net worth and the external finance
   premium.
5. Collateral cycles (Kiyotaki and Moore 1997) derived: land as an input and as security; amplification.
6. Leverage and margins (Geanakoplos 2010; Brunnermeier and Pedersen 2009); fire sales (Shleifer and Vishny).
7. 2008 in order: the house-price boom, subprime, securitization and ratings, the repo run (Part 26), Lehman,
   the freeze.
8. Households: debt, house prices and spending across US counties (Mian and Sufi 2014).
9. A hundred and fifty years in seventeen countries: credit growth predicts crises (Schularick and Taylor
   2012); recessions after credit booms are deeper (Jordà, Schularick and Taylor 2013).
10. Your guesses scored; what the predictors can and cannot do.
11. Fighting it: lender of last resort, guarantees, recapitalization, stress tests (2009); swap lines; what
    the 2008 playbook did in 2020.
12. Macroprudential policy: countercyclical buffers, loan-to-value limits, and the evidence.
13. Emerging-market crises: sudden stops (Calvo), original sin, the IMF's role and record (a pointer to
    Part 34).
14. Dials. 15. In practice: financial-stability departments, risk management (*Quant, Built* 40–41).
16. Frontier: non-linear macro-finance (Brunnermeier and Sannikov 2014); non-bank finance; climate and cyber
    risk.

*Agora:* `credit`: an economy with a collateral constraint (Kiyotaki–Moore), a financial accelerator, and a
crisis predictor fitted to the macrohistory database. The Island has a crisis.
*Dials:* the output cost of a financial crisis; the predictive power of credit growth. *Facts:* credit booms
precede crises.
*Called it?* Rajan at Jackson Hole (2005) and the forecasts of 2007.
*Reading:* Kindleberger; Minsky 1986; Fisher 1933; Bernanke 1983; Kiyotaki & Moore 1997; Bernanke, Gertler &
Gilchrist 1999; Schularick & Taylor 2012; Mian & Sufi, *House of Debt*; Reinhart & Rogoff 2009; Gorton 2010;
Tooze; Bernanke, Geithner & Paulson.

## Act VII · The World Economy

### Part 34 · The Open Economy (~58)
*Question:* what sets the price of one money in terms of another, and what can a country not have at once?
*Story:* on Wednesday 16 September 1992 the Bank of England raises its rate from 10 to 12 percent in the
morning, announces 15 in the afternoon, spends reserves by the billion, and leaves the Exchange Rate Mechanism
by evening. The speculators did not cause the contradiction. They found it.
0. Hook: one day in four acts; the question; objectives.
1. The balance of payments as an identity; the current account as saving minus investment.
2. Play it: you are the governor. Reserves are draining. Defend the peg or let it go?
3. Purchasing power parity: the Big Mac; the Balassa–Samuelson effect; half-lives of three to five years
   (Rogoff 1996).
4. Interest parity, covered and uncovered; the forward premium puzzle (Fama 1984) and the carry trade.
5. Meese and Rogoff (1983): no model beats a random walk out of sample.
6. Mundell–Fleming: IS–LM with a foreign sector; fixed and floating rates; the trilemma as a triangle.
7. Overshooting (Dornbusch 1976) derived: sticky prices, fast asset markets; the phase diagram; the jump.
8. Currency crises, three generations: fundamentals (Krugman 1979), self-fulfilling attacks (Obstfeld 1996),
   balance sheets (Asia 1997). 1992 placed.
9. Sudden stops and original sin; the IMF programme and its critics.
10. Currency areas (Mundell 1961); the euro's design and its crisis, 2010–12 (a pointer back to Part 31).
11. Global imbalances: the saving glut, the "exorbitant privilege", safe assets.
12. The dollar: dominant-currency pricing (Gopinath et al. 2020); the global financial cycle and the
    dilemma (Rey 2013); China's managed float.
13. Dials. 14. In practice: reserve managers, currency strategy, the IMF desk. 15. Frontier: exchange rates
    and financial intermediaries (Gabaix and Maggiori 2015); the exchange-rate disconnect (Itskhoki and
    Mukhin 2021).

*Agora:* `open`: a second island with its own currency; a small open economy (Mundell–Fleming and a New Keynesian
version), Dornbusch's model, a first-generation attack. The Archipelago.
*Dials:* exchange-rate pass-through to import and consumer prices; the half-life of PPP deviations.
*Facts:* exchange rates are a random walk at short horizons. *Called it?* Meese and Rogoff's horse race.
*Reading:* Mundell 1961, 1963; Dornbusch 1976; Krugman 1979; Meese & Rogoff 1983; Obstfeld 1996; Rogoff 1996;
Rey 2013; Gopinath et al. 2020; Krugman, Obstfeld & Melitz chs 13–22; Obstfeld & Rogoff chs 1–4, 9.

### Part 35 · Trade I: Comparative Advantage (~55)
*Question:* why do countries trade, and who wins and loses when they do?
*Story:* the mathematician Stanisław Ulam once challenged Paul Samuelson to name one proposition in all the
social sciences that is both true and not trivial. Years later Samuelson had his answer: Ricardo's comparative
advantage. That it is true needs no argument before a mathematician; that it is not trivial is shown by the
thousands of intelligent people who have never grasped it.
0. Hook: the challenge; the question; objectives.
1. Play it: two countries, two goods, four numbers. One country is worse at both: who should make what?
2. Ricardo (1817): the four numbers; relative prices; the gains for both.
3. Many goods: the chain of comparative advantage; a continuum (Dornbusch, Fischer and Samuelson 1977).
4. A test: Japan forced open in 1859 (Bernhofen and Brown 2004, 2005): the pattern and the size of the gain.
5. Factor proportions: Heckscher and Ohlin; the four theorems in the Lerner diagram.
6. Stolper and Samuelson (1941): trade has losers inside each country, by factor.
7. Leontief's paradox (1953) and the tests since (Trefler 1995: the case of the missing trade).
8. Specific factors: who loses in the short run; why losers are concentrated and gainers diffuse.
9. Tariffs and quotas in partial equilibrium: the two triangles; the large-country optimal tariff.
10. The political economy: protection for sale (Grossman and Helpman 1994); Smoot–Hawley; the Corn Laws.
11. Trade agreements as an escape from a prisoner's dilemma (Bagwell and Staiger 1999); the GATT and WTO.
12. Compensation: the theory and the record of trade adjustment assistance.
13. Dials. 14. In practice: trade ministries, customs analysis. 15. Frontier: testing Ricardo with
    agricultural potential (Costinot and Donaldson 2012).

*Agora:* `trade` (I): Ricardian models with two, many and a continuum of goods; a 2×2×2 Heckscher–Ohlin world;
tariff analysis. The two islands trade.
*Dials:* the gains from trade for one opened economy. *Facts:* rich countries trade similar goods with each
other (the puzzle Part 36 answers).
*Called it?* Heckscher–Ohlin's prediction for US trade against Leontief's table.
*Reading:* Ricardo 1817 ch 7; Stolper & Samuelson 1941; Leontief 1953; Dornbusch, Fischer & Samuelson 1977;
Bernhofen & Brown 2005; Grossman & Helpman 1994; Krugman, Obstfeld & Melitz chs 2–6, 9–10; Feenstra chs 1–3.

### Part 36 · Trade II: Scale, Firms and Gravity (~58)
*Question:* why is most trade between similar countries, and what did a generation of imports from China do?
*Story:* on 26 April 1956 a converted tanker, the *Ideal X*, leaves Newark with fifty-eight truck trailers on
deck. Loading a ship by hand cost $5.86 a ton; Malcom McLean's boxes cost 16 cents (verify). The world that
followed needed a new theory of trade, and got three.
0. Hook: the *Ideal X*; a data film of the trade web; the question; objectives.
1. Intra-industry trade (Grubel and Lloyd 1975): cars for cars.
2. Krugman (1979, 1980): love of variety and scale; trade between identical countries; the home-market
   effect.
3. Play it: guess the trade between two countries from their sizes and the distance.
4. Gravity: Tinbergen (1962); the fit; borders (McCallum 1995) and the repair (Anderson and van Wincoop
   2003): multilateral resistance.
5. Firms: exporters are rare, large and productive (Bernard and Jensen 1995).
6. Melitz (2003) derived: a productivity cutoff, selection, reallocation; trade raises productivity by
   killing firms.
7. Eaton and Kortum (2002): Ricardo with a distribution; gravity from technology.
8. One formula (Arkolakis, Costinot and Rodríguez-Clare 2012): the gain from trade from the home share and
   one elasticity; what it leaves out.
9. Counterfactuals by exact hat algebra (Dekle, Eaton and Kortum 2008).
10. The China shock (Autor, Dorn and Hanson 2013): commuting zones, the shift-share design and its modern
    reading; a decade of slow adjustment; the consumer side.
11. The 2018–19 tariffs: near-complete pass-through to US import prices (Amiti, Redding and Weinstein 2019;
    Fajgelbaum et al. 2020).
12. Value chains: trade in tasks; the iPhone's accounting; resilience (a pointer to Parts 63 and 66).
13. Dials. 14. In practice: trade-policy modelling, supply-chain strategy. 15. Frontier: trade and market
    power; services trade; trade elasticities in the short and long run (Boehm, Levchenko and Pandalai-Nayar
    2023).

*Agora:* `trade` (II): Krugman, Melitz and Eaton–Kortum models; a many-country quantitative model solved by hat
algebra on real trade shares; gravity by PPML.
*Dials:* the trade elasticity; tariff pass-through; local employment effects of import competition.
*Facts:* gravity; exporters are few and productive. *Called it?* the pre-2000 consensus on trade and wages.
*Reading:* Krugman 1979, 1980; Melitz 2003; Eaton & Kortum 2002; Anderson & van Wincoop 2003; Arkolakis,
Costinot & Rodríguez-Clare 2012; Autor, Dorn & Hanson 2013; Levinson, *The Box*; Feenstra chs 5–6; Head & Mayer
2014.

### Part 37 · Cities and Regions (~56)
*Question:* why is economic activity piled up in a few places, and what does that do to the people in them?
*Story:* around 1969 Thomas Schelling, on a plane with nothing to read, starts moving pennies and dimes on a
grid. Each coin moves only if fewer than a third of its neighbours are like it. Nobody wants segregation. The
board segregates almost completely.
0. Hook: the checkerboard, played; the question; objectives.
1. Play it: Schelling's rule on a grid, with your own tolerance threshold.
2. Von Thünen's isolated state (1826): rings of land use from transport cost.
3. The monocentric city (Alonso, Muth, Mills): the rent gradient derived; density; what the car and the
   lift did.
4. Why cities exist: sharing, matching, learning (Marshall 1890; Duranton and Puga 2004); the agglomeration
   elasticity and the sorting problem.
5. Zipf's law for cities; Gibrat's proportional growth (Gabaix 1999).
6. Core and periphery (Krugman 1991): transport costs, scale, a bifurcation, shown as a tomahawk.
7. Spatial equilibrium (Rosen 1979; Roback 1982): wages, rents and amenities move together; reading
   quality of life from prices.
8. Housing supply: regulation and geography (Glaeser and Gyourko; Saiz 2010); the aggregate cost (Hsieh and
   Moretti 2019) and its critics.
9. Rent control: San Francisco's 1994 expansion (Diamond, McQuade and Qian 2019): tenants stay, supply falls.
10. Neighbourhoods: Moving to Opportunity and the children (Chetty, Hendren and Katz 2016); a pointer to
    Part 40.
11. Quantitative spatial models: the Berlin Wall as an experiment (Ahlfeldt, Redding, Sturm and Wolf 2015).
12. Transport: railways in colonial India (Donaldson 2018); highways and suburbs (Baum-Snow 2007); China's
    *hukou* and migration.
13. Place-based policy: Shenzhen and the zones; the Tennessee Valley Authority (Kline and Moretti 2014).
14. Dials. 15. In practice: urban planning, real estate, transport appraisal. 16. Frontier: remote work and
    the donut city; cities and climate.

*Agora:* `city`: a monocentric city, Schelling's model, a Rosen–Roback system of cities, a small quantitative
spatial model. A town grows on the Island.
*Dials:* the agglomeration elasticity; the housing supply elasticity by city. *Facts:* Zipf's law for cities.
*Reading:* Schelling 1971; Alonso 1964; Krugman 1991; Roback 1982; Glaeser, *Triumph of the City*; Duranton &
Puga 2004; Ahlfeldt et al. 2015; Donaldson 2018; Fujita, Krugman & Venables; Redding & Rossi-Hansberg 2017.

## Act VIII · Work and the State

### Part 38 · Work and Wages (~58)
*Question:* what sets a wage, and what happens when the law sets it instead?
*Story:* in early 1992, before New Jersey raises its minimum wage from $4.25 to $5.05, David Card and Alan
Krueger telephone 410 fast-food restaurants on both sides of the Pennsylvania border, and call them again
eight months later. The textbook says employment in New Jersey must fall. It does not.
0. Hook: the phone survey; the question; objectives.
1. Play it: the minimum wage rises by a fifth: predict the change in employment.
2. Labour supply: hours and participation; the backward bend; Hicksian, Marshallian and Frisch elasticities.
3. Do people choose their hours? New York cab drivers (Camerer et al. 1997; Farber 2015) and Uber.
4. Labour demand; the competitive prediction for a wage floor (Stigler 1946).
5. The border design drawn; Card and Krueger's result (1994); the payroll-data reply (Neumark and Wascher
   2000); twenty-five years of designs.
6. The bunching estimator (Cengiz, Dube, Lindner and Zipperer 2019): jobs missing below, jobs added just
   above. Seattle (Jardim et al. 2022).
7. Monopsony (Robinson 1933): one employer, then a few, then search frictions (Manning 2003); the firm-level
   labour supply elasticity measured.
8. The same design on the Island under competition and under monopsony: the method tells them apart.
9. Human capital (Becker 1964); Mincer's equation (1974) fitted.
10. The return to schooling by five designs: quarter of birth (Angrist and Krueger 1991) and its weak
    instruments, twins, distance to college (Card 1995), compulsory-schooling laws, admission cutoffs.
11. Selection: Roy's model (1951) and Heckman's correction (1979); who migrates.
12. Immigration: the Mariel boatlift (Card 1990) and the re-analysis (Borjas 2017); the national approach.
13. Dials. 14. In practice: pay setting, labour ministries, HR analytics. 15. Frontier: employer
    concentration and non-competes; the minimum wage at high levels.

*Agora:* `labour` (I): a labour market under competition, monopsony and search; a Mincer world with ability
bias; a Roy model. The Island's labour market gets its truths planted.
*Dials:* the minimum wage's own-wage employment elasticity; the return to a year of school; the Hicksian and
Frisch elasticities; the firm-level supply elasticity. *Facts:* log wages are linear in schooling.
*Called it?* the 1978 survey in which 90% of economists agreed a minimum wage raises youth unemployment.
*Reading:* Card & Krueger 1994, *Myth and Measurement*; Neumark & Wascher 2000; Cengiz et al. 2019; Manning,
*Monopsony in Motion*; Mincer 1974; Angrist & Krueger 1991; Card 1999; Borjas chs 2–7; Cahuc et al.

### Part 39 · The Wage Structure (~56)
*Question:* why are some people paid so much more than others, and how much of the gap is unfair?
*Story:* in 2001–02 Marianne Bertrand and Sendhil Mullainathan answer 1,300 help-wanted advertisements in Boston
and Chicago with 5,000 invented résumés, identical except for the name at the top. Emily and Greg get one
call-back for every ten résumés. Lakisha and Jamal get one for every fifteen.
0. Hook: the résumés; the question; objectives.
1. The wage distribution since 1963: the college premium, the 90–10 gap, the hollow middle.
2. The race between education and technology (Tinbergen; Katz and Murphy 1992; Goldin and Katz 2008): supply,
   demand and one elasticity.
3. Play it: sort twelve jobs by what computers did to them between 1980 and 2010.
4. Tasks, not skills (Autor, Levy and Murnane 2003): routine and non-routine; polarization (Acemoglu and
   Autor 2011).
5. Robots across commuting zones (Acemoglu and Restrepo 2020); a pointer to Part 65.
6. Firms: the same worker is paid differently in different firms; the two-way fixed-effects model (Abowd,
   Kramarz and Margolis 1999), its bias, and Germany (Card, Heining and Kline 2013); sorting.
7. Superstars (Rosen 1981) and superstar firms; the falling labour share (Autor et al. 2020).
8. Unions: the wage gap, the compression, the decline.
9. Compensating differentials (Rosen 1974): the price of danger and of flexibility.
10. Discrimination in theory: taste (Becker 1957) and why competition may not remove it; statistical
    (Phelps 1972; Arrow 1973).
11. Discrimination measured: audits and correspondence studies; blind auditions (Goldin and Rouse 2000);
    what decompositions can and cannot say.
12. The gender gap: convergence, then the plateau; hours and flexibility (Goldin 2014); the child penalty
    (Kleven, Landais and Søgaard 2019).
13. Dials. 14. In practice: pay equity audits, workforce planning. 15. Frontier: pay transparency;
    bias in hiring algorithms.

*Agora:* `labour` (II): a supply-and-demand model of skill premia; a task-assignment model; a worker–firm
economy on which AKM is run with its truth known.
*Dials:* the elasticity of substitution between college and high-school labour; the firm share of wage
variance; the call-back gap. *Facts:* the gender gap opens at the first child.
*Reading:* Katz & Murphy 1992; Goldin & Katz 2008; Autor, Levy & Murnane 2003; Acemoglu & Autor 2011; Card,
Heining & Kline 2013; Bertrand & Mullainathan 2004; Goldin 2014; Kleven et al. 2019; Becker 1957.

### Part 40 · Inequality and Mobility (~56)
*Question:* how unequal are incomes and wealth, why, and do children escape where they started?
*Story:* in 1971 the Dutch economist Jan Pen asks you to imagine everyone in the country marching past in an
hour, each as tall as their income. For most of the hour you watch people who barely reach your waist. In the
last minutes come giants; in the last seconds, people whose heads are in the clouds.
0. Hook: the parade, as a data film; the question; objectives.
1. Play it: place yourself in the parade (your country, then the world).
2. Measures: Lorenz and Gini (Part 3); Atkinson's index and its ethics; top shares; what each hides.
3. A century of top incomes from tax records (Piketty and Saez 2003): the U; the measurement dispute
   (Auten and Splinter 2024).
4. Pareto tails: the law (1896); where it comes from: random growth with a floor (Champernowne; Gabaix
   2009), derived as a stationary distribution.
5. Why the tail moved so fast (Gabaix, Lasry, Lions and Moll 2016).
6. Wealth: who holds what; r against g (Piketty 2014), and the replies (housing, depreciation, the
   elasticity of substitution).
7. Kuznets's curve (1955) and what became of it.
8. Mobility: the intergenerational elasticity and its measurement; the Great Gatsby curve (Corak 2013).
9. Forty million tax records: rank–rank slopes, absolute mobility falling from 90% to 50% (Chetty et al.
   2014, 2017) (verify).
10. Places: the Opportunity Atlas; movers' designs; what correlates.
11. Global inequality: the elephant curve (Lakner and Milanovic 2016); between against within countries;
    China's and India's part.
12. Does inequality matter for growth, health, politics? What can be identified.
13. Redistribution's instruments (pointers to Parts 41 and 42); pre-distribution.
14. Dials. 15. In practice: distributional analysis. 16. Frontier: distributional national accounts;
    wealth-tax elasticities; genes, family and luck.

*Agora:* `distribution`: a random-growth model of income and wealth with its Kolmogorov equation; an
intergenerational model; inequality measures with standard errors.
*Dials:* the intergenerational elasticity of income; the Pareto exponent of top wealth. *Facts:* Pareto
tails; the Gatsby curve.
*Called it?* Kuznets's inverted U.
*Reading:* Pen 1971; Atkinson 1970; Piketty & Saez 2003; Piketty 2014; Gabaix 2009; Chetty et al. 2014, 2017;
Corak 2013; Milanovic, *Global Inequality*; Auten & Splinter 2024.

### Part 41 · Taxes (~58)
*Question:* who really pays a tax, and how high should the top rate be?
*Story:* in December 1974, in a Washington restaurant, Arthur Laffer draws a curve on a napkin for two aides to
President Ford: at a rate of zero the government collects nothing, and at a hundred percent also nothing. The
curve is correct. The question, which the napkin cannot answer, is where its top is.
0. Hook: the napkin; the question; objectives.
1. Incidence again (Part 2), now in general equilibrium: who pays the corporate tax (Harberger 1962)?
2. Deadweight loss rises with the square of the rate; the Harberger triangle measured.
3. Play it: set the top rate from three numbers.
4. Commodity taxes: Ramsey's rule (1927) derived; Diamond and Mirrlees: do not tax intermediate goods.
5. The income tax as an information problem (Mirrlees 1971): the government sees income, not ability.
6. The optimal top rate derived (Diamond 1998; Saez 2001): one over one plus a times e. The Laffer peak.
7. The whole schedule: the U-shape of marginal rates; the EITC and participation (Saez 2002).
8. Measuring e: the elasticity of taxable income (Feldstein 1995; Saez, Slemrod and Giertz 2012); real
   responses against relabelling; why e is a policy choice.
9. Bunching at kinks and notches (Saez 2010; Kleven and Waseem 2013): the estimator, drawn.
10. Salience: taxes on the shelf tag (Chetty, Looney and Kroft 2009).
11. Capital: the zero-tax results (Atkinson and Stiglitz 1976; Chamley 1986; Judd 1985) and their
    unravelling (Straub and Werning 2020); wealth taxes.
12. Corporations: profit shifting and the missing wealth of nations (Zucman); the global minimum tax.
13. Evasion: Allingham and Sandmo (1972); the Danish audit experiment (Kleven et al. 2011): third-party
    reporting is what works.
14. Dials. 15. In practice: Part 58; tax policy offices. 16. Frontier: optimal taxation with migration,
    with rents, with behavioural taxpayers.

*Agora:* `tax`: an optimal-tax calculator (Ramsey, Mirrlees by simulation, the Saez formulas); a bunching
estimator run on the Island's taxpayers.
*Dials:* the elasticity of taxable income; the Pareto parameter of top incomes; the revenue-maximizing top
rate; corporate-tax incidence on wages.
*Called it?* revenue forecasts for the 1981 and 2017 US tax cuts.
*Reading:* Ramsey 1927; Mirrlees 1971; Diamond & Mirrlees 1971; Saez 2001, 2010; Diamond & Saez 2011; Chetty
2009; Kleven et al. 2011; Zucman 2015; Salanié; Atkinson & Stiglitz; Gruber chs 18–25.

### Part 42 · Social Insurance (~56)
*Question:* what should the state insure, and how generously?
*Story:* in 2008 Oregon has money to add about 10,000 adults to Medicaid and 90,000 people who want in. It
holds a lottery. For the first time since the 1970s there is a randomized experiment on what health insurance
does: to health, to money, to peace of mind.
0. Hook: the draw; the question; objectives. A card: education, not advice.
1. Why markets underinsure (Part 13) and why the state can pool.
2. Play it: set the replacement rate of unemployment benefits.
3. Optimal unemployment insurance: the Baily (1978)–Chetty (2006) formula derived: the gain from smoothing
   against the duration elasticity.
4. Measuring both sides: benefit kinks and extensions (Meyer 1990; Card, Chetty and Weber 2007; Schmieder,
   von Wachter and Bender 2012); the consumption drop (Gruber 1997; Ganong and Noel 2019).
5. Moral hazard or liquidity? (Chetty 2008).
6. Health insurance: Arrow (1963); the RAND experiment (1974–82): people on free care used a third more,
   with little average health effect (verify).
7. Oregon's results: more care, less financial strain and depression, no detectable change in blood pressure
   in two years (Finkelstein et al. 2012; Baicker et al. 2013).
8. Pensions: pay-as-you-go against funded (Part 22); the transition problem; notional accounts.
9. Defaults: enrolment from 37% to 86% by changing a form (Madrian and Shea 2001) (verify); do defaults
   raise saving or move it (Chetty et al. 2014)?
10. Disability insurance: screening and the judges design (Maestas, Mueller-Smith and Strand 2013).
11. Help for the working poor: the negative income tax trials, the EITC (Eissa and Liebman 1996), cash
    against kind, tagging (Akerlof 1978).
12. Basic income: the theory and the recent trials.
13. One yardstick: the marginal value of public funds (Hendren and Sprung-Keyser 2020): 133 policies on one
    axis.
14. Dials. 15. In practice: actuarial offices, programme evaluation. 16. Frontier: social insurance for
    gig work; long-term care; insurance against automation.

*Agora:* `insurance`: an unemployment-insurance designer on the Part 24 labour market; a health-insurance market
with moral hazard and selection; a pension system on the OLG economy.
*Dials:* the duration elasticity of unemployment benefits; the price elasticity of medical spending; the MVPF
of several programmes.
*Reading:* Arrow 1963; Baily 1978; Chetty 2006, 2008; Finkelstein et al. 2012; Madrian & Shea 2001; Hendren &
Sprung-Keyser 2020; Feldstein & Liebman 2002; Gruber chs 12–17.

## Act IX · The Fields

### Part 43 · Measuring Market Power (~58)
*Question:* how do you tell whether a market is competitive when you cannot see anyone's costs?
*Story:* in the 1990s four firms sell most of America's breakfast cereal at margins near forty percent, and
regulators suspect collusion. Aviv Nevo estimates how shoppers substitute between two hundred boxes and finds
that no collusion is needed: differentiated brands and many of them explain the margins. The method came from
a 1995 paper on cars that most economists found unreadable.
0. Hook: the cereal aisle; the question; objectives.
1. Structure, conduct, performance (Bain 1951), and Demsetz's objection (1973): big because efficient?
2. Play it: two proposed mergers among five brands: which raises prices more?
3. Conduct as a parameter (Bresnahan 1982): rotating demand to see the markup.
4. Demand for differentiated products: why a system for 200 goods cannot be estimated directly;
   characteristics space (Lancaster 1966).
5. The logit; independence of irrelevant alternatives and the red bus; nested logit.
6. Random coefficients (Berry, Levinsohn and Pakes 1995) derived: market shares as integrals, the
   contraction that inverts them, the moment conditions, the instruments.
7. BLP run on the Island's car market, where the elasticities are known; then on the public automobile data.
8. From elasticities to markups and marginal costs; Nevo's cereals (2001).
9. Merger simulation; minivans and the value of new goods (Petrin 2002).
10. The supply side instead: production functions and the simultaneity problem (Olley and Pakes 1996;
    Levinsohn and Petrin 2003; Ackerberg, Caves and Frazer 2015).
11. Markups from production data (De Loecker and Warzynski 2012); the rise from 21% to 61% (De Loecker,
    Eeckhout and Unger 2020) (verify) and the measurement critique.
12. Entry thresholds: how many dentists does a town need for competition (Bresnahan and Reiss 1991)?
13. Dials. 14. In practice: Part 59. 15. Frontier: demand estimation with micro data and with learned
    embeddings; common pitfalls of instruments (Gandhi and Houde).

*Agora:* `io` (I): logit, nested-logit and BLP estimators; a merger simulator; Olley–Pakes; an entry model.
*Dials:* own- and cross-price elasticities for cars and cereal; aggregate markups. *Facts:* productivity
differs two to one within industries.
*Reading:* Bresnahan 1989; Berry 1994; Berry, Levinsohn & Pakes 1995; Nevo 2000, 2001; Olley & Pakes 1996;
De Loecker, Eeckhout & Unger 2020; Bresnahan & Reiss 1991; Berry & Haile 2021; Train.

### Part 44 · Dynamics, Platforms and Antitrust (~58)
*Question:* how do firms compete over time, and what is different when the product is a network?
*Story:* Harold Zurcher is the maintenance superintendent of the Madison, Wisconsin bus company. Every month,
for every bus, he decides whether to rebuild the engine or run it another month. In 1987 John Rust writes down
Zurcher's problem as a dynamic programme and recovers, from ten years of his decisions, what he must have
believed a breakdown costs.
0. Hook: Zurcher's ledger; the question; objectives.
1. Play it: the odometer climbs. Replace the engine now or wait?
2. Rust (1987): the optimal stopping problem; the nested fixed point; your rule against Zurcher's.
3. Faster: conditional choice probabilities (Hotz and Miller 1993).
4. Dynamic oligopoly: Markov-perfect equilibrium (Ericson and Pakes 1995); estimation in two steps
   (Bajari, Benkard and Levin 2007); the cement industry (Ryan 2012).
5. Vertical relations: double marginalization; resale price maintenance; foreclosure and the Chicago
   critique.
6. Two-sided markets (Rochet and Tirole 2003; Armstrong 2006): which side pays; why price below cost is not
   predation.
7. Network effects, tipping and lock-in: QWERTY (David 1985) and the reply (Liebowitz and Margolis 1990).
8. Competition and innovation: Arrow's replacement effect against Schumpeter; the inverted U (Aghion et al.
   2005).
9. Killer acquisitions (Cunningham, Ederer and Ma 2021).
10. Pricing algorithms that learn to collude: Q-learners in a Bertrand game (Calvano et al. 2020), run live;
    German petrol stations (Assad et al. 2024).
11. Antitrust's standards: Standard Oil, the consumer-welfare standard, the neo-Brandeisian critique;
    *Microsoft* (2001) and *Google* (2024) (verify), each side's best case.
12. Regulating a firm that knows more than you (Baron and Myerson 1982; Laffont and Tirole 1993).
13. Dials. 14. In practice: Part 59; platform strategy. 15. Frontier: data as a barrier; interoperability;
    competition among foundation models.

*Agora:* `io` (II): Rust's model with nested-fixed-point and CCP estimators; a small Ericson–Pakes industry; a
two-sided platform; Q-learning price setters.
*Dials:* indirect network effects on a platform; merger price effects from retrospectives.
*Called it?* merger retrospectives against the agencies' predictions (Ashenfelter, Hosken and Weinberg).
*Reading:* Rust 1987; Hotz & Miller 1993; Ericson & Pakes 1995; Rochet & Tirole 2003; Aghion et al. 2005;
Calvano et al. 2020; Cunningham, Ederer & Ma 2021; Tirole 2017, *Economics for the Common Good*; Whinston 2006.

### Part 45 · Behavioural Economics (~56)
*Question:* what changes in economics when people are not the agents of Part 5?
*Story:* Stefano DellaVigna and Ulrike Malmendier obtain the attendance records of 7,752 members of three
New England gyms. Members on the monthly contract pay about $70 and go four times: $17 a visit. A ten-visit
pass costs $10 a visit. They are paying not to go to the gym (2006).
0. Hook: the gym; the question; objectives.
1. Three departures (DellaVigna 2009): non-standard preferences, beliefs and decision making.
2. Play it: you are given a mug. Name your selling price. (Others name a buying price.)
3. Reference dependence: the endowment effect (Kahneman, Knetsch and Thaler 1990) and experienced traders
   (List 2003); prospect theory in one card (*Psychology, Built* 26).
4. In the field: marathon finish times bunch at round numbers (Allen et al. 2017); golfers putt better for
   par (Pope and Schweitzer 2011); house sellers (Genesove and Mayer 2001).
5. Present bias: beta–delta (Laibson 1997); sophisticates and naifs (O'Donoghue and Rabin 1999); the gym
   contract as a commitment device that fails.
6. Commitment demanded: SEED accounts in the Philippines (Ashraf, Karlan and Yin 2006).
7. Defaults and inertia (Part 42); Save More Tomorrow (Thaler and Benartzi 2004).
8. Inattention: shrouded fees (Gabaix and Laibson 2006); left-digit bias in used cars (Lacetera, Pope and
   Sydnor 2012).
9. Social preferences: inequity aversion (Fehr and Schmidt 1999); gift exchange in the field; what dictator
   games do and do not measure (List 2007).
10. Do markets cure it? Arbitrage, learning, and firms that profit from bias.
11. Behavioural welfare: whose preference counts (Bernheim and Rangel 2009); nudges and their critics.
12. Nudges at scale: the published effect is 8.7 points, the nudge units' 1.4 (DellaVigna and Linos 2022).
13. Models of limits: rational inattention (Sims 2003), sparsity (Gabaix 2014); expectations that
    overreact (Bordalo, Gennaioli and Shleifer).
14. Dials. 15. In practice: product design, consumer protection, pensions. 16. Frontier: structural
    behavioural economics; behavioural macro.

*Agora:* `behave`: reference-dependent, present-biased and inattentive agents that drop into the Island's
markets; a contract designer who exploits them. Reuses `explainer.psychology.psyche.choice`.
*Dials:* loss aversion; present bias (β); the effect of a default. *Called it?* experts' forecasts of nudge
effects (DellaVigna and Pope).
*Reading:* Kahneman & Tversky 1979; Thaler 1980; Laibson 1997; DellaVigna & Malmendier 2006; DellaVigna 2009;
List 2003; Bernheim & Rangel 2009; DellaVigna & Linos 2022; Thaler, *Misbehaving*; Dhami.

### Part 46 · Development (~58)
*Question:* why do the poor stay poor, and what actually helps?
*Story:* a bed net treated with insecticide costs a few dollars and prevents malaria. For years donors argue
whether to give nets away or sell them cheaply, so that only people who value them take one and people who pay
use it. In Kenya in 2007 Jessica Cohen and Pascaline Dupas randomize the price. At sixty cents, demand falls
by sixty percent, and those who pay use the net no more than those who do not (verify).
0. Hook: the price of a net; the question; objectives.
1. Counting the poor: a dollar a day and its descendants; whose prices (Deaton 2010).
2. Play it: a fixed aid budget and six programmes: spend it.
3. Poverty traps: the S-shaped curve; what the evidence finds (Kraay and McKenzie 2014; Balboni et al. 2022).
4. Dual economies and structural change (Lewis 1954); the productivity gap between farm and town (Gollin,
   Lagakos and Waugh 2014).
5. Credit: why the moneylender charges so much; group lending; six randomized evaluations of microcredit:
   modest, not transformative (Banerjee, Karlan and Zinman 2015).
6. Cash: PROGRESA's design (1997) and results (Schultz 2004); unconditional transfers (Haushofer and Shapiro
   2016); a village-level multiplier (Egger et al. 2022).
7. The graduation programme in six countries (Banerjee et al. 2015) and BRAC's long run.
8. Schools: Indonesia's 61,000 schools (Duflo 2001); teaching at the right level; learning against
   schooling.
9. Health: deworming and the "worm wars" (Miguel and Kremer 2004; the 2015 re-analyses); pricing preventive
   goods.
10. Risk: informal insurance in Indian villages (Townsend 1994); rainfall insurance that nobody buys.
11. Technology and firms: fertilizer and present bias (Duflo, Kremer and Robinson 2011); mobile money
    (Suri and Jack 2016); management (a pointer to Part 62).
12. History that persists: the *mita* (Dell 2010), the slave trades (Nunn 2008).
13. The debate over experiments: external validity, general equilibrium, big questions (Deaton 2010;
    Banerjee and Duflo); China's poverty reduction, with no experiment behind it.
14. Dials. 15. In practice: evaluators, the development banks, GiveWell-style cost-effectiveness.
16. Frontier: scaling (Muralidharan and Niehaus 2017); targeting with satellites and phones.

*Agora:* `village`: a village economy with a non-convex technology (a trap), informal insurance and a credit
market; a randomized roll-out run on it with spillovers.
*Dials:* the return to capital for microenterprises; the consumption effect of a cash transfer; the return to
schooling in poor countries.
*Called it?* Sachs's and Easterly's forecasts for the Millennium Villages.
*Reading:* Lewis 1954; Banerjee & Duflo, *Poor Economics*; Duflo 2001; Miguel & Kremer 2004; Cohen & Dupas
2010; Banerjee et al. 2015; Deaton 2010; Dell 2010; Ray; Sen, *Development as Freedom*.

### Part 47 · Political Economy (~55)
*Question:* why do governments so often choose policies that economists can show are wasteful?
*Story:* Benjamin Olken wants to know how much of the money for 600 Indonesian village roads is stolen. He
hires engineers to dig core samples out of each finished road and price the materials actually in it. About a
quarter of the spending is missing. Then he randomizes two cures: an audit from above, and village meetings
from below (2007).
0. Hook: the core samples; the question; objectives.
1. The logic of collective action (Olson 1965): small groups beat large ones; the sugar quota.
2. Play it: a hundred tokens: fund the public good, or lobby for a share?
3. Rent seeking (Tullock 1967; Krueger 1974): the rectangle is spent chasing the rectangle.
4. Voters: the median voter (Part 18); probabilistic voting; do voters affect policy or only elect
   (Lee, Moretti and Butler 2004)?
5. Lobbying and capture (Stigler 1971; Grossman and Helpman 1994); the value of connections (Fisman 2001).
6. Agency in government: elections as contracts (Barro 1973; Ferejohn 1986); term limits.
7. Olken's results: audits cut missing spending by eight points; meetings barely moved it (verify).
8. Corruption measured four ways: core samples, stock prices, parking tickets (Fisman and Miguel 2007),
   surveys.
9. Why bad institutions persist: commitment problems (Acemoglu and Robinson 2006); the franchise.
10. State capacity (Besley and Persson 2009); democracy and growth (Acemoglu et al. 2019).
11. Conflict: rainfall and civil war (Miguel, Satyanath and Sergenti 2004); the resource curse.
12. Media and persuasion (DellaVigna and Kaplan 2007); trade shocks and polarization (Autor et al. 2020).
13. Political business cycles; delegation as a remedy (central banks, fiscal councils).
14. Dials. 15. In practice: governance work, regulatory design, political risk. 16. Frontier: the
    economics of populism; state capacity in the digital age.

*Agora:* `politics`: probabilistic voting with lobbying; a rent-seeking contest; an agency model of politicians;
a two-group model of franchise extension.
*Dials:* the share of spending lost to corruption in audited programmes; the incumbency advantage.
*Reading:* Olson 1965; Tullock 1967; Krueger 1974; Stigler 1971; Olken 2007; Acemoglu & Robinson 2006, 2012;
Besley & Persson 2011; Persson & Tabellini; Fisman & Miguel 2007.

### Part 48 · Environment and Climate (~58)
*Question:* what is a tonne of carbon dioxide worth, and what does the answer turn on?
*Story:* in 1980 the economist Julian Simon offers the biologist Paul Ehrlich a bet: pick any raw materials, and
in ten years their real prices will be lower. Ehrlich picks chromium, copper, nickel, tin and tungsten. In
1990 he posts a cheque for $576.07. With other start dates he would mostly have won.
0. Hook: the bet and the cheque; the question; objectives.
1. Exhaustible resources: Hotelling's rule (1931) derived; why real resource prices have not risen at the
   rate of interest.
2. The bet rerun for every decade since 1900 (Kiel, Matheson and Golembiewski 2010).
3. Renewable resources: the fishery's dynamics; open access; tradable quotas (Costello, Gaines and Lynham
   2008).
4. Climate as the largest externality (Part 15): the carbon cycle and temperature in four equations.
5. A climate–economy model built: DICE (Nordhaus 1992), from the Ramsey model of Part 20.
6. Play it: choose the discount rate and watch the carbon price.
7. The social cost of carbon; Stern (2006) against Nordhaus: the Ramsey rule's two parameters as ethics and
   as evidence; an *is / ought* card.
8. Fat tails: Weitzman's dismal theorem (2009); insurance against catastrophe.
9. Instruments: taxes against permits again; the EU's market; British Columbia's tax; standards and
   subsidies.
10. Leakage, border adjustments and climate clubs (Nordhaus 2015).
11. Innovation: learning curves for solar and batteries; directed technical change (Acemoglu et al. 2012).
12. Damages measured: temperature and output (Dell, Jones and Olken 2012; Burke, Hsiang and Miguel 2015);
    mortality; the Huai River heating line (Chen et al. 2013; Ebenstein et al. 2017).
13. Electricity markets: merit order, scarcity, and California in 2000–01 (Borenstein, Bushnell and Wolak
    2002).
14. Dials. 15. In practice: Part 58; energy trading and regulation. 16. Frontier: tipping points;
    adaptation; the macroeconomics of the transition.

*Agora:* `climate`: a Hotelling extractor, a fishery, and a DICE-style integrated assessment model with
adjustable discounting and damages; a merit-order electricity market.
*Dials:* the social cost of carbon (as a function of the discount rate); the price elasticity of gasoline and
of electricity demand; the output effect of a degree of warming.
*Called it?* Simon against Ehrlich; solar-cost forecasts against outcomes.
*Reading:* Hotelling 1931; Nordhaus 1992, 2008, 2015; Stern 2007; Weitzman 2009; Acemoglu et al. 2012; Burke,
Hsiang & Miguel 2015; Borenstein, Bushnell & Wolak 2002; Hsiang & Kopp 2018; Sabin, *The Bet*; Nordhaus, *A Question
of Balance*.

### Part 49 · The Economic Approach (~55)
*Question:* how far can the model of choice under constraint be pushed into the rest of life?
*Story:* in the 1960s Gary Becker, late for a student's oral examination, weighs the price of a car park against
the chance of a ticket for parking in the street, and parks in the street. By the time he reaches the room he
has the outline of "Crime and Punishment: An Economic Approach" (1968). The method went on to marriage,
children, addiction and school, and the part asks what it found and where it failed.
0. Hook: the parking space; the question; objectives.
1. Crime as a choice: probability against severity; the optimal fine.
2. Play it: does doubling the fine or doubling the chance of being caught deter more?
3. Deterrence measured: police and crime (Levitt 1997 and its correction; Di Tella and Schargrodsky 2004;
   Chalfin and McCrary 2017); certainty beats severity; incapacitation.
4. The family: household production and the allocation of time (Becker 1965).
5. Marriage as a matching market (Becker 1973; Part 17): assortative mating; marital surplus estimated
   (Choo and Siow 2006).
6. Fertility: quantity and quality; the pill (Goldin and Katz 2002); China's one-child policy and its
   evidence.
7. Bargaining inside the household: who gets the child benefit (Lundberg, Pollak and Wales 1997).
8. Schools: class size in Tennessee's STAR and by Maimonides' rule (Angrist and Lavy 1999); teacher value
   added (Chetty, Friedman and Rockoff 2014); charter lotteries.
9. Early childhood: Perry Preschool and the Heckman curve; what replicates.
10. Health: the demand for health (Grossman 1972); physicians who induce demand; hospital prices
    (Cooper et al. 2019).
11. Drugs and patents: the price of innovation; deaths of despair and the opioid supply (Case and Deaton
    2015; Alpert et al. 2022).
12. Addiction: rational (Becker and Murphy 1988) and otherwise (Part 45).
13. The critics of "economics imperialism", and the reply.
14. Dials. 15. In practice: criminal-justice policy, school districts, health systems. 16. Frontier: the
    economics of fertility decline; marriage markets with skewed sex ratios.

*Agora:* `family`: a deterrence model, a transferable-utility marriage market (Choo–Siow), a household
bargaining model, an education production function with value-added estimation.
*Dials:* the elasticity of crime to police; the effect of class size; the variance of teacher value added.
*Reading:* Becker 1965, 1968, 1973, *A Treatise on the Family*; Chalfin & McCrary 2017; Angrist & Lavy 1999;
Chetty, Friedman & Rockoff 2014; Grossman 1972; Case & Deaton 2020; Heckman 2006.

### Part 50 · The Policy Memo (the capstone, ~50)
*Question:* a minister asks whether to do it. What do you write?
*Story:* one real proposal, chosen in Phase 2 (candidates: a national minimum wage at two-thirds of the median;
a carbon tax with a dividend; congestion pricing for one city; a child allowance). The part carries it from the
question to a four-page memo, using only what the series has built.
0. Hook: the request and the deadline; objectives.
1. The question made answerable: who is affected, through which markets, over what horizon.
2. The market in partial equilibrium: incidence and surplus (Parts 2, 10).
3. Who responds and how much: the Dials that matter, with their ranges (Parts 4, 38, 41).
4. Play it: before the analysis, what would you advise? Kept.
5. The margins that textbook pictures miss: information, market power, behaviour (Parts 13, 38, 45).
6. General equilibrium: prices, firms' entry and location, the budget (Parts 9, 32, 37).
7. The evidence: the three best designs, what each identifies, how they transfer to this case.
8. The policy run on the Island under the range of the Dials: the distribution of outcomes.
9. The budget cost and the marginal value of public funds (Parts 42, 58).
10. Who gains and who loses: the distribution table; an *is / ought* card.
11. The uncertainty, stated: what would change the advice.
12. The memo, written on screen; the two-minute oral version; your advice revisited.
13. In practice: how such memos are used and misused. 14. Frontier: what remains unidentified for this
    policy.

*Agora:* the capstone analysis, reproducible from one script. *Dials:* audited: every row used in the memo is
re-checked. *Reading:* the part's own source list; Gruber; Boardman et al.; Angrist & Pischke.

## Act X · The Graduate Core

This act is the toolkit that turns Acts II–IX into research. It assumes the model chapters of those acts.

### Part 51 · Computing Economies (~58)
*Question:* how is an economy that has no formula solved, and how do you know the answer is right?
*Story:* in 1950 at RAND, Richard Bellman needs a name for his work on multistage decisions that will not alarm
a Secretary of Defense who hates the word "research". He picks "dynamic programming": nobody can object to
"dynamic". Seventy years later a single household's saving problem inside a macro model is solved a million
times in one estimation run.
0. Hook: the name; the question; objectives.
1. The Bellman operator as a contraction: Blackwell's two conditions; the fixed-point theorem, drawn.
2. Value function iteration, timed; Howard's policy iteration; why it is so much faster.
3. Play it: three grids and their answers: which is fine enough?
4. Interpolation and the grid: linear, splines, Chebyshev; where to put the points.
5. The endogenous grid method (Carroll 2006): no root finding. The household of Part 22, a hundred times
   faster.
6. Projection methods (Judd 1992): the policy function as a polynomial; collocation, Galerkin.
7. Perturbation: first and second order around the steady state; when certainty equivalence misleads.
8. Accuracy: Euler-equation errors (Den Haan and Marcet 1994); a method is not solved until this is shown.
9. Expectations: quadrature, Tauchen and Rouwenhorst; simulation error.
10. Continuous time: the Hamilton–Jacobi–Bellman equation by upwind finite differences (Achdou et al.
    2022); why it is sparse and fast.
11. Occasionally binding constraints: the zero bound and borrowing limits.
12. The curse of dimensionality (Bellman 1957); sparse grids (Smolyak); a pointer to deep solvers (Part 64).
13. Reproducibility: seeds, tolerances, tests; what a replication package must contain.
14. Dials. 15. In practice: model teams at central banks; structural estimation. 16. Frontier:
    differentiable programming for economic models.

*Agora:* `solve`: one harness for value and policy iteration, endogenous grids, projection, perturbation and
finite-difference HJB, each with an Euler-error report; every earlier dynamic module moves onto it.
*Reading:* Bellman 1957; Stokey, Lucas & Prescott chs 3–4, 9; Judd, *Numerical Methods in Economics*; Carroll
2006; Den Haan & Marcet 1994; Aruoba, Fernández-Villaverde & Rubio-Ramírez 2006; Achdou et al. 2022; Sargent &
Stachurski; Fernández-Villaverde, Rubio-Ramírez & Schorfheide 2016.

### Part 52 · Many Agents (~60)
*Question:* what does macroeconomics get wrong by treating a country as one household?
*Story:* in 1992 Alan Kirman asks whom or what the representative individual represents, and answers: nobody.
Six years later Per Krusell and Anthony Smith solve an economy with a whole distribution of households and
find, to general relief, that the average behaves almost as if there were one. Twenty years after that, a
model with a realistic distribution reverses the textbook account of how monetary policy works.
0. Hook: Kirman's question; the question; objectives.
1. Aggregation: when one household is exact (Gorman) and why it almost never is.
2. Incomplete markets: uninsurable income risk and a borrowing limit (Bewley 1977; Huggett 1993).
3. The Aiyagari economy (1994) derived: the household's problem, the stationary distribution, the capital
   market; the equilibrium interest rate below the rate of time preference.
4. Solved on the Island with 100,000 households (Part 51's methods); Aiyagari's table reproduced.
5. Play it: rates fall by a point: whose spending moves, and why?
6. The wealth distribution: what the basic model misses at the top; fixes (heterogeneous discounting,
   entrepreneurs, returns: Benhabib, Bisin and Zhu).
7. Aggregate shocks: the state is a distribution. Krusell and Smith (1998): approximate aggregation, R²
   of 0.999998 (verify), and when it fails.
8. Continuous time: an HJB equation and a Kolmogorov forward equation as one system (Achdou et al. 2022).
9. HANK (Kaplan, Moll and Violante 2018): liquid and illiquid assets; the direct effect of a rate cut is
   small, the indirect effect through incomes is most of it.
10. Sequence-space Jacobians (Auclert, Bardóczy, Rognlie and Straub 2021): linearize in aggregates, not in
    the distribution; the model solved in seconds.
11. What changes for policy: fiscal multipliers, forward guidance, who gains from inflation (Doepke and
    Schneider 2006).
12. Firms: Hopenhayn (1992) and entry; lumpy investment and whether it aggregates (Khan and Thomas 2008).
13. Dials. 14. In practice: distributional analysis of monetary policy at central banks. 15. Frontier:
    estimation with micro data; heterogeneity in beliefs; climate and inequality in one model.

*Agora:* `hetero`: Aiyagari, Krusell–Smith, a two-asset HANK by sequence-space Jacobians, Hopenhayn's industry.
The Island's population becomes the model.
*Dials:* the average MPC implied by each model against Part 22's row. *Facts:* Pareto tails in wealth;
consumption smoother than income, household by household.
*Reading:* Bewley 1977; Huggett 1993; Aiyagari 1994; Krusell & Smith 1998; Kaplan, Moll & Violante 2018;
Auclert et al. 2021; Achdou et al. 2022; Hopenhayn 1992; Ljungqvist & Sargent chs 17–18; Kirman 1992.

### Part 53 · Information and Persuasion (~58)
*Question:* how does someone who controls only what others learn get them to do what she wants?
*Story:* a prosecutor wants convictions. The judge convicts only if guilt is more likely than not, and knows
that 30% of defendants are guilty. The prosecutor cannot lie, but she chooses which investigation to run. With
the right one, the judge convicts 60% of defendants, every time correctly following the evidence (Kamenica
and Gentzkow 2011).
0. Hook: the prosecutor's arithmetic; the question; objectives.
1. Play it: design the test the judge will see.
2. Bayesian games: types, beliefs, Bayes–Nash equilibrium (Harsanyi 1967–68).
3. Dynamic games of incomplete information: perfect Bayesian and sequential equilibrium; beliefs off the
   path; refinements revisited (Part 13).
4. Cheap talk (Crawford and Sobel 1982): the partition equilibria derived; more aligned, more informative.
5. Bayesian persuasion: the sender's value as a function of the belief; concavification, drawn.
6. Information design with many receivers (Bergemann and Morris 2019); correlated equilibrium again.
7. Blackwell's order (1953): when one experiment is worth more than another to everyone.
8. Common knowledge: agreeing to disagree (Aumann 1976); the email game (Rubinstein 1989): almost common
   knowledge is not enough.
9. Global games (Carlsson and van Damme 1993; Morris and Shin 1998) derived: a little private noise selects
   one equilibrium. Part 26 and Part 34 revisited.
10. Herds and cascades (Banerjee 1992; Bikhchandani, Hirshleifer and Welch 1992): rational people ignoring
    what they know.
11. Reputation: the chain-store paradox and its resolution (Kreps and Wilson 1982; Milgrom and Roberts
    1982).
12. Bargaining: Nash's axioms (1950); Rubinstein's alternating offers (1982), solved; delay under
    incomplete information.
13. Relational contracts (Levin 2003); repeated games with imperfect monitoring in one picture.
14. Dials. 15. In practice: rating design, disclosure rules, central-bank communication, platform
    recommendation. 16. Frontier: robust mechanism design; information design with learning algorithms.

*Agora:* `persuade`: Bayesian-game solvers, a cheap-talk solver, concavification for finite states, a global-game
threshold, a cascade simulator, Rubinstein bargaining.
*Reading:* Harsanyi 1967–68; Crawford & Sobel 1982; Kamenica & Gentzkow 2011; Bergemann & Morris 2019;
Rubinstein 1982, 1989; Morris & Shin 2003; Banerjee 1992; Kreps & Wilson 1982; Fudenberg & Tirole chs 6–10.

### Part 54 · Estimating Models (~60)
*Question:* how is a model's hidden machinery measured from the choices it predicts?
*Story:* in the early 1970s the Bay Area is building a railway, BART. The official forecast is that 15% of
commuters will take it. Daniel McFadden fits a model of choice to survey answers gathered before a single
train runs, and predicts 6.3%. The share turns out to be 6.2% (verify).
0. Hook: the forecast; the question; objectives.
1. What "structural" means: parameters that stay put when policy changes (Part 4's Lucas critique).
2. Random utility and the logit derived from extreme-value errors (McFadden 1974); maximum likelihood.
3. Play it: four moments and three parameters: which moment pins down which?
4. The generalized method of moments (Hansen 1982) derived: the weighting matrix, efficiency, the
   J-test; Euler equations estimated without solving the model (Hansen and Singleton 1982).
5. When the likelihood has no formula: simulation (McFadden 1989; Pakes and Pollard 1989); simulated
   moments; indirect inference (Gouriéroux, Monfort and Renault 1993).
6. A full example on the Island: the life-cycle household of Part 22 estimated by simulated moments
   (Gourinchas and Parker 2002); the truth recovered, with standard errors.
7. Dynamic discrete choice in general: Part 44's Rust model as the template; unobserved heterogeneity
   (Heckman and Singer 1984; Keane and Wolpin 1997).
8. Identification: what variation moves which parameter; sensitivity of estimates to moments (Andrews,
   Gentzkow and Shapiro 2017).
9. Calibration against estimation: the argument, and the modern compromise.
10. Sufficient statistics (Chetty 2009): the welfare answer from two elasticities, without the model; what
    it cannot do.
11. Validation: estimate before the experiment, predict the experiment (Todd and Wolpin 2006 on PROGRESA).
12. Partial identification (Manski): bounds instead of points.
13. Dials. 14. In practice: Parts 59–61; pricing and demand teams. 15. Frontier: estimation with machine
    learning inside (neural-network estimators; simulation-based inference).

*Agora:* `estimate`: one harness for ML, GMM, SMM and indirect inference with standard errors, a J-test and the
Andrews–Gentzkow–Shapiro sensitivity matrix; every Island model can be handed to it with its truth hidden.
*Called it?* McFadden's BART forecast; Todd and Wolpin's.
*Reading:* McFadden 1974, 1989; Hansen 1982; Hansen & Singleton 1982; Rust 1987; Keane & Wolpin 1997;
Gourinchas & Parker 2002; Chetty 2009; Andrews, Gentzkow & Shapiro 2017; Todd & Wolpin 2006; Train; Hayashi
chs 3–4, 7; Low & Meghir 2017; Wooldridge, *Econometric Analysis of Cross Section and Panel Data*; B. Hansen,
*Econometrics*.

### Part 55 · Identifying Macro (~60)
*Question:* with one history and no control group, how can anyone say what a policy did?
*Story:* in 1992 Christopher Sims runs the most careful vector autoregressions of his day on five countries and
finds that when a central bank raises its rate, prices rise. It is called the price puzzle, and it is what
identification failing looks like: the bank raised rates because it saw inflation coming.
0. Hook: the puzzle; the question; objectives.
1. The reduced-form VAR (Sims 1980); impulse responses; what is and is not identified.
2. Play it: three unlabelled impulse responses: which shock was it?
3. Identification 1: timing (recursive ordering). 2: long-run restrictions (Blanchard and Quah 1989).
   3: sign restrictions (Uhlig 2005). 4: external instruments (Stock and Watson 2012; Mertens and Ravn 2013).
   5: heteroskedasticity (Rigobon 2003).
4. All five run on the Island's history, where the monetary shock is known: which recover it.
5. Local projections (Jordà 2005); the same estimand as a VAR (Plagborg-Møller and Wolf 2021); bias
   against variance.
6. Narrative and high-frequency shocks as instruments (Part 31); the price puzzle resolved.
7. Estimating a DSGE model: the state-space form and the Kalman filter (statkit `ts`); the likelihood;
   Bayesian estimation by Metropolis–Hastings (An and Schorfheide 2007); Smets and Wouters's shocks.
8. What the data cannot tell apart: weak identification in DSGE models (Canova and Sala 2009).
9. Cross-sectional macro: regional multipliers and the missing intercept (Nakamura and Steinsson 2014;
   Wolf 2023); shift-share designs (Goldsmith-Pinkham, Sorkin and Swift 2020; Borusyak, Hull and Jaravel
   2022).
10. Matching impulse responses (Christiano, Eichenbaum and Evans 2005); moments from micro data in macro
    models.
11. Forecasting as a test: the models' record around 2008 and 2021 (a pointer to Part 57).
12. What macroeconomics knows and how (Nakamura and Steinsson 2018; Ramey 2016).
13. Dials. 14. In practice: central-bank research departments. 15. Frontier: heterogeneous-agent models
    estimated on micro and macro data together; identification with expectations data.

*Agora:* `macrometrics`: VARs with the five schemes, local projections, a Kalman-filter likelihood and a
Bayesian sampler for the Part 30 model, a shift-share toolkit. Reuses statkit `ts` and `ppl`.
*Dials:* the monetary and fiscal rows of Parts 31 and 32, re-derived with every method.
*Reading:* Sims 1980, 1992; Blanchard & Quah 1989; Uhlig 2005; Jordà 2005; Stock & Watson 2012, 2018;
Plagborg-Møller & Wolf 2021; An & Schorfheide 2007; Nakamura & Steinsson 2018; Ramey 2016; Kilian & Lütkepohl;
Hamilton chs 11–13.

### Part 56 · The Core Exam (~55)
*Question:* can you do it with the book closed?
*Story:* the night before the first-year examinations. Twelve problems of the kind every PhD programme sets,
four each in micro, macro and econometrics, solved on screen the way a grader wants to see them, with the
mistakes that cost marks.
0. Hook: the envelope; how to read a problem; objectives.
1. Micro 1: a consumer with a kinked budget: demand, Slutsky, welfare (Parts 5–6).
2. Micro 2: an exchange economy with an externality: equilibrium, the Pareto set, a Pigouvian fix (9, 15).
3. Micro 3: a first-price auction with a reserve: the bid function and revenue (16).
4. Micro 4: a screening contract for two types, then a continuum (10, 13, 14).
5. Macro 1: the Ramsey model with a tax on capital: steady state, the saddle path, the transition (20).
6. Macro 2: a McCall worker with benefits that expire (24).
7. Macro 3: the three-equation model under discretion: the inflation bias and the response to a cost shock
   (30).
8. Macro 4: an Aiyagari household: why the interest rate lies below the rate of time preference (52).
9. Metrics 1: a supply-and-demand system: order and rank conditions, the instrument, the Wald estimator (4).
10. Metrics 2: GMM for an Euler equation: moments, weights, the overidentification test (54).
11. Metrics 3: a difference-in-differences with staggered timing: what two-way fixed effects estimates (4;
    *Statistics, Built* 37).
12. Metrics 4: a VAR with a long-run restriction (55).
13. How the exam is marked; what to do when stuck. 14. Where each problem's idea is still open.

*Agora:* every answer's numbers come from the modules, with the exam's parameter values. *Play it:* each problem
is shown with a pause before its solution; on the site, the twelve problems with stepped hints.
*Reading:* MWG; Kreps; Ljungqvist & Sargent; Romer; Galí; Hayashi; past core examinations published by
departments (cited where a problem is adapted).

## Act XI · Economics at Work

### Part 57 · Reading the Economy in Real Time (~56)
*Question:* what is the economy doing right now, and how good is anyone's guess about next year?
*Story:* Paul Samuelson wrote in 1966 that the stock market had predicted nine of the last five recessions.
Economists do worse in the other direction: of 153 recessions in 63 countries between 1992 and 2014,
forecasters called five by the spring before (An, Jalles and Loungani 2018) (verify).
0. Hook: the two scorecards; the question; objectives.
1. How a number is made: the payroll survey and its birth–death model; GDP's source data; revisions as a
   fan.
2. Seasonal adjustment: what it removes and what it can invent (X-13).
3. Play it: nowcast this quarter's GDP as five releases arrive, one at a time.
4. Nowcasting: bridge equations; the dynamic factor model and the ragged edge (Giannone, Reichlin and
   Small 2008), by the Kalman filter; news as the revision.
5. Leading indicators; the yield curve as a recession predictor (Estrella and Mishkin 1998); the Sahm rule;
   the false alarm of 2022–24.
6. Scoring forecasts: bias, the mean squared error, Diebold and Mariano's test (1995); density forecasts
   and fan charts.
7. The record: the Greenbook against professionals (Romer and Romer 2000); the IMF's; 2008; 2021.
8. Why forecasting recessions is hard: non-linearity, and a forecast that changes the outcome.
9. New data: prices scraped online (Cavallo and Rigobon 2016); card spending in 2020 (Chetty et al. 2024);
   night lights as GDP (Henderson, Storeygard and Weil 2012); job postings.
10. Text as data: policy uncertainty from newspapers (Baker, Bloom and Davis 2016); central-bank minutes;
    language-model embeddings.
11. Judgment against models; combining forecasts; scenario analysis; the Bernanke review of the Bank of
    England's forecasting (2024).
12. Communicating uncertainty to people who want a number.
13. Dials. 14. In practice: this is the job. 15. Frontier: language models as forecasters; real-time
    distributional accounts.

*Agora:* `nowcast`: a mixed-frequency dynamic factor nowcaster on real-time vintages (ALFRED); a forecast
scorer; a recession-probability model. Reuses statkit `ts`.
*Dials:* forecast errors by horizon. *Facts:* the yield curve inverts before recessions.
*Called it?* the whole part is the Called-it card.
*Reading:* Giannone, Reichlin & Small 2008; Stock & Watson 2002, 2016; Diebold & Mariano 1995; Romer & Romer
2000; Estrella & Mishkin 1998; Cavallo & Rigobon 2016; Baker, Bloom & Davis 2016; Gentzkow, Kelly & Taddy
2019; Bernanke 2024; the Philadelphia Fed's Survey of Professional Forecasters.

### Part 58 · Scoring the Bill (~55)
*Question:* how does a government decide whether a project or a law is worth it?
*Story:* the US Flood Control Act of 1936 says a dam may be built if the benefits, "to whomsoever they may
accrue", exceed the costs. The Army Corps of Engineers now has to produce a number for both. Cost–benefit
analysis is what ninety years of producing that number has become.
0. Hook: the sentence in the Act; the question; objectives.
1. The steps of a cost–benefit analysis; standing; the counterfactual.
2. Valuing what has a price: surplus, shadow prices, the marginal cost of public funds.
3. Valuing what has none: time, noise, a view; hedonic prices; travel cost; stated preference and the
   *Exxon Valdez* debate.
4. A statistical life (Part 18): the wage-risk studies, the agencies' numbers, the age question.
5. Play it: the minister's budget: score a tax change before and after behaviour responds.
6. Discounting in practice: the Treasury Green Book, OMB's Circular A-4 and its 2023 revision (verify);
   declining rates.
7. Budget scoring: the baseline, the ten-year window, static against dynamic scores; the record of the
   scores.
8. Microsimulation: a tax-benefit calculator on a household survey (TAXSIM, EUROMOD); the distribution
   table.
9. Computable general equilibrium: a social accounting matrix (Part 3) that responds; what GTAP did and did
   not predict about NAFTA.
10. Evaluation after the fact: programme evaluation offices; the marginal value of public funds as a league
    table (Part 42).
11. Risk: optimism bias in megaprojects (Flyvbjerg); option value; reference-class forecasting.
12. Regulatory impact analysis; the social cost of carbon inside a rule (Part 48).
13. Goodhart's and Campbell's laws: what targets do to numbers.
14. Dials. 15. In practice: budget offices, finance ministries, development banks, consultancies.
16. Frontier: distributional weights in official appraisal; valuing wellbeing directly.

*Agora:* `microsim`: a tax-benefit microsimulation on the Island's household survey with behavioural responses
from the Dials; a small CGE model on the Island's social accounting matrix; a cost–benefit template.
*Dials:* the value of a statistical life and the discount rates used by agencies; scoring errors.
*Called it?* cost and ridership forecasts for large transport projects against outcomes.
*Reading:* Boardman et al.; HM Treasury, *The Green Book*; OMB Circular A-4; Viscusi & Aldy 2003; Hendren &
Sprung-Keyser 2020; Auerbach 2005 on dynamic scoring; Kehoe 2005 on NAFTA models; Flyvbjerg 2014.

### Part 59 · The Expert Witness (~55)
*Question:* how is economics used to decide a merger, and what survives cross-examination?
*Story:* in 1997 the Federal Trade Commission sues to stop Staples from buying Office Depot. The companies say
they compete with every shop that sells a pen. The FTC's economists show, from the firms' own price data, that
Staples charges about 13% more in towns where no other office superstore is present (verify). It is the first
big merger trial decided on econometrics.
0. Hook: the price map; the question; objectives.
1. What the law asks: a substantial lessening of competition; the consumer-welfare standard.
2. Play it: is this one market or two? (three pairs of products, with their data).
3. Market definition: the hypothetical-monopolist test; critical loss; the cellophane fallacy.
4. Shares and concentration: the thresholds in the guidelines (1982, 2010, 2023) and what moved.
5. Unilateral effects: diversion ratios and upward pricing pressure (Farrell and Shapiro 2010), derived.
6. Merger simulation in court (Part 43): what it adds, how it is attacked.
7. Efficiencies and pass-through; entry and repositioning.
8. Vertical mergers: bargaining leverage; *AT&T–Time Warner* (2018) and the Nash-bargaining model on trial.
9. Coordinated effects; cartels: detecting them (screens), estimating overcharges, the but-for price.
10. Regression in the witness box: specification, sensitivity, *Daubert*; what a judge can follow.
11. Labour markets: monopsony in merger review; no-poach agreements (Part 38).
12. Retrospectives: did consummated mergers raise prices? (hospitals, airlines, beer).
13. Regulated prices: the rate case, price caps, access pricing.
14. Dials. 15. In practice: agencies, consultancies, in-house teams. 16. Frontier: platform and data
    mergers; nascent competitors; ecosystems.

*Agora:* `merger`: a review toolkit (the hypothetical-monopolist test, diversion and UPP from estimated demand,
simulation, a bargaining model, an overcharge estimator), run on an Island merger with the truth known.
*Dials:* pass-through of cost savings; price effects in retrospectives.
*Called it?* predicted against realized prices in merger retrospectives (Part 44's row).
*Reading:* Davis & Garcés; the US Merger Guidelines (2010, 2023) and the EU's; Farrell & Shapiro 2010;
Ashenfelter et al. 2006 on *Staples*; Shapiro 2021 on *AT&T*; Kwoka, *Mergers, Merger Control, and Remedies*;
Whinston 2006.

### Part 60 · The Price (~55)
*Question:* how do firms actually set prices, and how much of the theory do they use?
*Story:* in 1985 People Express, a no-frills airline, is the fastest-growing company in American history, and
American Airlines cannot match its fares on every seat. American's answer is software: sell the seats that
would have flown empty at People's price, and protect the rest for late bookers. People Express is gone
within two years. The technique is called revenue management.
0. Hook: Ultimate Super Saver fares; the question; objectives.
1. What firms say they do: cost-plus, and why it survives.
2. Measuring willingness to pay: surveys and their bias, conjoint analysis, auctions, experiments.
3. Price experiments: design, interference between customers, what an elasticity from an A/B test means.
4. Play it: a hundred seats, sixty days, uncertain demand: set the price each week.
5. Revenue management: Littlewood's rule (1972) derived; protection levels; bid prices; overbooking.
6. Dynamic pricing as dynamic programming (Gallego and van Ryzin 1994); what airlines' data show
   (Williams 2022).
7. Versioning and menus (Part 10) in practice: good, better, best; damaged goods.
8. Bundles and subscriptions; the economics of "free".
9. Promotions and reference prices; ninety-nine cents; drip pricing and the law.
10. Why chains charge the same price everywhere (DellaVigna and Gentzkow 2019), and what they give up.
11. Cost pass-through: what happened to prices when costs jumped in 2021–22.
12. Algorithms: personalized prices, fairness constraints, the collusion question (Part 44).
13. B2B: negotiated prices, most-favoured-customer clauses, tenders.
14. Dials. 15. In practice: pricing teams in airlines, retail, software. 16. Frontier: pricing with
    learning (bandits); pricing AI services.

*Agora:* `revenue`: a revenue manager (Littlewood, EMSR, the Gallego–van Ryzin problem), a price-experiment
simulator with interference, a conjoint estimator.
*Dials:* typical price elasticities at the product level; pass-through of costs to retail prices.
*Reading:* Talluri & van Ryzin; Phillips, *Pricing and Revenue Optimization*; Gallego & van Ryzin 1994;
Williams 2022; DellaVigna & Gentzkow 2019; Dubé & Misra 2023; Nagle & Müller, *The Strategy and Tactics of
Pricing*; Cross, *Revenue Management*.

### Part 61 · Economics at the Platforms (~56)
*Question:* what do the economists inside technology companies do?
*Story:* on New Year's Eve 2014, for twenty-six minutes, a software fault switches off surge pricing in New
York while demand is at its peak. Requests pile up, drivers do not come, waits triple and most requests go
unfilled. On a comparable night with surge on, nearly every request is met (Hall, Kendrick and Nosko 2015)
(verify).
0. Hook: the twenty-six minutes; the question; objectives.
1. A platform as a designed market (Parts 17, 44): who it matches, what it prices, what it hides.
2. Play it: set the commission and watch both sides.
3. Surge pricing as market clearing; the consumer surplus under Uber's demand curve (Cohen et al. 2016);
   what drivers do.
4. Search and ranking: position effects; what a sponsored slot is worth; steering.
5. Reputation: why almost every rating is five stars; redesigns that restore information.
6. Ad auctions in practice (Part 16): quality scores, reserves, the move to first price, auto-bidding.
7. Does advertising work? The eBay search experiment (Blake, Nosko and Tadelis 2015); why it is so hard to
   measure (Lewis and Rao 2015).
8. Experiments at scale: A/B tests, peeking, variance reduction (*Statistics, Built* 13, 58).
9. When units interfere: marketplace experiments, switchbacks, two-sided randomization
   (*Statistics, Built* 64); bias on the Island's marketplace, with the truth known.
10. Causal machine learning in production: uplift, heterogeneous effects, long-term outcomes from
    surrogates.
11. The gig economy: flexibility valued (Chen et al. 2019); earnings; classification.
12. Data, attention and privacy: what a user's data is worth; the welfare of free goods (Brynjolfsson,
    Collis and Eggers 2019).
13. Dials. 14. In practice: the roles (Athey and Luca 2019). 15. Frontier: marketplaces with AI agents on
    both sides; recommendation and welfare.

*Agora:* `platform`: a two-sided marketplace with search, ranking, ratings, surge pricing and an ad auction; an
experimentation layer that can randomize by user, by time or by market.
*Dials:* the return on search advertising; the elasticity of rides to the surge multiplier.
*Called it?* the pre-experiment belief in paid-search returns at eBay.
*Reading:* Athey & Luca 2019; Varian 2007, 2014; Cohen et al. 2016; Blake, Nosko & Tadelis 2015; Lewis & Rao
2015; Kohavi, Tang & Xu; Bajari et al. 2023 on marketplace experiments; Tadelis 2016 on reputation; Einav,
Farronato & Levin 2016.

### Part 62 · Inside the Firm (~55)
*Question:* why are some firms so much better run than others, and can it be taught?
*Story:* in 2008 Nicholas Bloom and his colleagues offer free management consulting to a randomly chosen group
of large textile plants near Mumbai. The treated plants adopt basic practices: clean floors, recorded
defects, stock that is counted. Within a year their productivity is 17% higher (verify). The practices had
been free to adopt all along.
0. Hook: the plant floor before and after; the question; objectives.
1. Productivity dispersion: two to one within narrow industries (Syverson 2011); why the laggards survive.
2. Measuring management: the World Management Survey (Bloom and Van Reenen 2007); scores across countries
   and ownership.
3. Play it: four practices and a budget: which pays?
4. The experiment's results, and why the owners had not done it: information, delegation, competition.
5. Personnel economics (Part 14 at work): hiring, pay for performance, promotion, the Peter principle
   tested (Benson, Li and Shue 2019).
6. Executive pay: the size of the firm and the size of the cheque (Gabaix and Landier 2008); luck against
   skill (Bertrand and Mullainathan 2001).
7. Capital structure (Part 23): trade-off and pecking order; what CFOs say they do (Graham and Harvey
   2001).
8. Agency and governance (Jensen and Meckling 1976): boards, activists, family firms.
9. Private equity: what happens to firms and workers (Davis et al. 2014).
10. Decentralization and information technology; firms as hierarchies of knowledge (Garicano 2000).
11. Working from home, randomized (Bloom et al. 2015, 2024).
12. Culture, relational contracts and why practices do not transfer (Gibbons and Henderson 2012).
13. Mergers that destroy value; the diversification discount.
14. Dials. 15. In practice: strategy, corporate finance, people analytics. 16. Frontier: firms that
    organize people and models; management as software.

*Agora:* `org`: a firm with managers (delegation, incentives, a knowledge hierarchy) inside the Island's
industry; a management experiment with adoption costs.
*Dials:* the productivity effect of management practices; the pay–performance sensitivity of CEOs.
*Reading:* Bloom & Van Reenen 2007; Bloom et al. 2013; Syverson 2011; Lazear & Gibbs; Gabaix & Landier 2008;
Jensen & Meckling 1976; Graham & Harvey 2001; Gibbons & Roberts (eds), *The Handbook of Organizational
Economics*; Garicano 2000.

## Act XII · The Frontier

### Part 63 · The Economy as a Network (~58)
*Question:* when does a shock to one firm become a shock to everyone?
*Story:* on 11 March 2011 an earthquake and tsunami strike north-east Japan. Firms far from the coast, with no
damage at all, lose sales because a supplier's supplier is under water, and so do their customers. The loss
travels up and down the chains and takes about half a point off Japan's growth that year (Carvalho, Nirei,
Saito and Tahbaz-Salehi 2021) (verify).
0. Hook: the map of affected firms, by links; the question; objectives.
1. Leontief again (Part 3): the inverse as a sum over paths; upstream and downstream.
2. Hulten's theorem (1978): to first order, a sector's shock matters by its sales share and nothing else.
3. Play it: a production network: which firm's failure costs the most?
4. Why idiosyncratic shocks do not wash out: granular firms (Gabaix 2011) and unequal networks (Acemoglu,
   Carvalho, Ozdaglar and Tahbaz-Salehi 2012); the law of large numbers slowed.
5. Beyond Hulten (Baqaee and Farhi 2019): complementarities make large shocks non-linear. Oil in 1973.
6. Supply chains measured: the earthquake; input specificity (Barrot and Sauvagnat 2016); the pandemic.
7. The O-ring (Kremer 1993): one weak link; why skills sort.
8. Financial networks: clearing vectors (Eisenberg and Noe 2001); robust yet fragile (Acemoglu, Ozdaglar
   and Tahbaz-Salehi 2015; Elliott, Golub and Jackson 2014).
9. Social networks: the strength of weak ties (Granovetter 1973), tested on twenty million people (Rajkumar
   et al. 2022).
10. Diffusion: who to tell first; centrality and microfinance take-up in Indian villages (Banerjee et al.
    2013).
11. Games on networks: the key player (Ballester, Calvó-Armengol and Zenou 2006); peer effects and their
    identification.
12. Network formation (Jackson and Wolinsky 1996): stable against efficient.
13. Dials. 14. In practice: supply-chain risk, systemic-risk monitoring. 15. Frontier: endogenous
    production networks; resilience against efficiency (Part 66).

*Agora:* `network`: a production-network economy (linear and CES), a clearing system, diffusion and games on
graphs; the Island's firms linked by an input–output table.
*Dials:* the aggregate effect of firm-level shocks; the elasticity of substitution between inputs in the
short run.
*Reading:* Leontief 1936; Hulten 1978; Gabaix 2011; Acemoglu et al. 2012, 2015; Baqaee & Farhi 2019; Carvalho
et al. 2021; Eisenberg & Noe 2001; Kremer 1993; Jackson, *Social and Economic Networks*; Carvalho &
Tahbaz-Salehi 2019.

### Part 64 · Machines that Learn (~58)
*Question:* what does machine learning change in how economics is done?
*Story:* every year judges in the United States decide for millions of arrested people whether to hold them
before trial, by guessing who will fail to appear. Kleinberg, Lakkaraju, Leskovec, Ludwig and Mullainathan
(2018) train an algorithm on the same information. Their estimate: crime could fall by a quarter with no more
people jailed, or jailing by 40% with no more crime (verify). The hard part is not the prediction. It is
knowing what would have happened to the people the judges jailed.
0. Hook: the judge's desk; the question; objectives.
1. Prediction policy problems (Kleinberg et al. 2015): rain dances against umbrellas.
2. Play it: ten cases, the same facts the judge saw: detain or release? Then the algorithm's ranking.
3. The selective-labels problem and the judge-leniency design; what the comparison can claim.
4. Prediction is not causation: where a good forecast gives a bad policy.
5. Double machine learning (Chernozhukov et al. 2018): nuisance functions, orthogonal scores, cross-fitting
   (*Statistics, Built* 36, 49).
6. Heterogeneous effects: causal forests (Wager and Athey 2018); policy learning (Athey and Wager 2021).
7. Text and images as data: embeddings as covariates and as outcomes (Gentzkow, Kelly and Taddy 2019);
   satellite poverty maps (Jean et al. 2016).
8. Deep learning as a solution method: the policy function as a network, trained on Euler errors (Maliar,
   Maliar and Winant 2021; Azinovic, Gaegauf and Scheidegger 2022). Part 52 solved again.
9. Learning agents in models: reinforcement learners that set prices (Part 44), taxes (the AI Economist,
   Zheng et al. 2022) and bids.
10. Language models as subjects: *homo silicus* (Horton 2023); what simulated respondents can and cannot
    replace.
11. Language models as research assistants: measurement, coding, hypothesis generation (Ludwig and
    Mullainathan 2024); the validity questions.
12. Fairness (Part 39): impossibility results; discrimination by proxies; what regulators can audit.
13. Dials. 14. In practice: Part 61; credit scoring, public-sector targeting. 15. Frontier: foundation
    models for economic data; automated structural estimation.

*Agora:* `learn`: deep solvers for the Part 22 and Part 52 economies on `explainer.ai.autodiff`; Q-learning and
policy-gradient agents; a double-ML wrapper over statkit; a language-model subject harness (optional, cached).
*Called it?* the algorithm against the judges, and against later deployments.
*Reading:* Kleinberg et al. 2015, 2018; Mullainathan & Spiess 2017; Athey & Imbens 2019; Chernozhukov et al.
2018; Wager & Athey 2018; Gentzkow, Kelly & Taddy 2019; Maliar, Maliar & Winant 2021; Horton 2023; Ludwig &
Mullainathan 2024.

### Part 65 · The Economics of AI (~58)
*Question:* what happens to work, growth and the distribution of income if machines can do most tasks?
*Story:* in 1930, in the first year of the Depression, Keynes writes an essay for his grandchildren. In a
hundred years, he says, the standard of living will be four to eight times higher and the working week
fifteen hours. He was right about the first. The hundred years are up in 2030.
0. Hook: the essay and the two forecasts; the question; objectives.
1. Play it: in a model where ideas are produced by people and machines, set the share of tasks automated
   and watch the growth rate.
2. Technology and work, historically: the Luddites, Engels's pause (Part 19), the tractor, the ATM and the
   teller.
3. The task model (Zeira 1998; Acemoglu and Restrepo 2018): displacement, productivity, new tasks.
4. General-purpose technologies: the dynamo's forty years (David 1990); the productivity J-curve
   (Brynjolfsson, Rock and Syverson 2021); Solow's paradox.
5. What the experiments find: writing (Noy and Zhang 2023), customer support (Brynjolfsson, Li and Raymond
   2025), consulting (Dell'Acqua et al. 2023), coding; who gains most; the studies that find no gain
   (verify, in the frontier sweep).
6. From tasks to aggregates: exposure measures (Eloundou et al. 2024); Acemoglu's small number (2024)
   against the large ones; the arithmetic that separates them.
7. Wages and the labour share when capital can do a task (Part 39's model, extended).
8. Growth with automated research (Aghion, Jones and Jones 2019): Baumol's cost disease against a
   singularity; what bottlenecks do.
9. Nordhaus's tests for an approaching singularity (2021); the evidence since.
10. Market structure: scale, data and compute; open against closed models; who captures the surplus.
11. Policy: taxing robots (Guerreiro, Rebelo and Teles 2022), insurance and transfers, competition,
    education; an *is / ought* card.
12. Agents that transact: markets where both sides are software (Parts 61, 64).
13. Dials. 14. In practice: workforce strategy, AI policy, productivity measurement (Part 3).
15. Frontier: transformative-AI scenarios (Korinek and Suh 2024; Jones 2024); measuring AI's use from
    usage data.

*Agora:* `automation`: a task-based economy with automation and new tasks; a growth model with automatable
research and a bottleneck; adoption with complementary investment.
*Dials:* the productivity effect of generative AI by task; the share of tasks exposed; the elasticity of
substitution between tasks.
*Called it?* Keynes (1930); Frey and Osborne's 47% (2013) against a decade of employment data.
*Reading:* Keynes 1930; Zeira 1998; Acemoglu & Restrepo 2018, 2019; Autor 2015; Brynjolfsson, Rock & Syverson
2021; Aghion, Jones & Jones 2019; Nordhaus 2021; Acemoglu 2024; Agrawal, Gans & Goldfarb (eds), *The Economics
of Artificial Intelligence*; Korinek & Suh 2024.

### Part 66 · Geoeconomics and Industrial Policy (~58)
*Question:* what happens to the gains from trade when trade becomes a weapon?
*Story:* on 2 April 2025 the United States announces a tariff on almost every country, set by a formula: the
bilateral trade deficit divided by imports, halved, with a floor of ten percent. Within days economists are
arguing about one parameter in it, the rate at which tariffs pass into prices, and about whether a bilateral
deficit measures anything (verify the details in the frontier sweep).
0. Hook: the formula on a board; the question; objectives. A card: each side's best case (§1.2).
1. What the last decade's tariffs did: prices, quantities, retaliation, jobs (Part 36; Fajgelbaum et al.
   2020; Flaaen and Pierce 2024).
2. Play it: a tariff arrives. Retaliate or not? (a repeated game against three kinds of partner).
3. Trade wars as games: the optimal tariff, the Nash tariffs, what the WTO rules were for (Part 35; Ossa
   2014).
4. The 2025 tariffs on the quantitative model of Part 36: welfare, revenue, the range across the trade
   elasticity.
5. Bilateral deficits and the current account (Part 34): what a tariff can and cannot change.
6. Weaponized interdependence: chokepoints (Farrell and Newman 2019); sanctions and their evidence; the
   2022 reserve freeze.
7. A framework for geoeconomic power (Clayton, Maggiori and Schreger 2023): threats, hegemons, hedging.
8. Security against efficiency: optimal resilience; friend-shoring measured (Alfaro and Chor 2023).
9. Industrial policy, the old case: infant industries, learning by doing; the old evidence against.
10. The new evidence (Juhász, Lane and Rodrik 2023): South Korea's heavy-industry drive (Lane 2025),
    Napoleon's blockade (Juhász 2018), shipbuilding (Kalouptsidi 2018; Barwick, Kalouptsidi and Zahur 2019).
11. Chips, batteries and solar: subsidy races as games; what the first evaluations find.
12. Reserve currencies and payment systems: can the dollar be replaced (Part 34)?
13. China's model and the debate over it: state capacity, overcapacity, the second China shock.
14. Dials. 15. In practice: trade ministries, corporate supply-chain strategy, sanctions compliance.
16. Frontier: fragmentation scenarios; climate clubs as industrial policy.

*Agora:* `tradewar`: tariff games and counterfactuals on the Part 36 model with real trade shares; a
supply-chain model with a security premium; an infant-industry model with learning.
*Dials:* tariff pass-through (2018–19 and 2025); the long-run trade elasticity; the fiscal cost per job of
recent industrial subsidies.
*Called it?* forecasts of the 2025 tariffs' price effects against outcomes.
*Reading:* Ossa 2014; Fajgelbaum et al. 2020; Farrell & Newman 2019; Clayton, Maggiori & Schreger 2023;
Juhász, Lane & Rodrik 2023; Lane 2025; Juhász 2018; Hirschman 1945; Alfaro & Chor 2023; Irwin, *Clashing over
Commerce*.

### Part 67 · The Next Economics (~55)
*Question:* how much of what economics says is true, and how is the field changing the way it finds out?
*Story:* Abel Brodeur and his colleagues collect every test statistic from three top journals: about 50,000 of
them. Their distribution has a valley just below 1.96 and a hump just above it (2016; 2020) (verify). Results
that were nearly significant have gone somewhere.
0. Hook: the two-humped camel; the question; objectives.
1. Play it: six published results, their designs and p-values: which replicated?
2. Replication in the lab: eleven of eighteen experiments (Camerer et al. 2016); prediction markets that
   knew which.
3. Reproducibility of empirical papers: code and data policies; what the AEA's data editor finds; the
   Reinhart–Rogoff lesson (Part 32).
4. Specification searching by design: instruments and difference-in-differences show more bunching than
   trials and discontinuities (Brodeur, Cook and Heyes 2020).
5. Publication bias corrected (Andrews and Kasy 2019); the minimum wage and the value of life re-read.
6. Remedies: pre-analysis plans and their limits (Olken 2015); registered reports; multiple testing in
   economics (Part 4; *Statistics, Built* 33).
7. The empirical turn: from 50% theory to 20% in three decades (Hamermesh 2013; Angrist et al. 2017);
   administrative data and who can get it.
8. Structure and design, reconciled or not; the Dials audited: which moved most during the series.
9. Many analysts, one dataset (Huntington-Klein et al. 2021); expert forecasts of results (DellaVigna and
   Pope 2018).
10. What mainstream models leave out: complexity and agent-based models (Arthur; Farmer), their best case
    and their identification problem; an agent-based Island beside the equilibrium one.
11. The profession: who becomes an economist; the top-five journals (Heckman and Moktan 2020); advice and
    its accountability.
12. Economics with AI in the loop: automated literature review, data construction, hypothesis search
    (Part 64).
13. Dials. 14. In practice: how to read an economics paper, a forecast and an op-ed. 15. Frontier: a
    cumulative, machine-readable record of estimates: the Dials as a public good.

*Agora:* `field`: a model of a research field (a publication filter, specification search, replication) fitted
to the published z-curves; an agent-based variant of the Island.
*Dials:* the audit. *Called it?* the prediction markets for replications.
*Reading:* Brodeur et al. 2016, 2020; Camerer et al. 2016; Andrews & Kasy 2019; Christensen & Miguel 2018;
Angrist & Pischke 2010; Leamer 1983; Hamermesh 2013; Heckman & Moktan 2020; Arthur 2021; Rodrik, *Economics
Rules*; Akerlof 2020, "Sins of Omission".

### Part 68 · The Dissertation (~55)
*Question:* how is a new piece of economics made?
*Story:* back to Paris. One research question, chosen in Phase 2 so that it needs a natural experiment, a model
and a counterfactual (candidate: what a city's congestion charge did to traffic, prices and who lives where,
with public data), carried from idea to paper. Then the series' accounts are closed: the Dials, the Facts, the
Tableau.
0. Hook: Bastiat's city today, in data; objectives.
1. Finding a question: important, answerable, not answered. The literature in one page.
2. The data: sources, construction, the descriptive facts first.
3. The design: the identifying variation drawn (Part 4); threats listed before estimating.
4. Play it: predict the result before it is shown.
5. The estimates; robustness; what the design cannot say.
6. The model: the smallest one that speaks to the estimates (Parts 37, 54); estimation; fit.
7. The counterfactual: a policy that was not tried; uncertainty carried through.
8. Writing it: the introduction as an argument; the talk; the referee reports, and the reply.
9. The same paper on the Island: what the method would have found if the truth were known.
10. Agora against the Facts: the scorecard, all forty rows, your guesses beside it.
11. The Dials, final: what is settled within a range, what is contested, what was never identified.
12. The Tableau: the pipes that are open and the boxes still sealed (expectations, institutions,
    distribution within the household, the long-run growth rate).
13. Who feeds Paris now; the Queen's question, answered as well as the series can.
14. Frontier: twelve open problems, one from each act. 15. Outro: the last market, and the score's two
    voices on one note.

*Agora:* the thesis, reproducible from one script; `facts.scorecard()`; `dials.final()`.
*Play it:* the last market: the pit of Part 1 again, with everything the viewer now knows.
*Reading:* the part's own source list; Cochrane, "Writing Tips for PhD Students"; Shapiro, "How to Give an
Applied Micro Talk"; Varian, "How to Build an Economic Model in Your Spare Time"; Thomson, *A Guide for the
Young Economist*.

## 5. Threads that cross the parts

- **The Euler equation:** Part 7 (two periods) → 20 (Ramsey) → 22 (consumption) → 23 (asset prices) → 29–30
  (the cycle and the IS curve) → 52 (a hundred thousand of them) → 54 (estimated by GMM).
- **The fixed point:** Part 9 (Walras) → 11 (Nash) → 17 (stable matchings) → 26 (two of them, a run) → 29 and
  51 (the Bellman operator) → 43 (BLP's contraction) → 52 (a distribution that reproduces itself).
- **Screening and the envelope formula:** Part 10 (menus) → 13 (insurance) → 16 (revenue equivalence) → 41
  (Mirrlees) → 53 (information design).
- **Supply and demand identified:** Part 2 (the picture) → 4 (the instrument) → 38 (labour) → 43 (demand for
  differentiated products) → 55 (aggregate demand and supply shocks).
- **Multiple equilibria:** Part 11 (coordination) → 24 (coconuts) → 26 (runs) → 34 (currency attacks) → 37
  (cities) → 53 (global games select one).
- **Who bears it:** incidence in Part 2 → 35 (Stolper–Samuelson) → 36 (tariffs) → 38 (the minimum wage) → 41
  (taxes) → 66.
- **The Lucas critique:** stated in Part 4, shown in 28, and the reason for Parts 54 and 55.
- **Monopolistic competition:** Part 12 → 21 (Romer) → 30 (sticky prices) → 36 (Krugman and Melitz).
- **The Island's history:** the fish market (2), the lemons (13), the bank (26), the recession (27), the
  inflation (28), the crisis (33), the second island (34), the town (37): all in the data set that Parts 54,
  55 and 68 are handed.
- **Across series:** *Statistics, Built* for every estimator's theory; *Quant, Built* for finance beyond Part
  23; *Psychology, Built* 25–26 for the decision models under Part 45; *AI, Built* for the learning methods of
  Part 64; *Computer Science, Built* for the algorithms (matching, linear programming, complexity of
  equilibria); *Philosophy, Built* for the ethics under Parts 18, 40 and 48.

## 6. What the series is not

- Not a business or personal-finance channel. It explains how markets and policies work; it gives no advice.
- Not commentary. Current events appear as dated cases with data frozen on a stated day, not as takes.
- Not a defence of markets or a case against them. Both the welfare theorems and their failures are proved.
- Not a finance course (*Quant, Built*) or a statistics course (*Statistics, Built*), though it uses both.
- Not a history of thought, though every idea is given its people and its date.

## 7. Phases

0. **Infrastructure** (one or two sessions).
   - `explainer/economics/`: ACTS/PARTS, the Tableau map, timeline and scale strips, `chapter_card` with the
     question in the corner, payoff, reference, study, dial, fact, call and is/ought cards; `style.py`;
     `viz.py` (first instruments: `MarketCross`, `Tableau`, `IdentificationPicture`, `DialCard`, `FactCard`,
     `TAccounts`, the game stage); `agora/` with its `solve`/`simulate` interface; `island.py` with the cast;
     `facts.py`, `dials.py`, `calls.py`, `data.py` with `data/SOURCES.md`.
   - `score.py` on Monochord, with the four cues, and one data film; a two-minute test film
     (`videos/economics/soundcheck/`, as *Music, Built*'s) to judge the watching devices before Part 1.
   - `videos/economics/__init__.py`, `ECONOMICS_ZH_GUIDE.md`, `economics_text_zh.json`.
   - Tools: a `Course` entry for `economics` (prefix `econ`) in `tools/series_site.py` with its count in
     `tests/test_series_site.py`; `economics` in `videos/coursekit.SERIES` and `PREFIX`, and in `BILINGUAL`
     in `tools/make.py`; `--series economics` for the QA and packaging tools; `tools/check_dials.py`.
   - The browser game kit (`course/site/widgets/00_games.js`) and a scripted player for
     `tools/check_course.py`.
   - Promote the idea-diagram instruments of `explainer/psychology/viz.py` to a shared module.
   - `READING.md`: the map of textbooks, models and papers to parts, generated and tested as *Music, Built*'s.
   - `tests/economics/`: the Island's planted truths are recoverable; the Dials' schema; a silent smoke
     render.
1. **Pilots: Part 1, then Part 2.** Part 1 fixes the tone, the Island, the Tableau and the watching devices.
   Part 2 exercises what a typical part needs: a game on the viewer, a model built from primitives, a
   computed market, Dial rows, a data film. (The site counts a series' parts from 1 without gaps, so pilots
   are the first two parts.) Delivered with previews and contact sheets, reviewed, and the standard of §1
   locked.
2. **Act by act,** reviewing at each milestone:
   - Acts I–IV (Parts 3–18): the micro course, about 16 hours with the pilots. A complete first season on
     its own.
   - Acts V–VI (Parts 19–33): growth, money and the cycle.
   - Acts VII–IX (Parts 34–50): the world, work and the state, the fields. **The degree**, complete at
     Part 50.
   - Act X (Parts 51–56): the graduate core.
   - Act XI (Parts 57–62): the practice.
   - Act XII (Parts 63–68): the frontier and the finale.

   Each part goes through: the frontier sweep and Dial rows with sources and dates; the Data Room's licence
   checks; locking the chapter list; `compute.py` and its Agora module with tests; English scenes and the QA
   gates, including the §1.3 review on the contact sheet; the course entry, lab and game
   (`videos/coursekit/AUTHORING.md`); the Chinese edition and its gates; commit and push.

## 8. Decisions, and open risks

**Decisions** (the default is listed first in each; none is taken yet):

1. **Sixty-eight parts**, or a first season of 1–50, or of 1–18. The acts after IX are separable: X, XI and
   XII each stand on the degree and not on each other.
2. **30–60 minutes per part, most at 45–55.** Parts 9, 28–33, 36, 52, 54 and 55 are planned at the top of the
   range; if one passes 60 it is split.
3. **Micro first.** Alternative: Act I, then Acts V–VI (growth, money, the cycle), then Acts II–IV. It would
   need Parts 7, 9 and 12 moved up or summarized.
4. **`econ1` … `econ68` in `videos/economics/`.**
5. **Bilingual from the start.**
6. **The watching devices of §1.3**, each separable: cold opens; the Island as a serial with a named cast;
   Play it in the first third; the intermission and data films; *Called it?*; the score and data melodies;
   drawn places. A soundcheck film in Phase 0 lets them be judged before any part is built.
7. **Names:** Agora, the Island, the Tableau, the Facts, the Dials, the Data Room, Play it, Called it?
8. **Scope lines.** Finance beyond Part 23 stays with *Quant, Built*; econometric theory with *Statistics,
   Built*. Health, education and the family share one part (49); each could be its own. Economic history is
   one part (19) and a thread; a history-of-thought part is a possible addition. Marxian and other heterodox
   economics appear inside Parts 2, 9, 27, 33, 40 and 67, not as a part.
9. **The capstone's policy (Part 50) and the dissertation's question (Part 68)** are chosen in Phase 2 from
   the candidates listed, by what public data support.

**Open risks:**

- **Accuracy of the Dials and of dated facts.** A wrong estimate or a misattributed result is the worst
  error this series can make. Everything in this draft is from memory and is **(verify)** until its sweep;
  rows carry dates and are reviewed again before each act is released.
- **Balance.** The topics are politically live. §1.2 is the policy; Parts 32, 38, 40, 41, 44, 47, 48, 65 and
  66 get an additional read against it before release, and Part 66 is written last among its act so that its
  data are as late as possible.
- **Current events age.** Parts 28, 31, 57, 65 and 66 lean on recent episodes. Each freezes its data on a
  stated date and keeps the recent material in its last chapters, so a later revision touches few scenes.
- **Licences.** Replication packages, microdata and some long-run series have terms that forbid
  redistribution. Checked per part; restricted data are cited and summarized, and the Island stands in for
  demonstrations of method.
- **Compute.** Parts 43, 44, 52, 55 and 64 are heavy. Each has a small configuration that runs within the
  default budget and a full one that is cached; tests run the small one.
- **Scope of Agora.** Sixty models can become sixty unrelated scripts. The single `solve`/`simulate`
  interface, the estimation harness of Part 54 running on every module, and the Island's saved history are
  what make it one library; Parts 50 and 68 are where that is tested.
- **The score and the serial could wear thin** over sixty hours. The soundcheck and the two pilots are
  where that is judged; every device in §1.3 can be dialled down per part.

## 9. Progress

| Part | Status | Notes |
|---|---|---|
| Phase 0 | the first slice built | `explainer/economics/`: Agora (`market`, `crusoe`, `signals`, and from Part 2 `curves`), the Island, the Facts, the Dials and their gate, Called it?, the Data Room (Maddison 2023, FRED, the Philadelphia Fed's forecasters, and from Part 2 the Pink Sheet and USDA's coffee data, frozen 2026-11-18), the instruments, the score; the course entry, the lab kit and the game kit (`00_games.js`); `tests/economics/`. `READING.md`, written from the syllabus and the parts (`videos/economics/reading.py`); the Chinese term guide (`ECONOMICS_ZH_GUIDE.md`). Still to come: the soundcheck film, the Chinese text table |
| 1 | built, English | *Who Feeds Paris?* Every date, quotation and number checked against its source (see the part's README); the Chinese edition is to come |
| 2 | built, English | *The Scissors.* Agora gains `curves` (straight lines through elasticity, incidence and controls) and taxes, caps and floors in the double auction; the Data Room gains the World Bank's Pink Sheet and USDA's coffee balance sheets; the first Dial row (staples) and the first Fact's columns are filled |
| 3 | built, English | *The Measure.* Agora gains `accounts` (the Island's input-output table, GDP three ways, Leontief's inverse, value added in exports) and `indices` (Laspeyres, Paasche, Fisher, Törnqvist, the exact Cobb–Douglas index, chaining and drift); the Data Room gains FRED's national accounts, labour-market and price series, the World Bank's WDI, the UNDP's HDI and the Philadelphia Fed's real-time GDP; a new dial (the CPI's bias, from expert reviews); Kaldor's facts and the labour share are shown; the Dials gate checks every Data Room loader |
| 4 | built, English | *The Evidence.* Agora gains `econometrician` (the fish market and its planted curves, OLS, Wald and 2SLS over statkit's `quasi`, the omitted-variable formula, the apprenticeship by choice and by lottery, Lucas's islands, the two-level village trial, difference in differences); the Data Room gains the 1969 draft lottery and Lucas (1976) among the transcribed passages; the Museum's NSW data and Card and Krueger's table are used; a new dial (the return to a year of school, from Card 2001); Act I is complete |
| 5 | built, English | *What People Want.* Agora gains `consumer` (preferences and demand with corners and kinks, WARP, SARP and GARP, Afriat's index and his inequalities as an LP, Varian's bounds, Bronars's power, Becker's random consumers, the EITC's kink, a binary logit); the Data Room gains BEA's fifteen PCE categories and the population, 1929–2025, and the transcribed results of Harbaugh et al., Choi et al., Andreoni and Miller, Chen et al., Saez and McFadden; a new dial (consistency with utility maximization) and the BART *Called it?*; Act II begins |
| 6 | built, English | *Demand.* Agora gains `demand` (Cobb–Douglas, CES, linear expenditure and AIDS systems with their dual functions checked numerically, the Slutsky matrix and decompositions, the subsistence diet and Jensen and Miller's voucher design, welfare with Willig and Hausman, price indices and Feenstra, Hamilton's Engel drift, AIDS estimation with tests, the integrability loop); the transcribed results of Jensen and Miller, Hausman's cereal, Costa and Hamilton, Engel and Houthakker, the USDA's quintiles, Jaravel and the BLS's methods; rows added to the staples and CPI-bias dials, a new dial (food's income elasticity) and Engel's law as *Called it?* |
| 7 | built, English | *Time and Risk.* Agora's `risk` grows to the whole part (expected utility and its measures, dominance, insurance and portfolios, Rabin's calibration, the St Petersburg game, Fisher, discounting and beta–delta, Epstein–Zin, Hall's regression, Holt and Laury with noisy respondents, Ellsberg's maxmin and Chew's weighted utility); the Data Room gains real PCE, the PCE price index and the 3-month bill rate, and the transcribed results of Bernoulli, Samuelson, Allais, Ellsberg, Rabin, Thaler, Holt and Laury, Hayden and Platt, Madrian and Shea, Thaler and Benartzi, Barsky et al., Post et al. and Mehra and Prescott; two new dials (relative risk aversion; the EIS) and Bernoulli's *Called it?* |
| 8 | built, English | *The Firm.* Agora gains `firm` (technologies, costs and their duality identities, supply and Le Chatelier, free entry with identical and different firms, Cobb and Douglas's regressions, hold-up, Grossman–Hart–Moore, make-or-buy, Alchian's selection); the Data Room gains the transcribed Cobb–Douglas indices of 1899–1922 (via Felipe and Adams 2005) and the Penn World Table's labour share; two new dials (capital's output elasticity; the capital–labour elasticity of substitution); Act II is complete |
| 9 | built, English | *The Invisible Hand, Proved.* Agora gains `ge` (the box and the replicated core, Sperner and Scarf, tatonnement and Scarf's cycle, Newton, Crusoe, three equilibria, Arrow securities, Kantorovich's duals, misallocation, top trading cycles); the Data Room gains Brent and WTI crude via FRED and the transcribed Radford (1945), Edgeworth (1881), Hsieh and Klenow (2009), Bils, Klenow and Ruane (2021) and Kehoe (2014); a new dial (misallocation), the law of one price as a Fact, and the NAFTA *Called it?*; Act III begins |
| 10 | built, English | *The Price Maker.* Agora gains `pricing` (the monopoly price and pass-through, the ferry, three degrees of discrimination, two-part tariffs, bundling, the Coase equilibrium, Ramsey prices, the Averch–Johnson firm, monopsony, Littlewood's rule, personalized prices from a price experiment); the Data Room gains the BLS price of ground coffee via FRED and the transcribed De Loecker, Eeckhout and Unger (2020), Traina (2018), Nakamura and Zerom (2010) and Dubé and Misra (2023); a new dial (markups), incomplete pass-through as a Fact; no *Called it?* |
| 11 | built, English | *Games.* Agora gains `games` (equilibria by support enumeration, iterated elimination, the cognitive hierarchy and its fit, game trees, Rubinstein, the folk region, a strategy library with a noisy round robin and the ecology, correlated equilibrium by LP, the replicator, fictitious play, regret matching, Bayesian equilibria); the Data Room gains the FAS nuclear stockpiles via Our World in Data and the transcribed Nagel (1995), Thaler's FT contest (1997), Flood (1952, via Poundstone), Henrich et al. (2001), Camerer, Ho and Chong (2004) and Axelrod (1980); a new dial (depth of reasoning) and the guessing game's *Called it?* |
| 12 | built, English | *Competition among the Few.* Agora gains `oligopoly` (Cournot, Bertrand homogeneous and differentiated, Kreps–Scheinkman, Hotelling and Salop, Dixit–Stiglitz, Stackelberg, Dixit's credible capacity, collusion thresholds, Green–Porter, leniency, the HHI and mergers, the MHHI); the Data Room gains the BLS gasoline price via FRED and the transcribed Connor (1998, 2014), Boyer and Kotchoni (2015) and the merger guidelines; a new dial (cartel overcharges) and Stigler's *Called it?*; Act III is complete |
| 13 | built, English | *Lemons and Signals.* Agora gains `info` (lemons and blind offers, guarantees, Spence, Rothschild–Stiglitz and its existence, the Einav–Finkelstein diagram, a death spiral, the positive-correlation test, credit rationing, reputation); the Data Room gains the BLS CPIs for used cars and new vehicles via FRED and the transcribed Akerlof (1970), Einav, Finkelstein and Cullen (2010, Table 4), Cutler and Zeckhauser (1998), Tyler, Murnane and Willett (2000) and the selection papers; a new dial (the welfare cost of adverse selection) and the referees' *Called it?*; Act IV begins |
| 14 | built, English | *Incentives.* Agora gains `contracts` (teams, the linear and two-outcome agency problems, relative performance, multitask, tournaments, the ratchet, career concerns, Shapiro–Stiglitz, sharecropping, relational contracts); the Data Room gains the Maddison series for China and India and the transcribed Lazear (2000), Shearer (2004), Bandiera, Barankay and Rasul (2005), Raff and Summers (1987), Lin (1992), Jacob and Levitt (2003), Banerjee, Gertler and Ghatak (2002) and Frey and Oberholzer-Gee (1997); a new dial (output's response to piece rates) and the multitasking *Called it?* |
| 15 | built, English | *Spillovers.* Agora gains `public` (the externality market and Pigou's tax, Coase's bargain with transaction costs, public goods, typed players in the shared pot with punishment, Gordon's fishery, Weitzman's comparison, Vickrey's bottleneck, Arthur's lock-in); the Data Room gains CEDS sulphur dioxide via Our World in Data and the transcribed Coase (1960), Cheung (1973), Schmalensee and Stavins (2013), Duranton and Turner (2011) and Currie and Walker (2011); a new dial (traffic's response to roads) and the acid-rain *Called it?* |
| 16 | built, English | *Auctions.* Agora gains `auctions` (first-price bids with reserves and risk aversion, five formats on the same draws, Myerson's reserve, the winner's curse, Vickrey's prices for slots and the generalized second price, the exposure problem, demand reduction against Vickrey's rule); the Data Room gains the transcribed Binmore and Klemperer (2002), Klemperer (2002), Bazerman and Samuelson (1983), Cramton and Schwartz (2000), Ostrovsky and Schwarz (2009), Garbade and Ingber (2005) and the FCC's incentive auction; the intermission plays FRED's 3-month bill rate; a new dial (what a reserve adds), the Dutch 3G *Called it?*, and the winner's curse in the Facts |
| 17 | built, English | *Markets by Design.* Agora gains `matching` (deferred acceptance either side asking, the Boston rule, blocking pairs and every stable matching, manipulation checks, top trading cycles, kidney cycles and chains, Clarke's pivot rule, the bilateral-trade bound, the assignment game's core, a lottery-based school study); the Data Room gains the crude marriage rate via Our World in Data and the transcribed Roth (2012) and exam-school and Denver charter estimates; a new dial (what a sought-after school adds) and Roth's stability *Called it?* |
| 18 | built, English | *Social Choice and Welfare.* Agora gains `choice` (plurality, runoff, instant runoff, Borda, Condorcet and Copeland; agendas; Borda's failure of independence; Geanakoplos's pivotal voter; single peaks; bloc manipulation; Atkinson's family; the two veils; Scitovsky's reversal; Sen's liberal paradox); the Data Room gains V-Dem's electoral democracy index via Our World in Data and the transcribed values of a statistical life (DOT, EPA, Ashenfelter and Greenstone) and Duverger's law; a new dial (the value of a statistical life) and Duverger's *Called it?* |
| 19 | built, English | *The Great Escape.* Agora gains `malthus` (a Malthusian economy with a plague and an invention, England's labour demand curve, Galor and Weil's household and a toy unified growth economy, spatial noise); the Data Room gains the Bank of England's millennium series for England and Our World in Data's long-run population, life expectancy, fertility and heights, and Malthus's 1798 passage from the first edition; a new dial (English living standards before 1700, three reconstructions, with a new 'reconstruction' design) and Ehrlich's *Called it?* |
| 20 | built, English | *Growth I: Capital.* Agora gains `growth` (the Solow model, its golden rule and speed of convergence, Harrod-Domar, growth and development accounting, convergence regressions, Lucas's ratio, the Ramsey model by shooting); the Data Room gains the Penn World Table 11.0, with the internal rate of return; a new dial (the speed of convergence) and a row on capital's share; Samuelson's Soviet forecast as *Called it?*; Kaldor's facts and conditional convergence get their Agora columns |
| 21 | built, English | *Growth II: Ideas and Institutions.* Agora gains `ideas` (replication, AK, Romer's balanced path, Aghion and Howitt's market and planner research, semi-endogenous growth, directed technical change); the Data Room gains Acemoglu, Johnson and Robinson's 64 colonies (via hdm) and transcribes Nordhaus's price of light and Bloom et al.'s research numbers; a new dial (the social return to R&D); Romer's scale effect as *Called it?*; the price of light gets its Agora column |
| 22 | built, English | *Consumption and Saving.* Agora gains `household` (Keynes's function, the permanent-income annuity, the life cycle, Carroll's buffer stock by the endogenous grid method, simulated populations and their MPC, the wealthy hand-to-mouth, Friedman's cross-section, Campbell and Mankiw's rule of thumb) and `olg` (Samuelson's money, Diamond's economy, a pension's welfare); the Data Room gains FRED's monthly consumption by type with its price indexes, real disposable income and the saving rate, the Penn World Table's consumption shares, and transcribes the windfall studies; a new dial (the propensity to spend a windfall); Hall's random walk as *Called it?*; consumption smoother than income gets its Agora column |
| 23 | built, English | *Capital and Asset Prices.* Agora gains `assets` (Gordon, the user cost, Hayashi's firm, the option to wait, Mehra and Prescott's economy and region, the Hansen-Jagannathan bound, rare disasters, habits, a laboratory market); the Data Room gains Shiller's annual series and the Case-Shiller index against the CPI's rent; a new dial (investment's response to the user cost) and three rows on risk aversion; Fisher's 1929 plateau as *Called it?*; the equity premium and unpredictable returns get their Agora columns |
| 24 | built, English | *Looking for Work.* Agora gains `search` (McCall's searcher, the DMP model with its curves, Beveridge curves and path, Hosios's condition, the elasticity of tightness, Shimer's flows and the ins-and-outs shares, Burdett and Mortensen's job ladder); the Data Room gains FRED's JOLTS (openings, hires, separations, quits), unemployment by duration, the labour force, output per hour and the CBO's natural rate; two new dials (the matching elasticity; the worker's bargaining share); Mortensen and Pissarides's 1994 claim as *Called it?* (partly right); the Beveridge curve gets its Agora column |
| 25 | built, English | *Money.* Agora gains `money` (Kiyotaki and Wright's economy with its equilibrium check, barter's odds, Cagan's Laffer curve and a printed deficit, Baumol and Tobin, cash in advance, T-accounts); the Data Room gains the World Bank's money growth and inflation by country since 1960 and FRED's M1, M2, base money, currency, reserves, velocity and nominal GDP, and transcribes Hanke and Krus's hyperinflation peaks; a new dial (the interest semi-elasticity of money demand); Cagan's revenue ceiling as *Called it?* (wrong); the quantity theory gets its Agora column |
| 26 | built, English | *Banks and Runs.* Agora gains `bank` (Diamond and Dybvig's contract and run threshold, sequential service, suspension, Bagehot's lender against a fire sale, Merton's deposit-insurance put, bond losses, capital ratios with risk weights, deposit betas, the repo squeeze, Morris and Shin's global game, Diamond's delegated monitor); the Island gets a bank; the Data Room gains FRED's bank suspensions (1921-41, and monthly to 1933), small and large banks' weekly deposits, the FDIC's national deposit rates, the federal funds rate, Treasury yields, banks' equity ratio, money funds' assets and real GDP, and transcribes Silicon Valley Bank's numbers and the 2022 stress scenario; two new dials (the deposit beta; the output cost of a banking crisis); the 2022 stress scenario as *Called it?* (wrong) |
| 27 | built, English | *The Keynesian Revolution.* Agora gains `keynes` (the babysitting co-op and its curve, the cross and Kahn's multiplier, the paradox of thrift, IS-LM with a zero lower bound, AS-AD, Phillips's machine, frozen wage cuts, cycle spells); the Island has a recession; the Data Room gains FRED's real GNP from 1929, the NBER's recession months since 1854, America's gold stock 1914-1946, the CBO's potential GDP and Japan's call rate; a new dial (Okun's coefficient) and the propensity-to-spend dial shown again; Okun's law gets its Agora column; Keynes's *Economic Consequences of the Peace* as *Called it?* (partly right) |
| 28 | built, English | *Inflation and Expectations.* Agora gains `expectations` (Phillips's curve, acceleration, adaptive forecasts, Lucas's islands, the critique, Barro-Gordon with Rogoff's banker, the sacrifice ratio); the Island has an inflation; the Data Room gains FRED's core CPI, Michigan's expected inflation and the 5-year breakeven rate; two new dials (the slope of the Phillips curve; the sacrifice ratio); the persistence Fact shown; Friedman's 1967 forecast (right) and the Fed's June 2021 projection (wrong) as *Called it?* |
| 29 | built, English | *The Cycle as Equilibrium.* Agora gains `dp` (the cake by value function iteration and its contraction, Tauchen and Rouwenhorst, the HP and Hamilton filters) and `rbc` (Brock and Mirman, the growth model on a grid, Hansen's RBC solved by QZ with the Blanchard-Kahn count, impulse responses, moments, Gali's long-run VAR); the Island gets a cycle; the Data Room gains FRED's real investment, hours and BEA's residential and business investment indexes; a new dial (the Frisch elasticity); the volatility and hours Facts get Agora's column; Prescott's 75 percent (partly right) as *Called it?*. Corrections: FRED's chained-dollar series for residential and nonresidential investment begin in 2007, so the quantity indexes are used; the HP filter's end-point revision flips the sign of 2008's third quarter; with this film's data to 2019, Gali's VAR in levels still has hours rising, so the call is partly right rather than wrong |
| 30 | built, English | *Sticky Prices.* Agora gains `nk` (menu costs, Calvo's slope, determinacy, the three equations by undetermined coefficients and QZ, discretion and commitment, the zero bound and forward guidance, simulated price setters); the Island gets sticky prices; the Data Room gains the GDP deflator, core PCE prices and the Atlanta Fed's sticky- and flexible-price CPIs; the frequency-of-price-changes dial is entered; the sticky-prices and hump Facts get Agora's column; Bernanke's 2002 promise on deflation (right) as *Called it?*. Corrections: Bils and Klenow's 4.3 months is the median across categories in 1995-97, and Nakamura and Steinsson's 8-11 months excludes sales; Cecchetti's and Blinder's findings are stated qualitatively, not with the draft's numbers; the Play it became one question about the median price, since item-by-item durations could not all be checked; Part 31's story is Draghi's 2012 sentence, so the trailer uses it |
| 31 | built, English | *The Central Bank.* Agora gains `cb` (the market for reserves, a corridor and a floor, QE in T-accounts, the Island's monetary history with the bank's private news, four identification methods scored on 300 histories, the natural rate by the Kalman filter, self-fulfilling sovereign yields and a backstop); the Island gets its monetary history; the Data Room gains the Philadelphia Fed's first-quarter real-time GDP vintages, its Greenbook (Tealbook) inflation projections and the SPF's medians, the New York Fed's Holston-Laubach-Williams estimates, and FRED's balance-sheet, reserve, policy-rate, Treasury, European and British yield series; the dials for a tightening's effect, asset purchases and the neutral rate are entered; Romer and Romer's 2000 claim about the Greenbook (partly right) as *Called it?*. Corrections: Orphanides's 1970s finding is that real-time estimates of potential were overoptimistic, and with real-time data the Fed responded strongly to inflation forecasts before 1979 as after; this film's own crude real-time gap explains about a point of the 1970s shortfall; Draghi's sentence is not called unscripted; the QE1 days and figures are Gagnon, Raskin, Remache and Sack's eight baseline announcements (91 basis points); Japan's negative rate began in January 2016 without the draft's figure; the communication dates are the Fed's own; Part 32's story is Herndon's replication |
| 32 | built, English | *The Treasury.* Agora gains `fiscal` (debt dynamics and the stabilizing surplus, the spending multiplier in the Part 30 model with and without the zero bound, Ramey and Zubairy's local projections by state, the regional multiplier and its missing intercept, Barro's tax smoothing, the fiscal theory's price level, Sargent and Wallace's unpleasant arithmetic, Arellano's default model by value function iteration); the Island gets a treasury and a currency union of 48 regions; the Data Room gains Reinhart and Rogoff's panel as processed by Herndon, Ash and Pollin, Ramey and Zubairy's quarterly data since 1889, Ramey's tax files with Romer and Romer's narrative changes, Blanchard and Leigh's forecast errors, and FRED's deficit, debt, interest and Greek and German yield series; the spending-multiplier dial is filled and the tax-multiplier dial entered; the IMF's 2010 growth forecasts for the consolidations (wrong: Blanchard and Leigh's slope of -1.1) as *Called it?*. Corrections: the spreadsheet averaged rows 30 to 44 instead of 30 to 49, and with the excluded years and the weighting the corrected mean above 90% is 2.2%, not -0.1%; Guajardo, Leigh and Pescatori's estimates are stated qualitatively; Greece's 2012 exchange is the ESM's 53.5% nominal haircut; America's war debts fell mostly through growth and inflation, not repayment; modern monetary theory is described from its proponents' own summaries; climate investment is left to Part 48 and bill scoring to Part 58; Part 33's story is the Queen's question at the LSE |
| 33 | built, English | *Crises.* Agora gains `credit` (Minsky's borrowers through a boom, debt deflation, the costly-state-verification contract and the accelerator, Kiyotaki and Moore's collateral cycle solved exactly, Geanakoplos's leverage cycle, county balance sheets, the crisis predictor in and out of sample, recession paths, Basel's credit-gap guide); the Island has a boom, lenders, farmers and gatherers, and 400 counties; the Data Room gains the Jorda-Schularick-Taylor Macrohistory Database (release 6) and FRED's mortgage delinquencies, TED and Baa spreads, swap lines, household debt and the baht, won and peso; the crisis-cost dial gains two rows and the credit-warning dial is entered; the credit-booms Fact gets Agora's column; Rajan's 2005 Jackson Hole paper (right) as *Called it?*. Corrections: the Queen's words are given as reported, since accounts differ, and the British Academy's sentence was checked against the letter of 22 July 2009; Fisher's 'the more the debtors pay, the more they owe' against the 1933 paper; Gorton and Metrick's haircut figures are stated qualitatively; Schularick and Taylor's predictor is refitted here and scored out of sample (0.56 since 1950), with the better of two measures flagged as chosen after looking; the Kiyotaki-Moore calibration is the Island's (R = 1.1, eta = 2), since with R near 1 a 1% shock has no equilibrium; Part 34's story is Black Wednesday |
| 34 | built, English | *The Open Economy.* Agora gains `openecon` (real exchange rates and the pooled PPP half-life, Balassa-Samuelson, Fama's regression with Newey-West errors, the carry trade, Meese and Rogoff's horse race, Mundell-Fleming, Dornbusch, Krugman's attack, Obstfeld's regions, distributed-lag pass-through); the Island is pegged to the Archipelago, with its governor's dilemma, Dornbusch's calibration and a first-generation attack; the Data Room gains The Economist's Big Mac index, the World Bank's current accounts and FRED's exchange rates, interbank rates, import prices, dollar indexes, the US current account and investment position, Britain's reserves and the VIX; the pass-through dial gets its first rows and the PPP half-life dial is entered; the random-walk Fact gets Agora's column; Meese and Rogoff (right) as *Called it?*. Corrections: the plan's Agora module `open` is `openecon`; the planned New Keynesian small open economy is not built here (the Mundell-Fleming algebra and Dornbusch carry chapters 6 and 7); Meese and Rogoff are rerun with end-of-month rates, since monthly averages make changes falsely predictable; pass-through is measured on import prices excluding fuel, since oil's dollar price moves against the dollar and turns the all-imports estimate negative; the 2008 carry crash is narrated by the currencies this sample's strategy actually borrowed and held (the yen against the Australian and New Zealand dollars); Part 35's story is Ricardo's four numbers with Samuelson's answer to Ulam |
| 35 | built, English | *Trade I: Comparative Advantage.* Agora gains `trade` (Ricardo with two goods and the wage band, the chain and the DFS continuum with growth and shipping costs, the 2x2x2 Heckscher-Ohlin world with the Lerner diagram, Stolper-Samuelson and Rybczynski, specific factors, small- and large-country tariffs, quotas and the optimal tariff, protection for sale, a tariff war, Bernhofen and Brown's inner product, Leontief's ratio, Trefler's factor-content statistics, the ACR formula, Grubel-Lloyd); the two islands trade (fish and cloth, labour and capital, food and manufactures); the Data Room gains the JST database's imports and exports, FRED's customs duties, imports of goods and end-use trade, and Trefler's 1983 data, with Ricardo's, Bernhofen and Brown's, Leontief's, Irwin's, Goldberg and Maggi's and other tables transcribed; the gains-from-trade dial is entered; the two-way-trade Fact gets its data column; Heckscher and Ohlin's prediction for America (partly right) as *Called it?*. Corrections: Samuelson's answer to Ulam is quoted as several sources reproduce it, with the 1969 lecture not read; Japan opened its treaty ports in July 1859, six years after Perry's arrival (1853), with tariffs capped at low rates; Irwin's published estimate of the embargo's cost is 5% of GNP (the working paper's was 8%); Goldberg and Maggi's welfare weight of 50-88 is the working paper's; the Smoot-Hawley figures are on dutiable imports, and much of their rise was deflation; the Ideal X's loading cost is $5.83 a ton in the sources found, not $5.86; Part 36's story is the Ideal X |
| 36 | built, English | *Trade II: Scale, Firms and Gravity.* Agora's `trade` gains part II (Krugman's variety and home-market effect, gravity by OLS and PPML with two-way fixed effects, Melitz's cutoffs and simulated firms, Eaton and Kortum by formula and simulation, exact hat algebra with fixed deficits, a shift-share China shock); the Island's firms, three islands for Eaton-Kortum and 400 local labour markets; the Data Room gains CEPII's Gravity database for 2019 and FRED's imports from and exports to China and manufacturing employment, with Autor, Dorn and Hanson's, Fajgelbaum et al.'s, Boehm et al.'s, Xing and Detert's and other tables; the trade-elasticity and import-competition dials are entered and the pass-through dial gains two rows; the gravity, two-way-trade and few-exporters Facts get Agora's column; Krugman's 1995 estimate of trade and wages (partly right) as *Called it?*. Corrections: the Ideal X's loading cost is McLean's $5.83 a ton in the sources found; the Play-it guesses Spain's partners rather than two countries' sizes; the planned PPML 'keeps the zeros' does not apply to BACI's recorded flows; Autor, Dorn and Hanson's numbers are from NBER WP 18054; the counterfactual's domestic spending is GDP less goods exports, a stated proxy; Part 37's story is Schelling's checkerboard, dated by his 1971 paper |
| 37 | built, English | *Cities and Regions.* Agora's `city` (Schelling's checkerboard and tolerance curve, von Thünen's rings, the closed monocentric city with the car and the lift, agglomeration with sorting and movers, the rank − ½ Zipf fit and Gibrat's growth with a floor, Krugman's core and periphery with break and sustain points, a Rosen-Roback system of towns, a line city after Ahlfeldt et al. divided by a wall); the Island's six towns, crops and line city; the Data Room gains the Census Bureau's Vintage 2024 metropolitan populations, HYDE's urban shares since 1500 via Our World in Data, and FRED's twenty Case-Shiller metro indices and Barrero, Bloom and Davis's work-from-home rate, with tables from Saiz, Combes et al., Ahlfeldt et al., Ciccone and Hall, Diamond et al., Chetty et al., Hsieh and Moretti with Greaney's comment, Donaldson, Baum-Snow, Kline and Moretti, Shenzhen's census and Schelling's history; the agglomeration and housing-supply dials are entered; the Zipf Fact gets Agora's column; Cairncross's Death of Distance (partly right) as *Called it?*. Corrections: the plan's plane journey for Schelling was not found (the model is dated by a 1969 RAND memorandum, and Sakoda's 1949 precursor is credited); Shenzhen's 1979 population is about 314,000, not a 'fishing village of 30,000'; Hsieh and Moretti's 36% is shown with Greaney's 2026 comment, which finds an effect two orders of magnitude smaller; Ciccone and Hall's 5-6% rests on secondary summaries |
| 38 | built, English | *Work and Wages.* Agora's `labour` (labour supply with income effects and the three elasticities with Slutsky's equation, participation, a competitive wage floor, monopsony with a minimum wage, Card and Krueger's border design run on the Island under competition and monopsony, least squares and two-stage least squares, Roy's model and Heckman's two steps); the Island's worker, market, employer, restaurants and fishers; the Data Room gains Card and Krueger's 410 restaurants, three of Wooldridge's labour datasets from CRAN (Card's 1995 young men, the 1976 CPS, the 1980 NLS with IQ) and FRED's federal minimum wage, with tables from Card and Krueger, Neumark and Wascher, Cengiz et al., Jardim et al., the cab-driver studies, Chetty et al., Sokolova and Sorensen, Angrist and Krueger, Oreopoulos, the Mariel studies and Kearl et al.; Card and Krueger's +2.75 and Card's 0.132 are recomputed from the data; the minimum wage dial is new (contested), the schooling dial gains three rows and the labour supply dial is filled; Mincer's equation becomes a Fact with Agora's column; the 1979 survey of economists (partly right) as *Called it?*. Corrections: the FTC's 2024 non-compete rule is described as set aside by a court, never in effect; Bertrand and Mullainathan's call-back gap (50%) is from the AER abstract |
| 39 | built, English | *The Wage Structure.* Agora's `labour` gains part II (the canonical model with Katz and Murphy's regression and the demand index, a three-skill task model with automation, robot exposure across commuting zones, a worker-firm economy with AKM and its limited-mobility bias, Rosen's superstars, the hedonic wage locus, Becker's marginal employer, Phelps's statistical discrimination, Oaxaca-Blinder, the within estimator, the child-penalty event study); the Data Room gains Bertrand and Mullainathan's résumés (openintro), Autor and Dorn's polarization files with its own reader for old Stata files, Wooldridge's union panel and the 1978/1985 CPS, and the BLS's earnings by education and sex, deciles, employment by education, the labour share and prime-age employment via FRED, with tables from Katz and Murphy, Card and Lemieux, Ciccone and Peri, Autor, Goldin and Katz, Autor, Levy and Murnane, Acemoglu and Restrepo, Card, Heining and Kline, Autor et al., the BLS, Mas and Pallais, Goldin and Rouse, Quillian et al., Goldin, Kleven et al., Cullen and Pakzad-Hurson and Leontief; the call-back gap (9.65% against 6.45%) and the union premium within men (0.080) are recomputed; three new dials (skill substitution, the firm share, the call-back gap); the child penalty becomes a Fact with Agora's column; Leontief's horses (1983) as *Called it?* (too early to say). Corrections: the game uses Autor and Dorn's twelve occupation groups for 1980-2005, not twelve jobs for 1980-2010; Katz and Murphy's regression on recent national data is shown failing (trend and supply correlate 0.997); Goldin and Rouse's often-quoted 50% is not stated, since their abstract stresses imprecision; the next part's teaser uses the plan's own hook, Pen's parade |
| 40 | built, English | *Inequality and Mobility.* Agora's `distribution` (inequality measures with bootstrap errors, Atkinson's equally distributed equivalent, Pareto exponents from top shares and Hill's estimator, random growth with turnover and a floor, its Kolmogorov forward equation solved as a continuous-time Markov chain with one or two types, the speed of transitions, wealth's tail against r - g, Kuznets's dual economy, generations with transitory income, the Gatsby mechanism, the between-country Gini, a distributional table); the Data Room gains Piketty and Saez's top shares (1913-2022), Opportunity Insights' mobility tables (by parent percentile with the quintile shares summed from the transition matrix, absolute mobility by cohort, 741 commuting zones), the WID's top 1% shares via Our World in Data, and FRED's Distributional Financial Accounts and Census Gini, with tables from Pen, Atkinson, Auten and Splinter, Pareto and Gabaix, Gabaix, Lasry, Lions and Moll, Piketty and his critics, Kuznets, Solon, Mazumder, Corak, Chetty et al. (2014, 2016, 2017, 2018), Lakner and Milanovic, Klass et al. and the frontier; the rank-rank slope (0.341), the transition matrix (7.5%) and absolute mobility (92% to 50%) are recomputed; two new dials (the intergenerational elasticity, contested; the Pareto exponent of top wealth); Pareto tails and the Gatsby curve become Facts with Agora's columns; Kuznets's inverted U as *Called it?* (partly right). Corrections: the Play it is four guesses rather than placing the viewer in a world parade (no verified world percentile data in the Data Room); the elephant curve is described, not drawn; Corak's 22-country values are stated as his range, not plotted, and the Gatsby curve is shown across American commuting zones instead; the mechanism of chapter 5 is shown with type dependence |
| 41 | built, English | *Taxes.* Agora's `tax` (Laffer's curve and the marginal cost of public funds along it, Harberger's incidence of a capital tax in closed form from a fixed stock to a small open economy, the deadweight triangle against Harberger's approximation, Ramsey's inverse-elasticity taxes against a uniform rate, Diamond's optimal schedule with the Pareto tail integrated exactly beyond the grid, Saez's top rate and the top bracket's revenue curve, bunching with Saez's estimator and frictions, Allingham and Sandmo's evader); the Data Room gains the IRS's top statutory rates and federal receipts and deficits via FRED, with tables from Laffer and Wanniski, Harberger and Fuest, Peichl and Siegloch, Ramsey, Mirrlees, Diamond and Saez, Feldstein, Gruber and Saez, Saez, Slemrod and Giertz, Chetty, Looney and Kroft, Zucman, Tørsløv, Wier and Zucman, the OECD, Allingham and Sandmo, Kleven et al., Kleven, Landais and Saez and the CBO; America's 2022 Pareto parameter (1.56) is recomputed from the top shares and the 1986 elasticity (1.0) from the rates and shares; three new dials (the elasticity of taxable income, the revenue-maximizing top rate, the corporate tax's incidence on wages); the claim that the 2017 tax cuts would pay for themselves as *Called it?* (wrong). Corrections: the napkin's story is told with its disputes; the revenue curves use a tail that keeps its shape, so their peaks are Saez's formula exactly; the schedule's limit uses incomes' Pareto parameter, alpha/(1 + e), not skills'; a section on the marginal cost of public funds was added to keep the film above thirty minutes |
| 42 | built, English | *Social Insurance.* Agora's `insurance` (pooling with independent and common risks, Baily and Chetty's formula on a static search model with a balanced budget, checked exactly at the welfare optimum, Chetty's split into liquidity and moral hazard, a weekly search model with benefits that run out, health insurance's coinsurance trade-off calibrated to RAND's ratio, Oregon-style lotteries with their power, the examiner instrument, defaults under inertia, the EITC's schedule and an extensive-margin MVPF, tagging, a basic income financed by a flat tax with responses, pay-as-you-go arithmetic and the implicit debt, the MVPF); the Data Room gains continued and initial claims, the insured unemployment rate, benefits paid and the median duration of unemployment via FRED, with tables from Oregon, RAND, Arrow, Baily and Chetty, Meyer, Card, Chetty and Weber, Schmieder, von Wachter and Bender, Gruber, Ganong and Noel, Chetty et al. (Denmark), Maestas, Mullen and Strand, the IRS and Eissa and Liebman, Robins, the basic income trials, Hendren and Sprung-Keyser, Finkelstein, Hendren and Luttmer, the trustees and the CRS; UI's reach (35% of the unemployed since 1967) is recomputed; the duration elasticity dial is filled and two new dials open (the price elasticity of medical spending, the MVPF); the 1983 reform's 75 years as *Called it?* (wrong). Corrections: Madrian and Shea's 48 points are stated as 37% to 86% from the working paper read for Part 7; the 1.4-point Eissa-Liebman figure is the working paper's; Robins's figures are stated as approximate; the Called it? is the 1983 projection, since no verifiable quotation of the emergency-room claim was found; the next part's teaser uses Berry, Levinsohn and Pakes (1995) rather than the cereal margins, which were not checked |
| 43 | built, English | *Measuring Market Power.* Agora's `io` (Cournot with unequal costs and the structure-performance correlation with no collusion, Bresnahan's conduct identification, logit, nested and random-coefficient shares with exact Jacobians, multi-product Bertrand by Morrow and Skerlos's iteration, costs from prices, merger simulation and Werden's compensating cost reductions, Nevo's implied margins by ownership, a simulated car market with known demand, BLP and Gandhi-Houde instruments, plain logit by OLS and IV, Berry's contraction and the BLP estimator with a 40-Island Monte Carlo, logit and nested-logit surplus and the value of a clone, plants with unseen productivity and Ackerberg, Caves and Frazer's estimator, De Loecker and Warzynski's ratio, Bresnahan and Reiss's thresholds by an ordered probit); the Data Room gains Berry, Levinsohn and Pakes's 2,217 cars (BLPestimatoR, read without evaluation) and corporate profits after tax via FRED, with tables from the FTC's cereal case, Nevo, Bain and Demsetz, Bresnahan and Lau, Lancaster, McFadden and Berry, BLP, Petrin, Olley and Pakes, Levinsohn and Petrin, ACF, Syverson, De Loecker and Warzynski, De Loecker, Eeckhout and Unger and their critics, Bresnahan and Reiss, the 2023 Merger Guidelines, the MillerCoors studies and Axtell; the markups dial is updated and a new dial opens (one product's own-price elasticity); the Facts on productivity dispersion and Zipf's law for firms are shown; the 2008 MillerCoors clearance as *Called it?* (partly right). Not verified, so stated in words or computed on the Island instead: BLP's own elasticities and markups, Nevo's margins, the cereal industry's concentration ratios in the 1990s; Bresnahan and Reiss's finding is stated from the abstract |
| 44 | built, English | *Dynamics, Platforms and Antitrust.* Agora's `io` (II): Rust's model with the nested fixed point (Newton-Kantorovich) and Hotz and Miller's CCPs with renewal, replicated on his data (RC 9.79, theta 2.65, myopia rejected), the average cost of a replacement rule, a Pakes-McGuire duopoly, double marginalization, Armstrong's platform, lock-in by an inferior first mover, Arrow's replacement effect and the step-by-step inverted U, a killer acquisition, Q-learning price setters (profit gain 0.86, punishments in every session) and Baron and Myerson's regulator; the Data Room gains Rust's Madison bus panel (162 buses, 1974-1985, from the MIT-licensed mirror of his files), with tables from Rust, Hotz and Miller, Ericson and Pakes, BBL, Ryan, the vertical cases, Rochet and Tirole, Armstrong, Rysman, QWERTY's debate, Arrow, Aghion et al., Cunningham, Ederer and Ma, Calvano et al., Assad et al., the antitrust cases, Baron and Myerson, Kwoka and IDC; two new dials (merger retrospectives; the discount factor, profiled on Rust's data); Ballmer's 2007 iPhone remark as *Called it?* (wrong). Not verified, so stated in words or computed instead: Rust's own estimates (replicated here), Calvano et al.'s profit gains, the share of killer acquisitions, Assad et al.'s margin effects, network-effect elasticities |
| 45 | built, English | *Behavioural Economics.* Agora's `behave`: present-biased gym members who forecast with a belief about their own bias (monthly members forecast 13.9 visits, make 4.7, pay $15.02 a visit against a $10 pass) and the contract a gym designs for them (visits below cost, p = m - (1 - beta) b), an endowment-effect mug market (24% traded, not 50%), marathon bunching measured with Part 41's estimator, putts for par and birdie, loss-averse condominium sellers bracketed by two regressions, O'Donoghue and Rabin's naifs and sophisticates, a randomized commitment account (Wald ratio), defaults through procrastination and Save More Tomorrow, shrouded add-ons, left-digit bias and its estimator, rational inattention, sparsity, Fehr-Schmidt players, a filtered nudge literature with the Andrews-Kasy correction, rational and diagnostic forecasters; the Data Room gains List's 148 card-show traders (via AER), whose swap rate rises from 0% for non-traders to about half for regulars; prospect theory refitted to choices13k (lambda 1.13); three new dials (loss aversion, present bias, the effect of a default); experts' forecast that a token piece rate would crowd out effort as *Called it?* (wrong). The syllabus's draft facts checked against the sources: DellaVigna and Malmendier's 7,752 members, $70, 4.3 visits, $17 against $10; SEED's 28.4% take-up and 81-point rise; Madrian and Shea's 37% to 86% (as the authors later summarized it); Lacetera, Pope and Sydnor's $150-200 steps in 22 million sales; Pope and Schweitzer's two points; Genesove and Mayer's 25-35%; DellaVigna and Linos's 8.7 against 1.4 points. Not verified, so stated in words: Kahneman, Knetsch and Thaler's exact medians (stated as about two to one), Augenblick, Niederle and Sprenger's beta values |
| 46 | built, English | *Development.* Agora's `village`: a poverty trap from a technology with a fixed cost (steady states 9 and 59.8, threshold 18.2; a one-off transfer of 10 leaves 59% of households above it after twelve years, one of 20 97%), Lewis's surplus labour and turning point, the moneylender's break-even rate, a randomized microlender with quantile effects and a bootstrap band, the village multiplier, Townsend's test, index insurance with basis risk and trust, deworming with spillovers, a school-building difference in differences with its Wald ratio, a historical boundary by regression discontinuity, present-biased farmers and the timing of a fertilizer offer, bed-net demand by price, heterogeneous sites with partial pooling, targeting by village, phone and registry, and the aid budget at the margin; the Data Room gains the World Bank's $3.00-a-day headcounts and agriculture shares (the raw productivity gap recomputed for 172 countries) and three experiments from causaldata: Thornton's Malawi incentives (34% collected results with none, 79% with any), Cai, de Janvry and Sadoulet's insurance sessions (a default of buying +11 points) and Manacorda, Miguel and Vigorito's PANES households (support +10 points at the cutoff, by local linear regression); two new dials (the return to capital in small firms; the consumption effect of a cash transfer) and rows added to the return to schooling; Sachs's 2005 forecast as *Called it?* (wrong). The syllabus's draft facts checked against the sources: Cohen and Dupas's 20 clinics and 60% fall; Duflo, Kremer and Robinson's 24% base and 14 points (the syllabus had no number); Balboni et al.'s 6,000 households over 11 years; Banerjee et al.'s five of six sites; Egger et al.'s multiplier of 2.5. Not verified, so not stated: Schultz's enrolment effects in points (the gains after primary school and the 8% return are stated) |
| 47 | built, English | *Political Economy.* Agora's `politics`: Olson's group effort (9 for one member, nothing from 100) and a contest between a small and a large group, Tullock's contest (80% of the prize dissipated by five players; the asymmetric case in the problems), the build-or-lobby game (340 if all build, 104 in equilibrium), probabilistic voting with an organized group, a local linear regression discontinuity with robust errors, the Barro-Ferejohn threshold and lame-duck mayors (29% less taken by those who can run again), Acemoglu and Robinson's franchise as commitment with a map of revolution, democratization and promises, Olken's road audits on the Island (audit -8.0 points, s.e. 1.5, against a planted -8), Nordhaus's cycle and delegation, a rainfall instrument for conflict (OLS -1.51, 2SLS -1.97 against a planted -2); the Data Room gains Cattaneo, Frandsen and Titiunik's Senate elections from rdrobust (barely winning worth 7.41 points, s.e. 1.46, at the next election, matching rdrobust's documented estimate), the World Bank's tax revenue, control of corruption and GDP per head (corruption control correlated 0.72 with log income for 195 countries; tax 13% of GDP in the poorest quarter against 22% in the richest, 150 countries), the Pink Sheet's US and EU sugar prices (US sugar at a median of 1.9 times the world price, 1960-2026) and more of V-Dem's electoral democracy index (the world from 0.14 in 1900 to 0.53 in 2012 and 0.48 in 2025); two new dials (the share of spending lost to corruption; the incumbency advantage); the Treasury's May 2016 forecast as *Called it?* (wrong). The syllabus's draft facts checked against the sources: Olken's control mean is 27.7% in J-PAL's summary (the draft said about a quarter; the film says more than a fifth), the audit effect about 8 points and meetings small (verified); GAO's 2023 sugar estimates; Krueger's 7.3% and 15%; Ferraz and Finan's 27% with a 2025 replication's smaller estimates. Not verified, so not stated: Olken's control mean in the paper itself, and Lee's probability of winning |
| 48 | built, English | *Environment and Climate.* Agora's `climate`: Hotelling's rule on an Island mine (the rent from 1.01, exhausted in year 43; with costs falling 4% a year the price falls for 20 years first), the Simon-Ehrlich bet over every ten-year window from 1960 (Ehrlich wins 28 of 55; 1980-90, -38%), Gordon's fishery and Smith's fleet (open access to 0.2 of the natural stock, an overshoot to 0.03, a traded quota holding 0.72), a four-box carbon cycle (the IPCC's impulse response, timescales scaled 0.47, land use weighted 0.55) and a two-layer energy balance (ECS 3; other gases +36%; sulphur -0.44 W/m2 per 100 Mt) fitted to Mauna Loa (0.8 ppm) and HadCRUT5 (last decade 1.30 against 1.30), a DICE-style model on it with DICE-2023's damages and backstop (optimal warming 2.6 in 2100, 38% cut by 2050 at $110 a tonne; the SCC $561, $183, $88, $37 at 1, 2, 3, 5% against DICE-2023's $485, $176, $87, $32; $63 with rho 1.5% and eta 1.45, $408 with the Stern Review's 0.1% and log utility), fat tails (losses of 5% thin against 8-96% fat as the cut-off rises from 6 to 20 degrees), a climate club (nobody without a tariff, all fifteen at 9%), Wright's law on IRENA's solar prices (30% per doubling, 2000-2025), a toy of directed technical change, Burke, Hsiang and Miguel's panel run on ERA5 and World Bank data for 185 countries, 1961-2023 (optimum 10.5 degrees; -1.0 points per degree at 25), and a merit-order market where holding back 2 of 14 GW multiplies a firm's profit 28 times; the Data Room gains NOAA's CO2, HadCRUT5, the Global Carbon Budget, ERA5 temperatures, constant-dollar GDP per head, IRENA's solar, FAO's fish stocks and oil production; three dials (the social cost of carbon, energy elasticities, warm years and growth); Hubbert's 1956 peak as *Called it?* (partly right). The syllabus's draft facts checked against the sources: the bet's $576.07 and dates, Kiel et al.'s 61.6% of 99 decades (the draft said Ehrlich would 'mostly' have won: right), DICE-2023's tables, the US estimates, BBW's shares, the Huai River's 5.5 and 3.1 years. Not verified, so not stated: DICE-2016R's discounting parameters, the count of minerals in Slade (1982), the IEA's past solar forecasts (the solar-forecast *Called it?* the draft planned was replaced by Hubbert) |

**Corrections found while building Part 1** (the plan's draft, written from memory, against the sources): Bastiat's
Paris passage is in *Economic Sophisms*, First Series, ch. 18 (1845), not the *Harmonies*; Hume's is/ought passage is
in Book III of the *Treatise* (1740); after the Black Death England's GDP per head rose, and the long fall came in the
seventeenth century; the Survey of Professional Forecasters' August 2008 median for 2009 was +1.5% against an outcome of
−2.6%; Chamberlin's 1948 market is described from secondary summaries (Roth 1995), not re-read.

**Corrections found while building Part 2.** Smith's first double auction was in January 1956 (his Nobel
autobiography), not 1955; his worry that convergence was "an accident of symmetry", and the lopsided design he ran to
answer it, are his own words there, and they became the part's Play-it market. Marshall's 1890 text compares each
principle to "one blade of a pair of scissors"; the sentence about the upper and the under blade is from the later
editions (third, 1895; quoted from the fifth, 1907). The Dial rows are petrol, cigarettes and alcohol, from three
meta-analyses; housing services, in the draft, wait for Part 37. Gallet and List's mean (−0.48) is read from *Tobacco
in Australia*, not the paper. The Bureau of Labor Statistics published no consumer price index for October 2025;
deflated series fill that month from its neighbours and say so.

**Corrections found while building Part 3.** The 1934 report was transmitted on 4 January 1934 (the letter is dated 3
January); the warning "the welfare of a nation can, therefore, scarcely be inferred from a measurement of national
income" is on p. 7 of Senate Document 124, read in BEA's 2020 reprint, beside the passage on "housewives' services".
Petty's estimate is in *Verbum Sapienti* (written 1665, printed 1691): six million people at £6 13s 4d a head, £40
million, of which the stock yields £15 million and labour £25 million; he used the split to apportion a war tax. The
Boskin Commission's 1.1 points break down as 0.15, 0.25, 0.10 and 0.60 (Gordon 2006; Moulton 2018), and Lebow and
Rudd's estimate is 0.87 (0.9 in their abstract). Deaton and Heston's revision is the 2005 round only (China 40%
smaller, India 36%); the 2011 round in the draft is left out. Leontief's 1936 table is of 1919. The household survey
was not taken in October 2025, so the unemployment rate for that month does not exist; the intermission turns that
gap into a rest in its melody. The draft's social accounting matrix became an input-output table with four
industries; unemployment's flows wait for Part 24; the Big Mac index is mentioned, not used.

**Corrections found while building Part 4.** The story now opens with Moore's pig iron (1914, p. 126, quoted from the
*Econometrics Journal*'s 2025 editorial) and Wright's 1915 review; Working (1927) frames the question rather than
opening it. Stock and Trebbi (2003) attribute Appendix B to Philip Wright, not Sewall. The draft lottery of 1
December 1969 was not a fair draw: the correlation between birthday and draw order is −0.23, and only 1 of 20,000
fair shuffles comes as far (Fienberg 1971 told the story of the unmixed capsules). LaLonde's table 5 is for men; on
Dehejia and Wahba's subsample the experiment says +$1,794 and the adjusted PSID comparison +$1,548. The New Jersey
income-maintenance experiment ran 1968–72 with about 1,350 families and eight plans (guarantees of 50–125% of the
poverty line, tax rates of 30, 50 or 70%); PROGRESA's evaluation used 506 villages, 320 first and 186 about two
years later. Lucas's syllogism is quoted with its page (p. 41) from the secondary literature; the article was not
re-read. Card's (2001) table 2 is entered as eleven rows (the two with schooling as a dummy are left out). The plan's
chapter on forecasts as tests became the *Called it?* card in chapter 6; forecasting as a test waits for Part 57.

**Corrections found while building Part 5.** Samuelson was twenty-two, not twenty-three, when "A Note on the Pure
Theory of Consumer's Behaviour" appeared (February 1938; born May 1915); his phrase is "dropping off the last vestiges
of the utility analysis", and Moscati (2019) warns against reading him as a strict behaviourist. The eleven budgets of
Play it are Harbaugh, Krause and Berry's number (eleven choice sets of chips and juice, 2001); Choi et al. (2007) used
fifty, and their published mean index is 0.954 (60 of 93 subjects above 0.95, as reported in Choi et al. 2014). Kagel
et al.'s animal results are taken from Harbaugh et al.'s summary of Kagel, Battalio and Green (1995): 87% of rats and
81% of pigeons. Jensen and Miller's Giffen behaviour was among poor households, not the very poorest. Varian's 1982
test of US aggregate data was not read, so the part runs its own test on BEA's fifteen categories and reports its
power. The money pump is credited to Davidson, McKinsey and Suppes (1955), who credit Norman Dalkey.

**Corrections found while building Part 6.** Jensen and Miller's Hunan elasticity is +0.45 for households under 80%
of their calories from rice (+0.64 between 60% and 80%; +0.22, not significant, for everyone), not "about +0.2"; their
subsidy cut a 1.20-yuan jin of rice by 0.10–0.30 yuan, up to a quarter, for five months of 2006. Marshall gave no
reference for Giffen, and Stigler (1947) could not find the claim in Giffen's writings. Hausman's cereal is valued at
$78.1 million a year in the US with a virtual price of $7.14 against $3.48 (his NBER chapter, published 1997). Hamilton's
CPI-bias estimates (2.7 points a year in 1974–82, 0.6 in 1982–91) are read as Costa (2001) reports them. Housing and
energy elasticities, in the draft's dials, wait for Parts 37 and 48.

**Corrections found while building Part 7.** Bernoulli's own game pays one ducat for heads on the first toss and
doubles after (prizes 1, 2, 4, …), so on his logarithm it is worth $5.97 to someone with $1,000, not the $10.95 often
quoted for a game that starts at $2; Cramer's "about 2.9" is for the same 1, 2, 4 game. Savage's answers at the
lunch in May 1952 broke the independence axiom, but the sources do not agree on which options he chose, so the part
does not say. Kahneman and Tversky's first Allais problem drew 82% for the sure 2,400. The game-show evidence is Post,
van den Assem, Baltussen and Thaler (2008): risk aversion falls after both losses and gains, a break-even effect.
Hayden and Platt (2009) give the bids for Bernoulli's game: a median of $1.75 with real money (20 students) and $1.50
hypothetically (220), flat across truncations. Samuelson's 1937 note runs to seven pages and was written while he was
a graduate student. Sydnor's (2010) implied risk aversions were not read, so the deductible example uses illustrative
numbers computed on screen. Madrian and Shea's figures (86% against 37%; 76% at the default) are the NBER working
paper's. The plan's "In practice" chapter also carries the social discount rate (Ramsey's formula as an is/ought
card); the Stern–Nordhaus numbers wait for Part 48. The prospect-theory pointer is to *Psychology, Built* Part 26,
*Judgment and Choice*.

**Corrections found while building Part 8.** The 1928 formula refits from Cobb and Douglas's own indices (as
reproduced by Felipe and Adams 2005) to P′ = 1.01 L^0.746 C^0.254; Felipe and Adams's table 2 gives the unrestricted
and trend fits that the part shows breaking it. The Penn World Table puts the US labour share near 62% from 1950 to
1999 and at 56.8% in 2023: the fall the draft dated "since about 1980" is mostly after 2000 in this series (other
measures differ, so the Fact says which series it is). GM bought 60% of Fisher Body in 1919 and the rest in 1926;
the part tells the hold-up story as Klein, Crawford and Alchian (1978) told it, then the 2000 *Journal of Law and
Economics* dispute, and does not settle it. Douglas's own account of the 1927 collaboration (Douglas 1976) is
summarized without the details of where they met; the six-tenths rule is credited to Williams (1947) without its
title, which was not re-read; Hall and Hitch's sample is "a few dozen" firms. The learning curve is drawn at a fifth
per doubling as an illustration, not as Wright's estimate.

**Corrections found while building Part 9.** Radford's camps were Oflags, officers' camps, of 1,200 to 2,500 men;
the padre's walk happened in a transit camp in Italy, and the salmon's two cigarettes in twenty in a transit camp in
general; the liberation was on 12 April 1945 by elements of the 30th U.S. Infantry Division (all from the article).
The draft's Edgeworth box is Edgeworth's idea but not his drawing: he named the contract curve (1881, p. 21) and the
box in its familiar form came later, from Pareto and Bowley. Hsieh and Klenow's headline gains (30-50% for China,
40-60% for India) are relative to US efficiency in 1997; full equalization gives 87-115% and 100-128%. Scarf's 1960
economy is told as textbooks give it (each trader wants its own good and the next in fixed proportions); the
original paper was not reached. The draft's *Called it?* (the convergence theorem against Scarf's cycle) became the
NAFTA forecasts, a dated prediction with an outcome, and Scarf's cycle a chapter of its own. Oil prices from 2026 show
a spike the film does not explain. Kantorovich worked for the plywood trust in the late 1930s and published in 1939.

**Corrections found while building Part 10.** Dupuit's 1849 passage on the third-class carriages is paraphrased, not
quoted: the French text was not re-read. The draft's Play it (a bridge toll) became Bo's ferry, the same problem on
the Island. The draft's dial, markups by industry, became the aggregate markup, because that is where the measurement
is contested: De Loecker, Eeckhout and Unger's sales-weighted mean of 1.21 in 1980 and 1.61 in 2016 (the published
abstract; earlier working papers give 1.18 and 1.67) against Traina's flat or falling aggregate. Oi's two-part tariff
needs more ordinary visitors than keen ones: with one of each, shutting the ordinary visitor out pays (98 against
73), so the film uses two to one. Coffee's pass-through is incomplete in percent (0.15 at once, 0.55 after six
quarters) but about complete in dollars, once a pound of roast coffee is counted as 1.19 pounds of green beans; the
chapter says so. Nakamura and Zerom are read in the NBER working paper (2009); Dubé and Misra, Calvano et al. and Assad
et al. from their published abstracts. The draft's chapter 14, "In practice: Part 60", became Littlewood's rule, with
the airline war left to Part 60.

**Corrections found while building Part 11.** The Flood-Dresher experiment is dated to the start of 1950 (the
Stanford Encyclopedia says early 1950); the joint outcomes (60 mutual cooperation, 14 mutual defection) are
Poundstone's count from Flood's report, which was not re-read, and Nash's comment is quoted from the same accounts.
Nagel's 2/3 sessions had 67 subjects in four sessions of 15 to 18, a first-round mean of 36.73 and median of 33 (read
in the article). The Financial Times contest's mean (18.9) and winning number (13) are from secondary accounts.
Axelrod's second tournament is given as "more than sixty entries", the figure not having been checked. The penalty
kick's scoring table is illustrative; the published tests are cited for their findings, not their numbers. In
Agora's own round robin tit for tat comes fifth, behind tit for two tats, which the chapter says, with Axelrod's own
remark that tit for two tats would have won his first tournament. The draft's dials line had no dial for this part;
the depth of reasoning was added, with two of its three rows Agora's fits to published means, labelled as such.

**Corrections found while building Part 12.** The hook was "the Maui tapes"; the lysine story is now told from
Connor's 1998 article (the prices stated in its text, the months between left blank), and the slogan is attributed
as the Justice Department describes it, to ADM's president on a tape played at the trial, since accounts differ on
who first said it. ADM's 1996 fine was $100 million in all, $70 million of it for lysine; three ADM executives,
the informant among them, went to prison. Hotelling's 1929 examples are given as his own political one; the cider
and churches often quoted were not checked. Agora's Dixit model was first written with the incumbent able to threaten
any capacity, which made deterrence possible where it is not credible; it now caps the incumbent's reply at its
capacity and floors it at its reply at full cost, so only capacities between the two Cournot points deter, and the
Island's numbers (slips at $30, use at $10, a setup cost of $144) give strategic deterrence at 36. Rockets and
feathers could not be seen in monthly data (a first-month difference of 1 cent, standard error 11), and the chapter
says so. The 3-7% common-ownership effect sometimes quoted was not verified and is not used; the dispute is shown
instead. Called it? was planned as Stigler on which cartels cheat; it is Stigler's claim that secret price cuts break
cartels, judged partly right from Levenstein and Suslow's survey.

**Corrections found while building Part 13.** The rejections are given as Akerlof's essay recalls them (the
AER's and the RES's "triviality"; the JPE's referees: if correct, no goods could be traded), from excerpts; the
"fourth attempt" sometimes quoted was not checked. Harvard's PPO is told from Cutler and Zeckhauser's figures
(charges of about $500, $1,000 and over $2,000, enrollment about 20%, 15% and 9%, in 1996 dollars), not from Cutler
and Reber's paper, whose scanned text could not be read; their welfare and premium figures are from its abstract.
Einav, Finkelstein and Cullen's numbers are from the 2008 working paper; Agora's rebuild from the two published lines
gives $9.46 against their $9.55. Sheepskin effects are stated qualitatively, without numbers. The
credit-rationing example lets the risky projects be slightly worse, as well as riskier, so that the bank's return has
a clear peak; Stiglitz and Weiss's own projects have equal means. Agora's death spiral is a stylized simulation,
shown beside Harvard's data, not fitted to it.

**Corrections found while building Part 14.** The plan's "the next harvest was larger than the previous five
together" is not used: accounts of Xiaogang's 1979 harvest give different numbers, so the film says only that it was
far larger. Safelite's 44% and its even split between incentives and sorting are the published paper's, as later
summaries give them; the 1996 working paper's 20-36% is shown beside it. Ford's turnover and absenteeism figures were
not checked and are not used; Raff and Summers are cited for the queues, productivity and profits, and Ford's
"cost-cutting" remark is given as quoted. Shaban's gap between owned and sharecropped plots is stated without a
number (only secondary figures were found); Operation Barga's 28% is from the paper's abstract. The Called it? was
planned on Lin's decomposition; it is multitasking against Chicago's test scores, and Lin's result is told in chapter
11. Incomplete contracts, planned as a chapter, are folded into chapter 14, since Part 8 told Grossman, Hart and Moore.
The top of the promotion ladder is credited to Rosen (1986), not to Lazear and Rosen (1981). The Swiss survey's
50.8% and 24.6% were read in Frey and Oberholzer-Gee's article.

**Corrections found while building Part 15.** The *Called it?* was planned on the acid-rain programme's forecast
costs against its permit prices; no forecast price was verified, so it is the forecast that benefits would about equal
costs (Portney 1990, as Schmalensee and Stavins cite it) against their tally. Cheung's survey was in the spring of
1972, of nine beekeepers; the rents are his means, and the money-nectar correlation is for the late-spring farms. The
Stockholm figures (about a fifth less traffic, 53% of the city's voters) are from summaries of the official evaluation.
Fehr and Gächter's contribution levels are stated qualitatively; the curves drawn are Agora's typed players. The
cod moratorium's job losses are given as about 30,000 in Newfoundland and Labrador (estimates range from about 19,000
direct to 40,000 nationally). Duranton and Turner's dial rows are their preferred OLS (0.86) and the TSLS estimate with
geography (1.03).

**Corrections found while building Part 16.** The story's Dutch shortfall is confirmed (less than €3 billion against
almost €10 billion forecast; Klemperer 2002). The chapters were regrouped: the laboratory evidence joins the failures of
equivalence (chapter 6), and Treasury and electricity auctions get their own chapter (12), so the plan's chapters 6 and
13 are folded in. The Treasury moved every auction to a single price in October 1998 after a 1992 experiment whose
evidence its own studies called not unambiguous (Garbade and Ingber 2005). The German auction of 1999 (Mannesmann's
18.18 and 20 million DM per MHz, two rounds) is from Klemperer's footnote, citing the *Frankfurter Allgemeine* and
Jehiel and Moldovanu. The film says only that the publisher offered exactly Goethe's price (Moldovanu and Tietzel), and
asks, without answering, whether the go-between had told him. Ostrovsky and Schwarz's headline estimate of about 13% was not robust (p = 0.09);
the dial uses their estimates at fixed search volumes (2.7%, -2.2% and 3.3%). The dial's return is Part 61, not Part 39.
The *Called it?* is the Dutch government's forecast, with Klemperer's warning in the outcome.

**Corrections found while building Part 17.** The story's dates are from Roth's Nobel lecture: hiring two years
before graduation by 1940 (not 1945), the medical schools' embargo of 1945, offers open ten days (1945), eight (1946)
and less than twelve hours by 1950. The planned chapter "what a lottery reveals" uses Agora's district and Denver's
charter estimates (Abdulkadiroğlu, Angrist, Narita and Pathak, Table 6); the dial uses the exam-school offer effects
from the 2011 working paper's Table 4, not the published tables, which were not read. The intermission is the US
marriage rate (the oldest matching market), since no NRMP series is in the Data Room. Refugee placement is given as
the authors' predicted range (roughly 40 to 70 percent higher employment), not as an experimental result. Chen and
Kesten's parallel mechanism is said to be used in many provinces, not most.

**Corrections found while building Part 18.** Discounting is part of chapter 10 (cost-benefit analysis) rather than a
chapter of its own, so capabilities is chapter 12, the Dials 13, the practice chapter 14 and the frontier 15. The
planned second dial (inequality aversion implied by tax schedules) is left for Part 41, where optimal tax
schedules are built; this part opens only the value-of-a-statistical-life dial, in 2024 dollars by the CPI-U. The intermission is
V-Dem's electoral democracy index (version 16) for the world and four countries. The practice chapter covers the
American and British guidance on discount rates and weights (Circular A-4 of 2003 and 2023, restored to the 2003
version by executive order in 2025) and the voting reforms and bans since 2018, with Alaska's system kept by voters in
2024 and again in November 2026. Arrow's paper is 1950 (*JPE*) and the book 1951. The Borda manipulation shown is the
lie that wins outright (A E C B D), not one that only ties; the rules break ties by letter, and the search now checks
each result with the letters' order reversed.

**Corrections found while building Part 19.** The Black Death's effect is stated from the Bank of England's series:
England's population fell from about 4.8 to 2.6 million between 1348 and 1351 (46%), and real wages rose to 2.2 times
their 1348 level by 1400 and 2.7 times by 1450 ("double" in the plan was too low). English real wages did not pass
their 1450 level for good until 1874. Ashraf and Galor (2011) is stated in words, not dialled. Broadberry, Guan and Li
(2018) date the start of the divergence to around 1700, when the Yangzi delta fell behind Europe's richest region; the
chart uses Maddison's 2023 series, whose China path rises to about 1700 and falls after. The Great Divergence data film
is the intermission (chapter 10 of the plan), so the chapters after it are renumbered: the Industrial Revolution is 7,
the transition 8, unified growth 9, *Was it good?* 10, the Dials 11, practice 12 and the frontier 13. Malthus's *Called
it?* is folded into the hook; the formal call is Ehrlich's (1968), with the Simon-Ehrlich wager. Kelly's (2019) point
about persistence studies is demonstrated in Agora with two independent smooth random fields (55% of slopes
"significant" at 5%). The chapter cards' timeline now starts at the century of the earliest year a chapter lights.

**Corrections found while building Part 20.** The night-time photograph of Korea is described, not shown; the hook's
numbers are Maddison's, which have no estimates for the north from 1944 to 1989 and put the north ahead in 1940 (2,624
against 1,975 dollars a head). Kaldor's facts are checked on the Penn World Table 11.0, with its internal rate of return
for the return on capital. Easterly's (1999) Zambia counterfactual is read from his figure 1 (about 20,000 dollars a
head against about 600). Solow's 1957 share of technical change is seven eighths as published; Hogan's (1958)
correction made it 90%. Young's residuals are the published QJE figures (Hong Kong 2.3%, Singapore 0.2%, Korea 1.7%,
Taiwan 2.6%, Korea and Taiwan outside agriculture); his 1994 working paper had Singapore at -0.3%. Hsieh (2002) is
quoted from his abstract. Samuelson's forecast is documented by Levy and Peart (2011); the planned *Called it?* on
Solow-model forecasts for Asia is left out. Hall and Jones's 31.7 = 1.8 x 2.2 x 8.3 is for the five richest and five
poorest countries in 1988; Caselli's success measures (0.40, and 0.26 in Hall and Jones's form) are for 1996. Lucas's
58, 5 and 1.04 are his 1988 calculation, redone on 2019 data. The Ramsey model is solved by shooting only (time
elimination is left to the lab's extensions). An intermission (investment and income, 1960-2023) follows chapter 6, so
the chapters after it keep the plan's numbers but sit after the film. Kremer, Willis and You's magnitudes are from
their working paper's introduction; Acemoglu and Molina's comment is stated with them.

**Corrections found while building Part 21.** Nordhaus's labour price of light is read from his table 1.6 (1996):
41.5 hours of work per 1,000 lumen-hours for the Babylonian lamp, 5.37 for the tallow candle in 1800 and 0.000119 for
the compact fluorescent bulb in 1992, a fall of about 45,000 times since 1800 and about 350,000 since Babylon ("several
hundred thousand" in the plan). Bloom et al.'s numbers are from the working paper: research effort ×23 since the
1930s, research productivity ÷41, Moore's law ×18, a decline of about 5.3% a year. Comin and Hobijn's 45 years and
"at least a quarter" are from their abstract. AJR's estimates are refitted from the copy of their data in hdm: first
stage −0.61 (0.13), OLS 0.52, 2SLS 0.92 against their published 0.94; Albouy's 28 of 64 is from his working paper. Dell's
25% and 6 points are from her abstract, and the chapter's regression-discontinuity picture is illustrative. Nogales's
numbers are *Why Nations Fail*'s. The Aghion-Howitt chapter compares the paper's risk-neutral market research with a
log-utility planner (Agora's), so the crossing step size (about 1.49) is the island's, not a general result. The social
return to R&D is dialled from Jones and Williams (30%, a conservative value), Bloom, Schankerman and Van Reenen (55%,
from their 2012 version) and Lucking, Bloom and Van Reenen (58%). An intermission follows chapter 7.

**Corrections found while building Part 22.** The 2001 rebates were $300 or $600 (and $500 for heads of household),
reached about two-thirds of households, and went out over ten weeks from late July to late September by the
second-to-last digit of the Social Security number; Johnson, Parker and Souleles's 20-40% is on nondurables in the
quarter of receipt, about two-thirds over that quarter and the next. The 2008 figures (12-30% on nondurables, 50-90%
with durables) are Parker, Souleles, Johnson and McClelland's abstract; the 2020 figure (about 10%, s.e. 3.4) is from
Parker, Schild, Erhard and Johnson's NBER working paper 29648. Hsieh (2003) found no response to Alaska's dividend in
survey data, and Kueng (2018) a 25% response within a quarter in account data, rising with income. Ganong and Noel's
6% and 12% are from their NBER working paper (an earlier draft gave 13% at exhaustion). Fagereng, Holm and Natvik give
no single MPC: small prizes to the cash-poor are spent in full within the year, large prizes to the cash-rich slightly
below half. Wei and Zhang's "about half" of the 1990-2007 rise in household saving is the authors' own estimate.
Campbell and Mankiw's lambda on US data since 1960 is weakly identified (first-stage F about 4), so the film reports
it with that warning and quotes their own estimate as about one half. The wealthy hand-to-mouth are shown with a
one-asset shortcut (an illiquid return of 7% against cash's 3%), not Kaplan and Violante's two-asset model. An
intermission follows chapter 7.

**Corrections found while building Part 23.** Mehra and Prescott's figures (1889-1978) are 6.98% for stocks and 0.80%
for bills a year after inflation, a premium of 6.18%, with consumption growth of 1.83% (s.d. 3.57%), and the model's
largest premium with sensible preferences 0.35%: the plan's "six" stands. Shiller's own series give a premium of about
5.7% over the same years (one-year bonds rather than bills). Barro's (2006) calibration is sixty disasters, a 1.7%
chance a year, falls averaging 29%; the Island's five-size distribution averages 30% and is not his. Smith, Suchanek
and Williams's dividend values are not quoted: the Island's market uses 0, 8, 28 and 60 cents as an illustration, and
the film quotes only their 14 bubbles in 22 markets. Zwick and Mahon's published effects are 10.4% and 16.9% (the 2014
draft's were larger); their implied user-cost elasticity of about -1.6 is as the paper reports it against earlier
work. Hassett and Hubbard's range of -0.5 to -1 is quoted from the papers that cite it. Novy-Marx and Rauh's shortfall
at Treasury rates is about $3 trillion for the fifty states' main plans; other versions give other totals. An
intermission follows chapter 9.

**Corrections found while building Part 24.** The Beveridge curve is drawn from JOLTS (December 2000 on); the plan's
"since 1951" would need the help-wanted index, which the Data Room does not hold, so the film states Beveridge's 1944
definition and draws the twenty-five years of JOLTS. The matching function is estimated with the CPS job-finding rate
(Shimer's method) against JOLTS openings per unemployed worker, giving 0.58 for 2001-2019; JOLTS's own hires give 0.31,
because they include people moving between jobs, and both are dial rows. The volatility ratio is recomputed for
2001-2019 (about 25) rather than Shimer's 1951-2003 (almost 20). Mortensen and Pissarides's 1994 claim is scored
partly right rather than wrong: their abstract claims only that aggregate shocks proxy the cyclical behaviour of job
creation and destruction reasonably well, and the pattern held while the size did not. Petrongolo and Pissarides's
range of 0.5 to 0.7 is quoted from the papers that summarize the survey. Kroft, Lange and Notowidigdo's callback rates
(about 7% falling to about 4%) are from the working paper and J-PAL's summary; their percentage fall is stated
differently in the two, so the film gives only the rates. Davis and von Wachter's 1.4 and 2.8 years of earnings are
from the abstract (men with three or more years of tenure, mass layoffs, Social Security records from 1974). Cahuc,
Postel-Vinay and Robin's finding of no significant bargaining power below the top of the skill distribution is from the
abstract and post-print summary, and shown at zero. The remote-work shares are from Hansen et al.'s 2023 version
(more than threefold in the United States, fivefold or more elsewhere, 2019 to early 2023). The Island's Burdett and
Mortensen ladder has unemployment of 17% (offers at 0.1 a month, separations at 0.02): an illustration of the ladder,
not a calibration. An intermission follows chapter 8.

**Corrections found while building Part 25.** Furness visited Yap in 1903; his book is of 1910, and Friedman's essay
(Hoover WP E-91-3, 1991) retells it; the painted crosses are from Furness as Friedman tells it, and the film says the
crosses were removed rather than how. The Bank of France's earmarked gold is given as "the early 1930s", Friedman's
"1932-33" not being re-read. Jevons's singer was paid a third of the takings: the book's opening page. Kiyotaki and
Wright's model A is run with the Island's goods (salt, coconuts, fish) and storage costs of the Island's own; in
Agora's grid the fundamental and speculative patterns never overlap, with a thin band between where neither pure
pattern holds, so the film does not claim multiple equilibria there. The quantity-theory scatter is the World Bank's
broad money and CPI for 1990-2024 (146 economies with at least twenty years), not McCandless and Weber's sample, which is
only cited. Cagan's German figures (322% a month on average, about 20% revenue-maximizing) are from secondary summaries
of his table; the film's Laffer curve uses alpha = 5. The Hanke-Krus peaks are from their table; Hungary's fifteen-hour
doubling time from Hanke's commentary, the others computed with a thirty-day month. The money multiplier is M2 over
the base (FRED reports BOGMBASE in billions). Stablecoin totals are DeFi Llama's as reported in December 2025. An
intermission follows chapter 8.

**Corrections found while building Part 26.** The syllabus's "a quarter of its deposits" for 9 March 2023 is not used:
the film gives the 42 billion withdrawn and the 100 billion queued (Barr's testimony) and the 94% uninsured share (the
Federal Reserve's review), not a share of deposits. Silicon Valley Bank's held-to-maturity bonds ($91 billion, about
$15 billion below book) are from its year-end 2022 accounts as reported; its capital ratio of about 12% from the review.
The savings-and-loan clean-up is given as "as much as $124 billion" to taxpayers (Curry and Shibut 2000). The Reserve
Primary Fund held $785 million of Lehman paper, about 1.2% of the fund, and was marked to 97 cents; the share of the
fund asked for on 16 September is given as "about a quarter" from secondary accounts. Money funds' total assets rose in
the fourth quarter of 2008 (Z.1): the run was from prime to government funds, and the film says so. Gorton and Metrick's
haircut index is described, not quoted; the critique that their sample is structured debt only is stated. Calomiris and
Mason's verdicts follow their abstract (no unexplained failure risk in the first two crises, the third ambiguous
and small, early 1933 a panic). Jiang, Matvos, Piskorski and Seru's figures ($2 trillion, about 10%, about 190 banks with about $300
billion of assets if half the uninsured left) are from their summaries. The deposit-beta rows are the New York Fed's and
S&P Global's as reported, with the 2004-06 peak shown at 0.6 ("approaching 60 percent"); the film's own are from the
FDIC's national rates. Reinhart and Rogoff's output fall is "over 9 percent" (shown at 9); Cerra and Saxena's 10% is
from their own later summary. Cookson and coauthors' estimates differ across versions, so the film gives the direction
only. USDC's low is given as about 88 cents. The Bank Term Funding Program valued collateral at par; the film calls
that beyond Bagehot rather than against him. Bernanke, Diamond and Dybvig shared the 2022 Nobel prize. An intermission
follows chapter 8.

**Corrections found while building Part 27.** The co-op had about 150 couples (Krugman 1998); sources differ on whether
a coupon bought an hour or a half-hour of sitting, so the film does not say; Sweeney and Sweeney is JMCB 9(1) (1977):
86-89. The film's unemployment rates for the 1930s are the NBER's monthly series (1.4% in 1929, 23% in 1933), which
differs from Lebergott's annual figures; the film says so. Bewley interviewed 336 people in 1992-93 (Howitt's review);
the syllabus's "Connecticut" is not used. About fourteen Phillips machines were built (the Science Museum Group); the
first in a garage in Croydon. Ball, Leigh and Loungani give the US coefficient as about -0.45 (a range of -0.4 to
-0.5), Japan -0.15 and Spain -0.85, in their working paper's introduction; the film's own estimate against the CBO's
gaps is -0.62. Okun's 1962 figure is shown as one third (three points of output per point of unemployment). The
Dickens project covered sixteen countries. Keynes's forecast is scored partly right: the reparations were cut and
abandoned and never paid in full, but Mantoux (1946) argued Germany could have paid. Guerrieri, Lorenzoni, Straub and
Werning's results are stated as in their working paper. Samuelson's "neoclassical synthesis" is dated to his 1955
edition. An intermission follows chapter 8.

**Corrections found while building Part 28.** Phillips's fitted curve is $\dot w + 0.900 = 9.638u^{-1.394}$ (wages
stable at about 5.5% unemployment). Samuelson and Solow's menu is stated as 5-6% unemployment for stable prices and
3% with 4-5% inflation. The Play it options are 3, 6 and 11 percent; 1973's annual-average inflation was 6.3%. Ball's
sacrifice ratio for the US disinflation is given as 1.8 as cited by Federal Reserve staff (other citations give 2.4);
Mankiw's 2.8 is his textbook calculation by Okun's law; the film's own is 2.0 against the CBO's potential. Hazell,
Herreno, Nakamura and Steinsson are described without their coefficients; the slopes shown are the film's aggregate
regressions (-0.65, -0.18, -0.07), close to the aggregate numbers quoted in their draft's introduction. The Fed's June
2021 projection (3.4% for 2021, 2.1% for 2022) is from the chair's press conference; PCE inflation is fourth quarter
on fourth quarter in the current vintage (5.7% and 6.1%). The Rogoff curve includes the variance that supply shocks
add to inflation (a first draft omitted it); the best weight is 0.31. An intermission follows chapter 8.
