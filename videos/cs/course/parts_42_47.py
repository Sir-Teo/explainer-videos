"""Act VIII, Building Software, and the start of Act IX, Systems at Scale: the browser, services, people, the cloud, data pipelines, search (Parts 42-47)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=42, level="U", widget="raggedlines", prereq=(12, 19, 36, 37),
        question="What happens between typing a URL and seeing a page, and how does it fit in 16.7 milliseconds a frame?",
        story="The part opens by typing an address and pressing enter: the name is resolved, a connection opens, HTML "
              "arrives, and then the browser's own work begins. A browser is five machines in one program, and the "
              "part builds each small enough to read. The HTML tokenizer is a state machine that never rejects its "
              "input, and the tree builder repairs six malformed documents with a stack of open elements. The "
              "cascade picks a style by specificity, a lexicographic order on three counts, and matches selectors "
              "right to left. Layout distributes free space with flexbox and breaks paragraphs into lines, where "
              "Knuth and Plass's dynamic program beats the greedy rule on Darcy's letter in Pride and Prejudice. One "
              "event loop schedules tasks, microtasks and rendering into frames of 16.7 ms: a 120 ms task drops "
              "seven of them, and the same work in 8 ms chunks drops none. The part then covers JavaScript engines, "
              "virtual-DOM diffing, caches, Core Web Vitals, the same-origin security model and the WCAG contrast "
              "ratio, and runs the pieces together as a toy browser that renders the series' own README. It ends at "
              "the frontier: nested intrinsic sizing that costs 2,097,151 layouts at depth 20 without a cache and 41 "
              "with one, layout checked by solvers, and formal models of web security.",
        handoff="Part 43 designs the APIs a page calls and keeps them compatible as they change. Part 44 measures "
                "whether a faster page changes what people do, and returns to the contrast ratio. Parts 45 and 48 "
                "put caches and content delivery at planetary scale, Part 51 opens the rasterizer and the GPU, and "
                "Parts 54 and 55 ask what it takes to trust a compiler, including the one in a JavaScript engine.",
        outside="Enough HTML, CSS and JavaScript to read a short page; no web framework is assumed.",
        objectives={
            "U": ["Trace a page load from the URL to pixels, naming the parser, the cascade, layout, paint and the "
                  "event loop.",
                  "Compute a selector's specificity and decide which of two rules wins.",
                  "Predict the output order of a script that mixes setTimeout, promises and await."],
            "M": ["Implement Knuth-Plass line breaking by dynamic programming and prove it optimal for an additive "
                  "cost.",
                  "Run the flexbox grow and shrink algorithm by hand on three items.",
                  "Explain hidden classes and inline caches, and why a megamorphic call site is slow."],
            "D": ["Explain why nested intrinsic sizing costs 2^(d+1) - 1 layouts without a cache, and state the open "
                  "problem of relayout bounded by the size of a change.",
                  "Describe what Cassius and the formal web-security models prove, and what they leave out."],
            "I": ["Find the long task behind a dropped frame and split it into chunks that fit the frame budget.",
                  "Give list rows stable keys, and say what breaks without them.",
                  "Check a colour pair against the WCAG contrast thresholds of 4.5 and 3."],
        },
        results=[
            ("Specificity", r"(a,b,c)=(\#\text{ids},\ \#\text{classes},\ \#\text{types}),\ \text{compared lexicographically}"),
            ("Knuth-Plass", r"\operatorname{best}(j)=\min_{i<j,\ \text{line }i..j\text{ fits}}\ \operatorname{best}(i)+\operatorname{cost}(i,j)"),
            ("Flexbox, growing", r"w_i=b_i+F\,\frac{g_i}{\sum_j g_j},\qquad F=W-\sum_j b_j\ \ge 0"),
            ("Flexbox, shrinking", r"w_i=b_i+F\,\frac{s_i b_i}{\sum_j s_j b_j},\qquad F<0"),
            ("Contrast ratio", r"\frac{L_1+0.05}{L_2+0.05}\in[1,21],\quad L=0.2126R+0.7152G+0.0722B"),
            ("Nested sizing", r"2^{d+1}-1\ \text{layouts at depth } d \text{ without a cache},\quad 2d+1 \text{ with one}"),
        ],
        U=(0, 1, 2, 3, 4, 6), D=(14,), I=(9, 10, 12),
        also=(("The browser instruments", "explainer/cs/web"),),
    ),
    Part(
        n=43, level="U", widget="retrycounter", prereq=(31, 36, 38, 39),
        question="What changes when a function call has to cross a network that can lose, duplicate and delay it?",
        story="The part opens with the eight fallacies of distributed computing, three outages matched to them, and "
              "the Job split into three services: over a network that loses 5% of messages and duplicates 2%, "
              "retries without keys count 'the' 2,924 times instead of 2,733. Birrell and Nelson's stubs make a "
              "remote call look local, and Waldo's four reasons say why it never is. The part then derives what "
              "goes on the wire: JSON's integers stop being exact at 2^53, and Protocol Buffers' varints, tags and "
              "zigzag are built byte by byte and checked against the published examples. Schema evolution is "
              "treated as subtyping, with seven changes checked for forward and backward compatibility. The centre "
              "of the part is delivery: at most once loses counts, at least once adds them, and at least once plus "
              "deduplication is exact, which a model checker confirms over every execution of two retried "
              "increments. From there it covers Hyrum's law, queues with visibility timeouts, backpressure and "
              "retry storms, the transactional outbox and sagas, load balancing by two choices, forged JWTs and "
              "clock pitfalls. It ends with the Job's counts staying exact under 20% loss with idempotency keys, "
              "and at the frontier: session types, TLA+ and verified distributed systems.",
        handoff="Part 44 measures what a change does to the people who use it, with controlled experiments. Part 45 "
                "runs services on rented machines that come and go. Part 46 turns the outbox into a stream, with "
                "logs and change data capture. Parts 48 and 49 design whole systems from these blocks, and Part 50 "
                "keeps them running with service-level objectives and error budgets.",
        outside="Binary and hexadecimal, HTTP's methods at the level of a first web course, and the exponential "
                "distribution for the queueing chapter.",
        objectives={
            "U": ["Encode an integer as a varint and a signed integer with zigzag, and decode a short protobuf "
                  "message by hand.",
                  "Explain why a request that got no reply cannot be told from one that was never received, and "
                  "what at most once and at least once each promise.",
                  "Say which HTTP methods are safe and which are idempotent, and what a repeated POST does."],
            "M": ["Prove in a model that retrying until acknowledged plus deduplication by id applies every "
                  "operation exactly once.",
                  "Decide whether a schema change is backward compatible, forward compatible, both or neither.",
                  "Compute the time in an M/M/1 queue against load, and what a bound on the queue trades for it."],
            "D": ["Explain how a multiparty session type projects a global protocol onto each service and what "
                  "it guarantees.",
                  "Compare what model checking, proof and deterministic simulation each establish about a "
                  "distributed protocol, and state what remains open."],
            "I": ["Design an endpoint that is safe to retry, with an idempotency key recorded atomically with "
                  "its effect.",
                  "Replace a dual write by a transactional outbox, and a distributed transaction by a saga with "
                  "compensations.",
                  "Choose retry backoff, jitter and a retry budget so that an outage does not become a retry "
                  "storm."],
        },
        results=[
            ("Varint and zigzag", r"\text{bytes}(n)=\max\bigl(1,\lceil \operatorname{bits}(n)/7\rceil\bigr),\qquad z(n)=(n\ll 1)\oplus(n\gg 63)"),
            ("Field tag", r"\text{tag}=(\text{field}\ll 3)\ \vert\ \text{wire type}"),
            ("Exactly once", r"\text{at least once}+\text{apply an id only once}\ \Rightarrow\ \text{each operation applied once}"),
            ("Hyrum's law", r"P(\text{someone relies on it})=1-(1-p)^N\ \ge \tfrac12\ \text{ at } N\approx 0.69/p"),
            ("M/M/1", r"T=\frac{1}{\mu(1-\rho)},\qquad \rho=\lambda/\mu<1"),
            ("Fan-out tail", r"P(\text{some of } k \text{ calls is in its slowest } 1\%)=1-0.99^{k}"),
        ],
        U=(0, 1, 2, 4, 5), D=(14,), I=(6, 7, 9, 11, 12),
        also=(("The API instruments", "explainer/cs/api"),),
    ),
    Part(
        n=44, level="U", widget="morninglooks", prereq=(20, 28, 42),
        question="How do you measure the people who use software, and when can you believe an experiment on them?",
        story="The part opens in San Francisco on 9 December 1968, with Engelbart's demonstration of the mouse, "
              "hypertext and shared editing. Its first half measures the person. Fitts's law comes out of Shannon's "
              "channel capacity, and a simulated hand that corrects its own errors falls on the line with R squared "
              "0.99; Hick and Hyman make a choice cost its entropy, and the keystroke-level model predicts a task's "
              "time from its operators. Perception has thresholds at 0.1, 1 and 10 seconds, and colour has "
              "formulas: sRGB's transfer curve, OKLab, and the WCAG contrast ratio, applied to the series' own "
              "palette, whose red and orange nearly coincide under deuteranopia. The second half measures the "
              "product. The A/B test is a randomized trial with a two-proportion z-test and a sample size of about "
              "16 sigma squared over delta squared per arm. The part turns on peeking: an A/A test checked every "
              "morning for a month declares a winner 28% of the time, and a mixture sequential test bounded by "
              "Ville's inequality repairs it. CUPED cuts variance by 1 minus rho squared, and the part ends with "
              "multiple metrics, sample-ratio mismatch, Simpson's paradox, bandits, and a marketplace where "
              "interference turns a measured +5.4 points into +0.2 at launch.",
        handoff="Parts 45 and 50 run experiments on infrastructure itself, as canaries and staged rollouts. Part 46 "
                "builds the pipelines that log every event these experiments analyse, and Part 47 ranks search "
                "results and measures whether the ranking helps. Part 51 draws glyphs and colour on the GPU, and "
                "Part 57 asks when what was measured on some people generalizes to the rest.",
        outside="Logarithms, and a first course in probability: the binomial and normal distributions, variance and "
                "correlation.",
        objectives={
            "U": ["Compute a target's index of difficulty and its predicted movement time from Fitts's law.",
                  "Compute the WCAG contrast ratio of two sRGB colours from their relative luminances.",
                  "Run a two-proportion z-test on an A/B test's counts and say what its p-value does and does not "
                  "mean."],
            "M": ["Derive the sample size per arm for a given lift, significance level and power.",
                  "Explain why stopping at the first p below 0.05 inflates the false-positive rate, and derive "
                  "the always-valid bound from Ville's inequality.",
                  "Derive CUPED's optimal coefficient and its variance reduction of 1 - rho^2."],
            "D": ["Explain why interference breaks the A/B estimate in a marketplace, and compare cluster and "
                  "switchback designs that repair it.",
                  "Derive the privacy parameter of Warner's randomized response and the accuracy it costs."],
            "I": ["Plan an experiment: the metric, the guardrails, the sample size and the stopping rule, fixed "
                  "before the first look.",
                  "Check a running test for sample-ratio mismatch and many-metric false discoveries before "
                  "reading its result.",
                  "Audit an interface for target size, contrast and colour-only encodings against WCAG 2.2."],
        },
        results=[
            ("Fitts's law", r"MT=a+b\log_2\!\bigl(\tfrac{D}{W}+1\bigr)"),
            ("Hick-Hyman", r"T=a+b\log_2(n+1)\ \text{for equal choices},\qquad T=a+bH\ \text{in general}"),
            ("Nielsen-Landauer", r"\text{found}(n)=1-(1-L)^n,\qquad L=0.31:\ 84\%\text{ at } n=5"),
            ("Sample size per arm", r"n=\frac{(z_{1-\alpha/2}+z_{1-\beta})^2\,2\sigma^2}{\delta^2}\approx\frac{16\sigma^2}{\delta^2}"),
            ("Always-valid test", r"P_0\Bigl(\sup_n \Lambda_n\ge \tfrac1\alpha\Bigr)\le\alpha\quad\text{for a martingale }\Lambda_n\ge 0,\ \mathbb{E}_0\Lambda_n=1"),
            ("CUPED", r"\theta^*=\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}X},\qquad \operatorname{Var}(Y-\theta^*X)=(1-\rho^2)\operatorname{Var}Y"),
        ],
        U=(0, 1, 2, 3, 4, 8), D=(13,), I=(6, 7, 11, 12),
        also=(("The HCI and experiment instruments", "explainer/cs/people"),),
    ),
    Part(
        n=45, level="U", widget="autoscalegain", prereq=(28, 31, 32, 38),
        question="What is under a computer rented by the second, and what decides how much of it to rent?",
        story="The part opens with McCarthy's 1961 forecast of computing as a public utility, which S3 and EC2 made "
              "real in 2006, and with the Job's bill: $0.00160 on one on-demand server, $0.00003 on sixteen "
              "functions. It then descends the hierarchy, where every layer is a scheduling problem and a failure "
              "domain. A warehouse-scale computer is limited by watts and fails about 1.8 servers a day in a fleet "
              "of 2,000; virtual machines shrink to Firecracker's microVMs, and containers are namespaces, cgroups "
              "and content-addressed layers. Kubernetes is a reconciliation loop, and a level-triggered controller "
              "recovers from lost events that leave an edge-triggered one a replica short for good. Scheduling is "
              "bin packing, NP-hard by way of partition, with first fit decreasing within 1% of the exact optimum "
              "on random instances and next fit provably within a factor of 2. The part turns on autoscaling as "
              "control: a proportional controller acting on a delayed measurement is stable only below a gain of "
              "2 cos(d pi / (2d + 1)), and Erlang C gives the square-root staffing behind the cloud's economy of "
              "scale. Object storage earns its nines from erasure coding and a Markov chain of failure and repair, "
              "and the part ends with networking, infrastructure as code, noisy neighbours, the price of spot "
              "capacity, and a frontier where correlated rack failures cut 13.3 nines to 7.",
        handoff="Part 46 builds logs, streams and warehouses on this infrastructure, and tables on its object "
                "store. Part 47 runs a search engine across thousands of machines. Parts 48 and 49 design whole "
                "systems from load balancers, caches and queues, Part 50 keeps them running with service-level "
                "objectives and capacity plans, and Part 60 opens the accelerators that now fill the datacentre.",
        outside="Exponential and Poisson distributions for the queueing and durability chapters; no cloud account "
                "or vendor knowledge is assumed.",
        objectives={
            "U": ["Name the layers from region to container and say what fails together at each.",
                  "Pack a list of containers by next fit, first fit and first fit decreasing, and compare each "
                  "with the lower bound from the total size.",
                  "Explain why a reconciliation loop that compares desired with observed state survives lost "
                  "events."],
            "M": ["Prove that next fit uses at most 2 OPT - 1 bins, and show by reduction from partition that bin "
                  "packing is NP-hard.",
                  "Derive the stability limit of a proportional autoscaler with a measurement delay.",
                  "Derive Erlang C from the M/M/c chain, and the mean time to data loss from the chain of "
                  "failure and repair."],
            "D": ["Compute how correlated rack failures change an erasure code's durability, and say which "
                  "independence assumption fails.",
                  "State what learning-augmented algorithms promise for online scheduling with predicted sizes "
                  "and lifetimes, and what is open."],
            "I": ["Choose between functions and servers from a request rate, and find the break-even rate.",
                  "Set a checkpoint interval for a job on spot capacity from the interruption rate and the "
                  "checkpoint's cost.",
                  "Read an infrastructure plan as a diff, and decide whether to apply or adopt a drifted "
                  "resource."],
        },
        results=[
            ("Packing guarantees", r"\mathrm{NF}\le 2\,\mathrm{OPT}-1,\qquad \mathrm{FFD}\le \tfrac{11}{9}\mathrm{OPT}+\tfrac{6}{9}"),
            ("Autoscaler stability", r"e_{t+1}=e_t-K e_{t-d}\ \text{ is stable iff }\ 0<K<2\cos\frac{d\pi}{2d+1}"),
            ("Erlang C", r"C(c,a)=\frac{c\,B_c}{c-a(1-B_c)},\qquad B_k=\frac{a\,B_{k-1}}{k+a\,B_{k-1}},\ B_0=1"),
            ("Square-root staffing", r"c\approx a+\beta\sqrt{a},\qquad a=\lambda/\mu"),
            ("Mean time to data loss", r"T_i=\frac{1+\mu T_{i-1}}{(n-i)\lambda},\qquad \mathrm{MTTDL}=\sum_{i=0}^{n-k}T_i"),
            ("Young's checkpoint rule", r"\tau\approx\sqrt{2C/\lambda}"),
        ],
        U=(0, 1, 3, 4, 5), D=(13,), I=(7, 9, 10, 11, 12),
        also=(("The cloud instruments", "explainer/cs/cloud"),),
    ),
    Part(
        n=46, level="U", widget="watermarklag", prereq=(20, 35, 39, 43),
        question="How do you compute answers over data that never stops arriving, and arrives late, out of order and twice?",
        story="The part opens with the log, the structure the series keeps meeting as the write-ahead log, the Raft "
              "log, git's history and the outbox: four sources and four consumers need sixteen pipelines pairwise "
              "and eight connections through a log. Kafka's partitioned log keeps order per key, shares partitions "
              "among a consumer group, and compacts 2,000 updates to the 50 records that rebuild the same state. "
              "Change data capture turns a database's own log into a stream, and state becomes a fold over events. "
              "The part turns on time. Events carry the time they happened and arrive when they arrive; windows "
              "are cut in event time, and a watermark guesses when a window is complete. On 3,000 events, no lag "
              "drops 530 of them and a minute's lag drops one but answers 65 seconds late, while allowed lateness "
              "keeps the early answer and refines it. Barrier snapshots make a crashed counter's state exact, and "
              "sketches bound the memory of top-k, distinct counts and quantiles. The second half is the "
              "warehouse: star schemas, Parquet's encodings measured on the novels' words, Dremel's repetition and "
              "definition levels, tables on object storage, and joins across a hundred workers. The Job ends as a "
              "live top twenty over thirty novels, equal to the batch answer exactly once.",
        handoff="Part 47 builds a search index from a log of documents and keeps it current. Parts 48 and 49 design "
                "feeds, timelines and analytics systems from these pieces, and Part 50 turns logs, metrics and "
                "traces on the running system itself. Part 57 asks what can be learned from data at this scale, "
                "and Part 55 what it takes to trust the pipeline that delivered it.",
        outside="SQL at the level of a join and a GROUP BY; the exponential distribution for the delay model.",
        objectives={
            "U": ["Explain how keys, partitions and offsets give order per key and let each consumer read at its "
                  "own pace.",
                  "Assign events to tumbling, sliding and session windows by event time, and say what a watermark "
                  "claims.",
                  "Encode a small column with a dictionary, run lengths and deltas, and say why sorting helps."],
            "M": ["Trade completeness against latency with a watermark's lag, and use allowed lateness and "
                  "refinements to escape the trade.",
                  "Explain how barrier snapshots give exactly-once state, and why the guarantee is end to end.",
                  "Compute Dremel's repetition and definition levels for a nested column and rebuild the records "
                  "from them."],
            "D": ["Explain what incremental view maintenance by differential dataflow and DBSP computes, and at "
                  "what cost in state.",
                  "State the space lower bounds for streaming summaries and where KLL sits against them."],
            "I": ["Choose between a broadcast and a shuffle join from the table sizes, and repair a skewed key by "
                  "salting.",
                  "Size batches, partitions and retention for a throughput target on sequential storage.",
                  "Write data tests and a contract for a stream with duplicates and late arrivals."],
        },
        results=[
            ("Why a log", r"m\text{ sources},\ n\text{ consumers}:\quad mn\ \text{pipelines pairwise},\quad m+n\ \text{through a log}"),
            ("State is a fold", r"s_n=\operatorname{apply}(s_{n-1},e_n),\qquad \text{compaction keeps the last record of each key}"),
            ("Watermark", r"W(t)=\max\{\text{event time seen by } t\}-\text{lag};\quad [a,b)\ \text{fires when } W(t)\ge b"),
            ("Misra-Gries", r"f_x-\tfrac{n}{k}\ \le\ \hat f_x\ \le\ f_x\qquad\text{with } k-1 \text{ counters}"),
            ("Dremel levels", r"r=\text{depth at which the value repeats},\quad d=\#\text{optional or repeated fields present}"),
            ("Join crossover", r"SN=(B+S)\bigl(1-\tfrac1N\bigr)\ \Rightarrow\ S^*=\frac{B(N-1)}{N^2-N+1}\approx\frac{B}{N}"),
        ],
        U=(0, 1, 3, 4, 7, 8), D=(14,), I=(2, 10, 12),
        also=(("The data instruments", "explainer/cs/data"),),
    ),
    Part(
        n=47, level="U", widget="gapcodes", prereq=(16, 18, 20, 39),
        question="How do you find the ten most relevant passages among billions in a fifth of a second?",
        story="The part opens with the history of finding things, from Archie's file names in 1990 through "
              "AltaVista to Google's links as votes, and with its own engine: 11,261 passages of the thirty novels, "
              "40,692 terms, 2,364,691 postings. Words are tokenized and stemmed by Porter's rules, and their counts "
              "follow Zipf's and Heaps' laws. The inverted index turns a query into a merge of sorted lists, where "
              "skip pointers and galloping search cut the comparisons for 'the AND whale' from 11,137 to 1,418. "
              "Stored as gaps, postings shrink from 32 bits to 4.96 under Rice codes, within 5% of the counting "
              "bound. Ranking is derived from the probability ranking principle through the binary independence "
              "model to BM25, and judged with average precision and nDCG on nine queries, which a sign test shows "
              "are too few to separate BM25 from tf-idf. WAND returns the same top ten while scoring as few as a "
              "tenth of the candidates. The part then adds what the web needs: PageRank as a Markov chain's stationary "
              "distribution, a link farm that lifts its target from 346th to 114th, crawling with SimHash, sharded "
              "serving, spelling correction, learning to rank, and dense retrieval with product quantization and "
              "HNSW. It ends at the frontier: graph search without a recall guarantee, learned sparse retrieval, "
              "and retrieval for models that write.",
        handoff="Parts 48 and 49 design a search service: how to shard it, cache it and keep it fresh. Part 50 "
                "keeps a serving system like it healthy. Part 56 returns to the eigenvectors behind PageRank with "
                "spectral graph theory, Part 57 asks when a learned ranker will generalize, and Part 60 looks at "
                "the hardware built for vector search and inference.",
        outside="Logarithms, and probability at the level of Bayes' rule and a geometric distribution; the "
                "eigenvector view of a Markov chain helps for PageRank.",
        objectives={
            "U": ["Build an inverted index for a few documents by hand and answer an AND query by merging "
                  "postings.",
                  "Compute precision, recall and nDCG at k for a ranked list with graded judgments.",
                  "Run two steps of PageRank's power iteration on a small graph, including a page without "
                  "links."],
            "M": ["Derive the lengths of Elias gamma codes and the Golomb parameter for geometric gaps, and "
                  "compare a list's size with the bound log2 C(N, f).",
                  "Derive BM25 from the binary independence model, and explain what k1 and b control.",
                  "Explain why WAND's pivot rule never loses a top-k document."],
            "D": ["Explain why graph-based nearest-neighbour search has no worst-case recall guarantee, and what "
                  "locality-sensitive hashing guarantees in its place.",
                  "State what is open in evaluating retrieval for generated answers."],
            "I": ["Choose between document- and term-partitioned indexes, and use hedged requests against the "
                  "tail of a fan-out.",
                  "Build a judged query set and decide with a significance test whether a ranking change is an "
                  "improvement.",
                  "Combine lexical and dense retrieval, with compressed codes for the shortlist and exact "
                  "vectors for re-ranking."],
        },
        results=[
            ("Zipf and Heaps", r"f(r)\propto r^{-s},\qquad V(n)=K\,n^{\beta}\quad(s\approx 1.21,\ \beta\approx 0.485\text{ on the novels})"),
            ("Gap codes", r"|\gamma(g)|=2\lfloor\log_2 g\rfloor+1,\qquad M_{\text{Golomb}}\approx 0.69\,\tfrac{N}{f}"),
            ("BM25", r"\sum_{t\in q}\operatorname{idf}_t\,\frac{tf_t\,(k_1+1)}{tf_t+k_1\bigl(1-b+b\,\ell_d/\bar\ell\bigr)}"),
            ("nDCG", r"\mathrm{DCG}_k=\sum_{i=1}^{k}\frac{2^{g_i}-1}{\log_2(i+1)},\qquad \mathrm{nDCG}_k=\frac{\mathrm{DCG}_k}{\mathrm{IDCG}_k}"),
            ("PageRank", r"r=\frac{1-d}{N}\mathbf{1}+d\,P\,r,\qquad d=0.85"),
            ("Freshness", r"\text{fresh fraction}=\frac{1-e^{-\lambda I}}{\lambda I}"),
        ],
        U=(0, 1, 2, 3, 6, 8), D=(15,), I=(9, 10, 12, 14),
        also=(("The search instruments", "explainer/cs/search"),),
    ),
]
