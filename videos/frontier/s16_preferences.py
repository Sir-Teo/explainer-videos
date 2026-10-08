from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import Plot, label, load, mono_lines, note, source


class Preferences(VoiceoverScene):
    def construct(self):
        self.compare()
        self.reward_model()
        self.rlhf()
        self.goodhart()
        self.dpo()

    # ------------------------------------------------------------------
    def compare(self):
        prompt = label(r"``Explain why the sky is blue to a ten-year-old.''", font_size=30, color=C.USER).to_edge(UP, buff=0.8)
        a = mono_lines("Sunlight is made of all colors. Tiny bits of air bounce blue light around much more than red "
                       "light, so blue comes at us from every direction of the sky.", width=36, font_size=20)
        b = mono_lines("Rayleigh scattering: intensity scales as the inverse fourth power of wavelength, so shorter "
                       "wavelengths dominate the diffuse skylight spectrum.", width=36, font_size=20)
        boxes = VGroup()
        for t, name in [(a, "A"), (b, "B")]:
            hdr = label(rf"answer {name}", font_size=24, color=GREY_A)
            g = VGroup(hdr, t).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            boxes.add(VGroup(SurroundingRectangle(g, buff=0.25, color=GREY_B, corner_radius=0.1), g))
        boxes.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.2)
        pick = SurroundingRectangle(boxes[0], buff=0.08, color=C.REWARD, corner_radius=0.12, stroke_width=4)
        tick = label(r"preferred", font_size=28, color=C.REWARD).next_to(pick, DOWN, buff=0.15)
        tag = note(r"illustrative example").to_corner(UR, buff=0.3)
        with self.voiceover(
            "Imitation only goes so far. For many qualities, it's far easier to judge an answer than to write a "
            "perfect one. So the next stage learns from comparisons: <bookmark mark='s'/> show a person two responses "
            "to the same prompt, <bookmark mark='p'/> and ask which one is better."
        ) as vo:
            self.play(FadeIn(prompt), FadeIn(tag))
            vo.wait_until("s")
            self.play(FadeIn(boxes, lag_ratio=0.3))
            vo.wait_until("p")
            self.play(Create(pick), FadeIn(tick))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reward_model(self):
        plot = Plot(x_range=(-5, 5), y_range=(0, 1), width=6.5, height=3.6, x_ticks=[-4, -2, 0, 2, 4], y_ticks=[0, 0.5, 1],
                    x_label=r"$r_A - r_B$ (difference in reward scores)", y_label=r"$P(\text{person prefers } A)$")
        plot.move_to(RIGHT * 2.6 + DOWN * 0.6)
        xs = np.linspace(-5, 5, 200)
        curve = plot.line(xs, 1 / (1 + np.exp(-xs)), color=C.REWARD, stroke_width=4)
        bt = MathTex(r"P(A \succ B) = \sigma(r_A - r_B) = \frac{1}{1 + e^{-(r_A - r_B)}}", font_size=36).to_edge(UP, buff=0.6)
        rm = VGroup(
            RoundedRectangle(width=3.0, height=1.4, corner_radius=0.15, stroke_color=C.EDU, fill_color=C.EDU, fill_opacity=0.12),
            label(r"reward model", font_size=28),
        )
        rm[1].move_to(rm[0])
        rm.move_to(LEFT * 4.2 + DOWN * 0.3)
        inp = label(r"prompt $+$ answer", font_size=24, color=GREY_A).next_to(rm, UP, buff=0.35)
        out = MathTex(r"r", font_size=44, color=C.EDU).next_to(rm, DOWN, buff=0.4)
        a1 = Arrow(inp.get_bottom(), rm.get_top(), buff=0.08, stroke_width=3, color=GREY_B)
        a2 = Arrow(rm.get_bottom(), out.get_top(), buff=0.08, stroke_width=3, color=C.EDU)
        sub = label(r"(a language model with one number as output)", font_size=22, color=GREY_B).next_to(out, DOWN, buff=0.2)
        src = source(r"Bradley \& Terry (1952); Ouyang et al.\ 2022 (InstructGPT)")
        with self.voiceover(
            "Those choices train a reward model: a copy of the language model whose output is a single number, a "
            "score. <bookmark mark='b'/> It's trained so that the probability a person prefers answer A over answer B "
            "is the sigmoid of the difference between their scores. That's the Bradley-Terry model, from 1952."
        ) as vo:
            self.play(FadeIn(rm), FadeIn(inp), GrowArrow(a1), GrowArrow(a2), FadeIn(out), FadeIn(sub))
            vo.wait_until("b")
            self.play(FadeIn(bt), FadeIn(plot), FadeIn(src))
            self.play(Create(curve), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rlhf(self):
        k = 6
        names = [f"answer {i + 1}" for i in range(k)]
        ref = np.array([0.22, 0.25, 0.2, 0.15, 0.1, 0.08])
        rew = np.array([0.2, -0.5, 1.0, 0.1, 1.5, -1.0])
        beta = 0.7
        pol = ref * np.exp(rew / beta)
        pol /= pol.sum()
        bw = 0.7
        base_y = -1.6

        def bars(p, color, dx, opacity):
            return VGroup(*[Rectangle(width=bw * 0.42, height=max(0.02, 9 * v), stroke_width=0, fill_color=color,
                                      fill_opacity=opacity).move_to([(i - (k - 1) / 2) * 1.5 + dx, base_y + 4.5 * v, 0])
                            for i, v in enumerate(p)])
        r0 = bars(ref, C.REFERENCE, -0.16, 0.7)
        r1 = bars(pol, C.RL_POLICY, 0.16, 0.9)
        axis = Line([-4.8, base_y, 0], [4.8, base_y, 0], color=GREY_C)
        nl = VGroup(*[label(n, font_size=20, color=GREY_A).move_to([(i - (k - 1) / 2) * 1.5, base_y - 0.3, 0]) for i, n in enumerate(names)])
        rl = VGroup(*[MathTex(rf"r={v:+.1f}", font_size=24, color=C.REWARD if v > 0 else C.PENALTY).move_to([(i - (k - 1) / 2) * 1.5, base_y - 0.7, 0])
                      for i, v in enumerate(rew)])
        obj = MathTex(r"\max_\pi\; \mathbb{E}\big[\, r \,\big] \;-\; \beta\, \mathrm{KL}\big(\pi \,\|\, \pi_{\text{ref}}\big)",
                      font_size=40).to_edge(UP, buff=0.5)
        obj[0][-12:].set_color(C.COMM)
        key = VGroup(VGroup(Square(0.22, stroke_width=0, fill_color=C.REFERENCE, fill_opacity=0.7), label(r"the fine-tuned model it started from", font_size=22)).arrange(RIGHT, buff=0.12),
                     VGroup(Square(0.22, stroke_width=0, fill_color=C.RL_POLICY, fill_opacity=0.9), label(r"after RL: more probability on high-reward answers", font_size=22)).arrange(RIGHT, buff=0.12)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(obj, DOWN, buff=0.3)
        tag = note(r"schematic").to_corner(UR, buff=0.3)
        with self.voiceover(
            "Then comes reinforcement learning. The model writes answers, the reward model scores them, and the "
            "model is nudged toward the answers that score higher, <bookmark mark='k'/> with one constraint: a penalty "
            "for drifting too far from the fine-tuned model it started from, measured by the KL divergence. This is "
            "RLHF, reinforcement learning from human feedback: the recipe behind InstructGPT and the first ChatGPT."
        ) as vo:
            self.play(FadeIn(tag), Create(axis), FadeIn(nl), FadeIn(rl), FadeIn(r0), FadeIn(key[0]))
            self.play(FadeIn(r1, shift=UP * 0.1), FadeIn(key[1]), run_time=1.2)
            vo.wait_until("k")
            self.play(FadeIn(obj))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def goodhart(self):
        d = load("goodhart")
        x = np.sqrt(d["kl"])
        gold, proxy = d["gold"], d["proxy"]
        k = int(np.argmax(gold))
        assert 20 < d["n"][k] < 100 and gold[-1] < 0.5 * gold[k] and proxy[-1] > 10
        plot = Plot(x_range=(0, 3.2), y_range=(0, 3.5), width=8.0, height=4.4, x_ticks=[0, 1, 2, 3], y_ticks=[0, 1, 2, 3],
                    x_label=r"how far the policy has moved: $\sqrt{\mathrm{KL}}$", y_label=r"reward")
        plot.move_to(LEFT * 1.6 + DOWN * 0.4)
        m = x <= 3.2
        top = 3.5
        inside = m & (proxy <= top)
        j = int(np.argmax(proxy > top))  # first point above the chart
        x_exit = x[j - 1] + (x[j] - x[j - 1]) * (top - proxy[j - 1]) / (proxy[j] - proxy[j - 1])
        pl = plot.line(list(x[inside]) + [x_exit], list(proxy[inside]) + [top], color=C.EDU, stroke_width=4)
        up = Arrow(plot.c2p(x_exit, top - 0.35), plot.c2p(x_exit, top) + UP * 0.45, buff=0, color=C.EDU, stroke_width=4)
        gl = plot.line(x[m], gold[m], color=C.REWARD, stroke_width=4)
        pk = Dot(plot.c2p(x[k], gold[k]), radius=0.08, color=C.REWARD)
        lp = label(r"what the reward model thinks (keeps rising)", font_size=24, color=C.EDU).next_to(up, RIGHT, buff=0.15)
        lg = label(r"true quality", font_size=26, color=C.REWARD).next_to(plot.c2p(x[m][-1], gold[m][-1]), DOWN, buff=0.25).shift(LEFT * 0.6)
        head = label(r"Goodhart's law, simulated: best of $n$ answers, chosen by a noisy reward model", font_size=30).to_edge(UP, buff=0.4)
        side = VGroup(
            label(r"true quality $g \sim \mathcal{N}(0,1)$", font_size=24),
            label(r"reward model sees $g + \varepsilon$", font_size=24),
            label(r"(heavy-tailed error $\varepsilon$)", font_size=22, color=GREY_A),
            label(rf"peak at $n \approx {int(d['n'][k])}$", font_size=24, color=C.REWARD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(plot, RIGHT, buff=0.4).shift(UP * 0.6)
        src = source(r"simulation; the same shape as Gao, Schulman \& Hilton, \emph{Scaling Laws for Reward Model Overoptimization} (2022)")
        with self.voiceover(
            "The leash matters, because the reward model is only a proxy for what people want. Here's a simulation. "
            "Each candidate answer has a true quality, and the reward model sees that quality plus some error. "
            "<bookmark mark='s'/> Pick the best of n answers by the reward model's score. At first, true quality "
            "climbs. <bookmark mark='f'/> But push harder, and you start selecting the answers whose errors were "
            "biggest: the proxy reward keeps rising while the true quality falls. That's Goodhart's law, and OpenAI "
            "measured exactly this shape with real reward models in 2022."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(side[:3]), FadeIn(src))
            vo.wait_until("s")
            self.play(Create(pl), Create(gl), run_time=2.5)
            self.play(GrowArrow(up), FadeIn(lp), FadeIn(lg))
            vo.wait_until("f")
            self.play(FadeIn(pk, scale=2), FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dpo(self):
        loss = MathTex(r"\mathcal{L}_{\text{DPO}} = -\log \sigma\Big(",
                       r"\beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)}",
                       r"\;-\;",
                       r"\beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)}",
                       r"\Big)", font_size=40)
        loss[1].set_color(C.REWARD)
        loss[3].set_color(C.PENALTY)
        loss.move_to(UP * 1.0)
        bw = Brace(loss[1], DOWN, color=C.REWARD)
        lw = label(r"preferred answer: raise,\\relative to the reference", font_size=24, color=C.REWARD).next_to(bw, DOWN, buff=0.1)
        bl = Brace(loss[3], DOWN, color=C.PENALTY)
        ll = label(r"rejected answer: lower", font_size=24, color=C.PENALTY).next_to(bl, DOWN, buff=0.1)
        head = label(r"Direct Preference Optimization (2023): no reward model, no RL loop", font_size=34).to_edge(UP, buff=0.5)
        foot = VGroup(
            label(r"standard in open pipelines: T\"ulu 3, OLMo 3, \dots", font_size=26, color=GREY_A),
            label(r"Constitutional AI: comparisons judged by a model, against written principles", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.7)
        src = source(r"Rafailov et al.\ 2023; Bai et al.\ 2022 (Constitutional AI)")
        with self.voiceover(
            "In 2023, Direct Preference Optimization showed you can skip the reward model and the RL loop "
            "altogether. A bit of algebra turns the same objective into a simple loss on each pair: "
            "<bookmark mark='w'/> raise the probability of the preferred answer, relative to the reference model, "
            "<bookmark mark='l'/> and lower the rejected one. <bookmark mark='o'/> DPO and its variants are now "
            "standard in open post-training pipelines. And the comparisons don't have to come from people: with "
            "constitutional AI, a model judges responses against a written list of principles."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(Write(loss), run_time=2.0)
            vo.wait_until("w")
            self.play(GrowFromCenter(bw), FadeIn(lw))
            vo.wait_until("l")
            self.play(GrowFromCenter(bl), FadeIn(ll))
            vo.wait_until("o")
            self.play(FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()
