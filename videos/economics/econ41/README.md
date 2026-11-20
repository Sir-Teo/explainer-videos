# Economics, Built: Part 41, Taxes

Part 41 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth of Act VIII, *Work and the State*. It asks who really pays a tax, and how
high the top rate should be. Its answer: whoever cannot escape it, so workers bear much of a tax on mobile capital and
buyers bear the taxes they do not see; and the top rate that raises the most is 1/(1 + ae), about seventy percent if
top incomes respond weakly and forty if they respond strongly, where how strongly they respond depends partly on the
tax law itself.

It opens on Arthur Laffer's napkin of 1974 (the story as Jude Wanniski told it, with the caveat that accounts differ
and the napkin in the Smithsonian may be a later copy). The curve is right; where its top lies is the question. With
taxed income shrinking like (1 - t)^e, the top is at 80% for e = 0.25 and at 50% for e = 1. From there it covers:

- incidence: a 20% tax on capital's return on the Island, with capital's supply elasticity from zero (a closed economy
  with a fixed stock, where workers bear none of it) to infinity (a small open economy, where workers lose 117% of the
  revenue, 17% of it deadweight loss); Germany's municipal business tax (Fuest, Peichl and Siegloch: about 6,800 local
  rate changes, workers bearing about half);
- the deadweight triangle in a market with demand elasticity 0.5 and supply elasticity 1 (buyers bear two thirds of a
  20% tax); the loss as a share of revenue, 1.6% at 10%, 3.3% at 20% and 6.3% at 40%, against Harberger's
  approximation; the marginal cost of public funds along the Laffer curve ($1.07 for the last dollar raised at 20%
  with e = 0.25, $1.20 at 40%, $1.60 at 60%; $1.33 and $3 with e = 1; infinite at the top);
- a game: three numbers set the top rate. America's 2022 top shares give a = 1.56; with e = 0.25 and g = 0 the rate
  that raises the most is 72% (Diamond and Saez, with a = 1.5, 73%); 87%, 72%, 56% and 39% for e = 0.1, 0.25, 0.5 and
  1; 66% if top earners' dollars count a quarter as much as the average;
- Ramsey's rule: the same revenue from bread, clothes and travel (demand elasticities 0.2, 1 and 2) at 25.1%, 4.2% and
  2.0% instead of a uniform 11.2%, with 2.6 times less deadweight loss; Diamond and Mirrlees's production efficiency;
  Atkinson and Stiglitz;
- Mirrlees's problem: the government sees income, not ability; Diamond's three factors (the elasticity, the shape of
  the distribution, the welfare weights above) on the Island;
- the optimal top rate derived from one small reform, (1 - g)/(1 - g + ae);
- the whole schedule: Diamond's U on the Island (68% at the bottom, 55% near the 75th percentile, rising towards 71%
  at the top, where incomes' Pareto parameter is 1.6); the extensive margin, Saez's 2002 result and the Earned Income
  Tax Credit;
- an intermission without narration: America's top statutory rate, 1913-2025, as a tune;
- measuring the elasticity: the top rate against the top 1% share since 1913; the Tax Reform Act of 1986 (the top rate
  50% to 28%, the share kept up 44%, the top 1% share 9.1% to 13.2%: an implied elasticity of about 1.0, much of it
  relabelling and timing); Feldstein's panel (at least one), Gruber and Saez (about 0.4); Saez, Slemrod and Giertz's
  lesson that the elasticity is partly a policy choice;
- bunching at kinks (Saez's estimator on 200,000 Island taxpayers facing a kink from 20% to 40% at 50,000: 0.24
  against 0.25 planted, 0.20 with larger frictions; only the self-employed bunch at the EITC's first kink; Kleven and
  Waseem's notches in Pakistan);
- salience: Chetty, Looney and Kroft's tax-inclusive shelf tags (sales down about 8%, as if the price had risen by the
  7.375% tax);
- taxing capital: a dollar at 5% for forty years (7.04 untaxed, 4.36 with a quarter of the return taxed, 2.69 with
  half: a 62% tax on consumption forty years away); Atkinson and Stiglitz, Chamley and Judd, and Straub and Werning's
  revision;
