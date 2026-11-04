# Quant, Built — Part 29: Alpha Mining and Automated Research

Part 29 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act IV, Return Premia (23–29), built to the series' PhD layer.
Part 26 taught the series to count its trials; this part builds machines that make trials by the thousand. Its mining
ground is Part 27's survivorship-free panel of every Binance USDT coin: research on 2018–2020, 2021–2025 sealed.
It covers:

* formulaic alphas (Kakushadze's 101) as trees in a small grammar, and the settings that turn a formula into a trade;
* the size of the search space (doubly exponential in depth) and how much of it is the same signal in disguise;
* random search against a pure-noise baseline and the winner's curse;
* genetic programming (Koza; Allen and Karjalainen), bloat and parsimony;
* reinforcement learning (AlphaGen's synergy reward), with a REINFORCE token generator built here and the policy
  gradient derived;
* LLM research agents (Alpha-GPT, AlphaAgent, R&D-Agent-Quant) and an honest protocol for testing them;
* combining weak alphas: the equal-weight IC ceiling c/√ρ, the participation ratio, equal against estimated weights;
* the trial counter, the independent-trials bar, and a shuffle null that keeps the trials' correlation;
* decay with the horizon and through time (McLean and Pontiff), crowding, and WorldQuant's alpha factory;
* China's quant industry: index enhancement, February 2024, the hedge's arithmetic; High-Flyer and DeepSeek;
* what remains for humans: priors (and the economics of the low-volatility effect), data, judgement;
* **for the researcher**: the out-of-sample Sharpe ratio of an estimated combination, SR*/√(1 + K/(T SR*²)), derived,
  stated as a limit, simulated, the bar for one more alpha, and checked on the mined alphas; open problems;
* the mined combination registered (13,010 trials) and opened on 2021–2025.

Every number is computed by the series' own code ([`compute.py`](compute.py) and the House's
[`alphas`](../../../explainer/quant/house/alphas.py) module). Data: Binance public daily candles for every USDT pair,
listed or delisted (Part 27's panel). Firms are described from the public record only.

*An education in methods, not investment advice.*

## Chapters (about 56 minutes)

* **Hook: ten thousand formulas** (2.7). Sixty random formulas; the best of N climbing to an IC of 0.080 by ten
  thousand; three questions (is it real, how many ideas, how many tries); history from Koza to AlphaAgent; the plan.
* **1. Formulaic alphas** (3.5). Kakushadze (2016): 101 alphas, average pairwise correlation 15.9%, holding 0.6–6.4
  days; the grammar; Alpha#12 as a tree; delay, neutralisation, rank weights and decay; the coin panel (171 coins
  eligible in 2018–20, a median of 34 a day); Alpha#12, #41 and #101 on coins: −0.023, −0.019, −0.014 on 2018–19;
  +0.009, +0.031, −0.040 on 2020.
* **2. The search space** (2.3). N_d = N_1 + 5N_{d−1} + 28N_{d−1} + 8N_{d−1}²: 6, 492, 1.95 million, 3.1 × 10¹³,
  7.4 × 10²⁷, 4.4 × 10⁵⁶ by depth; Koza's grow method from the House's source; of 10,000 random draws 5,712 distinct
  formulas and 2,792 distinct scores.
* **3. Random search and the winner's curse** (3.8). 10,000 formulas to depth 4, signed by training IC; the
  best are one idea written several ways (vwap/low); against 300 pure-noise signals (median |IC| 0.007) the formulas'
  median is 0.042; 2018–19 against 2020: correlation 0.53, 85% kept their sign, above all a low-volatility pattern;
  the best of N: 0.080 on training against a noise bar of 0.045, 0.072 on 2020; the top 100 kept 82% (0.063 → 0.052);
  the shrinkage formula; the danger is redundancy, not luck.
* **4. Genetic programming** (4.0). Crossover drawn; fitness |IC| − 0.0005 × size, tournaments of 5, 70/20/10, 100 × 25,
  elitism; three runs: the highest climber 0.168 → 0.021 on 2020 (bloat to 12 nodes), the others 0.074 → 0.063 on
  average; random search against GP at equal budgets; champions: smoothed minimum dollar volume (size) and mean low/high (calm); Allen and Karjalainen (1999), whose rules also timed low volatility.
* **5. Reinforcement learning: AlphaGen** (3.5). Yu, Xue, Ao, Pan, He, Tu and He (KDD 2023); reverse Polish tokens with a
  validity mask; the synergy reward; REINFORCE and the policy gradient (log-derivative trick, the baseline); 1,500
  episodes, 808 distinct formulas; the pool of ten: 0.101 → 0.060 on 2020 (t = 6.4).
* **6. LLM research agents** (2.7). The loop; Alpha-GPT (Wang et al. 2023; top 10 of 41,000+ IQC teams, as reported);
  AlphaAgent (Tang et al. 2025; AST originality); R&D-Agent-Quant (Li et al., NeurIPS 2025; up to 2× returns with 70%
  fewer factors, as reported); three cautions; a four-rule protocol. No agent was run here.
* **7. Combining weak alphas** (3.1). c√(N/(1 + (N − 1)ρ)) → c/√ρ; the top 40 alphas: ρ̄ = 0.55, the first
  eigenvalue 59% of the total, participation ratio 2.7; equal against mean-variance weights by K: estimated 2.05 → 2.68
  in sample, −0.10 on 2020 with 40; equal weights 1.13 with 40, better at every K above 1.
* **8. The counter explodes** (3.3). The counter by part (346 → 10,346 at Part 26 → 23,478); this part's 13,010
  trials (10,000 random, 2,196 GP, 808 RL, 6 combinations); √(2 ln N)/√T = 2.51 against the combination's in-sample
  2.17; three qualifications; the shuffle null: one daily permutation of next-day returns shared by 500 formulas gives a mean best |IC| of 0.029 against 0.037 for independent trials, about 32 effective trials (6%); scaled to the search, about 820 and a bar of 2.11, which 2.17 just clears.
* **9. Decay, crowding and the alpha factory** (3.4). The best formula's IC by day ahead: 0.080 → 0.063 at 10 days
  (2020: 0.072 → 0.059); by year 0.080, 0.079, 0.072; a model of decay, turnover and cost; McLean and Pontiff (2016):
  −26% out of sample, −58% after publication; speed: rank autocorrelation 0.992 and turnover 0.20 a day for the mined alpha against about 0 and 2.3–2.7 for Alpha#12, #41, #101 (about 4% against 42% a year at 10 bp); WorldQuant and BRAIN (public record); crowding.
* **10. China's quant industry** (3.1). Index enhancement (指数增强) on the CSI 500 and 1000; February 2024 (micro-caps
  −31% in five days, DMA swaps, accounts frozen on 20 February, CSI 1000 quant funds −14% in H1, as reported); Ningbo Lingjun (2.57 billion yuan sold in a minute on 19 February,
  barred 20–22 February, public record); the hedge's arithmetic; three lessons.
