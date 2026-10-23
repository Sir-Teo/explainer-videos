# AI, Built — Part 9: Networks

Part 9 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). How neural networks came to be, from the first artificial neuron to the block
inside today's language models: the perceptron and its convergence proof, what one layer cannot do and the winter that
followed, backpropagation, what one and many layers can represent, why deep networks were so hard to train and the
fixes (initialization, the edge of chaos, residual streams, normalization), modern activations and gating,
Kolmogorov–Arnold networks, and the first neural language model on the series' scoreboard. Every network here is
trained on this computer, by `compute.py` (PyTorch on the CPU, or the series' own autodiff from Part 4).

* **How we got here.** 1943 to 2012 on one strip, with the two winters shaded (schematic): McCulloch & Pitts,
  Rosenblatt, Minsky & Papert, backpropagation, LeCun's zip codes, deep belief nets, AlexNet. Then two interleaved
  spirals learned by a 2 → 32 → 32 → 32 → 2 ReLU network, replayed through twelve checkpoints with its decision
  regions, its linear pieces (thousands of them) and its accuracy curve.
* **1. The first neurons.** McCulloch & Pitts (1943): threshold units compute AND, OR, NOT, so networks of them
  compute any logical formula; Hebb's postulate (1949, quoted from p. 62); Rosenblatt's perceptron (1958: simulated
  on an IBM 704; the *New York Times* of 8 July 1958); the Mark I Perceptron (1960: 400 photocells, 512 association
  units, 8 response units, motor-driven potentiometers); Widrow & Hoff's ADALINE and the LMS rule (1960) derived as
  stochastic gradient descent on the squared error.
* **2. The perceptron learns.** The rule w ← w + y x on mistakes and its geometry; trained live on 50 separable
  points (13 mistakes over 5 passes); Novikoff's theorem (1962) proved on screen: k ≤ (R/γ)², with R and the best
  margin γ computed (bound 334); the bound against reality on six data sets of shrinking margin, 20 orders each (the
  worst run uses at most 16% of it); what it doesn't promise (the widest margin: Part 6's SVM).
* **3. XOR, and the first winter.** XOR is not linearly separable (four inequalities, a contradiction); the
  perceptron cycles forever on it; Minsky & Papert's *Perceptrons* (1969), parity and connectedness, and their
  "intuitive judgment that the extension is sterile" (pp. 231–232); Rosenblatt's death (1971), Fukushima's
  neocognitron (1980), Hopfield (1982). A 2–2–1 tanh network trained on XOR with the series' own autodiff, replayed:
  the input square's decision region and the hidden layer's bent grid, where the four points become separable; 7 of
  20 random starts solve it, the rest stop in a local minimum with one point wrong.
