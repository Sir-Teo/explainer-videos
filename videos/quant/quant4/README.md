# Quant, Built — Part 4: Martingales and Measure

Part 4 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the first part of Act II, the Mathematical Toolkit. It makes "a fair game"
precise, at the depth of a graduate course: σ-algebras and filtrations, conditional expectation as a projection,
martingales and the martingale transform, stopping times and optional stopping with its proof, doubling and
admissibility, Barings, gambler's ruin, martingale convergence, Doob's decomposition, the change of measure, the
Radon–Nikodym theorem and Kakutani's dichotomy, stable laws, Ville's inequality and testing by betting, learning to
bet, how casinos, bookmakers and prediction markets live with all of this, and the 2023–2026 frontier. Every number is
computed by the series' own code ([`compute.py`](compute.py), the House's
[`martingale`](../../../explainer/quant/house/martingale.py) module) from public data: Kenneth French's daily US market
since 1926, Binance's Bitcoin, and the Nikkei 225 from FRED. Simulations and schematics are labelled on screen; firms,
courts and events come from the public record, with secondary reports labelled "as reported".

*An education in methods, not investment advice, and nothing here is gambling advice.*

## Chapters (about 57 minutes)

* **Can you beat a fair game?** A bettor wagers every day since 1926 that today's US return keeps yesterday's sign;
  drawn live, wealth passes 20 in February 1929 and reaches about 10¹⁰¹; started in 2000 it peaks at 6.7. The problem
  of points (Pascal to Fermat, 29 July 1654) as a tree: 2–1 is worth 48 : 16, 2–0 is worth 56 : 8. The era strip from
  1654 to 2023; objectives; the House.
* **1. Information: σ-algebras and filtrations.** Eight worlds and refining partitions; |F_n| = 2^(2^n); measurability
  as "constant on every block" (the first toss passes, the number of heads fails); adapted processes. The coin space
  as the unit interval, zoomed six tosses deep; Kolmogorov (1933).
* **2. Conditional expectation is a projection.** Kolmogorov's definition, the partition formula, orthogonality,
  Pythagoras (best mean-square forecast), taking out what is known, the tower, Jensen and independence, each with a
  reason. In 3D: Ω = {a, b, c}, P = (0.5, 0.3, 0.2), coordinates √p_i x_i; X = (3, 0, 1) projects to (1.875, 1.875, 1)
  and then to 1.7, as does X directly. On the market, E[r_{t+1} | sign r_t]: 1926–74 +13.5 / −9.4 bp, 1975–99
  +16.0 / −5.0 bp, 2000–20 −0.3 / +7.9 bp, with 200 block-bootstrap resamples. **Lab 1:** `cond_exp`.
