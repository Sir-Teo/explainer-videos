# AI, Built — Part 24: Learning Without Labels

Part 24 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Act IV, *Generation and Perception*. How a network learns what matters from
data nobody labelled: pretext puzzles, contrastive learning from word2vec's negatives to InfoNCE, SimCLR and MoCo, the
geometry of the hypersphere, collapse and the four ways out of it (negatives, asymmetry, decorrelation,
self-distillation), masked modelling, joint-embedding prediction, embeddings for search, and whether different
networks come to see the world alike. Every method is trained here, by `compute.py`, on MNIST, on the **same
three-layer convolutional network with the same budget**: 800 updates of 256 encoder passes (128 digits in two views,
or 256 in one), the same optimizer, schedule and views, three seeds (two for ablations), and each seed gives every
method the same starting network.

* **Hook: nobody told it what a digit is.** Six hundred test digits on a sphere, placed by a SimCLR network with three
  output numbers, coloured by labels it never saw; the nearest-neighbour accuracy of those three numbers; its training
  replayed; the collapsed alternative; the three families of answers; the plan.
* **1. Learning without labels.** Labels against unlabelled images (MNIST, ImageNet-1k, DINOv2's LVD-142M, DINOv3's
  LVD-1689M and its pool of about 17 billion); LeCun's cake (NIPS 2016); self-supervised learning defined; how we got
  here, from Barlow (1961) and Becker & Hinton (1992) to V-JEPA 2.1 (2026); how to judge a representation (frozen
  encoder: linear probe, weighted k-NN, a probe from ten labels per digit); the bench and its yardsticks (raw pixels,
  an untrained network, the network trained with every label).
* **2. Invent a puzzle.** Context prediction, jigsaw, colorization, inpainting, rotation (2015–2018); rotation
  prediction trained and replayed (the four turns of four digits with their predicted probabilities); its accuracy
  by digit (the half-turn-symmetric digits are its blind spots); its representation against the yardsticks; the
  chromatic-aberration shortcut (Doersch, Gupta & Efros 2015); Exemplar CNN (2014) and instance discrimination (2018).
* **3. Telling the real from the fake.** Noise-contrastive estimation (Gutmann & Hyvärinen 2010); word2vec's negative
  sampling (Mikolov et al. 2013); InfoNCE (van den Oord, Li & Vinyals 2018) as an N-way classification; the bound
  I(X; Y) ≥ log N − L_N derived (Gibbs; the partner's slot is uniform; the chain rule); checked on correlated Gaussians
  with known mutual information (2, 5, 10 nats; N = 2 … 512; two seeds): the estimate never exceeds log N; CPC.
* **4. Two views of one digit.** The views (crop and zoom, tilt and shear, contrast, blur, erasing, noise); SimCLR
  (Chen et al. 2020) and its NT-Xent loss; our SimCLR replayed through the nearest neighbours of six test digits; the
  projection head (probe before and after it); MoCo's queue and momentum encoder (He et al. 2020) against SimCLR;
  SimCLR with crops alone.
* **5. Alignment and uniformity.** The three-number SimCLR on the sphere, replayed with its alignment and uniformity;
  where the digits' mean directions land; the decomposition of the contrastive loss as N → ∞ (Wang & Isola 2020);
  SimCLR at five temperatures (0.05 … 1); how the softmax spreads its push over the negatives at low and high
  temperature (Wang & Liu 2021).
* **6. Collapse.** Pause and predict; a network trained only to make the two views agree, its embedding on the
  sphere collapsing to a point; the effective rank (Roy & Vetterli 2007; RankMe, Garrido et al. 2023); singular-value
  spectra (complete and dimensional collapse: Hua et al. 2021, Jing et al. 2022); the starved encoder; the four ways
  out.
* **7. No negatives: BYOL and SimSiam.** BYOL (Grill et al. 2020); SimSiam (Chen & He 2021) with and without its
  stop-gradient (three and two seeds): the spread of the embedding, and the three-number SimSiam on the sphere;
  SimSiam as alternating optimization; Tian, Chen & Ganguli (2021); BYOL without batch statistics (Richemond et al.
  2020); SimCLR, BYOL and SimSiam on the linear and ten-label probes.
* **8. Decorrelate: Barlow Twins and VICReg.** Barlow's redundancy reduction (1961); Barlow Twins (Zbontar et al.
  2021), its cross-correlation matrix replayed to the identity; VICReg (Bardes, Ponce & LeCun 2022) and VICReg without
  its variance term (collapse); the duality of the two families (Garrido et al. 2023); LeJEPA's SIGReg (Balestriero &
  LeCun 2025).
