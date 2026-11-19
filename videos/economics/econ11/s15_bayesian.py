from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

TOUGH = "#F25F5C"
WEAK = "#7EC8F5"


class Bayesian(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Games of incomplete information", r"What if I don't know what kind of player you are?",
             "Chapter thirteen. Games of incomplete information.", lit={1967: r"Harsanyi's types"},
             scale=("person", "firm"))
        self.types()
        self.threshold()

    def types(self):
        b = load("bayes")
        mt = matrix(np.array(b["tough"]), np.array(b["bo_vs_tough"]), [r"fight", r"share"],
                    [r"enter", r"stay out"], row_name=r"tough Ana", col_name=r"Bo", cell_w=1.7, cell_h=0.8,
                    font_size=22, labels_size=17, row_color=TOUGH)
        mw = matrix(np.array(b["weak"]), np.array(b["bo_vs_weak"]), [r"fight", r"share"], [r"enter", r"stay out"],
                    row_name=r"weak Ana", col_name=r"Bo", cell_w=1.7, cell_h=0.8, font_size=22, labels_size=17,
                    row_color=WEAK)
        pair = VGroup(mt, mw).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.7)
        pt = label(rf"chance {b['prior_tough']:.1f}", font_size=19, color=TOUGH).next_to(mt, DOWN, buff=0.15)
        pw = label(rf"chance {1 - b['prior_tough']:.1f}", font_size=19, color=WEAK).next_to(mw, DOWN, buff=0.15)
        rows = VGroup(
            label(r"Bo could fish Ana's grounds; \ only Ana knows whether she is the tough kind, \ who would fight",
                  font_size=22),
            label(r"Harsanyi (1967--68): \ treat the unknown as a move by nature, \ who picks Ana's \emph{type} with "
                  r"known chances", font_size=22, color=GREY_A),
            label(r"a strategy is now a plan: \ what each type of Ana does; \ Bo best-responds to the mix",
                  font_size=22, color=LEVEL),
            label(r"the Bayesian Nash equilibrium: \ tough Ana fights, \ weak Ana shares, \ and Bo enters",
                  font_size=23, color=EQ),
        ).arrange(DOWN, buff=0.3).next_to(VGroup(pair, pt, pw), DOWN, buff=0.8)
        f1 = frame_cell(mt, 0, 0)
        f2 = frame_cell(mw, 1, 0)
        tag = published_tag(r"Harsanyi, Management Science 14 (1967--68)", corner=DR, font_size=13)
        with self.voiceover(
            "So far every player has known the others' payoffs. Often they don't. <bookmark mark='a'/> Bo is "
            "thinking of fishing Ana's grounds. If he enters, Ana can fight him or share. Only Ana knows whether "
            "she is the tough kind, for whom fighting pays, or the weak kind, who would rather share. Bo thinks she "
            "is tough with chance three in ten. <bookmark mark='b'/> John Harsanyi showed in 1967 how to analyze such "
            "games: treat what you don't know as a move by nature, which picks the other player's type with known "
            "chances. <bookmark mark='c'/> A strategy is then a plan for every type, and each player best-responds "
            "given their beliefs. <bookmark mark='d'/> Here the equilibrium is that a tough Ana fights, a weak Ana "
            "shares, and Bo, expecting a fight only three times in ten, enters."
        ) as vo:
            self.play(FadeIn(pair), FadeIn(pt), FadeIn(pw), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(f1), Create(f2), FadeIn(rows[3]))
        self.clear_scene()

    def threshold(self):
        b = load("bayes")
        ps, enter = np.array(b["ps"]), np.array(b["enter"])
        ax = plane([0, 1], [-2.2, 2.2], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.0, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[-2, -1, 0, 1, 2], xlabel=r"Bo's belief that Ana is tough",
                   ylabel=r"Bo's expected gain from entering", font_size=16)
        a = ax.ax
        line = path(ax, ps, enter, color=BO, width=3.5, smooth=False)
        zero = DashedLine(a.c2p(0, 0), a.c2p(1, 0), color=GREY_B, stroke_width=1.5)
        thr = b["threshold"]
        T = Dot(a.c2p(thr, 0), radius=0.1, color=EQ)
        now = Dot(a.c2p(b["prior_tough"], b["prior_tough"] * -2 + (1 - b["prior_tough"]) * 2), radius=0.09, color=ANA)
        side = VGroup(
            label(r"entering pays against a weak Ana \ (+2), \\ and costs against a tough one \ ($-2$)", font_size=21),
            label(rf"Bo enters if the chance Ana is tough \\ is below {thr:.1f}", font_size=22, color=EQ),
            label(r"so a weak Ana would like to look tough, \\ and a tough one to prove it", font_size=22, color=HOLD),
            label(r"signalling and reputation: \ Part 13; \\ bidding without knowing others' values: \ Part 16; \\ "
                  r"choosing what others get to know: \ Part 53", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "What Bo does depends on what he believes. <bookmark mark='a'/> Entering gains two if Ana shares and "
            "loses two if she fights, so his expected gain falls as his belief that she is tough rises. "
            "<bookmark mark='b'/> He enters as long as that belief is below one half. <bookmark mark='c'/> Which "
            "means a weak Ana would like Bo to think she is tough, and a tough Ana would like to prove it: beliefs "
            "become something players compete to shape. <bookmark mark='d'/> Signalling and reputation are Part "
            "thirteen; bidding when you don't know the others' values, Part sixteen; and choosing what others get to "
            "know, Part fifty-three."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(now))
            vo.wait_until("b")
            self.play(FadeIn(T), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
