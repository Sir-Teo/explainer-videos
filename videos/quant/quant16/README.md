# Quant, Built — Part 16: Computing Prices

Part 16 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), closing Act III, Derivatives. It covers:

* Monte Carlo and its error, and the variance reduction that shrinks the constant: antithetics, control variates,
  importance sampling;
* quasi-Monte Carlo: Sobol points, and the Brownian bridge that makes them work on paths;
* multilevel Monte Carlo;
* American options by regression (Longstaff–Schwartz), bracketed by a duality upper bound (Andersen–Broadie);
* Greeks by bumping, pathwise and likelihood ratio, and all of them at once by adjoint differentiation (AAD);
* finite differences: the theta schemes, Rannacher's start, the American put as a complementarity problem;
* ADI schemes for Heston on non-uniform grids;
* Fourier pricing (Carr–Madan, COS), a race between every method, and what hardware buys.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's
[`engine`](../../../explainer/quant/house/engine.py), tested), on one CPU core. No market data are used: the
products are textbook cases (Black–Scholes with 20% volatility and 5% rates; Heston with v₀ = θ = 0.04, κ = 1.5,
ξ = 0.5, ρ = −0.7), so every method can be checked against an exact or near-exact price.

*An education in methods, not investment advice. Firms and episodes are described from the public record.*

## Chapters (about 50 minutes)

* **One price, many machines.** A one-year Heston call priced by simulation, a grid and two Fourier methods: the
  same answer at costs that differ by orders of magnitude. Then the objectives and the House.
* **1. Monte Carlo, and variance reduction.**
  * Boyle (1977): a price is an expectation, and the error is σ_f/√n in any dimension. For an at-the-money call
    (σ_f ≈ 19), one cent of accuracy needs about 3 million plain paths.
  * Error against paths, for plain Monte Carlo, antithetics and a control variate (the stock): the line drops but keeps
    slope −½. Sobol points change the slope: at 262,144 points the error is about 3 × 10⁻⁵, against 0.026 plain.
  * Importance sampling for a call struck at 160, in the money on 1.4% of paths: a normal shifted toward the strike
    cuts the standard error from 0.0059 to 0.0006, worth about a hundred times the paths.
* **2. Quasi-Monte Carlo, and the Brownian bridge.**
  * 256 random points clump; 256 Sobol points (1967) fill every small box.
  * An Asian option on 64 fixings: Sobol points fed step by step help, but the Brownian bridge (Caflisch, Morokoff
    and Owen 1997), which spends the best coordinates on the path's end and midpoints, cuts the spread about 31 times
    against random paths at 16,384 paths.
* **3. Multilevel Monte Carlo.**
  * Giles (2008): a telescoping sum of corrections between step sizes; many paths on coarse levels, few on fine
    ones. Cost about ε⁻² (log ε)² instead of ε⁻³.
  * On a continuously averaged Asian call under Euler, multilevel is 4, 12 and 26 times cheaper than a standard
    estimator at the same finest step for ε = 0.04, 0.02 and 0.01. The corrections' variance falls two- to threefold
    per level.
* **4. American options by simulation.**
  * Longstaff–Schwartz (2001): regress the realized continuation values on today's price, exercise where the payoff
    beats the fit. The rule is a real strategy, so its value is a lower bound: 6.061 for an at-the-money one-year put
    with 25 exercise dates (the European put is worth 5.574).
  * The dual (Rogers 2002; Haugh–Kogan 2004) and Andersen–Broadie (2004): the upper bound falls from 6.41 with 50 inner
    paths to 6.075 with 1,600, pinning the price in [6.061, 6.075]. With exercise at any time it is worth a little more:
    6.090 on a 2,000-step tree, 6.085 by the PDE.
