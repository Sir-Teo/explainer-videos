# Computer Science, Built — Part 48: System Design I: Building Blocks

Part 48 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act IX, *Systems at Scale*, and the first of two parts on system
design. A large system is assembled from a small set of blocks (load balancers, caches, rate limiters, queues, shards,
replicas, identifiers, blob stores and indexes for maps), chosen under numbers estimated on a napkin, and each block
has mathematics of its own: hashing that rebalances gracefully, caches whose hit rate a formula predicts and that
survive their own expiry, rate limiters that are token buckets in disguise, identifiers that sort by time without
coordination, and curves that turn a map into keys. We build and measure each block, and load-test the Job as a
service made from them.

The instruments are in `explainer/cs/design/` (tested in `tests/test_cs48_design.py`), with load balancing from Part
43's `explainer/cs/api/`; several chapters reuse the cached results of Parts 22, 31, 34, 35, 39, 41, 42, 43, 45 and 47:
* `blocks.py`: Maglev's table fill (an offset and a skip from two hashes of each backend's name, 65,537 slots)
  against a hash ring with virtual nodes, measuring the keys moved needlessly and the load spread when a backend
  leaves; LRU, in-cache LFU and a simplified W-TinyLFU (a 1% LRU window, admission to the main LRU by a Count-Min
  sketch that is halved periodically) on Zipf traces, Che's approximation with its characteristic time found by
  bisection, the best static set, and a one-off scan of cold keys; one hot key's stampede with and without XFetch's
  probabilistic early refresh; a token bucket with a checker for its (σ, ρ) envelope, fixed windows, and the
  sliding-window counter against an exact sliding log.
* `keys.py`: the birthday bound for UUIDv4; Snowflake and UUIDv7 encoders; the leaf level of a B+ tree under random
  and time-ordered inserts (pages, fill, pages touched); Morton (Z-order) and Hilbert curves, their locality, and the
  key ranges a 16 × 16 box needs on a 256 × 256 grid; geohash; the napkin worksheet; the Job as a service (Zipf
  requests over 3,000 books, eight workers on one queue, an optional LRU result cache); a learned index (the
  PGM-index's shrinking-cone segmentation with a bounded error) against a B+ tree's inner nodes.
* `explainer/cs/api/services.py` (Part 43): `balancing`, random assignment, round robin, two random choices and the
  least loaded of all over 50 servers at 90% load.

## Chapters

* **Hook.** The napkin, for an illustrative service: 10 million users a day × 20 actions = 200 million requests a
  day; ÷ 86,400 ≈ 2,315 a second on average; × 3 at the evening peak ≈ 6,944; one write in eleven ≈ 210 writes a
  second; 2 kB each, kept 5 years in 3 copies ≈ 199 TB; the reads at the peak move about 13 MB/s. The latency
  numbers to carry, as orders of magnitude after Jeff Dean's and Peter Norvig's lists (memory ~100 ns, SSD random
  read ~100 μs, datacentre round trip ~500 μs, disk seek ~10 ms, across a continent 50–100 ms), 2¹⁰ ≈ 10³, a day
  ≈ 10⁵ s, a year ≈ π × 10⁷ s. Nine blocks, and what this part will do with them.
* **1. How a design is made.** Eight decisions in order (requirements, capacity model, data model, API, high-level
  design, deep dives, trade-offs, design document), revised when a deep dive breaks an estimate, followed through on
  a pastebin. Functional and non-functional requirements; the latter turned into service-level objectives (99% of
  reads within 200 ms; 99.9% of requests succeeding over 30 days, an error budget of about 43 minutes, 3% of a single
  day). The capacity model from the napkin: 6,944 requests a second at 1,000 a server kept half busy (Part 31) is 14
  servers; 210 writes a second, 631 at the peak, is one primary with read replicas; 10 reads per write call for a
  cache; 199 TB means sharding the records and putting the texts in a blob store; 12.6 MB/s is 101 Mbit/s, a tenth of
  one 1 Gbit/s link. The data model and API (an idempotency key on create, 410 Gone against 404, a cursor rather than
  a page number); the high-level design and the question each box hides; trade-offs written down; the design
  document's sections.
* **2. Load balancing.** Layer 4 (Maglev, IPVS) against layer 7 (NGINX, Envoy, HAProxy). Policies simulated on 50
  servers at 90% load, time in the system in mean service times (mean, 99th percentile): random 10.1 and 48.8;
  round robin 4.8 and 21.0; two random choices 2.6 and 9.1; the least loaded of all 1.2 and 5.2, which needs fresh
  counts and herds when many balancers have stale ones. Hash modulo N against the ring with virtual nodes
  (illustrative: removing a server moves only its keys). Maglev's table filled step by step for 3 backends and 7
  slots; then 20 backends and 65,537 slots, each owning 3,276 or 3,277: removing one (5% of keys must move), Maglev
  also moved 0.34% of the others and the ring (100 virtual nodes each) 0%, but Maglev's busiest backend carried 1.03
  times the mean against the ring's 1.13. Active health checks, passive outlier ejection, a cap on the share
  ejected, and slow servers worse than dead ones.
* **3. Caching: where, and what to keep.** Caches at every hop: browser, CDN edge, reverse proxy, application
  (Redis, Memcached), the database's buffer pool. Cache-aside, read-through, write-through and write-back. LRU, LFU
  and W-TinyLFU's admission by a Count-Min sketch (Part 20); a one-off scan of 20,000 cold keys takes LRU from 39.1%
  to 32.5% and TinyLFU from 46.8% to 38.5%, nearly all of both drops the scan's own misses. Che's approximation
  derived: the characteristic time T, P(i cached) ≈ 1 − e^(−p_i T), Σ(1 − e^(−p_i T)) = C, h = Σ p_i(1 − e^(−p_i T));
  at 1,000 entries simulated LRU 34.2%, the formula 34.2%. Hit rate against size for 100,000 items with Zipf
  popularity (s = 0.9) and 400,000 requests: LRU 16% at 100 entries, 34% at 1,000, 60% at 10,000; Che within 0.5
  percentage points at every size; at 1,000 entries TinyLFU 43% and LFU 44%, against 47% for the best fixed set.
  One percent of the catalogue serves over a third of the requests.
* **4. Caching: staleness and stampedes.** Update the database, then delete the cached copy; the race in which a
  reader's stale set lands after the delete; a TTL bounds staleness whatever invalidation misses; jitter spreads keys
  filled together. A stampede simulated: one key requested 200 times a second, a 60-second TTL, 2 seconds to rebuild;
  in 300 s, 4 expiries cause 1,603 rebuilds (about 401 per expiry), at worst 223 in one second, all on the database.
  Request coalescing (single flight) and memcache's leases at Facebook (a token at most once every 10 seconds per
  key, voided by a delete; a reported cut in peak database queries from 17,000 to 1,300 a second). XFetch derived
  (Vattani, Chierichetti and Lowenstein): refresh if t − Δβ ln U ≥ expiry; −ln U is exponential, so a request r
  seconds before expiry triggers with probability e^(−r/βΔ), and the expected number of triggers reaches one at
  r* = βΔ ln(λβΔ) ≈ 12 s; in the same experiment, 6 rebuilds against 1,603, no misses against 1,603, never more than
  1 in a second.
