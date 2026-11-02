from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GOOD, NET, OPT, PART, REF, illustration, load


class DML(VoiceoverScene):
    def construct(self):
        d = load("dml")
        self.card()
        self.idea(d)
        self.slice(d)
        self.errors(d)

    def card(self):
        c = chapter_card(4, r"Differential machine learning", r"What if every training label came with its derivatives?",
                         part=PART)
        with self.voiceover("Chapter four. Differential machine learning."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self, d):
        rows = [cmath(r"\mathcal{L}(\theta)", r"=", r"\mathbb{E}\big[(f_\theta(x) - y)^2\big] + \lambda\,"
                      r"\mathbb{E}\big[\lVert \nabla_x f_\theta(x) - \partial y / \partial x \rVert^2\big]", font_size=34,
                      colors={r"\mathcal{L}(\theta)": NET})]
        whys = [why(r"Huge and Savine (2020): a desk's training label is one simulated payoff $y$ from a state $x$, noisy but "
                    rf"unbiased. Adjoint differentiation (Part 16) gives its pathwise derivatives almost free, so each "
                    rf"sample carries {d['d'] + 1} labels instead of one, and the network is fitted to both")]
        step = ladder(self, rows, whys, keep=1, top=2.2, x=-0.6, buff=1.0, edge=6.9)
        foot = wrapped_label(rf"the test: a basket call on {d['d']} correlated assets with normal (Bachelier) dynamics, where "
                             r"the exact price and deltas are known, so every error can be measured", 11.0, 21,
                             GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Chapter one's network learned from exact prices. A real desk does not have them: it has simulations. Each "
            "training example is one simulated payoff from some starting state, noisy but right on average. Brian Huge "
            "and Antoine Savine at Danske Bank noticed what else the desk has. Adjoint differentiation, from Part "
            "sixteen, gives the derivative of that payoff with respect to every input for almost nothing. "
            f"<bookmark mark='a'/> So each sample carries {d['d'] + 1} labels instead of one, and the network is fitted "
            "to the payoff and its derivatives together, by differentiating the network itself. The test: a basket "
            f"option on {d['d']} assets, where the right answer is known exactly."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def slice(self, d):
        s = d["slice"]
        u = np.asarray(s["u"])
        g = axes([-30, 30], [0, 32], x_length=7.4, y_length=4.4, xlabel=r"basket level relative to the strike",
                 ylabel=r"basket call price", xticks=[-20, 0, 20], yticks=[0, 10, 20, 30],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, min(y, 32)), radius=0.025, color=GREY_D)
                        for x, y in zip(s["scatter_B"], s["scatter_Y"]) if -30 <= x <= 30])
        ex = DashedVMobject(curve(ax, u, np.asarray(s["exact"]), REF, stroke_width=2.5), num_dashes=40)
        pl = curve(ax, u, np.clip(np.asarray(s["plain"]), 0, 32), BAD, stroke_width=3)
        df = curve(ax, u, np.clip(np.asarray(s["diff"]), 0, 32), GOOD, stroke_width=3.5)
        leg = legend([(GREY_B, r"training labels: one simulated payoff each"), (REF, r"exact price"),
                      (BAD, r"network fitted to payoffs"), (GOOD, r"fitted to payoffs and derivatives")], font_size=16)
        leg.next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        side = wrapped_label(r"1{,}024 samples. On payoffs alone the network chases the noise; the derivatives pin down its "
                             r"slope everywhere, and the price comes with them", 4.0, 19, GREY_A).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        src = illustration(r"a slice along equal moves of all seven assets")
        with self.voiceover(
            "Here is a slice through the seven-dimensional price, along equal moves in every asset. The grey dots are the "
            "training labels: each one a single simulated payoff, scattered far from the price. "
            "<bookmark mark='a'/> A network fitted to them alone, with a thousand samples, drifts away from the truth "
            "where the payoffs are largest and noisiest. "
            "<bookmark mark='b'/> Fitted to the payoffs and their derivatives, it lies on the exact price: the slopes "
            "fix its shape everywhere, and the level comes with them."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(dots), FadeIn(leg[0]), Create(ex), FadeIn(leg[1]))
            vo.wait_until("a")
            self.play(Create(pl), FadeIn(leg[2]))
            vo.wait_until("b")
            self.play(Create(df), FadeIn(leg[3]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def errors(self, d):
        rows = d["rows"]
        ns = sorted({r["n"] for r in rows})
        g1 = axes([np.log10(ns[0]) - 0.2, np.log10(ns[-1]) + 0.2], [-1.2, 1.0], x_length=5.2, y_length=3.6,
                  xlabel=r"training samples", ylabel=r"price error (RMSE)", xticks=list(np.log10(ns)),
                  xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yticks=[-1, 0, 1],
                  yfmt=lambda v: f"10^{{{int(round(v))}}}", font_size=14, log_x=True)
        g2 = axes([np.log10(ns[0]) - 0.2, np.log10(ns[-1]) + 0.2], [-3, 0], x_length=5.2, y_length=3.6,
                  xlabel=r"training samples", ylabel=r"delta error (RMSE)", xticks=list(np.log10(ns)),
                  xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yticks=[-3, -2, -1, 0],
                  yfmt=lambda v: f"10^{{{int(round(v))}}}", font_size=14, log_x=True)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).shift(DOWN * 0.3)
        lines = VGroup()
        for g, key, lo, hi in ((g1, "price_rmse", -1.2, 1.0), (g2, "delta_rmse", -3, 0)):
            for use, col in ((False, BAD), (True, GOOD)):
                rr = sorted([r for r in rows if r["differential"] == use], key=lambda r: r["n"])
                pts = [g.ax.c2p(np.log10(r["n"]), np.clip(np.log10(r[key]), lo, hi)) for r in rr]
                lines.add(VGroup(VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(pts),
                                 *[Dot(p_, radius=0.06, color=col) for p_ in pts]))
        leg = legend([(BAD, r"payoffs only"), (GOOD, r"payoffs and derivatives")], font_size=18).to_edge(UP, buff=0.4)
        r0 = {(r["n"], r["differential"]): r for r in rows}
        n0 = ns[0]
        k_eq = next((n for n in ns if r0[(n, False)]["price_rmse"] <= r0[(n0, True)]["price_rmse"]), None)
        txt = (rf"with {n0} samples and derivatives the price is as good as with {k_eq:,} without".replace(",", "{,}")
               if k_eq else rf"with {n0} samples and derivatives the price beats every plain fit up to {ns[-1]:,}".replace(",", "{,}"))
        foot = wrapped_label(txt + rf"; the deltas are {r0[(n0, False)]['delta_rmse'] / r0[(n0, True)]['delta_rmse']:.0f} "
                             r"times more accurate. Desks train such networks on a whole book overnight, then reprice it "
                             r"and its risks in one pass", 11.8, 20, GREY_A).to_edge(DOWN, buff=0.35)
        gain = r0[(n0, False)]["delta_rmse"] / r0[(n0, True)]["delta_rmse"]
        cmp = (f"as well as a plain network trained on {k_eq:,} samples" if k_eq else
               "better than any plain network here")
        with self.voiceover(
            "And here is the error as the training set grows, for the price on the left and the deltas on the right. "
            f"<bookmark mark='a'/> With {n0} samples and derivatives, the network prices {cmp}, and its deltas are "
            f"{gain:.0f} times more accurate. The derivatives are not decoration: for a risk system they are the point."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lines], FadeIn(foot), run_time=2.5)
        self.wait(0.5)
        self.clear_scene()
