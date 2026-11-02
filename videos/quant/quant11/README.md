# Quant, Built — Part 11: Trading Options

Part 11 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the practitioner's part of Act III. It covers:

* positions as Greeks, and what each strategy is a bet on;
* gamma scalping on a real Bitcoin path;
* volatility trading and a forecaster's edge;
* the market maker's book;
* expiry, pin risk and dispersion;
* India's expiry-day boom and the SEBI case against Jane Street, which is alleged and contested;
* hedging under costs, with a learned hedger.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`quoting`](../../../explainer/quant/house/quoting.py) engine and [`hedge`](../../../explainer/quant/house/hedge.py),
tested) from Deribit's DVOL, Binance's hourly BTCUSDT, Kenneth French's industries, and SEBI's published studies and
orders. Toy models are labelled as illustrations on screen.

*An education in methods, not investment advice. The SEBI matter is described as alleged, from the regulator's
interim order and the firm's public statements; no final finding had been made at the time of writing.*

## Chapters (about 40 minutes)

* **Gamma against theta.** The desk question: a long, hedged straddle in a quiet week loses theta, and vega if
  implied volatility falls.
  * May 2021: a 30-day ATM straddle bought at DVOL's 74% and hedged hourly. Realized volatility was 127%, and Bitcoin's
    low was 44% below the start.
  * The straddle earned only +1.7 on a premium of 16.9, because the crash carried spot away from the strike.

  Then the objectives, and the volatility desk's quoting engine.
* **1. Positions as Greeks.** The Taylor series of a book: delta, gamma, theta, vega, vanna and volga. P&L maps
  (spot ±25% against vol ±10 points after a week) for the straddle, strangle, risk reversal, butterfly, call spread
  and calendar.
* **2. Gamma scalping on a real path.** The hedge's trades on the May 2021 path, and the hedge ratio running to a full
  unit. The ledger reads gamma +6.4, theta −4.6, net +1.7: gamma pays where the strike is. Variance swaps are
  previewed.
* **3. Volatility trading, and a forecaster's edge.** Part 10's hedged short call, split by Sinclair's rule: sell when
  DVOL exceeds a HAR forecast, refitted weekly. On non-overlapping months it earned 1.75 (se 0.32, 26 months) on the
  signal against 0.57 (se 0.36, 17 months) off it, a t of about 2.4. The test was registered; the counter reads 73.
* **4. The market maker's book.** The die game and adverse selection (Glosten–Milgrom 1985). A toy book on 2,000
  identical client requests: quoting fixed around fair value lets vega inventory reach 64. Skewing quotes against
  inventory (Avellaneda–Stoikov) keeps it to 9, for spread income of 13.7 against 14.8. Firm cards come from the
  public record: SIG (1987; poker and game theory in training, per its job postings), Optiver (1986), IMC (1989) and
  Jane Street.
* **5. Expiry, pin risk, and dispersion.**
  * ATM gamma at 50% vol is 0.15 a day before expiry and 5.8 a minute before. Delta becomes a step, and there is pin
    risk.
  * American calls should be exercised early only for dividends.
  * Implied correlation, and its realized counterpart from French's industries (40 with full histories, rolling 36
    months): median 0.63, peaks of 0.82 (1929–33), 0.79 (1987) and 0.72 (2008), and a low of 0.27 in 2001.
* **6. India's expiry-day boom, and a case file.**
  * SEBI's studies: 91% of individual F&O traders lost money in FY2023–24; net losses were ₹1.81 lakh crore over
    FY22–24, and ₹1.06 lakh crore in FY25.
  * The 1 October 2024 circular, effective 20 November 2024: one weekly benchmark per exchange, a minimum contract of
    ₹15 lakh, and a 2% extra margin on short options at expiry.
  * The SEBI interim order of 3 July 2025 against Jane Street entities: alleged expiry-day index support and selling
    alongside large options positions, and about ₹4,844 crore impounded. The firm disputes the findings, deposited the
    amount in escrow, and resumed trading.
  * A toy model with invented numbers and linear impact shows why options positions and underlying trading are
    watched together.
