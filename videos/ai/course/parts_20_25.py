"""Act IV, Generation and Perception (Parts 20-25): generative families, diffusion, images and video, tokens, self-supervision, symmetry."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=20, level="M", widget="ganspiral", prereq=(1, 5, 7, 9),
        question="How can a machine learn a distribution well enough to draw new samples from it?",
        story="The part opens with digits nobody wrote, sampled from four of its own models, and sets the test "
              "bench: three densities in the plane (two moons, a ring of eight Gaussians, a checkerboard) and MNIST "
              "at 14 x 14 pixels with 16 grey levels. Maximum likelihood is minimum KL, and each family is one way "
              "to make it tractable. A PixelCNN factors the image by the chain rule, with an exact likelihood and "
              "196 sequential passes per sample. A VAE bounds the likelihood by the ELBO, and the part makes "
              "posterior collapse happen with an autoregressive decoder. A GAN replaces likelihood by a game: the "
              "optimal discriminator turns the value into a Jensen-Shannon divergence, the ring collapses to a few "
              "modes, and simultaneous gradient steps on min max xy spiral out by exactly sqrt(1 + eta^2) per "
              "step. Wasserstein critics, coupling flows with a triangular Jacobian, neural ODEs with a trace, and "
              "the energy models of Hopfield and Boltzmann up to Langevin sampling with the score follow. The part "
              "turns to judging: FID is derived as a Fréchet distance and shown to miss what precision and recall "
              "catch. It ends with five models on one budget of 6 x 10^12 training FLOPs, and with the families "
              "meeting again inside tokenizers and fast samplers.",
        handoff="The score, learned at every noise level, becomes diffusion in Part 21, where flow matching trains "
                "continuous flows by regression. Autoencoders and their tokens are the front end of the image, "
                "video and audio models of Parts 22 and 23, and next-scale prediction returns in Part 22. The "
                "contrastive idea drives the self-supervised learning of Part 24, and judging a model returns in "
                "Part 31.",
        outside="Multivariable calculus (Jacobians, determinants) and probability densities; entropy and KL from "
                "Part 1 and Markov chain Monte Carlo from Part 5.",
        objectives={
            "U": ["Explain what it means to sample from, evaluate and encode with a generative model, and name "
                  "what each of the five families gives up.",
                  "Write an image's probability by the chain rule and say why sampling it takes one pass per pixel."],
            "M": ["Derive the ELBO and its gap, the optimal discriminator and the Jensen-Shannon form of the GAN "
                  "value.",
                  "Compute a coupling layer's log-determinant and its inverse, and derive the instantaneous change "
                  "of variables for a continuous flow.",
                  "Derive the RBM's conditionals and free energy, and write a Langevin step from a score."],
            "D": ["State Kantorovich-Rubinstein duality, derive the WGAN objective from it, and explain why "
                  "Jensen-Shannon is flat at log 2 for disjoint supports.",
                  "Analyse simultaneous, alternating, extragradient and optimistic steps on a bilinear game through "
                  "the eigenvalues of their update matrices."],
            "I": ["Report a generator with FID, precision and recall together, stating the feature network, the "
                  "sample size and the reference set.",
                  "Diagnose mode collapse and posterior collapse from training curves, and choose a remedy "
                  "(gradient penalty, free bits) knowing its cost per step."],
        },
        results=[
            ("The ELBO's gap", r"\log p(x)-\operatorname{ELBO}=\operatorname{KL}\bigl(q(z\mid x)\,\|\,p(z\mid x)\bigr)"),
            ("The optimal discriminator", r"D^*=\frac{p}{p+q},\qquad V(D^*,G)=-\log 4+2\operatorname{JS}(p\,\|\,q)"),
            ("Simultaneous steps on xy", r"|\lambda|=|1\pm i\eta|=\sqrt{1+\eta^2}>1"),
            ("A coupling layer", r"y_b=x_b\odot e^{s(x_a)}+t(x_a),\qquad \log|\det J|=\sum_i s_i(x_a)"),
            ("A continuous flow", r"\frac{d\log p(z(t))}{dt}=-\operatorname{tr}\frac{\partial f}{\partial z}"),
            ("Fréchet distance in 1D", r"W_2^2=(\mu_1-\mu_2)^2+(\sigma_1-\sigma_2)^2"),
        ],
        U=(0, 1, 2, 5, 11), D=(7, 10, 16), I=(8, 14, 15),
    ),
    Part(
        n=21, level="M", widget="ddimsteps", prereq=(1, 5, 13, 20),
        question="How does a model turn pure noise into data, and how few steps can it take?",
        story="The part opens with a denoiser trained on the computer walking 300 points from noise into the letters "
              "'AI'. The data are those letters made into a mixture of 400 small Gaussians, so the score, the best "
              "denoiser and the flow's velocity are known exactly and every learned thing is measured against the "
              "truth. The forward process destroys data slowly and has a closed form; the variational bound turns "
              "into weighted errors of a noise guess, Tweedie's formula says the best guess is the score, and "
              "Vincent's theorem says plain regression learns it. Time is then run backwards with Anderson's "
              "reverse SDE or the probability-flow ODE, and DDPM, DDIM, EDM's Heun steps and DPM-Solver are compared "
              "by evaluations spent. The part turns from following a curved path in many steps to straightening "
              "it: flow matching regresses on straight-line velocities, reflow straightens the pairs, and "
              "distillation, consistency models and MeanFlow reach one step. Guidance turns a request into a push "
              "on the score. It ends with noise replaced by blanks: masked diffusion's bound is a weighted "
              "cross-entropy, and a masked-diffusion language model of the series' own is put on the scoreboard "
              "beside an autoregressive model of the same size.",
        handoff="The machinery meets real images and video in Part 22, in compressed latent spaces with "
                "transformers as the denoisers. Speech and sound generators use it in Part 23, denoising as a way "
                "to learn features returns in Part 24, diffusion builds molecules and protein structures in Part "
                "25, and world models imagine the next frame with it in Part 29.",
        outside="Multivariable calculus and Gaussian algebra; the Ornstein-Uhlenbeck process and Fokker-Planck "
                "equation of Part 5, and Langevin sampling from Part 20.",
        objectives={
            "U": ["Describe the forward process and compute how much signal and noise are left after t steps.",
                  "Explain in words why learning to guess the noise is enough to walk from noise back to data, and "
                  "what the guidance weight w does to a sample."],
            "M": ["Derive the forward closed form, Tweedie's formula, and the equality of denoising and explicit "
                  "score matching up to a constant.",
                  "Derive DDIM's step and show it is Euler's method in (x/alpha, sigma/alpha).",
                  "Derive flow matching's marginal velocity and classifier-free guidance's tilted density."],
            "D": ["Prove the marginal-field theorem of flow matching and relate its straight paths to the "
                  "Benamou-Brenier optimum.",
                  "Derive masked diffusion's bound as a weighted cross-entropy and as an any-order autoregressive "
                  "loss, and state what the bound does and does not say about likelihood."],
            "I": ["Choose a sampler, a step spacing and a noise schedule for a budget of network evaluations, and "
                  "measure the result against a many-step reference.",
                  "Distil a many-step sampler to a few steps, and report what guidance costs in recall for what "
                  "it gains in precision."],
        },
        results=[
            ("The forward process", r"q(x_t\mid x_0)=\mathcal N\bigl(\sqrt{\bar\alpha_t}\,x_0,\ (1-\bar\alpha_t)I\bigr)"),
            ("Tweedie's formula", r"\mathbb{E}[x_0\mid x]=\frac{x+\sigma^2\nabla\log p(x)}{\alpha},\qquad "
                                  r"\mathbb{E}[\varepsilon\mid x]=-\sigma\nabla\log p(x)"),
            ("Denoising score matching", r"J_{\text{DSM}}(\theta)=J_{\text{ESM}}(\theta)+C,\qquad C\text{ free of }\theta"),
            ("Probability-flow ODE", r"\frac{dx}{d\sigma}=\frac{x-D(x,\sigma)}{\sigma}"),
            ("Flow matching", r"x_\tau=(1-\tau)z+\tau x_1,\qquad v(x,\tau)=\mathbb{E}[x_1-z\mid x_\tau=x]"),
            ("Guidance", r"\nabla\log p(x)+w\,\nabla\log p(y\mid x)=\nabla\log\bigl[p(x)\,p(y\mid x)^w\bigr]"),
        ],
        U=(0, 1, 14, 15), D=(10, 13, 16), I=(7, 9, 12, 17),
        also=(("The exact test bench", "videos/ai/ai21/exact.py"),),
    ),
    Part(
        n=22, level="M", widget="noiseshift", prereq=(10, 13, 20, 21),
        question="How do a transformer and a denoiser, built for sequences and points, make pictures, video and 3D scenes?",
        story="The part opens with a word drawn letter by letter by a diffusion transformer trained on one CPU core, "
              "on 20 x 20 capital letters from 24 system fonts. A picture is cut into patches and read as a "
              "sequence: a small ViT learns the grid from its position vectors, and is set against a CNN of about "
              "the same size on 3, 7 and 20 training fonts to measure what a convolution's built-in locality is "
              "worth. Generation moves into a "
              "smaller space: eight autoencoders show the reconstruction-generation dilemma, and REPA borrows a "
              "frozen encoder's eyes. The denoiser becomes a transformer told what to draw through adaLN-Zero "
              "gates that start at zero, and Stable Diffusion 3's resolution shift is derived from equal "
              "uncertainty about a flat picture and checked at 20, 40 and 80 pixels. The part turns from noise to "
              "tokens: raster order, MaskGIT's cosine schedule and VAR's coarse-to-fine scales, then one "
              "transformer that names, draws and edits. Video is the same in time: a bouncing letter drawn as a "
              "whole clip, by teacher forcing and by diffusion forcing, rolled out to four times the training "
              "length. It ends in 3D, with NeRF's volume-rendering integral and its quadrature, and with Gaussian "
              "splatting's projected covariance.",
        handoff="The image encoders, and the CLIP and SigLIP models that tie pictures to words, are Part 23. The "
                "self-supervised encoders whose eyes REPA borrows are Part 24. Diffusion over 3D structure returns "
                "in AlphaFold 3 in Part 25, video that responds to a player's actions is a world model in Part 29, "
                "and telling real pictures from generated ones is part of Part 31.",
        outside="Linear algebra (covariances, Jacobians) and a first-order ODE; convolutions from Part 10, the "
                "transformer of Part 13 and Part 21's flow matching and guidance.",
        objectives={
            "U": ["Count a vision transformer's tokens for a given picture and patch size, and say how attention's "
                  "cost grows when the patch halves.",
                  "Explain what an inductive bias is and why a convolutional network may need fewer examples "
                  "than a vision transformer."],
            "M": ["Write out an adaLN-Zero block and show that it is the identity when its gates are zero.",
                  "Derive the resolution shift from equal uncertainty about a flat picture, and the drop of "
                  "2 log alpha in log signal-to-noise ratio.",
                  "Derive the volume-rendering integral and its alpha-compositing quadrature."],
            "D": ["Derive the projected covariance of a 3D Gaussian by linearizing the projection, and say when "
                  "the linearization fails.",
                  "Compare how representation alignment, representation autoencoders and unified models share "
                  "one network between understanding and generation, and state what is still open."],
            "I": ["Choose a latent size knowing the reconstruction-generation dilemma, and budget a model by "
                  "tokens and multiply-adds.",
                  "Diagnose exposure bias in an autoregressive video rollout and name the training change that "
                  "reduces it."],
        },
        results=[
            ("Patches as tokens", r"N=\frac{HW}{p^2},\qquad \text{attention}\propto N^2d,\quad \text{MLPs}\propto Nd^2"),
            ("adaLN-Zero", r"h\leftarrow h+\alpha(c)\odot F\bigl((1+\gamma(c))\odot\operatorname{LN}(h)+\beta(c)\bigr)"),
            ("The resolution shift", r"\sigma_m=\frac{\alpha\,\sigma_n}{1+(\alpha-1)\,\sigma_n},\qquad \alpha=\sqrt{m/n}"),
            ("Volume rendering", r"C=\int T\,\sigma\,\mathbf c\,dt,\qquad T(t)=\exp\Bigl(-\int_0^t\sigma\,ds\Bigr)"),
            ("Its quadrature", r"C\approx\sum_i T_i\,\alpha_i\,\mathbf c_i,\qquad \alpha_i=1-e^{-\sigma_i\delta_i}"),
            ("A splatted Gaussian", r"\Sigma=RSS^\top R^\top,\qquad \Sigma'=JW\,\Sigma\,W^\top J^\top"),
        ],
        U=(0, 1, 2, 7), D=(4, 11, 16), I=(5, 8, 12, 14),
    ),
    Part(
        n=23, level="U", widget="aliasfold", prereq=(1, 7, 13, 20),
        question="How do text, sound and pictures all become tokens that one transformer can read?",
        story="The part opens with a sentence, a picture and a voice turned into one stream of tokens, and with four "
              "histories on one time axis: listening from Audrey in 1952 to Whisper, speaking from the Voder of "
              "1939 to Qwen3-TTS, text from Shannon's letters to byte-pair encoding, and pictures from captioning "
              "to CLIP. Text comes first: BPE is a greedy compressor in which a merge found n times saves n "
              "symbols, Kudo's unigram model puts a probability on every cut, and bits per character let "
              "tokenizers be compared on the novels. Bytes and entropy patches remove the tokenizer. Pictures and "
              "sound need learned codes: a VQ codebook trained with the straight-through estimator can leave "
              "codes dead, which restarts and FSQ's fixed grid address in different ways. For sound, aliasing is derived and measured on "
              "tones sampled at 8 kHz, and a residual codec of the series' own codes speech spectrograms at 400 to "
              "3,200 bits a second. The part turns to recognition: CTC sums over every alignment with the forward "
              "recursion of Part 7, and a small CTC recognizer is set against Whisper. It ends with CLIP's "
              "contrastive loss as a bound on mutual information, the connectors of vision-language models, and "
              "omni models that listen and speak at once.",
        handoff="The self-supervised speech and image encoders that semantic tokens and vision-language models are "
                "built on are Part 24. Reasoning models think in tokens in Part 28, robots and world models write "
                "actions and video frames as tokens in Part 29, and what the tokens come to mean inside a model is "
                "Part 30. Tokenizer quirks in benchmarks and cloned voices return in Part 31.",
        outside="Logarithms, sines and cosines; bits and cross-entropy from Part 1 and the forward algorithm of "
                "Part 7.",
        objectives={
            "U": ["Run byte-pair encoding by hand on a short phrase and count the symbols each merge saves.",
                  "Compute where a tone above the Nyquist frequency appears after sampling, and convert bits per "
                  "token to bits per character."],
            "M": ["Compute a word's probability under a unigram tokenizer with the forward algorithm, and its "
                  "best cut with Viterbi.",
                  "Write the VQ-VAE losses with the straight-through estimator, and count the codes and bits of an "
                  "FSQ grid and of residual stages.",
                  "Derive CTC's forward recursion on the 2L + 1 extended states and say why a repeated letter "
                  "needs a blank."],
            "D": ["Derive InfoNCE's optimal critic and the bound log N - L <= I(X; Y), and explain why a batch "
                  "of N cannot certify more than log N.",
                  "Compare CLIP's softmax loss with SigLIP's sigmoid loss as estimators, and state how each "
                  "depends on the batch size."],
            "I": ["Choose a vocabulary size and tokenizer for a corpus, and compare models with different "
                  "tokenizers in bits per character on the same text.",
                  "Budget a speech or vision front end in tokens per second, bits per second and word error rate."],
        },
        results=[
            ("A merge saves what it finds", r"L_k=L_0-\sum_{i\le k}n_i"),
            ("The unigram tokenizer", r"P(x)=\sum_{\text{cuts of }x}\ \prod_{\text{pieces}}p(\text{piece})"),
            ("Bits per character", r"\frac{\text{bits}}{\text{character}}=\frac{\text{bits per token}}{\text{characters per token}}"),
            ("Aliasing", r"\cos\Bigl(2\pi(f+kf_s)\tfrac{n}{f_s}\Bigr)=\cos\Bigl(2\pi f\tfrac{n}{f_s}\Bigr)"),
            ("CTC", r"p(\mathbf y\mid\mathbf x)=\sum_{\pi:\ \mathcal B(\pi)=\mathbf y}\ \prod_{t=1}^{T}y_t(\pi_t)"),
            ("InfoNCE's bound", r"\log N-\mathcal L\ \le\ I(X;Y)"),
        ],
        U=(0, 1, 2, 5, 8, 10), D=(14,), I=(9, 12, 13, 15, 16),
        also=(("The series' byte-level BPE", "explainer/ai/novels.py"),),
    ),
    Part(
        n=24, level="M", widget="temperaturepush", prereq=(1, 3, 10, 23),
        question="How can a network learn what matters in data that nobody labelled?",
        story="The part opens with six hundred test digits placed on a sphere by a network that never saw a label, "
              "and beside it the collapsed alternative, every digit at one point. One bench is fixed: MNIST, the "
              "same three-layer convolutional encoder and 800 updates for every method, judged by a linear probe, "
              "k nearest neighbours and a probe from ten labels per digit. Pretext puzzles come first, with "
              "rotation prediction and its blind spots. Contrastive learning follows: InfoNCE is an N-way "
              "classification whose value bounds the mutual information and never exceeds log N, SimCLR pulls two "
              "views of one digit together, and on the sphere its loss splits into alignment and uniformity. The "
              "part turns on collapse: a network trained only to make two views agree sends everything to one "
              "point, and its effective rank shows it. Four ways out are trained and broken in turn: negatives, "
              "the asymmetry of BYOL and SimSiam's stop-gradient, the decorrelation of Barlow Twins and VICReg, "
              "and DINO's centring and sharpening. Masked autoencoders and JEPA predict what is hidden, in pixels "
              "or in meaning. It ends with every method on one budget, embeddings for search, and CKA's answer to "
              "whether different networks come to see the same world.",
        handoff="Augmentations teach a network what to ignore; Part 25 builds that symmetry into the network "
                "itself. Prediction in representation space is the heart of the world models in Part 29, probes "
                "and CKA are how Part 30 reads what a network knows, teachers and students return in Part 27's "
                "distillation, and embeddings are the memory that the agents of Part 29 search.",
        outside="Linear algebra (singular values, the Frobenius norm) and the softmax; mutual information from "
                "Part 1 and the contrastive loss of Part 23.",
        objectives={
            "U": ["Explain what a pretext task is and how a frozen representation is judged by a linear probe and "
                  "by nearest neighbours.",
                  "Describe collapse, and say why agreement between two views alone does not prevent it."],
            "M": ["Write the NT-Xent loss, compute its value at a collapsed encoder, and say what the temperature "
                  "does to the push on near and far negatives.",
                  "Compute the effective rank of an embedding from its singular values.",
                  "Explain how the stop-gradient, the variance term and centring with sharpening each block a "
                  "collapse, and what happens when each is removed."],
            "D": ["Derive InfoNCE's optimal critic and its bound, and the alignment-uniformity limit of the "
                  "contrastive loss as N grows.",
                  "Prove linear CKA's invariance to rotation and scaling, and state the platonic representation "
                  "hypothesis with the caveats the part's own checks raise."],
            "I": ["Choose between a frozen probe, few-label probe and fine-tuning to evaluate an encoder, and "
                  "monitor training without labels with the effective rank.",
                  "Build a retrieval index on embeddings and shorten them with Matryoshka training, knowing what "
                  "accuracy each length keeps."],
        },
        results=[
            ("InfoNCE's bound", r"I(X;Y)\ \ge\ \log N-L_N,\qquad \log N-L_N\le\log N"),
            ("NT-Xent", r"\ell_i=-\log\frac{e^{\cos(z_i,z_{i'})/\tau}}{\sum_{k\ne i}e^{\cos(z_i,z_k)/\tau}}"),
            ("Alignment and uniformity", r"\ell-\log N\ \to\ \frac{\|z-z^+\|^2}{2\tau}-\frac1\tau+\log\mathbb{E}_{z^-}e^{z\cdot z^-/\tau}"),
            ("What collapse costs", r"\ell_{\text{NT-Xent}}=\log(2N-1),\qquad \ell_{\text{SimSiam}}=-1"),
            ("Effective rank", r"\operatorname{erank}(Z)=\exp\Bigl(-\sum_k p_k\log p_k\Bigr),\quad p_k=\frac{\sigma_k}{\sum_j\sigma_j}"),
            ("Linear CKA", r"\frac{\|\tilde Y^\top\tilde X\|_F^2}{\|\tilde X^\top\tilde X\|_F\,\|\tilde Y^\top\tilde Y\|_F}"),
        ],
        U=(0, 1, 2, 6), D=(5, 12, 15), I=(10, 13, 14),
    ),
    Part(
        n=25, level="M", widget="oversmooth", prereq=(10, 13, 21, 24),
        question="What does a network gain by knowing the symmetries of its problem, and what did that do for science?",
        story="The part opens with five charged particles turned through a full circle while three trained networks "
              "predict their energy: a plain MLP's answer swings, the MLP trained on turned copies swings less, "
              "and a network built on distances does not move. Invariance and equivariance are defined, group "
              "averaging is derived with its price, and the recipe is stated: find what does not matter and build "
              "it in. Sets come first, with the Deep Sets theorem, then graphs, where message passing is "
              "permutation equivariant, can see no more than Weisfeiler and Leman's colour refinement, and "
              "over-smooths with depth at a rate set by the second eigenvalue of the averaging matrix. Networks "
              "that turn with the molecule follow: the gradient of an invariant energy is an equivariant force, "
              "and EGNN's equivariance is proved line by line. The part then turns from method to science. "
              "Protein folding runs from Anfinsen, Levinthal and CASP to AlphaFold 2's Evoformer, frames and "
              "FAPE, AlphaFold 3's diffusion over atoms without built-in equivariance, and protein design. "
              "Weather on a mesh, neural operators and materials by the million follow. It ends with mathematics: "
              "AlphaGeometry, proofs checked in Lean, and discovery by search with an exact evaluator.",
        handoff="Search guided by a network and judged by an exact checker is AlphaZero in Part 26 and the "
                "reasoning models of Part 28. A learned simulator that rolls the world forward, like the mesh "
                "network, is Part 29's world model; whether a network's layers respect the symmetries expected of "
                "them is Part 30's subject; CASP's blind tests and a nearly saturated olympiad lead to Part 31.",
        outside="Linear algebra (orthogonal matrices, eigenvalues of a symmetric matrix) and the idea of a group; "
                "convolution's equivariance from Part 10 and diffusion from Part 21.",
        objectives={
            "U": ["Tell an invariant function from an equivariant one, and name the symmetry of a set, a graph "
                  "and a molecule.",
                  "Explain why protein folding was hard, what CASP measured, and what changed in 2020."],
            "M": ["Write a Deep Sets network and one round of message passing, and check their permutation "
                  "symmetry.",
                  "Run colour refinement on two small graphs and decide whether message passing can tell them "
                  "apart.",
                  "Derive over-smoothing from the spectrum of the normalized adjacency matrix, and show that an "
                  "invariant energy has an equivariant force."],
            "D": ["Prove that a message-passing network is at most as discriminating as 1-WL, and that an EGNN "
                  "layer is E(n)-equivariant, reflections included.",
                  "Weigh built-in equivariance against augmentation in the light of AlphaFold 3's diffusion "
                  "module, and state what remains open."],
            "I": ["Check a trained model's symmetry numerically by turning, shifting and reordering its inputs, "
                  "and report the error against its test error.",
                  "Read the published claims of a scientific system (hit rates, blind tests, experimental "
                  "confirmation) and say which rest on an exact checker."],
        },
        results=[
            ("Invariance and equivariance", r"f(g\cdot x)=f(x),\qquad f(g\cdot x)=g\cdot f(x)"),
            ("Group averaging", r"\bar f(x)=\frac{1}{|G|}\sum_{g\in G}g^{-1}f(g\cdot x)"),
            ("Deep Sets", r"f(X)=\rho\Bigl(\sum_{x\in X}\phi(x)\Bigr)"),
            ("Graphs", r"f(PX,\,PAP^\top)=P\,f(X,A),\qquad \text{MPNN}\le\text{1-WL}"),
            ("Over-smoothing", r"\bigl\|\hat A^kH-u_1u_1^\top H\bigr\|\le|\lambda_2|^k\,\|H\|,\qquad u_1\propto\sqrt{\deg}"),
            ("An equivariant force", r"E(Rx+t)=E(x)\ \Longrightarrow\ F(Rx+t)=R\,F(x)"),
        ],
        U=(0, 1, 2, 8), D=(5, 7, 16, 17), I=(12, 13, 15),
    ),
]