* **5. Greeks, and adjoint differentiation.**
  * Three Monte Carlo estimators (Broadie–Glasserman 1996). For a call, bump, pathwise and likelihood ratio agree on
    delta 0.637; pathwise is the least noisy. For a digital the pathwise derivative is zero almost everywhere; the
    likelihood ratio's standard error is a third of the bump's.
  * AAD (Giles–Glasserman 2006, "smoking adjoints"): record the pricing on a tape, sweep it backwards. On an Asian
    option with 20,000 paths, five sensitivities cost 2.2 prices by AAD against 7.4 by bumping, with the series' own
    autodiff from *AI, Built*. The ratio stays constant as the inputs grow.
* **6. Finite differences.**
  * The theta scheme: explicit, fully implicit, Crank–Nicolson (1947). On a 100-point grid the explicit scheme gives
    10.411 with 2,000 steps; with 200 it explodes to about −7 × 10¹⁰.
  * Convergence: at the finest grids, doubling cuts Crank–Nicolson's error 4.0 times and the implicit scheme's 3.0
    times, falling toward 2.
  * A digital a week before expiry: Crank–Nicolson's gamma rings around the strike; Rannacher's (1984) two implicit
    half-steps remove it.
* **7. ADI for Heston.**
  * Heston's PDE in price and variance, split into directions: Douglas and Craig–Sneyd (1988), on in 't Hout–Foulon
    (2010) non-uniform grids.
  * From 20 to 160 price points the error falls from about 0.2 to 0.001–0.002; the finest grid takes under a second.
* **8. Fourier methods, and the race.**
  * Carr–Madan (1999) damped FFT and COS (Fang–Oosterlee 2008). COS with 128 terms (error 1.4 × 10⁻⁶) beats
    Carr–Madan with 16,384 points (2.5 × 10⁻⁵); with 256 terms its error is 5 × 10⁻⁸.
  * The race on one core: Monte Carlo's best (standard error 0.016 at 320,000 paths, 3 s), ADI (0.002 in 0.8 s), and
    COS beating Monte Carlo's accuracy in about 0.2 ms. Fourier for vanillas; grids for low-dimensional early exercise
    and barriers; simulation for everything else.
* **9. Hardware: grids, GPUs and quantum.** The overnight risk run; JPMorgan's 2011 move of its credit-derivative
  risk model onto Maxeler FPGAs (eight hours to about four minutes, as reported); Chakrabarti et al. (2021): quantum
  advantage in derivative pricing needs about 7,500 logical qubits and a T-depth of 54 million. COS beat Monte Carlo's
  best accuracy about 14,000 times faster on one core: algorithms first.
* **10. The pricing engine.** Rule 16: every price leaves the engine with its error (a standard error, a duality gap or
  a grid-refinement difference), and every method is checked nightly against an independent one. The trial counter
  stays at 73.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant16.compute                    # every number (mlmc and american take about a minute each)
EXPLAINER_TTS=silent python tools/qa_scene.py quant16 Fourier    # one chapter, silent, with a contact sheet
python tools/make.py quant16 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **How many paths for a price to one basis point?**
   * The standard error is σ_f/√n, so n ≈ (σ_f/ε)².
   * For a one-year at-the-money call the payoff's standard deviation is about 19, so ε = 0.01 needs about 3.5 million
     plain paths.
   * A control variate (here, about three times less error, so about nine times fewer paths) or Sobol points (orders of magnitude
     less error for a smooth one-dimensional payoff) cut that sharply. Quote the error with the price.
2. **Why is AAD's cost independent of the number of Greeks?**
   * The price is a composition of elementary operations. Reverse mode carries the adjoint ∂V/∂(intermediate) backward
     through the recorded tape, one multiply-add per edge.
   * One sweep yields ∂V/∂x for every input x at once; its cost is a small constant (here 2.2) times one pricing, for
     five inputs or five thousand.
   * Bumping needs one extra pricing per input (two for central differences). The price is memory: the tape stores the
     forward pass, so desks checkpoint long simulations.