* **3. Martingales: Ville's fair games.** Definition, super- and submartingales, Ville and Doob; S_n² − n, the
  exponential martingale, Doob's martingale and Jensen, each proved. The best-of-21 forecast drawn live with the
  next-step fan (tomorrow's two values, their mean = today). E(S_n − 2)⁺ rises to 1.92 at n = 50, E|S_50| = 5.61;
  Markov ≠ martingale.
* **4. You can't beat the system.** The martingale transform (Williams, ch. 10) and the cheat who stakes after
  peeking. The curtain desk: twelve tosses, stakes set before each card turns. Six systems on European red over
  20,000 sessions of 200 spins (limit 500): loss ÷ staked = −0.0267 (flat), −0.0250 ± 0.0025 (doubling), −0.0266
  (d'Alembert), −0.0274 (Labouchère), −0.0255 ± 0.0028 (Fibonacci), −0.0268 (Oscar): all within two standard errors
  of −1/37. **Lab 2:** `martingale_transform` and `system_stakes`.
* **5. Stopping times, and the walk that always wins.** The bell and the curtain (a hitting time rings; "the top of
  the path" needs the future). Stopped martingales; reflection P(τ₁ > n) = P(S_n ∈ {0, 1}) ≈ √(2/(πn)); E τ₁ = ∞ by
  Wald; the generating function (Shreve I, ch. 5). 10,000 walks to 10⁵ steps: P(τ₁ > 100) = 0.0757 (exact 0.0796);
  the mean of τ₁ ∧ n is 14, 45, 146, 483 for n = 10², 10³, 10⁴, 10⁵.
* **6. Optional stopping, proved.** The three conditions and uniform integrability; the leaking balance (S_{τ₁∧n}
  for n = 10 … 10⁴: 76% → 99% at +1, the mean stays 0). Li's (1980) casino of gamblers: E τ(HH) = 6; simulated
  waits 6.00, 4.00, 10.01, 14.05 for HH, HT, HTH, HHH; Penney: THH beats HHT 3/4 of the time (simulated 0.749);
  ABRACADABRA: 26¹¹ + 26⁴ + 26. **Lab 3:** `pattern_wait`.
* **7. Doubling and admissible strategies.** Why doubling escapes optional stopping; bankroll 2^k − 1 makes the
  game fair; 1,000 doublers × 3,000 sessions drawn live: 94.2% ruined at least once (theory 94.7%), mean P&L +9.9 ±
  55, mean wait for the first ruin 1,026 (theory 1,024). Admissibility (Harrison–Pliska 1981; Dybvig–Huang 1988).
* **8. Doubling down: Barings, 1995.** The crisis file with the Board of Banking Supervision's figures (via the RBA
  *Bulletin*, Nov. 1995): £827 m of unreported losses by 27 February 1995, group capital about £350 m. FRED's Nikkei
  through Kobe. A schematic doubling rule on the real index (labelled as such): it reaches 256 units and crosses a
  stated capital six days after Kobe; with unlimited credit it would have recovered within days, capped at 16 units it
  never does. Segregation of duties as the control that enforces the theorem's hypotheses.
* **9. Gambler's ruin and bold play.** a/b and de Moivre's (q/p)^X; expected duration a(b − a) = 2,500 (4,000 games:
  2,481 ± 31; roulette 1,598 vs 1,618); the roulette curves (50%, 6.3%, 0.51%); bold play (Dubins–Savage 1965).
* **10. Martingales converge.** The upcrossing trader and Doob's lemma (Gaussian walks: mean upcrossings of [−3, 3]
  1.46 against the bound 1.87); Doob's forward convergence theorem; uniform integrability. 100 Pólya urns live and the
  limits of 10,000 (K–S distance from uniform 0.007; P(limit > 0.9) = 0.097). Lévy's upward theorem as learning: a
  Bayesian learner of the market's mean, scrubbed from 1926: ±7.8% a year after ten years, 9.5% ± 2.0% by 2020.
* **11. Doob's decomposition.** Existence, uniqueness, ⟨M⟩, and the filtration's role. *Ivey v Genting* with the
  court's figures (house edge 1.24%, sorting edge about 6.5%): one simulated punto banco game, two drifts. The US
  market: 9.06 = 7.28 + 1.78; the compensator 2.893 against realized quadratic variation 2.894.
* **12. Change of measure.** P, Q and L on three tosses; the density process, Bayes' rule, discrete Girsanov, Esscher;
  200 paths recoloured, not moved; L collapses under P (median 0.002) and grows under Q. The Esscher measure of US
  returns: θ = −2.60, mean daily log return 3.64 → 0.60 bp, the worst 1% of days carry 1.13% of Q's weight.
  **Lab 4:** `esscher_tilt`.
* **13. Radon–Nikodym, and the singular infinite.** The theorem by dyadic martingales; equivalence and arbitrage;
  Kakutani's dichotomy. In 3D: bars Q(cell)/P(cell) refine from 2×2 to 16×16 into the density (1 + 2xy)/1.5, while a
  diagonal Q never forms a surface. Simulated: a constant 60% tilt sends log₁₀ L to about −88 in 10,000 tosses; a
  fading tilt ½ + 0.2/k keeps L positive with mean 0.99.
* **14. Heavy tails as stable laws.** Lévy, Mandelbrot, Fama; McCulloch's α (1.40 US, 1.27 Bitcoin; Mantegna and
  Stanley's 1.40 on screen); the characteristic function and Koutrouvelis's regression (US 1.75 [1.74, 1.78], Gaussian
  control 2.00); a maximum-likelihood fit replayed for three samples (α̂ = 1.45, 1.45, 1.51 against McCulloch's 1.35,
  1.35, 1.41); the kurtosis of h-day sums falls from 17.7 (h = 1) to 5.3 (h = 60): the variance is finite.
* **15. Ville's inequality and testing by betting.** The theorem and its proof; e-values (Vovk–Wang calibration); the
  law of the iterated logarithm. Two live counters over 2,000 fair games: daily t-tests 50% false alarms, e-process
  3.2%. Shafer and Vovk's game. Real data, as in the hook.
* **16. Learning to bet.** Kelly growth and the time to reject (2 log 20 / SR², about 2,400 days at a daily Sharpe of
  0.05); the online Newton step bettor replayed over 10,000 days (crosses 20 on day 2,541; stake near 0.21 against
  Kelly 0.20); a race of four bettors × four edges × 8 seeds (no edge: 3.1–4.5% false alarms; at SR 0.05 the fixed
  menu, median 3,054 days, beats ONS 3,393 and aGRAPA 3,475, the oracle needs 1,865); the hook's tests with the
  learner; a betting confidence sequence for Bitcoin's mean (−16 to +28 bp a day at the end of 2020). **Lab 5:**
  `ONSBettor`; Rule 5 gains "the stake may be learned"; trial counter 82.
* **17. The house, the book and the market.** Nevada roulette hold 17.34% (2024) against a 5.26% edge: about 3.3 bets
  per dollar of chips (UNLV); Azuma's bound against the exact chance the house is behind; Thorp, *Uston v. Resorts*,
  Ivey; Kaunitz, Zhong and Kreiner's bookmaker study; Flutter's US sportsbook margin (7.9%, 2024); Benter (as
  reported); Kalshi and Polymarket; Augenblick–Rabin's movement test (Bayesian forecasts 1.00, a 30% overreactor
  1.47); Bürgi–Deng–Whelan on Kalshi; sequential testing at Optimizely and Netflix.
