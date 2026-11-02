# Quant, Built — Part 8: Decisions and Control

Part 8 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act II, the Mathematical Toolkit. Part 7 forecast how much the market
will move; this part asks how much to bet, and when to stop. It is a lecture of about 55 minutes in nineteen chapters
plus a hook and an outro, built to replace the stochastic-control and portfolio-choice chapters of a graduate course:

* expected utility (the vNM axioms), risk aversion and the Arrow–Pratt premium, derived;
* Bellman's recursion, the HJB equation derived from the DPP and Itô, the verification theorem, and viscosity
  solutions (why monotone schemes converge);
* Merton's problem with consumption, by the HJB and by the martingale method; two-fund separation;
* transaction costs and the Davis–Norman no-trade band, by dynamic programming;
* Kelly and Breiman, proved; fractional Kelly and estimation risk (Thorp, Benter); LTCM; Samuelson's objection and
  the ergodicity debate;
* optimal stopping (the Snell envelope as a least concave majorant) and smooth fit (McKean's perpetual put);
* prospect theory (with Benartzi and Thaler's myopic loss aversion redone on data) and robust control (Maenhout);
* BSDEs with two interest rates, a mean-field liquidation game, and PPO on Merton's problem with and without costs;
* how funds, syndicates and desks size bets, and the 2023–2026 frontier.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`control`](../../../explainer/quant/house/control.py) module, tested against closed forms in
`tests/test_quant_house.py`), from Kenneth French's US market returns (monthly and daily, 1926–2020) and from seeded
simulations, labelled on screen.

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **How much to bet, and how we got here.** Haghani and Dewey (2016) gave 61 people $25 and a 60% coin at even odds;
  about 30% went bust. *Live:* 160 players in each of four columns flip the same coin 300 times on a log-wealth axis
  (all in: 91% bust; 40%: 18% bust, 74% at the cap; 20%: 96% at the cap, none bust). Kelly's curve g(f) with 20,000
  players per fraction (20%: 94% reach $250, none bust; 100%: 87% bust). The history, 1738–2017, as one tree rooted in
  expected utility; objectives; the House.
* **1. Utility and risk aversion.** St Petersburg; the vNM axioms card. *Visual:* the gamble as two weights on the
  utility curve, the chord's balance point dropping to the certainty equivalent (86.6 at log utility); a γ dial bends
  the CRRA curve live and the CE slides (67.1 at γ = 3, 51.2 at 30). Arrow–Pratt derived in five steps; exact against
  ½γσ²/W (13.4 vs 12.5 for ±50 at γ = 1; 32.9 vs 37.5 at γ = 3). Rabin's calibration warning.
* **2. Bellman's principle (Lab 1).** A three-period tree with values flowing back; the CRRA guess makes the policy
  myopic (Mossin, Samuelson). *Lab:* `bellman_merton` on screen, run: 62% at every wealth (Merton 61.7%). *Replay:* the
  floor problem's policy surface built backwards slab by slab in 3D, with the inset hump E[V_{n+1}](π) at w = 1 whose
  peak walks from 25% to 31%. Slices against portfolio insurance: largest gap 0.005.
* **3. The HJB equation and the verification theorem.** The HJB derived (DPP → Itô → h → 0 → FOC → ansatz).
  *Visual:* the Hamiltonian as a parabola in π whose vertex never moves without a floor and slides to 0 near a floor.
  The verification theorem card. *Experiment:* implicit finite differences with policy iteration (400 × 401;
  mostly 3 passes a step): π within 0.002 points of Merton, value within 0.07% of the closed form, error falling
  0.27% → 0.07% as the grid is refined.
* **4. Viscosity solutions.** Kinks from floors, stopping and maxima; |u′| = 1 has infinitely many a.e. solutions.
  *Visual:* test functions touching a peak (passes) and a valley (fails). Comparison, the value function as a
  viscosity solution, Barles–Souganidis. *Experiment:* u_t + |u_x| = 1 marched by upwind (error at rounding level on
  21, 81, 321 nodes) and central differences (error 10^6 to 10^131, worse as the grid is refined).
* **5. Merton's problem.** *Live:* two glasses (Merton rebalancing monthly, buy-and-hold drifting) on a five-year path.
  Over 20,000 thirty-year paths, γ = 3: certainty-equivalent growth 3.86% vs 3.77%; buy-and-hold's final stock share
  ranges from 63% to 95% (10th–90th percentile). Mutual-fund separation. US data: 238% at γ = 1, 79% at γ = 3, with
  ±2 SE from 42% to 116%.
* **6. Consumption, and the martingale method.** Merton (1971) derived: ν = 3.0% (log), 3.57% (γ = 3), 2.90% for a
  more patient investor (ρ = 1%); the finite-life rate rises from 4.7% to everything. Cox–Huang / KLS: X_T = (yξ_T)^{-1/γ},
  a power claim on the stock. *Live:* 2,000 daily-rebalanced investors land on the static curve (largest gap 0.34%).
