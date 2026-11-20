from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403


class Dornbusch(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Overshooting", r"Why do exchange rates jump more than the news?",
             "Chapter seven. Overshooting.",
             lit={1976: r"Dornbusch"}, scale=("nation", "world"), horizon=("a day", "a few years"))
        self.derive()
        self.paths()

    def derive(self):
        D = load("dornbusch")
        eqs = VGroup(
            label(r"goods prices are sticky; \ asset prices are not", font_size=26, color=E.ACCENT),
            MathTex(r"m - p = -\lambda\,(i - i^{*}) \qquad \text{(money market)}", font_size=34, color=WHITE),
            MathTex(r"i - i^{*} = E[\dot s] = \theta\,(\bar s - s) \qquad \text{(interest parity)}", font_size=34,
                    color=USD),
            label(r"money up by $\Delta m$: \ in the long run $\bar s$ and $p$ rise by $\Delta m$; \ today $p$ cannot",
                  font_size=21, color=GREY_A),
            MathTex(r"\Rightarrow\; i \text{ falls by } \frac{\Delta m}{\lambda} \;\Rightarrow\; "
                    r"s_0 - \bar s = \frac{\Delta m}{\lambda\,\theta}", font_size=36, color=GBP),
            label(rf"the Island: \ $\lambda = {D['lam']:.0f}$, \ $\theta = {D['theta']:.1f}$: \ the currency jumps "
                  rf"{D['factor']:.1f} times as far as it ends up", font_size=21, color=PRICE),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Dornbusch, \ ``Expectations and Exchange Rate Dynamics'', \ \emph{JPE} 84(6) (1976)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Exchange rates swing far more than the fundamentals behind them. Rudiger Dornbusch showed in 1976 that "
            "this needs no irrationality. <bookmark mark='a'/> Goods prices move slowly; asset prices move at once. "
            "<bookmark mark='b'/> In the money market, more money relative to prices must be held at a lower "
            "interest rate. <bookmark mark='c'/> And by interest parity, a lower interest rate at home must be "
            "matched by an expected rise in the currency's value. <bookmark mark='d'/> Now the central bank raises "
            "the money supply for good. In the long run prices and the exchange rate rise in proportion. But today "
            "prices cannot move, <bookmark mark='e'/> so the interest rate falls, and for investors to hold the "
            "currency at that lower rate it must be expected to appreciate from here on. The only way both can be "
            "true is for the currency to fall today by more than it will in the end. <bookmark mark='f'/> On the "
            f"Island's numbers, the currency jumps {D['factor']:.1f} times as far as its final resting place."
        ) as vo:
            self.play(FadeIn(eqs[0]), FadeIn(tag))
            for mk, r_ in zip("bcdef", eqs[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def paths(self):
        D = load("dornbusch")
        t = np.array(D["t"])
        ax = plane([-1, 8], [-0.02, 0.17], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.8, y_length=4.6,
                   xticks=[0, 2, 4, 6, 8], yticks=[0, 0.05, 0.10, 0.15], xlabel=r"years after the rise in money",
                   ylabel=r"\% above the old level", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        tt = np.concatenate([[-1, 0], t])
        s = np.concatenate([[0, 0], D["s"]])
        p = np.concatenate([[0, 0], D["p"]])
        sl = VMobject(stroke_color=GBP, stroke_width=3.5).set_points_as_corners([ax.ax.c2p(a, b) for a, b in
                                                                                  zip(tt, s)])
        pl = path(ax, tt, p, PRICE, 3.2, smooth=False)
        lr = seg(ax, -1, 0.10, 8, 0.10, GREY_C, 1.5, dashed=True)
        side = VGroup(
            label(r"pink: \ the price of foreign currency", font_size=18, color=GBP),
            label(r"gold: \ the price level", font_size=18, color=PRICE),
            label(rf"jump: \ +{100 * D['jump']:.0f}\%; \ long run: \ +10\%", font_size=19, color=WHITE),
            label(r"then it appreciates \\ as prices catch up", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=13)
        with self.voiceover(
            "Here is the path. <bookmark mark='a'/> The money supply rises ten percent at time zero. "
            f"<bookmark mark='b'/> The currency's price jumps {100 * D['jump']:.0f} percent at once, <bookmark "
            "mark='c'/> while prices start to rise only slowly. <bookmark mark='d'/> As prices catch up, the interest "
            "rate recovers and the currency appreciates back toward its new level, ten percent above the old. "
            "Overshooting, in the data, is weaker and slower than in the model; Part thirty-one's identification "
            "problem makes it hard to measure, and the forward premium puzzle of chapter four suggests "
            "the expected appreciation is not there. But the mechanism explains why exchange rates move so much on "
            "news about policy."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(lr), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(sl), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(pl), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
