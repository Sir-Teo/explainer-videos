"""The end of Act II and the start of the Transformer era: optimizers, scale, attention, the lineage, memory (Parts 11-15)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=11, level="U", widget="valleyrace", prereq=(4, 6, 9),
        question="Every model here learns by walking downhill on its loss, so why does it matter so much how you walk?",
        story="The part opens with four walkers in Rosenbrock's valley, gradient descent, the heavy ball, Adam and Lion, "
              "each at its best step size, and asks why they finish so far apart. Cauchy's gradient descent of 1847 is "
              "derived with its rate, which pays for the condition number; Polyak's heavy ball and Nesterov's method "
              "pay for its square root, and the measured contractions sit on the derived ones. Small batches make "
              "each step cheap and noisy, and the noise acts like a temperature set by the step size over the batch "
              "size; full-batch training on the spirals climbs to the edge of stability, where the sharpness hovers "
              "at 2 over the step. The part turns from one step size for all weights to geometry: Adam and its sign "
              "limit, weight decay that is not L2, the natural gradient and K-FAC, Shampoo and SOAP, and Muon, "
              "steepest descent under the spectral norm, computed by Newton-Schulz polynomials. Six optimizers then "
              "race on the character model with equal tuning, the same data order and three seeds. It ends with "
              "schedules and the river valley, schedule-free training, and what keeps very large runs from blowing "
              "up: QK-clip, gradient clipping and weight decay's equilibrium.",
        handoff="The critical batch is measured and the learning rate carried across width and depth in Part 12; the "
                "transformers of Parts 13 and 14 train with AdamW and a warmup; Part 18 trains with the full recipe, "
                "Muon included, and keeps it stable at scale; Parts 26 and 27 run reinforcement learning and "
                "fine-tuning on the same optimizers.",
        outside="Multivariable calculus (gradients, a second-order Taylor expansion), eigenvalues and the singular "
                "value decomposition.",
        objectives={
            "U": ["Explain why a step larger than 2 / L diverges on a bowl of curvature L, and what the condition "
                  "number does to gradient descent.",
                  "Describe what momentum, a random batch and Adam's per-weight step sizes each change about a "
                  "gradient step."],
            "M": ["Derive the descent lemma and the linear rate of gradient descent, and the heavy ball's tuned "
                  "momentum from the roots of its recurrence.",
                  "Derive Adam's bias correction and its sign-descent limit, and show that decoupled weight decay "
                  "and L2 differ under Adam.",
                  "Derive Muon's step as steepest descent under the spectral norm, and one Newton-Schulz round as "
                  "a polynomial on every singular value."],
            "D": ["State the stochastic differential equation that models SGD, the stationary covariance it "
                  "predicts, and the assumptions under which the step size over the batch size acts as a "
                  "temperature.",
                  "Derive the natural gradient as steepest descent under the Fisher metric, show its invariance "
                  "to reparametrization, and state what K-FAC and Shampoo approximate."],
            "I": ["Run a fair optimizer comparison: tune each baseline over a grid, match budgets and data order, "
                  "use several seeds and report the spread.",
                  "Choose a schedule (warmup, cosine, warmup-stable-decay or schedule-free) and diagnose a loss "
                  "spike with gradient clipping, QK-clip or weight decay."],
        },
        results=[
            ("Gradient descent's rate", r"f(x_k)-f^*\le\bigl(1-\tfrac{1}{\kappa}\bigr)^{k}\,(f(x_0)-f^*),"
                                        r"\quad \eta=\tfrac1L,\ \kappa=\tfrac{L}{\mu}"),
            ("The tuned heavy ball", r"\sqrt{\beta}=\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}"
                                     r"\quad\text{is the contraction per step}"),
            ("SGD as a diffusion", r"d\theta=-\nabla L\,dt+\sqrt{\eta/B}\;\Sigma^{1/2}\,dW"),
            ("Adam", r"\Delta\theta=-\eta\,\frac{\hat m}{\sqrt{\hat v}+\epsilon},\quad "
                     r"\hat m=\frac{m_t}{1-\beta_1^{\,t}},\ \hat v=\frac{v_t}{1-\beta_2^{\,t}}"),
            ("Muon's step", r"G=U\Sigma V^\top\ \Longrightarrow\ \Delta W=-\eta\,UV^\top"),
            ("One Newton-Schulz round", r"X\leftarrow aX+bXX^\top X+c\,(XX^\top)^2X:\quad "
                                        r"\sigma\mapsto a\sigma+b\sigma^3+c\sigma^5"),
        ],
        U=(0, 1, 3, 6), D=(4, 8, 16), I=(12, 13, 15),
        also=(("The series' autodiff", "explainer/ai/autodiff.py"),),
    ),
    Part(
        n=12, level="M", widget="isoflopvalley", prereq=(6, 9, 11),
        question="Why do bigger models get better so predictably, and how should a budget be split between "
                 "parameters and data?",
        story="The part opens with a fan of runs of Part 11's character model, eleven sizes at up to nine lengths, "
              "whose lower edge is a floor plus a straight line on log axes. It first asks what happens as a network "
              "grows infinitely wide: its output becomes a Gaussian process, and with neural-tangent step sizes it "
              "trains like a fixed kernel and learns no features. muP is derived from one observation, that random "
              "sums grow like the square root of the width and aligned updates like the width, and a coordinate "
              "check and learning-rate sweeps show one rate serving every width. The critical batch is derived and "
              "measured. Then the scaling laws: power laws fitted to the sweep, Chinchilla's formula, and the "
              "compute-optimal split found with a Lagrange multiplier under C = 6ND. The part turns to what bends "
              "the laws (Kaplan's parameter counting, over-training for inference, repeated data, experts, low "
              "precision) and to why they are power laws at all. It ends with emergence against all-or-nothing "
              "metrics, grokking and its Fourier circuit, scaling the answer with many tries, and the argument over "
              "whether pretraining has stalled.",
        handoff="Part 14 tells the story of GPT-3, Gopher and Chinchilla model by model; experts return in Part 16; "
                "Part 18 trains with the whole recipe (muP, batch sizes, schedules, eight-bit arithmetic) and does "
                "the FLOP accounting of a real run; the cost of answering is Part 19; Parts 27 and 28 scale "
                "reinforcement learning and thinking; grokking's circuit is a first taste of Part 30, and "
                "forecasting what models will do is Part 31.",
        outside="Multivariable calculus with Lagrange multipliers, the central limit theorem and the law of large "
                "numbers, fitting a line on log axes.",
        objectives={
            "U": ["Read a scaling-law plot: name the floor and the slope, and say what a straight line on log axes "
                  "does and does not promise beyond the measured range.",
                  "Explain with p to the power L why an all-or-nothing score can jump while the per-token score "
                  "rises smoothly."],
            "M": ["Derive muP's learning-rate rule from how random sums and aligned updates grow with width, and "
                  "run a coordinate check.",
                  "Derive the compute-optimal split of C = 6ND for a loss E + A/N^alpha + B/D^beta with a "
                  "Lagrange multiplier.",
                  "Derive the steps-against-examples hyperbola of the critical batch from a second-order model of "
                  "one step."],
            "D": ["Define the neural tangent kernel, show that gradient flow at infinite width is kernel "
                  "regression, and state what the lazy regime cannot learn.",
                  "Derive a power-law exponent from the data manifold's dimension and from the quanta model, and "
                  "state where each derivation stops matching the measurements."],
            "I": ["Transfer a learning rate tuned on a narrow, shallow model to a wide, deep one, and say what "
                  "copying the rate costs without muP.",
                  "Size a model for its lifetime: trade training compute against inference with 6ND + 2NT, and "
                  "decide when to raise the batch, repeat data, add experts or quantize."],
        },
        results=[
            ("Gradient flow at infinite width", r"\dot f=-\Theta\,(f-y),\quad "
                                                r"\Theta(x,x')=\nabla_\theta f(x)\cdot\nabla_\theta f(x')"),
            ("muP's rule", r"\text{random sum}\sim\sqrt n,\ \ \text{aligned update}\sim n\ \Longrightarrow\ "
                           r"\eta_{\text{hidden}}\propto\tfrac1n"),
            ("The critical batch", r"\Bigl(\frac{S}{S_{\min}}-1\Bigr)\Bigl(\frac{E}{E_{\min}}-1\Bigr)=1"),
            ("Chinchilla's law", r"L(N,D)=E+\frac{A}{N^{\alpha}}+\frac{B}{D^{\beta}},\qquad C\approx 6ND"),
            ("The compute-optimal split", r"N^*\propto C^{\,\beta/(\alpha+\beta)},\qquad "
                                          r"D^*\propto C^{\,\alpha/(\alpha+\beta)}"),
            ("All-or-nothing scores", r"P(\text{all }L\text{ tokens right})=p^{L}"),
        ],
        U=(0, 7, 9, 14), D=(1, 13, 17), I=(4, 6, 10, 12),
        also=(("The series' autodiff", "explainer/ai/autodiff.py"),),
    ),
    Part(
        n=13, level="U", widget="querycompass", prereq=(3, 9, 10),
        question="What does a transformer compute when every character looks back at the ones before it?",
        story="The part opens on the series' own transformer reading a sentence, with an arc from each character to "
              "the earlier ones it weighs. Attention is first a weighted average: the Nadaraya-Watson smoother of "
              "1964 on counts of 'her' in Great Expectations, with the distance score replaced by a learned affinity "
              "between a query and a key. It is also a memory read: one update of a modern Hopfield network is the "
              "same softmax formula, and its inverse temperature slides from an average of everything to the recall "
              "of one pattern. The division by the square root of d is derived from a variance, heads are shown to "
              "be low-rank maps, the causal mask decides who sees whom, and a four-block transformer is trained on "
              "the thirty novels and costed at 12 d squared weights a block. The part turns to position: sinusoids, "
              "ALiBi, no positions at all, and rotations whose scores depend only on the offset, trained side by "
              "side and stretched past their training length. It ends with what goes wrong and what heads learn: "
              "sinks, runaway scores and QK-norm, induction heads, one gradient step written as attention, and the "
              "limits of a fixed depth.",
        handoff="The block built here is stacked and scaled in Part 14; its keys and values become the cache of "
                "Part 15; attending to only some of the past is Part 16; long contexts and runaway logits return "
                "in Part 18 and fast serving in Part 19; thinking past a fixed depth is Part 28, and circuits in "
                "real models are Part 30.",
        outside="Dot products, matrix rank and rotations in the plane; the variance of a sum of independent terms; "
                "the softmax.",
        objectives={
            "U": ["Compute one head's output by hand: scores, softmax weights and the weighted average of the "
                  "values, and say what the causal mask removes.",
                  "Explain why the scores are divided by the square root of d, and why attention without "
                  "positions cannot tell 'dog bites man' from 'man bites dog'."],
            "M": ["Derive Var(q . k) = d for independent unit-variance entries, and the softmax Jacobian that "
                  "makes a saturated head hard to train.",
                  "Prove that rotary positions make the score depend on positions only through the offset n - m, "
                  "for fixed queries and keys.",
                  "Count a block's parameters and matrix operations, and find the context length at which "
                  "attention's work equals the weights'."],
            "D": ["Show that one gradient step on in-context least squares is a linear attention layer, and state "
                  "what agreement between a trained layer and that step does and does not establish.",
                  "State the circuit-complexity bound on fixed-depth transformers with its precision assumptions, "
                  "and the RASP-L conjecture on length generalization."],
            "I": ["Choose among sinusoidal, rotary, ALiBi and no positions, and extend a rotary model's context "
                  "with position interpolation or YaRN and a short fine-tune.",
                  "Diagnose attention sinks and growing scores, and apply a sink logit, an output gate, QK-norm or "
                  "a soft cap."],
        },
        results=[
            ("Attention", r"\operatorname{Attn}(q)=\sum_j p_j v_j,\qquad "
                          r"p=\operatorname{softmax}_j\Bigl(\frac{q\cdot k_j}{\sqrt d}\Bigr)"),
            ("Why the square root of d", r"\operatorname{Var}(q\cdot k)=d\,\sigma_q^2\sigma_k^2"),
            ("A Hopfield read", r"\xi^{\text{new}}=X^\top\operatorname{softmax}(\beta X\xi)"),
            ("Rotary positions", r"(R_mq)^\top(R_nk)=q^\top R_{n-m}\,k"),
            ("What a block costs", r"12d^2+9d\ \text{weights};\qquad 2LTd=24Ld^2\iff T=12d"),
            ("A gradient step as attention", r"\hat y=\frac{\eta}{N}\sum_{i=1}^{N}y_i\,(x_i\cdot x_q)"),
        ],
        U=(0, 1, 3, 5, 6, 8), D=(15, 16), I=(7, 11, 13, 17),
        also=(("The series' autodiff", "explainer/ai/autodiff.py"),),
    ),
    Part(
        n=14, level="U", widget="sixnd", prereq=(10, 12, 13),
        question="How did a model built to translate sentences become the engine of nearly everything?",
        story="The part opens in June 2017 with 'Attention Is All You Need', a translation model of 213 million "
              "parameters trained for three and a half days on eight graphics cards, and places every model it will "
              "meet by date and size. The Transformer is cut three ways: encoders, decoders and both. Pretraining on "
              "raw text and then fine-tuning becomes the recipe with ULMFiT, ELMo and GPT-1; BERT's masked objective "
              "wins the benchmarks, and T5 turns every task into text. The decoder then scales: GPT-2 does tasks it "
              "was never trained for, and GPT-3, 174.6 billion parameters counted from its shape and 3.14 x 10^23 "
              "operations by 6ND, learns from examples in its prompt. The part turns when a predictor of text "
              "becomes an assistant, through Codex, instruction tuning and ChatGPT in November 2022, and the "
              "frontier closes. Open weights follow from LLaMA to the models of 2026, converging on one recipe "
              "(pre-norm, RMSNorm, SwiGLU, rotary positions, grouped queries) and then splitting again, while "
              "training compute grows about five times a year. It ends on the series' novels, with a GPT-style and "
              "a BERT-style model of the same shape trained at matched budgets, and a family of small GPTs searched "
              "for learning in context.",
        handoff="The memory of past tokens, latent attention and hybrids are Part 15; mixtures of experts and "
                "sparse attention Part 16; the hardware behind the scale Part 17, and how a frontier run is "
                "organized Part 18; serving Part 19; instruction tuning and human feedback are rebuilt on the "
                "series' own model in Part 27, and reasoning is Part 28.",
        outside="Nothing beyond the earlier parts; the papers named are short and can be read alongside.",
        objectives={
            "U": ["Tell the lineage in order, from the 2017 Transformer through GPT-1, BERT, T5, GPT-2 and GPT-3 "
                  "to ChatGPT and open weights, saying what each step changed.",
                  "Distinguish an encoder, a decoder and an encoder-decoder by what each position may see and by "
                  "its training objective."],
            "M": ["Count a decoder's parameters from its shape, 12Ld^2 plus the embeddings, and estimate its "
                  "training compute as 6ND.",
                  "Write the causal and the masked language-model objectives, and work out how many prediction "
                  "targets each gets from a sequence.",
                  "Compute a SwiGLU layer's width at equal parameters, and the size of a KV cache with and "
                  "without grouped queries."],
            "D": ["Say what an equal-compute comparison of a causal and a masked model holds fixed and what it "
                  "does not, and design a task on which both can be scored.",
                  "Design a test for in-context learning in a small model, with calibration against a content-free "
                  "query, and state what a null result at that scale shows."],
            "I": ["Read a model card: layers, width, heads, context, total and active parameters, tokens per "
                  "parameter, and whether a compute figure is published or an outside estimate.",
                  "Fit a growth rate to dated compute estimates and convert it to a doubling time, with its "
                  "interval."],
        },
        results=[
            ("Parameters from the shape", r"N\approx 12Ld^2+(V+n_{\text{ctx}})\,d"),
            ("Training compute", r"C\approx 6ND\qquad(\text{GPT-3: }3.14\times10^{23}\text{ operations})"),
            ("The causal objective", r"L_{\text{LM}}=-\sum_{t}\log p(x_t\mid x_{<t})"),
            ("The masked objective", r"L_{\text{MLM}}=-\sum_{t\in M}\log p(x_t\mid x_{\setminus M}),"
                                     r"\quad |M|\approx 0.15\,n"),
            ("SwiGLU's width", r"3dh=8d^2\ \Longrightarrow\ h=\tfrac{8}{3}d"),
            ("The KV cache", r"4\,L\,n_{kv}\,d_{\text{head}}\ \text{bytes per token, in 16-bit numbers}"),
        ],
        U=(0, 1, 2, 3, 5, 8, 9), D=(14,), I=(10, 11, 12),
        also=(("The series' autodiff", "explainer/ai/autodiff.py"),),
    ),
    Part(
        n=15, level="U", widget="deltamemory", prereq=(10, 11, 13, 14),
        question="What should a model keep of everything it has read, and what can it afford to forget?",
        story="The part opens with the bill for remembering everything: a key and a value for every token in every "
              "layer, tens of gigabytes for one long conversation with Llama 3.1. It first shrinks that cache, by "
              "sharing keys and values between heads, by DeepSeek's latent attention, and by evicting tokens while "
              "keeping the attention sink. Then it drops the softmax: regrouped, attention becomes a recurrence on "
              "one matrix, the fast weights of 1992, written by outer products and read with a key. Hopfield's "
              "network and a count of overlaps show why adding fills up with crosstalk; decay forgets on purpose, "
              "and the delta rule, one step of least squares per token, corrects. An associative scan and chunks in "
              "the WY form train such recurrences in parallel, and state-space models reach the same place from "
              "control theory, with Mamba letting each input choose its step. The part turns at a recall test, where "
              "six small models show what a fixed memory can and cannot look up, and at the hybrids that keep "
              "attention in one layer of four. It ends with how long a context really is, retrieval as a memory "
              "outside the model, and the open bets of 2026.",
        handoff="Choosing which tokens to read, sparse attention and DeepSeek's indexer, is Part 16; serving the "
                "cache fast is Part 19; the delta rule's reflections and state tracking meet reasoning in Part 28; "
                "agents manage memory by hand with notes, compaction and retrieval in Part 29; Part 30 looks for "
                "where a trained model keeps its facts.",
        outside="Matrix products and outer products, eigenvalues of a rank-one update, and a first-order linear "
                "differential equation.",
        objectives={
            "U": ["Price a KV cache from layers, key-value heads, head size and context length, and say what "
                  "grouped queries and latent attention save.",
                  "Explain how regrouping the product turns attention without a softmax into a fixed-size memory "
                  "that is written with outer products and read with a key."],
            "M": ["Show that N random unit keys in d dimensions give a relative read error of about (N - 1)/d "
                  "when pairs are added.",
                  "Derive the delta rule as one gradient step on the squared read error, and find the "
                  "eigenvalues of I - beta k k^T for a projection and a reflection.",
                  "Show that the scan operator is associative, and derive the zero-order hold for a linear "
                  "state-space model."],
            "D": ["Classify linear attention, decay, the delta rule, the gated delta rule, Titans and softmax "
                  "attention as online learners: name each one's loss and optimizer.",
                  "State what remains open: how much attention a hybrid needs, how a fixed memory should grow, "
                  "and how to measure what a model does with a million tokens."],
            "I": ["Choose a cache policy (a window, kept sink tokens, heavy hitters) and say what each risks "
                  "evicting.",
                  "Judge a long-context claim against needle, RULER and NoLiMa style tests, and decide between "
                  "a longer window, a hybrid and retrieval, with the kNN-LM's bound on what a wrong neighbour "
                  "costs."],
        },
        results=[
            ("The cache, per token", r"4\,L\,H\,d_h\ \text{bytes}\quad(\text{keys and values, 16-bit})"),
            ("Linear attention as a memory", r"S_t=S_{t-1}+v_tk_t^\top,\qquad y_t=S_t\,q_t"),
            ("Crosstalk of adding", r"\frac{\mathbb{E}\,\|Sk_j-v_j\|^2}{\|v\|^2}\approx\frac{N-1}{d}"),
            ("The delta rule", r"S_t=S_{t-1}\bigl(I-\beta k_tk_t^\top\bigr)+\beta\,v_tk_t^\top"),
            ("The scan's operator", r"(a_1,b_1)\bullet(a_2,b_2)=(a_1a_2,\ a_2b_1+b_2)"),
            ("Zero-order hold", r"\bar A=e^{\Delta A},\qquad \bar B=A^{-1}\bigl(e^{\Delta A}-I\bigr)B"),
        ],
        U=(0, 1, 3, 4, 13), D=(10, 15), I=(2, 12, 14),
        also=(("The series' autodiff", "explainer/ai/autodiff.py"),),
    ),
]
