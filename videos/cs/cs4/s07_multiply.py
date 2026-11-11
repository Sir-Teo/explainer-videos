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


class Multiply(VoiceoverScene):
    def construct(self):
        self.card()
        self.schoolbook()
        self.array()
        self.carry_save()
        self.tree()
        self.booth()
        self.compare()

    def card(self):
        card = chapter_card(6, r"Multiplication", r"How do you multiply in logarithmic time?", lit=(1951, 1964),
                            part=PART)
        with self.voiceover("Chapter six. Multiplication."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

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
    def array(self):
        d = load("mult")
        r = {(x["n"], x["kind"]): x for x in d["rows"]}
        head = label(r"The array multiplier: \ one adder per row", font_size=36).to_edge(UP, buff=0.35)
        n = 8
        rows = VGroup()
        for j in range(n):
            g = VGroup(*[Square(0.3, stroke_color=GREY_D, stroke_width=1, fill_color=HEAD if j == 0 else CTRL,
                                fill_opacity=0.55) for _ in range(n)]).arrange(LEFT, buff=0.05)
            g.move_to([2.2 - 0.35 * j - 1.2, 2.0 - 0.48 * j, 0])
            rows.add(g)
        arrows = VGroup(*[Arrow(rows[j].get_bottom() + DOWN * 0.02, rows[j + 1].get_top() + UP * 0.02, buff=0.02,
                                stroke_width=2, color=GREY_C, max_tip_length_to_length_ratio=0.4) for j in range(n - 1)])
        txt = VGroup(label(r"row $j$: \ the running sum, \ plus $a \cdot b_j$ shifted, \ by a ripple adder", font_size=26,
                           color=GREY_A),
                     label(rf"$8 \times 8$: \ {r[(8, 'array')]['gates']} gates, \ {r[(8, 'array')]['settle']} gate delays",
                           font_size=28, color=NO),
                     label(rf"$16 \times 16$: \ {r[(16, 'array')]['gates']} gates, \ {r[(16, 'array')]['settle']} gate "
                           r"delays: \ $O(n)$", font_size=28, color=NO)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The obvious circuit adds the rows one at a time. <bookmark mark='a'/> Each row of the array is an adder "
            "that takes the running sum from the row above, adds the next partial product, and passes the result "
            "down. <bookmark mark='b'/> It is regular and easy to lay out on a chip, which is why early multipliers "
            "looked like this. But the carries ripple along each row and the sums ripple down the rows, and the delay "
            "grows in step with n: for our sixteen-bit circuit, we observed eighty-eight gate delays in the test vectors. A processor that wanted to "
            "multiply in one cycle needed a better idea."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows))
            vo.wait_until("a")
            self.play(Create(arrows), FadeIn(txt[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(txt[1]), FadeIn(txt[2]))
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

    # ------------------------------------------------------------------
    def booth(self):
        d = load("mult")
        bb = d["booth"]
        head = label(r"Booth recoding: \ half as many rows", font_size=36).to_edge(UP, buff=0.35)
        b = bb["b"]
        digits = bb["digits"]  # least significant first
        bits = format(b, "08b")
        cells = VGroup(*[MathTex(ch, font_size=40, color=DATA) for ch in bits]).arrange(RIGHT, buff=0.3).move_to(UP * 1.6)
        groups = VGroup(*[SurroundingRectangle(VGroup(cells[2 * k], cells[2 * k + 1]), buff=0.08, color=CTRL,
                                               corner_radius=0.05) for k in range(4)])
        dig = VGroup(*[MathTex(f"{v:+d}" if v else "0", font_size=40, color=HEAD).next_to(groups[3 - k], DOWN, buff=0.35)
                       for k, v in enumerate(digits)])
        val = MathTex(r"118 = " + " ".join(
            [rf"{'+' if v >= 0 and i else ''}{'-' if v < 0 else ''}{abs(v)} \cdot 4^{{{k}}}"
             for i, (k, v) in enumerate(reversed(list(enumerate(digits))))]), font_size=36, color=GREY_A).move_to(DOWN * 0.3)
        notes = VGroup(label(r"digits in $\{-2, -1, 0, 1, 2\}$, \ read from overlapping groups of three bits",
                             font_size=26, color=GREY_A),
                       label(r"each partial product is $0$, \ $\pm a$ \ or \ $\pm 2a$: \ a shift and a negation, \ no "
                             r"multiplication", font_size=26, color=GREY_A),
                       label(r"$n/2$ rows instead of $n$, \ and signed numbers come out right", font_size=28,
                             color=YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "One more trick halves the work before it starts. <bookmark mark='a'/> Andrew Booth, in 1951, noticed that "
            "a run of ones in the multiplier, like the three ones in a row here, can be written as a big power of two "
            "minus a small one. The modern form reads the multiplier two bits at a time, plus one bit of overlap, "
            "and turns each pair into one digit from minus two to two. <bookmark mark='b'/> A hundred and eighteen "
            "becomes two times sixty-four, minus sixteen, plus two times four, minus two. <bookmark mark='c'/> Each "
            "digit picks a partial product that is zero, plus or minus a, or plus or minus two a, which is only a "
            "shift and a negation. Half as many rows go into the tree, and because the recoding treats the top bit as "
            "a sign, two's complement numbers multiply correctly without any correction. Most fast multipliers "
            "use it, in the radix-four form Orville MacSorley described in 1961."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells))
            vo.wait_until("a")
            self.play(Create(groups), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in dig], lag_ratio=0.25), Write(val))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("mult")
        rows = d["rows"]
        head = label(r"Measured: \ multipliers from 4 to 16 bits", font_size=36).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[4, 16, 4], y_range=[0, 90, 30], x_length=5.6, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(LEFT * 3.0 + DOWN * 0.4)
        t1 = note(r"gate delays \ against bits", font_size=20).next_to(ax, UP, buff=0.1)
        curves, keys = VGroup(), VGroup()
        for kind in ("array", "wallace", "dadda"):
            rs = sorted([r for r in rows if r["kind"] == kind], key=lambda r: r["n"])
            curves.add(axis_plot([r["n"] for r in rs], [r["settle"] for r in rs], ax, KIND_COLOR[kind]))
            keys.add(label(kind.title(), font_size=24, color=KIND_COLOR[kind]))
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(ax, RIGHT, buff=0.2).shift(UP * 1.2)
        r16 = {r["kind"]: r for r in rows if r["n"] == 16}
        tab = VGroup(*[label(rf"{k.title()}: \ {r16[k]['gates']} gates, \ {r16[k]['settle']} delays", font_size=26,
                             color=KIND_COLOR[k]) for k in ("array", "wallace", "dadda")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.8 + DOWN * 1.0)
        tl = note(r"$16 \times 16$, \ every design checked against Python on 20{,}000 products \ (all of them up to "
                  r"$8 \times 8$)", font_size=20).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Measured in our netlists. <bookmark mark='a'/> The array multiplier's delay climbs in a straight line; "
            "the two trees climb slowly, like log n. <bookmark mark='b'/> At sixteen bits, Dadda's tree is three and a "
            "half times faster than the array, for about sixteen percent more gates, and fewer than Wallace's. The "
            "multiplier inside a modern processor is a Booth-recoded tree with a prefix adder at the bottom: three or "
            "four cycles for sixty-four bits, pipelined so a new multiplication can start every cycle."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(t1), FadeIn(keys))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(tl))
        self.wait(0.3)
        self.clear_scene()
