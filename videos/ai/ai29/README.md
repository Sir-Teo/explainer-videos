# AI, Built — Part 29: Agents and Worlds

Part 29 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). What it takes to act over many steps in a world you only partly see: from Shakey
and the DARPA races to today's coding and computer-use agents; beliefs and POMDPs; the agent loop with its tools,
protocols and memory; why errors compound and how fast agents' horizons are growing; imitation learning, behaviour
cloning's T²ε and DAgger; world models from Ha and Schmidhuber to Dreamer, Genie and V-JEPA; sim-to-real and domain
randomization; and vision-language-action models up to π0, FAST, π0.5 and the 2026 robot foundation models.
Everything that is trained here is trained on this computer, on the CPU, and replayed on screen; every other number
is cited, and company claims are labelled as such.

## Outline

* **Many steps in a row (hook).** 0.97³⁰; sixty simulated runs of a thirty-step task; the objectives.
* **1. From Shakey to agents.** SRI's Shakey (1966–72; Nilsson, Rosen; A*, STRIPS, the Hough transform); the DARPA
  Grand Challenges (2004: no finisher, Sandstorm about 7 of ~142 miles; 2005: five finishers, Stanley under 7 hours,
  self-supervised road detection; 2007 Urban Challenge, Boss); ALVINN (1989), Levine et al. (2016), Dactyl (2019),
  SayCan and RT-1 (2022); WebGPT (2021), ReAct (2022), Toolformer and function calling (2023), SWE-agent, computer use
  and MCP (2024), terminal coding agents (2025).
* **2. Acting without seeing everything.** POMDP definition card; Åström (1965); a robot localizing itself in a
  corridor of 40 cells and 4 doors, its belief predicted and corrected step by step; the belief update derived (Bayes,
  total probability, normalization) and shown to be Part 7's forward algorithm; the belief MDP (Kaelbling, Littman &
  Cassandra 1998); a language-model agent's context as its belief.
* **3. The agent loop.** ReAct (Yao et al. 2022: +34 and +10 points on ALFWorld and WebShop from one or two
  examples); a real trace from our simulated warehouse agent (real tools, scripted model with set error rates);
  Toolformer (Schick et al. 2023); function calling with JSON schemas (OpenAI, June 2023); the Model Context Protocol
  (Anthropic, November 2024), the Agentic AI Foundation (Linux Foundation, December 2025, with AGENTS.md and goose;
  over 10,000 MCP servers), Google's A2A.
* **4. Memory, and many agents.** The context window as working memory; compaction; MemGPT (2023); lost in the
  middle (Liu et al. 2023); retrieval memory with embeddings (Part 24); Generative Agents (Park et al. 2023),
  Reflexion (Shinn et al. 2023), Voyager (Wang et al. 2023: 3.3× unique items, milestones up to 15.3× faster);
  orchestrator and subagents; Anthropic's multi-agent research system (June 2025, a company report: +90.2% on an
  internal evaluation, ~15× the tokens of a chat, token usage explaining 80% of BrowseComp variance).
* **5. Compounding error.** pⁿ; the warehouse agent in its head, with tools (errors it can see are retried), and
  checking its work, 3,000 simulated tasks per point, each set falling on its own pⁿ; the half-time horizon
  n½ = ln 2 / (−ln p) ≈ 0.69 / (1 − p), derived.
* **6. Horizons that double.** METR's 50% time horizon (Kwa et al. 2025): tasks timed by people, a logistic fit per
  model (schematic); METR's Time Horizon 1.1 measurements, 2019–2026, refitted here (doubling time since 2023 with a
  bootstrap; since 2019); the 80% horizons against a constant-hazard model (t₅₀/t₈₀ = ln 2/ln 1.25 = 3.1) and their
  own doubling; the 16-hour reliability ceiling, Claude Mythos Preview's ~17 h, the page no longer updated
  (September 2026); METR's developer trial (Becker et al. 2025). Forecasting and its caveats are Part 31's.