* **4. Backpropagation.** Credit assignment; the delta equations derived (δ^L = ∇L ⊙ φ′, δ^l = (W^{l+1})ᵀδ^{l+1} ⊙
  φ′, ∂L/∂W^l = δ^l a^{l−1 ᵀ}); values forward and errors backward as pulses; the cost (backward ≈ 2× forward, ~6
  operations per weight per example, Part 12's C ≈ 6ND); the XOR network's nine gradients three ways (our autodiff,
  the hand-written delta equations, finite differences) agreeing to 4·10⁻¹⁷ and 5·10⁻¹⁰; Linnainmaa (1970), Werbos
  (1974), Rumelhart, Hinton & Williams (1986), LeCun et al. (1989).
* **5. One layer can do anything.** A unit as a hinge; a curve from 2 to 64 hinges by least squares; the miss falls
  like n⁻² (the chord bound h²/8·max|f″| derived; measured slope −2.01); three hinges make a bump, bumps make any curve;
  the universal approximation theorem (Cybenko 1989; Hornik, Stinchcombe & White 1989; Leshno, Lin, Pinkus & Schocken
  1993) and what it doesn't say.
* **6. Escaping the curse of dimensionality.** A grid needs m^d points: miss ∝ n^{−2/d}; Maurey's argument derived
  (a Gaussian bump is an average of cosine units; n random units miss by ≤ 1/√n in any dimension); computed: grid
  slopes −2.0, −1.0, −0.57, −0.34 in d = 1, 2, 4, 8, against random-unit slopes −0.48 to −0.49 in d = 1 to 64;
  Barron's theorem (1993), his lower bound n^{−1/d} for fixed bases, and the catch.
* **7. What depth adds.** The tent map composed k times (2^k pieces from 2k units); Telgarsky's depth separation
  (2016); the plane folded by ReLU layers (alternate folds 2|t| − 1, 1 → 32 linear pieces, an F mirrored into every
  piece); one layer of n units cuts the plane into ≤ 1 + n + C(n,2) pieces (Zaslavsky 1975), counted for n = 1…6;
  Montúfar et al. (2014); 48 random units in 1 to 6 layers give about the same number of pieces (Hanin & Rolnick
  2019); the spiral network's pieces before and after training.
* **8. The second winter, and the revival.** Vanishing gradients (Hochreiter 1991; Bengio, Simard & Frasconi 1994)
  measured through 50 sigmoid layers with the 1990s initialization; SVMs (1995), LSTM (1997), LeNet (1998); CIFAR's
  program (2004); deep belief nets (Hinton, Osindero & Teh 2006) as greedy layer-wise pretraining (schematic); GPUs
  (Raina et al. 2009; Cireşan et al. 2010, plain backpropagation), Glorot & Bengio (2010), ReLUs, speech and AlexNet
  (2012), the 2018 Turing Award.
* **9. Initialization, derived.** 50 layers of 256 ReLUs: weights 0.7× too small shrink the signal about thirty
  million times, 1.4× too big grow it about ten million times; Var(z) = n·Var(W)·E[a²] derived: LeCun's 1/n_in, the
  backward 1/n_out, Glorot's 2/(n_in + n_out); ReLU keeps half: He's 2/n; a 3D ridge plot of a 50-layer tanh network's
  activation histograms through depth for the old U[−1/√n, 1/√n], Glorot's 1/n and 4/n.
* **10. The edge of chaos.** Mean-field theory (Poole et al. 2016; Schoenholz et al. 2017): the length map and its
  fixed point (cobweb); the correlation map and χ₁; ordered, critical and chaotic phases, against a real network of
  width 1,000; the phase diagram over (σ_w², σ_b²) for tanh, whose edge meets σ_b = 0 at σ_w² = 1.00 (Glorot), and
  χ₁ = σ_w²/2 for ReLU (He); the depth scale ξ_c and trainability, computed over depth × σ_w² with Schoenholz et
  al.'s 6ξ_c; ten-thousand-layer CNNs (Xiao et al. 2018).
* **11. The residual stream.** h + f(h); the identity in every block's Jacobian; 40 plain layers against 40
  residual layers on the spirals; inside both as they train (answers and per-layer gradients, replayed); the product
  (I + J_L)⋯(I + J_1) expanded into 2^L paths (Veit, Wilber & Belongie 2016); highway networks (2015), ResNet's 152
  layers, GPT-2's 1/√N.
* **12. Normalization.** BatchNorm (Ioffe & Szegedy 2015) and the covariate-shift debate (Santurkar et al. 2018);
  LayerNorm (Ba, Kiros & Hinton 2016); RMSNorm (Zhang & Sennrich 2019) as projection onto a sphere; the Jacobians
  derived ((√d/‖h‖)(I − ĥĥᵀ); LayerNorm also removes the all-ones direction) and measured by autograd (singular values
  15 equal + 1 zero; 14 + 2); scale invariance; post-norm (2017) against pre-norm (GPT-2, Xiong et al. 2020) in our
  24-block model: starting gradients by block and held-out bits; OLMo 2's output norm (2024) and Dynamic Tanh (2025).
* **13. The modern block.** Sigmoid, tanh, ReLU, GELU (Hendrycks & Gimpel 2016, derived from a Gaussian coin) and
  SiLU (Elfwing et al.; Ramachandran et al. 2017); gating (Dauphin et al. 2017) as a 3D surface; SwiGLU (Shazeer 2020)
  and the 8d/3 width; published configurations (GPT-2 4d; Llama 2 7B 11,008 = 8/3·4,096 rounded to 256; Llama 3 8B
  14,336; Qwen3-8B 12,288); the block assembled, Llama 3 8B counted from its configuration (41.9M attention + 176.2M
  MLP weights per block, 8.03B in all); an ablation in a 24-block character model on the novels: plain, + residual,
  + post-LN, + pre-LN, + pre-RMSNorm, + SwiGLU.
* **14. Kolmogorov–Arnold networks.** Hilbert's 13th problem (1900); Kolmogorov and Arnold (1957); Girosi & Poggio's
  "irrelevant" (1989) and Kůrková's "relevant" (1991); KANs (Liu et al. 2024); a [2, 5, 1] KAN and an MLP of the same
  size trained on exp(sin πx + y²), the KAN's fifteen learned curves replayed; KANs and MLPs by size; Yu, Yu & Wang's
  fairer comparison (2024), KAN 2.0, and what frontier models use.
* **15. A neural language model.** Bengio, Ducharme, Vincent & Jauvin's design (2003) for characters (24 characters
  of context, learned 32-number vectors, 1,024 tanh units, direct connections), trained on Part 1's books, replayed:
  the bits-per-character curve with what it writes at nine checkpoints; mixed with Part 7's Kneser–Ney (the weight
  chosen on held-out text); the output layer's character vectors; the scoreboard's new rows.
