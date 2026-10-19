# AI, Built — Part 27: Post-Training and Alignment

Part 27 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). How a model that predicts text becomes an assistant that tries to help: supervised
fine-tuning, low-rank adapters, reward models learned from comparisons, reinforcement learning from human feedback
and its exact optimum, Goodhart's law measured, direct preference optimization, AI feedback under written
principles, distillation, model merging, and what goes wrong. Every method runs on the series' own model: a
6.8-million-parameter transformer trained on thirty novels (`explainer/ai/novels.py`), fine-tuned on this computer.

* **The same model, before and after.** Our base model asked for a line about something continues a novel; a few
  minutes of fine-tuning later it answers. InstructGPT's 1.3B model preferred to GPT-3's 175B (Ouyang et al. 2022).
* **1. From predictor to assistant.** What pretraining optimizes; the InstructGPT pipeline (13k demonstrations, 33k
  ranked prompts, 31k PPO prompts, about 40 contractors); Christiano et al.'s backflip from about 900 comparisons
  (2017), Stiennon et al.'s summaries (2020), ChatGPT (30 November 2022), Llama 2-Chat, DPO; alignment (helpful,
  honest, harmless; Askell et al. 2021).
* **2. Supervised fine-tuning.** Chat templates and special tokens; the loss masked to the answer = −log p(y | x);
  the two tasks made from the novels (which book? and a line about...); the base model against the fine-tuned one on
  held-out sentences; accuracy over training; forgetting on novel text; FLAN, Alpaca, LIMA, synthetic data.
* **3. Low-rank adapters.** Intrinsic dimension (Li et al. 2018; Aghajanyan et al. 2020); LoRA's W + (α/r) BA,
  r(d + k) against dk, B = 0 at the start and merged afterwards (Hu et al. 2021); ranks 1, 4, 16 against full
  fine-tuning on our model: parameters, accuracy, forgetting; QLoRA, DoRA, "LoRA learns less and forgets less".