* **7. Coding agents.** SWE-bench (Jimenez et al. 2023/24: 2,294 issues, 12 repositories, Claude 2 at 1.96%), an
  astropy issue as the example; SWE-agent's agent–computer interface (12.5% against 3.8%); SWE-bench Verified (OpenAI,
  August 2024: 500 problems, GPT-4o 33.2%); OpenAI's February 2026 audit (59.4% of 138 problems flawed; contamination
  evidence; a company's own audit) and SWE-Bench Pro (Scale AI, September 2025: 1,865 problems, 41 repositories) with
  Scale's public leaderboard (retrieved 29 October 2026); Terminal-Bench (2025; 2.0: 89 tasks, under 65%; 4.0 in
  2026) and Anthropic's 66.4% for Claude Opus 5.5 (September 2026, a company claim).
* **8. Using a computer.** Screenshots in, mouse and keyboard out; computer use (Anthropic, October 2024) and Operator
  (OpenAI, January 2025); OSWorld (Xie et al. 2024: 369 tasks, people 72.36%, best model 12.24%) and the companies'
  reported scores since (14.9%, 38.1%, 61.4%); OSWorld 2.0 (2026: 108 workflows, median 1.6 human hours, ~318 tool
  calls a task, best binary score 20.6%); Anthropic's 81.8% partial credit on 2.1 (a company claim); prompt
  injection.
* **9. Learning by imitation.** ALVINN; behaviour cloning defined; a windy lane solved exactly (the expert never
  leaves it; the learner sees a noisy camera); the cloned policy and the readings it never saw; its drives; the
  T²ε bound derived (Ross & Bagnell 2010); the measured cost against horizon, 8 seeds, against T²ε and Tε.
* **10. DAgger.** The algorithm (Ross, Gordon & Bagnell 2011); DAgger replayed round by round on the lane (the
  learner's table filling in, its drives, its cost); the no-regret reduction and the uTε_N bound; BC against DAgger at
  equal numbers of expert labels (8 seeds), and against the label budget; HG-DAgger (Kelly et al. 2019) and on-policy
  distillation (Part 27) as DAgger.
* **11. World models.** Dyna (Sutton 1990), Schmidhuber's recurrent world models, Ha & Schmidhuber (2018: V, M, C;
  906 on CarRacing; VizDoom in the dream), MuZero (Part 26); a small world model trained here on a bouncing ball
  (encoder to 8 numbers, learned dynamics, decoder), its dreams at checkpoints during training, imagination against
  reality and the error growing with the horizon.
* **12. Dreamer: learning inside a dream.** The RSSM (deterministic h, categorical z, prior and posterior; PlaNet,
  Dreamer, DreamerV2, V3 in *Nature* 2025); the loss derived term by term, KL balancing and free bits; KL balancing
  measured on our world model (3 seeds each, equal total KL weight); symlog, with a four-game regression measured;
  learning in imagination (λ-returns, REINFORCE with a critic baseline and return normalization, entropy); our
  Dreamer-lite on a 12 × 12 game of catch from pixels (3 seeds): its dreams at checkpoints against reality, its catch
  rate against real experience, one of its real games.
* **13. Worlds you can walk through.** Genie (Bruce et al. 2024: 11B, latent actions from unlabelled platformer
  videos); Genie 2 (December 2024), Genie 3 (August 2025: 720p, 24 fps, minutes of consistency, a minute of visual
  memory, promptable events, SIMA), Project Genie (January 2026), Genie 4 (27 October 2026, Google DeepMind's
  description: native audio, Gemini-planned events, pitched for robots); Dreamer 4 (Hafner, Yan & Lillicrap 2025:
  diamonds from offline data); V-JEPA 2 and its action-conditioned planner (Assran et al. 2025; Part 24).
