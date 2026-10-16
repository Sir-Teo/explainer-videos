"""Scene order for the final cut: (module, Scene class, chapter title)."""

TITLE = "Reinforcement Learning for Language Models, Derived: From the Policy Gradient to GRPO"

SCENES = [
    ("s01_hook", "Hook", "Learning from a single bit"),
    ("s02_policy", "Policy", "Part 1: A language model is a policy"),
    ("s03_gradient", "LogDerivative", "The log-derivative trick"),
    ("s04_baseline", "Baselines", "Baselines: same mean, less noise"),
    ("s05_credit", "Credit", "Credit assignment: values, TD errors, GAE"),
    ("s06_trust", "TrustRegions", "Part 2: Importance sampling and trust regions"),
    ("s07_ppo", "PPO", "PPO: the clipped objective"),
    ("s08_preferences", "Preferences", "Part 3: Rewards from preferences"),
    ("s09_kl", "KLOptimum", "The KL leash and its exact optimum"),
    ("s10_dpo", "DPO", "DPO: the reward hiding in the policy"),
    ("s11_grpo", "GRPO", "Part 4: GRPO: the group is the baseline"),
    ("s12_run", "RealRun", "A real run: what RL actually changed"),
    ("s13_biases", "Biases", "Hidden biases: lengths and averages"),
    ("s14_entropy", "Entropy", "Entropy: the exploration budget"),
    ("s15_sharpen", "Sharpening", "Sharpening or discovery?"),
    ("s16_mismatch", "Mismatch", "Part 5: When the sampler and the learner disagree"),
    ("s17_scale", "Scaling", "Scaling RL: compute, environments, reward hacking"),
    ("s18_outro", "Outro", "The whole family, one equation at a time"),
]
