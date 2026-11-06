from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


def rooms(n=9, w=1.2, y=0.0, x0=-5.4):
    g = VGroup()
    for i in range(n):
        r = VGroup(Rectangle(width=w * 0.9, height=1.0, stroke_color=GREY_B, stroke_width=2),
                   MathTex(str(i + 1), font_size=22, color=GREY_B))
        r[1].next_to(r[0], DOWN, buff=0.1)
        r.move_to([x0 + w * i, y, 0])
        g.add(r)
    dots = MathTex(r"\cdots", font_size=40, color=GREY_B).next_to(g, RIGHT, buff=0.25)
    return g, dots


def guest(color, label_=None):
    d = Circle(radius=0.22, color=color, fill_color=color, fill_opacity=0.5, stroke_width=2)
    return VGroup(d, MathTex(label_, font_size=20).move_to(d)) if label_ else VGroup(d)


class Hotel(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Infinite hotels", r"Can a part be as large as the whole?", lit=(1638, 1851),
                            part=PART)
        with self.voiceover("Chapter one. Infinite hotels."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.aristotle()
        self.one_guest()
        self.bus()
        self.dedekind()

    def aristotle(self):
        hcs = VGroup(history_card(r"c.\ 350 BCE", r"Aristotle, \textit{Physics} III", r"the infinite is only "
                                  r"\textit{potential}: \ you can always go on, \ never finish", width=6.0, color=HIST),
                     history_card(1638, r"Galileo, \textit{Two New Sciences}", r"`equal', `greater' and `less' do not "
                                  r"apply to infinite quantities", width=6.0, color=HIST)).arrange(RIGHT, buff=0.4)
        hcs.to_edge(UP, buff=0.5)
        pot = VGroup(MathTex(r"1,\ 2,\ 3,\ \dots", font_size=44), label(r"potential: \ a process that never ends",
                                                                         font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.2).move_to([-3.4, -1.0, 0])
        act = VGroup(MathTex(r"\{1, 2, 3, \dots\}", font_size=44, color=GOAL),
                     label(r"actual: \ a completed whole, \ an object", font_size=24, color=GOAL)).arrange(
            DOWN, buff=0.2).move_to([3.4, -1.0, 0])
        with self.voiceover(
            "For two thousand years the infinite was kept at arm's length. <bookmark mark='a'/>Aristotle allowed "
            "it only as a potential: you can always count one more, but you never finish, and there is no completed "
            "infinite collection. <bookmark mark='b'/>Galileo, in 1638, met the squares and the numbers, and drew "
            "the moral that comparisons of size simply do not apply to infinite totals. <bookmark mark='c'/>Cantor's "
            "revolution was to treat the infinite as actual, a completed set, an object with a size of its own."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hcs[0]), FadeIn(pot))
            vo.wait_until("b")
            self.play(FadeIn(hcs[1]))
            vo.wait_until("c")
            self.play(FadeIn(act))
        self.clear_scene()

    def one_guest(self):
        head = label(r"Hilbert's hotel: \ infinitely many rooms, \ every one full", font_size=30,
                     color=CONN).to_edge(UP, buff=0.5)
        rs, dots = rooms(y=0.6)
        gs = VGroup(*[guest(SETC).move_to(r[0]) for r in rs])
        new = guest(GOAL, "new").move_to([-5.4, 2.0, 0])
        rule = MathTex(r"n \ \mapsto\ n + 1", font_size=44, color=GOAL).move_to([0, -1.4, 0])
        cap = label(r"everyone moves one room up; \ room 1 is free", font_size=26, color=GREY_A).next_to(rule, DOWN,
                                                                                                    buff=0.3)
        with self.voiceover(
            "David Hilbert, in his lectures of the 1920s, put Galileo's paradox in a hotel. <bookmark mark='a'/>The "
            "hotel has infinitely many rooms, numbered one, two, three, and every room is taken. "
            "<bookmark mark='b'/>A new guest arrives. No problem: every guest moves from room n to room n plus one. "
            "<bookmark mark='c'/>Everyone still has a room, and room one is free. A full hotel has room for one more."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rs), FadeIn(dots), LaggedStart(*[FadeIn(g) for g in gs], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(new), Write(rule))
            self.play(*[g.animate.move_to(rs[i + 1][0]) for i, g in enumerate(gs[:-1])],
                      gs[-1].animate.shift(RIGHT * 1.2).set_opacity(0.3), run_time=1.6)
            vo.wait_until("c")
            self.play(new.animate.move_to(rs[0][0]), FadeIn(cap))
        self.clear_scene()

    def bus(self):
        head = label(r"A bus with infinitely many passengers", font_size=30, color=CONN).to_edge(UP, buff=0.5)
        rs, dots = rooms(y=0.6)
        gs = VGroup(*[guest(SETC).move_to(r[0]) for r in rs])
        bus = VGroup(*[guest(GOAL).move_to([-5.4 + 0.55 * i, 2.3, 0]) for i in range(10)])
        rule = MathTex(r"n \ \mapsto\ 2n", font_size=44, color=GOAL).move_to([0, -1.4, 0])
        cap = label(r"the old guests take the even rooms; \ the odd rooms, infinitely many, are free", font_size=26,
                    color=GREY_A).next_to(rule, DOWN, buff=0.3)
        odd = VGroup(*[SurroundingRectangle(rs[i][0], color=GOAL, buff=0.03) for i in (0, 2, 4, 6, 8)])
        with self.voiceover(
            "Now a bus arrives with infinitely many new guests. <bookmark mark='a'/>Move the guest in room n to room "
            "two n. <bookmark mark='b'/>The old guests fill the even rooms, and every odd room, infinitely many of "
            "them, is free for the bus. <bookmark mark='c'/>With more care, even infinitely many buses of "
            "infinitely many passengers fit, as the next chapter shows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rs), FadeIn(dots), FadeIn(gs), FadeIn(bus))
            vo.wait_until("a")
            self.play(Write(rule))
            moves = []
            for i, g in enumerate(gs):
                j = 2 * (i + 1) - 1
                if j < len(rs):
                    moves.append(g.animate.move_to(rs[j][0]))
                else:
                    moves.append(g.animate.move_to([7.8 + 0.4 * (j - len(rs)), g.get_y(), 0]))
            self.play(*moves, run_time=1.6)
            vo.wait_until("b")
            self.play(Create(odd), FadeIn(cap))
            self.play(*[bus[k].animate.move_to(rs[i][0]) for k, i in enumerate((0, 2, 4, 6, 8))],
                      *[bus[k].animate.set_opacity(0.3) for k in range(5, 10)], run_time=1.4)
        self.clear_scene()

    def dedekind(self):
        hcs = VGroup(history_card(1851, r"Bernard Bolzano", r"\textit{Paradoxes of the Infinite}", width=5.2,
                                  color=HIST),
                     history_card(1888, r"Richard Dedekind", r"\textit{Was sind und was sollen die Zahlen?}", width=6.4,
                                  color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        dc = definition_card(r"infinite (Dedekind)", r"a set is infinite if it can be matched one to one with a part "
                             r"of itself", width=9.0, font_size=26, color=P.CLAIM).move_to([0, 0.2, 0])
        sizes = definition_card(r"the same size (Cantor)", r"two sets have the same size \ (cardinality) \ if there is "
                                r"a bijection between them", width=9.0, font_size=26, color=GOAL).next_to(dc, DOWN,
                                                                                                    buff=0.4)
        moral = label(r"the paradox becomes the definition", font_size=28, color=OK).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Bernard Bolzano, in a book published after his death in 1851, insisted that such paradoxes are not "
            "contradictions. <bookmark mark='a'/>Richard Dedekind took the decisive step in 1888. What Galileo "
            "thought absurd, a part as large as the whole, he made the definition: a set is infinite exactly when "
            "it can be matched one to one with a part of itself. <bookmark mark='b'/>And Cantor's definition of "
            "size: two sets are the same size when there is a bijection, a perfect pairing, between them. "
            "<bookmark mark='c'/>The paradox became the definition, and the question changed. Not whether infinite "
            "sets can be compared, but whether all of them are the same size."
        ) as vo:
            self.play(FadeIn(hcs))
            vo.wait_until("a")
            self.play(FadeIn(dc))
            vo.wait_until("b")
            self.play(FadeIn(sizes))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()
