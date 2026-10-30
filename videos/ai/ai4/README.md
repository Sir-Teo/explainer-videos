# AI, Built — Part 4: Change

Part 4 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)): the calculus of learning. Every training step needs the derivative of the loss
with respect to every number in the model, 124,439,808 of them for GPT-2 and 4.02 billion for Qwen3-4B. This part
derives the derivative, gradient and Jacobian as best linear approximations; computes the Jacobians of real layers;
counts forward against reverse mode; backpropagates by hand; builds and checks the series' own autodiff library
(`explainer/ai/autodiff.py`) and trains with it; shows what floating point does to all of it; trades memory for
recomputation; uses curvature (Newton, Hessian-vector products, a trained network's Hessian, descent on quadratics,
saddles); and optimizes under constraints (Lagrange, KKT, duality) before differentiating through a fixed point. The
history runs from Leibniz and Newton through Cauchy, Lagrange, Karush, Kuhn and Tucker, Wengert, Linnainmaa, Werbos
and Rumelhart, Hinton and Williams, to IEEE 754, bf16 and FP8, and to Theano, TensorFlow, PyTorch and JAX. Everything
is computed by `compute.py`, small and on the CPU (about a minute in all).

* **Four billion derivatives** (hook). Part 1's single derivative, q − p̂; GPT-2's and Qwen3-4B's parameter counts
  (read from their weight files' headers); how we got here, 1684 to 2022, evenly spaced; the plan.
* **1. The derivative.** Part 1's surprise curve under a lens, straightening as the zoom grows; secants closing on the
  tangent; the definition (f(x+h) = f(x) + f′(x)h + r(h), r(h)/h → 0) as a card; measured: the error of the
  straight-line guess falls like h^2.00 with the true slope and like h^1.01 with a slope 10% off, so exactly one line
  is best; Leibniz's *Nova Methodus* (1684), Newton's fluxions; the derivative of the surprise from the definition
  (s′(¼) = −4/ln 2 = −5.77); eˣ, ln x and the chain rule as stretch factors on three number lines.
* **2. Many inputs: the gradient.** Partial derivatives as slices of a surface (3D); the tangent plane (its error
  falls like r^2.00, measured); the gradient as steepest ascent, derived with Cauchy–Schwarz on a ladder (theorem
  card); measured by finite differences in 720 directions: the steepest slope 0.8126 equals |∇f| = 0.8126, the two
  directions 0.21° apart; Cauchy (1847) and the update x ← x − η∇f.
* **3. Maps that bend: the Jacobian.** A map bending the plane; zoomed in, its grid straightens onto the Jacobian's;
  the definition card (m × n, the best matrix); the determinant as local area; the chain rule as a product of
  Jacobians.
* **4. The Jacobians of real layers.** The matrix product: ∂L/∂W = XᵀG and ∂L/∂X = GWᵀ derived; the Jacobian never
  formed (for one GPT-2 MLP matrix over 1,024 tokens it would hold 7.4 × 10¹² numbers, 30 TB in float32, against
  4.8 × 10⁹ multiply-adds for XᵀG); the softmax Jacobian diag(p) − ppᵀ by the quotient rule, computed and matched to
  the library (5.6 × 10⁻¹⁷), its zero row sums and non-negative eigenvalues (one zero), its O(n) product; layer norm's
  Jacobian (1/σ)(I − 11ᵀ/n − yyᵀ/n), matched (1.9 × 10⁻¹⁶), with two (near-)zero eigenvalues along 1 and y.
* **5. Forwards or backwards?** JVPs and VJPs (definition card); the chain J₄J₃J₂J₁ multiplied from the right
  (forward mode) or the left (reverse mode); counted on 25 two-hidden-layer networks with n, m ∈ {1, …, 256}: the whole
  Jacobian costs n forward passes forwards and m backwards, and timed, the cheaper mode by count was faster in 20 of
  20; a classifier with 874 parameters: forward mode needs 615× the multiply-adds of one backward pass (82× the time),
  the same gradient (4 × 10⁻¹⁷); Linnainmaa (1970), Werbos (1974), Rumelhart, Hinton & Williams (1986); Kelley (1960)
  and Bryson (1961).
* **6. Backpropagation, by hand.** One weight, one bias, a sigmoid and a squared error, forward (loss 0.854) and back
  (∂L/∂w = −0.259); fan-in adds; a two-layer network in matrices: δ₂ = q − e_y, ∂L/∂W₂ = δ₂a₁ᵀ, δ₁ = (W₂ᵀδ₂) ⊙ (1 − a₁²),
  ∂L/∂W₁ = δ₁xᵀ on a ladder; the per-example gradient computed: rank 1 (singular values 0.101, then 10⁻¹⁸), a batch of
  8 rank 4; by hand against the library 3.5 × 10⁻¹⁷ and PyTorch 5.6 × 10⁻¹⁷.
* **7. Calculus in a few pages of code.** The library as written; multiplication's VJP; `backward`; the topological
  order and the tape (the library's new `tape()` prints the worked example's Wengert list), values down it and
  gradients up it; Wengert (1964); checked against finite differences (2.2 × 10⁻¹⁰) and PyTorch (2.8 × 10⁻¹⁷);
  the family: Speelpenning (1980), Theano (2010), Chainer and TensorFlow (2015), PyTorch (2017), JAX (2018), with the
  same line in ours, PyTorch and JAX.
* **8. Training with our library.** The first gradient of Part 1's letter-pair model derived, (nᵢ/N)(1/27 − p̂_{j|i}),
  matched by the library on 300,000 pairs (1.9 × 10⁻¹⁴), its largest pushes on the commonest pairs; 729 scores trained
  (Adam, 1,500 steps): from log₂27 = 4.75 bits to 3.33, the counting answer, the scores becoming the log counts
  (correlation 0.995), with the text they write at each checkpoint; full-batch gradient descent at five step sizes,
  with the Hessian's top eigenvalue tracked: 0.0071 at the start (allowing η < 283) but 0.026 at the counting answer
  (η < 77); η = 57 settles at 3.332 bits, η = 85 never settles, its curvature hovering at 2/η (the edge of stability,
  Part 11).
* **9. Numbers in a computer.** IEEE 754 (1985, Kahan); bit layouts of float32, bfloat16, float16, FP8 E5M2 and E4M3
  (largest 3.4 × 10³⁸, 3.4 × 10³⁸, 65,504, 57,344, 448; 7.2, 2.4, 3.3, 0.9 and 1.2 digits); the ulp staircase across
  10⁻⁸ … 10⁶, enumerated from every bit pattern; rounding (1 + 1/256 = 1 and 257 = 256 in bf16); adding 0.01 ten
  thousand times: float32 100.003, float16 stalls at 32, bf16 at 4, bf16 numbers with a float32 sum 100.098; e^z
  overflows above 88.7 in float32 and 11.1 in float16; scores 1000, 999, 998 → ∞ and NaN; the log-sum-exp trick on a
  ladder, and our library's `log_softmax`.
* **10. Cancellation, and the gradient check.** (1 − cos x)/x² in float32 and float64 (at x = 10⁻⁴ float32 gives 0),
  the predicted u/(x²/2) and the stable rewrite; the central difference's truncation and roundoff errors derived,
  h* = (3u|f|/|f‴|)^(1/3); the V-curves measured on chapter 7's network along 8 directions: float64's best step
  3 × 10⁻⁵ (predicted 5 × 10⁻⁵), float32's 3 × 10⁻² (predicted 4 × 10⁻²), slopes +2.00 and −1.00, best errors
  6 × 10⁻¹³ and 5 × 10⁻⁷.
* **11. Memory: storing or recomputing.** Why reverse mode stores activations; checkpoints every k layers, memory
  n/k + k minimized at k = √n (ladder); measured on a 256-layer chain: 257 activations held when everything is kept,
  a flat minimum of 32 for k from 13 to 20 (√256 = 16), at the price of 496 layer evaluations against 256 (33,152 if
  nothing is kept); longer chains' best k 5, 9, 16, 32, 64 for n = 16 … 4,096; identical gradients; 1.27× the time;
  Griewank (1992), Chen et al. (2016).
* **12. Curvature, and Newton's method.** The Hessian, a bowl and a saddle (3D); Newton's step from the second-order
  Taylor model; Newton (1669), Raphson (1690), Simpson (1740); logistic regression with correlated features (κ = 187):
  gradient descent 2,362 steps to 10⁻¹⁰, Newton 3, correct digits 2, 5, 11 (quadratic convergence), paths on the
  contours.
* **13. Hessian-vector products.** Pearlmutter's Hv = ∇(∇f·v) (1994) on a ladder; checked against the full 371 × 371
  Hessian (10⁻¹⁷), about 2–3 gradients' cost, finite differences of gradients best at 2 × 10⁻⁹; power iteration with
  products alone finds the top eigenvalue; a 2–16–16–3 network trained on three spirals with its full Hessian at 6
  checkpoints, replayed with its decision regions: negative eigenvalues 72 → 0, outliers 56 → 4, 95% within 1% of zero
  at the end, the spectrum shrinking with the loss; Sagun et al. (2016).
* **14. Descent on a quadratic; saddles.** x ← (I − ηH)x in H's eigenvectors; stability η < 2/λmax; the best rate
  (κ − 1)/(κ + 1) derived; the κ = 25 valley (26 steps to 1%), momentum, Newton; measured rates for κ = 1 … 1,000
  equal to the formula; steps to 10⁻⁶ ∝ κ (6,908 at κ = 1,000); the valley's steps grow from η = 0.082 (2/λmax =
  0.08); a saddle: escape time 24.1 steps per factor of ten in y₀ (predicted 24.2), stuck exactly on the line with
  gradient 3 × 10⁻¹⁴; Dauphin et al. (2014), Jin et al. (2017).
