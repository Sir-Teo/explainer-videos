# AI, Built — Part 10: Seeing and Remembering

Part 10 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). The deep-learning turn of 2012 in vision and in sequences: convolution and what it
buys, LeNet, ImageNet and AlexNet, the deeper networks that followed, what their filters learn and how easily they are
fooled, cheaper convolutions; then recurrent networks and their vanishing gradients, the LSTM and the GRU, a character
LSTM on the series' scoreboard, sequence-to-sequence translation, the birth of attention, and the recurrent networks
of today. Every network in this part is trained on the computer that renders the video (`compute.py`), on MNIST,
CIFAR-10 and Part 1's thirty novels; numbers about historical systems are the published ones, cited on screen
(`specs.py`).

* **The edge that lit a neuron.** Hubel and Wiesel's cat (late 1950s; *J. Physiol.* 1959): a cell that fires for an
  edge at one angle; the 48 first-layer filters of our CIFAR-10 network, and how many of them pick out one
  orientation; our encoder–decoder's attention while it reverses a string; the path of the part; objectives.
* **1. Vision before deep learning.** Simple and complex cells (Hubel & Wiesel 1962; Nobel 1981); the image gradient
  and Sobel's operator (1968) computed on a digit and a photograph; SIFT (Lowe 1999, 2004) and histograms of oriented
  gradients (Dalal & Triggs 2005), HOG computed here; the hand-made pipeline (features, coding, pooling, a linear SVM)
  and the first two ImageNet winners (NEC-UIUC 28.2%, XRCE 25.8% top-5; Russakovsky et al. 2015); a linear
  classifier on raw pixels against the same classifier on our HOG features, MNIST and CIFAR-10, three seeds.
* **2. Convolution.** Weight sharing: six 28 × 28 maps from 3.7 million weights (fully connected), 122,304 (local,
  unshared) or 156 (shared); the definition (deep learning's cross-correlation); a learned LeNet kernel sweeping out
  a feature map; translation equivariance proved step by step; checked on our digit: circular padding exact, zero
  padding exact away from the border, a dense layer of the same shape not at all.
* **3. Receptive fields, stride and pooling.** The cone of a deep unit; r_ℓ = r_{ℓ−1} + (k_ℓ − 1) j_{ℓ−1}, j_ℓ =
  j_{ℓ−1} s_ℓ derived; computed from the published layer lists for LeNet-5, AlexNet, VGG-16 and ResNet-50; max pooling,
  and how a stride breaks exact equivariance for odd shifts (computed); Azulay & Weiss (2019), Zhang (2019).
* **4. LeNet and MNIST.** Fukushima's Neocognitron (1980); LeCun et al. (1989): backpropagation through shared
  weights on 7,291 zip-code digits, 5.0% test error (figures as reproduced by Karpathy 2022); Waibel et al.'s
  time-delay network (1989); LeNet-5 and MNIST (LeCun, Bottou, Bengio & Haffner 1998: 0.95%, 0.8% with distortions;
  several million checks a day); our LeNet trained here, three seeds, the first replayed: test error, its six kernels
  and its feature maps of one digit at eleven checkpoints; digits it gets wrong; LeNet against an MLP of the same
  size (three seeds): on shifted digits, and with the pixels shuffled by one fixed permutation.
* **5. ImageNet and AlexNet.** Deng et al. (CVPR 2009), WordNet and Mechanical Turk; ILSVRC (1,000 classes,
  1,281,167 training images, top-5 error); 2010–2012 results (ISI's Fisher vectors 26.2%, SuperVision 16.4% and 15.3%
  with extra data); AlexNet's weights and multiply-adds layer by layer, computed from the published architecture
  (60,965,224 weights; 4% in the convolutions, 92% of the multiply-adds there); the hardware side is Part 17's
  chapter 4; Cireșan et al.'s GPU networks (traffic signs, IJCNN 2011: 99.46% against 98.84% for people), Hinton et
  al. (2012) in speech, ILSVRC 2013, the 2018 Turing Award.
* **6. Why AlexNet won.** ReLU (Nair & Hinton 2010; Glorot, Bordes & Bengio 2011) and the slopes of the
  activations; AlexNet's CIFAR-10 measurement (six times faster to 25% training error); our race of ReLU, tanh and
  sigmoid in a six-layer CNN (SGD with momentum, three seeds); dropout (Hinton et al. 2012; Srivastava et al. 2014)
  on 5,000 digits, with and without (three seeds); test error against training-set size (500 to 60,000 digits, equal
  steps, three seeds) and its power-law slope; shifted copies as augmentation; none of it new, all of it together.
* **7. Deeper: VGG, Inception, ResNet.** The winning top-5 error by year, 2010–2017 (Russakovsky et al. 2015; He et
  al. 2015; Hu et al. 2017), and Karpathy's 5.1%; VGG (Simonyan & Zisserman 2014): two 3×3 layers for one 5×5,
  derived, and VGG-16 counted (138 million weights, 15.5 billion multiply-adds); GoogLeNet's Inception module (Szegedy
  et al. 2014); the degradation problem, batch normalization (Ioffe & Szegedy 2015), residual networks (He, Zhang, Ren
  & Sun 2015) and highway networks (Srivastava, Greff & Schmidhuber 2015); ImageNetV2 (Recht et al. 2019).
