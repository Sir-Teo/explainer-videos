from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import CODE, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, WIRE, YES, gate, wire


def venn(scale=1.0):
    r = 1.0 * scale
    X = Circle(r, stroke_color=DATA, stroke_width=3).shift(UP * 0.45 * scale)
    Y = Circle(r, stroke_color=CTRL, stroke_width=3).shift(DOWN * 0.4 * scale + LEFT * 0.55 * scale)
    Z = Circle(r, stroke_color=FUNC, stroke_width=3).shift(DOWN * 0.4 * scale + RIGHT * 0.55 * scale)
    lx = MathTex("x", font_size=32, color=DATA).move_to(X.get_center() + UP * 0.55 * scale)
    ly = MathTex("y", font_size=32, color=CTRL).move_to(Y.get_center() + LEFT * 0.5 * scale + DOWN * 0.2 * scale)
    lz = MathTex("z", font_size=32, color=FUNC).move_to(Z.get_center() + RIGHT * 0.5 * scale + DOWN * 0.2 * scale)
    return VGroup(X, Y, Z, lx, ly, lz)


class Boole(VoiceoverScene):
    def construct(self):
        self.card()
        self.laws_of_thought()
        self.syllogism()
        self.laws()
        self.distributive()
        self.proofs()

    def card(self):
        card = chapter_card(1, r"Boole's algebra", r"Can reasoning be done with equations?", lit=(1854,), part=PART)
        with self.voiceover("Chapter one. Boole's algebra."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def laws_of_thought(self):
        hc = history_card(1854, r"George Boole, \ Cork", r"\textit{An Investigation of the Laws of Thought}: \ logic "
                          r"written as algebra", width=6.4, font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(*[label(t, font_size=30, color=c) for t, c in (
            (r"a variable is a statement: \ its value is $1$ (true) or $0$ (false)", GREY_A),
            (r"$x\,y$: \ both \qquad $x + y$: \ either \qquad $\bar{x}$: \ not", CODE),
            (r"Boole's ``law of duality'': \ $x^2 = x$ \ \ (true and true is just true)", HEAD),
        )]).arrange(DOWN, buff=0.4).next_to(hc, DOWN, buff=0.6)
        note_ = note(r"engineers still write \textsc{and} as a product, \ \textsc{or} as a sum, \ \textsc{not} as a bar",
                     font_size=22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "George Boole was a self-taught schoolmaster who became a professor in Cork. In 1854 he published An "
            "Investigation of the Laws of Thought, and its idea was audacious: reasoning is a kind of algebra. "
            "<bookmark mark='a'/> A variable stands for a statement, and takes the value one for true or zero for false. "
            "<bookmark mark='b'/> Multiplication is and, addition is or, and a bar is not. <bookmark mark='c'/> His "
            "favourite law was x squared equals x: saying something twice is the same as saying it once, which is false "
            "for ordinary numbers but true for zero and one. Engineers still use his notation."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def syllogism(self):
        head = label(r"Boole's syllogisms, \ as equations", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup(*[VGroup(label(a, font_size=28, color=GREY_A), MathTex(b, font_size=36, color=c)).arrange(
            RIGHT, buff=0.6) for a, b, c in (
            (r"``every $x$ is a $y$''", r"x = x\,y", DATA),
            (r"``every $y$ is a $z$''", r"y = y\,z", DATA),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6).to_edge(LEFT, buff=1.2)
        chain = MathTex(r"x", r"= x y", r"= x (y z)", r"= (x y) z", r"= x z", font_size=42).next_to(rows, DOWN, buff=0.7)
        chain.align_to(rows, LEFT)
        chain[-1].set_color(YES)
        why = VGroup(note(r"substitute $y = yz$", font_size=22), note(r"associativity", font_size=22),
                     note(r"substitute $xy = x$", font_size=22))
        for k, (w, part) in enumerate(zip(why, chain[2:])):
            w.next_to(part, DOWN, buff=0.2 + 0.4 * (k % 2))
        concl = label(r"so: \ ``every $x$ is a $z$'' \ (Aristotle's \textit{Barbara})", font_size=30, color=HEAD)
        concl.next_to(chain, DOWN, buff=1.2).align_to(chain, LEFT)
        with self.voiceover(
            "Boole's own showpiece was the oldest piece of logic there is: Aristotle's syllogisms. "
            "<bookmark mark='a'/> Every x is a y becomes an equation: x equals x times y, since being an x and a y is "
            "the same as being an x. Every y is a z: y equals y z. <bookmark mark='b'/> Now calculate. x equals x y; "
            "substitute y z for y; regroup; substitute x for x y; and x equals x z. <bookmark mark='c'/> Every x is a "
            "z. Two thousand years of memorized rules for valid arguments became a few lines of algebra that a clerk, "
            "or a machine, could check."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows, lag_ratio=0.4))
            vo.wait_until("a")
            self.play(Circumscribe(rows[0], color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(chain[0]))
            for k in range(1, 5):
                self.play(FadeIn(chain[k], shift=RIGHT * 0.1), *([FadeIn(why[k - 2])] if k >= 2 else []), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def laws(self):
        head = label(r"The laws, \ in pairs", font_size=38).to_edge(UP, buff=0.35)
        pairs = [
            (r"identity", r"x \cdot 1 = x", r"x + 0 = x"),
            (r"annihilation", r"x \cdot 0 = 0", r"x + 1 = 1"),
            (r"idempotence", r"x \cdot x = x", r"x + x = x"),
            (r"complement", r"x \cdot \bar x = 0", r"x + \bar x = 1"),
            (r"commutativity", r"x y = y x", r"x + y = y + x"),
            (r"distributivity", r"x (y + z) = x y + x z", r"x + y z = (x + y)(x + z)"),
            (r"absorption", r"x (x + y) = x", r"x + x y = x"),
            (r"De Morgan", r"\overline{x y} = \bar x + \bar y", r"\overline{x + y} = \bar x\, \bar y"),
        ]
        rows = VGroup()
        for name, a, b in pairs:
            rows.add(VGroup(label(name, font_size=26, color=GREY_B), MathTex(a, font_size=34, color=DATA),
                            MathTex(b, font_size=34, color=CTRL)))
        for i, r in enumerate(rows):
            r[0].move_to([-4.6, 2.2 - 0.6 * i, 0], aligned_edge=LEFT).shift(LEFT * 1.2)
            r[1].move_to([-0.6, 2.2 - 0.6 * i, 0])
            r[2].move_to([3.6, 2.2 - 0.6 * i, 0])
        dual = label(r"swap $\cdot \leftrightarrow +$ \ and \ $0 \leftrightarrow 1$: \ every law turns into its partner "
                     r"(duality)", font_size=26, color=HEAD).to_edge(DOWN, buff=0.4)
        hl = SurroundingRectangle(rows[5][2], color=NO, buff=0.12)
        with self.voiceover(
            "Boole's algebra obeys a short list of laws, and they come in pairs. <bookmark mark='a'/> Identity, "
            "annihilation, idempotence, complement: each has a version for and and a version for or. "
            "<bookmark mark='b'/> Commutativity, distributivity, absorption, and De Morgan's laws from Part 2. "
            "<bookmark mark='c'/> Every law on the left turns into the one on the right if you swap and with or, and "
            "zero with one. That is the principle of duality, and in chapter four it will reappear in silicon. "
            "<bookmark mark='d'/> One law has no counterpart in ordinary arithmetic: or distributes over and. x plus y "
            "z equals x plus y, times x plus z. With numbers that is false. Here it is true."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows[:4]], lag_ratio=0.25))
            vo.wait_until("a")
            self.play(Circumscribe(rows[0], color=HEAD))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows[4:]], lag_ratio=0.25))
            vo.wait_until("c")
            self.play(FadeIn(dual))
            vo.wait_until("d")
            self.play(Create(hl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def distributive(self):
        head = label(r"$x + y z = (x + y)(x + z)$, \ drawn", font_size=38).to_edge(UP, buff=0.35)
        v1, v2 = venn(1.1).move_to(LEFT * 3.4 + DOWN * 0.3), venn(1.1).move_to(RIGHT * 3.4 + DOWN * 0.3)
        X1, Y1, Z1 = v1[0], v1[1], v1[2]
        X2, Y2, Z2 = v2[0], v2[1], v2[2]
        yz = Intersection(Y1, Z1, fill_color=HEAD, fill_opacity=0.6, stroke_width=0)
        x1 = X1.copy().set_fill(HEAD, 0.6).set_stroke(width=0)
        xy = Union(X2, Y2, fill_color=DATA, fill_opacity=0.25, stroke_width=0)
        xz = Union(X2, Z2, fill_color=FUNC, fill_opacity=0.25, stroke_width=0)
        both = Intersection(Union(X2, Y2), Union(X2, Z2), fill_color=HEAD, fill_opacity=0.6, stroke_width=0)
        t1 = MathTex(r"x + y z", font_size=40, color=HEAD).next_to(v1, DOWN, buff=0.35)
        t2 = MathTex(r"(x + y)(x + z)", font_size=40, color=HEAD).next_to(v2, DOWN, buff=0.35)
        eq = MathTex(r"=", font_size=60).move_to(DOWN * 0.3)
        with self.voiceover(
            "A picture makes it believable. Draw x, y and z as overlapping regions, true inside and false outside. "
            "<bookmark mark='a'/> On the left, y and z is the region inside both; add x, and you get everything in x, "
            "plus that lens. <bookmark mark='b'/> On the right, x or y is one big region, x or z another, and their "
            "and is where they overlap. <bookmark mark='c'/> The same shape. Every law can be checked like this, or by "
            "a truth table with eight rows, and that is the difference between Boole's algebra and ours: there are "
            "only finitely many cases, so every identity can be checked mechanically."
        ) as vo:
            self.play(FadeIn(head), FadeIn(v1), FadeIn(v2))
            vo.wait_until("a")
            self.play(FadeIn(yz))
            self.play(FadeIn(x1), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(xy))
            self.play(FadeIn(xz))
            self.play(FadeOut(xy), FadeOut(xz), FadeIn(both), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(eq, scale=1.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proofs(self):
        head = label(r"Proving with the laws", font_size=38).to_edge(UP, buff=0.35)
        steps = VGroup(*[MathTex(t, font_size=40, color=c) for t, c in (
            (r"x + x y", GREY_A),
            (r"= x \cdot 1 + x\, y", GREY_A),
            (r"= x\,(1 + y)", GREY_A),
            (r"= x \cdot 1", GREY_A),
            (r"= x", YES),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(LEFT * 3.0 + DOWN * 0.2)
        why = VGroup(*[note(t, font_size=24) for t in (r"identity", r"distributivity", r"annihilation", r"identity")])
        for w, s in zip(why, steps[1:]):
            w.next_to(s, RIGHT, buff=0.5)
        g_and = gate("AND", size=0.75).move_to(RIGHT * 2.4 + UP * 0.5)
        g_or = gate("OR", size=0.75).move_to(RIGHT * 4.2 + UP * 1.1)
        xp = np.array([1.0, 1.25, 0])
        yp = g_and.inp[1]() + LEFT * 0.5
        circ = VGroup(g_and, g_or, wire(xp, g_or.inp[0](), via="h"), wire(xp + RIGHT * 0.3, g_and.inp[0](), via="v"),
                      Line(xp, xp + RIGHT * 0.3, color=WIRE, stroke_width=3), wire(yp, g_and.inp[1]()),
                      wire(g_and.out(), g_or.inp[1]()), Dot(xp + RIGHT * 0.3, radius=0.05, color=WIRE),
                      MathTex("x", font_size=30, color=DATA).next_to(xp, LEFT, buff=0.1),
                      MathTex("y", font_size=30, color=DATA).next_to(yp, LEFT, buff=0.1),
                      MathTex("=", font_size=40).next_to(g_or, RIGHT, buff=0.5))
        plain = VGroup(Line(ORIGIN, RIGHT * 1.0, color=WIRE, stroke_width=3), MathTex("x", font_size=30, color=DATA))
        plain[1].next_to(plain[0], LEFT, buff=0.1)
        plain.next_to(circ[-1], RIGHT, buff=0.3)
        circ.add(plain)
        circ.move_to(RIGHT * 3.2 + UP * 0.8)
        use = label(r"simplifying an expression \\ $=$ removing gates", font_size=30, color=YES).next_to(circ, DOWN,
                                                                                                buff=0.7)
        with self.voiceover(
            "Laws let you simplify without truth tables. <bookmark mark='a'/> Absorption: x plus x y. Write x as x "
            "times one; factor out x; one plus anything is one; so the whole thing is x. <bookmark mark='b'/> As a "
            "circuit, an and gate and an or gate collapse into a plain wire. Every simplification of an expression "
            "removes gates from a circuit, and logic synthesis tools, which turn a hardware description into a chip, "
            "are at heart very fast, very clever users of these laws."
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            vo.wait_until("a")
            for s, w in zip(steps[1:], why):
                self.play(FadeIn(s, shift=DOWN * 0.1), FadeIn(w), run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(circ), FadeIn(use))
        self.wait(0.3)
        self.clear_scene()
