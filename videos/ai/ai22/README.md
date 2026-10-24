# AI, Built — Part 22: Images, Video and 3D

Part 22 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Act IV, *Generation and Perception*. How the transformer of Part 13 and the
diffusion and flow of Part 21 meet pictures, video and 3D scenes: from AlexNet to the vision transformer, from GANs to
latent diffusion transformers, from DALL·E to Stable Diffusion 3 and FLUX.2, from Sora to real-time autoregressive
video, and from NeRF to Gaussian splatting, with the 2025–26 frontier (representation autoencoders, unified models that
read, draw and edit, open audio–video models). Part 21's samplers and theory are used, not repeated; Part 20's VAE,
VQ-VAE and GANs and Part 24's self-supervised encoders are linked rather than retold.

Every model is trained here, on one CPU core, by `compute.py`: the pictures are Part 21's 20 × 20 capital letters from
24 system fonts (the last 4 held out); the videos are a 12 × 12 letter bouncing in a 20 × 20 box; the 3D scene is an
extruded gold letter A and a blue ball on a 64³ grid, photographed from 24 cameras. A judge (a small convolutional
classifier, 96% right on held-out fonts) reads generated letters; "FD" is the Fréchet distance between Gaussians fitted
to its 128 features for generated and real letters (FID's formula on our own features). Comparisons use equal budgets
(steps, batches, data order and, where stated, weights) and three seeds, with the spread shown.

## Chapters

* **Letters from noise.** A word drawn letter by letter by our diffusion transformer; how we got here, 2012–2026
  (AlexNet, GANs, ViT, DALL·E, diffusion beating GANs, Stable Diffusion, SD3 and Sora, Veo 3 and BAGEL, LTX-2); the plan.
* **1. An image is a sequence.** Patches as tokens, the summary token, learned positions (Dosovitskiy et al. 2020); a
  small ViT (155 thousand weights) trained on 20 fonts and replayed: held-out accuracy, what it calls eight unseen
  letters, and the centre patch's position vector at each checkpoint; where the summary token looks (share of its
  attention on inked patches); how far each head looks, against the distance between random patches; the 25 position
  vectors' similarities, neighbours against far patches.
* **2. Convolutions or attention?** AlexNet to ViT (Krizhevsky et al. 2012; non-local networks 2018; ViT's 88.55% after
  JFT-300M and its deficit on ImageNet alone; DeiT 83.1% without external data; Swin; ConvNeXt 87.8%; ViT-22B, DINOv2);
  inductive bias defined (locality, translation equivariance); pause and predict; ViT against a CNN of the same size
  (equal steps, batches, augmentations) on 3, 7 and 20 training fonts, three seeds, with their learning curves and
  their multiply-adds per picture.
* **3. A smaller space.** Latent diffusion (Rombach et al. 2022), perceptual and semantic compression, KL-f8; eight
  convolutional autoencoders from 16 to 100 latent numbers on 1 × 1 to 10 × 10 grids: held-out rebuild error, equal
  numbers on coarse and fine grids, then flow matching in each space (two seeds): the reconstruction–generation
  dilemma; SD3's 16 channels; deep-compression autoencoders (Chen et al. 2024): space-to-channel shortcuts, f32–f128.
