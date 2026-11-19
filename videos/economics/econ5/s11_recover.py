from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403


class Recover(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Recovering preferences", r"How much of someone's tastes do eleven choices pin down?",
             "Chapter nine. Recovering preferences.")
        self.bounds()
        self.forecast()

    def bounds(self):
        v = load("varian")
        P, X = np.array(v["P"]), np.array(v["X"])
        k = int(v["k"])
        ax = goods_axes(center=LEFT * 3.0 + DOWN * 0.25, top=13, x_length=5.3, y_length=5.3)
        a = ax.ax
        worse = VGroup()
        for i in v["worse"]:
            m = P[i] @ X[i]
            worse.add(Polygon(a.c2p(0, 0), a.c2p(min(m / P[i, 0], 13), 0),
                              a.c2p(min(m / P[i, 0], 13), max(0, (m - P[i, 0] * min(m / P[i, 0], 13)) / P[i, 1])),
                              a.c2p(0, min(m / P[i, 1], 13)), stroke_width=0, fill_color=VIOL, fill_opacity=0.18))
        hull = np.array(v["better"])
        pts = [a.c2p(hull[0, 0], 13)] + [a.c2p(x, y) for x, y in hull] + [a.c2p(13, hull[-1, 1]), a.c2p(13, 13)]
        better = Polygon(*pts, stroke_color=PASS, stroke_width=2, fill_color=PASS, fill_opacity=0.18)
        dots = VGroup(*[Dot(a.c2p(*x), radius=0.07, color=WHO["bo"]) for x in X])
        star = Dot(a.c2p(*X[k]), radius=0.12, color=WHITE)
        xs = np.array(v["xs"])
        true_ic = curve(ax, xs, np.array(v["true_ic"]), color=E.TRUTH, width=3, top=13, dashed=True)
        rows = VGroup(
            label(r"one of Bo's choices: \ 3.8 fish, \ 2.2 coconuts", font_size=23, color=WHITE),
            label(r"red: \ every bundle he could have had \\ on a budget where he chose something \\ revealed no "
                  r"better: \ \emph{revealed worse}", font_size=21, color=VIOL),
            label(r"green: \ bundles at least as good as choices \\ revealed better, \ and their averages "
                  r"\\ (convex tastes): \ \emph{revealed better}", font_size=21, color=PASS),
            label(r"his true indifference curve must run \\ between the two", font_size=23, color=E.TRUTH),
            label(r"Varian (1982); \ tighter with more data: \\ Blundell, Browning and Crawford (2008)", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"simulated: Bo's eleven choices; the dashed curve is the planted one", corner=DR,
                         font_size=13)
        with self.voiceover(
            "If choices are consistent, how much do they tell us about someone's tastes? Hal Varian showed how to "
            "draw the answer. <bookmark mark='a'/> Take one of Bo's choices: about four fish and two coconuts. "
            "<bookmark mark='b'/> Everything he could have afforded when he chose it, he revealed to be no better. "
            "So is everything affordable on any budget where he chose something that bundle beats. Shade all of "
            "it red: revealed worse. <bookmark mark='c'/> Anything he chose that is revealed better, and, if his "
            "tastes are convex, any average of those, and anything with more of both, is at least as good: green, "
            "revealed better. <bookmark mark='d'/> His true indifference curve, which we planted and the data never "
            "saw, has to run through the gap between them. And it does. <bookmark mark='e'/> With eleven choices "
            "the gap is wide. With hundreds, from the same person over the years, Richard Blundell, Martin Browning "
            "and Ian Crawford showed that the bounds can become tight enough to measure how people respond to "
            "prices, with no functional form assumed at all."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(FadeIn(star, scale=1.6), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(w) for w in worse], lag_ratio=0.3), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(better), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(true_ic), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def forecast(self):
        v = load("varian")
        L = np.array(load("budgets")["lines"])
        X = np.array(v["X"])
        pr = v["predict"]
        A, B = pr["line"]
        ax = goods_axes(center=LEFT * 3.0 + DOWN * 0.25, top=13, x_length=5.3, y_length=5.3)
        a = ax.ax
        old = VGroup(*[budget_line(ax, A_, B_, color=GREY_D, width=1.5) for A_, B_ in L])
        dots = VGroup(*[Dot(a.c2p(*x), radius=0.07, color=WHO["bo"]) for x in X])
        new = budget_line(ax, A, B, color=BUDGET, width=4)

        def on(x):
            return a.c2p(x, B - B / A * x)

        band = Line(on(pr["lo"]), on(pr["hi"]), color=PASS, stroke_width=12, stroke_opacity=0.6)
        ends = VGroup(Dot(on(pr["lo"]), radius=0.08, color=PASS), Dot(on(pr["hi"]), radius=0.08, color=PASS))
        truth = Dot(a.c2p(*pr["truth"]), radius=0.11, color=E.TRUTH)
        rows = VGroup(
            label(rf"a new trip: \ {A:g} fish or {B:g} coconuts", font_size=24, color=BUDGET),
            label(rf"any choice outside {pr['lo']:.1f} to {pr['hi']:.1f} fish \\ would contradict his eleven",
                  font_size=24, color=PASS),
            label(rf"what he buys: \ {pr['truth'][0]:.1f} fish \ (planted)", font_size=24, color=E.TRUTH),
            label(r"a forecast with no model of tastes at all: \\ only consistency", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "The same logic forecasts. <bookmark mark='a'/> Send Bo on a twelfth trip, where his money buys ten fish "
            "or five coconuts. <bookmark mark='b'/> Which choices on this line would keep all twelve consistent? "
            f"Only those between {pr['lo']:.0f} and {pr['hi']:.0f} fish. Anything else would contradict something "
            f"he's already done. <bookmark mark='c'/> He buys {pr['truth'][0]:.0f}: inside the band, as it must be. "
            "<bookmark mark='d'/> No utility function was assumed, no curve fitted. The forecast comes from "
            "consistency alone. It's wide, but it's honest about what eleven receipts can and can't tell you."
        ) as vo:
            self.play(FadeIn(ax), LaggedStart(*[Create(l_) for l_ in old], lag_ratio=0.05),
                      LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(Create(new), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(band), FadeIn(ends), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(truth, scale=1.6), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
