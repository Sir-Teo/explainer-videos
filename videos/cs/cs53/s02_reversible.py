from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono, tag_box


def wire_set(names, x0, x1, y0, gap, color=GREY_B, size=20):
    """Horizontal wires with a label at the left end of each; returns (wires, labels, ys)."""
    ys = [y0 - i * gap for i in range(len(names))]
    wires = VGroup(*[Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=2) for y in ys])
    labs = VGroup(*[label(n, font_size=size, color=GREY_A).next_to(w, LEFT, buff=0.15) for n, w in zip(names, wires)])
    return wires, labs, ys


def control(x, y, color=WHITE):
    return Dot([x, y, 0], radius=0.09, color=color)


def target(x, y, color=WHITE, r=0.2):
    c = Circle(radius=r, color=color, stroke_width=2.5).move_to([x, y, 0])
    return VGroup(c, Line([x - r, y, 0], [x + r, y, 0], color=color, stroke_width=2.5),
                  Line([x, y - r, 0], [x, y + r, 0], color=color, stroke_width=2.5))


def cross(x, y, color=WHITE, r=0.15):
    return VGroup(Line([x - r, y - r, 0], [x + r, y + r, 0], color=color, stroke_width=3),
                  Line([x - r, y + r, 0], [x + r, y - r, 0], color=color, stroke_width=3))


def perm_table(fn, hi, color, size=17):
    """The eight rows abc -> f(abc) of a three-bit gate, the rows in ``hi`` coloured."""
    rows = VGroup()
    for v in range(8):
        a, b, c = (v >> 2) & 1, (v >> 1) & 1, v & 1
        o = fn(a, b, c)
        col = color if v in hi else GREY_A
        rows.add(VGroup(mono(f"{a}{b}{c}", size=size, color=col), MathTex(r"\mapsto", font_size=26, color=GREY_B),
                        mono("".join(map(str, o)), size=size, color=col)).arrange(RIGHT, buff=0.25))
    rows.arrange(DOWN, buff=0.1)
    return rows


