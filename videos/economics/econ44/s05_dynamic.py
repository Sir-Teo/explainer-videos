from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class Dynamic(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Dynamic oligopoly", r"How do firms compete when today's investment shapes tomorrow?",
             "Chapter four. Dynamic oligopoly.", lit={1995: r"Ericson and Pakes", 2007: r"Bajari, \ Benkard and Levin",
                                                      2012: r"Ryan"}, scale=("firm", "market"), horizon=("a decade",))
        self.rules()
        self.policy()
        self.history()
        self.estimation()

    def rules(self):
        D = TRUTH["duopoly"]
        rows = VGroup(
            label(rf"two firms, \ each with a quality from 0 to {D['K'] - 1}", font_size=22, color=WHITE),
            label(rf"each period: \ profit from its share of {D['M']:g} buyers, \ given both qualities",
                  font_size=22, color=FIRM1),
            label(rf"invest $x$: \ the chance of climbing a step is $ax/(1+ax)$, \ $a$ = {D['a']}", font_size=22,
                  color=PATIENT),
            label(rf"with chance {D['delta']}, \ a step is lost: \ rivals and outside goods improve", font_size=22,
                  color=LOSS),
            label(r"Markov-perfect equilibrium: \ each firm's investment depends only on today's two qualities, \ "
                  r"and is the best reply to the other's", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to(DOWN * 0.1)
        head = label(r"Ericson and Pakes, \ in miniature", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.DYNAMIC_IO.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Zurcher made decisions alone. Firms make them against rivals who also look ahead. In 1995 Richard "
            "Ericson and Ariel Pakes built the framework economists use for this. Here it is in miniature. "
            f"<bookmark mark='a'/> Two firms, each with a quality level from zero to {D['K'] - 1}. "
            "<bookmark mark='b'/> Each period, each earns a profit from its share of buyers, which depends on both "
            "qualities. <bookmark mark='c'/> Each can invest to climb a step; more investment, a better chance. "
            "<bookmark mark='d'/> And each can lose a step, as rivals elsewhere and outside goods improve. "
            "<bookmark mark='e'/> In a Markov-perfect equilibrium each firm's investment depends only on today's two "
            "quality levels, and is its best reply to the other's, now and in every future state."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def policy(self):
        Dq = load("duopoly")
        X = np.array(Dq["X"])
        K = X.shape[0]
        cell = 0.62
        grid = VGroup()
        mx = X.max()
        for i in range(K):
            for j in range(K):
                v = X[i, j] / mx
                sq = Square(side_length=cell, stroke_width=0.6, stroke_color=BLACK,
                            fill_color=interpolate_color(ManimColor("#1B2230"), ManimColor(PATIENT), v),
                            fill_opacity=1).move_to(np.array([(j - K / 2) * cell, (i - K / 2) * cell, 0]))
                grid.add(sq)
        grid.move_to(LEFT * 2.2 + DOWN * 0.3)
        xl = label(r"the rival's quality \ $\rightarrow$", font_size=18, color=GREY_A).next_to(grid, DOWN, buff=0.2)
        yl = label(r"own quality \ $\rightarrow$", font_size=18, color=GREY_A).rotate(PI / 2).next_to(grid, LEFT,
                                                                                                    buff=0.2)
        diag = DashedLine(grid[0].get_corner(DL), grid[-1].get_corner(UR), color=WHITE, stroke_width=1.5)
        side = VGroup(
            label(r"brighter: \ more investment", font_size=18, color=PATIENT),
            label(rf"neck and neck \ (the diagonal): \\ {Dq['x_even']:.2f} on average", font_size=18, color=WHITE),
            label(rf"two steps ahead: \ {Dq['x_lead2']:.2f}; \\ two steps behind: \ {Dq['x_lag2']:.2f}",
                  font_size=18, color=FIRM1),
            label(r"at the top, \ nothing \\ left to climb", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"The equilibrium, found by iterating both firms' Bellman equations together in {Dq['iterations']} "
            "rounds, is a policy: how much a firm invests in every state. <bookmark mark='a'/> Here it is: own "
            "quality up the side, the rival's along the bottom; brighter cells mean more investment. "
            "<bookmark mark='b'/> Firms invest most when they are neck and neck, especially in the middle of the "
            "ladder, where a step decides who leads. <bookmark mark='c'/> A firm two steps ahead invests a little "
            "less, and so does one two steps behind. <bookmark mark='d'/> At the top there is nothing left to "
            "climb. Competition here is a race, and how hard firms run depends on how close the race is."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.01), FadeIn(xl), FadeIn(yl),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(diag), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def history(self):
        Dq = load("duopoly")
        P = np.array(Dq["path"])
        T = len(P)
        K = TRUTH["duopoly"]["K"]
        ax = plane([0, T], [0, K - 1], center=LEFT * 1.8 + UP * 0.6, x_length=8.2, y_length=3.0,
                   xticks=[0, 100, 200, 300], yticks=list(range(0, K, 2)), xlabel=r"period",
                   ylabel=r"quality", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        l1 = path(ax, np.arange(T), P[:, 0] + 0.05, FIRM1, 2.2, smooth=False)
        l2 = path(ax, np.arange(T), P[:, 1] - 0.05, FIRM2, 2.2, smooth=False)
        h = np.array(Dq["gap_hist"])
        bars = VGroup()
        for k, v in enumerate(h[:5]):
            r = Rectangle(width=0.55, height=max(v * 4.0, 0.02), stroke_width=0, fill_color=PATIENT,
                          fill_opacity=0.85).move_to(np.array([-4.6 + 0.8 * k, -3.2 + v * 2.0, 0]))
            bars.add(VGroup(r, label(f"{k}", font_size=16, color=GREY_A).next_to(r, DOWN, buff=0.08),
                            label(rf"{100 * v:.0f}\%", font_size=15, color=WHITE).next_to(r, UP, buff=0.06)))
        bl = label(r"the gap in quality, \ share of periods", font_size=17, color=PATIENT).next_to(bars, RIGHT,
                                                                                                 buff=0.4)
        side = VGroup(
            label(r"gold and blue: \\ the two firms", font_size=18, color=WHITE),
            label(rf"{Dq['lead_changes']} changes of \\ leader in {Dq['T']:,} \\ periods", font_size=18,
                  color=FIRM1),
            label(rf"mean gap: \ {Dq['mean_gap']:.2f} steps", font_size=18, color=PATIENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35).shift(UP * 0.6)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Simulate the industry under those policies. <bookmark mark='a'/> The two firms' qualities rise and "
            "fall, gold and blue, as investment succeeds and steps are lost. <bookmark mark='b'/> In "
            f"{Dq['T']:,} periods the leader changes {Dq['lead_changes']} times: with these parameters neither firm "
            "can pull away for long, because the follower races hardest when close. <bookmark mark='c'/> Most of "
            "the time the firms are level or one step apart. Change the costs of investing, or add entry and "
            "exit, and the same machinery can produce industries where one firm dominates for decades."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(l1), Create(l2), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.2), FadeIn(bl), FadeIn(side[2]))
        self.clear_scene()

    def estimation(self):
        cards = point_cards([
            (r"the burden", r"every state of every \\ firm: \ millions of \\ states, \ one solve \\ per guess", LOSS),
            (r"two steps", r"estimate firms' policies \\ from the data, \\ then the costs that \\ rationalize them "
                           r"\\ (Bajari, \ Benkard, \ Levin)", PATIENT),
            (r"cement", r"Ryan: \ the 1990 Clean \\ Air Act raised the cost \\ of building a plant, \\ a loss a static "
                        r"\\ model would miss", BUS),
        ], width=11.4, cols=3, font_size=18).move_to(DOWN * 0.1)
        head = label(r"estimating dynamic games", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.DYNAMIC_IO.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Estimating such models is harder still. <bookmark mark='a'/> With many firms the states multiply into "
            "millions, and solving the equilibrium for every guess of the costs is out of reach. "
            "<bookmark mark='b'/> Patrick Bajari, Lanier Benkard and Jonathan Levin extended the short cut of the "
            "last chapter to games: estimate how firms actually behave in each state, straight from the data, and "
            "then find the costs under which that behaviour is optimal. <bookmark mark='c'/> Stephen Ryan used such "
            "methods on American cement. The 1990 amendments to the Clean Air Act raised the cost of building a "
            "plant. Fewer firms then enter, and markets stay more concentrated for longer: a cost of the "
            "regulation that a static analysis would miss."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
