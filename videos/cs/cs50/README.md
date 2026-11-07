# Computer Science, Built — Part 50: Keeping It Running

Part 50 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth and last part of Act IX, *Systems at Scale*. A system is only as good as
its worst hour, and reliability engineering turns that into arithmetic: availability composes in series and in
parallel, an error budget makes unreliability a resource to spend, retries can hold a server in collapse long after
its trigger has gone, and metrics, traces and profiles tell you what actually happened, provided they do not lie. The
part ends by breaking the Job's own service on purpose and pricing each defence against the month's error budget.

The instruments are in `explainer/cs/ops/` (tested in `tests/test_cs50_ops.py`), with Part 45's Erlang C
(`explainer/cs/cloud/control.py`), Part 46's KLL (`explainer/cs/data/columnar.py`), Part 38's Raft cluster
(`explainer/cs/dist/raft.py`) and the Pebble emulator:
* `reliability.py`: nines as downtime per year, 30-day month and week; `evaluate`, availability of a tree of series,
  parallel and k-of-n parts (k of n exactly, by a dynamic program over parts of different availability); the two laws
  on parts of 99%; a request path (DNS, load balancers, app servers, database) replicated against built from one of
  each; an alternating renewal process (exponential up times of mean 720 h, repairs of mean 2 h, 200 years) against
  MTBF/(MTBF + MTTR), and the two levers; common-mode failure, three replicas of 99.9% with a share c of each one's
  downtime shared, by Monte Carlo (2,000,000 trials) against the exact (1 − cq)(1 − q′³); a Raft majority; N + k.
* `slo.py`: a synthetic 30-day month (Poisson requests around 1,000 a minute, binomial errors, background rate 0.01%)
  with six incidents (three blips, an outage, a degradation, a slow leak); the budget spent minute by minute and by
  incident; burn-rate thresholds b = f × 720 h / w; five alerting rules from *The Site Reliability Workbook* scored
  for detection time, reset time, missed significant incidents (at least 2% of the budget) and needless pages.
* `overload.py`: clients contending for one record under optimistic concurrency (a write fails if another starts
  within one unit of it) with five backoff strategies; a server of capacity 100 a second, simulated in 10 ms steps,
  with users sending 80 a second, a 1 s client timeout, three retries and a trigger that halves capacity from 30 s to
  40 s, under six policies (no retries, immediate retries, backoff with full jitter, a 10% retry budget as a token
  bucket, server-side shedding of requests that have waited over 0.5 s, client circuit breakers); the trigger sizes
  that tip it into the bad state; one thread pool against two bulkheads; hedged requests.
* `observe.py`: DDSketch (Masson, Rim and Lee) and an HDR-style log-linear histogram (128 sub-buckets per power of
  two) against KLL and a sample of 1,000, on 200,000 latencies (lognormal around 20 ms, 5% cache misses around 120 ms,
  a 0.5% Pareto tail); ten servers, one four times slower, for the average of p99s against the fleet's p99; synthetic
  traces of nine spans with parallel children, their critical path, and head against tail sampling; coordinated
  omission, a closed-loop generator against the latencies from intended send times; exact mean-value analysis of a
  closed system against M/M/1 at the same throughput; change-point detection with a permutation test.
* `profile.py`: a sampling profiler of Pebble running version zero of the Job (every 997th instruction's program
  counter mapped to its label, the labels to routines, the routines to stacks), checked against an exact count of
  every instruction with binomial standard errors; flame-graph rectangles from folded stacks; a CPU-time timer signal
  (`SIGPROF`, 1,000 Hz) sampling the emulator's own Python stack.
* `chaos.py`: the Job's counting service as three replicas under a crash, a partition and a slow replica, with three
  client configurations; Part 38's five-node Raft cluster under a script of crashes and a partition, with its safety
  checker.

`compute.py` also plans the Job service's capacity by Erlang C, and appends ledger row 19 to Part 49's ledger.

## Chapters