* **11. From a quant fund to DeepSeek** (1.7). High-Flyer (幻方), Fire-Flyer clusters, DeepSeek (public record); Fire-Flyer 2 (arXiv 2408.14158: 10,000 PCIe A100s, about half the cost, as reported).
* **12. What remains for humans** (2.4). The prior, the data, the judgement; √(2 ln N): 4.3 at 10⁴, 3.0 at 10²; why
  calm might beat wild (Frazzini–Pedersen; Bali–Cakici–Whitelaw) and what a prior must predict; when to stop searching.
* **13. The mined combination, registered and opened** (4.2). The 5 best random formulas, mean-variance weights on
  2018–20 (K chosen on 2020), 10 bp a round trip on the measured turnover (0.38 a day); research 1.73 ± 0.54 (0.88
  net); 2021–25: 2.78 ± 0.71 before costs, 1.64 net, worst fall 7.3%, positive every year (1.4 to 4.9); the coin
  market −0.43; break-even 24 bp, 0.51 at 20 bp; β = −0.02, hedged 3.53; 50 envelopes: bar 2.8 s.e., 3.9 gross, 2.3
  net; the five formulas and their weights; what it is, why it may not be money; what a desk would do next.
* **14. Rule 29: the alpha factory** (2.7). The sheet; `evaluate` from the House's source; the module; Rule 29; three
  cases.