* **14. From simulation to reality.** Isaac Gym (2021) and walking in minutes (Rudin et al. 2022); the reality gap;
  domain randomization defined (Tobin et al. 2017; Peng et al. 2018; OpenAI's Rubik's cube 2019); our cart-pole
  (Part 26's physics): linear policies trained by the cross-entropy method in one simulator against randomized ones
  (8 seeds each, equal episodes), tested every round on a "real" cart-pole (longer, heavier pole, weaker motor, a
  delay, noisy sensors); robustness maps over pole length and motor force; one episode each; learned simulators
  (Gemini 4 Argon for Robotics and Genie 4, October 2026, company claims).
* **15. Vision-language-action models.** RT-1 (2022), RT-2 (2023: 62% against 32% on unseen objects and scenes), Open
  X-Embodiment (2023), OpenVLA (2024: 7B, 970k trajectories, +16.5 points over the 55B RT-2-X); the anatomy of a VLA
  with π0's action expert (Black et al. 2024); flow matching on action chunks, exactly; regression against flow
  matching on two-way demonstrations, trained here (5 seeds each); action chunks.
* **16. Action tokens, and robot foundation models.** Per-step binning (RT-2, OpenVLA) and why its tokens carry little;
  FAST (Pertsch et al. 2025): the DCT, rounding, BPE; tokens against reconstruction error computed on held-out
  motions; π0-FAST (about 5× faster training, the company's report); π0.5 (April 2025) and its ablation (a company
  result); Gemini Robotics and GR00T N1 (March 2025); π*0.6 and Recap (November 2025); memory for VLAs (March 2026);
  π0.7 (April 2026); Gemini 4 Argon for Robotics and the Pi API (October 2026).
* **Recap**, where it comes back (Parts 30 and 31), seven problems, Part 30's teaser, references.

Running time: about 56 minutes (silent 480p build measured by `tools/lecture_length.py ai29`).

## Running it

```
python tools/make.py ai29                       # computations, then the narrated cut in English and Chinese
python tools/make.py ai29 --silent -q l --lang en   # a quick silent preview
```

or step by step, from the repo root:

```
python -m videos.ai.ai29.compute                # everything missing (about an hour on a laptop CPU)
python -m videos.ai.ai29.compute --force lane   # one item again
python tools/build.py ai29                      # English
python tools/build.py ai29 --lang zh            # Chinese
```

Every computation is seeded. Torch uses `AI29_THREADS` threads (default 2). The two long items, `dreamer` (three
Dreamer-lite seeds) and `klbal` (six world-model runs), keep each finished run in `.cache/ai29/*.partial.json`, so an
interrupted run resumes. No multiprocessing; nothing is downloaded. The METR measurements are written into
`compute.py` from METR's published data file (`metr.org/assets/benchmark_results_1_1.yaml`, retrieved 29 October 2026).
Part 26's cart-pole equations and drawing are reused through `videos/ai/ai26/envs.py` and `common.py`.

## Results on this machine

All numbers below come from `python -m videos.ai.ai29.compute` on this machine (Linux, CPU); the narration states
them through f-strings over the cached results, so another machine's last digits flow through to what is said.

* **Hook.** 0.97³⁰ = 0.40; of 60 simulated runs of a 30-step task, 27 reach the end.
* **Belief (corridor, 40 cells, 4 doors).** Uncertainty from 5.32 bits to 0.80 bits after 40 steps; the most likely
  cell is the robot's.
* **Agent loop (simulated warehouse agent, 3,000 tasks per point).** Effective per-step reliability fitted from success
  against task length: in its head 96.3% (a slip is set at 6% a step, but two slips can cancel), ReAct with
  tools 97.9% (theory 98%), ReAct with a check 99.3% (theory 99.4%); at 60 steps: 11%, 28% and 66% of tasks right; the
  check costs 1.15 calls a step.
* **METR (Time Horizon 1.1, 26 models, refitted).** Frontier models since 2023 within the 16-hour range (14 points):
  a doubling every 129 days (bootstrap 95%: 102–155; METR's own fit: 128.7); since 2019 (17 points): 188 days (METR:
  187.8); 80% horizons double every 133 days; median t₅₀/t₈₀ = 5.1 against 3.1 for a constant hazard.
* **Behaviour cloning against DAgger (windy lane, 400 expert labels each, 8 seeds, exact expectations).** The
  learner's error on the expert's states ε = 0.085 for both. Expected steps off the lane in 400: BC 94 on average
  (seeds 17–183), DAgger 31 (17–84); expert 0. Log-log slope of J(T): BC 1.30 (steps 10–60) and 1.59 (200–400), DAgger
  1.08 and 1.29. Against the label budget (50–1,600): BC 208 → 94 and flat from 200 labels on; DAgger 208 → 17. DAgger's
  replay (seed 0): 345 → 84 by round 4. The bound J ≤ J* + T²ε is checked for every seed at T = 10, 50, 200.
* **Bouncing-ball world model.** Imagined ball 0.10 px off after 1 step, 0.88 after 5, 4.9 after 20.
* **Dreamer-lite (12 × 12 catch, RSSM from pixels, policy trained only in imagination, 3 seeds).** All three seeds
  catch 100% of the balls after 4,556 steps of real play (60 rounds of 40 updates), against 29% for a random paddle.
* **KL balancing (world model alone, 3 seeds each, equal total KL weight).** Mean wrong pixels per dreamed frame over
  30 steps: balanced 5.8, plain 5.6 — no clear difference on a world this small (balanced is better for the first few
  steps: 0.8 against 1.5 wrong pixels one step ahead).
* **symlog (one network, four games with reward scales 1 to 1,000, 3 seeds).** Relative error by game, raw squared
  error: 278%, 38%, 12%, 0.5%; after symlog: 1.9%, 1.0%, 1.2%, 0.9%.
* **Regression against flow matching (two-way demonstrations, 400 demos, chunks of 20, 5 seeds, 60 starts each).**
  Regression hits the obstacle 98% of the time (seeds 95–100%); flow matching 27% (17–38%), passing above 51% of the
  time.
* **FAST (300 held-out one-second chunks of synthetic seven-joint motion).** Per-step binning: 350 tokens, RMS error
  0.0060 rad; 46% of tokens repeat the previous one, 75% are within one bin. FAST (BPE, 600 merges): γ = 2 → 12.4
  tokens (0.108 rad), γ = 10 → 25.2 (0.029), γ = 100 → 63.4 (0.0049): at about the per-step error, 6× fewer tokens.
* **Domain randomization (cart-pole, linear policies, CEM, 8 seeds each, equal episodes).** Both kinds balance all 500
  steps in Part 26's simulator; on the "real" cart-pole (1.7× pole, 3× pole mass, 30% weaker motor, 1.6× cart, a
  one-step delay, sensor noise): single-simulator policies 97 steps on average (44–283), randomized 473 (379–500).
  Over the robustness map (pole length 0.2–1.2 m, force 4–15 N, with delay and noise), the share of cells above 400
  steps: 0% against 83%.