* **15. Constraints: Lagrange multipliers.** The picture: gradients parallel at the constrained minimum on a circle
  (the tangential part read off as the point slides); Lagrange (1788); the Lagrangian on a ladder; x* = (0.783, 0.622),
  λ = 0.626, residual 1.6 × 10⁻⁸; λ as a price; maximum entropy for a die averaging 4.5 (Jaynes 1957): a softmax with
  β = 0.371, checked against a general solver (6 × 10⁻⁹); the KL-regularized closed form π* ∝ π_ref e^{r/β} (DPO,
  Part 27), checked (3 × 10⁻⁸).
* **16. Inequalities, KKT and duality.** Karush (1939), Kuhn & Tucker (1951); the KKT conditions (theorem card) with
  the inactive and active cases; the dual function, weak and strong duality on a ladder; min x² s.t. x ≥ 1 (no gap) and
  a non-convex double well (p* = −1.07, d* = −1.75, gap 0.68); a hard-margin SVM on 20 points solved as primal and dual:
  0.726908 both, 3 support vectors exactly where α > 0 (complementary slackness to 5 × 10⁻¹⁶); Boser, Guyon & Vapnik
  (1992).
* **17. Differentiating through a fixed point.** The implicit function theorem on a ladder, dz*/dθ = (I − J)⁻¹∂f/∂θ,
  as a VJP; a tiny deep equilibrium layer (8 numbers, fixed point in 30 iterations): backprop through K unrolled steps
  closes in geometrically (0.446 per step; ρ(J) = 0.386) to 3 × 10⁻¹³; a 12-number DEQ trained with implicit gradients
  only, replayed (loss 0.106 → 1.9 × 10⁻⁶, 11 → 29 iterations to equilibrium; matched against 200 unrolled steps to
  10⁻¹³); Bai, Kolter & Koltun (2019), iMAML (2019), OptNet (2017).
