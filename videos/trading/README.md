# Building a Top-Tier Real-Time Trading System

A 16-chapter explainer, in five parts, of how a top-tier electronic market maker
(the kind of system Jane Street, Hudson River Trading and their peers run) is
built: **the game** (what a market maker earns, why spreads exist, what an
exchange is), **seeing the market** (the exchange feed byte by byte, rebuilding
the order book), **the race** (why microseconds matter, the speed of light
between Chicago and New Jersey, the latency ladder inside a server, kernel
bypass, pinned cores and ring buffers, FPGAs), **the brain** (fair value from
order-book imbalance, Avellaneda–Stoikov quoting, backtesting against real
queues) and **staying alive** (pre-trade risk checks and Knight Capital,
determinism and replay, clocks, the research loop).

Neither firm publishes its blueprints. The video assembles the public record
(engineers' talks and blog posts, exchange specifications, regulatory filings,
academic studies) and checks it against two kinds of measurement:

* **One real day of exchange data, every message.** Nasdaq's full
  TotalView-ITCH 5.0 feed for **Wednesday, December 10, 2025**, the day of a
  Federal Reserve rate decision: 846,781,990 messages, 27.0 GB, 12,114 symbols,
  scanned in one pass by [`native/itch_scan.c`](native/itch_scan.c). Every chart of
  market data, every order book, every queue, and the market-making backtest
  come from it.
* **Experiments on the computer that rendered the video**
  ([`native/bench.c`](native/bench.c), [`native/book.c`](native/book.c)): the
  memory-latency staircase with and without huge pages, system calls,
  core-to-core hand-offs, kernel UDP, a lock-free ring buffer, false sharing,
  branch prediction, OS jitter on a pinned core, and an order book processing the
  whole day of SPY.

Schematics are labeled `schematic`. Numbers the narration states are asserted
against the data at render time.

*An explanation of public information, not affiliated with any firm named, and not investment advice.*

**Watch:** [`published/trading.mp4`](../../published/trading.mp4) (1080p, subtitles and chapters embedded).

<details><summary>Chapters</summary>

- `0:00` Two o'clock on Fed day
- `2:47` Part 1: What a market maker does
- `5:46` Inside the exchange
- `9:06` Part 2: The feed, byte by byte
- `11:38` Rebuilding the order book
- `13:56` Part 3: Why microseconds matter
- `16:52` The speed of light
- `19:55` Inside the box: the latency ladder
- `22:15` The hot path in software
- `25:50` Hardware: deciding before the packet ends
- `28:11` Part 4: Fair value
- `30:47` Quoting: spread, skew, inventory
- `32:47` Testing on real queues
- `35:42` Part 5: Risk, and Knight Capital
- `38:43` Determinism and the research loop
- `40:59` The whole machine

</details>

```bash
python -m videos.trading.compute              # optional: re-download the ITCH day (11.6 GB) and recompute everything
python -m videos.trading.compute bench        # re-measure this machine (changes the numbers, and some asserts may fail)
python tools/build.py trading -q l            # preview
python tools/build.py trading                 # final 1080p30 + subtitles + chapters
python tools/export_script.py trading         # regenerate SCRIPT.md from the code
python tools/check_narration.py trading       # Whisper listen test of every narration line
python tools/publish.py trading               # GitHub-sized copy -> published/trading.mp4
```

The derived results the scenes read (`data/*.json`, 1.8 MB) are committed, so the
video renders offline exactly as published: re-running `compute.py` would
re-measure a different machine. The raw feed and large intermediates live in
`.cache/trading/` (not committed).

## Outline