* **4. Borrowed eyes.** REPA (Yu et al. 2024): the denoiser's early tokens aligned with a frozen encoder by cosine
  similarity; our DiT with and without REPA (chapter 1's ViT as the teacher), three seeds: right letters, FD and the
  alignment over training; VA-VAE (Yao et al. 2025), REPA-E (Leng et al. 2025), representation autoencoders (Zheng et al.
  2025).
* **5. U-Net or transformer.** The U-Net (Ronneberger et al. 2015), ADM (Dhariwal & Nichol 2021); DiT (Peebles & Xie
  2023), quality tracking Gflops; our U-Net against our DiT at about equal weights and equal steps, three seeds, with
  the multiply-adds each spends.
* **6. adaLN-Zero.** In-context tokens, adaLN and adaLN-Zero; the block written out, gates starting at zero; our gates
  opening during training; the training replay (same noise, ten requests, at checkpoints, read by the judge); the three
  conditionings at equal budgets, three seeds; the alphabet.
* **7. Words into pictures.** GANs to diffusion; DALL·E (12 billion weights, 256 text then 32 × 32 image tokens),
  diffusion beats GANs (FID 4.59 against 6.95), DALL·E 2, Imagen (a bigger text encoder helps more), Parti, Stable
  Diffusion, DALL·E 3 (recaptioning); cross-attention; classifier-free guidance swept on our DiT (right letters,
  variety).
* **8. Stable Diffusion 3 and Flux.** MM-DiT (Esser et al. 2024): two streams, one joint attention; QK-norm; logit-normal
  t against uniform, three seeds; the resolution shift derived (σ' = ασ / (1 + (α − 1)σ), α = √(m/n)) and checked on
  letters drawn at 20, 40 and 80 pixels with the exact posterior; α = 3 at 1024²; FLUX.1, FLUX.1 Kontext, FLUX.2.
* **9. Pictures as tokens.** VQ-VAE and VQGAN (Esser et al. 2020); our tokenizer (25 tokens from 128 codes); raster
  order; MaskGIT (Chang et al. 2022) and its cosine schedule, our model drawing in 8 passes; the token models' training;
  raster against MaskGIT, three seeds.
* **10. Coarse to fine.** VAR (Tian et al. 2024): residual tokens on five scales, the error after each; the block-causal
  mask; our VAR drawing in five passes; raster, MaskGIT and VAR side by side; VAR's FID 1.73, MAR (continuous tokens),
  Infinity (bitwise tokens, a vocabulary of up to 2⁶⁴).
* **11. One model for words and pictures.** Chameleon, Transfusion, Janus, BAGEL; our tiny Transfusion (one transformer,
  next-token loss on text and flow matching on picture patches; causal attention except within a picture) that names,
  draws and edits ("bold"), its four loss terms, and its edits on two font pairs it never saw; InstructPix2Pix, GPT-4o
  images, FLUX.1 Kontext, Qwen-Image, Gemini 2.5 Flash Image.
* **12. Squeezing time.** Sora, Movie Gen, HunyuanVideo, Wan 2.1/2.2, Veo 3, Sora 2, HunyuanVideo 1.5, LTX-2; video
  tokens and their count; a causal video autoencoder trained here (the first frame alone, then four frames per latent
  frame; a still picture as a one-frame video); joint image–video training; 3D rotary positions; attention's cost.
* **13. Frames that agree.** Video in a frame autoencoder's latents, one token per frame; three video models (whole
  clip, teacher forcing, diffusion forcing) trained and replayed, three seeds; pause and predict; from one given frame,
  frames drawn together against frames from separate samples: the letter kept, and the wobble of its path.
* **14. Rolling forward.** Teacher forcing and diffusion forcing (Chen et al. 2024); rollouts from two given frames to
  32 frames (4× the training length): distance from the physics and the letter kept, frame by frame, three seeds,
  including diffusion forcing with slightly noised context; exposure bias; CausVid, Self Forcing (17 frames a second on
  one H100), Genie 3 (Part 29).
* **15. Light through a volume.** NeRF (Mildenhall et al. 2020); the volume-rendering integral derived, then its
  quadrature (alpha compositing); the Riemann sum against NeRF's sum on a uniform ball with a known answer; positional
  encoding; our NeRF trained on 24 photographs and replayed on a held-out view, PSNR, depth; three seeds.
* **16. Gaussian splatting.** 3D Gaussian splatting (Kerbl et al. 2023): Σ = RSSᵀRᵀ; the projected covariance
  J W Σ Wᵀ Jᵀ derived (EWA, Zwicker et al. 2001) and checked against 200,000 exactly projected samples, error against
  the Gaussian's size; 500 Gaussians fitted to the same photographs, replayed, against NeRF (PSNR, render time; three
  seeds); Instant-NGP, DUSt3R, VGGT.
* **Outro.** Eight pictures from the part's results, where the ideas come back (Parts 23, 24, 25, 29, 31), six
  problems, Part 23's teaser, references.

