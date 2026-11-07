# Quant, Built — Part 17: Deep Pricing and Hedging

Part 17 of the [43-part series](../README.md) covers learned pricing maps, calibration,
differential regression, BSDEs, optimal stopping, hedging with costs and model sensitivity.
Scientific corrections are committed; current-source bilingual visual QA is in progress.
See the [sequential QA record](../../../docs/qa/quantitative-finance-polish.md).
Continuous production-voice listening remains a separate pending pass.

## What this implementation establishes

The numerical examples are fixed-seed CPU demonstrations. They are not literal
replications of every cited paper, matched-budget comparisons, or deployment certifications.
The [original computation code](compute.py) and the House algorithms are unchanged in this pass.

| Chapters | Method and limits |
| --- | --- |
| Opening, 1–2 | Synthetic Black–Scholes labels and neural Greeks. Universal approximation does not guarantee optimization or accurate derivatives; smooth activations do not enforce convexity. |
| 3–5 | Rough Bergomi surrogate calibration and descriptive weekly Deribit surfaces. Correlated Monte Carlo labels, inverse-IV bias, box limits and local optimization affect interpretation. |
| 6–7 | Pathwise derivative labels and a Gaussian process with gradients. Labels from one path are correlated; the GP covariance and diagonal noise are working assumptions, not calibrated uncertainty. |
| 8–9 | A 100-asset issuer-default BSDE and a linear check. Brownian exposure is not a number of shares. Dense-network work can scale quadratically with dimension; iteration scatter is not a confidence interval. |
| 10 | A fitted Bermudan stopping rule. Its expected payoff is a lower bound; a simulated mean is an estimate. Published primal/dual estimates use different budgets. |
| 11–12 | Discrete hedgers, entropic sample risk, expected shortfall and drift. A seller's indifference premium subtracts the optimized no-claim baseline. Finite log-sum-exp does not prove a finite population exponential moment. |
| 13–14 | A delta-centred band, classical asymptotics and a structural prior. The replay and learned surface use the same seed. Persistent width limits and hard clamping distinguish this implementation from the cited soft-clamp study. |
| 15 | Penalized neural-SDE candidates illustrate model sensitivity. Finite calibration penalties, local searches, ratio estimates and barrier discretization do not certify robust price bounds. |
| 16 | An exact stationary-Gaussian reverse-process illustration and finite-signature diagnostics. No fitted BTC generator or BTC validation scores are shown. |
| 17–19 | Dated public deployment reports, proportionate model controls, research directions and a cross-generator validation design. Proposed monitoring and fallback routing are not implemented services. |
| Research | Continuous population loss identities, their Euler distinction and conditional a posteriori theory. Moving batch-loss averages are diagnostics, not error certificates. |

All finite plotted values are retained in the revised charts; coarse grids, omitted
nonfinite implied volatilities, saved histogram edge bins and saturated trade colours
are disclosed where used. Seed ranges are descriptive ranges, not confidence intervals.

## Data boundary and reproduction

There are 32 legacy Part 17 cache items. This pass restores 29 using their original
normal fixed-seed commands. It deliberately does not execute `generator`, `ddpm_reverse`
or `crossgen`: they use BTC daily history through 2025; `crossgen` also evaluates on
history overlapping its fit. The active scenes no longer consume those items or
present their scores. Chapter 16 instead demonstrates an exact Gaussian conditional
law with a fixed illustration seed, and chapter 19 explains an explicitly unfinished
validation design. The sealed investing window remains unopened.

The calibration chapters retain the original descriptive 2024–2025 Deribit quote
examples. These are surrogate-fit examples, not investing-scoreboard strategy results.
Part 16's original synthetic max-call cache supplies the LSM comparison through its
normal tracked loader. No new market configuration, register, seal or envelope-opening
operation is used. The Part-17 cumulative trial count stays 312; the global count stays
23,562. These counters count registered configurations, not the absence of all training.

For a fresh cache, invoke only the permitted original items, without `--force`, with
dependencies available. Do not run the legacy all-items command as a shortcut.