* **5. Rate limiting.** A token bucket (σ = 20, ρ = 100 a minute, refusals answered with 429): on a bursty trace of
  1,088 requests in 600 s it admitted 766. The envelope A(t, t + s) ≤ σ + ρs derived, the greediest admitted sender
  drawn, and every interval of up to 10 s of the trace checked: none above the line. Cruz's network calculus (1991);
  the leaky bucket shapes where the token bucket polices. GCRA keeps one theoretical arrival time, and with
  τ = (σ − 1)T admits exactly what the bucket admits. Fixed windows let up to twice the limit through across a
  boundary: with a limit of 100, our worst minute admitted 138. The sliding-window counter, 80 × 0.6 + 30 = 78, against
  an exact sliding log on our bursty trace: mean error 15%, worst 126%; Cloudflare reported three wrong decisions in
  a hundred thousand on real traffic (2017). One limit across many servers: a central counter, a local split, or
  approximate sharing (a Count-Min sketch errs only towards refusing); 429 with `Retry-After`.
* **6. Queues and asynchrony.** A web tier that answers 202 and a queue that absorbs a burst: a rate problem turned
  into a delay problem, which works only if the workers keep up on average. Why latency explodes near full load,
  from Part 31's M/M/1 simulation: a mean of 2 service times at half load, 10 at 0.9, 21 at 0.95, and a 99th
  percentile of 48 at 0.9; at 0.8, 3, 5 or 22 service times as job sizes vary more (Pollaczek–Khinchine).
  Priorities, weights and ageing against starvation; heavy-tailed jobs at load 0.8: FCFS 25.7 service times,
  processor sharing 4.4, shortest remaining first 2.0. Delayed jobs on a sorted set or a timing wheel; retries with
  doubling delays and full jitter; a dead-letter queue; idempotent jobs. Sizing a pool by Little's law: the napkin's
  210 writes a second, each a half-second job, keep 105 workers busy; at a 70% target, 150 workers; Erlang's pooling;
  scaling on the age of the oldest job; bounded queues.
* **7. Choosing storage.** Six shapes: relational, key–value, document, wide-column, graph, time-series. Access
  patterns decide, from Part 35: summing one column under a filter on another over 1,000,000 rows of 16 columns, a row
  store reads 128 MB and a column store 16 MB, 13.9 ms against 4.1 ms. The engine underneath, from Part 34: a B-tree
  writes 40.6 bytes to disk per byte written with 1% of it cached and 17.6 with 57% cached, a levelled LSM tree 11.9,
  a tiered one 2.2; a lookup of a missing key probes 2.0 runs (levelled) or 19.0 (tiered), 0.016 and 0.16 with a Bloom
  filter of 10 bits a key. Normalised against denormalised data, and the copy a rename misses. Indexes: with 400 keys
  a node, 10³ rows need 2 levels, 10⁶ 3, 10⁹ 4, 10¹² 5; in Part 35's word table the range from whale to whales, 1,704
  rows, lay on 966 pages through a secondary index and on 18 stored in index order; every index is a bet.
* **8. Sharding.** Range against hash partitioning: time-ordered keys put every write on the last range shard,
  hashed keys spread writes but scatter range scans; the compromise key (user, time). Hot keys, from Part 39's
  1,000,000 keys over 100 shards: the busiest shard carries 1.04 times the mean with uniform popularity, 2.3 at
  Zipf exponent 0.8, 7.8 at 1.0 (where the hottest key alone is 7% of requests) and 19.6 at 1.2; salting the 10
  hottest keys 20 ways brings these to 1.2, 1.8 and 2.8. Resharding from 10 machines to 11: hash mod N moved 90.9%
  of keys, a ring 8.6%, against the ideal 9.1%; fixed partitions moved whole; copy, stream, switch, delete; a routing
  table in ZooKeeper or etcd. Local against global secondary indexes: with each shard slow one time in 100, a query
  to 1, 10 or 100 shards is slow 1.0%, 9.7% or 64.0% of the time; a global index asks one shard but is updated
  asynchronously. Across shards: co-locate by customer; a two-phase commit whose coordinator crashes after deciding
  holds every participant's locks for 31.0 s.
* **9. Replication in practice.** One leader and its log; followers for reads and as warm spares. Reading your own
  writes, from Part 39 (followers apply a write 100 ms after the leader on average, reads go to any of 3 replicas):
  a read at once misses the write 67% of the time, after 100 ms 24%, after 500 ms 0.5%; two fixes. Failover:
  heartbeats every 100 ms on a jittery network, 10 simulated hours; a timeout of 150 ms raises 250.5 false alarms an
  hour and detects a crash in 102 ms; 200 ms, 30.3 and 152 ms; 300 ms, 3.4 and 252 ms; 1,000 ms, 2.6 and 952 ms;
  3,000 ms, 0.0 and 2,952 ms. Asynchronous replication loses the unshipped tail on promotion; semi-synchronous loses
  nothing acknowledged. Split brain, and fencing tokens 33 and 34 checked by the storage (Part 38). Active–active
  across regions, from Part 39 (two regions 50 ms apart, each writing one key 5 times a second): 19.3% of writes
  concurrent; last writer wins loses 9.7% with perfect clocks, 15.7% with 100 ms of skew, 22.7% with 250 ms; version
  vectors lose 0%.
