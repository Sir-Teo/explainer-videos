# AI, Built — Part 27: Post-Training and Alignment

Part 27 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). How a model that predicts text becomes an assistant that tries to help: supervised
fine-tuning, low-rank adapters, reward models learned from comparisons and what one of them actually learns,
reinforcement learning from human feedback, its exact optimum and how PPO is fitted to a language model, Goodhart's
law measured, direct preference optimization, AI feedback under written principles, distillation, model merging, and
what goes wrong. Every method runs on the series' own model: a 6.8-million-parameter transformer trained on thirty
novels (`explainer/ai/novels.py`), fine-tuned on this computer, and every number on screen is computed from it or
cited.

* **The same model, before and after.** Our base model asked for a line about something continues a novel; a few
  minutes of fine-tuning later it answers. InstructGPT's 1.3B model preferred to GPT-3's 175B (Ouyang et al. 2022).
* **1. From predictor to assistant.** What pretraining optimizes; the InstructGPT pipeline (13k demonstrations, 33k
  ranked prompts, 31k PPO prompts, about 40 contractors); Christiano et al.'s backflip from about 900 comparisons
  (2017), Stiennon et al.'s summaries (2020), ChatGPT (30 November 2022), Llama 2-Chat, DPO; alignment (helpful,
  honest, harmless; Askell et al. 2021).
* **2. Supervised fine-tuning.** Chat templates and special tokens; the loss masked to the answer = −log p(y | x);
  the two tasks made from the novels (which book? and a line about...); the base model against the fine-tuned one on
  held-out sentences; accuracy over training (on an even sample of the test sentences); forgetting on novel text;
  FLAN, Alpaca, LIMA, synthetic data.
* **3. Low-rank adapters.** What full fine-tuning stores (a copy per task); intrinsic dimension (Li et al. 2018;
  Aghajanyan et al. 2020); LoRA's W + (α/r) BA, r(d + k) against dk, B = 0 at the start and merged afterwards (Hu et
  al. 2021); ranks 1, 4, 16 against full fine-tuning on our model: parameters, accuracy over training, forgetting;
  QLoRA, DoRA, "LoRA learns less and forgets less".
* **4. Learning what people prefer.** Why comparisons (InstructGPT's labellers agreed 73% of the time);
  Bradley–Terry = Elo (Part 26); the reward model's loss; only differences are identified; our simulated people and
  their hidden taste ("gold": mood, concision past 12 words, no repetition); reward-model accuracy against the number
  of comparisons, and its ceiling, tested on comparisons between lines no reward model trained on; InstructGPT's
  reward model at 69.6%.
* **5. Inside our reward model.** What a real lab cannot do: compare the reward model with the taste it learned. On
  600 new lines: its score against gold, raw and with each question's average taken out (the shift chapter 4 said
  is never learned); its slope against the perfect learner's 1/τ; how often it orders two lines as gold does, against
  one simulated person; its score fitted as a sum of gold's own terms (mood, length, repetition, too short), for the
  reward models from 100 and from all comparisons; its score by line length beside gold's; which words raise and
  lower it, found by deleting one word at a time, against gold's change for the same deletion; the lines where the two
  disagree most, and why gold disagrees; each question's favourite line by the reward model, what it believed and
  what gold says: regressional and extremal Goodhart (Manheim & Garrabrant 2018).
* **6. Reinforcement learning on a leash.** The KL-regularized objective; its optimum π* ∝ π_ref e^{r/β}, derived;
  the optimum over eight real lines of comparable probability as β falls; PPO fitted to a language model: an answer
  as an episode, InstructGPT's per-token KL penalty with the reward model's score at the end, the value network
  initialized from the reward model, four networks in memory; baselines: the value network, RLOO's leave-one-out
  (Ahmadian et al. 2024), GRPO's group mean and spread (Shao et al. 2024; Part 28), and our runs' batch mean (= RLOO ×
  15/16); measured on our model: how well two batches' gradient estimates agree with no baseline, one shared
  baseline, each question's average, and the batch mean; KL-penalized policy gradient at two penalties (three seeds
  each), the reward model's belief against gold, both in gold units; the loosely leashed run replayed with gold's
  score beside its lines.
* **7. When the measure becomes the target.** Goodhart (1975) and Strathern (1997); the boat that circles forever
  (OpenAI 2016); best-of-n's KL = log n − (n−1)/n, derived; best-of-n on our model with a small and a large reward
  model, proxy and gold each on its own scale; Gao, Schulman & Hilton's functional forms (2023).