## Problems found and fixed while making it

* The first Dreamer-lite barely learned: the reward head could not read a one-pixel ball from the latent state. The ball
  is now drawn 2 × 2 (with the catch rule matching the drawing), and the reward head predicts a two-hot distribution
  over symlog bins (V3); all seeds then reach 100%.
* The first imitation task (a loop of road on a grid, a table policy) did not separate BC from DAgger: an arbitrary
  default action trapped the learner off the road for both. The windy lane, with a noisy camera, shows the effect the
  theory describes and is solvable exactly.
* The first two-way demonstrations used chunks of 8 moves; resampling the mode every 8 steps let flow matching wander
  into the obstacle (36%). Chunks of 20 positions relative to the current one give 27%.
* The first synthetic arm motions were so slow that a one-second chunk was almost a constant; moves are now 0.25–0.9 s.

## References

Books: S. Thrun, W. Burgard & D. Fox, *Probabilistic Robotics* (2005); R. S. Sutton & A. G. Barto, *Reinforcement
Learning: An Introduction*, 2nd ed. (2018).

* History: N. J. Nilsson (ed.), *Shakey the Robot*, SRI Technical Note 323 (1984); S. Thrun et al., *Stanley: The robot
  that won the DARPA Grand Challenge* (2006); C. Urmson et al., *Autonomous driving in urban environments: Boss and the
  Urban Challenge* (2008); D. Pomerleau, *ALVINN* (1989); S. Levine, C. Finn, T. Darrell & P. Abbeel, *End-to-end
  training of deep visuomotor policies* (2016); OpenAI et al., *Solving Rubik's Cube with a Robot Hand* (2019).