* **10. Unique IDs.** One counter is a bottleneck; Flickr's two ticket servers (2010) split it. UUIDv4: 128 bits, 6
  fixed, 122 random; the birthday bound 1 − e^(−n²/2¹²³) gives 9.4 × 10⁻²⁰ for 10⁹ IDs, 9.4 × 10⁻¹⁴ for 10¹²,
  9.4 × 10⁻⁸ for 10¹⁵, and 49.9% at 2.7 × 10¹⁸. Snowflake (Twitter, 2010): a sign bit, 41 bits of milliseconds since
  an epoch (2⁴¹ ms ≈ 69.7 years), 10 bits of machine (1,024 machines), 12 of sequence (4,096 IDs a millisecond);
  three generated examples on machine 7. UUIDv7 (RFC 9562, 2024): 48 bits of Unix milliseconds, the version, 74
  random bits; sorted as strings, in creation order. A clock stepped back 5 ms mints an ID twice; the fix never goes
  below the last timestamp issued; across machines, IDs are ordered only to within the skew. Index locality, 200,000
  inserts at 100 keys a page: random keys leave 2,889 leaf pages 69% full, time-ordered ones 2,000 pages 100% full;
  the last 10,000 inserts touch 2,730 pages against 101.
* **11. Blobs and the edge.** Metadata in a row, bytes in an object store (Amazon S3, 2006); write the bytes first
  and the row second, and sweep orphans. Durability from Part 45's model (2% of disks failing a year, a day to
  repair): one copy, 1.0× the space and a 2.0 × 10⁻² chance of losing the object in a year; three copies, 3.0× and
  3.7 × 10⁻¹⁰; Reed–Solomon with 10 data and 4 parity fragments, 1.4× and 4.5 × 10⁻¹⁴. Multipart uploads; chunks
  named by their hashes (Part 41's git and real git agree on the README's hash); fixed-size against content-defined
  chunking (LBFS, 2001), illustrative. Signed URLs: an HMAC over the object and the expiry, a capability to keep
  short-lived. Cache keys at the edge: normalise the URL, check signatures but leave them out of the key, `Vary` by
  encoding, and the content hash in the name with a year's `max-age` and `immutable`.
* **12. Maps as keys.** A box query on Part 22's 60 points: a longitude index returns 23, a latitude index 22, the
  box holds 8. Morton's bit interleaving (IBM, 1966): x = 5, y = 3 is key 27; cells 15 and 37 are side by side.
  Geohash (Niemeyer, 2008): London `gcpvj0e`, New York `dr5regw`, no shared prefix; London's prefixes, at its
  latitude, from 3,115 km × 5,004 km (`g`) to 95 m × 153 m (`gcpvj0e`); the Greenwich meridian at the edge of `g`, so
  a search covers a cell and its eight neighbours. Hilbert's curve (1891): a 12-cell box is 7 key ranges along the Z
  and 4 along Hilbert; on a 256 × 256 grid a 16 × 16 box needs 29.9 ranges on average on Z-order against 15.4 on
  Hilbert (worst of 300 boxes 46 against 26), while neighbouring cells sit a median 3 apart along both curves and
  2,731 apart at the 99th percentile on both; S2's cube faces and 64-bit cells. An adaptive quadtree over Part 22's
  points; square neighbours at 1 and 1.41 cell widths against a hexagon's six at one; H3 (Uber, 2018): 16
  resolutions, each cell about a seventh of its parent, 12 pentagons at each. Nearest three neighbours by rings of
  cells and the circle through the third candidate; Part 22's kd-tree finds one nearest neighbour among 20,000 points
  visiting about 25 of its 39,999 nodes; PostGIS's R-tree.
* **13. Real-time blocks.** Polling every 10 s, long polling ("Comet", 2006), WebSocket (RFC 6455, 2011) and
  Server-Sent Events on an illustrative minute. Connections are state: a registry from user to connection server; a
  server's death reconnects its clients at once; Part 43's ten-second outage against a capacity of 100 requests a
  second: retrying at once offered a peak of 990 a second and recovered at 119 s, backoff with jitter 381 and 69 s.
  Notifications: preferences, rate limits and an idempotency key, a queue per channel, APNs and FCM; from Part 42,
  ten requests 20 s apart cost 130 J of radio energy against 16.5 J together, 7.9× less (a radio tail of 11.6 s).
  Presence as a failure detector: an expiring key renewed by heartbeats, and Part 39's fixed timeouts against φ
  accrual. Search as a block: a change log feeding an indexer, eventual consistency, and type-ahead: `eliz` completes
  to elizabeth, eliza, elizabeth's, eliza's and elizabethan in the thirty novels (Part 47).
* **14. The Job as a service.** "Upload a book, get its top words": a load balancer, API servers, a result cache, a
  work queue, 8 workers and a blob store; 3,000 books requested with Zipf popularity, 80 ms of a worker per count on
  average, so 8 × 1000 / 80 = 100 requests a second at 100% busy. The load test: without a cache the median sits
  near 55 ms and the 99th percentile near 364 ms at 5 requests a second, and at 95 a second (95% busy) the tail is
  607 ms; with a 300-entry cache 63% of requests hit and return in a millisecond, the median falls to 1 ms, and the
  same tail holds to about 200 requests a second (310 ms there, 894 ms at 250). What a cache buys, with chapter 3's
  numbers at 300 entries (LRU 23.7%, Che 23.7%, W-TinyLFU 33.3%, the best static set 37.2%): capacity multiplied by
  1/(1 − h), paid for in staleness and stampedes.
* **15. Frontier: design as a science.** A learned index on 1,000,000 bursty timestamps: with a maximum error of 8,
  5,218 segments (125.2 kB) and 5 comparisons; 32, 380 segments (9.1 kB) and 7; 128, 40 (1.0 kB) and 9; 512, 30
  (0.7 kB) and 11; against a B+ tree's 17 inner nodes (70 kB) and 24 comparisons (Kraska et al.; the PGM-index of
  Ferragina and Vinciguerra). Predicting a system before building it: queueing networks, simulation, learned
  performance models. Metastable failures (Bronson et al., 2021), and Part 43's retry storm as one. Four open
  problems and the ★ research problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs48.compute