* **7. Transaction costs (Lab 2).** *Live:* the wealth point diffusing in the Davis–Norman wedge, reflected at its
  edges (35 trades in 15 years; turnover 0.9% a year against 24% for weekly rebalancing). Singular control, the
  variational inequality, the ε^{1/3} asymptotics. *Lab:* `no_trade_band`: at γ = 3, monthly, the band is 59.4–64.0%,
  57.2–66.2%, 55.8–67.8% and 54.0–69.6% for ε = 0.1%, 0.5%, 1% and 2% (half-widths 2.3, 4.5, 6.0, 7.8 points against
  3.0, 5.2, 6.5, 8.2 from the asymptotics). Log utility, 1%, quarterly: band 158–202%, growing 0.29% a year faster
  than quarterly rebalancing to Merton net of costs, with 10% turnover against 44%.
* **8. Kelly and Breiman.** Kelly (1956); Shannon showed Thorp the paper in 1960; Thorp's partnership from 3 November
  1969 compounded at about 20% a year, standard deviation about 6%, through May 1998 (Thorp 2006). Kelly derived for the
  coin and the stock; Breiman's theorem proved by the strong law. *Live:* fans at ½, 1, 2 × Kelly for 40 years with
  the time-average lines (growth 6.2%, 7.6%, 2.0% = the cash rate). Breiman's race: Kelly ahead of 2× Kelly in 70% of
  markets at 10 years and 95% at 100; ahead of ½ Kelly in 60% and 80%. US realized growth: 100% at 9.7%, the best
  218% at 12.6%; 348% ruined by September 1931.
* **9. Fractional Kelly, estimation risk, and LTCM.** (2c − c²) derived; overestimating the edge k-fold: full Kelly earns
  nothing at k = 2, half Kelly at k = 4 (closed form and 2,000 paths); Benter's warning, quoted. *Visual:* the
  bootstrap cloud of best fractions (90% between 116% and 302%) under the US parabola, full vs half Kelly on each
  draw. The registered split-sample test (198% chosen on 1926–1972 grew 13.4% a year afterwards). The LTCM crisis
  file ($129bn of assets on $4.7bn, 28:1, $1.3tn notional; −44% in August 1998; $3.6bn from fourteen firms), and a volatility slider: Kelly leverage 100 → 11 as volatility triples; 28:1 becomes 2.5 × Kelly.
* **10. Samuelson's objection, and ergodicity.** Kelly ends richer than the γ = 3 Merton investor 64%/87% of the time
  at 10/100 years, yet its CE growth is −3.6% vs +3.9% a year; the CE growth rate derived. *Live:* Peters' coin, the
  histogram of 100,000 players flipping 60 times, with the mean running right and the median left; 82% lose money.
  Peters (2019), Meder et al. (2021), Doctor–Wakker–Wang (2020), Toda (2023). Kelly stakes 25% (+0.62% a flip).
* **11. Optimal stopping: the Snell envelope (Lab 3).** Snell's recursion, supermartingale, optional sampling, and the
  least concave majorant for a random walk. *Replay:* value iteration as a rope pulled taut over 21 pegs (226 sweeps).
  *Lab:* `snell_envelope` against `concave_majorant`: agreement to 5 × 10^-14. The secretary problem (37 → 37.1%).
* **12. Free boundaries: smooth fit.** McKean's perpetual put derived: β = 1.11, b* = 52.6, V(100) = 23.21. *Visual:* an
  exercise-level slider with the slope-gap readout closing at b*; a 40-year CRR tree gives 52.5 and 23.01. Rates up
  to 7%: b* = 60.9. The one-year put's boundary (9.87 vs 9.35) and the variational inequality.
* **13. Prospect theory and ambiguity.** Allais; CPT (TK 1992). *Experiment (registered):* Benartzi–Thaler redone on
  French 1926–2020: stocks' CPT value overtakes bills' at an 18-month evaluation period. Ellsberg, Gilboa–Schmeidler,
  Hansen–Sargent; Maenhout's robust Merton derived. *Visual:* investor and nature's best replies crossing; with θ set
  by detection error on 94 years of data, 20% → θ = 1.9, π = 48%; 10% → θ = 4.4, π = 32%; no doubt 79%.
* **14. Backward SDEs.** Definition, the linear case = Black–Scholes, Bergman's two-rate driver, the comparison
  theorem, Gobet–Lemor–Warin. *Replay:* regression clouds stepping backwards over 20,000 paths to Y0 = 1.219, above
  both Black–Scholes prices (1.050 at 1%, 0.605 at 6%); convergence to the PDE's 1.230.
* **15. Mean-field games (Lab 4).** The liquidation game derived: 2ηQ″ + κ(N−1)/N Q′ − 2φQ = 0. *Replay:* fictitious
  play, plan backwards and crowd forwards, settling on the equilibrium. *Lab:* `mfg_liquidation`: residual below
  10^-12 in 48 rounds; share sold in the first fifth (κT/2η = 2): 20% alone, 28.7% (N = 2), 36.2% (N = 10), 38.1%
  (mean field), matching the closed form to 10^-7. A crowd of 500 traders with different blocks.
* **16. Reinforcement learning (Lab 5).** The MDP, policy gradient, one-step advantages, the PPO clip. *Lab:* the core
  of `ppo_merton`; five seeds end at 169–184% against the quarterly optimum of 184%, giving up at most 0.04% a year.
  *Replay:* `TrainingReplay` of the five seeds with the policy map. *Costs:* `ppo_rebalance` (ε = 1%, five seeds) does
  not find the band: it trades part of the way, leaving a strip of about 5 points alone; net growth 7.27–7.33% a year
  against 7.42% for the DP band and 7.13% for quarterly rebalancing to Merton (all on the same 200,000 markets).