* POMDPs: K. J. Åström, *Optimal control of Markov processes with incomplete state information* (1965); L. P.
  Kaelbling, M. L. Littman & A. R. Cassandra, *Planning and acting in partially observable stochastic domains* (1998).
* Agents: R. Nakano et al., *WebGPT* (2021); S. Yao et al., *ReAct* (2022); T. Schick et al., *Toolformer* (2023);
  OpenAI, *Function calling* (13 June 2023); J. S. Park et al., *Generative Agents* (2023); N. Shinn et al.,
  *Reflexion* (2023); G. Wang et al., *Voyager* (2023); C. Packer et al., *MemGPT* (2023); N. F. Liu et al., *Lost
  in the Middle* (2023); Anthropic, *Introducing the Model Context Protocol* (25 November 2024); Linux Foundation,
  *Agentic AI Foundation* (9 December 2025); Anthropic, *How we built our multi-agent research system* (13 June 2025).
* Horizons and evaluations: T. Kwa et al. (METR), *Measuring AI Ability to Complete Long Tasks* (2025); METR, *Time
  Horizon 1.1* (metr.org, last updated 8 September 2026; data retrieved 29 October 2026); J. Becker et al. (METR),
  *Measuring the impact of early-2025 AI on experienced open-source developer productivity* (2025); C. E. Jimenez et
  al., *SWE-bench* (ICLR 2024); J. Yang et al., *SWE-agent* (2024); OpenAI, *Introducing SWE-bench Verified* (August
  2024) and *Why we no longer evaluate SWE-bench Verified* (23 February 2026; reported by Decrypt, 24 February 2026);
  X. Deng et al., *SWE-Bench Pro* (arXiv 2509.16941, 2025); Scale AI, SWE-Bench Pro public leaderboard
  (labs.scale.com, retrieved 29 October 2026); M. A. Merrill et al., *Terminal-Bench* (arXiv 2601.11868, 2026);
  tbench.ai, *Terminal-Bench 4.0*; T. Xie et al., *OSWorld* (NeurIPS 2024); *OSWorld 2.0* (osworld-v2.xlang.ai,
  arXiv 2606.29537, 2026); Anthropic, *Introducing computer use* (22 October 2024), *Claude Sonnet 4.5* (29 September
  2025), *Introducing Claude Opus 5.5* (22 September 2026); OpenAI, *Computer-Using Agent* (23 January 2025).
* Imitation: S. Ross & J. A. Bagnell, *Efficient reductions for imitation learning* (AISTATS 2010); S. Ross, G. J.
  Gordon & J. A. Bagnell, *A reduction of imitation learning and structured prediction to no-regret online learning*
  (AISTATS 2011); M. Kelly et al., *HG-DAgger* (2019).
* World models: R. S. Sutton, *Dyna* (1990); J. Schmidhuber, *Making the world differentiable* (1990); D. Ha & J.
  Schmidhuber, *World Models* (2018); D. Hafner et al., *PlaNet* (2019), *Dreamer* (2020), *DreamerV2* (2021),
  *Mastering diverse domains through world models* (DreamerV3, 2023; *Nature* 2025); D. Hafner, W. Yan & T. Lillicrap,
  *Training Agents Inside of Scalable World Models* (Dreamer 4, arXiv 2509.24527, 2025); J. Bruce et al., *Genie*
  (2024); Google DeepMind, *Genie 2* (4 December 2024), *Genie 3* (5 August 2025), *Project Genie* (29 January 2026),
  *Genie 4: A new generation of world simulation* (27 October 2026); M. Assran et al., *V-JEPA 2* (2025).