* **Hook.** Three post-mortems, from the companies' own public reports: Amazon S3 on 28 February 2017 (one mistyped
  input to a tool removed far more capacity than meant, including two subsystems the region depended on), Cloudflare
  on 2 July 2019 (a firewall rule's regular expression backtracking catastrophically, Part 12, pushed everywhere at
  once) and CrowdStrike on 19 July 2024 (a content update that made a kernel driver read out of bounds, crashing
  about 8.5 million Windows machines by Microsoft's estimate). Each a routine change pushed too far, too fast. A
  year has 525,960 minutes: 99% allows 3.7 days of downtime, 99.9% 8.8 hours, 99.99% 53 minutes (4.3 a month),
  99.999% 5 minutes (0.4 a month).
* **1. Availability arithmetic.** Nines = −log₁₀(1 − A); downtime = (1 − A) × T: two nines 3.7 days a year, three
  nines 43.2 minutes a 30-day month, four nines 4.3 minutes a month or 1.0 a week, five nines 5.3 minutes a year.
  Series and parallel as Part 3's switch circuits: 2, 10 and 50 parts of 99% in series give 98.0%, 90.4% and 60.5%; 2
  and 3 in parallel give 99.99% and 99.9999%. A request path of four replicated stages (four name servers, two load
  balancers at 99.9%, three app servers at 99%, a database pair at 99.9%; illustrative) is 99.9997%, 5.5 nines, 1.6
  minutes a year; one of each is 98.70%, 1.9 nines, 4.7 days. One simulated server's year (9 failures);
  720/(720 + 2) = 99.72%, and 200 simulated years give 99.7%. Halving failures and halving repair time are worth
  exactly the same (24.3 hours down a year to 12.2; 2.6 nines to 2.9); repairing in 10 minutes gives 2.0 hours and 3.6
  nines. Correlated failure: three replicas of 99.9% promise 9.0 nines, but with 1%, 5%, 10% and 30% of each one's
  downtime common they give 5.0, 4.3, 4.0 and 3.5; the shared cause is a switch in series, A = (1 − cq)(1 − q′³).
* **2. SLOs and error budgets.** Indicator, objective, agreement (99.9% over 30 days; an SLA of 99.5%, illustrative);
  this month's SLI 99.945%. The budget, one bad request in a thousand or 43.2 minutes of total outage, draining over
  the synthetic month: the outage (25 minutes at 25%) takes 14.5%, the degradation (6 hours at 1.2%) 10.1%, the slow
  leak (3 days at 0.2%) 18.8%, the three blips 1.6% and background errors 9.9%: 54.9% spent. Burn rate b = error
  rate/(1 − SLO): the budget lasts 30 days/b (15 days at 2, 5 days at 6, 50 hours at 14.4); to page at a share f
  within a window w, b = f × 720 h/w: 2% in 1 hour gives 14.4 (1.44% errors, page), 5% in 6 hours 6.0 (0.60%, page),
  10% in 3 days 1.0 (0.10%, ticket). Five rules scored on the month: errors above 0.1% over 10 minutes catches
  everything at once but pages 20 times, 3 of them needlessly; over 36 hours it is quiet for the blips but takes 2.7
  hours for the degradation and 16.6 for the leak, and keeps paging 35.9 hours after the outage; a single burn of 14.4
  over an hour pages for the outage in 3 minutes and misses the degradation and the leak; two burn rates with a ticket
  catch all three significant incidents (outage 3 minutes, degradation 3.0 hours, leak 34.2 hours by ticket), but the
  outage alert lasts 5.9 hours after it ends; the multiwindow, multi-burn-rate rule (a short window a twelfth as long
  must agree) detects the same and stops 29 minutes after the outage.
* **3. How systems fail: gray, cascading, metastable.** Fault models nested from fail-stop (Schlichting and Schneider
  1983) through crash, omission and timing to arbitrary, and gray failure outside the ladder (chapter 15). A cascade
  (illustrative): five servers at 72% each, u = u₀ n/(n − k), one lost puts four at 90%, a second puts three at 120%,
  and the rest go. A metastable failure simulated: without retries the server is answering again 11 s after the
  trigger ends; with three immediate retries the sent load climbs to about 320 a second, four times what users send,
  and requests answered in time stay at zero for the remaining 80 s. The loop (a long queue, timeouts, retries, load
  above capacity) and its states, stable, vulnerable, metastable (Bronson et al. 2021; Huang et al. 2022).
* **4. Timeouts, retries, backoff and jitter.** Timeouts a little above the dependency's p99.9, deadlines passed
  downstream; three layers trying four times each turn one tap into 64 attempts, so retry at one layer, and only
  idempotent requests (Part 43). Twenty clients on one record: no backoff makes 29,279 attempts by t = 3,000 and none
  finishes; exponential backoff 240 and none finishes; full jitter finishes all twenty by t = 318 after 175 attempts.
  Brooker's comparison with 100 clients (base 1, cap 1,000, ten runs): no backoff 975,654 calls and exponential 2,900,
  neither ever done by t = 20,000; full jitter 1,071 calls, all done at 1,624; equal jitter 1,059 at 2,124;
  decorrelated jitter 1,789 at 1,864 (with 50 clients decorrelated finishes first, 684 against 807). Back on chapter
  three's server, backoff with full jitter still sends about 320 a second and answers none; a 10% retry budget keeps
  the load near 80 and answers again 19 s after the trigger. Hedged requests (Dean and Barroso 2013): replies
  exponential with mean 5 ms but 2% hitting a 200 ms pause; p99 203 ms unhedged, 53 ms hedging at 50 ms for 2.0% more
  requests, 25 ms at 20 ms for 3.7% (19 ms at 12 ms for 10.8%).
* **5. Breakers, bulkheads and load shedding.** The circuit breaker's three states (Nygard 2007); ours opens for 5 s
  when over half of the last second's calls failed, letting 5% through as probes. On chapter three's trigger the
  breakers are open from 32 s to 38 s, and 9,110 requests are answered in time against 2,567. Shedding requests that
  have waited over 0.5 s (a rejection costs a fiftieth of an answer): at most 226 sent a second, 46 to 49 answered a
  second through the trigger, normal at once after; CoDel's idea (Part 37) in services, and Maurer's account of
  Facebook switching to newest-first. The six policies over 120 s (users send 80 a second, about 9,600 in all): no
  retries 8,078 (recovers after 11 s), immediate retries 2,567 and with backoff 2,567 (never recover), the retry
  budget 7,530 (after 19 s), shedding 9,355 and breakers 9,110 (never stuck). Bulkheads: 30 threads serving A at 40 a
  second and B at 20; when B turns slow (2 s a call instead of 50 ms, from 20 s to 40 s) the shared pool lets only 28%
  of calls to healthy A succeed in its worst second; two bulkheads of 15 leave A untouched, and B averages 40% while
  slow. Degrading instead of failing, backpressure (Part 43), and shedding by criticality as in Google's SRE book.
* **6. Redundancy.** Ten machines' capacity from machines up 99% of the time: N gives 90.4% (1.0 nines), N + 1 99.48%
  (2.3), N + 2 99.979% (3.7), N + 3 99.99933% (5.2); Gray's 1985 Tandem study (operations and software, not hardware,
  caused most outages). Active–passive against active–active: to lose one of n sites run each below (n − 1)/n, the
  cascade arithmetic in reverse (two sites at 45% each, one left at 90%). Evacuating one of three regions at 60%
  leaves two at 90%; headroom, data already replicated (recovery point and recovery time) and practice. A Raft group's
  availability, the binomial tail above a majority: at 99% a node, 1, 3, 5 and 7 nodes give 2.0, 3.5, 5.0 and 6.5
  nines; at 99.9%, 3.0, 5.5, 8.0 and 10.5. Even sizes buy nothing; shared causes cap the nines.
