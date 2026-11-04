# Quant, Built — Part 27: Machine Learning for Returns

Part 27 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth part of Act IV, Return Premia (23–29), and the first built to the series'
PhD layer. Part 26 built the machine that keeps a backtest honest; this part runs every learner of the empirical
asset-pricing literature through it. It covers:

* why returns are a low signal-to-noise problem, and the arithmetic of breadth that makes a tiny $R^2$ valuable;
* Gu, Kelly and Xiu's model zoo (OLS, elastic net, PCR, PLS, boosted trees, networks of one to three layers) on a
  survivorship-free panel of every coin Binance has quoted in USDT, with a power analysis of the test;
* where the edge lives (Avramov, Cheng and Metzker; Leippold, Wang and Zhou): liquid against illiquid, gross against
  net;
* the virtue of complexity (Kelly, Malamud and Zhou), double descent, and Nagel's critique;
* **for the researcher**: the Marchenko–Pastur law, the exact ridge and ridgeless risk of Hastie, Montanari, Rosset
  and Tibshirani, the misspecified model in which size pays, random features converging to their kernel; each
  checked against simulation; open problems;
* conditional autoencoders and their linear special case, instrumented PCA; deep SDFs with adversarial moments, and
  why the SDF is the tangency portfolio; attention across assets and permutation equivariance; CNNs on chart images;
* foundation models (Chronos, TimesFM, Kronos) and a pocket model of the House's own, tested zero-shot;
* Lopez de Prado's toolkit (dollar bars, fractional differencing, triple-barrier labels, meta-labelling,
  uniqueness weights), each tested against the simple thing it replaces;
* split and adaptive conformal prediction;
* Two Sigma and Renaissance from the public record;
* two strategies registered (25 and 84 trials) and opened on 2021–2025.

Every number is computed by the series' own code ([`compute.py`](compute.py) and the House's
[`ml`](../../../explainer/quant/house/ml.py) module). Data: Binance's public archive of daily candles for every USDT
pair, listed or delisted (701 symbols, 566 with at least 30 days); Amit Goyal's update of the Welch–Goyal predictors;
Yahoo Finance daily bars for SPY, QQQ, EEM, GLD and XLE.

*An education in methods, not investment advice.*

## Chapters

* **Four tenths of a percent** (hook). Gu, Kelly and Xiu (2020): NN3 explains 0.40% of a stock's monthly return
  variance, yet its long-short earns 1.35 (value-weighted) and 2.45 (equal-weighted). Timing one asset at
  $R^2 = 1\%$ is worth about a third; many independent bets multiply it by $\sqrt N$. The history strip, the plan,
  the House's model shop.
* **1. A low signal-to-noise world.** Fifteen Welch–Goyal predictors, 1926–2020, in sample: the best ($ltr$)
  explains 0.73% of next month's return. Israel, Kelly and Moskowitz's four reasons machine learning is hard in
  finance. A low-noise and a high-noise pattern; bias–variance; the out-of-sample $R^2$ against zero.
* **2. The model zoo.** The panel: 566 coins, 170 in 2018–2020 (62 since delisted), 5,997 coin-weeks; a universe
  rule of 60 days listed and \$250,000 a day; 2021–2025 sealed (about 300 coins a week). Fifteen ranked
  characteristics. Nine models; expanding-window protocol; the ensemble lab. Every $R^2$ is negative (−2.6% to
  −1.7%); quintile long-short Sharpe ratios from −1.37 (NN3) to 0.99 (GBRT), each $\pm 1.4$ at two standard errors.
  Power: $T \ge 4(1 + SR^2/2)/SR^2$ years. Importance: liquidity, size and age lead for OLS, GBRT and NN3.
* **3. Where the edge lives.** Avramov–Cheng–Metzker (2023); Leippold–Wang–Zhou (2022). Liquid half: average
  tercile Sharpe 0.00; illiquid half 0.17; six of nine models better there. Turnover at 10 bp costs 5–14% a year;
  at 50 bp five of nine lose. Three economic restrictions.