3. **Crank–Nicolson gives the right price for a digital, but the gamma oscillates. Why, and the fix?**
   * Crank–Nicolson's amplification factor tends to −1 for the highest-frequency modes when the time step is large
     against the grid: they flip sign each step and barely decay.
   * A payoff with a jump or a kink is full of such modes, so they survive into the solution near the strike, and
     differentiating twice magnifies them.
   * Rannacher: start with a few fully implicit (half-)steps, which damp those modes strongly, then switch to
     Crank–Nicolson; the scheme stays second order.

## Problems, with solutions

1. **The optimal control variate.**
   * Var(Y − b(C − E C)) = Var Y − 2b Cov(Y, C) + b² Var C, a quadratic in b minimized at b* = Cov(Y, C)/Var C.
   * Substituting: Var Y − Cov(Y, C)²/Var C = Var Y (1 − ρ²_{YC}).
2. **Importance sampling's shift.**
   * Draw Z from N(θ, 1) instead of N(0, 1). The likelihood ratio is φ(z)/φ(z − θ) = exp(−θz + θ²/2), so
     E[f(Z)] = E_θ[f(Z) e^{−θZ + θ²/2}].
   * For a call struck at K, pick θ so the shifted mean lands on the strike: S₀ exp((r − σ²/2)T + σ√T θ) = K, so
     θ = (ln(K/S₀) − (r − σ²/2)T)/(σ√T).
3. **The duality bound.**
   * For any stopping time τ, optional stopping gives E[M_τ] = M₀ = 0, so E[h_τ] = E[h_τ − M_τ] ≤ E[max_t (h_t − M_t)].
   * Taking the supremum over τ gives the bound. Equality holds for the martingale part of the Snell envelope.
4. **Stability of the explicit scheme.**
   * For u_t = a u_xx, the explicit update u_j^{n+1} = u_j^n + λ(u_{j+1}^n − 2u_j^n + u_{j−1}^n), λ = aΔt/Δx².
   * Substituting u_j^n = g^n e^{ijkΔx}: g = 1 − 4λ sin²(kΔx/2).
   * |g| ≤ 1 for every k iff λ ≤ ½. For Black–Scholes, a = σ²S²/2 is largest at S_max, giving Δt ≤ ΔS²/(σ²S_max²).
