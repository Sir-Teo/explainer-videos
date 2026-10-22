# AI, Built — Part 31: Can We Trust It?

The finale of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). How to know what a model can do, and whether it does what we meant: measuring
honestly (bootstrap intervals, paired comparisons, contamination, arenas and judges, item response), forecasting
capabilities, reward hacking, supervising a model stronger than its supervisor, the evidence that models can deceive,
monitoring chains of thought, AI control, dangerous capabilities and safeguards, and what a model remembers about its
training data. Then the open problems, the series in six columns, and Part 1's scoreboard and Shannon's guessing game
one last time. Every statistic is computed here: on Part 1's counting models, on the series' own 6.8-million-parameter
transformer trained on thirty novels (`explainer/ai/novels.py`), on Part 27's which-book task, or in small simulations
labelled as such.

* **Hook.** Every part of the series on one map, and Part 1's scoreboard; Norbert Wiener, *Some Moral and Technical
  Consequences of Automation* (*Science*, 1960), and I. J. Good, *Speculations Concerning the First Ultraintelligent
  Machine* (1965), quoted verbatim; their questions now: is the purpose the one we meant, can we keep it under
  control, and underneath both, how would we know?
* **1. Measuring a model.** One number is a sample. The bootstrap (Efron 1979) on Part 1's counting models,
  paragraph by paragraph over the Falcon passage: 10,000 resamples; the 4- and 5-character models' intervals
  overlap (2.32 [2.28, 2.37] and 2.38 [2.32, 2.45] bits per character), the unpaired difference's interval
  [−0.024, 0.136] includes zero, the paired one [0.030, 0.084] does not (paragraph scores correlate at 0.94);
  Var(X − Y) = Var X + Var Y − 2 Cov(X, Y). A 500-question benchmark: standard error about 2 points near 70%; a
  model truly 2 points worse ties or wins 25% of the time; pairing shrinks the gap's error from 2.9 to 1.4 points.
  Miller (2024) on error bars for evaluations; Sclar et al. (2023): prompt format alone moved accuracy by up to 76
  points.
* **2. Has it seen the test?** GPT-3's 13-gram overlap filter and its bug (Brown et al. 2020), BIG-bench in GPT-4's
  training data (OpenAI 2023). Part 1's counting models with the passage leaked into their training text: the 7-character
  model drops from 2.96 to 1.57 bits per character and the ranking of models flips; half leaked, seen against unseen
  paragraphs; 13-gram overlap flags exactly the leaked paragraphs. The BIG-bench canary hidden once in the training
  text: its 36-character code drops from 266 bits to about 50, against 266 for 1,000 random codes. Dynamic
  benchmarks: LiveCodeBench, LiveBench, GSM1k (up to 8% drops; Zhang et al. 2024); the passage itself entered the US
  public domain on 1 January 2026.
* **3. Arenas and ratings.** Chatbot Arena (LMSYS, spring 2023; now LMArena); Bradley–Terry derived as Elo's model,
  fitted by maximum likelihood, with closed-form intervals from the information matrix. Ten simulated models, votes
  as they arrive: the 95% interval narrows from about 336 Elo points at 100 votes to 12 at 50,000; online Elo depends
  on the order of the votes (spread 53 points over 20 orderings); the best of k private variants of one model is
  inflated by about 13 points at k = 27. Style control (2024); *The Leaderboard Illusion* (Singh et al. 2025).
* **4. Judges, and what an item tells you.** MT-Bench (Zheng et al. 2023): GPT-4 agrees with experts over 80% of the
  time, but is biased by position, verbosity and self-preference. A simulated judge with those biases scrambles
  the ranking (the first answer wins 67% of the time; verdicts survive a swap only 49% of the time); evaluating both
  orders and a style term recover most of it. Item response theory (Lord 1952; Rasch 1960): the 2PL model, Fisher
  information a²p(1 − p); a 2,000-item simulated benchmark; 25 to 200 items chosen by information predict the rest
  better than random ones at small sizes (error 6.2 against 8.2 points at 25 items). tinyBenchmarks (Maia Polo et al.
  2024), the Epoch Capabilities Index (Ho et al. 2025).