* **7. Metrics, and why averages lie.** Counters, gauges and histograms (Prometheus, 2012). Two hundred thousand
  simulated latencies: mean 30.4 ms, median 20.5 ms, p99 177 ms, p99.9 834 ms, maximum 104 s; a page making 100
  requests meets one beyond the p99 63% of the time. Ten servers, one four times slower: nine p99s of about 170 to 182
  ms and one of 719; their average is 230 ms, the fleet's true p99 270 ms, and the ten DDSketches merged bucket by
  bucket give 268 ms. DDSketch's guarantee derived (γ = (1 + α)/(1 − α), x̂ = 2γⁱ/(γ + 1), |x̂ − x| ≤ αx); at α = 1%
  these latencies, 4 ms to 104 s, fill 332 buckets. Four summaries against the true quantiles (relative error at p50,
  p90, p99, p99.9 and p99.99): DDSketch 0.9%, 0.8%, 0.5%, 0.4%, 0.8% in 332 buckets; the log-linear (HdrHistogram)
  layout 0.1%, 0.2%, 0.1%, 0.0%, 0.3% in 1,070; KLL (Part 46) 0.7%, 0.5%, 9.8%, 48.5%, 84.7% with 238 values, since it
  bounds the error in rank; a sample of 1,000 0.5%, 2.1%, 2.2%, 52.0%, 68.0%. Cardinality (illustrative): 5
  methods × 8 statuses × 40 routes × 200 instances = 320,000 series; a user label for a million users makes
  3.2 × 10¹¹.
* **8. Logs and traces.** Structured logs as named fields, queries over them, and the trace id that joins them. Spans
  with trace, span and parent ids (Dapper, 2010), carried in the W3C `traceparent` header; OpenTelemetry. One
  synthetic trace of nine spans as a waterfall, catalog and recommender in parallel: 32.6 ms. Its critical path, the
  longest path through the DAG of work (Part 19): model 12.6 ms, render 6.0, features 5.8, recommender 4.0, front end
  2.4, auth 1.7; the catalog and its 12.5 ms database are off it, with 7.3 ms of slack. Sampling 50,000 traces (876
  with an error, 4,307 slower than 100 ms): head sampling at 1% kept 533, of them 4 errors and 54 slow ones; tail
  sampling kept 5,584, every error and every slow trace.
* **9. Coordinated omission.** A closed-loop generator meant to send 100 requests a second to a server that answers in
  1 ms but freezes for 4 s in every 40 (10% of the time): of 20,000 requests due in 200 s it measured 18,005, and the
  1,995 skipped are exactly those that would have waited. The closed loop reports 1.0 ms at p50, p90, p99 and p99.9, a
  maximum of 4.0 s and a mean of 2.1 ms; measured from intended send times, p50 1.0 ms, p90 402 ms, p99 3.6 s, p99.9
  4.0 s, mean 223 ms. The ramp of true waits through one freeze; Tene's name for it, wrk2's open loop and
  HdrHistogram's correction. Open against closed load (Schroeder, Wierman and Harchol-Balter 2006): 10 to 150 users
  thinking for 1 s with 10 ms requests; at 92% busy the closed system answers in 82 ms and an open one at the same
  throughput (M/M/1, Part 31) in 132 ms; at 150 users the closed mean is 500 ms and the open one 15,358 s.
* **10. Profiling and flame graphs.** Pebble runs version zero of the Job on 20,000 bytes of a novel: 6,292,955
  instructions, every 997th sampled (a prime, so as not to fall into step with a loop), 6,311 samples (scan 2,702,
  next 2,470, cmp 756, lower 108, read 105, the rest 170). The binomial standard error √(p̂(1 − p̂)/n) checked against
  exact counts: scan sampled at 42.81% ± 0.62 against 43.46% exactly (z = −1.0), next 39.14% ± 0.61 against 38.32%
  (+1.3), cmp 11.98% against 12.09% (−0.3), found 0.29% against 0.17% (+2.2); `pdig` ran 1,386 instructions and drew
  no sample. The flame graph (Gregg 2011): `word` 94.5% of samples, `scan` and `next` 82%, walking an unsorted table
  entry by entry, so the fix is Part 17's hash table. The emulator's own Python profiled by a 1,000 Hz CPU-time timer
  (600 samples): `step` itself 60%, `load` 15%, the decoded-instruction cache 12%, the loop in `run` 11%. Off-CPU
  time, and eBPF summing waits by stack in the kernel (Part 31).
* **11. Performance method and capacity.** USE for every resource and RED for every service (an illustrative disk only
  60% busy yet saturated); Google's four golden signals. The roofline again (Williams, Waterman and Patterson 2009;
  schematic). Capacity for the Job service by Erlang C (Part 45), 80 ms a book, mean wait under 20 ms and at most 20%
  waiting: 12, 35, 100, 300 and 1,000 books a second need 3, 5, 12, 30 and 90 servers, 32%, 56%, 67%, 80% and 89%
  busy, with 2.0, 2.2, 4.0, 6.0 and 10.0 spare against √(busy) of 1.0, 1.7, 2.8, 4.9 and 8.9. A 3% regression from
  commit 52 of 80 under 2% noise: a naive 5% rule fires five times (commits 4, 49, 52, 68, 77); change-point detection
  splits at commit 52, mean 1.000 to 1.032, and none of 2,000 shuffles splits as well.
