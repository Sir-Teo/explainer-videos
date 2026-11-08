from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Peers(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"When peers disagree", r"Should you split the difference?", lit=(), part=PART)
        with self.voiceover("Chapter thirteen. When peers disagree."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.bill()
        self.views()
        self.higher()

    def bill(self):
        d = load("peers")
        head = label(r"The restaurant bill", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        who = label(r"Christensen (2007)", font_size=21, color=GREY_B).next_to(head, DOWN, buff=0.15)
        me = person(r"I say \$43", color=AG["A"], scale=0.9).move_to([-3.8, 1.0, 0])
        you = person(r"my friend says \$45", color=AG["B"], scale=0.9).move_to([-1.0, 1.0, 0])
        rows = VGroup(
            label(rf"each of us gets such sums right {round(100 * d['reliability'])}\% of the time", font_size=22),
            label(rf"I'm right, \ she's wrong: \ ${d['me_right']:.2f}$", font_size=22, color=AG["A"]),
            label(rf"she's right, \ I'm wrong: \ ${d['peer_right']:.2f}$", font_size=22, color=AG["B"]),
            label(rf"both wrong \ (and so, \ almost surely, \ different): \ ${d['both_wrong']:.2f}$", font_size=22,
                  color=GREY_A),
            label(rf"so, \ given that we disagree: \ $P(\text{{I'm right}}) = {d['posterior']:.2f}$", font_size=26,
                  color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.2, -0.2, 0])
        f = MathTex(r"\frac{0.09}{0.09 + 0.09 + 0.01}", font_size=34).move_to([-2.4, -1.6, 0])
        foot = label(r"from 90\% to under 50\%: \ the disagreement is strong evidence", font_size=24,
                     color=OK).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now take two people who disagree. David Christensen's example. <bookmark mark='a'/>After dinner, my "
            "friend and I each work out our share of the bill in our heads. I get forty-three dollars; she gets "
            "forty-five. We are equally good at this, and each of us gets such sums right nine times in ten. "
            "<bookmark mark='b'/>The Reasoner treats it as a Bayesian problem. Before we compare, there is a nine in "
            "a hundred chance that I am right and she is wrong; <bookmark mark='c'/>the same chance that she is "
            "right and I am wrong; <bookmark mark='d'/>and a one in a hundred chance that we are both wrong, in which "
            "case our answers almost certainly differ. <bookmark mark='e'/>Given that we disagree, the chance that I "
            "am the one who is right is nine out of nineteen: just under a half. My confidence should fall from "
            "ninety percent to below fifty, which is what the equal weight view says: treat your peer's verdict as "
            "you treat your own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeIn(me), FadeIn(you), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            self.play(Write(f))
            self.play(FadeIn(foot))
        self.clear_scene()

    def views(self):
        head = label(r"Three views", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        hd = [label(r"view", font_size=22, color=P.CLAIM), label(r"says", font_size=22, color=P.CLAIM),
              label(r"its hard case", font_size=22, color=P.CLAIM)]
        rows = [[label(r"equal weight \ (Elga 2007)", font_size=20),
                 label(r"a peer's opinion counts as much as yours", font_size=19),
                 label(r"suspend judgment almost everywhere?", font_size=19)],
                [label(r"steadfast", font_size=20),
                 label(r"keep your view, \ if you reasoned well", font_size=19),
                 label(r"but which of you did?", font_size=19)],
                [label(r"total evidence \ (Kelly 2010)", font_size=20),
                 label(r"weigh the evidence and the disagreement", font_size=19),
                 label(r"how much each counts is the dispute", font_size=19)]]
        grid = ValueGrid(hd, rows, col_w=[3.6, 5.0, 4.4], cell_h=0.7, font_size=19).move_to([0, 0.4, 0])
        foot = VGroup(label(r"Christensen's extreme case: \ she says \$450 \ on a \$200 bill", font_size=23,
                            color=GOAL),
                      label(r"I am sure she's wrong: \ the answer itself is independent evidence of her error",
                            font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Three views have emerged. <bookmark mark='a'/>Adam Elga's equal weight view: give your peer's opinion "
            "the same weight as your own. Its difficulty is that, applied to philosophy, politics and religion, where "
            "peers disagree about everything, it seems to require suspending judgment almost everywhere. "
            "<bookmark mark='b'/>The steadfast view: if you reasoned well, you may keep your conclusion. But from "
            "the inside, you cannot tell which of you reasoned well. <bookmark mark='c'/>Thomas Kelly's total "
            "evidence view weighs the original evidence and the fact of disagreement together; the difficulty is "
            "that how much each should count is exactly what is in dispute. <bookmark mark='d'/>All agree on one "
            "case. If my friend says her share is four hundred and fifty dollars, on a two hundred dollar bill, I may "
            "stay confident that she is wrong. Her answer is itself independent evidence that something went wrong "
            "with her, not with me."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg))
            for mk, r in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*grid.cell[r])))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def higher(self):
        head = label(r"Higher-order evidence", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"a pilot checks her fuel: \ enough to reach the airport, \ by a correct calculation", font_size=23),
            label(r"then she learns: \ at this altitude, \ most pilots suffer hypoxia", font_size=23, color=GREY_A),
            label(r"which impairs reasoning \ without feeling impaired", font_size=23, color=GREY_A),
            label(r"her calculation was right; \ should she now trust it less?", font_size=25, color=GOAL),
            label(r"most say yes: \ evidence about your own reliability \ is evidence", font_size=23, color=OK),
            label(r"a peer's disagreement is evidence of this kind \ (Christensen 2010; \ Lasonen-Aarnio 2014)",
                  font_size=21, color=GREY_B)).arrange(DOWN, buff=0.27).move_to([0, -0.4, 0])
        with self.voiceover(
            "The deepest question here concerns evidence about yourself. <bookmark mark='a'/>A pilot checks her fuel "
            "and calculates, correctly, that she has enough to reach the airport. <bookmark mark='b'/>Then she learns "
            "that at her altitude most pilots suffer hypoxia, <bookmark mark='c'/>which impairs reasoning without "
            "any feeling of impairment. <bookmark mark='d'/>Her calculation was in fact right. Should she now trust "
            "it less? <bookmark mark='e'/>Most say yes: evidence about the reliability of your own thinking is "
            "evidence, even when your thinking was fine. <bookmark mark='f'/>A peer's disagreement is evidence of the "
            "same kind, and philosophers still dispute how much such higher-order evidence should count."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
