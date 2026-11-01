from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import ALPHA27, MONO, PART, code_tree, letter, letter_row, load, plain_axes

SMALL = {"a": "0", "b": "10", "c": "110", "d": "1110", "e": "11110", "f": "11111"}


def dyadic(code: str) -> tuple[float, float]:
    """The interval [0.c, 0.c + 2^-len) of binary fractions that start with the codeword c."""
    lo = int(code, 2) / 2 ** len(code) if code else 0.0
    return lo, lo + 2.0 ** -len(code)


def _bookmark_run_times(vo, mark, *nominal):
    """Fit sequential plays before this utterance's cue, allowing frame rounding.

    Impossible deadlines retain positive one-frame plays, not a synchronization
    guarantee. The actual cue and current elapsed time determine every budget.
    """
    frame = 1 / config.frame_rate
    floor = len(nominal) * frame
    budget = vo.mark_time(mark) - vo.elapsed() - (len(nominal) + 1) * frame
    scale = min(1.0, max(0.0, (budget - floor) / (sum(nominal) - floor)))
    return tuple(frame + (duration - frame) * scale for duration in nominal)


def _bookmark_ladder_step(scene, step, index, vo, mark):
    """Budget only this ladder step's scroll, transform and emphasis plays."""
    run_times = iter(_bookmark_run_times(vo, mark, 0.6, 1.2, 0.8))
    original_play = scene.play
    had_override = "play" in scene.__dict__
    original_override = scene.__dict__.get("play")

    def timed_play(*animations, **kwargs):
        kwargs["run_time"] = next(run_times)
        return original_play(*animations, **kwargs)

    scene.play = timed_play
    try:
        return step(index)
    finally:
        if had_override:
            scene.play = original_override
        else:
            del scene.play


def _decoder_wait_until(scene, vo, mark):
    """Do not start a decoder reveal before its word, even a sub-frame early."""
    gap = vo.mark_time(mark) - vo.elapsed()
    if gap > 0:
        scene.wait(gap)


