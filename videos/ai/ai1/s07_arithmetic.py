from __future__ import annotations

import math


from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import ALPHA27, MONO, ZoomLadder, letter_row, load, tt


def binary(x: float, n: int) -> str:
    """The first n binary digits of x in [0, 1)."""
    out = []
    for _ in range(n):
        x *= 2
        b = int(x)
        out.append(str(b))
        x -= b
    return "".join(out)


def common_prefix(a: str, b: str) -> int:
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]:
        k += 1
    return k


class Arithmetic(VoiceoverScene):
    def construct(self):
        self.card()
        self.whole_bits()
        self.encode()
        self.finish()
        self.decode()
        self.equivalence()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Arithmetic coding: prediction is compression",
                            r"Can a code pay exactly the surprise, a fraction of a bit at a time?", lit=(1976,), part=1)
        with self.voiceover("Chapter six. The best code for a good guesser.") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def whole_bits(self):
        bg = load("bigram")
        info = -math.log2(float(bg["q_u"]))
        head = label(r"Huffman's flaw: \ every symbol costs a whole number of bits", font_size=34).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(rf"\texttt{{u}} after \texttt{{q}}: \ carries ${info:.3f}$ bits, \ costs at least $1$", font_size=30),
            label(r"a model that knows English well: \ about $1$ bit per symbol of surprise", font_size=30),
            label(r"\ldots but a symbol code can never spend less than $1$ bit on a symbol", font_size=30,
                  color=C.SURPRISE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.4)
        fix = label(r"the fix: code the whole message at once, as one number", font_size=32, color=C.BITS)
        fix.to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Huffman's code has one flaw. Every symbol costs a whole number of bits, at least one. "
            "<bookmark mark='a'/> u after q carries two thousandths of a bit, and still costs a full bit. "
            "<bookmark mark='b'/> That's tolerable for letter frequencies, but a model that really knows English "
            "is surprised by about one bit per symbol, or less, and a symbol code can never go below one. "
            "<bookmark mark='c'/> The fix is to stop coding symbols one at a time, and code the whole message as a "
            "single number."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(fix))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def encode(self):
        a = load("arith")
        steps = a["steps"]
        msg = a["message"]
        assert msg == "the falcon" and len(steps) == 10
        lad = ZoomLadder(steps, W=8.4, x=-0.9, bar_h=0.38, font_size=20)
        dy = 1.05
        y_top = 2.35
        head = label(r"Encoding \texttt{the falcon} \ (after \texttt{he said})", font_size=30).to_edge(UP, buff=0.25)
        ctx_x, read_x = -5.95, 3.55
        # interval ends after each step
        lows = [s["low"] for s in steps[1:]] + [a["final_low"]]
        widths = [s["width"] for s in steps[1:]] + [a["final_width"]]
        assert all(abs(math.log2(w) - (steps[k + 1]["log2_width"] if k < 9 else math.log2(a["final_width"]))) < 1e-9
                   for k, w in enumerate(widths))
        nb = 34
        bits_so_far = []
        for lo, w in zip(lows, widths):
            bl, bh = binary(lo, nb), binary(lo + w, nb)
            bits_so_far.append((bl, bh, common_prefix(bl, bh)))
        assert bits_so_far[0][2] == 2 and bits_so_far[-1][2] >= 26

        def bin_lines(k):
            bl, bh, c = bits_so_far[k]
            g = VGroup()
            for name, b in (("low ", bl), ("high", bh)):
                t = Text(f"{name} = 0." + b + "...", font=MONO, font_size=20, color=GREY_B)
                off = len(f"{name} = 0.".replace(" ", ""))  # Text has no glyphs for spaces
                for j in range(c):
                    t[off + j].set_color(C.BITS)
                g.add(t)
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.3).shift(LEFT * 1.2)
            dec = label(rf"${c}$ bits decided", font_size=22, color=C.BITS).next_to(g, RIGHT, buff=0.4)
            return VGroup(g, dec)

        tot = ValueTracker(0.0)
        # a fixed label and a DecimalNumber (cached digits), so the readout isn't re-typeset every frame
        tot_head = MathTex(r"\log_2 \tfrac{1}{\text{width}} =", font_size=28, color=C.INTERVAL)
        tot_num = DecimalNumber(0, num_decimal_places=2, font_size=28, color=C.INTERVAL)
        tot_unit = MathTex(r"\text{bits}", font_size=28, color=C.INTERVAL)
        tot_lab = VGroup(tot_head, tot_num, tot_unit).arrange(RIGHT, buff=0.12).to_corner(UR, buff=0.35)
        tot_lab.shift(DOWN * 0.55 + LEFT * 0.35)  # room for the number to grow to two digits
        tot_num.add_updater(lambda m: m.set_value(tot.get_value()).next_to(tot_head, RIGHT, buff=0.12))
        tot_unit.add_updater(lambda m: m.next_to(tot_num, RIGHT, buff=0.12))
        shown = []  # (row, funnel, ctx, read) on screen, oldest first
        lines = None

        def add_row(k, run_time=0.9):
            nonlocal lines
            anims = []
            if len(shown) == 4:  # scroll: drop the oldest row (and the new top row's funnel), move the rest up
                old = shown.pop(0)
                anims += [FadeOut(m, shift=UP * 0.4) for m in old if m is not None]
                if shown[0][1] is not None:
                    anims.append(FadeOut(shown[0][1]))
                    shown[0] = (shown[0][0], None, shown[0][2], shown[0][3])
                for grp in shown:
                    anims += [m.animate.shift(UP * dy) for m in grp if m is not None]
                if anims:
                    self.play(*anims, run_time=0.5)
            y = y_top - dy * len(shown)
            row = lad.row(k, y)
            fun = lad.funnel(k - 1, y + dy, y) if shown else None
            st = steps[k]
            ctx = label(tt(st["context"]), font_size=22, color=C.CONTEXT).move_to([ctx_x, y, 0])
            rd = mtex(r"P(" + tt(st["symbol"]) + rf") = {st['p']:.3f}", font_size=24, color=C.INTERVAL)
            rd.move_to([read_x, y, 0], aligned_edge=LEFT)
            show = [FadeIn(row[0]), Create(row[2]), FadeIn(ctx)]
            if fun is not None:
                show.insert(0, FadeIn(fun))
            self.play(*show, run_time=run_time * 0.6)
            new_lines = bin_lines(k)
            self.play(FadeIn(row[1]), FadeIn(rd), tot.animate.set_value(-math.log2(widths[k])),
                      (Transform(lines, new_lines) if lines is not None else FadeIn(new_lines)), run_time=run_time * 0.6)
            if lines is None:
                lines = new_lines
            shown.append((row, fun, ctx, rd))

        src = cite(r"J.~Rissanen (1976); \ R.~Pasco (1976); \ I.~Witten, R.~Neal \& J.~Cleary, \textit{Arithmetic "
                   r"Coding for Data Compression} (1987)")
        with self.voiceover(
            "Arithmetic coding, worked out by Jorma Rissanen and Richard Pasco in 1976. We've already seen its "
            "heart: the nested slivers of the chain rule. <bookmark mark='a'/> Start with the unit interval, split "
            "by the model's guesses for the first letter. t takes a sliver 0.155 wide. Now write the two ends of "
            "that sliver in binary. <bookmark mark='b'/> They agree on their first two digits, one, one. Any number "
            "in the sliver starts that way, so those two bits are already decided."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tot_lab), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeOut(src))
            add_row(0, run_time=1.6)
            vo.wait_until("b")
            self.play(Indicate(lines[1], color=C.BITS))
        with self.voiceover(
            "Then zoom in and split again: h, e, space, f, a, l, c, o, n. <bookmark mark='a'/> Each letter "
            "narrows the interval by its probability, and as it narrows, more leading digits of its two ends come to "
            "agree. Those bits can be sent as soon as they're decided. <bookmark mark='b'/> A likely letter barely "
            "narrows the interval, and costs a fraction of a bit. An unlikely one, like the c in falcon, which "
            "the model gave less than one percent, costs seven bits."
        ) as vo:
            for k in range(1, 6):
                add_row(k, run_time=1.0)
            vo.wait_until("a")
            for k in range(6, 10):
                add_row(k, run_time=1.0)
            vo.wait_until("b")
            assert steps[7]["symbol"] == "c" and steps[7]["p"] < 0.01 and abs(steps[7]["bits"] - 7.0) < 0.05
            row_c = next(g for g in shown if g[0] is not None and g[3] is not None and "0.008" in g[3].tex_string)
            self.play(Indicate(row_c[3], color=C.SURPRISE), Indicate(row_c[0], color=C.SURPRISE, scale_factor=1.02))
        tot_num.clear_updaters()
        tot_unit.clear_updaters()
        self.lines = lines
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def finish(self):
        a = load("arith")
        bits, n, info = a["bits"], int(a["n_bits"]), float(a["info"])
        assert n == 29 and abs(info - 27.66) < 0.01 and bits == "11001010000101111011011001110"
        head = label(r"The final interval has width $2^{-27.66}$", font_size=34).to_edge(UP, buff=0.5)
        W = 12.0
        bar = Rectangle(width=W, height=0.5, stroke_color=GREY_C, stroke_width=1.5).move_to(UP * 1.2)
        inner = Rectangle(width=W * 0.42, height=0.5, stroke_width=0, fill_color=C.INTERVAL, fill_opacity=0.5)
        inner.move_to(bar).shift(RIGHT * 0.4)
        dyad = Rectangle(width=W * 0.2, height=0.5, stroke_width=2.5, stroke_color=C.BITS, fill_opacity=0)
        dyad.move_to(inner).shift(RIGHT * 0.3)
        lab_i = label(r"the message's interval", font_size=22, color=C.INTERVAL).next_to(inner, UP, buff=0.12)
        lab_i.align_to(inner, LEFT)
        lab_d = label(r"all numbers that start $0.b_1 b_2 \dots b_n$", font_size=22, color=C.BITS)
        lab_d.next_to(dyad, DOWN, buff=0.12)
        sch = note(r"schematic: \ magnified $2^{27}$ times").next_to(bar, UP, buff=0.55).align_to(bar, RIGHT)
        code = Text("0." + bits, font=MONO, font_size=32, color=C.BITS).move_to(DOWN * 0.6)
        cmp = VGroup(
            label(r"fixed $5$-bit code: \ $50$ bits", font_size=28, color=GREY_B),
            label(r"Huffman: \ $43$ bits", font_size=28, color=GREY_A),
            label(r"arithmetic coding: \ $29$ bits", font_size=28, color=C.BITS),
            label(rf"information content $\log_2 \frac{{1}}{{P}}$: \ ${info:.2f}$ bits", font_size=28, color=C.INTERVAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.45)
        bound = label(r"always within $2$ bits of $\log_2 \frac{1}{P(\text{message})}$", font_size=26,
                      color=GREY_A).next_to(code, DOWN, buff=0.25)
        with self.voiceover(
            "After ten letters, the interval has width two to the minus 27.66: the probability of the whole "
            "message. <bookmark mark='a'/> To finish, find the shortest binary fraction such that every number "
            "starting with those digits lies inside the interval. <bookmark mark='b'/> Here, it takes 29 bits. "
            "<bookmark mark='c'/> Compare: fifty for the fixed code, forty-three for Huffman, twenty-nine for "
            "arithmetic coding, against an information content of 27.66. Arithmetic coding always lands within two "
            "bits of the surprise of the whole message."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(bar), FadeIn(inner), FadeIn(lab_i), FadeIn(sch))
            self.play(Create(dyad), FadeIn(lab_d))
            vo.wait_until("b")
            self.play(Write(code), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in cmp], lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(bound))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decode(self):
        a = load("arith")
        steps = a["steps"]
        v = int(a["bits"], 2) / 2 ** int(a["n_bits"]) + 2.0 ** -(int(a["n_bits"]) + 1)
        lad = ZoomLadder(steps, W=10.0, x=0.3, bar_h=0.36, font_size=20)
        ys = [2.0, 0.9, -0.2]
        head = label(r"Decoding: the same model, run in reverse", font_size=32).to_edge(UP, buff=0.3)
        code = Text("0." + a["bits"], font=MONO, font_size=24, color=C.BITS).to_edge(DOWN, buff=0.4)
        rows, marks = VGroup(), VGroup()
        lo, w = 0.0, 1.0
        out = VGroup()
        for k in range(3):
            row = lad.row(k, ys[k], chosen=False)
            u = (v - lo) / w  # where the number falls in this row's interval
            x = lad.x - lad.W / 2 + u * lad.W
            mk = Line([x, ys[k] + 0.3, 0], [x, ys[k] - 0.3, 0], color=C.BITS, stroke_width=4)
            s = ALPHA27.index(steps[k]["symbol"])
            lo_k, hi_k = lad.bounds(k, s)
            assert lo_k <= u < hi_k
            hl = lad.row(k, ys[k])
            rows.add(VGroup(row, hl))
            marks.add(mk)
            lo, w = lo + w * lo_k, w * (hi_k - lo_k)
            out.add(letter_row(steps[k]["symbol"], font_size=34, color=C.TRUE_P))
        out.arrange(RIGHT, buff=0.1).to_corner(UR, buff=0.5).shift(DOWN * 0.6)
        with self.voiceover(
            "Decoding runs the same steps. The receiver has the bits, and an identical copy of the model. "
            "<bookmark mark='a'/> The bits name a number. It falls in the t sliver of the first split, so the first "
            "letter is t. <bookmark mark='b'/> Zoom in: it falls in the h sliver of the next, then e, and so on, "
            "one letter at a time, until the message is back, exactly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            for k in range(3):
                if k == 1:
                    vo.wait_until("b")
                self.play(FadeIn(rows[k][0]), run_time=0.5)
                self.play(Create(marks[k]), run_time=0.4)
                self.play(FadeIn(rows[k][1]), FadeIn(out[k]), run_time=0.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def equivalence(self):
        left = VGroup(RoundedRectangle(width=4.2, height=1.6, corner_radius=0.2, color=C.MODEL_Q, stroke_width=3),
                      label(r"a model that predicts\\ $q(x_t \mid x_{<t})$", font_size=28, color=C.MODEL_Q))
        right = VGroup(RoundedRectangle(width=4.2, height=1.6, corner_radius=0.2, color=C.BITS, stroke_width=3),
                       label(r"a compressor\\ $\ell(\text{text})$ bits", font_size=28, color=C.BITS))
        left.move_to(LEFT * 3.6 + UP * 1.4)
        right.move_to(RIGHT * 3.6 + UP * 1.4)
        a1 = Arrow(left.get_right() + UP * 0.3, right.get_left() + UP * 0.3, color=WHITE, buff=0.15)
        a2 = Arrow(right.get_left() + DOWN * 0.3, left.get_right() + DOWN * 0.3, color=WHITE, buff=0.15)
        l1 = label(r"arithmetic coding", font_size=22, color=GREY_A).next_to(a1, UP, buff=0.1)
        l2 = label(r"$q = 2^{-\ell}$", font_size=24, color=GREY_A).next_to(a2, DOWN, buff=0.1)
        eq = mtex(r"\text{compressed size} \approx \sum_t \log_2 \frac{1}{q(x_t \mid x_{<t})} = "
                  r"N \times \text{cross-entropy}", font_size=36).move_to(DOWN * 0.6)
        tag = label(r"to compress well, predict well; \ to predict well, compress well", font_size=32, color=C.BITS)
        tag.next_to(eq, DOWN, buff=0.45)
        facts = VGroup(
            note(r"Hutter Prize (2006): \ compress a fixed slice of Wikipedia, as a test of intelligence", font_size=22),
            note(r"Del\'etang et al., \textit{Language Modeling Is Compression} (2024): \ Chinchilla 70B compresses "
                 r"ImageNet patches to $43.4\%$, \ beating PNG ($58.5\%$)", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "This is the hinge of the whole part. <bookmark mark='a'/> Give arithmetic coding any model that "
            "predicts, and you get a compressor whose output is about log of one over q bits per symbol: the length "
            "of the text times the model's cross-entropy. <bookmark mark='b'/> And any compressor defines a model: a "
            "text that takes l bits is being assigned probability two to the minus l. <bookmark mark='c'/> So "
            "predicting well and compressing well are the same skill."
        ) as vo:
            self.play(FadeIn(left), FadeIn(right))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(l1))
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(tag, shift=UP * 0.1))
        with self.voiceover(
            "That's why, in 2006, Marcus Hutter offered a prize for compressing Wikipedia, as a test of "
            "intelligence. <bookmark mark='a'/> And it's why, in 2024, a team at DeepMind could show that a large "
            "language model, trained only on text, also compresses images and audio better than the formats made "
            "for them."
        ) as vo:
            self.play(FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(FadeIn(facts[1]))
        self.wait(0.5)
        self.clear_scene()
