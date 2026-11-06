# Computer Science, Built — Part 31: The Kernel

Part 31 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the first part of Act VI, *One Machine, Many Programs*. Early computers ran one job
at a time, and an expensive machine sat idle while a person thought. Time-sharing gave every user the illusion of a
whole machine. That needed protection, traps, processes and a scheduler. Queueing theory then explains why a busy
server is slow. Pebble gains a kernel mode, and PebbleOS, a kernel of 284 instructions, boots on it and runs the Job as
two processes joined by a pipe: ledger row 11.

The instruments are in `explainer/cs/os/` (tested in `tests/test_cs31_os.py`):
* `machine.py`, **Pebble with a kernel mode**:
  - a mode bit and the privileged extension of `explainer/cs/pebble/isa.py`: `ecall`, `eret`, `csrr`, `csrw`;
  - nine control registers (status, epc, cause, tval, tvec, scratch, timer, lo, hi);
  - traps and a countdown timer;
  - bounds checks on every user fetch, load and store;
  - per-mode instruction counts and an event log;
* `kernel.py`, **PebbleOS**:
  - boot; the trap entry that saves fifteen registers into a 128-byte PCB;
  - five system calls (exit, read, write, getpid, yield), with checked user pointers;
  - a 4 KiB pipe with blocking and restartable calls; round robin on the timer;
  - faults that kill only the offender;
  - `attribute` and `timeline` read per-process instruction counts out of the event log;
* `ulib.py`: the user library every process links: `_start`, and `getc`/`putc` buffered 4 KiB at a time over
  `read`/`write`. Part 13's compiler gains `target="os"`, which turns `getc`/`putc` into calls into it;