* **9. Self-distillation: DINO.** DeepCluster and SwAV; DINO (Caron et al. 2021): student, momentum teacher,
  prototypes; the two collapses and the two cures (centring, sharpening); the teacher's entropy and the KL to the
  student, for DINO and for DINO without each cure; the teacher's average answer over the prototypes, replayed;
  DINO's results.
* **10. Scale and curation.** DINOv2's retrieval-based curation (LVD-142M from 1.2 billion images; Oquab et al.
  2023); our version: an unbalanced pool of 14,000 digits curated by retrieval from 1,000 balanced seeds, and SimCLR
  trained on each (two seeds), digit by digit; DINOv3 (Siméoni et al. 2025: 7B, LVD-1689M, Gram anchoring, 88.4%
  linear); Web-SSL (Fan et al. 2025: images alone match CLIP at 7B on 16 VQA tasks).
* **11. Fill in the blanks: MAE and BEiT.** Denoising autoencoders (2008), BERT (2018), BEiT and MAE (2021); our
  masked autoencoder (75% of 49 patches hidden; the same network, hidden patches blanked) with its reconstructions
  replayed; the masking ratio (50%, 75%, 90%); a BEiT-style model predicting k-means codes of hidden patches; masked
  models against SimCLR.
* **12. Predict the meaning, not the pixels.** Joint-embedding, generative and joint-embedding predictive
  architectures (LeCun 2022); the energy view (contrastive against regularized methods); I-JEPA (Assran et al. 2023)
  and ours (two hidden blocks of the 4 × 4 map); I-JEPA, MAE and SimCLR on one budget; V-JEPA (2024), V-JEPA 2 and
  V-JEPA 2-AC (2025), V-JEPA 2.1 (2026), LeJEPA.
* **13. Every method, one budget.** The linear probe for every method (three seeds); the ten-label probe; the whole
  network fine-tuned from 100 labels against training from scratch; alignment and uniformity across methods; the
  effective rank as a label-free predictor (RankMe).
* **14. Embeddings for search.** Retrieval with our embedding; text embeddings from word2vec to Sentence-BERT, DPR,
  SimCSE, E5/GTE/BGE and MTEB, Qwen3-Embedding (2025) and Gemini Embedding 2 (2026); CLIP and SigLIP (Part 23);
  Matryoshka representation learning (Kusupati et al. 2022) trained (three seeds) against SimCLR cut short; OpenAI's
  shortened embeddings.