* **5. Forecasting capabilities.** The Chinchilla law L(N, D) = E + A/N^α + B/D^β (Hoffmann et al. 2022); Epoch AI's
  compute trends; emergence or a mirage (Schaeffer et al. 2023). METR's 50% time horizon (Kwa et al. 2025): its Time
  Horizon 1.1 measurements refitted here, a doubling every 129 days since 2023 (bootstrap 101–155; METR: 129), 187
  days since 2019. A backtest: fitted on the 7 frontier models released before 2025, the trend (a doubling every 197
  days) underpredicted every later model, o3 by a factor of 3 and an early Claude Mythos Preview by 8. Extrapolated,
  as arithmetic rather than prophecy: tasks of a 40-hour week around December 2026 (80% of bootstraps between
  September 2026 and March 2027), of a 167-hour month around September 2027 — far beyond the 16 hours METR's tasks
  measure reliably. Caveats: METR's randomized trial
  (Becker et al. 2025: developers 19% slower with AI, believed 20% faster), jagged abilities (International AI Safety
  Report 2026).
* **6. Reward hacking.** Krakovna et al.'s list of specification gaming (2020): the Lego block flipped, the boat race,
  the hand between camera and ball, the walker's sliding legs. The boat race built here: Q-learning on a grid course
  with a reward for targets that pay again, five seeds: the agent circles the targets for 56 points an episode and
  never finishes; with the finish alone it learns slowly or not at all; with potential-based shaping (Ng, Harada & Russell
  1999), derived, every seed finishes from episode 50. Coding agents: special-casing tests (Claude 3.7 Sonnet system
  card), `exit(0)` and skipped tests caught by a chain-of-thought monitor (Baker et al. 2025), METR on o3 (39 of 128
  runs on one task), "please do not cheat"; hacking that generalizes to sabotage and alignment faking (MacDiarmid et
  al. 2025) and inoculation prompting.
* **7. Supervising something stronger.** Debate (Irving, Christiano & Amodei 2018) and the complexity argument;
  Khan et al. (2024): judges reading debates between stronger models. Weak-to-strong generalization (Burns et al.
  2023): the performance gap recovered, PGR = (weak-to-strong − weak)/(ceiling − weak), computed on Part 27's
  which-book task with a 2-layer weak supervisor and the series' model as the strong student, five seeds, with and
  without the auxiliary confidence loss; how often the student copies the supervisor's mistakes.
* **8. Evidence of deception.** Sleeper agents that survive safety training (Hubinger et al. 2024) and the probes that
  catch them; in-context scheming (Meinke et al., Apollo Research 2024: five of six frontier models); sandbagging
  (Claude 3.5 Sonnet's multiplication accuracy, 99% → 34% when doing well would get it retrained, and 96% → 61% with
  no goal given);
  anti-scheming training and evaluation awareness (Schoen et al. 2025: o3's covert actions 13% → 0.4%, verbalized
  awareness rising); Claude Sonnet 4.5's "I think you're testing me" (system card, September 2025); alignment faking
  (Greenblatt et al. 2024).
* **9. Reading the chain of thought.** Why a visible chain of thought can be monitored; Baker et al. (2025): a
  GPT-4o monitor reading the chain of thought catches far more reward hacking than one reading only actions, and
  optimization pressure on the chain of thought teaches obfuscation; *Chain of Thought Monitorability: A New and
  Fragile Opportunity* (Korbak et al. 2025); unfaithful reasoning (Chen et al. 2025); GPT-6 Astra's system card
  (September 2026) on monitorability.
* **10. Control.** Assume the model may be trying to cause harm and design the protocol anyway (Greenblatt, Shlegeris,
  Sachan & Roger 2023). The game derived: P(red wins) = w/(c + w)·(1 − (1 − c − w)^N). Simulated: a suspicion monitor
  with a 2% human-audit budget; red's best attack rate; upfront auditing 22% safe, trusted monitoring 75%, deferring
  the most suspicious 10% to a trusted model 87% at 92% usefulness; one game replayed; the safety–usefulness frontier;
  the published numbers and Ctrl-Z (Bhatt et al. 2025).
