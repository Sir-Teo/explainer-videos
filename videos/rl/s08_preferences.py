from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import Plot, exact_tag, label, mono_lines, mtex, note, part_card, schematic_tag, source


def gumbel_pdf(x):
    return np.exp(-(x + np.exp(-x)))


def logistic_pdf(x):
    return np.exp(-x) / (1 + np.exp(-x)) ** 2


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class Preferences(VoiceoverScene):
    def construct(self):
        self.card()
        self.compare()
        self.gumbel()
        self.likelihood()
        self.proxy()

    def card(self):
        c = part_card(3, r"Learning what people want", r"reward models, the KL leash, DPO")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def compare(self):
        prompt = label(r"``Explain why the sky is blue to a ten-year-old.''", font_size=30, color=C.USER).to_edge(UP, buff=0.7)
        a = mono_lines("Sunlight is all the colors mixed. Air bounces blue light around much more than red, so "
                       "blue reaches your eyes from every part of the sky.", width=34, font_size=20)
        b = mono_lines("Rayleigh scattering: intensity scales as the inverse fourth power of wavelength, so short "
                       "wavelengths dominate the diffuse sky spectrum.", width=34, font_size=20)
        boxes = VGroup()
        for t, name in [(a, "A"), (b, "B")]:
            hdr = label(rf"answer {name}", font_size=24, color=GREY_A)
            g = VGroup(hdr, t).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            boxes.add(VGroup(SurroundingRectangle(g, buff=0.25, color=GREY_B, corner_radius=0.1), g))
        boxes.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.1)
        pick = SurroundingRectangle(boxes[0], buff=0.08, color=C.REWARD, corner_radius=0.12, stroke_width=4)
        tick = label(r"preferred", font_size=28, color=C.REWARD).next_to(pick, DOWN, buff=0.15)
        q = label(r"no checker can grade this, but a person can compare", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Arithmetic has a checker. Helpfulness, clarity and tone don't. But people can compare: <bookmark mark='s'/> "
            "show someone two answers to the same prompt, <bookmark mark='p'/> and ask which is better. How do we "
            "turn a pile of such choices into a reward?"
        ) as vo:
            self.play(FadeIn(prompt), FadeIn(note(r"illustrative example").to_corner(UR, buff=0.3)))
            vo.wait_until("s")
            self.play(FadeIn(boxes, lag_ratio=0.3))
            vo.wait_until("p")
            self.play(Create(pick), FadeIn(tick), FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gumbel(self):
        model = mtex(r"\text{choose } A \iff", r"u_A + \varepsilon_A", r">", r"u_B + \varepsilon_B", font_size=40)
        model[1][:2].set_color(C.REWARD)
        model[3][:2].set_color(C.REWARD)
        ml = label(r"a hidden utility $u$ for each answer, plus noise in each judgment", font_size=26, color=GREY_A)
        top = VGroup(model, ml).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        plot = Plot(x_range=(-6, 6), y_range=(0, 0.42), width=8.0, height=3.4, x_ticks=[-4, -2, 0, 2, 4],
                    x_label=r"$\varepsilon_B - \varepsilon_A$")
        plot.move_to(DOWN * 0.9 + LEFT * 1.6)
        xs = np.linspace(-6, 6, 400)
        g = plot.line(xs, gumbel_pdf(xs), color=GREY_A, stroke_width=3)
        gl = label(r"Gumbel noise", font_size=24, color=GREY_A).next_to(plot.c2p(-0.2, 0.37), UL, buff=0.05)
        lg = plot.line(xs, logistic_pdf(xs), color=C.REWARD, stroke_width=4)
        ll = label(r"difference of two: logistic", font_size=24, color=C.REWARD).next_to(plot.c2p(-1.6, 0.2), LEFT, buff=0.1)
        du = ValueTracker(-1.5)

        def area():
            d = du.get_value()
            m = xs <= d
            return plot.area(xs[m], logistic_pdf(xs[m]), C.REWARD, opacity=0.45)
        sh = always_redraw(area)
        vl = always_redraw(lambda: DashedLine(plot.c2p(du.get_value(), 0), plot.c2p(du.get_value(), 0.4), color=YELLOW))
        vlab = always_redraw(lambda: mtex(rf"u_A - u_B = {du.get_value():+.1f}", font_size=28, color=YELLOW)
                             .next_to(plot.c2p(du.get_value(), 0.4), UP, buff=0.05))
        res = mtex(r"P(A \succ B)", r"=", r"P\big(\varepsilon_B - \varepsilon_A < u_A - u_B\big)", r"=", r"\sigma(u_A - u_B)", font_size=36)
        res[4].set_color(C.REWARD)
        res.to_edge(DOWN, buff=0.25)
        pv = always_redraw(lambda: mtex(rf"\sigma = {sigmoid(du.get_value()):.2f}", font_size=34, color=C.REWARD)
                           .next_to(plot, RIGHT, buff=0.4).shift(UP * 0.5))
        sig = mtex(r"\sigma(z) = \frac{1}{1 + e^{-z}}", font_size=32).next_to(plot, RIGHT, buff=0.4).shift(DOWN * 0.6)
        with self.voiceover(
            "Model each judgment like this. Every answer has a hidden utility, and each time a person judges, they "
            "perceive it with some noise, and choose whichever looks better. <bookmark mark='g'/> If that noise "
            "follows a Gumbel distribution, the distribution of the largest of many small effects, then "
            "<bookmark mark='d'/> the difference of two independent noises is exactly logistic. <bookmark mark='a'/> "
            "So the probability of choosing A is the area to the left of the utility gap: the logistic sigmoid of "
            "the difference."
        ) as vo:
            self.play(Write(model), FadeIn(ml))
            vo.wait_until("g")
            self.play(FadeIn(plot), Create(g), FadeIn(gl), FadeIn(exact_tag(r"exact curves")))
            vo.wait_until("d")
            self.play(Create(lg), FadeIn(ll))
            vo.wait_until("a")
            self.play(FadeIn(sh), Create(vl), FadeIn(vlab), FadeIn(pv), FadeIn(sig))
            self.play(du.animate.set_value(2.2), run_time=3.0)
            self.play(Write(res))
        name = VGroup(label(r"the Bradley--Terry", font_size=28, color=GREY_A), label(r"model (1952)", font_size=28, color=GREY_A))
        name.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(sig, DOWN, buff=0.4, aligned_edge=LEFT)
        with self.voiceover(
            "This is the Bradley-Terry model, from 1952. Notice that only the difference of utilities matters. "
            "Add the same constant to every answer for a prompt, and nothing changes."
        ):
            self.play(FadeIn(name))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def likelihood(self):
        L = mtex(r"\mathcal{L}(\phi)", r"=", r"-\sum_{(x,\,y_w,\,y_l)}", r"\log \sigma\big(", r"r_\phi(x, y_w)", r"-", r"r_\phi(x, y_l)",
                 r"\big)", font_size=44).move_to(UP * 1.4)
        L[4].set_color(C.REWARD)
        L[6].set_color(C.PENALTY)
        n = label(r"maximum likelihood on comparisons: $y_w$ was preferred over $y_l$", font_size=26, color=GREY_A).next_to(L, DOWN, buff=0.25)
        rm = VGroup(RoundedRectangle(width=3.6, height=1.3, corner_radius=0.15, stroke_color=C.REWARD, fill_color=C.REWARD,
                                     fill_opacity=0.12), label(r"reward model $r_\phi$", font_size=28))
        rm[1].move_to(rm[0])
        rm.move_to(DOWN * 1.1 + LEFT * 2.5)
        inp = label(r"prompt $+$ answer", font_size=24, color=GREY_A).next_to(rm, LEFT, buff=0.5)
        out = mtex(r"r \in \mathbb{R}", font_size=36, color=C.REWARD).next_to(rm, RIGHT, buff=0.5)
        a1 = Arrow(inp.get_right(), rm.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        a2 = Arrow(rm.get_right(), out.get_left(), buff=0.1, color=C.REWARD, stroke_width=3)
        sub = label(r"a language model with a single number as output", font_size=24, color=GREY_A).next_to(rm, DOWN, buff=0.2)
        shift = label(r"$r_\phi(x, y) + c(x)$ fits the data equally well: only differences are learned", font_size=26, color=YELLOW)
        shift.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So fit the utilities by maximum likelihood. The reward model is a copy of the language model with a "
            "single number as its output, trained so that the preferred answer's score beats the rejected one's "
            "through the sigmoid. <bookmark mark='s'/> And because only differences matter, the reward model can "
            "carry an arbitrary offset for each prompt. That's harmless for us: a per-prompt offset is just a "
            "baseline, and we've seen that baselines don't change the policy gradient."
        ) as vo:
            self.play(Write(L), FadeIn(n), run_time=1.8)
            self.play(FadeIn(rm), FadeIn(inp), FadeIn(out), GrowArrow(a1), GrowArrow(a2), FadeIn(sub))
            vo.wait_until("s")
            self.play(FadeIn(shift))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proxy(self):
        plot = Plot(x_range=(0, 10), y_range=(0, 1.2), width=8.0, height=4.0, x_label=r"how far the policy moves from where it started",
                    y_label=r"reward")
        plot.move_to(DOWN * 0.4 + LEFT * 0.8)
        xs = np.linspace(0, 10, 200)
        proxy = 1.1 * (1 - np.exp(-xs / 3.0))
        gold = 0.75 * (1 - np.exp(-xs / 2.0)) - 0.035 * xs**1.5 * 0.6
        lp = plot.line(xs, proxy, color=C.REWARD, stroke_width=4)
        lg = plot.line(xs, np.clip(gold, 0, None), color=WHITE, stroke_width=4)
        tp = label(r"the reward model's score", font_size=24, color=C.REWARD).next_to(plot.c2p(10, proxy[-1]), UP, buff=0.12).shift(LEFT * 1.4)
        tg = label(r"what people actually think", font_size=24).next_to(plot.c2p(8.0, float(np.interp(8.0, xs, gold))), DL, buff=0.2)
        head = label(r"Goodhart's law: a measure that becomes a target stops being a good measure", font_size=28).to_edge(UP, buff=0.4)
        src = source(r"the shape measured by Gao, Schulman \& Hilton, \emph{Scaling Laws for Reward Model Overoptimization}, 2022")
        with self.voiceover(
            "But a reward model is a learned approximation, and the policy is an optimizer. <bookmark mark='p'/> "
            "Push hard enough, and the policy finds answers the reward model loves and people don't: "
            "<bookmark mark='g'/> the proxy keeps rising while true quality peaks and falls. OpenAI measured "
            "exactly this shape in 2022. That's why RLHF keeps the policy on a leash: the KL penalty to the "
            "reference. What does that leash actually do? Remarkably, we can solve for the best policy exactly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(schematic_tag()), FadeIn(src))
            vo.wait_until("p")
            self.play(Create(lp), FadeIn(tp), run_time=1.5)
            vo.wait_until("g")
            self.play(Create(lg), FadeIn(tg), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()