* **Recap** in eight computed pictures, where it comes back, six problems, Part 10's teaser, references.

Run from the repo root:

```
python tools/make.py ai9                 # everything: the computations, then the narrated cut in English and Chinese
python -m videos.ai.ai9.compute          # or just the numbers (every item; Part 1's books and Part 7's Kneser-Ney first)
python tools/build.py ai9                # English
python tools/build.py ai9 --lang zh      # Chinese
```

Every computation is seeded and resumes after an interruption. The language model (`lm`) is the long item: 24,000
steps of 512 positions, about two hours on two busy cores (much less on a laptop); it checkpoints every 500 steps
(`.cache/ai9/lm.ckpt.pt`) and keeps its final weights in `.cache/ai9/lm.pt`, so the analysis can be rerun without
retraining. The items made of many runs (`residual`, `trainable`, `block`, `kan`) save each run as it finishes
(`CACHE.partial`). Everything else takes a minute or two. Part 7's Kneser–Ney is read through Part 7's own cache
(`videos.ai.ai7.compute.load`), and the scoreboard through Part 1's; where Part 1's language-model rows (GPT-2,
Qwen3) have not been computed, the board shows Part 1's counting and compressor rows only, and the narration says so.

References: I. Goodfellow, Y. Bengio & A. Courville, *Deep Learning* (2016); S. J. D. Prince, *Understanding Deep
Learning* (2023); D. A. Roberts, S. Yaida & B. Hanin, *The Principles of Deep Learning Theory* (2022); M. Minsky &
S. Papert, *Perceptrons* (1969); D. E. Rumelhart, J. L. McClelland & the PDP Research Group, *Parallel Distributed
Processing* (1986); W. S. McCulloch & W. Pitts, *A Logical Calculus of the Ideas Immanent in Nervous Activity* (1943);
D. O. Hebb, *The Organization of Behavior* (1949); F. Rosenblatt, *The Perceptron* (1958); B. Widrow & M. E. Hoff,
*Adaptive Switching Circuits* (1960); A. B. J. Novikoff, *On Convergence Proofs on Perceptrons* (1962); S. Linnainmaa
(1970); P. Werbos, *Beyond Regression* (1974); D. E. Rumelhart, G. E. Hinton & R. J. Williams, *Learning
representations by back-propagating errors* (1986); Y. LeCun et al. (1989, 1998); G. Cybenko (1989); K. Hornik,
M. Stinchcombe & H. White (1989); M. Leshno, V. Lin, A. Pinkus & S. Schocken (1993); G. Pisier (1981); L. K. Jones
(1992); A. R. Barron, *Universal Approximation Bounds for Superpositions of a Sigmoidal Function* (1993); M. Telgarsky,
*Benefits of Depth in Neural Networks* (2016); T. Zaslavsky (1975); G. Montúfar, R. Pascanu, K. Cho & Y. Bengio
(2014); B. Hanin & D. Rolnick (2019); S. Hochreiter (1991); Y. Bengio, P. Simard & P. Frasconi (1994); C. Cortes &
V. Vapnik (1995); S. Hochreiter & J. Schmidhuber (1997); G. E. Hinton, S. Osindero & Y.-W. Teh (2006); R. Raina,
A. Madhavan & A. Y. Ng (2009); D. C. Cireşan, U. Meier, L. M. Gambardella & J. Schmidhuber (2010); X. Glorot &
Y. Bengio (2010); V. Nair & G. Hinton (2010); X. Glorot, A. Bordes & Y. Bengio (2011); K. He, X. Zhang, S. Ren &
J. Sun, *Delving Deep into Rectifiers* (2015) and *Deep Residual Learning* (2015); B. Poole et al. (2016); S. S.
Schoenholz, J. Gilmer, S. Ganguli & J. Sohl-Dickstein, *Deep Information Propagation* (2017); J. Pennington, S. S.
Schoenholz & S. Ganguli (2017); L. Xiao et al. (2018); R. K. Srivastava, K. Greff & J. Schmidhuber (2015); A. Veit,
M. Wilber & S. Belongie (2016); S. Ioffe & C. Szegedy (2015); S. Santurkar et al. (2018); J. L. Ba, J. R. Kiros &
G. E. Hinton (2016); B. Zhang & R. Sennrich (2019); R. Xiong et al. (2020); A. Radford et al., GPT-2 (2019); Team
OLMo, *2 OLMo 2 Furious* (2025); J. Zhu, X. Chen, K. He, Y. LeCun & Z. Liu, *Transformers without Normalization*
(2025); D. Hendrycks & K. Gimpel (2016); S. Elfwing, E. Uchibe & K. Doya (2017); P. Ramachandran, B. Zoph & Q. V. Le
(2017); Y. N. Dauphin, A. Fan, M. Auli & D. Grangier (2017); N. Shazeer, *GLU Variants Improve Transformer* (2020);
A. N. Kolmogorov (1957); V. I. Arnold (1957); F. Girosi & T. Poggio (1989); V. Kůrková (1991); Z. Liu et al., *KAN:
Kolmogorov–Arnold Networks* (2024) and *KAN 2.0* (2024); R. Yu, W. Yu & X. Wang, *KAN or MLP: A Fairer Comparison*
(2024); Y. Bengio, R. Ducharme, P. Vincent & C. Jauvin, *A Neural Probabilistic Language Model* (2003). Published
model configurations: each model's `config.json` on Hugging Face (GPT-2, Llama 2 7B, Llama 3 8B, Qwen3-8B).

