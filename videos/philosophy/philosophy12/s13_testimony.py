from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Testimony(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Taking someone's word", r"When may we believe what we are told?", lit=(1748,),
                            part=PART)
        with self.voiceover("Chapter twelve. Taking someone's word."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.sides()
        self.miracles()
        self.injustice()

    def sides(self):
        head = label(r"Two views of testimony", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        a = VGroup(label(r"reductionism", font_size=27, color=AG["A"]),
                   label(r"Hume, \ \textit{Enquiry} \S 10 \ (1748)", font_size=20, color=GREY_B),
                   label(r"trust in testimony is justified", font_size=22),
                   label(r"by our experience of its reliability,", font_size=22),
                   label(r"like any other induction", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.14)
        b = VGroup(label(r"anti-reductionism", font_size=27, color=AG["B"]),
                   label(r"Reid, \ \textit{Inquiry} \ (1764); \ Coady, \ \textit{Testimony} \ (1992)", font_size=20,
                         color=GREY_B),
                   label(r"we are built to believe what we are told:", font_size=22),
                   label(r"a principle of credulity, \ matched by veracity", font_size=22),
                   label(r"testimony is a basic source, \ like perception", font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.14)
        cols = VGroup(a, b).arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to([0, 0.7, 0])
        foot = VGroup(label(r"Coady's objection: \ the experience Hume appeals to \ is mostly itself learned from "
                            r"testimony", font_size=22, color=BAD),
                      label(r"few of us have checked that the Earth is round, \ or our own birthdays", font_size=21,
                            color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Most of what we know, we were told. <bookmark mark='a'/>David Hume thought that our trust in testimony "
            "is justified the same way as any other belief about the world: by experience, which shows that what "
            "people tell us usually turns out to be true. This view is called reductionism. "
            "<bookmark mark='b'/>Thomas Reid replied that we are made to believe what we are told, by a principle of "
            "credulity, matched in speakers by a principle of veracity, a disposition to tell the truth. Testimony is "
            "a basic source of knowledge, like perception. <bookmark mark='c'/>In 1992 C. A. J. Coady pressed the "
            "decisive objection to Hume's global version. The experience Hume appeals to is itself mostly learned "
            "from testimony. Few of us have checked that the Earth is round, or even the date of our own birth."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def miracles(self):
        d = load("miracles")["rows"]
        hc = history_card(1748, r"David Hume", r"`Of Miracles', \ \textit{Enquiry} \S 10", width=5.0,
                          color=HIST).to_corner(UL, buff=0.35)
        q = quote_card(r"No testimony is sufficient to establish a miracle, unless the testimony be of such a kind, "
                       r"that its falsehood would be more miraculous, than the fact, which it endeavours to "
                       r"establish.", r"David Hume", r"\textit{Enquiry} X.i", width=7.4, font_size=22).move_to(
            [2.8, 2.0, 0])
        f = MathTex(r"P(\text{miracle} \mid \text{report}) = \frac{P(m)\,r}{P(m)\,r + (1 - P(m))(1 - r)}",
                    font_size=32).move_to([0, 0.3, 0])
        hd = [label(r"prior of the miracle", font_size=21, color=P.CLAIM),
              label(r"witness right", font_size=21, color=P.CLAIM),
              label(r"believe the miracle?", font_size=21, color=P.CLAIM)]

        def pct(x, digits=4):
            return rf"{100 * x:.{digits}g}\%"
        rows = [[label(r"1 in a million", font_size=21), label(pct(r["reliability"], 8), font_size=21),
                 label(pct(r["posterior"]), font_size=21, color=(OK if r["posterior"] > 0.5 else BAD))] for r in d]
        grid = ValueGrid(hd, rows, col_w=[3.4, 3.0, 3.4], cell_h=0.52, font_size=21).move_to([0, -1.6, 0])
        foot = label(r"the threshold is exactly Hume's: \ when the witness's error is rarer than the miracle",
                     font_size=23, color=GOAL).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Hume's most famous use of the reductionist view is his essay on miracles. <bookmark mark='a'/>No "
            "testimony is sufficient to establish a miracle, he wrote, unless its falsehood would be more miraculous "
            "than the fact it tries to establish. <bookmark mark='b'/>Bayes's theorem makes the maxim exact. Let the "
            "miracle have prior probability P, and the witness be right with probability r. <bookmark mark='c'/>The "
            "Reasoner computes three cases. A miracle with a prior of one in a million, and a witness who is right "
            "ninety-nine times in a hundred: after the report, the miracle is still less than one chance in ten "
            "thousand. A witness wrong only once in a million: now it is even odds. And only a witness more reliable "
            "than the miracle is improbable makes belief reasonable. <bookmark mark='d'/>That is exactly Hume's line: "
            "the testimony's falsehood must be more miraculous than the miracle."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Write(f))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(3)], lag_ratio=0.7), run_time=6)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def injustice(self):
        hc = history_card(2007, r"Miranda Fricker", r"\textit{Epistemic Injustice}", width=4.8, color=HIST).to_corner(
            UL, buff=0.35)
        a = VGroup(label(r"testimonial injustice", font_size=26, color=BAD),
                   label(r"a speaker is given less credibility", font_size=22),
                   label(r"because of prejudice about who she is", font_size=22),
                   label(r"Fricker's example: \ Tom Robinson's testimony,", font_size=20, color=GREY_A),
                   label(r"\textit{To Kill a Mockingbird}", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.14)
        b = VGroup(label(r"hermeneutical injustice", font_size=26, color=GOAL),
                   label(r"a group lacks the shared concepts", font_size=22),
                   label(r"to make sense of its own experience", font_size=22),
                   label(r"before `sexual harassment' was named \ (1970s),", font_size=20, color=GREY_A),
                   label(r"victims could not say what was wrong", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.14)
        cols = VGroup(a, b).arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to([0, 0.2, 0])
        foot = label(r"a wrong to someone in her capacity as a knower, \ and a loss to everyone who could have "
                     r"learned from her", font_size=23, color=OK).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Testimony is also a matter of justice. <bookmark mark='a'/>Miranda Fricker named testimonial "
            "injustice: a speaker is given less credibility than she deserves because of prejudice about who she "
            "is. Her central example is Tom Robinson in To Kill a Mockingbird, whose true testimony a jury will not "
            "believe. <bookmark mark='b'/>Hermeneutical injustice is subtler: a group lacks the shared concepts to "
            "make sense of its own experience. Before the term sexual harassment was coined, in the 1970s, its "
            "victims had no ready way to say what was being done to them. <bookmark mark='c'/>Both wrong someone "
            "in her capacity as a knower. And both are losses for everyone else, who could have learned from her."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

