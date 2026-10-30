from __future__ import annotations


import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, PART, load, takeaway_card

AG, RP, AD, LI = OPT_COLORS["adagrad"], OPT_COLORS["rmsprop"], OPT_COLORS["adam"], OPT_COLORS["lion"]
CM = {r"m_t": OPT_COLORS["momentum"], r"v_t": AD, r"\hat m_t": OPT_COLORS["momentum"], r"\hat v_t": AD}


class Adam(VoiceoverScene):
    def construct(self):
        self.card()
        self.adagrad()
        self.rmsprop()
        self.adam_rule()
        self.bias()
        self.sign()
        self.lion()
        self.takeaway()

    def card(self):
        c = chapter_card(6, r"AdaGrad, RMSProp, Adam", r"Should every weight get its own step size?", part=PART, lit=(2014,))
        with self.voiceover("Chapter six. AdaGrad, RMSProp, Adam."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def adagrad(self):
        hist = history_card(2011, r"John Duchi, Elad Hazan \& Yoram Singer", r"AdaGrad: \ divide each weight's step by "
                            r"the root of the sum of its squared gradients so far", width=6.0).to_corner(UL, buff=0.35)
        rule = VGroup(cmath(r"s_t", "=", r"s_{t-1} + g_t^2", font_size=36),
                      cmath(r"\theta_t", "=", r"\theta_{t-1} - \frac{\eta}{\sqrt{s_t} + \epsilon}\, g_t", font_size=36))
        rule.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(hist, DOWN, buff=0.5).align_to(hist, LEFT)
        rn = label(r"per weight, \ elementwise", font_size=22, color=GREY_A).next_to(rule, DOWN, buff=0.2).align_to(rule, LEFT)
        # two weights, one with big gradients, one with small: the same step size after dividing (illustrative)
        ax = Axes(x_range=[0, 30, 10], y_range=[0, 1.2, 0.5], x_length=5.0, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.6, 1.2, 0])
        t = np.arange(1, 31)
        big = curve(ax, t, 1.0 / np.sqrt(t), AG, 3)
        bl = label(r"AdaGrad's step size: \ $\propto 1/\sqrt{t}$ \ for a steady gradient", font_size=20, color=AG)
        bl.next_to(ax, DOWN, buff=0.15)
        ill = note(r"illustrative").next_to(ax, UP, buff=0.1)
        sparse = label(r"rare features, \ small summed squares: \\ big steps when they do appear", font_size=22,
                       color=GREY_A).move_to([3.6, -1.9, 0])
        with self.voiceover(
            "One learning rate for every weight is a strange choice. Some weights see large gradients, others tiny "
            "ones; chapter one's condition number, one direction at a time. <bookmark mark='a'/> In 2011 John "
            "Duchi, Elad Hazan and Yoram Singer proposed AdaGrad: keep a running sum of each weight's squared "
            "gradients, and divide its step by the square root. <bookmark mark='b'/> A word that appears rarely has "
            "a small sum, so when it does appear, it gets a big step. <bookmark mark='c'/> The catch: the sum only "
            "ever grows, so every step size shrinks like one over the square root of time, and a long training run "
            "slows to a crawl."
        ) as vo:
            self.play(FadeIn(hist, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(Write(rule), FadeIn(rn))
            vo.wait_until("b")
            self.play(FadeIn(sparse))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(ill), Create(big), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()

    def rmsprop(self):
        slide = RoundedRectangle(width=7.6, height=3.6, corner_radius=0.1, stroke_color=GREY_B, stroke_width=2,
                                 fill_color="#1A2030", fill_opacity=1).move_to([-2.2, 0.3, 0])
        st = label(r"rmsprop: \ Divide the gradient by a running \\ average of its recent magnitude", font_size=26,
                   color=WHITE).next_to(slide.get_top(), DOWN, buff=0.35)
        f1 = MathTex(r"\text{MeanSquare}(w, t) = 0.9\,\text{MeanSquare}(w, t-1) + 0.1\,\Big(\tfrac{\partial E}{\partial w}(t)\Big)^2",
                     font_size=28, color=RP).next_to(st, DOWN, buff=0.4)
        f2 = label(r"divide the gradient by $\sqrt{\text{MeanSquare}(w, t)}$", font_size=24, color=GREY_A).next_to(f1, DOWN, buff=0.3)
        src = note(r"after T.~Tieleman \& G.~Hinton, \textit{Neural Networks for Machine Learning}, \ Lecture 6e (Coursera, 2012)",
                   font_size=18).next_to(slide, DOWN, buff=0.15)
        hist = history_card(2012, r"Geoffrey Hinton's online course", r"RMSProp: \ AdaGrad with a forgetting average. \ "
                            r"Never written up as a paper; \ cited by its lecture slide for years", width=4.6)
        hist.move_to([4.6, 0.3, 0])
        with self.voiceover(
            "The fix came from an online course. <bookmark mark='a'/> In 2012, in a lecture of Geoffrey Hinton's "
            "Coursera class on neural networks, one slide proposed RMSProp: replace AdaGrad's growing sum by a "
            "running average that forgets, nine tenths of the old value plus one tenth of the new squared gradient, "
            "and divide by its square root. <bookmark mark='b'/> It was never written up as a paper. For years, "
            "research papers cited a lecture slide."
        ) as vo:
            self.play(FadeIn(slide), FadeIn(st))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(f2), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(hist, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def adam_rule(self):
        hist = history_card(2014, r"Diederik Kingma \& Jimmy Ba", r"Adam, \ \textit{adaptive moment estimation}: \ "
                            r"momentum and RMSProp together, \ with a correction for their start", width=5.4)
        hist.to_corner(UR, buff=0.35)
        rows = VGroup(
            cmath(r"m_t", "=", r"\beta_1\, m_{t-1} + (1 - \beta_1)\, g_t", colors=CM, font_size=34),
            cmath(r"v_t", "=", r"\beta_2\, v_{t-1} + (1 - \beta_2)\, g_t^2", colors=CM, font_size=34),
            cmath(r"\hat m_t = \frac{m_t}{1 - \beta_1^{\,t}}", r",\quad", r"\hat v_t = \frac{v_t}{1 - \beta_2^{\,t}}", font_size=34),
            cmath(r"\theta_t", "=", r"\theta_{t-1} - \eta\, \frac{\hat m_t}{\sqrt{\hat v_t} + \epsilon}", colors=CM, font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_corner(UL, buff=0.45).shift(DOWN * 0.2)
        notes = VGroup(label(r"momentum: \ the average direction", font_size=20, color=OPT_COLORS["momentum"]),
                       label(r"RMSProp: \ the average squared size", font_size=20, color=AD),
                       label(r"the bias corrections", font_size=20, color=GREY_A),
                       label(r"defaults: \ $\beta_1 = 0.9$, \ $\beta_2 = 0.999$, \ $\epsilon = 10^{-8}$", font_size=20, color=GREY_A))
        for n_, r_ in zip(notes, rows):
            n_.next_to(r_, RIGHT, buff=0.35)
        notes[3].next_to(rows[3], DOWN, buff=0.25).align_to(rows[3], LEFT)
        for n_ in notes[:3]:
            keep_in_frame(n_)
        with self.voiceover(
            "In 2014 Diederik Kingma and Jimmy Ba put the two ideas together. <bookmark mark='a'/> Keep a running "
            "average of the gradient, m: that is momentum. <bookmark mark='b'/> Keep a running average of its square, "
            "v: that is RMSProp. <bookmark mark='c'/> Correct both for starting at zero, a step we'll derive in a "
            "moment, <bookmark mark='d'/> and step by the average direction divided by the root of the average "
            "square. They called it Adam, and with its defaults it trained most of deep learning for the next "
            "decade."
        ) as vo:
            self.play(FadeIn(hist, shift=LEFT * 0.2))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(Write(rows[k]), FadeIn(notes[k]))
        self.wait(0.3)
        self.clear_scene()

    def bias(self):
        a = load("adamview")
        head = label(r"why divide by $1 - \beta^{\,t}$?", font_size=30).to_edge(UP, buff=0.3)
        rows = [
            cmath(r"m_t", "=", r"(1 - \beta_1) \sum_{i=1}^{t} \beta_1^{\,t-i}\, g_i", font_size=32),
            cmath(r"\mathbb{E}\, m_t", "=", r"\mathbb{E}\, g \;(1 - \beta_1) \sum_{i=1}^{t} \beta_1^{\,t-i}", font_size=32),
            cmath(r"\mathbb{E}\, m_t", "=", r"(1 - \beta_1^{\,t})\; \mathbb{E}\, g", font_size=32),
        ]
        whys = [why(r"unroll from $m_0 = 0$"), why(r"if the gradients' mean is steady"), why(r"a geometric sum")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-3.4, buff=0.45, edge=6.9)
        # computed: one weight's real gradients over the first 60 steps, m and m-hat
        g = np.asarray(a["grads"])[:, 0]
        m, mh = np.asarray(a["m"])[:, 0], np.asarray(a["mhat"])[:, 0]
        T = len(g)
        lim = float(np.abs(g).max()) * 1.1
        ax = CornerAxes(x_range=[0, T, 10], y_range=[-lim, lim, lim], x_length=5.6, y_length=2.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.3, -2.1, 0])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(T, 0), color=GREY_D, stroke_width=1.5)
        gd = VGroup(*[Dot(ax.c2p(k + 1, v), radius=0.03, color=GREY_B) for k, v in enumerate(g)])
        cm = curve(ax, np.arange(1, T + 1), m, OPT_COLORS["momentum"], 2.5)
        cmh = curve(ax, np.arange(1, T + 1), mh, C.BITS, 3)
        lg = VGroup(label(r"one weight's gradients, \ steps $1$--$60$", font_size=18, color=GREY_B),
                    label(r"$m_t$: \ starts near zero", font_size=18, color=OPT_COLORS["momentum"]),
                    label(r"$\hat m_t$: \ corrected", font_size=18, color=C.BITS)).arrange(RIGHT, buff=0.3)
        lg.next_to(ax, UP, buff=0.1)
        keep_in_frame(lg)
        raw = float(a["raw_first"])
        first = VGroup(label(r"the very first step, \ per weight:", font_size=22, color=GREY_A),
                       label(rf"without the corrections: \ $\frac{{1 - \beta_1}}{{\sqrt{{1 - \beta_2}}}}\,\eta = {raw:.2f}\,\eta$",
                             font_size=22, color=C.SURPRISE),
                       label(r"with them: \ exactly $\eta$", font_size=22, color=C.BITS)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        first.move_to([3.6, -2.0, 0])
        tag = note(r"computed: \ the character model's second hidden matrix").to_corner(DR, buff=0.15)
        with self.voiceover(
            "Why the corrections? <bookmark mark='a'/> Unroll the average from its start at zero: m is a weighted sum "
            "of all the gradients so far. <bookmark mark='b'/> If their mean is steady, its expectation is that mean "
            "times a geometric sum, <bookmark mark='c'/> which is one minus beta to the t. Early on, m is biased "
            "towards zero, and dividing by that factor removes the bias. <bookmark mark='d'/> Here is one weight of "
            "our character model, its real gradients over the first sixty steps: the raw average starts near zero, "
            "the corrected one tracks the gradients from the first step. <bookmark mark='e'/> The correction matters "
            "most for v, whose memory is a thousand steps long. Without either correction the very first step would "
            f"be {raw:.2f} times eta; with them, it is exactly eta."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                step(k)
            vo.wait_until("d")
            self.play(Create(ax), Create(zero), FadeIn(gd), FadeIn(lg), FadeIn(tag))
            self.play(Create(cm), Create(cmh), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(first))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sign(self):
        a = load("adamview")
        head = cmath(r"\beta_1 = \beta_2 = 0,\ \epsilon \to 0:\quad", r"\frac{g_t}{\sqrt{g_t^2}}", "=", r"\operatorname{sign}(g_t)",
                     font_size=36).to_edge(UP, buff=0.35)
        hl = label(r"Adam's limit: \ every weight moves by exactly $\eta$, \ up or down: \ sign descent", font_size=24,
                   color=C.BITS).next_to(head, DOWN, buff=0.2)
        panels = VGroup()
        for k_ in ("1", "100", "1000"):
            h = np.asarray(a[f"hist{k_}"], float)
            h = h / h.max()
            ax = CornerAxes(x_range=[0, 2, 0.5], y_range=[0, 1.05, 0.5], x_length=3.4, y_length=2.0, tips=False,
                            axis_config={"stroke_color": GREY_C, "include_ticks": False})
            w = ax.c2p(0.05, 0)[0] - ax.c2p(0, 0)[0]
            bars = VGroup(*[Rectangle(width=w * 0.9, height=max(1e-3, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0,
                                      fill_color=AD, fill_opacity=0.9).move_to(ax.c2p(0.025 + 0.05 * i, v / 2))
                            for i, v in enumerate(h)])
            one = DashedLine(ax.c2p(1, 0), ax.c2p(1, 1.05), color=WHITE, stroke_width=1.5)
            xt = VGroup(*[MathTex(s_, font_size=18, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                          for s_, v in (("0", 0), (r"\eta", 1), (r"2\eta", 2))])
            kk = f"{int(k_):,}".replace(",", "{,}")
            cap = label(rf"step ${kk}$: \ median ${a[f'median{k_}']:.2f}\,\eta$", font_size=20,
                        color=GREY_A).next_to(xt, DOWN, buff=0.1)
            panels.add(VGroup(ax, bars, one, xt, cap))
        panels.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.9)
        pl = label(r"how far each of the $65{,}536$ weights of the second hidden matrix moved, \ $|\Delta\theta|$",
                   font_size=22, color=GREY_A).next_to(panels, UP, buff=0.25)
        tag = note(r"computed: \ Adam, $\eta = 0.002$, \ $\beta = (0.9, 0.999)$").to_corner(DR, buff=0.2)
        m1, m100, m1000 = (float(a[f"median{k}"]) for k in ("1", "100", "1000"))
        f1 = float(a["frac1"])
        said1 = (f"<bookmark mark='b'/> Later, the typical move is far smaller: {m100:.2f} eta at step 100, "
            f"{m1000:.2f} at step 1,000. The gradients are noisy, their average m is small next to their root "
            "mean square, and Adam's step becomes the sign of the gradient, scaled by its signal-to-noise ratio."
            if max(m100, m1000) < 0.6 else
            f"<bookmark mark='b'/> Later the typical move stays large, {m100:.2f} eta at step 100: the gradients "
            "keep their signs from step to step.")
        with self.voiceover(
            "Look at Adam's limit. Turn both memories off and let epsilon go to zero: the gradient divided by its "
            "own size is just its sign. Every weight moves by exactly eta, up or down. Adam is a smoothed form of "
            "sign descent. <bookmark mark='a'/> Here is how far each weight of our model's hidden matrix moves, in "
            f"units of eta. At the first step, the corrections make Adam exactly sign descent: {f1:.0%} of the "
            "weights move by eta. "
            + said1
        ) as vo:
            self.play(Write(head), FadeIn(hl))
            vo.wait_until("a")
            self.play(FadeIn(pl), FadeIn(panels[0]), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
            self.play(FadeIn(panels[2]))
        self.wait(0.3)
        self.clear_scene()

    def lion(self):
        hist = history_card(2023, r"Xiangning Chen, Chen Liang, \dots, Quoc Le \ (Google)", r"\textit{Symbolic Discovery of "
                            r"Optimization Algorithms}: \ a program search over update rules found Lion", width=6.2)
        hist.to_corner(UL, buff=0.35)
        rows = VGroup(
            cmath(r"c_t", "=", r"\beta_1\, m_{t-1} + (1 - \beta_1)\, g_t", font_size=34),
            cmath(r"\theta_t", "=", r"\theta_{t-1} - \eta\,\big(\operatorname{sign}(c_t) + \lambda\,\theta_{t-1}\big)",
                  font_size=34, colors={r"\theta_{t-1} - \eta\,\big(\operatorname{sign}(c_t) + \lambda\,\theta_{t-1}\big)": LI}),
            cmath(r"m_t", "=", r"\beta_2\, m_{t-1} + (1 - \beta_2)\, g_t", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(hist, DOWN, buff=0.45).align_to(hist, LEFT)
        notes = VGroup(label(r"$\beta_1 = 0.9$, \ $\beta_2 = 0.99$: \ two speeds of memory", font_size=22, color=GREY_A),
                       label(r"one state per weight, \ not Adam's two", font_size=22, color=GREY_A),
                       label(r"every weight moves by $\pm\eta$: \ a smaller $\eta$, \ a larger decay $\lambda$", font_size=22,
                             color=LI)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -2.2, 0])
        keep_in_frame(notes)
        with self.voiceover(
            "That limit became an optimizer. <bookmark mark='a'/> In 2023 a team at Google let a computer search "
            "over programs for update rules, and the winner, after simplification, was Lion: move every weight by "
            "the sign of a blend of momentum and the new gradient, <bookmark mark='b'/> then update the momentum "
            "more slowly. <bookmark mark='c'/> It keeps one number per weight instead of Adam's two, and because "
            "every step has full size, it wants a smaller learning rate and a larger weight decay. It runs in "
            "our race in Chapter 12."
        ) as vo:
            self.play(FadeIn(hist, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(Write(rows[0]), Write(rows[1]))
            vo.wait_until("b")
            self.play(Write(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"Adam: \ momentum over a running size",
                          r"$\hat m / \sqrt{\hat v}$, \ bias-corrected so the first step is $\eta$ per weight. \ Its "
                          r"limit is sign descent, \ the steepest step when every weight is bounded on its own.",
                          r"Next: \ what weight decay does inside Adam")
        with self.voiceover(
            "So Adam is momentum divided by a running size, corrected for its start, and in the limit it is sign "
            "descent: the steepest step when each weight may move by at most eta on its own. Next, a subtle bug in "
            "how it was used for years."
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