* **8. What the filters learn.** CIFAR-10 (Krizhevsky 2009); our network (48 kernels of 7×7×3 at stride 2, three more
  layers) trained here, ten epochs; the replay of its first layer, noise to oriented edges and colour-opponent blobs
  (compare Krizhevsky et al.'s figure 3); Hubel and Wiesel's experiment run on our filters (gratings at 16 angles,
  orientation selectivity, trained against untrained); top-activating patches and images of deeper channels (Zeiler &
  Fergus 2013).
* **9. Adversarial examples.** Szegedy et al. (2013); the panda and the gibbon (Goodfellow, Shlens & Szegedy 2014);
  the linearity argument and the fast gradient sign method derived; our LeNet fooled; error under FGSM and 20-step PGD
  against ε for a linear model, an MLP and LeNet (three seeds); transfer between models; CIFAR-10 photographs changed
  by two grey levels; adversarial training (fast FGSM with a random start, Wong, Rice & Kolter 2020; Madry et al. 2017), three
  seeds, against one-step and 20-step attacks; attacks on language models (Part 31).
* **10. Cheaper convolutions.** Depthwise separable convolutions (Sifre 2014; Chollet 2016) and their cost ratio
  1/C′ + 1/k², derived; measured on this computer against the FLOP ratio; MobileNet (Howard et al. 2017, table 8);
  dilated convolutions (the algorithme à trous, Holschneider et al. 1989; WaveNet, van den Oord et al. 2016) and their receptive fields; the vision transformer (Dosovitskiy et al. 2020, Part 22), ConvNeXt (Liu et
  al. 2022: ResNet-50 modernized from 76.1% to 82.0% against Swin-T's 81.3%; 87.8% with ImageNet-22K) and
  convolutional networks at scale (Smith et al. 2023).
* **11. Recurrence and vanishing gradients.** Jordan (1986), Elman (1990); backpropagation through time (Werbos 1990);
  the product of Jacobians and its bound σ_max(W)^{T−k} derived (Hochreiter 1991; Bengio, Simard & Frasconi 1994);
  measured on random tanh and linear RNNs at four spectral radii (twelve networks each); a one-unit RNN's loss cliff
  and gradient descent across it with and without clipping (after Pascanu, Mikolov & Bengio 2013).
* **12. LSTM and GRU.** The constant error carousel (Hochreiter & Schmidhuber 1997), input and output gates, the
  forget gate (Gers, Schmidhuber & Cummins 2000); the cell as a conveyor belt; ∂c_t/∂c_{t−1} = diag(f_t) and the
  memory's half-life, derived; the GRU (Cho et al. 2014; Chung et al. 2014); the memory task (remember the first of
  T = 10, 30, 100 symbols): RNN, LSTM and GRU, three seeds each, the gated cells from the chrono initialization
  (Tallec & Ollivier 2018; in an earlier run with PyTorch's default gate biases, the LSTM stayed at chance at T = 30
  in all three seeds, 12–14%),
  accuracy during training, and the gradient reaching each time step, replayed.
* **13. A character LSTM.** 512 cells on Part 1's thirty novels, truncated backpropagation through time with 64
  readers (after Karpathy 2015); its training replayed with what it writes at each checkpoint; its row on the
  scoreboard (bits per character on chapter 2 of *The Maltese Falcon*), beside Part 7's Kneser–Ney and Part 9's neural
  models; a cell that tracks quotation marks (Karpathy, Johnson & Fei-Fei 2015; Radford, Józefowicz & Sutskever 2017);
  the surprise of each character.
* **14. Sequence to sequence.** Phrase-based translation (Koehn, Och & Marcu 2003); Sutskever, Vinyals & Le (2014):
  34.81 BLEU against 33.30, reversing the source (25.9 → 30.6); Cho et al. (2014); teacher forcing (Williams & Zipser
  1989) and exposure bias; greedy decoding and beam search on our character LSTM, and
  degeneration (Holtzman et al. 2019); our encoder–decoder reversing strings: accuracy against length, the bottleneck;
  GNMT (Wu et al. 2016): 60% fewer errors, Chinese–English in production in September 2016.
* **15. The birth of attention.** Bahdanau, Cho & Bengio (2014): the additive score, the softmax, the context
  vector; one step of our model; with and without attention at equal training (three seeds), inside and beyond the
  training lengths; the alignment forming during training; their Table 1 (17.82 → 26.75 BLEU; 36.15 against Moses's
  35.63 without unknown words); neural Turing machines and memory networks (2014), Luong et al. and Xu et al. (2015),
  the Transformer (2017; Parts 13 and 14).
* **16. Recurrence returns.** Why the Transformer won training and why recurrence wins generation (Part 15); linear
  recurrences and the parallel prefix scan (Blelloch 1990; Martin & Cundy 2018), associativity derived; the scan
  against the loop, measured here, narrow and wide states; minGRU (Feng et al. 2024) on our memory task beside the
  others; QRNN, SRU, S4, LRU, RWKV, Mamba, xLSTM (2024; 7B in 2025) and today's hybrids.
* **Recap**, where it comes back (Parts 11, 13, 14, 15, 22, 25, 31), the problem set, Part 11's preview (three
  optimizers in one valley, computed), references.