python -m unittest tests.test_cs48_design
python tools/build.py cs48
```

## Problems, with solutions

1. **Consistent hashing.** Show that removing one of n backends from a consistent-hash ring moves only the keys it
   owned, and compute the load imbalance with v virtual nodes.

   *Solution.* Let P be the set of points on the ring (v for each backend) and send a key k to succ_P(h(k)), the
   first point of P clockwise from h(k). Removing backend b leaves P′ = P \ P_b. If succ_P(h(k)) = p belongs to
   another backend, then p ∈ P′, and no point of P′ lies strictly between h(k) and p, since P′ ⊂ P and no point of P
   did; so succ_P′(h(k)) = p and k stays. Only the keys whose successor was one of b's points move, each to the next
   surviving point clockwise, and with v points b's keys are spread over up to v different neighbours instead of
   landing on one. Our ring moved 0% of the other keys when one of 20 backends left (Maglev, which rebuilds its
   table, moved 0.34%). For the imbalance: the nv points are independent and uniform, and a backend owns the v arcs
   that end at its points. The nv arcs are uniform spacings, jointly Dirichlet(1, …, 1), so one backend's share is
   the sum of v of them, Beta(v, (n − 1)v): mean 1/n, variance (n − 1)/(n²(nv + 1)), a relative standard deviation
   √((n − 1)/(nv + 1)) ≈ 1/√v. The busiest of the n is then about 1 + z_n/√v times the mean, with z_n ≈ 1.87 the
   expected largest of 20 standard normals (about √(2 ln n) for large n): 1.18 for n = 20 and v = 100. For v = 1 the
   exact answer is the expected largest of n uniform spacings, H_n/n, so the busiest backend carries H_n times the
   mean, 3.60 for n = 20. Over 2,000 random rings of 20 backends the busiest carried, on average, 1.68 times the
   mean at v = 10, 1.19 at v = 100 and 1.06 at v = 1,000; the instrument's own ring (hashed with BLAKE2b) gave 3.81,
   1.52, 1.17 and 1.05 at v = 1, 10, 100 and 1,000, and 1.13 after the removal shown in chapter 2. The 1/√v decay is
   slow: to bring the busiest within 1% of the mean takes v ≈ (1.87/0.01)² ≈ 35,000 points a backend, which is why
   Maglev fills a table instead (1.03 with 65,537 slots).

2. **Che's approximation.** Derive Che's approximation for LRU under independent references, and check it against a
   simulation.

   *Solution.* Under the independent reference model each request is for item i with probability p_i, independently
   of all others. An LRU cache of C entries holds exactly the C distinct items most recently requested, so item i is
   in the cache just before a request if and only if it was requested within the last τ_i requests, where τ_i is the
   number of most recent requests it takes to see C distinct items other than i. τ_i is random and depends on i; Che,
   Tung and Wang replace it by one constant T, the characteristic time. The justification is that τ_i is a sum over
   many items, so it concentrates, and removing one item from a large catalogue barely changes it (Fricker, Robert
   and Roberts explain why the approximation is so accurate). Then P(i cached) = 1 − (1 − p_i)^T ≈ 1 − e^(−p_i T)
   (exact for Poisson requests in continuous time). The cache holds C items, so the expected number cached is C:
   Σ_i (1 − e^(−p_i T)) = C. The left side rises continuously from 0 to N, the number of items, so for 0 < C < N
   it fixes a unique T, found by bisection; and since 1 − e^(−x) ≤ x, C ≤ Σ p_i T = T, so T ≥ C. A request is for i
   with probability p_i, independently of the cache's state, and hits exactly when i is cached:
   h = Σ_i p_i (1 − e^(−p_i T)). For our 100,000 items with Zipf exponent 0.9, T is 111, 363, 1,362, 4,746 and
   20,172 requests for C = 100, 300, 1,000, 3,000 and 10,000, and the formula gives 15.6%, 23.7%, 34.2%, 45.5% and
   60.5% against simulated LRU hit rates of 15.7%, 23.7%, 34.2%, 45.4% and 60.1% on 400,000 requests, within 0.5
   percentage points everywhere; `tests/test_cs48_design.py` checks the same on a smaller trace. On the Job service's
   catalogue (3,000 books, exponent 1) the formula gives 63.0% at 300 entries, against the 63% measured in chapter 14.

3. **Early expiration.** Show that XFetch's early-refresh rule makes the expected number of concurrent rebuilds at
   expiry O(1).

   *Solution.* Requests arrive as a Poisson process of rate λ; the value expires at time E; a rebuild takes Δ, after
   which the new value and a new expiry are in place. A request at time E − r (r > 0) refreshes if
   −Δβ ln U ≥ r, with U uniform on (0, 1), and, as in the rule's plain form, any request may do so. Since −ln U is
   exponential with mean 1, it triggers with probability e^(−r/βΔ), independently of the others, so the triggers form
   a Poisson process whose intensity at remaining time r is λe^(−r/βΔ). Let R be the remaining time at the first
   trigger and X = λβΔ e^(−R/βΔ) = ∫_R^∞ λe^(−u/βΔ) du, the intensity accumulated before it. Then
   P(R ≤ r) = P(no trigger at remaining times above r) = exp(−λβΔ e^(−r/βΔ)), so P(X ≥ x) = e^(−x): X is
   exponential with mean 1, as the accumulated intensity at a Poisson process's first event always is. The rebuilds
   concurrent with the first are the triggers in the next Δ seconds, at remaining times between R − Δ and R; given R
   their expected number is at most ∫_(R−Δ)^R λe^(−r/βΔ) dr = X(e^(1/β) − 1). So the expected number of concurrent
   rebuilds is at most 1 + E[X](e^(1/β) − 1) = e^(1/β), whatever λ and Δ: 2.72 for β = 1. One case remains: if
   R < Δ the old value expires before the new one lands, and requests in between miss; P(R < Δ) =
   exp(−λβΔ e^(−1/β)), so the expected misses are at most λΔ exp(−λβΔ e^(−1/β)) ≤ e^(1/β − 1)/β, also a constant. In
   our experiment, λ = 200, Δ = 2 s and β = 1: λβΔ = 400, P(R < Δ) = e^(−147), and the refresh comes on average
   βΔ(ln λβΔ + γ) = 13.1 s before expiry (median 12.7 s; the scene's 12 s is where the expected count of earlier
   triggers is one). A Monte Carlo of 20,000 expiries without any lock gave 2.72 concurrent rebuilds on average,
   matching e. Without early refresh, every request in the Δ after expiry rebuilds, λΔ = 400 of them, and the
   instrument counted 1,603 in 4 expiries. The instrument also lets only one refresh run at a time, so it starts
   exactly one per cycle; each cycle is 62 − R seconds, about 48.9 on average, which is the 6 rebuilds in 300 s.

4. **Token bucket.** Prove that a token bucket with rate ρ and depth σ admits at most σ + ρt requests in any interval
   of length t.

   *Solution.* Let b(u) be the number of tokens at time u. Tokens accrue at rate ρ but never above σ, and an admitted
   request removes one token, which is only allowed when b ≥ 1, so b stays in [0, σ]. Take an interval [s, s + t] and
   let b₀ be the tokens just before its first admission. During the interval the tokens actually added, R, are at
   most ρt (capping at σ only discards some), and each of the A admissions spends one, so the tokens at the end are
   b₀ + R − A ≥ 0. Hence A ≤ b₀ + R ≤ σ + ρt. The bound is tight up to rounding: a sender that finds the bucket full
   and then sends whenever a token arrives is admitted σ + ⌊ρt⌋ in an interval of length t, the staircase drawn in
   chapter 5. With σ = 20 and ρ = 100 a minute, any minute admits at most 120 and any 10 s at most 36, and the check
   on every interval of up to 10 s of our trace found no violation; fixed windows with a limit of 100 admitted 138 in
   one minute, and up to 200 are possible. Since envelopes add, n such clients send a service at most nσ + nρt in any
   interval of length t, which is what makes the worst case something to size for.

5. **Build.** Add request coalescing to the Job service (one rebuild per missing key) and measure p99 during a cache
   flush.

   *Solution sketch.* First make the cache honest. `keys.job_service` puts a missed book into the cache the moment
   the request arrives, so a request for it during the 80 ms count already hits in 1 ms: as written, the model
   coalesces perfectly and for free. Keep instead a heap of (finish time, book), and before each arrival pop the
   counts that have finished and insert their books into the LRU. Then coalesce: a dictionary `inflight` from book to
   the finish time of its count; on a miss, if the book is in flight, the request waits for that count (its latency
   is the finish time minus now) and starts no work; otherwise it schedules a count on the earliest free worker, as
   now, and records it. For the flush, clear the cache at the 15,000th of 30,000 requests and take the 99th percentile
   of the requests in the following five seconds, with and without coalescing, at several rates. A sketch along these
   lines (seed 3, a 300-entry cache) gave, over the five seconds after the flush, 340 ms both ways at 100 requests a
   second, 362 against 340 ms at 150, and 659 against 431 ms at 200; over the whole run at 200, 444 against 331 ms,
   with 11,283 counts run against 11,131. The gain is modest because a count is short: at 200 requests a second
   about 16 arrive during one 80 ms count, and the most popular book is 1/H₃₀₀₀ ≈ 11.6% of them, so it is counted
   about twice over without coalescing. A complete answer sweeps the work time and the skew, where coalescing
   matters more, and reports how fast the hit rate recovers after the flush.

6. **★ Research.** A cache admission policy with a provable competitive ratio on drifting Zipf traffic.

   *Discussion.* Open. The classical analyses answer different questions. Against Belady's offline optimum, every
   deterministic online policy, LRU included, is at best C-competitive for a cache of C entries (Sleator and Tarjan),
   a worst case that says nothing about Zipf traffic. Against the best static set, stationary independent references
   are easy: exact frequency counts converge to the most popular items, which is the best static set. With drift the
   comparator has to move as well: the best static set over the whole trace is a weak target, while the best set
   within each window of W requests is a strong one, and online-learning formulations of caching that bound regret
   against a fixed cache are stated for fractional caches and adversarial sequences, not for an integral cache that
   can only admit or refuse a candidate against an LRU victim, as TinyLFU does, through a sketch that makes errors.
   A good partial answer would fix a drift model (for instance, ranks that swap with a neighbour at rate δ per
   request, or new items entering at the top at rate δ), take the best set in each window as the comparator, prove
   that a frequency filter which halves its counts every W requests (as our `CountMin` does every ten widths) keeps
   a hit rate within a stated additive term of it, with an error from sampling that falls as W grows and an error
   from drift that rises with δW, choose W to balance them, and show a lower bound for the same trade-off. It should
   be checked in our simulator against the moving optimum; on the stationary trace W-TinyLFU already trails the best
   static set by 3.9 points at 300 entries (33.3% against 37.2%) and 4.1 at 1,000 (43.3% against 47.4%).

## 习题与解答

1. **一致性哈希。** 证明从一致性哈希环上移除 n 个后端中的一个，只会移动它原来拥有的键，并计算 v 个虚拟节点时的负载不均衡。

   *解答。* 设 P 为环上所有点的集合（每个后端 v 个），键 k 交给 succ_P(h(k))，即从 h(k) 起顺时针遇到的第一个 P 中的点。移除后端 b
   后剩下 P′ = P \ P_b。若 succ_P(h(k)) = p 属于别的后端，则 p ∈ P′，并且 h(k) 与 p 之间严格没有 P′ 的点，因为 P′ ⊂ P，而 P 在那里
   本来就没有点；所以 succ_P′(h(k)) = p，k 不动。只有后继点属于 b 的键会移动，每个移到顺时针方向下一个幸存的点；有了 v 个点，b 的键
   分散到至多 v 个不同的邻居，而不是全压到一个上。20 个后端中去掉一个时，我们的环对其他键的移动是 0%（重建整张表的 Maglev 是
   0.34%）。关于不均衡：nv 个点独立且均匀，一个后端拥有终止于它的各点的 v 段弧。nv 段弧是均匀间隔，联合服从 Dirichlet(1, …, 1)，所以
   一个后端的份额是其中 v 段之和，服从 Beta(v, (n − 1)v)：均值 1/n，方差 (n − 1)/(n²(nv + 1))，相对标准差 √((n − 1)/(nv + 1)) ≈ 1/√v。
   于是 n 个中最忙的约为均值的 1 + z_n/√v 倍，其中 z_n ≈ 1.87 是 20 个标准正态变量最大值的期望（n 大时约为 √(2 ln n)）：n = 20、
   v = 100 时为 1.18。v = 1 时精确答案是 n 个均匀间隔中最大者的期望 H_n/n，所以最忙的后端承担均值的 H_n 倍，n = 20 时为 3.60。在
   2,000 个随机生成的 20 后端哈希环上，最忙者平均为均值的 1.68 倍（v = 10）、1.19 倍（v = 100）和 1.06 倍（v = 1,000）；工具里用
   BLAKE2b 哈希的环在 v = 1、10、100、1,000 时给出 3.81、1.52、1.17 和 1.05，第2章那次移除之后为 1.13。1/√v 衰减得很慢：要让最忙者
   与均值相差不到 1%，每个后端需要 v ≈ (1.87/0.01)² ≈ 35,000 个点，所以 Maglev 改为填一张表（65,537 个槽位时为 1.03）。

2. **Che 近似。** 在独立引用模型下推导 LRU 的 Che 近似，并用模拟检验它。

   *解答。* 在独立引用模型中，每个请求以概率 p_i 请求第 i 项，与其他请求独立。容量为 C 的 LRU 缓存恰好保存最近被请求的 C 个不同的
   项，所以第 i 项在某次请求之前位于缓存中，当且仅当它在最近 τ_i 次请求之内被请求过，其中 τ_i 是往回数、看到 C 个除 i 以外的不同项
   所需的请求数。τ_i 是随机的，并且依赖于 i；Che、Tung 和 Wang 把它换成一个常数 T，即特征时间。理由是 τ_i 是对许多项的求和，因而
   高度集中，而从很大的目录中去掉一项几乎不改变它（Fricker、Robert 和 Roberts 解释了这个近似为何如此准确）。于是
   P(i 在缓存中) = 1 − (1 − p_i)^T ≈ 1 − e^(−p_i T)（对连续时间的泊松请求是精确的）。缓存装着 C 项，所以在缓存中的项数的期望为 C：
   Σ_i (1 − e^(−p_i T)) = C。左边从 0 连续增长到项的总数 N，所以 0 < C < N 时它确定唯一的 T，可用二分法求出；又因为 1 − e^(−x) ≤ x，
   C ≤ Σ p_i T = T，所以 T ≥ C。一个请求以概率 p_i 请求 i，与缓存的状态无关，并且恰在 i 在缓存中时命中：
   h = Σ_i p_i (1 − e^(−p_i T))。对我们 Zipf 指数为 0.9 的 100,000 项，C = 100、300、1,000、3,000、10,000 时 T 为 111、363、1,362、
   4,746 和 20,172 次请求，公式给出 15.6%、23.7%、34.2%、45.5% 和 60.5%，40 万次请求上模拟的 LRU 命中率为 15.7%、23.7%、34.2%、
   45.4% 和 60.1%，处处相差不到 0.5 个百分点；`tests/test_cs48_design.py` 在一条较短的轨迹上做同样的检查。在那项任务的服务的目录上
   （3,000 本书，指数为 1），公式在 300 个条目时给出 63.0%，第14章测得 63%。

3. **提前过期。** 证明 XFetch 的提前刷新规则使过期时并发重建的期望次数为 O(1)。

   *解答。* 请求是速率为 λ 的泊松过程；值在时刻 E 过期；一次重建需要 Δ，之后新值和新的过期时间就位。时刻 E − r（r > 0）的请求在
   −Δβ ln U ≥ r 时刷新，U 在 (0, 1) 上均匀；按这条规则的原始形式，任何请求都可以这样做。由于 −ln U 服从均值为 1 的指数分布，它以概率
   e^(−r/βΔ) 触发，与其他请求独立，所以触发构成一个泊松过程，在剩余时间 r 处的强度为 λe^(−r/βΔ)。设 R 为第一次触发时的剩余时间，
   X = λβΔ e^(−R/βΔ) = ∫_R^∞ λe^(−u/βΔ) du，即在它之前累积的强度。于是 P(R ≤ r) = P(剩余时间大于 r 时没有触发) =
   exp(−λβΔ e^(−r/βΔ))，所以 P(X ≥ x) = e^(−x)：X 服从均值为 1 的指数分布，泊松过程在第一个事件处累积的强度总是如此。与第一次重建并发的，
   是接下来 Δ 秒内、剩余时间在 R − Δ 与 R 之间的触发；给定 R，它们的期望个数至多为 ∫_(R−Δ)^R λe^(−r/βΔ) dr = X(e^(1/β) − 1)。所以并发
   重建的期望次数至多为 1 + E[X](e^(1/β) − 1) = e^(1/β)，与 λ 和 Δ 无关：β = 1 时为 2.72。还剩一种情形：若 R < Δ，旧值在新值就位之前
   过期，其间的请求未命中；P(R < Δ) = exp(−λβΔ e^(−1/β))，所以未命中的期望至多为 λΔ exp(−λβΔ e^(−1/β)) ≤ e^(1/β − 1)/β，也是常数。在
   我们的实验中 λ = 200、Δ = 2 秒、β = 1：λβΔ = 400，P(R < Δ) = e^(−147)，刷新平均在过期前 βΔ(ln λβΔ + γ) = 13.1 秒发生（中位数 12.7
   秒；画面上的 12 秒是更早触发的期望次数达到一的位置）。不加任何锁、对 20,000 次过期做的蒙特卡罗模拟，平均有 2.72 次并发重建，与 e
   吻合。没有提前刷新时，过期后 Δ 之内的每个请求都去重建，共 λΔ = 400 个，工具在 4 次过期中数到 1,603 次。工具还只允许同时进行一次
   刷新，所以每个周期恰好开始一次；每个周期长 62 − R 秒，平均约 48.9 秒，这就是 300 秒中的 6 次重建。

4. **令牌桶。** 证明速率为 ρ、深度为 σ 的令牌桶在任何长度为 t 的区间内至多放行 σ + ρt 个请求。

   *解答。* 设 b(u) 为时刻 u 的令牌数。令牌以速率 ρ 累积，但从不超过 σ；放行一个请求取走一个令牌，而且只在 b ≥ 1 时才允许，所以 b
   始终在 [0, σ] 之内。取区间 [s, s + t]，设 b₀ 为区间内第一次放行之前的令牌数。区间内实际加入的令牌 R 至多为 ρt（在 σ 处截断只会丢掉
   一些），A 次放行各花掉一个，所以区间末的令牌数为 b₀ + R − A ≥ 0。因此 A ≤ b₀ + R ≤ σ + ρt。除了取整，这个界是紧的：一个发现桶是满的、
   之后每来一个令牌就发一个请求的发送者，在长度为 t 的区间内被放行 σ + ⌊ρt⌋ 个，就是第5章画的那条阶梯。σ = 20、ρ = 每分钟 100 时，
   任何一分钟至多放行 120 个，任何 10 秒至多 36 个；对我们轨迹中长度不超过 10 秒的每个区间的检查没有发现违例；而限额为 100 的固定
   窗口在一分钟内放行了 138 个，最多可能放行 200 个。由于包络可以相加，n 个这样的客户端在任何长度为 t 的区间内至多给服务发送
   nσ + nρt，这使最坏情况成为可以据以确定规模的东西。

5. **动手。** 给那项任务的服务加上请求合并（每个缺失的键只重建一次），并测量缓存清空期间的 p99。

   *解答要点。* 先让缓存诚实。`keys.job_service` 在请求到达的那一刻就把未命中的书放进缓存，于是在 80 毫秒的计数期间到来的请求已经能以
   1 毫秒命中：照现在的写法，这个模型免费地做到了完美的合并。改为维护一个（完成时间，书）的堆，每次到达之前弹出已完成的计数，并把它们
   的书插入 LRU。然后做合并：一个从书到其计数完成时间的字典 `inflight`；未命中时，若这本书正在计算，请求就等待那次计数（延迟为完成时间
   减去当前时间），不开始新的工作；否则像现在一样把计数排到最早空闲的工作机上，并记录下来。清空：在 30,000 个请求中的第 15,000 个时清空
   缓存，取之后五秒内请求的第 99 百分位数，分别在有、无合并时、在几种速率下测量。按这个思路写的草稿（种子 3，300 个条目的缓存）在清空
   之后的五秒内给出：每秒 100 个请求时两种都是 340 毫秒，150 时 362 对 340 毫秒，200 时 659 对 431 毫秒；200 时整次运行为 444 对 331
   毫秒，运行的计数为 11,283 对 11,131 次。收益不大，是因为一次计数很短：每秒 200 个请求时，一次 80 毫秒的计数期间约到达 16 个请求，
   最热门的书占其中的 1/H₃₀₀₀ ≈ 11.6%，所以没有合并时它大约被重复计算两次。完整的答案应扫过不同的工作时间和偏斜程度（在那里合并更
   重要），并报告清空后命中率恢复得多快。

6. **★ 研究。** 一个在漂移的 Zipf 流量上具有可证明竞争比的缓存准入策略。

   *讨论。* 尚未解决。经典的分析回答的是别的问题。与 Belady 的离线最优相比，任何确定性的在线策略（包括 LRU）对容量为 C 的缓存至多是
   C-竞争的（Sleator 和 Tarjan），这个最坏情形对 Zipf 流量什么也没说。与最佳静态集合相比，平稳的独立引用很容易：精确的频率计数会收敛到
   最热门的那些项，也就是最佳静态集合。有了漂移，比较的对象也必须移动：整条轨迹上的最佳静态集合是个弱目标，每个 W 次请求的窗口内的
   最佳集合是个强目标；而把缓存表述为在线学习、相对固定缓存给出遗憾界的工作，针对的是分数缓存和对抗性序列，而不是像 TinyLFU 那样只能
   通过一个会出错的草图、拿候选项与 LRU 的牺牲者比较而决定接纳或拒绝的整数缓存。好的部分答案应固定一个漂移模型（例如名次以每个请求
   δ 的速率与相邻者交换，或者新项以速率 δ 从顶端进入），以每个窗口内的最佳集合为比较对象，证明每 W 个请求把计数减半的频率过滤器（我们
   的 `CountMin` 每十倍宽度减半一次）的命中率与它相差不超过一个给定的加性项，其中抽样误差随 W 增大而减小，漂移误差随 δW 增大而增大，
   选择 W 使二者平衡，并给出同一权衡的下界。它应在我们的模拟器中对照移动的最优者来检验；在平稳的轨迹上，W-TinyLFU 已经在 300 个条目时
   落后最佳静态集合 3.9 个百分点（33.3% 对 37.2%），在 1,000 个条目时落后 4.1 个（43.3% 对 47.4%）。

## Glossary additions

* **back-of-the-envelope estimate, QPS, peak factor, latency numbers** — a design's arithmetic before its boxes;
  requests a second; the peak against the mean; orders of magnitude to carry.
* **functional and non-functional requirements, service-level objective (SLO), error budget** — what a system does
  and how well; a measurable target over a window; the failure it allows.
* **capacity model, data model, high-level design, deep dive, design document** — the decisions of a design, in
  order, and where they are written down.
* **layer-4 and layer-7 load balancing, round robin, least connections, power of two choices** — forwarding
  connections or requests; policies for choosing a server.
* **consistent hashing, virtual node, Maglev hashing, lookup table, disruption** — mapping keys to servers so that
  few move when the set changes.
* **health check, outlier ejection** — probing servers; removing the ones whose real traffic fails.
* **cache-aside, read-through, write-through, write-back** — four ways to connect a cache to its store.
* **LRU, LFU, W-TinyLFU, admission, Count-Min sketch, ageing** — what to evict; what to let in; counting
  popularity approximately, and forgetting it.
* **independent reference model, Che's approximation, characteristic time, best static set** — a model of requests;
  a formula for LRU's hit rate; the most popular items as a yardstick.
* **invalidation, TTL, jitter** — removing stale copies; a bound on their life; spreading expiries.
* **cache stampede (thundering herd), request coalescing (single flight), lease, probabilistic early expiration
  (XFetch)** — a hot key's expiry aimed at the store; rebuilding once; a token for the right to fill; refreshing
  before expiry at random.
* **token bucket, (σ, ρ) envelope, leaky bucket, GCRA, theoretical arrival time** — limiting rate with bursts; the
  guarantee it gives; shaping instead of policing; the same bucket as one timestamp.
* **fixed window, sliding log, sliding-window counter, 429, Retry-After** — counting requests in time; refusing
  politely.
* **asynchronous work, 202 Accepted, worker pool, backpressure, delayed job, timing wheel, full jitter, dead-letter
  queue** — work done after the answer; how it is scheduled, retried and given up on.
* **Little's law, Pollaczek–Khinchine formula, SRPT, Erlang's pooling** — queueing results that size pools and order
  work.
* **row store, column store, B-tree, LSM tree, write amplification, Bloom filter** — layouts and engines, and what
  they cost per write and per read.
* **normalisation, denormalisation, source of truth, secondary index, clustered order** — where each fact lives, and
  how it is found.
* **shard key, range and hash partitioning, hot key, celebrity problem, salting** — splitting data across machines;
  keys too popular to split; splitting them anyway.
* **resharding, fixed partitions, routing table, scatter–gather, local and global secondary indexes** — moving data
  while it is used; queries over many shards.
* **leader, follower, replication lag, read-your-writes, failover, semi-synchronous replication** — copies in
  practice, and what they cost when the leader fails.
* **split brain, fencing token, active–active, last writer wins, version vector** — two leaders at once; numbering
  their authority; writes accepted everywhere and their conflicts.
* **UUIDv4, UUIDv7, Snowflake ID, ticket server, birthday bound** — names minted without coordination, and the odds
  that two collide.
* **object store, blob, multipart upload, content addressing, content-defined chunking, erasure coding,
  Reed–Solomon** — storing large immutable bytes cheaply and durably.
* **signed URL, HMAC, capability, cache key, Vary, immutable** — handing out access to bytes; what an edge cache
  treats as the same request.
* **space-filling curve, Z-order (Morton), geohash, Hilbert curve, S2 cell, quadtree, H3** — turning places into
  keys that an ordinary index can range over.
* **nearest-neighbour query, kd-tree, R-tree** — finding what is close.
* **long polling, WebSocket, Server-Sent Events, connection registry, push notification, presence, fan-out** —
  letting the server speak first, and the state that costs.
* **learned index, PGM-index, queueing network, metastable failure** — the frontier: indexes fitted to data,
  predicted systems, outages that sustain themselves.

## Sources

* M. Kleppmann, *Designing Data-Intensive Applications* (2017); A. Xu, *System Design Interview: An Insider's Guide*
  (2020), and A. Xu and S. Lam, volume 2 (2022); B. Burns, *Designing Distributed Systems* (2018); A. Petrov,
  *Database Internals* (2019); L. A. Barroso, U. Hölzle and P. Ranganathan, *The Datacenter as a Computer* (third
  edition, 2018).
* D. Karger, E. Lehman, T. Leighton, R. Panigrahy, M. Levine and D. Lewin, "Consistent hashing and random trees",
  STOC 1997; M. Mitzenmacher, "The power of two choices in randomized load balancing", IEEE Trans. Parallel and
  Distributed Systems 2001; D. E. Eisenbud et al., "Maglev: a fast and reliable software network load balancer",
  NSDI 2016.
* L. A. Belady, "A study of replacement algorithms for a virtual-storage computer", IBM Systems Journal 1966;
  D. Sleator and R. Tarjan, "Amortized efficiency of list update and paging rules", Comm. ACM 1985.
* H. Che, Y. Tung and Z. Wang, "Hierarchical Web caching systems: modeling, design and experimental results", IEEE
  J. Selected Areas in Communications 2002; C. Fricker, P. Robert and J. Roberts, "A versatile and accurate
  approximation for LRU cache performance", ITC 2012; G. Einziger, R. Friedman and B. Manes, "TinyLFU: a highly
  efficient cache admission policy", ACM Trans. Storage 2017.
* R. Nishtala et al., "Scaling Memcache at Facebook", NSDI 2013; A. Vattani, F. Chierichetti and K. Lowenstein,
  "Optimal probabilistic cache stampede prevention", PVLDB 2015.
* R. L. Cruz, "A calculus for network delay, Part I: network elements in isolation", IEEE Trans. Information Theory
  1991; Cloudflare, "How we built rate limiting capable of scaling to millions of domains" (2017).
* J. D. C. Little, "A proof for the queuing formula L = λW", Operations Research 1961.
* E. F. Codd, "A relational model of data for large shared data banks", Comm. ACM 1970; F. Chang et al., "Bigtable:
  a distributed storage system for structured data", OSDI 2006; G. DeCandia et al., "Dynamo: Amazon's highly
  available key-value store", SOSP 2007; J. C. Corbett et al., "Spanner: Google's globally-distributed database",
  OSDI 2012; M. Burrows, "The Chubby lock service for loosely-coupled distributed systems", OSDI 2006.
* K. Davis, B. Peabody and P. Leach, RFC 9562, "Universally Unique IDentifiers (UUIDs)" (2024).
* I. S. Reed and G. Solomon, "Polynomial codes over certain finite fields", J. SIAM 1960; A. Muthitacharoen, B. Chen
  and D. Mazières, "A low-bandwidth network file system", SOSP 2001.
* D. Hilbert, "Über die stetige Abbildung einer Linie auf ein Flächenstück", Mathematische Annalen 1891; G. M.
  Morton, "A computer oriented geodetic data base and a new technique in file sequencing", IBM (1966); the S2
  Geometry documentation (s2geometry.io) and the H3 documentation (h3geo.org).
* I. Fette and A. Melnikov, RFC 6455, "The WebSocket Protocol" (2011).
* T. Kraska, A. Beutel, E. H. Chi, J. Dean and N. Polyzotis, "The case for learned index structures", SIGMOD 2018;
  P. Ferragina and G. Vinciguerra, "The PGM-index: a fully-dynamic compressed learned index with provable worst-case
  bounds", PVLDB 2020; N. Bronson, A. Aghayev, A. Charapko and T. Zhu, "Metastable failures in distributed systems",
  HotOS 2021.
