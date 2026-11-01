# Chinese edition of *Quant, Built* (量化金融，从零搭建)

Narration translations live in `videos/quant/quantN/zh_lines.py`, as a table of literal lines and templates, which
`tools/zh_lines.py` turns into `narration_zh.json`:

    python tools/zh_lines.py quantN --todo        # source lines the table doesn't cover yet
    python tools/translate_narration.py quantN --lang zh && python tools/zh_lines.py quantN
    python tools/zh_lines.py quantN --verify      # after any English render: will every line translate?

On-screen text lives in `videos/quant/quant_text_zh.json` (exact `strings`, `phrases` inside `\text{}`, regex
`patterns`): `python tools/collect_text.py quantN`, then `--check quantN` lists what is still English; merge
translations with `python tools/text_zh_add.py quant FILE`; `--lang zh quantN` dry-runs the Chinese build.

## Style

- Spoken Mandarin, short sentences; same content and order as the English. Chapter openings read "第N章。…"; parts
  read "第N部分".
- Keep every `<bookmark mark='x'/>`, in order, before the words it times.
- Full-width punctuation; numbers as digits (20%, 46亿美元 for $4.6 billion, 1987年10月19日). Money in 美元; "points of
  volatility" are 波动率点 (or 个点 once established).
- Latin letters stay Latin in math and tickers: S, K, T, r, σ, μ, d1, d2, N(d1), P, Q, BTC, VIX, DVOL, CBOE.
- Spoken math: σ平方, S平方乘以Gamma, 根号Δt, e的负rT次方, 二分之一, 正负, 按平方根缩小.
- Greeks keep their English names in narration and on screen (Delta, Gamma, Theta, Vega, Vanna, Volga): this is how
  Chinese trading desks say them. The formula's name stays "Black–Scholes"; the people are transliterated
  (布莱克、斯科尔斯、默顿).
- Firms: the House is 我们的公司 in narration and 本系列公司 where a noun phrase is needed on screen; real firms keep
  their usual Chinese names where one exists (高盛, 所罗门兄弟, 长期资本管理公司 (LTCM), 纽约联邦储备银行), otherwise the
  English name (Deribit, Binance → 币安, Jane Street, Citadel).
- Allegations stay labelled as allegations (据称, 被指控); "not investment advice" is 不构成投资建议.
- Data the House reads or writes (instrument names like `BTC-26DEC25-100000-C`, column names, tickers) stays in
  English: draw it with `data_text(...)`.

## Glossary

| English | 中文 |
|---|---|
| quantitative finance, quant | 量化金融，宽客/量化研究员 |
| option, call, put | 期权，看涨期权，看跌期权 |
| strike | 行权价 |
| expiry, time to expiry | 到期日，剩余时间（距到期） |
| payoff, the hockey stick | 收益，曲棍球杆 |
| premium | 期权费 |
| underlying | 标的 |
| at the money / in / out of the money | 平值 / 实值 / 虚值 |
| deep in the money | 深度实值 |
| European / American option | 欧式 / 美式期权 |
| early exercise, exercise boundary | 提前行权，提前行权边界 |
| early-exercise premium | 提前行权溢价 |
| free-boundary problem | 自由边界问题 |
| optimal stopping | 最优停止 |
| straddle, call spread, digital option | 跨式组合，看涨价差，数字期权 |
| warrant | 认股权证 |
| replication, replicating portfolio | 复制，复制组合 |
| hedge, delta hedge, hedger | 对冲，Delta对冲，对冲者 |
| rebalance | 调整（再平衡） |
| hedging error | 对冲误差 |
| riskless portfolio | 无风险组合 |
| arbitrage, no-arbitrage | 套利，无套利 |
| risk-free rate | 无风险利率 |
| bond, bank account | 债券，银行账户 |
| geometric Brownian motion | 几何布朗运动 |
| drift, expected growth rate | 漂移，期望增长率 |
| volatility | 波动率 |
| implied volatility | 隐含波动率 |
| realized volatility | 已实现波动率 |
| variance | 方差 |
| Ito's lemma | 伊藤引理 |
| partial differential equation | 偏微分方程 |
| heat equation | 热方程 |
| terminal condition | 终值条件 |
| Feynman–Kac theorem | 费曼–卡茨定理 |
| real-world measure P | 真实世界概率（测度）P |
| risk-neutral measure Q | 风险中性测度Q |
| change of measure, numéraire | 测度变换，计价单位 |
| Girsanov's theorem | 吉尔萨诺夫定理 |
| market price of risk | 风险的市场价格 |
| martingale | 鞅 |
| binomial tree (CRR) | 二叉树（CRR） |
| backward induction | 倒推 |
| central limit theorem | 中心极限定理 |
| lognormal | 对数正态 |
| put–call parity | 平价关系（看涨看跌平价） |
| forward price | 远期价格 |
| log-moneyness | 对数价值度（行权价与远期之比的对数） |
| the Greeks | 希腊字母 |
| dollar gamma | 美元Gamma |
| time decay | 时间衰减 |
| breakeven move | 盈亏平衡的变动幅度 |
| P&L, the ledger | 盈亏，账本 |
| long / short gamma | 做多 / 做空Gamma |
| volatility smile, skew | 波动率微笑，偏斜 |
| volatility surface; the Surface | 波动率曲面；基准曲面 |
| vega-weighted RMSE | 按Vega加权的均方根误差 |
| calendar arbitrage | 日历套利 |
| fat tails, power law, tail exponent | 肥尾，幂律，尾部指数 |
| inverse cubic law | 负三次方律 |
| Hill estimator | 希尔估计量 |
| standard deviation (σ) | 标准差 |
| variance risk premium | 方差风险溢价 |
| variance swap | 方差互换 |
| stochastic volatility, jumps | 随机波动率，跳跃 |
| rough volatility | 粗糙波动率 |
| transaction costs | 交易成本 |
| basis point | 基点 |
| Leland's volatility | 利兰波动率 |
| deep hedging | 深度对冲 |
| finite differences, Monte Carlo | 有限差分，蒙特卡洛 |
| regression Monte Carlo (Longstaff–Schwartz) | 回归蒙特卡洛（Longstaff–Schwartz） |
| portfolio insurance | 投资组合保险 |
| index futures | 股指期货 |
| Black Monday | 黑色星期一 |
| Brady Commission | 布雷迪委员会 |
| performativity | 述行性 |
| convergence trade, spread | 收敛交易，价差 |
| leverage, margin, fire sale | 杠杆，保证金，甩卖 |
| liquidity | 流动性 |
| market maker | 做市商 |
| carry trade, unwind | 套息交易，平仓 |
| trading desk, desk question | 交易台，交易台问题 |
| the House | 我们的公司（本系列公司） |
| the Track Record | 业绩记录 |
| the trial counter | 试验计数器 |
| not investment advice | 不构成投资建议 |
