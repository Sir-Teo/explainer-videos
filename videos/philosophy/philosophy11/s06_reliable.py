from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Reliable(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Reliable processes", r"Is knowledge true belief from a good source?", lit=(1979,),
                            part=PART)
        with self.voiceover("Chapter five. Reliable processes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.goldman()
        self.generality()
        self.norman()

    def goldman(self):
        hc = history_card(1979, r"Alvin Goldman", r"`What Is Justified Belief?'", width=5.0,
                          color=HIST).to_corner(UL, buff=0.35)
        claim = label(r"a belief is justified \ iff \ it is produced by a reliable process", font_size=27,
                      color=GOAL).move_to([0, 1.6, 0])
        good = VGroup(label(r"reliable", font_size=24, color=OK),
                      label(r"perception, \ memory, \ sound reasoning", font_size=22)).arrange(DOWN, buff=0.12)
        bad = VGroup(label(r"unreliable", font_size=24, color=BAD),
                     label(r"wishful thinking, \ guessing, \ hasty generalization", font_size=22)).arrange(
            DOWN, buff=0.12)
        cols = VGroup(good, bad).arrange(RIGHT, buff=1.6).move_to([0, 0.3, 0])
        box = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.15, color=JUST).move_to([0, -1.6, 0])
        bl = label(r"a process", font_size=22, color=JUST).move_to(box)
        outs = VGroup(*[Dot(radius=0.08, color=OK if i % 10 else BAD) for i in range(1, 21)]).arrange_in_grid(
            rows=2, buff=0.12).next_to(box, RIGHT, buff=0.6)
        ins = Arrow(box.get_left() + LEFT * 1.4, box.get_left(), buff=0.05, color=GREY_B)
        outa = Arrow(box.get_right(), outs.get_left(), buff=0.1, color=GREY_B)
        rate = label(r"reliability: \ the proportion of true beliefs it yields \ (here 18 of 20)", font_size=21,
                     color=GREY_A).next_to(VGroup(box, outs), DOWN, buff=0.25)
        ext = label(r"externalism: \ the believer need not know the process is reliable", font_size=24,
                    color=KNOW).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A different idea came from Alvin Goldman. <bookmark mark='a'/>In his 1979 paper, What Is Justified "
            "Belief?, justification is a matter of where a belief comes from. A belief is justified if and only if "
            "it is produced by a reliable belief-forming process. <bookmark mark='b'/>Perception, memory and sound "
            "reasoning are reliable. Wishful thinking, guessing and hasty generalization are not. "
            "<bookmark mark='c'/>Think of a process as a machine that takes in stimuli and puts out beliefs. Its "
            "reliability is the proportion of true beliefs it puts out. <bookmark mark='d'/>This is externalism: what "
            "makes the belief justified may lie outside the believer's view. A child who trusts her eyes does not "
            "need a theory of vision. Animals, on this view, know things too."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(claim))
            vo.wait_until("b")
            self.play(FadeIn(cols))
            vo.wait_until("c")
            self.play(Create(box), FadeIn(bl), GrowArrow(ins))
            self.play(GrowArrow(outa), LaggedStart(*[FadeIn(d) for d in outs], lag_ratio=0.08), run_time=2)
            self.play(FadeIn(rate))
            vo.wait_until("d")
            self.play(FadeIn(ext))
        self.clear_scene()

    def generality(self):
        d = load("generality")
        head = label(r"The generality problem", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        sub = label(r"Henry's one look at the barn \ is a token of many process types", font_size=24,
                    color=GREY_A).next_to(head, DOWN, buff=0.25)
        types = d["types"]
        names = [label(t["type"], font_size=21, color=WHITE) for t in types]
        x0 = -6.4
        rows = VGroup()
        W = 4.0
        for i, (t, nm) in enumerate(zip(types, names)):
            y = 1.25 - i * 0.72
            nm.move_to([x0 + nm.width / 2, y, 0])
            bg = Rectangle(width=W, height=0.32, stroke_color=GREY_C, stroke_width=1).move_to([-1.2 + W / 2, y, 0])
            fill = Rectangle(width=max(W * t["rate"], 0.03), height=0.32, stroke_width=0,
                             fill_color=OK if t["rate"] > 0.5 else BAD, fill_opacity=0.85)
            fill.align_to(bg, LEFT).set_y(y)
            pct = label(rf"{t['true']:,}/{t['all']:,} \ = \ {100 * t['rate']:.0f}\%", font_size=20,
                        color=GREY_A).next_to(bg, RIGHT, buff=0.15)
            rows.add(VGroup(nm, bg, fill, pct))
        pop = label(rf"a toy population: \ {d['total'][1]:,} barn-judgments made from the road, \ "
                    rf"{d['total'][0]:,} of them true", font_size=20, color=GREY_B).next_to(rows, DOWN, buff=0.35)
        q = label(r"which type is \textit{the} process? \ the answer decides the verdict", font_size=25,
                  color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "But reliabilism has a problem as old as the theory. <bookmark mark='a'/>Reliability belongs to a type of "
            "process, while a belief is produced by a single token. And every token belongs to many types. "
            "<bookmark mark='b'/>The Reasoner builds a toy population of barn-judgments made from a car, in farmland "
            "and in Barn County, by day and at dusk, and computes the reliability of each type that Henry's look "
            "belongs to. Vision in general: about ninety-four percent. Vision in daylight: ninety-six. Vision from "
            "the road in Barn County: ten percent. In daylight in Barn County: still ten. And the narrowest type, "
            "this very look at this very barn: one for one, a hundred percent. <bookmark mark='c'/>So is Henry's "
            "belief justified? It depends on which type is the process, and the theory does not say. Earl Conee and "
            "Richard Feldman argued in 1998 that there is no principled way to choose. That is the generality problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sub))
            vo.wait_until("b")
            self.play(FadeIn(pop))
            for r in rows:
                self.play(FadeIn(r[0]), FadeIn(r[1]), GrowFromEdge(r[2], LEFT), FadeIn(r[3]), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.clear_scene()

    def norman(self):
        head = label(r"Reliable, \ but is it knowledge?", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        a = VGroup(label(r"Norman the clairvoyant", font_size=26, color=SKEP),
                   label(r"BonJour (1980)", font_size=20, color=GREY_B),
                   label(r"a reliable power he has no reason to believe in;", font_size=21),
                   label(r"one day he finds himself believing", font_size=21),
                   label(r"`the President is in New York'", font_size=21, color=BEL),
                   label(r"true, \ and reliably produced", font_size=21, color=OK),
                   label(r"but believing it seems irresponsible", font_size=21, color=BAD)).arrange(DOWN, buff=0.14)
        b = VGroup(label(r"Mr Truetemp", font_size=26, color=SKEP),
                   label(r"Lehrer (1990)", font_size=20, color=GREY_B),
                   label(r"a device in his head, \ unknown to him,", font_size=21),
                   label(r"makes him believe the exact temperature", font_size=21),
                   label(r"`it is 104 degrees'", font_size=21, color=BEL),
                   label(r"true, \ and reliably produced", font_size=21, color=OK),
                   label(r"but he has no idea why he believes it", font_size=21, color=BAD)).arrange(DOWN, buff=0.14)
        cols = VGroup(a, b).arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to([0, 0.2, 0])
        foot = label(r"the internalist's reply: \ justification needs reasons the believer can see \ (Chapter 15)",
                     font_size=23, color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The other objection comes from cases of reliability without reasons. <bookmark mark='a'/>Laurence "
            "BonJour imagined Norman, who is in fact a perfectly reliable clairvoyant about certain matters, but has "
            "no evidence for or against the existence of such a power. One day he finds himself believing that the "
            "President is in New York. The belief is true and reliably produced. But Norman holding it, against "
            "all he knows, seems irresponsible. <bookmark mark='b'/>Keith Lehrer's Mr Truetemp has a device implanted "
            "in his head, without his knowledge, which makes him believe the exact temperature. His beliefs are "
            "reliably true, but he has no idea why he holds them. <bookmark mark='c'/>To many, these show that "
            "reliability is not enough: justification needs reasons the believer can see. We return to this quarrel "
            "in chapter fifteen."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in a], lag_ratio=0.5), run_time=5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in b], lag_ratio=0.5), run_time=5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