Run from the repo root:

```
python tools/make.py ai10                               # everything: the computations, then the films, resumable
nice -n 15 python -m videos.ai.ai10.compute             # every experiment (see below for how long)
nice -n 15 python -m videos.ai.ai10.compute charlstm    # one item (--force to recompute)
python tools/build.py ai10                              # English
python tools/build.py ai10 --lang zh                    # Chinese
```

How long: here, on two threads of a shared four-core Linux server that was running other jobs at the same time, the
experiments took about ten hours in all: the character LSTM two and a half, the memory task and seq2seq over an hour
each, the CIFAR-10 network, adversarial training, the data-size curve, dropout and the activations 40 to 55 minutes
each, the rest minutes. A quiet machine is faster. `make.py` first computes the parts whose results this one reads
(Parts 1, 7 and 9) and what those read in turn (Parts 5 and 6), which adds their own time.

The data: MNIST from PyTorch's mirror of the original files and CIFAR-10 from Alex Krizhevsky's page, downloaded
once into `.cache/ai10/` (resuming a broken download) and accepted only if their SHA-256 matches (`data.py`); Part 1's
novels through Part 1's `compute`. The long jobs checkpoint as they go: LeNet and the CIFAR-10 network after every
epoch, the character LSTM every 100 steps (`.cache/ai10/models/*.ckpt`, with the optimizer, the random generators
and the LSTM readers' memory), and the many short runs of the comparisons (activations, dropout, data size,
adversarial training, the memory task, seq2seq) one by one in `.cache/ai10/<item>.partial.json`; a killed run
resumes there. Every random choice is seeded. Training uses two threads (`torch.set_num_threads(2)`); nothing forks,
so the same code runs on macOS (Apple Silicon) and Linux. The scoreboard row reads Parts 1, 7 and 9 through their own
`compute` modules, so `make.py` computes those first.

`nets.py` holds the networks (LeNet-5, the MLP, the plain CNN, the CIFAR-10 network, the recurrent cells with minGRU
and its scan, the character LSTM, the encoder–decoder with Bahdanau attention), `data.py` the datasets, `specs.py` the
published numbers with their sources, and `compute.py` the experiments.

