from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, WIRE, YES, load

BLOCK = [YES, HEAD, INF, NO, FUNC, CTRL]


def mod6(colors=None):
    pos = {str(r): (2.2 * np.cos(PI / 2 - 2 * PI * r / 6), 2.2 * np.sin(PI / 2 - 2 * PI * r / 6) - 0.2) for r in range(6)}
    edges = []
    for r in range(6):
        for b in (0, 1):
            t = (2 * r + b) % 6
            if t == r:
                edges.append((str(r), str(t), str(b), [UP, RIGHT, DOWN, DOWN, LEFT, UP][r]))
            else:
                edges.append((str(r), str(t), str(b), 0.35 if b else -0.35))
    sd = StateDiagram(pos, edges, radius=0.42, font_size=24, edge_font=18, accept=("0", "3"))
    return sd


class Nerode(VoiceoverScene):
    def construct(self):
        self.card()
        self.languages()
        self.theorem()
        self.refine()
        self.bridge()

    def card(self):
        card = chapter_card(7, r"Machines and languages", r"What is the smallest machine for a job?", lit=(1957, 1958, 1971),
                            part=PART)
        with self.voiceover("Chapter seven. Machines and languages."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def languages(self):
        head = label(r"A machine accepts a language", font_size=38).to_edge(UP, buff=0.35)
        sd = mod6().scale(0.85).move_to(LEFT * 4.3 + DOWN * 0.3)
        txt = VGroup(
            label(r"read a binary number, \ most significant bit first", font_size=26, color=GREY_A),
            MathTex(r"r \;\to\; 2r + b \pmod 6", font_size=36, color=CODE),
            label(r"accept if the number is divisible by 3: \ $r \in \{0, 3\}$", font_size=26, color=YES),
            label(r"six states: \ is that the fewest possible?", font_size=28, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.6 + UP * 0.2)
        with self.voiceover(
            "A state machine that only answers yes or no at the end of its input is called a finite automaton, and "
            "the set of inputs it says yes to is its language. <bookmark mark='a'/> Here is one for the binary numbers "
            "divisible by three, read from the most significant bit. Its state is the number read so far, modulo six: "
            "reading a bit b doubles the number and adds b. It accepts when the remainder is zero or three. "
            "<bookmark mark='b'/> It works, but it is wasteful. Is six states the fewest a machine for this language "
            "can have? A theorem from 1958 answers that question exactly, for every language at once."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sd.nodes), LaggedStart(*[Create(e) for e in sd.edges], lag_ratio=0.06), run_time=3.0)
            self.play(LaggedStart(*[FadeIn(t) for t in txt[:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(txt[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        head = label(r"The Myhill--Nerode theorem \ (1958)", font_size=38).to_edge(UP, buff=0.35)
        defn = VGroup(
            label(r"two prefixes $x$ and $y$ are \textit{equivalent} if no suffix tells them apart:", font_size=26,
                  color=GREY_A),
            MathTex(r"x \equiv_L y \iff \forall z: \ \big(xz \in L \Leftrightarrow yz \in L\big)", font_size=38,
                    color=CODE),
        ).arrange(DOWN, buff=0.22).move_to(UP * 2.25)
        thm = label(r"$L$ is recognized by a finite automaton \ $\iff$ \ $\equiv_L$ has finitely many classes, \\ and "
                    r"the smallest automaton has exactly one state per class", font_size=28, color=YES).move_to(UP * 0.85)
        pf = VGroup(
            label(r"why: \ any machine must send inequivalent prefixes to different states", font_size=24,
                  color=GREY_A),
            label(r"(if $x$ and $y$ reached one state, \ every suffix would treat them alike)", font_size=22,
                  color=GREY_B),
            label(r"and the classes themselves form a machine: \ reading $b$ sends the class of $x$ to the class of "
                  r"$xb$", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(thm, DOWN, buff=0.35)
        bins = VGroup()
        for rem, words, c in ((0, r"\varepsilon,\ 11,\ 110,\ 1001", BLOCK[0]), (1, r"1,\ 100,\ 111,\ 1010", BLOCK[1]),
                              (2, r"10,\ 101,\ 1000,\ 1011", BLOCK[2])):
            bx = RoundedRectangle(width=3.6, height=1.0, corner_radius=0.12, stroke_color=c, stroke_width=2.5,
                                  fill_color=c, fill_opacity=0.12)
            t = label(rf"remainder {rem}", font_size=20, color=c).next_to(bx.get_top(), DOWN, buff=0.1)
            w = MathTex(words, font_size=26, color=GREY_A).next_to(t, DOWN, buff=0.1)
            bins.add(VGroup(bx, t, w))
        bins.arrange(RIGHT, buff=0.35).move_to(DOWN * 2.15)
        ex = label(r"for multiples of 3: \ the classes are the remainders 0, 1, 2 \ $\Rightarrow$ \ 3 states", font_size=26,
                   color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "John Myhill and Anil Nerode looked at a language from the outside, with no machine at all. "
            "<bookmark mark='a'/> Call two prefixes equivalent if no continuation can tell them apart: for every "
            "suffix z, x z is in the language exactly when y z is. <bookmark mark='b'/> Their theorem says a language "
            "can be recognized by a finite automaton exactly when this equivalence has finitely many classes, and "
            "then the smallest automaton has one state per class, no more and no fewer. <bookmark mark='c'/> The "
            "proof is short. Any machine must send two inequivalent prefixes to different states, because if they "
            "reached the same state every suffix would treat them alike; so a machine has at least as many states as "
            "there are classes. And the classes themselves form a machine: reading a bit takes the class of x to the "
            "class of x followed by that bit. <bookmark mark='d'/> For multiples of three, two prefixes are "
            "equivalent exactly when they leave the same remainder mod three. Three classes, so three states suffice, "
            "and the six-state machine has three it does not need."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defn[0]), Write(defn[1]))
            vo.wait_until("b")
            self.play(FadeIn(thm))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in pf], lag_ratio=0.4), run_time=2.4)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bins], lag_ratio=0.3), FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def refine(self):
        d = load("nerode")
        rounds = d["rounds"]
        head = label(r"Minimizing: \ split until nothing splits", font_size=36).to_edge(UP, buff=0.35)
        sd = mod6().scale(0.85).move_to(LEFT * 4.3 + DOWN * 0.3)
        steps = VGroup(
            label(r"round 0: \ accepting $\{0, 3\}$ \ vs \ rejecting $\{1, 2, 4, 5\}$", font_size=23, color=GREY_A),
            label(r"round 1: \ from 1 and 4, \ reading 0 or 1 \\ leads to the same blocks; \\ from 2 and 5 too, "
                  r"\ but differently: \ split", font_size=23, color=GREY_A),
            label(r"round 2: \ nothing splits: \\ $\{0, 3\}, \ \{1, 4\}, \ \{2, 5\}$", font_size=25, color=YES),
            label(r"merge each block into one state: \\ 3 states, \ the Myhill--Nerode minimum", font_size=25,
                  color=HEAD),
            note(r"Moore's refinement: \ $O(n^2)$ in the worst case; \\ Hopcroft's (1971): \ $O(n \log n)$",
                 font_size=21),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.next_to(sd, RIGHT, buff=0.6)

        def paint(r):
            return [sd.node[str(s)].circle.animate.set_fill(BLOCK[r[s]], 0.45).set_stroke(BLOCK[r[s]])
                    for s in range(6)]

        with self.voiceover(
            "There is an algorithm that finds those classes in any machine. <bookmark mark='a'/> Start by splitting "
            "the states into two blocks: accepting and rejecting. No suffix can make those equivalent. "
            "<bookmark mark='b'/> Then look at each block and ask, for each input bit, which block each state goes "
            "to. States that disagree must be split, because some suffix tells them apart. Here states one and four "
            "behave alike, and so do two and five, but differently from one and four, so the rejecting block splits "
            "in two. <bookmark mark='c'/> Repeat until no block splits. The three blocks that remain, zero and three, "
            "one and four, two and five, are exactly the remainders mod three. <bookmark mark='d'/> Merge each block "
            "into a single state and you have the minimal machine. Edward Moore's method, used here, is simple; John "
            "Hopcroft's refinement of 1971 does the same in n log n time, and is what tools use to shrink the "
            "automata inside every regular-expression engine and lexer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd))
            vo.wait_until("a")
            self.play(*paint(rounds[0]), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(*paint(rounds[-1]), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]), FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bridge(self):
        head = label(r"The first rung of a ladder", font_size=38).to_edge(UP, buff=0.4)
        outer = RoundedRectangle(width=11.6, height=5.4, corner_radius=0.3, stroke_color=HEAD, stroke_width=2.5,
                                 fill_color=HEAD, fill_opacity=0.05).move_to(DOWN * 0.35)
        mid = RoundedRectangle(width=8.0, height=3.7, corner_radius=0.3, stroke_color=INF, stroke_width=2.5,
                               fill_color=INF, fill_opacity=0.07).align_to(outer, DL).shift(UP * 0.3 + RIGHT * 0.3)
        inner = RoundedRectangle(width=4.4, height=2.0, corner_radius=0.3, stroke_color=YES, stroke_width=2.5,
                                 fill_color=YES, fill_opacity=0.1).align_to(mid, DL).shift(UP * 0.3 + RIGHT * 0.3)
        tl = VGroup(
            label(r"Turing machines: \ plus an unbounded tape \ (Part 1)", font_size=22, color=HEAD)
            .next_to(outer.get_corner(UL), DR, buff=0.2),
            label(r"pushdown automata: \ plus a stack \ (Part 12)", font_size=22, color=INF)
            .next_to(mid.get_corner(UL), DR, buff=0.2),
            label(r"finite automata: \\ a fixed number of states \ (this part)", font_size=22, color=YES)
            .next_to(inner.get_corner(UL), DR, buff=0.2),
        )
        exs = VGroup(
            MathTex(r"\text{multiples of 3},\ (01)^*", font_size=26, color=YES).move_to(inner).shift(DOWN * 0.35),
            MathTex(r"0^n 1^n,\ \text{balanced brackets}", font_size=26, color=INF).move_to(mid.get_right())
            .shift(LEFT * 1.6 + DOWN * 0.3),
            MathTex(r"0^n 1^n 2^n", font_size=26, color=HEAD).move_to(outer.get_right()).shift(LEFT * 1.3 + DOWN * 0.5),
        )
        rungs = VGroup(VGroup(inner, tl[2], exs[0]), VGroup(mid, tl[1], exs[1]), VGroup(outer, tl[0], exs[2]))
        bars = VGroup()
        lim = label(r"no finite automaton recognizes $\{0^n 1^n\}$: \ $0^i$ and $0^j$ are never equivalent \ (Part 12)",
                    font_size=24, color=NO).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "This is the first rung of a ladder that the series climbs in Part 12. <bookmark mark='a'/> Finite "
            "automata, with a fixed amount of memory, recognize the regular languages: the patterns of regular "
            "expressions and of every lexer. Add a stack and you get the machines that parse programming languages. "
            "Add an unbounded tape and you are back at Part 1's Turing machine, which can do anything computable. "
            "<bookmark mark='b'/> Myhill–Nerode also marks the ladder's first edge. The language of some zeros "
            "followed by the same number of ones has infinitely many classes, since zero to the i and zero to the j "
            "are told apart by the suffix one to the i. So no finite machine, however clever, can recognize it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(DrawBorderThenFill(inner), FadeIn(tl[2]), FadeIn(exs[0]))
            self.play(DrawBorderThenFill(mid), FadeIn(tl[1]), FadeIn(exs[1]))
            self.play(DrawBorderThenFill(outer), FadeIn(tl[0]), FadeIn(exs[2]))
            self.bring_to_front(mid, inner, tl, exs)
            vo.wait_until("b")
            self.play(Indicate(exs[1], color=NO, scale_factor=1.25), FadeIn(lim))
        self.wait(0.3)
        self.clear_scene()