* **18. Frontier: anytime-valid inference, 2023–2026.** Ten papers on screen; the numéraire bridge (the Kelly
  portfolio is the log-optimal e-variable); e-BH on 200 strategies × 2,520 days × 20 seeds: stopping on the first day
  with ten discoveries, e-BH's FDR is 2.5% and BH's 17.8%. **Lab 6:** `e_bh`.
* **Recap, desk questions, problems.**

## Textbook audit

| Textbook section | Chapter |
|---|---|
| Williams, *Probability with Martingales*, ch. 0 (branching process) | 10 (convergent martingales), README |
| Williams ch. 1–3 (measure spaces, events, random variables) | 1 |
| Williams ch. 4 (independence; §4.9 the monkey typing Shakespeare) | 1, 6 (ABRACADABRA) |
| Williams ch. 5–6 (integration, MON, DOM) | 6 (dominated convergence in the proof) |
| Williams ch. 7–8 (strong law, product measure) | 13 (L_n → 0, Kakutani) |
| Williams ch. 9 (conditional expectation, least squares, properties) | 2 |
| Williams ch. 10 (filtrations, martingales, "you can't beat the system", stopping times, optional stopping, hitting times) | 3, 4, 5, 6 |
| Williams ch. 11 (upcrossings, Doob's forward convergence theorem) | 10 |
| Williams ch. 12 (L²-bounded martingales, Doob decomposition, ⟨M⟩) | 11 |
| Williams ch. 13 (uniform integrability) | 6, 10 |
| Williams ch. 14 (UI martingales, Lévy upward, Doob's inequalities, Kakutani, Radon–Nikodym, likelihood ratios) | 10, 13, 15, 12 |
| Williams ch. 15 (applications: representation, discrete Black–Scholes, filtering) | Parts 5, 7, 9 |
| Williams ch. 16–18 (characteristic functions, weak convergence, CLT) | 14 |
| Shreve I, §2.1–2.2 (finite probability spaces) | 1 |
| Shreve I, §2.3 (conditional expectations) | 2 |
| Shreve I, §2.4–2.5 (martingales; Markov processes) | 3 |
| Shreve I, §3.1–3.2 (change of measure, Radon–Nikodym derivative process) | 12 |
| Shreve I, §5.2–5.3 (first passage times, reflection) | 5 |
| Shreve I, ch. 4 and §5.4 (American claims) | Parts 8, 10 |
| Shreve II, §1.1–1.3 (infinite probability spaces, coin tosses and Lebesgue measure) | 1 |
| Shreve II, §1.4 (convergence of integrals) | 6 |
| Shreve II, §1.6 (change of measure) | 12 |
| Shreve II, §2.2–2.4 (information, independence, conditional expectation) | 1, 2 |
| Föllmer–Schied, §1.2 (arbitrage and martingale measures, preview) | 7, 13 (full treatment Part 9) |
| Föllmer–Schied, App. A.2 (absolutely continuous and equivalent measures) | 13 |
| Durrett, *Probability: Theory and Examples*, ch. 4 (martingales) | 3–6, 10 |

Section numbers in Williams are given at chapter level, except §4.9; the chapter titles were checked against the
book's contents.

## Labs, replays and simulations

Labs (House code on screen, then run): `cond_exp` (2), `martingale_transform` + `system_stakes` (4), `pattern_wait`
(6), `esscher_tilt` (12), `ONSBettor` (16), `e_bh` (18). Fits and learners replayed: the stable-law maximum
likelihood (14, `TrainingReplay`, three seeds), the ONS bettor (16, `TrainingReplay`), the Bayesian drift learner (10,
scrubbed by a `ValueTracker`). Live simulations: the hook's wealth, the next-step fan, six systems, 120 first-passage
walks, the leaking balance, 80 doublers, 60 ruin games, 100 Pólya urns, two peeking counters, the confidence sequence.
3D: the projection (2), the dyadic Radon–Nikodym city (13).

## Build it

```bash
python -m videos.quant.quant4.compute                        # every number, cached in .cache/quant4/ (about 45 CPU-minutes)
EXPLAINER_TTS=silent python tools/qa_scene.py quant4 Optional   # one chapter, silent, with a contact sheet
python tools/make.py quant4 --cpu-voice -q m                 # English and Chinese, narrated by Kokoro on the CPU
```

`stable_mle` (about 30 minutes under load) and `learner` are resumable.

## Desk questions, with solutions

1. **A martingale starts at 1 and stops at 0 or 3.** The stopped process is bounded between 0 and 3, so optional
   stopping applies: E[M_τ] = 1. With p = P(hit 3), 3p + 0·(1 − p) = 1 and p = 1/3.
2. **Expected tosses to see HH.** Before every toss a new gambler arrives with $1 and bets it on heads at fair odds. If
   heads comes, the gambler bets the $2 on heads again, and otherwise leaves with nothing. The casino's net take is a
   martingale with bounded steps and E τ < ∞. When HH first appears at time τ, the casino has taken in τ dollars and
   owes $4 to the gambler who arrived at τ − 1 and $2 to the one who arrived at τ. So E[τ] − 6 = 0, and E[τ] = 6.
   (For HT the answer is 4: only the gambler at τ − 1 is paid.)
3. **$100 at European roulette, $200 needed.** One bet of everything on red succeeds with probability 18/37 ≈ 48.6%.
   One-unit bets succeed with probability (1 − (q/p)¹⁰⁰)/(1 − (q/p)²⁰⁰) ≈ 0.45%. In a subfair game, bold play is
   optimal (Dubins and Savage).
4. **Penney's game: HHT against THH.** Unless the first two tosses are HH (probability 1/4, and then HHT must come
   first, since the run of heads ends with a T), a T has appeared before any HH, so the first HH is preceded by a T:
   THH appears no later than HHT. P(THH first) = 3/4. Conway's formula (`penney_odds`) agrees, and so does a
   simulation (0.749).
5. **A fair walk stopped the first time it is up 1: E τ?** Infinite. If E τ were finite, Wald's identity would give
   E S_τ = 0 · E τ = 0, but S_τ = 1. (Equivalently, P(τ > n) ≈ √(2/(πn)) is not summable.)

## Problems, with solutions

1. **Exit time.** E[S²_{n+1} − (n + 1) | F_n] = S²_n + 2S_n·E[ξ] + E[ξ²] − n − 1 = S²_n − n, so S²_n − n is a
   martingale. Stop at τ = first time |S| = a. The steps are bounded and E[τ] < ∞, so E[S²_τ] − E[τ] = 0. Since
   S²_τ = a², E[τ] = a².
2. **Biased ruin.** E[(q/p)^{X_{n+1}} | F_n] = (q/p)^{X_n}·(p·(q/p) + q·(p/q)) = (q/p)^{X_n}. Optional stopping gives
   (q/p)^a = P(hit b)(q/p)^b + (1 − P(hit b)), so P(hit b) = (1 − (q/p)^a)/(1 − (q/p)^b). With p = 18/37, a = 10 and
   b = 20 this is 36.8% (a simulation of 4,000 games gives 36.4%).
3. **Doubling with 2^k − 1.** A session wins 1 unless the first k tosses are all losses (probability 2^{−k}), which
   loses 2^k − 1. The expected gain is (1 − 2^{−k}) − 2^{−k}(2^k − 1) = 0. The number of sessions up to and including
   the first ruin is geometric with mean 2^k: about 1,024 sessions for k = 10 (simulated 1,026).
4. **Collapse of the likelihood ratio.** E_P[L_n] = Σ_ω P(ω)Q(ω)/P(ω) = 1. log L_n is a sum of i.i.d. terms with mean
   E_P[log(Q/P)] = −D(P‖Q). Here D = ½ ln(0.5/0.6) + ½ ln(0.5/0.4) = 0.0204 nats a toss, so L_n → 0 almost surely.
   The median of L₃₀₀ is about e^{−300 × 0.0204} = 0.0022, which matches the simulated 0.002; after 10,000 tosses,
   log₁₀ L ≈ −10,000 × 0.0204/ln 10 = −88.6 (simulated median −88.3).
5. **Ville's inequality and peeking.** Let τ be the first n with W_n ≥ c. Optional stopping at the bounded time
   min(τ, n) gives 1 ≥ E[W_{τ∧n}] ≥ c·P(τ ≤ n), so P(τ ≤ n) ≤ 1/c. Let n → ∞, and take c = 1/α. A daily t-statistic
   is S_n/√n. By the law of the iterated logarithm, S_n/√(2n log log n) has limsup 1, so |S_n|/√n exceeds any fixed
   level infinitely often, and a test checked forever rejects a true null with probability one.
6. **Pólya's limit.** By induction: if P(R_n = k) = 1/(n + 1) for k = 1, …, n + 1 (with n + 2 balls), then
   P(R_{n+1} = k) = P(R_n = k)·(n + 2 − k)/(n + 2) + P(R_n = k − 1)·(k − 1)/(n + 2) = (1/(n + 1))·(n + 1)/(n + 2) =
   1/(n + 2). So R_n/(n + 2) is uniform on {1/(n + 2), …, (n + 1)/(n + 2)}, and its limit is Uniform(0, 1).
7. **Wald's identity.** With i.i.d. steps of mean μ and E|ξ| < ∞, M_n = S_n − nμ is a martingale with increments
   bounded in mean: E[|ΔM| | F] ≤ E|ξ| + |μ|. If E τ < ∞, then |M_{τ∧n}| ≤ Σ_{k≤τ} |ΔM_k|, whose mean is at most
   (E|ξ| + |μ|) E τ (the same argument as Wald's for Σ|ξ_k|), so optional stopping under condition (c) gives
   E[S_τ − τμ] = 0, i.e. E S_τ = μ E τ.

## Facts checked for this part

* Barings: the Board of Banking Supervision's report (18 July 1995), as summarized by the Reserve Bank of Australia
  (*Bulletin*, November 1995): £827 m of unreported losses by 27 February 1995, group capital about £350 m, unauthorised
  activity for about 2½ years, Leeson controlling front and back office; "clear segregation of duties is fundamental
  to any effective control system". Account 88888: FIA (2020). ING for £1, founding in 1762, the six-and-a-half-year
  sentence: public record. The positions' sizes and strikes are not shown (not checked).
* *Ivey v Genting* [2014] EWHC 3394 (QB): house edge 1.24% (player) and 1.06% (banker), perfect edge sorting about
  6.5%, just over £7.7 m won at Crockfords on 20–21 August 2012; [2017] UKSC 67.
* *Uston v. Resorts International Hotel*, 89 N.J. 163, 445 A.2d 370 (1982): the Casino Control Act left rules on card
  counting to the Casino Control Commission, which had adopted none, so the casino could not exclude Uston for
  counting on its own.
* UNLV Center for Gaming Research, *Nevada Table Games: Historical Hold Percentage Variations* (March 2026): roulette
  hold 17.34% (2024), monthly average 18.84% (Jan. 2004 – Feb. 2026), s.d. 3.15; blackjack 14.30% (2024).
* Flutter Entertainment plc, Form 10-K for fiscal 2024 (US segment): sportsbook net revenue margin 7.9% (7.5% in
  2023), amounts staked $50,876 m.
* Kaunitz, Zhong and Kreiner (2017), arXiv:1710.02824: 56,435 backtested bets, 3.5% return; 265 live bets, $957.50,
  8.5%; accounts "severely" limited.
* Kalshi: *KalshiEX v. CFTC* (D.D.C., September 2024, Judge Jia Cobb); the D.C. Circuit declined to stay it.
  Polymarket's 2024 presidential market: "nearly $3.7 billion" traded and one trader's net profit of about $79 m
  (Chainalysis), as reported by The Block.
* Bürgi, Deng and Whelan (CESifo WP 12122): only the qualitative findings (sharper prices near the close, a
  favourite–longshot bias, stronger for takers) are used; the return figures are not.
* Larsson, Ramdas and Ruf (2024) is cited by its arXiv number (2402.18810); its journal is not given.
* Waudby-Smith and Ramdas, *JRSS B* 86(1) (2024).

---

# 量化金融，从零搭建 — 第4部分：鞅与测度

本部分是第二幕“数学工具箱”的第一部分，以研究生课程的深度把“公平博弈”变得精确：σ代数与过滤，条件期望即投影，鞅与鞅变换，停时与可选停止定理
（附证明），加倍下注与容许策略，巴林银行，赌徒破产，鞅收敛，杜布分解，测度变换，拉东–尼科迪姆定理与角谷二分法，稳定分布，维尔不等式与以下注来检验，
学会下注，赌场、博彩公司和预测市场如何与这一切共处，以及2023–2026年的研究前沿。所有数字都由本系列自己的代码根据公开数据算出；模拟和示意在屏幕上
标明，公司、判例和事件来自公开记录，二手报道标明“据报道”。

*讲的是方法，不构成投资建议，也不构成任何博彩建议。*

## 各章（约57分钟）

* **你能战胜公平博弈吗？** 1926年以来每天押“今天与昨天同号”的赌徒，财富在1929年2月越过20；从2000年开始最高只到6.7。点数问题
  （帕斯卡致费马，1654年7月29日）：二比一值48比16，二比零值56比8。1654–2023年的时间线。
* **1. 信息：σ代数与过滤。** 八个世界与不断细分的划分；|F_n| = 2^(2^n)；可测即“在每一块上为常数”；适应过程；单位区间上的掷币空间；科尔莫戈罗夫。
* **2. 条件期望是一种投影。** 定义、划分公式、正交性、勾股定理、提出已知量、塔性质、詹森与独立性。三维投影：X = (3, 0, 1) → (1.875, 1.875, 1) → 1.7。
  市场上E[r_{t+1} | sign r_t]：1926–74年 +13.5 / −9.4个基点，1975–99年 +16.0 / −5.0，2000–20年 −0.3 / +7.9。**实验1：** `cond_exp`。
* **3. 鞅：维尔的公平博弈。** 上鞅、下鞅；S_n² − n、指数鞅、杜布鞅、詹森；二十一局三胜制的实时预测与“下一步扇形”；E(S_50 − 2)⁺ = 1.92。
* **4. 你赢不了这个系统。** 鞅变换；幕布后的十二次掷币；六个系统在欧式轮盘上各两万局：损失/注额都在−1/37的两个标准误之内。**实验2：** `martingale_transform`。
* **5. 停时，以及永远会赢的随机游走。** 敲钟与幕布；反射原理；E τ₁ = ∞（沃尔德）；一万条游走走到10⁵步：P(τ₁ > 100) = 0.0757（精确值0.0796）。
* **6. 可选停止定理的证明。** 三个条件与一致可积；“漏掉的天平”；李硕彦的赌徒赌场：E τ(HH) = 6；彭尼游戏3/4。**实验3：** `pattern_wait`。
* **7. 加倍下注与容许策略。** 一千位加倍下注者×三千局：94.2%至少破产一次，平均盈亏+9.9 ± 55，首次破产平均1,026局；哈里森–普利斯卡，迪布维格–黄。
* **8. 加倍下注：巴林银行，1995。** 银行监管委员会的数字：到1995年2月27日未申报亏损8.27亿英镑，集团资本约3.5亿英镑；日经指数与神户地震；
  在真实指数上的示意加倍规则（明确标注）；职责分离。
* **9. 赌徒破产与大胆下注。** a/b与棣莫弗鞅；期望持续时间a(b − a) = 2,500（模拟2,481 ± 31）；大胆下注（Dubins–Savage）。
* **10. 鞅会收敛。** 上穿交易者与杜布引理；一百个波利亚罐子；列维向上定理即学习：贝叶斯学习者到2020年估计市场年均收益9.5% ± 2.0%。
* **11. 杜布分解。** 存在性、唯一性、⟨M⟩、过滤的作用；艾维案（法院认定的1.24%与6.5%）；美国市场9.06 = 7.28 + 1.78。
* **12. 测度变换。** 密度过程、贝叶斯法则、离散吉尔萨诺夫、埃舍尔变换；美国收益的埃舍尔测度：θ = −2.60，最差1%的日子承载Q的1.13%权重。**实验4：** `esscher_tilt`。
* **13. 拉东–尼科迪姆，以及奇异的无穷。** 二进鞅证明；等价与套利；角谷二分法；三维柱状城市收敛到密度。
* **14. 作为稳定分布的厚尾。** 麦卡洛克α = 1.40；特征函数回归1.75；最大似然拟合回放；h日收益的峰度从17.7降到5.3：方差有限。
* **15. 维尔不等式与以下注来检验。** 证明；e值；重对数律；每日t检验误报50%，e过程3.2%；沙弗–沃夫克博弈。
* **16. 学会下注。** 凯利增长与拒绝时间；在线牛顿步下注者回放；四种下注者的比赛；比特币均值的置信序列。**实验5：** `ONSBettor`。
* **17. 赌场、庄家与市场。** 内华达轮盘留存率17.34%对5.26%优势；东和敬不等式；索普、乌斯顿案、艾维案；考尼茨等人的博彩研究；Flutter 7.9%；
  Kalshi与Polymarket（据报道）；奥根布利克–拉宾检验；Optimizely与Netflix。
* **18. 前沿：随时有效的推断。** 十篇论文；计价单位之桥；两百个策略上的e-BH：以“第一次有十个发现”为停止规则，e-BH的FDR为2.5%，BH为17.8%。**实验6：** `e_bh`。

教科书对照表见英文部分。

## 交易台问题与解答

1. **一个鞅从1出发，首次碰到0或3时停止。** 停止过程夹在0和3之间，可选停止定理成立：E[M_τ] = 1。设p = P(碰到3)，则3p = 1，p = 1/3。
2. **期望掷多少次才出现两个连续正面？** 每次掷币前来一位新赌徒，拿1美元按公平赔率押正面；若中，再把2美元押正面，否则离开。赌场的净收入是步长有界、
   E τ < ∞的鞅。HH在τ时刻首次出现时，赌场收进τ美元，要付τ − 1时刻到来的赌徒4美元、τ时刻到来的赌徒2美元：E[τ] = 6。（HT的答案是4。）
3. **欧式轮盘，手上100美元，今晚需要200美元。** 全部押红一次，成功概率18/37 ≈ 48.6%；每次押1美元，成功概率约0.45%。对你不利时，大胆下注最优。
4. **彭尼游戏：正正反对反正正。** 除非前两次都是正面（概率1/4，此时正正反必然先出现），否则在任何正正之前已出现过反面，于是第一个正正前面是反面：
   反正正不晚于正正反出现。P(反正正先出现) = 3/4（模拟0.749）。
5. **公平游走在第一次领先1时停止，E τ是多少？** 无穷大。若E τ有限，沃尔德恒等式给出E S_τ = 0，但S_τ = 1。

## 习题与解答

1. **离开区间的时间。** S²_n − n是鞅；在τ = 首次|S| = a时停止，步长有界且E[τ] < ∞，故E[τ] = a²。
2. **有偏博弈的破产概率。** (q/p)^{X_n}是鞅，可选停止给出P(碰到b) = (1 − (q/p)^a)/(1 − (q/p)^b)；p = 18/37、a = 10、b = 20时为36.8%。
3. **本金2^k − 1的加倍下注。** 期望收益(1 − 2^{−k}) − 2^{−k}(2^k − 1) = 0；直到第一次破产的轮数服从均值2^k的几何分布（k = 10时模拟为1,026）。
4. **似然比的崩塌。** E_P[L_n] = 1，而(1/n) log L_n → −D(P‖Q) = −0.0204；L₃₀₀的中位数约0.0022；一万次后log₁₀ L ≈ −88.6（模拟中位数−88.3）。
5. **维尔不等式与反复查看。** 在有界时刻min(τ, n)应用可选停止：1 ≥ c·P(τ ≤ n)，令n → ∞。由重对数律，每天查看的t检验终将拒绝真实的原假设。
6. **波利亚罐子的极限。** 归纳：若P(R_n = k) = 1/(n + 1)，则P(R_{n+1} = k) = 1/(n + 2)；所以红球比例在极限上服从Uniform(0, 1)。
7. **沃尔德恒等式。** M_n = S_n − nμ是鞅；若E τ < ∞，停止后的过程被一个可积量控制，由可选停止（条件c）得E S_τ = μ E τ。
