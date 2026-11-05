from __future__ import annotations

import itertools

import numpy as np

from videos.philosophy.philosophy2.common import *  # noqa: F403

TT = list(itertools.product((True, False), repeat=2))


def nand(a, b):
    return not (a and b)


def gate(name: str, color=CONN, w=1.1, h=0.72) -> VGroup:
    body = RoundedRectangle(width=w, height=h, corner_radius=0.3, stroke_color=color, stroke_width=2.5,
                            fill_color="#0B0F17", fill_opacity=1)
    bubble = Circle(radius=0.08, stroke_color=color, stroke_width=2.5).next_to(body, RIGHT, buff=0)
    t = label(name, font_size=18, color=color).move_to(body)
    g = VGroup(body, bubble, t)
    g.inp = [body.get_left() + UP * h / 4, body.get_left() + DOWN * h / 4]
    g.out = bubble.get_right()
    return g


def wire(a, b, color=GREY_B) -> VMobject:
    mid = (a[0] + b[0]) / 2
    return VMobject(stroke_color=color, stroke_width=3).set_points_as_corners([a, [mid, a[1], 0], [mid, b[1], 0], b])


class Post(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Enough connectives", r"How few connectives can say everything?",
                            lit=(1880, 1913, 1941), part=PART)
        with self.voiceover("Chapter three. Enough connectives."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.dnf()
        self.sheffer()
        self.circuit()
        self.post()

    def dnf(self):
        rows = [[p, q, p != q] for p, q in TT]
        grid = ValueGrid([r"p", r"q", r"p \oplus q"], rows, col_w=1.1, cell_h=0.6, font_size=34)
        grid.move_to([-3.8, 0.3, 0])
        true_rows = [i for i, r in enumerate(rows) if r[2]]
        boxes = VGroup(*[grid.row_box(i, color=OK) for i in true_rows])
        conj = {1: r"p \land \lnot q", 2: r"\lnot p \land q"}
        ms = VGroup(*[MathTex(conj[i], font_size=38, color=OK).next_to(grid.rows_bg[i], RIGHT, buff=0.5)
                      for i in true_rows])
        dnf = MathTex(r"p \oplus q", r"\;\equiv\;", r"(p \land \lnot q)", r"\lor", r"(\lnot p \land q)", font_size=46)
        dnf[0].set_color(GOAL)
        dnf.move_to([1.4, -2.4, 0])
        check = TruthTable(["(p & ~q) | (~p & q)"], font_size=30).move_to([3.9, 0.6, 0])
        assert [v[-1] for v in check.values] == [r[2] for r in rows]
        thm = theorem_card(r"Disjunctive normal form", r"every truth function, of any number of inputs, is "
                           r"expressed by an `or' of `and's of atoms and their negations", width=6.2,
                           font_size=22).to_corner(UR, buff=0.35)
        with self.voiceover(
            "Every one of those truth functions can be written with just three connectives: not, and, or. The recipe "
            "reads the table row by row. <bookmark mark='a'/>Take exclusive or. It is true in two rows: p true and q "
            "false, or p false and q true. <bookmark mark='b'/>Describe each true row exactly with an 'and': p and not "
            "q; not p and q. <bookmark mark='c'/>Join the descriptions with 'or'. The result is true in exactly the "
            "true rows, <bookmark mark='d'/>as its own table confirms."
        ) as vo:
            self.play(FadeIn(grid))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[Write(m) for m in ms], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(TransformFromCopy(ms, VGroup(dnf[2], dnf[4])), FadeIn(dnf[0:2]), FadeIn(dnf[3]))
            vo.wait_until("d")
            self.play(FadeIn(check, shift=LEFT * 0.2))
        with self.voiceover(
            "The recipe works for any table with any number of inputs. If no row is true, write p and not p. "
            "<bookmark mark='a'/>So not, and, or are functionally complete: they can express every truth function "
            "there is. The form the recipe produces has a name, the disjunctive normal form, and it comes back in "
            "Chapter five."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(check), FadeIn(thm, shift=LEFT * 0.2))
        self.clear_scene()

    def sheffer(self):
        dm = MathTex(r"p \lor q", r"\;\equiv\;", r"\lnot(\lnot p \land \lnot q)", font_size=44).to_edge(UP, buff=0.5)
        dmw = label(r"De Morgan: `or' is not needed", font_size=24, color=GREY_A).next_to(dm, DOWN, buff=0.2)
        hc = history_card(1913, r"Henry Sheffer", r"one connective suffices: not both, `nand', \ $p \uparrow q$. "
                          r"(Peirce found it in 1880 and never published it.)", width=5.0, color=HIST)
        hc.to_corner(DL, buff=0.4)
        eqs = VGroup(MathTex(r"\lnot p", r"\;\equiv\;", r"p \uparrow p", font_size=42),
                     MathTex(r"p \land q", r"\;\equiv\;", r"(p \uparrow q) \uparrow (p \uparrow q)", font_size=42),
                     MathTex(r"p \lor q", r"\;\equiv\;", r"(p \uparrow p) \uparrow (q \uparrow q)", font_size=42))
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.6, -0.4, 0])
        for e in eqs:
            e[2].set_color(CONN)
        # computed check of the three identities on all four rows
        ok1 = all((not p) == nand(p, p) for p, q in TT)
        ok2 = all((p and q) == nand(nand(p, q), nand(p, q)) for p, q in TT)
        ok3 = all((p or q) == nand(nand(p, p), nand(q, q)) for p, q in TT)
        assert ok1 and ok2 and ok3
        ticks = VGroup(*[MathTex(r"\checkmark", font_size=36, color=OK).next_to(e, RIGHT, buff=0.3) for e in eqs])
        with self.voiceover(
            "Can we use fewer? <bookmark mark='a'/>De Morgan's law, p or q is the same as not both not p and not q, "
            "removes 'or': not and 'and' are enough. <bookmark mark='b'/>In 1913 Henry Sheffer showed that one "
            "connective is enough: 'not both', usually called nand and written with an up arrow. <bookmark mark='c'/>"
            "Not p is p nand p. <bookmark mark='d'/>p and q is the nand of p nand q with itself. <bookmark mark='e'/>"
            "And or is the nand of two negations. <bookmark mark='f'/>Each identity checks in all four rows. Charles "
            "Sanders Peirce had found this in 1880, in a manuscript nobody read for fifty years."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(dm), FadeIn(dmw))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            for k, mk in enumerate("cde"):
                vo.wait_until(mk)
                self.play(Write(eqs[k]))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(t, scale=1.4) for t in ticks], lag_ratio=0.25))
        self.clear_scene()

    def circuit(self):
        g1, g2, g3, g4 = gate(r"nand"), gate(r"nand"), gate(r"nand"), gate(r"nand")
        g1.move_to([-2.4, 0.0, 0])
        g2.move_to([0.0, 1.2, 0])
        g3.move_to([0.0, -1.2, 0])
        g4.move_to([2.4, 0.0, 0])
        for g in (g1, g2, g3, g4):
            g.inp = [g[0].get_left() + UP * 0.18, g[0].get_left() + DOWN * 0.18]
            g.out = g[1].get_right()
        A, B = np.array([-5.4, 1.6, 0]), np.array([-5.4, -1.6, 0])
        la = MathTex("a", font_size=40, color=ATOM).next_to(A, LEFT, buff=0.2)
        lb = MathTex("b", font_size=40, color=ATOM).next_to(B, LEFT, buff=0.2)
        wires = VGroup(wire(A, g1.inp[0]), wire(B, g1.inp[1]), wire(A + RIGHT * 1.6, g2.inp[0]),
                       wire(g1.out, g2.inp[1]), wire(g1.out, g3.inp[0]), wire(B + RIGHT * 1.9, g3.inp[1]),
                       wire(g2.out, g4.inp[0]), wire(g3.out, g4.inp[1]), Line(g4.out, g4.out + RIGHT * 1.4,
                                                                             color=GREY_B, stroke_width=3))
        rails = VGroup(Line(A, A + RIGHT * 1.6, color=GREY_B, stroke_width=3),
                       Line(B, B + RIGHT * 1.9, color=GREY_B, stroke_width=3))
        dots = VGroup(*[Dot(p, radius=0.06, color=GREY_B) for p in (A + RIGHT * 1.6, B + RIGHT * 1.9, g1.out)])
        out_l = MathTex(r"a \oplus b", font_size=36, color=GOAL).next_to(g4.out + RIGHT * 1.4, RIGHT, buff=0.15)
        circ = VGroup(wires, rails, dots, g1, g2, g3, g4, la, lb, out_l).shift(DOWN * 0.3)
        readout = VGroup()
        sweep = []
        for a, b in TT:
            x1 = nand(a, b)
            x2, x3 = nand(a, x1), nand(b, x1)
            y = nand(x2, x3)
            assert y == (a != b)
            sweep.append((a, b, x1, x2, x3, y))
        with self.voiceover(
            "This is why a computer can be built from one kind of part. <bookmark mark='a'/>Four nand gates, wired "
            "like this, compute exclusive or. <bookmark mark='b'/>Run all four inputs through it and the output is "
            "true exactly when the inputs differ. <bookmark mark='c'/>Adders, memories and processors can all be "
            "built from nand gates alone, and flash memory, NAND flash, is named after the way its cells are wired. "
            "Sheffer's truth function, found with pencil and paper, is in your pocket billions of times over."
        ) as vo:
            self.play(FadeIn(VGroup(g1, g2, g3, g4)), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(VGroup(wires, rails, dots, la, lb, out_l)), run_time=1.5)
            vo.wait_until("b")
            for a, b, x1, x2, x3, y in sweep:
                vals = VGroup(tv(a, 30).next_to(la, UP, buff=0.1), tv(b, 30).next_to(lb, DOWN, buff=0.1),
                              tv(x1, 26).next_to(g1, DOWN, buff=0.12), tv(x2, 26).next_to(g2, UP, buff=0.12),
                              tv(x3, 26).next_to(g3, DOWN, buff=0.12), tv(y, 36).next_to(out_l, UP, buff=0.15))
                cols = [OK if v else BAD for v in (x1, x2, x3, y)]
                anims = [FadeIn(vals)]
                if readout:
                    anims.insert(0, FadeOut(readout))
                anims += [g1[0].animate.set_stroke(cols[0]), g2[0].animate.set_stroke(cols[1]),
                          g3[0].animate.set_stroke(cols[2]), g4[0].animate.set_stroke(cols[3])]
                self.play(*anims, run_time=0.8)
                readout = vals
                self.wait(0.6)
            vo.wait_until("c")
        self.clear_scene()

    def post(self):
        d = load("post")
        cls_tex = [r"\text{keeps F}", r"\text{keeps T}", r"\text{self-dual}", r"\text{monotone}", r"\text{affine}"]
        conns = ["¬", "∧", "∨", "→", "↔", "⊕", "↑", "↓", "⊤", "⊥"]
        sym = {"¬": r"\lnot", "∧": r"\land", "∨": r"\lor", "→": r"\to", "↔": r"\leftrightarrow", "⊕": r"\oplus",
               "↑": r"\uparrow", "↓": r"\downarrow", "⊤": r"\top", "⊥": r"\bot"}
        rows = []
        for c in conns:
            m = d["member"][c]
            rows.append([MathTex(sym[c], font_size=30, color=CONN)] +
                        [MathTex(r"\bullet" if m[k] else r"\circ", font_size=30, color=GREY_A if m[k] else BAD)
                         for k in d["classes"]])
        grid = ValueGrid([r""] + cls_tex, rows, cell_h=0.42, font_size=26)
        grid.scale(0.9).to_edge(LEFT, buff=0.4).shift(DOWN * 0.2)
        thm = theorem_card(r"Post's criterion", r"a set of connectives is complete iff, for each of the five "
                           r"classes, it has a connective outside it ($\circ$)", who=r"Emil Post, 1941", width=6.0,
                           font_size=22).to_corner(UR, buff=0.35)
        sets = VGroup()
        for r in d["sets"]:
            s = r",\ ".join(sym[c] for c in r["set"])
            ok = r["complete"]
            nice = {"T0": "keeps F", "T1": "keeps T", "self-dual": "self-dual", "monotone": "monotone",
                    "affine": "affine"}
            right = r"\text{complete}" if ok else rf"\text{{stuck: {', '.join(nice[x] for x in r['stuck_in'])}}}"
            sets.add(MathTex(rf"\{{{s}\}}", r"\quad", right, font_size=26, color=OK if ok else BAD))
        sets.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(thm, DOWN, buff=0.3).align_to(thm, LEFT)
        mono = MathTex(r"\text{monotone: } \mathrm{F}\to\mathrm{T}\text{ in an input never makes the output } "
                       r"\mathrm{T}\to\mathrm{F}", font_size=28).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "But not every set is enough. And with or can never build not, however you combine them. "
            "<bookmark mark='a'/>In 1941 Emil Post found the exact test. There are five properties a connective can "
            "have: it keeps falsehood, mapping all false to false; it keeps truth; it is self-dual; it is monotone; or "
            "it is affine, a sum modulo two. <bookmark mark='b'/>Here is each connective, with a hollow circle where "
            "it lacks the property."
        ) as vo:
            self.play(FadeIn(grid.head), FadeIn(grid.rule), FadeIn(VGroup(*[grid.cell[i][0] for i in range(len(rows))])))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i][1:])) for i in range(len(rows))], lag_ratio=0.1),
                      run_time=2.5)
        with self.voiceover(
            "Each property survives composition. Take monotone: <bookmark mark='a'/>switching an input from false to "
            "true never switches the output from true to false. And and or are monotone, and anything wired from "
            "monotone parts is monotone too. Not isn't, so it can never be built. <bookmark mark='b'/>So a complete "
            "set needs, for each of the five properties, some connective that lacks it. Post proved that is also "
            "enough. <bookmark mark='c'/>Checking sets: not with and, complete; nand alone, complete; and with or, "
            "stuck in the monotone class; not with if-and-only-if, stuck among the affine ones; and if-then, even "
            "with and, or and if-and-only-if, stuck keeping truth, because every one of them is true when all its "
            "inputs are. We cross-checked each verdict by generating every function the set can build."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(mono))
            vo.wait_until("b")
            self.play(FadeIn(thm, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.1) for s in sets], lag_ratio=0.12), run_time=3)
        self.clear_scene()
