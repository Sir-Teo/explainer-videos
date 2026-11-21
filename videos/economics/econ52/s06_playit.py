from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403

FIFTH = (r"the poorest fifth", r"the second fifth", r"the middle fifth", r"the fourth fifth", r"the richest fifth")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Play it: \ rates fall", r"Whose spending moves, \ and why?",
             "Chapter five. Play it: rates fall.", lit={2018: r"Kaplan, Moll and Violante"},
             scale=("household", "nation"), horizon=("a year",))
        self.ask()
        self.reveal()
        self.why()

    def ask(self):
        P = load("playit")
        H_ = load("hank")
        ax = plane([0, 12], [-0.3, 0], center=LEFT * 3.3 + UP * 0.6, x_length=5.2, y_length=2.6,
                   xticks=[0, 4, 8, 12], yticks=[-0.3, -0.2, -0.1, 0], xlabel=r"quarters",
                   ylabel=r"real rate, \ points", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}".replace("-", "{-}"), font_size=13)
        dr = 100 * np.array(H_["dr"])
        cut = path(ax, np.arange(13), dr[:13], DIRECT, 3.0, smooth=False)
        econ = VGroup(
            label(rf"the Island's economy: \ households with \\ about {P['liquid']:.0f} quarters of income in "
                  r"savings, \\ and output set by spending", font_size=18, color=WHITE),
            label(rf"on average they spend {100 * P['mpc']:.0f}\% of a windfall \\ within the quarter", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax, DOWN, buff=0.55).align_to(ax, LEFT)
        q = label(r"Which fifth of households, \ by wealth, \\ raises its spending the most \\ in the first quarter, "
                  r"\ as a share \\ of what it spent before?", font_size=23, color=E.ACCENT).to_edge(
            RIGHT, buff=0.5).shift(UP * 1.9)
        opts = VGroup()
        for t, c in zip((r"the poorest", r"the second", r"the middle", r"the richest"),
                        (FIFTHS[0], FIFTHS[1], FIFTHS[2], FIFTHS[4])):
            b = RoundedRectangle(width=2.6, height=0.8, corner_radius=0.1, stroke_color=c, stroke_width=2,
                                 fill_color=c, fill_opacity=0.1)
            opts.add(VGroup(b, label(t, font_size=20, color=c).move_to(b)))
        opts.arrange_in_grid(rows=2, cols=2, buff=0.25).next_to(q, DOWN, buff=0.45).align_to(q, RIGHT)
        ring = countdown().scale(0.55).next_to(opts, DOWN, buff=0.4)
        with self.voiceover(
            "Your turn. The central bank cuts the real interest rate by a quarter of a point, starting next "
            "quarter, and lets the cut fade over about a year. <bookmark mark='a'/> The economy is the Island's: "
            f"households hold about {P['liquid']:.0f} quarters of income in savings they can use, they spend on "
            f"average {100 * P['mpc']:.0f} percent of a windfall within the quarter, and output is whatever they "
            "buy. <bookmark mark='b'/> Line the households up by wealth and cut them into fifths. Which fifth raises "
            "its spending the most in the first quarter, as a share of what it spent before? <bookmark mark='c'/> "
            "The poorest, the second fifth, the middle, or the richest? Pause, and choose."
        ) as vo:
            self.play(FadeIn(ax), Create(cut), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(econ, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(o) for o in opts], lag_ratio=0.3), FadeIn(ring), run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.clear_scene()

    def reveal(self):
        P = load("playit")
        rows = P["rows"]
        top = max(r["total"] for r in rows)
        ax = plane([-0.5, 4.5], [0, 1.4], center=LEFT * 1.4 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                   xticks=[], yticks=[0, 0.4, 0.8, 1.2], ylabel=r"rise in spending, \ first quarter, \ \%",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        bars = VGroup()
        for i, r in enumerate(rows):
            p0, p1 = ax.ax.c2p(i - 0.32, 0), ax.ax.c2p(i + 0.32, r["total"])
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=FIFTHS[i],
                               fill_opacity=0.85).move_to((p0 + p1) / 2))
        names = VGroup(*[label(t.replace("the ", "").replace(" fifth", ""), font_size=17, color=FIFTHS[i]).next_to(
            ax.ax.c2p(i, 0), DOWN, buff=0.2) for i, t in enumerate(FIFTH)])
        vals = VGroup(*[label(rf"{r['total']:.2f}\%", font_size=17, color=WHITE).next_to(b, UP, buff=0.08)
                        for r, b in zip(rows, bars)])
        win = max(range(5), key=lambda i: rows[i]["total"])
        side = VGroup(
            label(rf"{FIFTH[win]}: \\ {rows[win]['total']:.2f}\%", font_size=21, color=FIFTHS[win]),
            label(rf"all households: \\ {P['total_pct']:.2f}\%", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        tag = island_tag(r"the Island's HANK economy \ (computed)", corner=DR, font_size=12)
        del top
        with self.voiceover(
            "Here is the first quarter. <bookmark mark='a'/> Every fifth spends more, but not equally. <bookmark "
            f"mark='b'/> The largest rise is in {FIFTH[win]}: {rows[win]['total']:.2f} percent. <bookmark "
            f"mark='c'/> The richest fifth raise their spending least, by {rows[-1]['total']:.2f} percent, and the "
            f"poorest by {rows[0]['total']:.2f}. Across everyone, spending rises {P['total_pct']:.2f} percent. If "
            "you chose the poorest, you were close, and for an interesting reason: their rise comes almost "
            "entirely from somewhere other than the interest rate."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(names), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), run_time=2.0)
            self.play(FadeIn(vals))
            vo.wait_until("b")
            self.play(Indicate(bars[win], color=WHITE), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def why(self):
        P = load("playit")
        rows = P["rows"]
        ax = plane([-0.5, 4.5], [0, 1.4], center=LEFT * 1.4 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                   xticks=[], yticks=[0, 0.4, 0.8, 1.2], ylabel=r"rise in spending, \ first quarter, \ \%",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        dirb, indb = VGroup(), VGroup()
        for i, r in enumerate(rows):
            d = max(r["direct"], 0.0)
            p0, p1 = ax.ax.c2p(i - 0.32, 0), ax.ax.c2p(i + 0.32, d)
            dirb.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0,
                               fill_color=DIRECT, fill_opacity=0.85).move_to((p0 + p1) / 2))
            q0, q1 = ax.ax.c2p(i - 0.32, d), ax.ax.c2p(i + 0.32, d + r["indirect"])
            indb.add(Rectangle(width=q1[0] - q0[0], height=max(q1[1] - q0[1], 0.01), stroke_width=0,
                               fill_color=INDIRECT, fill_opacity=0.85).move_to((q0 + q1) / 2))
        names = VGroup(*[label(t.replace("the ", "").replace(" fifth", ""), font_size=17, color=FIFTHS[i]).next_to(
            ax.ax.c2p(i, 0), DOWN, buff=0.2) for i, t in enumerate(FIFTH)])
        share = VGroup(*[label(rf"{100 * r['wealth_share']:.0f}\%", font_size=15, color=GREY_A).next_to(
            names[i], DOWN, buff=0.1) for i, r in enumerate(rows)])
        slab = label(r"share of wealth", font_size=14, color=GREY_A).next_to(share, LEFT, buff=0.25)
        side = VGroup(
            label(r"blue: \ the rate itself \\ (incomes held fixed)", font_size=19, color=DIRECT),
            label(r"gold: \ through incomes, \\ as others spend", font_size=19, color=INDIRECT),
            label(r"the poorest cannot borrow: \\ a cheaper loan they \\ cannot take means little; \\ a fatter "
                  r"paycheque \\ is spent", font_size=18, color=POOR),
            label(r"the richest respond to \\ the rate, \ and little \\ to their pay", font_size=18, color=RICH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Split each bar in two. <bookmark mark='a'/> The blue part is the direct effect: how each fifth would "
            "respond to the lower rate if its income did not change. <bookmark mark='b'/> The gold part is the "
            "indirect effect: other households spend more, firms produce more, and incomes rise. <bookmark "
            f"mark='c'/> For the poorest fifth, the direct effect is almost nothing, {rows[0]['direct']:.2f} percent. "
            "They are at or near their borrowing limit: a cheaper loan they cannot take means little to them, but a "
            "fatter paycheque is spent at once. <bookmark mark='d'/> The richest fifth respond mostly to the rate "
            "itself, and their pay is a small part of their resources. <bookmark mark='e'/> And the two groups who "
            "matter most for spending own almost none of the wealth: the poorest two fifths hold "
            f"{100 * (rows[0]['wealth_share'] + rows[1]['wealth_share']):.0f} percent of it. A representative "
            "household, who owns the average wealth, cannot see any of this."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in dirb], lag_ratio=0.15), FadeIn(side[0]),
                      run_time=1.6)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in indb], lag_ratio=0.15), FadeIn(side[1]),
                      run_time=1.6)
            vo.wait_until("c")
            self.play(Indicate(VGroup(dirb[0], indb[0]), color=WHITE), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Indicate(VGroup(dirb[4], indb[4]), color=WHITE), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(share), FadeIn(slab))
        self.clear_scene()