* **7. Hedging under costs.** The Whalley–Wilmott (1997) band, and Leland (1985). On 20,000 simulated 30-day paths at
  60% vol with 10 bp costs:

  | Rule | s.d. | cost |
  |---|---|---|
  | rehedge every 6 hours | 0.57 | 0.45 |
  | Whalley–Wilmott, γ = 10 / 1 / 0.1 | 0.65 / 0.83 / 1.26 | 0.31 / 0.24 / 0.19 |
  | deep hedge, κ = 1 / 4 / 16 (5,000 held-out paths) | 0.59 / 0.71 / 0.98 | 0.36 / 0.27 / 0.21 |

  The deep hedger (Buehler et al. 2019) chooses how far to move toward delta. It lands just inside the band's
  frontier at each cost weight. A first version, a residual on delta trained for 250 steps, was worse than the bands;
  moving a learned fraction toward delta fixed it.
* **8. The options quoting engine.** Rule 11: quotes lean against inventory within Greek limits, hedges are judged net
  of costs, and nothing is held into expiry near its strike without a plan for the pin. The counter reads 73.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant11.compute                   # every number, cached in .cache/quant11/ (a few minutes)
EXPLAINER_TTS=silent python tools/qa_scene.py quant11 Hedging # one chapter, silent, with a contact sheet
python tools/make.py quant11 --cpu-voice -q m            # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Long a hedged straddle in a quiet week.** The daily P&L is ½ΓS²[(dS/S)² − σ²_imp dt] + vega·dσ_imp. With no
   moves, the first term is the full theta charge, ½ΓS²σ²_imp dt per day. If implied volatility also falls, vega
   loses too. You make money when realized variance, weighted by gamma, exceeds implied.
2. **The die.** E[X] = 3.5, so quote symmetrically around it, for example 3.3 / 3.7. Given "even", E[X | even] = 4 and
   the quote moves to about 3.8 / 4.2. The question to ask is why you are being told: information that reaches you
   through a trade moves fair value against you (adverse selection).
3. **Short a large ATM option an hour before expiry.** Gamma is near its peak, Γ ≈ 1/(Sσ√(2πτ)). Small moves flip
   delta and force large hedge trades at the worst prices. Pin risk adds overnight uncertainty about assignment.
   Reduce or roll before the last hour, or hedge the gamma with other options.

## Problems, with solutions

1. **The gamma–theta integral.** Mark the option at σ_imp and hedge its delta. By Itô,
   dV = Θdt + ΔdS + ½ΓS²σ²_r dt. By the Black–Scholes PDE at σ_imp (r = 0), Θ = −½ΓS²σ²_imp. So the hedged book earns
   ½ΓS²(σ²_r − σ²_imp)dt, and over the life ∫½ΓS²(σ²_r,t − σ²_imp)dt. The weight ΓS² is large near the strike and
   near expiry. The same realized variance therefore pays a lot if it happens there, and little far from the strike
   (May 2021).
2. **Gamma at expiry.** Γ = φ(d₁)/(Sσ√τ). At the money with τ → 0, d₁ → 0 and φ(0) = 1/√(2π), so
   Γ ≈ 1/(Sσ√(2πτ)). At S = 100 and σ = 0.5: a day (τ = 1/365) gives 0.152, and a minute (τ = 1/525,600) gives 5.78,
   √1440 ≈ 38 times larger.
3. **Implied correlation for two assets.** σ_I² = ¼σ² + ¼σ² + 2·¼ρσ² = σ²(1 + ρ)/2, so ρ = 2σ_I²/σ² − 1.
4. **The die with an informed counterparty.** Suppose the counterparty knows the roll with probability p and otherwise
   trades at random. Quote 3.5 ± s with s ≤ 0.5. Uninformed trades earn s. Informed trades lose E|X − 3.5| − s =
   1.5 − s, since |X − 3.5| takes the values 0.5, 1.5 and 2.5 equally often, and all of them trade. Breaking even
   requires (1 − p)s = p(1.5 − s), so s = 1.5p, valid while p ≤ 1/3.
5. **The band's scaling.** With a band of half-width h around delta, the mis-hedge variance per unit time scales as
   h²σ²S². The rate of trading needed to stay inside it scales as (Γσ S)²·S/h in shares times price. A hedger with
   risk aversion γ therefore minimizes γσ²S²h² + λσ²S³Γ²/h. Setting the derivative to zero gives
   h³ = λSΓ²/(2γ), so h ∝ (λSΓ²/γ)^{1/3}. Whalley and Wilmott's asymptotics give the constant 3/2 in place of 1/2.

## Data and reproducibility

* Deribit DVOL and Binance BTCUSDT hourly, 2021–2025 (as in Part 10). Kenneth French's 49 industries, monthly, to
  2020.
