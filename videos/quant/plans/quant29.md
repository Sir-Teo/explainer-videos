# Part 29 · Alpha Mining and Automated Research: build plan (PhD layer built in)

Target: hook + 17 chapters + research + outro, 55–60 minutes. Every number from `videos/quant/quant29/compute.py`.
The mining ground is Part 27's survivorship-free panel of every Binance USDT coin (daily candles; weekly
cross-sections), research to December 2020, 2021–2025 sealed.

## House: `explainer/quant/house/alphas.py`

Expression trees over daily fields (close, open, high, low, quote volume, returns) with Kakushadze-style operators
(rank, ts_mean, ts_std, ts_rank, delta, delay, corr, sign, abs, log, +, −, ×, ÷); a vectorised evaluator on a
(days × coins) grid; random generation by depth; the count of formulas by depth; cross-sectional IC and its t;
genetic programming (tournament selection, subtree crossover, point mutation, a parsimony penalty); a REINFORCE token
generator (policy over reverse-Polish tokens, reward = gain in the combination's IC: AlphaGen's idea); combination
(equal weight, ridge-estimated, the shrinkage of Kan–Zhou); the counter.

## Chapters

0. Hook: a million formulas. Random formulas on coins: the best in-sample IC grows with N; out of sample it does not.
1. Formulaic alphas: Kakushadze (2016), *Wilmott*: 101 alphas, average pairwise correlation 15.9%, holding periods
   0.6–6.4 days; the operators; three of the 101 computed on coins.
2. The search space: how many formulas of depth d; why exhaustive search is impossible.
3. Random search and the winner's curse (Part 26's expected maximum, here in IC).
4. Genetic programming (Koza 1992): selection, crossover, mutation, bloat and parsimony; a run replayed.
5. Reinforcement learning: AlphaGen (Yu, Xue, Ao, Pan, He, Tu and He, KDD 2023): reward = contribution to the
   combination; a mini REINFORCE generator trained here.
6. LLM research agents: Alpha-GPT (Wang et al. 2023; top 10 of 41,000+ teams in WorldQuant's International Quant
   Championship; EMNLP 2025 demos); AlphaAgent (2025; originality via AST similarity; CSI 500 and S&P 500);
   R&D-Agent-Quant (Li et al., Microsoft, NeurIPS 2025 D&B: research and development agents, a bandit scheduler;
   reports up to 2× annualized returns of classical libraries with 70% fewer factors).
7. Combining weak alphas: correlation, breadth, the equal-weight limit IC/√ρ.
8. The counter explodes: millions of formulas against the hurdle.
9. Decay and crowding; the alpha factory (WorldQuant's model and its public BRAIN platform, public record only).
10. China's quant industry: index enhancement; the 2019–2023 boom; February 2024 (micro-caps −31% in the first five
    trading days of February; DMA swaps; a major quant fund's accounts frozen on 20 February; CSRC supervision of
    DMA), as reported by Reuters, Bloomberg and Caixin.
11. High-Flyer and DeepSeek (public record: founded c. 2015–16 by Liang Wenfeng; Fire-Flyer GPU clusters; DeepSeek
    launched 2023).
12. What remains for humans: priors, data, judgment.
13. The mined combination, registered and opened on 2021–2025.
14. Rule 29.
* Research: how many alphas can you combine? The out-of-sample Sharpe ratio of an estimated combination of K
  signals from T observations (Brown 1976; Kan and Zhou 2007): E[SR_oos] falls with K/T; proved, simulated, and
  checked on the mined alphas.
* Outro: recap, desk questions, twelve problems with two qual.
