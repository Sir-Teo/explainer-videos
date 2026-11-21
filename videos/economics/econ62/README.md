# Economics, Built: Part 62, Inside the Firm

Part 62 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth of Act XI, *Economics at Work*. It asks why some firms are so much better
run than others, and whether it can be taught. Its answer: partly because competition lets the laggards live, and
partly because management, which can be measured, causes productivity: cheap practices raised it by a sixth in a year
when they were taught. Owners had not adopted them because they did not know, had no time, and faced no pressure; and
practices that rest on trust are hard to copy. Inside the firm, how people are paid, promoted, financed and watched
shapes what they do. Much of it can be taught, but not all of it can be bought.

It opens in 2008 near Mumbai, where Bloom, Eifert, Mahajan, McKenzie and Roberts gave free management consulting to a
randomly chosen group of large textile plants: within a year the treated plants' productivity was 17% higher, from
better quality, more efficient production and less inventory, and within three years the treated firms opened more
plants; the practices had been free to adopt all along. The Island has weaving plants too. From there it covers:

- productivity dispersion: on the Island, survivors' 90/10 productivity ratio is 1.93 when buyers switch moderately
  easily, 2.76 when they hardly switch and 1.36 when they switch very easily (entrants: 3.1); Syverson's 1.92 within
  narrow American manufacturing industries; ready-mixed concrete;
- measuring management: Bloom and Van Reenen's eighteen practices scored 1 to 5; on the Island's 1,500 firms, 0.23 log
  points of productivity per point of score, and scores by owner (multinationals and dispersed shareholders highest,
  family firms with a family chief executive and government firms lowest);
- Play it: four practices for one plant over three years (recording and acting on defects returns 4.6 per dollar,
  cutting inventory 3.0, pay for performance 0.2, a faster loom loses money);
- the experiment: 28 Island plants in 17 firms, consulting randomized by firm (this run +21%, give or take 7; over 400
  reruns centred on +17% with a spread of 3 points); why owners had not adopted the practices (information, time,
  competition); Bruhn, Karlan and Schoar's Mexican firms;
- personnel economics: a switch to piece rates raises output per worker 20% from the same workers and 39% after
  turnover, about half from sorting; Lazear's Safelite (+44%); promoting the best seller against the best manager (the
  best manager's team sells about 10% more); *Called it?*: the Peter principle (partly right; Benson, Li and Shue);
- executive pay: Gabaix and Landier's assignment model (pay rises with firm size to the power one third; six-fold
  larger firms, six-fold pay, as from 1980 to 2003); pay for luck under weak boards (Bertrand and Mullainathan);
- capital structure: the trade-off theory (the Island's firm is worth most at about 55% debt, 9.8% more than with none),
  the pecking order (Myers and Majluf), and what 392 chief financial officers say (Graham and Harvey);
- an intermission: output per hour in American business since 1947, with its eras of fast and slow growth;
- agency and governance: Jensen and Meckling's owner-manager (perks rise from 2 to 29 as the manager's share falls
  from all to a tenth); boards, activists, and family successions (Bennedsen et al.: at least four points of
  operating profitability);
- private equity: Island buyouts (jobs at the old establishments -2.3% in two years and -5.1% in five, new
  establishments opened, productivity up); Davis et al.'s -3% and -6%;
- hierarchies of knowledge (Garicano): cheaper communication centralizes, cheaper knowledge decentralizes (Bloom,
  Garicano, Sadun and Van Reenen);
- working from home, randomized: the Island's call centre (+15% calls, quits 13% against 38%); Ctrip (+13%) and
  Trip.com's hybrid trial (quits down by a third, no change in reviews or promotions);