* **Recap**, where it comes back, problems, Part 5's teaser, references.

## Run

```
python tools/make.py ai4                         # computations, then the narrated film in English and Chinese
python -m videos.ai.ai4.compute                  # the numbers only (about a minute; Part 1's books in .cache/ai1)
python tools/build.py ai4                        # English
python tools/build.py ai4 --lang zh              # Chinese
EXPLAINER_TTS=silent python tools/build.py ai4 -q l --fps 15     # a quick silent preview
```

Everything is seeded and runs on the CPU in about a minute (one or two threads). `params` reads GPT-2's and
Qwen3-4B's weight-file headers over the network; offline, it uses the counts read when this part was made.

## The series' autodiff library

`explainer/ai/autodiff.py` gained three additive functions for this part (no existing behaviour changed; Part 9's
imports and results are unaffected): `topological_order(root)` (the order `backward` uses), `tape(root)` (the graph as
a Wengert list: index, operation, inputs, shape) and `sigmoid(z)` (a single node, derivative s(1 − s)). The library's
matrix product differentiates both factors only for 2-D arrays; chapter 17's unrolled check therefore keeps the state
as a 1 × d row.

## Computed results

| Item | Result |
|---|---|
| best line | error ∝ h^1.998 (true slope), h^1.013 (slope 10% off); tangent plane r^2.001 |
| steepest ascent | max of 720 directional derivatives 0.81263 = ‖∇f‖ 0.81263, 0.21° apart |
| softmax / layer norm Jacobians | formula vs library 5.6e-17 / 1.9e-16; eigenvalues ≥ 0 with one 0 / two ≈ 0 |
| forward vs reverse | n vs m forward passes exactly; timing agrees with the count in 20/20 networks; 874 parameters: 615× multiply-adds, 82× time |
| two-layer backprop | hand vs library 3.5e-17, vs PyTorch 5.6e-17; per-example dW rank 1 |
| library check | finite differences 2.2e-10, PyTorch 2.8e-17 |
| letter model | 3.335 bits (train), 3.336 (held out), counting 3.331; correlation with log counts 0.995 |
| first gradient | formula vs library 1.9e-14 on 300,000 pairs |
| step sizes (letter model) | λmax 0.0071 → 0.026; η = 2.8 still descending (3.350 at 3,000 steps); η = 28, 57 settle (3.332); η = 85, 141 bounce (3.355, 3.584) |
| accumulation of 0.01 × 10⁴ | float32 100.003, float16 32, bf16 4, bf16 + float32 sum 100.098 |
| V-curve | best h: float64 3.2e-5 (pred. 5.1e-5), float32 3.2e-2 (pred. 4.5e-2); best error 6.5e-13 / 5.4e-7 |
| checkpointing (n = 256) | peak 257 → 32 (k = 13…20), evaluations 256 → 496; keep-nothing 33,152; time 1.27× |
| Newton vs GD (κ = 187) | 3 steps vs 2,362 to 1e-10 |
| HVP | vs full Hessian 1e-17; 1.9–3.4 gradients' time (varies run to run); FD best 2.2e-9 |
| trained Hessian | negatives 72 → 0, outliers 56 → 4, 95% flat; λmax 0.96 → 2.2 → 0.0066 |
| GD on quadratics | measured rates = (κ−1)/(κ+1) to rounding; 6,908 steps at κ = 1,000; edge η = 0.082 |
| saddle | 24.1 steps per decade of y₀ (pred. 24.2); stuck gradient 2.8e-14 |
| Lagrange | λ = 0.626, residual 1.6e-8; die β = 0.371; RL closed form checked 3e-8 |
| SVM duality | p* = d* = 0.726908 (gap 9e-16), 3 support vectors; double-well gap 0.680 |
| DEQ | unrolled → implicit at 0.446/step (ρ = 0.386), floor 3e-13; trained 0.106 → 1.9e-6 |

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
   *Solution.* vᵀJv = Σᵢ pᵢvᵢ² − (Σᵢ pᵢvᵢ)² = E_p[v²] − E_p[v]² = Var_p(v) ≥ 0. (J1)ᵢ = pᵢ − pᵢΣⱼpⱼ = 0. Equality
   vᵀJv = 0 holds only for v constant on the support of p, so with all pᵢ > 0 the null space is exactly span(1).