* **12. Incidents and post-mortems.** An incident minute by minute (illustrative): a change at minute 2, errors at 4,
  the fast-burn page at 11, acknowledged at 13, declared at 16, the status page at 21, rolled back at 34, recovered at
  37; time to detect and time to mitigate; about 70% of Google's outages came from changes to a live system. Incident
  command (from the firefighters' Incident Command System): commander, operations, communication, planning. The
  blameless post-mortem and its sections, "where we got lucky" among them (Allspaw 2012). Reason's Swiss-cheese model
  with the four holes of the S3 outage. Six of Cook's eighteen observations (1998).
* **13. Chaos engineering.** Chaos Monkey and the Simian Army (Netflix, 2011); Basiri et al.'s principles (2016):
  steady state, hypothesis, real-world events, a difference between experiment and control, in production,
  continuously. Blast radius: 1% of traffic to the experiment and 1% to a control; crashing one of three replicas
  under the naive client loses 33% of the experiment's requests, and aborting after a minute costs 0.008% of the
  month's error budget, against 13% for chapter 14's whole hour on all traffic. Injecting crashes, partitions and
  slowness (`tc netem`); the hypotheses for Part 38's Raft cluster, written before the run.
* **14. The Job service under faults.** Three counter replicas, 20 requests a second (lognormal, median 40 ms); the
  steady state: 99.9% of requests answered within 300 ms. Counter 1 crashes from minute 10 to 15, counter 2 is cut off
  from 25 to 30, counter 3 is ten times slow from 40 to 50. The naive client keeps 66.7% of requests through the crash
  and the partition and 76% while one is slow, 90.48% over the hour; a 150 ms timeout with one retry elsewhere keeps
  99.91%; adding outlier ejection (five failures in a row) and a hedge at 100 ms keeps 100.00%. The cost: 6,835, 66
  and 0 bad requests, 13.22%, 0.13% and 0.00% of the month's budget, for 0.0%, 11.3% and 1.2% extra requests. Raft
  under a crashed leader, a minority partition and two crashed followers: 1,195 of 1,221 commands committed; besides
  the first second, before a leader is elected, the share dips only in the seconds of the leader crash (67%) and the
  partition (50%), not at all when two followers crash, and the safety checker finds no violation. Ledger row 19:
  thirty books on 42 workers, one ten times slow, take 0.71 s without hedging and 0.30 s with a hedge at 240 ms
  (healthy and unhedged, 0.32 s), for 2.0 extra requests a run.
* **15. Frontier: gray failure and metastability.** Gray failure and differential observability (Huang et al. 2017);
  health judged from real requests, as the Job's best client did. Where a trigger tips chapter three's server over:
  capacity left 90%, 80%, 70%, 60% and 50% for 2, 5, 10 and 20 s; 7 of the 20 triggers leave it collapsed a minute
  after they end (70% and 60% for 10 s or more, 50% for 5 s or more). Research on metastability models, safer change
  and machines on call. Four open problems and the ★ research problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs50.compute
python -m unittest tests.test_cs50_ops
python tools/build.py cs50
```

## Problems, with solutions

1. **Availability.** A request needs five services of 99.95% each, and each has two replicas. What is its
   availability, and what if 10% of each service's downtime is common-mode?

   *Solution.* Each replica is down q = 0.0005 of the time. With independent replicas a service is down only when both
   are, q² = 2.5 × 10⁻⁷, so it is up 1 − q², and five services in series give (1 − q²)⁵ ≈ 1 − 5q² = 1 − 1.25 × 10⁻⁶:
   99.99988%, 5.9 nines, about 0.66 minutes (39 s) a year. (Without the replicas, 0.9995⁵ = 99.750%, 2.6 nines, 21.9
   hours a year.) Now let a share c = 0.1 of each replica's downtime be a common event that takes both replicas down,
   as in chapter 1: the common part is down cq = 5 × 10⁻⁵ of the time, and to keep each replica's own downtime at q
   the independent part is down q′ = (1 − c)q/(1 − cq) = 4.5002 × 10⁻⁴. A service is up when the common cause is
   absent and not both independent parts are down: (1 − cq)(1 − q′²) = 1 − 5.020 × 10⁻⁵, 4.3 nines. Five in series:
   (1 − 5.020 × 10⁻⁵)⁵ = 99.9749%, 3.6 nines, 132 minutes (2.2 hours) a year, two hundred times the independent
   figure. To first order the unavailability is 5(cq + q′²) ≈ 5cq: the common-mode share acts as a part in series,
   each service is capped at 1 − cq, and the replicas' squared term no longer matters.

2. **Burn-rate threshold.** Derive the burn-rate threshold that pages when 5% of a 30-day budget is spent in 6 hours,
   and the time to detect a burn rate of 10.

   *Solution.* With N requests in the month, the budget is (1 − SLO)N errors. A burn rate b means an error rate
   b(1 − SLO), so a window of w hours, holding N w/720 requests, spends b(1 − SLO)N w/720, a share b w/720 of the
   budget. Setting that equal to f gives b = f × 720 h/w = 0.05 × 720/6 = 6: at a 99.9% objective, an error rate of
   0.6% over six hours. A burn of 10 starting from a clean window raises the 6-hour average burn as 10t/6 after t
   hours, which reaches 6 at t = 6 × 6/10 = 3.6 hours (3.58 with chapter 2's background burn of 0.1). In general the
   long window detects a burn b ≥ b* after w b*/b, when the budget spent is b(w b*/b)/720 = f, the same 5% whatever b
   is: a faster burn is caught sooner but not more cheaply. The multiwindow rule's 30-minute window reaches 6 after 18
   minutes, so the 6-hour window governs. The 1-hour threshold of 14.4 never fires on a burn of 10, which would
   exhaust the budget in 72 hours. Check against chapter 2: the degradation burned at 12 and was paged after 179
   minutes, against 6 × 6/12 = 3 hours (2.97 with the background).

3. **Retry amplification.** Show that with L layers each retrying r times, a failing backend sees (r + 1)ᴸ attempts,
   and that a 10% retry budget bounds it by 1.1ᴸ.

   *Solution.* Number the layers 1 to L from the user, with layer L calling the backend, and let aₖ be the attempts
   layer k makes per user action. While the backend fails, every attempt fails all the way up, so each request a layer
   receives becomes r + 1 attempts downstream: a₁ = r + 1 and aₖ = (r + 1)aₖ₋₁, and by induction the backend sees
   a_L = (r + 1)ᴸ (64 for chapter 4's three layers of four tries; 4¹⁰ ≈ 10⁶ for ten). A retry budget lets a client add
   retries worth at most a share β = 0.1 of its first attempts, as a token bucket earning β tokens per first attempt
   and holding at most B. A layer's first attempts are the requests it received, nₖ₋₁ (retries from above arrive as
   new requests), so over any period nₖ ≤ (1 + β)nₖ₋₁ + B, and by induction the backend sees at most
   1.1ᴸn₀ + B(1.1ᴸ − 1)/0.1 attempts for n₀ user actions: 1.1ᴸ per action in the long run (1.331 for three layers,
   2.59 for ten), plus a burst bounded by the buckets. The bound is multiplicative per layer, which is why retrying at
   one layer only, as chapter 4 advises, does better still: 1.1.

4. **DDSketch.** Prove DDSketch's guarantee: every value in bucket i is within relative error α of 2γⁱ/(γ + 1).

   *Solution.* With γ = (1 + α)/(1 − α), a value x goes to bucket i = ⌈log_γ x⌉, so γⁱ⁻¹ < x ≤ γⁱ. Then
   x̂/x = 2γⁱ/((γ + 1)x) lies in [2γⁱ/((γ + 1)γⁱ), 2γⁱ/((γ + 1)γⁱ⁻¹)) = [2/(γ + 1), 2γ/(γ + 1)). Since
   γ + 1 = 2/(1 − α), 2/(γ + 1) = 1 − α and 2γ/(γ + 1) = γ(1 − α) = 1 + α, so 1 − α ≤ x̂/x < 1 + α, that is,
   |x̂ − x| ≤ αx. The estimate is the harmonic mean of the bucket's ends, the one point equally far from both in
   relative terms. For quantiles: bucket counts are exact, so the bucket in which the cumulative count first passes
   the rank holds the true q-quantile, and the answer is within α of it. Merging sketches with the same α adds counts
   bucket by bucket, so the merged sketch is exactly the sketch of the union and keeps the guarantee, which is why
   chapter 7's merged p99 (268 ms) is right where the average of p99s (230 ms) is not. Values from m to M need at most
   about log_γ(M/m) ≈ ln(M/m)/(2α) buckets: about 509 for 4 ms to 104 s at α = 1%, of which our latencies fill 332.

5. **Build.** Add a circuit breaker and a retry budget to a client, and measure goodput through a capacity drop.

   *Solution notes.* Start from `overload` in `explainer/cs/ops/overload.py`, which already has a `"breaker"` and a
   `"budget"` policy, each tested with `policy == ...`. Let a policy name a set of mechanisms (for example
   `"breaker+budget"`, tested by membership), so that a timed-out request is retried only if the breaker is closed and
   the client holds a token (0.1 earned per first attempt, at most 10). The simulator's breaker is one state shared by
   all clients, open for 5 s when over half of the last second's attempts failed, with 5% of calls passing as probes;
   a fuller answer gives each of several clients its own three-state machine (closed: count failures over a sliding
   window with a minimum number of calls; open: fail fast for a cool-down; half-open: admit a few probes, close if
   they succeed, reopen if not). Measure goodput per second and in total, offered load, and `recovered_s`, the time
   after the trigger until goodput is back to 90% of demand, on chapter three's trigger and over the grid of
   `trigger_sizes`. A quick version of the combined policy answers 9,098 requests in time on chapter three's trigger
   (breakers alone 9,110, the budget alone 7,530): here the breaker does the work. On a deeper, longer drop, to 30%
   for 20 s, the budget alone did not recover within the run (2,496 answered), because the server still serves, first
   come first served, a backlog of requests whose clients have given up and drains it only at the headroom the budget
   leaves, while the combined client answered 8,133 and recovered one second after the drop ended. Tests to add: the
   combined policy recovers on every cell of the grid; while a breaker is open the offered load stays near the probe
   rate; retries never exceed 10% of first attempts plus the bucket.

6. **★ Research.** The exact set of triggers a retrying server cannot recover from.

   *Discussion.* Open. For a server of capacity μ, users sending λ < μ, a client timeout τ and r retries, two steady
   states can coexist: the good one, with a short queue and no timeouts, and a bad one in which every request waits
   past τ, so each user request becomes r + 1 attempts and the offered load is λ(r + 1), self-sustaining when
   λ(r + 1) > μ (chapter 3: 80 × 4 = 320 > 100). The trigger set is the set of perturbations, here a capacity fraction
   f for a duration D, that carry the state out of the good state's basin of attraction. What makes it hard is the
   state: a FCFS queue with deadlines is described by the ages of everything waiting, an infinite-dimensional, delayed
   and stochastic system, and the outcome near the boundary depends on more than the backlog. Our grid shows this: a
   drop to 70% for 10 s and a drop to 60% for 5 s both leave a deficit of about 100 requests, yet the first collapses
   and the second recovers, most likely because the first spends longer with waits past the timeout, generating
   retries. Near the boundary the outcome is random, so the exact set is really a probability of collapse as a
   function of (f, D). A good partial answer would take a fluid or diffusion model with an explicit treatment of
   timeouts and abandoned work, prove the bistability condition, and give inner and outer bounds on the collapse
   region (states from which recovery is certain, and states from which it is impossible) that are close to each other
   and agree with `trigger_sizes` over a range of λ, μ, τ and r; a closed form for the boundary in the deterministic
   limit would already be new.

## 习题与解答

1. **可用性。** 一个请求要经过五个服务，每个 99.95%，每个服务有两个副本。它的可用性是多少？如果每个服务的停机时间中有 10% 是
   共因的，又是多少？

   *解答。* 每个副本有 q = 0.0005 的时间停机。副本相互独立时，只有两个都停机，服务才停机，概率为 q² = 2.5 × 10⁻⁷，所以服务的可用性
   为 1 − q²；五个服务串联得 (1 − q²)⁵ ≈ 1 − 5q² = 1 − 1.25 × 10⁻⁶：99.99988%，5.9 个九，每年约 0.66 分钟（39 秒）。（没有副本时，
   0.9995⁵ = 99.750%，2.6 个九，每年 21.9 小时。）现在像第 1 章那样，设每个副本停机时间中有 c = 0.1 的份额是让两个副本同时停机的共因
   事件：共因部分有 cq = 5 × 10⁻⁵ 的时间停机；为了让每个副本自身的停机时间仍为 q，独立部分的停机比例为
   q′ = (1 − c)q/(1 − cq) = 4.5002 × 10⁻⁴。共因不发生、且两个独立部分不同时停机时，服务才可用：(1 − cq)(1 − q′²) = 1 − 5.020 × 10⁻⁵，
   4.3 个九。五个串联：(1 − 5.020 × 10⁻⁵)⁵ = 99.9749%，3.6 个九，每年 132 分钟（2.2 小时），是独立情形的两百倍。一阶近似下不可用度为
   5(cq + q′²) ≈ 5cq：共因份额相当于一个串联的部件，每个服务的可用性被封顶在 1 − cq，副本带来的平方项已无关紧要。

2. **消耗速率阈值。** 推导在 6 小时内花掉 30 天预算的 5% 时发出呼叫的消耗速率阈值，以及消耗速率为 10 时的检测时间。

   *解答。* 一个月有 N 个请求，预算为 (1 − SLO)N 个错误。消耗速率 b 意味着错误率为 b(1 − SLO)，所以 w 小时的窗口（含 N w/720 个
   请求）花掉 b(1 − SLO)N w/720，即预算的 b w/720。令它等于 f，得 b = f × 720 小时/w = 0.05 × 720/6 = 6：目标为 99.9% 时，就是六小时内
   0.6% 的错误率。从一个干净的窗口开始，消耗速率为 10 时，t 小时后 6 小时窗口的平均消耗速率为 10t/6，在 t = 6 × 6/10 = 3.6 小时时达到 6
   （计入第 2 章 0.1 的背景消耗速率为 3.58 小时）。一般地，长窗口在 w b*/b 之后检测到 b ≥ b* 的消耗，此时已花掉的预算为
   b(w b*/b)/720 = f，无论 b 是多少都是同样的 5%：消耗越快，发现得越早，但代价并不更小。多窗口规则的 30 分钟窗口在 18 分钟后就达到 6，
   所以起决定作用的是 6 小时窗口。1 小时、阈值 14.4 的规则对消耗速率 10 永远不会触发，而这样的消耗会在 72 小时内耗尽预算。与第 2 章
   对照：那次降级的消耗速率为 12，179 分钟后发出呼叫，而公式给出 6 × 6/12 = 3 小时（计入背景为 2.97 小时）。

3. **重试放大。** 证明当 L 层每层重试 r 次时，一个出故障的后端会收到 (r + 1)ᴸ 次尝试，而 10% 的重试预算把它限制在 1.1ᴸ。

   *解答。* 从用户一侧把各层编号为 1 到 L，第 L 层调用后端；设 aₖ 为每次用户操作中第 k 层发出的尝试次数。后端故障时，每次尝试都会一路
   失败上来，所以一层收到的每个请求都会在下游变成 r + 1 次尝试：a₁ = r + 1，aₖ = (r + 1)aₖ₋₁，归纳得后端收到 a_L = (r + 1)ᴸ 次（第 4 章
   三层、每层四次尝试时为 64；十层时 4¹⁰ ≈ 10⁶）。重试预算允许客户端追加的重试至多为其首次尝试的 β = 0.1，实现为令牌桶：每次首次尝试
   挣得 β 个令牌，至多存 B 个。一层的首次尝试就是它收到的请求 nₖ₋₁（上层的重试作为新请求到达），所以在任何时段内
   nₖ ≤ (1 + β)nₖ₋₁ + B，归纳得 n₀ 次用户操作至多让后端收到 1.1ᴸn₀ + B(1.1ᴸ − 1)/0.1 次尝试：长期看每次操作 1.1ᴸ 次（三层 1.331，十层
   2.59），外加一个受令牌桶限制的突发。这个界按层相乘，所以像第 4 章建议的那样只在一层重试更好：1.1。

4. **DDSketch。** 证明 DDSketch 的保证：桶 i 中的每个值与 2γⁱ/(γ + 1) 的相对误差都在 α 以内。

   *解答。* 取 γ = (1 + α)/(1 − α)，值 x 落入桶 i = ⌈log_γ x⌉，所以 γⁱ⁻¹ < x ≤ γⁱ。于是 x̂/x = 2γⁱ/((γ + 1)x) 落在
   [2γⁱ/((γ + 1)γⁱ), 2γⁱ/((γ + 1)γⁱ⁻¹)) = [2/(γ + 1), 2γ/(γ + 1)) 中。由于 γ + 1 = 2/(1 − α)，有 2/(γ + 1) = 1 − α，
   2γ/(γ + 1) = γ(1 − α) = 1 + α，所以 1 − α ≤ x̂/x < 1 + α，即 |x̂ − x| ≤ αx。这个估计是桶两端的调和平均，是按相对误差到两端距离相等的
   唯一一点。关于分位数：各桶的计数是精确的，所以累计计数第一次越过该秩的那个桶里正好有真实的 q 分位数，回答与它的相对误差在 α 以内。
   α 相同的草图合并时逐桶相加计数，合并后的草图恰好就是并集的草图，保证不变；这就是第 7 章合并后的 p99（268 毫秒）正确、而各 p99 的
   平均（230 毫秒）不正确的原因。从 m 到 M 的值至多需要约 log_γ(M/m) ≈ ln(M/m)/(2α) 个桶：α = 1% 时，4 毫秒到 104 秒约需 509 个，
   我们的延迟填了其中 332 个。

5. **动手。** 给一个客户端加上断路器和重试预算，并测量容量下降期间的有效吞吐量（goodput）。

   *解答要点。* 从 `explainer/cs/ops/overload.py` 中的 `overload` 出发，它已经有 `"breaker"` 和 `"budget"` 两种策略，各用
   `policy == ...` 判断。让一个策略表示一组机制（例如 `"breaker+budget"`，按成员关系判断），使超时的请求只有在断路器闭合且客户端持有
   令牌（每次首次尝试挣得 0.1 个，至多 10 个）时才重试。模拟器中的断路器是所有客户端共享的一个状态：上一秒的尝试过半失败时打开 5 秒，
   打开期间仍有 5% 的调用作为探测通过；更完整的答案给若干客户端各自一个三态机（闭合：在滑动窗口上计数失败，并要求最少调用数；打开：在
   冷却期内立即失败；半开：放行少量探测，成功则闭合，失败则重新打开）。在第 3 章的触发事件上以及 `trigger_sizes` 的整个网格上，测量每秒
   和总的有效吞吐量、发出的负载，以及 `recovered_s`（触发事件结束后到有效吞吐量回到需求的 90% 所需的时间）。组合策略的一个快速实现在第
   3 章的触发事件上及时回答了 9,098 个请求（只用断路器 9,110，只用预算 7,530）：这里起作用的是断路器。在更深、更长的下降（降到 30%，持续
   20 秒）中，只用预算在运行结束前都没有恢复（回答了 2,496 个），因为服务器仍按先来先服务处理一批客户端早已放弃的积压请求，而且只能用
   预算留下的余量来消化它；组合的客户端回答了 8,133 个，下降结束一秒后就恢复了。应补充的测试：组合策略在网格的每一格上都能恢复；断路器打开时，
   发出的负载保持在探测速率附近；重试从不超过首次尝试的 10% 加上令牌桶容量。

6. **★ 研究。** 一个会重试的服务器无法从中恢复的触发事件的精确集合。

   *讨论。* 尚未解决。对容量为 μ、用户发送 λ < μ、客户端超时为 τ、重试 r 次的服务器，可以并存两个稳态：好的稳态，队列短、没有超时；
   坏的稳态，每个请求的等待都超过 τ，于是每个用户请求变成 r + 1 次尝试，发出的负载为 λ(r + 1)，当 λ(r + 1) > μ 时它自我维持（第 3 章：
   80 × 4 = 320 > 100）。触发事件的集合，就是把状态带出好稳态吸引域的扰动（这里是容量比例 f 持续 D 秒）的集合。难点在状态本身：带截止
   时间的先来先服务队列要用所有等待者的年龄来描述，是一个无穷维、有时滞的随机系统，边界附近的结果不只取决于积压量。我们的网格就说明了
   这一点：降到 70% 持续 10 秒和降到 60% 持续 5 秒都留下约 100 个请求的缺口，但前者崩溃、后者恢复，很可能是因为前者有更长的时间处于等待超过超时、
   不断产生重试的状态。边界附近的结果是随机的，所以"精确集合"其实是崩溃概率作为 (f, D) 的函数。好的部分答案应当采用流体或扩散模型，
   明确处理超时和被放弃的工作，证明双稳态的条件，并给出崩溃区域的内界和外界（必然恢复的状态和不可能恢复的状态），两者彼此接近，并在一系列
   λ、μ、τ 和 r 上与 `trigger_sizes` 吻合；即使只在确定性极限下给出边界的闭式解，也已经是新的。

## Glossary additions

* **availability, nines, downtime budget** — the fraction of time a service works; −log₁₀ of the unavailability; the
  downtime a period allows.
* **series and parallel composition, k of n** — up only if every part is up; down only if every part is down; up while
  at least k parts are.
* **MTBF, MTTR, renewal process** — mean time between failures and to repair; alternating up and down times.
* **common-mode (correlated) failure** — one cause that takes replicas down together; a part in series with them.
* **SLI, SLO, SLA** — a measured ratio of good events; a target for it over a window; a contract with consequences.
* **error budget, error-budget policy** — the unreliability the objective allows; what a team does when it is spent.
* **burn rate, multiwindow multi-burn-rate alert** — the error rate over the rate the objective allows; a page when a
  long and a short window both burn fast.
* **fail-stop, crash, omission, timing and arbitrary (Byzantine) failure** — fault models, each containing the last.
* **gray failure, differential observability** — partial failure seen differently by the failure detector and by
  users.
* **cascading failure, metastable failure, trigger, sustaining effect** — survivors overloaded in turn; a bad state
  that outlasts its trigger because the failure itself feeds it.
* **timeout, deadline propagation, idempotency** — a bounded wait; passing the caller's deadline downstream; safe to
  repeat.
* **exponential backoff, full, equal and decorrelated jitter, retry budget** — growing waits; randomised waits; a cap
  on retries as a share of first attempts.
* **hedged request, tail latency** — a second copy sent after a short delay, the first answer winning; the slow
  percentiles.
* **circuit breaker (closed, open, half-open), bulkhead, load shedding, criticality** — failing fast for a dependency
  in trouble; separate pools; refusing work early; which requests to refuse first.
* **graceful degradation, backpressure** — serving less instead of failing; a full queue slowing its producer.
* **N + k, active–passive, active–active, failover, regional evacuation** — spare capacity; a standby against copies
  that all serve; taking over; moving a region's traffic away.
* **recovery point, recovery time** — how much recent data a failover can lose; how long it takes.
* **counter, gauge, histogram, cardinality** — a value that only grows; one that goes up and down; counts in buckets;
  the number of distinct label combinations.
* **quantile sketch, DDSketch, log-linear (HDR) histogram, relative error** — small mergeable summaries of a
  distribution; an error proportional to the value.
* **structured log, trace, span, trace context, critical path** — a log of named fields; the spans of one request; the
  ids that link them; the chain of work the end waited for.
* **head and tail sampling** — keeping a trace by a coin at its start, or by its outcome at its end.
* **coordinated omission, open and closed load** — a load generator's pauses lining up with the server's; arrivals
  regardless of the system, or users who wait.
* **sampling profiler, folded stacks, flame graph, off-CPU time** — periodic samples of where a program is; counts per
  stack; frames as wide as their share; time spent waiting.
* **USE, RED, golden signals** — utilisation, saturation and errors per resource; rate, errors and duration per
  service; latency, traffic, errors and saturation.
* **capacity planning, change-point detection** — servers for a forecast load; finding where a series' mean shifts.
* **incident, incident commander, post-mortem, blameless culture** — a broken service and the people restoring it; the
  person in charge; the written account afterwards; asking why an action made sense.
* **Swiss-cheese model** — harm getting through only where the holes in every defence line up.
* **chaos engineering, steady-state hypothesis, blast radius, fault injection** — experiments that break a system on
  purpose; what should not change; how much can be harmed; crashes, partitions and delays introduced deliberately.

## Sources

* B. Beyer, C. Jones, J. Petoff and N. R. Murphy (eds.), *Site Reliability Engineering* (2016); B. Beyer, N. R.
  Murphy, D. K. Rensin, K. Kawahara and S. Thorne (eds.), *The Site Reliability Workbook* (2018), chapter 5, "Alerting
  on SLOs".
* M. Nygard, *Release It!* (2007; 2nd ed. 2018); B. Gregg, *Systems Performance* (2nd ed., 2020) and *BPF Performance
  Tools* (2019); R. Jain, *The Art of Computer Systems Performance Analysis* (1991); M. Harchol-Balter, *Performance
  Modeling and Design of Computer Systems* (2013).
* Amazon Web Services, "Summary of the Amazon S3 service disruption in the Northern Virginia (US-EAST-1) region"
  (2017); Cloudflare, "Details of the Cloudflare outage on July 2, 2019" (2019); CrowdStrike, preliminary
  post-incident review and root cause analysis of the 19 July 2024 channel file update (2024).
* C. E. Shannon, "A symbolic analysis of relay and switching circuits", Trans. AIEE 1938; E. F. Moore and C. E.
  Shannon, "Reliable circuits using less reliable relays", J. Franklin Institute 1956; J. Gray, "Why do computers stop
  and what can be done about it?", Tandem Technical Report 85.7 (1985).
* R. D. Schlichting and F. B. Schneider, "Fail-stop processors: an approach to designing fault-tolerant computing
  systems", ACM TOCS 1983; P. Huang, C. Guo, L. Zhou, J. R. Lorch, Y. Dang, M. Chintalapati and R. Yao, "Gray failure:
  the Achilles' heel of cloud-scale systems", HotOS 2017.
* N. Bronson, A. Aghayev, A. Charapko and T. Zhu, "Metastable failures in distributed systems", HotOS 2021; L. Huang,
  M. Magnusson, A. B. Muralikrishna, S. Estyak, R. Isaacs, A. Aghayev, T. Zhu and A. Charapko, "Metastable failures in
  the wild", OSDI 2022.
* R. M. Metcalfe and D. R. Boggs, "Ethernet: distributed packet switching for local computer networks", Comm. ACM
  1976; M. Brooker, "Exponential backoff and jitter", AWS Architecture Blog (2015); J. Dean and L. A. Barroso, "The
  tail at scale", Comm. ACM 2013; B. Maurer, "Fail at scale", ACM Queue 2015; K. Nichols and V. Jacobson, "Controlling
  queue delay", ACM Queue 2012.
* D. Ongaro and J. Ousterhout, "In search of an understandable consensus algorithm", USENIX ATC 2014.
* C. Masson, J. E. Rim and H. K. Lee, "DDSketch: a fast and fully-mergeable quantile sketch with relative-error
  guarantees", PVLDB 2019; Z. Karnin, K. Lang and E. Liberty, "Optimal quantile approximation in streams", FOCS 2016;
  G. Tene, HdrHistogram and wrk2.
* B. H. Sigelman, L. A. Barroso, M. Burrows, P. Stephenson, M. Plakal, D. Beaver, S. Jaspan and C. Shanbhag, "Dapper,
  a large-scale distributed systems tracing infrastructure", Google Technical Report (2010); W3C, *Trace Context*; the
  OpenTelemetry project (2019).
* B. Schroeder, A. Wierman and M. Harchol-Balter, "Open versus closed: a cautionary tale", NSDI 2006.
* B. Gregg, "The flame graph", Comm. ACM 2016; S. Williams, A. Waterman and D. Patterson, "Roofline: an insightful
  visual performance model for multicore architectures", Comm. ACM 2009; A. K. Erlang, "Solution of some problems in
  the theory of probabilities of significance in automatic telephone exchanges" (1917); D. Daly, W. Brown, H. Ingo, J.
  O'Leary and D. Bradford, "The use of change point detection to identify software performance regressions in a
  continuous integration system", ICPE 2020.
* J. Allspaw, "Blameless postmortems and a just culture", Code as Craft (Etsy, 2012); J. Reason, *Human Error* (1990);
  R. I. Cook, "How complex systems fail" (1998).
* A. Basiri, N. Behnam, R. de Rooij, L. Hochstein, L. Kosewski, J. Reynolds and C. Rosenthal, "Chaos engineering",
  IEEE Software 2016; Netflix Technology Blog, "The Netflix Simian Army" (2011).
* T. Ahmed, S. Ghosh, C. Bansal, T. Zimmermann, X. Zhang and S. Rajmohan, "Recommending root-cause and mitigation
  steps for cloud incidents using large language models", ICSE 2023.
