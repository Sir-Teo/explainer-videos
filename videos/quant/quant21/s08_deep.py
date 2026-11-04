from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, CVA_C, EXPO, GOOD, PART, ask, fit_right, illustration, load


class Deep(VoiceoverScene):
    def construct(self):
        d = load("deepxva")
        self.card()
        self.idea()
        self.train(d)
        self.result(d)

    def card(self):
        c = chapter_card(7, r"A network that learns future values", r"Can exposure be learned from cash flows alone?",
                         part=PART)
        with self.voiceover("Chapter seven. A network that learns what a book will be worth, from its cash flows alone."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self):
        rows = [cmath(r"V(t_j, x)", r"=", r"\mathbb{E}\Big[\textstyle\sum_{k > t_j} \frac{D(T_k)}{D(t_j)}\,\text{CF}_k\ "
                      r"\Big|\ x_{t_j} = x\Big]", font_size=36, colors={r"V(t_j, x)": EXPO}),
                cmath(r"\hat V_\theta", r"=", r"\arg\min_\theta \sum_{\text{paths}, j}\Big(\hat V_\theta(t_j, x) - "
                      r"\textstyle\sum_{k > t_j}\frac{D(T_k)}{D(t_j)}\text{CF}_k\Big)^2", font_size=32,
                      colors={r"\hat V_\theta": GOOD})]
        whys = [why(r"the future value of the book is a conditional expectation of its discounted cash flows, given the "
                    r"state on that date: the quantity every exposure needs, at every date and on every path"),
                why(r"regress the realised discounted cash flows on the state with a network over (date, state): Part "
                    r"16's regression, with a network in place of polynomials. The idea behind deep xVA solvers "
                    r"(Gnoatto, Picarelli and Reisinger, 2023), which solve the adjustments' own equations the same way")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Chapters one to six used a pricing formula for the swaps on every path. Real books hold trades with no "
            "formula. But the value on a future date is always a conditional expectation: of the discounted cash "
            "flows still to come, given the state of the world then. <bookmark mark='a'/> So simulate the cash flows, "
            "and regress them on the state with a network, one network over date and state together. It is the "
            "regression of Part sixteen with a network in place of polynomials, and the starting point of the deep "
            "solvers that Alessandro Gnoatto and coauthors built for the valuation adjustments themselves."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def train(self, d):
        L = np.asarray(d["losses"])
        g = axes([0, len(L) * 50], [0, max(L) * 1.1], x_length=6.8, y_length=4.0, xlabel=r"training steps",
                 ylabel=r"mean squared error (scaled)", xticks=[0, 1000, 2000], yticks=[], font_size=14).to_edge(
            LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, np.arange(len(L)) * 50, L, GOOD, stroke_width=3)
        side = wrapped_label(r"inputs: the date and the Hull--White state; target: each path's realised discounted cash "
                             r"flows of the three swaps, never their formula value. The loss cannot reach zero: the "
                             r"target is noisy, and the network learns its conditional mean", 3.8, 18,
                             GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The network sees only the date, the state of the rate model, and what each path's swaps actually paid "
            "afterwards. <bookmark mark='a'/> Its error falls, and then levels off well above zero: each target is one "
            "noisy outcome, and the best the network can do is learn their average given the state, which is exactly "
            "the value we want."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def result(self, d):
        t, ee, en = np.asarray(d["times"]), np.asarray(d["EE_exact"]), np.asarray(d["EE_net"])
        g = axes([0, 10], [0, max(max(ee), max(en)) * 1.2], x_length=7.4, y_length=4.4, xlabel=r"years",
                 ylabel=r"EE, \$ million", xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 2, 4, 6], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        le = curve(ax, np.r_[0, t], np.r_[0, ee], EXPO, stroke_width=3.5)
        ln = VGroup(*[Dot(ax.c2p(a, b), color=GOOD, radius=0.06) for a, b in zip(t, en)])
        err = 100 * (d["cva_net"] / d["cva_exact"] - 1)
        side = VGroup(
            legend([(EXPO, r"exact Hull--White values"), (GOOD, r"the network's")], font_size=17),
            MathTex(rf"\text{{CVA: exact }} {1e3 * d['cva_exact']:.0f}\text{{k}},\ \text{{network }} "
                    rf"{1e3 * d['cva_net']:.0f}\text{{k}}\ ({err:+.0f}\%)", font_size=22),
            MathTex(rf"\text{{RMSE of values}} = {d['rmse']:.2f}\ \text{{vs spread}}\ {d['scale']:.1f}", font_size=22),
            wrapped_label(r"fresh paths, not the training ones. Exposure keeps only the positive part, so small errors in "
                          r"value become a bias in EE near zero; that is the part a desk checks against an exact "
                          r"model wherever one exists", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "On fresh paths, the network's values against the exact ones, turned into expected exposure. "
            "<bookmark mark='a'/> The profile follows the exact one. <bookmark mark='b'/> The CVA from the network is "
            f"{1e3 * d['cva_net']:.0f} thousand against {1e3 * d['cva_exact']:.0f} exact, {abs(err):.0f} percent "
            f"{'high' if err > 0 else 'low'}. The values themselves are close; the exposure takes only their positive "
            "part, so small errors near zero become a bias. A desk would use such a network only where it can still be "
            "checked against a method it trusts."
        ) as vo:
            self.play(FadeIn(g), Create(le), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in ln], lag_ratio=0.05, run_time=2))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
        q = ask(r"a network prices a book's future values 50 times faster than the model it learned from. When is it "
                r"safe to use it for capital?")
        with self.voiceover("A network prices a book's future values fifty times faster than the model it learned from. "
                            "When is it safe to use it for capital?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