* **17. Who sizes bets for a living.** Thorp's 1994 sports test ($50,000 → $123,000 profit in 101 days); Benter's
  fractional Kelly; Berlekamp and Axcom (Medallion's sizing is not public); NBIM's 1.25-point tracking-error limit;
  Bridgewater's All Weather; Millennium's drawdown rules as reported by the WSJ (via Business Insider, 2024).
  *Experiments:* Grossman–Zhou at α = 0.8 vs Kelly (worst drawdown 17% vs 99%; median growth 3.6% vs 7.4%); volatility
  targeting on French daily data (registered): Sharpe 0.51 vs 0.44, alpha 3.5% a year (t = 2.9), exposure 0.01–10.5.
  Almgren–Chriss and Almgren et al. (2005); Haghani and White (2023).
* **18. The frontier, 2023–2026.** A graph of the part's chapters with each paper lighting the edge it builds (list
  below).
* **19. The sizing module.** The new House functions; the sizing pipeline (Kelly 238% → half 119%; the robust fraction at a 20% detection error, 145%, is not smaller; the
  band; the drawdown floor; recompute on volatility); Rule 9 extended. The trial counter reads 82 (this part
  registered three tests).
* **Recap, desk questions, problems.**

## Hands-on

| Kind | Where | What |
|---|---|---|
| Lab 1 | ch 2 | `bellman_merton`: Merton by dynamic programming |
| Lab 2 | ch 7 | `no_trade_band`: the Davis–Norman band by DP |
| Lab 3 | ch 11 | `snell_envelope` against `concave_majorant` |
| Lab 4 | ch 15 | `mfg_liquidation`: fictitious play |
| Lab 5 | ch 16 | the core of `ppo_merton` |
| Replays | ch 2, 11, 14, 15, 16 | backward slabs; the rope; regression clouds; fictitious play; PPO (5 seeds, `TrainingReplay`) |
| Live simulations | hook, ch 5, 6, 7, 8, 10, 17 | coin columns; rebalancing glasses; martingale scatter; the wedge; Kelly fans; Peters' histogram; drawdown floor |
| 3D | ch 2 | the policy surface built backwards |

## Textbook audit

| Book · section | Chapter |
|---|---|
| Pham (2009) ch 1, stochastic analysis | Part 5 |
| Pham ch 2, control problems and financial examples | 2, 3 |
| Pham ch 3, DPP, HJB, verification, Merton, investment–consumption | 2, 3, 5, 6 |
| Pham ch 4, viscosity solutions (definition, comparison) | 4 (superreplication under constraints: Part 9) |
| Pham ch 5, optimal switching and stopping, free boundary, smooth fit | 11, 12 (switching: not covered) |
| Pham ch 6, BSDEs and control; reflected BSDEs | 14 (reflected: named in 12, 14) |
| Pham ch 7, martingale and convex-duality methods | 6 (duality in incomplete markets: Kramkov–Schachermayer, reading only) |
| Touzi (2013), control and DP; optimal stopping; verification examples | 2, 3, 11 |
| Touzi, viscosity solutions and the DPE in the viscosity sense | 4 |
| Touzi, stochastic target problems | Part 9 (superhedging) |
| Touzi, BSDEs; quadratic BSDEs; probabilistic numerics | 14 (quadratic BSDEs: not covered) |
| Touzi, finite differences | 3, 4; Part 16 |
| Karatzas–Shreve, *Methods*, ch 1 (the Brownian market) | Part 9 |
| Karatzas–Shreve, *Methods*, ch 3 (single-agent consumption/investment, martingale method) | 6 |
| Karatzas–Shreve, *Methods*, ch 4 (equilibrium) | Part 23 |
| Karatzas–Shreve, *Methods*, ch 6 (constrained consumption/investment) | 2 (floor), 6 (note) |
| Karatzas–Shreve, *Brownian Motion and Stochastic Calculus*, optional sampling | 11 |
| Björk, *Arbitrage Theory in Continuous Time*: stochastic optimal control, the martingale approach to optimal investment, optimal stopping | 3, 5, 6, 11 (the linear regulator: 15) |
| Merton, *Continuous-Time Finance*, the 1969 and 1971 papers | 5, 6 |
| Øksendal, optimal stopping; stochastic control | 11, 12; 2, 3 |
| Bertsekas, *Dynamic Programming and Optimal Control* I: the DP algorithm, dynamic portfolio analysis, optimal stopping, approximate DP | 2, 11, 16 |
| Sutton–Barto (2nd ed.) ch 3 MDPs, 4 DP, 6 TD, 13 policy gradient | 2, 16 (*AI, Built* Part 26 in full) |
| Back, *Asset Pricing and Portfolio Choice Theory*, ch 1 utility, ch 2 portfolio choice, dynamic programming, ch 14 continuous time | 1, 5, 2, 3, 6 |
| Carmona–Delarue vol. I, MFG by examples; MFG and FBSDEs | 15 (McKean–Vlasov control: reading only) |
| Shreve II ch 8, American derivatives | 11, 12 (pricing: Parts 10, 16) |
| Kahneman–Tversky; Wakker, *Prospect Theory* (rank dependence) | 13 |