* **For the researcher: how many alphas can you combine?** (5.7). Setup (r_t ~ N(μ, Σ), w* = Σ⁻¹μ, SR*² = ‖θ‖²);
  the derivation (z = θ + ε/√T, SR(ŵ) = z'θ/‖z‖); the in-sample mirror (‖z‖ ≈ √(SR*² + K/T)); the limit for K/T → γ (Brown 1976; Kan and Zhou 2007 for estimated
  Σ); simulations for T = 250, 500, 1,000 and K up to 80 (formula 0.081 against 0.081 simulated at K = 40, T = 250); the Wishart bias (T − 1)/(T − K − 2) and the second noise (0.114 against 0.095 at K = 80);
  the bar s² > S/(TS + 2K) and the best K = 5 for 1/√k signals; the mined alphas; three open problems.
* **Recap, desk questions, problems** (3.7). Fourteen lines; six desk questions; twelve problems (two at
  qualifying-exam level), solutions below.

## Hands-on

* Built and run here: random search over 10,000 formulas; three genetic-programming runs; a GRU REINFORCE generator
  with AlphaGen's synergy reward; equal, mean-variance and shrunk combinations; a shuffle null over 500 formulas.
* Labs: `random_tree` and `evaluate`, from the House's source.
* Simulations against theory: the out-of-sample Sharpe ratio of plug-in combinations (known and estimated Σ).

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| Kakushadze and Serur, *151 Trading Strategies* (2018) | the formulaic-alpha and stat-arb chapters | 1, 7, 9 |
| Isichenko, *Quantitative Portfolio Management* (2021) | ch. 2 (forecasting, alpha combination), ch. 3 (overfitting, multiple testing) | 3, 7, 8, research |
| Koza, *Genetic Programming* (1992) | the grow method, crossover, bloat | 2, 4 |
| Sutton and Barto, *Reinforcement Learning* (2018) | ch. 13 (policy gradients, REINFORCE with baseline) | 5 |

## Papers, chapter by chapter

* ch. 1: Kakushadze (2016), "101 formulaic alphas", *Wilmott* 84.
* ch. 2: Koza (1992).
* ch. 3: Harvey and Liu (2015); Part 26's sources.
* ch. 4: Koza (1992); Allen and Karjalainen (1999), *JFE* 51.
* ch. 5: Yu, Xue, Ao, Pan, He, Tu and He (2023), KDD, arXiv 2306.12964; Williams (1992), *Machine Learning* 8.
* ch. 6: Wang et al. (2023), Alpha-GPT, arXiv 2308.00016; Tang et al. (2025), AlphaAgent, arXiv 2502.16789; Li et al.
  (2025), R&D-Agent-Quant, arXiv 2505.15155.
* ch. 8: López de Prado and Lewis (2019), *Quantitative Finance* 19.
* ch. 9: McLean and Pontiff (2016), *JF* 71; Tulchinsky et al., *Finding Alphas* (2015; 2nd ed. 2019); WorldQuant press
  releases (2022–23).
* ch. 10–11: Reuters, Bloomberg and Caixin reporting on February 2024; company statements and press reports on High-Flyer
  and DeepSeek; DeepSeek-AI (2024), the V3 technical report.
* ch. 12: Frazzini and Pedersen (2014), *JFE* 111; Bali, Cakici and Whitelaw (2011), *JFE* 99.
* Research: Brown (1976); Kan and Zhou (2007), *JFQA* 42.

## For the researcher

* **The theorem.** For r_t ~ N(μ, Σ) i.i.d. in R^K with Σ known, the plug-in weights Σ⁻¹μ̂ have out-of-sample Sharpe
  ratio z'θ/‖z‖ with z = θ + ε/√T; as K, T → ∞ with K/T → γ, it converges in probability to SR*/√(1 + γ/SR*²).
  Brown (1976) introduced estimation risk in portfolio choice; Kan and Zhou (2007) give the exact finite-sample loss
  when Σ is estimated too.
* **Simplifications.** The research chapter's simulations use independent alphas of equal strength (and 1/√k strength
  for the bar); the mined alphas are far from independent, so the formula's numbers do not transfer, only its
  direction. The miners here are small: 10,000 random formulas, three GP runs of 100 × 25, 1,500 RL episodes; IC on
  ranks; no industry neutralisation (coins have none); costs a flat 10 bp a round trip; trades at the close the signal
  uses.
* **Open problems.** The joint correction for alphas selected on the same data that estimate their weights; the
  trade-off between sample size and staleness when edges decay; optimal joint shrinkage of means and covariance for
  many weak, correlated alphas.

## Build it

