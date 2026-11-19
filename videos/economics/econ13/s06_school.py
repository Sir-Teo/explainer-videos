from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403

STATE_A = "#7EC8F5"
STATE_B = "#F2A65A"


class School(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Is school a signal?", r"Does education raise earnings by making people more productive, \ or by "
             r"showing who already was?", "Chapter five. Is school a signal?", lit={2000: r"the GED's signal"},
             scale=("person", "nation"), horizon=("a decade", "a lifetime"))
        self.rival()
        self.ged()
        self.verdict()

    def rival(self):
        left = VGroup(
            label(r"human capital", font_size=32, color=GOOD),
            label(r"school teaches skills \\ employers pay for \\ (Becker, \ Mincer)", font_size=22),
            label(r"the return is \\ society's return too", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3)
        right = VGroup(
            label(r"signalling", font_size=32, color=SIGNAL),
            label(r"school shows who \\ was able already \\ (Spence)", font_size=22),
            label(r"the return is private: \\ society pays for a sort", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3)
        cols = VGroup(left, right).arrange(RIGHT, buff=2.2).move_to(UP * 0.7)
        bar = Line(UP * 2.4, DOWN * 0.9, color=GREY_C).move_to(cols.get_center())
        rows = VGroup(
            label(r"both predict that the educated earn more: \ the question is why", font_size=24, color=E.ACCENT),
            label(r"a clue: \ ``sheepskin effects'': \ the year that completes a diploma pays more than the years before "
                  r"it", font_size=22, color=LEMON),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Becker, \emph{Human Capital} (1964); \ Mincer (1974); \ Hungerford and Solon, REStat "
                            r"69(1) (1987)", corner=DR, font_size=12)
        with self.voiceover(
            "Is real school like the Island's? Two theories explain why the educated earn more. "
            "<bookmark mark='a'/> In the human capital theory of Gary Becker and Jacob Mincer, school teaches skills "
            "that employers pay for, so the return to a student is a return to society too. "
            "<bookmark mark='b'/> In Spence's theory, school shows who was able already, so the return is private, and "
            "society pays for an expensive sort. <bookmark mark='c'/> Both predict exactly what we see, that the "
            "educated earn more. The question is why. <bookmark mark='d'/> One clue is called the sheepskin effect, "
            "after the parchment diplomas were once printed on: in American data the year that completes a diploma "
            "seems to pay more than the years before it, as if the certificate itself were worth something."
        ) as vo:
            self.play(Create(bar), FadeIn(left[0]), FadeIn(right[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left[1:]))
            vo.wait_until("b")
            self.play(FadeIn(right[1:]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def ged(self):
        t = tables.TYLER_2000.data
        line = NumberLine(x_range=[30, 50, 5], length=10.0, include_numbers=True, font_size=20, color=GREY_B
                          ).move_to(UP * 1.6)
        ll = label(r"a dropout's score on the GED tests \ (an illustrative scale)", font_size=17, color=GREY_B
                   ).next_to(line, DOWN, buff=0.4)
        ta = VGroup(DashedLine(line.n2p(40) + DOWN * 0.3, line.n2p(40) + UP * 0.9, color=STATE_A, stroke_width=2.5),
                    label(r"one state's pass mark", font_size=17, color=STATE_A).next_to(line.n2p(40) + UP * 0.9, UP,
                                                                                       buff=0.05))
        tb = VGroup(DashedLine(line.n2p(45) + DOWN * 0.3, line.n2p(45) + UP * 0.9, color=STATE_B, stroke_width=2.5),
                    label(r"another's", font_size=17, color=STATE_B).next_to(line.n2p(45) + UP * 0.9, UP, buff=0.05))
        band = Rectangle(width=line.n2p(45)[0] - line.n2p(40)[0], height=0.3, stroke_width=0, fill_color=SIGNAL,
                         fill_opacity=0.35).move_to((line.n2p(40) + line.n2p(45)) / 2)
        rows = VGroup(
            label(r"John Tyler, \ Richard Murnane and John Willett (2000): \ the GED, \ a high-school equivalency "
                  r"certificate", font_size=22),
            label(r"states set different pass marks: \ a score between them earns the certificate in one state, \ not "
                  r"the other", font_size=22, color=SIGNAL),
            label(r"same skills, \ different certificate: \ any difference in earnings is the signal alone", font_size=22,
                  color=GREY_A),
            label(rf"young white dropouts at the margin: \ the certificate raised annual earnings by "
                  rf"{100 * t['white'][0]:.0f} to {100 * t['white'][1]:.0f}\%", font_size=23, color=EQ),
            label(r"for young nonwhite dropouts, \ no effect they could detect", font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.24).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Tyler, Murnane and Willett, QJE 115(2) (2000)", corner=UR, font_size=13)
        with self.voiceover(
            "A cleaner test came from a certificate. <bookmark mark='a'/> In America a dropout can sit the GED tests "
            "for a certificate meant to be equivalent to finishing high school. In 2000 John Tyler, Richard Murnane "
            "and John Willett noticed that states set different pass marks. <bookmark mark='b'/> A young dropout "
            "whose score falls between two states' marks gets the certificate in one state and not in the other. "
            "<bookmark mark='c'/> The skills are the same; only the certificate differs, so any difference in "
            "earnings is the signal alone. <bookmark mark='d'/> For young white dropouts on the margin of passing, the "
            "certificate raised annual earnings by ten to nineteen percent. <bookmark mark='e'/> For young nonwhite "
            "dropouts they found no effect they could detect, a reminder that a signal is only worth what employers "
            "believe it says."
        ) as vo:
            self.play(Create(line), FadeIn(ll), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(ta), FadeIn(tb), FadeIn(band), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def verdict(self):
        rows = VGroup(
            label(r"against pure signalling: \ when the law forced more schooling, \ earnings rose too \ (Part 4's "
                  r"quarter of birth)", font_size=23, color=GOOD),
            label(r"a forced extra year can't signal much: \ everyone had to take it", font_size=23, color=GREY_A),
            label(r"for signalling: \ diplomas, \ the GED, \ and how much of what is taught is never used at work",
                  font_size=23, color=SIGNAL),
            label(r"most economists conclude that both are at work; \ some, \ like Bryan Caplan (2018), \ argue that "
                  r"most of the return is signal", font_size=23),
            label(r"the share matters: \ subsidizing a signal buys a costlier sort, \ not more skill", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Angrist and Krueger, QJE 106(4) (1991); \ Caplan, \emph{The Case against Education} "
                            r"(2018)", corner=DR, font_size=13)
        with self.voiceover(
            "So which is it? <bookmark mark='a'/> Against pure signalling: when compulsory schooling laws forced some "
            "students to stay longer, their earnings rose too, as Part four's quarter-of-birth estimates showed. "
            "<bookmark mark='b'/> An extra year that everyone is forced to take cannot signal much, so at least part "
            "of the return must be skill. <bookmark mark='c'/> For signalling: diplomas seem to pay for themselves, "
            "the GED's certificate pays without any extra skill, and much of what is taught is never used at work. "
            "<bookmark mark='d'/> Most economists conclude that both are at work. Some, like Bryan Caplan in 2018, "
            "argue that most of the return is the signal. <bookmark mark='e'/> The share matters for policy: "
            "subsidizing a skill raises output, but subsidizing a signal only buys a more expensive sort."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
