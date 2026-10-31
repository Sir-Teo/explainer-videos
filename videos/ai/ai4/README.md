# AI, Built — Part 4: Change

Part 4 of the thirty-one-part series on how modern AI works and how it came to be
([plan](../README.md), [syllabus](../SYLLABUS.md)): the calculus of learning. This part derives derivatives,
gradients and Jacobians as best linear approximations; differentiates real layers; compares forward and reverse
mode; builds and checks the series' own autodiff library; and trains a letter model. Floating point, activation
recomputation, curvature, constraints and implicit differentiation complete the picture.

The results below describe the completed **31 October 2026 cloud run**, not universal performance guarantees.
Its 23 numerical items completed successfully and were recorded current by the computation driver. The
[validation receipt](../../../docs/qa/evidence/ai4-readme-validation/README.md) records exact source and artifact
hashes, metric definitions and independent checks. Numerical completion does not establish rendered visual QA or
narration/playback approval.

* **Four billion derivatives.** Recall q − p̂ for natural-log cross-entropy; a loss in bits multiplies this gradient
  by 1/ln 2. Show GPT-2 and Qwen3-4B parameter counts with independent provenance, the schematic parameter sea,
  the calculus timeline from 1684 to 2022, and the plan. Full-parameter training differentiates every trainable
  parameter; frozen-parameter or adapter training has a different scope.
* **1. The derivative.** Surprise −log₂p under a lens; secants approaching the tangent; the definition
  f(x+h) = f(x) + f′(x)h + o(h); the measured best-line error; Leibniz and Newton; derivation of
  s′(¼) = −4/ln 2; exponential, logarithm and chain-rule local stretch factors. The shown finite intervals are
  illustrative, and the final number line is drawn six times smaller.
* **2. Many inputs: the gradient.** Partial slices and a tangent plane at the same point used for the measurements;
  differentiability and Cauchy–Schwarz give steepest ascent along a nonzero gradient, descent against it, and zero
  first-order change along contour tangents. A finite difference sweeps 720 unique directions (721 samples include
  the repeated endpoint). Cauchy's descent update follows.
* **3. Maps that bend: the Jacobian.** A nonlinear grid and its local linear map, the m × n definition, local area
  factor |det J|, and correctly ordered matrix chain rule. Jacobians multiply; spectral norms satisfy
  ‖J_L⋯J_1‖₂ ≤ ∏ₗ‖Jₗ‖₂, generally with strict inequality. The product norm is maximum possible directional
  amplification, also for its transpose in backpropagation. A norm below one contracts every unit direction;
  a norm above one permits growth in some direction. Depth curves show mean log₁₀ norms and seed min–max bands.
* **4. The Jacobians of real layers.** Matrix-product VJPs XᵀG and GWᵀ; a dense Jacobian versus its contracted
  evaluation; softmax diag(p) − ppᵀ and its linear-cost VJP; epsilon-aware layer normalization before learned
  affine scale/shift. Theory has exact null directions; computed eigenvalues retain numerical roundoff signs.
* **5. Forwards or backwards?** JVPs, VJPs and contraction order; full input Jacobians across 25 networks; parameter
  gradients of a 16–32–10 classifier with 874 parameters. Counted dense derivative work and observed wall time are
  reported separately. The parameter reverse count requests W₁,b₁,W₂,b₂ and excludes dX for the constant input.
  The forward count describes this dense tangent implementation, not a lower bound on optimized forward AD.
* **6. Backpropagation, by hand.** Scalar sigmoid/squared-error example, fan-in addition, two-layer tanh/softmax
  cross-entropy, rank-one per-example matrix gradients and their batch sum; checks against the library and PyTorch.
* **7. Calculus in a few pages of code.** Multiplication's VJP, reverse traversal, topological order, values and
  gradients on a Wengert list; central finite-difference and PyTorch checks; related frameworks and code examples.
