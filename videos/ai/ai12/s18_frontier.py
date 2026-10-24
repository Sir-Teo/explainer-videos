from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import FIT, HIST, NCOL, PART, SP, TT, era_strip, load


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.debate()
        self.evidence()
        self.density()

    def card(self):
        card = chapter_card(17, r"Has pretraining stalled?", r"What does the evidence say, in 2026?", part=PART)
        with self.voiceover("Chapter seventeen. Has pretraining stalled?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def debate(self):
        events = [
            (r"Dec 2024", r"Sutskever: \\ ``pre-training as we \\ know it will end''"),
            (r"Feb 2025", r"GPT-4.5: \ OpenAI's \\ largest model, \\ pretraining scaled up"),
            (r"Jul 2025", r"Grok 4: \\ reinforcement learning \\ at pretraining scale"),
            (r"Sep 2025", r"Epoch AI: \ GPT-5 \\ likely used less \\ compute than GPT-4.5"),
            (r"Nov 2025", r"Gemini 3: \ ``the delta \\ \ldots is as big as \\ we've ever seen''"),
            (r"Jul 2026", r"Pichai: \ ``much larger \\ base models''; \\ Gemini 4 in training"),
            (r"Oct 2026", r"Microsoft: \ a $2.8$-trillion \\ MoE, forecast \\ from small models"),
        ]
        head, axis, tag, skel, marks = era_strip(self, events, head_text=r"The debate, \ 2024 to 2026",
                                                 tag_text=r"evenly spaced, \ not to scale", font_size=19)
        cite_ = cite(r"Sutskever, NeurIPS talk (Dec 2024); \ OpenAI, GPT-4.5 system card; \ xAI, Grok 4; \ Epoch AI (Sep "
                     r"2025); \ O.~Vinyals (Nov 2025); \ Alphabet earnings call (Jul 2026); \ Microsoft AI (Oct 2026)",
                     font_size=15, corner=DL)
        with self.voiceover(
            "Has pretraining stopped paying? In December 2024, Ilya Sutskever told the field's largest conference "
            "that pre-training as we know it will end: compute keeps growing, but we have but one internet. "
            "<bookmark mark='a'/> In February 2025, OpenAI released GPT-4.5, its largest model yet, a scale-up of "
            "pretraining. <bookmark mark='b'/> The growth moved elsewhere: in July, "
            "xAI ran reinforcement learning on Grok 4 at the scale of pretraining, <bookmark mark='c'/> and Epoch AI "
            "estimated that GPT-5 had probably used less training compute than GPT-4.5. <bookmark mark='d'/> Then "
            "in November, Google's Gemini 3, and Oriol Vinyals wrote that its gain from pretraining was as big as "
            "they had ever seen. <bookmark mark='e'/> In July 2026, Sundar Pichai said the next frontier needs much "
            "larger base models, and that Gemini 4 was in training. <bookmark mark='f'/> And in October, Microsoft "
            "described a mixture of experts with two point eight trillion parameters, its performance forecast in "
            "advance from a ladder of smaller models."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tag), FadeIn(skel), FadeIn(cite_))
            self.play(FadeIn(marks[0], shift=UP * 0.2))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(marks[k + 1], shift=(UP if (k + 1) % 2 == 0 else DOWN) * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def evidence(self):
        ch = load("chinchilla")
        pts = np.asarray(ch["extrap_pts"], float).reshape(-1, 4)  # N, D, measured, predicted
        err, mx, bias = float(ch["extrap_err"]), float(ch["extrap_max"]), float(ch["extrap_bias"])
        n_fit, n_test = int(ch["cheap"]["n"]), int(ch["extrap_n"])
        cut = float(ch.get("extrap_cut", 1e12))
        opt = ch["extrap_opt"]
        C = 6 * pts[:, 0] * pts[:, 1]
        lc = np.log10(C)
        res = pts[:, 3] - pts[:, 2]
        lim = max(0.05, math.ceil(np.abs(res).max() * 50) / 50)
        ax = CornerAxes(x_range=[math.floor(lc.min() * 2) / 2, math.ceil(lc.max() * 2) / 2, 0.5], y_range=[-lim, lim, lim / 2],
                        x_length=6.0, y_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.2, -0.4, 0])
        x0, x1 = ax.x_range[0] if hasattr(ax, "x_range") else lc.min(), lc.max()
        zero = DashedLine(ax.c2p(math.floor(lc.min() * 2) / 2, 0), ax.c2p(math.ceil(lc.max() * 2) / 2, 0), color=GREY_B, stroke_width=1.5)
        xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, -lim), DOWN, buff=0.08)
                      for v in range(math.ceil(lc.min()), math.floor(lc.max()) + 1)])
        yt = VGroup(*[MathTex(f"{v:+.2f}" if v else "0", font_size=20, color=GREY_B)
                      .next_to(ax.c2p(math.floor(lc.min() * 2) / 2, v), LEFT, buff=0.08) for v in (-lim, 0, lim)])
        xn = label(r"compute of the run being predicted", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"predicted minus measured \ (bits)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        dts = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=TT) for a, b in zip(lc, res)])
        side = VGroup(
            label(rf"fitted on our ${n_fit}$ cheapest runs \\ (up to ${sci(cut, 0)}$ operations)", font_size=22, color=GREY_A),
            label(rf"predicting the other ${n_test}$: \\ off by ${err:.3f}$ bits on average, \\ ${mx:.3f}$ at worst", font_size=24,
                  color=TT),
            label(rf"the best model at $10^{{13}}$: \\ predicted ${float(opt['pred']):.3f}$, \ measured ${float(opt['meas']):.3f}$",
                  font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.3, 0])
        slow = label(r"$L \propto C^{-0.050}$ \ (Kaplan): \ halving the loss takes $2^{1/0.05} \approx 10^{6}$ times "
                     r"the compute", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.3)
        ok = err < 0.03
        with self.voiceover(
            "What can a scaling law actually tell us? Test ours the way laboratories use theirs. Fit Chinchilla's "
            f"formula on only our {n_fit} cheapest runs, and predict the other {n_test}, up to ten times costlier. "
            f"<bookmark mark='a'/> On average the prediction is off by {err:.3f} bits, {mx:.3f} at worst"
            + (", and it does not drift as the compute grows: the law extrapolates. " if ok and abs(bias) < err else
               f", and it {'over' if bias > 0 else 'under'}estimates the loss as compute grows: a hint of curvature. ")
            + "<bookmark mark='b'/> That is the sense in which pretraining has not stalled: the loss keeps falling "
            "along its curve. But the curve was always slow. With Kaplan's exponent for compute, 0.05, halving the "
            "loss takes a million times the compute. What is debated is not the curve, but whether each step down "
            "it buys enough capability to be worth its price."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dts], lag_ratio=0.04), FadeIn(side[1]), run_time=2.0)
            self.play(FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(slow))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def density(self):
        hd = label(r"meanwhile, \ the same ability keeps getting cheaper", font_size=34).to_edge(UP, buff=0.4)
        # two exponentials, as on a log axis: halving times from the cited studies
        ax = CornerAxes(x_range=[0, 4, 1], y_range=[0, 5, 1], x_length=5.6, y_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.4, -0.6, 0])
        yrs = np.linspace(0, 4, 50)
        c1 = curve(ax, yrs, yrs * 12 / 8 * math.log10(2), C.TRUE_P, 3.5)  # compute needed halves every 8 months
        c2 = curve(ax, yrs, np.minimum(yrs * 12 / 3 * math.log10(2), 5), C.BITS, 3.5)  # density doubles every 3 months
        xt = VGroup(*[MathTex(str(v), font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v in range(0, 5)])
        yt = VGroup(*[MathTex(rf"10^{{{v}}}\times", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                      for v in range(0, 6)])
        xn = label(r"years", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        l1 = label(r"compute saved \ (halving every $8$ months)", font_size=20, color=C.TRUE_P).next_to(ax.c2p(4, 1.5), UL, buff=0.1)
        l2 = label(r"ability per parameter \ (doubling every $3$ months)", font_size=20, color=C.BITS).next_to(ax.c2p(1.6, 4.6), RIGHT, buff=0.1)
        sch = note(r"the cited rates, \ drawn").next_to(xn, DOWN, buff=0.12)
        cards = VGroup(
            history_card(2024, r"Ho et al.\ (Epoch AI)", r"the compute needed for a given language-model performance "
                         r"halved about every $8$ months \ ($5$ to $14$), \ 2012 to 2023", width=5.6, color=HIST),
            history_card(2024, r"Xiao et al., \ \textit{Densing law}", r"capability per parameter of open models doubled "
                         r"about every three months", width=5.6, color=HIST),
            history_card(2026, r"three axes now", r"pretraining, \ reinforcement learning, \ and thinking at answer time, "
                         r"\ each with its own curve", width=5.6, color=HIST),
        ).arrange(DOWN, buff=0.15).move_to([3.6, -0.5, 0])
        with self.voiceover(
            "The other side of the ledger is efficiency. <bookmark mark='a'/> In 2024, Anson Ho and colleagues at "
            "Epoch AI estimated that the compute needed to reach a given language-model performance halved about "
            "every eight months, from better architectures, data and training. <bookmark mark='b'/> The same year, "
            "Chaojun Xiao and colleagues at Tsinghua measured a densing law: the capability packed into each "
            "parameter of open models doubled about every three months. <bookmark mark='c'/> So the frontier moves "
            "on three curves at once: pretraining, reinforcement learning, and thinking at answer time, each slow "
            "on its own, each with a law that can be measured. The argument is about their prices, not their shapes."
        ) as vo:
            self.play(FadeIn(hd), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(sch))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(l1), FadeIn(cards[0], shift=LEFT * 0.1))
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(l2), FadeIn(cards[1], shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=LEFT * 0.1))
        self.wait(0.3)
        self.clear_scene()
