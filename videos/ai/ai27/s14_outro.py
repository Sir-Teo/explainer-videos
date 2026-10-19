from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ADAPT, ASSIST, GOLD, KLC, PART, POLICY, PROXY, REWARD


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.comes_back()
        self.problems()
        self.next_time()

    # ------------------------------------------------------------------
    def recap(self):
        rows = VGroup(
            label(r"supervised fine-tuning: \ maximum likelihood on the answers people want", font_size=26, color=ASSIST),
            label(r"LoRA: \ fine-tuning lives in a low-rank slice of weight space", font_size=26, color=ADAPT),
            label(r"reward models: \ Bradley--Terry on comparisons", font_size=26, color=PROXY),
            label(r"RLHF: \ $\pi^* \propto \pi_{\mathrm{ref}}\, e^{r/\beta}$, \ reached by sampling", font_size=26,
                  color=POLICY),
            label(r"Goodhart: \ the harder you optimize a learned reward, \ the more it lies", font_size=26, color=GOLD),
            label(r"DPO: \ the same optimum, \ fitted from comparisons directly", font_size=26, color=POLICY),
            label(r"constitutions, \ distillation, \ merging", font_size=26, color=KLC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(UP * 0.1)
        with self.voiceover(
            "Let's take stock. Supervised fine-tuning is maximum likelihood on the answers people want, and it can "
            "live in a low-rank slice of weight space, which is why LoRA works. A reward model learns people's "
            "preferences from comparisons with the Bradley-Terry model. Reinforcement learning with a KL leash aims "
            "at an exact optimum, the reference model reweighted by the exponential of the reward. Push a learned "
            "reward too hard and it stops measuring what it was meant to: Goodhart's law, which we measured. DPO "
            "reaches the same optimum straight from the comparisons. And written principles, distillation and model "
            "merging make all of this cheaper."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in rows], lag_ratio=0.5),
                      run_time=vo.remaining() * 0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def comes_back(self):
        rows = VGroup(
            label(r"Part 28: \ reinforcement learning on answers that can be checked: \ GRPO, \ reasoning",
                  font_size=26, color=POLICY),
            label(r"Part 29: \ agents trained to act over long tasks", font_size=26, color=ASSIST),
            label(r"Part 30: \ persona vectors and the inside of the model", font_size=26, color=PROXY),
            label(r"Part 31: \ can we trust what post-training produces?", font_size=26, color=GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.2)
        with self.voiceover(
            "All of this comes back. Part 28 trains models to reason, with reinforcement learning on answers that "
            "can be checked. Part 29 trains agents that act over long tasks. Part 30 opens the model up, persona "
            "vectors included. And Part 31 asks whether we can trust what post-training produces."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in rows], lag_ratio=0.5),
                      run_time=vo.remaining() * 0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Show that the Bradley--Terry likelihood of a set of comparisons is unchanged if a constant $c(x)$ is "
            r"added to $r(x, y)$ for every answer $y$ to a question $x$.",
            r"Prove that $\pi^* \propto \pi_{\mathrm{ref}}\, e^{r/\beta}$ maximizes $\mathbb E_\pi[r] - \beta\, "
            r"\mathrm{KL}(\pi \,\|\, \pi_{\mathrm{ref}})$, \ and that the maximum is $\beta \log Z$.",
            r"Show that best-of-$n$ sampling has $\mathrm{KL}(\pi_{\mathrm{BoN}} \,\|\, \pi_{\mathrm{ref}}) = \log n - "
            r"(n-1)/n$ when the reward has no ties.",
            r"Compute the gradient of the DPO loss for one pair, \ and show that it is weighted by "
            r"$\sigma(\hat r_l - \hat r_w)$, \ where $\hat r = \beta \log \pi_\theta / \pi_{\mathrm{ref}}$.",
            r"A LoRA adapter of rank $r$ on a $d \times k$ matrix has $r(d + k)$ parameters. \ For $d = k = 4096$, at "
            r"what rank does it have as many as the matrix?",
            r"Fit a Gaussian $q$ to any density $p$ by minimizing $\mathrm{KL}(p \,\|\, q)$. \ Show that $q$ has "
            r"the mean and variance of $p$.",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems to try, from the Bradley-Terry model to the forward KL. Pause here, and work "
            "through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 28, \ Reasoning", font_size=40).to_edge(UP, buff=0.5)
        body = VGroup(
            label(r"thinking out loud is computing", font_size=28, color=ASSIST),
            label(r"reinforcement learning on checkable answers: \ GRPO, \ derived", font_size=28, color=POLICY),
            label(r"how much longer thinking buys", font_size=28, color=GOLD),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.2)
        thanks = label(r"Thanks for watching.", font_size=30, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Next time: reasoning. Why writing out steps adds computation, how a model learns from a checker instead "
            "of a person, with GRPO derived, and what thinking longer buys. The best place to go deeper on this part "
            "is Nathan Lambert's free book on reinforcement learning from human feedback. Thanks for watching, and "
            "see you in Part 28."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in body], lag_ratio=0.4))
            self.play(FadeIn(thanks))
        self.wait(0.5)
        self.clear_scene()