class Reversible(VoiceoverScene):
    def construct(self):
        self.card()
        self.forget()
        self.landauer()
        self.gates()
        self.bennett()
        self.bridge()

    def card(self):
        card = chapter_card(1, r"The cost of forgetting", r"Does computing have to cost energy?",
                            lit=(1961, 1973, 1982),
                            extra=((1961, r"Landauer: \ erasure costs $kT\ln 2$"),
                                   (1973, r"Bennett: \ reversible computation"),
                                   (1982, r"Fredkin and Toffoli: \ conservative logic")), part=PART)
        with self.voiceover("Chapter one. The cost of forgetting. Does computing have to cost energy?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def forget(self):
        head = label(r"An AND gate forgets", font_size=36).to_edge(UP, buff=0.3)
        ins = VGroup(*[tag_box(s, DATA, size=20, w=0.9) for s in ("00", "01", "10", "11")]).arrange(DOWN, buff=0.35)
        outs = VGroup(tag_box("0", NO, size=20, w=0.9), tag_box("1", YES, size=20, w=0.9)).arrange(DOWN, buff=1.4)
        ins.move_to([-5.2, 0.2, 0])
        outs.move_to([-2.6, 0.2, 0])
        arrows = VGroup(*[Arrow(ins[i].get_right(), outs[0 if i < 3 else 1].get_left(), buff=0.08, stroke_width=2.5,
                                color=NO if i < 3 else YES, max_tip_length_to_length_ratio=0.1) for i in range(4)])
        cap_l = wrapped_label(r"four states in, \ two out: \ from a 0 you cannot tell which of three inputs it "
                              r"was", 4.8, font_size=19, color=GREY_A).next_to(VGroup(ins, outs), DOWN, buff=0.4)
        # a one-molecule memory: the molecule in the left half is 0, in the right half 1
        W, Hh = 3.6, 1.7
        cx, cy = 3.2, 0.55
        box = Rectangle(width=W, height=Hh, color=GREY_B, stroke_width=2.5).move_to([cx, cy, 0])
        wall = DashedLine([cx, cy - Hh / 2, 0], [cx, cy + Hh / 2, 0], color=GREY_B, dash_length=0.1)
        mol = Dot([cx + 0.9, cy + 0.2, 0], radius=0.11, color=HEAD)
        tags = VGroup(label(r"0", font_size=24, color=DATA).next_to(box, UP, buff=0.12).shift(LEFT * W / 4),
                      label(r"1", font_size=24, color=DATA).next_to(box, UP, buff=0.12).shift(RIGHT * W / 4))
        piston = Rectangle(width=0.14, height=Hh - 0.06, stroke_width=0, fill_color=KERN,
                           fill_opacity=1).move_to([cx + W / 2 - 0.1, cy, 0])
        cap_r = wrapped_label(r"erase: \ remove the wall, \ push the piston to the middle, \ restore the wall; \ the "
                              r"memory reads 0 whatever it held", 5.6, font_size=19, color=WHITE).next_to(
            box, DOWN, buff=0.4)
        heat = wrapped_label(r"the memory's two possible states became one; \ the lost uncertainty leaves as heat in "
                             r"the surroundings", 5.6, font_size=19, color=KERN).next_to(cap_r, DOWN, buff=0.25)
        ill = note(r"illustrative: \ a one-molecule memory", font_size=16).to_edge(DOWN, buff=0.3).set_x(cx)
        with self.voiceover(
            "Most of the logic we built in Part 3 throws information away. <bookmark mark='a'/> An AND gate takes "
            "four possible inputs to two possible outputs. Three different inputs all give a zero, and once you see "
            "the zero you cannot say which of them it was. <bookmark mark='b'/> Is that forgetting free? Picture the "
            "simplest memory there is: one molecule in a box, with a wall in the middle. Left means zero, right "
            "means one. <bookmark mark='c'/> To erase the bit, setting it to zero whatever it held, pull out the "
            "wall, push a piston to the middle, and put the wall back. <bookmark mark='d'/> Two possible states have "
            "become one. The physics says that lost uncertainty cannot vanish: it ends up in the surroundings, as "
            "heat."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ins), FadeIn(outs))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), FadeIn(cap_l))
            vo.wait_until("b")
            self.play(Create(box), Create(wall), FadeIn(tags), FadeIn(mol), FadeIn(ill))
            vo.wait_until("c")
            self.play(FadeOut(wall), FadeIn(piston), FadeIn(cap_r))
            for p in ([cx - 1.1, cy - 0.4, 0], [cx + 0.5, cy + 0.5, 0], [cx - 0.4, cy - 0.3, 0]):
                self.play(mol.animate.move_to(p), run_time=0.35)
            self.play(piston.animate.move_to([cx + 0.08, cy, 0]), mol.animate.move_to([cx - 0.8, cy + 0.1, 0]),
                      run_time=1.4)
            wall2 = DashedLine([cx, cy - Hh / 2, 0], [cx, cy + Hh / 2, 0], color=GREY_B, dash_length=0.1)
            self.play(FadeOut(piston), Create(wall2), tags[0].animate.set_color(HEAD))
            vo.wait_until("d")
            self.play(FadeIn(heat))
        self.wait(0.4)
        self.clear_scene()

    def landauer(self):
        d = load("landauer")
        head = label(r"Landauer's principle", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"\text{states: } 2", r"\to", r"1", font_size=34),
            MathTex(r"\Delta S", r"=", r"k", r"\ln 2", font_size=34),
            MathTex(r"Q", r"\ge", r"T", r"\Delta S", r"=", r"k", r"T", r"\ln 2", font_size=34),
            MathTex(r"Q", r"\ge", r"(1.38 \times 10^{-23}\,\mathrm{J/K})", r"\times", rf"{d['T']:.0f}\,\mathrm{{K}}",
                    r"\times", r"\ln 2", font_size=32),
            MathTex(r"Q", r"\ge", rf"{d['joules'] * 1e21:.2f} \times 10^{{-21}}\,\mathrm{{J}}", r"\approx",
                    rf"{d['electronvolts']:.3f}\,\mathrm{{eV}}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.62).move_to([-2.4, 0.0, 0])
        whys = VGroup(
            label(r"erasing a random bit halves the memory's possible states", font_size=18, color=GREY_B),
            label(r"its entropy falls by $k \ln 2$ \ ($k$: Boltzmann's constant)", font_size=18, color=GREY_B),
            label(r"the second law: \ the surroundings must gain at least that, \ as heat", font_size=18,
                  color=GREY_B),
            label(r"at room temperature", font_size=18, color=GREY_B),
            label(r"the least heat per erased bit", font_size=18, color=HEAD),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        side = VGroup(
            wrapped_label(rf"$10^{{18}}$ erasures a second at this limit: \ about "
                          rf"{d['per_1e18_erasures_W'] * 1e3:.1f} milliwatts", 3.6, font_size=19, color=KERN),
            wrapped_label(r"today's transistors dissipate far more than this per switch: \ the limit is a floor, "
                          r"\ not yet the ceiling", 3.6, font_size=19, color=GREY_A),
            wrapped_label(r"measured: \ B\'erut et al., \ \textit{Nature} 2012, \ a bead in a two-well optical "
                          r"trap", 3.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.7, 0.0, 0])
        with self.voiceover(
            "In 1961 Rolf Landauer, at IBM, put a number on it. <bookmark mark='a'/> Erasing a bit whose value is "
            "unknown takes the memory from two possible states to one. <bookmark mark='b'/> Its entropy falls by "
            "Boltzmann's constant times the logarithm of two. <bookmark mark='c'/> The second law of thermodynamics "
            "says the total cannot fall, so at least that much entropy must reach the surroundings, carried by heat: "
            "at least k T log two. <bookmark mark='d'/> At room temperature, three hundred kelvin, <bookmark "
            "mark='e'/> that is about three times ten to the minus twenty-one joules, or eighteen thousandths of an "
            "electronvolt, per bit. <bookmark mark='f'/> A billion billion erasures a second at this limit would "
            "cost about three milliwatts. Real transistors spend far more than this per switch. In 2012 a team in "
            "Lyon measured it, with a glass bead in a two-well laser trap."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[3].copy(), rows[4]), FadeIn(whys[4]))
            self.play(Circumscribe(rows[4], color=HEAD))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.15) for s in side], lag_ratio=0.5), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def gates(self):
        head = label(r"Gates that forget nothing", font_size=36).to_edge(UP, buff=0.3)

        def panel(kind, cx):
            wires, labs, ys = wire_set([r"$a$", r"$b$", r"$c$"], cx - 1.0, cx + 1.0, 2.3, 0.5)
            x = cx
            if kind == "toffoli":
                sym = VGroup(Line([x, ys[0], 0], [x, ys[2] - 0.2, 0], color=WHITE, stroke_width=2.5),
                             control(x, ys[0]), control(x, ys[1]), target(x, ys[2]))
                outs = [r"$a$", r"$b$", r"$c \oplus ab$"]
            else:
                sym = VGroup(Line([x, ys[0], 0], [x, ys[2], 0], color=WHITE, stroke_width=2.5),
                             control(x, ys[0]), cross(x, ys[1]), cross(x, ys[2]))
                outs = [r"$a$", r"$b$ or $c$", r"$c$ or $b$"]
            ol = VGroup(*[label(o, font_size=18, color=GREY_A).next_to(w, RIGHT, buff=0.15)
                          for o, w in zip(outs, wires)])
            return VGroup(wires, labs, sym, ol)
        tof = panel("toffoli", 0)
        fre = panel("fredkin", 0)
        t_name = label(r"Toffoli: \ flip $c$ if $a$ and $b$", font_size=21, color=HEAD)
        f_name = label(r"Fredkin: \ swap $b, c$ if $a$", font_size=21, color=LAM)
        t_tab = perm_table(lambda a, b, c: (a, b, c ^ (a & b)), (6, 7), HEAD)
        f_tab = perm_table(lambda a, b, c: (a, c, b) if a else (a, b, c), (5, 6), LAM)
        t_grp = VGroup(t_name, VGroup(tof, t_tab).arrange(RIGHT, buff=0.5)).arrange(DOWN, buff=0.3)
        f_grp = VGroup(f_name, VGroup(fre, f_tab).arrange(RIGHT, buff=0.5)).arrange(DOWN, buff=0.3)
        pair = VGroup(t_grp, f_grp).arrange(RIGHT, buff=0.9, aligned_edge=UP)
        pair.scale_to_fit_width(min(12.6, pair.width * 1.3)).next_to(head, DOWN, buff=0.35)
        notes = VGroup(
            wrapped_label(r"each is a \textbf{permutation} of the eight states: \ nothing merges, \ so nothing is "
                          r"lost, \ and running it twice undoes it", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"with $c = 0$ \ Toffoli writes $a$ AND $b$; \ with constant inputs either gate builds "
                          r"any Boolean circuit; \ Fredkin also conserves the number of 1s", 12.4, font_size=19,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The way out is to compute without merging states. <bookmark mark='a'/> Tommaso Toffoli's gate takes "
            "three bits and flips the third only if the first two are both one. <bookmark mark='b'/> Its table moves "
            "only two of the eight rows, swapping them: it is a permutation, so no two inputs share an output, "
            "nothing is lost, and applying it twice gives back the input. <bookmark mark='c'/> Edward Fredkin's gate "
            "swaps the second and third bits when the first is one; it even conserves the number of ones, like "
            "billiard balls. <bookmark mark='d'/> Neither throws anything away, and yet, with the third input set to "
            "zero, Toffoli's gate writes a AND b. Given constant inputs, either gate can build any Boolean circuit "
            "at all. Logic does not need to forget."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t_name), Create(tof[0]), FadeIn(tof[1]), FadeIn(tof[2]), FadeIn(tof[3]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in t_tab], lag_ratio=0.12), run_time=1.6)
            self.play(Indicate(VGroup(t_tab[6], t_tab[7]), color=HEAD))
            vo.wait_until("c")
            self.play(FadeIn(f_name), Create(fre[0]), FadeIn(fre[1]), FadeIn(fre[2]), FadeIn(fre[3]))
            self.play(LaggedStart(*[FadeIn(r) for r in f_tab], lag_ratio=0.12), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def bennett(self):
        head = label(r"Bennett: \ compute, \ copy, \ uncompute", font_size=36).to_edge(UP, buff=0.3)
        wires, labs, ys = wire_set([r"input", r"work", r"output"], -5.6, 5.6, 1.8, 1.0, size=21)
        def gate_box(x, y0, y1, tex, color):
            r = Rectangle(width=1.5, height=abs(y0 - y1) + 0.6, stroke_color=color, stroke_width=2.5, fill_color=BG,
                          fill_opacity=1).move_to([x, (y0 + y1) / 2, 0])
            return VGroup(r, MathTex(tex, font_size=34, color=color).move_to(r))
        comp = gate_box(-3.0, ys[0], ys[1], r"C", DATA)
        copy = VGroup(Line([0, ys[1], 0], [0, ys[2] - 0.2, 0], color=WHITE, stroke_width=2.5), control(0, ys[1]),
                      target(0, ys[2]))
        unc = gate_box(3.0, ys[0], ys[1], r"C^{-1}", LAM)
        stage_tex = [
            (r"(", r"x", r",\;", r"0", r",\;", r"0", r")"),
            (r"(", r"x", r",\;", r"f(x)\,g(x)", r",\;", r"0", r")"),
            (r"(", r"x", r",\;", r"f(x)\,g(x)", r",\;", r"f(x)", r")"),
            (r"(", r"x", r",\;", r"0", r",\;", r"f(x)", r")"),
        ]
        xs = [-4.65, -1.5, 1.5, 4.65]
        stages = [MathTex(*s, font_size=26, color=WHITE).move_to([x, -1.05, 0]) for s, x in zip(stage_tex, xs)]
        stages[1].set_color_by_tex(r"f(x)\,g(x)", DATA)
        stages[2].set_color_by_tex(r"f(x)\,g(x)", DATA)
        stages[2][5].set_color(YES)
        stages[3][5].set_color(YES)
        cursor = DashedLine([-4.65, 2.35, 0], [-4.65, -0.7, 0], color=HEAD, dash_length=0.08)
        notes = VGroup(
            wrapped_label(r"the garbage $g(x)$ is never erased: \ it is \textbf{uncomputed}, \ run backwards to "
                          r"zero, \ so no $kT \ln 2$ is owed (Bennett, \ 1973)", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"the price: \ about twice the steps, \ and room for the garbage meanwhile \ (Bennett "
                          r"traded the two off in 1989)", 12.4, font_size=19, color=GREY_A),
            wrapped_label(r"every quantum oracle in chapters 5 to 10 is built this way: \ leftover garbage would "
                          r"stay entangled with the answer and spoil the interference", 12.4, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Charles Bennett, also at IBM, showed in 1973 that any computation can be done reversibly. <bookmark "
            "mark='a'/> Give the circuit three registers: the input, a work area of zeros, and an output of zeros. "
            "<bookmark mark='b'/> First compute, reversibly: the work area now holds the answer, f of x, and a pile "
            "of intermediate garbage. <bookmark mark='c'/> Then copy the answer into the output, with "
            "controlled-NOTs, which is reversible too. <bookmark mark='d'/> Finally run the first circuit backwards. "
            "It turns the work area back into zeros, garbage and all. Nothing was ever erased, so no heat is owed. "
            "<bookmark mark='e'/> The price is about twice the steps, and space for the garbage in between. And this "
            "trick returns in every quantum algorithm in this part: garbage left behind would stay entangled with "
            "the answer and spoil the interference."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(wires), FadeIn(labs), Create(cursor), FadeIn(stages[0]))
            vo.wait_until("b")
            self.play(FadeIn(comp), cursor.animate.set_x(-1.5), TransformMatchingTex(stages[0].copy(), stages[1]))
            vo.wait_until("c")
            self.play(FadeIn(copy), cursor.animate.set_x(1.5), TransformMatchingTex(stages[1].copy(), stages[2]))
            vo.wait_until("d")
            self.play(FadeIn(unc), cursor.animate.set_x(4.65), TransformMatchingTex(stages[2].copy(), stages[3]))
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def bridge(self):
        head = label(r"From permutations to rotations", font_size=36).to_edge(UP, buff=0.3)
        n = 8
        cell = 0.27
        grid = VGroup()
        for r in range(n):
            for c in range(n):
                tgt = {6: 7, 7: 6}.get(c, c)
                on = r == tgt
                grid.add(Square(side_length=cell, stroke_color=GREY_D, stroke_width=1,
                                fill_color=(HEAD if c in (6, 7) else DATA) if on else BG, fill_opacity=1))
        grid.arrange_in_grid(rows=n, cols=n, buff=0)
        left = VGroup(grid, label(r"Toffoli: \ an $8 \times 8$ permutation matrix", font_size=19,
                                  color=GREY_A)).arrange(DOWN, buff=0.2)
        xm = MathTex(r"X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}", font_size=34, color=DATA)
        hm = MathTex(r"H = \tfrac{1}{\sqrt 2}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}", font_size=34, color=YES)
        mid = VGroup(xm, label(r"NOT: \ a permutation", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.2)
        right = VGroup(hm, label(r"a unitary that is not one", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.2)
        arr = MathTex(r"\longrightarrow", font_size=40, color=GREY_B)
        top = VGroup(left, mid, arr, right).arrange(RIGHT, buff=0.6)
        top.scale_to_fit_width(min(12.6, top.width * 1.15)).next_to(head, DOWN, buff=0.4)
        rule = wrapped_label(r"permutation matrices are exactly the unitary matrices with entries 0 and 1: \ "
                             r"quantum gates keep reversibility and allow every unitary", 12.0, font_size=20,
                             color=WHITE).next_to(top, DOWN, buff=0.35)

        def tile(year, text, col):
            fr = RoundedRectangle(width=4.0, height=1.35, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                  fill_color=BG, fill_opacity=1)
            g = VGroup(label(year, font_size=22, color=col), wrapped_label(text, 3.7, font_size=18, color=GREY_A))
            g.arrange(DOWN, buff=0.12).move_to(fr)
            return VGroup(fr, g)
        tiles = VGroup(tile(r"1980", r"Benioff: \ a Turing machine as a quantum-mechanical system", DATA),
                       tile(r"1982", r"Feynman: \ simulate physics with a computer made of quantum parts", HEAD),
                       tile(r"1985", r"Deutsch: \ the universal quantum computer", YES)).arrange(RIGHT, buff=0.25)
        tiles.next_to(rule, DOWN, buff=0.35)
        with self.voiceover(
            "Now write a reversible gate as a matrix acting on its basis states. <bookmark mark='a'/> Toffoli's gate "
            "becomes an eight by eight matrix with a single one in every row and column: a permutation. <bookmark "
            "mark='b'/> The NOT gate is the smallest. <bookmark mark='c'/> Permutation matrices are exactly the "
            "unitary matrices whose entries are zeros and ones. Allow any unitary, like this one, and the "
            "computation stays reversible but is no longer a shuffle of states: it is a rotation. <bookmark "
            "mark='d'/> That step was taken in three papers. In 1980 Paul Benioff described a Turing machine as a "
            "quantum-mechanical system. In 1982 Feynman proposed simulating physics with a computer made of quantum "
            "parts. And in 1985 David Deutsch defined the universal quantum computer. The next chapter meets its "
            "unit, the qubit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.01), FadeIn(left[1]), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(mid))
            vo.wait_until("c")
            self.play(FadeIn(arr), FadeIn(right))
            self.play(FadeIn(rule))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.5), run_time=3)
        self.wait(0.4)
        self.clear_scene()


_ = (NO, YES, KERN, LAM)
