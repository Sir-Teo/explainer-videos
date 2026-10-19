# AI, Built — Part 26: Reinforcement Learning, from Bellman to AlphaZero

Part 26 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)); the first part of Act V, Agency. How to learn to act when nobody gives the right
action, only how it turned out: from Thorndike's law of effect and Bellman's equation, through temporal differences,
Q-learning, DQN, policy gradients and PPO, to search, AlphaGo, AlphaZero, MuZero, and games of hidden information.
Every learner here is trained on this computer, and its training is replayed on screen: the cliff walk's values and
paths, DQN's and PPO's cart-pole policies, and our own AlphaZero for Connect Four, graded move by move against a
perfect solver.

* **The move nobody would play.** AlphaGo against Lee Sedol, game 2, move 37, from the game record; AlphaGo Zero.
* **1. Learning from consequences.** Thorndike (1911); the agent–environment loop; Markov decision processes
  (Bellman 1957); returns, discounting, the bound r_max / (1 − γ) and the recursion G_t = r_{t+1} + γ G_{t+1};
  policies, V and Q; credit assignment, exploration, non-stationary data.
* **2. Explore or exploit.** k-armed bandits (Thompson 1933); greedy against ε-greedy on the 10-armed testbed;
  regret = Σ Δ_a E[N_a]; UCB derived from Hoeffding; UCB1's O(log T) regret and the Lai–Robbins lower bound; UCB run
  live on five arms; Thompson sampling; regret on two coins over 50,000 pulls.
* **3. Bellman's equation.** Derived from the recursion and the Markov property; backup diagrams; a slippery
  gridworld; the linear solve V = (I − γP_π)^{-1} r_π; the optimality equation and the greedy policy.
* **4. Why value iteration works.** Value iteration sweep by sweep; the Bellman operator is a γ-contraction (proved);
  Banach's fixed-point theorem; two starts converging; policy iteration (Howard 1960) and the policy improvement
  theorem; generalized policy iteration; state counts from 44 to 2.08 × 10^170.
* **5. Temporal differences.** Monte Carlo against TD(0) (Sutton 1988, Samuel 1959); the random walk replayed; RMS
  error over episodes; n-step returns, TD(λ) and eligibility traces; TD-Gammon (Tesauro 1992); dopamine and the TD
  error (Schultz, Dayan & Montague 1997).
* **6. Q-learning.** Sarsa and Q-learning (Watkins 1989); convergence (Watkins & Dayan 1992); the cliff walk's
  training replayed for both; on- against off-policy; the deadly triad (Baird 1995).
* **7. Deep Q-networks.** DQN on Atari (Mnih et al. 2013, 2015); replay and target networks; DQN's training on the
  cart-pole replayed (greedy action over angle × angular velocity, the pole balancing at each checkpoint); the
  ablation; overestimation (Jensen), double Q-learning; Rainbow, Agent57.
* **8. Policy gradients.** The log-derivative trick and REINFORCE (Williams 1992), derived; baselines are unbiased
  (proved) and halve the variance here (measured); actor–critic, advantages, GAE; the curves.
* **9. Trust regions and PPO.** Why step size matters; the importance-sampled surrogate; TRPO; PPO's clip, plotted;
  PPO's training replayed; OpenAI Five, soft actor-critic, RLHF, GRPO.
* **10. Search before learning.** Minimax and alpha–beta on a tree; node counts on Connect Four (37.5 million for
  minimax at depth 9, 36,594 for well-ordered alpha–beta); Knuth & Moore; Deep Blue (1997); why Go resisted.
* **11. Monte Carlo tree search.** Random playouts (Brügmann 1993); select, expand, simulate, back up; UCT (Kocsis &
  Szepesvári 2006); a real tree growing; the solver's verdict (plain MCTS picks a losing move here); MCTS strength
  against simulations; Crazy Stone and MoGo.
* **12. AlphaGo.** Move 37; the four networks (Silver et al. 2016); search with priors and a value network; Fan
  Hui, Lee Sedol, move 78 of game 4.
* **13. Learning from zero.** AlphaGo Zero and AlphaZero (2017–18); the self-play loop and its loss; MCTS as policy
  improvement; our own AlphaZero for Connect Four: its prior on one position across every generation, how often
  its move keeps the win or the draw, with and without search, Elo ratings, and games at successive generations.
* **14. Planning with a learned model.** MuZero (2019–20): representation, dynamics, prediction, value equivalence;
  EfficientZero, Gumbel MuZero, video compression.
* **15. Beyond perfect information.** Information sets and Nash equilibria; regret matching on rock-paper-scissors
  (current against average strategy); CFR on Kuhn poker (exploitability, the value −1/18); Cepheus, Libratus,
  Pluribus; AlphaStar's league; adversarial policies against KataGo; AlphaTensor and AlphaDev.