```bash
# List the permitted original item names without executing them.
EXPLAINER_TTS=silent python - <<'PY'
from videos.quant.quant17.compute import ITEMS
print(' '.join(k for k in ITEMS if k not in {'generator', 'ddpm_reverse', 'crossgen'}))
PY
# Restore an individual original item, for example:
python -m videos.quant.quant17.compute hlp

# Cached-only visual checks after restoring dependencies:
python tools/qa_series.py quant17 --cached-only --resume
python tools/qa_series.py quant17 --lang zh --cached-only --resume
python tools/qa_series.py quant17 --motion --cached-only --resume
python tools/zh_lines.py quant17 --todo
python tools/lecture_length.py quant17 --floor 50
```

The narration estimate after the scientific pass is 63.7 minutes. Silent playback
includes animation and pauses. A render exit code, caption coverage or a sampled
speech report is not by itself visual approval or continuous listening certification.

## Desk questions

**Why a cube-root band?** The reflected-gap approximation has risk cost proportional
to half-width squared and turnover cost proportional to its inverse. Minimizing their
sum gives cube-root scaling. A static quadratic-versus-linear balance does not derive it.

**How should calibration be checked?** Reprice independently with numerical uncertainty,
check the training domain, and separate label, surrogate, optimization and model errors.
A bounded parameterization and a good quote fit do not identify the economic model.

**Why derivative labels?** Valid pathwise derivatives constrain local shape at modest
adjoint cost, with tape-memory requirements. They are correlated labels and require a
justified interchange of differentiation and expectation. A digital's zero pathwise
derivative is not its price derivative.

**Does average hedge profit prove better replication?** No. Physical drift and the
objective can create intended investment demand. Compare exposures and risk under stated
measures, and use the optimized no-claim baseline for an indifference premium.

## Ten worked solutions

1. **Cash invariance and the seller's premium.** For γ > 0 and a finite exponential
   moment, ρ(X+c) = γ⁻¹ log E exp(−γX−γc) = ρ(X)−c. Let Gδ be trading gains and Cδ
   costs. Define rZ = infδ ρ(−Z+Gδ−Cδ), r0 = infδ ρ(Gδ−Cδ), using the same admissible
   set. Cash invariance makes the optimized risk after selling for p equal to rZ−p;
   indifference therefore gives p = rZ−r0. Under a martingale measure, integrable gains,
   nonnegative costs and an admissible zero policy, Jensen gives r0 ≥ 0 and zero trading
   gives r0 ≤ 0. Under physical drift r0 need not vanish. Discrete underhedged calls with
   lognormal tails can have infinite population entropic risk despite finite sample values.

2. **Band turnover and scaling.** Locally write the hedge gap as reflected Brownian
   motion dε = a dW+dL−dU on [−h,h]. Stationarity and Itô on ε² give
   0 = a²−2h E[dL+dU]/dt, so total share turnover is a²/(2h). Its uniform stationary
   variance is h²/3. With a² = σ²S²Γ², the local objective per unit time is
   J(h) = γσ²S²h²/6 + cSσ²S²Γ²/(2h).
   Thus J′(h)=0 gives h³ = 3cSΓ²/(2γ). This is a local small-cost, continuous-rebalancing
   asymptotic with slowly varying coefficients, not an exact optimum for a daily neural policy.

3. **BSDE and units.** For dXi = μiXi dt+σXi dWi, Itô gives
   dY = (u_t+𝓛u)dt + Σi σXi∂iu dWi. With u_t+𝓛u=f(u),
   f(y)=[(1−δ)Q(y)+R]y and terminal u(T,X)=min Xi, set Zi=σXi∂iu.
   Zi is exposure per Brownian increment; the corresponding share holding is
   Δi=Zi/(σXi). A stock-only Brownian hedge does not perfectly hedge issuer default.
   Existence, uniqueness and the PDE representation require their integrability,
   Lipschitz, Markov and regularity assumptions.

4. **Differential normal equations.** For n×p price features Φ, derivative feature
   matrices Dj and observed derivative vectors zj, minimize
   ‖Φw−y‖² + λΣj‖Djw−zj‖². Differentiation gives
   (ΦᵀΦ+λΣjDjᵀDj)w = Φᵀy+λΣjDjᵀzj.
   With a singular system choose a suitable generalized solution or declared regularizer.
   Correlation or heteroskedasticity can motivate a different weighted statistical model.