* **8. Training with our library.** The first gradient of Part 1's letter-pair model, then 729 raw scores trained
  with Adam for 1,500 updates. The heatmap displays normalized **log q(j|i)**, not raw scores z. Correlation is
  between log q and log counted conditionals on the 552 entries with counted probability > 10⁻⁴. The optimization
  objective uses nats; reported losses use bits per transition. Minibatch curve row t evaluates pre-update
  parameters t−1, while snapshot t is post-update. A separate full-batch GD experiment tracks five step sizes
  and the curvature-dependent stability scale.
* **9. Numbers in a computer.** IEEE 754, normal/subnormal numbers, float32, bfloat16, float16 and FP8 E5M2/E4M3FN layouts;
  enumerated ulp staircases, rounding and accumulation, overflow, and stable log-sum-exp. Relative round-to-nearest
  precision bounds apply in the normal finite range; subnormal spacing gives an absolute-error regime instead.
* **10. Cancellation, and the gradient check.** (1 − cos x)/x² and its stable rewrite; central/forward truncation
  and roundoff error; V-curves on eight identical normalized directions shared by both precisions. A plotted
  optimum is the argmin of the plotted median error curve, distinct from the median of individual optima.
* **11. Memory: storing or recomputing.** Logical retained activations and the leading-order n/k + k model;
  checkpointing, recomputed forward-layer evaluations and gradient agreement. This count excludes weights,
  gradients, temporaries and allocator/process memory. Timing uses a separate 1,024-layer width-64 chain.
* **12. Curvature, and Newton's method.** Hessian, bowl/saddle and local quadratic model; logistic regression with
  condition number about 187. Newton's reported first hit uses gradient norm < 10⁻¹⁰; GD uses objective gap to the
  final numerical Newton reference < 10⁻¹⁰. These are different criteria, and the reference is not a certified exact
  optimum. Explicit budgets and convergence states remain recorded.
* **13. Hessian-vector products.** Hv = ∇(∇f·v), comparison with a full 371 × 371 Hessian and finite differences;
  power iteration targets the **signed eigenvalue of largest absolute value**, assuming a unique dominant magnitude and a nonzero initial component in its eigendirection.
  The trained 2–16–16–3 network's six spectra and decision maps concern 300 training examples. Relative thresholds
  classify negative, flat and outlier eigenvalues; a zero count below a threshold does not establish positive
  semidefiniteness. Top curvature initially increases and later decreases as training progresses.
* **14. Descent on a quadratic; saddles.** For a symmetric positive-definite Hessian, stability 0 < η < 2/λmax and
  the worst-case Euclidean error contraction (κ−1)/(κ+1) at the optimal constant step. Measured norm thresholds,
  explicit iteration caps, the unstable step-size edge, saddle escape and an invariant zero-gradient direction.
* **15. Constraints: Lagrange multipliers.** Local tangency at a constrained extremum, Lagrangian and multiplier;
  circle optimization, maximum-entropy die and KL-regularized policy. Solver status/residuals accompany numerical
  comparisons. The entropy exponential-family parameter and the positive KL penalty coefficient are separate uses
  of the symbol β.
* **16. Inequalities, KKT and duality.** Necessary KKT conditions under a constraint qualification, weak duality,
  and convex strong-duality assumptions. The hard-margin SVM has a free intercept b: its dual requires α ≥ 0 and
  Σᵢαᵢyᵢ = 0. Positive α implies a tight margin; a tight margin need not imply positive α in a degenerate solution.
  The nonconvex example uses finite x/λ grids and reports estimates, not certified continuous dual bounds.
* **17. Differentiating through a fixed point.** Implicit derivatives when I−J is invertible, with a contraction
  sufficient for convergence. The initial example has eight state coordinates; the trained example has twelve
  state coordinates and 181 trainable parameters. Weight-norm caps, fixed-point residual tolerances, iteration
  budgets and converged/capped counts are explicit. A capped iterate is not an exact equilibrium derivative.