## Papers

On screen, with what each found: von Neumann–Morgenstern (1944); Allais (1953); Snell (1952); Kelly (1956); Bellman
(1957); Breiman (1961); Ellsberg (1961); Dynkin (1963); Pratt (1964); Arrow (1965); McKean (1965); Merton (1969, 1971,
1980); Mossin (1968); Samuelson (1969, 1979); Magill and Constantinides (1976); Kahneman and Tversky (1979); Tversky and
Kahneman (1992); Crandall and Lions (1983); Karatzas, Lehoczky and Shreve (1987); Cox and Huang (1989); Gilboa and
Schmeidler (1989); Davis and Norman (1990); Pardoux and Peng (1990); Barles and Souganidis (1991); Grossman and Zhou
(1993); Shreve and Soner (1994); Benter (1994); Benartzi and Thaler (1995); Bergman (1995); El Karoui, Peng and Quenez
(1997); Rabin (2000); Hansen and Sargent (2001); Almgren and Chriss (2001); Anderson, Hansen and Sargent (2003);
Janeček and Shreve (2004); Rogers (2004); Maenhout (2004); Gobet, Lemor and Warin (2005); Almgren, Thum, Hauptmann and
Li (2005); Huang, Malhamé and Caines (2006); Thorp (2006); Lasry and Lions (2007); Carlin, Lobo and Viswanathan (2007);
Haghani and Dewey (2016); Schulman et al. (2017); Moreira and Muir (2017); Cardaliaguet and Lehalle (2018); Han,
Jentzen and E (2018); Lacker and Zariphopoulou (2019); Peters (2019); Doctor, Wakker and Wang (2020); Meder et al.
(2021); Haghani and White (2023).

Frontier (checked at the source, November 2026): Jia and Zhou (2023), "q-Learning in Continuous Time," *JMLR* 24(161);
Dai, Dong, Jia and Zhou, "Data-Driven Merton's Strategies via Policy Randomization," arXiv 2312.11797 (2023, revised
2026); Dai, Dong, Jia and Zhou (2026), "Merton's Problem with Recursive Perturbed Utility," arXiv 2602.13544; Huh,
Jeon, Koo and Lim (2025), "Breaking the Dimensional Barrier for Constrained Dynamic Portfolio Choice," arXiv
2501.12600; Huh and Koo (2026), "Breaking the Dimensional Barrier: Dynamic Portfolio Choice with Parameter Uncertainty
via Pontryagin Projection," arXiv 2601.03175; Laurière et al., "Learning in Mean Field Games: A Survey," arXiv
2205.12944; Chee, Frikha and Li (2026), "A Monotone Limit Approach to Entropy-Regularized American Options," arXiv
2602.18062; Toda (2023), "'Ergodicity Economics' is Pseudoscience," arXiv 2306.03275. Background: Wang, Zariphopoulou
and Zhou (2020), *JMLR* (exploratory control).

Reading only: Kramkov and Schachermayer (1999) on duality in incomplete markets; Fleming and Soner (2006) for
viscosity solutions in control; Crandall, Ishii and Lions (1992), the user's guide; MacLean, Thorp and Ziemba (2011),
the Kelly anthology; Peters and Gell-Mann (2016).

## Build it