* **8. Direct preference optimization.** DPO derived from the optimum and Bradley–Terry (Rafailov et al. 2023);
  trained on our comparisons and compared with RLHF; likelihood displacement; every method on one chart, gold gained
  against √KL (best-of-n, RLHF at two β, DPO at three); IPO, KTO, SimPO; online against offline data.
* **9. Feedback from AI, rules from people.** Constitutional AI's critique-and-revise and RLAIF (Bai et al. 2022);
  Lee et al. (2023); a reward model trained on another reward model's labels, on our model; published constitutions,
  OpenAI's Model Spec and deliberative alignment (2024), Claude's 2026 constitution.
* **10. Distillation.** Soft targets and temperature (Hinton et al. 2015); forward against reverse KL (Part 1's
  two-peaked fit), on-policy distillation; a 2-layer student of our model from text and from the teacher;
  DistilBERT, sequence-level distillation, DeepSeek-R1's distilled models.
* **11. Adding models together.** Linear mode connectivity (Frankle et al. 2020), model soups (Wortsman et al.
  2022), task arithmetic (Ilharco et al. 2023), on our model; TIES, DARE, Llama 3's averaging.
* **12. What goes wrong.** Sycophancy (Sharma et al. 2023; GPT-4o's rolled-back update, 2025); adversarial suffixes
  (Zou et al. 2023), many-shot jailbreaking (Anil et al. 2024), over-refusal (XSTest); emergent misalignment (Betley
  et al. 2025); alignment faking (Greenblatt et al. 2024); persona vectors (Chen et al. 2025).
* **13. The open recipes.** InstructGPT, Llama 2-Chat, Zephyr, Llama 3, Tülu 3, DeepSeek-R1; R1-Zero's AIME 2024
  accuracy (15.6% → 71.0%, 86.7% by majority vote) and its "aha moment"; Qwen3's four-stage pipeline and
  strong-to-weak distillation (on Qwen3-8B: 1,800 GPU hours against RL's 17,920, and better; Qwen Team 2025).
* **Recap** in ten pictures from the part's own results, where it comes back, the problem set (eight problems), Part
  28's teaser, references.

The silent preview runs 51.8 minutes (`python tools/lecture_length.py ai27`); the longest chapters are 5 (6.5
minutes) and 6 (7.4).

## Running it

From the repo root:

```
python tools/make.py ai27                   # everything: the base model if missing, the computations, English and Chinese
python -m explainer.ai.novels               # the series' base model alone (cached in .cache/novels/)
python -m videos.ai.ai27.compute            # every experiment, resuming where it stopped
python -m videos.ai.ai27.compute --force inside baselines   # recompute named items
python tools/build.py ai27                  # English
python tools/zh_lines.py ai27 --verify && python tools/build.py ai27 --lang zh     # Chinese
EXPLAINER_TTS=silent python tools/build.py ai27 -q l --fps 30 --lang en -j 2     # a quick silent preview
```

`compute.py` builds the two tasks from the novels (test questions come from paragraphs held out of the base model's
training), fine-tunes, collects simulated comparisons, trains every reward model and policy, and looks inside the
reward models; `post.py` holds the chat template, loss masking, LoRA and sampling. Every random choice is seeded
(numpy PCG64, `torch.manual_seed`, one `torch.Generator` per sampling call), so the same machine gives the same
numbers; another machine's floating point can move the last digits, and the narration (English and Chinese) is
written over the cached results and branches on them. Fine-tuning checkpoints every 50 steps (`.cache/ai27/*.ckpt`);
the items made of several runs (lora, rlhf, dpo_sweep, merge) keep each finished run (`CACHE.partial`); every other
item takes minutes. The torch thread count is set only when `compute.py` runs as a program (`AI27_THREADS`, default
up to 4); importing it from a scene changes nothing. Works on macOS and Linux (no multiprocessing).

On this shared Linux machine (four cores, load 6–9, one thread: `AI27_THREADS=1 nice -n 15`), the items took:
data and sft about 12 minutes, lora 1.1 hours, prefs 4 minutes, rm 1.1 hours, rlaif 1.1 hours, bon 18 minutes, rlhf
1.4 hours, dpo 10 minutes, dpo_sweep 26 minutes, merge 25 minutes, inside about 3 minutes, baselines about 2 minutes,
closed under a minute; a laptop with four free cores is several times faster.

## Results on this machine

- **Tasks**: which-book 6,000 training / 560 test sentences, 30 titles (chance 3%); a line about... 5,569 training lines, 30 topics.
- **SFT** (600 steps): which-book 0% → 27% on all 560 test sentences (in-training evaluations on an even sample of 150: 12%, 16%, 22%, 23%, 25%, 23%); held-out novel loss 3.602 → 4.226 nats; its lines: gold -0.25, 93% end cleanly.
- **LoRA** (which-book only, 600 steps): rank 1: 26,208 trained numbers, 14%, forgetting +0.894; rank 4: 104,832 trained numbers, 28%, forgetting +1.253; rank 16: 419,328 trained numbers, 31%, forgetting +1.856; full: 6,843,648 trained numbers, 33%, forgetting +1.103.
- **Comparisons**: 4,200 training, 840 test (between lines no reward model trained on). Reward models: 100 → 53%, 400 → 59%, 1,600 → 63%, 4,200 → 64%; ceiling (people agree with gold) 73%.
- **Inside the reward model** (600 new lines, 20 per question): correlation with gold 0.52 raw, 0.52 within a question (small model: 0.25, 0.24); slope 1.84 (perfect learner 4; small 3.02); orders 71% of 5,442 untied pairs as gold does (small 59%; one simulated person 76%).
  Weights on gold's terms as a share of gold's own (gold units): large mood 0.26, length 1.94, repetition 0.11, too short 0.87 (R² 0.46); small mood 0.14, length 2.23, repetition -0.50, too short 0.56 (R² 0.12).
  Words (deleted one at a time, ≥6 occurrences, 235 words; correlation with gold's change 0.20): raise most: good, music, said, than, gave, only, hand, place; lower most: felt, didn't, began, followed, don't, sea, reached, two.
  Each question's favourite: the large model believes +1.01, gold says +0.27, gold's own favourite +0.54; same line as gold's in 20% of questions (small model: believes +1.38, gold -0.01).
- **AI feedback**: judge from 100 comparisons 53%; fresh model on its 1,600 labels 55%; on 1,600 human labels 59%; the judge agrees with the people on 55%.
- **The KL-regularized optimum** over 8 lines about the sea (log-probabilities within 3.9 nats of each other, from 254 samples whose log-probabilities span 185 nats): share on the best line π_ref 3%, β=10: 4%, β=1: 12%, β=0.3: 66%, β=0.1: 100%.
- **Baselines** (first step, 6 batches × 16 lines, 6 questions): cosine between two batches' gradients: none 0.013, shifted 0.001, shared 0.014, value 0.015, group 0.014; the reward model's per-question mean ranges +0.19 to +1.15; mean squared gradient length relative to the batch-mean baseline: none 1.1×, shifted 20.9×, shared 1.1×, value 1.0×, group 1.0×.
- **Best-of-n**, small reward model: gold -0.250 at n=1, rising to -0.087 at n=256; proxy 1.50 → 5.68.
- **Best-of-n**, large reward model: gold -0.250 at n=1, peak +0.060 at n=128, -0.001 at n=256; proxy 0.83 → 3.31.
- **RLHF** β=0.1 (3 seeds, last 30 steps): reward model believes +0.634, gold +0.178 (gold units, over the fine-tuned model); KL 1.58; seed 0's final policy: gold -0.027, KL 1.57, 100% end cleanly.
- **RLHF** β=0.01 (3 seeds, last 30 steps): reward model believes +0.664, gold +0.184 (gold units, over the fine-tuned model); KL 2.04; seed 0's final policy: gold -0.046, KL 2.56, 100% end cleanly.
- **DPO** β=0.1: gold -0.023, KL 1.69, 100% end cleanly; probe pairs at the end: preferred +1.3, rejected -11.7 nats. Other β: β=0.03: gold -0.086, KL 6.49; β=0.3: gold -0.096, KL 0.76.
- **Distillation** (2-layer student, 1,438,336 parameters; teacher 6,843,648, held-out 3.602): from text 5.042, from the teacher 4.657 nats.
- **Merging**: which only: which 32%, gold -0.86, ended 100%; line only: which 0%, gold -0.27, ended 87%; sum x 0: which 0%, gold -0.52, ended 0%; sum x 0.5: which 20%, gold -0.56, ended 92%; sum x 1: which 22%, gold -0.69, ended 100%; path: 0.0: 33%/100%, 0.2: 31%/100%, 0.4: 27%/90%, 0.6: 13%/80%, 0.8: 0%/83%, 1.0: 0%/87%.

## Problems found and fixed while making it

- **The in-training evaluations sampled a few books only.** The which-book test list runs book by book, so its first
  150 sentences covered five titles; the SFT curve stopped near 17% while the final score on every sentence was 27%.
  `which_accuracy(model, d, n)` now takes an even sample, and sft, lora and merge were recomputed; the fine-tuned
  weights came out identical tensor for tensor (training never depended on the evaluations).
- **The closed-form optimum had nothing to show.** Over 64 samples a line's probability under the fine-tuned model
  spans tens of nats, so after renormalizing over eight lines spread over gold, one line held 99.96% of π_ref and no β
  moved it, while the narration claimed the probability piled onto the best answer. The eight lines are now, of every
  run of eight lines consecutive in log-probability and within 4 nats of each other, the one widest in gold, from 256
  samples; the narration branches on the shares it reports.
- **Deleting a line's last word also deleted its full stop.** The first occlusion pass dropped the final token, and
  with it the punctuation, which alone moved the reward model's score by about 2.5 on one line; a word is now deleted
  with its punctuation kept, and the example line is an ordinary one, not the most extreme.
- **A baseline that changed nothing.** With the reward model's scores as learned, every baseline gave about the same
  agreement between batches; the measurement now also adds a constant to every score (a shift the comparisons never
  pinned down), which is what a baseline is there to remove, and the narration says which effect the data show.
- **RLHF's curves zig-zagged with the question.** The runs take the thirty questions in turn and the reward model's
  scores carry an arbitrary shift per question; the reward model's score and gold also sat on scales four times apart.
  The chart now shows means over thirty-step windows (each question once, so the shifts cancel) as gains over the
  fine-tuned model, the reward model's divided by its slope on gold from chapter 5.
- **Gold and the proxy were nearly the same orange.** Gold is now yellow.
- **A new chapter's file name.** The Chinese template tools find scene modules by `s[0-9][0-9]_*.py`, so the new
  chapter is `s05_inside.py` (a name like `s05b_inside.py` would be invisible to them).
- Prompts the model reads ("Write a line about the sea.") are drawn as data and stay in English in the Chinese build,
  as the model's own lines do; on-screen labels no longer splice topic words into translated text.

## References

Ouyang et al. (2022); Christiano et al. (2017); Stiennon et al. (2020); Askell et al. (2021); Wei et al., FLAN (2021);
Taori et al., Alpaca (2023); Zhou et al., LIMA (2023); Li et al. (2018); Aghajanyan et al. (2020); Hu et al., LoRA
(2021); Dettmers et al., QLoRA (2023); Liu et al., DoRA (2024); Biderman et al. (2024); Bradley & Terry (1952);
Manheim & Garrabrant, *Categorizing variants of Goodhart's law* (2018); Gao, Schulman & Hilton (2023); Ziegler et al.,
*Fine-tuning language models from human preferences* (2019); Schulman et al., PPO (2017) and GAE (2016); Kool, van Hoof
& Welling, *Buy 4 REINFORCE samples, get a baseline for free!* (2019); Ahmadian et al., *Back to basics: revisiting
REINFORCE style optimization for learning from human feedback in LLMs* (2024); Shao et al., *DeepSeekMath* (GRPO,
2024); Rafailov et al., DPO (2023); Azar et al., IPO (2023); Ethayarajh et al., KTO (2024); Meng et al., SimPO (2024);
Tang et al. (2024); Bai et al., Constitutional AI (2022); Lee et al., RLAIF (2023); Guan et al., Deliberative alignment
(2024); Hinton, Vinyals & Dean (2015); Kim & Rush (2016); Sanh et al. (2019); Gu et al., MiniLLM (2024); Agarwal et al.,
GKD (2024); Frankle et al. (2020); Wortsman et al. (2022); Ilharco et al. (2023); Yadav et al., TIES (2023); Yu et al.,
DARE (2024); Sharma et al. (2023); Zou et al. (2023); Anil et al. (2024); Röttger et al. (2023); Betley et al. (2025);
Greenblatt et al. (2024); Chen et al. (2025); Touvron et al. (2023); Tunstall et al. (2023); Llama Team (2024); Lambert
et al., Tülu 3 (2024); DeepSeek-AI (2025); Qwen Team (2025); Anthropic, Claude's constitution (2026); N. Lambert,
*Reinforcement Learning from Human Feedback* (2025).

Checked against the primary sources for this part's new material: InstructGPT §3.5 and Appendix C (a per-token KL
penalty from the SFT model; the value function initialized from the reward model; a 6B reward model and 6B value
function for every policy size; PPO clip 0.2, no discount in GAE); DeepSeekMath §4.1 (GRPO drops the value model and
uses the group's average reward as the baseline, with the KL in the loss rather than the reward; PPO's value model is
"typically another model of comparable size"); Ahmadian et al. (PPO loads up to four models; RLOO outperforms PPO,
DPO and RAFT in their experiments); Manheim & Garrabrant (regressional: "when selecting for a proxy measure, you select
not only for the true goal, but also for the difference between the proxy and the goal"; extremal). DeepSeek-R1 (arXiv 2501.12948): R1-Zero and R1 are
trained with GRPO, which "foregoes the critic model"; R1-Zero's AIME 2024 pass@1 rises from 15.6% to 71.0%, 86.7% by
majority vote over 64 samples; the "aha moment" line; 800K samples for the distilled models. Zou et al. (2023): the
suffix is searched (greedy and gradient-based) to make the model's answer begin "Sure, here is".

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
derivatives to zero gives μ = E_p[x] and σ² = E_p[(x − μ)²]. This is why the forward-KL fit of chapter ten spreads
over both peaks.

**7. Baselines.** Show that E_{y~π}[b ∇ log π(y)] = 0 for any b that does not depend on y, and that for k answers
r_i − mean(r) = ((k−1)/k)(r_i − mean_{j≠i} r_j).

*Solution.* E_π[b ∇ log π(y)] = b Σ_y π(y) ∇π(y)/π(y) = b ∇ Σ_y π(y) = b ∇1 = 0, so a baseline leaves the gradient's
mean unchanged and can only change its noise (chapter 6 measures how much). With m_{−i} the mean of the others,
mean(r) = (r_i + (k−1) m_{−i})/k, so r_i − mean(r) = ((k−1)/k)(r_i − m_{−i}): our runs' batch-mean baseline is RLOO's
leave-one-out baseline, scaled by 15/16 for k = 16.

**8. Regressional Goodhart.** Let gold G ~ N(0, σ_G²) and a proxy R = G + E with independent noise E ~ N(0, σ_E²).
Show that E[G | R = r] = r σ_G² / (σ_G² + σ_E²).

*Solution.* G and R are jointly Gaussian with Cov(G, R) = σ_G² and Var(R) = σ_G² + σ_E², so E[G | R = r] =
r Cov(G, R)/Var(R) = r σ_G²/(σ_G² + σ_E²). An answer chosen because its proxy score is r is worth only that fraction
of r, on average: the shortfall r σ_E²/(σ_G² + σ_E²) grows with r, so the harder you select, the more you are
selecting noise. Chapter 5 measures it on our reward model's favourite lines.

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
μ = E_p[x]，σ² = E_p[(x − μ)²]。这就是第10章里正向KL的拟合会同时覆盖两个峰的原因。

**7. 基线。** 证明：对任何不依赖于y的b，E_{y~π}[b ∇ log π(y)] = 0；并证明对k个回答，r_i − mean(r) = ((k−1)/k)(r_i −
mean_{j≠i} r_j)。

*解答。* E_π[b ∇ log π(y)] = b Σ_y π(y) ∇π(y)/π(y) = b ∇ Σ_y π(y) = b ∇1 = 0，所以基线不改变梯度的均值，只能改变它的噪声
（第6章测量了改变多少）。记m_{−i}为其他回答的平均，则 mean(r) = (r_i + (k−1) m_{−i})/k，所以 r_i − mean(r) = ((k−1)/k)(r_i
− m_{−i})：我们训练中用的批内平均基线，就是RLOO的留一基线，在k = 16时乘以15/16。

**8. 回归型古德哈特。** 设金标准 G ~ N(0, σ_G²)，代理 R = G + E，其中噪声 E ~ N(0, σ_E²) 与G独立。证明
E[G | R = r] = r σ_G² / (σ_G² + σ_E²)。

*解答。* G和R是联合高斯的，Cov(G, R) = σ_G²，Var(R) = σ_G² + σ_E²，所以 E[G | R = r] = r Cov(G, R)/Var(R) =
r σ_G²/(σ_G² + σ_E²)。一个因为代理分数是r而被选中的回答，平均只值r的这么一部分：差额 r σ_E²/(σ_G² + σ_E²) 随r增大，所以挑得
越狠，挑中的噪声越多。第5章在我们奖励模型最喜欢的句子上测量了它。


## Glossary (terms in this part)

| English | 中文 |
|---|---|
| post-training, alignment | 后训练，对齐 |
| helpful, honest, harmless | 有用、诚实、无害 |
| supervised fine-tuning (SFT), instruction tuning | 监督微调（SFT），指令微调 |
| chat template, special token, loss masking | 聊天模板，特殊词元，损失屏蔽 |
| base model, fine-tuned model, forgetting | 基础模型，微调后的模型，遗忘 |
| low-rank adapter (LoRA), rank, adapter | 低秩适配器（LoRA），秩，适配器 |
| intrinsic dimension | 内在维数 |
| reward model, comparison, preference, labeller | 奖励模型，比较，偏好，标注员 |
| Bradley–Terry model | 布拉德利-特里模型 |
| gold (the hidden true taste), proxy | 金标准，代理 |
| simulated people, noise τ | 模拟的人，噪声τ |
| ceiling (of a reward model's accuracy) | 上限 |
| within-question comparison, shift per question | 同一问题内的比较，每个问题的平移 |
| correlation, slope | 相关系数，斜率 |
| gold units (a score divided by its slope on gold) | 金标准单位 |
| a perfect learner (slope 1/τ) | 完美的学习者（斜率1/τ） |
| decomposition into gold's terms: mood, length, repetition, too short | 按金标准的各项分解：情绪，长度，重复，太短 |
| occlusion (deleting one word at a time) | 遮挡（一次删掉一个词） |
| regressional Goodhart, extremal Goodhart | 回归型古德哈特，极端型古德哈特 |
| reinforcement learning from human feedback (RLHF) | 基于人类反馈的强化学习（RLHF） |
| reference model, the KL leash, β | 参考模型，KL绳子，β |
| KL-regularized optimum, partition function Z | KL正则化的最优解，配分函数Z |
| an answer as an episode: state, action (token) | 把回答当作回合：状态，动作（词元） |
| per-token KL penalty | 逐词元的KL惩罚 |
| value network (value model), critic | 价值网络（价值模型），评论家 |
| advantage, generalized advantage estimation (GAE) | 优势，广义优势估计（GAE） |
| baseline, group baseline, leave-one-out (RLOO) | 基线，组基线，留一（RLOO） |
| group relative policy optimization (GRPO) | 组相对策略优化（GRPO） |
| gradient estimate, cosine between two estimates | 梯度估计，两个估计之间的余弦 |
| best-of-n | 最优n选1 |
| over-optimization, reward hacking | 过度优化，奖励投机 |
| Goodhart's law | 古德哈特定律 |
| direct preference optimization (DPO), implicit reward | 直接偏好优化（DPO），隐式奖励 |
| likelihood displacement | 似然位移 |
| online / offline preference data | 在线/离线偏好数据 |
| Constitutional AI, constitution, critique and revision | 宪法式AI，宪法，批评与修改 |
| RL from AI feedback (RLAIF), AI judge | 基于AI反馈的强化学习（RLAIF），AI裁判 |
| model spec, deliberative alignment | 模型规范，审慎对齐 |
| distillation, teacher, student, soft targets, dark knowledge, temperature | 蒸馏，老师，学生，软目标，暗知识，温度 |
| forward KL, reverse KL, on-policy distillation | 前向KL，反向KL，在线策略蒸馏 |
| model merging, task vector, task arithmetic, model soup | 模型合并，任务向量，任务算术，模型汤 |
| linear mode connectivity | 线性模式连通 |
| sycophancy, jailbreak, adversarial suffix, many-shot jailbreaking, over-refusal | 谄媚，越狱，对抗后缀，多样本越狱，过度拒绝 |
| emergent misalignment, alignment faking, persona vector | 涌现式失准，对齐伪装，人格向量 |
| cold start, strong-to-weak distillation | 冷启动，强到弱蒸馏 |