2. **Forward against reverse.** A chain of L dense layers of width w maps ℝⁿ → ℝᵐ. Count the multiply-adds of its
   full Jacobian in each mode. *Solution.* One forward pass costs F = nw + (L − 2)w² + wm (plus O(Lw) for the
   nonlinearities). A JVP costs about F more, so the Jacobian by forward mode costs ≈ F + nF; a VJP costs about F, so
   reverse mode costs ≈ F + mF (plus storing the activations). Forward wins when n < m, reverse when m < n; for a loss
   (m = 1) reverse mode costs a small constant times one pass, whatever the number of parameters.
3. **The best finite-difference step.** With E(h) = (h²/6)|f‴| + u|f|/h, find h* and E(h*); repeat for the forward
   difference. *Solution.* E′(h) = (h/3)|f‴| − u|f|/h² = 0 ⇒ h* = (3u|f|/|f‴|)^(1/3), and
   since u|f|/h* = |f‴|h*²/3, E(h*) = |f‴|h*²/2 = ½(3u|f|)^(2/3)|f‴|^(1/3) ∝ u^(2/3). For the forward difference
   E(h) = (h/2)|f″| + 2u|f|/h, h* = 2√(u|f|/|f″|), E(h*) = 2√(u|f||f″|) ∝ u^(1/2): in float64 roughly 10⁻⁸ (relative)
   for the forward difference against 10⁻¹¹ for the central one; chapter 10 measured best errors 8 × 10⁻¹⁰ and
   6 × 10⁻¹³ (absolute).