## Running it

From the repo root:

```
python tools/make.py ai22                       # everything: the computations, then English and Chinese
python -m videos.ai.ai22.compute                # the numbers only (about 2.5 CPU-hours on one core; resumable)
AI22_THREADS=2 python -m videos.ai.ai22.compute     # torch threads (default 1; on a busy machine 1 is fastest)
AI22_QUICK=1 python -m videos.ai.ai22.compute       # a smoke test of every code path with tiny budgets (.cache/ai22_quick)
python tools/build.py ai22                      # English
python tools/build.py ai22 --lang zh            # Chinese
```

Every random choice is seeded (numpy PCG64 and `torch.manual_seed`, one generator per run); there is no
multiprocessing. Items made of several trainings save each one as it finishes (`CACHE.partial`), so an interrupted
run resumes; items that need another item's model (the judge, the vision transformer, the showcase DiT, the tokenizers,
the frame autoencoder) load it from `.cache/ai22/*.pt` or compute it first. The longest items are `denoisers` (fifteen
trainings, the U-Nets the slowest), `tokens`, `unified` and `clips`. The letters are drawn with Part 21's
`glyph_images` and its flow-matching `mlp` is borrowed; no other part's results are read.

## References

Books: S. J. D. Prince, *Understanding Deep Learning* (2023), ch. 12 and 18; R. Szeliski, *Computer Vision: Algorithms
and Applications*, 2nd ed. (2022); K. P. Murphy, *Probabilistic Machine Learning: Advanced Topics* (2023).

Papers and reports: Krizhevsky, Sutskever & Hinton, AlexNet (2012); Wang et al., Non-local Neural Networks (2018);
Dosovitskiy et al., An Image Is Worth 16x16 Words (2020); Touvron et al., DeiT (2020); Liu et al., Swin (2021); Liu et al.,
ConvNeXt (2022); Dehghani et al., ViT-22B (2023); Oquab et al., DINOv2 (2023); Rombach et al., Latent Diffusion (2022);
Chen et al., Deep Compression Autoencoder (2024); Xie et al., SANA (2024); Yu et al., REPA (2024); Yao, Yang & Wang,
VA-VAE (2025); Leng et al., REPA-E (2025); Zheng, Ma, Tong & Xie, Diffusion Transformers with Representation
Autoencoders (2025); Ronneberger, Fischer & Brox, U-Net (2015); Ho, Jain & Abbeel, DDPM (2020); Dhariwal & Nichol,
Diffusion Models Beat GANs (2021); Peebles & Xie, DiT (2023); Ramesh et al., DALL·E (2021) and DALL·E 2 (2022); Nichol et
al., GLIDE (2021); Saharia et al., Imagen (2022); Yu et al., Parti (2022); Betker et al., DALL·E 3 (2023); Ho & Salimans,
Classifier-Free Guidance (2022); Esser et al., SD3 (2024); Black Forest Labs, FLUX.1 (2024), FLUX.1 Kontext (2025),
FLUX.2 (2025); van den Oord et al., VQ-VAE (2017); Esser, Rombach & Ommer, VQGAN (2020); Chang et al., MaskGIT (2022);
Tian et al., VAR (2024); Li et al., MAR (2024); Han et al., Infinity (2024); Chameleon Team (2024); Zhou et al.,
Transfusion (2024); Wu et al., Janus (2024); Deng et al., BAGEL (2025); Brooks, Holynski & Efros, InstructPix2Pix (2022);
OpenAI, GPT-4o image generation system card addendum (2025); Qwen Team, Qwen-Image (2025); Google, Gemini 2.5 Flash Image
(2025); OpenAI, Video generation models as world simulators (Sora, 2024); Meta, Movie Gen (2024); Kong et al.,
HunyuanVideo (2024) and HunyuanVideo 1.5 (2025); Wan Team, Wan (2025) and Wan 2.2 (2025); Lightricks, LTX-2 (2026); Yu
et al., MAGVIT-v2 (2023); Su et al., RoFormer (2021); Chen et al., Diffusion Forcing (2024); Yin et al., CausVid (2024);
Huang et al., Self Forcing (2025); Google DeepMind, Genie 3 (2025); Mildenhall et al., NeRF (2020); Tancik et al.,
Fourier Features (2020); Müller et al., Instant-NGP (2022); Porter & Duff, Compositing Digital Images (1984); Zwicker,
Pfister, van Baar & Gross, EWA Splatting (2001); Kerbl, Kopanas, Leimkühler & Drettakis, 3D Gaussian Splatting (2023);
Wang et al., DUSt3R (2024); Wang et al., VGGT (2025).