* Sim-to-real: J. Tobin et al., *Domain randomization* (2017); X. B. Peng et al., *Sim-to-real transfer of robotic
  control with dynamics randomization* (2018); V. Makoviychuk et al., *Isaac Gym* (2021); N. Rudin et al., *Learning
  to walk in minutes* (2022); Google, *Gemini 4 Argon for Robotics* (13 October 2026).
* VLAs: A. Brohan et al., *RT-1* (2022), *RT-2* (2023); Open X-Embodiment Collaboration (2023); M. J. Kim, K. Pertsch
  et al., *OpenVLA* (2024); K. Black et al., *π0* (2024); K. Pertsch et al., *FAST* (2025); Physical Intelligence,
  *π0.5* (22 April 2025), *π\*0.6* (17 November 2025), *VLAs with long and short-term memory* (3 March 2026), *π0.7*
  (16 April 2026), *Frontier models for every robot* (13 October 2026); Gemini Robotics Team (March 2025); NVIDIA,
  *GR00T N1* (March 2025).

## Problems, with solutions

1. *A robot is at a door with prior probability q. It senses a door (probability 0.9 at one, 0.05 elsewhere). Find
   the posterior, and how many consistent sightings take q = 0.1 above 0.99.* — Bayes: q' = 0.9q / (0.9q + 0.05(1 − q)).
   In odds, each sighting multiplies by the likelihood ratio 0.9/0.05 = 18. Prior odds 1/9; after k sightings 18ᵏ/9.
   Two give 36 (q = 0.973), three give 648 (q = 0.9985): three sightings.
2. *Show −ln p ≥ 1 − p, so n½ ≤ 0.69/(1 − p); compute it for p = 0.98.* — ln x ≤ x − 1 for x > 0 (the logarithm is
   concave and touches its tangent at 1); put x = p. Hence n½ = ln 2/(−ln p) ≤ ln 2/(1 − p). For p = 0.98,
   n½ = 0.6931/0.02020 = 34.3 steps (the bound gives 34.7).
3. *Prove J(π̂) ≤ J(π*) + T²ε for behaviour cloning, and build a task where it is nearly reached.* — Couple the
   learner and the expert (same randomness). Let εₜ be the learner's error rate on the expert's distribution at step
   t, ε their mean. Until the first disagreement the two trajectories coincide; the probability of a disagreement by
   step t is at most Σ_{k≤t} εₖ (union bound). With costs in [0, 1], step t costs the learner at most the expert's cost
   plus that probability, so J(π̂) − J(π*) ≤ Σₜ Σ_{k≤t} εₖ ≤ T Σₖ εₖ = T²ε. Tight case: two states, "on" and "lost";
   the expert never leaves "on"; the learner leaves with probability ε a step, and "lost" is absorbing with cost 1.
   Then J = Σₜ (1 − (1 − ε)ᵗ) ≈ T²ε/2 for Tε ≪ 1: the same order as the bound.
4. *If success on a task of length t is exp(−(t/τ)ᵏ), show t₅₀/t₈₀ = (ln 2/ln 1.25)^{1/k}; find the k that gives METR's
   median ratio; what does k < 1 mean?* — Success S at length t_S: (t_S/τ)ᵏ = −ln S, so t_S = τ(−ln S)^{1/k} and the
   ratio is (ln 2/ln 1.25)^{1/k} = 3.106^{1/k}. With the measured median ratio r, k = ln 3.106/ln r (r = 5.08 gives
   k ≈ 0.70). k < 1 is a falling hazard: the longer a task has gone well, the less likely the next minute fails —
   what a mix of easy and hard tasks produces, and why long tasks are less hopeless than a constant hazard implies.
5. *Show symlog is odd, increasing, ≈ x near 0, and that symexp inverts it.* — symlog(−x) = −sign(x) ln(1 + |x|) =
   −symlog(x); its derivative is 1/(1 + |x|) > 0; ln(1 + u) = u − u²/2 + …, so symlog(x) ≈ x for small x;
   symexp(symlog(x)) = sign(x)(e^{ln(1+|x|)} − 1) = sign(x)|x| = x.
