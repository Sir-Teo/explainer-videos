from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

FT = "#F2A65A"


class LevelK(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Levels of thinking, \ fitted", r"If people think only a few steps ahead, how many?",
             "Chapter twelve. Levels of thinking, fitted.", lit={2004: r"Camerer, Ho and Chong"}, scale=("person",))
        self.model()
        self.fit()
        self.called()

    def model(self):
        lk = load("levelk")
        ch = lk["ch_15"]
        xs, sh = np.array(ch["choices"]), np.array(ch["shares"])
        ax = plane([-0.6, 6.6], [0, 0.4], center=LEFT * 2.8 + DOWN * 0.4, x_length=6.2, y_length=4.4,
                   xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[0, 0.1, 0.2, 0.3, 0.4], xlabel=r"level of thinking",
                   ylabel=r"share of players", font_size=16)
        a = ax.ax
        bars = VGroup(*[Rectangle(width=0.6, height=max(a.c2p(0, s)[1] - a.c2p(0, 0)[1], 1e-3), stroke_width=0,
                                  fill_color=LEVEL, fill_opacity=0.85).move_to(a.c2p(k, 0), aligned_edge=DOWN)
                        for k, s in enumerate(sh)])
        picks = VGroup(*[label(rf"{x:.0f}", font_size=17, color=E.ACCENT).next_to(b, UP, buff=0.06)
                         for b, x in zip(bars, xs)])
        side = VGroup(
            label(r"level 0: \ chooses at random \ (average 50)", font_size=21),
            label(r"level 1: \ best reply to level 0: \ 33", font_size=21, color=LEVEL),
            label(r"level 2, \ in the cognitive hierarchy: \\ best reply to a mix of levels 0 and 1", font_size=21,
                  color=LEVEL),
            label(r"how many at each level: \ Poisson, \ average $\tau$", font_size=21, color=GREY_A),
            label(rf"with $\tau = 1.5$: \ the population averages {ch['mean']:.1f}", font_size=22, color=EQ),
            label(r"Stahl and Wilson (1994); \ Nagel (1995); \\ Camerer, \ Ho and Chong (2004)", font_size=19,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "If equilibrium is the wrong guess for first-time play, what is the right one? A family of models "
            "assumes that people think a limited number of steps ahead. <bookmark mark='a'/> A level-nought player "
            "chooses at random, so level noughts average fifty. <bookmark mark='b'/> A level-one player best "
            "responds to level noughts, and chooses thirty-three. <bookmark mark='c'/> In Colin Camerer, Teck-Hua "
            "Ho and Juin-Kuan Chong's cognitive hierarchy, a level-two player responds to a mixture of level noughts "
            "and level ones, and so on up. <bookmark mark='d'/> How many players there are at each level follows a "
            "Poisson distribution, with an average number of steps called tau. <bookmark mark='e'/> With tau of one "
            "and a half, most players are at levels one and two, and the population averages about thirty-three and "
            "a half. <bookmark mark='f'/> Dale Stahl and Paul Wilson, and Nagel, proposed level models in the "
            "mid-nineties; the cognitive hierarchy is from 2004."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), GrowFromEdge(bars[0], DOWN), FadeIn(picks[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(picks[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[2:]], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(p_) for p_ in picks[2:]], lag_ratio=0.3), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def fit(self):
        lk = load("levelk")
        taus, means = np.array(lk["taus"]), np.array(lk["means"])
        ax = plane([0, 6], [0, 55], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.2, y_length=4.8,
                   xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[0, 10, 20, 30, 40, 50], xlabel=r"$\tau$: \ average steps of "
                   r"thinking", ylabel=r"predicted average choice", font_size=16)
        a = ax.ax
        curve = path(ax, taus, means, color=LEVEL, width=3.5)
        tn, tf = lk["tau_nagel"], lk["tau_ft"]
        mn, mf = lk["nagel"]["mean"], lk["ft"]["mean"]
        hn = DashedLine(a.c2p(0, mn), a.c2p(tn, mn), color=ANA, stroke_width=2)
        vn = DashedLine(a.c2p(tn, mn), a.c2p(tn, 0), color=ANA, stroke_width=2)
        hf = DashedLine(a.c2p(0, mf), a.c2p(tf, mf), color=FT, stroke_width=2)
        vf = DashedLine(a.c2p(tf, mf), a.c2p(tf, 0), color=FT, stroke_width=2)
        band = Rectangle(width=a.c2p(2, 0)[0] - a.c2p(1, 0)[0], height=a.c2p(0, 55)[1] - a.c2p(0, 0)[1],
                         stroke_width=0, fill_color=EQ, fill_opacity=0.12).move_to(a.c2p(1.5, 27.5))
        bl = label(r"$\tau$ from 1 to 2: \\ nearly 100 games", font_size=16, color=EQ).move_to(a.c2p(1.5, 50))
        side = VGroup(
            label(r"the more steps people take, \ the lower the average", font_size=21),
            label(rf"Nagel's students averaged {mn:.2f}: \ $\tau = {tn:.2f}$", font_size=22, color=ANA),
            label(rf"the Financial Times' readers {mf:.1f}: \ $\tau = {tf:.2f}$", font_size=22, color=FT),
            label(r"Camerer, \ Ho and Chong: \ values from 1 to 2 \\ fit nearly 100 games; \ 1.5 is typical",
                  font_size=21, color=EQ),
            label(r"readers who had days to think, \ and chose to enter, \\ went further than students in a "
                  r"classroom", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Camerer, Ho and Chong, QJE 119(3) (2004); \ fits to the means: \ Agora", corner=DR,
                            font_size=13)
        with self.voiceover(
            "The model makes a prediction for every value of tau, so it can be fitted to data. "
            "<bookmark mark='a'/> The more steps people take, the lower the average choice. "
            "<bookmark mark='b'/> Nagel's students averaged thirty-six point seven three, which the model matches with "
            "tau of one point one two. <bookmark mark='c'/> The Financial Times' readers averaged eighteen point nine: "
            "tau of about four. <bookmark mark='d'/> Across nearly a hundred games, Camerer, Ho and Chong found that "
            "values between one and two fit well, and one and a half is typical. <bookmark mark='e'/> Readers who "
            "had days to think, and chose to enter a newspaper contest, went several steps further than students in a "
            "classroom."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(band), FadeIn(bl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(curve))
            vo.wait_until("b")
            self.play(Create(hn), Create(vn), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(hf), Create(vf), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(band))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["nash_guessing"]
        g = load("guess")
        nz, ft = g["nagel"], g["ft"]
        cc = call_card(r"game theory's equilibrium", c.when,
                       r"in two-thirds of the average, \ everyone chooses 0: \ the only Nash equilibrium, \ reached by "
                       r"eliminating dominated choices round after round",
                       rf"Nagel's first rounds: \ an average of {nz['mean']:.2f}, \ a winning target near "
                       rf"{g['nagel_target']:.0f}; \ the Financial Times (1997): \ average {ft['mean']:.1f}, \ winning "
                       rf"number {ft['winner']:.0f}",
                       c.verdict, width=12.4, font_size=23).move_to(UP * 0.6)
        q = label(r"but played again, \ choices fall round by round toward 0: \\ equilibrium describes where "
                  r"learning goes, \ not where it starts", font_size=23, color=E.ACCENT).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Nagel, AER 85(5) (1995); \ Thaler's FT contest (1997)", corner=DR, font_size=13)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> Game theory's prediction for the guessing game is that everyone chooses "
            "nought, the only Nash equilibrium, reached by eliminating dominated choices round after round. "
            "<bookmark mark='b'/> In Nagel's first rounds the average was thirty-six point seven three, and the "
            "winning target about twenty-four; among the Financial Times' readers the average was eighteen point "
            "nine, and the winning number thirteen. <bookmark mark='c'/> Wrong, as a forecast of what people do the "
            "first time. But when Nagel's students played again, their choices fell round by round toward nought. "
            "Equilibrium describes where learning goes, not where it starts."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3), FadeIn(q))
        self.clear_scene()
