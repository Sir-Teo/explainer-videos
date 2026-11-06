# Computer Science, Built — Part 45: The Cloud

Part 45 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act IX, *Systems at Scale*. A modern application rents its computer
by the second from a building that draws tens of megawatts, and under the abstraction sit the series' own ideas at the
scale of buildings: virtual machines shrunk to microVMs, containers placed by bin-packing heuristics, control loops
that reconcile what is with what should be, and storage whose eleven nines we derive from a Markov chain. The Job gets
a price in dollars.

The instruments are in `explainer/cs/cloud/` (tested in `tests/test_cs45_cloud.py`):
* `packing.py`: next fit, first fit, best fit and first fit decreasing; the exact optimum by branch and bound (items
  sorted, equal-load bins tried once, the size bound as a cut-off); the four heuristics against it on random and on
  clustered instances; the family of halves alternating with tiny items on which next fit uses nearly twice the
  optimum; vector packing of (CPU, memory) demands, sorted by the larger demand against by CPU alone; the reduction
  from partition.
* `control.py`: a reconciler for a replica count, level-triggered against edge-triggered with lost "pod died"
  events; an autoscaler as a proportional controller acting on a delayed utilization measurement, with a quota;
  Erlang C by the stable Erlang B recursion, and the fewest servers meeting a mean-wait and a P(wait) target; an
  infrastructure plan as a diff (create, update, destroy) applied in dependency order, destroys in reverse.
* `durability.py`: the mean time to data loss for n fragments of which any k suffice, from the birth–death chain of
  failure and one-at-a-time repair, solved exactly; the probability of loss in a year and its nines; a Monte Carlo
  check of the same chain; whole racks failing together against fragments spread across racks.
* `cost.py`: AWS us-east-1 list prices as published in 2024; Lambda against m5.large servers at a steady request rate,
  and the break-even rate; a batch job on spot capacity with Poisson interruptions and checkpoints; the Job's bill
  three ways from its measured single-core time.

## Chapters

* **Hook.** John McCarthy at MIT's centennial (1961): computing may someday be organized as a public utility.
  Time-sharing, then owned servers and rented racks, then S3 (March 2006, storage by the gigabyte-month) and EC2
  (August 2006, a computer by the hour), and today billing by the second or by the request. Under the word cloud, a
  hierarchy in which every layer is a scheduling problem and a failure domain: region, building (tens of megawatts,
  tens of thousands of servers), rack, server, virtual machine, container. The Job gets a price: counting 25.0 MB of
  novels takes 1.41 s on one core of this machine, which costs $0.00160 on one on-demand server billed per second
  with a one-minute minimum, $0.00056 at a typical spot discount, and $0.00003 (about three thousandths of a cent) on
  sixteen functions billed per gigabyte-second, at dated list prices that leave out cold starts and reading the text
  from storage.
* **1. The warehouse-scale computer.** Barroso and Hölzle (2009): tens of thousands of servers, one owner, a few huge
  services programmed as one machine; the rack (a few dozen servers, a switch, a shared power feed) in rows with cold
  and hot aisles. The power chain from grid through transformers, UPS, PDU and rack to each server's supply, with
  diesel generators behind the batteries; the scarce resource is watts, and because thousands of servers never peak
  together operators install more than the ratings allow and cap power (Fan, Weber and Barroso, 2007). Idle is
  expensive: on a straight line from half power at idle, a server 30% busy draws 65% of its peak and does 46% of the
  work per watt it manages flat out; energy proportionality as the remedy. PUE (The Green Grid, 2007): about 2.5 for
  the industry average in 2007 (60% of the electricity never reaching a computer), 1.58 in 2023 (37%), 1.10 for
  Google's fleet in 2023 (9%). Failure as a rate: 2,000 servers in 50 racks, each failing once in three years (an
  assumption), 2000 / 1096 days ≈ 1.8 failures a day, 62 in a simulated month; failures that come in groups, and
  failure domains that nest from server to region.
* **2. Virtual machines, shrunk.** KVM (in Linux since 2007) runs guest code on the processor and takes only its exits;
  a user-space monitor such as QEMU (Bellard, 2003) emulates the rest, and a device access is exit, hand-off,
  emulation. A general-purpose monitor's device zoo against Firecracker's whole device model (virtio-net,
  virtio-block, virtio-vsock, a serial console, a keyboard controller used only to stop the machine); VENOM (2015), a
  guest escape through QEMU's emulated floppy controller. Booting: a general-purpose VM takes about 9 s in
  illustrative stages; the Firecracker project reports user code in as little as 125 ms, under 5 MiB of overhead per
  microVM and up to 150 microVMs started per second per host; SnapStart (2022) restores a snapshot instead. One
  microVM per function, customers mixed on one host, behind layered walls (guest kernel, KVM or the device model,
  then the jailer's chroot, namespaces, cgroups and seccomp filter). Isolation in grades: process, container (one
  kernel, about 450 system calls), gVisor (2018), microVM (Kata Containers, 2017), full VM.
* **3. Containers.** Namespaces decide what a process sees (pid 1 inside is 4242 to the host), cgroups how much it may
  use: `cpu.max 50000 100000` is half a processor, so a busy process runs 50 ms in every 100 ms and a request arriving
  while it is throttled waits about 45 ms (illustrative), and `memory.max` of 256 MiB ends in the out-of-memory
  killer. An image is a stack of layers, each named by the SHA-256 of its contents, and a manifest named by its own
  hash: a Merkle tree (Part 41); changing one line of the application renames only the top layer and the manifest,
  which is why a Dockerfile copies the code last. OverlayFS (2014): the higher layer wins, the first write copies a
  file up, a delete writes a whiteout, and a hundred containers share the read-only layers. A registry stores each
  blob once by hash, so a machine that ran `web:v1` pulls `web:v2` by downloading one layer; the Open Container
  Initiative (2015) and runc.