## Problems, with solutions

**1. The learning rate doesn't matter.** Show that the perceptron started from w₀ = 0 makes exactly the same mistakes
with the update w ← w + η y x, for any η > 0, as with η = 1.

*Solution.* By induction, the weights with rate η are η times the weights with rate 1: both start at 0, and if
w^(η) = η w^(1) then sign(w^(η)·x) = sign(w^(1)·x), so the same examples are mistakes and the updates η y x and y x
keep the proportion. The rate only rescales w, and the sign of w·x never sees the scale.

**2. XOR with two ReLUs.** Find weights for a 2–2–1 ReLU network that computes XOR exactly on {0, 1}².

*Solution.* h₁ = max(0, x₁ + x₂), h₂ = max(0, x₁ + x₂ − 1), y = h₁ − 2h₂. For (0, 0): 0. For (0, 1) and (1, 0):
h₁ = 1, h₂ = 0, so 1. For (1, 1): h₁ = 2, h₂ = 1, so 0. The hidden layer folds the line x₁ + x₂ at 1, the tent of
chapter seven.

**3. How fast sigmoid gradients vanish.** For sigmoid units, show σ′ ≤ ¼. If every weight matrix has operator norm at
most 1, how fast can ‖δ^l‖ shrink with depth?

*Solution.* σ′ = σ(1 − σ), and a product of two numbers with sum 1 is at most (½)² = ¼. From δ^l = (W^{l+1})ᵀδ^{l+1}
⊙ σ′(z^l), ‖δ^l‖ ≤ ‖W^{l+1}‖ · max|σ′| · ‖δ^{l+1}‖ ≤ ¼‖δ^{l+1}‖, so ‖δ^l‖ ≤ 4^{−(L−l)}‖δ^L‖: at least a factor of 4
per layer, 10⁻¹² after twenty layers. Larger weights can offset it, which is what initialization is about.

**4. He's rule.** For z ~ N(0, q), show E[max(0, z)²] = q/2, and deduce Var(W) = 2/n.