* **4. The virtue of complexity.** Kelly–Malamud–Zhou's random-feature ridge timer on the Welch–Goyal predictors,
  12-month windows: Sharpe 0.33 at $P = 12{,}000$, $z = 0.1$, against 0.52 for the volatility-scaled market;
  $R^2$ −42.5% at $P = T$ with almost no ridge, about +1% far beyond. Double descent on coins (1,000 coin-weeks):
  the ridgeless peak at $P = N$, gone with a little ridge.
* **5. The critics.** Nagel (2025): the dual form, the kernel limit, a similarity-weighted average of the last
  twelve returns; the exact kernel's median off-diagonal $\approx 10^{-5}$. The RFF timer (0.33) against 12-month
  momentum (0.40); correlation 0.32. In a simulated world built to reverse, the timer earns −0.28 where the reversal
  rule earns 1.05.
* **6. The theory of overparameterised prediction** (research chapter). The isotropic model; ridge and the
  pseudo-inverse. Marchenko–Pastur at $\gamma$ = 0.25, 0.8, 2 (the lower edge $(1 - \sqrt\gamma)^2$; the atom
  $1 - 1/\gamma$). The proof in five lines (bias and variance; rotation invariance; Marchenko–Pastur). The ridgeless
  limits $\sigma^2\gamma/(1 - \gamma)$ and $r^2(1 - 1/\gamma) + \sigma^2/(\gamma - 1)$; optimal ridge has no spike.
  Theory against simulation ($N = 200$, 30 draws): 4.0 against 3.88 at $\gamma = 0.8$; 1.17 against 1.17 at 3. The
  misspecified model ($P_{\text{total}} = 10N$, $r^2 = 2$): every $\gamma < 1$ is worse than zero (best 3.15
  against 3.00); ridgeless at $\gamma = 10$ reaches 2.91 ($R^2$ 3.0%), optimal ridge 4.3%. Random features: error
  $O(P^{-1/2})$ (0.014 at $P = 10$, 0.0003 at 30,000). Three open problems.
* **7. Autoencoder asset pricing.** The conditional factor model; managed portfolios (with the market); IPCA's
  alternating least squares and its PCA special case; the two-arm picture. Total $R^2$ on 2020: about 45% with one
  factor, 51.5% with five linear; CA1 and CA2 do not beat linear. Predictive $R^2$ about −2% everywhere: the premia
  were estimated on a market that fell 26% and then 57%, and applied to one that rose 143%.