* **Recap.** Connections, bilingual problems and solutions, Part 5's teaser, and references.

## Run

```sh
python tools/make.py ai4                         # compute, then narrated English/Chinese builds
python -m videos.ai.ai4.compute                  # numerical items; Part 1's books in .cache/ai1
python tools/build.py ai4                        # English
python tools/build.py ai4 --lang zh              # Chinese
EXPLAINER_TTS=silent python tools/build.py ai4 -q l --fps 15
```

Finish the numerical jobs before rendering or dry-running scenes: an ordinary missing-data load can compute.
The cache records recipe/source/library identity and external dependencies; cached-only QA must reject stale or
missing results without computing. The current driver's 23 per-item subprocess durations sum to **63.72 seconds**,
including those subprocesses' startup and cache publication, and excluding corpus preparation, rendering and
narration. This is one observed cloud run, not an expected runtime on every machine.

`params` reads bounded header/config/index metadata from canonical files at pinned repository revisions, without
loading full model weights. This run counted both models from headers: GPT-2 124,439,808 and Qwen3-4B 4,022,468,096.
Each model records its revision, header hashes and counting policy. A failed read may independently return a labeled
historical fallback; it must not be described as a fresh measurement.

Benchmark records name the software, declared one-thread environment, warmup, repetitions and individual timings.
Native threadpool introspection was unavailable in this run. Timings are fixed-order local observations, with no
confidence interval; work counts are a separate algebraic convention. In particular, the parameter-mode timing uses
one forward repetition and twenty reverse repetitions, while HVP timing uses 200 of each.

## The series' autodiff library

`explainer/ai/autodiff.py` supplies `topological_order(root)`, `tape(root)` and `sigmoid(z)` as well as the operations
used here. `backward()` accumulates requested leaf gradients; transient intermediate sensitivities are not all
exposed as persistent `.grad` fields. The tape omits constant inputs. The matrix-product VJP supports 2-D arrays;
the unrolled fixed-point check keeps the state as a 1 × d row.

## Current computed results

These values are rounded from the hashed current artifacts, with cohorts and units retained. Comparisons report
observed errors, not exact mathematical equality of floating-point arrays.

