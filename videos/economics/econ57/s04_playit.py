from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403

IND = ((r"payrolls", SPF), (r"production", GB), (r"retail sales", LATEST), (r"business survey", NOW))
SHORT = (r"before the quarter", r"month 1: \ the survey", r"month 1: \ hard data", r"month 2", r"month 3")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Play it: \ nowcast the quarter", r"Will GDP fall this quarter? \ Decide as the data arrive.",
             "Chapter three. Play it: nowcast the quarter.", lit={2008: r"Giannone, \ Reichlin and Small"},
             scale=("nation",), horizon=("a day", "a year"))
        self.play_it()

    def play_it(self):
        Isl = load("island")
        X = np.array(Isl["pick_months"])            # 9 months x 4: six before the quarter, then its three
        nc = Isl["pick_nowcasts"]
        months = np.arange(-6, 3)
        axl = plane([-6.4, 2.4], [-4.5, 3.5], center=LEFT * 3.5 + DOWN * 0.4, x_length=5.6, y_length=4.8,
                    xticks=[-6, -4, -2, 0, 2], yticks=[-4, -2, 0, 2], xlabel=r"month \ (0 = the quarter's first)",
                    ylabel=r"monthly indicators, \ standardized", xfmt=lambda v: f"{v:+.0f}".replace("-", "{-}")
                    if v else "0", yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=13)
        q_shade = shade(axl, [(-0.5, 2.4)], -4.5, 3.5, RECESS, 0.45)
        zl = DashedLine(axl.ax.c2p(-6.4, 0), axl.ax.c2p(2.4, 0), color=GREY_D, stroke_width=1)
        axr = plane([-0.5, 5.0], [-9, 7], center=RIGHT * 3.2 + DOWN * 0.4, x_length=5.0, y_length=4.8,
                    xticks=[0, 1, 2, 3, 4], yticks=[-8, -4, 0, 4], xlabel=r"release",
                    ylabel=r"GDP growth this quarter, \ \% a year", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=13)
        zr = DashedLine(axr.ax.c2p(-0.5, 0), axr.ax.c2p(5.0, 0), color=GREY_C, stroke_width=1.2)
        key = VGroup(*[label(n_, font_size=15, color=c_) for n_, c_ in IND]).arrange(RIGHT, buff=0.35)
        key.next_to(axl, UP, buff=0.25)

        def seg_lines(upto):
            """Each indicator's line through the months it has by release ``upto``."""
            g = VGroup()
            for i, (_, col) in enumerate(IND):
                last = -1
                if upto >= 1 and i == 3:
                    last = 0
                if upto >= 2:
                    last = 0
                if upto >= 3:
                    last = 1
                if upto >= 4:
                    last = 2
                keep = months <= last
                g.add(path(axl, months[keep], X[keep, i], col, 2.4, smooth=False))
            return g

        def ncmark(k):
            m, s = nc[k]["mean"], nc[k]["sd"]
            bar = Line(axr.ax.c2p(k, m - s), axr.ax.c2p(k, m + s), color=NOW, stroke_width=4)
            d = Dot(axr.ax.c2p(k, m), radius=0.09, color=NOW)
            return VGroup(bar, d)

        pn = Isl["p_neg"]
        probs = VGroup(*[label(rf"{SHORT[k]}: \ chance of a fall {100 * pn[k]:.0f}\%", font_size=17,
                               color=NOW) for k in range(5)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        probs.to_edge(DOWN, buff=0.25).shift(RIGHT * 2.6)
        tag = island_tag(r"simulated: \ the Island's factor model", corner=DL, font_size=12)
        lines0 = seg_lines(0)
        with self.voiceover(
            "Your turn. This is the Island, in the first days of a quarter. Four monthly indicators arrive at "
            "different times: payrolls, industrial production, retail sales and a business survey, which comes "
            "out first. <bookmark mark='a'/> Before the quarter starts, the six months behind us look ordinary, "
            "apart from one weak month for retail, "
            f"and the nowcast for the quarter's growth is {nc[0]['mean']:.1f} percent a year, with a wide band. "
            "<bookmark mark='b'/> Then the survey for the first month arrives, and it is weak: the nowcast drops "
            f"to {say_num(nc[1]['mean'], 1)}. <bookmark mark='c'/> Will GDP fall this quarter? Decide now, with "
            "what you have."
        ) as vo:
            self.play(FadeIn(axl), FadeIn(q_shade), FadeIn(zl), FadeIn(axr), FadeIn(zr), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines0), FadeIn(ncmark(0)), FadeIn(probs[0]), run_time=2.0)
            vo.wait_until("b")
            l1 = seg_lines(1)
            self.play(Transform(lines0, l1), FadeIn(ncmark(1)), FadeIn(probs[1]))
            vo.wait_until("c")
        ring = countdown().scale(0.55).move_to(axr.get_top() + UP * 0.1 + LEFT * 0.4)
        ask = label(r"fall, \ or not?", font_size=22, color=E.ACCENT).next_to(ring, LEFT, buff=0.25)
        self.play(FadeIn(ring), FadeIn(ask))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=7.0, rate_func=linear)
        self.play(FadeOut(ring), FadeOut(ask))
        truth = Star(n=5, outer_radius=0.16, color=E.ACCENT, fill_opacity=1).move_to(
            axr.ax.c2p(4.6, Isl["pick_truth"]))
        tl = label(rf"truth: \ ${Isl['pick_truth']:.1f}$", font_size=18, color=E.ACCENT).next_to(truth, RIGHT,
                                                                                               buff=0.1)
        with self.voiceover(
            "Here is what came next. <bookmark mark='a'/> The first month's payrolls, production and retail sales "
            f"confirm the survey: the nowcast falls to {say_num(nc[2]['mean'], 1)}, and the chance of a fall "
            f"passes {100 * pn[2]:.0f} percent. <bookmark mark='b'/> The second month leaves little doubt, "
            "<bookmark mark='c'/> and the third settles it. <bookmark mark='d'/> When the quarter's GDP is "
            f"finally published, it fell at {say_num(Isl['pick_truth'], 1)} percent a year. If you said 'fall' "
            "after the survey, you were early and right; most forecasters wait for the hard data, and many wait "
            "for the GDP release itself. A nowcast is this: a forecast of the present, updated every time a "
            "number comes out."
        ) as vo:
            vo.wait_until("a")
            self.play(Transform(lines0, seg_lines(2)), FadeIn(ncmark(2)), FadeIn(probs[2]))
            vo.wait_until("b")
            self.play(Transform(lines0, seg_lines(3)), FadeIn(ncmark(3)), FadeIn(probs[3]))
            vo.wait_until("c")
            self.play(Transform(lines0, seg_lines(4)), FadeIn(ncmark(4)), FadeIn(probs[4]))
            vo.wait_until("d")
            self.play(FadeIn(truth, scale=1.5), FadeIn(tl))
        self.wait(1.0)
        self.clear_scene()