5. **Stopping.** Let gn be discounted exercise payoff and Gnext the discounted payoff
   obtained by the fixed continuation policy. At date n, conditional expected value is
   gnF + E[Gnext|Fn](1−F), affine in F∈[0,1]. Its maximum is attained by stopping when
   gn≥E[Gnext|Fn], with either decision allowed at equality. Conditioning on Xn alone
   needs a sufficient Markov state. Every admissible fixed τ satisfies E[gτ]≤supτ′E[gτ′].
   Its Monte Carlo mean can exceed the supremum through sampling error; the lower-bound
   statement concerns expectation. Evaluation should be independent of fitted-policy selection.

6. **Leland's convention.** For a convex short option, a small step gives
   E|ΔΔ|≈ΓσS√Δt√(2/π). One-way cost c per dollar traded contributes
   cΓσS²√(2/π)/√Δt per unit time. Absorbing this into ½σ²S²Γ yields
   σ̂²=σ²+2cσ√(2/π)/√Δt = σ²[1+√(2/π)k/(σ√Δt)], k=2c.
   State one-way versus round-trip costs. This smooth-Gamma, Gaussian-increment
   approximation is not exact finite-cost replication or a general utility price.

7. **Merton's investment overlay.** In the frictionless complete constant-volatility
   model dS/S=μdt+σdW, zero rates, exponential utility and admissible replication,
   the claim hedge Δ separates from the no-claim investment problem. If π dollars are
   invested in the stock, the HJB first-order condition is μVx+πσ²Vxx=0.
   CARA utility has −Vxx/Vx=γ, giving π=μ/(γσ²) and
   δ*=Δ+μ/(γσ²S). Claim replication makes the optimized investment opportunity cancel
   in the indifference comparison; the complete-market premium is independent of μ.
   Daily constraints, costs and finite-sample fitting need not reproduce this ideal exactly.

8. **Validation-label noise.** Let Y=F(θ)+ε, E[ε|θ]=0, with validation noise
   conditionally independent of the fitted predictor, and E Var(ε|θ)=s².
   Expanding the square gives E(F̂−Y)²=E(F̂−F)²+s². This is a population identity;
   a realized finite-sample RMSE need not exceed s. Doubling label variance does not
   determine how the fitted predictor changes. Implied-volatility inversion is nonlinear
   and can bias labels, so the identity need not hold exactly for finite-path IVs.

9. **Continuous linear population loss.** For predictable controls with
   E∫₀ᵀe^{2R(T−t)}|Zt|²dt<∞, solve dY=RYdt+Z·dW:
   YT=e^{RT}y0+∫₀ᵀe^{R(T−t)}Zt·dWt. With the corresponding representation
   g=e^{RT}u0+∫₀ᵀe^{R(T−t)}Z*t·dWt, subtract, square and take expectations.
   The stochastic integral has mean zero; Itô isometry gives
   Lpop=e^{2RT}(y0−u0)²+E∫₀ᵀe^{2R(T−t)}|Z−Z*|²dt.
   Therefore |y0−u0|≤e^{−RT}√Lpop. Known population loss 9 with R=.02,T=1
   gives 3e^{−.02}≈2.9406; an observed training loss of 9 alone gives no such certificate.

10. **Step controls, Euler and rates.** On a uniform grid of width h, unweighted
    predictable step projection uses
    Zbar_i=E[h⁻¹∫ti^{ti+h}Z*t dt|Fti]. The best weighted projection uses the same
    conditional weighted average with weight e^{2R(T−t)}. Testing the admissible
    left-endpoint choice Zi=Z*ti gives, if E|Z*t−Z*s|²≤C|t−s|,
    E∫|Zstep−Z*|²dt≤CT h/2. A bounded deterministic exponential weight preserves O(h).
    This upper bound allows a smaller or zero floor; it proves neither an exact 1/N rate
    nor an Ω(1/N) lower bound. The explicit Euler driver is a different scheme. Put
    a=1+Rh>0: E[YN−g]=aᴺy0−e^{RT}u0, hence
    |e^{−RT}aᴺy0−u0|≤e^{−RT}√Lpop,Euler. The continuous coefficient does not directly
    bound |y0−u0| from Euler batch loss. Han–Long's nonlinear results require their
    regularity/coupling conditions, sufficiently small h and constants not computed here.