* **4. Orchestration and reconciliation.** Borg (Verma et al., 2015): cells of about ten thousand machines in the
  median, a Borgmaster replicated five times with Paxos, a Borglet on every machine; Kubernetes (2014) maps onto it
  almost one for one (pod and task, kubelet and Borglet, Deployment and job, etcd with Raft and the Paxos store).
  Declarative desired state against an imperative script; the reconciliation loop (observe, compare, act), which asks
  only what is different, so it is idempotent. Level- against edge-triggered, simulated: five replicas, two pods
  crashing at steps 12 and 25, 30% of "pod died" events lost; the edge-triggered controller loses one of the two
  events at step 25 and stays at 4 replicas for good; the level-triggered one climbs to 5 one pod per step and is
  short for 1 step after each crash. etcd replicated by Raft (Part 38), with every write committed by a majority
  (three members survive one failure, five survive two); versioned objects refuse updates based on stale reads, like
  compare-and-swap; the scheduler is a controller too.
* **5. Scheduling as bin packing.** First fit puts eight containers (0.5, 0.3, 0.6, 0.2, 0.4, 0.3, 0.5, 0.2 of a
  processor) into 3 full machines, and the fourth can be switched off; real schedulers filter, then score. NP-hard by
  way of partition (Part 26): 3, 1, 1, 2, 2, 1 (total 10) fit in 2 bins, 3, 3, 3, 1 need 3, so no fast algorithm can
  promise better than 3/2 of the optimum unless P = NP. Four heuristics against the exact optimum, 20 items an
  instance, bins above the optimum as mean / worst: on 200 instances with uniformly random sizes, next fit +24% /
  +50%, first fit +8% / +29%, best fit +8% / +29%, first fit decreasing +1% / +14%; on 100 instances with clustered
  sizes, +18% / +33%, +6% / +17%, +6% / +17%, +4% / +17%. What can be guaranteed: next fit on halves alternating with
  tiny items uses 4 bins against 3 for 8 items, 8 against 5 for 16, 12 against 7, 40 against 21 and 200 against 102
  for 400 (ratio 1.96); NF ≤ 2·OPT − 1 proved; FFD ≤ 11/9·OPT + 6/9 (Johnson 1973 with + 4, Dósa 2007 tight). Vector
  packing of 200 containers by CPU and memory: total demand says at least 38.4 machines; first fit sorted by each
  job's larger demand uses 43, 87% busy in CPU and 89% in memory; sorted by CPU alone, 63, 60% and 61%. Priorities and
  preemption; running production and batch on separate machines would need 20–30% more machines in the median Borg
  cell.
* **6. Autoscaling as control.** The loop, with a late measurement and a boot time; Kubernetes' Horizontal Pod
  Autoscaler, n ← ⌈n·u/u*⌉, and ours, n_{t+1} = n_t + K(u_{t−d}/u* − 1)·n_t (K = 1 is Kubernetes' rule). Load jumps
  from 40 to 100 requests a second at step 10, a server handles 10 at full use and the target is 60%, so the right
  size is 16.7 servers: K = 0.3 with a one-step delay settles at 16.4 after a peak of 18.0; K = 0.2 with three steps
  settles at 16.8 after 25.4; K = 0.5 oscillates between 5 and 99; K = 1 slams between 1 and the quota of 200.
  Linearized, e_{t+1} = e_t − K·e_{t−d}, stable only while K < 2 cos(dπ/(2d + 1)): 2 with no delay, 1.00 with one
  step, 0.45 with three, and all four runs land on the predicted side (Maxwell, 1868). Erlang C from the M/M/c chain,
  with the check C(2, 1) = 0.333. The fewest servers keeping the mean wait under a twentieth of a service time and
  P(wait) under a fifth: 10 erlangs need 14 servers (71% busy), 50 need 58 (86%), 100 need 111 (90%), 500 need 525
  (95%), 1,000 need 1,034 (97%); (c − a)/√a stays between 1.08 and 1.26, square-root staffing (Halfin and Whitt,
  1981), the economy of scale behind the cloud. Predictive scaling against a reactive loop on two days of daily load
  (illustrative).
* **7. Serverless.** Lambda (2014): a function run per event, an instance per concurrent event, billed by the
  millisecond, scaling to zero, with state kept outside (Jonas et al., 2019). The bill: 100 ms at 512 MB costs $0.83
  per million requests in compute and $0.20 in request fees, $1.03 in all, against $0.13 per million for an m5.large
  kept busy at 200 requests a second; a function costs 7.8 times as much per request, so it wins while the server
  would be busy less than 13% of the time, below 25.8 of its 200 requests a second. Cold starts (boot the microVM,
  start the runtime, load libraries): of twelve requests in an illustrative hour, a 3-minute keep-alive starts 6 cold
  and keeps an instance warm 29 of 60 minutes; a 10-minute one starts 2 cold and keeps it 57; Shahrad et al. (2020)
  on Azure Functions. Concurrency by Little's law: at 25.8 requests a second of 100 ms each, 2.6 instances in flight
  (24 requests on 5 instances in one random second), 10 at 100 requests a second, 100 at 1,000; AWS's default cap of
  1,000 concurrent executions per account and region is reached at 10,000 requests a second; throttling, the
  15-minute limit, and databases swamped by a thousand connections (Part 43).
* **8. Object storage and eleven nines.** Block, file and object storage; S3 Standard at $0.023 a gigabyte-month.
  Read after write: until 2020 an overwrite could be read stale for a while; since December 2020 every later GET and
  LIST sees the write; updates are atomic per key, the later writer wins, and there are no transactions across keys
  (Part 46 builds tables on this). RS(10, 4) fragments, two to a rack across seven racks: a whole rack plus two more
  disks leaves 10 of 14, still readable; 4 losses tolerated at 1.4× the data against 2 for three copies at 3×. The
  Markov chain of failure and repair, with T_i = (1 + μ·T_{i−1})/((n − i)λ) and MTTDL = Σ T_i: with 2% a year and a
  day's repair, three copies last about 2.7 billion years; a Monte Carlo with exaggerated rates gives 178 against 181
  years exact, and 11.8 against 11.6 for any 4 of 6. The table (stored, losses survived, mean years to loss, nines a
  year): one copy 1.0×, 0, 49.5, 1.7; two copies 2.0×, 1, 4.5×10⁵, 5.7; three copies 3.0×, 2, 2.7×10⁹, 9.4; 6 data
  + 3 parity 1.5×, 3, 9.7×10¹⁰, 11.0; 10 + 4 1.4×, 4, 2.2×10¹³, 13.3; 10 + 6 1.6×, 6, 3.0×10¹⁹, 19.5. S3 is designed
  for eleven nines: ten million objects, one lost about every ten thousand years. Every row assumes independent
  failures.
* **9. Cloud networking.** A VPC, 10.0.0.0/16 (Part 36), with a subnet in each zone, a route table (local, and
  0.0.0.0/0 to the internet gateway) and stateful security groups. Packets inside packets: the host's virtual switch
  maps the tenant's 10.0.2.7 to host 192.168.9.40 and wraps the packet in UDP port 4789 and a VXLAN header (RFC 7348,
  2014: 8 bytes, a 24-bit network number, about 16 million networks, 50 bytes a packet with the outer headers);
  Amazon's Nitro cards, Google's Andromeda (2018). Managed load balancers with health checks, at layer 4 or 7; Maglev
  (2016), hashing connections to backends in software; anycast through BGP. Egress: data in is free, out is $0.09 a
  gigabyte (about $90 a terabyte before discounts) and traffic between zones is billed too; one download costs 3.9
  months of storage; our 25 MB of novels about 0.22 cents a download; data has gravity.