## Problems

1. A ViT cuts a 224 × 224 picture into p × p patches. How many tokens for p = 16 and p = 8? By what factors do
   attention's and the MLPs' costs grow when p halves?
2. In an adaLN-Zero block with every gate α = 0, show the block is the identity and the gradients of its attention
   weights vanish, but the gradient of the gate's map W does not.
3. Derive the resolution shift σ_m = ασ_n / (1 + (α − 1)σ_n) from equal uncertainty about a flat picture, show it lowers
   the log signal-to-noise ratio by 2 log α, and evaluate it for σ_n = 0.5, α = 3.
4. MaskGIT draws 256 tokens in T = 8 passes, leaving ⌊256 cos(π k / 2T)⌋ masked after pass k. How many are fixed in each
   pass? Compare a linear schedule.
5. For density σ and colour c constant on [t_i, t_i + δ], show ∫ T σ c dt = T_i (1 − e^{−σδ}) c, and that the weights
   T_i α_i sum to 1 − T_{N+1}.
6. Compute the Jacobian of (u, v) = (f x / z, f y / z), and the projected covariance of an isotropic Gaussian s² I centred
   on the optical axis at depth z.

### Solutions

1. (224/16)² = 196 patch tokens (197 with the summary token); (224/8)² = 784. Halving p multiplies the number of tokens N
   by 4. Attention's score and mixing cost grows like N² d: 16 times. The MLPs and the projections cost about N d² per
   layer: 4 times. The patch embedding touches each pixel once either way, so its cost doesn't change.
