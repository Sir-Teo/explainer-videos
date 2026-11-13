"""The end of Act IX, Systems at Scale, and the start of Act X: system design, reliability, graphics, numerics, quantum computation (Parts 48-53)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=48, level="U", widget="chezipf", prereq=(20, 31, 39, 43),
        question="Which few blocks is a large system assembled from, and what does the arithmetic of each one promise?",
        story="The part opens on a napkin: 10 million users a day times 20 actions is 200 million requests, about "
              "2,315 a second on average and 6,944 at the evening peak, and 199 TB of storage in five years. A "
              "design is then made in eight decisions, followed through on a pastebin, and each block the decisions "
              "call for is built and measured. Two random choices beat round robin on 50 servers, and Maglev's "
              "table is compared with a hash ring when one of 20 backends leaves. Che's approximation, with one "
              "unknown called the characteristic time, predicts an LRU cache's hit rate on Zipf traffic to within "
              "half a point. A hot key's expiry causes about 400 rebuilds until XFetch's random early refresh "
              "replaces them with one, and a token bucket is shown to be a guarantee: at most sigma + rho s "
              "requests in any interval. The part goes on through queues, storage engines, sharding, replication, "
              "identifiers that sort by time, blobs, and space-filling curves that turn a map into keys. It ends "
              "by load-testing the Job as a service made of these blocks, with and without its cache, and at the "
              "frontier with a learned index and the question of predicting a system before it is built.",
        handoff="Part 49 designs eight whole systems with these blocks, from a URL shortener to a ride-hailing "
                "service. Part 50 keeps them running, with service-level objectives, retries and capacity plans, "
                "and returns to metastable failures. Part 56 looks at load and expansion through the spectrum of "
                "a graph, and Part 59 at the theory of the distributed algorithms underneath.",
        outside="Arithmetic with powers of ten, and the exponential function; no experience of running a service "
                "is assumed.",
        objectives={
            "U": ["Estimate a service's requests a second, storage and bandwidth from its daily users, a peak "
                  "factor and an object size.",
                  "Explain why a consistent-hash ring moves only the departed backend's keys, and what hash modulo "
                  "N moves instead.",
                  "Lay out a Snowflake ID's bits and compute how many years and how many IDs a millisecond it "
                  "allows."],
            "M": ["Derive Che's approximation and find the characteristic time by bisection.",
                  "Prove that a token bucket of depth sigma and rate rho admits at most sigma + rho s requests in "
                  "any interval of length s.",
                  "Derive XFetch's trigger probability and the time before expiry at which a refresh is expected."],
            "D": ["Build a learned index with a bounded error and compare its size and comparisons with a B+ "
                  "tree's inner nodes.",
                  "State what a competitive guarantee for cache admission on drifting Zipf traffic would have to "
                  "compare against, and why the classical bounds do not give it."],
            "I": ["Size a worker pool with Little's law and a target utilization, and say why the queue's age is "
                  "the signal to scale on.",
                  "Choose a shard key for a workload, and handle a hot key by salting it.",
                  "Load-test a design in simulation and report the median and the 99th percentile against the "
                  "request rate, with and without the cache."],
        },
        results=[
            ("Che's approximation", r"\sum_i\bigl(1-e^{-p_iT}\bigr)=C,\qquad h=\sum_i p_i\bigl(1-e^{-p_iT}\bigr)"),
            ("XFetch", r"\text{refresh if } t-\Delta\beta\ln U\ \ge\ \text{expiry};\quad P(\text{trigger at } r)=e^{-r/\beta\Delta}"),
            ("Token bucket envelope", r"A(t,\,t+s)\ \le\ \sigma+\rho s\quad\text{for every } t \text{ and } s\ge 0"),
            ("Birthday bound, UUIDv4", r"P(\text{collision among } n)\approx 1-e^{-n^2/2^{123}}"),
            ("Little's law", r"L=\lambda W:\quad 210/\text{s}\times 0.5\ \text{s}=105 \text{ busy workers}"),
            ("What a cache buys", r"\text{capacity}\ \times\ \frac{1}{1-h}\quad\text{at hit rate } h"),
        ],
        U=(0, 1, 2, 6, 10), D=(15,), I=(7, 8, 9, 11, 13, 14),
        also=(("The design instruments", "explainer/cs/design"),),
    ),
    Part(
        n=49, level="U", widget="fanoutcut", prereq=(39, 43, 46, 48),
        question="What is the one hard idea inside each of eight systems that almost everyone uses?",
        story="The part opens with eight systems and the eight ideas they turn on: the birthday bound, fan-out, "
              "logical clocks, Bloom filters, the assignment problem, control loops, idempotency and CRDTs. Each "
              "system is designed by Part 48's method, from the napkin to the hard part examined with numbers. A "
              "URL shortener needs seven base-62 characters for a trillion links, and a truncated hash collides "
              "often enough that every write must check. A news feed on a synthetic power-law graph of 100,000 "
              "users costs 6.9 million timeline writes a day pushed and 276 million fetches pulled, and the hybrid "
              "turns out to buy a bound on one post's fan-out, not fewer operations. A chat service orders "
              "messages by the conversation's sequence numbers, a crawler stays polite and forgets nothing with a "
              "Bloom filter, a dispatcher's optimal assignment beats the nearest driver, and three video players "
              "trade bitrate against stalls. A ledger that sums to zero still charges 1,390 payments twice until "
              "idempotency keys are added, and concurrent edits converge only when they are transformed. A "
              "Dynamo-style store and a metrics pipeline follow, the Job runs at a million books a day, and the "
              "frontier asks how designs fail and whether design can be checked before it is built.",
        handoff="Part 50 runs these systems, with service-level objectives, incident response and capacity "
                "planning, and uses the metrics pipeline. Part 51 opens the graphics and video pipelines behind the "
                "streaming service. Part 54 proves protocols and ledgers correct, and Part 59 returns to the "
                "theory of the distributed algorithms underneath.",
        outside="Logarithms and the idea of a probability; the systems themselves are familiar from daily use.",
        objectives={
            "U": ["Compute how many base-62 characters N links need, and convert a number to its code by repeated "
                  "division.",
                  "Explain why a conversation's sequence numbers order messages where the senders' clocks do not.",
                  "Write a payment as balanced ledger lines in cents and check that the entry sums to zero."],
            "M": ["Derive the daily cost of fan-out on write, on read and of the hybrid over a power-law follower "
                  "graph, and show that their ratio is reads over posts.",
                  "Transform two concurrent inserts so that both sites converge, and exhibit the divergence "
                  "without transformation.",
                  "Compute the chance of a stale read for a quorum setting (N, R, W), and say when it is zero."],
            "D": ["Explain why the count of operations gives the hybrid feed no interior optimum, and name what "
                  "must be priced for a finite threshold to appear.",
                  "Summarize what studies of post-mortems say about how designs fail, and what formal models and "
                  "deterministic simulation can check before a system is built."],
            "I": ["Size a crawler, a chat service or a metrics pipeline on a napkin: rates, connections, storage, "
                  "machines.",
                  "Make a payment API safe to retry with an idempotency key stored in the same transaction as its "
                  "reply.",
                  "Compare adaptive-bitrate players by mean bitrate, seconds stalled and quality switches on the "
                  "same traces."],
        },
        results=[
            ("Code length", r"L=\lceil\log_{62}N\rceil:\quad 10^{12}\ \text{links need } 7 \text{ characters}"),
            ("Truncated hashes", r"E[\text{collisions}]\approx\frac{m^2}{2\cdot 62^{k}}\quad(m \text{ links},\ k \text{ characters})"),
            ("Fan-out", r"\text{push}=p\,U\,E[F],\quad \text{pull}=r\,U\,E[F],\quad \frac{\text{pull}}{\text{push}}=\frac{r}{p}"),
            ("The hybrid feed", r"W(\tau)=U\bigl[\,p\,E[F;\,F<\tau]+r\,E[F;\,F\ge\tau]\,\bigr]"),
            ("Bloom filter", r"P(\text{false positive})=\bigl(1-e^{-kn/m}\bigr)^{k}"),
            ("Ledger invariants", r"\sum \text{lines}=0,\ \ \text{and at most one entry per payment}"),
        ],
        U=(0, 1, 2, 4, 8), D=(13,), I=(3, 5, 6, 7, 10, 11, 12),
        also=(("The case-study instruments", "explainer/cs/design/cases.py"),),
    ),
    Part(
        n=50, level="U", widget="retrystorm", prereq=(31, 38, 43, 48),
        question="Why does a system that survives the loss of half its capacity stay down after the capacity comes back?",
        story="The part opens with three post-mortems from the companies' own reports, Amazon S3 in 2017, "
              "Cloudflare in 2019 and CrowdStrike in 2024: each a routine change pushed too far, too fast. "
              "Reliability is then made arithmetic. Nines are downtime budgets, parts in series multiply their "
              "availabilities and parts in parallel multiply their failures, and a shared cause is a switch in "
              "series that caps the nines replicas can buy. An objective of 99.9% turns into an error budget that "
              "a synthetic month spends incident by incident, and burn-rate alerts are derived and scored. The "
              "turn comes with a server that loses half its capacity for ten seconds: without retries it answers "
              "again 11 seconds later, and with three immediate retries the load sent climbs to four times what "
              "users send and nothing is answered in time again. Retry budgets, load shedding and circuit breakers "
              "are measured against that trigger. The second half is about finding out: histograms and DDSketch, "
              "traces and their critical path, coordinated omission, a flame graph of Pebble running the Job, "
              "capacity plans, incidents and chaos experiments on the Job service and a Raft cluster. It ends at "
              "the frontier with gray failure and the triggers that tip a system into a metastable state.",
        handoff="Part 51 renders frames against a sixteen-millisecond budget, an objective of its own. Part 54 "
                "proves protocols and configurations correct before they ship, and Part 55 asks whether deployed "
                "software can be trusted at all. Part 59 returns to the theory of distributed algorithms and what "
                "they cannot do.",
        outside="Probabilities of independent events, and logarithms; no experience of being on call is assumed.",
        objectives={
            "U": ["Convert an availability into nines and into minutes of downtime a year, a month and a week.",
                  "Compute the availability of a request path built from parts in series and replicas in parallel.",
                  "Explain why the average of ten servers' 99th percentiles is not the fleet's 99th percentile."],
            "M": ["Derive the burn-rate threshold b = f x 720 h / w and choose the windows of a multiwindow alert.",
                  "Prove DDSketch's relative-error guarantee from its bucket boundaries.",
                  "Explain the loop that keeps a retrying server overloaded after its trigger ends, and why backoff "
                  "with jitter does not break it but a retry budget does."],
            "D": ["Define gray failure by differential observability and say how a client can judge health from "
                  "real requests.",
                  "Map which triggers, by depth and length, leave a retrying system collapsed, and state what a "
                  "model of metastability would have to predict."],
            "I": ["Detect coordinated omission in a load test and measure latency from intended send times instead.",
                  "Read a flame graph and check a sampling profile against the binomial error of its counts.",
                  "Design a chaos experiment with a steady state, a hypothesis, a control and a bounded blast radius."],
        },
        results=[
            ("Series and parallel", r"A_{\text{series}}=\prod_i A_i,\qquad A_{\text{parallel}}=1-\prod_i(1-A_i)"),
            ("Up time", r"A=\frac{\text{MTBF}}{\text{MTBF}+\text{MTTR}}"),
            ("A shared cause", r"A=(1-cq)\bigl(1-q'^{\,3}\bigr),\qquad q'=\frac{(1-c)\,q}{1-cq}"),
            ("Burn rate", r"b=\frac{\text{error rate}}{1-\text{SLO}},\qquad \text{page at } b=f\cdot\frac{720\ \text{h}}{w}"),
            ("DDSketch", r"\gamma=\frac{1+\alpha}{1-\alpha},\quad \hat x=\frac{2\gamma^{i}}{\gamma+1},\quad |\hat x-x|\le\alpha x"),
            ("A profile's error", r"\operatorname{se}(\hat p)=\sqrt{\hat p(1-\hat p)/n}"),
        ],
        U=(0, 1, 2, 6, 7), D=(15,), I=(8, 9, 10, 11, 12, 13, 14),
        also=(("The operations instruments", "explainer/cs/ops"),),
    ),
    Part(
        n=51, level="U", widget="depthcrowd", prereq=(4, 20, 22, 36),
        question="How do millions of samples of light become a picture, and how many samples are enough?",
        story="The part opens with the series' own box rendered at 1, 4, 16 and 256 paths per pixel, its error "
              "falling close to 1/sqrt(N), and with the two ways to make a picture: a rasterized triangle and a "
              "ray-traced image. The first half builds the rasterizer. Homogeneous coordinates make translation "
              "linear, perspective is similar triangles and one division, and the depth it stores is affine in "
              "1/d, so a 24-bit buffer that resolves 0.06 at distance 1000 with the near plane at 1 resolves only "
              "5.9 with it at 0.01. Edge functions, barycentric coordinates, interpolation of 1/w, the z-buffer, "
              "shading and mipmaps follow, each measured against a ray-cast reference. The part then turns from "
              "triangles to light: rays meet spheres and triangles, a bounding volume hierarchy cuts 100,000 "
              "tests per ray to 2.5, and radiometry leads to Kajiya's rendering equation, whose Neumann series is "
              "summed bounce by bounce on screen. A path tracer solves it by Monte Carlo with cosine-weighted "
              "sampling, Russian roulette and next-event estimation, and a denoiser makes 16 paths look better "
              "than 256. It ends with Bezier curves, subdivision surfaces and fonts, and at the frontier with "
              "real-time ray tracing and neural rendering.",
        handoff="Part 52 treats integration and linear solvers with the care rounding demands. Part 57 asks when "
                "learning from images can generalize, and Part 60 builds hardware for one job, of which the GPU is "
                "the first example. Part 61 returns to this part's open problems as research.",
        outside="Vectors, matrices and the dot and cross products; integrals over an angle for the second half.",
        objectives={
            "U": ["Compose translations and rotations as 4 x 4 matrices and predict the effect of their order.",
                  "Derive the perspective projection from similar triangles and say why the division cannot be "
                  "part of the matrix.",
                  "Evaluate a cubic Bezier curve by de Casteljau's construction and split it in two."],
            "M": ["Derive perspective-correct interpolation and show that u/w and 1/w are affine on the screen.",
                  "State the rendering equation, expand it as a Neumann series and identify each term with paths "
                  "of a given number of bounces.",
                  "Prove that Russian roulette leaves the estimator unbiased, and compute the variance it adds."],
            "D": ["Explain what a denoiser trades for its lower error, and why a guarantee for it is an open "
                  "problem.",
                  "Describe neural radiance fields and Gaussian splatting as this part's rendering run in reverse, "
                  "and what is lost."],
            "I": ["Choose near and far planes and a depth format so that two surfaces a given gap apart do not "
                  "z-fight.",
                  "Build a bounding volume hierarchy with the surface-area heuristic and count box and triangle "
                  "tests per ray.",
                  "Compare sampling strategies by efficiency, 1 / (error squared x time), at equal sample counts."],
        },
        results=[
            ("Perspective", r"y'=\frac{n\,y}{d},\qquad z_{\text{ndc}}=\frac{f+n}{f-n}-\frac{2fn}{(f-n)\,d}"),
            ("Depth resolution", r"\Delta\approx\frac{d^{2}\,(f-n)}{f\,n\,(2^{b}-1)}"),
            ("Perspective-correct interpolation", r"u=\frac{\sum_i\lambda_i\,u_i/w_i}{\sum_i\lambda_i/w_i}"),
            ("The rendering equation", r"L_o=L_e+\int_{\Omega} f_r\,L_i\cos\theta_i\,d\omega_i"),
            ("Neumann series", r"L=L_e+TL_e+T^{2}L_e+\cdots"),
            ("Russian roulette", r"E[X']=q\cdot\frac{X}{q}=X,\quad \operatorname{Var}[X']=\operatorname{Var}[X]+\bigl(\tfrac1q-1\bigr)E[X^{2}]"),
        ],
        U=(0, 1, 2, 3, 4, 13), D=(14,), I=(6, 8, 12),
        also=(("The graphics instruments", "explainer/cs/graphics"),),
    ),
    Part(
        n=52, level="U", widget="rungenodes", prereq=(4, 9, 20),
        question="With rounding in every operation, which computed answers can be trusted?",
        story="The part opens with the ten algorithms of the twentieth century, eight of them numerical, and with "
              "two equations whose answer is almost exactly (1, 1): elimination as taught returns x1 = 0, and "
              "swapping the rows first returns 1 and 1. The problem was well conditioned and the algorithm "
              "unstable, and the part is built on that separation. The condition number belongs to the problem, "
              "backward error to the algorithm, and the forward error is at most their product: on Hilbert "
              "systems the backward error stays near rounding level while the answer loses every digit by size "
              "12. Elimination becomes LU with pivoting, whose growth can reach 2^(n-1) and almost never does. "
              "Householder's mirrors solve least squares without squaring the condition number, the SVD "
              "regularizes a blur, and the shifted QR algorithm finds eight eigenvalues in 16 iterations, not "
              "623. Conjugate gradients and multigrid then solve Poisson's equation, the second at a cost "
              "proportional to the unknowns. Newton's fractal, Runge's phenomenon and Chebyshev points, "
              "quadrature, stiff and symplectic integrators and the BLAS follow, and the frontier is randomized "
              "and low-precision numerics, with the missing theorem for partial pivoting.",
        handoff="Part 53's quantum computer is a unitary matrix acting on a vector. Part 54 proves programs "
                "correct, floating point included. Part 56 reads a graph through the eigenvalues of its matrix, "
                "and Part 57's learning theory rests on the same optimization. Part 51's renderer is this part's "
                "linear algebra and integration done billions of times a second.",
        outside="Matrices, derivatives and Taylor series; Part 4's floating-point numbers are the starting point.",
        objectives={
            "U": ["Compute the relative condition number of a function and say how many digits it costs.",
                  "Solve a small system by LU with partial pivoting and explain what the tiny pivot did without it.",
                  "Run bisection, the secant method and Newton's method on one equation and compare the digits "
                  "gained per step."],
            "M": ["Derive forward error <= kappa x backward error and compute a solve's backward error from its "
                  "residual.",
                  "Derive Householder QR and explain why the normal equations square the condition number.",
                  "State conjugate gradients' bound and multigrid's work recurrence, and check both on Poisson's "
                  "equation."],
            "D": ["Explain why a randomized SVD with a few extra columns matches the best rank-k error, and what "
                  "power steps add.",
                  "State what smoothed analysis says about elimination's growth factor and which theorem for "
                  "partial pivoting is still missing."],
            "I": ["Choose a fill-reducing ordering for a sparse factorization and measure the factor's nonzeros.",
                  "Recognize a stiff problem from an explicit solver's step count and switch to an implicit method.",
                  "Use mixed-precision iterative refinement, and say at which condition number it stops working."],
        },
        results=[
            ("Condition numbers", r"\kappa_f=\Bigl|\frac{x f'(x)}{f(x)}\Bigr|,\qquad \kappa(A)=\|A\|\,\|A^{-1}\|=\frac{\sigma_{\max}}{\sigma_{\min}}"),
            ("Backward error analysis", r"\frac{\|\hat x-x\|}{\|x\|}\ \lesssim\ \kappa(A)\,\eta,\qquad \eta=\frac{\|b-A\hat x\|}{\|A\|\,\|\hat x\|}"),
            ("Growth under partial pivoting", r"\rho\ \le\ 2^{\,n-1},\ \text{attained by Wilkinson's matrix}"),
            ("Normal equations", r"\kappa(A^{\mathsf T}A)=\kappa(A)^{2}"),
            ("Conjugate gradients", r"\|e_k\|_A\ \le\ 2\Bigl(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\Bigr)^{k}\|e_0\|_A"),
            ("Multigrid's work", r"W(n)=c\,n+W(n/4)=\tfrac43\,c\,n"),
        ],
        U=(0, 1, 3, 10, 12), D=(15,), I=(8, 14),
        also=(("The numerical instruments", "explainer/cs/numeric"),),
    ),
    Part(
        n=53, level="U", widget="groverturn", prereq=(1, 19, 27, 30),
        question="What can a computer made of quantum parts do that no classical computer can, and what can it not?",
        story="The part opens with Feynman's question of 1981: n two-state particles need 2^n amplitudes, 16 "
              "petabytes for fifty, so can a classical computer simulate quantum physics at all? It starts from "
              "the cost of forgetting, Landauer's kT ln 2 per erased bit, and from reversible gates, which are "
              "permutations; allowing any unitary turns shuffles into rotations. A qubit is a point on the Bloch "
              "sphere, two of them can share a Bell state that wins the CHSH game 85.4% of the time against a "
              "classical 75%, and no gate can copy an unknown state. The series' state-vector simulator, about a "
              "hundred lines, then runs every algorithm. Interference answers Deutsch and Jozsa's question in one "
              "query, Simon's problem separates quantum from classical queries, and the quantum Fourier "
              "transform and phase estimation lead to Shor's algorithm, which factors 15 and 21 from spikes at "
              "multiples of 2^t / r. The turn is what does not speed up: Grover's search is a rotation that needs "
              "about (pi/4) sqrt(N) rounds, no fewer, and overshoots after that. The part closes with error "
              "correction, from the three-qubit code to the surface code and its threshold, and at the frontier "
              "with BB84, post-quantum standards and the resources RSA-2048 would take.",
        handoff="Part 54 proves programs correct, and the same logic extends to quantum ones. Part 55 asks what "
                "can be trusted, the post-quantum migration included. Part 56's expander graphs build good codes, "
                "classical and quantum, and Part 60 returns to the hardware.",
        outside="Complex numbers, vectors and matrices; no physics is assumed, and the physics itself is in the "
                "companion films.",
        objectives={
            "U": ["Write a qubit as two amplitudes, apply the Born rule, and place the state on the Bloch sphere.",
                  "Build a Bell state from H and CNOT and show that it does not factor into two qubits.",
                  "Explain Grover's search as two reflections that rotate the state by 2 theta, and compute the "
                  "best number of rounds for N items."],
            "M": ["Derive the quantum Fourier transform's circuit from its product formula and count its gates.",
                  "Run phase estimation on an eigenvalue and bound the probability of the nearest outcome by "
                  "4 / pi^2.",
                  "Reduce factoring to order finding, and recover the order from a measurement by continued "
                  "fractions."],
            "D": ["Place BQP between BPP and PSPACE, and state what the oracle separations do and do not show "
                  "about NP.",
                  "Compare the published resource estimates for RSA-2048 with today's hardware, and say what "
                  "error correction below threshold changes."],
            "I": ["Simulate a circuit as a state vector, and say what a real device returns in place of the "
                  "amplitudes.",
                  "Compute a repetition code's logical error rate at distance d and the factor each step in "
                  "distance buys.",
                  "Detect an intercept-and-resend eavesdropper in BB84 from the error rate of the kept bits."],
        },
        results=[
            ("Landauer's principle", r"Q\ \ge\ kT\ln 2\ \text{ per erased bit}"),
            ("The CHSH game", r"P_{\text{classical}}\le\tfrac34,\qquad P_{\text{quantum}}=\cos^{2}\tfrac{\pi}{8}\approx 0.854"),
            ("Quantum Fourier transform", r"|j\rangle\ \mapsto\ \frac{1}{\sqrt N}\sum_{k=0}^{N-1}e^{2\pi i jk/N}\,|k\rangle,\quad \tfrac{n(n+1)}{2}+\lfloor\tfrac n2\rfloor \text{ gates}"),
            ("Phase estimation", r"|a_m|^{2}\ \ge\ \frac{4}{\pi^{2}}\ \text{ for the nearest } m \text{ to } 2^{t}\theta"),
            ("Shor's reduction", r"a^{r}\equiv 1\ (\mathrm{mod}\ N),\ r \text{ even}:\quad \gcd\bigl(a^{r/2}\pm 1,\ N\bigr)"),
            ("Grover's rotation", r"\sin\theta=\frac{1}{\sqrt N},\qquad P_k=\sin^{2}\bigl((2k+1)\theta\bigr),\qquad k\approx\frac{\pi}{4}\sqrt N"),
        ],
        U=(0, 1, 2, 3, 5, 10), D=(11, 13), I=(4, 12),
        also=(("The quantum instruments", "explainer/cs/quantum"),),
    ),
]
