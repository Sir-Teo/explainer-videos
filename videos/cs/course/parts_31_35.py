"""Act VI, One Machine, Many Programs (the kernel, virtual memory, concurrency, storage), and databases (Parts 31-35)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=31, level="U", widget="queuehockey", prereq=(6, 10, 11, 13),
        question="How can one processor run many programs at once, safely, and why does a busy one feel so slow?",
        story="The part opens with one user who thinks for 10 seconds and computes for half a second, so the "
              "processor idles 95% of the time, and with PebbleOS booting and two processes printing interleaved "
              "letters. Time-sharing, from CTSS to Unix, needs three protections: Pebble gains a mode bit, "
              "privileged instructions, control registers and a timer, and a hostile halt, a wild store and a "
              "processor hog are each stopped. The trap, the process control block, the context switch and "
              "fork, exec and wait are traced in PebbleOS and measured on this machine. Scheduling follows: the "
              "convoy under FCFS, shortest-job-first by an exchange argument, round robin and its quantum, "
              "Corbato's multi-level feedback queue and how to game it, lottery, stride and CFS, work stealing, "
              "and the real-time bound of Liu and Layland with Mars Pathfinder's priority inversion. The part "
              "turns to queueing theory, where Little's law, M/M/1 and Pollaczek-Khinchine explain why response "
              "time explodes near full load and grows with the variance of the job size. It ends with PebbleOS, a "
              "kernel of 284 instructions, running the Job as two processes joined by a pipe: ledger row 11, 2.17 "
              "seconds against 0.81 bare.",
        handoff="Part 32 gives every process its own addresses, which makes fork cheap, and Part 33 deals with the "
                "races that preemption creates. Part 34 adds a disk to PebbleOS. Little's law returns for work in "
                "progress in Part 40 and for queues between services in Part 43, and Parts 45 and 50 plan capacity "
                "with queueing theory. The verified kernels of the Frontier chapter return in Part 54.",
        outside="Programming in C or a similar language; means, variances and the exponential distribution for "
                "the queueing chapter.",
        objectives={
            "U": ["Trace a system call through the trap, the kernel's dispatch and the return, and say what the "
                  "mode bit, the bounds check and the timer each protect.",
                  "Draw the Gantt chart of a small workload under FCFS, SJF, SRTF and round robin, and compute its "
                  "mean turnaround and response times.",
                  "Describe a process's states and what a context switch saves."],
            "M": ["Prove by an exchange argument that shortest-job-first minimizes mean turnaround, and state "
                  "the rules of the multi-level feedback queue and the rule that stops gaming.",
                  "Test a periodic task set against the Liu-Layland bound and by response-time analysis, and "
                  "explain why EDF schedules what rate-monotonic priorities miss.",
                  "Derive the M/M/1 response time, and apply Little's law and Pollaczek-Khinchine to a server."],
            "D": ["Explain what the proofs of seL4, CertiKOS and Hyperkernel establish and what they assume.",
                  "Compare a queue per core, one central queue and preemptive quanta for the 99.9th percentile "
                  "of short requests, and state the open problem of the best quantum under switching overhead."],
            "I": ["Read a system's cost in system calls and context switches with strace-style counts, and "
                  "choose a buffer size from the measured cost per call.",
                  "Size a server from its load and job-size variance, and say why running near full utilization "
                  "trades throughput for latency.",
                  "Compare monolithic kernels, microkernels, exokernels and unikernels by what runs in kernel "
                  "mode."],
        },
        results=[
            ("Interactive response time", r"R=\frac{N}{X}-Z,\qquad N^*=\frac{S+Z}{S}"),
            ("Liu-Layland bound", r"\sum_{i=1}^{n}\frac{C_i}{T_i}\le n\bigl(2^{1/n}-1\bigr)\ \to\ \ln 2"),
            ("Little's law", r"L=\lambda W"),
            ("M/M/1", r"E[T]=\frac{1}{\mu-\lambda},\qquad P(T>x)=e^{-(\mu-\lambda)x}"),
            ("Pollaczek-Khinchine", r"E[T]=E[S]+\frac{\lambda\,E[S^2]}{2(1-\rho)},\qquad \rho=\lambda E[S]"),
            ("Work stealing", r"T_P\approx \frac{T_1}{P}+T_\infty"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 14), D=(15,), I=(13,),
        also=(("The scheduler and queue simulators", "explainer/cs/os/sched.py"),
              ("PebbleOS", "explainer/cs/os/kernel.py")),
    ),
    Part(
        n=32, level="U", widget="beladyframes", prereq=(9, 11, 31),
        question="How does every program get a huge private memory when the machine has only one, and a finite one?",
        story="Two PebbleOS processes store their pid at the same virtual address, 0x405004, and each reads back its "
              "own: the two stores went to different physical addresses. The part builds the machinery behind that. "
              "Base and bounds and segments relocate and protect but fragment memory; paging cuts both spaces into "
              "equal pages, and the page table becomes a radix tree that the hardware walks and the TLB caches, "
              "measured on this machine as a staircase. Because memory is finite some page must leave: Belady's OPT "
              "is proved optimal by an exchange argument, FIFO on Belady's string faults 9 times with 3 frames and "
              "10 with 4, and LRU's stack property rules that anomaly out. Working sets and thrashing follow on "
              "the Job's trace. The part then turns from scarcity to what a level of indirection buys: copy-on-write "
              "fork, the zero page and mmap, the kernel mapped into every address space, buddy and slab "
              "allocators, trap-and-emulate virtual machines with the 24-reference nested walk, and containers. It "
              "ends with PebbleOS gaining an MMU: 46 more kernel instructions, a store into code killed with exit -15, "
              "and the Job's pipeline running unchanged under demand paging.",
        handoff="In Part 33 threads share one address space, which brings races and TLB shootdowns. Part 34 adds a "
                "disk to PebbleOS with a page cache and memory-mapped files, and Part 35's databases keep their own "
                "buffer pool. Part 45 builds the cloud from microVMs and containers, Part 48 meets LRU again as "
                "caches in front of services, and Part 55 attacks memory safety and address-space randomisation.",
        outside="Binary and hexadecimal arithmetic; pointers in C. The caches of Part 9 and the process of Part 31 "
                "are assumed.",
        objectives={
            "U": ["Split a virtual address into table indices and offset, walk a two-level page table by hand, "
                  "and say which PTE bit stops which access.",
                  "Replay a reference string through FIFO, LRU and OPT, count the faults, and exhibit Belady's "
                  "anomaly.",
                  "Compute an effective access time from a fault rate, and explain copy-on-write fork."],
            "M": ["Prove that OPT is optimal by an exchange argument and that LRU has the stack property, and "
                  "compute a whole LRU miss curve from stack distances.",
                  "Compute the size of flat and multi-level page tables and the reach of a TLB, and count the "
                  "memory references of a nested walk.",
                  "State the Popek-Goldberg condition and explain how trap-and-emulate runs an unmodified guest."],
            "D": ["Explain why translation reach has fallen behind memory size, and compare direct segments, "
                  "range TLBs, transparent huge pages and Midgard as answers.",
                  "State the open problems of page placement across CXL memory tiers and of TLB shootdown cost."],
            "I": ["Choose between a virtual machine and a container for isolation, naming what each shares with "
                  "the host and the attacks that crossed each boundary.",
                  "Diagnose a slowdown as TLB misses, page faults or thrashing from counters, and decide when huge "
                  "pages help."],
        },
        results=[
            ("Translation", r"\text{va}=\underbrace{10}_{L_1}\,|\,\underbrace{10}_{L_2}\,|\,\underbrace{12}_"
                            r"{\text{offset}}\ \text{bits},\qquad \text{TLB reach}=\text{entries}\times\text{page size}"),
            ("Effective access time", r"\text{EAT}=(1-p)\,t_{\text{mem}}+p\,t_{\text{fault}}"),
            ("Stack property", r"S_k(t)\subseteq S_{k+1}(t)\ \Rightarrow\ F_{\text{LRU}}(k+1)\le F_{\text{LRU}}(k)"),
            ("Sleator-Tarjan", r"F_{\text{LRU}}(k)\ \le\ \frac{k}{k-h+1}\,F_{\text{OPT}}(h)+h,\qquad h\le k"),
            ("Working set", r"W(t,\tau)=\{\text{pages referenced in }(t-\tau,\,t]\}"),
            ("Nested walk", r"(n+1)(m+1)-1=24\ \text{references for }n=m=4"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 9, 14), D=(15,), I=(13,),
        also=(("Page replacement and allocators", "explainer/cs/os/paging.py"),
              ("Pebble's MMU", "explainer/cs/os/mmu.py")),
    ),
    Part(
        n=33, level="U", widget="lostupdate", prereq=(10, 31, 32),
        question="Why do two threads that each add one to a counter raise it by only one, and what makes that "
                 "impossible?",
        story="Four threads add ten million each to one counter on this machine and it ends at 10,547,788: an "
              "addition is a load, an add and a store, and they interleave. The part builds an exhaustive "
              "interleaving model checker and counts: of the 20 schedules of two increments, 18 lose one. Mutual "
              "exclusion is then built from plain reads and writes, with Peterson's lock proved and checked in "
              "258 states, and the bakery for any number of threads. The part turns when the hardware reorders "
              "stores: under TSO the checker breaks Peterson in 10 steps, and one fence repairs it. Hardware locks "
              "from test-and-set to MCS, semaphores, monitors with Mesa semantics, and deadlock with the dining "
              "philosophers and the banker's algorithm follow. Two theories answer the reordering: memory models, "
              "where data-race freedom gives sequential consistency, and linearizability, with the Treiber stack, "
              "its ABA problem and Herlihy's consensus numbers, at whose top compare-and-swap implements every "
              "object. It ends with real bugs, from Therac-25 to the 2003 blackout, and with PebbleOS gaining "
              "threads, cas and amoadd: two threads of 2,000 plain increments end at 2,765 at quantum 500, and "
              "with amoadd or a lock always at 4,000.",
        handoff="Part 34 faces the cousin of the race, a crash in the middle of a write, and Part 35's databases "
                "turn locks into transactions. Part 38 asks the consensus question between computers that can "
                "fail and meets Fischer, Lynch and Paterson; Part 39 weakens consistency deliberately. Part 54 "
                "builds the verification methods used informally here, and Part 59 the theory of distributed "
                "computation.",
        outside="Programming with threads in any language helps; the store buffer and MESI caches of Part 10 are "
                "assumed.",
        objectives={
            "U": ["List the interleavings of two short threads, find the ones that lose an update, and repair "
                  "the race with a lock or an atomic instruction.",
                  "Write a bounded buffer with semaphores or a monitor, and explain why a condition is rechecked "
                  "in a while loop.",
                  "Name Coffman's four conditions, find the cycle in a deadlock, and remove it with a lock order."],
            "M": ["Prove Peterson's lock safe by an invariant, and show the schedule that breaks it under TSO and "
                  "the fence that repairs it.",
                  "Decide whether a history of a queue or a register is linearizable, and find the ABA schedule "
                  "of the Treiber stack.",
                  "Explain by valency why registers cannot solve consensus for two threads, and show that "
                  "test-and-set solves it for two and compare-and-swap for any number."],
            "D": ["State Herlihy's hierarchy and the universality of consensus, and what the Burns-Lynch bound "
                  "says about mutual exclusion from registers.",
                  "Explain why linearizability checking is NP-complete and how state counts grow from SC to TSO "
                  "to PSO, and state the open problems of weak-memory verification."],
            "I": ["Choose between a mutex, an atomic, a channel and a lock-free structure for a shared object, "
                  "from contention and measured cost per handoff.",
                  "Use a race detector, and say which bugs it cannot see: atomicity violations made of "
                  "individually atomic steps."],
        },
        results=[
            ("Interleavings of two threads", r"\binom{6k}{3k}\ \text{schedules};\quad 2\le\text{final count}"
                                             r"\le 2k\ \ (k\ge 2\text{ increments each})"),
            ("Peterson's lock", r"\text{flag}_i\leftarrow 1;\ \ \text{turn}\leftarrow j;\ \ \text{wait while }"
                                r"\text{flag}_j\wedge\text{turn}=j"),
            ("Coffman's conditions", r"\text{deadlock}\Rightarrow\text{exclusion}\wedge\text{hold-and-wait}"
                                     r"\wedge\text{no preemption}\wedge\text{cycle}"),
            ("DRF implies SC", r"\text{no data race in any SC execution}\ \Rightarrow\ \text{only SC behaviours}"),
            ("Linearizability", r"\exists\text{ a legal sequential order that keeps every real-time precedence}"),
            ("Consensus numbers", r"\text{registers }1,\quad\text{test-and-set, queues }2,\quad"
                                  r"\text{compare-and-swap }\infty"),
        ],
        U=(0, 1, 2, 3, 6, 7, 8, 15), D=(16,), I=(13, 14),
        also=(("The interleaving model checker", "explainer/cs/conc/mc.py"),
              ("The linearizability checker", "explainer/cs/conc/lin.py")),
    ),
    Part(
        n=34, level="U", widget="flashspare", prereq=(9, 28, 31, 32),
        question="How does data survive a power cut that can arrive between any two writes to the disk?",
        story="Appending one block to a file takes three writes: the bitmap, the data and the inode. The part "
              "opens by crashing after every subset of them: two of the eight outcomes are corrupt, two lose a "
              "block, and one passes fsck yet ends the file with a deleted file's password. It then builds "
              "storage from the bottom: the disk's seek, rotation and transfer, flash with its erase blocks and "
              "write amplification, inodes and directories, and PebbleFS, a small Unix file system, with FFS's "
              "locality. The centre of the part is crash consistency. PebbleFS is crashed at every point a disk "
              "could stop: with no ordering 34 of 126 crash points corrupt it, careful ordering costs 13 flushes "
              "instead of 5, and ordered journaling leaves all 150 intact. The part turns to the other designs "
              "that never overwrite, the log-structured file system and copy-on-write trees with checksums, and "
              "to RAID, where parity and Part 28's field rebuild lost disks. It then turns to the field, where "
              "disks fail more often and more quietly than datasheets say and fsync is easy to misuse, and ends "
              "with LSM trees and PebbleOS reading the thirty novels from its own disk: ledger row 12, 2.66 "
              "seconds.",
        handoff="Part 35's database keeps a write-ahead log, recovers with ARIES and indexes with B+ trees and "
                "this part's LSM trees. Part 39 puts copies on other machines, Part 45 prices durability in the "
                "cloud, Part 46 builds streaming systems on the partitioned log, and Part 50 does availability "
                "arithmetic with the failure rates of Chapter 12.",
        outside="Reading and writing files in C or Python; XOR. The memory hierarchy of Part 9 and the finite "
                "field of Part 28 are assumed.",
        objectives={
            "U": ["Compute the time of a random and of a sequential disk read from seek, rotation and transfer, "
                  "and explain why flash cannot overwrite in place.",
                  "Follow a path through superblock, inodes and directory blocks, and compute the largest file "
                  "an inode's pointers allow.",
                  "List the disk states a crash can leave after an append, and say how a journal's commit block "
                  "decides between the old file and the new."],
            "M": ["Compare writeback, ordered and data journaling by what each crash state can contain, and "
                  "explain why the commit needs a flush or a checksum.",
                  "Derive the cleaner's write cost 2/(1 - u), check flash's write amplification against the "
                  "estimate (1 + p)/2p, and compute RAID 5's small-write cost and mean time to data loss.",
                  "Compare leveled and tiered LSM compaction by write, read and space amplification."],
            "D": ["Explain what FSCQ and Yggdrasil prove about a file system and how CrashMonkey tests one, given "
                  "that k unflushed writes leave 2^k crash states.",
                  "State the LSM design space of Monkey and Dostoevsky and the open problems of zoned storage."],
            "I": ["Replace a file safely with write, fsync and rename, and name the bugs of in-place updates and "
                  "of delayed allocation.",
                  "Estimate the chance of a second failure or an unreadable sector during a RAID rebuild from "
                  "field failure rates, not the datasheet, and decide on scrubbing and checksums."],
        },
        results=[
            ("Disk access", r"t=t_{\text{seek}}+\tfrac12\,t_{\text{turn}}+t_{\text{transfer}},\qquad t_{\text{seek}}"
                            r"=t_{\min}+(t_{\max}-t_{\min})\sqrt{d/C}"),
            ("Largest PebbleFS file", r"(10+256+256^2)\ \text{blocks of 1 KiB}=67{,}381{,}248\ \text{bytes}"),
            ("Flash write amplification", r"\text{WA}\approx\frac{1+p}{2p},\qquad p=\frac{\text{spare}}"
                                          r"{\text{user capacity}}"),
            ("Cleaner's write cost", r"\frac{2}{1-u}\quad\text{at segment utilization }u"),
            ("RAID 6", r"P=\bigoplus_i D_i,\qquad Q=\sum_i g^{\,i}D_i\ \text{ over }\mathrm{GF}(2^8)"),
            ("RAID 5 mean time to data loss", r"\text{MTTDL}\approx\frac{\text{MTTF}^2}{N(N-1)\,\text{MTTR}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 7, 8, 11, 15), D=(16,), I=(12, 13),
        also=(("PebbleFS and its crash tester", "explainer/cs/store/fs.py"),
              ("The flash translation layer", "explainer/cs/store/flash.py")),
    ),
    Part(
        n=35, level="U", widget="bufferjoins", prereq=(9, 17, 33, 34),
        question="How can a program say what data it wants and leave the database to work out how to find it?",
        story="The Job is written twice: as Part 17's program, every step chosen by hand, and as one line of SQL "
              "over the thirty novels loaded as 4,609,954 rows, with the same twenty words as the answer. Codd's "
              "1970 idea, against the pointer-chasing programs of IMS and CODASYL, is that a query states its "
              "result. The part builds what that needs: relational algebra, functional dependencies and normal "
              "forms, Volcano iterators, four join algorithms costed in pages, and Selinger's dynamic program "
              "over join orders: the 120 orders of a five-table chain differ by a factor of 10,532. Its weak point "
              "is guessing sizes: under independence a city and its own country are estimated at 25 rows where "
              "492 match. The part then turns from one query to many users: schedules, the precedence graph and "
              "conflict serializability, two-phase locking and its proof, snapshots and the write skew of two "
              "doctors on call, and six isolation levels against five anomalies. ARIES recovers a crashed log by "
              "analysis, redo and undo, column stores speed up analytics, and the part ends with our own "
              "database planning the Job as a hash aggregate, checked against sqlite3: ledger row 13.",
        handoff="Part 39 stretches transactions across machines with two-phase commit and Spanner's clocks. Part "
                "43 builds services on a database, with idempotent requests and sagas; Part 46 turns the "
                "write-ahead log into a stream and builds warehouses on column stores; Part 47 scales the "
                "inverted index to the web; Part 48 puts shards, replicas and caches in front of a database.",
        outside="Sets and relations; reading a little SQL helps. The hash tables and B-trees of Part 17 and the "
                "journal of Part 34 are assumed.",
        objectives={
            "U": ["Write a query in relational algebra and in SQL, and evaluate it by hand on small tables.",
                  "Compute an attribute closure, find a key, and decompose a table into BCNF without losing "
                  "rows.",
                  "Draw a schedule's precedence graph, decide whether it is conflict-serializable, and show "
                  "that two-phase locking prevents a lost update."],
            "M": ["Derive the page I/O of block nested loops, sort-merge and Grace hash joins, and choose among "
                  "them for a given amount of memory.",
                  "Run Selinger's dynamic program on a small join graph, and explain how independence "
                  "assumptions make its size estimates fail.",
                  "Recover a crashed log by ARIES's analysis, redo and undo passes, and explain why redo repeats "
                  "history."],
            "D": ["State the AGM bound for the triangle query and explain why a generic join meets it where "
                  "every plan of binary joins does not.",
                  "State what is open in learned cardinality estimation and in checking isolation from "
                  "black-box histories, where serializability is NP-complete to test."],
            "I": ["Read a query plan from EXPLAIN, and decide whether an index, a covering index or fresh "
                  "statistics will change it.",
                  "Pick an isolation level knowing which anomalies it admits, and recognise write skew under "
                  "snapshot isolation.",
                  "Choose a row store or a column store for a workload from what each scan reads."],
        },
        results=[
            ("Join costs in page I/Os", r"\text{BNL: }M+\Bigl\lceil\frac{M}{B-2}\Bigr\rceil N,\qquad"
                                        r"\text{Grace hash: }3(M+N)"),
            ("Plan space", r"n!\ \text{left-deep},\quad n!\,C_{n-1}\ \text{bushy},\quad 2^n\ "
                           r"\text{subsets in the DP}"),
            ("Serializability theorem", r"\text{conflict-serializable}\iff\text{the precedence graph is acyclic}"),
            ("Two-phase locking", r"\text{no lock acquired after the first release}\ \Rightarrow\ "
                                  r"\text{conflict-serializable}"),
            ("Write-ahead logging", r"\text{a page reaches disk only after the log up to its pageLSN}"),
            ("AGM bound for triangles", r"|R\bowtie S\bowtie T|\le\sqrt{|R|\,|S|\,|T|}=N^{3/2}"),
        ],
        U=(0, 1, 2, 3, 4, 8, 9, 10, 15), D=(16,), I=(12, 14),
        also=(("Our database", "explainer/cs/db/engine.py"),
              ("Schedules, locking and isolation levels", "explainer/cs/db/txn.py")),
    ),
]
