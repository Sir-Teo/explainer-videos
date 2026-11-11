# Computer Science, Built — Part 47: Search Engines

Part 47 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act IX, *Systems at Scale*. Finding the ten most useful pages
among hundreds of billions in a fraction of a second rests on five pieces of mathematics: an inverted index turns a
query into the merging of sorted lists, compression keeps those lists in memory, a probabilistic model of relevance
yields BM25, a random surfer yields PageRank, and vectors searched through a layered graph find passages by meaning.
We build each piece small enough to read, and put them together as a search engine for the thirty novels.

The instruments are in `explainer/cs/search/` (tested in `tests/test_cs47_search.py`):
* `text.py`: the thirty novels cut into passages of 400 words (11,261 of them); a tokenizer with case folding; 48
  stop words; Porter's stemmer written out rule by rule and checked against his published examples; Zipf's and
  Heaps' laws fitted by least squares on log scales.
* `index.py`: the inverted index, postings with positions, built in one pass; Boolean intersection by linear merge,
  with skip pointers every √n, and by galloping search, each counting comparisons; phrase queries over positions;
  postings stored as gaps in variable-byte, Elias γ and δ, and Golomb–Rice codes, with the bits counted.
* `rank.py`: tf-idf with length normalisation and BM25 (Lucene's idf, k₁ = 1.2, b = 0.75); precision, average
  precision and nDCG on nine queries with rule-based judgments; WAND, document at a time with per-term score bounds,
  counting the passages it fully scores.
* `links.py`: PageRank by power iteration and HITS on a synthetic web grown by preferential attachment, with a link
  farm; SimHash fingerprints over three-word shingles; stand-in passage vectors (tf-idf projected to 64 dimensions by
  a random matrix); product quantization by k-means in each sub-space, searched by asymmetric distance; a compact
  HNSW graph; edit distance, a BK-tree and noisy-channel spelling correction; top-k autocompletion.

## Chapters

* **Hook.** Finding things: Archie (McGill, 1990) indexing FTP file names; crawlers and directories by 1994;
  AltaVista's full text of the web (1995); Google (1998), links as votes, an index of 24 million pages; today's
  indexes of hundreds of billions of pages (Google, *How Search Works*). Five ideas. Our engine: 11,261 passages,
  40,692 terms, 2,364,691 postings; *white whale* answered with four passages of *Moby-Dick* (BM25 10.53, 10.31,
  10.07, 9.59), each with a snippet.
* **1. Words, stems and Zipf.** Tokens, case folding (*US* and *us* merge), stop words (12 of the 23 tokens of
  Austen's first sentence); Porter's stemmer step by step on *generalizations* → `gener`, with the measure m; all 20
  of Porter's published examples reproduced; *whaling*, *whales* → `whale`, but *general* and *generous* both
  → `gener`, and *ran* never meets *run*. Zipf's law: 4,556,139 tokens and 61,720 different words; *the* occurs
  230,876 times (5.1%), the top 20 words are 32% of the text; slope −1.21 on ranks 10 to 10,000; 22,888 words (37%)
  occur once. Heaps' law: K = 32.9, β = 0.485, with *Ulysses*, last in our order, the jump at the end; stemming
  turns 61,720 words into 40,692 terms, 34% fewer.
* **2. The inverted index.** The incidence matrix: 40,692 terms by 11,261 passages, 458 million cells, of which
  2,364,691 (0.52%) are marked. Dictionary (*whale* in 390 passages, *ahab* in 181) and postings (a passage averages
  405 tokens and 210 distinct terms); *whale* opens with a run, passages 659 to 669, *Moby-Dick*'s pages of
  quotations about whales. Building by sorting (2.36 million pairs, 19 MB at 8 bytes a pair; blocked sort-based
  indexing as Part 16's external sort); single-pass in-memory indexing (Heinz and Zobel, 2003); segments merged like
  the carries of a binary counter, deletions in a bitmap, as in Lucene and Part 34's LSM trees.
* **3. Merging postings.** AND as a merge of two sorted lists, at most m + n comparisons; skip pointers every √n
  (*the* AND *whale*, 11,257 and 390 postings: 11,137 comparisons, 1,790 with skips); galloping search (Bentley and
  Yao, 1976): 1,418 for *the* AND *whale*, and 1,915 for *love* AND *marriag* against 2,680 for the merge. The five
  queries compared (merge, skips, galloping): *whale*–*sea* 924, 720, 994; *captain*–*ahab* 278, 292, 386;
  *love*–*marriag* 2,680, 2,598, 1,915; *the*–*whale* 11,137, 1,790, 1,418; *elizabeth*–*darci* 349, 310, 534. Lists
  of similar length favour the merge or skips; at length ratios of 4.7 and 28.9 galloping wins, 7.9 times fewer
  comparisons than the merge for *the* AND *whale*. Phrases over positions: *white whale* in 64 of the 125 passages
  that have both words; *mr darcy* 137 of 159; *sherlock holmes* 99 of 101; *call me ishmael* in exactly one of 3, the
  first line of chapter one; 4,556,139 positions beside 2,364,691 passage ids.
* **4. Compressing postings.** As 32-bit integers the ids take 9.5 MB; gaps average N/f (*whale*: 11,261/390 ≈
  28.9). Variable byte: 8.67 bits a posting. Elias γ (2⌊log₂ g⌋ + 1 bits, ideal for P(g) ≈ 1/(2g²) by Kraft) and δ:
  5.64 and 5.54 bits a posting. Golomb's code derived for geometric gaps, M ≈ 0.69 N/f (19.7 for *whale*), and
  Rice's power of two, k = 4; Rice codes with k = 2 drawn; Rice over the index, one k per list: 4.96 bits a posting,
  against the bound log₂ C(N, f), 4.74 bits, within 5%. Block codecs: fixed widths packed side by side and unpacked
  by SIMD, PForDelta (2006), Lemire and Boytsov's SIMD-BP128 (2015).
* **5. From tf-idf to BM25.** Term frequency damped by a logarithm and Spärck Jones's idf (ln(N/df): *whale* 3.36,
  *darci* 4.19); passages as vectors in Salton's SMART geometry, ranked by cosine; the probability ranking principle
  (Robertson, 1977) with its exchange proof; the binary independence model derived step by step to the
  Robertson–Spärck Jones idf (1976), and Lucene's form log(1 + (N − df + 0.5)/(df + 0.5)), never negative; Harter's
  two-Poisson model and Robertson and Walker's saturation tf(k₁ + 1)/(tf + k₁), drawn for k₁ = 0.5, 1.2, 2 and 5;
  length normalisation by b; BM25 at TREC-3 (1994), Lucene's defaults k₁ = 1.2, b = 0.75.
* **6. Is the ranking good?** Precision and recall at k on an illustrative ranking of ten (six relevant passages, one
  never retrieved); average precision 0.59; MAP on our nine queries, cut at ten: BM25 0.80, tf-idf 0.75. nDCG
  derived (gain 2^g − 1, discount 1/log₂(i + 1), divided by the ideal order): 0.80 for the illustrative ranking. Test
  collections (Cranfield), TREC's pooling, Zobel's finding that comparisons survive incomplete pools. Our nine
  queries, graded by rule: nDCG@10 of 1.00 for both rankers on six of them; *sherlock holmes* 0.60 for both, because
  4 of BM25's top ten come from *The Hound of the Baskervilles*, which the rule cannot count; *vampire count* 0.25
  and 0.23, swamped by *The Count of Monte Cristo*; means 0.847 and 0.834. The sign test: 6 ties, 3 for BM25, none
  for tf-idf, p = 2 × 2⁻³ = 0.25: nine queries cannot tell.
* **7. Top k, fast.** Scoring everything: *the sea* has a term in 11,257 of the 11,261 passages, and all are scored
  into a min-heap whose smallest score is θ. Per-term upper bounds and max-score (Turtle and Flood, 1995); WAND's
  pivot (Broder et al., 2003) on a toy query with bounds 0.8, 1.2, 3.0 and θ = 2.6: 4 of 13 documents scored, exactly
  those with *ahab*. On the novels, BM25's top ten with a rising θ: *white whale* 235 of 1,610 candidates scored
  (15%), *captain ahab ship* 117 of 952 (12%), *the sea* 1,144 of 11,257 (10%), *love marriage money* 359 of 3,633
  (10%), *pride prejudice* 213 of 454 (47%); every top ten identical to exhaustive scoring, score for score.
  Block-max WAND (Ding and Suel, 2011; in Lucene since 2019); tiered indexes and champion lists, which are unsafe.
* **8. Links and the random surfer.** Links as votes and anchor text (Brin and Page, 1998); the PageRank equation,
  d = 0.85, pages without links, the Google matrix's eigenvector as a Markov chain's stationary distribution (Part
  18), Perron–Frobenius. Power iteration on a synthetic web of 400 pages grown by preferential attachment plus a
  farm of 20: the change falls to 1.1 × 10⁻⁶ after 40 steps, faster than the guaranteed factor 0.85 a step; the
  top pages are the oldest (pages 0, 2, 1, 3, 8). HITS (Kleinberg, 1999) as the leading singular vectors of the link
  matrix: the top authority is the farm's target (page 399), the top hub a farm page (400), and all 20 farm pages
  are among the 20 best hubs. Link spam: the target ranks 346th of 400 without the farm, 114th of 420 with it;
  `nofollow` (2005) and TrustRank (Gyöngyi, Garcia-Molina and Pedersen, 2004).
* **9. Crawling the web.** The crawl loop: frontier, DNS and `robots.txt`, fetch, parse, content fingerprint, URL
  normalisation and the seen-URL set (Part 17); Mercator (Heydon and Najork, 1999) and crawler traps. The frontier's
  front queues for priority and back queues with a heap of hosts for politeness (a pause of about ten times the last
  fetch); `robots.txt` (Koster, 1994; RFC 9309, 2022). Freshness: a page changing at rate λ and revisited every I is
  fresh for (1 − e^(−λI))/(λI) of the time; Cho and Garcia-Molina's (2000) uniform revisiting beats proportional.
  SimHash (Charikar, 2002) over three-word shingles as Part 20's random hyperplanes: on 200 passages with words
  replaced at random, 1 word moves 2.4 bits on average (at most 7), 5 words 5.5 (13), 20 words 10.4 (22), 80 words
  19.8 (29); unrelated passages differ in 31.9 bits on average, at least 22; Manku, Jain and Das Sarma's (2007) 3-bit
  threshold for 8 billion pages, found by exact lookups on four 16-bit blocks.
* **10. Serving at scale.** The index as a sparse matrix cut by columns (document-partitioned shards) or by rows
  (term-partitioned servers); *whale* AND *sea* in each layout: four shards each return a top ten for the broker to
  merge, against one server shipping all 390 postings of *whale* to the other, which finds the 231 passages with
  both; web engines partition by document (Barroso, Dean and Hölzle, 2003). The tail at scale: 1 − 0.99ⁿ of queries
  are slow, 63% for 100 servers; hedged requests cut the 99.9th percentile from 1,800 ms to 74 ms for 2% more
  requests (Dean and Barroso, 2013). Shards and replicas as a grid; result caches for the head of a Zipf-skewed query
  stream, postings caches (Baeza-Yates et al., 2007).
* **11. Spelling and autocomplete.** The noisy channel, argmax P(w) P(t | w), with counts in the novels as the
  language model and a fixed penalty per edit (Kernighan, Church and Gale, 1990, learned theirs); the Levenshtein
  table (`captian` to `captain`: 2 edits) and Damerau's transposition (1964); BK-trees (Burkhard and Keller, 1973)
  pruning by the triangle inequality, drawn for `whsle` within one edit; on the 31,190 words that occur at least three
  times, tolerance 2 still costs 8,098 to 11,752 distances per typo, about a third. Seven inputs: *captian*,
  *elizabth*, *seperate*, *monstr* and *londn* repaired; *whale* kept (76 neighbours, none common enough); *recieve*
  → *relieve*, one substitution away, where *receive* is two. Completion as the best k below a trie node: *ca* gives
  *can*, *came*, *called*, *cannot*, *can't*.
* **12. Learning to rank.** Features of a query and a passage (BM25, tf-idf, phrase, proximity, length; on the web
  PageRank and clicks; MSLR-WEB30K has 136); pointwise, pairwise (RankNet, 2005) and listwise (ListNet, 2007)
  losses; LambdaRank's lambdas, RankNet's pair gradients times |ΔnDCG|, on six illustrative passages (nDCG 0.60;
  passage C, grade 3 at rank 3, pushed hardest); LambdaMART as boosted trees on the lambdas (*AI, Built* Part 6):
  nDCG 0.60, then 0.94, then 1, the ideal order; the Yahoo! Learning to Rank Challenge (2010). Clicks and position
  bias: the swapped-results eye-tracking study (Joachims et al., 2005), the cascade model (Craswell et al., 2008),
  inverse propensity weighting (Joachims, Swaminathan and Schnabel, 2017).
* **13. Dense retrieval.** Vocabulary mismatch; an encoder (*AI, Built* Part 24) and the dot product; our stand-in
  vectors, tf-idf projected to 64 dimensions by a random matrix (Part 20), 256 bytes each; DPR (Karpukhin et al.,
  2020). Product quantization (Jégou, Douze and Schmid, 2011): 8 sub-vectors of 8 dimensions, one byte each; recall
  of the true top ten over 100 queries is 7%, 13%, 31% and 54% with 2, 4, 8 and 16 bytes, squared error 0.66, 0.49,
  0.27 and 0.08; codes shortlist and exact vectors re-rank (Faiss). HNSW (Malkov and Yashunin) on 3,000 passage
  vectors: levels of 2,621, 334, 41 and 4 points; building took 1,061,951 distances; beam 40 finds 81% of the top
  ten for 467 distances, about a sixth of brute force's 3,000 (beams 10 to 160: 68% for 191 to 95% for 1,232).
  Reciprocal rank fusion (Cormack, Clarke and Büttcher, 2009); BEIR (2021); retrieval-augmented generation (*AI,
  Built* Part 15).
* **14. A search engine for the novels.** The pipeline on *the hound on the moor* (stems `hound`, `moor`): postings,
  BM25, top ten, snippets. Four top answers: *white whale* → *Moby-Dick*, passage 817 (BM25 10.5); *call me ishmael*
  → *Moby-Dick*, passage 676 (10.4); *pride and prejudice* → *Pride and Prejudice*, passage 2 (11.3); *the hound on
  the moor* → *The Hound of the Baskervilles*, passage 4,653 (15.4). The index's ids under each code: 32-bit 9.5 MB,
  variable byte 2.6, γ 1.7, δ 1.6, Golomb–Rice 1.5, the bound 1.4. What a web engine adds; Lucene beneath
  Elasticsearch, OpenSearch and Solr.
* **15. Frontier: retrieval and its limits.** Graph search without a guarantee (our HNSW: 68% recall for 191
  distances, 95% for 1,232, against 3,000), locality-sensitive hashing (Part 20); learned sparse retrieval (SPLADE,
  2021), late interaction (ColBERT, 2020), hybrids, and why BM25 stays hard to beat on new collections; retrieval
  for machines that write: retrieval-augmented generation and generative retrieval (Tay et al., 2022), and what is
  open in evaluating written answers. Four open problems and the ★ research problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs47.compute
python -m unittest tests.test_cs47_search
python tools/build.py cs47
```

## Problems, with solutions

1. **Galloping.** Show that galloping intersection of lists of sizes m ≤ n takes O(m log(n/m)) comparisons, and that
   this is optimal up to a constant.

   *Solution.* Let the short list be a₁ < … < a_m and the long one b₁ < … < b_n. Galloping keeps a position in the
   long list that only moves forward. For aᵢ it probes 1, 2, 4, 8, … places ahead until a probe reaches a value
   ≥ aᵢ or runs off the end, binary searches the last bracket, and makes one equality test. If the position advances
   by gᵢ places, the doubling makes at most log₂(gᵢ + 1) + 1 probes and leaves a bracket of fewer than gᵢ + 1 places,
   so the search for aᵢ costs at most 2 log₂(gᵢ + 1) + 3 comparisons. The gᵢ sum to at most n, and log is concave,
   so by Jensen Σ log₂(gᵢ + 1) ≤ m log₂(n/m + 1). The total is at most 2m log₂(n/m + 1) + 3m = O(m(1 + log(n/m))),
   which is O(m log(n/m)) once n ≥ 2m (for n < 2m it is O(m), the cost of reading the short list).
   For the lower bound, consider comparison algorithms on inputs where no aᵢ equals any b_j. When the algorithm stops,
   it must know for every aᵢ the gap (b_j, b_{j+1}) that holds it: if aᵢ and some b_j are incomparable in the order
   its outcomes imply, there is a linear extension in which they are adjacent, and making them equal changes no
   outcome but makes the intersection non-empty, so the algorithm is wrong on one of the two inputs. Because the aᵢ
   are sorted, the gaps form a non-decreasing sequence of m of the n + 1 slots, which can be chosen in C(n + m, m)
   ways, and each comparison (never "equal" here) has two outcomes. So some input needs at least
   log₂ C(n + m, m) ≥ m log₂((n + m)/m) ≥ m log₂(n/m) comparisons. On the novels, *love* AND *marriag* (500 and 2,363
   postings) took 1,915 comparisons, against m log₂(n/m) ≈ 1,120, within the factor of 2 of the analysis. *The* AND
   *whale* took 1,418, below the worst case's log₂ C(11,647, 390) ≈ 2,459, because every *whale* passage contains
   *the*: the bound is for the worst input, and adaptive analyses (Demaine, López-Ortiz and Munro) measure how hard an
   instance is.

2. **Code lengths.** Derive the lengths of Elias γ and δ codes, and the Golomb parameter that is optimal for geometric
   gaps.

   *Solution.* A gap g ≥ 1 has L = ⌊log₂ g⌋ + 1 binary digits, the first always 1. γ writes L − 1 zeros and then the
   L digits; the decoder counts zeros to learn how many digits follow, so the code is prefix-free and
   |γ(g)| = 2⌊log₂ g⌋ + 1. For each L there are 2^(L−1) gaps of length 2L − 1, so Σ 2^(−|γ(g)|) = Σ_L 2^(−L) = 1:
   the code is complete, and by Kraft it is ideal for P(g) = 2^(−|γ(g)|) ≈ 1/(2g²). δ writes L in γ and then the
   L − 1 digits after the leading 1: |δ(g)| = ⌊log₂ g⌋ + 2⌊log₂(⌊log₂ g⌋ + 1)⌋ + 1 = log₂ g + O(log log g), so it
   wins for large gaps. For g = 9, γ = `0001001` (7 bits) and δ = `00100001` (8); for g = 100, 13 bits against 11.
   For Golomb's code, let each passage hold the term independently with p = f/N, so P(g) = (1 − p)^(g−1) p. Write
   g − 1 = qM + r with 0 ≤ r < M. Then P(q) = Σ_r (1 − p)^(qM+r) p = θ^q (1 − θ), with θ = (1 − p)^M: the quotient is
   geometric again. Unary spends q + 1 bits, which is ideal when P(q) = 2^(−(q+1)), that is when θ = ½:
   (1 − p)^M = ½, M = ln 2 / (−ln(1 − p)) ≈ 0.69/p = 0.69 N/f. Within a block the probability of r falls only by the
   factor θ = ½ from one end to the other, so a (truncated) binary remainder is nearly ideal. The exact integer optimum
   is M = ⌈log(2 − p) / (−log(1 − p))⌉ (Gallager and van Voorhis, 1975). For *whale*, p = 390/11,261: M ≈ 19.7, the
   integer optimum 20, and under the geometric model 6.30 bits per gap with M = 20 and 6.32 with Rice's M = 16
   (k = 4), against the model's entropy of 6.27 bits. Real postings cluster, which is why the whole index's Rice
   codes (4.96 bits) sit a little above log₂ C(N, f) (4.74).

3. **BM25.** Derive BM25's term weight from the binary independence model with a two-Poisson approximation, and
   explain k₁ and b.

   *Solution.* Rank by the odds of relevance; by Bayes' rule and independence of terms given relevance, the log
   odds are, up to terms that do not depend on the passage, Σ over query terms present of
   w_t = log [p_t (1 − u_t)] / [u_t (1 − p_t)], where p_t and u_t are the chances that t occurs in a relevant and in
   an irrelevant passage. With no relevance information take p_t = ½, and since almost every passage is irrelevant
   u_t ≈ df/N: w_t = log((N − df)/df), with 0.5 added to each count to give the Robertson–Spärck Jones weight
   log((N − df + 0.5)/(df + 0.5)). It is negative for df > N/2 (for *the*, in 11,257 of 11,261 passages, −7.82), so
   Lucene and our `rank.py` use log(1 + (N − df + 0.5)/(df + 0.5)): 0.0004 for *the*, 3.36 for *whale*. The binary
   model ignores how often t occurs. Harter's two-Poisson model says a passage is either elite for t (about it) or
   not, with tf Poisson of mean λ in the first case and μ < λ in the second, the mixing weights depending on
   relevance. The weight of a count is then w(tf) = log [P(tf | R) P(0 | R̄)] / [P(tf | R̄) P(0 | R)]: it is 0 at
   tf = 0, rises with tf, and as tf grows the elite component dominates both mixtures, so w tends to a limit, the
   weight of eliteness itself, which plays the part of the binary model's weight. The model's four parameters cannot
   be estimated without relevance data, so Robertson and Walker kept only that shape: w(tf) ≈ w_t · tf/(tf + k₁),
   scaled by k₁ + 1 so that a single occurrence scores exactly w_t (a common factor, so the ranking is unchanged):
   tf(k₁ + 1)/(tf + k₁). k₁ sets how fast the count saturates: k₁ → 0 gives the binary model, k₁ → ∞ raw counts;
   with k₁ = 1.2 the factor is 1, 1.375, 1.774 and 1.964 at tf = 1, 2, 5 and 10, tending to 2.2. For length, a long
   passage has more occurrences because it is long (the verbosity hypothesis), so measure tf against the passage's
   relative length B = 1 − b + b|d|/avgdl: (tf/B)(k₁ + 1)/(tf/B + k₁) = tf(k₁ + 1)/(tf + k₁B). b = 0 ignores length
   (long passages cover more topics, the scope hypothesis); b = 1 normalises fully. With b = 0.75, a passage twice the
   average length has K = k₁B = 2.1 and scores 0.71 for one occurrence and 1.07 for two; one half the average, K = 0.75
   and 1.26 for one. Our passages are all about 400 words, so b changes little here.

4. **PageRank.** Show that PageRank is the stationary distribution of a Markov chain, and that power iteration
   converges at rate d.

   *Solution.* Let M be the N × N matrix with M_pq = 1/L(q) when q links to p (L(q) its number of links) and
   M_pq = 1/N for every p when q has no links; each column sums to 1. Let G = dM + (1 − d)/N · 𝟏𝟏ᵀ. G_pq is the
   chance that a surfer on q moves to p next (with probability d follow a random link, otherwise jump to a page chosen
   uniformly), its columns sum to d + (1 − d) = 1, and (Gr)_p = (1 − d)/N + d Σ_{q→p} r_q/L(q) (with dangling pages'
   rank spread evenly), which is the PageRank equation. So a vector r ≥ 0 with Σr = 1 and r = Gr is exactly a
   stationary distribution of that chain. Every entry of G is at least (1 − d)/N > 0, so the chain is irreducible and
   aperiodic, and by Perron–Frobenius the eigenvalue 1 is simple with a positive eigenvector: r exists and is unique.
   For convergence take any z with Σz = 0 (the difference of two probability vectors): 𝟏ᵀz = 0, so Gz = dMz, and
   since M has non-negative entries and columns summing to 1, ‖Mz‖₁ ≤ Σ_q |z_q| Σ_p M_pq = ‖z‖₁. Hence
   ‖Gz‖₁ ≤ d‖z‖₁, and the iterates r_k = G^k r₀ satisfy ‖r_k − r‖₁ ≤ d^k ‖r₀ − r‖₁ ≤ 2d^k, and successive changes
   shrink by at least d: ‖r_{k+1} − r_k‖₁ ≤ d^k ‖r₁ − r₀‖₁. (Equivalently, every other eigenvalue of G has modulus at
   most d; Haveliwala and Kamvar, 2003.) The bound does not depend on N: getting below 10⁻⁶ from at most 2 takes
   log(2 × 10⁶)/log(1/0.85) ≈ 89 steps for any web. On our synthetic web the change was 1.04 after the first step;
   the bound allows 1.04 × 0.85³⁹ ≈ 1.8 × 10⁻³ after forty, and we measured 1.1 × 10⁻⁶, shrinking by about 0.81 a
   step near the end.

5. **Build.** Add block-max WAND to our engine (score bounds per block of postings) and measure how many more
   documents it skips.

   *Solution notes.* In `rank.wand` each term's list is already a list of (passage, contribution) pairs with one
   bound `ub[i]`, its largest contribution. In the same pass, cut each list into blocks of B postings (say 64) and
   store, for each block, its last passage and its largest contribution; give each cursor a block pointer as well.
   Pick the pivot exactly as now, with the global bounds. Then make the shallow check: for every cursor whose current
   passage is no later than the pivot's, move only its block pointer to the block that would contain the pivot's
   passage (no postings are read), and add those blocks' maxima. If the sum exceeds θ, continue as WAND does: score
   the pivot if every such cursor is on it, else advance them to it. If not, no passage up to the end of the shortest
   of those blocks can reach θ: move those cursors to the smaller of (the earliest block end + 1) and the current
   passage of the first other cursor, without scoring anything. Count fully scored passages as `scored` does, and
   count block checks separately. Check safety exactly as `test_wand_matches_exhaustive` does, against
   `top(bm25_scores(...))`, on the toy documents and on the five queries of `compute_wand`, score for score. Then
   report, for block sizes 32, 64 and 128, the passages fully scored by WAND (235, 117, 1,144, 359 and 213 for the five
   queries) and by block-max WAND. Our passages all have about 400 words, so a term's contributions vary mainly with
   tf; expect the largest gains for long lists whose maximum is set by a few passages with a high count, and little
   for *pride prejudice*, whose terms are rare. Our cursors advance one posting at a time, so to turn skipped
   passages into saved time the cursor moves should also use the skip pointers or galloping of Chapter 3.

6. **★ Research.** Find a graph-based nearest-neighbour index with provable recall and query time on realistic data.

   *Discussion.* Open. Graph indexes such as HNSW win the benchmarks (ours finds 81% of the true top ten for 467 of
   3,000 distances), but their guarantees are heuristic: on adversarial inputs the greedy walk can stall far from the
   answer, and Indyk and Xu (NeurIPS 2023) built instances on which HNSW and other popular graphs need time linear in
   n, while proving bounds for one slowly built variant of DiskANN's graph on data of bounded doubling dimension.
   Structures with guarantees in doubling dimension, such as navigating nets (Krauthgamer and Lee, 2004) and cover
   trees (Beygelzimer, Kakade and Langford, 2006), and locality-sensitive hashing in high dimension (Part 20), lose in
   practice, and doubling dimension is a worst-case measure that may be large for real embeddings. A good answer
   would fix a model of realistic data (low intrinsic dimension in some measured sense, or a generative model of
   embeddings), give a graph built in near-linear time with degree and query time polylogarithmic in n (exponential
   only in the intrinsic dimension), prove recall at least 1 − δ for beam search on it, and show on real vectors that
   the model's assumptions hold. Partial results for a single beam width, for random data on a sphere, or a lower
   bound showing what no sparse graph can achieve, would already be new.

## 习题与解答

1. **倍增查找求交。** 证明对长度为 m ≤ n 的两个表，倍增（跳跃式）查找求交需要 O(m log(n/m)) 次比较，并证明这在常数因子内是最优的。

   *解答。* 设短表为 a₁ < … < a_m，长表为 b₁ < … < b_n。倍增查找在长表中维护一个只会向前移动的位置。对 aᵢ，它向前探查 1、2、4、
   8……个位置，直到某次探查到达 ≥ aᵢ 的值或越过表尾，再在最后一个区间里二分查找，最后做一次相等比较。若位置前进了 gᵢ 个位置，
   倍增至多探查 log₂(gᵢ + 1) + 1 次，留下的区间不到 gᵢ + 1 个位置，所以查找 aᵢ 至多花 2 log₂(gᵢ + 1) + 3 次比较。各 gᵢ 之和至多为 n，
   而 log 是凹函数，由 Jensen 不等式 Σ log₂(gᵢ + 1) ≤ m log₂(n/m + 1)。总数至多 2m log₂(n/m + 1) + 3m = O(m(1 + log(n/m)))，
   当 n ≥ 2m 时就是 O(m log(n/m))（n < 2m 时是 O(m)，即读一遍短表的代价）。
   下界：考虑基于比较的算法，输入中没有 aᵢ 等于任何 b_j。算法停下时，它必须知道每个 aᵢ 落在哪个间隙 (b_j, b_{j+1}) 中：如果在它的
   比较结果所蕴含的顺序里 aᵢ 与某个 b_j 不可比，就存在一个线性扩张使二者相邻，把它们设为相等不改变任何比较结果，却使交集非空，
   所以算法在这两个输入之一上出错。由于 aᵢ 有序，这些间隙构成 n + 1 个位置中 m 个位置的非降序列，共有 C(n + m, m) 种选法，而每次比较
   （这里从不出现“相等”）只有两种结果。所以某个输入至少需要 log₂ C(n + m, m) ≥ m log₂((n + m)/m) ≥ m log₂(n/m) 次比较。在小说上，
   *love* AND *marriag*（500 和 2,363 个倒排项）用了 1,915 次比较，而 m log₂(n/m) ≈ 1,120，在分析给出的 2 倍之内。*the* AND *whale*
   用了 1,418 次，低于最坏情形的 log₂ C(11,647, 390) ≈ 2,459，因为每个含 *whale* 的段落都含 *the*：下界针对最坏的输入，而自适应分析
   （Demaine、López-Ortiz 与 Munro）衡量的是一个实例有多难。

2. **编码长度。** 推导 Elias γ 码和 δ 码的长度，以及对服从几何分布的间隔最优的 Golomb 码参数。

   *解答。* 间隔 g ≥ 1 有 L = ⌊log₂ g⌋ + 1 位二进制数字，第一位总是 1。γ 码先写 L − 1 个 0，再写这 L 位数字；解码器数 0 的个数就知道
   后面跟着几位，所以它是前缀码，|γ(g)| = 2⌊log₂ g⌋ + 1。对每个 L 有 2^(L−1) 个长度为 2L − 1 的间隔，所以
   Σ 2^(−|γ(g)|) = Σ_L 2^(−L) = 1：这个码是完备的，由 Kraft 不等式，它对 P(g) = 2^(−|γ(g)|) ≈ 1/(2g²) 是理想的。δ 码先用 γ 码写 L，
   再写首位 1 之后的 L − 1 位：|δ(g)| = ⌊log₂ g⌋ + 2⌊log₂(⌊log₂ g⌋ + 1)⌋ + 1 = log₂ g + O(log log g)，所以间隔大时它更短。g = 9 时，
   γ = `0001001`（7 位），δ = `00100001`（8 位）；g = 100 时为 13 位对 11 位。
   对 Golomb 码，设每个段落独立地以概率 p = f/N 含有该词项，于是 P(g) = (1 − p)^(g−1) p。写 g − 1 = qM + r，0 ≤ r < M。则
   P(q) = Σ_r (1 − p)^(qM+r) p = θ^q (1 − θ)，其中 θ = (1 − p)^M：商仍服从几何分布。一元码花 q + 1 位，当 P(q) = 2^(−(q+1))、即
   θ = ½ 时最理想：(1 − p)^M = ½，M = ln 2 / (−ln(1 − p)) ≈ 0.69/p = 0.69 N/f。在一个块内，r 的概率从一端到另一端只下降 θ = ½ 倍，
   所以（截断的）二进制余数几乎是理想的。精确的整数最优值是 M = ⌈log(2 − p) / (−log(1 − p))⌉（Gallager 与 van Voorhis，1975）。
   对 *whale*，p = 390/11,261：M ≈ 19.7，整数最优值为 20；在几何模型下，M = 20 时每个间隔 6.30 位，Rice 码的 M = 16（k = 4）为
   6.32 位，而模型的熵是 6.27 位。真实的倒排表是成簇的，所以整个索引的 Rice 码（4.96 位）比 log₂ C(N, f)（4.74 位）略高。

3. **BM25。** 从二元独立模型出发，借助双泊松近似推导 BM25 的词项权重，并解释 k₁ 和 b。

   *解答。* 按相关的几率排序；由贝叶斯法则以及给定相关性时各词项独立，对数几率除去与段落无关的项外，等于对段落中出现的查询词项求和
   w_t = log [p_t (1 − u_t)] / [u_t (1 − p_t)]，其中 p_t、u_t 分别是 t 出现在相关段落和不相关段落中的概率。没有相关性信息时取
   p_t = ½；几乎所有段落都不相关，所以 u_t ≈ df/N：w_t = log((N − df)/df)，各计数加 0.5 就得到 Robertson–Spärck Jones 权重
   log((N − df + 0.5)/(df + 0.5))。当 df > N/2 时它是负的（*the* 出现在 11,261 个段落中的 11,257 个里，权重为 −7.82），所以 Lucene
   和我们的 `rank.py` 用 log(1 + (N − df + 0.5)/(df + 0.5))：*the* 为 0.0004，*whale* 为 3.36。二元模型不管 t 出现了几次。Harter 的
   双泊松模型说，一个段落对 t 要么是“精英”的（讲的就是它），要么不是；前一种情形 tf 服从均值 λ 的泊松分布，后一种服从均值 μ < λ 的
   泊松分布，混合权重取决于相关性。于是一个计数的权重为 w(tf) = log [P(tf | R) P(0 | R̄)] / [P(tf | R̄) P(0 | R)]：tf = 0 时为 0，
   随 tf 上升；tf 增大时精英分量在两个混合分布中都占主导，所以 w 趋于一个极限，即“精英”本身的权重，它扮演二元模型中权重的角色。
   这个模型的四个参数没有相关性数据就无法估计，所以 Robertson 与 Walker 只保留了它的形状：w(tf) ≈ w_t · tf/(tf + k₁)，再乘以
   k₁ + 1，使出现一次时恰好得 w_t（这是公共因子，不改变排序）：tf(k₁ + 1)/(tf + k₁)。k₁ 决定计数饱和得多快：k₁ → 0 退回二元模型，
   k₁ → ∞ 就是原始计数；k₁ = 1.2 时，tf = 1、2、5、10 对应的因子为 1、1.375、1.774、1.964，趋于 2.2。关于长度：长段落出现次数多是
   因为它长（冗长假设），所以用段落的相对长度 B = 1 − b + b|d|/avgdl 来衡量 tf：(tf/B)(k₁ + 1)/(tf/B + k₁) = tf(k₁ + 1)/(tf + k₁B)。
   b = 0 不考虑长度（长段落涵盖更多话题，即范围假设）；b = 1 完全归一化。取 b = 0.75，长度为平均两倍的段落 K = k₁B = 2.1，出现一次
   得 0.71，两次得 1.07；长度为平均一半时 K = 0.75，出现一次得 1.26。我们的段落都约 400 词，所以这里 b 影响不大。

4. **PageRank。** 证明 PageRank 是一个马尔可夫链的平稳分布，并证明幂迭代以速率 d 收敛。

   *解答。* 设 M 为 N × N 矩阵：q 链接到 p 时 M_pq = 1/L(q)（L(q) 为 q 的链接数）；q 没有链接时对所有 p 取 M_pq = 1/N；每一列之和
   为 1。令 G = dM + (1 − d)/N · 𝟏𝟏ᵀ。G_pq 是停在 q 上的冲浪者下一步到 p 的概率（以概率 d 随机点一个链接，否则均匀地跳到任一页面），
   它的列和为 d + (1 − d) = 1，而 (Gr)_p = (1 − d)/N + d Σ_{q→p} r_q/L(q)（没有链接的页面把排名平均分给所有页面），这正是 PageRank
   方程。所以满足 r ≥ 0、Σr = 1、r = Gr 的向量恰好是这个链的平稳分布。G 的每个元素至少为 (1 − d)/N > 0，所以这个链不可约且非周期，
   由 Perron–Frobenius 定理，特征值 1 是单重的，并有正的特征向量：r 存在且唯一。关于收敛：取任意满足 Σz = 0 的 z（两个概率向量之差），
   则 𝟏ᵀz = 0，所以 Gz = dMz；又因 M 的元素非负、列和为 1，‖Mz‖₁ ≤ Σ_q |z_q| Σ_p M_pq = ‖z‖₁。因此 ‖Gz‖₁ ≤ d‖z‖₁，迭代
   r_k = G^k r₀ 满足 ‖r_k − r‖₁ ≤ d^k ‖r₀ − r‖₁ ≤ 2d^k，相邻两步的变化也至少按 d 缩小：‖r_{k+1} − r_k‖₁ ≤ d^k ‖r₁ − r₀‖₁。（等价地，
   G 的其他特征值的模都不超过 d；Haveliwala 与 Kamvar，2003。）这个界与 N 无关：从至多 2 降到 10⁻⁶ 以下，对任何规模的网页都只需
   log(2 × 10⁶)/log(1/0.85) ≈ 89 步。在我们的合成网页上，第一步的变化是 1.04；这个界在第四十步时允许 1.04 × 0.85³⁹ ≈ 1.8 × 10⁻³，
   而实测为 1.1 × 10⁻⁶，临近结束时每步缩小约 0.81 倍。

5. **动手。** 给我们的引擎加上 block-max WAND（每个倒排块一个得分上界），并测量它多跳过了多少文档。

   *解答要点。* 在 `rank.wand` 中，每个词项的表已经是（段落，得分贡献）对的列表，并有一个上界 `ub[i]`，即它最大的贡献。在同一遍里把
   每个表切成 B 个倒排项一块（比如 64），为每块存下它的最后一个段落号和块内最大的贡献；再给每个游标一个块指针。仍像现在这样用全局
   上界选出枢轴。然后做浅层检查：对当前段落不晚于枢轴段落的每个游标，只把它的块指针移到可能包含枢轴段落的那一块（不读任何倒排项），
   把这些块的最大值相加。若和超过 θ，就照 WAND 的做法继续：这些游标都在枢轴上时给枢轴打分，否则把它们推进到枢轴。若不超过，则直到
   这些块中最早结束的那块的末尾，没有段落能达到 θ：把这些游标移到（最早的块末尾 + 1）与第一个其他游标的当前段落两者中较小的那个，
   一个也不打分。完整打分的段落照 `scored` 那样计数，块检查另行计数。安全性的检验与 `test_wand_matches_exhaustive` 一样，与
   `top(bm25_scores(...))` 比较，在玩具文档和 `compute_wand` 的五个查询上逐个分数核对。然后对块大小 32、64、128 报告 WAND（五个查询
   分别为 235、117、1,144、359、213）和 block-max WAND 完整打分的段落数。我们的段落都约 400 词，所以一个词项的贡献主要随 tf 变化；
   可以预期，最大值由少数高频段落决定的长表收益最大，而词项都很罕见的 *pride prejudice* 收益很小。我们的游标一次只前进一个倒排项，
   要把跳过的段落变成省下的时间，游标的移动还应当用上第 3 章的跳表指针或倍增查找。

6. **★ 研究。** 求一个基于图的最近邻索引，在现实的数据上有可证明的召回率和查询时间。

   *讨论。* 尚未解决。HNSW 这样的图索引在基准测试中领先（我们的图用 3,000 次中的 467 次距离计算找到真正前十中的 81%），但它们的
   保证是启发式的：在对抗性的输入上，贪心游走可能停在离答案很远的地方。Indyk 与 Xu（NeurIPS 2023）构造了使 HNSW 等常用图需要关于
   n 线性时间的实例，同时对 DiskANN 的图的一种慢速构建的变体，在倍增维度有界的数据上证明了界。在倍增维度下有保证的结构，如导航网
   （Krauthgamer 与 Lee，2004）和覆盖树（Beygelzimer、Kakade 与 Langford，2006），以及高维中的局部敏感哈希（第20部分），在实践中
   都不如图索引；而倍增维度是最坏情形的度量，对真实的嵌入向量可能很大。好的答案应当确定一个现实数据的模型（某种可测意义下的低内在
   维度，或嵌入向量的生成模型），给出一个近线性时间构建、度数和查询时间关于 n 为多对数（只对内在维度是指数的）的图，证明在它上面的
   束搜索召回率至少为 1 − δ，并在真实向量上表明模型的假设成立。仅对单一束宽、对球面上的随机数据的部分结果，或者说明任何稀疏图都做不到
   什么的下界，就已经是新的。

## Glossary additions

* **token, case folding, stop word, stem, lemmatizer** — the units a search engine indexes, and how words are
  normalised into terms.
* **Zipf's law, Heaps' law, hapax legomenon** — frequency against rank; vocabulary against text read; a word seen
  once.
* **inverted index, dictionary, postings, document frequency (df)** — from each term to the sorted passages that
  contain it.
* **blocked sort-based indexing, single-pass in-memory indexing, segment** — building an index larger than memory;
  an immutable piece of an index that changes.
* **skip pointer, galloping (exponential) search, positional index, phrase query** — faster intersection; positions
  for adjacent words.
* **gap, variable-byte code, Elias γ and δ codes, Golomb and Rice codes, PForDelta** — postings stored as small
  numbers in short codes.
* **tf-idf, vector space model, cosine similarity** — weighting terms and ranking by angle.
* **probability ranking principle, binary independence model, two-Poisson model, BM25, k₁, b** — ranking by the
  probability of relevance; its estimate from words; saturation and length normalisation.
* **precision, recall, average precision, MAP, DCG, nDCG, test collection, pooling, sign test** — measuring a
  ranking against judgments.
* **dynamic pruning, max-score, WAND, pivot, block-max WAND, safe and unsafe, tiered index, champion list** —
  finding the top k without scoring every candidate.
* **PageRank, damping factor, teleportation, Google matrix, power iteration, HITS, hub, authority, link farm,
  TrustRank** — ranking pages by links, and gaming it.
* **crawler, frontier, politeness, robots.txt, freshness, URL normalisation, shingle, SimHash, near-duplicate** —
  fetching the web, keeping it fresh, and recognising copies.
* **document- and term-partitioned index, broker, shard, replica, fan-out, hedged request, result cache, postings
  cache** — serving one query from many machines.
* **noisy channel, edit distance (Levenshtein, Damerau), BK-tree, trie, autocompletion** — guessing what the user
  meant to type.
* **learning to rank, pointwise, pairwise, listwise, RankNet, LambdaRank, LambdaMART, position bias, cascade model,
  inverse propensity weighting** — learning a ranking function from judgments and clicks.
* **dense retrieval, embedding, product quantization, codebook, asymmetric distance, inverted file, HNSW, beam width,
  recall@10** — searching by nearness of vectors, compressed and approximate.
* **hybrid retrieval, reciprocal rank fusion, learned sparse retrieval, late interaction, retrieval-augmented
  generation, generative retrieval** — combining words and vectors, and retrieval for language models.

## Sources

* C. D. Manning, P. Raghavan and H. Schütze, *Introduction to Information Retrieval* (2008); S. Büttcher, C. L. A.
  Clarke and G. V. Cormack, *Information Retrieval: Implementing and Evaluating Search Engines* (2010); I. H. Witten,
  A. Moffat and T. C. Bell, *Managing Gigabytes* (2nd ed., 1999).
* M. F. Porter, "An algorithm for suffix stripping", Program 1980; G. K. Zipf, *Human Behavior and the Principle of
  Least Effort* (1949); H. S. Heaps, *Information Retrieval: Computational and Theoretical Aspects* (1978).
* J. Zobel and A. Moffat, "Inverted files for text search engines", ACM Computing Surveys 2006; S. Heinz and J. Zobel,
  "Efficient single-pass index construction for text databases", JASIST 2003; A. Moffat and J. Zobel,
  "Self-indexing inverted files for fast text retrieval", ACM TOIS 1996; J. Bentley and A. Yao, "An almost optimal
  algorithm for unbounded searching", Information Processing Letters 1976; E. Demaine, A. López-Ortiz and J. I.
  Munro, "Adaptive set intersections, unions, and differences", SODA 2000.
* P. Elias, "Universal codeword sets and representations of the integers", IEEE Trans. Inf. Theory 1975; S. Golomb,
  "Run-length encodings", IEEE Trans. Inf. Theory 1966; R. Gallager and D. van Voorhis, "Optimal source codes for
  geometrically distributed integer alphabets", IEEE Trans. Inf. Theory 1975; M. Zukowski, S. Héman, N. Nes and
  P. Boncz, "Super-scalar RAM-CPU cache compression", ICDE 2006; D. Lemire and L. Boytsov, "Decoding billions of
  integers per second through vectorization", Software: Practice and Experience 2015.
* K. Spärck Jones, "A statistical interpretation of term specificity and its application in retrieval", Journal of
  Documentation 1972; S. Robertson and K. Spärck Jones, "Relevance weighting of search terms", JASIS 1976;
  S. Robertson, "The probability ranking principle in IR", Journal of Documentation 1977; S. Harter, "A probabilistic
  approach to automatic keyword indexing", JASIS 1975; S. Robertson and S. Walker, "Some simple effective
  approximations to the 2-Poisson model for probabilistic weighted retrieval", SIGIR 1994; S. Robertson and
  H. Zaragoza, "The probabilistic relevance framework: BM25 and beyond", Foundations and Trends in Information
  Retrieval 2009.
* K. Järvelin and J. Kekäläinen, "Cumulated gain-based evaluation of IR techniques", ACM TOIS 2002; J. Zobel, "How
  reliable are the results of large-scale information retrieval experiments?", SIGIR 1998.
* H. Turtle and J. Flood, "Query evaluation: strategies and optimizations", Information Processing & Management 1995;
  A. Broder, D. Carmel, M. Herscovici, A. Soffer and J. Zien, "Efficient query evaluation using a two-level retrieval
  process", CIKM 2003; S. Ding and T. Suel, "Faster top-k document retrieval using block-max indexes", SIGIR 2011.
* S. Brin and L. Page, "The anatomy of a large-scale hypertextual Web search engine", WWW 1998; J. Kleinberg,
  "Authoritative sources in a hyperlinked environment", J. ACM 1999; Z. Gyöngyi, H. Garcia-Molina and J. Pedersen,
  "Combating Web spam with TrustRank", VLDB 2004.
* A. Heydon and M. Najork, "Mercator: a scalable, extensible Web crawler", World Wide Web 1999; J. Cho and
  H. Garcia-Molina, "Synchronizing a database to improve freshness", SIGMOD 2000; M. Charikar, "Similarity estimation
  techniques from rounding algorithms", STOC 2002; G. S. Manku, A. Jain and A. Das Sarma, "Detecting near-duplicates
  for web crawling", WWW 2007; RFC 9309, *Robots Exclusion Protocol* (2022).
* L. A. Barroso, J. Dean and U. Hölzle, "Web search for a planet: the Google cluster architecture", IEEE Micro 2003;
  J. Dean and L. A. Barroso, "The tail at scale", Communications of the ACM 2013; R. Baeza-Yates et al., "The impact
  of caching on search engines", SIGIR 2007.
* F. Damerau, "A technique for computer detection and correction of spelling errors", Communications of the ACM
  1964; W. Burkhard and R. Keller, "Some approaches to best-match file searching", Communications of the ACM 1973;
  M. Kernighan, K. Church and W. Gale, "A spelling correction program based on a noisy channel model", COLING 1990.
* C. Burges et al., "Learning to rank using gradient descent", ICML 2005; C. Burges, "From RankNet to LambdaRank to
  LambdaMART: an overview", Microsoft Research Technical Report MSR-TR-2010-82 (2010); T. Joachims et al.,
  "Accurately interpreting clickthrough data as implicit feedback", SIGIR 2005; N. Craswell, O. Zoeter, M. Taylor
  and B. Ramsey, "An experimental comparison of click position-bias models", WSDM 2008; T. Joachims, A. Swaminathan
  and T. Schnabel, "Unbiased learning-to-rank with biased feedback", WSDM 2017.
* H. Jégou, M. Douze and C. Schmid, "Product quantization for nearest neighbor search", IEEE TPAMI 2011; Y. Malkov
  and D. Yashunin, "Efficient and robust approximate nearest neighbor search using hierarchical navigable small world
  graphs", IEEE TPAMI 2018; V. Karpukhin et al., "Dense passage retrieval for open-domain question answering", EMNLP
  2020; G. Cormack, C. Clarke and S. Büttcher, "Reciprocal rank fusion outperforms Condorcet and individual rank
  learning methods", SIGIR 2009; N. Thakur et al., "BEIR: a heterogeneous benchmark for zero-shot evaluation of
  information retrieval models", NeurIPS 2021 Datasets and Benchmarks.
* O. Khattab and M. Zaharia, "ColBERT: efficient and effective passage search via contextualized late interaction
  over BERT", SIGIR 2020; T. Formal, B. Piwowarski and S. Clinchant, "SPLADE: sparse lexical and expansion model for
  first stage ranking", SIGIR 2021; Y. Tay et al., "Transformer memory as a differentiable search index", NeurIPS
  2022; P. Indyk and H. Xu, "Worst-case performance of popular approximate nearest neighbor search implementations:
  guarantees and limitations", NeurIPS 2023.