References. Books: Goodfellow, Bengio & Courville, *Deep Learning* (2016); Szeliski, *Computer Vision: Algorithms and
Applications*, 2nd ed. (2022); Zhang, Lipton, Li & Smola, *Dive into Deep Learning* (2023); Graves, *Supervised
Sequence Labelling with Recurrent Neural Networks* (2012). Papers: Hubel & Wiesel (1959, 1962); Sobel & Feldman
(1968); Fukushima (1980); LeCun et al. (1989, 1998); Waibel et al. (1989); Lowe (1999, 2004); Dalal & Triggs (2005);
Deng et al. (2009); Russakovsky et al. (2015); Krizhevsky (2009); Krizhevsky, Sutskever & Hinton (2012); Cireșan,
Meier, Masci & Schmidhuber (2012); Hinton et al. (2012, speech); Nair & Hinton (2010); Glorot, Bordes & Bengio (2011);
Hinton et al. (2012, dropout); Srivastava et al. (2014); Raina, Madhavan & Ng (2009); Simonyan & Zisserman (2014);
Szegedy et al. (2014); Ioffe & Szegedy (2015); He, Zhang, Ren & Sun (2015); Srivastava, Greff & Schmidhuber (2015);
Hu, Shen & Sun (2017); Recht, Roelofs, Schmidt & Shankar (2019); Zeiler & Fergus (2013); Simonyan, Vedaldi &
Zisserman (2013); Olah, Mordvintsev & Schubert (2017); Luo, Li, Urtasun & Zemel (2016); Azulay & Weiss (2019); Zhang
(2019); Szegedy et al. (2013); Goodfellow, Shlens & Szegedy (2014); Madry et al. (2017); Wong, Rice & Kolter (2020);
Sifre (2014); Chollet (2016); Howard et al. (2017); Holschneider et al. (1989); Yu & Koltun (2015); van den Oord et
al. (2016); Dosovitskiy et al. (2020); Liu et al. (2022); Smith, Brock, Berrada & De (2023); Jordan (1986); Elman
(1990); Werbos (1990); Hochreiter (1991); Bengio, Simard & Frasconi (1994); Pascanu, Mikolov & Bengio (2013);
Hochreiter & Schmidhuber (1997); Gers, Schmidhuber & Cummins (2000); Tallec & Ollivier (2018); Cho et al. (2014); Chung et al. (2014); Karpathy
(2015); Karpathy, Johnson & Fei-Fei (2015); Radford, Józefowicz & Sutskever (2017); Koehn, Och & Marcu (2003);
Papineni et al. (2002); Sutskever, Vinyals & Le (2014); Williams & Zipser (1989); Bengio, Vinyals, Jaitly & Shazeer
(2015); Holtzman et al. (2019); Wu et al. (2016); Bahdanau, Cho & Bengio (2014); Graves, Wayne & Danihelka (2014);
Weston, Chopra & Bordes (2014); Luong, Pham & Manning (2015); Xu et al. (2015); Vaswani et al. (2017); Blelloch
(1990); Martin & Cundy (2018); Bradbury et al. (2016); Lei et al. (2017); Gu, Goel & Ré (2021); Orvieto et al.
(2023); Peng et al. (2023); Gu & Dao (2023); Beck et al. (2024, 2025); Feng, Tung, Ahmed, Bengio & Hajimirsadeghi
(2024).

## Problems, with solutions

**1. Equivariance, both ways.** Show that circular cross-correlation commutes with every shift T_s. Conversely, show
that a linear map on ℝⁿ (indices mod n) that commutes with all shifts is a circular cross-correlation.

*Solution.* With (T_s x)[i] = x[i − s] and (w ⋆ x)[i] = Σ_u w[u] x[i + u], all indices mod n:
(w ⋆ T_s x)[i] = Σ_u w[u] x[i + u − s] = (w ⋆ x)[i − s] = (T_s(w ⋆ x))[i]. Conversely, let A be linear with
A T_s = T_s A for every s, and let e_0 be the first basis vector. Every x is Σ_j x[j] T_j e_0, so
Ax = Σ_j x[j] T_j (A e_0). Write g = A e_0; then (Ax)[i] = Σ_j x[j] g[i − j] = Σ_u x[i + u] g[−u]. That is
w ⋆ x with w[u] = g[−u]. (So convolution is not one choice among many shift-equivariant linear layers: it is the only
one.)

**2. Receptive fields.** Prove r_L = 1 + Σ_ℓ (k_ℓ − 1) Π_{i<ℓ} s_i and compute it for AlexNet: conv1 11/4, pool 3/2,
conv2 5/1, pool 3/2, conv3–5 3/1, pool 3/2.

*Solution.* A unit of layer ℓ is a function of k_ℓ adjacent units of layer ℓ − 1, whose centres lie j_{ℓ−1} pixels
apart, where j_{ℓ−1} = Π_{i<ℓ} s_i is the product of the strides below. Their fields are each r_{ℓ−1} wide and
overlap except for the shifts, so r_ℓ = r_{ℓ−1} + (k_ℓ − 1) j_{ℓ−1}; summing from r_0 = 1 gives the formula. For
AlexNet the jumps before each layer are 1, 4, 8, 8, 16, 16, 16, 16, so r = 1 + 10·1 + 2·4 + 4·8 + 2·8 + 2·16 + 2·16 +
2·16 + 2·16 = 1 + 10 + 8 + 32 + 16 + 32 + 32 + 32 + 32 = 195 pixels.

