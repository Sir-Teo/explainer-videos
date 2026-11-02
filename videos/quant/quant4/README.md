# Quant, Built — Part 4: Martingales and Measure

Part 4 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the first part of Act II, the Mathematical Toolkit. It makes "a fair game"
precise. It covers information as a filtration, conditional expectation as a projection, martingales and optional
stopping, why the doubling system escapes the theorem, and how one doubling trader broke Barings. Then it turns to
Doob's decomposition of the market, changes of measure on a coin, heavy tails as stable laws, and testing by betting
with e-processes. Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`martingale`](../../../explainer/quant/house/martingale.py) module) from public data: Kenneth French's daily US market
since 1926, Binance's Bitcoin, and the Nikkei 225 from FRED. Simulations and schematics are labeled on screen; firms
and events come from the public record.

*An education in methods, not investment advice.*

## Chapters (about 40 minutes)

* **Can you beat a fair game?** A bettor wagers every day since 1926 that today's US market return keeps yesterday's
  sign, with stakes sized by the House's e-process. Wealth passes 20 in February 1929 and reaches about 10¹⁰¹. Started
  in 2000, it peaks at 6.7 and never reaches 20. Then the objectives, and the House's e-value monitor.
* **1. Information and conditional expectation.** Three coin tosses, eight worlds, partitions that refine
  (a filtration). E[#heads | F_n] is drawn as bars that change only when information arrives. Conditional expectation
  is shown as orthogonal projection (the error is orthogonal to everything computable), and the tower property as
  projecting twice.
* **2. Martingales and optional stopping.** The definition; Ville (1939) named martingales after the betting system,
  and Doob (1940, 1953) built the theory. Examples include a Doob martingale you can watch: the live probability that
  heads wins a best-of-21. Optional stopping and its three sufficient conditions. Doubling with an endless bankroll
  (E[τ] = 2, unbounded bets, the theorem fails) against a bankroll of 1,023 (1023/1024 × 1 − 1/1024 × 1023 = 0).
  Admissible strategies (Part 9).
* **3. Gambler's ruin and bold play.** The ruin probability a/b from optional stopping, and de Moivre's martingale
  (q/p)^X for a biased game. Starting at 50 and aiming for 100, the chance is 50% on a fair coin, 6.3% on European
  roulette and 0.51% on American roulette. Doubling a bankroll on European roulette: 0.45% with one-unit bets from 100
  units, 1.8 × 10⁻¹² from 500 units, against 48.6% with one bold bet (Dubins and Savage 1965). The casino as a firm.
* **4. Doubling down: Barings, 1995.** The crisis file: about £830 m lost, error account 88888 (opened in 1992), and
  ING buying the bank for £1. FRED's Nikkei 225 was 19,331 on 13 January, before the Kobe earthquake of 17 January. It
  closed at 17,785 on 23 January (−8%) and 16,809 on 27 February, the day after Barings failed. A hidden account
  supplied the unbounded bankroll a doubling strategy needs.
* **5. Doob's decomposition.** A 55% coin: drift 0.1 a toss plus a martingale. The US market's log wealth, 1926–2020,
  splits as 9.06 = 7.28 (the sum of each day's drift forecast, the mean so far) + 1.78 (the martingale), and $1 became
  $8,642. The squared martingale's predictable part is the sum of each day's EWMA variance forecast, 2.893, against a
  realized quadratic variation of 2.894.
* **6. Change of measure.** A fair coin against a 60% coin over three tosses: the table of P, Q and L = dQ/dP. The
  rules E_Q[X] = E_P[LX] and E_P[L] = 1. Equivalent measures agree on what is impossible, so an arbitrage looks the
  same under every equivalent measure. Over 300 tosses, L has mean 1 under P, but its median is 0.002 and 68% of paths
  end below 0.01. Under Q, 67% end above 100: L is the wealth of a gambler betting on Q.
* **7. Heavy tails as stable laws.** Lévy's stable family, Mandelbrot (1963) and Fama (1965). McCulloch's quantile
  estimate gives α = 1.40 for the US market, 1926–2020 (1.40–1.61 by decade), and 1.27 for Bitcoin. Mantegna and
  Stanley's probability of return to the origin gives slope 0.50 for a simulated Gaussian (α = 1.99), 0.60 for the US
  1926–2020 (α = 1.67), 0.69 for 1962–86 (α = 1.44) and 0.62 for Bitcoin (α = 1.62). Yet the variance is finite (Part
  1's tail exponent is near 3): the result is a truncated Lévy law, or volatility that moves.
* **8. Testing by betting.** Ville's inequality, e-processes, Shafer and Vovk, and Ramdas et al. (2023). Over 2,000
  simulated fair games of 2,500 days, a t-test checked daily rejects in 50% of them and an e-process in 3.2%. On real
  data, betting on sign continuation, the e-process passes 20 within three years when started in 1926 and within
  fifteen months when started in 1975. It never passes 20 when started in 2000, nor for Bitcoin from 2018.
* **9. The e-value monitor.** The House's `EProcess` and its uses, the trial counter (10) and Rule 5: a claim that
  something beats a fair game is tested with an e-process, valid whenever it is checked.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant4.compute                        # every number, cached in .cache/quant4/ (about a minute)
EXPLAINER_TTS=silent python tools/qa_scene.py quant4 Betting    # one chapter, silent, with a contact sheet
python tools/make.py quant4 --cpu-voice -q m                 # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **A martingale starts at 1 and stops at 0 or 3.** The stopped process is bounded between 0 and 3, so optional
   stopping applies: E[M_τ] = 1. With p = P(hit 3), 3p + 0·(1 − p) = 1 and p = 1/3.
2. **Expected tosses to see HH.** Before every toss a new gambler arrives with $1 and bets it on heads at fair odds. If
   heads comes, the gambler bets the $2 on heads again, and otherwise leaves with nothing. The casino's net take is a
   martingale with mean zero. When HH first appears at time τ, the casino has taken in τ dollars and owes $4 to the
   gambler who arrived at τ − 1 and $2 to the one who arrived at τ. So E[τ] − 6 = 0, and E[τ] = 6. (For HT the answer
   is 4: only the gambler at τ − 1 is paid.)
3. **$100 at European roulette, $200 needed.** One bet of everything on red succeeds with probability 18/37 ≈ 48.6%.
   One-unit bets succeed with probability (1 − (q/p)¹⁰⁰)/(1 − (q/p)²⁰⁰) ≈ 0.45%, because they expose the money to the
   edge thousands of times. In a subfair game, bold play is optimal (Dubins and Savage).

## Problems, with solutions

1. **Exit time.** E[S²_{n+1} − (n + 1) | F_n] = S²_n + 2S_n·E[ξ] + E[ξ²] − n − 1 = S²_n − n, so S²_n − n is a
   martingale. Stop at τ = first time |S| = a. The steps are bounded and E[τ] < ∞, so E[S²_τ] − E[τ] = 0. Since
   S²_τ = a², E[τ] = a².
2. **Biased ruin.** E[(q/p)^{X_{n+1}} | F_n] = (q/p)^{X_n}·(p·(q/p) + q·(p/q)) = (q/p)^{X_n}. Optional stopping gives
   (q/p)^a = P(hit b)(q/p)^b + (1 − P(hit b)), so P(hit b) = (1 − (q/p)^a)/(1 − (q/p)^b). With p = 18/37, a = 10 and
   b = 20 this is 36.8% (a simulation of 4,000 games gives 36.4%).
3. **Doubling with 2^k − 1.** A session wins 1 unless the first k tosses are all losses (probability 2^{−k}), which
   loses 2^k − 1. The expected gain is (1 − 2^{−k}) − 2^{−k}(2^k − 1) = 0. The number of sessions up to and including
   the first ruin is geometric with mean 2^k: about 1,024 sessions for k = 10, after which the 1,023 units won are
   lost at once.
4. **Collapse of the likelihood ratio.** E_P[L_n] = Σ_ω P(ω)Q(ω)/P(ω) = 1. log L_n is a sum of i.i.d. terms with mean
   E_P[log(Q/P)] = −D(P‖Q). Here D = ½ ln(0.5/0.6) + ½ ln(0.5/0.4) = 0.0204 nats a toss, so by the strong law
   L_n → 0 almost surely. The median of L₃₀₀ is about e^{−300 × 0.0204} = 0.0022, which matches the simulated 0.002.
5. **Ville's inequality and peeking.** Let τ be the first n with W_n ≥ c. Optional stopping at the bounded time
   min(τ, n) gives 1 = E[W_{τ∧n}] ≥ c·P(τ ≤ n), so P(τ ≤ n) ≤ 1/c. Let n → ∞, and take c = 1/α. A daily t-statistic
   is S_n/√n. By the law of the iterated logarithm, S_n/√(2n log log n) has limsup 1, so |S_n|/√n exceeds any fixed
   level infinitely often, and a test checked forever rejects a true null with probability one.

## Data and reproducibility

* Kenneth French's daily US market (value-weighted, with dividends), July 1926 to December 2020. The hold-out from
  2021 is sealed (Part 1).
* Binance BTCUSDT daily candles, August 2017 to December 2020, each monthly file checked against Binance's SHA-256.
* FRED's NIKKEI225 (daily close). The window July 1994 to March 1995 is recorded in the data manifest, and the
  hold-out from 2021 is sealed.
* Simulations use fixed seeds: the coin paths, the likelihood ratios (2,000 paths), the peeking experiment (2,000
  games) and a gambler's-ruin check. The trial counter registers the e-process tests (three US start dates, one for
  Bitcoin).

---

# 量化金融，从零搭建 — 第4部分：鞅与测度

本部分是第二幕“数学工具箱”的第一部分，把“公平博弈”变得精确：信息即σ代数流，条件期望即投影，鞅与可选停止，加倍下注为什么能逃出定理、
一个加倍下注的交易员如何拖垮巴林银行，市场的杜布分解，硬币上的测度变换，作为稳定分布的厚尾，以及用e过程做“以下注来检验”。
所有数字都由本系列自己的代码根据公开数据算出。

*讲的是方法，不构成投资建议。*

## 交易台问题与解答

1. **一个鞅从1出发，首次碰到0或3时停止。** 停止过程夹在0和3之间，可选停止定理成立：E[M_τ] = 1。设p = P(碰到3)，则3p + 0·(1 − p) = 1，
   p = 1/3。
2. **期望掷多少次才出现两个连续正面？** 每次掷币前来一位新赌徒，拿1美元按公平赔率押正面；若中，再把2美元押正面，否则离开。
   赌场的净收入是均值为零的鞅。HH在τ时刻首次出现时，赌场收进τ美元，要付τ − 1时刻到来的赌徒4美元、τ时刻到来的赌徒2美元：
   E[τ] − 6 = 0，E[τ] = 6。（HT的答案是4：只有τ − 1时刻的赌徒获胜。）
3. **欧式轮盘，手上100美元，今晚需要200美元。** 全部押红一次，成功概率18/37 ≈ 48.6%；每次押1美元，成功概率
   (1 − (q/p)¹⁰⁰)/(1 − (q/p)²⁰⁰) ≈ 0.45%，因为钱要成千上万次暴露在庄家优势下。在对你不利的博弈中，大胆下注是最优的（Dubins与Savage）。

## 习题与解答

1. **离开区间的时间。** E[S²_{n+1} − (n + 1) | F_n] = S²_n − n，所以S²_n − n是鞅。在τ = 首次|S| = a时停止：步长有界且E[τ] < ∞，
   故E[S²_τ] − E[τ] = 0，S²_τ = a²，所以E[τ] = a²。
2. **有偏博弈的破产概率。** E[(q/p)^{X_{n+1}} | F_n] = (q/p)^{X_n}·(p·(q/p) + q·(p/q)) = (q/p)^{X_n}。可选停止给出
   P(碰到b) = (1 − (q/p)^a)/(1 − (q/p)^b)。p = 18/37、a = 10、b = 20时为36.8%（4,000局模拟为36.4%）。
3. **本金2^k − 1的加倍下注。** 每一轮除非前k次全输（概率2^{−k}，输掉2^k − 1），否则赢1。期望收益为(1 − 2^{−k}) − 2^{−k}(2^k − 1) = 0。
   直到（含）第一次破产的轮数服从几何分布，均值2^k：k = 10时约1,024轮，然后赢来的1,023一次输光。
4. **似然比的崩塌。** E_P[L_n] = Σ_ω P(ω)Q(ω)/P(ω) = 1。log L_n是独立同分布项之和，均值为−D(P‖Q)；这里
   D = ½ ln(0.5/0.6) + ½ ln(0.5/0.4) = 每次0.0204奈特，由强大数定律L_n几乎必然趋于0。L₃₀₀的中位数约为e^{−300 × 0.0204} = 0.0022，
   与模拟的0.002一致。
5. **Ville不等式与反复查看。** 令τ为首个W_n ≥ c的n。在有界时刻min(τ, n)应用可选停止：1 = E[W_{τ∧n}] ≥ c·P(τ ≤ n)，令n → ∞，
   取c = 1/α即得。每日的t统计量是S_n/√n；由重对数律，S_n/√(2n log log n)的上极限为1，所以|S_n|/√n会无穷多次超过任何固定水平：
   永远查看下去的检验，必然会以概率一拒绝一个真实的原假设。
