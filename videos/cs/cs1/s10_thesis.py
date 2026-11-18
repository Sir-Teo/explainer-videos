from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, LIMIT, NO, PART, YES


class Thesis(WatchScene):
    def construct(self):
        self.card()
        self.statement()
        self.evidence()
        self.not_say()

    def card(self):
        self.chapter(9, r"The Church--Turing thesis", r"Is this what ``computable'' means?", lit=(1936,), part=PART, said="Chapter nine. The Church-Turing thesis.")

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
        self.ask(r"The Church--Turing thesis says your laptop computes...",
                 [r"more than a Turing machine", r"the same functions", r"the same functions, just as fast"], 1,
                 say="What does the thesis say about the laptop you are watching on?",
                 reveal="The same functions as a Turing machine. Nothing about how fast.")
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