```bash
python -m videos.quant.quant29.compute                            # every item; random ~15 min, GP ~5, RL ~6 on 2 cores
python -m pytest -q tests/test_quant_house.py -k "alphas or combination"
EXPLAINER_TTS=silent python tools/qa_scene.py quant29 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant29                                      # the narrated part
```

## Desk questions, with solutions

1. **10,000 alphas, IC 0.01, correlation 0.3.** Equal weights give c√(N/(1 + (N − 1)ρ)) = 0.01 × √(10,000/3,000.7) ≈
   0.018, about c/√ρ: the count hardly matters past a few dozen; ten thousand such alphas are worth 1/ρ ≈ 3.3
   independent ones.
2. **A GP run with training IC 0.08.** Ask for the number of distinct trees it evaluated (the hurdle grows like
   √(2 ln N)), then for the IC on a period no generation saw; and how the champion was chosen among runs (Chapter 4's
   pause: choosing on 2020 makes 2020 part of the training).
3. **An agent's Sharpe 3 on 2015–2022 A-shares.** Check the language model's training cut-off against the test period;
   count every loop; re-run on data after the cut-off (Chapter 6's protocol).
4. **Forty alphas at Sharpe 6 in sample with estimated weights.** Expect much less: estimated weights fit noise in every
   direction (the research chapter); here 2.68 in sample became −0.10 on 2020 while equal weights held 1.13.
5. **A small-cap book short large-cap futures.** It is long the size spread r_small − r_index (and the futures basis),
   which widens when crowded books unwind; with leverage L the loss is L times the spread's fall (February 2024).
6. **The fiftieth alpha, Sharpe 0.3 a year.** Add it only if s² > S/(TS + 2K) for the library's S, K and T, and if its
   residual against the library, not its own Sharpe ratio, survives out of sample.

## Problems, with solutions

1. **Small trees.** N_1 = 6; N_2 = 6 + 5·6 + 7·4·6 + (4 + 4)·6² = 6 + 30 + 168 + 288 = 492.
2. **The best noise IC.** s.e. = 0.10/√500 = 0.0045; with both signs, the best of 10,000 is about 0.0045 × √(2 ln
   20,000) = 0.0045 × 4.45 ≈ 0.020.
3. **IC to Sharpe.** IR ≈ 0.02 × √100 = 0.2 a day, ≈ 0.2 × √365 ≈ 3.8 a year: the fundamental law (Part 31), which
   assumes independent bets.
4. **The equal-weight IC.** Cov(Σs_i, r) = Nc and Var(Σs_i) = N + N(N − 1)ρ, so Corr = c√(N/(1 + (N − 1)ρ)) =
   0.01 × √(10,000/3,000.7) ≈ 0.0183.
5. **Bloat's price.** 10 × 0.0005 = 0.005 of training IC.
6. **An agent's trials.** 500 × 4 = 2,000 trials; √(2 ln 2,000) = 3.90 against √(2 ln 500) = 3.53: the bar rises by
   0.37 standard errors.
7. **The baseline.** E[∇log π(a) b] = b Σ_a π(a)∇log π(a) = b Σ_a ∇π(a) = b∇Σ_a π(a) = b∇1 = 0.
8. **The February hedge.** −20% − (−5%) = −15% per unit of gross long (more with leverage or a widening futures
   discount).
9. **Half-life.** 0.03 × 2^(−t/2) < 0.01 ⇔ t > 2 log₂3 ≈ 3.2 years.
10. **The formula by hand.** SR* = 0.02√20 = 0.0894 a day (1.71 a year); K/(T SR*²) = 20/(365 × 0.008) = 6.85; SR_oos
    = 0.0894/√7.85 = 0.032 a day, about 0.61 a year.
11. **(qual) Estimated combinations.** With Σ known, whiten: z = Σ^{1/2}ŵ = Σ^{−1/2}μ̂ = θ + ε/√T, ε ~ N(0, I_K). For any
    w, SR(w) = w'μ/√(w'Σw) = (Σ^{1/2}w)'θ/‖Σ^{1/2}w‖, so SR(ŵ) = z'θ/‖z‖. Now z'θ = ‖θ‖² + θ'ε/√T = ‖θ‖² + O_p(‖θ‖/√T)
    and ‖z‖² = ‖θ‖² + 2θ'ε/√T + ‖ε‖²/T with ‖ε‖²/T = K/T + O_p(√K/T) → γ; with ‖θ‖ = SR* fixed, SR(ŵ) →
    SR*²/√(SR*² + γ) = SR*/√(1 + γ/SR*²). For f(S, K) = S/√(S + K/T): ∂f/∂S = (S/2 + K/T)(S + K/T)^{−3/2},
    ∂f/∂K = −(S/(2T))(S + K/T)^{−3/2}; adding s² to S and 1 to K helps to first order iff s²(S/2 + K/T) > S/(2T), i.e.
    s² > S/(TS + 2K).
