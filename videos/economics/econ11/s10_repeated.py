from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403


class Repeated(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Repeated games and the folk theorem", r"When does the shadow of the future sustain "
             r"cooperation?", "Chapter eight. Repeated games and the folk theorem.", lit={1986: r"Fudenberg and Maskin"},
             scale=("person", "firm", "nation"), horizon=("a year", "a decade"))
        self.shadow()
        self.folk()
        self.finite()

    def shadow(self):
        r = load("repeated")
        T, R, P = r["T"], r["R"], r["P"]
        ax = plane([0, 0.95], [0, 30], center=LEFT * 2.9 + DOWN * 0.4, x_length=6.0, y_length=4.8,
                   xticks=[0, 0.25, 0.5, 0.75], yticks=[0, 10, 20, 30], xlabel=r"patience $\delta$: \ how much "
                   r"next round counts", ylabel=r"value of the whole game", font_size=16)
        ds = np.linspace(0, 0.95, 120)
        coop = path(ax, ds, R / (1 - ds), color=COOP, width=3.5, yr=(0, 30))
        dev = path(ax, ds, T + ds * P / (1 - ds), color=DEFECT, width=3.5, yr=(0, 30))
        thr = r["threshold"]
        cross = Dot(ax.ax.c2p(thr, R / (1 - thr)), radius=0.1, color=EQ)
        cl = label(r"keep cooperating: \ $\frac{R}{1-\delta}$", font_size=18, color=COOP).next_to(
            ax.ax.c2p(0.8, R / (1 - 0.8)), LEFT, buff=0.15)
        dl = label(r"defect once, \ punished for ever: \ $T + \frac{\delta P}{1-\delta}$", font_size=18,
                   color=DEFECT).next_to(ax.ax.c2p(0.55, T + 0.55 * P / 0.45), DOWN, buff=0.3).shift(RIGHT * 0.3)
        side = VGroup(
            label(r"the prisoner's dilemma, \ played again and again; \\ next round's payoff counts $\delta$ as much "
                  r"as this one's", font_size=21),
            label(r"grim trigger: \ cooperate, \ until the other defects; \\ then defect for ever", font_size=22,
                  color=COOP),
            label(rf"defecting gains {T - R:.0f} now \ (5 instead of 3), \\ and loses {R - P:.0f} in every later round "
                  r"(1 instead of 3)", font_size=21, color=DEFECT),
            MathTex(r"\delta \;\ge\; \frac{T - R}{T - P} = \frac{5 - 3}{5 - 1} = " + f"{thr:.1f}", font_size=34,
                    color=EQ),
            label(r"cooperation is an equilibrium \\ if the future matters enough", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Nash's reply to Flood and Dresher was that a hundred rounds make one long game. Here is why it matters. "
            "<bookmark mark='a'/> Let Ana and Bo play the prisoner's dilemma again and again, with next round's "
            "payoff counting a fraction delta of this round's: delta is their patience, or the chance the game goes "
            "on. <bookmark mark='b'/> Suppose each plays grim trigger: cooperate, until the other defects, and then "
            "defect for ever. <bookmark mark='c'/> Defecting gains two now, five instead of three, but loses two in "
            "every later round, one instead of three. <bookmark mark='d'/> Keeping faith is worth more once delta "
            "is at least two over four, one half. <bookmark mark='e'/> So in a long enough relationship, with "
            "patient enough players, cooperation is an equilibrium: no one wants to break it, because of what "
            "follows."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(coop), FadeIn(cl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(dev), FadeIn(dl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Write(side[3]), FadeIn(cross))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def folk(self):
        r = load("repeated")
        ax = plane([-0.3, 5.5], [-0.3, 5.5], center=LEFT * 3.0 + DOWN * 0.3, x_length=5.4, y_length=5.4,
                   xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 1, 2, 3, 4, 5], xlabel=r"Ana's average payoff",
                   ylabel=r"Bo's", font_size=16)
        a = ax.ax
        feas = Polygon(*[a.c2p(x, y) for x, y in r["feasible"]], stroke_color=GREY_B, stroke_width=2,
                       fill_color=GREY_D, fill_opacity=0.35)
        ir = Polygon(*[a.c2p(x, y) for x, y in r["rational"]], stroke_color=EQ, stroke_width=3, fill_color=EQ,
                     fill_opacity=0.3)
        pts = VGroup(*[VGroup(Dot(a.c2p(x, y), radius=0.08, color=WHITE),
                              label(t, font_size=15, color=GREY_A).next_to(a.c2p(x, y), d, buff=0.1))
                       for (x, y), t, d in (((3, 3), r"both cooperate", UR), ((1, 1), r"both defect", DL),
                                            ((5, 0), r"Ana defects alone", DOWN), ((0, 5), r"Bo defects alone", LEFT))])
        mm = VGroup(DashedLine(a.c2p(1, 1), a.c2p(1, 5.3), color=GREY_B, stroke_width=1.5),
                    DashedLine(a.c2p(1, 1), a.c2p(5.3, 1), color=GREY_B, stroke_width=1.5))
        side = VGroup(
            label(r"every average payoff the players could get, \\ by taking turns or mixing outcomes", font_size=21,
                  color=GREY_A),
            label(r"each can always guarantee 1 by defecting: \\ the minmax", font_size=21),
            label(r"the folk theorem: \ with patient players, \\ \emph{every} point in the gold region \\ is an "
                  r"equilibrium of the repeated game", font_size=22, color=EQ),
            label(r"Friedman (1971); \ Fudenberg and Maskin (1986)", font_size=19, color=GREY_B),
            label(r"repetition makes cooperation possible, \\ not inevitable: \ it allows almost anything", font_size=22,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = published_tag(r"Friedman, REStud 38(1) (1971); \ Fudenberg and Maskin, Econometrica 54(3) (1986)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Repetition does more than rescue cooperation. <bookmark mark='a'/> This grey region is every average "
            "payoff Ana and Bo could get, by mixing the four outcomes or taking turns. <bookmark mark='b'/> Each can "
            "always guarantee one by defecting, whatever the other does: that is the minmax. "
            "<bookmark mark='c'/> The folk theorem says that with patient enough players, every point in the gold "
            "region, every average payoff that gives each player more than their minmax, is an equilibrium of the "
            "repeated game, held in place by the threat of punishment. <bookmark mark='d'/> James Friedman proved a "
            "version in 1971, and Drew Fudenberg and Eric Maskin the general one in 1986; it was called a folk "
            "theorem because game theorists believed it long before anyone wrote it down. <bookmark mark='e'/> The "
            "lesson cuts both ways. Repetition makes cooperation possible, but it makes almost anything possible, "
            "including outcomes that are good for neither."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(feas), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(mm), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(ir), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def finite(self):
        rounds = VGroup(*[VGroup(Square(side_length=0.42, stroke_color=GREY_B, stroke_width=1.5, fill_opacity=0),
                                 label(f"{k}", font_size=14, color=GREY_B)) for k in range(91, 101)])
        for r in rounds:
            r[1].move_to(r[0])
        rounds.arrange(RIGHT, buff=0.12).to_edge(UP, buff=1.2)
        lab = label(r"the last ten of a hundred rounds", font_size=20, color=GREY_A).next_to(rounds, UP, buff=0.2)
        rows = VGroup(
            label(r"but if both know the game ends after round 100, \ round 100 is a one-shot dilemma: \ defect",
                  font_size=23),
            label(r"then nothing done in round 99 can be rewarded: \ defect there too, \ and so back to round 1",
                  font_size=23, color=DEFECT),
            label(r"Nash said as much of Flood and Dresher's game: \ the equilibrium was to defect throughout",
                  font_size=22, color=GREY_A),
            label(r"yet in experiments people cooperate until near the end \ (Selten and Stoecker, 1986)", font_size=23,
                  color=COOP),
            label(r"Kreps, Milgrom, Roberts and Wilson (1982): \ a little doubt about the other's type \\ is enough to "
                  r"make cooperation rational until the last rounds", font_size=22, color=EQ),
        ).arrange(DOWN, buff=0.32).next_to(rounds, DOWN, buff=0.6)
        tag = published_tag(r"Kreps, Milgrom, Roberts and Wilson, JET 27(2) (1982); \ Selten and Stoecker, JEBO 7(1) "
                            r"(1986)", corner=DR, font_size=13)
        with self.voiceover(
            "There is a catch when the end is known. <bookmark mark='a'/> If both players know the game ends after "
            "round one hundred, round one hundred is an ordinary one-shot dilemma, and both defect. "
            "<bookmark mark='b'/> Then nothing done in round ninety-nine can be rewarded or punished later, so both "
            "defect there too; and so on back to the first round. <bookmark mark='c'/> Nash made the same point "
            "about Flood and Dresher's game: in equilibrium, the players defect throughout. "
            "<bookmark mark='d'/> Yet in experiments people cooperate until near the end, and only then defect, as "
            "Reinhard Selten and Rolf Stoecker found in 1986. "
            "<bookmark mark='e'/> In 1982 David Kreps, Paul Milgrom, John Roberts and Robert Wilson showed why that "
            "can be rational: if each thinks there is a small chance the other is the kind of player who always "
            "returns cooperation, it pays to cooperate until the last few rounds."
        ) as vo:
            self.play(FadeIn(rounds), FadeIn(lab), FadeIn(tag))
            vo.wait_until("a")
            self.play(rounds[-1][0].animate.set_fill(DEFECT, 0.8), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[r[0].animate.set_fill(DEFECT, 0.8) for r in reversed(rounds[:-1])],
                                  lag_ratio=0.3), FadeIn(rows[1]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(*[r[0].animate.set_fill(COOP, 0.8) for r in rounds[:-2]], FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