* **Recap**, where it comes back, the problem set, Part 27's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai26.alphazero        # AlphaZero for Connect Four: about 2-3 hours on 4 cores (resumable)
python -m videos.ai.ai26.compute          # everything else (about an hour)
python tools/build.py ai26                # English
python tools/build.py ai26 --lang zh      # Chinese
```

`c4.py` is Connect Four on bitboards with a perfect solver (negamax, alpha–beta, a transposition table and
null-window search, after Pascal Pons), checked against brute force on random endgames; `envs.py` holds the
gridworld, cliff walk, random walk and cart-pole.

References: Sutton & Barto (2018); Lattimore & Szepesvári (2020); Bertsekas & Tsitsiklis (1996); Thorndike (1911);
Bellman (1957); Howard (1960); Thompson (1933); Lai & Robbins (1985); Auer, Cesa-Bianchi & Fischer (2002); Sutton
(1988); Watkins & Dayan (1992); Williams (1992); Tesauro (1995); Schultz, Dayan & Montague (1997); Baird (1995); Mnih
et al. (2015); van Hasselt, Guez & Silver (2016); Hessel et al. (2018); Badia et al. (2020); Schulman et al. (2015,
2016, 2017); Haarnoja et al. (2018); Berner et al. (2019); Knuth & Moore (1975); Campbell, Hoane & Hsu (2002); Allis
(1994); Brügmann (1993); Coulom (2006); Kocsis & Szepesvári (2006); Silver et al. (2016, 2017, 2018); Anthony, Tian &
Barber (2017); Schrittwieser et al. (2020); Ye et al. (2021); Danihelka et al. (2022); Mandhane et al. (2022); Hart &
Mas-Colell (2000); Zinkevich et al. (2007); Bowling et al. (2015); Brown & Sandholm (2017, 2019); Vinyals et al.
(2019); Wang et al. (2023); Fawzi et al. (2022); Mankowitz et al. (2023).

## Problems, with solutions

**1. The UCB bonus.** For rewards in [0, 1], show that the true mean exceeds μ̂_a + √(2 ln t / n_a) with probability at
most t^{-4}.

*Solution.* Hoeffding's inequality for the average of n independent rewards in [0, 1] gives
P(μ_a − μ̂_a ≥ ε) ≤ exp(−2nε²). With ε = √(2 ln t / n), 2nε² = 4 ln t, so the bound is exp(−4 ln t) = t^{-4}.

**2. A contraction.** Show that the Bellman operator T^π of a fixed policy is a γ-contraction in the max norm, and that
V^π is its only fixed point.

*Solution.* (T^π V)(s) = Σ_a π(a|s) Σ_{s'} P(s'|s,a)[r(s,a) + γV(s')]. The rewards cancel in a difference:
|(T^π V)(s) − (T^π U)(s)| = γ |Σ_a π(a|s) Σ_{s'} P(s'|s,a)(V(s') − U(s'))| ≤ γ Σ_a π(a|s) Σ_{s'} P(s'|s,a) ‖V − U‖_∞
= γ ‖V − U‖_∞, since the weights are nonnegative and sum to one. If V and U are both fixed points,
‖V − U‖_∞ = ‖T^π V − T^π U‖_∞ ≤ γ ‖V − U‖_∞ with γ < 1, so ‖V − U‖_∞ = 0. V^π is a fixed point by the Bellman
equation, so it is the only one (and Banach's theorem gives one exists, since ℝ^n is complete).

**3. The random walk, exactly.** Solve the Bellman equations of the five-state walk.

*Solution.* With no discount and rewards only at the exits, V(k) = ½ V(k−1) + ½ V(k+1) for k = 1, …, 5, with
V(0) = 0 (leaving left pays nothing) and V(6) = 1 (leaving right pays one). Second differences vanish, so V is linear
in k: V(k) = k/6, that is 1/6, 2/6, 3/6, 4/6, 5/6 for A to E.

**4. Baselines.** Show that a baseline b(s) leaves the policy gradient unbiased, and find the variance-minimizing
constant baseline for (G − b) ∇log π.

*Solution.* E_{a∼π}[b(s) ∇log π(a|s)] = b(s) Σ_a π(a|s) ∇log π(a|s) = b(s) Σ_a ∇π(a|s) = b(s) ∇ Σ_a π(a|s) = b(s) ∇1 = 0.
For a constant b and g = ∇log π, the mean doesn't depend on b, so minimize E[(G − b)² ‖g‖²]: its derivative in b is
−2 E[(G − b)‖g‖²] = 0, so b* = E[G ‖g‖²] / E[‖g‖²], a return average weighted by the squared size of the score.

**5. PPO's clip.** For Â > 0, show that the gradient of the clipped objective is zero once ρ > 1 + ε. What about Â < 0?

*Solution.* The objective is min(ρÂ, clip(ρ, 1−ε, 1+ε)Â). For Â > 0 and ρ > 1 + ε, the clipped term is (1+ε)Â < ρÂ, so
the minimum is (1+ε)Â, a constant: zero gradient, no incentive to raise the probability further. For Â < 0 and
ρ < 1 − ε, the clipped term (1−ε)Â is smaller than ρÂ, so the minimum is the constant (1−ε)Â: no incentive to lower
it further. But for Â < 0 and ρ > 1 + ε, ρÂ < (1+ε)Â, the minimum is the unclipped ρÂ and its gradient pushes ρ back
down: a step that made a bad action more likely is never clipped away.

**6. No regret gives equilibrium.** In a two-player zero-sum game, if both players' average regrets are at most ε,
their average strategies form a 2ε-Nash equilibrium.

*Solution.* Let player 1 maximize xᵀAy, let x_t, y_t be the strategies played and x̄, ȳ their averages, and
v̄ = (1/T) Σ_t x_tᵀ A y_t. Player 1's average regret: max_x xᵀAȳ − v̄ ≤ ε. Player 2's: v̄ − min_y x̄ᵀAy ≤ ε. So for every x,
xᵀAȳ ≤ v̄ + ε ≤ min_y x̄ᵀAy + 2ε ≤ x̄ᵀAȳ + 2ε: player 1 gains at most 2ε by deviating; and for every y,
x̄ᵀAy ≥ min_y x̄ᵀAy ≥ v̄ − ε ≥ max_x xᵀAȳ − 2ε ≥ x̄ᵀAȳ − 2ε: player 2 gains at most 2ε. That is a 2ε-equilibrium.

## 习题与解答

**1. UCB的加分。** 奖励在[0, 1]之内时，证明真实均值超过 μ̂_a + √(2 ln t / n_a) 的概率至多为 t^{-4}。

*解答。* 对n个取值在[0, 1]的独立奖励的平均值，霍夫丁不等式给出 P(μ_a − μ̂_a ≥ ε) ≤ exp(−2nε²)。取
ε = √(2 ln t / n)，则 2nε² = 4 ln t，上界为 exp(−4 ln t) = t^{-4}。

**2. 压缩映射。** 证明固定策略的贝尔曼算子 T^π 在最大范数下是γ-压缩，并由此说明 V^π 是它唯一的不动点。

*解答。* 两个值表之差中奖励相互抵消：|(T^π V)(s) − (T^π U)(s)| = γ|Σ_a π Σ_{s'} P (V − U)(s')| ≤ γ‖V − U‖_∞，因为权重非负
且和为1。若V、U都是不动点，则 ‖V − U‖_∞ ≤ γ‖V − U‖_∞，而γ < 1，所以两者相等。V^π满足贝尔曼方程，因而就是那个唯一的不动点。

**3. 随机游走的精确解。** 解出五状态随机游走的贝尔曼方程。

*解答。* 不打折、只有出口有奖励时，V(k) = ½V(k−1) + ½V(k+1)，k = 1,…,5，边界 V(0) = 0、V(6) = 1。二阶差分为零，
所以V关于k是线性的：V(k) = k/6，即A到E依次为1/6、2/6、3/6、4/6、5/6。

**4. 基线。** 证明基线b(s)不改变策略梯度的期望，并求使 (G − b)∇log π 方差最小的常数基线。

*解答。* E_{a∼π}[b ∇log π] = b Σ_a ∇π = b ∇Σ_a π = b ∇1 = 0。常数b不影响均值，只需最小化 E[(G − b)²‖g‖²]（g = ∇log π）：
对b求导令其为零，得 b* = E[G‖g‖²] / E[‖g‖²]，即以得分函数长度平方加权的回报平均。

**5. PPO的裁剪。** 优势为正时，证明 ρ > 1 + ε 之后裁剪目标的梯度为零。优势为负时呢？

*解答。* 目标为 min(ρÂ, clip(ρ, 1−ε, 1+ε)Â)。Â > 0 且 ρ > 1+ε 时，裁剪项 (1+ε)Â 小于 ρÂ，最小值为常数，梯度为零。
Â < 0 且 ρ < 1−ε 时，最小值是常数 (1−ε)Â，同样不再推动。但 Â < 0 且 ρ > 1+ε 时，ρÂ 更小，取的是未裁剪项，梯度把ρ
往回拉：让坏动作变得更可能的那一步，永远不会被裁剪掉。

**6. 无悔即均衡。** 在二人零和博弈中，若双方的平均遗憾都不超过ε，则双方的平均策略构成2ε-纳什均衡。

*解答。* 记玩家1最大化 xᵀAy，平均策略为 x̄、ȳ，平均收益 v̄ = (1/T)Σ x_tᵀAy_t。由玩家1的遗憾：max_x xᵀAȳ ≤ v̄ + ε；
由玩家2的遗憾：min_y x̄ᵀAy ≥ v̄ − ε。于是对任意x，xᵀAȳ ≤ v̄ + ε ≤ min_y x̄ᵀAy + 2ε ≤ x̄ᵀAȳ + 2ε；对任意y，
x̄ᵀAy ≥ v̄ − ε ≥ max_x xᵀAȳ − 2ε ≥ x̄ᵀAȳ − 2ε。任何一方单独偏离至多获益2ε，即2ε-均衡。