4. **Checkpoints.** With a checkpoint every k of n layers, memory is n/k + k. Show k = √n is best, and that two levels
   reach O(n^(1/3)). *Solution.* d/dk (n/k + k) = −n/k² + 1 = 0 ⇒ k = √n, M = 2√n. With two levels, keep n/k₁
   coarse checkpoints; within a segment of k₁ layers keep k₁/k₂ fine ones and recompute k₂ at a time:
   M = n/k₁ + k₁/k₂ + k₂, minimized at k₂ = n^(1/3), k₁ = n^(2/3): M = 3n^(1/3), for about two extra forward passes.
5. **Descent on a quadratic.** For ½xᵀHx with η = 2/(λmin + λmax), show the error shrinks by (κ − 1)/(κ + 1) per step
   and about (κ/2) ln(1/ε) steps reach ε. *Solution.* In H's eigenbasis cᵢ ← (1 − ηλᵢ)cᵢ. With this η,
   1 − ηλmin = (λmax − λmin)/(λmax + λmin) = (κ − 1)/(κ + 1) and 1 − ηλmax = −(κ − 1)/(κ + 1); every other factor is
   smaller in size. Then ((κ − 1)/(κ + 1))ᵗ = ε gives t = ln(1/ε)/ln((κ + 1)/(κ − 1)) ≈ (κ/2) ln(1/ε) for large κ
   (ln((1 + 1/κ)/(1 − 1/κ)) ≈ 2/κ). Chapter 14 measured 6,908 steps at κ = 1,000 for ε = 10⁻⁶ (formula: 6,908).
6. **The KL-regularized closed form.** Maximize Σₐπ(a)r(a) − βΣₐπ(a)log(π(a)/π_ref(a)) subject to Σπ = 1.
   *Solution.* ∂/∂π(a) of the Lagrangian: r(a) − β(log(π(a)/π_ref(a)) + 1) − λ = 0 ⇒ π(a) = π_ref(a)e^{r(a)/β}/Z with
   Z = Σₐπ_ref(a)e^{r(a)/β}. Substituting, the objective is Σπ r − Σπ(r − β log Z) = β log Z. (The objective is
   concave, so this stationary point is the maximum.)

