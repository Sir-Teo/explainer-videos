from __future__ import annotations


import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import ALPHA27, MONO, area_slivers, code_tree, letter, letter_row, load

SMALL = {"a": "0", "b": "10", "c": "110", "d": "1110", "e": "11110", "f": "11111"}


def dyadic(code: str) -> tuple[float, float]:
    """The interval [0.c, 0.c + 2^-len) of binary fractions that start with the codeword c."""
    lo = int(code, 2) / 2 ** len(code) if code else 0.0
    return lo, lo + 2.0 ** -len(code)


class Codes(VoiceoverScene):
    def construct(self):
        self.card()
        self.fixed()
        self.prefix()
        self.kraft()
        self.bound()
        self.huffman()
        self.theorem()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"Codes, and the limit Shannon proved", r"How few bits can a message take?",
                            lit=(1948, 1952), part=1)
        with self.voiceover("Chapter four. Surprise is measured in bits. So let's spend some bits.") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def fixed(self):
        hf = load("huffman")
        word = hf["word"]
        assert word == "the falcon" and hf["fixed_bits"] == 50
        head = label(r"A fixed-length code: \ $2^5 = 32 \ge 27$, \ so $5$ bits per symbol", font_size=34)
        head.to_edge(UP, buff=0.45)
        table = VGroup()
        for c in " abcdez":
            i = ALPHA27.index(c)
            row = VGroup(letter(c, font_size=28), Text(format(i, "05b"), font=MONO, font_size=26, color=C.BITS))
            row.arrange(RIGHT, buff=0.4)
            table.add(row)
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(LEFT * 4.6 + DOWN * 0.3)
        dots = MathTex(r"\vdots", font_size=30, color=GREY_B).next_to(table[-2], DOWN, buff=0.05)
        table[-1].next_to(dots, DOWN, buff=0.05).align_to(table[0], LEFT)
        w = letter_row(word, font_size=34).move_to(RIGHT * 1.6 + UP * 0.9)
        codes = VGroup(*[Text(format(ALPHA27.index(c), "05b"), font=MONO, font_size=20, color=C.BITS)
                         for c in word])
        codes.arrange(RIGHT, buff=0.12).next_to(w, DOWN, buff=0.5)
        if codes.width > 8.4:
            codes.width = 8.4
        tot = label(r"$10$ symbols $\times\ 5$ bits $= 50$ bits", font_size=32).next_to(codes, DOWN, buff=0.5)
        waste = label(r"but \texttt{e} is almost $200$ times more common than \texttt{z}", font_size=28, color=C.SURPRISE)
        waste.next_to(tot, DOWN, buff=0.4)
        with self.voiceover(
            "The simplest way to send letters as bits is a fixed-length code. Two to the five is thirty-two, enough "
            "for our twenty-seven symbols, <bookmark mark='a'/> so give each one a five-bit number. "
            "<bookmark mark='b'/> The falcon, ten symbols, costs fifty bits. <bookmark mark='c'/> But that's "
            "wasteful: e is almost two hundred times more common than z, and both cost five bits."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in table[:-1]], lag_ratio=0.15), FadeIn(dots), FadeIn(table[-1]))
            vo.wait_until("b")
            self.play(FadeIn(w), LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in codes], lag_ratio=0.12))
            self.play(FadeIn(tot))
            vo.wait_until("c")
            self.play(FadeIn(waste))
        p = load("letters")["p"]
        assert 180 < p[ALPHA27.index("e")] / p[ALPHA27.index("z")] < 200
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prefix(self):
        head = label(r"Variable length: \ short codewords for common symbols", font_size=34).to_edge(UP, buff=0.45)
        bad = VGroup(
            Text("e = 0    t = 1    a = 01", font=MONO, font_size=28, color=WHITE),
            Text("01  ->  'e t'  or  'a' ?", font=MONO, font_size=28, color=C.SURPRISE),
        ).arrange(DOWN, buff=0.3).move_to(UP * 1.4)
        rule = label(r"\textit{prefix-free}: \ no codeword is the start of another", font_size=32, color=C.BITS)
        rule.move_to(UP * 0.0)
        tree = code_tree(SMALL, x_range=(-3.0, 3.0), y_top=-0.6, dy=0.55, leaf_font=26)
        tree.shift(DOWN * 0.1)
        legend = VGroup(*[VGroup(letter(s, font_size=26), Text(c, font=MONO, font_size=24, color=C.BITS))
                          .arrange(RIGHT, buff=0.3) for s, c in SMALL.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend.move_to(RIGHT * 5.0 + DOWN * 1.7)
        with self.voiceover(
            "So give common symbols short codewords, like Morse code, which gives e a single dot. But careful. "
            "<bookmark mark='a'/> If e is zero, t is one, and a is zero one, then the bits zero one could be e, t, or "
            "a. <bookmark mark='b'/> The fix is a prefix-free code: no codeword is the start of another. "
            "<bookmark mark='c'/> Then the codewords are the leaves of a binary tree. Zero goes left, one goes right, "
            "and to decode, you walk down from the top until you reach a leaf."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bad[0]))
            self.play(FadeIn(bad[1]))
            vo.wait_until("b")
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeOut(bad), rule.animate.next_to(head, DOWN, buff=0.3))
            self.play(Create(tree[0]), FadeIn(tree[1]), FadeIn(tree[2]), run_time=1.8)
            self.play(FadeIn(tree[3]), FadeIn(legend))
        # decode a bit string by walking the tree
        msg = "110" + "0" + "10" + "11111"
        assert msg == SMALL["c"] + SMALL["a"] + SMALL["b"] + SMALL["f"]
        bits = Text(msg, font=MONO, font_size=34, color=C.BITS).next_to(rule, DOWN, buff=0.4)
        out = VGroup()
        with self.voiceover(
            "Watch it decode one, one, zero, zero, one, zero, one, one, one, one, one. Right, right, left: that's "
            "c. Start again at the top. Left: a. Right, left: b. Right five times: f. No separators needed."
        ) as vo:
            self.play(FadeIn(bits))
            pos = 0
            for sym in "cabf":
                c = SMALL[sym]
                path = VGroup(*[tree.edges[c[:k + 1]].copy().set_stroke(WHITE, 6) for k in range(len(c))])
                self.play(*[bits[pos + k].animate.set_color(WHITE) for k in range(len(c))],
                          LaggedStart(*[Create(e) for e in path], lag_ratio=0.6), run_time=0.4 + 0.25 * len(c))
                o = letter(sym, font_size=34, color=C.TRUE_P)
                out.add(o)
                out.arrange(RIGHT, buff=0.15).next_to(bits, RIGHT, buff=0.6)
                self.play(FadeIn(o), Indicate(tree.leaves[sym], color=C.TRUE_P), FadeOut(path), run_time=0.6)
                pos += len(c)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kraft(self):
        W, y_bar = 12.0, -2.4
        L = -W / 2
        # nodes placed at the midpoints of their dyadic intervals, so the tree sits right above its intervals
        pos = {}
        for c in SMALL.values():
            for k in range(len(c) + 1):
                pre = c[:k]
                a, b = dyadic(pre)
                pos[pre] = np.array([L + W * (a + b) / 2, 2.4 - 0.75 * len(pre), 0.0])
        edges = VGroup(*[Line(pos[pre[:-1]], pos[pre], color=C.BIT0 if pre[-1] == "0" else C.BIT1, stroke_width=3)
                         for pre in pos if pre])
        nodes = VGroup(*[Dot(p_, radius=0.05, color=GREY_A) for p_ in pos.values()])
        leaves = VGroup()
        ivs, drops, wl = VGroup(), VGroup(), VGroup()
        palette = [C.TRUE_P, C.MODEL_Q, C.INTERVAL, C.CONTEXT, C.SURPRISE, C.BITS]
        for (s, c), col in zip(SMALL.items(), palette):
            a, b = dyadic(c)
            leaves.add(letter(s, font_size=26, color=col).next_to(pos[c], DOWN, buff=0.12))
            r = Rectangle(width=W * (b - a), height=0.45, stroke_width=1.5, stroke_color=BACKGROUND, fill_color=col,
                          fill_opacity=0.85).move_to([L + W * (a + b) / 2, y_bar, 0])
            ivs.add(r)
            drops.add(DashedLine(pos[c] + DOWN * 0.45, r.get_top(), color=col, stroke_width=1.5, dash_length=0.08))
            wl.add(MathTex(rf"2^{{-{len(c)}}}", font_size=22 if len(c) < 4 else 15, color=BLACK).move_to(r))
        ends = VGroup(MathTex("0", font_size=26, color=GREY_B).next_to(ivs[0], DOWN, buff=0.15).align_to(ivs[0], LEFT),
                      MathTex("1", font_size=26, color=GREY_B).next_to(ivs[-1], DOWN, buff=0.15).align_to(ivs[-1], RIGHT))
        kr = mtex(r"\sum_i 2^{-\ell_i} \le 1", font_size=44, color=C.BITS).to_corner(UL, buff=0.5)
        kn = label(r"Kraft's inequality (1949)", font_size=24, color=GREY_A).next_to(kr, DOWN, buff=0.15)
        kn.align_to(kr, LEFT)
        with self.voiceover(
            "Prefix-free codes obey one budget, and there's a beautiful way to see it. Read a codeword as the start "
            "of a binary fraction: a number between zero and one, written in halves, where each digit says whether "
            "to keep the left half of what's left, for zero, or the right half, for one. <bookmark mark='a'/> The "
            "codeword one, one, zero: right half, right half again, then left. It stands for all the numbers "
            "between zero and one whose binary expansion begins point one one zero: an interval of width two to "
            "the minus three. <bookmark mark='b'/> A codeword of length l claims an interval of width two to the "
            "minus l."
        ) as vo:
            self.play(Create(edges), FadeIn(nodes), FadeIn(leaves), run_time=2.0)
            vo.wait_until("a")
            # halving [0, 1] three times: 1 = the right half, 1 = its right half, 0 = that one's left half
            unit = Rectangle(width=W, height=0.45, stroke_width=1.5, stroke_color=GREY_B).move_to([0, y_bar, 0])
            half = Rectangle(width=W, height=0.45, stroke_width=3, stroke_color=C.BITS, fill_color=C.BITS,
                             fill_opacity=0.18).move_to([0, y_bar, 0])
            self.play(Create(unit), FadeIn(half), FadeIn(ends), run_time=0.6)
            halv = mtex(r"0.110_2 = \tfrac12 + \tfrac14 + 0 \cdot \tfrac18", font_size=30, color=C.BITS)
            halv.to_edge(DOWN, buff=0.2)
            lo, w = 0.0, 1.0
            for bit in "110":
                w /= 2
                lo += w if bit == "1" else 0.0
                self.play(half.animate.stretch_to_fit_width(W * w).move_to([L + W * (lo + w / 2), y_bar, 0]),
                          run_time=0.5)
            self.play(FadeIn(halv), run_time=0.4)
            self.play(FadeOut(half), Create(drops[2]), FadeIn(ivs[2]), FadeIn(wl[2]))
            vo.wait_until("b")
            self.play(*[Create(d) for i, d in enumerate(drops) if i != 2],
                      *[FadeIn(r) for i, r in enumerate(ivs) if i != 2],
                      *[FadeIn(t) for i, t in enumerate(wl) if i != 2], run_time=1.5)
        with self.voiceover(
            "Because no codeword starts another, these intervals never overlap, and they all fit between zero and "
            "one. So their widths add up to at most one. <bookmark mark='a'/> That's Kraft's inequality: two to the "
            "minus length, summed over the codewords, is at most one. Short codewords are expensive: one bit "
            "uses up half the budget."
        ) as vo:
            self.play(Indicate(ivs, color=WHITE, scale_factor=1.03), run_time=1.5)
            vo.wait_until("a")
            self.play(Write(kr), FadeIn(kn))
            self.play(Indicate(ivs[0], color=WHITE), Indicate(wl[0], color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bound(self):
        hf = load("huffman")
        lt = load("letters")
        p, order = lt["p"], list(lt["order"])
        H = float(lt["H"])
        W, y0, sc = 11.4, -3.25, 0.25
        sky = area_slivers(p, W=W, y0=y0, scale=sc, order=order, color=C.SURPRISE, opacity=0.85)
        base = Line([-W / 2, y0, 0], [W / 2, y0, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"No prefix code beats the entropy", font_size=36).to_edge(UP, buff=0.35)
        setup = mtex(r"L = \sum_i p_i\, \ell_i \quad \text{(average length)}, \qquad H = \sum_i p_i \log_2 \tfrac{1}{p_i}",
                     font_size=32, color=GREY_A).next_to(head, DOWN, buff=0.3)
        colors = {r"p_i": C.TRUE_P, r"2^{-\ell_i}": C.BITS, "1": C.BITS}
        steps = [
            ["H - L", "=", r"\sum_i", r"p_i", r"\log_2", r"\frac{2^{-\ell_i}}{p_i}"],
            ["H - L", r"\le", r"\log_2", r"\sum_i", r"p_i", r"\frac{2^{-\ell_i}}{p_i}"],
            ["H - L", r"\le", r"\log_2", r"\sum_i", r"2^{-\ell_i}"],
            ["H - L", r"\le", r"\log_2", "1", "= 0"],
        ]
        eqs = [cmath(*st, colors=colors, font_size=50).move_to(UP * 1.25) for st in steps]
        whys = [why(r"combine the two sums"), why(r"Jensen, as in Chapter 3"), why(r"the $p_i$ cancel"),
                why(r"Kraft")]
        for w in whys:
            w.scale(1.15).move_to(UP * 0.3)
        res = label(r"$L \ge H$, \ with equality only if every $\ell_i = \log_2 \frac{1}{p_i}$", font_size=34,
                    color=C.BITS).move_to(UP * 1.25)
        h_lab = MathTex(rf"H = {H:.2f}", font_size=34, color=C.SURPRISE).move_to([-4.3, -1.6, 0])
        with self.voiceover(
            "Now we can prove a speed limit. Let L be the average codeword length, and H the entropy. "
            "<bookmark mark='a'/> Write their difference as one sum. <bookmark mark='b'/> Jensen's inequality, "
            "exactly as in chapter three, moves the log outside. <bookmark mark='c'/> The probabilities cancel, "
            "<bookmark mark='d'/> and Kraft's inequality says what's left is at most log one: zero. "
            "<bookmark mark='e'/> So the average length can never be less than the entropy, and it equals the "
            "entropy only if each symbol gets exactly log one over p bits: its surprise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(setup), Create(base),
                      LaggedStart(*[GrowFromEdge(sky[i], DOWN) for i in order], lag_ratio=0.03), run_time=1.8)
            self.play(FadeIn(h_lab))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(whys[0]))
            for k, mark in enumerate("bcd"):
                vo.wait_until(mark)
                self.play(FadeOut(whys[k]), FadeIn(whys[k + 1]), run_time=0.4)
                morph(self, eqs[k], eqs[k + 1], run_time=1.2, path_arc=-0.6 if k == 0 else 0.0)
            vo.wait_until("e")
            self.play(FadeOut(whys[3]), eqs[3].animate.scale(0.7).move_to(UP * 2.0), FadeIn(res, shift=DOWN * 0.1))
        # rounding the surprises up to whole bits: Shannon's code
        ell = np.ceil(-np.log2(p))
        Ls = float((p * ell).sum())
        assert abs(Ls - hf["L_shannon"]) < 1e-9 and abs(hf["L_shannon"] - 4.62) < 0.005
        steps_up, cum = {}, 0.0
        for i in order:
            h = sc * ell[i]
            steps_up[i] = Rectangle(width=max(W * p[i], 0.003), height=h, stroke_width=1.2, stroke_color=C.BITS,
                                    fill_color=C.BITS, fill_opacity=0.3).move_to([-W / 2 + (cum + p[i] / 2) * W, y0 + h / 2, 0])
            cum += p[i]
        stair = VGroup(*[steps_up[i] for i in order])
        l_lab = MathTex(rf"L = {Ls:.2f}", font_size=34, color=C.BITS).next_to(h_lab, UP, buff=0.2).align_to(h_lab, LEFT)
        sh = label(rf"round up, $\ell_i = \lceil \log_2 \frac{{1}}{{p_i}} \rceil$: \ still within Kraft, \ "
                   rf"$H \le L < H + 1$. \ Letters: ${hf['L_shannon']:.2f}$ bits", font_size=28, color=GREY_A)
        sh.next_to(res, DOWN, buff=0.35)
        with self.voiceover(
            "Codeword lengths must be whole numbers, so round the surprises up. That still fits Kraft's budget, "
            "and it costs less than one extra bit per symbol. For our letters, 4.62 bits."
        ) as vo:
            self.add(stair)
            self.bring_to_front(sky)
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in stair], lag_ratio=0.04), run_time=2.0)
            self.play(FadeIn(l_lab), FadeIn(sh))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def huffman(self):
        hf = load("huffman")
        codes = {ALPHA27[i]: c for i, c in enumerate(hf["codes"])}
        merges = [list(map(float, m)) for m in hf["merges"]]
        children = {int(m[2]): (int(m[0]), int(m[1])) for m in merges}
        prefix = {int(hf["root"]): ""}
        stack = [int(hf["root"])]
        while stack:
            n = stack.pop()
            if n in children:
                a, b = children[n]
                prefix[a], prefix[b] = prefix[n] + "0", prefix[n] + "1"
                stack += [a, b]
        assert all(prefix[i] == codes[ALPHA27[i]] for i in range(27))
        tree = code_tree(codes, x_range=(-6.5, 6.5), y_top=2.2, dy=0.43, leaf_font=20, show_bits=False,
                         edge_width=2.2, dot_r=0.035)
        head = label(r"Huffman's algorithm (1952): \ merge the two least likely, repeat", font_size=32)
        head.to_edge(UP, buff=0.3)
        first = merges[0]
        assert {ALPHA27[int(first[0])], ALPHA27[int(first[1])]} == {"z", "q"}
        side = VGroup(*[MathTex(rf"\texttt{{{ALPHA27[int(m[0])] if m[0] < 27 else '*'}}} + "
                                rf"\texttt{{{ALPHA27[int(m[1])] if m[1] < 27 else '*'}}} \to {m[3]:.4f}", font_size=24,
                                color=GREY_A) for m in merges[:3]])
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.45)
        with self.voiceover(
            "Which code gets closest? In 1952, David Huffman, then a graduate student, found the answer. "
            "<bookmark mark='a'/> Take the two least likely symbols, z and q, and join them under a new node whose "
            "probability is their sum. Then do it again with the two least likely of what's left, and again, "
            "<bookmark mark='b'/> twenty-six times, until one tree holds everything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tree.leaves.values())))
            vo.wait_until("a")
            self.play(FadeIn(side))
            groups = []
            for m in merges:
                pre = prefix[int(m[2])]
                groups.append(AnimationGroup(Create(tree.edges[pre + "0"]), Create(tree.edges[pre + "1"]),
                                             FadeIn(tree.nodes[pre])))
            vo.wait_until("b")
            self.play(LaggedStart(*groups, lag_ratio=0.5), run_time=max(3.0, vo.remaining() - 0.3))
        L, H = float(hf["L"]), float(hf["H"])
        assert abs(L - 4.127) < 0.001 and abs(H - 4.084) < 0.001 and len(hf["word_bits"]) == 43
        tab = VGroup()
        for s in " etaz":
            tab.add(VGroup(letter(s, font_size=24), Text(codes[s], font=MONO, font_size=22, color=C.BITS))
                    .arrange(RIGHT, buff=0.25))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.45)
        res = VGroup(
            label(rf"average: \ $L = {L:.3f}$ bits per symbol", font_size=28, color=C.BITS),
            label(rf"entropy: \ $H = {H:.3f}$", font_size=28, color=C.ENTROPY),
            label(r"\texttt{the falcon}: \ $43$ bits, \ not $50$", font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.45)
        with self.voiceover(
            "Read off the codewords: <bookmark mark='a'/> the space gets two bits, e, t and a get four, and z gets "
            "ten. <bookmark mark='b'/> On average, 4.127 bits per symbol, just four hundredths of a bit above the "
            "entropy. The falcon now costs forty-three bits instead of fifty. Huffman proved no prefix code for "
            "single symbols does better."
        ) as vo:
            self.play(FadeOut(side))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        head = label(r"Shannon's source coding theorem (1948)", font_size=40).to_edge(UP, buff=0.6)
        body = VGroup(
            label(r"A source with entropy $H$ bits per symbol can be encoded in", font_size=32),
            label(r"as close to $H$ bits per symbol as you like \ \ (code long blocks of symbols),", font_size=32),
            label(r"and, on average, in no fewer.", font_size=32, color=C.BITS),
        ).arrange(DOWN, buff=0.25)
        tag = label(r"entropy is the speed limit of compression", font_size=34, color=C.ENTROPY)
        VGroup(body, tag).arrange(DOWN, buff=0.7).next_to(head, DOWN, buff=0.8)
        box = SurroundingRectangle(body, color=GREY_C, buff=0.35, corner_radius=0.12)
        with self.voiceover(
            "Coding whole blocks of symbols at once spreads that last fraction of a bit thin. The result is "
            "Shannon's source coding theorem: <bookmark mark='a'/> a source with entropy H can be compressed to as "
            "close to H bits per symbol as you like, <bookmark mark='b'/> and, on average, no further. Entropy is "
            "the speed limit of compression."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(body[0]), FadeIn(body[1]), Create(box))
            vo.wait_until("b")
            self.play(FadeIn(body[2]))
            self.play(FadeIn(tag, shift=UP * 0.1))
        self.wait(0.5)
        self.clear_scene()
