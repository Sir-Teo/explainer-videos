from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, KIND_COLOR, NO, PART, YES, axis_plot, load)


def wallace_heights(n: int) -> list[list[int]]:
    """Column heights of an n x n multiplier's partial products, stage by stage, under Wallace's rule."""
    h = [min(k + 1, 2 * n - 1 - k) for k in range(2 * n)]
    h[-1] = 0
    out = [list(h)]
    while max(h) > 2:
        new = [0] * (2 * n + 1)
        for k, x in enumerate(h):
            fa, r = x // 3, x % 3
            new[k] += fa
            new[k + 1] += fa
            if r == 2:
                new[k] += 1
                new[k + 1] += 1
            else:
                new[k] += r
        h = new[:2 * n]
        out.append(list(h))
    return out


def dot_matrix(heights, x0=4.6, dx=0.42, y0=-2.2, dy=0.38, color=DATA):
    g = VGroup()
    for k, hgt in enumerate(heights):
        for r in range(hgt):
            g.add(Dot([x0 - dx * k, y0 + dy * r, 0], radius=0.09, color=color))
    return g


class Multiply(WatchScene):
    def construct(self):
        self.card()
        self.schoolbook()
        self.carry_save()
        self.tree()

    def card(self):
        self.chapter(6, r"Multiplication", r"How do you multiply in logarithmic time?", lit=(1951, 1964), part=PART, said="Chapter six. Multiplication.")

    # ------------------------------------------------------------------
    def schoolbook(self):
        head = label(r"Shift and add", font_size=38).to_edge(UP, buff=0.35)
        a, b = "1011", "1101"
        dx = 0.62
        xr = 1.4  # right edge of the numbers

        def row(bits, y, shift=0, color=DATA):
            return VGroup(*[MathTex(ch, font_size=40, color=color).move_to([xr - dx * (len(bits) - 1 - i + shift), y, 0])
                            for i, ch in enumerate(bits)])

        ra, rb = row(a, 2.3), row(b, 1.6)
        times = MathTex(r"\times", font_size=40, color=GREY_B).move_to([xr - dx * 4.3, 1.6, 0])
        bar1 = Line([xr - dx * 7.5, 1.2, 0], [xr + 0.3, 1.2, 0], color=GREY_B)
        pps = VGroup()
        for j in range(4):
            bit = b[3 - j]
            pps.add(row(a if bit == "1" else "0000", 0.8 - 0.55 * j, shift=j, color=HEAD if bit == "1" else GREY_C))
        bar2 = Line([xr - dx * 7.5, -1.5, 0], [xr + 0.3, -1.5, 0], color=GREY_B)
        prod = format(int(a, 2) * int(b, 2), "08b")
        rp = row(prod, -1.95, color=YES)
        dec = MathTex(r"11 \times 13 = 143", font_size=36, color=GREY_A).move_to(RIGHT * 4.3 + UP * 1.9)
        notes = VGroup(label(r"each partial product: \ $a$ or 0, \ shifted", font_size=26, color=HEAD),
                       label(r"a bit times a bit is an AND: \ $n^2$ AND gates", font_size=26, color=GREY_A),
                       label(r"then add $n$ numbers", font_size=26, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 4.15 + DOWN * 0.4)
        with self.voiceover(
            "Multiplication in binary is the schoolbook method with the times table thrown away. "
            "<bookmark mark='a'/> To multiply eleven by thirteen, go through the bits of thirteen from the right. "
            "Each bit is a zero or a one, so each row is either nothing or eleven itself, shifted one more place "
            "left. <bookmark mark='b'/> Add the rows and you have a hundred and forty-three. <bookmark mark='c'/> In "
            "gates, each digit of each row is a bit of a anded with a bit of b, so the rows cost n squared and gates "
            "all at once, in one gate delay. Everything else is adding n numbers together, and the question, again, "
            "is how fast."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ra), FadeIn(rb), FadeIn(times), Create(bar1), FadeIn(dec))
            vo.wait_until("a")
            for p in pps:
                self.play(FadeIn(p, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("b")
            self.play(Create(bar2), FadeIn(rp))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(nn) for nn in notes], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()


    # ------------------------------------------------------------------
    def carry_save(self):
        head = label(r"Carry-save: \ three numbers in, \ two out, \ no carries", font_size=36).to_edge(UP, buff=0.35)
        rng = np.random.default_rng(3)
        nums = [int(v) for v in rng.integers(40, 255, 3)]
        bits = [format(v, "08b") for v in nums]
        s_word = format(nums[0] ^ nums[1] ^ nums[2], "08b")
        c_word = format(((nums[0] & nums[1]) | (nums[0] & nums[2]) | (nums[1] & nums[2])) << 1, "09b")
        dx = 0.52
        xr = 0.6

        def row(b, y, color, shift=0):
            return VGroup(*[MathTex(ch, font_size=34, color=color).move_to([xr - dx * (len(b) - 1 - i + shift), y, 0])
                            for i, ch in enumerate(b)])

        r3 = VGroup(*[row(b, 1.9 - 0.5 * i, DATA) for i, b in enumerate(bits)])
        names = VGroup(*[MathTex(rf"{v}", font_size=28, color=GREY_B).move_to([xr + 1.2, 1.9 - 0.5 * i, 0])
                         for i, v in enumerate(nums)])
        cols = VGroup(*[SurroundingRectangle(VGroup(r3[0][i], r3[2][i]), buff=0.06, color=CTRL, stroke_width=1.5)
                        for i in range(8)])
        fa = label(r"one full adder per column, \ side by side", font_size=26, color=CTRL).next_to(cols, UP, buff=0.3)
        rs = row(s_word, -0.4, YES)
        rc = row(c_word, -0.9, HEAD)
        sn = VGroup(MathTex(rf"\text{{sums}}: {int(s_word, 2)}", font_size=26, color=YES).move_to([xr + 1.7, -0.4, 0]),
                    MathTex(rf"\text{{carries}}: {int(c_word, 2)}", font_size=26, color=HEAD).move_to([xr + 1.8, -0.9, 0]))
        check = MathTex(rf"{nums[0]} + {nums[1]} + {nums[2]} = {sum(nums)} = {int(s_word, 2)} + {int(c_word, 2)}",
                        font_size=32, color=GREY_A).move_to(DOWN * 1.9)
        foot = label(r"one full-adder delay, \ whatever $n$ is: \ the carries are saved, \ not propagated",
                     font_size=26, color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The better idea is to stop adding, in the usual sense. <bookmark mark='a'/> Take three numbers. Put a "
            "full adder on every column, all side by side, each adding the three bits in its own column. "
            "<bookmark mark='b'/> Each full adder makes a sum bit, which stays in its column, and a carry bit, which "
            "belongs one column to the left. Collect the sums into one number and the carries into another. "
            "<bookmark mark='c'/> The three numbers have become two with the same total, and it took one full-adder "
            "delay, no matter how wide the numbers are, because no carry travelled anywhere. This is carry-save "
            "addition, and a full adder used this way is called a three-to-two compressor."
        ) as vo:
            self.play(FadeIn(head), FadeIn(r3), FadeIn(names))
            vo.wait_until("a")
            self.play(Create(cols), FadeIn(fa))
            vo.wait_until("b")
            self.play(FadeIn(rs), FadeIn(sn[0]))
            self.play(FadeIn(rc, shift=LEFT * 0.2), FadeIn(sn[1]))
            vo.wait_until("c")
            self.play(FadeIn(check), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tree(self):
        self.ask(r"A Wallace tree for $n$-bit multiplication. \\ Its depth grows like...", [r"$n$", r"$\log n$",
                 r"$n^2$"], 1,
                 say="Wallace's tree adds all the partial products at once. How does its depth grow with n?",
                 reveal="Like log n. Each carry-save layer turns three numbers into two.")
        d = load("mult")
        r = {(x["n"], x["kind"]): x for x in d["rows"]}
        stages = wallace_heights(8)
        head = label(r"A Wallace tree: \ compress the partial products in parallel", font_size=34).to_edge(UP, buff=0.3)
        mats = [dot_matrix(h, x0=3.6, y0=-1.9) for h in stages]
        cap = VGroup(*[label(rf"stage {k}: \ tallest column {max(h)}", font_size=28, color=HEAD).to_edge(UP, buff=1.2)
                       for k, h in enumerate(stages)])
        rule = MathTex(r"h \to \lceil 2h/3 \rceil: \quad 8 \to 6 \to 4 \to 3 \to 2", font_size=34,
                       color=CODE).to_edge(DOWN, buff=0.85)
        fin = label(r"then one fast (prefix) adder for the last two rows", font_size=26, color=YES).to_edge(DOWN,
                                                                                                    buff=0.35)
        res = label(rf"$16 \times 16$: \ {r[(16, 'wallace')]['stages']} stages, \ {r[(16, 'wallace')]['settle']} gate "
                    rf"delays, \ against the array's {r[(16, 'array')]['settle']}", font_size=28,
                    color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 1964 Chris Wallace put this to work on all the partial products at once. <bookmark mark='a'/> Draw "
            "every partial-product bit of an eight-by-eight multiplication as a dot in its column: sixty-four dots, "
            "piled eight high in the middle. <bookmark mark='b'/> In every column, group the dots in threes and send "
            "each group through a full adder: one dot stays, one moves left. Every column shrinks to about two thirds "
            "of its height, all at the same time. Eight becomes six, then four, then three, then two. "
            "<bookmark mark='c'/> Two rows are left, and one fast prefix adder from chapter four finishes the job. "
            "Because each stage cuts the height by a constant factor, the number of stages grows like the logarithm "
            "of n. <bookmark mark='d'/> At sixteen bits the tree needs six stages and twenty-eight gate delays, where "
            "the array needed eighty-eight. Luigi Dadda's refinement of 1965 compresses only as much as each stage "
            "requires, and saves gates for the same depth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(mats[0], cap[0])))
            vo.wait_until("a")
            self.play(Indicate(mats[0], scale_factor=1.03))
            vo.wait_until("b")
            cur = mats[0]
            for k in range(1, len(stages)):
                self.play(ReplacementTransform(cur, mats[k]), ReplacementTransform(cap[k - 1], cap[k]), run_time=1.3)
                cur = mats[k]
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(fin))
            vo.wait_until("d")
            self.play(FadeOut(fin), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()


