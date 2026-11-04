# Quant, Built — Part 28: Text, LLMs and Alternative Data

Part 28 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth part of Act IV, Return Premia (23–29), built to the series' PhD layer.
Part 27 ran every learner of empirical asset pricing through Part 26's validation; this part turns them on words. Its
corpus is thirty years of the Federal Open Market Committee's own documents, read against the bond market's reaction.
It covers:

* words as numbers: tokens, the document-term matrix, Zipf's and Heaps' laws, tf-idf;
* dictionaries: Tetlock's media pessimism, Loughran and McDonald's finance lists, and how each dictionary misreads a
  genre it was not built for (here, a central bank's mandate words);
* tone against the two-year Treasury yield on statement days, and why words move yields through the path of policy
  (Kuttner; Gürkaynak, Sack and Swanson) rather than their mood;
* length, readability, how much a statement changes, and the life of forward-guidance phrases;
* SESTM (Ke, Kelly and Xiu): words learned from outcomes, fitted on the statements;
* topics (non-negative factorisation; LDA) as eras of the committee's agenda; Bybee, Kelly, Manela and Xiu's news as
  macro data; Hansen, McMahon and Prat's transparency experiment;
* embeddings (PPMI and SVD, word2vec) learned from the minutes;
* transformers and FinBERT; a pocket language model trained here;
* LLMs reading headlines and financial statements (Lopez-Lira and Tang; Chen, Kelly and Xiu; Kim, Muhn and
  Nikolaev);
* look-ahead bias (Glasserman and Lin; Sarkar and Vafa; He, Lv, Manela and Wu) and a time-sliced experiment with three
  pocket models trained on different slices of history;
* LLM trading agents; alternative data and the arithmetic of a shared data set (Kyle with N insiders; Katona,
  Painter, Patatoukas and Zeng's satellites); domain models (BloombergGPT) and the text desk;
* **for the researcher**: why screening finds the sentiment words (a population lemma from Chebyshev's association
  inequality, Ke, Kelly and Xiu's sure-screening theorem), recovery simulated by sample size, and a permutation test on
  the statements; open problems;
* the statement score registered (13 trials) and opened on 2021–2025.

Every number is computed by the series' own code ([`compute.py`](compute.py) and the House's
[`text`](../../../explainer/quant/house/text.py) module). Data: every FOMC statement (1997–2025) and set of minutes
(1996–2025) linked from the Board's meeting pages; FRED's daily 2- and 10-year Treasury yields; the Loughran–McDonald
master dictionary (1993–2025 edition, free for academic use, cached and not redistributed).

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **Hook: one sentence** (2.2). The statement of 22 January 2008 (the intermeeting 75 bp cut) against 11 December
  2007, word by word; the two-year fell 28 bp, the largest statement-day move of 1997–2020 (typical: 7.2 bp); history
  from the General Inquirer to chronologically consistent LLMs; the plan; the House's reading room.
* **1. Words as numbers** (3.0). The bag of words; the document-term matrix: 193 statements and 199 minutes to 2020,
  1.32 million words, 10,253 distinct; Zipf's slope −0.98; Heaps' law (2,626 distinct words in 1996, 10,220 by 2020);
  tf-idf.
* **2. Dictionaries** (2.5). Tetlock (2007); Loughran–McDonald (2011): 73.8% of Harvard negative counts in 10-Ks are
  not negative in finance; today's lists (2,355 negative, 354 positive, 297 uncertainty); LM shares of the statements
  over time; the misfit: the most counted negative word is *unemployment*, the most counted positive *stability*.
* **3. Tone and the two-year yield** (2.6). The reaction (close to close, 2-year); a lab running `tone`; regression on
  net tone: t = 0.33 (change in tone −0.22, negative share −0.74, uncertainty −0.16); Kuttner (2001); Gürkaynak, Sack
  and Swanson (2005): the path factor.
* **4. Length, readability and forward guidance** (3.0). Median 153 words before 2002, 408 since 2016; fog 21.0 and
  22.8 (Loughran and McDonald 2014 on readability); how much each statement changes (median 1 − cos = 0.13; rank
  correlation with the size of the move 0.31, p ≈ 1e-5; 3.4 bp in the least-changed quarter, 7.8 bp in the most);
  forward-guidance phrases from *likely to be measured* (2004) to *ongoing increases* (2022).
* **5. Supervised words: SESTM** (4.0). Ke, Kelly and Xiu (Dow Jones Newswires 1989–2017, 22.5 million articles;
  equal-weighted Sharpe 4.29 before costs, value-weighted 1.33); the model; the screen on statements to 2012 (α = 0.20,
  κ = 10 chosen on 2007–2012; 11 hawkish and 25 dovish words of 704); the two topics; the House's screen; rank
  correlation 0.51 in sample, 0.06 on 2013–2020 (p = 0.64).
* **6. Topics** (2.9). NMF and LDA; a lab (`nmf_topics`, error 0.89 → 0.75); eight topics, named by their words; the
  minutes' river of eras; Bybee, Kelly, Manela and Xiu (2024).
* **7. Inside the FOMC** (2.6). What the committee publishes; Hansen, McMahon and Prat (2018); discipline and
  conformity (Meade and Stasavage 2008); the minutes' length before and after the three-week rule (January 2005).
* **8. Embeddings** (2.4). Firth; PPMI and SVD, Levy and Goldberg (2014); neighbours (inflation: expectations,
  core; tightening: easing; liquidity: facilities, swap lines); a map; tightening − raise + lower = easing.
* **9. Transformers and FinBERT** (2.6). Attention; Huang, Wang and Yang (2023); the pocket model (4 layers, d = 160,
  1.9 million parameters, BPE 2,048, 4 million training tokens); its training replayed.
* **10. LLMs read the news** (2.5). The Lopez-Lira–Tang prompt; their result (134,129 headlines, Oct 2021–Dec 2023,
  after GPT-4's training cut-off; GPT-1, GPT-2 and BERT fail); Chen, Kelly and Xiu (2022); Kim, Muhn and Nikolaev
  (2024: 52% and 60%); three questions.
* **11. Look-ahead bias** (2.5). The backtest inside the training data; skill + look-ahead − distraction;
  Glasserman and Lin (2023); Sarkar and Vafa (2024); He, Lv, Manela and Wu (2025).
* **12. The time-sliced experiment** (3.9). Models A (minutes to 2007), B (to 2020) and C (to 2007 and 2013–2020);
  bits per character on the 2008–12 minutes: A 1.15, C 0.86, B 0.71; on held-out pre-2008 minutes A is best (0.77
  against 0.80); the statements year by year (A jumps from 0.59 to 1.23 after 2008); probes (*0 to 1/4 percent*: A
  0.1%, C 52%, B 70%; *effective lower bound*: A ~0, C 83%; *forward guidance*: A ~0, C 96%); samples; the two layers
  of look-ahead.
* **13. LLM trading agents** (2.3). The ReAct loop; TradingAgents (Xiao, Sun, Luo and Wang 2024); four checks.
* **14. Alternative data** (2.6). The menu; Katona, Painter, Patatoukas and Zeng (2025); Kyle with N insiders (each
  profit ∝ N^−3/2, informativeness N/(N+1)), simulated; a stylised adoption curve.
* **15. Domain models and the text desk** (2.3). BloombergGPT (50bn parameters; 363bn financial and 345bn general
  tokens); training sizes on a log scale; Li et al. (2023); how firms use text.
* **16. The text signal, registered and opened** (2.8). SESTM on statements to 2020 → five-day position in the
  two-year note; 13 trials; research Sharpe −0.04; 2021–2025: 41 statements, +2.1 bp a trade, Sharpe 0.31 ± 0.52
  (net 0.13), hit rate 49%; PSR(0) = 0.72; about 330 statements needed for 95%; the reading; the counter 10,468.
* **17. Rule 28: text features** (1.9). The first sheet; a lab (`point_in_time_vocab`, `first_use`); the module;
  Rule 28; three cases.
* **For the researcher: why screening finds the words** (4.4). The lemma (f_j → E[g q_j]/E[q_j]; π for neutral words;
  above or below π for charged words, by Chebyshev's association inequality), proved; Ke, Kelly and Xiu's Theorem C.2;
  the limits checked on 20,000 simulated articles (positive 0.581 vs 0.581, negative 0.422 vs 0.419, neutral 0.502
  vs 0.500); recovery by n, θ and article length with a word-by-word threshold z = √(2 log m); the statements:
  36 words kept against 21 under shuffled labels (p = 0.09), none with the z screen; three open problems.
* **Recap, desk questions, problems** (3.5). Fourteen lines; six desk questions; twelve problems (two at
  qualifying-exam level), solutions below.

## Hands-on

* Trained here: three pocket language models (1.9 million parameters each) on three slices of the minutes, each with
  its own point-in-time BPE tokenizer; the SESTM screen, topics and scores; NMF topics; PPMI–SVD embeddings.
* Labs: `tone`, `nmf_topics`, `sestm_screen`, `point_in_time_vocab` and `first_use`, from the House's source.
* Simulations against theory: SESTM's screening limits and recovery; Kyle's market with N insiders.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| Gentzkow, Kelly and Taddy, "Text as data" (*JEL* 2019) | 2 (representing text), 3 (dictionaries, supervised and unsupervised methods), 4 (applications) | 1–6, 8 |
| Kelly and Xiu, *Financial Machine Learning* (2023) | the text chapter: dictionaries, SESTM, topic models, embeddings, LLMs | 2, 5, 6, 8–10 |
| Jurafsky and Martin, *Speech and Language Processing* | 2 (words, tokens), 6 (vector semantics), 9–10 (transformers, LLMs) | 1, 8, 9 |

## Papers, chapter by chapter

* Hook and ch. 1: Stone et al. (1966); Gentzkow, Kelly and Taddy (2019).
* ch. 2: Tetlock (2007), *JF* 62; Antweiler and Frank (2004), *JF* 59; Tetlock, Saar-Tsechansky and Macskassy (2008), *JF* 63; Loughran and McDonald (2011), *JF* 66.
* ch. 3: Kuttner (2001), *JME* 47; Gürkaynak, Sack and Swanson (2005), *IJCB* 1.
* ch. 4: Gunning (1952); Loughran and McDonald (2014), *JF* 69; Cohen, Malloy and Nguyen (2020), "Lazy prices", *JF* 75.
* ch. 5: Ke, Kelly and Xiu (2019), NBER w26186.
* ch. 6: Blei, Ng and Jordan (2003); Lee and Seung (1999); Bybee, Kelly, Manela and Xiu (2024), *JF* 79.
* ch. 7: Hansen, McMahon and Prat (2018), *QJE* 133; Meade and Stasavage (2008), *Economic Journal* 118; Shapiro and Wilson (2022), *REStud*; Gorodnichenko, Pham and Talavera (2023), *AER*.
* ch. 8: Firth (1957); Mikolov et al. (2013); Levy and Goldberg (2014).
* ch. 9: Vaswani et al. (2017); Huang, Wang and Yang (2023), *CAR* 40.
* ch. 10: Lopez-Lira and Tang (2023), arXiv 2304.07619; Chen, Kelly and Xiu (2022); Kim, Muhn and Nikolaev (2024),
  arXiv 2407.17866; Araci (2019); Hansen and Kazinnik (2023); Cao, Jiang, Wang and Yang (2024), *JFE*.
* ch. 11–12: Glasserman and Lin (2023), arXiv 2309.17322; Sarkar and Vafa (2024); He, Lv, Manela and Wu (2025), arXiv
  2502.21206.
* ch. 13: Yao et al. (2023), ReAct; Xiao, Sun, Luo and Wang (2024), arXiv 2412.20138.
* ch. 14: Kyle (1985); Admati and Pfleiderer (1988); Katona, Painter, Patatoukas and Zeng (2025), *JFQA* 60; Zhu (2019),
  *RFS* 32.
* ch. 15: Wu et al. (2023), arXiv 2303.17564; Li et al. (2023), EMNLP industry track.

## For the researcher

* **The theorems.** Ke, Kelly and Xiu (2019), Theorems C.1–C.5 (screening, topic estimation, scoring); Chebyshev's
  association (rearrangement) inequality; Kyle (1985) and Admati and Pfleiderer (1988) for N symmetric insiders.
* **Simplifications.** The statement-day close-to-close move as the label (Gürkaynak, Sack and Swanson use intraday
  futures windows); a one-sided screen on the share of positive moves (not centred at ½ as in the paper, but at the
  sample's own share π); NMF instead of LDA; pocket models of 1.9 million parameters; the Kyle adoption curve is
  stylised.
* **Open problems.** Screening under dependent documents; phrases and contextual features at a log²m price; combining
  a large-corpus prior with a small labelled set, with guarantees.

## Build it

```bash
python -m videos.quant.quant28.compute                           # every item; the three pocket LMs take ~25 min on 3 cores
python -m pytest -q tests/test_quant_house.py -k "text or sestm or embeddings"
EXPLAINER_TTS=silent python tools/qa_scene.py quant28 TimeSlice   # one chapter, silent, with a contact sheet
python tools/build.py quant28                                     # the narrated part
```

## Desk questions, with solutions

1. **An LLM signal at Sharpe 4 on 2015–2020 news.** First the model's training cut-off: if it read the period, the
   backtest can be memory (Chapter 12 measures how much). Then anonymise firm identifiers and re-run (Glasserman–Lin);
   then use a model dated before 2015 (He, Lv, Manela and Wu).
2. **Tone explains 30% of statement-day moves from the prior close.** The move happens minutes after release; a
   regression from the prior close explains, it does not forecast. Measure from just after release, or predict a
   later window (Chapter 16 does: nothing is left by the close).
3. **`Unemployment` is the most counted negative word.** For a central bank it is a mandate word; drop mandate words or
   learn weights from outcomes (SESTM) and test the learned list against chance.
4. **36 words from 113 documents.** Shuffle the labels and screen again: 21 on average, p ≈ 0.09; with the word-by-word
   z threshold, none survive (research chapter).
5. **A data set whose buyers double each year.** Each buyer's profit ∝ N^−3/2: doubling N divides it by 2^1.5 ≈ 2.8 a
   year; measure the decay live and buy early or not at all.
6. **A general LLM beats your fine-tuned FinBERT on 2024 data.** Use a model dated before the test, a fixed version,
   and the costs; specialists still win on narrow labelled tasks (Li et al. 2023).

## Problems, with solutions

1. **tf-idf and length.** Doubling counts doubles tf's numerator and denominator alike: tf is unchanged, so the row and
   its cosine with any other row are unchanged.
2. **Zipf's head.** With frequency ∝ 1/r, the top k cover H_k/H_V ≈ (ln k + 0.577)/(ln V + 0.577) = 5.18/9.79 ≈ 53%.
3. **Net tone.** (3 − 6)/300 = −1.0%; without the two `unemployment`s, (3 − 4)/300 = −0.33%.
4. **Screening by chance.** f_j = X/10 with X ~ Bin(10, ½); |f − ½| ≥ 0.2 ⇔ X ≤ 3 or X ≥ 7, probability 2 × 0.172 =
   0.344: about 103 of 300 words pass.
5. **SESTM's penalty.** λ log p(1 − p) = log[p^λ(1 − p)^λ], the log density of Beta(λ + 1, λ + 1) up to a constant; the
   penalized MLE is the MAP under that prior.
6. **PMI.** P(w, c) = P(w)P(c) gives log 1 = 0; negative PMI needs pairs rarer than chance, which small counts estimate
   badly, so PPMI sets them to zero.
7. **Fog.** 14 words, 1 sentence; three or more syllables: *Committee*, *decided*, *federal* (*unchanged* has two), so
   3 of 14 = 21.4%: fog = 0.4 (14 + 21.4) ≈ 14.2.
8. **Bits per character.** 3.5 / ln 2 / 4.2 ≈ 1.20.
9. **Glasserman–Lin.** Named minus anonymised = look-ahead − distraction = 1.2 − 1.5 = −0.3: distraction exceeds
   look-ahead in sample; out of sample both are 0.8, so the in-sample gap was not skill.
10. **Kyle with N insiders.** Each profit ∝ 1/((N + 1)√N): from 4 to 9, (5 × 2)/(10 × 3) = 1/3; the total ∝ √N/(N + 1):
    (3/10)/(2/5) = 0.75.
11. **(qual) Association and screening.** For p, p′ i.i.d., Cov(g(p), q(p)) = ½E[(g(p) − g(p′))(q(p) − q(p′))] ≥ 0 since
    both are increasing. In SESTM's model, by the law of large numbers f_j → Pr(y > 0 | j ∈ article) = E[g q_j]/E[q_j]
    with q_j(p) = 1 − (1 − pO+_j − (1 − p)O−_j)^s. For j ∈ N, q_j is constant and f_j → E g = π; for O+_j > O−_j, q_j is
    increasing and the limit is π + Cov(g, q_j)/E q_j > π (strictly, if both are strictly increasing); for O+_j < O−_j,
    below π.
12. **(qual) Kyle with N insiders.** Guess x_n = β(v − p₀), p = p₀ + λ(Σx_n + u). Insider n maximises
    E[(v − p)x_n | v] = x_n(v − λx_n − λ(N − 1)βv) (taking p₀ = 0): x_n = (1 − λ(N − 1)β)v/(2λ), so β = 1/(λ(N + 1)).
    Market efficiency: λ = Cov(v, y)/Var(y) with y = Nβv + u: λ = Nβσ_v²/(N²β²σ_v² + σ_u²). Solving, β = σ_u/(σ_v√N),
    λ = σ_v√N/((N + 1)σ_u). Each insider's profit E[x_n(v − p)] = βσ_v²(1 − λNβ) = σ_uσ_v/((N + 1)√N), and
    Var(v | y) = σ_v²(1 − λNβ) = σ_v²/(N + 1).

## Data and reproducibility

* Federal Reserve Board: the meeting pages `fomchistorical{1994–2020}.htm` and `fomccalendars.htm`, every statement
  and minutes page they link; the text extracted (statements: policy paragraphs before the vote; minutes: discussion
  paragraphs), cached and checked by SHA-256 in `videos/quant/data/manifest.json`. 234 statements (1997–2025), 239
  minutes (1996–2025).
* FRED: DGS2 and DGS10, daily, 1996–2025, frozen and checked.
* Loughran–McDonald master dictionary, 1993–2025 edition (sraf.nd.edu); free for academic use; cached locally, not
  redistributed.
* Registered: `sestm_fomc_drift_part28` (13 trials); the counter goes from 10,455 to 10,468; the hold-out
  (`fred/dgs2_fomc_5day_drift`) sealed and opened once.
* Quoted, not computed: Tetlock's, Loughran–McDonald's, Ke–Kelly–Xiu's, Bybee et al.'s, Hansen–McMahon–Prat's,
  Lopez-Lira–Tang's, Kim–Muhn–Nikolaev's, Glasserman–Lin's, Sarkar–Vafa's, He et al.'s, Katona et al.'s, BloombergGPT's
  and Li et al.'s results; FinBERT's corpus size.
* Simulated or illustrative: the attention weights in Chapter 9; the SESTM worlds of the research chapter; Kyle's market
  and the adoption curve.
* Running external models (FinBERT, open-weight LLMs) was not part of this build; the language models here are the
  House's own pocket models, trained from scratch on the minutes.

---

# 量化金融，从零搭建 — 第28部分：文本、大语言模型与另类数据

本系列共四十三部分，这是第四幕"收益溢价"（第23–29部分）的第六部分，按本系列的博士层次标准构建。第27部分让实证资产定价的每一种学习器都经受第26部分的检验；本部分把它们用在文字上。语料是联邦公开市场委员会（FOMC）三十年来自己发布的文件，对照债券市场的反应来读。

*这是方法的教育，不是投资建议。*

## 章节（约55分钟）

* **开篇：一句话。** 2008年1月22日（会议间降息75个基点）的声明与2007年12月11日的声明逐词对比；两年期收益率下跌28个基点，是1997–2020年声明日最大的波动（典型值7.2个基点）；从General Inquirer到时间一致的大语言模型的历史；本部分的计划；本系列公司的阅览室。
* **1. 把文字变成数字。** 词袋；文档-词项矩阵：到2020年为止193份声明和199份会议纪要，132万词，10,253个不同的词；齐普夫斜率−0.98；希普斯定律（1996年2,626个不同的词，到2020年10,220个）；tf-idf。
* **2. 词典。** Tetlock（2007）；Loughran–McDonald（2011）：10-K中哈佛词表负面词计数的73.8%在金融语境里并不负面；如今的词表（2,355个负面词、354个正面词、297个不确定词）；声明中各类词的占比随时间变化；错配：被计数最多的负面词是*unemployment*，最多的正面词是*stability*。
* **3. 语气与两年期收益率。** 反应的度量（两年期，收盘到收盘）；运行`tone`的实验；对净语气回归：t = 0.33（语气变化−0.22，负面占比−0.74，不确定−0.16）；Kuttner（2001）；Gürkaynak、Sack与Swanson（2005）：路径因子。
* **4. 长度、可读性与前瞻指引。** 2002年前中位数153词，2016年以来408词；迷雾指数21.0与22.8（Loughran与McDonald 2014论可读性）；每份声明相对上一份改变了多少（中位数1 − cos = 0.13；与波动大小的秩相关0.31，p ≈ 1e-5；改动最少的四分之一平均3.4个基点，最多的7.8个基点）；前瞻指引用语，从*likely to be measured*（2004）到*ongoing increases*（2022）。
* **5. 有监督的词：SESTM。** Ke、Kelly与修大成（道琼斯新闻专线1989–2017，2250万篇文章；等权夏普比率4.29（未扣成本），市值加权1.33）；模型；在到2012年的声明上做筛选（α = 0.20、κ = 10，在2007–2012年上选出；704个词中11个鹰派、25个鸽派）；两个主题；本系列公司的筛选代码；样本内秩相关0.51，2013–2020年0.06（p = 0.64）。
* **6. 主题。** NMF与LDA；实验（`nmf_topics`，误差0.89 → 0.75）；八个主题，按其词命名；会议纪要的时代之河；Bybee、Kelly、Manela与修大成（2024）。
* **7. FOMC内部。** 委员会发布哪些文件；Hansen、McMahon与Prat（2018）；纪律与从众（Meade与Stasavage 2008）；三周规则（2005年1月）前后纪要的长度。
* **8. 词嵌入。** Firth；PPMI与SVD，Levy与Goldberg（2014）；近邻（inflation：expectations、core；tightening：easing；liquidity：facilities、swap lines）；一张图；tightening − raise + lower = easing。
* **9. Transformer与FinBERT。** 注意力；Huang、Wang与Yang（2023）；袖珍模型（4层，d = 160，190万参数，BPE 2,048，训练400万词元）；训练回放。
* **10. 大语言模型读新闻。** Lopez-Lira–Tang的提示词；他们的结果（134,129条标题，2021年10月–2023年12月，在GPT-4训练截止之后；GPT-1、GPT-2和BERT做不到）；Chen、Kelly与修大成（2022）；Kim、Muhn与Nikolaev（2024：52%与60%）；三个问题。
* **11. 前视偏差。** 训练数据里的回测；技能 + 前视 − 分心；Glasserman与Lin（2023）；Sarkar与Vafa（2024）；He、Lv、Manela与Wu（2025）。
* **12. 按时间切片的实验。** 模型A（到2007年的纪要）、B（到2020年）、C（到2007年以及2013–2020年）；在2008–12年纪要上的每字符比特：A 1.15，C 0.86，B 0.71；在2008年前留出的纪要上A最好（0.77对0.80）；逐年的声明（2008年后A从0.59跳到1.23）；探针（*0 to 1/4 percent*：A 0.1%，C 52%，B 70%；*effective lower bound*：A约为0，C 83%；*forward guidance*：A约为0，C 96%）；样本文本；前视的两层。
* **13. 大语言模型交易智能体。** ReAct循环；TradingAgents（Xiao、Sun、Luo与Wang 2024）；四项检查。
* **14. 另类数据。** 清单；Katona、Painter、Patatoukas与Zeng（2025）；有N个知情者的Kyle模型（每人利润 ∝ N^−3/2，信息含量N/(N+1)），并作模拟；一条程式化的采用曲线。
* **15. 领域模型与文本交易台。** BloombergGPT（500亿参数；3630亿金融词元与3450亿通用词元）；对数尺度上的训练规模；Li等（2023）；业界如何使用文本。
* **16. 文本信号，登记并打开。** 用到2020年的声明拟合SESTM → 两年期国债五日头寸；13次试验；研究期夏普比率−0.04；2021–2025年：41份声明，每笔+2.1个基点，夏普比率0.31 ± 0.52（扣成本后0.13），命中率49%；PSR(0) = 0.72；达到95%约需330份声明；解读；计数器10,468。
* **17. 第28条规则：文本特征。** 第一张表；实验（`point_in_time_vocab`、`first_use`）；模块；第28条规则；三个案例。
* **写给研究者：筛选为什么能找到那些词。** 引理（f_j → E[g q_j]/E[q_j]；中性词的极限为π；由切比雪夫关联不等式，情感词在π之上或之下），并给出证明；Ke、Kelly与修大成的定理C.2；在20,000篇模拟文章上检验极限（正面0.581对0.581，负面0.422对0.419，中性0.502对0.500）；按n、θ与文章长度的恢复率，逐词阈值z = √(2 log m)；声明上：保留36个词，打乱标签时平均21个（p = 0.09），用z筛选则一个也没有；三个开放问题。
* **回顾、交易台问题与习题。** 十四行回顾；六个交易台问题；十二道习题（两道为资格考试难度），解答见下文。

## 写给研究者

* **定理。** Ke、Kelly与修大成（2019）的定理C.1–C.5（筛选、主题估计、打分）；切比雪夫关联（重排）不等式；Kyle（1985）与Admati和Pfleiderer（1988）的N个对称知情者情形。
* **简化。** 用声明日收盘到收盘的波动作标签（Gürkaynak、Sack与Swanson用的是日内期货窗口）；单边筛选以样本自身的正向占比π为中心（论文以½为中心）；用NMF代替LDA；190万参数的袖珍模型；Kyle模型的采用曲线是程式化的。
* **开放问题。** 文档相关时的筛选；短语与上下文特征的代价是log²m；把大语料的先验与小样本标注结合起来，并给出保证。

## 交易台问题与解答

1. **在2015–2020年新闻上夏普比率为4的LLM信号。** 先查模型的训练截止日期：如果它读过这段时期，回测可能就是记忆（第12章量化了有多少）。然后匿名化公司标识重跑（Glasserman–Lin）；再用2015年之前的模型（He、Lv、Manela与Wu）。
2. **语气从前一日收盘起解释了声明日30%的波动。** 波动发生在发布后几分钟内；从前一日收盘起的回归是在解释，而不是预测。应从发布之后开始度量，或预测更晚的窗口（第16章就是这样做的：到收盘时什么也不剩）。
3. **`unemployment`是被计数最多的负面词。** 对央行来说它是职责中的词；去掉职责用词，或者从结果中学习权重（SESTM），并检验学到的词表能否胜过偶然。
4. **113份文档里保留了36个词。** 打乱标签再筛选：平均21个，p ≈ 0.09；用逐词z阈值，一个也留不下（研究章）。
5. **买家每年翻倍的数据集。** 每个买家的利润 ∝ N^−3/2：N翻倍使之每年除以2^1.5 ≈ 2.8；实时度量衰减，要么早买，要么不买。
6. **通用LLM在2024年数据上胜过你微调过的FinBERT。** 用测试期之前的模型、固定版本，并计入成本；在狭窄的标注任务上专用模型仍然占优（Li等 2023）。

## 习题与解答

1. **tf-idf与长度。** 计数翻倍时tf的分子分母同时翻倍：tf不变，所以该行及其与任何其他行的余弦都不变。
2. **齐普夫的头部。** 频率 ∝ 1/r时，前k个词覆盖H_k/H_V ≈ (ln k + 0.577)/(ln V + 0.577) = 5.18/9.79 ≈ 53%。
3. **净语气。** (3 − 6)/300 = −1.0%；去掉两个`unemployment`后为(3 − 4)/300 = −0.33%。
4. **偶然通过筛选。** f_j = X/10，X ~ Bin(10, ½)；|f − ½| ≥ 0.2 ⇔ X ≤ 3或X ≥ 7，概率2 × 0.172 = 0.344：300个词中约103个通过。
5. **SESTM的惩罚项。** λ log p(1 − p) = log[p^λ(1 − p)^λ]，相差一个常数即为Beta(λ + 1, λ + 1)的对数密度；惩罚极大似然就是该先验下的最大后验。
6. **PMI。** P(w, c) = P(w)P(c)时为log 1 = 0；负的PMI需要比偶然更稀少的词对，小计数对它估计很差，所以PPMI将其置零。
7. **迷雾指数。** 14个词，1个句子；三个及以上音节的词：*Committee*、*decided*、*federal*（*unchanged*是两个音节），所以14个中3个 = 21.4%：迷雾指数 = 0.4 (14 + 21.4) ≈ 14.2。
8. **每字符比特。** 3.5 / ln 2 / 4.2 ≈ 1.20。
9. **Glasserman–Lin。** 带名称减去匿名 = 前视 − 分心 = 1.2 − 1.5 = −0.3：样本内分心大于前视；样本外两者都是0.8，所以样本内的差距不是技能。
10. **有N个知情者的Kyle模型。** 每人利润 ∝ 1/((N + 1)√N)：从4到9，(5 × 2)/(10 × 3) = 1/3；总利润 ∝ √N/(N + 1)：(3/10)/(2/5) = 0.75。
11. **（资格考试）关联与筛选。** 取p、p′独立同分布，Cov(g(p), q(p)) = ½E[(g(p) − g(p′))(q(p) − q(p′))] ≥ 0，因为两者都递增。在SESTM的模型中，由大数定律f_j → Pr(y > 0 | j在文章中) = E[g q_j]/E[q_j]，其中q_j(p) = 1 − (1 − pO+_j − (1 − p)O−_j)^s。j ∈ N时q_j为常数，f_j → E g = π；O+_j > O−_j时q_j递增，极限为π + Cov(g, q_j)/E q_j > π（两者都严格递增时为严格不等式）；O+_j < O−_j时在π之下。
12. **（资格考试）有N个知情者的Kyle模型。** 猜测x_n = β(v − p₀)，p = p₀ + λ(Σx_n + u)。知情者n最大化E[(v − p)x_n | v] = x_n(v − λx_n − λ(N − 1)βv)（取p₀ = 0）：x_n = (1 − λ(N − 1)β)v/(2λ)，所以β = 1/(λ(N + 1))。市场有效：λ = Cov(v, y)/Var(y)，y = Nβv + u：λ = Nβσ_v²/(N²β²σ_v² + σ_u²)。解得β = σ_u/(σ_v√N)，λ = σ_v√N/((N + 1)σ_u)。每个知情者的利润E[x_n(v − p)] = βσ_v²(1 − λNβ) = σ_uσ_v/((N + 1)√N)，且Var(v | y) = σ_v²(1 − λNβ) = σ_v²/(N + 1)。

## 数据与复现

* 美联储理事会：会议页面`fomchistorical{1994–2020}.htm`和`fomccalendars.htm`及其链接的每份声明和纪要页面；抽取出的文本（声明：投票之前的政策段落；纪要：讨论段落）已缓存，并在`videos/quant/data/manifest.json`中用SHA-256校验。234份声明（1997–2025），239份纪要（1996–2025）。
* FRED：DGS2与DGS10，日度，1996–2025，已冻结并校验。
* Loughran–McDonald主词典，1993–2025版（sraf.nd.edu）；学术用途免费；仅在本地缓存，不再分发。
* 本部分登记：`sestm_fomc_drift_part28`（13次试验）；计数器从10,455升到10,468；样本外数据（`fred/dgs2_fomc_5day_drift`）已封存并只打开一次。
* 引用而非计算的结果：Tetlock、Loughran–McDonald、Ke–Kelly–修大成、Bybee等、Hansen–McMahon–Prat、Lopez-Lira–Tang、Kim–Muhn–Nikolaev、Glasserman–Lin、Sarkar–Vafa、He等、Katona等、BloombergGPT以及Li等的结果；FinBERT的语料规模。
* 模拟或示意：第9章的注意力权重；研究章中的SESTM世界；Kyle市场与采用曲线。
* 本次构建没有运行外部模型（FinBERT、开放权重的大语言模型）；这里的语言模型是本系列公司自己的袖珍模型，在纪要上从零训练。
