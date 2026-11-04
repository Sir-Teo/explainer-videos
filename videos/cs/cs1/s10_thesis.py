from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, LIMIT, NO, PART, YES


class Thesis(VoiceoverScene):
    def construct(self):
        self.card()
        self.statement()
        self.evidence()
        self.not_say()
        self.versions()

    def card(self):
        card = chapter_card(9, r"The Church--Turing thesis", r"Is this what ``computable'' means?", lit=(1936,),
                            part=PART)
        with self.voiceover("Chapter nine. The Church-Turing thesis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def statement(self):
        left = node_box(r"computable by \\ \textit{any} mechanical procedure", HEAD, font_size=32)
        right = node_box(r"computable by \\ a Turing machine", CTRL, font_size=32)
        left.move_to(LEFT * 3.6 + UP * 0.6)
        right.move_to(RIGHT * 3.6 + UP * 0.6)
        eq = MathTex(r"=", font_size=90, color=GREY_A).move_to(UP * 0.6)
        tags = VGroup(label(r"informal: \ intuition", font_size=26, color=HEAD).next_to(left, DOWN, buff=0.3),
                      label(r"formal: \ mathematics", font_size=26, color=CTRL).next_to(right, DOWN, buff=0.3))
        thesis = definition_card(r"The Church--Turing thesis",
                                 r"Every function that can be computed by a mechanical procedure, \ in the informal sense "
                                 r"of Chapter 1, \ can be computed by a Turing machine.", color=HEAD, width=11.0,
                                 font_size=28, kind=r"Thesis").to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Church and Turing had each given a precise definition of computing. <bookmark mark='a'/> On one side, the "
            "intuitive idea from chapter one: what a clerk can do by following rules. On the other, a mathematical "
            "object: what a Turing machine can do. <bookmark mark='b'/> The Church-Turing thesis says they are the same. "
            "Anything that can be computed by any mechanical procedure at all can be computed by a Turing machine. "
            "<bookmark mark='c'/> Notice what kind of statement this is. It cannot be proved, because one side of the "
            "equals sign is not mathematics. It is a claim that a definition is the right one."
        ) as vo:
            self.play(FadeIn(left))
            vo.wait_until("a")
            self.play(FadeIn(right), FadeIn(tags))
            vo.wait_until("b")
            self.play(FadeIn(eq, scale=1.4), FadeIn(thesis, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(Indicate(tags[0], color=HEAD))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def evidence(self):
        head = label(r"Why believe it?", font_size=40).to_edge(UP, buff=0.4)
        pillars = VGroup(*[definition_card(t, b, color=c, width=4.2, font_size=26, kind=r"evidence") for t, b, c in (
            (r"they all agree", r"Turing machines, \ the $\lambda$-calculus, \ recursive functions, \ counter machines, "
                                r"\ cellular automata: \ independent ideas, \ the same functions", FUNC),
            (r"Turing's analysis", r"start from what a person computing actually does, \ and arrive at the machine",
             CTRL),
            (r"no counterexample", r"ninety years of programming languages, \ computers and proposals, \ and nothing "
                                   r"computes beyond it", YES),
        )]).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.4)
        quote = label(r"``\dots\ a precise and unquestionably adequate definition \\ of the general notion of formal "
                      r"system.''", font_size=28).to_edge(DOWN, buff=1.0)
        src = note(r"G\"odel, on Turing's work (postscript, 1964)", font_size=22).next_to(quote, DOWN, buff=0.15)
        with self.voiceover(
            "Three reasons. <bookmark mark='a'/> First, every attempt to define computation, made independently by "
            "different people with different intuitions, gives exactly the same set of functions. <bookmark mark='b'/> "
            "Second, Turing's analysis starts from what a person computing actually does, and arrives at his machine, "
            "step by step. That is what convinced Gödel, who had been sceptical of Church's version. <bookmark mark='c'/> "
            "Third, ninety years later, after every programming language and every computer ever built, nothing "
            "computes a single function a Turing machine cannot. <bookmark mark='d'/> Gödel called Turing's definition "
            "precise and unquestionably adequate."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abc", pillars):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(quote), FadeIn(src))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def not_say(self):
        head = label(r"What the thesis does \textit{not} say", font_size=40).to_edge(UP, buff=0.4)
        items = VGroup(*[VGroup(MathTex(r"\times", font_size=52, color=NO), label(t, font_size=34)).arrange(RIGHT, buff=0.35)
                         for t in (r"that every machine is fast: \ it is about \textit{whether}, \ not \textit{how soon}",
                                   r"that minds are Turing machines: \ it is about procedures, \ not about thought",
                                   r"that every \textit{physical} process can be simulated: \ that is a separate claim")])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to(DOWN * 0.2)
        with self.voiceover(
            "It is easy to read too much into it. <bookmark mark='a'/> It says nothing about speed: a Turing machine "
            "can compute what your laptop computes, only perhaps far more slowly. <bookmark mark='b'/> It says nothing "
            "about minds: it is a claim about procedures, which people can follow, not about everything people do. "
            "<bookmark mark='c'/> And it says nothing, by itself, about physics. Whether every physical process can be "
            "simulated by a Turing machine is a different question."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abc", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def versions(self):
        head = label(r"Three theses, \ in decreasing order of certainty", font_size=38).to_edge(UP, buff=0.4)
        rows = [
            (r"Church--Turing", r"every mechanical procedure \\ can be run by a Turing machine", r"almost universally \\ "
                                                                                                 r"accepted", YES),
            (r"physical", r"every physical process \\ can be simulated by a Turing machine", r"widely believed; \\ "
                                                                                           r"open", HEAD),
            (r"extended", r"every reasonable machine \\ can be simulated with \\ polynomial slowdown",
             r"challenged by \\ quantum computers", NO),
        ]
        tab = VGroup()
        for i, (n, c, st, col) in enumerate(rows):
            r = VGroup(label(n, font_size=30, color=col), label(c, font_size=26, color=GREY_A),
                       label(st, font_size=26, color=col))
            r[0].move_to([-4.9, 1.4 - i * 1.55, 0])
            r[1].move_to([-0.6, 1.4 - i * 1.55, 0])
            r[2].move_to([4.4, 1.4 - i * 1.55, 0])
            tab.add(r)
        lines = VGroup(*[Line([-6.5, 0.62 - i * 1.55, 0], [6.5, 0.62 - i * 1.55, 0], color=GREY_D) for i in range(2)])
        ptr = VGroup(label(r"Chapter 6: \ robustness, \ measured", font_size=22, color=GREY_B),
                     label(r"Part 26: \ the basis of complexity theory", font_size=22, color=GREY_B),
                     label(r"Part 53: \ Shor's algorithm, \ 1994", font_size=22, color=GREY_B))
        ptr.arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In fact there are three theses, and they get bolder. <bookmark mark='a'/> The Church-Turing thesis, about "
            "procedures, is almost universally accepted. <bookmark mark='b'/> The physical version says every physical "
            "process can be simulated by a Turing machine. Most physicists believe it, but it is an open claim about "
            "the universe. <bookmark mark='c'/> The extended version says more: that every reasonable machine can be "
            "simulated with at most a polynomial slowdown, like the quadratic cost of extra tapes we measured. It is the "
            "foundation of complexity theory. And it may be false. Quantum computers can factor large numbers in "
            "polynomial time by Shor's algorithm, and nobody knows how to do that on an ordinary machine. We will build "
            "one, simulated, in Part 53. <bookmark mark='d'/> What matters for now is that computable has become a "
            "precise word. And once a word is precise, you can prove things about everything it covers: including that "
            "some things are not computable at all."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15), *([Create(lines[0])] if mk == "b" else []),
                          *([Create(lines[1])] if mk == "c" else []))
            vo.wait_until("d")
            self.play(FadeIn(ptr))
        self.wait(0.3)
        self.clear_scene()