* **15. Do all models see the same world?** CKA derived (Kornblith et al. 2019) and its invariances; the CKA between
  every pair of our methods and between seeds; the platonic representation hypothesis (Huh, Cheung, Wang & Isola,
  ICML 2024); our two checks: agreement against quality across methods, and two encoders that see only the top or the
  bottom half of each digit, trained apart (Becker & Hinton's setting), their agreement over training; the caveats.
* **Recap**, where it comes back, problems, Part 25's teaser, references.

## Running it

From the repo root:

```
python tools/make.py ai24                       # everything: the computations, then English and Chinese
python -m videos.ai.ai24.compute                # only the numbers (MNIST through Part 10's checked download)
python tools/build.py ai24                      # English
python tools/build.py ai24 --lang zh            # Chinese
AI24_SCALE=0.02 python -m videos.ai.ai24.compute   # a smoke test of every code path (into .cache/ai24_quick/)
```

Everything is seeded (`numpy` PCG64 and `torch.manual_seed`, one `torch.Generator` per run for the data order, the
views and the masks) and runs on one torch thread (`AI24_THREADS` to change it); there is no multiprocessing. Every
item made of several runs saves each run as it finishes (`CACHE.partial`), so an interrupted computation resumes;
each run takes two to four minutes. Each run's larger arrays (its test features, its replay snapshots) are in
`.cache/ai24/runs/`, the seed-0 networks of the compared methods in `.cache/ai24/models/` (about 20 MB). MNIST is read
through Part 10's downloader (`videos.ai.ai10.data`, checked against SHA-256); no other part's results are used.
RESULTS_TIME

## Results on this machine

RESULTS

## References

Books: K. P. Murphy, *Probabilistic Machine Learning: Advanced Topics* (2023), ch. 32; S. J. D. Prince, *Understanding
Deep Learning* (2023), ch. 14; R. Balestriero et al., *A Cookbook of Self-Supervised Learning* (2023).

Papers: H. B. Barlow, *Possible principles underlying the transformations of sensory messages* (1961); S. Becker &
G. E. Hinton, *Self-organizing neural network that discovers surfaces in random-dot stereograms* (Nature, 1992);
J. Bromley et al., *Signature verification using a "Siamese" time delay neural network* (1993); R. Hadsell, S. Chopra
& Y. LeCun, *Dimensionality reduction by learning an invariant mapping* (2006); Y. LeCun, S. Chopra, R. Hadsell,
M. Ranzato & F. J. Huang, *A tutorial on energy-based learning* (2006); P. Vincent, H. Larochelle, Y. Bengio &
P.-A. Manzagol, *Extracting and composing robust features with denoising autoencoders* (2008); M. Gutmann &
A. Hyvärinen, *Noise-contrastive estimation* (2010); T. Mikolov, I. Sutskever, K. Chen, G. Corrado & J. Dean,
*Distributed representations of words and phrases and their compositionality* (2013); A. Dosovitskiy et al.,
*Discriminative unsupervised feature learning with convolutional neural networks* (2014); C. Doersch, A. Gupta &
A. A. Efros, *Unsupervised visual representation learning by context prediction* (2015); M. Noroozi & P. Favaro,
*Jigsaw puzzles* (2016); R. Zhang, P. Isola & A. A. Efros, *Colorful image colorization* (2016); D. Pathak et al.,
*Context encoders* (2016); S. Gidaris, P. Singh & N. Komodakis, *Predicting image rotations* (2018); Z. Wu, Y. Xiong,
S. Yu & D. Lin, *Non-parametric instance discrimination* (2018); A. van den Oord, Y. Li & O. Vinyals, *Contrastive
predictive coding* (2018); G. Alain & Y. Bengio, *Linear classifier probes* (2016); M. Caron, P. Bojanowski,
A. Joulin & M. Douze, *DeepCluster* (2018); K. He, H. Fan, Y. Wu, S. Xie & R. Girshick, *MoCo* (2020); T. Chen,
S. Kornblith, M. Norouzi & G. Hinton, *SimCLR* (2020); T. Wang & P. Isola, *Alignment and uniformity on the
hypersphere* (2020); F. Wang & H. Liu, *Understanding the behaviour of contrastive loss* (2021); M. Caron et al.,
*SwAV* (2020); J.-B. Grill et al., *BYOL* (2020); P. H. Richemond et al., *BYOL works even without batch statistics*
(2020); X. Chen & K. He, *SimSiam* (2021); Y. Tian, X. Chen & S. Ganguli, *Understanding self-supervised learning
dynamics without contrastive pairs* (2021); J. Zbontar, L. Jing, I. Misra, Y. LeCun & S. Deny, *Barlow Twins* (2021);
A. Bardes, J. Ponce & Y. LeCun, *VICReg* (2022); T. Hua et al., *On feature decorrelation in self-supervised learning*
(2021); L. Jing, P. Vincent, Y. LeCun & Y. Tian, *Understanding dimensional collapse in contrastive self-supervised
learning* (2022); O. Roy & M. Vetterli, *The effective rank* (2007); Q. Garrido, R. Balestriero, L. Najman & Y. LeCun,
*RankMe* (2023); Q. Garrido et al., *On the duality between contrastive and non-contrastive self-supervised learning*
(2023); R. Balestriero & Y. LeCun, *LeJEPA* (2025); M. Caron et al., *DINO* (2021); M. Oquab et al., *DINOv2* (2023);
O. Siméoni et al., *DINOv3* (2025); D. Fan, S. Tong, J. Zhu et al., *Scaling language-free visual representation
learning* (2025); J. Devlin et al., *BERT* (2019); H. Bao, L. Dong, S. Piao & F. Wei, *BEiT* (2022); K. He, X. Chen,
S. Xie, Y. Li, P. Dollár & R. Girshick, *Masked autoencoders are scalable vision learners* (2022); Y. LeCun, *A path
towards autonomous machine intelligence* (2022); M. Assran et al., *I-JEPA* (2023); A. Bardes et al., *V-JEPA* (2024);
M. Assran et al., *V-JEPA 2* (2025); L. Mur-Labadia et al., *V-JEPA 2.1* (2026); N. Reimers & I. Gurevych,
*Sentence-BERT* (2019); V. Karpukhin et al., *Dense passage retrieval* (2020); T. Gao, X. Yao & D. Chen, *SimCSE*
(2021); N. Muennighoff, N. Tazi, L. Magne & N. Reimers, *MTEB* (2023); A. Kusupati et al., *Matryoshka representation
learning* (2022); Y. Zhang et al., *Qwen3 Embedding* (2025); M. Shanbhogue et al., *Gemini Embedding 2* (2026);
OpenAI, embeddings guide (`dimensions`, text-embedding-3, 2024); A. Radford et al., *CLIP* (2021); X. Zhai et al.,
*SigLIP* (2023); S. Kornblith, M. Norouzi, H. Lee & G. Hinton, *Similarity of neural network representations
revisited* (2019); M. Huh, B. Cheung, T. Wang & P. Isola, *The platonic representation hypothesis* (ICML 2024).
Data: Y. LeCun, C. Cortes & C. J. C. Burges, MNIST (1998).

## Problems, with solutions

**1. InfoNCE's optimal critic, and its ceiling.** With N candidates, one of them x's partner, show that the critic
minimizing the InfoNCE loss is f*(x, y) = log p(y | x)/p(y) + c(x), and that log N − L_N ≤ log N for every critic.

*Solution.* The loss is the cross-entropy of q_f(k | x, y₁…y_N) = e^{f(x, y_k)} / Σⱼ e^{f(x, y_j)} as a guess of the
partner's slot K. Given K = k, the candidates' density is p(y_k | x) Πⱼ≠ₖ p(y_j) = Πⱼ p(y_j) · p(y_k | x)/p(y_k), so by
Bayes the true posterior is p(K = k | x, y₁…y_N) = r(y_k) / Σⱼ r(y_j) with r(y) = p(y | x)/p(y). A cross-entropy is
smallest when the guess equals the truth, so e^{f*} ∝ r: f* = log r + c(x), and c(x) cancels in the softmax. For any
critic, each term −log q_f is ≥ 0 because q_f ≤ 1, so L_N ≥ 0 and the estimate log N − L_N never exceeds log N.

**2. Alignment and uniformity.** For unit vectors show z·z⁺ = 1 − ½‖z − z⁺‖², and derive the N → ∞ limit of the
contrastive loss.

*Solution.* ‖z − z⁺‖² = ‖z‖² + ‖z⁺‖² − 2 z·z⁺ = 2 − 2 z·z⁺. One view's loss is ℓ = −z·z⁺/τ + log(e^{z·z⁺/τ} +
Σⱼ e^{z·z_j/τ}) with N − 1 negatives. Subtract log N: the logarithm becomes log of an average of N terms, which tends to
log E_{z⁻} e^{z·z⁻/τ} by the law of large numbers (the partner's single term weighs 1/N). Substituting the identity,
ℓ − log N → ‖z − z⁺‖²/(2τ) − 1/τ + log E_{z⁻} e^{z·z⁻/τ}: an alignment term plus a term that is smallest when the
vectors spread uniformly over the sphere (Wang & Isola 2020; their L_uniform uses the Gaussian potential
e^{−t‖u − v‖²} = e^{−2t} e^{2t u·v} on the sphere).

**3. What collapse costs each loss.** Show that a constant encoder minimizes the SimSiam loss, but gives the NT-Xent
loss log(2N − 1).

*Solution.* SimSiam's loss is −cos(p, sg(z)) ≥ −1. If every z is the same vector z₀ and the predictor maps it to a
multiple of z₀, every cosine is 1 and the loss is −1, its global minimum. In NT-Xent, if every z is the same unit
vector, all 2N − 1 cosines of a view are 1, so its softmax is uniform and ℓ = −log(1/(2N − 1)) = log(2N − 1): the loss
of guessing at random. Any configuration that keeps each pair together and spreads the pairs apart scores lower, so
the contrastive loss pushes away from collapse.

**4. Barlow Twins.** With outputs standardized over the batch (mean 0, variance 1), show that C_ii = 1 exactly when
the two views' i-th outputs are equal for every image, and explain why a constant output is excluded.

*Solution.* C_ii = (1/n) Σ_b a_b b_b with (1/n)Σ a_b² = (1/n)Σ b_b² = 1; by Cauchy–Schwarz C_ii ≤ 1, with equality
exactly when the vectors (a_b) and (b_b) are equal. A constant output has zero variance; standardizing it gives 0 (the
small ε in the denominator), so C = 0 and the diagonal term Σᵢ(1 − 0)² takes its largest value: collapse is the worst
point of this loss, not a minimum.

**5. CKA's invariances.** Show that linear CKA is unchanged by X ↦ cXQ (Q orthogonal, c > 0), and that when n ≤ d any
two representations of rank n are related by an invertible linear map.

*Solution.* Centring commutes with right multiplication. ‖Ỹᵀ(cX̃Q)‖²_F = c²‖ỸᵀX̃Q‖²_F = c²‖ỸᵀX̃‖²_F, since right
multiplication by an orthogonal matrix keeps the Frobenius norm; and ‖(cX̃Q)ᵀ(cX̃Q)‖_F = c²‖QᵀX̃ᵀX̃Q‖_F =
c²‖X̃ᵀX̃‖_F. The c² cancel. If X and Y are n × d of rank n ≤ d, then XX⁺ = I_n, and A = X⁺Y + (I − X⁺X)B satisfies
XA = Y for every B; B can be chosen to make A invertible. So a statistic invariant to every invertible linear map (as
CCA is) finds any two such representations identical: this is why Kornblith et al. preferred CKA.

**6. DINO's two collapses.** Show H(P_t, P_s) = H(P_t) + KL(P_t ‖ P_s), and that a teacher whose output does not
depend on the input lets the student reach KL = 0 without learning anything.

*Solution.* −Σ P_t log P_s = −Σ P_t log P_t + Σ P_t log(P_t/P_s). If P_t(x) = π for every x, a student that outputs π
for every input has KL = 0, so the loss is H(π), the least possible for that teacher, and its output depends on nothing:
collapse. With π one-hot, H(π) = 0 (no centring); with π uniform, H(π) = log K (no sharpening). DINO's centring removes
the input-independent part of the teacher's logits and its low temperature keeps each answer confident, so neither
fixed point is stable.

## 习题与解答

**1. InfoNCE的最优打分函数与它的上限。** 有N个候选，其中一个是x的伙伴。证明使InfoNCE损失最小的打分函数是
f*(x, y) = log p(y | x)/p(y) + c(x)，并且对任何打分函数都有 log N − L_N ≤ log N。

*解答。* 这个损失是 q_f(k | x, y₁…y_N) = e^{f(x, y_k)} / Σⱼ e^{f(x, y_j)} 去猜伙伴所在位置K时的交叉熵。给定 K = k，候选的密度是
p(y_k | x) Πⱼ≠ₖ p(y_j) = Πⱼ p(y_j) · p(y_k | x)/p(y_k)，由贝叶斯公式，真实后验是 p(K = k | x, y₁…y_N) = r(y_k) / Σⱼ r(y_j)，
其中 r(y) = p(y | x)/p(y)。交叉熵在猜测等于真相时最小，所以 e^{f*} ∝ r：f* = log r + c(x)，c(x)在softmax里抵消。对任何打分函数，
每一项 −log q_f 都 ≥ 0，因为 q_f ≤ 1，所以 L_N ≥ 0，估计值 log N − L_N 永远不超过 log N。

**2. 对齐与均匀。** 对单位向量证明 z·z⁺ = 1 − ½‖z − z⁺‖²，并推导对比损失在 N → ∞ 时的极限。

*解答。* ‖z − z⁺‖² = ‖z‖² + ‖z⁺‖² − 2 z·z⁺ = 2 − 2 z·z⁺。一个视图的损失是 ℓ = −z·z⁺/τ + log(e^{z·z⁺/τ} + Σⱼ e^{z·z_j/τ})，
其中有N − 1个负样本。减去log N：对数里变成N项的平均，由大数定律趋于 log E_{z⁻} e^{z·z⁻/τ}（伙伴那一项只占1/N）。代入上面的恒等式，
ℓ − log N → ‖z − z⁺‖²/(2τ) − 1/τ + log E_{z⁻} e^{z·z⁻/τ}：一个对齐项，加上一个当向量在球面上均匀分布时最小的项（Wang & Isola
2020；他们的L_uniform用的是高斯势 e^{−t‖u − v‖²}，在球面上等于 e^{−2t} e^{2t u·v}）。

**3. 坍缩对各个损失意味着什么。** 证明常数编码器使SimSiam的损失最小，却使NT-Xent损失等于 log(2N − 1)。

*解答。* SimSiam的损失是 −cos(p, sg(z)) ≥ −1。如果每个z都是同一个向量z₀，而预测器把它映到z₀的某个倍数，每个余弦都是1，损失是−1，
即全局最小值。在NT-Xent里，如果每个z都是同一个单位向量，一个视图的2N − 1个余弦全是1，它的softmax是均匀的，ℓ = −log(1/(2N − 1))
= log(2N − 1)：等于随便乱猜的损失。任何让每对视图保持一致、又让不同的对彼此分开的配置，损失都更低，所以对比损失会把网络推离坍缩。

**4. Barlow Twins。** 当输出在批内标准化（均值0，方差1）时，证明 C_ii = 1 当且仅当两个视图的第i个输出对每张图像都相等，
并解释为什么常数输出被排除了。

*解答。* C_ii = (1/n) Σ_b a_b b_b，其中 (1/n)Σ a_b² = (1/n)Σ b_b² = 1；由柯西-施瓦茨不等式 C_ii ≤ 1，当且仅当向量(a_b)和(b_b)
相等时取等号。常数输出的方差为零，标准化后得到0（分母里的小ε），所以 C = 0，对角项 Σᵢ(1 − 0)² 取到最大值：坍缩是这个损失最差的
地方，而不是最小值。

**5. CKA的不变性。** 证明线性CKA在 X ↦ cXQ（Q正交，c > 0）下不变，并证明当 n ≤ d 时，任何两个秩为n的表示都可以用一个可逆线性映射
互相转换。

*解答。* 中心化和右乘可以交换。‖Ỹᵀ(cX̃Q)‖²_F = c²‖ỸᵀX̃Q‖²_F = c²‖ỸᵀX̃‖²_F，因为右乘正交矩阵不改变弗罗贝尼乌斯范数；而
‖(cX̃Q)ᵀ(cX̃Q)‖_F = c²‖QᵀX̃ᵀX̃Q‖_F = c²‖X̃ᵀX̃‖_F。c²互相抵消。如果X和Y都是 n × d、秩为 n ≤ d，那么 XX⁺ = I_n，
A = X⁺Y + (I − X⁺X)B 对任意B都满足 XA = Y；适当选B可以使A可逆。所以一个对所有可逆线性映射都不变的统计量（CCA就是这样）会认为任何
两个这样的表示完全相同：这就是Kornblith等人偏好CKA的原因。

**6. DINO的两种坍缩。** 证明 H(P_t, P_s) = H(P_t) + KL(P_t ‖ P_s)，并证明如果老师的输出与输入无关，学生不必学到任何东西就能让
KL = 0。

*解答。* −Σ P_t log P_s = −Σ P_t log P_t + Σ P_t log(P_t/P_s)。如果对每个x都有 P_t(x) = π，那么一个对所有输入都输出π的学生KL = 0，
损失等于H(π)，这是对这个老师而言最小的可能值，而它的输出与输入毫无关系：这就是坍缩。π是独热分布时 H(π) = 0（没有中心化）；
π是均匀分布时 H(π) = log K（没有锐化）。DINO的中心化去掉老师打分里与输入无关的部分，低温度让每个回答保持自信，所以这两个不动点
都不稳定。


## Glossary (new terms in this part)

| English | 中文 |
|---|---|
| self-supervised learning | 自监督学习 |
| representation, encoder | 表示，编码器 |
| label, unlabelled data | 标签，无标签数据 |
| pretext task | 前置任务（代理任务） |
| context prediction, jigsaw puzzle, colorization, inpainting | 上下文预测，拼图，上色，图像修补 |
| rotation prediction | 旋转预测 |
| shortcut, chromatic aberration | 捷径，色差 |
| instance discrimination, memory bank | 实例判别，记忆库 |
| contrastive learning, contrastive loss | 对比学习，对比损失 |
| positive pair, negative (sample) | 正样本对，负样本 |
| noise-contrastive estimation (NCE) | 噪声对比估计（NCE） |
| negative sampling | 负采样 |
| InfoNCE, critic (scoring function) | InfoNCE，打分函数 |
| contrastive predictive coding (CPC) | 对比预测编码（CPC） |
| view, augmentation | 视图，数据增强 |
| projection head | 投影头 |
| NT-Xent (normalized temperature-scaled cross-entropy) | NT-Xent（归一化温度交叉熵） |
| momentum encoder, queue | 动量编码器，队列 |
| hypersphere, unit vector | 超球面，单位向量 |
| alignment, uniformity | 对齐，均匀性 |
| temperature τ | 温度τ |
| hard negative | 难负样本 |
| uniformity–tolerance dilemma | 均匀性-容忍度困境 |
| collapse: complete, dimensional | 坍缩：完全坍缩，维度坍缩 |
| effective rank, RankMe | 有效秩，RankMe |
| singular-value spectrum | 奇异值谱 |
| siamese network | 孪生网络 |
| stop-gradient | 停止梯度 |
| predictor | 预测器 |
| online network, target network | 在线网络，目标网络 |
| exponential moving average (EMA) | 指数移动平均（EMA） |
| redundancy reduction | 冗余削减 |
| cross-correlation matrix | 互相关矩阵 |
| invariance, variance, covariance terms | 不变项，方差项，协方差项 |
| decorrelation | 去相关 |
| self-distillation, student, teacher | 自蒸馏，学生，老师 |
| prototype | 原型 |
| centring, sharpening | 中心化，锐化 |
| data curation, retrieval-based curation | 数据筛选，基于检索的筛选 |
| deduplication | 去重 |
| Gram anchoring | 格拉姆锚定 |
| masked image modelling, masked autoencoder (MAE) | 掩码图像建模，掩码自编码器（MAE） |
| masking ratio | 掩码比例 |
| visual token, codebook | 视觉词元，码本 |
| fine-tuning (the whole network) | （整个网络）微调 |
| joint-embedding predictive architecture (JEPA) | 联合嵌入预测架构（JEPA） |
| context block, target block | 上下文块，目标块 |
| energy-based view; contrastive vs regularized methods | 能量视角；对比式与正则化式方法 |
| world model | 世界模型 |
| linear probe, k-NN probe, few-label probe | 线性探针，k近邻探针，少标签探针 |
| embedding, retrieval, nearest-neighbour search | 嵌入，检索，最近邻搜索 |
| text embedding, sentence embedding | 文本嵌入，句子嵌入 |
| Matryoshka representation learning | 套娃表示学习 |
| centred kernel alignment (CKA), HSIC | 中心化核对齐（CKA），HSIC |
| mutual nearest neighbours | 互为近邻 |
| platonic representation hypothesis | 柏拉图表示假说 |