| # | Scene | What it establishes | Real data on screen |
|---|---|---|---|
| 1 | `Hook` | Nasdaq in the seconds around the Fed's 2:00 pm decision: firms pull quotes, then flood back. The day's shape. The firms. The trading loop, tick to trade. | Messages per 0.1 s by type, 13:59:58–14:00:03 (16,157 deletes in the 100 ms at 13:59:59.5, across 1,431 stocks); busiest second in every 10 s, 9:00–4:30; 846.8 M messages, 27.0 GB. |
| 2 | `TheJob` | The order book, queue by queue. The spread. Two-sided quoting earns the spread; informed traders cost more than uninformed ones pay (adverse selection); Glosten–Milgrom: s/2 = πΔ. Be right and be fast. | NVDA's book at 10:30:00.000, every order; the day's time-weighted spread, 1.108 ¢. Price path is schematic. |
| 3 | `TheExchange` | Gateways → one sequencer → one matching thread. Price-time priority. One Netflix order trading against 4,076 resting orders, stamped with one nanosecond. Unicast vs multicast (Nigito's 600 µs). The message mix. State machine replication (Jane Street's JX). | NFLX at 10:38:37.273156756 (4,108 messages at one ns); regular-session mix: new 34.9%, replaced 27.5%, canceled 34.2%, executions 2.0%; 97.3% of orders never trade. |
| 4 | `TheFeed` | A real Add Order, 36 bytes decoded field by field; Delete, Execute, Replace; MoldUDP64 packets, A/B arbitration, gaps. Volume and bursts. | NVDA's first messages after the open (buy 100 @ 180.35, order #54,010,847, 09:30:00.001333600); 34,311 messages/s average, 1,752,575 in the busiest second; the Netflix burst ≈ 136 kB ≈ 108 µs on a 10 Gb/s wire. |
| 5 | `BuildingTheBook` | Price-level array + FIFO lists + hash map, animated for a real add and delete. Python vs C on the whole SPY day; pre-faulting memory; the per-update tail. | 14,953,094 SPY messages: Python 777 ns/message, C 38 → 35 ns (6,819 page faults removed); per-update median 67 ns, 99.99th pct 14 µs. Both books agree at end of day. |
| 6 | `TheRace` | SPY/IVV/VOO: lockstep over a day, independent within a second; correlation collapses at short horizons (Epps effect; Budish et al.). Stale quotes and latency-arbitrage races (Aquilina, Budish & O'Neill). The reaction spike. Fleeting orders. | Mid-prices of the three ETFs on Nasdaq; SPY–IVV return correlation 0.999 (1 min), 0.96 (1 s), 0.50 (10 ms), 0.23 (1 ms), 0.04 (0.1 ms); 11.4 M gaps from a trade to the next order message: mode 20–25 µs; 14% of deleted orders deleted within 1 ms, 42% within 0.1 s. |
| 7 | `SpeedOfLight` | Aurora → Carteret: 1,178 km; light in vacuum 3.93 ms; straight fiber 5.77 ms; Spread Networks' 2010 route 13.33 ms round trip; microwave 3.982 ms (2016), 53 µs (1.3%) above the vacuum limit. The race, slowed down. Colocation and equal-length cables. | Data-center coordinates from OpenStreetMap; outlines from Natural Earth. Tower positions and the fiber route's shape are schematic. |
| 8 | `LatencyLadder` | The memory hierarchy measured: L1 ≈ 1.5 ns, L2 ≈ 5 ns, L3 ≈ 30–75 ns, DRAM ≈ 200–290 ns; the TLB (HRT's huge-pages post) and huge pages measured; the ladder of everything, at human scale. | Pointer chasing 4 KiB–1 GiB, 4 KiB vs 2 MiB pages (1 GiB: 291 → 207 ns); syscall 102 ns; core-to-core 220 ns; kernel UDP 2.8 µs spinning / 14.2 µs asleep. |
| 9 | `HotPath` | Kernel bypass; one pinned, spinning core per job; a lock-free ring buffer (animated); false sharing; branch prediction; OS jitter and the tail. | Ring buffer 15.7 M messages/s, median 300 ns, p99 156 µs; false sharing 46 vs 5.8 ns; branches 3.74 vs 0.47 ns; a pinned core interrupted 33,502 times in 10 s (11,209 > 10 µs, longest 6.9 ms, 3.4% of its time). |
| 10 | `Hardware` | The real add order in its 104-byte frame (83 ns at 10 Gb/s); an FPGA pipeline that acts while the frame is still arriving; STAC-T0 13.9 ns; brain vs reflexes; Hardcaml; layer-1 switches. | Frame layout of the real message (schematic pipeline). |
| 11 | `FairValue` | Order-book imbalance predicts the next move; the weighted mid / microprice; the signal decays within a second; fair value combines many sources. | P(next mid move up \| imbalance) over 4.4 M NVDA and 6.8 M SPY book states (one-cent spreads): 0.15 → 0.85 for SPY; correlation with the future change peaks ≈ 50 ms ahead and vanishes by 1 min. |
| 12 | `Quoting` | Inventory risk; Avellaneda–Stoikov reservation price and spread; skew with inventory and volatility (animated); the model on a real price path. | SPY's mid 11:00–11:01 (a 44 ¢ swing), with quotes and fills simulated as in the paper (labeled). |
| 13 | `Backtest` | Virtual orders queued behind real ones; a real queue replayed until our order fills, as the price drops through it; markouts; latency and signal sweeps; rebates. | NVDA, 9:45–3:45: "join the best" at 10 µs: 82,286 fills, markout +0.15 ¢ at the fill, −0.27 ¢ 1 ms later, −0.24 ¢/share overall; 1 µs → 10 ms latency: −0.24 → −0.50 ¢; with the imbalance signal −0.19 ¢ at 1 µs; median queue ahead 100 → 243 shares. |
| 14 | `Risk` | Inline pre-trade checks (SEC Rule 15c3-5). Knight Capital, August 1, 2012, from the SEC's order. What was missing. | Facts from the SEC order (Release 34-70694). Position growth over the 45 minutes is drawn linearly (schematic). |
| 15 | `ResearchLoop` | A sequenced, timestamped input log; deterministic replay; the simulator as the same program; clocks (PTP, GPS; MiFID II RTS 25); the research loop; firm styles (OCaml at Jane Street, C++ at HRT). | |
| 16 | `Outro` | The whole machine annotated with what we found; recap; credits. | |

## Color legend

| Concept | Color |
|---|---|
| bids / asks | green / coral |
| the market maker's own quotes and fills | gold |
| trades, executions | yellow |
| market-data messages (incoming) / orders (outgoing) | pale blue / orange |
| cancels | grey |
| latency, clocks, timing | teal |
| the operating system: kernel, interrupts, jitter | rose |
| L1 / L2 / L3 / main memory | light blue → violet |
| FPGAs | lavender |
| microwave / fiber / light in vacuum | teal / orange / yellow |
| fair value, signals | pink |
| inventory | brown |

## Data (`compute.py` → `data/*.json`)

| Item | What | Used in |
|---|---|---|
| `itch` | Downloads `S121025-v50.txt.gz` (11,557,662,295 bytes) from Nasdaq's public sample directory (emi.nasdaq.com/ITCH) and scans it once with `native/itch_scan.c` (9.4 min): counts by type, per-ms rates, per-µs bursts, order lifetimes, post-trade reaction gaps, and per-stock record files for SPY IVV VOO QQQ NVDA AAPL TSLA | all |
| `day` | the day's totals, per-second profile, peaks | 1, 3, 4 |
| `windows` | every message 13:59:58–14:00:03 by type (`native/itch_window.c`), and the Netflix burst | 1, 3, 4 |
| `messages` | real NVDA messages, byte for byte | 4, 5, 10 |
| `book` | NVDA's book at 10:30:00, 13:59:59, 14:00:01 with every order; the time-weighted spread; 80 real messages after 10:30:00 | 2, 13 |
| `bookbench` | the whole SPY day through a Python book and `native/book.c` | 5, 16 |
| `race` | reaction and lifetime histograms; SPY/IVV/VOO mid-prices and their return correlations at 18 time scales | 6, 12 |
| `signal` | imbalance → next move; correlation with future changes at 16 horizons | 11 |
| `mm` | the market-making backtest (10 runs in one pass) | 13 |
| `bench` | `native/bench.c` on this machine | 5, 8, 9 |
| `geo` | coordinates, distances, map outlines | 7 |

### Method notes

* **The day.** Timestamps are Nasdaq's own (nanoseconds since midnight, the matching
  engine's event time). "Regular session" is 9:30:00–16:00:00. "Busiest second" is
  over the whole day; the busiest ones (1.75 M at 16:00:02) come right after the
  close, when the closing cross prints and day orders are canceled. The busiest
  second of the regular session was 14:40:07 (933,181).
* **Before 2:00 pm.** In the 100 ms starting 13:59:59.5 there were 21,868
  messages, 16,157 of them Order Delete, across 1,431 stocks. The video calls this
  firms pulling quotes, which is what deletes are; it does not identify who sent them.
  The burst in the first ~200 µs after 14:00:00.000 cannot be a reaction to the
  announcement (the news originates in Washington, ~1 ms of light-travel away), so
  the narration only speaks of the following seconds.
* **Order book.** Prices are bucketed to whole cents (all displayed prices of
  these stocks are). Five SPY orders at the maximum price ($199,999.00, stub quotes)
  share the top level in the C book. The Python and C books agree on the final state.
* **Reaction gaps.** For every execution (E, C, P) in the regular session, the time
  to the next non-execution order message (A, F, D, X, U) in the same stock. It
  includes the reacting firm's whole round trip through Nasdaq's systems, and some
  messages unrelated to the trade.
* **Lifetimes.** For orders added during the regular session and removed during it:
  time from add (or replace) to delete. "Never trade": 13,772,814 of 501,302,973
  added orders had any execution.
* **Correlations.** Mid-prices from Nasdaq's book only (not the national best bid
  and offer), sampled on a regular grid 9:35–15:55, log returns, zero-zero pairs
  dropped.
* **Imbalance.** Q_bid / (Q_bid + Q_ask) at the best prices, at every change of the
  top of book with a one-cent spread; "next move" is the next change of the mid.
* **Backtest.** One pass over NVDA's messages, 9:45–15:45. Each run quotes 100
  shares at the best bid and ask, re-joins when they move, caps inventory at ±500
  shares, and delays every place/cancel by its latency. A virtual order records
  the real orders ahead of it at arrival; executions and cancels of those orders
  move it up; an execution of an order behind it (or at a worse price on its side)
  fills it. Virtual orders do not affect the real market, there are no fees or
  rebates, and inventory is marked to the mid at 3:45. Markouts are against the
  mid at the fill time plus the horizon. Rebates: Nasdaq's 2025 rule filings list
  credits of $0.0020–$0.0027 per share for displayed liquidity in its DLP tiers.
* **Machine.** A KVM virtual machine, 4 vCPUs of an Intel Xeon @ 2.10 GHz (L1d 48 KiB,
  L2 2 MiB per core, L3 260 MiB shared). Latencies are medians unless stated.
  Pointer chasing uses a random single-cycle permutation of 64-byte lines; huge
  pages via `madvise(MADV_HUGEPAGE)`. Ping-pong numbers are half the round trip.
* **Geography.** Great-circle distances on a sphere of radius 6,371.0 km; light in
  fiber with group index 1.468.

## Sources

* Brian Nigito (Jane Street), [*How to Build an Exchange*](https://www.janestreet.com/tech-talks/building-an-exchange/) (tech talk) and [*Multicast and the Markets*](https://signalsandthreads.com/multicast-and-the-markets), Signals and Threads ep. 3 (2020): sequencers, single-threaded engines, multicast, JX, message mix, switch and PCIe latencies.
* Andy Ray (Jane Street), [*Programmable Hardware*](https://signalsandthreads.com/programmable-hardware/), Signals and Threads; [Hardcaml](https://arxiv.org/abs/2312.15035).
* Guillaume Morin (HRT), [*Low Latency Optimization: Understanding Huge Pages*, Part 1](https://www.hudsonrivertrading.com/hrtbeat/low-latency-optimization-part-1/) and [Part 2](https://www.hudsonrivertrading.com/hrtbeat/low-latency-optimization-part-2/), HRT Beat (2022).
* Budish, Cramton & Shim, [*The High-Frequency Trading Arms Race*](https://conference.nber.org/conf_papers/f69665.pdf), QJE 2015 (ES–SPY correlation 0.0073 at 1 ms, 2011; arbitrage durations 97 ms → 7 ms, 2005–2011).
* Aquilina, Budish & O'Neill, [*Quantifying the High-Frequency Trading "Arms Race"*](https://www.fca.org.uk/publications/occasional-papers/occasional-paper-no-50-quantifying-high-frequency-trading-arms-race-new-methodology), QJE 2022 / FCA Occasional Paper 50.
* Glosten & Milgrom (1985), *Bid, ask and transaction prices in a specialist market with heterogeneously informed traders*, JFE; Avellaneda & Stoikov (2008), *High-frequency trading in a limit order book*, Quantitative Finance; Stoikov (2018), *The micro-price*.
* Quincy Data, [*Quincy Data Lowers Latency with McKay Brothers Upgrades*](https://quincy-data.com/media/20160512-quincy-data-lowers-latency-with-mckay-brothers-upgrades) (May 12, 2016): Aurora → Carteret 3.982 ms one way.
* Spread Networks: [Lightwave](https://www.lightwaveonline.com/network-design/dwdm-roadm/article/16665260/spread-networks-improves-latency-on-chicagonew-york-route) and contemporaneous coverage (825 route miles, 13.33 ms round trip at launch, 2010).
* AMD, [*AMD Sets STAC Benchmark World Record*](https://www.amd.com/en/blogs/2024/amd-sets-stac-benchmark-world-record-for-fastest-e.html) and the [STAC-T0 report](https://stacresearch.com/node/48577) (June 2024): 13.9 ns minimum actionable latency.
* U.S. SEC, [order against Knight Capital Americas](https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf), Release 34-70694 (Oct 16, 2013); [press release](https://www.sec.gov/news/press-release/2013-222).
* FIA Principal Traders Group, [letter on Nasdaq co-location equalization](https://fia.org/ptg/articles/fia-ptg-urges-sec-ensure-nasdaq-equalizes-all-co-location-data-center-latencies) (Oct 21, 2024).
* MiFID II RTS 25 (Commission Delegated Regulation (EU) 2017/574): 100 µs / 1 µs for HFT.
* SEC Rule 15c3-5 (Market Access Rule, 2010).
* Jane Street: [janestreet.com](https://www.janestreet.com/) (200+ venues, 45 countries); 2025 net trading revenue $39.6 billion as reported by Reuters (January 2026). HRT: [hudsonrivertrading.com](https://www.hudsonrivertrading.com/) and job postings.
* Nasdaq, TotalView-ITCH 5.0 specification and the public data at emi.nasdaq.com.
* Map data: [Natural Earth](https://www.naturalearthdata.com/) (public domain); US state outlines via PublicaMundi; coordinates from [OpenStreetMap](https://www.openstreetmap.org/) Nominatim (ODbL).