5. **Why reverse mode is cheap.**
   * f(g(h(x))) has Jacobian J_f J_g J_h. Forward mode multiplies right to left, carrying an n-column matrix, so it costs
     about n evaluations.
   * Reverse mode multiplies left to right, starting from the 1 × m row of a scalar output, so every product is a row
     vector: a constant multiple of one evaluation, whatever n is (Griewank's cheap gradient principle).

## Data and reproducibility

* No market data: all products are textbook cases with exact or near-exact references (Black–Scholes formulas,
  2,000-step trees, COS with 4,096 terms on a wide range).
* Wall-clock times are from one core of the build machine (best of five runs for the fast methods); they will differ
  on other hardware, but their ratios are what the part uses.
* Monte Carlo errors are reported as standard errors or as root-mean-square errors over repeated seeds.
* No strategy was tested; the trial counter is unchanged at 73.

---

# 量化金融，从零搭建 — 第16部分：计算价格

本部分讲：

* 蒙特卡洛及其误差，以及缩小常数的方差缩减：对偶变量、控制变量、重要性抽样；
* 拟蒙特卡洛：Sobol点，以及让它们在路径上起作用的布朗桥；
* 多层蒙特卡洛；
* 用回归为美式期权定价（Longstaff–Schwartz），并用对偶上界夹住（Andersen–Broadie）；
* 用扰动、路径法和似然比计算希腊字母，以及用伴随微分（AAD）一次算出全部；
* 有限差分：θ格式、Rannacher起步、作为互补问题的美式看跌期权；
* 非均匀网格上求解赫斯顿模型的ADI格式；
* 傅里叶定价（Carr–Madan、COS）、所有方法之间的竞赛，以及硬件能买到什么。

所有数字都由本系列自己的代码在一个CPU核上算出。不使用市场数据：产品都是教科书案例，因此每种方法都能与精确或近乎精确的价格核对。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录。*

## 交易台问题与解答

1. **要把价格算到一个基点，需要多少条路径？**
   * 标准误差是σ_f/√n，所以n ≈ (σ_f/ε)²。
   * 一年期平值看涨期权的收益标准差约为19，所以ε = 0.01需要约350万条普通路径。
   * 控制变量（这里误差约小三倍，路径约少九倍）或Sobol点（对光滑的一维收益，误差小几个数量级）能大幅减少路径。报价时要同时报误差。
2. **为什么AAD的成本与希腊字母的个数无关？**
   * 价格是基本运算的复合。反向模式沿着记录下来的计算带，把伴随量∂V/∂(中间量)向后传，每条边一次乘加。
   * 一次反向扫描就同时得到对每个输入x的∂V/∂x；其成本是一次定价的一个小常数倍（这里是2.2倍），无论有五个输入还是五千个。
   * 扰动法每个输入都要多定价一次（中心差分要两次）。AAD的代价是内存：计算带要存下前向过程，所以长模拟要设检查点。
3. **克兰克-尼科尔森给出数字期权的正确价格，但Gamma振荡。为什么？怎么修？**
   * 当时间步相对网格较大时，克兰克-尼科尔森格式对最高频模式的放大因子趋于−1：它们每步变号，几乎不衰减。
   * 带跳跃或拐点的收益充满这类模式，于是它们在行权价附近残留在解中，求两次导数又把它们放大。
   * Rannacher的办法：先走几个完全隐式的（半）步，强力衰减这些模式，再切换到克兰克-尼科尔森；格式仍是二阶的。

## 习题与解答

1. **最优控制变量。**
   * Var(Y − b(C − E C)) = Var Y − 2b Cov(Y, C) + b² Var C，是b的二次函数，在b* = Cov(Y, C)/Var C处取最小。
   * 代入得Var Y − Cov(Y, C)²/Var C = Var Y (1 − ρ²_{YC})。
2. **重要性抽样的平移。**
   * 从N(θ, 1)而不是N(0, 1)中抽Z。似然比为φ(z)/φ(z − θ) = exp(−θz + θ²/2)，所以E[f(Z)] = E_θ[f(Z) e^{−θZ + θ²/2}]。
   * 对行权价为K的看涨期权，选θ使平移后的均值落在行权价上：S₀ exp((r − σ²/2)T + σ√T θ) = K，即θ = (ln(K/S₀) − (r − σ²/2)T)/(σ√T)。
3. **对偶上界。**
   * 对任意停时τ，可选停时定理给出E[M_τ] = M₀ = 0，所以E[h_τ] = E[h_τ − M_τ] ≤ E[max_t (h_t − M_t)]。
   * 对τ取上确界即得上界。取Snell包络的鞅部分时等号成立。
4. **显式格式的稳定性。**
   * 对u_t = a u_xx，显式更新为u_j^{n+1} = u_j^n + λ(u_{j+1}^n − 2u_j^n + u_{j−1}^n)，λ = aΔt/Δx²。
   * 代入u_j^n = g^n e^{ijkΔx}，得g = 1 − 4λ sin²(kΔx/2)。
   * 对所有k都有|g| ≤ 1，当且仅当λ ≤ ½。对布莱克-斯科尔斯，a = σ²S²/2在S_max处最大，得Δt ≤ ΔS²/(σ²S_max²)。
5. **为什么反向模式便宜。**
   * f(g(h(x)))的雅可比矩阵是J_f J_g J_h。前向模式从右往左乘，携带n列的矩阵，成本约为n次求值。
   * 反向模式从左往右乘，从标量输出的1 × m行向量开始，每次乘积都是行向量：无论n多大，都是一次求值的常数倍（Griewank的“廉价梯度原理”）。
