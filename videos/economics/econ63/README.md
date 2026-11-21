# Economics, Built: Part 63, The Economy as a Network

Part 63 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act XII, *The Frontier*. It asks when a shock to one firm becomes a
shock to everyone. Its answer: to a first approximation, when the firm or sector is large, because a sector matters by
its sales (Hulten's theorem) and, with firms as unequal as real ones, their own shocks do not cancel out. Beyond that,
when the shock is large and the input hard to replace, when the network is lopsided, and when links are specific or
debts concentrated, a local shock travels along the links and grows. Dense links absorb small shocks and spread large
ones.

It opens on 11 March 2011, when an earthquake and tsunami struck north-east Japan. Firms far from the coast, with no
damage at all, stopped work for want of parts; Carvalho, Nirei, Saito and Tahbaz-Salehi traced the loss along
supplier-customer links, upstream and downstream, to about half a point (0.47) of Japan's GDP growth in the year
after. The Island's seventy-firm supply web shows the same in miniature. From there it covers:

- Leontief's paths: the Island's eight-sector input-output table as a network; sales per dollar of GDP (Domar
  weights) as the sum over supply paths, adding to 1.90; services 0.64, retail 0.30, energy 0.25 (a fifth of it sold
  to households directly); upstreamness from retail's 1.1 steps to metals' 3.4;
- Hulten's theorem: a small productivity shock moves GDP by the sector's sales share and nothing else; checked on the
  Island with Cobb-Douglas technologies (energy adds 14% of GDP as value added, sells 25%, and a 10% shock costs 2.5%);
- Play it: which sector's failure costs most when inputs are hard to replace for a year? Services (30% of GDP, against
  Hulten's 27%); energy costs 15.4% against its sales' 11.8%; retail 14.2%; chips 5.9%;
- why shocks do not wash out: with firm shocks of 12%, 10,000 equal firms give GDP a swing of 0.12%, 10,000 Zipf-sized
  firms 1.6%; Gabaix's granular hypothesis (the 100 largest American firms, about a third of the swings); a star of
  sectors against a ring (Acemoglu, Carvalho, Ozdaglar and Tahbaz-Salehi);
- beyond Hulten: GDP's response to energy shocks of every size by the elasticity of substitution; with complements a
  70-log-point loss costs 27 log points of GDP rather than 17.5, energy's sales share climbing from 0.25 to 0.60; the
  oil embargo of 1973; Baqaee and Farhi;
- supply chains, measured: the Island's 3,000 firms, 5% of them losing 40% of output; direct customers lose 7.4%,
  suppliers 17%; 2.0% of sales lost at the hit firms, 7.7% with the links; specific inputs carry the loss (17% against
  4.4% if every input could be replaced); Barrot and Sauvagnat; Boehm, Flaaen and Pandalai-Nayar; Thailand's floods and
  the chip shortage;
- the O-ring (Kremer): one weak link costs two fifths of a team's output; sorting the best with the best adds 11%;
  wages convex in skill; the Challenger;
- an intermission: Japan's industrial production month by month since 2000 (-15.8% in March 2011, the largest monthly
  fall in the window), with each quarter's growth as a tune;
- financial networks: a four-bank clearing vector (Eisenberg and Noe); ten banks in a ring against a complete network,
  robust yet fragile (Acemoglu, Ozdaglar and Tahbaz-Salehi); Lehman and AIG, clearing houses (Elliott, Golub and
  Jackson);