* **10. Infrastructure as code.** Console clicks against a declared file, through commit, plan, review and apply
  (CFEngine 1993, Puppet 2005, CloudFormation 2011, Terraform 2014; a simplified Terraform-like syntax). A plan is a
  diff of the state file against the code: the network and subnet unchanged, the database updated from small to
  large, the queue and service created, the old cache destroyed, "Plan: 2 to add, 1 to change, 1 to destroy." Applied
  in topological order (Part 18): 1 update db, 2 create queue, 3 create service, 4 destroy old-cache; db and queue
  share no path and can be applied together, Part 41's build graph with clouds for files. Drift: a database resized
  to xlarge by hand during an incident; the next refresh finds it and the plan proposes
  `~ db update size: xlarge -> large`, a change nobody wrote, to apply or to adopt in the code; scheduled
  plans, and the Kubernetes controller as the same idea run continuously. Immutable infrastructure: snowflakes
  patched in place against machines replaced from a content-addressed image, with rollback by pointing back.
* **11. Neighbours, regions and failure domains.** Noisy neighbours: the hypervisor divides cores and memory but not
  the last-level cache or the memory bus (Part 9); Intel's Cache Allocation Technology and Memory Bandwidth
  Allocation. CPI² (Zhang et al., 2013) flags a task whose cycles per instruction stray above its usual value plus 2σ
  and caps the neighbour whose CPU use rose with it; Schad et al. (2010) on the variance of EC2. Prime and probe on a
  shared cache; Osvik, Shamir and Tromer (2006) on AES, Ristenpart et al. (2009) on co-residence in EC2. Regions,
  zones (AWS: separate buildings within 100 km of each other), racks and hosts as nested failure domains, and S3
  in Northern Virginia down for about four hours in February 2017 after a mistyped command. Placement: RS(10, 4) two
  to a rack in seven racks leaves 12 fragments with one rack down, 10 with two, 8 and the object lost with three;
  all 14 in one rack lose it at the first rack failure. Five Raft replicas split 2, 2, 1 across three zones survive
  any zone; split 3, 2 across two they do not. Spread constraints pull against packing. Data residency: GDPR (applied from 2018) and Schrems II
  (2020); light in fibre covers about 200 km a millisecond, so replication between regions is usually asynchronous.
* **12. Cost, carbon, and the Job's bill.** Functions or servers for steady traffic from 0.1 to 1,000 requests a
  second: the function's monthly bill grows with the rate at $1.03 a million, one m5.large costs $69.12 a month, and
  the lines cross near 26 requests a second. Spot capacity: a ten-hour job, an interruption every 10 hours on average,
  checkpoints costing 1.2 minutes (and three minutes to restart, in the model), at a typical 65% discount: without
  checkpoints 17.4 hours and $0.58; every 120 minutes 11.3 h and $0.38; every 60, 10.8 h and $0.36; every 30, 10.7 h
  and $0.36, the cheapest; every 15, 11.0 h and $0.37; on demand 10.0 h and $0.96; Young's rule (1974),
  √(2C/λ) ≈ 38 minutes. Ledger row 16: the Job on sixteen functions, about 0.09 s of wall-clock time and $0.00003,
  and a second column, dollars. Energy and carbon: datacentres used roughly 1–1.5% of the world's electricity in 2022
  (IEA); the best fleets report a PUE of about 1.1; carbon-aware scheduling moves a flexible job to the cleanest
  hours (illustrative); the cheapest energy is the computation not done.
