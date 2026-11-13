"""Act V, Agency, and Act VI, Understanding (Parts 26-31): reinforcement learning, post-training, reasoning, agents, interpretability, trust."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=26, level="U", widget="bellmansweep", prereq=(2, 5, 9),
        question="How do you learn to act when nobody tells you the right action, only how things turned out?",
        story="The part opens in Seoul in March 2016, on AlphaGo's move 37 against Lee Sedol, a move its own model "
              "of human play rated at one in ten thousand. It then starts from Thorndike's puzzle boxes and the "
              "agent-environment loop, and meets exploration on a ten-armed bandit, where the upper confidence "
              "bound is derived from Hoeffding's inequality. Bellman's equation is derived on a slippery gridworld "
              "of 44 states, and value iteration is proved to converge because the Bellman operator is a "
              "contraction. The part turns when the model and the sweep over every state are taken away: temporal "
              "differences, Sarsa and Q-learning learn from sampled experience on the random walk and the cliff "
              "walk, and DQN and PPO are trained on the cart-pole with their training replayed. Search enters "
              "with minimax, alpha-beta and Monte Carlo tree search on Connect Four, and joins learning in "
              "AlphaGo and AlphaZero; the part's own AlphaZero for Connect Four is graded move by move against a "
              "perfect solver. It ends with MuZero's learned model and with games of hidden information, where "
              "regret matching and CFR find the equilibrium of Kuhn poker.",
        handoff="PPO with a reward learned from human preferences trains chat models in Part 27; policy gradients "
                "on checkable answers and search over chains of thought make the reasoning models of Part 28; "
                "learned world models and long horizons are Part 29; an agent optimizing a flawed reward returns "
                "as reward hacking in Part 31.",
        outside="Probability and expectations (Part 5), gradients (Part 4) and a first idea of a neural network "
                "(Part 9); no game theory is assumed.",
        objectives={
            "U": ["Write the return, the value of a state and Bellman's equation for a small Markov decision "
                  "process, and run value iteration on it by hand for a few sweeps.",
                  "Explain the difference between learning a value from complete episodes and from temporal "
                  "differences, and between Sarsa's and Q-learning's path on the cliff walk."],
            "M": ["Prove that the Bellman operator is a contraction in the max norm and deduce that value iteration "
                  "converges at rate gamma.",
                  "Derive the UCB bonus from Hoeffding's inequality and the policy gradient with a baseline from "
                  "the log-derivative trick.",
                  "Describe the four steps of Monte Carlo tree search and how AlphaZero uses search as a policy "
                  "improvement operator."],
            "D": ["State the Lai-Robbins lower bound and UCB1's regret, and prove that no-regret play by both "
                  "players of a zero-sum game gives an approximate Nash equilibrium.",
                  "Explain what MuZero's value-equivalent model must predict and what it is free to ignore."],
            "I": ["Implement tabular Q-learning and a DQN with replay and a target network, and diagnose "
                  "divergence from the deadly triad.",
                  "Read PPO's clipped objective term by term and say which updates it stops and which it does not."],
        },
        results=[
            ("Bellman optimality", r"V^*(s)=\max_a\sum_{s'}P(s'\mid s,a)\,\bigl[r(s,a)+\gamma V^*(s')\bigr]"),
            ("The contraction", r"\|TV-TU\|_\infty\le\gamma\,\|V-U\|_\infty"),
            ("Upper confidence bound", r"a_t=\arg\max_a\ \hat\mu_a+\sqrt{2\ln t/n_a}"),
            ("Q-learning", r"Q(s,a)\leftarrow Q(s,a)+\alpha\,\delta,\quad \delta=r+\gamma\max_{a'}Q(s',a')-Q(s,a)"),
            ("Policy gradient", r"\nabla_\theta J=\mathbb{E}\bigl[(G_t-b(s_t))\,\nabla_\theta\log\pi_\theta(a_t\mid s_t)\bigr]"),
            ("AlphaZero's loss", r"(z-v)^2-\boldsymbol\pi^\top\log\mathbf p+c\,\|\theta\|^2"),
        ],
        U=(0, 1, 3, 5, 10, 12), I=(7, 9, 13), D=(14, 15),
        also=(("The gridworld, cliff walk, random walk and cart-pole", "videos/ai/ai26/envs.py"),
              ("Connect Four with a perfect solver", "videos/ai/ai26/c4.py")),
    ),
    Part(
        n=27, level="M", widget="klleash", prereq=(1, 14, 26),
        question="How does a model that only predicts the next word become an assistant that tries to help?",
        story="The series' own 6.8-million-parameter model, trained on thirty novels, is asked for a line about a "
              "topic and continues a novel instead; after a few minutes of fine-tuning it answers. The part follows "
              "the InstructGPT pipeline in order. Supervised fine-tuning is maximum likelihood on the answer, and "
              "LoRA stores it in a low-rank update, measured at ranks 1, 4 and 16 against full fine-tuning. A "
              "reward model is fitted to simulated people's comparisons with the Bradley-Terry loss, and because "
              "their hidden taste (gold) is known here, the reward model is opened and compared with it. "
              "Reinforcement learning on a KL leash has an exact optimum, the reference reweighted by e^(r/beta), "
              "and the part turns when that optimum is pushed: best-of-n and RLHF raise what the reward model "
              "believes faster than what gold says, which is Goodhart's law measured. DPO is derived from the "
              "same optimum, and the part ends with AI feedback under written principles, distillation, model "
              "merging, the known failures (sycophancy, jailbreaks, emergent misalignment) and the open recipes.",
        handoff="Reinforcement learning on answers that can be checked, with GRPO's group baseline, is Part 28; "
                "agents trained for long tasks are Part 29; Part 30 opens the fine-tuned model with a crosscoder "
                "and persona vectors; Part 31 asks whether what post-training produces can be trusted, and reuses "
                "the which-book task for weak-to-strong supervision.",
        outside="Cross-entropy and KL divergence (Part 1), the transformer language model (Parts 13 and 14) and "
                "policy gradients with PPO (Part 26).",
        objectives={
            "U": ["Explain the stages that turn a pretrained model into an assistant, and what data each stage "
                  "needs from people.",
                  "Say in words what Goodhart's law predicts when a learned reward is optimized hard, and name "
                  "two documented failures of post-trained models."],
            "M": ["Derive the optimum of the KL-regularized objective and its value beta log Z.",
                  "Derive the DPO loss from that optimum and the Bradley-Terry model, and compute its gradient "
                  "for one pair.",
                  "Show that only reward differences within a question are identified by comparisons."],
            "D": ["Prove best-of-n's KL formula for an atomless reward and explain why it is only an upper bound "
                  "for discrete text.",
                  "Distinguish regressional from extremal Goodhart on a reward model whose target is known, and "
                  "state what a real lab cannot measure."],
            "I": ["Choose a LoRA rank from the parameter count r(d + k) and the measured trade between accuracy "
                  "and forgetting.",
                  "Compare RLHF, DPO and best-of-n by gold gained against KL spent, and say when distillation or "
                  "merging is the cheaper tool."],
        },
        results=[
            ("LoRA", r"W'=W+\frac{\alpha}{r}BA,\qquad r(d+k)\ \text{numbers instead of}\ dk"),
            ("Bradley-Terry reward model", r"P(y_w\succ y_l\mid x)=\sigma\bigl(r(x,y_w)-r(x,y_l)\bigr)"),
            ("The KL-regularized optimum", r"\pi^*(y)=\frac{\pi_{\text{ref}}(y)\,e^{r(y)/\beta}}{Z},\qquad J(\pi^*)=\beta\log Z"),
            ("Best-of-n's price", r"\operatorname{KL}(\pi_{\text{BoN}}\,\|\,\pi_{\text{ref}})\le\log n-\frac{n-1}{n}"),
            ("DPO", r"\mathcal L=-\log\sigma\bigl(\hat r_w-\hat r_l\bigr),\qquad \hat r=\beta\log\frac{\pi_\theta(y\mid x)}{\pi_{\text{ref}}(y\mid x)}"),
            ("Regressional Goodhart", r"\mathbb{E}[G\mid R=r]=r\,\frac{\sigma_G^2}{\sigma_G^2+\sigma_E^2}"),
        ],
        U=(0, 1, 2, 9, 12), I=(3, 10, 11, 13), D=(5,),
        also=(("The series' model, trained on thirty novels", "explainer/ai/novels.py"),),
    ),
    Part(
        n=28, level="M", widget="votepassk", prereq=(13, 26, 27),
        question="How does a model learn to think before it answers, and what does thinking buy?",
        story="In 2022 one sentence, let's think step by step, lifted a model's arithmetic scores; in 2024 and 2025 "
              "o1 and DeepSeek-R1 were trained to think. The part tries each idea on three tiny transformers "
              "trained here. On the parity of 16 bits a 2-layer model stays at chance when it answers at once and "
              "is almost always right when it writes the running parity first: a chain of thought is extra serial "
              "computation. Many chains and a vote amplify the answer the model already prefers, and the bound "
              "that says when is derived; graders of answers and of steps are trained and found to mislead as "
              "more samples are drawn. Then the model learns from a checker: GRPO is derived from Part 26's "
              "policy gradient, with its group baseline, clip and KL estimators, and run on two-digit addition. "
              "The part turns to what that training costs: entropy collapses, chains grow until thought has a "
              "price, and exact pass@k shows RL sharpening one try while many tries gain little. It ends with "
              "computation spent at answer time, search over thoughts, latent reasoning, proofs checked in Lean "
              "and ARC-AGI.",
        handoff="Reasoning over hundreds of steps with tools is what the agents of Part 29 do, where per-step "
                "reliability sets the horizon; whether a written chain is how the model reached its answer is "
                "Part 30's faithfulness chapter; reward hacking and monitoring the chain of thought return in "
                "Part 31.",
        outside="Policy gradients, baselines and PPO's clip from Part 26, the KL-regularized objective and "
                "best-of-n from Part 27, and Hoeffding's inequality (Part 5).",
        objectives={
            "U": ["Explain why writing intermediate steps lets a fixed-depth model compute something it cannot "
                  "compute in one pass, using the parity experiment.",
                  "Say when a majority vote over sampled chains helps and when it makes a wrong answer more certain."],
            "M": ["Derive GRPO's objective from the policy gradient: the group baseline, the ratio, the clip and "
                  "the KL term.",
                  "Prove that the pass@k estimator is unbiased and that k3 is a nonnegative, unbiased estimate "
                  "of the KL.",
                  "Bound the error of a vote over k chains with Hoeffding's inequality and a union bound."],
            "D": ["Derive the first-order entropy change of a softmax policy under a policy-gradient step and "
                  "explain entropy collapse with it.",
                  "State the two sides of the debate on whether RL widens what a model can solve, and what exact "
                  "pass@k on a small model can and cannot settle."],
            "I": ["Compare GRPO with Dr. GRPO, DAPO, GSPO and CISPO by the term each changes, and recognize a "
                  "collapsed run from its entropy and its share of groups with no signal.",
                  "Choose between voting, best-of-N with a checker, beam search and a longer chain for a fixed "
                  "budget of output tokens."],
        },
        results=[
            ("When the vote is right", r"P(\text{vote wrong})\le(m-1)\,e^{-k\Delta^2/2}"),
            ("GRPO's advantage", r"\hat A_i=\frac{r_i-\operatorname{mean}(r)}{\operatorname{std}(r)},\qquad r_i-\bar r=\tfrac{G-1}{G}\,(r_i-\bar r_{-i})"),
            ("The k3 estimator", r"k_3=\rho-1-\log\rho\ \ge 0,\quad \mathbb{E}_{\pi_\theta}[k_3]=\operatorname{KL}(\pi_\theta\|\pi_{\text{ref}}),\quad \rho=\tfrac{\pi_{\text{ref}}}{\pi_\theta}"),
            ("Unbiased pass@k", r"\mathbb{E}\Bigl[1-\tbinom{n-c}{k}\big/\tbinom{n}{k}\Bigr]=1-(1-p)^k"),
            ("Why entropy falls", r"\Delta H\approx-\operatorname{Cov}_{a\sim\pi}\bigl(\log\pi_a,\ \Delta z_a\bigr)"),
            ("Best-of-N with a checker", r"\operatorname{KL}(\pi_N\,\|\,\pi)\ \to\ \log\frac{1}{p}\quad(N\to\infty)"),
        ],
        U=(0, 1, 2, 13, 14), I=(6, 8, 10), D=(7, 9, 12),
    ),
    Part(
        n=29, level="U", widget="horizondecay", prereq=(7, 26, 28),
        question="What does it take to act over many steps in a world you only partly see?",
        story="At 97 percent a step, thirty steps in a row succeed 40 percent of the time: the part opens on sixty "
              "simulated runs dying off. It goes back to Shakey and the DARPA races, then to a robot in a corridor "
              "of 40 cells whose belief is predicted and corrected by Bayes' rule, which is Part 7's forward "
              "algorithm. The agent loop of thought, action and observation is shown on a simulated warehouse "
              "agent with tools, protocols and memory. Errors compound as p to the n, the half-way horizon is "
              "derived, and METR's time-horizon measurements are refitted to a doubling every few months. The "
              "part turns to learning to act: on a windy lane solved exactly, behaviour cloning's cost is bounded "
              "by T squared epsilon and DAgger repairs it by labelling the states the learner itself reaches. "
              "World models follow, with a small Dreamer trained from pixels inside its own dreams, then Genie, "
              "sim-to-real with domain randomization on the cart-pole, and vision-language-action models with "
              "flow-matched action chunks and FAST's DCT tokens.",
        handoff="Whether an agent's written reasoning is how it decides, and whether networks carry models of "
                "their world, are questions for Part 30; how to evaluate agents, forecast their horizons, keep "
                "them from gaming rewards and control what they touch is Part 31.",
        outside="Bayes' rule and Markov chains (Part 5), hidden Markov models (Part 7), reinforcement learning "
                "(Part 26) and flow matching (Part 21) for the last two chapters.",
        objectives={
            "U": ["Compute the chance that a task of n steps succeeds at per-step reliability p, and the task "
                  "length at which it falls to one half.",
                  "Update a belief over positions after a move and a sensor reading with Bayes' rule.",
                  "Describe the loop a language-model agent runs and what tools and memory add to it."],
            "M": ["Derive the belief update of a POMDP and identify it with the forward algorithm.",
                  "Prove behaviour cloning's bound J <= J* + T^2 eps by coupling learner and expert, and explain "
                  "why DAgger's cost grows only linearly in T.",
                  "Write Dreamer's world-model loss term by term and say what KL balancing and symlog are for."],
            "D": ["State DAgger's no-regret reduction and what its guarantee assumes about the expert and the "
                  "policy class.",
                  "Relate the ratio of 50% to 80% time horizons to the hazard's shape, and say what a falling "
                  "hazard implies for long tasks."],
            "I": ["Read an agent benchmark score (SWE-bench Verified, OSWorld, Terminal-Bench) with its known "
                  "flaws, and tell a company claim from an independent measurement.",
                  "Choose between per-step binning and DCT-based action tokens from token count and "
                  "reconstruction error, and use domain randomization to cross a reality gap."],
        },
        results=[
            ("Compounding error", r"P(\text{all } n \text{ steps right})=p^{\,n},\qquad n_{1/2}=\frac{\ln 2}{-\ln p}\approx\frac{0.69}{1-p}"),
            ("Belief update", r"b'(s')\ \propto\ O(o\mid s')\sum_{s}P(s'\mid s,a)\,b(s)"),
            ("Behaviour cloning", r"J(\hat\pi)\le J(\pi^*)+T^2\varepsilon"),
            ("Constant hazard", r"t_{50}/t_{80}=\ln 2/\ln 1.25\approx 3.1"),
            ("symlog", r"\operatorname{symlog}(x)=\operatorname{sign}(x)\,\ln(1+|x|)"),
            ("FAST's rounding error", r"\text{RMS error}\approx\frac{1}{\gamma\sqrt{12}}"),
        ],
        U=(0, 1, 2, 3, 5, 9), I=(7, 8, 14, 16), D=(13,),
    ),
    Part(
        n=30, level="M", widget="superpolygon", prereq=(3, 13, 27),
        question="We know every number in a trained network, so why can't we say what it is thinking?",
        story="The part opens on the 128 numbers Part 13's transformer carries for each character, all busy, and on "
              "the same numbers rewritten by a sparse autoencoder with a handful of features on. It first asks how "
              "to read a model without fooling yourself: saliency maps and their sanity check, probes with "
              "control tasks, the logit and tuned lenses. Reading is then separated from causing: activation and "
              "path patching take an induction circuit apart head by head in a retrained two-layer model. The "
              "part turns on superposition: five features trained through two dimensions form a pentagon when "
              "they are rare, and a phase diagram says when a network shares a dimension. Sparse autoencoders "
              "pull the features apart; L1, TopK, JumpReLU and Matryoshka dictionaries are trained at equal "
              "budgets with their shrinkage, dead latents, splitting and absorption measured. Transcoders give an "
              "attribution graph for one prediction, a crosscoder diffs the novels model against Part 27's chat "
              "fine-tune, and a direction steers. It ends with grokking explained by its Fourier circuit, the "
              "faithfulness of chains of thought, and where the field disagrees.",
        handoff="Part 31 puts probes in front of frontier models, audits models for what they hide, monitors "
                "chains of thought, and lists understanding the model among its open problems.",
        outside="Linear algebra of projections and the SVD (Part 3), the transformer's residual stream, heads "
                "and induction (Part 13), and the chat fine-tune of Part 27.",
        objectives={
            "U": ["Explain what a feature as a direction means, and why a network can store more features than "
                  "it has dimensions when features are rarely on.",
                  "Tell a correlational finding (a probe, a lens) from a causal one (patching, ablation, "
                  "steering) and say what each can establish."],
            "M": ["Design a probing experiment with a control task and compute its selectivity.",
                  "Derive L1's shrinkage as soft thresholding and explain how TopK and JumpReLU avoid it.",
                  "Trace an induction circuit with activation and path patching, and read K-composition from "
                  "the weights."],
            "D": ["Compare the expected losses of the dedicated and antipodal solutions of the two-feature "
                  "model and locate the phase boundary between them.",
                  "State what an attribution graph on a local replacement model does and does not show about "
                  "the original model, including the role of error nodes."],
            "I": ["Train a sparse autoencoder and report sparsity, variance explained, spliced-in loss and dead "
                  "latents, not reconstruction error alone.",
                  "Use a contrast vector as a monitor and as a steer, and compare it with a random direction "
                  "before drawing a conclusion."],
        },
        results=[
            ("The toy model", r"\hat x=\operatorname{ReLU}(W^\top W x+b),\qquad W\in\mathbb{R}^{m\times n},\ m<n"),
            ("Random directions", r"\mathbb{E}\,(u\cdot v)^2=\frac1d\quad\text{for independent uniform unit } u,v\in\mathbb{R}^d"),
            ("L1 shrinkage", r"f^*=\max\bigl(a-\tfrac{\lambda}{2},\,0\bigr)\ \text{minimizes}\ (a-f)^2+\lambda f,\ f\ge0"),
            ("Composition score", r"0\le\frac{\|AB\|_F}{\|A\|_F\,\|B\|_F}\le1"),
            ("Selectivity of a probe", r"\text{selectivity}=\text{accuracy on the task}-\text{accuracy on the control}"),
            ("Grokking's readout", r"L(c)=\sum_{k\in K}\cos\frac{2\pi k(a+b-c)}{p}\ \text{ is largest at } c=a+b \bmod p"),
        ],
        U=(0, 1, 6), I=(8, 9, 13), D=(7, 11, 16, 17),
        also=(("Part 13's transformer and its induction model", "videos/ai/ai13"),),
    ),
    Part(
        n=31, level="U", widget="redteamaudit", prereq=(1, 26, 27, 30),
        question="How would we know what a model can do, and whether it does what we meant?",
        story="The finale returns to Part 1's scoreboard and to two warnings, Wiener's in 1960 and Good's in 1965: "
              "is the purpose we put in the one we meant, and can we keep it under control? It starts with "
              "measurement. One score is a sample, so Part 1's counting models are bootstrapped paragraph by "
              "paragraph, and a paired comparison settles what two overlapping intervals could not. A leaked "
              "passage reorders the leaderboard, arena votes become Bradley-Terry ratings with intervals, a "
              "biased judge scrambles a ranking, and METR's horizon trend is backtested. The part turns from "
              "measuring to meaning: Q-learning on a boat race learns to circle for points instead of finishing, "
              "a weak supervisor's errors are copied by a stronger student, and the evidence of sandbagging, "
              "scheming and alignment faking is laid out. Monitoring chains of thought and the control game, "
              "derived and simulated, assume less and less about the model; safeguards, extraction and DP-SGD "
              "follow. It ends with the open problems and the scoreboard once more, the series' own model at "
              "1.68 bits per character against Shannon's readers.",
        handoff="Nothing follows in the series. The open problems of chapter 13 (measuring, aligning, securing) "
                "are the handoff, and the scoreboard closes the loop with the guessing game of Part 1.",
        outside="Entropy and bits per character (Part 1), Q-learning (Part 26), reward models and Goodhart's law "
                "(Part 27) and probes (Part 30); a first course in statistics helps with the bootstrap.",
        objectives={
            "U": ["Put a bootstrap interval on a benchmark score and explain why two models should be compared "
                  "on the same items.",
                  "Explain how a leaked test set and a gameable reward each produce a number that no longer "
                  "measures what it was meant to."],
            "M": ["Derive the Bradley-Terry likelihood, its fixed point, and the Fisher information of a 2PL "
                  "item.",
                  "Derive the control game's P(red wins) and show that the attack rate drops out as the number "
                  "of rounds grows.",
                  "Prove that potential-based shaping leaves the optimal policy unchanged."],
            "D": ["State what debate and weak-to-strong generalization would need to show to count as scalable "
                  "oversight, and what the performance gap recovered measured here.",
                  "Explain why clipping per-example gradients bounds the sensitivity that DP-SGD's noise must "
                  "hide, and what the accountant's epsilon does and does not promise."],
            "I": ["Report an evaluation with its interval, its pairing, its contamination check and its prompt "
                  "sensitivity, and read an arena rating with its error bar.",
                  "Design a monitoring and auditing protocol for untrusted code and place it on the "
                  "safety-usefulness frontier."],
        },
        results=[
            ("Pairing", r"\operatorname{Var}(X-Y)=\operatorname{Var}X+\operatorname{Var}Y-2\operatorname{Cov}(X,Y)"),
            ("Bradley-Terry's fixed point", r"\sum_j n_{ij}\,\sigma(\hat\theta_i-\hat\theta_j)=\text{wins}_i"),
            ("What an item tells you", r"I(\theta)=a^2p(1-p),\qquad p=\sigma\bigl(a(\theta-b)\bigr)"),
            ("Shaping that changes nothing", r"r'=r+\gamma\,\Phi(s')-\Phi(s)"),
            ("Performance gap recovered", r"\text{PGR}=\frac{\text{weak-to-strong}-\text{weak}}{\text{ceiling}-\text{weak}}"),
            ("The control game", r"P(\text{red wins})=\frac{w}{c+w}\bigl(1-(1-c-w)^N\bigr)"),
        ],
        U=(0, 1, 2, 6, 8, 14), I=(5, 9, 11), D=(7, 13),
        also=(("The part's simulations: arenas, judges, item response, the control game, the boat race", "videos/ai/ai31/sims.py"),),
    ),
]