6. *With Aᵗ = (1 − τ)ε + τA, show dAᵗ/dτ = A − ε. If demonstrations are ±m with probability ½ each, the
   squared-error-optimal deterministic action is 0.* — Differentiate the straight line. For the second part,
   E[(a − Y)²] = a² − 2aE[Y] + E[Y²] is minimized at a = E[Y] = 0: the mean of the two modes, the path through the
   obstacle. A generative policy instead samples Y.
7. *The orthonormal DCT is orthogonal; show that rounding γ·DCT(a) changes the signal by an RMS error of about
   1/(γ√12).* — Orthogonality preserves Euclidean norms (Parseval), so the error in the signal equals the error in the
   coefficients. Rounding γc to an integer leaves an error roughly uniform on [−½, ½] when |γc| is large, variance
   1/12; divided by γ, variance 1/(12γ²) per coefficient, so the RMS error per sample is 1/(γ√12) (0.029 at γ = 10, in
   the normalized units). Coefficients rounded to 0 have error |c| < 1/(2γ), usually smaller, so this is about an
   upper estimate.

## 习题与解答

1. *机器人在门前的先验概率是q。它感知到一扇门（在门前时概率0.9，别处0.05）。求后验概率；从q = 0.1出发，连续几次一致的观测能让它超过0.99？*
   —— 贝叶斯法则：q' = 0.9q / (0.9q + 0.05(1 − q))。用几率表示，每次观测乘以似然比0.9/0.05 = 18。先验几率1/9，k次之后是18ᵏ/9。
   两次得36（q = 0.973），三次得648（q = 0.9985）：需要三次。
2. *证明 −ln p ≥ 1 − p，从而 n½ ≤ 0.69/(1 − p)；计算 p = 0.98 时的值。* —— 对x > 0有ln x ≤ x − 1（对数是凹函数，在1处与切线相切）；
   取x = p。于是 n½ = ln 2/(−ln p) ≤ ln 2/(1 − p)。p = 0.98时，n½ = 0.6931/0.02020 = 34.3步（上界是34.7）。
3. *证明行为克隆满足 J(π̂) ≤ J(π*) + T²ε，并构造一个几乎达到这个界的任务。* —— 让学习者和专家共用同样的随机性。设εₜ为学习者在第t步、
   在专家分布上的错误率，ε为其平均。在第一次分歧之前，两条轨迹完全相同；到第t步为止出现分歧的概率至多是Σ_{k≤t} εₖ（联合界）。
   代价在[0, 1]之间，所以第t步学习者的代价至多是专家的代价加上这个概率，于是 J(π̂) − J(π*) ≤ Σₜ Σ_{k≤t} εₖ ≤ TΣₖ εₖ = T²ε。
   紧的例子：两个状态，“在路上”和“迷路”；专家从不离开“在路上”；学习者每步以概率ε离开，而“迷路”是吸收态，每步代价1。
   于是 J = Σₜ (1 − (1 − ε)ᵗ) ≈ T²ε/2（当Tε ≪ 1）：与上界同阶。
4. *若长度为t的任务成功率为exp(−(t/τ)ᵏ)，证明 t₅₀/t₈₀ = (ln 2/ln 1.25)^{1/k}；求出给出METR中位比值的k；k < 1意味着什么？*
   —— 成功率为S的长度满足(t_S/τ)ᵏ = −ln S，所以 t_S = τ(−ln S)^{1/k}，比值为 3.106^{1/k}。测得的中位比值为r时，
   k = ln 3.106/ln r（r = 5.08时k ≈ 0.70）。k < 1表示风险随时间下降：任务进行得越久而没出错，下一分钟出错的可能就越小——
   这正是难易混杂的一批任务会产生的结果，也说明长任务没有恒定风险所暗示的那么无望。
5. *证明symlog是奇函数、单调递增、在0附近≈x，且symexp是它的反函数。* —— symlog(−x) = −sign(x) ln(1 + |x|) = −symlog(x)；
   导数为1/(1 + |x|) > 0；ln(1 + u) = u − u²/2 + …，所以x很小时symlog(x) ≈ x；symexp(symlog(x)) = sign(x)(e^{ln(1+|x|)} − 1) = x。