| Item | Current result and scope |
|---|---|
| parameter counts | GPT-2 124,439,808; Qwen3-4B 4,022,468,096; both pinned headers, no historical fallback |
| best line / tangent plane | log-error slopes 1.998 (true scalar slope), 1.013 (slope 10% off), 2.001 (plane) |
| steepest ascent | finite-difference maximum 0.812625; gradient norm 0.812631; directions 0.207° apart |
| Jacobians through depth | mean log₁₀ norm at depth 60: gains 0.5/0.9/1/1.5/2 → −17.432/−2.464/−0.186/+2.146/+4.567; eight seeds |
| matrix-product VJP cost | 7,421,703,487,488 dense Jacobian entries; 29.69 decimal TB float32; 4,831,838,208 conventional FLOPs (2 per MAC), equivalent to 2,415,919,104 MACs for XᵀG; actual formula/library difference 0 |
| softmax / layernorm Jacobians | formula/library max differences 5.55e−17 / 1.94e−16; smallest stored eigenvalues −3.12e−17 / −2.12e−16; layernorm radial eigenvalue 9.93e−6 (ε=1e−5), before learned affine parameters |
| forward / reverse mode | cheaper counted input mode faster in 20/20 unequal-count networks; classifier P=874: 33,114,112 / 37,888 counted dense MACs plus tanh-derivative terms, ratio 874×; local parameter timing ratio 64.81×; gradient difference 4.16e−17 |
| scalar hand backprop | squared loss 0.854038; ∂L/∂w = −0.259143 |
| two-layer backprop | max differences to library/PyTorch 3.47e−17 / 5.55e−17; per-example dW rank 1 and batch-of-eight rank 4 under relative 1e−10 threshold |
| library gradient check | sampled central finite differences 2.20e−10; PyTorch 2.78e−17; 256 parameters |
| letter model | train/held-out 3.334868/3.335963 bits per transition; counting 3.330892; normalized-log-conditional correlation 0.996100 on 552 masked entries |
| first letter-model gradient | formula/library maximum difference 1.87e−14 on 300,000 training pairs |
| full-batch letter GD | λmax initially 0.0070756, at counting solution 0.0260055; 2/λmax ≈ 282.66/76.91; last-500-step mean losses at η≈2.83/28.27/56.53/84.80/141.33: 3.349622/3.332321/3.331538/3.355413/3.581980 bits; final-window monotonicity true/true/true/false/false |
| repeated addition of 0.01, 10,000 times | float32 100.002953; float16 32; bfloat16 4; bfloat16 inputs with float32 accumulator 100.097656 |
| cancellation at x=1e−4 | naive float32 (1−cos x)/x² = 0; stable rewrite = 0.5 |
| V-curve, fp64 | plotted median central-curve minimum at h=3.981e−5, error 6.473e−13; central model prediction 5.105e−5; median individual optimum 3.246e−5; forward-curve minimum error 8.132e−10 at h=1e−7 |
| V-curve, fp32 | plotted median central-curve minimum at h=0.015849, error 2.070e−6; central prediction 0.041493; paired eight directions; fp64 fitted right/left slopes +2.000/−0.884; fp32 right slope unavailable, left −0.895 |
| activation checkpointing | n=256: retained activations 257 → 32 (minimum at k=13…20); at k=16 forward-layer evaluations 256 → 496; keep-none 3 activations / 33,152 evaluations; max gradient difference 0; separate n=1024,width=64 local timing ratio 1.145× |
| Newton / GD | κ=186.73; Newton gradient-norm first hit at step 4 of cap 12; GD objective-gap first hit at step 2,362 of cap 200,000; both threshold 1e−10 in their respective units |
| HVP / trained Hessian | full-Hessian difference 1.08e−17; local HVP/gradient timing ratio 2.294×; finite-difference best 2.30e−9 at h=5.623e−5; final signed dominant-magnitude eigenvalue +0.00655422 |
| trained spectrum | λ < −0.01ρ count 72 → 0; λ > 0.1ρ count 56 → 4; fraction with abs(λ) ≤ 0.01ρ reaches 94.609%; final actual minimum −8.36e−6; ρ is spectral radius, and accuracy is training accuracy |
| SPD quadratics / valley | measured contraction rates match (κ−1)/(κ+1) to roundoff; κ=1000 needs 6,908 steps for relative iterate norm <1e−6; κ=25 valley reaches 1% in 26 steps; descent step cap 20,000 |
| saddle | escape to abs(y)>0.5 for all twelve starts within cap 4,999; initial y from 1e−1 to 1e−12 gives 19…284 steps; zero-axis gradient after 300 steps 2.81e−14 |
| Lagrange / entropy / KL | circle λ=0.625943, stationarity residual 1.56e−8; die parameter β=0.371049, numerical comparison 5.87e−9; KL coefficient β=0.5, comparison 2.98e−8; all three solver success flags true |
| free-intercept SVM | primal/dual ≈0.726908423262; absolute numerical gap 8.88e−16; Σαy residual 2.66e−15; complementarity residual 4.73e−16; positive multipliers and tight margins both at zero-based indices 2,5,17 in this run |
| nonconvex grid example | primal/dual-grid estimates −1.070230/−1.750000, estimated gap 0.679770; x-grid 440,001 points, spacing 1e−5 on [−2.2,2.2]; λ-grid 601 points, spacing 0.01 on [0,6] |
| implicit differentiation | initial 8-state solve converges in 29 iterations; unrolled relative-error fit 0.4603 per step, local ρ(J)=0.385982, error at K=60 8.76e−13; trained 12-state/181-parameter loss 0.106452 → 1.854e−6; mean training solve iterations 10.3125 → 28.25; final one-input solve 22; relative 200-unroll comparison 3.37e−13 |

