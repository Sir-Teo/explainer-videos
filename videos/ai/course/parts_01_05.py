"""Foundations (Parts 1-5): information, the symbolic era, linear algebra, calculus and probability."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=1, level="U", widget="huffmanblocks",
        question="How many bits does a text really hold, and what does guessing the next letter have to do with it?",
        story="The part opens with Shannon's 1951 experiment: hide a sentence, have someone guess it letter by "
              "letter, and write down how many guesses each letter took. From letter counts in thirty novels it "
              "builds probability and the chain rule, shows that Shannon's requirements leave only log2(1/p) as a "
              "measure of surprise, and defines entropy as the average surprise: 4.08 bits for single letters, 3.33 "
              "given the previous one. Codes come next: Kraft's inequality on the binary tree, Huffman's code and "
              "why it is optimal, typical sequences and the source coding theorem. The part turns when the code is "
              "built from the wrong model: the price is the KL divergence, and an arithmetic coder turns any "
              "predictor into a compressor that wastes at most two bits on the whole text. Learning by counting, "
              "Laplace's rule and the softmax gradient show how a model is fitted, and mutual information measures "
              "what the past tells the future. It ends on the scoreboard, bits per character on one passage, where "
              "gzip, a counting model, GPT-2 and Qwen3 are ranked by the same number.",
        handoff="Cross-entropy is the loss minimized for the rest of the series, and its gradient q - y is derived "
                "again by backpropagation in Part 4. Sampling text from a model returns in Part 5, the two "
                "directions of the KL divergence in Parts 20 and 27, and the scoreboard gains rows in Part 7 and "
                "closes the series in Part 31.",
        outside="Logarithms, sums and a little programming. No probability is assumed.",
        objectives={
            "U": ["Compute the surprise of an outcome and the entropy of a distribution in bits, and say what "
                  "each measures.",
                  "Build a Huffman code for a small alphabet and decode a message with it.",
                  "Explain why a model that predicts the next letter better compresses the text further."],
            "M": ["Prove Kraft's inequality on the binary tree and derive L >= H from it with Jensen's inequality.",
                  "Derive H(p, q) = H(p) + KL(p || q) and Gibbs' inequality, and tell forward from reverse KL by "
                  "what each fit covers.",
                  "Derive the gradient of the softmax cross-entropy with respect to the logits."],
            "D": ["State the asymptotic equipartition property, bound the size of the typical set, and prove the "
                  "source coding theorem from it.",
                  "Prove the data-processing inequality from the chain rule for mutual information, and say what "
                  "an estimate of mutual information at long distances does and does not establish."],
            "I": ["Convert between bits per token, bits per character, bits per byte and perplexity, and compare "
                  "two models only in a unit that does not depend on the tokenizer.",
                  "Run an arithmetic coder with integer registers, and account for a compressed size that must "
                  "include the model."],
        },
        results=[
            ("Entropy", r"H(p)=\sum_x p(x)\log_2\frac{1}{p(x)}\ \le\ \log_2 K"),
            ("Kraft-McMillan, and the best code", r"\sum_i 2^{-\ell_i}\le 1,\qquad H(p)\ \le\ L_{\text{Huffman}}\ <\ H(p)+1"),
            ("Cross-entropy", r"H(p,q)=\sum_x p(x)\log_2\frac{1}{q(x)}=H(p)+D_{\mathrm{KL}}(p\,\|\,q),\qquad "
                              r"D_{\mathrm{KL}}(p\,\|\,q)\ge 0"),
            ("Arithmetic coding", r"\ell(x_1\dots x_n)\ <\ \log_2\frac{1}{q(x_1\dots x_n)}+2,\qquad "
                                  r"q(x_1\dots x_n)=\prod_{i=1}^n q(x_i\mid x_{<i})"),
            ("The softmax gradient", r"q_k=\frac{e^{z_k}}{\sum_j e^{z_j}},\qquad "
                                     r"\frac{\partial(-\ln q_y)}{\partial z_k}=q_k-[k=y]"),
            ("Mutual information", r"I(X;Y)=H(X)-H(X\mid Y)=D_{\mathrm{KL}}\bigl(p(x,y)\,\|\,p(x)p(y)\bigr)\ \ge 0"),
        ],
        U=(0, 1, 2, 3, 9, 10, 13), D=(6, 12), I=(8, 14, 15),
        also=(("The arithmetic coder", "videos/ai/ai1/coder.py"),),
    ),
    Part(
        n=2, level="U", widget="astarweight",
        question="How far can a machine get by searching and by following rules someone wrote down?",
        story="In 1958 Simon and Newell forecast a computer chess champion within ten years; Deep Blue beat Kasparov "
              "in May 1997. The part walks through what was built in between. Turing's "
              "machine fixes what can be computed, and the halting problem what cannot. Search comes first: the "
              "8-puzzle's 181,440 states mapped by breadth-first search, Dijkstra's wavefront, and A*, whose "
              "heuristic turns the circle of expanded cells into an ellipse and stays optimal as long as it never "
              "overestimates. Hill climbing and simulated annealing give up the guarantee for reach; minimax and "
              "alpha-beta play games, and Samuel's checkers program learns its own scoring. Logic follows: "
              "resolution, DPLL and CDCL, and the random 3-SAT transition near 4.27 clauses per variable, then "
              "constraints, STRIPS planning and expert systems. The part turns with ELIZA and the two AI winters: "
              "hand-written rules could not cover the long tail of perception and language. It ends with what "
              "survives inside AlphaZero, SAT and SMT solvers, and proof assistants.",
        handoff="Learned weights replace hand-written rules in Part 9. Search guided by a learned evaluation is "
                "AlphaZero in Part 26, which also solves Connect Four; search over chains of thought returns in "
                "Part 28, planning and tools in Part 29, and proof and verification in Part 31.",
        outside="Some programming (loops, recursion, a queue). Nothing from Part 1 is needed.",
        objectives={
            "U": ["Trace breadth-first search, uniform-cost search and A* on a small graph, and say which of them "
                  "return a shortest path.",
                  "Run minimax and alpha-beta by hand on a small game tree and mark the branches that are pruned.",
                  "Explain the ELIZA effect and what caused each of the two AI winters."],
            "M": ["Prove that A* with an admissible heuristic returns an optimal path, and that a consistent "
                  "heuristic makes f non-decreasing along every path.",
                  "Derive alpha-beta's best case, and derive the Boltzmann distribution from the Metropolis rule "
                  "by detailed balance.",
                  "Refute a set of clauses by resolution, and run DPLL with unit propagation on a small formula."],
            "D": ["Prove the halting problem undecidable by diagonalization.",
                  "State what is proved and what is only predicted about the random 3-SAT threshold, and explain "
                  "how conflict-driven clause learning differs from chronological backtracking."],
            "I": ["Choose between exact search, weighted A* and local search for a problem from its size and from "
                  "how much a suboptimal answer costs.",
                  "Encode a small verification question (two circuits are equivalent) as a satisfiability problem "
                  "and read the solver's answer."],
        },
        results=[
            ("A*", r"f(n)=g(n)+h(n);\qquad h(n)\le h^*(n)\ \text{for all } n\ \Longrightarrow\ \text{the path "
                   r"returned is optimal}"),
            ("Consistency", r"h(n)\le c(n,n')+h(n')\ \Longrightarrow\ f\ \text{never decreases along a path}"),
            ("The Metropolis rule", r"P(\text{accept})=\min\bigl(1,\,e^{-\Delta E/T}\bigr)\ \Longrightarrow\ "
                                    r"\pi(x)\propto e^{-E(x)/T}"),
            ("Alpha-beta, best case", r"b^{\lceil d/2\rceil}+b^{\lfloor d/2\rfloor}-1\ \text{ leaves, against }"
                                      r"b^{d}\text{ for minimax}"),
            ("Resolution", r"\frac{A\vee\ell\qquad B\vee\neg\ell}{A\vee B},\qquad KB\models\alpha\iff "
                           r"KB\wedge\neg\alpha\ \vdash\ \square"),
            ("The halting problem", r"\text{No Turing machine decides, for every machine } M\text{ and input } w"
                                    r"\text{, whether } M\text{ halts on } w"),
        ],
        U=(0, 1, 2, 3, 6, 12, 13), D=(9,), I=(11, 14),
        also=(("Part 26: Connect Four solved, and AlphaZero", "videos/ai/ai26/README.md"),),
    ),
    Part(
        n=3, level="U", widget="lowrankcopy", prereq=(1,),
        question="How can a list of numbers stand for the meaning of a word?",
        story="Part 1's counting model could not tell 'the dog barked' from 'the hound barked', so this part gives "
              "words a place in a space. It opens on 102 words where GPT-2 puts them and builds the linear algebra "
              "needed to read that picture: the dot product and Cauchy-Schwarz, einsum, matrices as maps, "
              "projection and least squares, eigenvectors and the spectral theorem, and power iteration run live. "
              "The centre is the singular value decomposition, every matrix as turn, stretch, turn, and the "
              "Eckart-Young theorem: the best rank-k copy keeps the top k singular values. Norms and the condition "
              "number measure a matrix; random matrices give the Marchenko-Pastur bulk that training's outliers "
              "escape, and gradients turn out to be low rank. Word vectors then come from counting (PPMI and a "
              "truncated SVD), and word2vec is shown to factor the same shifted table. The part turns to high "
              "dimensions, where random directions are nearly perpendicular and Johnson-Lindenstrauss is proved, "
              "and ends with GPT-2's lopsided embedding space and low rank in recommendation and retrieval.",
        handoff="Part 4 builds the chain rule that computes every gradient. Part 9 keeps each layer's stretch near "
                "one, Part 11 builds Muon as steepest descent in the spectral norm, Part 13 writes attention in "
                "einsum, Part 15 squeezes memory through low rank, Part 27 fine-tunes through it (LoRA), and "
                "Part 30 reads and steers the directions inside a model.",
        outside="School algebra and coordinates in the plane. The letter tables of Part 1 are reused.",
        objectives={
            "U": ["Compute a dot product and a cosine similarity, and say what each tells about two word vectors.",
                  "Describe what a matrix does to the plane from its columns, and what its singular values "
                  "measure.",
                  "Explain why two random directions in 768 dimensions are almost always nearly perpendicular."],
            "M": ["Derive the projection onto a column space and the SVD from the spectral theorem applied to "
                  "the Gram matrix.",
                  "Prove the Eckart-Young theorem from Weyl's inequality, and derive power iteration's "
                  "convergence rate.",
                  "Derive the shifted-PMI target that skip-gram with negative sampling factorizes."],
            "D": ["Prove the Johnson-Lindenstrauss lemma by a Gaussian projection, a chi-squared Chernoff bound "
                  "and a union bound, and state the matching lower bound.",
                  "Compare a trained layer's spectrum with the Marchenko-Pastur law, and say what a fitted "
                  "power-law tail does and does not show."],
            "I": ["Write a contraction in einsum and count its cost, and pick the cheaper order of a matrix "
                  "chain.",
                  "Fit a matrix factorization to ratings with a penalty, and report held-out error against "
                  "baselines fitted on the same data."],
        },
        results=[
            ("The dot product", r"\mathbf a\cdot\mathbf b=|\mathbf a|\,|\mathbf b|\cos\theta,\qquad "
                                r"|\mathbf a\cdot\mathbf b|\le|\mathbf a|\,|\mathbf b|"),
            ("Projection", r"P=A(A^\top A)^{-1}A^\top,\qquad P^2=P=P^\top"),
            ("Singular values", r"A=U\Sigma V^\top,\qquad \|A\|_2=\sigma_1,\qquad \|A\|_F^2=\sum_i\sigma_i^2"),
            ("Eckart-Young", r"\min_{\operatorname{rank}B\le k}\|A-B\|_F^2=\sum_{i>k}\sigma_i^2,\qquad "
                             r"\text{attained by } A_k=\sum_{i\le k}\sigma_i\,\mathbf u_i\mathbf v_i^\top"),
            ("Power iteration", r"\mathbf x_{t+1}=\frac{A\mathbf x_t}{|A\mathbf x_t|}:\qquad \text{the error "
                                r"shrinks by } |\lambda_2/\lambda_1| \text{ per step}"),
            ("High dimensions", r"\operatorname{Var}(\cos\theta)=\frac1d;\qquad k\ge\frac{4\ln n}"
                                r"{\varepsilon^2/2-\varepsilon^3/3}\ \text{dimensions keep } n\text{ points' "
                                r"squared distances within } 1\pm\varepsilon"),
        ],
        U=(0, 1, 3, 4, 7, 12, 14), D=(10, 15, 16), I=(11, 17),
    ),
    Part(
        n=4, level="U", widget="quadraticdescent", prereq=(1, 3),
        question="How does a model with billions of parameters find out which way to change each one?",
        story="Full training of a model like Qwen3-4B needs four billion derivatives at every step, and Part 1 took "
              "its gradient on trust. This part builds the calculus. The derivative is the best linear "
              "approximation, the gradient points along steepest ascent by Cauchy-Schwarz, and the Jacobian is the "
              "local linear map, with the chain rule as a product of Jacobians. Real layers are differentiated "
              "(the matrix product, the softmax, layer normalization), and forward and reverse mode are counted: "
              "for one loss and many parameters, backwards wins by a factor of the parameter count. "
              "Backpropagation is done by hand and then written as the series' own autodiff library, checked "
              "against finite differences, and used to train Part 1's letter model. The part turns to what a "
              "computer does to the mathematics: floating point, cancellation, the gradient check's V-curve, and "
              "memory traded for recomputation. It ends with curvature (Newton's method, Hessian-vector products, "
              "descent on a quadratic and saddles), constraints (Lagrange multipliers, KKT and duality) and "
              "differentiating through a fixed point.",
        handoff="The library trains the series' first neural networks in Part 9; Jacobians multiplied through "
                "depth return in Parts 9 and 10, curvature and optimizers in Part 11, duality as the support "
                "vector machine in Part 6, the KL-regularized closed form as direct preference optimization in "
                "Part 27, and number formats and memory in Parts 17 to 19.",
        outside="Derivatives of one variable help but are rebuilt in chapter 1; matrices as in Part 3.",
        objectives={
            "U": ["Explain a derivative as the slope of the best line, and a gradient as the direction of "
                  "steepest ascent.",
                  "Backpropagate by hand through a small network with one hidden layer, and check the result "
                  "with a finite difference.",
                  "Train a small model by gradient descent and read its loss curve."],
            "M": ["Derive the Jacobian of the softmax and the vector-Jacobian products of a matrix product.",
                  "Implement reverse-mode autodiff on a graph in topological order, and count forward against "
                  "reverse mode for a given network.",
                  "Derive the stable step sizes and the rate (kappa - 1)/(kappa + 1) of gradient descent on a "
                  "quadratic, and compute a Hessian-vector product without the Hessian."],
            "D": ["State the KKT conditions and the assumptions under which strong duality holds, and derive "
                  "the dual of the hard-margin SVM.",
                  "Derive the implicit derivative of a fixed point, and state when it exists and when the "
                  "iteration that finds the fixed point converges."],
            "I": ["Choose the step of a gradient check from the precision in use, and recognise cancellation "
                  "and overflow in a loss.",
                  "Trade activation memory against recomputation with checkpoints, and say what the count "
                  "leaves out."],
        },
        results=[
            ("The derivative", r"f(x+h)=f(x)+f'(x)\,h+o(h)"),
            ("The chain rule", r"J_{f\circ g}(x)=J_f\bigl(g(x)\bigr)\,J_g(x),\qquad \bar x=J_g(x)^\top\,\bar y"
                               r"\ \ \text{(one backward step)}"),
            ("The softmax Jacobian", r"\frac{\partial p}{\partial z}=\operatorname{diag}(p)-p\,p^\top"),
            ("A layer's gradient", r"y=Wx,\quad \delta=\frac{\partial L}{\partial y}\ \Longrightarrow\ "
                                   r"\frac{\partial L}{\partial W}=\delta\,x^\top,\qquad "
                                   r"\frac{\partial L}{\partial x}=W^\top\delta"),
            ("Descent on a quadratic", r"x_{t+1}=(I-\eta H)\,x_t\ \text{converges}\iff 0<\eta<\frac{2}"
                                       r"{\lambda_{\max}};\qquad \min_\eta\max_i|1-\eta\lambda_i|="
                                       r"\frac{\kappa-1}{\kappa+1}"),
            ("A fixed point's derivative", r"z^*=f(z^*,\theta)\ \Longrightarrow\ \frac{\partial z^*}"
                                           r"{\partial\theta}=\Bigl(I-\frac{\partial f}{\partial z}\Bigr)^{-1}"
                                           r"\frac{\partial f}{\partial\theta}"),
        ],
        U=(0, 1, 2, 6, 8), D=(16, 17), I=(9, 10, 11),
        also=(("The series' autodiff library", "explainer/ai/autodiff.py"),),
    ),
    Part(
        n=5, level="U", widget="nucleuscut", prereq=(1, 3, 4),
        question="What does it mean for a model to hand us a distribution, and how do we draw from it?",
        story="Six hundred random dots flow into the letters 'AI': a diffusion model in miniature, and the place "
              "the part is heading. It starts with the bell curve, from Bernoulli's law of large numbers and a "
              "Galton board to the central limit theorem as repeated convolution, then Gaussians in many "
              "dimensions and conditioning. Fitting follows: maximum likelihood and its bias, Fisher information "
              "and the Cramer-Rao bound, Bayes's rule with a Gaussian prior as weight decay, and maximum entropy, "
              "which yields the softmax. Markov, Chebyshev, Chernoff and Hoeffding bound how far an average "
              "strays. The part turns from describing distributions to drawing from them: inverse-CDF, rejection, "
              "Box-Muller and the Gumbel-max trick, then temperature, top-k, top-p and min-p on GPT-2's next-word "
              "distribution. Markov chains, Monte Carlo, score-function gradients, Metropolis-Hastings and "
              "Langevin dynamics sample what cannot be sampled directly. It ends in continuous time: Brownian "
              "motion, Ito's lemma, stochastic differential equations and the Fokker-Planck equation, with the "
              "reverse-time SDE that ran the opening.",
        handoff="Maximum likelihood and Fisher information return in Parts 6 and 11; Bayes, Markov chains and "
                "their samplers in Part 7; the concentration inequalities as generalization bounds in Part 8; "
                "decoding in Part 19; score-function gradients and importance weights in Parts 26 and 27; and "
                "SDEs as noisy training in Part 11 and as generation in Parts 20 and 21.",
        outside="Integrals of one variable; the entropy of Part 1, the matrices of Part 3 and the gradients and "
                "Lagrange multipliers of Part 4.",
        objectives={
            "U": ["Explain why sums of many small independent effects look like a bell curve, and fit a mean "
                  "and a spread by maximum likelihood.",
                  "Update a belief with Bayes's rule, and say how a prior acts as regularization.",
                  "Describe what temperature, top-k and top-p each do to a next-token distribution."],
            "M": ["Derive the conditional of a multivariate Gaussian, the Cramer-Rao bound, and the "
                  "maximum-entropy distribution under a mean constraint.",
                  "Derive Hoeffding's inequality from Markov's, and the Gumbel-max trick.",
                  "Derive Metropolis-Hastings from detailed balance, and the score-function gradient with a "
                  "baseline."],
            "D": ["Derive Ito's lemma from the quadratic variation of Brownian motion, and the Fokker-Planck "
                  "equation from Ito's lemma by integration by parts.",
                  "Bound a reversible chain's mixing time by its spectral gap, and state the strong and weak "
                  "orders of the Euler-Maruyama scheme."],
            "I": ["Choose and report a decoding rule, measuring surprise, diversity and repetition rather than "
                  "likelihood alone.",
                  "Diagnose an importance-sampling or score-function estimate by its effective sample size and "
                  "variance, and reduce the variance with a baseline or reparameterization."],
        },
        results=[
            ("Conditioning a Gaussian", r"x_1\mid x_2\sim\mathcal N\bigl(\mu_1+\Sigma_{12}\Sigma_{22}^{-1}"
                                        r"(x_2-\mu_2),\ \Sigma_{11}-\Sigma_{12}\Sigma_{22}^{-1}\Sigma_{21}\bigr)"),
            ("Cramer-Rao", r"\operatorname{Var}(\hat\theta)\ \ge\ \frac{1}{n\,I(\theta)}\ \text{ for unbiased }"
                           r"\hat\theta,\qquad I(\theta)=\mathbb E\bigl[(\partial_\theta\log p_\theta(x))^2\bigr]"),
            ("Hoeffding", r"P\bigl(\bar X_n-\mathbb E\bar X_n\ge\varepsilon\bigr)\le e^{-2n\varepsilon^2}"
                          r"\qquad\text{for independent } X_i\in[0,1]"),
            ("Temperature and the Gumbel-max trick", r"p_T(k)=\frac{e^{z_k/T}}{\sum_j e^{z_j/T}},\qquad "
                                                     r"\arg\max_k\,(z_k+G_k)\sim\operatorname{softmax}(z)"
                                                     r"\ \text{ for i.i.d. Gumbel } G_k"),
            ("The score-function gradient", r"\nabla_\theta\,\mathbb E_{p_\theta}[f(x)]=\mathbb E_{p_\theta}"
                                            r"\bigl[(f(x)-b)\,\nabla_\theta\log p_\theta(x)\bigr]"),
            ("Fokker-Planck", r"dx=f\,dt+g\,dW\ \Longrightarrow\ \frac{\partial p}{\partial t}="
                              r"-\frac{\partial(f\,p)}{\partial x}+\tfrac12\frac{\partial^2(g^2p)}{\partial x^2}"),
        ],
        U=(0, 1, 3, 5, 8, 11, 14), D=(15, 17), I=(9, 12),
    ),
]
