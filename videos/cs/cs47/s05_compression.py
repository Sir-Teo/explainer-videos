from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs47.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, load, mono, tag_box


def _bits(s: str, colors, cell=0.3, size=15):
    """A bit string drawn as a row of small cells, one colour per bit."""
    g = VGroup()
    for ch, c in zip(s, colors):
        sq = Square(cell, stroke_color=c, stroke_width=1.2, fill_color=BG, fill_opacity=1)
        g.add(VGroup(sq, mono(ch, size=size, color=c).move_to(sq)))
    return g.arrange(RIGHT, buff=0.03)


def _two(a: str, b: str, ca=LAM, cb=DATA, size=17):
    """A code word in two coloured parts (prefix, then payload), set as one monospaced line."""
    parts = [mono(a, size=size, color=ca)] if a else []
    if b:
        parts.append(mono(b, size=size, color=cb))
    return VGroup(*parts).arrange(RIGHT, buff=0.02)


class Compression(VoiceoverScene):
    def construct(self):
        self.card()
        self.gaps()
        self.vbyte()
        self.elias()
        self.golomb()
        self.score()
        self.blocks()

    def card(self):
        card = chapter_card(4, r"Compressing postings", r"How do two million postings fit in a few megabytes?",
                            lit=(1966, 1975), extra=((1966, r"Golomb: \ run-length codes"),
                                                     (1975, r"Elias: \ universal codes")), part=PART)
        with self.voiceover("Chapter four. Compressing postings."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def gaps(self):
        ix = load("index")
        c = load("codes")
        ids = ix["sample"]["whale"]
        gp = [ids[0] + 1] + [b - a for a, b in zip(ids, ids[1:])]
        N, f = ix["docs"], ix["df"]["whale"]
        head = label(r"Store the gaps, \ not the ids", font_size=36).to_edge(UP, buff=0.3)
        t1 = label(rf"passages containing \texttt{{whale}}: \ the first twelve of {f}", font_size=20, color=DATA)
        top = VGroup(*[tag_box(str(d), color=DATA, size=20, w=0.9, h=0.56) for d in ids]).arrange(RIGHT, buff=0.12)
        bot = VGroup(*[tag_box(str(g), color=HEAD if g > 9 else YES, size=20, w=0.9, h=0.56) for g in gp]).arrange(
            RIGHT, buff=0.12)
        t1.next_to(head, DOWN, buff=0.45)
        top.next_to(t1, DOWN, buff=0.25)
        bot.next_to(top, DOWN, buff=0.9)
        arrows = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.06, stroke_width=2, color=GREY_C,
                                max_tip_length_to_length_ratio=0.25) for a, b in zip(top, bot)])
        t2 = label(r"gaps: \ the first id plus one, \ then the differences between neighbours", font_size=20,
                   color=YES).next_to(bot, DOWN, buff=0.25)
        notes = VGroup(
            wrapped_label(rf"{c['postings']:,} postings as 32-bit integers: \ "
                          rf"{c['bits']['raw32'] / 8 / 1e6:.1f} MB of document ids", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(rf"a term in $f$ of $N$ passages has gaps averaging $N/f$: \ for \texttt{{whale}}, \ "
                          rf"{N:,}/{f} $\approx$ {N / f:.1f}", 12.4, font_size=20, color=DATA),
            wrapped_label(r"frequent terms have short gaps; \ rare terms have long gaps, \ but few of them: \ so give "
                          r"small numbers short codes", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(t2, DOWN, buff=0.8)
        notes.set_x(0)
        with self.voiceover(
            "Chapter two's index holds two point three six million postings: as thirty-two-bit integers, nine and a "
            "half megabytes of document ids, and a web index holds vastly more. <bookmark mark='a'/> Here are the "
            "first twelve passages that contain whale. <bookmark mark='b'/> The list is sorted, so store the "
            "differences between neighbours instead: the gaps. The first is the id plus one, since our codes start at "
            "one. <bookmark mark='c'/> A term in f of N passages has gaps averaging N over f: for whale, about "
            "twenty-nine. Frequent terms have short gaps; rare terms have long ones, but few. So give small numbers "
            "short codes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(t1), LaggedStart(*[FadeIn(b) for b in top], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08),
                      LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in bot], lag_ratio=0.08), run_time=2)
            self.play(FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def vbyte(self):
        c = load("codes")
        ix = load("index")
        first = ix["sample"]["whale"][0] + 1

        def vb(g):
            groups = []
            while True:
                groups.insert(0, g & 127)
                g >>= 7
                if not g:
                    break
            return [("1" if i == len(groups) - 1 else "0") + format(x, "07b") for i, x in enumerate(groups)]
        head = label(r"Variable byte", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        for g in (1, 5, first):
            bytes_ = VGroup(*[_bits(b, [HEAD] + [DATA] * 7, cell=0.33, size=16) for b in vb(g)])
            bytes_.arrange(RIGHT, buff=0.18)
            name = VGroup(label(rf"gap {g}", font_size=20, color=WHITE),
                          label(rf"{len(vb(g))} byte" + ("s" if len(vb(g)) > 1 else ""), font_size=17,
                                color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            rows.add(VGroup(name, bytes_))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.3)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        for r in rows[1:]:
            r[1].align_to(rows[0][1], LEFT)
        legend = VGroup(
            VGroup(Square(0.22, stroke_color=HEAD, stroke_width=1.5), label(r"flag: \ the last byte?", font_size=17,
                                                                            color=HEAD)).arrange(RIGHT, buff=0.12),
            VGroup(Square(0.22, stroke_color=DATA, stroke_width=1.5), label(r"seven bits of the gap", font_size=17,
                                                                            color=DATA)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.5)
        left = VGroup(legend, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.8).next_to(head, DOWN, buff=0.9)
        left.to_edge(LEFT, buff=0.35)
        bpp = c["bits_per_posting"]
        notes = VGroup(
            wrapped_label(rf"{first} has {first.bit_length()} binary digits, \ more than seven: \ two bytes", 5.3,
                          font_size=19, color=WHITE),
            wrapped_label(rf"over the whole index: \ {bpp['vbyte']:.2f} bits per posting, \ against 32", 5.3,
                          font_size=19, color=YES),
            wrapped_label(r"every code ends on a byte boundary, \ so decoding is a mask, \ a shift and a test: \ fast; "
                          r"\ the same varint is in Lucene's file formats and in protocol buffers", 5.3,
                          font_size=19, color=GREY_A),
            wrapped_label(r"but a gap of 1 still costs 8 bits", 5.3, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        notes.next_to(head, DOWN, buff=0.9).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The simplest code works in whole bytes. <bookmark mark='a'/> Each byte carries seven bits of the gap and "
            "a flag that marks the last byte. <bookmark mark='b'/> One and five fit in a byte; six hundred and sixty "
            "has ten binary digits, so it takes two. <bookmark mark='c'/> Over the index: eight point "
            "six seven bits a posting, about a quarter of thirty-two. Decoding is a mask, a shift and a test, so it "
            "is fast. <bookmark mark='d'/> But a gap "
            "of one still costs eight bits."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(legend), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]), Indicate(rows[0][1], color=NO))
        self.wait(0.4)
        self.clear_scene()

    def elias(self):
        c = load("codes")
        sm = c["samples"]
        bpp = c["bits_per_posting"]
        head = label(r"Elias's $\gamma$ and $\delta$ codes", font_size=36).to_edge(UP, buff=0.3)
        gs = [int(g) for g in sm]
        xs = {"g": -6.3, "bin": -5.75, "gamma": -4.25, "delta": -2.2}
        hdr = VGroup(label(r"$g$", font_size=19, color=GREY_B).move_to([xs["g"], 0, 0]),
                     label(r"binary", font_size=19, color=GREY_B),
                     label(r"$\gamma$", font_size=19, color=GREY_B), label(r"$\delta$", font_size=19, color=GREY_B))
        for m, k in zip(hdr[1:], ("bin", "gamma", "delta")):
            m.move_to([0, 0, 0]).align_to([xs[k], 0, 0], LEFT)
        rows = VGroup()
        for g in gs:
            b = bin(g)[2:]
            ga, de = sm[str(g)]["gamma"], sm[str(g)]["delta"]
            cut = len(de) - (len(b) - 1)
            r = VGroup(label(f"{g}", font_size=19, color=WHITE).move_to([xs["g"], 0, 0]),
                       mono(b, size=17, color=GREY_A),
                       _two(ga[:len(b) - 1], ga[len(b) - 1:]),
                       _two(de[:cut], de[cut:]))
            for m, k in zip(r[1:], ("bin", "gamma", "delta")):
                m.move_to([0, 0, 0]).align_to([xs[k], 0, 0], LEFT)
            rows.add(r)
        table = VGroup(hdr, *rows)
        for i, r in enumerate(table):
            r.shift(UP * (2.3 - 0.46 * i))
        rule = Line([-6.6, 2.07, 0], [-0.4, 2.07, 0], color=GREY_D, stroke_width=1.5)
        key = VGroup(label(r"prefix: \ how many digits", font_size=17, color=LAM),
                     label(r"payload: \ the digits", font_size=17, color=DATA)).arrange(RIGHT, buff=0.4)
        key.next_to(rows, DOWN, buff=0.35).align_to(rule, LEFT)
        W = 6.3
        right = VGroup(
            wrapped_label(r"$g$ has $\lfloor \log_2 g \rfloor + 1$ binary digits, \ and the first is always 1", W,
                          font_size=20, color=WHITE),
            MathTex(r"|\gamma(g)| = 2\lfloor \log_2 g \rfloor + 1", font_size=34, color=DATA),
            wrapped_label(r"$\gamma$: \ the count of digits after the first, \ as zeros, \ then the digits", W,
                          font_size=19, color=GREY_B),
            wrapped_label(r"a code spending $L$ bits on a value is ideal when its probability is $2^{-L}$ \ (Kraft; "
                          r"\ \textit{AI, Built} Part 1): \ $\gamma$ is ideal for $P(g) \approx 1/(2g^2)$", W,
                          font_size=19, color=HEAD),
            MathTex(r"|\delta(g)| = \lfloor \log_2 g \rfloor + 2\lfloor \log_2(\lfloor \log_2 g \rfloor + 1) "
                    r"\rfloor + 1", font_size=28, color=DATA),
            wrapped_label(r"$\delta$: \ the number of digits in $\gamma$, \ then the digits after the leading 1", W,
                          font_size=19, color=GREY_B),
            wrapped_label(rf"on our index: \ $\gamma$ {bpp['gamma']:.2f} \ and $\delta$ {bpp['delta']:.2f} bits per "
                          r"posting", W, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        if right[4].width > W:
            right[4].width = W
        right.next_to(head, DOWN, buff=0.45).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Now we write bits. <bookmark mark='a'/> A gap g has floor of log two g, plus one, binary "
            "digits, the first always a one. <bookmark mark='b'/> Peter Elias's gamma code, from 1975, writes how "
            "many digits follow the first, as zeros, then the digits: twice floor log g, plus one, bits. Thirteen for "
            "a hundred. <bookmark mark='c'/> Part 1 of AI, Built showed that spending L bits on a value is ideal when "
            "its probability is two to the minus L. So gamma suits gaps that fall off like one over g squared. "
            "<bookmark mark='d'/> The delta code writes the digit count itself in gamma: eleven bits for a hundred. "
            "On our index, gamma spends five point six four bits a posting, and delta five point five four."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr[0]), FadeIn(hdr[1]), Create(rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r[0], r[1])) for r in rows], lag_ratio=0.15), FadeIn(right[0]),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(hdr[2]), LaggedStart(*[FadeIn(r[2]) for r in rows], lag_ratio=0.15), FadeIn(key),
                      run_time=1.5)
            self.play(Write(right[1]), FadeIn(right[2]))
            vo.wait_until("c")
            self.play(FadeIn(right[3]))
            vo.wait_until("d")
            self.play(FadeIn(hdr[3]), LaggedStart(*[FadeIn(r[3]) for r in rows], lag_ratio=0.15), run_time=1.5)
            self.play(Write(right[4]), FadeIn(right[5]))
            self.play(FadeIn(right[6]))
        self.wait(0.4)
        self.clear_scene()

    def golomb(self):
        ix = load("index")
        N, f = ix["docs"], ix["df"]["whale"]
        p = f / N
        M_exact = math.log(2) / -math.log(1 - p)
        M = int(round(M_exact))
        k = max(0, int(math.log2(max(1.0, 0.69 * N / f))))
        head = label(r"Golomb codes: \ the best parameter", font_size=36).to_edge(UP, buff=0.3)
        G = 3 * M
        x0, wid, h0 = -6.5, 5.9, 2.6
        bw = wid / G
        base_y = -0.9
        bars = VGroup()
        for g in range(1, G + 1):
            q = (g - 1) // M
            h = h0 * (1 - p) ** (g - 1)
            bars.add(Rectangle(width=bw * 0.85, height=h, stroke_width=0, fill_color=(DATA, LAM, KERN)[q],
                               fill_opacity=0.85).move_to([x0 + (g - 0.5) * bw, base_y + h / 2, 0]))
        axis = Line([x0, base_y, 0], [x0 + wid, base_y, 0], color=GREY_C, stroke_width=1.5)
        ticks = VGroup(*[label(f"{g}", font_size=16, color=GREY_B).next_to([x0 + (g - 0.5) * bw, base_y, 0], DOWN,
                                                                         buff=0.1) for g in (1, M + 1, 2 * M + 1)])
        masses = VGroup()
        for q in range(3):
            m = (1 - p) ** (q * M) * (1 - (1 - p) ** M)
            xc = x0 + (q + 0.5) * M * bw
            masses.add(label(rf"$q = {q}$: \ {m:.2f}", font_size=18, color=(DATA, LAM, KERN)[q]).move_to(
                [xc, base_y + h0 * (1 - p) ** (q * M) + 0.35, 0]))
        cap = wrapped_label(rf"gaps of \texttt{{whale}} if each passage holds it independently, \ $p = {f}/{format(N, ',').replace(',', '{,}')}$, "
                            rf"\ in blocks of $M = {M}$: \ each block holds about half the one before", 5.9,
                            font_size=18, color=GREY_A).next_to(axis, DOWN, buff=0.5).align_to(axis, LEFT)
        ill = note(r"the geometric model, \ not the measured gaps", font_size=17).next_to(cap, DOWN, buff=0.15)
        ill.align_to(cap, LEFT)
        W = 6.0
        steps = VGroup(
            wrapped_label(r"$P(g) = (1-p)^{g-1}\,p$, \ $p = f/N$: \ each passage holds the term independently", W,
                          font_size=19, color=WHITE),
            wrapped_label(r"write $g - 1 = qM + r$: \ $q$ in unary, \ $r$ in binary \ (Golomb, \ 1966)", W,
                          font_size=19, color=WHITE),
            wrapped_label(r"$P(q) \propto \big((1-p)^M\big)^q$: \ the quotient is geometric too", W, font_size=19,
                          color=LAM),
            wrapped_label(r"unary spends one more bit per step, \ so it is ideal when each step halves the "
                          r"probability: \ $(1-p)^M = \tfrac12$", W, font_size=19, color=HEAD),
            wrapped_label(rf"$M = \dfrac{{\ln 2}}{{-\ln(1-p)}} \approx 0.69\,\dfrac{{N}}{{f}}$: \ for "
                          rf"\texttt{{whale}}, \ {M_exact:.1f}", W, font_size=19, color=YES),
            wrapped_label(rf"Rice codes take $M = 2^k$, \ so $r$ is exactly $k$ bits: \ "
                          rf"$k = \lfloor \log_2 (0.69\,N/f) \rfloor = {k}$ here, \ one $k$ per list", W,
                          font_size=19, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        steps.next_to(head, DOWN, buff=0.5).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "But we know each list's length, so fit the code to it. <bookmark mark='a'/> If each passage "
            "holds a term independently, with probability p equal to f over N, gaps are geometric. <bookmark "
            "mark='b'/> Solomon Golomb's code of 1966 divides g minus one by a parameter M: the quotient in unary, "
            "the remainder in binary. <bookmark mark='c'/> The quotient is geometric too, and unary, one more bit per "
            "step, is ideal when each step halves the probability. <bookmark mark='d'/> So set one minus p, to the "
            "power M, to one half: M is about point six nine times the mean gap, near twenty for whale. <bookmark "
            "mark='e'/> Rice rounds M down to a power of two, so the remainder takes exactly k bits: here, four."
        ) as vo:
            self.play(FadeIn(head), Create(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(steps[0]),
                      FadeIn(ticks), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(masses), FadeIn(cap), FadeIn(ill), FadeIn(steps[2]))
            self.play(FadeIn(steps[3]))
            vo.wait_until("d")
            self.play(FadeIn(steps[4]))
            vo.wait_until("e")
            self.play(FadeIn(steps[5]))
        self.wait(0.4)
        self.clear_scene()

    def score(self):
        c = load("codes")
        bnd = load("bound")
        sm = c["samples"]
        bpp = c["bits_per_posting"]
        head = label(r"How close to the limit?", font_size=36).to_edge(UP, buff=0.3)
        k = 2
        rows = VGroup()
        for g in (1, 2, 3, 4, 5, 9, 17):
            code = sm[str(g)]["rice2"]
            rows.add(VGroup(label(f"{g}", font_size=19, color=WHITE), _two(code[:-k], code[-k:])))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.4)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        for r in rows:
            r[1].align_to(rows[0][1], LEFT)
        ttl = wrapped_label(r"Rice codes, \ $k = 2$: \ $q$ as ones and a zero, \ then $r$ in two bits", 4.6,
                            font_size=19, color=GREY_A)
        left = VGroup(ttl, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.55)
        left.to_edge(LEFT, buff=0.5)
        vals = [bpp["vbyte"], bpp["gamma"], bpp["delta"], bpp["rice"], bnd["bound_bits_per_posting"]]
        names = [r"vbyte", r"$\gamma$", r"$\delta$", r"Rice", r"bound"]
        chart = bar_chart(vals, names, [GREY_B, LAM, LAM, YES, HEAD], height=3.2, bar_w=0.8, gap=0.45, vmax=9.0,
                          fmt_=lambda v: f"{v:.2f}", font_size=19)
        chart.next_to(head, DOWN, buff=0.9).shift(RIGHT * 2.3)
        ylab = label(r"bits per posting \ (32-bit integers: \ 32)", font_size=18, color=GREY_A).next_to(chart, UP,
                                                                                                          buff=0.25)
        foot = wrapped_label(r"the bound: \ choosing which $f$ of $N$ passages hold a term carries "
                             r"$\log_2 \binom{N}{f}$ bits; \ no code that ignores how postings cluster can do better",
                             7.4, font_size=19, color=HEAD).next_to(chart, DOWN, buff=0.45)
        foot.set_x(chart.get_x())
        with self.voiceover(
            "Here are Rice codes with k equal to two. <bookmark mark='a'/> Gaps of one to four take three bits, and "
            "each further four adds a single one. <bookmark mark='b'/> With its own k for every list, Rice spends "
            "four point nine six bits a posting over the whole index. <bookmark mark='c'/> And "
            "there is a floor. Choosing which f of N passages hold a term carries log of N choose f bits: four point "
            "seven four a posting here. Rice comes within five percent of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ttl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(ylab), Create(chart[0]), *[GrowFromEdge(b, DOWN) for b in chart.bars[:4]],
                      FadeIn(chart.vals[:4]), FadeIn(chart.names[:4]))
            vo.wait_until("c")
            self.play(GrowFromEdge(chart.bars[4], DOWN), FadeIn(chart.vals[4]), FadeIn(chart.names[4]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def blocks(self):
        head = label(r"Block codecs and SIMD", font_size=36).to_edge(UP, buff=0.3)
        gaps = [3, 1, 6, 2, 1, 5, 1, 4]
        b = max(gaps).bit_length()
        cells = VGroup(*[tag_box(str(g), color=DATA, size=18, w=0.6) for g in gaps]).arrange(RIGHT, buff=0.1)
        t1 = label(rf"a block of gaps \ (illustrative): \ the largest needs {b} bits", font_size=20, color=GREY_A)
        packed = VGroup(*[_bits(format(g, f"0{b}b"), [YES] * b, cell=0.3) for g in gaps]).arrange(RIGHT, buff=0.1)
        t2 = label(rf"so every gap gets {b} bits, \ packed side by side: \ no flags, \ no unary, \ no branches",
                   font_size=20, color=YES)
        lanes = VGroup()
        for i in range(4):
            r = RoundedRectangle(width=2.3, height=0.55, corner_radius=0.08, stroke_color=KERN, stroke_width=1.6,
                                 fill_color=BG, fill_opacity=1)
            lanes.add(VGroup(r, label(rf"lane {i + 1}: \ {gaps[i]}", font_size=18, color=KERN).move_to(r)))
        lanes.arrange(RIGHT, buff=0.15)
        t3 = label(r"one SIMD instruction unpacks four gaps at once \ (Part 24)", font_size=20, color=KERN)
        VGroup(t1, cells, t2, packed, t3, lanes).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.5)
        notes = VGroup(
            wrapped_label(r"PForDelta \ (Zukowski et al., \ 2006): \ pick the width for most of the block, \ and "
                          r"store the few large gaps separately as exceptions", 6.0, font_size=19, color=WHITE),
            wrapped_label(r"SIMD-BP128 \ (Lemire \& Boytsov, \ 2015): \ blocks of 128 gaps, \ ``decoding billions "
                          r"of integers per second''", 6.0, font_size=19, color=WHITE),
        ).arrange(RIGHT, buff=0.4, aligned_edge=UP).next_to(lanes, DOWN, buff=0.7)
        with self.voiceover(
            "Rice codes decode one bit at a time, through branches, so modern engines trade a few bits for speed. "
            "<bookmark mark='a'/> Take a block of gaps and find the widest. <bookmark mark='b'/> Give every gap that "
            "many bits, packed side by side: no flags, no unary, no branches. <bookmark mark='c'/> Then the SIMD "
            "instructions of Part 24 unpack four gaps at once. <bookmark mark='d'/> PForDelta, from 2006, stores the "
            "rare large gaps as exceptions, and Lemire and Boytsov's codecs of 2015 decode billions of integers a "
            "second."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t1), LaggedStart(*[FadeIn(cl) for cl in cells], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(t2), LaggedStart(*[FadeIn(p) for p in packed], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(t3), LaggedStart(*[FadeIn(ln) for ln in lanes], lag_ratio=0.15))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (HEAD, NO)
