from __future__ import annotations

from explainer import *  # noqa: F403
from videos.rl.common import label


class Outro(VoiceoverScene):
    def construct(self):
        steps = [
            (r"REINFORCE", r"R\,\nabla \log \pi_\theta(y)", r"the log-derivative trick", C.SCORE),
            (r"+ baseline", r"(R - b)\,\nabla \log \pi_\theta(y)", r"same mean, less noise", C.BASELINE),
            (r"+ critic, GAE", r"\textstyle\sum_t \hat A_t\,\nabla \log \pi_\theta(y_t \mid s_t)", r"credit for each token", C.BASELINE),
            (r"PPO", r"\min\big(\rho_t \hat A_t,\ \operatorname{clip}(\rho_t)\hat A_t\big)", r"reuse samples, safely", C.RATIO),
            (r"KL leash", r"\pi^\star \propto \pi_{\text{ref}}\, e^{r/\beta}", r"the exact optimum $\Rightarrow$ DPO", C.KL),
            (r"GRPO", r"\hat A_i = \frac{R_i - \operatorname{mean}(R)}{\operatorname{std}(R)}", r"the group is the baseline", C.ADVANTAGE),
            (r"DAPO, Dr.\ GRPO", r"\frac{1}{\sum_i |o_i|}\textstyle\sum_{i,t}\ \ \text{or}\ \ \frac{1}{G L}\sum_{i,t}", r"remove the length bias", C.LENGTH),
            (r"GSPO, CISPO, TIS", r"\big(\tfrac{\pi_\theta(y)}{\pi_{\text{old}}(y)}\big)^{1/|y|},\ \ \operatorname{sg}[\min(\rho, C)]", r"tame the ratios at scale", C.OLD_POLICY),
            (r"On-policy distillation", r"r_t = -\log\frac{\pi_\theta(y_t \mid s_t)}{\pi_{\text{teacher}}(y_t \mid s_t)}", r"a reward for every token", C.REWARD),
        ]
        rows = VGroup()
        for name, tex, why_, col in steps:
            n = label(name, font_size=26, color=col)
            m = MathTex(tex, font_size=30)
            w = label(why_, font_size=22, color=GREY_A)
            rows.add(VGroup(n, m, w))
        for i, r in enumerate(rows):
            y = 3.25 - i * 0.78
            r[0].move_to([-4.9, y, 0])
            r[1].move_to([0.4, y, 0])
            if r[1].width > 6.0:
                r[1].width = 6.0
            r[2].move_to([5.2, y, 0])
        with self.voiceover(
            "Let's put the whole family in one place. It all starts from one identity: the gradient of an expected "
            "reward is the expected reward times the score. <bookmark mark='b'/> Subtract a baseline, and the noise "
            "falls while the mean stays put. <bookmark mark='c'/> Learn a value function, and each token gets its "
            "own credit. <bookmark mark='p'/> Reweight old samples by an importance ratio and clip it, and you can "
            "reuse every batch safely: that's PPO. <bookmark mark='k'/> Add a leash to the reference, and the optimal "
            "policy has a closed form, which hands you DPO. <bookmark mark='g'/> Replace the critic with a group of "
            "samples, and you have GRPO. <bookmark mark='l'/> Fix how it averages over tokens, <bookmark mark='s'/> "
            "tame its ratios when sampler and learner disagree, <bookmark mark='d'/> and if you have a better model "
            "to learn from, give every token its own reward."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for k, mark in enumerate(["b", "c", "p", "k", "g", "l", "s", "d"]):
                vo.wait_until(mark)
                self.play(FadeIn(rows[k + 1], shift=DOWN * 0.1), run_time=0.8)
        with self.voiceover(
            "Every one of these is the log-derivative trick, plus one idea about noise or about trust. A model "
            "samples, a checker says one or zero, and those single bits, multiplied across millions of attempts, "
            "add up to a model that reasons far more reliably."
        ):
            self.play(rows.animate.set_opacity(0.35), run_time=1.0)
            self.play(rows[0][0].animate.set_opacity(1.0), rows[0][2].animate.set_opacity(1.0),
                      rows[0][1].animate.set_opacity(1.0).scale(1.3).set_color(C.SCORE), run_time=1.0)
        self.wait(0.6)
        thanks = label(r"Every chart labeled \emph{real run} was computed on the 4-core CPU that rendered this video", font_size=28, color=GREY_A)
        self.play(FadeOut(rows), FadeIn(thanks))
        self.wait(2.0)
        self.play(FadeOut(thanks))
