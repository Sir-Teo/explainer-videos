# Part 28 · Text, LLMs and Alternative Data: build plan (new part, PhD layer built in)

Target: hook + 18 chapters + research + outro = 21 scenes, about 60 minutes (≈ 10,000 counted words at 168 wpm).
Every number from `videos/quant/quant28/compute.py`; research data through 2020-12-31; 2021–2025 sealed for the
envelope.

## Data (all public, cached and checksummed; loaders in `explainer/quant/data.py`)

* `fomc_index`, `fomc_text("statement")`: 234 FOMC statements, 1997–2025 (scheduled and unscheduled), the policy
  paragraphs before the vote; `fomc_text("minutes")`: 241 sets of minutes, 1996–2025, discussion paragraphs.
* `lm_dictionary`: the Loughran–McDonald master dictionary, 1993–2025 edition (free for academic use; cached, not
  redistributed; credited on screen).
* `fred("DGS2")`, `fred("DGS10")`: the 2- and 10-year Treasury yields, daily: the statement-day reaction.
* (No news archive is freely available: Tetlock, SESTM's Dow Jones Newswires, Lopez-Lira–Tang's headlines and
  Bybee et al.'s WSJ are described from their papers.)

## House: `explainer/quant/house/text.py` (done, tested)

tokenize, vocabulary, dtm, tfidf, zipf, tone/lm_sets, sestm_screen/sestm_topics/sestm_score, cooccurrence,
ppmi_svd, neighbours, nmf_topics, fog, word_diff, point_in_time_vocab, first_use, chebyshev_gap.

## Chapters

0. **Hook: one sentence.** The statement-day with the largest 2-year move in the research era, the word-level diff
   against the previous statement lighting up.
1. **Words as numbers.** Tokens, the document-term matrix, Zipf's law fitted on the FOMC corpus; tf-idf. Gentzkow,
   Kelly and Taddy (2019, *JEL*).
2. **Dictionaries.** Tetlock (2007, *JF* 62): WSJ "Abreast of the Market" pessimism (Harvard GI) predicts downward
   pressure then reversal, 1984–1999. Loughran–McDonald (2011, *JF* 66): 73.8% of Harvard negative word counts in
   10-Ks are not negative in finance (tax, cost, capital, board, liability, foreign, vice); Fin-Neg. Computed: LM
   negative and uncertainty shares of the statements over time.
3. **Tone and the 2-year yield.** Statement-day changes against tone and tone changes; regression and t-stats.
4. **Readability and length.** Fog index and word counts of statements 1997–2025 (the statement's growth).
5. **Supervised words: SESTM.** Ke, Kelly and Xiu (2019, NBER w26186): screen, topic, score; Dow Jones Newswires
   1989–2017, 22.5m articles; equal-weighted long-short Sharpe 4.29 (value-weighted 1.33) before costs. Fitted here
   on statements (train to 2012, test 2013–2020).
6. **Topics.** LDA idea; NMF topics on the minutes, shares over time; Bybee, Kelly, Manela and Xiu (2024, *JF* 79):
   800,000 WSJ articles 1984–2017, news attention tracks and forecasts activity.
7. **The FOMC's words.** Hansen, McMahon and Prat (2018, *QJE* 133): the October 1993 transcript revelation as a
   natural experiment; discipline vs conformity; LDA. Computed: forward-guidance phrases' first use and life.
8. **Embeddings.** Distributional meaning; PPMI + SVD on the minutes (Levy–Goldberg 2014); neighbours of inflation,
   accommodation, balance sheet; a 2-D map.
9. **Transformers and FinBERT.** Attention (AI series link); FinBERT (Huang, Wang and Yang 2023, *CAR* 40: 4.9bn
   tokens of filings, calls and analyst reports; beats LM on analyst-report sentences). Trained: a pocket LM on the
   minutes, replayed.
10. **LLMs read the news.** Lopez-Lira and Tang (2023): ChatGPT labels headlines, next-day returns; small models
    fail. Chen, Kelly and Xiu (2022): LLM embeddings of news across 16 markets. Kim, Muhn and Nikolaev (2024): GPT-4
    on anonymized statements, 60% direction accuracy with chain of thought vs analysts.
11. **Look-ahead bias.** Glasserman and Lin (2023): anonymised headlines; look-ahead vs distraction. Sarkar and Vafa
    (2024): tests on earnings calls and elections. He, Lv, Manela and Wu (2025): ChronoBERT/ChronoGPT.
12. **The time-sliced experiment, trained here.** Pocket LMs on minutes through 2007 vs through 2020; loss on
    2008–2012 text; next-word probabilities on crisis-era phrases.
13. **The look-ahead gap downstream.** Features from each model predicting the statement-day 2-year move; the leaked
    model's backtest flatters.
14. **LLM agents.** TradingAgents (Xiao, Sun, Luo and Wang 2024, arXiv 2412.20138): analyst, researcher, trader and
    risk roles; the look-ahead caveat.
15. **Alternative data.** Satellites: Katona, Painter, Patatoukas and Zeng (2025, *JFQA* 60): RS Metrics parking-lot
    counts 2011–2017, informed shorting, lower liquidity. Card panels, web traffic, job postings. Decay as data
    spreads, simulated.
16. **Domain models.** BloombergGPT (Wu et al. 2023): 50bn parameters; 363bn financial tokens + 345bn general.
17. **The text signal, registered and opened.** The SESTM statement score → post-statement 2-year drift, sealed
    2021–2025.
18. **Rule 28: text features.** Point-in-time vocabularies; dated models; the counter.
* **Research: SESTM's screening, proved.** Population lemma (Chebyshev's association inequality: f_j → π for
  neutral words, above π for positive words); Ke–Kelly–Xiu's sure-screening theorem (C.2) stated; recovery simulated
  by n and article length; applied to the statements.
* **Outro.** Recap, desk questions, ten problems + two qual problems.