The DEQ stores weight spectral-norm caps 0.8 (initial example) and 0.9 (training), and fixed-point solve cap 2,000.
All 38,448 training/evaluation solves (801 parameter states × 48 examples, including the final evaluation) and 540
fit-grid solves converged; capped/nonfinite counts were zero. Their residual tolerance is 1e−10; the separate initial
and final one-input solves use 1e−12. These counts are separate from the 800 optimizer updates and from unrolled
reference evaluations.

## Fact-check notes

* Cauchy's note: *Comptes rendus* 25, 536–538 (1847), on solving simultaneous equations (Lemaréchal, "Cauchy and the
  gradient method", *Doc. Math.* 2012).
* Wengert, "A simple automatic derivative evaluation program", *Comm. ACM* 7(8), 463–464 (1964).
* Linnainmaa's 1970 master's thesis (Helsinki) and BIT 16 (1976); Werbos's 1974 Harvard thesis; Kelley (1960) and
  Bryson (1961) as in Schmidhuber's survey (2015).
* FP8 E4M3/E5M2: Micikevicius et al., arXiv:2209.05433 (2022): E4M3 max 448 and no infinities, E5M2 IEEE-like.
* The Brandeis dice problem's year varies between sources (1957, 1962, 1963); the film names only Jaynes (1957) for
  the principle.
* Newton (1669), Raphson (1690), Simpson (1740): Ypma, "Historical development of the Newton–Raphson method",
  *SIAM Review* 37 (1995).
* Framework dates: Theano (Bergstra et al., SciPy 2010), Chainer (Tokui et al., 2015), TensorFlow (released November
  2015; Abadi et al. 2016), PyTorch (public release 2017; Paszke et al. 2017, 2019), JAX (Frostig, Johnson & Leary,
  SysML 2018).

## Problems, with solutions

1. **The softmax Jacobian.** Show J = diag(p) − ppᵀ is positive semidefinite, vᵀJv = Var_p(v), and J1 = 0.
   *Solution.* vᵀJv = Σᵢpᵢvᵢ² − (Σᵢpᵢvᵢ)² = Var_p(v) ≥ 0; (J1)ᵢ = pᵢ − pᵢΣⱼpⱼ = 0.
   Equality in the variance holds for vectors constant on the support of p. If all pᵢ>0, the null space is span(1).
2. **Forward against reverse.** For L≥2 dense layers with hidden width w mapping ℝⁿ→ℝᵐ, count dense
   multiply-accumulates (MACs) for a full input Jacobian, holding weights fixed.
   *Solution.* The primal dense work is F = nw + (L−2)w² + wm, plus nonlinearities. Each input JVP or output VJP
   is comparable to one primal pass, so full-Jacobian work is O(F+nF) or O(F+mF), with implementation-dependent
   constants. For a scalar loss, reverse mode needs one output seed rather than a seed for each input/parameter.
   This comparison is distinct from timing and from counting all scalar multiplication/addition operations.
3. **The best finite-difference step.** For positive coefficients in the model
   E(h)=(h²/6)|f‴|+u|f|/h with h>0, find h*; repeat for the forward-difference model.
   *Solution.* E′(h)=h|f‴|/3−u|f|/h²=0 gives h*=(3u|f|/|f‴|)^(1/3) and
   E(h*)=½(3u|f|)^(2/3)|f‴|^(1/3), of order u^(2/3). For
   E(h)=h|f″|/2+2u|f|/h, h*=2√(u|f|/|f″|) and E(h*)=2√(u|f||f″|), of order u^(1/2).
   These model balances assume nonzero derivative coefficients and a valid truncation/roundoff regime; they do not
   guarantee a particular empirical optimum. The current fp64 median curves reach 8.132e−10 forward and 6.473e−13
   central absolute error.