* `sched.py`: a tick-by-tick simulator of FCFS, SJF, SRTF, round robin, MLFQ (with the old gameable rule 4 and the
  boost), lottery, stride and CFS (Linux's nice-to-weight table); a Cilk-style work-stealing simulator;
* `queueing.py`: M/G/1 under FCFS, processor sharing and SRPT; M/M/1 sample paths; Pollaczek–Khinchine; *k* servers
  under d-FCFS, c-FCFS and preemptive quanta with overhead;
* `rt.py`: the Liu–Layland bound, response-time analysis, UUniFast, RMS and EDF timelines, and the Mars Pathfinder
  inversion with and without priority inheritance.

Measured on this machine (`videos/cs/cs31/compute.py` compiles and runs small C programs):
* a function call against `getpid` and a vDSO `clock_gettime`;
* `read()` with buffers of 1 byte to 1 MiB, and `strace -c` of `wc`;
* a pipe ping-pong between two processes on one CPU and on two;
* `fork`, `fork`+`exec`, `posix_spawn`, and `fork` with up to 1 GiB resident;
* a 25-line shell, run.

## Chapters

* **Hook.**
  - One user thinking 10 s and computing 0.5 s leaves the processor idle 95% of the time.
  - PebbleOS boots, and two processes print interleaved letters: 15 switches, 14 timer interrupts, 52 system calls.
* **1. From batch to time-sharing.**
  - GM-NAA I/O (1956), CTSS (1961), Multics (1965), Unix (1969–74), Linux (1991).
  - A closed queue of N users. The response time is flat until N* = (S + Z)/S = 21, then grows by S per user. The
    law R = N/X − Z checks.
* **2. Protection: the mode bit.**
  - Three threats (instructions, memory, time), and Pebble's new instructions and control registers.
  - Four processes, three hostile: the `halt` and the store into the kernel are killed (exits −2 and −7). The hog is
    preempted 121 times, and the good process finishes.
* **3. Traps and the system call.**
  - The five-step trap; one `getpid` traced: 78 kernel instructions (save 26, dispatch 23, handle 3, restore 26).
  - On this machine: a function call 1.5 ns, `getpid` 112 ns, the vDSO 29 ns.
  - `read()` costs 218 ns a byte one byte at a time, and 0.09 at 4 KiB.
* **4. The process.**
  - The job's 1 MiB region: library, buffers, 1.5 KB of code, a 512 KiB table, the stack. The PCB's fields.
  - The state diagram, counted in PebbleOS.
* **5. The context switch.**
  - 18 words saved; a switch through `yield` costs 118 kernel instructions.
  - Pipe ping-pong: 2.9 µs a round trip on one CPU, 25 µs across two.
* **6. fork, exec and wait.**
  - Why Unix split them; a 25-line shell with pipes, run.
  - `fork` takes 150 µs, `fork`+`exec` 1.3 ms, and `fork` with 1 GiB resident 33 ms. "A fork() in the road"
    (2019). PebbleOS has no fork until Part 32.
* **7. Scheduling: FCFS, SJF, SRTF.**
  - The metrics. The convoy: a mean turnaround of 110 under FCFS, 50 under SJF.
  - The exchange argument; SRTF with late arrivals (103 against 50).
  - 400 random jobs at load 0.8.
* **8. Round robin and MLFQ.**
  - RR: response 5, turnaround 85, on three jobs of 30. The quantum sweep with a one-tick switch (best near 12).
  - Corbató's MLFQ: the interactive job finishes at 341 against 641 under RR.
  - Gaming the old rule takes 89% of the machine, and accounting cuts it to 17%; starvation, and the boost.
* **9. Proportional share.**
  - Lottery against stride at 3:1, and lottery's unfairness against job length.
  - CFS: virtual runtime, the red–black tree, nice 0 against nice 5 (75.4%); EEVDF (Linux 6.6).
* **10. Many processors.**
  - Per-core queues, affinity and balancing.
  - Work stealing on a tree with T₁ = 83,647 and T∞ = 71: within 1% of T₁/P + T∞ up to 64 workers, with 487
    steals.
* **11. Real time.**
  - (2, 5) and (4, 7) at U = 0.971: RMS misses at 7, and EDF meets every deadline.
  - Liu–Layland's n(2^{1/n} − 1) → ln 2; random task sets under the bound, the exact test and EDF; harmonic periods.
  - Mars Pathfinder's priority inversion, and priority inheritance.
* **12. Queueing theory.**
  - Little's law by areas, and measured (L = 3.9816 = λW).
  - M/M/1 derived: W = 1/(μ − λ). The hockey stick against a million-job simulation, and two sample paths.
  - Pollaczek–Khinchine at load 0.8: 3, 5 and 23. FCFS, PS and SRPT on exponential and heavy-tailed sizes.
* **13. Kernel designs.**
  - Monolithic, microkernel, exokernel, unikernel; Tanenbaum–Torvalds (1992); L4.
  - Sizes: PebbleOS, seL4, Linux.
* **14. PebbleOS runs the Job.**
  - `tok | job`; a short run's timeline and the pipe's fill.
  - Instructions per byte: tok 34.0, job 49.9, kernel 23.0, against 38.7 bare. They are fitted on 24 passages and
    held out on 8: errors of 0.17%, 0.01% and 2.2%.
  - Ledger row 11: 2.67 billion instructions, **2.17 s** against row 8's 0.81 s.
* **15. Frontier: verified kernels and microsecond scheduling.**
  - seL4, CertiKOS, Hyperkernel.
  - 16 simulated cores with a bimodal service time. At load 0.7 the shorts' p99.9 is about 4,000 µs under d-FCFS,
    186 µs under c-FCFS, and 10 µs with 5 µs quanta. The quantum sweep.
  - eBPF and verifying its verifier. Open problems. Outro.

## Build

```bash
python -m videos.cs.cs31.compute           # every number in the part (about five minutes)
python tools/build.py cs31 -q l            # a 480p preview
python tools/build.py cs31                 # 1080p
```

## Problems, with solutions

1. **SRPT is optimal.** Prove by an exchange argument that SRPT minimises the mean response time for jobs arriving
   over time, on one server.

   *Solution.* Take any schedule, and the first moment t at which it runs some job j while another present job k
   has less remaining work, r_k < r_j. Consider the slots, from t on, in which the schedule runs j or k. Reassign
   them: k's remaining work first, then j's.
   - The last of the two still finishes in the last of those slots, so the later completion time is unchanged.
   - The earlier completion now comes after r_k units of those slots, which is no later than before.
   - Every other job runs in exactly the same slots.

   So the sum of completion times does not increase, and the schedule now agrees with SRPT at time t. Repeating at
   each disagreement (there are finitely many in any bounded horizon) transforms the schedule into SRPT's without
   increasing the total. Since the arrival times are fixed, minimising the total completion time minimises the mean
   response time (Schrage, 1968).

2. **Liu and Layland for two tasks.** Derive the bound 2(√2 − 1) for two tasks.

   *Solution.* Let T₁ < T₂ (T₁ has priority) and r = T₂/T₁.
   - If r > 2, shrinking T₂ to a value between T₁ and 2T₁ only makes the set harder for the same utilisation, so
     assume 1 < r ≤ 2.
   - The worst case releases both together. Task 1 runs twice before T₂, and task 2 fits exactly when
     C₂ = T₂ − 2C₁ (if C₁ ≤ T₂ − T₁). The utilisation is least when C₁ just fills the gap, C₁ = T₂ − T₁.
   - Then C₂ = 2T₁ − T₂, and U = (T₂ − T₁)/T₁ + (2T₁ − T₂)/T₂ = r − 1 + 2/r − 1 = r + 2/r − 2.
   - This is minimised at r = √2, where U = 2√2 − 2 = 2(√2 − 1) ≈ 0.828.

   Any set below this utilisation is schedulable, and this set (made the slightest bit heavier) is not.

3. **M/M/1's response time.** Show that the response time is exponential with rate μ − λ, and find its 99th
   percentile.

   *Solution.*
   - By PASTA (Poisson arrivals see time averages), an arrival finds n jobs with probability (1 − ρ)ρⁿ.
   - By memorylessness, the job in service still needs an exponential(μ) time. So the arrival's response time is a
     sum of K = n + 1 independent exponential(μ) times, where P(K = k) = (1 − ρ)ρ^{k−1} is geometric.
   - A geometric sum of exponentials is exponential: its transform is
     ∑ₖ (1 − ρ)ρ^{k−1} (μ/(μ + s))ᵏ = μ(1 − ρ)/(μ(1 − ρ) + s), the transform of an exponential with rate
     μ(1 − ρ) = μ − λ.
   - So P(T > x) = e^{−(μ−λ)x}, and the 99th percentile is ln 100/(μ − λ) ≈ 4.6 W.

   At ρ = 0.9 and μ = 1 that is 46 service times; our simulation measured 49, since the high-load tail converges
   slowly.

4. **Gaming the old MLFQ.** Show that a job that yields just before its quantum ends keeps the top queue under the
   old rule, and bound its share.

   *Solution.* Under the old rule 4, a job that gives up the processor before its allotment is used keeps its
   priority, and its allotment is reset. A job that runs q − 1 ticks and then does one tick of I/O never uses a full
   allotment, so it never moves down. Rule 1 lets it preempt every lower job whenever it is ready. Against one hog
   at a lower level, the hog runs only during the gamer's I/O ticks, so the gamer takes at least (q − 1)/q of the
   processor in the long run: 90% for q = 10 (we measured 89%, the difference being the hog's first allotment at
   the top). With k gamers sharing the top level by round robin, together they take all the processor time that
   their I/O ticks allow, and the hog can be starved. Rule 4 as fixed, counting time at a level whatever the
   pattern, demotes the gamer after its allotment, and the boost (rule 5) bounds starvation.

5. **Build: sleep and stride in PebbleOS.** Add `sleep(n)` and a stride scheduler to PebbleOS, and show two
   processes sharing 3 to 1.

   *Solution.*
   - Add three PCB fields: `wake`, `pass` and `stride` = L/tickets, with tickets set in the boot table.
   - `sys_sleep`: read the instruction counter (`IO_CYCLES`), set `wake` = now + n, mark the process BLOCKED, and
     schedule.
   - In `tick` and `schedule`: first make every BLOCKED process whose `wake` has passed READY (a process blocked on
     the pipe has `wake` = 0 and is woken as before).
   - Replace the round-robin scan with a scan for the READY process of least `pass`, and add its `stride` when it is
     dispatched.
   - Test: two processes that loop forever, incrementing a counter in memory, with tickets 300 and 100, preempted by
     the timer. After 10⁶ instructions, the dispatch counts in their PCBs (and the counters) are within one quantum
     of 3:1.

   `sleep` lets a process wait without spinning. With the stride, PebbleOS gives proportional shares exactly, as the
   simulation in chapter 9 does.

6. ★ **Research: the quantum for tail latency.** For k servers, bimodal sizes and preemption overhead δ, find the
   quantum that minimises the short requests' p99.9, and how it scales with δ and the load.

   *Where to start.*
   - Run `explainer/cs/os/queueing.multi(..., policy="ps", quantum=q, overhead=δ)` over a grid of q, δ (0.1–2 µs),
     load (0.3–0.85), k (4–64) and the long fraction. Check first that q → ∞ gives c-FCFS and δ = 0 favours q → 0.
   - The shorts' tail has two causes: waiting for a free core when all k hold long requests, which grows as q grows;
     and the capacity lost to overhead, a fraction δ/(q + δ) of the long work, which grows as q shrinks and pushes
     the effective load towards 1.
   - A first model balances the two. The probability that all k cores hold scans falls roughly geometrically in k;
     the overhead raises the load to ρ(1 + f·δ/q), where f is the long requests' share of the work. Does the
     optimum scale like √δ, as such balances usually do, or does the cliff near effective load 1 dominate?
   - Compare with the measured systems: Shinjuku (Kaffes et al., NSDI 2019) used 5–15 µs; Concord (Iyer et al.,
     SOSP 2023) cut the overhead with cooperative preemption.
   - Analytical footholds: Kleinrock's time-sharing models (1967), and the heavy-traffic results for many-server
     queues (Halfin and Whitt, 1981).

   Nobody has a closed form for the multi-server case with overhead. A good approximation, checked against
   simulation, would be useful to every system that sets a quantum.

## 习题与解答

1. **SRPT 最优。** 用交换论证证明：在单服务器上、作业随时间到达时，SRPT 使平均响应时间最小。

   *解答。* 取任意调度，找最早的时刻 t：此时它在运行作业 j，而另一个在场作业 k 的剩余工作量更少，r_k < r_j。考虑 t 之后
   该调度用来运行 j 或 k 的所有时间片，重新分配：先做完 k 的剩余工作，再做 j 的。两者中较晚完成的那个仍在这些时间片的最后一片
   完成，较晚的完成时间不变；较早的完成时间变为这些时间片中的第 r_k 个单位，不晚于原来；其他作业的时间片完全不变。所以完成时间
   之和不增，且调度在时刻 t 与 SRPT 一致。对每处不一致重复（有限时间内只有有限处），就把调度变成 SRPT 而总和不增。到达时间固定，
   完成时间总和最小即平均响应时间最小（Schrage，1968）。

2. **两个任务的 Liu–Layland 界。** 推导两任务的界 2(√2 − 1)。

   *解答。* 设 T₁ < T₂（T₁ 优先），r = T₂/T₁。若 r > 2，把 T₂ 缩到 T₁ 与 2T₁ 之间，在相同利用率下只会更难，故设 1 < r ≤ 2。
   最坏情况是两者同时释放；在 T₂ 之前任务 1 运行两次，当 C₂ = T₂ − 2C₁ 时任务 2 恰好放得下（若 C₁ ≤ T₂ − T₁）。C₁ 恰好填满
   空隙 C₁ = T₂ − T₁ 时利用率最小，此时 C₂ = 2T₁ − T₂，U = r − 1 + 2/r − 1 = r + 2/r − 2，在 r = √2 处取最小值
   2√2 − 2 ≈ 0.828。

3. **M/M/1 的响应时间。** 证明响应时间服从速率为 μ − λ 的指数分布，并求其第 99 百分位数。

   *解答。* 由 PASTA（泊松到达看到时间平均），到达者看到 n 个作业的概率为 (1 − ρ)ρⁿ；由无记忆性，正在服务的作业还需指数(μ)
   时间。于是响应时间是 K = n + 1 个独立指数(μ) 之和，K 服从几何分布 P(K = k) = (1 − ρ)ρ^{k−1}。几何个指数之和仍是指数分布：
   其变换为 μ(1 − ρ)/(μ(1 − ρ) + s)，速率 μ(1 − ρ) = μ − λ。所以 P(T > x) = e^{−(μ−λ)x}，第 99 百分位数为
   ln 100/(μ − λ) ≈ 4.6W。ρ = 0.9、μ = 1 时为 46 个服务时间；我们的模拟测得 49，高负载下尾部收敛较慢。

4. **钻旧 MLFQ 的空子。** 证明：在旧规则下，一个总在时间片用完前让出处理器的作业会一直留在最高队列，并给出它份额的界。

   *解答。* 旧的规则 4 下，作业若在用完配额前让出处理器，就保持优先级，配额重置。运行 q − 1 个刻度再做一个刻度 I/O 的作业永远
   用不完配额，永不降级；由规则 1，它一就绪就能抢占所有低优先级作业。对一个低层的计算密集作业，后者只能在它做 I/O 的刻度运行，
   所以它长期至少占 (q − 1)/q：q = 10 时为 90%（我们测得 89%，差别来自那个作业在最高层的第一段配额）。修正后的规则 4 不论运行
   方式如何都累计在该层的时间，配额用完即降级；提升（规则 5）则限制了饥饿。

5. **动手：给 PebbleOS 加 sleep 与步幅调度。** 并演示两个进程按 3 比 1 分享。

   *解答。* PCB 增加 `wake`、`pass` 和 `stride` = L/票数（票数写在启动表中）。`sys_sleep` 读取指令计数器（`IO_CYCLES`），令
   `wake` = 当前 + n，标为阻塞，然后调度。`tick` 与 `schedule` 先把 `wake` 已过的阻塞进程设为就绪（等管道的进程 `wake` = 0，
   照旧唤醒）；把轮转扫描换成找 `pass` 最小的就绪进程，调度它时加上它的 `stride`。测试：两个无限循环、在内存中计数的进程，
   票数 300 和 100，由定时器抢占；执行 10⁶ 条指令后，PCB 中的调度次数（以及计数）与 3:1 相差不超过一个时间片。

6. ★ **研究：为尾延迟选时间片。** 对 k 个服务器、双峰作业大小与抢占开销 δ，找出使短请求 p99.9 最小的时间片，以及它如何随 δ
   与负载变化。

   *从哪里开始。* 在 q、δ（0.1–2 µs）、负载（0.3–0.85）、k（4–64）和长请求比例的网格上运行
   `explainer/cs/os/queueing.multi(..., policy="ps", quantum=q, overhead=δ)`；先检查 q → ∞ 给出 c-FCFS，δ = 0 时 q 越小越好。
   短请求的尾部有两个成因：k 个核全被长请求占住时的等待（随 q 增大）；以及开销损失的容量，占长请求工作量的 δ/(q + δ)（随 q
   减小，把有效负载推向 1）。第一个模型平衡两者：全部核都是长请求的概率大致随 k 几何下降；开销把负载抬到 ρ(1 + f·δ/q)，f 是长请求
   占的工作量份额。最优值是否像这类平衡通常那样按 √δ 变化，还是有效负载接近 1 的悬崖占主导？与实测系统比较：Shinjuku（Kaffes 等，
   NSDI 2019）用 5–15 µs；Concord（Iyer 等，SOSP 2023）用协作式抢占降低开销。理论落脚点：Kleinrock 的分时模型（1967），以及多服务器
   排队的重载结果（Halfin 与 Whitt，1981）。多服务器加开销的情形没有闭式解；一个经模拟验证的好近似，对每个要设定时间片的系统都
   有用。

## Glossary additions

内核 kernel · 分时 time-sharing · 批处理 batch processing · 用户态 user mode · 内核态 kernel mode · 模式位 mode bit ·
特权指令 privileged instruction · 控制寄存器 control register · 陷阱 trap · 中断 interrupt · 系统调用 system call · vDSO ·
定时器 timer · 进程 process · 进程控制块 process control block · 就绪 ready · 阻塞 blocked · 上下文切换 context switch ·
管道 pipe · 文件描述符 file descriptor · 外壳 shell · 调度器 scheduler · 周转时间 turnaround time · 响应时间 response time ·
护航效应 convoy effect · 先来先服务 first come, first served · 短作业优先 shortest job first · 最短剩余时间优先 shortest
remaining time first · 轮转 round robin · 时间片 quantum · 多级反馈队列 multi-level feedback queue · 彩票调度 lottery
scheduling · 步幅调度 stride scheduling · 完全公平调度器 completely fair scheduler · 虚拟运行时间 virtual runtime · 亲和性
affinity · 负载均衡 load balancing · 工作窃取 work stealing · 速率单调 rate monotonic · 最早截止期优先 earliest deadline
first · 优先级反转 priority inversion · 优先级继承 priority inheritance · 利特尔法则 Little's law · 排队论 queueing theory ·
利用率 utilisation · 处理器共享 processor sharing · 尾延迟 tail latency · 宏内核 monolithic kernel · 微内核 microkernel ·
外核 exokernel · 单一内核 unikernel · 形式化验证 formal verification

## Sources

*Canon.* Books:
- Arpaci-Dusseau & Arpaci-Dusseau, *Operating Systems: Three Easy Pieces* (OSTEP, v1.10, 2023), virtualisation of the
  CPU;
- Tanenbaum & Bos, *Modern Operating Systems* (5th ed., 2023);
- Anderson & Dahlin, *Operating Systems: Principles and Practice* (2nd ed., 2014); Silberschatz, Galvin & Gagne,
  *Operating System Concepts* (10th ed., 2018);
- Cox, Kaashoek & Morris, *xv6: a simple, Unix-like teaching operating system* (2020);
- Harchol-Balter, *Performance Modeling and Design of Computer Systems* (2013); Kleinrock, *Queueing Systems*
  (vols. 1–2, 1975–76).

Papers:
- History: Corbató, Merwin-Daggett & Daley, "An Experimental Time-Sharing System" (1962); Corbató & Vyssotsky,
  "Introduction and Overview of the Multics System" (1965); Ritchie & Thompson, "The UNIX Time-Sharing System" (1974).
- Processes and switching: Baumann et al., "A fork() in the road" (HotOS 2019); Li, Ding & Shen, "Quantifying the
  cost of context switch" (2007).
- Scheduling:
  - Schrage (1968);
  - Waldspurger & Weihl, "Lottery Scheduling" (OSDI 1994), and "Stride Scheduling" (MIT TM-528, 1995);
  - Stoica & Abdel-Wahab, EEVDF (1995);
  - Blumofe & Leiserson, "Scheduling Multithreaded Computations by Work Stealing" (JACM 1999).
- Real time:
  - Liu & Layland (JACM 1973); Joseph & Pandya (1986); Bini & Buttazzo, UUniFast (2005);
  - Sha, Rajkumar & Lehoczky, "Priority Inheritance Protocols" (1990);
  - Reeves, "What really happened on Mars?" (1997).
- Queueing: Little (1961); Pollaczek (1930); Khinchine (1932); Harchol-Balter, Schroeder, Bansal & Agrawal,
  "Size-based scheduling to improve web performance" (TOCS 2003); Scully, Harchol-Balter & Scheller-Wolf, SOAP
  (2018).
- Kernel designs:
  - Accetta et al., Mach (1986); Liedtke, "On µ-Kernel Construction" (SOSP 1995);
  - Engler, Kaashoek & O'Toole, exokernel (SOSP 1995); Madhavapeddy et al., unikernels (ASPLOS 2013);
  - the Tanenbaum–Torvalds exchange, comp.os.minix (January 1992).
- Frontier:
  - Klein et al., "seL4: Formal Verification of an OS Kernel" (SOSP 2009); Gu et al., CertiKOS (OSDI 2016); Nelson
    et al., Hyperkernel (SOSP 2017);
  - Kaffes et al., Shinjuku (NSDI 2019); Ousterhout et al., Shenango (NSDI 2019); Fried et al., Caladan (OSDI 2020);
  - Gershuni et al., PREVAIL (PLDI 2019); Nelson et al., Jitterbug (OSDI 2020); Vishwanathan et al., Agni (CAV
    2023).
