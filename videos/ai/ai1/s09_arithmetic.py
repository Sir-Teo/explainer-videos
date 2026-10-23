from __future__ import annotations

import math


from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import ALPHA27, MONO, PART, ZoomLadder, letter, letter_row, load, tt


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
        self.bound()
        self.decode()
        self.precision()
        self.passage()
        self.equivalence()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Arithmetic coding: prediction is compression",
                            r"Can a code pay exactly the surprise, a fraction of a bit at a time?", lit=(1976,),
                            part=PART)
        with self.voiceover("Chapter eight. The best code for a good guesser.") as vo:
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
        fix.to_edge(DOWN, buff=0.5)
        k_ = 4.0  # screen units per bit
        waste = VGroup(
            Rectangle(width=max(k_ * info, 0.03), height=0.4, stroke_width=0, fill_color=C.SURPRISE, fill_opacity=0.9),
            Rectangle(width=k_, height=0.4, stroke_color=C.BITS, stroke_width=2.5, fill_opacity=0))
        waste[0].move_to([-2.0 + waste[0].width / 2, -1.6, 0])
        waste[1].move_to([-2.0 + k_ / 2, -2.2, 0])
        wl = VGroup(label(rf"information: \ ${info:.3f}$ bits", font_size=22, color=C.SURPRISE).next_to(waste[0], LEFT, buff=0.3),
                    label(r"cost: \ $1$ bit", font_size=22, color=C.BITS).next_to(waste[1], LEFT, buff=0.3))
        for t_ in wl:
            t_.align_to([-2.3, 0, 0], RIGHT)
        with self.voiceover(
            "Huffman's code has one flaw. Every symbol costs a whole number of bits, at least one. "
            f"<bookmark mark='a'/> u after q carries {info:.3f} bits, and still costs a full bit. "
            "<bookmark mark='b'/> That's tolerable for letter frequencies, but a model that really knows English "
            "is surprised by about one bit per symbol, or less, and a symbol code can never go below one. Coding long "
            "blocks would fix it, but a code table for blocks of a hundred letters would need twenty-seven to the "
            "hundred entries, and a model that reads the context changes its guesses at every letter. "
            "<bookmark mark='c'/> The fix is to code the whole message as a single number, one guess at a time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[2]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(waste[1]), FadeIn(wl[1]), GrowFromEdge(waste[0], LEFT), FadeIn(wl[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeOut(VGroup(waste, wl)), FadeIn(fix))
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
        c0 = bits_so_far[0][2]
        hard = max(range(len(steps)), key=lambda k: steps[k]["bits"])
        hs = steps[hard]
        hs_word = next(w for w in msg.split(" ") if msg.index(w) <= hard < msg.index(w) + len(w)) if msg[hard] != " " else msg
        hs_sym = msg[hard] if msg[hard] != " " else "space"

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
        hc = history_card(1976, r"Jorma Rissanen (IBM) \ and Richard Pasco (Stanford)",
                          r"arithmetic coding: \ a whole message as one number", width=6.4).move_to(DOWN * 0.3)
        with self.voiceover(
            "Arithmetic coding, worked out by Jorma Rissanen and Richard Pasco in 1976. We've already seen its "
            "heart: the nested slivers of the chain rule. <bookmark mark='a'/> Start with the unit interval, split "
            f"by the model's guesses for the first letter. t takes a sliver {steps[0]['p']:.3f} wide. Now write the "
            f"two ends of that sliver in binary. <bookmark mark='b'/> They agree on their first {c0} digits. Any "
            "number in the sliver starts that way, so those bits are already decided."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tot_lab), FadeIn(src), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(src), FadeOut(hc))
            add_row(0, run_time=1.6)
            vo.wait_until("b")
            self.play(Indicate(lines[1], color=C.BITS))
        with self.voiceover(
            "Then zoom in and split again: h, e, space, f, a, l, c, o, n. <bookmark mark='a'/> Each letter "
            "narrows the interval by its probability, and as it narrows, more leading digits of its two ends come to "
            "agree. Those bits can be sent as soon as they're decided. <bookmark mark='b'/> A likely letter barely "
            f"narrows the interval, and costs a fraction of a bit. An unlikely one, like the {hs_sym} in {hs_word}, "
            f"which the model gave {100 * hs['p']:.1f} percent, costs {hs['bits']:.1f} bits."
        ) as vo:
            for k in range(1, 6):
                add_row(k, run_time=1.0)
            vo.wait_until("a")
            for k in range(6, 10):
                add_row(k, run_time=1.0)
            vo.wait_until("b")
            row_c = next((g for g in shown if g[3] is not None and f"{hs['p']:.3f}" in g[3].tex_string), None)
            if row_c is not None:
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
        hf = load("huffman")
        nh, nf = len(hf["word_bits"]), int(hf["fixed_bits"])
        assert info <= n < info + 2  # the coder's guarantee
        head = label(rf"The final interval has width $2^{{-{info:.2f}}}$", font_size=34).to_edge(UP, buff=0.5)
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
            label(rf"fixed $5$-bit code: \ ${nf}$ bits", font_size=28, color=GREY_B),
            label(rf"Huffman: \ ${nh}$ bits", font_size=28, color=GREY_A),
            label(rf"arithmetic coding: \ ${n}$ bits", font_size=28, color=C.BITS),
            label(rf"information content $\log_2 \frac{{1}}{{P}}$: \ ${info:.2f}$ bits", font_size=28, color=C.INTERVAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            f"After ten letters, the interval has width two to the minus {info:.2f}: the probability of the whole "
            "message. <bookmark mark='a'/> To finish, find the shortest binary fraction such that every number "
            f"starting with those digits lies inside the interval. <bookmark mark='b'/> Here, it takes {n} bits. "
            f"<bookmark mark='c'/> Compare: {nf} for the fixed code, {nh} for Huffman, {n} for arithmetic coding, "
            f"against an information content of {info:.2f}."
        ) as vo:
            self.play(FadeIn(head), Create(bar), FadeIn(inner), FadeIn(lab_i), FadeIn(sch))
            vo.wait_until("a")
            self.play(Create(dyad), FadeIn(lab_d))
            vo.wait_until("b")
            self.play(Write(code), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in cmp], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bound(self):
        """Why the finished code is always within two bits of the message's information content."""
        head = label(r"Never more than $2$ bits over the surprise", font_size=36).to_edge(UP, buff=0.35)
        rows = [
            cmath(r"\ell", r"=", r"\Big\lceil \log_2 \tfrac{1}{P} \Big\rceil + 1", font_size=40),
            cmath(r"2^{-\ell}", r"\le", r"\tfrac{P}{2}", font_size=40),
            cmath(r"x + 2^{-\ell}", r"<", r"\text{low} + 2 \cdot 2^{-\ell} \le \text{low} + P", font_size=40),
            cmath(r"\ell", r"<", r"\log_2 \tfrac{1}{P} + 2", font_size=40),
        ]
        whys = [why(r"the length we will use"), why(r"since $\ell \ge \log_2 \frac{1}{P} + 1$"),
                why(r"$x$: the first multiple of $2^{-\ell}$ at or above low"), why(r"rounding up adds less than $1$")]
        step = ladder(self, rows, whys, keep=4, top=2.4, x=-1.4, buff=0.42, edge=6.9)
        y, W0, x0 = -2.35, 4.4, -2.6
        cell = W0 * 0.36  # a cell of the dyadic grid: at most half the interval
        x0 = -6.3 + 3.2
        grid = VGroup(*[Line([x0 - 3.2 + k * cell, y - 0.45, 0], [x0 - 3.2 + k * cell, y + 0.45, 0], color=GREY_C,
                             stroke_width=2) for k in range(9)])
        ruler = Line([x0 - 3.2, y, 0], [x0 - 3.2 + 8 * cell, y, 0], color=GREY_C, stroke_width=1.5)
        lowx = x0 - 3.2 + 1.55 * cell
        msg = Rectangle(width=W0, height=0.42, stroke_width=0, fill_color=C.INTERVAL, fill_opacity=0.55)
        msg.move_to([lowx + W0 / 2, y, 0])
        k0 = 2  # the first grid line at or above low
        inside = Rectangle(width=cell, height=0.42, stroke_color=C.BITS, stroke_width=4, fill_opacity=0)
        inside.move_to([x0 - 3.2 + (k0 + 0.5) * cell, y, 0])
        lm = label(r"width $P$", font_size=22, color=C.INTERVAL).next_to(msg, UP, buff=0.1)
        lc = label(r"width $2^{-\ell}$: \ all numbers starting with the same $\ell$ bits", font_size=22, color=C.BITS)
        lc.next_to(inside, DOWN, buff=0.55).align_to(grid, LEFT)
        sch = note(r"schematic").next_to(ruler, UP, buff=0.55).align_to(ruler, RIGHT)
        with self.voiceover(
            "Why within two bits? Let P be the message's probability: the width of its interval. "
            "<bookmark mark='a'/> Choose a length l: log of one over P, rounded up, plus one. <bookmark mark='b'/> "
            "Then a run of l bits names a little interval of width two to the minus l, at most half of P. "
            "<bookmark mark='c'/> Those little intervals tile the line, so the first one that starts at or after "
            "the low end must finish before the high end: it lies inside the message's interval, and its l bits "
            "pin the message down. <bookmark mark='d'/> So l bits always suffice, and l is less than the "
            "information content plus two."
        ) as vo:
            self.play(FadeIn(head), Create(ruler), FadeIn(grid), FadeIn(msg), FadeIn(lm), FadeIn(sch))
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(Create(inside), FadeIn(lc))
            vo.wait_until("d")
            step(3)
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
            self.play(FadeIn(head), FadeIn(code), FadeIn(rows[0][0]))
            vo.wait_until("a")
            for k in range(3):
                if k == 1:
                    vo.wait_until("b")
                if k:
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
        fwd = label(r"Chapter 15: \ language models as compressors, \ against gzip and xz", font_size=24, color=GREY_B)
        fwd.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "This is the hinge of the whole part. <bookmark mark='a'/> Give arithmetic coding any model that "
            "predicts, and you get a compressor whose output is about log of one over q bits per symbol: the length "
            "of the text times the model's cross-entropy. <bookmark mark='b'/> And any compressor defines a model: a "
            "text that takes l bits is being assigned probability two to the minus l. <bookmark mark='c'/> So "
            "predicting well and compressing well are the same skill. We'll put a language model to work as a "
            "compressor in the last chapter."
        ) as vo:
            self.play(FadeIn(left), FadeIn(right))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(l1))
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(tag, shift=UP * 0.1))
            self.play(FadeIn(fwd))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def precision(self):
        """The integer coder at work: 16-bit registers, the interval narrowed by each letter, then zoomed whenever a
        leading bit is decided (the coder's own record, from compute.py)."""
        ai = load("arithint")
        arith = load("arith")
        trace = [(k, int(lo), int(hi), z) for k, lo, hi, z in ai["trace"]]
        ends = [int(e) for e in ai["step_ends"]]
        steps = arith["steps"]
        R = 16
        FULL = 2 ** R
        X0, X1, Y = -5.6, 5.6, 0.2
        W = X1 - X0

        def X(v):
            return X0 + W * v / FULL

        ruler = Line([X0, Y, 0], [X1, Y, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup()
        for f, t in ((0, "0"), (0.25, r"\tfrac14"), (0.5, r"\tfrac12"), (0.75, r"\tfrac34"), (1, "1")):
            ticks.add(Line([X0 + W * f, Y - 0.12, 0], [X0 + W * f, Y + 0.12, 0], color=GREY_C, stroke_width=2))
            ticks.add(MathTex(t, font_size=26, color=GREY_B).next_to([X0 + W * f, Y - 0.12, 0], DOWN, buff=0.12))

        def bar(lo, hi):
            return Rectangle(width=max(X(hi + 1) - X(lo), 0.02), height=0.5, stroke_width=0, fill_color=C.INTERVAL,
                             fill_opacity=0.75).move_to([(X(lo) + X(hi + 1)) / 2, Y + 0.32, 0])

        def regs(lo, hi):
            a_, b_ = format(lo, f"0{R}b"), format(hi, f"0{R}b")
            k = 0
            while k < R and a_[k] == b_[k]:
                k += 1
            g = VGroup()
            for name, bits in ((r"low ", a_), (r"high", b_)):
                t = Text(f"{name} {bits}", font=MONO, font_size=24, color=GREY_B)
                off = len(name.strip())
                for j in range(k):
                    t[off + j].set_color(C.BITS)
                g.add(t)
            return g.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-3.3, 2.0, 0])

        head = label(r"In practice: \ whole numbers, and a zoom", font_size=34).to_edge(UP, buff=0.3)
        sub = label(rf"${R}$-bit registers, \ probabilities as $12$-bit counts: \ \texttt{{the falcon}}, as before",
                    font_size=22, color=GREY_B).next_to(head, DOWN, buff=0.12)
        cur = bar(0, FULL - 1)
        rg = regs(0, FULL - 1)
        sent_l = label(r"sent:", font_size=26, color=GREY_A).move_to([-5.9, -2.3, 0])
        out_bits = []
        pend = [0]

        def sent_mob():
            t = Text("".join(out_bits) or " ", font=MONO, font_size=28, color=C.BITS)
            t.next_to(sent_l, RIGHT, buff=0.25)
            return t

        def pend_mob():
            return label(rf"waiting: \ ${pend[0]}$", font_size=24, color=C.CONTEXT).move_to([4.6, -2.3, 0])

        sm, pm = sent_mob(), pend_mob()
        sym = letter(steps[0]["symbol"], font_size=40, color=C.INTERVAL).move_to([3.5, 2.0, 0])
        half_box = Rectangle(width=W / 2, height=0.9, stroke_width=0, fill_color=C.BITS, fill_opacity=0.18)

        def run_event(ev, rt):
            nonlocal cur, rg, sm, pm
            kind, lo, hi, z = ev
            if kind == "narrow":
                self.play(Transform(cur, bar(lo, hi)), Transform(rg, regs(lo, hi)), run_time=rt)
                return
            # a zoom: the half (or middle half) that holds the interval stretches to the whole range
            fx = {"0": 0.0, "1": 0.5, "p": 0.25}[z]
            hb = half_box.copy().move_to([X0 + W * (fx + 0.25), Y + 0.32, 0])
            if z in "01":
                out_bits.append(z)
                out_bits.extend(("1" if z == "0" else "0") * pend[0])
                pend[0] = 0
            else:
                pend[0] += 1
            self.play(FadeIn(hb), run_time=rt * 0.35)
            self.play(hb.animate.stretch_to_fit_width(W).move_to([X0 + W / 2, Y + 0.32, 0]).set_opacity(0),
                      Transform(cur, bar(lo, hi)), Transform(rg, regs(lo, hi)), Transform(sm, sent_mob()),
                      Transform(pm, pend_mob()), run_time=rt * 0.65)
            self.remove(hb)

        with self.voiceover(
            "A real coder can't keep fractions with thousands of digits. It keeps the interval as two whole numbers, "
            f"low and high, of {R} bits here, 32 in practice. <bookmark mark='a'/> The first letter narrows the "
            "interval. <bookmark mark='b'/> Now both ends agree on their leading bit: it's decided. Send it, and "
            "double the half that holds the interval, so it fills the whole range again: a zoom. "
            "<bookmark mark='c'/> When the interval straddles the middle but sits inside the middle half, the next "
            "bit isn't known yet. The coder zooms about the middle anyway, and remembers that a bit is waiting; it "
            "comes out, flipped, with the next decided bit. <bookmark mark='d'/> Letter by letter, narrow and zoom, "
            "and the bits stream out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), Create(ruler), FadeIn(ticks), FadeIn(cur), FadeIn(rg), FadeIn(sent_l),
                      FadeIn(sm), FadeIn(pm), FadeIn(sym))
            vo.wait_until("a")
            run_event(trace[0], 1.0)
            vo.wait_until("b")
            for ev in trace[1:ends[0]]:
                run_event(ev, 1.0)
            vo.wait_until("c")
            first_p = next((i for i, ev in enumerate(trace) if ev[3] == "p"), None)
            k = ends[0]
            for j in range(1, len(ends)):
                new_sym = letter(steps[j]["symbol"], font_size=40, color=C.INTERVAL).move_to(sym)
                self.play(Transform(sym, new_sym), run_time=0.25)
                for i in range(k, ends[j]):
                    run_event(trace[i], 0.9 if first_p is not None and i <= first_p + 1 and j < 4 else 0.45)
                k = ends[j]
                if j == 3:
                    vo.wait_until("d")
        final = Text(ai["falcon_bits"], font=MONO, font_size=28, color=C.BITS).next_to(sent_l, RIGHT, buff=0.25)
        nb, ne, info = len(ai["falcon_bits"]), int(ai["falcon_exact"]), float(ai["falcon_info"])
        cmp_said = ("the same as" if nb == ne else ("one fewer than" if nb == ne - 1 else
                    ("one more than" if nb == ne + 1 else f"{nb - ne:+d} bits against")))
        with self.voiceover(
            f"At the end, a couple of bits close it off: {nb} bits for the falcon, {cmp_said} the exact coder's {ne}. "
            "Whole numbers, and nothing longer than the registers, ever."
        ):
            self.play(Transform(sm, final), FadeOut(pm))
            self.play(Indicate(sm, color=C.BITS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def passage(self):
        ai = load("arithint")
        n, ideal = int(ai["n"]), float(ai["ideal"])
        fb, byf = [int(x) for x in ai["freq_bits"]], [int(x) for x in ai["by_freq"]]
        rb, byr = [int(x) for x in ai["reg_bits"]], [int(x) for x in ai["by_reg"]]
        show = [f for f in (6, 8, 10, 12, 16, 24) if f in fb]
        head = label(rf"The whole Falcon passage: \ ${n:,}$ letters, \ the best counting model".replace(",", "{,}"),
                     font_size=32).to_edge(UP, buff=0.35)
        info_l = label(rf"its information content under the model: \ ${ideal:,.1f}$ bits".replace(",", "{,}"),
                       font_size=28, color=C.INTERVAL).next_to(head, DOWN, buff=0.3)
        hdr = VGroup(label(r"probabilities rounded to", font_size=24, color=GREY_B),
                     label(r"bits sent", font_size=24, color=GREY_B), label(r"difference", font_size=24, color=GREY_B))
        rows = VGroup()
        for f in show:
            v = byf[fb.index(f)]
            rows.add(VGroup(label(rf"${f}$-bit counts", font_size=26),
                            MathTex(f"{v:,}".replace(",", "{,}"), font_size=30, color=C.BITS),
                            MathTex(f"{v - ideal:+,.1f}".replace(",", "{,}"), font_size=30,
                                    color=C.SURPRISE if v - ideal > 10 else GREY_A)))
        tab = VGroup(hdr, *rows)
        for j, x in enumerate((-3.6, 0.6, 3.6)):
            for r in tab:
                r[j].move_to([x, 0, 0], aligned_edge=RIGHT if j else LEFT)
        for i, r in enumerate(tab):
            for m in r:
                m.set_y(1.15 - 0.55 * i)
        tag = computed_tag()
        reg_note = label(rf"registers of ${rb[0]}$ to ${rb[-1]}$ bits, with $10$-bit counts: \ "
                         rf"${min(byr):,}$ to ${max(byr):,}$ bits".replace(",", "{,}"), font_size=24, color=GREY_A)
        reg_note.to_edge(DOWN, buff=0.4)
        fine = byf[fb.index(show[-1])] - ideal
        coarse = byf[fb.index(8)] - ideal if 8 in fb else None
        dips = [f for f in show if byf[fb.index(f)] < ideal]
        dip_said = (f"With {dips[0]}-bit counts it even came out a few bits under: rounding gave rare letters a "
                    "little more probability, and this passage happened to use them." if dips else "")
        coarse_said = f"Round them to 8 bits and it costs {coarse:,.0f} extra bits." if coarse is not None else ""
        with self.voiceover(
            f"Does the rounding cost much? We ran the whole Falcon passage, {n:,} letters, through a 32-bit coder "
            f"driven by our best counting model. <bookmark mark='a'/> Its information content under that model is "
            f"{ideal:,.0f} bits. <bookmark mark='b'/> With the probabilities rounded to {show[-1]}-bit counts, the "
            f"coder sent {fine:.1f} bits more than that, in the whole passage. {coarse_said} <bookmark mark='r'/> "
            f"{dip_said} <bookmark mark='c'/> The registers hardly matter, once they're a few bits wider than the "
            "counts. Arithmetic coding gives away almost nothing: what you pay is the model's surprise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hdr))
            vo.wait_until("a")
            self.play(FadeIn(info_l))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(reg_note))
        self.wait(0.3)
        self.clear_scene()