## 习题与解答

1. **softmax的雅可比矩阵。** 证明J = diag(p) − ppᵀ半正定，vᵀJv等于v在p下的方差，且J1 = 0。
   *解答。* vᵀJv = Σᵢ pᵢvᵢ² − (Σᵢ pᵢvᵢ)² = E_p[v²] − E_p[v]² = Var_p(v) ≥ 0；(J1)ᵢ = pᵢ − pᵢΣⱼpⱼ = 0。若所有pᵢ > 0，
   只有常数向量使vᵀJv = 0，所以零空间恰好是span(1)。
2. **前向与反向。** L层宽度为w的全连接网络把ℝⁿ映到ℝᵐ。分别数出两种模式求整个雅可比矩阵的乘加次数。
   *解答。* 一次前向计算约F = nw + (L − 2)w² + wm。每个雅可比-向量积约多花F，前向模式共约F + nF；每个向量-雅可比积约花F，
   反向模式共约F + mF（另需存下激活）。n < m时前向更省，m < n时反向更省；对损失（m = 1），反向模式只是一次前向的常数倍。
3. **有限差分的最佳步长。** 设E(h) = (h²/6)|f‴| + u|f|/h，求h*和E(h*)；再对前向差分做一遍。
   *解答。* E′(h) = 0 ⇒ h* = (3u|f|/|f‴|)^(1/3)；由u|f|/h* = |f‴|h*²/3，得E(h*) = ½(3u|f|)^(2/3)|f‴|^(1/3) ∝ u^(2/3)。
   前向差分E(h) = (h/2)|f″| + 2u|f|/h，h* = 2√(u|f|/|f″|)，E(h*) = 2√(u|f||f″|) ∝ u^(1/2)：在FP64里，前向差分的相对误差
   约10⁻⁸，中心差分约10⁻¹¹；第10章实测的最小（绝对）误差分别是8 × 10⁻¹⁰和6 × 10⁻¹³。
4. **检查点。** 每k层设一个检查点，内存为n/k + k。证明k = √n最好，两级检查点可达O(n^(1/3))。
   *解答。* 对k求导：−n/k² + 1 = 0 ⇒ k = √n，M = 2√n。两级时M = n/k₁ + k₁/k₂ + k₂，在k₂ = n^(1/3)、k₁ = n^(2/3)处
   取最小，M = 3n^(1/3)，代价约是多做两次前向计算。
5. **二次函数上的下降。** 对½xᵀHx取η = 2/(λmin + λmax)，证明误差每步缩小到(κ − 1)/(κ + 1)倍，约(κ/2)ln(1/ε)步到达ε。
   *解答。* 在H的特征基下cᵢ ← (1 − ηλᵢ)cᵢ；此η下两端的倍数为±(κ − 1)/(κ + 1)，其余更小。令((κ − 1)/(κ + 1))ᵗ = ε，
   t = ln(1/ε)/ln((κ + 1)/(κ − 1)) ≈ (κ/2)ln(1/ε)。第14章在κ = 1000、ε = 10⁻⁶时实测6908步，与公式相同。
6. **KL正则化的闭式解。** 在Σπ = 1下最大化Σπ(a)r(a) − βΣπ(a)log(π(a)/π_ref(a))。
   *解答。* 拉格朗日函数对π(a)求导为0：r(a) − β(log(π(a)/π_ref(a)) + 1) − λ = 0 ⇒ π(a) = π_ref(a)e^{r(a)/β}/Z，
   Z = Σπ_ref(a)e^{r(a)/β}；代回得最优值β log Z。目标是凹的，所以这个驻点就是最大值。

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