The research plots average losses from changing weights and batches. Their last-20,
last-40 or last-10 averages use the stated saved-log windows; none is an independently
estimated population loss of a single frozen model. The nonlinear unit-coefficient
loss shading omits theorem constants and discretization terms and is explicitly a diagnostic.

## Primary methods and source checks

- HLP (1994), Cybenko (1989): learned price maps and compact-set approximation.
- Huge–Savine (2020): differential learning; classical gradient GPs use their chosen likelihood.
- [Han–Jentzen–E (2018)](https://arxiv.org/html/1707.02568v3): the reported 57.300 Picard reference is approximate;
  the paper's 0.46% and 1,607 seconds describe its experiment and hardware.
- [Han–Long (2020)](https://link.springer.com/article/10.1186/s41546-020-00047-w): conditional a posteriori theory,
  including Theorem 1′ assumptions; not a certificate from a moving training average.
- [Becker–Cheridito–Jentzen (2019)](https://jmlr.org/papers/v20/18-232.html): deep stopping and published numerical estimates.
- Buehler et al. (2019), Rockafellar–Uryasev (2000), Leland (1985), Whalley–Wilmott (1997): objectives, tail risk and costs.
- [Arzel–Lehdili (2026)](https://arxiv.org/abs/2603.29994): structural prior plus differentiable soft clamp;
  the House instead uses hard clamping and a width base limited throughout training.
- [Gierjatowicz et al.](https://arxiv.org/abs/2007.04154): neural-SDE calibration/model-risk methods;
  this restricted noisy local search supplies no certified robust bounds.
- Ho–Jain–Abbeel (2020); Chevyrev–Oberhauser (2022): diffusion and suitable full normalized-signature methods.
- [Risk.net, 26 May 2022](https://www.risk.net/derivatives/7949306/jp-morgans-deep-hedging-reaches-cliquets):
  Euro Stoxx cliquet rollout live; S&P expansion planned. No unverified since-2018 vanilla-book claim is retained.
- [SR 26-2 and attachment](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm), 17 April 2026:
  nonbinding, risk-proportionate guidance, principally relevant above $30bn assets; generative/agentic AI excluded.
- [PRA SS1/23](https://www.bankofengland.co.uk/prudential-regulation/publication/2023/may/model-risk-management-principles-for-banks-ss):
  published May 2023, effective May 2024, revised April 2026; stated institutional scope matters.
- [Mueller et al. (2024)](https://arxiv.org/abs/2410.22568) and
  [Zernikov (2026)](https://arxiv.org/abs/2605.21696): benchmark-specific optimizer steps and regime-dependent empirical hedges.

Textbook connections: Dixon–Halperin–Bilokon on learning, derivatives and GPs;
Savine and Glasserman on adjoints, Greeks and Monte Carlo; Shreve on pricing and
complete-market hedging. Approximation theorems do not prove SGD efficiency for a
generic high-dimensional PDE, and a small held-out synthetic error does not establish
absence of overfitting on future markets.

---

# 量化金融，从零搭建 — 第17部分：深度定价与对冲

本部分研究学习定价映射、神经校准、微分回归、BSDE、最优停止、含成本对冲及模型敏感性。
科学解释已修订；当前源码的双语视觉检查正在进行。连续生产语音聆听仍是单独待办。
固定种子CPU示例不是所有论文的逐项复现、等预算比较或上线认证；原计算文件与研究所算法未改。

## 各章范围与证据

开场及第1–2章使用合成Black–Scholes标签：通用逼近不保证优化或导数准确，光滑激活也不保证凸性。
第3–5章讨论粗糙Bergomi代理及描述性周度Deribit曲面，区分标签噪声、隐含波动率反演偏差、参数边界与局部优化。
第6–7章的路径导数标签相互相关；高斯过程的核与噪声模型是工作假设，点态标准差不是认证区间。
第8–10章的BSDE及停止求解器有离散、训练与模拟误差；布朗暴露不是股票股数，训练迭代波动不是置信区间。
第11–14章报告有限样本风险，区分无索赔基准、投资需求与对冲，并披露结构带的硬夹持和持续宽度限制。
第15章仅展示带惩罚局部搜索的模型敏感性，没有认证稳健上下界。
第16章给出解析高斯反向示例及有限签名诊断。第17–19章区分公开报道、建议控制与尚未完成的跨生成器验证。
研究章严格区分连续总体损失、欧拉损失及移动训练平均。

本轮恢复32项旧缓存中的29项，使用原始正常固定种子命令。`generator`、`ddpm_reverse`及`crossgen`
使用截至2025年的比特币历史，且第三项回放与拟合历史重叠，因此有意不运行，也不展示其分数。
高斯示例不拟合市场数据，验证章不声称经验检验已完成。投资封存窗口未开启。
保留的2024–2025年Deribit报价仅用于描述性代理拟合示例，不是投资记分板策略结果。
没有新增登记市场配置；第17部分累计试验数保持312，全局保持23,562。计数器不表示没有任何模型训练。
复现命令见英文段落；不要用旧版全项目计算命令绕过这三个排除项，也不要使用强制刷新。
旁白估计63.7分钟；渲染成功、字幕覆盖或音频抽查不能替代视觉审批及连续聆听。

## 交易台问题解答

**为何是立方根带宽？** 反射误差的风险成本与半宽平方成比例，换手成本与半宽倒数成比例，最小化其和得到立方根。
静态二次与线性项的比较推不出该结论。

**如何核查校准？** 独立重定价并报告数值不确定性，检查训练区域，区分标签、代理、优化与模型误差。
参数落在盒内及报价拟合良好，不代表模型被识别。

**为何记录导数？** 有效路径导数以适度伴随计算及计算带内存增加局部形状信息，但标签相关，且须论证微分与期望可交换。
数字期权路径导数几乎处处为零，不代表价格导数为零。

**平均盈利是否说明复制更好？** 不是。实际漂移与风险目标可能产生有意的投资需求；应明确测度，比较暴露与风险，
并在无差异溢价中减去优化后的无索赔基准。

## 十道习题完整解答

1. **现金不变性与卖方溢价。** γ>0且指数矩有限时，ρ(X+c)=γ⁻¹log E exp(−γX−γc)=ρ(X)−c。
   设交易收益为Gδ、成本为Cδ，在相同容许策略集上令rZ=infδρ(−Z+Gδ−Cδ)、r0=infδρ(Gδ−Cδ)。
   收到p后优化风险为rZ−p，故无差异条件给出p=rZ−r0。在鞅测度、收益可积、成本非负且允许零交易时，
   Jensen给出r0≥0，零策略给出r0≤0，故基准为零。实际漂移下未必为零。
   对数正态尾部下离散少对冲的看涨期权，可能经验指数风险有限而总体指数风险无限。

2. **反射带换手及缩放。** 局部误差dε=a dW+dL−dU限制于[−h,h]。平稳时对ε²用Itô：
   0=a²−2h E[dL+dU]/dt，总换手率为a²/(2h)。均匀平稳误差方差为h²/3。
   取a²=σ²S²Γ²，每单位时间目标为J(h)=γσ²S²h²/6+cSσ²S²Γ²/(2h)。令导数为零，
   得h³=3cSΓ²/(2γ)。这是系数局部缓变、小成本、连续再平衡的渐近近似，不是每日神经策略精确最优解。

3. **BSDE及单位。** 对dXi=μiXi dt+σXi dWi使用Itô，
   dY=(u_t+𝓛u)dt+ΣiσXi∂iu dWi。若PDE为u_t+𝓛u=f(u)，f(y)=[(1−δ)Q(y)+R]y，
   终值u(T,X)=min Xi，则Zi=σXi∂iu。因此Zi是布朗增量暴露，股票持仓为Δi=Zi/(σXi)。
   仅用股票对冲布朗风险，不能完美覆盖发行人违约。存在唯一性及PDE表示各需其可积性、Lipschitz、马尔可夫与正则条件。

4. **微分回归正规方程。** 价格特征矩阵Φ为n×p，导数特征为Dj，导数标签为zj。
   最小化‖Φw−y‖²+λΣj‖Djw−zj‖²，求导得到
   (ΦᵀΦ+λΣjDjᵀDj)w=Φᵀy+λΣjDjᵀzj。奇异时需选广义解或明确正则化；相关及异方差标签可能需要不同加权模型。

5. **停止规则下界。** 令gn为贴现执行支付，Gnext为固定续持策略的贴现支付。给定Fn，目标为
   gnF+E[Gnext|Fn](1−F)，在F∈[0,1]上仿射，故gn≥E[Gnext|Fn]时停止最优；相等时任选。
   仅条件于Xn需要充分马尔可夫状态。每个容许固定停止时τ满足E[gτ]≤supτ′E[gτ′]。
   模拟样本均值可能因抽样误差超过真正最优值；下界针对期望。评估应独立于拟合策略的选择。

6. **Leland成本约定。** 凸期权的小步近似为E|ΔΔ|≈ΓσS√Δt√(2/π)。单边比例成本c产生单位时间成本
   cΓσS²√(2/π)/√Δt。把它吸收入½σ²S²Γ，得
   σ̂²=σ²+2cσ√(2/π)/√Δt=σ²[1+√(2/π)k/(σ√Δt)]，其中往返成本k=2c。
   必须明确单边或往返约定。这是光滑伽马、高斯增量近似，不是精确有限成本复制或一般效用价格。

7. **Merton投资叠加。** 在无摩擦、完全、常波动模型dS/S=μdt+σdW中，利率为零、采用指数效用且索赔可复制，
   对冲Δ与无索赔投资问题分离。若投资金额为π，HJB一阶条件为μVx+πσ²Vxx=0。
   CARA满足−Vxx/Vx=γ，故π=μ/(γσ²)，总股数δ*=Δ+μ/(γσ²S)。
   复制使无差异比较中的优化投资机会抵消，因此完全市场溢价与μ无关。每日限制、成本和有限拟合不必精确恢复该理想解。

8. **验证标签噪声。** 令Y=F(θ)+ε，E[ε|θ]=0；验证噪声给定θ后与已拟合预测器独立，且
   E Var(ε|θ)=s²。展开平方并取期望：E(F̂−Y)²=E(F̂−F)²+s²。
   这是总体恒等式，有限样本实现的均方根误差不必超过s。标签方差加倍不能确定拟合器如何变化。
   隐含波动率反演非线性，可使有限路径标签有偏，故该恒等式不一定精确适用于这些标签。

9. **连续线性总体损失。** 对可预测控制，要求E∫₀ᵀe^{2R(T−t)}|Zt|²dt有限。解线性方程得
   YT=e^{RT}y0+∫₀ᵀe^{R(T−t)}Zt·dWt。目标表示为
   g=e^{RT}u0+∫₀ᵀe^{R(T−t)}Z*t·dWt。相减、平方、取期望；随机积分均值为零，
   用Itô等距得Lpop=e^{2RT}(y0−u0)²+E∫₀ᵀe^{2R(T−t)}|Z−Z*|²dt。
   因此|y0−u0|≤e^{−RT}√Lpop。已知总体损失为9、R=.02、T=1，价格误差不超过
   3e^{−.02}≈2.9406。仅观察训练损失9，不能得到此认证。

10. **阶梯控制、欧拉与速率。** 均匀网格宽h，无权可预测投影为
    Zbar_i=E[h⁻¹∫ti^{ti+h}Z*t dt|Fti]；带权最优投影使用权重e^{2R(T−t)}的条件加权平均。
    若E|Z*t−Z*s|²≤C|t−s|，测试左端点控制Zi=Z*ti可得
    E∫|Zstep−Z*|²dt≤CT h/2；有界确定性指数权重仍保持O(h)。
    这是上界，允许更小甚至为零的误差底；既不证明精确1/N速率，也不证明Ω(1/N)下界。
    欧拉驱动是另一方案。令a=1+Rh>0，则E[YN−g]=aᴺy0−e^{RT}u0，
    故|e^{−RT}aᴺy0−u0|≤e^{−RT}√Lpop,Euler。不能直接用连续系数从欧拉批次损失认证原始y0。
    Han–Long非线性定理还需其正则及耦合条件、足够小的步长，以及这里未计算的常数。

研究图把不同权重及批次的损失取移动平均；末20、40或10个保存点均值，不是对单个冻结模型总体损失的独立估计。
非线性单位系数阴影省略定理常数与离散项，因此仅是诊断图。
主要论文与监管原始来源链接见英文参考段落。SR 26-2是不具强制约束力、按风险调整的监管指导，
主要相关于资产超过三百亿美元的银行，并明确排除生成式与代理式人工智能；排除不等于无需治理。
2022年公开报道支持Euro Stoxx棘轮上线及标普扩展计划，不支持未经核实的2018年起香草期权账簿主张。