12. **(qual) The best combination's IC.** For weights w, Corr(w's, r) = w'c/√(w'Cw); by Cauchy–Schwarz in the C inner
    product, w'c = (C^{1/2}w)'(C^{−1/2}c) ≤ √(w'Cw)√(c'C⁻¹c), with equality at w ∝ C⁻¹c: the maximum is √(c'C⁻¹c). For
    C = (1 − ρ)I + ρ11' and c = c1, C⁻¹1 = 1/(1 + (N − 1)ρ) · 1, so c'C⁻¹c = Nc²/(1 + (N − 1)ρ), the equal-weight value
    of Problem 4: with symmetric signals, equal weights are optimal.

## Data and reproducibility

* Binance public daily candles (spot, USDT quote) for every pair listed or delisted, Part 27's panel; the research grid
  is 2018–2020 plus 30 days of warm-up, coins counted on a day when listed 60 days with a median 28-day quote volume of
  at least 250,000 USDT; cached and checked by SHA-256 in `videos/quant/data/manifest.json`.
* Registered: `mined_combination_part29` (13,010 trials); the counter goes from 10,468 to 23,478; the hold-out
  (`binance/usdt_daily_returns`) sealed and opened once. The Track Record row: research 1.73 ± 0.54 (0.88 net),
  hold-out 2.78 ± 0.71 (1.64 net).
* Quoted, not computed: Kakushadze's statistics; Allen and Karjalainen's, AlphaGen's, Alpha-GPT's, AlphaAgent's,
  R&D-Agent-Quant's and McLean–Pontiff's results; WorldQuant's platform figures; the February 2024 figures and the
  High-Flyer and DeepSeek history, as reported.
* Simulated or illustrative: the crossover and token-stack pictures; the research chapter's alpha worlds.
* Running external code or models (open-weight LLM agents) was not part of this build; the miners here are the House's
  own.

---

# 量化金融，从零搭建 — 第29部分：阿尔法挖掘与自动化研究

本系列共四十三部分，这是第四幕"收益溢价"（第23–29部分）的最后一部分，按本系列的博士层次标准构建。第26部分教会本系列记录试验次数；本部分搭建成千上万次地制造试验的机器。挖掘场是第27部分那块没有幸存者偏差的面板：币安每一个以USDT报价的币；2018–2020年用于研究，2021–2025年密封。

*这是方法的教育，不是投资建议。*

## 章节（约56分钟）

* **开篇：一万个公式。** 六十个随机公式；N个中最好的那个在一万个时信息系数爬升到0.080；三个问题（是真的吗、有多少个想法、试了多少次）；从Koza到AlphaAgent的历史；本部分的计划。
* **1. 公式化阿尔法。** Kakushadze（2016）：101个阿尔法，两两平均相关15.9%，持有0.6–6.4天；语法；画成树的第12号阿尔法；滞后、中性化、秩权重与衰减；币的面板（2018–20年间171个币曾经合格，每天中位数34个）；第12、41、101号阿尔法在币上：2018–19年为−0.023、−0.019、−0.014；2020年为+0.009、+0.031、−0.040。
* **2. 搜索空间。** N_d = N_1 + 5N_{d−1} + 28N_{d−1} + 8N_{d−1}²：按深度依次为6、492、195万、3.1 × 10¹³、7.4 × 10²⁷、4.4 × 10⁵⁶；本系列公司源码中Koza的生长法；一万次随机抽取中有5,712个不同的公式、2,792个不同的得分。
* **3. 随机搜索与赢家诅咒。** 一万个深度不超过4的公式，按训练期信息系数定符号；最好的那些是同一个想法的几种写法（vwap/low）；与300个纯噪声信号相比（|IC|中位数0.007），公式的中位数是0.042；2018–19对2020：相关0.53，85%保持符号，首先是一种低波动率模式；N个中最好的：训练期0.080，噪声门槛0.045，2020年0.072；前100个保留了82%（0.063 → 0.052）；收缩公式；危险在于冗余，而不是运气。
* **4. 遗传规划。** 交叉示意；适应度|IC| − 0.0005 × 节点数，5个一组的锦标赛，70/20/10，100 × 25，精英保留；三次运行：爬得最高的那次在2020年从0.168跌到0.021（膨胀到12个节点），另外两次平均0.074 → 0.063；相同预算下随机搜索与遗传规划的比较；冠军：平滑后的最低成交额（规模）与最低价/最高价的均值（平静）；Allen与Karjalainen（1999），他们的规则也在择时低波动率。
* **5. 强化学习：AlphaGen。** Yu、Xue、Ao、Pan、He、Tu与He（KDD 2023）；带有效性掩码的逆波兰词元；协同奖励；REINFORCE与策略梯度（对数导数技巧、基线）；1,500个回合，808个不同的公式；十个公式的池子：2020年0.101 → 0.060（t = 6.4）。
* **6. 大语言模型研究智能体。** 循环；Alpha-GPT（Wang等 2023；据报道在IQC四万一千多支队伍中进入前十）；AlphaAgent（Tang等 2025；语法树原创性）；R&D-Agent-Quant（Li等，NeurIPS 2025；据报道收益最高两倍、因子少70%）；三点警示；四条规则的检验协议。这里没有运行任何智能体。
* **7. 组合弱阿尔法。** c√(N/(1 + (N − 1)ρ)) → c/√ρ；前40个阿尔法：平均相关0.55，第一特征值占总和的59%，参与比2.7；按K比较等权与均值-方差权重：估计权重样本内2.05 → 2.68，40个时2020年为−0.10；等权40个时为1.13，在K大于1的每一种规模上都更好。
* **8. 计数器爆炸。** 各部分的计数器（346 → 第26部分10,346 → 23,478）；本部分13,010次试验（10,000个随机、2,196个遗传规划、808个强化学习、6个组合）；√(2 ln N)/√T = 2.51，对比组合样本内的2.17；三点限定；打乱零假设：对500个公式共用同一个次日收益的每日置换，最好|IC|的均值为0.029，而独立试验时为0.037，约相当于32次有效试验（6%）；推广到整个搜索，约820次，门槛2.11，2.17恰好越过。
* **9. 衰减、拥挤与阿尔法工厂。** 最好的公式按未来第几天的信息系数：0.080 → 第10天0.063（2020年：0.072 → 0.059）；逐年0.080、0.079、0.072；衰减、换手与成本的模型；McLean与Pontiff（2016）：样本外−26%，发表后−58%；速度：挖出的阿尔法秩自相关0.992、每天换手0.20，第12、41、101号阿尔法约为0和2.3–2.7（按10个基点每年约4%对42%）；WorldQuant与BRAIN（公开记录）；拥挤。
* **10. 中国的量化行业。** 中证500与1000上的指数增强；2024年2月（据报道微盘股五天下跌31%、DMA互换、2月20日账户被冻结、跟踪中证1000的量化基金上半年−14%）；宁波灵均（2月19日一分钟内卖出25.7亿元，2月20–22日被限制交易，公开记录）；对冲的算术；三个教训。
* **11. 从量化基金到DeepSeek。** 幻方、萤火集群、DeepSeek（公开记录）；萤火二号（arXiv 2408.14158：一万块PCIe A100，据报道成本约为一半）。
* **12. 留给人的是什么。** 先验、数据、判断；√(2 ln N)：10⁴时4.3，10²时3.0；为什么平静可能胜过狂野（Frazzini–Pedersen；Bali–Cakici–Whitelaw），以及一个先验必须预测什么；何时停止搜索。
* **13. 挖掘出的组合，登记并打开。** 最好的5个随机公式，在2018–20年上估计均值-方差权重（K在2020年上选定），按实测换手（每天0.38）每个来回10个基点；研究期1.73 ± 0.54（扣成本后0.88）；2021–25年：扣成本前2.78 ± 0.71，扣成本后1.64，最大回撤7.3%，每年为正（1.4到4.9）；币市本身−0.43；盈亏平衡成本24个基点，20个基点时0.51；β = −0.02，对冲后3.53；50个信封：门槛2.8个标准误，扣成本前3.9，扣成本后2.3；五个公式及其权重；它是什么，为什么它可能不是钱，以及交易台接下来会做什么。
* **14. 第29条规则：阿尔法工厂。** 第一张表；本系列公司源码中的`evaluate`；模块；第29条规则；三个案例。
* **写给研究者：能组合多少个阿尔法？** 设定（r_t ~ N(μ, Σ)，w* = Σ⁻¹μ，SR*² = ‖θ‖²）；推导（z = θ + ε/√T，SR(ŵ) = z'θ/‖z‖）；样本内的镜像（‖z‖ ≈ √(SR*² + K/T)）；K/T → γ时的极限（Brown 1976；协方差也估计时见Kan与Zhou 2007）；T = 250、500、1,000、K至80的模拟（K = 40、T = 250时公式0.081，模拟0.081）；Wishart偏差(T − 1)/(T − K − 2)与第二种噪声（K = 80时0.114对0.095）；门槛s² > S/(TS + 2K)，以及1/√k信号的最佳K = 5；挖出的阿尔法；三个开放问题。
* **回顾、交易台问题与习题。** 十四行回顾；六个交易台问题；十二道习题（两道为资格考试难度），解答见下文。

## 写给研究者

* **定理。** 对R^K中独立同分布的r_t ~ N(μ, Σ)且Σ已知，插入式权重Σ⁻¹μ̂的样本外夏普比率为z'θ/‖z‖，其中z = θ + ε/√T；当K, T → ∞且K/T → γ时，它依概率收敛到SR*/√(1 + γ/SR*²)。Brown（1976）把估计风险引入组合选择；Kan与Zhou（2007）给出协方差也被估计时精确的有限样本损失。
* **简化。** 研究章的模拟使用强度相同的独立阿尔法（门槛部分用强度1/√k）；挖出的阿尔法远非独立，所以公式的数字不能照搬，只有方向成立。这里的挖掘器规模很小：一万个随机公式，三次100 × 25的遗传规划运行，1,500个强化学习回合；信息系数基于秩；没有行业中性化（币没有行业）；成本统一为每个来回10个基点；在信号所用的收盘价成交。
* **开放问题。** 在估计其权重的同一份数据上被选出的阿尔法的联合修正；优势衰减时样本量与陈旧之间的权衡；对许多弱且相关的阿尔法，均值与协方差的最优联合收缩。

## 交易台问题与解答

1. **一万个阿尔法，信息系数0.01，相关0.3。** 等权给出c√(N/(1 + (N − 1)ρ)) = 0.01 × √(10,000/3,000.7) ≈ 0.018，约为c/√ρ：过了几十个之后数量几乎无关紧要；一万个这样的阿尔法只相当于1/ρ ≈ 3.3个独立的。
2. **训练信息系数为0.08的遗传规划运行。** 问它评估了多少棵不同的树（门槛像√(2 ln N)那样增长），再问它在没有哪一代见过的时期上的信息系数；以及冠军是如何在多次运行之间选出的（第4章的暂停题：按2020年选，2020年就成了训练的一部分）。
3. **智能体在2015–2022年A股上的夏普比率为3。** 对照检验期检查语言模型的训练截止日期；计入每一轮循环；在截止日期之后的数据上重跑（第6章的协议）。
4. **估计权重下样本内夏普比率为6的四十个阿尔法。** 预期会少得多：估计权重在每个方向上拟合噪声（研究章）；这里样本内的2.68在2020年变成−0.10，而等权守住了1.13。
5. **做空大盘期货的小盘组合。** 它做多规模价差r_small − r_index（以及期货基差），而拥挤的组合平仓时这个价差会扩大；杠杆为L时，损失是价差下跌的L倍（2024年2月）。
6. **第五十个阿尔法，年化夏普比率0.3。** 只有当s² > S/(TS + 2K)（用库的S、K与T），并且它相对于库的残差（而不是它自己的夏普比率）在样本外站得住时，才加入。

## 习题与解答

1. **小树。** N_1 = 6；N_2 = 6 + 5·6 + 7·4·6 + (4 + 4)·6² = 6 + 30 + 168 + 288 = 492。
2. **最好的噪声信息系数。** 标准误 = 0.10/√500 = 0.0045；两个符号都算，一万个中最好的约为0.0045 × √(2 ln 20,000) = 0.0045 × 4.45 ≈ 0.020。
3. **从信息系数到夏普比率。** IR ≈ 0.02 × √100 = 每天0.2，≈ 0.2 × √365 ≈ 每年3.8：这是基本定律（第31部分），它假设各次押注相互独立。
4. **等权信息系数。** Cov(Σs_i, r) = Nc，Var(Σs_i) = N + N(N − 1)ρ，所以Corr = c√(N/(1 + (N − 1)ρ)) = 0.01 × √(10,000/3,000.7) ≈ 0.0183。
5. **膨胀的代价。** 10 × 0.0005 = 训练信息系数0.005。
6. **智能体的试验。** 500 × 4 = 2,000次试验；√(2 ln 2,000) = 3.90，对比√(2 ln 500) = 3.53：门槛升高0.37个标准误。
7. **基线。** E[∇log π(a) b] = b Σ_a π(a)∇log π(a) = b Σ_a ∇π(a) = b∇Σ_a π(a) = b∇1 = 0。
8. **2月的对冲。** −20% − (−5%) = 每单位多头总额−15%（有杠杆或期货贴水扩大时更多）。
9. **半衰期。** 0.03 × 2^(−t/2) < 0.01 ⇔ t > 2 log₂3 ≈ 3.2年。
10. **手算公式。** SR* = 0.02√20 = 每天0.0894（每年1.71）；K/(T SR*²) = 20/(365 × 0.008) = 6.85；SR_oos = 0.0894/√7.85 = 每天0.032，每年约0.61。
11. **（资格考试）估计组合。** Σ已知时做白化：z = Σ^{1/2}ŵ = Σ^{−1/2}μ̂ = θ + ε/√T，ε ~ N(0, I_K)。对任意w，SR(w) = w'μ/√(w'Σw) = (Σ^{1/2}w)'θ/‖Σ^{1/2}w‖，所以SR(ŵ) = z'θ/‖z‖。而z'θ = ‖θ‖² + θ'ε/√T = ‖θ‖² + O_p(‖θ‖/√T)，‖z‖² = ‖θ‖² + 2θ'ε/√T + ‖ε‖²/T，其中‖ε‖²/T = K/T + O_p(√K/T) → γ；保持‖θ‖ = SR*不变，SR(ŵ) → SR*²/√(SR*² + γ) = SR*/√(1 + γ/SR*²)。对f(S, K) = S/√(S + K/T)：∂f/∂S = (S/2 + K/T)(S + K/T)^{−3/2}，∂f/∂K = −(S/(2T))(S + K/T)^{−3/2}；给S加s²、给K加1，一阶意义下有帮助当且仅当s²(S/2 + K/T) > S/(2T)，即s² > S/(TS + 2K)。
12. **（资格考试）最优组合的信息系数。** 对权重w，Corr(w's, r) = w'c/√(w'Cw)；在C内积下用柯西–施瓦茨不等式，w'c = (C^{1/2}w)'(C^{−1/2}c) ≤ √(w'Cw)√(c'C⁻¹c)，在w ∝ C⁻¹c时取等号：最大值为√(c'C⁻¹c)。对C = (1 − ρ)I + ρ11'与c = c1，C⁻¹1 = 1/(1 + (N − 1)ρ) · 1，所以c'C⁻¹c = Nc²/(1 + (N − 1)ρ)，即第4题的等权值：信号对称时，等权就是最优的。

## 数据与复现

* 币安公开的日K线（现货，USDT报价），覆盖每一个在市或已下市的交易对，即第27部分的面板；研究网格为2018–2020年加30天预热，一个币在某天被计入的条件是已上市60天且28天成交额中位数不低于250,000 USDT；已缓存，并在`videos/quant/data/manifest.json`中用SHA-256校验。
* 本部分登记：`mined_combination_part29`（13,010次试验）；计数器从10,468升到23,478；样本外数据（`binance/usdt_daily_returns`）已封存并只打开一次。业绩记录这一行：研究期1.73 ± 0.54（扣成本后0.88），样本外2.78 ± 0.71（扣成本后1.64）。
* 引用而非计算的结果：Kakushadze的统计；Allen与Karjalainen、AlphaGen、Alpha-GPT、AlphaAgent、R&D-Agent-Quant以及McLean–Pontiff的结果；WorldQuant的平台数字；2024年2月的数字，以及幻方与DeepSeek的经历，均据报道。
* 模拟或示意：交叉与词元栈的图示；研究章中的阿尔法世界。
* 本次构建没有运行外部代码或模型（开放权重的大语言模型智能体）；这里的挖掘器是本系列公司自己的。