* **13. Frontier: scheduling, isolation and energy.** Where the nines go: RS(10, 4) with independent fragment failures
  gives 13.3 nines a year; with whole racks failing (each once in twenty years, a day to repair) and two fragments to
  each of seven racks, 7.0; with all fragments in one rack, 1.3. Scheduling with predictions: first fit decreasing
  comes within 1% of the optimum because it knows the sizes, next fit 24% above; online schedulers know neither sizes
  nor lifetimes; learning-augmented algorithms (Lykouris and Vassilvitskii, 2018); schedulers that predict VM
  lifetimes. Isolation: confidential computing (AMD SEV-SNP, Intel TDX, Arm CCA) with remote attestation; side
  channels (Parts 8 and 9); disaggregated memory and accelerators (CXL); verified kernels (seL4, Part 54) and fast
  hypervisors, but not yet both at cloud scale. Four open problems and the ★ research problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs45.compute
python -m unittest tests.test_cs45_cloud
python tools/build.py cs45
```

## Problems, with solutions

1. **Next fit.** Prove that next fit uses at most twice the optimal number of bins, and give inputs on which it uses
   nearly twice.

   *Solution.* Let next fit use m bins with loads L₁, …, L_m. It opens bin i + 1 only when the item that starts it
   does not fit in bin i, so L_i + L_{i+1} > 1 for every i < m. Pair the bins (1, 2), (3, 4), …: the ⌊m/2⌋ pairs
   hold total size S > ⌊m/2⌋. Every packing needs at least S bins, so OPT ≥ S > ⌊m/2⌋, and since OPT is an integer,
   OPT ≥ ⌊m/2⌋ + 1 ≥ (m + 1)/2, that is, m ≤ 2·OPT − 1. For the lower bound take 2k items (k even) alternating ½ and
   ε = 1/k. After a bin holding ½ + ε the next ½ overflows, so every bin holds exactly one half and one small item,
   and next fit uses k bins. The optimum pairs the halves in k/2 bins and puts the k small items, of total 1, in one
   more; k/2 + 1 is also the total size, so OPT = k/2 + 1 and NF = 2·OPT − 2, a ratio tending to 2. With the
   instrument's ε = 0.01: 16 items take 8 bins against 5, and 400 take 200 against 102, a ratio of 1.96.

2. **NP-hardness.** Show that bin packing is NP-hard by reducing partition to deciding whether two bins suffice.

   *Solution.* Given positive integers a₁, …, a_n with sum S, form items x_i = a_i/(S/2); if some a_i > S/2 the
   answer is no, and we output any fixed no-instance (three items of 0.6). The items total 2, so two bins of size 1
   suffice exactly when each is filled exactly, that is, when some subset has Σ x_i = 1, that is, Σ a_i = S/2: a
   partition. (An odd S needs no special case: integer subset sums cannot equal S/2.) The map takes polynomial time,
   and partition is NP-complete (Karp, 1972; Part 26), so deciding whether OPT ≤ 2 is NP-hard, and so is bin packing.
   On screen: 3, 1, 1, 2, 2, 1 gives 0.6, 0.2, 0.2, 0.4, 0.4, 0.2, which split as {3, 1, 1} and {2, 2, 1} into two
   bins; 3, 3, 3, 1 gives 0.6, 0.6, 0.6, 0.2, where no two 0.6 share a bin, so three are needed. Corollary: a
   polynomial algorithm that always used fewer than 3/2·OPT bins would return 2 whenever OPT = 2 (fewer than 3) and
   so decide partition; no such algorithm exists unless P = NP. The bound is for the absolute ratio: asymptotically,
   packings within (1 + ε)·OPT + 1 can be found in polynomial time (Fernandez de la Vega and Lueker, 1981).

3. **Erlang C.** Derive Erlang C from the birth–death chain of an M/M/c queue, and the mean wait from it.

   *Solution.* Let the state k be the number of requests in the system. Arrivals move k to k + 1 at rate λ; with k
   requests, min(k, c) servers are busy, so departures move k to k − 1 at rate min(k, c)·μ. In equilibrium the flow
   across each cut balances, λπ_k = min(k + 1, c)·μ·π_{k+1}, which gives π_k = π₀·a^k/k! for k ≤ c, with a = λ/μ, and
   π_k = π_c·ρ^{k−c} for k ≥ c, with ρ = a/c < 1. Normalizing, 1/π₀ = Σ_{k<c} a^k/k! + (a^c/c!)/(1 − ρ). Poisson
   arrivals see time averages, so an arrival waits exactly when it finds k ≥ c:
   C(c, a) = Σ_{k≥c} π_k = π_c/(1 − ρ) = [a^c/(c!(1 − ρ))] / [Σ_{k<c} a^k/k! + a^c/(c!(1 − ρ))].
   The mean queue length is L_q = Σ_{j≥0} j·π_{c+j} = π_c·ρ/(1 − ρ)² = C(c, a)·ρ/(1 − ρ), and Little's law gives
   W_q = L_q/λ = C(c, a)·ρ/(λ(1 − ρ)) = C(c, a)/(cμ − λ). (Given that it waits, a request waits an exponential time
   of rate cμ − λ.) Checks: c = 1 gives C = ρ, Part 31's M/M/1; c = 2, a = 1 gives C = 1/(2 + 1) = 1/3 and
   W_q = 1/3 of a service time. With 10 erlangs, 13 servers give C = 0.285, over the 0.2 target, and 14 give
   C = 0.174 and W_q = 0.174/4 = 0.044 service times, which is why the table's first row is 14.

4. **Mean time to data loss.** Derive the mean time to data loss for n fragments of which any k suffice, with failure
   rate λ per fragment and one repair at a time at rate μ.

   *Solution.* Let the state i be the number of failed fragments; the data is lost on reaching i = n − k + 1. From
   state i ≤ n − k a failure occurs at rate λ_i = (n − i)λ and, for i ≥ 1, a repair at rate μ. Let T_i be the expected
   time to go from i to i + 1 for the first time. T₀ = 1/(nλ). For i ≥ 1, the chain leaves i after a mean
   1/(λ_i + μ); with probability λ_i/(λ_i + μ) it moves up, and otherwise it drops to i − 1, needs T_{i−1} to return,
   and then T_i again: T_i = 1/(λ_i + μ) + μ/(λ_i + μ)·(T_{i−1} + T_i), that is, λ_i·T_i = 1 + μ·T_{i−1}, or
   T_i = (1 + μ·T_{i−1})/((n − i)λ). To be lost the chain must climb every level in turn, so
   MTTDL = Σ_{i=0}^{n−k} T_i. Unrolling, T_i = Σ_{j≤i} μ^{i−j}/(λ_j λ_{j+1} ⋯ λ_i), and when μ ≫ λ the term j = 0 of
   the last level dominates: MTTDL ≈ μ^{n−k} / (n(n − 1)⋯k · λ^{n−k+1}). For three copies (n = 3, k = 1) with
   λ = −ln(0.98) per year = 2.305 × 10⁻⁶ per hour and μ = 1/24 per hour, μ²/(6λ³) = 2.36 × 10¹³ hours, 2.7 billion
   years, within 0.03% of the exact sum. If the time to loss is close to exponential, the chance of loss in a year is
   p = 1 − e^{−1/MTTDL} ≈ 1/MTTDL in years, 3.7 × 10⁻¹⁰, or 9.4 nines. One more fragment, and one more tolerated
   loss, multiplies the mean by about μ/(nλ) for the new n, with μ/λ ≈ 1.8 × 10⁴ here (one copy to two: 49.5 to
   447,521 years, a factor of 9,000). That is why the nines climb so fast, and why the result is only as good as the
   assumption that failures are independent.

5. **Build.** Add a reconciler for a second resource that depends on the first, and show it converges in dependency
   order after random deletions.

   *Solution sketch.* Use `control.plan` as the compare step. Declare, say, three volumes and five pods, each pod
   naming a volume in its dependency list, as name → (kind, properties, dependencies). Each pass: with probability p
   delete a random resource from `actual`, and with it everything that uses it (or mark those resources broken, so
   that the plan updates them); then call `plan(desired, actual)` and apply only its first step, one action per
   pass, like `reconcile`'s one start per step. Because the plan lists creates and updates in topological order, its
   first step always has its dependencies present: a missing dependency would itself be an earlier step. That is the
   convergence proof: let Φ be the number of steps in the plan; with no deletions each pass applies an applicable step
   and lowers Φ by one, so the reconciler reaches the desired state within Φ passes of the last deletion, whatever
   was deleted before. Test it as `tests/test_cs45_cloud.py` does: over many seeds, assert that `actual == desired`
   within |desired| passes after deletions stop, and that the log of applied steps never creates a pod before its
   volume. Running the same loop edge-triggered, acting on deletion events of which some are lost, shows it stuck
   short, as in chapter four.

6. **★ Research.** Online vector bin packing of jobs with unknown lifetimes, with predictions: near optimal when
   accurate, robust when not.

   *Discussion.* Open. Three difficulties compound. Even with sizes known on arrival and no departures, online vector
   packing in d resources has a competitive ratio that grows with d, and first fit's O(d) is nearly the best possible
   (Azar, Cohen, Kamara and Shepherd, 2013). With departures, the objective changes (the peak number of machines, or
   the machine-hours paid for), and an adversary can leave every machine holding one long-lived job. And lifetime
   predictions, learned from traces such as Azure's (Cortez et al., 2017), are noisy and heavy-tailed. A good answer
   would fix d (two is already interesting), an objective and a measure of prediction error η; give an algorithm
   whose cost is within a constant of the optimum when η = 0 and degrades smoothly in η to within a constant of the
   best prediction-free guarantee; and prove a matching trade-off between those two constants. Partial results, one
   dimension with lifetimes, or two dimensions with exact lifetimes, or a careful evaluation on public cluster
   traces, would already be useful.

## 习题与解答

1. **下次适应。** 证明下次适应算法使用的箱子数至多是最优值的两倍，并给出使它用到接近两倍的输入。

   *解答。* 设下次适应用了 m 个箱子，装载量为 L₁, …, L_m。只有当开启第 i + 1 个箱子的那件物品放不进第 i 个箱子时，它才会开新箱，
   所以对每个 i < m 都有 L_i + L_{i+1} > 1。把箱子两两配对 (1, 2)、(3, 4)、…：这 ⌊m/2⌋ 对的总尺寸 S > ⌊m/2⌋。任何装法都至少需要
   S 个箱子，所以 OPT ≥ S > ⌊m/2⌋；OPT 是整数，于是 OPT ≥ ⌊m/2⌋ + 1 ≥ (m + 1)/2，即 m ≤ 2·OPT − 1。下界：取 2k 件物品（k 为偶数），
   ½ 与 ε = 1/k 交替出现。装着 ½ + ε 的箱子放不下下一个 ½，所以每个箱子恰好装一个 ½ 和一件小物品，下次适应用 k 个箱子。最优解把
   两个 ½ 配成一箱，共 k/2 箱，再把总尺寸为 1 的 k 件小物品放进另一箱；k/2 + 1 也正是总尺寸，所以 OPT = k/2 + 1，NF = 2·OPT − 2，
   比值趋于 2。按仪器里的 ε = 0.01：16 件物品用 8 箱对 5 箱，400 件用 200 箱对 102 箱，比值 1.96。

2. **NP 难。** 通过把划分问题归约为“两个箱子是否够用”的判定，证明装箱问题是 NP 难的。

   *解答。* 给定和为 S 的正整数 a₁, …, a_n，构造物品 x_i = a_i/(S/2)；若某个 a_i > S/2，答案为否，输出任意一个固定的否实例（三件
   0.6）。物品总尺寸为 2，所以两个容量为 1 的箱子够用，当且仅当两个箱子都恰好装满，即存在子集使 Σ x_i = 1，也就是 Σ a_i = S/2：
   一个划分。（S 为奇数无须特殊处理：整数子集和不可能等于 S/2。）这个映射是多项式时间的，而划分问题是 NP 完全的（Karp，1972；
   第 26 部分），所以判定 OPT ≤ 2 是 NP 难的，装箱问题也就是 NP 难的。屏幕上的例子：3、1、1、2、2、1 变成 0.6、0.2、0.2、0.4、0.4、
   0.2，分成 {3, 1, 1} 和 {2, 2, 1} 两箱；3、3、3、1 变成 0.6、0.6、0.6、0.2，任意两个 0.6 都不能同箱，所以需要三箱。推论：若某个
   多项式算法总是用少于 3/2·OPT 个箱子，那么在 OPT = 2 时它必然给出 2（少于 3），从而判定了划分问题；除非 P = NP，这样的算法不存在。
   这个界针对绝对比值；渐近地看，多项式时间内可以找到 (1 + ε)·OPT + 1 以内的装法（Fernandez de la Vega 与 Lueker，1981）。

3. **厄朗 C。** 从 M/M/c 队列的生灭链推导厄朗 C 公式，并由它推出平均等待时间。

   *解答。* 设状态 k 为系统中的请求数。到达以速率 λ 把 k 变为 k + 1；有 k 个请求时，忙着的服务器有 min(k, c) 台，所以离开以速率
   min(k, c)·μ 把 k 变为 k − 1。平衡时每道割上的流量相等，λπ_k = min(k + 1, c)·μ·π_{k+1}，由此得到：k ≤ c 时 π_k = π₀·a^k/k!，
   其中 a = λ/μ；k ≥ c 时 π_k = π_c·ρ^{k−c}，其中 ρ = a/c < 1。归一化，1/π₀ = Σ_{k<c} a^k/k! + (a^c/c!)/(1 − ρ)。泊松到达看到的是
   时间平均，所以一个到达者需要等待，当且仅当它看到 k ≥ c：
   C(c, a) = Σ_{k≥c} π_k = π_c/(1 − ρ) = [a^c/(c!(1 − ρ))] / [Σ_{k<c} a^k/k! + a^c/(c!(1 − ρ))]。
   平均队长 L_q = Σ_{j≥0} j·π_{c+j} = π_c·ρ/(1 − ρ)² = C(c, a)·ρ/(1 − ρ)，由利特尔定律得 W_q = L_q/λ = C(c, a)·ρ/(λ(1 − ρ)) =
   C(c, a)/(cμ − λ)。（在需要等待的条件下，等待时间服从速率为 cμ − λ 的指数分布。）验算：c = 1 时 C = ρ，即第 31 部分的 M/M/1；
   c = 2、a = 1 时 C = 1/(2 + 1) = 1/3，W_q 为三分之一个服务时间。负载 10 爱尔兰时，13 台服务器给出 C = 0.285，超过 0.2 的目标；
   14 台给出 C = 0.174、W_q = 0.174/4 = 0.044 个服务时间，所以表的第一行是 14。

4. **平均数据丢失时间。** 对 n 个分片、任意 k 个即可恢复、每个分片失效率为 λ、每次只修复一个且修复率为 μ 的情形，推导平均数据丢失
   时间。

   *解答。* 设状态 i 为失效的分片数；到达 i = n − k + 1 时数据丢失。在状态 i ≤ n − k，失效以速率 λ_i = (n − i)λ 发生；i ≥ 1 时，
   修复以速率 μ 发生。设 T_i 为从 i 第一次到达 i + 1 的期望时间。T₀ = 1/(nλ)。对 i ≥ 1，链在 i 停留的平均时间为 1/(λ_i + μ)；以
   概率 λ_i/(λ_i + μ) 向上走，否则退到 i − 1，需要 T_{i−1} 才回到 i，然后再花 T_i：T_i = 1/(λ_i + μ) + μ/(λ_i + μ)·(T_{i−1} + T_i)，
   即 λ_i·T_i = 1 + μ·T_{i−1}，或 T_i = (1 + μ·T_{i−1})/((n − i)λ)。要丢失数据，链必须依次爬过每一级，所以
   MTTDL = Σ_{i=0}^{n−k} T_i。展开得 T_i = Σ_{j≤i} μ^{i−j}/(λ_j λ_{j+1} ⋯ λ_i)；当 μ ≫ λ 时，最后一级中 j = 0 的项占主导：
   MTTDL ≈ μ^{n−k} / (n(n − 1)⋯k · λ^{n−k+1})。三副本（n = 3，k = 1），λ = −ln(0.98) 每年 = 每小时 2.305 × 10⁻⁶，μ = 每小时
   1/24，μ²/(6λ³) = 2.36 × 10¹³ 小时，即 27 亿年，与精确和相差不到 0.03%。若丢失时间接近指数分布，一年内丢失的概率为
   p = 1 − e^{−1/MTTDL} ≈ 1/MTTDL（以年计），即 3.7 × 10⁻¹⁰，9.4 个 9。多一个分片、多容忍一次丢失，平均时间大约乘上 μ/(nλ)
   （n 取新的值），这里 μ/λ ≈ 1.8 × 10⁴（从一副本到两副本：49.5 年变成 447,521 年，约 9,000 倍）。所以 9 的个数涨得这么快；也正因
   如此，结果的好坏完全取决于“失效相互独立”这个假设。

5. **动手。** 给调和器加上依赖于第一种资源的第二种资源，并证明在随机删除之后它按依赖顺序收敛。

   *解答要点。* 用 `control.plan` 作比较这一步。比如声明三个卷和五个 pod，每个 pod 在依赖列表里写上一个卷，格式为 名字 →（种类，
   属性，依赖）。每一轮：以概率 p 从 `actual` 中删除一个随机资源，连同使用它的一切（或者把它们标记为损坏，让计划去更新它们）；然后
   调用 `plan(desired, actual)`，只执行它的第一步，每轮一个动作，就像 `reconcile` 每步只启动一个。因为计划按拓扑序列出创建和更新，
   它的第一步的依赖总是已经存在：缺失的依赖本身会是更靠前的一步。这就是收敛的证明：设 Φ 为计划的步数；没有删除时，每一轮执行一个
   可执行的步骤，使 Φ 减一，所以无论之前删了什么，调和器都会在最后一次删除之后的 Φ 轮之内到达期望状态。照 `tests/test_cs45_cloud.py`
   的写法测试：对许多随机种子，断言删除停止后 |desired| 轮之内 `actual == desired`，并断言执行日志中从不在卷之前创建 pod。把同一个
   循环改成边沿触发，依据会丢失的删除事件行动，就会像第四章那样停在不足的状态。

6. **★ 研究。** 寿命未知的作业的在线向量装箱，带预测：预测准确时接近最优，不准确时依然稳健。

   *讨论。* 尚未解决。三重困难叠加在一起。即使物品到达时尺寸已知、也没有离开，d 种资源的在线向量装箱的竞争比也随 d 增长，而首次适应
   的 O(d) 几乎已是最好（Azar、Cohen、Kamara 与 Shepherd，2013）。有了离开，目标就变了（同时使用的机器数的峰值，或付费的机器小时数），
   对手可以让每台机器只剩一个长寿命的作业。而从 Azure 等轨迹中学到的寿命预测（Cortez 等，2017）既有噪声又有重尾。好的答案应固定 d
   （d = 2 就已经有意思）、一个目标和一种预测误差的度量 η；给出一个算法，η = 0 时代价在最优值的常数倍以内，随 η 平滑退化，最差也在
   不用预测的最好保证的常数倍以内；并证明这两个常数之间相匹配的权衡。部分结果，比如带寿命的一维情形、寿命精确已知的二维情形，或在
   公开的集群轨迹上的细致评估，就已经有用。

## Glossary additions

* **warehouse-scale computer, rack, top-of-rack switch, hot and cold aisles** — a datacentre programmed as one
  machine; its unit of servers, switch and power feed; how air flows through the rows.
* **UPS, PDU, power capping, oversubscription** — the power chain's batteries and distribution; limiting power when
  installed servers could together exceed the building's budget.
* **energy proportionality, PUE** — power that falls with load; power entering the building over power reaching the
  computers.
* **KVM, virtual machine monitor, virtio, microVM, jailer** — the kernel half and the user-space half of a hypervisor;
  paravirtual devices; a VM with a minimal device model; the confinement around the monitor process.
* **gVisor, Kata Containers** — a user-space kernel answering a container's system calls; containers run in microVMs.
* **namespace, cgroup, cpu.max, memory.max, OOM killer** — what a process can see, and how much it may use.
* **image, layer, manifest, registry, OverlayFS, copy-up, whiteout, OCI** — content-addressed files for containers and
  how they are stored, merged, changed and standardized.
* **cluster (cell), pod, kubelet, Deployment, controller, etcd** — Kubernetes' (and Borg's) units and parts.
* **desired and observed state, reconciliation loop, level- and edge-triggered** — declaring a goal and closing the gap
  to it; acting on the current difference rather than on events.
* **bin packing, next fit, first fit, best fit, first fit decreasing, vector bin packing** — packing items into fewest
  bins; the classic heuristics; packing by several resources at once.
* **filter and score, priority, preemption** — how a scheduler picks a machine, and who gives way.
* **autoscaler, Horizontal Pod Autoscaler, gain, delay, quota** — a feedback controller on the number of servers.
* **M/M/c queue, Erlang C, square-root staffing** — c servers fed by Poisson arrivals; the chance of waiting; spare
  capacity growing like √a.
* **predictive scaling** — starting capacity ahead of forecast load.
* **serverless, function as a service, cold start, keep-alive, concurrency limit, throttling** — code run per event and
  billed per millisecond, and its costs.
* **block, file and object storage; bucket, key; read-after-write consistency** — three shapes of storage; what a read
  sees after a write.
* **erasure code, Reed–Solomon, fragment, parity, overhead** — storing data so that any k of n pieces rebuild it.
* **MTTDL, nines of durability, failure domain, correlated failure** — mean time to data loss; −log₁₀ of the yearly
  loss probability; what fails together.
* **VPC, subnet, route table, security group, internet gateway** — a tenant's private network and its rules.
* **overlay network, encapsulation, VXLAN, virtual switch** — tenant packets carried inside host packets.
* **load balancer, health check, layer 4 and layer 7, Maglev, anycast** — one address in front of many machines, near
  and far.
* **egress, data gravity** — the price of moving data out; why computation moves to data.
* **infrastructure as code, state file, plan, apply, drift, immutable infrastructure, snowflake** — the desired
  infrastructure in version control, and keeping the real one equal to it.
* **noisy neighbour, Cache Allocation Technology, Memory Bandwidth Allocation, CPI², antagonist** — interference
  between tenants, its partitioning and its detection.
* **prime and probe, co-residence, constant-time code** — a cache side channel, the placement it needs, a defence.
* **region, availability zone, spread constraint (anti-affinity), data residency, adequacy decision** — where things
  run, apart and within the law.
* **on demand, spot, checkpoint, Young's rule** — prices for capacity that can or cannot be taken back; saving progress
  at the right interval.
* **carbon intensity, carbon-aware scheduling** — emissions per kilowatt-hour; moving flexible work in time and space.
* **confidential computing, remote attestation, disaggregation, CXL, learning-augmented algorithm** — the frontier's
  encrypted VMs, pooled hardware and algorithms that use predictions.

## Sources

* L. A. Barroso, U. Hölzle and P. Ranganathan, *The Datacenter as a Computer: Designing Warehouse-Scale Machines*
  (3rd edn, 2018); B. Burns, J. Beda and K. Hightower, *Kubernetes: Up and Running* (2nd edn, 2019); K. Morris,
  *Infrastructure as Code* (2nd edn, 2020); M. Harchol-Balter, *Performance Modeling and Design of Computer Systems:
  Queueing Theory in Action* (2013).
* J. McCarthy, remarks at the MIT centennial (1961); M. Armbrust et al., "A view of cloud computing", Communications of
  the ACM 2010.
* X. Fan, W.-D. Weber and L. A. Barroso, "Power provisioning for a warehouse-sized computer", ISCA 2007; L. A. Barroso
  and U. Hölzle, "The case for energy-proportional computing", IEEE Computer 2007; The Green Grid, PUE white paper
  (2007); Uptime Institute, annual global data center surveys; Google, environmental reports; J. Dean, "Designs,
  lessons and advice from building large distributed systems", LADIS 2009 keynote.
* G. Popek and R. Goldberg, "Formal requirements for virtualizable third generation architectures", Communications of
  the ACM 1974; A. Kivity et al., "kvm: the Linux virtual machine monitor", Ottawa Linux Symposium 2007; F. Bellard,
  "QEMU, a fast and portable dynamic translator", USENIX ATC 2005; A. Agache, M. Brooker, A. Florescu, A. Iordache,
  A. Liguori, R. Neugebauer, P. Piwonka and D.-M. Popa, "Firecracker: lightweight virtualization for serverless
  applications", NSDI 2020.
* A. Verma, L. Pedrosa, M. Korupolu, D. Oppenheimer, E. Tune and J. Wilkes, "Large-scale cluster management at Google
  with Borg", EuroSys 2015; B. Burns, B. Grant, D. Oppenheimer, E. Brewer and J. Wilkes, "Borg, Omega, and
  Kubernetes", ACM Queue 2016.
* E. G. Coffman Jr, M. R. Garey and D. S. Johnson, "Approximation algorithms for bin packing: a survey", in
  D. Hochbaum (ed.), *Approximation Algorithms for NP-Hard Problems* (1996); D. S. Johnson, *Near-Optimal Bin Packing
  Algorithms* (PhD thesis, MIT, 1973); G. Dósa, "The tight bound of first fit decreasing bin-packing algorithm is
  FFD(I) ≤ 11/9 OPT(I) + 6/9", ESCAPE 2007; R. Karp, "Reducibility among combinatorial problems" (1972);
  W. Fernandez de la Vega and G. Lueker, "Bin packing can be solved within 1 + ε in linear time", Combinatorica 1981;
  Y. Azar, I. R. Cohen, S. Kamara and B. Shepherd, "Tight bounds for online vector bin packing", STOC 2013.
* J. C. Maxwell, "On governors", Proceedings of the Royal Society 1868; A. K. Erlang, "Solution of some problems in
  the theory of probabilities of significance in automatic telephone exchanges" (1917); S. Halfin and W. Whitt,
  "Heavy-traffic limits for queues with many exponential servers", Operations Research 1981.
* E. Jonas et al., "Cloud programming simplified: a Berkeley view on serverless computing", UC Berkeley technical
  report, 2019; M. Shahrad et al., "Serverless in the wild: characterizing and optimizing the serverless workload at a
  large cloud provider", USENIX ATC 2020.
* M. Mahalingam et al., "Virtual eXtensible Local Area Network (VXLAN)", RFC 7348 (2014); M. Dalton et al.,
  "Andromeda: performance, isolation, and velocity at scale in cloud network virtualization", NSDI 2018; D. E. Eisenbud
  et al., "Maglev: a fast and reliable software network load balancer", NSDI 2016.
* M. Burgess, "Cfengine: a site configuration engine", USENIX Computing Systems 1995.
* X. Zhang, E. Tune, R. Hagmann, R. Jnagal, V. Gokhale and J. Wilkes, "CPI²: CPU performance isolation for shared
  compute clusters", EuroSys 2013; J. Schad, J. Dittrich and J.-A. Quiané-Ruiz, "Runtime measurements in the cloud:
  observing, analyzing, and reducing variance", VLDB 2010; D. A. Osvik, A. Shamir and E. Tromer, "Cache attacks and
  countermeasures: the case of AES", CT-RSA 2006; T. Ristenpart, E. Tromer, H. Shacham and S. Savage, "Hey, you, get
  off of my cloud: exploring information leakage in third-party compute clouds", CCS 2009.
* Regulation (EU) 2016/679 (GDPR); Court of Justice of the European Union, Case C-311/18 (*Schrems II*), 2020.
* J. W. Young, "A first order approximation to the optimum checkpoint interval", Communications of the ACM 1974;
  T. Lykouris and S. Vassilvitskii, "Competitive caching with machine learned advice", ICML 2018; E. Cortez et al.,
  "Resource Central: understanding and predicting workloads for improved resource management in large cloud
  platforms", SOSP 2017; International Energy Agency, *Electricity 2024* (2024).
* AWS documentation and price lists for us-east-1 (2024): EC2, Lambda (pricing and quotas), S3 (pricing, durability,
  and strong read-after-write consistency since December 2020), data transfer.
