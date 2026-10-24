from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import FIT, HIST, NCOL, PART, SP, TT, era_strip, load, predict_card, takeaway_card


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.debate()
        self.predict()
        self.evidence()
        self.density()
        self.takeaway()

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
            (r"Nov 2025", r"Gemini 3: \ Vinyals: \\ gain from pretraining \\ as big as ever"),
            (r"Jul 2026", r"Pichai: \ next frontier \\ needs much larger \\ base models; \ Gemini 4"),
            (r"Oct 2026", r"Microsoft: \ a $2.8$-trillion \\ MoE, forecast \\ from small models"),
        ]
        head, axis, tag, skel, marks = era_strip(self, events, head_text=r"The debate, \ 2024 to 2026",
                                                 tag_text=r"evenly spaced, \ not to scale", font_size=19)
        cite_ = cite(r"Sutskever, NeurIPS talk (Dec 2024); \ OpenAI, GPT-4.5 system card; \ xAI, Grok 4; \ Epoch AI "
                     r"(Sep "
                     r"2025); \\ O.~Vinyals (Nov 2025); \ Alphabet earnings call (Jul 2026); \ Microsoft AI (Oct 2026)",
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
        ax = CornerAxes(x_range=[math.floor(lc.min() * 2) / 2 - 1, math.ceil(lc.max() * 2) / 2, 0.5], y_range=[-lim, lim, lim / 2],
                        x_length=6.0, y_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.2, -0.4, 0])
        x0, x1 = ax.x_range[0] if hasattr(ax, "x_range") else lc.min(), lc.max()
        zero = DashedLine(ax.c2p(ax.x_range[0], 0), ax.c2p(ax.x_range[1], 0), color=GREY_B, stroke_width=1.5)
        xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, -lim), DOWN, buff=0.08)
                      for v in range(math.ceil(ax.x_range[0]), math.floor(lc.max()) + 1)])
        yt = VGroup(*[MathTex(f"{v:+.2f}" if v else "0", font_size=20, color=GREY_B)
                      .next_to(ax.c2p(ax.x_range[0], v), LEFT, buff=0.08) for v in (-lim, 0, lim)])
        xn = label(r"compute of the run \ (operations)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"predicted minus measured \ (bits)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        dts = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=TT) for a, b in zip(lc, res)])
        Nf, Df, Lf = (np.asarray(ch[k], float) for k in ("fit_N", "fit_D", "fit_L"))
        cheap = 6 * Nf * Df <= cut
        cp = ch["cheap"]
        fit_res = (float(cp["E"]) + float(cp["A"]) * Nf[cheap] ** -float(cp["alpha"]) + float(cp["B"]) * Df[cheap] ** -float(cp["beta"])
                   - Lf[cheap])
        lcf = np.log10(6 * Nf[cheap] * Df[cheap])
        inside = (lcf >= ax.x_range[0]) & (np.abs(fit_res) <= lim)
        fdts = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=GREY_B) for a, b in zip(lcf[inside], fit_res[inside])])
        cutl = DashedLine(ax.c2p(math.log10(cut), -lim), ax.c2p(math.log10(cut), lim), color=GREY_B, stroke_width=1.5)
        fl_ = label(r"grey: \ the fitted runs", font_size=18, color=GREY_B).next_to(ax.c2p(math.log10(cut), lim), LEFT, buff=0.1)
        fl_.shift(DOWN * 0.15)
        side = VGroup(
            label(rf"fitted on our ${n_fit}$ cheapest runs \\ (up to ${sci(cut, 0)}$ operations)", font_size=22, color=GREY_A),
            label(rf"predicting the other ${n_test}$: \\ off by ${err:.3f}$ bits on average, \\ ${mx:.3f}$ at worst", font_size=24,
                  color=TT),
            label(rf"the best model at $10^{{13}}$: \\ predicted ${float(opt['pred']):.3f}$, \ measured "
                  rf"${float(opt['meas']):.3f}$",
                  font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.3, 0])
        slow = label(r"$L \propto C^{-0.050}$ \ (Kaplan): \ halving the loss takes $2^{1/0.05} \approx 10^{6}$ times "
                     r"the compute", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.3)
        ratio = float(ch.get("extrap_ratio", 10.0))
        steady = err < 0.03 and abs(bias) < 0.6 * err
        if steady:
            said1 = (
                ", and it does not drift as the compute grows: the law extrapolates. <bookmark mark='b'/> That is the "
                "sense in which pretraining has not stalled: the loss keeps falling along its curve. "
            )
        elif bias > 0:
            said1 = (
                ", and almost always on the high side: the costlier runs come out better than the cheap ones "
                "predicted. <bookmark mark='b'/> That is the sense in which pretraining has not stalled: at every scale "
                "we tried, the loss fell at least as fast as the law promised. "
            )
        else:
            said1 = (
                ", and almost always on the low side: the costlier runs fall short of the forecast. "
                "<bookmark mark='b'/> On our small scale, that is the stalling argument in miniature: a law fitted on "
                "small runs can promise more than larger ones deliver. "
            )
        with self.voiceover(
            "What can a scaling law actually tell us? Test ours the way laboratories use theirs. Fit Chinchilla's "
            f"formula on only our {n_fit} cheapest runs, and predict the other {n_test}, up to {ratio:.0f} times "
            f"costlier. <bookmark mark='a'/> On average the prediction is off by {err:.3f} bits, {mx:.3f} at worst"
            + said1
            + "But the curve was always slow. With Kaplan's exponent for compute, 0.05, halving the "
            "loss takes a million times the compute. What is debated is not the curve, but whether each step down "
            "it buys enough capability to be worth its price."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(zero), FadeIn(side[0]))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in fdts], lag_ratio=0.01), Create(cutl), FadeIn(fl_),
                      run_time=2.0)
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
        l1 = label(r"compute saved \\ (halving every $8$ months)", font_size=20, color=C.TRUE_P).move_to(ax.c2p(3.05, 0.48))
        l2 = label(r"ability per parameter \\ (doubling every $3$ months)", font_size=20, color=C.BITS).move_to(ax.c2p(1.15, 4.45))
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

    # ------------------------------------------------------------------
    def predict(self):
        pc = predict_card(r"Fit the law on our cheapest runs and predict runs ten times costlier. \ Will it miss by "
                          r"a hundredth of a bit, \ a tenth, \ or more?")
        with self.voiceover(
            "Pause and predict. Fit the law on our cheapest runs, and predict runs ten times costlier. Will it miss "
            "by a hundredth of a bit, a tenth, or more?"
        ):
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(pc))

    def takeaway(self):
        tk = takeaway_card(r"The curves hold; \ the argument is about prices",
                           r"Pretraining, \ reinforcement learning and answer-time compute each follow a measurable "
                           r"law, \ and efficiency keeps lowering the price of a given ability.",
                           r"next: \ the recap")
        with self.voiceover(
            "The takeaway: every axis of scale we can measure still follows its law. What is argued over is the price "
            "of the next step, and that price keeps falling. Now, the recap."
        ) as vo:
            self.play(FadeIn(tk[0], shift=UP * 0.2))
            self.wait(max(0.0, vo.duration * 0.5 - 1.0))
            self.play(FadeIn(tk[1]))
        self.wait(0.4)
        self.play(FadeOut(tk))