class Prefix(VoiceoverScene):
    def construct(self):
        self.card()
        self.fixed()
        self.prefix()
        self.kraft()
        self.converse()
        self.mcmillan()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"Prefix codes and the Kraft--McMillan inequality", r"How short can codewords be?",
                            lit=(1948,), part=PART)
        with self.voiceover("Chapter four. Surprise is measured in bits. So let's spend some bits."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def fixed(self):
        hf = load("huffman")
        word = hf["word"]
        nfix = int(hf["fixed_bits"])
        p = load("letters")["p"]
        ratio = float(p[ALPHA27.index("e")] / p[ALPHA27.index("z")])
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
        tot = label(rf"${len(word)}$ symbols $\times\ 5$ bits $= {nfix}$ bits", font_size=32).next_to(codes, DOWN,
                                                                                               buff=0.5)
        waste = label(rf"but \texttt{{e}} is ${ratio:.0f}$ times more common than \texttt{{z}}", font_size=28,
                      color=C.SURPRISE).next_to(tot, DOWN, buff=0.4)
        with self.voiceover(
            "The simplest way to send letters as bits is a fixed-length code. Two to the five is thirty-two, enough "
            "for twenty-seven symbols, <bookmark mark='a'/> so each gets a five-bit number. "
            f"<bookmark mark='b'/> The falcon, {len(word)} symbols, costs {nfix} bits. <bookmark mark='c'/> But "
            f"that's wasteful: e is {ratio:.0f} times more common than z, and both cost five bits."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in table[:-1]], lag_ratio=0.15), FadeIn(dots),
                      FadeIn(table[-1]), FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(table, color=C.BITS, scale_factor=1.03))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in codes], lag_ratio=0.12))
            self.play(FadeIn(tot))
            vo.wait_until("c")
            self.play(FadeIn(waste))
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
        tree = code_tree(SMALL, x_range=(-4.2, 3.2), y_top=0.9, dy=0.78, leaf_font=30)
        tree.shift(DOWN * 0.3)
        legend = VGroup(*[VGroup(letter(s, font_size=26), Text(c, font=MONO, font_size=24, color=C.BITS))
                          .arrange(RIGHT, buff=0.3) for s, c in SMALL.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend.move_to(RIGHT * 5.3 + DOWN * 1.3)
        morse_codes = (("e", "·"), ("t", "−"), ("a", "·−"), ("n", "−·"), ("q", "−−·−"), ("z", "−−··"))
        morse = VGroup(*[VGroup(letter(c, font_size=28), Text(m, font=MONO, font_size=30, color=C.BITS))
                         .arrange(RIGHT, buff=0.3) for c, m in morse_codes]).arrange(RIGHT, buff=0.75)
        morse_t = label(r"Morse code: \ the common letters get the short codes", font_size=26, color=GREY_A)
        morse_n = label(r"\ldots and a pause between letters keeps \texttt{e}\,\texttt{t} apart from \texttt{a}",
                        font_size=24, color=GREY_B)
        morse_g = VGroup(morse_t, morse, morse_n).arrange(DOWN, buff=0.3).move_to(DOWN * 1.9)
        with self.voiceover(
            "So give common symbols short codewords, as Morse code gives e a single dot. But careful. "
            "<bookmark mark='a'/> If e is zero, t is one, and a is zero one, then zero one could be e, t, or a. "
            "<bookmark mark='b'/> The fix is a prefix-free code: no codeword starts another. <bookmark mark='c'/> "
            "Then the codewords are the leaves of a binary tree: zero goes left, one goes right, and to decode, you "
            "walk down from the top to a leaf."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bad[0]), FadeIn(morse_t), LaggedStart(*[FadeIn(m) for m in morse],
                                                                                  lag_ratio=0.2), run_time=1.6)
            self.play(FadeIn(morse_n))
            vo.wait_until("a")
            self.play(FadeIn(bad[1]))
            vo.wait_until("b")
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeOut(bad), FadeOut(morse_g), rule.animate.next_to(head, DOWN, buff=0.3))
            self.play(Create(tree[0]), FadeIn(tree[1]), FadeIn(tree[2]), run_time=1.8)
            self.play(FadeIn(tree[3]), FadeIn(legend))
        msg = SMALL["c"] + SMALL["a"] + SMALL["b"] + SMALL["f"]
        bits = Text(msg, font=MONO, font_size=34, color=C.BITS).next_to(rule, DOWN, buff=0.4)
        out = VGroup()
        with self.voiceover(
            "Watch it decode. <bookmark mark='c_right1'/>Right, <bookmark mark='c_right2'/>right, "
            "<bookmark mark='c_left'/>left: <bookmark mark='c_leaf'/>c. Back to the top. "
            "<bookmark mark='a_left'/>Left: <bookmark mark='a_leaf'/>a. "
            "<bookmark mark='b_right'/>Right, <bookmark mark='b_left'/>left: <bookmark mark='b_leaf'/>b. "
            "<bookmark mark='f_path'/>Right five times: <bookmark mark='f_leaf'/>f. No separators needed."
        ) as vo:
            self.play(FadeIn(bits))
            pos = 0
            cues = {
                "c": (("c_right1", "c_right2", "c_left"), "c_leaf"),
                "a": (("a_left",), "a_leaf"),
                "b": (("b_right", "b_left"), "b_leaf"),
                "f": (("f_path",), "f_leaf"),
            }
            for sym in "cabf":
                c = SMALL[sym]
                path = VGroup(*[tree.edges[c[:k + 1]].copy().set_stroke(WHITE, 6) for k in range(len(c))])
                path_marks, leaf_mark = cues[sym]
                if sym == "f":
                    _decoder_wait_until(self, vo, path_marks[0])
                    path_time, = _bookmark_run_times(vo, leaf_mark, 0.4 + 0.25 * len(c))
                    self.play(LaggedStart(*[AnimationGroup(bits[pos + k].animate.set_color(WHITE), Create(path[k]))
                                           for k in range(len(c))], lag_ratio=0.6), run_time=path_time)
                else:
                    for k, mark in enumerate(path_marks):
                        _decoder_wait_until(self, vo, mark)
                        next_mark = path_marks[k + 1] if k + 1 < len(path_marks) else leaf_mark
                        path_time, = _bookmark_run_times(vo, next_mark, (0.4 + 0.25 * len(c)) / len(c))
                        self.play(bits[pos + k].animate.set_color(WHITE), Create(path[k]), run_time=path_time)
                _decoder_wait_until(self, vo, leaf_mark)
                o = letter(sym, font_size=34, color=C.TRUE_P)
                out.add(o)
                out.arrange(RIGHT, buff=0.15).next_to(bits, RIGHT, buff=0.6)
                self.play(FadeIn(o), Indicate(tree.leaves[sym], color=C.TRUE_P), FadeOut(path), run_time=0.6)
                pos += len(c)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kraft(self):
        kr_ = load("kraft")
        leaves_n = [int(v) for v in kr_["leaves"]]
        lmax = int(kr_["prefix"]["lmax"])
        W, y_top, dy = 12.0, 1.9, 0.74
        L = -W / 2
        y_bot = y_top - dy * lmax

        def node(pre):
            a, b = dyadic(pre)
            return np.array([L + W * (a + b) / 2, y_top - dy * len(pre), 0.0])

        # the full tree, lmax deep, faint; the code's own branches drawn over it
        full = VGroup()
        for d in range(1, lmax + 1):
            for v in range(2 ** d):
                pre = format(v, f"0{d}b")
                full.add(Line(node(pre[:-1]), node(pre), color=GREY_D, stroke_width=1.2))
        own = set()
        for c in SMALL.values():
            own.update(c[:k] for k in range(1, len(c) + 1))
        edges = VGroup(*[Line(node(pre[:-1]), node(pre), color=C.BIT0 if pre[-1] == "0" else C.BIT1, stroke_width=3.5)
                         for pre in sorted(own, key=len)])
        palette = [C.TRUE_P, C.MODEL_Q, C.INTERVAL, C.CONTEXT, C.SURPRISE, C.BITS]
        leafs, under, counts = VGroup(), VGroup(), VGroup()
        bottom = VGroup(*[Dot(node(format(v, f"0{lmax}b")), radius=0.045, color=GREY_C) for v in range(2 ** lmax)])
        for (s, c), col, n_ in zip(SMALL.items(), palette, leaves_n):
            leafs.add(VGroup(Dot(node(c), radius=0.09, color=col),
                             letter(s, font_size=24, color=col).next_to(node(c), UP + LEFT * 0.4, buff=0.08)))
            a, b = dyadic(c)
            r = Rectangle(width=W * (b - a), height=0.42, stroke_width=1.5, stroke_color=BACKGROUND, fill_color=col,
                          fill_opacity=0.85).move_to([L + W * (a + b) / 2, y_bot - 0.45, 0])
            under.add(r)
            counts.add(MathTex(rf"2^{{{lmax - len(c)}}}" if n_ > 2 else str(n_), font_size=24 if n_ > 2 else 20,
                               color=BLACK).move_to(r))
        sub = VGroup()  # each codeword's subtree, shaded down to the bottom row
        for c, col in zip(SMALL.values(), palette):
            pts = [node(c)]
            a, b = dyadic(c)
            pts += [np.array([L + W * b - W / 2 ** lmax / 2, y_bot, 0]), np.array([L + W * a + W / 2 ** lmax / 2, y_bot, 0])]
            sub.add(Polygon(*pts, stroke_width=0, fill_color=col, fill_opacity=0.16))
        ends = VGroup(MathTex("0", font_size=26, color=GREY_B).next_to(under[0], DOWN, buff=0.12).align_to(under[0], LEFT),
                      MathTex("1", font_size=26, color=GREY_B).next_to(under[-1], DOWN, buff=0.12).align_to(under[-1], RIGHT))
        cnt = mtex(rf"{' + '.join(str(n_) for n_ in leaves_n)} \le 2^{lmax} = {2 ** lmax}", font_size=34, color=C.BITS)
        cnt.to_corner(UR, buff=0.4)
        kr = mtex(r"\sum_i 2^{\,l_{\max} - l_i} \le 2^{\,l_{\max}} \ \Longrightarrow \ \sum_i 2^{-l_i} \le 1",
                  font_size=36, color=C.BITS).next_to(cnt, DOWN, buff=0.25).align_to(cnt, RIGHT)
        with self.voiceover(
            "Prefix-free codes obey a budget, and the tree shows why. <bookmark mark='a'/> Grow the tree down to the "
            f"longest codeword: {lmax} levels, {2 ** lmax} leaves at the bottom. <bookmark mark='b'/> A codeword of "
            "length l sits l levels down, and everything below it is off limits, so it uses up two to the l max "
            "minus l of the bottom leaves. <bookmark mark='c'/> No codeword starts another, so these shares never "
            f"overlap: together, at most {2 ** lmax}. <bookmark mark='d'/> Divide by two to the l max: two to the "
            "minus length, summed over the codewords, is at most one. That's Kraft's inequality, from Leon Kraft's "
            "1949 master's thesis."
        ) as vo:
            self.play(Create(edges), LaggedStart(*[FadeIn(lf) for lf in leafs], lag_ratio=0.1), run_time=1.6)
            vo.wait_until("a")
            self.add(full)
            self.bring_to_front(edges, leafs)
            self.play(FadeIn(full), FadeIn(bottom), run_time=1.2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(sh) for sh in sub], lag_ratio=0.3), run_time=1.6)
            self.bring_to_front(edges, leafs)
            self.play(LaggedStart(*[FadeIn(r) for r in under], lag_ratio=0.2), FadeIn(counts), FadeIn(ends), run_time=1.4)
            vo.wait_until("c")
            self.play(Write(cnt))
            vo.wait_until("d")
            self.play(Write(kr))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def converse(self):
        kr_ = load("kraft")
        sk = float(kr_["shannon_kraft"])
        ell = np.asarray(kr_["shannon_lengths"])
        canon = list(kr_["canonical"])
        th = theorem_card(r"Kraft's inequality", r"a prefix code with codeword lengths $l_1, \dots, l_n$ exists "
                          r"\textit{if and only if} \ $\sum_i 2^{-l_i} \le 1$", who=r"L.~G.~Kraft (1949)", width=9.6,
                          color=C.BITS).to_edge(UP, buff=0.4)
        how = label(r"given lengths that fit: \ shortest first, \ each takes the leftmost node still free", font_size=26,
                    color=GREY_A).next_to(th, DOWN, buff=0.35)
        p = load("letters")["p"]
        order = list(load("letters")["order"])
        show = [order[0], order[1], order[2], order[12], order[-1]]
        rows = VGroup()
        for i in show:
            rows.add(VGroup(letter(ALPHA27[i], font_size=26),
                            MathTex(rf"\lceil \log_2 \tfrac{{1}}{{{p[i]:.4f}}} \rceil = {int(ell[i])}", font_size=28,
                                    color=GREY_A),
                            Text(canon[i], font=MONO, font_size=24, color=C.BITS)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([-1.2, -1.4, 0])
        tot = mtex(rf"\sum 2^{{-l}} = {sk:.2f} \le 1", font_size=34, color=C.BITS).next_to(rows, RIGHT, buff=0.9)
        # lengths 1, 2, 3, 3 placed shortest first, each at the leftmost free node of its depth
        TW, ty, tdy = 7.0, 0.75, 0.85

        def tnode(pre):
            a_, b_ = dyadic(pre)
            return np.array([-TW / 2 + TW * (a_ + b_) / 2, ty - tdy * len(pre), 0.0])

        faint = VGroup(*[Line(tnode(format(v, f"0{d}b")[:-1]), tnode(format(v, f"0{d}b")), color=GREY_D,
                              stroke_width=1.5) for d in range(1, 4) for v in range(2 ** d)])
        demo = ["0", "10", "110", "111"]
        cols = [C.TRUE_P, C.MODEL_Q, C.INTERVAL, C.CONTEXT]
        placed = VGroup()
        for c, col in zip(demo, cols):
            path = VGroup(*[Line(tnode(c[:k - 1]), tnode(c[:k]), color=col, stroke_width=4) for k in range(1, len(c) + 1)])
            a_, b_ = dyadic(c)
            shade = Polygon(tnode(c), np.array([-TW / 2 + TW * a_ + 0.15, ty - tdy * 3, 0]),
                            np.array([-TW / 2 + TW * b_ - 0.15, ty - tdy * 3, 0]), stroke_width=0, fill_color=col,
                            fill_opacity=0.18) if len(c) < 3 else VMobject()
            word = Text(c, font=MONO, font_size=26, color=col).next_to(tnode(c), DOWN, buff=0.15)
            if len(c) < 3:
                word.next_to(tnode(c), LEFT, buff=0.15)
            placed.add(VGroup(shade, path, Dot(tnode(c), radius=0.07, color=col), word))
        demo_t = label(r"lengths $1, 2, 3, 3$: \ $\tfrac12 + \tfrac14 + \tfrac18 + \tfrac18 = 1$", font_size=28,
                       color=GREY_A).next_to(VGroup(faint, placed), DOWN, buff=0.35)
        with self.voiceover(
            "The budget is also enough. <bookmark mark='a'/> Hand me any lengths whose powers of a half add up to "
            "at most one, and a prefix code with those lengths exists: give out codewords shortest first, each at "
            "the leftmost free node of its depth. <bookmark mark='b'/> For example, round each letter's surprise up "
            f"to whole bits. The powers of a half add up to {sk:.2f}, so here is a prefix code with those lengths. "
            "We'll meet it again next chapter."
        ) as vo:
            self.play(FadeIn(th, shift=DOWN * 0.2), Create(faint))
            vo.wait_until("a")
            self.play(FadeIn(how), FadeIn(demo_t))
            for g_ in placed:
                self.play(FadeIn(g_[0]), Create(g_[1]), FadeIn(g_[2]), FadeIn(g_[3]), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeOut(VGroup(faint, placed, demo_t)))
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25), run_time=2.0)
            self.play(Write(tot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mcmillan(self):
        kr_ = load("kraft")
        ud, bad = kr_["ud"], kr_["bad"]
        kx = int(kr_["bad_cross"])
        un, ud_ = (int(x) for x in ud["kraft_frac"].split("/"))
        bn, bd = (int(x) for x in bad["kraft_frac"].split("/"))
        head = label(r"Do prefix codes lose anything?", font_size=36).to_edge(UP, buff=0.35)
        codes = VGroup()
        for name, d, col in ((r"decodable, \ not prefix-free", ud, C.INTERVAL), (r"not decodable", bad, C.SURPRISE)):
            words = r",\ ".join(rf"\texttt{{{c}}}" for c in d["code"].values())
            codes.add(VGroup(label(name, font_size=24, color=col),
                             label(rf"$\{{${words}$\}}$ \quad $\sum 2^{{-l}} = {d['kraft_frac']}$", font_size=26)
                             ).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        codes.arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_corner(UL, buff=0.5).shift(DOWN * 0.7)
        cw = ud["code"]
        msg_ud = ["d", "a", "b", "c"]
        parts = VGroup(*[Text(cw[m], font=MONO, font_size=28, color=WHITE) for m in msg_ud]).arrange(RIGHT, buff=0.3)
        for t_ in parts:
            t_[0].set_color(C.INTERVAL)  # every codeword starts with the 0 that announces it
        syms = VGroup(*[letter(m, font_size=26, color=C.INTERVAL).next_to(t_, DOWN, buff=0.15) for m, t_ in
                        zip(msg_ud, parts)])
        ud_demo = VGroup(parts, syms).move_to([3.0, codes[0].get_y() - 0.1, 0])
        bw = bad["code"]
        amb = VGroup(Text(bw["c"], font=MONO, font_size=28, color=WHITE), MathTex(r"\to", font_size=30),
                     data_text("a b", font=MONO, font_size=26, color=C.SURPRISE), label(r"or", font_size=26, color=GREY_B),
                     Text("c", font=MONO, font_size=26, color=C.SURPRISE), MathTex("?", font_size=34, color=C.SURPRISE))
        amb.arrange(RIGHT, buff=0.25).move_to([3.0, codes[1].get_y() - 0.05, 0])
        rows = [
            cmath(r"\Big(\sum_i 2^{-l_i}\Big)^k", r"=", r"\sum_{\text{messages of } k \text{ codewords}} 2^{-\text{length}}",
                  font_size=32),
            cmath(r"\Big(\sum_i 2^{-l_i}\Big)^k", r"=", r"\sum_{m=1}^{k\, l_{\max}} A_m\, 2^{-m}", font_size=32),
            cmath(r"\Big(\sum_i 2^{-l_i}\Big)^k", r"\le", r"\sum_{m=1}^{k\, l_{\max}} 2^m\, 2^{-m} = k\, l_{\max}",
                  font_size=32),
        ]
        whys = [why(r"multiply out"), why(r"$A_m$: messages that are $m$ bits long"),
                why(r"decodable: \ $A_m \le 2^m$")]
        step = ladder(self, rows, whys, keep=3, top=0.9, x=0.9, buff=0.42, edge=6.9)
        # the bad code's (5/4)^k outgrows k * lmax
        P = np.asarray(bad["powers"])
        K = len(P)
        ax_g = axes([0, K], [-1, 2], x_length=5.2, y_length=3.0, xlabel=r"$k$ codewords per message",
                    ylabel=r"(log scale)", xticks=[0, 10, 20], yticks=[-1, 0, 1, 2],
                    yfmt=lambda v: rf"10^{{{int(v)}}}", center=[3.7, -1.55, 0], font_size=18)
        ax = ax_g.ax
        ks = np.arange(1, K + 1)
        lin = curve(ax, ks, np.log10(ks * bad["lmax"]), GREY_A, 2.5)
        grow = curve(ax, ks, np.log10(P), C.SURPRISE, 3.5)
        good = curve(ax, ks, np.log10(np.asarray(ud["powers"])), C.INTERVAL, 3.5)
        cross = glow_dot(ax.c2p(kx, math.log10(P[kx - 1])), color=C.SURPRISE, radius=0.07)
        leg = VGroup(label(rf"$({bad['kraft_frac']})^k$", font_size=22, color=C.SURPRISE),
                     label(rf"$k\, l_{{\max}} = {bad['lmax']}k$", font_size=22, color=GREY_A),
                     label(rf"$({ud['kraft_frac']})^k$", font_size=22, color=C.INTERVAL)).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.08)
        leg.next_to(ax_g, LEFT, buff=0.35).shift(UP * 0.3)
        th = label(r"McMillan (1956): \\ \textit{every} decodable code \\ obeys $\sum 2^{-l_i} \le 1$", font_size=30,
                   color=C.BITS).move_to([-3.6, -2.2, 0])
        tag = computed_tag()
        tag.next_to(ax_g, UP, buff=0.05).align_to(ax_g, RIGHT)
        with self.voiceover(
            "Could a code that isn't prefix-free do better? <bookmark mark='a'/> This one isn't: zero starts zero "
            "one. Yet it decodes, because every codeword begins with a zero, and a zero always means a new "
            f"codeword. Its sum is {un} over {ud_}. <bookmark mark='b'/> This one, with sum {bn} over {bd}, can't "
            "be decoded: zero one is a b, or c. <bookmark mark='c'/> In 1956 Brockway McMillan showed the budget "
            "binds every decodable code. Raise the sum to a power k and multiply out: each term is a message of k "
            "codewords. <bookmark mark='d'/> Group the messages by their length in bits. <bookmark mark='e'/> If "
            "the code decodes, different messages never give the same bits, so at most two to the m are m bits "
            "long, and the sum is at most k times the longest length."
        ) as vo:
            self.play(FadeIn(head), FadeIn(codes[0]))
            vo.wait_until("a")
            self.play(Indicate(codes[0], color=C.INTERVAL, scale_factor=1.04))
            self.play(LaggedStart(*[FadeIn(VGroup(t_, y_)) for t_, y_ in zip(parts, syms)], lag_ratio=0.4),
                      run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(codes[1]), FadeIn(amb))
            vo.wait_until("c")
            self.play(FadeOut(ud_demo), FadeOut(amb))
            step(0)
            vo.wait_until("d")
            _bookmark_ladder_step(self, step, 1, vo, "e")
            vo.wait_until("e")
            step(2)
        with self.voiceover(
            "A sum above one, raised to the k, grows exponentially; k times a constant grows in a straight line. "
            f"<bookmark mark='a'/> For the bad code, five fourths to the k overtakes two k at k equals {kx}: the "
            "bound breaks, so it can't be decodable. <bookmark mark='b'/> So prefix codes lose nothing: any lengths "
            "a decodable code can have, a prefix code can have too."
        ) as vo:
            final_step = VGroup(rows[2], whys[2])
            final_step.generate_target()
            final_step.target.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-2.8, 0.25, 0])
            self.play(FadeOut(VGroup(rows[0], rows[1], whys[0], whys[1])), MoveToTarget(final_step))
            self.play(FadeIn(ax_g), FadeIn(tag), Create(lin), Create(good), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(grow), run_time=1.6)
            self.play(FadeIn(cross, scale=0.5))
            vo.wait_until("b")
            self.play(FadeIn(th, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
