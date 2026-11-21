from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


class Discount(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Discounting", r"How much is a benefit in fifty years worth today?",
             "Chapter six. Discounting.", lit={1928: r"Ramsey", 1998: r"Weitzman", 2026: r"the Green Book's 3\%"},
             scale=("nation", "world"), horizon=("a decade", "a century"))
        self.factors()
        self.bridge()
        self.rules()
        self.weitzman()

    def factors(self):
        D = load("discount")
        t = np.array(D["t"])
        ax = plane([0, 100], [0, 1.0], center=LEFT * 2.6 + DOWN * 0.4, x_length=7.0, y_length=4.8,
                   xticks=[0, 25, 50, 75, 100], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"years from now",
                   ylabel=r"what a dollar then is worth now", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                   font_size=15)
        curves = [(D["df_2"], BEN, r"2\%"), (D["df_35"], RATE, r"3.5\%"), (D["df_7"], COST, r"7\%")]
        lines = VGroup(*[path(ax, t, df, c_, 3.0, smooth=False) for df, c_, _ in curves])
        labs = VGroup(*[label(n_, font_size=19, color=c_).next_to(ax.ax.c2p(x_, df[x_]), UR, buff=0.06)
                        for (df, c_, n_), x_ in zip(curves, (55, 35, 18))])
        v30 = vline(ax, 30, 0, 1.0, GREY_C, 1.5)
        p30 = D["pound30"]
        side = VGroup(
            MathTex(r"PV = \sum_t \frac{B_t - C_t}{(1 + r)^t}", font_size=32, color=WHITE),
            label(r"a dollar in thirty years, \ today:", font_size=21, color=GREY_A),
            label(rf"at 2\%: \ {100 * p30['0.02']:.0f} cents", font_size=22, color=BEN),
            label(rf"at 3.5\%: \ {100 * p30['0.035']:.0f} cents", font_size=22, color=RATE),
            label(rf"at 7\%: \ {100 * p30['0.07']:.0f} cents", font_size=22, color=COST),
            label(rf"in a hundred years, \ at 7\%: \ {100 * D['pound100']['0.07']:.1f} cents", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Costs come first and benefits later, so everything turns on how the future is weighed against the "
            "present. <bookmark mark='a'/> A dollar in t years counts as one over one plus r, to the power t. "
            "<bookmark mark='b'/> At two percent a year, a dollar in thirty years is worth "
            f"{100 * p30['0.02']:.0f} cents today; at three and a half, {100 * p30['0.035']:.0f}; at seven, "
            f"{100 * p30['0.07']:.0f}. <bookmark mark='c'/> A hundred years out, at seven percent, a dollar is worth "
            f"{100 * D['pound100']['0.07']:.1f} cents: at that rate, nothing that happens to our great-grandchildren "
            "counts for much."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[Create(l_) for l_ in lines], FadeIn(labs), Create(v30), FadeIn(side[1:5]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def bridge(self):
        B, D = load("bridge"), load("discount")
        r, v = 100 * np.array(B["rates"]), np.array(B["npv"])
        ax = plane([0, 10], [-200, 700], center=LEFT * 2.4 + DOWN * 0.4, x_length=7.4, y_length=5.0,
                   xticks=[0, 2, 4, 6, 8, 10], yticks=[-200, 0, 200, 400, 600], xlabel=r"discount rate, \ \%",
                   ylabel=r"the bridge's NPV, \ millions", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:+.0f}".replace("-", "{-}") if y else "0", font_size=15)
        z = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(10, 0), color=GREY_C, stroke_width=1.5)
        curve = path(ax, r, v, RATE, 3.2, yr=(-200, 700))
        irr = dot(ax, 100 * B["irr"], 0, WHITE, 0.09)
        il = label(rf"IRR {100 * B['irr']:.1f}\%", font_size=19, color=WHITE).next_to(irr, UR, buff=0.1)
        marks = VGroup()
        for rr, c_ in ((0.03, BEN), (0.035, RATE), (0.07, COST)):
            npv = D["bridge"][f"{rr:.3f}"]
            marks.add(VGroup(dot(ax, 100 * rr, npv, c_, 0.08),
                             label(f"{100 * rr:g}\\%: \\ ${npv:+.0f}$".replace("-", "{-}"), font_size=17,
                                   color=c_).next_to(ax.ax.c2p(100 * rr, npv), UR if rr < 0.05 else UP, buff=0.1)))
        gb = D["bridge"]["gb2003"]
        side = VGroup(
            label(r"the higher the rate, \ the less the century of crossings counts", font_size=19, color=GREY_A),
            label(rf"the Green Book's declining schedule: \ ${gb:+.0f}$".replace("-", "{-}"), font_size=20,
                  color=RATE),
            label(r"the internal rate of return: \ the rate at which NPV $= 0$", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(UP * 1.2)
        tag = island_tag(r"the Island's bridge", corner=DR, font_size=12)
        with self.voiceover(
            "For the bridge, the rate decides. <bookmark mark='a'/> Its net present value falls as the rate rises, "
            "because the costs come in the first three years and the benefits over a century. <bookmark mark='b'/> "
            f"At three percent the bridge is worth {D['bridge']['0.030']:.0f} million; at three and a half, "
            f"{D['bridge']['0.035']:.0f}; at seven, it loses {abs(D['bridge']['0.070']):.0f} million. <bookmark "
            f"mark='c'/> The rate at which it breaks even, its internal rate of return, is {100 * B['irr']:.1f} "
            "percent. Whether the Island builds depends on whether the rate the ministry uses is above or below "
            "that, and so the rate is not a technicality. It is the decision."
        ) as vo:
            self.play(FadeIn(ax), Create(z), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.4), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(irr, scale=1.5), FadeIn(il), FadeIn(side[2]))
        self.clear_scene()

    def rules(self):
        T = tables.DISCOUNT_58.data
        eq = MathTex(r"r = \underbrace{0.5\%}_{\text{impatience}} + \underbrace{1.0\%}_{\text{catastrophe}} + "
                     r"\underbrace{1.0}_{\eta} \times \underbrace{2.0\%}_{\text{growth}} = 3.5\%", font_size=34,
                     color=WHITE).to_edge(UP, buff=0.5)
        ax = plane([0, 300], [0, 4], center=LEFT * 3.4 + DOWN * 1.0, x_length=5.4, y_length=3.0,
                   xticks=[0, 30, 75, 125, 200, 300], yticks=[0, 1, 2, 3, 4], xlabel=r"years ahead",
                   ylabel=r"the Green Book's rate, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=13)
        steps = [(0, 30, 3.5), (31, 75, 3.0), (76, 125, 2.5), (126, 200, 2.0), (201, 300, 1.5)]
        st = VGroup(*[seg(ax, a, r_, b, r_, RATE, 3.5) for a, b, r_ in steps])
        new = seg(ax, 0, 3.0, 30, 3.0, BEN, 3.5)
        nl = label(r"2026: \ 3.0\%", font_size=16, color=BEN).next_to(ax.ax.c2p(30, 3.0), RIGHT, buff=0.1).shift(
            DOWN * 0.15)
        tl = VGroup(
            history_card(2003, r"HM Treasury, \ the Green Book", r"3.5\% for thirty years, \ declining after",
                         color=RATE,
                         width=5.6, font_size=18),
            history_card(2003, r"OMB Circular A-4", r"7\% (the return on private capital) \ and 3\% (consumers' "
                         r"rate), \ both reported", color=COST, width=5.6, font_size=18),
            history_card(2023, r"OMB's revision", rf"{T['omb_2023']:.1f}\%, \ from thirty years of real Treasury "
                         r"yields; \ rescinded in February 2025", color=BEN, width=5.6, font_size=18),
            history_card(2026, r"the Treasury's review", r"Freeman and Groom: \ 3.00\% for years 1 to 30, \ "
                         r"accepted in October", color=BEN, width=5.6, font_size=18),
        ).arrange(DOWN, buff=0.16).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.35)
        tag = published_tag(tables.DISCOUNT_58.tag, corner=DL, font_size=12)
        with self.voiceover(
            "So governments write the rate down. <bookmark mark='a'/> Britain's Treasury builds it from Frank Ramsey's "
            "rule: half a percent for pure impatience, one percent for the risk that some catastrophe makes the "
            "future irrelevant, and the growth of consumption, two percent, times how fast the value of an extra "
            "pound falls as people get richer, one. Three and a half percent. <bookmark mark='b'/> For long horizons "
            "the Green Book steps the rate down: three percent after thirty years, then two and a half, two, one and "
            "a half. <bookmark mark='c'/> America's budget office took another view in 2003: money for a project "
            "could otherwise have been invested, at about seven percent, or consumed, at about three, so report "
            "both. <bookmark mark='d'/> In 2023 it cut the main rate to two percent, from the real yield on "
            "Treasury bonds over thirty years, and in February 2025 a new administration rescinded the revision and "
            "brought the 2003 rates back. <bookmark mark='e'/> In October 2026, after a review by Mark Freeman and "
            "Ben Groom, Britain's Treasury accepted a cut of its headline rate to three percent, the first change in "
            "about a quarter of a century. The same bridge passes at one ministry and fails at another."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ax), LaggedStart(*[Create(s_) for s_ in st], lag_ratio=0.3), FadeIn(tl[0]),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(tl[1], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(tl[2], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(tl[3], shift=UP * 0.1), Create(new), FadeIn(nl))
        self.clear_scene()

    def weitzman(self):
        D = load("discount")
        W = D["weitzman"]
        h, rate, fwd = np.array(W["horizon"]), 100 * np.array(W["rate"]), 100 * np.array(W["forward"])
        ax = plane([0, 300], [0, 8], center=LEFT * 2.6 + DOWN * 0.4, x_length=7.0, y_length=4.8,
                   xticks=[0, 50, 100, 150, 200, 250, 300], yticks=[0, 1, 2, 4, 7, 8], xlabel=r"years ahead",
                   ylabel=r"the rate to use, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=15)
        r1 = seg(ax, 0, 1, 300, 1, BEN, 1.8, dashed=True)
        r7 = seg(ax, 0, 7, 300, 7, COST, 1.8, dashed=True)
        cf = path(ax, h, fwd, RATE, 3.2)
        ca = path(ax, h, rate, WHITE, 2.2)
        tips = D["tips_annual"]
        side = VGroup(
            label(r"the right rate is 1\% or 7\%, \ equally likely", font_size=20, color=GREY_A),
            MathTex(r"\bar{P}_t = \tfrac12 (1.01)^{-t} + \tfrac12 (1.07)^{-t}", font_size=28, color=WHITE),
            label(r"pink: \ the rate from year $t$ to $t+1$", font_size=19, color=RATE),
            label(r"white: \ the average rate from today", font_size=19, color=WHITE),
            label(rf"the market's real rate: \ {D['tips_mean']:.2f}\% \ (10-year TIPS, \ 2003--2025)", font_size=19,
                  color=CBO),
            label(rf"\ \ \ from {min(tips.values()):.1f}\% to {max(tips.values()):.1f}\% a year".replace("-", "{-}"),
                  font_size=17, color=CBO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Weitzman, \emph{JEEM} (1998), \emph{AER} (2001); \ FRED: \ DFII10", corner=DL,
                            font_size=12)
        with self.voiceover(
            "Why should the rate fall with the horizon at all? Martin Weitzman's argument, from 1998: <bookmark "
            "mark='a'/> suppose no one knows whether the right rate for the next centuries is one percent or seven, "
            "and each is equally likely. <bookmark mark='b'/> Then the value today of a dollar in t years is the "
            "average of the two discount factors, not the factor at the average rate. <bookmark mark='c'/> The "
            "seven percent world's factor shrinks so fast that, far out, only the one percent world still counts, "
            "and the rate from each year to the next falls towards the lowest possible rate. <bookmark mark='d'/> "
            "The average rate from today falls more slowly, the shape the Green Book's steps approximate. <bookmark "
            "mark='e'/> And the market's own real rate has moved a long way: the yield on ten-year inflation-"
            f"protected Treasuries averaged {D['tips_mean']:.2f} percent from 2003 to 2025, below zero in some "
            "years and above two in others."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(r1), Create(r7), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cf), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(ca), FadeIn(side[3]), run_time=1.6)
            vo.wait_until("e")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.clear_scene()