**3. Separable convolutions.** Derive the cost ratio 1/C′ + 1/k² of a depthwise separable convolution. For k = 3 and
C′ = 512, how much cheaper is it? Why can the measured speed-up be smaller?

*Solution.* A standard layer computes, at each of H·W positions and for each of C′ outputs, a k·k·C dot product:
H W C C′ k² multiply-adds. The depthwise step does a k·k product per channel per position, H W C k²; the pointwise step
a C-long product per output per position, H W C C′. The ratio is (H W C k² + H W C C′)/(H W C C′ k²) = 1/C′ + 1/k². For
k = 3, C′ = 512: 1/512 + 1/9 ≈ 0.113, about 8.8 times cheaper. The depthwise step uses each weight on one channel only,
so it does about k² operations per number it reads (arithmetic intensity is low), and on most hardware it runs far
below peak, bound by memory bandwidth (Part 17's roofline); the time saved is then less than the arithmetic saved.

**4. The fast gradient sign method.** For a linear score w·x, show max_{‖η‖_∞≤ε} w·η = ε‖w‖₁. With a margin of 3
between two classes and ‖w_y − w_{y′}‖₁ = 300, which ε flips the decision?

*Solution.* w·η = Σ_i w_i η_i ≤ Σ_i |w_i| |η_i| ≤ ε Σ_i |w_i|, with equality when η_i = ε sign(w_i). The decision
between y and y′ depends on the difference of their scores, (w_y − w_{y′})·x = 3; the attack η = −ε sign(w_y −
w_{y′}) lowers it by ε‖w_y − w_{y′}‖₁ = 300ε, so any ε > 3/300 = 0.01 flips it (ignoring the clipping of pixels to
[0, 1]), a change of 1% of the pixel range in every pixel.

**5. The memory's half-life.** For an LSTM with i_t = 0 and f_t = f, show c_T = f^{T−k} c_k, find the half-life of
the memory, and say why the forget gate's bias is often started at 1.

*Solution.* With no input, c_t = f c_{t−1}, so by induction c_T = f^{T−k} c_k, and the gradient ∂c_T/∂c_k = f^{T−k}
I decays the same way. Half of the memory is gone when f^n = 1/2, after n = ln 2/(−ln f) ≈ 0.69/(1 − f) steps for f
near 1: 69 steps for f = 0.99. A forget gate is σ(W[h, x] + b_f); with small random weights at initialization it sits
near σ(b_f), which is 0.5 for b_f = 0 (a half-life of one step: the network starts out forgetting everything) and
σ(1) ≈ 0.73 for b_f = 1 (about 2.2 steps, and larger biases give longer memories). Starting near remembering lets
gradients reach back while the gates learn (Gers et al. 2000; Józefowicz et al. 2015).

**6. The scan.** Show that (a, b) ∘ (a′, b′) = (aa′, a′b + b′) is associative, and that the Hillis–Steele scan finds
every h_t of h_t = a_t h_{t−1} + b_t in ⌈log₂ T⌉ rounds.

*Solution.* Read (a, b) as the affine map h ↦ ah + b; then (a, b) ∘ (a′, b′) is "apply (a, b), then (a′, b′)": h ↦
a′(ah + b) + b′ = (aa′)h + (a′b + b′). Composition of maps is associative, so ∘ is. In round r = 1, 2, …, every
position t ≥ d (d = 2^{r−1}) combines its pair with that of t − d. By induction, after round r position t holds the
composition of the steps from max(1, t − 2^r + 1) to t: true for r = 0 (each step alone), and round r joins two
adjacent blocks of 2^{r−1} steps. After ⌈log₂ T⌉ rounds every block reaches back to step 1, and from h_0 = 0 the b
part is h_t. Each round costs O(T), so the work is O(T log T) (Blelloch's work-efficient scan does it in O(T) work and
2 log₂ T rounds).

## 习题与解答

**1. 两个方向的等变性。** 证明循环互相关与每个平移T_s可交换。反过来，证明ℝⁿ上（下标取模n）与所有平移可交换的线性映射一定是循环
互相关。

*解答。* 记 (T_s x)[i] = x[i − s]，(w ⋆ x)[i] = Σ_u w[u] x[i + u]，下标都取模n：
(w ⋆ T_s x)[i] = Σ_u w[u] x[i + u − s] = (w ⋆ x)[i − s] = (T_s(w ⋆ x))[i]。反过来，设A线性，且对每个s都有 A T_s = T_s A，
e_0是第一个基向量。每个x都可写成 Σ_j x[j] T_j e_0，所以 Ax = Σ_j x[j] T_j (A e_0)。令 g = A e_0，则
(Ax)[i] = Σ_j x[j] g[i − j] = Σ_u x[i + u] g[−u]，这正是 w[u] = g[−u] 的 w ⋆ x。（所以卷积不是众多平移等变线性层中的一种
选择，而是唯一的一种。）

**2. 感受野。** 证明 r_L = 1 + Σ_ℓ (k_ℓ − 1) Π_{i<ℓ} s_i，并对AlexNet计算：conv1 11/4，池化3/2，conv2 5/1，池化3/2，
conv3–5 3/1，池化3/2。

*解答。* 第ℓ层的一个单元是第ℓ − 1层k_ℓ个相邻单元的函数，这些单元的中心彼此相隔j_{ℓ−1}个像素，其中 j_{ℓ−1} = Π_{i<ℓ} s_i 是下面
各层步长的乘积。它们的感受野各宽r_{ℓ−1}，除了平移之外彼此重叠，所以 r_ℓ = r_{ℓ−1} + (k_ℓ − 1) j_{ℓ−1}；从 r_0 = 1 求和就得到
公式。AlexNet各层之前的跳距依次是1, 4, 8, 8, 16, 16, 16, 16，所以 r = 1 + 10·1 + 2·4 + 4·8 + 2·8 + 2·16 + 2·16 + 2·16 + 2·16
= 195个像素。

**3. 可分离卷积。** 推导深度可分离卷积的代价比 1/C′ + 1/k²。k = 3、C′ = 512时便宜多少？为什么实测的加速可能更小？

*解答。* 标准卷积在H·W个位置上、对C′个输出各算一个k·k·C的点积：H W C C′ k²次乘加。深度卷积对每个通道、每个位置算一个k·k的乘积，
H W C k²次；逐点卷积对每个输出、每个位置算一个长C的乘积，H W C C′次。两者之比是 (H W C k² + H W C C′)/(H W C C′ k²) =
1/C′ + 1/k²。k = 3、C′ = 512时为 1/512 + 1/9 ≈ 0.113，大约便宜8.8倍。深度卷积的每个权重只作用于一个通道，每读一个数只做大约k²次
运算（算术强度低），在多数硬件上它远低于峰值、受内存带宽限制（第17部分的屋顶线），省下的时间就少于省下的算术。

**4. 快速梯度符号法。** 对线性打分 w·x，证明 max_{‖η‖_∞≤ε} w·η = ε‖w‖₁。若两类之间的间隔是3，且 ‖w_y − w_{y′}‖₁ = 300，
多大的ε能翻转判决？

*解答。* w·η = Σ_i w_i η_i ≤ Σ_i |w_i| |η_i| ≤ ε Σ_i |w_i|，取 η_i = ε sign(w_i) 时取等号。y与y′之间的判决取决于两者打分之差
(w_y − w_{y′})·x = 3；攻击 η = −ε sign(w_y − w_{y′}) 把它降低 ε‖w_y − w_{y′}‖₁ = 300ε，所以任何 ε > 3/300 = 0.01 都能翻转它
（不计像素被截到[0, 1]），也就是每个像素改动像素范围的1%。

**5. 记忆的半衰期。** 对 i_t = 0、f_t = f 的LSTM，证明 c_T = f^{T−k} c_k，求记忆的半衰期，并说明为什么遗忘门的偏置常常从1开始。

*解答。* 没有输入时 c_t = f c_{t−1}，归纳得 c_T = f^{T−k} c_k，梯度 ∂c_T/∂c_k = f^{T−k} I 也以同样方式衰减。当 f^n = 1/2，
即 n = ln 2/(−ln f) ≈ 0.69/(1 − f) 步（f接近1时）后，记忆剩下一半：f = 0.99时是69步。遗忘门是 σ(W[h, x] + b_f)；初始化时权重
小而随机，它停在σ(b_f)附近：b_f = 0时是0.5（半衰期一步：网络一开始什么都忘），b_f = 1时是σ(1) ≈ 0.73（约2.2步，偏置更大，记忆
更长）。从“记住”附近出发，梯度就能在门学会之前传回去（Gers等，2000；Józefowicz等，2015）。

**6. 扫描。** 证明 (a, b) ∘ (a′, b′) = (aa′, a′b + b′) 满足结合律，并证明Hillis–Steele扫描在⌈log₂ T⌉轮内求出
h_t = a_t h_{t−1} + b_t 的每一个h_t。

*解答。* 把(a, b)看作仿射映射 h ↦ ah + b；那么 (a, b) ∘ (a′, b′) 就是“先做(a, b)，再做(a′, b′)”：h ↦ a′(ah + b) + b′ =
(aa′)h + (a′b + b′)。映射的复合满足结合律，所以∘也满足。在第r = 1, 2, …轮，每个位置t ≥ d（d = 2^{r−1}）把自己的一对数与位置
t − d的合并。归纳可知，第r轮之后位置t保存的是从 max(1, t − 2^r + 1) 到t各步的复合：r = 0时成立（每步单独），第r轮把两个相邻的、
各含2^{r−1}步的块接起来。⌈log₂ T⌉轮之后，每个块都回溯到第1步，从 h_0 = 0 出发，b那一部分就是h_t。每轮代价O(T)，总工作量
O(T log T)（布莱洛克的工作量最优扫描用O(T)工作量、2 log₂ T轮完成）。

## Glossary (new terms, for AI_ZH_GUIDE.md)

| English | 中文 |
|---|---|
| computer vision | 计算机视觉 |
| visual cortex, receptive field (of a neuron) | 视觉皮层，（神经元的）感受野 |
| simple cell, complex cell | 简单细胞，复杂细胞 |
| orientation selectivity, tuning curve, grating | 方向选择性，调谐曲线，光栅 |
| colour-opponent cell | 颜色拮抗细胞 |
| edge, image gradient, Sobel operator | 边缘，图像梯度，索贝尔算子 |
| feature descriptor: SIFT, HOG (histogram of oriented gradients) | 特征描述子：SIFT，HOG（方向梯度直方图） |
| keypoint, cell, block normalization | 关键点，单元格，块归一化 |
| hand-made (hand-designed) features, pipeline | 手工设计的特征，流水线 |
| Fisher vector, bag of visual words | 费舍尔向量，视觉词袋 |
| convolution, cross-correlation, kernel (filter) | 卷积，互相关，卷积核（滤波器） |
| feature map, channel | 特征图，通道 |
| weight sharing, locally connected | 权值共享，局部连接 |
| translation equivariance, translation invariance | 平移等变，平移不变 |
| circular padding, zero padding | 循环填充，零填充 |
| receptive field (of a unit), effective receptive field | （单元的）感受野，有效感受野 |
| stride, jump (spacing), pooling, max pooling | 步长，跳距，池化，最大池化 |
| anti-aliasing, blur pooling | 抗混叠，模糊池化 |
| the Neocognitron, S-cells, C-cells | 新认知机，S细胞，C细胞 |
| LeNet, MNIST | LeNet，MNIST |
| zip code, check reader | 邮政编码，支票识别系统 |
| time-delay neural network (TDNN) | 时延神经网络（TDNN） |
| ImageNet, ILSVRC, top-5 error | ImageNet，ILSVRC（ImageNet大规模视觉识别挑战赛），前五错误率 |
| WordNet, Amazon Mechanical Turk | WordNet，亚马逊土耳其机器人（众包平台） |
| AlexNet (SuperVision), CIFAR-10 | AlexNet（SuperVision），CIFAR-10 |
| rectified linear unit (ReLU), saturation | 修正线性单元（ReLU），饱和 |
| dropout | 随机失活（dropout） |
| data augmentation, random crop, flip | 数据增强，随机裁剪，翻转 |
| VGG, GoogLeNet, Inception module, 1 × 1 convolution | VGG，GoogLeNet，Inception模块，1 × 1卷积 |
| degradation problem | 退化问题 |
| batch normalization | 批归一化 |
| residual network (ResNet), highway network | 残差网络（ResNet），高速公路网络 |
| activation maximization, saliency map, feature visualization | 激活最大化，显著图，特征可视化 |
| adversarial example, perturbation, transferability | 对抗样本，扰动，可迁移性 |
| fast gradient sign method (FGSM), projected gradient descent (PGD) | 快速梯度符号法（FGSM），投影梯度下降（PGD） |
| adversarial training, robustness, certified defence | 对抗训练，鲁棒性，可认证防御 |
| depthwise convolution, pointwise convolution, depthwise separable | 深度卷积，逐点卷积，深度可分离 |
| MobileNet, ConvNeXt, vision transformer (ViT), Swin | MobileNet，ConvNeXt，视觉Transformer（ViT），Swin |
| dilated (atrous) convolution | 空洞卷积（膨胀卷积） |
| recurrent neural network (RNN), hidden state | 循环神经网络（RNN），隐状态 |
| backpropagation through time (BPTT), truncated BPTT | 随时间反向传播（BPTT），截断的BPTT |
| vanishing gradient, exploding gradient | 梯度消失，梯度爆炸 |
| Jacobian, spectral radius, largest singular value | 雅可比矩阵，谱半径，最大奇异值 |
| gradient clipping, cliff | 梯度裁剪，悬崖 |
| long short-term memory (LSTM), cell state, constant error carousel | 长短期记忆（LSTM），细胞状态，恒定误差传送带 |
| input gate, forget gate, output gate | 输入门，遗忘门，输出门 |
| gated recurrent unit (GRU), update gate, reset gate | 门控循环单元（GRU），更新门，重置门 |
| half-life (of a memory) | （记忆的）半衰期 |
| chrono initialization | 时序初始化 |
| character-level language model, char-rnn | 字符级语言模型，char-rnn |
| sequence to sequence (seq2seq), encoder, decoder | 序列到序列（seq2seq），编码器，解码器 |
| machine translation, phrase-based, BLEU | 机器翻译，基于短语的，BLEU |
| teacher forcing, exposure bias, scheduled sampling | 教师强制，暴露偏差，计划采样 |
| greedy decoding, beam search, beam width | 贪心解码，束搜索，束宽 |
| neural text degeneration | 神经文本退化 |
| bottleneck | 瓶颈 |
| attention, alignment, context vector, additive score | 注意力，对齐，上下文向量，加性打分 |
| query, key, value | 查询，键，值 |
| neural Turing machine, memory network | 神经图灵机，记忆网络 |
| linear recurrence, parallel prefix scan, associative | 线性递推，并行前缀扫描，结合律（可结合的） |
| minGRU, minLSTM, xLSTM, state-space model | minGRU，minLSTM，xLSTM，状态空间模型 |

Names: David Hubel → 大卫·休伯尔; Torsten Wiesel → 托斯滕·威泽尔; Kunihiko Fukushima → 福岛邦彦; Yann LeCun → 杨立昆;
Léon Bottou → 莱昂·博图; Patrick Haffner → 帕特里克·哈夫纳; Alex Waibel → 亚历克斯·魏贝尔; David Lowe → 大卫·罗; Fei-Fei Li →
李飞飞; Jia Deng → 邓嘉; Alex Krizhevsky → 亚历克斯·克里热夫斯基; Ilya Sutskever → 伊利亚·苏茨克维; Geoffrey Hinton → 杰弗里·
辛顿; Dan Cireșan → 丹·奇雷尚; Jürgen Schmidhuber → 于尔根·施密德胡伯; Karen Simonyan → 卡伦·西蒙尼扬; Andrew Zisserman →
安德鲁·齐瑟曼; Christian Szegedy → 克里斯蒂安·塞格迪; Kaiming He → 何恺明; Xiangyu Zhang → 张祥雨; Shaoqing Ren → 任少卿; Jian Sun
→ 孙剑; Ian Goodfellow → 伊恩·古德费洛; Aleksander Madry → 亚历山大·马德里; Andrew Howard → 安德鲁·霍华德; Zhuang Liu → 刘壮;
Michael Jordan → 迈克尔·乔丹; Jeffrey Elman → 杰弗里·埃尔曼; Paul Werbos → 保罗·韦尔博斯; Sepp Hochreiter → 塞普·霍赫赖特; Yoshua
Bengio → 约书亚·本吉奥; Razvan Pascanu → 拉兹万·帕斯卡努; Felix Gers → 费利克斯·格斯; Kyunghyun Cho → 赵京焕; Andrej Karpathy →
安德烈·卡帕西; Oriol Vinyals → 奥里奥尔·维尼亚尔斯; Dzmitry Bahdanau → 德米特里·巴赫达瑙; Guy Blelloch → 盖伊·布莱洛克.
Kept in Latin script (no established Chinese form found): Quoc Le, Junyoung Chung, Thang Luong, Hieu Pham, Kelvin Xu,
Leo Feng. Model names stay in Latin script: LeNet, AlexNet, VGG, GoogLeNet, ResNet, MobileNet,
ConvNeXt, ViT, Swin, WaveNet, GNMT, QRNN, SRU, S4, LRU, RWKV, Mamba, xLSTM, minGRU, minLSTM.
