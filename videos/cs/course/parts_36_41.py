"""Act VII, Many Machines, and the start of Act VIII, Building Software: networks, agreement, scale, engineering (Parts 36-41)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=36, level="U", widget="alohaload", prereq=(17, 18, 28),
        question="How does a message cross a network that nobody owns, and what limits it at each layer?",
        story="The part opens with one datagram, 'Call me Ishmael.', sent from a Pebble in San Francisco to one in "
              "Frankfurt: 16 bytes become a 64-byte frame, and the ping takes the 108 ms that light needs in 11,020 "
              "km of fibre. The telephone network reserved a circuit for every call; Baran and Davies cut messages "
              "into packets that share links, and the Internet stacks that idea in five layers with IP at the waist. "
              "The part then climbs the layers and derives what limits each: Shannon's capacity under QAM, bit "
              "stuffing and CRC-32 for frames, ALOHA's throughput G e^(-2G) with its peak of 1/2e, Ethernet's "
              "backoff, and Perlman's spanning tree against a broadcast storm. At the network layer it builds "
              "longest-prefix match with tries, distance vector with its count to infinity, link state with its "
              "transient loops, and BGP, where an equal-prefix hijack takes 50 of 125 systems and a sub-prefix "
              "hijack all of them. It assembles these into its own internet of eight cities with ping and "
              "traceroute, adds fading, OFDM and MIMO for wireless, and ends at the frontier: a verifier that finds "
              "a forwarding loop from the tables alone, and BAD GADGET, a set of BGP policies that never converges.",
        handoff="Part 37 builds TCP on these lossy packets, and congestion control that keeps the network from "
                "collapsing as ALOHA does. Part 38 makes machines agree over a network that delays and drops "
                "messages, and Part 39 replicates data across its latencies. Part 42 puts HTTP and the browser on "
                "top, and Part 45 rents networks in the cloud.",
        outside="Binary and hexadecimal, logarithms, the exponential and Poisson distributions at the level of a "
                "first probability course.",
        objectives={
            "U": ["Trace a datagram through the five layers, naming each header and which addresses change at "
                  "every hop.",
                  "Derive pure ALOHA's throughput G e^(-2G) and slotted ALOHA's G e^(-G), with their maxima.",
                  "Run distance vector by hand on a small graph, and show the count to infinity after a cut."],
            "M": ["Compute a channel's Shannon capacity and the gap between a QAM constellation and the limit.",
                  "Build longest-prefix match with a binary and a multibit trie and count the memory reads.",
                  "Explain why link-state routers that update at different times can loop, and find the loop."],
            "D": ["State the stable paths problem, show that BAD GADGET has no stable solution, and say what "
                  "Gao-Rexford policies guarantee.",
                  "Find an order of router updates after a link failure under which no packet loops, and state "
                  "what is known about the fewest rounds."],
            "I": ["Plan addresses with CIDR, and diagnose a path with ping, traceroute and a packet capture.",
                  "Explain how a prefix hijack spreads, and what route-origin validation stops and does not stop."],
        },
        results=[
            ("Shannon's capacity", r"C = B\log_2\!\bigl(1+\tfrac{S}{N}\bigr)"),
            ("ALOHA", r"S_{\text{pure}} = G e^{-2G}\le \tfrac{1}{2e},\qquad S_{\text{slotted}} = G e^{-G}\le \tfrac1e"),
            ("What a CRC catches", r"g(x)\nmid x^{i}B(x)\ \text{ when } \deg B<\deg g,\ B(0)=g(0)=1"),
            ("Distance vector", r"D_x(y)=\min_{v}\bigl\{c(x,v)+D_v(y)\bigr\},\quad \text{exact after } n-1 \text{ rounds}"),
            ("Head-of-line blocking", r"\text{input-queued throughput}\ \to\ 2-\sqrt2\approx 0.586"),
            ("MIMO capacity", r"C=\mathbb{E}\log_2\det\bigl(I+\tfrac{\mathrm{SNR}}{n}HH^{*}\bigr)"),
        ],
        U=(0, 1, 2, 4, 5, 6, 7, 9, 10), D=(15,), I=(11, 12),
        also=(("The network instruments", "explainer/cs/net"),),
    ),
    Part(
        n=37, level="U", widget="aimdzigzag", prereq=(22, 30, 36),
        question="How do you build a reliable conversation, shared fairly, on a network that loses packets?",
        story="The part opens with the Job's novels, 24,971,555 bytes, sent from Frankfurt to San Francisco over a "
              "link that loses one packet in 1,000: Reno takes 34.9 s, CUBIC 24.2 s, BBR 3.2 s. It builds "
              "reliability from nothing: stop-and-wait, the alternating bit, Go-Back-N and Selective Repeat, with "
              "the theorem on how many sequence numbers a window needs tested at its edge. TCP adds the handshake, "
              "SYN cookies, flow control and a timer that learns the round trip. Then the part turns to October "
              "1986, when the link from the Lawrence Berkeley Laboratory to UC Berkeley fell from 32 kb/s to 40 b/s, reproduces the "
              "collapse with fixed windows, and applies Jacobson's cure. Chiu and Jain's phase plane shows why the "
              "cure is additive increase with multiplicative decrease, one tooth of the sawtooth gives the Mathis "
              "formula, and Kelly's theorem reads the whole of it as dual ascent on link prices. Queues, "
              "bufferbloat, CoDel, CUBIC and BBR follow, then DNS, HTTP/2 against QUIC, and caches under Zipf's "
              "law. It ends with the novels fetched over the series' own TCP, ledger row 14, and with the 2022 "
              "starvation theorem: low delay, a full link and fairness under jitter cannot all be had.",
        handoff="Part 38 asks machines to agree over this network, where a timeout cannot tell a dead machine from "
                "a slow one, and Part 39 replicates data across its round trips. Part 42 builds the browser on QUIC "
                "and TLS, Part 45 rents load balancers and content networks, and retries, backoff and CoDel's idea "
                "return inside large services in Parts 49 and 50.",
        outside="Geometric series, expectations, and Lagrange multipliers for the chapter on optimization.",
        objectives={
            "U": ["Trace stop-and-wait, Go-Back-N and Selective Repeat through a loss, and compute their "
                  "utilization.",
                  "Explain the three-way handshake, flow control and the congestion window, and why the 1986 "
                  "collapse happened.",
                  "Retell Chiu and Jain's four-line proof that AIMD converges to equal shares."],
            "M": ["Prove that Go-Back-N needs a window below the sequence space and Selective Repeat at most half "
                  "of it.",
                  "Derive the Mathis formula from one tooth of the sawtooth, and the retransmission timer from "
                  "SRTT and RTTVAR.",
                  "Solve a small network utility maximization by dual ascent and read the prices."],
            "D": ["State the starvation theorem for delay-convergent congestion control and explain the role of "
                  "non-congestive delay.",
                  "Measure the delay a rule must accept to stay fair under ACK jitter, and say which part of that "
                  "trade-off is open."],
            "I": ["Size socket buffers to a bandwidth-delay product, and choose between CUBIC and BBR on a lossy "
                  "long path.",
                  "Diagnose bufferbloat and cure it with CoDel, and choose DNS TTLs and cache sizes on purpose."],
        },
        results=[
            ("Stop-and-wait", r"U=\frac{L/R}{\mathrm{RTT}+L/R}"),
            ("Sequence space", r"\text{Go-Back-N: } W\le S-1,\qquad \text{Selective Repeat: } W\le S/2"),
            ("The timer", r"\mathrm{RTO}=\mathrm{SRTT}+4\cdot\mathrm{RTTVAR}"),
            ("AIMD is fair", r"x_1-x_2\ \mapsto\ b^{k}(x_1-x_2)\to 0 \quad\text{after } k \text{ decreases}"),
            ("The Mathis formula", r"\text{rate}\approx\frac{\mathrm{MSS}}{\mathrm{RTT}}\sqrt{\frac{3}{2p}}"),
            ("Kelly's problem", r"\max\sum_r \log x_r\ \text{ s.t. }\sum_{r\ni l}x_r\le c_l;\quad x_r=\frac{1}{\sum_{l\in r}p_l}"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7, 12), D=(16,), I=(9, 10, 13, 14),
        also=(("Congestion control's theory", "explainer/cs/net/cc.py"), ("The TCP simulator", "explainer/cs/net/tcp.py")),
    ),
    Part(
        n=38, level="U", widget="raftsplitvote", prereq=(33, 36, 37),
        question="How can machines agree on anything when messages are lost and a slow machine looks like a dead one?",
        story="The part opens with five Pebbles running Raft for nine seconds through a crashed leader, a partition "
              "and a restart: 236 commands committed in 15 terms, every invariant holding. It then starts from "
              "nothing. The two generals can never be certain over a lossy link, and without a shared clock the "
              "order of events is a definition: Lamport's clocks respect causality, vector clocks characterize it, "
              "and Chandy and Lamport's markers photograph a bank that never stops. With synchronized rounds, "
              "FloodSet reaches consensus in f + 1 rounds and no fewer, checked against every crash pattern. Then "
              "the part turns: Fischer, Lynch and Paterson prove that with unbounded delays no deterministic "
              "protocol can guarantee a decision if one process may crash, and an exhaustive explorer shows the "
              "bivalent configurations of two tiny protocols. Coins, failure detectors and partial synchrony are "
              "the ways around, and Paxos and Raft take the last: always safe because majorities intersect, live "
              "when the network behaves. The series' Raft survives a thousand storms while three planted bugs are "
              "caught. It ends with traitors, 3f + 1, PBFT and Nakamoto's chain of work, and with what is known "
              "about proving and breaking such protocols.",
        handoff="Part 39 replicates data at scale with quorums, two-phase commit and Spanner's clocks, and runs the "
                "Job on sixteen Pebbles. Raft returns as etcd under Kubernetes in Part 45, Chandy and Lamport's "
                "snapshots as stream checkpoints in Part 46, and TLA+ and proofs of protocols in Part 54.",
        outside="Proof by induction and by contradiction; elementary probability for the randomized protocols.",
        objectives={
            "U": ["Explain why the two generals cannot agree, and why a timeout cannot tell a crash from a delay.",
                  "Stamp a space-time diagram with Lamport and vector clocks and read off which events are "
                  "concurrent.",
                  "Trace a Raft election and a log replication, and say why two majorities always share a server."],
            "M": ["Prove that vector clocks characterize happened-before, and that a Chandy-Lamport snapshot is a "
                  "consistent cut.",
                  "Walk through the FLP proof: a bivalent initial configuration, and a step that keeps it bivalent.",
                  "Prove Paxos's safety invariant by induction on ballots, and Raft's leader completeness."],
            "D": ["State the lower bounds on agreement (f + 1 rounds, FLP, 3f + 1, Dolev-Reischuk's quadratic "
                  "messages) and which protocols meet them.",
                  "Design a fault-injection strategy that exposes a deep protocol bug, and say why no theory yet "
                  "bounds the runs it needs."],
            "I": ["Choose the number of voters and the election timeouts of an etcd or ZooKeeper cluster, and "
                  "explain why four voters tolerate no more than three.",
                  "Protect a lock with a fencing token, and test a replicated system with injected faults."],
        },
        results=[
            ("Vector clocks", r"a\to b\iff V(a)<V(b)"),
            ("Synchronous crash consensus", r"f+1 \text{ rounds are sufficient and necessary}"),
            ("FLP", r"\text{asynchronous, one crash}\ \Rightarrow\ \text{no deterministic consensus}"),
            ("Majorities intersect", r"|Q_1|,|Q_2|>\tfrac n2\ \Rightarrow\ Q_1\cap Q_2\neq\varnothing"),
            ("Byzantine agreement", r"n\ge 3f+1 \quad\text{(without signatures)}"),
            ("Nakamoto's race", r"P=1-\sum_{k=0}^{z}\frac{\lambda^{k}e^{-\lambda}}{k!}\Bigl(1-\bigl(\tfrac qp\bigr)^{z-k}\Bigr),\ \lambda=\tfrac{zq}{p}"),
        ],
        U=(0, 1, 2, 3, 7), D=(11,), I=(8,),
        also=(("The series' Raft", "explainer/cs/dist/raft.py"), ("Consensus explorers", "explainer/cs/dist/consensus.py")),
    ),
    Part(
        n=39, level="U", widget="quorumoverlap", prereq=(20, 37, 38),
        question="What does each guarantee cost when data lives on many machines, and one of them is always failing?",
        story="The part opens with the Job run as MapReduce on sixteen Pebbles: Pebble 4 crashes at 0.4 s, three "
              "finished maps are redone, and the same top twenty words come out in 0.60 s against 2.65 s on one "
              "machine. It then prices the guarantees one at a time. Replicas lag, so 67% of immediate reads miss "
              "your own post; quorums with R + W > N never do, and sloppier ones are stale for a measured while. "
              "CAP is stated precisely on a 40/60 partition: refuse 40% of requests, or answer all of them and "
              "merge conflicts later. CRDTs make the merge a join that cannot conflict, a hash ring moves 8.6% of "
              "keys where modulo hashing moves 91%, and Chord finds a key in about half of log n hops. Two-phase "
              "commit blocks for 31 s behind a crashed coordinator, and Spanner waits out its clock uncertainty "
              "instead. Then the part turns from correctness to time: one slow server in a hundred makes 63.9% of "
              "requests slow at a fan-out of 100, hedging and two choices repair it, and a retry storm keeps a "
              "service down after its spike has passed. It ends by asking how little coordination a problem "
              "needs: the CALM theorem, and causal consistency as the most an always-available system can promise.",
        handoff="CRDTs return in version control and local-first web apps (Parts 41 and 42). Part 46 builds "
                "streams with watermarks and query engines that shuffle like MapReduce, Parts 48 and 49 design "
                "systems with sharding, hot keys and fencing tokens, and Part 50 cures metastable failures with "
                "load shedding and retry budgets.",
        outside="Elementary probability (independent events, the exponential distribution), hashing, and partial "
                "orders for the chapter on CRDTs.",
        objectives={
            "U": ["Decide from N, R and W whether a read can miss an acknowledged write, and explain why.",
                  "State the CAP theorem precisely and say what a CP and an AP system each do during a partition.",
                  "Place keys on a consistent-hash ring and count how many move when a node joins."],
            "M": ["Prove that replicas whose merge is commutative, associative and idempotent converge, and build "
                  "a G-counter and an OR-set.",
                  "Show where two-phase commit blocks, and compute Spanner's commit wait from the clock "
                  "uncertainty.",
                  "Derive the slow share 1 - (1 - p)^n of a fan-out and the effect of a hedged request."],
            "D": ["State the CALM theorem and use invariant confluence to decide which invariants of an "
                  "application need coordination.",
                  "Explain why causal consistency is the strongest always-available convergent model, and what "
                  "is open about its metadata and about metastable failures."],
            "I": ["Choose a consistency level as a product decision, naming the anomalies a user may see.",
                  "Watch the 99th percentile, hedge reads that are safe to repeat, and give every request a "
                  "deadline, backoff with jitter and a retry budget."],
        },
        results=[
            ("Quorums", r"R+W>N\ \Rightarrow\ \text{every read quorum meets every write quorum}"),
            ("CRDT merge", r"x\sqcup y=y\sqcup x,\quad (x\sqcup y)\sqcup z=x\sqcup(y\sqcup z),\quad x\sqcup x=x"),
            ("Consistent hashing", r"\text{keys moved by node } n+1:\ \tfrac{1}{n+1}\ \text{ (modulo: } \tfrac{n}{n+1})"),
            ("Chord", r"\text{hops}\approx\tfrac12\log_2 n+1"),
            ("Spanner's commit wait", r"\text{wait until } \mathrm{TT.now().earliest}>s:\ \text{about } 2\varepsilon"),
            ("The tail at scale", r"P(\text{slow})=1-(1-p)^{n},\qquad 1-0.99^{100}\approx 0.634"),
        ],
        U=(0, 1, 2, 4, 6), D=(9,), I=(7, 8),
        also=(("Quorums, CRDTs, hashing, tails", "explainer/cs/dist/scale.py"), ("The Job as MapReduce", "explainer/cs/dist/mapreduce.py")),
    ),
    Part(
        n=40, level="U", widget="brookslate", prereq=(14, 15, 31),
        question="Why does software that a thousand people change every day fail differently from a weekend's program?",
        story="The part opens at Garmisch in October 1968, where the NATO conference named the software crisis, and "
              "with the software on screen: this repository, 2,587 Python modules and 5,564 imports, with 5 import "
              "cycles and 2 imports against its layering. Parnas's keyword-in-context index is built twice, and "
              "one change touches three of five modules in the flowchart decomposition and one of six when each "
              "module hides a decision. Abstract types, contracts and Liskov's rule follow, with a Square that "
              "fails Rectangle's property on the first random trial. The repository's coupling is measured, SOLID "
              "and six patterns are stated with counterexamples, and then the part tests the tests: eight flaky "
              "tests turn 82% of runs red, a fuzzer crashes the Pebble assembler at 24 sites, and a suite that "
              "covers 77% of the statements kills only 62% of the mutants. The second half is about people and "
              "time: technical debt as a model, merge conflicts against integration interval, work in progress "
              "under Little's law, Conway's law, Brooks' law simulated with its condition, and estimates whose "
              "plan of medians is met 12% of the time. It ends with the profession's failures, Horizon and the "
              "737 MAX, and with what evidence the field has, including models that write code.",
        handoff="Part 41 turns this part's dependency graphs into machines: version control and build systems. "
                "Part 43 designs the interfaces between services and the teams behind them, Part 44 delivers "
                "software continuously and measures it, Part 50 handles incidents, and Part 54 replaces tests "
                "with proofs where proofs are affordable.",
        outside="The ability to read Python, and experience of writing a program of a few hundred lines.",
        objectives={
            "U": ["Name the decision each module of a design hides, and predict which modules a given change "
                  "touches.",
                  "State a representation invariant and a contract, and show why Square is not a behavioural "
                  "subtype of Rectangle.",
                  "Explain why a test can pass alone and fail in a suite, and what a mutation score measures "
                  "that coverage does not."],
            "M": ["Compute afferent and efferent coupling and instability on an import graph, and find its "
                  "cycles.",
                  "Bisect a test order to find a polluter, and run mutation testing on a module.",
                  "Simulate Brooks' law and a schedule of lognormal tasks, and read the tail."],
            "D": ["Explain the oracle problem for machine-written patches, and why passing tests is an "
                  "incomplete criterion.",
                  "Propose a score for a test suite that predicts whether an accepted patch is correct, and "
                  "validate it on mutants."],
            "I": ["Write a design document, keep changes small enough to review, and fix flaky tests rather "
                  "than retry them.",
                  "Limit work in progress, integrate daily, and estimate in ranges with a stated confidence.",
                  "Read the DORA metrics without turning them into targets."],
        },
        results=[
            ("Brooks' channels", r"n \text{ people}\ \Rightarrow\ \tfrac{n(n-1)}{2} \text{ channels}"),
            ("Little's law", r"L=\lambda W:\quad \text{work in progress}=\text{throughput}\times\text{time in progress}"),
            ("Instability", r"I=\frac{C_e}{C_a+C_e}"),
            ("Behavioural subtyping", r"S<:T\ \Rightarrow\ \bigl(\forall x{:}T.\ \varphi(x)\bigr)\Rightarrow\bigl(\forall y{:}S.\ \varphi(y)\bigr)"),
            ("Mutation score", r"\frac{\text{mutants killed}}{\text{mutants}}=62\%\ \text{ under } 77\%\ \text{statement coverage}"),
            ("A lognormal task", r"\text{mean}=\text{median}\cdot e^{\sigma^{2}/2}\ >\ \text{median}"),
        ],
        U=(0, 1, 2, 4, 5, 11), D=(12,), I=(7, 8, 9, 10),
        also=(("Software-engineering instruments", "explainer/cs/se"),),
    ),
    Part(
        n=41, level="U", widget="queuebisect", prereq=(21, 26, 29, 40),
        question="What happens to a change between the keyboard and production, and why can each step be trusted?",
        story="The part opens in April 2005, when BitKeeper's licence was withdrawn and Torvalds wrote git within "
              "days, and with the series' own object store giving three files, their tree and their commit "
              "the same names as git 2.43. Names are hashes of content, so history is a Merkle graph: editing one "
              "file renames only the objects on its path, and a flipped bit is caught by rehashing. Merge bases, "
              "three-way merge over Myers' diff, rebase and bisection follow, then deltas that store forty "
              "versions of the syllabus in 154 KB instead of 4.2 MB. The second machine is the build system: make "
              "trusts clocks and rebuilds all 202 targets after a fresh checkout, a build that hashes its inputs "
              "rebuilds none and stops early after a comment edit, and a clean build has work 235 s and span 34 s. "
              "The third is the package manager, and here the part turns: choosing versions is NP-complete, by a "
              "reduction from 3-SAT shown as packages, so resolvers are SAT solvers. Above the three, a merge "
              "queue tests batches and bisects failures, and a canary needs 100,000 requests to catch a doubled "
              "0.1% error rate reliably. It ends at the frontier of structured merge, build correctness and "
              "authors that are programs.",
        handoff="Part 42's browser caches assets by content hash, Part 43 versions the interfaces between "
                "services, and Part 44 turns canaries into experiments with proper statistics. Part 50 releases "
                "and rolls back during incidents, and Parts 55 and 61 return to the supply chain and to whether a "
                "compiler can be trusted.",
        outside="Everyday use of a version-control system and a compiler; graphs and binary search.",
        objectives={
            "U": ["Compute a git object id by hand from its header and content, and say which objects one edit "
                  "renames.",
                  "Find the merge base of two commits, perform a three-way merge, and bisect a history.",
                  "Explain why a build driven by timestamps rebuilds too much or too little, and what early "
                  "cutoff saves."],
            "M": ["Classify a build system by its scheduler and its rebuilder, and bound a parallel build by its "
                  "work and span.",
                  "Reduce 3-SAT to package installability, and encode a dependency diamond as clauses.",
                  "Compute the test runs a merge queue needs per change and the power of a canary test."],
            "D": ["State what structured merge, build minimality and complete version solving each leave "
                  "unsolved.",
                  "Design a merge-queue policy for changes with individual failure probabilities and argue for "
                  "its batch sizes and bisection order."],
            "I": ["Make a build hermetic and cached, commit lockfiles, and verify what a dependency update "
                  "brings in.",
                  "Deliver through a merge queue, a canary, feature flags and expand-contract migrations, and "
                  "choose between rolling back and rolling forward."],
        },
        results=[
            ("A git object's name", r"\mathrm{id}=\operatorname{SHA1}\bigl(\text{kind}\ \text{size}\ \backslash 0\ \text{content}\bigr)"),
            ("Bisection", r"\lceil\log_2 n\rceil \text{ tests}:\quad 10^{3}\to 10,\quad 10^{6}\to 20"),
            ("Brent's bound", r"\max\bigl(\tfrac{W}{P},S\bigr)\ \le\ T_P\ \le\ \tfrac{W}{P}+S"),
            ("Version resolution", r"\text{3-SAT}\ \le_p\ \text{INSTALLABLE}\ \Rightarrow\ \text{NP-complete}"),
            ("A merge queue's batch", r"P(\text{batch of } b \text{ is green})=(1-p)^{b}"),
        ],
        U=(0, 1, 2, 4), D=(8,), I=(6, 7),
        also=(("The git object store", "explainer/cs/vcs/git.py"), ("The build engine", "explainer/cs/vcs/build.py"),
              ("The version solver", "explainer/cs/vcs/deps.py")),
    ),
]