```bash
python -m videos.quant.quant8.compute                    # every number, cached in .cache/quant8/ (about an hour of
                                                         # CPU, most of it the ten PPO runs; each item resumable)
EXPLAINER_TTS=silent python tools/qa_scene.py quant8 Costs    # one chapter, silent, with a contact sheet
python tools/make.py quant8 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

The PPO seeds are separate items (`ppo`, `ppo_s1` … `ppo_s4`, `ppo_cost_s0` … `ppo_cost_s4`) so they can run in
parallel processes; `ppo_seeds` and `ppo_costs` collect them.

## Desk questions, with solutions

1. **A 60% coin at even odds.** Maximize g(f) = 0.6 log(1 + f) + 0.4 log(1 − f): g′(f) = 0.6/(1 + f) − 0.4/(1 − f) = 0
   gives f* = 0.2, and g(0.2) = 0.6 log 1.2 + 0.4 log 0.8 ≈ 2.0% a flip. g(0.4) ≈ −0.2%: twice Kelly no longer
   grows. With a cap and a time limit the target is reaching the cap, not long-run growth, so slightly less than Kelly
   does as well. In 300 flips with a $250 cap, 10% and 20% both reach it about 94% of the time.
2. **Sharpe 1 at 10% volatility.** f* = (μ − r)/σ² = SR/σ = 10, and Kelly's excess growth is SR²/2 = 50% a year on
   paper. But a Sharpe ratio measured over four years has a standard error near √(1.5/4) ≈ 0.6 (Part 6). If the true
   Sharpe is 0.5, ten times leverage is twice Kelly and grows no faster than cash. Volatility can also triple, which
   divides Kelly by nine (chapter 9). Use half Kelly or less on the estimate, and recompute as the volatility forecast
   changes.
3. **Why not Kelly.** Kelly maximizes E log W, the expected utility of an investor with γ = 1. For γ = 3 the optimal
   fraction is a third of Kelly's at every horizon. Kelly ends richer with a probability that tends to one, but its
   rare losses are so large in that investor's utility that its certainty equivalent is lower (chapter 10:
   −3.6% against +3.9% a year).

4. **A drifted weight, with costs.** With a 1% cost per dollar traded and γ = 3 (μ = 8%, r = 2%, σ = 18%), the
   no-trade band from dynamic programming (monthly) is 55.8% to 67.8% around Merton's 61.7% (chapter 7). 66% is
   inside it: do nothing. Rebalancing to 62% would pay 1% on 4% of wealth for a gain of second order in the distance
   from the optimum; only when the weight leaves the band is trading worth its cost, and then only to the nearest
   edge.

## Problems, with solutions

1. **Kelly for any odds.** g(f) = p log(1 + bf) + q log(1 − f). g′(f) = pb/(1 + bf) − q/(1 − f) = 0 gives
   pb(1 − f) = q(1 + bf), so f* = (pb − q)/b = p − q/b. For a small edge, expand to second order:
   g(f) ≈ f(pb − q) − f²(pb² + q)/2. This is zero again at f ≈ 2(pb − q)/(pb² + q), which for b = 1 is 2(p − q) = 2f*.
2. **Merton's value function.** HJB: V_t + max_π {(r + π(μ − r))wV_w + ½π²σ²w²V_ww} = 0. Substitute
   V = e^{a(T−t)}w^{1−γ}/(1 − γ), so that V_t = −aV, wV_w = (1 − γ)V and w²V_ww = −γ(1 − γ)V. Dividing by (1 − γ)V,
   the HJB becomes −a/(1 − γ) + max_π {r + π(μ − r) − ½γπ²σ²} = 0. The maximum is at π* = (μ − r)/(γσ²), where it
   equals r + (μ − r)²/(2γσ²). So a = (1 − γ)(r + (μ − r)²/(2γσ²)), and V(T) = u(w).
3. **Fractional Kelly.** Excess growth is g(f) − r = f(μ − r) − ½f²σ², maximized at f* = (μ − r)/σ² with
   g* − r = (μ − r)²/(2σ²). At f = cf* it is c(μ − r)²/σ² − ½c²(μ − r)²/σ² = (2c − c²)(g* − r). The volatility is
   cf*σ. At c = ½: 75% of the growth and half the volatility. At c = 2: none of the growth and twice the volatility.
4. **The secretary.** If the best candidate is at position j > k, the rule picks them exactly when the best of the
   first j − 1 lies among the first k, which has probability k/(j − 1). So P(k) = (k/n)Σ_{j=k+1}^{n} 1/(j − 1). With
   x = k/n this is a Riemann sum for x∫_x^1 dt/t = −x log x. Its derivative, −log x − 1, is zero at x = 1/e, where
   the value is 1/e ≈ 36.8%. For n = 100 the best k is 37, with 37.1%.
5. **Peters' coin.** Staking a fraction f each flip gives g(f) = ½log(1 + 0.5f) + ½log(1 − 0.4f).
   g′(f) = 0.25/(1 + 0.5f) − 0.2/(1 − 0.4f) = 0 gives 0.25 − 0.1f = 0.2 + 0.1f, so f* = 0.25. Then
   g = ½log(1.125 × 0.9) = ½log 1.0125 ≈ +0.62% a flip, where staking everything loses ½log(1/0.9) ≈ 5.3%. Staking a
   quarter turns a losing gamble into a growing one.
6. **Smooth fit for the perpetual put.** Exercising at level b gives V_b(S) = (K − b)(S/b)^{−β} for S ≥ b, with
   β = 2r/σ². For fixed S this is S^{−β}(K − b)b^{β}, so maximize h(b) = (K − b)b^{β}: h′(b) = b^{β−1}(β(K − b) − b) = 0
   gives b* = βK/(1 + β). The slope of V_b at S = b is −β(K − b)/b, which equals −1 exactly when β(K − b) = b, the same
   condition: choosing the best boundary and pasting smoothly onto the payoff are one equation. With r = 5%, σ = 30%,
   K = 100: β = 1.11, b* = 52.6, V(100) = 47.4 × (100/52.6)^{−1.11} = 23.2.
7. **The liquidating crowd.** With φ = 0 the equation is Q″ + aQ′ = 0, a = κ(N − 1)/(2Nη), so Q′ = Ce^{−at} and
   Q(t) = (e^{−at} − e^{−aT})/(1 − e^{−aT}) with Q(0) = 1, Q(T) = 0. As N → ∞, aT = κT/(2η) = 2, and the share sold by
   T/5 is 1 − Q(T/5) = (1 − e^{−0.4})/(1 − e^{−2}) = 0.3297/0.8647 = 38.1%, against 20% for one trader alone (a = 0,
   a straight line) and 28.7% for two (aT = 1).


## Data and reproducibility

* Kenneth French's Fama–French factors, monthly and daily (market excess return and T-bill), July 1926 to December
  2020. The hold-out from 2021 is sealed (Part 6).
* Registered with the trial counter: the split-sample Kelly test, myopic loss aversion on US data, and volatility
  targeting on US data (one configuration each).
* Compute: about an hour of CPU on one thread per process, almost all of it PPO (ten runs of 300 iterations × 1,024
  ten-year episodes, two 32-unit hidden layers). Everything is seeded.
* Facts and their sources. LTCM: U.S. Treasury testimony presenting the President's Working Group's figures (Gensler,
  6 May 1999: $129 billion of assets on $4.7 billion of capital, 28 to 1, $1.3 trillion notional) and Federal Reserve
  History (a 44% loss in August 1998; fourteen firms, $3.6 billion, 23 September). Haghani and Dewey: their paper
  (arXiv 1701.01427). Thorp: his own chapter, Thorp (2006), *Handbook of Asset and Liability Management* vol. 1, ch. 9,
  pp. 385–428: Shannon and the Kelly paper (MIT, 1960), 3 November 1969, "approximately 20% annually with a standard
  deviation of about 6%" through May 1998, about $80 billion of trades in some 1.25 million bets, and the 1994
  sports test ($50,000, a $123,000 profit in 101 days, estimates "deliberately chosen to be conservative"). Benter:
  his chapter in Hausch, Lo and Ziemba (eds.), *Efficiency of Racetrack Betting Markets* (1994), pp. 191 and 195
  (the factor-of-two warning, downswings of more than 50% under full Kelly, "a conservative fractional Kelly betting
  strategy was employed throughout", about 470 races a year, a track take of about 19%, four of five seasons
  profitable). Berlekamp: Wikipedia and the University of California Senate memorial (Bell Labs under Kelly in 1960 and
  1962; control of Axcom in 1989). NBIM: the fund's risk-management page (a 1.25-percentage-point limit on expected
  relative volatility; about 0.3 at 30 June 2026). Bridgewater: "The All Weather Story" (launched 1996; "equal risk on
  each scenario"; "leverage is an implementation tool"). Millennium: reported by the *Wall Street Journal*, as relayed
  by *Business Insider* (October 2024); the firm declined to comment; a report, not a disclosure. Almgren et al.:
  "Equity market impact," *Risk* 18(7), 2005 (Citigroup's US equity trades). Haghani and White, *The Missing
  Billionaires* (Wiley, 2023).
* Not on screen because they could not be verified: that Medallion uses Kelly sizing; a "≈15% a year after fees"
  figure for Princeton Newport Partners (reported from Thorp's 2017 book only by secondary sources; the screen uses
  his 2006 chapter instead).

---

# 量化金融，从零搭建 — 第8部分：决策与控制

第7部分预测了市场会动多大，本部分问该下多大的注、何时停止。这是一场约55分钟的讲座，十九章加开场和结尾，可以替代研究生课程中随机控制与组合选择的相应章节：

* 期望效用（冯·诺伊曼-摩根斯坦公理）、风险厌恶，推导阿罗-普拉特溢价；
* 贝尔曼递推，从动态规划原理和伊藤公式推导HJB方程，验证定理，以及黏性解（为什么单调格式收敛）；
* 带消费的默顿问题，用HJB和鞅方法两种方式求解；两基金分离；
* 交易成本与戴维斯-诺曼不交易区间，用动态规划求解；
* 凯利与布雷曼定理的证明；分数凯利与估计风险（索普、本特）；LTCM；萨缪尔森的反驳与遍历性之争；
* 最优停止（斯内尔包络即最小凹优函数）与光滑粘合（麦基恩的永续看跌期权）；
* 前景理论（用数据重做贝纳茨-塞勒的短视损失厌恶）与稳健控制（梅恩豪特）；
* 双利率下的BSDE、平均场清仓博弈，以及有无交易成本时默顿问题上的PPO；
* 基金、投注团队和交易台如何定仓位，以及2023至2026年的前沿。

所有数字都由本系列自己的代码算出：历史部分用肯尼斯·弗伦奇的美国市场收益（月度与日度，1926–2020），其余用带种子的模拟，并在屏幕上标明。

*讲的是方法，不构成投资建议。*

## 各章（约55分钟）

* **该下多大的注，以及我们如何走到这里。** 哈加尼和杜威（2016）的硬币游戏，约30%的人输光。现场模拟：四列各160名玩家同抛一枚硬币300次（全押91%输光；押40%有18%输光；押20%有96%达到上限、无人输光）。凯利曲线；1738–2017年的历史，以期望效用为根的一棵树。
* **1. 效用与风险厌恶。** 公理卡片；赌博作为挂在效用曲线上的两个砝码，确定性等价86.6（对数效用）；伽马旋钮实时弯曲曲线（伽马为3时67.1，为30时51.2）。推导阿罗-普拉特；精确值对比近似值；拉宾的警告。
* **2. 贝尔曼原理（实验一）。** 三期树上的倒向归纳；幂效用下的短视性。实验：`bellman_merton`，处处62%（默顿61.7%）。回放：带下限问题的策略曲面在三维中一片片倒着搭建，财富为1时的最优比例从25%走到31%；与投资组合保险的最大差距0.005。
* **3. HJB方程与验证定理。** 推导HJB；哈密顿量是比例的抛物线，无下限时顶点不动，有下限时滑向零；验证定理。有限差分加策略迭代（400 × 401）：比例与默顿相差0.002个百分点以内，价值误差0.07%。
* **4. 黏性解。** |u′| = 1的无穷多几乎处处解；检验函数接触峰顶（通过）与谷底（不通过）；比较原理、Barles–Souganidis。迎风格式误差在舍入水平，中心差分误差从10^6到10^131。
* **5. 默顿问题。** 两个杯子：每月再平衡与买入持有；20,000条三十年路径上，伽马为3的确定性等价增长3.86%对3.77%。共同基金定理。美国数据：伽马1为238%，伽马3为79%（±2个标准误：42%–116%）。
* **6. 消费与鞅方法。** 推导默顿（1971）：ν = 3.0%（对数）、3.57%（伽马3）、更有耐心时2.90%；有限寿命下从4.7%升到全部。考克斯-黄 / KLS：终值是股票的幂次权益；2,000名每日再平衡的投资者落在静态曲线上（最大差距0.34%）。
* **7. 交易成本（实验二）。** 戴维斯-诺曼楔形中被反射的财富点（15年35笔交易，年换手0.9%对24%）。奇异控制、变分不等式、ε^{1/3}渐近。实验：`no_trade_band`，伽马3、按月：成本0.1%、0.5%、1%、2%时区间为59.4–64.0%、57.2–66.2%、55.8–67.8%、54.0–69.6%。对数效用、1%、按季：区间158–202%，扣成本后每年比按季再平衡到默顿多增长0.29%，换手10%对44%。
* **8. 凯利与布雷曼。** 凯利（1956）；香农1960年把论文给了索普；索普的合伙企业自1969年11月3日起到1998年5月每年复利约20%、标准差约6%（Thorp 2006）。推导与证明。现场：½、1、2倍凯利的扇形与时间平均线（6.2%、7.6%、2.0%即现金利率）。布雷曼的赛跑：10年/100年后凯利领先2倍凯利70%/95%，领先半凯利60%/80%。美国实现增长：100%为9.7%，最优218%为12.6%。
* **9. 分数凯利、估计风险与LTCM。** 推导(2c − c²)；优势高估k倍：全凯利在k = 2时增长为零，半凯利在k = 4；本特的警告。自助法最优比例云（90%在116%–302%之间）。登记过的样本分割检验。LTCM危机档案；波动率三倍时凯利杠杆从100降到11。
* **10. 萨缪尔森的反驳与遍历性。** 凯利更富的概率64%/87%，但确定性等价增长−3.6%对+3.9%；推导。现场：十万名玩家的彼得斯硬币直方图，82%亏钱；Peters、Meder等、Doctor–Wakker–Wang、Toda。凯利押25%（每次+0.62%）。
* **11. 最优停止：斯内尔包络（实验三）。** 价值迭代像绳子拉紧搭在21根木桩上（226次扫描）；实验：与上凸包相差5 × 10^-14。秘书问题（37 → 37.1%）。
* **12. 光滑粘合。** 麦基恩永续看跌期权：β = 1.11，b* = 52.6，V(100) = 23.21；40年二叉树给出52.5和23.01。利率升到7%时b* = 60.9。
* **13. 前景理论与模糊性。** 阿莱悖论；累积前景理论；登记检验：股票的前景价值在18个月的评估周期上超过国库券。埃尔斯伯格、吉尔博阿-施迈德勒、汉森-萨金特；推导梅恩豪特的稳健默顿：检测误差20%时θ = 1.9、比例48%；10%时θ = 4.4、32%；无怀疑79%。
* **14. 倒向随机微分方程。** 回放：两万条路径上的回归点云一步步倒推，Y0 = 1.219，高于两个Black–Scholes价格（1.050和0.605）；收敛到PDE的1.230。
* **15. 平均场博弈（实验四）。** 推导清仓博弈；虚拟博弈回放；实验：48轮残差低于10^-12；前五分之一时间卖出：单独20%、两家28.7%、十家36.2%、平均场38.1%。
* **16. 强化学习（实验五）。** 五个种子最终在169%–184%（季度最优184%），最多每年少赚0.04%；`TrainingReplay`回放。有成本时：PPO没有找到区间，净增长7.27–7.33%，区间7.42%，按季再平衡到默顿7.13%。
* **17. 谁以定仓位为生。** 索普1994年的体育投注测试；本特的分数凯利；伯利坎普与Axcom（大奖章的仓位方法未公开）；挪威主权基金1.25个百分点的跟踪误差上限；桥水全天候；据《华尔街日报》报道的千禧年回撤规则。格罗斯曼-周对凯利（最大回撤17%对99%）；波动率目标（夏普0.51对0.44，阿尔法每年3.5%，t = 2.9）。
* **18. 前沿，2023–2026。** 各章构成一张图，每篇论文点亮它所建立的那条边。
* **19. 仓位模块。** 新函数；定仓位流程（凯利238% → 一半119%；20%检测误差下的稳健比例145%并不更小）；扩展的第九条规则；试验计数器82。
* **回顾、交易台问题与习题。**

## 交易台问题与解答


1. **六成的硬币，赔率一赔一。** 最大化g(f) = 0.6 log(1 + f) + 0.4 log(1 − f)。令g′(f) = 0.6/(1 + f) − 0.4/(1 − f) = 0，得f* = 0.2，
   g(0.2) ≈ 每次2.0%。g(0.4) ≈ −0.2%：两倍凯利就不再增长。有上限和时间限制时，目标是达到上限而不是长期增长，略低于凯利同样好。
   在300次、上限250美元的设定下，押10%和20%达到上限的概率都约为94%。
2. **波动率10%、夏普为1。** f* = (μ − r)/σ² = SR/σ = 10，纸面上凯利的超额增长为SR²/2 = 每年50%。但四年测得的夏普比率，
   标准误约为√(1.5/4) ≈ 0.6（第6部分）。若真实夏普为0.5，十倍杠杆就是两倍凯利，增长不比现金快。波动率还可能变成三倍，
   使凯利杠杆除以九（第9章）。应按估计值用半凯利或更低，并随波动率预测重新计算。
3. **为什么不用凯利。** 凯利最大化E log W，即伽马为1的投资者的期望效用。对伽马为3的投资者，最优比例在每个期限上都是凯利的三分之一。
   凯利最终更富的概率趋于一，但它少见的亏损在该投资者的效用中代价极大，所以它的确定性等价更低（第10章：每年−3.6%对+3.9%）。

4. **成本下漂移的权重。** 每交易一美元成本1%、伽马为3（μ = 8%，r = 2%，σ = 18%）时，按月动态规划得到的不交易区间是55.8%到67.8%，
   围绕默顿的61.7%（第7章）。66%在区间内：什么都不做。只有权重离开区间时交易才值得付出成本，而且只交易到最近的边缘。

## 习题与解答

1. **任意赔率下的凯利。** g(f) = p log(1 + bf) + q log(1 − f)。令g′(f) = pb/(1 + bf) − q/(1 − f) = 0，得pb(1 − f) = q(1 + bf)，
   即f* = (pb − q)/b = p − q/b。小优势时展开到二阶：g(f) ≈ f(pb − q) − f²(pb² + q)/2，在f ≈ 2(pb − q)/(pb² + q)处再次为零，
   b = 1时即2(p − q) = 2f*。
2. **默顿的价值函数。** HJB方程为V_t + max_π {(r + π(μ − r))wV_w + ½π²σ²w²V_ww} = 0。代入V = e^{a(T−t)}w^{1−γ}/(1 − γ)，
   则V_t = −aV，wV_w = (1 − γ)V，w²V_ww = −γ(1 − γ)V。除以(1 − γ)V后，HJB化为−a/(1 − γ) + max_π {r + π(μ − r) − ½γπ²σ²} = 0。
   最大值在π* = (μ − r)/(γσ²)处取得，等于r + (μ − r)²/(2γσ²)。所以a = (1 − γ)(r + (μ − r)²/(2γσ²))，且V(T) = u(w)。
3. **分数凯利。** 超额增长g(f) − r = f(μ − r) − ½f²σ²，在f* = (μ − r)/σ²处取最大，此时g* − r = (μ − r)²/(2σ²)。
   在f = cf*处它等于(2c − c²)(g* − r)，波动率为cf*σ。c = ½时得到75%的增长和一半的波动率；c = 2时增长为零，波动率翻倍。
4. **秘书问题。** 若最佳者在位置j > k，当且仅当前j − 1人中最好的那位落在前k人之中时规则会选中他，概率为k/(j − 1)。
   所以P(k) = (k/n)Σ_{j=k+1}^{n} 1/(j − 1)。记x = k/n，这是x∫_x^1 dt/t = −x log x的黎曼和。其导数−log x − 1在x = 1/e处为零，
   此时值为1/e ≈ 36.8%。n = 100时最优k为37，成功率37.1%。
5. **彼得斯的硬币。** 每次押比例f，增长率g(f) = ½log(1 + 0.5f) + ½log(1 − 0.4f)。令g′(f) = 0.25/(1 + 0.5f) − 0.2/(1 − 0.4f) = 0，
   得0.25 − 0.1f = 0.2 + 0.1f，即f* = 0.25。此时g = ½log(1.125 × 0.9) = ½log 1.0125 ≈ 每次+0.62%，而全押每次损失½log(1/0.9) ≈ 5.3%。
   只押四分之一，就把一个亏损的赌博变成了增长的赌博。
6. **永续看跌期权的光滑粘合。** 在水平b行权，S ≥ b时V_b(S) = (K − b)(S/b)^{−β}，β = 2r/σ²。固定S时它等于S^{−β}(K − b)b^{β}，
   所以最大化h(b) = (K − b)b^{β}：h′(b) = b^{β−1}(β(K − b) − b) = 0，得b* = βK/(1 + β)。V_b在S = b处的斜率是−β(K − b)/b，
   它等于−1恰好当β(K − b) = b，即同一个条件：选最优边界与光滑地粘到收益上是同一个方程。r = 5%、σ = 30%、K = 100时，
   β = 1.11，b* = 52.6，V(100) = 23.2。
7. **清仓的人群。** φ = 0时方程为Q″ + aQ′ = 0，a = κ(N − 1)/(2Nη)，所以Q′ = Ce^{−at}，Q(t) = (e^{−at} − e^{−aT})/(1 − e^{−aT})，
   满足Q(0) = 1、Q(T) = 0。N → ∞时aT = κT/(2η) = 2，到T/5时卖出的份额为(1 − e^{−0.4})/(1 − e^{−2}) = 38.1%，
   单独一家（a = 0，直线）为20%，两家（aT = 1）为28.7%。

