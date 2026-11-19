from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403
from videos.economics.econ7.compute import _eu_lines

PAIR1 = [("1A", [(r"for sure", r"\$1 million")], SAFE),
         ("1B", [(r"10\%", r"\$5 million"), (r"89\%", r"\$1 million"), (r"1\%", r"nothing")], RISKY)]
PAIR2 = [("2A", [(r"11\%", r"\$1 million"), (r"89\%", r"nothing")], SAFE),
         ("2B", [(r"10\%", r"\$5 million"), (r"90\%", r"nothing")], RISKY)]


def pair_cards(pair, font_size=26, width=4.4):
    return VGroup(*[lottery_card(rows, name, color=c, width=width, font_size=font_size) for name, rows, c in pair])


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Play it: \ Allais's two pairs", r"Would you take a sure million, or a gamble at five?",
             "Chapter four. Play it: Allais's two pairs.", lit={1953: r"Allais's paradox"}, horizon=("a day",))
        self.choose(PAIR1, 1, "Here is the first choice. Option 1A: a million dollars, for sure. Option 1B: a ten "
                    "percent chance of five million, an eighty-nine percent chance of one million, and a one percent "
                    "chance of nothing. Pause the film and choose: 1A or 1B?")
        self.choose(PAIR2, 2, "Write your choice down. Now a second choice. Option 2A: an eleven percent chance of a "
                    "million, and otherwise nothing. Option 2B: a ten percent chance of five million, and otherwise "
                    "nothing. Pause, and choose again: 2A or 2B?")
        self.reveal()
        self.algebra()
        self.in_triangle()
        self.lunch()

    def choose(self, pair, n, say):
        stage = game_stage(11.6, 5.6, center=DOWN * 0.2)
        cards = pair_cards(pair, font_size=28, width=4.8).arrange(RIGHT, buff=1.2).move_to(stage.box.get_center() +
                                                                                           UP * 0.4)
        q = label(rf"choice {n}: \ which would you take?", font_size=30).next_to(cards, UP, buff=0.4)
        ring = countdown().next_to(cards, DOWN, buff=0.5)
        with self.voiceover(say):
            self.play(FadeIn(stage), FadeIn(q))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.5), run_time=1.6)
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=6.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        t = load("triangle")
        c1 = pair_cards(PAIR1, font_size=22, width=3.7).arrange(RIGHT, buff=0.4)
        c2 = pair_cards(PAIR2, font_size=22, width=3.7).arrange(RIGHT, buff=0.4)
        rows = VGroup(c1, c2).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        picks = VGroup(SurroundingRectangle(c1[0], color=WHITE, buff=0.08, stroke_width=3),
                       SurroundingRectangle(c2[1], color=WHITE, buff=0.08, stroke_width=3))
        side = VGroup(
            label(r"the most common answers:", font_size=27),
            label(r"1A, \ the sure million; \\ and 2B, \ the five-million gamble", font_size=27, color=E.ACCENT),
            label(rf"Kahneman and Tversky (1979), \\ the same pattern in smaller sums: \\ "
                  rf"{100 * t['kt']:.0f}\% took the sure thing in the first pair, \\ most took the gamble in the "
                  rf"second", font_size=22, color=GREY_A),
            label(r"sensible? \ most people think so", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        tag = published_tag(r"Allais, Econometrica (1953); Kahneman and Tversky, Econometrica (1979), p.\ 265",
                            corner=DR, font_size=13)
        with self.voiceover(
            "If you're like most people, <bookmark mark='a'/> you took the sure million in the first pair: why risk "
            "a sure fortune for a one percent chance of ending up with nothing? And in the second pair you took the "
            "gamble: the chances of winning are almost the same, eleven percent against ten, and the prize is five "
            "times as large. <bookmark mark='b'/> When Daniel Kahneman and Amos Tversky put the same structure to "
            "their subjects in 1979, with smaller sums, eighty-two percent took the sure thing in the first pair, and most "
            "took the gamble in the second. <bookmark mark='c'/> Both answers feel sensible. Together, they break "
            "expected utility."
        ) as vo:
            self.play(FadeIn(rows), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(picks[0]), FadeIn(side[0]), FadeIn(side[1]))
            self.play(Create(picks[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def algebra(self):
        rows = VGroup(
            MathTex(r"EU(1A) - EU(1B)", r"\;=\;", r"0.11\,u(1\text{M})", r"-", r"0.10\,u(5\text{M})", r"-",
                    r"0.01\,u(0)", font_size=38),
            MathTex(r"EU(2A) - EU(2B)", r"\;=\;", r"0.11\,u(1\text{M})", r"-", r"0.10\,u(5\text{M})", r"-",
                    r"0.01\,u(0)", font_size=38),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 1.4)
        for r_ in rows:
            r_[2].set_color(SAFE)
            r_[4].set_color(RISKY)
        same = label(r"the same number: \ if 1A beats 1B, \ 2A must beat 2B", font_size=30,
                     color=E.ACCENT).next_to(rows, DOWN, buff=0.55)
        why = VGroup(
            label(r"why: \ each pair shares an 89\% chance of one prize", font_size=26),
            label(r"pair 1: \ 89\% of \$1 million in both; \ pair 2: \ 89\% of nothing in both", font_size=24,
                  color=GREY_A),
            label(r"independence says a shared part shouldn't matter, \ whatever it is", font_size=26, color=EUL),
        ).arrange(DOWN, buff=0.22).next_to(same, DOWN, buff=0.5)
        head = label(r"why the common answers break expected utility", font_size=32,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        rows.next_to(head, DOWN, buff=0.5)
        same.next_to(rows, DOWN, buff=0.5)
        why.next_to(same, DOWN, buff=0.45)
        with self.voiceover(
            "Here's why. Write out the difference in expected utility between 1A and 1B. <bookmark mark='a'/> It's "
            "eleven hundredths of the utility of a million, minus ten hundredths of the utility of five million, "
            "minus one hundredth of the utility of nothing. <bookmark mark='b'/> Now do the same for 2A against 2B. "
            "It's exactly the same expression. <bookmark mark='c'/> So whatever your utility function, if 1A beats "
            "1B, then 2A must beat 2B. <bookmark mark='d'/> The reason is that each pair is built from the other by "
            "changing a part the two options share. In the first pair, both options include an eighty-nine percent "
            "chance of a million; in the second, that shared chance is of nothing instead. The independence axiom "
            "says a part both options share shouldn't affect which you prefer."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(Write(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(Write(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(same))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(w_) for w_ in why], lag_ratio=0.6), run_time=3)
        self.clear_scene()

    def in_triangle(self):
        t = load("triangle")
        tr = triangle(center=LEFT * 3.2 + DOWN * 0.2, side=5.2)
        pts = {k: tr.p(*v) for k, v in t["points"].items()}
        dots = VGroup(*[Dot(pts[k], radius=0.08, color=SAFE if k.endswith("A") else RISKY) for k in pts])
        names = VGroup(
            label(r"1A", font_size=20, color=SAFE).next_to(pts["1A"], LEFT, buff=0.1).shift(UP * 0.25),
            label(r"1B", font_size=20, color=RISKY).next_to(pts["1B"], RIGHT, buff=0.1),
            label(r"2A", font_size=20, color=SAFE).next_to(pts["2A"], UL, buff=0.06),
            label(r"2B", font_size=20, color=RISKY).next_to(pts["2B"], RIGHT, buff=0.1))
        ch1 = Line(pts["1A"], pts["1B"], color=E.ACCENT, stroke_width=4)
        ch2 = Line(pts["2A"], pts["2B"], color=E.ACCENT, stroke_width=4)
        fam = t["families"]["0.9"]
        lines = VGroup(*[tri_path(tr, p_, color=EUL, width=2.2, opacity=0.8) for p_ in _eu_lines(fam["slope"], 9)])
        fam2 = t["families"]["0.95"]
        lines2 = VGroup(*[tri_path(tr, p_, color=EUL, width=2.2, opacity=0.8) for p_ in _eu_lines(fam2["slope"], 9)])
        side = VGroup(
            label(r"the four lotteries in the triangle", font_size=25),
            label(r"1A $\to$ 1B \ and \ 2A $\to$ 2B: \\ parallel moves, \ slope 10", font_size=25, color=E.ACCENT),
            label(r"lines flatter than 10: \ B is better in both pairs", font_size=23, color=EUL),
            label(r"lines steeper than 10: \ A is better in both", font_size=23, color=EUL),
            label(r"1A with 2B needs lines steep at the left \\ and shallow at the right: \\ not parallel, \ not "
                  r"expected utility", font_size=24, color=FAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "In the triangle the point is plain. <bookmark mark='a'/> Here are the four lotteries: 1A at the corner, "
            "the sure million; 1B just above and to its right; 2A and 2B far over on the right, near the corner for "
            "nothing. <bookmark mark='b'/> The move from 1A to 1B and the move from 2A to 2B are parallel arrows, "
            "with the same slope of ten. <bookmark mark='c'/> Expected utility's indifference lines are parallel "
            "too. If they're flatter than the arrows, the B lottery is better in both pairs. <bookmark mark='d'/> If "
            "they're steeper, A is better in both. <bookmark mark='e'/> Choosing 1A and then 2B needs lines that are "
            "steep on the left of the triangle and shallow on the right. They can't be parallel. Something other "
            "than expected utility is going on, and chapter eight comes back to what."
        ) as vo:
            self.play(FadeIn(tr), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(names))
            vo.wait_until("b")
            self.play(Create(ch1), Create(ch2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(ReplacementTransform(lines, lines2), FadeIn(side[3]), run_time=1.6)
            vo.wait_until("e")
            self.play(FadeOut(lines2), FadeIn(side[4]))
        self.clear_scene()

    def lunch(self):
        a = tables.ALLAIS_1953.data
        hc = history_card(r"May 1952", r"Paris: \ a colloquium on risk", r"Maurice Allais puts his two pairs to "
                          r"Leonard Savage over lunch; \ Savage, the axiom's champion, \ answers against it",
                          color=FAN, width=9.6, font_size=25).move_to(UP * 1.3)
        later = VGroup(
            label(r"Savage, \ \emph{The Foundations of Statistics} (1954): \ on reflection, \ he changed his answer",
                  font_size=25, color=GREY_A),
            label(r"Allais, \ \emph{Econometrica} (1953): \ the ``American school'' describes neither real choice "
                  r"\\ nor, he argued, rational choice", font_size=25, color=GREY_A),
            label(r"is the axiom a description of how people choose, \ or advice on how they should?", font_size=28,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.35).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Allais (1953); Savage (1954), ch.\ 5", corner=DR, font_size=14)
        with self.voiceover(
            "The pairs are Maurice Allais's. <bookmark mark='a'/> In May 1952, at a colloquium on risk in Paris, he "
            "put them to Leonard Savage over lunch. Savage was the axiom's great champion, and his answers broke "
            "it. <bookmark mark='b'/> In his book two years later Savage wrote that, on "
            "reflection, he had changed his mind: the axiom was right and his first answer a mistake. Allais "
            "published the pairs in Econometrica in 1953, arguing the reverse: that what he called the American school "
            "described neither how people choose nor how a rational person should. <bookmark mark='c'/> That is the "
            "question every paradox in this part raises. Is expected utility a description of behaviour, or advice?"
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(hc, color=FAN, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(later[0]), FadeIn(later[1]))
            vo.wait_until("c")
            self.play(FadeIn(later[2]))
        self.clear_scene()