- corporations and havens: 36% of multinationals' foreign profits booked in havens in 2015 (Tørsløv, Wier and Zucman);
  about 8% of households' financial wealth offshore (Zucman); the 2021 global minimum tax of 15%, agreed by 136 of the
  140 members of the OECD's inclusive framework;
- evasion: Allingham and Sandmo on the Island (a cautious taxpayer declares nothing below a 14% audit rate and
  everything only at 50%); the Danish randomized audits (evasion of 0.3% on third-party-reported income, 37% on
  self-reported income);
- three dials, all new (the elasticity of taxable income; the revenue-maximizing top rate; the share of the corporate
  tax on wages); scoring a tax change (raising the top rate from 37% to 40% keeps 75% of the static gain with e = 0.25
  and almost none with e = 1; cutting it to 30% loses 82% or 24% of the static loss); *Called it?* on the claim that
  the 2017 tax cuts would pay for themselves (wrong); a frontier chapter on migration (European footballers), bargaining
  and behaviour.

## Build it

```bash
python -m videos.economics.econ41.compute              # every number (a few seconds), into .cache/econ41/
python tools/qa_scene.py econ41 TopRate                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ41 -q l   # the whole part, silent preview
python tools/build.py econ41                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 41                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the IRS's top statutory rates and federal receipts and
deficits as shares of GDP, via FRED (`TAX_FRED`); Piketty and Saez's top shares (as in Part 40); and tables from
Laffer and Wanniski, Harberger, Fuest, Peichl and Siegloch, Ramsey, Mirrlees, Diamond and Saez, Feldstein, Gruber and
Saez, Saez, Slemrod and Giertz, Chetty, Looney and Kroft, Zucman, Tørsløv, Wier and Zucman, the OECD, Allingham and
Sandmo, Kleven et al., Kleven, Landais and Saez, and the Congressional Budget Office.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A curve on a napkin | The napkin; where its top lies; the questions; objectives |
| 1 | Who pays the corporate tax? | Incidence from closed to open; Germany's local business tax |
| 2 | The cost of a tax grows with its square | The triangle; Harberger's formula; the cost of the last dollar |
| 3 | Play it: set the top rate from three numbers | The game; the revenue curves by elasticity |
| 4 | Taxing goods: Ramsey's rule | Inverse elasticities; against a uniform rate; Diamond-Mirrlees; Atkinson-Stiglitz |
| 5 | The income tax as an information problem | Mirrlees's problem; Diamond's three factors on the Island |
| 6 | The optimal top rate, derived | One small reform; the algebra |
| 7 | The whole schedule | Diamond's U; the extensive margin and the EITC |
| — | Intermission | The top statutory rate, 1913-2025, as a tune |
| 8 | Measuring the elasticity | A century of rates and shares; the 1986 reform; why the elasticity is a policy choice |
| 9 | Bunching at kinks | Saez's estimator on the Island; frictions; the self-employed; notches |
| 10 | Taxes on the shelf tag | Chetty, Looney and Kroft; what salience changes |
| 11 | Taxing capital | Compounding; Atkinson-Stiglitz, Chamley-Judd and the revision |
| 12 | Corporations and tax havens | Profit shifting; offshore wealth; the global minimum tax |
| 13 | Evasion | Allingham and Sandmo; Denmark's random audits |
| 14 | The Dials | The elasticity; the top rate; who pays the corporate tax |
| 15 | In practice: scoring a tax change | Who does it; static against behavioural scores; *Called it?* (wrong) |
| 16 | Frontier | Migration; bargaining; behaviour |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 42, *Social Insurance* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's tax module (`explainer.economics.agora.tax`), with the
Island's Part 41 truths, or from the Data Room; the narration states the cached numbers.

- **Laffer.** Revenue t (1 - t)^e per unit of untaxed base; the peak at 1/(1 + e). The marginal cost of public funds
  is (1 - t)/(1 - t - te): raising the rate by dt costs taxpayers the base times dt (the envelope theorem) and raises
  the base times (1 - te/(1 - t)) dt.
- **Incidence.** Output K^0.3 L^0.7; firms pay capital its marginal product; a 20% tax on capital's return; capital's
  supply K0 (r_net/r0)^eta, solved in closed form, with eta from 0 to 200 and the small open economy as eta = infinity.
  Workers' loss is the fall in the wage; owners' loss the area under the supply curve between the old and new net
  returns.
- **The triangle.** Constant-elasticity demand (0.5) and supply (1), a unit tax as a share of the untaxed price, the
  exact surplus losses by numerical integration, and Harberger's approximation 1/2 t² (eps_d eps_s/(eps_d + eps_s)) pq.
- **The top rate.** a is the Pareto exponent of 2022 incomes from Piketty and Saez's top 1% and 0.1% shares (as in
  Part 40). The revenue curves assume every top income scales with (1 - t)^e, so the tail keeps its shape and the
  income above the threshold scales with the power ae: revenue t/(a - 1) ((1 - t)/(1 - t0))^(ae), whose peak is
  1/(1 + ae) exactly.
- **Ramsey.** Independent goods with demand p^-eps and unit cost; taxes with t/(1 + t) proportional to 1/eps, scaled to
  raise 0.3; the uniform rate raising the same; consumer-surplus losses in closed form.
- **Diamond's schedule.** Skills lognormal (sigma 0.5) below the 97th percentile and Pareto (exponent 2) above it, the
  density continuous; quasi-linear utility with e = 0.25; welfare weights proportional to 1/skill, averaging one; the
  integrals above each skill include the Pareto tail beyond the grid exactly, so the rate approaches
  1/(1 + ae) with incomes' a = 2/(1 + 0.25) = 1.6.
- **The elasticity.** The IRS's top statutory rate (37% after 2018, where FRED's series ends) against the top 1% share
  excluding capital gains; the 1986 elasticity is the log change of the share over the log change of 1 - t, 1986 to
  1988.
- **Bunching.** 200,000 taxpayers with lognormal ability around 40,000 choosing z = n (1 - t)^e; the marginal rate
  rises from 20% to 40% at 50,000; a 1% multiplicative error (5% in the noisy version, with a window of ±5,000);
  Saez's estimator with a seventh-degree polynomial fitted outside a window of ±2,500 and bins of 500.
- **Evasion.** A 30% tax, a fine equal to the evaded tax, relative risk aversion 2; the declared share maximizes
  expected utility over a grid of 4,001 values.
- **Scoring.** Revenue from the top bracket per taxpayer in it, with the 2022 a, relative to the current 37%; the
  static score holds incomes fixed.

## Problems and solutions

**1.** *Laffer: revenue is t(1 - t)^e. Find the revenue-maximizing rate for e = 0.5, and the revenue lost by setting
the rate 10 points above it.*

*Solution.* The derivative (1 - t)^(e - 1) (1 - t - te) is zero at t = 1/(1 + e) = 1/1.5 = 66.7%, where revenue is
0.667 x 0.333^0.5 = 0.385. At 76.7% it is 0.767 x 0.233^0.5 = 0.370, so 3.8% of the maximum is lost: near the top
the curve is flat, which is why its location is hard to see in the data.

**2.** *Incidence: demand elasticity 0.5, supply elasticity 1. What share of a small tax do buyers bear? And if supply
were perfectly elastic?*

*Solution.* Buyers bear eps_s/(eps_d + eps_s) = 1/1.5 = two thirds, sellers one third: the less elastic side bears
more. With perfectly elastic supply the price sellers receive cannot fall, so buyers bear all of it, as workers bear
all of a capital tax in a small open economy.

**3.** *The triangle: with the same elasticities, use Harberger's formula for the deadweight loss of a 10% and a 30%
tax, per unit of spending.*

*Solution.* The combined elasticity is eps_d eps_s/(eps_d + eps_s) = 0.5/1.5 = 1/3, so the loss is t²/6 of spending:
0.17% at 10% and 1.5% at 30%. Three times the rate, nine times the loss. As a share of the revenue (about t times
spending) it is t/6: 1.7% and 5%.

**4.** *Ramsey: two independent goods with elasticities 0.5 and 2. If the first is taxed at 20%, what does Ramsey's
rule set for the second?*

*Solution.* The rule sets t/(1 + t) proportional to 1/eps. For the first good, 0.2/1.2 = 0.167 = k/0.5, so k = 0.083.
For the second, t/(1 + t) = 0.083/2 = 0.042, so t = 0.042/0.958 = 4.3%.

**5.** *The top rate: a = 1.5. Find the top rate for e = 0.2 and 0.5, with g = 0 and with g = 0.3.*

*Solution.* tau = (1 - g)/(1 - g + ae). With g = 0: 1/1.3 = 76.9% for e = 0.2 and 1/1.75 = 57.1% for e = 0.5. With
g = 0.3: 0.7/1.0 = 70.0% and 0.7/1.45 = 48.3%. The elasticity moves the answer more than the welfare weight does.

**6.** *Bunching: a kink at 50 where the rate rises from 20% to 40%; the excess mass is 3.5 (thousand). What
elasticity does Saez's formula give?*

*Solution.* e = b / (z* ln((1 - t0)/(1 - t1))) = 3.5 / (50 x ln(0.8/0.6)) = 3.5 / (50 x 0.288) = 3.5 / 14.4 = 0.24.

**7.** *Evasion: in Allingham and Sandmo's model with risk neutrality, when is it optimal to declare everything?
(audit probability p, fine theta)*

*Solution.* Each dollar hidden saves the tax t with probability 1 - p and, if audited, costs the tax back plus a fine
theta t, a net loss of theta t against declaring honestly. The expected gain is t ((1 - p) - p theta), so a
risk-neutral taxpayer declares everything when p (1 + theta) >= 1, that is p >= 1/(1 + theta): 50% with theta = 1, and
otherwise declares nothing. Risk aversion makes partial declarations optimal between the two, which is the Island's
curve.

**8.** *Derive the top rate: show that a small increase dtau yields (1 - g)(z_m - z̄) dtau - tau e z_m dtau/(1 - tau)
per top earner, and solve for tau\*.*

*Solution.* Each top earner pays dtau more on income above the threshold, z_m - z̄ on average: the mechanical gain. It
costs them as much, which society values at g per dollar, so the net welfare gain is (1 - g)(z_m - z̄) dtau. Their
incomes fall by dz = e z_m dtau/(1 - tau), since the elasticity is with respect to 1 - tau, and each dollar not
earned loses tau of revenue: tau e z_m dtau/(1 - tau). At the optimum the sum is zero, so tau/(1 - tau) =
(1 - g)(z_m - z̄)/(e z_m) = (1 - g)/(ae) with a = z_m/(z_m - z̄), and tau\* = (1 - g)/(1 - g + ae).

## Lab and interactive

- `python -m videos.economics.labs 41`: the Laffer peak; Harberger's incidence from closed to open; the triangle
  against its approximation; Ramsey against a uniform rate; Diamond's schedule; the top rate from America's top
  shares; bunching; Allingham and Sandmo.
- The interactive (course site): set the top rate. The reader sets a, e and g, and sees the top bracket's revenue
  curve, the revenue-maximizing and optimal rates, the revenue at today's 37% as a share of the most possible, and the
  optimal rate against the elasticity.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[41]`; the three dials are in
`explainer/economics/dials.py`; the 2017 claim is a *Called it?* entry (`explainer/economics/calls.py`). FRED's series
were retrieved on 2026-11-20. The napkin's story is told as Wanniski told it, with the dispute over its details
stated; Fuest, Peichl and Siegloch's share and count, Diamond and Saez's 73%, Chetty, Looney and Kroft's 8% and the
Danish audit figures are from the published papers and their abstracts; Tørsløv, Wier and Zucman's 36% and Zucman's
8% from their papers' abstracts; the global minimum tax from the OECD's statement of October 2021; the footballers'
elasticities from Kleven, Landais and Saez's abstract; Mnuchin's words as reported in September 2017; the CBO's
estimate from its April 2018 outlook.
