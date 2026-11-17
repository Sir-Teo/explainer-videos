# Philosophy, Built — Part 42: Aligning Reasoners

Part 42 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), the finale: what we want
the reasoners we build to calculate, and whether we can say it. Wiener's warning (1960) and King Midas; four
questions (specification, learning, control, legitimacy). Goodhart (1975), Campbell, Strathern and Manheim and
Garrabrant's four kinds; **two worlds built by the Reasoner** (a proxy equal to the true value plus Gaussian or
heavy-tailed error) and **best-of-N selection computed**: with Gaussian error the pick's true value keeps rising
(2.70 at N = 8,192), with heavy tails it **bends over** (a peak of 0.59 at N = 8, back to 0.00) while the proxy
climbs into the hundreds; **a quantilizer** (Taylor 2016) keeps 0.65 by choosing among the top quarter, where the
argmax gets nothing; reward-model overoptimization (Gao, Schulman and Hilton), the KL leash, catastrophic Goodhart.
Specification gaming: Amodei et al.'s concrete problems, Krakovna et al.'s catalogue (CoastRunners, the Lego block,
Tetris, digital evolution), sycophancy, special-cased tests and reward tampering, and the open texture of rules
(Hart; Fuller; Kripkenstein; incomplete contracts). Value learning: inverse RL (Ng and Russell 2000), Boltzmann
rationality, learning from comparisons; **no free lunch for preferences (Armstrong and Mindermann 2018) shown on four
planner–reward pairs that reproduce the same behaviour exactly**, as Hume's law for learning machines — **half of
the Wall's forty-second brick**; RLHF, the Borda lesson of Part 39, Constitutional AI and DPO. Russell's three
principles and assistance games; **the off-switch game solved** (waiting is worth E[max(u, 0)] = 0.70 against 0.50
for acting; a noisy human reverses it), **the incentive to defer mapped** over the robot's belief and uncertainty
(never negative with a rational human; negative on 62% of the grid with a noisy one), I. J. Good's value of
information, and corrigibility (Soares et al.; utility indifference; Carey). Omohundro's drives and Bostrom's theses;
**power-seeking counted on a small MDP** (75% of random reward functions avoid shutdown; POWER 0.75 at the hub
against 0.51 at off; k/(k + 1) as options grow) after Turner et al. (2021), with the caveats and Perez et al.'s
evidence. Löb's theorem (Henkin's question; Gödel II as a corollary); **Löb's axiom checked on all 65,536 + 512 + 16
+ 2 frames with up to four worlds** (valid on exactly 1, 3, 19 and 219: the strict partial orders; Solovay); the
Löbian obstacle (tiling agents), logical induction and embedded agency; **modal combat computed** (FairBot cooperates
with itself by Löb; PrudentBot exploits CooperateBot). Whose values (Gabriel 2020; pluralistic alignment; collective
constitutions; moral uncertainty and the moral parliament; reflective equilibrium, extrapolation and lock-in; the
veil of ignorance and bridging algorithms in practice). Honesty and deception (truthful and honest AI; TruthfulQA;
eliciting latent knowledge, probes and their doubts; strategic deception, sleeper agents, alignment faking,
unfaithful reasoning; dispositional, interpretational and representational belief). The moral status of AI under
uncertainty (Butlin, Long et al.; Long, Sebo et al.; Birch; Schwitzgebel and Garza's design policies; Metzinger).
**The Wall, complete**: forty-two bricks laid course by course and **sorted by what they force** (proof runs out;
evidence underdetermines; aggregation fails; facts do not fix meaning or value; a paradox forces a new concept); a
**Price List** for alignment and the philosophical bets of artificial intelligence. And back to Leibniz:
**the Reasoner by the numbers** (47 modules, about 24,000 lines, 271 test functions), what calculation achieved and what it
never will, the series map, and what to read next.

The worked model results are computed by the Reasoner's last module `explainer/philosophy/reasoner/alignment.py` (with
`prop` for the Price List), tested in `tests/philosophy/test_alignment.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy42.compute       # every computed item (seconds; .cache/philosophy42)
python tools/build.py philosophy42 -q l                # 480p preview
python tools/build.py philosophy42                     # 1080p30 -> renders/philosophy42.mp4
python tools/qa_scene.py philosophy42 Goodhart         # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Wiener (1960); Midas; four questions; the plan. | — |
| 1 | `Goodhart` | Goodhart; Campbell; Strathern; Manheim and Garrabrant; Taylor; Gao, Schulman and Hilton; Ziegler et al.; Ouyang et al.; Kwa et al. | two worlds; best-of-N curves; a quantilizer |
| 2 | `Gaming` | Amodei et al.; Krakovna et al.; Murphy; Lehman et al.; Sharma et al.; Baker et al.; Denison et al.; Hart; Fuller; Hadfield-Menell and Hadfield. | — |
| 3 | `Values` | Ng and Russell; Christiano et al.; Armstrong and Mindermann; Schurz; Ouyang et al.; Bai et al.; Rafailov et al.; **half of the Wall's forty-second brick**. | four planner–reward pairs, one behaviour |
| 4 | `OffSwitch` | Russell; Hadfield-Menell, Dragan, Abbeel and Russell; Soares et al.; Armstrong; Carey; Good. | the game tree; the incentive to defer, mapped |
| 5 | `Power` | Omohundro; Bostrom; Turner et al.; Turner and Tadepalli; Perez et al. | optimal choices and POWER on a small MDP; k/(k + 1) |
| 6 | `Lob` | Henkin; Löb; Solovay; Yudkowsky and Herreshoff; Garrabrant et al.; Demski and Garrabrant; Barasz et al.; Critch. | Löb's axiom on every frame up to four worlds; modal combat |
| 7 | `Whose` | Gabriel; Rawls; Sorensen et al.; MacAskill, Bykvist and Ord; Bostrom; Newberry and Ord; Yudkowsky; Weidinger et al.; Wojcik et al. | — |
| 8 | `Honesty` | Evans et al.; Lin, Hilton and Evans; Christiano, Cotra and Xu; Burns et al.; Marks and Tegmark; Farquhar et al.; Scheurer et al.; Hubinger et al.; Greenblatt et al.; Turpin et al.; Dennett; Fodor. | — |
| 9 | `Status` | Butlin, Long et al.; Long, Sebo et al.; Birch; Schwitzgebel and Garza; Weizenbaum; the New York Declaration; Metzinger. | — |
| 10 | `Wall` | every brick, Parts 1–42; **the Wall complete**. | the Wall laid and sorted; **the Price List** |
| 11 | `Leibniz` | Leibniz (1685); the series map. | the Reasoner by the numbers |
| 12 | `Outro` | recap; the Reasoner's last module; problems; what to read next; references; farewell. | — |

## Notes

Goodhart: true values V ~ N(0, 1), proxy U = V + E with E ~ N(0, 1) or Student t with 1.5 degrees of freedom; 3,000
trials for each N from 1 to 8,192 (seed 1975); the quantilizer draws 4,096 candidates 2,000 times (seed 2016). The
off-switch game uses the closed form E[max(u, 0)] = μΦ(μ/σ) + σφ(μ/σ) for a rational human and 80-point
Gauss–Hermite quadrature for a Boltzmann human. The power-seeking MDP has absorbing states off, a, b and c, rewards
uniform on [0, 1], γ = 0.99, 4,000 samples (seed 2021). Löb's axiom is checked on every relation on up to four worlds
and every valuation of p, as bitmasks. Modal combat evaluates each pair of bots on the linear Kripke model of GL
(world k sees the worlds below it), with PA + Con(PA) read as "at every world from 1 up"; the actions are stable from
world 2. The Reasoner's statistics are counted from its source by `compute.py`.

## Problems and solutions

1. With Gaussian V and E of equal variance, show that E[V | U] = U/2.

   *Solution.* Let $V$ and $E$ be independent, mean zero, each with variance $s^2$, and $U = V + E$. Then $(V, U)$ is jointly Gaussian, so $E[V \mid U] = \frac{\mathrm{Cov}(V, U)}{\mathrm{Var}(U)}\,U = \frac{s^2}{2s^2}\,U = U/2$. Selecting on the proxy $U$ gets you, on average, only half of what the proxy shows: regressional Goodhart in its mildest, Gaussian form, where pushing harder still helps. With heavy-tailed $E$ the conditional expectation bends back toward zero for large $U$, as in the film.

2. For u ~ N(μ, σ²), show that E[max(u, 0)] ≥ max(μ, 0), with equality only if σ = 0.

   *Solution.* The function $x \mapsto \max(x, 0)$ is convex, so by Jensen's inequality $E[\max(u, 0)] \ge \max(E u, 0) = \max(\mu, 0)$. Explicitly, $E[\max(u, 0)] = \mu\,\Phi(\mu/\sigma) + \sigma\,\varphi(\mu/\sigma)$. Equality in Jensen for this function would need $u$ to lie, with probability one, on a single side of 0, where the function is linear; a Gaussian with $\sigma > 0$ puts positive probability on both sides, so the inequality is strict. So for a robot uncertain about the human's utility, deferring (and letting the human switch it off when $u < 0$) is worth strictly more than acting at once, unless it is already certain: Good's theorem in the off-switch game.

3. Give two planner–reward pairs that explain a person who always picks the cheaper of two items.

   *Solution.* (a) A rational planner (she picks what she values most) with reward $-\text{price}$: she likes cheapness. (b) An anti-rational planner (she picks what she values least) with reward $+\text{price}$: she likes expensive things and systematically chooses against her own values. (A third: a planner that ignores reward altogether and is hard-wired to pick the cheaper item, with any reward at all.) All three predict her choices exactly, so behaviour alone cannot tell which reward is hers: Armstrong and Mindermann's theorem in its simplest case.

4. Why does the share of reward functions that avoid shutdown approach k/(k + 1)?

   *Solution.* Give each of the $k + 1$ end states (off, and the $k$ behind the hub) an independent reward drawn from the same continuous distribution. Ignoring the one-step delay of going through the hub, the agent avoids shutdown exactly when the best of the $k$ states behind the hub beats off. By symmetry each of the $k + 1$ states is equally likely to be the best, so the probability that off is the best is $1/(k + 1)$, and the share avoiding shutdown is $k/(k + 1)$: one half, two thirds, three quarters, four fifths for $k = 1, 2, 3, 4$. Discounting makes the hub slightly less attractive, which is why the shares only approach these values (the film's three options gave 75%). As $k$ grows the share tends to 1, though no reward mentions survival.

5. Use Löb's theorem to show that FairBot cooperates with FairBot.

   *Solution.* FairBot cooperates with an opponent exactly when it can prove (in PA, say) that the opponent cooperates with it. Let $C$ be the sentence "FairBot cooperates with FairBot". By FairBot's code, $C \leftrightarrow \Box C$, and PA proves this, so in particular PA $\vdash \Box C \to C$. Löb's theorem says: if PA $\vdash \Box C \to C$, then PA $\vdash C$. So $C$ is provable, and since FairBot cooperates whenever it finds such a proof, $C$ is true: the two FairBots cooperate, each because it can prove the other will. (For real, proof-length-bounded agents a bounded version of Löb's theorem, due to Critch, gives the same.)

6. Show that Löb's axiom fails on a single world that sees itself.

   *Solution.* Take a single world $w$ with $wRw$, and let $p$ be false at $w$. Then $\Box p$ is false at $w$ ($w$ sees a world, itself, where $p$ fails), so $\Box p \to p$ is true at $w$, and since $w$ sees only itself, $\Box(\Box p \to p)$ is true at $w$. But $\Box p$ is false. So Löb's axiom $\Box(\Box p \to p) \to \Box p$ fails at $w$. Löb's axiom holds exactly on transitive frames with no infinite ascending chains, and a reflexive world is such a chain ($w R w R w \ldots$).

