# Computer Science, Built — Part 49: System Design II: Case Studies

Part 49 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth part of Act IX, *Systems at Scale*, and the second of two parts on system
design. Eight systems almost everyone uses (a URL shortener, a news feed, a chat service, a web crawler, a
ride-hailing dispatcher, a video platform, a payment ledger and a collaborative editor) are each designed from the
napkin up, and each turns on one hard idea the series has already built: the birthday bound, fan-out, logical clocks,
Bloom filters, the assignment problem, control loops, idempotency and CRDTs. Each is stress-tested in simulation, a
Dynamo-style store and a metrics pipeline follow, and the Job runs as a service at a million books a day.

The instruments are in `explainer/cs/design/cases.py` (tested in `tests/test_cs49_cases.py`), with Part 39's
`explainer/cs/dist/`; two chapters reuse the cached results of Parts 46 and 48:
* `cases.py`: the shortener's base-62 lengths for 10⁶, 10⁹ and 10¹² links and the expected collisions m²/(2·62ᵏ)
  of hashes truncated to k characters, with `base62` itself; a synthetic follower graph of 100,000 users (Pareto
  tail of exponent α = 2.1 from a minimum of 20, capped at 99,999) and the daily cost of fan-out on write, on read
  and of the hybrid at thresholds of 100, 1,000 and 10,000 followers; the crawler's napkin for a billion pages a
  month, and a Bloom filter at 9.6 bits a URL with its false positives measured against (1 − e^(−kn/m))ᵏ;
  ride-hailing dispatch, greedy nearest-driver against the optimal assignment of a batch (SciPy's
  `linear_sum_assignment`), 60 riders and 70 drivers in a 10 km city over 200 rounds; adaptive bitrate on
  Markov-modulated bandwidth traces (good, fair and poor states) with a six-rung ladder, 2 s segments and a 30 s
  buffer, comparing a rate-based player (the highest rung under the harmonic mean of the last five throughputs), a
  buffer-based one (Huang et al.: a 5 s reservoir and a 20 s cushion) and RobustMPC (Yin et al.: a five-segment
  lookahead, each rung held for the horizon, the forecast discounted by the recent worst error); a double-entry
  ledger of 5,000 payments with timeouts, retries and declines, with and without idempotency keys; operational
  transformation of random concurrent pairs of inserts and deletes on "the cat sat", against applying the remote
  operation unchanged; the cardinality of one metric as labels are added; and the Job at a million books a day
  (uploads, cached reads, workers sized for 60% utilization at a 3× peak, an hour at the peak simulated on a central
  queue, and the monthly bill).
* `explainer/cs/dist/replicas.py` (Part 39): `edit_session`, three replicas making 30 random edits with the
  replicated growable array or with positions replayed as sent, the operations delivered in random order (causally
  ready order for the array); 50 sessions of each.
* `explainer/cs/dist/scale.py` (Part 39): `pbs`, Bailis et al.'s probabilistically bounded staleness, the chance that
  a read just after an acknowledged write returns the old value, for six settings of (N, R, W).
* Part 48's `blocks.cache_experiment` (W-TinyLFU on Zipf traffic over 100,000 items), for the shortener's hit rates;
  Part 46's ledger, to which `compute.py` appends row 18.

## Chapters

* **Hook.** Eight systems and the eight ideas they turn on (the birthday bound, fan-out, logical clocks, Bloom
  filters, the assignment problem, control loops, idempotency, CRDTs). The method of Part 48: requirements, the
  napkin, the API and data model, a high-level design with one request traced through it, the hard part examined with
  numbers, and the trade-offs.
