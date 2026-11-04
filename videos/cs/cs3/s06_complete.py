from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import CODE, COST, CTRL, DATA, HEAD, HIST, LIMIT, NO, PART, WIRE, YES, gate, load, wire


def inp(text, p):
    return MathTex(text, font_size=30, color=DATA).move_to(np.asarray(p) + LEFT * 0.35)


def dot(p):
    return Dot(np.asarray(p), radius=0.05, color=WIRE)


class Complete(VoiceoverScene):
    def construct(self):
        self.card()
        self.from_nand()
        self.xor4()
        self.dnf()
        self.post()

    def card(self):
        card = chapter_card(5, r"One gate is enough", r"Which gates can build every function?", part=PART)
        with self.voiceover("Chapter five. One gate is enough."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def from_nand(self):
        head = label(r"NOT, \ AND, \ OR, \ from NAND alone", font_size=38).to_edge(UP, buff=0.35)
        # NOT: tie the inputs
        g1 = gate("NAND", size=0.8).move_to(LEFT * 4.6 + UP * 0.8)
        x1 = g1.inp[0]() + LEFT * 0.6 + DOWN * 0.11
        not_c = VGroup(g1, wire(x1, g1.inp[0](), via="v"), wire(x1, g1.inp[1](), via="v"), dot(x1), inp("x", x1),
                       MathTex(r"\bar x", font_size=30, color=YES).next_to(g1.out(), RIGHT, buff=0.1))
        l1 = label(r"NOT: \ 1 gate", font_size=26, color=CTRL).next_to(not_c, DOWN, buff=0.5)
        # AND: NAND then NOT
        g2 = gate("NAND", size=0.8).move_to(LEFT * 1.3 + UP * 0.8)
        g3 = gate("NAND", size=0.8).move_to(LEFT * 0.0 + UP * 0.8)
        mid = g2.out()
        and_c = VGroup(g2, g3, wire(mid, g3.inp[0]()), wire(mid, g3.inp[1]()), dot(mid),
                       inp("x", g2.inp[0]()), inp("y", g2.inp[1]()),
                       MathTex(r"x y", font_size=30, color=YES).next_to(g3.out(), RIGHT, buff=0.1))
        l2 = label(r"AND: \ 2 gates", font_size=26, color=CTRL).next_to(and_c, DOWN, buff=0.5)
        # OR: invert each input, then NAND  (De Morgan)
        ga = gate("NAND", size=0.7).move_to(RIGHT * 2.6 + UP * 1.4)
        gb = gate("NAND", size=0.7).move_to(RIGHT * 2.6 + UP * 0.2)
        gc = gate("NAND", size=0.8).move_to(RIGHT * 4.4 + UP * 0.8)
        xa = ga.inp[0]() + LEFT * 0.4 + DOWN * 0.1
        xb = gb.inp[0]() + LEFT * 0.4 + DOWN * 0.1
        or_c = VGroup(ga, gb, gc, wire(xa, ga.inp[0](), via="v"), wire(xa, ga.inp[1](), via="v"),
                      wire(xb, gb.inp[0](), via="v"), wire(xb, gb.inp[1](), via="v"), dot(xa), dot(xb),
                      wire(ga.out(), gc.inp[0]()), wire(gb.out(), gc.inp[1]()), inp("x", xa), inp("y", xb),
                      MathTex(r"x + y", font_size=30, color=YES).next_to(gc.out(), RIGHT, buff=0.1))
        l3 = label(r"OR: \ 3 gates \ ($\overline{\bar x\, \bar y} = x + y$)", font_size=26, color=CTRL).next_to(
            or_c, DOWN, buff=0.4)
        d = load("nandmin")
        tab = VGroup()
        for r in d["rows"]:
            if r["name"] in ("x", "y"):
                continue
            tab.add(VGroup(label(r["name"].replace("=>", r"$\Rightarrow$").replace("NOT", r"\textsc{not}").replace(
                "AND", r"\textsc{and}"), font_size=20, color=GREY_A), MathTex(str(r["nands"]), font_size=24, color=COST)
            ).arrange(RIGHT, buff=0.15))
        tab.arrange_in_grid(rows=2, buff=(0.35, 0.18)).to_edge(DOWN, buff=0.45)
        tl = note(r"the fewest NANDs for each of the 16 two-input functions, \ found by exhaustive search", font_size=22)
        tl.next_to(tab, UP, buff=0.18)
        with self.voiceover(
            "Chapter four said a chip is mostly NAND gates. Could it be nothing but NAND gates? <bookmark mark='a'/> "
            "Not: join a NAND's two inputs together. x NAND x is not x. One gate. <bookmark mark='b'/> And: a NAND, "
            "then a not. Two gates. <bookmark mark='c'/> Or: invert both inputs, then NAND them. By De Morgan, not "
            "x NAND not y is x or y. Three gates. <bookmark mark='d'/> We searched every possible arrangement of NAND "
            "gates, for every one of the sixteen functions of two inputs. Not needs one, and needs two, or three, "
            "exclusive-or four, and the hardest, exclusive-nor, five."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(not_c), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(and_c), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(or_c), FadeIn(l3))
            vo.wait_until("d")
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(t) for t in tab], lag_ratio=0.06), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def xor4(self):
        head = label(r"Exclusive-or in four NANDs", font_size=38).to_edge(UP, buff=0.35)
        s = 1.0
        g1 = gate("NAND", size=s).move_to(LEFT * 2.2)
        g2 = gate("NAND", size=s).move_to(RIGHT * 0.4 + UP * 1.2)
        g3 = gate("NAND", size=s).move_to(RIGHT * 0.4 + DOWN * 1.2)
        g4 = gate("NAND", size=s).move_to(RIGHT * 3.0)
        xa = np.array([-5.0, 1.45, 0])
        xb = np.array([-5.0, -1.45, 0])
        ws = VGroup(
            wire(xa, g1.inp[0](), via="h"), wire(xb, g1.inp[1](), via="h"),
            Line(xa, [g2.inp[0]()[0], xa[1], 0], color=WIRE, stroke_width=3),
            wire([g2.inp[0]()[0], xa[1], 0], g2.inp[0](), via="v"),
            Line(xb, [g3.inp[1]()[0], xb[1], 0], color=WIRE, stroke_width=3),
            wire([g3.inp[1]()[0], xb[1], 0], g3.inp[1](), via="v"),
            wire(g1.out(), g2.inp[1]()), wire(g1.out(), g3.inp[0]()),
            wire(g2.out(), g4.inp[0]()), wire(g3.out(), g4.inp[1]()),
        )
        dots = VGroup(dot(g1.out() + RIGHT * 0.0), dot([(g1.out()[0] + g2.inp[1]()[0]) / 2, g1.out()[1], 0]))
        labels = VGroup(MathTex("x", font_size=34, color=DATA).next_to(xa, LEFT, buff=0.1),
                        MathTex("y", font_size=34, color=DATA).next_to(xb, LEFT, buff=0.1),
                        MathTex(r"x \oplus y", font_size=34, color=YES).next_to(g4.out(), RIGHT, buff=0.1),
                        MathTex(r"\overline{xy}", font_size=28, color=GREY_B).next_to(g1.out(), DOWN, buff=0.15))
        exp = MathTex(r"\overline{\overline{x\,\overline{xy}}\;\cdot\;\overline{y\,\overline{xy}}} = x \bar y + \bar x y",
                      font_size=36, color=CODE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is the four-gate exclusive-or, a small classic. <bookmark mark='a'/> The first gate computes not x "
            "and y. <bookmark mark='b'/> Each of the next two combines it with one input: the top one is zero only when "
            "x is one and y is not, the bottom one only when y is one and x is not. <bookmark mark='c'/> The last NAND "
            "is one when either of those is zero: exactly when the inputs differ. Sharing that first gate between both "
            "paths is what makes four enough."
        ) as vo:
            self.play(FadeIn(head), FadeIn(labels[:2]))
            vo.wait_until("a")
            self.play(Create(ws[0]), Create(ws[1]), FadeIn(g1), FadeIn(labels[3]))
            vo.wait_until("b")
            self.play(Create(VGroup(*ws[2:8])), FadeIn(g2), FadeIn(g3), FadeIn(dots))
            vo.wait_until("c")
            self.play(Create(VGroup(*ws[8:])), FadeIn(g4), FadeIn(labels[2]))
            self.play(Write(exp))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dnf(self):
        head = label(r"Any truth table, \ from AND, OR and NOT", font_size=38).to_edge(UP, buff=0.35)
        rows = [((0, 0, 0), 0), ((0, 0, 1), 1), ((0, 1, 0), 0), ((0, 1, 1), 1), ((1, 0, 0), 0), ((1, 0, 1), 0),
                ((1, 1, 0), 1), ((1, 1, 1), 0)]
        tab = VGroup()
        for i, ((a, b, c), f) in enumerate(rows):
            r = VGroup(*[MathTex(str(v), font_size=30, color=GREY_A) for v in (a, b, c)],
                       MathTex(str(f), font_size=30, color=YES if f else GREY_D))
            for j, m in enumerate(r):
                m.move_to([-5.4 + 0.7 * j, 1.6 - 0.5 * i, 0])
            tab.add(r)
        hdr = VGroup(*[MathTex(t, font_size=30, color=DATA) for t in ("a", "b", "c")],
                     MathTex("f", font_size=30, color=HEAD))
        for j, m in enumerate(hdr):
            m.move_to([-5.4 + 0.7 * j, 2.2, 0])
        terms = {1: r"\bar a \bar b c", 3: r"\bar a b c", 6: r"a b \bar c"}
        tms = VGroup()
        for i, t in terms.items():
            tms.add(MathTex(t, font_size=32, color=CTRL).next_to(tab[i], RIGHT, buff=0.6))
        f = MathTex(r"f = \bar a \bar b c + \bar a b c + a b \bar c", font_size=40, color=YES).move_to(RIGHT * 3.0 + UP * 1.0)
        steps = VGroup(label(r"each row where $f = 1$: \ an AND of the inputs, \ each plain or negated", font_size=24,
                             color=GREY_A),
                       label(r"OR them together: \ the \textit{disjunctive normal form}", font_size=24, color=GREY_A),
                       label(r"so AND, OR, NOT build anything; \\ and NAND builds all three: \ NAND is \textit{complete}",
                             font_size=28, color=HEAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(
            f, DOWN, buff=0.5)
        with self.voiceover(
            "Now the general argument. <bookmark mark='a'/> Take any truth table, here one with three inputs. "
            "<bookmark mark='b'/> For each row where the output is one, write an and of the inputs, each either plain "
            "or negated, so that it is true on that row and no other. <bookmark mark='c'/> Then or those terms "
            "together. The result is true on exactly the rows it should be. This is the disjunctive normal form, and "
            "it shows that and, or and not can build every function. <bookmark mark='d'/> Since NAND builds all three, "
            "NAND alone can build every function. It is complete. So is NOR, by the mirror argument."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(tab))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in tms], lag_ratio=0.3), FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(Write(f), FadeIn(steps[1]))
            vo.wait_until("d")
            self.play(FadeIn(steps[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def post(self):
        d = load("post")
        head = label(r"Post's test (1941): \ five ways to be trapped", font_size=36).to_edge(UP, buff=0.3)
        props = ["0-preserving", "1-preserving", "monotone", "self-dual", "affine"]
        short = [r"keeps 0", r"keeps 1", r"monotone", r"self-dual", r"affine"]
        show = ["AND", "OR", "XOR", "NOT x", "x => y", "NAND", "NOR"]
        rows = {r["name"]: r for r in d["rows"]}
        tab = VGroup()
        hdr = VGroup(*[label(s, font_size=22, color=GREY_B) for s in short])
        for j, h in enumerate(hdr):
            h.move_to([-2.4 + 1.45 * j, 2.15, 0])
        tab.add(hdr)
        for i, nm in enumerate(show):
            r = rows[nm]
            name = label(nm.replace("=>", r"$\Rightarrow$").replace("NOT", r"\textsc{not}"), font_size=26,
                         color=YES if r["complete"] else CTRL).move_to([-4.6, 1.55 - 0.52 * i, 0], aligned_edge=RIGHT)
            cells = VGroup(*[MathTex(r"\checkmark" if r[p] else r"\times", font_size=30,
                                     color=GREY_A if r[p] else NO).move_to([-2.4 + 1.45 * j, 1.55 - 0.52 * i, 0])
                             for j, p in enumerate(props)])
            tab.add(VGroup(name, cells))
        expl = VGroup(*[note(t, font_size=20) for t in (
            r"keeps 0: \ all-0 inputs give 0", r"keeps 1: \ all-1 inputs give 1",
            r"monotone: \ turning an input on never turns the output off",
            r"self-dual: \ flipping every input flips the output", r"affine: \ an XOR of inputs, plus a constant")]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(DL, buff=0.35)
        thm = theorem_card(r"Post (1941)", r"A set of gates is complete exactly when, for each of the five properties, "
                           r"at least one gate in the set lacks it.", width=5.4, font_size=21).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Which other sets of gates are complete? Emil Post answered that completely in 1941. <bookmark mark='a'/> "
            "There are exactly five ways for a set of gates to be trapped. If every gate keeps zero, giving zero on all "
            "zero inputs, then every circuit does too, and you can never build not. The same for keeping one. If every "
            "gate is monotone, circuits are monotone: and and or alone can never invert. If every gate is self-dual, or "
            "every gate is affine, an exclusive-or of its inputs plus a constant, circuits stay trapped there too. "
            "<bookmark mark='b'/> Here are some gates against the five properties. A cross means the gate escapes that "
            "trap. <bookmark mark='c'/> Post proved that escaping all five is also enough. A set is complete exactly "
            "when each trap is escaped by some gate in it. Among single two-input gates, only NAND and NOR escape all "
            "five."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(expl, lag_ratio=0.2), FadeIn(hdr))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.2), run_time=2.4)
            vo.wait_until("c")
            self.play(FadeIn(thm), *[Indicate(tab[1 + show.index(n)][0], color=YES) for n in ("NAND", "NOR")])
        self.wait(0.3)
        self.clear_scene()