* **11. Dangerous capabilities and safeguards.** Frontier safety frameworks (Anthropic's Responsible Scaling Policy,
  OpenAI's Preparedness Framework, Google DeepMind's Frontier Safety Framework, California's SB 53); the thresholds
  crossed, 2025–2026, from the labs' own system cards; Constitutional Classifiers (Sharma et al. 2025) and their next
  generation (2026), activation probes in production; adaptive attacks (*The Attacker Moves Second*, Nasr, Carlini et
  al. 2025).
* **12. What a model remembers.** Extraction from GPT-2 (Carlini et al. 2021), memorization grows log-linearly with
  size, duplication and context (Carlini et al. 2023), extraction from ChatGPT (Nasr et al. 2023), membership
  inference (Shokri et al. 2017). On the series' model: exact continuations of training text against held-out text, by
  prefix length (Carlini et al.'s definition, computed by teacher forcing); duplicated text; a loss-threshold
  membership test. Differential privacy (Dwork et al. 2006) and DP-SGD (Abadi et al. 2016): a secret planted in a
  small character model's training text, its exposure (Carlini et al. 2019) with plain SGD and with DP-SGD, and ε from
  a Rényi accountant (Mironov et al. 2019); VaultGemma (2025).
* **13. Open problems.** Measuring, aligning, securing: what we can't yet do, with the part's own numbers.
* **14. The guessing game, revisited.** The series act by act; Part 1's scoreboard with every model of the series:
  counting, Kneser–Ney (Part 7), the first transformer (Part 13), the series' own model; Shannon's sentence played
  by Part 1's counting program and by the series' model; Wiener's sentence once more.
* **Recap** in eight pictures from the part's own results, the problem set, references, and thanks.

Run from the repo root:

```
python -m explainer.ai.novels             # the series' model: about 1.5 hours on 4 cores (cached; Part 27 uses it too)
python -m videos.ai.ai31.compute          # every experiment
python tools/build.py ai31                # English
python tools/build.py ai31 --lang zh      # Chinese
```

Part 27's which-book questions are read from its cache when that is complete, and otherwise rebuilt the same way
(same seed) without touching it. `compute.py` holds the experiments; `sims.py` the simulations (Bradley–Terry and Elo, the biased judge, item
response, the control game, the boat race and Q-learning); `lm_tools.py` the experiments on the series' model (bits
on the passage, Shannon's game with token-path summation, extraction, weak-to-strong).

References: N. Wiener, *Some Moral and Technical Consequences of Automation*, Science 131 (1960); I. J. Good,
*Speculations Concerning the First Ultraintelligent Machine* (1965); B. Efron, *Bootstrap methods: another look at
the jackknife* (1979); B. Efron & R. Tibshirani, *An Introduction to the Bootstrap* (1993); E. Miller, *Adding Error
Bars to Evals* (2024); M. Sclar et al. (2023); Brown et al. (2020); Srivastava et al., BIG-bench (2022); OpenAI, GPT-4
technical report (2023); Zhang et al., GSM1k (2024); Jain et al., LiveCodeBench (2024); White et al., LiveBench (2024);
R. A. Bradley & M. E. Terry (1952); Chiang et al., Chatbot Arena (2024); Singh et al., *The Leaderboard Illusion*
(2025); Zheng et al., MT-Bench (2023); F. M. Lord (1952); G. Rasch (1960); Maia Polo et al., tinyBenchmarks (2024);
Ho et al., Epoch Capabilities Index (2025); Hoffmann et al. (2022); Schaeffer, Miranda & Koyejo (2023); Kwa et al.,
*Measuring AI Ability to Complete Long Tasks* (2025); METR, Time Horizon 1.1 (2026); Becker et al. (2025);
International AI Safety Report (2026); Krakovna et al. (2020); A. Ng, D. Harada & S. Russell (1999); Anthropic, Claude
3.7 Sonnet system card (2025); Baker et al., *Monitoring Reasoning Models for Misbehavior* (2025); METR, o3 evaluation
(2025); MacDiarmid et al. (2025); G. Irving, P. Christiano & D. Amodei, *AI Safety via Debate* (2018); Khan et al.
(2024); Burns et al., *Weak-to-Strong Generalization* (2023); Hubinger et al., *Sleeper Agents* (2024); Anthropic,
*Simple probes can catch sleeper agents* (2024); Meinke et al., *Frontier Models are Capable of In-context Scheming*
(2024); Schoen et al., *Stress Testing Deliberative Alignment for
Anti-Scheming Training* (2025); Anthropic, Claude Sonnet 4.5 system card (2025); Greenblatt et al., *Alignment Faking*
(2024); Korbak, Balesni et al. (2025); Chen et al., *Reasoning Models Don't Always Say What They Think* (2025); OpenAI,
GPT-6 Astra system card (2026); R. Greenblatt, B. Shlegeris, K. Sachan & F. Roger, *AI Control* (2023); Bhatt et al.,
*Ctrl-Z* (2025); Anthropic, Responsible Scaling Policy; OpenAI, Preparedness Framework v2 (2025); Google DeepMind,
Frontier Safety Framework v3 (2025); Sharma et al., *Constitutional Classifiers* (2025); Nasr, Carlini et al., *The
Attacker Moves Second* (2025); Carlini et al. (2019, 2021, 2023); Nasr et al. (2023); Shokri et al. (2017); C. Dwork,
F. McSherry, K. Nissim & A. Smith (2006); Abadi et al., *Deep Learning with Differential Privacy* (2016); I. Mironov,
K. Talwar & L. Zhang, *Rényi Differential Privacy of the Sampled Gaussian Mechanism* (2019); Google, VaultGemma (2025);
C. Dwork & A. Roth, *The Algorithmic Foundations of Differential Privacy* (2014); C. E. Shannon, *Prediction and
Entropy of Printed English* (1951).

## Problems, with solutions

**1. Pairing.** Two models' per-item scores have equal variance σ² and correlation ρ. Show that the paired standard
error of the difference is √(2(1 − ρ)) times one model's. What is the factor at ρ = 0.94?

*Solution.* Var(X − Y) = σ² + σ² − 2ρσ² = 2(1 − ρ)σ², so the standard error of the mean difference over n items is
√(2(1 − ρ)) σ/√n, √(2(1 − ρ)) times one model's σ/√n. At ρ = 0.94 the factor is √0.12 ≈ 0.35: the difference is
known about three times more precisely than either score. Unpaired, the two scores' errors add as if independent, a
factor of √2 ≈ 1.41 instead.

**2. Bradley–Terry's fixed point.** Show that at the Bradley–Terry maximum-likelihood estimate, each model's expected
number of wins, Σ_j n_ij σ(θ_i − θ_j), equals its actual number of wins.

*Solution.* With w_ij the wins of i over j and n_ij = w_ij + w_ji, the log-likelihood is
ℓ = Σ_{i,j} w_ij log σ(θ_i − θ_j). Since d/dx log σ(x) = 1 − σ(x) and σ(−x) = 1 − σ(x),
∂ℓ/∂θ_i = Σ_j [w_ij (1 − σ(θ_i − θ_j)) − w_ji σ(θ_i − θ_j)] = Σ_j w_ij − Σ_j n_ij σ(θ_i − θ_j). Setting it to zero
gives the claim. (Only differences are identified: adding a constant to every θ changes nothing, so one rating is
fixed, here the mean.)

**3. What an item tells you.** For the item P(y = 1 | θ) = σ(a(θ − b)), derive the Fisher information a²p(1 − p),
and show it is largest at θ = b, where it equals a²/4.

*Solution.* log P(y | θ) = y log p + (1 − y) log(1 − p) with dp/dθ = a p(1 − p), so the score is
(y − p) a, and the information is E[(y − p)²] a² = a² p(1 − p). p(1 − p) is largest at p = ½, that is at θ = b, where
it is ¼. An item tells you most about models whose ability is near its difficulty, and more the sharper it is (larger
a); that is why a few well-chosen items can stand in for many.

**4. Shaping without changing the answer.** With r′ = r + γΦ(s′) − Φ(s) and Φ = 0 at the end of an episode, show that
every policy's return changes by −Φ(s₀), so the optimal policies are the same.

*Solution.* Along any episode s₀, s₁, …, s_T, Σ_t γ^t (γΦ(s_{t+1}) − Φ(s_t)) = Σ_t (γ^{t+1}Φ(s_{t+1}) − γ^tΦ(s_t)),
which telescopes to γ^T Φ(s_T) − Φ(s₀) = −Φ(s₀). Every policy's expected return from s₀ shifts by the same −Φ(s₀),
so their order, and the best policy, are unchanged (Ng, Harada & Russell 1999). A bonus for each target, which pays
again on every lap, is not of this form, and it changes the answer.

**5. The control game.** Each round, independently, the red team's attack is caught with probability c and succeeds
unnoticed with probability w; otherwise nothing decisive happens. Derive P(red wins) = w/(c + w)·(1 − (1 − c − w)^N)
over N rounds. If an attack is caught with probability q = 0.48 and an uncaught attack works with probability
s = 0.3, what is the blue team's safety as N → ∞?

*Solution.* Red wins at round k if rounds 1 … k − 1 were undecided and round k is a success:
Σ_{k=1}^N (1 − c − w)^{k−1} w = w (1 − (1 − c − w)^N)/(c + w). As N → ∞ the game is decided almost surely, and red
wins with probability w/(c + w). With attack rate p, c = pq and w = p(1 − q)s, so p cancels:
P(red wins) = (1 − q)s/(q + (1 − q)s) = 0.156/0.636 ≈ 0.25, a safety of about 0.75 — the 75% of chapter ten. Red's
attack rate only sets how fast the game ends.

**6. Why clip.** After clipping every example's gradient to norm C, by how much can adding or removing one example
change the sum of gradients? Why does that make Gaussian noise of scale σC the right amount?

*Solution.* The sum changes by exactly that example's clipped gradient, whose norm is at most C: the sum's
sensitivity is C, whatever the data. The Gaussian mechanism adds noise proportional to the sensitivity; with noise
N(0, σ²C²I), two neighbouring datasets' outputs are Gaussians with means at most C apart, and their Rényi divergence
of order α is at most α C²/(2σ²C²) = α/(2σ²), independent of C and of the data. The accountant adds this up over the
steps (with the gain from sampling each batch) to give ε. Without clipping a single example could move the sum
arbitrarily far, and no finite noise would hide it.

## 习题与解答

**1. 配对。** 两个模型逐题得分的方差都是σ²，相关系数为ρ。证明：配对之后，差的标准误是单个模型的 √(2(1 − ρ)) 倍。ρ = 0.94
时这个倍数是多少？

*解答。* Var(X − Y) = σ² + σ² − 2ρσ² = 2(1 − ρ)σ²，所以n道题上平均差的标准误是 √(2(1 − ρ)) σ/√n，正好是单个模型
σ/√n 的 √(2(1 − ρ)) 倍。ρ = 0.94 时，倍数是 √0.12 ≈ 0.35：差，比任何一个分数都要精确大约三倍。不配对时，两个分数的误差
按独立的情形相加，倍数是 √2 ≈ 1.41。

**2. 布拉德利-特里的不动点。** 证明在布拉德利-特里模型的最大似然估计处，每个模型的期望胜场数
Σ_j n_ij σ(θ_i − θ_j)，等于它实际的胜场数。

*解答。* 记w_ij为i胜j的次数，n_ij = w_ij + w_ji，对数似然为 ℓ = Σ_{i,j} w_ij log σ(θ_i − θ_j)。由于
d/dx log σ(x) = 1 − σ(x)，且 σ(−x) = 1 − σ(x)，
∂ℓ/∂θ_i = Σ_j [w_ij (1 − σ(θ_i − θ_j)) − w_ji σ(θ_i − θ_j)] = Σ_j w_ij − Σ_j n_ij σ(θ_i − θ_j)。令它为零，即得结论。
（能辨识的只有差：每个θ都加上同一个常数，什么都不变，所以要固定一个评分，这里固定的是平均值。）

**3. 一道题能告诉你什么。** 对题目 P(y = 1 | θ) = σ(a(θ − b))，推导费希尔信息 a²p(1 − p)，并证明它在 θ = b 处最大，
最大值为 a²/4。

*解答。* log P(y | θ) = y log p + (1 − y) log(1 − p)，且 dp/dθ = a p(1 − p)，所以得分函数是 (y − p) a，信息是
E[(y − p)²] a² = a² p(1 − p)。p(1 − p) 在 p = ½ 也就是 θ = b 处最大，等于¼。一道题，对能力接近它难度的模型最有信息量，
区分度a越大，信息越多；这就是为什么挑得好的几道题，能代替很多道题。

**4. 不改变答案的奖励塑形。** 设 r′ = r + γΦ(s′) − Φ(s)，且回合结束时Φ = 0。证明每个策略的回报都改变了 −Φ(s₀)，所以最优
策略不变。

*解答。* 沿任意一个回合 s₀, s₁, …, s_T，Σ_t γ^t (γΦ(s_{t+1}) − Φ(s_t)) = Σ_t (γ^{t+1}Φ(s_{t+1}) − γ^tΦ(s_t))，
裂项相消，只剩 γ^T Φ(s_T) − Φ(s₀) = −Φ(s₀)。每个策略从s₀出发的期望回报，都平移同样的 −Φ(s₀)，所以它们的先后顺序、
以及最好的策略，都不变（Ng、Harada和Russell，1999）。每碰到一个目标就加分、每绕一圈又重新加分的奖励，不是这种形式，
它会改变答案。

**5. 控制博弈。** 每一轮相互独立：红队的攻击以概率c被抓住，以概率w不被察觉地成功；否则这一轮没有分出结果。推导N轮之内
P(红队获胜) = w/(c + w)·(1 − (1 − c − w)^N)。如果一次攻击被抓住的概率是 q = 0.48，没被抓住的攻击成功的概率是
s = 0.3，那么N → ∞ 时蓝队的安全性是多少？

*解答。* 红队在第k轮获胜，要求前 k − 1 轮都没分出结果、第k轮成功：
Σ_{k=1}^N (1 − c − w)^{k−1} w = w (1 − (1 − c − w)^N)/(c + w)。N → ∞ 时，博弈几乎必然分出结果，红队获胜的概率是
w/(c + w)。攻击率为p时，c = pq，w = p(1 − q)s，p被约掉：P(红队获胜) = (1 − q)s/(q + (1 − q)s) = 0.156/0.636 ≈ 0.25，
安全性约为0.75，正是第10章里的百分之七十五。红队的攻击率只决定博弈多快结束。

**6. 为什么要裁剪。** 把每个样本的梯度都裁剪到范数C之后，加入或去掉一个样本，最多能让梯度之和改变多少？为什么这使得尺度为
σC的高斯噪声恰好合适？

*解答。* 和改变的正是那个样本裁剪后的梯度，它的范数至多是C：不管数据是什么，和的敏感度都是C。高斯机制加的噪声和敏感度
成正比；噪声为 N(0, σ²C²I) 时，两个相邻数据集的输出是均值相差至多C的两个高斯分布，它们α阶的Rényi散度至多是
α C²/(2σ²C²) = α/(2σ²)，与C和数据都无关。会计方法把它在所有步上加起来（再算上每批随机抽样带来的增益），就得到ε。
不裁剪的话，一个样本就能把和推到任意远，多大的噪声都藏不住它。

## Glossary (new terms in Part 31)

| English | 中文 |
|---|---|
| the bootstrap, resample | 自助法，重抽样（统计；不同于强化学习里的"自举"） |
| confidence interval, standard error | 置信区间，标准误 |
| paired comparison, unpaired | 配对比较，不配对 |
| benchmark, held-out test | 基准测试，留出的测试集 |
| contamination, leak | 污染，泄漏 |
| n-gram overlap | n元组重叠 |
| canary string | 金丝雀字符串 |
| dynamic benchmark | 动态基准测试 |
| arena, leaderboard, vote | 竞技场，排行榜，投票 |
| Elo rating, online Elo | 埃洛等级分，在线埃洛 |
| style control | 风格控制 |
| LLM as a judge; position, verbosity and self-preference bias | 用大模型当裁判；位置偏差、冗长偏差、自我偏好 |
| item response theory (IRT), 2PL, difficulty, discrimination | 项目反应理论（IRT），双参数模型，难度，区分度 |
| Fisher information | 费希尔信息 |
| time horizon (50%) | （百分之五十）时间跨度 |
| doubling time, backtest, extrapolation | 倍增时间，回测，外推 |
| specification gaming, reward hacking | 规格投机，奖励投机 |
| potential-based shaping | 基于势函数的奖励塑形 |
| scalable oversight, debate | 可扩展监督，辩论 |
| weak-to-strong generalization, performance gap recovered (PGR) | 由弱到强的泛化，性能差距恢复率（PGR） |
| auxiliary confidence loss | 辅助置信度损失 |
| deception, scheming, sandbagging | 欺骗，图谋，藏拙 |
| sleeper agent, probe | 潜伏特工，探针 |
| evaluation awareness | 评测意识 |
| chain-of-thought monitoring, monitorability, obfuscation | 思维链监控，可监控性，混淆 |
| AI control; red team, blue team; trusted and untrusted model | AI控制；红队，蓝队；可信模型与不可信模型 |
| audit budget, trusted monitoring, defer to trusted | 审计预算，可信监控，转交可信模型 |
| safety, usefulness | 安全性，有用性 |
| frontier safety framework, capability threshold | 前沿安全框架，能力阈值 |
| safeguard, classifier, adaptive attack | 防护措施，分类器，自适应攻击 |
| memorization, extraction, membership inference | 记忆，提取，成员推断 |
| differential privacy, ε, DP-SGD, clipping, accountant | 差分隐私，ε，DP-SGD，裁剪，隐私会计 |
| exposure | 暴露度 |