2. The block computes h + α₁ ⊙ Attn(·) and then adds α₂ ⊙ MLP(·); with α = W c + b = 0 both branches vanish and the
   output is h. Any parameter θ inside a branch reaches the loss only through α ⊙ F(θ), so ∂L/∂θ = α ⊙ (∂L/∂out) ∂F/∂θ = 0
   (this includes the branch's scale and shift γ, β). But ∂L/∂α = (∂L/∂out) ⊙ F(·), which is generally non-zero, and
   ∂L/∂W = (∂L/∂α) cᵀ ≠ 0. The first step opens the gates; after that the branches learn.
3. For a flat picture, every pixel z_i = (1 − σ) c + σ ε_i; averaging n pixels gives z̄ = (1 − σ) c + σ ε̄ with
   ε̄ ~ N(0, 1/n), so ĉ = z̄ / (1 − σ) has standard deviation σ / ((1 − σ)√n). Setting it equal at m and n pixels:
   σ_m / (1 − σ_m) = α σ_n / (1 − σ_n) with α = √(m/n); solving, σ_m = α σ_n / (1 + (α − 1) σ_n). With SNR = (1 − σ)²/σ²,
   log SNR_m = 2 log((1 − σ_m)/σ_m) = 2 log((1 − σ_n)/(α σ_n)) = log SNR_n − 2 log α. For σ_n = 0.5, α = 3:
   σ_m = 1.5 / 2 = 0.75.
4. Still masked after passes 0 … 8: 256, 251, 236, 212, 181, 142, 97, 49, 0; so the passes fix 5, 15, 24, 31, 39, 45, 48
   and 49 tokens. A linear schedule fixes 32 every pass. The cosine schedule commits few tokens while the model knows
   least, and more once most of the picture is fixed.
5. On the segment T(t) = T_i e^{−σ(t − t_i)}, so ∫ T σ c dt = T_i c ∫₀^δ σ e^{−σs} ds = T_i c (1 − e^{−σδ}) = T_i α_i c.
   Since T_{i+1} = T_i (1 − α_i), T_i α_i = T_i − T_{i+1}, and the sum telescopes to T_1 − T_{N+1} = 1 − T_{N+1}: the
   weights sum to at most 1, and the rest is the background's share.
6. J = [[f/z, 0, −f x/z²], [0, f/z, −f y/z²]]. On the axis (x = y = 0), J = (f/z) [I₂ | 0], so
   Σ' = J (s² I) Jᵀ = (f s / z)² I₂: a circle whose radius shrinks like 1/z, as perspective requires.

## 习题（中文）

1. ViT把224 × 224的图片切成p × p的图块。p = 16和p = 8时各有多少个词元？p减半时，注意力和MLP的计算量各增长多少倍？
2. 在一个所有门控α = 0的adaLN-Zero块中，证明这个块是恒等映射，它的注意力权重的梯度为零，但门控映射W的梯度不为零。
3. 由“对一张均匀图片的不确定性相同”推导分辨率偏移σ_m = ασ_n / (1 + (α − 1)σ_n)，证明它把对数信噪比降低2 log α，并计算
   σ_n = 0.5、α = 3时的值。
4. MaskGIT用T = 8次前向传播生成256个词元，第k次之后还有⌊256 cos(πk/2T)⌋个被掩码。每一次固定多少个词元？与线性调度比较。
5. 若密度σ和颜色c在[t_i, t_i + δ]上为常数，证明∫ T σ c dt = T_i (1 − e^{−σδ}) c，并证明权重T_i α_i之和等于1 − T_{N+1}。
6. 求(u, v) = (f x / z, f y / z)的雅可比矩阵，以及中心在光轴上、深度为z的各向同性高斯s² I投影后的协方差。

### 解答

1. (224/16)² = 196个图块词元（加上汇总词元是197个）；(224/8)² = 784个。p减半，词元数N变为4倍。注意力的打分和混合代价按
   N² d增长：16倍。MLP和各个投影每层约为N d²：4倍。图块嵌入无论如何每个像素只碰一次，代价不变。
2. 这个块先计算h + α₁ ⊙ Attn(·)，再加上α₂ ⊙ MLP(·)；α = W c + b = 0时两个分支都消失，输出就是h。分支内部的任何参数θ只通过
   α ⊙ F(θ)影响损失，所以∂L/∂θ = α ⊙ (∂L/∂out) ∂F/∂θ = 0（分支的缩放γ和平移β也一样）。但∂L/∂α = (∂L/∂out) ⊙ F(·)一般
   不为零，∂L/∂W = (∂L/∂α) cᵀ ≠ 0。第一步就把门打开；此后分支才开始学习。
3. 对一张均匀图片，每个像素z_i = (1 − σ) c + σ ε_i；对n个像素求平均得z̄ = (1 − σ) c + σ ε̄，ε̄ ~ N(0, 1/n)，所以
   ĉ = z̄ / (1 − σ)的标准差是σ / ((1 − σ)√n)。令m个和n个像素时两者相等：σ_m / (1 − σ_m) = α σ_n / (1 − σ_n)，α = √(m/n)；
   解得σ_m = α σ_n / (1 + (α − 1) σ_n)。由SNR = (1 − σ)²/σ²，log SNR_m = 2 log((1 − σ_m)/σ_m) = 2 log((1 − σ_n)/(α σ_n))
   = log SNR_n − 2 log α。σ_n = 0.5、α = 3时，σ_m = 1.5 / 2 = 0.75。
4. 第0到第8次之后仍被掩码的个数：256, 251, 236, 212, 181, 142, 97, 49, 0；所以每次分别固定5, 15, 24, 31, 39, 45, 48,
   49个词元。线性调度每次固定32个。余弦调度在模型知道得最少时只确定少数词元，等大部分图片已经确定后再加快。
5. 在这一段上T(t) = T_i e^{−σ(t − t_i)}，所以∫ T σ c dt = T_i c ∫₀^δ σ e^{−σs} ds = T_i c (1 − e^{−σδ}) = T_i α_i c。
   由T_{i+1} = T_i (1 − α_i)得T_i α_i = T_i − T_{i+1}，求和逐项相消，得T_1 − T_{N+1} = 1 − T_{N+1}：权重之和至多为1，其余是
   背景的份额。
6. J = [[f/z, 0, −f x/z²], [0, f/z, −f y/z²]]。在光轴上（x = y = 0），J = (f/z) [I₂ | 0]，所以Σ' = J (s² I) Jᵀ =
   (f s / z)² I₂：一个圆，半径按1/z缩小，正如透视所要求的。

## Glossary

| English | 中文 |
|---|---|
| vision transformer (ViT) | 视觉Transformer（ViT） |
| patch, patch embedding | 图块，图块嵌入 |
| summary token ([CLS]) | 汇总词元（[CLS]） |
| learned position vector (position embedding) | 学到的位置向量（位置嵌入） |
| attention distance | 注意力距离 |
| inductive bias; locality; translation equivariance | 归纳偏置；局部性；平移等变 |
| latent space, latent diffusion | 潜空间，潜空间扩散 |
| perceptual and semantic compression | 感知压缩与语义压缩 |
| spatial compression factor (f8, f32), latent channels | 空间压缩倍数（f8，f32），潜变量通道 |
| deep compression autoencoder (DC-AE), space-to-channel | 深度压缩自编码器（DC-AE），空间到通道 |
| reconstruction–generation dilemma | 重建与生成的两难 |
| representation alignment (REPA), projector | 表示对齐（REPA），投影头 |
| representation autoencoder (RAE) | 表示自编码器（RAE） |
| U-Net, skip connection | U-Net，跳跃连接 |
| diffusion transformer (DiT) | 扩散Transformer（DiT） |
| adaptive layer norm (adaLN), adaLN-Zero, gate | 自适应层归一化（adaLN），adaLN-Zero，门控 |
| in-context conditioning | 上下文条件（作为额外词元） |
| cross-attention | 交叉注意力 |
| multiply-adds (MACs) per picture | 每张图片的乘加次数 |
| MM-DiT, joint attention, QK-norm | MM-DiT，联合注意力，QK归一化 |
| logit-normal timestep sampling | 对数几率正态（logit-normal）时间步采样 |
| resolution-dependent timestep shift | 随分辨率的时间步偏移 |
| recaptioning | 重新标注（用模型写详细描述） |
| vector-quantized tokenizer, VQGAN | 向量量化分词器，VQGAN |
| raster order | 光栅顺序 |
| masked generative transformer (MaskGIT), cosine schedule | 掩码生成式Transformer（MaskGIT），余弦调度 |
| next-scale prediction (VAR), residual quantization, block-causal mask | 下一尺度预测（VAR），残差量化，块因果掩码 |
| bitwise tokens | 按位词元 |
| unified model, mixture of transformer experts (MoT) | 统一模型，Transformer专家混合（MoT） |
| in-context editing | 上下文编辑 |
| spacetime patches | 时空图块 |
| causal 3D autoencoder | 因果三维自编码器 |
| 3D rotary positions (3D RoPE) | 三维旋转位置编码（3D RoPE） |
| joint image–video training | 图像与视频联合训练 |
| full-sequence diffusion | 全序列扩散 |
| teacher forcing, diffusion forcing, self forcing | 教师强制，扩散强制，自我强制 |
| exposure bias, rollout | 暴露偏差，滚动生成（推演） |
| neural radiance field (NeRF) | 神经辐射场（NeRF） |
| volume rendering, transmittance, alpha compositing | 体渲染，透射率，阿尔法合成 |
| positional encoding (Fourier features) | 位置编码（傅里叶特征） |
| PSNR | 峰值信噪比（PSNR） |
| 3D Gaussian splatting, covariance projection, EWA splatting | 三维高斯泼溅，协方差投影，EWA泼溅 |
| Jacobian | 雅可比矩阵 |
| Fréchet distance (FD) on a judge's features | 评判网络特征上的弗雷歇距离（FD） |