* **4. Learning what people prefer.** Why comparisons (InstructGPT's labellers agreed 73% of the time);
  Bradley–Terry = Elo (Part 26); the reward model's loss; only differences are identified; our simulated people and
  their hidden taste ("gold"); reward-model accuracy against the number of comparisons, and its ceiling, tested on
  comparisons between lines no reward model trained on; InstructGPT's reward model at 69.6%.
* **5. Reinforcement learning on a leash.** The KL-regularized objective; its optimum π* ∝ π_ref e^{r/β}, derived;
  the optimum over eight real answers as β falls; KL-penalized policy gradient on our model at two penalties, the
  reward model's score against gold (three seeds each, with their spread), and the loosely leashed run replayed
  through its samples.
* **6. When the measure becomes the target.** Goodhart (1975) and Strathern (1997); the boat that circles forever
  (OpenAI 2016); best-of-n's KL = log n − (n−1)/n, derived; best-of-n on our model with a small and a large reward
  model, proxy against gold; Gao, Schulman & Hilton's functional forms (2023).
* **7. Direct preference optimization.** DPO derived from the optimum and Bradley–Terry (Rafailov et al. 2023);
  trained on our comparisons and compared with RLHF; likelihood displacement; every method on one chart, gold gained
  against √KL (best-of-n, RLHF at two β, DPO at three); IPO, KTO, SimPO; online against offline data.
* **8. Feedback from AI, rules from people.** Constitutional AI's critique-and-revise and RLAIF (Bai et al. 2022);
  Lee et al. (2023); a reward model trained on another reward model's labels, on our model; published constitutions,
  OpenAI's Model Spec and deliberative alignment (2024), Claude's 2026 constitution.
* **9. Distillation.** Soft targets and temperature (Hinton et al. 2015); forward against reverse KL (Part 1's
  two-peaked fit), on-policy distillation; a 2-layer student of our model from text and from the teacher;
  DistilBERT, sequence-level distillation, DeepSeek-R1's distilled models.
* **10. Adding models together.** Linear mode connectivity (Frankle et al. 2020), model soups (Wortsman et al.
  2022), task arithmetic (Ilharco et al. 2023), on our model; TIES, DARE, Llama 3's averaging.
* **11. What goes wrong.** Sycophancy (Sharma et al. 2023; GPT-4o's rolled-back update, 2025); adversarial suffixes
  (Zou et al. 2023), many-shot jailbreaking (Anil et al. 2024), over-refusal (XSTest); emergent misalignment (Betley
  et al. 2025); alignment faking (Greenblatt et al. 2024); persona vectors (Chen et al. 2025).
* **12. The open recipes.** InstructGPT, Llama 2-Chat, Zephyr, Llama 3, Tülu 3, DeepSeek-R1; R1-Zero's AIME 2024
  accuracy (15.6% → 71.0%, 86.7% by majority vote) and its "aha moment"; Qwen3's four-stage pipeline and
  strong-to-weak distillation (on Qwen3-8B: 1,800 GPU hours against RL's 17,920, and better; Qwen Team 2025).
* **Recap** in eight pictures from the part's own results, where it comes back, the problem set, Part 28's teaser,
  references.

Run from the repo root:

```
python -m explainer.ai.novels             # the series' base model: about 1.5 hours on 4 cores (cached)
python -m videos.ai.ai27.compute          # every experiment (about 2 hours)
python tools/build.py ai27                # English
python tools/build.py ai27 --lang zh      # Chinese
```

`compute.py` builds the two tasks from the novels (test questions come from paragraphs held out of the base model's
training), fine-tunes, collects simulated comparisons, and trains every reward model and policy; `post.py` holds the
chat template, loss masking, LoRA and sampling.

References: Ouyang et al. (2022); Christiano et al. (2017); Stiennon et al. (2020); Askell et al. (2021); Wei et al.,
FLAN (2021); Taori et al., Alpaca (2023); Zhou et al., LIMA (2023); Li et al. (2018); Aghajanyan et al. (2020); Hu et
al., LoRA (2021); Dettmers et al., QLoRA (2023); Liu et al., DoRA (2024); Biderman et al. (2024); Bradley & Terry
(1952); Gao, Schulman & Hilton (2023); Rafailov et al., DPO (2023); Azar et al., IPO (2023); Ethayarajh et al., KTO
(2024); Meng et al., SimPO (2024); Tang et al. (2024); Bai et al., Constitutional AI (2022); Lee et al., RLAIF (2023);
Guan et al., Deliberative alignment (2024); Hinton, Vinyals & Dean (2015); Kim & Rush (2016); Sanh et al. (2019); Gu
et al., MiniLLM (2024); Frankle et al. (2020); Wortsman et al. (2022); Ilharco et al. (2023); Yadav et al., TIES
(2023); Yu et al., DARE (2024); Sharma et al. (2023); Zou et al. (2023); Anil et al. (2024); Röttger et al. (2023);
Betley et al. (2025); Greenblatt et al. (2024); Chen et al. (2025); Touvron et al. (2023); Tunstall et al. (2023);
Llama Team (2024); Lambert et al., Tülu 3 (2024); DeepSeek-AI (2025); Qwen Team (2025); Anthropic, Claude's
constitution (2026); N. Lambert, *Reinforcement Learning from Human
Feedback* (2025).

## Problems, with solutions

**1. Shifts don't matter.** Show that the Bradley–Terry likelihood of a set of comparisons is unchanged if a constant
c(x) is added to r(x, y) for every answer y to a question x.

*Solution.* Each comparison's probability is σ(r(x, y_w) − r(x, y_l)); adding c(x) to both rewards leaves the
difference, and so every factor of the likelihood, unchanged. Only differences within a question are identified,
which is why a reward model's raw scores can't be compared across questions.

**2. The KL-regularized optimum.** Prove that π* ∝ π_ref e^{r/β} maximizes J(π) = E_π[r] − β KL(π ‖ π_ref), and that
the maximum is β log Z, Z = Σ_y π_ref(y) e^{r(y)/β}.

*Solution.* J(π) = Σ π (r − β log(π/π_ref)) = −β Σ π log(π / (π_ref e^{r/β})) = −β KL(π ‖ π*) + β log Z. KL ≥ 0 with
equality only at π = π* (Gibbs), so π* is the maximizer and J(π*) = β log Z.

**3. Best-of-n.** Show that best-of-n sampling has KL(π_BoN ‖ π_ref) = log n − (n−1)/n when the reward has no ties.

*Solution.* Let u ∈ [0, 1] be an answer's quantile under π_ref, ordered by reward. The best of n has quantile
max(u_1, …, u_n), with density n u^{n−1}; since π_BoN(y) / π_ref(y) = n u(y)^{n−1}, the KL is E[log n + (n−1) log u]
with u ~ Beta(n, 1). E[log u] = −1/n, so KL = log n − (n−1)/n.

**4. What DPO's gradient weighs.** Compute the gradient of the DPO loss for one pair, with r̂ = β log π_θ/π_ref.

*Solution.* L = −log σ(r̂_w − r̂_l), so ∇L = −σ(r̂_l − r̂_w) (∇r̂_w − ∇r̂_l) = −β σ(r̂_l − r̂_w) (∇ log π_θ(y_w) −
∇ log π_θ(y_l)). Each pair pushes the preferred answer up and the rejected one down, weighted by how wrongly the
implicit reward currently orders them.

**5. When LoRA stops saving.** A rank-r adapter on a d × k matrix has r(d + k) parameters. For d = k = 4096, at what
rank does it have as many as the matrix?

*Solution.* r(d + k) = dk gives r = dk/(d + k) = 2048. Ranks in practice are 4 to 64, a few thousandths of the
matrix.

**6. Forward KL matches moments.** Fit a Gaussian q to a density p by minimizing KL(p ‖ q). Show that q has p's mean
and variance.

*Solution.* KL(p ‖ q) = −H(p) − E_p[log q] and −E_p[log q] = ½ log(2πσ²) + E_p[(x − μ)²]/(2σ²). Setting the
derivatives to zero gives μ = E_p[x] and σ² = E_p[(x − μ)²]. This is why the forward-KL fit of chapter nine spreads
over both peaks.

## 习题与解答

**1. 平移无关。** 证明：对同一个问题x的每个回答y，都给r(x, y)加上同一个常数c(x)，Bradley–Terry 似然不变。

*解答。* 每次比较的概率是 σ(r(x, y_w) − r(x, y_l))；两个奖励同时加上c(x)，差不变，所以似然的每个因子都不变。能辨识的只有
同一问题内的差，这也是奖励模型的原始分数不能跨问题比较的原因。

**2. KL正则化的最优解。** 证明 π* ∝ π_ref e^{r/β} 使 J(π) = E_π[r] − β KL(π ‖ π_ref) 最大，并且最大值为 β log Z，其中
Z = Σ_y π_ref(y) e^{r(y)/β}。

*解答。* J(π) = Σ π (r − β log(π/π_ref)) = −β Σ π log(π / (π_ref e^{r/β})) = −β KL(π ‖ π*) + β log Z。KL ≥ 0，且只在
π = π* 时取等号（吉布斯不等式），所以 π* 是最优解，J(π*) = β log Z。

**3. 最优n选1。** 证明当奖励没有并列时，最优n选1采样满足 KL(π_BoN ‖ π_ref) = log n − (n−1)/n。

*解答。* 设u ∈ [0, 1]是一个回答按奖励排序在π_ref下的分位数。n个里最好的那个，分位数是 max(u_1, …, u_n)，密度为 n u^{n−1}；
由于 π_BoN(y)/π_ref(y) = n u(y)^{n−1}，KL = E[log n + (n−1) log u]，其中 u ~ Beta(n, 1)。E[log u] = −1/n，所以
KL = log n − (n−1)/n。

**4. DPO的梯度在加权什么。** 记 r̂ = β log π_θ/π_ref，求一对样本上DPO损失的梯度。

*解答。* L = −log σ(r̂_w − r̂_l)，所以 ∇L = −σ(r̂_l − r̂_w)(∇r̂_w − ∇r̂_l) = −β σ(r̂_l − r̂_w)(∇log π_θ(y_w) −
∇log π_θ(y_l))。每一对都把被偏好的回答往上推、被拒绝的往下压，权重是隐式奖励目前把它们排错的程度。

**5. LoRA什么时候不再省。** 秩为r的适配器放在d × k矩阵上，有 r(d + k) 个参数。d = k = 4096 时，秩为多少时它和矩阵一样大？

*解答。* r(d + k) = dk，得 r = dk/(d + k) = 2048。实际用的秩是4到64，只有矩阵的千分之几。

**6. 正向KL匹配矩。** 用最小化 KL(p ‖ q) 的方法，把高斯分布q拟合到密度p上。证明q的均值和方差等于p的。

*解答。* KL(p ‖ q) = −H(p) − E_p[log q]，而 −E_p[log q] = ½ log(2πσ²) + E_p[(x − μ)²]/(2σ²)。令导数为零，得
μ = E_p[x]，σ² = E_p[(x − μ)²]。这就是第9章里正向KL的拟合会同时覆盖两个峰的原因。
