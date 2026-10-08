from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import Plot, calc, label, load, mono_lines, note, num_table, source


class Preferences(VoiceoverScene):
    def construct(self):
        self.compare()
        self.reward_model()
        self.rm_math()
        self.rlhf()
        self.goodhart()
        self.dpo()
        self.dpo_math()

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
    def rm_math(self):
        ra, rb = 1.3, 0.4  # illustrative scores

        def sig(z):
            return 1 / (1 + np.exp(-z))
        m = ra - rb
        p, L, g = sig(m), -np.log(sig(m)), 1 - sig(m)
        assert round(p, 3) == 0.711 and round(L, 3) == 0.341 and round(g, 3) == 0.289
        assert round(-np.log(sig(3.0)), 3) == 0.049 and round(1 - sig(3.0), 3) == 0.047
        head = label(r"Training the reward model on one comparison", font_size=34).to_edge(UP, buff=0.4)
        sc = VGroup(*[VGroup(label(rf"answer {n}", font_size=28, color=GREY_A), MathTex(rf"r_{n} = {v}", font_size=40, color=c)
                             ).arrange(DOWN, buff=0.12) for n, v, c in [("A", ra, C.REWARD), ("B", rb, C.PENALTY)]])
        sc.arrange(RIGHT, buff=0.8)
        nums = calc(r"P(A \succ B) &= \sigma(1.3 - 0.4) = \frac{1}{1 + e^{-0.9}} = 0.711",
                    r"\\ \mathcal{L} &= -\log \sigma(r_A - r_B) = -\log 0.711 = 0.341",
                    r"\\ \frac{\partial \mathcal{L}}{\partial r_A} &= -\big(1 - \sigma(0.9)\big) = -0.289",
                    r"\\ \frac{\partial \mathcal{L}}{\partial r_B} &= +\big(1 - \sigma(0.9)\big) = +0.289",
                    r"\\ \text{gap } 3: \ \mathcal{L} &= 0.049, \ \text{slope } {-0.047}", font_size=32)
        nums[4].set_color(GREY_A)
        left = VGroup(sc, nums).arrange(DOWN, buff=0.6, aligned_edge=LEFT).next_to(head, DOWN, buff=0.6).to_edge(LEFT, buff=0.6)
        plot = Plot(x_range=(-3, 4), y_range=(0, 3.5), width=4.4, height=3.6, x_ticks=[-2, 0, 2, 4], y_ticks=[0, 1, 2, 3],
                    x_label=r"gap $r_A - r_B$", y_label=r"loss $-\log\sigma$", font_size=22)
        plot.to_edge(RIGHT, buff=0.5).align_to(nums, UP).shift(DOWN * 0.2)
        xs = np.linspace(-3, 4, 200)
        curve = plot.line(xs, -np.log(sig(xs)), color=C.LOSS, stroke_width=4)
        d1 = Dot(plot.c2p(m, L), radius=0.08, color=C.REWARD)
        d2 = Dot(plot.c2p(3.0, -np.log(sig(3.0))), radius=0.08, color=GREY_A)
        tx = np.array([m - 1.2, m + 1.2])
        tan = plot.line(tx, L - g * (tx - m), color=C.REWARD, stroke_width=3)
        shift = note(r"only the gap matters: add 10 to both scores and nothing changes").to_edge(DOWN, buff=0.35)
        tag = note(r"illustrative scores").to_corner(UR, buff=0.3)
        with self.voiceover(
            "Here's one comparison with numbers. Say the reward model scores answer A at 1.3 and answer B at 0.4. "
            "<bookmark mark='p'/> Then it predicts that a person prefers A with probability sigma of 0.9: 71 percent. "
            "<bookmark mark='l'/> The loss is minus the log of that probability, 0.34. <bookmark mark='g'/> Its slope "
            "with respect to A's score is minus 0.29, and with respect to B's, plus 0.29: each step raises A's score "
            "and lowers B's by the same amount. <bookmark mark='c'/> Once a pair is ranked confidently, say with a gap "
            "of 3, the loss is 0.05 and the push shrinks to 0.05 too: the training effort goes to the comparisons the "
            "model still gets wrong. <bookmark mark='s'/> And only the gap matters: add ten to every score, and "
            "nothing changes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(sc, lag_ratio=0.3))
            vo.wait_until("p")
            self.play(Write(nums[0]))
            vo.wait_until("l")
            self.play(Write(nums[1]), FadeIn(plot), Create(curve))
            self.play(FadeIn(d1, scale=2))
            vo.wait_until("g")
            self.play(Write(nums[2:4]), Create(tan))
            vo.wait_until("c")
            self.play(Write(nums[4]), FadeIn(d2, scale=2))
            vo.wait_until("s")
            self.play(FadeIn(shift))
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

    # ------------------------------------------------------------------
    def dpo_math(self):
        beta = 0.1
        lp = {"w": (-41.2, -43.2), "l": (-38.5, -37.5)}  # (policy, reference) sequence log-probs, illustrative
        ratio = {k: round(a - b, 1) for k, (a, b) in lp.items()}
        rhat = {k: beta * v for k, v in ratio.items()}
        z = rhat["w"] - rhat["l"]
        sz = 1 / (1 + np.exp(-z))
        assert ratio == {"w": 2.0, "l": -1.0} and round(z, 2) == 0.30
        assert round(sz, 3) == 0.574 and round(-np.log(sz), 3) == 0.554 and round(np.log(2), 3) == 0.693
        assert lp["l"][0] > lp["w"][0]  # the rejected answer is still the likelier one in absolute terms
        head = label(r"DPO on one pair, in numbers", font_size=34).to_edge(UP, buff=0.4)
        seq = MathTex(r"\log \pi(y \mid x) = \sum_{t} \log \pi(y_t \mid x, y_{<t})", font_size=36, color=GREY_A)
        seq.next_to(head, DOWN, buff=0.4)
        tab = num_table([r"", r"\log \pi_\theta", r"\log \pi_{\text{ref}}", r"\text{log-ratio}", r"\hat r = \beta \times \text{ratio}"],
                        [[r"y_w", "-41.2", "-43.2", "+2.0", "+0.20"],
                         [r"y_l", "-38.5", "-37.5", "-1.0", "-0.10"]], font_size=38, h_buff=0.8, v_buff=0.3)
        tab.rows[0][0].set_color(C.REWARD)
        tab.rows[1][0].set_color(C.PENALTY)
        tab.next_to(seq, DOWN, buff=0.55)
        nums = calc(r"z &= \beta\big[(+2.0) - (-1.0)\big] = 0.1 \times 3.0 = 0.30",
                    r"\\ \mathcal{L}_{\text{DPO}} &= -\log \sigma(0.30) = -\log 0.574 = 0.554",
                    r"\\ \text{step } 0\ (\pi_\theta = \pi_{\text{ref}}): \ \mathcal{L}_{\text{DPO}} &= -\log \sigma(0) = \log 2 = 0.693",
                    font_size=36)
        nums[2].set_color(GREY_A)
        nums.next_to(tab, DOWN, buff=0.6)
        box = SurroundingRectangle(VGroup(tab.rows[0][1], tab.rows[1][1]), buff=0.1, color=C.HIGHLIGHT, corner_radius=0.08)
        tag = note(r"illustrative log-probabilities, $\beta = 0.1$").to_corner(UR, buff=0.3)
        with self.voiceover(
            "Here's DPO on one pair. Each log-probability is a sum over the answer's tokens: the same per-token "
            "numbers as in fine-tuning. <bookmark mark='r'/> Compared with the reference model, the policy has raised "
            "the log-probability of the preferred answer by 2, and lowered the rejected one by 1. Times beta, 0.1, "
            "those are implicit rewards: 0.2, and minus 0.1. <bookmark mark='z'/> Their gap, 0.3, goes into the same "
            "Bradley-Terry loss as the reward model: minus log sigma of 0.3, which is 0.554. <bookmark mark='s'/> "
            "Every pair starts at log 2, 0.693, because at step zero the policy is the reference. "
            "<bookmark mark='a'/> And notice: the rejected answer is still the more likely one, in absolute terms. "
            "DPO doesn't care. Only the ratios to the reference count."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(seq))
            self.play(FadeIn(tab.header), Create(tab.rule), FadeIn(VGroup(*[VGroup(*r[:3]) for r in tab.rows])))
            vo.wait_until("r")
            self.play(FadeIn(VGroup(*[r[3] for r in tab.rows]), shift=LEFT * 0.1))
            self.play(FadeIn(VGroup(*[r[4] for r in tab.rows]), shift=LEFT * 0.1))
            vo.wait_until("z")
            self.play(Write(nums[0]))
            self.play(Write(nums[1]))
            vo.wait_until("s")
            self.play(Write(nums[2]))
            vo.wait_until("a")
            self.play(Create(box))
        self.wait(0.4)
        self.clear_scene()
