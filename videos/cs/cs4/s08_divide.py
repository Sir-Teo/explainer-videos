from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, fmt, load, say, sci

QCOL = {-2: "#4C6EF5", -1: "#74C0FC", 0: "#5C677D", 1: "#FFD43B", 2: "#FF922B"}


class Divide(VoiceoverScene):
    def construct(self):
        self.card()
        self.restoring()
        self.srt()
        self.table_plot()
        self.fdiv()
        self.newton()

    def card(self):
        card = chapter_card(7, r"Division, \ and a famous bug", r"Why is dividing the hardest of the four?",
                            lit=(1958, 1994), part=PART)
        with self.voiceover("Chapter seven. Division, and a famous bug."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def restoring(self):
        d = load("divide")["restoring"]
        head = label(rf"Long division: \ ${d['x']} \div {d['d']}$, \ one bit at a time", font_size=36).to_edge(UP, buff=0.35)
        hdr = VGroup(*[label(t, font_size=22, color=GREY_B) for t in (r"bring down", r"remainder", r"minus 13",
                                                                      r"quotient bit")])
        rows = VGroup(hdr)
        for st in d["steps"]:
            q = st["q"]
            rows.add(VGroup(MathTex(rf"\text{{bit }} {st['bit']}", font_size=26, color=GREY_B),
                            MathTex(str(st["r"]), font_size=28, color=DATA),
                            MathTex(str(st["try"]), font_size=28, color=YES if q else NO),
                            MathTex(str(q), font_size=30, color=YES if q else GREY_B)))
        for i, r in enumerate(rows):
            for j, m in enumerate(r):
                m.move_to([-6.0 + 1.55 * j, 2.4 - 0.48 * i, 0])
        res = MathTex(rf"{d['x']} = {d['d']} \times {d['q']} + {d['r']} \qquad \text{{quotient }} "
                      rf"{format(d['q'], '08b')}_2", font_size=32, color=YES).move_to(RIGHT * 0.2 + UP * 1.6, aligned_edge=LEFT)
        rules = VGroup(
            label(r"shift in the next bit; \ try subtracting the divisor", font_size=24, color=GREY_A),
            label(r"if it fits: \ quotient bit 1, \ keep the difference", font_size=24, color=YES),
            label(r"if not: \ bit 0, \ restore the old remainder", font_size=24, color=NO),
            label(r"$n$ steps, \ each an $n$-bit subtraction: \ slow", font_size=26, color=HEAD),
            note(r"non-restoring division skips the restore: \\ a negative remainder is fixed by adding next time",
                 font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 0.2 + DOWN * 0.6, aligned_edge=LEFT)
        with self.voiceover(
            "Division is the hard one, because each digit depends on the remainder left by the one before. "
            "<bookmark mark='a'/> The schoolbook method, in binary: bring down the next bit of two hundred, and try "
            "subtracting thirteen. If it fits, the quotient bit is one and the difference becomes the remainder. If it "
            "does not, the bit is zero and the old remainder is restored. <bookmark mark='b'/> Eight steps give "
            "fifteen, remainder five. <bookmark mark='c'/> That is one quotient bit per subtraction, and every "
            "subtraction waits for the last, so a sixty-four-bit division takes sixty-four of them. Skipping the "
            "restore, and adding the divisor back on the next step instead, saves a little; it is called "
            "non-restoring division. To go faster, you have to produce more than one bit per step, and that needs a "
            "cleverer idea."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:4]], lag_ratio=0.5), FadeIn(rules[0:3]), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[4:]], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(res))
            vo.wait_until("c")
            self.play(FadeIn(rules[3]), FadeIn(rules[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def srt(self):
        head = label(r"SRT division: \ two bits per step, \ by guessing", font_size=36).to_edge(UP, buff=0.35)
        rec = MathTex(r"w_{j+1} = 4\,w_j - q_{j+1}\, d, \qquad q \in \{-2, -1, 0, 1, 2\}", font_size=38,
                      color=CODE).move_to(UP * 2.0)
        inv = MathTex(r"|w_j| \le \tfrac{2}{3}\, d", font_size=36, color=HEAD).next_to(rec, DOWN, buff=0.35)
        # the overlap picture: which q keep the next remainder in range, as a function of p = 4w over d
        ax = NumberLine(x_range=[-8 / 3, 8 / 3, 2 / 3], length=10.0, color=GREY_C).move_to(DOWN * 0.9)
        bands = VGroup()
        for q in (-2, -1, 0, 1, 2):
            lo, hi = q - 2 / 3, q + 2 / 3
            y = -0.25 - 0.22 * (q + 2)
            bands.add(Line(ax.n2p(max(lo, -8 / 3)) + UP * (y + 0.0), ax.n2p(min(hi, 8 / 3)) + UP * y,
                           color=QCOL[q], stroke_width=8))
            bands.add(MathTex(f"q = {q:+d}" if q else "q = 0", font_size=20, color=QCOL[q]).next_to(
                ax.n2p(min(hi, 8 / 3)) + UP * y, RIGHT, buff=0.1))
        bands.shift(DOWN * 0.3)
        axl = MathTex(r"4 w / d", font_size=26, color=GREY_B).next_to(ax, LEFT, buff=0.25)
        axn = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(ax.n2p(k), UP, buff=0.15) for k in range(-2, 3)])
        axl.add(axn)
        expl = VGroup(
            label(r"each $q$ works on an interval of width $\tfrac43$; \ neighbours overlap by $\tfrac13$", font_size=26,
                  color=GREY_A),
            label(r"so $q$ can be chosen from a few leading bits of $w$ and $d$: \ a small table", font_size=26,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 1958 Dura Sweeney at IBM, James Robertson at Illinois and Keith Tocher in London found that idea, "
            "independently, and division with it carries their initials: SRT. <bookmark mark='a'/> Work in base four, "
            "so each step makes two bits of quotient, and allow negative digits: each quotient digit is one of minus "
            "two, minus one, zero, one or two. The remainder is kept within two thirds of the divisor. "
            "<bookmark mark='b'/> Here is why that helps. For each digit, draw the range of remainders it can handle "
            "without the next remainder leaving the band. The ranges overlap. Near a boundary, two digits are both "
            "right, and either choice is corrected automatically by the digits that follow. <bookmark mark='c'/> So "
            "the hardware never needs the exact remainder to choose. A handful of its leading bits, and a few leading "
            "bits of the divisor, are enough to look the digit up in a small table, while the full subtraction "
            "happens in carry-save form, with no carries to wait for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rec))
            vo.wait_until("a")
            self.play(Indicate(rec, scale_factor=1.02), FadeIn(inv))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(axl), LaggedStart(*[Create(b) for b in bands], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(expl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plot(self, d, x0=-2.8, y0=0.0, cw=0.32, ch=0.058):
        cells = {}
        g = VGroup()
        for pi, di, q in d["table"]:
            r = Rectangle(width=cw, height=ch, stroke_width=0, fill_color=QCOL[q], fill_opacity=0.9)
            r.move_to([x0 + cw * (di - 16 + 0.5), y0 + ch * (pi + 0.5), 0])
            g.add(r)
            cells[(pi, di)] = r
        frame = Rectangle(width=16 * cw, height=88 * ch, stroke_color=GREY_D, stroke_width=1).move_to(
            [x0 + 8 * cw, y0, 0])
        xl = VGroup(*[MathTex(t, font_size=20, color=GREY_B).move_to([x0 + cw * k, y0 - 44 * ch - 0.25, 0])
                      for k, t in ((0, "1"), (8, "1.5"), (16, "2"))])
        xt = label(r"divisor $d$", font_size=22, color=GREY_B).next_to(xl, DOWN, buff=0.1)
        yt = label(r"estimate of $4w$", font_size=22, color=GREY_B).rotate(PI / 2).next_to(frame, LEFT, buff=0.3)
        yl = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to([x0, y0 + ch * 8 * v, 0], LEFT, buff=0.1)
                      for v, t in ((-4, "-4"), (0, "0"), (4, "4"))])
        return g, cells, VGroup(frame, xl, xt, yt, yl)

    def table_plot(self):
        d = load("divide")
        head = label(r"The quotient-digit table, \ computed", font_size=36).to_edge(UP, buff=0.3)
        g, cells, axes = self.plot(d, x0=-6.2)
        keys = VGroup(*[VGroup(Square(0.25, stroke_width=0, fill_color=QCOL[q], fill_opacity=0.9),
                               MathTex(f"{q:+d}" if q else "0", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.15)
                        for q in (2, 1, 0, -1, -2)]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(LEFT * 0.4 + UP * 1.4)
        txt = VGroup(
            label(rf"{say(d['cells'])} cells: \ remainder to $\tfrac18$, \ divisor to $\tfrac1{{16}}$", font_size=26,
                  color=GREY_A),
            label(rf"every one checked: \ its digit keeps the remainder in range \\ for every point of the cell", font_size=24,
                  color=GREY_A),
            label(rf"400{{,}}000 random divisions \ never visit {d['never']} of them", font_size=26, color=HEAD),
            label(rf"quotients correct to ${sci(d['good_max_rel_err'])}$ \ after {d['steps']} steps", font_size=26,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(RIGHT * 0.5 + DOWN * 1.0, aligned_edge=LEFT)
        with self.voiceover(
            "Here is that table, built for this video: the same shape as a real radix-four divider's. "
            "<bookmark mark='a'/> Across, the divisor, from one to two; up, an estimate of four times the remainder. "
            "Each little cell is coloured by the quotient digit it holds, and each digit was checked against every "
            "point of its cell: whatever the true values inside, that digit keeps the next remainder in range. "
            "<bookmark mark='b'/> The staircases are the overlaps of the last picture, seen in two dimensions. "
            "<bookmark mark='c'/> Run four hundred thousand random divisions through it, and a striking thing "
            "appears: hundreds of cells, near the top and bottom edges, are never visited at all. The divisions come "
            "out right to the last bit. And the never-visited cells are exactly where trouble hides."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axes))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in g], lag_ratio=0.0015), FadeIn(keys), run_time=3.0)
            self.play(FadeIn(txt[0]), FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(FadeIn(txt[2]), FadeIn(txt[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fdiv(self):
        d = load("divide")
        p = d["pentium"]
        head = label(r"1994: \ five missing entries", font_size=38).to_edge(UP, buff=0.3)
        g, cells, axes = self.plot(d, x0=-6.2, y0=-0.2)
        bad = VGroup(*[SurroundingRectangle(cells[(pi, di)], buff=0.04, color=NO, stroke_width=3)
                       for pi, di in d["bad_cells"]])
        story = VGroup(
            label(r"Thomas Nicely, \ summing reciprocals of twin primes, \\ finds wrong answers", font_size=22,
                  color=GREY_A),
            MathTex(rf"\frac{{{p['x']}}}{{{p['d']}}} = {p['true']:.9f}", font_size=32, color=YES),
            MathTex(rf"\text{{Pentium: }} {p['pentium']:.9f}", font_size=32, color=NO),
            label(r"5 of 1{,}066 table entries were 0 instead of 2, \\ at the upper edge, \ thought unreachable",
                  font_size=22, color=GREY_A),
            label(r"about 1 random division in 9 billion; \\ the recall cost Intel \$475 million", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(LEFT * 0.4 + UP * 0.8, aligned_edge=LEFT)
        ours = VGroup(
            label(rf"our toy: \ empty the highest visited cell in five columns", font_size=22, color=NO),
            label(rf"{say(d['bad_wrong'])} of {say(d['bad_divisions'])} random divisions come out wrong, \\ by up to "
                  rf"{100 * d['bad_max_rel']:.0f}\%", font_size=22, color=NO),
            note(r"a wrong digit pushes the remainder out of range, \\ and no later digit can bring it back", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        ours.align_to(story, LEFT)
        with self.voiceover(
            "In 1994 Thomas Nicely, a mathematician in Virginia, was adding up the reciprocals of twin primes on a "
            "new Intel Pentium, and the sums came out wrong. <bookmark mark='a'/> The cause was the table. Intel's "
            "divider used radix-four SRT with a table of one thousand and sixty-six entries, and five of them, on the "
            "upper edge, held zero where they should have held two: they had been assumed unreachable. "
            "<bookmark mark='b'/> The most famous example: four million, one hundred and ninety-five thousand, eight "
            "hundred and thirty-five divided by three million, one hundred and forty-five thousand, seven hundred and "
            "twenty-seven is one point three three three eight two; the Pentium said one point three three three seven "
            "three, wrong in the fourth decimal place. <bookmark mark='c'/> We can do the same to our table. Empty the highest "
            "cell that random divisions ever visit, in five columns, and run two million divisions. Almost one in a "
            "hundred now comes out wrong, some badly, because a wrong digit throws the remainder out of the band and "
            "no later digit can bring it back. Intel's cells were reached about once in nine billion random divisions, "
            "which is why its testing missed them. Intel first said most users would never notice, then replaced the "
            "chips, for four hundred and seventy-five million dollars. Since then, chip arithmetic has been proved "
            "correct by machine, as Part 54 will show."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axes), FadeIn(g), FadeIn(story[0]))
            vo.wait_until("a")
            self.play(Create(bad), FadeIn(story[3]))
            vo.wait_until("b")
            self.play(FadeIn(story[1]), FadeIn(story[2]))
            vo.wait_until("c")
            self.play(*[c.animate.set_fill(BG, 1) for c in [cells[(pi, di)] for pi, di in d["bad_cells"]]])
            self.play(FadeIn(ours, lag_ratio=0.3), FadeIn(story[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def newton(self):
        d = load("divide")
        nr = d["newton"]
        head = label(r"Or divide by multiplying: \ Newton--Raphson", font_size=36).to_edge(UP, buff=0.35)
        it = MathTex(r"y_{k+1} = y_k\,(2 - d\, y_k)", font_size=42, color=CODE).move_to(LEFT * 3.0 + UP * 1.8)
        why = MathTex(r"e_{k+1} = d\, e_k^2 \quad \text{where } e_k = \tfrac1d - y_k", font_size=32,
                      color=HEAD).next_to(it, DOWN, buff=0.35)
        der = note(r"Newton's method on $f(y) = \tfrac1y - d$: \ the error squares at every step", font_size=22).next_to(
            why, DOWN, buff=0.2)
        rows = VGroup()
        for r in nr:
            err = r["err"]
            rows.add(VGroup(MathTex(rf"k = {r['k']}", font_size=28, color=GREY_B),
                            MathTex(rf"{r['y']:.16f}"[:18], font_size=28, color=DATA),
                            MathTex(sci(err) if err else r"0 \ (\text{exact in float64})", font_size=28,
                                    color=YES if err < 1e-6 else GREY_A)))
        for i, r in enumerate(rows):
            for j, m in enumerate(r):
                m.move_to([[-5.6, -2.8, 1.6][j], -0.4 - 0.48 * i, 0], aligned_edge=LEFT)
        tl = note(rf"$d = {d['nr_d']}$, \ first guess $0.75$ \ (from a small table)", font_size=22).next_to(rows, UP,
                                                                                                         buff=0.2).align_to(rows, LEFT)
        side = VGroup(label(r"correct digits double each step", font_size=26, color=YES),
                      label(r"each step: two multiplications, \ on the fast tree multiplier", font_size=24, color=GREY_A),
                      label(r"Goldschmidt's variant multiplies \\ numerator and denominator in parallel", font_size=24,
                            color=GREY_A),
                      note(r"used for division and square roots \ in many floating-point units", font_size=22)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.6 + UP * 1.1)
        with self.voiceover(
            "There is a completely different way to divide: do not. Compute the reciprocal of d, and multiply. "
            "<bookmark mark='a'/> To find one over d, apply Newton's method to the function one over y minus d. The "
            "iteration needs only multiplications: y times two minus d y. <bookmark mark='b'/> And its error squares "
            "at every step. If the error is a hundredth, the next is about a ten-thousandth. "
            "<bookmark mark='c'/> Start from a rough guess read from a small table, and watch the correct digits "
            "roughly double at every step. Five steps give one over one point seven to full double "
            "precision. <bookmark mark='d'/> Each step costs two multiplications on the fast multiplier we just built. "
            "Robert Goldschmidt's variant multiplies the numerator and the denominator by the same factors in "
            "parallel, and floating-point units use these methods for division and square roots."
        ) as vo:
            self.play(FadeIn(head), FadeIn(it))
            vo.wait_until("a")
            self.play(Indicate(it, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(why), FadeIn(der))
            vo.wait_until("c")
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s) for s in side], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()