4. **Checkpoints.** Minimize the leading-order logical activation model n/k+k, ignoring integer/end effects;
   show two checkpoint levels give O(n^(1/3)) storage.
   *Solution.* −n/k²+1=0 gives k=√n and M=2√n. Two levels give M=n/k₁+k₁/k₂+k₂;
   k₂=n^(1/3), k₁=n^(2/3) yield M=3n^(1/3), with additional forward recomputation.
   This model excludes weights, gradients, workspace and allocator memory; it is not a measured process-memory bound.
5. **Descent on an SPD quadratic.** Let H=Hᵀ≻0, 0<λmin≤λmax, κ=λmax/λmin and
   η=2/(λmin+λmax). For f(x)=½xᵀHx, prove a worst-case Euclidean error bound and estimate the steps to relative
   norm ε, where 0<ε<1 and x₀≠0 (x₀=0 is already optimal).
   *Solution.* In an orthonormal eigenbasis, cᵢ←(1−ηλᵢ)cᵢ, so
   ‖x_t‖₂≤ρ^t‖x₀‖₂ with ρ=(κ−1)/(κ+1). The endpoint eigenvalues attain ±ρ; interior factors have magnitude
   at most ρ, so arbitrary initial errors need not shrink by exactly ρ at every step. For κ>1, the sufficient
   worst-case count is ceil[ln(1/ε)/ln((κ+1)/(κ−1))], approximately (κ/2)ln(1/ε) for large κ.
   For κ=1 one step reaches zero. Function-gap contraction is bounded by ρ^(2t), rather than ρ^t.
   The current κ=1000 two-dimensional example, initialized in the endpoint eigendirections, needs 6,908 steps
   for relative iterate norm <1e−6.
6. **The KL-regularized closed form.** On a finite action set, assume finite rewards, β>0, π_ref(a)>0 for every
   action and Σₐπ_ref(a)=1. Maximize Σₐπ(a)r(a)−βΣₐπ(a)ln(π(a)/π_ref(a)) over the probability simplex.
   *Solution.* The interior stationarity equation is
   r(a)−β[ln(π(a)/π_ref(a))+1]−λ=0, giving π*(a)=π_ref(a)e^{r(a)/β}/Z with
   Z=Σₐπ_ref(a)e^{r(a)/β}. This candidate is positive and normalized. Strict concavity for β>0 makes it the unique
   global maximizer; its objective value is β ln Z. At β=0 the formula is undefined; a reference with zeros requires
   restricting the optimization to its support rather than dividing by zero.

## 习题与解答

1. **softmax 的雅可比矩阵。** 证明 J=diag(p)−ppᵀ 半正定，vᵀJv=Var_p(v)，且 J1=0。
   *解答。* vᵀJv=Σᵢpᵢvᵢ²−(Σᵢpᵢvᵢ)²=Var_p(v)≥0；(J1)ᵢ=pᵢ−pᵢΣⱼpⱼ=0。
   方差为零时，v 在 p 的支撑集上为常数；若每个 pᵢ>0，零空间恰好是 span(1)。
2. **前向与反向。** 对 L≥2、隐藏层宽度 w、从 ℝⁿ 到 ℝᵐ 的全连接网络，固定权重，数完整输入雅可比矩阵的稠密乘加次数（MAC）。
   *解答。* 前向值计算的稠密工作为 F=nw+(L−2)w²+wm，另有非线性操作。一个输入 JVP 或输出 VJP 的代价与一次前向同阶，
   所以完整雅可比矩阵约为 O(F+nF) 或 O(F+mF)，常数随实现而变。标量损失只需一个反向输出种子。
   这些计数不同于墙钟时间，也不同于把乘法和加法分别计数的标量操作数。
