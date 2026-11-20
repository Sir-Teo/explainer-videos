from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class Wages(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Why wages do not fall", r"If workers are idle, \ why does their pay not drop until they are "
             r"hired?", "Chapter nine. Why wages do not fall.", lit={1936: r"Keynes", 1999: r"Bewley"},
             scale=("person", "firm"), horizon=("a year",))
        self.keynes()
        self.bewley()
        self.spike()

    def keynes(self):
        rows = VGroup(
            label(r"the classical cure: \ wages fall until it pays to hire everyone", font_size=24, color=GREY_A),
            label(r"Keynes's two objections", font_size=27, color=E.ACCENT),
            label(r"1. \ \ money wages are sticky: \ workers resist cuts to their own pay, \ firm by firm",
                  font_size=23, color=RATE),
            label(r"2. \ \ even if all wages fell, \ prices would follow, \ and real wages might not fall at all",
                  font_size=23, color=PRICE),
            label(r"falling prices also raise the burden of debts fixed in money \ (Fisher, \ 1933)", font_size=22,
                  color=HOLD),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Keynes, \emph{The General Theory}, \ chs.\ 2 and 19; \ Fisher, \ Econometrica 1(4) "
                            r"(1933)", corner=DR, font_size=12)
        with self.voiceover(
            "The classical answer to a slump was that wages fall until it pays firms to hire everyone who wants "
            "work. <bookmark mark='a'/> Keynes had two objections. <bookmark mark='b'/> First, money wages are "
            "sticky. Workers resist cuts to their own pay, firm by firm, because a cut is a loss relative to other "
            "workers, even when everyone's pay would fall together. <bookmark mark='c'/> Second, and deeper: even "
            "if all wages did fall, firms' costs would fall, prices would follow, and real wages might not fall at "
            "all. A general cut in money wages is not a cut in real wages. <bookmark mark='d'/> And falling prices "
            "raise the real burden of debts that are fixed in money, which Irving Fisher called debt deflation, "
            "in 1933. That makes spending fall further."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def bewley(self):
        rows = VGroup(
            label(r"Truman Bewley asked the people who set pay", font_size=27, color=E.ACCENT),
            label(r"336 managers, \ union leaders and employment counsellors, \ interviewed in 1992 and 1993, \ "
                  r"during a recession", font_size=22, color=GREY_A),
            label(r"almost none had cut pay", font_size=24, color=RATE),
            label(r"the reason they gave: \ morale; \ a cut feels like an insult, \ and good workers leave first",
                  font_size=23, color=SPEND),
            label(r"so firms laid some people off rather than cut everyone's pay", font_size=23, color=PRICE),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Bewley, \emph{Why Wages Don't Fall during a Recession} (1999); \ Howitt's review",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Why are wages sticky? Truman Bewley went and asked. <bookmark mark='a'/> In 1992 and 1993, during a "
            "recession, he interviewed three hundred and thirty-six managers, union leaders and employment "
            "counsellors about how pay was set. <bookmark mark='b'/> Almost none had cut pay, even with many people "
            "looking for work who would have taken less. <bookmark mark='c'/> The reason they gave was morale. A "
            "pay cut feels like an insult, it makes workers less cooperative, and the best of them, who can find "
            "other jobs, leave first. <bookmark mark='d'/> So firms preferred to lay some people off and keep "
            "everyone else's pay, and the burden of the slump fell on the unemployed."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def spike(self):
        W = load("wages")
        e = np.array(W["edges"])
        mids = 0.5 * (e[1:] + e[:-1])
        ax = plane([-0.12, 0.14], [0, 0.36], center=LEFT * 1.9 + DOWN * 0.3, x_length=8.2, y_length=4.8,
                   xticks=[-0.1, -0.05, 0, 0.05, 0.1], yticks=[0, 0.1, 0.2, 0.3],
                   xlabel=r"change in a worker's pay over a year", ylabel=r"share of workers",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=15)

        def bars(h, color, op):
            g = VGroup()
            for x, y in zip(mids, h):
                lo, hi = ax.ax.c2p(x, 0), ax.ax.c2p(x, max(y, 1e-4))
                bw = abs(ax.ax.c2p(e[1], 0)[0] - ax.ax.c2p(e[0], 0)[0]) * 0.9
                g.add(Rectangle(width=bw, height=hi[1] - lo[1], fill_color=color, fill_opacity=op,
                                stroke_width=0).move_to((lo + hi) / 2))
            return g
        want = bars(W["hist_want"], SPEND, 0.55)
        got = bars(W["hist_got"], RATE, 0.85)
        side = VGroup(
            label(rf"the changes firms would make: \\ {100 * W['share_cut_wanted']:.0f}\% of workers due a cut",
                  font_size=20, color=SPEND),
            label(rf"if four in five cuts are not made: \\ {100 * W['share_zero']:.0f}\% get exactly zero; \\ only "
                  rf"{100 * W['share_cut']:.0f}\% are cut", font_size=20, color=RATE),
            label(r"real pay data show the same spike at zero: \\ Card and Hyslop (1997); \\ Dickens et al.\ (2007)",
                  font_size=19, color=GREY_A),
            label(r"wages cannot fall to clear the market: \\ employment must", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is what stickiness does to the data, on the Island. <bookmark mark='a'/> In blue, the pay changes "
            "firms would make if cuts were as easy as raises: an average rise of one percent, with "
            f"{100 * W['share_cut_wanted']:.0f} percent of workers due for a cut. <bookmark mark='b'/> Now suppose "
            "four in five of those cuts are not made, and the pay is frozen instead. In pink, what workers actually "
            f"get: {100 * W['share_zero']:.0f} percent get exactly zero, a spike, and only "
            f"{100 * W['share_cut']:.0f} percent are cut. <bookmark mark='c'/> Records of real pay show the same "
            "spike at zero, in study after study: David Card and Dean Hyslop's for America, and a project across "
            "sixteen countries led by William Dickens. <bookmark mark='d'/> When wages cannot fall far enough to "
            "clear the market, something else has to adjust, and that something is employment."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in want], lag_ratio=0.02), FadeIn(side[0]),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in got], lag_ratio=0.02), FadeIn(side[1]),
                      run_time=1.5)
            for mk, r_ in zip("cd", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