- the strength of weak ties: Granovetter's job-finders (17% saw the contact often, 56% occasionally, 28% rarely); two
  forces and an inverted U; *Called it?*: right (Rajkumar et al.'s LinkedIn experiments);
- diffusion: seeding the Island's village of 200 households at the most central (86% informed after eight rounds), at
  random (63%) or at the least central (15%); microfinance in 43 villages of Karnataka (Banerjee, Chandrasekhar, Duflo
  and Jackson);
- games on networks: the key player (Ballester, Calvó-Armengol and Zenou) is the clique member who bridges to the hub
  (50% of total effort) rather than the hub with most links (36%); the reflection problem and how networks identify
  peer effects (Manski; Bramoullé, Djebbari and Fortin);
- network formation (Jackson and Wolinsky): the complete network, the star and the empty network by link cost; the
  efficient star is unstable when links cost more than delta;
- the Dials (how much of the cycle comes from firms' own shocks, new; how easily firms swap inputs within a year,
  new), the jobs that use this economics, and the frontier: supply networks fragile by design (Elliott, Golub and
  Leduc), networks that rewire, resilience against efficiency.

## Build it

```bash
python -m videos.economics.econ63.compute              # every number (under a minute), into .cache/econ63/
python tools/qa_scene.py econ63 Chains                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ63 -q l   # the whole part, silent preview
python tools/build.py econ63                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 63                     # the lab
```

The data are Japan's industrial production from the OECD's Main Economic Indicators via FRED (JPNPROINDMISMEI),
registered in [`SOURCES.md`](../../../explainer/economics/data/SOURCES.md). Everything else is computed on the Island,
or stated from the papers listed in `dials.SHOWN[63]`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A supplier's supplier | The 2011 earthquake; the Island's supply web and a shock along its links; the question; objectives |
| 1 | Leontief's paths | The input-output table as a network; Domar weights as sums over paths; upstreamness |
| 2 | Hulten's theorem | Sales, not links or value added; checked on the Island; why |
| 3 | Play it: which failure costs most? | Four sectors, inputs hard to replace; sales first, an upstream premium |
| 4 | Why shocks do not wash out | Equal against Zipf-sized firms; Gabaix; a star against a ring |
| 5 | Beyond Hulten: large shocks | Response curves by elasticity; the moving sales share; 1973 |
| 6 | Supply chains, measured | The Island's quake by distance; specific inputs; Japan, America, since |
| 7 | The O-ring | One weak link; sorting; convex wages |
| — | Intermission | Japan's industrial production since 2000, as a line and a tune |
| 8 | Financial networks | A clearing vector by hand; ring against complete; what regulators took from it |
| 9 | The strength of weak ties | Granovetter's survey; two forces; *Called it?* |
| 10 | Diffusion: who to tell first | A village seeded three ways; microfinance in Karnataka |
| 11 | Games on networks: the key player | Bonacich effort; removing the bridge; the reflection problem |
| 12 | Network formation | Efficient against pairwise stable networks by link cost |
| 13 | The Dials | Firms' own shocks in the cycle (new); input substitution within a year (new) |
| 14 | In practice | Supply-chain risk, systemic risk, seeding, planning; three cautions |
| 15 | Frontier | Fragile by design; networks that rewire; resilience against efficiency |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 64, *Machines that Learn* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `network` module (`explainer.economics.agora.network`);
the narration states the cached numbers.

- **The Island's table.** Eight sectors with planted input shares (rows buyers, columns suppliers; labour the rest)
  and consumption shares; Domar weights beta' (I - Omega)^(-1), their path-by-path partial sums, and upstreamness.
- **Hulten and the Play-it.** Unit-cost prices with the wage as numeraire under CES technologies (elasticity theta
  between labour and every input, shares at the baseline), solved as a fixed point; real GDP as minus the log of the
  consumption price index. Hulten's check: Cobb-Douglas, a 10% fall in each sector's productivity. Play it: theta =
  0.15, a fall of 0.5 log points (about two fifths). The response curves: energy's productivity from -0.7 to +0.3 log
  points for theta = 0.15, 0.5, 1 and 1.5.
- **Granularity.** Independent firm shocks of 12%; equal firms against Zipf sizes (s_i proportional to 1/i), 10 to
  10,000 firms; forty simulated years with 1,000 firms; stars and rings of 5 to 500 sectors, each buying half its costs
  from its supplier, equal consumption shares.
- **The quake.** 3,000 firms in five tiers of 600; each above the first buys from three in the tier below with
  Dirichlet(2) cost weights, 40% of links specific; 5% of firms keep 60% of their output; a customer makes up 95% of a
  generic input's shortfall and 25% of a specific one's, and combines inputs with elasticity 0.2; suppliers sell what
  their customers buy. Comparisons: elasticity 1, and every input replaceable.
- **The O-ring.** 400 workers with q from Beta(8, 1.5), clipped to [0.4, 0.999]; teams of four sorted against drawn at
  random; wages proportional to q^4.
- **Banks.** The four-bank example; ten banks each owing 10, in a ring or spread evenly, outside assets 11, a loss at
  one bank from 0 to 20; the Eisenberg-Noe clearing vector by iteration from full payment.
- **Weak ties.** The chance a contact knows of a job you do not, 0.8 e^(-2.5 s), and the chance they pass it on,
  0.15 + 0.85 s, for tie strength s.
- **Diffusion.** 200 households on a ring, each linked to its six nearest with 8% rewired, plus six households linked
  to 18 others; five seeds; each round each informed household tells each contact with chance 0.12; 300 runs a rule.
- **The key player.** A hub with seven followers, a clique of five, one bridge; effort (I - 0.2 G)^(-1) 1.
- **Formation.** Four players, delta = 0.6, every network enumerated for link costs 0.05 to 1.2; pairwise stability.
- **Fragility.** Four essential inputs, 2, 3 or 5 potential suppliers of each; the largest fixed point of
  rho = (1 - (1 - r rho)^n)^m.
- **The Dials' Island rows.** Gabaix's granular residual on 1,000 Zipf firms (firm shocks 10%, an aggregate shock of
  2.4%, 40 years, 400 histories; planted share 0.34); the elasticity of substitution from thirty years of the Island's
  cost shares (productivity shocks of 5%, shares measured with 3% noise, pair fixed effects; planted 0.15).
- **The intermission.** JPNPROINDMISMEI monthly, January 2000 to March 2024; each quarter's growth of the quarterly
  average as the tune.

## Problems and solutions

**1.** *Leontief: with input shares Omega and consumption shares beta, show that sales over GDP are
lambda' = beta' (I - Omega)^(-1), and that the weights add to at least one, with equality only without intermediate
inputs.*

*Solution.* With zero profits a sector's costs equal its sales, so sector j spends Omega_ji S_j on sector i's output.
Sector i's sales are what households buy plus what other sectors buy: S_i = beta_i Y + sum_j Omega_ji S_j, or
S' = Y beta' + S' Omega. Dividing by GDP Y and solving, lambda' = beta' (I - Omega)^(-1) = beta' (I + Omega + Omega^2
+ ...). The weights add to lambda' 1 = 1 + beta' Omega 1 + beta' Omega^2 1 + ..., and every term after the first is
non-negative; they are all zero only if no sector that households buy from (or that sells to one) buys intermediate
inputs.

**2.** *Hulten: in a competitive economy with Cobb-Douglas technologies, show that d log Y / d log A_i = lambda_i,
whatever the network.*

*Solution.* With the wage as numeraire, sector i's unit cost is log p_i = -log A_i + sum_j Omega_ij log p_j, so
log p = -(I - Omega)^(-1) log A. With Cobb-Douglas consumption, real GDP (the real wage bill, labour fixed) is
log Y = -beta' log p = beta' (I - Omega)^(-1) log A = lambda' log A. So the derivative with respect to log A_i is
lambda_i exactly; the network enters only through lambda, that is through sales.

**3.** *Granularity: with Zipf sizes s_i proportional to 1/i, show that the square root of the sum of squared shares
falls like 1/log n, not 1/sqrt(n).*

*Solution.* The shares are s_i = (1/i)/H_n with H_n = 1 + 1/2 + ... + 1/n, about ln n + 0.58. The sum of squares is
(1 + 1/4 + 1/9 + ...)/H_n^2, and the numerator tends to pi^2/6, about 1.64. So the square root is about 1.28/ln n:
it halves only when n is squared. With equal firms it is 1/sqrt(n), which halves when n is quadrupled.

**4.** *Clearing: three banks in a ring each owe the next 10 and hold nothing else; show that every (p, p, p) with
0 <= p <= 10 clears, and say which one Eisenberg and Noe's algorithm picks, and why.*

*Solution.* Bank i pays min(10, what it receives), and receives what bank i - 1 pays: p_i = min(10, p_(i-1)). Any
equal vector with p between 0 and 10 satisfies all three equations, so there is a continuum of clearing vectors, from
everyone defaulting completely to everyone paying in full. The algorithm starts from full payment and lowers payments
only when a bank cannot pay, so it stops at once at (10, 10, 10): the greatest clearing vector, in which the circle of
debts simply cancels. It matters because a supervisor who assumed the worst fixed point would see a crisis that
netting the debts removes; a clearing house that nets multilateral positions delivers the greatest one.

**5.** *Key player: for a star of one hub and k leaves with x = (I - delta G)^(-1) 1, compute the hub's effort and the
loss from removing it.*

*Solution.* By symmetry each leaf's effort is x_l = 1 + delta x_h and the hub's is x_h = 1 + delta k x_l. Substituting,
x_h = (1 + delta k)/(1 - delta^2 k) and x_l = (1 + delta)/(1 - delta^2 k), which needs delta^2 k < 1. Total effort is
x_h + k x_l = (1 + k + 2 delta k)/(1 - delta^2 k). Without the hub the leaves are isolated and each puts in 1, so the
loss is (1 + k + 2 delta k)/(1 - delta^2 k) - k, which grows quickly as delta^2 k approaches one.

**6.** *Jackson and Wolinsky: for n players, show that the star is efficient for delta - delta^2 < c <
delta + (n - 2) delta^2 / 2, and pairwise stable only for c < delta.*

*Solution.* Any network that connects everyone with fewer than n(n - 1)/2 links has some pairs at distance two or
more; among connected networks with n - 1 links (the fewest), the star puts every pair within two steps, so its total,
2(n - 1)(delta - c) + (n - 1)(n - 2) delta^2, beats every other tree. Adding a link between two leaves raises the total
by 2(delta - delta^2) - 2c, which is negative when c > delta - delta^2, so the star beats denser networks there, and
the complete network wins below. The star beats the empty network when its total is positive, which with the formula
above gives c < delta + (n - 2) delta^2 / 2. For stability: a leaf that cut its link would lose delta + (n - 2)
delta^2 > c, so leaves keep their links; two leaves adding a link each gain delta - delta^2 < c, so they do not; and
the hub, cutting a link, saves c and loses delta (the leaf is then isolated), so it keeps it only if c < delta. For
delta < c < delta + (n - 2) delta^2 / 2 the efficient star is not stable.

## Lab and interactive

- `python -m videos.economics.labs 63`: Domar weights and paths; Hulten checked; the failure ranking with complements;
  granular volatility; the quake by distance; the O-ring; clearing and contagion; diffusion by seeding; the key player;
  network formation; fragility; the Dials' Island estimates; Japan's March 2011 on the FRED data.
- The interactive (course site): network. The reader chooses which Island sector to hit, how hard, and how easily
  firms can substitute inputs, and compares the loss of GDP with Hulten's rule.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[63]`; the new Dials (how much of the cycle
comes from firms' and sectors' own shocks; how easily firms swap inputs within a year) are in
`explainer/economics/dials.py`, and the *Called it?* record of the strength of weak ties in
`explainer/economics/calls.py`. The methods are stated from the works cited in the chapters (Leontief 1936, Domar 1961,
Granovetter 1973, Lucas 1977, Hulten 1978, Kremer 1993, Manski 1993, Jackson and Wolinsky 1996, Eisenberg and Noe 2001,
Ballester, Calvó-Armengol and Zenou 2006, Bramoullé, Djebbari and Fortin 2009, Gabaix 2011, Foerster, Sarte and Watson
2011, Acemoglu et al. 2012 and 2015, Antràs et al. 2012, Banerjee et al. 2013, Elliott, Golub and Jackson 2014, Barrot
and Sauvagnat 2016, Atalay 2017, Oberfield 2018, Baqaee and Farhi 2019, Boehm, Flaaen and Pandalai-Nayar 2019, Acemoglu
and Azar 2020, Carvalho, Nirei, Saito and Tahbaz-Salehi 2021, Elliott, Golub and Leduc 2022, Rajkumar et al. 2022) and
computed here.
