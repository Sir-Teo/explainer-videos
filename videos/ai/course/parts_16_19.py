"""Act III, the Transformer Era: sparsity, silicon, pretraining at scale, inference (Parts 16-19)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=16, level="M", widget="expertload", prereq=(4, 7, 13, 15),
        question="Can a model use only a small part of itself for each token, and still be trained?",
        story="The part opens on DeepSeek-V3, where 8 of 256 experts and one shared expert light up for each word, and "
              "traces three threads to it: experts, sparse attention and sparse weights. It starts in 1991, where "
              "Jacobs, Jordan, Nowlan and Hinton make experts compete by weighting each one's own error with its "
              "posterior responsibility, and follows Shazeer's top-k gate of 2017 to the modern layer. The router's "
              "gradient is derived and checked by finite differences: a chosen score moves by its gate times how far "
              "its expert beat the gate-weighted average, and an unchosen score gets nothing. A mixture is then "
              "trained on the series' character transformer against dense models of equal arithmetic and of equal "
              "parameters. The part turns on collapse: left alone the router plays favourites, Switch's auxiliary "
              "loss spreads the load at the cost of a second goal, and DeepSeek's bias steers the choice without "
              "touching the loss. Capacity factors, the all-to-all between chips, parameter counts and upcycling "
              "follow from the same picture of loads. The second half asks the same question of depth "
              "(mixture-of-depths), of attention (windows, block selection, a learned indexer on a recall task) and "
              "of weights (lottery tickets, 2:4 pruning, sparse activations), and ends with the open mixtures and "
              "sparse-attention models of late 2026.",
        handoff="The tensor cores and links that make experts and 2:4 sparsity fast are Part 17. Expert parallelism "
                "and its all-to-all return in Part 18, serving experts and sparse attention in Part 19, experts in "
                "image and video models in Part 22, and sparsity inside the network, as features found by sparse "
                "autoencoders, in Part 30.",
        outside="Calculus and linear algebra; the softmax Jacobian of Part 4 and the transformer block of Part 13.",
        objectives={
            "U": ["Explain what a router, a gate and an expert are, and why a top-k mixture has many more parameters "
                  "than it uses for one token.",
                  "Count the total and the active parameters of a mixture-of-experts model from its configuration."],
            "M": ["Derive the router's gradient through a top-k softmax gate and through DeepSeek-V3's sigmoid gate, "
                  "and check it by finite differences.",
                  "Derive Switch's auxiliary loss and its lower bound, and compute the share of token slots dropped "
                  "at a capacity factor.",
                  "Compute what mixture-of-depths saves in matrix work and in attention scores at a routed fraction."],
            "D": ["Compare block selection (NSA, MoBA) with a learned indexer (DSA) as sparse attention, and state what "
                  "each can and cannot retrieve at a fixed number of keys per query.",
                  "State the lottery ticket hypothesis with rewinding, and say which control (re-initialized masks, "
                  "random masks) separates the mask from the initial weights."],
            "I": ["Choose between an auxiliary loss, a loss-free bias and a capacity factor for a mixture, and say "
                  "what each costs in dropped tokens and in the busiest chip's load.",
                  "Compute the all-to-all bytes and the experts' FLOPs per token per layer, and compare their ratio "
                  "with a chip's ridge."],
        },
        results=[
            ("The router's gradient", r"\frac{\partial L}{\partial s_j}=g_j\,(u_j-\bar u)\ \ (j\in K),\qquad 0\ "
                                      r"\text{otherwise};\quad \bar u=\sum_{i\in K}g_iu_i"),
            ("Switch's auxiliary loss", r"L_{\text{aux}}=\alpha E\sum_{i=1}^{E} f_iP_i,\qquad E\sum_i f_i^2\ \ge\ 1"),
            ("The loss-free bias", r"K=\operatorname{top-}k\,(s_i+b_i),\qquad b_i\leftarrow b_i-\gamma\,"
                                   r"\operatorname{sign}\bigl(f_i-\tfrac1E\bigr)"),
            ("Dropped at capacity factor c", r"\text{dropped share}=\sum_{i=1}^{E}\max\bigl(0,\ f_i-\tfrac{c}{E}\bigr)"),
            ("Teams of k from N experts", r"\Bigl(\frac{N}{k}\Bigr)^{k}\le\binom{N}{k}\le\Bigl(\frac{eN}{k}\Bigr)^{k}"),
            ("The all-to-all's intensity", r"\frac{\text{experts' FLOPs}}{\text{bytes sent}}=\frac{2\cdot 3dh\cdot k}"
                                           r"{3dk}=2h"),
        ],
        U=(0, 1, 3, 9, 14), I=(7, 8, 15), D=(13, 16),
        also=(("The series' autodiff", "explainer/ai/autodiff.py"),),
    ),
    Part(
        n=17, level="U", widget="rooflineridge", prereq=(3, 10),
        question="Why does AI run on graphics processors, and what limits how fast they can go?",
        story="The part opens with a count: Llama 3.1's training run on 16,384 H100s used about eighty million times "
              "the arithmetic of AlexNet's two gaming cards, almost all of it matrix products. It starts where "
              "clocks stopped: Dennard scaling ends when the voltage can fall no further, power grows like the cube "
              "of the clock, and the only way left to use transistors is in parallel. The GPU, built to run one "
              "small program on millions of pixels, becomes that parallel machine through CUDA, warps of 32 threads "
              "and latency hidden by keeping many loads in flight, and AlexNet shows what it is for. The part then "
              "turns from history to arithmetic: a matrix product costs 2mnk operations but needs each number "
              "fetched only once, tiling earns that reuse, and the roofline says any program runs at most at the "
              "smaller of the chip's peak and its memory bandwidth times the operations per byte. The computer "
              "rendering the film is measured against its own roofline. Systolic arrays and tensor cores build the "
              "reuse into the wiring, smaller number formats raise the peak, and the alpha-beta model prices the "
              "links between chips, where a ring all-reduce meets the bandwidth bound. It ends with kernels and "
              "Triton, the trends in FLOPs, dollars and watts, chips beyond the GPU, and the racks of late 2026.",
        handoff="Part 18 trains across many GPUs with the alpha-beta model, the ring all-reduce and eight-bit "
                "arithmetic. Part 19 puts inference on the roofline: reading a prompt is arithmetic-bound, writing "
                "an answer is memory-bound, and FlashAttention and the four-bit formats follow from that.",
        outside="School physics (power, voltage) and matrix multiplication; no computer architecture is assumed.",
        objectives={
            "U": ["Explain why clock speeds stopped rising in the early 2000s and why that made parallel chips the "
                  "way forward.",
                  "Count the operations of a matrix product, and say what a GPU spends its transistors on that a "
                  "CPU does not."],
            "M": ["Derive the arithmetic intensity of a matrix product and of its tiled form, and place a workload "
                  "on a chip's roofline.",
                  "Derive the time of a ring and of a tree all-reduce in the alpha-beta model, and find where they "
                  "cross.",
                  "Compute a floating-point format's unit roundoff and largest finite number from its bit layout."],
            "D": ["State Hong and Kung's lower bound on the traffic of a matrix product and the bandwidth lower "
                  "bound for all-reduce, and say which algorithms meet them.",
                  "Explain why the ridge of the roofline keeps moving right, and what that asks of future kernels "
                  "and number formats."],
            "I": ["Read a datasheet's peak, bandwidth and link speed, compute the ridge, and decide whether a "
                  "matrix-vector or a matrix-matrix workload can reach the roof.",
                  "Estimate a kernel's occupancy from its registers per thread, and say when fewer warps doing "
                  "more work per load are faster."],
        },
        results=[
            ("Switching power", r"P=CV^2f;\qquad \text{lengths and }V\text{ down by }\kappa\ \Rightarrow\ "
                                r"\text{power per area constant}"),
            ("Arithmetic intensity of C = AB", r"I=\frac{W}{Q}=\frac{2mnk}{s\,(mk+kn+mn)}\ \ \text{FLOP/byte}"),
            ("Tiling, and Hong and Kung's bound", r"Q\approx\frac{2n^3}{b},\ \ 3b^2\le M;\qquad Q=\Omega\Bigl("
                                                   r"\frac{n^3}{\sqrt M}\Bigr)"),
            ("The roofline", r"\text{speed}\ \le\ \min\bigl(P,\ \beta I\bigr),\qquad \text{ridge}\ I^\ast=P/\beta"),
            ("A systolic array", r"\text{cell }(i,j)\text{ meets }a_{ik},b_{kj}\text{ at cycle }i+j+k;\quad "
                                 r"T=K+2n-2"),
            ("Ring all-reduce", r"T_{\text{ring}}=2(p-1)\,\alpha+2\,\frac{p-1}{p}\,\frac{n}{\beta}"),
        ],
        U=(0, 1, 2, 4, 5, 6), I=(11, 12, 13), D=(14,),
    ),
    Part(
        n=18, level="M", widget="pipelinebubble", prereq=(11, 14, 16, 17),
        question="What does it take to train one model on sixteen thousand GPUs for fifty-four days?",
        story="The part opens on Llama 3's run: 16,384 GPUs, 54 days, 466 interruptions, 419 of them unplanned, one every three hours. It "
              "first follows the data. A sample of Common Crawl goes through extraction, a blocklist and language "
              "identification; MinHash is derived (two sets' minimum hashes agree with probability equal to their "
              "Jaccard similarity) and banded into an S-curve that finds near-duplicates without comparing every "
              "pair; a quality classifier, contamination checks, mixtures and a unigram model of collapse follow. "
              "After the objectives and the staging of a run, the part turns to arithmetic: about six operations "
              "per parameter per token, sixteen bytes per parameter in mixed-precision Adam. No single chip holds "
              "that, so the model is cut five ways, each checked on four processes of the rendering computer: data "
              "parallelism on the ring all-reduce, whose bandwidth bound is proved, ZeRO and FSDP, Megatron's tensor "
              "split, the pipeline with its bubble, and context and expert parallelism. The last third keeps the "
              "run alive: fewer bits with loss scaling and per-tile FP8 scales, QK-norm and the z-loss, a second "
              "token predicted ahead, and Young's checkpoint interval against failures. It ends by training the "
              "series' model with the 2020 recipe and the 2026 recipe at equal data, steps and seed, for the "
              "scoreboard.",
        handoff="Serving the trained model is Part 19, where the multi-token-prediction module returns as a drafter "
                "and the number formats as four-bit weights. The same data pipelines feed images, video and sound "
                "in Parts 22 and 23; post-training starts from a pretrained model in Part 27 and reasoning in Part "
                "28; Parts 30 and 31 open the model up and test how far its evaluations can be trusted.",
        outside="Probability with sets and independence; the optimizers of Part 11 and the hardware terms of Part "
                "17 (FLOP, bandwidth, the alpha-beta model).",
        objectives={
            "U": ["Describe the stages between a web crawl and a pretraining corpus, and say what each one removes.",
                  "Tell the causal, masked, span-corruption and fill-in-the-middle objectives apart on one "
                  "sentence."],
            "M": ["Prove that two sets' minimum hashes agree with probability equal to their Jaccard similarity, "
                  "and derive the banding curve.",
                  "Estimate a run's compute as 6ND and its memory per GPU without ZeRO and at ZeRO stages 1, 2 "
                  "and 3.",
                  "Derive the pipeline bubble for GPipe, 1F1B, interleaved 1F1B and ZB-H1, and Young's checkpoint "
                  "interval."],
            "D": ["Prove that no all-reduce beats the ring's bandwidth term, by counting the messages one number "
                  "needs.",
                  "Derive the bound QK-norm puts on an attention logit and explain what the z-loss constrains "
                  "instead."],
            "I": ["Choose a layout of data, tensor, pipeline, context and expert parallelism for a given cluster, "
                  "and compute the run's model FLOPs utilization.",
                  "Pick a number format and its scaling (BF16, FP16 with loss scaling, FP8 per tile) for training, "
                  "and a checkpoint interval from the checkpoint cost and the failure rate."],
        },
        results=[
            ("MinHash", r"\Pr\bigl[\min h(A)=\min h(B)\bigr]=J(A,B)=\frac{|A\cap B|}{|A\cup B|}"),
            ("Banding: b bands of r", r"\Pr[\text{candidate pair}]=1-\bigl(1-s^{r}\bigr)^{b}"),
            ("Compute and memory", r"C\approx 6ND,\qquad \text{mixed-precision Adam: }(2+2+12)\ \text{bytes per "
                                   r"parameter}"),
            ("All-reduce's bandwidth bound", r"T\ \ge\ 2\,\frac{p-1}{p}\,\frac{n}{B}\quad\text{(the ring meets it)}"),
            ("The pipeline bubble", r"\frac{\text{idle}}{\text{total}}=\frac{p-1}{m+p-1}\quad\text{(GPipe and "
                                    r"1F1B)}"),
            ("Young's checkpoint interval", r"\tau^\ast=\sqrt{2\,\delta M},\qquad \text{waste}\approx\sqrt{2\delta/M}"),
        ],
        U=(0, 1, 2, 6), D=(9, 15), I=(4, 13, 17, 18),
    ),
    Part(
        n=19, level="M", widget="roundingstep", prereq=(13, 15, 17, 18),
        question="Why is writing an answer so much slower than reading a prompt, and what makes it cheap?",
        story="The part opens with a speed limit: to write one token a model reads every active weight, so tokens "
              "per second cannot beat the memory bandwidth divided by the bytes of weights, while the chip's "
              "arithmetic sits almost idle. On Part 17's roofline a prompt is a matrix product and a decode step a "
              "matrix-vector product, and the key-value cache is priced per token for multi-head, grouped-query and "
              "latent attention. A server answers by sharing each read among many conversations: batching trades "
              "speed against cost, continuous batching keeps the batch full, and pages and shared prefixes keep the "
              "memory full. The part then turns to exactness. Speculative decoding lets a drafter guess ahead and "
              "the big model check in one pass, and the acceptance rule min(1, p/q) with its leftover is proved to "
              "return the big model's distribution; two drafters are trained and timed. Quantization starts from "
              "Bennett's rounding error, meets outlier channels, and spends the error where it hurts least with "
              "SmoothQuant, GPTQ derived from Optimal Brain Surgeon, and rotations, down to the four-bit floats "
              "MXFP4 and NVFP4 and a quantized cache. FlashAttention computes attention in tiles with an online "
              "softmax and never writes its table. It ends with constrained decoding by an automaton's token mask "
              "and with what longer thinking and on-device models cost in late 2026.",
        handoff="Generating images one pixel at a time and the race to take fewer steps are Parts 20 and 21. "
                "Reasoning models pay for their thinking tokens at decode time in Part 28, and agents run long "
                "contexts with shared prefixes in Part 29. The outlier channels of chapter 9 return in Part 30 as "
                "a clue to superposition, and Part 31 asks how far the output can be trusted.",
        outside="Probability (total variation, expectations of geometric sums), a Lagrange multiplier, and Part "
                "17's roofline and number formats.",
        objectives={
            "U": ["Explain why a decode step is bound by memory bandwidth and a prefill by arithmetic, and compute "
                  "the weight-only bound on tokens per second.",
                  "Compute the bytes a key-value cache keeps per token from a model's layers, heads and head size."],
            "M": ["Prove that speculative sampling outputs the big model's distribution and accepts a draft with "
                  "probability 1 - TV(p, q), and derive the expected tokens per pass.",
                  "Derive the rounding error of a uniform quantizer and say when the prediction fails.",
                  "Derive the online softmax and FlashAttention's memory traffic, and combine two chunks of keys "
                  "exactly."],
            "D": ["Derive the Optimal Brain Surgeon update and its error with a Lagrange multiplier, and explain "
                  "how GPTQ applies it column by column.",
                  "Show that a transformer with unit-gain RMSNorm is invariant to an orthogonal rotation of its "
                  "residual stream, and explain why a rotation helps four-bit activations."],
            "I": ["Size a server: choose a batch, a page size and a prefix cache from the context length, the "
                  "memory and the price of a GPU-hour.",
                  "Choose a weight format and a scale granularity (per tensor, per row, per block) for a target "
                  "number of bits, and say what calibration data the method needs."],
        },
        results=[
            ("The weight-only bound", r"\text{tokens per second}\ \le\ \frac{\text{memory bandwidth}}"
                                      r"{\text{bytes of active weights}}"),
            ("Speculative sampling", r"\text{accept }x\sim q\text{ w.p. }\min\Bigl(1,\frac{p(x)}{q(x)}\Bigr);\ "
                                     r"\text{else draw from }\frac{(p-q)_+}{\sum_y (p-q)_+}"),
            ("Exactness and acceptance", r"\Pr[\text{output}=x]=p(x),\qquad \Pr[\text{accept}]=1-"
                                         r"\operatorname{TV}(p,q)"),
            ("Tokens per pass, k drafts", r"\mathbb{E}[\text{tokens}]=\frac{1-\alpha^{k+1}}{1-\alpha},\qquad "
                                          r"S(k)=\frac{1-\alpha^{k+1}}{(1-\alpha)(1+kc)}"),
            ("Rounding error", r"\mathbb{E}[e^2]=\frac{\Delta^2}{12},\qquad \Delta=\frac{\max|w|}{2^{\,b-1}-1}"),
            ("Optimal Brain Surgeon", r"\delta=\frac{\hat w_q-w_q}{[H^{-1}]_{qq}}\,H^{-1}e_q,\qquad "
                                      r"\text{error}=\frac{(w_q-\hat w_q)^2}{2\,[H^{-1}]_{qq}}"),
        ],
        U=(0, 2, 8, 16), I=(3, 4, 5, 13, 15), D=(11, 17),
    ),
]
