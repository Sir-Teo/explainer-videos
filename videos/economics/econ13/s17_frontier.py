from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ selection on moral hazard, \ and the end of pooling", r"What if people choose "
             r"insurance by how much they'll use it, \ and what if insurers come to know more than we do?",
             "Chapter fifteen. Frontier: selection on moral hazard, and the end of pooling.",
             lit={2013: r"selection on moral hazard"}, scale=("person", "market", "world"), horizon=("a year",
                                                                                                    "a decade"))
        self.moral()
        self.pooling()
        self.open()

    def moral(self):
        rows = VGroup(
            label(r"Einav, \ Finkelstein, \ Ryan, \ Schrimpf and Cullen (2013): \ one firm, \ a change in the plans "
                  r"offered to some employees", font_size=22),
            label(r"people differ not only in how sick they are, \ but in how much more care they use when insured",
                  font_size=23, color=SIGNAL),
            label(r"and they choose cover partly on that: \ selection on moral hazard", font_size=24, color=LEMON),
            label(r"it mattered about as much as selection on health risk, \ and far more than on risk aversion",
                  font_size=23, color=GREY_A),
            label(r"so a high deductible saves less than it seems: \ those who would cut back most \ avoid it",
                  font_size=23, color=LOSS),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Einav, Finkelstein, Ryan, Schrimpf and Cullen, AER 103(1) (2013)", corner=DR, font_size=13)
        with self.voiceover(
            "Two frontiers. The first joins this part to the next. <bookmark mark='a'/> In 2013 Liran Einav, Amy "
            "Finkelstein, Stephen Ryan, Paul Schrimpf and Mark Cullen studied one firm that changed the health plans it "
            "offered to some of its employees but not others. <bookmark mark='b'/> People differ not only in how sick "
            "they are, but in how much more care they use once insured. <bookmark mark='c'/> And they choose their "
            "cover partly on that: selection on moral hazard. <bookmark mark='d'/> In their estimates it mattered "
            "about as much as selection on health risk, and much more than differences in risk aversion. "
            "<bookmark mark='e'/> The consequence: a high-deductible plan saves less than it seems, because the people "
            "who would cut back most when they pay more are exactly those who avoid it."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def pooling(self):
        rows = VGroup(
            label(r"insurance works by pooling: \ the lucky pay for the unlucky, \ because nobody knows which they are",
                  font_size=23),
            label(r"more data lets insurers price each person's risk: \ driving apps, \ health records, \ genes",
                  font_size=23, color=SIGNAL),
            label(r"the asymmetry can reverse: \ the insurer, \ or its algorithm, \ may know more than you do",
                  font_size=23, color=LEMON),
            label(r"perfect prediction would end insurance: \ the risk you were born with can't be pooled once "
                  r"it's known", font_size=23, color=LOSS),
            label(r"America's Genetic Information Nondiscrimination Act (2008) \ bars health insurers and employers "
                  r"from using genetic tests", font_size=22, color=GOOD),
            label(r"pricing by algorithm: \ Part 10's personalized prices, \ applied to risk", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.1)
        tag = published_tag(r"Genetic Information Nondiscrimination Act, Pub.\ L.\ 110-233 (2008)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "The second frontier is the end of pooling. <bookmark mark='a'/> Insurance works by pooling: the lucky pay "
            "for the unlucky, because nobody knows in advance which they will be. <bookmark mark='b'/> More data lets "
            "insurers price each person's own risk: driving apps, health records, genetic tests. "
            "<bookmark mark='c'/> The asymmetry of this part can even reverse, so that the insurer, or its algorithm, "
            "knows more about your risk than you do. <bookmark mark='d'/> Taken to its limit, perfect prediction "
            "would end insurance against the risks you are born with: once they are known, they can no longer be "
            "pooled. <bookmark mark='e'/> Some societies have drawn a line. America's Genetic Information "
            "Nondiscrimination Act of 2008 bars health insurers and employers from using genetic information. "
            "<bookmark mark='f'/> Pricing risk by algorithm is Part ten's personalized pricing, applied to risk."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def open(self):
        head = label(r"open questions", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"when should a society forbid pricing on what can be observed, \ and who pays for the pool?",
                  font_size=23),
            label(r"do the remedies' costs \ (taxes, \ mandates, \ forgone choice) \ exceed the triangles they close?",
                  font_size=23, color=LOSS),
            label(r"can information design \ (what a platform reveals, \ and to whom) \ beat bans? \ Part 53",
                  font_size=23, color=SIGNAL),
            label(r"how should a firm write a contract when it can't see effort? \ Part 14, \ next", font_size=23,
                  color=GOOD),
        ).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Open questions follow. When should a society forbid pricing on what can be seen, "
            "and who should pay for the pool that results? <bookmark mark='b'/> Do the remedies, with their taxes, "
            "mandates and lost choice, cost more than the triangles they close? <bookmark mark='c'/> Could "
            "information design, choosing what a platform reveals and to whom, work better than bans? That is Part "
            "fifty-three. <bookmark mark='d'/> And how should a contract be written when one side cannot see what the "
            "other does? That is the next part."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(rows[0], shift=UP * 0.1))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