* SEBI: the study on F&O profits and losses (September 2024) and its July 2025 update; the 1 October 2024 circular;
  the interim order of 3 July 2025. Firm facts come from the public record (founding years; SIG's job postings).
* Registered with the trial counter: the forecast-edge test (1), bringing it to 73.
* The deep hedger trains in about a minute per cost weight on a CPU with one thread.

---

# 量化金融，从零搭建 — 第11部分：交易期权

从业者的一部分：

* 头寸即希腊字母，以及每种策略在押注什么；
* 真实比特币路径上的伽马剥头皮；
* 波动率交易与预测者的优势；
* 做市商的账本；
* 到期、钉住风险与离散度；
* 印度到期日交易热潮，以及SEBI对简街的案件（指控，有争议）；
* 有成本时的对冲，以及一个学出来的对冲者。

*讲的是方法，不构成投资建议。SEBI一案根据监管机构的临时命令和该公司的公开声明描述为指控；截至撰写时尚无最终裁定。*

## 交易台问题与解答

1. **安静一周里持有对冲后的跨式组合多头。** 每日损益为½ΓS²[(dS/S)² − σ²_imp dt] + vega·dσ_imp。没有波动时，第一项就是全额的时间损耗，
   每天½ΓS²σ²_imp dt；若隐含波动率也下降，vega也亏钱。只有当按伽马加权的已实现方差超过隐含方差时才赚钱。
2. **骰子。** E[X] = 3.5，围绕它对称报价，例如3.3 / 3.7。得知"偶数"后，E[X | 偶数] = 4，报价移到约3.8 / 4.2。要问的是为什么告诉你：
   通过交易传到你这里的信息，会让公允价值朝不利于你的方向移动（逆向选择）。
3. **到期前一小时卖出一大笔平值期权。** 伽马接近峰值，Γ ≈ 1/(Sσ√(2πτ))。小幅波动就会让delta翻转，迫使你在最差的价格大量对冲交易。
   钉住风险又带来是否被行权的隔夜不确定性。在最后一小时之前减仓或展期，或用其他期权对冲伽马。

## 习题与解答

1. **伽马–时间损耗积分。** 按σ_imp给期权定价并对冲delta。由伊藤公式，dV = Θdt + ΔdS + ½ΓS²σ²_r dt。由σ_imp下的布莱克–斯科尔斯方程（r = 0），
   Θ = −½ΓS²σ²_imp。所以对冲后的账本赚取½ΓS²(σ²_r − σ²_imp)dt，整个期限内为∫½ΓS²(σ²_r,t − σ²_imp)dt。权重ΓS²在执行价附近和临近到期时很大，
   所以同样的已实现方差发生在那里就赚得多，远离执行价就赚得少（2021年5月）。
2. **到期时的伽马。** Γ = φ(d₁)/(Sσ√τ)。平值且τ → 0时，d₁ → 0，φ(0) = 1/√(2π)，所以Γ ≈ 1/(Sσ√(2πτ))。S = 100、σ = 0.5时：
   一天（τ = 1/365）为0.152，一分钟（τ = 1/525,600）为5.78，大了√1440 ≈ 38倍。
3. **两资产的隐含相关性。** σ_I² = ¼σ² + ¼σ² + 2·¼ρσ² = σ²(1 + ρ)/2，所以ρ = 2σ_I²/σ² − 1。
4. **有知情对手的骰子。** 设对手以概率p知道点数，否则随机交易。报价3.5 ± s，s ≤ 0.5。与不知情者的交易赚s；与知情者的交易亏
   E|X − 3.5| − s = 1.5 − s，因为|X − 3.5|等可能地取0.5、1.5、2.5，而且都会成交。盈亏平衡要求(1 − p)s = p(1.5 − s)，即s = 1.5p，
   在p ≤ 1/3时成立。
5. **对冲带宽度的标度。** 在delta周围半宽为h的带内，错配对冲每单位时间的方差按h²σ²S²增长；为留在带内所需的交易速率，按股数乘价格计约为(ΓσS)²·S/h。
   风险厌恶为γ的对冲者因此最小化γσ²S²h² + λσ²S³Γ²/h。令导数为零得h³ = λSΓ²/(2γ)，即h ∝ (λSΓ²/γ)^{1/3}。
   Whalley与Wilmott的渐近分析给出的常数是3/2而不是1/2。