- culture and relational contracts (Part 14's model; NUMMI; Gibbons and Henderson);
- mergers that destroy value: the Island's diversification discount (-12.6%, of which -5.9 points were there before),
  Berger and Ofek's 13-15%, acquirers' $240 billion loss in 1998-2001, DaimlerChrysler;
- the Dials (what better management adds, new; a chief executive's wealth against the shareholders', new), the jobs
  that use this economics, and the frontier: generative AI at work (Brynjolfsson, Li and Raymond) and firms of people
  and models.

## Build it

```bash
python -m videos.economics.econ62.compute              # every number (under a minute), into .cache/econ62/
python tools/qa_scene.py econ62 Experiment             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ62 -q l   # the whole part, silent preview
python tools/build.py econ62                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 62                     # the lab
```

The data are FRED's output per hour in the nonfarm business sector (OPHNFB, from the BLS), registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md). Everything else is computed on the Island, or stated
from the papers listed in `dials.SHOWN[62]`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Clean floors | The Mumbai experiment; an Island plant floor before and after; the question; objectives |
| 1 | Productivity dispersion | Survivors' 90/10 ratio; competition and the laggards; Syverson |
| 2 | Measuring management | Eighteen practices scored; the Island's scores by owner |
| 3 | Play it: four practices and a budget | Value per dollar over three years |
| 4 | The experiment, and why they had not done it | The Island's 28 plants; information, time, competition; Mexico |
| 5 | Personnel economics | Piece rates, effort and sorting; the Peter principle; *Called it?* |
| 6 | Executive pay | Talent assigned to firm size; pay for luck |
| 7 | Capital structure | The trade-off; the pecking order; what CFOs say |
| — | Intermission | Output per hour in American business since 1947, as a line and a tune |
| 8 | Agency and governance | The owner-manager's perks; boards, activists, family successions |
| 9 | Private equity | Buyouts against matched firms; the debate |
| 10 | Hierarchies of knowledge | Garicano's teams; communication against information technology |
| 11 | Working from home, randomized | The Island's trial; Ctrip and Trip.com |
| 12 | Culture and relational contracts | Self-enforcing effort; why practices do not travel |
| 13 | Mergers that destroy value | The diversification discount and selection; acquirers' losses |
| 14 | The Dials | Management's effect (new); CEO pay-performance sensitivity (new) |
| 15 | In practice | Strategy, corporate finance, people analytics; three cautions |
| 16 | Frontier | Generative AI at work; firms of people and models |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 63, *The Economy as a Network* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `org` module (`explainer.economics.agora.org`) and Part
14's `contracts.relational`; the narration states the cached numbers.

- **Dispersion.** 4,000 entrants with log productivity N(0, 0.45); CES demand of elasticity 2 to 10 with total revenue
  4,000 and a fixed cost of 0.25; plants with negative profit exit until none would.
- **Management.** 1,500 firms in seven ownership groups with planted mean scores; 18 practices scored 1 to 5 with
  noise; log productivity rises 0.25 per point of the score, plus noise (s.d. 0.35).
- **Practices.** A plant with revenue $8 million, value added at the margin 25%, inventory $1.5 million carried at
  12%; each practice's cost, effect and chance of working planted; 20,000 draws over three years.
- **The experiment.** 17 firms (11 with two plants), 11 treated at random; weekly log productivity with plant effects,
  common shocks, persistent post-period shifts (s.d. 0.08) and noise (s.d. 0.08); a 17% effect phased in over 30
  weeks; difference in differences over the following year with firm-clustered errors; 400 runs.
- **Piece rates.** Ability log-normal (median 1, log-s.d. 0.3); outside options 11 a^0.6 plus noise; a $11 wage; a
  piece rate of 11 a unit with the wage guaranteed; effort cost 30 (e - 1)^2/2; 40% turnover.
- **The Peter principle.** 400 teams of 8; selling and managing skills standard normal with correlation 0.2; team
  sales 1 + 0.1 x the others' selling skill + 0.08 x the manager's managing skill.
- **CEO pay.** Gabaix and Landier with Zipf firm sizes (alpha = 1), beta = 2/3, gamma = 1. Pay for luck: 3,000 firms,
  skill and luck standard normal, half with weak boards paying 0.5 x results, half paying 0.5 x skill.
- **Capital structure.** Value 100 unlevered, a 21% tax shield, log-normal value next year with volatility 35%, and
  60% of value lost in default.
- **Agency.** Perks P = k/alpha - 1 with k = 3 on a firm worth 100.
- **Buyouts.** 300 targets and 1,200 controls with 3 to 11 establishments; targets close their least productive
  establishments faster and open more new ones.
- **Hierarchies.** Garicano's team with problems Exp(1), optimized over the knowledge of workers and the manager for
  communication costs 0.6 to 0.1 and knowledge costs 0.08 to 0.03.
- **Working from home.** 250 volunteers, half sent home for 40 weeks; minutes +9%, calls a minute +4%, quits 17.5%
  against 35% planted.
- **Conglomerates.** 2,000 firms, 40% diversified; a true effect of -6% and a pre-existing gap of -8% planted.
- **The intermission.** OPHNFB quarterly, 1947Q1 to 2026Q3; each year's growth of the yearly average, 1948-2025.

## Problems and solutions

**1.** *Dispersion: with CES demand of elasticity sigma, show that a plant's revenue share is proportional to
phi^(sigma - 1), and explain why higher sigma raises the survival cutoff.*

*Solution.* With CES demand a plant's quantity is proportional to its price to the power -sigma, and with constant
markups its price is proportional to 1/phi. Revenue p q is then proportional to p^(1 - sigma), that is to
phi^(sigma - 1). Profit is revenue over sigma less a fixed cost. As sigma rises, the shares concentrate on the most
productive plants (phi^(sigma - 1) is more convex), so the least productive ones earn too little to cover the fixed
cost, and the cutoff rises; survivors are fewer and more alike.

**2.** *Piece rates: with output a e, piece rate r and effort cost c (e - 1)^2/2, find a worker's effort, and the
ability above which they prefer the piece rate to a guaranteed wage w.*

*Solution.* Above the standard the worker maximizes r a e - c (e - 1)^2/2, so e = 1 + r a/c, and earns
r a (1 + r a/c) - (r a)^2/(2c) = r a + (r a)^2/(2c). They prefer this to the guarantee w (at effort 1) when
r a + (r a)^2/(2c) > w; solving the quadratic, when r a > c (sqrt(1 + 2w/c) - 1). Abler workers clear the bar, which
is why the piece rate both raises effort and changes who stays and who joins.

**3.** *Gabaix and Landier: if pay is w(n) proportional to S(n*)^(beta/alpha) S(n)^(gamma - beta/alpha), show that
scaling every firm by lambda scales pay by lambda^gamma.*

*Solution.* Replace every S by lambda S: w becomes lambda^(beta/alpha) lambda^(gamma - beta/alpha) = lambda^gamma
times the old pay. With gamma = 1, pay rises one for one with the size of firms in general, while across firms at a
moment it rises only with own size to the power gamma - beta/alpha, about a third.

**4.** *Jensen and Meckling: maximize alpha (V - P) + k ln(1 + P), and find the agency cost as a function of alpha.*

*Solution.* The first-order condition is -alpha + k/(1 + P) = 0, so P = k/alpha - 1 (when positive). The firm's value
is V - P. A sole owner (alpha = 1) takes k - 1; the agency cost of owning only alpha is the extra perks,
k/alpha - k = k (1 - alpha)/alpha, which grows without bound as the manager's share falls, and outside investors
price it into the shares.

**5.** *Trade-off: with value V_U + tau D - expected distress costs, write the first-order condition for the best debt,
and explain why more volatile firms borrow less.*

*Solution.* The best D sets tau = d/dD [P(default | D) x distress cost], the marginal tax saving equal to the marginal
expected distress cost. For a more volatile firm the probability of default rises faster with D at any level of debt,
so the right side is larger and the condition holds at lower D: riskier firms carry less debt.

**6.** *Garicano: with problems z ~ Exp(1), worker knowledge z_w and helping time h, show that a manager's span is
e^(z_w)/h, and that cheaper communication lowers z_w.*

*Solution.* Each worker passes up the problems harder than z_w, a share e^(-z_w); a manager with one unit of time who
spends h on each can help n = 1/(h e^(-z_w)) = e^(z_w)/h workers. Raising z_w costs knowledge c for every worker and
saves the manager's time; when h falls, help is cheap, so the saving from worker knowledge falls and the optimal z_w
falls: workers know less and pass more up, which is centralization.

## Lab and interactive

- `python -m videos.economics.labs 62`: dispersion by competition; management scores; the four practices; the
  experiment; piece rates; the Peter principle; CEO pay and pay for luck; the trade-off; perks; buyouts; hierarchies;
  working from home; the diversification discount; productivity eras on FRED data.
- The interactive (course site): management. The reader runs the Island's management experiment, choosing how many firms
  to treat, how noisy the plants are and how long to wait, and sees how often the result is found.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[62]`; the new Dials (what better
management adds; how a chief executive's wealth moves with the shareholders') are in `explainer/economics/dials.py`,
and the *Called it?* record of the Peter principle in `explainer/economics/calls.py`. The methods are stated from the
works cited in the chapters (Modigliani and Miller 1958, Jensen and Meckling 1976, Myers and Majluf 1984, Jensen and
Murphy 1990, Berger and Ofek 1995, Hall and Liebman 1998, Garicano 2000, Lazear 2000, Bertrand and Mullainathan 2001,
Graham and Harvey 2001, Syverson 2004 and 2011, Moeller, Schlingemann and Stulz 2005, Bennedsen et al. 2007, Bloom and
Van Reenen 2007, Gabaix and Landier 2008, Gibbons and Henderson 2012, Bloom et al. 2013, Bloom, Garicano, Sadun and
Van Reenen 2014, Davis et al. 2014, Bloom, Liang, Roberts and Ying 2015, Bruhn, Karlan and Schoar 2018, Benson, Li and
Shue 2019, Bloom, Han and Liang 2024, Brynjolfsson, Li and Raymond 2025) and computed here.
