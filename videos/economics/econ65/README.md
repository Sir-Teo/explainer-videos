# Economics, Built: Part 65, The Economics of AI

Part 65 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third of Act XII, *The Frontier*. It asks what happens to work, growth and
incomes if machines can do most tasks. Its answer: machines take tasks and the economy invents new ones, so wages
depend on which is faster and on how much cheaper the machines are. So far the experiments find large gains on single
tasks, most for the least experienced, and the arithmetic of adoption turns them into modest aggregate gains. If
machines can do every task, output can grow far faster while wages stop growing and income goes to whoever owns the
machines; while any essential task is left to people, that task sets the pace.

It opens with Keynes's *Economic Possibilities for our Grandchildren* (1930): in a hundred years the standard of life
in progressive countries four to eight times as high, and a fifteen-hour week. In 2022 GDP per head was 4.4 to 7.4
times its 1930 level in six rich countries (Britain 4.4, France 5.4, the United States 5.5, the Netherlands 5.6, Sweden
7.0, Germany 7.4), but hours per worker, though they fell by 12-45% from 1950 to 2023, are still 1,300-1,900 a year
against about 780. From there it covers:

- Play it: an economy whose ideas come from research tasks done by people or machines; automating half of them gives a
  boom to about 7% growth that fades, ninety percent a boom to about 24% around year 43 that falls back to under 7% by
  year 100, and every task an explosion past 50% a year by year 49;
- technology and work: the Luddites and Ricardo's chapter "On Machinery" (1821); Engels's pause on the Bank of
  England's series (GDP per head 35% above its 1770 level by 1840, the real wage 17%); the horse and Leontief's
  warning; the ATM, with Hannan and Hanweck's branch staff (about 20 per urban branch in 1988, a little over 13 by
  2004) and 39% more branches; new work (about 60% of US jobs in 2018 had titles that did not exist in 1940);
- the task model (Zeira; Acemoglu and Restrepo): with capital fixed, automating from a fifth of tasks to the point
  where machines stop being cheaper (two thirds) adds 67 log points of productivity to the wage and subtracts 109 of
  displacement, net -42; in the long run the wage rises but labour's share falls from 81% to 24%, and new tasks in
  which people are four times as productive restore it to 62% and raise the wage by another 25%; so-so automation
  (the wage gain from automating a tenth of the tasks falls from 53% to 3% as the machine's cost nears the wage);
  robots and jobs, and the wage structure;
- general-purpose technologies: the dynamo (electric motors under 5% of factory drive in 1899, about 78% in 1929);
  the productivity J-curve on the Island (measured productivity 6% below the old path in year 8, then 13% above it
  against a true 7%); Solow's paradox and American output per hour by period (2.8% a year in 1948-73, 1.4% in
  1973-95, 3.0% in 1995-2004, 1.5% in 2004-19, 2.3% since);
- the experiments: Noy and Zhang (time -40%, quality +18%), Peng et al.'s Copilot (-55.8%), Dell'Acqua et al.'s
  consultants (25.1% faster inside the frontier, 19 points less often right outside it), Brynjolfsson, Li and
  Raymond's support desk (+14%), METR's experienced developers (19% slower); the Island's desk recovers a 15% average
  and +33% for the least skilled fifth, against nothing for the most skilled;
- from tasks to aggregates: Eloundou et al.'s exposure (80% of workers with a tenth of tasks exposed, 19% with half);
  Hulten's theorem and Acemoglu's arithmetic (a fifth exposed, 23% of those adopted, a 14.4% cost saving: 0.66% TFP
  in ten years); the same arithmetic with wider adoption (2.6%) or everything exposed adopted (10.7%); Goldman Sachs
  and Aghion and Bunel;
- an intermission: hours worked a year per worker in six countries since 1950, against Keynes's line;
- wages and labour's share: the US labour share (PWT) from 63% in 1950 to 57% in 2023; the race between the automation
  frontier and capital (after Korinek and Suh): under business as usual the wage doubles in sixty years; if every task
  is automatable within twenty years or five, it falls to the cost of a machine doing the same work and stays there,
  while output grows ten-fold and labour's share falls from 73% to 6%;
