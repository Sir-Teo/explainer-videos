from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403

GROUPS = (r"the poor", r"the middle", r"the rich")


class Voters(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Voters", r"Who do parties compete for, and do voters change policy or only choose it?",
             "Chapter four. Voters.", lit={2004: r"Lee, Moretti and Butler", 2015: r"Cattaneo, Frandsen and Titiunik"},
             scale=("nation",), horizon=("an election",))
        self.swing()
        self.affect()
        self.senate()
        self.robust()

    def swing(self):
        V = load("voting")
        P_ = V["plain"]
        ax = plane([0, 3], [-1.0, 0.7], center=LEFT * 2.0 + DOWN * 0.35, x_length=6.6, y_length=4.6, xticks=[],
                   yticks=[-0.8, -0.4, 0, 0.4], ylabel=r"net transfer, \ share of average income",
                   yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0", font_size=14)
        zero = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(3, 0), color=GREY_B, stroke_width=1.4)
        bars = VGroup()
        for i, (nm, t) in enumerate(zip(GROUPS, P_["transfer"])):
            p0, p1 = ax.ax.c2p(0.5 + i - 0.3, 0), ax.ax.c2p(0.5 + i + 0.3, t)
            r = Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.02), stroke_width=0,
                          fill_color=VOTER if i == 1 else GREY_B, fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(rf"{nm} \\ {100 * V['alpha'][i]:.0f}\% of voters", font_size=14,
                                     color=WHITE).next_to(ax.ax.c2p(0.5 + i, -1.0), DOWN, buff=0.1),
                            label(rf"{t:+.2f}".replace("-", "{-}"), font_size=16, color=WHITE).next_to(
                                r, UP if t >= 0 else DOWN, buff=0.05)))
        side = VGroup(
            label(r"Part 18: \ with one issue, \\ both parties go to \\ the median voter", font_size=18, color=GREY_A),
            label(r"here: \ voters also care \\ about other things, \\ so some are swing voters", font_size=18,
                  color=WHITE),
            label(r"the middle group \\ has twice the \\ swing voters", font_size=18, color=VOTER),
            label(r"both parties offer \\ it the most", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        xs = np.linspace(-5.2, 1.0, 21)
        line = Line([-5.5, 0.0, 0], [1.3, 0.0, 0], color=GREY_B, stroke_width=2)
        voters = VGroup(*[Dot([x, 0.0, 0], radius=0.07, color=GREY_A) for x in xs])
        med = voters[10].get_center()
        pa = label(r"party A", font_size=18, color=POL).move_to([-5.2, 0.45, 0])
        pb = label(r"party B", font_size=18, color=LOBBY).move_to([1.0, 0.95, 0])
        strip = VGroup(line, voters, pa, pb)
        swing_ix = (3, 7, 9, 10, 11, 13, 16)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Part eighteen's median voter theorem says that with one issue, two parties both move to the voter in "
            "the middle. <bookmark mark='a'/> Real voters care about many things, a party's leader, its record, its "
            "values, so a promise of money moves only some of them: the swing voters. <bookmark mark='b'/> Here are "
            "three groups on the Island, the poor, the middle and the rich, and two parties offering transfers "
            "paid for by everyone. <bookmark mark='c'/> The middle group has twice as many swing voters as the "
            "others. <bookmark mark='d'/> Both parties end up offering it the most: in this model of probabilistic "
            f"voting, a group gets more the more of its votes are up for grabs, here a transfer worth "
            f"{100 * P_['transfer'][1]:.0f} percent of average income, paid for mostly by the rich. Policy follows not "
            "need, and not numbers, but how "
            "easily a group's votes can be bought."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(side[0]), Create(strip[0]), LaggedStart(*[FadeIn(d) for d in strip[1]],
                                                                                    lag_ratio=0.05),
                      FadeIn(strip[2]), FadeIn(strip[3]), run_time=1.5)
            self.play(strip[2].animate.move_to(med + UP * 0.45), strip[3].animate.move_to(med + UP * 0.95),
                      run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), *[strip[1][k].animate.set_color(VOTER).scale(1.4) for k in swing_ix])
            vo.wait_until("b")
            self.play(FadeOut(strip), run_time=0.6)
            self.play(FadeIn(ax), Create(zero), *[FadeIn(b[1]) for b in bars], run_time=0.8)
            self.play(*[GrowFromEdge(b[0], DOWN if V["plain"]["transfer"][i] >= 0 else UP) for i, b in enumerate(bars)],
                      *[FadeIn(b[2]) for b in bars], run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(bars[1], color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def affect(self):
        chain = flow_chain([(r"a close election: \\ the winner \\ as if by a coin", VOTER),
                            (r"compare districts \\ barely won and \\ barely lost", VOTER),
                            (r"how the winner \\ then votes \\ in Congress", POL),
                            (r"voters elect \\ policies, \\ not affect them", E.ACCENT)],
                           notes=[r"U.S. House, \\ 1946--1995", r"a regression \\ discontinuity",
                                  r"a big win or \\ a narrow one: \\ the same votes", r"candidates cannot \\ commit to "
                                  r"\\ compromise"],
                           box_w=2.8, box_h=1.05, font_size=18, note_size=16).move_to(UP * 0.6)
        tag = published_tag(tables.VOTERS_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Do voters change what politicians do, or only choose between politicians who will do what they "
            "always meant to? <bookmark mark='a'/> David Lee, Enrico Moretti and Matthew Butler used close "
            "elections, where who wins is almost a coin toss, <bookmark mark='b'/> and compared House districts "
            "that a party barely won with districts it barely lost: a regression discontinuity, as in Part four. "
            "<bookmark mark='c'/> If politicians moved toward voters when their seat was marginal, how they voted "
            "in Congress would depend on how strong the other party was. It did not. <bookmark mark='d'/> Voters "
            "elect policies; they do not affect them, because a candidate cannot credibly promise to vote against "
            "their own beliefs once elected."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
        self.clear_scene()

    def senate(self):
        S = load("senate")
        B = S["bins"]
        h = S["h"]
        ax = plane([-50, 50], [20, 80], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.2, y_length=4.8,
                   xticks=[-50, -25, 0, 25, 50], yticks=[20, 35, 50, 65, 80],
                   xlabel=r"the Democrats' margin today, \ points", ylabel=r"their share at the seat's next election",
                   xfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", yfmt=lambda v: f"{v:.0f}",
                   font_size=13)
        cut = vline(ax, 0, 20, 80, WHITE)
        pts = VGroup(*[dot(ax, x, y, VOTER if x >= 0 else POL, 0.06) for x, y in zip(B["mids"], B["means"])])
        fl, fr = S["fit_left"], S["fit_right"]
        fits = VGroup(seg(ax, -h, fl[0] - fl[1] * h, 0, fl[0], POL, 3.2), seg(ax, 0, fr[0], h, fr[0] + fr[1] * h,
                                                                             VOTER, 3.2))
        win = Rectangle(width=(ax.ax.c2p(h, 0) - ax.ax.c2p(-h, 0))[0], height=(ax.ax.c2p(0, 80) - ax.ax.c2p(0, 20))[1],
                        stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.08).move_to(ax.ax.c2p(0, 50))
        side = VGroup(
            label(rf"U.S. Senate, \\ {S['first']}--{S['last']}: \ {S['n']:,} \\ elections".replace(",", "{,}"),
                  font_size=18, color=WHITE),
            label(r"dots: \ averages in \\ 2.5-point bins", font_size=18, color=GREY_A),
            label(rf"lines: \ local linear, \\ within {h:.1f} points", font_size=18, color=E.ACCENT),
            label(rf"the jump: \ {S['jump']:.2f} points \\ (s.e. {S['se']:.2f})", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Cattaneo, \ Frandsen and Titiunik (2015), \ via the R package rdrobust 4.1.2", corner=DL,
                       font_size=12)
        with self.voiceover(
            "Close elections also measure what winning is worth. Here are real data: <bookmark mark='a'/> "
            f"{S['n']:,} elections to the United States Senate between {S['first']} and {S['last']}, compiled by "
            "Matias Cattaneo, Brigham Frandsen and Rocío Titiunik. Across, the Democrats' margin of victory or "
            "defeat; up the side, their share of the vote when the same seat next comes up, six years later. "
            "<bookmark mark='b'/> Each dot averages the elections in a band two and a half points wide. "
            f"<bookmark mark='c'/> Fit a line on each side, within {h:.1f} points of zero, weighting the closest "
            f"races most. <bookmark mark='d'/> At zero the lines jump by {S['jump']:.2f} points, with a standard "
            f"error of {S['se']:.2f}. That is the incumbent party's advantage: barely winning a seat, rather than "
            "barely losing it, is worth about seven points of the vote six years later. The same calculation in "
            "the rdrobust software these data come with gives the same number."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(cut), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(win), Create(fits), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(fits, color=WHITE))
        self.clear_scene()

    def robust(self):
        S = load("senate")
        R = S["robust"]
        ax = plane([0, len(R)], [0, 20], center=LEFT * 1.8 + DOWN * 0.35, x_length=7.6, y_length=4.4, xticks=[],
                   yticks=[0, 4, 8, 12, 16, 20], ylabel=r"the jump, \ points, \ with 95\% intervals",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        items = VGroup()
        for i, r in enumerate(R):
            x = i + 0.5
            items.add(VGroup(Line(ax.ax.c2p(x, r["jump"] - 1.96 * r["se"]), ax.ax.c2p(x, r["jump"] + 1.96 * r["se"]),
                                  color=VOTER, stroke_width=3),
                             dot(ax, x, r["jump"], VOTER if abs(r["h"] - S["h"]) > 0.01 else E.ACCENT, 0.08),
                             label(rf"{r['h']:g}", font_size=14, color=WHITE).next_to(ax.ax.c2p(x, 0), DOWN,
                                                                                     buff=0.12)))
        xl = label(r"bandwidth, \ points either side of zero", font_size=15, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        side = VGroup(
            label(r"narrow: \ few elections, \\ wide intervals", font_size=18, color=WHITE),
            label(r"wide: \ more elections, \\ but less alike", font_size=18, color=WHITE),
            label(r"seven or eight points \\ across sensible choices", font_size=18, color=E.ACCENT),
            label(r"the House: \ Lee, \ 2008, \\ about 7.7; \ critics find \\ bare winners differ", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Cattaneo, \ Frandsen and Titiunik (2015), \ via rdrobust", corner=DL, font_size=12)
        with self.voiceover(
            "A regression discontinuity has one choice that matters: how far from zero to look. <bookmark "
            "mark='a'/> Look only at the very closest races, and there are few of them, so the estimate is noisy. "
            "<bookmark mark='b'/> Look further, and there are more races, but they are less alike, and the "
            "straight lines must do more work. <bookmark mark='c'/> Across sensible choices the jump stays near "
            "seven or eight points, falling a little as the window widens. <bookmark mark='d'/> For the House, "
            "David Lee found about the same. Devin Caughey and Jasjeet Sekhon later showed that in the House, bare "
            "winners and bare losers differ in ways visible before the election, which suggests the true advantage "
            "there is smaller. The second dial of chapter fourteen collects these."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(xl), LaggedStart(*[FadeIn(it) for it in items], lag_ratio=0.2),
                      run_time=2.0)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