3. **有限差分的最佳步长。** 对正系数模型 E(h)=h²|f‴|/6+u|f|/h、h>0，求最优步长，再求前向差分模型的结果。
   *解答。* E′(h)=h|f‴|/3−u|f|/h²=0，得到 h*=(3u|f|/|f‴|)^(1/3)，
   E(h*)=½(3u|f|)^(2/3)|f‴|^(1/3)，量级为 u^(2/3)。前向模型 E(h)=h|f″|/2+2u|f|/h，
   得 h*=2√(u|f|/|f″|)、E(h*)=2√(u|f||f″|)，量级为 u^(1/2)。这些平衡需要非零导数系数及有效的截断/舍入近似，
   不保证某个实测最优值。本次 fp64 中位数曲线的最小绝对误差为：前向 8.132e−10，中心 6.473e−13。
4. **检查点。** 忽略整数和端点效应，最小化逻辑激活存储模型 n/k+k，并证明两级检查点可达 O(n^(1/3))。
   *解答。* −n/k²+1=0 给出 k=√n、M=2√n。两级时 M=n/k₁+k₁/k₂+k₂；
   k₂=n^(1/3)、k₁=n^(2/3)，得到 M=3n^(1/3)，代价是额外的前向重计算。
   这个模型不含权重、梯度、工作区或分配器内存，不是实测进程内存上界。
5. **对称正定二次函数上的下降。** 设 H=Hᵀ≻0，0<λmin≤λmax，κ=λmax/λmin，
   η=2/(λmin+λmax)。对 f(x)=½xᵀHx，证明欧氏误差范数的最坏情况上界，并估计到相对范数 ε（0<ε<1、x₀≠0）的步数；x₀=0 已经最优。
   *解答。* 在正交特征基下 cᵢ←(1−ηλᵢ)cᵢ，因此 ‖x_t‖₂≤ρ^t‖x₀‖₂，ρ=(κ−1)/(κ+1)。
   两端特征值的因子为 ±ρ，其余因子的绝对值至多为 ρ；任意初始误差不一定每步恰好缩小到 ρ 倍。
   κ>1 时，最坏情况的充分步数为 ceil[ln(1/ε)/ln((κ+1)/(κ−1))]，大 κ 时约为 (κ/2)ln(1/ε)。
   κ=1 时一步归零。函数值误差的收缩上界是 ρ^(2t)，不是 ρ^t。本次 κ=1000 的二维例子从两端特征方向出发，
   在 6,908 步达到相对迭代范数 <1e−6。
6. **KL 正则化的闭式解。** 有限动作集上，奖励有限，β>0，每个 π_ref(a)>0 且 Σₐπ_ref(a)=1。
   在概率单纯形上最大化 Σₐπ(a)r(a)−βΣₐπ(a)ln(π(a)/π_ref(a))。
   *解答。* 内点驻点满足 r(a)−β[ln(π(a)/π_ref(a))+1]−λ=0，因此 π*(a)=π_ref(a)e^{r(a)/β}/Z，
   Z=Σₐπ_ref(a)e^{r(a)/β}。这个分布严格为正且归一化；β>0 使目标严格凹，所以它是唯一全局最大值，目标值为 β ln Z。
   β=0 时公式没有定义；若参考分布含零概率，必须把问题限制在其支撑集上，不能直接除以零。

## References

Books: A. Griewank & A. Walther, *Evaluating Derivatives*, 2nd ed. (2008); M. Blondel & V. Roulet, *The Elements of
Differentiable Programming* (2024); J. Nocedal & S. J. Wright, *Numerical Optimization*, 2nd ed. (2006); S. Boyd &
L. Vandenberghe, *Convex Optimization* (2004); N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed.
(2002); I. Goodfellow, Y. Bengio & A. Courville, *Deep Learning* (2016).