*Solution.* By symmetry, ∫₀^∞ z² φ(z) dz is half of ∫ z² φ(z) dz = q. For z_i = Σ_j W_ij a_j with independent weights
of mean 0 and a_j = max(0, z_j^{prev}), Var(z) = n Var(W) E[a²] = n Var(W) q_prev / 2, which equals q_prev exactly when
Var(W) = 2/n.

**5. Depth counts pieces.** Show that the k-fold composition of the tent map t(x) = 1 − |2x − 1| on [0, 1] has 2^k
linear pieces, while one hidden layer of m ReLUs on ℝ has at most m + 1.

*Solution.* t maps [0, ½] and [½, 1] each linearly onto [0, 1]. If t^k has 2^k pieces, each mapping its interval
monotonically onto [0, 1], then on each piece t^{k+1} = t ∘ t^k breaks at the one point where t^k = ½, giving two
pieces that each map onto [0, 1]: 2^{k+1}. A one-layer network c + Σ a_i max(0, w_i x + b_i) is linear except at the m
kinks −b_i/w_i, so it has at most m + 1 pieces, and needs m ≥ 2^k − 1 units to equal t^k; k layers of 2 units do it.

**6. RMSNorm's Jacobian.** For y = √d h / ‖h‖, show ∂y/∂h = (√d/‖h‖)(I − ĥĥᵀ), with ĥ = h/‖h‖. What does this imply
about the gradient with respect to h?

*Solution.* ∂(h/‖h‖)/∂h = I/‖h‖ − h hᵀ/‖h‖³ = (I − ĥĥᵀ)/‖h‖. The matrix is symmetric and sends h to 0, so the gradient
Jᵀg = Jg is orthogonal to h: RMSNorm's input never gets a gradient along itself, and doubling h halves the gradient.

## 习题与解答

**1. 学习率无关紧要。** 证明：感知机从 w₀ = 0 出发，用更新 w ← w + η y x（任意 η > 0）犯的错误，和 η = 1 时完全一样。

*解答。* 用归纳法：学习率为η时的权重，等于学习率为1时的权重的η倍。两者都从0出发；若 w^(η) = η w^(1)，则
sign(w^(η)·x) = sign(w^(1)·x)，所以判错的是同样的例子，而更新 η y x 和 y x 保持这个比例。学习率只是缩放w，而w·x的符号看不到尺度。

**2. 用两个ReLU做异或。** 给一个2–2–1的ReLU网络找出权重，使它在 {0, 1}² 上精确地算出异或。

*解答。* h₁ = max(0, x₁ + x₂)，h₂ = max(0, x₁ + x₂ − 1)，y = h₁ − 2h₂。(0, 0)：0。(0, 1)和(1, 0)：h₁ = 1，h₂ = 0，得1。
(1, 1)：h₁ = 2，h₂ = 1，得0。隐藏层在x₁ + x₂ = 1处把直线折了一下，正是第7章的帐篷。

**3. sigmoid的梯度消失得有多快。** 证明sigmoid满足 σ′ ≤ ¼。如果每个权重矩阵的算子范数都不超过1，‖δ^l‖随深度最快缩小多少？

*解答。* σ′ = σ(1 − σ)，两个和为1的数之积至多是 (½)² = ¼。由 δ^l = (W^{l+1})ᵀδ^{l+1} ⊙ σ′(z^l)，得
‖δ^l‖ ≤ ‖W^{l+1}‖ · max|σ′| · ‖δ^{l+1}‖ ≤ ¼‖δ^{l+1}‖，所以 ‖δ^l‖ ≤ 4^{−(L−l)}‖δ^L‖：每层至少缩小4倍，20层后是10⁻¹²。
更大的权重可以抵消它，这正是初始化要处理的事。

**4. 何恺明的规则。** 对 z ~ N(0, q)，证明 E[max(0, z)²] = q/2，并推出 Var(W) = 2/n。

*解答。* 由对称性，∫₀^∞ z² φ(z) dz 是 ∫ z² φ(z) dz = q 的一半。对 z_i = Σ_j W_ij a_j，权重独立、均值为0，
a_j = max(0, z_j^{prev})，有 Var(z) = n Var(W) E[a²] = n Var(W) q_prev / 2，它等于 q_prev 当且仅当 Var(W) = 2/n。

