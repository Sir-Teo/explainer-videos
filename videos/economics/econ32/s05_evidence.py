from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class Evidence(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The multiplier in evidence", r"Four designs for one number: \ what do they find?",
             "Chapter four. The multiplier in evidence.",
             lit={2002: r"Blanchard and Perotti", 2011: r"Ramey", 2014: r"Nakamura and Steinsson"},
             scale=("nation", "city"), horizon=("a quarter", "five years"))
        self.designs()
        self.news()
        self.states()
        self.regions()

    def designs(self):
        cards = point_cards([
            (r"timing", r"spending is set months ahead, \\ so its surprise this quarter \\ is a shock \ (Blanchard "
                        r"\\ and Perotti, \ 2002)", SPEND),
            (r"military news", r"wars and buildups announced \\ in the press, \ valued in \\ dollars \ (Ramey, "
                               r"\ 2011)", INFL),
            (r"regions", r"defence contracts across \\ states with one monetary \\ policy \ (Nakamura and "
                         r"\\ Steinsson, \ 2014)", OUTPUT),
            (r"forecast errors", r"growth that fell short where \\ austerity was planned \\ (Blanchard and Leigh, "
                                 r"\ 2013)", TAX),
        ], width=12.8, cols=2, font_size=21).move_to(DOWN * 0.2)
        head = label(r"spending also responds to the economy: \ four ways around that", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Blanchard and Perotti, \ \emph{QJE} 117(4) (2002); \ Ramey, \ \emph{QJE} 126(1) (2011); "
                            r"\ Nakamura and Steinsson, \ \emph{AER} 104(3) (2014); \ Blanchard and Leigh, \ "
                            r"\emph{AER} 103(3) (2013)", corner=DR, font_size=11)
        with self.voiceover(
            "Measuring the multiplier runs into Part 31's problem: governments spend more in recessions, so "
            "spending and output move together for reasons that are not the multiplier. Four designs get around "
            "it. <bookmark mark='a'/> Timing: budgets are set months in advance, so the part of this quarter's "
            "spending that surprises is a shock; Olivier Blanchard and Roberto Perotti used it in 2002. "
            "<bookmark mark='b'/> Military news: Valerie Ramey read the press for news of wars and buildups and "
            "valued it in dollars, because markets and households react to news, not to the delivery of tanks. "
            "<bookmark mark='c'/> Regions: Emi Nakamura and Jón Steinsson compared states that get more defence "
            "contracts when national defence spending rises. <bookmark mark='d'/> And forecast errors: where "
            "austerity was planned, did growth fall short of the forecasts?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def news(self):
        R = load("rz")
        h = np.array(R["h"])
        ax = plane([0, 20], [0, 1.4], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[0, 4, 8, 12, 16, 20], yticks=[0, 0.25, 0.5, 0.75, 1.0, 1.25],
                   xlabel=r"quarters after the shock",
                   ylabel=r"cumulative multiplier, \ $\sum \Delta Y / \sum \Delta G$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=15)
        one = seg(ax, 0, 1, 20, 1, GREY_C, 1.5, dashed=True)
        ln = path(ax, h[1:], np.clip(R["news"][1:], 0, 1.4), INFL, 3.5)
        lb = path(ax, h, np.clip(R["bp"], 0, 1.4), SPEND, 3.5)
        side = VGroup(
            label(r"US quarterly data, \ 1889--2015 \\ (Ramey and Zubairy)", font_size=18, color=GREY_A),
            label(rf"red: \ military news: \\ {R['news8']:.2f} after two years, \ {R['news16']:.2f} after four",
                  font_size=18, color=INFL),
            label(rf"teal: \ Blanchard--Perotti timing: \\ {R['bp8']:.2f} after two years", font_size=18, color=SPEND),
            label(r"both below one: \\ private spending fell \\ as the government's rose", font_size=19,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Ramey and Zubairy, \ \emph{JPE} 126(2) (2018), \ replication data; \ this film's local "
                       r"projections", corner=DR, font_size=12)
        with self.voiceover(
            "Here are the first two designs on the longest record there is: American data since 1889, assembled "
            "by Valerie Ramey and Sarah Zubairy, with the World Wars and Korea in it. <bookmark mark='a'/> For each "
            "horizon, output and spending are projected on the shock, and the multiplier is the extra output so "
            "far over the extra spending so far. <bookmark mark='b'/> With military news, in red: "
            f"{R['news8']:.2f} after two years, {R['news16']:.2f} after four. <bookmark mark='c'/> With "
            f"Blanchard and Perotti's timing, in teal: {R['bp8']:.2f}. <bookmark mark='d'/> Both are below one. "
            "When the federal government spent more, private spending fell, on average over a century. These are "
            "this film's estimates from their data; they match the published ones to two decimal places."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(one), FadeIn(tag), FadeIn(side[0]), run_time=0.6)
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(side[1]), run_time=1.8)
            vo.wait_until("c")
            self.play(Create(lb), FadeIn(side[2]), run_time=1.8)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def states(self):
        R = load("rz")
        vals = [(r"normal times", R["normal8"], SPEND), (r"high unemployment", R["slack8"], INFL),
                (r"rates near zero", R["zlb8"], RATE)]
        ax = plane([0, 3.4], [0, 1.2], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.4, xticks=[],
                   yticks=[0, 0.25, 0.5, 0.75, 1.0], ylabel=r"military-news multiplier, \ two years",
                   yfmt=lambda v: f"{v:.2f}", font_size=15)
        one = seg(ax, 0, 1, 3.4, 1, GREY_C, 1.5, dashed=True)
        bars, labs = VGroup(), VGroup()
        for k, (n, v, c) in enumerate(vals):
            p0, p1 = ax.ax.c2p(0.3 + k * 1.05, 0), ax.ax.c2p(1.05 + k * 1.05, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=c, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
            labs.add(VGroup(label(f"{v:.2f}", font_size=18, color=c).next_to(bars[-1], UP, buff=0.08),
                            label(n, font_size=16, color=GREY_A).next_to(ax.ax.c2p(0.675 + k * 1.05, 0), DOWN,
                                                                           buff=0.12)))
        side = VGroup(
            label(rf"unemployment of 6.5\% or more: \\ {100 * R['share_slack']:.0f}\% of quarters", font_size=18,
                  color=INFL),
            label(rf"near-zero rates: \ {100 * R['share_zlb']:.0f}\% of quarters", font_size=18, color=RATE),
            label(r"no sign that slack \\ makes the multiplier large", font_size=19, color=WHITE),
            label(r"other studies find it does; \\ the question is open", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"Ramey and Zubairy, \ \emph{JPE} 126(2) (2018), \ replication data; \ this film", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Theory said the multiplier should be larger in slumps and at the zero bound. <bookmark mark='a'/> "
            f"Split the century by unemployment: in normal times, {R['normal8']:.2f} after two years; "
            f"<bookmark mark='b'/> with unemployment above six and a half percent, {R['slack8']:.2f}. "
            f"<bookmark mark='c'/> In quarters with interest rates near zero, {R['zlb8']:.2f}. "
            "<bookmark mark='d'/> Ramey and Zubairy found no sign that slack makes the multiplier large. Studies "
            "using other methods, notably Alan Auerbach and Yuriy Gorodnichenko's, found much larger multipliers in "
            "recessions, and the difference between them is still argued."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(one), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(labs[1]), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(labs[2]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def regions(self):
        G = load("regions")
        g, y = np.array(G["g"]), np.array(G["y"])
        gd, yd = g - g.mean(axis=0), y - y.mean(axis=0)
        ax = plane([-3, 3], [-6, 6], center=LEFT * 2.6 + DOWN * 0.3, x_length=5.6, y_length=4.8,
                   xticks=[-2, 0, 2], yticks=[-4, 0, 4],
                   xlabel=r"a region's spending, \ relative to the year's average",
                   ylabel=r"its output, \ relative", xfmt=lambda v: f"{v:+.0f}" if v else "0",
                   yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=14)
        rng = np.random.default_rng(0)
        idx = rng.choice(gd.size, 500, replace=False)
        pts = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.025, color=GREY_B) for a, b in
                       zip(gd.ravel()[idx], yd.ravel()[idx]) if -3 <= a <= 3 and -6 <= b <= 6])
        fit = seg(ax, -3, -3 * G["b_fe"], 3, 3 * G["b_fe"], OUTPUT, 3.5)
        side = VGroup(
            label(rf"the Island: \ {G['R']} regions, \ {G['T']} years, \\ one central bank", font_size=18,
                  color=GREY_A),
            label(rf"within each year: \ {G['b_fe']:.2f} \\ (planted: \ {G['m_local']:.1f})", font_size=18,
                  color=OUTPUT),
            label(rf"the nation as a whole: \ {G['b_nat']:.2f} \\ (planted: \ {G['m_agg']:.1f})", font_size=18,
                  color=SPEND),
            label(r"the year effects hold the difference: \\ the central bank's response, \ national taxes \\ --- "
                  r"the missing intercept", font_size=18, color=HOLD),
            label(r"published: \ Nakamura and Steinsson about 1.5; \\ Chodorow-Reich's survey, \ 1.8", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Nakamura and Steinsson, \ \emph{AER} 104(3) (2014); \ Chodorow-Reich, \ \emph{AEJ: "
                            r"Policy} 11(2) (2019); \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "The third design compares regions. On the Island we can see what it measures. "
            f"<bookmark mark='a'/> {G['R']} regions share one central bank for {G['T']} years. National "
            "spending lands more in some than in others. <bookmark mark='b'/> Compare regions within the same "
            f"year, and output rises {G['b_fe']:.2f} for each point of extra spending, close to the planted local "
            "multiplier of one and a half. <bookmark mark='c'/> But the nation as a whole gains only "
            f"{G['b_nat']:.2f}, because the central bank leans against national spending, and the region-by-region "
            "comparison cannot see that: <bookmark mark='d'/> it is absorbed in what all regions share in a year, "
            "the missing intercept. <bookmark mark='e'/> Nakamura and Steinsson found a regional multiplier of about "
            "one and a half in American states; Gabriel Chodorow-Reich's survey of such studies, about one point "
            "eight. Both are honest answers to a different question from the national one."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.004), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