- growth with automated research (Jones; Bloom, Jones, Van Reenen and Webb; Aghion, Jones and Jones): people's share of
  research costs rises from almost nothing to almost all as machines multiply, and growth falls back; Baumol's two
  sectors (growth slides from 3.3% to 0.9% a year as the automated good's share of spending falls from half to 7%);
- Nordhaus's tests on today's data: no acceleration of productivity, capital's share up from 37% to 43%, transistors
  doubling every two years; *Called it?*: Nordhaus (2021), too early to say;
- market structure: fixed costs that grow (training compute four to five times a year, Epoch AI), fast followers, a
  free-entry toy in which the frontier narrows from nine firms to one; who captures the surplus along the chain;
- policy: *Called it?*: Frey and Osborne's 47% (too early to say; payroll employment has risen 16% since September
  2013); Guerreiro, Rebelo and Teles's temporary robot tax; six levers; an *is / ought* card;
- agents that transact: Varian's model of sales (the average price paid is c + (1 - mu)(v - c), so buyer agents push
  prices towards cost); learning and language-model price setters; signals, congestion and liability;
- the Dials (generative AI on a task; AI's addition to productivity growth, both new), practice, and the frontier:
  scenarios (Korinek and Suh; Jones), adoption measured by survey (Bick, Blandin and Deming: 39% of Americans aged
  18-64 by August 2024) and by usage logs; *Called it?*: Keynes, partly right.

## Build it

```bash
python -m videos.economics.econ65.compute              # every number (a few seconds), into .cache/econ65/
python tools/qa_scene.py econ65 Tasks                  # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ65 -q l   # the whole part, silent preview
python tools/build.py econ65                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 65                     # the lab
```

The data are the Maddison Project Database, the Penn World Table 11.0, FRED (OPHNFB, PAYEMS), the Bank of England's
millennium series and Rupp's microprocessor trend data, all in the Data Room and registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md). Everything else is computed on the Island, or stated
from the papers listed in `dials.SHOWN[65]`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Keynes's grandchildren | The essay's two forecasts against the record; the question; objectives |
| 1 | Play it: automate the lab | Five shares of research automated; booms, bottlenecks and an explosion |
| 2 | Technology and work, historically | The Luddites and Ricardo; Engels's pause; the horse; the ATM; new work |
| 3 | The task model | Displacement, productivity and new tasks; the wage and labour's share; so-so automation |
| 4 | General-purpose technologies | The dynamo; the J-curve; Solow's paradox in the data |
| 5 | What the experiments find | Five studies; the Island's support desk; the jagged frontier |
| 6 | From tasks to aggregates | Exposure; Hulten's arithmetic; three readings; the map |
| — | Intermission | Hours worked in six countries since 1950, as lines and a tune |
| 7 | Wages and labour's share | The US labour share; the race between automation and capital; the wage floor |
| 8 | Growth with automated research | Ideas getting harder to find; the research bottleneck; Baumol's disease |
| 9 | Nordhaus's tests | The signatures of a singularity, on today's data; *Called it?* |
| 10 | Market structure | Fixed and marginal costs; a free-entry toy; the chain |
| 11 | Policy | *Called it?*: Frey and Osborne; robot taxes; six levers; is and ought |
| 12 | Agents that transact | Varian's shoppers; software sellers; market design |
| 13 | The Dials | Generative AI on a task; AI's addition to productivity growth (both new) |
| 14 | In practice | Workforce strategy, policy, measurement; three cautions |
| 15 | Frontier | Scenarios; adoption by survey and by usage; *Called it?*: Keynes |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 66, *Geoeconomics and Industrial Policy* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `automation` module
(`explainer.economics.agora.automation`); the narration states the cached numbers.

- **Keynes.** GDP per head in 2022 against 1930 (Maddison Project) for Britain, the United States, France, Germany,
  Sweden and the Netherlands; average annual hours per person employed (PWT `avh`) for the United States, Britain,
  Germany, France, Japan and South Korea; fifteen hours a week times fifty-two.
- **The task model.** Tasks on [N - 1, N] combined with elasticity sigma = 0.8; capital on tasks below I, labour above;
  labour spread optimally over its tasks acts like a quantity J = integral of g^(sigma - 1), with g = 4 in new tasks
  (above 1) and 1 elsewhere. Short run: K = 2, L = 1, a task automated only while capital is cheaper there. Long run:
  capital at a rental of 0.8, the wage from the unit-cost condition. So-so: the tasks from 0.5 to 0.6 automated at
  rentals from 0.3 to 0.95.
- **The J-curve.** Intangible investment with a hump-shaped flow peaking at 5% of output over ten years from year 3,
  plus upkeep of 10% of the stock; the stock raises output by half its size four years after it is built; measured
  productivity Y - I, true Y/(1 + 0.25 H).
- **The desk.** 2,000 agents with skill ~ N(0, 1), log output 0.9 + 0.22 skill + noise (s.d. 0.18); half treated at
  random; the effect on log output 0.14 - 0.11 skill, at least -0.02.
- **Hulten.** TFP gain = exposed x adopted x labour-cost saving x labour's share of those tasks' costs (0.535).
- **Growth.** Y = A K^0.35 L^0.65, saving 25%, depreciation 5%, population and researchers growing 1%; research input
  a CES (sigma = 0.3) over automated tasks (capital in research, 5% of K, in researcher-equivalents) and people's
  tasks; dA = 0.02 R A^0.5. Stopped when growth passes 50% a year.
- **Baumol.** Two goods with elasticity 0.5, productivity growing 6% and 0.5% a year, half of spending on each at
  the start.
- **The race.** The short-run task model with sigma = 0.8, machines' productivity 0.4 per unit of capital, saving 20%,
  depreciation 5%, K starting at 2; the frontier 0.3 + 0.25 (1 - exp(-t/40)) under business as usual, or rising
  linearly to every task in 20 or 5 years.
- **Nordhaus.** OPHNFB, annual averages by decade and first quarters by period; 1 - PWT `labsh` for the United States;
  the transistor doubling time by least squares on log2.
- **Shoppers.** Varian's equilibrium price distribution with four sellers, v = 1, c = 0.4, integrated numerically.
- **Entry.** A market of 40 doubling each year, a frontier cost of 0.4 tripling; N = floor(sqrt(M/F) - 1).
- **The intermission.** PWT `avh` for six countries, 1950-2023; the melody is their average.

## Problems and solutions

**1.** *The task model: with Y = (integral over [N - 1, N] of y(i)^((sigma - 1)/sigma) di)^(sigma/(sigma - 1)),
capital on [N - 1, I] and labour L spread over [I, N], show that w = Y^(1/sigma) (N - I)^(1/sigma) L^(-1/sigma), and
split d ln w into displacement and productivity.*

*Solution.* Each labour task gets L/(N - I) workers, so the labour tasks contribute (N - I) (L/(N - I))^r, with
r = (sigma - 1)/sigma, which is (N - I)^(1/sigma) L^r. Output is Y = (C + (N - I)^(1/sigma) L^r)^(1/r), where C is the
capital tasks' term. The wage is dY/dL = Y^(1 - r) (N - I)^(1/sigma) L^(r - 1); since 1 - r = 1/sigma and r - 1 =
-1/sigma, w = Y^(1/sigma) (N - I)^(1/sigma) L^(-1/sigma). Taking logs with L fixed, d ln w = (1/sigma) d ln Y +
(1/sigma) d ln(N - I): automation (I up) lowers N - I, the displacement effect, and raises Y, the productivity effect.

**2.** *Hulten: show that if tasks making up a share s of GDP become cheaper by a fraction c, TFP rises by about s c;
reproduce Acemoglu's two thirds of a percent.*

*Solution.* With competitive markets, aggregate TFP growth is the sum over activities of their sales as a share of GDP
times their own productivity growth (Hulten's theorem, Part 63). A fall of c in the cost of activities with share s is
a productivity rise of about c in them, so TFP rises by about s c. Acemoglu's inputs: s = 0.20 x 0.23 = 0.046 of GDP,
c = 0.27 x 0.535 = 0.144, so s c = 0.0066, two thirds of a percent over the decade in which the adoption happens.

**3.** *Baumol: two goods with elasticity epsilon < 1 and productivity growth g1 > g2; show that good 1's share of
spending tends to zero and aggregate growth to g2.*

*Solution.* With a common wage, prices are inverse productivities, so p1/p2 falls at rate g1 - g2. With CES demand,
spending shares are proportional to a_i p_i^(1 - epsilon), so the ratio of good 1's share to good 2's falls at rate
(1 - epsilon)(g1 - g2) > 0 and tends to zero. Real growth is the spending-weighted average of the sectors' growth
(a Divisia index), s1 g1 + (1 - s1) g2, which tends to g2 as s1 tends to zero.

**4.** *Varian: in the model of sales with a share mu of shoppers, show that each seller's expected profit is
(1 - mu)(v - c)/n and that the average price paid is c + (1 - mu)(v - c).*

*Solution.* In the mixed equilibrium every price in the support earns the same profit. At the top, p = v, a seller
never wins the shoppers (the price is almost surely the highest) and sells only to its share of the captive buyers,
(1 - mu)/n, earning (1 - mu)(v - c)/n. Summing over n sellers, total profit is (1 - mu)(v - c). Total profit is also
the average price paid minus c, times the one unit each buyer buys, so the average price paid is c + (1 - mu)(v - c).

**5.** *Free entry: with Cournot profits M/(N + 1)^2 and a fixed cost F, find N*; how fast must M grow to hold N*
fixed if F triples every year?*

*Solution.* Entry continues while M/(N + 1)^2 >= F, so N* is the largest integer with N + 1 <= sqrt(M/F), about
sqrt(M/F) - 1. N* depends only on M/F, so holding it fixed needs M to grow as fast as F: tripling every year. If M only
doubles, M/F falls by a third a year and N* + 1 by a factor of sqrt(2/3) a year, about 18%.

**6.** *Ideas: in dA/dt = theta S^lambda A^phi with S growing at n, show that g_A = lambda n/(1 - phi); then let a share
beta < 1 of research tasks use capital, with sigma < 1, and show that growth returns to the same rate.*

*Solution.* g_A = theta S^lambda A^(phi - 1). On a balanced path g_A is constant, so lambda n + (phi - 1) g_A = 0, and
g_A = lambda n/(1 - phi). With automated tasks, research input is R = [beta^(1/sigma) K_R^r + (1 - beta)^(1/sigma)
S^r]^(1/r) with r < 0. As K_R grows faster than S, K_R^r tends to zero and R tends to (1 - beta)^(1/(sigma r)) S, a
constant times S: the people's tasks bind. The equation for ideas is then the same as without automation up to a
constant, and g_A returns to lambda n/(1 - phi) (here lambda = 1), after a boom while K_R catches up.

## Lab and interactive

- `python -m videos.economics.labs 65`: Keynes's forecasts on the Data Room; the task model's decomposition and its
  long run; so-so automation; the J-curve; the support desk's experiment; Hulten's arithmetic; growth with automated
  research and the bottleneck; Baumol's two sectors; the race between automation and capital; Varian's shoppers.
- The interactive (course site): automate. The reader sets the share of research tasks done by machines and how
  complementary the tasks are, and watches the growth rate and people's share of research costs over two centuries.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[65]`; the new Dials (generative AI on a
task; AI's addition to productivity growth) are in `explainer/economics/dials.py`, and the *Called it?* records of
Keynes (1930), Frey and Osborne (2013) and Nordhaus (2021) in `explainer/economics/calls.py`. The methods are stated
from the works cited in the chapters (Ricardo 1821, Keynes 1930, Baumol 1967, Varian 1980, Leontief 1983, Devine 1983,
David 1990, Jones 1995, Zeira 1998, Autor, Levy and Murnane 2003, Hannan and Hanweck 2008, Nordhaus 2008, Allen 2009,
Autor 2015, Bessen 2015, Acemoglu and Restrepo 2018, 2019, 2020 and 2022, Aghion, Jones and Jones 2019, Acemoglu,
Manera and Restrepo 2020, Bloom, Jones, Van Reenen and Webb 2020, Calvano et al. 2020, Brynjolfsson, Rock and
Syverson 2021, Nordhaus 2021, Guerreiro, Rebelo and Teles 2022, Acemoglu and Johnson 2023, Briggs and Kodnani 2023,
Dell'Acqua et al. 2023, Noy and Zhang 2023, Peng et al. 2023, Acemoglu 2024, Aghion and Bunel 2024, Autor, Chin,
Salomons and Seegmiller 2024, Bick, Blandin and Deming 2024, Eloundou et al. 2024, Fish, Gonczarowski and Shorrer
2024, Jones 2024, Korinek and Suh 2024, Brynjolfsson, Li and Raymond 2025, Korinek and Vipra 2025, METR 2025) and
computed here.