**5. 深度数出小块。** 证明[0, 1]上的帐篷映射 t(x) = 1 − |2x − 1| 复合k次后有2^k个线性段，而ℝ上一个由m个ReLU组成的隐藏层至多有m + 1段。

*解答。* t把[0, ½]和[½, 1]各自线性地映到[0, 1]上。若t^k有2^k段，每段都单调地映满[0, 1]，那么在每一段上，t^{k+1} = t ∘ t^k
在t^k = ½的那一点断开，得到两段，各自映满[0, 1]：共2^{k+1}段。单层网络 c + Σ a_i max(0, w_i x + b_i) 除了m个折点−b_i/w_i之外
都是线性的，所以至多m + 1段；要等于t^k，需要 m ≥ 2^k − 1 个单元，而k层、每层2个单元就够了。

**6. RMSNorm的雅可比矩阵。** 对 y = √d h / ‖h‖，证明 ∂y/∂h = (√d/‖h‖)(I − ĥĥᵀ)，其中 ĥ = h/‖h‖。这对关于h的梯度意味着什么？

*解答。* ∂(h/‖h‖)/∂h = I/‖h‖ − h hᵀ/‖h‖³ = (I − ĥĥᵀ)/‖h‖。这个矩阵是对称的，并且把h送到0，所以梯度 Jᵀg = Jg 与h正交：
RMSNorm的输入永远得不到沿它自身方向的梯度，而h加倍时，梯度减半。

## Glossary (new terms in this part)

| English | 中文 |
|---|---|
| artificial neuron, unit | 人工神经元，单元 |
| McCulloch–Pitts unit, threshold | 麦卡洛克–皮茨单元，阈值 |
| Hebb's rule | 赫布规则 |
| perceptron, Mark I Perceptron | 感知机，Mark I感知机 |
| association unit, response unit | 联想单元，响应单元 |
| ADALINE, least mean squares (LMS) | ADALINE，最小均方 |
| margin, convergence theorem | 间隔，收敛定理 |
| linearly separable | 线性可分 |
| XOR, parity, connectedness | 异或，奇偶性，连通性 |
| hidden layer, hidden unit | 隐藏层，隐藏单元 |
| backpropagation, delta (δ) | 反向传播，delta（δ） |
| forward pass, backward pass | 前向传播，反向传播 |
| finite differences | 有限差分 |
| reverse-mode automatic differentiation | 自动微分的反向模式 |
| universal approximation theorem | 万能近似定理 |
| hinge, bump | 合页，鼓包 |
| rectified linear unit (ReLU) | 线性整流单元（ReLU） |
| curse of dimensionality | 维数灾难 |
| Barron's bound | 巴伦界 |
| linear region (piece) | 线性区域（小块） |
| depth separation | 深度分离 |
| folding | 折叠 |
| vanishing / exploding gradients | 梯度消失 / 梯度爆炸 |
| deep belief net, greedy layer-wise pretraining | 深度信念网络，逐层贪心预训练 |
| initialization (Glorot / Xavier, He) | 初始化（格洛罗初始化，何恺明初始化） |
| mean-field theory | 平均场理论 |
| length map, correlation map | 长度映射，相关映射 |
| ordered phase, chaotic phase, edge of chaos | 有序相，混沌相，混沌的边缘 |
| depth scale (ξ) | 深度尺度（ξ） |
| residual connection, residual stream | 残差连接，残差流 |
| highway network | 高速公路网络 |
| batch normalization, layer normalization, RMSNorm | 批归一化，层归一化，RMSNorm |
| pre-norm, post-norm, warm-up | 前置归一化，后置归一化，预热 |
| internal covariate shift | 内部协变量偏移 |
| Jacobian, singular value | 雅可比矩阵，奇异值 |
| GELU, SiLU (Swish) | GELU，SiLU（Swish） |
| gating, gated linear unit (GLU), SwiGLU | 门控，门控线性单元（GLU），SwiGLU |
| feed-forward network (MLP) | 前馈网络（MLP） |
| Kolmogorov–Arnold representation theorem | 柯尔莫哥洛夫–阿诺德表示定理 |
| Kolmogorov–Arnold network (KAN), spline | 柯尔莫哥洛夫–阿诺德网络（KAN），样条 |
| neural language model, embedding | 神经语言模型，嵌入 |
| Hilbert's thirteenth problem | 希尔伯特第13问题 |
