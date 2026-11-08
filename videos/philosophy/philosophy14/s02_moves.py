from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403

DET = {"b~m": r"\text{butler}", "bm": r"\text{both}", "~bm": r"\text{maid}", "~b~m": r"\text{neither}"}


class Moves(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Three ways to change", r"What can happen to a set of beliefs?", lit=(1985,),
                            part=PART)
        with self.voiceover("Chapter one. Three ways to change."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.detective()
        self.update_()
        self.recovery()

    def detective(self):
        d = load("moves")
        head = label(r"The detective's beliefs, \ as worlds", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sp = SphereView(d["rank"], center=[-3.4, -0.6, 0], step=1.0, names=DET, font_size=22,
                     angles={"b~m": PI, "bm": 0.0, "~bm": PI / 2, "~b~m": -PI / 2})
        legend = stack([(r"each dot: \ a way the case could be", GREY_A),
                        (r"inner disc: \ what she believes now", BEL),
                        (r"outer rings: \ less plausible, \ in order", SPH)], font_size=21,
                       aligned_edge=LEFT).move_to([3.4, 2.1, 0])
        ops = [
            ("expansion", r"$K + A$: \ add $A$, \ consistent with $K$", r"the maid has an alibi", d["expand ~m"]),
            ("revision", r"$K * A$: \ add $A$, \ even against $K$", r"the butler has an alibi", d["revise ~b"]),
            ("contraction", r"$K \div A$: \ stop believing $A$", r"doubt the butler's guilt", d["contract b"]),
        ]
        rows = VGroup()
        for name, form, story, res in ops:
            res_t = r",\ ".join(DET[w].replace(r"\text{", r"\text{").replace("}", "}") for w in res)
            rows.add(VGroup(label(name, font_size=24, color=NEW), label(form, font_size=21),
                            label(story, font_size=20, color=GREY_A),
                            MathTex(r"\to \{" + res_t + r"\}", font_size=24, color=BEL)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -1.3, 0])
        with self.voiceover(
            "A detective's case makes the three moves concrete. <bookmark mark='a'/>There are four ways the case could "
            "be: the butler did it, the maid did it, both did, or neither. <bookmark mark='b'/>The detective believes "
            "the butler did it, unsure about the maid: those worlds are in her inner disc. The other worlds lie on "
            "rings, in order of plausibility. <bookmark mark='c'/>Expansion adds a belief consistent with what she has: "
            "the maid has an alibi, and the disc shrinks to one world. <bookmark mark='d'/>Revision adds a belief that "
            "contradicts what she has: the butler has an alibi. She must give something up, and she moves to the most "
            "plausible world where he is innocent: the maid did it. <bookmark mark='e'/>Contraction removes a belief "
            "without adding its negation: she stops believing the butler did it, and admits the most plausible "
            "alternative, the maid, as a possibility."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sp.rings), FadeIn(sp.dots), FadeIn(sp.tags))
            vo.wait_until("b")
            self.play(FadeIn(legend))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), *sp.paint(d["expand ~m"], NEW), sp.dot["bm"].animate.set_opacity(0.3))
            vo.wait_until("d")
            self.play(sp.dot["bm"].animate.set_opacity(1), *sp.paint(d["beliefs"], WHITE))
            self.play(FadeIn(rows[1]), *sp.paint(d["revise ~b"], NEW), Indicate(sp.ring[1], color=NEW))
            vo.wait_until("e")
            self.play(*sp.paint(d["revise ~b"], WHITE))
            self.play(FadeIn(rows[2]), *sp.paint(d["contract b"], NEW))
        self.clear_scene()

    def update_(self):
        d = load("moves")["book"]
        hc = history_card(1991, r"Katsuno and Mendelzon", r"`On the difference between updating a knowledge base and "
                                                          r"revising it'", width=7.2, color=HIST).to_corner(UL,
                                                                                                         buff=0.35)
        setup = stack([(r"you believe: \ exactly one of the book and the magazine is on the floor", WHITE),
                       (r"news: \ the book is not on the floor", NEW)], font_size=24).next_to(hc, DOWN, buff=0.45)
        setup.set_x(0)
        names = {"b~m": r"\text{book}", "~bm": r"\text{magazine}", "~b~m": r"\text{neither}"}
        left = VGroup(label(r"revision: \ you \textit{learn} it", font_size=25, color=NEW),
                      label(r"you were wrong about the book", font_size=21, color=GREY_A),
                      MathTex(r"\to \{" + r",\ ".join(names[w] for w in d["revision"]) + r"\}", font_size=30,
                              color=BEL),
                      label(r"so the magazine is on the floor", font_size=22)).arrange(DOWN, buff=0.2).move_to(
            [-3.4, -1.3, 0])
        right = VGroup(label(r"update: \ a robot \textit{moves} the book", font_size=25, color=NEW),
                       label(r"the world changed; \ each possibility moves", font_size=21, color=GREY_A),
                       MathTex(r"\to \{" + r",\ ".join(names[w] for w in d["update"]) + r"\}", font_size=30,
                               color=BEL),
                       label(r"the magazine: \ still unknown", font_size=22)).arrange(DOWN, buff=0.2).move_to(
            [3.4, -1.3, 0])
        foot = label(r"update breaks AGM's vacuity postulate: \ not every change of mind is a revision", font_size=22,
                     color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Revision has a cousin that is easy to confuse with it. <bookmark mark='a'/>You believe that exactly one "
            "of the book and the magazine is on the floor. Now: the book is not on the floor. <bookmark mark='b'/>If "
            "you learn this, you were wrong about the book, and so the magazine must be the one on the floor. "
            "<bookmark mark='c'/>But if a robot has just picked the book up, the world has changed. Each possibility "
            "moves: the magazine is wherever it was, and you no longer know where that is. Hirofumi Katsuno and Alberto "
            "Mendelzon called the second operation update. <bookmark mark='d'/>The Reasoner confirms that update breaks "
            "one of the postulates of the next chapter. Not every change of mind is a revision."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(setup))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in left], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m) for m in right], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recovery(self):
        head = label(r"The recovery debate", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        post = MathTex(r"\text{recovery:}\quad K \subseteq (K \div A) + A", font_size=36, color=BEL).next_to(
            head, DOWN, buff=0.4)
        rows = stack([
            (r"you believe: \ Cleopatra had a son; \ so, \ she had a child", WHITE),
            (r"a historian casts doubt: \ contract `she had a child', \ and the son goes too", GREY_A),
            (r"then: \ she had a child after all", NEW),
            (r"recovery says: \ believe again that she had a son", BAD),
            (r"but the child might have been a daughter \ (Hansson, \ 1991)", GOAL),
            (r"for belief \textit{sets} recovery is automatic; \ for belief \textit{bases} it is a real choice", GREY_A),
        ], font_size=24, buff=0.28, width=12.4).next_to(post, DOWN, buff=0.45)
        with self.voiceover(
            "One postulate has divided the field. <bookmark mark='a'/>Recovery: if you give up A and then get A back, "
            "you have everything you started with. <bookmark mark='b'/>Sven Ove Hansson's example. You believe "
            "Cleopatra had a son, and so that she had a child. <bookmark mark='c'/>A historian casts doubt on the "
            "child, so you give that up, and the son goes with it. <bookmark mark='d'/>Then new evidence: she did have "
            "a child. <bookmark mark='e'/>Recovery says you must again believe she had a son. <bookmark mark='f'/>But "
            "the child might have been a daughter. <bookmark mark='g'/>For belief sets closed under logic, recovery "
            "comes for free; for the finite belief bases a machine actually stores, it is a real choice, and the "
            "theories of base revision reject it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(post))
            for mk, r in zip("bcdefg", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
