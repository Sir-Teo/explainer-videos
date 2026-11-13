"""Act II, Learning from Data (Parts 6-10): classical and statistical ML, generalization, networks, CNNs and RNNs."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=6, level="U", widget="ridgelassopath", prereq=(1, 3, 4, 5),
        question="Given a page of a novel, how can a machine learn from examples who wrote it?",
        story="The part opens with a 1,000-word page and one task: Austen or Dickens? Each of 639 pages from five "
              "novels is described, as Mosteller and Wallace described the Federalist papers, by how often it uses "
              "the 70 commonest words, and 191 pages are held out. Every classical method is then written in numpy "
              "and run on the pages. Least squares is derived as a projection and shown best among linear unbiased "
              "estimators; ridge shrinks it along the weak singular directions and the lasso sets weights exactly "
              "to zero. Logistic regression gives probabilities, Newton's method solves it in 8 steps, and on the "
              "separable 70-rate pages its weights grow without end. Naive Bayes, Fisher's direction, nearest "
              "neighbours and the curse of dimensionality, kernels and the support vector machine, trees, bagging, "
              "random forests, AdaBoost and second-order gradient boosting follow, each derived and measured. The "
              "part turns to keeping score: ROC area, calibration, log loss and cross-validation. It ends with "
              "twelve procedures on the same ten folds, Breiman's two cultures, and why trees and now tabular "
              "foundation models win on tables.",
        handoff="Cross-entropy, gradients and curvature train every network of Parts 9 and 11, and the softmax is "
                "logistic regression with many classes. Part 7 takes the labels away; Part 8 asks why any of these "
                "fits generalizes and reuses the pages, the margins and the runaway logistic weights; attention is "
                "read as a kernel smoother in Part 13, and calibration returns for language models in Part 31.",
        outside="Calculus and matrix algebra; the projection and SVD of Part 3 and the Lagrange multipliers of Part 4.",
        objectives={
            "U": ["Fit a line by least squares and a classifier by logistic regression, and read the fitted "
                  "weights as a rule for telling two authors apart.",
                  "Explain how k nearest neighbours and a decision tree classify a page, and why accuracy on the "
                  "training pages overstates accuracy on new ones."],
            "M": ["Derive ridge's shrinkage factors through the SVD and the lasso's soft threshold from "
                  "subgradients.",
                  "Derive the logistic gradient and Hessian, and show that a Newton step is a weighted "
                  "least-squares fit.",
                  "Derive the bagging variance formula, AdaBoost's step size from the exponential loss, and "
                  "XGBoost's leaf weight and split gain."],
            "D": ["Prove the Gauss-Markov theorem and the representer theorem, and state what each assumes.",
                  "State Mercer's condition and decide whether a given kernel's Gram matrices can have negative "
                  "eigenvalues."],
            "I": ["Compare classifiers on the same cross-validation folds, reporting ROC area, log loss and "
                  "calibration as well as accuracy.",
                  "Choose a penalty, a depth or a number of rounds on training folds only, and say when a tree "
                  "ensemble is the right default for a table."],
        },
        results=[
            ("Normal equations", r"X^\top X\hat\beta=X^\top y,\qquad \hat y=X\hat\beta\ \perp\ y-\hat y"),
            ("Ridge through the SVD", r"\hat y_\lambda=\sum_j u_j\,\frac{d_j^2}{d_j^2+\lambda}\,u_j^\top y"),
            ("The soft threshold", r"w=\operatorname{sign}(z)\,\max(|z|-\lambda,\,0)"),
            ("Logistic gradient and Hessian", r"\nabla L=\tfrac1n X^\top(p-y),\qquad \nabla^2L=\tfrac1n X^\top SX\succeq 0"),
            ("Bagging B correlated trees", r"\operatorname{Var}\Bigl(\tfrac1B\sum_b T_b\Bigr)=\rho\sigma^2+\frac{1-\rho}{B}\,\sigma^2"),
            ("AdaBoost's step", r"\alpha=\tfrac12\log\frac{1-\varepsilon}{\varepsilon}"),
        ],
        U=(0, 1, 5, 9, 12), D=(10,), I=(16, 17),
    ),
    Part(
        n=7, level="U", widget="gplengthscale", prereq=(1, 3, 5, 6),
        question="With no labels at all, what hidden structure can a model find in data?",
        story="Part 6's pages come back uncoloured, and a two-component mixture fitted without labels recovers "
              "the two authors on 97% of them. The part builds models with parts that are never observed. "
              "Principal components are derived two ways, as the closest line and as the direction of greatest "
              "spread, then turned into a probability model; independent components unmix two microphones at a "
              "cocktail party. Mixtures are fitted by EM, whose lower bound is derived from Jensen's inequality "
              "and drawn under the real likelihood, and the same engine fits topic models, hidden Markov models "
              "(Baum-Welch) and IBM's Model 1 for translation. The part then counts as well as counting can: "
              "Kneser-Ney smoothing from Good-Turing, and an infinity-gram on a suffix array of all thirty novels, "
              "which adds a row to the scoreboard at 2.027 bits per character. It turns to graphs, d-separation "
              "and belief propagation, and to what a graph says about causes: Simpson's paradox and the back-door "
              "adjustment. It ends with the Bayesian toolkit: Gaussian processes, the evidence as Occam's razor, "
              "Bayesian optimization, and variational inference with the reparameterization trick.",
        handoff="Model 1's alignments return as attention in Part 13, hidden state through time as the state-space "
                "models of Part 15, and mixtures as the mixtures of experts of Part 16. The forward algorithm "
                "trains speech recognizers as CTC in Part 23, Gaussian processes are the infinite-width networks "
                "of Part 12, the ELBO and the reparameterization trick train the autoencoders and diffusion models "
                "of Parts 20 and 21, the do operator is causal tracing in Part 30, and Kneser-Ney is the row the "
                "neural language model of Part 9 has to beat.",
        outside="Calculus, matrix algebra and probability with Gaussians (Parts 3 and 5); Part 6's pages.",
        objectives={
            "U": ["Explain what a principal component is and compute the share of the spread it keeps.",
                  "Run the E step and the M step of a two-bell mixture by hand, and say what each one does.",
                  "Explain Simpson's paradox with a confounder, and why seeing is not doing."],
            "M": ["Derive PCA from a Lagrange multiplier and EM's lower bound from Jensen's inequality, and "
                  "prove that EM never lowers the likelihood.",
                  "Implement the forward and Viterbi recursions of a hidden Markov model and state their cost.",
                  "Derive a Gaussian process's posterior mean and variance by conditioning a joint Gaussian."],
            "D": ["Derive the ELBO identity, run coordinate-ascent variational inference on a conjugate model, "
                  "and explain why the mean-field answer is too narrow.",
                  "Split the log evidence of a Gaussian process into data fit and complexity penalty, and "
                  "explain how it selects a model without held-out data."],
            "I": ["Build an n-gram model with Kneser-Ney smoothing and report its bits per character on "
                  "held-out text.",
                  "Tune a hyperparameter by Bayesian optimization with expected improvement, and compare the "
                  "evaluations spent with a grid."],
        },
        results=[
            ("PCA", r"Cu_j=\lambda_ju_j,\qquad \text{error with }k\text{ directions}=\sum_{j>k}\lambda_j"),
            ("EM's bound", r"\log p(x;\theta)=\mathcal B(q,\theta)+\operatorname{KL}\bigl(q\,\|\,p(z\mid x;\theta)\bigr)"),
            ("The forward algorithm", r"\alpha_t(j)=b_j(x_t)\sum_i\alpha_{t-1}(i)\,a_{ij}"),
            ("Good-Turing", r"r^*=(r+1)\,\frac{N_{r+1}}{N_r},\qquad p(\text{unseen})=\frac{N_1}{N}"),
            ("Back-door adjustment", r"P(y\mid do(x))=\sum_z P(y\mid x,z)\,P(z)"),
            ("Gaussian process posterior", r"\mu_*=k_*^\top(K+\sigma^2I)^{-1}y,\quad "
                                           r"\sigma_*^2=k_{**}-k_*^\top(K+\sigma^2I)^{-1}k_*"),
        ],
        U=(0, 1, 4, 6, 12), D=(14, 16), I=(8, 10, 15),
    ),
    Part(
        n=8, level="U", widget="descentpeak", prereq=(5, 6, 7),
        question="A model is fitted to examples, so why should it work on anything else?",
        story="The part opens on the gap: Part 6's nearest-neighbour vote scores 93% on its own training pages and "
              "68% on new ones. Risk, empirical risk and the Bayes risk are defined, and bias and variance are "
              "derived and measured over polynomial degrees. The classical guarantees are then built one step at a "
              "time: Hoeffding for one rule, the union bound for many, shattering, the Sauer-Shelah lemma and the VC "
              "bound, Rademacher complexity and margins. Computed on the 448 training pages, most of them say "
              "little or nothing; a PAC-Bayes bound optimized for a 9,217-weight network gives 35.6%, non-vacuous, "
              "against 2.8% measured. The part turns when a 300,034-weight network fits shuffled authors "
              "completely: the classical story cannot explain why the same network generalizes on true labels. "
              "The explanations since follow: gradient descent's implicit bias toward the minimum-norm and the "
              "max-margin fit, double descent with its peak at p = n, benign overfitting, and the unsettled debate "
              "over flat minima. It ends where generalizing stops being enough: covariate shift with importance "
              "weights, and passages a language model reproduces word for word once it has seen them often enough.",
        handoff="Margins return in Part 9 in the perceptron's convergence proof. Which minimum training finds, "
                "sharpness and the edge of stability are the subject of Part 11; models far bigger than their data, "
                "grokking and scaling laws belong to Part 12; held-out scores, contaminated test sets, memorization "
                "and privacy come back in Parts 30 and 31.",
        outside="Probability with expectations and tail bounds (Part 5), least squares and the SVD (Parts 3 and 6).",
        objectives={
            "U": ["Explain the difference between training error and risk, and why the best of many rules looks "
                  "better on its training examples than it is.",
                  "Split a model's expected squared error into bias, variance and noise, and read the U-shaped "
                  "curve.",
                  "Describe the random-label experiment and the double-descent curve, and say what each one "
                  "contradicts."],
            "M": ["Derive the union bound for a finite family and the VC bound through the growth function and "
                  "the Sauer-Shelah lemma.",
                  "Compute the Rademacher complexity of norm-bounded linear rules, and state the margin bound.",
                  "Prove that gradient descent from zero reaches the minimum-norm interpolant, and explain the "
                  "peak at p = n through the smallest singular value."],
            "D": ["Prove the PAC-Bayes theorem by a change of measure, and optimize the bound over a Gaussian "
                  "posterior for a small network.",
                  "State the effective-rank conditions for benign overfitting, and explain why a rescaling of "
                  "the weights defeats sharpness as a measure of generalization."],
            "I": ["Correct a covariate shift by importance weighting, with weights from a domain classifier, "
                  "and report the effective sample size.",
                  "Test a language model for extractable training passages, and explain how repetition in the "
                  "training data and deduplication change the result."],
        },
        results=[
            ("Bias and variance", r"\mathbb E\,(y-\hat f(x))^2=\text{bias}^2+\text{variance}+\sigma^2"),
            ("Many rules: the union bound", r"P\Bigl(\max_{h\in\mathcal H}\bigl|\hat R(h)-R(h)\bigr|\ge\varepsilon\Bigr)"
                                            r"\le 2\,|\mathcal H|\,e^{-2n\varepsilon^2}"),
            ("Sauer-Shelah", r"\Pi_{\mathcal H}(n)\le\sum_{i=0}^{d}\binom ni\le\Bigl(\frac{en}{d}\Bigr)^d"),
            ("PAC-Bayes", r"R(Q)\le\hat R(Q)+\sqrt{\frac{\operatorname{KL}(Q\,\|\,P)+\ln(2\sqrt n/\delta)}{2n}}"),
            ("The minimum-norm fit", r"w_\infty=X^{+}y,\qquad \hat\beta=\sum_i\frac{u_i^\top t}{\sigma_i}\,v_i"),
            ("Importance weighting", r"R_q(h)=\mathbb E_{x\sim p}\bigl[w(x)\,\ell(h,x)\bigr],\qquad w=\frac qp"),
        ],
        U=(0, 1, 2, 3, 9, 12), D=(7, 14, 15), I=(16, 17),
    ),
    Part(
        n=9, level="U", widget="signaldepth", prereq=(4, 6, 8),
        question="How did a threshold unit of 1943 become the block inside today's language models?",
        story="The part opens with a strip from 1943 to 2012, two winters shaded, and a small ReLU network bending "
              "its linear pieces around two spirals. McCulloch and Pitts's threshold units compute any logical "
              "formula; Rosenblatt's perceptron learns from mistakes, and Novikoff's theorem bounds how many it can "
              "make. Then XOR: no line separates it, Minsky and Papert's book appears, and the first winter "
              "follows. A hidden layer solves XOR, and backpropagation, derived as the delta equations and checked "
              "three ways, trains it. One layer of hinges can approximate any curve, Barron's rate escapes the "
              "curse of dimensionality, and depth folds the plane into exponentially many pieces. The part turns "
              "on why deep networks would not train: gradients vanish through 50 sigmoid layers. The fixes are "
              "derived and measured: initialization that keeps the variance, the edge of chaos, the residual "
              "stream, normalization. It ends by assembling the modern block with its gated MLP, weighing "
              "Kolmogorov-Arnold networks, and training Bengio's neural language model to 2.38 bits per character, "
              "1.99 when mixed with Kneser-Ney.",
        handoff="Weight sharing over space and time gives the convolutional and recurrent networks of Part 10. How "
                "to scale weights and learning rates as networks grow is the subject of Parts 11 and 12. The "
                "residual stream is the backbone of the transformer in Part 13 and what Part 30 reads inside "
                "models; the gated MLP, multiplied, becomes the experts of Part 16; learned embeddings of "
                "characters become embeddings of tokens, images and sounds.",
        outside="The chain rule and Part 4's autodiff; variances of sums of independent terms (Part 5).",
        objectives={
            "U": ["Run the perceptron rule by hand, and show with four inequalities that no single unit computes "
                  "XOR.",
                  "Explain how a hidden layer makes XOR separable, and how hinges add up to any curve.",
                  "Tell the history from 1943 to 2012: what each winter was about and what ended it."],
            "M": ["Prove Novikoff's bound, and derive the delta equations of backpropagation.",
                  "Derive the LeCun, Glorot and He initializations from the variance of one layer, and predict "
                  "how a signal grows or shrinks through depth when the scale is wrong.",
                  "Derive the Jacobians of a residual block and of RMSNorm, and explain what each does to the "
                  "gradient."],
            "D": ["Reproduce Maurey's argument for the 1/sqrt(n) rate of random units, and state Barron's "
                  "theorem with its lower bound for fixed bases.",
                  "Compute the mean-field length and correlation maps, locate the edge of chaos, and relate the "
                  "depth scale to trainability.",
                  "State the Kolmogorov-Arnold theorem and assess the evidence for and against KANs."],
            "I": ["Count the weights of a transformer block from a published configuration, including the "
                  "8d/3 width of a SwiGLU MLP.",
                  "Choose an initialization, a normalization placement and an activation for a deep network, "
                  "and diagnose a stalled run from its per-layer gradients."],
        },
        results=[
            ("Novikoff's bound", r"\text{mistakes}\ \le\ \Bigl(\frac{R}{\gamma}\Bigr)^2"),
            ("Backpropagation", r"\delta^l=(W^{l+1})^\top\delta^{l+1}\odot\varphi'(z^l),\qquad "
                                r"\frac{\partial L}{\partial W^l}=\delta^l\,(a^{l-1})^\top"),
            ("Depth folds", r"\text{the tent map composed }k\text{ times: }2^k\text{ pieces from }2k\text{ units}"),
            ("Initialization", r"\operatorname{Var}(z)=n_{\text{in}}\operatorname{Var}(W)\,\mathbb E[a^2]"
                               r"\ \Rightarrow\ \operatorname{Var}(W)=\tfrac{2}{n}\ \text{for ReLU}"),
            ("The residual Jacobian", r"\frac{\partial h_L}{\partial h_0}=(I+J_L)\cdots(I+J_1):\ 2^L\text{ paths}"),
            ("RMSNorm's Jacobian", r"\frac{\sqrt d}{\|h\|}\,\bigl(I-\hat h\hat h^\top\bigr)"),
        ],
        U=(0, 1, 2, 3, 5, 8), D=(6, 10, 14), I=(13, 15),
        also=(("The series' autodiff", "explainer/ai/autodiff.py"),),
    ),
    Part(
        n=10, level="U", widget="receptivecone", prereq=(6, 7, 9),
        question="How did machines learn to see an image and to remember a sentence?",
        story="The part opens in the late 1950s with Hubel and Wiesel's cat, a cortical cell that fires for an edge "
              "at one angle, and then shows the first-layer filters of a network trained here on CIFAR-10 and "
              "counts those that pick out one orientation. Vision before deep learning was designed features (Sobel, SIFT, HOG) "
              "under a learned linear classifier. Convolution replaces them: shared weights, translation "
              "equivariance proved, receptive fields computed layer by layer. LeNet reads digits, ImageNet supplies "
              "the data, and AlexNet wins in 2012 with ReLUs, dropout and GPUs; VGG, Inception and ResNet go "
              "deeper. The part looks at what the filters learn and how a perturbation of one step along the sign "
              "of the gradient fools them. It then turns from space to time: a recurrent network's gradient is a "
              "product of Jacobians that vanishes or explodes, the LSTM's cell carries it on a path with "
              "derivative diag(f), and a character LSTM takes a row on the scoreboard. It ends with "
              "sequence-to-sequence translation, the attention Bahdanau, Cho and Bengio added in 2014, and the "
              "linear recurrences and parallel scans of today's recurrent models.",
        handoff="Bahdanau's attention becomes the whole of the Transformer in Parts 13 and 14. The linear "
                "recurrences and their scans are Part 15's memory; clipping and the optimizers that train deep "
                "networks are Part 11; images cut into patches and convolutions inside the new models are Part 22; "
                "equivariance for rotations, molecules and graphs is Part 25; adversarial attacks return, on "
                "language models, in Part 31.",
        outside="Part 9's backpropagation, initialization and residual connections; sums over a sliding window.",
        objectives={
            "U": ["Compute a convolution of a small image with a 3 x 3 kernel by hand, and count the weights "
                  "that sharing saves against a fully connected layer.",
                  "Tell the story from LeNet to AlexNet to ResNet: what changed in 2012, and which ingredients "
                  "were already known.",
                  "Explain what the cell and the gates of an LSTM do, in words and on a drawing."],
            "M": ["Prove that convolution commutes with translation, and compute a stack's receptive field "
                  "from its kernels and strides.",
                  "Derive the product of Jacobians in backpropagation through time and its bound, and the "
                  "half-life of an LSTM's cell path.",
                  "Write one step of an encoder-decoder with additive attention: scores, softmax, context "
                  "vector."],
            "D": ["Derive the fast gradient sign method from the linearity argument, and compare FGSM, PGD and "
                  "adversarial training under one threat model.",
                  "Show that a linear recurrence is an associative scan, and state what minGRU and xLSTM give "
                  "up and gain against attention."],
            "I": ["Compute the cost ratio of a depthwise separable convolution, and explain why measured "
                  "speed-ups differ from the FLOP ratio.",
                  "Decode from a sequence model greedily and with a beam, and recognise exposure bias and "
                  "degenerate repetition in the output."],
        },
        results=[
            ("Translation equivariance", r"w\star(T_sx)=T_s(w\star x),\qquad (T_sx)[i]=x[i-s]"),
            ("Receptive field", r"r_\ell=r_{\ell-1}+(k_\ell-1)\,j_{\ell-1},\qquad j_\ell=j_{\ell-1}\,s_\ell"),
            ("Fast gradient sign method", r"\eta=\varepsilon\,\operatorname{sign}\bigl(\nabla_xJ(\theta,x,y)\bigr)"),
            ("Gradients through time", r"\Bigl\|\frac{\partial h_T}{\partial h_k}\Bigr\|\le\sigma_{\max}(W)^{T-k}"),
            ("The LSTM cell", r"c_t=f_t\odot c_{t-1}+i_t\odot g_t,\qquad h_t=o_t\odot\tanh(c_t)"),
            ("Additive attention", r"\alpha_{ij}=\frac{\exp e_{ij}}{\sum_k\exp e_{ik}},\qquad c_i=\sum_j\alpha_{ij}h_j"),
        ],
        U=(0, 1, 2, 4, 5, 13), D=(9, 16), I=(10, 14),
        also=(("The series' autodiff", "explainer/ai/autodiff.py"),),
    ),
]
