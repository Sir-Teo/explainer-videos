from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import quoting as Q
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, illustration, load


class Hedging(VoiceoverScene):
    def construct(self):
        h = load("hedging")
        self.card()
        self.band()
        self.frontier(h)

    def card(self):
        c = chapter_card(7, r"Hedging under costs", r"How often should you rehedge when every trade costs money?",
                         part=PART)
        with self.voiceover("Chapter seven. Hedging under costs."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def band(self):
        S = np.linspace(70, 130, 121)
        b = Q.ww_band(S, 100.0, 15 / 365, 0.6, 0.001, gamma_risk=1.0)
        g = axes([70, 130], [-0.05, 1.05], x_length=6.4, y_length=4.0, xlabel=r"underlying", ylabel=r"hedge, units held "
                 r"(short call)", xticks=[70, 85, 100, 115, 130], yticks=[0, 0.5, 1], font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        band = Polygon(*[ax.c2p(x, y) for x, y in zip(S, np.clip(b["hi"], -0.05, 1.05))],
                       *[ax.c2p(x, y) for x, y in zip(S[::-1], np.clip(b["lo"][::-1], -0.05, 1.05))], stroke_width=0,
                       fill_color=VEGA, fill_opacity=0.3)
        mid = curve(ax, S, b["delta"], OPT, stroke_width=3)
        side = VGroup(
            MathTex(r"\Delta \pm \left(\frac{3\,\lambda\, S\,\Gamma^2}{2\,\gamma}\right)^{1/3}", font_size=36, color=VEGA),
            wrapped_label(r"Whalley and Wilmott (1997): with a proportional cost $\lambda$ and risk aversion $\gamma$, "
                          r"do nothing while the hedge stays inside a band around delta; when it leaves, trade only to "
                          r"the band's edge", 4.4, 20, GREY_A),
            wrapped_label(r"the band is widest where gamma is large, near the strike: there delta moves fastest, and "
                          r"chasing it costs most", 4.4, 20, OPT),
            wrapped_label(r"Leland (1985) instead raises the volatility used for hedging to pay for the costs", 4.4, 19,
                          GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        src = illustration(r"a 15-day call, 60\% vol, 10 bp cost, $\gamma = 1$")
        with self.voiceover(
            "Part ten hedged for free. Real hedging costs money on every trade, and a hedger who chases delta every "
            "minute pays the spread to death. <bookmark mark='a'/> Vlad Whalley and Paul Wilmott found the answer in "
            "1997: a band around delta. Inside it, do nothing. When the hedge drifts out, trade only back to the "
            "band's edge. The band's width grows with the cost and with gamma, and shrinks with how much you mind "
            "risk. <bookmark mark='b'/> It is widest near the strike, where delta moves fastest and chasing it "
            "would cost the most."
        ) as vo:
            self.play(FadeIn(g), Create(mid), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(band), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def frontier(self, h):
        rows = h["rows"]
        g = axes([0.15, 0.5], [0.5, 1.5], x_length=6.6, y_length=4.4, xlabel=r"average trading cost (per 100)",
                 ylabel=r"spread of hedged P\&L (s.d.)", xticks=[0.2, 0.3, 0.4, 0.5], yticks=[0.5, 0.75, 1.0, 1.25, 1.5],
                 font_size=17).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        groups = {"every step": GREY_B, "fixed band": ALT, "Whalley-Wilmott": VEGA, "deep hedge": GAMMA}
        dots, lines = VGroup(), VGroup()
        for name, col in groups.items():
            pts = sorted([(r_["cost"], r_["sd"]) for r_ in rows if r_["rule"] == name and np.isfinite(r_["sd"])])
            if name == "fixed band":
                pts = sorted(pts + [(r_["cost"], r_["sd"]) for r_ in rows if r_["rule"] == "every step"])
            pts = [p for p in pts if 0.15 <= p[0] <= 0.5 and p[1] <= 1.5]
            dots.add(VGroup(*[Dot(ax.c2p(*p), radius=0.07, color=col) for p in pts]))
            lines.add(VMobject(stroke_color=col, stroke_width=2.5).set_points_as_corners([ax.c2p(*p) for p in pts])
                      if len(pts) > 1 else VGroup())
        leg = legend([(GREY_B, r"rehedge every 6 hours"), (ALT, r"fixed bands"), (VEGA, r"Whalley--Wilmott bands"),
                      (GAMMA, r"a learned hedger (deep hedging)")], font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        dh = [r_ for r_ in rows if r_["rule"] == "deep hedge"]
        side = VGroup(
            wrapped_label(r"each point: a short 30-day option on 20{,}000 simulated paths (5{,}000 held out for the "
                          r"learner), costs of 10 bp; lower and to the left is better", 4.2, 19, GREY_A),
            wrapped_label(r"the learned hedger: a network reads time, moneyness and its current hedge, and chooses "
                          r"how far to move toward delta; trained through the simulator to minimize variance plus "
                          r"$\kappa$ times cost (Buehler et al.\ 2019)", 4.2, 19, GAMMA),
            wrapped_label(r"Whalley--Wilmott's simple band is hard to beat; the learner lands just inside it at each of "
                          r"three cost weights, without being told the shape of the answer", 4.2, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        src = illustration(r"geometric Brownian motion at 60\%; 120 rebalancing points")
        with self.voiceover(
            "Compare the rules on the same twenty thousand simulated paths. Lower is less risk, further left is "
            "less cost. Rehedging every six hours is the least risky and the most expensive. <bookmark mark='a'/> "
            "Fixed bands and Whalley-Wilmott bands trade risk for cost along curves, and the Whalley-Wilmott curve "
            "is the better of the two. <bookmark mark='b'/> Then a learned hedger: a small network that reads the "
            "time, the moneyness and its current hedge, and decides how far to move toward delta, trained through "
            "the simulator to minimize risk plus a price on costs, the deep hedging of Hans Bühler and coauthors. "
            "<bookmark mark='c'/> It is not told about bands, and at each of three prices on cost it lands just "
            "inside the Whalley-Wilmott curve. The classical answer was already very good; the learner's value is that it would work the same "
            "way for a book of many options, or a model with no formula."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg[0]), FadeIn(dots[0]), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(leg[1]), FadeIn(leg[2]), Create(lines[1]), Create(lines[2]), FadeIn(dots[1]),
                      FadeIn(dots[2]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(leg[3]), FadeIn(side[1]), FadeIn(dots[3]), Create(lines[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