* **8. Deep SDFs with adversarial moments.** Conditional moments as infinitely many unconditional ones; the SDF
  portfolio is the tangency portfolio (Sherman–Morrison) and Hansen–Jagannathan bounds every Sharpe ratio; the
  min–max game. On 2020: adversarial −1.53, linear 0.02, the market 1.58. The adversarial SDF's correlation with
  the market: −0.996 (the training market's mean was −40% a year).
* **9. Attention across assets.** Why cross-asset information; Kelly–Kuznetsov–Malamud–Xu (2025). Queries, keys,
  values; permutation equivariance and Deep Sets; uniform attention as cross-sectional demeaning. The House's
  attention is nearly flat (7.3% on the top five of 75 coins, 6.7% if uniform). Attention $R^2$ −9.7%, Sharpe
  −0.72; a same-width pointwise network −1.2%, 0.64.
* **10. Images of prices.** Jiang–Kelly–Xiu (2023) images (32 × 60). Convolution and cross-entropy. The paper's
  findings. On coins: 6,718 training images; accuracy 49.3% against a base rate of 52.5%; CNN long-short −0.50
  against 20-day momentum 2.64 in 2020; about 23,000 weights.
* **11. Foundation models.** Chronos, TimesFM, Kronos; tokens, next-token loss, sampled forecasts. Kronos's reported
  gains (RankIC +93% and +87%, volatility MAE −9%, synthetic fidelity +22%), not replicated here. The pocket model
  (an MLP on 60-day windows of $\log|r|$ from 172 coins, 19,011 windows), zero-shot on five ETFs from August 2015:
  EWMA (offset fitted) best everywhere ($R^2$ 2.8–9.0%); the pocket model 0–5.2%, beating HAR only on EEM.
* **12. The practitioner's toolkit.** Bitcoin 2018–2020: dollar bars cut excess kurtosis from 22.6 to 8.3 but
  raise squared-return autocorrelation (0.08 to 0.30). Fractional differencing passes the ADF test at $d = 0.3$
  ($-3.33$) keeping correlation 0.92 with the price (the return keeps 0.09). The triple barrier. Meta-labelling:
  precision 61% to 66% on 65% of the bets, reward per unit of risk unchanged (0.28). Uniqueness 0.115: 1,086 labels
  are worth about 125.
* **13. Conformal prediction.** Split conformal and its guarantee. The coin panel: 89.7% covered at 90%, 73.6% at
  80%; the March 2020 crash week 12%. Bitcoin: a fixed interval from the first 120 days (±10.4%) covers 98%, still
  missing four days of March 2020; adaptive conformal inference covers 89.7%, with widths from 2.5% to 11%.
* **14. From the public record: Two Sigma and Renaissance.** Medallion's reported 66% a year gross, 39% net,
  1988–2018 (Zuckerman); Two Sigma's founding, scale and self-description; the SEC's January 2025 order (\$90
  million penalty, \$165 million repaid to funds, model changes not supervised; allegations against individuals
  remain allegations). Breadth, capacity, models as controlled code.
* **15. The machine-learned strategies, registered and opened.** NN3 on coins (25 trials), registered before any
  research result: research −0.71, hold-out 1.29 ± 0.34 (1.13 net of 10 bp; equal-weighted −0.41; $R^2$ +0.3%);
  positive every year (0.75 to 2.42); 1.09 without its best five weeks; about 0.5 at 50 bp. Deflated: hurdle 0.89
  and DSR 0.81 for its own 25 trials, hurdle 1.73 and DSR 0.17 for the series' 10,455. The complexity timer
  (84 trials): research 0.33 ± 0.11, hold-out −0.17 ± 0.45 against the market's 0.72.
* **16. Rule 27: the model desk.** The sheet; the theorem in the House; the module; the rule.
* **Recap, desk questions, problems.**

## Hands-on

* Every model is trained here: the nine-model zoo with expanding refits, three autoencoders at five $K$, an
  adversarial SDF (three seeds), a transformer and its pointwise twin (three seeds), a chart CNN (three seeds), the
  pocket foundation model (three seeds), boosted trees for meta-labels.
* Labs: the network ensemble (`MLPEnsemble.fit`), the ridge risk theorem (`ridge_risk_theory`), and the toolkit's
  functions on screen.
* Simulations against theory: Marchenko–Pastur spectra, ridgeless and optimal-ridge risk, the misspecified model,
  random-feature kernel error.

## Textbook audit

| Textbook | Chapters | Where |
|---|---|---|
| Kelly and Xiu, *Financial Machine Learning* (2023) | return prediction (regularisation, dimension reduction, trees, networks, the virtue of complexity); factor models and SDFs (IPCA, autoencoders, adversarial SDFs); optimal portfolios (as Part 30); text (as Part 28) | ch. 1–9 |
| Lopez de Prado, *Advances in Financial Machine Learning* | 2 (bars), 3 (triple barrier, meta-labelling), 4 (uniqueness and sample weights), 5 (fractional differencing), 10 (bet sizing, as context) | ch. 12 |
| Hastie, Tibshirani and Friedman, *Elements of Statistical Learning* | 3 (ridge, lasso, PCR, PLS), 10 (boosting), 11 (networks) | ch. 2, 6 |
| Goodfellow, Bengio and Courville, *Deep Learning* | 6–9 (feed-forward, regularisation, optimisation, convolution) | ch. 2, 9, 10 |
| Isichenko, *Quantitative Portfolio Management* | 2 (forecasting, machine learning in practice) | ch. 1–3 |

## Papers, chapter by chapter

* Hook: Gu, Kelly and Xiu (2020); Grinold (1989).
* ch. 1: Welch and Goyal (2008); Campbell and Thompson (2008); Israel, Kelly and Moskowitz (2020).
* ch. 2: Gu, Kelly and Xiu (2020); Lo (2002).
* ch. 3: Avramov, Cheng and Metzker (2023); Leippold, Wang and Zhou (2022).
* ch. 4: Rahimi and Recht (2007); Belkin, Hsu, Ma and Mandal (2019); Kelly, Malamud and Zhou (2024).
* ch. 5: Nagel (2025).
* ch. 6: Marchenko and Pastur (1967); Dobriban and Wager (2018); Bartlett, Long, Lugosi and Tsigler (2020); Hastie,
  Montanari, Rosset and Tibshirani (2022); Mei and Montanari (2022); Giannone, Lenza and Primiceri (2021).
* ch. 7: Kelly, Pruitt and Su (2019); Gu, Kelly and Xiu (2021).
* ch. 8: Hansen and Jagannathan (1991); Chen, Pelger and Zhu (2024).
* ch. 9: Zaheer et al. (2017); Lee et al. (2019); Kelly, Kuznetsov, Malamud and Xu (2025).
* ch. 10: Jiang, Kelly and Xiu (2023).
* ch. 11: Ansari et al. (2024), Chronos; Das, Kong, Sen and Zhou (2024), TimesFM; Shi et al. (2025), Kronos.
* ch. 12: Lopez de Prado (2018).
* ch. 13: Vovk, Gammerman and Shafer (2005); Lei, G'Sell, Rinaldo, Tibshirani and Wasserman (2018); Gibbs and Candès
  (2021).
* ch. 14: Zuckerman (2019); SEC, *In the Matter of Two Sigma Investments, LP and Two Sigma Advisers, LP* (January
  2025).

## For the researcher

* **The ridge risk** (ch. 6) is exact in the proportional limit for isotropic Gaussian features (Hastie et al. 2022,
  Thm. 1 for ridgeless, Thm. 5 for ridge; Dobriban and Wager 2018 for general $\Sigma$ through the Stieltjes
  transform of the limiting spectrum). Non-isotropic $\Sigma$ changes the integrals to ones against the
  deterministic equivalent of $\hat\Sigma$; heavy tails and dependence are not covered.
* **The misspecified model** is Hastie et al.'s Section 5 in its simplest form (the unseen features as noise);
  Kelly, Malamud and Zhou (2024) prove the timing analogue with random features, where the Sharpe ratio of the
  timing strategy rises with complexity while the $R^2$ can be negative. Mei and Montanari (2022) give the exact
  risk of random-feature regression, which interpolates between the linear model and the kernel limit.
* **Simplifications.** The video treats the random-feature inner product's convergence pointwise; uniform
  convergence over a compact set holds with an extra $\sqrt{\log}$ factor (Rahimi and Recht). The attention
  "theorem" quotes Zaheer et al.'s characterisation for countable domains and continuous functions; the video's
  uniform-attention case is exact. The autoencoder's IPCA reduction assumes orthonormal characteristics each week.
  The SDF chapter uses unconditional second moments; Chen, Pelger and Zhu's macro-state LSTM is omitted.
* **Open problems** (ch. 6): dense against sparse predictability (Giannone, Lenza and Primiceri 2021); exact risk
  under dependence, heavy tails and decay; whether deep learning's gains in finance are kernel (NTK) or feature
  learning.

## Build it

```bash
python -m videos.quant.quant27.compute                           # every item; the coin grid takes ~20 min the first time
python -m pytest -q tests/test_quant_house.py -k "ml_ or ridge"  # the House's ml module, and the theorem against simulation
EXPLAINER_TTS=silent python tools/qa_scene.py quant27 Theory      # one chapter, silent, with a contact sheet
python tools/build.py quant27                                     # the narrated part
```

## Desk questions, with solutions

1. **500 stocks, out-of-sample $R^2$ of 0.5% a month: what long-short Sharpe ratio?** A forecast with correlation
   $\rho$ to the return gives each bet an information ratio of about $\rho/\sqrt{1 - \rho^2}$, with
   $\rho^2 = R^2$; with $N$ independent bets the portfolio's is $\sqrt N$ times that: $\sqrt{0.005/0.995} \approx
   0.071$, times $\sqrt{500} \approx 22.4$, times $\sqrt{12}$, is about 5.5 a year. Real errors share factors (the
   effective $N$ is the number of independent residual bets, often a few dozen), $R^2$ is uneven across stocks and
   time, and costs take a share: 1–2 is a good outcome, as Gu, Kelly and Xiu's 1.35 value-weighted shows.
2. **A million parameters, 10,000 observations, a perfect training fit. Useless?** No. With $\gamma = 100$ the
   minimum-norm interpolator's variance is $\sigma^2/(\gamma - 1)$, about 1% of $\sigma^2$; what matters is the bias
   (how much signal the features cannot see) and whether a ridge penalty does better. Ask for the ridge path, the
   out-of-sample risk against a simple baseline at the same budget, and the seeds' spread.
3. **55% directional accuracy: tradable?** Not by itself. If the up-moves it misses are larger than those it catches,
   55% loses money; the base rate may already be 55%; its bets may duplicate positions you hold; and turnover against
   costs decides the net. Measure the long-short's Sharpe ratio after costs, and its correlation with existing books.
4. **Two years, 40 coins, weekly, Sharpe 1.0: a 95% interval?** $\operatorname{se} \approx \sqrt{(1 + SR^2/2)/T} =
   \sqrt{1.5/2} \approx 0.87$, so about $1 \pm 1.7$: $-0.7$ to $2.7$. To tell 1 from 0.5 at two standard errors needs
   $\operatorname{se} \le 0.25$: $T \approx 1.5/0.0625 = 24$ years, or a cross-section with far more independent bets.
5. **A meta-model doubles precision but takes one bet in ten.** Expected profit per unit of risk decides. If the kept
   bets' mean over standard deviation exceeds the full set's by more than the loss of breadth (a factor of
   $\sqrt{10}$ in the Sharpe ratio, if bets are independent), it is better; otherwise not. Chapter 12's
   meta-labelling raised precision from 61% to 66% and left the ratio at 0.28. Decide on held-out data, net of costs.
6. **A conformal interval covered 90% in the 2010s and 70% in 2020.** The guarantee holds for exchangeable data; a
   regime change breaks exchangeability, so nothing is violated. Use adaptive conformal inference (long-run coverage
   under any drift), recalibrate on a rolling window, or condition on volatility (normalised residuals).

## Problems, with solutions

1. **(qual) Split conformal.** Let $R_1, \dots, R_n, R_{n+1}$ be the calibration scores and the new one, exchangeable.
   The rank of $R_{n+1}$ among them is uniform on $\{1, \dots, n + 1\}$ (ties broken at random). $y \in C(x)$ iff
   $R_{n+1} \le R_{(k)}$ with $k = \lceil (n+1)(1 - \alpha) \rceil$, which holds when the rank is at most $k$:
   probability $k/(n + 1) \ge 1 - \alpha$. Without ties, the event is exactly rank $\le k$, so the probability is
   $k/(n + 1) < (n + 1)(1 - \alpha)/(n + 1) + 1/(n + 1) = 1 - \alpha + 1/(n + 1)$.
2. **(qual) The exact OLS risk.** $\hat b - b = (X^{\top}X)^{-1}X^{\top}\varepsilon$, so $\mathbb E|\hat b - b|^2 =
   \sigma^2\, \mathbb E\operatorname{tr}(X^{\top}X)^{-1}$. $X^{\top}X$ is Wishart $W_P(I, N)$, whose inverse has mean
   $I/(N - P - 1)$ for $N > P + 1$. So the risk is $\sigma^2 P/(N - P - 1) \to \sigma^2\gamma/(1 - \gamma)$ as
   $P/N \to \gamma < 1$: Chapter 6's ridgeless formula, exact in finite samples.
3. **Ridge to the interpolator.** $\hat b_\lambda = X^{\top}(XX^{\top} + \lambda N I)^{-1}y$ (push-through identity).
   For $P > N$, $XX^{\top}$ is invertible almost surely, so as $\lambda \downarrow 0$, $\hat b_\lambda \to
   X^{\top}(XX^{\top})^{-1}y = X^{+}y$, which solves $Xb = y$ and lies in the row space of $X$, hence is the solution
   of least norm.
4. **Random features.** $\mathbb E\cos(w^{\top}\Delta) = \operatorname{Re}\,\mathbb E\, e^{i w^{\top}\Delta}$, the
   real part of the normal characteristic function at $\Delta$: $e^{-\gamma^2|\Delta|^2/2}$. The sin and cos pair
   gives $\sin a\sin b + \cos a\cos b = \cos(a - b)$, so $z(x)^{\top}z(y)$ is an average of such cosines.
5. **Adaptive conformal.** With $\alpha_{t+1} = \alpha_t + \gamma(\alpha - \mathrm{err}_t)$, summing gives
   $\alpha_{T+1} - \alpha_1 = \gamma\sum_t(\alpha - \mathrm{err}_t)$. The working level stays in
   $[-\gamma, 1 + \gamma]$ (below 0 the interval is infinite and never misses; above 1 it is empty and always misses),
   so $|\alpha_{T+1} - \alpha_1| \le \max(\alpha_1, 1 - \alpha_1) + \gamma$; divide by $\gamma T$.
6. **The SDF is the tangency portfolio.** $\mathbb E[(1 - w^{\top}R)R] = 0$ gives $\mu = (\Sigma + \mu\mu^{\top})w$.
   Sherman–Morrison: $(\Sigma + \mu\mu^{\top})^{-1}\mu = \Sigma^{-1}\mu/(1 + \mu^{\top}\Sigma^{-1}\mu)$. For any
   excess return $R_p$, $0 = \mathbb E[MR_p] = \mathbb E[M]\mathbb E[R_p] + \operatorname{cov}(M, R_p)$, so
   $|\mathbb E R_p|/\sigma(R_p) \le \sigma(M)/\mathbb E[M]$ (Hansen–Jagannathan).
7. **Two barriers.** For $X_t = \mu t + \sigma W_t$ from 0, $e^{-2\mu X_t/\sigma^2}$ is a martingale; optional stopping
   at the first exit of $(-b, b)$: $p\, e^{-2\mu b/\sigma^2} + (1 - p)\, e^{2\mu b/\sigma^2} = 1$, so
   $p = (e^{2\mu b/\sigma^2} - 1)/(e^{2\mu b/\sigma^2} - e^{-2\mu b/\sigma^2})$; $p = 1/2$ when $\mu = 0$.
8. **Fractional weights.** $w_k = (-1)^k\binom{d}{k} = \Gamma(k - d)/(\Gamma(-d)\Gamma(k + 1))$, and
   $\Gamma(k - d)/\Gamma(k + 1) \sim k^{-d-1}$, so $w_k \sim k^{-d-1}/\Gamma(-d)$, negative for $0 < d < 1$ since
   $\Gamma(-d) < 0$: a hyperbolic, not geometric, memory.
9. **Uniqueness.** A day in the interior is covered by $h$ labels, so each label's average uniqueness is
   $\tfrac1h\sum_{t}1/c_t = 1/h$; with $h = 10$, 0.1. Chapter 12 found 0.115 because the edges of the sample (and
   gaps) are covered by fewer labels; the effective sample is about $n/h$.
10. **Equivariance.** For a permutation matrix $\Pi$, $Q, K, V$ become $\Pi Q, \Pi K, \Pi V$, the score matrix
    $\Pi QK^{\top}\Pi^{\top}$, and the row-wise softmax commutes with permuting rows and columns together, so
    $A \mapsto \Pi A \Pi^{\top}$ and $AV \mapsto \Pi A V$. The residual and the position-wise feed-forward layer are
    applied row by row, so they commute with $\Pi$ too.

## Data and reproducibility

* **The coin panel.** Every USDT pair in Binance's public archive (data.binance.vision), daily candles, 2017 to
  2025, including delisted pairs; stablecoins, fiat and leveraged tokens excluded. Each Sunday's universe: listed at
  least 60 days, median daily USDT volume of at least \$250,000 over four weeks. The target is the next week's log
  return, to the last close before a delisting. 2021–2025 is sealed in `videos/quant/data/envelope.json` and was
  opened once, by the two registered strategies.
* **Research windows.** 2018-07 to 2020-12 for coins (the zoo tests 2019 and 2020 with expanding refits); 1926–2020
  for the Welch–Goyal timer; ETFs 2010–2020 for the pocket model (tested from August 2015).
* **Seeds.** Every network averages three or five seeds; the theory chapter's simulations use 20–30 draws each.
* **Kronos** was described from its paper only; the House did not run its code.

---

# 中文

《量化，从零构建》第27部分：机器学习预测收益。这是第四幕“收益溢价”（23–29）的第五部分，也是第一部按本系列“博士层”标准制作的部分。第26部分建立了让回测保持诚实的机器；本部分让实证资产定价文献中的每一个学习器都经过它。

## 章节

* **千分之四**（开场）。顾、凯利和修（2020）：NN3只解释了股票月收益方差的0.40%，但它的多空组合按市值加权夏普比率为1.35，按等权为2.45。
* **1. 低信噪比的世界。** 十五个Welch–Goyal预测变量，1926–2020年，样本内最好的（$ltr$）解释下月收益的0.73%。
* **2. 模型动物园。** 566个币，2018–2020年有170个（62个后来下架），5,997个币周；2021–2025年封存。九个模型的样本外$R^2$全为负（−2.6%到−1.7%）；五分位多空夏普比率从−1.37（NN3）到0.99（GBRT），两个标准误约为±1.4。
* **3. 优势在哪里。** 流动性较好的一半平均为0.00，较差的一半为0.17；按10个基点计换手成本每年5–14%，按50个基点九个模型中五个亏钱。
* **4. 复杂度的美德。** 随机特征择时：$P = 12{,}000$时夏普比率0.33，波动率缩放的市场为0.52。
* **5. 批评者。** 纳格尔（2025）：核极限是对过去十二个月收益的相似度加权平均。
* **6. 过参数化预测的理论**（研究章节）。马尔琴科–帕斯图尔定律；岭回归与无岭回归的精确风险及其证明；理论与模拟吻合；设定错误模型中$\gamma = 10$时无岭回归的$R^2$为3.0%；随机特征误差为$O(P^{-1/2})$；三个开放问题。
* **7. 自编码器资产定价。** 一个因子解释约45%，五个线性因子51.5%；预测$R^2$约−2%：溢价在下跌的市场中估计（−26%，然后−57%），用于上涨143%的市场。
* **8. 带对抗矩的深度SDF。** SDF组合就是切点组合；对抗SDF在2020年为−1.53，与市场的相关系数为−0.996。
* **9. 跨资产的注意力。** 置换等变性；注意力几乎均匀；transformer的$R^2$为−9.7%，逐资产网络为−1.2%。
* **10. 价格的图像。** 6,718张训练图；准确率49.3%，基准52.5%；CNN多空−0.50，二十天动量2.64。
* **11. 基础模型。** Chronos、TimesFM、Kronos（仅根据论文介绍）；我们的小模型零样本迁移到五只ETF，不及拟合过的EWMA。
* **12. 实践者的工具箱。** 美元K线、分数阶差分、三重障碍、元标签、唯一性权重。
* **13. 共形预测。** 面板上90%覆盖89.7%；比特币上自适应共形覆盖89.7%。
* **14. 来自公开记录：Two Sigma与文艺复兴。**
* **15. 机器学习策略，登记并打开。** 币上的NN3：研究期−0.71，留出期1.29 ± 0.34（扣除10个基点后1.13）；复杂度择时：研究期0.33，留出期−0.17。计数器10,455。
* **16. 第27条规则：模型部门。**

## 写给研究者

岭回归风险在各向同性高斯特征的比例极限下是精确的（Hastie等2022，定理1与定理5）；设定错误模型是其第5节的最简形式，凯利、马拉穆德和周（2024）证明了择时版本。视频简化之处：随机特征的逐点收敛、Deep Sets刻画的条件、IPCA约化所需的正交特征、SDF只用无条件二阶矩。开放问题：可预测性是稠密还是稀疏；相依、厚尾与衰减下的精确风险；深度学习的收益来自核还是特征学习。

## 交易台问题与解答

1. **500只股票，月度样本外$R^2$为0.5%，多空夏普比率能有多少？** 每笔下注的信息比率约为$\sqrt{R^2/(1-R^2)} \approx 0.071$，$N$个独立下注乘以$\sqrt N \approx 22.4$，再乘$\sqrt{12}$，约为5.5。实际误差共享因子，独立下注只有几十个，加上成本，1–2就是好结果。
2. **一百万个参数、一万个观测、训练集完美拟合，没用吗？** 不一定。$\gamma = 100$时最小范数插值器的方差为$\sigma^2/(\gamma-1)$，约为$\sigma^2$的1%；关键是偏差和岭回归能否更好。要看岭路径、样本外风险以及同等预算下的简单基准。
3. **方向准确率55%，能交易吗？** 单凭这一点不能。要看涨跌幅大小、基准比率、与已有持仓的相关性以及扣除成本后的结果。
4. **两年、40个币、周度、夏普比率1.0，95%区间？** 标准误约$\sqrt{1.5/2} \approx 0.87$，区间约为−0.7到2.7；要在两个标准误上区分1和0.5，需要约24年。
5. **元模型把精确率翻倍但只接受十分之一的下注。** 看每单位风险的期望利润：除非保留下注的均值与标准差之比的提高超过广度损失（独立时为$\sqrt{10}$倍），否则更差。在留出数据上、扣除成本后决定。
6. **共形区间在2010年代覆盖90%，2020年只覆盖70%。** 保证依赖可交换性，市场状态的变化打破了它，并没有违反什么。用自适应共形推断、滚动重新校准，或按波动率标准化残差。

## 习题与解答

1. **（资格考试）分裂共形。** 可交换时$R_{n+1}$在$n+1$个分数中的秩是均匀的；覆盖等价于秩不超过$k = \lceil (n+1)(1-\alpha)\rceil$，概率$k/(n+1) \ge 1-\alpha$；无并列时恰为$k/(n+1) < 1-\alpha+1/(n+1)$。
2. **（资格考试）OLS的精确风险。** $\mathbb E|\hat b - b|^2 = \sigma^2\,\mathbb E\operatorname{tr}(X^{\top}X)^{-1} = \sigma^2 P/(N-P-1)$（逆Wishart的均值），极限为$\sigma^2\gamma/(1-\gamma)$。
3. **岭回归趋于插值器。** $\hat b_\lambda = X^{\top}(XX^{\top}+\lambda N I)^{-1}y \to X^{\top}(XX^{\top})^{-1}y = X^{+}y$，它位于$X$的行空间，因而是范数最小的解。
4. **随机特征。** $\mathbb E\cos(w^{\top}\Delta)$是正态特征函数的实部，等于$e^{-\gamma^2|\Delta|^2/2}$。
5. **自适应共形。** 求和得$\alpha_{T+1}-\alpha_1 = \gamma\sum_t(\alpha-\mathrm{err}_t)$，而工作水平留在$[-\gamma, 1+\gamma]$内，除以$\gamma T$即得。
6. **SDF即切点组合。** $\mu = (\Sigma+\mu\mu^{\top})w$，由谢尔曼–莫里森得$w \propto \Sigma^{-1}\mu$；由$0 = \mathbb E[M]\mathbb E[R_p] + \operatorname{cov}(M,R_p)$得汉森–贾甘纳坦界。
7. **双障碍。** $e^{-2\mu X_t/\sigma^2}$是鞅，由可选停止得$p = (e^{2\mu b/\sigma^2}-1)/(e^{2\mu b/\sigma^2}-e^{-2\mu b/\sigma^2})$，$\mu = 0$时为二分之一。
8. **分数阶权重。** $w_k = \Gamma(k-d)/(\Gamma(-d)\Gamma(k+1)) \sim k^{-d-1}/\Gamma(-d)$：双曲而非几何的记忆。
9. **唯一性。** 内部每天被$h$个标签覆盖，平均唯一性为$1/h$；$h = 10$时为0.1，第12章的0.115来自样本边缘覆盖较少；有效样本约为$n/h$。
10. **等变性。** 置换后得分矩阵变为$\Pi QK^{\top}\Pi^{\top}$，逐行softmax与同时置换行列可交换，所以$AV \mapsto \Pi AV$；残差和逐位置前馈层也与$\Pi$可交换。

## 数据与复现

币安公开档案中的每一个USDT交易对（含已下架），日K线；每周样本池要求上市至少60天、四周日成交额中位数至少25万美元；2021–2025年封存，只由两个已登记策略打开一次。Kronos仅根据论文介绍，我们的公司没有运行它的代码。