Papers: Cauchy (1847); Karush (1939); Kuhn & Tucker (1951); Jaynes (1957); Kelley (1960); Bryson (1961); Wengert
(1964); Linnainmaa (1970, 1976); Werbos (1974); Speelpenning (1980); IEEE 754 (1985); Rumelhart, Hinton & Williams
(1986); Goldberg (1991); Griewank (1992); Boser, Guyon & Vapnik (1992); Pearlmutter (1994); Cortes & Vapnik (1995);
Bergstra et al., Theano (2010); Dauphin et al. (2014); Tokui et al., Chainer (2015); Abadi et al., TensorFlow (2016);
Chen et al., *Training Deep Nets with Sublinear Memory Cost* (2016); Sagun, Bottou & LeCun (2016); Jin et al. (2017);
Amos & Kolter, OptNet (2017); Paszke et al. (2017, 2019); Frostig, Johnson & Leary, JAX (2018); Baydin et al. (2018);
Bai, Kolter & Koltun, *Deep Equilibrium Models* (2019); Rajeswaran et al., iMAML (2019); Karpathy, micrograd (2020);
Micikevicius et al., *FP8 Formats for Deep Learning* (2022).

## Glossary (new terms of this part)

| English | 中文 |
|---|---|
| derivative; best linear approximation | 导数；最好的线性近似 |
| tangent plane; partial derivative; directional derivative | 切平面；偏导数；方向导数 |
| steepest ascent; Cauchy–Schwarz inequality | 最陡上升；柯西–施瓦茨不等式 |
| Jacobian (matrix) | 雅可比矩阵 |
| Jacobian-vector product (JVP), vector-Jacobian product (VJP) | 雅可比-向量积，向量-雅可比积 |
| forward mode, reverse mode | 前向模式，反向模式 |
| computation graph, topological order | 计算图，拓扑顺序 |
| tape, Wengert list | 磁带（运算记录），文格特列表 |
| define-by-run, static graph, tracing | 边运行边定义，静态图，追踪 |
| error signal δ, outer product, rank one | 误差信号δ，外积，秩为1 |
| floating point; sign, exponent, mantissa | 浮点数；符号位，指数，尾数 |
| unit in the last place (ulp), unit roundoff | 最后一位单位（ulp），单位舍入误差 |
| overflow, underflow, NaN | 溢出，下溢，非数（NaN） |
| log-sum-exp trick | log-sum-exp技巧 |
| loss scaling | 损失缩放 |
| (catastrophic) cancellation, truncation error | （灾难性）抵消，截断误差 |
| central / forward difference, gradient check | 中心差分 / 前向差分，梯度检验 |
| checkpointing (activation recomputation) | 检查点（激活重计算） |
| Hessian, curvature | 黑塞矩阵，曲率 |
| Newton's method, quadratic convergence | 牛顿法，二次收敛 |
| Hessian-vector product (Pearlmutter's trick), power iteration | 黑塞-向量积（珀尔马特技巧），幂迭代 |
| Hessian spectrum: bulk, outliers | 黑塞谱：主体，离群值 |
| condition number κ; stability edge 2/λmax | 条件数κ；稳定边界2/λmax |
| saddle point, escape | 鞍点，逃离 |
| Lagrange multiplier, Lagrangian, shadow price | 拉格朗日乘子，拉格朗日函数，影子价格 |
| maximum entropy, Boltzmann distribution | 最大熵，玻尔兹曼分布 |
| KKT conditions, complementary slackness | KKT条件，互补松弛 |
| dual function, weak / strong duality, duality gap, Slater's condition | 对偶函数，弱对偶 / 强对偶，对偶间隙，斯莱特条件 |
| support vector, margin | 支持向量，间隔 |
| implicit function theorem, fixed point | 隐函数定理，不动点 |
| deep equilibrium model (DEQ), unrolling, contraction, spectral radius | 深度平衡模型（DEQ），展开，压缩映射，谱半径 |