* **1. A URL shortener.** Two calls, `POST /shorten` and `GET /hBxM5A4`. The napkin (illustrative): 100 million new
  links a month is about 39 a second; 100 clicks a link is about 3,858 redirects a second, 11,574 at a 3× peak; six
  billion links in five years, 3 TB at 500 bytes each before replicas. Base 62, L = ⌈log₆₂ N⌉: a million links in 4
  characters (14,776,336 codes), a billion in 6 (56,800,235,584), a trillion in 7 (3,521,614,606,208); the
  trillionth link converted by repeated division (Part 4) is `hBxM5A4`. The design from Part 48's blocks: Maglev,
  stateless app servers, a W-TinyLFU cache, the key–value store of chapter 10, blocks of a million numbers handed to
  each app server, and a click log counted by a stream job (Part 46). Three ways to choose the number: a hash
  truncated to k characters, with m²/(2·62ᵏ) expected collisions by Part 17's birthday bound (6 characters: 8.8 among
  a million links, 88,028 among a hundred million; 7: 0.14 and 1,420; 8: 0.0023 and 22.9), so every write must
  check and retry; a counter handed out in blocks (no checks, the shortest codes, but guessable); Snowflake IDs (no
  coordination, but 64 bits take 11 characters). The choice: the counter, scrambled by a fixed bijection when codes
  must not be guessable. 301 against 302 (Part 42's caching): a permanent redirect lets browsers and CDNs absorb
  later clicks but loses the analytics and the right to repoint the link. Zipf makes 302 affordable: on Part 48's
  traffic a W-TinyLFU cache holding 0.1%, 0.3%, 1%, 3% and 10% of the items catches 24%, 33%, 43%, 52% and 65% of
  requests.
* **2. A news feed: fan-out.** A synthetic power-law follower graph of 100,000 users: median 37 followers, mean 138,
  the largest account followed by all 99,999 others; half a post and twenty timeline reads per user a day, 50,000
  posts against 2.0 million reads. Push (fan-out on write) costs 50,000 × 138 ≈ 6.9 million timeline writes a day;
  pull (fan-out on read) costs 2.0 million × 138 ≈ 276.0 million fetches; every follow is one follower and one
  followee, so the two means are equal and the ratio is reads over posts, 40×. The celebrity problem: one post by
  the largest account costs as much as 2,703 by a median one, and the 119 accounts with at least 10,000 followers
  (0.12% of users) receive 27% of all follows. The hybrid, pushing ordinary accounts and pulling those above a
  threshold: operations a day 6.9 M (push all), 79.5 M (pull ≥ 10,000), 137.9 M (≥ 1,000), 213.1 M (≥ 100), 276.0 M
  (pull all); the worst fan-out of one post 99,999, 9,833, 999 and 99. Counted in operations pure push is cheapest
  (pulling the 119 giants costs 12× as much); what the hybrid buys is the tail, and the pulled posts are the same few
  hot items for everyone. Silberstein et al. (2010) choose per pair of author and reader.
* **3. A news feed: ranking and reading.** The read path: a stateless timeline service merges the pushed IDs from a
  timeline cache with the giants' latest posts, hydrates them from the post store, ranks them and returns a page of
  twenty. Timelines hold IDs, not copies: 800 per timeline (Twitter's figure, after Krikorian) × 100,000 users × 8
  bytes = 640 MB, and a deleted post is one write. Ranking: six illustrative candidates scored EdgeRank-style as
  affinity × weight × e^(−age/12) (a video 5 h old 0.53, a link 2 h old 0.46, a close friend's photo 16 h old 0.25,
  a stranger's photo 1 h old 0.18, statuses 8 h and 3 h old 0.15 and 0.04); learned two-stage ranking (Part 47).
  Paging a moving list (illustrative IDs 120 … 112, then 122 and 121 arrive): page 2 by offset 4 shows 2 posts again
  and still walks past the skipped rows (Part 43); a cursor "older than 117" returns 116 … 113 with one index seek
  (Part 35); a ranked feed's cursor names a cached snapshot. Read your own writes (Part 39): read from the leader for
  a minute after writing, carry the last write's log position, or let the app show the post itself.
* **4. A chat service.** Requirements: one-to-one and group messages, each delivered once and in order to every
  device, receipts, end-to-end encryption. The napkin (illustrative): 100 million daily users × 40 messages, about
  46,000 a second, 138,000 at a 3× peak; 400 GB of bodies a day; 50 million open connections, 25 servers at the 2
  million a server WhatsApp reported in 2012. Gateways holding WebSockets (RFC 6455), a chat service partitioned by
  conversation appending to a log per conversation, a session registry with short leases, and a push service for
  sleeping phones. Order: Ana's clock runs 3 s slow, so her "Yes!" is stamped 09:59:58, before Ben's "Dinner at 8?" at
  10:00:00; the conversation's owner numbers them 41 and 42, and a retried send keeps its number (Part 43). Receipts
  as watermarks (delivered up to 44, read up to 42); a phone that was off asks `sync(conversation, after=44)` and
  gets exactly 45, 46 and 47; a phone holding 44 that receives 46 asks for 45. Group fan-out with sender keys; the
  double ratchet (Perrin and Marlinspike, 2016): message keys from a hash chain (Part 29), deleted after use, and a
  fresh Diffie–Hellman (Part 30) on each reply; the server can no longer search or filter.
* **5. A web crawler.** A billion pages in 30 days: 386 pages a second; 193 fetches in flight at half a second each;
  0.31 Gbit/s at 100 kB a page; 0.39 of one machine at 500 connections; at one request a second per host, at least
  386 hosts busy at once; a Bloom filter at 1% false positives needs 9.6 bits a URL, 1.2 GB. The loop: frontier,
  fetcher with a DNS cache (Mercator wrote its own resolver), parser, page store, a seen-before test, and hosts
  assigned to machines by a hash of the name. Mercator's frontier: front queues by priority, back queues one per
  host, and a heap of the times each host may next be asked. Dedup: a 24-bit, 3-hash Bloom filter reporting a false
  "seen"; measured on 200,000 URLs at 9.6 bits each and 7 hashes, 1.005% false positives against 0.997% from
  theory; no false negatives, so nothing is fetched twice. SimHash (Charikar 2002) for near-duplicate content:
  Manku et al. (2007) used 64-bit fingerprints, at most 3 bits apart, over 8 billion pages.
* **6. Ride-hailing dispatch.** A million drivers reporting every 4 s is 250,000 writes a second, about 25 MB/s
  (illustrative), kept as the latest position per driver keyed by an H3 cell (Part 48), with the history on the log.
  The design: a connection gateway, a location service writing a geo index, dispatch asking it for drivers in the
  rider's cell and the ring around it, an ETA service, and an offer over the driver's open connection. Greedy against
  batched: an illustrative pair of riders on a line where greedy gives B the far driver; then 60 riders and 70
  drivers at random in a 10 km city, 200 rounds: mean pickup 1.17 km greedy against 0.96 km for the optimal
  assignment of the batch (the assignment problem of Part 18, Kuhn 1955), and the worst pickup in a round 4.80 km
  against 3.04 km. ETAs by contraction hierarchies (Geisberger et al., 2008) on a five-junction road: removing v adds
  the shortcut a–b of length 6, and queries climb upward from both ends. Surge pricing as a market in every cell
  (illustrative curves; the equilibrium moves from 5 rides an hour at price 5 to 6.875 at 6.5 when a concert ends);
  Hall, Kendrick and Nosko (2015); prices capped in emergencies.
* **7. A video platform.** A six-rung ladder from 0.3 to 4.3 Mbit/s cut into 2-second segments, listed in an HLS or
  DASH manifest; the buffer-based player's choices traced on it. An hour at the top rung is 1.9 GB of transfer, and
  an hour stored at every rung (11.25 Mbit/s in all) 5.1 GB. Encoding through a queue, in parallel by segment; an
  origin blob store and CDN edges holding the Zipf head; Netflix's Open Connect. Adaptive bitrate as a control loop on
  one simulated session (bandwidth, rung and buffer drawn): rate-based, buffer-based (reservoir and cushion) and MPC.
  Over five synthetic ten-minute traces: mean bitrate 2.33, 2.66 and 2.79 Mbit/s; stalls 3.0 s, 0.0 s and 5.0 s;
  53, 61 and 63 quality switches. Our MPC bought the best picture by trusting its forecast and keeping a smaller
  buffer (Yin et al., with a better predictor, found MPC ahead); Dobrian et al. (2011) found rebuffering the quality
  metric that hurt engagement most.
* **8. A payment ledger.** Double entry: $50.00 leaves the customer, $48.50 reaches the merchant and $1.50 goes to
  fees, then a $20.00 payment ($19.40 and $0.60); every entry sums to zero, so by induction (Part 2) the ledger does;
  integers in cents; append-only, mistakes reversed by new entries. The design: a payments API, a single-leader
  ledger database, an outbox (Part 43) to the card processor; a lost reply forces a retry, and an idempotency key
  stored with its reply in the same transaction makes it harmless (Helland 2012). Five thousand simulated payments:
  without keys 6,209 entries and 1,390 payments charged twice; with keys 4,839 entries and none; both ledgers sum to
  exactly 0, so Σ = 0 cannot catch a double charge and "at most one entry per payment" is a second invariant. A card
  payment as a state machine (created, authorized, captured, settled; declined, voided, refunded), each transition a
  compare-and-set, written with its ledger lines and outbox message in one transaction (Part 35). Daily
  reconciliation against the processor's settlement file (illustrative: $12.50 against $12.05, an entry missing on
  each side); consistency over availability during a partition (Part 39), with "pending" answered at the edge.
* **9. A collaborative editor.** Requirements: local first, convergence, intention; about 50 operations a second for
  a busy document, relayed by a collaboration server to an operation log compacted into snapshots. Positions shift:
  on "the cat sat", A inserts `z` at 1 while B appends `x` at 11; applied as sent, A ends with "tzhe cat saxt" and B
  with "tzhe cat satx". Operational transformation (Ellis and Gibbs, 1989) shifts B's insert to 12, and both read
  "tzhe cat satx"; over 5,000 random concurrent pairs, transformation converged in 100% and applying operations as
  sent in 6.3%. The original algorithm diverges with many sites; Jupiter (1995) and later Google Docs route
  operations through one server. A sequence CRDT, the replicated growable array (Roh et al., 2011): permanent names
  (counter, replica), inserts naming the element they follow, the larger name first, tombstones; in 50 sessions of
  three people making 30 edits, the array converged every time and positional replay never. Cursors anchored to
  names (an offset of 8 points into "cat" once "big " is typed); presence never logged; transformation against CRDTs
  (Yjs, Automerge).
* **10. A Dynamo-style key-value store.** DeCandia et al. (2007): an always-writable cart, latency at the 99.9th
  percentile (300 ms in the paper's example), no master, `get` and `put` with a context. The napkin (illustrative):
  10⁹ keys × 2 kB = 2 TB, 6 TB with N = 3, 12 machines on half-full 1 TB disks, 4,167 requests a second each at a
  peak of 50,000. Consistent hashing with virtual nodes; the preference list C, D, E; the coordinator answers after
  W = 2 writes. Quorums, R + W > N, simulated with Part 39's PBS model (20,000 writes a row, exponential delays of
  mean 10 ms): the chance that a read just after the acknowledgement is stale is 52.8% for (3, 1, 1) and 19.4% 10 ms
  later; 26.4% and 9.6% for (3, 1, 2); 19.7% and 2.7% for (5, 2, 2); 0% for (3, 2, 2), the paper's common setting,
  (3, 1, 3) and (5, 3, 3). Failures (illustrative): a sloppy quorum sends D's copy to F with a hint, handed back when
  D returns; Merkle trees find the differing key ranges. Conflicts: version vectors, siblings, a cart merged by union
  so that a removed pen comes back; R and W as a dial; Dynamo chose availability, Cassandra and Riak followed, a
  ledger could not.
* **11. A metrics pipeline.** A sample is a name, labels, a time and a value; agents, a log (Part 46), ingesters
  sharded by series, time-series shards, a downsampler and object storage. Cardinality multiplies: 50 services, then
  × 40 endpoints = 2,000 series, × 6 statuses = 12,000, × 8 regions = 96,000, × 200 pods = 19.2 million, × a
  million user IDs ≈ 1.9 × 10¹³. The napkin for 19.2 million series every 10 s: 1.92 million samples a second,
  1.66 × 10¹¹ a day, 2.65 TB a day at 16 bytes a sample, about 227 GB at Gorilla's 1.37 bytes (Pelkonen et al.,
  2015), from delta-of-delta timestamps and XORed values, each usually a single 0 bit. Downsampling an hour of 360
  points into 12 five-minute buckets of min, max, sum and count keeps a spike the mean hides; percentiles need a
  histogram or a sketch (Part 50). Retention tiers (illustrative): 15 days at 10 s, 90 days of minutes, 2 years of
  hours, 718,080 numbers per series against 6,307,200 at full resolution, about 9× fewer.
* **12. The Job at a million books a day.** 11.6 uploads a second; 20 reads per upload, 231 a second, 60% of them
  (assumed) answered by a cache; work at a 3× peak 313 books a second; at 80 ms a book (Part 48's model) and 60%
  busy, 42 workers; 219 TB of storage a year at 600 kB a book. An hour at the peak simulated on one queue: median 56
  ms and 99th percentile 372 ms for the requests that reach a worker, the tail of the exponential service time
  itself (80 ln 100 ≈ 368 ms); 42 workers at Part 45's on-demand price cost $2,903 a month, 0.0097 cents a book.
  Ledger row 18: the thirty novels as thirty parallel requests, the slowest of thirty, 80 ms × H₃₀ ≈ 0.32 s, for
  0.290 cents, against Part 6's 281 s.
* **13. Frontier: how designs fail, and what is unknown.** Yuan et al. (OSDI 2014): most catastrophic failures in
  five distributed systems came from mishandled non-fatal errors; Google's SRE book (2016): about 70% of outages come
  from changes to a live system; Gunawi et al. (2016): hundreds of cloud outage reports. Eight designs against five
  trade-offs (a qualitative table). Research on design itself: lightweight formal models (TLA⁺, P), deterministic
  simulation (FoundationDB, Antithesis), designs proposed from requirements. Four open problems and the ★ research
  problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs49.compute
python -m unittest tests.test_cs49_cases
python tools/build.py cs49
```

## Problems, with solutions

1. **Short IDs.** How many base62 characters does a shortener need for 10¹² links, and how many collisions does a
   7-character truncated hash give at 10⁸?

   *Solution.* L characters give 62^L codes, so we need the least L with 62^L ≥ N: L = ⌈log₆₂ N⌉. For N = 10¹²,
   log₆₂ 10¹² = 12/log₁₀ 62 = 12/1.7924 ≈ 6.69, so L = 7: 62⁶ = 56,800,235,584 is too few and 62⁷ =
   3,521,614,606,208 leaves room for 2.5 trillion more. The trillionth link, by repeated division by 62, is
   `hBxM5A4`. For a hash kept to k = 7 characters, model the m codes as independent and uniform over N = 62⁷ values.
   Each of the C(m, 2) pairs collides with probability 1/N, so by linearity the expected number of colliding pairs is
   C(m, 2)/N = m(m − 1)/(2N) ≈ m²/(2N); equivalently, inserting the links one at a time, the i-th lands on a used code
   with probability about (i − 1)/N, and the sum is the same. For m = 10⁸: 10¹⁶/(2 × 3.5216 × 10¹²) ≈ 1,420.
   Triple collisions add only about m³/(6N²) ≈ 0.013, and the chance of no collision at all is about e^(−1420): the
   collisions are certain, which is why every write must check the store and retry with a salt. The retries
   themselves are cheap (1,420 in a hundred million writes); the cost is the check on every write. At 10⁶ links the
   same hash gives 0.14; to bring 10⁸ links below one expected collision needs 62ᵏ > 5 × 10¹⁵, so k ≥ 9 (0.37). A
   counter handed out in blocks needs neither the check nor the extra characters.

2. **Fan-out.** For followers drawn from a power law with exponent α, derive the expected cost of fan-out on write
   and on read, and the best celebrity threshold.

   *Solution.* Take U users, each posting p and reading r times a day, with follower counts F independent and
   P(F > x) = (f_m/x)^(α−1) for x ≥ f_m (a density proportional to x^(−α)), capped at M = U − 1; our instrument has
   α = 2.1, f_m = 20, p = 0.5 and r = 20. Every follow is one follower and one followee, so the mean number of
   followees is also E[F]. Push writes each post into F timelines, E[F] per post and pUE[F] a day; pull fetches from
   every followee at each read, E[F] per read and rUE[F] a day; the ratio r/p = 40 does not depend on α. Integrating
   the density, E[F] = f_m(α − 1)/(α − 2) for α > 2 without the cap (220 here), and with the cap
   E[F] = f_m[(α − 1) − (f_m/M)^(α−2)]/(α − 2) = 134.7, against 138.0 measured (the standard error of the mean is
   about 4.6, since the standard deviation is 1,454). So push costs 50,000 × 138 ≈ 6.9 million writes a day and pull
   276.0 million fetches. The mean hides the tail: for α < 3 the uncapped variance is infinite, and one post can cost
   99,999 writes. The hybrid pushes accounts with F < τ and pulls the rest, which costs
   W(τ) = U[p E[F; F < τ] + r E[F; F ≥ τ]], with E[F; F ≥ τ] = f_m[(α − 1)(f_m/τ)^(α−2) − (f_m/M)^(α−2)]/(α − 2)
   and U(f_m/τ)^(α−1) accounts pulled. At τ = 100, 1,000 and 10,000 the model's share of follows going to pulled
   accounts is 76%, 47% and 24% (measured 77%, 49% and 27%), and it pulls 17,027, 1,352 and 107 accounts (measured
   16,953, 1,336 and 119). Now W(τ) = U[pE[F] + (r − p)E[F; F ≥ τ]] decreases in τ whenever r > p: with every operation
   costing the same there is no interior optimum, and pushing everything is cheapest (6.9 million against 79.5 million
   at τ = 10,000). A finite best threshold appears only when something the count omits is priced. (a) A deadline: if a
   post must reach every follower within L seconds and a server writes s timelines a second, then τ ≤ sL, and since W
   decreases, τ* = sL; with the instrument's s = 50,000 (the largest account's post takes 2.0 s on one server) and
   L = 0.2 s, τ* = 10,000, pulling 119 accounts. (b) A price κ per unit of worst-case fan-out (capacity provisioned for
   the biggest burst), with a pushed write costing c_w and a pulled fetch c_r (cheap, since pulled posts are hot and
   cached): W(τ) = U[p c_w E[F; F < τ] + r c_r E[F; F ≥ τ]] + κτ, and since the density is
   (α − 1)f_m^(α−1)τ^(−α), W′(τ) = −U(r c_r − p c_w)(α − 1)f_m^(α−1)τ^(1−α) + κ. If r c_r > p c_w, W′ rises from
   negative values towards κ, so it crosses zero once, at a minimum:
   τ* = [U(α − 1)f_m^(α−1)(r c_r − p c_w)/κ]^(1/(α−1)), nearly proportional to U(r c_r − p c_w)/κ for α = 2.1 (the
   exponent is 0.91); if p c_w ≥ r c_r, W′ > 0 and everything is pulled. Silberstein et al.'s rule, push the pair
   (author u, reader v) when p_u c_w ≤ r_v c_r, is exact when edges cost independently, as in the linear model; with
   our uniform rates it pushes everything.

3. **Batched dispatch.** Show that a batched assignment never has a larger total pickup distance than greedy, and give
   an example where it is much smaller.

   *Solution.* Fix a batch: riders R, free drivers D with |D| ≥ |R|, and distances d(r, x). Any rule that gives each
   rider a different driver defines an injective map σ: R → D, and greedy, in whatever arrival order, is one of
   them. The batched assignment minimizes Σ_r d(r, σ(r)) over all such maps, so its total is at most greedy's, with
   equality when greedy happens to be optimal. A family where greedy is exponentially worse lies on a line: drivers at
   d₀ = 0, d₁ = 2 − ε and d_k = 2d_(k−1) − ε; rider 1 at 1, then rider k at d_(k−1) for k = 2, …, n, in that order.
   Rider 1 takes d₁ (at 1 − ε, nearer than d₀ at 1); rider k finds d_(k−1) taken and takes d_k, at d_(k−1) − ε, just
   nearer than d₀ at d_(k−1). Greedy's total telescopes to d_n − 1 ≈ 2ⁿ − 1, while the batch sends rider 1 to d₀ and
   every other rider to the driver standing where it is: a total of 1. With ε = 0.001, n = 5 gives 30.97 against 1
   and n = 10 gives 1,021.98 against 1. In our random city the gain is modest, a mean pickup of 1.17 km against
   0.96 km (18% less), with the worst pickup in a round falling from 4.80 to 3.04 km; but minimizing the sum does not
   in general minimize the worst pickup, which is the bottleneck assignment problem. Two caveats: across successive
   windows, each optimal for the riders it holds, the comparison with greedy over a whole day is no longer a theorem,
   since earlier batches change which drivers later ones see; and the window itself adds waiting time.

4. **The ledger.** Prove that double-entry posting preserves Σ balances = 0, and that idempotency keys prevent double
   charges under retries.

   *Solution.* Let the balances be B: accounts → ℤ (integers of cents, so sums are exact; in floating point a balanced
   entry can sum to a tiny non-zero amount). An entry is a list of lines (a_j, v_j) with Σ_j v_j = 0, which the
   instrument asserts when it builds each entry. Posting sets B′(a) = B(a) + Σ_(j: a_j = a) v_j, so
   Σ_a B′(a) = Σ_a B(a) + Σ_j v_j = Σ_a B(a). Initially every balance is 0, so by induction over the sequence of
   posted entries Σ B = 0 after each. This needs each entry posted atomically: if entries are transactions, every
   serializable execution is equivalent to some sequence, while a half-posted entry visible to a reader would break
   the invariant; and since entries are only appended, a correction is a new, reversing entry that also sums to zero.
   For idempotency, the server handles a request with key k in one transaction: if k is recorded, return the stored
   reply; otherwise post the entry and record (k, reply) under a unique index. Claim: at most one entry carries k.
   A transaction that posts for k also records k, so any later one finds k and posts nothing; two concurrent ones
   cannot both commit, since serializability (or the unique index) aborts one. The client sends the same key with
   every attempt of one payment, so all its retries share k and it is charged at most once. The argument needs the
   key chosen before the first attempt and kept by the client, never reused for another payment, retained by the
   server at least as long as retries can arrive, and checked inside the transaction that posts (a check outside it
   lets two concurrent retries both pass); a retry with the same key but a different amount should be refused. In our
   simulation (5,000 payments, 30% retried once, 5% of attempts declined) the naive server charged 1,390 payments
   twice (27.8%, near the 0.3 × 0.95² ≈ 27.1% expected when both attempts go through) and the keyed one none, while
   both ledgers summed to exactly 0: every double charge was itself a balanced entry, so balance and "at most one entry
   per key" are separate invariants. The instrument records a key only when an attempt posts, so a retry after a
   decline may still succeed: what to store for a failed attempt is a design decision.

5. **Build.** Add hinted handoff to a three-replica store, and measure availability and stale reads when one node is
   partitioned.

   *Solution sketch.* A handoff needs somewhere to go, so use five nodes with N = 3: each key's preference list is the
   first three nodes clockwise from its hash (Part 39's ring, with `scale`'s hashing), and the next two are its
   fallbacks. Give every node a dictionary from key to a set of versions tagged with version vectors (Part 38), one
   counter per coordinator, and keep only versions not dominated by another. Draw replication delays as in
   `scale.pbs` (exponential, mean 10 ms) and run a Poisson workload of gets and puts over Zipf keys from clients that
   can reach the majority side. Partition node D from everyone for 60 s, then heal it. Compare two policies for each
   (R, W) in (1, 1), (2, 2) and (1, 3): a strict quorum, where a put succeeds only if W of the three home replicas
   answer within a timeout and a get if R do; and a sloppy quorum with hinted handoff, where an unreachable home replica
   is replaced by the first healthy fallback, which stores the version with a hint naming D and, when D is reachable
   again, delivers it and deletes its copy; run `replicas.merkle_sync` between the home replicas every T seconds as
   the background repair. Measure the fraction of puts and gets that succeed; the fraction of successful gets that
   return a version dominated by one already acknowledged (stale); the siblings created; and, after the heal, how long
   D keeps answering stale reads. What a complete answer should find, and explain: with D gone, the keys whose lists
   contain D (three fifths of them) keep full availability under strict quorums when R, W ≤ 2, but lose every put
   when W = 3; the sloppy quorum restores those puts, at the price that R + W > N no longer guarantees overlap, since
   the W copies may include a fallback that no read asks. After the heal, R = 1 reads that reach D return old values
   until the hints arrive; with handoff that window is about the handoff delay, without it the anti-entropy period T.
   A further run lets clients on D's side write as well: then both sides accept puts, and the siblings the cart must
   merge appear.

6. **★ Research.** The provably optimal fan-out policy for a power-law follower graph.

   *Discussion.* Open in the form asked: a policy chosen per user and per post that minimizes the total work of a
   feed for a given power law and ratio of reads to writes, with a proof. Under the linear model, where each pushed
   timeline write and each pulled fetch has a fixed price and edges are independent, the problem is easy and is
   solved per edge: push the pair (u, v) when u's post rate times the write price is at most v's read rate times the
   fetch price (Silberstein et al.); with uniform rates and reads more frequent than posts it pushes everything, as
   problem 2 showed. What makes it hard is everything the linear model leaves out and real feeds depend on: pulled
   posts are shared and cached, so the price of pulling a celebrity falls with the number of readers who pull it
   (Che's approximation of Part 48 makes that price a function of the whole policy); write capacity is provisioned
   for the worst burst, a maximum rather than a sum; a delivery deadline caps fan-out; posting and reading rates are
   correlated with follower counts and with each other; and a ranked feed needs a candidate set, so pulling changes
   which posts can be ranked at all. A good partial answer would fix one such coupled model, for instance per-edge
   prices plus an LRU cache of pulled posts under the independent reference model plus a peak-capacity term, prove
   that an optimal policy is a threshold in (follower count, post rate) or show that it is not, derive the threshold
   for a Pareto law with exponent α, and check it on our synthetic graph against the hybrid's measured costs.

## 习题与解答

1. **短标识符。** 一个短链接服务存放 10¹² 个链接需要多少个 base62 字符？截断为 7 个字符的哈希在 10⁸ 个链接时会产生多少次冲突？

   *解答。* L 个字符给出 62^L 个代码，所以需要满足 62^L ≥ N 的最小 L：L = ⌈log₆₂ N⌉。N = 10¹² 时，
   log₆₂ 10¹² = 12/log₁₀ 62 = 12/1.7924 ≈ 6.69，所以 L = 7：62⁶ = 56,800,235,584 不够，62⁷ = 3,521,614,606,208 还能再容纳 2.5
   万亿个。第一万亿个链接反复除以 62，得到 `hBxM5A4`。对截断为 k = 7 个字符的哈希，把 m 个代码看作在 N = 62⁷ 个值上独立且均匀分布。
   C(m, 2) 对中的每一对以概率 1/N 冲突，由期望的线性性，冲突对数的期望为 C(m, 2)/N = m(m − 1)/(2N) ≈ m²/(2N)；等价地，逐个插入链接，
   第 i 个落在已用代码上的概率约为 (i − 1)/N，求和结果相同。m = 10⁸ 时为 10¹⁶/(2 × 3.5216 × 10¹²) ≈ 1,420。三重冲突只增加约
   m³/(6N²) ≈ 0.013，完全没有冲突的概率约为 e^(−1420)：冲突是必然的，所以每次写入都必须检查存储，冲突时加盐重试。重试本身很便宜
   （一亿次写入中 1,420 次）；代价在于每次写入都要做的检查。同样的哈希在 10⁶ 个链接时为 0.14；要让 10⁸ 个链接的期望冲突低于一次，
   需要 62ᵏ > 5 × 10¹⁵，即 k ≥ 9（0.37）。分块发放的计数器既不需要检查，也不需要多出的字符。

2. **扇出。** 对服从指数为 α 的幂律的关注者数，推导写时扇出与读时扇出的期望代价，以及最佳的名人阈值。

   *解答。* 设有 U 个用户，每人每天发帖 p 次、阅读 r 次，关注者数 F 相互独立，x ≥ f_m 时 P(F > x) = (f_m/x)^(α−1)（密度正比于
   x^(−α)），并截断在 M = U − 1；我们的工具取 α = 2.1、f_m = 20、p = 0.5、r = 20。每一次关注都是一个关注者和一个被关注者，所以被关注
   数的均值也是 E[F]。推把每个帖子写进 F 条时间线，每帖 E[F]，每天 pUE[F]；拉在每次阅读时从每个被关注者处取，每次阅读 E[F]，每天
   rUE[F]；两者之比 r/p = 40，与 α 无关。对密度积分，不截断且 α > 2 时 E[F] = f_m(α − 1)/(α − 2)（这里为 220），截断后
   E[F] = f_m[(α − 1) − (f_m/M)^(α−2)]/(α − 2) = 134.7，测得 138.0（标准差为 1,454，所以均值的标准误约为 4.6）。于是推每天约
   50,000 × 138 ≈ 690 万次写入，拉 2.760 亿次读取。均值掩盖了尾部：α < 3 时不截断的方差是无穷大，一个帖子就可能要写 99,999 次。混合
   方案推送 F < τ 的账号，拉取其余的，代价为 W(τ) = U[p E[F; F < τ] + r E[F; F ≥ τ]]，其中
   E[F; F ≥ τ] = f_m[(α − 1)(f_m/τ)^(α−2) − (f_m/M)^(α−2)]/(α − 2)，被拉取的账号有 U(f_m/τ)^(α−1) 个。τ = 100、1,000 和 10,000 时，
   模型给出的指向被拉取账号的关注比例为 76%、47% 和 24%（测得 77%、49% 和 27%），被拉取的账号为 17,027、1,352 和 107 个（测得
   16,953、1,336 和 119 个）。而 W(τ) = U[pE[F] + (r − p)E[F; F ≥ τ]]，只要 r > p 就随 τ 递减：每次操作代价相同时没有内部最优，全部推送
   最便宜（690 万对 τ = 10,000 时的 7,950 万）。只有给计数所忽略的东西定价，才会出现有限的最佳阈值。(a) 截止时间：若一个帖子必须在
   L 秒内送达每个关注者，而一台服务器每秒写 s 条时间线，则 τ ≤ sL；由于 W 递减，τ* = sL。取工具中的 s = 50,000（最大账号的一个帖子
   在一台服务器上要 2.0 秒）和 L = 0.2 秒，τ* = 10,000，拉取 119 个账号。(b) 给最坏扇出的每个单位定价 κ（为最大突发预留的容量），
   推送一次写入的代价为 c_w，拉取一次读取为 c_r（被拉取的帖子是热门且有缓存的，所以便宜）：
   W(τ) = U[p c_w E[F; F < τ] + r c_r E[F; F ≥ τ]] + κτ；密度为 (α − 1)f_m^(α−1)τ^(−α)，所以
   W′(τ) = −U(r c_r − p c_w)(α − 1)f_m^(α−1)τ^(1−α) + κ。若 r c_r > p c_w，W′ 从负值向 κ 上升，只穿过零一次，那里是最小值：
   τ* = [U(α − 1)f_m^(α−1)(r c_r − p c_w)/κ]^(1/(α−1))，α = 2.1 时几乎正比于 U(r c_r − p c_w)/κ（指数为 0.91）；若 p c_w ≥ r c_r，则
   W′ > 0，全部拉取。Silberstein 等的规则（当 p_u c_w ≤ r_v c_r 时推送（作者 u，读者 v）这一对）在各条边代价相互独立时是精确的，线性
   模型正是如此；在我们均匀的速率下，它全部推送。

3. **批量派单。** 证明批量指派的总接驾距离从不大于贪心，并给出一个它小得多的例子。

   *解答。* 固定一批：乘客集合 R，空闲司机集合 D，|D| ≥ |R|，距离为 d(r, x)。任何给每位乘客分配不同司机的规则都定义一个单射
   σ: R → D，贪心无论按什么到达顺序，都是其中之一。批量指派在所有这样的映射上最小化 Σ_r d(r, σ(r))，所以它的总和至多等于贪心的，
   贪心恰好最优时取等号。贪心坏到指数级的一族例子在一条直线上：司机位于 d₀ = 0、d₁ = 2 − ε 和 d_k = 2d_(k−1) − ε；乘客 1 在 1，然后
   乘客 k 在 d_(k−1)（k = 2, …, n），依次到达。乘客 1 选 d₁（距离 1 − ε，比距离为 1 的 d₀ 近）；乘客 k 发现 d_(k−1) 已被占用，选 d_k，
   距离 d_(k−1) − ε，刚好比距离为 d_(k−1) 的 d₀ 近。贪心的总和逐项相消为 d_n − 1 ≈ 2ⁿ − 1，而批量把乘客 1 派给 d₀，其余每位乘客派给就站
   在其所在位置的司机：总和为 1。取 ε = 0.001，n = 5 时为 30.97 对 1，n = 10 时为 1,021.98 对 1。在我们随机的城市里收益不大：平均接驾
   1.17 公里对 0.96 公里（少 18%），每轮最远的接驾从 4.80 公里降到 3.04 公里；但最小化总和一般并不最小化最远的接驾，那是瓶颈指派问题。
   两点保留：在相继的多个时间窗口上，每个窗口对它所含的乘客都最优，但与整天的贪心相比就不再是定理了，因为前面的批次改变了后面的批次
   能看到哪些司机；而且窗口本身增加了等待时间。

4. **账本。** 证明复式记账的过账保持 Σ 余额 = 0，并证明幂等键能防止重试下的重复扣款。

   *解答。* 设余额为 B: 账户 → ℤ（以分为单位的整数，所以求和是精确的；用浮点数时，一笔平衡的分录加起来可能是一个极小的非零值）。一笔分录是
   若干行 (a_j, v_j)，Σ_j v_j = 0，工具在构造每笔分录时都断言这一点。过账令 B′(a) = B(a) + Σ_(j: a_j = a) v_j，所以
   Σ_a B′(a) = Σ_a B(a) + Σ_j v_j = Σ_a B(a)。开始时每个余额都是 0，所以对已过账分录的序列归纳，每一步之后都有 Σ B = 0。这要求每笔
   分录原子地过账：若分录是事务，则每个可串行化的执行都等价于某个序列，而被读者看到的过了一半的分录会破坏不变量；又因为分录只追加，
   更正是一笔新的、反向的分录，它的和也是零。关于幂等：服务器在一个事务中处理带键 k 的请求：若 k 已有记录，返回存下的回复；否则过账，
   并在唯一索引下记录 (k, 回复)。断言：至多一笔分录带有 k。为 k 过账的事务也记录了 k，所以之后的任何事务都会找到 k 而不过账；两个并发的
   事务不可能都提交，因为可串行化（或唯一索引）会让其中一个中止。客户端在同一笔支付的每次尝试中都发送同一个键，所以它的所有重试共享 k，
   至多扣款一次。这个论证要求：键在第一次尝试之前选定并由客户端保存，从不用于另一笔支付，服务器保留它至少与重试可能到达的时间一样长，
   并且在过账的同一事务内检查（在事务外检查，会让两个并发的重试都通过）；键相同而金额不同的重试应被拒绝。在我们的模拟中（5,000 笔
   支付，30% 重试一次，5% 的尝试被拒付），朴素的服务器对 1,390 笔支付扣了两次款（27.8%，接近两次尝试都成功时的期望
   0.3 × 0.95² ≈ 27.1%），带键的服务器一笔也没有，而两个账本的和都恰好为 0：每次重复扣款本身都是一笔平衡的分录，所以平衡与"每个键
   至多一笔分录"是两个独立的不变量。工具只在某次尝试过账时才记录键，所以拒付之后的重试仍可能成功：失败的尝试应存下什么，是一个设计
   决定。

5. **动手。** 给一个三副本的存储加上提示移交，并测量一个节点被分区时的可用性和陈旧读。

   *解答要点。* 移交需要有地方可去，所以用五个节点、N = 3：每个键的偏好列表是从它的哈希起顺时针的前三个节点（第39部分的环，用
   `scale` 的哈希），接下来的两个是它的后备。给每个节点一个从键到版本集合的字典，版本用版本向量（第38部分）标记，每个协调者一个计数器，
   只保留不被其他版本支配的版本。复制延迟按 `scale.pbs` 的方式抽取（指数分布，均值 10 毫秒），由能到达多数派一侧的客户端在 Zipf 分布的
   键上运行泊松的读写负载。把节点 D 与所有人分区 60 秒，然后恢复。对 (R, W) 取 (1, 1)、(2, 2) 和 (1, 3)，比较两种策略：严格法定人数，
   写入只有在三个本属副本中有 W 个在超时内应答时才成功，读取要 R 个；宽松法定人数加提示移交，不可达的本属副本由第一个健康的后备代替，
   后备保存这个版本和一条指明 D 的提示，D 重新可达时交付并删除自己的副本；每 T 秒在本属副本之间运行 `replicas.merkle_sync` 作为后台
   修复。测量成功的写和读的比例；成功的读中，返回的版本被某个已确认版本支配（陈旧）的比例；产生的兄弟值；以及恢复之后 D 继续给出
   陈旧读的时间。完整的答案应发现并解释：D 不在时，偏好列表含 D 的那些键（占五分之三）在严格法定人数下，R、W ≤ 2 时仍完全可用，但
   W = 3 时失去所有写入；宽松法定人数恢复了这些写入，代价是 R + W > N 不再保证相交，因为 W 个副本中可能有一个没有读去询问的后备。
   恢复之后，到达 D 的 R = 1 读在提示到达之前返回旧值；有移交时这个窗口约为移交的延迟，没有时为反熵的周期 T。再做一次运行，让 D 一侧的
   客户端也写入：两侧都接受写入，购物车必须合并的兄弟值就出现了。

6. **★ 研究。** 对幂律关注图可证明最优的扇出策略。

   *讨论。* 按题目的提法尚未解决：一个按用户、按帖子选择的策略，对给定的幂律和读写比最小化信息流的总工作量，并给出证明。在线性
   模型下，每次推送的时间线写入和每次拉取的读取各有固定的价格，各条边相互独立，问题很容易，按边求解：当 u 的发帖速率乘以写的价格不超过
   v 的阅读速率乘以读的价格时，推送 (u, v) 这一对（Silberstein 等）；速率均匀、阅读比发帖频繁时，它全部推送，正如第 2 题所示。难的是
   线性模型忽略、而真实信息流所依赖的一切：被拉取的帖子是共享的、有缓存的，所以拉取一个名人的价格随拉取它的读者数下降（第48部分的
   Che 近似使这个价格成为整个策略的函数）；写入容量按最坏的突发来预留，是最大值而不是总和；送达的截止时间限制了扇出；发帖和阅读的
   速率与关注者数相关，彼此也相关；排序的信息流需要候选集，所以拉取改变了哪些帖子能被排序。好的部分答案应固定一个这样耦合的模型，例如
   按边定价，加上独立引用模型下对被拉取帖子的 LRU 缓存，再加上峰值容量项；证明最优策略是（关注者数，发帖速率）上的阈值，或证明它不是；
   对指数为 α 的帕累托分布推导出阈值，并在我们的合成图上对照混合方案测得的代价检验它。

## Glossary additions

* **base62, ID space, truncated hash, counter blocks, bijective scrambling** — short codes from digits and both
  cases of letters; how many there are; hashing and keeping a prefix; ranges of numbers handed out in advance; making
  consecutive numbers unguessable.
* **301 and 302 redirects** — a move that caches remember, and one they do not.
* **fan-out on write (push), fan-out on read (pull), hybrid fan-out, celebrity problem** — building timelines when
  posts are written or when they are read; pushing most accounts and pulling the largest; the accounts whose posts
  reach millions.
* **power-law (Pareto) degree distribution** — a few accounts with most of the followers.
* **timeline cache, hydration, two-stage ranking, EdgeRank** — lists of post IDs; looking the IDs up; cheap
  candidate selection then expensive ordering; an early hand-made feed score.
* **offset and cursor pagination, read-your-writes** — counting rows against naming a position; seeing one's own
  writes at once.
* **connection gateway, session registry, per-conversation sequence number, receipt watermark, offline sync** —
  holding devices' connections; finding them; ordering within a conversation; delivered-up-to and read-up-to;
  fetching what was missed.
* **end-to-end encryption, double ratchet, chain key, sender keys** — servers that relay only ciphertext; keys that
  change with every message and every reply; one encryption per group message.
* **URL frontier, front and back queues, politeness, DNS cache** — what a crawler fetches next; priority in front,
  one queue per host behind; limiting the rate per host.
* **Bloom filter, SimHash, near-duplicate detection** — a set with false positives and no false negatives;
  fingerprints that differ in few bits for similar pages.
* **geo index, location update, greedy and batched matching, assignment problem, Hungarian method, bottleneck
  assignment** — drivers by cell; matching each request at once or a window of them optimally; minimizing the sum or
  the maximum.
* **contraction hierarchy, shortcut, surge pricing** — road graphs prepared for fast queries; prices that clear a
  local market.
* **encoding ladder, segment, manifest, HLS, DASH, CDN, Open Connect** — one title at several bitrates, cut into
  files listed for the player and served from the edge.
* **adaptive bitrate (ABR), rate-based, buffer-based, model predictive control (MPC), rebuffering, reservoir,
  cushion, QoE** — choosing each segment's quality from throughput, from the buffer, or by planning ahead; stalls;
  the buffer levels between which quality rises; the objective traded off.
* **double-entry bookkeeping, journal entry, reversing entry, idempotency key, outbox** — entries that sum to zero;
  corrections by new entries; making retries harmless; sending messages from inside a transaction.
* **authorization, capture, settlement, void, refund, reconciliation, settlement file** — a card payment's states;
  matching our records against the outside world's.
* **operational transformation (OT), transformation function, TP1, Jupiter** — rewriting concurrent operations so
  copies converge; the property it must have; one server fixing the order.
* **sequence CRDT, replicated growable array (RGA), tombstone, presence** — characters with permanent names; deleted
  ones kept; who is here, never logged.
* **preference list, coordinator, (N, R, W), sloppy quorum, hinted handoff, anti-entropy, Merkle tree, siblings,
  probabilistically bounded staleness (PBS)** — the parts of a Dynamo-style store, and how stale its reads are.
* **time series, label, cardinality, delta-of-delta, XOR compression, Gorilla** — a metric per combination of
  labels; how many there are; compressing timestamps and values to a bit or so.
* **downsampling, rollup (min, max, sum, count), retention tier, mergeable sketch** — keeping old data coarsely;
  what survives aggregation; percentiles that do.
* **change-induced outage, mishandled non-fatal error, deterministic simulation, lightweight formal methods** — how
  systems actually fail, and two ways to find it before production does.

## Sources

* A. Xu, *System Design Interview: An Insider's Guide* (2020), and A. Xu and S. Lam, volume 2 (2022);
  M. Kleppmann, *Designing Data-Intensive Applications* (2017); B. Burns, *Designing Distributed Systems* (2018);
  B. Beyer, C. Jones, J. Petoff and N. R. Murphy (eds.), *Site Reliability Engineering* (2016).
* A. Silberstein, J. Terrace, B. F. Cooper and R. Ramakrishnan, "Feeding frenzy: selectively materializing users'
  event feeds", SIGMOD 2010; R. Krikorian, "Timelines at scale", QCon San Francisco talk, published by InfoQ.
* T. Perrin and M. Marlinspike, "The Double Ratchet Algorithm", Signal specification (2016); I. Fette and
  A. Melnikov, RFC 6455, "The WebSocket Protocol" (2011).
* A. Heydon and M. Najork, "Mercator: a scalable, extensible Web crawler", World Wide Web 1999; M. Najork and
  A. Heydon, "High-performance Web crawling", Compaq SRC Research Report 173 (2001); B. H. Bloom, "Space/time
  trade-offs in hash coding with allowable errors", Comm. ACM 1970; M. Charikar, "Similarity estimation techniques
  from rounding algorithms", STOC 2002; G. S. Manku, A. Jain and A. Das Sarma, "Detecting near-duplicates for web
  crawling", WWW 2007.
* H. W. Kuhn, "The Hungarian method for the assignment problem", Naval Research Logistics Quarterly 1955;
  R. Geisberger, P. Sanders, D. Schultes and D. Delling, "Contraction hierarchies: faster and simpler hierarchical
  routing in road networks", WEA 2008; J. Hall, C. Kendrick and C. Nosko, "The effects of Uber's surge pricing: a
  case study" (2015); the H3 documentation (h3geo.org).
* T.-Y. Huang, R. Johari, N. McKeown, M. Trunnell and M. Watson, "A buffer-based approach to rate adaptation:
  evidence from a large video streaming service", SIGCOMM 2014; X. Yin, A. Jindal, V. Sekar and B. Sinopoli, "A
  control-theoretic approach for dynamic adaptive video streaming over HTTP", SIGCOMM 2015; F. Dobrian et al.,
  "Understanding the impact of video quality on user engagement", SIGCOMM 2011; R. Pantos and W. May, RFC 8216,
  "HTTP Live Streaming" (2017); ISO/IEC 23009-1, MPEG-DASH (2012).
* J. Gray, "The transaction concept: virtues and limitations", VLDB 1981; P. Helland, "Idempotence is not a medical
  condition", ACM Queue 2012.
* C. A. Ellis and S. J. Gibbs, "Concurrency control in groupware systems", SIGMOD 1989; D. A. Nichols, P. Curtis,
  M. Dixon and J. Lamping, "High-latency, low-bandwidth windowing in the Jupiter collaboration system", UIST 1995;
  H.-G. Roh, M. Jeon, J.-S. Kim and J. Lee, "Replicated abstract data types: building blocks for collaborative
  applications", J. Parallel and Distributed Computing 2011; M. Shapiro, N. Preguiça, C. Baquero and M. Zawirski,
  "Conflict-free replicated data types", SSS 2011.
* D. Karger, E. Lehman, T. Leighton, R. Panigrahy, M. Levine and D. Lewin, "Consistent hashing and random trees",
  STOC 1997; G. DeCandia et al., "Dynamo: Amazon's highly available key-value store", SOSP 2007; P. Bailis,
  S. Venkataraman, M. J. Franklin, J. M. Hellerstein and I. Stoica, "Probabilistically bounded staleness for
  practical partial quorums", PVLDB 2012.
* T. Pelkonen et al., "Gorilla: a fast, scalable, in-memory time series database", PVLDB 2015.
* D. Yuan et al., "Simple testing can prevent most critical failures: an analysis of production failures in
  distributed data-intensive systems", OSDI 2014; H. S. Gunawi et al., "Why does the cloud stop computing? Lessons
  from hundreds of service outages", SoCC 2016; C. Newcombe et al., "How Amazon Web Services uses formal methods",
  Comm. ACM 2015; J. Zhou et al., "FoundationDB: a distributed unbounded key-value store", SIGMOD 2021.
