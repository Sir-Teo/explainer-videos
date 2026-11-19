from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403

NJ = "#F26D6D"
PA = "#5DADEC"


class Credibility(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The credibility revolution", r"Where can you find an experiment nobody designed?",
             "Chapter seven. The credibility revolution.", scale=("person", "nation"), horizon=("a lifetime",))
        self.lottery()
        self.birthdays()
        self.border()
        self.revolution()

    def lottery(self):
        chain = flow_chain([(r"lottery number", E.ACCENT), (r"served in Vietnam", GREY_A),
                            (r"earnings in the 1980s", EXP)], box_w=3.3, box_h=0.95, buff=1.0, font_size=28,
                           notes=[r"a birthday drawn at random", r"low numbers were more likely to be drafted",
                                  r"the only route from the lottery"], note_size=21)
        chain.move_to(UP * 1.0)
        res = VGroup(
            label(r"Joshua Angrist, 1990: \ Social Security earnings records", font_size=26, color=E.ACCENT),
            label(r"white veterans earned about 15\% less than they would have, \\ in the early 1980s", font_size=26,
                  color=EXP),
            label(r"comparing veterans with non-veterans directly: \ who volunteered?", font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(chain, DOWN, buff=0.9)
        tag = published_tag(r"J.\ D.\ Angrist, AER 80(3) (1990), abstract", corner=DR, font_size=15)
        with self.voiceover(
            "The intermission's lottery was a real one, and it became one of the most famous instruments in "
            "economics. <bookmark mark='a'/> Your birthday's number decided how likely you were to be drafted to "
            "Vietnam. <bookmark mark='b'/> Men with low numbers were more likely to serve. <bookmark mark='c'/> And "
            "the number itself, a capsule drawn from a glass jar, could affect a man's later earnings only through "
            "whether he served. <bookmark mark='d'/> In 1990 Joshua Angrist used it with Social Security earnings "
            "records, and found that in the early 1980s white veterans earned about fifteen percent less than "
            "they would have otherwise, the equivalent of losing two years of work experience. For non-white "
            "veterans he found no lasting loss. Simply comparing veterans with non-veterans could never have told "
            "him this, because the men who served differed from those who didn't in many other ways."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]))
            vo.wait_until("a")
            self.play(Indicate(chain.boxes[0], color=E.ACCENT))
            vo.wait_until("b")
            self.play(GrowArrow(chain.arrows[0]), FadeIn(chain.boxes[1]), FadeIn(chain.notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(chain.arrows[1]), FadeIn(chain.boxes[2]), FadeIn(chain.notes[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.4))
        self.clear_scene()

    def birthdays(self):
        dl = load("dial")
        rows = [r for r in dl["rows"] if r[0].startswith("Angrist and Krueger")]
        head = VGroup(label(r"born early in the year: \ older when school starts, \\ so the law lets them leave with "
                            r"a little less schooling", font_size=26),
                      label(r"Angrist and Krueger, 1991: \ quarter of birth as the instrument", font_size=26,
                            color=E.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.5)
        table = VGroup(VGroup(label(r"men born", font_size=23, color=GREY_B), label(r"least squares", font_size=23,
                                                                                     color=OLSC),
                              label(r"instrument", font_size=23, color=IVC)))
        for r in rows:
            table.add(VGroup(label(r[1].split(",")[0].replace("US men born ", "").replace("-", "--"), font_size=24),
                             label(f"{r[2]:.3f}", font_size=26, color=OLSC),
                             label(rf"{r[3]:.3f} \ ({r[4]:.3f})", font_size=26, color=IVC)))
        for t in table:
            for i, x in enumerate((-3.2, 0.2, 3.4)):
                t[i].move_to([x, 0, 0])
        table.arrange(DOWN, buff=0.35).move_to(DOWN * 0.6)
        for t in table:
            for i, x in enumerate((-3.2, 0.2, 3.4)):
                t[i].set_x(x)
        note_ = label(r"the instrument agrees with least squares, \ or exceeds it: \ little sign of ability bias",
                      font_size=24, color=E.ACCENT).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Angrist and Krueger, QJE 106(4) (1991), via Card (2001), table 2", corner=DR,
                            font_size=14)
        with self.voiceover(
            "Other instruments came from the oddities of law. <bookmark mark='a'/> American children start school "
            "in the year they turn six, and may leave when they turn sixteen. So a boy born in January is older "
            "when he starts school than one born in December, and reaches the leaving age having sat through a "
            "little less of it. In 1991 Joshua Angrist and Alan Krueger used the quarter of birth as an "
            "instrument for schooling. <bookmark mark='b'/> Their estimates of the return to a year of school came "
            "out about as large as the plain least-squares ones, or larger: little sign of the ability bias that "
            "everyone had feared. A birthday isn't an experiment, but it isn't a choice either."
        ) as vo:
            self.play(FadeIn(head[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), FadeIn(table[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in table[1:]], lag_ratio=0.3))
            self.play(FadeIn(note_))
        self.clear_scene()

    def border(self):
        c = load("credibility")
        ax = axes([0, 3], [18, 25], x_length=5.6, y_length=4.6, yticks=[18, 20, 22, 24],
                  ylabel=r"full-time-equivalent employees per restaurant", font_size=20, center=LEFT * 2.6 + DOWN * 0.3)
        a = ax.ax
        xl = VGroup(label(r"Feb.--Mar.\ 1992", font_size=20, color=GREY_B).next_to(a.c2p(0.6, 18), DOWN, buff=0.15),
                    label(r"Nov.--Dec.\ 1992", font_size=20, color=GREY_B).next_to(a.c2p(2.4, 18), DOWN, buff=0.15))
        nj = VGroup(Line(a.c2p(0.6, c["NJ"][0]), a.c2p(2.4, c["NJ"][1]), color=NJ, stroke_width=5),
                    Dot(a.c2p(0.6, c["NJ"][0]), color=NJ), Dot(a.c2p(2.4, c["NJ"][1]), color=NJ))
        pa = VGroup(Line(a.c2p(0.6, c["PA"][0]), a.c2p(2.4, c["PA"][1]), color=PA, stroke_width=5),
                    Dot(a.c2p(0.6, c["PA"][0]), color=PA), Dot(a.c2p(2.4, c["PA"][1]), color=PA))
        cf = c["NJ"][0] + (c["PA"][1] - c["PA"][0])
        cfl = DashedLine(a.c2p(0.6, c["NJ"][0]), a.c2p(2.4, cf), color=NJ, stroke_width=3, stroke_opacity=0.7)
        gap = Arrow(a.c2p(2.55, cf), a.c2p(2.55, c["NJ"][1]), buff=0, color=E.ACCENT, stroke_width=4,
                    max_tip_length_to_length_ratio=0.25)
        rows = VGroup(
            label(r"1 April 1992: \ New Jersey's minimum wage \\ rises from \$4.25 to \$5.05; \ Pennsylvania's "
                  r"does not", font_size=24),
            label(rf"New Jersey: \ {c['NJ'][0]:.2f} $\to$ {c['NJ'][1]:.2f}", font_size=24, color=NJ),
            label(rf"Pennsylvania: \ {c['PA'][0]:.2f} $\to$ {c['PA'][1]:.2f}", font_size=24, color=PA),
            label(rf"difference in differences: \ $+{c['did']:.2f}$ \ (s.e.\ {c['se_did']:.2f})", font_size=26,
                  color=E.ACCENT),
            label(r"disputed ever since: \ Part 38", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        tag = published_tag(rf"Card and Krueger, AER (1994), table 3: {c['n_NJ']} New Jersey and {c['n_PA']} "
                            r"Pennsylvania fast-food restaurants", corner=DL, font_size=14)
        with self.voiceover(
            "A third kind of natural experiment is a border. <bookmark mark='a'/> On the first of April 1992 New "
            "Jersey raised its minimum wage from four dollars twenty-five to five dollars and five cents. Next door, "
            "eastern Pennsylvania didn't. David Card and Alan Krueger surveyed fast-food restaurants on both sides, "
            "before and after. <bookmark mark='b'/> In New Jersey, employment per restaurant rose slightly. "
            "<bookmark mark='c'/> In Pennsylvania, it fell. <bookmark mark='d'/> If New Jersey had followed "
            "Pennsylvania's path, it would have ended here. The gap between that and what happened is the "
            "difference in differences: about two and three-quarter workers per restaurant, more, not fewer. "
            "<bookmark mark='e'/> The finding upended a textbook prediction, and it has been argued over ever "
            "since. Part 38 takes up the argument."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=E.ACCENT))
            vo.wait_until("b")
            self.play(Create(nj[0]), FadeIn(nj[1:]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(pa[0]), FadeIn(pa[1:]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(cfl), GrowArrow(gap), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def revolution(self):
        designs = point_cards([
            (r"instruments", r"something that moves the cause \\ and nothing else: \ a lottery, a birthday", IVC),
            (r"difference in differences", r"a group that changed beside \\ one that did not: \ a border", E.ACCENT),
            (r"regression discontinuity", r"a rule with a cutoff: \\ just above against just below", "#F28C6F"),
            (r"randomized experiments", r"the lottery, \ run on purpose", EXP),
        ], width=12.4, cols=2, font_size=23).move_to(DOWN * 0.1)
        head = label(r"The credibility revolution", font_size=36).to_edge(UP, buff=0.4)
        foot = label(r"Nobel prize, 2021: \ David Card; \ Joshua Angrist and Guido Imbens", font_size=25,
                     color=E.ACCENT).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Angrist and Pischke, JEP 24(2) (2010); \emph{Statistics, Built} Parts 35--37", corner=DR,
                            font_size=13).shift(UP * 0.5)
        with self.voiceover(
            "By 2010 Joshua Angrist and Jörn-Steffen Pischke could call it the credibility revolution, and say it "
            "had taken the con out of econometrics. Its tools are designs. <bookmark mark='a'/> Instruments: "
            "something that moves the cause and nothing else. <bookmark mark='b'/> Differences in differences: a "
            "group that changed beside one that didn't. <bookmark mark='c'/> Regression discontinuities: a rule "
            "with a cutoff, comparing people just above it with people just below. <bookmark mark='d'/> And, "
            "where possible, a lottery run on purpose. <bookmark mark='e'/> In 2021 the Nobel prize went to Card, "
            "and to Angrist and Guido Imbens, who showed exactly what an instrument identifies. The statistics of "
            "these designs is in Statistics, Built, Parts 35 to 37."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c_ in zip("abcd", designs.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