6. *设Aᵗ = (1 − τ)ε + τA，证明dAᵗ/dτ = A − ε。若示范以各½的概率为±m，证明平方误差最优的确定性动作是0。* —— 对直线求导即可。
   第二问：E[(a − Y)²] = a² − 2aE[Y] + E[Y²]在a = E[Y] = 0处取最小：两个峰的平均，正是穿过障碍物的那条路。生成式策略则是对Y采样。
7. *正交归一化的DCT是正交变换；证明把γ·DCT(a)取整，信号的均方根误差约为1/(γ√12)。* —— 正交变换保持欧氏范数（帕塞瓦尔），
   所以信号的误差等于系数的误差。|γc|较大时，把γc取整留下的误差近似均匀分布在[−½, ½]上，方差1/12；除以γ，每个系数的方差为1/(12γ²)，
   所以每个样本的均方根误差为1/(γ√12)（γ = 10时为0.029，归一化单位）。被取整为0的系数误差是|c| < 1/(2γ)，通常更小，所以这大致是一个上估计。

## Glossary (terms in this part)

| English | 中文 |
|---|---|
| agent, agent loop | 智能体，智能体循环 |
| partially observable Markov decision process (POMDP) | 部分可观测马尔可夫决策过程（POMDP） |
| belief, belief update, belief MDP | 信念，信念更新，信念MDP |
| observation | 观测 |
| predict, correct (filtering); Kalman filter | 预测，修正（滤波）；卡尔曼滤波 |
| ReAct: thought, action, observation | ReAct：想法，动作，观测 |
| tool use, function calling, JSON schema | 工具使用，函数调用，JSON模式说明 |
| Model Context Protocol (MCP), server, host | 模型上下文协议（MCP），服务器，宿主应用 |
| context window, compaction | 上下文窗口，（总结式）压缩 |
| retrieval memory, skill library, reflection | 检索记忆，技能库，反思 |
| lead agent, subagent (multi-agent system) | 主智能体，子智能体（多智能体系统） |
| compounding error, horizon | 误差累积，时程 |
| half-time horizon n½ | 一半把握的时程n½ |
| time horizon (50%, 80%), doubling time | （百分之五十、百分之八十）时间跨度，倍增时间 |
| constant hazard, Weibull | 恒定风险，韦布尔分布 |
| SWE-bench, patch, fail-to-pass tests | SWE-bench，补丁，从失败到通过的测试 |
| agent–computer interface (ACI) | 智能体与计算机的接口（ACI） |
| contamination | （数据）污染 |
| computer use, screenshot, prompt injection | 电脑使用，截图，提示注入 |
| behaviour cloning, demonstration, expert | 行为克隆，示范，专家 |
| distribution shift; union bound | 分布偏移；联合界 |
| DAgger (dataset aggregation), no-regret learning | DAgger（数据集聚合），无悔学习 |
| world model, imagination, dream | 世界模型，想象，梦 |
| recurrent state-space model (RSSM), deterministic state, stochastic state | 循环状态空间模型（RSSM），确定性状态，随机状态 |
| prior, posterior; KL balancing; free bits | 先验，后验；KL平衡；自由比特 |
| symlog, symexp, two-hot target | 对称对数（symlog），symexp，双热目标 |
| λ-return, critic, return normalization | λ回报，评论家，回报归一化 |
| latent action model | 潜在动作模型 |
| reality gap, sim-to-real, domain randomization | 现实差距，从仿真到现实，域随机化 |
| cross-entropy method (CEM) | 交叉熵方法（CEM） |
| vision-language-action model (VLA), action expert | 视觉–语言–动作模型（VLA），动作专家 |
| action chunk, flow matching | 动作块，流匹配 |
| FAST action tokens, discrete cosine transform (DCT), byte-pair encoding (BPE) | FAST动作词元，离散余弦变换（DCT），字节对编码（BPE） |
| per-step binning | 逐步分箱 |
| robot foundation model, co-training, ablation | 机器人基础模型，联合训练，消融实验 |
